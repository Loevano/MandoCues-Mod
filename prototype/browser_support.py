"""Portable browser setup for the optional Playwright checks."""
from pathlib import Path
import hashlib
import json
import os
import shutil

ROOT = Path(__file__).resolve().parent
(ROOT / 'checks').mkdir(exist_ok=True)


def launch_chromium(playwright):
    """Prefer Playwright's browser; allow an explicit installed Chrome path."""
    override = os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
    if override:
        return playwright.chromium.launch(executable_path=override, headless=True)
    if Path(playwright.chromium.executable_path).exists():
        return playwright.chromium.launch(headless=True)
    candidates = [
        Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
        Path(os.environ.get('PROGRAMFILES', 'C:/Program Files')) / 'Google/Chrome/Application/chrome.exe',
        Path(os.environ.get('LOCALAPPDATA', 'C:/Users/Default/AppData/Local')) / 'Google/Chrome/Application/chrome.exe',
    ]
    for name in ('chromium', 'chromium-browser', 'google-chrome', 'google-chrome-stable'):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))
    for candidate in candidates:
        if candidate.is_file():
            return playwright.chromium.launch(executable_path=str(candidate), headless=True)
    raise RuntimeError('Install the test browser first: python -m playwright install chromium')


def check_original_score_books(root):
    """Check originals when present; the portable package needs only its assets."""
    catalog = json.loads((root / 'src/score-assets/score-catalog.json').read_text(encoding='utf-8'))
    missing = []
    for book in catalog['books']:
        source = root.parent / '06_SCORES' / book['file']
        if not source.is_file():
            missing.append(book['file'])
            continue
        assert hashlib.sha256(source.read_bytes()).hexdigest() == book['sha256'], source
    if missing:
        print(f'SKIP: {len(missing)} original score books are not included; packaged score assets are used.')
