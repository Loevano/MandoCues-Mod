"""Review ten grouped suggestions, their real targets, prompts and saved opt-outs."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
ORDER=['opnametoets','planning','cue-aanklikken','noteplek','maat-aanpassen','sterren','view-toggle','score-selecteren','score-notes','score-vergelijk']
with sync_playwright() as p:
    browser=launch_chromium(p)
    context=browser.new_context(viewport={'width':1512,'height':1100})
    page=context.new_page();errors=[];network=[]
    page.add_init_script("localStorage.setItem('mandocues-proposal-tour-v1', JSON.stringify(['sterren','cue-aanklikken','maat-aanpassen']))")
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto((ROOT/'dist/index.html').as_uri())
    expect(page.locator('#proposal-welcome')).to_be_visible()
    page.locator('[data-tour-action="welcome-start"]').click()
    assert page.evaluate('proposalTourSteps.map(s=>s.id)')==ORDER
    assert page.evaluate('proposalTourSelection.size===proposalTourParts.length')
    expect(page.locator('[data-proposal-selection-count]')).to_have_text('10')
    def take_data():
        return page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,rating:t.rating,best:t.best,alt:!!t.alt,text:t.draft.text,selections:Object.fromEntries(Object.entries(t.scoreSelections||{}).map(([k,v])=>[k,[...v].sort()]))}))')
    def open_step(id):page.evaluate('(id)=>openTourStep(proposalTourSteps.findIndex(s=>s.id===id))',id)
    original=take_data()
    steps=page.evaluate('proposalTourSteps.map(s=>({id:s.id,title:s.title,view:s.view,parts:s.parts.map(p=>p.id)}))')
    selected={'sterren','opnametoets','score-notes'}
    selected_parts=sorted(part for step in steps if step['id'] in selected for part in step['parts'])
    for index,step in enumerate(steps):
        expect(page.locator('#proposal-tour-title')).to_have_text(step['title'])
        expect(page.locator('.proposal-tour-card header')).to_contain_text(f'Suggestie {index+1} van 10')
        expect(page.locator('.proposal-tour-highlight')).to_be_visible()
        assert page.evaluate('tourTarget.matches(proposalTourSteps[proposalTourIndex].target)')
        assert page.evaluate('!tourTarget.matches(".proposal-view-toggle")')
        assert page.evaluate('proposalView')==step['view']
        expect(page.locator('[data-tour-choice]')).to_be_checked()
        page.locator('[data-tour-choice]').set_checked(step['id'] in selected)
        if step['id']=='cue-aanklikken':
            for cue in [1,0]:
                page.locator(f'.calm-cue-list [data-select-cue="{cue}"]').click()
                expect(page.locator('#main-panel .main-cue')).to_contain_text('1M18' if cue else '1M02')
                expect(page.locator('.calm-notes > header')).to_contain_text('1M18' if cue else '1M02')
            expect(page.locator('.tour-shortcuts')).to_be_visible()
            expect(page.locator('.tour-shortcuts summary')).to_have_count(0)
            expect(page.locator('.tour-shortcuts')).to_contain_text('⌥[ en ⌥]')
            expect(page.locator('.tour-shortcuts')).to_contain_text('⌥1 t/m ⌥9')
            expect(page.locator('.tour-shortcuts')).to_contain_text('Houd ⌥ + ⌘ vast')
        if step['id']=='noteplek':
            for take in [1,2]:
                page.locator(f'.calm-cue-list [data-select-take="c0-t{take}"]').click()
                expect(page.locator('.calm-notes > header')).to_contain_text(f'Take {take}')
                expect(page.locator('.calm-notes .note-list')).to_contain_text('Nice entrance' if take==1 else 'Cello a little calmer')
            for selector in ['.calm-cue-list .cue-group.current','.calm-notes']:
                assert page.locator(selector).evaluate('(el)=>getComputedStyle(el).outlineStyle')=='solid'
        if step['id']=='maat-aanpassen':
            assert page.evaluate('tourTarget.matches(".calm-notes .composer-footer")')
            page.locator('.tour-extra summary').click()
            expect(page.locator('.tour-extra')).to_contain_text('vergelijk de opgeslagen opnametijden uit de originele WAV’s met ons take-log')
            assert 'OriginationDate' in page.evaluate('tourPromptFor(proposalTourSteps[proposalTourIndex])')
            page.locator('.tour-extra summary').click()
            picker=page.locator('.calm-notes .measure-picker').first
            picker.locator('summary').click()
            expect(picker.locator('[data-picker-measure]')).to_be_focused()
            page.wait_for_timeout(100)
            panel=picker.locator('.measure-picker-panel').bounding_box();card=page.locator('.proposal-tour-card').bounding_box()
            assert panel['x']+panel['width']<=card['x'] or card['x']+card['width']<=panel['x'] or panel['y']+panel['height']<=card['y'] or card['y']+card['height']<=panel['y'],(panel,card)
            page.keyboard.press('Escape')
            stamp=page.locator('.calm-notes .note-list [data-note-time-edit]').first
            original_stamp=stamp.input_value();stamp.click();stamp.fill('99:59');stamp.press('Escape')
            expect(stamp).to_have_value(original_stamp)
        if step['id']=='view-toggle':
            expect(page.locator('.score-canvas')).to_be_visible()
            expect(page.locator('.score-display-menu')).to_be_visible()
        if step['id']=='score-selecteren':
            # The tutorial card must leave both the take picker and score usable.
            page.locator('.score-take-picker [data-select-take="c0-t2"]').click()
            cell=page.locator('[data-score-page="1"] [data-score-measure="3"][data-score-instrument="vln1"]')
            cell.click(modifiers=['Meta'],position={'x':8,'y':8})
            assert page.evaluate('scoreSelection(state(),takeById(state(),state().selected)).some(k=>k==="3"||k.startsWith("3:"))')
            page.locator('[data-score-undo]').click()
        if step['id']=='score-notes':
            cell=page.locator('[data-score-page="1"] [data-score-measure="3"][data-score-instrument="vln1"]')
            cell.dblclick(position={'x':8,'y':8})
            page.locator('#score-comment-text').fill('Tour interaction check')
            page.locator('#score-comment-text').press('Enter')
            expect(page.locator('.score-text-annotation').filter(has_text='Tour interaction check')).to_be_visible()
            page.locator('[data-score-undo]').click()
            expect(page.locator('.score-text-annotation').filter(has_text='Tour interaction check')).to_have_count(0)
            # Following a saved note scrolls to page 2; the highlight follows that page.
            page.locator('.cutlist-notes-list [data-goto]').first.click()
            page.wait_for_timeout(150)
            assert page.evaluate('Number(tourTarget.dataset.scorePage)')==2
        if step['id']=='score-vergelijk':
            for take,modifiers in [(1,[]),(2,['Meta'])]:
                page.locator(f'.score-take-picker [data-select-take="c0-t{take}"]').click(modifiers=modifiers)
            assert page.evaluate('scoreVisibleTakes(state()).length')==2
            page.locator('[data-score-toggle]').click()
            expect(page.locator('.all-takes-view')).to_be_visible()
            assert page.evaluate('tourTarget.matches(".score-take-picker")')
            page.locator('[data-score-toggle]').click()
            expect(page.locator('.score-canvas')).to_be_visible()
        page.wait_for_timeout(70)
        card=page.locator('.proposal-tour-card').bounding_box()
        assert card['x']>=0 and card['y']>=0 and card['x']+card['width']<=1512 and card['y']+card['height']<=1100,(step,card)
        page.screenshot(path=str(ROOT/f'checks/compact-tour-{index+1}.png'))
        page.locator('[data-tour-action="next"]').click()
    expect(page.locator('#proposal-prompt')).to_be_visible()
    expect(page.locator('.tour-summary-choice')).to_have_count(10)
    prompt=page.evaluate('selectedTourPrompt()')
    assert page.evaluate('Array.from(proposalTourSelection).sort()')==selected_parts
    for step in steps:
        included=any(line.endswith('. '+step['title']) for line in prompt.splitlines() if line.startswith('## '))
        assert included==(step['id'] in selected),step
    assert 'Good / NG / Hold' in prompt and 'Alt-toggle' in prompt
    assert 'Dubbelklik' in prompt and 'doelmaat' in prompt
    assert take_data()==original
    page.evaluate('Object.defineProperty(navigator,"clipboard",{configurable:true,value:{writeText:async text=>{window.copiedTourPrompt=text;}}})')
    page.locator('[data-tour-action="copy"]').click();assert page.evaluate('window.copiedTourPrompt')==prompt
    with page.expect_download() as download:page.locator('[data-tour-action="download"]').click()
    target=ROOT/'checks/tour-prompt.md';download.value.save_as(str(target));assert target.read_text()==prompt
    page.locator('#proposal-prompt [data-tour-action="close-dialog"]').click()
    page.locator('[data-proposal-action="questions"]').click()
    expect(page.locator('#proposal-questions li')).to_have_count(page.evaluate('openQuestions().length'))
    expect(page.locator('#proposal-questions input[type=checkbox]')).to_have_count(0)
    page.locator('#proposal-questions [data-tour-action="close-dialog"]').first.click()
    page.reload();page.locator('[data-tour-action="welcome-skip"]').click()
    assert page.evaluate('Array.from(proposalTourSelection).sort()')==selected_parts
    expect(page.locator('[data-proposal-selection-count]')).to_have_text('3')
    # A live new take has no saved notes: metadata must target the draft, not view buttons.
    page.locator('[data-proposal-view="recording"]').click()
    page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
    live=page.evaluate('running(state()).id');page.locator('[data-draft]').fill('Draft kept through tour')
    open_step('maat-aanpassen')
    assert page.evaluate('tourTarget.matches(".calm-notes .composer-footer")')
    assert page.evaluate('tourTarget.querySelector("[data-draft-clock]").dataset.take')==live
    page.locator('[data-proposal-view="cutlist"]').click();page.wait_for_timeout(100)
    assert page.evaluate('tourTarget===null');expect(page.locator('.proposal-tour-highlight')).to_be_hidden()
    open_step('maat-aanpassen');assert page.evaluate('tourTarget.matches(".calm-notes .composer-footer")')
    open_step('view-toggle');assert page.evaluate('running(state()).id')==live
    page.keyboard.press('Escape');page.locator('[data-proposal-view="recording"]').click()
    expect(page.locator('[data-draft]')).to_have_value('Draft kept through tour')
    page.keyboard.press('Meta+Enter');assert page.evaluate('!running(state())')
    # Every step remains reachable on mobile, including its optional extra text.
    page.set_viewport_size({'width':390,'height':844})
    for step in steps:
        open_step(step['id']);page.wait_for_timeout(70)
        expect(page.locator('.proposal-tour-highlight')).to_be_visible()
        assert page.evaluate('tourTarget.matches(proposalTourSteps[proposalTourIndex].target)')
        if page.locator('details.tour-extra').count():
            page.locator('.tour-extra summary').click();page.wait_for_timeout(70)
        r=page.locator('.proposal-tour-card').bounding_box()
        assert r['x']>=0 and r['y']>=0 and r['x']+r['width']<=390 and r['y']+r['height']<=844,(step,r)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),step
    # Previously excluded individual proposals remain excluded within a merged group.
    page.evaluate('localStorage.setItem("mandocues-proposal-tour-v2",JSON.stringify({excluded:["alt-best","score-zoom","cue-sneltoetsen"]}))')
    page.reload();page.locator('[data-tour-action="welcome-skip"]').click();open_step('sterren')
    assert page.locator('[data-tour-choice="sterren"]').evaluate('(el)=>el.indeterminate')
    prompt=page.evaluate('selectedTourPrompt()')
    assert 'Good / NG / Hold' in prompt and 'Alt-toggle' not in prompt
    assert 'trackpad-knijpzoom' not in prompt and 'twee cijfers: houd' not in prompt
    page.locator('[data-proposal-action="prompt"]').click()
    assert page.locator('[data-tour-choice="sterren"]').evaluate('(el)=>el.indeterminate')
    page.locator('[data-tour-choice="sterren"]').uncheck()
    page.locator('[data-tour-choice="sterren"]').check()
    assert 'Alt-toggle' in page.evaluate('selectedTourPrompt()')
    # Explicitly excluding everything remains empty after reload.
    page.evaluate('localStorage.setItem("mandocues-proposal-tour-v2",JSON.stringify({excluded:proposalTourParts.map(part=>part.id)}))')
    page.reload();page.locator('[data-tour-action="welcome-start"]').click()
    expect(page.locator('[data-tour-choice="opnametoets"]')).not_to_be_checked()
    assert page.evaluate('proposalTourSelection.size')==0
    assert not errors,errors
    assert not network,network
    browser.close()
print('PASS: ten steps, correct targets including empty live takes, mobile, default/grouped choices, old individual opt-outs, exact prompts, shared state and optional detail')
