# Calculus Chapters 1–3 answer checks

This source update targets every existing textbook exercise ID in Chapters1–3:
368 in Chapter1,570 in Chapter2, and844 in Chapter3 (1,782total). The source
question bank, source PDFs, artwork, shared instructions, and IDs are preserved.

Each chapter patch supplies explicit numeric or mathematical multiple-choice
response contracts. Multipart questions have labeled fields. Source-sensitive
proofs, freehand drawings, and open-ended examples have selected-result checks;
these do not automatically establish completion of the original task.
The on-screen scope states that limitation, and the grader's `complete:false`
prevents those recognition checks from awarding full task completion.
Graph estimates have explicit tolerances. Numeric entry accepts fractions and
arithmetic expressions in the unit displayed beside the input.

`build.py` validates and merges the three top-level chapter patches and the
bounded review/ProblemsPlus patches. It never guesses an answer or derives
one from answer-key prose. `coverage.json` inventories exact IDs and sets.
`check-runtime.cjs` executes the real practice enrichment pipeline, response
part extraction, and checker, rather than just inspecting stored grader flags.
It requires every one of the1,782questions to have supported fields, explicit
review metadata, correct/blank/wrong feedback, and no changes to other chapters.
`check-dom.cjs` additionally executes the actual delegated button, radio, and
input events, including individual part buttons and saved-note migration.

The Chapter1 baseline already had full coverage. Its audit corrected §1.2#8:
the common point for `1+m(x+3)` is `(−3,1)`. All Chapter1 check fields remain
covered. Chapter2/3 scripts contain original calculations and adaptations from
the supplied Stewart8th-edition exercises. New answer checks do not imply a
new fully worked solution where one is not explicitly supplied.

Development dependencies are outside the website: SymPy, NumPy, and mpmath for
mathematical derivation/checking; linkedom for the optional DOM event test.
The runtime website needs no new dependency.

Rebuild the bounded source patches first, then integrate:

```sh
python3 scripts/calculus-ch1/build.py
python3 scripts/calculus-answer-checks/chapter-02/author-problems-plus.py
python3 scripts/calculus-answer-checks/chapter-02/author-review-concepts.py
python3 scripts/calculus-answer-checks/chapter-02/review-exercises.py
python3 scripts/calculus-answer-checks/chapter-02/author.py
python3 scripts/calculus-answer-checks/chapter-03/review.py
python3 scripts/calculus-answer-checks/chapter-03/author.py
python3 scripts/calculus-answer-checks/build.py --require-complete
node scripts/calculus-answer-checks/check-runtime.cjs
NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/calculus-answer-checks/check-dom.cjs
python3 tools/verify_export.py --refresh
python3 tools/verify_export.py
```

Chapter-specific mathematical/source audits document the independent checks,
reviewed PDF pages, source fingerprints, conventions, and remaining assessment
limits. Mathematical spot checks and visual/source review are separate from
runtime correctness; executing the expected answer through a checker does not
independently establish that the expected answer is mathematically correct.

No recurring task or scheduled update is enabled by this change.

## Integrated verification

All1,782question records pass the actual practice pipeline with3,507supported
response fields (1,230numeric and2,277choice). The runtime checks reject6,066
wrong-answer cases as well as blank and invalid numeric entries. DOM event
tests pass all1,782questions,3,507inputs, and2,458individual part buttons.
Other calculus chapters' answer entries remain byte-for-byte equivalent after
JSON parsing. Saved notes survive the response-contract version migration;
old completion results are cleared when the revised contract first loads.

The corrected246legacy Chapter3 contracts all pass the strict independent
source comparison. The recorded mathematical checks include Chapter1's3,359
checks, Chapter2's8,786checks, Chapter3's6,278checks, and the separate bounded
review/ProblemsPlus/related-rate checks documented in their audit files.

Browser QA covered fraction input, an exact pi/square-root expression,
multipart choices, the corrected §3.2#13 worked solution, and long derivative
choices at a390px iframe viewport. The phone document stays within its375px
content width; long choices wrap without page overflow. This is Chromium QA,
not screen-reader or cross-browser certification.

§2.8#56 is an explicit assessment limit: the coarse position sketch supports
qualitative velocity/acceleration and jerk-unit checks, but does not determine
a unique accurate numerical acceleration or jerk. The interface states this
and does not award completion of the original drawing/numerical-estimation task.
