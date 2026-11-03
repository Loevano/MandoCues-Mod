"""Only cue ordering and the confirmed Space shortcut extend the v2 layout."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'prototype'))
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 browser=launch_chromium(p);context=browser.new_context(viewport={'width':1512,'height':1000});page=context.new_page();page.clock.install();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 expect(page.locator('.v3-review-toolbar,.v3-cue-workspace,.v3-clock-settings,.v3-reference-score,.v3-planner')).to_have_count(0)
 expect(page.locator('.main-session-times label')).to_have_count(4)
 expect(page.locator('[data-review-drag-cue]')).to_have_count(26)
 expect(page.locator('.calm-notes')).to_have_count(1)
 # The original controls and note pane retain their positions.
 base=context.new_page();base.goto((ROOT.parent/'prototype/dist/index.html').as_uri());base.locator('[data-tour-action="welcome-skip"]').click()
 for selector in ['#main-panel','.calm-notes']:
  assert page.locator(selector).bounding_box()==base.locator(selector).bounding_box(),selector
 a=page.locator('.calm-content').bounding_box();b=base.locator('.calm-content').bounding_box()
 assert all(a[k]==b[k] for k in ['x','y','width']),(a,b)
 base.close()
 original=page.evaluate('({cueCodes:cues.map(c=>c[0]),takes:allTakes(state()).map(t=>({id:t.id,notes:t.notes})),cueNotes:state().cueNotes})')
 # Keyboard reorder is also available on the drag grip, without changing take/note IDs.
 handle=page.locator('[data-review-drag-cue="0"]');handle.focus();handle.press('ArrowDown')
 assert page.evaluate('reviewRecordingOrder(state()).slice(0,2)')==[1,0]
 page.locator('[data-review-drag-cue="0"]').drag_to(page.locator('[data-review-cue-key="1"]'))
 assert page.evaluate('reviewRecordingOrder(state()).slice(0,2)')==[0,1]
 assert page.evaluate('({cueCodes:cues.map(c=>c[0]),takes:allTakes(state()).map(t=>({id:t.id,notes:t.notes})),cueNotes:state().cueNotes})')==original
 page.locator('[data-review-cue-sort]').select_option('cue')
 expect(page.locator('[data-review-drag-cue="0"]')).to_have_attribute('aria-disabled','true')
 page.locator('[data-review-cue-sort]').select_option('recording')
 # First Space starts just the session. Typing does not change transport.
 page.locator('.proposal-workspace-title').click();page.keyboard.press('Space')
 assert page.evaluate('state().sessionStarted&&!running(state())')
 editor=page.locator('.calm-notes [data-draft]');editor.fill('Keep this');editor.press('Space')
 expect(editor).to_have_value('Keep this ');assert page.evaluate('!running(state())')
 page.locator('.proposal-workspace-title').click();page.keyboard.press('Space');assert page.evaluate('!!running(state())')
 expect(page.locator('[data-review-drag-cue="0"]')).to_have_attribute('aria-disabled','true')
 page.keyboard.press('Space');assert page.evaluate('!running(state())')
 # Existing Comp tool remains the original score view.
 page.locator('[data-proposal-view="cutlist"]').click();expect(page.locator('.score-canvas')).to_be_visible()
 expect(page.locator('.v3-reference-score')).to_have_count(0)
 page.locator('[data-proposal-view="recording"]').click()
 for width in [1512,900,390]:
  page.set_viewport_size({'width':width,'height':1000})
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  page.screenshot(path=str(ROOT/f'check-minimal-{width}.png'))
 assert not errors,errors
 browser.close()
print('PASS original layout geometry, notes/IDs retained, pointer/keyboard cue reordering, separate sorting, protected Space transport and original Comp tool')
