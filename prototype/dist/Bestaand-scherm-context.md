# Vergelijking met het bestaande Recording-scherm · 19 oktober 2026

Bron: de door Floris op 17 oktober aangeleverde gerenderde inspectie-HTML. Dit is geen volledige JavaScript-/TypeScript-appbron. SoundVibeHQ en de oorspronkelijke PDF-boeken zijn niet aangepast.

| Onderdeel | Bestaand scherm | Huidig voorstel |
| --- | --- | --- |
| Sessiesettings | Session length, Prep per cue, Max music | Behouden; compact bij de sessiebediening |
| Cuegegevens | Muziekduur, Complexity, Planned, Actual, aftekenen | Behouden; aftekenen blijft onafhankelijk van selectie/opname |
| Sessietijdlijn | Blokken op geplande cuetijd | Behouden; volledige cuecodes en direct kiezen |
| Takes / overdubs | Afzonderlijke nummers, labels, verwijderen | Behouden; labels en verwijderen weer actief in beide weergaven |
| Planning | Automatisch met handmatige override; leegmaken herstelt auto | Auto en override actief; alle 26 zichtbare waarden zijn als voorbeeld-overrides overgenomen |
| Bediening | Start/stop, Next cue, Overdub, Break, End/Reopen | Behouden; Previous cue erbij, gegroepeerd in het hoofdpaneel |
| Notes | Take-notes en cue-notes | Beide aanwezig; eigen take-notes en partituurlaag |
| Beoordeling | Good / Hold / NG / Best | Bewust voorstel: sterren, Best en Alt |
| Start/stoptoets | Zichtbare uitleg noemt Space | Bewust voorstel: Command+Enter, zodat spatie tekst blijft |
| Klokken | Kloktijd, werktijd, resterend, geplande/verwachte eindtijd | Kloktijd groot; afwijking eronder. Expected end bewust verborgen op verzoek van Floris; berekening intern behouden |
| Note-tijd | Geen betrouwbare DAW-koppeling uit HTML te bewijzen | Werkelijke kloktijd met datum, vanaf eerste letter; geen relatieve note-tijdcode. Nog geen DAW-sync |
| Add cues / Chat / PDF | Zichtbaar aanwezig | Lokale demonstraties aanwezig; geen nagebouwde serverintegratie |

## Grenzen van de vergelijking

- De inspectie-HTML toont ook een reset van alle takes en timings en een titel “Drag to reorder tabs”. Deze interacties zijn niet nagebouwd in de demo. Dat is geen voorstel om ze uit de echte app te verwijderen.
- Echte opslag, samenwerking, opname-/engineerkoppeling en serverexports zijn niet te controleren met deze momentopname en zitten niet in de lokale demo.
- Het oorspronkelijke scherm noemt planning als voorbereiding plus een gewogen aandeel van de sessie op basis van muziekduur × complexiteit (easy 0,7; medium 1; hard 1,5). De lokale Auto-schatting volgt die toelichting, afgerond op halve minuten. De exacte productieformule, afronding en behandeling van pauzes/overrides zijn niet bewezen. Behoud de echte planner bij implementatie.
- De oorspronkelijke velden en handelingen zijn bestaande functionaliteit, geen optionele suggesties. Behoud ook niet-nagebouwde bestaande functies in de echte app.

## Wat nog een keuze is

Floris vergelijkt twee indelingen van hetzelfde hoofdpaneel: A met cue/take links en klok midden; B met klok boven cue/take. Beide hebben compacte sessiegegevens rechts en delen dezelfde state. De definitieve indeling is nog niet gekozen.
