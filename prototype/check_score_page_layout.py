"""Preview-style spreads, paged navigation and global zoom preserve editing layers."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri()+'#cutlist');page.locator('[data-tour-action="welcome-skip"]').click()
    expect(page.locator('[data-proposal-view="cutlist"]')).to_have_text('Comp tool')
    page.wait_for_function('Array.from(document.querySelectorAll(".production-score-image")).every(i=>i.complete&&i.naturalWidth)')
    def layers():return page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,selection:scoreSelection(state(),t)}))')
    saved=layers();count=page.evaluate('state().doc.pages')
    def columns(n):
        page.locator('.score-display-menu>summary').click();page.locator(f'[data-score-columns="{n}"]').check()
    def continuous(value):
        page.locator('.score-display-menu>summary').click();page.locator('[data-score-continuous]').set_checked(value)
    columns(2)
    expect(page.locator('.score-paper')).to_have_count(count)
    a=page.locator('[data-score-page="1"]').bounding_box();b=page.locator('[data-score-page="2"]').bounding_box()
    assert abs(a['y']-b['y'])<1 and b['x']>=a['x']+a['width'],(a,b)
    assert layers()==saved
    continuous(False)
    expect(page.locator('.score-paper')).to_have_count(2)
    page.locator('[data-score-page-step="1"]').click()
    expect(page.locator('.score-paper').first).to_have_attribute('data-score-page','3')
    page.locator('[data-score-page-step="-1"]').click()
    columns(1)
    expect(page.locator('.score-paper')).to_have_count(1)
    page.locator('[data-score-page-step="1"]').click()
    expect(page.locator('.score-paper')).to_have_attribute('data-score-page','2')
    # Explicit navigation to a note on another page renders the correct group.
    page.evaluate('state().page=3;state().measure=35;renderDemo();revealScoreMeasure()')
    expect(page.locator('.score-paper')).to_have_attribute('data-score-page','3')
    continuous(True);columns(2)
    # Both columns retain their own measure coordinates and note layer.
    page.locator('.score-canvas').evaluate('(el)=>el.scrollTop=0')
    cell=page.locator('[data-score-page="2"] [data-score-cell]').first
    bar=cell.get_attribute('data-score-measure')
    cell.click(modifiers=['Meta'])
    assert page.evaluate('(bar)=>scoreSelection(state(),takeById(state(),state().selected)).includes(bar+":vln1")',bar)
    cell.dblclick();page.locator('#score-comment-text').fill('Second page note');page.locator('#score-comment-text').press('Enter')
    assert page.evaluate('takeById(state(),state().selected).notes.at(-1).page')==2
    selection=layers()
    # Pinching over the right page anchors that page rather than the left one.
    page.locator('.score-canvas').evaluate('(el)=>el.scrollTop=0')
    anchor=page.locator('[data-score-page="2"]').evaluate('(el)=>{const r=el.getBoundingClientRect();return {x:r.left+r.width*.6,y:r.top+r.height*.2}}')
    page.evaluate('''point=>document.querySelector('[data-score-page="2"]').dispatchEvent(new WheelEvent('wheel',{bubbles:true,cancelable:true,ctrlKey:true,deltaY:-15,clientX:point.x,clientY:point.y}))''',anchor)
    fractions=page.locator('[data-score-page="2"]').evaluate('(el,p)=>{const r=el.getBoundingClientRect();return {x:(p.x-r.left)/r.width,y:(p.y-r.top)/r.height}}',anchor)
    assert abs(fractions['x']-.6)<.01 and abs(fractions['y']-.2)<.01,fractions
    page.locator('[data-score-zoom="fit"]').click()
    for _ in range(4):page.locator('[data-score-zoom="out"]').click()
    expect(page.locator('[data-score-zoom-value]')).to_have_text('10%')
    expect(page.locator('[data-score-zoom="out"]')).to_be_disabled()
    page.locator('#score-cue').select_option('1')
    expect(page.locator('[data-score-zoom-value]')).to_have_text('10%')
    assert page.evaluate('scorePageColumns(state())')==2
    page.locator('#score-cue').select_option('0')
    assert layers()==selection
    page.locator('[data-score-zoom="fit"]').click()
    page.locator('[data-select-take="c0-t1"]').click()
    assert page.evaluate('scorePageColumns(state())')==2
    for width in [1512,390]:
        page.set_viewport_size({'width':width,'height':1100})
        page.locator('[data-score-zoom="fit"]').click()
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        a=page.locator('[data-score-page="1"]').bounding_box();b=page.locator('[data-score-page="2"]').bounding_box()
        assert abs(a['y']-b['y'])<1 and b['x']>a['x']
        page.screenshot(path=str(ROOT/f'checks/score-two-pages-{width}.png'))
    assert not errors,errors
    browser.close()
print('PASS: Comp tool label, two-page spreads, optional continuous scroll, single-page navigation, page-specific editing, global 10% zoom and mobile width')
