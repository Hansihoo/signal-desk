"""Public signal inbox: acquisition, impact triage, original review and alert outbox.

Rules estimate review priority, never truth or actual product performance. All received
in-window candidates survive; only the worklist/display is limited. No paid API is used.
"""
import argparse
import hashlib
import json
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .timeutil import iso_utc

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'config/signal_review_publication.json'
RULE_VERSION = 'impact-1'


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def canonical_url(url):
    p = urlsplit(url)
    if p.scheme not in ('https', 'http') or not p.hostname or p.username or p.password:
        raise ValueError('A public HTTP(S) original URL is required')
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not k.lower().startswith('utm_') and k.lower() not in ('ref', 'source', 'fbclid', 'gclid')]
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/') or '/', urlencode(sorted(query)), ''))


def impact_priority(title, excerpt=''):
    """A transparent queue heuristic. Unknown names receive a review slot too."""
    text = (title + ' ' + excerpt[:2500]).lower()
    score, reasons = 20, ['새 이름도 제외하지 않는 기본 검토']
    groups = [
        (r'reverse.engineer|역공학|역분석|binary analysis|바이너리|decompil|디컴파일|computer.use|browser.agent|code.execution', 30, '새 업무 수행 방식'),
        (r'agent|에이전트|coding|코딩|developer|개발자|rag\b|retrieval|knowledge|지식|ontology|온톨로지|workflow|워크플로|document|문서', 15, '개발·운영·지식 업무 영향'),
        (r'launch|introduc|unveil|open.source|new tool|add.{0,50}provider|새로운|출시|공개|신규|connects|통합|지원', 20, '새 제공·연결·기능 후보'),
        (r'benchmark|measur|validat|case stud|실측|검증|사례|reconstruct|복원|porting', 15, '평가·구현·검증 사례'),
        (r'pricing|price cut|license|licenc|가격|요금|라이선스|채용|layoff|workforce', 15, '비용·권리·조직 판단 영향'),
    ]
    for pattern, weight, reason in groups:
        if re.search(pattern, text):
            score += weight
            reasons.append(reason)
    if re.search(r'critical vulnerab|security incident|breach|data leak|end.of.life|shutdown|보안 사고|유출|서비스 종료|지원 종료|철회', title, re.I):
        score += 50; reasons.append('제목에 명시된 긴급 위험·종료·철회 후보')
    if re.search(r'breaking changes|migration (?:notes|required)|호환성.*변경|마이그레이션 필요', excerpt, re.I):
        score += 25; reasons.append('호환성 변경·이전 조건 확인 필요')
    if re.fullmatch(r'(?:[\w.-]+(?::\s*|==))?v?\d+(?:\.\d+){1,3}(?:[-+].*)?', title.strip(), re.I):
        score -= 15
        reasons.append('버전명만 있는 항목; 의미 검토 필요')
    return {'score': min(100, max(5, score)), 'reasons': reasons, 'rule_version': RULE_VERSION}


def ensure_schema(conn):
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS signal_candidates (
      id TEXT PRIMARY KEY, url TEXT NOT NULL, title TEXT NOT NULL, excerpt TEXT NOT NULL,
      fingerprint TEXT NOT NULL, published_at TEXT NOT NULL, first_seen_at TEXT NOT NULL,
      last_seen_at TEXT NOT NULL, priority INTEGER NOT NULL, reasons TEXT NOT NULL,
      source_ids TEXT NOT NULL, revision INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS signal_reviews (
      id TEXT PRIMARY KEY, candidate_id TEXT NOT NULL, fingerprint TEXT NOT NULL,
      reviewed_at TEXT NOT NULL, decision TEXT NOT NULL, event_key TEXT NOT NULL,
      recheck_after TEXT NOT NULL, document TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS signal_candidate_editions (
      candidate_id TEXT NOT NULL, fingerprint TEXT NOT NULL, document TEXT NOT NULL,
      PRIMARY KEY(candidate_id,fingerprint));
    CREATE TABLE IF NOT EXISTS signal_alerts (
      id TEXT PRIMARY KEY, review_id TEXT NOT NULL, created_at TEXT NOT NULL,
      acknowledged_at TEXT NOT NULL DEFAULT '', receipt TEXT NOT NULL DEFAULT '');
    CREATE TABLE IF NOT EXISTS signal_review_batches (id TEXT PRIMARY KEY, content_hash TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS signal_feed_health (
      id TEXT PRIMARY KEY, url TEXT NOT NULL, attempted_at TEXT NOT NULL,
      succeeded_at TEXT NOT NULL, error TEXT NOT NULL, received INTEGER NOT NULL);
    ''')


def sync_candidates(conn):
    ensure_schema(conn)
    groups = {}
    for row in conn.execute("SELECT * FROM news_items WHERE source_id LIKE 'ai_%' ORDER BY first_seen_at,id"):
        row = dict(row)
        try:
            url = canonical_url(row['url'])
        except ValueError:
            continue
        try:
            payload = json.loads(row.get('raw_payload') or '{}')
            if not isinstance(payload, dict): payload = {}
        except (ValueError, TypeError):
            payload = {}
        text = payload.get('detail', '')
        if not isinstance(text, str): text = ''
        group = groups.setdefault(url, {'rows': [], 'excerpt': '', 'title': row['title']})
        group['rows'].append(row)
        if len(text) > len(group['excerpt']):
            group['excerpt'], group['title'] = text, row['title']
    changed = 0
    for url, group in groups.items():
        rows = group['rows']
        observations = []
        for r in rows:
            try: detail = json.loads(r.get('raw_payload') or '{}').get('detail', '')
            except (ValueError, AttributeError): detail = ''
            if not isinstance(detail, str): detail = ''
            observations.append((r['title'], re.sub(r'\s+', ' ', detail).strip()))
        observations = sorted(set(observations))
        fingerprint = digest(observations)
        group['excerpt'] = '\n\n'.join(dict.fromkeys(text for _, text in observations if text))
        key = hashlib.sha256(url.encode()).hexdigest()[:24]
        old = conn.execute('SELECT * FROM signal_candidates WHERE id=?', (key,)).fetchone()
        priority = impact_priority(group['title'], group['excerpt'])
        full_excerpt = group['excerpt']
        breaking = re.search(r'breaking changes|migration notes', full_excerpt, re.I)
        group['excerpt'] = full_excerpt[:2400]
        if breaking and breaking.start() >= 2400:
            group['excerpt'] += '\n[원문 이전 조건 발췌]\n' + full_excerpt[breaking.start():breaking.start()+1400]
        first = min(r['first_seen_at'] for r in rows)
        last = max(r['last_seen_at'] for r in rows)
        if old:
            first = min(first, old['first_seen_at'])
            # A remote backlog may contain a newer observation than local feeds.
            if old['last_seen_at'] > last:
                continue
        published = min((r['published_at'] for r in rows if r['published_at']), default='')
        revision = (old['revision'] + int(old['fingerprint'] != fingerprint)) if old else 1
        values = (key, url, group['title'], group['excerpt'], fingerprint, published, first, last,
                  priority['score'], json.dumps(priority, ensure_ascii=False),
                  json.dumps(sorted({r['source_id'] for r in rows})), revision)
        changed += int(not old or old['fingerprint'] != fingerprint)
        conn.execute('INSERT OR REPLACE INTO signal_candidates VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', values)
        current = dict(conn.execute('SELECT * FROM signal_candidates WHERE id=?', (key,)).fetchone())
        conn.execute('INSERT OR IGNORE INTO signal_candidate_editions VALUES (?,?,?)',
                     (key, fingerprint, json.dumps(current, ensure_ascii=False)))
    conn.commit()
    return changed


def worklist(conn, limit=12, now=None):
    ensure_schema(conn)
    now = now or iso_utc()
    pending = []
    for row in conn.execute('SELECT * FROM signal_candidates ORDER BY priority DESC, first_seen_at, id'):
        item = dict(row)
        review = conn.execute('SELECT * FROM signal_reviews WHERE candidate_id=? AND fingerprint=? ORDER BY reviewed_at DESC,id DESC LIMIT 1',
                              (item['id'], item['fingerprint'])).fetchone()
        if review and (not review['recheck_after'] or datetime.fromisoformat(review['recheck_after'].replace('Z', '+00:00')) > datetime.fromisoformat(now.replace('Z', '+00:00'))):
            continue
        item['previous_review'] = json.loads(review['document']) if review else None
        item['reasons'] = json.loads(item['reasons'])
        item['source_ids'] = json.loads(item['source_ids'])
        item['state'] = 'recheck_due' if review else 'review_not_performed'
        item['prior_editions'] = [json.loads(r[0]) for r in conn.execute(
            'SELECT document FROM signal_candidate_editions WHERE candidate_id=? AND fingerprint!=?',
            (item['id'], item['fingerprint']))]
        pending.append(item)
    if limit is None or len(pending) <= limit:
        return pending
    if limit < 3:
        return pending[:limit]
    # Protect both newly seen unknown subjects and old backlog from keyword bias.
    reserve = max(1, limit // 4)
    selected = pending[:limit - reserve * 2]
    used = {r['id'] for r in selected}
    fresh = [r for r in pending if r['id'] not in used and r['priority'] <= 50]
    if len(fresh) < reserve:
        fresh = [r for r in pending if r['id'] not in used]
    selected += sorted(fresh, key=lambda r: (r['first_seen_at'], r['id']), reverse=True)[:reserve]
    used = {r['id'] for r in selected}
    selected += sorted((r for r in pending if r['id'] not in used), key=lambda r: (r['first_seen_at'], r['id']))[:limit-len(selected)]
    return selected


def validate_review(review, conn, require_receipts=False):
    for field in ('candidate_id', 'fingerprint', 'candidate_url', 'candidate_title', 'decision', 'event_key',
                  'event_change', 'reviewed_at', 'novelty', 'summary', 'impact', 'reason'):
        if not isinstance(review.get(field), str) or not review[field].strip():
            raise ValueError('Missing review field: ' + field)
    canonical_url(review['candidate_url'])
    if not re.fullmatch(r'[a-f0-9]{24}', review['candidate_id']) or not re.fullmatch(r'[a-f0-9]{64}', review['fingerprint']):
        raise ValueError('Invalid candidate identity/fingerprint')
    if review['candidate_id'] != hashlib.sha256(canonical_url(review['candidate_url']).encode()).hexdigest()[:24]:
        raise ValueError('Candidate URL does not match identity')
    if require_receipts:
        current = conn.execute('SELECT * FROM signal_candidates WHERE id=?', (review['candidate_id'],)).fetchone()
        if not current or current['fingerprint'] != review['fingerprint']:
            raise ValueError('Review does not bind the current candidate edition')
    if not re.fullmatch(r'[a-z0-9][a-z0-9._-]{2,160}', review['event_key']):
        raise ValueError('Stable event_key required')
    if review['decision'] not in ('important', 'already_known', 'duplicate', 'out_of_scope', 'follow_up', 'unconfirmed'):
        raise ValueError('Invalid decision')
    if review['novelty'] not in ('new_tool', 'capability_change', 'incident', 'policy_change', 'existing_story'):
        raise ValueError('Invalid novelty')
    reviewed = datetime.fromisoformat(review['reviewed_at'].replace('Z', '+00:00'))
    if reviewed.tzinfo is None:
        raise ValueError('Review timestamp needs a timezone')
    if review.get('recheck_after'):
        due = datetime.fromisoformat(review['recheck_after'].replace('Z', '+00:00'))
        if due.tzinfo is None or due <= reviewed:
            raise ValueError('Recheck must follow actual review')
    if review['decision'] in ('follow_up', 'unconfirmed') and not review.get('recheck_after'):
        raise ValueError('Deferred/failed originals need a recheck time')
    if review['decision'] == 'important' and review['novelty'] == 'existing_story':
        raise ValueError('Existing story must not create a new-event alert')
    evidence = review.get('evidence', [])
    if review['decision'] in ('important', 'already_known') and not any(e.get('role') == 'primary' for e in evidence):
        raise ValueError('Primary original evidence is required')
    for item in evidence:
        canonical_url(item['url'])
        if item.get('role') not in ('primary', 'discovery') or not item.get('finding'):
            raise ValueError('Evidence scope/finding required')
        acquired = datetime.fromisoformat(item['checked_at'].replace('Z', '+00:00'))
        if acquired.tzinfo is None or acquired > reviewed:
            raise ValueError('Evidence must actually precede review')
        if not re.fullmatch(r'[0-9a-f]{64}', item.get('sha256', '')):
            raise ValueError('Original content hash required')
        if require_receipts:
            receipt = ROOT / item.get('receipt', '')
            if ROOT / 'data/raw/signal_review' not in receipt.resolve().parents:
                raise ValueError('Receipt must belong to the public signal evidence store')
            saved = json.loads(receipt.read_text(encoding='utf-8'))
            raw = ROOT / saved['raw_path']
            if ROOT / 'data/raw/signal_review' not in raw.resolve().parents:
                raise ValueError('Invalid raw path')
            if saved['url'] != item['url'] or saved['sha256'] != item['sha256'] or saved['checked_at'] != item['checked_at']:
                raise ValueError('Review does not match acquisition receipt')
            if hashlib.sha256(raw.read_bytes()).hexdigest() != item['sha256']:
                raise ValueError('Original bytes changed')


def import_reviews(conn, document, require_receipts=False):
    ensure_schema(conn)
    if document.get('schema_version') != 1 or not isinstance(document.get('reviews'), list):
        raise ValueError('Expected review batch v1')
    for review in document['reviews']:
        validate_review(review, conn, require_receipts)
    for ack in document.get('acknowledgements', []):
        if not re.fullmatch(r'[a-f0-9]{24}', ack.get('alert_id', '')) or not ack.get('receipt'):
            raise ValueError('Actual user-visible alert receipt required')
        when = datetime.fromisoformat(ack['acknowledged_at'].replace('Z', '+00:00'))
        if when.tzinfo is None: raise ValueError('Alert receipt needs timezone')
    inserted = 0
    with conn:
        for review in document['reviews']:
            key = digest(review)
            inserted += conn.execute('INSERT OR IGNORE INTO signal_reviews VALUES (?,?,?,?,?,?,?,?)',
                (key, review['candidate_id'], review['fingerprint'], review['reviewed_at'], review['decision'],
                 review['event_key'], review.get('recheck_after', ''), json.dumps(review, ensure_ascii=False))).rowcount
            if review['decision'] == 'important':
                alert_key = digest([review['event_key'], review['event_change']])[:24]
                conn.execute('INSERT OR IGNORE INTO signal_alerts(id,review_id,created_at) VALUES (?,?,?)',
                             (alert_key, key, review['reviewed_at']))
        for ack in document.get('acknowledgements', []):
            if not conn.execute('SELECT id FROM signal_alerts WHERE id=?', (ack['alert_id'],)).fetchone():
                raise ValueError('Cannot acknowledge a nonexistent alert')
            conn.execute("UPDATE signal_alerts SET acknowledged_at=?,receipt=? WHERE id=? AND acknowledged_at=''",
                         (ack['acknowledged_at'], ack['receipt'], ack['alert_id']))
    return inserted


def apply_publication(conn, path=MANIFEST):
    ensure_schema(conn)
    path = Path(path)
    if not path.is_file():
        return
    manifest = json.loads(path.read_text(encoding='utf-8'))
    for batch in manifest['batches']:
        target = (path.parent / batch['path']).resolve()
        if path.parent.resolve() not in target.parents:
            raise ValueError('Review batch must remain in config')
        body = target.read_bytes()
        sha = hashlib.sha256(body).hexdigest()
        old = conn.execute('SELECT content_hash FROM signal_review_batches WHERE id=?', (batch['id'],)).fetchone()
        if old:
            if old[0] != sha:
                raise ValueError('Applied signal review batch was modified: ' + batch['id'])
            continue
        import_reviews(conn, json.loads(body))
        conn.execute('INSERT INTO signal_review_batches VALUES (?,?)', (batch['id'], sha))
        conn.commit()


def export_signals(conn):
    sync_candidates(conn)
    apply_publication(conn)
    alerts = []
    for row in conn.execute('SELECT a.*,r.document FROM signal_alerts a JOIN signal_reviews r ON r.id=a.review_id ORDER BY a.created_at'):
        alerts.append({**dict(row), 'document': json.loads(row['document'])})
    health = [dict(r) for r in conn.execute('SELECT * FROM signal_feed_health ORDER BY id')]
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if 'agent_news_sources' in tables:
        health += [dict(r) for r in conn.execute('SELECT id,url,attempted_at,succeeded_at,error,item_count AS received FROM agent_news_sources ORDER BY id')]
    queue = worklist(conn, None)
    known = {}
    for table in ('research_reports', 'newsroom_articles'):
        if table not in tables: continue
        for r in conn.execute('SELECT id,document FROM '+table):
            document = json.loads(r['document'])
            urls = [x.get('url', '') for x in document.get('references', [])]
            urls += [document.get('source_url', '')]
            for url in urls:
                if not url: continue
                try: known.setdefault(canonical_url(url), []).append(r['id'])
                except ValueError: pass
    for row in queue:
        row['related_reports'] = sorted(set(known.get(row['url'], [])))
    return {'schema_version': 1, 'priority_rule': RULE_VERSION, 'pending_count': len(queue),
            'pending': queue, 'alerts': alerts, 'sources': health, 'known_originals': known,
            'review_count': conn.execute('SELECT COUNT(*) FROM signal_reviews').fetchone()[0]}


def fetch_original(url):
    from .agent_news import _fetch, _tree
    canonical_url(url)
    body, _, _, _ = _fetch({'url': url}, {})
    checked = iso_utc()
    sha = hashlib.sha256(body).hexdigest()
    folder = ROOT / 'data/raw/signal_review'
    folder.mkdir(parents=True, exist_ok=True)
    raw = folder / (sha + '.raw')
    if not raw.exists():
        raw.write_bytes(body)
    receipt = {'url': url, 'checked_at': checked, 'sha256': sha, 'raw_path': raw.relative_to(ROOT).as_posix()}
    path = folder / (digest(receipt) + '.json')
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    return {**receipt, 'receipt': path.relative_to(ROOT).as_posix(),
            'text': _tree(body).text(), 'scope': 'acquisition only; read relevant sections before writing a review'}


def collect(conn, days=30, raw_dir='data/raw/ai_news'):
    from .ai_news import collect_feed_candidates
    from .agent_news import collect_agent_news
    first = collect_feed_candidates(conn, raw_dir=raw_dir, days=days)
    second = collect_agent_news(conn, raw_dir=str(Path(raw_dir) / 'agents'), days=days)
    changed = sync_candidates(conn)
    apply_publication(conn)
    return {'changed': bool(changed or first['health_changed'] or second['changed']),
            'inserted': first['inserted'] + second['inserted'], 'updated': first['updated'] + second['updated'],
            'failures': first['failures'] + second['failures'], 'candidate_editions_changed': changed,
            'fetched': first['fetched'] + second['fetched'], 'sources': second['sources']}


def replay_raw(conn, path):
    """Recover missing candidates without overwriting newer rows or inventing dates."""
    from .ai_news import AI_FEEDS, _google_news_source, _model_news_source, parse_ai_feed, filter_recent_ai_items
    from .db import upsert_news_items
    body = Path(path).read_bytes(); bundle = json.loads(body)
    sources = {s['id']: s for s in AI_FEEDS + [_google_news_source(bundle['days']), _model_news_source(bundle['days'])]}
    observed = datetime.fromisoformat(bundle['collected_at'].replace('Z', '+00:00'))
    recovered = []
    for feed in bundle['feeds']:
        source = sources[feed['source_id']]
        rows = filter_recent_ai_items(parse_ai_feed(feed['body'], source, None), days=bundle['days'], now=observed)
        for row in rows:
            if conn.execute('SELECT id FROM news_items WHERE source_id=? AND external_id=?',
                            (row['source_id'], row['external_id'])).fetchone(): continue
            payload = json.loads(row['raw_payload'])
            payload.update(recovered_original_observed_at=bundle['collected_at'],
                           recovered_bundle_sha256=hashlib.sha256(body).hexdigest())
            row['raw_payload'] = json.dumps(payload, ensure_ascii=False)
            # first_seen_at is this actual normalization, not the earlier raw receipt.
            recovered.append(row)
    result = upsert_news_items(conn, recovered, dedupe_by_title=False)
    return {**result, 'changed': bool(sync_candidates(conn)), 'recovered': len(recovered)}


def sync_public(conn, document=None):
    """Recover the cloud backlog after local downtime; remote data is never instructions."""
    ensure_schema(conn)
    if document is None:
        import urllib.request
        url = 'https://hansihoo.github.io/signal-desk/research-data.json'
        with urllib.request.urlopen(urllib.request.Request(url, headers={'Cache-Control': 'no-cache'}), timeout=45) as response:
            body = response.read(32_000_001)
        if len(body) > 32_000_000: raise ValueError('Public snapshot exceeds limit')
        document = json.loads(body)
    remote = document.get('signal_review')
    if remote is None: return {'imported': 0, 'state': 'pre-discovery-deployment'}
    columns = ('id','url','title','excerpt','fingerprint','published_at','first_seen_at','last_seen_at','priority','reasons','source_ids','revision')
    imported = 0
    with conn:
        for row in remote['pending']:
            if row['id'] != hashlib.sha256(canonical_url(row['url']).encode()).hexdigest()[:24] or not re.fullmatch(r'[a-f0-9]{64}', row['fingerprint']):
                raise ValueError('Invalid public candidate identity')
            old = conn.execute('SELECT * FROM signal_candidates WHERE id=?', (row['id'],)).fetchone()
            if old and old['last_seen_at'] >= row['last_seen_at']: continue
            copy = {k: row[k] for k in columns}
            copy['first_seen_at'] = min(old['first_seen_at'], row['first_seen_at']) if old else row['first_seen_at']
            copy['reasons'] = json.dumps(row['reasons'], ensure_ascii=False)
            copy['source_ids'] = json.dumps(row['source_ids'])
            conn.execute('INSERT OR REPLACE INTO signal_candidates VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', tuple(copy[k] for k in columns))
            conn.execute('INSERT OR IGNORE INTO signal_candidate_editions VALUES (?,?,?)',
                         (row['id'], row['fingerprint'], json.dumps(copy, ensure_ascii=False)))
            imported += 1
    apply_publication(conn)
    return {'imported': imported, 'state': 'public-backlog-synchronized'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default='data/housing_watch.sqlite')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('collect'); p.add_argument('--days', type=int, default=30); p.add_argument('--output')
    p = sub.add_parser('queue'); p.add_argument('--limit', type=int, default=12)
    p = sub.add_parser('fetch'); p.add_argument('url')
    p = sub.add_parser('review'); p.add_argument('--input', required=True)
    p = sub.add_parser('replay'); p.add_argument('--input', required=True)
    sub.add_parser('sync-public')
    sub.add_parser('export')
    sub.add_parser('alerts')
    p = sub.add_parser('ack'); p.add_argument('alert_id'); p.add_argument('--receipt', required=True)
    args = parser.parse_args(argv)
    from .db import connect, init_db
    conn = connect(args.db)
    try:
        init_db(conn); ensure_schema(conn)
        if args.command == 'collect': result = collect(conn, days=max(1, args.days))
        elif args.command == 'fetch': result = fetch_original(args.url)
        elif args.command == 'review':
            result = {'inserted': import_reviews(conn, json.loads(Path(args.input).read_text(encoding='utf-8')), True)}
        elif args.command == 'replay': result = replay_raw(conn, args.input)
        elif args.command == 'sync-public': result = sync_public(conn)
        elif args.command == 'ack':
            if not args.receipt.strip(): raise ValueError('Actual user-visible receipt required')
            cursor = conn.execute("UPDATE signal_alerts SET acknowledged_at=?,receipt=? WHERE id=? AND acknowledged_at=''",
                                  (iso_utc(), args.receipt, args.alert_id)); conn.commit()
            result = {'acknowledged': cursor.rowcount}
        else:
            result = export_signals(conn)
            if args.command == 'queue':
                by_id = {r['id']: r for r in result['pending']}
                result['pending'] = [by_id[r['id']] for r in worklist(conn, max(1, args.limit))]
            if args.command == 'alerts': result = {'alerts': [a for a in result['alerts'] if not a['acknowledged_at']]}
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if getattr(args, 'output', None):
            output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True); output.write_text(text, encoding='utf-8')
        print(text)
        return 0
    except (ValueError, OSError, KeyError, sqlite3.Error) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False)); return 1
    finally:
        conn.close()


if __name__ == '__main__':
    raise SystemExit(main())
