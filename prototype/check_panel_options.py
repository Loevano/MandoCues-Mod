"""Compare real panel layouts without losing recording, note or planning state."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1728,'height':1117});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 page.evaluate("unifiedState.takes[0][1].draft.text='Keep this draft';renderDemo()")
 for layout in ['A','B']:
  page.locator(f'[data-main-layout="{layout}"]').click()
  expect(page.locator('#main-panel')).to_have_class(__import__('re').compile('layout-'+layout))
  assert page.evaluate("unifiedState.takes[0][1].draft.text")== 'Keep this draft'
  clock=page.locator('#main-panel [data-wall-clock]');assert float(clock.evaluate('el=>getComputedStyle(el).fontSize').replace('px',''))>=65
  assert page.locator('#main-panel .main-take-heading').inner_text().startswith('Take 2')
  assert page.locator('.proposal-session-header').count()==1
  assert page.locator('#main-panel details.calm-session').count()==0
  page.locator('#main-panel').screenshot(path=str(ROOT/f'checks/panel-option-{layout}.png'))
 # Floating planned picker: no layout shift, typed and clicked minutes share the timeline.
 summary=page.locator('#main-panel .planned-picker>summary');before=clock.bounding_box();summary.click()
 picker=page.locator('#main-panel .planned-picker-panel');expect(picker).to_be_visible()
 assert clock.bounding_box()==before
 picker.locator('input').fill('32');picker.locator('input').press('Enter')
 expect(page.locator('#main-panel .planned-picker>summary')).to_contain_text('32')
 expect(page.locator('[data-session-cue="0"]')).to_have_attribute('title',__import__('re').compile('32 min'))
 page.locator('.cue-group.current .planned-picker>summary').click()
 page.locator('.cue-group.current [data-pick-planned="15"]').click()
 expect(page.locator('#main-panel .planned-picker>summary')).to_contain_text('15')
 page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
 expect(page.locator('#main-panel .rec-status')).to_have_text('● Recording')
 expect(page.locator('#main-panel .main-take-heading>strong')).to_have_text('Take 3')
 for layout in ['A','B']:
  page.locator(f'[data-main-layout="{layout}"]').click()
  expect(page.locator('#main-panel .rec-status')).to_have_text('● Recording')
  assert page.evaluate('running(unifiedState).id')=='c0-t3'
  page.locator('#main-panel').screenshot(path=str(ROOT/f'checks/panel-option-{layout}.png'))
  page.set_viewport_size({'width':390,'height':844})
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),layout
  page.screenshot(path=str(ROOT/f'checks/panel-option-{layout}-mobile.png'))
  page.set_viewport_size({'width':1728,'height':1117})
 assert not errors,errors
 browser.close();print('PASS: two panel options, large clock/cue/take, shared live state, compact settings, floating planned picker and mobile bounds')
