"""Deleting a stopped take is explicit, isolated and never reuses its number."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100});page.clock.install();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 original=page.evaluate('takeById(state(),"c0-t1")')
 page.locator('[data-delete-take="c0-t2"]').click();expect(page.locator('.app-dialog')).to_contain_text('bar selections')
 page.locator('.app-dialog [data-app-dialog-close]').first.click();assert page.evaluate('state().takes[0].length')==2
 page.locator('[data-delete-take="c0-t2"]').click();page.locator('[data-confirm-delete-take]').click()
 assert page.evaluate('state().selected')=='c0-t1'
 assert page.evaluate('takeById(state(),"c0-t1")')==original
 assert page.evaluate('nextEntryNumber(state(),0)')==3
 page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
 assert page.evaluate('running(state()).id')=='c0-t3'
 expect(page.locator('[data-delete-take="c0-t3"]')).to_be_disabled()
 page.evaluate('deleteProposalTake(state(),"c0-t3")');assert page.evaluate('running(state()).id')=='c0-t3'
 page.keyboard.press('Meta+Enter');page.locator('[data-proposal-view="cutlist"]').click()
 page.evaluate("state().cutlistView='all';renderDemo()")
 page.locator('.all-takes-view [data-delete-take="c0-t3"]').click();page.locator('[data-confirm-delete-take]').click()
 assert page.evaluate('nextEntryNumber(state(),0)')==4
 page.locator('.score-take-picker [data-delete-take="c0-t1"]').click();page.locator('[data-confirm-delete-take]').click()
 assert page.evaluate('state().selected===null&&state().takes[0].length===0')
 page.evaluate('newEmptyScoreTake(state())');assert page.evaluate('state().selected')=='c0-t4'
 assert page.evaluate('state().takes[1].length')==2
 assert not errors,errors
 browser.close();print('PASS: confirmation/cancel, isolated deletion, protected rolling take, PDF and All takes, deleting last take and non-reused numbering')
