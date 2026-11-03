"""Exercise the complete review and real section/note/planner/order/display actions."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'prototype'))
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1100});page.clock.install();errors=[];page.set_default_timeout(10000)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'experiments.html').as_uri())
 expect(page.locator('.v3-review-topline')).to_contain_text('1 van 8')
 print('Loaded full review',flush=True)
 assert not errors,errors
 def step(id,variant='A'):
  page.evaluate('(id)=>reviewGo(id)',id)
  page.locator(f'[data-review-variant="{variant}"]').click()
 def startstop():
  page.locator('.v3-review-caption').click();page.keyboard.press('Space')
 # Confirmed transport: first press is session only, even with preview variants.
 step('workspace','B')
 page.locator('.calm-notes [data-draft]').fill('Retain this draft')
 page.locator('.v3-review-caption').click();page.keyboard.press('Space')
 assert page.evaluate('state().sessionStarted&&!running(state())')
 page.locator('[data-review-variant="A"]').click()
 expect(page.locator('.calm-notes [data-draft]')).to_have_value('Retain this draft')
 step('sections')
 page.locator('[data-review-section-range]').fill('4–10');page.locator('[data-review-section-range]').press('Enter')
 before=page.evaluate('nextEntryNumber(state(),state().cue)')
 startstop();live=page.evaluate('running(state()).id')
 assert page.evaluate('running(state()).barRange')=={'from':4,'to':10}
 assert page.evaluate('running(state()).num')==before
 assert page.evaluate('running(state()).kind')=='take'
 # Switching a section A/B preview cannot stop or change the live range.
 page.locator('[data-review-variant="B"]').click();assert page.evaluate('running(state()).id')==live
 expect(page.locator('[data-review-section-from]')).to_be_disabled()
 startstop()
 page.locator('[data-review-section-from]').fill('12');page.locator('[data-review-section-to]').fill('15');page.locator('[data-review-section-apply]').click()
 startstop();assert page.evaluate('running(state()).num')==before+1
 assert page.evaluate('running(state()).barRange')=={'from':12,'to':15}
 startstop()
 expect(page.locator('[aria-label="Takes grouped by bar range"]')).to_contain_text('Bars 4–10')
 print('PASS sections',flush=True)
 # Note shortcuts work while typing, and preserve the user's text and timestamp.
 step('notes')
 field=page.locator('.calm-notes [data-draft]');field.fill('Cello softer');stamp=page.evaluate('takeById(state(),state().selected).draft.clockAt')
 field.press('Meta+j');expect(page.locator('.v3-note-range-popover')).to_be_visible()
 page.locator('[data-review-note-value]').fill('13–20');page.locator('[data-review-note-value]').press('Enter')
 expect(field).to_have_value('Cello softer');field.press('Enter')
 note=page.evaluate('takeById(state(),state().selected).notes.at(-1)')
 assert (note['text'],note['measure'],note['measureEnd'],note['clockAt'])==('Cello softer',13,20,stamp),note
 expect(page.locator('.calm-notes .note-list')).to_contain_text('13–20')
 page.locator('[data-review-variant="B"]').click()
 page.locator('.calm-notes [data-draft]').fill('Violin brighter')
 page.locator('[data-review-note-from]').fill('21');page.locator('[data-review-note-to]').fill('23');page.locator('.v3-inline-note-range [data-review-note-apply]').click()
 page.locator('.calm-notes [data-draft]').press('Enter')
 assert page.evaluate('takeById(state(),state().selected).notes.at(-1).measureEnd')==23
 exported=page.evaluate('sessionTakeLog().takes.find(t=>t.takeId===state().selected)')
 assert exported['barRange']=={'from':12,'to':15}
 assert exported['notes'][-1]['barEnd']==23
 print('PASS note ranges',flush=True)
 # Planning fits the exact available seconds and excludes completed cues.
 step('planning')
 page.evaluate('cueSettings(state(),25).complete=true;renderDemo()')
 result=page.evaluate('reviewPlanPreview(state())')
 assert not result.get('error'),result
 assert result['total']+result['reserved']==result['available']
 assert not any(r['j']==25 for r in result['rows'])
 old=page.evaluate('cueSettings(state(),25).planned')
 page.locator('[data-review-plan-apply]').click()
 assert page.evaluate('cueSettings(state(),25).planned')==old
 assert abs(page.evaluate('scoreWorkflowTiming(state()).delta'))<=1
 page.evaluate('proposalSessionBreak(state())');page.clock.fast_forward(120000)
 assert abs(page.evaluate('scoreWorkflowTiming(state()).delta'))<=1,'Reserved break should not become a new delay'
 page.evaluate('proposalSessionBreak(state())')
 page.locator('[data-review-variant="B"]').click()
 page.locator('[data-review-plan-lock="0"]').check()
 result=page.evaluate('reviewPlanPreview(state())')
 assert not result.get('error'),result
 locked=next(r for r in result['rows'] if r['j']==0)
 assert locked['locked']
 # Impossible budgets produce an explicit blocked preview instead of overallocating.
 page.evaluate('reviewPlannerState(state()).bufferMinutes=1500;renderDemo()')
 expect(page.locator('[data-review-plan-apply]')).to_be_disabled()
 page.evaluate('reviewPlannerState(state()).bufferMinutes=5;renderDemo()')
 print('PASS planning',flush=True)
 # Reordering changes only reference order, with stable source arrays and take IDs.
 step('order','B')
 identity=page.evaluate('({cues:cues.map(c=>c[0]),takes:allTakes(state()).map(t=>({id:t.id,notes:t.notes}))})')
 page.locator('[data-review-move-cue="0"][data-direction="1"]').click()
 assert page.evaluate('reviewRecordingOrder(state()).slice(0,2)')==[1,0]
 assert page.evaluate('({cues:cues.map(c=>c[0]),takes:allTakes(state()).map(t=>({id:t.id,notes:t.notes}))})')==identity
 page.locator('[data-review-cue-sort]').select_option('cue')
 expect(page.locator('[data-review-move-cue="0"]').first).to_be_disabled()
 page.locator('[data-review-cue-sort]').select_option('recording')
 page.locator('[data-review-variant="A"]').click()
 page.locator('[data-review-drag-cue="0"]').drag_to(page.locator('[data-review-cue-key="1"]'))
 assert page.evaluate('reviewRecordingOrder(state()).slice(0,2)')==[0,1],page.evaluate('reviewRecordingOrder(state())')
 print('PASS cue order',flush=True)
 # Clock preferences do not touch the saved note clocks.
 step('clocks','B');saved=page.evaluate('allTakes(state()).flatMap(t=>t.notes).map(n=>n.clockAt)')
 page.locator('[data-review-clock-zone="secondary"]').select_option('America/Los_Angeles')
 expect(page.locator('[data-review-world-clock]')).to_be_visible()
 page.locator('[data-review-clock-toggle="remaining"]').uncheck()
 assert page.locator('#main-panel [data-proposal-remaining]').locator('..').evaluate('(el)=>el.hidden')
 assert page.evaluate('allTakes(state()).flatMap(t=>t.notes).map(n=>n.clockAt)')==saved
 print('PASS clocks',flush=True)
 # Both score variants render the same score and retain global scale.
 step('score');expect(page.locator('.v3-reference-score')).to_be_visible()
 zoom=page.evaluate('state().zoom');page.locator('[data-review-reference-zoom="in"]').click();assert page.evaluate('state().zoom')>zoom
 zoom=page.evaluate('state().zoom');page.locator('[data-review-variant="B"]').click()
 expect(page.locator('.score-canvas')).to_be_visible();assert page.evaluate('state().zoom')==zoom
 page.locator('[data-review-variant="A"]').click();assert page.evaluate('state().zoom')==zoom
 print('PASS score',flush=True)
 # Go through every variant at mobile and desktop sizes, including a complete summary.
 for width,height in [(1512,1100),(1366,768),(390,844)]:
  page.set_viewport_size({'width':width,'height':height})
  for id in page.evaluate('reviewSteps.map(s=>s.id)'):
   for v in ['A','B']:
    step(id,v);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,id,v)
    expect(page.locator('[data-review-next]')).to_be_in_viewport()
    page.screenshot(path=str(ROOT/f'check-round-{width}-{id}-{v}.png'))
  page.locator('[data-review-next]').click();expect(page.locator('.v3-review-summary')).to_be_visible()
  assert page.locator('.v3-summary-rows article').count()==8
  with page.expect_download() as download:page.locator('[data-review-download]').click()
  data=json.loads(Path(download.value.path()).read_text());assert len(data['steps'])==8 and data['confirmed']['proTools']=='deferred'
 # A live take remains stoppable even from the final choice overview.
 page.set_viewport_size({'width':1512,'height':1100});step('workspace','B');startstop()
 assert page.evaluate('!!running(state())')
 page.locator('[data-review-overview]').click();expect(page.locator('.v3-summary-live .record.stop')).to_be_visible()
 page.locator('.v3-summary-live .record.stop').click();assert page.evaluate('!running(state())')
 page.reload();expect(page.locator('.v3-review-topline')).to_contain_text('1 van 8')
 assert page.evaluate('Object.keys(reviewChoices).length')==8
 assert not errors,errors
 browser.close()
print('PASS eight A/B prototypes, first-Space session start, section numbering/live ownership, note-range metadata, exact/locked/impossible planning, stable cue IDs/order, clock preferences, global score zoom and summary download at desktop/mobile sizes')
