# v4 — 3 november 2026

Herstelpunt: Git-tag before-v4-20261103, commit 689779e. De gedeelde v3.2.2-presentatie en review-v3 blijven behouden. Comp tool staat nog in review-v3/index.html#cutlist; v4 vervangt alleen de actieve tweede weergave door Score. Nieuwe UI-keuzes lokaal beoordelen voordat we de gedeelde site veranderen.

Werkvolgorde: expliciet model voor werkbelasting/complexiteit, cuetijd en prognose; herstelbare handmatige correcties; opnamebereiken; score met notes zonder compselecties; korte gezamenlijke review met concrete varianten.

Voorlopige keuzen: mm:ss op te nemen muziek per cue (initieel de bestaande muziekduur); gewichten Easy .7, Medium 1, Hard 1.5. Initieel wordt de sessietijd over voorbereiding en gewogen muziekduur verdeeld. Een eenmaal gestarte sessie behoudt haar oorspronkelijke tempo-referentie wanneer de eindtijd verandert: meer beschikbare tijd is geen bewijs van langzamer werken.

Alleen afgeronde cues met betrouwbare gemeten/corrigeerbare werktijd worden als referentie gebruikt. Voorbereiding wordt apart gehouden, verschillende complexiteiten/werkbelasting worden genormaliseerd, en weinig voorbeelden krijgen minder gewicht. Aantal takes is context en bepaalt niet zelfstandig de voortgang. Onvoltooide cues houden minimaal een afrondreserve tot Done of een expliciete resterende-werkschatting. Deze aannames worden zichtbaar en beproefbaar; geen claim dat dit een gevalideerd sessie-algoritme is.

Het hoofdscherm toont beschikbare werktijd voor deze cue en verwachte sessie-uitloop. Kloktijd blijft compact; overige cijfers staan onder Timing details. Muziekduur, moeilijkheid, budget, werkelijk werk en afgerond blijven per cue bereikbaar. Handmatig herstellen mag de opname-identiteit en notes niet veranderen.

Vragen/keuzes pas aan het einde als A/B-review. Geen automatische introductie. Spatie eerst sessie, daarna takes; tijdens tekstinvoer gewone spatie. Brackets cues, Option takes; N opent het noteveld.

## Uitgewerkt

De hoofdweergave toont beschikbare cuetijd en sessieprognose, met een apart detailmenu. Handmatig herstellen en referentiecues uitsluiten zijn actief. ±15/30/60 in Planning past dezelfde eindtijd aan. De startbudgetten worden bewaard; een gecompleteerde cue bevriest zijn leertijd. Opnamebereiken blijven bij echte take-ID's en gaan mee in de take-logexport. Score deelt takes, note-invoer en transport; compselecties zijn verborgen en geblokkeerd zonder de oude data te verwijderen.

Review v4 bevat zes stappen met vijf werkende A/B-keuzes en een scorestap. Werkbelasting kan één expliciete duur of expliciete duren per niet-overlappend maatbereik zijn. Losse leer-/verdelingsvoorbeelden zijn herkenbaar aparte data. Mijn keuzes toont de selectie met download. De kaart blijft versleepbaar. Er is geen automatisch welkomscherm.

Lees PLANNING.md voor formules, afrondreserve, leergewicht, handmatig herstel en meetbeperkingen. Dit is een lokale sessieproef, geen bewezen algoritme en geen duurzame productieopslag.

## Herstelronde v4.1 na afwijzing

De eerste layout is expliciet afgewezen. Herstelpunt: rejected-v4-layout-20261103. Actief is nu dezelfde v4-index met label v4.1, opgebouwd uit de echte v3-hoofdcomponenten. Geen afzonderlijk nieuw dashboard of weggehaalde sessiecontrols. De grote klok, cue en bekende bediening blijven; cue-tijd/prognose vullen die structuur aan. Het pure planningsmodel blijft gelijk.

Takebereiken staan naast de take-identiteit en openen in een compacte verankerde popup met From bar / Till bar. Geen 1–8-default of automatische 2–8/12–19-presets vanuit de review. A biedt één bereik; B toont alleen daadwerkelijk door de gebruiker opgeslagen bereiken. Rijen en omliggende bediening bewegen niet bij openen/typen. De oude take-grid is vervangen omdat de inhoud feitelijk buiten de rij overliep.

Nieuwe check_layout.py meet daadwerkelijke containment en onderlinge overlap op vijf breedtes. Testresultaten alleen niet als ontwerpgoedkeuring presenteren; Floris moet de herstelde proef nog beoordelen.
