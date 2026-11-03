"""Visual containment matters: a page can avoid horizontal scroll and still overlap."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'prototype'))
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright,expect

def assert_rows(page,context):
 violations=page.evaluate('''() => [...document.querySelectorAll('.calm-take-row')].filter(row=>row.getBoundingClientRect().height).flatMap(row=>{
  const r=row.getBoundingClientRect();return [...row.querySelectorAll('.calm-take-name,.take-label-input,[data-v4-edit-take-range],.take-tools')].map(el=>({el,r:el.getBoundingClientRect()})).filter(({r:c})=>c.width&&c.height&&(c.top<r.top-1||c.bottom>r.bottom+1||c.left<r.left-1||c.right>r.right+1)).map(({el,r:c})=>({take:row.dataset.calmTake,child:el.className,row:{x:r.x,y:r.y,w:r.width,h:r.height},childRect:{x:c.x,y:c.y,w:c.width,h:c.height}}));})''')
 assert not violations,(context,violations)
 overlaps=page.evaluate('''() => [...document.querySelectorAll('.calm-take-row')].filter(row=>row.getBoundingClientRect().height).flatMap(row=>{
  const items=[...row.querySelectorAll('.calm-take-name,.take-label-input,[data-v4-edit-take-range],.take-tools')].map(el=>({name:el.className,r:el.getBoundingClientRect()}));return items.flatMap((a,i)=>items.slice(i+1).filter(b=>a.r.width&&b.r.width&&Math.min(a.r.right,b.r.right)-Math.max(a.r.left,b.r.left)>1&&Math.min(a.r.bottom,b.r.bottom)-Math.max(a.r.top,b.r.top)>1).map(b=>({take:row.dataset.calmTake,a:a.name,b:b.name})));})''')
 assert not overlaps,(context,overlaps)


with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':982});page.set_default_timeout(10000);errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.goto((ROOT/'index.html').as_uri())
 expect(page.locator('#main-panel.original-panel')).to_have_count(1)
 for selector in ['.original-wall-clock','[data-action=prev-cue]','[data-action=next-cue]','.cue-jump-menu','[data-session-action=break]','[data-session-action=end]','[data-session-action=reset]']:
  expect(page.locator('#main-panel '+selector)).to_have_count(1)
 expect(page.locator('.calm-notes')).to_have_count(1)
 # Merely evaluating an A/B layout must never create musical/session data.
 before=page.evaluate('JSON.stringify({ranges:state().v4Ranges,takes:allTakes(state()).map(t=>({id:t.id,range:t.barRange}))})')
 page.evaluate("v4ApplyChoice('ranges','B');v4ApplyChoice('ranges','A');v4ApplyChoice('ranges','B')")
 assert page.evaluate('JSON.stringify({ranges:state().v4Ranges,takes:allTakes(state()).map(t=>({id:t.id,range:t.barRange}))})')==before
 # Open the range picker: positions of record, navigation, timeline and rows stay put.
 selectors=['#main-panel .record','#main-panel .proposal-cue-switcher','.cue-timeline','.calm-take-row']
 boxes={s:page.locator(s).first.bounding_box() for s in selectors}
 page.locator('[data-v4-range-open=next]').click()
 expect(page.locator('#v4-range-popover')).to_be_visible()
 expect(page.locator('#v4-range-form [name=from]')).to_have_value('')
 expect(page.locator('#v4-range-form [name=to]')).to_have_value('')
 assert all(page.locator(s).first.bounding_box()==boxes[s] for s in selectors)
 page.locator('#v4-range-form [name=from]').fill('6');page.locator('#v4-range-form [name=to]').fill('9')
 assert all(page.locator(s).first.bounding_box()==boxes[s] for s in selectors)
 page.keyboard.press('Escape');expect(page.locator('#v4-range-popover')).to_have_count(0)
 for width in [1512,1280,1024,900,390]:
  page.set_viewport_size({'width':width,'height':982})
  page.evaluate("showProposalView('recording');selectCue(state(),0)")
  page.locator('.calm-cue-list').scroll_into_view_if_needed();assert_rows(page,('recording',width))
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  page.screenshot(path=str(ROOT/f'check-layout-recording-{width}.png'))
  page.locator('[data-calm-take]').first.locator('[data-v4-edit-take-range]').click()
  expect(page.locator('#v4-range-popover')).to_be_visible()
  rect=page.locator('#v4-range-popover').bounding_box();assert rect['x']>=0 and rect['x']+rect['width']<=width+1
  page.keyboard.press('Escape')
  page.locator('[data-proposal-view=cutlist]').click();assert_rows(page,('score',width))
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  page.screenshot(path=str(ROOT/f'check-layout-score-{width}.png'))
 # Highlight only the control, without a transient main-panel sized rectangle.
 page.set_viewport_size({'width':1512,'height':982});page.evaluate('openTourStep(2);positionProposalTour()')
 r=page.locator('.v4-range-slot .v4-range-trigger').bounding_box();h=page.locator('.proposal-tour-highlight').bounding_box()
 assert abs(h['width']-(r['width']+10))<2,(h,r)
 assert h['height']<60,(h,r)
 assert not errors,errors
 browser.close()
print('PASS no row overflow/overlap at five widths, original panel retained, no seeded ranges, stable floating editor and precise highlight')
