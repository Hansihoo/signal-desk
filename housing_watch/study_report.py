"""Study-document presentation. Research facts remain in report-v1 data.

Existing report IDs keep Editorial. Future reports use the selected study style;
optional interactive catalog data is bound to the exact report content hash.
"""
import json
from pathlib import Path
from .briefing_preview import _escape as esc, _authored_blocks, _citations, _table, _chart
from .research_data import validate_report
from .research_topics import public_url
from .research_workflow import digest

ROOT = Path(__file__).parent
CONFIG = ROOT.parent / 'config'


def settings():
    path = CONFIG / 'study_pages.json'
    if not path.exists():
        return {'legacy_report_ids': [], 'default_layout': 'editorial', 'catalogs': {}}
    value = json.loads(path.read_text(encoding='utf-8'))
    if value.get('schema_version') != 1 or value.get('default_layout') not in ('study', 'editorial'):
        raise ValueError('Invalid study presentation configuration')
    return value


def uses_study(report_id):
    config = settings()
    return config['default_layout'] == 'study' and report_id not in config['legacy_report_ids']


def catalog_for(report):
    filename = settings().get('catalogs', {}).get(report['id'])
    if not filename:
        return None
    if Path(filename).name != filename:
        raise ValueError('Catalog must use a config filename')
    catalog = json.loads((CONFIG / filename).read_text(encoding='utf-8'))
    if catalog.get('report_id') != report['id'] or catalog.get('schema_version') != 1:
        raise ValueError('Catalog identity mismatch')
    # Historical editions must not show a later catalog.
    if catalog.get('report_hash') != digest(report):
        return None
    seen = set()
    for item in catalog['tools']:
        if item['id'] in seen:
            raise ValueError('Duplicate catalog tool')
        seen.add(item['id'])
        for field in ('docs', 'repo', 'license_url'):
            if public_url(item[field]) != item[field]:
                raise ValueError('Unsafe catalog link')
        if not set(item['source_ids']) <= {r['id'] for r in report['references']}:
            raise ValueError('Catalog source not in report')
        # Keep all factual catalog copy in the canonical, reviewed report too.
        chapter = next(ch for ch in report['explanation'] if ch['id'] == 'catalog')
        block = next((b for b in chapter['blocks'] if b['title'] == item['name']), None)
        if not block or any(item[key] not in block['text'] for key in (
                'purpose','use','reuse','fit','jenkins','limits','alternatives','license','maintenance')):
            raise ValueError('Catalog copy differs from reviewed report')
    return catalog


def _catalog(catalog, numbers):
    fields = sorted({t['field'] for t in catalog['tools']})
    options = ''.join('<option>%s</option>' % esc(f) for f in fields)
    result = ['''<div class="catalog-controls" hidden>
      <label>기술 검색<input id="tool-search" type="search" placeholder="이름, 기능 또는 상황 검색"></label>
      <label>분야<select id="tool-field"><option value="">전체</option>%s</select></label>
      <label>추천 범위<select id="tool-tier"><option value="">전체</option><option>필수 기반</option><option>상황별 권장</option><option>대규모 환경에서 고려</option></select></label>
      <button id="tool-reset" type="button">초기화</button></div>
      <p id="tool-count" aria-live="polite">%d개 기술</p>
      <p class="catalog-help" hidden>비교할 기술을 2개 이상 선택하면 아래 비교표에 표시됩니다. 선택은 필터를 바꿔도 유지됩니다.</p>
      <div class="tool-catalog">''' % (options, len(catalog['tools']))]
    for t in catalog['tools']:
        search = ' '.join(str(v) for v in t.values()).lower()
        result.append('<article class="tool" data-tool="%s" data-field="%s" data-tier="%s" data-search="%s">' % tuple(esc(v) for v in (t['id'],t['field'],t['tier'],search)))
        result.append('<p class="tool-meta">분야: %s<br>추천 범위: %s<br>유형: %s</p><h3>%s</h3><p>%s</p><p class="tool-fit"><strong>도입 조건</strong> %s</p><label class="tool-select" hidden><input type="checkbox" value="%s">비교 선택</label>' % tuple(esc(v) for v in (t['field'],t['tier'],t['kind'],t['name'],t['purpose'],t['fit'],t['id'])))
        result.append('<details><summary>상세 정보</summary><dl>')
        for label,key in [('활용 예시','use'),('대신 구현하는 기능','reuse'),('기존 Jenkins에 추가할 가치','jenkins'),('주의사항과 운영 비용','limits'),('대체 기술','alternatives'),('라이선스','license'),('유지보수 확인','maintenance')]:
            result.append('<div><dt>%s</dt><dd>%s</dd></div>' % (label,esc(t[key])))
        result.append('</dl><p class="tool-links"><a href="%s">공식 문서 ↗</a><a href="%s">저장소 ↗</a><a href="%s">라이선스 ↗</a></p>%s</details></article>' % (esc(t['docs']),esc(t['repo']),esc(t['license_url']),_citations(t,numbers)))
    result.append('</div><p id="tool-empty" hidden>검색 조건에 맞는 기술이 없습니다.</p><section id="tool-comparison" hidden><h3>선택한 기술 비교</h3><p>기능이 다른 도구는 대체 관계가 아닐 수 있습니다. 기존 Jenkins에서 필요한 역할을 기준으로 읽으십시오.</p><div class="study-table" tabindex="0" role="region" aria-label="선택한 기술 비교"><table><thead><tr><th scope="col">기술</th><th scope="col">기능과 재사용 범위</th><th scope="col">Jenkins 추가 가치</th><th scope="col">조건과 주의사항</th><th scope="col">라이선스</th></tr></thead><tbody></tbody></table></div><button id="clear-comparison" type="button">비교 해제</button></section>')
    return ''.join(result)


def render_study(report, prefix='', edition=None):
    validate_report(report)
    numbers = {s['id']:i for i,s in enumerate(report['references'],1)}
    catalog = catalog_for(report)
    chapters = report.get('explanation', [])
    inline_tables = {'frameworks':'framework-comparison','ci':'ci-comparison'}
    tables = {t['id']:t for t in report.get('tables',[])}
    data_anchor = False
    def data_content(html):
        nonlocal data_anchor
        if data_anchor:
            return html
        data_anchor = True
        return '<div id="data">%s</div>' % html
    nav = ''.join('<a data-section-link href="#chapter-%s">%s</a>' % (esc(ch['id']),esc(ch['title'])) for ch in chapters)
    quick = [('개요', chapters[0]['id'] if chapters else 'summary'),('구축','architecture'),('도구','catalog'),('AI 활용','agents')]
    available = {c['id'] for c in chapters}
    quick = [(label,id) for label,id in quick if id in available]
    shortnav = ''.join('<a data-section-link href="#chapter-%s">%s</a>' % (esc(id),label) for label,id in quick)
    toolbar = '<div class="study-toolbar"><div class="study-toolbar-inner"><a id="document-back" href="%sindex.html">← 리서치 목록</a><nav class="study-quick" aria-label="주요 목차">%s</nav><details id="document-menu"><summary>목차 <span id="document-current"></span><span aria-hidden="true">▾</span></summary><nav aria-label="문서 목차">%s</nav></details><button id="study-print" type="button">인쇄</button></div></div>' % (prefix,shortnav,nav)
    parts = [toolbar,'<article class="study-document" id="study-document">',
        '<header class="study-title"><p class="study-eyebrow">%s</p><h1>%s</h1><p class="study-deck">%s</p><p class="study-byline">자료 확인 %s</p>%s</header>' % (esc(' / '.join(report['topic_path']).replace('개발·운영','개발과 운영')),esc(report['title']),esc(report['description']),esc(report['checked_on']),'<p class="study-notice">이전 기록 (%s차)</p>' % edition if edition else '')]
    parts.append('<section id="summary" class="study-summary"><h2>요약</h2><p class="study-summary-deck">%s</p><dl>%s</dl></section>' % (esc(report['deck']),''.join('<div><dt>%s</dt><dd>%s %s</dd></div>' % (esc(p['label']),esc(p['text']),_citations(p,numbers)) for p in report['summary'])))
    parts.append('<section class="study-outline" id="outline"><h2>목차</h2><ol>%s</ol></section>' % ''.join('<li><a href="#chapter-%s"><span>%02d</span><b>%s</b></a></li>' % (esc(ch['id']),i,esc(ch['title'].split('. ',1)[-1])) for i,ch in enumerate(chapters,1)))
    for index,ch in enumerate(chapters,1):
        parts.append('<section class="study-chapter" id="chapter-%s"><header><p class="chapter-number">%02d</p><h2>%s</h2><p class="chapter-lead">%s</p></header>' % (esc(ch['id']),index,esc(ch['title'].split('. ',1)[-1]),esc(ch['lead'])))
        blocks = ch['blocks']
        if ch['id']=='catalog' and catalog:
            parts.append(_authored_blocks(blocks[:1],numbers));parts.append(_catalog(catalog,numbers))
        else:
            for bi,block in enumerate(blocks):
                if block['type']=='code' or (ch['id']=='tips' and bi>0):
                    parts.append('<details class="study-depth"><summary>%s</summary>%s</details>' % (esc(block['title']),_authored_blocks([block],numbers)))
                else:
                    parts.append(_authored_blocks([block],numbers))
        if inline_tables.get(ch['id']) in tables:
            parts.append(data_content(_table(tables[inline_tables[ch['id']]],numbers)))
        parts.append('</section>')
    remaining_tables = [t for t in report.get('tables',[]) if t['id'] not in {
        inline_tables.get(ch['id']) for ch in chapters}]
    if remaining_tables or report['datasets'] or report['metrics']:
        parts.append('<section class="study-chapter" id="%s"><h2>비교 자료</h2>' % ('study-data' if data_anchor else 'data'))
        parts.extend(_table(t,numbers) for t in remaining_tables)
        parts.extend('<p><strong>%s</strong> %s %s — %s %s</p>' % (
            esc(m['label']),esc(m['value']),esc(m['unit']),esc(m['qualifier']),_citations(m,numbers))
            for m in report['metrics'])
        parts.extend(_chart(d,numbers) for d in report['datasets'])
        parts.append('</section>')
    for lesson in report.get('learning',[]):
        parts.append('<details class="study-depth" id="learning-%s"><summary>%s</summary><p>%s</p>%s</details>' % (esc(lesson['id']),esc(lesson['title']),esc(lesson['lead']),_authored_blocks(lesson['blocks'],numbers)))
    parts.append('<section class="study-chapter" id="result"><h2>%s</h2>%s</section>' % (esc(report['result']['title']),''.join('<h3>%s</h3><p>%s %s</p>' % (esc(p['label']),esc(p['text']),_citations(p,numbers)) for p in report['result']['points'])))
    parts.append('<section class="study-chapter study-references" id="references"><h2>참고자료</h2><p>%s</p><ol>%s</ol><h3>검토 범위</h3><p>%s</p>%s</section></article>' % (esc(report['source_note']),''.join('<li id="ref-%d"><a href="%s">%s ↗</a><p>%s</p></li>' % (i,esc(s['url']),esc(s['title']),esc(s['description'])) for i,s in enumerate(report['references'],1)),esc(report['scope']),''.join('<p>%s %s</p>' % (esc(c['text']),_citations(c,numbers)) for c in report['caveats'])))
    payload = json.dumps(catalog['tools'] if catalog else [],ensure_ascii=False)
    for char, code in (('<','003c'), ('>','003e'), ('&','0026')):
        payload = payload.replace(char, chr(92) + 'u' + code)
    css = (ROOT/'study_report.css').read_text(encoding='utf-8')
    js = (ROOT/'study_report.js').read_text(encoding='utf-8')
    return '<style>%s</style><div class="study-reader">%s</div><script type="application/json" id="study-tools">%s</script><script>%s</script>' % (css,''.join(parts),payload,js)
