# Overdracht voor de collega

Open **index.html**. Eén werkruimte met Recording en Cut list; de welkomstmelding laat je kiezen tussen de rondleiding en zelf bekijken. Alles werkt offline.

De rondleiding toont steeds één suggestie. Suggesties staan standaard aangevinkt. Vink uit wat je niet aan Claude wilt meegeven en ga verder. Via Claude-prompt kun je je selectie bekijken, aanpassen, kopiëren of downloaden. De bestaande teksten worden samengevoegd; niet opnieuw gegenereerd. Vragen staan apart en blijven vragen.

Verder werken: open de hele map in Codex en plak CODEX_STARTPROMPT.txt. Lees HUIDIGE_STAND.md voor de laatste keuzes. De vorige vijf prototypes staan onder Git-tag before-unified-ui-20261018.

Bouwen en controleren, met Python 3.10+ zonder extra pakketten:

```sh
python3 -X utf8 prototype/build.py
python3 -X utf8 prototype/check_handoff.py
```

Op Windows kun je python3 vervangen door py -3. Browsercontroles zijn optioneel; zie prototype/README.md.

De GUI is Engels, de uitleg Nederlands. Jouw programma en ontwerpkeuzes gaan voor. Het pakket verandert niets op SoundVibeHQ. Nieuwe demo-notes en takes verdwijnen bij herladen; promptkeuzes blijven alleen lokaal in de browser bewaard.

Voor samenwerken: dezelfde privé-Git-repository, eigen branches, eerst pullen en wijzigingen reviewen. Dit deelt code, geen live browser-sessies. Er is geen server of online account nodig om de pagina te proberen.
