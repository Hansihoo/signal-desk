import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from housing_watch.db import connect, init_db, upsert_news_items
from housing_watch.news import collect_weekly_news
from housing_watch.public_site import build_public_site, collect_public_data, public_library
from housing_watch.research_topics import collect_topic_feeds, load_topics


FEED = b'''<rss version="2.0"><channel><title>Papers</title><item>
<title>Shared evidence</title><link>https://example.com/paper</link><guid>one</guid>
<description>Original source excerpt</description><pubDate>Sat, 03 Oct 2026 00:00:00 GMT</pubDate>
</item></channel></rss>'''


class ResearchTopicTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(':memory:')
        init_db(self.conn)
        self.topic = {'id':'papers','name':'논문','description':'공개 논문 자료','collector':'rss',
                      'feeds':[{'id':'journal','name':'Journal','url':'https://example.com/rss'}]}

    def tearDown(self):
        self.conn.close()

    def collect(self, topic=None, body=FEED):
        with tempfile.TemporaryDirectory() as temp, patch('housing_watch.research_topics._read_url', return_value=body):
            return collect_topic_feeds(self.conn, topic or self.topic, raw_dir=temp)

    def test_new_rss_topic_collects_and_gets_its_own_page(self):
        self.collect()
        topics = load_topics() + [self.topic]
        library = public_library(self.conn, topics)
        self.assertEqual(library[0]['topic_id'], 'papers')
        self.assertEqual(library[0]['summary'], 'Original source excerpt')
        payload = json.loads(self.conn.execute('SELECT raw_payload FROM news_items').fetchone()[0])
        self.assertNotIn('developer_impact', payload)
        with tempfile.TemporaryDirectory() as temp:
            health = [{'topic_id':'news','source':'News','ok':False,'message':'Offline'}]
            build_public_site(self.conn, temp, health=health, topics=topics)
            catalog = json.loads((Path(temp) / 'topics.json').read_text(encoding='utf-8'))
            self.assertEqual(catalog[-1]['count'], 1)
            page = (Path(temp) / 'research/papers/index.html').read_text(encoding='utf-8')
            self.assertIn('논문 리서치', page)
            self.assertIn('Original source excerpt', page)
            self.assertIn('"prefix": "../../"', page)
            data = json.loads(page.split('<script id="briefing-data" type="application/json">')[1].split('</script>')[0])
            self.assertEqual(data['health'], [])
            news = (Path(temp) / 'research/news/index.html').read_text(encoding='utf-8')
            data = json.loads(news.split('<script id="briefing-data" type="application/json">')[1].split('</script>')[0])
            self.assertEqual(data['health'], health)

    def test_same_title_in_other_domains_is_not_deleted(self):
        upsert_news_items(self.conn, [{'source_id':'ai_test','external_id':'1','title':'Shared evidence',
                                     'url':'https://example.com/ai','score':300}], source_prefix='ai_%')
        self.collect()
        other = dict(self.topic, id='papers-extra', name='다른 논문')
        self.collect(other)
        weekly = {'source_id':'google_news_top_ko','external_id':'2','title':'Shared evidence',
                  'url':'https://example.com/news','score':100}
        result = {'source_id':'google_news_ko_bundle','raw_path':'unused','items':[weekly]}
        with patch('housing_watch.news.fetch_google_news_ko', return_value=result):
            collect_weekly_news(self.conn, source='google-news')
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM news_items').fetchone()[0], 4)
        self.collect()
        self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM news_items').fetchone()[0], 4)
        rows = public_library(self.conn, load_topics() + [self.topic, other])
        self.assertEqual({row['topic_id'] for row in rows}, {'ai','news','papers','papers-extra'})

    def test_atom_and_partial_feed_failure_keep_successful_sources(self):
        atom = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>atom-1</id><title>Climate evidence</title>
        <link href="https://example.com/climate"/><summary>Measured trend</summary><updated>2026-10-03T00:00:00Z</updated></entry></feed>'''
        topic = dict(self.topic, feeds=self.topic['feeds'] + [{'id':'broken','url':'https://example.com/broken'}])
        with tempfile.TemporaryDirectory() as temp, patch('housing_watch.research_topics._read_url', side_effect=[atom, b'not XML']):
            result = collect_topic_feeds(self.conn, topic, raw_dir=temp)
        self.assertEqual(result['fetched'], 1)
        self.assertEqual(len(result['failures']), 1)
        self.assertEqual(public_library(self.conn, [topic])[0]['summary'], 'Measured trend')

    def test_archived_topics_and_items_are_preserved_after_rename(self):
        self.collect()
        with tempfile.TemporaryDirectory() as temp:
            build_public_site(self.conn, temp, topics=[self.topic])
            files = list((Path(temp) / 'archive').glob('*/briefing.json'))
            original = files[0].read_bytes()
            renamed = dict(self.topic, name='새 이름')
            build_public_site(self.conn, temp, topics=[renamed])
            self.assertEqual(files[0].read_bytes(), original)
            old = (files[0].parent / 'index.html').read_text(encoding='utf-8')
            self.assertIn('"name": "논문"', old)
            self.assertNotIn('"name": "새 이름"', old)

    def test_config_rejects_path_escape_and_credential_urls(self):
        for invalid in [dict(self.topic, id='../outside'), dict(self.topic, feeds=[{'id':'one','url':'https://user:secret@example.com/rss'}])]:
            with tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / 'topics.json'
                path.write_text(json.dumps({'topics':[invalid]}), encoding='utf-8')
                with self.assertRaises(ValueError):
                    load_topics(path)

    def test_selected_registry_controls_collection(self):
        with patch('housing_watch.public_site.collect_topic_feeds', return_value={'fetched':1,'failures':[]}) as rss, patch('housing_watch.public_site.collect_ai_news') as ai, patch('housing_watch.public_site.collect_weekly_news') as news:
            health = collect_public_data(self.conn, {'sources':[]}, topics=[self.topic])
        rss.assert_called_once()
        ai.assert_not_called()
        news.assert_not_called()
        self.assertEqual(health[0]['source'], '논문')
