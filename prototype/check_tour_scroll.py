"""Tour navigation reveals targets even after the reviewer scrolls elsewhere."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_support import launch_chromium
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=launch_chromium(p)
    page=browser.new_page(viewport={'width':1512,'height':900})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'dist/index.html').as_uri())
    page.locator('[data-tour-action="welcome-skip"]').click()
    for width in [1512,390]:
        page.set_viewport_size({'width':width,'height':900})
        for id in ['duidelijke-labels','opnametoets','session-plan','cue-takes','sterren','notes-enter','snelle-notes','bereikbare-bediening','score-per-cue','score-zoom','score-overzicht']:
            page.evaluate('''()=>{
                const c=document.querySelector('#cue-scroll');if(c)c.scrollTop=c.scrollHeight;
                unifiedState.recordingScroll=100000;
                const score=document.querySelector('.score-canvas');if(score)score.scrollTop=score.scrollHeight;
            }''')
            exists=page.evaluate('(id)=>proposalTourSteps.some(s=>s.id===id)',id)
            assert exists,id
            page.evaluate('(id)=>openTourStep(proposalTourSteps.findIndex(s=>s.id===id))',id)
            page.wait_for_timeout(60)
            expect(page.locator('.proposal-tour-highlight')).to_be_visible()
            visible=page.evaluate('''()=>{
                const el=findTourTarget(proposalTourSteps[proposalTourIndex]),r=el.getBoundingClientRect();
                let top=Math.max(0,r.top),bottom=Math.min(innerHeight,r.bottom);
                for(let p=el.parentElement;p;p=p.parentElement){
                    if(/auto|scroll|hidden/.test(getComputedStyle(p).overflowY)){
                        const b=p.getBoundingClientRect();top=Math.max(top,b.top);bottom=Math.min(bottom,b.bottom);
                    }
                }
                return bottom-top;
            }''')
            assert visible>=min(20,page.evaluate('tourTarget.offsetHeight')),(width,id,visible)
    assert not errors,errors
    browser.close()
print('PASS: tutorial reveals recording controls, timeline, notes and score after arbitrary scrolling at desktop/mobile widths')
