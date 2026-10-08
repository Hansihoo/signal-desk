# Handoff

## Latest work: model navigation counts, 2026-10-08

The main and sidebar count document pages rather than model/settings rows. The
native comparison explorer is1 page; model guides count current `model_pages.pages`
documents (currently14), excluding earlier editions and route aliases. Parent
topic totals include these additional pages. Row counts inside the comparison
explorer retain their original meaning. Regenerate with `publish`; no DB migration
or authored report revision is needed. See [the count contract](AI_MODEL_RESEARCH.md).

## Business planning (2026-10-08)

Read [BUSINESS_PLANNING.md](BUSINESS_PLANNING.md) for public/private boundaries,
weekly official-source review, product evidence rules and commands. Public business
reports render at `preview/business.html` and `research/business/index.html`.
Confidential data stays outside Git in `D:/3_codex_docs/SignalDesk/BusinessPlanning`;
`business-private` uses its own SQLite and HTML, never the public DB/export pipeline.
Initial reports are a planning baseline, not validated eligibility or actual leads.

This document is the first stop for a future Codex agent.

## Latest work: header overlap and model-library mobile layout, 2026-10-08

Theo reported the menu/Signal Desk brand overlap. The live768px baseline confirms
icon overlap and wider button hit-area interception. The common Editorial shell
now places a44px menu control in the header, with a separate sidebar close control
and focus restoration; outside clicks do not immediately close a newly opened
menu. Small-screen auxiliary links wrap onto their own line. The model library's
narrow date/category columns also wrapped characters vertically; mobile rows now
group all metadata and wider screens keep readable table columns.

99 tests passed, followed by6 affected model-page tests. The browser regression
checks35 page/width combinations, actual brand hit tests, Enter/Space, close,
Escape/outside click, search/empty/reset and single-line metadata. Local390/768/
1440px images are retained under ignored reports/header-fixed-*.png. Read
[the responsive contract](BRIEFING_TEMPLATE.md); generated HTML/PNG stay ignored.
Public sourcec1fc546 deployed successfully in
[Actions37738799969](https://github.com/Hansihoo/signal-desk/actions/runs/37738799969).
Cloud99 tests and housing review passed. The same35 browser checks also passed
against the live site, including metadata/search states and actual logo clicks.
Live390/768/1440px screenshots remain in ignored reports/header-live/. All owned
browser/test scratch was cleaned. Local housing review still fails only its
0-active-notice check; the other11 checks pass.

## Latest work: full model documents and daily new-model publishing, 2026-10-08

Theo requested public-site application, copying other model pages, and replacing weekly comparison review with daily05:00 new-model checks and detailed page additions. Read [AI model operations](AI_MODEL_RESEARCH.md). `model-pages --collect` fetched all14 in-scope documents without failures, preserving original HTML/body/controls and same-site dependencies in SQLite. Immutable editions include shared asset changes; failed or absent documents retain prior content. `preview/ai-model-guides.html` searches model documents; `preview/model-guides/<slug>.html` shows isolated original interactive content and edition links. The original comprehensive table and its additional filters are available as a source document; native789 observations remain separate.

New officially reviewed model facts can deploy with immutable `config/ai_model_publication.json` batches. New official model reports use existing immutable report publication inputs, stable IDs and AI model topic paths. Do not commit generated databases/HTML/raw evidence. The user now authorizes related normal commit/push and Pages publication; verify Hansihoo identity/root/fetch+actual push before every write. Theo upstream remains read-only. Existing weekly heartbeat was deleted; the replacement ID ai is ACTIVE daily05:00 Asia/Seoul. Source-only GitHub Actions scheduling moved to the same Korean time, independent of the local agent's availability.

Local verification:99 tests;14 actual pages with no page errors or mobile root overflow;89 generated HTML pages /2048 local references /0 missing targets. New-page navigation, controls and public deployment verification are recorded after completion below. Source meaning is preserved as Theo-authored material; independent official rechecking of every old table or actual model execution was not performed.

Public deployment: commit55c71fc, [Actions37736392889](https://github.com/Hansihoo/signal-desk/actions/runs/37736392889) completed successfully (95s). Cloud99 tests and housing review passed. Public export contains1041 source records,17 authored reports/28 editions,789 model observations and14 complete model pages. All18 checked model routes returned200; every imported source document/assets matches the local validated input. The local0-active housing limitation does not describe cloud results. Normal push preserved the prior MCP public-verification commits; only the overlapping worklog row required reconciliation, retaining both records.

Live browser verification: at390px, public main → model library → GPT-6.1 document displays the full body; original source tool filtering returns89 rows, native local filtering166 records, and native Opus search17 observations. Root width/scroll width are both390; page errors0. Public screenshots remain in ignored reports/model-*-live-mobile.png paths. The source popup regression test, library category/empty states, added native facets and latest brief/desk images were also verified locally. All owned scratch was cleaned.

## Earlier work: accumulating complete model comparison, 2026-10-08

Theo clarified that the requested outcome is the actual comprehensive model
table maintained inside research, rather than only links and a comparison guide.
Read [AI model operations](AI_MODEL_RESEARCH.md). `ai-models --collect` reads the
original HTML, generated guide JSON and five independent JSON snapshots. It imports
789 observations: 274 specifications, 283 AA model configurations, 31 coding-agent
configurations, 63 Cursor configurations, 24 availability entries and 114 earlier
evaluations. The second real refresh inserted/updated zero and retained 789 identical
observations and 789 immutable first editions. AA model, Agent and Cursor values,
settings, fallback, units and check dates remain separate; absent rows are retained.

The native research subpage is `site/preview/ai-models.html`, also addressable as
`site/research/ai/models/index.html`. Main and AI model tree links open it. It supports
search, presets, provider/effort/harness/source filters, columns, sorting, CSV,
original evidence and per-observation history. Earlier evaluations are optional.
`ai-models --input` adds officially reviewed facts without overwriting upstream
observations. Optional `candidate_ids` closes the matching news review candidates.
The complete ledger is also part of `research-data` JSON. The existing daily
`publish --collect` and full SQLite cloud backups include it after source deployment.

All changes remain local and uncommitted. No upstream repository changes or
independent re-evaluation of every model were performed. Theo selected weekly agent
review at that stage: the earlier heartbeat `AI 모델 비교표 주간 검토` (ID `ai`) was active
Monday09:00 Asia/Seoul, checking official sources and adding changed-only reviewed
facts locally. It does not authorize commits, pushes or public deployment. The
automatic collector follows upstream data updates and gathers candidates. Housing's existing active-notice
review limitation remains separate from model data quality.

## Earlier work: model references and new-model discovery, 2026-10-08

Theo requested that his existing GitHub LLM materials and new-model information
belong to the AI model area. Read [AI model research operations](AI_MODEL_RESEARCH.md)
for the authoritative scope, upstream catalog mapping, commands and review rules.
The source is public `theo-s-han/research-analysis`; only Signal Desk was modified.
`collect_ai_news` now imports 13 model-related catalog references and a dedicated
model-update news search. Original dates/hashes and authored-versus-official source
types are preserved. Canonical slugs survive title changes and same-title records.

The new `llm-model-comparison` report is under development/AI models/API. Its new
immutable batch adds four visible explanation chapters, preserving all 16 earlier
documents; the local export has 17 current reports / 28 stored revisions. The MCP
featured report stays selected. This is reference integration and comparison
guidance, not a fresh verification of every model specification/price/benchmark.

Local checks: 83 tests, actual collection (117 AI / 194 total records), publishing,
report/render/search/context/brief/desk, 43 HTML pages / 1782 internal references,
320/390px report fit, main search/navigation, model-library search and three-page
AI briefing with no page errors. Images remain under ignored `reports/` and fetched
catalog evidence under `data/raw/ai_news/model_research/`; owned scratch was removed.
Housing review fails only its active-notice check (0 of 8). LH lists returned zero;
GDELT 429 used the existing fallback. The CLI Edge exporter wrote a PNG but stayed
running; its owned process was stopped and isolated Playwright/Edge completed QA.
Source changes are local, uncommitted and not deployed. Weekly deep review remains
planned at that point. That first catalog-only phase did not monitor shared benchmark assets;
the accumulating ledger above supersedes this limitation.

## Latest work: first reader-purpose main and MCP Apps, 2026-10-08

Theo requested actual application on the main so the result can be assessed.
The Editorial main now features MCP Apps through a notice-comparison scenario.
Topic panels and board rows show `deck` sentences. Only MCP's authored document
changed: stable ID, new immutable batch, revision3. Other fifteen documents and
old MCP editions compare equal to the pre-change snapshot.

Optional v1 `explanation` reuses validated chapter/blocks, renders visibly before
data/result and has separate anchors. Five primary MCP chapters explain roles,
the same A/B/C example, data versus HTML, and click versus conversation updates.
Three optional chapters cover the official time example, preparation and transfer.
See `docs/READER_PURPOSE_APPLICATION.2026-10-08.md` for the editorial brief,
source/meaning review and comprehension self-review. No actual reader study or
SDK execution is claimed. Other reports remain in the dated repair backlog.

Local checks:74 tests, compileall, JS syntax, publish/brief/desk/review and images,
40 generated HTML pages /1693 internal links; actual320/390px main/report fit.
Enter/Space disclosures, full-text search of optional prose and parent filter
(two hackathon posts) pass. Primary explanation is outside all disclosures.
Retain the registered `reader-purpose-main.2026-10-08` root (production/offline
outputs, receipts and screenshots) below the existing temp parent. Server25120
on127.0.0.1:45427 remains used.

Source1c3119a deployed in run37720532179 (success,1m39s). Public967 source records,
16 reports/27 revisions, all authored documents/revision numbers match local;
CSS66e51886df96 matches. Public main/report click-through,5 visible primary
chapters/3 disclosures, Enter and console checks pass. Public old MCP r2 matches.
Captures are actual1280px. Requested public390px stayed1280px; narrow checks use
matching output locally at actual320/390px. Override reset. Main/report retained
as deliverables; previous chooser/review tabs retained for continuing work.

## Previous work: research comprehension audit, 2026-10-08

Theo said summaries and structure were replacing actual understanding. All sixteen
current SQLite reports / forty-six learning chapters, their summaries/tables/results
and the renderer/validators were reviewed. The authoring baseline is now
`docs/RESEARCH_WRITING_GUIDE.md`, routed from AGENTS.md. The dated content audit
contains a reader outcome and repair for every report; `RESEARCH_WRITING_EXAMPLES.md`
contains coherent MCP Apps and function-calling explanations plus an A2A connection
example. Drafts have consistent inputs/outputs and transfer questions, but are not
executed SDK tutorials or evidence of actual reader testing.

Concrete issues: the MCP hero table reverses the HTML-reading actor; the hackathon
query example has no date parameter/result despite a date-filtered question; the
Tally headline implies causality beyond the stored evidence. Preserve useful
existing explanation and source limitations. Do not claim the 72 tests or 46 chapters
prove comprehension. Official teaching guidance and selected technical docs were
checked October8; all program eligibility/financial/model details were not refreshed.

This is a documentation/content-review change. Current authored report hashes,
revisions, publication configuration, HTML/CSS and SQLite remain unchanged. The
prose drafts were not imported/deployed as report revisions. The known content
corrections and full report rewrites remain the next content workstream; begin with
MCP Apps and hackathon/RAG/evaluation. Recheck primary sources, keep the report ID,
use a new immutable batch and verify the actual rendered reading path. No chooser
or new design is needed solely for content corrections.

Documentation verification:39 local links resolve; all16 audit IDs/revisions match
SQLite. Two conceptual JSON objects and three fixture rows agree with the SeoulA
and GyeonggiB expected outcomes. The sorted ID/revision/content-hash fingerprint
is unchanged (`e845174aa74161f2f8709bd6c01d445c8e2489f4980e6577fd91895755a3a771`).
No product build/collector/browser run was needed for these documentation-only
changes. PROJECT_STATUS.md and WORK_LOG.md distinguish the completed audit from
unapplied report rewrites.

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
filter and direct child navigation pass; no report-console errors. The local
source refresh exported 468 records; GDELT 429 fell back to Google News RSS.

Source commit `6b9dc30` deployed successfully in run `37639214281` (2m34s).
The public export has 855 source records / 16 reports / 26 revisions / 46 chapters.
All sixteen authored documents match the local export; five new public pages and
normalized CSS `de2fc07102be` match. Live main featured the hackathon report and
its parent filter showed two accumulated reports. The published learning report
has eight disclosures and thirteen official references; Enter opens chapter two,
chapter seven shows the seven-day plan, and no console errors were reported.
Public screenshots were taken at actual1280px. The requested390px override stayed
at1280px; public narrow checks are therefore not claimed. Matching production
output was tested locally at actual320/390px. The viewport override was reset.
Main/report tabs are retained as deliverables; prior selection/review tabs remain
handoffs. Captures and deployment/browser receipts are inside the registered root.

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
- forty-six expandable learning chapters across fifteen development reports; MCP Apps includes seven and hackathon preparation includes eight, with terms, process, examples and evidence,
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
