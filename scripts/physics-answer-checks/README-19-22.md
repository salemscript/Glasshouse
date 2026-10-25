# Physics chapters 19–22 answer checks

All384 listed exercises: chapter19 107, chapter20 89, chapter21 87, chapter22 101. Each source-reviewed contract records every requested numerical result or conclusion, original reasoning, units, assumptions, PDF pages and verification. The corresponding author scripts reproduce calculations; a separate independent review covers all46 conceptual questions.

This batch adds answer checks, not complete worked solutions or lab coverage. Drawings and written proofs are checked through their quantities and conclusions, not automatic evaluation of prose or freehand work. Estimation examples state their assumptions and include general relationships. Printed-key conflicts are explicitly explained where present.

Run from the repository root:

```sh
python scripts/physics-answer-checks/build-19-22.py
node scripts/physics-answer-checks/check-runtime-19-22.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/physics-answer-checks/check-dom-19-22.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/check-math-typography.cjs
python scripts/physics-answer-checks/compare-existing-19-22.py
python scripts/physics-answer-checks/check-source-parts-19-22.py
python tools/verify_export.py --refresh
python tools/verify_export.py
```

The tests use the actual enrichment, response-part discovery, checker and delegated UI event code. They verify correct/blank/incorrect submissions, wrong signs and zero for nonzero quantities, accepted rounding, every choice distractor, per-part buttons, saved-note migration and unchanged answer records outside this batch. Linkedom is development-only. Choices use stable varied ordering. Numeric tolerances remain below nonzero answers; conventional two/three-significant-figure submissions are explicitly accepted.

Final verification: 384 exercises, 894 fields (706 numeric and 188 choice). All 46 conceptual questions were independently cross-reviewed against the original diagrams. Raw-source subpart candidates were reviewed; remaining letters are figure names, function arguments, or neighboring-column text, rather than omitted requested fields. The legacy-key comparison uses the pre-change Git HEAD, not the rebuilt library. Differences are unit conventions, explicit labels on zeros/counts, printed rounding, and documented equivalent angle or charge-position configurations.

Notable corrections and conventions: Chapter 19 uses the stated gas molar mass, mean versus rms speed where appropriate, the stated lunar gravity, and explicit process-average heat capacity. Chapter 20 P37 uses its chapter's refrigeration coefficient definition (heating coefficient is K+1); P65 distinguishes positive heat input from signed net heat. Chapter 21 preserves signed force components, equivalent angles and complete charge-contact sequences. Chapter 22 corrects microscopic-length transcription errors and explains P17's paired charge-position ambiguity. The full UI suites and fraction-rendering regression pass. No non-target answer record changes.
