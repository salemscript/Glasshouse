# Physics chapter-end equation reference

Covers all 44 chapters of Halliday, Resnick & Walker, *Fundamentals of Physics, Extended*, 10th edition, from the supplied chapter PDFs already in `site/books/physics/`.

The actual section heading is **Review & Summary**. The chapter directory in `site/book-data.js` locates every summary. `author.py` extracts its pages, checks cited equation numbers against those pages (including ranges), generates 467 native MathML equation lines in 193 topic groups, and records source PDF SHA-256 fingerprints and exact page references in `source-audit.json`. All 548 numbered references appearing in those summaries are covered. Multiple equivalent relations or component forms may share one displayed line; “467 lines” is not a claim that the book numbers exactly 467 equations.

Transcriptions contain mathematical facts; symbol/unit guides, search organization, and teaching annotations are original. No solution-manual text is used. Unnumbered mathematical relationships in the summaries are included where applicable. No textbook prose or page images were added to the public application; source buttons open existing PDFs at the exact pages.

Important editorial distinctions: constant-acceleration restrictions; signed work and heat; ideal-gas adiabats requiring reversibility; isolated-system entropy; magnitudes versus vector components; source versus passive power; peak versus RMS AC amplitudes; thin-film reflection phase changes; image-distance conventions; the historical Bohr angular-momentum rule explicitly marked as incorrect; the book’s uncertainty-width convention distinguished from a standard-deviation bound; the edition’s Hubble value and approximate Lawson benchmark identified as textbook values. Chapter 1 keeps density and unit conversion without repeating obsolete SI-definition prose.

## Build and validate

Build dependencies: Python 3, Poppler `pdftotext`, and `python3 -m pip install -r scripts/physics-formulas/requirements.txt`. Then:

    python3 scripts/physics-formulas/author.py
    python3 scripts/physics-formulas/check.py
    node --check site/physics-formula-data.js
    node --check site/physics-formulas.js
    node --check site/study.js

`check.py` uses only the Python standard library. Its 1,949 checks cover source fingerprints, 44-chapter completeness, all numbered-summary reference coverage, group identifiers, valid MathML, page bounds, and independent numerical checks of related physical identities: constant-acceleration kinematics, projectile range, RC current/energy balance, relativistic momentum/energy, Maxwell-distribution normalization and second moment, well-wavefunction normalization and Schrödinger eigenenergy, density-of-states integration versus Fermi energy, Planck integration versus Stefan–Boltzmann, thin-film phase, and ideal-gas adiabatic entropy. These numerical checks supplement source review; they do not independently prove every transcription.

## UI behavior and browser review

The Physics Formulas tab uses a dedicated chapter/search reference. Chapter choice updates the route and the chapter used by other study tabs. Search spans all chapters and includes titles, equations, reference numbers, symbol guides, and assumptions; Greek symbols and names are normalized. Clearing search returns to the chosen scope. All-chapter mode lazily renders closed chapters to keep the initial DOM small; only opened or directly selected chapters render their equation cards.

Reviewed in Chromium on October 23, 2026. Chapter 27 displays all six groups; searching `27-33` returns RC charging; its source button opens global PDF page 819, local chapter page 23, printed page 793. All-chapter scope shows 44 summaries and initially renders only the active chapter’s six cards; Chapter 44 opens its two groups on demand. Unknown search has an accessible clear action. At 390 px viewport, document/client width are both 375 px, and the six long Chapter 31 equation lines scroll inside their own regions. Light and dark math contrast was visually checked. Sum limits and fractions are native MathML; a braced script E preserves the distinct emf glyph. Source renderings of Chapters 36, 38 and 41 were inspected to resolve the grating half-width, uncertainty convention, Planck coefficient, and density-of-states coefficient. No Safari or assistive-technology certification claimed.
