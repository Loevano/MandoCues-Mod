"""All-take overview: navigation, notes, independent layers and fixed tools."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium

ROOT = Path(__file__).resolve().parent
errors = []
with sync_playwright() as p:
    browser = launch_chromium(p)
    page = browser.new_page(viewport={'width': 1512, 'height': 1100})
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto((ROOT / 'dist/index.html').as_uri() + '#partituur')
    for variant in ['A', 'B']:
        page.locator(f'[data-variant="{variant}"]').click()
        page.locator('[data-action="reset"]').click()
        page.evaluate('''() => {
            const s=state(),t=s.takes[s.cue][0];
            t.best=false;t.alt=false;
            t.scoreSelections={[s.doc.id]:['1:vln1','2','35']};
            t.notes.push({id:'overview-test',source:s.doc.id,page:3,measure:35,
                text:'Watch the entrance',instruments:['vc'],at:0});
            s.scoreSeeOtherTakes=false;
        }''')
        page.locator('[data-cutlist-view="all"]').click()
        expect(page.locator('.all-takes-table tbody > tr')).to_have_count(2)
        expect(page.locator('.all-takes-table thead th')).to_have_count(42)
        first = page.locator('.all-takes-table tbody > tr').first
        expect(first.locator('.has-selection')).to_have_count(3)
        expect(first.locator('.partial-selection')).to_have_count(1)
        expect(page.locator('.all-takes-view .star-rating')).to_have_count(0)
        tools = first.locator('.all-takes-tools').bounding_box()
        first.locator('[data-take-best]').click()
        first.locator('[data-take-alt]').click()
        assert tools == first.locator('.all-takes-tools').bounding_box()
        expect(first.locator('[data-take-best]')).to_have_attribute('aria-pressed', 'true')
        expect(first.locator('[data-take-alt]')).to_have_text('Alt 1')
        first.locator('[data-cutlist-notes="35"]').click()
        expect(page.locator('.all-takes-preview')).to_contain_text('Watch the entrance')
        page.locator('.all-takes-preview [data-cutlist-bar]').click()
        expect(page.locator('[data-cutlist-view="score"]')).to_have_attribute('aria-pressed', 'true')
        assert page.evaluate('state().selected') == 'c0-t1'
        assert page.evaluate('state().page') == 3
        expect(page.locator('.score-paper[data-score-page="3"] .chosen')).to_have_count(4)
        expect(page.locator('.score-paper[data-score-page="3"] .chosen').first).to_be_in_viewport()
        # Sidebar note editing must reveal the score rather than an invisible editor.
        page.locator('[data-cutlist-view="all"]').click()
        page.locator('.cutlist-sidebar [data-score-note="overview-test"]').click()
        expect(page.locator('#score-comment-text')).to_have_value('Watch the entrance')
        page.locator('[data-score-cancel-comment]').click()
        # A normal switch back preserves the score's reading position.
        canvas_top = page.locator('.score-canvas').evaluate('(el)=>el.scrollTop')
        page.locator('[data-cutlist-view="all"]').click()
        page.locator('[data-cutlist-view="score"]').click()
        assert abs(page.locator('.score-canvas').evaluate('(el)=>el.scrollTop')-canvas_top) <= 1
        page.locator('[data-score-setting="scoreLinkInstruments"]').click()
        page.locator('[data-cutlist-view="all"]').click()
        page.locator('[data-cutlist-expand="c0-t1"]').click()
        expect(page.locator('.all-takes-instrument')).to_have_count(4)
        row = page.locator('.all-takes-instrument').first
        expect(row.locator('.has-selection')).to_have_count(3)
        row.locator('[data-cutlist-bar="1"]').click()
        expect(page.locator('.score-paper[data-score-page="1"] .chosen')).to_have_count(1)
        assert page.evaluate('state().scoreFocus.instruments') == ['vln1']
        # Opening another layer leaves the running take alone.
        other_selection = page.evaluate('scoreSelection(state(),takeById(state(),"c0-t2"))')
        page.evaluate('toggleRecord(state())')
        live = page.evaluate('running(state()).id')
        page.locator('[data-cutlist-view="all"]').click()
        page.locator('[data-cutlist-take="c0-t2"]').click()
        assert page.evaluate('running(state()).id') == live
        page.locator('[data-cutlist-take="c0-t2"]').click(modifiers=['Meta'])
        page.locator('.all-takes-table [data-cutlist-bar="2"][data-take="c0-t2"]').click()
        assert page.evaluate('running(state()).id') == live
        assert page.evaluate('scoreSelection(state(),takeById(state(),"c0-t2"))') == other_selection
        page.evaluate('toggleRecord(state())')
        page.locator('[data-cutlist-view="all"]').click()
        page.locator('#score-cue').select_option('1')
        expect(page.locator('.all-takes-view h3')).to_contain_text(page.evaluate('cues[1][0]'))
        expect(page.locator('.all-takes-preview')).to_have_count(0)
        page.locator('.all-takes-scroll').evaluate('(el)=>el.scrollLeft=500')
        offset = page.locator('.all-takes-scroll').evaluate('(el)=>el.scrollLeft')
        page.locator('.all-takes-tools [data-take-best]').first.click()
        assert page.locator('.all-takes-scroll').evaluate('(el)=>el.scrollLeft') == offset
        page.set_viewport_size({'width': 640, 'height': 1000})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.set_viewport_size({'width': 1512, 'height': 1100})
    page.locator('#score-cue').select_option('0')
    page.locator('.all-takes-scroll').evaluate('(el)=>el.scrollLeft=0')
    (ROOT / 'checks').mkdir(exist_ok=True)
    page.screenshot(path=str(ROOT / 'checks/all-takes.png'), full_page=True)
    assert not errors, errors
    browser.close()
print('PASS: all-takes overview in 04A/B, fixed controls, notes, instruments and score navigation')
