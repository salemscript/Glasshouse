# Physics problem animation coverage

The full batch contains **2,117 illustrations across 4,170 Problems in 44 chapters**. Every chapter has floor(problem count / 2) + 1 illustrated problems. Conceptual Questions are not part of this Problems denominator.

## Scope and review

28 individually authored scenes are retained. The remaining mappings select a named object or process from the actual question text, using bounded chapter scopes only to disambiguate meanings. There is no chapter-only fallback. Shared renderers are deliberately simple visual companions, not solutions, replicas of missing figures, or numerically exact simulations. Complex arrangements may show one component, without fabricating the entire apparatus. Object-based records have not each received an independent manual physics simulation audit; the per-question audit records this distinction honestly.

Prompt extraction removes module headings, examines the setup before the first question mark, and limits the matching window to avoid neighboring-question OCR contamination. Explicit static constraints suppress mechanical motion. Stationary apparatus uses an animated outline or highlight. Quantum illustrations use probability density, energy bands, or nuclei rather than classical electron orbits.

## Experience

Silent looping SVG illustrations appear to the right of each selected problem, below it on narrower screens, with no labels or playback controls. They inherit theme colors. Animation pauses offscreen and in hidden tabs, respects reduced motion, and renders at approximately 30 frames per second. They do not alter answer checking, assistance, or progress.

## Verification

`python scripts/build-physics-illustrations.py` rebuilds the manifest, per-question audit, and chapter coverage. `node scripts/check-physics-loops.cjs` verifies strict majority for all 44 chapters, renderer availability, animation frame changes, valid numeric output, no labels or controls, and source question hashes. Visual review covers representative renderers, different phases, theme color changes, and actual problem layouts. It is representative UI review, not a claim of manually watching every question.

See `scripts/answer-data/physics-loop-coverage.json` for exact chapter totals and `scripts/answer-data/physics-illustration-audit.json` for source hashes and matching evidence. Future changes to source questions should rebuild and re-review their mappings.
