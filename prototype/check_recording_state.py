"""Idle/recording is explicit, with advancing clocks in the cut-list transport."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100});page.clock.install()
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 expect(page.locator('#main-panel')).to_have_class(__import__('re').compile('is-idle'))
 expect(page.locator('#main-panel .rec-status')).to_contain_text('Not recording')
 idle=page.locator('#main-panel .record').evaluate('(el)=>getComputedStyle(el).backgroundColor')
 page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
 expect(page.locator('#main-panel')).to_have_class(__import__('re').compile('is-recording'))
 expect(page.locator('#main-panel .rec-status')).to_contain_text('Recording')
 assert page.locator('#main-panel .record').evaluate('(el)=>getComputedStyle(el).backgroundColor')!=idle
 page.locator('[data-proposal-view="cutlist"]').click()
 expect(page.locator('.proposal-live-bar [data-wall-clock]')).to_be_visible()
 expect(page.locator('.proposal-live-bar [data-proposal-expected-end]')).to_be_visible()
 before=page.locator('.proposal-live-bar [data-wall-clock]').inner_text()
 page.clock.run_for(2200)
 expect(page.locator('.proposal-live-bar .timer')).to_have_text('00:02')
 assert page.locator('.proposal-live-bar [data-wall-clock]').inner_text()!=before
 page.keyboard.press('Meta+Enter')
 expect(page.locator('.proposal-live-bar .rec-status')).to_have_text('NOT RECORDING')
 expect(page.locator('.proposal-live-bar .timer')).to_have_text('00:02')
 assert not errors,errors
 direct=browser.new_page(viewport={'width':1512,'height':1100})
 direct.goto((ROOT/'dist/index.html').as_uri()+'#cutlist');direct.locator('[data-tour-action="welcome-skip"]').click()
 expect(direct.locator('.proposal-live-bar [data-proposal-expected-end]')).not_to_have_text('Invalid Date')
 assert direct.evaluate('scoreWorkflowTiming(state()).clock.booked')==360*60
 browser.close()
print('PASS: explicit idle/live styling, cut-list take clock advances, wall/expected clocks visible and stopped duration retained')
