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
 live=page.evaluate('running(state()).id')
 expect(page.locator(f'[data-calm-take="{live}"]')).to_have_class(__import__('re').compile('is-recording'))
 page.locator('[data-select-take="c0-t1"]').click()
 assert page.evaluate('running(state()).id')==live
 expect(page.locator('[data-calm-take="c0-t1"]')).not_to_have_class(__import__('re').compile('is-recording'))
 expect(page.locator('.calm-notes .take-recording-status')).to_have_text('● Take 3 is recording')
 page.evaluate("const el=document.querySelector('#cue-scroll'),b=document.querySelector('#main-panel .record');el.scrollTop+=b.getBoundingClientRect().bottom-el.getBoundingClientRect().top+20;syncSticky()")
 expect(page.locator('.sticky-slot .rec-status.rolling')).to_be_in_viewport()
 badge=page.locator('.sticky-slot .rec-status.rolling')
 assert badge.evaluate('(el)=>parseFloat(getComputedStyle(el).fontSize)')>=12
 assert badge.evaluate('(el)=>getComputedStyle(el).backgroundColor')=='rgb(188, 36, 68)'
 expect(page.locator('.sticky-slot .identity')).to_contain_text('Take 3')
 page.screenshot(path=str(ROOT/'checks/recording-status-scroll.png'))
 page.locator('[data-proposal-view="cutlist"]').click()
 expect(page.locator('.proposal-live-bar [data-wall-clock]')).to_be_visible()
 expect(page.locator('.proposal-live-bar [data-proposal-plan]')).to_be_visible()
 expect(page.locator('.proposal-live-bar .rec-status.rolling')).to_be_in_viewport()
 expect(page.locator('.proposal-live-bar .identity')).to_contain_text('Take 3')
 expect(page.locator('.score-take-row.is-recording [data-select-take]')).to_have_attribute('data-select-take',live)
 expect(page.locator('.score-take-row.is-recording .take-recording-status')).to_have_text('● Recording')
 page.screenshot(path=str(ROOT/'checks/recording-status-cutlist.png'))
 page.locator(f'[data-select-take="{live}"]').click()
 before=page.locator('.proposal-live-bar [data-wall-clock]').inner_text()
 page.clock.run_for(2200)
 expect(page.locator('.proposal-live-bar .timer')).to_have_text('00:02')
 assert page.locator('.proposal-live-bar [data-wall-clock]').inner_text()!=before
 page.set_viewport_size({'width':390,'height':844})
 for view in ['recording','cutlist']:
  page.evaluate('(view)=>showProposalView(view)',view)
  if view=='recording':page.evaluate("const el=document.querySelector('#cue-scroll'),b=document.querySelector('#main-panel .record');el.scrollTop+=b.getBoundingClientRect().bottom-el.getBoundingClientRect().top+20;syncSticky()")
  selector='.sticky-slot' if view=='recording' else '.proposal-live-bar'
  expect(page.locator(selector+' .rec-status.rolling')).to_be_in_viewport()
  stop=page.locator(selector+' .stop')
  expect(stop).to_be_in_viewport()
  b=stop.bounding_box();assert b['x']>=0 and b['x']+b['width']<=390,(view,b)
  assert page.evaluate('running(state()).id')==live
 page.set_viewport_size({'width':1512,'height':1100})
 page.keyboard.press('Meta+Enter')
 expect(page.locator('.proposal-live-bar .rec-status')).to_have_text('NOT RECORDING')
 expect(page.locator('.proposal-live-bar .timer')).to_have_text('00:02')
 expect(page.locator('.rec-status.rolling,.score-take-row.is-recording')).to_have_count(0)
 assert not errors,errors
 direct=browser.new_page(viewport={'width':1512,'height':1100})
 direct.goto((ROOT/'dist/index.html').as_uri()+'#cutlist');direct.locator('[data-tour-action="welcome-skip"]').click()
 expect(direct.locator('.proposal-live-bar [data-proposal-plan]')).not_to_have_text('Invalid Date')
 assert direct.evaluate('scoreWorkflowTiming(state()).clock.booked')==360*60
 browser.close()
print('PASS: explicit global idle/live styling, live take distinct from editing selection, scrolled recording status, cut-list take clock advances, wall clock and schedule difference visible and stopped duration retained')
