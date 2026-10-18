# 01 — Cue & take-hiërarchie

De vraag: Hoe houden we cues en hun takes overzichtelijk bij elkaar?

De kleine aanpassingen uit het overzicht zijn in dit voorbeeld alvast meegenomen. Aanvulling: filter op sterren, markeer Alt-takes en houd maximaal één Beste per cue.

De bestaande lijst kan al uitklappen. Dit voorstel maakt de relatie cue → takes visueel duidelijker, met inspringing, leesbare cuegegevens en labels.

De inklapfunctie blijft behouden. Het voorstel verandert de presentatie en beoordelingen; bestaande overdubs en hun nummering blijven afzonderlijk bestaan.

Probeer: Open een cue, kies Beste of Alt en filter op 4–5 sterren. De beoordelingen en labels blijven bewaard als je het filter weghaalt.

### Inklapbare takes

Vrijblijvende suggestie van Floris: Cue & take-hiërarchie. Pas dit toe op mijn bestaande app. Mijn code, ontwerpkeuzes en oordeel blijven leidend. Bekijk eerst wat er al bestaat; behoud de bestaande visuele stijl en werk met bestaande componenten, state en opslag. Het prototype toont voorbeelddata, geen voorgeschreven architectuur. Alle tekst in de daadwerkelijke GUI moet Engels zijn, inclusief knoppen, labels, hints, tooltips, toegankelijkheidslabels en meldingen. Gebruik bijvoorbeeld Best, Add, Edit, Delete, Bar en Book p. Vragen, uitleg en voorstellen voor de collega mogen Nederlands blijven. Vertaal geen oorspronkelijke cue-/projectnamen of zelf ingevoerde notities.

Gewenst gedrag:
Groepeer takes visueel en semantisch onder hun eigen cue, met inspringing, een duidelijke cuekop en onderscheid tussen cuevelden en takevelden. Bewaar bestaande cue- en take-identiteiten. Een take mag niet bij de verkeerde cue terechtkomen. Gebruik de sterrenbeoordeling voor de kwaliteit; behoud Beste als afzonderlijke keuze. Gebruik voor de beoordeling van een take 1 tot en met 5 klikbare sterren, met een numerieke waarde per take. Een nieuwe take kan nog onbeoordeeld zijn. Een eventuele aparte Beste-take-markering blijft een afzonderlijke keuze. Maak de takes onder een cue altijd inklapbaar. Klikken op het cuenummer of de titel kiest die cue; een afzonderlijk pijltje klapt de takes open of dicht zonder de actieve cue te wijzigen. Selecteer en open de gekozen cue, maar behoud concepten en open toestand van andere cues. Tijdens een lopende take wordt een wissel naar een andere cue tegengehouden met een heldere melding; stop de take niet impliciet. Aanvulling: voeg een sterrenfilter toe, bijvoorbeeld alleen 4–5 sterren. Laat dit alleen de weergave filteren, nooit de takes verwijderen of hernummeren. Voeg een onafhankelijke Alt-markering toe. Beste is een toggle met maximaal één Beste per cue; opnieuw klikken mag die keuze opheffen. Alt en sterren blijven afzonderlijke eigenschappen. Nummer Alt-takes per cue in take-volgorde als Alt 1, Alt 2 enzovoort, onafhankelijk van het sterrenfilter. Toon het totale aantal alts bij de cue; zonder alts staat er een streepje. Niet-geselecteerde Alt-knoppen tonen Alt –. Houd de knopbreedte gelijk zodat sterren niet verschuiven. Bij verwijderen wordt de nummering opnieuw aaneengesloten. Integreer deze wijziging in de bestaande Recording-weergave. Hergebruik hetzelfde opnamepaneel, dezelfde sessiecontext, cue-/takelijst, notitie-invoer en state; maak geen los dashboard of nieuwe algemene UI. In de lokale voorbeelden gebruiken voorstellen 01, 02, 03 en 05 dezelfde componenten. De partituur/kniplijst is de aparte werkweergave. Beste verandert alleen de highlight: geen vinkje of wisselende Beste-tekst in de cuekop. Reserveer een vaste breedte voor Beste en Alt in alle toestanden; sterren, cuegegevens en omliggende tekst blijven op dezelfde plaats bij aan- en uitzetten.

Uitwerking:
Gebruik een toegankelijke uitklapknop per cue met aria-expanded. Laat meerdere cues tegelijk open kunnen. Toon in de gesloten cuekop het aantal takes zonder wisselende Beste-tekst. Behoud de open toestand bij het bewerken.

Controle:
Een take bewerken verandert geen andere cue; sterren en Beste blijven behouden bij open/dicht of wisselen van weergave. Toetsenbordbediening werkt en lege cues hebben een heldere lege toestand. Sterren blijven per take bewaard bij scrollen, open/dicht en wisselen van indeling. Cuekeuze en inklappen zijn aparte acties, bereikbaar met toetsenbord en met duidelijke labels. Een klik op een cue werkt ook zonder Go to cue. Inklappen verliest geen beoordelingen of notities; een lopende opname krijgt nooit ongemerkt een andere cue. Een nieuwe Beste heft de vorige Beste binnen dezelfde cue op, maar verandert andere cues niet. Alt blijft bewaard bij filteren en in-/uitklappen. Het filter verandert alleen zichtbaarheid. Controleer dat takekeuze, notes, sterren en cuebediening dezelfde gegevens gebruiken als de bestaande Recording-componenten.

Context uit het bestaande scherm:
De aangeleverde inspector-HTML is een momentopname van het gerenderde Recording-scherm, geen volledige JavaScript-/TypeScript-bron en geen geteste integratie. In die momentopname bestaan al een uitklapbare cue/takelijst, afzonderlijke Take- en Overdub-nummers, handmatige geplande tijd, Go to cue, Break, End session, aftekenen/ongedaan maken, Chat en PDF. Controleer de echte code en behoud deze bestaande functies en data; behandel de voorbeelden als voorstellen voor de presentatie of aanvullende invoer. Gebruik niet het totale aantal take- en overdub-rijen om het volgende gewone take-nummer te bepalen.

Maak een kleine samenhangende wijziging, controleer de bestaande flows en vat kort samen wat veranderd is. Implementeer alleen dit voorstel. Neem andere suggesties alleen mee waar het hierboven expliciet nodig is voor de getoonde flow.

