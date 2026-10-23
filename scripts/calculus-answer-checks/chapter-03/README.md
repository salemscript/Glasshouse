# Chapter 3 answer checks

This authoring batch supplies **710 exact question-ID contracts with 1,340 labeled fields**: 464 new contracts (1,069 fields), plus 246 independently reviewed legacy contracts (271 fields). The separate parent-owned `review.json` supplies the remaining 134 chapter-review records (220 fields). Together they cover **all 844 actual Chapter 3 source records with 1,560 fields**, including section exercises, concept checks, true/false questions, review exercises, Problems Plus, and all embedded projects.

The textbook is the supplied Stewart *Calculus: Early Transcendentals*, eighth edition, `site/books/calculus/chapter-03.pdf`. Original question artwork, diagrams, page references, shared instructions and IDs remain authoritative. The extracted prompt text is search-only and sometimes omits column continuations or misreads operators. For example, §3.8 Exercise 2 continues with parts (c)–(e), Problems Plus 1 uses `y=1−x²`, Problems Plus 27 uses `e^(2x)`, and Problems Plus 28 uses `≥` rather than `>`.

The patches add objective feedback, not a claim that a radio selection independently assesses a written proof or hand-drawn graph. Those records have `grader.complete=false` and explicit assessment scope. Numeric graph estimates have stated tolerances. Every new contract has original mathematical reasoning and source metadata; no solution-manual explanation was imported.

Two legacy mathematical issues were corrected through the entire native prompt/check/teaching entry: §3.2 Exercise 13 had incorrectly transcribed the source numerator `x²+1` as `x⁴+1`; §3.4 Exercise 43 divided by an inner base unnecessarily, introducing a removable hole that the ordinary chain-rule power form avoids. Source-variable names were restored for §3.1 Exercises 20/46 and §3.5 Exercises 55/56/58. Legacy graph/proof/two-method exercises are explicitly limited to the results their controls actually check.

Special assumptions are visible in the fields and explanations:

- The ANH project distinguishes a batch withdrawal followed by replacement from continuous well-mixed withdrawal/replacement; both give the same optimized RBC loss but different extracted blood volumes. The source does not specify the protocol.
- §3.9 Exercise 46 assumes the Ferris wheel touches the ground, since no clearance is given. Exercise 49 admits both approaching and receding branches.
- §3.10 Exercise 10 includes the infinitely many disconnected accuracy windows away from zero. Exercise 42 names the denominator of the relative-error convention.
- Problems Plus 12 includes the horizontal/vertical orthogonal intersection at the origin and distinguishes “at least one orthogonal intersection” from requiring every intersection to be orthogonal.
- Problems Plus 30 preserves the exterior-point and finite-slope restrictions for real tangent pairs. Problem 34 distinguishes the one-sided water-rise rates before and after full submergence.

Rebuild from the repository root (development dependencies only):

```sh
python3 -m pip install --target /tmp/calculus-ch3-deps -r scripts/calculus-answer-checks/chapter-03/requirements.txt
PYTHONPATH=/tmp/calculus-ch3-deps python3 scripts/calculus-answer-checks/chapter-03/author.py
PYTHONPATH=/tmp/calculus-ch3-deps python3 scripts/calculus-answer-checks/chapter-03/check.py
python3 scripts/calculus-answer-checks/build.py --require-complete
```

The author pins the original legacy bank to commit `ead9ee586a79b0c7d1ac9ab3041c9653e4fa2b74`, so rebuilding after publication does not misclassify this new work as legacy. The source PDF SHA-256 and per-set coverage are recorded in `source-review.json`. `wordninja` performs a deterministic development-only spacing pass over new prose; it is not shipped as a runtime dependency.

Validation includes **6,278 structural and independent mathematical checks** in `check.py`, with exact tangent-point/slope derivations, polynomial constraints, corrected derivatives, motion distances, related rates, accuracy boundaries, inverse identities, contact geometry and the source fingerprint. Independent collaborators additionally provided 1,116 source/derivative/sample checks for all 246 legacy records, and 7,892 tests for Problems Plus 15/16/21/29. Their reports/scripts are under `scripts/calculus-ch1/legacy-chapter3-review.json`, `scripts/calculus-ch1/check-legacy-chapter3.py`, and `scripts/calculus-answer-checks/chapter-02/chapter03-independent-review.json` / `check-chapter03-independent.py`. Parent-owned runtime/DOM tests exercise the actual site controls. These checks substantially strengthen the audit; they are not a formal proof of every transcription or an accessibility certification.
