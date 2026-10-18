"""Placing and dragging notes above a bar infers the bar and staff scope."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1100})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri()+'#cutlist')
    page.locator('[data-tour-action="welcome-skip"]').click()
    page.wait_for_function('Array.from(document.querySelectorAll(".production-score-image")).every(i=>i.complete&&i.naturalWidth)')
    page.locator('[data-score-new-take]').click()
    def point(bar,instrument=None):
        return page.evaluate('''({bar,instrument})=>{
            const s=state(),r=scoreRegions(s,1).find(r=>r.measure===bar),p=document.querySelector('[data-score-page="1"]').getBoundingClientRect();
            const cell=scoreCells(s,1).find(c=>c.measure===bar&&c.instrument===instrument);
            const y=instrument?cell.y+cell.height*.2:r.y-.02;
            return {x:p.left+(r.x+r.width*.25)*p.width,y:p.top+y*p.height};
        }''',{'bar':bar,'instrument':instrument})
    def saved():return page.evaluate('takeById(state(),state().selected).notes.at(-1)')
    def drag_to(target):
        note=page.locator('.score-text-annotation').filter(has_text='Position determines bar')
        note.scroll_into_view_if_needed();b=note.bounding_box()
        page.mouse.move(b['x']+3,b['y']+3);page.mouse.down()
        page.mouse.move(target['x']+3,target['y']+3,steps=8)
        expect(page.locator('.score-note-bar-preview:not([hidden])')).to_have_attribute('data-bar','6')
        page.mouse.up()
        expect(page.locator('.score-note-bar-preview:not([hidden])')).to_have_count(0)
    a=point(5)
    page.mouse.dblclick(a['x'],a['y'])
    expect(page.locator('#score-comment-measure')).to_have_value('5')
    expect(page.locator('#score-comment-instrument')).to_have_value('all')
    page.locator('#score-comment-text').fill('Position determines bar')
    page.locator('#score-comment-text').press('Enter')
    original=saved();assert original['measure']==5 and len(original['instruments'])==4
    drag_to(point(6,'vln2'))
    moved=saved();assert moved['measure']==6 and moved['instruments']==['vln2'],moved
    assert moved['at']==original['at'] and moved['originalAt']==original['originalAt']
    assert moved['page']==1 and moved['bookPage']==7
    page.keyboard.press('Meta+z');assert saved()==original
    page.keyboard.press('Meta+Shift+z');assert saved()==moved
    drag_to(point(6))
    assert saved()['instruments']==['vln1','vln2','vla','vc']
    # A separate double click above bar 6 still resolves that bar at 150% zoom.
    page.locator('[data-score-zoom="in"]').click();page.locator('[data-score-zoom="in"]').click()
    page.locator('.score-canvas').evaluate('(el)=>{el.scrollTop=0;el.scrollLeft=0}')
    page.locator('[data-score-page="1"] [data-score-cell="6:vc"]').scroll_into_view_if_needed()
    a=point(6,'vc')
    page.mouse.dblclick(a['x'],a['y'])
    expect(page.locator('#score-comment-measure')).to_have_value('6')
    expect(page.locator('#score-comment-instrument')).to_have_value('vc')
    assert not errors,errors
    browser.close()
print('PASS: clicks above bars 5/6, instrument/all scope, drag highlight and reassignment, immutable timestamp, undo/redo and zoom coordinates')
