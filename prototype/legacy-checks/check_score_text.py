from browser_support import launch_chromium
"""Notes are plain score text at their anchor; every edit selection covers all staves."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent
errors=[]
with sync_playwright() as p:
 b=launch_chromium(p)
 page=b.new_page(viewport={'width':1512,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
 for variant in ['A','B']:
  page.goto((ROOT/'dist/index.html').as_uri()+'#partituur')
  page.locator('[data-action="reset"]').click();page.locator(f'[data-variant="{variant}"]').click()
  if variant=='A':page.locator('[data-score-new-take]').click()
  else:page.locator('.score-session-actions [data-action="record"]').click()
  def cell(m,i):return page.locator(f'[data-score-page="1"] [data-score-measure="{m}"][data-score-instrument="{i}"]')
  def keys():return page.evaluate('scoreSelection(state(),takeById(state(),state().selected))')
  cell(2,'vln2').click(modifiers=['Meta']);assert len(keys())==4
  assert all(k.startswith('2:') for k in keys())
  cell(2,'vc').click(button='right',modifiers=['Meta']);assert keys()==[]
  page.locator('[data-score-undo]').click();assert len(keys())==4
  cell(3,'vla').click(modifiers=['Meta','Shift']);assert len(keys())==8
  cell(3,'vln1').click(button='right',modifiers=['Meta']);assert len(keys())==4
  cell(2,'vln2').dblclick(position={'x':8,'y':8})
  page.locator('#score-comment-placement').select_option('free');page.locator('#score-comment-text').fill('minder expressief');page.locator('#score-comment-text').press('Enter')
  note=page.locator('.score-text-annotation').filter(has_text='minder expressief')
  expect(note).to_have_text('minder expressief');assert note.evaluate('el=>el.childElementCount')==0
  assert note.evaluate('el=>getComputedStyle(el).backgroundColor')=='rgba(0, 0, 0, 0)'
  assert note.evaluate('el=>getComputedStyle(el).borderTopWidth')=='0px'
  saved=page.evaluate('takeById(state(),state().selected).notes.find(n=>n.text==="minder expressief")');assert saved['instruments']==['vln2']
  for width in [1512,1100]:
   page.set_viewport_size({'width':width,'height':1100})
   paper=page.locator('[data-score-page="1"]').bounding_box();r=note.bounding_box()
   assert abs((r['x']-paper['x'])/paper['width']-saved['anchor']['x'])<.002
   assert abs((r['y']-paper['y'])/paper['height']-saved['anchor']['y'])<.002
  page.set_viewport_size({'width':1512,'height':1100})
  note.click();page.locator('#score-comment-text').fill('zachter');page.locator('#score-comment-text').press('Enter')
  expect(page.locator('.score-text-annotation').filter(has_text='zachter')).to_have_count(1)
  page.locator('[data-score-undo]').click();expect(note).to_have_count(1)
  # A note in a blank margin needs no guessed measure or instrument label.
  paper=page.locator('[data-score-page="1"]');paper.scroll_into_view_if_needed();r=paper.bounding_box()
  paper.dblclick(position={'x':r['width']*.1,'y':r['height']*.02})
  expect(page.locator('#score-comment-measure')).to_have_value('')
  page.locator('#score-comment-text').fill('algemeen');page.locator('#score-comment-text').press('Enter')
  expect(page.locator('.score-text-annotation').filter(has_text='algemeen')).to_have_count(1)
  page.evaluate('''()=>{const s=state(),t=takeById(s,s.selected);t.scoreSelections[s.doc.id]=['9:vc'];renderDemo();}''')
  assert keys()==['9:vln1','9:vln2','9:vla','9:vc']
  page.locator('[data-score-page="1"] [data-score-measure="9"]').first.scroll_into_view_if_needed()
  page.screenshot(path=str(ROOT/f'checks/24-scoretekst-{variant}.png'))
  page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.set_viewport_size({'width':1512,'height':1100})
 assert not errors,errors
 b.close()
print('PASS: plain unlabelled score text at exact anchors, resize, edit/undo, blank-margin notes, independent instrument context, whole-measure selection/removal and legacy selections in A/B')
