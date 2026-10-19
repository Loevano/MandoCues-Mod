# MandoCues · één voorstel

Open `../index.html` of `dist/index.html`. De offline pagina heeft Recording en Comp tool met gedeelde gegevens. Bij openen kies je Rondleiding starten of Zelf bekijken. A toont de invulvelden bovenaan; B plaatst ze in Planning naast de titel. B is voorlopig gekozen; beide gebruiken dezelfde takes, notes en opnamebediening.

## Bouwen

Python 3.10 of nieuwer, zonder extra pakketten. Vanuit deze map:

```sh
python3 -X utf8 build.py
python3 -X utf8 check_handoff.py
```

Op Windows: vervang python3 door py -3. Alle benodigde scorebeelden en mappings zitten in `src/score-assets/`; de oorspronkelijke boeken zijn geen buildvereiste.

De bron staat in `src/`. `unified-app.js` hergebruikt de bestaande opname- en scorecomponenten met één state. `proposal-tour.json` bevat de 25 korte suggesties en vaste promptteksten; `proposal-tour.js` regelt de rondleiding en selectie. `build.py` genereert de offline app en actuele documenten. Bewerk `dist/` niet rechtstreeks.

## Browsercontroles

Optioneel, met Playwright in een aparte Python-omgeving:

```sh
python -m pip install playwright
python -m playwright install chromium
python -X utf8 check_unified_workspace.py
python -X utf8 check_proposal_tour.py
python -X utf8 check_recording_shortcut.py
python -X utf8 check_main_panel.py
python -X utf8 check_go_to_cue.py
python -X utf8 check_original_controls.py
python -X utf8 check_panel_options.py
python -X utf8 check_planning_sessions.py
python -X utf8 check_fresh_timing.py
python -X utf8 check_take_log.py
python -X utf8 check_auto_plan.py
python -X utf8 check_take_labels.py
python -X utf8 check_take_delete.py
python -X utf8 check_take_range.py
python -X utf8 check_cue_fields.py
python -X utf8 check_recording_scroll.py
python -X utf8 check_note_metadata.py
python -X utf8 check_note_time_width.py
python -X utf8 check_all_takes.py
python -X utf8 check_score_note_drag.py
python -X utf8 check_score_settings.py
python -X utf8 check_score_overlap.py
python -X utf8 check_score_take_scroll.py
python -X utf8 check_score_zoom.py
python -X utf8 check_score_page_layout.py
```

`browser_support.py` gebruikt Playwright Chromium of een gevonden Chrome-installatie. Je kunt ook PLAYWRIGHT_CHROMIUM_EXECUTABLE instellen. Uitvoer en screenshots komen in `checks/`.

`legacy-checks/` hoort uitsluitend bij de vorige vijf prototypes, herstelbaar via Git-tag `before-unified-ui-20261018`. Draai die oude controles op die oude versie.

## Delen

`python3 -X utf8 package.py` maakt een klein ZIP-pakket om de pagina te proberen. `python3 -X utf8 handoff.py --output ../../MandoCues-overdracht-rondleiding` maakt een broncode-overdracht met assets, controles en Codex-instructies. Het doel mag nog niet bestaan.

De GUI is Engels; rondleiding en vragen zijn Nederlands. Alleen promptkeuzes worden lokaal bewaard. Nieuwe demo-invoer verdwijnt bij herladen. Er is geen audio-opname, DAW-/filmverbinding, live score following of server. De oorspronkelijke app en PDF-boeken blijven ongewijzigd.

`dist/Pro-Tools-takekoppeling.md` beschrijft de onderzochte takekoppeling, voorwaarden en officiële bronnen. Nieuwe demo-takes loggen hun lokale start/stop met datum; PDF → Take sheet biedt een JSON-momentopname. Dit is geen DAW-bevestiging of synchronisatie, en herladen wist de demo-invoer.
