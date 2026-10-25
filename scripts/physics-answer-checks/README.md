# Physics chapters 11–13 answer checks

The six bounded source-review batches cover all 311 listed tasks: problems and conceptual questions. Each record includes every requested numeric result or explicit conclusion, its units, original reasoning, source PDF page references, and assumptions. The original textbook statements and diagrams remain the source of truth.

These are answer-check additions, not a claim that all exercises have complete interactive worked solutions or simulations. Estimation or drawing/proof questions use an explicitly scoped result/conclusion check; a choice does not assess an entire freehand diagram or written proof.

## Build and verify

- `python scripts/physics-answer-checks/build.py`
- `node scripts/physics-answer-checks/check-runtime.cjs`
- `NODE_PATH=/path/to/linkedom/node_modules node scripts/physics-answer-checks/check-dom.cjs`
- `NODE_PATH=/path/to/linkedom/node_modules node scripts/check-math-typography.cjs`
- `python tools/verify_export.py --refresh` followed by `python tools/verify_export.py`

The build rejects missing or duplicate tasks and malformed grader records. Runtime tests load the real enrichment, response-part, adaptation and checking code, testing correct, blank, invalid and incorrect answers. DOM tests exercise actual radio/input events and per-part controls for every chapter 11–13 task. Records outside these chapters must remain unchanged.

The source-review batches are the editable inputs. `coverage.json`, `runtime-audit.json` and `dom-audit.json` are generated validation results. No checker is generated from a generic hint or an unreviewed answer-key string.

Final validation: 311 exercises / 722 response fields. The actual runtime and delegated DOM event suites pass correct, blank, incorrect and sign tests; all choice distractors are rejected. Two- and three-significant-figure numeric values are accepted explicitly in addition to each source-specific tolerance. All calculus/physics choice fractions pass the typography regression suite. Non-target answer records remain byte-equivalent after JSON decoding.

Review resolutions: the raw-source missing-letter candidates are diagram labels, axis units/function arguments, or neighboring-column OCR contamination (not omitted exercise parts). P12.57 contains neighboring P63 text in its OCR, while the original source artwork remains authoritative. P12.79 has explicit checks for all six requested distances. Existing-key comparison differences are unit conversions, explicit units added to zero/count/dimensionless values, or printed rounding; P13.9 corrects an old squared-distance unit. Chapter11 P9 was corrected to4.780914m during independent comparison. P11.75(c) uses the exact stated givens. Rounded source constants and estimation/graph assumptions are recorded per exercise. Freehand diagrams and full written derivations remain outside automatic grading.
