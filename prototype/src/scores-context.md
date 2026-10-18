# Partituren uit 06_SCORES

Gecontroleerd op 17 oktober 2026. De originele PDF-bestanden blijven ongewijzigd.

## Gevonden boeken

- **Full score**: 83 PDF-pagina’s — Afterparty - String Quartet - Full Scores (book) v3.pdf
- **Viola**: 29 PDF-pagina’s — Afterparty - String Quartet - Viola (book) v3.pdf
- **Violin 1**: 29 PDF-pagina’s — Afterparty - String Quartet - Violin 1 (book) v3.pdf
- **Violin 2**: 29 PDF-pagina’s — Afterparty - String Quartet - Violin 2 (book) v3.pdf
- **Violoncello**: 28 PDF-pagina’s — Afterparty - String Quartet - Violoncello (book) v3.pdf

## In het prototype

Prototype 04 opent per app-cue de bijbehorende full-scorepagina’s. De startcue is **1M02 — Arrival**, boekpagina 7–9, maat 1–41. Die drie pagina’s en maatvakken zijn handmatig gecontroleerd; het Arrival-fragment is ook als PDF meegeleverd. Voor de overige cues zijn de maatvakken benaderd vanuit de gedrukte maatnummers. Meermaatsrusten zijn niet opgesplitst in verzonnen individuele locaties.

De cuekiezer toont de juiste pagina’s en maatnummers. Links wissel je tussen takes; iedere take heeft eigen notes, maatselecties en concepten. Een nieuwe take begint schoon. De losse instrumentboeken blijven als bronbestanden op Floris’ computer en worden niet aan het prototype toegevoegd.

Notes bewaren de documentversie en cuegebonden pagina; de weergave toont ook de oorspronkelijke boekpagina. Voor Arrival is fragmentpagina 1–3 gelijk aan boekpagina 7–9.

De echte score heeft geen take-specifieke tijdankers. Maat kiezen en later corrigeren werken; de demo-timer bepaalt niet automatisch welke maat werkelijk gespeeld wordt. Ook het schematische voorbeeld gebruikt handmatig gekozen maatnummers; er is geen gesimuleerd maatvolgen.

## Cue-index van het volledige boek

| Cue in de PDF | PDF-pagina’s |
| --- | --- |
| 1M01 | 3–5 |
| 1M02 | 7–9 |
| 1M05 | 11 |
| 1M06 | 13 |
| 1M07 | 15 |
| 1M09AB | 17–20 |
| 1M10 | 21–23 |
| 1M11 | 25–26 |
| 1M15 | 27–32 |
| 1M16 | 33–34 |
| 1M17 | 35–36 |
| 1M18 | 37–45 |
| 1M20 | 47–48 |
| 1M21 | 49–51 |
| 1M22 | 53–55 |
| 1M23 | 57–59 |
| 1M24 | 61–63 |
| 1M26 | 65–66 |
| 1M27 | 67–69 |
| 1M28 | 71 |
| 1M34 | 73–76 |
| 1M38 | 77–78 |
| 1M40 | 79–80 |
| 1M41 | 81–82 |
| 1M43 | 83 |

De pagina-index is uit leesbare PDF-cuecodes samengesteld; 1M02 is daarnaast visueel gecontroleerd. Dit is een pagina-index, geen algemene scoreherkenning. **1M09AB** is één notatie in de boeken: app-cues 1M09A en 1M09B moeten expliciet aan dit gedeelde materiaal worden gekoppeld; niet stilzwijgend splitsen.

Score-catalogus.json bevat ook de cuepagina’s voor viool 1, viool 2, altviool en cello, met bestandsnamen en SHA-256-versies. Paginanummers van de cello wijken na 1M15 af van de andere partijen.


## Cue-overzicht in prototype 04

Alle 26 app-cues openen de bijbehorende echte full-scorepagina’s uit de index. De twee app-cues 1M09A en 1M09B delen de boekcue 1M09AB; hun takegegevens blijven apart. Bij Arrival zijn de maatvakken visueel gecontroleerd. De overige vakken zijn benaderd vanuit de gedrukte maatnummers: controleer ze en splits meermaatsrusten niet automatisch. De PDF-boeken blijven ongewijzigd. Notes en selecties staan in afzonderlijke demo-lagen per take en bron, en verdwijnen bij herladen. Er is geen live score following.


## Kniplijst en notes op de partituur

Prototype 04 heeft A (kniplijst) en B (partituur als hoofdwerkplek, met een compact sessieblok). Beide gebruiken dezelfde notes en kniplijst per take.

Dubbelklik opent de invoer. De maat en het instrument bepalen de context. Enter plaatst alleen de tekst, standaard boven de betreffende notenbalk; Alle instrumenten staat boven het systeem bij die maat. Onder en Op klikplek blijven opties. De plaatsing is een benadering op een bestaande PDF, zonder volledige notatie-engine. Maat, instrument en klikpositie blijven als metadata bewaard, met details in de lijst links. Ook zonder herkende maat kun je een note plaatsen. Een klik op de tekst bewerkt hem.

De kniplijst kiest altijd volledige maten voor alle instrumenten. Cmd+linksklik voegt toe; Cmd+rechtsklik verwijdert. Slepen werkt ook; Shift is niet nodig. De verticale plek beperkt de kniplijst niet tot een instrument. Staflabels helpen alleen bij de context van notes.

Cmd+Z maakt een selectie- of note-actie ongedaan; tekstinvoer houdt zijn eigen undo. Takekleuren blijven in de lijst en selecties herkenbaar. Een nieuwe take begint schoon; ongeplaatste notes blijven apart per take. Cmd/Ctrl+klik in de take-lijst schakelt extra takes in/uit ter vergelijking; één take blijft bewerkbaar. Andere kniplijsten zijn heel licht zichtbaar, hun notes alleen bij expliciete vergelijking. Een eigen PDF krijgt de maatmapping niet automatisch.


## Notes-kolom en taal

De titel Notes for Take 1 gebruikt dezelfde takekleur en een bolletje als de take-lijst. Book p. staat direct onder Bar, zonder lege tussenregel. Note, metadata en Edit/Delete staan compact onder elkaar. De GUI is Engels; de collega-uitleg blijft Nederlands. Eigen notities en oorspronkelijke cue-/projectnamen worden niet vertaald.
