import sqlite3
from pathlib import Path

from .timeutil import iso_utc


SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    external_id TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    agency TEXT,
    category TEXT,
    region TEXT,
    status TEXT,
    published_at TEXT,
    deadline_at TEXT,
    summary TEXT,
    raw_text TEXT,
    content_hash TEXT,
    state TEXT DEFAULT 'new',
    importance INTEGER DEFAULT 0,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    UNIQUE(source_id, external_id)
);

CREATE TABLE IF NOT EXISTS raw_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    raw_path TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    item_count INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_items_source ON items(source_id);
CREATE INDEX IF NOT EXISTS idx_items_status ON items(status);
CREATE INDEX IF NOT EXISTS idx_items_deadline ON items(deadline_at);
CREATE INDEX IF NOT EXISTS idx_items_region ON items(region);
"""

DETAIL_COLUMNS = {
    "address": "TEXT",
    "area_range_m2": "TEXT",
    "area_range_pyeong": "TEXT",
    "supply_units": "TEXT",
    "deposit": "TEXT",
    "monthly_rent": "TEXT",
    "price": "TEXT",
    "eligibility": "TEXT",
    "application_period": "TEXT",
    "move_in_month": "TEXT",
    "detail_summary": "TEXT",
    "detail_text": "TEXT",
    "detail_collected_at": "TEXT",
}


def connect(path):
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    conn.executescript(SCHEMA)
    ensure_detail_columns(conn)
    ensure_fts(conn)
    conn.commit()


def ensure_detail_columns(conn):
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(items)").fetchall()}
    for name, column_type in DETAIL_COLUMNS.items():
        if name not in existing:
            conn.execute("ALTER TABLE items ADD COLUMN %s %s" % (name, column_type))


def ensure_fts(conn):
    try:
        conn.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(
                title,
                summary,
                raw_text,
                region,
                category,
                agency,
                source_id
            )
            """
        )
        return True
    except sqlite3.OperationalError:
        return False


def has_fts(conn):
    try:
        conn.execute("SELECT rowid FROM items_fts LIMIT 1")
        return True
    except sqlite3.OperationalError:
        return False


def record_snapshot(conn, source_id, raw_path, item_count):
    conn.execute(
        "INSERT INTO raw_snapshots(source_id, raw_path, fetched_at, item_count) VALUES (?, ?, ?, ?)",
        (source_id, raw_path, iso_utc(), item_count),
    )


def calculate_importance(item, interest):
    score = 0
    text = " ".join(
        [
            item.get("title", ""),
            item.get("summary", ""),
            item.get("region", ""),
            item.get("category", ""),
            item.get("status", ""),
        ]
    )
    for keyword in interest.get("keywords", []):
        if keyword and keyword in text:
            score += 2
    region = item.get("region") or ""
    for preferred_region in interest.get("regions", []):
        if preferred_region and (preferred_region in region or region in preferred_region):
            score += 2
            break
    if item.get("status") in interest.get("preferred_statuses", []):
        score += 3
    return min(score, 10)


def upsert_items(conn, items, interest):
    inserted = 0
    updated = 0
    for item in items:
        importance = calculate_importance(item, interest)
        now = item.get("collected_at") or iso_utc()
        existing = conn.execute(
            "SELECT id, content_hash FROM items WHERE source_id = ? AND external_id = ?",
            (item["source_id"], item["external_id"]),
        ).fetchone()

        values = (
            item["source_id"],
            item["external_id"],
            item["title"],
            item["url"],
            item.get("agency", ""),
            item.get("category", ""),
            item.get("region", ""),
            item.get("status", ""),
            item.get("published_at", ""),
            item.get("deadline_at", ""),
            item.get("summary", ""),
            item.get("raw_text", ""),
            item.get("content_hash", ""),
            item.get("address", ""),
            item.get("area_range_m2", ""),
            item.get("area_range_pyeong", ""),
            item.get("supply_units", ""),
            item.get("deposit", ""),
            item.get("monthly_rent", ""),
            item.get("price", ""),
            item.get("eligibility", ""),
            item.get("application_period", ""),
            item.get("move_in_month", ""),
            item.get("detail_summary", ""),
            item.get("detail_text", ""),
            item.get("detail_collected_at", ""),
            importance,
            now,
        )

        if existing:
            conn.execute(
                """
                UPDATE items
                SET title = ?, url = ?, agency = ?, category = ?, region = ?, status = ?,
                    published_at = ?, deadline_at = ?, summary = ?, raw_text = ?,
                    content_hash = ?, address = ?, area_range_m2 = ?, area_range_pyeong = ?,
                    supply_units = ?, deposit = ?, monthly_rent = ?, price = ?, eligibility = ?,
                    application_period = ?, move_in_month = ?, detail_summary = ?, detail_text = ?,
                    detail_collected_at = ?, importance = ?, last_seen_at = ?
                WHERE id = ?
                """,
                values[2:] + (existing["id"],),
            )
            updated += 1
            row_id = existing["id"]
        else:
            cursor = conn.execute(
                """
                INSERT INTO items(
                    source_id, external_id, title, url, agency, category, region, status,
                    published_at, deadline_at, summary, raw_text, content_hash,
                    address, area_range_m2, area_range_pyeong, supply_units, deposit,
                    monthly_rent, price, eligibility, application_period, move_in_month,
                    detail_summary, detail_text, detail_collected_at,
                    importance, first_seen_at, last_seen_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                values + (now,),
            )
            inserted += 1
            row_id = cursor.lastrowid

        sync_fts(conn, row_id)
    conn.commit()
    return {"inserted": inserted, "updated": updated}


def prune_items_outside_regions(conn, regions):
    if not regions:
        return 0
    items = conn.execute("SELECT id, region FROM items").fetchall()
    keep_ids = []
    for item in items:
        if region_in_scope(item["region"], regions):
            keep_ids.append(item["id"])
    if len(keep_ids) == len(items):
        return 0
    placeholders = ",".join("?" for _ in keep_ids) if keep_ids else "NULL"
    deleted = conn.execute(
        "DELETE FROM items WHERE id NOT IN (%s)" % placeholders,
        tuple(keep_ids),
    ).rowcount
    if has_fts(conn):
        try:
            conn.execute("DELETE FROM items_fts")
            for row in conn.execute("SELECT id FROM items").fetchall():
                sync_fts(conn, row["id"])
        except sqlite3.OperationalError:
            pass
    conn.commit()
    return deleted


def prune_items_outside_sources(conn, source_ids):
    if not source_ids:
        return 0
    placeholders = ",".join("?" for _ in source_ids)
    deleted = conn.execute(
        "DELETE FROM items WHERE source_id NOT IN (%s)" % placeholders,
        tuple(source_ids),
    ).rowcount
    if has_fts(conn):
        try:
            conn.execute("DELETE FROM items_fts")
            for row in conn.execute("SELECT id FROM items").fetchall():
                sync_fts(conn, row["id"])
        except sqlite3.OperationalError:
            pass
    conn.commit()
    return deleted


def region_in_scope(region, regions):
    value = region or ""
    for wanted in regions:
        if wanted and (wanted in value or value in wanted):
            return True
    return False


def sync_fts(conn, row_id):
    if not has_fts(conn):
        return
    row = conn.execute("SELECT * FROM items WHERE id = ?", (row_id,)).fetchone()
    if not row:
        return
    try:
        conn.execute("DELETE FROM items_fts WHERE rowid = ?", (row_id,))
        conn.execute(
            """
            INSERT INTO items_fts(rowid, title, summary, raw_text, region, category, agency, source_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row_id,
                row["title"],
                row["summary"],
                _fts_text(row),
                row["region"],
                row["category"],
                row["agency"],
                row["source_id"],
            ),
        )
    except sqlite3.OperationalError:
        pass


def _fts_text(row):
    return " ".join(
        [
            row["raw_text"] or "",
            row["address"] or "",
            row["area_range_m2"] or "",
            row["area_range_pyeong"] or "",
            row["supply_units"] or "",
            row["deposit"] or "",
            row["monthly_rent"] or "",
            row["price"] or "",
            row["eligibility"] or "",
            row["application_period"] or "",
            row["detail_summary"] or "",
            row["detail_text"] or "",
        ]
    )


def all_items(conn):
    rows = conn.execute(
        """
        SELECT *
        FROM items
        ORDER BY
            CASE
              WHEN status IN ('모집중', '접수중', '공고중', '정정공고중') THEN 0
              ELSE 1
            END,
            COALESCE(deadline_at, '') ASC,
            COALESCE(published_at, '') DESC,
            id DESC
        """
    ).fetchall()
    return [dict(row) for row in rows]


def latest_snapshots(conn, limit=10):
    rows = conn.execute(
        "SELECT * FROM raw_snapshots ORDER BY fetched_at DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(row) for row in rows]
