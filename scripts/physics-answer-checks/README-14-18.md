# Physics chapters 14–18 answer checks

Scope: all 576 listed exercises, including every numerical problem and conceptual question: chapter14 100, chapter15 128, chapter16 107, chapter17 122, chapter18 119. This batch adds answer checks, not a claim of complete worked solutions or lab coverage. Freehand plots and written proofs are assessed through their requested quantities and conclusions; the checker does not evaluate a student's drawing or prose.

`ch14.json` through `ch18.json` contain original source-reviewed answer contracts; the corresponding author scripts reproduce derivations. Each record identifies source PDF pages, requested fields, units and signs, assumptions, and verification reasoning. An independent review covers the conceptual questions. The chapter PDFs and original exercise artwork remain the source of the complete questions and diagrams.

Numeric checking preserves each reviewed tolerance and explicitly accepts conventional two- and three-significant-figure results. Estimation and ambiguous-convention problems state the conditions under which their checks apply. Choices are ordered by a stable per-exercise hash so the first choice does not systematically reveal the answer.

Reproduce this batch from the repository root:

```sh
python scripts/physics-answer-checks/build-14-18.py
node scripts/physics-answer-checks/check-runtime-14-18.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/physics-answer-checks/check-dom-14-18.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/check-math-typography.cjs
python scripts/physics-answer-checks/compare-existing-14-18.py
python scripts/physics-answer-checks/check-source-parts-14-18.py
python tools/verify_export.py --refresh
python tools/verify_export.py
```

The DOM test needs the development-only Linkedom package; the published site has no added dependency. Runtime checks use the actual enrichment, response-part discovery, choice adapter and answer checker. They check correct, blank, invalid, wrong-sign, rounded/alternate responses and every choice distractor. DOM checks exercise the actual delegated input/radio and check-button events, per-part controls, and saved-note migration. The runtime suite also asserts that answer records outside this batch have not changed.

Final review: 576 exercises and 1,257 answer fields (1,016 numeric, 241 choice). All55 conceptual questions independently cross-reviewed. Numeric regression checks also reject zero for nonzero answers, except explicitly valid phase equivalents. The existing-key comparison reports unit notations/conversions, printed rounding, explicitly labeled estimation assumptions, and these reviewed substantive differences: Chapter17 P97's out-of-phase statement conflicts with its printed in-phase key; Chapter18 P49 checks signed work done ON the gas, not an unsigned magnitude; Chapter18 P87 uses an explicit2.0m² area estimate and includes the general relation. Source subpart candidates were reviewed: remaining letters are diagram names, axis/function labels, or neighboring OCR; no requested part is omitted.

Corrections before publication include Chapter14 P49's fixed-barge flow area, Chapter15 P7's micrometre unit, Chapter16 P11's graph period and P59's node count, Chapter17 P3's individual reflection count, P25's microwatt unit and P109's reflected-path geometry, and Chapter18 Q4/Q9 phase-change interpretations. Tiny-value tolerances remain smaller than their nonzero answers. Prior chapter records are unchanged.
