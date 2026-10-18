# MandoCues · voorstel van Floris

**Open [index.html](index.html)** voor één werkruimte met **Recording** en **Cut list**. Bij openen kies je **Rondleiding starten** of **Zelf bekijken**. De rondleiding toont per suggestie een korte uitleg en een checkbox voor je Claude-prompt. Alleen aangevinkte tekstonderdelen gaan mee.

Recording gebruikt bediening bovenaan en een compacte balk bij scrollen. Cut list behoudt de bestaande scorebediening en All takes. Beide delen cues, takes, notes en beoordelingen. De GUI is Engels; rondleiding en vragen zijn Nederlands. Alles blijft vrijblijvend.

Voor Codex: [CODEX_STARTPROMPT.txt](CODEX_STARTPROMPT.txt), [AGENTS.md](AGENTS.md) en [HUIDIGE_STAND.md](HUIDIGE_STAND.md).

```sh
python3 -X utf8 prototype/build.py
python3 -X utf8 prototype/check_handoff.py
```

Python 3.10+, zonder extra pakketten voor de build. Alle score-assets zitten erbij. Zie [prototype/README.md](prototype/README.md) voor browsercontroles.

Werk in `prototype/src/`, bouw `dist/` opnieuw en commit bron en uitvoer samen. Haal vóór wijzigingen de laatste commits op en werk op een eigen branch. Browser-notes worden niet tussen computers gedeeld en verdwijnen bij herladen.

De vorige versie is bewaard als Git-tag `before-unified-ui-20261018` (commit `d5f7119`). Herstelinstructies staan in HUIDIGE_STAND.md. De oorspronkelijke app en scoreboeken worden niet gewijzigd; de demo neemt geen audio op.
