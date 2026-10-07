# Homepage and report contract

2026-10-07: The user chose **HTML5 UP Editorial** and explicitly asked to apply it
to each research report and keep new reports accumulating like board posts. The
main and all 11 current reports now use the actual template source. Earlier scope
of only the main and one report is superseded. Collectors, daily source archives
and weekly deep-review scheduling are separate workstreams.

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

Current sources: `housing_watch/editorial_shell.html`, `editorial_home.html`,
`editorial_report.html`, `editorial.css`, `editorial.js`, `editorial.py` and
`briefing_preview.py`. Original CSS/fonts/licenses are in `assets/editorial/`.
Research content is separate in
SQLite and the [versioned JSON contract](RESEARCH_DATA.md), seeded from the authored
`config/research_reports.example.json`. Templates contain no report-specific facts;
chart geometry is computed from numeric rows and threshold. The public exporter generates the pair
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

## Applied Editorial template, 2026-10-07

Explicit user selection and production request authorize the actual Editorial
implementation; this is no longer a direction chooser. Main: subject-led featured
report, evidence table/chart, recent findings by field, searchable accumulating
board, and source-library links. Report: title/topic, outline summary, data,
result, optional collapsed teaching chapters, and references. Scope/evidence dates,
assumptions, numeric geometry, and citations retain the authored data.

The official CSS is stored unmodified. The renderer removes remote imports and
packages licensed fonts; native JavaScript replaces template jQuery menu handling.
SVG replaces Font Awesome, Korean body stays at least 14px, and portrait layouts
put the title before the evidence panel. Stock photography is replaced by actual
source-derived tables/charts; no invented numeric decorations. The footer gives
HTML5 UP credit and links the full licenses and modification notice.

Review mode remains an offline standalone HTML with embedded CSS/JS/fonts. Public
pages share one local cache-versioned stylesheet, keeping report accumulation
small; there is no remote runtime dependency. Both use the same content/template.

| Observed area | Original Editorial | Adapted report/main | Remaining difference |
| --- | --- | --- | --- |
| First screen | Serif title, left copy/right image, coral rule | Same shell/banner and serif title, right factual evidence | Longer Korean titles use 3em desktop / 2em narrow; no decorative photo |
| Body | Underlined section headings, separated posts/features | Same section hierarchy with sourced tables, concise findings and report posts | More text than the demo; visible learning chapters supply depth |
| Navigation | Gray sidebar, menu and search | Gray sidebar, grouped subject tree, report search and history | Native accessible SVG toggle; report categories lead to the board |
| Narrow screen | Single column, sidebar toggle | Title first, evidence below, 14px body, native details | Original portrait image-first order is intentionally changed for reading |

Functional verification and rendered visual comparison are complete; user feedback
on the finished layout remains welcome. This records actual source reuse and screen
comparison, not a claim of pixel identity or that the user already approved every
adapted detail. The earlier rejected custom designs and original template captures
are preserved as comparison references.

## Applied to collected development information, 2026-10-04

Theo's subsequent request asks to collect the desired information and generate
HTML. Ten reviewed subjects now use this format: subject, outline summary, sourced
data, result, references. A graph is used only for a comparable numeric metric;
eligibility, terms, and timelines use semantic tables. Main rows contain the first
two data-owned highlights so measurement period and participation limits remain
visible. Headlines wrap naturally at the viewport rather than splitting content
at an arbitrary word count. Data and presentation stay independent.

The same `/preview/` main links to stable report-ID pages and official references.
The earlier storage report remains addressable. All stored reports are generated;
the manifest controls which reports lead the main. This initial researched collection
does not add the planned weekly deep-review automation. See RESEARCH_DATA.md for
batch persistence and the current verification/evidence limits.

## Expandable explanations, 2026-10-04

Theo requested enough detail to learn unfamiliar subjects, rather than infer their
meaning from compressed headlines. Keep the main concise; include optional
explanatory chapters after the report summary and before the data. The current
ten reports contain 26 chapters; MCP Apps is the deep example with seven.

For subsequent reviewed technical reports:

- Define an unfamiliar concept before using its abbreviation or mechanism.
- Explain the actors and process: who does what, what goes in, and what returns.
- Include a concrete, clearly labelled hypothetical example where it improves
  understanding; never present invented metrics or opportunities as observations.
- Explain how to interpret figures, eligibility or limits, including what they
  cannot establish. Separate official facts from editorial recommendations.
- Cite the official learning material at the relevant block, then offer the
  complete reference. Do not replace original evidence with a generated example.

Use independent native disclosures with meaningful chapter titles and one-sentence
leads; readers can choose the concept they need. Each chapter must contain actual
explanation, not repeat the summary. Plain-text paragraph, process, glossary and
code blocks live in the optional learning data contract. No layout or interface
instruction text belongs in collected content. Old reports can omit learning, and
nontechnical subjects need only the detail that helps interpretation.
