# Vergelijking met het bestaande Recording-scherm · 19 oktober 2026

Bron: de door Floris op 17 oktober aangeleverde gerenderde inspectie-HTML. Dit is geen volledige JavaScript-/TypeScript-appbron. SoundVibeHQ en de oorspronkelijke PDF-boeken zijn niet aangepast.

| Onderdeel | Bestaand scherm | Huidig voorstel |
| --- | --- | --- |
| Sessiesettings | Session length, Prep per cue, Max music | Behouden; compact zichtbaar bij de sessiekeuze, zonder A/B-keuze |
| Cuegegevens | Muziekduur, Complexity, Planned, Actual, aftekenen | Behouden; aftekenen blijft onafhankelijk van selectie/opname |
| Sessietijdlijn | Blokken op geplande cuetijd | Behouden; volledige cuecodes en direct kiezen |
| Takes / overdubs | Afzonderlijke nummers, labels, verwijderen | Behouden; labels en verwijderen weer actief in beide weergaven |
| Planning | Automatisch met handmatige override; leegmaken herstelt auto | Auto en override actief; alle 26 zichtbare waarden zijn als voorbeeld-overrides overgenomen |
| Bediening | Start/stop, Next cue, Go to cue, Overdub, Break, End/Reopen | Behouden; Go to cue naast Next cue, Previous cue erbij. Zoeken op cuecode/titel; cuewisseling tijdens een take geblokkeerd |
| Notes | Take-notes en cue-notes | Beide aanwezig; eigen take-notes en partituurlaag |
| Beoordeling | Good / Hold / NG / Best | Bewust voorstel: sterren, Best en Alt |
| Start/stoptoets | Zichtbare uitleg noemt Space | Bewust voorstel: Command+Enter, zodat spatie tekst blijft |
| Klokken | Kloktijd, werktijd, resterend, geplande/verwachte eindtijd | Kloktijd in AM/PM met vier oorspronkelijke sessietijden eronder; gekleurd planningsvlak met +/− of alleen On schedule |
| Note-tijd | Geen betrouwbare DAW-koppeling uit HTML te bewijzen | Werkelijke kloktijd met datum, vanaf eerste letter; geen relatieve note-tijdcode. Nog geen DAW-sync |
| Add cues / Chat / PDF | Zichtbaar aanwezig | Lokale demonstraties aanwezig; geen nagebouwde serverintegratie |

## Grenzen van de vergelijking

- De inspectie-HTML toont ook een titel “Drag to reorder tabs”; die tab-herordening is niet nagebouwd. Reset van takes en timings is nu met bevestiging aanwezig per opnamedag. Behoud in productie het bestaande resetbeleid en echte opslag.
- Echte opslag, samenwerking, opname-/engineerkoppeling en serverexports zijn niet te controleren met deze momentopname en zitten niet in de lokale demo.
- Het oorspronkelijke scherm noemt planning als voorbereiding plus een gewogen aandeel van de sessie op basis van muziekduur × complexiteit (easy 0,7; medium 1; hard 1,5). De lokale Auto-schatting volgt die toelichting, afgerond op halve minuten. De exacte productieformule, afronding en behandeling van pauzes/overrides zijn niet bewezen. Behoud de echte planner bij implementatie.
- De oorspronkelijke velden en handelingen zijn bestaande functionaliteit, geen optionele suggesties. Behoud ook niet-nagebouwde bestaande functies in de echte app.

## Wat nog een keuze is

Er is één vaste indeling: de drie sessievelden bovenaan, de vier sessietijden onder de grote klok en eindtijd/verlengen in Planning. De A/B-keuze is vervallen. De eerdere klok-midden/-boven-varianten zijn ingetrokken. Nieuwe werktijden beginnen op nul; de oude 42-/8-minutenvoorbeeld-offsets zijn verwijderd. De expliciete tweede dag is een lokale voorbeeldsessie met gescheiden data, geen bewezen koppeling met echte opnamedagen.

## Controle naast het screenshot van 19 oktober

- Grote cue, AM/PM-klok, opnamestatus, gekleurd planningsvlak, Next cue, Go to cue, Overdub, Break en End/Reopen blijven herkenbaar. Go to cue is bestaande bediening, geen optionele nieuwe suggestie.
- Music length, Planned, Actual, aftekenen, take-labels en verwijderen zijn aanwezig. De cumulatieve cuewerktijd is geen muziekduur of take-timer.
- Bewuste voorstellen blijven: sterren met Best/Alt, één take-notitiepaneel, direct cue kiezen, Command+Enter, Comp tool en minder hoofdklokken. De secundaire klokken staan onder Planning; verwijderen uit de hoofdweergave betekent niet verwijderen uit de app.
- Bevestigd: gebruikte muziekduur compact naast Max music; reset van takes/tijden met bevestiging; algemene cue-notes blijven ingeklapt. De muziekduur is de som van de huidige cuelijst (53:14), niet een overgetypt totaal uit het screenshot.
- Complexity gebruikt weer de oorspronkelijke namen Easy/Medium/Hard met dezelfde gewichten 0,7/1/1,5.
- Het aantal afgeronde cues staat weer compact in het planningsvlak, gekoppeld aan dezelfde handmatige vakjes. Afvinken blijft los van opnemen en takekeuze.
- De oorspronkelijke tab-herordening, echte opslag, samenwerking en serverexports zijn niet gecontroleerd of geïntegreerd. De inspectie en screenshots zijn geen volledige appbron.
