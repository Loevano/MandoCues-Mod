"""A draft and a placed note share the same bar/time controls and time anchor."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.clock.install()
    page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
    page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter');page.clock.run_for(2200)
    take=page.evaluate('state().selected');field=page.locator(f'[data-draft="{take}"]')
    field.fill('Cello intonation');original=page.evaluate('state().takes[0].at(-1).draft.at')
    count=page.evaluate('takeById(state(),state().selected).notes.length')
    composer=page.locator(f'[data-composer="{take}"]');before=composer.bounding_box()
    picker=composer.locator('.measure-picker');picker.locator('summary').click()
    assert composer.bounding_box()==before
    picker.locator('[data-picker-measure]').fill('18');picker.locator('[data-picker-measure]').press('Enter')
    assert page.evaluate('takeById(state(),state().selected).notes.length')==count
    expect(field).to_have_value('Cello intonation')
    stamp=composer.locator('[data-note-time-edit="draft"]');stamp.click();stamp.fill('00:45')
    page.clock.run_for(1100);expect(stamp).to_have_value('00:45');stamp.press('Enter')
    assert page.evaluate('takeById(state(),state().selected).draft.at')==45
    page.clock.run_for(2200)
    current=page.evaluate('position(takeById(state(),state().selected))')
    composer.locator('[data-reset-note-time="draft"]').click()
    assert page.evaluate('takeById(state(),state().selected).draft.at')==current and current>original
    expect(field).to_have_value('Cello intonation')
    assert page.evaluate('takeById(state(),state().selected).draft.measure')==18
    page.clock.run_for(2200)
    current=page.evaluate('position(takeById(state(),state().selected))')
    composer.locator('[data-reset-note-time="draft"]').click()
    assert page.evaluate('takeById(state(),state().selected).draft.at')==current
    stamp.click();stamp.fill('00:46');stamp.press('Enter');field.press('Enter')
    note=page.evaluate('takeById(state(),state().selected).notes.at(-1)')
    assert note['measure']==18 and note['at']==46 and note['originalAt']==original,note
    # Same menu on the next draft; All survives placing and doesn't submit early.
    assert page.evaluate('takeById(state(),state().selected).draft.at') is None
    page.clock.run_for(2200)
    field.fill('Whole take')
    second_start=page.evaluate('position(takeById(state(),state().selected))')
    assert page.evaluate('takeById(state(),state().selected).draft.at')==second_start and second_start>original
    picker.locator('summary').click();picker.locator('[data-pick-measure="all"]').click()
    stamp.click();stamp.fill('00:12');stamp.press('Escape')
    assert page.evaluate('takeById(state(),state().selected).draft.at')!=12
    field.press('Enter');note=page.evaluate('takeById(state(),state().selected).notes.at(-1)')
    assert note['measure'] is None and note['measureScope']=='all'
    # Clock buttons belong to their own take, even while another take records.
    page.locator('[data-select-take="c0-t1"]').click()
    page.evaluate('takeById(state(),"c0-t1").cursor=17')
    old_row=page.locator('.calm-notes [data-note-id="seed-1"]')
    old_row.locator('[data-reset-note-time]').click()
    expect(old_row.locator('[data-note-time-edit]')).to_have_value('00:17')
    assert page.evaluate('takeById(state(),"c0-t1").notes[0].at')==17
    assert page.evaluate('running(state()).id')==take
    assert page.evaluate('takeById(state(),"c0-t2").notes[0].at')==38
    assert not errors,errors
    browser.close()
print('PASS: shared draft/saved metadata controls, floating bar picker, time edit/current-time refresh/Escape, immutable first-typing time, All and no early note submission')
