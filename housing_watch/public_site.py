"""Public-source collection and a persistent, searchable static briefing archive."""

import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from .ai_brief import render_ai_news_html
from .ai_news import AINewsFetchError, collect_ai_news
from .config import enabled_sources
from .db import all_items, record_snapshot, upsert_items
from .news import NewsFetchError, collect_weekly_news
from .render import render_brief_html
from .sources import fetch_source
from .timeutil import iso_utc, now_kst


def collect_public_data(conn, config):
    health = []
    for source in enabled_sources(config):
        try:
            result = fetch_source(source)
            stats = upsert_items(conn, result["items"], config.get("interest", {}))
            record_snapshot(conn, source["id"], result["raw_path"], len(result["items"]))
            conn.commit()
            health.append({"source": source["name"], "ok": True, "count": len(result["items"])})
            print("%s: fetched=%d inserted=%d updated=%d" % (source["id"], len(result["items"]), stats["inserted"], stats["updated"]))
        except (OSError, ValueError, RuntimeError) as exc:
            health.append({"source": source["name"], "ok": False, "message": str(exc)})
    for name, collector, options in [
        ("AI 개발 소식", collect_ai_news, {"limit": 120, "days": 7}),
        ("주간 뉴스", collect_weekly_news, {"source": "auto", "limit": 40}),
    ]:
        try:
            result = collector(conn, **options)
            health.append({"source": name, "ok": True, "count": result["fetched"], "warnings": result["failures"]})
            print("%s: fetched=%d warnings=%d" % (name, result["fetched"], len(result["failures"])))
        except (OSError, ValueError, RuntimeError, AINewsFetchError, NewsFetchError) as exc:
            health.append({"source": name, "ok": False, "message": str(exc)})
    return health


def public_library(conn):
    entries = []
    for row in conn.execute("SELECT * FROM news_items ORDER BY published_at DESC, id DESC"):
        item = dict(row)
        try:
            payload = json.loads(item.get("raw_payload") or "{}")
        except (ValueError, TypeError):
            payload = {}
        if not isinstance(payload, dict):
            payload = {}
        entries.append({
            "id": "news-%s" % item["id"],
            "topic": "AI 개발" if item["source_id"].startswith("ai_") else "주간 뉴스",
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
        entries.append({
            "id": "housing-%s" % item["id"], "topic": "청약·주거",
            "title": item["title"], "summary": (item.get("detail_summary") or item.get("summary") or "")[:400],
            "url": _public_url(item["url"]), "source": item.get("agency") or item["source_id"],
            "category": item.get("category") or "", "published_at": item.get("published_at") or "",
            "first_seen_at": item["first_seen_at"], "score": item.get("importance") or 0,
            "basis": "공식 공고", "status": item.get("status") or "",
        })
    return [entry for entry in entries if entry["url"]]


def _public_url(value):
    try:
        parsed = urlsplit(value or "")
        return value if parsed.scheme in ("https", "http") and parsed.netloc and not parsed.username and not parsed.password else ""
    except ValueError:
        return ""


def build_public_site(conn, output_path="site", health=None):
    output = Path(output_path)
    output.mkdir(parents=True, exist_ok=True)
    entries = public_library(conn)
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
    snapshot = {"date": date, "created_at": created_at, "items": entries, "health": health or []}
    daily = archive / date
    if not (daily / "briefing.json").exists():
        daily.mkdir(exist_ok=True)
        _write_json(daily / "briefing.json", snapshot)
        history = [entry for entry in history if entry["date"] != date]
        history.append({"date": date, "created_at": created_at, "count": len(entries)})
    history.sort(key=lambda entry: entry["date"], reverse=True)
    _write_json(archive_index, history)
    _write_json(output / "library.json", entries)
    _write_json(output / "status.json", {"generated_at": created_at, "count": len(entries), "health": health or []})
    _write_page(output / "index.html", snapshot, history)
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
    return {"path": str(output / "index.html"), "items": len(entries), "archives": len(history), "health": health or []}


def _write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_page(path, snapshot, history, prefix="", archived=False):
    template = Path(__file__).with_name("public_site.html").read_text(encoding="utf-8")
    data = dict(snapshot, history=history, prefix=prefix, archived=archived)
    serialized = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    content = template.replace("__BRIEFING_DATA__", serialized)
    # A static preview remains readable if JavaScript is unavailable.
    preview = "".join('<li><a href="%s">%s</a></li>' % (html.escape(item["url"], quote=True), html.escape(item["title"])) for item in snapshot["items"][:10])
    content = content.replace("__NOSCRIPT_ITEMS__", preview)
    path.write_text(content, encoding="utf-8")
