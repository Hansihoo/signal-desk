# Developer opportunity research

This is an additional Signal Desk research domain, not a replacement for the multi-topic homepage.
The supplied specification is preserved verbatim in [the original requirements](ai/OPPORTUNITY_REQUIREMENTS.md).

## Current implementation scope

On 2026-10-03, Theo explicitly selected HTML structure, categories, and requirements first.
Implemented in this phase: a new main-library topic, eight category routes, outline metrics,
technical tags, collection/filter requirements, official-source candidates, an individual
report template, and a self-contained downloadable HTML template. There are no collected
opportunity records or new program tables/adapters yet. The topic's `planned` collector
is skipped during public collection. It cannot contribute fake records to the library.

The remaining pipeline, actual data filters/charts, verifier/change log, and three-phase
schedule below are future requirements, not completed features. Existing dated JSON keeps
its original catalog. The original cloud briefing therefore does not gain this new topic.

Editable files: `config/opportunity_outline.json` controls categories/tags/fields/sources;
`public_site.html`, `.css`, and `.js` control the shared shell; `opportunity_report.html`
controls the standalone download shell. UI entries use existing topic routes with
`?section=<category>` and `?template=1`. Generated `report-template.html` includes inline
styles and no JavaScript or runtime asset dependency.

## Product contract

The audience is an AI/software solo developer looking for an action they can take now.
Opportunities include hackathons, competitions, security/AI safety bounties, OSS patch
rewards, grants, developer programs, marketplaces, freelance demand, and separately
labelled revenue case studies. Do not turn product launches or investment news into
opportunities. Keep case studies separate from currently open participation programs.

Each program needs an official source and a direct application/submission/rules link.
Keep original currency and distinguish individual maximum, total prize, grant limit,
base reward, actual payout, MRR, ARR, and founder-reported revenue. Unknown amounts,
dates, country restrictions, and status stay null/UNKNOWN. Never infer them with an LLM.

Status is OPEN, ALWAYS_OPEN, DEADLINE_SOON (14 days), CLOSED, or UNKNOWN. Default listings
show only the first three after verification. CLOSED belongs in the archive. Label
OFFICIAL, VERIFIED, MEDIA REPORTED, SELF REPORTED, and UNVERIFIED evidence separately.
Source failure must not silently update a program to open or erase existing data.

## Fit with the current repository

Keep Python, SQLite, source adapters, generated static HTML/JSON, GitHub Actions, and
GitHub Pages. A static JSON export is sufficient for the initial read-only API surface;
adding a paid application server or replacing the stack is unnecessary for this domain.
Use a dedicated opportunities table and change-event table when collection is implemented,
because deadline, reward meaning, eligibility, verification, and program deduplication
do not fit the existing news table. Preserve immutable raw snapshots and dated reports.

The collection pipeline is adapter -> normalizer -> verifier -> canonical program
deduplication -> SQLite -> static JSON/HTML -> dashboard. Deduplication considers
organization, stable program ID, canonical title, and official URL. Emit a change event
only when deadline, reward, scope, rules, status, or execution links change; a successful
recheck alone is not a new opportunity. Compute remaining days from a timezone-aware
deadline; a date without a known timezone must not gain a fabricated time.

## Screen and report structure

The main library leads to Developer Opportunities, then an opportunity category, then
an individual report. The domain overview contains executable/open count, 14-day deadline
count, always-open count, today's new count, and today's changed count. Before a collector
is connected, display collection-pending indicators rather than live zero counts.

The report follows: topic/core -> summary -> structured data -> action -> references.
Its data contains reward fields, deadline/timezone, eligibility/country, scope/rules,
application/submission/documentation links, source/evidence labels, and verification time.
An HTML download should retain those fields and references without external runtime dependencies.
Provide category/status/organization/reward/deadline/country/source and technical-tag filters
when real records are available; do not ship inactive controls that appear to filter data.

Use meaningful deadline/category/reward/new/change views once real data is present.
No invented scores, star ratings, success estimates, fabricated example payouts, or
decorative charts masquerading as measurements.

## Source and automation plan

First adapters: MSRC, Google Bug Hunters, OpenAI/Bugcrowd, Devpost, Kaggle, and GitHub.
Candidate seed programs: Microsoft Bug Bounty, Google AI VRP, Chrome VRP, OSS Patch
Rewards, OpenAI Security Bug Bounty, and OpenAI Safety Bug Bounty. A candidate source
link is not a verified open program. Fetch and verify program-specific terms before promotion.

Requested future schedule is 19:00 collect, 19:30 verify/deduplicate, and 20:00 daily report
in Asia/Seoul. Scope it to this new domain so the other research areas retain their schedule.
GitHub cron is approximate; sequencing collector/verification/report in a workflow avoids
reporting stale data when jobs are delayed. Daily reports should contain only new programs,
material changes, approaching deadlines, and new case studies, not yesterday's unchanged list.

## Authoritative starting references

Checked on 2026-10-03 for reference discovery, not full program verification:

- [Microsoft program directory](https://www.microsoft.com/en-us/msrc/bounty) links program scope/terms and its reporting route.
- [Google Bug Hunters](https://bughunters.google.com/) is the official program portal; program-specific rules still require verification.
- [OpenAI Safety Bug Bounty overview](https://openai.com/index/safety-bug-bounty/) links separate Safety and Security engagements on Bugcrowd.

Maintain field-level source evidence and the last successful verification time during implementation.
