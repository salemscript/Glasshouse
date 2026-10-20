// Selected and adapted OpenStax McMurry exercises. ©2023 Rice University, CC BY-NC-SA 4.0. App-authored hints and solutions.
window.ORGANIC_BANK = [
  {
    "id": "mcmurry-2-49a",
    "chapter": "02 · Polar Covalent Bonds; Acids and Bases",
    "topic": "Acid strength",
    "title": "From pKₐ to Kₐ · Acetone",
    "prompt": "Calculate Kₐ values from the following pKₐ’s: Acetone, pKₐ = 19.3.",
    "answer": 5.011872336272715e-20,
    "tolerance": 2.5059361681363575e-22,
    "unit": "",
    "hint": "pKₐ is the negative base-10 logarithm of Kₐ.",
    "hints": [
      "pKₐ is the negative base-10 logarithm of Kₐ.",
      "Invert the definition: Kₐ = 10^(−pKₐ). Use the 10ˣ key, not eˣ.",
      "Keep the minus sign in the exponent. Enter a very small result using scientific notation."
    ],
    "solution": "Kₐ = 10^(−19.3) = 5.01187e-20. A larger pKₐ corresponds to a smaller dissociation constant.",
    "level": "Core",
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "Only the named subpart of Exercise 2-49 is presented and graded.",
    "source": {
      "book": "organic",
      "chapter": 2,
      "section": "Additional Problems",
      "exercise": "2-49a",
      "pdfPage": 85,
      "printedPage": "67"
    }
  },
  {
    "id": "mcmurry-2-49b",
    "chapter": "02 · Polar Covalent Bonds; Acids and Bases",
    "topic": "Acid strength",
    "title": "From pKₐ to Kₐ · Formic acid",
    "prompt": "Calculate Kₐ values from the following pKₐ’s: Formic acid, pKₐ = 3.75.",
    "answer": 0.00017782794100389227,
    "tolerance": 8.891397050194613e-07,
    "unit": "",
    "hint": "pKₐ is the negative base-10 logarithm of Kₐ.",
    "hints": [
      "pKₐ is the negative base-10 logarithm of Kₐ.",
      "Invert the definition: Kₐ = 10^(−pKₐ). Use the 10ˣ key, not eˣ.",
      "Keep the minus sign in the exponent. Enter a very small result using scientific notation."
    ],
    "solution": "Kₐ = 10^(−3.75) = 0.000177828. A larger pKₐ corresponds to a smaller dissociation constant.",
    "level": "Core",
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "Only the named subpart of Exercise 2-49 is presented and graded.",
    "source": {
      "book": "organic",
      "chapter": 2,
      "section": "Additional Problems",
      "exercise": "2-49b",
      "pdfPage": 85,
      "printedPage": "67"
    }
  },
  {
    "id": "mcmurry-2-50a",
    "chapter": "02 · Polar Covalent Bonds; Acids and Bases",
    "topic": "Acid strength",
    "title": "From Kₐ to pKₐ · Nitromethane",
    "prompt": "Calculate pKₐ values from the following Kₐ’s: Nitromethane, Kₐ = 5.0 × 10⁻¹¹.",
    "answer": 10.301029995663981,
    "tolerance": 0.005,
    "unit": "",
    "hint": "Use pKₐ = −log₁₀(Kₐ).",
    "hints": [
      "Use pKₐ = −log₁₀(Kₐ).",
      "Enter the complete scientific-notation value into the base-10 logarithm, then negate the result.",
      "Because Kₐ is less than one, its logarithm is negative. The resulting pKₐ is positive."
    ],
    "solution": "pKₐ = −log₁₀(5.0 × 10⁻¹¹) = 10.301030.",
    "level": "Core",
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "Only the named subpart of Exercise 2-50 is presented and graded.",
    "source": {
      "book": "organic",
      "chapter": 2,
      "section": "Additional Problems",
      "exercise": "2-50a",
      "pdfPage": 85,
      "printedPage": "67"
    }
  },
  {
    "id": "mcmurry-2-50b",
    "chapter": "02 · Polar Covalent Bonds; Acids and Bases",
    "topic": "Acid strength",
    "title": "From Kₐ to pKₐ · Acrylic acid",
    "prompt": "Calculate pKₐ values from the following Kₐ’s: Acrylic acid, Kₐ = 5.6 × 10⁻⁵.",
    "answer": 4.251811972993799,
    "tolerance": 0.005,
    "unit": "",
    "hint": "Use pKₐ = −log₁₀(Kₐ).",
    "hints": [
      "Use pKₐ = −log₁₀(Kₐ).",
      "Enter the complete scientific-notation value into the base-10 logarithm, then negate the result.",
      "Because Kₐ is less than one, its logarithm is negative. The resulting pKₐ is positive."
    ],
    "solution": "pKₐ = −log₁₀(5.6 × 10⁻⁵) = 4.251812.",
    "level": "Core",
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "Only the named subpart of Exercise 2-50 is presented and graded.",
    "source": {
      "book": "organic",
      "chapter": 2,
      "section": "Additional Problems",
      "exercise": "2-50b",
      "pdfPage": 85,
      "printedPage": "67"
    }
  },
  {
    "id": "mcmurry-7-34a",
    "chapter": "07 · Alkenes: Structure and Reactivity",
    "topic": "Degree of unsaturation",
    "title": "Count unsaturation · C₁₀H₁₆",
    "prompt": "Calculate the degree of unsaturation in the following formula: C₁₀H₁₆.",
    "answer": 3,
    "tolerance": 0,
    "unit": "",
    "hint": "A saturated, acyclic hydrocarbon has formula CₙH₂ₙ₊₂.",
    "hints": [
      "A saturated, acyclic hydrocarbon has formula CₙH₂ₙ₊₂.",
      "For ten carbons, compare the given H count with 2(10) + 2.",
      "Each ring or double bond removes two hydrogens; divide the hydrogen deficit by two."
    ],
    "solution": "DU = (2C + 2 − H)/2 = [2(10) + 2 − 16]/2 = 3. The formula alone does not specify where the rings or multiple bonds are.",
    "level": "Core",
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "Adapted from 7-34(a): only the degree of unsaturation is graded; the request to draw five structures is omitted.",
    "source": {
      "book": "organic",
      "chapter": 7,
      "section": "Additional Problems",
      "exercise": "7-34a",
      "pdfPage": 255,
      "printedPage": "237"
    }
  },
  {
    "id": "mcmurry-7-36",
    "chapter": "07 · Alkenes: Structure and Reactivity",
    "topic": "Degree of unsaturation",
    "title": "Find loratadine’s hydrogen count",
    "prompt": "Loratadine, marketed as an antiallergy medication under the brand name Claritin, has four rings, eight double bonds, and the formula C₂₂H?ClN₂O₂. How many hydrogens does loratadine have? (Calculate your answer; don’t count hydrogens in the structure.)",
    "answer": 23,
    "tolerance": 0,
    "unit": "",
    "hint": "Four rings plus eight double bonds give twelve degrees of unsaturation.",
    "hints": [
      "Four rings plus eight double bonds give twelve degrees of unsaturation.",
      "Use DU = (2C + 2 + N − H − X)/2, where X counts halogens. Oxygen does not enter this formula.",
      "Rearrange to H = 2C + 2 + N − X − 2DU, then substitute C = 22, N = 2, X = 1."
    ],
    "solution": "H = 2(22) + 2 + 2 − 1 − 2(12) = 23. The molecular formula is C₂₂H₂₃ClN₂O₂.",
    "level": "Core",
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "The source illustration is omitted because the problem explicitly asks for calculation from the stated formula and bond counts.",
    "source": {
      "book": "organic",
      "chapter": 7,
      "section": "Additional Problems",
      "exercise": "7-36",
      "pdfPage": 255,
      "printedPage": "237"
    }
  },
  {
    "id": "mcmurry-7-67a",
    "chapter": "07 · Alkenes: Structure and Reactivity",
    "topic": "Degree of unsaturation",
    "title": "Cholesterol’s unsaturation",
    "prompt": "Calculate the degree of unsaturation in the following formula: Cholesterol, C₂₇H₄₆O.",
    "answer": 5,
    "tolerance": 0,
    "unit": "",
    "hint": "Oxygen does not change the degree-of-unsaturation calculation.",
    "hints": [
      "Oxygen does not change the degree-of-unsaturation calculation.",
      "Use DU = (2C + 2 − H)/2 for a formula containing only C, H, and O.",
      "Substitute C = 27 and H = 46; divide the entire numerator by two."
    ],
    "solution": "DU = [2(27) + 2 − 46]/2 = 5. These five units can be distributed among rings and multiple bonds.",
    "level": "Core",
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "Only subpart (a) of Exercise 7-67 is presented and graded.",
    "source": {
      "book": "organic",
      "chapter": 7,
      "section": "Additional Problems",
      "exercise": "7-67a",
      "pdfPage": 259,
      "printedPage": "241"
    }
  },
  {
    "id": "mcmurry-13-31b",
    "chapter": "13 · Nuclear Magnetic Resonance Spectroscopy",
    "topic": "NMR chemical shift",
    "title": "NMR: ppm to hertz",
    "prompt": "When measured on a spectrometer operating at 200 MHz, chloroform (CHCl₃) shows a single sharp absorption at 7.3 δ. How many hertz downfield from TMS would chloroform absorb if the measurement were carried out on a spectrometer operating at 360 MHz?",
    "answer": 2628,
    "tolerance": 1,
    "unit": "Hz",
    "hint": "Chemical shift in ppm is independent of spectrometer frequency.",
    "hints": [
      "Chemical shift in ppm is independent of spectrometer frequency.",
      "Use Δν (Hz) = δ (ppm) × spectrometer frequency (MHz).",
      "Use the requested 360 MHz instrument, not the original 200 MHz instrument."
    ],
    "solution": "Δν = 7.3 × 360 = 2628 Hz downfield from TMS. The chemical shift remains 7.3 ppm.",
    "level": "Core",
    "origin": "textbook",
    "solutionAuthored": true,
    "selection": "The setup and subpart (b) of Exercise 13-31 are presented and graded.",
    "source": {
      "book": "organic",
      "chapter": 13,
      "section": "Additional Problems",
      "exercise": "13-31b",
      "pdfPage": 463,
      "printedPage": "445"
    }
  }
];
