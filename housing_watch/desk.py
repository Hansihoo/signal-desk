import html
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from .db import all_items, latest_job_items, latest_news_items
from .housing_profile import apply_profile_filter, load_housing_profile
from .news import summarize_news
from .render import ACTIVE_STATUSES
from .timeutil import iso_utc


TAB_LABELS = {
    "summary": "중요 요약",
    "housing": "청약",
    "weekly-news": "주간 빅뉴스",
    "jobs": "이직 공고",
}


def render_desk_html(
    conn,
    output_path="site/desk.html",
    active_tab="summary",
    item_limit=5,
    max_width=645,
    profile_path=None,
    hide_profile_excluded=True,
):
    if active_tab not in TAB_LABELS:
        raise ValueError("unknown desk tab: %s" % active_tab)

    raw_items = all_items(conn)
    profile = load_housing_profile(profile_path)
    items, profile_filter = apply_profile_filter(raw_items, profile, hide_profile_excluded)
    news_items = latest_news_items(conn, max(item_limit * 4, 30))
    job_items = latest_job_items(conn, max(item_limit * 2, 20))
    active = [item for item in items if item.get("status") in ACTIVE_STATUSES]
    top_housing = sorted(active if active else items, key=_priority)[:item_limit]
    summary_items = sorted(items, key=_summary_priority)[:item_limit]
    urgent_count = sum(1 for item in active if _days_until(item.get("deadline_at")) is not None and _days_until(item.get("deadline_at")) <= 14)

    html_text = _page(
        items=items,
        active=active,
        raw_item_count=len(raw_items),
        profile=profile,
        profile_filter=profile_filter,
        news_items=news_items,
        job_items=job_items,
        top_housing=top_housing,
        summary_items=summary_items,
        urgent_count=urgent_count,
        active_tab=active_tab,
        max_width=max_width,
    )
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_text, encoding="utf-8")
    return str(output)


def _page(
    items,
    active,
    raw_item_count,
    profile,
    profile_filter,
    news_items,
    job_items,
    top_housing,
    summary_items,
    urgent_count,
    active_tab,
    max_width,
):
    displayed_news_count = len(_rank_news_for_briefing(news_items, limit=5, politics_limit=2))
    displayed_job_count = len(_rank_jobs_for_briefing(job_items, limit=5))
    nav = "\n".join(_tab_button(key, label, active_tab) for key, label in TAB_LABELS.items())
    summary_panel = _panel(
        "summary",
        active_tab,
        _summary_panel(items, active, news_items, job_items, summary_items, urgent_count, profile_filter),
    )
    housing_panel = _panel(
        "housing",
        active_tab,
        _housing_panel(items, active, top_housing, urgent_count, profile, profile_filter),
    )
    weekly_panel = _panel(
        "weekly-news",
        active_tab,
        _weekly_news_panel(news_items),
    )
    jobs_panel = _panel(
        "jobs",
        active_tab,
        _jobs_panel(job_items),
    )
    filter_label = ""
    if profile:
        filter_label = " · 프로필 제외 %d건" % profile_filter.get("excluded", 0)
    header_summary = "청약 %d/%d건 · 뉴스 %d건 · 이직 %d건 · %s 탭%s" % (
        len(active),
        raw_item_count,
        displayed_news_count,
        displayed_job_count,
        TAB_LABELS[active_tab],
        filter_label,
    )
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Signal Desk</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #111318;
      --muted: #626b7a;
      --faint: #8a94a6;
      --line: #d9dfeb;
      --rule: #222733;
      --bg: #edf1f6;
      --panel: #ffffff;
      --blue: #2457c5;
      --green: #087f5b;
      --amber: #a45f11;
      --red: #a42721;
      --violet: #6441a5;
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
      width: min(100vw, {max_width}px);
      max-width: {max_width}px;
      min-height: 100svh;
      margin: 0 auto;
      padding: 28px 30px 30px;
      background: var(--panel);
      border-left: 1px solid #cfd6e3;
      border-right: 1px solid #cfd6e3;
      overflow: hidden;
    }}
    @media (max-width: 520px) {{
      .frame {{
        padding: 22px 18px 24px;
        border-left: 0;
        border-right: 0;
      }}
      h1 {{
        font-size: 31px;
      }}
      .tab {{
        font-size: 12px;
        padding-left: 4px;
        padding-right: 4px;
      }}
      .metric b {{
        font-size: 24px;
      }}
      .card {{
        padding: 14px 13px 13px;
      }}
      .card h2 {{
        font-size: 16px;
      }}
      .fact {{
        grid-template-columns: 58px 1fr;
        font-size: 12px;
      }}
    }}
    @media (min-width: 700px) {{
      body {{
        padding: 24px 0;
      }}
      .frame {{
        min-height: auto;
        border: 1px solid #cfd6e3;
        border-radius: 8px;
        box-shadow: 0 18px 42px rgba(27, 37, 54, 0.13);
      }}
    }}
    header {{
      padding: 0 0 14px;
      border-bottom: 2px solid var(--rule);
      margin-bottom: 12px;
    }}
    .masthead {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 0;
      align-items: start;
    }}
    .masthead > div:first-child {{
      min-width: 0;
    }}
    .kicker {{
      color: var(--red);
      font-size: 10px;
      font-weight: 900;
      text-transform: uppercase;
    }}
    h1 {{
      margin: 3px 0 0;
      font-size: 38px;
      line-height: 1.06;
      letter-spacing: 0;
    }}
    .issue {{
      display: none;
    }}
    .summary {{
      margin: 10px 0 0;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.5;
      overflow-wrap: anywhere;
      word-break: keep-all;
    }}
    .tabs {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0;
      margin: 0 0 14px;
      border-bottom: 1px solid var(--line);
    }}
    .tab {{
      min-height: 46px;
      padding: 13px 6px 11px;
      border: 0;
      border-bottom: 2px solid transparent;
      border-radius: 0;
      background: transparent;
      color: var(--muted);
      font: inherit;
      font-size: 14px;
      font-weight: 850;
      cursor: pointer;
      white-space: nowrap;
    }}
    .tab.active {{
      border-color: var(--rule);
      color: var(--ink);
    }}
    .panel {{
      display: none;
    }}
    .panel.active {{
      display: block;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin: 0 0 18px;
    }}
    .metric {{
      min-height: 72px;
      padding: 14px 13px 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfe;
    }}
    .metric b {{
      display: block;
      font-size: 30px;
      line-height: 1;
    }}
    .metric span {{
      display: block;
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
      white-space: nowrap;
    }}
    .section-title {{
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 8px;
      align-items: center;
      margin: 0 0 13px;
      font-size: 16px;
      font-weight: 850;
      color: var(--rule);
    }}
    .section-title::after {{
      content: "";
      height: 1px;
      background: var(--line);
    }}
    .card {{
      display: block;
      margin: 0 0 14px;
      padding: 18px 18px 17px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-left: 4px solid var(--line);
      border-radius: 8px;
      color: inherit;
      text-decoration: none;
      overflow: hidden;
    }}
    .card:hover {{
      border-left-color: var(--blue);
    }}
    .card h2 {{
      display: block;
      width: 100%;
      margin: 10px 0 12px;
      font-size: 20px;
      line-height: 1.34;
      font-weight: 850;
      letter-spacing: 0;
      overflow-wrap: anywhere;
      word-break: break-all;
    }}
    .topline {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}
    .badge {{
      display: inline-block;
      padding: 2px 0;
      border-radius: 0;
      font-size: 12px;
      font-weight: 850;
      white-space: nowrap;
    }}
    .badge.blue {{ color: var(--blue); }}
    .badge.green {{ color: var(--green); }}
    .badge.amber {{ color: var(--amber); }}
    .badge.gray {{ color: var(--faint); }}
    .badge.violet {{ color: var(--violet); }}
    .badge + .badge::before,
    .badge + .dday::before,
    .dday + .badge::before {{
      content: "/";
      color: var(--line);
      margin: 0 6px 0 2px;
      font-weight: 700;
    }}
    .dday {{
      color: var(--amber);
      font-size: 13px;
      font-weight: 850;
      white-space: nowrap;
    }}
    .facts {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 7px;
      margin-top: 12px;
    }}
    .fact {{
      display: grid;
      grid-template-columns: 74px 1fr;
      gap: 12px;
      color: var(--ink);
      font-size: 13.5px;
      line-height: 1.42;
      overflow-wrap: anywhere;
      word-break: break-all;
    }}
    .fact b {{
      color: var(--muted);
      font-weight: 750;
    }}
    .job-fact {{
      grid-template-columns: 74px 1fr;
    }}
    .card.housing {{
      border-left-color: #b8c7e8;
    }}
    .card.housing:hover {{
      border-left-color: var(--blue);
    }}
    .housing-visual {{
      display: grid;
      grid-template-columns: 1.35fr 1fr 1fr;
      gap: 9px;
      margin: 12px 0 14px;
      padding: 10px;
      border: 1px solid #dde5f0;
      border-radius: 8px;
      background: #f7f9fc;
    }}
    .visual-tile {{
      min-height: 74px;
      padding: 11px 12px;
      border: 1px solid #dce4ef;
      border-radius: 6px;
      background: #ffffff;
      overflow: hidden;
    }}
    .visual-tile b {{
      display: block;
      margin-bottom: 7px;
      color: var(--muted);
      font-size: 11.5px;
      font-weight: 800;
    }}
    .visual-tile span {{
      display: block;
      color: var(--ink);
      font-size: 14px;
      font-weight: 850;
      line-height: 1.34;
      overflow-wrap: anywhere;
      word-break: keep-all;
    }}
    .visual-tile.price {{
      grid-column: span 3;
      min-height: 54px;
    }}
    .housing-facts {{
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px 16px;
    }}
    .housing-facts .fact {{
      grid-template-columns: 64px 1fr;
    }}
    .fact.wide {{
      grid-column: 1 / -1;
    }}
    @media (max-width: 560px) {{
      .housing-visual,
      .housing-facts {{
        grid-template-columns: 1fr;
      }}
      .visual-tile.price,
      .fact.wide {{
        grid-column: auto;
      }}
    }}
    .card.job {{
      border-left-color: #b8d9cc;
    }}
    .card.job:hover {{
      border-left-color: var(--green);
    }}
    .why {{
      margin: 10px 0 0;
      padding: 11px 12px;
      border-radius: 6px;
      background: #f5f7fa;
      color: var(--ink);
      font-size: 13px;
      line-height: 1.5;
      overflow-wrap: anywhere;
    }}
    .meta {{
      margin-top: 11px;
      color: var(--muted);
      font-size: 12.5px;
      line-height: 1.5;
      overflow-wrap: anywhere;
    }}
    .empty {{
      margin: 0;
      padding: 14px 12px;
      background: transparent;
      border: 1px dashed #b8c3d4;
      border-radius: 8px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }}
    footer {{
      margin-top: 14px;
      padding-top: 10px;
      border-top: 1px solid var(--line);
      color: var(--muted);
      font-size: 10.5px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }}
  </style>
</head>
<body>
  <main class="frame">
    <header>
      <div class="masthead">
        <div>
          <div class="kicker">Signal Desk Brief</div>
          <h1>오늘 볼 소식</h1>
        </div>
        <div class="issue">MOBILE<br>NOTE</div>
      </div>
      <p class="summary">{html.escape(header_summary)}</p>
    </header>
    <nav class="tabs" aria-label="소식 탭">
      {nav}
    </nav>
    {summary_panel}
    {housing_panel}
    {weekly_panel}
    {jobs_panel}
    <footer>생성시각: {html.escape(iso_utc())}</footer>
  </main>
  <script>
    function showTab(name) {{
      document.querySelectorAll("[data-panel]").forEach(function(panel) {{
        panel.classList.toggle("active", panel.getAttribute("data-panel") === name);
      }});
      document.querySelectorAll("[data-tab]").forEach(function(tab) {{
        var selected = tab.getAttribute("data-tab") === name;
        tab.classList.toggle("active", selected);
        tab.setAttribute("aria-selected", selected ? "true" : "false");
      }});
    }}
    document.querySelectorAll("[data-tab]").forEach(function(tab) {{
      tab.addEventListener("click", function() {{
        showTab(tab.getAttribute("data-tab"));
      }});
    }});
  </script>
</body>
</html>
"""


def _tab_button(key, label, active_tab):
    selected = key == active_tab
    classes = "tab active" if selected else "tab"
    return (
        '<button class="%s" type="button" data-tab="%s" aria-controls="panel-%s" aria-selected="%s">%s</button>'
        % (
            classes,
            html.escape(key, quote=True),
            html.escape(key, quote=True),
            "true" if selected else "false",
            html.escape(label),
        )
    )


def _panel(key, active_tab, content):
    classes = "panel active" if key == active_tab else "panel"
    return '<section id="panel-%s" class="%s" data-panel="%s">%s</section>' % (
        html.escape(key, quote=True),
        classes,
        html.escape(key, quote=True),
        content,
    )


def _summary_panel(items, active, news_items, job_items, summary_items, urgent_count, profile_filter):
    ranked_news = _rank_news_for_briefing(news_items, limit=3, politics_limit=1)
    ranked_jobs = _rank_jobs_for_briefing(job_items, limit=2)
    selected_jobs = ranked_jobs[: min(2, len(ranked_jobs))]
    selected_news = ranked_news[: min(2, max(0, 5 - len(selected_jobs)), len(ranked_news))]
    remaining = max(0, 5 - len(selected_jobs) - len(selected_news))
    excluded_count = profile_filter.get("excluded", 0)
    if profile_filter.get("decisions"):
        third_value = excluded_count
        third_label = "프로필 제외"
    else:
        third_value = len(job_items)
        third_label = "이직공고"
    cards = "\n".join(
        [_job_card(item, compact=True) for item in selected_jobs]
        + [_news_card(item, compact=True) for item in selected_news]
        + [_summary_card(item) for item in summary_items[:remaining]]
    )
    return """<div class="metrics">
  <div class="metric"><b>{total}</b><span>전체 신호</span></div>
  <div class="metric"><b>{active_count}</b><span>진행중</span></div>
  <div class="metric"><b>{third_value}</b><span>{third_label}</span></div>
</div>
<div class="section-title">중요한 것만</div>
{cards}""".format(
        total=len(items) + len(selected_news) + len(job_items),
        active_count=len(active),
        third_value=third_value,
        third_label=html.escape(third_label),
        cards=cards or '<p class="empty">아직 요약할 소식이 없습니다.</p>',
    )


def _housing_panel(items, active, top_housing, urgent_count, profile, profile_filter):
    cards = "\n".join(_housing_card(item) for item in top_housing)
    nearest = _nearest_deadline(active)
    excluded_count = profile_filter.get("excluded", 0)
    third_value = excluded_count if profile else urgent_count
    third_label = "프로필 제외" if profile else "14일내 마감"
    filter_note = ""
    if profile:
        filter_note = '<div class="why"><b>프로필 필터</b><br>%s 기준으로 명확히 어려운 공고 %d건을 숨겼습니다. 무주택 여부와 공고별 산정은 원문 확인이 필요합니다.</div>' % (
            "로컬 프로필",
            excluded_count,
        )
    return """<div class="metrics">
  <div class="metric"><b>{total}</b><span>청약 공고</span></div>
  <div class="metric"><b>{active_count}</b><span>진행중</span></div>
  <div class="metric"><b>{third_value}</b><span>{third_label}</span></div>
</div>
<div class="section-title">서울/경기 청약</div>
{filter_note}
{cards}
<div class="meta">가장 가까운 마감: {nearest}</div>""".format(
        total=len(items),
        active_count=len(active),
        third_value=third_value,
        third_label=html.escape(third_label),
        filter_note=filter_note,
        cards=cards or '<p class="empty">프로필 기준으로 남은 청약 공고가 없습니다. 제외 기준을 보려면 --show-profile-excluded 옵션으로 다시 생성하세요.</p>',
        nearest=html.escape(nearest or "-"),
    )


def _weekly_news_panel(news_items):
    visible_items = _rank_news_for_briefing(news_items, limit=5, politics_limit=2)
    cards = "\n".join(_news_card(item) for item in visible_items)
    categories = sorted({item.get("category") or "종합" for item in visible_items})
    politics_count = sum(1 for item in visible_items if (item.get("category") or "") == "정치")
    return """<div class="metrics">
  <div class="metric"><b>{shown}</b><span>표시 뉴스</span></div>
  <div class="metric"><b>{politics_count}</b><span>정치 최대2</span></div>
  <div class="metric"><b>7일</b><span>기준 기간</span></div>
</div>
<div class="section-title">주간 빅뉴스</div>
{cards}
<div class="meta">분야: {categories}</div>""".format(
        shown=len(visible_items),
        politics_count=politics_count,
        cards=cards or '<p class="empty">아직 수집된 주간 빅뉴스가 없습니다. 기준: 최근 7일, 경제/정치/사회/문화/연예/기술.</p>',
        categories=html.escape(", ".join(categories) if categories else "-"),
    )


def _jobs_panel(job_items):
    visible_items = _rank_jobs_for_briefing(job_items, limit=5)
    cards = "\n".join(_job_card(item) for item in visible_items)
    urgent_count = sum(1 for item in visible_items if _is_urgent_job(item))
    salary_count = sum(1 for item in visible_items if item.get("salary_10y"))
    return """<div class="metrics">
  <div class="metric"><b>{shown}</b><span>표시 공고</span></div>
  <div class="metric"><b>{urgent_count}</b><span>14일내 마감</span></div>
  <div class="metric"><b>{salary_count}</b><span>연봉 조사</span></div>
</div>
<div class="section-title">경력 이직 공고</div>
{cards}
<div class="meta">범위: 중견기업 이상, 경력직, Theo 프로필과 가까운 C++/엔진/오피스/데스크톱 개발 중심.</div>""".format(
        shown=len(visible_items),
        urgent_count=urgent_count,
        salary_count=salary_count,
        cards=cards or '<p class="empty">아직 수집된 이직 공고가 없습니다. `jobs --input`으로 정규화 JSON을 넣으면 이 탭에 표시됩니다.</p>',
    )


def _rank_news_for_briefing(news_items, limit, politics_limit=2):
    non_politics = [item for item in news_items if (item.get("category") or "") != "정치"]
    politics = [item for item in news_items if (item.get("category") or "") == "정치"][:politics_limit]
    ranked = non_politics[:limit]
    remaining = limit - len(ranked)
    if remaining > 0:
        ranked.extend(politics[:remaining])
    return ranked


def _rank_jobs_for_briefing(job_items, limit):
    return sorted(job_items, key=_job_priority)[:limit]


def _news_card(item, compact=False):
    title = item.get("title_ko") or item.get("title") or ""
    category = item.get("category") or "종합"
    summary = _news_summary(item, title, category)
    published = _short_date(item.get("published_at") or "")
    date_badge = '<span class="badge gray">%s</span>' % html.escape(published) if published else ""
    return """<a class="card" href="{url}">
  <div class="topline"><span class="badge blue">{category}</span>{date_badge}</div>
  <h2>{title}</h2>
  <div class="why"><b>요약</b><br>{summary}</div>
</a>""".format(
        url=html.escape(item.get("url") or "#", quote=True),
        category=html.escape(category),
        date_badge=date_badge,
        title=html.escape(title),
        summary=html.escape(summary),
    )


def _job_card(item, compact=False):
    deadline = _job_deadline_label(item.get("deadline_at"))
    if compact:
        facts = """
    <div class="fact job-fact"><b>회사명</b><span>{company}</span></div>
    <div class="fact job-fact"><b>공고명</b><span>{posting}</span></div>
    <div class="fact job-fact"><b>하는일</b><span>{work}</span></div>
    <div class="fact job-fact"><b>지역</b><span>{location}</span></div>
    <div class="fact job-fact"><b>10년차</b><span>{salary}</span></div>"""
    else:
        facts = """
    <div class="fact job-fact"><b>회사명</b><span>{company}</span></div>
    <div class="fact job-fact"><b>공고명</b><span>{posting}</span></div>
    <div class="fact job-fact"><b>하는일</b><span>{work}</span></div>
    <div class="fact job-fact"><b>자격요건</b><span>{requirements}</span></div>
    <div class="fact job-fact"><b>우대사항</b><span>{preferred}</span></div>
    <div class="fact job-fact"><b>지역</b><span>{location}</span></div>
    <div class="fact job-fact"><b>10년차</b><span>{salary}</span></div>
    <div class="fact job-fact"><b>마감일</b><span>{deadline}</span></div>"""
    return """<a class="card job" href="{url}">
  <div class="topline"><span class="badge green">경력</span><span class="badge gray">{company_size}</span><span class="dday">{dday}</span></div>
  <h2>{title}</h2>
  <div class="facts">{facts}
  </div>
  <div class="meta">링크: {link}</div>
</a>""".format(
        url=html.escape(item.get("url") or "#", quote=True),
        company_size=html.escape(_short_value(item.get("company_size") or "중견/대기업", 18)),
        dday=html.escape(deadline),
        title=html.escape(item.get("posting_title") or ""),
        facts=facts.format(
            company=html.escape(_short_value(item.get("company_name") or "-", 42)),
            posting=html.escape(_short_value(item.get("posting_title") or "-", 82)),
            work=html.escape(_short_value(item.get("work_summary") or "확인 필요", 82)),
            requirements=html.escape(_short_value(item.get("requirements") or "확인 필요", 88)),
            preferred=html.escape(_short_value(item.get("preferred") or "확인 필요", 76)),
            location=html.escape(_short_value(item.get("location") or "확인 필요", 48)),
            salary=html.escape(_short_value(item.get("salary_10y") or "별도 조사 필요", 58)),
            deadline=html.escape(item.get("deadline_at") or "마감일 확인"),
        ),
        link=html.escape(_link_label(item.get("url") or "")),
    )


def _summary_card(item):
    title = item.get("title") or ""
    status = item.get("status") or "-"
    dday = _deadline_label(item.get("deadline_at"))
    href = item.get("url") or "#"
    profile_note = _profile_note(item)
    return """<a class="card" href="{url}">
  <div class="topline"><span class="badge violet">청약</span><span class="badge {badge_color}">{status}</span><span class="dday">{dday}</span></div>
  <h2>{title}</h2>
  <div class="facts">
    <div class="fact"><b>지역</b><span>{region}</span></div>
    <div class="fact"><b>주소</b><span>{address}</span></div>
    <div class="fact"><b>가격</b><span>{price}</span></div>
    {profile_note}
  </div>
  <div class="why"><b>왜 중요:</b> {reason}</div>
</a>""".format(
        url=html.escape(href, quote=True),
        badge_color="green" if status in ACTIVE_STATUSES else "gray",
        status=html.escape(status),
        dday=html.escape(dday),
        title=html.escape(title),
        region=html.escape(item.get("region") or "-"),
        address=html.escape(_short_value(item.get("address") or "원문/PDF 확인", 64)),
        price=html.escape(_price_label(item)),
        profile_note=profile_note,
        reason=html.escape(_importance_reason(item)),
    )


def _housing_card(item):
    status = item.get("status") or "-"
    dday = _deadline_label(item.get("deadline_at"))
    profile_note = _profile_note(item, wide=True)
    return """<a class="card housing" href="{url}">
  <div class="topline"><span class="badge {badge_color}">{status}</span><span class="dday">{dday}</span></div>
  <h2>{title}</h2>
  <div class="housing-visual" aria-label="청약 핵심 스냅샷">
    <div class="visual-tile"><b>위치</b><span>{address}</span></div>
    <div class="visual-tile"><b>면적</b><span>{area}</span></div>
    <div class="visual-tile"><b>공급</b><span>{supply}</span></div>
    <div class="visual-tile price"><b>가격</b><span>{price}</span></div>
  </div>
  <div class="facts housing-facts">
    <div class="fact"><b>기관</b><span>{agency}</span></div>
    <div class="fact"><b>유형</b><span>{category}</span></div>
    <div class="fact"><b>지역</b><span>{region}</span></div>
    <div class="fact"><b>일정</b><span>{schedule}</span></div>
    <div class="fact wide"><b>조건</b><span>{eligibility}</span></div>
    {profile_note}
  </div>
  <div class="why"><b>확인 포인트</b><br>{review_note}</div>
  <div class="meta">공식 링크: {link}</div>
</a>""".format(
        url=html.escape(item.get("url") or "#", quote=True),
        badge_color="green" if status in ACTIVE_STATUSES else "gray",
        status=html.escape(status),
        dday=html.escape(dday),
        title=html.escape(item.get("title") or ""),
        address=html.escape(_short_value(item.get("address") or item.get("region") or "원문 확인", 96)),
        area=html.escape(_short_value(_area_label(item), 58)),
        supply=html.escape(_short_value(item.get("supply_units") or "원문 확인", 52)),
        price=html.escape(_short_value(_price_label(item), 96)),
        eligibility=html.escape(_short_value(item.get("eligibility") or "원문 확인", 130)),
        profile_note=profile_note,
        agency=html.escape(item.get("agency") or "-"),
        category=html.escape(item.get("category") or "-"),
        region=html.escape(item.get("region") or "-"),
        schedule=html.escape(_schedule_label(item)),
        review_note=html.escape(_housing_review_note(item)),
        link=html.escape(_link_label(item.get("url") or "")),
    )


def _profile_note(item, wide=False):
    label = item.get("_profile_label")
    if not label:
        return ""
    reason = item.get("_profile_reason") or label
    class_name = "fact wide" if wide else "fact"
    return '<div class="%s"><b>프로필</b><span>%s</span></div>' % (
        class_name,
        html.escape(_short_value(reason, 150 if wide else 92)),
    )


def _housing_review_note(item):
    notes = []
    price = _price_label(item)
    if "원문" in price:
        notes.append("보증금/월세/분양가는 첨부 공고문에서 확인")
    if not item.get("application_period"):
        notes.append("접수 시작·마감 시간은 원문에서 확인")
    if item.get("_profile_label"):
        notes.append("무주택 여부와 공고별 소득·자산 산정은 별도 확인")
    days = _days_until(item.get("deadline_at"))
    if days is not None and 0 <= days <= 14:
        notes.append("마감이 14일 이내라 우선 검토")
    if not notes:
        notes.append("주소, 면적, 공급, 조건을 원문과 대조")
    return " · ".join(notes)


def _priority(item):
    active_rank = 0 if item.get("status") in ACTIVE_STATUSES else 1
    region_rank = _region_rank(item.get("region"))
    deadline = item.get("deadline_at") or "9999-99-99"
    return (active_rank, region_rank, deadline, -(item.get("importance") or 0), -(item.get("id") or 0))


def _job_priority(item):
    days = _days_until(item.get("deadline_at"))
    if days is None:
        deadline_rank = 9999
    elif days < 0:
        deadline_rank = 9998
    else:
        deadline_rank = days
    return (deadline_rank, -(item.get("fit_score") or 0), -(item.get("id") or 0))


def _summary_priority(item):
    active_rank = 0 if item.get("status") in ACTIVE_STATUSES else 1
    urgent_rank = _days_until(item.get("deadline_at"))
    if urgent_rank is None or urgent_rank < 0:
        urgent_rank = 9999
    region_rank = _region_rank(item.get("region"))
    return (active_rank, urgent_rank, region_rank, -(item.get("importance") or 0), -(item.get("id") or 0))


def _region_rank(region):
    value = region or ""
    if "서울" in value:
        return 0
    if "경기" in value:
        return 1
    return 2


def _days_until(value):
    if not value:
        return None
    try:
        deadline = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (deadline - datetime.now().date()).days


def _deadline_label(value):
    days = _days_until(value)
    if days is None:
        return "마감일 확인"
    if days < 0:
        return "마감"
    if days == 0:
        return "오늘 마감"
    return "D-%d" % days


def _job_deadline_label(value):
    days = _days_until(value)
    if days is None:
        return value or "마감일 확인"
    if days < 0:
        return "마감"
    if days == 0:
        return "오늘 마감"
    return "D-%d" % days


def _is_urgent_job(item):
    days = _days_until(item.get("deadline_at"))
    return days is not None and 0 <= days <= 14


def _nearest_deadline(items):
    dated = [item.get("deadline_at") for item in items if item.get("deadline_at")]
    return sorted(dated)[0] if dated else ""


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


def _schedule_label(item):
    if item.get("application_period"):
        return "접수 %s" % _short_value(item["application_period"], 70)
    return "게시 %s · 마감 %s" % (item.get("published_at") or "-", item.get("deadline_at") or "-")


def _short_date(value):
    if not value:
        return ""
    if "T" in value:
        return value.split("T", 1)[0]
    if " " in value:
        return value.split(" ", 1)[0]
    return value[:10]


def _link_label(value):
    if not value:
        return "-"
    host = urlparse(value).netloc
    return host or value


def _news_summary(item, title, category):
    summary = item.get("summary_ko") or ""
    old_patterns = ["상위 노출 뉴스입니다", "후속 확인이 필요합니다", "원문 출처를 열어"]
    if not summary or any(pattern in summary for pattern in old_patterns):
        return summarize_news(title, category, item.get("source_name") or "", item.get("source_id") or "")
    return summary


def _importance_reason(item):
    pieces = []
    if item.get("status") in ACTIVE_STATUSES:
        pieces.append("현재 신청/공고 상태")
    days = _days_until(item.get("deadline_at"))
    if days is not None and 0 <= days <= 14:
        pieces.append("마감이 14일 이내")
    region = item.get("region") or ""
    if "서울" in region:
        pieces.append("관심 지역 서울")
    elif "경기" in region:
        pieces.append("관심 지역 경기")
    if item.get("importance"):
        pieces.append("관심 키워드 점수 %s" % item["importance"])
    return ", ".join(pieces) if pieces else "최근 수집된 관심 범위 공고"


def _short_value(value, max_len):
    value = value or ""
    if len(value) <= max_len:
        return value
    return value[: max_len - 1].rstrip() + "…"
