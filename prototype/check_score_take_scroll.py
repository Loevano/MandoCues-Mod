"""Switching take layers keeps the score at the current reading position."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium

ROOT = Path(__file__).resolve().parent
errors = []
with sync_playwright() as p:
    browser = launch_chromium(p)
    page = browser.new_page(viewport={'width': 1512, 'height': 1100})
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto((ROOT / 'dist/index.html').as_uri() + '#partituur')
    for variant in ['A', 'B']:
        page.locator(f'[data-variant="{variant}"]').click()
        page.locator('[data-action="reset"]').click()
        page.wait_for_function('Array.from(document.querySelectorAll(".production-score-image")).every(i=>i.complete&&i.naturalWidth)')
        # An older take may have a different saved page and document offset.
        page.evaluate('''() => {
            const s=state(),t=takeById(s,'c0-t1');
            t.scoreViews={[s.doc.id]:{page:3,measure:35,top:2200}};
        }''')
        for offset in [0, 400, 1800]:
            page.locator('.score-canvas').scroll_into_view_if_needed()
            page.locator('.score-canvas').evaluate('(canvas,top)=>canvas.scrollTop=top', offset)
            page.wait_for_timeout(100)
            for take, modifiers in [('c0-t1', []), ('c0-t2', []),
                                    ('c0-t2', []), ('c0-t1', ['Meta']),
                                    ('c0-t1', ['Meta'])]:
                button = page.locator(f'[data-select-take="{take}"]')
                before = page.evaluate('({y:scrollY,page:state().page,top:document.querySelector(".score-canvas").scrollTop})')
                expect(button).to_be_in_viewport()
                expect(page.locator('.cutlist-notes-list')).to_be_in_viewport()
                button.click(modifiers=modifiers)
                # Catch delayed browser anchoring as well as explicit scrolling.
                page.wait_for_timeout(150)
                after = page.evaluate('({y:scrollY,page:state().page,top:document.querySelector(".score-canvas").scrollTop})')
                assert abs(after['y'] - before['y']) <= 1, (variant, take, before, after)
                assert after['page'] == before['page'], (variant, before, after)
                assert abs(after['top'] - before['top']) <= 1, (variant, before, after)
            expect(page.locator('[data-select-take="c0-t2"]')).to_have_attribute('aria-current', 'true')
            expect(page.locator('.score-take-picker [data-select-take][aria-pressed="true"]')).to_have_count(1)
        # Explicit bar navigation must still move to the requested score location.
        before = page.locator('.score-canvas').evaluate('(canvas)=>canvas.scrollTop')
        document_top = page.evaluate('scrollY')
        page.evaluate('() => {state().page=3;state().measure=35;renderDemo();revealScoreMeasure();}')
        assert page.evaluate('state().page') == 3
        assert abs(page.locator('.score-canvas').evaluate('(canvas)=>canvas.scrollTop') - before) > 100
        assert abs(page.evaluate('scrollY') - document_top) <= 1
        # Wheel scrolling must stay inside the score and leave the sidebar still.
        canvas = page.locator('.score-canvas')
        canvas.evaluate('(el)=>el.scrollTop=0')
        sidebar_top = page.locator('.cutlist-sidebar').bounding_box()['y']
        canvas.hover()
        page.mouse.wheel(0, 700)
        page.wait_for_timeout(250)
        assert canvas.evaluate('(el)=>el.scrollTop') > 0
        assert abs(page.evaluate('scrollY') - document_top) <= 1
        assert page.locator('.cutlist-sidebar').bounding_box()['y'] == sidebar_top
    assert not errors, errors
    browser.close()
print('PASS: take switching and comparison preserve the reading position in 04A/B; bar navigation still scrolls')
