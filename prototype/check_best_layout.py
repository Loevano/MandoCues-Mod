from browser_support import launch_chromium
"""Best toggles must not move cue text, ratings, buttons or take rows."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT = Path(__file__).resolve().parent
URL = (ROOT / 'dist/index.html').as_uri()
SNAPSHOT = '''() => {
 const group=document.querySelector('.cue-group.current');
 const base=group.getBoundingClientRect();
 return Array.from(group.querySelectorAll('.cue-header,.cue-id,.cue-name,.cue-count,.source-cue-facts,.take-block,.take-block-head,.take-fold-button,.take-tools,.star-rating,.best,.alt')).map(el=>{
  const r=el.getBoundingClientRect();
  return [el.className,r.x-base.x,r.y-base.y,r.width,r.height];
 });
}'''
errors=[]
with sync_playwright() as p:
 browser=launch_chromium(p)
 page=browser.new_page()
 page.on('pageerror',lambda e:errors.append(str(e)))
 for width in [390,740,1000,1512]:
  page.set_viewport_size({'width':width,'height':1100})
  for route,variants in [('cue-take',['A']),('bediening',['A','B']),('notities',['A','B']),('planning',['A'])]:
   page.goto(URL+'#'+route)
   if route=='bediening':page.evaluate('state().controlsPrevious=true;renderDemo()')
   for variant in variants:
    if len(variants)>1:page.locator(f'[data-variant="{variant}"]').click()
    if page.locator('.cue-group.current [data-open-cue]').get_attribute('aria-expanded')=='false':
     page.locator('.cue-group.current [data-open-cue]').click()
    count=page.locator('.cue-group.current .cue-count').inner_text()
    baseline=page.evaluate(SNAPSHOT)
    for take in ['c0-t1','c0-t1','c0-t2','c0-t1']:
     button=page.locator(f'.cue-group.current [data-take-best="{take}"]')
     # Variant B opens only one full take card at a time.
     if button.count()==0:continue
     button.click()
     expect(page.locator('.cue-group.current .cue-count')).to_have_text(count)
     current=page.evaluate(SNAPSHOT)
     assert len(current)==len(baseline),(width,route,variant)
     for before,after in zip(baseline,current):
      assert before[0]==after[0]
      assert all(abs(a-b)<0.1 for a,b in zip(before[1:],after[1:])),(width,route,variant,take,before,after)
     assert page.locator('.cue-group.current .best[aria-pressed="true"]').count()<=1
 assert not errors,errors
 browser.close()
print('PASS: Best toggles and switching keep cue text, stars, buttons and rows fixed at 390, 740, 1000 and 1512px in every recording variant')
