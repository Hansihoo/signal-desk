"""Local business working records. Never connected to the public DB or exporter."""

import hashlib
import html
import json
import re
import sqlite3
from datetime import date
from pathlib import Path

from .timeutil import iso_utc


DEFAULT_ROOT = Path("D:/3_codex_docs/SignalDesk/BusinessPlanning")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIELDS = {"id", "category", "title", "public_report_id", "status", "owner", "due_on",
          "customer", "pricing", "proposal", "technical_evidence", "next_action",
          "source_url", "checked_on"}
REQUIRED = {"id", "category", "title", "status", "checked_on", "next_action"}
CATEGORIES = ("국책사업", "영업 기회", "경쟁사·시장")
STATUSES = ("확인 필요", "검토 중", "보류", "진행", "종료")


def private_root(value=DEFAULT_ROOT):
    root = Path(value).resolve()
    if root == PROJECT_ROOT or PROJECT_ROOT in root.parents:
        raise ValueError("Private business storage must be outside the Signal Desk repository")
    if any((parent / ".git").exists() for parent in (root, *root.parents)):
        raise ValueError("Private business storage must be outside any Git repository")
    for name in ("business.sqlite3", "index.html"):
        target = root / name
        if target.is_symlink() or target.resolve().parent != root:
            raise ValueError("Private output must stay inside its external workspace")
    return root


def validate_input(document):
    if not isinstance(document, dict) or set(document) != {"schema_version", "records"} or type(document["schema_version"]) is not int or document["schema_version"] != 1:
        raise ValueError("Expected private business schema version 1")
    if not isinstance(document["records"], list):
        raise ValueError("records must be a list")
    records, ids = [], set()
    for raw in document["records"]:
        if not isinstance(raw, dict) or set(raw) - FIELDS or REQUIRED - set(raw):
            raise ValueError("Invalid private business record fields")
        record = {key: raw.get(key, "") for key in FIELDS}
        if any(not isinstance(value, str) for value in record.values()):
            raise ValueError("Private business fields must be plain text")
        if any(not record[key].strip() for key in REQUIRED):
            raise ValueError("Required private business fields must be nonempty")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", record["id"]) or record["id"] in ids:
            raise ValueError("Private records need unique stable IDs")
        if record["category"] not in CATEGORIES or record["status"] not in STATUSES:
            raise ValueError("Unknown private category or status")
        if record["public_report_id"] and not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", record["public_report_id"]):
            raise ValueError("Invalid public report ID")
        for key in ("checked_on", "due_on"):
            if record[key] and date.fromisoformat(record[key]).isoformat() != record[key]:
                raise ValueError("Use ISO calendar dates")
        ids.add(record["id"])
        records.append(record)
    return records


def connect_private(root=DEFAULT_ROOT):
    root = private_root(root)
    root.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(root / "business.sqlite3")
    conn.row_factory = sqlite3.Row
    columns = ", ".join('"%s" TEXT NOT NULL' % field for field in sorted(FIELDS - {"id"}))
    conn.execute("CREATE TABLE IF NOT EXISTS business_records (id TEXT PRIMARY KEY, %s, revision INTEGER NOT NULL, content_hash TEXT NOT NULL, updated_at TEXT NOT NULL)" % columns)
    conn.execute("CREATE TABLE IF NOT EXISTS business_revisions (id TEXT NOT NULL, revision INTEGER NOT NULL, document TEXT NOT NULL, saved_at TEXT NOT NULL, PRIMARY KEY(id, revision))")
    conn.commit()
    return conn


def import_private(conn, document):
    _assert_private_connection(conn)
    records = validate_input(document)  # Validate the whole batch before mutation.
    stats = {"inserted": 0, "updated": 0, "unchanged": 0}
    with conn:
        for record in records:
            serialized = json.dumps(record, ensure_ascii=False, sort_keys=True)
            digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
            old = conn.execute("SELECT revision, content_hash FROM business_records WHERE id=?", (record["id"],)).fetchone()
            if old and old["content_hash"] == digest:
                stats["unchanged"] += 1
                continue
            revision, saved = old["revision"] + 1 if old else 1, iso_utc()
            fields = sorted(FIELDS)
            columns = fields + ["revision", "content_hash", "updated_at"]
            conn.execute("INSERT OR REPLACE INTO business_records (%s) VALUES (%s)" %
                         (", ".join('"%s"' % key for key in columns), ", ".join("?" for _ in columns)),
                         [record[key] for key in fields] + [revision, digest, saved])
            conn.execute("INSERT INTO business_revisions VALUES (?, ?, ?, ?)", (record["id"], revision, serialized, saved))
            stats["updated" if old else "inserted"] += 1
    return stats


def render_private(conn, root=DEFAULT_ROOT):
    root = private_root(root)
    if _assert_private_connection(conn) != root / "business.sqlite3":
        raise ValueError("Private database and HTML must share the same workspace")
    esc = html.escape
    rows = []
    for item in conn.execute("SELECT * FROM business_records ORDER BY checked_on DESC, id"):
        details = "".join('<dt>%s</dt><dd>%s</dd>' % (label, esc(item[key]) or "미입력") for key, label in (
            ("customer", "고객·파트너"), ("pricing", "가격·비용"), ("proposal", "제안 전략"),
            ("technical_evidence", "내부 기능 검증"), ("source_url", "근거 위치"),
            ("public_report_id", "공개 자료 ID")))
        rows.append('<article data-category="%s" data-status="%s"><p class="meta">%s · %s · %s · %d차</p><h2>%s</h2><p><b>다음 행동</b> %s</p><p>담당 %s · 기한 %s</p><details><summary>사내 검토 내용</summary><dl>%s</dl></details></article>' %
                    (esc(item["category"]), esc(item["status"]), esc(item["category"]), esc(item["status"]), esc(item["checked_on"]), item["revision"], esc(item["title"]), esc(item["next_action"]), esc(item["owner"]) or "미정", esc(item["due_on"]) or "미정", details))
    options = lambda values: "".join('<option>%s</option>' % esc(value) for value in values)
    content = '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>사업기획 사내 작업 자료</title>
<style>body{margin:0;background:#f7f8fa;color:#23303d;font:16px/1.8 system-ui,sans-serif}main{max-width:960px;margin:auto;padding:32px 20px}h1{font-size:28px;margin:0}h2{font-size:21px;margin:0}header{padding:20px 0}.meta{color:#566577;font-size:14px}form{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}label{display:grid;gap:4px}input,select{font:inherit;padding:8px;border:1px solid #bdc7d2;border-radius:6px;max-width:100%%;box-sizing:border-box}article{background:white;border:1px solid #dae1e8;border-radius:10px;padding:22px;margin:18px 0;overflow-wrap:anywhere}details{border-top:1px solid #e5e8ec;padding-top:12px}summary{cursor:pointer}dt{font-weight:700}dd{margin:0 0 14px;white-space:pre-wrap}article[hidden]{display:none}p{margin:8px 0}</style>
<main><header><p class="meta">Signal Desk · 로컬 사내 작업 공간</p><h1>사업기획 사내 작업 자료</h1><p>고객·가격·제안 전략·내부 검증 기록. 파일과 SQLite는 공개 사이트와 분리해 이 컴퓨터에 보관합니다.</p></header>
<form><label>내용 검색<input type="search" id="query"></label><label>분야<select id="category"><option value="">전체</option>%s</select></label><label>상태<select id="status"><option value="">전체</option>%s</select></label></form><p id="count" aria-live="polite"></p>%s
<p>갱신: python -m housing_watch business-private --input &lt;외부 사내 JSON&gt;</p></main>
<script>const records=[...document.querySelectorAll('article')];const controls=['query','category','status'].map(id=>document.getElementById(id));function filter(){const [q,c,s]=controls.map(e=>e.value);let n=0;records.forEach(row=>{row.hidden=!(row.textContent.toLowerCase().includes(q.toLowerCase())&&(!c||row.dataset.category===c)&&(!s||row.dataset.status===s));if(!row.hidden)n++});document.getElementById('count').textContent=n+'건 / 전체 '+records.length+'건'}controls.forEach(e=>e.addEventListener('input',filter));document.querySelector('form').addEventListener('submit',e=>e.preventDefault());filter();</script></html>''' % (options(CATEGORIES), options(STATUSES), "".join(rows))
    target = root / "index.html"
    target.write_text(content, encoding="utf-8")
    return target


def _assert_private_connection(conn):
    main = next(row for row in conn.execute("PRAGMA database_list") if row[1] == "main")
    if not main[2]:
        raise ValueError("Private business records require an external file database")
    target = Path(main[2]).resolve()
    if target.name != "business.sqlite3" or private_root(target.parent) / "business.sqlite3" != target:
        raise ValueError("Refusing private business data in a public or unrelated database")
    return target


def run_private(root=DEFAULT_ROOT, input_path=None):
    root = private_root(root)
    document = None
    if input_path:
        source = Path(input_path).resolve()
        private_root(source.parent)  # Never store authored confidential input in a Git tree.
        document = json.loads(source.read_text(encoding="utf-8-sig"))
        validate_input(document)
    conn = connect_private(root)
    try:
        stats = import_private(conn, document) if document is not None else None
        return {"stats": stats, "path": str(render_private(conn, root))}
    finally:
        conn.close()
