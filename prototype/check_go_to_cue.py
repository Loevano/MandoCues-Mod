"""The original cue jump stays beside Next cue and shares safe cue selection."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium

ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1100})
    errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto((ROOT/'dist/index.html').as_uri())
    page.locator('[data-tour-action="welcome-skip"]').click()
    page.locator('[data-draft="c0-t2"]').fill('Keep this draft')
    menu=page.locator('.cue-jump-menu');summary=menu.locator('summary')
    next_button=page.locator('#main-panel [data-action="next-cue"]')
    for width in (1512,900,390):
        page.set_viewport_size({'width':width,'height':1100})
        page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop=0')
        panel_before=page.locator('#main-panel').bounding_box()
        before=next_button.bounding_box()
        summary.click()
        expect(menu).to_have_attribute('open','')
        expect(page.locator('[data-cue-jump-search]')).to_be_focused()
        assert next_button.bounding_box()==before
        assert page.locator('#main-panel').bounding_box()==panel_before
        popup=page.locator('.cue-jump-panel').bounding_box()
        assert popup['x']>=0 and popup['x']+popup['width']<=width
        assert popup['y']>=0 and popup['y']+popup['height']<=1100
        assert page.locator('.cue-jump-options').evaluate('(el)=>el.scrollHeight>el.clientHeight')
        page.keyboard.press('Escape');expect(summary).to_be_focused()
    summary.click();search=page.locator('[data-cue-jump-search]')
    search.fill('1m18');search.press('Enter')
    expect(page.locator('#main-panel .main-cue')).to_contain_text('1M18')
    assert page.evaluate('state().cue')==1
    summary.click();search.fill('no such cue')
    expect(page.locator('.cue-jump-empty')).to_be_visible()
    search.press('Enter');assert page.evaluate('state().cue')==1
    search.fill('Arrival');search.press('ArrowDown');page.keyboard.press('Enter')
    assert page.evaluate('state().cue')==0
    expect(page.locator('[data-draft="c0-t2"]')).to_have_value('Keep this draft')
    summary.click();page.locator('#main-panel .main-cue').click()
    assert not menu.evaluate('(el)=>el.open')
    summary.click();page.locator('[data-go-to-cue="25"]').scroll_into_view_if_needed();page.locator('[data-go-to-cue="25"]').click()
    assert page.evaluate('state().cue')==25
    expect(next_button).to_be_disabled()
    page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
    live=page.evaluate('running(state()).id')
    expect(menu).to_have_attribute('inert','')
    page.evaluate('selectCue(state(),0)')
    assert page.evaluate('state().cue')==25 and page.evaluate('running(state()).id')==live
    page.keyboard.press('Meta+Enter')
    summary.click();search.fill('1m02');search.press('Enter')
    assert page.evaluate('state().cue')==0
    page.locator('[data-proposal-view="cutlist"]').click()
    assert page.evaluate('state().cue')==0
    assert not errors,errors
    browser.close()
print('PASS: Go to cue click/search/keyboard, floating menu, stable controls, no-match, mobile bounds, draft preservation and live take protection')
