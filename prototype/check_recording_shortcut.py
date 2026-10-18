"""Cmd+Enter works from the first tour focus, then from text editors and both views."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium

ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1100})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri())
    count=page.evaluate('allTakes(state()).length')
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('!state().sessionStarted&&!running(state())')
    page.locator('[data-tour-action="welcome-start"]').click()
    page.evaluate("openTourStep(proposalTourSteps.findIndex(step=>step.id==='opnametoets'))")
    expect(page.locator('#proposal-tour-title')).to_be_focused()
    expect(page.locator('#main-panel .record')).to_contain_text('Start session')
    # No click in the workspace before the first session/take shortcut.
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('state().sessionStarted&&!running(state())')
    assert page.evaluate('allTakes(state()).length')==count
    expect(page.locator('#main-panel .record')).to_contain_text('Record 1M02')
    page.keyboard.press('Meta+Enter')
    live=page.evaluate('running(state()).id')
    assert page.evaluate('allTakes(state()).length')==count+1
    expect(page.locator('#main-panel .record')).to_contain_text('Stop take')
    # Holding the keys or IME composition cannot toggle again.
    for option in ['repeat:true','isComposing:true']:
        page.evaluate('document.activeElement.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",metaKey:true,bubbles:true,cancelable:true,'+option+'}))')
        assert page.evaluate('running(state()).id')==live
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('!running(state())')
    page.keyboard.press('Escape')
    field=page.locator(f'[data-draft="{live}"]')
    field.fill('Keep this draft')
    field.press('Space')
    expect(field).to_have_value('Keep this draft ')
    field.press('Meta+Enter')
    newer=page.evaluate('running(state()).id')
    assert newer!=live
    expect(page.locator(f'[data-draft="{newer}"]')).to_have_value('')
    field=page.locator(f'[data-draft="{newer}"]')
    field.fill('Notes with spaces')
    field.press('Shift+Enter')
    expect(field).to_have_value('Notes with spaces\n')
    field.press('Enter')
    assert page.evaluate('running(state()).id')==newer
    expect(page.locator('.calm-notes .note-list')).to_contain_text('Notes with spaces')
    field.fill('Unsent draft survives stopping')
    field.press('Meta+Enter')
    assert page.evaluate('!running(state())')
    expect(field).to_have_value('Unsent draft survives stopping')
    page.locator('[data-proposal-view="cutlist"]').click()
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('!!running(state())')
    page.locator('[data-proposal-action="prompt"]').click()
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('!!running(state())')
    page.locator('#proposal-prompt [data-tour-action="close-dialog"]').click()
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('!running(state())')
    # Reload restores the same initial Start session keyboard/mouse flow.
    page.reload();page.locator('[data-tour-action="welcome-skip"]').click()
    page.locator('[data-proposal-view="recording"]').click()
    expect(page.locator('#main-panel .record')).to_contain_text('Start session')
    page.locator('#main-panel .record').click()
    assert page.evaluate('state().sessionStarted&&!running(state())')
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('!!running(state())')
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('!running(state())')
    assert not errors,errors
    browser.close()
print('PASS: session start, immediate tour shortcut, take start/stop, repeat/IME guards, text entry, drafts, both views and modal isolation')
