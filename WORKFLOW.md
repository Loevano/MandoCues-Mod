# MandoCues — werkwijze, tools en geleerde lessen

Bijgewerkt 4 november 2026. Dit document is voor implementatie en overdracht. Besluiten en actuele stand: [PROJECT_KNOWLEDGE.md](PROJECT_KNOWLEDGE.md). Geen credentials of tokens in dit document opnemen.

## 1. Begin bij de juiste map en versie

Werkmap: `/Users/florisheemskerk/Documents/Coding/Mando Cues/MandoCues-Mod`.

```sh
git status --short --branch
git log -5 --oneline
```

De huidige branch heet nog `feature/session-review-v3`, ook voor de nieuwe lokale v4. De branchnaam bepaalt de productversie niet. De root-index en oude overdrachtsmappen zijn historische ingangen. Open expliciet `review-v4/index.html` voor nieuw werk en `review-v3/index.html` voor de bewaarde presentatie/Comp tool.

Voor samenwerken: eerst status/diff controleren, dan passende fetch/pull of merge. Geen werk van Jens of Floris overschrijven. Maak onafhankelijke geteste commits; geen force-push voor gewone synchronisatie. De bestaande SSH-remote is `git@github.com:Loevano/MandoCues-Mod.git`. Een Sites-credential hoort niet bij deze GitHub-repository. Maak niet routinematig een nieuwe SSH-key aan als een bestaande verbinding eerder werkte.

Herstel een oude versie bij voorkeur apart:

```sh
git worktree add ../MandoCues-v3-herstel before-v4-20261103
```

Die checkout bevat de toenmalige `review-v3/index.html`. Reset de actieve werkmap niet. Controleer eerst dat het doelpad nog vrij is.

## 2. Bronlagen en build

| Laag | Gebruik |
| --- | --- |
| `prototype/src` → `prototype/dist` | Bewaarde v2-basis met gedeelde opname-/scorestate en ingesloten assets |
| `review-v3/build.py` | Voegt de kleine v3-lagen toe; bewaarde v3.2.2 is de basis voor v4 |
| `review-v3/minimal.js/css` | Space, versie, gedeelde cuevolgorde, sleepgrepen |
| `review-v3/schedule-timing.js` | Gedeelde secondegrenzen tegen valse planningflikkering |
| `review-v3/note-times.js` | `writtenAt` versus `clockAt`, N, ↓/klokje |
| `review-v3/best-takes.js` | Meerdere Best-takes per cue |
| `review-v3/presentation-tour.js` | Korte versleepbare v3-rondleiding |
| `review-v4/planning-model.js` | Pure schattingsfuncties, zonder DOM of klok |
| `review-v4/workspace.js/css` | Plannings-UI, echte cuewerktijd, correcties, sessiebediening |
| `review-v4/take-ranges.js` | Gewone takes met bereik, bereikpresets, B, log-/Take sheet-export |
| `review-v4/score-workspace.js` | Scoreweergave met gedeeld transport en notes, zonder actieve compselecties |
| `review-v4/review.js` | Zes reviewstappen, werkende A/B-invoer, losse voorbeelden en keuze-export |
| `review-v4/build.py` | Bouwt de volledige zelfstandige v4-HTML boven op de ongewijzigde v3-HTML |

V4-modules worden in bovenstaande volgorde als aanvulling ingeladen. Bestaande functies/state worden deels omwikkeld; lees de actieve definitie en de wrappers voordat je aan gedeelde handlers verandert. Een gegenereerd indexbestand rechtstreeks aanpassen wordt bij de volgende build overschreven.

Vanuit de repository:

```sh
python3 review-v4/build.py
```

Geen npm-install, bundler, frameworkserver, originele scoreboeken of externe onderzoeksprojecten nodig voor deze statische build. Alle scorebeelden zitten in de bron/HTML. De huidige v3 omvat 68 ingesloten scorebeelden; v4 hergebruikt die. Custom PDF-uploads hebben niet automatisch dezelfde gevalideerde mapping.

De v4-build controleert dat hij v3 niet wijzigt. `review-v4/restore.json` bewaart de verwachte SHA256 van die basis. Als bewust een nieuwe basis wordt gekozen, moeten zowel herstelbeleid als tests expliciet worden aangepast. Een hashfout niet oplossen door blind een nieuwe hash te schrijven.

`prototype/build.py`, `prototype/package.py` en `prototype/handoff.py` bouwen/pakken de oude basis; ze produceren niet vanzelf v4. De gedeelde overdrachtsmappen en ZIP’s zijn momentopnamen. Niet ongevraagd als huidige v4 rondsturen of overschrijven.

## 3. Aanwezige runtimes en browsergereedschap

Vastgesteld op deze Mac:

- Python/Playwright: `/Users/florisheemskerk/Documents/Coding/Composition Study/.venv/bin/python`.
- Duurzaam gevonden Node bij Playwright: `/Users/florisheemskerk/Documents/Coding/Composition Study/.venv/lib/python3.14/site-packages/playwright/driver/node`.
- Tijdelijk gedownloade publicatieruntime: `/tmp/mandocues-node-runtime/node-v24.22.2-darwin-arm64/bin/node`. Deze is van nodejs.org gedownload en met SHASUMS256 gecontroleerd. `/tmp` kan later leeg zijn; behandel dit pad niet als installatiegarantie.
- `node` stond niet op de gewone PATH. Eerst bestaande runtime zoeken; niet meteen opnieuw installeren. De genoemde omgeving buiten deze repo is een testhulpmiddel, geen buildvereiste voor de overdracht.
- `prototype/browser_support.py` start eerst een beschikbare Playwright-browser en anders een bestaande Google Chrome/Chromium. `PLAYWRIGHT_CHROMIUM_EXECUTABLE` kan een expliciet geïnstalleerd exemplaar aangeven.

Lees vóór Sites-preview/browserwerk de dan geldende Sites-skill en de toepasselijke lokale-previewreferentie. In deze sessie is een lokale macOS/portable-omgeving gebruikt; de skill onderscheidt die van een beheerde Linux-preview.

Als een headless browser in de sandbox direct met SIGABRT/TargetClosedError stopt, is dat niet vanzelf een appfout. Dezelfde gerichte browsercheck werkte hier met de vereiste uitvoeringsgoedkeuring. Gebruik de toolgoedkeuring voor die check; installeer niet willekeurig nieuwe browsers of verander appcode om een sandboxprobleem te omzeilen.

## 4. Gerichte verificatie

### Gereedschap kiezen

- Zoek bron en handlers eerst met `rg` / `rg --files`; lees gerichte fragmenten in plaats van de hele gegenereerde HTML van circa 7,5 MB.
- Bewerk de kleine JS/CSS-/documentatiebronnen met een gerichte patch. Bouw daarna de HTML; vervang geen actieve bron door een oude handoffkopie.
- Batch onafhankelijke leesacties eventueel parallel. Houd mutaties, build → test → package → save → deploy en goedkeuringsstappen achter elkaar.
- Gebruik Playwright voor echte browserinteractie en een gecontroleerde klok voor tijdgevallen. Inspecteer screenshots met de lokale image-viewer wanneer tekstomloop of doelkaders niet uit DOM-asserts blijken. Een screenshot alleen bewijst geen statebehoud.
- Voor de pure berekening is Node met assert voldoende. Maak voorbeelden voor de review apart van echte sessiemetingen en test dat een voorbeeld geen takes/notes toevoegt.
- Gebruik de native Sites-tools voor hosting; geen browserautomatisering of nieuwe plugin nodig als de beschikbare tools de actie al ondersteunen. Git gebruikt hier de bestaande SSH-remote, niet een Sites-token.
- Voor later Pro Tools-onderzoek: lees de bewaarde bronnen en raadpleeg primaire Avid/EBU/MIDI-documentatie. BWF MetaEdit is een onderzocht hulpmiddel voor metadata-uitlezing; er is geen WAV-import in onze demo. Installeer of verbind niets bij de engineer zonder een concrete opdracht.

Commando’s hieronder zijn voorbeelden vanuit de repository. Kies alleen controles die bij de wijziging horen.

```sh
python3 review-v4/build.py
node review-v4/check_model.cjs
```

Bij ontbrekende `node` op PATH mag de gevonden runtime met volledig pad worden gebruikt:

```sh
"/Users/florisheemskerk/Documents/Coding/Composition Study/.venv/lib/python3.14/site-packages/playwright/driver/node" review-v4/check_model.cjs
```

Browserchecks met de bestaande testomgeving:

```sh
"/Users/florisheemskerk/Documents/Coding/Composition Study/.venv/bin/python" review-v4/check_workspace.py
"/Users/florisheemskerk/Documents/Coding/Composition Study/.venv/bin/python" review-v4/check_score_ranges.py
"/Users/florisheemskerk/Documents/Coding/Composition Study/.venv/bin/python" review-v4/check_review.py
"/Users/florisheemskerk/Documents/Coding/Composition Study/.venv/bin/python" review-v4/check_layout.py
```

| Check | Betekenis |
| --- | --- |
| `check_model.cjs` | Gewogen werkbelasting, kleine datasets/uitschieters, uitsluiten, budgetbehoud, eindtijd onafhankelijk van werktempo, afrondreserve |
| `check_workspace.py` | Geen secondeflikkering, cuecorrecties, niet leren vóór Done, bevroren afgeronde referentie, uitsluiten, eindtijd met beide tekens, tijd loopt door in een open editor |
| `check_score_ranges.py` | Doorlopende take-nummers/ranges, export, gedeelde opname-/notestate, compdata behouden, notes maken/verwijderen/undo, shortcuts, globale zoom, 1512/900/390 breedtes |
| `check_layout.py` | Take-inhoud binnen de rij én onderling zonder overlap, oorspronkelijke controls behouden, geen fake-ranges, geen reflow bij maatkeuze, exacte highlight, vijf breedtes |
| `check_review.py` | Ongewijzigde v3-SHA, herhaalbare v4-build, zes A/B-stappen, bereikduurvalidatie, geïsoleerde voorbeelden, export/opslag van reviewkeuzes, slepen en smalle schermen |
| `prototype/check_handoff.py` | Schone geïsoleerde rebuild van de **bewaarde basis**; geen v4-interactietest |

Chrome/Chromium is getest; Safari/WebKit niet apart. Screenshots `review-v4/check-*.png` zijn lokale controlebestanden en worden niet gecommit. Een browsercheck met gecontroleerde tijd moet de klok expliciet vooruitzetten; echte sleeps zijn daarvoor geen vervanging.

Historische checks niet blind als actuele v4-eisen gebruiken. `review-v3/check_review.py` verwacht onder meer dat de actieve hostingcheckout nog de v2-hostingkopie bevat. Die plek is bewust bijgewerkt naar de gepubliceerde v3.2.2. De v2-backup staat nog veilig in de backupmap; de oude assert is versiegebonden/verouderd. Oude rijhoogte- en Command+Enter-verwachtingen horen evenmin bij de nieuwe v4. Pas een test alleen bewust aan op een bevestigd nieuw gedrag; verklaar een echte fout niet weg als ‘oude test’.

## 5. Gevonden fouten: oorzaak en beste aanpak

### V4-layout overloopt ondanks geslaagde kliktests

De eerste v4-layout is door Floris afgewezen. Echte browsermetingen vonden 108 px take-inhoud in een vaste rij van 78 px. Nieuwe gridregels botsten met bestaande `.take-label-input`-regels; de patch had een niet-bestaande `.take-label` aangenomen. Controls bleven klikbaar en de documentbreedte bleef passen, maar kinderen overlapten aangrenzende rijen. Vergelijk dus DOM en berekende bounding boxes, inclusief onderlinge intersecties, niet alleen scrollWidth of zichtbaarheid.

De v4.1-herstelronde hergebruikt de werkende v3-hoofdcomponenten en kolomstructuur. Nieuwe maatbediening opent als een verankerde popup buiten de normale flow. Controleer expliciet dat recordknop, cuenavigatie, tijdlijn en take-rijen dezelfde bounding boxes houden tijdens openen en typen. Escape moet de bovenste editor sluiten; de oude document-level tourhandler mag niet alvast de hele review sluiten.

De ranges-B-review schreef ook werkelijk fictieve presets naar de sessie. Dit is verwijderd: een A/B-keuze mag uitsluitend de invoervariant wijzigen, niet muziekdata toevoegen. Begin-/eindmaat blijven leeg tot echte invoer. `check_layout.py` vergelijkt de sessie vóór/na variantwissels en controleert vijf breedtes. De tutorialhighlight richt zich op de knop; geen geanimeerde sprong vanuit het oude hoofdvakkader. Vroege v4 is herstelbaar via tag `rejected-v4-layout-20261103`.

### Planning knippert groen/oranje na een cuewissel

Gereproduceerd met Playwright-klok: sessie en cue begonnen op verschillende milliseconden en werden elk apart afgerond. Elk seconde-interval kon tijdelijk een valse −00:01 ontstaan; herhaald wisselen verloor ook fracties.

Oplossing in `review-v3/schedule-timing.js`: cue- en sessiewerk gebruiken dezelfde secondegrenzen. V4 gebruikt die fase ook voor de tijd tot de eindtijd. Geen drempelband, kleurvertraging of debounce toevoegen die een rekenfout slechts verstopt. Test herhaalde cuewissels, echte uitloop, de vijfminutengrens, pauze en einde/hervatten.

### Bewaren van een editor wist ondertussen verstreken tijd

Een veld met de werktijd van het openingsmoment mag niet bij elke Save als nieuwe correctie worden toegepast. V4 bewaart wat getoond was en corrigeert alleen als het veld werkelijk gewijzigd is. Een ongewijzigde resterende-werkschatting houdt ook haar bestaande anker. Test met open dialog + gecontroleerde tijd vooruit.

### Afgeronde cue blijft ongemerkt bijleren

Done zet de gemeten referentiewerktijd vast. Wachten na Done mag die sample niet blijven verhogen. Heropenen begint vanaf de bewaarde werktijd, zonder idle-tijd als cuewerk te boeken. Eindtijd/werkbudget en samples zijn verschillende gegevens.

### Compdata verliezen bij ‘Score vereenvoudigen’

Niet leegmaken om kleuren te verbergen. V4 onderdrukt de compweergave en bewerkingsroutes, met behoud van oude selecties en v3-bron. Vergelijk echte take-ID’s/notes/scorelagen vóór en na een viewwissel of Command-drag. De geselecteerde take en de lopende take moeten onafhankelijk blijven.

### Grote sprongen door één afwijkende cue

Normaliseer eerst opnameomvang en complexiteit, zet voorbereiding apart en houd de steekproef klein in gewicht. Neem geen technische storing automatisch als universeel werktempo over. Uitsluiten verandert de al verstreken sessiekloktijd niet. Meer tijd geven mag de gemeten productiviteit niet herschrijven.

### Oude bekende UI-punten

De vertraagde toggle-handler bij Go to cue kan zoektekst resetten; deze is niet als opgelost gevalideerd. Ook de blauwe Start session-kleur is niet overal gelijk in de compacte Score-balk. V4 verbergt de oude All takes-toggle met zijn verkeerde tooltip; dat herstelt de oude v3-toggle niet. Zie PROJECT_HISTORY voor het oorspronkelijke bewijs.

## 6. Sites-publicatie: exacte bestaande identiteit gebruiken

Deze gegevens zijn de laatst bevestigde publicatie, niet een opdracht om bij documentatiewerk te deployen:

- Actief account: Floris, gecontroleerd via de Sites-response met `florisheemskerk01@gmail.com` als eigenaar.
- Site: `appgprj_6ad673aeeebc8191a4882963260b87df`.
- URL: `https://mandocues-voorstel-floris.superfrog5.chatgpt.site`.
- Broncheckout: `../sites/mando-voorstel-floris` ten opzichte van deze repository.
- Manifest daar: `.openai/hosting.json`, `static.directory = dist`.
- Laatste geslaagde hostingversie: **3**, met presentatie **v3.2.2**. De exacte saved-version-ID, deployment-ID en hostingbroncommit staan in `review-v3/publication.json`.
- De online site is openbaar zonder account voor mensen met de URL. `noindex, nofollow, noarchive` en `robots.txt` met Disallow zijn zoekmachineverzoeken, geen wachtwoord of echte linkbeveiliging.
- Er is geen apart hostingabonnement afgesloten. Kosten/limieten niet onderzocht; geen onbeperkt gratis hosting beloven.

**Voor iedere geautoriseerde publicatie:**

1. Lees de actuele **Sites**-skill; toolnamen/contracten kunnen veranderen. Ontdek relevante native tools via hun metadata. Gebruik de provider-tools in plaats van browserklikken als ze de actie ondersteunen.
2. Lees het manifest en doe `get_site`. Controleer account/eigenaar, project-ID, audience en bestaande URL. Bij twijfel `list_sites` raadplegen vóór een nieuwe Site wordt gemaakt.
3. Vraag een verse `create_source_repository_write_credential` voor exact dezelfde Site. Bewaar die alleen in sessiegeheugen. De bronhelper krijgt de credential via verborgen stdin, niet als CLI-argument of tijdelijk bestand.
4. Open eerst de bestaande bron via `site-workflow.mjs --project-id <exact-id>` zonder archivePath. Start de helper met een TTY en korte yield; geef na de melding over verborgen invoer één newline-afgesloten JSON-object met de credential. Bewaar het volledige openingsresultaat met checkout_path.
5. Wijzig de geretourneerde checkout vanuit de geteste build. V3-publicaties kopiëren `review-v3/index.html` naar `dist/index.html`, met alleen de noindex-metatag als toevoeging en `dist/robots.txt`. Een toekomstige v4-publicatie vraagt een bewuste bronkeuze én behoud van de v3/Comp-link of een meegeleverd archief; niet alleen de bestandsnaam verwisselen.
6. Laat dezelfde helper synchroniseren/verpakken met het eerdere `source`-resultaat, de credential, alleen resterende checks in `commands` en een **absoluut archivePath buiten de checkout**. Een buildless HTML-site heeft geen npm-build nodig. De helper commit/pusht en controleert de hostingbron.
7. Geef de **exacte** geretourneerde `project_id`, volledige `commit_sha` en `archive` aan `save_site_version`; geef de geretourneerde saved-version-ID aan `deploy_site_version` voor de bestaande publieke audience. GitHub’s appbroncommit is niet deze hostingbroncommit. Archief en broncommit moeten exact bij elkaar horen.
8. Poll alleen als de deployment pending/building/publishing is. `succeeded` met URL is het publicatiebewijs; geen onnodige dubbele deployment. Behoud bestaande audience; wijzig die niet alleen om te kunnen deployen.
9. Werk publication.json en de kennis bij na succes. Rapporteer wat echt online staat. Native private-publicatieroutes worden volgens de skill gebruikt als ooit bewust een owner-private Site wordt gekozen.

Het momenteel aanwezige helperpad is `/Users/florisheemskerk/.codex/plugins/cache/openai-curated-remote/sites/1.1.3/scripts/site-workflow.mjs`. Dit is een versiegebonden cachepad: bij ontbreken eerst de huidige skill/catalogus raadplegen. De Node-directory moet voor child-processen zo nodig ook op PATH staan.

### Account-/URL-probleem dat werkelijk is voorgekomen

De publicatietools gebruikten tijdelijk het Guido-/gheeneman-account, ook toen Floris dacht al te zijn omgeschakeld. De oude Floris-Site gaf `project_not_found`, maar was niet verdwenen. Na de accountwisseling verscheen hij opnieuw in `list_sites` met Floris als eigenaar en werkte dezelfde project-ID weer.

De tijdelijke gheeneman-Site `appgprj_6aea39b640e08191927568766a425501`, checkout `../sites/mando-voorstel-v3-2`, is **niet de actieve publicatie**. De oude URL kan nog bestaan; hij is niet verwijderd. Pas geen verkeerde-accountsite aan om een ontbrekend project te ‘repareren’.

Een slug wijzigen verandert de sitenaam, niet het accountsegment van de URL. De tools boden geen directe accountwissel. De gebruiker wisselde de sessie/account; daarna controleerden we opnieuw de native Site-responses. Publiceer dus pas onder de bevestigde eigenaar. Een eigen domein is een andere route met DNS-werk en was hier niet ingesteld.

### Grote HTML-upload: HTTP 400

De circa 7,5 MB zelfstandige HTML gaf `RPC failed; HTTP 400` bij Git-push naar de Sites-bron. De helper had lokale commits behouden. Op 3 november werkte de herhaling na deze **checkout-lokale** instellingen:

```sh
git config http.postBuffer 104857600
git config http.version HTTP/1.1
```

Dit zijn geen globale Git- of netwerkfixes en geen standaardstap voor iedere fout. Controleer eerst de fout en remote-status, behoud dezelfde project-ID en hervat de helper; geen force-push of nieuwe Site. Credentials in foutoutput blijven geredigeerd. Andere authenticatiefouten vragen een verse credential; lees de actuele skill/troubleshooting.

## 7. Wat delen en wat bewaren

Een `file:///Users/...`-link werkt alleen op de eigen computer. De zelfstandige HTML kun je als bestand delen, maar ontvangers zien dan geen volgende lokale edits. Een gedeelde website vraagt opnieuw publiceren; een GitHub-push alleen is daarvoor onvoldoende.

V4 is lokaal gelaten op verzoek om eerst de prototypes te beoordelen. Publiceer die niet automatisch bij kennis-/documentatiewerk. Behoud de huidige gedeelde v3 en het herstelmanifest. Voor later zijn ook de browserdata van een echte sessie niet duurzaam: reviewkeuzes blijven lokaal, maar takes/notes/timingmetingen verdwijnen bij herladen. Bouw productie-opslag pas als een afzonderlijke gevraagde stap.

De centrale Coding/Knowledge-verwijzing blijft wijzen naar PROJECT_KNOWLEDGE.md. Daar verwijst het overzicht naar dit werkdocument, PLANNING, de bewaarde Pro Tools-onderzoeken en PROJECT_HISTORY. Zo blijft kennis vindbaar zonder meerdere tegenstrijdige ‘laatste versies’.
