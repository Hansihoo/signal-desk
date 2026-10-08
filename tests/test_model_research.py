import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from housing_watch.ai_news import AI_FEEDS, _model_news_source, collect_ai_news, parse_ai_feed
from housing_watch.db import connect, init_db
from housing_watch.model_research import CONFIG_PATH, SOURCE_ID, collect_model_research, parse_model_catalog
from housing_watch.public_site import public_library


def catalog():
    return {"documents": [{"slug": "llm-models", "title": "모델 통합 비교", "description": "조건별 비교",
                            "category": "모델 리서치", "updatedAt": "2026-10-07", "referenceDate": "2026-09-30", "sha256": "a" * 64}]}


class ModelResearchTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        self.conn = connect(":memory:")
        init_db(self.conn)
        self.addCleanup(self.conn.close)
        ledger = patch("housing_watch.ai_news.collect_model_ledger", return_value={"inserted": 0, "updated": 0, "unchanged": 0, "fetched": 0, "retained": 0})
        ledger.start()
        self.addCleanup(ledger.stop)
        pages = patch("housing_watch.ai_news.collect_model_pages", return_value={"failures": []})
        pages.start()
        self.addCleanup(pages.stop)

    def test_dates_provenance_and_scope(self):
        document = catalog()
        document["documents"].append(dict(document["documents"][0], slug="windows-guide", category="업무 활용"))
        with patch("housing_watch.model_research.iso_utc", return_value="2026-10-08T00:00:00Z"):
            items = parse_model_catalog(document, self.config)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category"], "LLM 모델")
        self.assertEqual(items[0]["published_at"], "2026-10-07T00:00:00Z")
        payload = json.loads(items[0]["raw_payload"])
        self.assertEqual(payload["reference_date"], "2026-09-30")
        self.assertEqual(payload["source_tier"], "authored-research")
        document["documents"][0]["referenceDate"] = None
        self.assertEqual(json.loads(parse_model_catalog(document, self.config)[0]["raw_payload"])["reference_date"], "")

    def test_repeat_then_hash_change_then_title_change_keeps_identity(self):
        document = catalog()
        with tempfile.TemporaryDirectory() as directory, patch("housing_watch.model_research._read_catalog") as read:
            read.return_value = json.dumps(document).encode()
            self.assertEqual(collect_model_research(self.conn, directory)["inserted"], 1)
            original = dict(self.conn.execute("SELECT * FROM news_items").fetchone())
            result = collect_model_research(self.conn, directory)
            self.assertEqual((result["inserted"], result["updated"], result["unchanged"]), (0, 0, 1))
            document["documents"][0]["sha256"] = "b" * 64
            read.return_value = json.dumps(document).encode()
            self.assertEqual(collect_model_research(self.conn, directory)["updated"], 1)
            document["documents"][0]["title"] = "모델 통합 비교 개정"
            read.return_value = json.dumps(document).encode()
            self.assertEqual(collect_model_research(self.conn, directory)["updated"], 1)
            current = dict(self.conn.execute("SELECT * FROM news_items").fetchone())
            self.assertEqual(current["id"], original["id"])
            self.assertEqual(current["first_seen_at"], original["first_seen_at"])
            self.assertNotEqual(current["content_hash"], original["content_hash"])

    def test_distinct_documents_with_same_title_are_preserved(self):
        document = catalog()
        document["documents"].append(dict(document["documents"][0], slug="another-model", sha256="b" * 64))
        with tempfile.TemporaryDirectory() as directory, patch("housing_watch.model_research._read_catalog", return_value=json.dumps(document).encode()):
            result = collect_model_research(self.conn, directory)
        self.assertEqual(result["inserted"], 2)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM news_items").fetchone()[0], 2)

    def test_invalid_catalog_retains_previous_rows_and_creates_no_snapshot(self):
        with tempfile.TemporaryDirectory() as directory, patch("housing_watch.model_research._read_catalog") as read:
            read.return_value = json.dumps(catalog()).encode()
            collect_model_research(self.conn, directory)
            before = list(self.conn.execute("SELECT * FROM news_items"))
            for mutation in ({"slug": "../escape"}, {"updatedAt": "2026-02-30"}, {"sha256": "missing"}):
                invalid = catalog()
                invalid["documents"][0].update(mutation)
                read.return_value = json.dumps(invalid).encode()
                with self.assertRaises(ValueError):
                    collect_model_research(self.conn, directory)
                self.assertEqual(list(self.conn.execute("SELECT * FROM news_items")), before)
            self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM raw_snapshots").fetchone()[0], 1)
            self.assertEqual(len(list(Path(directory).glob("theo_model_catalog_*.json"))), 4)

    def test_duplicate_slug_is_rejected_before_import(self):
        document = catalog()
        document["documents"].append(copy.deepcopy(document["documents"][0]))
        with self.assertRaises(ValueError):
            parse_model_catalog(document, self.config)

    def test_public_export_distinguishes_authored_research(self):
        with tempfile.TemporaryDirectory() as directory, patch("housing_watch.model_research._read_catalog", return_value=json.dumps(catalog()).encode()):
            collect_model_research(self.conn, directory)
        entry = public_library(self.conn)[0]
        self.assertEqual((entry["topic_id"], entry["category"]), ("ai", "LLM 모델"))
        self.assertIn("공식 원문 재확인 필요", entry["basis"])
        self.assertTrue(entry["url"].endswith("/docs/llm-models/"))

    def test_new_model_search_is_candidate_and_uses_model_category(self):
        source = _model_news_source(3)
        self.assertEqual(source["tier"], "news-search")
        self.assertIn("when%3A3d", source["feed_url"])
        items = parse_ai_feed(b'<rss><channel><item><title>Aster launches</title><link>https://example.org/model</link></item></channel></rss>', source)
        self.assertEqual(items[0]["category"], "LLM 모델")
        self.assertEqual(json.loads(items[0]["raw_payload"])["source_tier"], "news-search")

    def test_model_catalog_failure_does_not_block_official_feed(self):
        body = b'<rss><channel><item><title>New coding model</title><link>https://openai.com/example</link></item></channel></rss>'
        with tempfile.TemporaryDirectory() as directory, patch("housing_watch.ai_news._read_url", return_value=body), patch("housing_watch.ai_news.collect_model_research", side_effect=OSError("offline")):
            result = collect_ai_news(self.conn, raw_dir=directory)
        self.assertGreater(result["fetched"], 0)
        self.assertTrue(any(SOURCE_ID in message for message in result["failures"]))

    def test_feed_and_catalog_same_title_keep_both_sources(self):
        document = catalog()
        body = '<rss><channel><item><title>모델 통합 비교</title><link>https://openai.com/example</link></item></channel></rss>'.encode()
        with tempfile.TemporaryDirectory() as directory, patch("housing_watch.ai_news._read_url", return_value=body), patch("housing_watch.model_research._read_catalog", return_value=json.dumps(document).encode()):
            collect_ai_news(self.conn, raw_dir=directory)
            collect_ai_news(self.conn, raw_dir=directory)
        source_ids = {row[0] for row in self.conn.execute("SELECT source_id FROM news_items")}
        self.assertIn(SOURCE_ID, source_ids)
        self.assertTrue(source_ids & {source["id"] for source in AI_FEEDS})


if __name__ == "__main__":
    unittest.main()
