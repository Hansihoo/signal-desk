import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from housing_watch.ai_brief import build_ai_news_pages, format_ai_issue_summary, render_ai_news_html
from housing_watch.ai_news import categorize_ai_news, filter_recent_ai_items, parse_ai_feed
from housing_watch.db import connect, init_db, latest_ai_news_items, upsert_news_items


RSS_SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item>
      <title>OpenAI announces a new GPT model for coding</title>
      <link>https://openai.com/news/example-gpt-coding</link>
      <guid isPermaLink="false">openai-example</guid>
      <pubDate>Fri, 19 Jun 2026 12:00:00 GMT</pubDate>
      <description><![CDATA[The update adds stronger tool use, API controls, and eval guidance for developers.]]></description>
    </item>
  </channel>
</rss>
""".encode("utf-8")


ATOM_SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>tag:github.com,2008:Repository/123/v1.2.3</id>
    <title>v1.2.3</title>
    <updated>2026-06-18T09:30:00Z</updated>
    <link rel="alternate" href="https://github.com/vllm-project/vllm/releases/tag/v1.2.3" />
    <content type="html">Improves inference throughput and fixes a serving regression.</content>
  </entry>
</feed>
""".encode("utf-8")


class AINewsTests(unittest.TestCase):
    def test_parse_rss_ai_feed(self):
        source = {
            "id": "ai_openai_news",
            "name": "OpenAI News",
            "feed_url": "https://openai.com/news/rss.xml",
            "home_url": "https://openai.com/news/",
            "tier": "official",
            "score_base": 150,
        }
        items = parse_ai_feed(RSS_SAMPLE, source, limit=3)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["source_id"], "ai_openai_news")
        self.assertEqual(items[0]["category"], "LLM 모델")
        self.assertEqual(items[0]["source_name"], "OpenAI News")
        self.assertIn("개발자는", items[0]["summary_ko"])
        payload = json.loads(items[0]["raw_payload"])
        self.assertIn("developer_impact", payload)
        self.assertIn("action_needed", payload)

    def test_parse_atom_release_feed(self):
        source = {
            "id": "ai_vllm_releases",
            "name": "vLLM releases",
            "feed_url": "https://github.com/vllm-project/vllm/releases.atom",
            "home_url": "https://github.com/vllm-project/vllm",
            "tier": "open-source",
            "score_base": 126,
            "category_hint": "오픈소스",
        }
        items = parse_ai_feed(ATOM_SAMPLE, source, limit=3)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category"], "오픈소스")
        self.assertEqual(items[0]["url"], "https://github.com/vllm-project/vllm/releases/tag/v1.2.3")
        self.assertIn("로컬 추론", json.loads(items[0]["raw_payload"])["developer_impact"])

    def test_categorize_ai_news(self):
        self.assertEqual(categorize_ai_news("Claude adds a new reasoning model"), "LLM 모델")
        self.assertEqual(categorize_ai_news("SDK deprecation notice for the API"), "API/플랫폼")
        self.assertEqual(categorize_ai_news("A new benchmark paper for agents"), "연구")

    def test_filter_recent_ai_items_keeps_week_window(self):
        now = datetime(2026, 6, 20, 0, 0, 0, tzinfo=timezone.utc)
        items = [
            {"title": "recent", "published_at": "2026-06-19T00:00:00+00:00"},
            {"title": "old", "published_at": "2026-06-01T00:00:00+00:00"},
            {"title": "undated", "published_at": ""},
        ]
        recent = filter_recent_ai_items(items, days=7, now=now)
        self.assertEqual([item["title"] for item in recent], ["recent", "undated"])
        strict = filter_recent_ai_items(items, days=7, now=now, include_undated=False)
        self.assertEqual([item["title"] for item in strict], ["recent"])

    def test_render_three_page_expandable_brief(self):
        conn = connect(":memory:")
        init_db(conn)
        ai_items = [
            _sample_item("ai_openai_news", "GPT coding model", "LLM 모델", 150),
            _sample_item("ai_litellm_releases", "LiteLLM proxy update", "API/플랫폼", 130),
            _sample_item("ai_vllm_releases", "vLLM serving release", "오픈소스", 125),
            _sample_item("ai_langgraph_releases", "LangGraph agent runtime", "AI 개발", 120),
            _sample_item("ai_huggingface_blog", "Agent benchmark paper", "연구", 115),
            _sample_item("ai_google_news_llm", "AI safety policy", "안전", 110),
        ]
        upsert_news_items(conn, ai_items, source_prefix="ai_%")
        upsert_news_items(conn, [_sample_item("google_news_top_ko", "General news", "경제", 200)])

        latest = latest_ai_news_items(conn, limit=20)
        self.assertEqual(len(latest), 6)
        self.assertTrue(all(item["source_id"].startswith("ai_") for item in latest))

        pages = build_ai_news_pages(latest, per_page=2)
        self.assertEqual(len(pages), 3)
        self.assertEqual([page["number"] for page in pages], [1, 2, 3])

        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "ai-news.html"
            render_ai_news_html(conn, str(output), per_page=2, max_width=645, active_page=2)
            html_text = output.read_text(encoding="utf-8")

        self.assertIn('data-page="1"', html_text)
        self.assertIn('data-page="2"', html_text)
        self.assertIn('data-page="3"', html_text)
        self.assertIn('class="page is-active" data-page="2"', html_text)
        self.assertIn("<details", html_text)
        self.assertIn("GPT coding model", html_text)
        self.assertIn("개발자 요약", html_text)
        self.assertIn("개발자 영향", html_text)
        self.assertIn("원문 보기", html_text)

        with patch("housing_watch.ai_news.now_utc", return_value=datetime(2026, 6, 20, tzinfo=timezone.utc)):
            summary = format_ai_issue_summary(conn, limit=6, days=7)
        self.assertIn("최근 7일 AI 이슈", summary)
        self.assertIn("GPT coding model", summary)


def _sample_item(source_id, title, category, score):
    payload = {
        "developer_impact": "개발자 영향: 의존성, 평가, 운영 정책을 확인해야 합니다.",
        "detail": "상세 내용: 릴리스 노트와 후속 링크를 확인할 가치가 있습니다.",
        "action_needed": "확인 작업: 현재 프로젝트와 겹치는지 점검합니다.",
        "source_tier": "test",
    }
    return {
        "source_id": source_id,
        "external_id": source_id + "-" + title.lower().replace(" ", "-"),
        "title": title,
        "title_ko": title,
        "url": "https://example.com/" + title.lower().replace(" ", "-"),
        "source_name": source_id,
        "source_url": "https://example.com",
        "category": category,
        "language": "English",
        "country": "",
        "published_at": "2026-06-19T00:00:00+00:00",
        "summary_ko": "개발자 요약: %s" % title,
        "score": score,
        "raw_payload": json.dumps(payload, ensure_ascii=False, sort_keys=True),
        "content_hash": title,
        "collected_at": "2026-06-20T00:00:00+00:00",
    }


if __name__ == "__main__":
    unittest.main()
