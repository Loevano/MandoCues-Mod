# Werken aan deze overdracht

- Maak voor iedere afzonderlijke wijziging een eigen Git-commit. Bundel geen onafhankelijke wijzigingen in één commit; valideer elke wijziging voordat je die commit.
- Lees `HUIDIGE_STAND.md` voor de huidige keuzes. `prototype/src/feedback.md` is chronologische geschiedenis; latere correcties gaan voor eerdere wensen.
- Dit is een lokaal suggestieprototype, geen werkende opname-app. Behoud het karakter van vrijblijvende voorstellen en de bestaande vormgeving. Verander geen externe app, originele scoreboeken of ander project.
- Alle daadwerkelijke GUI-tekst is Engels, inclusief hints, toegankelijkheidslabels en meldingen. Vragen, prompts en toelichting buiten de demo mogen Nederlands blijven. Vertaal geen oorspronkelijke cue-/projectnamen of zelf getypte notes.
- Bewerk bronbestanden onder `prototype/src/`; `prototype/dist/` wordt gegenereerd. Bouw na wijzigingen met `python3 -X utf8 prototype/build.py` vanuit deze map.
- `build.py`, `score_fixture.py`, `production_score.py` en `score_overview.py` gebruiken alleen de Python-standaardbibliotheek. Alle benodigde score-assets zitten in `prototype/src/score-assets/`. Externe projecten en originele scoreboeken zijn geen buildvereiste.
- Behoud vaste posities voor sterren, Best en Alt. Een gekozen take mag geen verspringende knoppen of onverwacht groter wordende rijen veroorzaken.
- Enter plaatst een note; Shift+Enter geeft een nieuwe regel. Spatie is gewone tekst. Op Mac start Command+Enter een nieuwe take als er geen loopt en stopt de lopende take als die er wel is, ook tijdens typen. Negeer key-repeat en IME-compositie; gewoon Enter plaatst een note. Stop hoort bij de opnamebediening, niet naast Add/Delete in de note-editor.
- Geselecteerde take en lopende take zijn onafhankelijk. Een nieuwe take heeft eigen lege notes en kniplijstselectie.
- Kniplijstselecties betreffen hele maten. Link instruments staat standaard aan (alle instrumenten samen); uit selecteert per instrument. See other takes toont/verbergt alleen achtergrondselecties; expliciet vergeleken takes blijven zichtbaar. Cmd/Ctrl+links klikken/slepen voegt toe; rechts verwijdert. Gewone klik kiest een take; Cmd/Ctrl+klik vergelijkt meerdere takes. Dubbelklik op de score maakt een note.
- Score-notes zijn kale tekst op de score. Instrumentgebonden tekst hoort bij dat instrument; All instruments staat boven de bovenste balk bij die maat, binnen de gekozen take. De PDF zelf blijft ongewijzigd.
- Geen nieuw prototype 06: montage/export en de vraag over take-timers zijn toelichting of vragen, geen aparte demo.
- Controleer na wijzigingen gericht de betrokken flows. `python3 -X utf8 prototype/check_handoff.py` verifieert de pakketinhoud en een schone rebuild. Browsercontroles staan beschreven in `prototype/README.md`.
- Publiceren, uploads en het aanmaken van een gedeelde repository horen niet bij het overnemen van dit pakket.
