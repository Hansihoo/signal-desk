import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from housing_watch.ai_news import collect_feed_candidates, parse_ai_feed
from housing_watch.agent_news import collect_agent_news, published_date
from housing_watch.db import connect, init_db, upsert_news_items
from housing_watch.signal_review import (impact_priority, sync_candidates, worklist, import_reviews,
                                         export_signals, apply_publication, canonical_url, sync_public)


class SignalReviewTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(':memory:'); init_db(self.conn)
        self.source = dict(id='ai_test', name='Test', tier='discovery', feed_url='https://example.org/rss')

    def tearDown(self): self.conn.close()

    def add(self, title='Unknown tool connects agents to binary analysis', suffix='a', detail=''):
        body = ('<rss><channel><item><title>'+title+'</title><link>https://example.org/'+suffix+
                '</link><description>'+detail+'</description></item></channel></rss>').encode()
        items = parse_ai_feed(body, self.source, limit=None)
        upsert_news_items(self.conn, items, dedupe_by_title=False); sync_candidates(self.conn)
        return next(x for x in worklist(self.conn, None) if x['url'].endswith('/'+suffix))

    def review(self, row, **values):
        result = dict(candidate_id=row['id'], fingerprint=row['fingerprint'], candidate_url=row['url'],
            candidate_title=row['title'], decision='important', event_key='unknown-tool-launch',
            event_change='initial-release', reviewed_at='2026-10-21T03:00:00Z', novelty='new_tool',
            summary='A verified new capability', impact='Changes a development task', reason='Original compared to earlier release',
            evidence=[dict(url='https://example.org/original', role='primary', checked_at='2026-10-21T02:00:00Z',
                           sha256='a'*64, finding='Specific launch scope and limitation read')])
        result.update(values)
        return {'schema_version': 1, 'reviews': [result]}

    def test_rea_position_71_survives_storage_and_priority(self):
        entries = ['<item><title>Routine item %d</title><link>https://example.org/%d</link></item>'%(i,i) for i in range(100)]
        entries[70] = '<item><title>REA connects agents to Ghidra to reverse engineer anything</title><link>https://example.org/rea</link></item>'
        body = ('<rss><channel>'+''.join(entries)+'</channel></rss>').encode()
        with tempfile.TemporaryDirectory() as d, patch('housing_watch.ai_news.AI_FEEDS',[self.source]), patch('housing_watch.ai_news._read_url', return_value=body):
            result = collect_feed_candidates(self.conn, raw_dir=d)
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM news_items WHERE source_id=?',('ai_test',)).fetchone()[0],100)
        sync_candidates(self.conn)
        self.assertTrue(any('REA connects' in x['title'] for x in worklist(self.conn,3)))

    def test_unknown_name_has_same_impact_priority_as_known_name(self):
        self.assertEqual(impact_priority('REA connects agents to binary analysis')['score'],
                         impact_priority('UnseenName connects agents to binary analysis')['score'])
        self.assertGreater(impact_priority('New tool performs reverse engineering with validation')['score'],impact_priority('v1.0.1')['score'])
        self.assertLess(impact_priority('v1.0.1','Internal deprecation cleanup and security typing docs')['score'],
                        impact_priority('New tool performs reverse engineering with validation')['score'])
        self.assertIn('호환성 변경·이전 조건 확인 필요',impact_priority('tool: v6.7.0','BREAKING CHANGES Saved snapshots must be regenerated')['reasons'])

    def test_moved_official_engineering_article_paths_are_parsed(self):
        from housing_watch.agent_news import parse_listing
        source=dict(id='engineering',name='Engineering',publisher='Company',url='https://example.org/engineering',
                    format='html',paths=['/engineering/','/research/'],kind='article',tier='official')
        body=b'<main><a href="/research/actual"><h2>New development workflow</h2></a></main>'
        self.assertEqual(parse_listing(body,source,None)[0]['url'],'https://example.org/research/actual')

    def test_same_headline_different_urls_and_same_url_aliases(self):
        self.add('A release', 'one'); self.add('A release', 'two')
        self.assertEqual(len(worklist(self.conn,None)),2)
        self.assertEqual(canonical_url('https://example.org/one/?utm_source=x#x'),'https://example.org/one')

    def test_unknown_old_candidate_gets_reserved_slot(self):
        oldest=self.add('Unknown subject', 'old')
        self.conn.execute("UPDATE signal_candidates SET first_seen_at='2026-10-01T00:00:00Z' WHERE id=?",(oldest['id'],))
        for i in range(10): self.add(suffix='new'+str(i))
        self.conn.execute("UPDATE signal_candidates SET first_seen_at='2026-10-01T00:00:00Z' WHERE id=?",(oldest['id'],))
        self.assertIn(oldest['id'],[r['id'] for r in worklist(self.conn,3)])

    def test_fresh_unfamiliar_subject_and_old_backlog_both_get_slots(self):
        old=self.add('Unknown older subject','old')
        for i in range(8):self.add(suffix='high'+str(i))
        fresh=self.add('Unfamiliar subject Kepler','fresh')
        self.conn.execute("UPDATE signal_candidates SET first_seen_at='2026-01-01T00:00:00Z' WHERE id=?",(old['id'],))
        ids=[r['id'] for r in worklist(self.conn,3)]
        self.assertIn(old['id'],ids);self.assertIn(fresh['id'],ids)

    def test_review_gate_outbox_dedupe_ack_and_changed_candidate(self):
        row=self.add(); batch=self.review(row)
        self.assertEqual(import_reviews(self.conn,batch),1)
        self.assertEqual(import_reviews(self.conn,batch),0)
        self.assertEqual(worklist(self.conn),[])
        other=self.add(suffix='other')
        import_reviews(self.conn,self.review(other))
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM signal_alerts').fetchone()[0],1)
        self.conn.execute("UPDATE signal_alerts SET acknowledged_at='2026-10-21T04:00:00Z',receipt='visible message verified'")
        self.assertTrue(export_signals(self.conn)['alerts'][0]['acknowledged_at'])
        self.add(detail='Meaningful changed capability')
        self.assertTrue(any(r['id']==row['id'] for r in worklist(self.conn)))

    def test_rumor_no_primary_existing_story_and_stale_edition_fail_closed(self):
        row=self.add()
        for changes in [dict(evidence=[]),dict(novelty='existing_story'),dict(reviewed_at='2026-10-21')]:
            with self.assertRaises(ValueError):import_reviews(self.conn,self.review(row,**changes))
        with self.assertRaises(ValueError):import_reviews(self.conn,self.review(row,fingerprint='b'*64),require_receipts=True)
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM signal_reviews').fetchone()[0],0)

    def test_unconfirmed_due_recheck_and_old_story_not_new_alert(self):
        row=self.add()
        import_reviews(self.conn,self.review(row,decision='unconfirmed',evidence=[],recheck_after='2026-10-22T00:00:00Z'))
        self.assertEqual(worklist(self.conn,now='2026-10-21T05:00:00Z'),[])
        self.assertEqual(worklist(self.conn,now='2026-10-23T05:00:00Z')[0]['state'],'recheck_due')
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM signal_alerts').fetchone()[0],0)

    def test_immutable_batch_and_date_precision(self):
        row=self.add(); batch=self.review(row,decision='already_known',novelty='existing_story')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'reviews.json').write_text(json.dumps(batch),encoding='utf-8')
            m=p/'manifest.json';m.write_text(json.dumps({'batches':[{'id':'batch','path':'reviews.json'}]}),encoding='utf-8')
            apply_publication(self.conn,m);apply_publication(self.conn,m)
            (p/'reviews.json').write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'modified'):apply_publication(self.conn,m)
        self.assertEqual(published_date('By Author · 13 October 2026'),'2026-10-13')

    def test_cloud_backlog_survives_offline_and_old_edition_survives_change(self):
        row = self.add(); snapshot = export_signals(self.conn)
        other = connect(':memory:'); init_db(other)
        self.assertEqual(sync_public(other, {'signal_review': snapshot})['imported'],1)
        self.assertEqual(export_signals(other)['pending'][0]['id'],row['id'])
        self.assertEqual(sync_public(other, {'signal_review': snapshot})['imported'],0)
        other.close()
        self.add(detail='New behavior to review')
        self.assertEqual(len(worklist(self.conn)[0]['prior_editions']),1)

    def test_failed_source_preserves_latest_success_and_candidates(self):
        rss=b'<rss><channel><item><title>Novel workflow</title><link>https://example.org/new</link></item></channel></rss>'
        with tempfile.TemporaryDirectory() as d, patch('housing_watch.ai_news.AI_FEEDS',[self.source]),patch('housing_watch.ai_news._read_url',return_value=rss):
            collect_feed_candidates(self.conn,raw_dir=d)
            sync_candidates(self.conn)
            before=self.conn.execute('SELECT succeeded_at FROM signal_feed_health WHERE id=?',('ai_test',)).fetchone()[0]
            with patch('housing_watch.ai_news._read_url',side_effect=OSError('offline')):
                result=collect_feed_candidates(self.conn,raw_dir=d)
            after=self.conn.execute('SELECT * FROM signal_feed_health WHERE id=?',('ai_test',)).fetchone()
        self.assertTrue(result['failures']);self.assertEqual(after['succeeded_at'],before)
        self.assertEqual(after['error'],'offline');self.assertTrue(worklist(self.conn))

    def test_acknowledgement_replays_from_public_batch(self):
        row=self.add();batch=self.review(row);import_reviews(self.conn,batch)
        alert=self.conn.execute('SELECT id FROM signal_alerts').fetchone()[0]
        batch['acknowledgements']=[dict(alert_id=alert,acknowledged_at='2026-10-21T04:00:00Z',receipt='User-visible message confirmed')]
        import_reviews(self.conn,batch)
        self.assertTrue(export_signals(self.conn)['alerts'][0]['acknowledged_at'])

    def test_empty_feed_is_a_retrieval_gap_not_unchanged_success(self):
        with tempfile.TemporaryDirectory() as d,patch('housing_watch.ai_news.AI_FEEDS',[self.source]),patch('housing_watch.ai_news._read_url',return_value=b'<html>Changed layout</html>'):
            result=collect_feed_candidates(self.conn,raw_dir=d)
        self.assertTrue(result['failures']);self.assertTrue(result['health_changed'])
        row=self.conn.execute('SELECT * FROM signal_feed_health WHERE id=?',('ai_test',)).fetchone()
        self.assertEqual(row['succeeded_at'],'');self.assertIn('No readable',row['error'])


if __name__ == '__main__': unittest.main()
