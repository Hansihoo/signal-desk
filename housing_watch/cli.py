import argparse
import os
import sys

from .ai_brief import format_ai_issue_summary, render_ai_news_html
from .ai_news import AINewsFetchError, collect_ai_news
from .config import database_path, enabled_sources, load_config, scoped_regions
from .db import connect, init_db, prune_items_outside_regions, prune_items_outside_sources, record_snapshot, upsert_items
from .desk import render_desk_html
from .jobs import (
    JobFetchError,
    JobImportError,
    collect_jobs_from_json,
    collect_jobs_from_saramin,
    load_job_source_config,
    saramin_options_from_config,
)
from .news import NewsFetchError, collect_weekly_news
from .report import write_report
from .render import export_image, render_brief_html, render_html
from .review import format_review, review_project
from .public_site import build_public_site, collect_public_data
from .search import format_context, format_search_results, search_items
from .sources import FetchError, fetch_source


def main(argv=None):
    _configure_stdio()
    parser = argparse.ArgumentParser(description="Housing Watch MVP")
    parser.add_argument("--config", default="config/sources.json", help="source config path")
    sub = parser.add_subparsers(dest="command", required=True)

    collect = sub.add_parser("collect", help="fetch configured sources and update SQLite")
    collect.add_argument("--source", help="collect only one source id")

    search = sub.add_parser("search", help="search local notices")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=8)

    context = sub.add_parser("context", help="print Codex-friendly search context")
    context.add_argument("query")
    context.add_argument("--limit", type=int, default=8)

    sub.add_parser("report", help="write Markdown report")
    sub.add_parser("render", help="write mobile HTML briefing")

    brief = sub.add_parser("brief", help="write concise mobile HTML briefing and PNG")
    brief.add_argument("--collect", action="store_true", help="collect sources before rendering")
    brief.add_argument("--limit", type=int, default=5, help="maximum notices in the concise briefing")
    brief.add_argument("--width", type=int, default=390, help="maximum mobile image width in pixels")
    brief.add_argument("--height", type=int, default=1500, help="screenshot height in pixels")
    brief.add_argument("--html", default="site/brief.html", help="brief HTML output path")
    brief.add_argument("--image", default="reports/brief.png", help="brief image output path")
    brief.add_argument("--profile", help="optional local profile markdown path for conservative eligibility filtering")
    brief.add_argument("--show-profile-excluded", action="store_true", help="show profile-excluded housing items instead of hiding them")
    brief.add_argument("--no-image", action="store_true", help="skip PNG export")

    desk = sub.add_parser("desk", help="write tabbed Signal Desk HTML and selected-tab PNG")
    desk.add_argument("--collect", action="store_true", help="collect housing sources before rendering")
    desk.add_argument("--tab", choices=["summary", "housing", "weekly-news", "jobs"], default="summary", help="active tab to render/export")
    desk.add_argument("--limit", type=int, default=5, help="maximum cards per populated tab")
    desk.add_argument("--width", type=int, default=645, help="maximum mobile desk image width in pixels")
    desk.add_argument("--height", type=int, default=1500, help="screenshot height in pixels")
    desk.add_argument("--html", default="site/desk.html", help="desk HTML output path")
    desk.add_argument("--image", help="desk image output path; defaults to reports/desk-{tab}.png")
    desk.add_argument("--profile", help="optional local profile markdown path for conservative housing eligibility filtering")
    desk.add_argument("--show-profile-excluded", action="store_true", help="show profile-excluded housing items instead of hiding them")
    desk.add_argument("--no-image", action="store_true", help="skip PNG export")

    news = sub.add_parser("news", help="collect weekly big news and render the news tab")
    news.add_argument("--source", choices=["auto", "gdelt", "google-news"], default="auto", help="news source strategy")
    news.add_argument("--limit", type=int, default=12, help="maximum news candidates to keep")
    news.add_argument("--width", type=int, default=645, help="maximum mobile desk image width in pixels")
    news.add_argument("--height", type=int, default=1500, help="screenshot height in pixels")
    news.add_argument("--html", default="site/desk.html", help="desk HTML output path")
    news.add_argument("--image", default="reports/desk-weekly-news.png", help="weekly news image output path")
    news.add_argument("--translate-url", help="optional LibreTranslate base URL")
    news.add_argument("--translate-key", help="optional LibreTranslate API key")
    news.add_argument("--no-render", action="store_true", help="collect only; skip HTML and PNG")
    news.add_argument("--no-image", action="store_true", help="skip PNG export")

    ai_news = sub.add_parser("ai-news", help="collect AI developer news and render a 3-page briefing")
    ai_news.add_argument("--limit", type=int, default=24, help="maximum AI news candidates to keep")
    ai_news.add_argument("--days", type=int, default=7, help="collect and render items from the latest N days")
    ai_news.add_argument("--per-page", type=int, default=6, help="maximum cards per page")
    ai_news.add_argument("--page", type=int, choices=[1, 2, 3], default=1, help="initial page to render/export")
    ai_news.add_argument("--width", type=int, default=645, help="maximum mobile briefing width in pixels")
    ai_news.add_argument("--height", type=int, default=1500, help="screenshot height in pixels")
    ai_news.add_argument("--html", default="site/ai-news.html", help="AI briefing HTML output path")
    ai_news.add_argument("--image", help="AI briefing image output path; defaults to reports/ai-news-page{page}.png")
    ai_news.add_argument("--no-collect", action="store_true", help="render from existing local AI news rows")
    ai_news.add_argument("--no-render", action="store_true", help="collect only; skip HTML and PNG")
    ai_news.add_argument("--no-image", action="store_true", help="skip PNG export")

    issues = sub.add_parser("issues", aliases=["issue", "이슈"], help="pull the latest weekly AI developer issues")
    issues.add_argument("--limit", type=int, default=18, help="maximum weekly issues to report")
    issues.add_argument("--days", type=int, default=7, help="issue lookback window in days")
    issues.add_argument("--per-page", type=int, default=6, help="maximum cards per page")
    issues.add_argument("--page", type=int, choices=[1, 2, 3], default=1, help="initial page to render/export")
    issues.add_argument("--width", type=int, default=645, help="maximum mobile briefing width in pixels")
    issues.add_argument("--height", type=int, default=1500, help="screenshot height in pixels")
    issues.add_argument("--html", default="site/ai-news.html", help="AI briefing HTML output path")
    issues.add_argument("--image", help="AI briefing image output path; defaults to reports/ai-news-page{page}.png")
    issues.add_argument("--no-collect", action="store_true", help="render/report from existing local AI news rows")
    issues.add_argument("--no-render", action="store_true", help="collect and print only; skip HTML and PNG")
    issues.add_argument("--no-image", action="store_true", help="skip PNG export")

    jobs = sub.add_parser("jobs", help="import career job items and render the jobs tab")
    jobs.add_argument("--input", help="normalized jobs JSON file to import")
    jobs.add_argument("--fetch", choices=["saramin"], help="fetch live jobs from a supported source")
    jobs.add_argument("--jobs-config", default="config/job_sources.json", help="jobs source config path")
    jobs.add_argument("--keyword", action="append", help="keyword for live job search; can be repeated")
    jobs.add_argument("--count", type=int, help="maximum live jobs to request per keyword")
    jobs.add_argument("--min-fit-score", type=int, help="minimum local fit score for live jobs")
    jobs.add_argument("--salary-estimates", help="company salary estimates JSON path")
    jobs.add_argument("--source-id", default="manual_jobs", help="source id to use for imported JSON")
    jobs.add_argument("--limit", type=int, default=5, help="maximum job cards to show")
    jobs.add_argument("--width", type=int, default=645, help="maximum mobile desk image width in pixels")
    jobs.add_argument("--height", type=int, default=1500, help="screenshot height in pixels")
    jobs.add_argument("--html", default="site/desk.html", help="desk HTML output path")
    jobs.add_argument("--image", default="reports/desk-jobs.png", help="jobs image output path")
    jobs.add_argument("--no-render", action="store_true", help="import only; skip HTML and PNG")
    jobs.add_argument("--no-image", action="store_true", help="skip PNG export")

    image = sub.add_parser("export-image", help="export latest HTML briefing to PNG")
    image.add_argument("--html", default="site/latest.html")
    image.add_argument("--out", default="reports/latest.png")
    image.add_argument("--width", type=int, default=430)
    image.add_argument("--height", type=int, default=1200)

    review = sub.add_parser("review", help="review generated data, brief HTML, and image")
    review.add_argument("--html", default="site/brief.html")
    review.add_argument("--image", default="reports/brief.png")
    review.add_argument("--width", type=int, default=390)

    publish = sub.add_parser("publish", help="build public-source dashboard and dated archive")
    publish.add_argument("--collect", action="store_true", help="refresh public sources before building")
    publish.add_argument("--output", default="site", help="static site output directory")

    args = parser.parse_args(argv)
    config = load_config(args.config)
    conn = connect(database_path(config))
    init_db(conn)

    if args.command == "publish":
        try:
            health = collect_public_data(conn, config) if args.collect else []
            result = build_public_site(conn, args.output, health)
            print("Wrote %(path)s: %(items)d public items, %(archives)d dated briefings" % result)
            for source in health:
                if not source["ok"]:
                    print("source warning: %s: %s" % (source["source"], source["message"]), file=sys.stderr)
            return 0
        except (OSError, ValueError, RuntimeError) as exc:
            print("publish: failed: %s" % exc, file=sys.stderr)
            return 1
        finally:
            conn.close()

    if args.command == "collect":
        return cmd_collect(conn, config, args.source)
    if args.command == "search":
        results = search_items(conn, args.query, args.limit)
        print(format_search_results(results))
        return 0
    if args.command == "context":
        results = search_items(conn, args.query, args.limit)
        print(format_context(results, args.query))
        return 0
    if args.command == "report":
        paths = write_report(conn)
        print("Wrote %s and %s" % (paths["weekly"], paths["latest"]))
        return 0
    if args.command == "render":
        path = render_html(conn)
        print("Wrote %s" % path)
        return 0
    if args.command == "brief":
        if args.collect:
            collect_status = cmd_collect(conn, config)
            if collect_status != 0:
                return collect_status
        html_path = render_brief_html(
            conn,
            args.html,
            args.limit,
            args.width,
            profile_path=args.profile,
            hide_profile_excluded=not args.show_profile_excluded,
        )
        print("Wrote %s" % html_path)
        if not args.no_image:
            image_path = export_image(html_path, args.image, args.width, args.height)
            print("Wrote %s" % image_path)
        return 0
    if args.command == "desk":
        if args.collect:
            collect_status = cmd_collect(conn, config)
            if collect_status != 0:
                return collect_status
        html_path = render_desk_html(
            conn,
            args.html,
            args.tab,
            args.limit,
            args.width,
            profile_path=args.profile,
            hide_profile_excluded=not args.show_profile_excluded,
        )
        print("Wrote %s" % html_path)
        if not args.no_image:
            image_path = args.image or "reports/desk-%s.png" % args.tab
            image_path = export_image(html_path, image_path, args.width, args.height)
            print("Wrote %s" % image_path)
        return 0
    if args.command == "news":
        try:
            result = collect_weekly_news(
                conn,
                source=args.source,
                limit=args.limit,
                translate_url=args.translate_url,
                translate_key=args.translate_key,
            )
        except NewsFetchError as exc:
            print("news: failed: %s" % exc, file=sys.stderr)
            return 1
        print(
            "%s: fetched=%d inserted=%d updated=%d deduped=%d raw=%s"
            % (
                result["source_id"],
                result["fetched"],
                result["inserted"],
                result["updated"],
                result.get("deduped", 0),
                result["raw_path"],
            )
        )
        for failure in result["failures"]:
            print("fallback: %s" % failure, file=sys.stderr)
        if not args.no_render:
            html_path = render_desk_html(conn, args.html, "weekly-news", args.limit, args.width)
            print("Wrote %s" % html_path)
            if not args.no_image:
                image_path = export_image(html_path, args.image, args.width, args.height)
                print("Wrote %s" % image_path)
        return 0
    if args.command in ("ai-news", "issues", "issue", "이슈"):
        if not args.no_collect:
            try:
                result = collect_ai_news(conn, limit=args.limit, days=args.days)
            except AINewsFetchError as exc:
                print("ai-news: failed: %s" % exc, file=sys.stderr)
                return 1
            print(
                "%s: days=%d fetched=%d inserted=%d updated=%d deduped=%d raw=%s"
                % (
                    result["source_id"],
                    result.get("days", args.days),
                    result["fetched"],
                    result["inserted"],
                    result["updated"],
                    result.get("deduped", 0),
                    result["raw_path"],
                )
            )
            for failure in result["failures"]:
                print("source warning: %s" % failure, file=sys.stderr)
        if not args.no_render:
            html_path = render_ai_news_html(conn, args.html, args.per_page, args.width, args.page, days=args.days)
            print("Wrote %s" % html_path)
            if not args.no_image:
                image_path = args.image or "reports/ai-news-page%d.png" % args.page
                image_path = export_image(html_path, image_path, args.width, args.height)
                print("Wrote %s" % image_path)
        if args.command in ("issues", "issue", "이슈"):
            print()
            print(format_ai_issue_summary(conn, limit=args.limit, days=args.days))
        return 0
    if args.command == "jobs":
        fetched_any = False
        if args.input:
            try:
                result = collect_jobs_from_json(conn, args.input, source_id=args.source_id)
            except JobImportError as exc:
                print("jobs: failed: %s" % exc, file=sys.stderr)
                return 1
            print(
                "%s: fetched=%d inserted=%d updated=%d raw=%s"
                % (
                    result["source_id"],
                    result["fetched"],
                    result["inserted"],
                    result["updated"],
                    result["raw_path"],
                )
            )
            fetched_any = True
        if args.fetch == "saramin":
            try:
                source_config = load_job_source_config(args.jobs_config)
                saramin_options = saramin_options_from_config(source_config)
                env_key = saramin_options["env_key"]
                access_key = None
                if env_key != "SIGNAL_DESK_SARAMIN_KEY":
                    access_key = os.environ.get(env_key)
                    if not access_key:
                        raise JobFetchError("%s is not set" % env_key)
                result = collect_jobs_from_saramin(
                    conn,
                    access_key=access_key,
                    keywords=args.keyword or saramin_options["keywords"] or None,
                    count=args.count or saramin_options["count"],
                    source_id="saramin_api",
                    salary_estimates_path=args.salary_estimates or saramin_options["salary_estimates_path"],
                    minimum_fit_score=(
                        args.min_fit_score
                        if args.min_fit_score is not None
                        else saramin_options["minimum_fit_score"]
                    ),
                    params=saramin_options["params"],
                )
            except (JobFetchError, JobImportError) as exc:
                print("jobs: failed: %s" % exc, file=sys.stderr)
                return 1
            print(
                "%s: fetched=%d kept=%d inserted=%d updated=%d raw=%s"
                % (
                    result["source_id"],
                    result["fetched"],
                    result["kept"],
                    result["inserted"],
                    result["updated"],
                    result["raw_path"],
                )
            )
            fetched_any = True
        if not fetched_any and args.no_render:
            print("jobs: --input or --fetch is required when --no-render is used", file=sys.stderr)
            return 1
        if not args.no_render:
            html_path = render_desk_html(conn, args.html, "jobs", args.limit, args.width)
            print("Wrote %s" % html_path)
            if not args.no_image:
                image_path = export_image(html_path, args.image, args.width, args.height)
                print("Wrote %s" % image_path)
        return 0
    if args.command == "export-image":
        path = export_image(args.html, args.out, args.width, args.height)
        print("Wrote %s" % path)
        return 0
    if args.command == "review":
        result = review_project(conn, args.html, args.image, args.width)
        print(format_review(result))
        return 0 if result["ok"] else 1
    parser.print_help()
    return 1


def _configure_stdio():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def cmd_collect(conn, config, source_id=None):
    sources = enabled_sources(config, source_id)
    if not sources:
        print("No matching enabled sources.")
        return 1

    total_inserted = 0
    total_updated = 0
    failures = []
    for source in sources:
        try:
            result = fetch_source(source)
            items = result["items"]
            stats = upsert_items(conn, items, config.get("interest", {}))
            record_snapshot(conn, result["source_id"], result["raw_path"], len(items))
            conn.commit()
            total_inserted += stats["inserted"]
            total_updated += stats["updated"]
            print(
                "%s: fetched=%d inserted=%d updated=%d raw=%s"
                % (source["id"], len(items), stats["inserted"], stats["updated"], result["raw_path"])
            )
        except (FetchError, OSError, ValueError) as exc:
            failures.append((source["id"], str(exc)))
            print("%s: failed: %s" % (source["id"], exc), file=sys.stderr)

    pruned_sources = prune_items_outside_sources(conn, [source["id"] for source in sources])
    pruned_regions = prune_items_outside_regions(conn, scoped_regions(config))
    pruned = pruned_sources + pruned_regions
    if pruned_sources:
        print("Pruned %d items from disabled or renamed sources." % pruned_sources)
    if pruned_regions:
        print("Pruned %d items outside configured regions." % pruned_regions)
    print("Done. inserted=%d updated=%d pruned=%d failed=%d" % (total_inserted, total_updated, pruned, len(failures)))
    return 1 if failures and not (total_inserted or total_updated) else 0


if __name__ == "__main__":
    raise SystemExit(main())
