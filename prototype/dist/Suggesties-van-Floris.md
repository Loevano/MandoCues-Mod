# MandoCues · voorstel van Floris

Eén werkruimte met Recording en Cut list. Bij openen kies je Rondleiding starten of Zelf bekijken. De rondleiding toont één suggestie tegelijk; een checkbox bepaalt of die tekst meegaat naar Claude. De app werkt los van deze keuze.

Alle daadwerkelijke GUI-tekst is Engels. Uitleg en vragen blijven Nederlands. Het zijn vrijblijvende ideeën; jouw programma en ontwerpkeuzes gaan voor.

## Vragen

- Waarvoor gebruiken we de duur van elke take?
- Zou ‘New take’ maken en selecteren ook werken, zonder start/stop?
- Wat gebeurt er met de sessietimers als je vergeet een take te starten?
- Waarvoor gebruiken jullie de verschillende klokken tijdens een sessie?
- Is alleen de voor-/achterstand genoeg, bijvoorbeeld ‘1:20 behind’ of ‘+01:20’?
- Welke tijd gebruiken we bij notes: film, take, sessie of kloktijd? Zullen we één vaste bron kiezen?

## De rondleiding

De onderstaande tekstonderdelen worden alleen samengevoegd als ze zijn aangevinkt. Er wordt geen nieuwe prompt gegenereerd.

### 1. Het hoofdpaneel

Ik heb de bediening en de belangrijkste tijden bij elkaar gezet.

**Promptonderdeel:**

Verduidelijk de benamingen voor Max music, muziekduur, complexiteit, geplande werktijd en tijd op deze cue. Gebruik bijvoorbeeld Maximale muziekduur (min), Muziekduur, Complexiteit, Geplande werktijd en Aan deze cue gewerkt. Toon voor/achter met een expliciet teken en tekst, niet alleen Behind. Scheid Take Controls, Cue Controls en Session Controls zichtbaar. Houd cuecodes in het sessieplan leesbaar zonder afkapping. Houd Previous cue, Next cue, Overdub, Break en End session als zichtbare knoppen in het hoofdpaneel, gegroepeerd onder Take, Cue en Session. Verstop deze handelingen niet in Session details. Laat de bestaande sessie- en pauzeregels van de app leidend; de lokale demo bewijst die niet. Stop of verplaats een take niet impliciet bij een cuewissel of sessieactie.

### 2. Start de sessie met ⌘ Enter

Spatie heb je nodig voor notes. ⌘ Enter start de sessie; daarna start of stopt dezelfde toets een take.

**Promptonderdeel:**

Starten en stoppen met de spatiebalk kan botsen met het typen van notes, omdat je spatie ook voor tekst nodig hebt. Voorstel voor onze Mac-workflow: gebruik Command+Enter eerst voor Start session. Als de sessie loopt, start dezelfde combinatie een take of stopt de lopende take, ook tijdens typen. Sessiestart maakt nog geen take. De sneltoets moet direct na laden en tijdens de rondleiding werken, ook als het rondleidingstekstje de focus heeft; een handmatige klik in de app mag niet nodig zijn. In het welkomstscherm en andere modale uitleg-/promptvensters blijft opnamebediening geblokkeerd. Spatie blijft gewone tekst en standaard browserbediening. Gewoon Enter plaatst een note. Een ingedrukte of herhalende toets mag niet meerdere keren schakelen; negeer IME-compositie. Bewaar concepten, tijdankers en leespositie bij start/stop. De stopknop blijft apart en bereikbaar. Dit is een voorstel voor de toetskeuze; behoud andere bestaande workflows.

### 3. Voor- of achterlopen in één oogopslag

Cue-tijd, voor-/achterstand en verwachte eindtijd in één overzicht.

**Promptonderdeel:**

Houd in het hoofdpaneel de cue, muziekduur, geplande cuetijd, take-tijd, cue-tijd tegenover de planning, kloktijd en verwachte eindtijd zichtbaar. Toon één beknopte voor-/achterstand met expliciet teken en ahead/behind, ondersteund door kleur. Overige sessietijden blijven beschikbaar onder Session details. Haal geen bestaande klokken of functies weg; behoud hun bestaande berekening en bron. Het doel van de verschillende klokken blijft een open vraag. De demo is een presentatievoorstel; neem zijn voorbeeldberekening en pauzebeleid niet over als vervanging van bestaande planningslogica.

### 4. Overal dezelfde kloknotatie

De grote klok en take-tijden allebei in 24-uursnotatie, bijvoorbeeld 19:54:59.

**Promptonderdeel:**

Onder de takes staat de tijd in 24-uursnotatie, terwijl de grote klok AM/PM gebruikt. Zullen we dat gelijk trekken, bijvoorbeeld overal 19:54:59?

### 5. Het sessieplan blijft een tijdlijn

Langere blokken betekenen meer geplande opnametijd.

**Promptonderdeel:**

Behoud het sessieplan als één horizontale tijdlijn, met bloklengtes evenredig aan de geplande cuetijd. Houd volledige cuecodes leesbaar en laat horizontaal scrollen waar nodig. Een klik kiest de cue met dezelfde bestaande veiligheidsregels; wissel niet stilzwijgend tijdens een lopende take.

### 6. Een cue direct aanklikken

Klik verschillende cues. Het opnamepaneel en de takes wisselen mee.

**Promptonderdeel:**

Laat een klik op cuenummer of titel direct die cue kiezen, zonder Go to cue te hoeven gebruiken. Houd cuekeuze los van het pijltje om takes in te klappen. Bewaar concepten en blokkeer cuewisseling zolang een take loopt met een duidelijke melding. Stop of verplaats een take niet impliciet. Markeer alleen de gekozen cue duidelijk in de lijst: kleur de volledige cuekop en toon links een lichte accentlijn. Laat de markering meewisselen met de cuekeuze, ook tijdens de rondleiding. Houd de afzonderlijke take-selectie herkenbaar.

### 7. Snel naar een andere cue

Met [ en ] naar de vorige/volgende cue. Met ⌥ 1–9 direct een cue kiezen.

**Promptonderdeel:**

Gebruik [ en ] voor vorige/volgende cue voor en een modifier om direct naar bijvoorbeeld cue 8 te springen. In deze proef gebruikt de bedieningsdemo Alt+1–9 buiten tekstinvoer. Maak de uiteindelijke toetsen configureerbaar en controleer browser-/systeemconflicten. Typen in notes krijgt voorrang; een actieve take wisselt niet stilzwijgend van cue.

### 8. Takes herkenbaar onder hun cue

Takes staan onder hun cue. Met het pijltje klap je ze in of uit.

**Promptonderdeel:**

Maak de relatie cue → takes zichtbaar met ingesprongen, even hoge take-regels. Plaats take-labels rechts van het cuenummer met een subtiele verticale verbindingslijn. Behoud de bestaande takegrootte; maak het cuenummer minstens even prominent en groter dan het take-label. Een apart cuepijltje klapt die regels in of uit. Houd sterren, Best en Alt op vaste posities; selecteren maakt geen grotere editor in de regel. Bewaar concepten en beoordelingen bij inklappen. De geselecteerde take en de werkelijk lopende take blijven herkenbaar en onafhankelijk.

### 9. Sterren in plaats van Good / NG / Hold

Beoordeel takes met 1–5 sterren. Filter bijvoorbeeld op 4–5 sterren.

**Promptonderdeel:**

Vervang de Good / NG / Hold-beoordeling door 1 tot en met 5 klikbare sterren per take. Bewaar de numerieke beoordeling bij de juiste take. Een nieuwe take mag nog onbeoordeeld zijn. Behoud een eventuele Beste-markering als afzonderlijke keuze. Aanvulling: filter bijvoorbeeld op 4–5 sterren. Filter alleen de weergave; verwijder of hernummer geen takes.

### 10. Een favoriete take en alternatieven

Eén Best per cue; genummerde Alt-labels voor reservetakes.

**Promptonderdeel:**

Aanvulling: voeg een onafhankelijke Alt-toggle toe voor één of meer reservetakes. Maak Beste een toggle met maximaal één Beste per cue; een nieuwe Beste heft de vorige binnen die cue op. Sterren blijven apart. Bewaar alles bij de vaste take-ID. Nummer Alt-takes per cue in take-volgorde als Alt 1, Alt 2 enzovoort, onafhankelijk van het sterrenfilter. Toon het totale aantal alts bij de cue; zonder alts staat er een streepje. Niet-geselecteerde Alt-knoppen tonen Alt –. Houd de knopbreedte gelijk zodat sterren niet verschuiven. Bij verwijderen wordt de nummering opnieuw aaneengesloten. Beste verandert alleen de highlight: geen vinkje of wisselende Beste-tekst in de cuekop. Reserveer een vaste breedte voor Beste en Alt in alle toestanden; sterren, cuegegevens en omliggende tekst blijven op dezelfde plaats bij aan- en uitzetten.

### 11. Notes per take

Klik verschillende takes. Het paneel toont de notes van de gekozen take.

**Promptonderdeel:**

Toon naast vaste cue-/take-regels één apart notitiepaneel voor de gekozen take. Toon alle notes zonder eigen intern scrollvak. Cue-algemene notes staan apart en zijn inklapbaar. Bewaar concepten per take. Een oudere take bekijken stopt of hernoemt de lopende take niet; toon duidelijk welke take wordt bekeken en welke werkelijk loopt.

### 12. Enter plaatst een losse note

Typ een opmerking en druk Enter voor een losse note. Shift+Enter maakt een nieuwe regel.

**Promptonderdeel:**

Maak van een niet-lege ingevoerde opmerking met Enter een losse bulletnotitie bij de juiste cue en take. Houd de lege invoer klaar voor de volgende note; Shift+Enter maakt een nieuwe regel. Verstuur niet tijdens IME-compositie. Bewaar concepten per take. Cue-algemene opmerkingen blijven apart. Zorg dat notes ook bij de hoofd bediening zichtbaar moeten zijn, zodat je niet naar beneden hoeft te scrollen om te schrijven.

### 13. Maat en tijdcode direct aanpassen

Klik op maat of tijdcode om te wijzigen. Het klokje zet de oorspronkelijke tijdcode terug.

**Promptonderdeel:**

Voeg bij een note de tijdcode toe; bewaar het moment bij beginnen met typen als onveranderlijke oorspronkelijke tijdcode. Een klein klokje herstelt die waarde na een handmatige wijziging; gebruik niet de actuele afspeelpositie. Maatnummers worden voorlopig handmatig ingevuld of bewust in de partituur gekozen. Geen maat afleiden uit de take-timer. Een nieuwe take begint zonder maatnummer. Schrap de aparte Edit-knop bij notes. Klikken op Bar opent een scrollbaar menu met All (de hele take, zonder specifieke maat) en alle bekende maatnummers van de cue, met wat ruimte voor extra maten. Geef het invoerveld direct focus: typen en Enter kiest de maat. Geen Another bar-label of Choose bar-knop. De tijdcode is direct aanklikbaar en met Enter aanpasbaar; Escape annuleert. Bewaar de oorspronkelijke tijdcode ook bij andere note-bewerkingen en undo/redo. Delete blijft apart. Kies voor de tijdcode samen één relevante bron: film, take, sessie of kloktijd. Automatisch maatvolgen blijft een latere uitbreiding bij een betrouwbare koppeling met de uitvoering.

### 14. Veelgebruikte notes sneller invullen

Kies bijvoorbeeld Intonation of More expressive en pas de tekst zo nodig aan.

**Promptonderdeel:**

Aanvulling: bied veelvoorkomende notities als aanpasbare suggesties aan, bijvoorbeeld Intonatie, Meer expressief, Minder expressief, Strak en Alt take. Een klik vult het concept bij de juiste take; daarna kun je aanpassen en Enter drukken. Bewaar bestaand concept en leg het bedoelde moment bij de eerste invoer vast.

### 15. Stoppen zonder terug te scrollen

Een compacte start/stopbalk blijft bereikbaar als je naar beneden scrolt.

**Promptonderdeel:**

Behoud de opnamebediening boven de cue-/takelijst. Zodra die buiten de interne scrollweergave valt, neemt een compacte vaste balk de cue, lopende take en start/stop over. Houd deze bediening buiten de note-editor, gescheiden van Add/Delete. Voorkom dubbel zichtbare of knipperende stopknoppen en behoud concept, tijdanker en scrollpositie bij stoppen.

### 16. Opname en kniplijst in één werkruimte

Wissel tussen de opnameweergave en de partituur om je kniplijst te maken.

**Promptonderdeel:**

Maak één werkruimte met Recording en Cut list als twee weergaven van dezelfde cue-, take-, rating-, note- en opname-state. Neem de gekozen opname-indeling met bediening bovenaan en compacte balk bij scrollen als basis; hergebruik de bestaande kniplijst. Wisselen mag een lopende take, concepten, scoreselecties of leespositie niet verliezen of stilzwijgend kopiëren. Maak geen onafhankelijke demo-state per weergave.

### 17. De partituur bij deze cue

Kies een cue en zie de bijbehorende partituur rechts.

**Promptonderdeel:**

Koppel de actieve cue aan zijn bestaande scorebron en PDF-pagina’s. Toon de partituur groot rechts met takes en notes links. Gebruik de bestaande gevalideerde maat-/instrumentmapping waar aanwezig en label benaderingen. Een eigen PDF krijgt niet vanzelf mapping. Wijzig het bron-PDF niet en behoud aparte takegegevens voor cues die dezelfde scorepagina’s delen.

### 18. De partituur groot in beeld

Zoom met je trackpad of de knoppen. Fit width toont de volle breedte. Scroll door alle pagina’s.

**Promptonderdeel:**

Gebruik de beschikbare breedte en hoogte voor een grote, doorlopende partituur. Behoud de bestaande onafhankelijke scroll van de score en de take-/noteskolom: alle pagina’s van de cue staan onder elkaar. Houd de scoreweergave permanent groot. Combineer Recording/Cut list, cue/take, opnamestatus, take-tijd en start/stop in één compacte bovenbalk; laat de reviewbediening bereikbaar. Voeg Zoom in, Zoom out, een percentage en Fit width toe aan de compacte scoreknoppenrij. Behoud takes, notes, kniplijstselecties, vergelijkingen en leespositie bij zoomen, vergroten en takekeuze. Zoom schaalt score én hun annotatielagen samen; klik-/sleepcoördinaten blijven correct. Beperk horizontaal scrollen tot het scorevlak. Verplaats lange gebruiksuitleg uit de werkruimte naar de rondleiding; behoud de bestaande bediening en de oorspronkelijke PDF. Ondersteun ook trackpad-knijpzoom binnen het scorevlak (Chromium ctrl-wheel en Safari gesture-events), met het punt onder de vingers als anker. Gewoon scrollen blijft scrollen; de rest van de pagina zoomt niet mee.

### 19. Eigen notes en selecties per take

Klik een take om zijn notes en geselecteerde maten te zien. Een nieuwe take begint leeg.

**Promptonderdeel:**

Bewaar kniplijstselecties, score-notes, concepten en leespositie per vaste take-ID én scorebronversie. Een nieuwe take heeft een lege eigen laag. Terugklikken herstelt de juiste gegevens zonder de score onverwacht te verschuiven. Deel deze gegevens met de opnameweergave; de geselecteerde take mag verschillen van de lopende take.

### 20. Instrumenten koppelen en andere takes tonen

Ketting aan: selecteer alle instrumenten tegelijk. Oog aan: toon selecties van andere takes.

**Promptonderdeel:**

Behoud Link instruments en See other takes als compacte, benoemde instellingen boven de partituur. Beide beginnen aan. Link instruments bepaalt alleen nieuwe selecties en herschrijft geen eerdere gedeeltelijke selecties. See other takes verbergt alleen achtergrondreferenties; expliciet gekozen vergelijkingstakes en hun notes blijven zichtbaar. Bewaar instellingen bij wisselen van weergave.

### 21. Bruikbare maten markeren

⌘+linksklik of slepen voegt maten toe. ⌘+rechtsklik verwijdert ze.

**Promptonderdeel:**

Hergebruik de bestaande kniplijstselectie op maatvakken. Command+linksklik of slepen voegt toe en Command+rechtsklik of Command+Option+linksslepen verwijdert. Link instruments staat standaard aan: alle instrumenten van de geraakte maten. Uit selecteert de geraakte instrumenten. Opnieuw koppelen herschrijft bestaande selecties niet. Voorkom het browsercontextmenu tijdens verwijderen. Selectie is per take en bron, geen audio-edit.

### 22. Notes als tekst op de score

Dubbelklik voor een note bij een maat en instrument. Notes voor alle instrumenten staan bovenaan.

**Promptonderdeel:**

Dubbelklik op de bestaande scoremapping opent een note-editor bij de gekozen maat en instrument. Enter plaatst kale tekst; Shift+Enter maakt een regel en Escape annuleert. Standaard boven de betreffende notenbalk; All instruments boven de bovenste balk bij die maat binnen deze take. Bewaar maat, instrument, pagina, take en bron als metadata. Geen achtergrondkaart of badges op de PDF. Bied handmatige plaatsingscorrectie; beloof geen volledige notatie-engine. Gebruik de horizontale maatvakken ook voor dubbelklikken vlak boven de balken, zodat bijvoorbeeld boven maat 5 direct maat 5 gekozen wordt. Leid de instrumentcontext af uit de verticale positie: bij een balk voor dat instrument, boven de hele groep voor All instruments.

### 23. Notes terugvinden en verplaatsen

Klik links om een note terug te vinden. Sleep de tekst naar een andere maat; die licht op en wordt overgenomen.

**Promptonderdeel:**

Behoud de compacte score-noteslijst met Bar, Note en Time. Klikken op note-tekst navigeert naar de juiste scoreplek; het maatnummer blijft direct aanpasbaar. Behoud alleen de aparte Delete-actie. Maat en tijdcode zijn direct bij hun waarde bewerkbaar: een scrollbare matenlijst met All voor de hele take en nummers, typen plus Enter voor een maat, klikken en Enter voor de tijdcode. Een klein klokje herstelt de onveranderlijk opgeslagen oorspronkelijke tijdcode. Klik op tekst in de score om te bewerken en sleep die om de positie te corrigeren. Houd take en bron correct, behoud concepten en maak bewerkingen ongedaan zonder andere takes te wijzigen. Laat bij het slepen de doelmaat subtiel oplichten op basis van de bestaande scoremapping. Werk bij loslaten maatnummer, pagina/boekpagina en instrumentcontext bij zonder tijdcode, take of tekst te veranderen. Bewaar de gekozen vrije tekstpositie. Boven de volledige instrumentgroep wordt de context All instruments. Annuleren wijzigt niets; Command+Z herstelt positie én metadata.

### 24. Scorebewerkingen ongedaan maken

⌘ Z maakt de laatste bewerking ongedaan. ⌘ Shift Z voert hem opnieuw uit.

**Promptonderdeel:**

Behoud undo/redo voor toevoegen, verwijderen, aanpassen en verplaatsen van score-notes en maatselecties, per take en scorebron. Command+Z maakt ongedaan, Command+Shift+Z voert opnieuw uit. Onderschep geen normale tekst-undo binnen invoervelden. Andere takes en de oorspronkelijke PDF veranderen niet.

### 25. Takes vergelijken op dezelfde score

⌘+klik op meerdere takes om hun selecties en notes samen op de score te zien.

**Promptonderdeel:**

Gewone klik kiest één take; Command+klik schakelt extra takes in of uit voor vergelijking, met minimaal één geselecteerde take. De laatst toegevoegde is bewerkbaar. Houd vaste takekleuren en leespositie; toon expliciete vergelijkingen duidelijker dan achtergrondreferenties. Vergelijken wijzigt geen opname, notes of opgeslagen selecties en neemt geen notes over in een nieuwe take.

### 26. Alle takes per maat vergelijken

Bekijk welke maten je per take hebt geselecteerd. Klik een maat om die in de partituur te openen.

**Promptonderdeel:**

Behoud de bestaande PDF/All takes-schakelaar. Toon in All takes één gedeelde horizontale maat-as met een rij per take, vaste takekleuren, Best/Alt en note-indicatoren. Deel de bestaande selectie-state. Klik op een maat opent die take op de juiste scoreplek; een notestip toont de notes daar. Bij ontkoppelde instrumenten kunnen instrumentrijen uitklappen. Bewaar horizontale en verticale leespositie bij bewerken.

## Gedeelde promptinleiding

Geselecteerde suggesties van Floris voor mijn bestaande MandoCues-app. Implementeer alleen de onderstaande selectie. Bekijk eerst wat al bestaat en behoud mijn bestaande stijl, componenten, state en opslag. Mijn code, workflow en ontwerpkeuzes blijven leidend; dit is geen opdracht om mijn hele programma te vervangen.

Alle daadwerkelijke GUI-tekst is Engels, inclusief hints, tooltips, toegankelijkheidslabels en meldingen. Vragen en toelichting mogen Nederlands blijven. Vertaal geen oorspronkelijke cue-/projectnamen of eigen notes. De demo gebruikt voorbeelddata, neemt geen audio op en bewijst geen DAW-, film- of automatische scorekoppeling. De keuze van een tijdcodebron en het nut van take-timers zijn open vragen, geen impliciete implementatieopdracht.


## Gedeelde afsluiting

Stem gedeelde onderdelen op elkaar af. Voeg geen andere suggesties toe. Controleer de betrokken bestaande flows en vat kort samen wat is aangepast, getest en wat een echte bronkoppeling vereist.
