"""Planning fields are editable without moving the UI; recording days isolate their data."""
from pathlib import Path
from datetime import datetime,timezone
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100},timezone_id='Europe/Amsterdam');errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.clock.install(time=datetime(2026,10,19,8,0,tzinfo=timezone.utc))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 expect(page.locator('#main-panel [data-wall-clock]')).to_have_text('10:00:00 AM')
 expect(page.locator('#main-panel .planning-metrics,#main-panel [data-proposal-elapsed]')).to_have_count(0)
 expect(page.locator('[data-session-setting="length"]')).not_to_be_visible()
 panel=page.locator('#main-panel');before=panel.bounding_box();page.locator('.session-planning-menu>summary').click()
 assert panel.bounding_box()==before
 end=page.locator('[data-planning-finish]');expect(end).to_have_value('16:00');end.fill('17:30');end.press('Tab')
 assert page.evaluate('state().booked')==450
 target=page.evaluate('state().scoreWorkflowClock.plannedEndAt');page.clock.run_for(120000)
 expect(end).to_have_value('17:30');assert page.evaluate('state().scoreWorkflowClock.plannedEndAt')==target
 page.keyboard.press('Meta+Enter');assert page.evaluate('state().scoreWorkflowClock.plannedEndAt')==target
 assert abs(page.evaluate('scoreWorkflowTiming(state()).remaining')-448*60)<2
 page.locator('[data-session-setting="length"]').fill('480');page.locator('[data-session-setting="length"]').press('Tab')
 expect(end).to_have_value('18:02');page.locator('[data-extend-session="60"]').click();expect(end).to_have_value('19:02')
 expect(page.locator('[data-session-hours]')).to_have_text('9h 00m')
 page.locator('.session-planning-menu>summary').click()
 first=page.evaluate('state().sessionId')
 page.locator('[data-draft="c0-t2"]').fill('Day one draft')
 page.evaluate('state().zoom=1.4')
 page.locator('[data-session-select]').select_option('strings-demo-day2')
 assert page.evaluate('state().takes.flat().length')==0 and page.evaluate('state().selected') is None
 assert page.evaluate('state().zoom')==1.4 and page.evaluate('scoreWorkflowTiming(state()).cueElapsed')==0
 page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
 expect(page.locator('[data-session-select]')).to_be_disabled()
 page.evaluate('(id)=>switchProposalSession(id)',first)
 assert page.evaluate('state().sessionId')=='strings-demo-day2'
 page.locator('[data-draft="c0-t1"]').fill('Day two note');page.locator('[data-draft="c0-t1"]').press('Enter')
 page.keyboard.press('Meta+Enter')
 page.locator('[data-session-select]').select_option(first)
 expect(page.locator('[data-draft="c0-t2"]')).to_have_value('Day one draft')
 assert page.evaluate('state().takes[0].length')==2 and page.evaluate('state().booked')==540
 page.locator('[data-session-select]').select_option('strings-demo-day2')
 expect(page.locator('.calm-notes .note-list')).to_contain_text('Day two note')
 assert page.evaluate('state().takes[0].length')==1
 for width in [1512,900,390]:
  page.set_viewport_size({'width':width,'height':844});page.locator('.session-planning-menu>summary').click()
  box=page.locator('.session-planning-panel').bounding_box();assert box['x']>=0 and box['x']+box['width']<=width and box['y']>=0 and box['y']+box['height']<=844,(width,box)
  page.keyboard.press('Escape');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
 assert not errors,errors
 browser.close();print('PASS: AM/PM, floating Planning, fixed Finish by, duration/extension, independent recording-day state, live-switch protection and responsive menu')
