"""Existing recording context remains recognizable without depending on the live site."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 expect(page.locator('.app-sidebar [aria-current="page"]')).to_have_text('Recording')
 expect(page.locator('[data-session-setting="length"]')).to_have_value('360')
 expect(page.locator('[data-session-hours]')).to_have_text('6h 00m')
 expect(page.locator('.session-chat')).to_have_count(0)
 page.locator('[data-app-action="chat"]').click();expect(page.locator('.session-chat')).to_be_visible()
 page.locator('.session-chat textarea').fill('Local demo message');page.locator('.session-chat button').last.click()
 expect(page.locator('.session-chat-messages')).to_contain_text('Local demo message')
 page.locator('.session-chat [data-app-action="chat"]').click();expect(page.locator('.session-chat')).to_have_count(0)
 page.locator('.session-pdf-menu summary').click();page.locator('[data-app-export="order"]').click()
 expect(page.locator('.session-export-preview tbody tr')).to_have_count(26)
 page.locator('.app-dialog [data-app-dialog-close]').first.click()
 page.locator('[data-app-action="add-cues"]').click()
 before=page.evaluate('state().sessionStarted');page.keyboard.press('Meta+Enter');assert page.evaluate('state().sessionStarted')==before
 expect(page.locator('[data-add-session-cue]')).to_have_count(7)
 page.locator('[data-add-session-cue="1M04"]').check();page.locator('[data-app-action="confirm-cues"]').click()
 expect(page.locator('.calm-cue-list')).to_contain_text('Pool Flashback')
 page.evaluate('selectCue(state(),26)');page.locator('[data-proposal-view="cutlist"]').click()
 expect(page.locator('.unlinked-score')).to_have_text('No score linked for this cue.')
 for width in [390,900,1512]:
  page.set_viewport_size({'width':width,'height':1100})
  for view in ['recording','cutlist']:
   page.locator(f'[data-proposal-view="{view}"]').click()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,view)
 assert not errors,errors
 browser.close()
print('PASS: sidebar/session context, units, initially closed local chat, PDF views, add cues, missing score and responsive width')
