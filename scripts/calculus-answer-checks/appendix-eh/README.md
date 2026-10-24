# Appendix E and H answer checks

All 100 existing tasks have explicit source-reviewed answer contracts: 50 sigma-notation exercises (58 response fields) and 50 complex-number exercises (137 fields), 195 fields total. Numeric real and imaginary components are separate; polar answers use radians in [0,2π). Every subpart is represented. Proofs and root sketches retain a visible limited-assessment contract.

The original supplied full source was visually read at zero-based PDF indexes 1251–1252 (printed A38–A39) and 1277 (printed A64). Text extraction alone loses conjugation bars, exponent positions, and the numerator 3 of E48. These were explicitly resolved against rendered originals. H5 is conjugate(12+7i); H6 is conjugate(2i(1/2−i)); H44 is e^(−iπ), and H45 is e^(2+iπ).

Authoring and independent calculation checks:

```sh
PYTHONPATH=/tmp/glasshouse-math-checks python scripts/calculus-answer-checks/appendix-eh/e.py
PYTHONPATH=/tmp/glasshouse-math-checks python scripts/calculus-answer-checks/appendix-eh/h.py
python scripts/calculus-answer-checks/appendix-eh/build.py
```

The authoring scripts run 199 independent exact/numerical checks: finite sums by explicit addition, sum limits, polynomial induction identities, complex arithmetic against Python's complex/cmath operations, polar coordinates against atan2 and modulus, polynomial-root substitution, power-root substitution, trigonometric identities and antiderivative differentiation. The corresponding audits list the checks and the original per-question reasoning. These mathematical checks are separate from UI grader tests.

No generic inferred grader or copied solution-manual explanation was used. Choices for sigma notation prescribe one indexing convention and acknowledge equivalent reindexings. Source-only irrelevant continuation strips were reported to the integrating agent; no shared source files are changed here.
