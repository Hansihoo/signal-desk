import re

from .textutil import clean_text, stable_space


M2_TO_PYEONG = 0.3025


def enrich_item_from_detail(item, html_text):
    text = clean_text(html_text)
    focused = _focus_text(text, item.get("title", ""))

    detail = {
        "detail_text": _clip(focused, 4000),
        "address": _extract_address(focused),
        "area_range_m2": _extract_area(focused),
        "supply_units": _extract_supply_units(focused),
        "deposit": _extract_money(focused, ["임대보증금", "보증금"]),
        "monthly_rent": _extract_money(focused, ["월임대료", "임대료"]),
        "price": _extract_money(focused, ["분양가격", "공급가격", "가격"]),
        "eligibility": _extract_eligibility(focused),
        "application_period": _extract_application_period(focused),
        "move_in_month": _extract_after_label(focused, "입주예정월", 30),
    }
    detail["area_range_pyeong"] = _area_to_pyeong(detail["area_range_m2"])
    detail["detail_summary"] = build_detail_summary(detail)
    item.update(detail)
    if detail["detail_summary"]:
        item["summary"] = stable_space("%s %s" % (item.get("summary", ""), detail["detail_summary"]))
    if detail["detail_text"]:
        item["raw_text"] = stable_space("%s %s" % (item.get("raw_text", ""), detail["detail_text"]))
    return item


def build_detail_summary(detail):
    parts = []
    if detail.get("address"):
        parts.append("주소 %s" % detail["address"])
    if detail.get("area_range_m2"):
        area = detail["area_range_m2"]
        if detail.get("area_range_pyeong"):
            area = "%s (%s)" % (area, detail["area_range_pyeong"])
        parts.append("면적 %s" % area)
    if detail.get("supply_units"):
        parts.append("공급 %s" % detail["supply_units"])
    if detail.get("eligibility"):
        parts.append("조건 %s" % detail["eligibility"])
    if detail.get("application_period"):
        parts.append("접수 %s" % detail["application_period"])
    return " · ".join(parts)


def _focus_text(text, title):
    anchors = []
    if title:
        idx = text.find(title)
        if idx >= 0:
            anchors.append(idx)
    for marker in ["공고내용", "공급정보", "신청자격", "모집공고일", "소재지"]:
        idx = text.find(marker)
        if idx >= 0:
            anchors.append(idx)
    if not anchors:
        return text[:12000]
    start = max(0, min(anchors) - 300)
    return text[start : start + 12000]


def _extract_address(text):
    patterns = [
        r"소재지\s*:\s*(.+?)(?=\s+(?:전용면적|총 세대수|난방방식|입주예정월|function|공급정보))",
        r"주소\s*[:：]\s*(.+?)(?=\s+(?:전용면적|총 세대수|난방방식|입주예정월|신청|접수|$))",
    ]
    for pattern in patterns:
        value = _first_group(pattern, text)
        if value:
            return _clean_value(value)
    return ""


def _extract_area(text):
    value = _first_group(r"전용면적\(?㎡\)?\s*:\s*([0-9.,~\-\s㎡m²]+)", text)
    if value:
        return _normalize_area(value)
    value = _first_group(r"전용\s*([0-9.,~\-\s]+)\s*㎡", text)
    if value:
        return _normalize_area(value)
    return ""


def _extract_supply_units(text):
    for pattern in [
        r"총\s*세대수\s*:\s*([0-9,]+(?:\s*세대)?)",
        r"공급호수\s*:\s*(.+?)(?=\s+○|\s+■|\s+신청|\s+접수|\s*$)",
        r"모집호수\s*:\s*(.+?)(?=\s+○|\s+■|\s+신청|\s+접수|\s*$)",
    ]:
        value = _first_group(pattern, text)
        if value:
            cleaned = _clip(_clean_value(value), 80)
            if pattern.startswith("총") and "세대" not in cleaned:
                cleaned = "%s 세대" % cleaned
            return cleaned
    return ""


def _extract_money(text, labels):
    for label in labels:
        pattern = r"%s\s*[:：]?\s*([0-9,]+(?:\s*원|\s*천원|\s*만원)?(?:\s*[~\-]\s*[0-9,]+(?:\s*원|\s*천원|\s*만원)?)?)" % re.escape(label)
        value = _first_group(pattern, text)
        if value:
            return _clean_value(value)
    return ""


def _extract_eligibility(text):
    patterns = [
        r"신청자격\s*[:：]\s*(.+?)(?=\s+■|\s+○|\s+접수|\s+신청방법|\s+신청문의|\s*$)",
        r"공급대상\s*[:：]\s*(.+?)(?=\s+■|\s+○|\s+접수|\s+신청방법|\s*$)",
    ]
    for pattern in patterns:
        value = _first_group(pattern, text)
        if value:
            return _clip(_clean_value(value), 90)
    keyword_hits = []
    for keyword in ["청년", "대학생", "신혼부부", "한부모", "고령자", "주거급여수급자", "무주택", "청년창업인"]:
        if keyword in text:
            keyword_hits.append(keyword)
    return ", ".join(dict.fromkeys(keyword_hits[:6]))


def _extract_application_period(text):
    patterns = [
        r"신청기간\s*[:：]\s*(.+?)(?=\s+■|\s+○|\s+신청자격|\s+신청문의|\s*$)",
        r"인터넷\s*접수\s*[:：]\s*(.+?)(?=\s+○|\s+■|\s+방문|\s+서류|\s*$)",
        r"접수\s*[:：]\s*(.+?)(?=\s+■|\s+○|\s+서류|\s*$)",
    ]
    for pattern in patterns:
        value = _first_group(pattern, text)
        if value:
            return _clip(_clean_value(value), 90)
    return ""


def _extract_after_label(text, label, max_len):
    value = _first_group(r"%s\s*:\s*(.+?)(?=\s+[가-힣A-Za-z]+\s*:|\s+function|\s+공급정보|\s*$)" % re.escape(label), text)
    return _clip(_clean_value(value), max_len) if value else ""


def _area_to_pyeong(value):
    numbers = [float(number.replace(",", "")) for number in re.findall(r"\d+(?:\.\d+)?", value or "")]
    if not numbers:
        return ""
    converted = [round(number * M2_TO_PYEONG, 1) for number in numbers[:2]]
    if len(converted) == 1:
        return "%.1f평" % converted[0]
    return "%.1f~%.1f평" % (converted[0], converted[1])


def _normalize_area(value):
    cleaned = _clean_value(value)
    cleaned = cleaned.replace("m²", "㎡").replace("m2", "㎡")
    cleaned = re.sub(r"\s+", "", cleaned)
    if "㎡" not in cleaned:
        cleaned = "%s㎡" % cleaned
    return cleaned


def _first_group(pattern, text):
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return match.group(1)


def _clean_value(value):
    value = stable_space(value)
    value = value.replace("-->", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -·:：|")


def _clip(value, max_len):
    value = stable_space(value or "")
    if len(value) <= max_len:
        return value
    return value[: max_len - 1].rstrip() + "…"
