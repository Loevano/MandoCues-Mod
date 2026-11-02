# v3 — review na de echte opnamesessie

2 november 2026. Floris testte de **originele MandoCues-site**, niet ons voorstel. De aangeleverde tekst is denkrichting, geen blind uit te voeren specificatie.

## Versies en herstel

- **v2**: voorstel van 19 oktober, code `1bb803e` (functionele UI `93124f8`), tien suggesties met planning als nummer 6. De laatste bevestigde hostingversie is 2.
- Bewaard met tag `before-session-review-v3-20261102` en backupmap `../../Backups/before-session-review-v3-20261102` vanaf deze map. Die bevat een zelfstandige demo, de hostingbron, een bron-ZIP, volledige Git-bundle en SHA256-manifest.
- **v3**: branch `feature/session-review-v3`. Alle voorstellen samen als een A/B-reviewrondleiding; geen goedgekeurde vervanging van v2. De bestaande `prototype/src` en gegenereerde app blijven voorlopig gelijk.
- Online versie vandaag niet opnieuw te bevestigen: Sites geeft `project_not_found`. Niet zonder overleg een nieuw project registreren of de oude link vervangen. Geen publicatie aangevraagd voor deze reviewronde.

## Bevestigd door Floris

Spatie blijft voorlopig de handmatige start-/stoptoets buiten tekstvelden. Tijdens het typen blijft het een gewone spatie. De eerste spatie start alleen de sessie; volgende drukken starten/stoppen takes. Pro Tools is op expliciet verzoek voorlopig uitgesteld; daar nu geen koppeling, test of extra vragen voor maken.

## Volgorde en afbakening

| Ronde | Probleem / voorstel | Wat Floris kan beoordelen | Nog open |
| --- | --- | --- | --- |
| 1 | Minder zoeken en scrollen | A huidige voorstelindeling; B notes en actieve takes direct naast bediening en planning. Eén klik Current cue naar het overzicht; geen automatisch springen. Eerdere notes binnen de cue direct terugleesbaar. | Welke indeling? Zijn Session setup en More timing inklapbaar prettig? Hoeveel eerdere notes tegelijk nodig? |
| 2 | Snelle handmatige start | Afzonderlijke schakelaar in de review om Space en bestaande bediening te proberen; tekstinvoer beschermd. | Bevestigd: eerste Space start alleen de sessie. |
| 3 | Secties en maatlabels | Los prototype voor maatbereik vóór take en voor een note, bijvoorbeeld 4–10 of 13–20; apart van commenttekst. | Sneltoetsen kiezen zonder bestaande Option+take-keuze te breken. Voorstel: Command+J opent note-maatbereik vanuit editor; Command+Shift+J takebereik. Eerst toetsen en beoordelen. |
| 4 | Flexibele planning | Preview met nieuwe eindtijd, pauze en resterende cues. Voor/na per cue vergelijken vóór toepassen. | Handmatige overrides beschermen of na expliciete keuze herverdelen; buffer en voorbereiding. Niet stilzwijgend tijdnood groen rekenen. |
| 5 | Cuevolgorde | Opnamevolgorde via slepen; Cue order als aparte sortering. IDs houden, array-indexen niet als permanente identiteit gebruiken. Current cue-knop. | Reorder tijdens opnemen blokkeren? Reorder heeft alleen effect op opnamevolgorde, niet op cue-identiteit. |
| 6 | Instelbare tijden | Kleine instellingen voor zichtbare klokken, primaire klok/tijdcode en optionele tweede tijdzone. | Voorkeuren per gebruiker/dag; geen extra standaardklokken. |
| 7 | Score/Comp tool | Bestaande continue score en globale zoom behouden; optie score naast notities beoordelen. | A4 blijft beschikbaar; Comp tool nog praktijkgericht uitproberen. |
| — | Pro Tools | Uitgesteld op verzoek van Floris. Bestaand onderzoek blijft alleen als naslag bewaard. | Niet nodig voor deze review. |
| 9 | Rondleiding | Alleen de goedgekeurde veranderingen in workflowvolgorde uitleggen. | Niet vóór review de oude tour vervangen. |

## Eén reviewronde

Open [index.html](index.html). Dit is een lokale vergelijking op basis van echte v2-componenten en gedeelde demo-state. Wisselen A/B mag notes, concepten en een lopende take niet verliezen. Alle acht onderdelen komen achter elkaar, elk met A/B, terug/volgende en een gezamenlijk keuzeoverzicht. De reviewknoppen slaan alleen een voorkeur op; geen automatische toepassing op de gedeelde of online versie.

In B staan actieve takes en het noteveld direct naast de bediening, gevolgd door eerder opgeslagen notes. Session setup en de vier kleinere sessietijden (More timing) zijn bewust inklapbaar; klok en planningsafwijking blijven zichtbaar. Het overzicht van alle cues staat eronder. De notitiebron blijft expliciet: bekijken van een oudere take verandert de lopende opname niet. Eerdere notes uit andere takes openen hun eigen take om verder te werken.

De Space-proef is apart aan/uit te zetten. Standaard Space volgens de laatste wens. De proef toont geen gekoppelde DAW en belooft geen automatische synchronisatie.

## Planningvoorstel om later te testen

Beschikbare minuten = nieuwe eindtijd minus nu minus expliciete pauze/buffer. Alleen resterende, onafgeronde cues herverdelen. Muziekduur × complexiteitsgewicht (voorlopig 0,7 / 1 / 1,5) geeft de verhouding; trek voorbereiding eerst af. Trek geen reeds verricht werk nogmaals van de nieuwe resterende tijd af. Houd te weinig tijd zichtbaar; een minimum mag de beschikbare minuten niet stilzwijgend overschrijden.

Voor het voorbeeld (zonder voorbereiding/buffer): medium 2 min, medium 2 min, medium 2 min, hard 1 min, easy 1 min krijgen gewichten 2 / 2 / 2 / 1,5 / 0,7. Totaal 8,2. Bij 60 resterende minuten is dat circa 14,6 / 14,6 / 14,6 / 11,0 / 5,1 min. Afronding moet exact tot het beschikbare budget optellen. Dit is een voorstel, geen gekalibreerde sessieplanner.

Zie ook [onderzoek Pro Tools](research/PRO_TOOLS.md).

## Nog te vragen / valideren

- Pro Tools-onderzoek en bijbehorende vragen staan on hold; nu niet verder uitwerken.
- Gegevens van de echte sessie kunnen de planner kalibreren; geen verzonnen empirische prestaties gebruiken.
- Geen notes of audio automatisch verwijderen omdat een engineerclip weg is; behoud IDs, herkomst en een wijzigingslog.
