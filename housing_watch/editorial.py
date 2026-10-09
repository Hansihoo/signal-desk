"""HTML5 UP Editorial presentation; all research facts come from validated data."""

import base64
import hashlib
import re
from pathlib import Path
from urllib.parse import urlencode

from .briefing_preview import _escape, _report_replacements, _topic_rows, _chart, _table
from .research_data import validate_report


ROOT = Path(__file__).parent
ASSETS = ROOT / "assets" / "editorial"


def _style():
    # Exact vendor CSS stays intact on disk. Replace its two remote imports with
    # locally packaged fonts; icons are native SVG in the adapted shell.
    vendor = re.sub(r"^@import[^\n]+\n", "", (ASSETS / "main.css").read_text(encoding="utf-8"), flags=re.M)
    fonts = (ASSETS / "fonts.css").read_text(encoding="utf-8")
    for path in ASSETS.glob("*.woff2"):
        fonts = fonts.replace(path.name, "data:font/woff2;base64," + base64.b64encode(path.read_bytes()).decode("ascii"))
    licenses = "\n".join(path.read_text(encoding="utf-8") for path in sorted(ASSETS.glob("*-LICENSE.txt")))
    return "/* Embedded fonts — redistribution notices:\n" + licenses.replace("*/", "* /") + "\n*/\n" + fonts + vendor + (ROOT / "editorial.css").read_text(encoding="utf-8")


def _fill(template, values):
    # Single pass prevents report text containing __PLACEHOLDERS__ from becoming code.
    return re.sub(r"__[A-Z][A-Z_]*?__", lambda match: values[match.group()], template)


def _headline(text):
    # Keep short joined terms (e.g. 표·버튼·입력) together. Very long terms can
    # still wrap inside their capped inline block, rather than overflowing.
    parts = re.split(r"(\S*[·/]\S*)", text)
    return "".join('<span class="title-term">%s</span>' % _escape(part)
                   if index % 2 else _escape(part) for index, part in enumerate(parts))


def _groups(reports):
    groups = {}
    for report in reports:
        groups.setdefault(report["topic_path"][0], []).append(report)
    return groups


def _tree(reports, prefix, active=None, has_model_ledger=False, model_page_count=0, model_library_count=None):
    guide_count = model_page_count if model_library_count is None else model_library_count
    parts = ['<ul class="research-tree">']
    for name, members in _groups(reports).items():
        categories = {}
        for item in members:
            children = categories
            for label in item["topic_path"][1:]:
                node = children.setdefault(label, {"members": [], "children": {}})
                node["members"].append(item)
                children = node["children"]

        def branch(nodes, path):
            links = []
            for label, node in nodes.items():
                current_path = path + [label]
                items = node["members"]
                # A single deep leaf is a report page; its parent remains the
                # board containing both direct reports and all descendants.
                target = (prefix + items[0]["id"] + ".html" if len(current_path) > 2
                          and len(items) == 1 and not node["children"] else
                          prefix + "index.html?" + urlencode({"topic": " / ".join(current_path)}) + "#board")
                child_links = branch(node["children"], current_path) if node["children"] else ""
                if current_path[-1] == "AI 모델·API":
                    model_links = []
                    if has_model_ledger:
                        model_links.append('<li><a href="%sai-models.html"%s><span class="tree-label">전체 모델 비교표</span><small>1</small></a></li>' % (
                            prefix, ' aria-current="page"' if active == "ai-models" else ""))
                    if guide_count:
                        model_links.append('<li><a href="%sai-model-guides.html"%s><span class="tree-label">모델별 가이드·평가 자료</span><small>%d</small></a></li>' % (
                            prefix, ' aria-current="page"' if active == "ai-model-guides" else "", guide_count))
                    child_links = "".join(model_links) + child_links
                children_html = '<ul class="tree-children">%s</ul>' % child_links if child_links else ""
                page_count = len(items)
                if label == "AI 모델·API":
                    page_count += int(has_model_ledger) + model_page_count
                links.append('<li><a href="%s"%s><span class="tree-label">%s</span> <small>%d</small></a>%s</li>' % (
                    _escape(target), ' aria-current="page"' if any(item["id"] == active for item in items) else "",
                    _escape(label), page_count, children_html))
            return "".join(links)

        links = branch(categories, [name])
        if any(item["topic_id"] == "business" for item in members):
            links = '<li><a href="%sbusiness.html">사업 전체 자료</a></li>' % prefix + links
        page_count = len(members)
        if any("AI 모델·API" in item["topic_path"][1:] for item in members):
            page_count += int(has_model_ledger) + model_page_count
        parts.append('<li><details class="tree-group" open><summary><span class="tree-label">%s</span><small>%d</small></summary><ul>%s</ul></details></li>' % (
            _escape(name), page_count, links))
    return "".join(parts) + "</ul>"


def _board_tools(reports):
    options = []
    for name, members in _groups(reports).items():
        paths = list(dict.fromkeys(" / ".join(item["topic_path"][:depth])
                                   for item in members for depth in range(2, len(item["topic_path"]) + 1)))
        children = "".join('<option value="%s">%s</option>' % (_escape(path), _escape(" / ".join(path.split(" / ")[1:]))) for path in paths)
        options.append('<optgroup label="%s"><option value="%s">%s 전체</option>%s</optgroup>' % (_escape(name), _escape(name), _escape(name), children))
    return '''<form class="board-tools" action="index.html" method="get">
      <div class="board-query"><label class="sr-only" for="report-query">보고서 검색</label><input type="search" id="report-query" name="q" placeholder="주제·내용 검색"></div>
      <div><label class="sr-only" for="report-topic">보고서 분야</label><select id="report-topic" name="topic"><option value="">전체 분야</option>%s</select></div>
      <button type="submit">검색</button></form>''' % "".join(options)


def _post(report, url, edition=None):
    # Search the full authored text, including collapsed learning, without rendering
    # hidden explanatory prose or depending on a backend/search service.
    def texts(value):
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for key, item in value.items():
                if key not in ("url", "source_ids", "id"):
                    yield from texts(item)
        elif isinstance(value, list):
            for item in value:
                yield from texts(item)
    search = _escape(" ".join(texts(report)).lower())
    label = " / ".join(report["topic_path"])
    if edition:
        label += " · %d차" % edition
    return '''<article class="research-post" data-topic="%s" data-path="%s" data-search="%s">
      <div class="post-meta"><span>%s</span><time datetime="%s">%s</time></div>
      <h3><a href="%s">%s</a></h3><p>%s</p><a class="post-link" href="%s">보고서 읽기 <span aria-hidden="true">↗</span></a></article>''' % (
        _escape(report["topic_path"][0]), _escape(" / ".join(report["topic_path"])), search, _escape(label), report["checked_on"],
        report["checked_on"].replace("-", "."), _escape(url), _headline(report["title"]),
        _escape(report["deck"]), _escape(url))


def _topic_features(reports):
    parts = []
    for index, (name, members) in enumerate(_groups(reports).items(), 1):
        latest = members[0]
        url = "index.html?" + urlencode({"topic": name}) + "#board"
        parts.append('''<article><span class="topic-mark" aria-hidden="true">%02d</span><div class="content">
          <h3><a href="%s">%s</a><small>%d건</small></h3><a class="latest-title" href="%s.html">%s</a>
          <p class="latest-deck">%s</p><time class="latest-date" datetime="%s">%s</time></div></article>''' % (
            index, _escape(url), _escape(name), len(members), _escape(latest["id"]), _headline(latest["title"]),
            _escape(latest["deck"]), latest["checked_on"], latest["checked_on"].replace("-", ".")))
    return "".join(parts)


def _hero(report, target=None):
    numbers = {source["id"]: index for index, source in enumerate(report["references"], 1)}
    if report["datasets"]:
        visual = _chart(report["datasets"][0], numbers)
    elif report.get("tables"):
        visual = _table(report["tables"][0], numbers)
    else:
        visual = '<ol class="hero-facts">%s</ol>' % "".join('<li>%s</li>' % _escape(item) for item in report["highlights"])
    if target:
        visual = visual.replace('href="#ref-', 'href="' + _escape(target) + '#ref-')
    return visual


def _edition_nav(item, history, prefix):
    editions = [row for row in history if row["id"] == item["id"]]
    if not editions:
        return ""
    links = "".join('<a href="%shistory/%s-r%d.html">%s · %d차</a>' % (
        prefix, _escape(row["id"]), row["revision"], row["document"]["checked_on"].replace("-", "."), row["revision"])
        for row in sorted(editions, key=lambda row: row["revision"], reverse=True))
    return '<section class="edition-list"><header class="major"><h2>이전 기록</h2></header>%s</section>' % links


def render_editorial(output, snapshot, featured, research_data=None, standalone=True):
    from .model_ledger_view import model_ledger_content
    from .model_pages_view import render_model_pages, library_content, official_guides
    reports = [validate_report(item) for item in research_data["reports"]] if research_data else [validate_report(featured)]
    reports = sorted(reports, key=lambda item: (item["checked_on"], item["id"]), reverse=True)
    by_id = {item["id"]: item for item in reports}
    if len(by_id) != len(reports):
        raise ValueError("Duplicate report IDs")
    validate_report(featured)
    revisions = {row["id"]: row["revision"] for row in (research_data or {}).get("report_versions", [])}
    history, seen = [], set()
    for row in (research_data or {}).get("report_history", []):
        document = validate_report(row["document"])
        revision = row["revision"]
        if row["id"] != document["id"] or row["id"] not in by_id or type(revision) is not int or revision < 1:
            raise ValueError("Invalid report history")
        key = (row["id"], revision)
        if key in seen:
            raise ValueError("Duplicate report edition")
        seen.add(key)
        if revision < revisions.get(row["id"], revision):
            history.append(row)
    # Validate all content before writing, then generate stable routes from the
    # canonical DB history. Rebuilding does not replace old text with latest text.
    destination = Path(output) / "preview"
    destination.mkdir(parents=True, exist_ok=True)
    history_root = destination / "history"
    history_root.mkdir(exist_ok=True)
    style, script = _style(), (ROOT / "editorial.js").read_text(encoding="utf-8")
    (destination / "briefing.css").write_text(style, encoding="utf-8")
    style_version = hashlib.sha256(style.encode("utf-8")).hexdigest()[:12]
    shell = (ROOT / "editorial_shell.html").read_text(encoding="utf-8")
    ledger = (research_data or {}).get("model_ledger", {"records": [], "history": [], "runs": []})
    has_model_ledger = bool(ledger["records"])
    model_pages = (research_data or {}).get("model_pages", {"pages": [], "history": [], "runs": []})
    model_page_count = len(model_pages["pages"])
    model_library_count = model_page_count + len(official_guides(reports))
    def page(title, description, content, prefix="", active=None, contents="", editions=""):
        style_block = ('<style id="editorial-style">%s</style>' % style if standalone else
                       '<link rel="stylesheet" href="%sbriefing.css?v=%s">' % (prefix, style_version))
        return _fill(shell, {"__PAGE_TITLE__": _escape(title), "__DESCRIPTION__": _escape(description),
            "__STYLE_BLOCK__": style_block, "__SCRIPT__": script, "__CONTENT__": content, "__PREFIX__": prefix,
            "__TREE__": _tree(reports, prefix, active, has_model_ledger, model_page_count, model_library_count), "__CONTENTS_NAV__": contents, "__EDITION_NAV__": editions,
            "__BUSINESS_LINK__": '<a href="%sbusiness.html">사업</a>' % prefix if any(item["topic_id"] == "business" for item in reports) else ""})
    values = dict(_report_replacements(featured), __REPORT_URL__=_escape(featured["id"] + ".html"),
        __HEADLINE__=_headline(featured["title"]),
        __HERO_VISUAL__=_hero(featured, featured["id"] + ".html"), __TOPIC_FEATURES__=_topic_features(reports),
        __REPORT_COUNT__=str(len(reports)), __BOARD_TOOLS__=_board_tools(reports),
        __BOARD_ROWS__="".join(_post(item, item["id"] + ".html") for item in reports), __TOPIC_ROWS__=_topic_rows(snapshot))
    content = _fill((ROOT / "editorial_home.html").read_text(encoding="utf-8"), values)
    model_links = []
    if has_model_ledger:
        model_links.append('<a href="ai-models.html">주요 LLM 모델 통합 비교 ↗</a><small>1페이지</small><p>사양·제공 상태·AA·코딩 에이전트·Cursor 평가와 변경 기록</p>')
    if model_library_count:
        model_links.append('<a href="ai-model-guides.html">모델별 가이드·비용·평가 자료 ↗</a><small>%d페이지</small>' % model_library_count)
    model_link = '<section class="model-ledger-link">%s</section>' % "".join(model_links)
    if model_links:
        content = content.replace('<section id="board">', model_link + '<section id="board">')
    (destination / "index.html").write_text(page("최근 동향", "개발 동향, 사업 기회와 운영 자료", content), encoding="utf-8")
    business = [item for item in reports if item["topic_id"] == "business"]
    if business:
        def business_page(prefix=""):
            values = {"__BUSINESS_DATE__": _escape(max(item["checked_on"] for item in business)),
                "__REPORT_COUNT__": str(len(business)), "__BOARD_TOOLS__": _board_tools(business),
                "__BOARD_ROWS__": "".join(_post(item, prefix + item["id"] + ".html") for item in business)}
            return page("사업기획", "폴라리스오피스 국책사업·영업 기회·경쟁사 동향", _fill(
                (ROOT / "editorial_business.html").read_text(encoding="utf-8"), values), prefix, "business")
        (destination / "business.html").write_text(business_page(), encoding="utf-8")
        formal = Path(output) / "research" / "business"
        formal.mkdir(parents=True, exist_ok=True)
        (formal / "index.html").write_text(business_page("../../preview/"), encoding="utf-8")
    template = (ROOT / "editorial_report.html").read_text(encoding="utf-8")
    def report_page(item, edition=None):
        prefix = "../" if edition else ""
        values = _report_replacements(item)
        values["__HEADLINE__"] = _headline(item["title"])
        values.update(__HERO_VISUAL__=_hero(item), __EDITION_NOTICE__=(
            '<p class="edition-notice">이전 기록 · %d차 · <a href="../%s.html">현재 보고서</a></p>' % (edition, _escape(item["id"])) if edition else ""))
        content = _fill(template, values)
        if item["id"] == "llm-model-comparison" and not edition and model_links:
            content = model_link + content
        contents = '<nav class="sidebar-contents" aria-label="이 보고서 차례"><header class="major"><h2>차례</h2></header><a href="#summary">요약</a>%s%s<a href="#result">결과</a>%s<a href="#references">참고내용</a></nav>' % (values["__EXPLANATION_LINK__"], values["__DATA_LINK__"], values["__LEARNING_LINK__"])
        return page(item["title"], item["description"], content, prefix, item["id"], contents, _edition_nav(item, history, prefix))
    for item in reports:
        rendered = report_page(item)
        (destination / (item["id"] + ".html")).write_text(rendered, encoding="utf-8")
        if item["id"] == featured["id"]:
            (destination / "report.html").write_text(rendered, encoding="utf-8")
    for row in history:
        (history_root / (row["id"] + "-r%d.html" % row["revision"])).write_text(report_page(row["document"], row["revision"]), encoding="utf-8")
    reviewed_candidates = {candidate_id for row in ledger["records"] if row["source_kind"] == "reviewed"
                           for candidate_id in row["original"].get("candidate_ids", [])}
    candidates = [{"title": item["title"], "url": item["url"], "source": item["source"],
                   "published_at": item["published_at"], "summary": item["summary"]}
                  for item in snapshot.get("items", []) if item.get("topic_id") == "ai" and item.get("category") == "LLM 모델"
                  and item.get("source") != "Theo 모델 리서치" and item["id"] not in reviewed_candidates]
    candidates.sort(key=lambda item: item["published_at"], reverse=True)
    model_content = model_ledger_content(ledger, candidates[:30])
    model_content = '<p><a href="ai-model-guides.html">모델별 분석·선택 가이드·원본 표</a></p>' + model_content
    (destination / "ai-models.html").write_text(page("주요 LLM 모델 통합 비교", "전체 모델 정보와 신규·변경 기록", model_content,
        active="ai-models"), encoding="utf-8")
    models_root = Path(output) / "research" / "ai" / "models"
    models_root.mkdir(parents=True, exist_ok=True)
    (models_root / "index.html").write_text(page("주요 LLM 모델 통합 비교", "전체 모델 정보와 신규·변경 기록",
        model_content.replace('href="ai-model-guides.html"', 'href="../../../preview/ai-model-guides.html"'), "../../../preview/", active="ai-models"), encoding="utf-8")
    render_model_pages(destination, model_pages, page, reports)
    (models_root / "guides.html").write_text(page("모델별 자료", "모델별 가이드·비용·평가 자료",
        library_content(model_pages, "../../../preview/", reports), "../../../preview/", active="ai-model-guides"), encoding="utf-8")
    old_rows = "".join(_post(row["document"], "%s-r%d.html" % (row["id"], row["revision"]), row["revision"])
                       for row in sorted(history, key=lambda row: (row["saved_at"], row["id"], row["revision"]), reverse=True))
    archive = '<section class="history-heading"><header><h1>이전 기록</h1></header></section><section id="board"><div class="section-title"><header class="major"><h2>보고서 기록</h2></header><span class="record-total">%d건</span></div>%s<div class="posts research-posts">%s</div><p class="board-empty" hidden>검색 결과가 없습니다.</p><nav class="board-pagination" aria-label="목록 페이지" hidden><button type="button" data-page="previous">이전</button><span class="page-status" aria-live="polite"></span><button type="button" data-page="next">다음</button></nav>%s</section>' % (
        len(history), _board_tools(reports), old_rows, '<p>이전 기록이 없습니다.</p>' if not history else "")
    (history_root / "index.html").write_text(page("이전 기록", "이전 판의 보고서", archive, "../"), encoding="utf-8")
    notices = "".join('<h2>%s</h2><pre class="license-text">%s</pre>' % (_escape(path.stem), _escape(path.read_text(encoding="utf-8"))) for path in sorted(ASSETS.glob("*LICENSE.txt")))
    (destination / "licenses.html").write_text(page("디자인 라이선스", "Editorial 및 포함 서체의 라이선스", '<section><h1>디자인 라이선스</h1><p>HTML5 UP Editorial 원본을 보고서 목록·한국어 보고서·기록 탐색에 맞춰 수정했습니다. 원본의 기본 레이아웃과 색을 유지하고, 한국어 글자와 탐색 간격을 조정했습니다. 아이콘과 메뉴 동작은 SVG와 기본 JavaScript로 변경했습니다.</p>' + notices + '</section>'), encoding="utf-8")
    return destination
