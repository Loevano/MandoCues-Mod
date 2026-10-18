from browser_support import launch_chromium, check_original_score_books
"""Verify full-page instrument cut-lists with actual clicks, drags and undo."""
from pathlib import Path
import hashlib,json
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent
errors,network=[],[]
with sync_playwright() as p:
 b=launch_chromium(p)
 page=b.new_page(viewport={'width':1512,'height':1100})
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
 page.goto((ROOT/'dist/index.html').as_uri()+'#partituur')
 expect(page.locator('[data-variant]')).to_have_count(2)
 expect(page.locator('.score-toolbar,.score-page-overview,.score-gesture-help')).to_have_count(0)
 expect(page.locator('.score-paper')).to_have_count(3)
 assert page.locator('.score-canvas').evaluate('el=>el.clientHeight>2200&&getComputedStyle(el).overflowY==="visible"')
 assert page.locator('.score-viewer').bounding_box()['width']>800
 assert page.locator('.cutlist-how').bounding_box()['y']>page.locator('.score-paper').last.bounding_box()['y']
 assert page.evaluate('assets.production.documents.every(d=>d.regions.every(r=>scoreCells({...state(),doc:{id:d.id}},r.page).filter(c=>c.measure===r.measure).every(c=>c.height>0)))')
 page.locator('[data-score-new-take]').click()
 def cell(m,i='vln1',p=1):return page.locator(f'.score-paper[data-score-page="{p}"] [data-score-measure="{m}"][data-score-instrument="{i}"]')
 def note(text):return page.locator('.score-note-text').filter(has_text=text)
 def saved(text):return page.evaluate('(text)=>takeById(state(),state().selected).notes.find(n=>n.text===text)',text)
 def write(text):
  page.locator('#score-comment-text').fill(text);page.locator('#score-comment-text').press('Enter')
 cell(2).scroll_into_view_if_needed();r=cell(2).bounding_box();paper=page.locator('.score-paper').first.bounding_box()
 cell(2).dblclick(position={'x':r['width']*.45,'y':r['height']*.4})
 expect(page.locator('#score-comment-dialog')).to_be_visible()
 write('Viool een op deze plek')
 n=saved('Viool een op deze plek');assert n['instruments']==['vln1']
 expected_x=(r['x']+r['width']*.45-paper['x'])/paper['width'];expected_y=(r['y']+r['height']*.4-paper['y'])/paper['height']
 assert abs(n['anchor']['x']-expected_x)<.003 and abs(n['anchor']['y']-expected_y)<.003
 expect(note('Viool een op deze plek')).to_be_visible()
 expect(note('Viool een op deze plek')).to_have_text('Viool een op deze plek')
 assert note('Viool een op deze plek').evaluate('el=>el.children.length')==0
 # Keyboard undo removes the note, redo restores it.
 page.locator('.work-heading h1').click();page.keyboard.press('Meta+z');expect(note('Viool een op deze plek')).to_have_count(0)
 page.keyboard.press('Meta+Shift+z');expect(note('Viool een op deze plek')).to_have_count(1)
 cell(3,'vln2').dblclick();write('Alleen tweede viool')
 assert saved('Alleen tweede viool')['instruments']==['vln2']
 def drag(m1,i1,m2,i2,shift=False,button='left',p=1):
  start=cell(m1,i1,p);start.scroll_into_view_if_needed();a=start.bounding_box();z=cell(m2,i2,p).bounding_box()
  page.keyboard.down('Meta')
  if shift:page.keyboard.down('Shift')
  page.mouse.move(a['x']+a['width']*.45,a['y']+a['height']*.5);page.mouse.down(button=button)
  page.mouse.move(z['x']+z['width']*.55,z['y']+z['height']*.5,steps=12);page.mouse.up(button=button)
  if shift:page.keyboard.up('Shift')
  page.keyboard.up('Meta')
 def keys():return page.evaluate('scoreSelection(state(),takeById(state(),state().selected))')
 drag(4,'vln1',5,'vln2')
 assert set(keys())=={f'{m}:{i}' for m in [4,5] for i in ['vln1','vln2','vla','vc']},keys()
 drag(4,'vln1',5,'vln1',button='right')
 assert not keys(),keys()
 page.locator('[data-score-undo]').click();assert len(keys())==8
 drag(6,'vc',7,'vc',shift=True)
 assert all(f'{m}:{i}' in keys() for m in [6,7] for i in ['vln1','vln2','vla','vc'])
 cell(6,'vla').dblclick();write('Note bij altviool');assert saved('Note bij altviool')['instruments']==['vla']
 cell(7,'vln2').dblclick();write('Command blijft een instrument');assert saved('Command blijft een instrument')['instruments']==['vln2']
 cell(8,'vln1').dblclick(modifiers=['Shift']);write('Shift note voor iedereen');assert len(saved('Shift note voor iedereen')['instruments'])==4
 drag(6,'vc',7,'vc',shift=True,button='right')
 assert not any(k.startswith(('6:','7:')) for k in keys())
 expect(note('Note bij altviool')).to_have_count(1)
 # Text editing and deleting remain reversible without affecting other notes.
 note('Viool een op deze plek').click();page.locator('#score-comment-text').fill('Aangepaste vioolnote');page.locator('#score-comment-text').press('Enter')
 expect(note('Aangepaste vioolnote')).to_have_count(1)
 page.locator('[data-score-undo]').click();expect(note('Viool een op deze plek')).to_have_count(1)
 n=saved('Viool een op deze plek');page.locator(f'[data-delete-note="{n["id"]}"]').click();expect(note('Viool een op deze plek')).to_have_count(0)
 page.keyboard.press('Meta+z');expect(note('Viool een op deze plek')).to_have_count(1)
 # Native undo in the editor changes only text, never the cut-list history.
 cell(10,'vla').dblclick();field=page.locator('#score-comment-text');field.press_sequentially('Tekst met spaties')
 history=page.evaluate('takeById(state(),state().selected).scoreUndo[state().doc.id].length')
 field.press('Meta+z');assert field.input_value()!='Tekst met spaties'
 assert page.evaluate('takeById(state(),state().selected).scoreUndo[state().doc.id].length')==history
 field.press('Escape');expect(page.locator('#score-comment-dialog')).to_have_count(0)
 # A second page uses its own staff locations; notes remain at their own page and instrument.
 cell(18,'vc',2).dblclick();write('Cello op pagina twee');assert saved('Cello op pagina twee')['page']==2 and saved('Cello op pagina twee')['instruments']==['vc']
 previous_notes=page.locator('.score-note-text').count();previous_keys=set(keys())
 page.locator('[data-score-new-take]').click();expect(page.locator('.score-note-text')).to_have_count(0);assert not keys()
 expect(page.locator('[data-score-undo]')).to_be_disabled()
 page.locator('[data-select-take="c0-t3"]').click();expect(page.locator('.score-note-text')).to_have_count(previous_notes);assert set(keys())==previous_keys
 # Correct a saved measure and preserve the instrument, with undo restoring its click anchor.
 n=saved('Cello op pagina twee');item=page.locator(f'[data-note-id="{n["id"]}"]');item.locator('.measure-picker summary').click();item.locator('[data-picker-measure]').fill('36');item.locator('[data-picker-measure]').press('Enter')
 moved=saved('Cello op pagina twee');assert moved['page']==3 and moved['instruments']==['vc'] and moved['anchor']
 page.locator('[data-score-undo]').click();assert saved('Cello op pagina twee')['page']==2
 page.locator('.score-paper').first.scroll_into_view_if_needed()
 page.screenshot(path=str(ROOT/'checks/18-kniplijst-instrumenten.png'),full_page=True)
 page.screenshot(path=str(ROOT/'checks/19-kniplijst-venster.png'))
 # Cue changes still load actual pages, and a new cue has no previous take's layer.
 page.locator('#score-cue').select_option('1');expect(page.locator('.score-paper')).to_have_count(9)
 expect(page.locator('.score-note-text')).to_have_count(0)
 page.locator('#score-cue').select_option('0');expect(page.locator('.score-note-text')).to_have_count(previous_notes)
 # Narrow screens keep full pages and note editing inside the page width.
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 cell(8,'vc').dblclick();expect(page.locator('#score-comment-dialog')).to_be_visible()
 box=page.locator('#score-comment-dialog').bounding_box();assert box['x']>=0 and box['x']+box['width']<=390
 page.locator('#score-comment-text').press('Escape')
 assert not errors,errors
 assert not network,network
 b.close()
check_original_score_books(ROOT)
print('PASS: long full-size score, one layout, double-click comments and retained score anchors, whole-measure selection and removal, independent note context, undo/redo, native text undo, clean take layers, measure corrections, cue pages, mobile and unchanged PDFs')
