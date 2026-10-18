"""All timecode digits fit before/after Enter, live rollover and in the score note list."""
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
                for value in ['00:42','01:02:03','99999:59:59']:
                    field.click();field.fill(value);fits(field)
                    field.press('Enter');fits(field)
                composer.locator('[data-reset-note-time="draft"]').click();fits(field)
            # Saved timecodes retain sufficient width and do not collide with Delete.
            selector='.calm-notes [data-note-id="seed-2"]' if view=='recording' else '.score-note-row[data-note-id="seed-2"]'
            row=page.locator(selector);stamp=row.locator('[data-note-time-edit]')
            for value in ['00:42','01:02:03','99999:59:59']:
                stamp.click();stamp.fill(value);fits(stamp);stamp.press('Enter');fits(stamp)
                if view=='cutlist':
                    stamp_box=stamp.locator('..').bounding_box();delete=row.locator('[data-delete-note]').bounding_box()
                    assert stamp_box['x']+stamp_box['width']<=delete['x']+.5,(stamp_box,delete)
            row.locator('[data-reset-note-time]').click()
            expect(stamp).to_have_value('00:38');fits(stamp)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,view)
    page.evaluate("showProposalView('recording')")
    page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
    live=page.evaluate('running(state()).id')
    page.evaluate('running(state()).base=3599')
    page.clock.run_for(250)
    field=page.locator(f'[data-composer="{live}"] [data-note-time-edit="draft"]')
    expect(field).to_have_value('59:59');fits(field)
    page.clock.run_for(1100)
    expect(field).to_have_value('1:00:00');fits(field)
    field.click();field.fill('12:34:56');fits(field);field.press('Escape')
    expect(field).to_have_value('1:00:00');fits(field)
    page.screenshot(path=str(ROOT/'checks/note-time-width.png'))
    assert not errors,errors
    browser.close()
print('PASS: full short/long timecodes, draft/saved/score fields, reset/Escape, live hour rollover, no reset/delete overlap and mobile width')
