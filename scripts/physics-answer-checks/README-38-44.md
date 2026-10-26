# Physics chapters 38–44 answer checks

Scope: all 598 listed exercises in chapters38–44. Per-question contracts record every requested numerical result or conclusion, original reasoning, units, signs, assumptions, source PDF pages and verification. Author scripts reproduce calculations. Independent cross-reviews cover all94 conceptual questions.

This adds answer checks, not a claim of complete worked solutions or lab coverage. Drawings and proofs are checked through requested quantities and conclusions, not automatic evaluation of freehand work or prose. Estimation examples state assumptions and general relationships; source/key conflicts are explained where applicable.

Reproduce from the repository root:

```sh
python scripts/physics-answer-checks/build-38-44.py
node scripts/physics-answer-checks/check-runtime-38-44.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/physics-answer-checks/check-dom-38-44.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/check-math-typography.cjs
python scripts/physics-answer-checks/compare-existing-38-44.py
python scripts/physics-answer-checks/check-source-parts-38-44.py
python tools/verify_export.py --refresh
python tools/verify_export.py
```

The tests exercise actual enrichment, response discovery, checking and delegated UI events: correct/blank/invalid/wrong submissions, wrong signs, zero versus nonzero quantities, accepted rounding/equivalents, every choice distractor, per-part controls and saved-note migration. Non-target answer records remain unchanged. Linkedom is development-only. Choice order varies deterministically. Numeric tolerances remain smaller than nonzero answers, with explicit conventional rounded results unless noRounding is required for precision or physical bounds.

Final verification: 598 exercises and 1,341 response fields (921 numeric,420 choice); all94 conceptual questions independently source-reviewed and cross-compared. All requested parts are covered, including the additional four-part conservation question in44.6 and the recovered subparts in42.47/69/97. Remaining source-part scan letters denote figure panels, mathematical arguments or neighboring OCR. Source-key comparisons use pre-change Git HEAD and normalized units.

Notable resolutions: microscopic units and uncertainty conventions (38), anisotropic density and source energy levels (39), underconstrained quantum numbers and the inconsistent logical-shell claim (40), error denominators and finite-window Fermi-Dirac integration (41), mass versus atom abundance, coherent decay data and complete primary-chart isotope sets (42), molar-mass units and per-particle versus combined collision energy (43), conservation subparts, particle spin constraints and cosmological wavelength units (44). Estimation and source/key inconsistencies have explicit scopes and notes. The chapter42 audit preserves queried NNDC NuDat records, inclusion/exclusion evidence, retrieval details, hash and discovery-paper support.

The whole-book audit uses the actual practice enrichment, response adapter and answer checker. All44chapters,4,695exercises and11,224responsefields are available, with no unresolved graders or reference responses. Every field is numeric or multiple-choice. Earlierchapter answer records remain unchanged. This is complete answer-check coverage, not a claim that freehand drawings, full written proofs, worked solutions or labs have all been completed.

Final runtime, delegated DOM-event, fraction-rendering, full-book availability and portable-export integrity checks pass. Browser QA confirms the complete four-part conservation-law question grades correctly. The published data are checked against the tested file hashes after deployment.
