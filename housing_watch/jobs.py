import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from .db import record_snapshot, upsert_job_items
from .timeutil import compact_timestamp, iso_utc


SARAMIN_JOB_SEARCH_URL = "https://oapi.saramin.co.kr/job-search"
USER_AGENT = "SignalDesk/0.1 (+local personal job briefing)"


JOB_REQUIRED_FIELDS = (
    "company_name",
    "posting_title",
    "work_summary",
    "requirements",
    "preferred",
    "location",
    "salary_10y",
    "deadline_at",
    "url",
)

ALIASES = {
    "company_name": ("company_name", "company", "회사명"),
    "posting_title": ("posting_title", "title", "공고명", "채용공고명"),
    "work_summary": ("work_summary", "job_description", "doing", "하는일", "하는 일", "직무내용"),
    "requirements": ("requirements", "qualification", "자격요건", "지원자격"),
    "preferred": ("preferred", "preferred_qualifications", "우대사항"),
    "location": ("location", "region", "지역", "근무지"),
    "salary_10y": ("salary_10y", "salary", "10연차 연봉", "10년차 연봉"),
    "salary_basis": ("salary_basis", "연봉근거", "연봉 근거"),
    "deadline_at": ("deadline_at", "deadline", "마감일"),
    "url": ("url", "link", "링크"),
    "source_name": ("source_name", "source", "출처"),
    "company_size": ("company_size", "회사규모"),
    "seniority": ("seniority", "경력"),
    "employment_type": ("employment_type", "고용형태"),
    "published_at": ("published_at", "posted_at", "등록일"),
}


class JobImportError(Exception):
    pass


class JobFetchError(Exception):
    pass


def collect_jobs_from_json(conn, input_path, source_id="manual_jobs", raw_dir="data/raw/jobs"):
    items, raw_bytes = load_job_items_from_json(input_path, source_id=source_id)
    stats = upsert_job_items(conn, items)
    raw_path = write_raw_snapshot(raw_bytes, raw_dir, source_id)
    record_snapshot(conn, source_id, raw_path, len(items))
    conn.commit()
    return {
        "source_id": source_id,
        "raw_path": raw_path,
        "fetched": len(items),
        "inserted": stats["inserted"],
        "updated": stats["updated"],
    }


def collect_jobs_from_saramin(
    conn,
    access_key=None,
    keywords=None,
    count=30,
    source_id="saramin_api",
    raw_dir="data/raw/jobs",
    salary_estimates_path=None,
    minimum_fit_score=4,
    params=None,
):
    access_key = access_key or os.environ.get("SIGNAL_DESK_SARAMIN_KEY")
    if not access_key:
        raise JobFetchError("SIGNAL_DESK_SARAMIN_KEY is not set")

    keywords = keywords or ["C++ 엔진", "C++ Windows", "오피스 개발", "스프레드시트 개발"]
    salary_estimates = load_salary_estimates(salary_estimates_path)
    all_items = []
    raw_responses = []
    for keyword in keywords:
        payload, url = fetch_saramin_jobs(access_key, keyword, count=count, params=params)
        raw_responses.append({"keyword": keyword, "url": _redact_access_key(url), "payload": payload})
        parsed = parse_saramin_jobs(payload, source_id=source_id, query=keyword, salary_estimates=salary_estimates)
        all_items.extend(parsed)

    items = dedupe_job_items(all_items)
    if minimum_fit_score is not None:
        items = [item for item in items if item.get("fit_score", 0) >= minimum_fit_score]

    stats = upsert_job_items(conn, items)
    raw_bytes = json.dumps(
        {
            "source_id": source_id,
            "queries": keywords,
            "minimum_fit_score": minimum_fit_score,
            "responses": raw_responses,
            "normalized_count": len(items),
        },
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    raw_path = write_raw_snapshot(raw_bytes, raw_dir, source_id)
    record_snapshot(conn, source_id, raw_path, len(items))
    conn.commit()
    return {
        "source_id": source_id,
        "raw_path": raw_path,
        "fetched": len(all_items),
        "kept": len(items),
        "inserted": stats["inserted"],
        "updated": stats["updated"],
    }


def fetch_saramin_jobs(access_key, keyword, count=30, params=None):
    request_params = {
        "access-key": access_key,
        "keywords": keyword,
        "count": str(min(max(int(count or 30), 1), 110)),
        "start": "0",
        "sort": "pd",
        "sr": "directhire",
        "fields": "posting-date,expiration-date,count",
    }
    if params:
        for key, value in params.items():
            if value is not None and str(value).strip():
                request_params[key] = str(value).strip()
    url = SARAMIN_JOB_SEARCH_URL + "?" + urllib.parse.urlencode(request_params)
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            body = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read(300).decode("utf-8", "replace").strip()
        raise JobFetchError("Saramin HTTP %d: %s" % (exc.code, detail))
    except urllib.error.URLError as exc:
        raise JobFetchError("Saramin request failed: %s" % exc)

    try:
        payload = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise JobFetchError("Saramin returned invalid JSON: %s" % exc)
    if isinstance(payload, dict) and payload.get("code"):
        raise JobFetchError("Saramin API error %s: %s" % (payload.get("code"), payload.get("message", "")))
    return payload, url


def parse_saramin_jobs(payload, source_id="saramin_api", query="", salary_estimates=None):
    jobs = _as_list(_as_dict(payload.get("jobs")).get("job") if isinstance(payload, dict) else None)
    items = []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        if str(job.get("active", "1")) == "0":
            continue
        position = _as_dict(job.get("position"))
        company = _as_dict(job.get("company"))
        company_detail = _as_dict(company.get("detail"))
        company_name = _text(company_detail.get("name") or company.get("name"))
        posting_title = _text(position.get("title"))
        url = _text(job.get("url"))
        if not company_name or not posting_title or not url:
            continue

        experience = _as_dict(position.get("experience-level"))
        seniority = _text(experience.get("name") or position.get("experience-level")) or "경력 확인 필요"
        if not is_senior_saramin_job(posting_title, seniority, experience):
            continue

        location = _name_field(position.get("location")) or "근무지 확인 필요"
        job_code = _name_field(position.get("job-code")) or _name_field(position.get("job-mid-code"))
        keyword_text = _text(job.get("keyword"))
        industry = _name_field(position.get("industry"))
        education = _name_field(position.get("required-education-level"))
        employment_type = _name_field(position.get("job-type"))
        source_salary = _name_field(job.get("salary"))
        salary_10y, salary_basis = salary_for_company(company_name, salary_estimates or {}, source_salary)
        deadline_at = _saramin_deadline(job)
        published_at = _date_only(_text(job.get("posting-date"))) or _date_from_timestamp(job.get("posting-timestamp"))

        raw_payload = json.dumps(job, ensure_ascii=False, sort_keys=True)
        item = {
            "source_id": source_id,
            "external_id": str(job.get("id") or _hash(company_name + posting_title + url)),
            "company_name": company_name,
            "posting_title": posting_title,
            "work_summary": saramin_work_summary(posting_title, job_code, keyword_text, industry, query),
            "requirements": saramin_requirements(seniority, education),
            "preferred": "상세 우대사항은 공고 원문 확인",
            "location": location,
            "salary_10y": salary_10y,
            "salary_basis": salary_basis,
            "deadline_at": deadline_at,
            "url": url,
            "source_name": "Saramin Open API",
            "company_size": saramin_company_size_hint(job),
            "seniority": seniority,
            "employment_type": employment_type,
            "published_at": published_at,
            "fit_score": 0,
            "raw_payload": raw_payload,
            "content_hash": _hash(raw_payload),
            "collected_at": iso_utc(),
        }
        item["fit_score"] = score_job_for_profile(item)
        items.append(item)
    return items


def load_job_items_from_json(input_path, source_id="manual_jobs"):
    path = Path(input_path)
    raw_bytes = path.read_bytes()
    try:
        payload = json.loads(raw_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise JobImportError("invalid jobs JSON: %s" % exc)

    records = payload.get("items") or payload.get("jobs") if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        raise JobImportError("jobs JSON must be a list or an object with items/jobs")

    items = [normalize_job_item(record, source_id=source_id) for record in records]
    return items, raw_bytes


def normalize_job_item(record, source_id="manual_jobs"):
    if not isinstance(record, dict):
        raise JobImportError("each job record must be an object")

    item = {
        "source_id": record.get("source_id") or source_id,
        "company_name": _pick(record, "company_name"),
        "posting_title": _pick(record, "posting_title"),
        "work_summary": _pick(record, "work_summary") or "확인 필요",
        "requirements": _pick(record, "requirements") or "확인 필요",
        "preferred": _pick(record, "preferred") or "확인 필요",
        "location": _pick(record, "location") or "확인 필요",
        "salary_10y": _pick(record, "salary_10y") or "별도 조사 필요",
        "salary_basis": _pick(record, "salary_basis"),
        "deadline_at": _pick(record, "deadline_at") or "마감일 확인",
        "url": _pick(record, "url"),
        "source_name": _pick(record, "source_name"),
        "company_size": _pick(record, "company_size") or "중견/대기업 후보",
        "seniority": _pick(record, "seniority") or "경력",
        "employment_type": _pick(record, "employment_type"),
        "published_at": _pick(record, "published_at"),
        "collected_at": record.get("collected_at") or iso_utc(),
    }

    missing = [field for field in ("company_name", "posting_title", "url") if not item.get(field)]
    if missing:
        raise JobImportError("missing required job fields: %s" % ", ".join(missing))

    item["external_id"] = record.get("external_id") or _hash(
        "|".join([item["company_name"], item["posting_title"], item["url"]])
    )
    item["fit_score"] = int(record.get("fit_score") or score_job_for_profile(item))
    item["raw_payload"] = json.dumps(record, ensure_ascii=False, sort_keys=True)
    item["content_hash"] = _hash(item["raw_payload"])
    return item


def load_job_source_config(path="config/job_sources.json"):
    config_path = Path(path)
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise JobImportError("invalid job source config: %s" % exc)


def saramin_options_from_config(config):
    saramin = (config or {}).get("saramin") or {}
    return {
        "enabled": bool(saramin.get("enabled", False)),
        "env_key": saramin.get("env_key") or "SIGNAL_DESK_SARAMIN_KEY",
        "keywords": saramin.get("keywords") or [],
        "count": int(saramin.get("count") or 30),
        "params": saramin.get("params") or {},
        "minimum_fit_score": saramin.get("minimum_fit_score", 4),
        "salary_estimates_path": saramin.get("salary_estimates") or "",
    }


def load_salary_estimates(path=None):
    if not path:
        return {}
    salary_path = Path(path)
    if not salary_path.exists():
        return {}
    try:
        payload = json.loads(salary_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise JobImportError("invalid salary estimates JSON: %s" % exc)
    rows = payload.get("items") if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        return {}
    estimates = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        company = _text(row.get("company_name") or row.get("회사명"))
        salary = _text(row.get("salary_10y") or row.get("10년차 연봉") or row.get("10연차 연봉"))
        if not company or not salary:
            continue
        estimates[_company_key(company)] = {
            "salary_10y": salary,
            "salary_basis": _text(row.get("salary_basis") or row.get("연봉근거") or row.get("연봉 근거")),
        }
    return estimates


def salary_for_company(company_name, salary_estimates, source_salary=""):
    estimate = salary_estimates.get(_company_key(company_name))
    if estimate:
        return estimate["salary_10y"], estimate.get("salary_basis") or "회사명 기준 연봉 조사값"
    if source_salary:
        return "별도 조사 필요", "사람인 공고 연봉: %s; 10년차 연봉 별도 조사 필요" % source_salary
    return "별도 조사 필요", "10년차 연봉 별도 조사 필요"


def saramin_work_summary(title, job_code, keyword_text, industry, query):
    parts = []
    if job_code:
        parts.append("직무: %s" % job_code)
    if industry:
        parts.append("업종: %s" % industry)
    if keyword_text:
        parts.append("키워드: %s" % keyword_text)
    if not parts:
        parts.append("공고 제목 기준: %s" % title)
    if query:
        parts.append("검색어: %s" % query)
    return _short_text("; ".join(parts), 180)


def saramin_requirements(seniority, education):
    parts = [seniority or "경력 확인 필요"]
    if education:
        parts.append(education)
    parts.append("상세 자격요건은 공고 원문 확인")
    return " / ".join(parts)


def saramin_company_size_hint(job):
    stock = _text(job.get("stock"))
    if stock:
        return "상장/중견 이상 후보"
    return "중견/대기업 후보"


def is_senior_saramin_job(title, seniority, experience):
    title_text = (title or "").lower()
    seniority_text = seniority or ""
    code = str(experience.get("code", ""))
    min_years = _safe_int(experience.get("min"))
    if code == "1" or seniority_text == "신입":
        return False
    if "신입" in seniority_text and "경력" not in seniority_text:
        return False
    if min_years is not None and min_years >= 5:
        return True
    if any(keyword in seniority_text for keyword in ("경력", "시니어", "년")):
        return True
    return any(keyword in title_text for keyword in ("senior", "시니어", "리드", "lead", "경력"))


def dedupe_job_items(items):
    seen = set()
    deduped = []
    for item in sorted(items, key=lambda value: value.get("fit_score", 0), reverse=True):
        key = "|".join([_company_key(item.get("company_name")), _company_key(item.get("posting_title")), item.get("url") or ""])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def score_job_for_profile(item):
    text = " ".join(
        [
            item.get("posting_title", ""),
            item.get("work_summary", ""),
            item.get("requirements", ""),
            item.get("preferred", ""),
            item.get("location", ""),
            item.get("seniority", ""),
        ]
    ).lower()
    score = 0
    for keyword in ("c++", "cpp", "c/c++", "엔진", "오피스", "스프레드시트", "sheet", "windows", "desktop"):
        if keyword in text:
            score += 2
    for keyword in ("경력", "10년", "시니어", "리드", "lead", "principal", "staff"):
        if keyword in text:
            score += 1
    for keyword in ("서울", "경기", "판교", "성남", "강남", "구로", "마곡"):
        if keyword in text:
            score += 1
            break
    return min(score, 10)


def write_raw_snapshot(raw_bytes, raw_dir, source_id):
    path = Path(raw_dir) / ("%s_%s.json" % (source_id, compact_timestamp()))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw_bytes)
    return str(path)


def _pick(record, canonical):
    for key in ALIASES[canonical]:
        value = record.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def _as_dict(value):
    return value if isinstance(value, dict) else {}


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _name_field(value):
    if isinstance(value, dict):
        return _text(value.get("name") or value.get("#text") or value.get("value"))
    return _text(value)


def _text(value):
    if value is None:
        return ""
    return str(value).strip()


def _short_text(value, limit):
    value = " ".join((value or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def _date_only(value):
    value = value or ""
    if not value:
        return ""
    return value[:10]


def _date_from_timestamp(value):
    try:
        timestamp = int(value)
    except (TypeError, ValueError):
        return ""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()


def _saramin_deadline(job):
    date_value = _date_only(_text(job.get("expiration-date")))
    if date_value:
        return date_value
    timestamp_value = _date_from_timestamp(job.get("expiration-timestamp"))
    if timestamp_value:
        return timestamp_value
    close_type = _as_dict(job.get("close-type"))
    return _text(close_type.get("name") or job.get("close-type")) or "마감일 확인"


def _safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _company_key(value):
    text = _text(value).lower()
    for token in ("(주)", "주식회사", "㈜", " ", "\t", "\n"):
        text = text.replace(token, "")
    return "".join(ch for ch in text if ch.isalnum())


def _redact_access_key(url):
    parsed = urllib.parse.urlsplit(url)
    pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query = urllib.parse.urlencode([(key, "***" if key == "access-key" else value) for key, value in pairs])
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query, parsed.fragment))


def _hash(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
