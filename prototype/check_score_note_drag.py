"""Exercise note dragging, editing, history and take isolation in both score views."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium

ROOT = Path(__file__).resolve().parent
errors = []
with sync_playwright() as p:
    browser = launch_chromium(p)
    page = browser.new_page(viewport={'width': 1512, 'height': 1100})
    page.on('pageerror', lambda error: errors.append(str(error)))
    for variant in ['A', 'B']:
        page.goto((ROOT / 'dist/index.html').as_uri() + '#partituur')
        page.locator('[data-action="reset"]').click()
        page.locator(f'[data-variant="{variant}"]').click()
        def new_take():
            if variant == 'A':
                page.locator('[data-score-new-take]').click()
            else:
                page.locator('.score-session-actions [data-action="record"]').click()
                page.locator('.score-session-actions [data-action="record"]').click()

        new_take()
        cell = page.locator('[data-score-page="1"] [data-score-measure="2"][data-score-instrument="vln2"]')
        cell.dblclick(position={'x': 8, 'y': 8})
        page.locator('#score-comment-text').fill('Drag this note')
        page.locator('#score-comment-text').press('Enter')
        note = page.locator('.score-text-annotation').filter(has_text='Drag this note')

        def saved():
            return page.evaluate('''() => allTakes(state()).flatMap(t => t.notes).find(n => n.text === 'Drag this note')''')

        def start_drag(dx, dy):
            note.scroll_into_view_if_needed()
            box = note.bounding_box()
            page.mouse.move(box['x'] + 5, box['y'] + 5)
            page.mouse.down()
            page.mouse.move(box['x'] + 5 + dx, box['y'] + 5 + dy, steps=8)
            return box

        original = saved()
        selection = page.evaluate('scoreSelection(state(), takeById(state(), state().selected))')
        before = start_drag(70, 35)
        page.mouse.up()
        expect(page.locator('#score-comment-dialog')).to_have_count(0)
        moved = saved()
        after = note.bounding_box()
        assert abs(after['x'] - before['x'] - 70) < 2
        assert abs(after['y'] - before['y'] - 35) < 2
        assert moved['placement'] == 'free'
        assert {k: v for k, v in original.items() if k not in ('anchor', 'placement')} == {k: v for k, v in moved.items() if k not in ('anchor', 'placement')}
        assert page.evaluate('scoreSelection(state(), takeById(state(), state().selected))') == selection
        page.locator('[data-score-undo]').click()
        assert saved() == original
        page.locator('[data-score-redo]').click()
        assert saved() == moved
        # A small movement remains a click and opens the ordinary editor.
        start_drag(2, 1)
        page.mouse.up()
        expect(page.locator('#score-comment-dialog')).to_be_visible()
        page.locator('[data-score-cancel-comment]').click()
        assert saved() == moved
        # Escape and pointer cancellation discard previews without adding history.
        start_drag(50, 20)
        page.keyboard.press('Escape')
        page.mouse.up()
        assert saved() == moved
        if page.locator('#score-comment-dialog').count():
            page.locator('[data-score-cancel-comment]').click()
        start_drag(50, 20)
        note.dispatch_event('pointercancel')
        page.mouse.up()
        assert saved() == moved
        if page.locator('#score-comment-dialog').count():
            page.locator('[data-score-cancel-comment]').click()
        # Dragging compared text updates its owner, never the other take or live take.
        owner = page.evaluate('state().selected')
        new_take()
        other = page.evaluate('state().selected')
        page.locator(f'[data-select-take="{owner}"]').click(modifiers=['Meta'])
        page.locator(f'[data-select-take="{other}"]').click(modifiers=['Meta'])
        page.locator(f'[data-select-take="{other}"]').click(modifiers=['Meta'])
        assert page.evaluate('state().selected') == other
        live = page.evaluate('running(state())?.id || null')
        start_drag(40, 20)
        page.mouse.up()
        assert saved()['anchor'] != moved['anchor']
        assert page.evaluate('state().selected') == owner
        assert page.evaluate('running(state())?.id || null') == live
        assert page.evaluate('(id) => takeById(state(), id).notes.length', other) == 0
        page.locator('[data-score-undo]').click()
        assert saved() == moved
        # Page edges constrain the whole note, and normalized placement survives resize.
        start_drag(-3000, -3000)
        page.mouse.up()
        assert saved()['anchor'] == {'x': 0, 'y': 0}
        page.set_viewport_size({'width': 1100, 'height': 1100})
        paper = page.locator('[data-score-page="1"]').bounding_box()
        box = note.bounding_box()
        assert abs(box['x'] - paper['x']) < 2 and abs(box['y'] - paper['y']) < 2
        page.set_viewport_size({'width': 1512, 'height': 1100})
    assert not errors, errors
    browser.close()
print('PASS: note drag/click, exact placement, undo/redo, cancellation, comparison ownership, page bounds and resizing in A/B')
