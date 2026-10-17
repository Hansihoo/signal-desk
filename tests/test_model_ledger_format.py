"""Exercise the shipped JS formatter with the table and raw detail-field names."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest


@unittest.skipUnless(shutil.which("node"), "Node.js is required to run the browser formatter")
class ModelLedgerNumberFormatTests(unittest.TestCase):
    def test_official_values_keep_precision_in_table_detail_and_history(self):
        source = (Path(__file__).resolve().parents[1] / "housing_watch/model_ledger.js").read_text(encoding="utf-8")
        # Load the real declarations/formatter without starting the page's DOM code.
        declarations = source[source.index("  const corePrices"):source.index("  const officialColumns")]
        helpers = "\n".join(re.search(r"^  const " + name + r" = .*;$", source, re.M).group(0)
                            for name in ("percent", "costs", "harnessName", "missing"))
        formatter = source[source.index("  function display("):source.index("  function node(")]
        fixture = {"records": [{"source_kind": "reviewed", "fields": {"출력 USD / 이미지": 0.009}}]}
        calls = [
            [0.009, "official:출력 USD / 이미지"], [0.009, "출력 USD / 이미지"],
            [0.757, "official_score"], [0.757, "평가 점수"],
            [0, "출력 USD / 100만 토큰"], [None, "출력 USD / 이미지"],
            [1048576, "context"], [501.3, "parameters"],
        ]
        program = "const data=" + json.dumps(fixture, ensure_ascii=False) + ";\n" + declarations + helpers + formatter
        program += "console.log(JSON.stringify(" + json.dumps(calls, ensure_ascii=False) + ".map(([v,k])=>display(v,k))));"
        result = subprocess.run([shutil.which("node"), "-e", program], capture_output=True, text=True, encoding="utf-8", check=True)
        self.assertEqual(json.loads(result.stdout), ["$0.009", "$0.009", "0.757", "0.757", "$0", "—", "1,048,576", "501.3B"])


if __name__ == "__main__":
    unittest.main()
