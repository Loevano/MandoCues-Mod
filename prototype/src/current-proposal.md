# Eén voorstel · 18 oktober 2026

De huidige richting vervangt het overzicht met vijf afzonderlijke prototypes.

- Eén opnameweergave, gebaseerd op de gekozen 2A: bediening bovenaan en compacte balk bij scrollen.
- Eén kniplijst met de bestaande wijzigingen: grote doorlopende score met zoom en Expand/Restore, takes en notes, All takes, instrument-/zichtbaarheidsinstellingen, note-navigatie en slepen.
- Recording en Cut list delen cue, take, opname, beoordelingen, notes en concepten. Een lopende take blijft lopen bij wisselen.
- Bij openen: Rondleiding starten of Zelf bekijken. Later opnieuw openen via Rondleiding.
- De rondleiding volgt de workflow: hoofdpaneel → sessiestart → planning en cue/take → beoordeling en notes → partituur en kniplijst. Open vragen staan apart.
- De rondleiding bevat 26 korte suggesties met een highlight, een standaard aangevinkte checkbox voor Claude en Terug/Volgende. Uitvinken blijft mogelijk; expliciete uitvinkkeuzes worden bewaard. Oude gedeeltelijke opt-in-selecties worden eenmalig vervangen door alles aan. Kiezen beïnvloedt alleen de prompt, niet de werking van de demo.
- De selectie blijft lokaal in de browser bewaard. Kopiëren/downloaden voegt bestaande teksten samen; geen nieuwe generatie. Open vragen staan apart.
- GUI Engels; uitleg en vragen Nederlands. Command+Enter start eerst de sessie en daarna een take, of stopt de lopende take. Dit werkt ook met focus op de rondleiding. Enter plaatst een note en spatie is tekst.
- Hoofdpaneel: zichtbare Take-/Cue-/Session-knoppen, inclusief Break en End session. Cue-tijd/gepland, take-tijd, voor-/achterstand, kloktijd en verwachte eindtijd blijven in beeld; overige sessietijden onder Session details. Het doel van de verschillende klokken is een open vraag.
- Note-metadata direct bewerken: scrollbare Bar-lijst met All voor de hele take, typen plus Enter voor een maat, tijdcode aanklikken en Enter. Het klokje herstelt het oorspronkelijke typmoment. Alleen Delete blijft als aparte actie.
- Maatnummers bij notes zijn handmatig: invullen of bewust in de partituur kiezen. Geen Follow bar of afleiding uit de take-timer.

## Herstelpunt

De versie vóór deze samenvoeging is commit `d5f7119`, Git-tag `before-unified-ui-20261018`. Dezelfde tag staat op GitHub. Je kunt die versie apart bekijken zonder het huidige werk te overschrijven:

```sh
git worktree add ../MandoCues-vorige-versie before-unified-ui-20261018
```

Daarna open je `../MandoCues-vorige-versie/index.html`. Er is ook een lokale ZIP: `MandoCues-herstelpunt-20261018-d5f7119.zip` naast de gedeelde werkkopie.

De demo is geen recorder en heeft geen echte DAW-/filmtijd of live score following. Maatvakken buiten Arrival zijn benaderingen. Nieuwe demo-invoer verdwijnt bij herladen. Echte gedeelde sessie-opslag en kniplijstexport zijn geen onderdeel van dit voorstel.
