"""Model document library and isolated, interactive copies of source pages."""

import json
import re
from html import escape
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


ROOT = Path(__file__).parent


def library_content(pages, prefix=""):
    rows = []
    for row in sorted(pages["pages"], key=lambda row: (row["document"]["updated_on"], row["slug"]), reverse=True):
        doc = row["document"]
        searchable = " ".join([doc["title"], doc["description"], doc["category"], *doc["tags"]])
        rows.append('<tr data-category="%s" data-search="%s"><td><a href="%smodel-guides/%s.html">%s</a><p>%s</p></td><td>%s</td><td>%s</td><td>%s</td></tr>' % tuple(escape(str(value), quote=True) for value in (
            doc["category"], searchable.casefold(), prefix, row["slug"], doc["title"], doc["description"],
            doc["category"], doc["updated_on"] or "미표기", doc["reference_date"] or "미표기")))
    categories = sorted({row["document"]["category"] for row in pages["pages"]})
    options = ''.join('<option>%s</option>' % escape(value) for value in categories)
    warnings = (pages.get("runs") or [{}])[0].get("failures", [])
    notice = '<p role="status">일부 원문을 갱신하지 못해 이전 자료를 보존했습니다.</p>' if warnings else ""
    return '<style>%s</style><section class="model-document-library" data-ui-id="model-library"><header><h1>모델 리서치 자료</h1></header><p>Theo의 모델 분석·선택 가이드·비용 비교·벤치마크 해설입니다. 원자료의 수정일·기준일을 보존하며, 가져온 날짜를 독립적인 사실 확인일로 표시하지 않습니다.</p><p><a href="%sai-models.html">전체 모델 비교표</a></p>%s<div class="model-library-tools"><label>자료 검색<input id="model-page-query" type="search" placeholder="모델 이름, 비용, 벤치마크"></label><label>자료 분야<select id="model-page-category"><option value="">전체</option>%s</select></label></div><div class="table-wrapper"><table><thead><tr><th>자료</th><th>분야</th><th>자료 수정일</th><th>원자료 기준일</th></tr></thead><tbody id="model-page-rows">%s</tbody></table></div><p id="model-page-empty" hidden>검색 결과가 없습니다.</p><p id="model-page-count" role="status"></p></section><script>%s</script>' % (
        (ROOT / "model_pages.css").read_text(encoding="utf-8"), escape(prefix), notice, options, ''.join(rows),
        (ROOT / "model_pages.js").read_text(encoding="utf-8"))


def source_document(doc, file_slugs, token):
    """Package same-origin dependencies without changing source facts or scripts.

    The containing iframe grants scripts/downloads but no same-origin storage or
    parent access. CSP blocks fetch, forms and new remote executable dependencies.
    """
    text = doc["html"]
    for path, asset in doc["assets"].items():
        pattern = r'<script\b([^>]*?)\bsrc=["\x27]' + re.escape(path) + r'["\x27]([^>]*)>\s*</script>'
        if path.endswith(".js"):
            text = re.sub(pattern, lambda m: '<script>' + asset.replace('</script', '<\\/script') + '</script>', text, flags=re.I)
        else:
            pattern = r'<link\b[^>]*\bhref=["\x27]' + re.escape(path) + r'["\x27][^>]*>'
            text = re.sub(pattern, lambda m: '<style>' + asset.replace('</style', '<\\/style') + '</style>', text, flags=re.I)
    def link(match):
        url = match.group(2)
        if url.startswith('#'):
            return match.group(0)
        resolved = urljoin(doc["source_url"], url)
        parsed = urlparse(resolved)
        filename = unquote(parsed.path.rsplit('/', 1)[-1])
        slug = file_slugs.get(filename) if parsed.netloc == 'theo-s-han.github.io' else None
        if slug:
            resolved = '../' + slug + '.html' + ('#' + parsed.fragment if parsed.fragment else '')
        return match.group(1) + escape(resolved, quote=True) + match.group(3)
    text = re.sub(r'(\bhref=["\x27])([^"\x27]+)(["\x27])', link, text)
    csp = "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: https:; font-src data:; connect-src 'none'; form-action 'none'; base-uri 'none'"
    shim = """<script>(function(){for(const name of ['localStorage','sessionStorage']){try{window[name].getItem('signal-desk-test')}catch(e){let data={};Object.defineProperty(window,name,{value:{getItem:k=>data[k]??null,setItem:(k,v)=>{data[k]=String(v)},removeItem:k=>delete data[k],clear:()=>{data={}}}})}}})();</script>"""
    text = re.sub(r'(<head\b[^>]*>)', lambda m: m.group(1) + '<meta http-equiv="Content-Security-Policy" content="' + escape(csp, quote=True) + '">' + shim, text, count=1, flags=re.I)
    # Source tables keep their own filters and scroll containers. This additional
    # wrapper makes older wide tables navigable in a narrow embedded document.
    # Changing iframe height repositions the source's fixed filter popup midway
    # through a checkbox click. Freeze while open and debounce shrinking after
    # close; resize on Escape as well. check_model_frames.cjs covers real input.
    bridge = """<style>html,body{max-width:100%;overflow-wrap:anywhere}img,svg{max-width:100%}.signal-source-table{max-width:100%;overflow:auto}a{overflow-wrap:anywhere}</style><script>(()=>{document.querySelectorAll('a[href]').forEach(a=>{if(!a.getAttribute('href').startsWith('#')){a.target='_blank';a.rel='noopener'}});document.querySelectorAll('table').forEach(t=>{const wrap=document.createElement('div');wrap.className='signal-source-table';t.before(wrap);wrap.append(t)});const end=document.createElement('div');document.body.append(end);let previous=0,timer;const send=()=>{clearTimeout(timer);if(document.querySelector('.llm-filter-panel:not([hidden])'))return;const height=Math.max(600,Math.ceil(end.getBoundingClientRect().bottom+window.scrollY+32));const publish=()=>{if(height!==previous&&!document.querySelector('.llm-filter-panel:not([hidden])')){previous=height;parent.postMessage({type:'signal-model-height',token:TOKEN,height},'*')}};if(height<previous)timer=setTimeout(publish,250);else publish()};new ResizeObserver(send).observe(document.body);document.addEventListener('input',()=>requestAnimationFrame(send));document.addEventListener('click',()=>requestAnimationFrame(send));document.addEventListener('keydown',()=>requestAnimationFrame(send));send()})();</script>""".replace('TOKEN', json.dumps(token))
    return re.sub(r'</body>', lambda m: bridge + m.group(0), text, count=1, flags=re.I)


def page_content(row, all_pages, edition=False):
    doc, slug, revision = row["document"], row["slug"], row["revision"]
    token = slug + '-r' + str(revision)
    # Fixed-position menus measure window.innerHeight. For a table application,
    # provide a real, stable viewport instead of a document-sized iframe whose
    # height changes whenever filtering hides rows. Long articles still expand.
    viewport = ' data-fixed-viewport="true"' if 'llm-table-controls.js' in doc['assets'] else ''
    editions = [item for item in all_pages["history"] if item["slug"] == slug]
    links = ''.join('<a href="%s-r%d.html">%d차</a> ' % (slug, item['revision'], item['revision']) for item in sorted(editions, key=lambda item:item['revision'], reverse=True))
    return '<style>%s</style><section class="model-source-heading" data-ui-id="model-source"><header><h1>%s</h1></header><p><a href="../ai-model-guides.html">모델 리서치 자료</a> · <a href="../ai-models.html">전체 모델 비교표</a> · <a href="%s" target="_blank" rel="noopener">Theo 원문</a></p><p>자료 수정일 %s · 원자료 기준일 %s · Theo 작성 자료</p>%s<p class="model-source-editions">이전 기록: %s</p></section><iframe class="model-source-frame"%s title="%s 본문" src="content/%s-r%d.html" sandbox="allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox"></iframe><script>%s</script>' % (
        (ROOT / 'model_pages.css').read_text(encoding='utf-8'), escape(doc['title']), escape(doc['source_url'],quote=True),
        escape(doc['updated_on'] or '미표기'), escape(doc['reference_date'] or '미표기'),
        '<p>이전 판 · <a href="%s.html">현재 자료</a></p>' % slug if edition else '', links, viewport, escape(doc['title'],quote=True), slug, revision,
        """(()=>{const frame=document.querySelector('.model-source-frame');window.addEventListener('message',event=>{const d=event.data;if(!frame.dataset.fixedViewport&&event.source===frame.contentWindow&&d?.type==='signal-model-height'&&d.token===TOKEN&&Number.isFinite(d.height)&&d.height>=600&&d.height<=200000){frame.style.height=d.height+'px'}})})();""".replace('TOKEN',json.dumps(token)))


def render_model_pages(destination, pages, page):
    destination = Path(destination)
    root = destination / 'model-guides'
    content_root = root / 'content'
    content_root.mkdir(parents=True, exist_ok=True)
    file_slugs = {row['document']['file']:row['slug'] for row in pages['pages']}
    for row in pages['history']:
        doc = row['document']
        token = row['slug']+'-r'+str(row['revision'])
        (content_root / (token+'.html')).write_text(source_document(doc,file_slugs,token),encoding='utf-8')
        (root / (token+'.html')).write_text(page(doc['title'],doc['description'],page_content(row,pages,True),'../',active='ai-model-guides'),encoding='utf-8')
    for row in pages['pages']:
        doc = row['document']
        (root / (row['slug']+'.html')).write_text(page(doc['title'],doc['description'],page_content(row,pages),'../',active='ai-model-guides'),encoding='utf-8')
    (destination / 'ai-model-guides.html').write_text(page('모델 리서치 자료','모델별 가이드·비용·평가 자료',library_content(pages),active='ai-model-guides'),encoding='utf-8')
