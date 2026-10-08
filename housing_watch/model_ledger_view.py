"""Native, offline-capable model research explorer in the Editorial shell."""

import json
from pathlib import Path


ROOT = Path(__file__).parent


def model_ledger_content(ledger, candidates=None, source_prefix="../"):
    data = dict(ledger, candidates=candidates or [], source_prefix=source_prefix)
    serialized = json.dumps(data, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = (ROOT / "model_ledger.html").read_text(encoding="utf-8")
    return template.replace("__MODEL_DATA__", serialized).replace("__MODEL_STYLE__", (ROOT / "model_ledger.css").read_text(encoding="utf-8")).replace("__MODEL_SCRIPT__", (ROOT / "model_ledger.js").read_text(encoding="utf-8"))
