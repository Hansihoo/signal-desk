"""Apply immutable reviewed model fact batches on both local and cloud builds."""

import hashlib
import json
import re
from pathlib import Path

from .model_ledger import import_reviewed_models
from .timeutil import iso_utc


MANIFEST = Path(__file__).resolve().parent.parent / 'config/ai_model_publication.json'


def apply_model_publication(conn, manifest_path=MANIFEST):
    path = Path(manifest_path)
    document = json.loads(path.read_text(encoding='utf-8'))
    if document.get('schema_version') != 1 or not isinstance(document.get('batches'), list):
        raise ValueError('Model publication requires schema_version=1 and batches')
    conn.execute('CREATE TABLE IF NOT EXISTS model_import_batches (id TEXT PRIMARY KEY, content_hash TEXT NOT NULL, applied_at TEXT NOT NULL)')
    prepared, seen = [], set()
    for batch in document['batches']:
        name, filename = batch.get('id',''), batch.get('path','')
        if not re.fullmatch(r'[a-z0-9][a-z0-9._-]{0,95}',name) or name in seen or not re.fullmatch(r'[A-Za-z0-9._-]+\.json',filename):
            raise ValueError('Invalid model publication batch')
        seen.add(name)
        source = path.parent / filename
        facts = json.loads(source.read_text(encoding='utf-8'))
        digest = hashlib.sha256(json.dumps(facts,ensure_ascii=False,sort_keys=True,allow_nan=False).encode()).hexdigest()
        old = conn.execute('SELECT content_hash FROM model_import_batches WHERE id=?',(name,)).fetchone()
        if old and old['content_hash'] != digest:
            raise ValueError('Reviewed model batch changed; add a new immutable batch: '+name)
        prepared.append((name,digest,facts,bool(old)))
    for name,digest,facts,applied in prepared:
        if applied:
            continue
        import_reviewed_models(conn,facts)
        with conn:
            conn.execute('INSERT INTO model_import_batches VALUES (?,?,?)',(name,digest,iso_utc()))
