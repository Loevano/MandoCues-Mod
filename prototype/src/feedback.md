# Alle notes van Floris

Bijgewerkt: 18 oktober 2026. Dit overzicht bundelt Floris’ opmerkingen uit deze chat. Latere correcties gaan voor eerdere varianten. Het onderscheid tussen wensen, open vragen en voorstellen blijft behouden.

## 1. Doel en overdracht naar de collega

- Kleine, klikbare prototypes maken om suggesties voor zijn opnameprogramma te laten zien en er een filmpje van te kunnen maken.
- Per suggestie een eigen omgeving, zodat hij één idee tegelijk kan bekijken en proberen.
- Bij twijfel A/B-varianten aanbieden, met duidelijk zichtbare verschillen.
- Per visueel voorbeeld een kort stukje: waarom zou dit handiger zijn? Geen lange lappen tekst op de pagina.
- De pagina begint met een kort lijstje kleine aanpassingen, zoals sterren in plaats van Good / NG / Hold. Daarna de prototypes, elk met één grotere vraag over indeling of bediening. Benoem dat de kleine voorstellen daarin alvast zijn meegenomen, zodat dezelfde functie niet telkens als nieuw voorstel aanvoelt.
- Per gekozen variant één complete, direct kopieerbare prompt voor zijn eigen Claude. De prompt moet de benodigde context bevatten en op zijn bestaande code worden afgestemd.
- Alles is vrijblijvend: zijn programma, zijn Claude en zijn ontwerpkeuzes gaan voor. Hij kan elk idee afzonderlijk overnemen of overslaan.
- Het overzicht simpel noemen, bijvoorbeeld **Prototypes van Floris**.
- In de tekst voor de collega niet verwijzen naar screenshots of deze chat; hij kent die achtergrond niet.
- Achteraf per suggestie kunnen aanvinken wat de collega wil implementeren, met één variant per gekozen A/B-voorstel. Daarna de bestaande teksten samenvoegen of weglaten tot één Claude-prompt, zonder opnieuw genereren. Ook de kleine suggesties los kunnen kiezen.
- Een overzicht met prototypes, begeleidende tekst en prompts kunnen doorsturen. Filmmodus is handig voor de schermopname.

## 2. Cues, takes en beoordelingen

- Duidelijk laten zien dat takes onderdelen van een cue zijn: eronder groeperen en laten inspringen.
- Het eerdere cue/take-ontwerpvoorstel is een referentie voor deze manier van presenteren.
- Laatste keuze: takes altijd kunnen inklappen. Suggestie 1 heeft daarom alleen de inklapbare uitvoering; B met permanent zichtbare takes vervalt.
- Klikken op cuenummer of titel kiest direct die cue in de lijst, zonder Go to cue nodig te hebben. Een apart pijltje toont of verbergt de takes zonder cuewisseling.
- Ook de geselecteerde take met notes moet kunnen inklappen, met behoud van concepten en beoordelingen.
- De eerste suggestie over deze ordening beviel; A/B vergelijken blijft bij de andere suggesties nuttig.
- Good / NG / Hold vervangen door een beoordeling van **1 tot en met 5 sterren**.
- Deze cue/take-groepering ook meenemen in de andere relevante prototypes, zodat de collega zijn eigen werkruimte blijft herkennen.

## 3. Suggestie 2: bediening en notes bij scrollen

- Het grote opnamepaneel met cue, status, timers en planning herkenbaar houden. Het mag niet onduidelijk worden of dat paneel verdwijnt of wordt vervangen.
- Variant A: het grote paneel blijft bovenaan; na scrollen blijft een compacte bedieningsbalk bereikbaar.
- Variant B: expliciet laten zien wat in een vast zijpaneel staat en wat in de lijst blijft.
- Duidelijk tonen wat vaststaat en wat scrollt. Zowel A als B moest begrijpelijker worden.
- Takes en notes niet uit de demonstratie weglaten: anders is niet duidelijk hoe dit op zijn programma aansluit.
- Geen verzonnen extra introductiepaneel met bijvoorbeeld ‘12 cues, 3 uur gepland’. Toon direct de relevante werkruimte.
- Notes moeten ook op het beginscherm bij de grote opnamebediening zichtbaar zijn; niet pas onderaan na scrollen.
- Laatste keuze voor 2A: het aparte scrollvak voor notes vervalt. Laat alle notes bovenin volledig onder elkaar staan. Het paneel groeit mee; alleen de hele werkruimte scrollt.
- De stopbediening bij suggestie 2 mag niet tussendoor verschijnen en verdwijnen bij scrollen. In 2A neemt de compacte balk het over zodra de grote opnameknop wegscrollt; de zwevende stopknop is alleen een vangnet buiten de zichtbare werkruimte.
- Bij de notes duidelijk scheiden welke opmerking bij welke take hoort.
- De interface rustiger maken; de hoeveelheid checkboxes maakte A en B onoverzichtelijk.

## 4. Notes schrijven

- Bij een take kunnen typen en met **Enter** een nieuwe losse note/bullet plaatsen.
- Daarna meteen verder kunnen typen aan de volgende note.
- **Shift+Enter** kan een nieuwe regel binnen dezelfde note maken.
- Een afzonderlijke plek voor **Cue algemeen** en notes bij de laatste of geselecteerde take is een bruikbare mogelijkheid.
- Altijd duidelijk aangeven bij welke cue en take je schrijft.
- Tijdcode en eventueel maatnummer als voorstel bij de note tonen; die voorstellen moeten later te wijzigen zijn.
- Ook na Enter het maatnummer direct kunnen corrigeren door op het cijfer te klikken en een ander nummer te kiezen, bijvoorbeeld uit een verticale cijferlijst. Geen aparte ‘wijzig’-link of verplichte Bewerk-stap. Voor verder gelegen maten ook kunnen typen. Een automatisch voorstel kan verkeerd zijn; een handmatige correctie blijft behouden.
- Het bedoelde moment automatisch vastleggen bij het schrijven. In de huidige proef wordt daarvoor het begin van het typen gebruikt, zodat later op Enter drukken de positie niet verschuift.
- Concepten en bestaande notes blijven bij hun eigen take wanneer je wisselt, een take stopt of een nieuwe begint.
- Geen aparte contextchat voor deze notitieflow toevoegen.

### Correctie over checkboxes

- Floris vroeg **geen afvinkbare opmerkingen of takenlijst** bij teksten zoals ‘Mooie inzet; deze bewaren’. Dat was een eigen invulling van Codex en is teruggedraaid.
- De bedoelde checkboxes zijn **Volg tijd** en **Volg maat**: automatisch de beschikbare actuele positie aan een nieuwe note koppelen, als dat werkt.
- Een geplaatste note blijft daarna aan de vastgelegde plek gekoppeld. Tijd en maat moeten achteraf aanpasbaar blijven.
- De exacte vorm en bronkeuze van deze volgopties moeten nog worden uitgewerkt. De proef heeft nu Volg maat met een vooraf ingestelde voorbeeldkoppeling. Dit is geen echte live herkenning; Volg tijd met bronkeuze blijft een open onderdeel.

## 5. Opnametoets en stoppen tijdens schrijven

- **Spatie is nodig om notes te schrijven en moet daarom geen globale opname-sneltoets zijn.** Alleen rekening houden met tekstfocus is als ontwerp te riskant.
- Een take kunnen stoppen zonder eerst naar boven te scrollen of de note-invoer te verlaten.
- De stopknop bij de invoer en een bereikbare vaste bediening zijn daarvoor nuttige mogelijkheden.
- Een geschikte vervangende sneltoets kiezen die niet met normale tekstinvoer of belangrijke browseracties botst.
- **Command+R is ongeschikt**, omdat dit de browserpagina herlaadt.
- Stoppen mag een concept en de vastgelegde positie niet verliezen.

### Voorstel van Codex, geen oorspronkelijke toetskeuze van Floris

- **Mac: ⌘+Enter — Stop take. Windows/Linux: Ctrl+Enter — Stop take.**
- Deze combinatie stopt alleen de actieve take, ook tijdens typen. Nogmaals indrukken start geen nieuwe take en plaatst geen note.
- Starten gebeurt in deze proef bewust via de opnameknop. De globale spatiebinding is verwijderd.
- De uiteindelijke app kan de sneltoets instelbaar maken. Controleer hem in de gebruikte browser, besturingssysteem en eventuele andere actieve muzieksoftware; er is geen universeel conflictvrije toets.
- Het voorstel geldt wanneer de opnamewerkruimte focus heeft. In de browser-adresbalk houden toetsen hun browserfunctie.

## 6. Welke positie hoort bij de note?

Floris’ open vraag: gebruiken we **filmtijdcode, sessietijd, take-tijd, maatnummer, of een combinatie**? De beschikbare posities zouden bij het schrijf-moment goed vastgelegd moeten worden.

| Verwijzing | Bedoelde plek | Nog te bepalen |
| --- | --- | --- |
| Filmtijdcode | Moment in de film | Welke player/recorder levert deze tijd, met welke frame rate en offset? |
| Sessietijd | Moment binnen de sessie | Bedoelen we sessie-verstreken tijd of de kloktijd? |
| Take-tijd | Moment binnen deze uitvoering | Is er een echte recorder-/mediaklok of alleen een app-timer? |
| Maatnummer | Muzikale plek in de score | Is die handmatig gekozen of via een gecontroleerde koppeling bekend? |

- De filmtijdcode bij notes kunnen gebruiken is expliciet gewenst als uitbreiding.
- Eén note kan meerdere verwijzingen hebben; ze hoeven elkaar niet uit te sluiten.
- Welke bron standaard wordt gevolgd, is nog een ontwerpkeuze. Het eerdere voorstel van Codex was take-tijd plus filmtijd waar beschikbaar, met maat erbij zodra betrouwbaar bekend.
- Niet suggereren dat alles al automatisch gesynchroniseerd is. De echte bronkoppelingen en het gedrag bij pauzeren, zoeken, herstarten en herhalingen moeten worden gecontroleerd.

## 7. Partituur en scoretool

- De score/partituur meenemen in de voorstellen; dit is een belangrijk onderdeel dat in de eerste proef ontbrak.
- Eerst kijken wat in het verwante project al bestaat, in plaats van een volledig werkende implementatie aan te nemen.
- De genoemde projectnamen waren **Score Analysis Tool** en mogelijk **Orchestral Analysis**. Verwant werk is gevonden in **Composition Study / Score Study**.
- De collega beschikt over de PDF/score. Onderzoeken hoe die naast de opname en notes bruikbaar kan worden gemaakt.
- De partituur op brede schermen **rechts**, takekeuze en notes **links**, in beide varianten.
- Notes aan een maat of scoreplek kunnen koppelen en vanuit de note naar die plek teruggaan.
- Graag automatisch zien welke maten een take bevat, op basis van de juiste partituur en een koppeling met de uitvoering. Die positie vervolgens als maatvoorstel bij de note aangeven.
- Het prototype laat dit gedrag zien met vooraf ingestelde maat/tijdankers per voorbeeldtake. Voor echte automatische invulling is een betrouwbare koppeling met de gespeelde positie nodig. Alleen de PDF kennen is daarvoor onvoldoende.
- De ervaring uit het andere project opnemen in de Claude-overdracht, zodat hij niet opnieuw alles hoeft uit te zoeken.

### Gecontroleerde projectcontext, geen volledige functionaliteitsclaim

- In Composition Study bestaat een specifieke PDF/video-scoreplayer met maatgebieden en handmatige tijdankers. Bestaande verslagen beschrijven tests met echte media; deze player is niet opnieuw getest in deze taak.
- Dit bewijst geen algemene PDF-importer, automatische noot-/maatherkenning of live score following.
- De prototypeverzameling gebruikt nu de echte Arrival-score als standaard in prototype 04. De schematische proef met vooraf ingestelde tijdankers blijft apart te kiezen. Een andere PDF kan lokaal geopend worden; pagina en maat worden daarbij handmatig gekozen.
- De take-klok in deze prototypes is een demonstratie. Er is geen echte recorder- of filmverbinding toegevoegd.

## 8. Tijdweergave

- De tijd onder de takes staat in 24-uursnotatie, terwijl het grote paneel AM/PM toont.
- Als kleine suggestie opnemen: overal hetzelfde tijdformaat gebruiken, bijvoorbeeld **19:54:59**.
- Dit gaat over de notatie van een kloktijd, niet over het omzetten van take-duur naar kloktijd.

## 9. Geparkeerd of teruggedraaid

- De aparte opnamestatusvarianten met een rustigere balk of rood kader zijn vooral een smaakkeuze en hebben lage prioriteit. Bewaren voor eventueel later, niet als belangrijk hoofdvoorstel presenteren.
- Geen contextchat als vervanging van de bedoelde takenotes.
- Geen afvinkstatus bij de inhoud van opmerkingen.
- Geen verwijzingen naar screenshots in de collega-presentatie.
- Geen automatische score-/tijdkoppeling als werkend presenteren wanneer die nog niet gebouwd of gecontroleerd is.

## Technische bron voor de toetskeuze

De officiële [Chrome-sneltoetsen](https://support.google.com/chrome/answer/157179?hl=en) en [Apple-sneltoetsen](https://support.apple.com/en-us/102650) zijn bekeken. Browser- en systeemsneltoetsen zijn contextafhankelijk; de keuze voor ⌘/Ctrl+Enter als uitsluitend Stop is een productvoorstel van Codex, geen aanbeveling van Apple of Google.


## 10. Aanvullende input — toegevoegd

Aanvullingen zijn bij de bestaande voorstellen verwerkt; overlappende ideeën blijven bij elkaar.

- **Waarom:** minder onoverzichtelijke papieren aantekeningen, sneller corrigeren en notes kunnen gebruiken in andere workflows.
- **Valkuil:** één afgesproken take-telling met muzikanten en engineer. Geen verschillende ‘waarheden’ over welk take-nummer wordt opgenomen.
- **Sterren:** Vijf sterren met een filter, bijvoorbeeld alleen 4–5 sterren.
- **Beste en Alt:** maximaal één Beste per cue; meerdere reservetakes kunnen Alt krijgen. Sterren blijven apart.
- **Snelle notes:** suggesties voor Intonatie, Meer expressief, Minder expressief, Strak en Alt take. Nog kunnen aanvullen voordat je Enter drukt.
- **Bediening:** onderscheid Take, Cue en Sessie; notes bij de hoofdweergave. Dit vult prototype 02 aan.
- **Cue-sneltoetsen:** [ en ] voor vorige/volgende; een modifier voor direct naar bijvoorbeeld cue 8. In deze proef Alt+1–9 buiten tekstinvoer; uiteindelijke toetsen configureerbaar en op conflicten controleren.
- **Planning:** snel ‘één minuut achter’ kunnen zien. Groot getal, teken, voor/achter en kleur; leesbaar sessieplan zonder afgekorte cuecodes. Eigen prototype 05.
- **Benamingen:** Max music, muziekduur, complexiteit, geplande tijd en tijd op de cue met duidelijke eenheden en labels.
- **Gedeelde take-identiteit:** eerst handmatig afspreken welk nummer telt. Bewaard als ontwerpvraag; het oorspronkelijke prototype 06 is vervallen.
- **Timen of loggen:** De vraag is of alleen registreren voldoende is, zonder take-duur te hoeven meten. Bewaard als note/vraag, zonder eigen prototype. Registratietijd en echte mediastarttijd zijn verschillende velden.
- **Creation date en DAW:** Bestandsdatum is genoemd als mogelijke aansluiting op Pro Tools/Logic. Dat is als onderzoeksvraag bewaard; er is geen automatische koppeling vastgesteld of gebouwd. De demo kan alleen handmatig een bestandsnaam aanwijzen, zonder upload.
- **Kniplijst:** per cue maatbereik; per take meerdere delen includen/excluden. Voorbeeld: Take 1 maat 1–4 en 7–9, Take 2 maat 5–6. Prototype 06 (voorheen 07) met maatbereiken (A) en een eenvoudige maat-tijdlijn (B). Gaten blijven zichtbaar, ook in de concept-CSV.
- **Complexiteit:** begin handmatig en overzichtelijk. Een maat-CSV is nog geen audio-edit, EDL of DAW-montage; de editor controleert de overgangen.

Aanvullende-input.md bevat de volledige input en de vindplaatsen. Nieuwe ontwerpen en kleinere aanvullingen zijn afzonderlijk te kiezen in de overdracht aan Claude. De vraag over loggen staat onder Nog uit te zoeken; het aparte prototype daarvoor is op verzoek vervallen.


## 11. Referentie uit de inspector — uitsluitend lokaal gebruiken

- Floris leverde HTML uit de inspector aan om het prototype herkenbaarder en beter passend te maken. SoundVibeHQ zelf mag hiervoor niet veranderen.
- De aangeleverde tekst is gerenderde HTML, geen volledige JavaScript-/TypeScript-code. De prototype-aanpassingen zijn uitsluitend lokaal; de pagina en zijn scripts worden niet uitgevoerd.
- In de momentopname bestaan al uitklappen, gewone takes, overdubs, labels, cuenotities, handmatige planning, Go to cue, Break/End session, aftekenen, Chat en PDF. Die functies moeten in de echte app behouden blijven.
- Prototype 01 formuleert uitklappen daarom als bestaande functionaliteit met een duidelijker presentatievoorstel.
- Prototype 02 krijgt meer herkenbare sessiecontext, cuegegevens, een leesbaar cueplan en een Overdub-knop.
- Take- en overdub-nummers blijven afzonderlijk. Een overdub schuift het volgende gewone take-nummer niet op; notes en labels blijven bij hun eigen registratie.
- De zichtbare planningsuitleg wordt als context meegenomen, zonder te doen alsof de interne berekening of backend is getest.
- Bestaand-scherm-context.md geeft de relevante samenvatting voor de collega en Claude; de ruwe inspectiepagina wordt niet meegeleverd.

## 12. Echte scores uit 06_SCORES

- Floris wees de map 06_SCORES aan. Hier staan vijf PDF-boeken: Full Scores (83 pagina’s), viool 1 (29), viool 2 (29), altviool (29) en cello (28).
- De originele bestanden zijn alleen gelezen. Voor prototype 04 is een apart fragment van 1M02 Arrival gemaakt: boekpagina 7–9, maat 1–41. De drie paginabeelden en maatgebieden zijn visueel gecontroleerd.
- De echte partituur staat standaard rechts; notes blijven links. Via Ga naar maat kun je een bekende maat kiezen, een note plaatsen, het cijfer achteraf aanpassen en met ↗ naar de scoreplek teruggaan.
- Fragmentpagina 1–3 en originele boekpagina 7–9 worden uit elkaar gehouden. Bij een bronwissel blijven concepten per take en document bewaard.
- De echte score heeft nog geen take-specifieke tijdankers. Volg maat staat daarom uit. De schematische proef blijft apart beschikbaar voor het testen van voorbeeldankers.
- Er is een pagina-index voor alle vijf boeken gemaakt op basis van leesbare cuecodes. 1M02 is in alle vier losse stemmen op PDF-pagina 4 te vinden. De overige stemmen worden niet allemaal in het prototype geladen of aan de ZIP toegevoegd.
- 1M09AB is één gedeelde scorecue in de boeken. De app-cues 1M09A en 1M09B moeten expliciet aan dat materiaal worden gekoppeld, niet automatisch opgesplitst.
- Partituren-overzicht.md beschrijft de bron en grenzen. Score-catalogus.json bevat cuepagina’s en SHA-256-versies. Het is geen automatische muziek- of uitvoeringsherkenning.


## 13. Scorebediening per cue en take — weer opgepakt

Floris heeft deze uitbreiding na het parkeren weer opgepakt.

- Per cue de bijbehorende scorepagina’s en maten vanuit het overzicht openen.
- Cmd + links slepen voegt toe aan de selectie; Cmd + rechts slepen verwijdert eruit. Ctrl op Windows/Linux; aparte modi voor touch en toetsenbord.
- Gewoon links klikken opent een notitievak bij de gekozen scoreplek, met maat en het tijdanker van het klikmoment.
- Elke nieuwe take begint met een schone scorelaag, zonder notes, concepten of selecties van eerdere takes.
- Een take-lijst laat je heen en weer wisselen tussen de eigen score-notities, concepten en selecties van iedere take.
- Selecties mogen uit losse maten en verschillende pagina’s bestaan. Ze blijven apart van de notes: uit de selectie halen wist geen note.
- Voor Arrival zijn de maatvakken gecontroleerd. Bij de overige cues zijn de vakken uit gedrukte nummers benaderd; meermaatsrusten worden niet automatisch opgesplitst. De twee app-cues 1M09A en 1M09B delen de score 1M09AB, maar niet hun take-notities.


## 14. Beste zonder vinkje

- Bij Beste blijft alleen de highlight de geselecteerde status aangeven. Geen extra vinkje dat de knop breder maakt en de sterren laat verschuiven.


## 15. Genummerde Alt-takes

- Toon per cue hoeveel Alt-takes er zijn; zonder alts een streepje.
- Label de gekozen reservetakes Alt 1, Alt 2 enzovoort in take-volgorde. De nummering blijft onafhankelijk van filters.
- Niet-geselecteerd: Alt –. Een vaste knopbreedte voorkomt dat sterren verschuiven.


## 16. Notities verwijderen

- Naast Bewerk staat Verwijder bij iedere take-notitie. Verwijderen raakt alleen die note; de overige notes en het concept blijven staan.


## 17. Stopknop gescheiden van notities

- Geen Stop take-knop naast Plaats of de notitie-acties, om onbedoeld stoppen te voorkomen. Dit vervangt het eerdere voorstel voor een stopknop direct bij de invoer.
- Stop blijft bereikbaar via de afzonderlijke opnamebediening en de compacte bediening bij scrollen.


## 18. Prototype 6 wordt alleen een vraag

- Timen of loggen en de gedeelde take-telling blijven onder Nog uit te zoeken staan. Het zelfstandige prototype daarvoor is verwijderd.
- De kniplijst schuift van prototype 07 naar 06; de eerdere prototypes 01–05 behouden hun nummer.


## 19. Geen bronlabels bij de voorstellen

- Persoonlijke bronvermeldingen zijn verwijderd uit het overzicht, de voorbeelden, prompts en overdracht. De suggesties blijven staan.


## 20. Eerst kleine suggesties, daarna korte vragen

Direct onder de kleine suggesties en vóór de prototypes staan deze vragen, zonder implementatieopdracht:

- Waarom houden we de tijd van elke take bij?
- Zou ‘Nieuwe take’ maken en selecteren ook werken?
- Wat gebeurt er met de timers als je vergeet een take te starten?
- Welke timers gebruiken we tijdens de sessie echt?
- Is één voor-/achterstand genoeg, bijvoorbeeld ‘1:20 behind’ of ‘+01:20’?
- Kunnen we de filmtijdcode ook bij notes bewaren?


## 21. Kniplijst op de partituur — vervangt de eerdere scorebediening

- Eén grote, doorlopende partituur; geen A/B en geen bedieningsblokken boven de score.
- Dubbelklik plaatst een note op de klikplek, gekoppeld aan maat en instrument. De tekst blijft zichtbaar op de score.
- Cmd+dubbelklik: één instrument. Cmd+Shift+dubbelklik: alle instrumenten. Bij een gewone dubbelklik geldt een volledige selectie in die maat voor alle instrumenten.
- Cmd+links/rechts slepen: geraakte maten en instrumenten toevoegen/verwijderen. Een drag kan meerdere instrumenten raken; Shift geldt altijd voor alle.
- Cmd+Z: ongedaan maken van selectie- en note-acties. Normale tekst-undo blijft werken tijdens typen.
- Elke take behoudt zijn eigen kniplijst. Korte gebruiksuitleg onder de partituur.


## 22. Geen apart montageprototype

- Prototype 06 Montage/Kniplijst export is verwijderd, ook uit de navigatie en implementatiekeuzes.
- Prototype 04 heet gewoon Kniplijst.
- Alleen als opmerking erbij: ‘Later: deze kniplijst exporteren voor de editor?’ Geen aparte implementatieopdracht.


## 23. Gedeelde opnameweergave en nieuwe klikbediening

- De gewone voorstellen gebruiken dezelfde Recording-componenten: opnamepaneel, sessiecontext, cueplan, cue-/takelijst en notes. Geen los nieuw dashboard per suggestie.
- De kniplijst blijft de aparte partituurweergave, met een lijst van alle takes van de cue. Kiezen wisselt naar de eigen PDF-laag van die take.
- Cmd+linksklik voegt maat-/instrumentvakken toe; Cmd+rechtsklik verwijdert ze. Slepen en Shift voor alle instrumenten blijven mogelijk.
- Een gewone linksklik opent nu de commentbox; dubbelklikken is niet meer nodig. Enter plaatst de comment linksboven op die scorepagina.
- Iedere take heeft een vaste kleur, terug te zien in de take-lijst, maatselectie en commentboxen. Een nieuwe take begint schoon.
- Concept-comments blijven bij hun eigen take als je tussendoor een andere take kiest.


## 24. Geen verschuiving bij Beste

- Beste verandert alleen de highlight, zonder vinkje of extra tekst in de cuekop.
- Vaste knopbreedtes: sterren, tekst en knoppen blijven staan bij aan- en uitzetten of een andere Beste kiezen.


## 25. Partituur-toggle in het hoofdvenster

- Partituur aan/uit vanuit de bestaande opnameweergave; rechts naast bediening en notes.
- De score volgt de actieve cue. Takes en concepten blijven behouden, net als de leespositie per cue.
- Op een smal scherm staat de partituur eronder. De leesweergave staat in het hoofdvenster; de kniplijst blijft de plek om scoreselecties en comments te proberen.


## 26. Alternatief: werken vanuit de partituur

- Extra alternatief B bij prototype 4: de partituur als hoofdwerkplek voor notes en kniplijst.
- Links de takes met hun eigen notes en scorelaag; doorklikken om terug te lezen.
- Rechtsboven een klein sessieblok: cue, lopende take, nieuwe take, cuetijd en voor-/achterstand. Overige tijden ingeklapt.
- Planning en herinneringen blijven werken, bijvoorbeeld als de cue langer duurt dan gepland.
- Een oudere take bekijken verandert de lopende take niet. Cue- en sessietijd lopen onafhankelijk door.
- De bestaande kniplijst en opnameweergave blijven beschikbaar. Een workflow om te proberen, geen voorgeschreven vervanging.


## 27. Notes als gewone partituurtekst; kniplijst voor alle instrumenten

- Notes staan als alleen de tekst op hun plek in de score, zonder kaders of labels. De plek bepaalt de context.
- Details blijven in de notes-lijst links; de tekst op de score blijft aanklikbaar om te bewerken.
- De kniplijst selecteert altijd volledige maten voor alle instrumenten. Geen aparte instrumentselecties; Shift is niet nodig.
- Toevoegen, verwijderen, slepen en undo werken op hele maten. Dit geldt in A en B.


## 28. Suggestie 2 rustiger, met zichtbare vergelijking

- Take-regels blijven even groot; sterren, Beste en Alt staan altijd op dezelfde plek. Geen groeiende editor in een geselecteerde take-regel.
- Eén apart notitiepaneel; de bekeken en lopende take blijven onderscheiden.
- Minder tekst en meteen zichtbare timers; aanvullende sessiegegevens inklapbaar.
- Het sessieplan blijft een horizontale tijdlijn, met bloklengte naar geplande cuetijd.
- A: bediening bovenaan met compacte balk na scrollen. B: vaste bediening links. Beide kunnen schermvullend.
- Vorige/nieuwe versie vergelijkbaar; per wijziging Goed, Liever terug of Twijfel kunnen aangeven en bewaren.

## 29. Takes vergelijken in de kniplijst

- ⌘/Ctrl+klik schakelt takes bij/uit. Een gewone klik kiest weer één take.
- Er blijft één take bewerkbaar; de werkelijk lopende take verandert niet door vergelijken.
- Expliciet gekozen takes tonen hun eigen kniplijstkleuren. Andere takes blijven heel licht als achtergrond zichtbaar, zonder hun notes.
- Een nieuwe take begint schoon en neemt geen vergelijkingslagen over. Kniplijstselecties blijven altijd voor alle instrumenten.

## 30. Dubbelklik en gebruikelijke tekstplaatsing op de score

- Dubbelklik schrijft een note; een gewone klik op bestaande note-tekst opent bewerken. Dit vervangt de eerdere gewone klik om notes te plaatsen.
- Standaard tekst boven de betreffende notenbalk. Voor Alle instrumenten staat de tekst boven de bovenste balk bij die maat, binnen deze take.
- Onder en Op klikplek blijven opties. Alleen tekst op de score; details links.
- Dorico onderscheidt staff-attached en system-attached text. De PDF-proef benadert plaatsing met staflabels en controle op bestaande donkere pixels, zonder een volledige notatie-engine na te bouwen.
- Geen zwart hovervlak over de partituur.


## 31. Compacte notes-kolom en Engelse GUI

- De take bij de notes-kop krijgt dezelfde kleur en hetzelfde bolletje als de take-lijst.
- Book p. staat direct onder Bar, links uitgelijnd met het maatnummer. Geen lege tussenregel.
- Minder witruimte tussen note, metadata en Edit/Delete.
- Alle daadwerkelijke GUI-tekst is Engels: knoppen, labels, opties, invoerhints, tooltips, toegankelijkheidslabels, meldingen en voorbeeldnotities.
- Vragen, uitleg en voorstellen voor de collega mogen Nederlands blijven. Dit geldt ook voor de toelichting in de Claude-overdracht; die schrijft wel expliciet een Engelse GUI voor.
- Oorspronkelijke cue-/projectnamen en door de gebruiker geschreven notes worden niet vertaald.


## 32. Kniplijstkleuren duidelijker

- Blauwe en groene referenties van andere takes waren te licht. Maak ze duidelijker zichtbaar.
- Sterkere kleurvlakken en een gekleurde stippelrand voor andere takes; gekozen takes hebben een doorgetrokken rand. De muziek moet leesbaar blijven.


## 33. Korte suggesties met context; Mac-sneltoets

- Leg bij kleine suggesties kort uit waarom, zonder een nieuwe workflow voor te schrijven.
- Start/stop met spatie kan botsen met notes typen. Voorstel nu: Command+Enter voor start én stop op Mac. Dit vervangt de eerdere stop-only-keuze. Gewoon Enter plaatst een note; toetsherhaling doet geen extra start/stop.
- Stel bij notes automatisch tijdcode en waar mogelijk een maatnummer voor; beide blijven na Enter aanpasbaar.
- Open vraag: welke tijd past bij notes — film, take, sessie of kloktijd — en kunnen we één vaste bron aanhouden?
- Vraag waarvoor de duur van iedere take wordt gebruikt en of alleen New take maken/selecteren ook werkt.
- De voorstellen blijven vrijblijvend; geen verzoek om de hele workflow om te gooien.


## 34. Eén voorstel met rondleiding

- De huidige vijf-prototypeversie bewaren: d5f7119, tag before-unified-ui-20261018 en een herstel-ZIP.
- Geen losse prototypes meer, maar één pagina met Recording/Cut list-toggle en gedeelde take-, note- en opnamegegevens.
- Opname-indeling: de gekozen 2A met bediening bovenaan en compacte balk bij scrollen.
- Kniplijst: de bestaande wijzigingen uit de opgehaalde versie behouden.
- Bij openen een bericht met Rondleiding starten of Zelf bekijken.
- Rondleiding met één korte suggestie en highlight tegelijk, per suggestie een checkbox voor de Claude-prompt, plus Terug/Volgende.
- Alleen gekozen bestaande tekstonderdelen samenvoegen; niet opnieuw genereren. Vragen blijven los van implementatiekeuzes.
- Onduidelijke ontwerpkeuzes eerst voorleggen; geen nieuwe A/B-keuzes of afwijkende UI's verzinnen.


## 35. Claude-prompt standaard aangevinkt

- Suggesties staan bij een nieuwe selectie standaard aangevinkt voor de Claude-prompt.
- Je kunt iedere suggestie uitvinken. Eerder opgeslagen keuzes blijven behouden, ook als alles is uitgezet.


## 36. Zo min mogelijk onnodig lezen

- Rondleidingtekst beperken tot de suggestie en hoe je die probeert.
- Geen uitleg over normale kwaliteitseisen of eigen bugfixes, zoals niet-verspringende sterren en knoppen. Die gewoon goed laten werken.
- Technische details blijven in de Claude-prompt, niet in de korte uitleg voor de collega.


## 37. Concreet uitleggen wat een paneel doet

- Take-notes kort uitleggen: klik een take; lees en schrijf zijn notes in het getoonde paneel.
- Algemene cue-notes niet door diezelfde uitleg mengen. Ze bestaan apart onder Cue notes en gaan over de hele cue.
- Ook overige uitleg concreet formuleren: wat klik je aan en wat zie je dan, zonder abstracte termen of extra bijzinnen.


## 38. Vanzelfsprekende bewerkbaarheid niet uitleggen

- Bij tijdcode en maat alleen noemen wat automatisch wordt toegevoegd. Dat beide altijd bewerkbaar zijn hoeft niet in de korte toelichting.


## 39. Cuekeuze kunnen proberen in de rondleiding

- Bij direct aanklikken meerdere cues zichtbaar en klikbaar maken, in plaats van één cue uitlichten.
- Korte uitnodiging om verschillende cues te proberen; opnamepaneel, geselecteerde cue en takes moeten zichtbaar meewisselen.


## 40. Cue als hoofdniveau, takes daaronder

- Take-regels rechts van de cue inspringen, zodat ze duidelijk bij die cue horen.
- De huidige takegrootte behouden; cuenummers minstens even prominent maken.
- De bestaande inklapbare lijst behouden, met een subtiele verticale lijn voor de onderliggende takes.


## 41. Geselecteerde cue duidelijker markeren

- De gekozen cue moet ook in de lijst direct herkenbaar zijn, naast de bestaande markering in het opnamepaneel en de timeline.
- Geef de volledige cuekop een gekleurde achtergrond en een lichte accentlijn links; laat die meewisselen bij cuekeuze.
- Behoud het onderscheid tussen de gekozen cue en de geselecteerde take, ook in de rondleiding.


## 42. Maatnummers voorlopig handmatig

- Zonder betrouwbare koppeling met de uitvoering geen automatische maatnummers voorstellen.
- Vul de maat handmatig in of kies hem bewust in de partituur; achteraf blijft het maatcijfer direct aanpasbaar.
- Follow bar en gesimuleerde maat/tijdvoorstellen uit de actieve demo verwijderen. Een take-timer bepaalt geen gespeelde maat.
- Tijdcode blijft bij de note; automatisch maatvolgen eventueel later met een betrouwbare bron onderzoeken.


## 43. Alle suggesties standaard aangevinkt

- Ook suggesties vanaf 6 en verder standaard selecteren voor de Claude-prompt.
- Oude gedeeltelijke selecties uit de eerdere opt-in-versie eenmalig vervangen door alles aan.
- Nieuwe opslag onthoudt alleen expliciet uitgevinkte suggesties. Nieuwe suggesties beginnen aangevinkt; eigen uitvinkkeuzes blijven behouden bij teruggaan en herladen.


## 44. Takekeuze kunnen proberen bij Notes per take

- Bij suggestie 6 zowel de takes als hun notitiepaneel uitlichten.
- Takeknoppen aanklikbaar houden en het paneel zichtbaar laten meewisselen bij het kiezen van een andere take.
- De uitleg kort houden: verschillende takes aanklikken en hun notes zien.


## 45. Command+Enter ook direct en voor sessiestart

- Suggestie 7 direct met Command+Enter kunnen proberen, zonder eerst met de muis op de opnameknop te klikken.
- Eerste druk start de sessie; daarna start en stopt dezelfde combinatie een take. Sessiestart maakt geen take.
- Focus op rondleidingstekst mag de sneltoets niet blokkeren. Welkomst- en promptvensters blijven afgeschermd.
- Spatie blijft tekst; Enter plaatst een note. Geen herhaalde acties door een ingedrukte toets of IME-compositie.


## 46. Vraag naar het doel van de verschillende klokken

- Kort en neutraal vragen waarvoor de verschillende klokken tijdens een sessie gebruikt worden.
- Het huidige voorstel kiest een presentatie; het gebruiksdoel van de bestaande timers is nog een open vraag. Geen opdracht om die timers of hun logica te verwijderen.


## 47. Middenweg voor het hoofdpaneel

- Direct zichtbaar: cue met muziekduur en geplande werktijd, start/stop, take-tijd, cue-tijd tegenover gepland en voor-/achterstand.
- Gekozen extra tijden: kloktijd en verwachte eindtijd. Overige sessietijden uitklapbaar behouden.
- Previous cue, Next cue en Overdub weer zichtbare knoppen. Voor nu ook Break en End session zichtbaar proberen, gegroepeerd onder Take, Cue en Session.
- Geen bestaande functies of klokken schrappen. Het doel van de oorspronkelijke klokken blijft een korte open vraag voor de collega.
- Lokale Break/End session zijn demonstratiegedrag: notes en takes blijven bewaard; sessieacties stoppen geen lopende take impliciet. In de echte app blijft de bestaande logica leidend.


## 48. Grote partituur met zoom en doorlopende pagina’s

- Zoom in en uit kunnen kiezen, met een percentage en Fit width.
- De score krijgt de beschikbare breedte en hoogte; Expand score view maakt extra ruimte. Escape herstelt de normale werkruimte.
- Alle pagina’s doorlopend onder elkaar laten staan. Jens’ onafhankelijke scroll van score en takes/notes en de leespositie bij takekeuze behouden.
- Het lange uitlegblok onder de score verwijderen uit de GUI. De bediening kort in de rondleiding uitleggen.
- Notes, kniplijstselecties en vergelijkingen blijven correct op hun plek bij zoomen en vergroten.


## 49. Maat en tijdcode direct bewerken

- Geen aparte Edit-knop naast notes; Delete blijft.
- Bar opent een scrollbaar menu met All en de maatnummers van de cue (met wat extra ruimte). All is bevestigd als een note voor de hele take, zonder specifiek maatnummer.
- Direct een nummer kunnen typen en Enter drukken. Another bar en Choose bar vervallen.
- Tijdcode aanklikken, tekst wijzigen en Enter drukken; Escape annuleert.
- Een klein klokje herstelt de oorspronkelijke tijdcode, niet de huidige positie. De tijdcode wordt bij het beginnen met typen vastgelegd; deze oorspronkelijke waarde blijft bewaard na correcties en andere note-bewerkingen.


## 50. Rondleiding volgt de sessieworkflow

- Eerst het hoofdpaneel kort toelichten vanuit Floris: bediening en belangrijkste tijden bij elkaar.
- Daarna sessiestart en take-start/stop met Command+Enter; spatie blijft voor het typen van notes.
- Vervolgens planning, cue- en takekeuze, beoordeling en notes maken/bewerken; daarna naar de partituur en kniplijst.
- Vragen over de verschillende klokken en het nut van take-timing staan apart onder Vragen, zonder extra tekst in de introductie.
- Bestaande promptkeuzes blijven aan dezelfde suggestie-ID gekoppeld bij het herordenen.


## 51. Quick notes direct zichtbaar

- Veelgebruikte notes staan direct als knoppen bij de editor, zonder uitklapmenu.


## 52. Rondleiding scrolt naar de suggestie

- Elke stap brengt het bijbehorende onderdeel automatisch in beeld, ook na zelf scrollen.
- Het sessieplan wordt als tijdlijn zichtbaar gemaakt; rekening houden met de vaste opnamebalk.


## 53. Trackpadzoom

- In- en uitzoomen door te knijpen op het trackpad boven de partituur.
- De plek onder de vingers blijft het anker; normaal scrollen blijft onafhankelijk werken.


## 54. Kniplijst permanent groot, één bovenbalk

- Recording/Cut list, cue/take en opnamebediening staan samen in één compacte balk boven de kniplijst.
- Geen aparte titel-/projectrij en geen Expand/Restore-stap meer; de score vult meteen de beschikbare werkruimte.
- Rondleiding, Vragen en Claude-prompt blijven bereikbaar. Op smalle schermen mag de compacte balk over twee regels lopen.


## 55. Voorstelbediening onderaan Recording

- Naam, Rondleiding, Vragen en Claude-prompt onderaan de scrollbare opnameweergave, zodat het hoofdpaneel meer ruimte krijgt.
- De compacte kniplijstbalk blijft behouden.


## 56. Scorepositie bepaalt maat bij plaatsen en slepen

- Dubbelklikken vlak boven een maat neemt die maat direct over in de note.
- Tijdens slepen licht de doelmaat subtiel op; loslaten past het maatnummer en de instrumentcontext aan.
- Boven de volledige instrumentgroep is All instruments; bij een instrument is de note instrumentgebonden.
- Notes blijven kale tekst op de gekozen plek; verplaatsen blijft ongedaan te maken.


## 57. Score-note verwijderen met ⌫

- Bevestigd: Delete/Backspace (⌫), niet de backslash-toets.
- Klik een bestaande score-note en verwijder hem met ⌫; Command+Z haalt hem terug.
- In het tekstveld blijft ⌫ gewone tekstbewerking. Bij een bestaande note staat ook Delete naast Cancel.


## 58. Snel wisselen tussen cues en takes — voorstel, nog niet ingevoerd

- Aandachtspunt: Alt+1–9 kiest nu de volgorde in de cuelijst, niet de cuecode. Alt+1 = 1M02 Arrival; Alt+2 = 1M18 Calling Harry. Dat kan verwarren, zeker na herordenen.
- De huidige sneltoetsen werken alleen in Recording, buiten tekstinvoer. Cuewisseling blijft geblokkeerd bij een lopende take.
- Voorstel voor dezelfde bediening in Recording en Cut list:
  - ⌥1–9: direct Take 1–9 binnen de gekozen cue, op werkelijk take-nummer in plaats van zichtbare rijpositie. Een ontbrekende take wordt niet aangemaakt.
  - ⌥[ / ⌥]: vorige/volgende bestaande take, ook voorbij Take 9.
  - [ / ]: vorige/volgende cue. De brackets voorlopig niet herbestemmen.
- Voorbeeld: ⌥1 → eerste twee maten selecteren met Command-drag → ⌥2 → andere maten kiezen → ] naar de volgende cue.
- Takekeuze verandert alleen de geselecteerde bewerkingslaag, nooit welke take loopt. Scorepositie, concepten en selecties per take behouden; tekstinvoer en open modale vensters krijgen voorrang. Toetsen tijdens een sleepsessie niet laten wisselen van take.
- Nog een voorstel: de huidige toetsen blijven ongewijzigd totdat Floris de indeling kiest. Gewone take-nummers en overdubnummers moeten bij eventuele uitwerking onderscheidbaar blijven.


## 59. Sneltoetsen gekozen en ingevoerd

- Alt is voor takes; zonder Alt wisselen brackets tussen cues, in Recording én Cut list.
- [ = vorige cue. ] = volgende cue. Alt+[ = vorige take. Alt+] = volgende take.
- Alt+1 t/m 9 kiest het echte take-nummer binnen deze cue; de oude cijferkeuze op cuevolgorde vervalt.
- Voor Take 12 of 34: Alt+Command indrukken, beide loslaten en twee cijfers typen. Een klein vast statusbericht toont Take __ en de ingevoerde cijfers.
- Escape, vijf seconden zonder invoer, klikken, focus verliezen of een andere actie annuleert. Een ontbrekende take wordt niet aangemaakt.
- Modifiers loslaten vóór de cijfers voorkomt dat Command-cijfers als browserbediening bedoeld raken. Tekstvelden houden normale invoer; niet navigeren tijdens slepen of vanuit modale vensters.
- Directe nummers kiezen gewone takes; brackets met Alt doorlopen de bestaande take-/overdublijst. Selectie, concepten en leespositie blijven behouden, en de lopende take blijft dezelfde.
- De open vraag uit punt 58 is hiermee beantwoord; de historische notitie over cuevolgorde blijft bewaard.


## 60. Metadata tijdens het schrijven

- Maat en tijdcode vóór Enter gebruiken dezelfde bediening als bij een geplaatste note.
- Bar opent hetzelfde zwevende, scrollbare menu met All en direct typen plus Enter.
- Tijdcode aanklikken, aanpassen en Enter; klokje herstelt het oorspronkelijke typmoment. Enter in metadata plaatst de note nog niet.


## 61. Voorstelbalk weer bovenaan, los van de GUI

- Nieuwste keuze: voorstelnaam, Rondleiding, Vragen en Claude-prompt compact bovenaan in een eigen balk.
- Deze reviewbediening hoort niet bij de voorgestelde opname-GUI; ook in Cut list staat die apart.
- De rondleiding blijft een verzameling vrijblijvende ideeën, zonder oordeel over het bestaande programma.


## 62. Brackets ingedrukt houden

- Eén druk blijft één cue of take. Ingedrukt houden herhaalt de navigatie en versnelt na kort vasthouden.
- Alt blijft takes betekenen, zonder Alt cues. In tekstvelden blijven brackets tekst; cijfer- en opnameacties herhalen niet.


## 63. Bestaande app herkenbaar houden

- Zijbalk met MandoCues, Dashboard, Cues, Sessions, Recording, Tasks, Stats, Settings en accountcontext.
- Sessiekeuze, Session length in minuten met uren ernaast, Prep per cue, Max music in minuten, Add cues, Chat en PDF zichtbaar behouden.
- Chat standaard dicht; lokale proefberichten. PDF toont Recording order of Take sheet en kan via de browser worden afgedrukt.
- Inspectie-HTML is een gerenderde momentopname, geen volledige JavaScriptbron. Max music heeft daar het aria-label Maximum minutes of music.
- Nieuwe cues zonder meegeleverde score tonen No score linked; geen verzonnen partituur.


## 64. Cuebediening en opnamestatus

- Vorige/volgende cue staan als pijlen bij de cuenaam, met kleine bracket-hints. Overdub blijft bij de takebediening.
- Break krijgt een koffie-icoon. Standby zegt expliciet Not recording; alleen een lopende take toont de rode Recording-status.
- Cut list toont een lopende take-tijd, kloktijd en Expected end. Bij een gestopte take staat de vastgelegde duur.
- Music length is de muziekduur van de cue in minuten:seconden; Planned work is werktijd in expliciete minuten. Demo-planning is geen productiebeleid.


## 65. Rondleiding voor de collega redigeren

- Begin bij Recording en sessiestart, daarna cue → take → notes → beoordeling. Sneltoetsen na de basis.
- In Cut list eerst score en take kiezen, dan maten selecteren en notes maken; vergelijken en instellingen volgen later.
- Formuleer als vrijblijvende ideeën voor de collega, met korte aanwijzingen om te proberen. Geen uitleg over tussentijdse fixes of onze ontwerphistorie.
- Kloktijd onderscheiden van take-duur. Details zoals twee cijfers invoeren en het tijdcode-resetknopje blijven in de bediening en implementatieprompt, zonder de rondleiding te belasten.
- Bestaande suggestie-ID’s en opgeslagen promptkeuzes blijven behouden.


## 66. PDF-zoom globaal

- De gekozen zoom/schaal blijft gelijk bij wisselen tussen cues.
- Geen afzonderlijke zoomstand per cue, take of scorebron herstellen. Alleen zelf zoomen of Fit width gebruiken verandert de schaal.
- Dit is gewoon gedrag van de werkruimte; geen extra uitleg over de fix in de rondleiding.


## 67. Cue-navigatie stopt bij de grens

- [ op de eerste cue blijft daar; ] op de laatste cue blijft daar. Geen sprong van 1M02 naar 1M05 of andersom.
- Hetzelfde geldt bij ingedrukt houden, in Recording en Cut list. De cuepijlen volgen dezelfde grenzen.


## 68. Recording als één doorlopende pagina

- De Recording-kop en sessie-instellingen scrollen mee met de bediening, tijdlijn, cues en notes.
- Geen apart scrollvenster onder de vaste kop en geen kader in een kader. Gebruik ruimte en scheidingslijnen.
- De compacte opnamebediening blijft bereikbaar zodra de grote knop wegscrollt. De grote doorlopende scoreweergave blijft behouden.


## 69. Cueknoppen onder de cuenaam

- Previous cue en Next cue naast elkaar op een vaste rij onder de cuenaam.
- Hun positie hangt niet af van de lengte van de cuenaam. Brackets en de grenzen aan begin/einde blijven behouden.


## 70. Duidelijkere lopende take

- Alleen een duidelijkere opnamestatus; geen rood schermkader.
- Een duidelijk leesbare rode Recording-badge in grote en compacte bediening. Markeer ook de lopende take bij takes/notes.
- Een andere take selecteren mag de zichtbaarheid van de lopende take niet wegnemen of een gestopte take als lopend tonen.


## 71. Klok groter en voor-/achterstand compacter

- Time groter. Expected end voorlopig weg; plaats voor-/achterstand bij of onder de klok.
- Alleen het teken en de tijd: − voor achterstand, + voor voorsprong; geen zichtbare behind/ahead-tekst.
- Achterstand onder vijf minuten oranje, vanaf vijf minuten rood (grens bevestigd). Voorsprong groen, nul neutraal.
- Cue time is de bestede werktijd per cue; de geplande minuten zijn het werkbudget per cue. De demo gebruikt vaste voorbeeldwaarden uit de eerdere weergave; behoud bestaande productieberekeningen.


## 72. Oorspronkelijke cuegegevens behouden

- Complexity, Planned en Actual horen ook in onze weergave bij iedere cue. Behoud de muziekduur.
- Planned is geplande werktijd in minuten, Actual de werkelijk bestede werktijd per cue (niet alleen take-duur).
- Voeg het handmatige afvinkvakje voor een afgeronde cue terug toe. Afgerond en geselecteerd blijven aparte statussen.
- Geen nieuwe workflow nodig waar de oorspronkelijke site dit al goed deed; takes blijven inklapbaar onder de cue en notes blijven behouden.


## 73. Tijdcode volledig zichtbaar

- Het laatste cijfer van het tijdcodeveld bij notes werd afgeknipt.
- Houd alle cijfers zichtbaar in concepten en geplaatste notes, ook bij langere tijdcodes en tijdens bewerken.
- Het klokje en maatnummer mogen de tekst niet overlappen. Dit is een weergavefix, geen extra uitleg voor de rondleiding.


## 74. Klokje neemt de huidige tijdcode over

- Klikken op het klokje werkt de tijdcode bij naar de huidige positie van die take. Niet terug naar het moment waarop je begon te typen.
- Dit werkt tijdens typen en bij een geplaatste note. Opnieuw klikken gebruikt opnieuw het actuele moment.
- Enter plaatst de note en zet een nieuwe klaar met een nieuw tijdanker. Maat en tekst blijven behouden bij het bijwerken van de tijdcode.
- Bij een andere geselecteerde take hoort het klokje bij die take, niet bij een andere lopende opname.


## 75. Alt zonder volgnummers

- De knop heet altijd Alt; geen Alt 1, Alt 2 enzovoort.
- Toon alleen het totale aantal Alt-takes per cue, ook nul. Highlight en knopposities blijven behouden.


## 76. Naam Comp tool

- De score-/kniplijstweergave heet voortaan Comp tool.
- Bestaande links blijven werken; wijzig alleen de naam in de GUI en actuele uitleg.


## 77. Paginaweergave zoals Preview

- Twee scorepagina’s naast elkaar kunnen tonen.
- Een compact menu met Continuous scroll, Single page en Two pages.
- Verder uitzoomen, tot 10%; knijpzoom en Fit width blijven werken.
- Pagina-indeling en zoom blijven globaal bij wisselen van cue of take.


## 78. Overlap en kleurcontrast in Comp tool

- Overlappende selecties blijven afzonderlijk per take bewaard; toevoegen of verwijderen in één take verandert de andere niet.
- Laat overlap zichtbaar in beide kleuren met arcering en aparte kleurstrepen, ook wanneer één take alleen als achtergrondreferentie zichtbaar is.
- Verhoog het contrast van geselecteerde en achtergrondmaten. Muziek en notes blijven leesbaar.


## 79. Rondleiding met bruikbare voorbeelden

- Verwijder de algemene indelingszin en de oude suggestie 9 (Losse notes per take).
- Noem [ en ] bij direct een cue kiezen.
- Vul de eerste drie voorbeeldcues met takes en notes. Een take-suggestie opent bij een lege cue een gevuld voorbeeld, zonder tijdens de rondleiding takes aan te maken.
- Vermeld Command+Option+slepen naast Command+rechtsklik voor verwijderen van maatselecties.


## 80. Twee indelingen om het hoofdpaneel te beoordelen

- A: cue/take links, grote klok midden, sessiegegevens en bediening rechts.
- B: klok boven cue/take, sessiegegevens en bediening rechts. Geen definitieve keuze: beide delen dezelfde state en functies.
- Cue en take prominent; lopende opname rood en duidelijk herkenbaar.
- Geen apart Session details-vak: instellingen en overige sessietijden compact bij elkaar.
- Planned gebruikt een zwevende scrolllijst met minuten en directe invoer via Enter, ook in de cuelijst.
- De Alt-knop is smaller en behoudt een vaste breedte.


## 81. Kloktijd bij notes

- Geen relatieve take-, sessie- of projecttijdcodes meer bij notes.
- Gebruik de echte kloktijd in 24-uursnotatie, met datum als UTC-instant bewaard voor latere synchronisatie.
- Vastleggen bij de eerste letter. Ook na het wissen van alle tekst blijft die kloktijd staan; alleen het klokje zet hem op nu. Enter maakt na plaatsen een nieuw concept klaar.
- Klikken en Enter past de tijd aan; het klokje vult de actuele kloktijd in. De maat blijft handmatig.
- De demo bevat geen koppeling met Pro Tools of andere DAW.


## 82. Gebruikelijke Mac-selectie voor vergelijken

- Command+klik kiest losse takes. Shift+klik kiest de reeks vanaf het laatste klikanker.
- Command+Shift+klik voegt een reeks toe. Gewone klik kiest alleen die take.
- De aangeklikte take is bewerkbaar; opname, notes, maatselecties en leespositie blijven behouden.


## 83. Bestaande automatische planning behouden

- Bewaar alle 26 zichtbare Planned-waarden uit de aangeleverde momentopname.
- Een handmatige minutenkeuze blijft een override; leegmaken of Auto kiezen schakelt terug naar een automatische schatting.
- Auto reageert op sessieduur, voorbereiding, muziekduur en Complexity. Een handmatige override blijft staan.
- De lokale schatting volgt de zichtbare uitleg (voorbereiding + gewogen aandeel), geen geverifieerde kopie van de productieplanner. Behoud bij echte implementatie de bestaande logica en opslag.


## 84. Bestaande take-labels behouden

- Een eigen label per take/overdub, bewerkbaar in Recording en Comp tool (ook All takes).
- Labels delen dezelfde take-ID, blijven bij wisselen behouden en staan op het take sheet.
- Sterren, Best en Alt blijven op vaste posities.


## 85. Bestaande take verwijderen behouden

- Verwijderknop bij de take in Recording, Comp tool en All takes. Bevestigen verwijdert ook de eigen notes en maatselecties.
- Een lopende take is beschermd. Overige takes, cuewerktijd en planning blijven behouden.
- Overgebleven takes worden niet hernummerd; nieuwe takes hergebruiken geen verwijderd nummer.


## 86. Terug naar de oorspronkelijke opbouw; tijden verduidelijken

- De keuze voor de nieuwe A is ingetrokken. Neem de oorspronkelijke verhoudingen, grote cue en herkenbare opnamestatus als basis.
- Een nieuwe sessie begint met nul sessie- en cuewerktijd, niet met de oude voorbeeldstanden 42:00 en 08:00.
- Music length is muziekduur; Planned de gereserveerde werktijd; Actual/Worked on cue de cumulatieve werktijd inclusief tijd tussen takes; Take duration de afzonderlijke take.
- Een lokale forecast gebruikt ongebruikte geplande cuetijd, afgeronde cues en pauzetijd. Dit is geen geverifieerde kopie van de productieplanner.


## 87. Oorspronkelijke verhoudingen, minder klokken in beeld

- Eén hoofdvak met grote cue links, klok in AM/PM rechts en groen/oranje/rood planningsvlak.
- Recording met icoon en After Party eenmaal; viewkeuze midden. Opnamedag eronder, zonder zichtbaar Session-prefix.
- Neem de rode rand, gloed en globale Recording-melding over tijdens een lopende take.
- Planning bij de titel bevat de geplande eindtijd, invulvelden en secundaire klokken. A toont de velden bovenaan, B plaatst ze in het menu; voorlopig B.
- Finish by is de geplande eindtijd, Projected end is berekend. +15/+30/+60 verlengt voorlopig het geplande einde; keuze achteraf laten beoordelen.
- De rondleiding vraagt kort welke oorspronkelijke klokken tijdens een sessie nodig zijn, vanuit Floris. Geen lange uitleg.
- De eerste dag heeft voorbeeldtakes; de tweede dag is expliciet een aparte demosessie. Notes, takes, planning en chat blijven per dag gescheiden. Tijdens een take is dagwisseling geblokkeerd; een gestarte sessie blijft tijdens bekijken van een andere dag doortellen.
- Nieuwe vragen pas na afloop, met de voorlopig gekozen optie erbij.


## 88. Takes achteraf terugkoppelen aan Pro Tools

- Onderzoek eerst welke datum-/tijdmetadata Pro Tools bewaart; Original Time Stamp is niet vanzelf de echte kloktijd.
- Voeg een korte vrijblijvende suggestie toe aan de rondleiding: onze Take 3 kan bij de engineer Take 4 zijn. Koppelen via gecontroleerde kloktijden, zonder hernummeren.
- BWF heeft OriginationDate/OriginationTime; daadwerkelijk schrijfgedrag in de gebruikte Pro Tools-versie nog met originele WAVs controleren. Houd rekening met klokverschil, datum, QuickPunch en meerdere kanalen.
- Nieuwe demo-takes/overdubs bewaren aparte lokale start-/stopinstants, tijdzone, sessie/cue en log-ID. Geen tijd verzinnen voor voorbeeldtakes. Take sheet kan een JSON-log downloaden; demo-opslag blijft vluchtig en is geen DAW-bevestiging.
- Technische aanpak, bronnen en praktijktest staan in Pro-Tools-takekoppeling.md. Voorlopig kandidaten voorstellen en handmatig bevestigen; geen automatische audio- of maatsynchronisatie.


## 89. AM/PM behouden

- Kloktijden met AM/PM zoals in het origineel, ook bij notes en in het take sheet. Geen voorstel meer voor overal 24-uursweergave.
- Bewaar UTC-instants en datum ongewijzigd; dit gaat over weergave en invoer. Duurvelden blijven minuten/seconden.
- Note-tijden accepteren AM/PM, inclusief 12 AM (middernacht) en 12 PM (middag). De bestaande 24-uursinvoer blijft als invoergemak geaccepteerd en wordt met AM/PM getoond.
