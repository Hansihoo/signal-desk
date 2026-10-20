"""Direct agent-company watches, independent of the legacy ranked news cap.

Lists discover candidates; excerpts are not authored or independently reviewed news.
Publication dates retain date-only precision. Failed fetches preserve saved items.
"""

import hashlib
import gzip
import io
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zlib
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

from .ai_news import parse_ai_feed
from .db import upsert_news_items
from .timeutil import iso_utc, now_utc, KST

SOURCES = Path(__file__).resolve().parent.parent / 'config/agent_news_sources.json'
MAX_BYTES = 3_000_000


class Node:
    def __init__(self, tag='', attrs=None, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, attrs or {}, parent, []

    def walk(self, tags=None):
        if tags is None or self.tag in tags:
            yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk(tags)

    def text(self):
        if self.tag in ('script', 'style', 'nav', 'footer'):
            return ''
        return re.sub(r'\s+', ' ', ' '.join(c.text() if isinstance(c, Node) else c for c in self.children)).strip()


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = self.current = Node()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs), self.current)
        self.current.children.append(node)
        if tag not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.current.children.append(Node(tag, dict(attrs), self.current))

    def handle_endtag(self, tag):
        n = self.current
        while n.parent and n.tag != tag:
            n = n.parent
        if n.tag == tag and n.parent:
            self.current = n.parent

    def handle_data(self, data):
        self.current.children.append(data)


def _url(value):
    try:
        p = urlsplit(value)
        if p.scheme not in ('http', 'https') or not p.netloc or p.username or p.password:
            return ''
        return urlunsplit((p.scheme, p.netloc, p.path, p.query, ''))
    except (ValueError, TypeError):
        return ''


def load_sources(path=None):
    rows = json.loads(Path(path or SOURCES).read_text(encoding='utf-8'))['sources']
    seen = set()
    for row in rows:
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,47}', row['id']) or row['id'] in seen or not _url(row['url']):
            raise ValueError('Invalid or duplicate agent news source')
        if row['format'] not in ('feed', 'html') or row['kind'] not in ('article', 'release', 'weekly') or row['tier'] not in ('official', 'discovery'):
            raise ValueError('Invalid source format/kind/tier')
        if row['format']=='html' and not row.get('paths'):
            raise ValueError('HTML watches require verified article path prefixes')
        seen.add(row['id'])
    return rows


def published_date(text):
    """Do not invent time zones/times for publishers giving only a calendar date."""
    patterns = [
        (r'\b(20\d{2})-(\d{2})-(\d{2})\b', lambda m: (int(m[1]),int(m[2]),int(m[3]))),
        (r'(20\d{2})년\s*(\d{1,2})월\s*(\d{1,2})일', lambda m: (int(m[1]),int(m[2]),int(m[3]))),
        (r'\b(\d{2})\.(\d{2})\.(\d{2})\b', lambda m: (2000+int(m[1]),int(m[2]),int(m[3])) if int(m[1])>12 else (2000+int(m[3]),int(m[1]),int(m[2]))),
    ]
    for pat, convert in patterns:
        m = re.search(pat, text or '')
        if m:
            try: return date(*convert(m)).isoformat()
            except ValueError: pass
    text = re.sub(r'\b(\d{1,2})\s+([A-Za-z]+)\s+(20\d{2})\b', r'\2 \1, \3', text or '')
    m = re.search(r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2}),?\s+(20\d{2})', text or '', re.I)
    if m:
        month = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'].index(m[1][:3].lower())+1
        try: return date(int(m[3]),month,int(m[2])).isoformat()
        except ValueError: pass
    return ''


def _tree(body):
    p = Tree(); p.feed(body.decode('utf-8','replace') if isinstance(body, bytes) else body)
    return p.root


def parse_listing(body, source, limit=20):
    if source['format']=='feed':
        rows = parse_ai_feed(body, {'id':'ai_agent_'+source['id'], 'name':source['name'],
            'feed_url':source['url'],'home_url':source['url'],'tier':source['tier'],'score_base':160}, limit=limit)
        return [{'url':r['url'], 'title':r['title'], 'published_at':r['published_at'],
                 'excerpt':json.loads(r['raw_payload']).get('detail','')} for r in rows]
    tree, rows, seen = _tree(body), [], set()
    for a in tree.walk({'a'}):
        ancestors=list(_parents(a))
        if any(n.tag in ('nav','footer') for n in ancestors) or (any(n.tag=='header' for n in ancestors) and not any(n.tag in ('article','main') for n in ancestors)):
            continue
        target = _url(urljoin(source['url'], a.attrs.get('href','')))
        if not target or urlsplit(target).netloc!=urlsplit(source['url']).netloc or not any(urlsplit(target).path.startswith(p) for p in source['paths']):
            continue
        if target in seen or urlsplit(target).path.rstrip('/')==urlsplit(source['url']).path.rstrip('/'):
            continue
        if re.search(r'/page/\d+/?$',urlsplit(target).path):
            continue
        heads = list(a.walk({'h1','h2','h3','h4'}))
        context = a
        if not heads:
            for parent in _parents(a):
                # A short article container may place its date outside its link.
                candidates=list(parent.walk({'h1','h2','h3','h4'}))
                if len(candidates)==1 and len(parent.text())<2200:
                    context=parent;heads=candidates;break
                if parent.tag in ('article','li') and len(parent.text())<2200:
                    context=parent;break
                if parent.tag in ('main','body'): break
        title = heads[0].text() if heads else a.text()
        if len(title)<5 or title in ('자세히 보기','원문 보기','Read more','Learn more'):
            continue
        times = [n.attrs.get('datetime') or n.text() for n in context.walk({'time'})]
        when = next((published_date(t) for t in times if published_date(t)), '') or published_date(context.text())
        paras = [n.text() for n in context.walk({'p'}) if n.text()]
        excerpt = ' '.join(paras)
        if not heads and when:
            title = re.sub(r'^(?:[A-Za-z]+ \d{1,2},? 20\d{2}|\d{2}\.\d{2}\.\d{2})\s*','',title)
            title = re.sub(r'^(Announcements|Research|Product|Engineering)\s+', '', title)
        if len(title.strip())<5:
            continue
        if source['tier']=='discovery' and '/releases/' in target:
            m=re.search(re.escape(title)+r'\s+([A-Z][A-Z0-9 -]{2,40})',context.text())
            if m:title=m[1].strip()+' '+title
        rows.append({'url':target,'title':title[:260],'published_at':when,'excerpt':excerpt[:900]})
        seen.add(target)
        if limit is not None and len(rows)>=limit: break
    return rows


def _parents(n):
    while n.parent:
        n=n.parent;yield n


def detail_metadata(body):
    tree = _tree(body)
    meta={n.attrs.get('property') or n.attrs.get('name'):n.attrs.get('content','') for n in tree.walk({'meta'})}
    headings=[n for n in tree.walk({'h1'}) if n.text()]
    when=meta.get('article:published_time','') or meta.get('date','')
    if not when:
        for n in tree.walk({'script'}):
            if n.attrs.get('type')=='application/ld+json':
                raw=''.join(c for c in n.children if isinstance(c,str))
                m=re.search(r'"datePublished"\s*:\s*"([^"]+)"',raw)
                if m: when=m[1];break
    if not when:
        for n in tree.walk({'time'}):
            when=published_date(n.attrs.get('datetime') or n.text())
            if when:break
    if not when:
        # Published dates can be in article headers; prefer explicit publication labels.
        m=re.search(r'(?:Published|Posted)\s+([A-Za-z]+\s+\d{1,2},?\s+20\d{2})',tree.text())
        when=published_date(m[1]) if m else ''
    return {'title':headings[0].text() if headings else meta.get('og:title',''),
            'excerpt':meta.get('description') or meta.get('og:description',''),
            'published_at':published_date(when)}


def ensure_schema(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS agent_news_sources (
        id TEXT PRIMARY KEY, name TEXT NOT NULL, url TEXT NOT NULL, publisher TEXT NOT NULL,
        tier TEXT NOT NULL, attempted_at TEXT NOT NULL, succeeded_at TEXT NOT NULL DEFAULT '',
        error TEXT NOT NULL DEFAULT '', etag TEXT NOT NULL DEFAULT '', modified TEXT NOT NULL DEFAULT '',
        raw_path TEXT NOT NULL DEFAULT '', checksum TEXT NOT NULL DEFAULT '', item_count INTEGER NOT NULL DEFAULT 0)''')


def _fetch(source, old):
    headers={'User-Agent':'SignalDesk/0.1 (+public agent news watch)'}
    if old and old.get('url')==source['url'] and old.get('raw_path') and Path(old['raw_path']).is_file():
        if old.get('etag'):headers['If-None-Match']=old['etag']
        if old.get('modified'):headers['If-Modified-Since']=old['modified']
    try:
        with urllib.request.urlopen(urllib.request.Request(source['url'],headers=headers),timeout=18) as r:
            body=r.read(MAX_BYTES+1)
            if len(body)>MAX_BYTES:raise ValueError('Source exceeds bounded response size')
            # urllib retains compressed bytes. Some publisher/CDN responses omit
            # Content-Encoding, so also recognize the gzip wire signature.
            if r.headers.get('Content-Encoding','').lower()=='gzip' or body.startswith(b'\x1f\x8b'):
                try:
                    with gzip.GzipFile(fileobj=io.BytesIO(body)) as decoded:
                        body=decoded.read(MAX_BYTES+1)
                except (OSError,EOFError,zlib.error) as exc:
                    raise ValueError('Invalid compressed source response') from exc
                if len(body)>MAX_BYTES:raise ValueError('Decoded source exceeds bounded response size')
            return body,r.headers.get('ETag',''),r.headers.get('Last-Modified',''),False
    except urllib.error.HTTPError as exc:
        exc.close()
        if exc.code==304 and old and Path(old.get('raw_path','')).is_file():
            return Path(old['raw_path']).read_bytes(),old.get('etag',''),old.get('modified',''),True
        raise


def collect_agent_news(conn, sources=None, raw_dir='data/raw/agent_news', days=30, per_source=None):
    from .signal_review import impact_priority
    ensure_schema(conn)
    sources=sources if sources is not None else load_sources()
    old={r['id']:dict(r) for r in conn.execute('SELECT * FROM agent_news_sources')}
    totals={'fetched':0,'inserted':0,'updated':0,'failures':[], 'changed':False, 'sources':[]}
    attempted=iso_utc();cutoff=(now_utc()-timedelta(days=days)).date().isoformat()
    with ThreadPoolExecutor(max_workers=6) as pool:
        tasks={s['id']:pool.submit(_fetch,s,old.get(s['id'])) for s in sources}
        for s in sources:
            previous=old.get(s['id'],{})
            try:
                body,etag,modified,revalidated=tasks[s['id']].result()
                rows=parse_listing(body,s,limit=per_source)
                if not rows:raise ValueError('No readable entries; source layout may have changed')
                checksum=hashlib.sha256(body).hexdigest()
                raw=Path(raw_dir)/s['id']/(checksum+('.xml' if s['format']=='feed' else '.html'))
                raw.parent.mkdir(parents=True,exist_ok=True)
                if not raw.exists():raw.write_bytes(body)
                changed=[];metadata_budget=3
                for r in rows:
                    if not _url(r['url']):continue
                    external=hashlib.sha256(r['url'].encode()).hexdigest()
                    existing=conn.execute('SELECT * FROM news_items WHERE source_id=? AND external_id=?',('ai_agent_'+s['id'],external)).fetchone()
                    # Detail metadata supplies missing dates/titles, never fabricated dates.
                    if not r['published_at'] and existing:
                        r['published_at']=existing['published_at']
                    if not r['published_at'] and metadata_budget and s['format']=='html':
                        metadata_budget-=1
                        try:
                            detail,_,_,_=_fetch(dict(s,url=r['url']),{})
                            dp=Path(raw_dir)/s['id']/('detail-'+hashlib.sha256(detail).hexdigest()+'.html')
                            if not dp.exists():dp.write_bytes(detail)
                            for k,v in detail_metadata(detail).items():
                                if v:r[k]=v
                        except (OSError,ValueError) as exc:
                            totals['failures'].append(s['id']+' detail: '+str(exc))
                    if r['published_at'] and r['published_at'][:10]<cutoff:continue
                    if r['published_at'] and r['published_at'][:10]>now_utc().astimezone(KST).date().isoformat():continue
                    kind='weekly' if '/weekly/' in r['url'] else 'release' if '/releases/' in r['url'] else s['kind']
                    excerpt=r.get('excerpt','')
                    if excerpt.startswith('원문 요약이 짧습니다.'):excerpt=''
                    payload={'detail':excerpt,'source_tier':s['tier'],'publisher':s['publisher'],
                        'news_kind':kind,'listing_url':s['url'],'review_status':'source_excerpt'}
                    fingerprint=hashlib.sha256(json.dumps([r['title'],r['published_at'],payload],ensure_ascii=False,sort_keys=True).encode()).hexdigest()
                    if existing and existing['content_hash']==fingerprint:
                        conn.execute('UPDATE news_items SET last_seen_at=? WHERE id=?',(attempted,existing['id']))
                    else:
                        changed.append({'source_id':'ai_agent_'+s['id'],'external_id':external,
                            'title':r['title'],'title_ko':'','url':r['url'],'source_name':s['name'],'source_url':s['url'],
                            'category':'에이전트 소식','published_at':r['published_at'],'summary_ko':excerpt[:900],
                            'score':impact_priority(r['title'],excerpt)['score'],'raw_payload':json.dumps(payload,ensure_ascii=False,sort_keys=True),
                            'content_hash':fingerprint,'collected_at':attempted})
                    totals['fetched']+=1
                stats=upsert_news_items(conn,changed,dedupe_by_title=False)
                totals['inserted']+=stats['inserted'];totals['updated']+=stats['updated']
                values=(s['id'],s['name'],s['url'],s['publisher'],s['tier'],attempted,iso_utc(),'',etag,modified,str(raw),checksum,len(rows))
                state_change=not previous or bool(previous.get('error')) or previous.get('url')!=s['url']
                conn.execute('''INSERT OR REPLACE INTO agent_news_sources
                    (id,name,url,publisher,tier,attempted_at,succeeded_at,error,etag,modified,raw_path,checksum,item_count)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',values)
                totals['changed'] |= bool(changed) or state_change
                totals['sources'].append({'id':s['id'],'ok':True,'count':len(rows),'revalidated':revalidated})
            except (OSError,ValueError,ET.ParseError) as exc:
                message=str(exc)
                totals['failures'].append(s['id']+': '+message)
                conn.execute('''INSERT OR REPLACE INTO agent_news_sources
                    (id,name,url,publisher,tier,attempted_at,succeeded_at,error,etag,modified,raw_path,checksum,item_count)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (s['id'],s['name'],s['url'],s['publisher'],s['tier'],attempted,previous.get('succeeded_at',''),message,
                     previous.get('etag',''),previous.get('modified',''),previous.get('raw_path',''),previous.get('checksum',''),previous.get('item_count',0)))
                totals['changed'] |= not previous or previous.get('error','')!=message
                totals['sources'].append({'id':s['id'],'ok':False,'error':message})
    conn.commit()
    return totals


def export_sources(conn):
    ensure_schema(conn)
    return [dict(r) for r in conn.execute('SELECT id,name,url,publisher,tier,attempted_at,succeeded_at,error,item_count FROM agent_news_sources ORDER BY id')]
