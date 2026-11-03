# MandoCues — actuele projectkennis

Bijgewerkt 3 november 2026. Dit is het centrale overzicht voor Floris, Jens en een volgende coding-agent. De verwijzing in `Coding/Knowledge/Projects/MandoCues.md` wijst hierheen; houd geen tweede statuskopie bij. Oude instructies en bevindingen zijn volledig bewaard in [PROJECT_HISTORY.md](PROJECT_HISTORY.md).

## Waar we nu werken

| Onderdeel | Actuele plek en betekenis |
| --- | --- |
| Actieve ontwikkeling | [review-v4/index.html](review-v4/index.html): lokale v4-proef, Recording + Score |
| V4-bron | `review-v4/*.js`, `workspace.css`, [build.py](review-v4/build.py) |
| V4-algoritme | [PLANNING.md](review-v4/PLANNING.md), met formules, aannames en grenzen |
| V4-review | Knop **Review v4**: zes stappen; vijf werkende A/B-keuzes en Score |
| Gepubliceerde presentatie | [Floris-site, v3.2.2](https://mandocues-voorstel-floris.superfrog5.chatgpt.site/#recording) |
| Publicatiestatus | [review-v3/publication.json](review-v3/publication.json); hostingversie 3 is presentatie v3.2.2 |
| Bewaarde Comp tool | [review-v3/index.html#cutlist](review-v3/index.html#cutlist) |
| Repo / branch | `MandoCues-Mod`, `feature/session-review-v3`, remote `git@github.com:Loevano/MandoCues-Mod.git` |
| Laatste functionele v4-commit vóór deze kennisupdate | `6bb684d` |
| Praktisch gereedschap en publicatie | [WORKFLOW.md](WORKFLOW.md) |

V4 is **lokaal** en vervangt de gedeelde v3 niet. De root-`index.html`, `prototype/dist`, losse map `../prototype` en oude overdrachtsmappen zijn geen actuele v4. Lokale edits en GitHub-pushes publiceren niets automatisch.

## Doel en laatste keuzes van Floris

De originele MandoCues-site is het uitgangspunt. De echte opnamesessietest betrof die originele site, niet onze demo. Onze bron daarvan bestaat uit inspectie-HTML en screenshots; we hebben geen volledige productiecode of bewezen kopie van hun planner.

De laatste call verlegt de prioriteit naar **overzicht en betrouwbare tijdplanning**: hoeveel tijd is beschikbaar voor deze cue, hoeveel werk wordt nog verwacht en wat betekent dat voor het einde van de sessie? Notes zijn nuttig, maar niet de hoofdtaak. Vermijd extra panelen, overbodige klokken en algemene herontwerpen zonder concrete aanleiding.

Floris wil open ontwerpkeuzes achteraf beoordelen via werkende prototypes. V4 biedt daarvoor één reviewronde. Maak bij routinekeuzes een redelijke voorlopige keuze; presenteer wezenlijke keuzes in de review in plaats van losse vragen tussendoor. Geen automatisch welkomstbericht. Uitleg is beknopt, suggestief en gericht aan de collega; gewone bugfixes hoeven niet in de tutorial te worden uitgelegd.

GUI, knoppen, tooltips en toegankelijkheidslabels zijn Engels. Review, vragen en kennis mogen Nederlands zijn. Eigen notities, cuecodes en oorspronkelijke titels blijven ongewijzigd. Behoud herkenbare cue-/takehiërarchie, vaste knopposities en een ondubbelzinnige opnamestatus.

## Tijdplanning v4: wat is gebouwd

- **Opnameomvang** is de muziek die werkelijk opgenomen moet worden. Die staat los van de totale cueduur. De oude muziekduur is alleen de beginwaarde. Variant A vult één mm:ss-duur in; B telt expliciete duren per niet-overlappend maatbereik op. Maatnummers alleen geven geen betrouwbare muziekduur.
- Werkbelasting = opnameomvang × complexiteit. Voorlopig Easy 0,7 / Medium 1 / Hard 1,5, met voorbereiding apart. Het initiële sessiebudget levert het referentietempo; dit is een hypothese, geen bewezen haalbaarheidsmeting.
- Alleen afgeronde, betrouwbare cues trainen de schatting. Werk omvat ook tijd tussen takes. Take-aantal en take-duur zijn context, geen zelfstandige voortgangsmeter.
- Het model normaliseert voor complexiteit en omvang, begrenst uitschieters en dempt kleine datasets met drie cue-equivalenten aan referentiegewicht. Afgeronde werktijd wordt bij Done vastgezet.
- Beschikbare cuetijd en verwachte resterende werktijd blijven afzonderlijk. Een onafgeronde cue behoudt een expliciete afrondreserve tot Done of een handmatige resterende-werkschatting. Een lege budgetklok betekent niet dat de muziek klaar is.
- Resterende tijd herverdelen verlaagt niet stilzwijgend de werkschatting. Meer sessietijd is geen bewijs van lager werktempo. Oorspronkelijke cuebudgetten blijven bewaard naast actuele budgetten.
- **Cue timing** laat opnameomvang, budget, werkelijk werk, resterend werk en inclusie als leervoorbeeld corrigeren. Correcties bewaren oude/nieuwe waarde en tijdstip. Een gemiste cuewissel kan controle van beide cues vragen; er is geen automatische engineerwaarheid.
- Pauzes stoppen werkklokken; een vaste eindtijd blijft naderen. **Planning** heeft ±15/30/60 minuten om dezelfde eindtijd te wijzigen. Dit is daadwerkelijke budgetaanpassing, niet alleen een label voor voorspelde uitloop.
- Groen = op schema/ruimte; oranje = minder dan vijf minuten verwachte uitloop; rood vanaf vijf minuten. De overige tijden staan onder Timing details. AM/PM blijft voor kloktijden; duur is geen projecttijdcode.

Alle formules en beperkingen staan in [review-v4/PLANNING.md](review-v4/PLANNING.md). De belangrijkste volgende validatie is vergelijken met echte sessiedata en de productieplanner. Er is nog geen geavanceerd, empirisch gevalideerd studio- of ensemblemodel.

## Takes, ranges, notes en score

Gewone takes mogen verschillende instartbereiken hebben, bijvoorbeeld 2–8 en 12–19. **From bar / Till bar**, bereikknoppen en Whole cue werken voor volgende takes. Nummers lopen door; een ander bereik maakt geen overdub of nieuwe nummerreeks. Het bereik blijft bij de vaste take-ID, is achteraf bewerkbaar en staat in take-log/Take sheet. Verwijderde take-nummers worden niet hergebruikt, behalve bij de expliciete bevestigde sessiereset.

Recording en Score delen cue, geselecteerde take, lopende take, notes, beoordelingen, planning en bereik. Geselecteerd is niet hetzelfde als werkelijk opgenomen. Meerdere takes mogen Best zijn; Alt heeft geen volgnummer, alleen een totaal per cue. Notes en beoordelingen veranderen de lopende opname niet.

Score toont de partituur groot, doorlopend, met globale 10–300%-zoom, trackpadzoom, Fit width en één/twee pagina’s. Takekeuze behoudt de leespositie; cue-/viewkeuze reset zoom niet. Alleen de gekozen take wordt actief getoond. Compselecties/vergelijking zijn hier verborgen en geblokkeerd; oude data en de volledige Comp tool blijven in v3 bewaard.

Notes zijn kale tekst op de score. Dubbelklik kiest maat/instrumentcontext uit de mapping; slepen werkt die context bij. ‘All instruments’ betekent alle instrumenten binnen de gekozen take, boven het systeem bij die maat. Het betekent niet alle takes. Arrival heeft specifieke mapping; buiten die betrouwbare mapping zijn benaderingen geen echte notatieherkenning. Bron-PDF’s worden niet gewijzigd.

De note-tijd is een echte kloktijd met datum, geen take-/film-/DAW-tijdcode. Eerste letter of **N** legt het schrijfmoment vast; wissen van tekst reset het niet. Bewaar `writtenAt` apart van bewerkbare `clockAt`. Eerst **↓** voor nu, dan het klokje om de oorspronkelijke tijd te herstellen. Enter slaat op en bereidt de volgende note voor; Shift+Enter maakt een nieuwe regel. Bar is handmatig of bewust uit de score gekozen; geen automatische maat uit een lopende timer.

## Sneltoetsen die gelden

| Toets | Gedrag |
| --- | --- |
| Space | Buiten tekstinvoer: eerst alleen de sessie, daarna take start/stop |
| [ en ] | Vorige/volgende cue, stoppen aan de uiteinden; geen wrap |
| Option+[ en Option+] | Vorige/volgende take |
| Option+1 t/m Option+9 | Het echte gewone take-nummer, niet cuevolgorde |
| Option+Command vasthouden + twee cijfers | Bijvoorbeeld 12; loslaten annuleert onvolledige invoer |
| N | Noteveld focussen en schrijfmoment vastleggen, bestaand concept behouden |
| B, v4 | Recording: volgend bereik; Score: bereik van gekozen take bewerken |
| Enter / Shift+Enter | Note opslaan en volgende klaarzetten / nieuwe regel |
| Delete/Backspace / Command+Z | Geselecteerde score-note verwijderen / scorebewerking herstellen |

Option en Alt zijn dezelfde Mac-toets. Command+Enter is niet meer de opnamebediening. Geen Control-cijferkeuze toevoegen: Floris heeft bevestigd de bestaande navigatietoetsen te houden. Systeem-/browsercombinaties zijn niet vanzelf vrij; Control+Option wordt onder meer voor VoiceOver gebruikt. Bescherm tekstinvoer, modals, slepen, herhaalde events en IME. Alleen brackets mogen gedoseerd herhalen. Eigen sneltoetshints zijn vet en gekleurd; verander daarmee geen gebruikersnotes.

## Review en opslag

Review v4: (1) twee hoofdsignalen of tijden uitgeklapt, (2) opnameomvang per cue of bereik, (3) bereik invoeren of bereikpresets, (4) leren of vaste referentie, (5) budget herverdelen of vast, (6) Score. A/B verandert de zichtbare proef. De leer-/verdelingsvoorbeelden gebruiken herkenbaar aparte data en verzinnen geen metingen in de sessie. De kaart is versleepbaar; Mijn keuzes geeft overzicht en JSON-download.

**Notes, takes en timingmetingen zijn demo-state en verdwijnen bij herladen.** Reviewvoorkeuren blijven lokaal bewaard; de keuzes-download is een momentopname. Geen gedeelde backend, productie-opslag of audio-opname. De Chat/PDF-acties bewijzen geen samenwerking tussen computers. Daggegevens zijn in de demo gescheiden; bekijken van een andere dag pauzeert een al lopende sessie voorlopig niet. Dagwisseling tijdens een take is geblokkeerd.

## Pro Tools: kennis behouden, werk uitgesteld

De laatste call kiest voorlopig handmatige bediening; geen live Pro Tools-koppeling bouwen. Bewaar wel het onderzoek:

- [Kloktijden, WAV/BWF en koppelen achteraf](prototype/src/protools-sync.md), onderzocht 19 oktober.
- [LTC/MTC en mogelijke bridge](review-v3/research/PRO_TOOLS.md), onderzocht 2 november.

Session Info as Text levert clip-/bestands-/tijdlijninformatie; het is niet vanzelf een kalenderlog van opnamemomenten. BWF OriginationDate/OriginationTime, Original Time Stamp en TimeReference zijn verschillende velden. Documentatie bewijst niet dat de gebruikte Pro Tools-workflow betrouwbare opnamekloktijden schrijft. Test dat later met originele bestanden; Finder-datums zijn geen bewezen opnamestarts.

LTC/MTC kan projectpositie geven, maar bewijst geen record-state of cue-/take-identiteit. Een gewone kliklijn is geen LTC. Eventuele latere koppeling vraagt opname-events én vaste bronidentiteit, microfoongroepering, punches, datum/tijdzone/klokcorrectie en expliciete bevestiging. Geen automatische hernummering. Nieuwe demo-takes loggen echte lokale transportmomenten; voorbeeldtakes hebben geen verzonnen engineerlog.

Dit zijn bewaarde bevindingen met bronverwijzingen, geen garantie op de huidige Pro Tools-versie of een gebouwde integratie. Controleer primaire documentatie en een engineerpraktijktest vóór hervatting.

## Herstelpunten

| Versie | Herstelpunt |
| --- | --- |
| Laatste gedeelde v3.2.2 vóór v4 | Tag `before-v4-20261103`, commit `689779e`; SHA256 in [restore.json](review-v4/restore.json) |
| V3.1 | Tag `presentation-v3.1-20261103`, commit `ec3506e` |
| Afgewezen brede A/B-proef | Tag `v3-full-ab-review-20261102`, `review-v3/experiments.html` |
| V2 | Tag `before-session-review-v3-20261102`, commit `1bb803e`; bundle/ZIP/manifest in `../Backups/before-session-review-v3-20261102` |
| Vijf prototypes vóór samenvoeging | Tag `before-unified-ui-20261018`, commit `d5f7119` |

Open oude versies desgewenst in een aparte worktree; reset de actieve werkmap niet. Namen van branches/tags zijn geen bewijs van huidige online status. [publication.json](review-v3/publication.json) registreert de laatst geslaagde publicatie.

## Bekende aandachtspunten

- Safari/WebKit is niet afzonderlijk gevalideerd. Browserbewijs is Chrome/Chromium, inclusief 1512/900/390-pixelbreedtes.
- De historische Go to cue-zoekrace is niet aantoonbaar opgelost: een vertraagde toggle-handler kan zoektekst resetten. Niet als verholpen rapporteren zonder reproductie en fix.
- In de compacte Score-balk kan de kleur van Start session nog afwijken van de blauwe grote knop. De oude All takes-toggle had ook een onjuiste tooltip; v4 verbergt die toggle, v3 is daarmee niet gerepareerd.
- V4-leergewichten, afrondreserve, pauzebeleid, budgetverdeling en herstel van gemiste cuewissels moeten aan echte sessies worden getoetst.
- Productie-opslag, DAW-sync, betrouwbare automatische score-/maatvolging en uiteindelijke comp-export zijn niet gebouwd.
- Oude tests horen bij hun eigen versie. De oude v3-backupcheck verwacht nog de hostingkopie van v2 op de actieve hostingplek; die is bewust v3 geworden. Dat is een verouderde testverwachting, geen verloren v2-backup. Zie WORKFLOW voor huidige checks.

Actuele beslissingen staan hierboven; oudere afwijkende instructies in [PROJECT_HISTORY.md](PROJECT_HISTORY.md) zijn geschiedenis, geen nieuwe opdrachten.
