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
- De rondleiding begint met Command+Enter voor sessie-/takestart, daarna het +/−-voorstel, cue/take kiezen, notes, beoordeling en Comp tool. Alleen concrete toevoegingen zijn selecteerbare voorstellen; algemene indeling, bestaande timers en normale undo krijgen geen losse suggestiestap. Open vragen staan apart.
- De uitleg is gericht aan de collega: vrijblijvende ideeën en korte aanwijzingen om te proberen, zonder eigen bugfixes of ontwerphistorie uit te leggen.
- De rondleiding bevat 10 korte stappen met een highlight, een standaard aangevinkte checkbox voor Claude en Terug/Volgende. Uitvinken blijft mogelijk; expliciete uitvinkkeuzes worden bewaard. Oude gedeeltelijke opt-in-selecties worden eenmalig vervangen door alles aan. Kiezen beïnvloedt alleen de prompt, niet de werking van de demo.
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

- De losse tijdlijnsuggestie is verwijderd; de tijdlijn blijft werken. Bij direct cue kiezen staan ook de basis-sneltoetsen voor cues/takes. Uitklapbare details bij cuekeuze bevatten alle sneltoetsen, inclusief tweecijferige takekeuze met ⌥ + ⌘ vasthouden. Er is geen losse sneltoetsstap.

- De rondleiding is gebundeld in tien stappen: starten, planning, cues/takes, take-notes/Quick notes, maat/kloktijd, sterren/Best/Alt, Comp tool/zoom, maatselectie, score-notes/bewerken en vergelijken/overzicht. Pro Tools staat kort onder optionele uitleg bij kloktijd. De appfuncties blijven behouden. Iedere groep bevat de oorspronkelijke promptonderdelen met vaste IDs; eerder uitgezette onderdelen blijven uitgesloten. Een gedeeltelijke selectie verschijnt als gemengd vinkje; opnieuw aanvinken kiest de hele groep. Tellers en overzicht tellen tien groepen, niet de onderliggende onderdelen.
- De maat-/kloktijdhighlight richt zich eerst op de conceptbediening, ook bij een lege nieuwe take. Een ontbrekend doel mag nooit terugvallen op de Recording/Comp tool-schakelaar.
