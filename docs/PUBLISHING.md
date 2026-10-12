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

Recovery completed: source422d896 deployed in
[run37805827869](https://github.com/Hansihoo/signal-desk/actions/runs/37805827869),
created16:03:51Z and completed16:05:42Z on2026-10-08 (01:03–01:05 KST on2026-10-09).
CI tests, housing briefing/review, save and deployment succeeded. HTTP checks at
16:06:59Z confirmed the live main/new MCP/previous MCP-r4/data/CSS routes return200.
MCP revision5 exactly matches the reviewed input; other19 current documents and
all prior52 editions retain their hashes,53 editions total. CSS matches local output,
the empty data section/navigation is hidden, and teaching/citation anchors resolve.
Actual rendering/interactions were verified locally at1280/390/320px; public-browser
interaction was not retested because the in-app bridge was unavailable. Existing
workflow configuration and credentials were preserved.

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

On2026-10-12, the user requested publication of Home and the corrected DevOps r6.
Source `b031c7d` deployed through [Pages38187510657](https://github.com/Hansihoo/signal-desk/actions/runs/38187510657)
in2m18s. CI142tests/housing review pass. Public44reports/145editions preserve the
other43 reports/all144prior editions/model804+806/14original pages exactly. New/old
image hashes and shared CSS match local output; live Home shows six updates and
the corrected document is visibly open in Chrome. Collection warning1 remains
separate from deployment success. [Publication receipts](DEVOPS_DIAGRAM_REPAIR.2026-10-12.md).

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

## 2026-10-11 reviewed model addition

Source7b497f3 and [Pages38084103110](https://github.com/Hansihoo/signal-desk/actions/runs/38084103110)
published Qwen-Image-2.1-Turbo and5 official comparison observations. CI138tests and
housing review passed. Public43reports/142editions,802observations/804revisions,
Theo14documents and18model-library pages verified. Eight routes,12preservation
checks and22actual browser checks passed; inspected PNGs retained outside Git.
The Qwen ID explicitly uses existing model-guide Editorial while the general study
default is preserved. [Evidence, limits and failed-check history](AI_MODEL_REVIEW.2026-10-11.md).

## 2026-10-12 reviewed decision-model addition

Source78ce32c and [Pages38172786459](https://github.com/Hansihoo/signal-desk/actions/runs/38172786459)
published Microsoft-Decision-1 and2 official specification/pricing observations.
CI139tests and housing review passed. Public44reports/144editions,804observations/
806revisions,Theo14documents and19model-library pages verified. Eight HTTP200
routes,13preservation checks and22browser checks passed; inspected PNGs retained
outside Git. Earlier Python connection failure and one original iframe mobile filter
timeout remain recorded separately; subsequent PC5source filters passed.
[Actual evidence and limits](AI_MODEL_REVIEW.2026-10-12.md).


## 2026-10-12 revised DevOps publication

User-requested sourcef35cde2/[Pages38191602612](https://github.com/Hansihoo/signal-desk/actions/runs/38191602612)
published the reviewed DevOps r9 and preserved r7/r8 history. Completed10:24:29KST,
workflow2m31s/job2m26s; CI143tests28.883s and housing review pass. Public44/150,
other43/all147previous editions and update times/model804+806/14originals+14history
exact. Three inline image hashes match. Actual Chrome opens the changed9chapter
outline and shared-goal heading; requested tab kept. Weekly-news warning1 remains
separate from deployment success, and illustrative remoteCI/CD/human learning trial
remain unperformed. [Content and publication receipts](DEVOPS_HEADING_REVIEW.2026-10-12.md).

## 2026-10-12 DevOps r14 배포 완료

소스1d17b18/[Pages38214660351](https://github.com/Hansihoo/signal-desk/actions/runs/38214660351)
success15:54:40KST. 공개r14 원고/4장12목차/CI-CD표/전달과 복구2도식/실습9파일이 반영됐다.
45문서/157판, 다른44현재/기존152판/모델804+806/원본14+14 정확히 보존.
로컬152시험/제출tree품질-발행-brief-review/CI152시험39.788s와 cloud review 통과.
Home/원고/ZIP/r1-r13 HTTP 및 anchor, Chrome1864px 표/전달 PNG/복구3단계와 목차 이동 확인.
ZIP 생성OS 메타데이터는 플랫폼별로 다르나9파일 내용은 정확히 같음.
모바일은 기존 로컬 DOM 범위, 예제 원격CI/운영 서버/사람 학습 시험은 미수행.
FDE 기존 배포와 작업 파일, 원문/내용 검토 날짜를 보존. 생성 출력/workflow/권한 변경 없음.
자세한 결과와 증거: docs/DEVOPS_PUBLICATION.2026-10-12.md.
