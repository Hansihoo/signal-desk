# Signal Desk

사업기획 영역은 공개 공식 자료와 사내 작업 자료를 분리한다.
공개 목록은 `preview/business.html`, 사내 화면은 저장소 밖
`D:/3_codex_docs/SignalDesk/BusinessPlanning/index.html`이다.
조사 항목·주간 검토·입력 명령은 [사업기획 운영](docs/BUSINESS_PLANNING.md)을 참고한다.

Signal Desk is a local-first personal signal dashboard.

It collects updates Theo cares about, stores them in a searchable local database, and turns them into concise mobile briefings that Codex can explain later.

First MVP domain: **housing subscription and public rental notices** for Seoul and Gyeonggi.

Additional MVP domains now exist for weekly big news, AI developer news, and normalized career job briefings.

Public site: [Signal Desk](https://hansihoo.github.io/signal-desk/).

AI research serves developers and managers learning to use AI and assessing changes
to products, organizations and the labor market. Agents follow [research operations](docs/AI_RESEARCH_OPERATIONS.md),
[the source catalog](docs/AI_RESEARCH_SOURCES.md) and [the review log](docs/ai/AI_RESEARCH_REVIEW_LOG.md).
These define proactive topic discovery, coverage gaps, source limits and separate
collection/review/publication dates. Broad source connections, common freshness
metadata and broad recurring execution remain implementation work; see [project status](PROJECT_STATUS.md).

The [curated main](https://hansihoo.github.io/signal-desk/preview/index.html)
now uses the 2026-10-09 reinforced editions of all20 authored reports and14 separate
model reading guides. Each explains a reader question, mechanisms or conditions,
a complete case and an application exercise. Independent agents read the changed
drafts, found substantive defects and rechecked the repairs. Imported model originals
stay preserved; each guide is pinned to the original document, assets and metadata.
[Repair, individual verdicts and verification limits](docs/RESEARCH_AUTHORING_REPAIR.2026-10-09.md).
GitHub Actions refreshes public sources daily at approximately 05:00 Asia/Seoul;
accumulated data and dated briefings are retained between runs. See [publishing operations](docs/PUBLISHING.md).

The public homepage is a multi-topic research library. Each topic has its own page;
add research areas and public RSS/Atom feeds in `config/research_topics.json`.
See [research hub and free hosting scope](docs/RESEARCH_HUB.md).

The **Developer Opportunities** topic currently provides an HTML outline with eight
categories and a downloadable report template. Real opportunity collection and verification
are deferred. See [scope and requirements](docs/OPPORTUNITIES.md).

The latest product direction broadens this to **development information**, with
opportunities as a subtopic. The curated homepage -> report -> official evidence
experience is implemented. Weekly changed-only development review remains planned;
the existing daily source refresh continues. See [research delivery analysis and
plan](docs/RESEARCH_EXPERIENCE_PLAN.md).

The [research homepage](https://hansihoo.github.io/signal-desk/preview/index.html)
and authored reports use the user-selected **HTML5 UP Editorial** design.
The main shows recent findings and an accumulating, searchable topic board. New
reviewed reports appear on publication; earlier documents remain addressable in
the [report history](https://hansihoo.github.io/signal-desk/preview/history/index.html).
See the [template contract](docs/BRIEFING_TEMPLATE.md).

Research content is independent of web design. `research-data --collect` refreshes
public sources and writes `data/research.json` without rendering webpages. Authored
reports are imported into SQLite with changed-only revisions; the representative
pair renders this structured content. See [data contract and workflow](docs/RESEARCH_DATA.md).

Development reports explain definitions, processes, examples and evidence in the
primary reading path, with optional deeper exercises in disclosures. The
[MCP Apps report](https://hansihoo.github.io/signal-desk/preview/mcp-apps-workflows.html)
connects the same comparison task across input, tool result and screen interaction.
This detail is stored as report data independently of HTML/CSS; conceptual examples
and editorial recommendations are distinguished from tested integrations.

The [hackathon learning report](https://hansihoo.github.io/signal-desk/preview/hackathon-tech-roadmap.html)
is nested under hackathons and includes a practice plan, a consistent date-filtering
example and official event evidence. Further technical reports cover document RAG,
voice architectures, agent evaluation and A2A connections. Parent topic filters
include all descendants. Closed events and residency restrictions are distinguished
from learning examples; dated conditions must be rechecked before participation.

Report comprehension was reviewed on 2026-10-08. The
[content audit](docs/RESEARCH_CONTENT_REVIEW.2026-10-08.md) records concrete defects
and each report's intended reader outcome. Future authors follow the
[writing guide](docs/RESEARCH_WRITING_GUIDE.md) and
[worked explanations](docs/RESEARCH_WRITING_EXAMPLES.md): write to resolve the
reader's question before extracting summaries and tables. The audit records the
earlier defects; [the subsequent repair](docs/RESEARCH_REPAIR.2026-10-08.md) records
the 20 revised editions and verification. Comprehension self-review is complete;
actual reader testing has not been performed.

The 2026-10-09 feedback still finds the prose difficult to learn from. Authors now
apply the project [research-teaching skill](skills/research-teaching/SKILL.md),
including prerequisite concepts, missing-evidence research and separate title/summary
and full-explanation reviews. [Skill comparison and application](docs/RESEARCH_TEACHING_SKILL.2026-10-09.md).

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
- cumulative model comparison: `site/preview/ai-models.html` and `site/research/ai/models/index.html`
- model ledger JSON: `data/ai-models.json` (`python -m housing_watch ai-models --collect`)
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

- [AI model research](docs/AI_MODEL_RESEARCH.md): complete accumulating model comparison, changed-only refresh, official additions, new-model discovery and review rules.

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
# Development research reports

Reviewed development information is published at
[Signal Desk](https://hansihoo.github.io/signal-desk/preview/index.html).
The first collection (2026-10-04) contains ten reports across development changes,
support/participation, and market/business information. Each links summary, sourced
data, conclusions, and official references. Data remains independent of HTML/CSS;
see [the content contract](docs/RESEARCH_DATA.md) for reviewed input batches and
stable report URLs. Existing daily source collection is separate from the planned
weekly deep review.

Model documents are accumulated in full, with source table controls and immutable editions. `model-pages --collect` discovers additional Theo model documents; daily05:00 source collection adds their pages. A current-chat daily05:00 agent checks official new models and writes/publishes new detailed research pages. See [AI model operations](docs/AI_MODEL_RESEARCH.md).
