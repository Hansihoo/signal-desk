# Decisions

## 2026-06-18: SQLite is the Source of Truth

Markdown and HTML are generated outputs. They should not become the canonical data store.

Reason:

- dedupe,
- search,
- filtering,
- future multi-domain expansion,
- reliable regeneration.

## 2026-06-18: Start With Housing MVP

Housing notices are concrete, structured, and useful enough to validate the full loop.

## 2026-06-18: Use No Python Dependencies in MVP

The current MVP runs on Python 3.8 standard library.

Reason:

- easy local execution,
- fewer setup failures,
- simpler handoff.

## 2026-06-18: Keep Generated Outputs Out of Git

DB, raw snapshots, reports, images, and HTML outputs are local artifacts.

Reason:

- avoid noisy commits,
- avoid accidentally committing large or stale data,
- keep repo focused on code and docs.

## 2026-06-18: Do Not Guess Missing Price Data

When official HTML does not expose deposit/monthly rent/price, cards show `원문/PDF 확인`.

Reason:

- housing decisions need source accuracy,
- many official pages keep price tables in attached PDF/HWP files.

## 2026-06-19: Prepare Weekly News With Existing Data/Feed Tools First

The weekly big-news tab should start from existing open data and feed tooling rather than a custom crawler.

Reason:

- broad news is noisy and benefits from source-frequency scoring,
- GDELT and Media Cloud already solve much of the broad news discovery problem,
- Miniflux/FreshRSS/Newscope-style tools cover fixed feeds and RSS-less pages,
- Signal Desk should focus on normalization, search, scoring, rendering, and Codex handoff.

## 2026-06-19: Keep Translation Explicit

Weekly news cards should have Korean briefing fields, but real machine translation should be an explicit provider choice.

Reason:

- Korean Google News RSS can produce Korean cards without translation,
- GDELT can provide better original article URLs but often returns non-Korean titles,
- high-quality automatic translation needs a stable engine such as a self-hosted LibreTranslate endpoint or a future LLM step,
- the fallback should never pretend that an untranslated title was translated.

## 2026-06-20: Keep Job Salary as a Separate Research Field

Career job cards should show a 10-year salary estimate, but that value is not assumed to come from the posting itself.

Reason:

- postings often omit salary,
- salary estimates require separate sources such as salary reviews, company disclosures, or market data,
- the visible card should stay concise,
- `salary_basis` preserves how the estimate was researched without cluttering the mobile view.

## 2026-06-20: Use Saramin API as the First Live Jobs Adapter

The first live jobs adapter should use Saramin Open API rather than scraping logged-in job pages.

Reason:

- Saramin provides an official `job-search` API with JSON output,
- API access can be controlled through `SIGNAL_DESK_SARAMIN_KEY`,
- raw responses can be stored under `data/raw/jobs/`,
- list results are enough for weekly candidate discovery,
- detailed job text and official company pages can be added later without changing `job_items`.

## 2026-06-20: Make the Tabbed Desk Wider Than the Brief Image

The concise housing `brief` remains capped at `390px`, but the multi-topic `desk` defaults to `645px`.

Reason:

- `brief` is a compact share image,
- `desk` is an interactive mobile HTML page with tabs,
- 390px and 430px made the tabbed screen feel too narrow in the browser,
- 645px gives housing/job cards enough room for detail while still fitting a mobile-style share image.

## 2026-06-20: Keep Housing Profile Filtering Conservative

The housing profile filter hides only notices that are clearly inconsistent with Theo's local profile and official 2026 기준 values.

Reason:

- 청약 eligibility depends on notice-specific income, asset, household, and home-ownership calculations,
- a local profile parser can miss nuance, so ambiguous notices should stay visible,
- the private profile file should remain outside the repository and be passed with `--profile` or `SIGNAL_DESK_PROFILE_PATH`,
- visible cards should say why a remaining notice still needs manual review rather than pretending to make a final eligibility decision.

## 2026-06-20: Make Housing Tab Cards More Document-Like

The housing tab can be longer than the concise `brief` and should prioritize direct review usefulness.

Reason:

- Theo should not need to open every card just to see address, area, supply, price, condition, and schedule,
- official pages often lack direct image data in normalized HTML, so the first version uses a visual snapshot layout rather than guessed images,
- actual site images, floor plans, or PDF thumbnails should be added only when extracted from official attachments or stable source fields.
