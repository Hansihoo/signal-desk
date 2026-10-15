"""Article prose and source watches, kept separate from quantitative report v1."""

import hashlib
import html
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from .agent_news import _url, export_sources
from .timeutil import iso_utc, KST

ARTICLES = Path(__file__).resolve().parent.parent/'config/newsroom_articles.2026-10-14.json'


def ensure_articles(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS newsroom_articles (
        id TEXT PRIMARY KEY, document TEXT NOT NULL, content_hash TEXT NOT NULL,
        created_at TEXT NOT NULL, updated_at TEXT NOT NULL, revision INTEGER NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS newsroom_article_revisions (
        id TEXT NOT NULL, revision INTEGER NOT NULL, document TEXT NOT NULL,
        content_hash TEXT NOT NULL, saved_at TEXT NOT NULL, PRIMARY KEY(id,revision))''')


def validate_article(a):
    fields={'id','title','deck','publisher','published_on','checked_on','source_url','sections','references'}
    optional={'kind','source_aliases','featured'}
    if not isinstance(a,dict) or not fields<=set(a) or set(a)-fields-optional or not re.fullmatch(r'[a-z][a-z0-9-]{0,79}',a.get('id','')):
        raise ValueError('Invalid article fields or ID')
    if a.get('kind','article') not in ('article','release'):
        raise ValueError('Invalid article kind')
    if 'featured' in a and not isinstance(a['featured'],bool):raise ValueError('Invalid featured flag')
    if not isinstance(a.get('source_aliases',[]),list) or any(not u or _url(u)!=u for u in a.get('source_aliases',[])):
        raise ValueError('Invalid article source alias')
    for key in ('title','deck','publisher'):
        if not isinstance(a[key],str) or not a[key].strip():raise ValueError('Empty article text')
    for key in ('published_on','checked_on'):
        if date.fromisoformat(a[key]).isoformat()!=a[key]:raise ValueError('Invalid article date')
    if _url(a['source_url'])!=a['source_url']:raise ValueError('Invalid article original URL')
    ids=set()
    if not isinstance(a['references'],list) or not a['references']:raise ValueError('Missing article sources')
    for ref in a['references']:
        if set(ref)!={'id','title','url'} or ref['id'] in ids or not ref['title'] or _url(ref['url'])!=ref['url']:
            raise ValueError('Invalid article reference')
        ids.add(ref['id'])
    if a['source_url'] not in [r['url'] for r in a['references']]:raise ValueError('Original must be cited')
    if not isinstance(a['sections'],list) or not a['sections']:raise ValueError('Missing article body')
    for section in a['sections']:
        if set(section)!={'heading','paragraphs'} or not isinstance(section['heading'],str) or not section['paragraphs']:
            raise ValueError('Invalid article section')
        for p in section['paragraphs']:
            if set(p)!={'text','source_ids'} or not isinstance(p['text'],str) or not p['text'].strip() or not p['source_ids'] or set(p['source_ids'])-ids:
                raise ValueError('Each article paragraph needs valid sources')
    return a


def import_articles(conn,path=None):
    rows=json.loads(Path(path or ARTICLES).read_text(encoding='utf-8'))['articles']
    for a in rows:validate_article(a)
    if len({a['id'] for a in rows})!=len(rows):raise ValueError('Duplicate article IDs')
    originals=[url for article in rows for url in _article_urls(article)]
    if len(originals)!=len(set(originals)):raise ValueError('Duplicate article source URLs')
    ensure_articles(conn)
    stats={'inserted':0,'updated':0,'unchanged':0}
    with conn:
        for a in rows:
            document=json.dumps(a,ensure_ascii=False,sort_keys=True)
            digest=hashlib.sha256(document.encode()).hexdigest()
            old=conn.execute('SELECT * FROM newsroom_articles WHERE id=?',(a['id'],)).fetchone()
            if old and old['content_hash']==digest:
                stats['unchanged']+=1;continue
            now=iso_utc();rev=old['revision']+1 if old else 1
            conn.execute('INSERT OR REPLACE INTO newsroom_articles VALUES (?,?,?,?,?,?)',
                         (a['id'],document,digest,old['created_at'] if old else now,now,rev))
            conn.execute('INSERT INTO newsroom_article_revisions VALUES (?,?,?,?,?)',(a['id'],rev,document,digest,now))
            stats['updated' if old else 'inserted']+=1
    return stats


def export_newsroom(conn):
    ensure_articles(conn)
    articles=[dict(json.loads(r['document']),revision=r['revision'],updated_at=r['updated_at']) for r in conn.execute('SELECT * FROM newsroom_articles ORDER BY updated_at DESC,id')]
    history=[{'id':r['id'],'revision':r['revision'],'document':json.loads(r['document'])} for r in conn.execute('SELECT * FROM newsroom_article_revisions ORDER BY id,revision')]
    return {'articles':articles,'history':history,'sources':export_sources(conn)}


def _e(v):return html.escape(str(v),quote=True)


def _date(value):
    if not value:return '발표일 미확인'
    try:
        dt=datetime.fromisoformat(value.replace('Z','+00:00'))
        if dt.tzinfo:return dt.astimezone(KST).strftime('%Y.%m.%d')
    except ValueError:pass
    return _e(value[:10].replace('-','.'))


def _stamp(value):
    try:
        dt=datetime.fromisoformat(value.replace('Z','+00:00'))
        return dt.replace(tzinfo=KST) if dt.tzinfo is None else dt
    except (ValueError,TypeError):return datetime.min.replace(tzinfo=timezone.utc)


def _time(value):
    return _stamp(value).astimezone(KST).strftime('%Y.%m.%d %H:%M KST') if value else '성공 기록 없음'


def source_rows(snapshot):
    rows=[];seen=set()
    earliest={}
    for item in snapshot.get('items',[]):
        value=item.get('first_seen_at')
        if item.get('topic_id')=='ai' and value and _stamp(value).year>1:
            url=item.get('url','')
            if url not in earliest or _stamp(value)<_stamp(earliest[url]):earliest[url]=value
    for item in sorted(snapshot.get('items',[]),key=lambda x:(bool(x.get('published_at')), _stamp(x.get('published_at') or x.get('first_seen_at'))),reverse=True):
        if item.get('topic_id')!='ai' or not _url(item.get('url','')) or item.get('source')=='Theo 모델 리서치':continue
        if item.get('news_tier') not in (None,'','official','official/community','open-source','discovery'):continue
        if not isinstance(item.get('id'),str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}',item['id']):continue
        if item['url'] in seen:continue
        seen.add(item['url'])
        rows.append(dict(item,first_seen_at=earliest.get(item['url'],item.get('first_seen_at',''))))
    return rows


def _story_card(a):
    return '<article class="news-story"><div class="news-meta"><span>%s</span><time datetime="%s">%s</time><span>기사</span></div><h3><a href="articles/%s.html">%s</a></h3><p>%s</p><a class="news-read" href="articles/%s.html">기사 읽기 ↗</a></article>'%(
        _e(a['publisher']),_e(a['published_on']),_date(a['published_on']),_e(a['id']),_e(a['title']),_e(a['deck']),_e(a['id']))


def _source_card(r):
    label='원문' if re.search(r'[가-힣]',r['title']) else '영문 원문'
    excerpt=_source_excerpt(r)
    return '<article class="news-source"><div class="news-meta"><span>%s</span><time>%s</time><span>%s</span></div><h3><a href="%s" target="_blank" rel="noopener noreferrer">%s ↗</a></h3>%s</article>'%(
        _e(r.get('publisher') or r.get('source','')),_date(r.get('published_at')),_e(label),_e(r['url']),_e(r['title']),'<p>'+_e(excerpt)+'</p>' if excerpt else '')


def _source_excerpt(row):
    text=row.get('summary','') or ''
    return '' if any(phrase in text for phrase in ('원문 요약이 짧습니다','원문에서 내용을 읽을 수 있습니다','원문을 열어 확인')) else text


def readable_articles(data):
    """A delivery gate, not a claim that automated checks establish editorial quality."""
    articles=[]
    for article in data.get('articles',[]):
        paragraphs=[p['text'] for s in article.get('sections',[]) for p in s.get('paragraphs',[])]
        if not all(re.search(r'[가-힣]',article.get(k,'')) for k in ('title','deck')):continue
        if len(paragraphs)<3 or len(''.join(paragraphs))<200 or not all(re.search(r'[가-힣]',text) for text in paragraphs):continue
        if any('원문 요약이 짧습니다' in text for text in paragraphs):continue
        articles.append(article)
    return sorted(articles,key=lambda a:(a['published_on'],a['id']),reverse=True)


def _article_kind(article):
    return article.get('kind') or ('release' if '/changelog/' in article['source_url'] else 'article')


def _article_urls(article):
    return {url.rstrip('/') for url in [article['source_url'],*article.get('source_aliases',[])]}


def _home_explore(rows, articles, watches, reports):
    available={r.get('publisher') or r.get('source','') for r in rows}|{a['publisher'] for a in articles}
    watched={s['publisher'] for s in watches if s.get('tier')=='official'}
    order=('OpenAI','Anthropic','Google','Microsoft','Cursor','Cognition','LangChain','Langfuse','A2A Project')
    publishers=sorted((watched & available) or available,key=lambda name:(order.index(name) if name in order else len(order),name))[:9]
    reviewed={a['publisher'] for a in articles}
    companies=''.join('<li><a href="%s?%s">%s%s</a></li>'%('news.html' if name in reviewed else 'news-sources.html',_e(urlencode({'publisher':name})),_e(name),'' if name in reviewed else '<small>원문</small>') for name in publishers)
    topics={}
    for report in reports:
        path=tuple(report['topic_path'][:2])
        topics[path]=topics.get(path,0)+1
    topic_links=''.join('<li><a href="index.html?%s#board"><span>%s</span><small>%d</small></a></li>'%(
        _e(urlencode({'topic':' / '.join(path)})),_e(path[-1]),count)
        for path,count in sorted(topics.items(),key=lambda item:(-item[1],item[0]))[:7])
    return '''<nav class="home-explore" aria-label="기업과 주제 탐색">
      <details open><summary>기업·프로젝트</summary><ul>%s<li><a href="news.html">전체 소식 ↗</a></li></ul></details>
      <details open><summary>리서치 주제</summary><ul>%s<li><a href="#board">전체 보고서 ↘</a></li></ul></details>
    </nav>'''%(companies,topic_links)


def newsroom_home(snapshot, reports=()):
    data=snapshot.get('newsroom',{});articles=readable_articles(data)
    rows=source_rows(snapshot)
    releases=[a for a in articles if _article_kind(a)=='release'][:3]
    featured=([a for a in articles if a.get('featured')]+[a for a in articles if not a.get('featured')])[:3]
    latest=[a for a in articles if a not in featured][:3]
    more=[a for a in articles if a not in featured and a not in latest][:6]
    watches=data.get('sources',[])
    failures=[r for r in watches if r['error']]
    last=max((r['succeeded_at'] for r in watches if r['succeeded_at']),default='')
    status=('최근 탐지 '+_time(last)+' · '+str(len(watches)-len(failures))+'/'+str(len(watches))+'개 경로 확인') if watches else '탐지 이력이 아직 없습니다'
    if failures:status+=' · '+str(len(failures))+'개 경로 확인 실패'
    release_html=''.join('<li><div class="release-meta"><time>%s</time><span>%s</span></div><h3><a href="articles/%s.html">%s</a></h3><p>%s</p></li>'%(
        _date(a['published_on']),_e(a['publisher']),_e(a['id']),_e(a['title']),_e(a['deck']))
        for a in releases) or '<li class="news-empty">변경 내용을 확인한 도구 소식이 등록되면 표시됩니다.</li>'
    card_html=''.join(_story_card(a) for a in featured) or '<p class="news-empty">원문을 검토한 기사가 등록되면 여기에 표시됩니다.</p>'
    latest_html=''.join('<li><div class="release-meta"><time>%s</time><span>%s</span></div><h3><a href="articles/%s.html">%s</a></h3></li>'%(
        _date(a['published_on']),_e(a['publisher']),_e(a['id']),_e(a['title'])) for a in latest) or '<li class="news-empty">추가로 검토한 소식이 등록되면 표시됩니다.</li>'
    discovery_html=''.join(_story_card(a) for a in more)
    return '''<section class="news-masthead"><div class="news-intro"><p class="eyebrow">SIGNAL DESK / AI & AGENTS</p><h1>AI와 에이전트 소식.</h1><p>주요 기업의 발표와 도구 업데이트, 업무에 필요한 맥락을 읽습니다.</p></div>
    <form class="home-news-search" action="news.html" method="get"><label class="sr-only" for="home-news-query">AI 소식 검색</label><input id="home-news-query" type="search" name="q" placeholder="기업·도구·소식 검색"><button type="submit">검색</button></form>
    <nav class="news-nav" aria-label="소식 탐색"><a href="#latest-news">주목할 소식</a><a href="#latest-sources">최신 소식</a><a href="#agent-releases">도구 업데이트</a><a href="#board">리서치 보고서</a><a href="ai-models.html">모델 비교표</a></nav></section>
    <div class="news-front">%s<section id="latest-news"><div class="news-section-title"><h2>주목할 소식</h2><a href="news.html">전체 보기 ↗</a></div><div class="news-stories">%s</div></section>
    <aside class="news-rail" aria-label="최신 소식과 도구 업데이트"><section id="latest-sources"><div class="news-section-title"><h2>최신 소식</h2><a href="news.html">더 보기 ↗</a></div><ol class="release-list latest-list">%s</ol></section><section id="agent-releases"><div class="news-section-title"><h2>도구 업데이트</h2><a href="news.html?kind=release">더 보기 ↗</a></div><ol class="release-list">%s</ol></section><a class="watch-health" href="news.html#watch-status">%s <span>탐지 현황 ↗</span></a></aside></div>
    <section class="news-discoveries"><div class="news-section-title"><h2>더 읽을 소식</h2><a href="news.html">한국어 기사 더 보기 ↗</a></div><div class="news-discovery-grid">%s</div><p class="news-caption"><a href="news-sources.html">새로 탐지한 원문 목록 ↗</a> · 원어 제목으로 제공하며 링크는 출처로 바로 연결됩니다.</p></section>'''%(_home_explore(rows,articles,watches,reports),card_html,latest_html,release_html,_e(status),discovery_html)


def article_body(a,older=None):
    refs={r['id']:i for i,r in enumerate(a['references'],1)}
    sections=''.join('<section>%s%s</section>'%('<h2>'+_e(s['heading'])+'</h2>' if s['heading'] else '',
        ''.join('<p>%s%s</p>'%(_e(p['text']),''.join('<a class="citation" href="#news-ref-%d">[%d]</a>'%(refs[k],refs[k]) for k in p['source_ids'])) for p in s['paragraphs'])) for s in a['sections'])
    previous='<p class="news-history">'+(' · '.join('<a href="%s">%d차 기사</a>'%(_e(url),rev) for rev,url in older))+'</p>' if older else ''
    return '''<article class="article-reader"><a class="article-back" href="../news.html">← 전체 소식</a><header class="article-heading"><div class="news-meta"><span>%s</span><time datetime="%s">원문 발표 %s</time><span>기사</span></div><h1>%s</h1><p class="article-deck">%s</p><p class="article-byline">Signal Desk · 원문 검토 %s</p></header><div class="article-prose">%s</div><footer class="article-sources"><h2>원문과 더 읽을 자료</h2><ol>%s</ol>%s</footer></article>'''%(
        _e(a['publisher']),_e(a['published_on']),_date(a['published_on']),_e(a['title']),_e(a['deck']),_date(a['checked_on']),sections,
        ''.join('<li id="news-ref-%d"><a href="%s" target="_blank" rel="noopener noreferrer">%s ↗</a></li>'%(i,_e(r['url']),_e(r['title'])) for i,r in enumerate(a['references'],1)),previous)


def source_body(r):
    return '''<article class="article-reader"><a class="article-back" href="../news.html">← 전체 소식</a><header class="article-heading"><div class="news-meta"><span>%s</span><time>출처 날짜 %s</time><span>원문 소식</span></div><h1>%s</h1><p class="article-deck">%s</p></header><div class="article-prose"><p class="source-reading-note">원문 목록에서 발견한 자료입니다. 아래 내용은 출처가 제공한 발췌이며 Signal Desk의 검토 기사와 구분합니다.</p><p>처음 발견한 날짜: %s</p><p><a class="button primary" href="%s" target="_blank" rel="noopener noreferrer">원문 읽기 ↗</a></p></div></article>'''%(
        _e(r.get('publisher') or (r.get('source') or '원문')),_date(r.get('published_at')),_e(r['title']),_e(_source_excerpt(r)),_date(r.get('first_seen_at')),_e(r['url']))


def write_news_pages(destination,snapshot,page):
    data=snapshot.get('newsroom',{});articles=data.get('articles',[]);readable=readable_articles(data);rows=source_rows(snapshot)
    root=destination/'articles';root.mkdir(exist_ok=True)
    def write(name,title,body,original=None):
        text=page(title,title,body,'../').replace('<body>','<body class="newsroom-page article-page">',1)
        if original:
            text=text.replace('</head>','<link rel="canonical" href="%s"><meta http-equiv="refresh" content="0;url=%s"></head>'%(_e(original),_e(original)),1)
        (root/(name+'.html')).write_text(text,encoding='utf-8')
    for a in readable:
        history=[r for r in data.get('history',[]) if r['id']==a['id'] and r['revision']<a['revision']]
        write(a['id'],a['title'],article_body(a,[(r['revision'],a['id']+'-r'+str(r['revision'])+'.html') for r in history]))
        for r in history:write(a['id']+'-r'+str(r['revision']),r['document']['title'],article_body(r['document']))
    by_original={url:a for a in readable for url in _article_urls(a)}
    for r in rows:
        article=by_original.get(r['url'].rstrip('/'))
        write(r['id'],article['title'] if article else r['title'],article_body(article) if article else source_body(r),None if article else r['url'])
    # Old numeric links may belong to a source alias hidden by list deduplication.
    for r in snapshot.get('items',[]):
        article=by_original.get(r.get('url','').rstrip('/'))
        if article and r.get('topic_id')=='ai' and re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}',str(r.get('id',''))):
            write(r['id'],article['title'],article_body(article))
    items=[]
    for a in readable:
        card='<div class="news-index-item" data-kind="%s" data-publisher="%s" data-news-search="%s">%s</div>'%(
            _article_kind(a),_e(a['publisher']),_e((a['title']+' '+a['deck']+' '+a['publisher']).lower()),_story_card(a))
        items.append((_stamp(a['published_on']),card))
    sources=[]
    for r in rows:
        if r['url'].rstrip('/') in by_original:continue
        kind=r.get('news_kind') or ('release' if '/releases/tag/' in r['url'] else 'article')
        publisher=r.get('publisher') or r.get('source') or '원문'
        card='<div class="news-index-item" data-kind="%s" data-publisher="%s" data-news-search="%s">%s</div>'%(
            _e(kind),_e(publisher),_e((r['title']+' '+_source_excerpt(r)+' '+publisher).lower()),_source_card(r))
        sources.append((_stamp(r.get('published_at')),card))
    items.sort(key=lambda x:x[0],reverse=True)
    publishers=sorted({a['publisher'] for a in articles}|{r.get('publisher') or r.get('source') or '원문' for r in rows})
    health=''.join('<li><div><strong>%s</strong><span>%s</span></div><p>%s</p><small>최근 시도 %s / 최근 성공 %s</small><a href="%s">출처 ↗</a></li>'%(
        _e(s['name']),'확인 실패' if s['error'] else '목록 확인',_e(s['error'] or str(s['item_count'])+'개 목록 항목 확인'),
        _time(s['attempted_at']),_time(s['succeeded_at']),_e(s['url'])) for s in data.get('sources',[]))
    options=''.join('<option value="%s">%s</option>'%(_e(name),_e(name)) for name in publishers)
    template="""<section class="news-index" id="news-index"><p class="eyebrow">NEWSROOM</p><h1>%s</h1>
    <nav class="news-nav" aria-label="기사와 원문"><a href="news.html">한국어 기사</a><a href="news-sources.html">원문 탐지</a></nav><p>%s</p>
    <form class="news-tools">
      <label><span class="sr-only">소식 검색</span><input name="news-query" type="search" placeholder="기업, 도구, 내용 검색"></label>
      <label><span class="sr-only">소식 종류</span><select name="news-kind"><option value="">모든 소식</option><option value="article">기사와 발표</option><option value="release">도구 업데이트</option><option value="weekly">위클리</option></select></label>
      <label><span class="sr-only">기업 또는 출처</span><select name="news-publisher"><option value="">모든 기업과 출처</option>%s</select></label>
      <button type="submit">검색</button>
    </form><div class="news-index-list">%s</div><p class="news-empty" hidden>해당 조건의 소식이 없습니다.</p>
    <nav class="news-pagination" aria-label="소식 목록 페이지" hidden><button type="button" data-news-page="previous">이전</button><span aria-live="polite"></span><button type="button" data-news-page="next">다음</button></nav></section>
    <section id="watch-status"><div class="news-section-title"><h2>탐지 현황</h2></div>
    <p>목록 수집 성공은 원문 전체 검토를 뜻하지 않습니다. 확인에 실패해도 이전 자료와 마지막 성공 시각을 보존합니다.</p>
    <ul class="watch-list">%s</ul></section>"""
    for filename,title,description,entries in (
        ('news.html','AI 소식','원문을 읽고 변화와 사용 조건을 정리한 한국어 기사입니다.',items),
        ('news-sources.html','탐지한 원문','공식 발표와 릴리즈를 원어 제목으로 제공합니다. 한국어 기사가 없는 항목은 출처로 바로 연결됩니다.',sources)):
        names=sorted({a['publisher'] for a in readable}) if filename=='news.html' else publishers
        options=''.join('<option value="%s">%s</option>'%(_e(name),_e(name)) for name in names)
        body=template%(title,description,options,''.join(item for _,item in sorted(entries,key=lambda item:item[0],reverse=True)),health or '<li>아직 탐지를 실행하지 않았습니다.</li>')
        if filename=='news.html':body=body.replace('<option value="weekly">위클리</option>','')
        (destination/filename).write_text(page(title,title,body,active='news').replace('<body>','<body class="newsroom-page">',1),encoding='utf-8')
