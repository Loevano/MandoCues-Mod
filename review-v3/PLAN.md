# v3 — kleine aanpassingen op de vorige indeling

Bijgewerkt 3 november 2026.

Laatste keuze van Floris: behoud A, de vorige indeling. Alleen cuevolgorde herschikken via de sleepgreep overnemen. De eerder bevestigde Space-bediening blijft: eerst alleen sessiestart, daarna take starten/stoppen, met gewone spaties tijdens tekstinvoer.

Open [index.html](index.html). Deze pagina heeft de bestaande take-/cue-notes, hoofdklokken, scoreweergave en oorspronkelijke rondleiding. De brede A/B-balk en overige nieuwe experimenten zijn niet actief. Er is geen nieuwe notes-layout, clock display-menu of driepanelenweergave.

De sleepgreep staat links van de cues. Order kiest opnamevolgorde of cuevolgorde als weergavesortering. Slepen verandert geen cue-/take-/note-identiteit. Tijdens opnemen is herschikken geblokkeerd.

Herstelpunten: v2 blijft bewaard als before-session-review-v3-20261102. De volledige A/B-ronde is apart bewaard als [experiments.html](experiments.html) en Git-tag v3-full-ab-review-20261102. Niets verwijderd uit die geschiedenis.

Bouwen: python3 review-v3/build.py. Controleren: check_minimal.py met Playwright en python3 review-v3/check_review.py. build-experiments.py bouwt alleen het historische experimentenbestand. Er wordt niets online gepubliceerd in deze ronde.

## Eerdere brede review — historisch, niet de huidige richting

# v3 — review na de echte opnamesessie

2 november 2026. Floris testte de **originele MandoCues-site**, niet ons voorstel. De aangeleverde tekst is denkrichting, geen blind uit te voeren specificatie.

## Versies en herstel

- **v2**: voorstel van 19 oktober, code `1bb803e` (functionele UI `93124f8`), tien suggesties met planning als nummer 6. De laatste bevestigde hostingversie is 2.
- Bewaard met tag `before-session-review-v3-20261102` en backupmap `../../Backups/before-session-review-v3-20261102` vanaf deze map. Die bevat een zelfstandige demo, de hostingbron, een bron-ZIP, volledige Git-bundle en SHA256-manifest.
- **v3**: branch `feature/session-review-v3`. Alle voorstellen samen als een A/B-reviewrondleiding; geen goedgekeurde vervanging van v2. De bestaande `prototype/src` en gegenereerde app blijven voorlopig gelijk.
- Online versie vandaag niet opnieuw te bevestigen: Sites geeft `project_not_found`. Niet zonder overleg een nieuw project registreren of de oude link vervangen. Geen publicatie aangevraagd voor deze reviewronde.

## Bevestigd door Floris

Spatie blijft voorlopig de handmatige start-/stoptoets buiten tekstvelden. Tijdens het typen blijft het een gewone spatie. De eerste spatie start alleen de sessie; volgende drukken starten/stoppen takes. Pro Tools is op expliciet verzoek voorlopig uitgesteld; daar nu geen koppeling, test of extra vragen voor maken.

## Eén ronde met acht A/B-stappen

Open [index.html](index.html). Alles is uitgewerkt als één lokale rondleiding, met terug/volgende, A/B-keuze, overslaan en opmerkingen. Aan het einde staat een overzicht met JSON-download. De keuzes blijven alleen als reviewvoorkeuren op dit apparaat bewaard, geen definitieve goedkeuring of wijziging van v2. Demo-takes en notes verdwijnen nog bij herladen.

| Stap | A | B |
| --- | --- | --- |
| 1. Werkplek | Vorige indeling | Actieve takes en notes naast de bediening; kleinere tijden onder More timing |
| 2. Eerdere opmerkingen | Notes van de gekozen take | Alle notes van deze cue samen met hun take-eigenaar |
| 3. Take-secties | Eén bereikveld, zoals 4–10 | Van/Tot en takes gegroepeerd per bereik |
| 4. Maatlabels bij notes | ⌘J opent een zwevend bereikveld | Van/Tot direct bij de editor |
| 5. Planning | Resterende tijd volledig herverdelen | Gekozen budgetten vastzetten; alleen het overige herverdelen |
| 6. Cuevolgorde | Slepen aan de greep | Pijltjes voor omhoog/omlaag |
| 7. Klokken | Instellingen in compact Clock display-menu | Instellingen direct zichtbaar |
| 8. Partituur | Leespartituur naast de notes | Grote bestaande Comp tool |

Vaste afspraken: Space start eerst alleen de sessie; daarna start/stop van takes. In tekstvelden blijft het een gewone spatie. Command+Enter blijft als bestaande bediening beschikbaar. Pro Tools staat op hold en heeft geen reviewstap.

Bij de take-sectie opent ⌘⇧J de invoer. Het bereik wordt alleen aan volgende gewone takes toegekend; nummers lopen door en bestaande takes wijzigen niet. Tijdens een take kan het bereik niet veranderen. Notelabels zijn aparte metadata, ook in de take-logexport; Enter blijft opslaan en een volgend concept klaarzetten.

De planner toont een preview met eindtijd, toekomstige pauze, buffer en voorbereiding. Apply wijzigt alleen de demo. Afgeronde cues blijven behouden. Rekenfouten worden niet gemaskeerd met minimumwaarden; een onmogelijke verdeling blokkeert toepassen. Een gereserveerde pauze wordt tijdens daadwerkelijk pauzeren verbruikt zodat dezelfde tijd niet tweemaal als vertraging telt.

Cuevolgorde gebruikt aparte verwijzingen naar cues; de cue-, take- en notearrays worden niet herschikt. Recording order bepaalt de navigatie. Cue order is een aparte natuurlijke codesortering en overschrijft de opnamevolgorde niet. Herordenen is tijdens opnemen geblokkeerd. Current cue springt alleen op verzoek; geen voortdurend automatisch scrollen.

Klokinstellingen wijzigen alleen de weergave van sessietijden; note-kloktijden blijven intact. Lokale tijd, UTC, Amsterdam of Los Angeles zijn beschikbaar. Er is geen gesimuleerde projecttijdcode. De leespartituur en Comp tool delen de bestaande globale zoom en bron.

## Bouwen en controleren

```sh
python3 review-v3/build.py
python3 review-v3/check_review.py
```

Browsercontrole met de bestaande Playwright-omgeving:

```sh
'/Users/florisheemskerk/Documents/Coding/Composition Study/.venv/bin/python' review-v3/check_round.py
```

`check_review.py` controleert v2-checksums, herstelpunt en deterministische build. `check_round.py` oefent alle acht varianten en de echte metadata-/transport-/plan-/sorteeracties op desktop en klein scherm. De volgende bronbestanden vormen samen deze reviewlaag: review.js, sections.js, note-ranges.js, planner.js, cue-order.js, clocks.js, reference-score.js en review-tour.js.

## Rekenkader voor de planningsproef

Beschikbare minuten = nieuwe eindtijd minus nu minus expliciete pauze/buffer. Alleen resterende, onafgeronde cues herverdelen. Muziekduur × complexiteitsgewicht (voorlopig 0,7 / 1 / 1,5) geeft de verhouding; trek voorbereiding eerst af. Trek geen reeds verricht werk nogmaals van de nieuwe resterende tijd af. Houd te weinig tijd zichtbaar; een minimum mag de beschikbare minuten niet stilzwijgend overschrijden.

Voor het voorbeeld (zonder voorbereiding/buffer): medium 2 min, medium 2 min, medium 2 min, hard 1 min, easy 1 min krijgen gewichten 2 / 2 / 2 / 1,5 / 0,7. Totaal 8,2. Bij 60 resterende minuten is dat circa 14,6 / 14,6 / 14,6 / 11,0 / 5,1 min. Afronding moet exact tot het beschikbare budget optellen. Dit is een voorstel, geen gekalibreerde sessieplanner.

Het eerdere [Pro Tools-onderzoek](research/PRO_TOOLS.md) blijft alleen als naslag bewaard; het hoort niet bij deze ronde.

## Nog te vragen / valideren

- Pro Tools-onderzoek en bijbehorende vragen staan on hold; nu niet verder uitwerken.
- Gegevens van de echte sessie kunnen de planner kalibreren; geen verzonnen empirische prestaties gebruiken.
- Geen notes of audio automatisch verwijderen omdat een engineerclip weg is; behoud IDs, herkomst en een wijzigingslog.
