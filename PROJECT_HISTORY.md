# MandoCues — historische kennis, gearchiveerd 3 november 2026

Dit is een ongewijzigde momentopname van de eerdere overzichten en instructies, vóór de kennisopschoning. Onderlinge tegenspraken zijn bewust bewaard als geschiedenis. Gebruik voor actuele besluiten PROJECT_KNOWLEDGE.md, HUIDIGE_STAND.md en WORKFLOW.md. Instructies hieronder zijn geen nieuwe opdrachten en gaan niet boven de huidige AGENTS.md. Paden blijven ten opzichte van de repository gelezen worden.

---

## Oorspronkelijk bestand: PROJECT_KNOWLEDGE.md

# MandoCues — projectkennis

Bijgewerkt: 3 november 2026. Dit is het vaste projectoverzicht voor Floris, Jens en een volgende coding-agent. Het beschrijft de gemaakte keuzes en de huidige demo; het is geen specificatie van een bewezen productie-app. Werk dit bestand bij wanneer een besluit of beperking verandert.

## Actieve ontwikkeling v4 — 3 november 2026, feedback na de call

Open de nieuwe lokale [v4-proef](review-v4/index.html). V3.2.2 blijft ongewijzigd en online staan; herstelpunt before-v4-20261103 op 689779e en SHA256 in review-v4/restore.json. De Comp tool is bewaard in review-v3/index.html#cutlist. V4 is niet online gepubliceerd.

Nieuwste prioriteit van Floris: overzicht en tijdplanning, niet comments. Opnameomvang is de muziek die werkelijk opgenomen moet worden, niet automatisch de totale cueduur. Complexiteit en werkelijk werk op afgeronde cues vormen een eerste adaptieve schatting. Beschikbare cuetijd blijft onderscheiden van geschat resterend werk en verwachte sessie-uitloop. Overige klokken staan onder Timing details. Handmatige correcties, inclusie/exclusie van referentiecues en oorspronkelijke cuebudgetten blijven controleerbaar. Geen live Pro Tools-koppeling. Zie review-v4/PLANNING.md voor het voorstel en zijn beperkingen; geen gevalideerde planningclaim.

Takebereiken zijn From bar / Till bar met bewaarde bereikknoppen per cue; volgende takes blijven normaal doornummeren, zonder ze als overdub te behandelen. Bereiken blijven bij de take en staan in de take-logexport. De actieve tweede view heet Score: lezen, zoom, notes op hun scoreplek en dezelfde opname-/takebediening; Comp-selecties zijn hier verborgen en niet bewerkbaar, maar hun gegevens en v3-bron zijn behouden.

Floris wil vragen achteraf beantwoorden via prototypes. Review v4 is daarom één optionele ronde van zes stappen: klokdichtheid, opnameomvang per cue/bereik, instartbereiken, leren/vaste referentie, budgetten herverdelen/vast en Score. A/B verandert de proef direct; losse rekenvoorbeelden schrijven geen nepmetingen. Mijn keuzes geeft een overzicht en JSON-export. Geen automatische introductie of losse vragen tussendoor.

Bouw: python3 review-v4/build.py. Tests: Node check_model.cjs plus check_workspace.py, check_score_ranges.py en check_review.py met de aanwezige Playwright-omgeving. V3-basis en oorspronkelijke score-assets blijven onveranderd. Dagelijkse productie-opslag is niet toegevoegd: metingen/notes zijn demo-state, alleen reviewvoorkeuren blijven lokaal opgeslagen.

## Actieve publicatie op Floris-account — 3 november 2026

De publicatietool is nu gekoppeld aan Floris (florisheemskerk01@gmail.com). Op uitdrukkelijk spoedverzoek is de bestaande Floris-Site bijgewerkt met v3.2.2: https://mandocues-voorstel-floris.superfrog5.chatgpt.site/#recording . Sites bevestigt geslaagde hostingversie 3. Gebruik voortaan review-v3/publication.json en checkout ../sites/mando-voorstel-floris; niet de gheeneman-Site. De automatische welkomdialoog is verwijderd; Rondleiding blijft op verzoek bereikbaar. De knipperfix uit v3.2.1 is meegenomen. De gevraagde −15/−30/−60-planningsknoppen staan nog open: Floris gaf de account-/URL-correctie voorrang. De vorige publicatiegeschiedenis hieronder is historisch.

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


---

## Oorspronkelijk bestand: HUIDIGE_STAND.md

# Nieuwe ontwikkeling — lokale v4

Laatste callfeedback: tijdplanning staat centraal. Open [review-v4/index.html](review-v4/index.html) en gebruik Review v4 om concrete keuzes achter elkaar te bekijken. Details in [review-v4/PLAN.md](review-v4/PLAN.md) en [PLANNING.md](review-v4/PLANNING.md). De lokale v4-proef vervangt de online v3.2.2 nog niet. De oude Comp tool blijft bewaard. Onderstaande v3-/v2-beschrijvingen zijn de eerdere stand.

# Actuele lokale presentatie — v3.2 · 3 november 2026

Open [review-v3/index.html](review-v3/index.html); bron en keuzes staan in [PROJECT_KNOWLEDGE.md](PROJECT_KNOWLEDGE.md) en [review-v3/PLAN.md](review-v3/PLAN.md). De onderstaande beschrijving is de bewaarde v2-basis, geen actuele wijzigingslijst. Voor v3.2 gelden Space voor transport, onafhankelijke Best-takes, gedeeld herschikken in tijdlijn/cuelijst, N en oorspronkelijke/huidige notetijden en de aangepaste tien-stappenrondleiding. De bestaande layout en klokken blijven. De v2-build en oude overdracht zijn niet overschreven; er is niets opnieuw online gepubliceerd.

# Eén voorstel · 19 oktober 2026

De huidige richting vervangt het overzicht met vijf afzonderlijke prototypes.

Eén vaste Recording-indeling: grote cue links, AM/PM-klok rechts. Elapsed (working), Remaining, Planned end en Projected end staan compact onder de klok. Session length, Prep per cue en Max music staan zichtbaar bij de sessiekeuze. Planning bij de titel bevat Finish by en verlengen. De A/B-indelingsschakelaar is verwijderd.

Nieuwe sessie-/cuewerktijd begint op nul. Music length is de muziekduur; Planned is gereserveerde werktijd; Worked on cue/Actual telt het werk op die cue, ook tussen takes en zonder pauze; Take duration is één take. De eerste drie voorbeeldcues hebben takes en notes.

- Eén opnameweergave, gebaseerd op de gekozen 2A: bediening bovenaan en compacte balk bij scrollen. Eén doorlopend scrollgebied, inclusief kop en sessie-instellingen, zonder geneste kaders.
- Bestaande take-labels en take verwijderen zijn actief in beide weergaven; labels staan ook op het take sheet. Lopende takes zijn beschermd en verwijderde nummers worden niet hergebruikt.
- Planned bewaart de 26 inspectiewaarden als voorbeeld-overrides. Auto of leegmaken herstelt een schatting op basis van sessieduur, voorbereiding, muziekduur en Complexity; behoud in productie de echte planner.
- Eén kniplijst met de bestaande wijzigingen: permanent grote doorlopende score met knop-/trackpadzoom en één compacte bovenbalk, takes en notes, All takes, instrument-/zichtbaarheidsinstellingen, note-navigatie en slepen.
- Page layout biedt Single page, Two pages en een aparte Continuous scroll-optie; bij uitgeschakelde scroll zijn paginaknoppen beschikbaar. Zoom gaat van 10–300%.
- De PDF-zoom is één globale werkruimte-instelling: wisselen van cue, take, scorebron of weergave behoudt het percentage en de schaal. Alleen handmatig zoomen of Fit width verandert die.
- Overlap in Comp tool blijft onafhankelijk per take bewaard en verschijnt als meerkleurige arcering met kleurstrepen; achtergrondreferenties blijven ook op overlappende maten zichtbaar.
- Alt heet overal Alt, zonder volgnummer. Het totale aantal alternatieven staat bij de cue en in de scoreweergave.
- Cuegegevens blijven behouden: muziekduur, bewerkbare Complexity en Planned (min), Actual als cumulatieve werktijd en een handmatig Done-vakje. Planned stuurt de cuebegroting en tijdlijn; de bestaande demo-sessieplanner houdt zijn eigen voorbeeldberekening. Afgerond verschijnt ook in de tijdlijn en staat los van geselecteerd/lopend.
- Recording en Comp tool delen cue, take, opname, beoordelingen, notes en concepten. Een lopende take blijft lopen bij wisselen.
- Bij openen: Rondleiding starten of Zelf bekijken. Voorstelnaam en reviewknoppen staan in een aparte compacte balk boven beide weergaven.
- De rondleiding scrolt automatisch naar elk onderdeel. Quick notes staan direct zichtbaar bij de editor.
- De rondleiding begint met Command+Enter voor sessie-/takestart, daarna cue/take kiezen, notes, beoordeling, het +/−-voorstel als suggestie 6 en Comp tool. Alleen concrete toevoegingen zijn selecteerbare voorstellen; algemene indeling, bestaande timers en normale undo krijgen geen losse suggestiestap. Open vragen staan apart.
- De uitleg is gericht aan de collega: vrijblijvende ideeën en korte aanwijzingen om te proberen, zonder eigen bugfixes of ontwerphistorie uit te leggen.
- De rondleiding bevat 10 korte suggesties met een highlight, een standaard aangevinkte checkbox voor Claude en Terug/Volgende. Uitvinken blijft mogelijk; expliciete uitvinkkeuzes worden bewaard. Oude gedeeltelijke opt-in-selecties worden eenmalig vervangen door alles aan. Kiezen beïnvloedt alleen de prompt, niet de werking van de demo.
- De selectie blijft lokaal in de browser bewaard. Kopiëren/downloaden voegt bestaande teksten samen; geen nieuwe generatie. Open vragen staan apart.
- GUI Engels; uitleg en vragen Nederlands. Kloktijden gebruiken AM/PM, ook bij notes; duurvelden blijven minuten/seconden. Command+Enter start eerst de sessie en daarna een take, of stopt de lopende take. Dit werkt ook met focus op de rondleiding. Enter plaatst een note en spatie is tekst.
- Herkenbare appcontext: zijbalk, sessiekeuze, Session length (min), Prep per cue, Max music (min), Add cues, Chat standaard dicht en de PDF-overzichten. De inspectie-HTML is geen volledige appbron; planningscijfers zijn voorbeelddata.
- Hoofdpaneel: grote cue links, klok in AM/PM rechts. Recording/take-duur is duidelijk zichtbaar; een lopende take heeft ook de rode rand, gloed en globale melding uit het oorspronkelijke scherm. Geen signalen door alleen een oudere take te bekijken. On schedule staat groen; − achterstand is onder vijf minuten oranje en vanaf vijf minuten rood; + voorsprong is groen. De vier oorspronkelijke sessietijden staan onder de grote klok, inclusief berekende Projected end. Cuewerktijd staat compact bij Planned. De afzonderlijke cuewerktijdbalk en Session details zijn weg.
- Note-metadata vóór en na Enter gelijk: zwevende scrollbare Bar-lijst met All voor de hele take, typen plus Enter; echte kloktijd hh:mm:ss AM/PM aanklikken en Enter. Het klokje vult de huidige kloktijd in. De eerste letter legt de tijd vast; alle tekst wissen laat deze staan. Alleen het klokje zet de tijd op nu. De datum blijft bewaard als UTC-instant. Geen relatieve tijdcodes bij notes en geen DAW-sync gebouwd.
- Score-notes: dubbelklik neemt de maat op die plek over, ook vlak boven de balk. Slepen toont de doelmaat en past de maat-/instrumentcontext aan. Klik een bestaande score-note en verwijder met ⌫ of Delete naast Cancel; ⌘Z herstelt hem. Tekstvelden houden gewone tekstbewerking.
- Maatnummers bij notes zijn handmatig: invullen of bewust in de partituur kiezen. Geen Follow bar of afleiding uit de take-timer.

## Sneltoetsen

In beide weergaven: [ vorige cue, ] volgende cue; Alt+[ vorige take, Alt+] volgende take. Alt+1 t/m 9 kiest het echte take-nummer. Voor Take 12: houd Option (Alt)+Command vast en typ 1 en 2. Het venster staat alleen open tijdens vasthouden en sluit na de tweede digit of loslaten van één modifier. Onvolledige invoer vervalt; geen takekeuze na loslaten. Voor Take 2 kan ook 0 en 2. Extra cijfers onder dezelfde vastgehouden combinatie voeren geen nieuwe keuze uit. Brackets ingedrukt houden herhaalt navigatie en versnelt na kort vasthouden. Bij de eerste en laatste cue stopt navigatie; brackets en cuepijlen springen niet naar de andere kant. De eerdere keuze op cuevolgorde vervalt; de open vraag hierover is beantwoord. Takekeuze verandert de bewerkingslaag, nooit de lopende opname.

## Herstelpunt

De versie vóór deze samenvoeging is commit `d5f7119`, Git-tag `before-unified-ui-20261018`. Dezelfde tag staat op GitHub. Je kunt die versie apart bekijken zonder het huidige werk te overschrijven:

```sh
git worktree add ../MandoCues-vorige-versie before-unified-ui-20261018
```

Daarna open je `../MandoCues-vorige-versie/index.html`. Er is ook een lokale ZIP: `MandoCues-herstelpunt-20261018-d5f7119.zip` naast de gedeelde werkkopie.

De demo is geen recorder en heeft geen echte DAW-/filmtijd of live score following. Maatvakken buiten Arrival zijn benaderingen. Nieuwe demo-invoer verdwijnt bij herladen. Echte gedeelde sessie-opslag en kniplijstexport zijn geen onderdeel van dit voorstel.

## Broncode en controles

- `prototype/src/unified-app.js`: de gedeelde werkruimte; hergebruikt bestaande opname- en scorecomponenten.
- `prototype/src/proposal-tour.json`: stappen, korte uitleg en vaste promptonderdelen. Er is één vaste hoofdpaneelindeling, zonder A/B-keuze.
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

Shift+klik in Comp tool kiest een reeks takes vanaf het laatste klikanker; Command+klik kiest losse takes. Command+Shift+klik voegt een reeks toe. De aangeklikte take wordt de bewerkbare laag.

Auto-planning: Planned bevat de originele 26 inspectiewaarden als voorbeeld-overrides. Auto kiezen of leegmaken schakelt terug naar een schatting die reageert op Complexity, sessieduur en voorbereiding. De lokale formule volgt de zichtbare tooltip en is niet de geverifieerde productieplanner.

Take-labels en take verwijderen zijn behouden in Recording, Comp tool en All takes. Labels staan ook op het take sheet. Verwijderen vraagt bevestiging, beschermt een lopende take en hergebruikt geen verwijderd nummer. De bronvergelijking in `prototype/src/rendered-context.md` vermeldt wat is behouden, bewust gewijzigd en niet nagebouwd.

Recording met opname-icoon en After Party eenmaal; gecentreerde viewkeuze. De dagkeuze toont één bekende dag en een expliciete tweede demosessie. Takes, notes, cues, instellingen en chat zijn per dag gescheiden. Dagwisseling tijdens een take is geblokkeerd; een gestarte sessie telt tijdens bekijken van een andere dag voorlopig door. Dit is nog geen serveropslag.

Finish by blijft vaststaan. +15/+30/+60 verlengt het geplande einde; dit is voorlopig gekozen boven alleen een uitloopvoorspelling. Session length (min) toont de uren ernaast. Het doel van de oorspronkelijke extra klokken blijft onder Vragen staan; het is geen losse tutorialsuggestie.

Nog te beoordelen door Floris:
1. Uitloopknoppen verlengen het geplande einde of melden alleen verwachte extra werktijd? Voorlopig verlengen.
2. Sessie laten doortellen bij bekijken van een andere dag of automatisch pauzeren? Voorlopig doortellen; tijdens een take is wisselen geblokkeerd.

## Takekoppeling met Pro Tools (voorstel)

De rondleiding heeft een korte stap na note-kloktijd: onze Take 3 kan bij de engineer Take 4 heten. Een latere koppeling gebruikt gecontroleerde opnamekloktijden en handmatige bevestiging; geen hernummering. Pro Tools Original Time Stamp is projectpositie, geen gegarandeerde kloktijd. Zie `prototype/src/protools-sync.md` (gegenereerd als `Pro-Tools-takekoppeling.md`) voor de officiële bronnen en de test met originele WAVs.

Nieuwe takes/overdubs bewaren aparte UTC-start-/stopinstants en tijdzone/sessie/cue/log-ID. Dit zijn onze lokale transportmomenten, geen DAW-bevestigingen. PDF → Take sheet → Download take log (JSON) exporteert ze met note-kloktijden. Voorbeeldtakes hebben geen opnamelog; niets verzinnen. Invoer verdwijnt nog bij herladen. Er is geen import, matching of DAW-verbinding gebouwd. Productie vraagt duurzame logs en een gecontroleerde engineerbron.

- Go to cue staat naast Next cue als bestaande bediening. De zwevende lijst is doorzoekbaar op cuecode/titel en verschuift de bediening niet. Kiezen gebruikt dezelfde cue-state en blokkeert tijdens een lopende take; bestaande notes/concepten blijven behouden.

## Bevestigd na vergelijking met het origineel

- Gebruikte muziekduur naast Max music (som van de huidige cuelijst; nu 53:14), met markering boven de limiet. Easy/Medium/Hard zijn de oorspronkelijke Complexity-namen. Het aantal afgeronde cues staat compact in het planningsvlak.
- Reset naast End session vraagt bevestiging voor de huidige opnamedag en is tijdens een take geblokkeerd. Wis takes, take-notes, selecties, cue-afvinkingen en werktijden; behoud algemene cue-notes, planning, chat, scorebron/leespositie en globale zoom. Nummering begint na deze expliciete reset opnieuw bij 1; losse takes verwijderen blijft nummers niet hergebruiken.
- Algemene cue-notes blijven ingeklapt; geen nieuwe optionele tutorialstappen voor deze bestaande functies.

De eerder openstaande browsercontroles voor reset, muziekduur, Complexity, Done en Planning zijn alsnog geslaagd. AM/PM, Go to cue, hoofdbediening en de rondleiding waren al in de browser gecontroleerd.

## Laatste review: vaste indeling en gerichte rondleiding

- Geen indelingskeuze bovenaan. De drie sessievelden blijven zichtbaar naast Add cues / Chat / PDF; Planning bevat alleen eindtijd en verlengen.
- De vier oorspronkelijke tijden staan compact onder de grote klok, zonder afzonderlijke vakken. Alleen On schedule bij nul; anders één getal met + of −. Onder vijf minuten achterstand oranje, vanaf vijf rood. Het afgeronde-cuetotaal blijft zichtbaar.
- Take-duur staat alleen zichtbaar tijdens opnemen, op één vaste plek naast Recording en het take-nummer. Geen stilstaande duur naast Overdub. De opnameknop en omliggende bediening behouden hun positie bij sessie-/takestart en stop.
- Rondleiding: 10 gebundelde voorstellen, begint met ⌘ Enter. De algemene indelingsstap is weg; planning gaat specifiek over +/− en de kleurgrenzen. Undo blijft werken, zonder eigen optionele stap.

- Start session heeft een blauwe knop, onderscheiden van Record in rood. De eerste rondleidingsstap laat alleen de ⌘ Enter-hint drie keer kort knipperen; niet bij verminderde beweging, na sessiestart of buiten die stap.

- De losse tijdlijnsuggestie is verwijderd; de tijdlijn blijft werken. Bij direct cue kiezen staan ook de basis-sneltoetsen voor cues/takes. Bij cuekeuze staan alle sneltoetsen direct zichtbaar, inclusief tweecijferige takekeuze met ⌥ + ⌘ vasthouden; dit is niet inklapbaar. Er is geen losse sneltoetsstap.

- De rondleiding is gebundeld in tien suggesties: starten, cues/takes, take-notes/Quick notes, maat/kloktijd, sterren/Best/Alt, planning, Comp tool/zoom, maatselectie, score-notes/bewerken en vergelijken/overzicht. Pro Tools staat direct zichtbaar bij kloktijd, zonder uitklappen. De appfuncties blijven behouden. Iedere groep bevat de oorspronkelijke promptonderdelen met vaste IDs; eerder uitgezette onderdelen blijven uitgesloten. Een gedeeltelijke selectie verschijnt als gemengd vinkje; opnieuw aanvinken kiest de hele groep. Tellers en overzicht tellen tien groepen, niet de onderliggende onderdelen.
- De maat-/kloktijdhighlight richt zich eerst op de conceptbediening, ook bij een lege nieuwe take. Een ontbrekend doel mag nooit terugvallen op de Recording/Comp tool-schakelaar.

- De zichtbare Pro Tools-uitleg draait om notes via hun kloktijd aan de juiste engineer-opname koppelen, eventueel met AI. Session Info as Text levert clip-/projecttijden; echte opnametijden moeten aanvullend uit gecontroleerde metadata of een engineerlog komen. Dit is een toekomstvoorstel, geen gebouwde import of AI-koppeling.

- Alle zichtbare sneltoetsen in tutorialtitels, uitleg, promptvoorvertoning en bestaande GUI-hints zijn vet en blauw. Gebruik de gedeelde shortcutText-opmaak voor eigen uitleg; laat eigen notes en cue-/projectnamen ongemoeid. Lichte stopknoppen gebruiken donkerblauw voor contrast.

- Tussen suggestie 6 en 7 staat een ongenummerde aanwijzing bij de Recording/Comp tool-toggle: Comp tool is nog niet helemaal uitgewerkt. Klikken op Comp tool of Verder vervolgt bij de scorestap. Dit is geen extra promptkeuze; tien suggesties en hun bestaande keuzes blijven behouden.

- De compacte opnamebalk reserveert vaste kolommen voor klok en planningsstatus; On schedule, plus-/mintijden en langere achterstand verplaatsen de klok, take-duur en knoppen niet. Gecontroleerd in beide views op zes schermbreedtes.


---

## Oorspronkelijk bestand: AGENTS.md

# Werken aan deze overdracht

- Maak voor iedere afzonderlijke wijziging een eigen Git-commit. Bundel geen onafhankelijke wijzigingen in één commit; valideer elke wijziging voordat je die commit.
- Lees `HUIDIGE_STAND.md` voor de huidige keuzes. `prototype/src/feedback.md` is chronologische geschiedenis; latere correcties gaan voor eerdere wensen.
- Dit is één lokale voorstelpagina met Recording, Comp tool en een rondleiding, geen werkende opname-app. Behoud het karakter van vrijblijvende voorstellen en de bestaande vormgeving. Verander geen externe app, originele scoreboeken of ander project.
- Alle daadwerkelijke GUI-tekst is Engels, inclusief hints, toegankelijkheidslabels en meldingen. Vragen, prompts en toelichting buiten de demo mogen Nederlands blijven. Vertaal geen oorspronkelijke cue-/projectnamen of zelf getypte notes.
- Bewerk bronbestanden onder `prototype/src/`; `prototype/dist/` wordt gegenereerd. Bouw na wijzigingen met `python3 -X utf8 prototype/build.py` vanuit deze map.
- `build.py`, `score_fixture.py`, `production_score.py` en `score_overview.py` gebruiken alleen de Python-standaardbibliotheek. Alle benodigde score-assets zitten in `prototype/src/score-assets/`. Externe projecten en originele scoreboeken zijn geen buildvereiste.
- De rondleiding begint met de suggestie voor sessiestart via Command+Enter, daarna cue/take kiezen, notes, beoordeling en kniplijst. Sneltoetsen staan bij cuekeuze altijd zichtbaar; Pro Tools-uitleg staat ook direct zichtbaar binnen de maat-/kloktijdstap; score-instellingen en All takes hebben geen losse stap. Introductie vanuit Floris kort formuleren; timer-/workflowvragen blijven onder Vragen. Behoud bestaande promptkeuzes per suggestie-ID bij herordenen.
- Houd de rondleiding kort: alleen wat een suggestie toevoegt en hoe je die probeert. Normale kwaliteitseisen en eigen bugfixes, zoals niet-verspringende knoppen, horen niet in de uitleg voor de collega. Technische details blijven in de implementatieprompt. Beschrijf concreet wat je aanklikt en wat je dan ziet. Leg take-notes en algemene cue-notes niet in één uitleg door elkaar uit.
- Behoud vaste posities voor sterren, Best en Alt. De knop heet altijd Alt, zonder volgnummer; toon alleen het totale aantal alternatieven per cue, ook nul. Een gekozen take mag geen verspringende knoppen of onverwacht groter wordende rijen veroorzaken.
- Enter plaatst een note; Shift+Enter geeft een nieuwe regel. Spatie is gewone tekst. Op Mac start Command+Enter eerst de sessie zonder een take te maken. Tijdens de sessie start Command+Enter een nieuwe take als er geen loopt en stopt de lopende take als die er wel is, ook tijdens typen. Negeer key-repeat en IME-compositie; gewoon Enter plaatst een note. Stop hoort bij de opnamebediening, niet naast Add/Delete in de note-editor.
- Concepten gebruiken vóór Enter dezelfde maat-/kloktijdbediening als geplaatste notes; Enter in metadata plaatst geen note. Notes gebruiken werkelijke kloktijd hh:mm:ss AM/PM, vastgelegd bij de eerste letter. Bewaar de datum als UTC-instant; toon lokale tijd met AM/PM. Geen take-/sessie-/filmtijdcode bij notes. Het klokje vult Date.now() in, ook voor een oudere take, vóór en na Enter. Enter maakt een nieuw concept met nieuwe kloktijd klaar. Tijd is direct bewerkbaar met Enter; Escape annuleert. Bar opent een zwevende scrolllijst met All en maatnummers, typen plus Enter kiest direct. Notes hebben geen Edit-knop; Delete blijft apart. Behoud kloktijd en datum bij tekstbewerking, slepen en undo/redo. Dit bewijst geen DAW-synchronisatie.
- Maatnummers bij notes zijn voorlopig handmatig: invullen of bewust in de partituur kiezen. Geen gesimuleerd maatvolgen, Follow bar of maat afleiden uit de take-timer. Automatisering vereist later een betrouwbare koppeling met de uitvoering.
- In Recording en Comp tool: [ vorige cue, ] volgende cue; Alt+[ vorige take, Alt+] volgende take; Alt+1 t/m 9 kiest het echte gewone take-nummer. Option (Alt)+Command vasthouden toont invoer voor precies twee cijfers (12, 34, …); loslaten van één modifier annuleert onvolledige invoer. Na de tweede digit kies je de bestaande take. Geen zichtbare Escape-instructie of invoer na loslaten. Geen oude cijferkeuze op cuevolgorde. Bescherm tekstinvoer, modale vensters, slepen en IME. Cue-navigatie stopt aan het begin/einde van de lijst, zonder terug te springen naar de andere kant. Alleen brackets mogen gedoseerd herhalen en versnellen bij ingedrukt houden; cijfers en opnamecommando’s herhalen niet. Takekeuze verandert nooit de lopende take.
- Behoud per cue de oorspronkelijke velden: muziekduur, Complexity, Planned in minuten, Actual en een handmatig afvinkvakje voor afgerond. Complexity/Planned zijn bewerkbaar. Planned bewaart de 26 inspectiewaarden als voorbeeld-overrides; Auto of een leeg invoerveld herstelt een automatische schatting op basis van sessieduur, voorbereiding en gewogen muziekduur. Dit is een lokale benadering van de zichtbare tooltip; behoud de echte productieplanner. Planned wordt gedeeld met de cueplanning en tijdlijn. Actual toont cumulatieve werktijd per cue, inclusief tijd tussen takes en zonder pauzetijd; wisselen bewaart de tijd. Afvinken verandert geen cue-/takekeuze of transport en kan ongedaan worden gemaakt door uitvinken. Houd selected cue en completed cue visueel onderscheiden. Dit is bestaande functionaliteit, geen extra suggestie.
- Geselecteerde take en lopende take zijn onafhankelijk. Een nieuwe take heeft eigen lege notes en kniplijstselectie.
- Kniplijstselecties betreffen hele maten. Overlap blijft per take bewaard en wordt met meerdere kleuren/arcering zichtbaar, inclusief zichtbare achtergrondtakes. Toevoegen/verwijderen of undo in één take wijzigt nooit een andere. Gebruik duidelijk kleurcontrast zonder de gedrukte muziek te bedekken. Link instruments staat standaard aan (alle instrumenten samen); uit selecteert per instrument. See other takes toont/verbergt alleen achtergrondselecties; expliciet vergeleken takes blijven zichtbaar. Cmd/Ctrl+links klikken/slepen voegt toe; rechts verwijdert. Gewone klik kiest één take; Command+klik kiest losse takes, Shift+klik een aaneengesloten reeks vanaf het laatste klikanker. Command+Shift+klik voegt een reeks toe. Behoud het anker bij Shift; gewone/Command-klik zet het opnieuw. Dubbelklik op de score maakt een note.
- De partituur toont standaard alle cuepagina’s doorlopend en scrollt onafhankelijk van takes/notes. Via Page layout kan één of twee pagina’s per rij worden gekozen en Continuous scroll uit; dan zijn er paginaknoppen. Zoom loopt van 10–300%. Pagina-indeling en zoom blijven globaal over cues, takes en weergaven. De kniplijst is permanent vergroot, met één compacte bovenbalk voor viewkeuze en opnamebediening. Zoom in/uit, trackpad-knijpzoom en Fit width blijven beschikbaar. Zoom is globaal voor de werkruimte en blijft gelijk bij wisselen van cue, take, scorebron en weergave; sla geen zoomstand per take op. Alleen zoomen of Fit width verandert die instelling. Zoom schaalt score en annotatielagen samen. Behoud leespositie bij takekeuze en zet lange gebruiksuitleg in de rondleiding.
- De voorstelnaam en reviewknoppen staan compact bovenaan in een eigen balk, buiten de voorgestelde GUI. Houd de zijbalk en bestaande sessiecontext herkenbaar; Chat standaard dicht. Het inspectiebestand is gerenderde HTML, geen volledige appbron.
- Score-notes zijn kale tekst op de score. Instrumentgebonden tekst hoort bij dat instrument; All instruments staat boven de bovenste balk bij die maat, binnen de gekozen take. Bepaal bij plaatsen en slepen de maat en instrumentcontext uit de bestaande scoremapping, ook vlak boven maatvakken. Laat de doelmaat bij slepen subtiel oplichten. Delete/Backspace verwijdert een geselecteerde note buiten tekstvelden; naast Cancel staat ook Delete bij bestaande notes. Command+Z herstelt verwijderen en verplaatsen inclusief metadata. De PDF zelf blijft ongewijzigd.
- Gebruik de oorspronkelijke Recording-verhoudingen: één hoofdvak met een grote cue links, grote klok in AM/PM rechts en een groen/oranje/rood planningsvlak. Toon On schedule bij nul, − voor achterstand, + voor voorsprong; onder vijf minuten achterstand oranje, vanaf vijf minuten rood. Bewaar Previous cue/Next cue en Go to cue op een vaste rij onder de cuenaam, Overdub bij opnemen en Break/End session zichtbaar. Neem tijdens een werkelijk lopende take de oorspronkelijke rode schermrand, subtiele gloed en globale Recording-melding over; stop verwijdert die meteen. Houd lopende en geselecteerde take onafhankelijk. Cuewerktijd staat compact bij Planned, zonder eigen balk. Nieuwe sessie- en cuewerktijden beginnen op nul, geen voorbeeld-offsets. De demo schat resterend cuewerk op basis van onvoltooide cuetijd en werkelijke werktijd; behoud productiebeleid bij implementatie. De hoofdpagina toont klok, voor/achter, cuewerktijd en live take-duur, plus Elapsed (working), Remaining, Planned end en Projected end compact onder de klok. De drie sessie-invulvelden staan zichtbaar bovenaan; Planning bevat de eindtijd en verlengen. Finish by is een vaste geplande eindtijd; Projected end wordt berekend. +15/+30/+60 verlengt voorlopig de geplande eindtijd.
- Recording heeft één scrollgebied voor kop, bediening, tijdlijn, cues en notes; geen geneste scroll of kaderstapeling. Het ene herkenbare hoofdvak behoudt zijn oorspronkelijke afgeronde, gekleurde rand. De compacte opnamebalk blijft sticky. Er is één vaste indeling zonder A/B-schakelaar. De drie sessievelden staan zichtbaar bij de sessiekeuze. Behoud Recording met opname-icoon, After Party eenmaal, gecentreerde Recording/Comp tool-schakelaar en dagkeuze zonder zichtbaar Session-prefix. Recording en Comp tool delen state. Opnamedagen bewaren eigen takes, notes, planning, cues en chat; een tweede dag is expliciet demo. Dagwisseling tijdens een take is geblokkeerd. Een al gestarte sessie blijft voorlopig doortellen als een andere dag wordt bekeken. Zoom/pagina-indeling blijven globaal. Rondleiding/prompt staan in proposal-tour.json en proposal-tour.js.
- De vorige vijf prototypes blijven herstelbaar via tag `before-unified-ui-20261018`; verander dat herstelpunt niet.
- Geen nieuw prototype 06: montage/export en de vraag over take-timers zijn toelichting of vragen, geen aparte demo.
- Controleer na wijzigingen gericht de betrokken flows. `python3 -X utf8 prototype/check_handoff.py` verifieert de pakketinhoud en een schone rebuild. Browsercontroles staan beschreven in `prototype/README.md`.
- Publiceren, uploads en het aanmaken van een gedeelde repository horen niet bij het overnemen van dit pakket.

- Behoud take-labels en de expliciete verwijderknop in Recording en Comp tool/All takes; dezelfde state en export. Verwijderen vraagt bevestiging voor notes en selecties, beschermt lopende takes en verandert andere takes of cuewerktijd niet. Hernummer geen takes en hergebruik verwijderde take-/overdubnummers niet. De inspectie toont ook sessiereset en tab-herordening; niet nagebouwd betekent niet verwijderen uit de echte app. Zie prototype/src/rendered-context.md.

- In deze reviewronde kiest Codex zelf een redelijke voorlopige optie en voert het werk uit; vragen achteraf als korte lijst met de gekozen optie. Grote uiterlijke alternatieven mogen A/B ter beoordeling blijven. Bewaar onbeantwoorde klok-/workflowvragen onder Vragen. De rondleiding bevat alleen concrete voorstellen, vanuit Floris, zonder lange tekst of stellige claims.

- Take-sync is een toekomstvoorstel: koppel onze take-ID aan engineerbestand/clip na controle, zonder hernummeren of audio te wijzigen. Original Time Stamp/BWF TimeReference is geen gegarandeerde kloktijd. Raadpleeg `prototype/src/protools-sync.md`. Bewaar `takeLog` met echte lokale start-/stopinstants, tijdzone, sessie/cue en unieke ID; geen verzonnen log voor voorbeeldtakes. Note-tijdbewerking en takekeuze mogen dit log niet wijzigen. JSON-export via Take sheet is een demo-momentopname; geen persistente opslag of DAW-bevestiging.

- Go to cue staat naast Next cue als bestaande bediening. De zwevende lijst is doorzoekbaar op cuecode/titel en verschuift de bediening niet. Kiezen gebruikt dezelfde cue-state en blokkeert tijdens een lopende take; bestaande notes/concepten blijven behouden.

- Bevestigd: behoud originele Complexity-labels Easy/Medium/Hard en de 0,7/1/1,5-gewichten. Toon gebruikte muziekduur compact naast Max music en afgeronde-cuetotaal in het planningsvlak. Cue-notes blijven ingeklapt. Reset takes/tijden is per opnamedag, met bevestiging en geblokkeerd tijdens een take. Behoud cue-notes, planning, chat en scoreweergave; wis takegegevens/werktijden/aftekenen. Deze expliciete reset begint nummering opnieuw bij 1; individuele takeverwijdering niet.

- Take-duur is alleen zichtbaar tijdens een lopende take, op één vaste plek naast opnamestatus/take-nummer. Geen stilstaande Take duration 00:00 naast Overdub. Reserveer de statusruimte en houd knopbreedte/hoogte vast zodat starten/stoppen niets verplaatst. Toon bij nul alleen On schedule, geen tweede 00:00. De rondleiding heeft 10 gebundelde voorstellen; geen algemene indelingsstap of losse undo-suggestie.

- Start session heeft een blauwe knop, onderscheiden van Record in rood. De eerste rondleidingsstap laat alleen de ⌘ Enter-hint drie keer kort knipperen; niet bij verminderde beweging, na sessiestart of buiten die stap.

- De losse tijdlijnsuggestie is verwijderd; de tijdlijn blijft werken. Bij direct cue kiezen staan ook de basis-sneltoetsen voor cues/takes. Bij cuekeuze staan alle sneltoetsen direct zichtbaar, inclusief tweecijferige takekeuze met ⌥ + ⌘ vasthouden; dit is niet inklapbaar. Er is geen losse sneltoetsstap.

- De rondleiding is gebundeld in tien suggesties: starten, cues/takes, take-notes/Quick notes, maat/kloktijd, sterren/Best/Alt, planning, Comp tool/zoom, maatselectie, score-notes/bewerken en vergelijken/overzicht. Pro Tools staat direct zichtbaar bij kloktijd, zonder uitklappen. De appfuncties blijven behouden. Iedere groep bevat de oorspronkelijke promptonderdelen met vaste IDs; eerder uitgezette onderdelen blijven uitgesloten. Een gedeeltelijke selectie verschijnt als gemengd vinkje; opnieuw aanvinken kiest de hele groep. Tellers en overzicht tellen tien groepen, niet de onderliggende onderdelen.
- De maat-/kloktijdhighlight richt zich eerst op de conceptbediening, ook bij een lege nieuwe take. Een ontbrekend doel mag nooit terugvallen op de Recording/Comp tool-schakelaar.

- Alle zichtbare sneltoetsen in tutorialtitels, uitleg, promptvoorvertoning en bestaande GUI-hints zijn vet en blauw. Gebruik de gedeelde shortcutText-opmaak voor eigen uitleg; laat eigen notes en cue-/projectnamen ongemoeid. Lichte stopknoppen gebruiken donkerblauw voor contrast.

- Tussen suggestie 6 en 7 staat een ongenummerde aanwijzing bij de Recording/Comp tool-toggle: Comp tool is nog niet helemaal uitgewerkt. Klikken op Comp tool of Verder vervolgt bij de scorestap. Dit is geen extra promptkeuze; tien suggesties en hun bestaande keuzes blijven behouden.


---

## Oorspronkelijk bestand: README.md

# MandoCues · voorstel van Floris

**Open [index.html](index.html)** voor één werkruimte met **Recording** en **Cut list**. Bij openen kies je **Rondleiding starten** of **Zelf bekijken**. De rondleiding toont per suggestie een korte uitleg en een checkbox voor je Claude-prompt. Alleen aangevinkte tekstonderdelen gaan mee.

Recording gebruikt bediening bovenaan en een compacte balk bij scrollen. Cut list behoudt de bestaande scorebediening en All takes. Beide delen cues, takes, notes en beoordelingen. De GUI is Engels; rondleiding en vragen zijn Nederlands. Alles blijft vrijblijvend.

Voor Codex: [CODEX_STARTPROMPT.txt](CODEX_STARTPROMPT.txt), [AGENTS.md](AGENTS.md) en [HUIDIGE_STAND.md](HUIDIGE_STAND.md).

```sh
python3 -X utf8 prototype/build.py
python3 -X utf8 prototype/check_handoff.py
```

Python 3.10+, zonder extra pakketten voor de build. Alle score-assets zitten erbij. Zie [prototype/README.md](prototype/README.md) voor browsercontroles.

Werk in `prototype/src/`, bouw `dist/` opnieuw en commit bron en uitvoer samen. Haal vóór wijzigingen de laatste commits op en werk op een eigen branch. Browser-notes worden niet tussen computers gedeeld en verdwijnen bij herladen.

De vorige versie is bewaard als Git-tag `before-unified-ui-20261018` (commit `d5f7119`). Herstelinstructies staan in HUIDIGE_STAND.md. De oorspronkelijke app en scoreboeken worden niet gewijzigd; de demo neemt geen audio op.


---

## Oorspronkelijk bestand: CODEX_STARTPROMPT.txt

Dit is Floris’ MandoCues-voorstel: één werkruimte met Recording, Cut list en een rondleiding.

Lees AGENTS.md, HUIDIGE_STAND.md en prototype/README.md.
Controleer met python3 -X utf8 prototype/check_handoff.py dat broncode en build overeenkomen.
Open index.html of prototype/dist/index.html om de pagina te bekijken.

De vastgelegde keuzes:
- Opnameweergave: 2A, bediening bovenaan en compacte balk bij scrollen.
- Kniplijst: de bestaande scorebediening behouden, inclusief All takes en instellingen.
- Beide weergaven delen cues, takes, notes, beoordelingen en opname-state.
- Bij openen een keuze: Rondleiding starten of Zelf bekijken.
- Eén korte uitleg en highlight per suggestie; een checkbox kiest die tekst voor Claude.
- Alleen gekozen vaste promptteksten samenvoegen. Vragen blijven vragen.
- De oude vijf prototypes staan onder Git-tag before-unified-ui-20261018.

Werk in prototype/src/ en bouw opnieuw met prototype/build.py.
Alle echte GUI-tekst is Engels; rondleiding en toelichting blijven Nederlands.
Leg onduidelijke ontwerpkeuzes aan mij voor; verzin geen nieuwe A/B-demos.
Mijn code en ontwerpkeuzes blijven leidend. Niets publiceren of op SoundVibeHQ wijzigen zonder mijn opdracht.
Controleer nu alleen of de overdracht werkt en wacht daarna op mijn concrete wijzigingsvraag.


