# Editorial assets

The user selected **HTML5 UP Editorial** in the HTML Design Helper gallery and
explicitly authorized applying it to the main page and every research report on
2026-10-07. These are actual source assets, not a screenshot imitation.

- `main.css`: unmodified CSS from the official
  [Editorial download](https://html5up.net/editorial/download), retrieved 2026-10-07.
- `LICENSE.txt`: the template's CC BY 3.0 license. The rendered footer credits
  [HTML5 UP Editorial](https://html5up.net/editorial) and links the full notices.
- `fonts.css` and `pretendard-variable.woff2`: the unmodified full Korean/Latin
  variable font from [Pretendard v1.3.9](https://github.com/orioncactus/pretendard/tree/v1.3.9),
  retrieved 2026-10-09. Original path:
  `packages/pretendard/dist/web/variable/woff2/PretendardVariable.woff2`.
  SHA256 `9599f12fd42fc0bce1cd50b47a0c022e108d7aa64dd0d1bb0ed44f3282d900b4`.
  The original SIL OFL 1.1 notice is `pretendard-LICENSE.txt` and is included in
  the existing published license page/CSS notices.
- The six older Open Sans, Roboto Slab and Noto Serif KR subset files/notices
  remain as historical assets. Active CSS no longer declares them. Their Korean
  coverage depended on the 2026-10-07 headings and caused later titles to mix
  Noto Serif KR and Malgun Gothic within the same word.

`editorial.py` removes the vendor CSS's two external imports at rendering time.
Its default review mode embeds fonts/CSS/JavaScript in each standalone HTML.
Production publication uses one local `briefing.css` containing the fonts, with
a content-hash cache version; report history uses a parent-relative stylesheet
link. There are no remote font or script requests. The font notices are included
in the stylesheet; full
template and font licenses are also published at `preview/licenses.html`.

The wrapper/main/inner, header, banner, features, posts, and sidebar structure,
white/gray/coral palette and spacing come from Editorial. Typography now uses one
complete Pretendard family: main headings 700, subheadings/emphasis 600, body 400.
Synthetic bold is disabled. Adaptations
in `housing_watch/editorial.css`, `.js`, and `.html` files add Korean report text,
data tables/charts, native disclosure learning chapters, an accumulating board,
keyboard-accessible SVG menu controls, and historical report navigation. Stock
photos, demo text, Font Awesome and jQuery are not part of the research presentation.

On narrow screens the title precedes the evidence panel and body text is at least
14px. Sidebar categories lead to topic-filtered report lists so future reports
in the same category accumulate without duplicating tree entries.
