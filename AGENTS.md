# Werken aan MandoCues

## Eerst lezen

- PROJECT_KNOWLEDGE.md is de actuele bron van projectkennis. Lees ook HUIDIGE_STAND.md en WORKFLOW.md.
- Actieve ontwikkeling is review-v4; de online presentatie blijft v3.2.2. Lees review-v4/AGENTS.md voor de actuele implementatieafspraken.
- PROJECT_HISTORY.md, oudere feedback en oude overdrachtsmappen zijn geschiedenis. Nieuwste gebruikersbesluiten gaan voor oudere instructies. De oorspronkelijke AGENTS.md is daar volledig bewaard.

## Scope en versiebeheer

- Maak voor iedere afzonderlijke wijziging een eigen commit en valideer die gericht. Bewaar bron en bijbehorende gegenereerde uitvoer samen.
- Bewerk v4-bron in review-v4; bouw met python3 review-v4/build.py. Niet rechtstreeks index.html aanpassen.
- Laat review-v3, prototype/src, prototype/dist en het before-v4-20261103-herstelpunt intact zolang ze de bewaarde basis zijn. Een bewuste basisupgrade vraagt ook bijwerken van manifests en passende testverwachtingen; niet stilzwijgend rebuilden om een fout te maskeren.
- De Comp tool en de afgewezen A/B-proef blijven herstelbaar; maak ze niet opnieuw de actieve v4-richting.
- Online v3 niet door v4 vervangen zonder expliciet publicatieverzoek. Lokale builds/GitHub-pushes zijn geen deployment. Bij geautoriseerde publicatie de actuele Sites-skill gebruiken en dezelfde Site-identiteit behouden.
- Check branch/status vóór pull, merge of commit. Bewaar werk van Jens en Floris. Herstel oude versies in een aparte worktree, niet met reset van de actieve map.

## Productafspraken

- Tijdplanning en overzicht zijn primair. Opnameomvang, complexiteit en werkelijk cuewerk zijn de basis; take-aantal of take-duur bewijst geen voortgang.
- Houd beschikbare cuetijd en verwacht resterend werk apart. Verlengde eindtijd is geen bewijs van lager werktempo. Alleen afgeronde, betrouwbare cues leren; correcties/exclusies moeten begrijpelijk en herstelbaar blijven.
- Geen live Pro Tools-integratie in deze ronde. Bewaar het eerdere onderzoek zonder ongeteste kloktijd-/metadata- of SDK-claims als werkende koppeling te presenteren.
- GUI Engels; review/vragen Nederlands en beknopt. Vertaal geen cuecodes, oorspronkelijke titels of gebruikersnotes.
- Floris beantwoordt open ontwerpkeuzes achteraf via concrete prototypes in één review. Ga door met redelijke voorlopige keuzes; geen herhaalde losse vragen. Geen automatische welkomdialoog.
- Vaste cue-/take-identiteiten en knopposities, duidelijke lopende take, geen take-hernummering bij verwijderen, geen verloren notes of Comp-data. Geselecteerde en lopende take zijn onafhankelijk.
- Space start eerst alleen de sessie en daarna takes; tekstvelden houden gewone spaties. Brackets cues, Option takes, N noteveld, B v4-bereik. Geen nieuwe Control-cijferkeuze of browser-/systeemsneltoetsen zonder reden. Bescherm tekst, modals, IME, key-repeat en slepen.
- Notes bewaren geschreven tijd apart van bewerkbare kloktijd; ↓ is nu, klokje is oorspronkelijke tijd. Enter slaat op en zet een volgende klaar. Geen automatisch maatnummer uit de take-timer.
- Score blijft groot en doorlopend, met globale zoom en notes. Compselecties zijn in v4 verborgen/geblokkeerd, niet gewist. Bron-PDF’s blijven intact; een benaderde mapping is geen notatie-engine.

## Tools en bewijs

- Gebruik de bestaande runtimes en browser_support.py volgens WORKFLOW. Installeer niet opnieuw omdat node niet op PATH staat.
- Draai tests passend bij de gewijzigde versie; oude v2-/v3-tests kunnen bewuste v4-keuzes weerspreken. Leg een echte fout versus verouderde verwachting expliciet vast.
- Voor klokfouten gecontroleerde tijd en cuewissels testen; geen kunstmatige drempel om knipperen te verbergen. Gebruik pure modeltests voor rekeninvarianten en browsertests voor identiteit, correcties en interactie.
- Sites-account vóór publiceren controleren met list_sites/get_site. project_not_found kan een ander account betekenen. Gebruik de Floris-Site uit review-v3/publication.json; maak geen nieuwe site alleen wegens een accountfout.
- Credentials alleen in sessiegeheugen en verborgen stdin van de Sites-helper. Nooit in Git, docs, commandoregel of logs. GitHub en Sites gebruiken verschillende repositories/commit-SHA’s.
- Werk kennis bij na echte besluiten, gevonden oorzaken, nieuwe testresultaten of publicatie. Bewaar één actuele waarheid met verwijzingen naar geschiedenis en onderzoek.
