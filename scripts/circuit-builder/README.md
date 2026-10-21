# Chapter 27 Circuit Studio

Original free-build DC circuit lab for Physics 27.1–27.4. The existing guided experiment remains expandable underneath, including the physical-time RC lab in 27.4. Named textbook examples keep their original specialized models.

## Model and interaction

Place wires between any two grid points; the route goes horizontally first, then vertically. Every intermediate dot and crossing joins electrically. Place components on neighboring dots. Remove a wire before inserting a component on its edge. Edit exact values or sliders, move/rotate/reverse/delete components, and undo/redo up to 50 edits. Layout and probes persist locally after validation.

Supports 1 Ω–1 MΩ resistors, −24…24 V ideal voltage sources and −1…1 A ideal current sources, with at most 80 elements and eight independent sources. Voltage is always a two-point difference. Ground only establishes the reference; floating networks can have measurable internal differences without invented absolute potentials.

`site/circuit-solver.js` contracts ideal wires and solves each network by modified nodal analysis. Rank-revealing elimination retains free-variable coefficients, so redundant voltage sources can have known voltage and unknown individual current. Contradictory sources, shorted nonzero voltage sources, and unreturned current sources produce unknown readings and explanatory messages. No artificial resistance/leakage is added. Numerical residuals are checked.

Conventional current and absorbed power use A→B signs; negative source power means supplied energy. Wire-segment currents are recovered from actual grid-junction current conservation. Arrows show unique currents along wires and branch components; redundant ideal-wire cycles have arbitrary circulating current, so their individual arrows are omitted. A whole wire can cross a junction and carry different currents in its segments. Component markers follow actual solved current sign and magnitude on a fixed speed scale, with a displayed cap. Zero current stops. Colors use a fixed ±24 V reference; glow uses a fixed 10 W reference. Exact numbers are never clipped to those visual scales. This is a steady-state DC builder; capacitors and time dependence remain in the guided RC experiment.

## Independent mathematical checks

Run `node scripts/circuit-builder/check-solver.cjs`.

1267 assertions passed: analytic series/divider/parallel results; independent 2×2 Cramer-rule bridge checks; 80 varied dividers; 30 varied bridges; junction current conservation; signed energy conservation; voltage/current/power scaling; reversed sources/probes; changed ground; floating and disconnected probes; open branches; current sources; conflicting and redundant ideal sources; bounds and invalid placement.

## Browser review

Reviewed in Chromium through the managed preview, October 21, 2026:

- Default 9 V divider reads 6 V. Exact source input 12 V gives 8 V; equal 200 Ω resistors give 6 V at 12 V. Reversed probes read −6 V. Moving ground preserves 30 mA branch current.
- Built the divider from a blank board entirely through placement controls: one voltage source, two resistors and five wires. Read 6 V and 30 mA. Removing a resistor produced zero current; undo restored the reading. Reload preserved the custom circuit.
- Built a current-source loop through controls; 30 mA into a 100 Ω return gave −3 V, resistor −30 mA, and powers −0.09 W/+0.09 W.
- Balanced bridge reads 0 V. Parallel preset gives 90 mA/45 mA and source −135 mA.
- Resistance slider changes the reading immediately, stays focused, and supports keyboard input. Grid Enter moves a probe; Escape cancels pending placement. Blank probes display an em dash rather than fake zero.
- RC experiment remains mounted under 27.4; advancing one time constant gives 5.689 V at 9 V, R=2 kΩ, C=500 μF, matching 9(1−exp(−1)).
- Light and dark board inspected. At a 390 px iframe viewport, document width 375 px (no document overflow); board width 278 px with 760 px scrollable schematic. Numeric editing works with controls stacked below the board.

Follow-up browser review: full node voltage labels are enabled by default, with signed component voltage differences and a voltage/current key above the board. At −9 V the first wire arrow reverses from B2→C2 to C2→B2 and the probe reads −6 V. At 0 V there are zero wire arrows and zero moving markers. The table now displays a signed current for wire routes whose segment current is constant, and “Varies at junctions” for routes crossing a current split. Parallel branches display 135 mA before the split, 90 mA and 45 mA in the returns, and 135 mA after recombination. An additional 296 solver assertions independently check every grid junction in all four presets with both source polarities, plus open branches and ambiguous wire cycles.

No Safari or screen-reader certification is claimed. SVG components and grid nodes expose keyboard buttons and descriptive labels; reduced-motion CSS disables moving markers.

## Reviewed primary source

OpenStax, *University Physics Volume 2*, §10.3, Kirchhoff’s Rules:
https://openstax.org/books/university-physics-volume-2/pages/10-3-kirchhoffs-rules

Teaching takeaway: make every signed branch follow the same endpoint reference. A junction constrains charge flow; a loop constrains potential differences. The UI ties highlighted probe points to V(+)−V(−), resistor current to ΔV/R, and signed power to energy conservation. All explanations, code, diagrams and preset layouts here are original; no solution-manual text is reproduced.

This is a chapter exploration, not a claim of complete exercise-by-exercise simulation or solution coverage.
