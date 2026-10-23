# Chapter 2 answer checks

This patch supplies explicit objective response contracts for all **570 existing Chapter 2 source records**, with **1,269 labeled fields**. Every section, review subsection and Problems Plus entry is covered. Existing textbook statements, diagrams, source crops and question IDs remain unchanged.

`author.py` authors the eight main sections and reads the exclusively authored auxiliary patches `problems-plus.json`, `review-concepts.json`, and `review-exercises.json`. It writes the consolidated `../chapter-02.json`; it does not mutate the website answer library. The parent integration builder installs the patch.

The original user-supplied source is Stewart, *Calculus: Early Transcendentals*, 8th edition, `site/books/calculus/chapter-02.pdf`. Source exercise pages were read with Poppler; graphs and ambiguous notation were rendered and visually inspected. The annotations and objective adaptations are original. No solution-manual explanations were imported. `verification.json` records the source fingerprint and independent check results.

## Assessment scope

- Finite numerical results use numeric inputs. Infinite/nonexistent limits, symbolic formulas, domains, graph properties and proof conclusions use explicit mathematical choices.
- Multipart exercises expose separate labeled checks. Table-derived derivatives state a centered or one-sided secant convention; they are estimates, not exact derivatives inferred from sparse data.
- A request for **some** epsilon–delta radius can have infinitely many valid answers. Numerical adaptations explicitly ask for the **largest symmetric radius**; symbolic choices ask for a sufficient radius valid for every positive epsilon.
- A correct recognition choice does not automatically grade an independently written proof, freehand sketch, historical report or open-ended explanation. These entries have `grader.complete=false` and a visible assessment-scope statement.
- Section 2.8 Exercise 56 contains a coarse position sketch. It does not uniquely determine accurate numerical second/third derivatives at 10 seconds. Its check therefore tests consistent velocity/acceleration behavior and jerk units/sign interpretation; it does not invent precise numerical acceleration or jerk. The original drawing/estimation work still requires review.
- Section 2.7's writing project was exported as **four records sharing the same task**, distinguished by suggested bibliography. All four retain their source IDs and check the common tangent slope 5 and line `y=5x−2`; the historical comparison/report remains ungraded.

## Scientific and editorial details

The patch retains the correct finite limit **−4** in §2.3 Exercise 43, positive **1/4** in Exercise 16, limiting point **(4,0)** in Exercise 66, and Exercise 3's approach point `x→3`, giving **105**. Source graph holes and isolated values are distinguished from limits. Negative velocity is distinguished from positive speed; signed `dV/dt` is distinguished from outflow magnitude. The oxygen-solubility graph in §2.7 Exercise 57 explicitly labels its horizontal axis **°F**; the controls preserve that printed unit rather than silently relabeling it. Ordinary two-sided derivative domains exclude endpoints; an existing right derivative at an endpoint is identified separately where relevant.

## Verification

```sh
python3 scripts/calculus-answer-checks/chapter-02/author.py
PYTHONPATH=/tmp/calculus-check-deps python3 scripts/calculus-answer-checks/chapter-02/check.py
python3 scripts/calculus-answer-checks/chapter-02/graph-audit.py
node scripts/calculus-answer-checks/chapter-02/check-runtime.cjs
```

The development checks use SymPy (`check.py`) and PyMuPDF (`graph-audit.py`), neither of which is a browser dependency. Install them in a temporary development environment if absent.

- **8,786 independent assertions**: exact ID/field contracts, source-encoded symbolic limits, signed velocities, derivatives and tangent data, graph model conditions, separate root solving, and sampled epsilon–delta inequalities.
- Actual website `AnswerChecker`: **1,269 correct results**, **1,992 incorrect-result cases**, **2,538 blank/invalid cases**.
- `graph-audit.py` differentiates the original PDF illustration's cubic Bezier segments for §2.8 Exercises 1–2 to cross-check graph estimates and tolerances. This validates a reading of the artwork, not an exact analytic function behind a sketch.
- The independently authored Problems Plus, concept/true-false and regular review subsets have their own authoring and verification evidence.

These checks independently cover selected authored expressions and exercise every objective contract. They do not claim an independent mathematical proof of every transcription, distractor, artwork reading or prose statement, nor browser/assistive-technology certification. Parent integration performs the actual UI and cross-chapter regression checks.
