"""Direct note metadata editing keeps the original timestamp and correct take scope."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1100})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.clock.install()
    page.goto((ROOT/'dist/index.html').as_uri())
    page.locator('[data-tour-action="welcome-skip"]').click()
    page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
    expect(page.locator('.quick-note-suggestions')).not_to_have_attribute('open','')
    expect(page.locator('details.quick-note-suggestions')).to_have_count(0)
    expect(page.locator('[data-quick-note="Intonation"]')).to_be_visible()
    take=page.evaluate('running(state()).id')
    page.clock.run_for(2200)
    field=page.locator(f'[data-draft="{take}"]');field.fill('Frozen at first key')
    original=page.evaluate('takeById(state(),state().selected).draft.at')
    page.clock.run_for(3500)
    field.press('Enter')
    note_id=page.evaluate('takeById(state(),state().selected).notes.at(-1).id')
    def saved():
        return page.evaluate('([take,id])=>takeById(state(),take).notes.find(n=>n.id===id)',[take,note_id])
    assert saved()['at']==saved()['originalAt']==original
    row=page.locator(f'[data-note-id="{note_id}"][role="listitem"]')
    expect(row.locator('.note-adjust')).to_have_count(0)
    expect(row.locator('[data-delete-note]')).to_have_count(1)
    def choose_bar(value):
        picker=page.locator(f'[data-measure-menu="{note_id}"]')
        before=row.bounding_box()
        picker.locator('summary').click()
        assert row.bounding_box()==before, 'Opening the bar menu moved the note row'
        assert picker.locator('.measure-picker-panel').evaluate('(el)=>getComputedStyle(el).position')=='fixed'
        input=picker.locator('[data-picker-measure]')
        expect(input).to_be_focused()
        choices=picker.locator('.measure-choices')
        assert choices.evaluate('(el)=>el.scrollHeight>el.clientHeight')
        expect(choices.locator('[data-pick-measure="all"]')).to_have_count(1)
        expect(choices.locator('[data-pick-measure="41"]')).to_have_count(1)
        expect(picker.locator('[data-apply-measure]')).to_have_count(0)
        if value=='all':
            choices.locator('[data-pick-measure="all"]').click()
        else:
            for digit in str(value):input.press(digit)
            input.press('Enter')
    choose_bar(8)
    assert saved()['measure']==8
    choose_bar('all')
    assert saved()['measure'] is None and saved()['measureScope']=='all'
    expect(row.locator('.measure-picker > summary')).to_contain_text('All')
    choose_bar(18)
    assert saved()['measure']==18 and saved()['at']==original
    stamp=row.locator('[data-note-time-edit]')
    stamp.click();stamp.fill('00:45');stamp.press('Escape')
    assert saved()['at']==original
    stamp.click();stamp.fill('00:45');stamp.press('Enter')
    assert saved()['at']==45 and saved()['originalAt']==original
    expect(stamp).to_have_attribute('readonly','')
    current=page.evaluate('(take)=>position(takeById(state(),take))',take)
    row.locator('[data-reset-note-time]').click()
    assert saved()['at']==current and saved()['originalAt']==original and current>original
    page.keyboard.press('Meta+Enter')
    page.locator('[data-proposal-view="cutlist"]').click()
    row=page.locator(f'.score-note-row[data-note-id="{note_id}"]')
    expect(row.locator('[data-score-note]')).to_have_count(0)
    expect(row.locator('[data-delete-note]')).to_have_count(1)
    choose_bar('all')
    assert saved()['measureScope']=='all' and saved()['page'] is None
    choose_bar(18)
    assert saved()['page'] is not None
    stamp=row.locator('[data-note-time-edit]')
    stamp.click();stamp.fill('01:02:03');stamp.press('Enter')
    assert saved()['at']==3723 and saved()['originalAt']==original
    expect(stamp).to_have_value('1:02:03')
    current=page.evaluate('(take)=>position(takeById(state(),take))',take)
    row.locator('[data-reset-note-time]').click()
    assert saved()['at']==current and saved()['originalAt']==original
    page.locator('[data-score-undo]').click();assert saved()['at']==3723
    page.locator('[data-score-redo]').click();assert saved()['at']==current
    # Editing the score text must not replace the original captured time.
    page.locator('.score-text-annotation').filter(has_text='Frozen at first key').click()
    page.locator('#score-comment-text').fill('The same note, corrected')
    page.locator('#score-comment-text').press('Enter')
    assert saved()['originalAt']==original and saved()['at']==current
    for width in [390,1512]:
        page.set_viewport_size({'width':width,'height':844})
        picker=page.locator(f'[data-measure-menu="{note_id}"]')
        picker.locator('summary').click()
        expect(picker.locator('[data-picker-measure]')).to_be_focused()
        r=picker.locator('.measure-picker-panel').bounding_box()
        assert r['x']>=0 and r['y']>=0 and r['x']+r['width']<=width and r['y']+r['height']<=844,(width,r)
        choices=picker.locator('.measure-choices');choices.evaluate('(el)=>{el.scrollTop=el.scrollHeight}')
        expect(choices.locator('button').last).to_be_in_viewport()
        page.keyboard.press('Escape')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
    row.locator('[data-delete-note]').click()
    assert saved() is None
    assert not errors,errors
    browser.close()
print('PASS: scrollable full bar list, All take scope, direct typing/Enter, inline time edits, current-take time refresh, history, text editing and mobile popup bounds')
