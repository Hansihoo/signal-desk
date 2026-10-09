import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from housing_watch.db import connect
from housing_watch.research_data import load_report_input
from housing_watch.research_workflow import (
    PROFILES, REVIEW_CRITERIA, VERSION, body_review_input, collect_originals, digest,
    draft_issues, evidence_issues, first_screen, make_plan, quality_issues, report_nodes,
    run_research, verify_release,
)


def request(kind="technology"):
    return {"id": "document-rag-grounding", "topic_id": "opportunities", "topic_path": ["개발 관련 정보"],
            "reader": "문서 검색 AI를 만드는 개발자", "reader_question": "내 문서를 바탕으로 답하는 AI는 어떻게 만들고 오류를 찾는가?",
            "outcome": "검색과 답변 생성의 실패를 구분하고 정답 질문을 설계한다.", "research_type": kind,
            "plan_questions": False,
            "sources": [{"id": "source", "title": "Original", "url": "https://example.com/research", "kind": "official_document"}]}


def original(source):
    text = "An original defines retrieval and response generation as distinct steps. " * 3
    return text.encode(), "text/plain", source["url"]


def report_fixture():
    # Use a real v1 artifact; no duplicate toy rendering contract.
    report = copy.deepcopy(load_report_input("config/reader_refinement.2026-10-09.json")[0])
    report.update(id="document-rag-grounding", topic_id="opportunities", title="문서 검색 AI의 동작과 오류 구분", deck="질문에 필요한 문단을 찾아 AI에게 제공하고 답변의 근거를 대조한다.")
    report["references"] = [{"id": "source", "title": "Original", "url": "https://example.com/research", "description": "Fixture original"}]
    for _, node in report_nodes(report):
        node["source_ids"] = ["source"] if node.get("kind") != "example" else []
    return report


class FakeProvider:
    identity = "offline-routing-fixture-v1"

    def __init__(self, repair_stage=None):
        self.calls = []
        self.repair_stage = repair_stage
        self.failed = False

    def generate(self, stage, payload, max_output_tokens):
        self.calls.append((stage, copy.deepcopy(payload)))
        if stage == "plan":
            return {"document":{"research_type":"technology", "questions":[{"id":"core", "question":"How do retrieval and response errors differ?", "requires":PROFILES["technology"]["requires"]}]}}
        if stage == "analyze":
            source = payload["sources"][0]
            doc = {"evidence": [{"id": "e1", "source_id": source["id"], "source_hash": source["content_hash"],
                                 "quote": "retrieval and response generation as distinct steps", "meaning": "検索と生成は別工程。",
                                 "limits": "Fixture, not performance evidence", "supports": PROFILES["technology"]["requires"]}],
                   "answers": [{"question_id": "core", "answer": "検索資料と最終回答を別々に確認する。", "reasoning": "Different stages need different fixes",
                                "evidence_ids": ["e1"], "limits": "No SDK run"}], "gaps": []}
            return {"document": doc}
        if stage == "write":
            report = report_fixture()
            if self.failed:
                report["explanation"][0]["lead"] += " After actual repair, search input and response output are compared separately."
            doc = {"report": report, "claims": [{"path": path, "kind": "example" if node.get("kind") == "example" else "fact" if node.get("kind") == "fact" or path.startswith(("/tables/", "/metrics/")) else "inference", "evidence_ids": [] if node.get("kind") == "example" else ["e1"]} for path, node in report_nodes(report)],
                   "answer_paths": {"core": ["/explanation/0"]}}
            return {"document": doc}
        checks = {k: {"passed": True, "reason": "Offline routing fixture only; not a semantic verdict", "locations": ["deck" if stage == "review_first_screen" else "/explanation/0"]}
                  for k in (REVIEW_CRITERIA if stage == "review_body" else ("readability", "question_answered", "reader_outcome"))}
        findings = []
        if stage == "review_body" and self.repair_stage and not self.failed:
            findings = [{"stage": self.repair_stage, "code": "fixture_defect", "detail": "Missing evidence or explanation at /explanation/0"}]
            self.failed = True
        return {"document": {"input_hash": digest(payload), "checks": checks, "issues": findings}}


class ResearchWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.conn.close)
        self.addCleanup(self.temp.cleanup)

    def run_workflow(self, provider=None, **kwargs):
        return run_research(self.conn, request(), provider or FakeProvider(), self.temp.name, fetcher=original, **kwargs)

    def test_type_profiles_and_custom_method(self):
        self.assertNotEqual(make_plan(request("market"))["questions"], make_plan(request())["questions"])
        r = request("custom")
        with self.assertRaises(ValueError):
            make_plan(r)
        r["custom_profile"] = {"method": "Evaluate policy conditions", "requires": ["effective_date", "eligibility"]}
        self.assertIn("effective_date", make_plan(r)["questions"][0]["requires"])
        r["questions"] = [{"id": "q", "question": "Question", "requires": ["eligibility"]}]
        with self.assertRaisesRegex(ValueError, "omit profile"):
            make_plan(r)

    def test_auto_classification_and_question_planning_precede_collection(self):
        r = request("auto")
        p = FakeProvider()
        package = run_research(self.conn,r,p,self.temp.name,fetcher=original)
        self.assertEqual(package["status"], "ready", package["issues"])
        self.assertEqual(p.calls[0][0], "plan")
        self.assertEqual(package["plan"]["request"]["research_type"], "technology")
        self.assertEqual(package["usage"]["calls"],5)

    def test_four_stage_run_and_unchanged_cache_zero_paid_calls(self):
        p = FakeProvider()
        first = self.run_workflow(p)
        self.assertEqual(first["status"], "ready", first["issues"])
        self.assertEqual([s for s, _ in p.calls], ["analyze", "write", "review_first_screen", "review_body"])
        screen = p.calls[2][1]
        self.assertEqual(set(screen), {"title", "description", "deck"})
        second = self.run_workflow(FakeProvider())
        self.assertEqual(second["status"], "ready", second["issues"])
        self.assertEqual(second["usage"]["calls"], 0)
        self.assertEqual(second["usage"]["cache_hits"], 4)
        self.assertEqual(second["sources"][0]["last_successful_collection"], first["sources"][0]["last_successful_collection"])

    def test_auto_plan_with_existing_questions_and_discovered_original(self):
        r = request("auto")
        source = r.pop("sources")[0]
        r["allowed_domains"] = ["example.com"]
        r["questions"] = [{"id": "candidate", "question": "Which retrieval failures matter?", "requires": ["mechanism"]}]
        searches = []
        def search(question, domains):
            searches.append((question, domains))
            return [source]
        package = run_research(self.conn, r, FakeProvider(), self.temp.name, fetcher=original, searcher=search)
        self.assertEqual(package["status"], "ready", package["issues"])
        self.assertEqual(package["plan"]["request"]["research_type"], "technology")
        self.assertEqual(package["usage"]["searches"], 1)
        self.assertEqual(package["usage"]["fetches"], 1)
        self.assertEqual(len(searches), 1)
        verify_release([package["draft"]["report"]], [package])

    def test_repair_routes_to_analysis_or_writing(self):
        for stage in ("analysis", "writing"):
            with self.subTest(stage=stage):
                conn = connect(":memory:")
                p = FakeProvider(stage)
                package = run_research(conn, request(), p, self.temp.name, fetcher=original)
                conn.close()
                self.assertEqual(package["status"], "ready", package["issues"])
                self.assertEqual(package["events"][1]["stage"], stage)
                stages = [s for s, _ in p.calls]
                self.assertEqual(stages.count("analyze"), 2 if stage == "analysis" else 1)

    def test_missing_evidence_searches_then_recollects_not_rewords(self):
        p = FakeProvider("research")
        r = request()
        r["allowed_domains"] = ["example.com"]
        calls = []
        def search(q, domains):
            calls.append(q)
            return [dict(r["sources"][0], id="extra", url="https://example.com/more")]
        package = run_research(self.conn, r, p, self.temp.name, fetcher=original, searcher=search)
        self.assertEqual(package["status"], "ready", package["issues"])
        self.assertEqual(package["usage"]["searches"], 1)
        self.assertEqual(package["usage"]["fetches"], 2)
        self.assertEqual([x for x, _ in p.calls].count("analyze"), 2)

    def test_research_gap_without_search_adapter_blocks(self):
        package = self.run_workflow(FakeProvider("research"))
        self.assertEqual(package["status"], "blocked")
        self.assertEqual(package["issues"][0]["stage"], "research")

    def test_call_input_fetch_and_round_limits_stop(self):
        for limits in ({"calls": 1}, {"input_chars": 5}, {"fetches": 0}, {"rounds": 0}):
            with self.subTest(limits=limits):
                conn = connect(":memory:")
                package = run_research(conn, request(), FakeProvider(), self.temp.name, limits=limits, fetcher=original)
                conn.close()
                self.assertEqual(package["status"], "blocked")
                self.assertTrue(package["issues"])

    def test_failed_refresh_does_not_refresh_or_use_stale_original(self):
        first, _ = collect_originals(self.conn, request()["sources"], self.temp.name, fetcher=original)
        def failed(_):
            raise OSError("unavailable")
        second, _ = collect_originals(self.conn, request()["sources"], self.temp.name, max_age_hours=0, fetcher=failed)
        self.assertEqual(second[0]["status"], "failed")
        self.assertNotIn("text", second[0])
        stored = json.loads(self.conn.execute("SELECT document FROM research_originals").fetchone()[0])
        self.assertEqual(stored["last_successful_collection"], first[0]["last_successful_collection"])

    def test_forged_quote_hash_measurement_and_seller_case_rejected(self):
        package = self.run_workflow()
        for field, value, expected in (("quote", "not actually in the original source", "original_support"),
                                      ("source_hash", "bad", "original_support"),
                                      ("supports", ["measurement"], "measurement_scope"),
                                      ("supports", ["actual_case"], "actual_case_type")):
            a = copy.deepcopy(package["analysis"])
            a["evidence"][0][field] = value
            found = evidence_issues(package["plan"], package["sources"], a)
            self.assertIn(expected, [x["code"] for x in found])

    def test_posted_budget_is_not_paid_price(self):
        package = self.run_workflow()
        package["sources"][0]["kind"] = "buyer_posting"
        e = package["analysis"]["evidence"][0]
        e.update(supports=["price"], price_type="paid_amount")
        self.assertIn("price_type", [x["code"] for x in evidence_issues(package["plan"], package["sources"], package["analysis"])])

    def test_stale_review_changed_report_and_unmapped_claim_rejected(self):
        package = self.run_workflow()
        report = package["draft"]["report"]
        verify_release([report], [package])
        altered = copy.deepcopy(report)
        altered["title"] += " changed"
        with self.assertRaisesRegex(ValueError, "bind"):
            verify_release([altered], [package])
        package["draft"]["report"]["deck"] += " changed"
        self.assertIn("stale_review", [x["code"] for x in quality_issues(package)])
        package["draft"]["claims"] = []
        self.assertIn("unmapped_claim", [x["code"] for x in quality_issues(package)])

    def test_source_text_tampering_and_citation_url_drift_rejected(self):
        package = self.run_workflow()
        package["sources"][0]["text"] += " tampered"
        self.assertIn("original_integrity", [x["code"] for x in quality_issues(package)])
        package = self.run_workflow()
        package["draft"]["report"]["references"][0]["url"] += "/other"
        self.assertIn("reference_url", [x["code"] for x in quality_issues(package)])

    def test_provider_needs_explicit_key_and_does_not_log_it(self):
        from housing_watch.research_provider import ResponsesProvider
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "no paid call"):
                ResponsesProvider("explicit-model")

    def test_real_market_and_technology_pilot_release_and_regression(self):
        reports = load_report_input("config/research_quality_pilot.2026-10-09.json")
        packages = json.loads(Path("config/research_quality_pilot.2026-10-09.quality.json").read_text(encoding="utf-8"))["packages"]
        verify_release(reports, packages)
        market = next(r for r in reports if r["id"] == "upwork-ai-integration-demand")
        self.assertNotIn("수요 신호", market["title"] + market["deck"])
        self.assertTrue(any(s["kind"] == "buyer_posting" for s in packages[0]["sources"]))
        self.assertIn("1,500", json.dumps(market, ensure_ascii=False))
        self.assertEqual(packages[0]["plan"]["request"]["research_type"], "market")
        self.assertEqual(packages[1]["plan"]["request"]["research_type"], "technology")
        self.assertIn("worked_example", packages[1]["analysis"]["evidence"][1]["supports"])
        damaged = copy.deepcopy(packages)
        damaged[0]["sources"] = [s for s in damaged[0]["sources"] if s["kind"] != "buyer_posting"]
        with self.assertRaisesRegex(ValueError, "quality gate"):
            verify_release(reports, damaged)

    def test_quality_batch_immutability_and_rollback(self):
        from housing_watch.research_data import apply_publication, load_publication
        publication, batches = load_publication()
        apply_publication(self.conn, publication, batches)
        before = self.conn.execute("SELECT COUNT(*) FROM research_report_revisions").fetchone()[0]
        changed = copy.deepcopy(batches)
        changed[-1][1].quality_packages[0]["body_review"]["checks"]["analysis"]["reason"] += " changed"
        with self.assertRaisesRegex(ValueError, "new batch ID"):
            apply_publication(self.conn, publication, changed)
        self.assertEqual(before, self.conn.execute("SELECT COUNT(*) FROM research_report_revisions").fetchone()[0])
        altered = copy.deepcopy(batches)
        altered[-1][1][0]["deck"] += " altered"
        with self.assertRaisesRegex(ValueError, "bind"):
            apply_publication(self.conn, publication, altered)
        self.assertEqual(before, self.conn.execute("SELECT COUNT(*) FROM research_report_revisions").fetchone()[0])

    def test_changed_original_invalidates_cached_generation(self):
        first = self.run_workflow()
        def changed(source):
            body,mime,url = original(source)
            return body + b" Original revised.", mime, url
        second = run_research(self.conn, request(), FakeProvider(), self.temp.name, fetcher=changed, limits={"max_age_hours":0})
        self.assertEqual(second["status"], "ready", second["issues"])
        self.assertGreater(second["usage"]["calls"], 0)
        self.assertNotEqual(first["sources"][0]["content_hash"], second["sources"][0]["content_hash"])
        self.assertEqual(first["sources"][0]["first_collected"], second["sources"][0]["first_collected"])

    def test_invalid_review_location_and_blocked_package_are_rejected(self):
        package = self.run_workflow()
        package["body_review"]["checks"]["evidence"]["locations"] = ["/missing/claim"]
        self.assertIn("review_location", [x["code"] for x in quality_issues(package)])
        package["status"] = "blocked"
        self.assertIn("workflow_not_ready", [x["code"] for x in quality_issues(package)])

    def test_provider_payload_binding_refusal_and_web_search_url_provenance(self):
        from housing_watch.research_provider import ResponsesProvider
        calls = []
        results = []
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, count): return json.dumps(results.pop(0)).encode()
        def opener(req, timeout):
            calls.append(json.loads(req.data.decode()))
            return Response()
        with patch.dict(os.environ, {"OPENAI_API_KEY":"offline-secret"}):
            p = ResponsesProvider("explicit-writer", "explicit-reviewer", discovery=True, opener=opener)
            def result(doc, extra=None):
                return {"status":"completed", "output":[{"type":"message","content":[{"type":"output_text","text":json.dumps(doc)}]}] + (extra or []), "usage":{"input_tokens":5,"output_tokens":7}}
            results.append(result({"checks":{},"issues":[]}))
            payload = first_screen(report_fixture())
            response = p.generate("review_first_screen", payload, 100)
            self.assertEqual(response["document"]["input_hash"], digest(payload))
            self.assertEqual(calls[0]["model"], "explicit-reviewer")
            self.assertFalse(calls[0]["store"])
            self.assertEqual(json.loads(calls[0]["input"]), payload)
            self.assertNotIn("offline-secret", p.identity)
            results.append(result({"sources":[{"url":"https://example.com/real"},{"url":"https://example.com/invented"}]},
                                  [{"type":"web_search_call","action":{"sources":[{"url":"https://example.com/real"}]}}]))
            response = p.generate("discover", {"question":"question","allowed_domains":["example.com"]}, 100)
            self.assertEqual(response["document"]["sources"], [{"url":"https://example.com/real"}])
            self.assertEqual(calls[-1]["max_tool_calls"], 1)
            self.assertEqual(response["usage"]["web_search_calls"], 1)
            results.append({"status":"incomplete"})
            with self.assertRaisesRegex(ValueError, "incomplete"):
                p.generate("write", {}, 100)
            self.assertEqual(len(calls), 3)


if __name__ == "__main__":
    unittest.main()
