# v4 — session planning first

- Latest call feedback supersedes older v3 requirements: timing is the primary task; fewer clocks; editable recording workload; learned cue estimates; simple bar ranges; Score replaces Comp tool in the active UI.
- Preserve review-v3 and the before-v4-20261103 Git tag. Comp tool remains available there. Do not change its score layers or source PDFs.
- Build with python3 review-v4/build.py. index.html is generated from the preserved v3 page plus local v4 modules. English product UI; concise Dutch review copy.
- This is a new local review version. Do not replace the shared v3 presentation until Floris requests publication of v4.
- No live DAW integration. Cue working time, including time between takes, is the primary measurement; take duration/count are context, not independent evidence of progress.
- Distinguish available cue time from forecast remaining work. An unfinished cue must not silently become zero remaining work when its estimate expires. Only completed, included cues train the estimator; expose correction and exclusion.
- Recording duration is explicit mm:ss; do not infer it from bar count without tempo information. Ranges describe takes, not separate take-number sequences or overdubs.
- Present unanswered choices together as working A/B previews in the v4 review, no repeated async questions. Keep existing Space/bracket/Option shortcuts; introduce no reserved Mac commands.
- Keep each independent change in its own validated commit. Run meaningful planning invariants and browser flows.
