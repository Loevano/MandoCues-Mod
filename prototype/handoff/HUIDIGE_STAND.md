# Eén voorstel · 18 oktober 2026

De huidige richting vervangt het overzicht met vijf afzonderlijke prototypes.

- Eén opnameweergave, gebaseerd op de gekozen 2A: bediening bovenaan en compacte balk bij scrollen. Eén doorlopend scrollgebied, inclusief kop en sessie-instellingen, zonder geneste kaders.
- Eén kniplijst met de bestaande wijzigingen: permanent grote doorlopende score met knop-/trackpadzoom en één compacte bovenbalk, takes en notes, All takes, instrument-/zichtbaarheidsinstellingen, note-navigatie en slepen.
- De PDF-zoom is één globale werkruimte-instelling: wisselen van cue, take, scorebron of weergave behoudt het percentage en de schaal. Alleen handmatig zoomen of Fit width verandert die.
- Alt heet overal Alt, zonder volgnummer. Het totale aantal alternatieven staat bij de cue en in de scoreweergave.
- Cuegegevens blijven behouden: muziekduur, bewerkbare Complexity en Planned (min), Actual als cumulatieve werktijd en een handmatig Done-vakje. Planned stuurt de cuebegroting en tijdlijn; de bestaande demo-sessieplanner houdt zijn eigen voorbeeldberekening. Afgerond verschijnt ook in de tijdlijn en staat los van geselecteerd/lopend.
- Recording en Comp tool delen cue, take, opname, beoordelingen, notes en concepten. Een lopende take blijft lopen bij wisselen.
- Bij openen: Rondleiding starten of Zelf bekijken. Voorstelnaam en reviewknoppen staan in een aparte compacte balk boven beide weergaven.
- De rondleiding scrolt automatisch naar elk onderdeel. Quick notes staan direct zichtbaar bij de editor.
- De rondleiding volgt de workflow: hoofdpaneel → sessiestart en planning → cue en take kiezen → notes → beoordeling → sneltoetsen → partituur en kniplijst → vergelijken en instellingen. Open vragen staan apart.
- De uitleg is gericht aan de collega: vrijblijvende ideeën en korte aanwijzingen om te proberen, zonder eigen bugfixes of ontwerphistorie uit te leggen.
- De rondleiding bevat 26 korte suggesties met een highlight, een standaard aangevinkte checkbox voor Claude en Terug/Volgende. Uitvinken blijft mogelijk; expliciete uitvinkkeuzes worden bewaard. Oude gedeeltelijke opt-in-selecties worden eenmalig vervangen door alles aan. Kiezen beïnvloedt alleen de prompt, niet de werking van de demo.
- De selectie blijft lokaal in de browser bewaard. Kopiëren/downloaden voegt bestaande teksten samen; geen nieuwe generatie. Open vragen staan apart.
- GUI Engels; uitleg en vragen Nederlands. Command+Enter start eerst de sessie en daarna een take, of stopt de lopende take. Dit werkt ook met focus op de rondleiding. Enter plaatst een note en spatie is tekst.
- Herkenbare appcontext: zijbalk, sessiekeuze, Session length (min), Prep per cue, Max music (min), Add cues, Chat standaard dicht en de PDF-overzichten. De inspectie-HTML is geen volledige appbron; planningscijfers zijn voorbeelddata.
- Hoofdpaneel: Previous cue en Next cue met bracket-hints op een vaste rij onder de cuenaam, Overdub naast opnemen en een koffie-icoon bij Break. Standby vermeldt Not recording; alleen de lopende status is rood. Een duidelijke rode Recording-badge in grote/compacte bediening en bij de lopende take blijft herkenbaar als je een andere take bewerkt, zonder rood schermkader. Time is groter, met voor-/achterstand eronder: − achter, + voor en 00:00 op schema. Achterstand onder vijf minuten oranje, vanaf vijf minuten rood; voorsprong groen en nul neutraal. Geen zichtbare ahead/behind-tekst. Expected end voorlopig weg uit hoofd- en compacte bediening, ook in Comp tool. Cue-tijd/gepland en take-tijd blijven staan; overige sessietijden onder Session details. Het doel van de verschillende klokken is een open vraag.
- Note-metadata vóór én na Enter op dezelfde manier bewerken: zwevende scrollbare Bar-lijst met All voor de hele take, typen plus Enter voor een maat, tijdcode aanklikken en Enter. Het klokje vult de huidige tijdcode van die take in; Enter plaatst de note en zet een nieuw concept klaar. Alleen Delete blijft als aparte actie.
- Score-notes: dubbelklik neemt de maat op die plek over, ook vlak boven de balk. Slepen toont de doelmaat en past de maat-/instrumentcontext aan. Klik een bestaande score-note en verwijder met ⌫ of Delete naast Cancel; ⌘Z herstelt hem. Tekstvelden houden gewone tekstbewerking.
- Maatnummers bij notes zijn handmatig: invullen of bewust in de partituur kiezen. Geen Follow bar of afleiding uit de take-timer.

## Sneltoetsen

In beide weergaven: [ vorige cue, ] volgende cue; Alt+[ vorige take, Alt+] volgende take. Alt+1 t/m 9 kiest het echte take-nummer. Voor Take 12: Alt+Command indrukken, loslaten, 1 en 2 typen. Escape of vijf seconden zonder invoer annuleert. Brackets ingedrukt houden herhaalt navigatie en versnelt na kort vasthouden. Bij de eerste en laatste cue stopt navigatie; brackets en cuepijlen springen niet naar de andere kant. De eerdere keuze op cuevolgorde vervalt; de open vraag hierover is beantwoord. Takekeuze verandert de bewerkingslaag, nooit de lopende opname.

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
- `prototype/check_navigation_keys.py`: dezelfde cue-/takebediening in beide weergaven, twee cijfers, leespositie, concepten, live take en beschermde tekst-/sleep-/modale interacties.
- `prototype/src/proposal-shell.js`: herkenbare appcontext en lokale sessie-/Chat-/PDF-acties.
- `prototype/check_draft_metadata.py`, `check_bracket_hold.py`, `check_app_context.py` en `check_recording_state.py`: conceptmetadata, vasthouden van brackets, appcontext en opnamestatus/tijden.
- `prototype/check_unified_workspace.py` en `check_proposal_tour.py`: gedeelde gegevens, live take, promptkeuze en telefoonformaat.
- `prototype/check_review_bar.py`, `check_score_note_location.py` en `check_score_note_delete.py`: aparte reviewbalk bovenaan, note-plaatsing/slepen en verwijderen met herstel.
- `prototype/check_note_metadata.py`, `check_tour_scroll.py`, `check_score_pinch.py` en `check_score_zoom.py`: directe metadata, automatische rondleidingnavigatie, trackpadzoom en compacte scorewerkruimte.
- `prototype/check_all_takes.py`, `check_score_note_drag.py`, `check_score_settings.py` en `check_score_take_scroll.py`: bestaande scorebewerkingen en leespositie.
- `prototype/legacy-checks/`: checks van de eerdere vijf prototypes. Alleen bij de oude Git-tag van toepassing.

Alles bouwt met Python 3.10+ zonder extra pakketten. `python3 -X utf8 prototype/check_handoff.py` vergelijkt de huidige uitvoer met een schone geïsoleerde build. Browsercontroles gebruiken optioneel Playwright; zie `prototype/README.md`.
