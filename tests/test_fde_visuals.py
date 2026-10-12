import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from housing_watch.study_report import render_study, visuals_for
from housing_watch.study_visual import reviewed_asset

ROOT = Path(__file__).resolve().parent.parent


class FdeVisualTests(unittest.TestCase):
    def test_both_editions_render_without_raster_files(self):
        for filename in ('fde_research.2026-10-12.json', 'fde_research.2026-10-12.r2.json'):
            report = json.loads((ROOT/'config'/filename).read_text(encoding='utf-8'))['reports'][0]
            guide = visuals_for(report)
            self.assertTrue(all(v['asset'].endswith('.svg') for v in guide['images'].values()))
            rendered = render_study(report)
            self.assertEqual(rendered.count('data:image/svg+xml;base64,'), 5)
            self.assertNotIn('class="learning-kind"', rendered)
            self.assertIn('href="#ref-1"', rendered)
            self.assertIn('O1001', rendered)

    def test_svg_hash_and_static_graphics_contract(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'diagram.svg'
            original = b'<svg xmlns="http://www.w3.org/2000/svg"><rect width="10" height="10"/></svg>'
            path.write_bytes(original)
            visual = {'asset':path.name,'sha256':hashlib.sha256(original).hexdigest()}
            self.assertEqual(reviewed_asset(visual, folder), ('image/svg+xml', original))
            path.write_bytes(original+b' ')
            with self.assertRaisesRegex(ValueError, 'reviewed bytes'):
                reviewed_asset(visual, folder)
            for node in (b'<script>alert(1)</script>', b'<image href="https://example.com/external.png"/>'):
                data = b'<svg xmlns="http://www.w3.org/2000/svg">'+node+b'</svg>'
                path.write_bytes(data)
                visual['sha256'] = hashlib.sha256(data).hexdigest()
                with self.assertRaisesRegex(ValueError, 'static graphics'):
                    reviewed_asset(visual, folder)

    def test_existing_png_compatibility(self):
        guide = json.loads((ROOT/'config/devops_visuals.2026-10-10.r4.json').read_text(encoding='utf-8'))
        mime, data = reviewed_asset(guide['images']['summary'], ROOT/'housing_watch/assets/editorial')
        self.assertEqual(mime, 'image/png')
        self.assertTrue(data.startswith(b'\x89PNG\r\n\x1a\n'))
