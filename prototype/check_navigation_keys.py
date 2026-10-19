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
    def release():
        page.keyboard.up('Meta');page.keyboard.up('Alt')
    def prefix(reverse=False):
        focus()
        page.keyboard.down('Meta' if reverse else 'Alt')
        page.keyboard.down('Alt' if reverse else 'Meta')
        expect(page.locator('.take-number-entry')).to_contain_text('Take __ · Type two digits')
        expect(page.locator('.take-number-entry')).not_to_contain_text('Esc')
        expect(page.locator('.take-number-entry')).not_to_contain_text('Release')
    def number(n):
        prefix()
        digits=str(n).zfill(2)
        page.keyboard.press(digits[0])
        expect(page.locator('.take-number-entry')).to_contain_text('Take '+digits[0]+'_')
        page.keyboard.press(digits[1])
        expect(page.locator('.take-number-entry')).to_have_count(0)
        before=selected();page.keyboard.press('1');page.keyboard.press('2')
        assert selected()==before # One choice per held chord.
        release()
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
        # Cue boundaries do not wrap or reset the selected take, in either view.
        first=selected();page.keyboard.press('[')
        assert page.evaluate('state().cue')==0 and selected()==first
        if view=='recording':expect(page.locator('#main-panel [data-action="prev-cue"]')).to_be_disabled()
        page.evaluate('selectCue(state(),cues.length-1)');focus()
        last=selected();page.keyboard.press(']')
        assert page.evaluate('state().cue===cues.length-1') and selected()==last
        if view=='recording':expect(page.locator('#main-panel [data-action="next-cue"]')).to_be_disabled()
        page.keyboard.press('[');assert page.evaluate('state().cue===cues.length-2')
        page.keyboard.press(']');assert page.evaluate('state().cue===cues.length-1')
        page.evaluate('selectCue(state(),0)');focus()
        # Releasing either modifier cancels partial input, in either press order.
        before=selected()
        for reverse in [False,True]:
            for released in ['Alt','Meta']:
                prefix(reverse);page.keyboard.press('1')
                page.keyboard.up(released)
                expect(page.locator('.take-number-entry')).to_have_count(0)
                release();page.keyboard.press('2');assert selected()==before
        # Hold as long as needed; there is no timeout while modifiers stay down.
        prefix();page.clock.run_for(6100)
        expect(page.locator('.take-number-entry')).to_be_visible()
        page.keyboard.press('0');page.keyboard.press('2');assert selected()=='c0-t2';release()
        # Physical Mac Option key codes work for held two-digit entry, too.
        prefix()
        for code in ['Digit1','Digit2']:
            page.evaluate('(code)=>document.activeElement.dispatchEvent(new KeyboardEvent("keydown",{key:"œ",code,altKey:true,metaKey:true,bubbles:true,cancelable:true}))',code)
        assert selected()=='c0-t12';release()
        # Repeated digits / IME never turn one physical press into two digits.
        prefix();page.keyboard.down('1');page.keyboard.down('1')
        expect(page.locator('.take-number-entry')).to_contain_text('Take 1_')
        page.keyboard.up('1');release()
        prefix();page.evaluate('document.activeElement.dispatchEvent(new KeyboardEvent("keydown",{key:"1",code:"Digit1",altKey:true,metaKey:true,isComposing:true,bubbles:true,cancelable:true}))')
        expect(page.locator('.take-number-entry')).to_have_count(0);release()
        # Escape remains a harmless fallback; no instruction is needed in the UI.
        prefix();page.keyboard.press('1');page.keyboard.press('Escape')
        expect(page.locator('.take-number-entry')).to_have_count(0);release()
        prefix();page.evaluate('window.dispatchEvent(new Event("blur"))')
        expect(page.locator('.take-number-entry')).to_have_count(0);release()
        prefix();page.locator('[data-proposal-view="'+view+'"]').click()
        expect(page.locator('.take-number-entry')).to_have_count(0);release()
        # Digits typed after releasing the chord never choose a take.
        before=selected();prefix();release()
        expect(page.locator('.take-number-entry')).to_have_count(0)
        page.keyboard.press('1');page.keyboard.press('2');assert selected()==before
        number(12);assert selected()=='c0-t12'
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
    prefix();page.keyboard.press('Escape');release()
    expect(page.locator('.proposal-tour-card')).to_be_visible()
    assert not errors,errors
    browser.close()
print('PASS: shared cue/take keys, non-wrapping cue boundaries, actual take numbers, held two-digit entry, release cancellation, Mac key codes, text/modal/drag protection, drafts, score position and live take isolation')
