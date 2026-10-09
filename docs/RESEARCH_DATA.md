# Research data contract

## Broad AI research provenance policy, 2026-10-09

[Research operations](AI_RESEARCH_OPERATIONS.md) defines required provenance meanings:
original publication/update, first/latest successful acquisition, actual content
review, measurement/effective periods and next checks. These are future common
contract requirements, not an extension of the validated report schema v1.
Existing `checked_on`, revision/storage and export generation dates keep their
current meanings. References still accept only `id`, `title`, `url`, `description`.
Until storage/export/render compatibility and failure retention are implemented,
record actual original URLs, dates, check scope and gaps in
[the review log](ai/AI_RESEARCH_REVIEW_LOG.md). A generated page is not new evidence.

## Accumulating AI model ledger, 2026-10-08

`model_ledger` is an additive export property containing `schema_version: 1`,
`records`, immutable `history`, and the latest twenty `runs`. It is separate from
the authored report schema and source-news catalog. Each observation preserves
model/provider, source kind, original fields, units/conditions, source URL and
original date (verified/observed/measured according to source kind); runtime
metadata adds revision/change/retention state. The UI names this `원자료 날짜`.
SQLite tables are `model_observations`, `model_observation_revisions` and
`model_sync_runs`. Refreshes import all seven upstream files atomically and
change only new/different observations. Missing rows and old suites remain.
`ai-models --input` accepts officially reviewed partial additions; the complete
upstream refresh never overwrites them. See [AI model operations](AI_MODEL_RESEARCH.md).
The research subpage is generated from this ledger, with filters, CSV, original
evidence and per-record revisions. It does not replace immutable report editions.

## AI model reference connection, 2026-10-08

Theo's model research catalog is collected as `AI 개발 / LLM 모델` source records;
the source tier is authored research, with original update/check dates and hashes.
These references do not become independently reviewed reports automatically.
The new immutable `ai-model-connection-2026-10-08` batch adds `llm-model-comparison`
under development/AI models/API, without changing earlier documents or the featured
MCP report. See [AI model operations](AI_MODEL_RESEARCH.md) for collection/review
scope and limits. Local total: 17 current reports / 28 revisions; public deployment
has not been performed for this change.

## Content authoring quality, 2026-10-08

Read the [writing guide](RESEARCH_WRITING_GUIDE.md) before authoring or revising
reports. Reader question, prior knowledge and intended outcome are editorial
working metadata in documentation. The complete explanation
comes before the summary/table representation. Required fields and citation IDs
validate structure, not meaning, source entailment or reader comprehension.

The [content audit](RESEARCH_CONTENT_REVIEW.2026-10-08.md) inspected the sixteen
current SQLite documents and forty-six chapters. It includes specific role and
example inconsistencies plus a per-report repair plan. Representative improvements
are in [the prose examples](RESEARCH_WRITING_EXAMPLES.md). The MCP Apps example is
now applied in a new batch; the function-calling draft remains unpublished.
A reviewed correction needs a new immutable batch,
not an edit to an already-applied batch or silent replacement of history.

## Reader-purpose main and report, 2026-10-08

`config/development_reader_purpose.2026-10-08.json` revises only MCP Apps (3rd
edition); the other fifteen current documents and earlier editions are unchanged.
It is the featured report. The main board and latest-topic panels display `deck`
sentences, retaining full-text search and accumulating report IDs.

Optional v1 `explanation` uses the same `{id,title,lead,blocks}` content contract
as `learning`. Blocks are paragraph/steps/terms/code with validated source IDs.
These primary chapters render visibly before data/result. `learning` remains
optional disclosure depth. Chapter IDs are unique within each collection and
anchors have separate prefixes. Empty/absent explanation emits no section or
navigation link. Plain text is escaped; blank lines form separate paragraphs.
No presentation fields or reader-brief metadata are stored in report data.
See [the application record](READER_PURPOSE_APPLICATION.2026-10-08.md).

## Reviewed expansion, 2026-10-07

`config/development_updates.2026-10-07.json` adds five reviewed reports and twenty
learning chapters in a new once-only batch. Earlier batches and eleven documents
are unchanged. Current total: sixteen reports, twenty-six stored revisions,
forty-six chapters. The featured report is `hackathon-tech-roadmap`.

The hackathon learning page lives under
`["지원·참여", "해커톤·공모전", "기술 학습"]`. Topic paths remain content labels;
the renderer builds a nested tree, links a single deep leaf directly to its report,
and includes descendants when filtering a parent. No schema/layout fields were
added. Tests exercise four levels, escaping, relative history paths and counts.

Research covers organizer requirements in three selected 2026 events and current
official technical documentation. The trend interpretation and suggested study
sequence are editorial judgments, not measured industry popularity. Google
submission ended August 31; October 8 is the planned winner announcement.
Elastic's July event ended. IBM Bob is restricted to US residents. Tables carry
sources and limitations; study exercises and time plans are visibly examples or
recommendations. No invented popularity scores, benchmark results or savings
claims are used.

Twenty-one primary-source responses and hash receipts are retained under ignored
`data/raw/research/2026-10-07-expansion/`. Existing public feeds were separately
refreshed; their excerpts are not automatically treated as reviewed conclusions.
The five reports are manual research additions; weekly changed-only deep review
remains planned.

Research content and web presentation are independent. SQLite is the authoritative
store; JSON is an exchange/export format, and HTML/CSS is a replaceable view.

```text
official feeds / authored research JSON
    -> validation and normalization -> SQLite
    -> research JSON -> HTML/CSS presentation
```

## Data-only workflow

```powershell
# Export accumulated public data without fetching or rendering.
python -m housing_watch research-data

# Refresh configured public sources, then export JSON only.
python -m housing_watch research-data --collect

# Import reviewed authored research into SQLite and export, without rendering.
python -m housing_watch research-data --input config/research_quality_pilot.2026-10-09.json --quality config/research_quality_pilot.2026-10-09.quality.json

# Generate the existing website when desired.
python -m housing_watch publish
```

Default data-only output: `data/research.json`. Publishing writes the same contract
to `site/research-data.json` and renders the Editorial main, every stored report,
and previous editions. These JSON files are ignored generated outputs; `--output`
takes a JSON path.

Automatic authored research uses the separate [question/evidence workflow](RESEARCH_PIPELINE.md).
Its plan, original excerpts, claim mappings and review receipts are a quality sidecar;
report/export v1 remains unchanged. Imports require `--quality`, or the explicit
`--legacy-unreviewed` compatibility override with a warning. The override preserves
old imports but does not record substantive review. Existing immutable publication
batches remain compatible; new sidecar-backed batches verify both documents before import.

Data-only collection may update SQLite/raw-source snapshots; it never generates
HTML/CSS/PNG or changes dated website archives. Partial failures retain earlier
records and appear in `health` and warnings. A successful command means export
succeeded, not that every source succeeded.

## Export envelope, version 1

| Field | Contents |
| --- | --- |
| `schema_version` | Integer contract version, currently 1. |
| `generated_at` | UTC export time, distinct from evidence check dates. |
| `topics` | Stable IDs, names, descriptions; no asset paths or layout. |
| `source_records` | Public source IDs, topic/category, title, excerpt, URL/name, publication/first-seen dates, existing score/basis. Collected records, not reviewed conclusions. |
| `reports` | Reviewed/authored content using the report contract below. |
| `report_versions` | Report ID, current revision, UTC saved time. Prior documents remain in SQLite. |
| `report_history` | Additive v1 field: all stored revisions with ID, revision, UTC saved time and validated plain-content document. No presentation fields. |
| `featured_report_id` | Selected report for the representative pair. |
| `publication_report_ids` | Reviewed report IDs in editorial order; independent of layout. |
| `health` | Results/warnings for this export; empty without collection. |

Public source export reuses the existing explicit allowlist and excludes private
jobs/salary/profile, credentials, and arbitrary raw payloads. Authored imports are
intended for publication: only import content that belongs on the public site.

## Report content

`config/research_reports.example.json` is **hand-authored input**, not a generated
report. It contains the existing report's content previously embedded in HTML.

| Field | Contents |
| --- | --- |
| `id`, `topic_id`, `topic_path` | Stable IDs and a hierarchy of topic labels. |
| `title`, `description`, `deck` | Subject, description, headline finding. |
| `checked_on`, `scope`, `source_note` | YYYY-MM-DD evidence check date, applicable scope, source basis. |
| `highlights` | Plain-text main-page overview bullets. |
| `summary` | Points with `kind` (`fact`, `estimate`, `judgment`), label, text, and source IDs. |
| `metrics` | Numeric values, units, labels, qualifiers, source IDs; empty when unnecessary. |
| `datasets` | Numeric rows, shared unit, fact/estimate kind, assumptions, methodology, note, sources, optional threshold; empty when unnecessary. |
| `tables` (optional) | Plain-text comparison columns and rows with source IDs and a scope note. No cell markup or styles. |
| `learning` (optional) | Ordered explanatory chapters with stable IDs, titles, short leads and typed plain-text blocks. Facts cite evidence; examples and recommendations are labelled. |
| `result` | Conclusion title and points using the same point contract. |
| `references` | Unique IDs, titles, credential-free HTTP(S) URLs, descriptions. |
| `caveats` | Scope/uncertainty text and applicable source IDs. |

No CSS classes, colors, coordinates, chart widths, or HTML belong in this contract.
The renderer chooses chart geometry and numeric formatting. A different design can
use tables or different charts. The current numeric contract supports nonnegative
comparison rows; time series/negative values need an explicit contract extension.

Input: `schema_version: 1` and `reports: [...]`. Exported JSON can also be re-imported:
only `reports` are imported; `source_records`/metadata are not ingestion instructions.
Report fields are required. Arrays may be empty except topic labels, highlights,
and dataset rows. Unknown/missing report fields, duplicate IDs, invalid dates/URLs,
dangling source references, invalid numeric values, unsupported versions, factual
points/metrics/data without sources, and estimated datasets without assumptions are rejected. All documents
validate before a transactional import. The renderer escapes plain text.

## Explanatory chapter contract

Each optional `learning` chapter has `id`, `title`, `lead` and a nonempty
`blocks` array. Block fields are `type`, `kind`, `title`, `source_ids` plus:

- `paragraph` / `code`: nonempty `text` (code remains escaped text).
- `steps` / `terms`: nonempty `items`, each with `label` and `text`.

`kind` is `fact`, `example`, or `judgment`. Factual blocks require at least
one existing reference; hypothetical examples and editorial recommendations are
visibly distinguished. Duplicate chapter IDs, unknown fields/types, empty content
and dangling evidence IDs fail validation before storage changes. IDs are local to
the report. Version 1 remains additive: older reports omit learning entirely.

The view renders independent, initially collapsed native `details`/`summary`
sections with keyboard support. It adds the report contents link only if chapters
exist. No JavaScript or data field controls layout, colours, or open state.
Definitions, process steps and examples remain in SQLite/exported JSON when the
HTML design is replaced. The time and notice examples explain MCP Apps; Signal
Desk's static disclosures are not a running MCP App or an implemented MCP server.

## Revisions and editing

`research_reports` holds current ID, revision, hash, JSON document, UTC update time.
`research_report_revisions` retains immutable documents keyed by report/revision.
Identical imports do not change timestamps or create revisions; changed documents
create the next revision. Imports do not delete unlisted reports. Existing complete
SQLite cloud backups also preserve these tables.

Publishing seeds the example only when missing; it never replaces database edits.
Editing the example file alone therefore does not update an existing report:
explicitly import, then publish. Editing generated JSON alone is not persistent;
import reviewed changes into SQLite before exporting again.

Presentation sources: `editorial_shell.html`, `editorial_home.html`,
`editorial_report.html`, `editorial.css`, `editorial.js`, `editorial.py` and the content
helpers in `briefing_preview.py`. Actual template CSS/fonts/licenses live in
`housing_watch/assets/editorial/`. Templates own layout/navigation; report text,
date, numbers, citations, and thresholds come from data. Legacy source library
and dated snapshots retain their existing format. No new collectors or weekly
automation are introduced by this separation.

## Initial development research, 2026-10-04

`config/development_baseline.2026-10-04.json` is reviewed authored input, not a
generated export. Ten reports cover AI APIs, Agent/MCP, safety, OSS rewards, grants,
developer programmes, hackathons, marketplaces, freelance demand, and a small SaaS
case. Twenty-one distinct official/first-party URLs support the content. Raw public
research evidence is retained under `data/raw/research/2026-10-04/` and ignored by Git.

`config/research_publication.json` chooses the featured report and report order and
lists immutable reviewed input batches. On export/publish, unapplied batches are
validated and imported with a receipt in `research_import_batches`. Receipt and
report changes share one SQLite transaction. Repeating publication skips an applied
batch, preserving later database edits. Modifying an applied batch is rejected:
add a new dated batch ID for subsequent reviewed changes. Source-controlled authored
inputs let the cloud apply the same research without replacing its accumulated DB.
They contain public content only; generated DB/raw/JSON/HTML/PNG remain ignored.

`config/development_learning.2026-10-04.json` is the next immutable reviewed
batch. It adds 26 learning chapters across the same ten reports, including seven
MCP Apps chapters, and clearer MCP copy. It adds official MCP architecture,
quickstart and Apps specification, GitHub app differences and Stripe MRR definition
references. The previous baseline input is unchanged. Publishing updates each
report revision once and preserves accumulated source records and older revisions.

`/preview/index.html` presents **all stored reports**, grouped by topic, with text
search, category filters and eight entries per page. The curated manifest still
chooses the lead report; adding a report does not require changing the manifest to
appear on the board. Stable report
URLs are `/preview/<report-id>.html`; `report.html` aliases the current featured
report. All stored reports also get an address, including the earlier storage
report at `/preview/github-pages-storage.html`. Quantitative comparisons use bars;
eligibility and timelines use semantic tables. Each report retains summary, data,
result, references, evidence dates, and scope. Main-page copy leads to the reviewed
report; the separate existing feed library/daily archives keep their routes.

Evidence limits are visible: Google dynamic rules were first checked through their
official indexed content and later confirmed on the rendered official page; the Bugcrowd rule body was not fully readable, so current
reward amounts are not asserted. Upwork percentages measure 2025 US-origin contract
earnings, not job counts. Tally values are founder-reported historical MRR, not
audited profit or a one-person income. Eligibility and future deadlines are not
inferred from promotional maximums. Weekly deep review/changed-only scheduling is
still a separate, unimplemented workstream; the existing daily feed refresh continues.

## Editorial accumulation and report history, 2026-10-07

The user explicitly selected `html5up-editorial` and expanded scope to every
research report. `publish` renders the main and all validated current reports,
sorted by evidence check date descending, then stable ID. Categories are derived
from `topic_path`; sidebar children lead to filtered lists. Reports in the same
category accumulate on that list instead of creating duplicate tree entries.

New reviewed subjects need a new stable report ID. Revising the same subject keeps
its current URL and creates a SQLite revision. Every earlier revision is rendered
at `/preview/history/<report-id>-r<revision>.html` using its own stored document;
`/preview/history/index.html` and the report sidebar link those editions. Identical
imports do not create new editions. A design-only publication changes neither the
authored text nor evidence dates/revisions. These HTML documents are generated
outputs and remain outside source commits.

Design-review mode embeds CSS/scripts/licensed font subsets in a standalone HTML
document. Production uses one cache-versioned local stylesheet containing the
fonts, with parent-relative history links; scripts remain embedded. Neither mode
requests remote fonts or scripts. The original Latin fonts are packaged with a
Korean heading subset and local serif fallback. Measured local standalone preview
is about 9.5 MB; the shared-style production preview is about 0.89 MB for 11 current
reports, 10 older editions, main/history/license and CSS. A current MCP HTML report
is about 30.5 KB and the shared font/CSS file about 344 KB. These are measured
outputs, not a lifetime guarantee. Stored data remains independent of either mode.

Verification: 71 tests, compileall, JS syntax check, publish/brief/summary desk and
housing review pass. Existing briefing PNGs inspected. 1,067 local internal links/stylesheets
resolve; mobile width 390 verified on main and all 11 reports with all 26 chapters
expanded, 14px body and no horizontal overflow. Search, empty/reset, top/subtopic
filters, pagination, previous/current edition navigation and Enter/Space native
disclosure were exercised in the browser. Weekly deep research remains unimplemented.

Verification: 63 tests, compileall, publish, brief, summary desk and review pass.
Existing images were inspected; 13 research pages / 271 internal links pass. All
ten reports and the main fit 390px; 430px main, earnings and MRR views pass. Official
Upwork navigation/back and console checks pass. [Deployment 37133263430](https://github.com/Hansihoo/signal-desk/actions/runs/37133263430)
succeeded in 2m15s. Public JSON contains 360 accumulated source records and 11 reports;
all ten new documents exactly match the reviewed inputs. Public CSS matches committed
source hash `22fb84de3dc9`. Main and representative report tabs/captures are retained.

## Verification on 2026-10-03

59 tests and compileall pass, including idempotence, revision retention, invalid batch
rejection, database-error rollback, citation/number validation, escaped data rendering,
and data-only CLI isolation. Actual data-only refresh exports 325 local source records
and the existing authored report while all 29 website files remain byte-identical.
GDELT 429 falls back with a recorded warning. Publish/brief/summary desk/review, images,
and 40 local links pass. [Deployment](https://github.com/Hansihoo/signal-desk/actions/runs/37126426967)
succeeds; public JSON contains 339 accumulated source records and the identical report.
390/430px overflow, data-driven chart ratios/threshold, keyboard disclosure, main/report
navigation and console checks pass. Published CSS matches committed LF source bytes,
hash `60797995360d`; local CRLF checkout bytes have a different hash. Generated outputs
are retained outside Git. Main/report layout approval and weekly review remain separate.

Editorial publication [37628018293](https://github.com/Hansihoo/signal-desk/actions/runs/37628018293)
succeeded in 1m28s. Live export: 776 source records, 11 current reports, 21 stored
revisions. Current and older authored documents match; local/cloud saved timestamps
are intentionally distinct. All 25 public pages use `171be08edf65`, the normalized
CSS content hash; Windows filesystem bytes differ by line endings. Native public
main→MCP navigation, seven expanded chapters at 390px, official quickstart/back and
console pass. Main/report and local selectable review remain available.

The independent `model_pages` export contains complete source documents/assets/current editions/history/sync results. It does not add fields to the authored report schema. Reviewed official model observations can deploy through config/ai_model_publication.json immutable batches; rendering/export applies these facts once and refuses modified applied batches.
