# MandoCues · voorstel van Floris

Eén werkruimte met Recording en Cut list. Bij openen kies je Rondleiding starten of Zelf bekijken. De rondleiding toont één suggestie tegelijk; een checkbox bepaalt of die tekst meegaat naar Claude. De app werkt los van deze keuze.

Alle daadwerkelijke GUI-tekst is Engels. Uitleg en vragen blijven Nederlands. Het zijn vrijblijvende ideeën; jouw programma en ontwerpkeuzes gaan voor.

## Vragen

- Waarvoor gebruiken we de duur van elke take?
- Zou ‘New take’ maken en selecteren ook werken, zonder start/stop?
- Wat gebeurt er met de sessietimers als je vergeet een take te starten?
- Welke timers hebben we tijdens de sessie echt nodig?
- Is alleen de voor-/achterstand genoeg, bijvoorbeeld ‘1:20 behind’ of ‘+01:20’?
- Welke tijd gebruiken we bij notes: film, take, sessie of kloktijd? Zullen we één vaste bron kiezen?

## De rondleiding

De onderstaande tekstonderdelen worden alleen samengevoegd als ze zijn aangevinkt. Er wordt geen nieuwe prompt gegenereerd.

### 1. Sterren in plaats van Good / NG / Hold

Beoordeel takes met 1–5 sterren. Filter bijvoorbeeld op 4–5 sterren.

**Promptonderdeel:**

Vervang de Good / NG / Hold-beoordeling door 1 tot en met 5 klikbare sterren per take. Bewaar de numerieke beoordeling bij de juiste take. Een nieuwe take mag nog onbeoordeeld zijn. Behoud een eventuele Beste-markering als afzonderlijke keuze. Aanvulling: filter bijvoorbeeld op 4–5 sterren. Filter alleen de weergave; verwijder of hernummer geen takes.

### 2. Een cue direct aanklikken

Kies een cue direct in de lijst, zonder Go to cue.

**Promptonderdeel:**

Laat een klik op cuenummer of titel direct die cue kiezen, zonder Go to cue te hoeven gebruiken. Houd cuekeuze los van het pijltje om takes in te klappen. Bewaar concepten en blokkeer cuewisseling zolang een take loopt met een duidelijke melding. Stop of verplaats een take niet impliciet.

### 3. Takes herkenbaar onder hun cue

Takes staan onder hun cue. Met het pijltje klap je ze in of uit.

**Promptonderdeel:**

Maak de relatie cue → takes zichtbaar met ingesprongen, even hoge take-regels. Een apart cuepijltje klapt die regels in of uit. Houd sterren, Best en Alt op vaste posities; selecteren maakt geen grotere editor in de regel. Bewaar concepten en beoordelingen bij inklappen. De geselecteerde take en de werkelijk lopende take blijven herkenbaar en onafhankelijk.

### 4. Enter plaatst een losse note

Typ een opmerking en druk Enter voor een losse note. Shift+Enter maakt een nieuwe regel.

**Promptonderdeel:**

Maak van een niet-lege ingevoerde opmerking met Enter een losse bulletnotitie bij de juiste cue en take. Houd de lege invoer klaar voor de volgende note; Shift+Enter maakt een nieuwe regel. Verstuur niet tijdens IME-compositie. Bewaar concepten per take. Cue-algemene opmerkingen blijven apart. Zorg dat notes ook bij de hoofd bediening zichtbaar moeten zijn, zodat je niet naar beneden hoeft te scrollen om te schrijven.

### 5. Tijd en maat als aanpasbaar voorstel

Automatisch tijdcode en waar mogelijk een maatnummer bij je note. Beide kun je na Enter aanpassen.

**Promptonderdeel:**

Zou het handig zijn om bij het schrijven van een note automatisch de relevante tijdcode en, waar een betrouwbare scorekoppeling bestaat, het maatnummer mee te geven? Bewaar het moment bij beginnen met typen; Enter plaatst de note. Beide waarden blijven daarna aanpasbaar of weg te laten. Kies voor de tijdcode samen één relevante bron: film, take, sessie of kloktijd. Dit is nog een open keuze, geen opdracht om al die bronnen tegelijk te implementeren. Laat een klik op het maatcijfer direct een verticale lijst en een invoerveld openen. Overschrijf handmatige correcties niet automatisch. Zonder betrouwbare koppeling geen verzonnen automatisch maatnummer; een PDF alleen is daarvoor onvoldoende.

### 6. Eén plek om notes te schrijven

Alle notes van de gekozen take op één plek. Algemene cue-notes staan apart.

**Promptonderdeel:**

Toon naast vaste cue-/take-regels één apart notitiepaneel voor de gekozen take. Toon alle notes zonder eigen intern scrollvak. Cue-algemene notes staan apart en zijn inklapbaar. Bewaar concepten per take. Een oudere take bekijken stopt of hernoemt de lopende take niet; toon duidelijk welke take wordt bekeken en welke werkelijk loopt.

### 7. Spatie is ook nodig voor tekst

Spatie heb je nodig voor notes. Voorstel: ⌘ Enter om een take te starten of stoppen.

**Promptonderdeel:**

Starten en stoppen met de spatiebalk kan botsen met het typen van notes, omdat je spatie ook voor tekst nodig hebt. Voorstel voor onze Mac-workflow: gebruik Command+Enter om een take te starten en dezelfde combinatie om de lopende take te stoppen, ook tijdens typen. Spatie blijft gewone tekst en standaard browserbediening. Gewoon Enter plaatst een note. Een ingedrukte of herhalende toets mag niet meerdere keren schakelen; negeer IME-compositie. Bewaar concepten, tijdankers en leespositie bij start/stop. De stopknop blijft apart en bereikbaar. Dit is een voorstel voor de toetskeuze; behoud andere bestaande workflows.

### 8. Stoppen zonder terug te scrollen

Een compacte start/stopbalk blijft bereikbaar als je naar beneden scrolt.

**Promptonderdeel:**

Behoud de opnamebediening boven de cue-/takelijst. Zodra die buiten de interne scrollweergave valt, neemt een compacte vaste balk de cue, lopende take en start/stop over. Houd deze bediening buiten de note-editor, gescheiden van Add/Delete. Voorkom dubbel zichtbare of knipperende stopknoppen en behoud concept, tijdanker en scrollpositie bij stoppen.

### 9. Overal dezelfde kloknotatie

De grote klok en take-tijden allebei in 24-uursnotatie, bijvoorbeeld 19:54:59.

**Promptonderdeel:**

Onder de takes staat de tijd in 24-uursnotatie, terwijl de grote klok AM/PM gebruikt. Zullen we dat gelijk trekken, bijvoorbeeld overal 19:54:59?

### 10. Een favoriete take en alternatieven

Eén Best per cue; genummerde Alt-labels voor reservetakes.

**Promptonderdeel:**

Aanvulling: voeg een onafhankelijke Alt-toggle toe voor één of meer reservetakes. Maak Beste een toggle met maximaal één Beste per cue; een nieuwe Beste heft de vorige binnen die cue op. Sterren blijven apart. Bewaar alles bij de vaste take-ID. Nummer Alt-takes per cue in take-volgorde als Alt 1, Alt 2 enzovoort, onafhankelijk van het sterrenfilter. Toon het totale aantal alts bij de cue; zonder alts staat er een streepje. Niet-geselecteerde Alt-knoppen tonen Alt –. Houd de knopbreedte gelijk zodat sterren niet verschuiven. Bij verwijderen wordt de nummering opnieuw aaneengesloten. Beste verandert alleen de highlight: geen vinkje of wisselende Beste-tekst in de cuekop. Reserveer een vaste breedte voor Beste en Alt in alle toestanden; sterren, cuegegevens en omliggende tekst blijven op dezelfde plaats bij aan- en uitzetten.

### 11. Veelgebruikte notes sneller invullen

Kies bijvoorbeeld Intonation of More expressive en pas de tekst zo nodig aan.

**Promptonderdeel:**

Aanvulling: bied veelvoorkomende notities als aanpasbare suggesties aan, bijvoorbeeld Intonatie, Meer expressief, Minder expressief, Strak en Alt take. Een klik vult het concept bij de juiste take; daarna kun je aanpassen en Enter drukken. Bewaar bestaand concept en leg het bedoelde moment bij de eerste invoer vast.

### 12. Duidelijke labels en knoppen

Aparte bediening voor Take, Cue en Session, met duidelijke namen voor de tijden.

**Promptonderdeel:**

Verduidelijk de benamingen voor Max music, muziekduur, complexiteit, geplande werktijd en tijd op deze cue. Gebruik bijvoorbeeld Maximale muziekduur (min), Muziekduur, Complexiteit, Geplande werktijd en Aan deze cue gewerkt. Toon voor/achter met een expliciet teken en tekst, niet alleen Behind. Scheid Take Controls, Cue Controls en Session Controls zichtbaar. Houd cuecodes in het sessieplan leesbaar zonder afkapping.

### 13. Snel naar een andere cue

Met [ en ] naar de vorige/volgende cue. Met ⌥ 1–9 direct een cue kiezen.

**Promptonderdeel:**

Gebruik [ en ] voor vorige/volgende cue voor en een modifier om direct naar bijvoorbeeld cue 8 te springen. In deze proef gebruikt de bedieningsdemo Alt+1–9 buiten tekstinvoer. Maak de uiteindelijke toetsen configureerbaar en controleer browser-/systeemconflicten. Typen in notes krijgt voorrang; een actieve take wisselt niet stilzwijgend van cue.

### 14. Het sessieplan blijft een tijdlijn

Langere blokken betekenen meer geplande opnametijd.

**Promptonderdeel:**

Behoud het sessieplan als één horizontale tijdlijn, met bloklengtes evenredig aan de geplande cuetijd. Houd volledige cuecodes leesbaar en laat horizontaal scrollen waar nodig. Een klik kiest de cue met dezelfde bestaande veiligheidsregels; wissel niet stilzwijgend tijdens een lopende take.

### 15. Voor- of achterlopen in één oogopslag

Eén status voor voor-/achterlopen, bijvoorbeeld +02:00 behind. Extra tijden staan onder Session details.

**Promptonderdeel:**

Toon één beknopte voor-/achterstand met expliciet teken en ahead/behind, ondersteund door kleur. Houd aanvullende sessietimers onder Session details. Hergebruik de bestaande planning en klokken; een voorbeeldberekening is geen bewezen voorspelling uit echte takes. Het nut van de take-timer en de definitieve tijdcodebron blijven aparte open vragen.

### 16. Opname en kniplijst in één werkruimte

Wissel tussen de opnameweergave en de partituur om je kniplijst te maken.

**Promptonderdeel:**

Maak één werkruimte met Recording en Cut list als twee weergaven van dezelfde cue-, take-, rating-, note- en opname-state. Neem de gekozen opname-indeling met bediening bovenaan en compacte balk bij scrollen als basis; hergebruik de bestaande kniplijst. Wisselen mag een lopende take, concepten, scoreselecties of leespositie niet verliezen of stilzwijgend kopiëren. Maak geen onafhankelijke demo-state per weergave.

### 17. De partituur bij deze cue

Kies een cue en zie de bijbehorende partituur rechts.

**Promptonderdeel:**

Koppel de actieve cue aan zijn bestaande scorebron en PDF-pagina’s. Toon de partituur groot rechts met takes en notes links. Gebruik de bestaande gevalideerde maat-/instrumentmapping waar aanwezig en label benaderingen. Een eigen PDF krijgt niet vanzelf mapping. Wijzig het bron-PDF niet en behoud aparte takegegevens voor cues die dezelfde scorepagina’s delen.

### 18. Een eigen scorelaag per take

Kies een take om zijn notes en kniplijst te zien. Een nieuwe take begint met een lege scorelaag.

**Promptonderdeel:**

Bewaar kniplijstselecties, score-notes, concepten en leespositie per vaste take-ID én scorebronversie. Een nieuwe take heeft een lege eigen laag. Terugklikken herstelt de juiste gegevens zonder de score onverwacht te verschuiven. Deel deze gegevens met de opnameweergave; de geselecteerde take mag verschillen van de lopende take.

### 19. Bruikbare maten markeren

⌘+linksklik of slepen voegt maten toe. ⌘+rechtsklik verwijdert ze.

**Promptonderdeel:**

Hergebruik de bestaande kniplijstselectie op maatvakken. Command+linksklik of slepen voegt toe en Command+rechtsklik of Command+Option+linksslepen verwijdert. Link instruments staat standaard aan: alle instrumenten van de geraakte maten. Uit selecteert de geraakte instrumenten. Opnieuw koppelen herschrijft bestaande selecties niet. Voorkom het browsercontextmenu tijdens verwijderen. Selectie is per take en bron, geen audio-edit.

### 20. Takes vergelijken op dezelfde score

⌘+klik op meerdere takes om hun selecties en notes samen op de score te zien.

**Promptonderdeel:**

Gewone klik kiest één take; Command+klik schakelt extra takes in of uit voor vergelijking, met minimaal één geselecteerde take. De laatst toegevoegde is bewerkbaar. Houd vaste takekleuren en leespositie; toon expliciete vergelijkingen duidelijker dan achtergrondreferenties. Vergelijken wijzigt geen opname, notes of opgeslagen selecties en neemt geen notes over in een nieuwe take.

### 21. Alle takes naast dezelfde maten

Bekijk de maatselecties van alle takes in één raster. Klik een maat om naar de score te gaan.

**Promptonderdeel:**

Behoud de bestaande PDF/All takes-schakelaar. Toon in All takes één gedeelde horizontale maat-as met een rij per take, vaste takekleuren, Best/Alt en note-indicatoren. Deel de bestaande selectie-state. Klik op een maat opent die take op de juiste scoreplek; een notestip toont de notes daar. Bij ontkoppelde instrumenten kunnen instrumentrijen uitklappen. Bewaar horizontale en verticale leespositie bij bewerken.

### 22. Instrumenten en referenties aan of uit

Ketting: alle instrumenten samen selecteren. Oog: selecties van andere takes als referentie tonen.

**Promptonderdeel:**

Behoud Link instruments en See other takes als compacte, benoemde instellingen boven de partituur. Beide beginnen aan. Link instruments bepaalt alleen nieuwe selecties en herschrijft geen eerdere gedeeltelijke selecties. See other takes verbergt alleen achtergrondreferenties; expliciet gekozen vergelijkingstakes en hun notes blijven zichtbaar. Bewaar instellingen bij wisselen van weergave.

### 23. Notes als tekst op de score

Dubbelklik voor een note bij een maat en instrument. Notes voor alle instrumenten staan bovenaan.

**Promptonderdeel:**

Dubbelklik op de bestaande scoremapping opent een note-editor bij de gekozen maat en instrument. Enter plaatst kale tekst; Shift+Enter maakt een regel en Escape annuleert. Standaard boven de betreffende notenbalk; All instruments boven de bovenste balk bij die maat binnen deze take. Bewaar maat, instrument, pagina, take en bron als metadata. Geen achtergrondkaart of badges op de PDF. Bied handmatige plaatsingscorrectie; beloof geen volledige notatie-engine.

### 24. Terugvinden, aanpassen en verplaatsen

Klik op een note om naar zijn plek te gaan. Sleep de tekst op de score om hem te verplaatsen.

**Promptonderdeel:**

Behoud de compacte score-noteslijst met Bar, Note en Time. Klikken op note-tekst navigeert naar de juiste scoreplek; het maatnummer blijft direct aanpasbaar. Geef aparte edit/delete-acties met duidelijke toegankelijkheidslabels. Klik op tekst in de score om te bewerken en sleep die om de positie te corrigeren. Houd take en bron correct, behoud concepten en maak bewerkingen ongedaan zonder andere takes te wijzigen.

### 25. Scorebewerkingen ongedaan maken

⌘ Z maakt de laatste bewerking ongedaan. ⌘ Shift Z voert hem opnieuw uit.

**Promptonderdeel:**

Behoud undo/redo voor toevoegen, verwijderen, aanpassen en verplaatsen van score-notes en maatselecties, per take en scorebron. Command+Z maakt ongedaan, Command+Shift+Z voert opnieuw uit. Onderschep geen normale tekst-undo binnen invoervelden. Andere takes en de oorspronkelijke PDF veranderen niet.

## Gedeelde promptinleiding

Geselecteerde suggesties van Floris voor mijn bestaande MandoCues-app. Implementeer alleen de onderstaande selectie. Bekijk eerst wat al bestaat en behoud mijn bestaande stijl, componenten, state en opslag. Mijn code, workflow en ontwerpkeuzes blijven leidend; dit is geen opdracht om mijn hele programma te vervangen.

Alle daadwerkelijke GUI-tekst is Engels, inclusief hints, tooltips, toegankelijkheidslabels en meldingen. Vragen en toelichting mogen Nederlands blijven. Vertaal geen oorspronkelijke cue-/projectnamen of eigen notes. De demo gebruikt voorbeelddata, neemt geen audio op en bewijst geen DAW-, film- of automatische scorekoppeling. De keuze van een tijdcodebron en het nut van take-timers zijn open vragen, geen impliciete implementatieopdracht.


## Gedeelde afsluiting

Stem gedeelde onderdelen op elkaar af. Voeg geen andere suggesties toe. Controleer de betrokken bestaande flows en vat kort samen wat is aangepast, getest en wat een echte bronkoppeling vereist.
