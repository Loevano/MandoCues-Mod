"""Continuous score zoom preserves layers, reading position and editing coordinates."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1100})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri()+'#cutlist')
    page.locator('[data-tour-action="welcome-skip"]').click()
    page.wait_for_function('Array.from(document.querySelectorAll(".production-score-image")).every(i=>i.complete&&i.naturalWidth)')
    expect(page.locator('.cutlist-how,.cutlist-mapping-hint')).to_have_count(0)
    assert page.locator('.score-paper').count()==page.evaluate('state().doc.pages')
    canvas=page.locator('.score-canvas')
    assert canvas.bounding_box()['height']>700
    assert canvas.bounding_box()['y']+canvas.bounding_box()['height']<=1100
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('[data-score-new-take]').click()
    owner=page.evaluate('state().selected')
    cell=lambda bar:page.locator(f'[data-score-page="1"] [data-score-cell="{bar}:vln2"]')
    cell(2).click(modifiers=['Meta'])
    cell(3).dblclick()
    page.locator('#score-comment-text').fill('Zoom keeps this note here')
    page.locator('#score-comment-text').press('Enter')
    note=page.locator('.score-text-annotation').filter(has_text='Zoom keeps this note here')
    def layers():
        return page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,selection:scoreSelection(state(),t)}))')
    saved=layers()
    paper=page.locator('[data-score-page="1"]')
    base=paper.bounding_box()['width']
    canvas.evaluate('(el)=>{el.scrollTop=400}')
    def center():
        return page.evaluate('''()=>{
            const c=document.querySelector('.score-canvas'),r=c.getBoundingClientRect(),cy=r.top+c.clientHeight/2;
            const p=[...c.querySelectorAll('.score-paper')].find(p=>{const b=p.getBoundingClientRect();return b.top<=cy&&b.bottom>=cy});
            const b=p.getBoundingClientRect();return {page:p.dataset.scorePage,y:(cy-b.top)/b.height};
        }''')
    anchor=center()
    for percent in [125,150,175]:
        page.locator('[data-score-zoom="in"]').click()
        expect(page.locator('[data-score-zoom-value]')).to_have_text(f'{percent}%')
        assert abs(paper.bounding_box()['width']/base-percent/100)<.01
        after=center();assert after['page']==anchor['page'] and abs(after['y']-anchor['y'])<.005,(anchor,after)
        assert layers()==saved
    page.locator('[data-select-take="c0-t1"]').click()
    expect(page.locator('[data-score-zoom-value]')).to_have_text('175%')
    page.locator(f'[data-select-take="{owner}"]').click()
    for _ in range(5):page.locator('[data-score-zoom="in"]').click()
    expect(page.locator('[data-score-zoom-value]')).to_have_text('300%')
    expect(page.locator('[data-score-zoom="in"]')).to_be_disabled()
    assert canvas.evaluate('(el)=>el.scrollWidth>el.clientWidth')
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('[data-score-zoom="fit"]').click()
    expect(page.locator('[data-score-zoom-value]')).to_have_text('100%')
    assert canvas.evaluate('(el)=>el.scrollLeft')==0
    for _ in range(2):page.locator('[data-score-zoom="out"]').click()
    expect(page.locator('[data-score-zoom-value]')).to_have_text('50%')
    expect(page.locator('[data-score-zoom="out"]')).to_be_disabled()
    assert abs(paper.bounding_box()['width']/base-.5)<.01
    assert layers()==saved
    page.locator('[data-score-zoom="fit"]').click()
    page.locator('[data-score-zoom="in"]').click()
    # Selection and annotation dragging use the scaled score coordinates.
    cell(4).click(modifiers=['Meta'])
    assert page.evaluate('scoreSelection(state(),takeById(state(),state().selected)).filter(k=>k.startsWith("4:")).length')==4
    cell(4).click(button='right',modifiers=['Meta'])
    assert page.evaluate('scoreSelection(state(),takeById(state(),state().selected)).filter(k=>k.startsWith("4:")).length')==0
    note.scroll_into_view_if_needed();box=note.bounding_box()
    page.mouse.move(box['x']+5,box['y']+5);page.mouse.down()
    page.mouse.move(box['x']+45,box['y']+25,steps=8);page.mouse.up()
    moved=note.bounding_box();assert abs(moved['x']-box['x']-40)<3 and abs(moved['y']-box['y']-20)<3
    page.locator('[data-score-undo]').click()
    assert layers()==saved
    # The cut list is always expanded; navigation and transport share one row.
    expect(page.locator('.site-header')).to_be_hidden()
    expect(page.locator('[data-score-expand]')).to_have_count(0)
    expect(page.locator('.cutlist-sidebar')).to_be_visible()
    expect(page.locator('[data-proposal-action="tour"]')).to_be_visible()
    expect(page.locator('[data-proposal-action="prompt"]')).to_be_visible()
    assert canvas.bounding_box()['height']>900
    assert canvas.bounding_box()['y']+canvas.bounding_box()['height']<=1100
    toggle=page.locator('.proposal-view-toggle').bounding_box()
    transport=page.locator('.proposal-live-bar').bounding_box()
    assert abs(toggle['y']+toggle['height']/2-transport['y']-transport['height']/2)<3
    expect(page.locator('[data-score-zoom-value]')).to_have_text('125%')
    canvas.evaluate('(el)=>{el.scrollTop=el.scrollHeight}')
    expect(page.locator('.score-paper').last).to_be_in_viewport()
    assert page.locator('.score-take-picker').evaluate('(el)=>el.scrollTop')==0
    page.screenshot(path=str(ROOT/'checks/score-expanded.png'))
    page.keyboard.press('Escape')
    expect(page.locator('.site-header')).to_be_hidden()
    assert layers()==saved
    for width in [390,1024,1512]:
        page.set_viewport_size({'width':width,'height':1100})
        page.locator('[data-score-zoom="fit"]').click()
        page.locator('[data-score-zoom="in"]').click()
        assert canvas.bounding_box()['height']>450,width
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
        for selector in ['[data-proposal-view="recording"]','[data-proposal-view="cutlist"]','.proposal-live-bar .record','[data-proposal-action="tour"]']:
            box=page.locator(selector).bounding_box()
            assert box['x']>=0 and box['x']+box['width']<=width,(width,selector,box)
    # Switching back restores review actions and the main recording panel.
    page.locator('[data-proposal-view="recording"]').click()
    expect(page.locator('.site-header')).to_be_visible()
    expect(page.locator('.site-header [data-proposal-action="tour"]')).to_be_visible()
    page.locator('[data-proposal-view="cutlist"]').click()
    page.locator('[data-score-zoom="fit"]').click()
    canvas.evaluate('(el)=>{el.scrollTop=0}')
    page.screenshot(path=str(ROOT/'checks/score-zoom.png'))
    assert not errors,errors
    browser.close()
print('PASS: continuous pages, viewport space, 50–300% zoom, reading anchor, shared take zoom, scaled selection/note drag, permanently expanded workspace, compact transport and responsive widths')
