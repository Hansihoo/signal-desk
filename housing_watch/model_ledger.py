"""Accumulating observations from Theo's complete model comparison sources.

Only data is imported: upstream scripts and markup are never executed. Different
evaluation suites/settings remain different observations, including old editions.
"""

import hashlib
import json
import math
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urljoin, urlsplit

from .model_research import CONFIG_PATH, _date
from .timeutil import iso_utc


FILES = {
    "table": "주요 LLM 모델.html", "guides": "llm-model-research.js",
    "availability": "llm-model-availability.json", "models": "llm-model-benchmarks.json",
    "agents": "llm-agent-benchmarks.json", "cursor": "llm-cursor-benchmarks.json",
    "workload": "llm-developer-measurements.json",
}
SPEC_KEYS = ["ordinal", "provider", "model", "release", "kind", "access", "status", "parameters",
             "context", "harness", "agent_index", "deep_swe", "agent_terminal", "swe_atlas",
             "agent_tokens", "agent_minutes", "agent_turns", "agent_cost", "public_coding",
             "tier", "basis", "q4_load", "q4_ram", "q8_load", "fp16_load", "note", "references"]


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def _hash(value):
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _observation_hash(record):
    # Table row numbering is presentation, not a change in model information.
    normalized = json.loads(_json(record))
    cells = normalized.get("original", {}).get("cells", [])
    if normalized["source_kind"] in ("spec", "legacy-agent") and len(cells) == len(SPEC_KEYS):
        normalized["original"]["cells"] = cells[1:]
    return _hash(normalized)


def ensure_model_schema(conn):
    for statement in (
        """CREATE TABLE IF NOT EXISTS model_observations (
        id TEXT PRIMARY KEY, source_kind TEXT NOT NULL, model TEXT NOT NULL, provider TEXT NOT NULL,
        revision INTEGER NOT NULL, content_hash TEXT NOT NULL, document TEXT NOT NULL,
        first_seen_at TEXT NOT NULL, changed_at TEXT NOT NULL, last_seen_at TEXT NOT NULL,
        is_present INTEGER NOT NULL DEFAULT 1)""",
        """CREATE TABLE IF NOT EXISTS model_observation_revisions (
        observation_id TEXT NOT NULL, revision INTEGER NOT NULL, document TEXT NOT NULL,
        saved_at TEXT NOT NULL, changed_fields TEXT NOT NULL,
        PRIMARY KEY(observation_id, revision))""",
        """CREATE TABLE IF NOT EXISTS model_sync_runs (
        id INTEGER PRIMARY KEY, checked_at TEXT NOT NULL, ok INTEGER NOT NULL,
        summary TEXT NOT NULL, error TEXT NOT NULL, raw_paths TEXT NOT NULL)""",
    ):
        conn.execute(statement)


class _ComparisonTable(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.inside = False
        self.rows, self.headers = [], []
        self.row, self.cell = None, None
        self.row_attrs = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "table" and attrs.get("id") == "tbl":
            self.inside = True
        if not self.inside:
            return
        if tag == "tr":
            self.row, self.row_attrs = [], attrs
        if tag in ("td", "th"):
            self.cell = {"text": "", "links": [], "tip": attrs.get("title", ""), "header": tag == "th"}
        if self.cell is not None:
            if attrs.get("data-tip"):
                self.cell["tip"] = attrs["data-tip"]
            if tag == "a" and attrs.get("href"):
                self.cell["links"].append(attrs["href"])
            if tag == "br":
                self.cell["text"] += " "

    def handle_data(self, text):
        if self.inside and self.cell is not None:
            self.cell["text"] += text

    def handle_endtag(self, tag):
        if not self.inside:
            return
        if tag in ("td", "th") and self.cell is not None:
            self.cell["text"] = " ".join(self.cell["text"].split())
            self.row.append(self.cell)
            self.cell = None
        if tag == "tr" and self.row:
            if self.row[0]["header"]:
                self.headers = self.row
            else:
                self.rows.append((self.row_attrs, self.row))
            self.row = None
        if tag == "table":
            self.inside = False


def _safe_url(value, base):
    url = urljoin(base, value)
    if urlsplit(url).scheme != "https" or not urlsplit(url).netloc or urlsplit(url).username:
        raise ValueError("Model evidence requires an HTTPS URL")
    return url


def _number(value, scale=1):
    if value is None:
        return None
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("Invalid numeric model measurement")
    return value * scale


def parse_model_bundle(bodies, config):
    """Normalize all source rows without merging unlike evaluations or filling gaps."""
    base = config["site_url"] + "materials/"
    documents = {key: json.loads(bodies[key].decode("utf-8-sig"))
                 for key in ("availability", "models", "agents", "cursor", "workload")}
    match = re.search(r"\}\)\((\{[\s\S]*\})\);\s*$", bodies["guides"].decode("utf-8-sig"))
    if not match:
        raise ValueError("Upstream generated model data contract changed")
    guides = json.loads(match.group(1))
    parser = _ComparisonTable()
    parser.feed(bodies["table"].decode("utf-8-sig"))
    if len(parser.headers) != len(SPEC_KEYS) or not parser.rows:
        raise ValueError("Upstream comparison table columns changed")
    records, ids = [], set()

    def add(kind, key, model, provider, fields, source, checked="", original=None, tips=None):
        if not isinstance(model, str) or not model.strip() or not isinstance(provider, str):
            raise ValueError("Model observation needs a model and provider")
        identity = kind + ":" + _hash(key)
        if identity in ids:
            raise ValueError("Duplicate model observation identity")
        ids.add(identity)
        source = _safe_url(source, base)
        records.append({"id": identity, "source_kind": kind, "model": model, "provider": provider,
                        "fields": fields, "source_url": source, "checked_on": _date(checked),
                        "original": original or {}, "tips": tips or {}})

    for attrs, cells in parser.rows:
        if len(cells) != len(SPEC_KEYS):
            raise ValueError("Incomplete upstream comparison row")
        fields = {key: cell["text"] or None for key, cell in zip(SPEC_KEYS, cells) if key != "ordinal"}
        model, provider = fields.pop("model"), fields.pop("provider")
        links = [_safe_url(link, base) for cell in cells for link in cell["links"]]
        fields["references"] = list(dict.fromkeys(links))
        fields["suite"] = "기존 표 · Agent v1.3" if attrs.get("data-aa") == "1" else "모델 사양 · 원본 표"
        fields["condition"] = "원본 표의 사양·상태·메모. 행별 확인일 미명시. 로컬 메모리는 원본 추정치."
        kind = "legacy-agent" if attrs.get("data-aa") == "1" else "spec"
        add(kind, [provider, model, fields["kind"], fields["harness"]], model, provider, fields,
            quote(FILES["table"]) + "#tbl", original={"attributes": attrs, "cells": cells},
            tips={key: cell["tip"] for key, cell in zip(SPEC_KEYS, parser.headers)})

    availability = documents["availability"]
    for row in availability["models"]:
        fields = {"status": row.get("status"), "context": row.get("context"),
                  "harness": row["tool"], "kind": "도구 제공 목록", "note": row.get("note"),
                  "suite": availability["scope"], "condition": availability["scope"] + " · " + row.get("note", "")}
        add("availability", [row["id"], row["tool"]], row["name"], row["provider"], fields,
            FILES["availability"], availability["verifiedAt"], row)

    for row in guides["modelRows"]:
        keys = ["intelligence", "briefcase", "automation", "model_terminal", "scicode", "model_cost", "cursor_score", "cursor_cost", "lcr"]
        if len(row["values"]) != len(keys):
            raise ValueError("Guide metric columns changed")
        fields = dict(zip(keys, row["values"]))
        fields.update(effort=row["effort"], context=row.get("context"), note=row.get("note"),
                      kind="이전 모델 가이드", suite="모델 가이드 · 이전 기록", condition="AA 모델 / Cursor 별도 평가 · 원문 기록 " + row["observed"])
        add("legacy-model", row["id"], row["model"], row["provider"] or "미명시", fields, row["source"], row["observed"], row)
    for row in guides["agentRows"]:
        keys = ["agent_index", "deep_swe", "agent_terminal", "swe_atlas", "agent_cost", "agent_minutes", "agent_tokens"]
        if len(row["values"]) != len(keys):
            raise ValueError("Guide agent columns changed")
        fields = dict(zip(keys, row["values"]))
        fields.update(effort=row["effort"], harness=row["harness"], context=row.get("context"), kind="이전 Agent 가이드",
                      suite="Agent · TB 4.0 · 가이드", condition="원본 Agent 가이드 · 평가 기준일 미명시")
        add("legacy-agent-guide", row["id"], row["model"], row["provider"] or "미명시", fields, row["source"], original=row)

    model_doc = documents["models"]
    for row in model_doc["records"]:
        fields = {"kind": "AA 모델 평가", "suite": model_doc["suite"], "label": row["name"], "effort": row["effort"],
                  "release": row.get("release"), "context": row.get("contextTokens"),
                  "parameters": row.get("parameters"), "active_parameters": row.get("activeParameters"),
                  "access": "오픈웨이트" if row.get("isOpenWeights") else "API/클라우드",
                  "intelligence": None if row.get("estimated") else _number(row.get("index")),
                  "estimated_intelligence": row.get("index") if row.get("estimated") else None,
                  "briefcase": _number(row.get("briefcase")), "model_cost": _number(row.get("cost")),
                  "benchmark_versions": model_doc.get("benchmarkVersions", {}),
                  "condition": row["name"] + " · " + model_doc["suite"] + " · 실행일 미명시",
                  "note": "SciCode는 원본에서 평가 재검토 중. 추정 종합 Index는 실측 칸에 표시하지 않음."}
        for target, key in [("automation", "automation"), ("model_terminal", "terminal"), ("scicode", "scicode"), ("lcr", "lcr")]:
            fields[target] = _number(row.get(key), 100)
        add("model", [row["sourceId"], model_doc["suite"], model_doc.get("benchmarkVersions")], row["model"], row["provider"], fields, row["source"], model_doc["verifiedAt"], row)

    agent_doc = documents["agents"]
    for row in agent_doc["records"]:
        fields = {"kind": "코딩 에이전트 평가", "suite": agent_doc["suite"], "effort": row["effort"],
                  "harness": row["harness"], "harness_version": row.get("harnessVersion"),
                  "harness_versions": row.get("harnessVersions"), "agent_index": _number(row.get("index")),
                  "deep_swe": _number(row.get("deepSWE")), "agent_terminal": _number(row.get("terminalBench")),
                  "swe_atlas": _number(row.get("sweAtlas")), "agent_cost": _number(row.get("costUsd")),
                  "agent_minutes": _number(row.get("timeSeconds"), 1 / 60), "agent_tokens": _number(row.get("totalTokens")),
                  "agent_turns": _number(row.get("turns")), "fallback_models": row.get("fallbackModels", []),
                  "retained_attempts": row.get("retainedAttempts"), "benchmark_versions": agent_doc.get("benchmarkVersions"),
                  "condition": agent_doc["suite"] + " · " + row["harness"] + " " + row.get("harnessVersion", "") +
                               " · fallback: " + (", ".join(row.get("fallbackModels", [])) or "없음") + " · 실행일 미명시"}
        add("agent", [row["sourceId"], agent_doc["suite"], agent_doc.get("benchmarkVersions")], row["model"], row["provider"], fields, agent_doc["source"], agent_doc["verifiedAt"], row)

    cursor_doc = documents["cursor"]
    for row in cursor_doc["records"]:
        fields = {"kind": "Cursor 평가", "suite": cursor_doc["suite"], "label": row["label"], "effort": row["effort"], "harness": "Cursor",
                  "cursor_score": _number(row.get("score")), "cursor_cost": _number(row.get("costUsd")),
                  "cursor_tokens": _number(row.get("tokens")), "cursor_steps": _number(row.get("steps")),
                  "condition": cursor_doc["suite"] + " · " + row["label"] + " · AA와 별도 실행 환경 · 실행일 미명시"}
        add("cursor", [row["label"], cursor_doc["suite"]], row["model"], row["provider"], fields, cursor_doc["source"], cursor_doc["verifiedAt"], row)

    for row in documents["workload"]["records"]:
        total, completed, cost = row["totalTasks"], row["completedTasks"], row["totalCostUsd"]
        for key in ("totalTasks", "completedTasks", "unassistedCompletedTasks", "regressionFreeCompletedTasks"):
            if type(row[key]) is not int or row[key] < 0:
                raise ValueError("Invalid workload measurement")
        if _number(cost) is None or cost < 0 or completed > total or any(row[key] > completed for key in ("unassistedCompletedTasks", "regressionFreeCompletedTasks")):
            raise ValueError("Workload successes exceed assigned tasks")
        fields = {"kind": "실사용 측정", "suite": row["testSuite"], "effort": row["effort"], "harness": row["harness"],
                  "unassisted": 100 * row["unassistedCompletedTasks"] / total if total else None,
                  "regression_free": 100 * row["regressionFreeCompletedTasks"] / total if total else None,
                  "success_cost": cost / completed if completed else None,
                  "condition": row["workload"] + " · " + row["testSuite"]}
        add("workload", row["id"], row["model"], row.get("provider", "미명시"), fields, row["source"], row["measuredAt"], row)
    return records


def upsert_model_observations(conn, records, checked_at=None, complete=True):
    ensure_model_schema(conn)
    checked_at = checked_at or iso_utc()
    ids = [record["id"] for record in records]
    if len(set(ids)) != len(ids) or not ids:
        raise ValueError("Model import needs unique nonempty records")
    stats = {"inserted": 0, "updated": 0, "unchanged": 0, "retained": 0, "fetched": len(records)}
    with conn:
        # Missing rows are retained, with an explicit status separate from lifecycle.
        if complete:
            conn.execute("UPDATE model_observations SET is_present=0 WHERE source_kind!='reviewed'")
        for record in records:
            document, digest = _json(record), _observation_hash(record)
            old = conn.execute("SELECT * FROM model_observations WHERE id=?", (record["id"],)).fetchone()
            if old and _observation_hash(json.loads(old["document"])) == digest:
                conn.execute("UPDATE model_observations SET last_seen_at=?, content_hash=?, is_present=1 WHERE id=?", (checked_at, digest, record["id"]))
                stats["unchanged"] += 1
                continue
            previous = json.loads(old["document"]) if old else {}
            fields = sorted(key for key in set(previous.get("fields", {})) | set(record["fields"])
                            if previous.get("fields", {}).get(key) != record["fields"].get(key))
            revision = old["revision"] + 1 if old else 1
            conn.execute("""INSERT INTO model_observations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                ON CONFLICT(id) DO UPDATE SET model=excluded.model, provider=excluded.provider,
                revision=excluded.revision, content_hash=excluded.content_hash, document=excluded.document,
                changed_at=excluded.changed_at, last_seen_at=excluded.last_seen_at, is_present=1""",
                (record["id"], record["source_kind"], record["model"], record["provider"], revision, digest, document,
                 old["first_seen_at"] if old else checked_at, checked_at, checked_at))
            conn.execute("INSERT INTO model_observation_revisions VALUES (?, ?, ?, ?, ?)",
                         (record["id"], revision, document, checked_at, _json(fields)))
            stats["updated" if old else "inserted"] += 1
        stats["retained"] = conn.execute("SELECT COUNT(*) FROM model_observations WHERE is_present=0").fetchone()[0]
    return stats


def import_reviewed_models(conn, document):
    """Add agent-reviewed official facts without replacing an upstream snapshot."""
    if not isinstance(document, dict) or document.get("schema_version") != 1 or not isinstance(document.get("records"), list):
        raise ValueError("Reviewed models need schema_version=1 and records")
    records = []
    for entry in document["records"]:
        for key in ("id", "model", "provider", "source_url", "checked_on"):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                raise ValueError("Reviewed model needs " + key)
        fields = entry.get("fields")
        if not isinstance(fields, dict) or not all(isinstance(fields.get(key), str) and fields[key].strip() for key in ("kind", "suite", "condition")):
            raise ValueError("Reviewed models need kind, suite and source conditions")
        _date(entry["checked_on"])
        source = _safe_url(entry["source_url"], "")
        candidate_ids = entry.get("candidate_ids", [])
        if not isinstance(candidate_ids, list) or any(not isinstance(value, str) or not re.fullmatch(r"news-\d+", value) for value in candidate_ids):
            raise ValueError("Reviewed candidate IDs must refer to news records")
        for url in fields.get("references", []):
            _safe_url(url, "")
        identity = "reviewed:" + _hash([entry["id"], entry["model"], fields.get("effort"), fields.get("harness"), fields["suite"]])
        records.append({"id": identity, "source_kind": "reviewed", "model": entry["model"], "provider": entry["provider"],
                        "fields": fields, "source_url": source, "checked_on": entry["checked_on"], "original": entry, "tips": {}})
    return upsert_model_observations(conn, records, complete=False)


def _read_material(url):
    request = urllib.request.Request(url, headers={"User-Agent": "SignalDesk/0.1"})
    with urllib.request.urlopen(request, timeout=20) as response:
        if response.geturl() != url:
            raise ValueError("Unexpected model material redirect")
        body = response.read(4 * 1024 * 1024 + 1)
    if len(body) > 4 * 1024 * 1024:
        raise ValueError("Model material is too large")
    return body


def collect_model_ledger(conn, raw_dir="data/raw/ai_news/model_ledger"):
    ensure_model_schema(conn)
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    bodies, paths, checked = {}, {}, iso_utc()
    try:
        for key, filename in FILES.items():
            body = _read_material(config["site_url"] + "materials/" + quote(filename))
            path = Path(raw_dir) / (key + "_" + hashlib.sha256(body).hexdigest() + Path(filename).suffix)
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_bytes(body)
            bodies[key], paths[key] = body, str(path)
        records = parse_model_bundle(bodies, config)
        stats = upsert_model_observations(conn, records, checked)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        conn.execute("INSERT INTO model_sync_runs(checked_at,ok,summary,error,raw_paths) VALUES (?,0,'{}',?,?)",
                     (checked, str(exc), _json(paths)))
        conn.commit()
        raise ValueError("Model ledger refresh failed; previous observations retained: " + str(exc)) from exc
    conn.execute("INSERT INTO model_sync_runs(checked_at,ok,summary,error,raw_paths) VALUES (?,1,?,'',?)", (checked, _json(stats), _json(paths)))
    conn.commit()
    return stats


def export_model_ledger(conn):
    ensure_model_schema(conn)
    records = []
    for row in conn.execute("SELECT * FROM model_observations ORDER BY is_present DESC, model, source_kind, id"):
        records.append(dict(json.loads(row["document"]), revision=row["revision"], changed_at=row["changed_at"],
                            first_seen_at=row["first_seen_at"], retained=not row["is_present"]))
    history = [dict(json.loads(row["document"]), revision=row["revision"], saved_at=row["saved_at"],
                    changed_fields=json.loads(row["changed_fields"]))
               for row in conn.execute("SELECT * FROM model_observation_revisions ORDER BY saved_at DESC, observation_id, revision DESC")]
    runs = [dict(checked_at=row["checked_at"], ok=bool(row["ok"]), summary=json.loads(row["summary"]), error=row["error"])
            for row in conn.execute("SELECT * FROM model_sync_runs ORDER BY id DESC LIMIT 20")]
    return {"schema_version": 1, "records": records, "history": history, "runs": runs}
