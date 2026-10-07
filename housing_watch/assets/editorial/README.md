# Editorial assets

The user selected **HTML5 UP Editorial** in the HTML Design Helper gallery and
explicitly authorized applying it to the main page and every research report on
2026-10-07. These are actual source assets, not a screenshot imitation.

- `main.css`: unmodified CSS from the official
  [Editorial download](https://html5up.net/editorial/download), retrieved 2026-10-07.
- `LICENSE.txt`: the template's CC BY 3.0 license. The rendered footer credits
  [HTML5 UP Editorial](https://html5up.net/editorial) and links the full notices.
- `fonts.css` and six `.woff2` files: official Google Fonts text subsets of Open
  Sans 400/700, Roboto Slab 400/700, and Noto Serif KR 400/700. Latin characters and
  the existing Korean report headings were requested through the Google Fonts CSS2
  API. Korean glyphs outside the subset use the declared local serif fallback.
- Font notices: original Google Fonts `ofl/opensans/OFL.txt`,
  `apache/robotoslab/LICENSE.txt`, and `ofl/notoserifkr/OFL.txt` from
  [google/fonts](https://github.com/google/fonts). Font binaries are unchanged.

`editorial.py` removes the vendor CSS's two external imports at rendering time.
Its default review mode embeds fonts/CSS/JavaScript in each standalone HTML.
Production publication uses one local `briefing.css` containing the fonts, with
a content-hash cache version; report history uses a parent-relative stylesheet
link. There are no remote font or script requests. The font notices are included
in the stylesheet; full
template and font licenses are also published at `preview/licenses.html`.

The wrapper/main/inner, header, banner, features, posts, and sidebar structure,
white/gray/coral palette, spacing and Latin fonts come from Editorial. Adaptations
in `housing_watch/editorial.css`, `.js`, and `.html` files add Korean report text,
data tables/charts, native disclosure learning chapters, an accumulating board,
keyboard-accessible SVG menu controls, and historical report navigation. Stock
photos, demo text, Font Awesome and jQuery are not part of the research presentation.

On narrow screens the title precedes the evidence panel and body text is at least
14px. Sidebar categories lead to topic-filtered report lists so future reports
in the same category accumulate without duplicating tree entries.
