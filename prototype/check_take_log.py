"""Keep manual transport wall times separate from notes and DAW timestamps."""
from pathlib import Path
import json
from datetime import datetime
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium

ROOT = Path(__file__).resolve().parent
with sync_playwright() as p:
    browser = launch_chromium(p)
    page = browser.new_page(viewport={'width':1512,'height':1100}, timezone_id='Europe/Amsterdam')
    page.clock.install(time=datetime.fromisoformat("2026-10-19T21:58:58+00:00"))
    page.clock.pause_at(datetime.fromisoformat("2026-10-19T21:59:58+00:00"))  # Near midnight: retain dates, not only HH:mm:ss.
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto((ROOT/'dist/index.html').as_uri())
    page.locator('[data-tour-action="welcome-skip"]').click()
    assert all(t['log'] is None for t in page.evaluate('sessionTakeLog().takes'))
    count = page.evaluate('allTakes(state()).length')
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('allTakes(state()).length') == count
    page.keyboard.press('Meta+Enter')
    log = page.evaluate('({...running(state()).takeLog})')
    assert log['sessionId'] == 'strings-20261020' and log['cueCode'] == '1M02'
    assert log['loggedStartAt'] == page.evaluate('new Date(running(state()).started).toISOString()')
    assert log['timeZone'] == 'Europe/Amsterdam' and log['utcOffsetMinutes'] == 120
    assert log['source'] == 'manual-demo-transport' and log['loggedEndAt'] is None
    page.clock.run_for(5000)
    page.evaluate("state().selected='c0-t1';showProposalView('cutlist')")
    assert page.evaluate('({...running(state()).takeLog})') == log
    page.keyboard.press('Meta+Enter')
    stopped = page.evaluate('state().takes[0].at(-1).takeLog')
    assert stopped['loggedStartAt'] == log['loggedStartAt'] and stopped['id'] == log['id']
    assert stopped['loggedEndAt'] > stopped['loggedStartAt']
    assert page.evaluate('new Date(state().takes[0].at(-1).started).getDate() !== new Date(state().takes[0].at(-1).takeLog.loggedEndAt).getDate()'), (log, stopped)
    assert page.evaluate('state().takes[0].at(-1).duration') == 5
    page.evaluate("state().takes[0].at(-1).notes.push({id:'test',text:'Note later corrected',measure:8,clockAt:Date.now()+60000});showProposalView('recording')")
    assert page.evaluate('state().takes[0].at(-1).takeLog') == stopped
    page.clock.run_for(3000)
    assert page.evaluate('state().takes[0].at(-1).takeLog') == stopped
    page.locator('.session-pdf-menu summary').click()
    page.locator('[data-app-export="takes"]').click()
    expect(page.locator('.session-export-preview')).to_contain_text('11:59:58 PM')
    expect(page.locator('.session-export-preview')).to_contain_text('Recording time not logged (example take)')
    with page.expect_download() as download:
        page.locator('[data-app-action="download-take-log"]').click()
    data = json.loads(Path(download.value.path()).read_text())
    assert data['format'] == 'mandocues-take-log-v1' and data['demo'] is True
    entry = next(t for t in data['takes'] if t['log'] and t['log']['id'] == log['id'])
    assert entry['log'] == stopped and entry['durationSeconds'] == 5
    assert entry['notes'][0]['bar'] == 8 and entry['notes'][0]['clockAt'].endswith('Z')
    page.locator('.app-dialog [data-app-dialog-close]').first.click()
    page.evaluate("switchProposalSession('strings-demo-day2')")
    page.keyboard.press('Meta+Enter'); page.keyboard.press('Meta+Enter')
    other = page.evaluate('running(state()).takeLog')
    assert other['sessionId'] != log['sessionId'] and other['id'] != log['id']
    page.keyboard.press('Meta+Enter')
    page.evaluate("switchProposalSession('strings-20261020')")
    assert page.evaluate('state().takes[0].at(-1).takeLog') == stopped
    page.evaluate('openAddSessionCues()')
    page.locator('[data-add-session-cue="1M04"]').check()
    page.locator('[data-app-action="confirm-cues"]').click()
    page.evaluate('selectCue(state(),cues.length-1)')
    page.keyboard.press('Meta+Enter'); page.keyboard.press('Meta+Enter')
    assert page.evaluate('sessionTakeLog().takes.at(-1).cueCode') == '1M04'
    assert not errors, errors
    browser.close()
print('PASS: explicit manual start/stop dates, no invented example times, independent notes/selection, JSON download and isolated session IDs')
