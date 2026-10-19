"""Existing take labels are shared without moving the rating controls."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 field=page.locator('[data-take-label="c0-t2"]').first;tools=page.locator('[data-calm-take="c0-t2"] .take-tools');before=tools.bounding_box()
 field.fill('Strings only');page.locator('[data-take-best="c0-t2"]').click();expect(page.locator('[data-take-best="c0-t2"]')).to_have_attribute('aria-pressed','true');expect(field).to_have_value('Strings only');after=tools.bounding_box()
 assert all(abs(before[k]-after[k])<1 for k in ['x','y','width','height'])
 page.locator('[data-proposal-view="cutlist"]').click();expect(field).to_have_value('Strings only')
 field.fill('Softer opening');field.press('Tab')
 page.evaluate("state().cutlistView='all';renderDemo()");expect(field).to_have_value('Softer opening')
 expect(page.locator('.all-takes-view [data-take-label="c0-t2"]')).to_have_value('Softer opening')
 page.locator('[data-proposal-view="recording"]').click();expect(field).to_have_value('Softer opening')
 page.locator('.session-pdf-menu>summary').click();page.locator('[data-app-export="takes"]').click()
 expect(page.locator('.app-dialog')).to_contain_text('Softer opening')
 assert not errors,errors
 browser.close();print('PASS: shared take labels in Recording/PDF/All takes, take sheet export and stable stars/Best/Alt')
