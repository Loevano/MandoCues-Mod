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

- Latest correction v4.1: Floris rejected the initial v4 layout. Reuse the actual v3 component DOM and column structure; do not replace the whole dashboard again. Preserve the large cue/AM-PM clock and original session actions. New range controls must float without reflow and must fit their rows.
- Never seed real session ranges by selecting an A/B presentation. No invented start/end defaults. Test child containment AND pairwise overlap, not just horizontal page overflow or clickability. check_layout.py reproduces the actual row-collision class of failures.
- Preserve the rejected design via rejected-v4-layout-20261103; the current local entry remains review-v4/index.html with a v4.1 badge. The planner and online v3 are unchanged by this UI repair.
