"""Score settings preserve layers while switching selection scope and visibility."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium

ROOT = Path(__file__).resolve().parent
with sync_playwright() as p:
    browser = launch_chromium(p)
    page = browser.new_page(viewport={'width': 1512, 'height': 1100})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto((ROOT / 'dist/index.html').as_uri() + '#cutlist')
    page.locator('[data-tour-action="welcome-skip"]').click()
    link = page.get_by_role('button', name='Link instruments', exact=True)
    eye = page.get_by_role('button', name='See other takes', exact=True)
    expect(link).to_have_attribute('aria-pressed', 'true')
    expect(eye).to_have_attribute('aria-pressed', 'true')
    assert page.locator('.score-settings').bounding_box()['y'] < page.locator('.score-paper').first.bounding_box()['y']
    page.locator('[data-score-new-take]').click()
    first = page.evaluate('state().selected')

    def cell(bar, instrument):
        return page.locator(f'.score-paper[data-score-page="1"] [data-score-cell="{bar}:{instrument}"]')

    def keys():
        return page.evaluate('scoreSelection(state(),takeById(state(),state().selected))')

    cell(4, 'vln1').click(modifiers=['Meta'])
    assert len(keys()) == 4
    link.click()
    cell(5, 'vln2').click(modifiers=['Meta'])
    assert set(keys()) == {f'4:{i}' for i in ['vln1', 'vln2', 'vla', 'vc']} | {'5:vln2'}
    cell(4, 'vc').click(button='right', modifiers=['Meta'])
    assert '4:vc' not in keys() and '4:vla' in keys()
    page.locator('[data-score-undo]').click()
    assert '4:vc' in keys()
    # A drag in unlinked mode touches only the staves in its rectangle.
    start, end = cell(6, 'vc'), cell(7, 'vc')
    start.scroll_into_view_if_needed()
    a, z = start.bounding_box(), end.bounding_box()
    page.keyboard.down('Meta')
    page.mouse.move(a['x'] + a['width'] * .4, a['y'] + a['height'] * .5)
    page.mouse.down()
    page.mouse.move(z['x'] + z['width'] * .6, z['y'] + z['height'] * .5, steps=8)
    page.mouse.up()
    page.keyboard.up('Meta')
    assert {k for k in keys() if k.startswith(('6:', '7:'))} == {'6:vc', '7:vc'}
    before = keys()
    link.click()
    assert keys() == before  # Relinking never rewrites saved partial selections.
    cell(5, 'vln1').click(modifiers=['Meta'])
    assert all(f'5:{i}' in keys() for i in ['vln1', 'vln2', 'vla', 'vc'])
    cell(5, 'vc').click(button='right', modifiers=['Meta'])
    assert not any(k.startswith('5:') for k in keys())
    page.locator('[data-score-new-take]').click()
    second = page.evaluate('state().selected')
    assert not keys()
    expect(page.locator('.ghost-range')).not_to_have_count(0)
    eye.click()
    expect(page.locator('.ghost-range')).to_have_count(0)
    page.locator(f'[data-select-take="{first}"]').click(modifiers=['Meta'])
    expect(page.locator('.compared-range')).not_to_have_count(0)
    expect(eye).to_have_attribute('aria-pressed', 'false')
    # Explicit comparison notes remain visible with background layers off.
    cell(8, 'vln1').dblclick()
    page.locator('#score-comment-text').fill('Comparison remains visible')
    page.locator('#score-comment-text').press('Enter')
    page.locator(f'[data-select-take="{second}"]').click(modifiers=['Meta'])
    page.locator(f'[data-select-take="{second}"]').click(modifiers=['Meta'])
    expect(page.locator('.comparison-note')).to_contain_text('Comparison remains visible')
    page.locator('[data-proposal-view="recording"]').click()
    page.locator('[data-proposal-view="cutlist"]').click()
    expect(eye).to_have_attribute('aria-pressed', 'false')
    expect(link).to_have_attribute('aria-pressed', 'true')
    page.set_viewport_size({'width': 390, 'height': 844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.locator('.score-settings').scroll_into_view_if_needed()
    page.screenshot(path=str(ROOT / 'checks/score-settings-mobile.png'))
    assert not errors, errors
    browser.close()
print('PASS: score settings, linked/unlinked clicks and drags, undo, partial layer preservation, ghost visibility, explicit comparisons, workspace switching and mobile width')
