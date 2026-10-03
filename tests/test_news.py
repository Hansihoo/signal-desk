import unittest

from housing_watch.db import connect, init_db, latest_news_items, upsert_news_items
from housing_watch.news import categorize_news, parse_google_news_rss


GOOGLE_RSS_SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item>
      <title>대통령 국정조사 관련 여야 충돌 - 테스트신문</title>
      <link>https://news.google.com/rss/articles/example</link>
      <guid isPermaLink="false">example-guid</guid>
      <pubDate>Thu, 18 Jun 2026 21:01:00 GMT</pubDate>
      <source url="https://example.com">테스트신문</source>
    </item>
  </channel>
</rss>
""".encode("utf-8")


class NewsTests(unittest.TestCase):
    def test_parse_google_news_rss(self):
        items = parse_google_news_rss(GOOGLE_RSS_SAMPLE, limit=3)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["source_id"], "google_news_top_ko")
        self.assertEqual(items[0]["title_ko"], "대통령 국정조사 관련 여야 충돌")
        self.assertEqual(items[0]["source_name"], "테스트신문")
        self.assertEqual(items[0]["source_url"], "https://example.com")
        self.assertEqual(items[0]["category"], "정치")
        self.assertIn("핵심은 대통령 국정조사 관련 여야 충돌 입니다", items[0]["summary_ko"])
        self.assertIn("국회 일정", items[0]["summary_ko"])

    def test_parse_world_google_news_rss(self):
        items = parse_google_news_rss(GOOGLE_RSS_SAMPLE, limit=3, source_id="google_news_world_ko", category_hint="국제", score_base=119)
        self.assertEqual(items[0]["source_id"], "google_news_world_ko")
        self.assertEqual(items[0]["category"], "국제")
        self.assertEqual(items[0]["score"], 119)

    def test_upsert_and_latest_news_items(self):
        conn = connect(":memory:")
        init_db(conn)
        parsed = parse_google_news_rss(GOOGLE_RSS_SAMPLE, limit=3)
        stats = upsert_news_items(conn, parsed)
        self.assertEqual(stats["inserted"], 1)
        latest = latest_news_items(conn, limit=5)
        self.assertEqual(len(latest), 1)
        self.assertEqual(latest[0]["title_ko"], "대통령 국정조사 관련 여야 충돌")
        duplicate = dict(parsed[0])
        duplicate["external_id"] = "changed-guid"
        duplicate["summary_ko"] = "핵심은 대통령 국정조사 관련 여야 충돌 입니다. 업데이트된 요약입니다."
        stats = upsert_news_items(conn, [duplicate])
        self.assertEqual(stats["updated"], 1)
        latest = latest_news_items(conn, limit=5)
        self.assertEqual(len(latest), 1)
        world_duplicate = dict(parsed[0])
        world_duplicate["source_id"] = "google_news_world_ko"
        world_duplicate["external_id"] = "world-guid"
        stats = upsert_news_items(conn, [world_duplicate])
        self.assertEqual(stats["updated"], 1)
        latest = latest_news_items(conn, limit=5)
        self.assertEqual(len(latest), 1)

    def test_categorize_news(self):
        self.assertEqual(categorize_news("AI 반도체 기업 실적 발표"), "경제")
        self.assertEqual(categorize_news("배우 신작 영화 공개"), "연예")


if __name__ == "__main__":
    unittest.main()
