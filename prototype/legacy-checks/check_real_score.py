from browser_support import launch_chromium, check_original_score_books
"""Validate real cue sources, document isolation and the unmodified score book."""
from pathlib import Path
import json,hashlib
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent
errors=[]
with sync_playwright() as p:
 b=launch_chromium(p)
 page=b.new_page(viewport={'width':1512,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'dist/index.html').as_uri()+'#partituur')
 def open_source():
  if not page.locator('.cutlist-source').evaluate('el=>el.open'):page.locator('.cutlist-source summary').click()
 def source(value):
  open_source();page.locator('#score-source').select_option(value)
 catalog=json.loads((ROOT/'src/score-assets/score-catalog.json').read_text())['books'][0]
 ranges={c['cue']:c for c in catalog['cuePages']}
 for index,code in enumerate(page.evaluate('cues.map(c=>c[0])')):
  page.locator('#score-cue').select_option(str(index));canonical='1M09AB' if code in ['1M09A','1M09B'] else code
  expected=ranges[canonical]
  expect(page.locator('.score-paper')).to_have_count(expected['endPage']-expected['startPage']+1)
  assert page.locator('.production-score-image').first.get_attribute('alt')==f"{canonical}, book page {expected['startPage']}"
 page.locator('#score-cue').select_option('0');page.locator('[data-score-new-take]').click()
 page.locator('.score-paper[data-score-page="2"] [data-score-measure="18"][data-score-instrument="vln1"]').dblclick()
 page.locator('#score-comment-text').fill('Echte bron');page.locator('#score-comment-text').press('Enter')
 source('example')
 page.locator('.score-paper[data-score-page="1"] [data-score-measure="18"][data-score-instrument="vla"]').dblclick()
 page.locator('#score-comment-text').fill('Schematische bron');page.locator('#score-comment-text').press('Enter')
 expect(page.locator('.score-note-text').filter(has_text='Echte bron')).to_have_count(0)
 # Source changes also scope the undo history to the right document.
 source('production')
 expect(page.locator('.score-note-text').filter(has_text='Echte bron')).to_have_count(1)
 expect(page.locator('.score-note-text').filter(has_text='Schematische bron')).to_have_count(0)
 page.locator('[data-score-undo]').click();expect(page.locator('.score-note-text').filter(has_text='Echte bron')).to_have_count(0)
 source('example')
 expect(page.locator('.score-note-text').filter(has_text='Schematische bron')).to_have_count(1)
 source('production')
 open_source()
 with page.expect_download() as dl:page.locator('[data-action="download-production-score"]').click()
 file=ROOT/'checks/Arrival-fragment-download.pdf';dl.value.save_as(str(file))
 assert file.read_bytes()==(ROOT/'dist/Afterparty-1M02-Arrival-excerpt.pdf').read_bytes()
 page.locator('#pdf-file').set_input_files(str(ROOT/'dist/Floris-voorbeeldpartituur.pdf'))
 expect(page.locator('.pdf-native')).to_have_count(1)
 expect(page.locator('[data-score-cell]')).to_have_count(0)
 assert not errors,errors
 b.close()
check_original_score_books(ROOT)
print('PASS: 26 real cue mappings, independent source layers/undo, excerpt download, own-PDF guard and original score hashes')
