# Eén voorstel · 18 oktober 2026

De huidige richting vervangt het overzicht met vijf afzonderlijke prototypes.

- Eén opnameweergave, gebaseerd op de gekozen 2A: bediening bovenaan en compacte balk bij scrollen.
- Eén kniplijst met de bestaande wijzigingen: permanent grote doorlopende score met knop-/trackpadzoom en één compacte bovenbalk, takes en notes, All takes, instrument-/zichtbaarheidsinstellingen, note-navigatie en slepen.
- Recording en Cut list delen cue, take, opname, beoordelingen, notes en concepten. Een lopende take blijft lopen bij wisselen.
- Bij openen: Rondleiding starten of Zelf bekijken. Voorstelnaam en reviewknoppen staan onderaan Recording; in de kniplijst blijven ze compact bereikbaar.
- De rondleiding scrolt automatisch naar elk onderdeel. Quick notes staan direct zichtbaar bij de editor.
- De rondleiding volgt de workflow: hoofdpaneel → sessiestart → planning en cue/take → beoordeling en notes → partituur en kniplijst. Open vragen staan apart.
- De rondleiding bevat 26 korte suggesties met een highlight, een standaard aangevinkte checkbox voor Claude en Terug/Volgende. Uitvinken blijft mogelijk; expliciete uitvinkkeuzes worden bewaard. Oude gedeeltelijke opt-in-selecties worden eenmalig vervangen door alles aan. Kiezen beïnvloedt alleen de prompt, niet de werking van de demo.
- De selectie blijft lokaal in de browser bewaard. Kopiëren/downloaden voegt bestaande teksten samen; geen nieuwe generatie. Open vragen staan apart.
- GUI Engels; uitleg en vragen Nederlands. Command+Enter start eerst de sessie en daarna een take, of stopt de lopende take. Dit werkt ook met focus op de rondleiding. Enter plaatst een note en spatie is tekst.
- Hoofdpaneel: zichtbare Take-/Cue-/Session-knoppen, inclusief Break en End session. Cue-tijd/gepland, take-tijd, voor-/achterstand, kloktijd en verwachte eindtijd blijven in beeld; overige sessietijden onder Session details. Het doel van de verschillende klokken is een open vraag.
- Note-metadata direct bewerken: zwevende scrollbare Bar-lijst met All voor de hele take, typen plus Enter voor een maat, tijdcode aanklikken en Enter. Het klokje herstelt het oorspronkelijke typmoment. Alleen Delete blijft als aparte actie.
- Score-notes: dubbelklik neemt de maat op die plek over, ook vlak boven de balk. Slepen toont de doelmaat en past de maat-/instrumentcontext aan. Klik een bestaande score-note en verwijder met ⌫ of Delete naast Cancel; ⌘Z herstelt hem. Tekstvelden houden gewone tekstbewerking.
- Maatnummers bij notes zijn handmatig: invullen of bewust in de partituur kiezen. Geen Follow bar of afleiding uit de take-timer.

## Nog te kiezen: sneltoetsen

⌥1–9 kiest nu plek 1–9 in de cuelijst (1M02, 1M18, …), alleen in Recording. Nieuw voorstel, nog niet ingevoerd: ⌥1–9 voor echte take-nummers, ⌥[ / ⌥] voor vorige/volgende take en [ / ] voor cues, met dezelfde betekenis in beide weergaven. De vraag staat onder Vragen; zie feedbackpunt 58.

## Herstelpunt

De versie vóór deze samenvoeging is commit `d5f7119`, Git-tag `before-unified-ui-20261018`. Dezelfde tag staat op GitHub. Je kunt die versie apart bekijken zonder het huidige werk te overschrijven:

```sh
git worktree add ../MandoCues-vorige-versie before-unified-ui-20261018
```

Daarna open je `../MandoCues-vorige-versie/index.html`. Er is ook een lokale ZIP: `MandoCues-herstelpunt-20261018-d5f7119.zip` naast de gedeelde werkkopie.

De demo is geen recorder en heeft geen echte DAW-/filmtijd of live score following. Maatvakken buiten Arrival zijn benaderingen. Nieuwe demo-invoer verdwijnt bij herladen. Echte gedeelde sessie-opslag en kniplijstexport zijn geen onderdeel van dit voorstel.

## Broncode en controles

- `prototype/src/unified-app.js`: de gedeelde werkruimte; hergebruikt bestaande opname- en scorecomponenten.
- `prototype/src/proposal-tour.json`: stappen, korte uitleg en vaste promptonderdelen. Geen A/B-keuzes in de nieuwe UI.
- `prototype/src/proposal-tour.js`: welkomstkeuze, highlights, opt-in selectie en prompt-export.
- `prototype/src/app.js`, `controls-calm.js`, `score-interactions.js`, `production-score.js` en `score-compare.js`: bestaande onderdelen en handlers. Oude presentatiefuncties zijn geen actieve losse prototypes meer.
- `prototype/build.py`: één offline HTML-app plus actuele uitleg. Oude genummerde HTML-links verwijzen door naar de gedeelde werkruimte; oude variantprompts worden niet meer uitgegeven.
- `prototype/check_unified_workspace.py` en `check_proposal_tour.py`: gedeelde gegevens, live take, promptkeuze en telefoonformaat.
- `prototype/check_review_footer.py`, `check_score_note_location.py` en `check_score_note_delete.py`: reviewbediening onderaan, note-plaatsing/slepen en verwijderen met herstel.
- `prototype/check_note_metadata.py`, `check_tour_scroll.py`, `check_score_pinch.py` en `check_score_zoom.py`: directe metadata, automatische rondleidingnavigatie, trackpadzoom en compacte scorewerkruimte.
- `prototype/check_all_takes.py`, `check_score_note_drag.py`, `check_score_settings.py` en `check_score_take_scroll.py`: bestaande scorebewerkingen en leespositie.
- `prototype/legacy-checks/`: checks van de eerdere vijf prototypes. Alleen bij de oude Git-tag van toepassing.

Alles bouwt met Python 3.10+ zonder extra pakketten. `python3 -X utf8 prototype/check_handoff.py` vergelijkt de huidige uitvoer met een schone geïsoleerde build. Browsercontroles gebruiken optioneel Playwright; zie `prototype/README.md`.
