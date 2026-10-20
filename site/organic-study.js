'use strict';
// App-authored checks and references grounded in McMurry, Organic Chemistry, OpenStax 10th ed.
window.STUDY_DATA = window.STUDY_DATA || {};
window.STUDY_DATA.organic = [
  [
    1,
    "Structure and Bonding",
    "How many σ and π bonds form a carbon–carbon triple bond?",
    [
      "One σ bond and two π bonds.",
      "Three σ bonds.",
      "Two σ bonds and one π bond.",
      "Three π bonds."
    ],
    0,
    "The sp orbitals form the σ bond; two pairs of unhybridized p orbitals form the two π bonds.",
    "C≡C: 1 σ + 2 π; carbon is sp-hybridized.",
    "For an ordinary carbon–carbon triple bond; its bond axes are approximately linear. Reference: chapter 1 Summary, PDF p. 47 (printed p. 29)."
  ],
  [
    2,
    "Polar Covalent Bonds; Acids and Bases",
    "Within the same solvent, which acid is strongest?",
    [
      "The acid with the largest pKa.",
      "The acid with the smallest pKa.",
      "The acid with the smallest Ka.",
      "All acids have identical strength."
    ],
    1,
    "A smaller pKa means a larger acid-dissociation constant and greater tendency to donate a proton.",
    "pKa = −log₁₀Ka",
    "Compare values determined under comparable solvent and temperature conditions. Reference: chapter 2 Summary, PDF p. 80 (printed p. 62)."
  ],
  [
    3,
    "Organic Compounds: Alkanes and Their Stereochemistry",
    "Which statement describes constitutional isomers?",
    [
      "Same connectivity, different bond rotation only.",
      "Different molecular formulas, same mass.",
      "Same molecular formula, different atom connectivity.",
      "Mirror images with identical connectivity."
    ],
    2,
    "Constitutional isomers differ in the connections between atoms; conformers differ only by rotations.",
    "Acyclic saturated alkane: CₙH₂ₙ₊₂",
    "The alkane formula assumes an open-chain hydrocarbon with no rings or multiple bonds. Reference: chapter 3 Summary, PDF p. 116 (printed p. 98)."
  ],
  [
    4,
    "Organic Compounds: Cycloalkanes and Their Stereochemistry",
    "Why does methylcyclohexane favor an equatorial methyl group?",
    [
      "It changes the molecular formula.",
      "It removes all carbon–carbon bonds.",
      "It forces the ring into a planar hexagon.",
      "It reduces 1,3-diaxial steric interactions."
    ],
    3,
    "An axial methyl group crowds axial hydrogens on carbons three positions away; equatorial placement reduces that crowding.",
    "Chair flip: axial ⇄ equatorial; up/down orientation is retained.",
    "Apply to cyclohexane chairs; a ring flip changes conformation, not cis/trans configuration. Reference: chapter 4 Summary, PDF p. 145 (printed p. 127)."
  ],
  [
    5,
    "Stereochemistry at Tetrahedral Centers",
    "What defines a pair of enantiomers?",
    [
      "Nonsuperimposable mirror-image stereoisomers.",
      "Isomers differing only in connectivity.",
      "Any two conformers of one molecule.",
      "Any two molecules with different formulas."
    ],
    0,
    "Enantiomers share connectivity but are mirror images that cannot be superimposed.",
    "Maximum configurations from n independent stereocenters: 2ⁿ",
    "The actual count can be smaller because of symmetry, including meso forms; R/S does not predict rotation sign. Reference: chapter 5 Summary, PDF p. 180 (printed p. 162)."
  ],
  [
    6,
    "An Overview of Organic Reactions",
    "In a polar reaction, what does an ordinary double-barbed curved arrow track?",
    [
      "Movement of an atomic nucleus.",
      "Movement of an electron pair.",
      "Movement of a single electron only.",
      "The path of an entire solvent molecule."
    ],
    1,
    "A double-barbed arrow starts at an electron pair or bond and points to its destination; a fishhook tracks one electron.",
    "Nucleophile donates an electron pair to an electrophile.",
    "Use double-barbed arrows for polar mechanisms and fishhooks for single-electron radical steps. Reference: chapter 6 Summary, PDF p. 216 (printed p. 198)."
  ],
  [
    7,
    "Alkenes: Structure and Reactivity",
    "During ionic addition of HBr to propene, why is 2-bromopropane the major product?",
    [
      "Bromide first removes every hydrogen.",
      "A primary carbocation is always more stable.",
      "Protonation favors the more stable secondary carbocation.",
      "The double bond remains unchanged."
    ],
    2,
    "Protonation that gives the secondary carbocation is favored; bromide then bonds at that carbon.",
    "Markovnikov addition: H adds to the carbon bearing more H atoms.",
    "For the ordinary ionic HBr mechanism without peroxide-driven radical conditions; rearrangements can matter for other substrates. Reference: chapter 7 Summary, PDF p. 252 (printed p. 234)."
  ],
  [
    8,
    "Alkenes: Reactions and Synthesis",
    "What alcohol forms from hydroboration–oxidation of propene?",
    [
      "2-Propanol.",
      "Propanone.",
      "Propanoic acid.",
      "1-Propanol."
    ],
    3,
    "Hydroboration places boron at the less substituted carbon; oxidation replaces C–B with C–OH.",
    "Alkene → alcohol: 1. BH₃; 2. H₂O₂, OH⁻",
    "Net non-Markovnikov hydration with syn addition; use the sequential reagents shown. Reference: chapter 8 Summary, PDF p. 293 (printed p. 275)."
  ],
  [
    9,
    "Alkynes: An Introduction to Organic Synthesis",
    "Partial hydrogenation of an internal alkyne with Lindlar catalyst gives which product?",
    [
      "A cis alkene.",
      "A trans alkene as the sole product.",
      "A ketone.",
      "A carboxylic acid."
    ],
    0,
    "The poisoned catalyst allows syn addition of hydrogen and stops at the alkene stage.",
    "Internal alkyne + H₂/Lindlar → cis alkene",
    "Contrast dissolving-metal reduction, which favors trans alkenes; terminal alkene products have no cis/trans pair. Reference: chapter 9 Summary, PDF p. 323 (printed p. 305)."
  ],
  [
    10,
    "Organohalides",
    "Why must Grignard reagents be kept away from water?",
    [
      "Water makes the C–Mg bond permanent.",
      "Water protonates and destroys the reagent.",
      "Water converts every reagent to benzene.",
      "Water prevents any acid–base reaction."
    ],
    1,
    "The carbon bonded to magnesium is strongly basic and reacts with a proton donor to produce a hydrocarbon.",
    "RMgX + H₂O → RH + Mg(OH)X",
    "Prepare and use Grignard reagents in dry ether; avoid acidic O–H or N–H groups before workup. Reference: chapter 10 Summary, PDF p. 350 (printed p. 332)."
  ],
  [
    11,
    "Reactions of Alkyl Halides: Nucleophilic Substitutions and Eliminations",
    "What stereochemical change occurs at a reacting stereocenter in an SN2 substitution?",
    [
      "Guaranteed retention from frontside attack.",
      "Complete carbocation equilibration.",
      "Inversion of configuration from backside attack.",
      "Loss of all stereocenters in the molecule."
    ],
    2,
    "The nucleophile attacks opposite the leaving group, causing geometrical inversion at the reacting carbon.",
    "SN2 rate = k[substrate][nucleophile]",
    "For a concerted SN2 step; an R label need not become S if substituent priority order changes. Reference: chapter 11 Summary, PDF p. 390 (printed p. 372)."
  ],
  [
    12,
    "Structure Determination: Mass Spectrometry and Infrared Spectroscopy",
    "What do infrared absorption bands primarily report about an organic molecule?",
    [
      "The exact number of all stereocenters.",
      "Its proton NMR integration.",
      "Its chromosome sequence.",
      "Its bond vibrations and functional groups."
    ],
    3,
    "IR absorption occurs when radiation excites appropriate stretching or bending vibrations.",
    "IR wavenumber: ν̃ = 1/λ; units cm⁻¹",
    "Band positions depend on bond type and environment; IR-active vibrations change dipole moment. Use multiple bands together. Reference: chapter 12 Summary, PDF p. 427 (printed p. 409)."
  ],
  [
    13,
    "Structure Determination: Nuclear Magnetic Resonance Spectroscopy",
    "A proton coupled to two equivalent neighboring protons in a simple first-order spectrum usually gives what pattern?",
    [
      "A triplet.",
      "A singlet.",
      "A doublet.",
      "A quartet."
    ],
    0,
    "For n equivalent coupled neighbors, the first-order n + 1 rule gives three lines when n = 2.",
    "First-order splitting: n equivalent neighbors → n + 1 lines",
    "The simple rule assumes suitable first-order coupling; exchangeable protons, nonequivalent neighbors and strong coupling can behave differently. Reference: chapter 13 Summary, PDF p. 461 (printed p. 443)."
  ],
  [
    14,
    "Conjugated Compounds and Ultraviolet Spectroscopy",
    "Which diene conformation is needed for a standard Diels–Alder cycloaddition?",
    [
      "s-Trans locked so it cannot rotate.",
      "s-Cis.",
      "A saturated chain with no π bonds.",
      "A diene with no conjugation."
    ],
    1,
    "The s-cis arrangement places the conjugated diene ends close enough to form the two new σ bonds.",
    "Conjugated diene + dienophile → cyclohexene framework",
    "The diene must be able to adopt s-cis; the usual thermal [4+2] reaction is concerted and stereospecific. Reference: chapter 14 Summary, PDF p. 496 (printed p. 478)."
  ],
  [
    15,
    "Benzene and Aromaticity",
    "Which π-electron count can satisfy the Hückel rule for a planar, cyclic, fully conjugated ring?",
    [
      "Four π electrons.",
      "Eight π electrons.",
      "Six π electrons.",
      "Twelve π electrons."
    ],
    2,
    "Six satisfies 4n + 2 with n = 1. Counting electrons alone is insufficient without the stated geometry and conjugation.",
    "Aromatic monocyclic π system: 4n + 2 electrons",
    "Requires cyclic, planar, uninterrupted p-orbital overlap; 4n systems under these conditions are antiaromatic. Reference: chapter 15 Summary, PDF p. 527 (printed p. 509)."
  ],
  [
    16,
    "Chemistry of Benzene: Electrophilic Aromatic Substitution",
    "How does chlorine on chlorobenzene affect electrophilic aromatic substitution?",
    [
      "It activates the ring and directs only meta.",
      "It deactivates the ring and directs only meta.",
      "It removes the need for an electrophile.",
      "It deactivates the ring but directs ortho/para."
    ],
    3,
    "Its inductive withdrawal deactivates the ring, while lone-pair resonance donation favors ortho and para attack.",
    "Halogens: deactivating, ortho/para-directing substituents.",
    "For electrophilic aromatic substitution; directing effects differ from nucleophilic aromatic substitution. Reference: chapter 16 Summary, PDF p. 575 (printed p. 557)."
  ],
  [
    17,
    "Alcohols and Phenols",
    "Which product typically forms when a secondary alcohol is oxidized without C–C bond cleavage?",
    [
      "A ketone.",
      "An aldehyde.",
      "An ether.",
      "An alkane."
    ],
    0,
    "Oxidation removes hydrogen from oxygen and the hydroxyl-bearing carbon to form a carbonyl.",
    "R₂CHOH → R₂C=O",
    "For ordinary secondary-alcohol oxidation; tertiary alcohols lack the necessary hydrogen and resist analogous oxidation. Reference: chapter 17 Summary, PDF p. 620 (printed p. 602)."
  ],
  [
    18,
    "Ethers and Epoxides; Thiols and Sulfides",
    "Where does a strong nucleophile generally attack an unsymmetrical epoxide under basic conditions?",
    [
      "Always at the more substituted carbon.",
      "At the less hindered epoxide carbon.",
      "Only at the oxygen atom.",
      "Only at a remote methyl group."
    ],
    1,
    "Basic ring opening follows an SN2-like attack at the less crowded carbon, breaking that carbon–oxygen bond.",
    "Epoxide + Nu⁻ → ring-opened alkoxide → alcohol after workup",
    "For nucleophilic opening under basic conditions; acid-catalyzed regiochemistry requires a separate analysis. Reference: chapter 18 Summary, PDF p. 652 (printed p. 634)."
  ],
  [
    19,
    "Aldehydes and Ketones: Nucleophilic Addition Reactions",
    "After aqueous workup, what does NaBH₄ reduction of an ordinary ketone produce?",
    [
      "An alkene.",
      "A carboxylic acid.",
      "A secondary alcohol.",
      "An amide."
    ],
    2,
    "Hydride adds to the carbonyl carbon, and the resulting alkoxide is protonated during workup.",
    "R₂C=O → R₂CHOH",
    "NaBH₄ reduces ordinary aldehydes and ketones; do not assume identical reactivity for all carboxylic acid derivatives. Reference: chapter 19 Summary, PDF p. 710 (printed p. 692)."
  ],
  [
    20,
    "Carboxylic Acids and Nitriles",
    "Why is acetic acid more acidic than ethanol?",
    [
      "Its conjugate base has no electrons.",
      "Ethanol cannot contain an O–H bond.",
      "Acetic acid is a hydrocarbon.",
      "Its conjugate base is resonance stabilized over two oxygens."
    ],
    3,
    "Acetate delocalizes its negative charge over two equivalent oxygens; ethoxide lacks that stabilization.",
    "pH = pKa + log₁₀([A⁻]/[HA])",
    "Henderson–Hasselbalch applies to acid/base equilibrium; the concentration form approximates activities in dilute solutions. Reference: chapter 20 Summary, PDF p. 747 (printed p. 729)."
  ],
  [
    21,
    "Carboxylic Acid Derivatives: Nucleophilic Acyl Substitution Reactions",
    "What is the key mechanistic sequence in nucleophilic acyl substitution?",
    [
      "Nucleophilic addition, then elimination of a leaving group.",
      "Only rotation about a single bond.",
      "Loss of the carbonyl oxygen with no intermediate.",
      "A mandatory free-radical chain."
    ],
    0,
    "Attack gives a tetrahedral intermediate; collapse restores the carbonyl and expels a leaving group.",
    "RCOY + Nu → RCONu + leaving group",
    "Applies to acyl derivatives with suitable leaving groups; compare acid chlorides, esters and amides under matched conditions. Reference: chapter 21 Summary, PDF p. 796 (printed p. 778)."
  ],
  [
    22,
    "Carbonyl Alpha-Substitution Reactions",
    "Why can an α hydrogen next to a carbonyl be removed more readily than a typical alkane hydrogen?",
    [
      "The resulting ion has no charge.",
      "The resulting enolate is resonance stabilized.",
      "All α carbons are aromatic.",
      "A carbonyl prevents all proton transfer."
    ],
    1,
    "The enolate distributes charge between the α carbon and oxygen through resonance.",
    "Carbonyl compound + strong base → enolate + conjugate acid",
    "Enolate formation requires an α hydrogen; kinetic/thermodynamic enolate selection depends on base, temperature and equilibration. Reference: chapter 22 Summary, PDF p. 831 (printed p. 813)."
  ],
  [
    23,
    "Carbonyl Condensation Reactions",
    "Before dehydration, what functional-group pattern does a simple aldol addition create?",
    [
      "An α-chloro ether.",
      "A nitrile with no oxygen.",
      "A β-hydroxy aldehyde or ketone.",
      "A saturated hydrocarbon."
    ],
    2,
    "An enolate attacks another carbonyl, producing an alcohol at the β position relative to the retained carbonyl.",
    "Aldol addition → β-hydroxy carbonyl; dehydration → α,β-unsaturated carbonyl",
    "Distinguish addition from condensation with water loss; aldol donors require suitable α hydrogens. Reference: chapter 23 Summary, PDF p. 866 (printed p. 848)."
  ],
  [
    24,
    "Amines and Heterocycles",
    "Why is aniline generally less basic than a simple alkylamine?",
    [
      "Aniline contains no nitrogen lone pair.",
      "All aromatic compounds are strong bases.",
      "Alkylamines cannot be protonated.",
      "Its nitrogen lone pair is delocalized into the aromatic ring."
    ],
    3,
    "Resonance lowers availability of the aniline lone pair for bonding to a proton.",
    "Amine + H⁺ ⇌ ammonium ion",
    "Compare in the same solvent; ring substituents and solvation also affect basicity. Reference: chapter 24 Summary, PDF p. 912 (printed p. 894)."
  ],
  [
    25,
    "Biomolecules: Carbohydrates",
    "How do the α and β anomers of a cyclic sugar differ?",
    [
      "In configuration at the anomeric carbon.",
      "In molecular formula.",
      "In the number of carbon atoms.",
      "In every stereocenter simultaneously."
    ],
    0,
    "Cyclization of the carbonyl creates an anomeric center; α and β forms differ at this new center.",
    "Open-chain sugar ⇌ cyclic hemiacetal (α or β)",
    "For aldoses forming hemiacetals; ketoses form hemiketals. Do not confuse α/β with D/L classification. Reference: chapter 25 Summary, PDF p. 956 (printed p. 938)."
  ],
  [
    26,
    "Biomolecules: Amino Acids, Peptides, and Proteins",
    "What linkage joins amino acid residues in a peptide?",
    [
      "A carbon–carbon triple bond.",
      "An amide bond.",
      "An ether bond between side chains.",
      "A glycosidic bond."
    ],
    1,
    "A peptide bond links the carboxyl-derived carbonyl of one residue to the amino nitrogen of another.",
    "Peptide linkage: C(=O)–N (amide)",
    "Sequences are conventionally read from N terminus to C terminus; primary structure specifies residue order. Reference: chapter 26 Summary, PDF p. 996 (printed p. 978)."
  ],
  [
    27,
    "Biomolecules: Lipids",
    "What is a triacylglycerol structurally?",
    [
      "Three glucose units linked by glycosidic bonds.",
      "A peptide with three amino acids.",
      "Glycerol esterified with three fatty acids.",
      "A nucleotide with three bases."
    ],
    2,
    "Each glycerol hydroxyl forms an ester with a fatty acid; the fatty acid chains may be saturated or unsaturated.",
    "Triacylglycerol hydrolysis → glycerol + fatty acids",
    "Basic hydrolysis (saponification) gives fatty-acid salts rather than neutral fatty acids until acid workup. Reference: chapter 27 Summary, PDF p. 1034 (printed p. 1016)."
  ],
  [
    28,
    "Biomolecules: Nucleic Acids",
    "What distinguishes a nucleotide from a nucleoside?",
    [
      "A nucleotide lacks a sugar.",
      "A nucleoside has three peptide bonds.",
      "Only nucleosides contain a base.",
      "A nucleotide includes a phosphate group."
    ],
    3,
    "A nucleoside contains a base and sugar; adding phosphate gives a nucleotide.",
    "Nucleoside = base + sugar; nucleotide = nucleoside + phosphate",
    "DNA uses 2-deoxyribose and RNA uses ribose; polymer backbones contain 3′–5′ phosphodiester links. Reference: chapter 28 Summary, PDF p. 1059 (printed p. 1041)."
  ],
  [
    29,
    "The Organic Chemistry of Metabolic Pathways",
    "In ordinary fatty-acid β oxidation, how many carbons are removed per repeating cycle?",
    [
      "Two carbons, released as acetyl-CoA.",
      "One carbon, released as methane.",
      "Three carbons, released as glucose.",
      "Six carbons, released as benzene."
    ],
    0,
    "Repeated oxidation and cleavage shorten the acyl chain by a two-carbon acetyl unit.",
    "β oxidation: acyl-CoA chain shortens by C₂ per cycle",
    "For the ordinary cycle; the final cleavage and odd-chain or unsaturated substrates need additional accounting or pathways. Reference: chapter 29 Summary, PDF p. 1110 (printed p. 1092)."
  ],
  [
    30,
    "Orbitals and Organic Chemistry: Pericyclic Reactions",
    "What best describes a pericyclic reaction?",
    [
      "A mechanism that always forms a free carbocation.",
      "A concerted reorganization through a cyclic transition state.",
      "A reaction requiring a long-lived radical intermediate.",
      "Any acid–base reaction in water."
    ],
    1,
    "Bond reorganization occurs in one step, with orbital symmetry governing allowed pathways and stereochemistry.",
    "Thermal 4π electrocyclic ring closure: conrotatory; thermal 6π: disrotatory",
    "For idealized electrocyclic closures; photochemical selection rules reverse these rotational modes. Reference: chapter 30 Summary, PDF p. 1137 (printed p. 1119)."
  ],
  [
    31,
    "Synthetic Polymers",
    "What is characteristic of an isotactic polymer?",
    [
      "Its substituents are placed randomly.",
      "Its stereochemical pattern alternates regularly.",
      "Its repeat-unit stereocenters follow the same stereochemical pattern.",
      "It contains no covalent backbone bonds."
    ],
    2,
    "Isotactic chains have a regular repeated arrangement; syndiotactic chains alternate and atactic chains are irregular.",
    "Isotactic = same pattern; syndiotactic = alternating; atactic = irregular",
    "Tacticity describes stereoregularity in suitable polymers; it is distinct from chain-growth versus step-growth mechanisms. Reference: chapter 31 Summary, PDF p. 1159 (printed p. 1141)."
  ]
];
