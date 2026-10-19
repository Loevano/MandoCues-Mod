# MandoCues · voorstel van Floris

Eén werkruimte met Recording en Comp tool. Bij openen kies je Rondleiding starten of Zelf bekijken. De rondleiding toont één suggestie tegelijk; een checkbox bepaalt of die tekst meegaat naar Claude. De app werkt los van deze keuze.

Alle daadwerkelijke GUI-tekst is Engels. Uitleg en vragen blijven Nederlands. Het zijn vrijblijvende ideeën; jouw programma en ontwerpkeuzes gaan voor.

## Vragen

- Waarvoor gebruiken we de duur van elke take?
- Zou ‘New take’ maken en selecteren ook werken, zonder start/stop?
- Wat gebeurt er met de sessietimers als je vergeet een take te starten?
- Waarvoor gebruiken jullie de verschillende klokken tijdens een sessie?
- Zou een klok met de voor-/achterstand genoeg overzicht geven tijdens de sessie?

## De rondleiding

De onderstaande tekstonderdelen worden alleen samengevoegd als ze zijn aangevinkt. Er wordt geen nieuwe prompt gegenereerd.

### 1. ⌘ Enter voor start en stop?

Spatie gebruik je ook in notes. Voorstel: ⌘ Enter voor sessiestart en daarna start/stop van een take.

**Promptonderdeel:**

Starten en stoppen met de spatiebalk kan botsen met het typen van notes, omdat je spatie ook voor tekst nodig hebt. Voorstel voor onze Mac-workflow: gebruik Command+Enter eerst voor Start session. Als de sessie loopt, start dezelfde combinatie een take of stopt de lopende take, ook tijdens typen. Sessiestart maakt nog geen take. De sneltoets moet direct na laden en tijdens de rondleiding werken, ook als het rondleidingstekstje de focus heeft; een handmatige klik in de app mag niet nodig zijn. In het welkomstscherm en andere modale uitleg-/promptvensters blijft opnamebediening geblokkeerd. Spatie blijft gewone tekst en standaard browserbediening. Gewoon Enter plaatst een note. Een ingedrukte of herhalende toets mag niet meerdere keren schakelen; negeer IME-compositie. Bewaar concepten, tijdankers en leespositie bij start/stop. De stopknop blijft apart en bereikbaar. Dit is een voorstel voor de toetskeuze; behoud andere bestaande workflows.

Behoud de opnamebediening boven de cue-/takelijst. Zodra die buiten beeld scrolt, neemt een compacte vaste balk de cue, lopende take en start/stop over. Houd deze bediening buiten de note-editor, gescheiden van Add/Delete. Voorkom dubbel zichtbare of knipperende stopknoppen en behoud concept, tijdanker en scrollpositie bij stoppen. Gebruik in Recording één scrollgebied inclusief kop en sessie-instellingen, zonder een genest scrollvenster of extra paneelkaders. De compacte opnamebalk blijft sticky zodra de grote knop wegscrollt.

### 2. Voor- en achterstand met + en −?

Voorstel: +02:00 voor voorsprong, −02:00 voor achterstand. Achterstand: oranje onder 5 minuten, rood vanaf 5 minuten.

**Promptonderdeel:**

Gebruik voor de bestaande planningsafwijking + voor voorsprong en − voor achterstand. Toon bij nul alleen On schedule, zonder extra 00:00 ernaast. Onder vijf minuten achterstand oranje, vanaf vijf minuten rood; op schema en voorsprong groen. Behoud de oorspronkelijke hoofdverhoudingen, klok met AM/PM, Elapsed (working), Remaining, Planned end en Projected end onder de grote klok en de bestaande berekeningen. Zet Session length, Prep per cue en Max music compact zichtbaar bij de sessiekeuze. Planning bevat eindtijd en bewust verlengen met +15/+30/+60. Geen A/B-indelingsschakelaar. De interpretatie en productieplanning blijven leidend; de lokale demo is geen gevalideerde kopie van de planner.

### 3. Cues en takes direct kiezen

Voorstel: cues direct kiezen, met hun takes eronder. Klik een cue of take om te proberen.

**Sneltoetsen**

[ en ] wisselen cues. ⌥[ en ⌥] wisselen takes; ⌥1 t/m ⌥9 kiest een take. Houd ⌥ + ⌘ vast en typ twee cijfers voor bijvoorbeeld Take 12.

**Promptonderdeel:**

Laat een klik op cuenummer of titel direct die cue kiezen, zonder Go to cue te hoeven gebruiken. Houd cuekeuze los van het pijltje om takes in te klappen. Bewaar concepten en blokkeer cuewisseling zolang een take loopt met een duidelijke melding. Stop of verplaats een take niet impliciet. Markeer alleen de gekozen cue duidelijk in de lijst: kleur de volledige cuekop en toon links een lichte accentlijn. Laat de markering meewisselen met de cuekeuze, ook tijdens de rondleiding. Houd de afzonderlijke take-selectie herkenbaar. Gebruik in beide weergaven [ en ] voor vorige/volgende cue, Option+[ en Option+] voor vorige/volgende take en Option+1 t/m 9 voor het echte take-nummer. Bescherm tekstinvoer en stop bij het eerste en laatste item, zonder omloop; takekeuze verandert geen lopende opname.

Maak de relatie cue → takes zichtbaar met ingesprongen, even hoge take-regels. Plaats take-labels rechts van het cuenummer met een subtiele verticale verbindingslijn. Behoud de bestaande takegrootte; maak het cuenummer minstens even prominent en groter dan het take-label. Een apart cuepijltje klapt die regels in of uit. Houd sterren, Best en Alt op vaste posities; selecteren maakt geen grotere editor in de regel. Bewaar concepten en beoordelingen bij inklappen. De geselecteerde take en de werkelijk lopende take blijven herkenbaar en onafhankelijk.

Gebruik in Recording en Comp tool dezelfde toetsen: [ voor vorige cue, ] voor volgende cue, Alt+[ voor vorige take, Alt+] voor volgende take en Alt+1 t/m 9 voor het echte take-nummer binnen de gekozen cue. Verwijder de eerdere Alt+cijfer-koppeling aan cuevolgorde; een cijfer is geen cuecode. Voor twee cijfers: houd Option (Alt)+Command ingedrukt en typ bijvoorbeeld 1 en 2 voor Take 12 of 0 en 2 voor Take 2. Toon alleen tijdens vasthouden een klein venster met Take __ en Type two digits; na één cijfer Take 1_. Na het tweede cijfer kies je de bestaande take en sluit het venster. Loslaten van één van beide modifiers annuleert onvolledige invoer en sluit het venster direct. Geen loslaat-en-daarna-typen-modus of zichtbare Escape-instructie. Klikken, vensterfocus verliezen, tekstfocus, IME of een andere actie annuleert ook. Een volgende keuze vereist opnieuw indrukken; herhaalde of extra cijfers onder dezelfde vastgehouden combinatie starten geen nieuwe keuze. Gebruik preventDefault voor de afgevangen combinaties. Gebruik fysieke toetscodes voor Option-cijfers en brackets, omdat Option het tekstteken verandert. Key-repeat en IME voeren geen extra acties uit. Normale tekstinvoer, open modale vensters en actieve sleepacties krijgen voorrang. Directe nummers kiezen gewone takes op werkelijk take-nummer, onafhankelijk van filters en ontbrekende nummers; maak ontbrekende takes niet aan en onderscheid overdubs met hetzelfde nummer. Vorige/volgende take volgt de bestaande lijst, inclusief overdubs, en blijft bij de eerste/laatste staan. Cue-navigatie met brackets en knoppen stopt eveneens bij de eerste en laatste cue, zonder naar de andere kant te springen; ook bij ingedrukt houden. Behoud leespositie, notes, concepten en selectie per take. Wisselen kiest de bewerkingslaag en start of stopt niets; een lopende take verandert niet. Cuewisseling tijdens een take blijft geblokkeerd. Behoud configureerbare toetsen en test de browsers en toetsenbordindelingen die de gebruiker inzet. Brackets ingedrukt houden mag navigatie herhalen: eerst één stap, daarna gedoseerd herhalen en na kort vasthouden sneller. Alleen brackets mogen herhalen; cijfers, tweecijferinvoer en opnamecommando’s blijven beschermd tegen key-repeat.

### 4. Notes bij de gekozen take

Zou één notitiepaneel per take handig zijn? Kies een take en typ een note, of probeer een Quick note.

**Promptonderdeel:**

Toon naast vaste cue-/take-regels één apart notitiepaneel voor de gekozen take. Toon alle notes zonder eigen intern scrollvak. Cue-algemene notes staan apart en zijn inklapbaar. Bewaar concepten per take. Een oudere take bekijken stopt of hernoemt de lopende take niet; toon duidelijk welke take wordt bekeken en welke werkelijk loopt.

Aanvulling: bied veelvoorkomende notities als aanpasbare suggesties aan, bijvoorbeeld Intonatie, Meer expressief, Minder expressief, Strak en Alt take. Een klik vult het concept bij de juiste take; daarna kun je aanpassen en Enter drukken. Bewaar bestaand concept en leg het bedoelde moment bij de eerste invoer vast.

### 5. Kloktijd en maat bij een note

De eerste letter legt de kloktijd vast. Kies zelf de maat; het klokje vult de huidige tijd in. Enter slaat je note op en zet een nieuwe klaar.

**Takes terugvinden in Pro Tools**

Voorstel: vergelijk de opgeslagen opnametijden uit de originele WAV’s met ons take-log. Controleer het tijdverschil met één bekende take en bevestig de koppeling. Ontbreekt de opnametijd, dan koppel je handmatig.

**Promptonderdeel:**

Bewaar bij notes de werkelijke kloktijd (hh:mm:ss AM/PM), vastgelegd bij de eerste letter, ook als alle concepttekst daarna wordt gewist, om later met opnamebestanden te kunnen synchroniseren. Geen take-, sessie- of filmtijdcode in de note-interface. Bewaar ook de datum en tijdzone/UTC-instant; toon lokaal AM/PM. Klik de tijd om te bewerken; Enter bevestigt, Escape annuleert. Het klokje vult de actuele kloktijd in, ook voor een oudere take en vóór Enter. Enter plaatst de note en maakt een nieuw concept met een nieuwe kloktijd klaar. Bewaar de aangemaakte datum bij tijdcorrecties en verander de tijd niet bij het bewerken of slepen van tekst. Undo/redo bewaart de tijd. Maatnummers zijn handmatig: invullen of bewust in de partituur kiezen. Bar opent een zwevende scrolllijst met All (hele take) en maatnummers; typen plus Enter kiest direct. Geen automatische maten uit een timer. Gebruik dezelfde metadata-editor bij concepten en geplaatste notes. Enter in metadata plaatst geen note. Behoud Delete als aparte actie. De echte DAW-synchronisatie is geen onderdeel van deze demo.

Bied een optionele koppeling achteraf tussen onze take-/notegegevens en de oorspronkelijke Pro Tools-opnames. Voorbeeld: onze Take 3 hoort bij engineer Take 4. Koppel vaste IDs; hernummer geen takes en wijzig geen audio. De demo bewaart bij daadwerkelijk starten/stoppen van de lokale take de UTC-datum/tijd, IANA-tijdzone, UTC-offset bij start, sessie-ID, cuecode en een unieke log-ID; dit zijn handmatige appgebeurtenissen, geen bevestigde DAW-starts. De bestaande voorbeeldtakes hebben geen werkelijk gelogd opnamemoment. PDF > Take sheet biedt de tijden en Download take log (JSON); demo-invoer verdwijnt bij herladen. Behoud bestaande productieopslag en voeg voor productie duurzame opslag van deze gebeurtenissen toe.

Concrete invoerroute: lees de bext-chunk van de oorspronkelijke WAV/BWF-bestanden, met OriginationDate en OriginationTime, bestandsreferentie en duur. Voor een eerste controle kan de engineer de originele Audio Files in BWF MetaEdit openen en het CORE-document als CSV exporteren; die CSV bevat FileName, OriginationDate en OriginationTime. De technische metadata kunnen aanvullend de bestandsduur leveren. Vergelijk deze gegevens met de JSON-export van ons take-log. Normaliseer datum en tijd naar dezelfde tijdzone, controleer een bekende take en bewaar het gemeten tijdverschil apart. Startverschillen door handmatig klikken blijven onzekerheid; vraag bevestiging van de koppeling, bijvoorbeeld onze Take 3 aan engineer Take 4. Groepeer microfoonkanalen tot één opname; kies niet automatisch één bestand als één take. Verifieer eerst originele WAV/BWF-bestanden uit de gebruikte Pro Tools-versie en opnamewijze. BWF OriginationDate/OriginationTime kunnen aanknopingspunten bieden; het bestaan van die velden bewijst niet dat Pro Tools ze in iedere workflow vult met de echte opnamestart. Original Time Stamp/BWF TimeReference is project-/tijdcodepositie, niet vanzelf kloktijd. Finder Date Created, Date Modified en browser File.lastModified zijn geen bewezen starttijd. Gebruik een Pro Tools Session Info as Text-export voor bronbestand-/clip-/playlistrelaties; behandel diens EDL-tijden niet als opnamedatum. QuickPunch, pre-roll, meerdere kanalen, loopopnames en consolidatie vragen een onderscheid tussen bestand, clip en take.

Controleer vooraf computerklokken en tijdzones; kalibreer met bekende koppelingen en bewaar de gekozen klokcorrectie apart. Stel kandidaten voor op basis van gecontroleerde klokgegevens, datum, cue, duur en opnamegroep, met expliciete onzekerheid voor handmatige startverschillen. Alleen na bevestiging een engineer-label en bronbestand-/clip-ID aan onze take koppelen; behoud oorspronkelijke nummers, tijden en een herleidbaar wijzigingslog. Meerdere kandidaten, ontbrekende tijden of niet-gelogde takes blijven ongekoppeld tot handmatige controle. Het gaat om takes terugvinden, niet sample-nauwkeurige audiosynchronisatie of automatisch maatvolgen. Zie Pro-Tools-takekoppeling.md voor bronnen, beperkingen en de voorgestelde praktijktest.

### 6. Sterren, Best en Alt

Zou 1–5 sterren met een filter handig zijn? Best kiest je favoriet; Alt markeert reservetakes.

**Promptonderdeel:**

Vervang de Good / NG / Hold-beoordeling door 1 tot en met 5 klikbare sterren per take. Bewaar de numerieke beoordeling bij de juiste take. Een nieuwe take mag nog onbeoordeeld zijn. Behoud een eventuele Beste-markering als afzonderlijke keuze. Aanvulling: filter bijvoorbeeld op 4–5 sterren. Filter alleen de weergave; verwijder of hernummer geen takes.

Aanvulling: voeg een onafhankelijke Alt-toggle toe voor één of meer reservetakes. Maak Beste een toggle met maximaal één Beste per cue; een nieuwe Beste heft de vorige binnen die cue op. Sterren blijven apart. Bewaar alles bij de vaste take-ID. Alle take-knoppen tonen steeds Alt, zonder volgnummer. Markeer de keuze alleen met de bestaande highlight en aria-pressed. Toon alleen het totale aantal alternatieven per cue, onafhankelijk van het sterrenfilter, ook als het nul is. Houd de knopbreedte gelijk zodat sterren niet verschuiven. Beste verandert alleen de highlight: geen vinkje of wisselende Beste-tekst in de cuekop. Reserveer een vaste breedte voor Beste en Alt in alle toestanden; sterren, cuegegevens en omliggende tekst blijven op dezelfde plaats bij aan- en uitzetten.

### 7. Werken vanuit de partituur?

Voorstel: Comp tool voor notes en een kniplijst op de partituur. Zoom met het trackpad of de knoppen; Page layout toont één of twee pagina’s.

**Promptonderdeel:**

Maak één werkruimte met Recording en Comp tool als twee weergaven van dezelfde cue-, take-, rating-, note- en opname-state. Neem de gekozen opname-indeling met bediening bovenaan en compacte balk bij scrollen als basis; hergebruik de bestaande kniplijst. Wisselen mag een lopende take, concepten, scoreselecties of leespositie niet verliezen of stilzwijgend kopiëren. Maak geen onafhankelijke demo-state per weergave.

Koppel de actieve cue aan zijn bestaande scorebron en PDF-pagina’s. Toon de partituur groot rechts met takes en notes links. Gebruik de bestaande gevalideerde maat-/instrumentmapping waar aanwezig en label benaderingen. Een eigen PDF krijgt niet vanzelf mapping. Wijzig het bron-PDF niet en behoud aparte takegegevens voor cues die dezelfde scorepagina’s delen.

Gebruik de beschikbare breedte en hoogte voor een grote, doorlopende partituur. Behoud de bestaande onafhankelijke scroll van de score en de take-/noteskolom: alle pagina’s van de cue staan onder elkaar. Houd de scoreweergave permanent groot. Combineer Recording/Comp tool, cue/take, opnamestatus, take-tijd en start/stop in één compacte bovenbalk; laat de reviewbediening bereikbaar. Voeg Zoom in, Zoom out, een percentage en Fit width toe aan de compacte scoreknoppenrij. Behoud takes, notes, kniplijstselecties, vergelijkingen en leespositie bij zoomen, vergroten en takekeuze. Zoom schaalt score én hun annotatielagen samen; klik-/sleepcoördinaten blijven correct. Beperk horizontaal scrollen tot het scorevlak. Verplaats lange gebruiksuitleg uit de werkruimte naar de rondleiding; behoud de bestaande bediening en de oorspronkelijke PDF. Ondersteun ook trackpad-knijpzoom binnen het scorevlak (Chromium ctrl-wheel en Safari gesture-events), met het punt onder de vingers als anker. Gewoon scrollen blijft scrollen; de rest van de pagina zoomt niet mee. Bewaar zoom als één globale instelling van de werkruimte voor alle cues, takes en scorebronnen. Wisselen van cue, take, document of weergave herstelt geen afzonderlijke zoomstand en reset niet naar 100%. Alleen bewust zoomen of Fit width verandert de zoom. Voeg een compact Preview-achtig Page layout-menu toe met een keuze tussen Single page en Two pages en een afzonderlijke Continuous scroll-optie. Toon bij uitgeschakelde Continuous scroll alleen de huidige pagina of het huidige paginapaar met vorige/volgende paginaknoppen. Bewaar indeling globaal naast zoom, zonder aan takes gekoppelde weergavemodi. Ondersteun 10–300% zoom; Fit width past één pagina of een volledig paginapaar in de beschikbare breedte. Behoud annotaties en selecties per werkelijke pagina en houd het zoomanker onder de vingers, ook in de rechterkolom.

### 8. Maten kiezen voor de kniplijst

Kies links een take en markeer maten met ⌘+slepen. Verwijderen kan met ⌘+rechtsklik of ⌘⌥+slepen. Elke take bewaart zijn eigen selectie.

**Promptonderdeel:**

Bewaar kniplijstselecties, score-notes, concepten en leespositie per vaste take-ID én scorebronversie. Een nieuwe take heeft een lege eigen laag. Terugklikken herstelt de juiste gegevens zonder de score onverwacht te verschuiven. Deel deze gegevens met de opnameweergave; de geselecteerde take mag verschillen van de lopende take.

Hergebruik de bestaande kniplijstselectie op maatvakken. Command+linksklik of slepen voegt toe en Command+rechtsklik of Command+Option+linksslepen verwijdert. Link instruments staat standaard aan: alle instrumenten van de geraakte maten. Uit selecteert de geraakte instrumenten. Opnieuw koppelen herschrijft bestaande selecties niet. Voorkom het browsercontextmenu tijdens verwijderen. Selectie is per take en bron, geen audio-edit. Behoud undo/redo voor toevoegen, verwijderen, aanpassen en verplaatsen van score-notes en maatselecties, per take en scorebron. Command+Z maakt ongedaan, Command+Shift+Z voert opnieuw uit. Onderschep geen normale tekst-undo binnen invoervelden. Andere takes en de oorspronkelijke PDF veranderen niet.

Behoud Link instruments en See other takes als compacte, benoemde instellingen boven de partituur. Beide beginnen aan. Link instruments bepaalt alleen nieuwe selecties en herschrijft geen eerdere gedeeltelijke selecties. See other takes verbergt alleen achtergrondreferenties; expliciet gekozen vergelijkingstakes en hun notes blijven zichtbaar. Bewaar instellingen bij wisselen van weergave.

### 9. Notes op de partituur

Dubbelklik bij een maat om te schrijven. Sleep de note naar een andere plek; klik links op een note om die terug te vinden.

**Promptonderdeel:**

Dubbelklik op de bestaande scoremapping opent een note-editor bij de gekozen maat en instrument. Enter plaatst kale tekst; Shift+Enter maakt een regel en Escape annuleert. Standaard boven de betreffende notenbalk; All instruments boven de bovenste balk bij die maat binnen deze take. Bewaar maat, instrument, pagina, take en bron als metadata. Geen achtergrondkaart of badges op de PDF. Bied handmatige plaatsingscorrectie; beloof geen volledige notatie-engine. Gebruik de horizontale maatvakken ook voor dubbelklikken vlak boven de balken, zodat bijvoorbeeld boven maat 5 direct maat 5 gekozen wordt. Leid de instrumentcontext af uit de verticale positie: bij een balk voor dat instrument, boven de hele groep voor All instruments.

Behoud de compacte score-noteslijst met Bar, Note en Time. Klikken op note-tekst navigeert naar de juiste scoreplek; het maatnummer blijft direct aanpasbaar. Behoud alleen de aparte Delete-actie. Maat en kloktijd zijn direct bij hun waarde bewerkbaar: een scrollbare matenlijst met All voor de hele take en nummers, typen plus Enter voor een maat, klikken en Enter voor de kloktijd. Een klein klokje vult de werkelijke huidige kloktijd in, ook tijdens typen of bij een oudere take. Gebruik geen relatieve take-/sessietijd. Bewaar de werkelijke datum en UTC-instant om later te kunnen synchroniseren. Enter plaatst de note en maakt een nieuw concept met een nieuw tijdanker klaar. Klik op tekst in de score om te bewerken en sleep die om de positie te corrigeren. Houd take en bron correct, behoud concepten en maak bewerkingen ongedaan zonder andere takes te wijzigen. Laat bij het slepen de doelmaat subtiel oplichten op basis van de bestaande scoremapping. Werk bij loslaten maatnummer, pagina/boekpagina en instrumentcontext bij zonder kloktijd, take of tekst te veranderen. Bewaar de gekozen vrije tekstpositie. Boven de volledige instrumentgroep wordt de context All instruments. Annuleren wijzigt niets; Command+Z herstelt positie én metadata. Een klik op bestaande scoretekst opent de editor met de note geselecteerd, zonder direct een tekstcursor te plaatsen. Delete/Backspace verwijdert de geselecteerde note; Command+Z herstelt hem. Zodra de gebruiker een tekstveld bewerkt, werkt Delete/Backspace alleen op tekst. Voeg bij het bewerken van een bestaande note Delete naast Cancel toe; geen Delete voor een nog niet geplaatste note. Negeer toetsen met modifiers, key-repeat en IME. Maak alle verwijderacties ongedaan met dezelfde take-/brongebonden history.

### 10. Meerdere takes vergelijken

⌘+klik kiest losse takes; Shift+klik kiest een reeks. Bekijk hun notes en maatselecties samen.

**Alle takes per maat**

Klik op ♪ boven de partituur voor het overzicht per maat. Klik daar een maat om terug te gaan naar de partituur.

**Promptonderdeel:**

Gewone klik kiest één take. Command+klik schakelt losse takes in of uit, met minimaal één geselecteerd. Shift+klik kiest de aaneengesloten reeks tussen het laatste gewone/Command-klikanker en de aangeklikte take; Command+Shift+klik voegt die reeks toe. Gebruik de gebruikelijke Mac-selectie: Shift houdt het anker vast, een gewone of Command-klik zet het anker opnieuw. Dit werkt in PDF en All takes en verandert geen takes of notities. De laatst toegevoegde is bewerkbaar. Houd vaste takekleuren en leespositie; toon expliciete vergelijkingen duidelijker dan achtergrondreferenties. Verhoog kleurcontrast; laat overlap zien met meerkleurige arcering en aparte kleurstrepen per take. Verberg een achtergrondselectie niet zodra de gekozen take dezelfde maat bevat. Selecties blijven onafhankelijk per take; toevoegen, verwijderen en undo in één take wijzigen de andere niet. Vergelijken wijzigt geen opname, notes of opgeslagen selecties en neemt geen notes over in een nieuwe take.

Behoud de bestaande PDF/All takes-schakelaar. Toon in All takes één gedeelde horizontale maat-as met een rij per take, vaste takekleuren, Best/Alt en note-indicatoren. Deel de bestaande selectie-state. Klik op een maat opent die take op de juiste scoreplek; een notestip toont de notes daar. Bij ontkoppelde instrumenten kunnen instrumentrijen uitklappen. Bewaar horizontale en verticale leespositie bij bewerken.

## Gedeelde promptinleiding

Geselecteerde suggesties van Floris voor mijn bestaande MandoCues-app. Implementeer alleen de onderstaande selectie. Bekijk eerst wat al bestaat en behoud mijn bestaande stijl, componenten, state en opslag. Mijn code, workflow en ontwerpkeuzes blijven leidend; dit is geen opdracht om mijn hele programma te vervangen. Behoud bij cues de bestaande muziekduur, Complexity, Planned (min), Actual als cumulatieve werktijd en het handmatige afvinken van afgeronde cues. Behoud daarnaast bestaande take-labels, take verwijderen, automatische planning met handmatige override en terug naar Auto, sessiereset en bestaande herordening; ook waar de lokale demo iets niet nabouwt. Deze bestaande functies zijn geen optionele nieuwe suggesties; cuekeuze, takekeuze en afgerond blijven onafhankelijk.

Alle daadwerkelijke GUI-tekst is Engels, inclusief hints, tooltips, toegankelijkheidslabels en meldingen. Vragen en toelichting mogen Nederlands blijven. Vertaal geen oorspronkelijke cue-/projectnamen of eigen notes. De demo gebruikt voorbeelddata, neemt geen audio op en bewijst geen DAW-, film- of automatische scorekoppeling. Notes gebruiken echte kloktijd; DAW-synchronisatie is nog niet gebouwd. Het nut van take-timers blijft een open vraag.


## Gedeelde afsluiting

Stem gedeelde onderdelen op elkaar af. Voeg geen andere suggesties toe. Controleer de betrokken bestaande flows en vat kort samen wat is aangepast, getest en wat een echte bronkoppeling vereist.
