# Organic Chemistry Chapters 6–11 review

Reviewed 2026-10-26. All 368 source questions have exposed numeric or choice checks; runtime testing covers 1,163 fields. Added checks to 302 previously unchecked questions and expanded/reviewed existing checks. Integration updates 351 records, preserving original textbook statements and other chapters.

Each chapter owner inspected actual PDF figures and authored original reasoning. Secondary reviews checked Chapter 7 rearrangements/stereochemistry, all Chapter 8 new records, Chapter 9 difficult structure and synthesis exercises, and Chapter 11 stereochemistry/mechanism exercises. Root independently checked shared instructions, stereoisomer enumeration, selected numeric calculations, reaction-condition ambiguities, and source-part mapping.

## Deliberate limits

214 questions retain explicit drawing, model, or source-scope limits. Choosing a structure or mechanism is not automatic assessment of a learner-produced drawing. Nonunique synthesis routes and structures are presented as valid examples, with ambiguity noted. No experimental product ratio is inferred from missing solvent, temperature, or stereochemical information.

## Notable source findings

- 6-38: independent enumeration gives 3, 6, and 10 stereoisomers; reference images contain a duplicate and an omission.
- 6-36(e): equivalent methyl groups alone do not make an unsaturated radical chlorination a clean single-product process.
- 7-17(d): simple addition prediction requires an explicit rearrangement limitation.
- 8-56 and 8-70: structural clues do not establish one unique starting structure.
- 9-41: the only-carbon-source restriction is preserved by deriving chloroform from a second portion of the starting alkyne.
- 10-44(c): count all 14 hydrogens of 3-methylpentane when weighting radical bromination products.
- 11-21: distinguish conditional textbook elimination products from an experimentally unique outcome under unspecified conditions.
- 11-68: E-specific elimination at the target bond does not exclude a different regioisomer.
- 11-71: optical inactivity alone does not distinguish a meso compound from a racemic mixture.

## Verification

Run `python scripts/organic-answer-checks/integrate-6-11.py`, then `node scripts/organic-answer-checks/verify-runtime-6-11.cjs`. The latter tests accepted answers, every wrong choice, wrong numeric values, empty responses, source-part availability, chemical-text escaping, and preservation of mathematical fraction rendering. Previous Chapters 1–5 regression test also passes. Export hashes/local references pass. Browser QA confirms visible referenced diagrams, correct feedback on numeric and structure choices, and chemical R/S displayed as notation rather than division.
