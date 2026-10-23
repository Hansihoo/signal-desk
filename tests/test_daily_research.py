import json
import sqlite3
import subprocess
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from housing_watch import daily_research as daily


SOURCE = {'id': 'nipa-test', 'name': 'NIPA', 'url': 'https://www.nipa.kr/home/2-2?tab=2',
          'area': '국책사업·조달', 'mode': 'nipa_table', 'coverage': 'first page', 'browser_task': 'search'}
BODY = '''<h1>사업공고</h1><table><tr><td>3</td><td>D-5</td><td>
<a href="/home/2-2/12345">문서 AI 공급기업 모집</a><p>사업</p>
신청기간 : 2026-10-15 09:00 ~ 2026-10-30 18:00</td><td>담당자</td><td>2026-10-15</td></tr></table>'''.encode()
FIRST = '2026-10-21T00:00:00+00:00'
SECOND = '2026-10-21T01:00:00+00:00'


class DailyResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.addCleanup(self.conn.close)
        self.catalog = {'sources': [SOURCE]}

    def collect(self, body=BODY, now=FIRST, catalog=None, fetcher=None, **kwargs):
        return daily.collect(self.conn, catalog or self.catalog, Path(self.temp.name) / 'raw',
                             fetcher=fetcher or (lambda s, old: (body, 'etag', 'modified', False)),
                             now=now, max_age_minutes=kwargs.pop('max_age_minutes', 0), **kwargs)

    def test_nipa_real_title_period_and_date_ignore_counter_and_staff(self):
        row = daily.parse_source(BODY, SOURCE)[0]
        self.assertEqual(row['title'], '문서 AI 공급기업 모집')
        self.assertEqual(row['published_at'], '2026-10-15')
        self.assertEqual(row['period'], '2026-10-15 09:00 ~ 2026-10-30 18:00')
        self.assertNotIn('담당자', json.dumps(row, ensure_ascii=False))
        self.assertNotIn('D-5', json.dumps(row))

    def test_bizinfo_uses_notice_identity_and_publication_column_not_views(self):
        body = '''<h1>지원사업 공고</h1><table><tr><td>1500</td><td>기술</td><td>
        <a href="/sii/siia/selectSIIA200Detail.do?cpage=9&amp;pblancId=PBLN_000123&amp;keyword=AI">문서 AX 지원</a>
        </td><td>예산 소진시까지</td><td>부처</td><td>기관</td><td>2026-10-20</td><td>20261099</td></tr></table>'''.encode()
        source = dict(SOURCE, mode='bizinfo_table', url='https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do')
        row = daily.parse_source(body, source)[0]
        self.assertEqual(row['title'], '문서 AX 지원')
        self.assertEqual(row['url'], 'https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000123')
        self.assertEqual(row['published_at'], '2026-10-20')
        self.assertNotIn('20261099', str(row))

    def test_initial_snapshot_is_baseline_and_repeat_does_not_create_revision(self):
        result = self.collect()
        self.assertEqual((result['baseline'], result['new']), (1, 0))
        self.assertEqual(daily.queue(self.conn)['total'], 0)
        result = self.collect(BODY.replace(b'D-5', b'D-4'), now=SECOND)
        self.assertEqual((result['new'], result['changed']), (0, 0))
        row = self.conn.execute('SELECT * FROM daily_candidates').fetchone()
        self.assertEqual((row['first_seen_at'], row['last_seen_at']), (FIRST, SECOND))
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM daily_candidate_editions').fetchone()[0], 1)

    def test_unchanged_baseline_notice_still_enters_deadline_worklist(self):
        self.collect()
        far = daily.queue(self.conn, today=date(2026, 10, 22))
        due = daily.queue(self.conn, today=date(2026, 10, 23))
        self.assertEqual((far['total'], far['deadline_total']), (0, 0))
        self.assertEqual((due['total'], due['deadline_total']), (0, 1))
        self.assertEqual(due['deadline_hints'][0]['days_remaining_hint'], 7)
        self.assertEqual(due['deadline_hints'][0]['change_kind'], 'baseline')
        self.assertIn('verify actual status', due['deadline_hints'][0]['limitation'])
        self.assertEqual(daily.queue(self.conn, today=date(2026, 10, 31))['deadline_total'], 0)

    def test_open_ended_or_ambiguous_period_is_not_a_fabricated_deadline(self):
        for period in ['예산 소진시까지', '2026-10-23부터 예산 소진시까지']:
            body = BODY.replace(b'2026-10-15 09:00 ~ 2026-10-30 18:00', period.encode())
            self.collect(body)
            result = daily.queue(self.conn, today=date(2026, 10, 23))
            self.assertEqual((result['deadline_total'], result['unresolved_period_count']), (0, 1))

    def test_real_amendment_and_new_notice_preserve_previous_editions(self):
        self.collect()
        body = BODY.replace(b'2026-10-30 18:00', b'2026-11-02 18:00') + BODY.replace(b'12345', b'12346')
        result = self.collect(body, now=SECOND)
        self.assertEqual((result['changed'], result['new']), (1, 1))
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM daily_candidate_editions').fetchone()[0], 3)
        self.assertEqual(daily.queue(self.conn)['total'], 2)
        old = self.conn.execute('SELECT document FROM daily_candidate_editions WHERE observed_at=?', (FIRST,)).fetchone()[0]
        self.assertIn('2026-10-30', old)

    def test_failed_or_empty_fetch_preserves_last_success_and_candidates(self):
        self.collect()
        for fetcher in [lambda s, o: (_ for _ in ()).throw(OSError('temporary timeout')),
                        lambda s, o: (b'<html>layout changed</html>', '', '', False)]:
            result = self.collect(now=SECOND, fetcher=fetcher)
            self.assertEqual(result['sources'][0]['status'], 'failed')
            state = self.conn.execute('SELECT * FROM daily_source_state').fetchone()
            self.assertEqual(state['succeeded_at'], FIRST)
            self.assertEqual(state['attempted_at'], SECOND)
            self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM daily_candidates').fetchone()[0], 1)

    def test_invalid_late_row_rolls_back_entire_source_revision(self):
        self.collect()
        good = {'url': 'https://www.nipa.kr/home/2-2/12345', 'title': 'Changed notice', 'published_at': '2026-10-20'}
        bad = {'url': 'javascript:invalid', 'title': 'Invalid item'}
        with patch.object(daily, 'parse_source', return_value=[good, bad]):
            result = self.collect(now=SECOND)
        self.assertEqual(result['changed'], 0)
        self.assertEqual(result['sources'][0]['status'], 'failed')
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM daily_candidate_editions').fetchone()[0], 1)
        current = json.loads(self.conn.execute('SELECT document FROM daily_candidates').fetchone()[0])
        self.assertEqual(current['title'], '문서 AI 공급기업 모집')

    def test_source_url_change_failure_does_not_bind_old_etag_to_new_url(self):
        self.collect()
        new_source = dict(SOURCE, url='https://www.nipa.kr/new-list')
        catalog = {'sources': [new_source]}
        self.collect(now=SECOND, catalog=catalog, fetcher=lambda s, o: (_ for _ in ()).throw(OSError('new URL failed')))
        state = dict(self.conn.execute('SELECT * FROM daily_source_state').fetchone())
        self.assertEqual(state['url'], SOURCE['url'])
        self.assertEqual(state['succeeded_at'], FIRST)

    def test_cache_reuse_does_not_refresh_acquisition_time(self):
        self.collect()
        result = self.collect(now='2026-10-21T00:15:00+00:00', max_age_minutes=30,
                              fetcher=lambda s, o: self.fail('fresh cache must not fetch'))
        self.assertEqual(result['cached'], 1)
        self.assertEqual(self.conn.execute('SELECT succeeded_at FROM daily_source_state').fetchone()[0], FIRST)

    def test_receipt_separates_attempt_start_from_actual_acquisition(self):
        with patch.object(daily, 'iso_utc', side_effect=[FIRST, SECOND]):
            self.collect(now=None)
        state = self.conn.execute('SELECT * FROM daily_source_state').fetchone()
        self.assertEqual((state['attempted_at'], state['succeeded_at']), (FIRST, SECOND))
        receipt = json.loads(next((Path(self.temp.name) / 'raw').rglob('*.receipt.json')).read_text(encoding='utf-8'))
        self.assertEqual((receipt['attempt_started_at'], receipt['acquired_at']), (FIRST, SECOND))

    def test_browser_route_is_an_explicit_unreviewed_gap(self):
        result = self.collect(catalog={'sources': [dict(SOURCE, mode='browser')]},
                              fetcher=lambda s, o: self.fail('browser routes must not use text fetch'))
        self.assertEqual(result['sources'][0]['status'], 'browser_required')
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM daily_source_state').fetchone()[0], 0)

    def test_long_publisher_list_cannot_hide_other_source_in_worklist(self):
        catalog = {'sources': [SOURCE, dict(SOURCE, id='other-source', name='Other')]}
        body = b''.join(BODY.replace(b'12345', str(12345 + n).encode()) for n in range(10))
        self.collect(body, catalog=catalog)
        result = daily.queue(self.conn, limit=2, include_baseline=True)
        self.assertEqual(result['total'], 20)
        self.assertEqual({x['source_id'] for x in result['items']}, {'nipa-test', 'other-source'})

    def test_revalidation_of_old_change_cannot_bury_new_unknown_notice(self):
        self.collect()
        amended = BODY.replace(b'2026-10-30 18:00', b'2026-11-02 18:00')
        self.collect(amended, now=SECOND)
        unknown = BODY.replace(b'12345', b'12346').replace('문서 AI 공급기업 모집'.encode(), '새 이름'.encode())
        self.collect(amended + unknown, now='2026-10-22T00:00:00+00:00')
        result = daily.queue(self.conn, limit=1)
        self.assertEqual(result['items'][0]['title'], '새 이름')
        self.assertEqual(result['items'][0]['change_kind'], 'new')

    def test_cli_guard_failure_creates_no_database(self):
        target = Path(self.temp.name) / 'not-created' / 'daily.sqlite'
        with patch.object(daily, 'DATABASE', target), patch.object(daily.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'verify')):
            with self.assertRaises(subprocess.CalledProcessError):
                daily.main(['collect'])
        self.assertFalse(target.parent.exists())

    def test_catalog_resolves_existing_business_sources_without_changing_them(self):
        catalog = daily.load_catalog()
        self.assertEqual(sum(s['mode'] != 'browser' for s in catalog['sources']), 7)
        sources = {s['id']: s for s in catalog['sources']}
        for source_id in ('ms365-copilot-release-daily', 'acrobat-updates-daily'):
            self.assertEqual(sources[source_id]['mode'], 'browser')
            self.assertEqual(sources[source_id]['area'], 'AI 문서 활용')
        self.assertEqual(sources['ms365-copilot-release-daily']['url'],
                         'https://learn.microsoft.com/en-us/microsoft-365/copilot/release-notes')
        self.assertTrue(all(s.get('url') and s.get('name') for s in catalog['sources']))


if __name__ == '__main__':
    unittest.main()
