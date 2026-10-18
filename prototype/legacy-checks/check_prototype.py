from browser_support import launch_chromium
"""Check the actual standalone handoff in temporary Chrome profiles."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'checks';OUT.mkdir(exist_ok=True)
URL=(ROOT/'dist/index.html').as_uri()
errors,external=[],[]
ideas=json.loads((ROOT/'src/content.json').read_text())
discussion=json.loads((ROOT/'src/discussion.json').read_text())
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':1100},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto(URL)
    expect(page.locator('.suggestion-card')).to_have_count(len(ideas))
    expect(page.locator('h1')).to_contain_text('van Floris')
    expect(page.locator('.small-suggestions-list li')).to_have_count(6)
    expect(page.locator('.small-suggestions-list li').first).to_contain_text('1–5 sterren')
    assert page.locator('.small-suggestions').bounding_box()['y']<page.locator('.prototype-collection').bounding_box()['y']
    assert not any(x in page.locator('body').inner_text().lower() for x in ['screenshots','bronstatus','contextchat','opnamestatus'])
    page.wait_for_timeout(250)
    page.screenshot(path=str(OUT/'01-overzicht.png'),full_page=True)
    page.locator('a[href="#cue-take"]').click()
    expect(page.locator('#main-panel')).to_have_count(1)
    expect(page.locator('#details-0 .take-block')).to_have_count(3)
    page.locator('[data-open-cue="1"]').click()
    page.locator('[data-select-cue="1"]').click()
    page.locator('[data-take-best="c1-t2"]').click()
    expect(page.locator('[data-take-best="c1-t1"]')).to_have_attribute('aria-pressed','false')
    page.locator('#details-1 [data-rating-key="c1-t2"][data-stars="5"]').click()
    expect(page.locator('#details-1 [data-rating-key="c1-t2"][data-stars="5"]')).to_have_attribute('aria-pressed','true')
    page.locator('[data-action="copy"]').first.click()
    expect(page.locator('#toast')).to_contain_text('gekopieerd')
    print('PASS: shared recording shell, cue/take data, stars, unique Best and prompt copy',flush=True)

    page.goto(URL+'#bediening')
    page.evaluate('state().controlsPrevious=true;renderDemo()')
    expect(page.locator('.sticky-slot')).to_have_attribute('aria-hidden','true')
    expect(page.locator('#main-panel')).to_be_visible()
    expect(page.locator('.main-panel .session-metrics')).to_be_visible()
    top_note=page.locator('#main-panel [data-draft="c0-t2"]')
    expect(top_note).to_be_visible()
    expect(page.locator('#main-panel [data-cue-draft="0"]')).to_be_visible()
    top_note.fill('Notitie direct vanaf het beginscherm')
    expect(page.locator('.grouped-list [data-draft="c0-t2"]')).to_have_value('Notitie direct vanaf het beginscherm')
    top_note.press('Enter')
    expect(page.locator('#main-panel .start-recent')).to_contain_text('Notitie direct vanaf het beginscherm')
    expect(page.locator('.grouped-list [data-notes-for="c0-t2"] .note-card')).to_have_count(2)
    assert page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop')==0
    page.screenshot(path=str(OUT/'08-notities-beginscherm.png'),full_page=True)
    page.locator('#main-panel [data-action="record"]').click()
    expect(page.locator('.main-panel .stop')).to_be_visible()
    # No floating-stop flash between the main button and compact bar, in either direction.
    samples=page.evaluate('''async()=>{
        const area=document.querySelector('#cue-scroll');
        const max=Math.min(area.scrollHeight-area.clientHeight,document.querySelector('#main-panel').offsetHeight+80);
        const samples=[];
        const positions=[];
        for(let y=0;y<=max;y+=13)positions.push(y);
        positions.push(max,...positions.slice().reverse());
        for(const y of positions){
            area.scrollTop=y;
            await new Promise(requestAnimationFrame);
            await new Promise(requestAnimationFrame);
            samples.push({y,floating:!document.querySelector('#recording-dock').hidden,compact:document.querySelector('.sticky-slot').getAttribute('aria-hidden')==='false'});
        }
        return samples;
    }''')
    assert not any(row['floating'] for row in samples),samples
    assert any(row['compact'] for row in samples),samples
    page.locator('.prompt-card summary').click()
    page.set_viewport_size({'width':1512,'height':500})
    page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
    expect(page.locator('#recording-dock')).to_be_visible()
    page.set_viewport_size({'width':1512,'height':1100})
    page.evaluate('window.scrollTo(0,0)')
    expect(page.locator('#recording-dock')).to_be_hidden()
    page.locator('.prompt-card summary').click()
    print('PASS: no floating-stop flash when scrolling A up/down; fallback remains reachable outside workspace',flush=True)
    page.locator('[data-action="scroll-takes"]').click()
    page.wait_for_function('document.querySelector(".sticky-slot").getAttribute("aria-hidden")==="false"')
    scroll_before=page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop')
    page.locator('.sticky-slot [data-action="record"]').click()
    assert abs(page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop')-scroll_before)<3, (scroll_before,page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop'))
    page.locator('.grouped-list [data-draft="c0-t3"]').fill('Concept blijft bij deze take')
    page.locator('[data-variant="B"]').click()
    expect(page.locator('.main-panel-side .session-metrics')).to_be_visible()
    expect(page.locator('#main-panel [data-draft]')).to_have_count(0)
    expect(page.locator('.grouped-list [data-draft="c0-t3"]')).to_be_visible()
    expect(page.locator('.control-comparison')).to_contain_text('Controls stay on the left')
    assert page.locator('#main-panel').bounding_box()['x']<page.locator('.side-scroll').bounding_box()['x']
    expect(page.locator('.grouped-list [data-draft="c0-t3"]')).to_have_value('Concept blijft bij deze take')
    expect(page.locator('.cue-general').first).to_contain_text('Cue notes')
    fold=page.locator('.cue-general-fold').first
    fold.locator('summary').click()
    fold.locator('textarea').fill('Algemene afspraak in variant B')
    fold.locator('textarea').press('Enter')
    expect(fold).to_have_attribute('open','')
    expect(fold).to_contain_text('Algemene afspraak in variant B')
    fold.locator('summary').click()
    assert 'SESSION PLAN' not in page.locator('#demo').inner_text()
    page.locator('#cue-scroll').evaluate('(el)=>el.scrollTop=0')
    page.screenshot(path=str(OUT/'02-bediening-zijpaneel.png'),full_page=True)
    page.locator('[data-variant="A"]').click()
    page.locator('[data-action="scroll-takes"]').click()
    page.wait_for_function('document.querySelector(".sticky-slot").getAttribute("aria-hidden")==="false"')
    page.screenshot(path=str(OUT/'03-bediening-scroll.png'),full_page=True)
    # Selecting a cue is separate from expanding it, in both control layouts.
    for v in ['A','B']:
        page.locator(f'[data-variant="{v}"]').click()
        page.locator('[data-select-cue="0"]').click()
        field=page.locator('.grouped-list [data-draft="c0-t3"]')
        expect(field).to_have_value('Concept blijft bij deze take')
        page.locator('.grouped-list [data-toggle-take="c0-t3"]').click()
        expect(field).to_be_hidden()
        page.locator('.grouped-list [data-toggle-take="c0-t3"]').click()
        expect(field).to_have_value('Concept blijft bij deze take')
        page.locator('[data-select-cue="1"]').press('Enter')
        expect(page.locator('.main-cue')).to_contain_text('1M18')
        expect(page.locator('#details-1')).to_be_visible()
        page.locator('[data-open-cue="1"]').click()
        expect(page.locator('#details-1')).to_be_hidden()
        expect(page.locator('.main-cue')).to_contain_text('1M18')
        page.locator('[data-select-cue="2"]').click()
        expect(page.locator('.main-cue')).to_contain_text('1M34')
        expect(page.locator('#details-2')).to_contain_text('No takes')
        page.locator('[data-select-cue="1"]').click()
        page.locator('#main-panel [data-action="record"]').click()
        page.locator('[data-select-cue="2"]').click()
        expect(page.locator('.main-cue')).to_contain_text('1M18')
        expect(page.locator('#toast')).to_contain_text('Stop the active')
        expect(page.locator('.main-panel .rec-status')).to_contain_text('RECORDING')
        page.keyboard.press('Meta+Enter')
        page.locator('[data-select-cue="0"]').click()
        expect(page.locator('.grouped-list [data-draft="c0-t3"]')).to_have_value('Concept blijft bij deze take')
    print('PASS: cue selection by click/keyboard, separate disclosure, empty cues, recording guard and collapsible take drafts in A/B',flush=True)
    print('PASS: full panel retained, compact bar only after scrolling, stop/draft/scroll preserved, notes in both variants',flush=True)

    page.goto(URL+'#bediening')
    page.evaluate('state().controlsPrevious=true;renderDemo()')
    page.locator('[data-variant="A"]').click()
    page.locator('[data-action="reset"]').click()
    page.evaluate('state().controlsPrevious=true;renderDemo()')
    field=page.locator('#main-panel [data-draft="c0-t2"]')
    for n in range(10):
        field.fill(f'Bovenste note {n+1}: teruglezen en maat controleren.')
        expect(page.locator('#main-panel [data-measure-input="c0-t2"]')).to_have_value('19')
        field.press('Enter')
    history=page.locator('.start-recent')
    expect(history.locator('.note-card')).to_have_count(11)
    assert history.evaluate('(el)=>getComputedStyle(el).overflowY')=='visible'
    assert history.evaluate('(el)=>Math.abs(el.scrollHeight-el.clientHeight)<=1')
    last=history.locator('.note-card').last
    picker=last.locator('.measure-picker')
    picker.locator('summary').click()
    expect(picker).to_have_attribute('open','')
    last.screenshot(path=str(OUT/'11-maatkeuze.png'))
    picker.locator('[data-pick-measure="20"]').click()
    expect(last.locator('.measure-chip')).to_contain_text('20')
    expect(picker).not_to_have_attribute('open','')
    picker.locator('summary').press('Enter')
    picker.locator('[data-picker-measure]').fill('0')
    picker.locator('[data-apply-measure]').click()
    expect(last.locator('.measure-chip')).to_contain_text('20')
    picker.locator('[data-picker-measure]').fill('27')
    picker.locator('[data-picker-measure]').press('Enter')
    expect(last.locator('.measure-chip')).to_contain_text('27')
    expect(page.locator('.grouped-list [data-notes-for="c0-t2"] .note-card').last.locator('.measure-chip')).to_contain_text('27')
    picker.locator('summary').click()
    page.keyboard.press('Escape')
    expect(picker).not_to_have_attribute('open','')
    expect(picker.locator('summary')).to_be_focused()
    picker.locator('summary').click()
    page.locator('.control-comparison').click()
    expect(picker).not_to_have_attribute('open','')
    page.locator('#main-panel [data-stars="4"]').click()
    expect(last.locator('.measure-chip')).to_contain_text('27')
    expect(page.locator('#main-panel .take-measures')).to_contain_text('Bars 17–22')
    page.locator('#main-panel [data-follow-measure="c0-t2"]').uncheck()
    page.locator('#main-panel [data-measure-input="c0-t2"]').fill('')
    field.fill('Deze note heeft geen maat');field.press('Enter')
    expect(history.locator('.note-card').last.locator('.measure-chip')).to_have_count(0)
    page.locator('[data-variant="B"]').click()
    changed=page.locator('.grouped-list [data-notes-for="c0-t2"] .note-card').nth(10)
    changed.locator('.measure-picker summary').click()
    changed.locator('[data-pick-measure="28"]').click()
    page.locator('[data-variant="A"]').click()
    expect(history.locator('.note-card').nth(10).locator('.measure-chip')).to_contain_text('28')
    assert '· wijzig' not in history.inner_text()
    page.screenshot(path=str(OUT/'09-alle-notes-directe-maatkeuze.png'),full_page=True)
    print('PASS: full note history without inner scrolling; direct measure choices, arbitrary input, validation, keyboard/outside dismissal and mirrored data',flush=True)

    page.goto(URL+'#notities')
    field=page.locator('#details-0 [data-draft="c0-t2"]')
    field.fill('Opmerking met gewone spaties');captured=page.locator('#details-0 [data-draft-clock="c0-t2"]').inner_text()
    field.press('Enter');last=page.locator('#details-0 [data-notes-for="c0-t2"] .note-card').last
    expect(last).to_contain_text('Opmerking met gewone spaties')
    assert last.locator('.time-chip').inner_text().startswith(captured)
    field.fill('Concept blijft staan');field.press('Space');field.press('Control+Enter')
    assert page.evaluate('!!running(state())')
    expect(field).to_have_value('Concept blijft staan ')
    field.press('Meta+Enter')
    expect(field).to_have_value('Concept blijft staan ')
    assert page.evaluate('!running(state())')
    page.evaluate('document.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",metaKey:true,repeat:true,bubbles:true}))');assert page.evaluate('!running(state())')
    expect(page.locator('.note-composer .composer-stop')).to_have_count(0)
    page.locator('[data-variant="B"]').click()
    expect(page.locator('#details-0 [data-draft="c0-t2"]')).to_have_value('Concept blijft staan ')
    expect(page.locator('#main-panel [data-draft="c0-t2"]')).to_have_value('Concept blijft staan ')
    print('PASS: common note editor, Enter/time anchor, mirrored draft and Command+Enter without accidental note submission or key-repeat toggles',flush=True)

    page.goto(URL+'#partituur')
    expect(page.locator('[data-variant]')).to_have_count(2)
    expect(page.locator('.score-paper')).to_have_count(3)
    cell=page.locator('.score-paper[data-score-page="2"] [data-score-measure="18"][data-score-instrument="vln1"]')
    cell.dblclick()
    page.locator('#score-comment-text').fill('Controleer de cello hier')
    page.locator('#score-comment-text').press('Enter')
    expect(page.locator('.score-note-text').filter(has_text='Controleer de cello hier')).to_have_count(1)
    page.locator('[data-select-take="c0-t1"]').click()
    expect(page.locator('.score-note-text').filter(has_text='Controleer de cello hier')).to_have_count(0)
    page.locator('[data-select-take="c0-t2"]').click()
    expect(page.locator('.score-note-text').filter(has_text='Controleer de cello hier')).to_have_count(1)
    page.locator('[data-action="film"]').click();expect(page.locator('.explanation')).to_be_hidden()
    page.keyboard.press('Escape');expect(page.locator('.explanation')).to_be_visible()
    print('PASS: one full-score layout, single-click comment text, separate take layers and film mode',flush=True)

    ideas=json.loads((ROOT/'src/content.json').read_text())
    for i in ideas:
        for v in i['variants']:
            actual=page.evaluate('([id,v])=>promptFor(ideas.find(i=>i.id===id),v)',[i['id'],v])
            assert actual==(ROOT/f"dist/{i['number']}-prompt-{v}.txt").read_text()
    with page.expect_download() as dl:page.locator('#export').click()
    dl.value.save_as(str(OUT/'Suggesties-van-Floris.md'))
    doc=(OUT/'Suggesties-van-Floris.md').read_text()
    assert 'screenshots' not in doc.lower() and 'contextchat' not in doc.lower()
    assert doc.count('### A ·')==3 and doc.count('### B ·')==3
    assert '### Inklapbare takes' in doc
    assert not (ROOT/'dist/01-prompt-B.txt').exists()
    assert 'geen algemene PDF-herkenning of live score following' in doc
    page.goto(URL)
    with page.expect_download() as dl:page.locator('[data-action="export-feedback"]').click()
    dl.value.save_as(str(OUT/'Alle-notes-van-Floris.md'))
    assert (OUT/'Alle-notes-van-Floris.md').read_text()==(ROOT/'dist/Alle-notes-van-Floris.md').read_text()
    page.goto(URL+'#voor-claude')
    expect(page.locator('.implementation-builder input[type="checkbox"]')).to_have_count(len(ideas)+sum(not d.get('questionOnly') for d in discussion))
    expect(page.locator('[data-action="copy-bundle"]')).to_be_disabled()
    expect(page.locator('[data-action="download-bundle"]')).to_be_disabled()
    page.locator('[data-implementation-choice="note:sterren"]').check()
    assert '1 tot en met 5 klikbare sterren' in page.locator('.bundle-preview').text_content()
    assert ideas[0]['variants']['A'] not in page.locator('.bundle-preview').text_content()
    page.locator('[data-implementation-choice="note:sterren"]').uncheck()
    page.locator('[data-implementation-choice="idea:cue-take"]').check()
    page.locator('[data-implementation-choice="idea:bediening"]').check()
    page.locator('[data-implementation-variant="idea:bediening"]').select_option('B')
    page.locator('[data-implementation-choice="note:tijdformaat"]').check()
    combined=page.locator('.bundle-preview').text_content()
    assert ideas[0]['requirement'] in combined
    assert ideas[1]['requirement'] in combined and ideas[1]['variants']['B'] in combined
    assert ideas[1]['variants']['A'] not in combined
    assert ideas[2]['requirement'] not in combined and ideas[3]['context'] not in combined
    discussion=json.loads((ROOT/'src/discussion.json').read_text())
    assert discussion[0]['text'] in combined and discussion[1]['text'] not in combined
    assert 'Implementeer alleen dit voorstel.' not in combined
    expect(page.locator('#implementation-count')).to_have_text('3 gekozen')
    with page.expect_download() as dl:page.locator('[data-action="download-bundle"]').click()
    dl.value.save_as(str(OUT/'Claude-geselecteerde-suggesties.md'))
    assert (OUT/'Claude-geselecteerde-suggesties.md').read_text()==combined
    page.evaluate('''()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{window.copiedBundle=text;}}})''')
    page.locator('[data-action="copy-bundle"]').click()
    expect(page.locator('#toast')).to_contain_text('Selectie gekopieerd')
    assert page.evaluate('window.copiedBundle')==combined
    page.locator('[data-implementation-choice="idea:bediening"]').uncheck()
    assert ideas[1]['requirement'] not in page.locator('.bundle-preview').text_content()
    expect(page.locator('[data-implementation-variant="idea:bediening"]')).to_be_disabled()
    page.locator('[data-implementation-choice="idea:bediening"]').check()
    assert page.locator('.bundle-preview').text_content()==combined
    page.reload()
    expect(page.locator('[data-implementation-variant="idea:bediening"]')).to_have_value('B')
    assert page.locator('.bundle-preview').text_content()==combined
    page.goto(URL+'#notities')
    page.locator('[data-decision="Interessant"]').click()
    page.locator('a[href="#voor-claude"]').first.click()
    expect(page.locator('[data-implementation-choice="idea:notities"]')).not_to_be_checked()
    page.locator('[data-implementation-choice="idea:partituur"]').check()
    assert ideas[3]['context'] in page.locator('.bundle-preview').text_content()
    page.locator('.implementation-preview summary').click()
    expect(page.locator('.bundle-preview')).to_be_visible()
    page.screenshot(path=str(OUT/'10-keuze-voor-claude.png'),full_page=True)
    for checkbox in page.locator('.implementation-builder input[type="checkbox"]').all():checkbox.uncheck()
    expect(page.locator('[data-action="copy-bundle"]')).to_be_disabled()
    expect(page.locator('#implementation-count')).to_have_text('0 gekozen')
    assert not page.evaluate('combinedPrompt()')
    print('PASS: explicit suggestion selection, one variant, exact existing text, copy/download equality, persistence and exclusion',flush=True)
    for path in sorted((ROOT/'dist').glob('0*.html')):
        page.goto(path.as_uri());expect(page.locator('.work-heading h1')).to_be_visible()
    page.set_viewport_size({'width':390,'height':844})
    for id in ['',*map(lambda i:i['id'],ideas)]:
        page.goto(URL+('#'+id if id else ''))
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),id
        if id and 'B' in next(i for i in ideas if i['id']==id)['variants']:
            page.locator('[data-variant="B"]').click()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),id+' B'
            if id=='partituur':
                assert all(b.bounding_box()['width']>=90 for b in page.locator('.take-picker [data-select-take]').all())
    page.screenshot(path=str(OUT/'07-mobiel.png'),full_page=True)
    assert not errors,errors
    assert not external,external
    browser.close()
    print('PASS: all entrypoints, 8 complete matching prompts, handover download, 390px A/B layouts, no JS errors or network requests',flush=True)
