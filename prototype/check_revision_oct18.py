from browser_support import launch_chromium
import re
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent
URL=(ROOT/'dist/index.html').as_uri();errors=[]
with sync_playwright() as p:
 b=launch_chromium(p)
 page=b.new_page(viewport={'width':1512,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL+'#bediening')
 for variant in ['A','B']:
  page.locator(f'[data-variant="{variant}"]').click();page.locator('[data-action="reset"]').click()
  expect(page.locator('.control-comparison,.control-layout-key,.start-notes')).to_have_count(0)
  expect(page.locator('.cue-timeline-track button')).to_have_count(26)
  def boxes():return page.locator('.calm-take-row').evaluate_all('els=>els.map(el=>{let b=el.getBoundingClientRect();return [el.dataset.calmTake,b.height,...Array.from(el.querySelectorAll(".star-rating,.best,.alt")).flatMap(e=>{let r=e.getBoundingClientRect();return [r.x-b.x,r.y-b.y,r.width,r.height]})]})')
  before=boxes()
  for take in ['c0-t1','c0-t2','c0-t1']:
   page.locator(f'.calm-take-name[data-select-take="{take}"]').click()
   assert boxes()==before,(variant,take,before,boxes())
   expect(page.locator('.calm-notes>header')).to_contain_text('Take '+take[-1])
   page.locator(f'[data-take-best="{take}"]').click();assert boxes()==before
   page.locator(f'[data-take-alt="{take}"]').click();assert boxes()==before
  page.locator('#main-panel [data-action="record"]').click()
  assert page.evaluate('running(state()).id')=='c0-t3'
  unrated=boxes();page.locator('[data-rating-key="c0-t3"][data-stars="5"]').click();assert boxes()==unrated
  field=page.locator('.calm-notes textarea[data-draft]');field.fill('Concept blijft behouden')
  if variant=='A':
   page.locator('#cue-scroll').evaluate('el=>el.scrollTop=document.querySelector("#main-panel").offsetHeight+100')
   page.wait_for_timeout(100)
   expect(page.locator('.sticky-slot')).to_have_attribute('aria-hidden','false')
  field.press('Meta+Enter');assert page.evaluate('!running(state())')
  expect(field).to_have_value('Concept blijft behouden')
  page.locator('[data-control-version="previous"]').click();expect(page.locator('.control-comparison')).to_have_count(1)
  page.locator('[data-control-version="new"]').click();expect(page.locator('.calm-notes textarea[data-draft]')).to_have_value('Concept blijft behouden')
  page.locator('[data-action="fullscreen-prototype"]').click()
  assert page.evaluate('!!document.fullscreenElement||!!document.querySelector(".prototype-expanded")')
  page.screenshot(path=str(ROOT/f'checks/25-rustiger-2{variant}.png'))
  if page.evaluate('!!document.fullscreenElement'):page.evaluate('document.exitFullscreen()')
  else:page.keyboard.press('Escape')
  page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),variant
  page.set_viewport_size({'width':1512,'height':1100})
 page.locator('.control-review>summary').click();page.locator('[data-control-review="rows"][data-review-value="Goed"]').click();page.reload()
 page.locator('.control-review>summary').click();expect(page.locator('[data-control-review="rows"][data-review-value="Goed"]')).to_have_attribute('aria-pressed','true')
 page.goto(URL+'#partituur')
 def cell(m,i='vln1'):return page.locator(f'[data-score-page="1"] [data-score-measure="{m}"][data-score-instrument="{i}"]')
 page.locator('[data-select-take="c0-t1"]').click();cell(2).click(modifiers=['Meta'])
 page.locator('[data-select-take="c0-t2"]').click();cell(3,'vc').click(modifiers=['Meta'])
 expect(page.locator('.ghost-range[data-cut-measure="2"]')).to_have_count(1)
 page.locator('[data-select-take="c0-t1"]').click(modifiers=['Meta'])
 expect(page.locator('.score-take-picker [aria-pressed="true"]')).to_have_count(2)
 expect(page.locator('.compared-range[data-cut-measure="2"]')).to_have_count(1)
 expect(page.locator('.compared-range[data-cut-measure="3"]')).to_have_count(1)
 page.locator('[data-select-take="c0-t1"]').click(modifiers=['Meta'])
 expect(page.locator('.score-take-picker [aria-pressed="true"]')).to_have_count(1)
 assert page.evaluate('state().selected')=='c0-t2'
 cell(4,'vln2').hover();assert cell(4,'vln2').evaluate('el=>getComputedStyle(el).backgroundColor')=='rgba(0, 0, 0, 0)'
 cell(4,'vln2').click();expect(page.locator('#score-comment-dialog')).to_have_count(0)
 cell(4,'vln2').dblclick();page.locator('#score-comment-text').fill('rustiger');page.locator('#score-comment-text').press('Enter')
 note=page.locator('.score-text-annotation').filter(has_text=re.compile('^rustiger$'));expect(note).to_have_text('rustiger')
 assert note.evaluate('el=>el.children.length')==0
 data=page.evaluate('takeById(state(),state().selected).notes.find(n=>n.text==="rustiger")');assert data['instruments']==['vln2'] and data['placement']=='auto'
 page.wait_for_timeout(100)
 pos=note.bounding_box();staff=cell(4,'vln2').bounding_box();assert pos['y']<staff['y']+staff['height']/2
 note.click();page.locator('#score-comment-instrument').select_option('all');page.locator('#score-comment-text').press('Enter')
 pos=note.bounding_box();upper=cell(4,'vln1').bounding_box();assert pos['y']<upper['y']+upper['height']/2
 page.locator('[data-score-page="1"]').evaluate('el=>window.scrollTo(0,window.scrollY+el.getBoundingClientRect().top-15)');page.screenshot(path=str(ROOT/'checks/27-score-plaatsing.png'))
 note.click();page.locator('#score-comment-placement').select_option('free');page.locator('#score-comment-text').press('Enter')
 page.locator('[data-select-take="c0-t1"]').click(modifiers=['Meta'])
 page.screenshot(path=str(ROOT/'checks/26-score-vergelijken.png'))
 page.locator('[data-score-new-take]').click();expect(page.locator('.score-text-annotation')).to_have_count(0)
 assert page.evaluate('scoreVisibleTakes(state()).length')==1
 assert not errors,errors
 b.close()
print('PASS: calm 2A/B fixed row/rating/label geometry, preserved drafts, previous/new comparison, persisted review, fullscreen, mobile; multi-take comparison, ghost ranges, clear hover, double-click, instrument/system text and clean take layers')
