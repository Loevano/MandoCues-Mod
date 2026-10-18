# Eén voorstel · 18 oktober 2026

De huidige richting vervangt het overzicht met vijf afzonderlijke prototypes.

- Eén opnameweergave, gebaseerd op de gekozen 2A: bediening bovenaan en compacte balk bij scrollen.
- Eén kniplijst met de bestaande wijzigingen: grote score, takes en notes, All takes, instrument-/zichtbaarheidsinstellingen, note-navigatie en slepen.
- Recording en Cut list delen cue, take, opname, beoordelingen, notes en concepten. Een lopende take blijft lopen bij wisselen.
- Bij openen: Rondleiding starten of Zelf bekijken. Later opnieuw openen via Rondleiding.
- De rondleiding bevat 25 korte suggesties met een highlight, een checkbox voor Claude en Terug/Volgende. Kiezen beïnvloedt alleen de prompt, niet de werking van de demo.
- De selectie blijft lokaal in de browser bewaard. Kopiëren/downloaden voegt bestaande teksten samen; geen nieuwe generatie. Open vragen staan apart.
- GUI Engels; uitleg en vragen Nederlands. Command+Enter start/stopt, Enter plaatst een note en spatie is tekst.

## Herstelpunt

De versie vóór deze samenvoeging is commit `d5f7119`, Git-tag `before-unified-ui-20261018`. Dezelfde tag staat op GitHub. Je kunt die versie apart bekijken zonder het huidige werk te overschrijven:

```sh
git worktree add ../MandoCues-vorige-versie before-unified-ui-20261018
```

Daarna open je `../MandoCues-vorige-versie/index.html`. Er is ook een lokale ZIP: `MandoCues-herstelpunt-20261018-d5f7119.zip` naast de gedeelde werkkopie.

De demo is geen recorder en heeft geen echte DAW-/filmtijd of live score following. Maatvakken buiten Arrival zijn benaderingen. Nieuwe demo-invoer verdwijnt bij herladen. Echte gedeelde sessie-opslag en kniplijstexport zijn geen onderdeel van dit voorstel.
