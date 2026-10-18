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
    for variant in ['unified']:
        page.reload();page.locator('[data-tour-action="welcome-skip"]').click()
        page.wait_for_function('Array.from(document.querySelectorAll(".production-score-image")).every(i=>i.complete&&i.naturalWidth)')
        # Compact rows keep separate rating/Best/Alt controls in fixed columns.
        def take_layout():
            return page.locator('.score-take-row').evaluate_all("""rows=>rows.map(row=>{
                const r=row.getBoundingClientRect();
                return [r.height,...Array.from(row.querySelectorAll('.star-rating,.score-take-flags')).flatMap(el=>{
                    const b=el.getBoundingClientRect();return [b.x-r.x,b.y-r.y,b.width,b.height];
                })];
            })""")
        layout = take_layout()
        assert all(row[0] <= 60 for row in layout), layout
        selected = page.evaluate('state().selected')
        for take in ['c0-t2', 'c0-t1']:
            row = page.locator(f'.score-take-row:has([data-select-take="{take}"])')
            alt = row.locator('[data-take-alt]')
            previous_alt = alt.get_attribute('aria-pressed')
            row.locator('[data-take-best]').click()
            expect(row.locator('[data-take-best]')).to_have_attribute('aria-pressed', 'true')
            expect(page.locator('.score-take-flags .best[aria-pressed="true"]')).to_have_count(1)
            alt.click()
            expect(alt).to_have_attribute('aria-pressed', 'false' if previous_alt == 'true' else 'true')
            row.locator('[data-stars="4"]').click()
            expect(row.locator('[data-stars="4"]')).to_have_attribute('aria-pressed', 'true')
            assert page.evaluate('state().selected') == selected
            assert take_layout() == layout
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
        page.locator('.score-canvas').evaluate('(canvas)=>{canvas.scrollTop=0}')
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
    page.set_viewport_size({'width': 390, 'height': 844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert page.locator('.score-take-picker').evaluate('(el)=>el.scrollWidth<=el.clientWidth')
    page.screenshot(path=str(ROOT / 'checks/compact-take-list.png'), full_page=True)
    assert not errors, errors
    browser.close()
print('PASS: take switching and comparison preserve the reading position in the shared score view; bar navigation still scrolls')
