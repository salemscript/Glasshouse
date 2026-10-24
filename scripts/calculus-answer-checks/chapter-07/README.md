# Chapter 7 answer-check source audit

All 647 actual source question IDs have explicit answer contracts, including
concept checks, True/False, review, Problems Plus, and discovery-project items.
The patch contains 1,023 labeled numeric or mathematical choice fields. No IDs
are manufactured and no generic answer-key confirmation is used.
151 contracts mark `complete:false`: their objective results do not establish
completion of a requested proof, drawing, CAS comparison, or open-ended argument.
The original source question artwork remains the authority for full instructions.
These are answer checks; they do not claim 647 newly authored worked solutions.

## Sources and review

Primary exercise source: supplied Stewart, Calculus: Early Transcendentals,
8th edition, `site/books/calculus/chapter-07.pdf`, printed pages 471–542.
`source-audit.json` records the source SHA-256 and exact bank/source pages for
all 647 records. The authoring modules transcribe original integrands, bounds,
data tables, graph readings and diagram geometry. Graph readings carry explicit
tolerances instead of presenting raster estimates as exact constants.

The missing reference-table formulas were visually checked on original Stewart
reference pages 5–6, recovered from the PDF embedded at
https://paperzz.com/doc/8408759/u---stewart-calculus . Formula 31 is
u(2u²−a²)√(a²−u²)/8+a⁴asin(u/a)/8; formula 33 is
−√(a²−u²)/u−asin(u/a); formula 53 is
[a+bu−a²/(a+bu)−2a ln|a+bu|]/b³. Formula 62 is the
recurrence explicitly differentiated in `check-numerical.py`. These are original
checks derived from the displayed mathematical identities, not copied manual
explanations. The alternate university table
https://math.colgate.edu/math112/dlantz/supps/e3F10.pdf was useful for locating
formula numbers; the original reference-page images determined the final checks.
No full externally downloaded textbook is committed.

## Independent verification

Run with Python, SymPy and mpmath (development dependencies only):

```sh
python3 scripts/calculus-answer-checks/chapter-07/author.py
python3 scripts/calculus-answer-checks/chapter-07/check-math.py
python3 scripts/calculus-answer-checks/chapter-07/check-legacy.py
python3 scripts/calculus-answer-checks/chapter-07/check-numerical.py
```

- `derivative-audit.json`: 208 authored primitives differentiated by independent
  55-digit central differences at real-domain sample points; all pass.
- `legacy-audit.json`: 164 inherited contracts revisited; 158 independent
  primitive/definite-integral checks pass, with six partial-fraction-form
  questions retained after structural review.
- `numerical-audit.json`: 153 checks pass, using direct integration of each
  interpolating panel polynomial for quadrature, high-precision definite
  integration, and symbolic verification of the table-62 recurrence for four n.

These checks are not exhaustive formal proofs; graph precision, open-ended
arguments and software output remain explicitly scoped limitations. Parameters
in the numerical derivative audit are fixed at 5/2; domain reasoning and branch
conditions are recorded in the authored question explanations. Singularities
must not be crossed by an indefinite primitive's arbitrary constant.

Two inherited source-reading mistakes were corrected together with their native
questions and worked steps: §7.1 #16 has z/10^z, not z·10^z; §7.3 #11 includes an
x factor and its definite value is 1/12, not π/8. Both replacement answers pass
independent calculus checks. The new checks also explicitly handle zero scale
in §7.5 #28 and zero frequency in §7.5 #53.

Only the chapter patch and its exclusive audit directory are edited. The parent
integration owns shared bank generation and actual runtime/DOM validation.
