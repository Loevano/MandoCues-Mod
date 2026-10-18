# Overdracht voor Jens

Dit is het werkende prototype én de broncode. Uitpakken en de hele map bewaren.

**Bekijken:** open `prototype/dist/index.html` in je browser. Werkt offline, zonder installatie.

**Verder werken:** open deze hele map in Codex en plak de tekst uit `CODEX_STARTPROMPT.txt`. De partituurbeelden en alle bestanden voor de build zitten erbij; Floris’ Mac is niet nodig.

**Opnieuw bouwen** vanuit deze map, met Python 3.10 of nieuwer:

```sh
python3 -X utf8 prototype/build.py
python3 -X utf8 prototype/check_handoff.py
```

Op Windows kun je `python3` vervangen door `py -3`. Voor bekijken en bouwen zijn geen extra Python-pakketten nodig. Browsercontroles zijn optioneel; zie `prototype/README.md`.

De interface is Engels; de voorstellen en vragen zijn Nederlands. Alles blijft een suggestie: jouw programma en ontwerpkeuzes gaan voor. Dit pakket past niets aan op SoundVibeHQ.

**Let op:** nieuwe notes en takes in de demo verdwijnen bij herladen. Het pakket bevat de voorbeelddata, niet Floris’ ingevulde browser-sessie.

## Samen verder werken

De eenvoudigste vervolgstap is één gedeelde privé-Git-repository van deze map. Ieder opent zijn eigen kopie in Codex en werkt op een eigen branch; wijzigingen voeg je samen via commits en reviews. `prototype/src/` en de meegeleverde assets zijn de bron. `dist/` bouw je daarna opnieuw.

Dat deelt de code, niet de notes die je in de browser typt. Voor gedeelde sessiedata is aparte opslag nodig. Er is nu geen repository aangemaakt of iets online gezet.
