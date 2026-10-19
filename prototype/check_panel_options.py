"""One fixed panel keeps cue controls and live duration in place at start/stop."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1728,'height':1117});page.clock.install();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 expect(page.locator('[data-main-layout]')).to_have_count(0)
 expect(page.locator('[data-session-setting="length"]')).to_be_visible()
 expect(page.locator('#main-panel .main-session-times label')).to_have_count(4)
 expect(page.locator('#main-panel [data-proposal-plan]')).to_have_text('On schedule')
 for width in [1728,1024,900,390]:
  page.set_viewport_size({'width':width,'height':1117});page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop=0')
  selectors=['#main-panel .main-cue','#main-panel .record','#main-panel [data-action="record-overdub"]','#main-panel [data-action="prev-cue"]','#main-panel [data-action="next-cue"]','#main-panel .original-clock-side']
  positions=lambda:{s:page.locator(s).bounding_box() for s in selectors}
  before=positions()
  if not page.evaluate('state().sessionStarted'):page.keyboard.press('Meta+Enter')
  idle=positions();page.keyboard.press('Meta+Enter');live=positions()
  for s in selectors:
   assert before[s]==idle[s]==live[s],(width,s,before[s],idle[s],live[s])
  expect(page.locator('.main-live-take')).to_be_visible();page.clock.run_for(2200)
  expect(page.locator('#main-panel .recording-take-duration')).to_have_text('00:02')
  page.screenshot(path=str(ROOT/f'checks/fixed-panel-{width}-live.png'))
  page.keyboard.press('Meta+Enter');stopped=positions()
  for s in selectors:assert before[s]==stopped[s],(width,s,before[s],stopped[s])
  expect(page.locator('.main-live-take')).not_to_be_visible()
  expect(page.locator('.proposal-take-clock')).to_have_count(0)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  page.screenshot(path=str(ROOT/f'checks/fixed-panel-{width}-idle.png'))
 page.set_viewport_size({'width':390,'height':1117})
 page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop=0')
 page.locator('[data-action="record-overdub"]').click()
 assert page.evaluate('running(state()).kind')=='overdub'
 expect(page.locator('.main-live-take')).to_contain_text('Overdub 1')
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.keyboard.press('Meta+Enter')
 assert not errors,errors
 browser.close()
print('PASS fixed panel start/stop geometry and responsive widths')
