"""Holding brackets repeats navigation without repeating digit or recording actions."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page();page.clock.install()
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 def key(repeat=False):page.evaluate('(repeat)=>document.body.dispatchEvent(new KeyboardEvent("keydown",{key:"]",code:"BracketRight",bubbles:true,cancelable:true,repeat}))',repeat)
 for view in ['recording','cutlist']:
  page.locator(f'[data-proposal-view="{view}"]').click();page.evaluate('selectCue(state(),0)')
  key();assert page.evaluate('state().cue')==1
  key(True);assert page.evaluate('state().cue')==1
  page.clock.run_for(250);key(True);assert page.evaluate('state().cue')==2
  page.clock.run_for(700);key(True);assert page.evaluate('state().cue')==3
  page.clock.run_for(115);key(True);assert page.evaluate('state().cue')==4
  page.evaluate('document.body.dispatchEvent(new KeyboardEvent("keyup",{code:"BracketRight",bubbles:true}))')
  key(True);assert page.evaluate('state().cue')==4
  for code,key_name,boundary in [('BracketLeft','[','0'),('BracketRight',']','cues.length-1')]:
   page.evaluate('selectCue(state(),'+boundary+')')
   for repeat in [False,True,True]:
    page.clock.run_for(300)
    page.evaluate('''({code,key,repeat})=>document.body.dispatchEvent(new KeyboardEvent('keydown',{code,key,repeat,bubbles:true,cancelable:true}))''',{'code':code,'key':key_name,'repeat':repeat})
    assert page.evaluate('state().cue==='+boundary)
   page.evaluate('(code)=>document.body.dispatchEvent(new KeyboardEvent("keyup",{code,bubbles:true}))',code)
 browser.close()
print('PASS: one press, throttled repeat, faster held navigation, release stops, no boundary wrap and shared workspace semantics')
