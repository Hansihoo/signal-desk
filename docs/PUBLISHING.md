# GitHub Pages and continuous collection

## Deployment

The existing `Hansihoo/signal-desk` repository hosts the public site through GitHub Pages.
Live site: https://hansihoo.github.io/signal-desk/
`.github/workflows/deploy.yml` runs on main-branch pushes, manual dispatch, and daily at
20:00 UTC (05:00 Asia/Seoul the following day). GitHub scheduling is approximate.

The workflow tests the code, restores previous state, collects public sources, generates
the site, checks the housing briefing, saves state, and deploys a Pages artifact.
One concurrency group serializes all collection and deployment runs.

Verified on 2026-10-03: [first deployment](https://github.com/Hansihoo/signal-desk/actions/runs/37093169002)
and [restore plus refresh](https://github.com/Hansihoo/signal-desk/actions/runs/37093390480)
both succeeded with 39 passing tests. The second run restored the first snapshot,
increased the public library from 165 to 177 records, kept the original daily briefing,
and saved a second release asset. Live search, topic filtering, archive navigation,
and the 430px mobile layout were checked in the browser.

```powershell
python -m housing_watch publish --collect
python -m housing_watch publish
```

The second command renders existing local data without fetching sources.

Deployment recovery on 2026-10-09: run37804406384 initially could not find its
uploaded artifact; rerunning the job left two same-name artifacts, which the
deployment action rejected. Use a fresh workflow run instead of rerunning that
job; this creates a distinct run's output without deleting the earlier artifacts.
The initial artifact-visibility failure's underlying service cause is unconfirmed.

Matching attempt-specific upload/deployment names were evaluated and YAML-checked,
but GitHub refused that workflow edit because the current Hansihoo OAuth credential
lacks the workflow scope. The unpublished edit was withdrawn; the existing workflow,
permissions, durable release state and site paths remain unchanged. A future workflow
change requires an authorized workflow-capable credential rather than switching accounts.
[Upload's name input](https://github.com/actions/upload-pages-artifact/blob/v5.0.0/action.yml)
and [deployment's artifact_name input](https://github.com/actions/deploy-pages/blob/v5.0.1/action.yml)
support the matching names; [metadata selection](https://github.com/actions/deploy-pages/blob/v5.0.1/src/internal/api-client.js)
requires exactly one matching artifact.

## Public experience

- `site/index.html`: recent updates, keyword search, topic filtering, and full collected library.
- `site/research/<topic-id>/index.html`: independent research topic pages.
- `site/topics.json`: topic metadata, counts, and latest publication dates.
- `site/library.json`: selected public fields from AI/news/housing records.
- `site/status.json`: generation time and source health.
- `site/archive/index.json`: dated briefing catalog.
- `site/archive/YYYY-MM-DD/briefing.json`: immutable first successful briefing for that Korean date.
- `site/archive/YYYY-MM-DD/index.html`: readable historical snapshot.
- `site/ai-news.html` and `site/brief.html`: existing detail briefings.

Search on the public site covers exported AI news, general news, and housing. The older
local `search/context` commands remain housing-only. Article links and feed excerpts
are collection aids; they are not presented as independently verified research.

The latest site can update repeatedly in a day. The first saved daily briefing is
preserved. Historical pages are rebuilt from their saved JSON, never from today's data.
Records accumulate from the first cloud collection; no complete historical backfill is promised.

The public homepage is a research hub with all topics selected initially. Add domains and
public feeds through `config/research_topics.json`; see `RESEARCH_HUB.md` for instructions
and the current free-hosting envelope. Pages does not collect user submissions or run
analytics; GitHub's hosting infrastructure still records visitor IPs for security.

## Durable state

Generated databases, raw responses, HTML, and reports stay out of source commits.
Each successful build saves a compressed snapshot as an asset on the monthly prerelease
`signal-desk-data-YYYY-MM`. Asset names include UTC timestamp, run ID, and attempt number.
Snapshots are retained rather than replaced. Each next run selects the newest state asset
across months and restores SQLite, raw source responses, and the site archive.

Actions artifacts are used only to deploy Pages; their expiration does not erase the
research store. A failed release API request or invalid restore stops the run rather
than silently starting an empty database. Tar paths and link types are checked before
writing; SQLite integrity is checked after restore.

Public GitHub schedules may disable after 60 days of repository inactivity. The first
successful deployment each UTC month updates `docs/ai/CLOUD_STATUS.md` with an operational
receipt. Its commit uses `[skip ci]` to avoid a recursive collection run.

## Privacy and scope

The repository, Pages site, and release assets are public. Cloud collection uses only
public housing sources and AI/general news feeds. It never imports local job JSON,
salary estimates, private profiles, cookies, or local credentials. Public-site export
excludes jobs and raw payloads; cloud backup rejects a DB containing local job imports.
Do not seed public cloud state from a private local database.

On partial source failures, previously saved information remains available and the home
page shows a collection-health notice. An empty first collection fails deployment.
Use source health and the last successful workflow when checking freshness.

## Operations and recovery

Inspect the `Collect and publish Signal Desk` workflow for source errors or deployment failures.
Use **Run workflow** to refresh manually. Disable that workflow to pause collection.
The source-of-truth database can be recovered with:

```powershell
python -m housing_watch.cloud_state restore --repo Hansihoo/signal-desk --root <existing-scratch-directory>
```

Restore only into an explicitly chosen empty scratch directory, never over a private
local DB. Raw responses and snapshots grow over time; GitHub currently limits an individual
release asset to 2 GiB and a release to 1,000 assets. Revisit storage before those limits.

References: [Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages),
[scheduled events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows),
[release storage](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).

## Model documents and reviewed facts

As requested on2026-10-08, the daily source schedule moved to05:00 Asia/Seoul. `publish --collect` imports complete model documents and shared assets, along with the accumulating model ledger. New in-scope Theo catalog documents create native library entries and isolated interactive document pages automatically. Full SQLite snapshots preserve model document and observation revisions. Reviewed official additions deploy through immutable config/ai_model_publication.json batches; new researched model reports use the existing research publication manifest. The separate local Codex daily05:00 heartbeat creates new detailed reports after official-source review and is authorized to commit/push only related Signal Desk model changes. See [scope and controls](AI_MODEL_RESEARCH.md).
