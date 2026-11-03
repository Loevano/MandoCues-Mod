"""Exercise the presentation edits without changing the preserved v2 app."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'prototype'))
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright,expect

with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1000});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.clock.install();page.goto((ROOT/'index.html').as_uri());expect(page.locator('#proposal-welcome')).to_have_count(0)
 editor=page.locator('.calm-notes [data-draft]')
 # First letter freezes the original instant, even if all text is removed.
 editor.fill('Cello');anchor=page.evaluate('takeById(state(),state().selected).draft.writtenAt')
 assert anchor is not None
 page.clock.run_for(5000);editor.fill('');page.clock.run_for(5000);editor.fill('Calmer cello')
 assert page.evaluate('takeById(state(),state().selected).draft.writtenAt')==anchor
 now=page.locator('.calm-notes [data-reset-note-time="draft"]');now.click()
 assert page.evaluate('takeById(state(),state().selected).draft.clockAt')>anchor
 page.locator('.calm-notes [data-restore-note-time="draft"]').click()
 assert page.evaluate('takeById(state(),state().selected).draft.clockAt')==anchor
 # Save carries the original anchor; current-time and restore remain independent.
 editor.press('Enter');note=page.evaluate('takeById(state(),state().selected).notes.at(-1)')
 assert note['writtenAt']==anchor
 page.locator(f'.calm-notes [data-reset-note-time="{note["id"]}"]').click()
 page.locator(f'.calm-notes [data-restore-note-time="{note["id"]}"]').click()
 assert page.evaluate('takeById(state(),state().selected).notes.at(-1).clockAt')==anchor
 assert page.evaluate('takeById(state(),state().selected).draft.clockAt') is None
 # N focuses the existing draft without replacing it or becoming typed content.
 page.locator('.proposal-workspace-title').click();page.keyboard.press('n')
 expect(editor).to_be_focused();expect(editor).to_have_value('')
 n_anchor=page.evaluate('takeById(state(),state().selected).draft.writtenAt')
 page.clock.run_for(5000);editor.fill('Keep this draft')
 page.locator('.proposal-workspace-title').click();page.keyboard.press('n')
 expect(editor).to_have_value('Keep this draft')
 assert page.evaluate('takeById(state(),state().selected).draft.writtenAt')==n_anchor
 editor.press('n');expect(editor).to_have_value('Keep this draftn')
 # Choosing another Best does not clear the first; selected/live takes stay unchanged.
 selected=page.evaluate('state().selected')
 best=page.locator('.cue-group.current [data-take-best]')
 ids=best.evaluate_all('(buttons)=>buttons.map(b=>b.dataset.takeBest)')
 assert len(ids)>=2
 for take in ids[:2]:
  button=page.locator(f'.cue-group.current [data-take-best="{take}"]')
  if button.get_attribute('aria-pressed')!='true':button.click()
 for take in ids[:2]:expect(page.locator(f'.cue-group.current [data-take-best="{take}"]')).to_have_attribute('aria-pressed','true')
 page.locator(f'.cue-group.current [data-take-best="{ids[1]}"]').click()
 expect(page.locator(f'.cue-group.current [data-take-best="{ids[0]}"]')).to_have_attribute('aria-pressed','true')
 assert page.evaluate('state().selected')==selected
 # The walkthrough follows real session order and keeps its correct target.
 page.locator('[data-proposal-action="tour"]').click()
 ids=page.evaluate('proposalTourSteps.map(s=>s.id)')
 assert ids[:6]==['sessieplan','cue-aanklikken','sterren','noteplek','maat-aanpassen','planning']
 expect(page.locator('.proposal-tour-highlight')).to_be_visible()
 # Drag by the header, then re-render: automatic positioning must not undo the move.
 card=page.locator('.proposal-tour-card');header=card.locator('header');r=header.bounding_box();before=card.bounding_box()
 page.mouse.move(r['x']+40,r['y']+12);page.mouse.down();page.mouse.move(110,160,steps=6);page.mouse.up()
 after=card.bounding_box();assert abs(after['x']-(110-(r['x']+40-before['x'])))<3,after
 page.evaluate('renderDemo(); positionProposalTour()')
 assert abs(card.bounding_box()['x']-after['x'])<1
 for index,id in enumerate(ids):
  page.evaluate('(index)=>openTourStep(index)',index)
  expect(page.locator('#proposal-tour-title')).to_have_text(page.evaluate('proposalTourSteps[proposalTourIndex].title'))
  target=page.evaluate('tourTarget?.className||""');assert target,(id,target)
  checkbox=page.locator('.proposal-tour-card [data-tour-choice]')
  if id!='comp-tool-overgang':expect(checkbox).to_be_checked()
  if id=='cue-aanklikken':
   expect(page.locator('.proposal-tour-highlight')).not_to_be_visible()
   # Take selection remains interactive while the tour is open.
   page.locator('.cue-group.current [data-select-take]').first.click()
   assert page.evaluate('state().selected')==page.locator('.cue-group.current [data-select-take]').first.get_attribute('data-select-take')
  if id=='noteplek':expect(page.locator('.sticky-slot')).to_have_class('sticky-slot is-stuck')
  if id=='maat-aanpassen':
   assert 'composer-footer' in target,(id,target)
   expect(page.locator('.tour-inline-help')).to_contain_text('Voor later')
   assert 'File → Export' not in page.locator('.tour-inline-help').inner_text()
  if id=='view-toggle':assert 'score-paper' in target
  if id=='planning':expect(page.locator('.tour-schedule-examples .main-plan-card')).to_have_count(3)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),id
 page.locator('[data-tour-action="close"]').click()
 # Existing explicit opt-outs survive the new ordering and a page reload.
 page.evaluate("openTourStep(1)")
 page.locator('.proposal-tour-card [data-tour-choice]').uncheck()
 page.reload();expect(page.locator('#proposal-welcome')).to_have_count(0)
 page.evaluate('openTourStep(1)');expect(page.locator('.proposal-tour-card [data-tour-choice]')).not_to_be_checked()
 page.evaluate('openTourStep(0)');expect(page.locator('.proposal-tour-card [data-tour-choice]')).to_be_checked()
 # Review cards and their controls remain within the viewport on smaller screens.
 for width in [900,390]:
  page.set_viewport_size({'width':width,'height':844})
  for index in range(len(ids)):
   page.evaluate('(index)=>openTourStep(index)',index)
   page.evaluate('positionProposalTour()')
   rect=page.locator('.proposal-tour-card').bounding_box()
   assert rect['x']>=0 and rect['x']+rect['width']<=width+1,(width,ids[index],rect)
   assert rect['y']>=0 and rect['y']+rect['height']<=845,(width,ids[index],rect)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,ids[index])
 assert not errors,errors
 browser.close()
print('PASS note anchors/N/NOW/restore, independent Best takes, tour order/targets/dragging/sticky bar and opt-out persistence')
