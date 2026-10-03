import html
import json
from pathlib import Path

from .ai_news import filter_recent_ai_items
from .db import latest_ai_news_items
from .timeutil import iso_utc


PAGE_DEFINITIONS = [
    ("모델/플랫폼", ["LLM 모델", "API/플랫폼"]),
    ("개발/오픈소스", ["AI 개발", "오픈소스"]),
    ("연구/흐름", ["연구", "안전", "시장/정책"]),
]


def render_ai_news_html(conn, output_path="site/ai-news.html", per_page=6, max_width=645, active_page=1, days=None):
    per_page = max(1, int(per_page or 1))
    active_page = min(3, max(1, int(active_page or 1)))
    items = latest_ai_news_items(conn, limit=max(per_page * 8, 60))
    if days:
        items = filter_recent_ai_items(items, days=days)
    pages = build_ai_news_pages(items, per_page)
    html_text = _html_page(pages, per_page, max_width, active_page, days)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_text, encoding="utf-8")
    return str(output)


def format_ai_issue_summary(conn, limit=18, days=7):
    limit = max(1, int(limit or 1))
    days = max(1, int(days or 1))
    items = latest_ai_news_items(conn, limit=max(limit * 3, 60))
    items = filter_recent_ai_items(items, days=days)[:limit]
    lines = ["최근 %d일 AI 이슈 %d건" % (days, len(items))]
    assigned = set()
    for page_index, (title, categories) in enumerate(PAGE_DEFINITIONS, start=1):
        selected = []
        for item_index, item in enumerate(items):
            if item_index in assigned:
                continue
            if item.get("category") in categories:
                selected.append(item)
                assigned.add(item_index)
        if not selected:
            continue
        lines.append("")
        lines.append("%d. %s" % (page_index, title))
        for item in selected:
            lines.append(
                "- [%s] %s - %s"
                % (
                    item.get("category") or "AI",
                    item.get("title_ko") or item.get("title") or "",
                    _short_text(item.get("summary_ko") or "", 120),
                )
            )
    leftovers = [item for item_index, item in enumerate(items) if item_index not in assigned]
    if leftovers:
        lines.append("")
        lines.append("기타")
        for item in leftovers:
            lines.append(
                "- [%s] %s - %s"
                % (
                    item.get("category") or "AI",
                    item.get("title_ko") or item.get("title") or "",
                    _short_text(item.get("summary_ko") or "", 120),
                )
            )
    return "\n".join(lines)


def build_ai_news_pages(items, per_page=6):
    enriched = [_enrich_item(item) for item in items]
    assigned = set()
    pages = []
    for page_index, (title, categories) in enumerate(PAGE_DEFINITIONS, start=1):
        selected = []
        for item_index, item in enumerate(enriched):
            if item_index in assigned:
                continue
            if item.get("category") in categories:
                selected.append(item)
                assigned.add(item_index)
            if len(selected) >= per_page:
                break
        pages.append({"number": page_index, "title": title, "categories": categories, "items": selected})

    for page in pages:
        if len(page["items"]) >= per_page:
            continue
        for item_index, item in enumerate(enriched):
            if item_index in assigned:
                continue
            page["items"].append(item)
            assigned.add(item_index)
            if len(page["items"]) >= per_page:
                break
    return pages


def _html_page(pages, per_page, max_width, active_page, days=None):
    page_buttons = "\n".join(_page_button(page, active_page) for page in pages)
    page_sections = "\n".join(_page_section(page, active_page) for page in pages)
    total = sum(len(page["items"]) for page in pages)
    generated_at = iso_utc()
    return """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Developer Brief</title>
  <style>
    :root {{
      --ink: #101828;
      --muted: #667085;
      --bg: #f5f7fb;
      --panel: #ffffff;
      --line: #d8e0ea;
      --blue: #1d4ed8;
      --green: #047857;
      --amber: #b45309;
      --red: #b42318;
      --chip: #eef4ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans KR", sans-serif;
      letter-spacing: 0;
    }}
    .frame {{
      width: min(100%, {max_width}px);
      max-width: {max_width}px;
      min-height: 100vh;
      margin: 0;
      padding: 18px 16px 22px;
      overflow: hidden;
    }}
    header {{
      padding: 2px 0 14px;
    }}
    .kicker {{
      color: var(--blue);
      font-size: 12px;
      font-weight: 850;
    }}
    h1 {{
      margin: 5px 0 8px;
      font-size: 27px;
      line-height: 1.16;
      letter-spacing: 0;
    }}
    .lead {{
      margin: 0;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
      overflow-wrap: anywhere;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin: 14px 0 12px;
    }}
    .metric {{
      min-height: 58px;
      padding: 10px 8px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .metric b {{
      display: block;
      font-size: 21px;
      line-height: 1;
    }}
    .metric span {{
      display: block;
      margin-top: 6px;
      color: var(--muted);
      font-size: 11px;
      white-space: nowrap;
    }}
    .page-nav {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 7px;
      margin: 0 0 13px;
    }}
    .page-nav button {{
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--muted);
      font: inherit;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .page-nav button.is-active {{
      border-color: #b7cdfc;
      background: var(--chip);
      color: var(--blue);
    }}
    .page {{
      display: none;
    }}
    .page.is-active {{
      display: block;
    }}
    .page-title {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 8px;
      margin: 0 0 9px;
    }}
    .page-title h2 {{
      margin: 0;
      font-size: 16px;
      line-height: 1.3;
      letter-spacing: 0;
    }}
    .page-title span {{
      color: var(--muted);
      font-size: 11px;
      white-space: nowrap;
    }}
    details.news-card {{
      margin: 0 0 9px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }}
    details.news-card[open] {{
      border-color: #b7cdfc;
    }}
    summary {{
      display: block;
      padding: 12px;
      cursor: pointer;
      list-style: none;
    }}
    summary::-webkit-details-marker {{
      display: none;
    }}
    .headline-row {{
      display: flex;
      align-items: center;
      gap: 7px;
      margin-bottom: 8px;
    }}
    .category {{
      display: inline-block;
      max-width: 120px;
      padding: 4px 7px;
      border-radius: 999px;
      background: #ecfdf3;
      color: var(--green);
      font-size: 11px;
      font-weight: 850;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .source {{
      color: var(--muted);
      font-size: 11px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    h3 {{
      margin: 0;
      font-size: 15px;
      line-height: 1.35;
      letter-spacing: 0;
      overflow-wrap: anywhere;
      word-break: normal;
    }}
    .summary-text {{
      margin: 8px 0 0;
      color: #344054;
      font-size: 12px;
      line-height: 1.48;
      overflow-wrap: anywhere;
    }}
    .detail {{
      padding: 0 12px 12px;
      border-top: 1px solid #edf2f7;
    }}
    .detail-row {{
      display: grid;
      grid-template-columns: 74px 1fr;
      gap: 9px;
      padding-top: 10px;
      font-size: 12px;
      line-height: 1.45;
    }}
    .detail-row b {{
      color: var(--muted);
      font-weight: 800;
    }}
    .detail-row span {{
      overflow-wrap: anywhere;
    }}
    .source-link {{
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      margin-top: 11px;
      color: var(--blue);
      font-size: 12px;
      font-weight: 850;
      text-decoration: none;
    }}
    .empty {{
      margin: 0;
      padding: 14px 12px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }}
    footer {{
      margin-top: 12px;
      color: var(--muted);
      font-size: 10px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }}
  </style>
</head>
<body>
  <main class="frame">
    <header>
      <div class="kicker">Signal Desk</div>
      <h1>AI Developer Brief</h1>
      <p class="lead">유명 LLM, AI 개발 도구, 오픈소스 릴리스, 연구 흐름을 개발자 관점으로 압축했습니다.</p>
    </header>
    <div class="metrics">
      <div class="metric"><b>3</b><span>페이지</span></div>
      <div class="metric"><b>{per_page}</b><span>페이지당</span></div>
      <div class="metric"><b>{total}</b><span>표시 항목</span></div>
    </div>
    <nav class="page-nav" aria-label="AI news pages">
      {page_buttons}
    </nav>
    {page_sections}
    <footer>{range_label}<br>생성시각: {generated_at}</footer>
  </main>
  <script>
    (function () {{
      var buttons = document.querySelectorAll("[data-page-button]");
      var pages = document.querySelectorAll("[data-page]");
      function activate(page) {{
        buttons.forEach(function (button) {{
          var selected = button.getAttribute("data-page-button") === page;
          button.classList.toggle("is-active", selected);
          button.setAttribute("aria-selected", selected ? "true" : "false");
        }});
        pages.forEach(function (section) {{
          section.classList.toggle("is-active", section.getAttribute("data-page") === page);
        }});
      }}
      buttons.forEach(function (button) {{
        button.addEventListener("click", function () {{
          activate(button.getAttribute("data-page-button"));
        }});
      }});
    }})();
  </script>
</body>
</html>
""".format(
        max_width=max_width,
        per_page=per_page,
        total=total,
        page_buttons=page_buttons,
        page_sections=page_sections,
        range_label=html.escape("범위: 최근 %d일" % days if days else "범위: 저장된 AI 이슈"),
        generated_at=html.escape(generated_at),
    )


def _page_button(page, active_page):
    active = page["number"] == active_page
    return '<button class="%s" type="button" data-page-button="%d" aria-selected="%s">%d. %s</button>' % (
        "is-active" if active else "",
        page["number"],
        "true" if active else "false",
        page["number"],
        html.escape(page["title"]),
    )


def _page_section(page, active_page):
    cards = "\n".join(_news_card(item) for item in page["items"])
    if not cards:
        cards = '<p class="empty">아직 이 페이지에 표시할 AI 소식이 없습니다.</p>'
    active = " is-active" if page["number"] == active_page else ""
    return """<section class="page{active}" data-page="{number}">
  <div class="page-title">
    <h2>{title}</h2>
    <span>{count}개</span>
  </div>
  {cards}
</section>""".format(
        active=active,
        number=page["number"],
        title=html.escape(page["title"]),
        count=len(page["items"]),
        cards=cards,
    )


def _news_card(item):
    payload = item.get("_payload", {})
    detail = payload.get("detail") or "원문을 열어 자세한 변경 범위를 확인하세요."
    impact = payload.get("developer_impact") or "개발 흐름과 기술 선택에 참고할 만한 신호입니다."
    action = payload.get("action_needed") or "원문과 관련 릴리스 노트를 확인하세요."
    source = item.get("source_name") or "-"
    date = _date_label(item.get("published_at") or "")
    return """<details class="news-card">
  <summary>
    <div class="headline-row"><span class="category">{category}</span><span class="source">{source} · {date}</span></div>
    <h3>{title}</h3>
    <p class="summary-text">{summary}</p>
  </summary>
  <div class="detail">
    <div class="detail-row"><b>영향</b><span>{impact}</span></div>
    <div class="detail-row"><b>상세</b><span>{detail}</span></div>
    <div class="detail-row"><b>확인</b><span>{action}</span></div>
    <a class="source-link" href="{url}">원문 보기</a>
  </div>
</details>""".format(
        category=html.escape(item.get("category") or "AI"),
        source=html.escape(source),
        date=html.escape(date),
        title=html.escape(item.get("title_ko") or item.get("title") or ""),
        summary=html.escape(item.get("summary_ko") or ""),
        impact=html.escape(impact),
        detail=html.escape(_short_text(detail, 520)),
        action=html.escape(action),
        url=html.escape(item.get("url") or "#", quote=True),
    )


def _enrich_item(item):
    enriched = dict(item)
    try:
        payload = json.loads(item.get("raw_payload") or "{}")
    except (TypeError, ValueError):
        payload = {}
    enriched["_payload"] = payload
    return enriched


def _date_label(value):
    value = value or ""
    if not value:
        return "-"
    return value[:10]


def _short_text(value, max_len):
    value = value or ""
    if len(value) <= max_len:
        return value
    return value[: max_len - 3].rstrip() + "..."
