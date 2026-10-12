"""Export the reviewed FDE study report as a portable single HTML file."""

import argparse
import html
import json
import re
from pathlib import Path

from .research_data import load_report_input
from .research_workflow import verify_release
from .study_report import render_study


ROOT = Path(__file__).resolve().parent.parent


def portable_html(report, css):
    fragment = render_study(report)
    # Preserve the DOM element required by the shared reader's initialization.
    # A portable document returns to its own summary instead of a site index.
    fragment, anchors = re.subn(
        r'<a id="document-back"[^>]*>.*?</a>',
        '<a id="document-back" href="#summary">↑ 요약</a>', fragment, count=1)
    fragment, handlers = re.subn(
        r'const canBack = [^\n]+;', 'const canBack = () => false;', fragment, count=1)
    if anchors != 1 or handlers != 1:
        raise ValueError('Portable reader contract changed; inspect navigation before export')
    fragment = fragment.replace("'← 리서치 목록'", "'↑ 요약'")
    fragment = fragment.replace("'리서치 목록으로 이동'", "'요약으로 이동'")
    return ('<!doctype html><html lang="ko" class="study-html"><head>'
            '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><style>%s</style></head><body class="study-page">'
            '<div id="wrapper"><main id="main"><div class="inner">%s'
            '<footer style="padding:30px;text-align:center;font-size:12px">Design: '
            '<a href="https://html5up.net/editorial">HTML5 UP Editorial</a> · '
            '<a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0</a> · adapted'
            '</footer></div></main></div></body></html>') % (html.escape(report['title']), css, fragment)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT/'config/fde_research.2026-10-12.r2.json')
    parser.add_argument('--quality', type=Path, default=ROOT/'config/fde_research.2026-10-12.r2.quality.json')
    parser.add_argument('--output', type=Path, default=ROOT/'reports/fde-study-share.html')
    args = parser.parse_args()
    reports = load_report_input(args.input)
    if len(reports) != 1 or reports[0]['id'] != 'fde-enterprise-adoption':
        raise ValueError('Choose the single reviewed FDE report')
    packages = json.loads(args.quality.read_text(encoding='utf-8-sig'))['packages']
    verify_release(reports, packages)
    css = (ROOT/'site/preview/briefing.css').read_text(encoding='utf-8')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(portable_html(reports[0], css), encoding='utf-8')
    print('Wrote portable FDE document:', args.output)


if __name__ == '__main__':
    main()
