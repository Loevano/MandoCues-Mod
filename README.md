# MandoCues · voorstel van Floris

**Ontwikkelversie: [open lokale v4](review-v4/index.html)** en klik **Review v4** voor de keuzes. V4 richt zich op cue-/sessieplanning, takebereiken en Score met notes.

**Gedeelde presentatie: [v3.2.2 online](https://mandocues-voorstel-floris.superfrog5.chatgpt.site/#recording).** De nieuwe v4 staat nog niet online. De [oude Comp tool](review-v3/index.html#cutlist) is bewaard.

Begin met [PROJECT_KNOWLEDGE.md](PROJECT_KNOWLEDGE.md), [HUIDIGE_STAND.md](HUIDIGE_STAND.md), [AGENTS.md](AGENTS.md) en [WORKFLOW.md](WORKFLOW.md). De root-index en oude overdrachtsmappen tonen eerdere versies.

```sh
python3 review-v4/build.py
node review-v4/check_model.cjs
```

De HTML-build gebruikt alleen Python-standaardbibliotheek en meegeleverde assets. Browserchecks gebruiken apart Playwright/Chrome; de beschikbare lokale runtimes en controles staan in WORKFLOW. Dit is een demo: geen audio-opname, live DAW-koppeling of duurzame opslag van nieuwe takes/notes. Alleen reviewvoorkeuren blijven lokaal bewaard.

Herstelpunt vóór v4: tag `before-v4-20261103`, commit `689779e`. De volledige eerdere kennis blijft in [PROJECT_HISTORY.md](PROJECT_HISTORY.md).
