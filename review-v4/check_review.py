"""Verify concrete A/B choices, workload editor, review persistence and restoration."""
from pathlib import Path
import sys,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'prototype'))
from browser_support import launch_chromium
from playwright.sync_api import sync_playwright,expect
manifest=json.loads((ROOT/'restore.json').read_text())
assert hashlib.sha256((ROOT/manifest['file']).read_bytes()).hexdigest()==manifest['sha256']
before=(ROOT/'index.html').read_bytes();subprocess.run([sys.executable,str(ROOT/'build.py')],check=True);assert (ROOT/'index.html').read_bytes()==before
with sync_playwright() as p:
 browser=launch_chromium(p);page=browser.new_page(viewport={'width':1512,'height':1000});page.set_default_timeout(10000);errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.goto((ROOT/'index.html').as_uri())
 expect(page.locator('.proposal-tour-card,dialog[open]')).to_have_count(0)
 page.locator('[data-proposal-action=tour]').click()
 expect(page.locator('.proposal-tour-card header')).to_contain_text('1 van 6')
 page.locator('[data-v4-review-choice=B]').click();expect(page.locator('.v4-timing-details')).to_have_attribute('open','')
 page.locator('[data-v4-review-choice=A]').click();expect(page.locator('.v4-timing-details')).not_to_have_attribute('open','')
 # The card is still movable and keeps its position on a data render.
 header=page.locator('.proposal-tour-card header');r=header.bounding_box();page.mouse.move(r['x']+30,r['y']+10);page.mouse.down();page.mouse.move(150,130,steps=6);page.mouse.up()
 position=page.locator('.proposal-tour-card').bounding_box();page.evaluate('renderDemo();positionProposalTour()')
 assert abs(page.locator('.proposal-tour-card').bounding_box()['x']-position['x'])<1
 page.locator('[data-tour-action=next]').click();page.locator('[data-v4-review-choice=B]').click();page.locator('[data-v4-try-workload]').click()
 form=page.locator('#v4-cue-timing');expect(form.locator('.v4-music-part')).to_have_count(1)
 part=form.locator('.v4-music-part').first;part.locator('[data-part-from]').fill('2');part.locator('[data-part-to]').fill('8');part.locator('[data-part-duration]').fill('00:30')
 form.locator('[data-v4-music-add]').click();part=form.locator('.v4-music-part').nth(1);part.locator('[data-part-from]').fill('8');part.locator('[data-part-to]').fill('19');part.locator('[data-part-duration]').fill('00:45')
 page.locator('[form=v4-cue-timing]').click();expect(form.locator('[data-v4-music-error]')).to_contain_text('non-overlapping')
 part.locator('[data-part-from]').fill('12');page.locator('[form=v4-cue-timing]').click()
 assert page.evaluate('v4Row(state(),state().cue).musicSeconds')==75
 assert len(page.evaluate('v4Row(state(),state().cue).musicParts'))==2
 page.locator('[data-tour-action=next]').click();page.locator('[data-v4-review-choice=B]').click()
 expect(page.locator('[data-v4-range-preset]')).to_have_count(2)
 page.locator('[data-tour-action=next]').click();page.locator('[data-v4-learning-example]').click()
 first=page.locator('#v4-learning-example strong').inner_text();original=page.evaluate('state().takes.flat().length')
 page.locator('[data-v4-review-choice=B]').click();second=page.locator('#v4-learning-example strong').inner_text();assert first!=second
 assert page.evaluate('state().takes.flat().length')==original
 page.locator('[data-tour-action=next]').click();page.locator('[data-v4-review-choice=B]').click()
 assert page.evaluate('v4State(state()).settings.allocation')=='fixed'
 page.locator('[data-v4-allocation-example]').click();expect(page.locator('#v4-allocation-example')).to_contain_text('10:00')
 page.locator('[data-v4-review-choice=A]').click();expect(page.locator('#v4-allocation-example')).to_contain_text('08:20')
 page.locator('[data-v4-review-choice=B]').click();expect(page.locator('#v4-allocation-example')).to_contain_text('30 minuten')
 page.locator('[data-tour-action=next]').click();expect(page.locator('.score-canvas')).to_be_visible()
 expect(page.locator('[data-proposal-view=cutlist]')).to_have_text('Score')
 assert page.evaluate('tourTarget.matches(".score-paper")')
 page.locator('[data-tour-action=next]').click();expect(page.locator('#v4-review-summary')).to_be_visible()
 expect(page.locator('#v4-review-summary li')).to_have_count(5)
 with page.expect_download() as pending:page.locator('[data-v4-review-download]').click()
 downloaded=json.loads(Path(pending.value.path()).read_text());assert downloaded['version']==4
 assert downloaded['choices']['workload']=='B' and downloaded['choices']['allocation']=='B'
 page.reload();expect(page.locator('.proposal-tour-card')).to_have_count(0)
 assert page.evaluate('v4State(state()).settings.workload')=='ranges'
 assert page.evaluate('v4State(state()).settings.allocation')=='fixed'
 # Review controls stay reachable at all supported widths, including the example.
 for width in [1512,900,390]:
  page.set_viewport_size({'width':width,'height':844})
  for i in range(6):
   page.evaluate('(i)=>openTourStep(i)',i);page.evaluate('positionProposalTour()')
   box=page.locator('.proposal-tour-card').bounding_box()
   assert box['x']>=0 and box['x']+box['width']<=width+1,(width,i,box)
   assert box['y']>=0 and box['y']+box['height']<=845,(width,i,box)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,i)
 assert not errors,errors
 browser.close()
print('PASS six-step interactive A/B review, section duration/validation, example isolation, export/persistence, card dragging and preserved v3')
