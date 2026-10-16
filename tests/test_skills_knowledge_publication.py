"""Publication must validate frozen review inputs without a local catalog or DB."""

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from housing_watch.research_workflow import quality_issues, verify_release

ROOT = Path(__file__).resolve().parents[1]


class SkillsKnowledgePublicationTests(unittest.TestCase):
    def package(self, suffix=""):
        name = "skills_knowledge_research.2026-10-16" + suffix
        return json.loads((ROOT / "config" / (name + ".quality.json")).read_text(encoding="utf-8"))["packages"][0]

    def test_both_editions_verify_without_loading_live_authoring_sources(self):
        with patch("housing_watch.authoring.compose", side_effect=AssertionError("Publication must use frozen instructions")):
            for suffix in ("", ".r2"):
                package = self.package(suffix)
                self.assertEqual(quality_issues(package), [])
                verify_release([package["draft"]["report"]], [package])

    def test_changed_instruction_snapshot_is_rejected(self):
        package = copy.deepcopy(self.package(".r2"))
        package["authoring"]["recipe"]["components"][0]["sources"][0]["text"] += " Changed"
        self.assertIn("authoring_binding", {issue["code"] for issue in quality_issues(package)})

    def test_review_cannot_be_reused_after_removing_selected_instructions(self):
        package = copy.deepcopy(self.package(".r2"))
        del package["authoring"]
        self.assertIn("stale_review", {issue["code"] for issue in quality_issues(package)})
