# Linear algebra answer checks and worked solutions

The source inventory contains 755 question records across all nine chapters of
the supplied Anton–Kaul *Elementary Linear Algebra*, 12th edition. The inventory
combines selected section exercises, chapter reviews, and the five existing
Section 1.1 records. All 755 have original worked explanations and a total of
1,485 numeric or multiple-choice answer fields.

Each chapter JSON records the source-image review, requested outcomes, answer
fields, original reasoning, and any source defect. Proofs, constructions, and
drawing tasks use concrete mathematical recognition choices; the site does not
claim to grade arbitrary freehand proofs or drawings. Nonunique results are
checked using valid representative constructions, with invalid distractors
verified by residual, orthogonality, rank, or span tests where applicable.

The Python generators reproduce the answers and run exact SymPy checks. They
verify identities such as inverse products, system residuals, eigenvector
equations, matrix reconstructions, orthogonality, and equivalent spans. Numerical
iterations also use NumPy. Source cropping was separately reviewed against the
full chapter PDFs; canonical replacements keep matrix rows together and include
referenced matrices. Corrections to inconsistent printed questions are visible
in the individual exercise notices.

Run from the repository root with Node and Python (SymPy and NumPy installed):

```sh
node scripts/linear-answer-checks/prepare-inputs.cjs
for chapter in 01 02 03 04 05 06 07 08 09; do
  python scripts/linear-answer-checks/ch${chapter}-verify.py
done
python scripts/linear-answer-checks/integrate.py
node scripts/linear-answer-checks/verify-typesetting.cjs
node scripts/linear-answer-checks/verify-runtime.cjs
```

The integration step refuses missing or unexpected IDs. The runtime test loads
the actual application scripts, checks all correct answers, rejects blanks and
every incorrect choice, checks numerical rejection, and renders every worked
answer and solution view. `coverage.json` and `runtime-audit.json` record results.

Math uses explicit TeX delimiters and vendored KaTeX, including accessible MathML.
Fractions are stacked; tall matrix entries have explicit row spacing. Existing
legacy math and chemical text retain their previous rendering paths.
