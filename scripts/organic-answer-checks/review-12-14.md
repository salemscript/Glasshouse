# Organic Chemistry Chapters 12–14 answer-check review

Reviewed 2026-10-26. All 186 textbook questions now have checkable fields: 50 in Chapter 12, 71 in Chapter 13, and 65 in Chapter 14. Added checks to 118 previously unavailable questions and reviewed the remaining 68. There are 463 verified answer fields. Earlier Chapters 1–11 retain their 683 checkable questions.

Drawing, spectrum-sketch, structure, and mechanism tasks are adapted to multiple-choice recognition of the requested outcomes. These choices do not automatically grade a learner-produced drawing. Original textbook statements are preserved. Scope notes distinguish adapted coverage and ambiguous source data.

## Review

Each chapter reviewer inspected the original PDF figures and spectra, then authored options and explanations. Root independently recalculated radiation energies, NMR frequency/ppm conversions, and Beer–Lambert concentrations. Root also checked selected mass-spectrum fragments, isotope patterns, NMR equivalence, structure deductions, and complex Diels–Alder bond maps and stereochemistry.

- Chapter 12: use actual structures rather than misleading image descriptions; correct 12-44 fragment formula to C₆H₁₁O⁺ at m/z 99. Interpret 12-42 using its nonlinear wavenumber axis. A reference spectrum is needed to distinguish E/Z trisubstituted alkenes in 12-37. Sparse spectra support proposed structures without proving uniqueness.
- Chapter 13: add the missing Figure 13.21 used by 13-20. Correct the conditional reading of 13-44(b), whose vinyl integrations total too many H. In 13-55(c), explicitly identify the conflict between the one-oxygen formula and the two-oxygen ester suggested by the shifts. Do not silently claim a structure fits inconsistent data. Recognize diastereotopic proton pairs and avoid overly precise grading of estimated shifts.
- Chapter 14: correct the 14-8(b) ketone description, the 14-7 product name, and 14-17 relative stereochemistry (the shared edges contain sp² carbons, so “cis ring fusions” was inappropriate). Treat 14-19 as one valid precursor rather than a unique reverse assignment. State the chapter-model assumptions in 14-20. Complex cycloadditions use explicit atom/bond maps.

## Validation

`python scripts/organic-answer-checks/integrate-12-14.py`

`node scripts/organic-answer-checks/verify-runtime-12-14.cjs`

Runtime tests load the actual enrichment and answer-check pipeline. They verify every correct answer, every incorrect choice, wrong numerical answers, blanks, independently recomputed numerical values, zero rejection for nonzero energies, chemical notation, and unchanged fraction rendering. Original source statements and unrelated chapters are checked against the preceding commit. Source-figure paths are verified. Earlier Chapters 1–5 and 6–11 regression suites pass.

Browser QA checks mechanism options, correct and incorrect feedback, notation and layout, the added NMR figure, and visible source-error notices. Export manifest hashes, compressed JSON, and local references are validated before publication.
