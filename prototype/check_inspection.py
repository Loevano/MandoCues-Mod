from browser_support import launch_chromium
"""Check compatibility examples based on the supplied rendered HTML, offline."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parent
errors, external=[],[]
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1100})
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto((ROOT/'dist/index.html').as_uri()+'#bediening')
    expect(page.locator('.source-session-summary')).to_contain_text('Preparation')
    expect(page.locator('.source-cue-plan button')).to_have_count(26)
    expect(page.locator('#main-panel [data-action="record"]')).to_contain_text('Take 3')
    page.locator('#main-panel [data-action="record-overdub"]').click()
    expect(page.locator('.main-panel .rec-status')).to_contain_text('OVERDUB 1')
    field=page.locator('#main-panel [data-draft="c0-od1"]')
    field.fill('Alleen strijkers bij deze overdub')
    expect(page.locator('#main-panel [data-measure-input="c0-od1"]')).to_have_value('')
    field.press('Enter')
    field.fill('Concept voor dezelfde overdub')
    field.press('Meta+Enter')
    expect(field).to_have_value('Concept voor dezelfde overdub')
    expect(page.locator('#main-panel [data-action="record"]')).to_contain_text('Take 3')
    expect(page.locator('#main-panel [data-action="record-overdub"]')).to_contain_text('Overdub 2')
    expect(page.locator('.grouped-list [data-notes-for="c0-od1"]')).to_contain_text('Alleen strijkers')
    expect(page.locator('[data-select-cue="0"]')).to_contain_text('2 takes · 1 overdub')
    page.locator('#main-panel [data-action="record"]').click()
    expect(page.locator('.main-panel .rec-status')).to_contain_text('TAKE 3')
    expect(page.locator('#main-panel [data-draft="c0-t3"]')).to_have_value('')
    page.keyboard.press('Meta+Enter')
    page.locator('[data-variant="B"]').click()
    page.locator('.grouped-list [data-select-take="c0-od1"]').click()
    expect(page.locator('.grouped-list [data-draft="c0-od1"]')).to_have_value('Concept voor dezelfde overdub')
    page.locator('[data-session-cue="15"]').click()
    expect(page.locator('.main-cue')).to_contain_text('Shanghai')
    expect(page.locator('[data-select-cue="15"]')).to_have_attribute('aria-current','true')
    page.locator('[data-session-cue="0"]').click()
    expect(page.locator('#main-panel [data-action="record"]')).to_contain_text('Take 4')
    page.locator('[data-variant="A"]').click()
    page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop=0')
    page.screenshot(path=str(ROOT/'checks/15-bestaand-scherm-context.png'),full_page=True)
    assert not errors,errors
    assert not external,external
    browser.close()
    print('PASS: 26 cues, session context, separate overdub numbering/IDs/drafts and no remote requests')
