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

