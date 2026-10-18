"""The two workspaces share real cue/take/note state and preserve score controls."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1100})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri())
    page.locator('[data-tour-action="welcome-skip"]').click()
    expect(page.locator('.proposal-shell')).to_have_count(1)
    expect(page.locator('[data-variant],.suggestion-card,.side-nav')).to_have_count(0)
    assert page.evaluate('active.id')=='bediening'
    page.locator('[data-take-best="c0-t2"]').click()
    page.locator('[data-rating-key="c0-t2"][data-stars="5"]').click()
    field=page.locator('[data-draft="c0-t2"]')
    field.fill('Same note in both views')
    page.locator('[data-measure-input="c0-t2"]').fill('18')
    field.press('Enter')
    page.locator('[data-proposal-view="cutlist"]').click()
    expect(page.locator('.score-note-copy').filter(has_text='Same note in both views')).to_have_count(1)
    expect(page.locator('[data-take-best="c0-t2"]')).to_have_attribute('aria-pressed','true')
    expect(page.locator('[data-rating-key="c0-t2"][data-stars="5"]')).to_have_attribute('aria-pressed','true')
    page.locator('[data-score-page="1"] [data-score-cell="3:vln1"]').dblclick()
    page.locator('#score-comment-text').fill('From the score')
    page.locator('#score-comment-text').press('Enter')
    page.locator('[data-proposal-view="recording"]').click()
    expect(page.locator('.calm-notes')).to_contain_text('From the score')
    page.locator('[data-rating-filter]').select_option('5')
    expect(page.locator('[data-calm-take="c0-t1"]')).to_be_hidden()
    page.locator('[data-rating-filter]').select_option('0')
    page.keyboard.press('Meta+Enter')
    live=page.evaluate('running(state()).id')
    assert live=='c0-t3'
    field=page.locator(f'[data-draft="{live}"]');field.fill('Draft with ordinary spaces')
    page.locator('[data-proposal-view="cutlist"]').click()
    assert page.evaluate('running(state()).id')==live
    assert page.evaluate('scoreSelection(state(),running(state()))')==[]
    expect(page.locator('.score-note-copy')).to_have_count(0)
    page.locator('[data-select-take="c0-t1"]').click()
    assert page.evaluate('running(state()).id')==live
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('!running(state())')
    page.locator('[data-select-take="c0-t3"]').click()
    page.locator('[data-proposal-view="recording"]').click()
    expect(page.locator(f'[data-draft="{live}"]')).to_have_value('Draft with ordinary spaces')
    page.locator('[data-select-cue="1"]').click()
    page.locator('[data-proposal-view="cutlist"]').click()
    expect(page.locator('#score-cue')).to_have_value('1')
    expect(page.locator('.score-paper')).to_have_count(9)
    for width in [390,1512]:
        page.set_viewport_size({'width':width,'height':1100})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
        page.locator('[data-proposal-view="recording"]').click()
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
        page.locator('[data-proposal-view="cutlist"]').click()
    page.screenshot(path=str(ROOT/'checks/unified-cutlist.png'))
    assert not errors,errors
    browser.close()
print('PASS: one workspace, shared notes/ratings/cues, live take isolation, clean score layers, drafts and mobile width')
