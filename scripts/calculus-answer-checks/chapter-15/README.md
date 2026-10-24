# Chapter 15 answer checks

490 of 490 source task IDs are covered, with 847 labeled fields (489 numeric and 358 explicit mathematical choices). This includes sections 15.1–15.9, all three projects, Concept Check, True–False Quiz, Review Exercises and Problems Plus. The source is the local Stewart Calculus: Early Transcendentals, eighth-edition Chapter 15 PDF.

145 tasks explicitly have `complete: false`: their checks assess numerical results, selected formulas or conclusions, not a submitted proof, drawing, graph, or open-ended explanation. These flags must remain visible in coverage reporting. These are answer checks, not full worked-solution certification.

Authoring is split into `section01.py`–`section09.py`, `review.py` and `plus.py`. Run those scripts to regenerate their individual patches; `build.py` merges them, checks exact ID coverage and field contracts, and writes the top-level chapter patch and source audit. Dependencies are SymPy, mpmath and SciPy. In this workspace use `PYTHONPATH=/tmp/glasshouse-math-checks`.

Independent verification:

- `verify.py`: 174 scalar integrals checked with SciPy adaptive quadrature, independently of SymPy's symbolic integration.
- `verify-moments.py`: 145 mass, first-moment and inertia values checked by numerical quadrature, including transformed coordinates and Jacobians.
- `verify-special.py`: 16 additional geometric, probability and change-of-variables checks, including the shifted-cylinder sphere, three-cylinder intersection, perturbed sphere, exposure model, and spherical cap.
- Saved JSON reports contain actual and expected values. Formula derivations and source-specific rationale are in section audit files and authoring scripts.

Source inspection used rendered PDF exercise pages and enlarged diagrams, not OCR alone. The polar/spherical figures, limits, radicals and Jacobians were visually checked. Peer inspection confirmed 15.8#20 is the upper shell with the first-octant wedge removed. Peer inspection also corrected 15.1#7 to contour readings approximately 27, 13, 5 and 17, yielding an integral estimate of 248 and mean 15.5. Diagram-based estimates retain explicit tolerances and limited-scope flags.

The integration owner was notified of source-crop errors in 15.1#7, 15.3#40, 15.8#46, Review Concept Check #5, and Review #60. These source repairs belong to the shared question dataset rather than this exclusive patch directory. The checks include the complete mathematical subparts from the original PDF.
