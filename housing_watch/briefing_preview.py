"""Two-page editorial template preview; not a new collector or archive format."""

import hashlib
import html
from pathlib import Path
from urllib.parse import urlencode

from .research_topics import public_url


CHECKED_ON = "2026.10.03"


def storage_scenarios(topics=10, weeks=52, years=10):
    """Decimal KB/MB, one stored copy per report; maximum one report/topic/week."""
    reports = topics * weeks * years
    return [(label, size_kb, reports * size_kb / 1000) for label, size_kb in (
        ("텍스트 중심", 50), ("표·그래프 포함", 100), ("이미지 포함", 1000))]


def _escape(value):
    return html.escape(str(value), quote=True)


def _topic_rows(snapshot):
    rows = []
    for topic in snapshot.get("topics", []):
        if topic.get("stage") == "outline":
            continue
        items = [item for item in snapshot.get("items", [])
                 if item.get("topic_id") == topic["id"] and public_url(item.get("url"))]
        items.sort(key=lambda item: (item.get("published_at") or "", item.get("first_seen_at") or ""), reverse=True)
        topic_url = "../research/%s/index.html" % _escape(topic["id"])
        if items:
            latest = items[0]
            query = urlencode({"section": latest.get("category") or "기타", "report": latest["id"]})
            report_url = topic_url + "?" + _escape(query)
            title = _escape(latest["title"])
            source = _escape(latest.get("source") or "원문 자료")
            date = _escape((latest.get("published_at") or latest.get("first_seen_at") or "")[:10])
            description = "최근 자료 · %s · %s" % (source, date)
        else:
            report_url, title = topic_url, "등록된 자료가 아직 없습니다"
            description = "수집 자료 확인 전"
        rows.append('''<article class="topic-row">
          <div class="topic-label"><a href="%s">%s</a><span>자료실</span></div>
          <div><p class="topic-description">%s</p><a class="topic-title" href="%s">%s</a>
          <p class="source-note">수집 기록 · 상세 분석 전</p></div>
          <a class="row-arrow" href="%s" aria-label="%s 자료 읽기">↗</a>
        </article>''' % (topic_url, _escape(topic["name"]), description, report_url,
                       title, report_url, _escape(topic["name"])))
    return "".join(rows) or '<p class="muted">최근 자료는 분야별 자료실에 연결됩니다.</p>'


def _chart_rows():
    rows = []
    for index, (label, size, total) in enumerate(storage_scenarios()):
        width = min(total / 1000 * 100, 100)
        value = "%s MB" % format(total, ",.0f") if total < 1000 else "%.1f GB" % (total / 1000)
        size_label = "%d KB / 건" % size if size < 1000 else "1 MB / 건"
        classes = "storage-fill scenario-%d" % index
        if total > 1000:
            classes += " over-limit"
        rows.append('''<div class="storage-row"><div class="storage-label"><strong>%s</strong><span>%s</span></div>
          <div class="storage-track"><span class="%s" style="width:%.1f%%"></span></div>
          <div class="storage-value">%s%s</div></div>''' % (
            label, size_label, classes, width, value,
            '<small>1 GB 초과</small>' if total > 1000 else ""))
    return "".join(rows)


def build_briefing_preview(output, snapshot):
    destination = Path(output) / "preview"
    destination.mkdir(parents=True, exist_ok=True)
    style = Path(__file__).with_name("briefing_preview.css").read_bytes()
    (destination / "briefing.css").write_bytes(style)
    version = hashlib.sha256(style).hexdigest()[:12]
    replacements = {"__STYLE_VERSION__": version, "__CHECKED_ON__": CHECKED_ON,
                    "__TOPIC_ROWS__": _topic_rows(snapshot), "__CHART_ROWS__": _chart_rows()}
    for page, template in (("index.html", "briefing_preview_home.html"),
                           ("report.html", "briefing_preview_report.html")):
        content = Path(__file__).with_name(template).read_text(encoding="utf-8")
        for key, value in replacements.items():
            content = content.replace(key, value)
        (destination / page).write_text(content, encoding="utf-8")
    return destination
