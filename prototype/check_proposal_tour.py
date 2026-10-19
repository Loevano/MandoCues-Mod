"""Walk every suggestion and verify opt-in prompts, shared state and safe controls."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    context=browser.new_context(viewport={'width':1512,'height':1100})
    page=context.new_page();errors=[];network=[]
    # Old partial opt-in lists must not disable later suggestions by default.
    page.add_init_script("localStorage.setItem('mandocues-proposal-tour-v1', JSON.stringify(['sterren','cue-aanklikken','cue-takes','notes-enter','maat-aanpassen']))")
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto((ROOT/'dist/index.html').as_uri())
    expect(page.locator('#proposal-welcome')).to_be_visible()
    page.locator('[data-tour-action="welcome-start"]').click()
    expect(page.locator('.proposal-tour-card')).to_contain_text('Een mogelijke indeling voor Recording')
    assert page.evaluate('proposalTourSelection.size===proposalTourSteps.length')
    expect(page.locator('[data-tour-choice="duidelijke-labels"]')).to_be_checked()
    def take_data():
        return page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,rating:t.rating,best:t.best,alt:!!t.alt,text:t.draft.text,selections:Object.fromEntries(Object.entries(t.scoreSelections||{}).map(([k,v])=>[k,[...v].sort()]))}))')
    original=take_data()
    assert page.evaluate('proposalTourSteps.slice(0,2).map(s=>s.id)')==['duidelijke-labels','opnametoets']
    steps=page.evaluate('proposalTourSteps.map(s=>({id:s.id,title:s.title,view:s.view}))')
    order=[s['id'] for s in steps]
    for first,second in [('cue-takes','noteplek'),('noteplek','maat-aanpassen'),('maat-aanpassen','protools-sync'),('protools-sync','sterren'),('alt-best','cue-sneltoetsen'),('score-lagen','score-selecteren'),('score-selecteren','score-notes'),('score-notes','score-vergelijk'),('score-vergelijk','score-instellingen')]:
        assert order.index(first)<order.index(second),(first,second)
    selected={'sterren','opnametoets','score-notes'}
    for index,step in enumerate(steps):
        expect(page.locator('#proposal-tour-title')).to_have_text(step['title'])
        expect(page.locator('.proposal-tour-highlight')).to_be_visible()
        expect(page.locator('[data-tour-choice]')).to_be_checked()
        page.locator('[data-tour-choice]').set_checked(step['id'] in selected)
        if step['id']=='cue-aanklikken':
            page.locator('.calm-cue-list [data-select-cue="1"]').click()
            expect(page.locator('#main-panel .main-cue')).to_contain_text('1M18')
            expect(page.locator('.calm-notes > header')).to_contain_text('1M18')
            expect(page.locator('.calm-cue-list [data-select-cue="1"]')).to_have_attribute('aria-current','true')
            heading=page.locator('.calm-cue-list .cue-group.current>.calm-cue-heading')
            other=page.locator('.calm-cue-list .cue-group:not(.current)>.calm-cue-heading').first
            assert heading.evaluate('(el)=>getComputedStyle(el).backgroundColor')!=other.evaluate('(el)=>getComputedStyle(el).backgroundColor')
            assert heading.evaluate('(el)=>getComputedStyle(el).boxShadow')!='none'
            page.screenshot(path=str(ROOT/'checks/selected-cue-tour.png'))
            expect(page.locator('[data-tour-choice="cue-aanklikken"]')).not_to_be_checked()
            page.locator('.calm-cue-list [data-select-cue="0"]').click()
            expect(page.locator('#main-panel .main-cue')).to_contain_text('1M02')
            assert page.evaluate('proposalTourSteps[proposalTourIndex].id')=='cue-aanklikken'
            page.wait_for_timeout(150)
            page.screenshot(path=str(ROOT/'checks/tour-click-cues.png'))
        if step['id']=='noteplek':
            expect(page.locator('body')).to_have_class(__import__('re').compile(r'tour-take-notes'))
            for take in [1,2]:
                page.locator(f'.calm-cue-list [data-select-take="c0-t{take}"]').click()
                expect(page.locator('.calm-notes > header')).to_contain_text(f'Take {take}')
                expect(page.locator('.calm-notes .note-list')).to_contain_text('Nice entrance' if take==1 else 'Cello a little calmer')
            for selector in ['.calm-cue-list .cue-group.current','.calm-notes']:
                assert page.locator(selector).evaluate('(el)=>getComputedStyle(el).outlineStyle')=='solid'
            page.screenshot(path=str(ROOT/'checks/tour-take-notes.png'))
        if step['id']=='protools-sync':
            expect(page.locator('.proposal-tour-card')).to_contain_text('Take 3 bij ons, Take 4 bij de engineer?')
            assert 'OriginationDate' in page.evaluate('tourPromptFor(proposalTourSteps[proposalTourIndex])')
            page.screenshot(path=str(ROOT/'checks/tour-protools-sync.png'))
        if step['id']=='tijdformaat':
            assert page.evaluate('tourTarget.closest("#main-panel")!==null')
        if step['id']=='maat-aanpassen':
            picker=page.locator('.calm-notes .measure-picker').first
            picker.locator('summary').click()
            expect(picker.locator('[data-picker-measure]')).to_be_focused()
            page.wait_for_timeout(70)
            panel=picker.locator('.measure-picker-panel').bounding_box()
            card=page.locator('.proposal-tour-card').bounding_box()
            assert panel['x']+panel['width']<=card['x'] or card['x']+card['width']<=panel['x'] or panel['y']+panel['height']<=card['y'] or card['y']+card['height']<=panel['y'],(panel,card)
            page.keyboard.press('Escape')
            expect(page.locator('#proposal-tour-title')).to_have_text(step['title'])
            stamp=page.locator('.calm-notes .note-list [data-note-time-edit]').first
            original_stamp=stamp.input_value()
            stamp.click();stamp.fill('99:59');stamp.press('Escape')
            expect(stamp).to_have_value(original_stamp)
            expect(page.locator('#proposal-tour-title')).to_have_text(step['title'])
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
    expect(page.locator('#proposal-questions li')).to_have_count(page.evaluate('openQuestions().length'))
    expect(page.locator('#proposal-questions')).not_to_contain_text('⌥1–9 kiest nu de cuevolgorde, niet de cuecode.')
    expect(page.locator('#proposal-questions input[type=checkbox]')).to_have_count(0)
    page.locator('#proposal-questions [data-tour-action="close-dialog"]').first.click()
    # Selection survives reopening, unlike temporary demo notes.
    page.reload();page.locator('[data-tour-action="welcome-skip"]').click()
    assert page.evaluate('proposalTourSelection.size')==3
    page.locator('[data-proposal-action="tour"]').click()
    page.evaluate("openTourStep(proposalTourSteps.findIndex(s=>s.id==='sterren'))")
    expect(page.locator('[data-tour-choice="sterren"]')).to_be_checked()
    page.locator('[data-tour-choice="sterren"]').uncheck()
    assert not any(line.startswith('## ') and line.endswith('. Sterren in plaats van Good / NG / Hold?') for line in page.evaluate('selectedTourPrompt()').splitlines())
    page.locator('[data-tour-choice="sterren"]').check()
    page.keyboard.press('Escape');expect(page.locator('.proposal-tour-card')).to_have_count(0)
    # Guided view changes never stop a live take or lose a draft.
    page.locator('[data-proposal-view="recording"]').click();page.keyboard.press('Meta+Enter')
    assert page.evaluate('state().sessionStarted&&!running(state())')
    page.keyboard.press('Meta+Enter')
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
    for step_id in ['duidelijke-labels','opnametoets','cue-aanklikken','noteplek','maat-aanpassen','protools-sync','bereikbare-bediening','score-per-cue','score-zoom','score-selecteren','score-overzicht','score-undo']:
        index=next(i for i,step in enumerate(steps) if step['id']==step_id)
        page.evaluate('(index)=>openTourStep(index)',index)
        page.wait_for_timeout(60)
        if step_id=='cue-aanklikken':
            page.locator('.calm-cue-list [data-select-cue="1"]').click()
            expect(page.locator('#main-panel .main-cue')).to_contain_text('1M18')
            page.locator('.calm-cue-list [data-select-cue="0"]').click()
            expect(page.locator('#main-panel .main-cue')).to_contain_text('1M02')
        if step_id=='noteplek':
            for take in [1,2]:
                page.locator(f'.calm-cue-list [data-select-take="c0-t{take}"]').click()
                expect(page.locator('.calm-notes > header')).to_contain_text(f'Take {take}')
        r=page.locator('.proposal-tour-card').bounding_box()
        assert r['x']>=0 and r['y']>=0 and r['x']+r['width']<=390 and r['y']+r['height']<=844,(index,r)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),index
    page.screenshot(path=str(ROOT/'checks/tour-mobile.png'))
    # A deliberate empty selection remains empty after reload.
    page.evaluate('localStorage.setItem("mandocues-proposal-tour-v2",JSON.stringify({excluded:proposalTourSteps.map(step=>step.id)}))')
    page.reload();page.locator('[data-tour-action="welcome-start"]').click()
    expect(page.locator('[data-tour-choice="duidelijke-labels"]')).not_to_be_checked()
    assert page.evaluate('proposalTourSelection.size')==0
    assert not errors,errors
    assert not network,network
    browser.close()
print('PASS: checked-by-default suggestions, preserved deselections, welcome choices, all tour targets, opt-in exact prompts/copy/download, persistence, open questions, live-take/draft preservation and mobile tour')
