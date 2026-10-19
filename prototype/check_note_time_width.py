"""All clock time digits fit before/after Enter, live rollover and in the score note list."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100});page.clock.install()
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri());page.locator('[data-tour-action="welcome-skip"]').click()
    def fits(field):
        actual=field.evaluate('''el=>{const cs=getComputedStyle(el),ctx=document.createElement('canvas').getContext('2d');ctx.font=cs.font;return {content:el.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight),text:ctx.measureText(el.value).width,scroll:el.scrollLeft}}''')
        assert actual['content']>=actual['text']+1,actual
        assert actual['scroll']==0,actual
        control=field.locator('..');reset=control.locator('[data-reset-note-time]')
        assert field.bounding_box()['x']+field.bounding_box()['width']<=reset.bounding_box()['x']+.5
    for width in [1512,390]:
        page.set_viewport_size({'width':width,'height':1100})
        for view in ['recording','cutlist']:
            page.evaluate('(view)=>showProposalView(view)',view)
            if view=='recording':
                composer=page.locator('[data-composer="c0-t2"]')
                field=composer.locator('[data-note-time-edit="draft"]')
                fits(field)
                for value in ['12:42:00 AM','01:02:03 PM','11:59:59 PM','23:59:59']:
                    field.click();field.fill(value);fits(field)
                    field.press('Enter');fits(field)
                    assert field.input_value().endswith((' AM',' PM'))
                composer.locator('[data-reset-note-time="draft"]').click();fits(field)
            # Saved clock times retain sufficient width and do not collide with Delete.
            selector='.calm-notes [data-note-id="seed-2"]' if view=='recording' else '.score-note-row[data-note-id="seed-2"]'
            row=page.locator(selector);stamp=row.locator('[data-note-time-edit]')
            for value in ['12:42:00 AM','01:02:03 PM','11:59:59 PM','23:59:59']:
                stamp.click();stamp.fill(value);fits(stamp);stamp.press('Enter');fits(stamp)
                assert stamp.input_value().endswith((' AM',' PM'))
                if view=='cutlist':
                    stamp_box=stamp.locator('..').bounding_box();delete=row.locator('[data-delete-note]').bounding_box()
                    assert stamp_box['x']+stamp_box['width']<=delete['x']+.5,(stamp_box,delete)
            row.locator('[data-reset-note-time]').click()
            expect(stamp).to_have_value(page.evaluate('noteTimeValue({clockAt:Date.now()})'));fits(stamp)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,view)
    page.evaluate("showProposalView('recording')")
    page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
    live=page.evaluate('running(state()).id')
    field=page.locator(f'[data-composer="{live}"] [data-note-time-edit="draft"]')
    expect(field).to_have_value(page.evaluate('noteTimeValue({clockAt:Date.now()})'));fits(field)
    # A take's relative cursor cannot affect a wall-clock note timestamp.
    page.evaluate('running(state()).base=3599');page.clock.run_for(1100)
    expect(field).to_have_value(page.evaluate('noteTimeValue({clockAt:Date.now()})'));fits(field)
    field.click();field.fill('12:34:56');fits(field);field.press('Escape')
    expect(field).to_have_value(page.evaluate('noteTimeValue({clockAt:Date.now()})'));fits(field)
    page.screenshot(path=str(ROOT/'checks/note-time-width.png'))
    assert not errors,errors
    browser.close()
print('PASS: full short/long clock times, draft/saved/score fields, reset/Escape, independence from take time, no reset/delete overlap and mobile width')
