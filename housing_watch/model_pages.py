"""Accumulate complete, hash-verified Theo model documents and dependencies."""

import hashlib
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse

from .model_research import CONFIG_PATH, _read_catalog, parse_model_catalog
from .timeutil import iso_utc


class Dependencies(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("src"):
            self.paths.add(attrs["src"])
        if tag == "link" and "stylesheet" in attrs.get("rel", "").split():
            self.paths.add(attrs.get("href", ""))


def _fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "SignalDesk/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.geturl() != url:
            raise ValueError("Unexpected model document redirect")
        body = response.read(2 * 1024 * 1024 + 1)
    if len(body) > 2 * 1024 * 1024:
        raise ValueError("Model document is too large")
    return body


def _raw(raw_dir, body, suffix):
    digest = hashlib.sha256(body).hexdigest()
    path = Path(raw_dir) / (digest + suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_bytes(body)
    return str(path)


def load_page(entry, config, raw_dir, fetch=_fetch):
    filename = entry.get("file", "")
    if not isinstance(filename, str) or not filename.endswith(".html") or any(c in filename for c in "/\\") or filename in (".", ".."):
        raise ValueError("Invalid model document filename")
    source_url = config["site_url"] + "materials/" + quote(filename)
    body = fetch(source_url)
    _raw(raw_dir, body, ".html")
    if hashlib.sha256(body).hexdigest() != entry["sha256"]:
        raise ValueError("Catalog/content hash mismatch: " + entry["slug"])
    source_html = body.decode("utf-8")
    if not re.search(r"<body\b", source_html, re.I) or not re.search(r"</html>", source_html, re.I):
        raise ValueError("Incomplete model HTML document")
    parser = Dependencies()
    parser.feed(source_html)
    assets = {}
    for path in sorted(parser.paths):
        # Original documents currently use three same-directory assets. Never
        # turn a new script URL into an unchecked remote-code dependency.
        if not re.fullmatch(r"[A-Za-z0-9_-]+\.(?:js|css)", path):
            raise ValueError("Unsupported model page dependency: " + path)
        asset = fetch(urljoin(source_url, path))
        _raw(raw_dir, asset, Path(path).suffix)
        assets[path] = asset.decode("utf-8")
    return {"slug": entry["slug"], "file": filename, "title": entry["title"],
            "description": entry["description"], "category": entry["category"],
            "tags": entry.get("tags", []), "updated_on": entry.get("updatedAt") or "",
            "reference_date": entry.get("referenceDate") or "", "source_url": source_url,
            "source_sha256": entry["sha256"], "source_kind": "theo-authored",
            "html": source_html, "assets": assets}


def ensure_tables(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS model_pages (
        slug TEXT PRIMARY KEY, document TEXT NOT NULL, content_hash TEXT NOT NULL,
        revision INTEGER NOT NULL, first_seen_at TEXT NOT NULL, last_seen_at TEXT NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS model_page_revisions (
        slug TEXT NOT NULL, revision INTEGER NOT NULL, document TEXT NOT NULL,
        content_hash TEXT NOT NULL, saved_at TEXT NOT NULL, PRIMARY KEY(slug,revision))""")
    conn.execute("""CREATE TABLE IF NOT EXISTS model_page_runs (
        id INTEGER PRIMARY KEY, collected_at TEXT NOT NULL, result TEXT NOT NULL)""")


def upsert_pages(conn, documents):
    # Validate the complete batch before touching stored pages. Slug identifies a
    # document, and shared asset changes are part of the immutable edition hash.
    slugs = [doc["slug"] for doc in documents]
    if len(slugs) != len(set(slugs)) or any(not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", slug) for slug in slugs):
        raise ValueError("Invalid or duplicate model page slug")
    prepared = []
    for doc in documents:
        if not doc.get("title") or not doc.get("html") or urlparse(doc["source_url"]).scheme != "https":
            raise ValueError("Incomplete model page")
        text = json.dumps(doc, ensure_ascii=False, sort_keys=True, allow_nan=False)
        prepared.append((doc["slug"], text, hashlib.sha256(text.encode()).hexdigest()))
    stats = dict(inserted=0, updated=0, unchanged=0)
    with conn:
        ensure_tables(conn)
        now = iso_utc()
        for slug, text, digest in prepared:
            old = conn.execute("SELECT * FROM model_pages WHERE slug=?", (slug,)).fetchone()
            if old and old["content_hash"] == digest:
                conn.execute("UPDATE model_pages SET last_seen_at=? WHERE slug=?", (now, slug))
                stats["unchanged"] += 1
                continue
            revision = old["revision"] + 1 if old else 1
            conn.execute("INSERT OR REPLACE INTO model_pages VALUES (?,?,?,?,?,?)",
                         (slug, text, digest, revision, old["first_seen_at"] if old else now, now))
            conn.execute("INSERT INTO model_page_revisions VALUES (?,?,?,?,?)", (slug, revision, text, digest, now))
            stats["updated" if old else "inserted"] += 1
    return stats


def collect_model_pages(conn, raw_dir="data/raw/ai_news/model_pages"):
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    catalog_body = _read_catalog(config["catalog_url"])
    _raw(raw_dir, catalog_body, ".json")
    catalog = json.loads(catalog_body)
    matched = {item["external_id"] for item in parse_model_catalog(catalog, config)}
    entries = [entry for entry in catalog["documents"] if entry["slug"] in matched]
    documents, failures = [], []
    def fetch_entry(entry):
        try:
            return load_page(entry, config, raw_dir), None
        except (OSError, ValueError) as exc:
            return None, entry["slug"] + ": " + str(exc)
    with ThreadPoolExecutor(max_workers=6) as pool:
        for document, failure in pool.map(fetch_entry, entries):
            if failure:
                failures.append(failure)
            else:
                documents.append(document)
    stats = dict(upsert_pages(conn, documents), fetched=len(entries), failures=failures)
    with conn:
        ensure_tables(conn)
        conn.execute("INSERT INTO model_page_runs(collected_at,result) VALUES (?,?)", (iso_utc(), json.dumps(stats, ensure_ascii=False)))
    if not documents:
        raise ValueError("No complete model pages fetched: " + "; ".join(failures))
    return stats


def export_model_pages(conn):
    ensure_tables(conn)
    conn.commit()
    def record(row):
        return {"slug": row["slug"], "revision": row["revision"], "document": json.loads(row["document"])}
    return {"pages": [record(row) for row in conn.execute("SELECT * FROM model_pages ORDER BY slug")],
            "history": [record(row) for row in conn.execute("SELECT * FROM model_page_revisions ORDER BY slug,revision")],
            "runs": [{"collected_at": row["collected_at"], **json.loads(row["result"])}
                     for row in conn.execute("SELECT * FROM model_page_runs ORDER BY id DESC LIMIT 10")]}
