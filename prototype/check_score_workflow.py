from browser_support import launch_chromium
"""Score-first alternative reuses the cut-list layers and keeps live work separate from browsing."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent
errors=[]
with sync_playwright() as p:
 b=launch_chromium(p)
 page=b.new_page(viewport={'width':1512,'height':1100})
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri()+'#partituur')
 expect(page.locator('.score-session-dock')).to_have_count(0)
 page.locator('[data-variant="B"]').click()
 expect(page.locator('.score-session-dock')).to_be_visible()
 expect(page.locator('.score-first-stage .production-score-image')).to_have_count(3)
 seed=page.evaluate('JSON.stringify(state().takes.map(ts=>ts.map(t=>({id:t.id,notes:t.notes,rating:t.rating,best:t.best,text:t.draft.text}))))')
 page.locator('[data-variant="A"]').click();assert page.evaluate('JSON.stringify(state().takes.map(ts=>ts.map(t=>({id:t.id,notes:t.notes,rating:t.rating,best:t.best,text:t.draft.text}))))')==seed
 page.locator('[data-variant="B"]').click()
 page.locator('.score-session-actions [data-action="record"]').click()
 assert page.evaluate('running(state()).id')=='c0-t3'
 expect(page.locator('.score-session-active')).to_contain_text('Take 3')
 expect(page.locator('.score-text-annotation')).to_have_count(0)
 cell=page.locator('.score-paper[data-score-page="1"] [data-score-measure="2"][data-score-instrument="vc"]')
 cell.click(modifiers=['Meta']);assert page.evaluate('scoreSelection(state(),takeById(state(),state().selected))')==['2:vln1','2:vln2','2:vla','2:vc']
 cell.dblclick();page.locator('#score-comment-text').fill('Note vanuit de partituurwerkplek');page.locator('#score-comment-text').press('Enter')
 expect(page.locator('.score-text-annotation')).to_contain_text('Note vanuit de partituurwerkplek')
 expect(page.locator('.cutlist-notes-list')).to_contain_text('Note vanuit de partituurwerkplek')
 page.locator('[data-select-take="c0-t1"]').click()
 assert page.evaluate('state().selected')=='c0-t1'
 assert page.evaluate('running(state()).id')=='c0-t3'
 expect(page.locator('.score-session-active')).to_contain_text('Take 3')
 expect(page.locator('.score-viewing-other')).to_contain_text('Viewing Take 1')
 expect(page.locator('.score-text-annotation').filter(has_text='Note vanuit de partituurwerkplek')).to_have_count(0)
 page.locator('[data-select-take="c0-t3"]').click()
 expect(page.locator('.score-text-annotation')).to_contain_text('Note vanuit de partituurwerkplek')
 page.locator('.score-session-details>summary').click()
 page.locator('[data-score-workflow-later]').click();page.locator('[data-score-workflow-later]').click()
 expect(page.locator('[data-score-workflow-reminder]')).to_contain_text('over budget')
 expect(page.locator('[data-score-workflow-plan]')).to_contain_text('behind')
 page.keyboard.press('Meta+Enter');assert page.evaluate('!running(state())')
 page.locator('.score-session-details>summary').click()
 page.locator('[data-score-page="2"] [data-score-measure]').first.scroll_into_view_if_needed()
 expect(page.locator('.score-session-dock')).to_be_in_viewport()
 page.locator('#score-cue').select_option('1')
 expect(page.locator('.score-session-dock header')).to_contain_text('1M18')
 page.locator('#score-cue').select_option('0')
 assert page.evaluate('scoreWorkflowTiming(state()).cueElapsed')>=12*60
 page.locator('.score-session-dock').scroll_into_view_if_needed()
 page.screenshot(path=str(ROOT/'checks/23-partituur-als-werkplek.png'))
 page.locator('[data-variant="A"]').click()
 expect(page.locator('.score-text-annotation')).to_contain_text('Note vanuit de partituurwerkplek')
 page.locator('[data-variant="B"]').click()
 cell=page.locator('.score-paper[data-score-page="1"] [data-score-measure="3"][data-score-instrument="vln1"]')
 cell.dblclick();page.locator('#score-comment-text').fill('Concept tussen indelingen')
 page.locator('[data-variant="A"]').click();expect(page.locator('#score-comment-text')).to_have_value('Concept tussen indelingen')
 page.locator('[data-variant="B"]').click();expect(page.locator('#score-comment-text')).to_have_value('Concept tussen indelingen')
 page.locator('#score-comment-text').press('Escape')
 for width in [1100,800,390]:
  page.set_viewport_size({'width':width,'height':844})
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  expect(page.locator('.cutlist-notes-list')).to_be_visible()
 page.goto((ROOT/'dist/index.html').as_uri()+'#voor-claude')
 page.locator('[data-implementation-choice="idea:partituur"]').check()
 page.locator('[data-implementation-variant="idea:partituur"]').select_option('B')
 assert page.evaluate('combinedPrompt().includes(ideas.find(i=>i.id==="partituur").variants.B)')
 assert not page.evaluate('combinedPrompt().includes(ideas.find(i=>i.id==="partituur").variants.A)')
 expected=(ROOT/'dist/04-prompt-B.txt').read_text()
 assert page.evaluate('promptFor(ideas.find(i=>i.id==="partituur"),"B")')==expected
 assert not errors,errors
 b.close()
print('PASS: 04B score workflow, shared layers and concepts, clean new live take, notes/selection, browsing during recording, independent cue time, planning/reminder, stop shortcut, cue resume and responsive layout')
