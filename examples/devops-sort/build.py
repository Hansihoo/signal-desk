import argparse
import hashlib
from pathlib import Path
import re
import shutil
import tempfile
import zipapp

parser = argparse.ArgumentParser()
parser.add_argument('version')
parser.add_argument('--output', default='dist')
args = parser.parse_args()
if not re.fullmatch(r'[A-Za-z0-9_-]+', args.version):
    parser.error('version must use letters, numbers, underscores or hyphens')
output = Path(args.output)
output.mkdir(parents=True, exist_ok=True)
artifact = output / (args.version + '.pyz')
if artifact.exists():
    parser.error('version already exists; choose a new version')
with tempfile.TemporaryDirectory() as staging:
    staging = Path(staging)
    for name in ['app.py', 'sorting.py']:
        shutil.copyfile(Path(__file__).parent / 'src' / name, staging / name)
    (staging / 'version.py').write_text('VERSION = {!r}\n'.format(args.version), encoding='utf-8')
    zipapp.create_archive(staging, artifact, main='app:main')
sha = hashlib.sha256(artifact.read_bytes()).hexdigest()
artifact.with_suffix('.sha256').write_text(sha + '\n', encoding='utf-8')
print('{} SHA256={}'.format(artifact, sha))
