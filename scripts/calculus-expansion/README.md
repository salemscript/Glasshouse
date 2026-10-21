# Calculus answer-check expansion

This checkpoint covers every source record in **§5.5 (94)** and **§6.5 (33)**,
including all seven §6.5 baseball/movie project questions. It also corrects
§2.3 Exercise 3: the original source approach point is x→3, giving 105.

It adds **54** previously missing worked explanations and replaces/reviews
**74** existing explanations. All 128 records have numeric or multiple-choice
checks, totaling 164 explicit fields. The source exercise artwork, shared
instructions, diagrams, PDFs and IDs remain unchanged.

**The full Chapters 2–6 expansion is unfinished.** `coverage.json` lists every
source ID outside this checkpoint by chapter and set; those entries are not
claims that all legacy solutions/checks are missing. The unpublished Chapter
2–4 draft was removed by workspace maintenance and needs reconstruction.
No recurring task has been enabled.

`author.py` explicitly records each integrand, substitution, antiderivative,
endpoint, parameter assumption, final answer and response contract. Source
pages 418–420 and 463–465 were rendered and visually inspected. Explanations
are original derivations; no solution-manual prose was imported.

Important conditions include real cube roots, original trigonometric domain
exclusions, absolute values in logarithms, signed graph area, the 2/3 ratio for
an average over **radius**, initial amounts for growth models, elapsed times
in minutes versus hours, impulse signs and force on the **bat**, and continuous
versus discrete seat-position optimization. Graph estimates have explicit
absolute tolerances. The convexity exercise distinguishes weak and strict
inequalities. Drawings, written proofs and reports are not automatically graded;
selected conclusions and proof methods are checked and do not earn full
original-task completion credit.

The runtime change in `answer-library.js` retains a new full worked explanation
when outdated guided-hint rules are rejected. Previously the rejection could
clear the newer solution summary as well.

Rebuild/check from the repository root:

```sh
python3 scripts/calculus-expansion/build.py
python3 scripts/calculus-expansion/check-math.py
node scripts/calculus-expansion/check-runtime.cjs
python3 tools/verify_export.py --refresh
python3 tools/verify_export.py
```

The independent mathematics check uses SymPy, NumPy and mpmath (development
checks only). It performs 307 high-precision derivative, quadrature, root,
signed-area, unit, momentum, optimization and geometry checks. Runtime checks
exercise the actual enrichment, response-part and hint modules, every correct
answer and every distractor, blanks and invalid numeric input, all help tiers,
and exact preservation of records outside the authored list. They also check
all 368 Chapter 1 exercises as a regression.

An optional DOM integration check uses linkedom installed **outside the website**:

```sh
npm install --prefix /tmp/glasshouse-ui-checks linkedom --no-save --ignore-scripts
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/calculus-expansion/check-dom.cjs
```

This executes actual delegated button/radio/input events for all 128 added or
updated exercises, 164 inputs and 55 individual part-check buttons, including
incorrect/blank/correct feedback, direct solution access, saved-note migration
and completion restrictions. It is a DOM integration test, not a claim of
browser screenshot, animation or assistive-technology testing. The deployed
bank and changed runtime file are byte-checked against the published artifacts.
