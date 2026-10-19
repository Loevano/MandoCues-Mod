"""Changing schedule text must not move clocks or transport controls."""
from pathlib import Path
import sys
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent.parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':982});page.clock.install()
 page.goto((root/'prototype/dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 for view in ['recording','cutlist']:
  page.evaluate('(v)=>showProposalView(v)',view)
  for width in [1512,1250,1024,900,760,390]:
   page.set_viewport_size({'width':width,'height':982})
   if view=='recording':page.evaluate("const el=document.querySelector('#cue-scroll'),b=document.querySelector('#main-panel .record');el.scrollTop+=b.getBoundingClientRect().bottom-el.getBoundingClientRect().top+20;syncSticky()")
   panel='.sticky-slot .transport' if view=='recording' else '.proposal-live-bar .transport'
   def boxes():return page.locator(panel).evaluate('(el)=>[el,...el.querySelectorAll(".transport-clocks,.transport-clocks>*,[data-wall-clock],.transport-take-time,.record")].filter(e=>e.getBoundingClientRect().width).map(e=>{const b=e.getBoundingClientRect();return [b.x,b.y,b.width,b.height]})')
   baseline=None
   for delta in [0,1,-1,299,300,36001,0]:
    page.evaluate('d=>{state().scoreWorkflowClock.booked+=scoreWorkflowTiming(state()).delta-d}',delta)
    page.clock.run_for(220)
    assert page.locator(panel+' [data-proposal-plan]').inner_text()==page.evaluate('(d)=>proposalScheduleText(d)',delta)
    b=boxes()
    if baseline is None:baseline=b
    assert b==baseline,(view,width,delta,baseline,b)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(view,width)
 print('PASS stable signed schedule, clocks and buttons in both transports across six widths')
 browser.close()
