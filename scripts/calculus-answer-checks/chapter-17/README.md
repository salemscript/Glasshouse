# Chapter 17 answer checks

All 123 original tasks have explicit answer contracts, including all exercises, Concept Check, True-False Quiz and review. Proofs and plots check their stated mathematical conclusions, not the full written/graphical submission.

The original chapter PDF pages 1160, 1167–1168, 1175–1176 and 1180–1182 were inspected visually, including right-column continuations. The shared source-crop correction restores the pendulum subparts and Earth's-interior application. In the latter, the harmonic coordinate is signed; physical distance is its absolute value.

`section01.py` through `section04.py` and `review.py` generate the authored records. `verify.py` merges them and independently integrates the source differential equations numerically. Every analytic ODE solution is also substituted into the differential equation and any initial/boundary conditions during authoring. Power-series coefficient recurrences are checked through at least degree 23. Variable parameters and arbitrary constants are distinguished in the answer labels.

Reproduce with `PYTHONPATH=/tmp/glasshouse-math-checks python <script>` when using the development-only SymPy installation. SciPy is required for `verify.py`. No development dependencies are shipped to the website.
