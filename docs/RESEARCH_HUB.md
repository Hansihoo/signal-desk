# Multi-topic research library

The public product is a main research library containing many independent topics.
AI, housing, and weekly news are initial topics, not the fixed scope of the site.
It is a static reading site: no accounts, user submissions, analytics SDKs, or application server.
GitHub itself logs visitor IP addresses for security; do not promise that the host records nothing.

## Main and topic pages

- `/index.html`: topic directory, all-topic search, recent updates, and daily archive.
- `/research/<topic-id>/index.html`: one topic's records, keyword search, and optional detail briefing.
- `/research/<topic-id>/index.html?section=<category>`: one subtopic's records.
- `/research/<topic-id>/index.html?section=<category>&report=<record-id>`: an individually addressable source-note document.
- `/topics.json`: public topic metadata, record counts, and latest source publication date.
- `/archive/YYYY-MM-DD/index.html`: the first saved briefing for that date.

The homepage initially shows all topics. Source publication date can be older than fetch time;
counts reflect stored records, not independently verified research reports.
Topic pages initially show their entire accumulated library and only their own source health.

## Report and tree scaffold

The reading structure is main -> topic -> subtopic -> individual record. Desktop uses
a left navigation outline and a right document. Mobile starts with a collapsed outline.
Native details/summary controls remain usable with a keyboard; report links include the
original source, publication date, basis, and first collection time.

Existing record categories supply the initial subtopics. The outline previews four recent
records per category and links to the complete list; a selected older record stays visible.
On a topic page, other topic branches provide overview links; their records load on navigation to that topic page.

Individual documents have summary, evidence, review, and conclusion sections. Current
data supplies source excerpts and metadata only. Review and conclusion are explicitly
marked pending; this HTML scaffold does not claim independently researched analysis.

Edit `housing_watch/public_site.html` for structure, `public_site.css` for shared visual
tokens/layout, and `public_site.js` for navigation and rendering. Publish copies the two
assets into `site/`; content hashes in their URLs prevent stale style/script caches.
All inserted source text uses DOM text nodes. Public links permit only HTTP(S) URLs
without embedded credentials.

Archived documents use query routes within the original dated page, including topic,
section, and report IDs. Their outline and report bodies are built solely from that
saved snapshot. Updating the shared HTML layout never changes the archived JSON.
The collection schedule, SQLite model, and daily snapshot format are unchanged by this UI phase.

## Add a research topic

Edit `config/research_topics.json`. Stable lowercase IDs become permanent page paths.
Each topic has a name, description, collector, and optional collection limit.
Built-in collectors are `ai`, `housing`, and `news`; each may belong to one topic.
`planned` topics add a clearly labelled HTML outline while skipping collection. The
Developer Opportunities outline is configured in `config/opportunity_outline.json`;
its source candidates and fields do not become public library records.
The `rss` collector supports additional independent topics with public RSS/Atom feeds.

Example entry (replace the placeholder URL with a verified feed):

```json
{
  "id": "papers",
  "name": "논문",
  "description": "관심 분야의 공개 논문과 원문 자료를 모읍니다.",
  "collector": "rss",
  "limit": 40,
  "feeds": [
    {"id": "journal", "name": "학술지", "url": "https://example.org/research/rss.xml"}
  ]
}
```

Commit and push the registry change to main; the existing workflow collects and publishes
the new topic automatically. No live feed was added merely to demonstrate this feature.
Use `python -m housing_watch publish --topics <registry.json> --collect` for a selected registry.
Arbitrary websites, paid databases, and PDF sources still need their own verified adapters.

## Storage and evidence rules

Normalized records remain in SQLite. Generic feeds keep source excerpts and URLs without
AI developer recommendations or claims of independent verification. Raw XML is retained
under `data/raw/research/<topic-id>/`. Duplicate titles are reconciled within a collection
domain, so identical titles in different research topics do not erase each other.

Daily JSON snapshots preserve their original topic names and records. Older snapshots
without topic metadata are rendered using their saved labels without rewriting the JSON.
Removing a topic from the current registry hides its current public export; the stored
database and archived snapshots remain. Keep topic IDs stable to preserve links.

## Free hosting envelope

Checked against GitHub documentation on 2026-10-03:

| Resource | Current documented boundary |
| --- | --- |
| GitHub Free Pages | Public repositories; published site at most 1 GB. |
| Pages bandwidth | Soft limit of 100 GB per month. This measures transferred bytes, not user count. |
| Public Actions | Standard GitHub-hosted runners are free; larger runners are charged. |
| Private Actions | GitHub Free includes 2,000 minutes/month and 500 MB artifact storage; free Pages requires a public repo. |
| Release snapshots | Each asset under 2 GiB; up to 1,000 assets per release. Not part of the published Pages site. |
| Other services | AI API calls, paid data, and a purchased custom domain have separate costs. |

There is no free-tier quota on the number of topic subpages. All topics share the site's
size and bandwidth envelope. Text and source links are inexpensive; PDFs, images, complete
daily library copies, and raw snapshots can grow rapidly. Revisit archive packaging and
storage before reaching the site limit. Current design avoids adding a paid AI API.

GitHub Pages also restricts commercial transaction/SaaS hosting. A public informational
library fits the intended static publishing shape; selling subscriptions would require
a separate hosting decision.

## Verification

On 2026-10-03, 45 unit tests passed including RSS/Atom collection, cross-topic title
preservation, unsafe registry rejection, archive immutability, and topic-specific health.
[Hub deployment](https://github.com/Hansihoo/signal-desk/actions/runs/37113326705)
and [final refresh](https://github.com/Hansihoo/signal-desk/actions/runs/37113583835)
both restored state and deployed successfully. Public records accumulated to 230 while
the original daily briefing retained its 165 records and 12:27:29 KST timestamp.
All three topic routes, keyword search, historical filtering, and 430px mobile layout
were checked in the live browser. Brief/desk images and `review` were checked locally.

The report/tree scaffold deployed successfully in
[run 37115050077](https://github.com/Hansihoo/signal-desk/actions/runs/37115050077).
46 unit tests, JS syntax, compileall, publish/brief/desk/review, and briefing image checks
passed. The live main -> AI topic -> LLM category -> individual document path, original
source link, document contents anchors, and archived report routes were checked.
430px mobile outline toggling, Enter-key control, search/topic filtering, and lack of
horizontal overflow were verified. No browser console errors were captured.
Live records reached 245; the original cloud archive stayed at 165 records and
12:27:29 KST. Local archive HTML separately matched its own original saved JSON.

Sources: [Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits),
[Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions),
[Release quotas](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases),
[Pages IP logging](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).
