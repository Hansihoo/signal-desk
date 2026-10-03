# Signal Desk

Signal Desk is a local-first personal signal dashboard.

It collects updates Theo cares about, stores them in a searchable local database, and turns them into concise mobile briefings that Codex can explain later.

First MVP domain: **housing subscription and public rental notices** for Seoul and Gyeonggi.

Additional MVP domains now exist for weekly big news, AI developer news, and normalized career job briefings.

Public site: [Signal Desk](https://hansihoo.github.io/signal-desk/).
GitHub Actions refreshes public sources daily at approximately 08:17 Asia/Seoul;
accumulated data and dated briefings are retained between runs. See [publishing operations](docs/PUBLISHING.md).

The public homepage is a multi-topic research library. Each topic has its own page;
add research areas and public RSS/Atom feeds in `config/research_topics.json`.
See [research hub and free hosting scope](docs/RESEARCH_HUB.md).

The **Developer Opportunities** topic currently provides an HTML outline with eight
categories and a downloadable report template. Real opportunity collection and verification
are deferred. See [scope and requirements](docs/OPPORTUNITIES.md).

The latest product direction broadens this to **development information**, with
opportunities as a subtopic. A curated homepage -> one-page report -> official evidence
experience and weekly changed-only development review are planned; the current HTML
outline and daily workflow have not been changed. See [research delivery analysis and
plan](docs/RESEARCH_EXPERIENCE_PLAN.md).

The first paired [homepage preview](https://hansihoo.github.io/signal-desk/preview/index.html)
and [representative report](https://hansihoo.github.io/signal-desk/preview/report.html)
are available for template review. Only this pair receives the new layout; see the
[template contract](docs/BRIEFING_TEMPLATE.md).

Future domains:

- jobs and hiring notices
- stocks and disclosures
- youth housing and public policy updates

## Current Capabilities

- Publish a searchable public-source dashboard and dated briefing archive with `publish`.
- Refresh on GitHub Actions and deploy through GitHub Pages; durable state lives in release snapshots.

- Collect Seoul/Gyeonggi housing notices from official public housing pages.
- Keep raw HTML snapshots for audit and parser recovery.
- Normalize notices into SQLite.
- Enrich cards from detail pages when official HTML exposes address, area, supply, eligibility, and schedule.
- Filter housing cards with an optional local profile so clearly impossible notices can be hidden before briefing.
- Search locally from Codex-friendly commands.
- Generate Markdown reports.
- Generate mobile HTML briefings.
- Export mobile PNG briefing images with a fixed width.
- Collect weekly big-news candidates, keep Korean briefing fields, and keep the article link on each card without showing source clutter.
- Collect AI developer news from famous LLM, AI platform, and open-source release sources.
- Generate a 3-page AI Developer Brief where cards show title/summary first and expand for impact, detail, action, and source link.
- Treat "이슈 뽑아줘" as a weekly AI issue pull using the `issues` command.
- Generate a tabbed mobile desk that separates important summaries, housing notices, and weekly big news.
- Import career job candidates into a normalized jobs table and render a concise mobile jobs tab.
- Fetch senior career job candidates from the Saramin Open API when `SIGNAL_DESK_SARAMIN_KEY` is configured.
- Run a self-review command before treating output as ready.

## Quick Start

```powershell
python -m housing_watch collect
python -m housing_watch search "서울 행복주택 청년" --limit 3
python -m housing_watch context "이번 주 서울 행복주택에서 볼 만한 공고" --limit 3
python -m housing_watch report
python -m housing_watch render
python -m housing_watch export-image --width 430 --height 1200
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch news --source auto --limit 12 --width 645 --height 1500
python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500
python -m housing_watch ai-news --limit 18 --per-page 6 --width 645 --height 1500
python -m housing_watch jobs --input config/jobs.example.json --no-image
python -m housing_watch desk --tab summary --width 645 --height 1500
python -m housing_watch desk --tab summary --profile "D:\path\to\profile.md" --width 645 --height 1500
python -m housing_watch review --width 390
python -m unittest discover -s tests
```

When a Saramin API key is configured:

```powershell
$env:SIGNAL_DESK_SARAMIN_KEY="..."
python -m housing_watch jobs --fetch saramin --no-image
```

Generated local outputs:

- DB: `data/housing_watch.sqlite`
- raw snapshots: `data/raw/`
- Markdown report: `reports/latest.md`
- full mobile HTML: `site/latest.html`
- full mobile image: `reports/latest.png`
- concise mobile HTML: `site/brief.html`
- concise mobile image: `reports/brief.png`
- tabbed desk HTML: `site/desk.html`
- selected-tab desk images: `reports/desk-summary.png`, `reports/desk-housing.png`, `reports/desk-weekly-news.png`, `reports/desk-jobs.png`
- weekly news raw snapshots: `data/raw/news/`
- AI developer briefing HTML: `site/ai-news.html`
- AI developer briefing images: `reports/ai-news-page1.png`, `reports/ai-news-page2.png`, `reports/ai-news-page3.png`
- AI developer news raw snapshots: `data/raw/ai_news/`
- imported jobs raw snapshots: `data/raw/jobs/`

Generated files are ignored by git. Recreate them with the commands above.

Natural request shortcut:

- When Theo says `이슈 뽑아줘`, run `python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500`.
- Report the grouped terminal summary and point to `site/ai-news.html` plus the generated page image.

## Repository Map

```text
AGENTS.md                Codex working rules for this repo
PROJECT_STATUS.md        Current feature progress ledger
config/sources.json      Enabled sources and interest scope
config/job_sources.json  Job source adapter defaults
config/jobs.example.json Example normalized jobs input
config/job_salary_estimates.example.json Example separate salary estimate mapping
housing_watch/           Current MVP Python package
tests/                   Parser, detail extraction, render, and review tests
docs/                    Architecture, handoff, roadmap, operations, data model
data/raw/.gitkeep        Placeholder for local raw snapshots
reports/.gitkeep         Placeholder for local reports/images
site/.gitkeep            Placeholder for local HTML output
```

## Documentation Index

- [Publishing and continuous collection](docs/PUBLISHING.md): GitHub Pages, daily refresh, archive, privacy, and recovery.

- [Handoff](docs/HANDOFF.md): where to start when another Codex resumes work.
- [Features](docs/FEATURES.md): what exists now and how each feature behaves.
- [Roadmap](docs/ROADMAP.md): planned expansion beyond housing notices.
- [Architecture](docs/ARCHITECTURE.md): pipeline shape and module responsibilities.
- [Data Model](docs/DATA_MODEL.md): SQLite fields and output contracts.
- [Operations](docs/OPERATIONS.md): commands, verification, and automation loop.
- [Sources](docs/SOURCES.md): current official sources and candidate sources.
- [MVP Goals](docs/MVP_GOALS.md): completion criteria for the housing MVP.
- [Tabbed Briefing](docs/TABBED_BRIEFING.md): mobile tabs and selected-tab image export.
- [Weekly News Tool Research](docs/NEWS_TOOLS_RESEARCH.md): researched tools for the future big-news tab.
- [Jobs Briefing](docs/JOBS_BRIEFING.md): job card field contract, import shape, and source strategy.

## Important Product Rule

Markdown and HTML are outputs. SQLite is the source of truth.

```text
sources
-> raw snapshots
-> normalized SQLite
-> search/context
-> report/HTML/image
-> Codex explanation
```

## Current Housing MVP Notes

Signal Desk currently focuses on Seoul and Gyeonggi housing notices.

The concise card should help Theo decide whether to open the official notice without asking follow-up questions. Each card attempts to show:

- status and D-day
- title
- address
- area in square meters and pyeong
- supply count
- price or `원문/PDF 확인`
- eligibility/conditions
- agency, category, region, and schedule
- a wider desk-only visual snapshot for location, area, supply, and price

Some official pages expose price only inside PDF/HWP files. In that case, Signal Desk does not guess; it marks the field as `원문/PDF 확인`.

Optional profile filtering:

- pass a local Markdown profile with `--profile`, or set `SIGNAL_DESK_PROFILE_PATH`,
- the repo does not store the profile file,
- the filter only hides clear mismatches, such as youth-housing income/asset limits, age-only targets, and household-type-only notices,
- ambiguous cases stay visible with a `프로필` note so Theo can ask Codex for follow-up.

## Current Jobs MVP Notes

The jobs tab is ready for normalized career postings.

It can also fetch live Saramin Open API candidates when `SIGNAL_DESK_SARAMIN_KEY` is set.

Each visible card shows:

- company name
- posting title
- work summary
- requirements
- preferred qualifications
- location
- 10-year salary estimate
- deadline
- link target

Salary is stored separately from the job posting as `salary_10y`; keep the research basis in `salary_basis`.

Saramin list results do not include full detailed duties/qualifications/preferred text, so the live adapter summarizes title, job code, keywords, experience, and education, then keeps the original posting link on the card.

## Requirements

- Python 3.8+
- Windows Edge or Chrome for image export
- No Python package dependencies for the current MVP
