# Takes terugkoppelen aan Pro Tools

Onderzocht op 19 oktober 2026. Voorstel voor later; er is geen DAW-koppeling of WAV-import gebouwd.

Het idee is bruikbaar: onze Take 3 kan bij de engineer Take 4 heten. Met gecontroleerde opnametijden kunnen we een koppeling voorstellen, die iemand bevestigt. Kloktijd is hierbij een zoekhulp. Het bewijst geen exacte audio-uitlijning.

## Concrete route voor de eerste versie

1. Bewaar de originele opnames uit de **Audio Files**-map van de engineer, plus ons JSON-take-log via **PDF → Take sheet → Download take log**.
2. Open de WAV’s in **BWF MetaEdit** met **Open Directory**. Bekijk in **CORE** de velden `OriginationDate` en `OriginationTime` en exporteer het CORE-document als CSV. Alleen uitlezen/exporteren; de WAV’s hoeven niet te worden bewerkt. Deze workflow is beschreven door [MediaArea](https://mediaarea.net/BWFMetaEdit/workflows). De CSV bevat per bestand onder andere `FileName`, `OriginationDate` en `OriginationTime`; zie het [FADGI CORE-formaat](https://www.digitizationguidelines.gov/audio-visual/documents/core_doc_help.html).
3. Zet de metadata om naar dezelfde tijdzone als ons log. BWF bevat in deze velden geen tijdzone: leg die van de engineer vast. Vergelijk één bekende take om het tijdverschil te controleren; controleer later nog een referentie, omdat handmatig starten ook vertraging geeft.
4. Zoek per cue/dag de passende starttijd en controleer stop/duur als aanvullende aanwijzing. Groepeer tegelijk opgenomen microfoonbestanden. Laat iemand de match bevestigen en bewaar beide nummers: **onze Take 3 ↔ engineer Take 4**. De audio en de bestaande take-nummers blijven behouden.
5. Ontbreken geldige opnametijden, dan volgt er geen automatische match. Koppel handmatig op cue, engineer-label, bestand/clip en luistercontrole, of gebruik een expliciet opnamelog van de engineer.

Dit is een concreet voorstel voor import en koppeling; de huidige demo heeft die import nog niet. De metadata-uitlezing en CSV-export bestaan al in BWF MetaEdit. Of de gebruikte Pro Tools-opnames de benodigde kloktijd bevatten, moet uit die originele bestanden blijken. Een Session Info as Text-export kan helpen bij clip-/bestandsrelaties, maar vervangt de echte opnametijd niet.

## Wat de bestanden kunnen vertellen

- BWF heeft aparte `OriginationDate` en `OriginationTime` voor de aanmaak van de audiosequentie. `TimeReference` bevat de tijdcode als sampletelling. Die drie velden zijn verschillende gegevens; de datum-/tijdvelden bevatten zelf geen tijdzone. [EBU Tech 3285, §2.3, p. 10–11](https://tech.ebu.ch/docs/tech/tech3285.pdf#page=10).
- Pro Tools beschrijft Original Time Stamp als een tijdlijnpositie ten opzichte van de sessiestart. Herhaald opnemen vanaf dezelfde projectpositie levert dus geen unieke kloktijd op. Workspace onderscheidt Date Created, Original Time Stamp en Shoot Date; dat laatste kan bij geïmporteerde veldopnames uit de aanmaakdatum worden overgenomen. Dit documenteert geen garantie dat iedere native Pro Tools-opname een correcte werkelijke starttijd in BWF krijgt. [Pro Tools Reference Guide 2026.4, p. 496–499 en 1203](https://resources.avid.com/SupportFiles/PT/Pro_Tools_Reference_Guide_2026.4.pdf#page=598).
- `File > Export > Session Info as Text` geeft bestands-, clip- en playlistinformatie. De EDL bevat clipposities en duur, geen gegarandeerde kalenderdatum van de opname. QuickPunch kan meerdere punches uit één doorlopend audiobestand halen. Eén bestand is daarom niet altijd één take. [Dezelfde handleiding, p. 698–701 en 823–824](https://resources.avid.com/SupportFiles/PT/Pro_Tools_Reference_Guide_2026.4.pdf#page=800).

De huidige officiële handleiding is rechtstreeks gedownload en uitgelezen omdat de webviewer deze grote PDF niet kon openen. De oudere [officiële Workspace-uitleg](https://apps.avid.com/proToolsFirstHelp/version12.3/enu/Pro%20Tools%20First%20Help/sess6.Workspace.16.034.html) beschrijft hetzelfde onderscheid.

**Nog niet bewezen:** welke werkelijke kloktijd de engineer met zijn Pro Tools-versie en opnamewijze in onze originele WAV-bestanden terugkrijgt. Dat moet een praktijktest vaststellen. De BWF-specificatie en het kunnen lezen van metadata bewijzen het schrijfgedrag van Pro Tools niet. Gebruik ook Finder-aanmaak-/wijzigingsdatums en `File.lastModified` niet blind als opnamestart, zeker na kopiëren of exporteren.

## Voorgestelde werkwijze

1. Houd onze eigen take-ID, sessie/dag, cuecode, start en stop bij. Sla echte instants met volledige datum op; bewaar ook tijdzone en offset. De note-tijd blijft afzonderlijk en begint bij de eerste letter. Een note-tijd veranderen verandert het take-log niet.
2. Controleer vóór de sessie of beide computers dezelfde tijd en tijdzone gebruiken. Neem een paar bekende referentietakes, ook later op de dag. Bepaal daarmee klokverschil en de spreiding door handmatig start/stoppen. Corrigeer een matchberekening; overschrijf de oorspronkelijke waarnemingen niet.
3. Lees achteraf eerst metadata van ongewijzigde bron-WAVs. Gebruik eventuele sessietekst voor namen, playlists en clip-/bronrelaties. Bewaar waar elk tijdgegeven vandaan komt. Laat ongeldige of ontbrekende tijden onbekend; maak er geen schijnzekere kloktijd van.
4. Groepeer tegelijk opgenomen microfoonkanalen. Behandel QuickPunch, loopopnames, overdubs, pre-roll, clips en later gemaakte bounces/consolidaties afzonderlijk. Zoek kandidaten binnen de juiste sessie/datum en cue, met gecorrigeerde starttijd en duur als hulpmiddelen. Een vaste nummer-offset zoals ‘altijd +1’ is onvoldoende als later nog een take ontbreekt.
5. Laat iemand de koppeling bevestigen: **MandoCues Take 3 ↔ engineer Take 4**, met bronbestanden/clipreferenties. Behoud beide namen en IDs. Toon twijfel en laat handmatig koppelen als er meerdere kandidaten zijn, tijden ontbreken of een take niet is gelogd. Pas geen audio of takevolgorde aan.

Pas met een gecontroleerde relatie tussen echte opnamestart en projectpositie kun je onderzoeken waar een note in de Pro Tools-tijdlijn hoort. Startvertraging en punches beperken de nauwkeurigheid. Dit levert geen automatisch maatnummer of sample-nauwkeurige synchronisatie op. Als de WAVs geen bruikbare kloktijd bevatten, is een expliciet opnamelog van de engineer of een latere gevalideerde DAW-eventkoppeling nodig; alleen projecttimestamps zijn onvoldoende.

## Wat de demo nu bewaart

Nieuwe takes en overdubs krijgen `takeLog`: unieke ID, sessie-ID, cuecode, `loggedStartAt`, `loggedEndAt`, IANA-tijdzone en UTC-offset bij start. Start/stop zijn onze lokale knop-/toetsmomenten, nadrukkelijk geen bevestiging van de engineer. De voorbeeldtakes blijven zonder opnamelog; daarvoor worden geen tijden verzonnen.

Via **PDF → Take sheet → Download take log (JSON)** kun je dit bekijken en meenemen, inclusief note-kloktijden met datum. Het bestand is als demo gemarkeerd. De demo bewaart nieuwe invoer niet na herladen; downloaden bewaart een momentopname. Productie vraagt duurzame opslag, behoud van logs bij verwijderen en een afzonderlijk bevestigingslog voor koppelingen.

## Eerst samen met de engineer testen

Maak twee korte takes vanaf dezelfde projectpositie, met bekende kloktijd en bewust verschillende take-nummers in beide systemen. Bewaar originele WAVs, metadata en een Session Info as Text-export. Controleer welke datum-/tijdvelden gevuld zijn en of ze overeenkomen met de echte opname. Herhaal met QuickPunch, meerdere kanalen, een onderbreking en een gekopieerd bestand. Controleer ook datumwisseling en een bekend klokverschil. De koppeling is pas betrouwbaar als de herkomst van de tijden en het groepsgedrag zijn vastgesteld.

Voorlopige keuze: kandidaten tonen en handmatig bevestigen. Geen automatische hernummering of stille koppeling. Vraag aan de collega: **welke opnamewijze gebruiken jullie, en kunnen we dit met een paar originele WAVs controleren?**
