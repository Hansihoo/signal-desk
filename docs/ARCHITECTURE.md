# Architecture

## Intent

Signal Desk is a local-first research pipeline. It prepares important updates before Theo asks Codex questions.

The first implemented domain is housing notices. The architecture should stay broad enough for jobs, IT news, stocks, and policy updates.

The source of truth is SQLite, not Markdown.

```text
Official sources / fixed watches / future APIs
  -> source adapters
  -> raw snapshots
  -> normalized SQLite items
  -> search/context commands
  -> Markdown report
  -> mobile HTML briefing
  -> optional PNG export
```

## Core Design

### Source Adapters

Each source adapter fetches one source and normalizes rows into a shared item shape.

Current adapter:

- `seoul_housing_table`: parses Seoul Housing Portal table pages for LH/SH notices.

Future adapters:

- `lh_openapi`: public data API for LH notices.
- `myhome_openapi`: public housing recruitment notices from MyHome.
- `changedetection_webhook`: changes detected from pages without stable APIs.
- `n8n_webhook`: records pushed from n8n workflows.
- `jobs_*`: future job source adapters.
- `news_rss`: future IT/news RSS source adapter.
- `opendart`: future Korean disclosure source adapter.

### Storage

`data/housing_watch.sqlite` stores the current MVP data:

- `items`: normalized notices.
- `raw_snapshots`: fetch metadata and raw snapshot paths.
- `items_fts`: optional FTS5 search index when SQLite supports it.

Markdown and HTML are regenerated from the database.

### Search

Search is hybrid:

- SQLite FTS5 when available.
- Lightweight semantic scoring based on token overlap and Korean character n-grams.

The semantic-lite scorer is intentionally dependency-free. Later, it can be replaced or supplemented with embeddings.

### Reporting

Reports are derived outputs:

- `reports/YYYY-WW.md`: weekly Markdown report.
- `reports/latest.md`: latest Markdown report copy.
- `site/latest.html`: mobile-first visual briefing.
- `reports/latest.png`: optional screenshot output.
- `site/brief.html`: concise mobile briefing for sharing.
- `reports/brief.png`: concise mobile image capped to the requested width.

### Review Loop

`python -m housing_watch review --width 390` checks whether the generated data and concise briefing are ready to share.

The review command intentionally focuses on operational quality:

- local DB has items,
- active notices exist,
- official links are present,
- concise HTML has a mobile viewport and max-width,
- long text has wrapping protection,
- concise card count stays small,
- PNG width does not exceed the mobile delivery width.

## Why This Shape

This follows the same broad pattern used by RSS readers, monitoring systems, and AI news curators:

```text
fetch -> normalize -> persist -> classify/search -> render/deliver
```

It keeps each piece replaceable. For example, n8n can later handle collection while this project keeps storage, search, and reporting.

## Naming Note

The repo is `signal-desk`, but the current Python package is `housing_watch` because the first MVP is housing-only. Rename or generalize the package only after a second domain is implemented.
