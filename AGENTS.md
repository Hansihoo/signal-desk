# Signal Desk Agent Instructions

## Project Goal

Signal Desk is Theo's local-first personal signal dashboard.

It collects important updates in advance, keeps them searchable for Codex, and renders concise mobile briefings. The first MVP domain is housing subscription/public rental notices for Seoul and Gyeonggi.

AI research also serves developers and managers who need to learn, adopt and operate
AI, and understand changes to products, organizations and the labor market. Discover
important missing topics proactively rather than waiting for the user to name them.

## Before Changing Code

Read these files first:

- `README.md`
- `docs/HANDOFF.md`
- `docs/ARCHITECTURE.md`
- `docs/MVP_GOALS.md`
- `PROJECT_STATUS.md`

Then state:

- goal
- work type
- impact scope
- risk
- verification plan

## Development Rules

- Keep the MVP incremental. Add one source or feature at a time.
- Prefer official sources first.
- Keep raw fetched data under `data/raw/`.
- Keep normalized data in SQLite. Markdown, HTML, and PNG are generated outputs.
- Do not commit generated DBs, raw snapshots, reports, PNGs, or HTML output.
- Do not hardcode API keys, cookies, sessions, or personal credentials.
- If a website structure changes, update parser logic and add or update tests.
- If UI or briefing changes, run `brief`, `review`, and inspect `reports/brief.png`.
- Update `PROJECT_STATUS.md` when feature status changes.
- Update `docs/ai/WORK_LOG.md` for meaningful implementation or verification work.
- Keep docs useful for a future Codex agent that cannot inspect your memory.

## AI Research Discovery and Freshness

Before planning, collecting, expanding or reviewing AI/development/market/workforce
research, read [AI research operations](docs/AI_RESEARCH_OPERATIONS.md),
[the source catalog](docs/AI_RESEARCH_SOURCES.md) and
[the review log](docs/ai/AI_RESEARCH_REVIEW_LOG.md).

- Cover models/tools, knowledge/data, execution/operations, enterprise adoption and roles, products/business, labor/skills, security/responsibility and industry applications. Ontology, knowledge bases and FDE are explicit subjects; the list is a coverage map, not a keyword-only filter.
- Define the developer's or manager's question. Check coverage gaps and discover new topics through official technical sources, implementation cases, hiring and market evidence. Record selection, deferral, counterevidence and missing conditions.
- Distinguish a documented source from a connected collector or a scheduled run. Check original pages and actual retrieval outcomes; a feed entry does not establish a full content review.
- Record acquisition dates. Preserve first collection, latest successful collection, actual content review, original publication/update and measurement/effective periods separately. Failed retrieval and HTML regeneration do not refresh evidence dates. Do not invent missing original dates or backfill first collection with today.
- Report new, changed, unchanged, collection failed and review not performed separately, including partial coverage. Unread originals/attachments and failed sources cannot be called unchanged.
- Initial knowledge mapping is not limited to seven days. Use daily discovery and weekly deep review as the broad operating direction while preserving existing daily model and weekly business scopes. This documentation does not create or change automations; broad connections/execution remain tracked in PROJECT_STATUS.md.
- The common provenance fields are implementation requirements, not additions to report schema v1. Until compatible storage/export/render contracts exist, keep exact original URLs, dates, actual check scope and gaps in the review log. Do not inject unsupported fields into validated JSON.
- Follow the writing guide below. Preserve editions and separate source/meaning review, comprehension self-review, output checks and actual reader testing.

## Research Writing and Content Review

New generated research uses [the executable quality workflow](docs/RESEARCH_PIPELINE.md).
Define questions and necessary evidence before collection; select or explicitly narrow the
research method. Preserve report-v1 and immutable editions. New release batches bind a quality
sidecar; use `research-check` and `research-audit`. Legacy format checks/agent Pass records do
not retroactively satisfy this workflow. Missing evidence returns to research, misinterpretation
to analysis and explanation defects to writing. Never enable paid generation/discovery merely
because an ordinary publish/collection job runs. Preserve failed acquisition and review dates.

For PolarisOffice government programs, sales opportunities or peer business direction,
read `docs/BUSINESS_PLANNING.md` first. Keep confidential customer, pricing, proposal
and internal engine/UI evidence outside this public Git repository and its DB/site/
release backups. Use `business-private` for the separate external working store.

For AI/LLM model lists, comparisons, new releases, availability, costs or benchmarks,
read `docs/AI_MODEL_RESEARCH.md` first. It owns the research scope, Theo's existing
source mapping, accumulating model ledger, collection commands and official-fact import procedure.
Keep source update/check dates and model/evaluation conditions; source collection
does not establish independent fact verification or actual workload performance.
Use `ai-models --collect` for the full comparison and `ai-models --input` for reviewed
official additions; preserve original observations and revisions. Do not implement
model maintenance only as report links or new-news cards.

When writing, expanding, or reviewing authored research reports:

- The user rejected the voice report's first screen after the previous independent Pass. Follow [the concrete voice repair](docs/VOICE_REPORT_REPAIR.2026-10-09.md) and the skill's first-screen regression case. Give title/deck/summary to a reviewer before providing the body; require a concrete reader task and one comparison axis. Do not equate implementation structures with vendor products, or promise measured speed/cost/difficulty from feature documentation alone. Previous agent Pass is not user approval.

- Read [substantive authoring research](docs/AI_WRITING_RESEARCH.2026-10-09.md) and the skill's [question/evidence review](skills/research-teaching/references/substantive-review.md) when the user rejects information value. Map each reader question to a supported answer and a body location; acquire missing mechanisms/cases instead of repeating generic verification advice. Use task-specific criteria for explanations, tutorials, market analysis and opportunities. In the user-authorized independent review workflow, give reviewers the changed edition, repair concrete findings and request a new verdict; distinguish agent review from human reader testing. Current complete repair state is [the 2026-10-09 ledger](docs/RESEARCH_AUTHORING_REPAIR.2026-10-09.md).
- Apply the project [research-teaching skill](skills/research-teaching/SKILL.md). The 2026-10-09 user feedback still rejects the prose as hard to learn from. Define prerequisite concepts and gather missing evidence; review title/summary alone before reviewing the whole explanation. Record where the draft fails and revise it. The dated [skill analysis](docs/RESEARCH_TEACHING_SKILL.2026-10-09.md) explains the adopted methods; passing format/output checks is not reader approval.
- Development-trend content serves practical AI use. Define the reader's concrete task and resulting artifact, then teach the necessary concepts through a complete worked example and application exercise. Distinguish using an existing tool from implementing a new one. Treat role descriptions as intermediate learning, not the final reader outcome. Follow the authoring and evidence-based review steps in `docs/RESEARCH_WRITING_GUIDE.md`. The earlier MCP Apps 3rd edition was rejected as a textbook standard; use `docs/RESEARCH_REPAIR.2026-10-08.md` for the latest20-report repair scope and verification limits, without claiming reader approval.
- Read `docs/RESEARCH_WRITING_GUIDE.md` first. Use `docs/RESEARCH_CONTENT_REVIEW.2026-10-08.md` for known defects and repair priorities, and `docs/RESEARCH_WRITING_EXAMPLES.md` for representative explanations. Recheck dated technical facts before reuse.
- Define the reader's question, assumed prior knowledge, and what they should be able to explain, decide, or do afterward. Keep this editorial brief in working documentation; do not add unsupported fields to the validated report schema.
- Write a coherent explanation and a consistent worked example before deriving the headline, summary, table, or learning blocks. Preserve the source's actors, conditions, units, and limits; do not turn an observation into a causal conclusion.
- Keep essential concepts and decision conditions in the primary reading path. Use disclosures for optional depth, not to hide the knowledge needed to understand the headline. A fixed layout or short-copy target must not remove necessary explanation.
- Check example inputs, tool parameters, returned fields, and expected outcomes together. Separate conceptual examples from tested tutorials.
- Record content meaning/source review, reader-comprehension review, and technical output checks separately. Passing tests, valid source IDs, chapter counts, and responsive layout do not establish comprehension. Do not claim actual reader testing unless it was performed.
- Preserve earlier report editions. Publish reviewed content changes using a new immutable batch and the existing report ID, with applicable rendering and link checks.

## Common Commands

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
python -m housing_watch desk --tab jobs --width 645 --height 1500
python -m housing_watch desk --tab summary --profile "D:\path\to\profile.md" --width 645 --height 1500
python -m housing_watch review --width 390
python -m unittest discover -s tests
```

## Theo Natural Requests

- When Theo says `이슈 뽑아줘`, treat it as: collect the latest 7 days of AI developer issues, render the 3-page AI Developer Brief, and report the grouped text summary.
- Default command:

```powershell
python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500
```

- If only refreshing from already collected rows, use `--no-collect`.
- Mention the generated `site/ai-news.html` and `reports/ai-news-page1.png` path in the final response.

## Completion Contract

A meaningful housing MVP change is not complete until:

- tests pass,
- data collection works,
- search/context output is usable,
- report/render output is generated,
- concise mobile briefing is generated,
- tabbed desk briefing is generated when a multi-topic or summary UI changed,
- `review` passes,
- image output is visually inspected when UI changed,
- docs/status are synchronized.

## Commit Messages

When creating commits for Theo, use Korean commit messages:

```text
[Tag] Korean summary

- Korean detail about what changed or was verified.
- Korean detail about support work or follow-up.
```
