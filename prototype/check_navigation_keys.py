"""Cue/take keys share semantics, support two digits, and protect editing/live state."""
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
    # Welcome/prompt dialogs never accept app navigation, even with body focus.
    page.keyboard.press('Alt+1')
    assert page.evaluate('state().selected')=='c0-t2'
    page.locator('[data-tour-action="welcome-skip"]').click()
    page.evaluate('''()=>{
        const s=state();
        for(let n=3;n<=35;n++)if(n!==4)s.takes[0].push(newTake(0,n));
        s.takes[0].push(newTake(0,1,false,'overdub'));
        s.takes[0].find(t=>t.num===12).draft.text='Take twelve draft';
        renderDemo();
    }''')
    def selected():return page.evaluate('state().selected')
    def focus():page.locator('.score-canvas' if page.evaluate('proposalView')=='cutlist' else '#cue-scroll').focus()
    def prefix():
        focus()
        page.keyboard.down('Alt');page.keyboard.down('Meta')
        expect(page.locator('.take-number-entry')).to_contain_text('Release ⌥⌘')
        page.keyboard.up('Meta');page.keyboard.up('Alt')
        expect(page.locator('.take-number-entry')).to_contain_text('Take __')
    def number(n):
        prefix()
        page.keyboard.press(str(n)[0])
        expect(page.locator('.take-number-entry')).to_contain_text('Take '+str(n)[0]+'_')
        page.keyboard.press(str(n)[1])
        expect(page.locator('.take-number-entry')).to_have_count(0)
    for view in ['recording','cutlist']:
        page.locator(f'[data-proposal-view="{view}"]').click();focus()
        page.keyboard.press('Alt+1');assert selected()=='c0-t1'
        page.keyboard.press('Alt+2');assert selected()=='c0-t2'
        assert page.evaluate('state().cue')==0
        page.keyboard.press('Alt+4');assert selected()=='c0-t2' # Missing number is not row 4.
        page.keyboard.press('Alt+]');assert selected()=='c0-t3'
        page.keyboard.press('Alt+]');assert selected()=='c0-t5'
        page.keyboard.press('Alt+[');assert selected()=='c0-t3'
        # Option produces other printable characters on Mac; physical codes still work.
        page.evaluate('document.activeElement.dispatchEvent(new KeyboardEvent("keydown",{key:"™",code:"Digit2",altKey:true,bubbles:true,cancelable:true}))')
        assert selected()=='c0-t2'
        for prop in ['repeat:true','isComposing:true']:
            page.evaluate('document.activeElement.dispatchEvent(new KeyboardEvent("keydown",{key:"¡",code:"Digit1",altKey:true,bubbles:true,cancelable:true,'+prop+'}))')
            assert selected()=='c0-t2'
        number(12);assert selected()=='c0-t12'
        number(34);assert selected()=='c0-t34'
        number(99);assert selected()=='c0-t34'
        page.keyboard.press('Alt+]');assert selected()=='c0-t35'
        page.keyboard.press('Alt+]');assert selected()=='c0-od1'
        page.keyboard.press('Alt+]');assert selected()=='c0-od1'
        page.keyboard.press('Alt+[');assert selected()=='c0-t35'
        page.keyboard.press('Alt+1');assert selected()=='c0-t1' # Ordinary take, not Overdub 1.
        page.keyboard.press('Alt+[');assert selected()=='c0-t1' # No wrap at first take.
        page.keyboard.press(']');assert page.evaluate('state().cue')==1
        page.keyboard.press('[');assert page.evaluate('state().cue')==0
        # Escape, timeout, blur and clicking cancel incomplete two-digit entries.
        prefix();page.keyboard.press('1');page.keyboard.press('Escape')
        expect(page.locator('.take-number-entry')).to_have_count(0)
        before=selected();prefix();page.clock.run_for(5100)
        expect(page.locator('.take-number-entry')).to_have_count(0);assert selected()==before
        prefix();page.evaluate('window.dispatchEvent(new Event("blur"))')
        expect(page.locator('.take-number-entry')).to_have_count(0)
        prefix();page.locator('[data-proposal-view="'+view+'"]').click()
        expect(page.locator('.take-number-entry')).to_have_count(0)
        # Command must be released before the digits; held-chord digits do not jump.
        focus();page.keyboard.down('Alt');page.keyboard.down('Meta')
        page.keyboard.press('1');assert selected()==before
        page.keyboard.up('Meta');page.keyboard.up('Alt')
        page.keyboard.press('1');page.keyboard.press('2');assert selected()=='c0-t12'
        assert page.evaluate('takeById(state(),"c0-t12").draft.text')=='Take twelve draft'
    # Score position and each take's notes/selections survive rapid key switching.
    canvas=page.locator('.score-canvas');canvas.evaluate('(el)=>el.scrollTop=350')
    original=page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,selection:scoreSelection(state(),t),draft:t.draft}))')
    top=canvas.evaluate('(el)=>el.scrollTop');focus()
    page.keyboard.press('Alt+1');page.keyboard.press('Alt+2')
    assert abs(canvas.evaluate('(el)=>el.scrollTop')-top)<=1
    assert page.evaluate('allTakes(state()).map(t=>({id:t.id,notes:t.notes,selection:scoreSelection(state(),t),draft:t.draft}))')==original
    # Do not change takes or cues mid-selection drag.
    page.locator('[data-score-page="1"] [data-score-cell="2:vln2"]').scroll_into_view_if_needed()
    cell=page.locator('[data-score-page="1"] [data-score-cell="2:vln2"]').bounding_box()
    page.keyboard.down('Meta');page.mouse.move(cell['x']+5,cell['y']+5);page.mouse.down()
    page.mouse.move(cell['x']+30,cell['y']+20)
    page.keyboard.up('Meta');page.keyboard.press('Alt+1');assert selected()=='c0-t2'
    page.keyboard.press(']');assert page.evaluate('state().cue')==0
    page.mouse.up()
    # Take choice during recording only changes the editing layer.
    focus();page.keyboard.press('Meta+Enter');page.keyboard.press('Meta+Enter')
    live=page.evaluate('running(state()).id')
    page.keyboard.press('Alt+1');assert selected()=='c0-t1'
    page.keyboard.press(']');assert page.evaluate('state().cue')==0
    assert page.evaluate('running(state()).id')==live
    page.keyboard.press('Meta+Enter');assert page.evaluate('!running(state())')
    # Text editors retain Option characters, brackets, and normal digit input.
    page.locator('[data-proposal-view="recording"]').click()
    focus();page.keyboard.press('Alt+1')
    field=page.locator('[data-draft="c0-t1"]');field.fill('Draft')
    field.press('Alt+2');assert selected()=='c0-t1'
    field.press(']');assert page.evaluate('state().cue')==0
    field.press('Alt+Meta');expect(page.locator('.take-number-entry')).to_have_count(0)
    page.locator('[data-proposal-action="prompt"]').click()
    page.keyboard.press('Alt+2');page.keyboard.press(']');assert selected()=='c0-t1'
    page.locator('#proposal-prompt [data-tour-action="close-dialog"]').click()
    # Prefix Escape cancels only the entry, keeping the active tutorial step.
    page.evaluate('openTourStep(proposalTourSteps.findIndex(s=>s.id==="cue-sneltoetsen"))')
    prefix();page.keyboard.press('Escape')
    expect(page.locator('.proposal-tour-card')).to_be_visible()
    assert not errors,errors
    browser.close()
print('PASS: shared cue/take keys, actual take numbers, two-digit prefix, cancellation, Mac key codes, text/modal/drag protection, drafts, score position and live take isolation')
