"""Public-source collection and a persistent, searchable static briefing archive."""

import html
import hashlib
import json
import re
from pathlib import Path

from .ai_brief import render_ai_news_html
from .ai_news import AINewsFetchError, collect_ai_news
from .briefing_preview import build_briefing_preview
from .config import enabled_sources
from .db import all_items, record_snapshot, upsert_items
from .news import NewsFetchError, collect_weekly_news
from .render import render_brief_html
from .research_topics import collect_topic_feeds, load_topics, opportunity_outline, public_url, topic_for_item
from .research_data import build_research_data, write_research_data
from .sources import fetch_source
from .timeutil import iso_utc, now_kst


def collect_public_data(conn, config, topics=None):
    topics = topics if topics is not None else load_topics()
    health = []
    housing = next((topic for topic in topics if topic["collector"] == "housing"), None)
    for source in enabled_sources(config) if housing else []:
        try:
            result = fetch_source(source)
            stats = upsert_items(conn, result["items"], config.get("interest", {}))
            record_snapshot(conn, source["id"], result["raw_path"], len(result["items"]))
            conn.commit()
            health.append({"source": source["name"], "topic_id": housing["id"], "ok": True, "count": len(result["items"])})
            print("%s: fetched=%d inserted=%d updated=%d" % (source["id"], len(result["items"]), stats["inserted"], stats["updated"]))
        except (OSError, ValueError, RuntimeError) as exc:
            health.append({"source": source["name"], "topic_id": housing["id"], "ok": False, "message": str(exc)})
    for topic in topics:
        name = topic["name"]
        if topic["collector"] in ("housing", "planned"):
            continue
        try:
            if topic["collector"] == "ai":
                result = collect_ai_news(conn, limit=topic.get("limit", 120), days=topic.get("days", 7))
            elif topic["collector"] == "news":
                result = collect_weekly_news(conn, source=topic.get("source", "auto"), limit=topic.get("limit", 40))
            else:
                result = collect_topic_feeds(conn, topic)
            health.append({"source": name, "topic_id": topic["id"], "ok": True, "count": result["fetched"], "warnings": result["failures"]})
            print("%s: fetched=%d warnings=%d" % (name, result["fetched"], len(result["failures"])))
        except (OSError, ValueError, RuntimeError, AINewsFetchError, NewsFetchError) as exc:
            health.append({"source": name, "topic_id": topic["id"], "ok": False, "message": str(exc)})
    return health


def public_library(conn, topics=None):
    topics = topics if topics is not None else load_topics()
    entries = []
    for row in conn.execute("SELECT * FROM news_items ORDER BY published_at DESC, id DESC"):
        item = dict(row)
        try:
            payload = json.loads(item.get("raw_payload") or "{}")
        except (ValueError, TypeError):
            payload = {}
        if not isinstance(payload, dict):
            payload = {}
        topic = topic_for_item(topics, item["source_id"])
        if topic is None:
            continue
        entries.append({
            "id": "news-%s" % item["id"],
            "topic": topic["name"], "topic_id": topic["id"],
            "title": item.get("title_ko") or item["title"],
            "summary": str(payload.get("detail") or item.get("summary_ko") or "")[:400],
            "url": _public_url(item["url"]),
            "source": item.get("source_name") or item["source_id"],
            "category": item.get("category") or "",
            "published_at": item.get("published_at") or "",
            "first_seen_at": item["first_seen_at"],
            "score": item.get("score") or 0,
            "basis": "공식 출처" if payload.get("source_tier") == "official" else "피드·원문 링크",
        })
    for item in all_items(conn):
        topic = topic_for_item(topics, item["source_id"], housing=True)
        if topic is None:
            continue
        entries.append({
            "id": "housing-%s" % item["id"], "topic": topic["name"], "topic_id": topic["id"],
            "title": item["title"], "summary": (item.get("detail_summary") or item.get("summary") or "")[:400],
            "url": _public_url(item["url"]), "source": item.get("agency") or item["source_id"],
            "category": item.get("category") or "", "published_at": item.get("published_at") or "",
            "first_seen_at": item["first_seen_at"], "score": item.get("importance") or 0,
            "basis": "공식 공고", "status": item.get("status") or "",
        })
    return [entry for entry in entries if entry["url"]]


def _public_url(value):
    return public_url(value)


def build_public_site(conn, output_path="site", health=None, topics=None):
    topics = topics if topics is not None else load_topics()
    output = Path(output_path)
    output.mkdir(parents=True, exist_ok=True)
    entries = public_library(conn, topics)
    if not entries:
        raise ValueError("No public data is available; refusing to publish an empty site.")
    created_at = iso_utc()
    date = now_kst().strftime("%Y-%m-%d")
    archive = output / "archive"
    archive.mkdir(exist_ok=True)
    archive_index = archive / "index.json"
    history = json.loads(archive_index.read_text(encoding="utf-8")) if archive_index.exists() else []
    if not isinstance(history, list) or any(not isinstance(entry, dict) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", entry.get("date", "")) for entry in history):
        raise ValueError("Invalid archive index; existing archive must be repaired before publishing.")
    catalog = _topic_catalog(topics, entries)
    snapshot = {"date": date, "created_at": created_at, "items": entries, "health": health or [], "topics": catalog}
    for suffix in ("css", "js"):
        asset = Path(__file__).with_name("public_site." + suffix)
        (output / asset.name).write_bytes(asset.read_bytes())
    daily = archive / date
    if not (daily / "briefing.json").exists():
        daily.mkdir(exist_ok=True)
        _write_json(daily / "briefing.json", snapshot)
        history = [entry for entry in history if entry["date"] != date]
        history.append({"date": date, "created_at": created_at, "count": len(entries)})
    history.sort(key=lambda entry: entry["date"], reverse=True)
    _write_json(archive_index, history)
    _write_json(output / "library.json", entries)
    _write_json(output / "topics.json", catalog)
    _write_json(output / "status.json", {"generated_at": created_at, "count": len(entries), "health": health or []})
    _write_page(output / "index.html", snapshot, history)
    for topic in catalog:
        topic_path = output / "research" / topic["id"]
        topic_path.mkdir(parents=True, exist_ok=True)
        selected = dict(snapshot, items=[item for item in entries if item["topic_id"] == topic["id"]],
                        health=[entry for entry in snapshot["health"] if entry.get("topic_id") == topic["id"]])
        _write_page(topic_path / "index.html", selected, history, "../../", selected_topic=topic["id"])
        if topic.get("view") == "opportunities":
            _write_opportunity_template(topic_path / "report-template.html", opportunity_outline())
    # Each dated page is rebuilt from its saved snapshot, never from today's rows.
    for entry in history:
        saved = archive / entry["date"] / "briefing.json"
        if not saved.is_file():
            raise ValueError("Missing archived briefing: %s" % entry["date"])
        _write_page(saved.parent / "index.html", json.loads(saved.read_text(encoding="utf-8")), history, "../../", archived=True)
    render_ai_news_html(conn, str(output / "ai-news.html"), per_page=6, days=7)
    # Explicitly omit private profile filtering from the public housing page.
    render_brief_html(conn, str(output / "brief.html"), hide_profile_excluded=False, use_profile=False)
    (output / ".nojekyll").write_text("", encoding="utf-8")
    research_data = build_research_data(conn, entries, topics, health)
    write_research_data(output / "research-data.json", research_data)
    report = next(report for report in research_data["reports"] if report["id"] == research_data["featured_report_id"])
    build_briefing_preview(output, snapshot, report, research_data, standalone=False)
    return {"path": str(output / "index.html"), "items": len(entries), "archives": len(history), "health": health or []}


def _write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def _topic_catalog(topics, entries):
    catalog = []
    for topic in topics:
        items = [item for item in entries if item["topic_id"] == topic["id"]]
        entry = {"id": topic["id"], "name": topic["name"], "description": topic.get("description", ""),
                        "detail_page": topic.get("detail_page", ""), "count": len(items),
                        "latest": max((item["published_at"] or item["first_seen_at"] for item in items), default="")}
        if topic.get("view") == "opportunities":
            entry.update(view="opportunities", stage="outline", outline=opportunity_outline())
        catalog.append(entry)
    return catalog


def _write_opportunity_template(path, outline):
    template = Path(__file__).with_name("opportunity_report.html").read_text(encoding="utf-8")
    tables = []
    for group in outline["field_groups"]:
        rows = []
        for key, label in group["fields"]:
            value = "UNKNOWN" if key in ("status", "verification_status") else "확인 전" if key in ("is_verified", "is_self_reported") else "—"
            rows.append("<tr><th scope=\"row\">%s<small>%s</small></th><td>%s</td></tr>" % (html.escape(label), html.escape(key), value))
        tables.append("<h3>%s</h3><table><tbody>%s</tbody></table>" % (html.escape(group["name"]), "".join(rows)))
    template = template.replace("__FIELD_TABLES__", "".join(tables))
    template = template.replace("__SHARED_CSS__", Path(__file__).with_name("public_site.css").read_text(encoding="utf-8"))
    path.write_text(template, encoding="utf-8")


def _write_page(path, snapshot, history, prefix="", archived=False, selected_topic=""):
    template = Path(__file__).with_name("public_site.html").read_text(encoding="utf-8")
    data = dict(snapshot, history=history, prefix=prefix, archived=archived, selected_topic=selected_topic)
    if "topics" not in data:
        # Older saved JSON remains unchanged; infer its own original topic labels.
        known = {topic["name"]: topic for topic in load_topics()}
        labels = list(dict.fromkeys(item["topic"] for item in data["items"]))
        data["topics"] = [{"id": known[label]["id"] if label in known else "legacy-%d" % index,
                            "name": label, "description": "", "count": sum(item["topic"] == label for item in data["items"])}
                           for index, label in enumerate(labels)]
    serialized = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    content = template.replace("__BRIEFING_DATA__", serialized)
    assets = b"".join(Path(__file__).with_name("public_site." + suffix).read_bytes() for suffix in ("css", "js"))
    content = content.replace("__ASSET_PREFIX__", prefix).replace("__ASSET_VERSION__", hashlib.sha256(assets).hexdigest()[:12])
    topic = next((topic for topic in data["topics"] if topic["id"] == selected_topic), None)
    title = topic["name"] + " 리서치" if topic else "리서치 아카이브"
    description = topic.get("description") if topic else "여러 분야의 자료와 원문을 모으고, 주제별 리서치와 지난 브리핑을 찾아봅니다."
    content = content.replace("__PAGE_TITLE__", html.escape(title)).replace("__PAGE_DESCRIPTION__", html.escape(description or "", quote=True))
    # A static preview remains readable if JavaScript is unavailable.
    preview = "".join('<li><a href="%s">%s</a></li>' % (html.escape(item["url"], quote=True), html.escape(item["title"])) for item in snapshot["items"][:10])
    content = content.replace("__NOSCRIPT_ITEMS__", preview)
    path.write_text(content, encoding="utf-8")
