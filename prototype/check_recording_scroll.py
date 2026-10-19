"""Recording has one scroll viewport including session context and reachable transport."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':900})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri())
    page.locator('[data-tour-action="welcome-skip"]').click()
    for width in [1512,390]:
        page.set_viewport_size({'width':width,'height':900})
        page.evaluate("showProposalView('recording');document.querySelector('#cue-scroll').scrollTop=0")
        scroll=page.locator('#cue-scroll');header=page.locator('.proposal-view-bar')
        expect(scroll).to_contain_text('Session length')
        assert scroll.evaluate('(el)=>el.scrollHeight>el.clientHeight')
        assert page.locator('.calm-scroll').evaluate('(el)=>getComputedStyle(el).overflowY')=='visible'
        for selector in ['.browser-frame','.calm-scroll','.calm-notes']:
            assert page.locator(selector).evaluate('(el)=>parseFloat(getComputedStyle(el).borderTopWidth)')==0,selector
        assert page.locator('#main-panel').evaluate('(el)=>parseFloat(getComputedStyle(el).borderTopWidth)')>0
        initial=header.bounding_box()['y']
        # Scrolling over the recording area moves session context with the rest of the page.
        box=page.locator('#main-panel').bounding_box()
        page.mouse.move(box['x']+20,box['y']+20);page.mouse.wheel(0,400)
        page.wait_for_timeout(150)
        assert scroll.evaluate('(el)=>el.scrollTop')>100
        assert header.bounding_box()['y']<initial-100
        page.evaluate("const el=document.querySelector('#cue-scroll'),b=document.querySelector('#main-panel .record');el.scrollTop+=b.getBoundingClientRect().bottom-el.getBoundingClientRect().top+20;syncSticky()")
        expect(page.locator('.sticky-slot')).to_have_class(__import__('re').compile('is-stuck'))
        expect(page.locator('.sticky-slot .record')).to_be_in_viewport()
        before=scroll.evaluate('(el)=>el.scrollTop')
        # Rendering and switching views retain the position of the full Recording page.
        page.evaluate('renderDemo()')
        assert abs(scroll.evaluate('(el)=>el.scrollTop')-before)<1
        page.evaluate("showProposalView('cutlist')")
        expect(page.locator('#cue-scroll')).to_have_count(0)
        expect(page.locator('.score-canvas')).to_be_visible()
        page.evaluate("showProposalView('recording')")
        assert abs(scroll.evaluate('(el)=>el.scrollTop')-before)<1
        expect(page.locator('.sticky-slot .record')).to_be_in_viewport()
        # Start session, start take, and stop remain usable without returning to the header.
        page.locator('.sticky-slot .record').click()
        assert page.evaluate('state().sessionStarted&&!running(state())')
        page.locator('.sticky-slot .record').click()
        assert page.evaluate('!!running(state())')
        page.locator('.sticky-slot .stop').click()
        assert page.evaluate('!running(state())')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.screenshot(path=str(ROOT/f'checks/recording-scroll-{width}.png'))
        page.evaluate('state().sessionStarted=false;renderDemo()')
    assert not errors,errors
    browser.close()
print('PASS: one Recording scroll area, moving session header, flat sections, sticky transport, view/scroll preservation and responsive widths')
