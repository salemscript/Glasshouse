# Chapter Understanding checks

Every displayed chapter in the six active subjects has at least ten concept checks.
The original multiple-choice question and the previous seventeen added questions
remain. Nine newly authored two-option misconception checks are added per chapter.
These are original teaching statements, not copied textbook exercises or solutions.
Each has a direct correct/incorrect answer and an explanation of the principle or
correction. They cover independent chapter ideas, not numerical reskins.

## Curriculum mapping

`chapter-reference.json` snapshots existing chapter titles, the introductory
concept check, and chapter relationships from the site's textbook-based curriculum.
The TSV files map original teaching checks directly to those actual chapter numbers.
Calculus uses Stewart's chapters 1–17; Physics uses Halliday/Resnick/Walker 1–44;
General Chemistry uses OpenStax Atoms First 2e 1–21; Organic Chemistry uses
OpenStax/McMurry 1–31; Linear Algebra uses Anton/Kaul 1–9. Differential Equations
shares calculus chapters 9 and 17 and uses the same stable IDs for identical checks.

Supplementary primary-source review for potentially subtle concepts:
- https://openstax.org/books/organic-chemistry/pages/30-9-a-summary-of-rules-for-pericyclic-reactions
  Thermal/photochemical orbital occupancy changes selection rules; permission does
  not guarantee a rapid reaction. Questions avoid asserting one rule for all counts.
- https://openstax.org/books/university-physics-volume-3/pages/11-1-introduction-to-particle-physics
  Quarks participate in strong interactions; electrons and neutrinos are leptons.
- https://openstax.org/books/university-physics-volume-3/pages/11-7-evolution-of-the-early-universe
  The microwave background supports a hot early universe; large-scale expansion
  does not require locally bound atoms to expand.
- https://openstax.org/books/chemistry-atoms-first-2e/pages/13-introduction
  Equilibrium is dynamic and actual reaction Gibbs energy vanishes at equilibrium;
  standard Gibbs energy is a distinct quantity.

## Rebuild and validate

From the repository root:

```
python scripts/understanding/build.py
node scripts/understanding/verify.cjs
python tools/verify_export.py --refresh
python tools/verify_export.py
```

The automated verification checks all 1,257 answer flows through the actual Study
handlers, including wrong-answer noncompletion, correct-answer persistence,
unique storage keys, valid answer indices/options, and chapter-local question
counts. This tests implementation and data integrity; mathematical and scientific
correctness was reviewed while authoring each statement and explanation, not
inferred from passing structural tests.

Existing progress keys are retained. New concepts have stable descriptive IDs;
this prevents different chapter questions from accidentally sharing completion.
The two reused calculus chapters intentionally share only identical new checks
with Differential Equations. No textbook practice questions or answer keys change.
