# Data Model

## Authored research reports

`research_reports`: stable ID, current revision, content hash, JSON document, UTC
update time. `research_report_revisions`: report ID/revision key, hash, immutable
document, saved time. Identical imports leave both unchanged; edits add a revision.
Generated `data/research.json` and `site/research-data.json` export current public
sources and reports under version 1. SQLite remains canonical. See
[research data contract](RESEARCH_DATA.md).

## SQLite

Default path:

```text
data/housing_watch.sqlite
```

The DB is generated locally and ignored by git.

## `items`

Core fields:

- `source_id`
- `external_id`
- `title`
- `url`
- `agency`
- `category`
- `region`
- `status`
- `published_at`
- `deadline_at`
- `summary`
- `raw_text`
- `content_hash`
- `state`
- `importance`
- `first_seen_at`
- `last_seen_at`

Housing detail fields:

- `address`
- `area_range_m2`
- `area_range_pyeong`
- `supply_units`
- `deposit`
- `monthly_rent`
- `price`
- `eligibility`
- `application_period`
- `move_in_month`
- `detail_summary`
- `detail_text`
- `detail_collected_at`

## `news_items`

Weekly big-news fields:

- `source_id`
- `external_id`
- `title`
- `title_ko`
- `url`
- `source_name`
- `source_url`
- `category`
- `language`
- `country`
- `published_at`
- `summary_ko`
- `score`
- `raw_payload`
- `content_hash`
- `first_seen_at`
- `last_seen_at`

Notes:

- GDELT records should use original article URLs when available.
- Google News RSS fallback records use Google News article links and keep the publisher name/source homepage when exposed by RSS.
- `title_ko` is a Korean title field. Korean RSS titles are copied directly; non-Korean titles require an optional LibreTranslate-compatible endpoint for real machine translation.
- AI developer news uses the same table with `source_id` values prefixed by `ai_`.
- AI developer news stores card expansion fields in `raw_payload` JSON: `developer_impact`, `detail`, `action_needed`, `source_tier`, `feed_url`, and `home_url`.
- `latest_ai_news_items` reads only `ai_%` rows so the AI briefing does not mix with broad weekly news.

## `job_items`

Career job fields:

- `source_id`
- `external_id`
- `company_name`
- `posting_title`
- `work_summary`
- `requirements`
- `preferred`
- `location`
- `salary_10y`
- `salary_basis`
- `deadline_at`
- `url`
- `source_name`
- `company_size`
- `seniority`
- `employment_type`
- `published_at`
- `fit_score`
- `raw_payload`
- `content_hash`
- `first_seen_at`
- `last_seen_at`

Visible jobs card contract:

- 회사명
- 공고명
- 하는일
- 자격요건
- 우대사항
- 지역
- 10년차 연봉
- 마감일
- 링크

Notes:

- `salary_10y` is a separate research field, not assumed to be present in the job posting.
- `salary_basis` should record the salary research basis, but the mobile card keeps the visible salary line short.
- Do not store Theo's private profile file in the repository.

## `raw_snapshots`

Fields:

- `source_id`
- `raw_path`
- `fetched_at`
- `item_count`

## FTS

When SQLite supports FTS5, `items_fts` is created.

Search currently combines:

- token overlap,
- Korean character n-grams,
- importance boost,
- active-status boost,
- deadline boost.

This is intentionally dependency-free. Later it can be supplemented with embeddings.

## Output Contracts

### `context`

Context output should be concise and structured for Codex. It should not dump full raw HTML.

### `brief`

Brief output should be mobile-shareable.

Card fields:

- status
- D-day
- title
- address
- area
- supply
- price
- eligibility
- agency/category/region
- schedule
- optional profile-review note when `--profile` or `SIGNAL_DESK_PROFILE_PATH` is used

If a field is not available in official HTML, use `원문 확인` or `원문/PDF 확인`.

Profile filter notes:

- profile-derived fields are attached only in memory as `_profile_status`, `_profile_label`, and `_profile_reason`,
- they are not stored in SQLite,
- excluded cards are hidden by default and can be inspected with `--show-profile-excluded`.

### `desk`

Desk output is a generated HTML view, not a separate canonical store.

Tabs:

- `summary`: high-priority items across implemented domains.
- `housing`: housing cards using the same decision fields as `brief`.
- `weekly-news`: broad weekly news cards with Korean title, expanded summary, category, date, and a hidden card-level article link.
- `jobs`: career job cards with company, role, work, qualification, preference, location, salary estimate, deadline, and link.

Selected-tab images are exported as `reports/desk-*.png`. The desk defaults to `645px`, while the concise housing `brief` remains `390px`.

### `ai-news`

AI Developer Brief output is generated from `news_items` rows whose `source_id` starts with `ai_`.

Outputs:

- `site/ai-news.html`
- `reports/ai-news-page1.png`
- `reports/ai-news-page2.png`
- `reports/ai-news-page3.png`

The HTML contains exactly 3 page sections. Cards use native `<details>` so the collapsed state shows title/summary first, while the expanded state reveals developer impact, detail, suggested action, and source link.
