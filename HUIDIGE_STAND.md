# Huidige stand · 18 oktober 2026

Dit document beschrijft de laatste werkende versie. De uitgebreidere notities in `prototype/src/feedback.md` zijn geschiedenis: oude voorstellen kunnen daar nog staan.

## Wat je krijgt

Een offline HTML-prototype met vijf voorstellen, eigen voorbeelddata, broncode, score-assets, uitleg en losse prompts voor Claude. Er is geen server nodig. Op Mac start en stopt Command+Enter; spatie blijft tekst. De homepagina begint met kleine suggesties en korte vragen; daarna volgen de prototypes. Onderaan kun je voorstellen aanvinken en bestaande prompts samenvoegen.

| Voorstel | Huidige uitwerking |
| --- | --- |
| 01 · Cue/takes | Takes onder hun cue, inklapbaar. Klikbare cues. Sterren 1–5, één Best per cue en genummerde Alt-labels. Knoppen blijven op vaste posities. |
| 02 · Bediening | A: groot paneel bovenaan, compacte bediening bij scrollen. B: vaste bediening links. Beide: vaste take-rijen, één notes-paneel en een horizontale Session timeline. Extra timers zijn ingeklapt. |
| 03 · Notes | Notes per take, algemene cue-notes apart. Enter plaatst een bullet. Alle notes zichtbaar; Edit/Delete en een rechtstreeks aanpasbaar maatnummer. A toont meerdere editors, B de gekozen take. |
| 04 · Kniplijst/partituur | Grote score rechts, takes/notes links. A: brede scoreweergave. B: vanuit de score werken, met compact sessieblok rechtsboven. Meerdere takes vergelijken en per take maten selecteren/notes schrijven. |
| 05 · Planning | Voorbeeldweergave voor voor-/achterlopen binnen de opnamebediening. Dit is een demo, geen echte voorspelling. |

Bij 02 kun je New layout en Previous layout vergelijken met dezelfde takes/notes. Full screen geeft ruimte om de indeling te proberen. De Nederlandse beoordeling Goed/Liever terug/Twijfel staat buiten de app-interface en is los van de implementatiechecklist.

## Kniplijst: bediening

- Muzieknoot, ketting en oog blijven samen op één regel zichtbaar, ook in All takes. De muzieknootknop schakelt tussen de partituur en een raster met alle takes van de huidige cue: aan toont de PDF, uit toont alle takes. De maatkolommen delen één horizontale as; takekleuren tonen selecties, strepen betekenen gedeeltelijke instrumentselecties. Klik op een maat om die take op de juiste scoreplek te openen; een stip toont de notes bij die maat. Best en Alt blijven vast naast de take staan; sterren worden in dit overzicht niet getoond. Met Link instruments uit zijn instrumentrijen per take uitklapbaar.

- De takekiezer links is een compacte lijst met sterren, Best en Alt op vaste posities, zonder losse kaders per take.
- Klik op een take om die te kiezen. Cmd/Ctrl+klik voegt een take toe aan de vergelijking of haalt die eruit. De laatst toegevoegde take is bewerkbaar; de lopende take verandert niet.
- Gekozen takes hebben eigen kleuren. Andere kniplijstbereiken hebben een zachter maar duidelijk zichtbaar kleurvlak met een gekleurde stippelrand als referentie; gekozen takes hebben een doorgetrokken rand; hun notes verschijnen pas bij expliciete vergelijking.
- Cmd/Ctrl+links klikken of slepen selecteert hele maten voor alle instrumenten. Cmd/Ctrl+rechts verwijdert ze. Boven de PDF staat een uitbreidbare rij met instellingen: Link instruments (ketting) en See other takes (oog), standaard beide aan. Met Link instruments uit selecteer je per instrument; opnieuw inschakelen verandert bestaande selecties niet. See other takes verbergt alleen achtergrondselecties, terwijl expliciet vergeleken takes zichtbaar blijven.
- Dubbelklik op de score opent een note. Enter plaatst kale tekst. Klik op bestaande tekst om te bewerken. Instrument en maat volgen de klikplek. All instruments betekent alle instrumenten binnen deze take, niet alle takes.
- Tekst staat standaard boven het instrument; All instruments boven de bovenste balk bij die maat. Below en At click position blijven beschikbaar om te corrigeren.
- Cmd/Ctrl+Z maakt scorebewerkingen ongedaan; Shift erbij herhaalt ze. Tijdens typen blijft normale tekst-undo werken.
- Een nieuwe take krijgt een lege eigen laag. Vergelijken kopieert geen notes of selecties.
- Score-notes staan in een compacte lijst met kolommen Bar, Note en Time, plus edit/delete-iconen met hover- en toetsenbordhighlight. De gekozen take staat boven de lijst; geen dubbele notes-kop, Go to bar of Score source in deze view. Alleen het aanklikbare maatnummer wordt getoond; geen boekpagina eronder.

## Wat echt is, wat voorbeeld is

- Alle benodigde beelden en een PDF-fragment zitten in het pakket. 26 cuekeuzes openen de bijbehorende pagina’s uit het meegeleverde scorebeeldmateriaal. 1M09A/B delen scorepagina’s, met eigen take-data.
- Arrival: boekpagina 7–9, maat 1–41, handmatig gecontroleerde vakken. Andere cuevakken zijn benaderingen vanuit gedrukte maatnummers. Automatische tekstplaatsing gebruikt een eenvoudige controle op vrije ruimte; geen volledige notatie-engine.
- Eigen PDF openen kan, maar geeft geen automatische maatmapping. De originele PDF wordt nooit beschreven; aantekeningen zijn overlays.
- De transportknop simuleert tijd. Er wordt geen audio opgenomen. Er is geen verbinding met DAW, film of echte tijdcode. Follow bar werkt alleen met beschikbare voorbeeldankers; geen live score following.
- Nieuwe notes, takes en eigen PDF’s blijven in deze geopende demo en verdwijnen bij herladen. Sommige voorkeuren, beoordelingen en promptkeuzes worden lokaal in de browser bewaard. Dit is geen gedeelde sessie-opslag.
- Een echte kniplijstexport en de keuze tussen film-, sessie- en take-tijdcode zijn nog open. Ook de vraag of je takes liever logt dan “recordt” blijft een vraag.
- Chat is al inklapbaar; daar staat geen vervangingsvraag meer over. Geen aparte montage-demo 06 en geen persoonsattributie in de voorstellen behalve Floris.

## Waar aanpassen

- `src/content.json`: voorstellen, varianten en implementatieprompts.
- `src/discussion.json`: kleine suggesties en vragen op de homepagina.
- `src/app.js`, `extra.js`, `inspection.js`: gedeelde UI, opname-/note-state en bestaande schermcontext.
- `src/controls-calm.js`: de rustigere versie van voorstel 02.
- `src/production-score.js`, `score-interactions.js`, `score-workflow.js`, `score-compare.js`: score, kniplijst, scoregerichte werkplek en vergelijken/tekstplaatsing.
- `src/style.css`, `src/shell.html`: vormgeving en HTML-sjabloon.
- `src/score-assets/`: meegeleverde beelden, fragment-PDF en mapping. De JSON-catalogus beschrijft ook de oorspronkelijke boeken; die volledige originelen zijn niet nodig en zitten niet in deze overdracht.
- `build.py`: maakt `dist/index.html`, documenten, redirects, PDF-fragment en prompts. `package.py`: een kleiner ZIP-pakket voor alleen bekijken. `handoff.py`: een nieuwe broncode-overdracht.

Paden in deze opsomming zijn relatief aan `prototype/`. Floris’ andere scoreproject is achtergrondcontext, geen afhankelijkheid. Het oorspronkelijke eerste ontwerp en de eerste overdracht waren niet beschikbaar; de huidige broncode en laatste review zijn leidend.
