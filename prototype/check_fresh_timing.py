"""A fresh session has no invented work; cue and take clocks have distinct scopes."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100});page.clock.install();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 def timing():return page.evaluate('(()=>{const t=scoreWorkflowTiming(state());return {elapsed:t.elapsed,cue:t.cueElapsed,delta:t.delta,remaining:t.remaining,forecast:t.clock.remaining}})()')
 initial=timing();assert initial=={'elapsed':0,'cue':0,'delta':0,'remaining':21600,'forecast':21600},initial
 page.clock.run_for(120000);assert timing()==initial
 page.keyboard.press('Meta+Enter');page.clock.run_for(5000)
 t=timing();assert t['elapsed']==t['cue']==5 and t['delta']==0 and t['remaining']==21595,t
 page.keyboard.press('Meta+Enter');page.clock.run_for(3000);page.keyboard.press('Meta+Enter')
 assert page.evaluate('state().takes[0].at(-1).duration')==3
 assert timing()['cue']==8
 page.clock.run_for(2000);assert timing()['cue']==10
 page.locator('[data-session-action="break"]').click();page.clock.run_for(5000)
 t=timing();assert t['cue']==10 and t['elapsed']==10 and t['delta']==5,t
 page.locator('[data-session-action="break"]').click()
 page.evaluate('selectCue(state(),1)');page.clock.run_for(3000)
 assert timing()['cue']==3 and timing()['elapsed']==13
 page.evaluate('selectCue(state(),0)');assert timing()['cue']==10
 assert not errors,errors
 browser.close();print('PASS: fresh zero clocks, frozen before Start session, separate take duration, cumulative cue work, budget forecast, breaks and cue resume')
