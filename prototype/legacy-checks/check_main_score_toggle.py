from browser_support import launch_chromium
"""The score toggle stays in the recording window without resetting its work."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parent
errors=[]
with sync_playwright() as p:
 b=launch_chromium(p)
 page=b.new_page(viewport={'width':1512,'height':1100})
 page.on('pageerror',lambda e:errors.append(str(e)))
 for route,variants in [('cue-take',['A']),('bediening',['A','B']),('notities',['A','B']),('planning',['A'])]:
  page.goto((ROOT/'dist/index.html').as_uri()+'#'+route)
  for v in variants:
   if len(variants)>1:page.locator(f'[data-variant="{v}"]').click()
   if page.locator('[data-score-toggle]').get_attribute('aria-expanded')=='true':page.locator('[data-score-toggle]').click()
   before=page.evaluate('JSON.stringify(state().takes.map(ts=>ts.map(t=>({id:t.id,rating:t.rating,best:t.best,notes:t.notes,text:t.draft.text,rolling:t.rolling}))))')
   page.locator('[data-score-toggle]').click()
   expect(page.locator('[data-score-toggle]')).to_have_attribute('aria-expanded','true')
   expect(page.locator('#main-score-pane')).to_be_visible()
   expect(page.locator('#main-panel')).to_have_count(1)
   expect(page.locator('#main-score-pane header')).to_contain_text('1M02')
   assert page.locator('#main-score-pane').bounding_box()['x']>page.locator('.recording-score-body').bounding_box()['x']
   page.locator('.main-score-pages').evaluate('el=>el.scrollTop=200')
   page.locator('#main-score-pane [data-action="toggle-main-score"]').click()
   expect(page.locator('#main-score-pane')).to_have_count(0)
   assert page.evaluate('JSON.stringify(state().takes.map(ts=>ts.map(t=>({id:t.id,rating:t.rating,best:t.best,notes:t.notes,text:t.draft.text,rolling:t.rolling}))))')==before
   page.locator('[data-score-toggle]').click()
   assert page.locator('.main-score-pages').evaluate('el=>el.scrollTop')==200
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   page.set_viewport_size({'width':390,'height':844})
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(route,v)
   page.locator('#main-score-pane [data-action="toggle-main-score"]').click()
   page.set_viewport_size({'width':1512,'height':1100})
 page.goto((ROOT/'dist/index.html').as_uri()+'#cue-take')
 page.locator('[data-score-toggle]').click()
 page.locator('[data-select-cue="1"]').click()
 expect(page.locator('#main-score-pane header')).to_contain_text('1M18')
 expect(page.locator('#main-score-pane img').first).to_have_attribute('alt', 'Score 1M18, book page 37')
 expect(page.locator('#main-score-pane')).to_be_in_viewport()
 page.screenshot(path=str(ROOT/'checks/22-partituur-in-hoofdvenster.png'))
 page.goto((ROOT/'dist/index.html').as_uri()+'#notities')
 field=page.locator('#main-panel [data-draft="c0-t2"]');field.fill('Concept blijft bij de take')
 page.locator('[data-score-toggle]').click();expect(page.locator('#main-panel [data-draft="c0-t2"]')).to_have_value('Concept blijft bij de take')
 page.keyboard.press('Meta+Enter');assert page.evaluate('!running(state())')
 assert not errors,errors
 b.close()
print('PASS: main score toggle, actual cue pages, right-hand desktop view, mobile width, take/draft preservation, remembered score scroll and stop shortcut')
