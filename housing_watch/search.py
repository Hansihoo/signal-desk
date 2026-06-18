from datetime import datetime

from .db import all_items
from .textutil import cosine, tokens


ACTIVE_STATUSES = {"모집중", "접수중", "공고중", "정정공고중"}


def search_items(conn, query, limit=8):
    query = query.strip()
    if not query:
        return []
    query_tokens = set(tokens(query))
    scored = []
    for item in all_items(conn):
        haystack = " ".join(
            [
                item.get("title") or "",
                item.get("summary") or "",
                item.get("raw_text") or "",
                item.get("region") or "",
                item.get("category") or "",
                item.get("agency") or "",
                item.get("address") or "",
                item.get("area_range_m2") or "",
                item.get("area_range_pyeong") or "",
                item.get("supply_units") or "",
                item.get("deposit") or "",
                item.get("monthly_rent") or "",
                item.get("price") or "",
                item.get("eligibility") or "",
                item.get("application_period") or "",
                item.get("detail_summary") or "",
            ]
        )
        score = cosine(query, haystack) * 5.0
        if query in haystack:
            score += 4.0
        item_tokens = set(tokens(haystack))
        score += len(query_tokens.intersection(item_tokens)) * 0.8
        score += min(item.get("importance") or 0, 10) * 0.15
        if item.get("status") in ACTIVE_STATUSES:
            score += 1.0
        if _deadline_is_future(item.get("deadline_at")):
            score += 0.5
        if score > 0:
            result = dict(item)
            result["score"] = round(score, 4)
            scored.append(result)
    scored.sort(key=lambda row: row["score"], reverse=True)
    return scored[:limit]


def _deadline_is_future(value):
    if not value:
        return False
    try:
        return datetime.strptime(value, "%Y-%m-%d").date() >= datetime.now().date()
    except ValueError:
        return False


def format_search_results(results):
    if not results:
        return "검색 결과가 없습니다."
    lines = []
    for index, item in enumerate(results, 1):
        lines.append(
            "%d. [%s/%s] %s\n   지역: %s | 상태: %s | 게시: %s | 마감: %s | score: %.2f\n   주소: %s | 면적: %s | 공급: %s | 가격: %s | 조건: %s\n   %s"
            % (
                index,
                item.get("agency") or "-",
                item.get("category") or "-",
                item.get("title") or "-",
                item.get("region") or "-",
                item.get("status") or "-",
                item.get("published_at") or "-",
                item.get("deadline_at") or "-",
                item.get("score") or 0,
                item.get("address") or "원문 확인",
                _area_label(item),
                item.get("supply_units") or "원문 확인",
                _price_label(item),
                item.get("eligibility") or "원문 확인",
                item.get("url") or "",
            )
        )
    return "\n".join(lines)


def format_context(results, query):
    lines = [
        "# Housing Watch Search Context",
        "",
        "Question: %s" % query,
        "",
        "Use these locally collected notices as source context. Verify final application details from the linked official page before acting.",
        "",
    ]
    for index, item in enumerate(results, 1):
        lines.extend(
            [
                "## Result %d" % index,
                "",
                "- Title: %s" % (item.get("title") or ""),
                "- Agency: %s" % (item.get("agency") or ""),
                "- Category: %s" % (item.get("category") or ""),
                "- Region: %s" % (item.get("region") or ""),
                "- Status: %s" % (item.get("status") or ""),
                "- Published: %s" % (item.get("published_at") or ""),
                "- Deadline: %s" % (item.get("deadline_at") or ""),
                "- Address: %s" % (item.get("address") or "원문 확인"),
                "- Area: %s" % (_area_label(item)),
                "- Supply: %s" % (item.get("supply_units") or "원문 확인"),
                "- Price: %s" % (_price_label(item)),
                "- Eligibility: %s" % (item.get("eligibility") or "원문 확인"),
                "- Application Period: %s" % (item.get("application_period") or "원문 확인"),
                "- Detail Summary: %s" % (item.get("detail_summary") or "원문 확인"),
                "- Importance: %s" % (item.get("importance") or 0),
                "- URL: %s" % (item.get("url") or ""),
                "",
            ]
        )
    return "\n".join(lines)


def _area_label(item):
    if item.get("area_range_m2") and item.get("area_range_pyeong"):
        return "%s / %s" % (item["area_range_m2"], item["area_range_pyeong"])
    return item.get("area_range_m2") or item.get("area_range_pyeong") or "원문 확인"


def _price_label(item):
    parts = []
    if item.get("deposit"):
        parts.append("보증금 %s" % item["deposit"])
    if item.get("monthly_rent"):
        parts.append("월 %s" % item["monthly_rent"])
    if item.get("price"):
        parts.append(item["price"])
    return " / ".join(parts) if parts else "원문/PDF 확인"
