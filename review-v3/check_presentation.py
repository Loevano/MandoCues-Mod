"""Exercise the presentation edits without changing the preserved v2 app."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'prototype'))
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright,expect

with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1000});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.clock.install();page.goto((ROOT/'index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 editor=page.locator('.calm-notes [data-draft]')
 # First letter freezes the original instant, even if all text is removed.
 editor.fill('Cello');anchor=page.evaluate('takeById(state(),state().selected).draft.writtenAt')
 assert anchor is not None
 page.clock.run_for(5000);editor.fill('');page.clock.run_for(5000);editor.fill('Calmer cello')
 assert page.evaluate('takeById(state(),state().selected).draft.writtenAt')==anchor
 now=page.locator('.calm-notes [data-reset-note-time="draft"]');now.click()
 assert page.evaluate('takeById(state(),state().selected).draft.clockAt')>anchor
 page.locator('.calm-notes [data-restore-note-time="draft"]').click()
 assert page.evaluate('takeById(state(),state().selected).draft.clockAt')==anchor
 # Save carries the original anchor; current-time and restore remain independent.
 editor.press('Enter');note=page.evaluate('takeById(state(),state().selected).notes.at(-1)')
 assert note['writtenAt']==anchor
 page.locator(f'.calm-notes [data-reset-note-time="{note["id"]}"]').click()
 page.locator(f'.calm-notes [data-restore-note-time="{note["id"]}"]').click()
 assert page.evaluate('takeById(state(),state().selected).notes.at(-1).clockAt')==anchor
 assert page.evaluate('takeById(state(),state().selected).draft.clockAt') is None
 # N focuses the existing draft without replacing it or becoming typed content.
 page.locator('.proposal-workspace-title').click();page.keyboard.press('n')
 expect(editor).to_be_focused();expect(editor).to_have_value('')
 n_anchor=page.evaluate('takeById(state(),state().selected).draft.writtenAt')
 page.clock.run_for(5000);editor.fill('Keep this draft')
 page.locator('.proposal-workspace-title').click();page.keyboard.press('n')
 expect(editor).to_have_value('Keep this draft')
 assert page.evaluate('takeById(state(),state().selected).draft.writtenAt')==n_anchor
 editor.press('n');expect(editor).to_have_value('Keep this draftn')
 assert not errors,errors
 browser.close()
print('PASS first-letter and N anchors, clearing drafts, independent NOW/restore before and after Enter')
