# Prototypes van Floris

Open `dist/index.html` in je browser. Dit zelfstandige bestand werkt offline, zonder installatie. De vijf genummerde HTML-bestanden openen ieder een voorstel. Werk in `src/`, niet rechtstreeks in de gegenereerde HTML.

## Bouwen

Python 3.10 of nieuwer, zonder extra pakketten. Vanuit deze map:

```sh
python3 -X utf8 build.py
python3 -X utf8 check_handoff.py
```

Op Windows: vervang `python3` door `py -3`. `-X utf8` zorgt dat de Nederlandse tekst op alle systemen goed wordt gelezen.

Alle scorebeelden, mappings en het PDF-fragment zitten in `src/score-assets/`. De volledige originele boeken en het andere scoreproject zijn geen buildvereiste. Een eigen PDF opent lokaal zonder automatische maatmapping. Dit prototype neemt geen audio op en synchroniseert niet met een DAW of film. Nieuwe demo-invoer verdwijnt bij herladen.

## Browsercontroles (optioneel)

Voor de controles is Playwright nodig; voor bekijken en bouwen niet. Gebruik bij voorkeur een aparte Python-omgeving. Binnen die omgeving:

```sh
python -m pip install playwright
python -m playwright install chromium
python -X utf8 check_english_ui.py
python -X utf8 check_revision_oct18.py
```

Deze controles testen de Engelse interface, note-layout, rustige A/B-bediening, vaste knopposities, opnamebediening, vergelijken en score-notes. `check_prototype.py` controleert ook de homepagina en promptselectie. Aanvullende `check_*.py`-bestanden testen specifieke flows. Uitvoer en screenshots komen in `checks/`.

`browser_support.py` gebruikt eerst de Playwright-browser, anders een gevonden Chrome-installatie. Eventueel kun je `PLAYWRIGHT_CHROMIUM_EXECUTABLE` instellen op een eigen browserpad. Controles van hashes van originele boeken worden expliciet overgeslagen als die boeken ontbreken; het prototype gebruikt de meegeleverde assets.

## Delen

- `python3 -X utf8 package.py` maakt het kleine ZIP-pakket met alleen het werkende prototype en uitleg in de bovenliggende map.
- `python3 -X utf8 handoff.py --output ../MandoCues-overdracht-nieuw` maakt een volledige overdrachtsmap en ZIP met broncode, assets, controles en Codex-instructies. Een bestaande doelmap wordt niet overschreven.
- In een broncode-overdracht staan `START_HIER.md`, `AGENTS.md` en `HUIDIGE_STAND.md` één map hoger. Dat laatste document gaat voor oude opmerkingen in `src/feedback.md`.

De actuele app-interface is Engels. Vragen en uitleg voor de collega blijven Nederlands. De originele SoundVibeHQ-app en originele PDF’s worden niet gewijzigd.
