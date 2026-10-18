# MandoCues · Prototypes van Floris

Vrijblijvende voorstellen voor de opnameworkflow. De interface is Engels; vragen en toelichting zijn Nederlands.

**Bekijken:** open [index.html](index.html) in de projectroot in je browser. Deze opent het prototype in `prototype/dist/`. Werkt lokaal en offline.

**Verder werken met Codex:** open deze hele map en gebruik [CODEX_STARTPROMPT.txt](CODEX_STARTPROMPT.txt). Lees [AGENTS.md](AGENTS.md) en [HUIDIGE_STAND.md](HUIDIGE_STAND.md) voor de actuele keuzes.

Bouwen en controleren, vanuit deze map:

```sh
python3 -X utf8 prototype/build.py
python3 -X utf8 prototype/check_handoff.py
```

Python 3.10 of nieuwer; geen extra pakketten voor de build. Op Windows kan `py -3` in plaats van `python3`. Alle benodigde score-assets zitten erbij. Optionele browsercontroles staan in [prototype/README.md](prototype/README.md).

Werk in `prototype/src/`, bouw `dist/` opnieuw en commit bron en gegenereerde bestanden samen. Haal vóór wijzigingen de laatste commits op en werk op een eigen branch. Browser-notes worden niet tussen computers gedeeld en verdwijnen bij herladen.

De oorspronkelijke app en scoreboeken worden niet aangepast. Het prototype neemt geen audio op. [START_HIER.md](START_HIER.md) bevat de korte overdracht.
