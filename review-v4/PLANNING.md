# Tijdplanning in de v4-proef

Dit is een controleerbare eerste hypothese voor sessieplanning, nog geen gevalideerd algoritme. Het prototype verwerkt handmatige sessie-/cuekeuze, geen DAW-signalen. Voor dagelijks gebruik moet dit eerst worden vergeleken met echte sessies. Er is geen betrouwbaar automatisch maatvolgen of muzikale voortgangsherkenning.

## Wat de gebruiker ziet

- **Available for this cue:** het huidige cuebudget min werkelijk werk; onder nul wordt het Over cue budget. Dit is de beschikbare tijd, geen zekerheid dat de cue dan klaar is.
- **Session forecast:** geschat resterend werk tegenover de tijd tot Finish by. − is verwachte uitloop, + verwachte ruimte. Oranje bij minder dan vijf minuten uitloop; rood vanaf vijf minuten. Groen bij nul of ruimte.
- **Estimated work left:** apart van het cuebudget. Een cue blijft onafgerond tot Done; nul op de budgetklok betekent niet automatisch dat het werk op is.
- **Timing details:** sessietijd over, werkelijk werk op deze cue, geschat resterend totaalwerk en kloktijd met AM/PM.

## Werkbelasting en initiële schatting

Per cue is de werkelijk op te nemen muziekduur apart bewerkbaar, in mm:ss. De oude totale muziekduur is alleen de beginwaarde. Variant A gebruikt één duur per cue. Variant B telt expliciet ingevoerde duren van niet-overlappende opnamebereiken op. Er wordt geen duur afgeleid uit maatnummers. Overlappende delen moeten tot unieke muziekpassages worden samengevoegd om dubbeltellen te voorkomen.

De voorlopige complexiteitsgewichten zijn Easy = 0,7; Medium = 1; Hard = 1,5. Dit zijn de bestaande uitgangsgewichten, niet gemeten nieuwe parameters. Gewogen muziekduur = opnameomvang × gewicht.

Voorbereiding per cue wordt apart begroot. Het overgebleven startsessiebudget wordt gedeeld door de totale gewogen opnameomvang. Dat geeft een aanvankelijk werktempo: werkseconden per gewogen muziekseconde. De initiële schatting is voorbereiding + tempo × gewogen opnameomvang. De startplanning past daardoor binnen het gekozen budget, tenzij alleen de voorbereiding al niet past. Dat is een verdelingskeuze, geen bewijs dat de sessie haalbaar is.

Na sessiestart verandert de oorspronkelijke tempo-referentie niet door alleen de eindtijd te verlengen of in te korten. Meer beschikbare tijd bewijst niet dat het werk langzamer gaat. De startbudgetten blijven apart bewaard naast actuele beschikbare budgetten.

## Leren van afgeronde cues

Alleen afgeronde cues met positieve, betrouwbare werktijd en positieve werkbelasting tellen mee. Tijd op een onafgeronde cue vertelt zonder muzikale voortgang niet hoeveel werk nog nodig is. Aantal takes en take-duur blijven context; ze zijn geen onafhankelijke maat voor productiviteit. We tellen dus niet simpelweg takes op of voorspellen dat acht takes altijd tweemaal zo lang duren als vier.

Per betrouwbare cue vergelijken we de gemeten productieve werktijd (werk min voorbereiding) met de oorspronkelijke verwachting voor zijn gewogen muziekduur. Die verhouding wordt begrensd tussen 0,25 en 4 en op logschaal gecombineerd. Drie cue-equivalenten aan oorspronkelijke verwachting dempen het effect van kleine datasets. Zeer korte cues krijgen minder gewicht; voor de te voorspellen complexiteit krijgen andere complexiteiten voorlopig een half gewicht. Deze demping voorkomt dat één uitschieter de sessieprognose overheerst.

Voorbeeld: een Hard-cue die naar verhouding precies 1,5 keer zoveel werk vroeg als een Medium-cue, is niet automatisch bewijs dat de hele sessie langzamer gaat: die moeilijkheid zat al in de verwachting. Afgeronde werktijd wordt vastgezet bij Done, zodat wachten op de volgende cue de leersample niet blijft verhogen. Uitvinken heropent de cue vanaf die vastgezette werktijd.

Variant A leert zo geleidelijk. Variant B houdt het referentietempo vast. Het rekenvoorbeeld in Review v4 gebruikt aparte data en schrijft geen nepmetingen naar de echte proefstate.

## Resterend werk en beschikbare tijd

Voor een onafgeronde cue nemen we de hogere waarde van geschat totaalwerk min werkelijk werk en een kleine afrondreserve. Die reserve is voorlopig 10% van de schatting, begrensd door voorbereiding en minimaal 30 seconden. De reserve blijft bestaan tot Done of een handmatige resterende-werkschatting. Hij is zichtbaar beschreven en later aan echte sessies te toetsen; het programma weet niet vanzelf of er nog één of vijf takes nodig zijn.

Een expliciete resterende-werkschatting telt af vanaf het gecorrigeerde werktijdanker. De gebruiker mag daar bewust nul invullen. Dat markeert de cue niet automatisch als Done. Budget en resterende werkverwachting blijven afzonderlijke waarden.

Herverdelen van beschikbare tijd verandert de werkschatting niet. Bij 25 minuten beschikbaar en 30 minuten geschat werk blijft de verwachte uitloop 5 minuten, ook als de budgetten over de volgende cues worden verkleind. Variant A herverdeelt bij cuewissel, afronden of bewuste planningcorrecties; Variant B houdt budgetten vast. Handmatig vastgezette cuebudgetten blijven behouden. Herverdelen levert geen verborgen tijdwinst op.

## Handmatige controle en herstel

Cuewerktijd omvat ook overleg en werk tussen takes, onafhankelijk van handmatig starten/stoppen van takes. Pauze houdt de werktimers tegen; de vaste eindtijd blijft ondertussen naderen. Late starts worden zichtbaar wanneer een vaste Finish by gekozen is; zonder vaste eindtijd begint de relatieve sessieduur bij Start session.

In Cue timing kan de gebruiker opnameomvang, budget, werkelijk werk en resterende werkschatting bijstellen. Een storing kan met de inclusiecheckbox uit het leerwerktempo worden gehouden. De verstreken kloktijd blijft wel van de tijd tot de eindtijd afgaan. Correcties bewaren tijdstip, oude en nieuwe waarde in het lokale correctielog. Een gemiste cuewissel vraagt controle van beide betrokken cuewerktijden; er is geen automatische waarheid uit de engineerdata.

Een open bewerkingsvenster pauzeert niets. Alleen een daadwerkelijk gewijzigde werktijd corrigeert de meter; bewaren van een andere instelling mag geen inmiddels verstreken tijd wissen. Take-ID's, take-log, notes en opnamebereiken veranderen niet bij een timingcorrectie.

De v3-flikkerfout blijft voorkomen: deadline en werk gebruiken dezelfde secondegrenzen. De vijfminutengrens blijft echt; er is geen tolerantieband die kleine fouten alleen verstopt.

## Grenzen van deze proef

Het model schat nog geen ensemble-, engineer-, bezettings- of leercurve-effecten apart. Het is niet betrouwbaar om al die parameters uit twee cues af te leiden. Meer gegevens rechtvaardigen later een uitgebreider model; nu moeten uitlegbaarheid en herstel vooropstaan.

Alle proefmetingen en notes leven voorlopig in de geopende demo en worden bij herladen niet duurzaam bewaard. Reviewkeuzes worden wel lokaal bewaard en zijn als JSON te downloaden. Take-logexport bevat de takebereiken; dit vervangt geen productiedatabase of DAW-log. De bestaande gedeelde v3-site is niet door deze lokale v4-proef vervangen.

Verificatie: check_model.cjs test modelinvarianten; check_workspace.py test klokfasen, leren, uitsluiten, correcties en budgetten; check_score_ranges.py test take-/score-identiteit; check_review.py test concrete A/B-keuzes en het ongewijzigde v3-herstelpunt.
