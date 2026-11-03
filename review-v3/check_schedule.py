"""Regression for a one-second schedule flicker after switching cues."""
from pathlib import Path
from datetime import datetime,timedelta,timezone
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'prototype'))
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1000});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 start=datetime(2026,11,3,12,0,tzinfo=timezone.utc);page.clock.install(time=start);page.clock.pause_at(start+timedelta(seconds=1))
 page.goto((ROOT/'index.html').as_uri());expect(page.locator('#proposal-welcome')).to_have_count(0)
 # Equal total work/budget: neither cue selection nor take selection is a delay.
 page.evaluate('''() => {const s=state();cues.forEach((_,j)=>cueSettings(s,j).planned=5);setProposalBudget(s,cues.length*5);performRecordingAction(s);}''')
 page.clock.run_for(250);page.evaluate('selectCue(state(),1)')
 samples=[]
 for _ in range(30):
  page.clock.run_for(100)
  samples.append(page.evaluate('''() => {const t=scoreWorkflowTiming(state());return {delta:t.delta,elapsed:t.elapsed,cue:t.cueElapsed,status:document.querySelector('[data-plan-status]').textContent,classes:document.querySelector('[data-plan-card]').className};}'''))
 assert all(t['delta']==0 for t in samples),samples
 assert all(t['status']=='On schedule' and 'is-on-time' in t['classes'] for t in samples),samples
 # Frequent cue switches do not accumulate rounded-away work.
 for cue in [2,0,1,3,1,0,2,1]:
  page.clock.run_for(137);page.evaluate('(cue)=>selectCue(state(),cue)',cue)
  assert page.evaluate('scoreWorkflowTiming(state()).delta')==0
  assert page.evaluate('''() => {const t=scoreWorkflowTiming(state()),spent=Object.entries(t.clock.cueSpent).filter(([j])=>+j!==state().cue).reduce((n,[,seconds])=>n+seconds,0);return spent+t.cueElapsed===t.elapsed;}''')
 # Rendering and switching views use the same stable forecast.
 page.evaluate("showProposalView('cutlist')");page.clock.run_for(1250)
 expect(page.locator('[data-proposal-plan]')).to_have_text('On schedule')
 page.evaluate("showProposalView('recording')");page.clock.run_for(1250)
 expect(page.locator('[data-plan-card]')).to_have_class('main-plan-card is-on-time')
 # Real overruns still show orange, then red at five minutes.
 page.clock.fast_forward(300000)
 delta=page.evaluate('scoreWorkflowTiming(state()).delta');assert 0<delta<300,delta
 expect(page.locator('[data-plan-card]')).to_have_class('main-plan-card is-behind')
 page.clock.fast_forward(300000)
 assert page.evaluate('scoreWorkflowTiming(state()).delta')>=300
 expect(page.locator('[data-plan-card]')).to_have_class('main-plan-card is-late')
 # Pauses stop both work clocks and keep their totals when resuming.
 before=page.evaluate('scoreWorkflowTiming(state())')
 page.evaluate('proposalSessionBreak(state())');page.clock.run_for(1500)
 paused=page.evaluate('scoreWorkflowTiming(state())')
 assert paused['elapsed']==before['elapsed'] and paused['cueElapsed']==before['cueElapsed']
 page.evaluate('proposalSessionBreak(state())')
 assert page.evaluate('scoreWorkflowTiming(state()).delta')==paused['delta']
 page.evaluate('proposalEndSession(state())');ended=page.evaluate('scoreWorkflowTiming(state())')
 page.clock.run_for(1200)
 assert page.evaluate('scoreWorkflowTiming(state()).elapsed')==ended['elapsed']
 page.evaluate('performRecordingAction(state())');page.clock.run_for(1000)
 assert page.evaluate('scoreWorkflowTiming(state()).elapsed')==ended['elapsed']+1
 # Increasing the real session budget still produces the green ahead state.
 page.evaluate('setProposalBudget(state(),state().booked+60);renderDemo()');page.clock.run_for(200)
 assert page.evaluate('scoreWorkflowTiming(state()).delta')<0
 expect(page.locator('[data-plan-card]')).to_have_class('main-plan-card is-ahead')
 assert not errors,errors
 browser.close()
print('PASS no schedule flicker or cue-switch drift, consistent views, real orange/red/ahead states, pause and end/reopen')
