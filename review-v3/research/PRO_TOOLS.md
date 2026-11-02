# Pro Tools volgen — onderzoek voor v3

Onderzocht 2 november 2026. Geen live-koppeling geïmplementeerd. Bronclaims, technische gevolgtrekkingen en voorgestelde keuzes staan hieronder afzonderlijk.

## Wat we weten uit documentatie

**Tijdcode over een audiolijn is mogelijk.** LTC is een tijdcodesignaal; een gewone muziek-/kliklijn is dat niet. Avid beschrijft hoe Sync X LTC genereert met tijdadressen van de Pro Tools-tijdlijn tijdens opnemen of afspelen. Deze documentatie bewijst dat tijdcode binnenkomt, niet dat de ontvanger daarmee opname en afspelen kan onderscheiden. [Avid Sync X Guide, hoofdstuk 6](https://cdn.avid.com/ProTools/2021.3/A6F1378B/Pro%20Tools%20Sync%20X%20Guide.pdf).

**Zonder Sync X bestaan andere routes.** Source Elements documenteert MTC uit Pro Tools via Setup → Peripherals → Synchronization → MTC Generator Port en Gen MTC. Een converter zoals hun Source-LTC kan MTC naar audio-LTC omzetten en andersom; het is een bestaande mogelijkheid met eigen licentie, geen benodigde aankoopkeuze voor dit project. De concrete studio-uitgang en framerate moeten worden afgesproken. [Source-LTC User Guide, p. 2 en 9](https://static.source-elements.com/docs/PDF_Source-LTC_1.0_User_Guide-Web-Version.pdf).

**MTC is een synchronisatieprotocol.** De specificatie kent quarter-frame en full-frame-berichten en optionele SMPTE-userbits. Hieruit volgt geen standaard uitwisseling van de cuecode of bestands-/take-naam van een Pro Tools-opname. [MIDI Association — MIDI Time Code](https://midi.org/midi-time-code).

**Er bestaat een aparte Pro Tools-API.** De Scripting SDK kan volgens Avid sessies, clips en playback state opvragen en met Pro Tools communiceren via gRPC/Protocol Buffers. Avid publiceert de download en documentatie achter acceptatie van de toolkitvoorwaarden. Dat is een kandidaat voor aanvullende gegevens, geen bewijs dat alle noodzakelijke live-eventvelden/stabiele clip-IDs al beschikbaar zijn in de gebruikte versie. De precieze SDK-versie en opdrachten moeten nog in een praktijktest worden onderzocht. [Avid SDK FAQ](https://kb.avid.com/pkb/articles/en_US/Knowledge/Pro-Tools-Scripting-SDK-FAQ), [toolkit](https://developer.avid.com/scripting/).

**Browser-MIDI heeft randvoorwaarden.** Web MIDI vereist een secure context, toestemming en ondersteuning van de browser. Sysex vereist afzonderlijke toegang; MTC-full-frame-berichten mogen daarom niet worden verondersteld te arriveren zonder die toegang. De actuele W3C-specificatie is een Working Draft en bewijst geen browserondersteuning in de studio. [W3C Web MIDI API](https://www.w3.org/TR/webmidi/).

## Conclusie voor het ontwerp

Een kabel met LTC/MTC kan ons de **projectpositie** geven. Alleen die positie is onvoldoende voor automatisch cue/takebeheer: afspelen en opnemen kunnen dezelfde tijdcode geven; takes kunnen vanaf dezelfde plek beginnen; een naam of verwijdering verandert niet noodzakelijk het tijdcodesignaal. Dit is een technische gevolgtrekking, geen geteste koppeling.

Om het doel van Floris te halen moeten drie dingen los worden vastgelegd:

1. **Projectpositie** met framerate, drop/non-drop, geldigheid en signaalverlies.
2. **Daadwerkelijke opnamegebeurtenissen**, start/stop, bron/session-ID en eventuele opname/punchsegmenten.
3. **Identiteit**: engineer-bestands-/clipreferenties, cuetoewijzing, naam en maatbereik; plus wijzigingen na stoppen.

Lokale kloktijd blijft nuttig voor notes en controle achteraf, maar is een ander gegeven dan de ontvangen projecttijdcode. Bewaar beide met hun herkomst, niet als één verwisselbare timer.

## Voorgestelde routes ter beoordeling

| Route | Wat haalbaar onderzocht kan worden | Wat extra nodig blijft |
| --- | --- | --- |
| LTC-uitgang → line-input van Floris’ interface → decoder | Projecttijdcode ontvangen; decoder moet framerate en lockverlies expliciet melden | Record-state en betrouwbare take/cue-naam ontbreken |
| MIDI/MTC-uitgang → MIDI-input → ontvanger | Projectpositie zonder audiodecoder | Record-state, take/cue-identiteit en browsercompatibiliteit |
| Bridge bij Pro Tools via ondersteunde SDK, met netwerkverbinding naar MandoCues | Opname-/clip-/sessiegegevens via beschikbare versiegebonden API onderzoeken | Installatietoestemming engineer, commands, identiteit en transportlatentie testen |
| Tijdcode én bridge | Positie en opname-identiteit combineren | Synchronisatie/reconnect/authoriteit aantoonbaar testen |

**Voorlopig advies:** behandel Pro Tools als bron voor opname en identiteit zodra de bridge die betrouwbaar kan leveren. Gebruik LTC/MTC eventueel als positiekanaal. Bouw eerst een read-only proof of concept; stuur vanuit deze app nog geen opnamecommando’s terug. Er is nu geen keuze voor een betaalde converter, hardwareaankoop of installatie gemaakt.

## Handmatige terugval en override

Voor nu Space buiten tekstinvoer. Later expliciete bronstatus: Manual, Following Pro Tools, Connection lost of Manual override. Bij de eerste handmatige start tijdens gekoppelde modus vraagt de app of Floris de automatische bron wil overrulen. Bevestiging geldt voorlopig voor die overrideperiode, niet voor altijd; terug naar Follow is bewust en zichtbaar. Dit is een voorstel dat nog als klein prototype wordt beoordeeld.

Bij signaalverlies niet automatisch stoppen, een nieuwe take verzinnen of plots terugschakelen. Markeer de bron onzeker, houd een log en laat een bewuste terugval toe. Na reconnect worden brongebeurtenissen ontdubbeld op identiteit, niet op take-nummer of alleen tijdcode.

## Verwijderen en naamgeving

Eén interne take-ID verwijst naar één opnamegroep en de bijbehorende bronclips/-bestanden. Meerdere microfoonkanalen zijn geen losse takes. Een engineernaam is een aanpasbaar label, geen primaire sleutel. Een bronverwijdering bewaart notes en het oude verband en wordt zichtbaar als bron ontbreekt. Niet automatisch notes of audio wissen of alle latere takes hernummeren.

Een cue kan worden gekozen via expliciete engineer-/markerconventie of gevalideerde tijdcodebereiken; die mapping is sessiespecifiek. Een globale take-offset van +1 of een oplopende teller is geen sluitende identificatie. Secties binnen een cue blijven gewone takes met een afzonderlijk maatbereik.

## Praktijktest vóór een belofte van automatische sync

Met de engineer: Pro Tools-versie, opnamewijze (normal/QuickPunch/loop), framerate, beschikbare uitgang en toestemming voor een bridge afspreken. Daarna testen: play zonder record, twee takes vanaf dezelfde positie, punch, meerdere kanalen, naam wijzigen, take verwijderen, kabel los, reconnect, klokverschil en herstart van de browser. Voor elke handeling vergelijken we ontvangen tijdcode, opname-events, bronreferenties, take-ID en notes.

Open vraag aan Floris staat uit: welke versie/signaalroute gebruikt de engineer en mag er een helper op zijn Mac draaien? Zonder die gegevens kunnen we het ontwerp en de ontvangerproef voorbereiden, maar niet aantonen dat cue, take en duur automatisch betrouwbaar volgen.
