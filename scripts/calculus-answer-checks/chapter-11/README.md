# Chapter 11 answer checks

Coverage: **751 of 751 actual source tasks; 1,570 objective response fields**. This includes all eleven sections, logistic/elusive-limit/radiation projects, the Newton writing project, all review concept/True–False/exercise items and all 26 Problems Plus items.

Original source: `site/books/calculus/chapter-11.pdf`, printed pages 693–790. Questions and diagrams were reviewed in the original page renders, not inferred from existing answer-key entries. `source-audit.json` records each question's source pages, calculation rationale and limited-scope flag; its missing list is empty. `math-cases.json` preserves explicit formulas used in repeatable checks.

## Honest scope

237 contracts have `complete:false`: proofs, plotted graphs, diagrams, open-ended examples, numerical experiments, and the historical report still require human review. Their numerical, algebraic or conceptual conclusions have explicit answer checks. A correct selected conclusion does not establish a proof or a correct drawing. The remaining 514 contracts check the requested objective results. Formula selection uses explicit mathematical expressions; alternate valid open-ended constructions remain separately reviewed.

The original question display remains authoritative. Error-bound fields name the particular valid bound being checked; they do not claim uniqueness or confuse a guaranteed bound with the actual maximum error. Numerical answers retain unrounded calculated values and source-appropriate tolerances. Power-series endpoints were tested separately from radii, and series/sequence convergence are distinguished.

## Source correction

`source-correction.json` identifies four spurious numbered records extracted from the Newton project's bibliography. Those are **references, not four exercises**. It preserves the complete report and references in one actual unnumbered report record, with limited mathematical checks. The denominator is consequently 754 − 4 + 1 = 751. Shared `build.py` applies this correction idempotently; this directory does not mutate the question bank.

## Rebuild and verify

```sh
PYTHONPATH=/tmp/calculus-ch7-deps python3 scripts/calculus-answer-checks/chapter-11/author.py
PYTHONPATH=/tmp/calculus-ch7-deps python3 scripts/calculus-answer-checks/chapter-11/verify.py
```

Dependencies: Python 3, SymPy and mpmath. `author.py` reads only source records plus the explicit section/review/Problems Plus author files, and regenerates `chapter-11.json` and the two audits. It does not inherit existing graders, allowing a deterministic rebuild after integration.

Independent verification includes source-ID equality; finite numerical answers and unique choices; finite term accumulation; symbolic sequence limits and strict threshold checks; Taylor coefficients computed from derivatives (including removable singularities); sampled next-derivative maxima and true remainder bounds; radii computed independently from source coefficients; integrated series versus high-precision quadrature; bead-volume quadrature; Fibonacci-like recurrence substitution; the midpoint spiral's limiting coordinates; and exact geometric/differential identities. These checks supplement source/endpoint review; sampling alone is not claimed as a proof of a global derivative bound.

## Specific conventions and corrections

- 11.1 #83 checks the actual nth-month Fibonacci recurrence and the requested ratio limit, the golden ratio. There is no invented 12-month requirement.
- 11.1 #85 and Review #10 use the definition's **n > N**, not n ≥ N.
- 11.2 #55/#56 preserve the source's actual repeating decimal blocks.
- 11.2 #72 distinguishes steady-state maintenance from the first interval without a loading dose.
- 11.5 #33 excludes negative integer parameter values that make a denominator zero.
- 11.6 #50 explicitly defines matching *rounded decimal places* for the Ramanujan approximations; this differs from counting matching unrounded initial digits.
- 11.8 #38 handles the exceptional all-zero periodic coefficient sequence.
- Review #30 has π^n in its numerator, giving cos(√π/3), not cos(π/3).
- Review #60 separately names the textbook next-term bound relative to mg and the exact bound relative to the true force.
- Radiation uses the constants printed in the book, and converts wavelength units before evaluating Planck's law.
- Problems Plus #3 excludes nonzero integer multiples of π where a summand is undefined, but handles x = 0 directly.
- Problems Plus #26 identifies the exceptional odd scaled harmonic term as the denominator 2^k. The source hint's phrase “last one” is only literally true if n itself is a power of two.

No solution-manual prose was copied. These are original answer-check contracts and calculation explanations, not a claim of complete worked-solution or interactive-lab coverage.

## Independent peer review

The integration agent separately reviewed 11.11 #34–35 against printed pages 779–782. The third-order optics correction agrees with source equation (4): h²[n₁(1/s₀+1/R)²/(2s₀) + n₂(1/R−1/sᵢ)²/(2sᵢ)]. For waves, v²=(gL/2π)tanh(2πd/L); the first omitted term is 4π²gd³/(3L²), hence under d/L<0.1 its magnitude is less than (4π²/3000)gL ≈ 0.0131595gL < 0.014gL. Both contracts passed this separate source and dimensional review.
