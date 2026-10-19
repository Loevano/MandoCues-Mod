"""Mac-style individual and range comparison keeps the same editable take and data."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
 page.evaluate("state().takes[0].push(newTake(0,3),newTake(0,4));showProposalView('cutlist')")
 original=page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,selection:t.scoreSelections}))')
 def ids():return page.evaluate('scoreVisibleTakes(state()).map(t=>t.id)')
 for matrix in [False,True]:
  page.evaluate('(all)=>{state().cutlistView=all?"all":"score";renderDemo()}',matrix)
  attr='data-cutlist-take' if matrix else 'data-select-take'
  def click(n,modifiers=[]):page.locator(f'[{attr}="c0-t{n}"]').click(modifiers=modifiers)
  click(1);click(4,['Shift']);assert set(ids())=={f'c0-t{n}' for n in range(1,5)}
  assert page.evaluate('state().selected')=='c0-t4'
  click(2,['Shift']);assert ids()==['c0-t2','c0-t1'] or set(ids())=={'c0-t1','c0-t2'}
  click(4,['Meta']);assert set(ids())=={'c0-t1','c0-t2','c0-t4'}
  click(3,['Shift']);assert set(ids())=={'c0-t3','c0-t4'}
  click(1,['Meta','Shift']);assert set(ids())=={f'c0-t{n}' for n in range(1,5)}
  click(2);assert ids()==['c0-t2']
 assert page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,selection:t.scoreSelections}))')==original
 assert not errors,errors
 browser.close();print('PASS: plain/Command/Shift/Command+Shift comparison, stable range anchor, primary layer, PDF and All takes, unchanged notes and selections')
