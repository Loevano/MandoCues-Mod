"""Visible controls, shared clocks and reversible local session actions."""
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium

ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1100})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.clock.install(time=datetime(2026,10,18,10,0,tzinfo=timezone.utc))
    page.goto((ROOT/'dist/index.html').as_uri())
    page.locator('[data-tour-action="welcome-skip"]').click()
    for selector in ['[data-action="prev-cue"]','[data-action="next-cue"]','[data-action="record-overdub"]','[data-session-action="break"]','[data-session-action="end"]','[data-wall-clock]','[data-proposal-expected-end]','[data-proposal-cue-clock]']:
        el=page.locator('#main-panel '+selector)
        expect(el).to_be_visible()
        assert not el.evaluate('(el)=>!!el.closest("details")'),selector
    expect(page.locator('#main-panel [data-session-action="break"]')).to_be_disabled()
    page.keyboard.press('Meta+Enter')
    page.locator('#main-panel [data-action="next-cue"]').click()
    expect(page.locator('#main-panel .main-cue')).to_contain_text('1M18')
    page.locator('#main-panel [data-action="prev-cue"]').click()
    expect(page.locator('#main-panel .main-cue')).to_contain_text('1M02')
    page.locator('#main-panel [data-action="record-overdub"]').click()
    live=page.evaluate('running(state()).id')
    assert page.evaluate('running(state()).kind')=='overdub'
    assert page.evaluate('nextEntryNumber(state(),0,"take")')==3
    for selector in ['[data-action="next-cue"]','[data-session-action="break"]','[data-session-action="end"]']:
        expect(page.locator('#main-panel '+selector)).to_be_disabled()
    page.clock.run_for(2200)
    expect(page.locator('#main-panel [data-live]')).not_to_have_text('00:00')
    page.keyboard.press('Meta+Enter')
    page.locator('[data-select-take="c0-t2"]').click()
    field=page.locator('[data-draft="c0-t2"]');field.fill('Keep my draft through break and end')
    def timing():
        return page.evaluate('(()=>{const t=scoreWorkflowTiming(state());return {elapsed:t.elapsed,cue:t.cueElapsed,delta:t.delta,expected:proposalEndTime(t),planned:proposalEndTime(t,false)}})()')
    before=timing()
    page.locator('#main-panel [data-session-action="break"]').click()
    paused=timing()
    page.clock.run_for(62000)
    after=timing()
    assert after['elapsed']==paused['elapsed'] and after['cue']==paused['cue'],(paused,after)
    assert after['delta']>=paused['delta']+62,(paused,after)
    assert after['expected']!=paused['expected'] and after['planned']==before['planned']
    expect(page.locator('#main-panel .record')).to_contain_text('Resume session')
    # Cmd+Enter resumes the session without creating a take.
    count=page.evaluate('allTakes(state()).length')
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('!state().sessionPausedAt&&!running(state())')
    assert page.evaluate('allTakes(state()).length')==count
    page.clock.run_for(2100)
    assert timing()['elapsed']>=paused['elapsed']+2
    before_end=timing()
    page.locator('#main-panel [data-session-action="end"]').click()
    expect(page.locator('#main-panel .rec-status')).to_contain_text('Session ended')
    frozen=timing();page.clock.run_for(61000)
    assert timing()==frozen
    assert frozen['planned']==before_end['planned']
    assert page.evaluate('allTakes(state()).length')==count
    expect(field).to_have_value('Keep my draft through break and end')
    page.keyboard.press('Meta+Enter')
    assert page.evaluate('state().sessionStarted&&!running(state())')
    expect(field).to_have_value('Keep my draft through break and end')
    page.locator('[data-calm-session] > summary').click()
    expect(page.locator('.calm-extra-times')).to_contain_text('Session elapsed')
    expect(page.locator('.calm-extra-times')).to_contain_text('Remaining work')
    expect(page.locator('.calm-extra-times')).to_contain_text('Planned end')
    page.locator('[data-calm-session] > summary').click()
    for width in [390,900,1512]:
        page.set_viewport_size({'width':width,'height':1100})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
        for selector in ['.proposal-action-group','.proposal-session-clocks']:
            for item in page.locator(selector).all():
                r=item.bounding_box()
                assert r['x']>=0 and r['x']+r['width']<=width,(width,selector,r)
    page.locator('#cue-scroll').evaluate('(el)=>{el.scrollTop=0}')
    page.screenshot(path=str(ROOT/'checks/main-panel.png'))
    assert not errors,errors
    browser.close()
print('PASS: visible main controls, cue navigation, overdub numbering, shared clocks, break/resume/end, retained drafts and responsive layout')
