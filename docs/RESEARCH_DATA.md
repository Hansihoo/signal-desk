# Research data contract

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

# Import authored research into SQLite and export, without rendering.
python -m housing_watch research-data --input config/research_reports.example.json

# Generate the existing website when desired.
python -m housing_watch publish
```

Default data-only output: `data/research.json`. Publishing writes the same contract
to `site/research-data.json` and renders the representative pair from its selected
report. These JSON files are ignored generated outputs; `--output` takes a JSON path.

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
| `featured_report_id` | Selected report for the representative pair. |
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

Presentation sources: `briefing_preview_home.html`, `briefing_preview_report.html`,
`briefing_preview.css`, `briefing_preview.py`. Templates own layout/navigation; report
text, date, numbers, citations, and thresholds come from data. Legacy source library
and dated snapshots retain their existing format. No new collectors or weekly
automation are introduced by this separation.

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
