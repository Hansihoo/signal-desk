import html
import os
import subprocess
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path

from .db import all_items
from .housing_profile import apply_profile_filter, load_housing_profile
from .timeutil import iso_utc


ACTIVE_STATUSES = {"모집중", "접수중", "공고중", "정정공고중"}


def render_html(conn, output_path="site/latest.html", item_limit=16):
    items = all_items(conn)
    active = [item for item in items if item.get("status") in ACTIVE_STATUSES]
    top_items = sorted(items, key=_priority)[:item_limit]
    status_counts = Counter(item.get("status") or "상태없음" for item in items)
    region_counts = Counter(item.get("region") or "지역없음" for item in items)

    html_text = _page(items, active, top_items, status_counts, region_counts)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_text, encoding="utf-8")
    return str(output)


def render_brief_html(
    conn,
    output_path="site/brief.html",
    item_limit=5,
    max_width=390,
    profile_path=None,
    hide_profile_excluded=True,
    use_profile=True,
):
    raw_items = all_items(conn)
    profile = load_housing_profile(profile_path) if use_profile else None
    items, profile_filter = apply_profile_filter(raw_items, profile, hide_profile_excluded)
    active = [item for item in items if item.get("status") in ACTIVE_STATUSES]
    source_items = active if active else items
    top_items = sorted(source_items, key=_priority)[:item_limit]
    urgent_count = sum(1 for item in active if _days_until(item.get("deadline_at")) is not None and _days_until(item.get("deadline_at")) <= 14)
    html_text = _brief_page(items, active, top_items, urgent_count, max_width, profile, profile_filter, len(raw_items))
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_text, encoding="utf-8")
    return str(output)


def export_image(html_path="site/latest.html", output_path="reports/latest.png", width=430, height=1200):
    html_file = Path(html_path).resolve()
    output_file = Path(output_path).resolve()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    browser = _find_browser()
    if not browser:
        raise RuntimeError("Edge 또는 Chrome 실행 파일을 찾지 못했습니다.")
    args = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=%d,%d" % (width, height),
        "--screenshot=%s" % str(output_file),
        html_file.as_uri(),
    ]
    if os.name != "nt":
        args[1:1] = ["--no-sandbox", "--disable-dev-shm-usage"]
    subprocess.run(args, check=True)
    return str(output_file)


def _find_browser():
    candidates = [
        os.path.join(os.environ.get("ProgramFiles", ""), "Microsoft", "Edge", "Application", "msedge.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Microsoft", "Edge", "Application", "msedge.exe"),
        os.path.join(os.environ.get("ProgramFiles", ""), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Google", "Chrome", "Application", "chrome.exe"),
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        browser = shutil.which(name)
        if browser:
            return browser
    return None


def _page(items, active, top_items, status_counts, region_counts):
    total = len(items)
    active_count = len(active)
    max_region = max(region_counts.values()) if region_counts else 1
    cards = "\n".join(_item_card(item) for item in top_items)
    regions = "\n".join(_bar(region, count, max_region) for region, count in region_counts.most_common(8))
    statuses = "\n".join(_pill(status, count) for status, count in status_counts.most_common())

    return """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>청약 주택 브리핑</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #17202a;
      --muted: #667085;
      --line: #d9e2ec;
      --paper: #f7fafc;
      --panel: #ffffff;
      --blue: #1d4ed8;
      --green: #047857;
      --amber: #b45309;
      --red: #b42318;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans KR", sans-serif;
      letter-spacing: 0;
    }
    main {
      width: min(100%%, 520px);
      margin: 0 auto;
      padding: 20px 16px 28px;
    }
    header {
      padding: 18px 0 14px;
    }
    .eyebrow {
      color: var(--blue);
      font-weight: 800;
      font-size: 13px;
    }
    h1 {
      margin: 6px 0 8px;
      font-size: 30px;
      line-height: 1.18;
      letter-spacing: 0;
    }
    .sub {
      margin: 0;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.55;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin: 16px 0;
    }
    .stat {
      min-height: 74px;
      padding: 12px 10px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }
    .stat strong {
      display: block;
      font-size: 23px;
      line-height: 1.1;
    }
    .stat span {
      display: block;
      margin-top: 6px;
      color: var(--muted);
      font-size: 12px;
    }
    section {
      margin-top: 18px;
    }
    h2 {
      margin: 0 0 10px;
      font-size: 17px;
      letter-spacing: 0;
    }
    .pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 9px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 999px;
      font-size: 12px;
      color: var(--muted);
    }
    .pill b { color: var(--ink); }
    .bars {
      padding: 12px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }
    .bar-row {
      display: grid;
      grid-template-columns: 72px 1fr 28px;
      gap: 8px;
      align-items: center;
      margin: 8px 0;
      font-size: 12px;
      color: var(--muted);
    }
    .track {
      height: 8px;
      background: #edf2f7;
      border-radius: 999px;
      overflow: hidden;
    }
    .fill {
      height: 100%%;
      background: linear-gradient(90deg, #1d4ed8, #059669);
      border-radius: 999px;
    }
    .card {
      display: block;
      padding: 14px;
      margin-bottom: 10px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      color: inherit;
      text-decoration: none;
      overflow: hidden;
    }
    .card h3 {
      margin: 8px 0 10px;
      font-size: 16px;
      line-height: 1.38;
      letter-spacing: 0;
      overflow-wrap: anywhere;
      word-break: normal;
    }
    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }
    .badge {
      display: inline-block;
      padding: 4px 7px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 800;
      background: #e0ecff;
      color: var(--blue);
    }
    .badge.active {
      background: #dcfce7;
      color: var(--green);
    }
    .badge.closed {
      background: #f2f4f7;
      color: #475467;
    }
    .importance {
      margin-left: 4px;
      color: var(--amber);
      font-weight: 800;
    }
    footer {
      margin-top: 18px;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.5;
    }
  </style>
</head>
<body>
<main>
  <header>
    <div class="eyebrow">Housing Watch</div>
    <h1>청약 주택 브리핑</h1>
    <p class="sub">Codex 질문 대응을 위해 미리 수집한 공식 공고 기반 요약입니다. 신청 전 원문 공고를 확인하세요.</p>
  </header>
  <div class="stats">
    <div class="stat"><strong>%d</strong><span>전체 공고</span></div>
    <div class="stat"><strong>%d</strong><span>모집/접수중</span></div>
    <div class="stat"><strong>%d</strong><span>관심 상위</span></div>
  </div>
  <section>
    <h2>상태</h2>
    <div class="pills">%s</div>
  </section>
  <section>
    <h2>지역 분포</h2>
    <div class="bars">%s</div>
  </section>
  <section>
    <h2>먼저 볼 공고</h2>
    %s
  </section>
  <footer>
    생성시각: %s<br>
    데이터는 로컬 수집본이며, 실제 접수 여부와 조건은 공식 링크 기준으로 확인해야 합니다.
  </footer>
</main>
</body>
</html>
""" % (
        total,
        active_count,
        len(top_items),
        statuses,
        regions,
        cards or "<p class=\"sub\">아직 수집된 공고가 없습니다.</p>",
        html.escape(iso_utc()),
    )


def _brief_page(items, active, top_items, urgent_count, max_width, profile=None, profile_filter=None, raw_item_count=None):
    cards = "\n".join(_brief_card(item) for item in top_items)
    latest_deadline = _nearest_deadline(active)
    profile_filter = profile_filter or {"excluded": 0}
    raw_item_count = raw_item_count if raw_item_count is not None else len(items)
    summary = "공식 공고에서 수집한 현재 확인용 요약입니다. 신청 전 원문 공고를 확인하세요."
    third_value = urgent_count
    third_label = "14일내 마감"
    total_label = "전체"
    if profile:
        third_value = profile_filter.get("excluded", 0)
        third_label = "프로필 제외"
        total_label = "검토 공고"
        summary = "로컬 프로필 기준으로 명확히 어려운 청약을 숨긴 요약입니다. 무주택 여부와 공고별 산정은 원문 확인이 필요합니다."
    return """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>청약 주택 요약</title>
  <style>
    :root {{
      --ink: #111827;
      --muted: #5f6b7a;
      --line: #d7dee8;
      --bg: #f6f8fb;
      --panel: #ffffff;
      --blue: #1d4ed8;
      --green: #047857;
      --amber: #b45309;
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
      margin: 0;
      padding: 16px 14px 18px;
      overflow: hidden;
    }}
    .kicker {{
      color: var(--blue);
      font-size: 12px;
      font-weight: 800;
    }}
    h1 {{
      margin: 4px 0 6px;
      font-size: 25px;
      line-height: 1.18;
      letter-spacing: 0;
    }}
    .summary {{
      margin: 0;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 7px;
      margin: 13px 0 14px;
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
    .section-title {{
      margin: 0 0 8px;
      font-size: 15px;
      font-weight: 850;
    }}
    .notice {{
      display: block;
      margin: 0 0 8px;
      padding: 11px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      color: inherit;
      text-decoration: none;
      overflow: hidden;
    }}
    .topline {{
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 7px;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 7px;
      border-radius: 999px;
      background: #dcfce7;
      color: var(--green);
      font-size: 11px;
      font-weight: 850;
      white-space: nowrap;
    }}
    .dday {{
      color: var(--amber);
      font-size: 12px;
      font-weight: 850;
      white-space: nowrap;
    }}
    h2 {{
      display: block;
      width: 100%;
      margin: 0;
      font-size: 14px;
      line-height: 1.34;
      letter-spacing: 0;
      overflow-wrap: anywhere;
      word-break: break-all;
    }}
    .facts {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 4px;
      margin-top: 8px;
    }}
    .fact {{
      display: grid;
      grid-template-columns: 38px 1fr;
      gap: 6px;
      color: var(--ink);
      font-size: 11px;
      line-height: 1.35;
      overflow-wrap: anywhere;
      word-break: break-all;
    }}
    .fact b {{
      color: var(--muted);
      font-weight: 750;
    }}
    .meta {{
      margin-top: 7px;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }}
    footer {{
      margin-top: 11px;
      color: var(--muted);
      font-size: 10px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }}
  </style>
</head>
<body>
  <main class="frame">
    <div class="kicker">Housing Watch</div>
    <h1>청약 주택 요약</h1>
    <p class="summary">{summary}</p>
    <div class="metrics">
      <div class="metric"><b>{total}</b><span>{total_label}</span></div>
      <div class="metric"><b>{active_count}</b><span>진행중</span></div>
      <div class="metric"><b>{third_value}</b><span>{third_label}</span></div>
    </div>
    <div class="section-title">바로 확인할 공고</div>
    {cards}
    <footer>
      최근 마감: {latest_deadline}<br>
      생성시각: {generated_at}
    </footer>
  </main>
</body>
</html>
""".format(
        max_width=max_width,
        total=len(items),
        total_label=html.escape(total_label),
        summary=html.escape(summary),
        active_count=len(active),
        third_value=third_value,
        third_label=html.escape(third_label),
        cards=cards or '<p class="summary">프로필 기준으로 남은 청약 공고가 없습니다. 제외 기준을 보려면 --show-profile-excluded 옵션으로 다시 생성하세요.</p>',
        latest_deadline=html.escape(latest_deadline or "-"),
        generated_at=html.escape(iso_utc()),
    )


def _brief_card(item):
    status = item.get("status") or "-"
    dday = _deadline_label(item.get("deadline_at"))
    profile_note = _profile_note(item)
    return """<a class="notice" href="{url}">
  <div class="topline"><span class="badge">{status}</span><span class="dday">{dday}</span></div>
  <h2>{title}</h2>
  <div class="facts">
    <div class="fact"><b>주소</b><span>{address}</span></div>
    <div class="fact"><b>면적</b><span>{area}</span></div>
    <div class="fact"><b>공급</b><span>{supply}</span></div>
    <div class="fact"><b>가격</b><span>{price}</span></div>
    <div class="fact"><b>조건</b><span>{eligibility}</span></div>
    {profile_note}
  </div>
  <div class="meta">{agency} · {category} · {region}<br>{schedule}</div>
</a>""".format(
        url=html.escape(item.get("url") or "#", quote=True),
        status=html.escape(status),
        dday=html.escape(dday),
        title=html.escape(item.get("title") or ""),
        address=html.escape(_short_value(item.get("address") or item.get("region") or "원문 확인", 64)),
        area=html.escape(_area_label(item)),
        supply=html.escape(_short_value(item.get("supply_units") or "원문 확인", 64)),
        price=html.escape(_price_label(item)),
        eligibility=html.escape(_short_value(item.get("eligibility") or "원문 확인", 54)),
        profile_note=profile_note,
        agency=html.escape(item.get("agency") or "-"),
        category=html.escape(item.get("category") or "-"),
        region=html.escape(item.get("region") or "-"),
        schedule=html.escape(_schedule_label(item)),
    )


def _profile_note(item):
    label = item.get("_profile_label")
    if not label:
        return ""
    reason = item.get("_profile_reason") or label
    return '<div class="fact"><b>프로필</b><span>%s</span></div>' % html.escape(_short_value(reason, 82))


def _pill(status, count):
    return '<span class="pill"><b>%s</b>%d</span>' % (html.escape(status), count)


def _bar(region, count, max_region):
    width = max(4, int(count / float(max_region) * 100))
    return (
        '<div class="bar-row"><span>%s</span><div class="track"><div class="fill" style="width:%d%%"></div></div><b>%d</b></div>'
        % (html.escape(region), width, count)
    )


def _item_card(item):
    status = item.get("status") or "-"
    badge_class = "active" if status in ACTIVE_STATUSES else "closed"
    return """<a class="card" href="%s">
  <span class="badge %s">%s</span><span class="importance">중요도 %s</span>
  <h3>%s</h3>
  <div class="meta">
    <span>%s</span><span>%s</span><span>%s</span><span>게시 %s</span><span>마감 %s</span>
  </div>
</a>""" % (
        html.escape(item.get("url") or "#", quote=True),
        badge_class,
        html.escape(status),
        html.escape(str(item.get("importance") or 0)),
        html.escape(item.get("title") or ""),
        html.escape(item.get("agency") or "-"),
        html.escape(item.get("category") or "-"),
        html.escape(item.get("region") or "-"),
        html.escape(item.get("published_at") or "-"),
        html.escape(item.get("deadline_at") or "-"),
    )


def _priority(item):
    active_rank = 0 if item.get("status") in ACTIVE_STATUSES else 1
    region_rank = _region_rank(item.get("region"))
    deadline = item.get("deadline_at") or "9999-99-99"
    return (active_rank, region_rank, -(item.get("importance") or 0), deadline, -(item.get("id") or 0))


def _region_rank(region):
    region = region or ""
    if "서울" in region:
        return 0
    if "경기" in region:
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


def _short_value(value, max_len):
    value = value or ""
    if len(value) <= max_len:
        return value
    return value[: max_len - 1].rstrip() + "…"
