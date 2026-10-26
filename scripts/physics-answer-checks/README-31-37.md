# Physics chapters 31–37 answer checks

Scope: all 828 listed exercises in chapters31–37, with source-reviewed numerical results and conclusions for every requested part. Per-chapter contracts record original reasoning, units, signs, assumptions, PDF pages and verification. Author scripts reproduce calculations; independent conceptual cross-reviews cover all86 questions. Chapter30 was already completed and is preserved.

This adds answer checks, not a claim of complete worked solutions or lab coverage. Drawings and proofs are checked through their requested quantities and conclusions, not automatic evaluation of freehand work or prose. Estimates state assumptions and general relationships; source-key conflicts are explained where applicable.

Reproduce from the repository root:

```sh
python scripts/physics-answer-checks/build-31-37.py
node scripts/physics-answer-checks/check-runtime-31-37.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/physics-answer-checks/check-dom-31-37.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/check-math-typography.cjs
python scripts/physics-answer-checks/compare-existing-31-37.py
python scripts/physics-answer-checks/check-source-parts-31-37.py
python tools/verify_export.py --refresh
python tools/verify_export.py
```

Tests use actual enrichment, response discovery, checking and delegated UI events: correct/blank/invalid/wrong submissions, wrong signs, zero versus nonzero quantities, accepted rounding/equivalents, every choice distractor, per-part controls and saved-note migration. Non-target records must remain unchanged. Linkedom is development-only. Choice order varies deterministically; numeric tolerances remain below nonzero answers and explicitly accept conventional two/three-significant-figure results.

Final verification: 828 exercises and 2,132 response fields (1,380 numeric and 752 choice). All86 conceptual questions independently cross-reviewed against source diagrams; final per-question comparisons are saved. Source-subpart scan candidates were checked: remaining letters identify diagram panels, mathematical arguments or neighboring OCR, not omitted requested answers. The legacy-key comparison uses pre-change Git HEAD and normalized SI units, including electron-volts and microscopic time/length units.

Corrections before publication include switched LC topology and phasor resonance (31); square-plate symmetry and magnetic-gradient arrow directions (32); radiation-pressure interpretation, cone geometry and refraction dispersion (33); shared-table signs, two-interface refraction and virtual-object optics (34); nested optical paths, numbered interference-curve points and fringe-boundary ambiguity (35); phase wrapping, full Airy diameter, missing/grazing orders and grating comparisons (36); signed intervals, rest-energy balance, source wording and physical speed bounds (37). Printed-key/source conflicts are visibly explained where present. The root spot-check report independently derives selected optical, diffraction and relativistic cases.

Fields marked `noRounding` retain necessary precision; the builder does not add conventional rounded alternatives to those fields. Actual runtime tests reject speed parameters of +1 or -1 for sub-light-speed answers, and browser checks confirm rejection of beta1 while accepting the precise result. High-precision refractive indices similarly reject n1. Conventional equivalent phase angles and explicitly justified rounded-data alternatives remain accepted.

All actual runtime, delegated DOM-event, fraction-rendering and portable-export integrity checks pass. Browser QA confirms multipart optics grading using the exact fraction10/3 and the expected real/virtual/side/orientation conclusions. Prior chapter answer records remain unchanged.
