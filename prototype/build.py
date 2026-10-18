"""Build offline, standalone demos and the complete colleague handoff."""
from pathlib import Path
import json
import base64
from score_fixture import make_fixture
from production_score import load_production_score
import shutil

ROOT = Path(__file__).resolve().parent
SRC, DIST = ROOT / 'src', ROOT / 'dist'
DIST.mkdir(exist_ok=True)
ideas = json.loads((SRC / 'content.json').read_text())
assets = make_fixture()
assets['production'] = load_production_score()
discussion = json.loads((SRC / 'discussion.json').read_text())
feedback = (SRC / 'feedback.md').read_text()
(DIST / 'Alle-notes-van-Floris.md').write_text(feedback)

def prompt_for(i, v):
    variant_label = f", variant {v}" if len(i['variants']) > 1 else ''
    detail_label = f"Variant {v}" if len(i['variants']) > 1 else 'Uitwerking'
    return f"Vrijblijvende suggestie van {i.get('origin','Floris')}: {i['short']}{variant_label}. Pas dit toe op mijn bestaande app. Mijn code, ontwerpkeuzes en oordeel blijven leidend. Bekijk eerst wat er al bestaat; behoud de bestaande visuele stijl en werk met bestaande componenten, state en opslag. Het prototype toont voorbeelddata, geen voorgeschreven architectuur. Alle tekst in de daadwerkelijke GUI moet Engels zijn, inclusief knoppen, labels, hints, tooltips, toegankelijkheidslabels en meldingen. Gebruik bijvoorbeeld Best, Add, Edit, Delete, Bar en Book p. Vragen, uitleg en voorstellen voor de collega mogen Nederlands blijven. Vertaal geen oorspronkelijke cue-/projectnamen of zelf ingevoerde notities.\n\nGewenst gedrag:\n{i['requirement']}\n\n{detail_label}:\n{i['variants'][v]}\n\nControle:\n{i['accept']}" + ('\n\nContext uit het bestaande scherm:\n'+i['inspection'] if i.get('inspection') else '') + ('\n\nErvaring uit Floris’ andere project:\n'+i['context'] if i.get('context') else '') + '\n\nMaak een kleine samenhangende wijziging, controleer de bestaande flows en vat kort samen wat veranderd is. Implementeer alleen dit voorstel. Neem andere suggesties alleen mee waar het hierboven expliciet nodig is voor de getoonde flow.'

shell = (SRC / 'shell.html').read_text()
for marker, value in [('CSS',(SRC/'style.css').read_text()),('CONTENT',json.dumps(ideas,ensure_ascii=False).replace('</','<\\/')),('FEEDBACK',json.dumps(feedback,ensure_ascii=False).replace('</','<\\/')),('DISCUSSION',json.dumps(discussion,ensure_ascii=False).replace('</','<\\/')),('ASSETS',json.dumps(assets,ensure_ascii=False).replace('</','<\\/')),('EXTRA_JS',(SRC/'extra.js').read_text()),('EXTRA_INPUT',json.dumps((SRC/'extra-input.md').read_text(),ensure_ascii=False).replace('</','<\\/')),('INSPECTION_JS',(SRC/'inspection.js').read_text()),('PRODUCTION_SCORE_JS',(SRC/'production-score.js').read_text()),('SCORE_INTERACTIONS_JS',(SRC/'score-interactions.js').read_text()),('SCORE_WORKFLOW_JS',(SRC/'score-workflow.js').read_text()),('CONTROLS_CALM_JS',(SRC/'controls-calm.js').read_text()),('SCORE_COMPARE_JS',(SRC/'score-compare.js').read_text()),('JS',(SRC/'app.js').read_text()),('UNIFIED_JS',(SRC/'unified-app.js').read_text()),('TOUR_STEPS',json.dumps(json.loads((SRC/'proposal-tour.json').read_text()),ensure_ascii=False).replace('</','<\\/')),('TOUR_JS',(SRC/'proposal-tour.js').read_text())]:
    shell = shell.replace(f'/*{marker}*/',value)
# Retire only the generated entrypoints and documents of the first version.
for name in ['03-opnamestatus.html','04-notities.html','03-opnamestatus.md','04-notities.md','MandoCues-overdracht-aan-collega.md','01-prompt-B.txt','06-take-afspraak.html','06-take-afspraak.md','07-kniplijst.html','07-kniplijst.md','07-prompt-A.txt','07-prompt-B.txt','04-prompt-B.txt','06-kniplijst.html','06-kniplijst.md','06-prompt-A.txt','06-prompt-B.txt','Jens-input.md']:
    (DIST/name).unlink(missing_ok=True)
(DIST/'index.html').write_text(shell)
shutil.copyfile(SRC/'root.html', ROOT.parent/'index.html')
(DIST/'Aanvullende-input.md').write_text((SRC/'extra-input.md').read_text())
(DIST/'Bestaand-scherm-context.md').write_text((SRC/'rendered-context.md').read_text())
(DIST/'Wijzigingen-18-oktober.md').write_text((SRC/'changes-20261018.md').read_text())
(DIST/'Partituren-overzicht.md').write_text((SRC/'scores-context.md').read_text())
shutil.copyfile(SRC/'score-assets/score-catalog.json',DIST/'Score-catalogus.json')
shutil.copyfile(SRC/'score-assets/Afterparty-1M02-Arrival-excerpt.pdf',DIST/'Afterparty-1M02-Arrival-excerpt.pdf')
intro = '''# Prototypes van Floris

Een paar kleine suggesties voor je opnameprogramma. Open index.html, probeer een voorbeeld en kies eventueel A of B. Bevalt iets? De knop ‘Kopieer prompt’ geeft je de volledige opdracht voor je eigen Claude. Neem alleen mee wat jij handig vindt. Jouw programma en ontwerpkeuzes gaan voor.

Filmmodus verbergt de uitleg voor een schermopname; Escape toont die weer. Alle voorbeelden werken lokaal. Er wordt geen audio opgenomen. Notities en zelfgekozen PDF’s blijven in deze geopende demo en verdwijnen bij herladen; er wordt niets geüpload.

'''
small = sorted((d for d in discussion if d.get('small')), key=lambda d: d['order'])
questions = [d for d in discussion if not d.get('small')]
small_doc = '## Kleine aanpassingen\n\n' + '\n'.join('- '+d['bullet'] for d in small) + '\n\n'
questions_doc = '## Vragen\n\n' + '\n'.join('- '+d['title']+(' '+d['text'] if d['text'] else '') for d in questions) + '\n\n' if questions else ''
doc = intro + small_doc + questions_doc + '## De prototypes\n\nHieronder zie je hoe de kleine voorstellen kunnen werken binnen een grotere indeling. Elk prototype onderzoekt één vraag.\n\n'
for i in ideas:
    # Keep the shareable ZIP compact: the complete offline app lives in index.html.
    # These entrypoints still open an individual prototype, without duplicating all scores.
    target='index.html#'+i['id']
    entry=f'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{i['short']} — Prototypes van Floris</title><script>location.replace({json.dumps(target)});</script><p><a href="{target}">Open {i['short']}</a></p></html>'''
    (DIST/f"{i['number']}-{i['id']}.html").write_text(entry)
    attribution = 'Aanvullend voorstel.' if i.get('group') == 'aanvullend' else 'De kleine aanpassingen uit het overzicht zijn in dit voorbeeld alvast meegenomen.'
    if i.get('extra'): attribution += ' '+i['extra']
    section = f"## {i['number']} — {i['short']}\n\nDe vraag: {i['question']}\n\n{attribution}\n\n{i['why']}\n\n{i['tradeoff']}\n\nProbeer: {i['try']}\n\n"
    if i.get('comment'):section += i['comment']+'\n\n'
    for v in i['variants']:
        prompt = prompt_for(i,v)
        (DIST/f"{i['number']}-prompt-{v}.txt").write_text(prompt)
        section += f"### {i[v.lower()]}\n\n{prompt}\n\n"
    (DIST/f"{i['number']}-{i['id']}.md").write_text('# '+section.lstrip('# '))
    doc += section+'\n---\n\n'
discussion_doc = small_doc + questions_doc
(DIST/'Kleine-suggesties-en-vragen.md').write_text('# '+discussion_doc.lstrip('# '))
(DIST/'Suggesties-van-Floris.md').write_text(doc)
(DIST/'Floris-voorbeeldpartituur.pdf').write_bytes(base64.b64decode(assets['pdf']))
context = ROOT/'src/score-context.md'
if context.exists():
    (DIST/'Score-ervaring-voor-Claude.md').write_text(context.read_text())
(DIST/'LEESMIJ.txt').write_text('''Prototypes van Floris

Open index.html in je browser. Dit bestand werkt op zichzelf en offline.
De genummerde HTML-bestanden openen direct hun eigen voorbeeld via index.html.
Laat die bestanden bij elkaar in dezelfde map; alleen index.html bevat alle data.
Je kunt ook uitsluitend index.html sturen: dat werkt zelfstandig en offline.
Het overzicht begint met kleine aanpassingen in bullets. Daaronder staan
vijf prototypes, elk met één grotere vraag. Aanvullende input vult bestaande
voorbeelden aan. De kniplijst staat bij prototype 04; export is alleen een opmerking.

1. Probeer een suggestie en vergelijk de beschikbare varianten.
2. Klik Kopieer prompt bij de variant die je wilt gebruiken.
3. Plak de prompt in je eigen Claude. Jouw ontwerpkeuzes gaan voor.

Filmmodus is handig voor een schermopname. Escape toont de uitleg weer.
Suggesties-van-Floris.md bevat alle uitleg en de beschikbare prompts per voorbeeld.
De prompts staan ook los in de genummerde .txt-bestanden.
Onderaan het overzicht kun je suggesties aanvinken en per voorstel één variant
kiezen. Kopieer of download daarna de hele selectie voor Claude. De bestaande
teksten worden samengevoegd; er wordt geen nieuwe prompt gegenereerd.
De selectie wordt waar mogelijk in deze browser bewaard en reist niet mee
met de ZIP. De ontvanger kiest zelf wat hij wil overnemen.
Aanvullende-input.md bevat de aanvullende input en waar die is verwerkt.
Bestaand-scherm-context.md beschrijft de zichtbare bestaande functies uit de
aangeleverde inspector-HTML, plus de beperkingen van die momentopname.
Score-ervaring-voor-Claude.md geeft optionele achtergrond uit Floris’ andere project.
Partituren-overzicht.md en Score-catalogus.json beschrijven de gevonden boeken
en cuepagina's. Prototype 04 opent per cue de bijbehorende full-scorepagina’s.
Arrival staat op PDF-pagina 7–9, maat 1–41. Het originele boek blijft ongewijzigd.
De overige maatvakken zijn benaderd vanuit gedrukte maatnummers; meermaatsrusten
zijn niet opgesplitst. 1M09A en 1M09B delen de score 1M09AB, met aparte take-data.
Elke take heeft eigen notes en geselecteerde maten. Een nieuwe take begint schoon.
Cmd + linksklik voegt volledige maten toe voor alle instrumenten; Cmd + rechtsklik
verwijdert volledige maten. Slepen werkt ook, zonder dat Shift nodig is.
Dubbelklik opent een invoerveld. Enter zet alleen tekst boven de betreffende
notenbalk, of boven het systeem voor Alle instrumenten. Onder/Vrij blijven opties.
Met Cmd/Ctrl+klik in de take-lijst kun je takes vergelijken. Takekleuren blijven in de
lijst en geselecteerde maatvakken herkenbaar. Cmd+Z maakt
selectie- en commentacties ongedaan. De score loopt volledig door.
Prototype 04B onderzoekt de partituur als hoofdwerkplek: takes en notes links,
met een compact sessieblok rechtsboven voor de lopende take, cuetijd en planning.
Op Windows/Linux gebruik je Ctrl. Wissel links van take om zijn eigen laag te zien.
De gewone voorstellen gebruiken dezelfde opnamecomponenten; de kniplijst is apart.
Suggestie 2 heeft vaste take-regels, één notitiepaneel en een tijdlijn. Vorige/nieuwe
versie zijn vergelijkbaar; je kunt per wijziging een oordeel bewaren.
Wijzigingen-18-oktober.md beschrijft wat er veranderd is.
Alle programma-UI is Engels; vragen en uitleg voor de collega blijven Nederlands.
Eigen notities, cue-/projectnamen en de oorspronkelijke partituren blijven behouden.
Alleen demo-data; herladen wist die.
De vraag over timen/loggen en gedeelde take-telling staat onder Vragen;
hiervoor is geen zelfstandig prototype meer.

Er wordt geen audio opgenomen of bestand geüpload. Demo-notities en een eigen
PDF verdwijnen bij herladen. Alleen beoordelingen worden waar mogelijk lokaal
bewaard. Reset wist het huidige voorbeeld, niet je beoordeling.

Het echte Arrival-fragment is meegeleverd als drie gecontroleerde paginabeelden
en als Afterparty-1M02-Arrival-excerpt.pdf. Fragmentpagina 1–3 correspondeert met
boekpagina 7–9. De klikgebieden zijn handmatig gecontroleerd. Een eigen PDF
krijgt die mapping niet automatisch. Er is geen live score following.
De schematische proef is apart te kiezen en heeft vooraf ingestelde
voorbeeld-tijdankers. Bij de echte score blijft Volg maat uit zolang tijdankers
van een echte take ontbreken. Klik na Enter direct op het maatcijfer om te
corrigeren; het pijltje brengt je naar de bekende scoreplek.
In suggestie 2A staan alle notes bovenaan volledig onder elkaar, zonder eigen
scrollvak. Het paneel groeit mee met de lijst.
''')
print(f'Built one standalone offline app, {len(ideas)} direct entrypoints, {sum(len(i["variants"]) for i in ideas)} prompts and score documents.')
