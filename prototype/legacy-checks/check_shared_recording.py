from browser_support import launch_chromium
"""Check shared recording components and the current coloured cut-list interactions."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent
URL=(ROOT/'dist/index.html').as_uri()
errors,network=[],[]
with sync_playwright() as p:
 b=launch_chromium(p)
 page=b.new_page(viewport={'width':1512,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
 for id in ['cue-take','bediening','notities','planning']:
  page.goto(URL+'#'+id)
  expect(page.locator('#main-panel')).to_have_count(1)
  expect(page.locator('.source-session-summary')).to_have_count(1)
  expect(page.locator('.source-cue-plan')).to_have_count(1)
  expect(page.locator('.grouped-list')).to_have_count(1)
  expect(page.locator('[data-select-cue="1"]')).to_have_count(1)
  assert page.evaluate('state().takes.length')==26
 page.goto(URL+'#cue-take')
 expect(page.locator('#details-0 .take-block')).to_have_count(3)
 page.locator('#details-0 [data-take-alt="c0-t2"]').click();expect(page.locator('[data-take-alt="c0-t2"]')).to_have_text('Alt 1')
 page.locator('#details-0 [data-stars="5"][data-rating-key="c0-t1"]').click()
 page.locator('[data-rating-filter]').select_option('5');expect(page.locator('#details-0 .take-block')).to_have_count(2)
 page.locator('[data-rating-filter]').select_option('0')
 page.locator('[data-take-best="c0-t1"]').click();expect(page.locator('#details-0 .best[aria-pressed="true"]')).to_have_count(1)
 page.locator('#details-0 [data-toggle-take="c0-t1"]').click();field=page.locator('#details-0 [data-draft="c0-t1"]');field.fill('Eén gedeeld take-component');field.press('Enter')
 expect(page.locator('#details-0 [data-notes-for="c0-t1"]')).to_contain_text('Eén gedeeld take-component')
 page.goto(URL+'#notities');expect(page.locator('#main-panel .start-notes')).to_be_visible()
 field=page.locator('#details-0 [data-draft="c0-t2"]');field.fill('Notities in bestaande opnameweergave');field.press('Enter')
 expect(page.locator('#main-panel [data-notes-for="c0-t2"]')).to_contain_text('Notities in bestaande opnameweergave')
 page.locator('[data-variant="B"]').click();expect(page.locator('#main-panel')).to_have_count(1)
 expect(page.locator('#details-0 .take-summary-row')).to_have_count(1)
 page.keyboard.press('Meta+Enter')
 page.goto(URL+'#planning');expect(page.locator('#main-panel .schedule-focus')).to_contain_text('+2 min')
 page.locator('.planning-adjust>summary').click();page.locator('[data-extra="faster"]').click()
 expect(page.locator('.schedule-focus')).to_contain_text('+1 min')
 page.locator('[data-planning="remaining"]').fill('132');page.locator('[data-planning="remaining"]').press('Tab')
 expect(page.locator('.schedule-focus')).to_contain_text('−6 min')
 page.locator('.source-cue-plan [data-session-cue="1"]').click();expect(page.locator('.main-cue')).to_contain_text('1M18')
 page.screenshot(path=str(ROOT/'checks/20-gedeelde-opnameweergave.png'))
 page.goto(URL+'#partituur');page.locator('[data-score-new-take]').click()
 def cell(m,i='vln1',p=1):return page.locator(f'.score-paper[data-score-page="{p}"] [data-score-measure="{m}"][data-score-instrument="{i}"]')
 def keys():return page.evaluate('scoreSelection(state(),takeById(state(),state().selected))')
 cell(2).click(modifiers=['Meta']);assert keys()==['2:vln1','2:vln2','2:vla','2:vc']
 expect(page.locator('#score-comment-dialog')).to_have_count(0)
 cell(2).click(button='right',modifiers=['Meta']);assert keys()==[]
 cell(3,'vc').click(modifiers=['Meta','Shift']);assert len(keys())==4
 cell(3,'vln2').click(button='right',modifiers=['Meta','Shift']);assert not keys()
 cell(4,'vla').dblclick();expect(page.locator('#score-comment-dialog')).to_be_visible()
 page.locator('#score-comment-text').fill('Note op de klikplek');page.locator('#score-comment-text').press('Enter')
 card=page.locator('.score-text-annotation').filter(has_text='Note op de klikplek')
 expect(card).to_have_count(1)
 paper=page.locator('.score-paper').first
 assert card.evaluate('el=>el.children.length')==0
 assert card.evaluate('el=>getComputedStyle(el).borderTopWidth')=='0px'
 assert card.bounding_box()['y']>paper.bounding_box()['y']
 color=page.locator('[data-select-take="c0-t3"]').evaluate('el=>el.style.getPropertyValue("--take-color")')
 card.click();expect(page.locator('#score-comment-dialog')).to_be_visible()
 page.locator('#score-comment-text').fill('Bewerkte comment');page.locator('#score-comment-text').press('Enter')
 expect(page.locator('.score-text-annotation').filter(has_text='Bewerkte comment')).to_have_count(1)
 page.locator('[data-score-undo]').click();expect(page.locator('.score-text-annotation').filter(has_text='Note op de klikplek')).to_have_count(1)
 cell(5).dblclick();page.locator('#score-comment-text').fill('Concept blijft bij take drie')
 page.locator('[data-score-new-take]').click();expect(page.locator('.score-text-annotation')).to_have_count(0)
 expect(page.locator('#score-comment-dialog')).to_have_count(0)
 other=page.locator('[data-select-take="c0-t4"]').evaluate('el=>el.style.getPropertyValue("--take-color")');assert color!=other
 cell(2).click(modifiers=['Meta']);assert keys()==['2:vln1','2:vln2','2:vla','2:vc']
 page.locator('[data-select-take="c0-t3"]').click()
 expect(page.locator('#score-comment-text')).to_have_value('Concept blijft bij take drie')
 page.locator('#score-comment-text').press('Enter')
 expect(page.locator('.score-text-annotation')).to_have_count(2)
 assert not keys()
 page.locator('[data-select-take="c0-t4"]').click();assert keys()==['2:vln1','2:vln2','2:vla','2:vc']
 expect(page.locator('.score-text-annotation')).to_have_count(0)
 page.locator('[data-select-take="c0-t3"]').click();page.locator('.score-sheet').first.scroll_into_view_if_needed()
 page.screenshot(path=str(ROOT/'checks/21-comments-takekleur.png'))
 first=page.locator('.score-text-annotation').first;first.click();noteid=page.evaluate('state().scoreComment.editId')
 page.locator(f'[data-delete-note="{noteid}"]').click();expect(page.locator('#score-comment-dialog')).to_have_count(0)
 cell(7).dblclick(position={'x':8,'y':8});expect(page.locator('#score-comment-dialog')).to_be_visible();page.locator('#score-comment-text').press('Escape')
 page.set_viewport_size({'width':390,'height':844})
 for id in ['cue-take','bediening','notities','planning','partituur']:
  page.goto(URL+'#'+id);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),id
 assert not errors,errors
 assert not network,network
 b.close()
print('PASS: shared recording components, common take state, stars/Alt/notes/planning, Cmd clicks, plain score text at the click position, edit/undo, take-specific drafts and mobile offline layouts')
