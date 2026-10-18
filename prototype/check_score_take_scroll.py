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
        for offset in [0, 200, 400, 1800]:
            page.evaluate('(top)=>window.scrollTo({top,behavior:"instant"})', offset)
            page.wait_for_timeout(100)
            for take, modifiers in [('c0-t1', []), ('c0-t2', []),
                                    ('c0-t2', []), ('c0-t1', ['Meta']),
                                    ('c0-t1', ['Meta'])]:
                button = page.locator(f'[data-select-take="{take}"]')
                before = page.evaluate('({y:scrollY,page:state().page})')
                if offset < 500:
                    expect(button).to_be_in_viewport()
                    button.click(modifiers=modifiers)
                else:
                    # Trigger the same handler without Playwright scrolling an
                    # offscreen button into view before it clicks.
                    button.dispatch_event('click', {'metaKey': bool(modifiers)})
                # Catch delayed browser anchoring as well as explicit scrolling.
                page.wait_for_timeout(150)
                after = page.evaluate('({y:scrollY,page:state().page})')
                assert abs(after['y'] - before['y']) <= 1, (variant, take, before, after)
                assert after['page'] == before['page'], (variant, before, after)
            expect(page.locator('[data-select-take="c0-t2"]')).to_have_attribute('aria-current', 'true')
            expect(page.locator('.score-take-picker [aria-pressed="true"]')).to_have_count(1)
        # Explicit bar navigation must still move to the requested score location.
        before = page.evaluate('scrollY')
        page.evaluate('() => {state().page=3;state().measure=35;renderDemo();revealScoreMeasure();}')
        assert page.evaluate('state().page') == 3
        assert abs(page.evaluate('scrollY') - before) > 100
    assert not errors, errors
    browser.close()
print('PASS: take switching and comparison preserve the reading position in 04A/B; bar navigation still scrolls')
