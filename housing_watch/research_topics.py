"""Configurable research domains and public RSS/Atom collection."""

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

from .ai_news import AINewsFetchError, _read_url, _write_raw, parse_ai_feed
from .db import record_snapshot, upsert_news_items


DEFAULT_TOPICS = Path(__file__).resolve().parent.parent / "config/research_topics.json"
OPPORTUNITY_OUTLINE = DEFAULT_TOPICS.with_name("opportunity_outline.json")
SLUG = re.compile(r"[a-z][a-z0-9-]{0,47}")


def public_url(value):
    try:
        parsed = urlsplit(value or "")
        return value if parsed.scheme in ("https", "http") and parsed.netloc and not parsed.username and not parsed.password else ""
    except (ValueError, TypeError):
        return ""


def load_topics(path=None):
    data = json.loads(Path(path or DEFAULT_TOPICS).read_text(encoding="utf-8"))
    topics = data.get("topics") if isinstance(data, dict) else None
    if not isinstance(topics, list) or not topics:
        raise ValueError("Research topics must be a non-empty list.")
    ids, names, builtins = set(), set(), set()
    for topic in topics:
        if not isinstance(topic, dict) or not SLUG.fullmatch(str(topic.get("id", ""))):
            raise ValueError("Research topic IDs must be safe lowercase slugs.")
        name = topic.get("name")
        collector = topic.get("collector")
        if not isinstance(name, str) or not name.strip() or topic["id"] in ids or name in names:
            raise ValueError("Research topic IDs and names must be unique and non-empty.")
        if collector not in ("ai", "housing", "news", "rss", "planned"):
            raise ValueError("Unknown research collector: %s" % collector)
        if not isinstance(topic.get("description", ""), str):
            raise ValueError("Research descriptions must be text.")
        if collector == "news" and topic.get("source", "auto") not in ("auto", "gdelt", "google-news"):
            raise ValueError("Unsupported news source.")
        if collector not in ("rss", "planned") and collector in builtins:
            raise ValueError("Each built-in collector may belong to only one topic.")
        ids.add(topic["id"])
        names.add(name)
        builtins.add(collector)
        if topic.get("view") not in (None, "opportunities") or (topic.get("view") == "opportunities" and collector != "planned"):
            raise ValueError("The opportunity outline view requires a planned collector.")
        if topic.get("detail_page") not in (None, "ai-news.html", "brief.html"):
            raise ValueError("Unsupported detail page.")
        if not isinstance(topic.get("limit", 40), int) or not 1 <= topic.get("limit", 40) <= 500:
            raise ValueError("Research collection limit must be between 1 and 500.")
        if not isinstance(topic.get("days", 7), int) or not 0 <= topic.get("days", 7) <= 365:
            raise ValueError("Research collection days must be between 0 and 365.")
        if collector == "rss":
            feeds = topic.get("feeds")
            if not isinstance(feeds, list) or not feeds:
                raise ValueError("An RSS research topic requires public feeds.")
            feed_ids = set()
            for feed in feeds:
                if not isinstance(feed, dict) or not SLUG.fullmatch(str(feed.get("id", ""))) or feed["id"] in feed_ids or not public_url(feed.get("url")):
                    raise ValueError("RSS feeds require unique safe IDs and public HTTP(S) URLs.")
                feed_ids.add(feed["id"])
    return topics


def opportunity_outline():
    """UI requirements only; these are never exported as collected opportunities."""
    return json.loads(OPPORTUNITY_OUTLINE.read_text(encoding="utf-8"))


def topic_for_item(topics, source_id, housing=False):
    collector = "housing" if housing else "ai" if source_id.startswith("ai_") else "news"
    if source_id.startswith("research_"):
        return next((topic for topic in topics if topic["collector"] == "rss" and source_id.startswith("research_" + topic["id"] + "_")), None)
    return next((topic for topic in topics if topic["collector"] == collector), None)


def collect_topic_feeds(conn, topic, raw_dir=None):
    """Use the existing XML parser, replacing all AI-specific interpretation fields."""
    raw_dir = raw_dir or "data/raw/research/" + topic["id"]
    source_ids = ["research_%s_%s" % (topic["id"], feed["id"]) for feed in topic["feeds"]]
    items, failures = [], []
    for feed, source_id in zip(topic["feeds"], source_ids):
        try:
            body = _read_url(feed["url"])
            raw_path = _write_raw(raw_dir, source_id, body, ".xml")
            source = {"id": source_id, "name": feed.get("name") or feed["id"], "feed_url": feed["url"],
                      "home_url": feed.get("home_url", ""), "category_hint": topic["name"]}
            parsed = parse_ai_feed(body, source, limit=topic.get("limit", 40))
            if not parsed:
                raise ValueError("Feed contains no readable RSS/Atom entries.")
            for item in parsed:
                original = json.loads(item["raw_payload"])
                # Keep source excerpts, not generated AI advice or implicit verification.
                excerpt = original["detail"]
                if excerpt.startswith("원문 요약이 짧습니다."):
                    excerpt = ""
                payload = {"detail": excerpt, "topic_id": topic["id"], "feed_url": feed["url"]}
                item["summary_ko"] = excerpt
                item["raw_payload"] = json.dumps(payload, ensure_ascii=False, sort_keys=True)
                item["content_hash"] = hashlib.sha256(item["raw_payload"].encode("utf-8")).hexdigest()
            items.extend(parsed)
            record_snapshot(conn, source_id, raw_path, len(parsed))
        except (AINewsFetchError, OSError, ValueError, ET.ParseError) as exc:
            failures.append("%s: %s" % (feed["id"], exc))
    if not items:
        raise ValueError("No research feed returned items: " + "; ".join(failures))
    stats = upsert_news_items(conn, items, source_ids=source_ids)
    conn.commit()
    return dict(stats, fetched=len(items), failures=failures)
