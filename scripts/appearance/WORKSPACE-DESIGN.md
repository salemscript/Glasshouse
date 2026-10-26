# Glasshouse Studio interface

Design direction approved by the user: Bartosz Ciechanowski's Bicycle article for the relationship between visible models and explanations; Linear for workspace hierarchy and restraint; Stripe for confident typography and visual presentation. Glasshouse keeps its own original layout, copy, coral identity, themes, models, and exercise system. No third-party assets or interface code were copied.

References reviewed:
- https://ciechanow.ski/bicycle/
- https://linear.app/
- https://stripe.com/

## Implemented

- Persistent desktop subject/workspace navigation with current-page semantics, complete subject access, and horizontally scrollable phone navigation.
- New original homepage with an exact, interactive secant/tangent demonstration for f(x)=x², fixed axes, two distinct line styles, and live slopes. Subject counts now refer to the actual textbook inventory instead of the small legacy curated bank.
- Shared surfaces, spacing, cards, reading/practice panels, typography, responsive behavior, and mode-aware colors. User-owned palette and mode preferences remain in place.
- All 268 shared physics apparatus models use the retained-SVG renderer, coalesced slider paints, visibility pause, playback pace, and reduced-motion steps. Model compute functions, equations, target values, and exercise answer data are unchanged.
- Immediately adjacent observations connect each explanation step to its apparatus. Previous/next explanation controls update the same original stage state used by the diagram; they pause playback.
- Expand experiment removes the desktop side column without hiding controls. The standard view keeps controls alongside the scene on desktop and below it on phones.
- Pin readings captures actual model outputs and the model time. The comparison table shows quantities, pinned/current values, units, and signed differences. Reset clears the reference. The UI explicitly notes that advancing time also changes time-dependent readings.
- Existing Physics II response graphs retain their mathematical scales and assumptions. Specialized circuit-builder, calculus series, and other subject labs keep their specialized behavior and receive compatible surrounding surfaces.

## Verification

`NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/appearance/check-workspace.cjs`

Passed 268 actual apparatus mounts and 788 exposed model controls, correct numerical predictions, explanation navigation, pin/clear/reset, expanded view, retained SVG identity, animation progress/cancellation, and reduced-motion behavior. The test uses linkedom with an explicit standards-equivalent select-value setter because linkedom omits that browser setter.

`node scripts/physics-answer-checks/check-book-coverage.cjs`

All 4,695 Physics exercises remain answer-checkable through the real practice pipeline, no issues.

`NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/check-math-typography.cjs`

11,211 choices and 16,703 fractions checked; no unformatted mathematical slashes; 56 prose slash exceptions preserved.

Browser review in Chromium: live derivative control (h=0.05 gives secant slope 2.05), elevator comparison (648 N to 588 N when acceleration is set to zero; gravity remains 588 N), Coulomb interaction (doubling separation changes signed force from −53.925 nN to −13.481 nN and moves the graph marker), story controls, expanded view, phone and tablet layouts, theme/mode, specialized calculus series, and answer checks. Phone frames at 320/390 CSS px contain diagram overflow within the diagram rather than the document. Chromium review is not a claim of exhaustive browser or assistive-technology certification.

## Exploration workbench update

References reviewed: https://ciechanow.ski/bicycle/ and https://phet.colorado.edu/en/about (2026-10-26). Original implementation follows their emphasis on manipulating quantities, immediate visual feedback, and making invisible relationships visible. No copied artwork or explanatory text.

The shared 268-model physics apparatus renderer now offers guided/free exploration, scene-side transport, precise numeric controls, and individual quantity resets. Coulomb separation has a pointer/keyboard handle with fixed geometry mapping. The dedicated electric-flux lab has a draggable true-angle normal; its angle controls the projected surface, cosine graph, and signed flux. Pointer capture, bounded values and keyboard alternatives are implemented. Existing specialized models remain separate; this is not a claim that every model has object dragging or 3D scenes.

Validation: shared mount harness exercises every registered model and control, exact inputs, per-quantity resets, mode switching, scene handle mapping, comparison and playback teardown. Browser checks cover Coulomb's inverse-square response, keyboard handles, and actual pointer dragging of the dedicated flux surface. Neither the reference sites' physics models nor their assets are embedded.
