"""Import Theo's public model research catalog as references, not verified news."""

import hashlib
import json
import re
import urllib.error
import urllib.request
import uuid
from datetime import date
from pathlib import Path

from .db import record_snapshot, upsert_news_items
from .timeutil import compact_timestamp, iso_utc


CONFIG_PATH = Path(__file__).resolve().parent.parent / "config/ai_model_research.json"
SOURCE_ID = "ai_theo_model_research"


def _date(value):
    if value in (None, ""):
        return ""
    if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
        raise ValueError("Model research dates must be YYYY-MM-DD")
    return value


def parse_model_catalog(document, config):
    """Preserve source update/check dates and canonical document identity."""
    if not isinstance(document, dict) or not isinstance(document.get("documents"), list):
        raise ValueError("Model research catalog requires documents")
    items, slugs = [], set()
    for entry in document["documents"]:
        if not isinstance(entry, dict):
            raise ValueError("Invalid model research entry")
        if entry.get("category") not in config["categories"] and entry.get("slug") not in config["additional_slugs"]:
            continue
        slug = entry.get("slug", "")
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", slug) or slug in slugs:
            raise ValueError("Invalid or duplicate model research slug")
        slugs.add(slug)
        title, description = entry.get("title"), entry.get("description")
        if not isinstance(title, str) or not title.strip() or not isinstance(description, str):
            raise ValueError("Model research needs plain title and description")
        digest = entry.get("sha256", "")
        if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise ValueError("Model research needs its source content hash")
        updated, reference = _date(entry.get("updatedAt")), _date(entry.get("referenceDate"))
        detail = "%s\n자료 수정일: %s · 원자료 기준일: %s. Theo의 정리 자료이며 공식 발표의 독립 재검증 결과가 아닙니다." % (
            description, updated or "미표기", reference or "미표기")
        payload = {
            "source_tier": "authored-research", "upstream_category": entry["category"],
            "upstream_sha256": digest, "reference_date": reference, "updated_at": updated,
            "repository_url": config["repository_url"], "detail": detail,
            "developer_impact": "모델·추론 설정·Agent/Harness·평가판을 맞춰 비교하세요. 서로 다른 평가 환경의 점수를 직접 합치지 않습니다.",
            "action_needed": "선택 전 제공자의 공식 모델 목록·가격·제한·종료 일정을 다시 확인하고, 현재 작업의 샘플로 검증하세요.",
        }
        raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        url = config["site_url"] + "docs/" + slug + "/"
        content = json.dumps({"title": title, "url": url, "payload": payload}, ensure_ascii=False, sort_keys=True)
        items.append({
            "source_id": SOURCE_ID, "external_id": slug, "title": title, "title_ko": title,
            "url": url, "source_name": "Theo 모델 리서치", "source_url": config["site_url"],
            "category": "LLM 모델", "language": "Korean", "country": "",
            "published_at": updated + "T00:00:00Z" if updated else "",
            "summary_ko": description or "Theo의 모델 비교 자료를 원문에서 확인합니다.",
            "score": 100, "raw_payload": raw,
            "content_hash": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "collected_at": iso_utc(),
        })
    if not items:
        raise ValueError("No model research documents matched the configured scope")
    return items


def _read_catalog(url):
    request = urllib.request.Request(url, headers={"User-Agent": "SignalDesk/0.1"})
    with urllib.request.urlopen(request, timeout=20) as response:
        if response.geturl() != url:
            raise ValueError("Unexpected model catalog redirect")
        body = response.read(2 * 1024 * 1024 + 1)
    if len(body) > 2 * 1024 * 1024:
        raise ValueError("Model research catalog is too large")
    return body


def collect_model_research(conn, raw_dir="data/raw/ai_news/model_research"):
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    body = _read_catalog(config["catalog_url"])
    path = Path(raw_dir) / ("theo_model_catalog_%s_%s.json" % (compact_timestamp(), uuid.uuid4().hex[:8]))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    items = parse_model_catalog(json.loads(body.decode("utf-8")), config)
    existing = {row["external_id"]: row["content_hash"] for row in conn.execute(
        "SELECT external_id, content_hash FROM news_items WHERE source_id=?", (SOURCE_ID,))}
    changed = [item for item in items if existing.get(item["external_id"]) != item["content_hash"]]
    stats = upsert_news_items(conn, changed, source_ids=[SOURCE_ID], dedupe_by_title=False)
    record_snapshot(conn, SOURCE_ID, str(path), len(items))
    conn.commit()
    return dict(stats, fetched=len(items), unchanged=len(items) - len(changed), raw_path=str(path))
