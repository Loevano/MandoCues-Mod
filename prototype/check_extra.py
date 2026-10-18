from browser_support import launch_chromium
"""Exercise the additional proposals through the offline UI, without DAW or network access."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'checks'
URL=(ROOT/'dist/index.html').as_uri()
errors=[]
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1100})
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(URL+'#cue-take')
    page.locator('[data-take-alt="c0-t3"]').click()
    page.locator('[data-rating-filter]').select_option('5')
    expect(page.locator('#details-0 .take-block')).to_have_count(1)
    expect(page.locator('[data-take-alt="c0-t3"]')).to_have_attribute('aria-pressed','true')
    page.locator('[data-rating-filter]').select_option('0')
    expect(page.locator('#details-0 .take-block')).to_have_count(3)
    page.locator('[data-take-best="c0-t1"]').click()
    expect(page.locator('[data-take-best="c0-t3"]')).to_have_attribute('aria-pressed','false')
    page.locator('[data-take-best="c0-t1"]').click()
    expect(page.locator('#details-0 .best[aria-pressed="true"]')).to_have_count(0)

    page.goto(URL+'#notities')
    field=page.locator('#details-0 [data-draft="c0-t2"]')
    field.fill('Eigen aanvulling')
    page.locator('#details-0 [data-composer="c0-t2"] .quick-note-suggestions summary').click()
    page.locator('#details-0 [data-quick-note="More expressive"][data-take="c0-t2"]').click()
    expect(field).to_have_value('Eigen aanvulling · More expressive')
    expect(field).to_be_focused()
    field.press('Enter')
    expect(page.locator('#details-0 [data-notes-for="c0-t2"] .note-card').last).to_contain_text('Eigen aanvulling · More expressive')
    expect(page.locator('#details-0 [data-notes-for="c0-t1"] .note-card')).to_have_count(1)

    page.goto(URL+'#bediening')
    page.evaluate('state().controlsPrevious=true;renderDemo()')
    page.locator('.control-comparison').click()
    page.keyboard.press('Alt+8')
    expect(page.locator('.main-cue')).to_contain_text('1M17')
    page.keyboard.press('BracketRight')
    expect(page.locator('.main-cue')).to_contain_text('1M10')
    page.keyboard.press('BracketLeft')
    expect(page.locator('.main-cue')).to_contain_text('1M17')
    page.keyboard.press('Alt+1')
    field=page.locator('#main-panel [data-draft="c0-t2"]')
    field.fill('[ ]')
    expect(page.locator('.main-cue')).to_contain_text('1M02')
    page.locator('#main-panel [data-action="record"]').click()
    page.locator('.control-comparison').click()
    page.keyboard.press('BracketRight')
    expect(page.locator('.main-cue')).to_contain_text('1M02')
    expect(page.locator('#toast')).to_contain_text('Stop the active')
    page.keyboard.press('Meta+Enter')
    print('PASS: star filter, Alt, unique Best, quick-note drafts and safe cue shortcuts',flush=True)

    page.goto(URL+'#planning')
    page.locator('.planning-adjust summary').click()
    expect(page.locator('.schedule-focus')).to_contain_text('+2 min')
    page.locator('[data-extra="faster"]').click()
    expect(page.locator('.schedule-focus')).to_contain_text('+1 min')
    page.locator('[data-extra="pause-five"]').click()
    expect(page.locator('.schedule-focus')).to_contain_text('+6 min')
    page.locator('[data-planning="remaining"]').fill('132')
    page.locator('[data-planning="remaining"]').press('Tab')
    expect(page.locator('.schedule-focus')).to_contain_text('−1 min')
    expect(page.locator('.schedule-focus')).to_contain_text('ahead')
    page.locator('[data-planning="remaining"]').fill('133')
    page.locator('[data-planning="remaining"]').press('Tab')
    expect(page.locator('.schedule-focus')).to_contain_text('on schedule')
    page.locator('[data-session-cue="11"]').click()
    expect(page.locator('.main-cue')).to_contain_text('Ray Wakes Up')
    page.screenshot(path=str(OUT/'12-planning-extra.png'),full_page=True)

    print('PASS: schedule ahead/on/behind',flush=True)

    page.goto(URL+'#extra-input')
    page.locator('.extra-purpose summary').click()
    with page.expect_download() as dl:page.locator('[data-action="export-extra"]').click()
    dl.value.save_as(str(OUT/'Aanvullende-input.md'))
    assert (OUT/'Aanvullende-input.md').read_text()==(ROOT/'src/extra-input.md').read_text()
    page.goto(URL+'#voor-claude')
    expect(page.locator('[data-implementation-choice="note:loggen-vraag"]')).to_have_count(0)
    expect(page.locator('[data-implementation-choice="idea:take-afspraak"]')).to_have_count(0)
    expect(page.locator('[data-implementation-choice="idea:kniplijst"]')).to_have_count(0)
    page.locator('[data-implementation-choice="idea:planning"]').check()
    text=page.locator('.bundle-preview').text_content()
    ideas=json.loads((ROOT/'src/content.json').read_text())
    planning=next(i for i in ideas if i['id']=='planning')
    assert planning['requirement'] in text
    page.set_viewport_size({'width':390,'height':844})
    for key in ['planning']:
        page.goto(URL+'#'+key)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),key
        if key!='planning':
            page.locator('[data-variant="B"]').click()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),key+' B'
    assert not errors,errors
    browser.close()
    print('PASS: attributed source download, selective prompt and narrow A/B layouts',flush=True)
