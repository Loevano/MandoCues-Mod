"""Original music capacity, complexity, completion summary and confirmed day reset."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium

ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100})
    page.clock.install();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
    page.locator('.session-planning-menu>summary').click()
    expect(page.locator('[data-music-usage]')).to_have_text('53:14 / 60:00')
    page.locator('[data-session-setting="music"]').fill('1')
    page.locator('[data-session-setting="music"]').press('Tab')
    expect(page.locator('[data-music-usage]')).to_have_class('session-music-usage is-over')
    expect(page.locator('[data-music-usage]')).to_have_text('53:14 / 01:00')
    page.locator('.session-planning-menu>summary').click()
    page.locator('[data-cue-complexity="0"]').select_option('Hard')
    for j in (0,1,2):page.locator(f'[data-cue-complete="{j}"]').check()
    expect(page.locator('.completed-cue-count')).to_have_text('3 of 26 cues done')
    page.locator('[data-draft="c0-t2"]').fill('A draft to reset')
    page.evaluate("state().cueNotes[0].push({id:'keep-general',text:'Keep cue note'});state().zoom=1.4")
    # Leave a distinct take on the other recording day.
    page.locator('[data-session-select]').select_option('strings-demo-day2')
    page.evaluate('newEmptyScoreTake(state())')
    other=page.evaluate('state().takes.map(ts=>ts.map(t=>({id:t.id,notes:t.notes,label:t.label})))')
    page.locator('[data-session-select]').select_option('strings-20261020')
    take_data=page.evaluate('JSON.stringify(state().takes)')
    page.locator('[data-session-action="reset"]').click()
    expect(page.locator('.app-dialog')).to_contain_text('Cue notes and planning settings stay.')
    page.locator('.app-dialog footer [data-app-dialog-close]').click()
    assert page.evaluate('JSON.stringify(state().takes)')==take_data
    page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter');page.clock.run_for(3200)
    expect(page.locator('[data-session-action="reset"]')).to_be_disabled()
    page.evaluate('confirmSessionReset(state())');expect(page.locator('.app-dialog')).to_have_count(0)
    page.keyboard.press('Meta+Enter')
    page.locator('[data-session-action="reset"]').click()
    page.locator('[data-confirm-session-reset]').click()
    assert page.evaluate('allTakes(state()).length')==0
    assert page.evaluate('state().selected') is None
    assert page.evaluate('scoreWorkflowTiming(state()).elapsed')==0
    assert page.evaluate('scoreWorkflowTiming(state()).cueElapsed')==0
    assert not page.evaluate('state().sessionStarted')
    assert page.evaluate('state().cueNotes[0].some(n=>n.id==="keep-general")')
    assert page.evaluate('state().zoom')==1.4
    assert page.evaluate('state().cueSettings[0].complexity')=='Hard'
    assert page.evaluate('state().maxMusicMinutes')==1
    expect(page.locator('.completed-cue-count')).to_have_text('0 of 26 cues done')
    expect(page.locator('.calm-cue-notes')).not_to_have_attribute('open','')
    page.locator('[data-proposal-view="cutlist"]').click()
    assert page.evaluate('state().selected') is None
    page.locator('[data-proposal-view="recording"]').click()
    page.locator('[data-session-select]').select_option('strings-demo-day2')
    assert page.evaluate('state().takes.map(ts=>ts.map(t=>({id:t.id,notes:t.notes,label:t.label})))')==other
    page.locator('[data-session-select]').select_option('strings-20261020')
    page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
    assert page.evaluate('running(state()).num')==1
    page.keyboard.press('Meta+Enter')
    for width in (390,900,1512):
        page.set_viewport_size({'width':width,'height':1100})
        page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop=0')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
        expect(page.locator('[data-session-action="reset"]')).to_be_visible()
    assert not errors,errors
    browser.close()
print('PASS: music capacity, original complexity names, cue totals, reset confirmation/cancel, live guard, retained planning/cue notes and day isolation')
