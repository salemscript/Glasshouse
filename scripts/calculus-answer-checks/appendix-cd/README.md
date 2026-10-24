# Appendix C and D answer checks

All 129 source tasks are covered: 40 conic/region tasks in C and 89 trigonometry tasks in D. The 349 fields comprise 155 numeric entries and 194 mathematical selections. Seventy tasks explicitly limit grading to results or reasoning steps because their original instruction includes a drawing or proof.

Source review used the supplied full Stewart 8e PDF: physical page 1237 (A23), pages 1246–1247 (A32–A33), and referenced identities on pages 1242–1244 (A28–A30). Source question `part.page` values are zero-based. Every equation and figure was visually inspected; the search-only OCR was not treated as mathematical ground truth.

Original answer contracts and reasoning are reproducible with:

```sh
PYTHONPATH=/tmp/glasshouse-math-checks python scripts/calculus-answer-checks/appendix-cd/author.py
PYTHONPATH=/tmp/glasshouse-math-checks python scripts/calculus-answer-checks/appendix-cd/verify.py
```

Verification separately derives all 155 numeric fields from source coefficients, geometric constructions, unit-circle cases and transformations. It also verifies 66 exact trigonometric ratios (including undefined ratios), six shared-given trig combinations, 53 symbolic identity/root/incidence checks, and 4,000 interior inequality samples. Endpoint inclusion is reviewed directly against the source inequalities. A numerical substitution is not presented as a proof of an identity or completeness of a root set; those rely on the stated algebraic derivations.

Subtleties retained:

- C36 uses the axis-aligned ellipse standard form taught in this appendix; a general rotated ellipse would not be determined by the stated points alone.
- D26 and D25 retain undefined reciprocal/quotient trigonometric ratios.
- D55 equality is asserted on the common domain: at odd multiples of π the left expression is zero but the right expression is undefined.
- D69–72 retain zero-factor cases, repeated-root deduplication and closed-interval endpoints.
- D39–41 include readable restatements of the referenced identities in their response instructions.
- All graph/proof contracts state their scope and do not award full original-task completion.

`source-crop-recommendations.json` contains two source-display repairs for parent integration: remove an extraneous continuation on D56 and use the top-right continuation for D83. No shared source files were edited by this batch.
