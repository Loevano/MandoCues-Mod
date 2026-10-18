"""Pinch zoom changes only the score, anchored under the gesture."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1000})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri()+'#cutlist')
    page.locator('[data-tour-action="welcome-skip"]').click()
    page.wait_for_function('Array.from(document.querySelectorAll(".production-score-image")).every(i=>i.complete&&i.naturalWidth)')
    original=page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,selection:scoreSelection(state(),t)}))')
    page.locator('.score-canvas').evaluate('(el)=>el.scrollTop=200')
    anchor=page.evaluate('''()=>{
        const c=document.querySelector('.score-canvas'),r=c.getBoundingClientRect(),x=r.left+c.clientWidth*.4,y=r.top+c.clientHeight*.35;
        const p=c.querySelector('.score-paper'),b=p.getBoundingClientRect();return {x,y,px:(x-b.left)/b.width,py:(y-b.top)/b.height};
    }''')
    def wheel(delta,ctrl=True):
        return page.evaluate('''({delta,ctrl,anchor})=>{
            const c=document.querySelector('.score-canvas'),e=new WheelEvent('wheel',{bubbles:true,cancelable:true,ctrlKey:ctrl,deltaY:delta,clientX:anchor.x,clientY:anchor.y});
            c.dispatchEvent(e);return e.defaultPrevented;
        }''',{'delta':delta,'ctrl':ctrl,'anchor':anchor})
    assert not wheel(40,False)
    assert page.evaluate('state().zoom')==1
    assert wheel(-35)
    zoom=page.evaluate('state().zoom');assert zoom>1
    after=page.evaluate('''({x,y})=>{
        const b=document.querySelector('.score-paper').getBoundingClientRect();return {px:(x-b.left)/b.width,py:(y-b.top)/b.height};
    }''',anchor)
    assert abs(after['px']-anchor['px'])<.005 and abs(after['py']-anchor['py'])<.005,(anchor,after)
    assert wheel(35)
    assert abs(page.evaluate('state().zoom')-1)<.001
    # Safari uses gesture events, independently from the Chromium wheel stream.
    for name,scale in [('gesturestart',1),('gesturechange',1.6),('gestureend',1.6)]:
        assert page.evaluate('''({name,scale,anchor})=>{
            const e=new Event(name,{bubbles:true,cancelable:true});
            Object.defineProperties(e,{scale:{value:scale},clientX:{value:anchor.x},clientY:{value:anchor.y}});
            document.querySelector('.score-canvas').dispatchEvent(e);return e.defaultPrevented;
        }''',{'name':name,'scale':scale,'anchor':anchor})
    expect(page.locator('[data-score-zoom-value]')).to_have_text('160%')
    assert page.evaluate('visualViewport.scale')==1
    assert page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,selection:scoreSelection(state(),t)}))')==original
    for _ in range(5):wheel(-80)
    assert page.evaluate('state().zoom')==3
    for _ in range(5):wheel(80)
    assert page.evaluate('state().zoom')==.5
    page.locator('[data-score-zoom="fit"]').click()
    expect(page.locator('[data-score-zoom-value]')).to_have_text('100%')
    assert not errors,errors
    browser.close()
print('PASS: Chromium pinch wheel, Safari gesture handling, pointer anchor, zoom limits, native scroll and unchanged notes/selections')
