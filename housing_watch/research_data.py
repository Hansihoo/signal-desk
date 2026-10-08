"""Research content contract, SQLite revisions, and presentation-free JSON export."""

import hashlib
import json
import math
import re
from datetime import date
from pathlib import Path

from .research_topics import public_url
from .timeutil import iso_utc


SCHEMA_VERSION = 1
FEATURED_REPORT_ID = "github-pages-storage"
EXAMPLE_PATH = Path(__file__).resolve().parent.parent / "config/research_reports.example.json"
PUBLICATION_PATH = EXAMPLE_PATH.with_name("research_publication.json")
REPORT_FIELDS = {"id", "topic_id", "topic_path", "title", "description", "checked_on",
                 "scope", "deck", "highlights", "source_note", "summary", "metrics",
                 "datasets", "result", "references", "caveats"}


def storage_scenarios(topics=10, weeks=52, years=10):
    """Decimal KB/MB, one stored copy per report; comparison assumptions only."""
    reports = topics * weeks * years
    return [(label, size_kb, reports * size_kb / 1000) for label, size_kb in (
        ("50 KB / 건", 50), ("100 KB / 건", 100), ("1 MB / 건", 1000))]


def _object(value, fields, required=None):
    if not isinstance(value, dict) or set(value) - fields or (required or fields) - set(value):
        raise ValueError("Invalid object fields; expected %s" % ", ".join(sorted(required or fields)))


def _text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected nonempty plain text")


def _id(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", value):
        raise ValueError("IDs must be stable lowercase letters, numbers, or hyphens")


def _list(value):
    if not isinstance(value, list):
        raise ValueError("Expected a list")
    return value


def _number(value):
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise ValueError("Expected a finite nonnegative number")


def validate_report(report):
    """Validate content before any database mutation; no layout or arbitrary extra fields."""
    _object(report, REPORT_FIELDS | {"tables", "learning", "explanation"}, REPORT_FIELDS)
    for key in ("id", "topic_id"):
        _id(report[key])
    for key in ("title", "description", "checked_on", "scope", "deck", "source_note"):
        _text(report[key])
    checked = date.fromisoformat(report["checked_on"])
    if checked.isoformat() != report["checked_on"]:
        raise ValueError("checked_on must be YYYY-MM-DD")
    for key in ("topic_path", "highlights"):
        if not _list(report[key]):
            raise ValueError("%s cannot be empty" % key)
        for text in report[key]:
            _text(text)
    sources = set()
    for source in _list(report["references"]):
        _object(source, {"id", "title", "url", "description"})
        _id(source["id"])
        if source["id"] in sources:
            raise ValueError("Duplicate source ID")
        sources.add(source["id"])
        for key in ("title", "description", "url"):
            _text(source[key])
        if public_url(source["url"]) != source["url"]:
            raise ValueError("Source URL must be an HTTP(S) URL without credentials")

    def citations(record):
        for source_id in _list(record["source_ids"]):
            _id(source_id)
            if source_id not in sources:
                raise ValueError("Unknown source ID: %s" % source_id)

    def points(records):
        for point in _list(records):
            _object(point, {"kind", "label", "text", "source_ids"})
            if point["kind"] not in ("fact", "estimate", "judgment"):
                raise ValueError("kind must be fact, estimate, or judgment")
            _text(point["label"])
            _text(point["text"])
            citations(point)
            if point["kind"] == "fact" and not point["source_ids"]:
                raise ValueError("A factual summary needs a source")

    points(report["summary"])
    _object(report["result"], {"title", "points"})
    _text(report["result"]["title"])
    points(report["result"]["points"])
    for metric in _list(report["metrics"]):
        _object(metric, {"label", "value", "unit", "qualifier", "source_ids"})
        _number(metric["value"])
        _text(metric["label"])
        _text(metric["unit"])
        if not isinstance(metric["qualifier"], str):
            raise ValueError("qualifier must be text")
        citations(metric)
        if not metric["source_ids"]:
            raise ValueError("A factual metric needs a source")
    dataset_ids = set()
    for dataset in _list(report["datasets"]):
        fields = {"id", "title", "kind", "unit", "rows", "threshold", "assumptions", "note", "method", "source_ids"}
        _object(dataset, fields, fields - {"threshold"})
        _id(dataset["id"])
        if dataset["id"] in dataset_ids:
            raise ValueError("Duplicate dataset ID")
        dataset_ids.add(dataset["id"])
        for key in ("title", "unit", "note"):
            _text(dataset[key])
        if dataset["kind"] not in ("fact", "estimate"):
            raise ValueError("Dataset kind must be fact or estimate")
        for key in ("assumptions", "method"):
            for text in _list(dataset[key]):
                _text(text)
        if dataset["kind"] == "estimate" and not dataset["assumptions"]:
            raise ValueError("An estimate needs assumptions")
        citations(dataset)
        rows = _list(dataset["rows"])
        if not rows:
            raise ValueError("Dataset rows cannot be empty")
        for row in rows + ([dataset["threshold"]] if "threshold" in dataset else []):
            _object(row, {"label", "value", "source_ids"})
            _text(row["label"])
            _number(row["value"])
            citations(row)
            if dataset["kind"] == "fact" and not (row["source_ids"] or dataset["source_ids"]):
                raise ValueError("Factual data needs a source")
    table_ids = set()
    for table in _list(report.get("tables", [])):
        _object(table, {"id", "title", "columns", "rows", "note"})
        _id(table["id"])
        if table["id"] in table_ids:
            raise ValueError("Duplicate table ID")
        table_ids.add(table["id"])
        _text(table["title"])
        _text(table["note"])
        columns = _list(table["columns"])
        if len(columns) < 2:
            raise ValueError("A comparison table needs at least two columns")
        for column in columns:
            _text(column)
        if not _list(table["rows"]):
            raise ValueError("Table rows cannot be empty")
        for row in table["rows"]:
            _object(row, {"values", "source_ids"})
            if len(_list(row["values"])) != len(columns):
                raise ValueError("Table row must match its columns")
            for value in row["values"]:
                _text(value)
            citations(row)
            if not row["source_ids"]:
                raise ValueError("A factual table row needs a source")
    lesson_ids = set()
    # Essential explanation shares the authored block contract with optional
    # learning, but is rendered in the primary reading path. Prefixes keep
    # chapter anchors unique between the two independent content collections.
    chapters = [(field, lesson) for field in ("explanation", "learning")
                for lesson in _list(report.get(field, []))]
    for field, lesson in chapters:
        _object(lesson, {"id", "title", "lead", "blocks"})
        _id(lesson["id"])
        if (field, lesson["id"]) in lesson_ids:
            raise ValueError("Duplicate learning ID")
        lesson_ids.add((field, lesson["id"]))
        _text(lesson["title"])
        _text(lesson["lead"])
        if not _list(lesson["blocks"]):
            raise ValueError("Learning blocks cannot be empty")
        for block in lesson["blocks"]:
            if not isinstance(block, dict) or block.get("type") not in ("paragraph", "steps", "terms", "code"):
                raise ValueError("Unsupported learning block type")
            content = "text" if block["type"] in ("paragraph", "code") else "items"
            _object(block, {"type", "kind", "title", content, "source_ids"})
            if block["kind"] not in ("fact", "example", "judgment"):
                raise ValueError("Learning kind must be fact, example, or judgment")
            _text(block["title"])
            if content == "text":
                _text(block["text"])
            else:
                if not _list(block["items"]):
                    raise ValueError("Learning items cannot be empty")
                for item in block["items"]:
                    _object(item, {"label", "text"})
                    _text(item["label"])
                    _text(item["text"])
            citations(block)
            if block["kind"] == "fact" and not block["source_ids"]:
                raise ValueError("Factual learning needs a source")
    for caveat in _list(report["caveats"]):
        _object(caveat, {"text", "source_ids"})
        _text(caveat["text"])
        citations(caveat)
    return report


def load_report_input(path=EXAMPLE_PATH):
    document = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(document, dict) or type(document.get("schema_version")) is not int or document["schema_version"] != SCHEMA_VERSION:
        raise ValueError("Unsupported research schema_version")
    reports = _list(document.get("reports"))
    ids = set()
    for report in reports:
        validate_report(report)
        if report["id"] in ids:
            raise ValueError("Duplicate report ID in import")
        ids.add(report["id"])
    return reports


def _ensure_tables(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS research_reports (
        id TEXT PRIMARY KEY, revision INTEGER NOT NULL, content_hash TEXT NOT NULL,
        document TEXT NOT NULL, updated_at TEXT NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS research_report_revisions (
        report_id TEXT NOT NULL, revision INTEGER NOT NULL, content_hash TEXT NOT NULL,
        document TEXT NOT NULL, saved_at TEXT NOT NULL, PRIMARY KEY(report_id, revision))""")


def import_reports(conn, reports, only_missing=False):
    ids = set()
    for report in reports:
        validate_report(report)
        if report["id"] in ids:
            raise ValueError("Duplicate report ID in import")
        ids.add(report["id"])
    with conn:
        _ensure_tables(conn)
        return _upsert_reports(conn, reports, only_missing)


def _upsert_reports(conn, reports, only_missing=False):
    """Validated input; caller owns the transaction, including any batch receipt."""
    stats = {"inserted": 0, "updated": 0, "unchanged": 0}
    for report in reports:
        document = json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False)
        digest = hashlib.sha256(document.encode("utf-8")).hexdigest()
        old = conn.execute("SELECT revision, content_hash FROM research_reports WHERE id=?", (report["id"],)).fetchone()
        if old and (only_missing or old["content_hash"] == digest):
            stats["unchanged"] += 1
            continue
        revision = old["revision"] + 1 if old else 1
        now = iso_utc()
        conn.execute("INSERT INTO research_report_revisions VALUES (?, ?, ?, ?, ?)",
                     (report["id"], revision, digest, document, now))
        conn.execute("INSERT OR REPLACE INTO research_reports VALUES (?, ?, ?, ?, ?)",
                     (report["id"], revision, digest, document, now))
        stats["updated" if old else "inserted"] += 1
    return stats


def load_publication(path=None):
    path = Path(path or PUBLICATION_PATH)
    document = json.loads(path.read_text(encoding="utf-8-sig"))
    _object(document, {"schema_version", "featured_report_id", "report_ids", "batches"})
    if type(document["schema_version"]) is not int or document["schema_version"] != SCHEMA_VERSION:
        raise ValueError("Unsupported publication schema")
    for key in ("featured_report_id",):
        _id(document[key])
    ids = _list(document["report_ids"])
    for report_id in ids:
        _id(report_id)
    if len(set(ids)) != len(ids) or document["featured_report_id"] not in ids:
        raise ValueError("Publication needs unique IDs and a listed featured report")
    batch_ids = set()
    batches = []
    for batch in _list(document["batches"]):
        _object(batch, {"id", "input"})
        _id(batch["id"])
        _text(batch["input"])
        if batch["id"] in batch_ids or Path(batch["input"]).name != batch["input"] or not batch["input"].endswith(".json"):
            raise ValueError("Use unique batch IDs and JSON filenames in the configuration directory")
        batch_ids.add(batch["id"])
        batches.append((batch["id"], load_report_input(path.parent / batch["input"])))
    return document, batches


def apply_publication(conn, publication, batches):
    """Apply each immutable reviewed batch once; later SQLite edits stay intact."""
    with conn:
        _ensure_tables(conn)
        conn.execute("""CREATE TABLE IF NOT EXISTS research_import_batches (
            id TEXT PRIMARY KEY, content_hash TEXT NOT NULL, applied_at TEXT NOT NULL)""")
        for batch_id, reports in batches:
            digest = hashlib.sha256(json.dumps(reports, ensure_ascii=False, sort_keys=True,
                                              allow_nan=False).encode("utf-8")).hexdigest()
            old = conn.execute("SELECT content_hash FROM research_import_batches WHERE id=?", (batch_id,)).fetchone()
            if old:
                if old["content_hash"] != digest:
                    raise ValueError("A reviewed batch changed; add a new batch ID instead: " + batch_id)
                continue
            _upsert_reports(conn, reports)
            conn.execute("INSERT INTO research_import_batches VALUES (?, ?, ?)", (batch_id, digest, iso_utc()))
        stored = {row["id"] for row in conn.execute("SELECT id FROM research_reports")}
        if set(publication["report_ids"]) - stored:
            raise ValueError("Publication references a missing report")


def ensure_example_report(conn):
    """Bootstrap the authored example once; publishing never replaces an edited report."""
    return import_reports(conn, load_report_input(), only_missing=True)


def build_research_data(conn, records, topics, health=None):
    ensure_example_report(conn)
    publication, batches = load_publication()
    apply_publication(conn, publication, batches)
    reports, versions = [], []
    for row in conn.execute("SELECT * FROM research_reports ORDER BY id"):
        reports.append(validate_report(json.loads(row["document"])))
        versions.append({"id": row["id"], "revision": row["revision"], "updated_at": row["updated_at"]})
    catalog = [{key: topic[key] for key in ("id", "name", "description") if key in topic} for topic in topics]
    for report in reports:
        if not any(topic["id"] == report["topic_id"] for topic in catalog):
            catalog.append({"id": report["topic_id"], "name": report["topic_path"][-1], "description": ""})
    history = [{"id": row["report_id"], "revision": row["revision"], "saved_at": row["saved_at"],
                "document": validate_report(json.loads(row["document"]))}
               for row in conn.execute("SELECT * FROM research_report_revisions ORDER BY report_id, revision")]
    return {"schema_version": SCHEMA_VERSION, "generated_at": iso_utc(),
            "featured_report_id": publication["featured_report_id"],
            "publication_report_ids": publication["report_ids"], "topics": catalog,
            "source_records": records, "reports": reports, "report_versions": versions,
            "report_history": history, "health": health or []}


def write_research_data(path, document):
    """Write only JSON. No renderer, daily HTML archive, CSS, or PNG is invoked."""
    output = Path(path)
    if output.suffix.lower() != ".json":
        raise ValueError("Research data output must be a .json file")
    serialized = json.dumps(document, ensure_ascii=False, indent=2, allow_nan=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(serialized + "\n", encoding="utf-8")
    return output
