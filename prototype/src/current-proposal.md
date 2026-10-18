# Eén voorstel · 18 oktober 2026

De huidige richting vervangt het overzicht met vijf afzonderlijke prototypes.

- Eén opnameweergave, gebaseerd op de gekozen 2A: bediening bovenaan en compacte balk bij scrollen. Eén doorlopend scrollgebied, inclusief kop en sessie-instellingen, zonder geneste kaders.
- Eén kniplijst met de bestaande wijzigingen: permanent grote doorlopende score met knop-/trackpadzoom en één compacte bovenbalk, takes en notes, All takes, instrument-/zichtbaarheidsinstellingen, note-navigatie en slepen.
- De PDF-zoom is één globale werkruimte-instelling: wisselen van cue, take, scorebron of weergave behoudt het percentage en de schaal. Alleen handmatig zoomen of Fit width verandert die.
- Recording en Cut list delen cue, take, opname, beoordelingen, notes en concepten. Een lopende take blijft lopen bij wisselen.
- Bij openen: Rondleiding starten of Zelf bekijken. Voorstelnaam en reviewknoppen staan in een aparte compacte balk boven beide weergaven.
- De rondleiding scrolt automatisch naar elk onderdeel. Quick notes staan direct zichtbaar bij de editor.
- De rondleiding volgt de workflow: hoofdpaneel → sessiestart en planning → cue en take kiezen → notes → beoordeling → sneltoetsen → partituur en kniplijst → vergelijken en instellingen. Open vragen staan apart.
- De uitleg is gericht aan de collega: vrijblijvende ideeën en korte aanwijzingen om te proberen, zonder eigen bugfixes of ontwerphistorie uit te leggen.
- De rondleiding bevat 26 korte suggesties met een highlight, een standaard aangevinkte checkbox voor Claude en Terug/Volgende. Uitvinken blijft mogelijk; expliciete uitvinkkeuzes worden bewaard. Oude gedeeltelijke opt-in-selecties worden eenmalig vervangen door alles aan. Kiezen beïnvloedt alleen de prompt, niet de werking van de demo.
- De selectie blijft lokaal in de browser bewaard. Kopiëren/downloaden voegt bestaande teksten samen; geen nieuwe generatie. Open vragen staan apart.
- GUI Engels; uitleg en vragen Nederlands. Command+Enter start eerst de sessie en daarna een take, of stopt de lopende take. Dit werkt ook met focus op de rondleiding. Enter plaatst een note en spatie is tekst.
- Herkenbare appcontext: zijbalk, sessiekeuze, Session length (min), Prep per cue, Max music (min), Add cues, Chat standaard dicht en de PDF-overzichten. De inspectie-HTML is geen volledige appbron; planningscijfers zijn voorbeelddata.
- Hoofdpaneel: Previous cue en Next cue met bracket-hints op een vaste rij onder de cuenaam, Overdub naast opnemen en een koffie-icoon bij Break. Standby vermeldt Not recording; alleen de lopende status is rood. Cut list toont take-tijd, kloktijd en Expected end. Cue-tijd/gepland, take-tijd, voor-/achterstand, kloktijd en verwachte eindtijd blijven in beeld; overige sessietijden onder Session details. Het doel van de verschillende klokken is een open vraag.
- Note-metadata vóór én na Enter op dezelfde manier bewerken: zwevende scrollbare Bar-lijst met All voor de hele take, typen plus Enter voor een maat, tijdcode aanklikken en Enter. Het klokje herstelt het oorspronkelijke typmoment. Alleen Delete blijft als aparte actie.
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
