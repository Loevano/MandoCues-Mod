"""Build one offline MandoCues proposal, a guided tour and matching handoff docs."""
from pathlib import Path
import base64
import json
import shutil
from score_fixture import make_fixture
from production_score import load_production_score

ROOT=Path(__file__).resolve().parent
SRC,DIST=ROOT/'src',ROOT/'dist'
DIST.mkdir(exist_ok=True)
def read(name):return (SRC/name).read_text(encoding='utf-8')
def write(name,value):(DIST/name).write_text(value,encoding='utf-8')
def embedded(value):return json.dumps(value,ensure_ascii=False).replace('</','<\\/')

ideas=json.loads(read('content.json'))
discussion=json.loads(read('discussion.json'))
tour=json.loads(read('proposal-tour.json'))
steps=tour['steps']
assert len({s['id'] for s in steps})==len(steps)
assert all(s['view'] in ('recording','cutlist') for s in steps)
parts=[part for step in steps for part in step['parts']]
assert len({part['id'] for part in parts})==len(parts)
for part in parts:
    assert part.get('prompt') or any(d['id']==part.get('discussion') for d in discussion),part['id']
def tour_prompt(step):
    return '\n\n'.join(next(d['text'] for d in discussion if d['id']==part['discussion']) if part.get('discussion') else part['prompt'] for part in step['parts'])
assets=make_fixture();assets['production']=load_production_score()
feedback=read('feedback.md')
shell=read('shell.html')
values={
    'CSS':read('style.css'),'CONTENT':embedded(ideas),'DISCUSSION':embedded(discussion),
    'FEEDBACK':embedded(feedback),'ASSETS':embedded(assets),'EXTRA_INPUT':embedded(read('extra-input.md')),
    'TOUR_STEPS':embedded(tour),
}
for marker,name in [('EXTRA_JS','extra.js'),('INSPECTION_JS','inspection.js'),
    ('PRODUCTION_SCORE_JS','production-score.js'),('SCORE_INTERACTIONS_JS','score-interactions.js'),
    ('SCORE_WORKFLOW_JS','score-workflow.js'),('CONTROLS_CALM_JS','controls-calm.js'),
    ('SCORE_COMPARE_JS','score-compare.js'),('JS','app.js'),('APP_SHELL_JS','proposal-shell.js'),('UNIFIED_JS','unified-app.js'),('TOUR_JS','proposal-tour.js')]:
    values[marker]=read(name)
for marker,value in values.items():shell=shell.replace('/*'+marker+'*/',value)
write('index.html',shell)
shutil.copyfile(SRC/'root.html',ROOT.parent/'index.html')
# Old links still open the current workspace; obsolete variant prompts stay in Git history.
for idea in ideas:
    target='index.html#'+('cutlist' if idea['id']=='partituur' else 'recording')
    entry=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MandoCues proposal</title><script>location.replace({json.dumps(target)});</script><a href="{target}">Open MandoCues</a></html>'
    write(f"{idea['number']}-{idea['id']}.html",entry)
    (DIST/f"{idea['number']}-{idea['id']}.md").unlink(missing_ok=True)
    for variant in idea['variants']:(DIST/f"{idea['number']}-prompt-{variant}.txt").unlink(missing_ok=True)
small=sorted((d for d in discussion if d.get('small')),key=lambda d:d['order'])
questions=[d for d in discussion if not d.get('small')]
questions_doc='## Vragen\n\n'+'\n'.join('- '+d['title']+(' '+d['text'] if d['text'] else '') for d in questions)+'\n'
small_doc='## Kleine suggesties\n\n'+'\n'.join('- '+d['bullet'] for d in small)+'\n\n'
write('Kleine-suggesties-en-vragen.md','# Suggesties en open vragen\n\n'+small_doc+questions_doc)
doc='# MandoCues · voorstel van Floris\n\nEén werkruimte met Recording en Comp tool. Bij openen kies je Rondleiding starten of Zelf bekijken. De rondleiding toont één suggestie tegelijk; een checkbox bepaalt of die tekst meegaat naar Claude. De app werkt los van deze keuze.\n\nAlle daadwerkelijke GUI-tekst is Engels. Uitleg en vragen blijven Nederlands. Het zijn vrijblijvende ideeën; jouw programma en ontwerpkeuzes gaan voor.\n\n'
doc+=questions_doc+'\n## De rondleiding\n\nDe onderstaande tekstonderdelen worden alleen samengevoegd als ze zijn aangevinkt. Er wordt geen nieuwe prompt gegenereerd.\n\n'
for index,step in enumerate(steps,1):
    prompt=tour_prompt(step)
    detail=step.get('details')
    extra=f"**{detail['title']}**\n\n{detail['text']}\n\n" if detail else ''
    doc+=f"### {index}. {step['title']}\n\n{step['text']}\n\n{extra}**Promptonderdeel:**\n\n{prompt}\n\n"
doc+='## Gedeelde promptinleiding\n\n'+tour['promptIntro']+'\n## Gedeelde afsluiting\n\n'+tour['promptClosing'].strip()+'\n'
write('Suggesties-van-Floris.md',doc)
for output,source in [('Alle-notes-van-Floris.md','feedback.md'),('Aanvullende-input.md','extra-input.md'),
    ('Bestaand-scherm-context.md','rendered-context.md'),('Partituren-overzicht.md','scores-context.md'),
    ('Score-ervaring-voor-Claude.md','score-context.md'),('Huidig-voorstel.md','current-proposal.md'),
    ('Pro-Tools-takekoppeling.md','protools-sync.md')]:write(output,read(source))
(DIST/'Wijzigingen-18-oktober.md').unlink(missing_ok=True)
shutil.copyfile(SRC/'score-assets/score-catalog.json',DIST/'Score-catalogus.json')
shutil.copyfile(SRC/'score-assets/Afterparty-1M02-Arrival-excerpt.pdf',DIST/'Afterparty-1M02-Arrival-excerpt.pdf')
(DIST/'Floris-voorbeeldpartituur.pdf').write_bytes(base64.b64decode(assets['pdf']))
write('LEESMIJ.txt','''MandoCues · voorstel van Floris

Open index.html in je browser. Dit bestand werkt zelfstandig en offline.
Bij openen kies je Rondleiding starten of Zelf bekijken.

Eén werkruimte: Recording en Cut list delen cues, takes, sterren en notes.
Recording gebruikt bediening bovenaan met een compacte balk bij scrollen.
Cut list bevat de bestaande scorefuncties en het All takes-overzicht.

De rondleiding highlight per stap één suggestie met een korte uitleg.
Voeg toe aan de prompt voor Claude staat standaard aangevinkt.
Vink uit wat je niet wilt overnemen; bestaande opgeslagen keuzes blijven behouden.
Volgende gaat ook verder zonder die suggestie te kiezen.
Aan het einde, of via Claude-prompt bovenaan, kopieer of download je je selectie.
De bestaande tekstonderdelen worden samengevoegd, niet opnieuw gegenereerd.
Je kunt Rondleiding later opnieuw starten; je selectie blijft lokaal bewaard.
Vragen staan apart en worden niet automatisch implementatieopdrachten.

De interface is Engels; de rondleiding en vragen zijn Nederlands.
Alles is vrijblijvend. Jouw programma, workflow en ontwerpkeuzes gaan voor.

Command+Enter start of stopt een take op Mac. Gewoon Enter plaatst een note.
Spatie blijft tekst. Er wordt geen audio opgenomen en niets geüpload.
De demo heeft geen echte DAW-/filmverbinding of live maat-/partituurherkenning.
Een PDF alleen bepaalt niet welke maat er wordt gespeeld.
Nieuwe takes, notes en eigen PDF's verdwijnen bij herladen.
Alleen de suggestiekeuze wordt waar mogelijk in deze browser bewaard;
die wordt niet met anderen gedeeld.

Suggesties-van-Floris.md bevat de teksten en exacte promptonderdelen.
Huidig-voorstel.md beschrijft de actuele keuzes en het herstelpunt.
Alle-notes-van-Floris.md is geschiedenis; latere correcties gaan voor eerdere.
De oude vijf voorbeelden zijn bewaard op Git-tag before-unified-ui-20261018.
''')
print(f'Built one offline workspace, two shared views and {len(steps)} guided suggestions.')
