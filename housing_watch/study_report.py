"""Study-document presentation. Research facts remain in report-v1 data.

Existing report IDs keep Editorial. Future reports use the selected study style;
optional interactive catalog data is bound to the exact report content hash.
"""
import base64
import hashlib
import json
import io
from pathlib import Path, PurePosixPath
import re
import zipfile
from .briefing_preview import _escape as esc, _authored_blocks, _citations, _table, _chart
from .research_data import validate_report
from .research_topics import public_url
from .research_workflow import digest, pointer
from .study_visual import reviewed_asset

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


def visuals_for(report):
    config = settings()
    filename = config.get('visual_guides', {}).get(report['id'])
    filenames = ([filename] if filename else []) + config.get('visual_editions', {}).get(report['id'], [])
    if not filenames:
        return None
    guide = None
    for candidate in filenames:
        if Path(candidate).name != candidate:
            raise ValueError('Visual guide must use a config filename')
        item = json.loads((CONFIG / candidate).read_text(encoding='utf-8'))
        if item.get('schema_version') != 1 or item.get('report_id') != report['id']:
            raise ValueError('Visual guide identity mismatch')
        if item.get('report_hash') == digest(report):
            guide = item
            break
    if guide is None:
        return None
    topics = guide.get('topic_sections')
    if topics is not None:
        if set(topics) != {ch['id'] for ch in report['explanation']}:
            raise ValueError('Topic sections must cover each chapter')
        seen = set()
        for chapter in report['explanation']:
            sections = topics[chapter['id']]
            starts = [s['start'] for s in sections]
            if not starts or starts[0] != 0 or any(type(i) is not int for i in starts) or starts != sorted(set(starts)):
                raise ValueError('Topic sections need ordered unique block boundaries')
            for section in sections:
                sid, start = section['id'], section['start']
                if not re.fullmatch(r'[a-z][a-z0-9-]*', sid) or sid in seen:
                    raise ValueError('Topic section IDs must be unique')
                seen.add(sid)
                if start >= len(chapter['blocks']) or chapter['blocks'][start]['type'] != 'terms':
                    raise ValueError('Topic section needs reviewed introductory points')
    else:
        for chapter in report['explanation']:
            first = chapter['blocks'][0]
            if first['type'] != 'terms' or first['title'] != '핵심 정리':
                raise ValueError('Visual study chapter needs reviewed key points')
    allowed = {'summary'} | {c['id'] for c in report['explanation']}
    for place, visual in guide['images'].items():
        if place not in allowed or Path(visual['asset']).name != visual['asset']:
            raise ValueError('Invalid visual location or asset filename')
        reviewed_asset(visual, ROOT / 'assets' / 'editorial')
    _practice_files(report, guide)
    visual_ids, visual_paths = set(), set()
    for visual in guide.get('block_visuals', []):
        if not re.fullmatch(r'visual-[a-z0-9-]+', visual['id']) or visual['id'] in visual_ids:
            raise ValueError('Inline visual IDs must be unique')
        path = visual['path']
        if not re.fullmatch(r'/explanation/\d+/blocks/\d+', path) or path in visual_paths:
            raise ValueError('Inline visual needs a unique canonical block path')
        try:
            block = pointer(report, path)
        except (KeyError, IndexError, TypeError):
            raise ValueError('Inline visual block is missing')
        if visual['kind'] not in ('flow', 'recovery') or block['type'] != 'steps' or not 2 <= len(block['items']) <= 6:
            raise ValueError('Inline visual needs reviewed process steps')
        visual_ids.add(visual['id']); visual_paths.add(path)
    table_ids = {table['id'] for table in report.get('tables', [])}
    topic_ids = {s['id'] for sections in (topics or {}).values() for s in sections}
    placed_tables = set()
    for topic_id, ids in guide.get('topic_tables', {}).items():
        if topic_id not in topic_ids or not isinstance(ids, list) or not ids or not set(ids) <= table_ids or placed_tables.intersection(ids) or len(ids) != len(set(ids)):
            raise ValueError('Topic table placement must reference unique reviewed tables')
        placed_tables.update(ids)
    return guide


def _practice_files(report, guide):
    bundle = guide.get('practice_bundle')
    if not bundle:
        return []
    filename = bundle['filename']
    if not re.fullmatch(r'[a-z0-9-]+\.zip', filename):
        raise ValueError('Invalid practice bundle filename')
    topic_ids = {s['id'] for sections in guide.get('topic_sections', {}).values() for s in sections}
    lesson = next((ch for ch in report.get('learning', []) if ch['id'] == bundle['lesson_id']), None)
    if not lesson or bundle['topic_id'] not in topic_ids or not bundle['files']:
        raise ValueError('Practice bundle must refer to reviewed code and a topic')
    files, seen = [], set()
    for item in bundle['files']:
        name, index = item['path'], item['block']
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name or name in seen:
            raise ValueError('Unsafe practice file path')
        if type(index) is not int or index < 0 or index >= len(lesson['blocks']):
            raise ValueError('Invalid practice code index')
        block = lesson['blocks'][index]
        if block['type'] != 'code' or name != 'devops-sort/' + block['title']:
            raise ValueError('Practice file differs from reviewed code')
        seen.add(name)
        files.append((name, block['text'].encode('utf-8')))
    return files


def write_practice_bundle(report, destination):
    """Export immutable practice code, never the current mutable example folder."""
    guide = visuals_for(report)
    files = _practice_files(report, guide) if guide else []
    if not files:
        return None
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, contents in files:
            info = zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, contents)
    target = Path(destination) / 'assets' / guide['practice_bundle']['filename']
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or target.read_bytes() != data.getvalue():
        target.write_bytes(data.getvalue())
    return target


def _process_figure(block, visual, numbers):
    nodes = []
    for index,item in enumerate(block['items'],1):
        if visual['kind'] == 'recovery':
            filename, explanation = item['text'].split('\n',1) if '\n' in item['text'] else (item['text'],'')
            body = '<code class="version-file">%s</code><p>%s</p>' % (esc(filename),esc(explanation))
        else:
            body = '<p>%s</p>' % esc(item['text'])
        arrow = '<span class="visual-arrow" aria-hidden="true"></span>' if index < len(block['items']) else ''
        nodes.append('<li><span class="visual-step" aria-hidden="true">%02d</span><strong>%s</strong>%s%s</li>' % (index,esc(item['label']),body,arrow))
    return '<figure class="process-figure %s" id="%s" aria-labelledby="%s-title"><figcaption id="%s-title">%s</figcaption><ol class="process-flow" style="--flow-columns:%d" role="list">%s</ol><p class="topic-sources">%s</p></figure>' % (esc(visual['kind']),esc(visual['id']),esc(visual['id']),esc(visual['id']),esc(block['title']),len(nodes),''.join(nodes),_citations(block,numbers))


def _topic_content(blocks, numbers, block_visuals=None):
    parts = []
    for block in blocks:
        cites = _citations(block, numbers)
        visual = (block_visuals or {}).get(digest(block))
        if visual:
            parts.append(_process_figure(block,visual,numbers))
        elif block['type'] == 'paragraph':
            parts.append('<div class="topic-prose"><p>%s %s</p></div>' % (esc(block['text']), cites))
        elif block['type'] == 'code':
            parts.append('<figure class="topic-code"><figcaption>%s</figcaption><pre tabindex="0" role="region" aria-label="%s"><code>%s</code></pre><p class="topic-sources">%s</p></figure>' % (esc(block['title']),esc(block['title']),esc(block['text']),cites))
        else:
            parts.append(_authored_blocks([block], numbers, heading_tag='p', show_editorial_labels=False))
    return ''.join(parts)


def _topic_section(chapter, section, next_start, chapter_number, topic_number, numbers, bundle, prefix, block_visuals=None, table_html=''):
    blocks = chapter['blocks'][section['start']:next_start]
    first = blocks[0]
    points = ''.join('<li><strong>%s</strong> %s</li>' % (esc(i['label']),esc(i['text'])) for i in first['items'])
    download = ''
    if bundle and bundle['topic_id'] == section['id']:
        download = '<p class="practice-download"><a download href="%sassets/%s">실습 파일 다운로드 ↓</a><span>Python 코드, 테스트, 빌드와 CI 설정</span></p>' % (prefix,esc(bundle['filename']))
    return ('<section class="study-topic" id="topic-%s" data-chapter="chapter-%s"><h3><span class="topic-number">%d.%d</span> %s</h3><ul class="topic-points">%s</ul><p class="topic-sources">%s</p>%s%s%s</section>') % (esc(section['id']),esc(chapter['id']),chapter_number,topic_number,esc(first['title']),points,_citations(first,numbers),download,table_html,_topic_content(blocks[1:],numbers,block_visuals))


def _visual_figure(visual, place):
    mime, data = reviewed_asset(visual, ROOT / 'assets' / 'editorial')
    source = 'data:' + mime + ';base64,' + base64.b64encode(data).decode('ascii')
    return ('<figure class="study-visual" id="visual-%s"><img src="%s" alt="%s" '
            'width="%d" height="%d" decoding="async"><figcaption><span>%s</span>'
            '<button type="button" class="visual-open" hidden aria-haspopup="dialog">'
            '이미지 크게 보기</button></figcaption></figure>') % (
                esc(place), source, esc(visual['alt']), visual['width'], visual['height'], esc(visual['caption']))


def _key_points(block, numbers):
    return '<div class="chapter-keypoints" aria-label="핵심 정리"><ol>%s</ol><p class="keypoint-sources">%s</p></div>' % (
        ''.join('<li><strong>%s</strong><p>%s</p></li>' % (esc(i['label']), esc(i['text'])) for i in block['items']),
        _citations(block, numbers))


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
    visual_guide = visuals_for(report)
    images = visual_guide['images'] if visual_guide else {}
    expanded_code_chapters = visual_guide.get('expanded_code_chapters', []) if visual_guide else []
    reader_content_only = visual_guide.get('reader_content_only', False) if visual_guide else False
    topics = visual_guide.get('topic_sections') if visual_guide else None
    bundle = visual_guide.get('practice_bundle') if visual_guide else None
    block_visuals = {digest(pointer(report,v['path'])):v for v in visual_guide.get('block_visuals', [])} if visual_guide else {}
    topic_tables = visual_guide.get('topic_tables', {}) if visual_guide else {}
    chapters = report.get('explanation', [])
    inline_tables = {'frameworks':'framework-comparison','ci':'ci-comparison'}
    tables = {t['id']:t for t in report.get('tables',[])}
    used_tables, used_datasets = set(), set()
    data_anchor = False
    def data_content(html):
        nonlocal data_anchor
        if data_anchor:
            return html
        data_anchor = True
        return '<div id="data">%s</div>' % html
    nav = ''.join('<a data-section-link href="#chapter-%s">%s</a>' % (esc(ch['id']),esc(ch['title'])) for ch in chapters)
    if topics:
        nav = ''.join('<div class="toc-chapter"><a data-section-link href="#chapter-%s">%s</a><ol>%s</ol></div>' % (
            esc(ch['id']),esc(ch['title']),''.join('<li><a data-section-link href="#topic-%s">%d.%d %s</a></li>' % (esc(s['id']),ci,si,esc(ch['blocks'][s['start']]['title'])) for si,s in enumerate(topics[ch['id']],1))) for ci,ch in enumerate(chapters,1))
    quick = [('개요', chapters[0]['id'] if chapters else 'summary'),('구축','architecture'),('운영','operations'),('학습','study'),('도구','catalog'),('AI 활용','agents')]
    available = {c['id'] for c in chapters}
    quick = [(label,id) for label,id in quick if id in available]
    if topics:
        quick = [(label,ch['id']) for label,ch in zip(('이해','구성','구축','운영'),chapters)]
    shortnav = ''.join('<a data-section-link href="#chapter-%s">%s</a>' % (esc(id),label) for label,id in quick)
    toolbar = '<div class="study-toolbar"><div class="study-toolbar-inner"><a id="document-back" href="%sindex.html">← 리서치 목록</a><nav class="study-quick" aria-label="주요 목차">%s</nav><details id="document-menu"><summary>목차 <span id="document-current"></span><span aria-hidden="true">▾</span></summary><nav aria-label="문서 목차">%s</nav></details><button id="study-print" type="button">인쇄</button></div></div>' % (prefix,shortnav,nav)
    if topics:
        toolbar = toolbar.replace('목차 <span id="document-current"></span>', '목차 보기').replace('</button></div></div>', '</button></div><p id="document-current" class="study-location" aria-label="현재 읽는 위치"></p></div>')
    parts = [toolbar,'<article class="study-document" id="study-document">',
        '<header class="study-title"><p class="study-eyebrow">%s</p><h1>%s</h1><p class="study-deck">%s</p><p class="study-byline">자료 확인 %s</p>%s</header>' % (esc(' / '.join(report['topic_path']).replace('개발·운영','개발과 운영')),esc(report['title']),esc(report['description']),esc(report['checked_on']),'<p class="study-notice">이전 기록 (%s차)</p>' % edition if edition else '')]
    summary_first = visual_guide and visual_guide.get('summary_image_first', False)
    parts.append('<section id="summary" class="study-summary"><h2>요약</h2>%s<p class="study-summary-deck">%s</p><dl>%s</dl></section>' % (_visual_figure(images['summary'], 'summary') if summary_first and 'summary' in images else '',esc(report['deck']),''.join('<div><dt>%s</dt><dd>%s %s</dd></div>' % (esc(p['label']),esc(p['text']),_citations(p,numbers)) for p in report['summary'])))
    if 'summary' in images and not summary_first:
        parts.append(_visual_figure(images['summary'], 'summary'))
    outline = []
    for i,ch in enumerate(chapters,1):
        subtopics = '<ol>%s</ol>' % ''.join('<li><a data-section-link href="#topic-%s"><span>%d.%d</span>%s</a></li>' % (esc(s['id']),i,si,esc(ch['blocks'][s['start']]['title'])) for si,s in enumerate(topics[ch['id']],1)) if topics else ''
        outline.append('<li><a href="#chapter-%s"><span>%02d</span><b>%s</b></a>%s</li>' % (esc(ch['id']),i,esc(ch['title'].split('. ',1)[-1]),subtopics))
    parts.append('<section class="study-outline" id="outline"><h2>목차</h2><ol>%s</ol></section>' % ''.join(outline))
    for index,ch in enumerate(chapters,1):
        lead = '<p class="chapter-lead">%s</p>' % esc(ch['lead'])
        heading = ch['title'] if topics else ch['title'].split('. ',1)[-1]
        parts.append('<section class="study-chapter" id="chapter-%s"><header>%s<h2>%s</h2>%s</header>' % (esc(ch['id']),'' if topics else '<p class="chapter-number">%02d</p>' % index,esc(heading),lead if topics or not visual_guide else ''))
        blocks = ch['blocks']
        if visual_guide and not topics:
            parts.append(_key_points(blocks[0], numbers))
            blocks = blocks[1:]
            if ch['id'] in images:
                parts.append(_visual_figure(images[ch['id']], ch['id']))
            parts.append(lead)
        if topics:
            sections = topics[ch['id']]
            for ti,section in enumerate(sections,1):
                end = sections[ti]['start'] if ti < len(sections) else len(blocks)
                table_html = ''
                for tid in topic_tables.get(section['id'], []):
                    table_html += '<div class="topic-table">%s</div>' % data_content(_table(tables[tid],numbers))
                    used_tables.add(tid)
                parts.append(_topic_section(ch,section,end,index,ti,numbers,bundle,prefix,block_visuals,table_html))
        elif ch['id']=='catalog' and catalog:
            parts.append(_authored_blocks(blocks[:1],numbers,show_editorial_labels=not reader_content_only));parts.append(_catalog(catalog,numbers))
        else:
            for bi,block in enumerate(blocks):
                if block['type']=='code' or (ch['id']=='tips' and bi>0):
                    expanded = ' open' if block['type']=='code' and ch['id'] in expanded_code_chapters else ''
                    parts.append('<details class="study-depth"%s><summary>%s</summary>%s</details>' % (expanded,esc(block['title']),_authored_blocks([block],numbers,show_editorial_labels=not reader_content_only)))
                else:
                    parts.append(_authored_blocks([block],numbers,show_editorial_labels=not reader_content_only))
        # IDs prefixed with the chapter ID keep its evidence in the reading path.
        for table in report.get('tables', []):
            if table['id'] not in used_tables and (table['id'] == inline_tables.get(ch['id']) or table['id'].startswith(ch['id'] + '-')):
                parts.append(data_content(_table(table, numbers)))
                used_tables.add(table['id'])
        for dataset in report['datasets']:
            if dataset['id'].startswith(ch['id'] + '-') and dataset['id'] not in used_datasets:
                parts.append(data_content(_chart(dataset, numbers)))
                used_datasets.add(dataset['id'])
        parts.append('</section>')
    remaining_tables = [t for t in report.get('tables',[]) if t['id'] not in used_tables]
    remaining_datasets = [d for d in report['datasets'] if d['id'] not in used_datasets]
    if remaining_tables or remaining_datasets or report['metrics']:
        parts.append('<section class="study-chapter" id="%s"><h2>비교 자료</h2>' % ('study-data' if data_anchor else 'data'))
        parts.extend(_table(t,numbers) for t in remaining_tables)
        parts.extend('<p><strong>%s</strong> %s %s — %s %s</p>' % (
            esc(m['label']),esc(m['value']),esc(m['unit']),esc(m['qualifier']),_citations(m,numbers))
            for m in report['metrics'])
        parts.extend(_chart(d,numbers) for d in remaining_datasets)
        parts.append('</section>')
    elif not data_anchor:
        # Keep incoming historical links without adding an empty reader section.
        parts.append('<section id="data" hidden aria-hidden="true"></section>')
    for lesson in report.get('learning',[]):
        contents = _topic_content(lesson['blocks'],numbers) if topics else _authored_blocks(lesson['blocks'],numbers,show_editorial_labels=not reader_content_only)
        parts.append('<details class="study-depth" id="learning-%s"><summary>%s</summary><p>%s</p>%s</details>' % (esc(lesson['id']),esc(lesson['title']),esc(lesson['lead']),contents))
    result_tag = 'p class="result-label"' if topics else 'h3'
    result_end = 'p' if topics else 'h3'
    parts.append('<section class="study-chapter" id="result"><h2>%s</h2>%s</section>' % (esc(report['result']['title']),''.join('<%s>%s</%s><p>%s %s</p>' % (result_tag,esc(p['label']),result_end,esc(p['text']),_citations(p,numbers)) for p in report['result']['points'])))
    reference_intro = '' if reader_content_only else '<p>%s</p>' % esc(report['source_note'])
    scope_heading = '적용 범위와 한계' if reader_content_only else '검토 범위'
    parts.append('<section class="study-chapter study-references" id="references"><h2>참고자료</h2>%s<ol>%s</ol><%s>%s</%s><p>%s</p>%s</section></article>' % (reference_intro,''.join('<li id="ref-%d"><a href="%s">%s ↗</a><p>%s</p></li>' % (i,esc(s['url']),esc(s['title']),esc(s['description'])) for i,s in enumerate(report['references'],1)),result_tag,scope_heading,result_end,esc(report['scope']),''.join('<p>%s %s</p>' % (esc(c['text']),_citations(c,numbers)) for c in report['caveats'])))
    payload = json.dumps(catalog['tools'] if catalog else [],ensure_ascii=False)
    for char, code in (('<','003c'), ('>','003e'), ('&','0026')):
        payload = payload.replace(char, chr(92) + 'u' + code)
    css = (ROOT/'study_report.css').read_text(encoding='utf-8')
    js = (ROOT/'study_report.js').read_text(encoding='utf-8')
    if images:
        parts.append('<dialog id="study-image-dialog" aria-labelledby="study-image-title"><form method="dialog"><h2 id="study-image-title">이미지 크게 보기</h2><button aria-label="이미지 확대 보기 닫기">닫기</button></form><p class="image-help">확대해서 가로로 움직이며 읽을 수 있습니다.</p><div class="image-pan" tabindex="0" role="region" aria-label="확대한 이미지"><img alt=""></div></dialog>')
    layout = 'study-reader study-hierarchy' if topics else 'study-reader'
    return '<style>%s</style><div class="%s">%s</div><script type="application/json" id="study-tools">%s</script><script>%s</script>' % (css,layout,''.join(parts),payload,js)
