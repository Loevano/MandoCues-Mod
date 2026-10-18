"""Original cue planning, actual working time and manual completion stay in the shared model."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100});page.clock.install()
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
    expect(page.locator('[data-cue-complete]')).to_have_count(page.evaluate('cues.length'))
    expect(page.locator('[data-cue-planned="0"]')).to_have_value('10')
    expect(page.locator('[data-cue-complexity="0"]')).to_have_value('Medium')
    expect(page.locator('[data-cue-actual="0"]')).to_have_text('08:00')
    expect(page.locator('[data-cue-actual="2"]')).to_have_text('—')
    selected=page.evaluate('state().selected')
    original=page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,draft:t.draft,rating:t.rating,best:t.best,alt:t.alt}))')
    # Editing another cue never jumps the cue/take or changes notes.
    page.locator('[data-cue-complexity="1"]').select_option('High')
    field=page.locator('[data-cue-planned="1"]');field.fill('30');field.press('Enter')
    assert page.evaluate('cuePlannedMinutes(1)')==30
    assert page.evaluate('state().cue')==0 and page.evaluate('state().selected')==selected
    assert page.locator('[data-session-cue="1"]').evaluate('(el)=>el.style.flexBasis')=='240px'
    assert page.locator('[data-session-cue="1"]').get_attribute('title').endswith('30 min')
    page.locator('[data-cue-complete="1"]').check()
    expect(page.locator('[data-session-cue="1"]')).to_have_class('is-complete')
    assert page.evaluate('state().cue')==0
    assert page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,draft:t.draft,rating:t.rating,best:t.best,alt:t.alt}))')==original
    # Actual is cue working time, not the sum of take durations or wall-clock time.
    page.evaluate("document.querySelector('#cue-scroll').focus()")
    page.keyboard.press('Meta+Enter');page.clock.run_for(4200)
    expect(page.locator('[data-cue-actual="0"]')).to_have_text('08:04')
    page.keyboard.press('Meta+Enter');page.clock.run_for(3200)
    live=page.evaluate('running(state()).id')
    page.keyboard.press('Meta+Enter');assert page.evaluate('!running(state())')
    page.clock.run_for(2200)
    expect(page.locator('[data-cue-actual="0"]')).to_have_text('08:09')
    page.locator('[data-session-action="break"]').click();page.clock.run_for(3000)
    expect(page.locator('[data-cue-actual="0"]')).to_have_text('08:09')
    page.locator('[data-session-action="break"]').click()
    page.evaluate('selectCue(state(),1)');page.clock.run_for(2200)
    expect(page.locator('[data-cue-actual="0"]')).to_have_text('08:09')
    expect(page.locator('[data-cue-actual="1"]')).to_have_text('00:02')
    expect(page.locator('[data-cue-complete="1"]')).to_be_checked()
    expect(page.locator('[data-cue-complexity="1"]')).to_have_value('High')
    expect(page.locator('[data-cue-planned="1"]')).to_have_value('30')
    page.evaluate("showProposalView('cutlist')");page.clock.run_for(2200)
    page.evaluate("showProposalView('recording')")
    expect(page.locator('[data-cue-actual="1"]')).to_have_text('00:04')
    # Manual completion is independent of cue selection, transport and unfolding.
    page.locator('[data-cue-complete="1"]').uncheck()
    expect(page.locator('[data-session-cue="1"]')).not_to_have_class('is-complete')
    page.evaluate('selectCue(state(),0)')
    page.keyboard.press('Meta+Enter');live=page.evaluate('running(state()).id')
    page.locator('[data-cue-complete="0"]').check()
    assert page.evaluate('running(state()).id')==live
    page.keyboard.press('Meta+Enter')
    page.evaluate('selectCue(state(),1)');page.evaluate('selectCue(state(),0)')
    expect(page.locator('[data-cue-complete="0"]')).to_be_checked()
    # Input validation cannot poison the shared planning budget.
    for value in ['','-1','2000']:
        field=page.locator('[data-cue-planned="0"]');field.fill(value);field.press('Enter')
        expect(field).to_have_value('10')
        assert page.evaluate('cuePlannedMinutes(0)')==10
    for width in [1512,900,390]:
        page.set_viewport_size({'width':width,'height':1100})
        for selector in ['[data-cue-planned="0"]','[data-cue-complexity="0"]','[data-cue-complete="0"]','[data-cue-actual="0"]']:
            box=page.locator(selector).bounding_box();assert box['x']>=0 and box['x']+box['width']<=width,(width,selector,box)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
        page.locator('[data-open-cue="0"]').click();page.locator('[data-open-cue="0"]').click()
        expect(page.locator('[data-cue-complete="0"]')).to_be_checked()
        page.screenshot(path=str(ROOT/f'checks/cue-fields-{width}.png'))
    assert not errors,errors
    browser.close()
print('PASS: cue complexity/planned edits, shared timeline, manual completion, cumulative working time through takes/breaks/views, input validation and responsive fields')
