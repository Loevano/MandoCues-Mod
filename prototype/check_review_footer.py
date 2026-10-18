"""Review controls live at the end of Recording and survive all rerenders."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1000})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri())
    page.locator('[data-tour-action="welcome-skip"]').click()
    for width in [1512,390]:
        page.set_viewport_size({'width':width,'height':1000})
        page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop=0')
        expect(page.locator('.proposal-review-footer .site-header')).to_have_count(1)
        expect(page.locator('.proposal-review-footer')).not_to_be_in_viewport()
        assert page.locator('.proposal-view-bar').bounding_box()['y']<30
        page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop=el.scrollHeight')
        expect(page.locator('[data-proposal-action="tour"]')).to_be_in_viewport()
        page.locator('[data-proposal-action="questions"]').click()
        page.locator('[data-tour-action="close-dialog"]').last.click()
        page.keyboard.press('Meta+Enter')
        expect(page.locator('.proposal-review-footer .site-header')).to_have_count(1)
        page.locator('[data-proposal-view="cutlist"]').click()
        expect(page.locator('.proposal-cutlist-review [data-proposal-action="tour"]')).to_be_visible()
        page.locator('[data-proposal-view="recording"]').click()
        expect(page.locator('.proposal-review-footer [data-proposal-action="tour"]')).to_have_count(1)
        assert page.locator('.site-header').count()==1
    assert not errors,errors
    browser.close()
print('PASS: review controls below Recording, recovered top space, rerender/view-switch preservation and responsive layout')
