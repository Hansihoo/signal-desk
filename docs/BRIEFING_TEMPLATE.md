# Homepage and report contract

2026-10-03: Only the homepage and one report are in scope. Other topic layouts,
collectors, daily archive format, and weekly review automation remain unchanged.

- [Homepage](https://hansihoo.github.io/signal-desk/preview/index.html)
- [Report](https://hansihoo.github.io/signal-desk/preview/report.html)

## Reader-facing editorial revision

Theo rejected the first pair because it described a prototype and its navigation
instead of presenting a finished publication. The revised pages remove prototype
badges, reading instructions, template demonstrations, review-status captions,
software-style sidebars, and large action buttons.

The publication name is Signal Desk. The lead headline is the concrete finding:
“무료 보관, 파일 크기가 누적 용량을 가른다”. Clicking the headline opens the report.
The homepage provides three outline bullets and existing topic-source titles/dates.
Collected titles are source records, not newly researched conclusions; generic
collected recommendations are not reused. Empty fields never invent analysis.

The report follows the requested order: **title/topic -> outline summary -> visual
data -> results -> references**. Copy uses brief factual or interpretive statements.
Navigation consists of topics, contents, and a return link. Main/report mobile body copy stays at 14px. Essential scope, date,
assumptions, and citations stay visible; implementation status belongs in these docs.

## Published outputs examined

Reviewed the actual editions on 2026-10-03, rather than relying on product guides:

- [Stanford HAI, Inside the AI Index: 12 Takeaways from the 2026 Report](https://hai.stanford.edu/news/inside-the-ai-index-12-takeaways-from-the-2026-report), published April 13, 2026. Topic-specific takeaway headings, dated publication, numerical evidence and associated charts. Article and browser layout inspected.
- [Thoughtworks Technology Radar, Volume 34, April 2026](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2026/04/tr_technology_radar_vol_34_en_1.pdf). Themed analysis on printed pp. 8–10 and named classifications on pp. 12–13. PDF text examined. Used its separation of analysis and evidence; no copied artwork or branding.

Our editorial choices: subject-led titles, short outline summaries, a chart with a
specific metric title, and conclusions supported by cited evidence. These are design
judgments extracted from the publications, not a claim that all reports use one layout.

## Report evidence and assumptions

Official GitHub documentation checked on 2026-10-03:

- [Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)

Ten topics, one report/topic/week, 52 weeks/year, and one stored copy/report are
assumptions. Decimal 50 KB/100 KB/1 MB scenarios produce 260 MB/520 MB/5.2 GB in
ten years. These are not measurements or a guaranteed site lifetime. The chart now
uses the same uncapped 0–5.2 GB scale for every bar, with the approximate 1 GB Pages
limit marked at 19.23%. The labels identify assumed sizes rather than pretending
that a particular content format always has a known size.

Attachments, common files, and repeated cumulative snapshots are excluded. The
existing daily archive repeats accumulated records; the expandable calculation note
states this. Proposed storage changes are not implemented. Pages size, bandwidth,
Actions execution/storage, and paid external services are distinct resources.

## Generation and verification

Sources: `housing_watch/briefing_preview_home.html`, `briefing_preview_report.html`,
`briefing_preview.css`, `briefing_preview.py`. The public exporter generates the pair
under ignored `site/preview/`. No new runtime dependency, account, form, or tracker.

51 tests, compileall, publish, brief, summary desk, and review pass. Existing briefing
and desk images inspected. 40 local links/assets/anchors pass. [Initial reader revision deployment](https://github.com/Hansihoo/signal-desk/actions/runs/37124680126) and [final deployment](https://github.com/Hansihoo/signal-desk/actions/runs/37125006248) succeeded. Final source commit cc80637; both pages load CSS hash 48b427a85c86.

Public main -> report -> official Pages document/back and an existing AI record were
opened successfully. Desktop and 390/430px layouts inspected; no horizontal overflow.
The final narrow-screen body uses 14px type. Native calculation disclosure works with
the keyboard. No console errors observed. Temporary viewport overrides were reset.
Both publication tabs are retained. Final home/report screenshots are preserved under
the registered thread verification root; earlier captures remain retained.

Expand this format only after Theo reviews the pair. Weekly changed-only review
requires separate collection/editing work; it is not part of this revision.
