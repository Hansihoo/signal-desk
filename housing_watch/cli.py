import argparse
import sys

from .config import database_path, enabled_sources, load_config, scoped_regions
from .db import connect, init_db, prune_items_outside_regions, prune_items_outside_sources, record_snapshot, upsert_items
from .report import write_report
from .render import export_image, render_brief_html, render_html
from .review import format_review, review_project
from .search import format_context, format_search_results, search_items
from .sources import FetchError, fetch_source


def main(argv=None):
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
    brief.add_argument("--no-image", action="store_true", help="skip PNG export")

    image = sub.add_parser("export-image", help="export latest HTML briefing to PNG")
    image.add_argument("--html", default="site/latest.html")
    image.add_argument("--out", default="reports/latest.png")
    image.add_argument("--width", type=int, default=430)
    image.add_argument("--height", type=int, default=1200)

    review = sub.add_parser("review", help="review generated data, brief HTML, and image")
    review.add_argument("--html", default="site/brief.html")
    review.add_argument("--image", default="reports/brief.png")
    review.add_argument("--width", type=int, default=390)

    args = parser.parse_args(argv)
    config = load_config(args.config)
    conn = connect(database_path(config))
    init_db(conn)

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
        html_path = render_brief_html(conn, args.html, args.limit, args.width)
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
