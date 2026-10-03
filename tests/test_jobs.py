import json
import tempfile
import unittest
from pathlib import Path

from housing_watch.db import connect, init_db, latest_job_items, upsert_job_items
from housing_watch.jobs import (
    dedupe_job_items,
    load_job_items_from_json,
    load_salary_estimates,
    normalize_job_item,
    parse_saramin_jobs,
    score_job_for_profile,
)


SARAMIN_SAMPLE = {
    "jobs": {
        "count": 2,
        "start": 0,
        "total": "2",
        "job": [
            {
                "url": "https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx=1",
                "active": 1,
                "company": {"detail": {"href": "https://example.com/company", "name": "예시테크"}},
                "position": {
                    "title": "시니어 C++ 엔진 개발자",
                    "industry": {"code": "301", "name": "솔루션·SI·ERP·CRM"},
                    "location": {"code": "101070", "name": "서울 > 구로구"},
                    "job-type": {"code": "1", "name": "정규직"},
                    "job-mid-code": {"code": "22", "name": "IT개발·데이터"},
                    "job-code": {"code": "2072", "name": "소프트웨어개발"},
                    "experience-level": {"code": 2, "min": 8, "max": 15, "name": "경력 8~15년"},
                    "required-education-level": {"code": "8", "name": "대학교졸업(4년)이상"},
                },
                "keyword": "C++,Windows,엔진,스프레드시트",
                "salary": {"code": "18", "name": "5,000~6,000만원"},
                "id": "1",
                "posting-date": "2026-06-18T13:46:04+0900",
                "expiration-date": "2026-07-10T23:59:59+0900",
                "close-type": {"code": "1", "name": "접수마감일"},
            },
            {
                "url": "https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx=2",
                "active": 1,
                "company": {"detail": {"name": "신입테크"}},
                "position": {
                    "title": "신입 개발자",
                    "location": {"name": "서울"},
                    "experience-level": {"code": 1, "min": 0, "max": 0, "name": "신입"},
                },
                "id": "2",
            },
        ],
    }
}


class JobTests(unittest.TestCase):
    def test_normalize_job_item_accepts_korean_field_names(self):
        item = normalize_job_item(
            {
                "회사명": "테스트소프트",
                "공고명": "C++ 오피스 엔진 개발자",
                "하는일": "문서/스프레드시트 엔진 개발",
                "자격요건": "C++ 경력 10년 이상",
                "우대사항": "Windows 데스크톱 개발 경험",
                "지역": "서울 강남",
                "10연차 연봉": "7,000만~9,000만원 추정",
                "마감일": "2026-07-10",
                "링크": "https://example.com/jobs/1",
            },
            source_id="test_jobs",
        )
        self.assertEqual(item["company_name"], "테스트소프트")
        self.assertEqual(item["posting_title"], "C++ 오피스 엔진 개발자")
        self.assertEqual(item["salary_10y"], "7,000만~9,000만원 추정")
        self.assertEqual(item["deadline_at"], "2026-07-10")
        self.assertGreater(item["fit_score"], 0)

    def test_load_job_items_from_json_list(self):
        payload = [
            {
                "company_name": "테스트테크",
                "posting_title": "시니어 C++ 개발자",
                "work_summary": "엔진 개발",
                "requirements": "C++ 경력",
                "preferred": "리드 경험",
                "location": "경기 판교",
                "salary_10y": "8,000만원 내외",
                "deadline_at": "2026-07-15",
                "url": "https://example.com/jobs/2",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "jobs.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            items, raw = load_job_items_from_json(str(path), source_id="test_jobs")
        self.assertEqual(len(items), 1)
        self.assertIn(b"C++", raw)
        self.assertEqual(items[0]["source_id"], "test_jobs")

    def test_upsert_and_latest_job_items(self):
        conn = connect(":memory:")
        init_db(conn)
        item = normalize_job_item(
            {
                "company_name": "테스트테크",
                "posting_title": "시니어 C++ 개발자",
                "work_summary": "스프레드시트 엔진 개발",
                "requirements": "C++ 10년 이상",
                "preferred": "오피스 개발 경험",
                "location": "서울",
                "salary_10y": "8,000만원 내외",
                "deadline_at": "2026-07-15",
                "url": "https://example.com/jobs/2",
            },
            source_id="test_jobs",
        )
        stats = upsert_job_items(conn, [item])
        self.assertEqual(stats["inserted"], 1)
        latest = latest_job_items(conn, limit=3)
        self.assertEqual(len(latest), 1)
        self.assertEqual(latest[0]["company_name"], "테스트테크")

        changed = dict(item)
        changed["external_id"] = "changed"
        changed["salary_10y"] = "8,500만원 내외"
        stats = upsert_job_items(conn, [changed])
        self.assertEqual(stats["updated"], 1)
        latest = latest_job_items(conn, limit=3)
        self.assertEqual(len(latest), 1)
        self.assertEqual(latest[0]["salary_10y"], "8,500만원 내외")

    def test_score_job_for_profile_prefers_engine_cpp_jobs(self):
        score = score_job_for_profile(
            {
                "posting_title": "시니어 C++ 엔진 개발자",
                "work_summary": "Windows 데스크톱 오피스 엔진 개발",
                "requirements": "C++ 경력 10년",
                "preferred": "스프레드시트 경험",
                "location": "서울",
                "seniority": "경력",
            }
        )
        self.assertGreaterEqual(score, 8)

    def test_parse_saramin_jobs_keeps_career_jobs(self):
        items = parse_saramin_jobs(
            SARAMIN_SAMPLE,
            source_id="saramin_test",
            query="C++ 엔진",
            salary_estimates={
                "예시테크": {
                    "salary_10y": "8,000만~1억원 추정",
                    "salary_basis": "테스트 연봉 조사",
                }
            },
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["company_name"], "예시테크")
        self.assertEqual(items[0]["posting_title"], "시니어 C++ 엔진 개발자")
        self.assertIn("소프트웨어개발", items[0]["work_summary"])
        self.assertIn("경력 8~15년", items[0]["requirements"])
        self.assertEqual(items[0]["location"], "서울 > 구로구")
        self.assertEqual(items[0]["salary_10y"], "8,000만~1억원 추정")
        self.assertEqual(items[0]["deadline_at"], "2026-07-10")
        self.assertEqual(items[0]["published_at"], "2026-06-18")

    def test_parse_saramin_jobs_marks_salary_for_separate_research(self):
        items = parse_saramin_jobs(SARAMIN_SAMPLE, source_id="saramin_test", query="C++ 엔진")
        self.assertEqual(items[0]["salary_10y"], "별도 조사 필요")
        self.assertIn("사람인 공고 연봉", items[0]["salary_basis"])

    def test_load_salary_estimates(self):
        payload = [
            {
                "company_name": "예시테크",
                "salary_10y": "8,000만~1억원 추정",
                "salary_basis": "테스트 연봉 조사",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "salary.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            estimates = load_salary_estimates(str(path))
        self.assertEqual(estimates["예시테크"]["salary_10y"], "8,000만~1억원 추정")

    def test_dedupe_job_items_prefers_higher_fit_score(self):
        first = {"company_name": "예시테크", "posting_title": "C++ 개발자", "url": "https://example.com/1", "fit_score": 3}
        second = dict(first)
        second["fit_score"] = 8
        deduped = dedupe_job_items([first, second])
        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0]["fit_score"], 8)


if __name__ == "__main__":
    unittest.main()
