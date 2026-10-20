// Selected exercises transcribed from the user-provided Stewart, Calculus: Early Transcendentals, 8th edition PDF.
// Source prompts were checked against rendered pages. Hints and solutions are independently authored.
// Numerical grading covers these selections only; the full source exercise sets remain in the textbook reader.
window.CALCULUS_BANK = [
  {
    "id": "stewart-1-1-25-f2-only",
    "chapter": "01 · Functions and Models",
    "topic": "Evaluating functions",
    "title": "Evaluate f(2) · selected portion",
    "prompt": "If f(x) = 3x² − x + 2, find f(2).",
    "answer": 12.0,
    "unit": "",
    "tolerance": 0.001,
    "hint": "Replace every x in the function with 2.",
    "solution": "f(2) = 3(2²) − 2 + 2 = 12 − 2 + 2 = 12. This grades only the f(2) portion of Exercise 25.",
    "level": "Foundation",
    "source": {
      "book": "calculus",
      "chapter": 1,
      "section": "1.1",
      "exercise": "25 (f(2) only)",
      "pdfPage": 53,
      "printedPage": "21"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "Only the f(2) item from the exercise’s list is presented and graded.",
    "hints": [
      "Replace every x in the function with 2.",
      "Write 3(2²) − 2 + 2 before doing any arithmetic.",
      "Square first, then multiply. The final two terms cancel."
    ]
  },
  {
    "id": "stewart-2-3-11",
    "chapter": "02 · Limits and Derivatives",
    "topic": "Limits using factorization",
    "title": "A removable discontinuity",
    "prompt": "Evaluate the limit, if it exists: lim as x → 5 of (x² − 6x + 5)/(x − 5).",
    "answer": 4.0,
    "unit": "",
    "tolerance": 0.001,
    "hint": "Factor the numerator before taking the limit.",
    "solution": "x² − 6x + 5 = (x − 1)(x − 5). For x ≠ 5 the quotient equals x − 1, so the limit is 5 − 1 = 4.",
    "level": "Foundation",
    "source": {
      "book": "calculus",
      "chapter": 2,
      "section": "2.3",
      "exercise": "11",
      "pdfPage": 134,
      "printedPage": "102"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Factor the numerator before taking the limit.",
      "Look for two numbers whose product is 5 and whose sum is −6.",
      "Cancel the common factor only for x ≠ 5, then evaluate the simplified expression at 5."
    ]
  },
  {
    "id": "stewart-2-3-18",
    "chapter": "02 · Limits and Derivatives",
    "topic": "Difference quotient limits",
    "title": "The slope hidden in a limit",
    "prompt": "Evaluate the limit, if it exists: lim as h → 0 of [(2 + h)³ − 8]/h.",
    "answer": 12.0,
    "unit": "",
    "tolerance": 0.001,
    "hint": "Expand (2 + h)³ and cancel h.",
    "solution": "(2 + h)³ − 8 = 12h + 6h² + h³. Dividing by h gives 12 + 6h + h², whose limit as h → 0 is 12.",
    "level": "Foundation",
    "source": {
      "book": "calculus",
      "chapter": 2,
      "section": "2.3",
      "exercise": "18",
      "pdfPage": 134,
      "printedPage": "102"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Expand (2 + h)³ and cancel h.",
      "Use (a + b)³ = a³ + 3a²b + 3ab² + b³.",
      "After subtracting 8, every remaining term contains h. Divide before setting h to zero."
    ]
  },
  {
    "id": "stewart-3-9-33",
    "chapter": "03 · Differentiation Rules",
    "topic": "Related rates",
    "title": "Determine a ladder’s length",
    "prompt": "The top of a ladder slides down a vertical wall at a rate of 0.15 m/s. At the moment when the bottom of the ladder is 3 m from the wall, it slides away from the wall at a rate of 0.2 m/s. How long is the ladder?",
    "answer": 5.0,
    "unit": "m",
    "tolerance": 0.001,
    "hint": "Let x and y be horizontal and vertical distances. Differentiate x² + y² = L².",
    "solution": "The ladder has fixed length L, so x x′ + y y′ = 0. At this instant x = 3, x′ = 0.2, and y′ = −0.15. Thus 3(0.2) − 0.15y = 0, giving y = 4. Finally L = √(3² + 4²) = 5 m.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 3,
      "section": "3.9",
      "exercise": "33",
      "pdfPage": 282,
      "printedPage": "250"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Let x and y be horizontal and vertical distances. Differentiate x² + y² = L².",
      "Differentiate to obtain x(dx/dt) + y(dy/dt) = 0. The downward rate is negative.",
      "Substitute x = 3, dx/dt = 0.2, dy/dt = −0.15 to find y. Then use L = √(x² + y²)."
    ]
  },
  {
    "id": "stewart-3-9-31",
    "chapter": "03 · Differentiation Rules",
    "topic": "Related rates",
    "title": "Expanding equilateral triangle",
    "prompt": "The sides of an equilateral triangle are increasing at a rate of 10 cm/min. At what rate is the area of the triangle increasing when the sides are 30 cm long?",
    "answer": 259.8076211353316,
    "unit": "cm²/min",
    "tolerance": 0.01,
    "hint": "For side length s, the area is A = (√3/4)s².",
    "solution": "Differentiating A = (√3/4)s² with respect to time gives dA/dt = (√3/2)s(ds/dt). At s = 30 and ds/dt = 10, dA/dt = 150√3 ≈ 259.807621 cm²/min.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 3,
      "section": "3.9",
      "exercise": "31",
      "pdfPage": 282,
      "printedPage": "250"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "For side length s, the area is A = (√3/4)s².",
      "Apply the chain rule: dA/dt = (√3/2)s(ds/dt).",
      "Substitute the side length and its rate separately. Area rate has units cm²/min."
    ]
  },
  {
    "id": "stewart-4-7-39",
    "chapter": "04 · Applications of Differentiation",
    "topic": "Optimization",
    "title": "The largest pizza slice",
    "prompt": "If you are offered one slice from a round pizza (in other words, a sector of a circle) and the slice must have a perimeter of 32 inches, what diameter pizza will reward you with the largest slice?",
    "answer": 16.0,
    "unit": "inches",
    "tolerance": 0.001,
    "hint": "Write the perimeter as two radii plus the arc length. Sector area is half the radius times the arc length.",
    "solution": "Let r be the radius and s the arc length. From 2r + s = 32, s = 32 − 2r. The slice area is A = rs/2 = 16r − r². A′ = 16 − 2r vanishes at r = 8, and A″ = −2 < 0, so this is the maximum. The requested diameter is 2r = 16 inches. The corresponding angle is s/r = 2 radians, a valid sector.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 4,
      "section": "4.7",
      "exercise": "39",
      "pdfPage": 370,
      "printedPage": "338"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Write the perimeter as two radii plus the arc length. Sector area is half the radius times the arc length.",
      "Let s be arc length. Substitute s = 32 − 2r into A = rs/2.",
      "Differentiate the area with respect to r and set it to zero. The question asks for diameter, twice the radius."
    ]
  },
  {
    "id": "stewart-5-3-69",
    "chapter": "05 · Integrals",
    "topic": "Fundamental theorem of calculus",
    "title": "Recover a function value",
    "prompt": "If f(1) = 12, f′ is continuous, and ∫ from 1 to 4 of f′(x) dx = 17, what is the value of f(4)?",
    "answer": 29.0,
    "unit": "",
    "tolerance": 0.001,
    "hint": "The integral of f′ is the net change in f.",
    "solution": "By the fundamental theorem of calculus, ∫₁⁴ f′(x) dx = f(4) − f(1) = 17. Therefore f(4) = 12 + 17 = 29.",
    "level": "Foundation",
    "source": {
      "book": "calculus",
      "chapter": 5,
      "section": "5.3",
      "exercise": "69",
      "pdfPage": 433,
      "printedPage": "401"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "The integral of f′ is the net change in f.",
      "Write f(4) − f(1) = 17.",
      "The integral gives a change, not the final value. Add the initial value to that change."
    ]
  },
  {
    "id": "stewart-6-1-13-area-portion",
    "chapter": "06 · Applications of Integration",
    "topic": "Areas between curves",
    "title": "Two parabolas · area portion",
    "prompt": "Sketch the region enclosed by the given curves and find its area: y = 12 − x², y = x² − 6.",
    "answer": 72.0,
    "unit": "square units",
    "tolerance": 0.001,
    "hint": "Find the intersection x-values, then integrate upper minus lower.",
    "solution": "The intersections satisfy 12 − x² = x² − 6, so x = ±3 and y = 3. The enclosed region lies between the downward-opening parabola above and the upward-opening parabola below. Its area is ∫₋₃³ [(12 − x²) − (x² − 6)] dx = [18x − (2/3)x³]₋₃³ = 36 − (−36) = 72 square units.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 6,
      "section": "6.1",
      "exercise": "13 (area portion)",
      "pdfPage": 466,
      "printedPage": "434"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "The numerical area is graded; the sketch instruction is retained from the textbook.",
    "hints": [
      "Find the intersection x-values, then integrate upper minus lower.",
      "Solve 12 − x² = x² − 6 for both intersection points.",
      "Integrate 18 − 2x² between those intersections. Symmetry lets you double the integral over the positive half."
    ]
  },
  {
    "id": "stewart-7-1-71",
    "chapter": "07 · Techniques of Integration",
    "topic": "Integration by parts",
    "title": "Use derivative endpoint data",
    "prompt": "Suppose that f(1) = 2, f(4) = 7, f′(1) = 5, f′(4) = 3, and f″ is continuous. Find the value of ∫ from 1 to 4 of x f″(x) dx.",
    "answer": 2.0,
    "unit": "",
    "tolerance": 0.001,
    "hint": "Use integration by parts with u = x and dv = f″(x) dx.",
    "solution": "Integration by parts gives ∫₁⁴ x f″(x) dx = [x f′(x)]₁⁴ − ∫₁⁴ f′(x) dx. The boundary term is 4(3) − 1(5) = 7. The remaining integral is f(4) − f(1) = 7 − 2 = 5. Hence the answer is 7 − 5 = 2.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 7,
      "section": "7.1",
      "exercise": "71",
      "pdfPage": 509,
      "printedPage": "478"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Use integration by parts with u = x and dv = f″(x) dx.",
      "Integration by parts gives [x f′(x)]₁⁴ − ∫₁⁴ f′(x) dx.",
      "Evaluate the boundary product at both ends; the remaining integral is f(4) − f(1)."
    ]
  },
  {
    "id": "stewart-8-1-14",
    "chapter": "08 · Further Applications of Integration",
    "topic": "Arc length",
    "title": "Length of a logarithmic curve",
    "prompt": "Find the exact length of the curve: y = ln(cos x), 0 ≤ x ≤ π/3.",
    "answer": 1.3169578969248166,
    "unit": "units",
    "tolerance": 0.001,
    "hint": "Use L = ∫ √(1 + (y′)²) dx and 1 + tan²x = sec²x.",
    "solution": "y′ = −tan x. On 0 ≤ x ≤ π/3, cos x is positive, so √(1 + tan²x) = sec x. Thus L = ∫₀^(π/3) sec x dx = [ln|sec x + tan x|]₀^(π/3) = ln(2 + √3) ≈ 1.316958.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 8,
      "section": "8.1",
      "exercise": "14",
      "pdfPage": 580,
      "printedPage": "549"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Use L = ∫ √(1 + (y′)²) dx and 1 + tan²x = sec²x.",
      "Differentiate ln(cos x) to get −tan x. The arc-length integrand simplifies to sec x on this interval.",
      "An antiderivative of sec x is ln|sec x + tan x|. Evaluate both endpoints; enter a decimal."
    ]
  },
  {
    "id": "stewart-9-2-19aiii",
    "chapter": "09 · Differential Equations",
    "topic": "Euler’s method",
    "title": "Four Euler steps · part (a)(iii)",
    "prompt": "Use Euler’s method with each of the following step sizes to estimate the value of y(0.4), where y is the solution of the initial-value problem y′ = y, y(0) = 1. (iii) h = 0.1.",
    "answer": 1.4641,
    "unit": "",
    "tolerance": 0.001,
    "hint": "For this equation, each step is y_next = y + 0.1y.",
    "solution": "With h = 0.1, Euler’s update is yₙ₊₁ = 1.1yₙ. Starting at y₀ = 1, the four steps give y₁ = 1.1, y₂ = 1.21, y₃ = 1.331, and y₄ = 1.4641 at x = 0.4. The requested Euler estimate is 1.4641, rather than the exact e^0.4.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 9,
      "section": "9.2",
      "exercise": "19(a)(iii)",
      "pdfPage": 629,
      "printedPage": "598"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "Only part (a)(iii), step size h = 0.1, is presented and graded.",
    "hints": [
      "For this equation, each step is y_next = y + 0.1y.",
      "Start at y₀ = 1 and multiply by 1.1 after each step of width 0.1.",
      "Reaching x = 0.4 takes four steps. Use Euler’s estimate rather than the exact exponential solution."
    ]
  },
  {
    "id": "stewart-10-4-2",
    "chapter": "10 · Parametric Equations and Polar Coordinates",
    "topic": "Polar area",
    "title": "Area within a polar sector",
    "prompt": "Find the area of the region that is bounded by the given curve and lies in the specified sector: r = cos θ, 0 ≤ θ ≤ π/6.",
    "answer": 0.23915286937262953,
    "unit": "square units",
    "tolerance": 0.001,
    "hint": "Use A = (1/2)∫ r² dθ and the half-angle identity for cos²θ.",
    "solution": "A = (1/2)∫₀^(π/6) cos²θ dθ = ∫₀^(π/6) (1 + cos 2θ)/4 dθ = [θ/4 + sin(2θ)/8]₀^(π/6). Therefore A = π/24 + √3/16 ≈ 0.239152869 square units.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 10,
      "section": "10.4",
      "exercise": "2",
      "pdfPage": 703,
      "printedPage": "672"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Use A = (1/2)∫ r² dθ and the half-angle identity for cos²θ.",
      "Substitute r = cos θ into ½∫r² dθ, keeping the factor ½.",
      "Use cos²θ = (1 + cos 2θ)/2. Evaluate θ/4 + sin(2θ)/8 at the bounds in radians."
    ]
  },
  {
    "id": "stewart-11-1-23",
    "chapter": "11 · Infinite Sequences and Series",
    "topic": "Sequence limits",
    "title": "Limit of a rational sequence",
    "prompt": "Determine whether the sequence converges or diverges. If it converges, find the limit: aₙ = (3 + 5n²)/(n + n²).",
    "answer": 5.0,
    "unit": "",
    "tolerance": 0.001,
    "hint": "Divide numerator and denominator by n².",
    "solution": "aₙ = (3/n² + 5)/(1/n + 1). As n → ∞, the terms 3/n² and 1/n tend to 0. The sequence converges to 5/1 = 5.",
    "level": "Foundation",
    "source": {
      "book": "calculus",
      "chapter": 11,
      "section": "11.1",
      "exercise": "23",
      "pdfPage": 735,
      "printedPage": "704"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Divide numerator and denominator by n².",
      "Rewrite the expression as (3/n² + 5)/(1/n + 1).",
      "As n grows without bound, terms with n in the denominator approach zero."
    ]
  },
  {
    "id": "stewart-12-3-49",
    "chapter": "12 · Vectors and the Geometry of Space",
    "topic": "Dot products and work",
    "title": "Work by a constant force",
    "prompt": "Find the work done by a force F = 8i − 6j + 9k that moves an object from the point (0, 10, 8) to the point (6, 12, 20) along a straight line. The distance is measured in meters and the force in newtons.",
    "answer": 144.0,
    "unit": "J",
    "tolerance": 0.01,
    "hint": "Work is the dot product of force and displacement.",
    "solution": "The displacement is ⟨6 − 0, 12 − 10, 20 − 8⟩ = ⟨6, 2, 12⟩ m. Work = ⟨8, −6, 9⟩ · ⟨6, 2, 12⟩ = 48 − 12 + 108 = 144 J.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 12,
      "section": "12.3",
      "exercise": "49",
      "pdfPage": 844,
      "printedPage": "813"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Work is the dot product of force and displacement.",
      "Displacement is the final position minus the initial position, component by component.",
      "Multiply each force component by its matching displacement component, then add. Keep the negative y-force sign."
    ]
  },
  {
    "id": "stewart-12-3-39-scalar-projection-only",
    "chapter": "12 · Vectors and the Geometry of Space",
    "topic": "Scalar projection",
    "title": "Projection onto a vector · scalar portion",
    "prompt": "Find the scalar projection of b onto a: a = ⟨−5, 12⟩, b = ⟨4, 6⟩.",
    "answer": 4.0,
    "unit": "",
    "tolerance": 0.001,
    "hint": "The scalar projection is (a · b)/|a|.",
    "solution": "a · b = (−5)(4) + 12(6) = 52, and |a| = √(25 + 144) = 13. Hence compₐ b = 52/13 = 4. This grades only the scalar projection requested in Exercise 39.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 12,
      "section": "12.3",
      "exercise": "39 (scalar projection only)",
      "pdfPage": 844,
      "printedPage": "813"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "The source asks for scalar and vector projections. Only the scalar projection is presented and graded.",
    "hints": [
      "The scalar projection is (a · b)/|a|.",
      "Compute a · b = (−5)(4) + (12)(6), and |a| = √[(-5)² + 12²].",
      "Divide the dot product by |a|, not |a|². The requested result is a scalar."
    ]
  },
  {
    "id": "stewart-13-3-1",
    "chapter": "13 · Vector Functions",
    "topic": "Space-curve arc length",
    "title": "Length of a helix",
    "prompt": "Find the length of the curve: r(t) = ⟨t, 3 cos t, 3 sin t⟩, −5 ≤ t ≤ 5.",
    "answer": 31.622776601683796,
    "unit": "units",
    "tolerance": 0.001,
    "hint": "Integrate the magnitude of r′(t) over the parameter interval.",
    "solution": "r′(t) = ⟨1, −3 sin t, 3 cos t⟩. Its magnitude is √(1 + 9sin²t + 9cos²t) = √10. The length is ∫₋₅⁵ √10 dt = 10√10 ≈ 31.622777.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 13,
      "section": "13.3",
      "exercise": "1",
      "pdfPage": 899,
      "printedPage": "868"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Integrate the magnitude of r′(t) over the parameter interval.",
      "Differentiate each component: r′(t) = ⟨1, −3 sin t, 3 cos t⟩.",
      "Use sin²t + cos²t = 1 in the speed. Multiply that constant speed by the full parameter interval."
    ]
  },
  {
    "id": "stewart-14-3-41",
    "chapter": "14 · Partial Derivatives",
    "topic": "Partial derivatives",
    "title": "An indicated partial derivative",
    "prompt": "Find the indicated partial derivative: R(s, t) = t e^(s/t); R_t(0, 1).",
    "answer": 1.0,
    "unit": "",
    "tolerance": 0.001,
    "hint": "Differentiate with respect to t while holding s constant; use both product and chain rules.",
    "solution": "R_t(s, t) = e^(s/t) + t e^(s/t)(−s/t²) = e^(s/t)(1 − s/t). At (s, t) = (0, 1), this gives e⁰(1 − 0) = 1.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 14,
      "section": "14.3",
      "exercise": "41",
      "pdfPage": 955,
      "printedPage": "924"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Differentiate with respect to t while holding s constant; use both product and chain rules.",
      "The product rule gives e^(s/t) + t e^(s/t)(−s/t²).",
      "Hold s constant while differentiating, then substitute s = 0 and t = 1."
    ]
  },
  {
    "id": "stewart-15-1-16",
    "chapter": "15 · Multiple Integrals",
    "topic": "Iterated integrals",
    "title": "A double polynomial integral",
    "prompt": "Calculate the iterated integral: ∫ from y = 0 to 1 of [∫ from x = 0 to 1 of (x + y)² dx] dy.",
    "answer": 1.1666666666666667,
    "unit": "",
    "tolerance": 0.001,
    "hint": "Expand the square and integrate with respect to x first.",
    "solution": "The inner integral is ∫₀¹ (x² + 2xy + y²) dx = 1/3 + y + y². Integrating in y gives [y/3 + y²/2 + y³/3]₀¹ = 1/3 + 1/2 + 1/3 = 7/6 ≈ 1.166667.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 15,
      "section": "15.1",
      "exercise": "16",
      "pdfPage": 1030,
      "printedPage": "999"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Expand the square and integrate with respect to x first.",
      "Expand (x + y)² as x² + 2xy + y². Treat y as constant in the inner integral.",
      "After integrating over x, integrate 1/3 + y + y² over y from 0 to 1."
    ]
  },
  {
    "id": "stewart-16-2-45",
    "chapter": "16 · Vector Calculus",
    "topic": "Work along a space curve",
    "title": "Climbing a helical staircase",
    "prompt": "A 160-lb man carries a 25-lb can of paint up a helical staircase that encircles a silo with a radius of 20 ft. If the silo is 90 ft high and the man makes exactly three complete revolutions climbing to the top, how much work is done by the man against gravity?",
    "answer": 16650.0,
    "unit": "ft·lb",
    "tolerance": 0.01,
    "hint": "Gravity contributes work according to the vertical height gained. The weights are already forces in pounds.",
    "solution": "The total weight lifted is 160 + 25 = 185 lb. Against gravity, the line integral is ∫ 185 dz = 185(z_final − z_initial). The vertical rise is 90 ft, so the work is 185 × 90 = 16,650 ft·lb. The radius and number of turns do not change this gravitational work.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 16,
      "section": "16.2",
      "exercise": "45",
      "pdfPage": 1117,
      "printedPage": "1086"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "hints": [
      "Gravity contributes work according to the vertical height gained. The weights are already forces in pounds.",
      "Add the man’s weight and the can’s weight, then multiply by the vertical rise.",
      "The weights are already forces. Do not multiply by g or by the length of the helical path."
    ]
  },
  {
    "id": "stewart-17-3-6-uses-exercise-4",
    "chapter": "17 · Second-Order Differential Equations",
    "topic": "Critical damping",
    "title": "Critical damping of a spring",
    "prompt": "For the spring in Exercise 4, find the damping constant that would produce critical damping. Exercise 4 data: A force of 13 N is needed to keep a spring with a 2-kg mass stretched 0.25 m beyond its natural length.",
    "answer": 20.396078054371138,
    "unit": "N·s/m",
    "tolerance": 0.001,
    "hint": "Find the spring constant from Hooke’s law, then set the characteristic discriminant c² − 4mk equal to zero.",
    "solution": "Hooke’s law gives k = 13/0.25 = 52 N/m. For m x″ + c x′ + kx = 0, critical damping occurs when c² − 4mk = 0. Thus c = 2√(mk) = 2√(2·52) = 4√26 ≈ 20.396078 N·s/m.",
    "level": "Core",
    "source": {
      "book": "calculus",
      "chapter": 17,
      "section": "17.3",
      "exercise": "6 (uses Exercise 4)",
      "pdfPage": 1206,
      "printedPage": "1175"
    },
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "Exercise 6 is quoted; the force, mass, and stretch data it references are supplied from Exercise 4 on the same page.",
    "hints": [
      "Find the spring constant from Hooke’s law, then set the characteristic discriminant c² − 4mk equal to zero.",
      "First use k = F/stretch. Critical damping requires c² = 4mk.",
      "Use the positive root c = 2√(mk). Keep mass in kg and stretch in meters."
    ]
  }
];
