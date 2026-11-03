"""Browser checks for planning state and manual recovery, using a controlled clock."""
from pathlib import Path
from datetime import datetime,timedelta,timezone
import sys,json
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'prototype'))
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1000});page.set_default_timeout(10000);errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 start=datetime(2026,11,3,12,tzinfo=timezone.utc);page.clock.install(time=start);page.clock.pause_at(start+timedelta(seconds=1));page.goto((ROOT/'index.html').as_uri())
 expect(page.locator('.proposal-version')).to_have_text('v4')
 expect(page.locator('#proposal-welcome')).to_have_count(0)
 expect(page.locator('[data-v4-forecast]')).to_have_text('On schedule')
 expect(page.locator('.v4-timing-details')).not_to_have_attribute('open','')
 notes=page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes.map(n=>({id:n.id,text:n.text,clockAt:n.clockAt}))}))')
 # Space first starts only the session. Cue working time is independent of takes.
 page.locator('.proposal-workspace-title').click();page.keyboard.press('Space')
 assert page.evaluate('state().sessionStarted&&!running(state())')
 page.clock.run_for(1234);page.evaluate('selectCue(state(),1)')
 for _ in range(20):
  page.clock.run_for(100)
  assert page.evaluate('v4Forecast(state()).delta')==0
 # Correct a missed cue switch without changing take IDs, comments or transport.
 page.locator('#main-panel [data-v4-edit-cue]').click()
 form=page.locator('#v4-cue-timing');form.locator('[name=worked]').fill('35:00');form.locator('[name=music]').fill('02:00')
 page.locator('[form="v4-cue-timing"]').click()
 assert page.evaluate('v4Row(state(),1).musicSeconds')==120
 assert page.evaluate('v4Forecast(state()).current.workedSeconds')==2100
 assert page.evaluate('v4State(state()).corrections.length')==1
 assert page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes.map(n=>({id:n.id,text:n.text,clockAt:n.clockAt}))}))')==notes
 assert page.evaluate('!running(state())')
 # Leaving a timing dialog open must not erase work while editing only music.
 page.locator('#main-panel [data-v4-edit-cue]').click();page.clock.run_for(3000)
 form.locator('[name=music]').fill('02:10');page.locator('[form="v4-cue-timing"]').click()
 assert page.evaluate('v4Forecast(state()).current.workedSeconds')>=2103
 assert page.evaluate('v4State(state()).corrections.length')==1
 # Only completing the cue trains the estimator; the original pace is immutable.
 assert page.evaluate('v4Forecast(state()).samples')==0
 rate=page.evaluate('v4State(state()).rate')
 page.locator('.cue-group.current [data-cue-complete]').check()
 assert page.evaluate('v4Forecast(state()).samples')==1
 assert page.evaluate('v4Forecast(state()).factor')>1
 completed=page.evaluate('v4Forecast(state()).current.workedSeconds');factor=page.evaluate('v4Forecast(state()).factor')
 page.clock.run_for(2500)
 assert page.evaluate('v4Forecast(state()).current.workedSeconds')==completed
 assert page.evaluate('v4Forecast(state()).factor')==factor
 before=page.evaluate('v4Forecast(state()).remaining')
 page.evaluate('setProposalBudget(state(),state().booked+30)')
 assert page.evaluate('v4State(state()).rate')==rate
 assert abs(page.evaluate('v4Forecast(state()).remaining')-before)<.01
 # Exclude an atypical cue from learning; keep the work in the session ledger.
 page.locator('#main-panel [data-v4-edit-cue]').click();form.locator('[name=include]').uncheck();page.locator('[form="v4-cue-timing"]').click()
 assert page.evaluate('v4Forecast(state()).samples')==0
 assert page.evaluate('v4Forecast(state()).current.workedSeconds')>=2100
 # Both signs adjust the same end, with a 15-minute minimum.
 page.locator('.session-planning-menu>summary').click()
 before=page.evaluate('state().scoreWorkflowClock.plannedEndAt')
 page.locator('[data-extend-session="30"]').click();page.locator('[data-v4-shorten="30"]').click()
 assert page.evaluate('state().scoreWorkflowClock.plannedEndAt')==before
 page.evaluate('setProposalBudget(state(),15)');page.locator('[data-v4-shorten="60"]').click()
 assert page.evaluate('state().booked')==15
 assert not errors,errors
 browser.close()
print('PASS v4 planning, no flicker, cue correction, learning/exclusion, fixed learned reference and signed deadline controls')
