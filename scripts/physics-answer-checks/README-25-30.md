# Physics chapters 25–30 answer checks

Scope: all 621 listed exercises: chapter25 91, chapter26 96, chapter27 118, chapter28 104, chapter29 99, chapter30 113. Source-reviewed contracts record requested numerical results and conclusions, original reasoning, units, signs, assumptions, source PDF pages and verification. Author scripts reproduce calculations. Separate cross-reviews cover all70 conceptual questions against the original diagrams.

This adds answer checks, not a claim of complete worked solutions or lab coverage. Drawings and proofs are checked through their requested quantities and conclusions; freehand work and prose are not automatically evaluated. Estimation examples state assumptions and general relationships; source-key conflicts are explained where applicable.

Reproduce from the repository root:

```sh
python scripts/physics-answer-checks/build-25-30.py
node scripts/physics-answer-checks/check-runtime-25-30.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/physics-answer-checks/check-dom-25-30.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/check-math-typography.cjs
python scripts/physics-answer-checks/compare-existing-25-30.py
python scripts/physics-answer-checks/check-source-parts-25-30.py
python tools/verify_export.py --refresh
python tools/verify_export.py
```

Tests exercise actual enrichment, response discovery, checking and delegated UI events: correct/blank/invalid/wrong submissions, wrong signs, zero versus nonzero quantities, accepted rounding and equivalents, every choice distractor, per-part controls and saved-note migration. Non-target answer records must remain unchanged. Linkedom is development-only. Choice order varies deterministically; numeric tolerances remain below nonzero answers and accept conventional two/three-significant-figure results explicitly.

Final verification: 621 exercises and 1,465 fields (1,087 numeric, 378 choice). All70 conceptual questions independently source-reviewed and cross-compared. Reviewed subpart-scan flags are figure labels, mathematical arguments or neighboring OCR, not omitted requested answers. The source-key comparison uses the original pre-change Git HEAD. Remaining differences are converted units, printed rounding, signed versus magnitude labels, equivalent angles and documented source/printed-key conflicts.

Corrections before publication include capacitor network and outer-wire connectivity (25), center-intercept current-density ranking and the shortened-heater source-key conflict (26), maze nodes, field direction and inherited micro-unit transcriptions (27), microscopic dimensions and cross-product signs (28), exact path winding and field-cancellation geometry (29), and Lenz-law directions, loop rankings and literal-source component values (30). Separate per-chapter audits and cross-review reports record these decisions. The root spot checks independently verify two linked Ampere paths, graph-derived arc angle, maze current and a motional-emf maximum. Cases involving charged floating nodes, estimates or omitted conditions explicitly state their grading scope. Checks cover final quantities and conclusions; they do not automatically assess freehand drawings or full written derivations.
