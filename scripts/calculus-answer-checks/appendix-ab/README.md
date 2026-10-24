# Appendices A and B answer checks

132/132 source tasks have explicit answer contracts with 196 labeled fields. Appendix A has 70 tasks/84 fields; B has62 tasks/112 fields. Every source exercise page was visually inspected: source indices1222–1223 (printed A9–A10) and1228–1229 (A15–A16), corresponding to full-PDF physical pages1223–1224 and1229–1230.

Run `section-a.py`, `section-b.py`, then `build.py`; SymPy is a development-only dependency. A's interval solvers are independently tested by direct substitution of a rational grid plus exact boundaries into the original inequalities (11,620 checks including physical/end-point checks). B's lines are checked at their source points; vector dot products, determinants, midpoint identities and distances independently verify its geometry (67 checks). Audit files retain original reasoning and test labels.

Written proofs and graphs have selected-result checks and `complete:false`; choosing a conclusion does not grade a proof or drawing. A42 uses physical t≥0. B62 states hours since2pm, miles and mi/h explicitly. B52 is −x≤y<(x+3)/2, with x>−1 and excluded vertex. A64's response prompt states the referenced positive-multiplier and reciprocal rules because the source exercise only references them by number.

`source-corrections.json` proposes A39's missing right-column continuation and removal of empty continuation crops in A64 and B56. It is for parent integration; no shared source files were modified here.
