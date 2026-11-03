"""Recording ranges, parked comp data and score note flows share one take model."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'prototype'))
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1000});page.set_default_timeout(10000);errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.goto((ROOT/'index.html').as_uri())
 original=page.evaluate('allTakes(state()).map(t=>({id:t.id,selections:t.scoreSelections}))')
 # Add a range without creating or renumbering a take.
 page.locator('[data-v4-range-open=next]').click();form=page.locator('#v4-range-form')
 form.locator('[name=from]').fill('12');form.locator('[name=to]').fill('8');form.locator('[type=submit]').click()
 expect(form.locator('.v4-range-error')).to_contain_text('end bar')
 form.locator('[name=from]').fill('2');form.locator('[name=to]').fill('8');form.locator('[type=submit]').click()
 assert page.evaluate('v4Ranges(state()).pending')=={'from':2,'to':8}
 assert page.evaluate('state().takes[0].length')==2
 page.locator('.proposal-workspace-title').click();page.keyboard.press('Space');assert page.evaluate('state().sessionStarted&&!running(state())')
 page.keyboard.press('Space');assert page.evaluate('running(state()).num')==3
 assert page.evaluate('running(state()).barRange')=={'from':2,'to':8}
 expect(page.locator('[data-v4-range-open=next]')).to_be_disabled()
 page.keyboard.press('Space');assert page.evaluate('!running(state())')
 page.locator('[data-v4-range-open=next]').click();form.locator('[name=from]').fill('12');form.locator('[name=to]').fill('19');form.locator('[type=submit]').click()
 page.locator('.proposal-workspace-title').click();page.keyboard.press('Space')
 assert page.evaluate('running(state()).num')==4
 assert page.evaluate('running(state()).barRange')=={'from':12,'to':19}
 assert page.evaluate('state().takes[0].find(t=>t.num===3).barRange')=={'from':2,'to':8}
 assert page.evaluate('sessionTakeLog().takes.find(t=>t.number===3&&t.cueCode==="1M02").barRange')=={'from':2,'to':8}
 live=page.evaluate('running(state()).id')
 # Changing views during a take preserves it, and only changes the view.
 page.locator('[data-proposal-view=cutlist]').click();expect(page.locator('.proposal-workspace-title')).to_have_text('Score')
 assert page.url.endswith('#score');assert page.evaluate('running(state()).id')==live
 expect(page.locator('[data-score-setting], [data-score-toggle], [data-score-clear-selection]')).to_have_count(0)
 expect(page.locator('.score-comparison-layer,.in-take-selection')).to_have_count(0)
 # Comp drag is disabled, including data changes; the old layers remain preserved.
 cell=page.locator('[data-score-cell="2:vln1"]').first;cell.scroll_into_view_if_needed();r=cell.bounding_box()
 snapshot=page.evaluate('JSON.stringify(takeById(state(),state().selected).scoreSelections||{})')
 page.keyboard.down('Meta');page.mouse.move(r['x']+2,r['y']+2);page.mouse.down();page.mouse.move(r['x']+r['width']-2,r['y']+r['height']-2,steps=5);page.mouse.up();page.keyboard.up('Meta')
 assert page.evaluate('JSON.stringify(takeById(state(),state().selected).scoreSelections||{})')==snapshot
 # Stop in Score via the same Space action.
 page.locator('[data-proposal-view=cutlist]').click();page.keyboard.press('Space');assert page.evaluate('!running(state())')
 # N selects the editor; Enter keeps the note on this take in both views.
 page.keyboard.press('n');editor=page.locator('[data-draft][data-editor-place=v4-score]');expect(editor).to_be_focused();editor.fill('Keep this entrance');editor.press('Enter')
 assert page.evaluate('takeById(state(),state().selected).notes.at(-1).text')=='Keep this entrance'
 # Double-click mapped bar 5 creates a positioned score note with the correct bar.
 cell=page.locator('[data-score-cell="5:vln1"]').first;cell.dblclick()
 expect(page.locator('#score-comment-text')).to_be_visible()
 expect(page.locator('#score-comment-measure')).to_have_value('5')
 page.locator('#score-comment-text').fill('Softer here');page.locator('#score-comment-text').press('Enter')
 expect(page.locator('.score-note-text').filter(has_text='Softer here')).to_be_visible()
 page.locator('.score-note-text').filter(has_text='Softer here').click();page.keyboard.press('Backspace')
 assert not page.evaluate('takeById(state(),state().selected).notes.some(n=>n.text==="Softer here")')
 page.keyboard.press('Meta+z')
 assert page.evaluate('takeById(state(),state().selected).notes.some(n=>n.text==="Softer here")')
 page.locator('[data-proposal-view=recording]').click();expect(page.locator('.calm-notes')).to_contain_text('Keep this entrance')
 assert page.evaluate('allTakes(state()).filter(t=>t.num<3).map(t=>({id:t.id,selections:t.scoreSelections}))')==original
 # Global score zoom survives cue changes and view switches.
 page.locator('[data-proposal-view=cutlist]').click();page.locator('[data-score-zoom=in]').click();zoom=page.evaluate('state().zoom')
 page.locator('[data-proposal-view=cutlist]').click();page.keyboard.press('BracketRight')
 assert page.evaluate('state().cue')==1;assert page.evaluate('state().zoom')==zoom
 page.locator('[data-proposal-view=recording]').click();assert page.evaluate('state().zoom')==zoom
 for width in [1512,900,390]:
  page.set_viewport_size({'width':width,'height':1000})
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  page.screenshot(path=str(ROOT/f'check-recording-{width}.png'))
  page.locator('[data-proposal-view=cutlist]').click()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  page.screenshot(path=str(ROOT/f'check-score-{width}.png'))
  page.locator('[data-proposal-view=recording]').click()
 assert not errors,errors
 browser.close()
print('PASS bar-range numbering, shared recording/score notes, parked comp layers, annotation/delete/undo, shortcuts, zoom and responsive widths')
