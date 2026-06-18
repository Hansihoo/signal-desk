# Data Model

## SQLite

Default path:

```text
data/housing_watch.sqlite
```

The DB is generated locally and ignored by git.

## `items`

Core fields:

- `source_id`
- `external_id`
- `title`
- `url`
- `agency`
- `category`
- `region`
- `status`
- `published_at`
- `deadline_at`
- `summary`
- `raw_text`
- `content_hash`
- `state`
- `importance`
- `first_seen_at`
- `last_seen_at`

Housing detail fields:

- `address`
- `area_range_m2`
- `area_range_pyeong`
- `supply_units`
- `deposit`
- `monthly_rent`
- `price`
- `eligibility`
- `application_period`
- `move_in_month`
- `detail_summary`
- `detail_text`
- `detail_collected_at`

## `raw_snapshots`

Fields:

- `source_id`
- `raw_path`
- `fetched_at`
- `item_count`

## FTS

When SQLite supports FTS5, `items_fts` is created.

Search currently combines:

- token overlap,
- Korean character n-grams,
- importance boost,
- active-status boost,
- deadline boost.

This is intentionally dependency-free. Later it can be supplemented with embeddings.

## Output Contracts

### `context`

Context output should be concise and structured for Codex. It should not dump full raw HTML.

### `brief`

Brief output should be mobile-shareable.

Card fields:

- status
- D-day
- title
- address
- area
- supply
- price
- eligibility
- agency/category/region
- schedule

If a field is not available in official HTML, use `원문 확인` or `원문/PDF 확인`.

