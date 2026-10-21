"""Fast, local preparation of verified public business/peer listing candidates.

This is acquisition only: no article, eligibility verdict, alert or publication.
The report/model DB is never opened. Browser-only routes stay explicit gaps.
"""
import argparse
import hashlib
import json
import re
import sqlite3
import subprocess
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit

from .agent_news import _fetch, _tree, parse_listing
from .signal_review import canonical_url
from .timeutil import iso_utc

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / 'config/daily_research_sources.json'
DATABASE = ROOT / 'data/daily-research.sqlite'
RAW = ROOT / 'data/raw/daily_research'
MODES = {'feed', 'html', 'nipa_table', 'bizinfo_table', 'browser'}


def load_catalog(path=CATALOG):
    path = Path(path)
    catalog = json.loads(path.read_text(encoding='utf-8'))
    if catalog.get('schema_version') != 1:
        raise ValueError('Unsupported daily-research catalog')
    refs = {s['id']: s for s in json.loads((ROOT / catalog['business_source_catalog']).read_text(encoding='utf-8'))['sources']}
    seen = set()
    for source in catalog['sources']:
        if source.get('source_ref'):
            original = refs[source['source_ref']]
            source.update(name=original['name'], url=original['url'])
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,47}', source['id']) or source['id'] in seen:
            raise ValueError('Invalid/duplicate daily source ID')
        if source['mode'] not in MODES or not source.get('coverage') or not source.get('browser_task'):
            raise ValueError('Each source requires a supported mode, coverage and follow-up task')
        canonical_url(source['url'])
        if source['mode'] == 'html' and not source.get('paths'):
            raise ValueError('HTML sources require verified article paths')
        seen.add(source['id'])
    return catalog


def parse_source(body, source):
    if source['mode'] == 'browser':
        raise ValueError('This route requires a real browser review')
    if source['mode'] in ('feed', 'html'):
        params = dict(source, format=source['mode'], kind='article', tier='official')
        rows = parse_listing(body, params, limit=None)
        return [{k: row.get(k, '') for k in ('url', 'title', 'published_at')} for row in rows]
    rows = []
    for tr in _tree(body).walk({'tr'}):
        cells = [n for n in tr.children if getattr(n, 'tag', '') == 'td']
        links = list(tr.walk({'a'}))
        for a in links:
            target = urljoin(source['url'], a.attrs.get('href', ''))
            p = urlsplit(target)
            if p.hostname != urlsplit(source['url']).hostname:
                continue
            title = a.text().strip()
            if source['mode'] == 'nipa_table' and re.fullmatch(r'/home/2-2/\d+', p.path) and len(cells) >= 5:
                # Ignore D-day counters, row numbers, views and staff names.
                period = re.search(r'신청기간\s*:\s*(.+)', cells[2].text())
                rows.append({'url': target, 'title': title, 'published_at': cells[-1].text(),
                             'period': period[1] if period else '', 'context': ''})
            elif source['mode'] == 'bizinfo_table' and p.path.endswith('/selectSIIA200Detail.do') and len(cells) >= 7:
                key = parse_qs(p.query).get('pblancId', [''])[0]
                if not re.fullmatch(r'PBLN_[0-9]+', key):
                    continue
                # Search form state is not the notice identity. Views are volatile.
                url = urlunsplit((p.scheme, p.netloc, p.path, urlencode({'pblancId': key}), ''))
                rows.append({'url': url, 'title': title, 'published_at': cells[6].text(),
                             'period': cells[3].text(), 'context': cells[1].text() + ' / ' + cells[4].text() + ' / ' + cells[5].text()})
    return rows


def ensure_schema(conn):
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS daily_source_state (
      id TEXT PRIMARY KEY, url TEXT NOT NULL, attempted_at TEXT NOT NULL,
      succeeded_at TEXT NOT NULL, status TEXT NOT NULL, error TEXT NOT NULL,
      etag TEXT NOT NULL, modified TEXT NOT NULL, raw_path TEXT NOT NULL,
      checksum TEXT NOT NULL, item_count INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS daily_candidates (
      source_id TEXT NOT NULL, url TEXT NOT NULL, document TEXT NOT NULL,
      fingerprint TEXT NOT NULL, first_seen_at TEXT NOT NULL, last_seen_at TEXT NOT NULL,
      changed_at TEXT NOT NULL, change_kind TEXT NOT NULL,
      PRIMARY KEY(source_id,url));
    CREATE TABLE IF NOT EXISTS daily_candidate_editions (
      source_id TEXT NOT NULL, url TEXT NOT NULL, fingerprint TEXT NOT NULL,
      observed_at TEXT NOT NULL, document TEXT NOT NULL,
      PRIMARY KEY(source_id,url,fingerprint));
    ''')


def collect(conn, catalog, raw_dir=RAW, fetcher=_fetch, now=None, max_age_minutes=30):
    ensure_schema(conn)
    now = now or iso_utc()
    old = {row['id']: dict(row) for row in conn.execute('SELECT * FROM daily_source_state')}
    result = {'baseline': 0, 'new': 0, 'changed': 0, 'cached': 0, 'sources': [],
              'coverage': 'provided listings only; originals, attachments, pagination/search and browser routes still require review'}
    work = []
    for s in catalog['sources']:
        previous = old.get(s['id'], {})
        if s['mode'] == 'browser':
            result['sources'].append({'id': s['id'], 'status': 'browser_required', 'url': s['url'], 'task': s['browser_task']})
            continue
        if previous.get('status') == 'ok' and previous.get('url') == s['url'] and previous.get('succeeded_at'):
            age = datetime.fromisoformat(now) - datetime.fromisoformat(previous['succeeded_at'])
            if timedelta(0) <= age < timedelta(minutes=max_age_minutes):
                result['cached'] += 1
                result['sources'].append({'id': s['id'], 'status': 'cached', 'succeeded_at': previous['succeeded_at'], 'count': previous['item_count']})
                continue
        work.append(s)
    with ThreadPoolExecutor(max_workers=4) as pool:
        tasks = {s['id']: pool.submit(fetcher, s, old.get(s['id'])) for s in work}
        for s in work:
            previous = old.get(s['id'], {})
            counts = {'baseline': 0, 'new': 0, 'changed': 0}
            conn.execute('SAVEPOINT daily_source')
            try:
                body, etag, modified, revalidated = tasks[s['id']].result()
                checksum = hashlib.sha256(body).hexdigest()
                raw = Path(raw_dir) / s['id'] / (checksum + ('.xml' if s['mode'] == 'feed' else '.html'))
                raw.parent.mkdir(parents=True, exist_ok=True)
                if not raw.exists():
                    raw.write_bytes(body)
                receipt = dict(url=s['url'], acquired_at=now, sha256=checksum, raw_path=str(raw), revalidated=revalidated)
                receipt_path = raw.parent / (now.replace(':', '').replace('+', '-') + '-' + checksum[:12] + '.receipt.json')
                if not receipt_path.exists():
                    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
                rows = parse_source(body, s)
                if not rows:
                    raise ValueError('No readable entries; browser/parser check required, not unchanged')
                first_snapshot = not previous.get('succeeded_at') or previous.get('url') != s['url']
                seen = set()
                for row in rows:
                    url = canonical_url(row['url'])
                    if url in seen or not row['title'].strip():
                        continue
                    seen.add(url)
                    document = {k: row.get(k, '') for k in ('title', 'published_at', 'period', 'context')}
                    document.update(url=url, source_id=s['id'], source_name=s['name'], area=s['area'])
                    encoded = json.dumps(document, ensure_ascii=False, sort_keys=True)
                    fingerprint = hashlib.sha256(encoded.encode()).hexdigest()
                    existing = conn.execute('SELECT * FROM daily_candidates WHERE source_id=? AND url=?', (s['id'], url)).fetchone()
                    if existing and existing['fingerprint'] == fingerprint:
                        conn.execute('UPDATE daily_candidates SET last_seen_at=? WHERE source_id=? AND url=?', (now, s['id'], url))
                        continue
                    kind = 'changed' if existing else 'baseline' if first_snapshot else 'new'
                    first = existing['first_seen_at'] if existing else now
                    conn.execute('INSERT OR REPLACE INTO daily_candidates VALUES (?,?,?,?,?,?,?,?)', (s['id'], url, encoded, fingerprint, first, now, now, kind))
                    conn.execute('INSERT OR IGNORE INTO daily_candidate_editions VALUES (?,?,?,?,?)', (s['id'], url, fingerprint, now, encoded))
                    counts[kind] += 1
                if not seen:
                    raise ValueError('No valid listing entries; not unchanged')
                conn.execute('INSERT OR REPLACE INTO daily_source_state VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                             (s['id'], s['url'], now, now, 'ok', '', etag, modified, str(raw), checksum, len(seen)))
                conn.execute('RELEASE daily_source')
                for kind, count in counts.items():
                    result[kind] += count
                result['sources'].append({'id': s['id'], 'status': 'listing_only', 'count': len(seen), 'revalidated': revalidated, 'sha256': checksum})
            except (OSError, ValueError, ET.ParseError) as exc:
                conn.execute('ROLLBACK TO daily_source')
                conn.execute('RELEASE daily_source')
                # Keep validators and raw bytes bound to their last successful URL.
                # A failed move must never apply the old ETag to the new address.
                conn.execute('INSERT OR REPLACE INTO daily_source_state VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                             (s['id'], previous.get('url', s['url']), now, previous.get('succeeded_at', ''), 'failed', str(exc),
                              previous.get('etag', ''), previous.get('modified', ''), previous.get('raw_path', ''), previous.get('checksum', ''), previous.get('item_count', 0)))
                result['sources'].append({'id': s['id'], 'url': s['url'], 'status': 'failed', 'error': str(exc), 'last_success': previous.get('succeeded_at', '')})
    conn.commit()
    return result


def queue(conn, limit=24, include_baseline=False):
    rows = []
    for item in conn.execute('SELECT * FROM daily_candidates ORDER BY changed_at DESC,source_id,url'):
        if item['change_kind'] == 'baseline' and not include_baseline:
            continue
        doc = json.loads(item['document'])
        doc.update(change_kind=item['change_kind'], first_seen_at=item['first_seen_at'],
                   observed_at=item['last_seen_at'], changed_at=item['changed_at'])
        text = doc['title'] + ' ' + doc['context']
        doc['triage_hint'] = sum(bool(re.search(p, text, re.I)) for p in
                                [r'문서|오피스|document|office|pdf', r'AI|AX|에이전트|agent|지식|데이터|SaaS',
                                 r'정정|연장|마감|종료|보안|security', r'공공|공급|제휴|파트너|인수|partner|acqui'])
        rows.append(doc)
    # Revalidation does not make an old change new. Give each publisher/source
    # a slot so one long feed cannot bury government notices or unknown peers.
    rows.sort(key=lambda x: (x['changed_at'], x['triage_hint']), reverse=True)
    buckets = {}
    for row in rows:
        buckets.setdefault(row['source_id'], []).append(row)
    selected = []
    while any(buckets.values()) and len(selected) < limit:
        for bucket in buckets.values():
            if bucket and len(selected) < limit:
                selected.append(bucket.pop(0))
    return {'total': len(rows), 'items': selected, 'meaning': 'unreviewed listing observations; new means newly observed, not verified new launch'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'collect', 'queue'])
    parser.add_argument('--limit', type=int, default=24)
    parser.add_argument('--include-baseline', action='store_true')
    parser.add_argument('--force', action='store_true', help='revalidate even a recent successful listing')
    args = parser.parse_args(argv)
    if args.limit < 1:
        parser.error('--limit must be positive')
    catalog = load_catalog()
    if args.command == 'plan':
        output = catalog
    elif args.command == 'collect':
        # Same exact-root/account/remote guard as all project writes, including cache.
        subprocess.run(['git', '-C', str(ROOT), 'signal-gh', 'verify'], check=True, capture_output=True, text=True)
        DATABASE.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(DATABASE)) as conn:
            conn.row_factory = sqlite3.Row
            output = collect(conn, catalog, max_age_minutes=0 if args.force else 30)
    elif not DATABASE.is_file():
        output = {'total': 0, 'items': [], 'status': 'not_collected', 'manual_sources': [s for s in catalog['sources'] if s['mode'] == 'browser']}
    else:
        with closing(sqlite3.connect(DATABASE.as_uri() + '?mode=ro', uri=True)) as conn:
            conn.row_factory = sqlite3.Row
            output = queue(conn, args.limit, args.include_baseline)
            output['sources'] = [dict(r) for r in conn.execute('SELECT id,url,attempted_at,succeeded_at,status,error,item_count FROM daily_source_state')]
            output['manual_sources'] = [s for s in catalog['sources'] if s['mode'] == 'browser']
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return int(any(s.get('status') == 'failed' for s in output.get('sources', [])))


if __name__ == '__main__':
    raise SystemExit(main())
