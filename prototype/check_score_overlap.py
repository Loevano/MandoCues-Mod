"""Overlapping takes stay independent, readable and visible through comparison modes."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri()+'#cutlist');page.locator('[data-tour-action="welcome-skip"]').click()
    page.locator('[data-select-take="c0-t2"]').click()
    def selection(take):return page.evaluate('(id)=>scoreSelection(state(),takeById(state(),id))',take)
    first=selection('c0-t1')
    cell=page.locator('[data-score-page="1"] [data-score-cell="4:vln1"]')
    cell.click(modifiers=['Meta'])
    assert selection('c0-t1')==first
    assert len([k for k in selection('c0-t2') if k.startswith('4:')])==4
    overlay=page.locator('[data-score-page="1"] .score-cut-range[data-cut-measure="4"]')
    expect(overlay).to_have_class(__import__('re').compile('has-overlap'))
    assert set(overlay.get_attribute('data-cut-takes').split())=={'c0-t1','c0-t2'}
    expect(overlay.locator('.score-take-band')).to_have_count(2)
    colours=overlay.locator('.score-take-band').evaluate_all('(els)=>els.map(el=>getComputedStyle(el).borderTopColor)')
    assert colours[0]!=colours[1]
    assert 'repeating-linear-gradient' in overlay.evaluate('(el)=>getComputedStyle(el).backgroundImage')
    expect(overlay.locator('[data-range-take="c0-t1"]')).to_have_class(__import__('re').compile('is-reference'))
    # Hidden references leave the layers intact; explicit comparisons remain visible.
    page.get_by_role('button',name='See other takes',exact=True).click()
    assert overlay.get_attribute('data-cut-takes')=='c0-t2'
    assert selection('c0-t1')==first
    page.locator('[data-select-take="c0-t1"]').click(modifiers=['Meta'])
    assert set(overlay.get_attribute('data-cut-takes').split())=={'c0-t1','c0-t2'}
    page.locator('[data-select-take="c0-t2"]').click()
    cell.click(button='right',modifiers=['Meta'])
    assert selection('c0-t1')==first
    assert not any(k.startswith('4:') for k in selection('c0-t2'))
    page.locator('[data-score-undo]').click()
    assert len([k for k in selection('c0-t2') if k.startswith('4:')])==4
    assert selection('c0-t1')==first
    page.get_by_role('button',name='See other takes',exact=True).click()
    expect(overlay.locator('.score-take-band')).to_have_count(2)
    # Hovering selection cells still never paints an opaque black box.
    cell.hover();assert cell.evaluate('(el)=>getComputedStyle(el).backgroundColor')=='rgba(0, 0, 0, 0)'
    page.screenshot(path=str(ROOT/'checks/score-overlap.png'))
    assert not errors,errors
    browser.close()
print('PASS: independent overlapping selections, visible reference/compared colours, overlap hatching, visibility toggles, remove/undo isolation and transparent cell hover')
