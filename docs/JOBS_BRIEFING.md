# Jobs Briefing

The jobs domain is the second Signal Desk domain after housing/news.

## Scope

Target use case:

- Theo asks Codex whether there are new career-change opportunities from the last week.
- Signal Desk keeps career job records normalized locally.
- The mobile `jobs` tab shows enough detail to decide whether the posting is worth opening.

Current MVP status:

- normalized `job_items` table,
- JSON import command,
- Saramin Open API live fetch command,
- profile-lite scoring for C++/engine/office/desktop work,
- `jobs` tab in `site/desk.html`,
- `reports/desk-jobs.png` export.

WorkNet and official company career-page adapters should feed the same normalized fields next.

## Card Field Contract

Visible fields requested by Theo:

- 회사명
- 공고명
- 하는일
- 자격요건
- 우대사항
- 지역
- 10년차 연봉
- 마감일
- 링크

Internal support fields:

- `salary_basis`: how the 10-year salary estimate was researched.
- `fit_score`: local relevance score for Theo's profile.
- `source_id`, `external_id`, `raw_payload`, `content_hash`: source traceability and dedupe.

## Import Shape

Example:

```json
[
  {
    "company_name": "예시테크",
    "posting_title": "시니어 C++ 오피스 엔진 개발자",
    "work_summary": "문서 편집기와 스프레드시트 엔진 성능 개선",
    "requirements": "C++ 개발 경력 8년 이상",
    "preferred": "오피스 제품 또는 문서 엔진 개발 경험",
    "location": "서울 또는 경기 판교",
    "salary_10y": "7,500만~9,500만원 추정",
    "salary_basis": "채용 플랫폼, 연봉 리뷰, 기업 공시를 분리 조사",
    "deadline_at": "2026-07-15",
    "url": "https://example.com/jobs/senior-cpp-office-engine"
  }
]
```

Korean aliases such as `회사명`, `공고명`, `하는일`, `자격요건`, `우대사항`, `지역`, `10년차 연봉`, `마감일`, and `링크` are accepted.

## Commands

```powershell
python -m housing_watch jobs --input config/jobs.example.json --no-image
python -m housing_watch jobs --fetch saramin --no-image
python -m housing_watch desk --tab jobs --width 645 --height 1500
```

Use `--no-render` when importing only.

```powershell
python -m housing_watch jobs --input path\to\jobs.json --source-id saramin_career --no-render
```

Saramin live fetch requires:

```powershell
$env:SIGNAL_DESK_SARAMIN_KEY="..."
python -m housing_watch jobs --fetch saramin --keyword "C++ 엔진" --keyword "오피스 개발" --no-image
```

Default live fetch options live in `config/job_sources.json`.

Salary estimates are separate:

```powershell
python -m housing_watch jobs --fetch saramin --salary-estimates config/job_salary_estimates.example.json
```

## Source Strategy

Recommended order:

1. Saramin API for broad career-market coverage.
2. Official company career pages for large and mid-sized companies Theo cares about.
3. WorkNet/Work24 APIs for official public job data after API approval.
4. Wanted/JobKorea or community/news sources only when terms and access are acceptable.

Do not commit API keys, cookies, logged-in pages, or Theo's profile file.

## Official References

- Saramin Job Search API: `https://oapi.saramin.co.kr/guide/job-search`
- Work24 Open API introduction: `https://www.work24.go.kr/cm/e/a/0110/selectOpenApiIntro.do`
- Data.go.kr WorkNet job API: `https://www.data.go.kr/data/3038225/openapi.do`

## Current Limitations

- Saramin does not provide detailed responsibilities/requirements/preferred qualifications in the list API, so the card summarizes title, job code, keywords, experience, education, and points to the original posting for details.
- `salary_10y` is filled only from a separate salary-estimate mapping; otherwise it stays `별도 조사 필요`.
- Company-size filtering is approximate. The default Saramin query uses listed-company filters, but official company watchlists are still needed for exact large/mid-sized company coverage.
