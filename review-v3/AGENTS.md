# Lokale review v3

- Lees PLAN.md en de oorspronkelijke bevindingen. Dit is een review na gebruik van de originele site.
- v2 is bewaard via tag before-session-review-v3-20261102 en een geverifieerde backup. Niet overschrijven.
- De actieve pagina bouwt boven op de bestaande v2-app met alleen minimal.js en minimal.css; wijzig index.html niet direct. De brede afgewezen experimenten blijven apart als experiments.html en via tag v3-full-ab-review-20261102.
- Laatste besluit, 3 november: behoud de vorige (A/v2-)indeling. Neem alleen cuevolgorde via de bolletjesgreep over, plus de eerder bevestigde spatiebediening. Geen extra panelen, klokinstellingen, nieuwe planning, maatbereik-UI of grote A/B-rondleiding toevoegen. De oude tutorial voorlopig laten zoals die is.
- GUI Engels; reviewuitleg Nederlands, kort en buiten de productflow.
- Spatie is de voorlopig gewenste handmatige transporttoets; tijdens tekstinvoer blijft het tekst. De eerste spatie start alleen de sessie. Pro Tools is voorlopig uitgesteld; geen integratiewerk of vragen daarover in deze ronde.
- Publiceer deze experimenten niet over de bestaande demo voordat Floris de gekozen wijzigingen beoordeeld heeft. Dit is een expliciet lokale reviewfase.
- Bouw met python3 review-v3/build.py vanuit de repository; de bestaande prototype/dist/index.html blijft byte-identiek.

- Presentatie-update v3.1 (3 november): stel het lokale versienummer in version.json in en toon het subtiel in de bovenbalk. questions.json bevat de drie actuele punten: planningidee, essentiële klokken en betrouwbare voor-/achterstand. De oude take-duur/New take/vergeten-start-vragen en de Command+Enter-suggestie vervallen. Space bedient transport; Command+Enter doet dat niet meer. Verder geen UI-/plannerwijzigingen.
