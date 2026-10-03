# Roadmap

## Product Direction

Signal Desk should become Theo's personal update desk:

```text
fixed sources + broad research
-> local searchable database
-> Codex answers
-> mobile briefings
```

## Phase 1: Housing MVP

Status: Done.

- Seoul/Gyeonggi housing notices.
- SQLite local store.
- Search/context.
- Mobile card briefing.
- PNG export.
- Review loop.

## Phase 2: Multi-Topic Desk and Weekly Big News

Goal: prepare a single mobile briefing surface where each domain is separated by tabs.

Status:

- Tabbed desk shell: Done.
- Important summary tab: Done for housing plus weekly news.
- Weekly big-news collector: Done as MVP.

Candidate work:

- improve GDELT stability and backoff behavior,
- compare Media Cloud for research-grade analysis,
- use Miniflux/FreshRSS/Newscope-style RSS tooling for fixed feeds,
- integrate news items into search/context,
- add a self-hosted LibreTranslate endpoint for non-Korean titles,
- score by source frequency, frontpage/rank, recency, and category diversity.

## Phase 3: Better Housing Detail Quality

Goal: reduce "원문/PDF 확인" fields.

Candidate work:

- extract official PDF/HWP attachment URLs,
- parse PDFs for price tables and unit details,
- add per-complex cards when one notice contains many complexes,
- include application method and document submission window,
- add "must act by" field separate from official closing date.

## Phase 4: Automation

Implementation now includes a public dashboard, dated archive, release-backed collection
state, and a daily GitHub Actions / Pages workflow. Deployment verification is tracked in
`PROJECT_STATUS.md`. See `PUBLISHING.md` for operations.

Goal: make weekly collection/reporting automatic.

Candidate work:

- create Codex weekly automation,
- optionally add n8n for fixed source polling,
- optionally add changedetection.io for pages without stable APIs,
- store automation run logs.

## Phase 5: Jobs

Status:

- Normalized `job_items` table: Done.
- JSON import for normalized career jobs: Done.
- Saramin Open API adapter: Done.
- Mobile jobs tab and selected-tab image export: Done.
- More live source adapters: In progress.

Candidate work:

- run Saramin live collection after `SIGNAL_DESK_SARAMIN_KEY` is approved,
- add WorkNet API adapter when key/approval is available,
- add source adapter for selected company career pages,
- add source adapter for JobKorea/Wanted/community sources only when access terms are acceptable,
- research 10-year salary estimates from separate salary sources and store the basis in `salary_basis`,
- integrate job items into search/context.

## Phase 6: IT and AI News

Candidate work:

- RSS adapters for official blogs,
- Hacker News/API source,
- GitHub releases/trending source,
- summarize updates into "why Theo should care".

## Phase 7: Stocks and Disclosures

Candidate work:

- OpenDART adapter,
- KRX/public data adapter,
- normalize fields: ticker, company, disclosure type, date, risk/opportunity note,
- keep strict source attribution.
