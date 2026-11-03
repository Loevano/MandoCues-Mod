# MandoCues — projectkennis

Bijgewerkt: 3 november 2026. Dit is het vaste projectoverzicht voor Floris, Jens en een volgende coding-agent. Het beschrijft de gemaakte keuzes en de huidige demo; het is geen specificatie van een bewezen productie-app. Werk dit bestand bij wanneer een besluit of beperking verandert.

## Correctie v3.2.1 — 3 november 2026

De planning knipperde tussen On schedule en −00:01/oranje na cuewissels. Oorzaak gereproduceerd: sessie- en cue-stopwatch werden elk vanaf hun eigen startmilliseconde afgerond. Tijdelijk telde de sessie een seconde die nog niet van het resterende cuewerk was afgetrokken. Bij herhaald wisselen gingen bovendien fracties verloren. review-v3/schedule-timing.js laat cuewerk dezelfde secondegrenzen als sessiewerk gebruiken; budgetten, voor-/achterstand, kleurdrempels en pauzebeleid blijven behouden. Geen tolerantieband of vertragingsfilter om de fout te maskeren. check_schedule.py controleert de reproductie, herhaald wisselen, beide weergaven, echte oranje/rode/voorstand en pauze/einde/hervatten. De v2-basis blijft ongewijzigd. Publiceer dit op dezelfde actieve Site.

## Online publicatie v3.2 — 3 november 2026

Floris heeft de lokale presentatie expliciet laten publiceren. Deel: https://mandocues-voorstel-v32.gheeneman.chatgpt.site/#recording . Sites bevestigt geslaagde publicatie, hostingversie 1 met presentatie v3.2. De oude Site is vanuit het huidige account niet bereikbaar; daarom is een afzonderlijke Site aangemaakt in ../sites/mando-voorstel-v3-2. Gebruik voortaan de exacte projectidentiteit uit review-v3/publication.json en de .openai/hosting.json in die checkout voor updates; geen nieuwe Site aanmaken. De bestaande oktober-demo is niet vervangen.

Iedereen met de URL kan zonder account openen. noindex/noarchive en robots.txt verzoeken zoekmachines de pagina niet op te nemen; dit is geen toegangsbeveiliging. Alle 68 score-afbeeldingen blijven ingebed. De hostingkopie is exact de opgegeven review-v3/index.html met alleen de robots-metatag toegevoegd. Lokale edits verschijnen pas online na opnieuw publiceren. De vorige lokale-only-instructie is voor deze expliciet gevraagde publicatie opgeheven. Identiteiten, broncommit en deployment staan in publication.json.

## Actuele presentatie v3.2 — 3 november 2026

Open [review-v3/index.html](review-v3/index.html). De bestaande v2-indeling blijft intact. Alleen de laatst gevraagde verfijningen zijn actief: cues herschikken in tijdlijn én lijst met één gedeelde opnamevolgorde; meerdere Best-takes; N om het noteveld te focussen en een tijdanker te zetten; ↓ voor huidige kloktijd en klokje voor het oorspronkelijke schrijfmoment. Notes bewaren writtenAt apart van de bewerkbare clockAt, ook na Enter en tekst wissen.

De rondleiding telt tien suggesties: sessieplan, cues/takes, sterren, noteveld met compacte balk bij scrollen, kloktijd/maat, planning, Comp tool, maten kiezen, score-notes en vergelijken. De Comp-overgang blijft ongenummerd. De kaart is aan de kop versleepbaar; de grote tutorial-selectiebox bij cues is weg. Vinkkeuzes blijven per onderdeel bewaard. Pro Tools staat alleen als kort toekomstidee vermeld. De vraag over verschillende instartmaten staat bij de drie bestaande planning-/klokvragen; geen nieuwe sectie-UI of planningsalgoritme.

Space blijft: eerst sessie, daarna take starten/stoppen, gewone tekst in tekstvelden. Brackets kiezen cues, Option+brackets/1–9 kiezen takes; Option+Command vasthouden voor twee cijfers. Floris bevestigt na de verduidelijkingsvraag: laat de sneltoetsen zoals ze waren. Geen nieuwe Control- of cijferkeuze voor cues.

Bouw: `python3 review-v3/build.py`. Actieve aanvullingen: minimal.js/css, note-times.js, best-takes.js en presentation-tour.js; tekstvragen in questions.json, versienummer in version.json. Gerichte browserchecks: check_minimal.py en check_presentation.py; check_review.py controleert de ongewijzigde v2, backup en herhaalbare build. v3.1 is herstelbaar op commit ec3506e; v2 en afgewezen A/B-proeven blijven afzonderlijk bewaard. Dit is een lokale presentatie, niet opnieuw online gepubliceerd.

## Presentatieversie v3.1 — 3 november 2026

Alleen kleine vervolgwijzigingen: subtiel versienummer in de bovenbalk, aangepaste teksten onder Vragen, Space voor transport en de oude Command+Enter-stap uit de rondleiding. De actuele pagina is [review-v3/index.html](review-v3/index.html); versie staat in review-v3/version.json. Vragen komen uit review-v3/questions.json: kort planningidee op basis van muziekduur/moeilijkheid/werktempo/werkelijke cuetijd, plus vragen over essentiële klokken en een actuele, betrouwbare voor-/achterstand. De drie oude take-timer/New take/vergeten-start-vragen vervallen. Er is geen nieuw planningsalgoritme geïmplementeerd.

De rondleiding begint nu bij cues/takes kiezen en telt negen suggesties. Command+Enter bedient transport niet meer; de eerste Space start alleen de sessie, volgende drukken starten/stoppen takes. De gekozen bestaande indeling, notes, cue-sleepgreep en Comp tool zijn behouden. Nog steeds geen nieuwe klokinstellingen, driepanelenweergave of brede reviewflow. Geen online publicatie uitgevoerd voor deze tekst-/versie-update.

## Laatste besluit — 3 november 2026

Floris wijst de brede v3-herinrichting af. Behoud de vorige A/v2-indeling en neem alleen cuevolgorde herschikken via de bolletjesgreep over; de eerder bevestigde Space-bediening blijft. Geen notes naast de bediening, nieuwe klokinstellingen, drie panelen, planningsproef of andere wijzigingen toevoegen. De bestaande notes moeten behouden blijven. De tutorial voorlopig niet opnieuw vormgeven.

De actuele [lokale pagina](review-v3/index.html) gebruikt alleen `review-v3/minimal.js` en `minimal.css` boven op de ongewijzigde v2-build. De volledige experimentele ronde staat apart in [experiments.html](review-v3/experiments.html) en tag `v3-full-ab-review-20261102`; niet opnieuw als huidige richting aanbieden. Onderstaande reviewbeschrijving van 2 november is geschiedenis waar dit besluit van afwijkt. Er is geen online publicatie gedaan voor deze versmalling.

## Nieuwe reviewronde — 2 november 2026

Floris testte de originele MandoCues-site in een echte opnamesessie. Zijn bevindingen zijn opgeslagen in [de reviewmap](review-v3/bevindingen-opnamesessie-20261102.txt). Op laatste verzoek alle voorstellen samen uitwerken in één A/B-reviewrondleiding; geen definitieve herinrichting of vervanging van de bestaande publicatie zonder review.

De v2-basis (`1bb803e`, UI `93124f8`) is bewaard met tag `before-session-review-v3-20261102` en een geverifieerde bron-ZIP, zelfstandige HTML, hostingbron en volledige Git-bundle in `../Backups/before-session-review-v3-20261102`. De branch `feature/session-review-v3` bevat het nieuwe werk. Het oude herstelpunt uit oktober blijft behouden.

Begin bij [PLAN.md](review-v3/PLAN.md) en [de lokale A/B-reviewrondleiding](review-v3/index.html): acht stappen met werkplek, cue-notes, take-secties, note-maatbereiken, herplannen, cuevolgorde, klokinstellingen en partituur. A/B, overslaan, opmerkingen en een downloadbaar keuzeoverzicht zijn beschikbaar. Deze laag bouwt apart boven op de bestaande demo; de v2-bron, overdracht en hostingkopie zijn niet aangepast. De oude rondleiding wordt pas aangepast aan goedgekeurde keuzes. A/B-klikken bewaren alleen lokale reviewvoorkeuren; het is geen definitieve implementatiegoedkeuring.

**Nieuwe instructie boven de oude Command+Enter-keuze:** voorlopig Space voor handmatige take-start/stop, met gewone spaties in tekstvelden. Uiteindelijk Pro Tools als leidende bron volgen zodat Floris geen tweede take-telling hoeft bij te houden. Bevestigd: de eerste Space start alleen de sessie; daarna start/stop van takes. Pro Tools is uitdrukkelijk uitgesteld; geen verdere integratiewerkzaamheden of vragen in deze ronde.

De overige bevindingen betreffen flexibele herverdeling tot een eindtijd, gewone takes met maatsecties, maatbereiken bij notes via shortcuts, cuevolgorde en instelbare klokken. Deze voorstellen zijn lokaal uitgewerkt als de acht reviewstappen; ze zijn nog niet goedgekeurd of online gepubliceerd. Onderzoek naar [Pro Tools volgen](review-v3/research/PRO_TOOLS.md) scheidt LTC/MTC-projectpositie van record-state en cue/take-identiteit; een kabel alleen bewijst die identiteit niet. Er is geen echte sync gebouwd.

De Sites-opvraag gaf op 2 november `project_not_found`. Hostingversie 2 uit oktober is de laatst bevestigde publicatie, niet vandaag opnieuw geverifieerd. Geen nieuw siteproject aanmaken of oude link vervangen zonder dit op te lossen.

## Snel beginnen

- Online demo: [MandoCues · voorstel van Floris](https://mandocues-voorstel-floris.superfrog5.chatgpt.site).
- Werkende repository: deze map, `Coding/Mando Cues/MandoCues-Mod`.
- Broncode: [prototype/src](prototype/src/). Bewerk de bron; `prototype/dist` wordt gegenereerd.
- Lees ook [AGENTS.md](AGENTS.md), [HUIDIGE_STAND.md](HUIDIGE_STAND.md) en [prototype/README.md](prototype/README.md).
- GitHub: `git@github.com:Loevano/MandoCues-Mod.git`; werkbranch `feature/unified-proposal-tour`.
- Laatst gecontroleerde functionele commit: `93124f8`, planning naar suggestie 6. Daarvoor: `c7b1c87`, vaste posities voor klok en planningsstatus.
- De losse map `Coding/Mando Cues/prototype` is een oudere kopie. Gebruik die niet als actieve bron.

## Doel en mensen

Floris en Jens maken een interactief UI-voorstel voor de collega die MandoCues ontwikkelt. Het ondersteunt een opnamesessie: cues en takes kiezen, planning volgen, notes schrijven en een kniplijst maken op de partituur. Jens heeft onder meer aan de scoreworkflow gewerkt. Behoud die functies en beoordeel veranderingen aan de hand van de gedeelde repository; schrijf wijzigingen niet zonder bewijs aan een specifieke persoon toe.

De oorspronkelijke site blijft het uitgangspunt: herkenbare verhoudingen en bestaande functies behouden, met gerichte toevoegingen. Het materiaal van de oorspronkelijke site is inspectie-HTML en screenshots, geen volledige productiebron. De lokale planner is daarom geen geverifieerde kopie van de echte berekeningen.

## Wat er nu is

Eén werkruimte met **Recording** en **Comp tool**, die dezelfde cues, takes, notes, beoordelingen en lopende take delen. Het eerdere overzicht met vijf prototypes en de A/B-keuzes zijn vervangen door dit ene voorstel.

De demo is zelfstandig HTML/CSS/JavaScript met ingebedde scorebeelden. Er is geen echte audio-opname, gedeelde database, DAW-/filmverbinding, automatische maatvolging of gebouwde Pro Tools-import. Nieuwe demo-invoer verdwijnt bij herladen. Alleen keuzes voor de Claude-prompt worden lokaal in de browser onthouden.

### Vormgeving en tekst

- GUI, tooltips, toegankelijkheidslabels en meldingen zijn Engels. Rondleiding, vragen en uitleg voor de collega mogen Nederlands zijn. Eigen notes en oorspronkelijke cue-/projectnamen niet vertalen.
- Uitleg is kort, suggestief en gericht aan de collega. Geen betuttelende formuleringen of uitleg over interne bugfixes. Zo weinig mogelijk leesruis.
- Grote cuecode en cuenaam links; grote klok met AM/PM rechts. De oorspronkelijke hoofdverhoudingen zijn bewust teruggenomen.
- Recording/Comp tool staat centraal bovenaan. After Party staat eenmaal; de opnamedag is selecteerbaar zonder zichtbaar Session-prefix.
- Recording heeft één scrollgebied en compacte sticky bediening. Geen stapeling van kaders en geneste scrollvensters.
- Sterren, Best en Alt blijven op hun plaats. Takes worden niet groter bij selecteren. Takes staan ingesprongen onder hun cue; de geselecteerde cue is afzonderlijk herkenbaar.
- De echte lopende take blijft onafhankelijk van de take die je bekijkt. Opnemen is zichtbaar via status, duur, globale melding en de later expliciet gevraagde rode schermrand/gloed.

### Recording en planning

- Command+Enter start eerst de sessie zonder een take te maken. Daarna start of stopt dezelfde combinatie een take, ook tijdens noteren. Spatie blijft tekst.
- Start session is bedoeld als blauwe knop, onderscheiden van Record. De rondleiding laat de shortcut bij de eerste stap drie keer kort knipperen, behalve bij verminderde beweging.
- Previous cue, Next cue en Go to cue staan op een vaste rij onder de cuenaam. Overdub blijft bij de opnamebediening; Break en End session zijn zichtbaar.
- Behoud oorspronkelijke cuevelden: muziekduur, Complexity, Planned in minuten, Actual en een handmatig Done-vakje. Beoordelen, selecteren en afvinken zijn onafhankelijke acties.
- Complexity heet Easy / Medium / Hard. Planned bewaart de oorspronkelijke 26 inspectiewaarden als voorbeeld-overrides; Auto of leegmaken herstelt een lokale schatting met gewichten 0,7 / 1 / 1,5. Behoud bij echte implementatie de productieplanner.
- Actual/Worked on cue is cumulatieve werktijd op een cue, inclusief tijd tussen takes en exclusief pauzes. Music length is muziekduur; Planned is gereserveerde werktijd; take-duur geldt voor één take.
- De sessievelden Session length, Prep per cue en Max music blijven zichtbaar. Max music toont ook de ingeplande muziekduur. Planning bevat Finish by en +15/+30/+60 om de eindtijd te verlengen.
- De vier oorspronkelijke sessietijden staan compact onder de klok: Elapsed (working), Remaining, Planned end en Projected end.
- Bij nul alleen On schedule; + betekent voorsprong, − achterstand. Op schema/voorsprong groen; achterstand onder vijf minuten oranje, vanaf vijf minuten rood. Het aantal afgeronde cues staat erbij.
- De compacte klok/planningsbalk reserveert vaste kolommen zodat On schedule en langere plus-/mintijden de omringende bediening niet verplaatsen.
- Takes hebben labels en een verwijderknop. Verwijderen beschermt lopende takes, vraagt bevestiging en hergebruikt geen nummers. Alt heet altijd Alt; alleen het totaal per cue wordt getoond.
- Er zijn twee opnamedagen, waarvan de tweede expliciet demo is. Gegevens zijn per dag gescheiden; dagwisseling tijdens een take is geblokkeerd. Reset vraagt bevestiging, wist takes/werktijden/Done, behoudt cue-notes/planning/chat/scoreweergave en begint de nummering opnieuw bij 1.

### Notes en kloktijden

- Eén notitiepaneel voor de gekozen take; algemene cue-notes bestaan en blijven ingeklapt.
- Enter slaat een note op en zet een volgende klaar. Shift+Enter maakt een nieuwe regel. Quick notes zijn direct zichtbaar.
- Eerste getypte letter legt de echte kloktijd vast. Ook na alle tekst wissen blijft dat tijdanker staan. Het klokje zet de tijd op NU; een volgende note krijgt een nieuw tijdanker.
- Toon AM/PM, bewaar datum/tijd als UTC-instant. Note-tijd en het afzonderlijke start-/stoplog van een take zijn verschillende gegevens.
- Tijd is direct bewerkbaar met Enter. De zwevende scrollbare Bar-lijst werkt vóór en na opslaan identiek: typen plus Enter of een maat kiezen. All betekent de hele take zonder specifiek maatnummer.
- Maatnummers zijn handmatig of bewust op de partituur gekozen. Niet afleiden uit de take-timer; betrouwbare automatische tracking is niet gebouwd.
- Geen aparte Edit-knop voor note-metadata. Een menu mag geen andere inhoud verplaatsen. Book p. staat onder de maat; takekleuren blijven herkenbaar.

### Comp tool en partituur

- De voormalige Cut list heet **Comp tool**. De score vult de werkruimte onder één compacte bovenbalk, met takes/notes links.
- Standaard doorlopend scrollen door alle cuepagina’s. Page layout biedt Single page, Two pages en Continuous scroll; zonder continuous zijn er paginaknoppen.
- Zoom 10–300%, knoppen, Fit width en trackpad-knijpzoom. Zoom en pagina-indeling zijn globaal; ze veranderen niet door cue-, take-, bron- of viewkeuze.
- Takekeuze behoudt de leespositie. Selecties en notes blijven afzonderlijk per take en scorebron bewaard.
- Kniplijstselecties zijn hele maten, standaard voor alle instrumenten. Link instruments staat aan; de bestaande optie om instrumenten los te bekijken/selecteren blijft beschikbaar. Dit is de latere uitwerking van de eerdere wens om de kniplijst steeds voor het geheel te gebruiken.
- Command+slepen voegt toe. Command+rechtsklik en Command+Option+slepen verwijderen. Overlap blijft in beide takes bewaard en wordt zichtbaar met meerdere kleuren/arcering.
- Command+klik kiest losse takes; Shift+klik kiest een reeks; Command+Shift+klik voegt een reeks toe. Dit volgt de gebruikelijke Mac-selectie.
- See other takes toont achtergrondselecties; expliciet vergeleken takes blijven zichtbaar. All takes toont selecties en notes per maat/take.
- Dubbelklik maakt een score-note met de aangeklikte maat en instrumentcontext. Voor alle instrumenten staat tekst boven het systeem bij de maat, binnen de gekozen take. Dit betekent niet automatisch alle takes.
- Notes op de score zijn kale tekst, zonder zwarte hovervlakken. Slepen licht de doelmaat op en werkt de maat/context bij. Geselecteerde notes verwijderen met Delete/Backspace of Delete naast Cancel; Command+Z herstelt inclusief metadata/positie.
- De PDF zelf blijft ongewijzigd. Maatmapping buiten Arrival is een benadering; presenteer dat niet als betrouwbare automatische notatieherkenning.

## Sneltoetsen

| Toets | Actie |
| --- | --- |
| ⌘ Enter | Eerst sessie starten; daarna take starten/stoppen |
| Enter / Shift+Enter | Note opslaan en volgende klaarzetten / nieuwe regel |
| [ en ] | Vorige/volgende cue, zonder wrappen aan de uiteinden |
| ⌥[ en ⌥] | Vorige/volgende take |
| ⌥1 t/m ⌥9 | Het echte take-nummer kiezen |
| ⌥ + ⌘ vasthouden, twee cijfers typen | Bijvoorbeeld 12 voor Take 12; 02 voor Take 2 |
| ⌘+klik / Shift+klik | Losse takes / aaneengesloten reeks vergelijken |
| ⌘+slepen | Maten toevoegen aan kniplijst |
| ⌘+rechtsklik / ⌘⌥+slepen | Maten verwijderen uit kniplijst |
| Delete/Backspace | Geselecteerde score-note verwijderen buiten tekstinvoer |
| ⌘Z | Scorebewerking herstellen |

Option en Alt zijn op Mac dezelfde toets. Het tweecijferige venster bestaat alleen tijdens vasthouden van Option+Command; loslaten annuleert onvolledige invoer. Brackets mogen gedoseerd herhalen; opname/cijfers niet. Bescherm tekstinvoer, modals, slepen en IME. Alle zichtbare shortcuts in eigen uitleg zijn vet en blauw via de gedeelde `shortcutText`-opmaak; eigen notes blijven ongemoeid.

## Rondleiding — actuele volgorde

De rondleiding opent met een keuze om te starten of zelf te kijken. Er zijn tien suggesties, met standaard aangevinkte Claude-keuze; expliciet uitvinken blijft bewaard. Samenvoegen/herordenen mag bestaande keuzes per onderdeel-ID niet verliezen.

1. ⌘ Enter voor start en stop.
2. Cues en takes direct kiezen, met altijd zichtbare sneltoetsen.
3. Notes bij de gekozen take en Quick notes.
4. Kloktijd en maat bij een note, met direct zichtbare Pro Tools-uitleg.
5. Sterren, Best en Alt.
6. Voor- en achterstand met +/− en kleurvoorbeelden — bewust later geplaatst op verzoek van Floris.

Daarna een **ongenummerde overgang** bij de toggle naar Comp tool, met de melding dat dit onderdeel nog niet helemaal is uitgewerkt. Geen extra promptkeuze.

7. Werken vanuit de partituur, inclusief zoom.
8. Maten kiezen voor de kniplijst.
9. Notes op de partituur.
10. Meerdere takes vergelijken en het overzicht.

Highlights scrollen naar hun eigen doel en laten relevante bediening bruikbaar. Een ontbrekend doel mag nooit een willekeurige toggle highlighten. De Claude-prompt is een samenvoeging van vaste geselecteerde onderdelen; de demo voert geen AI-generatie uit.

## Pro Tools — onderzocht voorstel, niet gebouwd

Zie [het onderzoeksdocument](prototype/src/protools-sync.md) voor officiële bronnen en een praktijktest. Kernpunten uit dat onderzoek:

- Pro Tools **File → Export → Session Info as Text** kan bestands-/cliplijsten en track-EDLs leveren. Projecttijdcodes zijn niet vanzelf echte opnamekloktijden.
- BWF kan OriginationDate/OriginationTime bevatten. Original Time Stamp en BWF TimeReference zijn geen garantie op de kloktijd van opnemen. Welke velden de gebruikte Pro Tools-workflow werkelijk vult, moet met originele WAVs worden getest.
- Idee: vergelijk note-kloktijden en ons take-log met gecontroleerde opname-intervallen, na datum/tijdzone/klokcorrectie. Zo kan onze Take 3 aan engineer Take 4 worden gekoppeld zonder te hernummeren.
- Gebruik aanvullende metadata of een engineerlog; verzin ontbrekende tijden niet. Houd rekening met meerdere microfoons, punches, overdubs, loopopnames en notes die na stoppen zijn geschreven. Stel matches voor en laat ze bevestigen.
- Nieuwe demo-takes loggen echte lokale transportmomenten met UTC-datum, tijdzone, cue/sessie en unieke ID. Voorbeeldtakes hebben geen verzonnen opnamelog. Export: PDF → Take sheet → Download take log (JSON).
- Er is geen WAV-import, AI-matching, DAW-bevestiging, sample-nauwkeurige sync of automatische maatvolging geïmplementeerd.

## Bestanden, bouwen en overdracht

| Pad ten opzichte van deze repository | Betekenis |
| --- | --- |
| `prototype/src/unified-app.js` | Gedeelde werkruimte, views en sessiestate |
| `prototype/src/proposal-shell.js` | Appcontext, sessievelden, Chat en export |
| `prototype/src/proposal-tour.json` | Volgorde, tekst, vaste promptonderdelen en IDs |
| `prototype/src/proposal-tour.js` | Welkomstkeuze, highlights, vinkjes en prompt |
| `prototype/src/app.js`, `controls-calm.js`, `extra.js` | Opname-, note- en toetsenbediening |
| `prototype/src/score-*.js`, `production-score.js` | Partituur, lagen, selectie en vergelijking |
| `prototype/src/score-assets/` | Meegeleverde scorebeelden en mappings |
| `prototype/src/style.css` | Vormgeving |
| `prototype/src/feedback.md` | Chronologische feedback; latere correcties gaan voor |
| `prototype/src/rendered-context.md` | Vergelijking met de oorspronkelijke UI |
| `prototype/dist/index.html` | Zelfstandig HTML-bestand met alle benodigde demo-assets |
| `index.html` | Kleine doorverwijzing; niet zelfstandig als losse bijlage sturen |
| `prototype/handoff/` | Documenten/instructies voor broncode-overdracht |

Vanuit de repository:

```sh
python3 -X utf8 prototype/build.py
python3 -X utf8 prototype/check_handoff.py
python3 -X utf8 prototype/package.py
```

Python 3.10+, standaardbibliotheek voor de build. Browsercontroles gebruiken apart Playwright/Chromium of Chrome; zie de README. `check_handoff.py` vergelijkt de uitvoer met een schone geïsoleerde build.

De map `../MandoCues-overdracht-rondleiding` en de gelijknamige ZIP zijn **momentopnamen**, geen automatisch bijgewerkte bron. De viewer-ZIP is `MandoCues-voorstel-van-Floris.zip` in deze repository. `handoff.py --output <nieuw-pad>` maakt een overdracht; bestaande doelen worden bewust niet overschreven. Controleer bestaande manifest-hashes vóór het verversen van een pakket, zodat eigen wijzigingen behouden blijven.

Voor los delen zonder hosting is alleen `prototype/dist/index.html` zelfstandig. Een `file:///...`-link werkt alleen op de eigen computer. Ontvangen kopieën worden niet automatisch bijgewerkt.

## Online publicatie — geverifieerde configuratie

- URL: https://mandocues-voorstel-floris.superfrog5.chatgpt.site
- Publicatie via de beschikbare **Sites**-koppeling, niet via de GitHub-remote.
- Hostingcheckout: `../sites/mando-voorstel-floris` ten opzichte van deze repository.
- Manifest: `../sites/mando-voorstel-floris/.openai/hosting.json`.
- Project-ID: `appgprj_6ad673aeeebc8191a4882963260b87df`. Behoud dit ID; maak voor een update geen nieuwe site.
- Statische directory: `dist`. Deze bevat een kopie van de gegenereerde HTML, met `noindex, nofollow, noarchive` toegevoegd, plus `robots.txt` met Disallow.
- Publieke toegang voor iedereen met de link is door Floris bevestigd, inclusief de meegeleverde partituurpagina’s. Geen account nodig; het is geen wachtwoordbeveiliging of besloten allowlist. Zoekmachine-instructies zijn geen toegangsbeveiliging.
- Laatst bevestigde publicatie: versie 2, planning als suggestie 6. Hostingbroncommit `27b2a85757a5b271a9dd76dd96b03f2520eb6d30`; deployment `appgdep_6ad676442e3c81919f6ac09037da296a`, succesvol.
- Een lokale wijziging, build of GitHub-push werkt de site **niet** automatisch bij. Publiceer een nieuwe versie naar hetzelfde project om de link te behouden.
- Er is geen apart hostingabonnement afgesloten tijdens deze sessie. Kosten, quota en blijvende gratis beschikbaarheid zijn niet onderzocht; beloof geen onbeperkt gratis hosting.

Publicatieroute voor een volgende agent: lees de dan beschikbare Sites-skill; gebruik `get_site` en een verse `create_source_repository_write_credential`, open de bestaande checkout met de source helper, vervang de HTML vanuit de geteste build en behoud noindex/robots. Laat de helper de exacte bron pushen en het archief maken. Daarna `save_site_version` en `deploy_site_version`; wacht op een terminale succesvolle status. Bewaar credentials uitsluitend in sessiegeheugen en geef ze via stdin door, nooit in documentatie, Git, shellargumenten of logoutput.

Lokale uitvoeringsnotitie van 19 oktober: Node was niet op PATH beschikbaar. De runtime onder `Coding/Composition Study/.venv/lib/python3.14/site-packages/playwright/driver/node` werkte; de map moest ook op PATH staan voor onderliggende helpers. De eerste grote Git-upload kreeg HTTP 400; een lokale `http.postBuffer` van 524288000 in alleen de hostingcheckout verholp dat. Controleer de actuele omgeving voordat je deze historische reparatie herhaalt.

## Bekende fouten en controlebewijs

**Nog open uit de review van 19 oktober; niet als opgelost presenteren:**

1. Go to cue kan bij snel invullen/plakken de zoektekst wissen. De vertraagde `toggle`-handler in `unified-app.js` reset het veld; Enter kan daarna de huidige/verkeerde cue kiezen. Het is een timinggevoelige fout, niet bij elke poging zichtbaar.
2. Start session is blauw in Recording, maar nog paars in de compacte Comp tool-balk. De gewenste consistente kleur is niet overal toegepast.
3. De ♪-knop voor score/take-overzicht heeft steeds de tooltip en aria-label Show score PDF, ook wanneer hij juist naar All takes wisselt.

Deze drie punten zijn aan Floris voorgelegd. De daaropvolgende opdrachten betroffen de vaste planningspositie, publicatie en tourvolgorde; die zijn uitgevoerd zonder de drie overige punten stilzwijgend als verholpen te bestempelen.

**Controles uit deze sessie:** brede review met 36 bestaande checks. De cuezoekcontrole faalde incidenteel door bovenstaande echte fout. `check_score_take_scroll.py` stopte op de verouderde eis dat een rij maximaal 60 px hoog is (huidige rijen circa 67 px); met tijdelijk aangepaste grens slaagde het verdere scroll-/selectiegedrag. Werk die testverwachting bewust bij; een falende check is niet automatisch een appfout.

De laatste functionele wijzigingen zijn gericht gecontroleerd: tourvolgorde/highlights, bewaarde promptkeuzes, automatisch scrollen, schone build en handoff. De vaste statusposities zijn in beide views op zes breedtes gecontroleerd. Alle 26 bestaande cuepartituren zijn in de brede review geladen. De eerste publicatie is anoniem in Chrome geopend met werkende rondleiding en score. De tweede publicatie is door Sites als succesvol bevestigd. Dit is geen claim dat elke browser of iedere combinatie foutloos is; Safari/WebKit is niet afzonderlijk gevalideerd.

## Open ontwerpvragen en latere implementatie

- Waarvoor gebruikt de oorspronkelijke workflow iedere timer precies? De vier tijden zijn behouden, maar het productiebeleid moet met de collega worden afgestemd.
- Voorlopig verlengt +15/+30/+60 de geplande eindtijd. Nog te beoordelen: liever alleen verwachte uitloop melden?
- Voorlopig blijft een gestarte sessie tellen bij bekijken van een andere dag. Nog te beoordelen: automatisch pauzeren?
- Pro Tools-kloktijden moeten met originele bestanden en engineer worden gevalideerd vóór automatische matching.
- Echte opslag/samenwerking, betrouwbare score-/maatvolging en bruikbare kniplijstexport vereisen aparte implementatie. De lokale Chat en JSON-export bewijzen geen gedeelde backend.

## Geschiedenis en samenwerken

- Eerdere vijf prototypes en varianten zijn bewaard via tag `before-unified-ui-20261018`, commit `d5f7119`. Het herstelpunt niet veranderen.
- Lokale backup naast de repository: `MandoCues-herstelpunt-20261018-d5f7119.zip`. De eerdere Jens-overdracht is historisch; gebruik voor huidig werk de gedeelde repository.
- Eerst waren scoreworkflow en opnamebediening verdeeld over prototypes. Daarna één voorstel, kortere rondleiding en vaste layout. Laatste wensen gaan voor oude screenshots en feedback.
- Haal wijzigingen van Jens op zonder lokaal werk te overschrijven; controleer branch, diff en remotes. Iedere afzonderlijke wijziging krijgt een geteste eigen commit.
- Floris wil voortgang en concrete uitvoering. Bij routinekeuzes doorgaan; bij wezenlijke onduidelijkheid gericht vragen. In de laatste reviewronde mocht een redelijke voorlopige keuze worden gemaakt met vragen achteraf. Een expliciet verzoek om een fout eerst voor te leggen blijft leidend.
- Projectkennis blijft hier. De centrale `Coding/Knowledge`-map bevat een verwijzing zodat er geen tweede, verouderende kopie van de projectstatus ontstaat.
