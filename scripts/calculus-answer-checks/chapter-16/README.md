# Chapter 16 answer checks

All **436 actual source tasks** have explicit answer contracts, with **662 fields** (240 numeric, 422 choices). There are **197 limited-assessment tasks**: selection checks do not grade the complete proof, drawing, computer plot, or historical report.

Coverage includes sections 16.1–16.9, all 16 concept checks, 13 true/false questions, 41 review exercises, six Problems Plus exercises, and the actual writing project.

## Source review

Every exercise page was visually read from the retained original textbook source. During authoring the chapter PDF was found unreadable; the parent restored its exact chapter range from the retained full source. Full-source PDF pages 1099–1184 correspond to the chapter; exercise SVG page numbers are one less than full-source PDF page numbers. The coverage audit hashes the repaired chapter PDF.

Eight numbered bibliography citations under *Three Men and Two Theorems* had been imported as independent exercises. `source-correction.json` replaces those eight records with one historical writing project, retaining the report and bibliography in its original source image. Applying the correction repeatedly is safe.

Source continuity issues were reported for 16.2 exercises 35 and 52, 16.5 exercise 39, and review concept 9(c); the parent corrected their source crops. No OCR formula is accepted when the original typeset statement disagrees.

## Verification

- `verify-independent.py`: **240 independent numeric checks**, covering every numeric answer field, using closed forms, alternate projections, one-dimensional moment integrals, independent quadrature, and source-derived physical formulas.
- `verify-symbolic.py`: **124 checks** of stored potentials, tangent planes, and finite differences of independently transcribed source fields against stored curl/divergence answers.
- `build.py`: exact source-ID coverage, field counts, finite numeric values, distinct choice options, and answer membership.
- Parent peer inspection confirmed the source graph interpretations in 16.3 exercises 25/26, the approximate 22 J work in 16.2 exercise 51, and the two-to-one parametrization in 16.7 exercise 8.

Run from the repository root with SymPy available (the authoring environment uses `PYTHONPATH=/tmp/glasshouse-math-checks`):

```sh
python scripts/calculus-answer-checks/chapter-16/build.py
python scripts/calculus-answer-checks/chapter-16/verify-independent.py
python scripts/calculus-answer-checks/chapter-16/verify-symbolic.py
```

The `section01.py` through `section09.py`, `review.py`, and `plus.py` files reproduce the bounded authoring patches. Regenerate those before `build.py` only when changing an authoring script.

## Deliberate mathematical qualifications

- **16.7 #8:** the given parameter disk covers the geometric cone twice. The geometric surface integral is π/√2. The explanation distinguishes it from the double-counted parameter-domain integral √2π.
- **16.9 #15:** the printed `tan z` field is singular at z=π/2 inside and on the stated solid. The checker identifies the failed regularity assumptions and separately labels the finite *formal divergence integral*. It does not misrepresent this as an ordinary flux justified by the Divergence Theorem.
- **Review #24:** the field contains cot z and csc²z at points of the path where z=0. The pulled-back expression has removable singularities, and its extended/improper integral is zero; this convention is stated explicitly.
- **Review #26(d):** the source does not separately name an orientation. The checker explicitly uses `r_u × r_v`; the opposite orientation reverses the answer.
- **16.6 #27/28:** the plotted surfaces are not uniquely specified algebraically. Checks provide reproducible parametrizations and plotting windows resembling the source, with the actual plot still requiring visual review.
- **16.2 #51:** approximately 22 J is a diagram estimate, with a ±3 J graph-reading tolerance.

Final numerical review also checked the source-specific density in 16.2 #37 (ρ=k(1−y)), the pentagon's area 9/2 in 16.4 #21, the midpoint under-estimate in 16.6 #55, and the spherical cap area 4π in 16.6 #61.
