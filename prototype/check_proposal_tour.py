"""Walk every suggestion and verify opt-in prompts, shared state and safe controls."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    context=browser.new_context(viewport={'width':1512,'height':1100})
    page=context.new_page();errors=[];network=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto((ROOT/'dist/index.html').as_uri())
    expect(page.locator('#proposal-welcome')).to_be_visible()
    page.locator('[data-tour-action="welcome-start"]').click()
    expect(page.locator('.proposal-tour-card')).to_contain_text('Sterren in plaats van')
    assert page.evaluate('proposalTourSelection.size')==0
    def take_data():
        return page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,rating:t.rating,best:t.best,alt:!!t.alt,text:t.draft.text,selections:Object.fromEntries(Object.entries(t.scoreSelections||{}).map(([k,v])=>[k,[...v].sort()]))}))')
    original=take_data()
    steps=page.evaluate('proposalTourSteps.map(s=>({id:s.id,title:s.title,view:s.view}))')
    selected={'sterren','opnametoets','score-notes'}
    for index,step in enumerate(steps):
        expect(page.locator('#proposal-tour-title')).to_have_text(step['title'])
        expect(page.locator('.proposal-tour-highlight')).to_be_visible()
        if step['id'] in selected:page.locator('[data-tour-choice]').check()
        page.wait_for_timeout(30)
        card=page.locator('.proposal-tour-card').bounding_box()
        assert card['x']>=0 and card['y']>=0 and card['x']+card['width']<=1512 and card['y']+card['height']<=1100,(step,card)
        assert page.evaluate('proposalView')==step['view']
        if index in [0,6,16]:page.screenshot(path=str(ROOT/f'checks/tour-{index+1}.png'))
        page.locator('[data-tour-action="next"]').click()
    expect(page.locator('#proposal-prompt')).to_be_visible()
    prompt=page.evaluate('selectedTourPrompt()')
    assert page.evaluate('Array.from(proposalTourSelection).sort()')==sorted(selected)
    for step in steps:
        included=any(line.endswith('. '+step['title']) for line in prompt.splitlines() if line.startswith('## '))
        assert included==(step['id'] in selected),step
    page.evaluate('Object.defineProperty(navigator,"clipboard",{configurable:true,value:{writeText:async text=>{window.copiedTourPrompt=text;}}})')
    page.locator('[data-tour-action="copy"]').click()
    assert page.evaluate('window.copiedTourPrompt')==prompt
    # Touring does not create takes or edit notes, ratings or selections.
    assert take_data()==original
    with page.expect_download() as download:page.locator('[data-tour-action="download"]').click()
    target=ROOT/'checks/tour-prompt.md';download.value.save_as(str(target));assert target.read_text()==prompt
    page.locator('#proposal-prompt [data-tour-action="close-dialog"]').click()
    page.locator('[data-proposal-action="questions"]').click()
    expect(page.locator('#proposal-questions li')).to_have_count(6)
    expect(page.locator('#proposal-questions input[type=checkbox]')).to_have_count(0)
    page.locator('#proposal-questions [data-tour-action="close-dialog"]').first.click()
    # Selection survives reopening, unlike temporary demo notes.
    page.reload();page.locator('[data-tour-action="welcome-skip"]').click()
    assert page.evaluate('proposalTourSelection.size')==3
    page.locator('[data-proposal-action="tour"]').click()
    expect(page.locator('[data-tour-choice="sterren"]')).to_be_checked()
    page.locator('[data-tour-choice="sterren"]').uncheck()
    assert '## 1. Sterren in plaats van' not in page.evaluate('selectedTourPrompt()')
    page.locator('[data-tour-choice="sterren"]').check()
    page.keyboard.press('Escape');expect(page.locator('.proposal-tour-card')).to_have_count(0)
    # Guided view changes never stop a live take or lose a draft.
    page.locator('[data-proposal-view="recording"]').click();page.keyboard.press('Meta+Enter')
    live=page.evaluate('running(state()).id');page.locator('[data-draft]').fill('Draft kept through tour')
    page.evaluate("openTourStep(proposalTourSteps.findIndex(s=>s.id==='score-per-cue'))")
    assert page.evaluate('running(state()).id')==live
    page.keyboard.press('Escape');page.locator('[data-proposal-view="recording"]').click()
    expect(page.locator('[data-draft]')).to_have_value('Draft kept through tour')
    page.keyboard.press('Meta+Enter');assert page.evaluate('!running(state())')
    # Review dialogs cannot accidentally start a recording via Cmd+Enter.
    page.locator('[data-proposal-action="prompt"]').click();page.keyboard.press('Meta+Enter');assert page.evaluate('!running(state())')
    page.locator('#proposal-prompt [data-tour-action="close-dialog"]').click()
    # Small viewports retain an in-bounds card, highlight and functioning next action.
    page.set_viewport_size({'width':390,'height':844})
    for index in [0,6,7,16,18,20,24]:
        page.evaluate('(index)=>openTourStep(index)',index)
        page.wait_for_timeout(60)
        r=page.locator('.proposal-tour-card').bounding_box()
        assert r['x']>=0 and r['y']>=0 and r['x']+r['width']<=390 and r['y']+r['height']<=844,(index,r)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),index
    page.screenshot(path=str(ROOT/'checks/tour-mobile.png'))
    assert not errors,errors
    assert not network,network
    browser.close()
print('PASS: welcome choices, all tour targets, opt-in exact prompts/copy/download, persistence, open questions, live-take/draft preservation and mobile tour')
