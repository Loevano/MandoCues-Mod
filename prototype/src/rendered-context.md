# Context uit het bestaande Recording-scherm

Floris heeft op 17 oktober 2026 gerenderde HTML uit de inspector aangeleverd als referentie voor de lokale prototypes. SoundVibeHQ zelf is hiervoor niet aangepast of bediend.

Dit is een momentopname van de zichtbare interface, geen volledige JavaScript-/TypeScript-bron. Eventhandlers, opslag, servergedrag en integraties zijn hiermee niet bewezen.

## Wat zichtbaar al bestaat

- Zijmenu en project-/sessiekeuze.
- Sessieduur, voorbereiding per cue en maximale muziekduur.
- Groot opnamepaneel met cue, muziekduur, complexiteit, geplande werktijd, tijd op de cue en sessieklokken.
- Gewone takes én overdubs, met afzonderlijke nummers. Het getoonde totaalaantal registraties kan dus groter zijn dan het aantal gewone takes.
- Start/stop, Overdub, Next cue, Break, Go to cue en End session.
- Sessietijdlijn met 26 cues en een tabel met cuecode, titel, muziekduur, complexiteit, geplande tijd, werkelijke tijd en takes.
- In-/uitklappen van takes, labels per registratie, Good/Hold/NG/Best en een notitieveld.
- Cuenotities voor deze sessie.
- Handmatige override van geplande werktijd.
- Aftekenen en ongedaan maken van aftekenen.
- Add cues, Chat en PDF-acties.
- De zichtbare sneltoetsuitleg noemt Space voor start/stop, N voor volgende cue en P voor pauze. Een toegankelijkheidstekst noemt Space ook voor slepen. Controleer de werkelijke sneltoetsafhandeling voordat je die aanpast.

## Planning volgens de zichtbare toelichting

De UI noemt voorbereiding plus een aandeel in de sessie naar verhouding van muziekduur × complexiteit, met gewichten easy 0,7×, medium 1× en hard 1,5×. Planned kan handmatig worden ingevuld; leegmaken gaat volgens de toelichting terug naar automatisch.

De precieze interne berekening is niet onderzocht. Prototype 05 gebruikt bewust een simpele, handmatig instelbare voorbeeldberekening om de presentatie van voor/achter te laten proberen. Gebruik die demoformule niet als vervanging van bestaande planningslogica.

## Gevolgen voor de voorstellen

- Prototype 01 verbetert de zichtbare groepering; uitklappen wordt niet als ontbrekende nieuwe functie voorgesteld.
- Prototype 02 houdt de sessiecontext, het cueplan en cuegegevens herkenbaar. De Overdub-actie is ook in de lokale proef te proberen.
- Een overdub krijgt een eigen ID en teller; na Take 2 en Overdub 1 volgt nog steeds Take 3. Notes, sterren en labels blijven bij de juiste registratie.
- Bestaande Break/End session, Chat/PDF, labels, aftekenen en handmatige planning moeten in de echte app behouden blijven, ook waar een geïsoleerd prototype ze niet volledig nabouwt.
- De nieuwe bediening is een voorstel voor presentatie en invoer, geen voorgeschreven herbouw van de bestaande app.
- Inspectie-HTML bewijst geen automatische partituurherkenning, recorderverbinding, betrouwbare filmtijdcode of DAW-koppeling.

De overdracht bevat deze samenvatting van de relevante schermstructuur. De aangeleverde pagina wordt niet uitgevoerd of integraal in de prototypes opgenomen. Voorbeeldregistraties blijven demonstratiedata.


## Gedeelde lokale opnameweergave

De gewone voorstellen 01, 02, 03 en 05 hergebruiken nu hetzelfde opnamepaneel, dezelfde sessiecontext, het cueplan en de cue-/takecomponenten. Notes, sterren en takekeuze gebruiken hetzelfde take-model binnen een voorbeeld. Alleen de kniplijst met partituur heeft een eigen werkweergave. Dit is hergebruik binnen de lokale prototypecode; de aangeleverde inspectie-HTML is geen volledige appbron.
