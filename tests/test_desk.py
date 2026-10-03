import tempfile
import unittest
from pathlib import Path

from housing_watch.db import connect, init_db, upsert_items, upsert_job_items, upsert_news_items
from housing_watch.desk import _rank_news_for_briefing, render_desk_html


class DeskRenderTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        init_db(self.conn)
        upsert_items(
            self.conn,
            [
                {
                    "source_id": "test",
                    "external_id": "1",
                    "title": "2026년 서울 행복주택 입주자 모집공고",
                    "url": "https://example.com/notice/1",
                    "agency": "SH",
                    "category": "행복주택",
                    "region": "서울",
                    "status": "모집중",
                    "published_at": "2026-06-18",
                    "deadline_at": "2026-07-01",
                    "summary": "서울 행복주택 모집중",
                    "raw_text": "서울 행복주택 입주자 모집",
                    "content_hash": "abc",
                    "address": "서울특별시 강남구 테스트로 1",
                    "area_range_m2": "36~59㎡",
                    "area_range_pyeong": "10.9~17.8평",
                    "supply_units": "120호",
                    "deposit": "5,000만원",
                    "monthly_rent": "20만원",
                    "eligibility": "청년, 신혼부부",
                    "application_period": "2026-06-20 ~ 2026-07-01",
                    "collected_at": "2026-06-18T00:00:00Z",
                }
            ],
            {"keywords": ["행복주택"], "regions": ["서울"], "preferred_statuses": ["모집중"]},
        )
        upsert_news_items(
            self.conn,
            [
                {
                    "source_id": "google_news_top_ko",
                    "external_id": "news-1",
                    "title": "AI 반도체 시장 급등",
                    "title_ko": "AI 반도체 시장 급등",
                    "url": "https://news.google.com/rss/articles/news-1",
                    "source_name": "테스트뉴스",
                    "source_url": "https://example.com",
                    "category": "기술",
                    "language": "Korean",
                    "country": "KR",
                    "published_at": "2026-06-18T21:00:00+00:00",
                    "summary_ko": "기술 분야의 상위 노출 뉴스입니다.",
                    "score": 120,
                    "raw_payload": "{}",
                    "content_hash": "news-hash",
                    "collected_at": "2026-06-18T00:00:00Z",
                }
            ]
        )
        upsert_job_items(
            self.conn,
            [
                {
                    "source_id": "test_jobs",
                    "external_id": "job-1",
                    "company_name": "테스트테크",
                    "posting_title": "시니어 C++ 오피스 엔진 개발자",
                    "work_summary": "스프레드시트 엔진과 Windows 데스크톱 기능 개발",
                    "requirements": "C++ 개발 경력 10년 이상",
                    "preferred": "오피스 제품 또는 문서 엔진 개발 경험",
                    "location": "서울 강남",
                    "salary_10y": "8,000만~9,500만원 추정",
                    "salary_basis": "채용 플랫폼/연봉 리뷰 별도 조사",
                    "deadline_at": "2026-07-10",
                    "url": "https://example.com/jobs/1",
                    "company_size": "중견기업",
                    "seniority": "경력",
                    "fit_score": 9,
                    "raw_payload": "{}",
                    "content_hash": "job-hash",
                    "collected_at": "2026-06-18T00:00:00Z",
                }
            ]
        )

    def test_desk_html_has_tabs_and_mobile_width(self):
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "desk.html"
            render_desk_html(self.conn, str(html_path), active_tab="summary", item_limit=5)
            text = html_path.read_text(encoding="utf-8")
            self.assertIn("중요 요약", text)
            self.assertIn("청약", text)
            self.assertIn("주간 빅뉴스", text)
            self.assertIn("이직 공고", text)
            self.assertIn("max-width: 645px", text)
            self.assertIn('data-panel="summary"', text)
            self.assertIn('class="panel active" data-panel="summary"', text)
            self.assertIn("서울특별시 강남구 테스트로 1", text)
            self.assertIn("청약 핵심 스냅샷", text)
            self.assertIn("확인 포인트", text)
            self.assertIn("공식 링크", text)
            self.assertIn("AI 반도체 시장 급등", text)
            self.assertIn("시니어 C++ 오피스 엔진 개발자", text)

    def test_desk_can_export_a_different_active_tab_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "desk-weekly.html"
            render_desk_html(self.conn, str(html_path), active_tab="weekly-news", item_limit=5, max_width=390)
            text = html_path.read_text(encoding="utf-8")
            self.assertIn('class="panel active" data-panel="weekly-news"', text)
            self.assertIn("AI 반도체 시장 급등", text)
            self.assertNotIn("테스트뉴스", text)

    def test_desk_can_hide_profile_excluded_housing_items(self):
        profile_text = """
- 생년월일: 1988-11-20
- 가구: 미혼 1인가구
- 연봉: 약 6,400 만 원

### 자산

| 항목 | 금액 |
| --- | --- |
| 주식 | 4,000만원 |
| 전세보증금 | 2억원 |
| 현금 | 200만원 |
"""
        with tempfile.TemporaryDirectory() as tmp:
            profile_path = Path(tmp) / "profile.md"
            profile_path.write_text(profile_text, encoding="utf-8")
            html_path = Path(tmp) / "desk-profile.html"
            render_desk_html(
                self.conn,
                str(html_path),
                active_tab="housing",
                item_limit=5,
                max_width=390,
                profile_path=str(profile_path),
            )
            text = html_path.read_text(encoding="utf-8")
            self.assertIn("프로필 제외 1건", text)
            self.assertIn("프로필 기준으로 남은 청약 공고가 없습니다", text)
            self.assertNotIn("서울특별시 강남구 테스트로 1", text)

    def test_desk_can_render_jobs_tab_with_requested_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "desk-jobs.html"
            render_desk_html(self.conn, str(html_path), active_tab="jobs", item_limit=5, max_width=390)
            text = html_path.read_text(encoding="utf-8")
            self.assertIn('class="panel active" data-panel="jobs"', text)
            self.assertIn("회사명", text)
            self.assertIn("공고명", text)
            self.assertIn("하는일", text)
            self.assertIn("자격요건", text)
            self.assertIn("우대사항", text)
            self.assertIn("지역", text)
            self.assertIn("10년차", text)
            self.assertIn("마감일", text)
            self.assertIn("테스트테크", text)
            self.assertIn("8,000만~9,500만원 추정", text)

    def test_news_ranking_limits_politics(self):
        items = [
            {"title_ko": "정치 1", "category": "정치"},
            {"title_ko": "정치 2", "category": "정치"},
            {"title_ko": "정치 3", "category": "정치"},
            {"title_ko": "경제 1", "category": "경제"},
            {"title_ko": "사회 1", "category": "사회"},
            {"title_ko": "국제 1", "category": "국제"},
        ]
        ranked = _rank_news_for_briefing(items, limit=5, politics_limit=2)
        self.assertEqual([item["category"] for item in ranked], ["경제", "사회", "국제", "정치", "정치"])


if __name__ == "__main__":
    unittest.main()
