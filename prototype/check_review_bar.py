"""Proposal controls stay above, separated from the proposed application."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 for width in [1512,390]:
  page.set_viewport_size({'width':width,'height':1100})
  for view in ['recording','cutlist','recording']:
   page.locator(f'[data-proposal-view="{view}"]').click()
   expect(page.locator('body>.site-header [data-proposal-action="tour"]')).to_be_in_viewport()
   expect(page.locator('#app [data-proposal-action]')).to_have_count(0)
   assert page.locator('.site-header').count()==1
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 browser.close()
print('PASS: separate compact review bar above both workspaces, rerenders and responsive width')
