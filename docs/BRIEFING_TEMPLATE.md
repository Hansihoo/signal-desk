# Briefing and representative report preview

2026-10-03: Theo requested only a homepage and one completed representative report before
using them as templates for other areas. This is a two-page preview, not a rollout of
all topics or weekly research automation.

## Deliverables

- [Homepage preview](https://hansihoo.github.io/signal-desk/preview/index.html)
- [Representative report](https://hansihoo.github.io/signal-desk/preview/report.html)

The report covers GitHub Pages' free scope and archive storage strategy. It follows
**title/topic -> outline summary -> visual data -> results -> references**. The chart
distinguishes official limits from calculated scenarios. Ten topics, one report per
week, 52 weeks/year, and one stored copy/report are assumptions, not measured data.
Decimal 50 KB/100 KB/1 MB scenarios produce 260 MB/520 MB/5.2 GB after ten years.
The chart caps bar length at 1 GB and labels the actual amount when it exceeds the cap.
The accompanying table and accessible chart description retain the values.

The existing archive embeds accumulated records in daily snapshots. It does not meet
the single-copy assumption. The report states this and proposes a future archive design;
that optimization is not implemented here. Pages size, monthly bandwidth, Actions
execution, Actions artifact storage, and external service fees are distinct resources.

Official documents reviewed on 2026-10-03:

- [Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)

The homepage leads directly to the report. Other rows use current public source titles
and dates and are explicitly labelled source records, not completed analyses. It does
not re-use generic collected recommendation text as a verified executive summary.
Other topic pages, historical labels, collectors, and the daily schedule remain as-is.

## Editable source and generation

- `housing_watch/briefing_preview_home.html`: homepage layout and editorial lead.
- `housing_watch/briefing_preview_report.html`: the completed report and content order.
- `housing_watch/briefing_preview.css`: shared responsive/print styles.
- `housing_watch/briefing_preview.py`: generation, safe source rows, and chart calculations.
- `housing_watch/public_site.py`: calls the preview builder with the filtered public snapshot.

`python -m housing_watch publish` generates `site/preview/index.html`, `report.html`,
and versioned `briefing.css`. Generated HTML/assets are ignored by Git and deployed
through the existing Pages workflow. The preview uses native HTML links and disclosures,
and does not add accounts, forms, tracking, runtime libraries, or model API calls.

## Template review criteria

Check that the homepage makes the lead report easy to choose; the report summary is
understandable before reading data; chart units and assumptions are visible; results
follow from evidence; and references make official verification easy. Topic-specific
reports may substitute a comparison table or process diagram when quantitative data
would mislead. Expansion to other domains and weekly changed-only publishing remain
next steps after reviewing this pair.

## Verification

51 unit tests and compileall pass. New checks cover scenario units, assumptions and
single-copy limitations, source-title escaping, safe record selection, and encoded links.
Local publish, brief, summary desk generation, review, and briefing image checks pass.
[Initial deployment](https://github.com/Hansihoo/signal-desk/actions/runs/37119399670)
and [final deployment](https://github.com/Hansihoo/signal-desk/actions/runs/37119684353)
succeeded. The live homepage -> report -> official GitHub document/back flow and a
linked existing AI record were checked. The 430px layout has no horizontal overflow;
chart/table labels and keyboard disclosure were inspected. No console errors were
captured. Both preview tabs and final PNG captures remain available for user review.
