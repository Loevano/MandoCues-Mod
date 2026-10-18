"""Create a portable source-code folder and ZIP without local project metadata."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
CORE = ('build.py', 'score_fixture.py', 'production_score.py', 'score_overview.py',
        'package.py', 'handoff.py', 'browser_support.py', 'README.md', '.gitignore')


def run(script):
    subprocess.run([sys.executable, '-X', 'utf8', str(script)], cwd=script.parent,
                   env=dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1'), check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT.parent / 'MandoCues-overdracht-Jens')
    args = parser.parse_args()
    destination = args.output.resolve()
    archive = destination.with_name(destination.name + '.zip')
    if destination.exists() or archive.exists():
        raise SystemExit(f'Choose a new --output path; the destination or ZIP already exists: {destination}')
    run(ROOT / 'build.py')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='mando-handoff-', dir=destination.parent) as temporary:
        bundle = Path(temporary) / destination.name
        project = bundle / 'prototype'
        project.mkdir(parents=True)
        for name in CORE:
            shutil.copy2(ROOT / name, project / name)
        for check in ROOT.glob('check_*.py'):
            shutil.copy2(check, project / check.name)
        for name in ('src', 'dist', 'handoff'):
            shutil.copytree(ROOT / name, project / name, ignore=shutil.ignore_patterns('__pycache__', '.DS_Store'))
        for doc in (ROOT / 'handoff').iterdir():
            if doc.is_file():
                shutil.copy2(doc, bundle / doc.name)
        run(project / 'check_handoff.py')
        files = {p.relative_to(bundle).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in sorted(bundle.rglob('*')) if p.is_file()}
        (bundle / 'INHOUD.sha256.json').write_text(json.dumps({'format': 1, 'files': files}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        shutil.move(str(bundle), str(destination))
    try:
        with ZipFile(archive, 'w', ZIP_DEFLATED) as zipped:
            for path in sorted(destination.rglob('*')):
                if path.is_file():
                    zipped.write(path, destination.name + '/' + path.relative_to(destination).as_posix())
        with ZipFile(archive) as zipped:
            assert zipped.testzip() is None, 'ZIP integrity check failed'
    except BaseException:
        archive.unlink(missing_ok=True)
        raise
    print(f'Handoff: {destination}')
    print(f'ZIP: {archive} ({archive.stat().st_size:,} bytes; {len(files)+1} files)')


if __name__ == '__main__':
    main()
