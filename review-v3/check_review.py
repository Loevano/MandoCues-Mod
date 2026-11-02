"""Verify the untouched v2 recovery point and deterministic isolated review build."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
repo=ROOT.parent;backup=repo.parent/'Backups/before-session-review-v3-20261102'
manifest=json.loads((backup/'manifest.json').read_text())
assert hashlib.sha256((repo/'prototype/dist/index.html').read_bytes()).hexdigest()==manifest['backup_files']['offline-v2.html']
assert hashlib.sha256((repo.parent/'sites/mando-voorstel-floris/dist/index.html').read_bytes()).hexdigest()==manifest['backup_files']['published-source-v2.html']
for name,digest in manifest['backup_files'].items():assert hashlib.sha256((backup/name).read_bytes()).hexdigest()==digest,name
before=(ROOT/'index.html').read_bytes()
subprocess.run([sys.executable,str(ROOT/'build.py')],check=True)
assert (ROOT/'index.html').read_bytes()==before,'Review output differs from source'
assert subprocess.check_output(['git','rev-list','-n','1','before-session-review-v3-20261102'],cwd=repo,text=True).strip()==manifest['commit']
print('PASS immutable v2 source/hosting copy, backup hashes/tag, and deterministic isolated review build')
