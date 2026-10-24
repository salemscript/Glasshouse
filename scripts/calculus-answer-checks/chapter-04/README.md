# Chapter 4 source-reviewed answer contracts

The nine section scripts cover all 641 section and project records. The separately authored Problems Plus patch covers 26 more. `build.py` merges these 667 records into `../chapter-04.json`; the parent integration separately adds the 118 chapter review records.

The merged patch supplies 2,036 fields: 436 numerical and 1,600 mathematical selections. There are 336 explicitly limited tasks whose drawings, proofs, reports, or open-ended discussion cannot be fully assessed by a selection. They retain `complete:false`; answer-check coverage is not a claim that their entire original tasks are automatically graded.

All exercise and project source pages were visually inspected in the supplied chapter PDF (printed pages 275–364). Source page references are recorded per question in the section audit files. `coverage-audit.json` records the PDF fingerprint, counts, and exact-ID inventory. Numerical graph readings carry explicit tolerances. Source illustrations remain the authoritative question presentation, with stale native prompts cleared.

Run each `section01.py` through `section09.py`, then `problems-plus.py`, then `build.py`. Authoring uses SymPy, NumPy, SciPy, and mpmath as development-only dependencies. The nine section scripts execute 461 exact derivative, condition, limit, and root-residual assertions.

`verify-independent.py` additionally checks 3,624 derivative/curvature signs through independent 40-digit numerical differentiation at six interior points per declared interval. It compares 18 optimization objectives against 1,001 feasible trial points each (18,018 comparisons). Real odd-root branches are explicitly handled in the section contracts rather than evaluated through complex principal powers. These checks supplement, rather than replace, the original source review and algebra.

Notable qualifications and corrections:

- §4.1 secondary rainbow project distinguishes the stated total ray turning angle from the opposite-angle convention used by the requested approximately 129-degree result.
- §4.3 #64 includes the inflection at zero, which a sign-change-only root scan can miss.
- §4.4 #84 has limiting area ratio 1/3.
- §4.6 #18 has four curvature zeros; zero is a cusp minimum, not an additional inflection.
- §4.6 #26 uses the continuous real logarithmic domain where sin(x)>0; its repeating pattern has no limit at positive infinity.
- §4.7 #37–38 distinguish a maximum with a degenerate zero-length wire piece from an unattained supremum if both pieces must be positive.
- §4.7 #82, read literally on the entire line, has infimum zero at infinity and no attained minimum. The commonly intended finite segment interpretation is separately labeled; its global transition is 5√2, distinct from the local curvature transition 5√3.
- §4.9 #38 requires separate constants on the two components t<0 and t>0.

No recurrence, scheduling, shared runtime, or publication settings are changed by these files.
