# Chapter 12 answer checks

This patch covers all 449 source records: 362 section/project records, 79 chapter review records, and 8 Problems Plus records. The final merged file has 1,088 fields: 515 numeric and 573 mathematical choices. Exact ID coverage has no gaps.

The supplied textbook chapter was reviewed from rendered PDF exercise pages, including geometric diagrams, fractions, signs, shared instructions, and project continuations. The source fingerprint and counts are in `coverage-audit.json`; per-question original mathematical reasoning and global source-page references are in the section, review, and Problems Plus audit files.

There are 196 limited tasks with `complete:false`. Their checks assess explicit conclusions or constructions, not complete freehand drawings, computer plots, arbitrary examples, or written proofs. The original question artwork remains available and authoritative; the patch clears stale native prompts rather than replacing source questions with abbreviated OCR.

Rebuild with the six `section01.py` through `section06.py` scripts, `review.py`, `problems-plus.py`, and `build.py`. The scripts use development-only SymPy, NumPy, SciPy, and mpmath. They execute 124 exact symbolic assertions. `verify-independent.py` passes 1,234 additional checks using scalar coordinate arithmetic, independently solved equilibrium systems, least-squares distance computations, numerical geometric integration, ray/rectangle intersections, and randomized vector identities. This is mathematical validation separate from the shared application's runtime/DOM validation.

Source-sensitive details:

- §12.1 #43 reads the schematic point approximately as (2,1,4), with explicitly labeled graph-estimate tolerances. Its diagram-placement conclusions remain limited assessment.
- §12.2 #34 interprets wind *from* northwest as blowing southeast. #36 cable vectors are forces on the beam and point toward the hook.
- §12.3 #38 has two possible third direction angles, 60° and 120°, because the z-component sign is unspecified.
- §12.5 #66 finds the perpendicular line that actually intersects the source line, rather than any orthogonal direction.
- The §12.5 perspective project computes clipping intervals and perspective endpoints exactly, and solves camera-ray/rectangle intersections for the hidden segment.
- §12.6 #49 uses the numerical semiaxes supplied in the exercise, without representing them as freshly verified geodetic data.
- Problems Plus #3 distinguishes the literal finite-parameter swept surface from its closure: one limiting ruling is omitted, without changing the enclosed volume.
- Problems Plus #7 records that the finite upper holding-force formula requires θ+θs<90°. At or above that threshold there is no finite upper holding-force bound in the ideal Coulomb model.
- Problems Plus #8 distinguishes positive-volume solids from zero-volume boundaries when discussing the minimum-volume question.

No shared question bank, runtime, website assets, deployment settings, or recurring updates are changed by these authoring files.
