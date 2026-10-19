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
    page.locator('[data-proposal-action="fullscreen"]').click()
    assert page.evaluate('document.fullscreenElement===document.documentElement||document.body.classList.contains("proposal-expanded")')
    page.locator('[data-proposal-view="cutlist"]').click()
    page.locator('[data-proposal-view="recording"]').click()
    page.locator('[data-proposal-action="fullscreen"]').click()
    assert page.evaluate('!document.fullscreenElement&&!document.body.classList.contains("proposal-expanded")')
    assert page.evaluate('active.id')=='bediening'
    expect(page.locator('#main-panel [data-proposal-plan]')).to_have_class('proposal-schedule is-on-time')
    page.locator('.session-planning-menu>summary').click()
    expect(page.locator('[data-proposal-elapsed]')).to_contain_text('00:')
    expect(page.locator('.planning-metrics')).to_contain_text('6:00:00')
    page.locator('.session-planning-menu>summary').click()
    # Cue selection remains visible in the list, separately from take selection.
    for cue_id in [1,0]:
        page.locator(f'.calm-cue-list [data-select-cue="{cue_id}"]').click()
        expect(page.locator('.calm-cue-list .cue-group.current')).to_have_count(1)
        heading=page.locator('.calm-cue-list .cue-group.current>.calm-cue-heading')
        other=page.locator('.calm-cue-list .cue-group:not(.current)>.calm-cue-heading').first
        assert heading.evaluate('(el)=>getComputedStyle(el).backgroundColor')!=other.evaluate('(el)=>getComputedStyle(el).backgroundColor')
        assert heading.evaluate('(el)=>getComputedStyle(el).boxShadow')!='none'
        expect(heading.locator('[data-select-cue]')).to_have_attribute('data-select-cue',str(cue_id))
    # A cue is the parent: its label is larger, with takes visibly to its right.
    for width in [390,1512]:
        page.set_viewport_size({'width':width,'height':1100})
        cue=page.locator('.calm-cue-heading [data-select-cue="0"] b')
        take=page.locator('[data-calm-take="c0-t1"] .calm-take-name b')
        assert take.bounding_box()['x']>=cue.bounding_box()['x']+12,width
        assert cue.evaluate('(el)=>parseFloat(getComputedStyle(el).fontSize)')>take.evaluate('(el)=>parseFloat(getComputedStyle(el).fontSize)'),width
        row=page.locator('[data-calm-take="c0-t1"]')
        assert row.locator('.calm-take-name').bounding_box()['x']+row.locator('.calm-take-name').bounding_box()['width']<=row.locator('.take-tools').bounding_box()['x'],width
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
    page.locator('[data-open-cue="0"]').click()
    expect(page.locator('[data-calm-take="c0-t1"]')).to_be_hidden()
    page.locator('[data-open-cue="0"]').click()
    expect(page.locator('[data-calm-take="c0-t1"]')).to_be_visible()
    tools=page.locator('[data-calm-take="c0-t2"] .take-tools')
    before=tools.bounding_box()
    page.locator('[data-take-best="c0-t2"]').click()
    page.locator('[data-select-take="c0-t1"]').click()
    after=tools.bounding_box()
    assert all(abs(before[key]-after[key])<1 for key in ('x','y','width','height')),(before,after)
    page.locator('[data-select-take="c0-t2"]').click()
    page.locator('#cue-scroll').evaluate('(el)=>{el.scrollTop=0}')
    page.screenshot(path=str(ROOT/'checks/cue-take-hierarchy.png'))
    page.locator('[data-rating-key="c0-t2"][data-stars="5"]').click()
    field=page.locator('[data-draft="c0-t2"]')
    field.fill('Same note in both views')
    page.locator('[data-composer="c0-t2"] .measure-picker > summary').click()
    page.locator('[data-composer="c0-t2"] [data-picker-measure]').fill('18')
    page.locator('[data-composer="c0-t2"] [data-picker-measure]').press('Enter')
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
    assert page.evaluate('state().sessionStarted&&!running(state())')
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
    # No clock-derived bars, including in the former schematic timing demo.
    manual=browser.new_page(viewport={'width':1512,'height':1100})
    manual.on('pageerror',lambda e:errors.append(str(e)))
    manual.goto((ROOT/'dist/index.html').as_uri())
    manual.locator('[data-tour-action="welcome-skip"]').click()
    manual.keyboard.press('Meta+Enter')
    assert manual.evaluate('state().sessionStarted&&!running(state())'),manual.evaluate('({started:state().sessionStarted,live:running(state())?.id,focus:document.activeElement.outerHTML})')
    for source in ['production','example']:
        manual.evaluate('(source)=>switchScoreDocument(state(),source==="example"?schematicScoreDoc():productionScoreDoc())',source)
        expect(manual.locator('[data-follow-measure]')).to_have_count(0)
        bar=manual.locator('[data-composer="c0-t2"] .measure-picker > summary')
        expect(bar).to_contain_text('+')
        field=manual.locator('[data-draft="c0-t2"]')
        field.fill('A note without a bar')
        manual.wait_for_timeout(250)
        expect(bar).to_contain_text('+')
        field.press('Enter')
        assert manual.evaluate('takeById(state(),"c0-t2").notes.at(-1).measure') is None
        bar.click()
        manual.locator('[data-composer="c0-t2"] [data-picker-measure]').fill('18')
        manual.locator('[data-composer="c0-t2"] [data-picker-measure]').press('Enter')
        field.fill('A manually located note');field.press('Enter')
        note_id=manual.evaluate('takeById(state(),"c0-t2").notes.at(-1).id')
        manual.locator(f'[data-measure-menu="{note_id}"] > summary').click()
        manual.locator(f'[data-note-id="{note_id}"][data-pick-measure="19"]').click()
        assert manual.evaluate('takeById(state(),"c0-t2").notes.at(-1).measure')==19
        manual.keyboard.press('Meta+Enter')
        expect(manual.locator('[data-draft="c0-t3"]')).to_have_value('')
        expect(manual.locator('[data-composer="c0-t3"] .measure-picker > summary')).to_contain_text('+')
        manual.keyboard.press('Meta+Enter')
        manual.locator('[data-select-take="c0-t2"]').click()
        manual.evaluate('state().takes[0]=state().takes[0].filter(t=>t.id!=="c0-t3")')
    manual.close()
    assert not errors,errors
    browser.close()
print('PASS: one workspace, shared notes/ratings/cues, live take isolation, clean score layers, drafts and mobile width')
