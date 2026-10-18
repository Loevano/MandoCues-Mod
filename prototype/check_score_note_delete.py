"""Delete removes a selected score note, while text editing retains native keys."""
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
    page.locator('[data-score-new-take]').click()
    owner=page.evaluate('state().selected')
    page.locator('[data-score-page="1"] [data-score-cell="2:vln2"]').dblclick()
    expect(page.locator('#score-comment-dialog [data-delete-note]')).to_have_count(0)
    page.locator('#score-comment-text').fill('Delete only this note')
    page.locator('#score-comment-text').press('Enter')
    original=page.evaluate('takeById(state(),state().selected).notes[0]')
    def saved():return page.evaluate('(id)=>takeById(state(),id).notes',owner)
    def annotation():return page.locator('.score-text-annotation').filter(has_text='Delete only this note')
    baseline=page.evaluate('allTakes(state()).filter(t=>t.id!==state().selected).map(t=>({id:t.id,notes:t.notes,selection:scoreSelection(state(),t)}))')
    for key in ['Backspace','Delete']:
        annotation().click()
        expect(page.locator('#score-comment-dialog')).to_be_focused()
        expect(page.locator('#score-comment-dialog [data-delete-note]')).to_have_count(1)
        page.keyboard.press(key)
        assert saved()==[]
        expect(page.locator('#score-comment-dialog')).to_have_count(0)
        page.keyboard.press('Meta+z');assert saved()==[original]
        page.keyboard.press('Meta+Shift+z');assert saved()==[]
        page.keyboard.press('Meta+z');assert saved()==[original]
    annotation().click()
    text=page.locator('#score-comment-text');text.fill('abc');text.press('Backspace')
    expect(text).to_have_value('ab')
    assert saved()==[original]
    text.press('Control+Backspace')
    assert saved()==[original]
    # The explicit Delete action discards the draft and deletes the saved note.
    page.locator('#score-comment-dialog [data-delete-note]').click()
    assert saved()==[]
    expect(page.locator('#score-comment-dialog')).to_have_count(0)
    page.keyboard.press('Meta+z');assert saved()==[original]
    # No stale focused-note state: an ordinary non-note button cannot delete it.
    page.locator('[data-score-setting="scoreLinkInstruments"]').focus()
    page.keyboard.press('Backspace');assert saved()==[original]
    # A compared note belongs to its own take and its own undo stack.
    page.locator('[data-score-new-take]').click()
    other=page.evaluate('state().selected')
    page.locator(f'[data-select-take="{owner}"]').click(modifiers=['Meta'])
    annotation().click();page.keyboard.press('Backspace');assert saved()==[]
    assert page.evaluate('(id)=>takeById(state(),id).notes',other)==[]
    page.keyboard.press('Meta+z');assert saved()==[original]
    assert page.evaluate('allTakes(state()).filter(t=>![state().selected,"'+other+'"].includes(t.id)).map(t=>({id:t.id,notes:t.notes,selection:scoreSelection(state(),t)}))')==baseline
    assert not errors,errors
    browser.close()
print('PASS: selected-note Delete/Backspace, native text deletion, Cancel/Delete editor, undo/redo, no stale selection and comparison take isolation')
