from browser_support import launch_chromium
import re
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent
URL=(ROOT/'dist/index.html').as_uri();errors=[];inventory=[]
with sync_playwright() as p:
 b=launch_chromium(p)
 page=b.new_page(viewport={'width':1512,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
 for route,variants in [('cue-take',['A']),('bediening',['A','B']),('notities',['A','B']),('partituur',['A','B']),('planning',['A'])]:
  page.goto(URL+'#'+route)
  for variant in variants:
   if len(variants)>1:page.locator(f'[data-variant="{variant}"]').click()
   inventory.append(route+' '+variant+'\n'+page.locator('#demo').text_content())
   attrs=page.locator('#demo').evaluate('el=>Array.from(el.querySelectorAll("[aria-label],[placeholder],[title]")).flatMap(e=>[e.getAttribute("aria-label"),e.getAttribute("placeholder"),e.getAttribute("title")]).filter(Boolean)')
   inventory.extend(attrs)
   texts=page.locator('#demo').evaluate('el=>{const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),out=[];while(w.nextNode()){const t=w.currentNode.textContent.trim();if(t)out.push(t);}return out;}')
   names=page.evaluate('cues.map(c=>c[1])')
   forbidden=re.compile(r'\b(partituur|notities|notitie|maat|maten|opname|geen|nieuwe|tijdcode|gepland|kies|volg|voorbereiding|sessieduur|snelle|bewerk|verwijder|toon|sterren|ster|bij|voor|pagina’s)\b',re.I)
   for text in [*texts,*attrs]:
    for name in names:text=text.replace(name,'[cue title]')
    assert not forbidden.search(text),(route,variant,text)
 page.goto(URL+'#partituur');page.locator('[data-select-take="c0-t1"]').click()
 page.locator('.cutlist-sidebar').scroll_into_view_if_needed()
 page.screenshot(path=str(ROOT/'checks/28-english-score-notes.png'))
 cell=page.locator('[data-score-page="1"] [data-score-measure="2"][data-score-instrument="vln2"]')
 cell.dblclick();expect(page.locator('#score-comment-text')).to_have_attribute('aria-label','Note');inventory.append(page.locator('#score-comment-dialog').text_content())
 page.locator('#score-comment-text').fill('Cello zachter — eigen tekst');page.locator('#score-comment-text').press('Enter')
 expect(page.locator('.score-text-annotation').filter(has_text='Cello zachter — eigen tekst')).to_have_count(1)
 (ROOT/'checks/english-ui.txt').write_text('\n'.join(inventory))
 page.goto(URL+'#partituur');page.locator('[data-select-take="c0-t1"]').click()
 note=page.locator('article[data-note-id="seed-1"]');bar=note.locator('.measure-picker>summary').bounding_box();book=note.locator('.score-page-reference').bounding_box()
 assert book['y']>bar['y'] and abs(book['x']-bar['x'])<1
 assert book['y']-(bar['y']+bar['height'])<5
 dot=page.locator('.score-notes-take .take-color-dot');expect(dot).to_have_count(1)
 assert dot.evaluate('el=>getComputedStyle(el).backgroundColor')==page.locator('[data-select-take="c0-t1"] .take-color-dot').evaluate('el=>getComputedStyle(el).backgroundColor')
 assert note.bounding_box()['height']<100,note.bounding_box()
 expect(page.locator('.cutlist-notes-list>summary')).to_contain_text('Notes for Take 1')
 expect(page.locator('.score-page-reference').first).to_have_text('Book p. 8')
 for width in [390,1512]:
  page.set_viewport_size({'width':width,'height':1100});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 for route in ['cue-take','bediening','notities','planning']:
  page.goto(URL+'#'+route);page.locator('[data-score-toggle]').click()
  expect(page.locator('#main-score-pane header small')).to_contain_text('bars')
  page.locator('[data-score-toggle]').click()
 page.goto(URL+'#partituur')
 for idea in page.evaluate('ideas.map(i=>({id:i.id,number:i.number,variants:Object.keys(i.variants)}))'):
  for v in idea['variants']:
   text=page.evaluate('([id,v])=>promptFor(ideas.find(i=>i.id===id),v)',[idea['id'],v])
   assert text==(ROOT/f"dist/{idea['number']}-prompt-{v}.txt").read_text()
   assert 'GUI moet Engels' in text
 page.keyboard.down('Meta');page.keyboard.down('Enter')
 assert page.evaluate('!!running(state())')
 live=page.evaluate('running(state()).id')
 page.keyboard.down('Enter');assert page.evaluate('running(state()).id')==live
 page.keyboard.up('Enter');page.keyboard.up('Meta')
 page.keyboard.press('Meta+Enter');assert page.evaluate('!running(state())')
 assert page.evaluate('state().takes[0].length')==3
 page.locator('.cutlist-source>summary').click();page.locator('#score-source').select_option('example')
 expect(page.locator('.score-paper').first).to_contain_text('String quartet - schematic demo score')
 assert not errors,errors
 b.close()
(ROOT/'checks/english-ui.txt').write_text('\n'.join(inventory))
print('PASS: all routes rendered; compact coloured take heading, book page below bar, responsive layout and untouched user-entered text. UI inventory: checks/english-ui.txt')
