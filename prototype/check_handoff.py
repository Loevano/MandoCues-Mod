"""Check a portable package and rebuild it in isolation; Python stdlib only."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
BUILD_FILES = ('build.py', 'score_fixture.py', 'production_score.py', 'score_overview.py')


def verify_integrity():
    manifest = ROOT.parent / 'INHOUD.sha256.json'
    if not manifest.is_file():
        raise SystemExit('No package manifest here. Omit --integrity when checking the working source.')
    entries = json.loads(manifest.read_text(encoding='utf-8'))['files']
    for name, digest in entries.items():
        path = ROOT.parent / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise SystemExit(f'Package file missing or changed: {name}')
    print(f'PASS: {len(entries)} package files match their delivery checksums.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity', action='store_true', help='Also verify the original delivery checksums (before editing).')
    args = parser.parse_args()
    if args.integrity:
        verify_integrity()
    with tempfile.TemporaryDirectory(prefix='MandoCues portable check ') as directory:
        isolated = Path(directory) / 'prototype'
        isolated.mkdir()
        for name in BUILD_FILES:
            shutil.copy2(ROOT / name, isolated / name)
        shutil.copytree(ROOT / 'src', isolated / 'src', ignore=shutil.ignore_patterns('__pycache__', '.DS_Store'))
        env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
        result = subprocess.run([sys.executable, '-X', 'utf8', str(isolated / 'build.py')], cwd=isolated, env=env, capture_output=True, text=True, encoding='utf-8')
        if result.returncode:
            raise SystemExit(result.stdout + result.stderr)
        generated = {p.name: p for p in (isolated / 'dist').iterdir() if p.is_file()}
        delivered = {p.name: p for p in (ROOT / 'dist').iterdir() if p.is_file() and p.name != '.DS_Store'}
        if generated.keys() != delivered.keys():
            raise SystemExit(f'Dist differs from source. Run build.py first. Missing: {sorted(generated.keys()-delivered.keys())}; extra: {sorted(delivered.keys()-generated.keys())}')
        for name, path in generated.items():
            if path.read_bytes() != delivered[name].read_bytes():
                raise SystemExit(f'Dist differs from source: {name}. Run build.py first.')
        entrypoint=ROOT.parent / 'index.html'
        if entrypoint.exists() and entrypoint.read_bytes() != (isolated.parent / 'index.html').read_bytes():
            raise SystemExit('Root entrypoint differs from source. Run build.py first.')
        print(f'PASS: clean isolated rebuild matches all {len(generated)} dist files byte for byte.')
        print('PASS: no original score books, external project, browser or third-party Python packages needed for the build.')


if __name__ == '__main__':
    main()
