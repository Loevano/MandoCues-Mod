"""Review variants share notes/live state; Space is manual only outside text input."""
from pathlib import Path
import sys,hashlib
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'prototype'))
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':982});page.clock.install()
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'index.html').as_uri());expect(page.locator('#proposal-welcome')).to_have_count(0)
 expect(page.locator('[data-review-layout="A"]')).to_have_attribute('aria-pressed','true')
 original=page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes}))')
 field=page.locator('[data-draft="c0-t2"]');field.fill('A draft with spaces')
 page.locator('[data-review-layout="B"]').click()
 expect(page.locator('[data-draft="c0-t2"]')).to_have_value('A draft with spaces')
 expect(page.locator('.v3-active-take-buttons')).to_be_visible()
 page.locator('[data-review-history]').click()
 expect(page.locator('.v3-history-list')).to_contain_text('Nice entrance; keep this.')
 # Existing notes in an older take remain explicitly owned by that take.
 page.locator('.v3-history-list [data-select-take="c0-t1"]').click()
 expect(page.locator('.calm-notes>header')).to_contain_text('Take 1')
 assert page.evaluate('takeById(state(),"c0-t2").draft.text')=='A draft with spaces'
 for width in [1512,1366,1024,900,390]:
  page.set_viewport_size({'width':width,'height':900 if width!=1366 else 768})
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  if width>=900:
   field=page.locator('.calm-notes textarea[data-draft]');box=field.bounding_box();record=page.locator('#main-panel .record').bounding_box()
   assert 0<box['y']<page.viewport_size['height']-70,(width,box)
   assert record['y']+record['height']<page.viewport_size['height'],(width,record)
  page.screenshot(path=str(ROOT/f'check-B-{width}.png'))
 page.set_viewport_size({'width':1512,'height':982})
 # Plain text Space cannot start a take. Nonempty text clock remains frozen.
 field=page.locator('.calm-notes textarea[data-draft]');field.fill('Note');field.press('Space')
 assert page.evaluate('!state().sessionStarted&&!running(state())')
 expect(field).to_have_value('Note ')
 page.locator('.v3-review-caption').click();page.keyboard.press('Space')
 assert page.evaluate('state().sessionStarted&&!running(state())')
 page.keyboard.press('Space')
 live=page.evaluate('running(state())?.id');assert live
 assert page.evaluate('state().sessionStarted')
 page.clock.run_for(1200)
 page.locator('[data-review-layout="A"]').click();assert page.evaluate('running(state()).id')==live
 page.locator('[data-review-layout="B"]').click();assert page.evaluate('running(state()).id')==live
 page.locator('.v3-review-caption').click();page.keyboard.press('Space');assert page.evaluate('!running(state())')
 # Space must not activate record while a dialog or form control has focus.
 page.locator('.v3-more-timing>summary').click()
 page.locator('.v3-active-take-buttons [data-select-take="c0-t1"]').click()
 expect(page.locator('.v3-more-timing')).to_have_attribute('open','')
 page.locator('[data-review-decision]').click();page.locator('#v3-layout-decision').focus();page.keyboard.press('Space');assert page.evaluate('!running(state())')
 page.locator('[data-review-prefer="B"]').click()
 page.locator('.calm-notes [data-draft]').fill('Saved after review');page.locator('.calm-notes [data-draft]').press('Enter')
 expect(page.locator('.calm-notes .note-list')).to_contain_text('Saved after review')
 page.locator('[data-review-layout="A"]').click();expect(page.locator('.calm-notes .note-list')).to_contain_text('Saved after review')
 # The review layer must not modify or lose the initial note records.
 current=page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes}))')
 for old in original:
  owner=next(t for t in current if t['id']==old['id'])
  assert owner['notes'][:len(old['notes'])]==old['notes']
 # A cue switch follows the new cue without stale notes; Comp tool shares the stopped take.
 page.locator('#main-panel [data-action="next-cue"]').click()
 assert page.evaluate('state().cue')==1
 page.locator('[data-review-layout="B"]').click()
 expect(page.locator('.v3-active-takes>header')).to_contain_text('1M18')
 page.locator('[data-proposal-view="cutlist"]').click()
 expect(page.locator('#score-cue')).to_have_value('1')
 page.locator('[data-proposal-view="recording"]').click()
 # Holding Space cannot create multiple takes; typing/modifiers and dialogs stay protected.
 page.locator('.v3-review-caption').click();page.keyboard.down('Space')
 held=page.evaluate('running(state()).id')
 page.keyboard.down('Space');assert page.evaluate('running(state()).id')==held
 page.keyboard.up('Space');page.keyboard.press('Space');assert page.evaluate('!running(state())')
 assert not errors,errors
 browser.close()
print('PASS v3 A/B draft, saved note and live-take preservation, cue history, Space guards, viewport width and input reachability')
