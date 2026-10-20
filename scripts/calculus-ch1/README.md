# Calculus Chapter 1 worked solutions

This one-time update supplies original worked explanations and final answers for
all 368 source exercise records in the seven Chapter 1 sets, including all
13 concept checks, 14 true/false questions and 28 regular review exercises.
The existing source question artwork, PDFs and IDs remain unchanged.

The tab-separated files contain exercise number, final answer, working and
reasoning/conditions. In the review file, C/T/E distinguish the three separately
numbered subsections. `build.py` maps these records to the exact question IDs in
the exported book and updates only their answer-library entries. It also adds
26 binary checks for the true/false and one-to-one classifications. Existing
numeric graders remain intact; a worked solution does not imply that every
drawing, proof or written explanation has an automatic grader.

Source exercise pages were visually inspected in the existing user-supplied
Stewart 8th edition Chapter 1 PDF. Approximate graph readings are labeled as
such. Printed odd-question final values were used to cross-check readings and
results; the teaching explanations were derived independently. No solution
manual explanations were imported. Important domain details include inherited
holes in Problem-solving Exercise 20, real inverse branches in §1.5 Exercises
59–60, all conditions on nested roots/logarithms, and the distinction between
terminal-departure time and the one-hour flight in §1.1 Exercise 22.

Rebuild and check from the repository root:

```sh
python3 scripts/calculus-ch1/build.py
python3 scripts/calculus-ch1/check-math.py
node scripts/calculus-ch1/check-runtime.cjs
python3 tools/verify_export.py --refresh
python3 tools/verify_export.py
```

The optional independent mathematical check requires NumPy, SymPy and mpmath;
the website itself requires no new dependencies. It checks symbolic identities,
raw-table regressions, unit conversions, real inverse branches, interval cases,
and recursive compositions. Runtime checks execute the real help, answer and
part-selection modules for every exact Chapter 1 ID, including all three help
tiers and answer checking. They are DOM-independent checks, not a claim of
browser screenshot or assistive-technology testing.

The new **View worked solution** button enters the existing solution view and
marks the attempt assisted. It does not mark an exercise correct or complete.
The original three-tier hint control continues to work. Coverage is recorded
in `coverage.json`. No recurring automation is enabled.
