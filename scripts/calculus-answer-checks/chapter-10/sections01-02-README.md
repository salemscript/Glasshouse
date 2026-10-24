# Sections 10.1–10.2 answer-check source audit

All 137 actual source records are covered by bounded patches, including both laboratory projects. Section 10.1 contains 58 records and 190 fields; section 10.2 contains 79 records and 183 fields. There are 123 numeric fields and 250 mathematical-choice fields. The 81 graph, proof, exploratory, or construction tasks retain `complete:false`; their conclusions can be checked, but these controls do not assess the full drawing or proof.

Source: the supplied Stewart *Calculus: Early Transcendentals*, eighth edition, Chapter 10 PDF. Printed pages 645–649 and 655–658 were visually inspected, including figure labels, graph matches, shared instructions and both projects. The JSON audits retain source-bank page references for each question.

Rebuild the two patches with `section01.py` and `section02.py`, then run `verify-sections01-02.py`. The independent audit records 224 passing checks. Verification does not import author scripts: it evaluates original coordinate functions, compares finite-difference derivatives, uses Cartesian slice integrals, independently sums 400,000 polygonal segments for lengths and 400,000 conical frustums for surfaces, evaluates explicit Simpson weights, computes the cow's involute grazing-boundary polygon, and tests the Bézier self-intersection with two distinct interior parameters.

Source-sensitive decisions:

- 10.1 #30 checks all nine cubic-curve intersections with graphical tolerances.
- 10.1 #45 distinguishes geometric path intersections from simultaneous collisions.
- 10.1 rolling-circle project explicitly distinguishes physical inside rolling from the algebraic extension when the fixed radius is smaller than the moving radius.
- 10.2 #10 has two source parameters at the stated point but one common tangent.
- 10.2 #18 has a point with both a horizontal and a vertical tangent, from different parameter values.
- 10.2 #19 has no vertical tangent: simultaneous zero parameter derivatives at the endpoints have finite limiting slope.
- 10.2 #52 is `x=cos²(t)`, not `cos(2t)`; distance counts four traversals of the parabola segment.
- 10.2 #62 is `x=2t²+1/t`; the source image resolves the OCR ambiguity.
- 10.2 #64 uses only the upper cardioid half to avoid counting the same surface twice.
- The Bézier project supplies one explicitly verified loop by replacing P₁ with (80,20), plus valid C and smoothly joined S examples; alternative artistic constructions remain possible.

Chapter-wide merge and publishing are owned by the integrating agent. These files do not change the shared runtime or the question bank.
