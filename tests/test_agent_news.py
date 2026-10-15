import json
import tempfile
import unittest
from datetime import datetime,timezone
from pathlib import Path
from unittest.mock import patch

from housing_watch.agent_news import collect_agent_news, detail_metadata, parse_listing, published_date, export_sources
from housing_watch.ai_news import collect_ai_news
from housing_watch.db import connect, init_db
from housing_watch.newsroom import import_articles, export_newsroom, article_body, source_body, source_rows


SOURCE={'id':'company','name':'Company News','publisher':'Company','url':'https://company.example/news',
        'format':'html','paths':['/news/'],'kind':'article','tier':'official'}
BODY=b'''<html><nav><a href="/news/fake">Fake navigation story</a></nav><main>
<a href="/news/launch"><h2>Agent launch</h2><time datetime="2026-10-13">Yesterday</time><p>Real launch details.</p></a>
<a href="/news/launch"><h2>Duplicate</h2></a>
<a href="javascript:alert(1)"><h2>Unsafe link</h2></a>
<a href="https://evil.example/news/evil"><h2>Different host</h2></a></main></html>'''


class AgentNewsTests(unittest.TestCase):
    def setUp(self):
        self.conn=connect(':memory:');init_db(self.conn)

    def tearDown(self):self.conn.close()

    def test_html_discovery_keeps_date_precision_and_excludes_navigation_duplicates_hosts(self):
        rows=parse_listing(BODY,SOURCE)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0],{'url':'https://company.example/news/launch','title':'Agent launch','published_at':'2026-10-13','excerpt':'Real launch details.'})

    def test_publication_metadata_does_not_use_collection_date(self):
        self.assertEqual(published_date('Published Oct 13, 2026'),'2026-10-13')
        self.assertEqual(published_date('2026년 10월 14일'),'2026-10-14')
        self.assertEqual(published_date('09.25.26'),'2026-09-25')
        self.assertEqual(published_date('26.10.14'),'2026-10-14')
        self.assertEqual(published_date('TODAY'),'')
        meta=detail_metadata('<h1>Launch</h1><script type="application/ld+json">{"datePublished":"2026-10-13"}</script>')
        self.assertEqual(meta['published_at'],'2026-10-13')

    def test_release_details_link_uses_its_single_heading_container(self):
        witness=dict(SOURCE,url='https://aiwitness.kr/',paths=['/releases/'])
        body='<div><h3>v1.2.3</h3><time datetime="2026-10-14">Today</time><div><div><a href="/releases/123">자세히 보기</a></div></div></div>'
        rows=parse_listing(body,witness)
        self.assertEqual(rows[0]['title'],'v1.2.3')
        self.assertEqual(rows[0]['published_at'],'2026-10-14')

    def test_card_headers_and_image_only_links_do_not_disappear_or_include_pagination(self):
        body='<main><a href="/news/new"><header><h2>New agent feature</h2></header></a><a href="/news?page=2">Next page</a><a href="/news/page/2/">Page 2</a><article><a href="/news/image"><img src="x"></a><h3>Image card title</h3><time datetime="2026-10-13"></time></article></main>'
        rows=parse_listing(body,SOURCE)
        self.assertEqual([r['title'] for r in rows],['New agent feature','Image card title'])
        self.assertEqual(detail_metadata('<h1></h1><header><h1>Real title</h1><span>Published Oct 13, 2026</span></header>')['title'],'Real title')

    def test_date_only_link_cannot_mask_later_title_link(self):
        body='<article><a href="/news/real">Oct 13, 2026</a><a href="/news/real">Actual title</a><time datetime="2026-10-13"></time></article>'
        rows=parse_listing(body,SOURCE)
        self.assertEqual(rows[0]['title'],'Actual title')

    def test_failure_and_empty_layout_preserve_items_and_last_success(self):
        with tempfile.TemporaryDirectory() as d, patch('housing_watch.agent_news._fetch',return_value=(BODY,'etag','',False)):
            first=collect_agent_news(self.conn,[SOURCE],raw_dir=d,days=365)
            self.assertEqual(first['inserted'],1)
            old=export_sources(self.conn)[0]['succeeded_at']
            with patch('housing_watch.agent_news._fetch',side_effect=OSError('network unavailable')):
                failed=collect_agent_news(self.conn,[SOURCE],raw_dir=d)
            self.assertTrue(failed['changed'])
            self.assertEqual(export_sources(self.conn)[0]['succeeded_at'],old)
            self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM news_items').fetchone()[0],1)
            with patch('housing_watch.agent_news._fetch',return_value=(b'<html>layout changed</html>','','',False)):
                empty=collect_agent_news(self.conn,[SOURCE],raw_dir=d)
            self.assertIn('No readable entries',empty['failures'][0])
            self.assertEqual(export_sources(self.conn)[0]['succeeded_at'],old)

    def test_repeated_content_is_unchanged_and_keeps_first_seen_and_one_raw_blob(self):
        with tempfile.TemporaryDirectory() as d, patch('housing_watch.agent_news._fetch',return_value=(BODY,'etag','',False)):
            first=collect_agent_news(self.conn,[SOURCE],raw_dir=d,days=365)
            first_seen=self.conn.execute('SELECT first_seen_at FROM news_items').fetchone()[0]
            second=collect_agent_news(self.conn,[SOURCE],raw_dir=d,days=365)
            self.assertFalse(second['changed'])
            self.assertEqual(second['updated'],0)
            self.assertEqual(self.conn.execute('SELECT first_seen_at FROM news_items').fetchone()[0],first_seen)
            self.assertEqual(len(list(Path(d).rglob('*.html'))),1)

    def test_empty_or_malformed_feed_becomes_health_failure(self):
        feed=dict(SOURCE,format='feed')
        with tempfile.TemporaryDirectory() as d,patch('housing_watch.agent_news._fetch',return_value=(b'not XML','','',False)):
            result=collect_agent_news(self.conn,[feed],raw_dir=d)
        self.assertFalse(result['sources'][0]['ok'])

    def test_korean_today_is_not_rejected_as_future_before_utc_midnight(self):
        body=BODY.replace(b'2026-10-13',b'2026-10-14')
        late_utc=datetime(2026,10,13,16,tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as d,patch('housing_watch.agent_news._fetch',return_value=(body,'','',False)),patch('housing_watch.agent_news.now_utc',return_value=late_utc):
            result=collect_agent_news(self.conn,[SOURCE],raw_dir=d)
        self.assertEqual(result['inserted'],1)
        self.assertEqual(self.conn.execute('SELECT published_at FROM news_items').fetchone()[0],'2026-10-14')

    def test_legacy_outage_cannot_prevent_successful_agent_watch(self):
        result={'fetched':1,'inserted':1,'updated':0,'failures':[],'changed':True,'sources':[]}
        with tempfile.TemporaryDirectory() as d, patch('housing_watch.ai_news._read_url',side_effect=OSError('offline')), \
                patch('housing_watch.ai_news.collect_model_research',side_effect=OSError('offline')), \
                patch('housing_watch.ai_news.collect_model_ledger',side_effect=OSError('offline')), \
                patch('housing_watch.ai_news.collect_model_pages',side_effect=OSError('offline')), \
                patch('housing_watch.agent_news.collect_agent_news',return_value=result) as watch:
            collected=collect_ai_news(self.conn,raw_dir=d)
        self.assertEqual(collected['fetched'],1)
        self.assertEqual(collected['inserted'],1)
        self.assertEqual(watch.call_args.kwargs['raw_dir'],str(Path(d)/'agents'))

    def test_source_body_escapes_untrusted_source_data(self):
        body=source_body({'id':'news-1','source':'<script>x</script>','title':'<img src=x>','summary':'<script>y</script>',
                         'published_at':'<script>z','first_seen_at':'','url':'https://example.com/'})
        self.assertNotIn('<script>',body)
        self.assertNotIn('<img src=x>',body)

    def test_undated_discovery_cannot_outrank_dated_news_by_collection_time(self):
        rows=source_rows({'items':[{'id':'old','topic_id':'ai','url':'https://example.com/old','published_at':'','first_seen_at':'2026-10-14'},
                                  {'id':'new','topic_id':'ai','url':'https://example.com/new','published_at':'2026-10-13','first_seen_at':'2026-10-13'}]})
        self.assertEqual(rows[0]['url'],'https://example.com/new')

    def test_new_source_alias_does_not_reset_the_urls_first_discovery_date(self):
        snapshot={'items':[
            {'id':'new-source','topic_id':'ai','url':'https://example.com/story','published_at':'2026-10-13','first_seen_at':'2026-10-14T01:00:00Z'},
            {'id':'old-source','topic_id':'ai','url':'https://example.com/story','published_at':'2026-10-13','first_seen_at':'2026-10-13T01:00:00Z'}]}
        rows=source_rows(snapshot)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['first_seen_at'],'2026-10-13T01:00:00Z')
        self.assertEqual(snapshot['items'][0]['first_seen_at'],'2026-10-14T01:00:00Z')

    def test_article_import_preserves_old_editions_and_does_not_refresh_unchanged_copy(self):
        article={'id':'article-example','title':'A real news story','deck':'A clear lead','publisher':'Company','published_on':'2026-10-13',
                 'checked_on':'2026-10-14','source_url':'https://example.com/news',
                 'sections':[{'heading':'','paragraphs':[{'text':'Sourced prose.','source_ids':['original']}]}],
                 'references':[{'id':'original','title':'Original','url':'https://example.com/news'}]}
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'input.json';path.write_text(json.dumps({'articles':[article]}),encoding='utf-8')
            self.assertEqual(import_articles(self.conn,path)['inserted'],1)
            before=export_newsroom(self.conn)
            self.assertEqual(import_articles(self.conn,path)['unchanged'],1)
            self.assertEqual(export_newsroom(self.conn),before)
            article['title']='An updated story';path.write_text(json.dumps({'articles':[article]}),encoding='utf-8')
            self.assertEqual(import_articles(self.conn,path)['updated'],1)
            data=export_newsroom(self.conn)
            self.assertEqual(len(data['history']),2)
            self.assertEqual(data['history'][0]['document']['title'],'A real news story')
            self.assertIn('news-ref-1',article_body(article))
            article['sections'][0]['paragraphs'][0]['source_ids']=['unknown']
            path.write_text(json.dumps({'articles':[article]}),encoding='utf-8')
            with self.assertRaises(ValueError):import_articles(self.conn,path)
            self.assertEqual(export_newsroom(self.conn),data)


if __name__=='__main__':unittest.main()
