# MandoCues · voorstel van Floris

Eén werkruimte met Recording en Cut list. Bij openen kies je Rondleiding starten of Zelf bekijken. De rondleiding toont één suggestie tegelijk; een checkbox bepaalt of die tekst meegaat naar Claude. De app werkt los van deze keuze.

Alle daadwerkelijke GUI-tekst is Engels. Uitleg en vragen blijven Nederlands. Het zijn vrijblijvende ideeën; jouw programma en ontwerpkeuzes gaan voor.

## Vragen

- Waarvoor gebruiken we de duur van elke take?
- Zou ‘New take’ maken en selecteren ook werken, zonder start/stop?
- Wat gebeurt er met de sessietimers als je vergeet een take te starten?
- Waarvoor gebruiken jullie de verschillende klokken tijdens een sessie?
- Zou een klok met de voor-/achterstand genoeg overzicht geven tijdens de sessie?
- Welke tijd gebruiken we bij notes: film, take, sessie of kloktijd? Zullen we één vaste bron kiezen?

## De rondleiding

De onderstaande tekstonderdelen worden alleen samengevoegd als ze zijn aangevinkt. Er wordt geen nieuwe prompt gegenereerd.

### 1. Een mogelijke indeling voor Recording

Cuekeuze bij de cuenaam, takebediening bij elkaar. Zou deze indeling passen bij jullie sessies?

**Promptonderdeel:**

Verduidelijk de benamingen voor Max music, muziekduur, complexiteit, geplande werktijd en tijd op deze cue. Gebruik Engelse labels met eenheid: Session length (min), Prep per cue (min), Max music (min), Music length (minutes:seconds) en Planned work (min). Toon − voor achterstand en + voor voorsprong, zonder zichtbare ahead/behind-tekst. Gebruik oranje onder vijf minuten achterstand en rood vanaf vijf minuten; voorsprong groen en nul neutraal. Scheid Take Controls, Cue Controls en Session Controls zichtbaar. Houd cuecodes in het sessieplan leesbaar zonder afkapping. Houd Previous cue, Next cue, Overdub, Break en End session als zichtbare knoppen in het hoofdpaneel, gegroepeerd onder Take, Cue en Session. Verstop deze handelingen niet in Session details. Laat de bestaande sessie- en pauzeregels van de app leidend; de lokale demo bewijst die niet. Stop of verplaats een take niet impliciet bij een cuewissel of sessieactie. Houd de bestaande zijbalk, sessiekeuze, Add cues, inklapbare Chat en PDF-acties herkenbaar aanwezig. Plaats Previous cue en Next cue samen op een vaste rij onder de cuenaam, Overdub bij de takeknop en een koffie-icoon bij Break; toon subtiele bracket-hints. Maak Not recording en Recording duidelijk verschillend; alleen een lopende take krijgt de rode status. Gebruik een goed leesbare rode Recording-badge in de grote en compacte bediening en een duidelijke status bij de lopende take. Houd lopende en geselecteerde take gescheiden, ook bij scrollen en wisselen van weergave. Geen rood schermkader. Maak Time groter met de voor-/achterstand eronder. Laat Expected end voorlopig weg uit de hoofd- en compacte bediening, ook in Cut list; behoud take-tijd, kloktijd en planningsafwijking. De lokale planner is voorbeelddata; behoud de echte bestaande berekeningen.

### 2. ⌘ Enter voor start en stop?

Spatie gebruik je ook in notes. Voorstel: ⌘ Enter voor sessiestart en daarna start/stop van een take.

**Promptonderdeel:**

Starten en stoppen met de spatiebalk kan botsen met het typen van notes, omdat je spatie ook voor tekst nodig hebt. Voorstel voor onze Mac-workflow: gebruik Command+Enter eerst voor Start session. Als de sessie loopt, start dezelfde combinatie een take of stopt de lopende take, ook tijdens typen. Sessiestart maakt nog geen take. De sneltoets moet direct na laden en tijdens de rondleiding werken, ook als het rondleidingstekstje de focus heeft; een handmatige klik in de app mag niet nodig zijn. In het welkomstscherm en andere modale uitleg-/promptvensters blijft opnamebediening geblokkeerd. Spatie blijft gewone tekst en standaard browserbediening. Gewoon Enter plaatst een note. Een ingedrukte of herhalende toets mag niet meerdere keren schakelen; negeer IME-compositie. Bewaar concepten, tijdankers en leespositie bij start/stop. De stopknop blijft apart en bereikbaar. Dit is een voorstel voor de toetskeuze; behoud andere bestaande workflows.

### 3. De planning in één overzicht

Een grotere klok met de voor-/achterstand eronder. − is achter, + is voor. Zou dit genoeg overzicht geven?

**Promptonderdeel:**

Toon de kloktijd groter, met de sessieafwijking eronder; laat Expected end voorlopig uit de hoofd- en compacte bediening. Gebruik − voor achterstand, + voor voorsprong en 00:00 op schema, zonder zichtbare ahead/behind-tekst. Achterstand onder vijf minuten is oranje; vanaf vijf minuten rood. Voorsprong is groen en nul neutraal. Geef dezelfde betekenis in toegankelijke labels en tooltips en gebruik deze presentatie ook in Recording, de compacte scrollbalk en Cut list. Cue-tijd tegenover geplande werktijd en de take-tijd blijven beschikbaar; overige sessietijden blijven onder Session details. Behoud de bestaande planningsberekeningen en bron; de demo bevat voorbeelddata en bewijst geen productiebeleid.

### 4. Kloktijden in 24-uursnotatie

Zullen we kloktijden overal hetzelfde tonen, bijvoorbeeld 19:54?

**Promptonderdeel:**

Onder de takes staat de tijd in 24-uursnotatie, terwijl de grote klok AM/PM gebruikt. Zullen we dat gelijk trekken, bijvoorbeeld overal 19:54:59?

### 5. Leesbare cues in de tijdlijn

De bestaande tijdlijn, met leesbare cuecodes. Klik een blok om die cue te kiezen.

**Promptonderdeel:**

Behoud het sessieplan als één horizontale tijdlijn, met bloklengtes evenredig aan de geplande cuetijd. Houd volledige cuecodes leesbaar en laat horizontaal scrollen waar nodig. Een klik kiest de cue met dezelfde bestaande veiligheidsregels; wissel niet stilzwijgend tijdens een lopende take.

### 6. Een cue direct kiezen

Zou direct kiezen in de lijst handig zijn? Klik verschillende cues en bekijk hoe het paneel en de takes meewisselen.

**Promptonderdeel:**

Laat een klik op cuenummer of titel direct die cue kiezen, zonder Go to cue te hoeven gebruiken. Houd cuekeuze los van het pijltje om takes in te klappen. Bewaar concepten en blokkeer cuewisseling zolang een take loopt met een duidelijke melding. Stop of verplaats een take niet impliciet. Markeer alleen de gekozen cue duidelijk in de lijst: kleur de volledige cuekop en toon links een lichte accentlijn. Laat de markering meewisselen met de cuekeuze, ook tijdens de rondleiding. Houd de afzonderlijke take-selectie herkenbaar.

### 7. Takes onder hun cue

Cues als hoofdregel, met takes daaronder. Klap een cue open en kies een take.

**Promptonderdeel:**

Maak de relatie cue → takes zichtbaar met ingesprongen, even hoge take-regels. Plaats take-labels rechts van het cuenummer met een subtiele verticale verbindingslijn. Behoud de bestaande takegrootte; maak het cuenummer minstens even prominent en groter dan het take-label. Een apart cuepijltje klapt die regels in of uit. Houd sterren, Best en Alt op vaste posities; selecteren maakt geen grotere editor in de regel. Bewaar concepten en beoordelingen bij inklappen. De geselecteerde take en de werkelijk lopende take blijven herkenbaar en onafhankelijk.

### 8. Notes bij de gekozen take

Eén paneel voor de notes van de gekozen take. Klik verschillende takes om te zien hoe dat werkt.

**Promptonderdeel:**

Toon naast vaste cue-/take-regels één apart notitiepaneel voor de gekozen take. Toon alle notes zonder eigen intern scrollvak. Cue-algemene notes staan apart en zijn inklapbaar. Bewaar concepten per take. Een oudere take bekijken stopt of hernoemt de lopende take niet; toon duidelijk welke take wordt bekeken en welke werkelijk loopt.

### 9. Losse notes per take

Een opmerking per note, om ze apart terug te lezen. Typ iets en druk Enter; Shift+Enter maakt een nieuwe regel.

**Promptonderdeel:**

Maak van een niet-lege ingevoerde opmerking met Enter een losse bulletnotitie bij de juiste cue en take. Houd de lege invoer klaar voor de volgende note; Shift+Enter maakt een nieuwe regel. Verstuur niet tijdens IME-compositie. Bewaar concepten per take. Cue-algemene opmerkingen blijven apart. Zorg dat notes ook bij de hoofd bediening zichtbaar moeten zijn, zodat je niet naar beneden hoeft te scrollen om te schrijven.

### 10. Tijdcode en maat bij een note

Een tijdcode bij elke note; de maat kies je zelf. Klik de tijd of het maatnummer om die te wijzigen.

**Promptonderdeel:**

Voeg bij een note de tijdcode toe; bewaar het moment bij beginnen met typen als onveranderlijke oorspronkelijke tijdcode. Een klein klokje herstelt die waarde na een handmatige wijziging; gebruik niet de actuele afspeelpositie. Maatnummers worden voorlopig handmatig ingevuld of bewust in de partituur gekozen. Geen maat afleiden uit de take-timer. Een nieuwe take begint zonder maatnummer. Schrap de aparte Edit-knop bij notes. Klikken op Bar opent een scrollbaar menu met All (de hele take, zonder specifieke maat) en alle bekende maatnummers van de cue, met wat ruimte voor extra maten. Geef het invoerveld direct focus: typen en Enter kiest de maat. Geen Another bar-label of Choose bar-knop. De tijdcode is direct aanklikbaar en met Enter aanpasbaar; Escape annuleert. Bewaar de oorspronkelijke tijdcode ook bij andere note-bewerkingen en undo/redo. Delete blijft apart. Kies voor de tijdcode samen één relevante bron: film, take, sessie of kloktijd. Automatisch maatvolgen blijft een latere uitbreiding bij een betrouwbare koppeling met de uitvoering. Gebruik dezelfde metadata-editor bij het concept vóór Enter en bij een geplaatste note: dezelfde zwevende scrollbare maatkeuze, All, typen plus Enter, tijdcode aanklikken, Enter en het klokje. Enter in een metadataveld bevestigt die waarde en verstuurt de opmerking niet. Bewaar concept, oorspronkelijke tijdcode en gekozen maat bij wisselen en plaatsen.

### 11. Veelgebruikte opmerkingen

Aanpasbare tekstknoppen voor opmerkingen die vaker terugkomen, zoals Intonation. Klik er één om te proberen.

**Promptonderdeel:**

Aanvulling: bied veelvoorkomende notities als aanpasbare suggesties aan, bijvoorbeeld Intonatie, Meer expressief, Minder expressief, Strak en Alt take. Een klik vult het concept bij de juiste take; daarna kun je aanpassen en Enter drukken. Bewaar bestaand concept en leg het bedoelde moment bij de eerste invoer vast.

### 12. Bediening tijdens het noteren

Als het grote paneel uit beeld gaat, blijft start/stop bovenaan bereikbaar. Handig tijdens het noteren?

**Promptonderdeel:**

Behoud de opnamebediening boven de cue-/takelijst. Zodra die buiten beeld scrolt, neemt een compacte vaste balk de cue, lopende take en start/stop over. Houd deze bediening buiten de note-editor, gescheiden van Add/Delete. Voorkom dubbel zichtbare of knipperende stopknoppen en behoud concept, tijdanker en scrollpositie bij stoppen. Gebruik in Recording één scrollgebied inclusief kop en sessie-instellingen, zonder een genest scrollvenster of extra paneelkaders. De compacte opnamebalk blijft sticky zodra de grote knop wegscrollt.

### 13. Sterren in plaats van Good / NG / Hold?

Zou 1–5 sterren per take handig zijn? Klik de sterren en probeer bijvoorbeeld het filter 4–5 sterren.

**Promptonderdeel:**

Vervang de Good / NG / Hold-beoordeling door 1 tot en met 5 klikbare sterren per take. Bewaar de numerieke beoordeling bij de juiste take. Een nieuwe take mag nog onbeoordeeld zijn. Behoud een eventuele Beste-markering als afzonderlijke keuze. Aanvulling: filter bijvoorbeeld op 4–5 sterren. Filter alleen de weergave; verwijder of hernummer geen takes.

### 14. Een favoriete take en reserves

Best voor je favoriete take; Alt 1, Alt 2 enzovoort voor reservetakes. Los van de sterren.

**Promptonderdeel:**

Aanvulling: voeg een onafhankelijke Alt-toggle toe voor één of meer reservetakes. Maak Beste een toggle met maximaal één Beste per cue; een nieuwe Beste heft de vorige binnen die cue op. Sterren blijven apart. Bewaar alles bij de vaste take-ID. Nummer Alt-takes per cue in take-volgorde als Alt 1, Alt 2 enzovoort, onafhankelijk van het sterrenfilter. Toon het totale aantal alts bij de cue; zonder alts staat er een streepje. Niet-geselecteerde Alt-knoppen tonen Alt –. Houd de knopbreedte gelijk zodat sterren niet verschuiven. Bij verwijderen wordt de nummering opnieuw aaneengesloten. Beste verandert alleen de highlight: geen vinkje of wisselende Beste-tekst in de cuekop. Reserveer een vaste breedte voor Beste en Alt in alle toestanden; sterren, cuegegevens en omliggende tekst blijven op dezelfde plaats bij aan- en uitzetten.

### 15. Snel tussen cues en takes

Met [ en ] wissel je cues. Met Alt erbij wissel je takes; Alt+1 t/m 9 kiest direct een take.

**Promptonderdeel:**

Gebruik in Recording en Cut list dezelfde toetsen: [ voor vorige cue, ] voor volgende cue, Alt+[ voor vorige take, Alt+] voor volgende take en Alt+1 t/m 9 voor het echte take-nummer binnen de gekozen cue. Verwijder de eerdere Alt+cijfer-koppeling aan cuevolgorde; een cijfer is geen cuecode. Voor twee cijfers: druk Alt+Command in, laat beide los en typ bijvoorbeeld 1 en 2 voor Take 12 of 3 en 4 voor Take 34. Toon kort de twee cijferposities als Take __ en daarna Take 1_; na het tweede cijfer kies je de bestaande take. Escape, vijf seconden zonder invoer, klikken, vensterfocus verliezen of een andere actie annuleert de invoer. Cijfers onder ingedrukte Command/Alt-modifiers voeren de keuze niet uit: vraag eerst de modifiers los te laten om browsercombinaties te vermijden. Gebruik fysieke toetscodes voor Option-cijfers en brackets, omdat Option het tekstteken verandert. Key-repeat en IME voeren geen extra acties uit. Normale tekstinvoer, open modale vensters en actieve sleepacties krijgen voorrang. Directe nummers kiezen gewone takes op werkelijk take-nummer, onafhankelijk van filters en ontbrekende nummers; maak ontbrekende takes niet aan en onderscheid overdubs met hetzelfde nummer. Vorige/volgende take volgt de bestaande lijst, inclusief overdubs, en blijft bij de eerste/laatste staan. Cue-navigatie met brackets en knoppen stopt eveneens bij de eerste en laatste cue, zonder naar de andere kant te springen; ook bij ingedrukt houden. Behoud leespositie, notes, concepten en selectie per take. Wisselen kiest de bewerkingslaag en start of stopt niets; een lopende take verandert niet. Cuewisseling tijdens een take blijft geblokkeerd. Behoud configureerbare toetsen en test de browsers en toetsenbordindelingen die de gebruiker inzet. Brackets ingedrukt houden mag navigatie herhalen: eerst één stap, daarna gedoseerd herhalen en na kort vasthouden sneller. Alleen brackets mogen herhalen; cijfers, tweecijferinvoer en opnamecommando’s blijven beschermd tegen key-repeat.

### 16. Werken vanuit de partituur?

Een tweede weergave voor notes en een kniplijst op de score. Klik Cut list om te proberen.

**Promptonderdeel:**

Maak één werkruimte met Recording en Cut list als twee weergaven van dezelfde cue-, take-, rating-, note- en opname-state. Neem de gekozen opname-indeling met bediening bovenaan en compacte balk bij scrollen als basis; hergebruik de bestaande kniplijst. Wisselen mag een lopende take, concepten, scoreselecties of leespositie niet verliezen of stilzwijgend kopiëren. Maak geen onafhankelijke demo-state per weergave.

### 17. De partituur bij de cue

Voorstel: de bijbehorende partituur naast de takes. Kies een cue om de score te bekijken.

**Promptonderdeel:**

Koppel de actieve cue aan zijn bestaande scorebron en PDF-pagina’s. Toon de partituur groot rechts met takes en notes links. Gebruik de bestaande gevalideerde maat-/instrumentmapping waar aanwezig en label benaderingen. Een eigen PDF krijgt niet vanzelf mapping. Wijzig het bron-PDF niet en behoud aparte takegegevens voor cues die dezelfde scorepagina’s delen.

### 18. Ruimte voor de partituur

De score groot in beeld, met doorlopende pagina’s. Zoom met je trackpad of de knoppen; Fit width toont de volle breedte.

**Promptonderdeel:**

Gebruik de beschikbare breedte en hoogte voor een grote, doorlopende partituur. Behoud de bestaande onafhankelijke scroll van de score en de take-/noteskolom: alle pagina’s van de cue staan onder elkaar. Houd de scoreweergave permanent groot. Combineer Recording/Cut list, cue/take, opnamestatus, take-tijd en start/stop in één compacte bovenbalk; laat de reviewbediening bereikbaar. Voeg Zoom in, Zoom out, een percentage en Fit width toe aan de compacte scoreknoppenrij. Behoud takes, notes, kniplijstselecties, vergelijkingen en leespositie bij zoomen, vergroten en takekeuze. Zoom schaalt score én hun annotatielagen samen; klik-/sleepcoördinaten blijven correct. Beperk horizontaal scrollen tot het scorevlak. Verplaats lange gebruiksuitleg uit de werkruimte naar de rondleiding; behoud de bestaande bediening en de oorspronkelijke PDF. Ondersteun ook trackpad-knijpzoom binnen het scorevlak (Chromium ctrl-wheel en Safari gesture-events), met het punt onder de vingers als anker. Gewoon scrollen blijft scrollen; de rest van de pagina zoomt niet mee. Bewaar zoom als één globale instelling van de werkruimte voor alle cues, takes en scorebronnen. Wisselen van cue, take, document of weergave herstelt geen afzonderlijke zoomstand en reset niet naar 100%. Alleen bewust zoomen of Fit width verandert de zoom.

### 19. Een eigen laag per take

Elke take heeft eigen notes en geselecteerde maten. Kies links een take om die te bekijken.

**Promptonderdeel:**

Bewaar kniplijstselecties, score-notes, concepten en leespositie per vaste take-ID én scorebronversie. Een nieuwe take heeft een lege eigen laag. Terugklikken herstelt de juiste gegevens zonder de score onverwacht te verschuiven. Deel deze gegevens met de opnameweergave; de geselecteerde take mag verschillen van de lopende take.

### 20. Maten kiezen voor de kniplijst

Kies een take en markeer maten met ⌘+slepen. ⌘+rechtsklik haalt maten uit die selectie.

**Promptonderdeel:**

Hergebruik de bestaande kniplijstselectie op maatvakken. Command+linksklik of slepen voegt toe en Command+rechtsklik of Command+Option+linksslepen verwijdert. Link instruments staat standaard aan: alle instrumenten van de geraakte maten. Uit selecteert de geraakte instrumenten. Opnieuw koppelen herschrijft bestaande selecties niet. Voorkom het browsercontextmenu tijdens verwijderen. Selectie is per take en bron, geen audio-edit.

### 21. Een note op de score

Dubbelklik bij een maat om een note te schrijven. De plek bepaalt de maat en het instrument.

**Promptonderdeel:**

Dubbelklik op de bestaande scoremapping opent een note-editor bij de gekozen maat en instrument. Enter plaatst kale tekst; Shift+Enter maakt een regel en Escape annuleert. Standaard boven de betreffende notenbalk; All instruments boven de bovenste balk bij die maat binnen deze take. Bewaar maat, instrument, pagina, take en bron als metadata. Geen achtergrondkaart of badges op de PDF. Bied handmatige plaatsingscorrectie; beloof geen volledige notatie-engine. Gebruik de horizontale maatvakken ook voor dubbelklikken vlak boven de balken, zodat bijvoorbeeld boven maat 5 direct maat 5 gekozen wordt. Leid de instrumentcontext af uit de verticale positie: bij een balk voor dat instrument, boven de hele groep voor All instruments.

### 22. Notes terugvinden op de score

Klik links op een note om de plek te zien. Sleep de tekst naar een andere maat om hem daaraan te koppelen.

**Promptonderdeel:**

Behoud de compacte score-noteslijst met Bar, Note en Time. Klikken op note-tekst navigeert naar de juiste scoreplek; het maatnummer blijft direct aanpasbaar. Behoud alleen de aparte Delete-actie. Maat en tijdcode zijn direct bij hun waarde bewerkbaar: een scrollbare matenlijst met All voor de hele take en nummers, typen plus Enter voor een maat, klikken en Enter voor de tijdcode. Een klein klokje herstelt de onveranderlijk opgeslagen oorspronkelijke tijdcode. Klik op tekst in de score om te bewerken en sleep die om de positie te corrigeren. Houd take en bron correct, behoud concepten en maak bewerkingen ongedaan zonder andere takes te wijzigen. Laat bij het slepen de doelmaat subtiel oplichten op basis van de bestaande scoremapping. Werk bij loslaten maatnummer, pagina/boekpagina en instrumentcontext bij zonder tijdcode, take of tekst te veranderen. Bewaar de gekozen vrije tekstpositie. Boven de volledige instrumentgroep wordt de context All instruments. Annuleren wijzigt niets; Command+Z herstelt positie én metadata. Een klik op bestaande scoretekst opent de editor met de note geselecteerd, zonder direct een tekstcursor te plaatsen. Delete/Backspace verwijdert de geselecteerde note; Command+Z herstelt hem. Zodra de gebruiker een tekstveld bewerkt, werkt Delete/Backspace alleen op tekst. Voeg bij het bewerken van een bestaande note Delete naast Cancel toe; geen Delete voor een nog niet geplaatste note. Negeer toetsen met modifiers, key-repeat en IME. Maak alle verwijderacties ongedaan met dezelfde take-/brongebonden history.

### 23. Een keuze terugnemen

Selecties en score-notes zijn ongedaan te maken met ⌘ Z. ⌘ Shift Z voert de bewerking opnieuw uit.

**Promptonderdeel:**

Behoud undo/redo voor toevoegen, verwijderen, aanpassen en verplaatsen van score-notes en maatselecties, per take en scorebron. Command+Z maakt ongedaan, Command+Shift+Z voert opnieuw uit. Onderschep geen normale tekst-undo binnen invoervelden. Andere takes en de oorspronkelijke PDF veranderen niet.

### 24. Meerdere takes vergelijken

⌘+klik op meerdere takes om hun notes en geselecteerde maten samen op dezelfde score te bekijken.

**Promptonderdeel:**

Gewone klik kiest één take; Command+klik schakelt extra takes in of uit voor vergelijking, met minimaal één geselecteerde take. De laatst toegevoegde is bewerkbaar. Houd vaste takekleuren en leespositie; toon expliciete vergelijkingen duidelijker dan achtergrondreferenties. Vergelijken wijzigt geen opname, notes of opgeslagen selecties en neemt geen notes over in een nieuwe take.

### 25. Instrumenten en andere takes

Link instruments koppelt de instrumenten bij maatselectie. See other takes toont of verbergt achtergrondselecties van andere takes.

**Promptonderdeel:**

Behoud Link instruments en See other takes als compacte, benoemde instellingen boven de partituur. Beide beginnen aan. Link instruments bepaalt alleen nieuwe selecties en herschrijft geen eerdere gedeeltelijke selecties. See other takes verbergt alleen achtergrondreferenties; expliciet gekozen vergelijkingstakes en hun notes blijven zichtbaar. Bewaar instellingen bij wisselen van weergave.

### 26. Alle takes per maat

Een overzicht van de geselecteerde maten per take. Klik een maat om die op de partituur te bekijken.

**Promptonderdeel:**

Behoud de bestaande PDF/All takes-schakelaar. Toon in All takes één gedeelde horizontale maat-as met een rij per take, vaste takekleuren, Best/Alt en note-indicatoren. Deel de bestaande selectie-state. Klik op een maat opent die take op de juiste scoreplek; een notestip toont de notes daar. Bij ontkoppelde instrumenten kunnen instrumentrijen uitklappen. Bewaar horizontale en verticale leespositie bij bewerken.

## Gedeelde promptinleiding

Geselecteerde suggesties van Floris voor mijn bestaande MandoCues-app. Implementeer alleen de onderstaande selectie. Bekijk eerst wat al bestaat en behoud mijn bestaande stijl, componenten, state en opslag. Mijn code, workflow en ontwerpkeuzes blijven leidend; dit is geen opdracht om mijn hele programma te vervangen.

Alle daadwerkelijke GUI-tekst is Engels, inclusief hints, tooltips, toegankelijkheidslabels en meldingen. Vragen en toelichting mogen Nederlands blijven. Vertaal geen oorspronkelijke cue-/projectnamen of eigen notes. De demo gebruikt voorbeelddata, neemt geen audio op en bewijst geen DAW-, film- of automatische scorekoppeling. De keuze van een tijdcodebron en het nut van take-timers zijn open vragen, geen impliciete implementatieopdracht.


## Gedeelde afsluiting

Stem gedeelde onderdelen op elkaar af. Voeg geen andere suggesties toe. Controleer de betrokken bestaande flows en vat kort samen wat is aangepast, getest en wat een echte bronkoppeling vereist.
