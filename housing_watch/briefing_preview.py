"""HTML presentation of structured research content; no report facts live here."""

import html
import re
from urllib.parse import urlencode

from .research_topics import public_url


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
        if topic["id"] == "business" and not items:
            continue  # Authored business reports have their own board, not a feed archive.
        topic_url = "../research/%s/index.html" % _escape(topic["id"])
        if items:
            latest = items[0]
            query = urlencode({"section": latest.get("category") or "기타", "report": latest["id"]})
            report_url = topic_url + "?" + _escape(query)
            title = _escape(latest["title"])
            source = _escape(latest.get("source") or "원문 자료")
            date = _escape((latest.get("published_at") or latest.get("first_seen_at") or "")[:10])
            description = "%s · %s" % (source, date)
        else:
            report_url, title = topic_url, "등록된 자료가 아직 없습니다"
            description = ""
        rows.append('''<article class="topic-row">
          <div class="topic-label"><a href="%s">%s</a></div>
          <div><p class="topic-description">%s</p><a class="topic-title" href="%s">%s</a>
          </div><a class="row-arrow" href="%s" aria-label="%s">↗</a>
        </article>''' % (topic_url, _escape(topic["name"]), description, report_url,
                       title, report_url, title))
    return "".join(rows) or '<p class="empty-note">등록된 자료 없음</p>'


def _format_value(value, unit):
    if unit == "MB" and value >= 1000:
        return "%.1f GB" % (value / 1000)
    return "%s %s" % (format(value, ",g"), unit)


def _line_break(text):
    return _escape(text)


def _citations(record, source_numbers):
    return "".join('<a class="citation" href="#ref-%d">[%d]</a>' %
                   (source_numbers[key], source_numbers[key]) for key in record["source_ids"])


def _points(points, source_numbers):
    return "".join("<li><strong>%s</strong> — %s%s</li>" %
                   (_escape(point["label"]), _escape(point["text"]), _citations(point, source_numbers))
                   for point in points)


def _chart(dataset, source_numbers):
    rows = []
    threshold = dataset.get("threshold")
    maximum = max([row["value"] for row in dataset["rows"]] + [threshold["value"] if threshold else 0, 1])
    for index, row in enumerate(dataset["rows"]):
        width = row["value"] / maximum * 100
        value = _format_value(row["value"], dataset["unit"])
        classes = "storage-fill scenario-%d" % (index % 3)
        rows.append('''<div class="storage-row"><div class="storage-label">%s</div>
          <div class="storage-track"><span class="%s" style="width:%.1f%%"></span></div>
          <div class="storage-value">%s</div></div>''' % (
            _escape(row["label"]), classes, width, _escape(value)))
    limit = '<div class="chart-limit"><span>%s %s</span></div>' % (
        _escape(threshold["label"]), _escape(_format_value(threshold["value"], dataset["unit"]))) if threshold else ""
    description = "; ".join("%s: %s" % (row["label"], _format_value(row["value"], dataset["unit"])) for row in dataset["rows"])
    if threshold:
        description += "; %s %s 점선" % (threshold["label"], _format_value(threshold["value"], dataset["unit"]))
    methods = "".join("<p>%s</p>" % _escape(text) for text in dataset["method"])
    caption = "추정" if dataset["kind"] == "estimate" else "자료"
    if dataset["unit"] == "MB":
        caption += " · 십진 단위"
    return '''<figure class="storage-figure%s" style="--threshold-position:%.6f%%">
      <figcaption><h3>%s</h3><span>%s%s</span></figcaption>
      <p class="chart-assumption">%s</p>%s
      <div class="storage-chart" role="img" aria-label="%s">%s</div>
      <div class="chart-scale"><span>0</span><span>%s</span></div>
      <p class="chart-note">%s</p></figure>%s''' % (
        " has-threshold" if threshold else "", threshold["value"] / maximum * 100 if threshold else 0,
        _escape(dataset["title"]), caption, _citations(dataset, source_numbers),
        _escape(" · ".join(dataset["assumptions"])), limit, _escape(description), "".join(rows),
        _escape(_format_value(maximum, dataset["unit"])), _escape(dataset["note"]),
        '<details class="method-note"><summary>산정 근거</summary>%s</details>' % methods if methods else "")


def _table_text(text):
    # Keep short dates/identifiers legible without making long source text
    # unbreakable. Escape every fragment before adding presentation markup.
    parts = re.split(r"(\S*[-·/]\S*)", text)
    return "".join('<span class="table-token">%s</span>' % _escape(part)
                   if index % 2 and len(part) <= 24 else _escape(part)
                   for index, part in enumerate(parts))


def _table(table, source_numbers):
    headers = "".join('<th scope="col">%s</th>' % _escape(text) for text in table["columns"])
    rows = []
    for row in table["rows"]:
        cells = ['<th scope="row">%s</th>' % _table_text(row["values"][0])]
        cells.extend('<td>%s%s</td>' % (_table_text(value), _citations(row, source_numbers)
                     if index == len(row["values"]) - 1 else "")
                     for index, value in enumerate(row["values"][1:], 1))
        rows.append("<tr>%s</tr>" % "".join(cells))
    return '<div class="report-table%s" role="region" aria-label="%s" tabindex="0"><table><caption>%s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody></table><p class="chart-note">%s</p></div>' % (
        " two-column" if len(table["columns"]) == 2 else "", _escape(table["title"]), _escape(table["title"]), headers, "".join(rows), _escape(table["note"]))


def _authored_blocks(blocks, source_numbers, heading_tag="h3"):
    rendered = []
    for block in blocks:
        label = {"fact": "", "example": "가상 예시", "judgment": "검토 의견"}[block["kind"]]
        heading = '<%s>%s%s</%s>' % (heading_tag, _escape(block["title"]),
            ' <span class="learning-kind">%s</span>' % label if label else "", heading_tag)
        if block["type"] == "paragraph":
            body = "".join('<p>%s</p>' % _escape(paragraph) for paragraph in block["text"].split("\n\n"))
        elif block["type"] == "code":
            body = '<pre><code>%s</code></pre>' % _escape(block["text"])
        elif block["type"] == "steps":
            body = '<ol class="learning-steps">%s</ol>' % "".join(
                '<li><strong>%s</strong><p>%s</p></li>' % (_escape(item["label"]), _escape(item["text"]))
                for item in block["items"])
        else:
            body = '<dl class="learning-terms">%s</dl>' % "".join(
                '<div><dt>%s</dt><dd>%s</dd></div>' % (_escape(item["label"]), _escape(item["text"]))
                for item in block["items"])
        cites = _citations(block, source_numbers)
        rendered.append('<div class="learning-block">%s%s%s</div>' % (
            heading, body, '<p class="learning-sources">근거 %s</p>' % cites if cites else ""))
    return "".join(rendered)


def _explanation(chapters, source_numbers):
    if not chapters:
        return ""
    prose = "".join('<section class="explanation-chapter" id="explanation-%s"><h3>%s</h3><p class="explanation-lead">%s</p>%s</section>' % (
        _escape(chapter["id"]), _escape(chapter["title"]), _escape(chapter["lead"]),
        _authored_blocks(chapter["blocks"], source_numbers, "h4")) for chapter in chapters)
    return '<section id="explanation" class="report-section" aria-labelledby="explanation-title"><header class="major"><h2 id="explanation-title">본문</h2></header><div class="report-prose">%s</div></section>' % prose


def _learning(lessons, source_numbers):
    if not lessons:
        return ""
    chapters = []
    for lesson in lessons:
        chapters.append('''<details class="learning-chapter" id="learning-%s">
          <summary><span class="learning-heading">%s</span><span class="learning-toggle" aria-hidden="true"><span class="when-closed">펼치기</span><span class="when-open">접기</span></span><span class="learning-lead">%s</span></summary>
          <div class="learning-body">%s</div></details>''' % (
            _escape(lesson["id"]), _escape(lesson["title"]), _escape(lesson["lead"]), _authored_blocks(lesson["blocks"], source_numbers)))
    return '<section id="learning" class="report-section" aria-labelledby="learning-title"><h2 id="learning-title">해설</h2>%s</section>' % "".join(chapters)


def _report_replacements(report):
    source_numbers = {source["id"]: index for index, source in enumerate(report["references"], 1)}
    metrics = "".join('<p><strong>%s</strong><span>%s%s</span><small>%s</small></p>' % (
        _escape(_format_value(metric["value"], metric["unit"])), _escape(metric["label"]),
        _citations(metric, source_numbers), _escape(metric["qualifier"])) for metric in report["metrics"])
    numeric_values = {_format_value(metric["value"], metric["unit"]) for metric in report["metrics"]}
    numeric_values.update(_format_value(row["value"], dataset["unit"]) for dataset in report["datasets"] for row in dataset["rows"])
    pattern = re.compile("|".join(re.escape(_escape(value)) for value in sorted(numeric_values, key=len, reverse=True))) if numeric_values else None
    highlights = []
    for text in report["highlights"]:
        escaped = _escape(text)
        highlights.append("<li>%s</li>" % (pattern.sub(lambda match: "<strong>%s</strong>" % match.group(), escaped) if pattern else escaped))
    references = "".join('<li id="ref-%d"><span>[%d]</span><div><a href="%s">%s</a><p>%s</p></div></li>' % (
        index, index, _escape(source["url"]), _escape(source["title"]), _escape(source["description"]))
        for index, source in enumerate(report["references"], 1))
    caveats = " ".join(_escape(caveat["text"]) + _citations(caveat, source_numbers) for caveat in report["caveats"])
    return {"__TITLE__": _escape(report["title"]), "__HEADLINE__": _line_break(report["title"]),
            "__DESCRIPTION__": _escape(report["description"]), "__CHECKED_ON_ISO__": report["checked_on"],
            "__CHECKED_ON__": report["checked_on"].replace("-", "."),
            "__TOPIC_NAME__": _escape(report["topic_path"][0]),
            "__CATEGORY__": ' <span>／</span> '.join(_escape(text) for text in report["topic_path"]),
            "__DECK__": _escape(report["deck"]), "__SCOPE__": _escape(report["scope"]),
            "__HIGHLIGHTS__": "".join(highlights), "__SOURCE_NOTE__": _escape(report["source_note"]),
            "__SUMMARY__": _points(report["summary"], source_numbers),
            "__EXPLANATION_LINK__": '<a href="#explanation">본문</a>' if report.get("explanation") else "",
            "__EXPLANATION__": _explanation(report.get("explanation", []), source_numbers),
            "__LEARNING_LINK__": '<a href="#learning">해설</a>' if report.get("learning") else "",
            "__LEARNING__": _learning(report.get("learning", []), source_numbers),
            "__METRICS__": '<div class="limits-row">%s</div>' % metrics if metrics else "",
            "__DATASETS__": "".join(_chart(dataset, source_numbers) for dataset in report["datasets"])
                            + "".join(_table(table, source_numbers) for table in report.get("tables", [])),
            "__RESULT_TITLE__": _line_break(report["result"]["title"]),
            "__RESULT_POINTS__": _points(report["result"]["points"], source_numbers),
            "__REFERENCES__": references, "__CAVEATS__": caveats}


def build_briefing_preview(output, snapshot, report, research_data=None, standalone=True):
    from .editorial import render_editorial
    return render_editorial(output, snapshot, report, research_data, standalone)
