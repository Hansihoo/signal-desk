# Handoff

This document is the first stop for a future Codex agent.

## Latest work: key technical research and hackathon learning, 2026-10-07

Five new authored reports / twenty learning chapters are in the immutable
`development-updates-2026-10-07` batch. Sixteen current reports / twenty-six
revisions / forty-six chapters now render from SQLite. Earlier eleven documents
match the previous export. The representative report is `hackathon-tech-roadmap`.
Its eight chapters explain prerequisites, function calling/structured output,
RAG, evaluation, multimodal choices, MCP/A2A, seven-day practice and a verifiable
demo. Other additions cover document RAG, voice architecture, agent evaluation
and the October 1 official A2A CLI announcement.

The topic tree now preserves arbitrary-depth paths. Parent filters include all
descendants; a single deep leaf opens its report directly. Runtime hackathon
parent filtering showed both the old AWS notice and new learning report. Keep
the selected Editorial CSS and compact typography; this work adds content and
hierarchical navigation rather than a new design.

Official evidence is checked on October 7. Google event reception ended August 31
(October 8 is winner announcement), Elastic's July event ended, and IBM Bob is
US-residents-only. These are learning examples, not a domestic active-event list.
The study sequence is editorial advice; no industry popularity ranking was
measured. OpenAI Evals read-only/shutdown dates were checked in the current
official deprecations page and the Promptfoo migration guide.

Local checks: 72 tests, compileall, publish, brief/desk/review, image inspection,
1531 internal references; new reports and all twenty expanded chapters at actual
320/390px pass without horizontal overflow. Enter/Space disclosures, parent
filter and direct child navigation pass; no report-console errors. The public
source refresh exported 468 records; GDELT 429 fell back to Google News RSS.
Deployment verification will be recorded after the run completes.

Retain `C:/Users/Theo/AppData/Local/Temp/signal-desk-01a0ff9d/research-expansion.2026-10-07/`
and its standalone/production previews, checks and captures. Raw evidence root
is ignored and registered separately. The existing loopback server PID 25120
on 45427 remains in use. A failed pre-fix restore test left
`F:/CodexTemp/tmp4371ant8` after a SQLite lock; it is registered, preserved and
excluded from deliverables. Later tests passed. Do not delete thread artifacts
without the user's cleanup request. Weekly deep-review automation is still pending.

## Project Summary

Signal Desk is a local-first update collection and briefing system.

The long-term goal is to collect multiple categories of important updates for Theo: housing, jobs, AI/IT, stocks, and policy. The current implementation has the first housing MVP, a weekly big-news MVP, an AI developer-news MVP, and a jobs briefing/import MVP.

## Current State

Implemented:

- official-source housing collector,
- raw HTML snapshot storage,
- SQLite normalized storage,
- validated authored research and changed-only revisions in SQLite,
- expandable learning chapters in ten development reports; MCP Apps includes seven chapters with terms, process, official example and evidence,
- `research-data` JSON-only collection/import/export independent of rendering,
- detail-page enrichment,
- optional local-profile housing filtering,
- local search/context output,
- Markdown report generation,
- mobile HTML rendering,
- PNG image export,
- tabbed mobile desk rendering,
- weekly big-news collection with GDELT-first and Korean Google News RSS fallback,
- AI developer news collection with OpenAI, Hugging Face, GitHub release feeds, and Google News AI search fallback,
- `issues` command for Theo's `이슈 뽑아줘` request, scoped to the latest 7 days by default,
- 3-page expandable AI Developer Brief rendering,
- career job JSON import, normalized `job_items`, and jobs tab rendering,
- Saramin Open API live job fetch when `SIGNAL_DESK_SARAMIN_KEY` is configured,
- automated review command,
- searchable public dashboard and dated briefing archive at https://hansihoo.github.io/signal-desk/,
- multi-topic research homepage, independent topic pages, and configurable public RSS/Atom research feeds,
- report/tree HTML scaffold: main -> topic -> category -> source-note document; review/conclusion sections pending,
- Developer Opportunities HTML outline, eight categories, planned metrics/source links, and a standalone HTML report template (no opportunity collection yet),
- daily GitHub Actions collection and Pages deployment with durable release snapshots,
- tests for parsers, detail extraction, rendering, and review checks.

Current source scope:

- Seoul Housing Portal LH public lease list for Seoul.
- Seoul Housing Portal LH public lease list for Gyeonggi.
- Seoul Housing Portal SH public lease list for Seoul.

Current generated output:

- `site/index.html`, `site/library.json`, `site/status.json`
- `data/research.json` (data-only), `site/research-data.json` (public export)
- `site/topics.json` and `site/research/<topic-id>/index.html`
- `site/public_site.css` and `site/public_site.js` (shared report/tree assets)
- `site/archive/YYYY-MM-DD/briefing.json` and `index.html`
- `site/brief.html`
- `reports/brief.png`
- `site/desk.html`
- `reports/desk-summary.png`
- `reports/desk-weekly-news.png`
- `reports/desk-jobs.png`
- `site/ai-news.html`
- `reports/ai-news-page1.png`
- `reports/ai-news-page2.png`
- `reports/ai-news-page3.png`

These are ignored by git and should be regenerated locally.

## Most Important Commands

```powershell
python -m housing_watch collect
python -m housing_watch publish --collect
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch news --source auto --limit 12 --width 645 --height 1500
python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500
python -m housing_watch ai-news --limit 18 --per-page 6 --width 645 --height 1500
python -m housing_watch jobs --input config/jobs.example.json --no-image
python -m housing_watch desk --tab summary --width 645 --height 1500
python -m housing_watch desk --tab jobs --width 645 --height 1500
python -m housing_watch review --width 390
python -m unittest discover -s tests
```

When `SIGNAL_DESK_SARAMIN_KEY` is configured:

```powershell
python -m housing_watch jobs --fetch saramin --no-image
```

## Current Product Decisions

The first implementation for template review is limited to two pages:
[homepage preview](https://hansihoo.github.io/signal-desk/preview/index.html) and
[representative report](https://hansihoo.github.io/signal-desk/preview/report.html).
Read [the template contract](BRIEFING_TEMPLATE.md) before expanding to other topics.
The title/topic -> summary -> visual data -> results -> references order is user-requested.
It uses a reviewed GitHub storage report and clearly labelled assumptions; other domains
still link to existing source-note views rather than pretending their analysis is done.

Latest direction, accepted on 2026-10-03: broaden developer research to **development
information**, with income opportunities as a subtopic. Theo requested research and
planning before implementing an executive-style homepage -> concise report -> official
evidence experience. Read [the delivery research and plan](RESEARCH_EXPERIENCE_PLAN.md)
before further UI or collection work. Weekly development review with changed-only
publishing is intended from the week of 2026-10-05, but not implemented. The current
public outline label, source-note pages, and daily workflow remain as described below.

- The public product is a main research library containing extensible topics. Existing AI/housing/news are initial examples.
- Add topic metadata and RSS/Atom feeds in `config/research_topics.json`; see `RESEARCH_HUB.md` for the contract and hosting limits.
- No public accounts, user-input forms, or analytics SDKs are required. The hosting provider still records security access logs.

- SQLite is the source of truth.
- Markdown/HTML/PNG are generated outputs.
- If price is not available from official HTML, show `원문/PDF 확인`.
- Do not infer eligibility or price from incomplete text.
- Optional housing profile filtering is conservative: hide only clear mismatches and keep ambiguous cases visible.
- Theo's private profile file is an input path or environment variable, not repository data.
- Housing cards must be useful without opening every link.
- The concise mobile image width is capped at `390px`.
- The tabbed desk is wider by default at `645px`; the concise `brief` remains `390px`.
- Housing desk cards use a longer snapshot layout for location, area, supply, price, schedule, conditions, and profile notes.
- Current housing scope is Seoul and Gyeonggi only.
- The tabbed desk separates `summary`, `housing`, and `weekly-news`; only the selected tab is visible in exported images.
- The weekly big-news collector stores Korean briefing fields in `news_items`.
- AI developer news also uses `news_items`, but source ids are scoped with the `ai_` prefix and rendered separately through `site/ai-news.html`.
- When Theo says `이슈 뽑아줘`, run `python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500`, then summarize the grouped terminal output.
- AI Developer Brief cards are collapsed by default; title/summary are visible first, while impact/detail/action/source link appear after expanding.
- AI Developer Brief is always organized into three pages: model/platform, development/open-source, and research/flow.
- GDELT gives better original article URLs but can return HTTP 429. `--source auto` falls back to Korean Google News RSS.
- Real non-Korean machine translation requires an optional LibreTranslate-compatible endpoint through `--translate-url`.
- Career jobs use `job_items`; visible cards must stay limited to company, posting title, work, requirements, preferred qualifications, location, 10-year salary estimate, deadline, and link.
- `salary_10y` is separately researched and should keep its basis in `salary_basis`; do not infer salary without a basis.
- Saramin live collection requires `SIGNAL_DESK_SARAMIN_KEY`; the source defaults are in `config/job_sources.json`.

## Known Limitations

- SH notices often keep address, floor plan, detailed price, and unit breakdown in attached PDF/HWP files.
- LH pages expose useful address/area/supply data in HTML, but exact deposit/monthly rent often still requires the attached notice.
- The search scorer is semantic-lite, not embedding-based.
- Daily collection is active on GitHub Actions at approximately 08:17 Asia/Seoul; no separate local Codex automation is required.
- Public feed collection and dated briefings are implemented; independent deep research and cross-topic analysis remain future work.
- See `PUBLISHING.md` for state recovery, public-data boundaries, manual refresh, and pausing the workflow. Two cloud runs verified restore, accumulation, and deployment on 2026-10-03.
- The Python package is still named `housing_watch` because the first MVP domain is housing.
- Saramin list API does not expose full detailed responsibilities/requirements/preferred qualifications, so the adapter summarizes list fields and links to the original posting.
- WorkNet and official company career-page adapters are not implemented yet.
- Profile filtering uses static 2026 기준 values in `housing_watch/housing_profile.py`; update these when official annual limits change.
- AI source feeds are pragmatic RSS/Atom inputs. If OpenAI, Hugging Face, GitHub, or Google News changes feed shape, update `housing_watch/ai_news.py` and `tests/test_ai_news.py`.

## Next Best Work

For data/design separation, read `RESEARCH_DATA.md`. Import reviewed JSON into SQLite
before publishing. Generated JSON edits alone will be overwritten. Initial seeding
never replaces existing database edits. Weekly development review is still pending.

1. Add PDF extraction for official notice attachments.
2. Add a source adapter for MyHome or 청년안심주택.
3. Add WorkNet and official company career-page adapters for `job_items`.
4. Add a source type for n8n/changedetection webhook imports.
5. Monitor the GitHub collection workflow; add separate Codex deep-research automation only when a distinct analysis task is requested.
6. Integrate `news_items` into search/context if Theo wants to ask Codex detailed questions across all domains.
7. Add optional Korean translation/summarization for non-Korean AI titles when a local or configured model is available.
8. Generalize package naming now that housing is no longer the only domain.
9. Move profile eligibility thresholds into a versioned config or collected official reference table.
# Reviewed development research (2026-10-04)

Read `docs/RESEARCH_DATA.md` before changing the public briefing reports. Ten reviewed
inputs in `config/development_baseline.2026-10-04.json` and the publication manifest
are applied once to SQLite locally and in cloud publishing. Do not overwrite the
cloud DB with local state or edit an applied batch in place; append a new dated
reviewed batch. The main is `/preview/index.html`, reports use stable ID filenames,
and `report.html` aliases the featured report. The existing source library and
daily archives remain available. Weekly deep review is not implemented yet.

## Mobile template selection (2026-10-06)

Read [MOBILE_TEMPLATE_SELECTION.md](MOBILE_TEMPLATE_SELECTION.md) before continuing
the mobile-selection workstream. The authenticated bridge was verified on loopback
port 45428 and saves only template preferences in the thread scratch; recheck its
process before resuming. The prior process is no longer running on 2026-10-07.
Local button/save/restore/reset/conflict/reconnect checks and166 shared-tool tests
pass. The Cloudflare tunnel launch was rejected by automatic approval review with
`blocked by policy`; no public URL exists and no alternate launch was attempted.
Phone/Remote device verification remains pending. Test preferences were cleared.
Do not treat its cleared test preference as the later user's explicit PC selection.

## Selected Editorial implementation (2026-10-07)

Latest refinement: reader wording (`분야`, `전체 보고서`, `최근 동향`) replaces
generic research labels in the curated shell. Navigation has compact non-duplicated
padding and 14px links. Shared 15px body, column-based title sizing, Korean word
grouping and balanced headings avoid unnecessary splits. Tables use natural
column widths and keyboard-accessible contained scrolling. Refer to the updated
template contract before changing these rules. Local verification: 71 tests,
brief/desk/review/images, all 11 reports/26 chapters at 320 and 390px, main/MCP
also at 768/1280/1440px. Authored data and stored revisions are unchanged. New
review outputs live under the registered retained temp root
`editorial-readability.2026-10-07/`, with `review.html` and self-contained
`offline/preview/` alongside the production-format pages. CSS version
`de2fc07102be`; final deployment 37634625748 succeeded in 1m29s from source
commit `aa571c0`. Public main/report use this exact CSS and updated reader labels;
11 current and 21 stored authored documents match the preserved inputs. Public
desktop captures were checked at actual 1440px. The final public 390px request
remained at 1440px in the browser tool, so it is not counted as a narrow-screen
check. Actual 320/390px checks above are from the equivalent local generated
pages, with their measurements retained in `browser-checks.json`. The selectable
review has its own wrapper MutationObserver error while its source hash/selection
state loads; public report console has no errors. Treat its static selection
preview separately from runtime verification.

The user explicitly chose `html5up-editorial` in the PC gallery and said to fit the
design to **each research item** with accumulating board posts. This supersedes
the earlier main-plus-one-report scope and the mobile test's empty selection.
The scratch selection record was updated to revision 6 after scope/source-hash
validation. The 2026-10-05 baseline is preserved, with an additional pre-Editorial
copy. No further selection/confirmation is required to use this chosen template.

Actual original template CSS, Google font subsets and licenses live in
`housing_watch/assets/editorial/`. `editorial_shell/home/report.html`,
`editorial.css`, `editorial.js`, and `editorial.py` own presentation. Shared content
helpers stay in `briefing_preview.py`; the superseded preview templates/CSS were
removed to avoid editing unused files. Reports remain SQLite-authored content.

Main: all 11 stored reports, top/subtopic filters, full authored-text search,
eight posts per page, field/latest highlights and source-library links. New IDs
appear automatically at publication even if absent from the curated lead manifest.
Changed IDs retain their URL and all older SQLite editions render under
`/preview/history/<id>-r<N>.html`; existing 10 older editions are linked. The JSON
envelope adds presentation-free `report_history` without a schema migration.

Tests 70, compileall, JS syntax, publish/brief/desk/review and briefing image checks
pass. Actual 390px main/all 11 reports and all 26 expanded chapters have no horizontal
overflow. Search/empty/reset/subtopic filters/pagination, keyboard Enter/Space and
previous/current edition links pass; 1,067 internal links/stylesheets resolve. The selected
template capture was compared with the result. See `BRIEFING_TEMPLATE.md` for the
source reuse and adaptation details. Weekly deep review remains a separate task.

Current review environment: loopback port 45427, PID 25120, serving the preserved
thread scratch; validate liveness before using. New rendered outputs are under
`editorial-preview.2026-10-07/`; the MCP selectable review is
`editorial-mcp-review.2026-10-07.html`. Both are retained until cleanup is requested.

Deployment [37628018293](https://github.com/Hansihoo/signal-desk/actions/runs/37628018293)
succeeded in 1m28s for source commit `bf11f7d`. Live export has 776 source records,
11 current reports and 21 stored editions. Current and prior authored documents
match the local reviewed inputs; saved timestamps legitimately differ between
local/cloud imports. Published CSS normalized text matches Git and renderer hash
`171be08edf65` (Windows output bytes have CRLF). All 25 live pages use that version.
Public main→MCP, all seven chapters at 390px, official quickstart/back and console
pass. Public main/report tabs and the offline selectable review are retained.
