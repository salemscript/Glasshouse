# Chapter 13 answer contracts

286 source records, with explicit labeled numeric or mathematical-choice checks for all sections, chapter review, and Problems Plus. Original source exercise text and diagrams remain authoritative. Parent scripts preserve every ID.

Regenerate each `section01.py`–`section04.py`, `review.py`, and `plus.py`, then run `check_math.py` to merge `../chapter-13.json`. The audit uses independent numerical differentiation, SciPy quadrature, geometric substitutions, initial values, transition endpoint conditions, and projectile energy/ground conditions. The actual browser/checker pipeline is tested separately by the shared scripts.

Important interpretation details:

- Frenet frames and curvature are checked only at regular points; zero velocity and zero curvature exceptions are explicit.
- Normal, osculating, and rectifying plane alternatives are distinct planes, never scalar multiples of the correct plane equation.
- A graphical estimate uses a stated tolerance and does not pretend to be an exact measurement.
- Projectile checks specify gravitational units and ground-height conventions.
- Problems Plus 8 uses the explicitly labeled unrolled-cylinder winding model, giving axial centerline span `Lr/[π(R+r)]`, with thin-cable approximation `Lr/(πR)`. Finite end coverage and exact three-dimensional solid-tube contact are not determined by the source wording. This is not marked fully automatically graded.
- Original proof, graph, and open-ended tasks retain `complete:false`; selecting their conclusions does not certify the whole written argument or drawing.

All explanations and answer contracts are original derivations from the supplied chapter, not copied solution-manual prose.
