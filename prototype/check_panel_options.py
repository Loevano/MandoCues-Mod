"""Original-style grouping, clear recording feedback and compact alternative share state."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1728,'height':1117});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 expect(page.locator('.proposal-project-title')).to_have_text('After Party')
 assert page.locator('.proposal-project-heading h1 svg').count()==1
 header=page.locator('.proposal-session-header').bounding_box();panel=page.locator('#main-panel').bounding_box()
 assert header['y']+header['height']<panel['y']
 expect(page.locator('#main-panel .proposal-session-header,.proposal-main-planning,.main-session-rail')).to_have_count(0)
 expect(page.locator('[data-proposal-cue-clock]')).to_have_text('00:00')
 expect(page.locator('[data-plan-status]')).to_have_text('On schedule')
 for layout in ['A','B']:
  page.locator(f'[data-main-layout="{layout}"]').click()
  name=page.locator('#main-panel .main-cue>b');clock=page.locator('#main-panel [data-wall-clock]')
  assert name.evaluate('el=>parseFloat(getComputedStyle(el).fontSize)')>=60
  assert clock.evaluate('el=>parseFloat(getComputedStyle(el).fontSize)')>=45
  assert name.bounding_box()['x']<clock.bounding_box()['x']
  page.screenshot(path=str(ROOT/f'checks/original-panel-{layout}-idle.png'))
 # Views stay centered in the header.
 nav=page.locator('.proposal-view-toggle').bounding_box();bar=page.locator('.proposal-view-bar').bounding_box()
 assert abs((nav['x']+nav['width']/2)-(bar['x']+bar['width']/2))<2
 page.locator('.session-planning-menu>summary').click()
 page.locator('[data-session-setting="length"]').fill('300');page.locator('[data-session-setting="length"]').press('Tab')
 expect(page.locator('[data-session-hours]')).to_have_text('5h 00m')
 page.locator('[data-session-setting="length"]').fill('360');page.locator('[data-session-setting="length"]').press('Tab')
 page.locator('.session-planning-menu>summary').click()
 page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
 expect(page.locator('.session-planning-panel')).not_to_be_visible()
 expect(page.locator('body')).to_have_class(__import__('re').compile('take-is-recording'))
 expect(page.locator('.proposal-global-recording')).to_contain_text('Take 3')
 for layout in ['A','B']:
  page.locator(f'[data-main-layout="{layout}"]').click()
  assert page.evaluate('running(state()).id')=='c0-t3'
  expect(page.locator('#main-panel .main-take-heading')).to_contain_text('Take 3')
  page.screenshot(path=str(ROOT/f'checks/original-panel-{layout}-recording.png'))
  for width in [900,390]:
   page.set_viewport_size({'width':width,'height':844})
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(layout,width)
   page.screenshot(path=str(ROOT/f'checks/original-panel-{layout}-{width}.png'))
  page.set_viewport_size({'width':1728,'height':1117})
 page.keyboard.press('Meta+Enter')
 assert page.evaluate('!document.body.classList.contains("take-is-recording")')
 assert not errors,errors
 browser.close();print('PASS: original cue/clock proportions, single session context, centered view switch, minutes/hours, global recording feedback, shared alternatives and responsive width')
