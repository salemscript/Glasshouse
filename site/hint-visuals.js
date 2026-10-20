/* Step-aware, original visual support for reviewed Glasshouse textbook exercises. */
'use strict';
window.HintVisuals = (() => {
  const C = {bg:'#101b25',grid:'#2b3946',ink:'#edf3f3',muted:'#acbdc6',blue:'#60d8d0',coral:'#ff7967',gold:'#ffd06e'};
  const esc = s => String(s ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const clamp = (x,a=0,b=1) => Math.min(b,Math.max(a,Number(x)||0));
  const n = x => Number(Number(x).toFixed(3));
  const fmt = (x,d=2) => Number(x).toFixed(d).replace(/\.0+$/,'');
  const text = (x,y,t,color=C.ink,size=18,anchor='start') => `<text x="${n(x)}" y="${n(y)}" fill="${color}" font-size="${size}" text-anchor="${anchor}">${esc(t)}</text>`;
  const line = (x1,y1,x2,y2,color=C.grid,w=2,extra='') => `<line x1="${n(x1)}" y1="${n(y1)}" x2="${n(x2)}" y2="${n(y2)}" stroke="${color}" stroke-width="${w}" ${extra}/>`;
  const dot = (x,y,color=C.blue,r=5) => `<circle cx="${n(x)}" cy="${n(y)}" r="${r}" fill="${color}"/>`;
  const arrow = (x1,y1,x2,y2,color='blue',w=4) => line(x1,y1,x2,y2,C[color],w,`marker-end="url(#hv-arrow-${color})"`);
  const phase = (title,equation,explanation,focus,start=0) => ({title,equation,explanation,focus,start});
  function svg(body,description) {
    return `<svg viewBox="0 0 800 440" role="img" aria-label="${esc(description)}" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Arial,sans-serif"><desc>${esc(description)}</desc><defs>${['blue','coral','gold'].map(c=>`<marker id="hv-arrow-${c}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="${C[c]}"/></marker>`).join('')}</defs><rect width="800" height="440" fill="${C.bg}"/>${body}</svg>`;
  }
  const exact = {
    'calculus-section-2-3-11': {
      frame:'removable-limit',title:'A hole does not stop a limit',
      parameter:{key:'gap',label:'Starting distance from x = 5',min:.05,max:2,step:.05,value:1,unit:''},sides:true,
      note:'Exact function from this exercise. Moving the point helps explain a limit; it does not change the problem.',
      phases:[
        phase('Factor the numerator','x² − 6x + 5 = (x − 5)(x − 1)','The highlighted numerator has the same x − 5 factor as the denominator. Factoring lets you identify what can cancel.',[556,107,213,84],0),
        phase('Keep the nearby graph','f(x) = x − 1, for x ≠ 5','Cancel only for x ≠ 5. The blue line shows the remaining nearby values; the gold hole marks the missing value at x = 5.',[250,164,147,147],.35),
        phase('Approach from both sides','limₓ→₅ f(x) = limₓ→₅ (x − 1)','Run the coral point toward the gold hole. Switch left and right: the approached height is the same even though the original quotient is undefined there.',[261,160,115,161],.8)
      ]
    },
    'calculus-section-2-3-18': {
      frame:'secant-slope',title:'Turn a difference quotient into a slope',
      parameter:{key:'h',label:'Starting horizontal change h',min:-1,max:1,step:.01,value:1,unit:''},
      note:'Exact cubic and difference quotient from this exercise. A zero-width secant is undefined; its limiting direction is a tangent.',
      phases:[
        phase('Find the vertical change','Δy = (2 + h)³ − 2³','The coral leg of the triangle is the change in the curve’s height. Expand the cube first so you can simplify that change.',[276,48,269,251],0),
        phase('Divide by the horizontal change','secant slope = Δy / h','The gold horizontal leg is h. The quotient compares the two changes; cancelling h is valid while h is nonzero.',[552,100,217,109],.45),
        phase('Let the secant become a tangent','limₕ→₀ Δy/h = f′(2)','Run or scrub toward the end. The two points meet while the line settles to a direction. That limiting direction is the requested slope.',[284,227,150,112],.8)
      ]
    },
    'calculus-section-3-9-33': {
      frame:'sliding-ladder',title:'Connect two rates with one rigid ladder',
      parameter:{key:'x',label:'Explore the bottom position x',min:1.8,max:4.5,step:.05,value:3,unit:'m'},
      note:'At the source instant, x = 3 m, x′ = +0.20 m/s and y′ = −0.15 m/s. Reset restores that instant. Playback explores later motion with x′ held constant.',
      phases:[
        phase('Choose the sign of the rate','dy/dt = −0.15 m/s','Upward is positive for the height y. The coral arrow points downward, so its rate is negative. The turquoise arrow marks increasing x.',[79,86,133,276],0),
        phase('Differentiate the constraint','x² + y² = L²  ⇒  x x′ + y y′ = 0','The gold ladder stays rigid. Differentiation links its two changing legs; substitute the source rates into this relationship to find y.',[554,74,225,104],0),
        phase('Recover the fixed length','L = √(x² + y²)','The gold hypotenuse is L. Once you know both legs at the same instant, use the right triangle to find the length. Reset before using the source numbers.',[140,88,285,281],0)
      ]
    },
    'calculus-section-6-1-13': {
      frame:'between-curves',title:'See where the area integral comes from',
      parameter:{key:'n',label:'Number of midpoint strips',min:4,max:48,step:2,value:12,unit:''},
      note:'Exact source parabolas. More strips improve the area approximation; they do not change the required exact area.',
      phases:[
        phase('Locate both intersection bounds','12 − x² = x² − 6','The two intersection dots mark where the curves exchange which one is on top. Solve this equality for both roots to set your integration bounds.',[110,160,395,79],0),
        phase('Build the strip height','height = (12 − x²) − (x² − 6)','The blue curve is the upper edge; the coral curve is the lower edge. The gold strip spans the difference. Subtract the whole lower expression.',[553,64,226,164],.4),
        phase('Add the thin strips','A = ∫ₐᵇ (upper − lower) dx','Scrub across the region. Each thin strip contributes height × width. The integral adds those contributions as the width approaches zero.',[92,89,434,239],.65),
        phase('Evaluate upper minus lower bound','A = F(b) − F(a),   F′(x) = upper − lower','The integral needs both end values of the antiderivative. Keep their signs when subtracting; the shaded region represents a positive area.',[95,103,431,204],.85)
      ]
    },
    'physics-chapter-02-problems-1': {
      frame:'constant-speed',title:'Connect speed, seconds, and distance',
      note:'Exact source speed and 0.50 s interval. Playback is slowed; the time readout shows actual model seconds.',
      phases:[
        phase('Make the units match','v(m/s) = v(km/h) × (1000 m / 1 km) × (1 h / 3600 s)','The source speed is in km/h, but the sneeze lasts seconds. Convert the speed first so the time units cancel correctly.',[75,57,247,65],0),
        phase('Multiply speed by elapsed time','Δx = v Δt','Run the car and watch the gold rectangle grow. Its height is speed and its width is time, so its area is the distance travelled.',[81,236,458,144],.5)
      ]
    },
    'physics-chapter-05-problems-1': {
      frame:'vector-forces',title:'Build the force before finding acceleration',
      note:'Exact source forces, angle, and mass. Playback adds vectors head to tail; it does not show the object’s path.',
      phases:[
        phase('Add the east–west components','Fₓ = 9.0 − 8.0 cos 62°','Turquoise points east. The coral force has a westward projection, so its x component is negative. Add signed components along the same axis.',[78,280,458,75],0),
        phase('Find the northward component','Fᵧ = 8.0 sin 62°','The coral force also points north, giving a positive y component. Run to slide this vector to the turquoise tip without changing its direction or length.',[221,110,274,207],.45),
        phase('Convert the resultant into acceleration','|Fnet| = √(Fₓ² + Fᵧ²),   a = |Fnet| / m','The gold arrow runs from the starting point to the final tip. Its length is the net force. Divide that magnitude by the mass to get acceleration.',[199,137,173,190],1)
      ]
    },
    'organic-2-16': {
      frame:'acid-log-scale',title:'Undo a base-ten logarithm',
      parameter:{key:'pka',label:'Explore a pKₐ value',min:1,max:14,step:.01,value:9.31,unit:''},
      note:'HCN has source pKₐ = 9.31, marked in gold. Other slider values are comparisons, not replacements for the source value.',
      phases:[
        phase('Keep the negative sign','pKₐ = −log₁₀(Kₐ)  ⇒  log₁₀(Kₐ) = −pKₐ','The line slopes down: increasing pKₐ makes Kₐ smaller. The minus sign reverses the direction of the relationship.',[555,68,230,100],0),
        phase('Choose the correct exponential base','Kₐ = 10^(−pKₐ)','A base-ten exponential undoes a base-ten logarithm. Run to see that one extra pKₐ unit makes Kₐ ten times smaller.',[112,79,414,284],.5),
        phase('Use the marked source value','Kₐ = 10^(−9.31)','Reset returns to the gold HCN marker. Evaluate the negative exponent with base ten; keep enough digits until the final rounding.',[348,229,130,108],0)
      ]
    },
    'organic-13-5': {
      frame:'nmr-field',title:'Link chemical shift to hertz separation',
      parameter:{key:'mhz',label:'Explore instrument frequency',min:200,max:500,step:10,value:200,unit:'MHz'},
      note:'Exact 2.1 ppm acetone signal and source 200 / 500 MHz comparison. This diagram compares axes; it is not a spin-dynamics simulation.',
      phases:[
        phase('Choose the instrument frequency','Δν(Hz) = δ(ppm) × ν₀(MHz)','The chemical-shift position is fixed on the blue ppm axis. The instrument frequency sets how many hertz correspond to each ppm.',[71,29,502,157],0),
        phase('Compare the two instruments','Δν₂ / Δν₁ = ν₀,₂ / ν₀,₁','Run toward the stronger instrument. The coral peak moves on the hertz axis while the blue peak stays fixed in ppm.',[68,212,507,179],.5),
        phase('Calculate each requested quantity','δ = Δν/ν₀;   Δν = δ ν₀','Use the instrument frequency stated in each part. A change in field changes the hertz separation; it does not change the molecule’s ppm position.',[74,66,491,296],.85)
      ]
    },
    'physics-chapter-12-problems-4': {
      custom:'bow',title:'Balance the two string tensions',
      parameter:{key:'angle',label:'Explore the included string angle φ',min:40,max:160,step:1,value:90,unit:'°'},
      note:'An ideal symmetric two-string force diagram, using the source condition F = T. Angle changes are exploration; this is not a string-motion simulation.',
      phases:[
        phase('Resolve the two tensions','F = 2T cos(φ/2)','Each gold string makes half the included angle with the direction opposite the pull. Its turquoise projection contributes to the same resultant.',[116,51,492,338],0),
        phase('Apply the source condition','F = T  ⇒  cos(φ/2) = 1/2','The perpendicular components cancel by symmetry. With F = T, the sum of the two along-pull components must equal one tension.',[181,190,450,105],.5),
        phase('Find the half-angle','φ/2 = arccos(1/2)','Use inverse cosine in degree mode. The component equation contains φ/2, so this operation returns half of the included angle.',[304,105,280,243],.7),
        phase('Return to the full angle','φ = 2 arccos(1/2)','The inverse cosine gives the half-angle, measured from the bisector. Double it to answer the question about the whole angle between the strings.',[304,105,280,243],1)
      ]
    },
    'physics-chapter-12-problems-16': {
      custom:'crate',title:'Use a tipping edge to simplify torque',
      parameter:{key:'height',label:'Explore the height of the push h',min:.1,max:.75,step:.005,value:.375,unit:'m'},
      note:'Exact 0.750 m cube, 500 N weight, and 350 N push. The picture shows moment balance at the tipping threshold; it does not simulate sliding or unknown friction.',
      phases:[
        phase('Locate the weight’s moment arm','weight arm = cube width / 2','The weight acts through the center of the uniform cube. Its perpendicular distance to the gold tipping edge is half of the cube width.',[153,174,296,190],0),
        phase('Calculate the restoring moment','τweight = W × (width / 2)','The coral weight tends to restore the cube. The turquoise push tends to tip it. About the edge, unknown edge contact forces have zero moment arm.',[327,190,178,191],.45),
        phase('Balance the moments at threshold','F h = W (width / 2)  ⇒  h = W width / (2F)','Move the height slider: the same force has more tipping effect higher up. At the threshold its moment equals the weight’s restoring moment. Solve for h.',[62,76,416,305],1)
      ]
    },
    'physics-chapter-12-problems-54': {
      custom:'ladder-torque',title:'Find the forces before the ladder’s distance',
      parameter:{key:'angle',label:'Explore ladder angle to the floor',min:30,max:80,step:1,value:55,unit:'°'},
      note:'Exact 5.0 m uniform ladder, 400 N weight, and μₛ = 0.46. The wall is frictionless. Exploring an angle shows the required forces; it is not a slipping-motion simulation.',
      phases:[
        phase('Balance the vertical forces','Nground − W = 0','The wall reaction is horizontal. The ground normal points up and the weight points down, so the normal equals the ladder’s weight.',[206,156,231,244],0),
        phase('Use friction at impending slip','fmax = μₛ Nground;   Rwall = fmax','At the limiting position, floor friction reaches μₛNground. Horizontal force balance makes its magnitude equal to the wall reaction.',[76,95,420,304],.4),
        phase('Take moments about the foot','Rwall y = W x / 2','The weight acts halfway along the ladder, with moment arm x/2. The wall reaction has arm y. Floor forces pass through the pivot and drop out.',[117,66,348,321],.8),
        phase('Combine torque with geometry','x/y = 2fmax/W;   x² + y² = L²','The force balance gives a distance-to-height ratio. The right triangle then turns that ratio into the requested foot distance x.',[135,80,310,296],1)
      ]
    }
  };
  const legacy = {'stewart-2-3-11':'calculus-section-2-3-11','stewart-2-3-18':'calculus-section-2-3-18','stewart-3-9-33':'calculus-section-3-9-33','stewart-6-1-13-area-portion':'calculus-section-6-1-13','halliday10-003':'physics-chapter-02-problems-1','halliday10-006':'physics-chapter-05-problems-1','mcmurry-13-5a':'organic-13-5','mcmurry-13-5c':'organic-13-5'};
  const formalPhases = [
    phase('Count bonds and lone-pair electrons','FC = V − N − B/2','Gold dots represent the neutral atom’s valence electrons. Coral dots are nonbonding electrons; each bond pair contributes two electrons to B.',[384,74,271,259],0),
    phase('Assign half of each bonding pair','assigned electrons = N + B/2','Run the bookkeeping: both electrons of each lone pair belong to the atom, while one electron from each bond pair is assigned to it. No bonds are being made or broken.',[345,113,348,228],.45),
    phase('Compare with the neutral atom','FC = neutral valence electrons − assigned electrons','Compare the gold neutral reference with the electrons assigned to this atom. A deficit gives a positive formal charge; an excess gives a negative charge.',[86,97,588,239],1)
  ];
  function formalData(q,p) {
    if(q?.id!=='organic-2-7'||!p?.verified)return null;
    const first=p.steps?.[0],rules=first?.blanks?.map(b=>b.rule?.answer)||[];
    if(!/group.valence|bonding electrons/i.test(first?.text||'')||rules.length<3)return null;
    const [valence,bonding,nonbonding]=rules.map(Number);
    if(![valence,bonding,nonbonding].every(Number.isInteger)||valence<1||valence>8||bonding<0||bonding>12||nonbonding<0||nonbonding>8||bonding%2||nonbonding%2)return null;
    const label=p.label||p.coach?.target||'Selected atom';
    const element=/oxygen/i.test(label)?'O':/nitrogen/i.test(label)?'N':/carbon/i.test(label)?'C':'atom';
    return {valence,bonding,nonbonding,element,label};
  }
  function sphereMode(p) {
    const rules=p.finalRules||[],unit=String(rules[0]?.unit||'').replace(/\s/g,'');
    if(/[³3]/.test(unit))return 'volume';
    if(/[²2]/.test(unit))return 'area';
    const scope=String(p.label||'')+' '+String(rules[0]?.selectionPrompt||rules[0]?.answerLabel||'');
    return /volume/i.test(scope)?'volume':/surface|area/i.test(scope)?'area':'circumference';
  }
  function sphereDescriptor(p) {
    const mode=sphereMode(p),definitions={
      circumference:phase('Go around the equator','C = 2πr','The gold equator is a circle of radius r. Run to trace one full trip around that circle; its length is the circumference. Use the converted radius in kilometers.',[116,152,301,116],0),
      area:phase('Cover the outside surface','A = 4πr²','Surface area covers the whole sphere, not just a circular slice. The turquoise surface spreads over the globe. A radius in kilometers gives area in square kilometers.',[111,78,311,312],0),
      volume:phase('Fill the interior','V = (4/3)πr³','Volume measures the three-dimensional interior. The gold interior appears inside the outer surface. A radius in kilometers gives volume in cubic kilometers.',[134,102,263,260],0)
    };
    return {id:'physics-chapter-01-problems-1',custom:'sphere',scopeMode:mode,title:'Earth as a sphere: radius to geometry',note:'Exact source radius: 6.37 × 10⁶ m. The sphere is shown in perspective and is not to scale. The highlighted formula follows the active part; the other formulas are reference relationships.',phases:[phase('Convert the radius before squaring or cubing','r(km) = r(m) ÷ (1000 m/km)','The arrow runs from the center to the surface: that is the radius, not the diameter. Convert meters to kilometers first so every later length, area, or volume has the requested units.',[256,202,168,57],0),definitions[mode]]};
  }
  function graphDescriptor(q,p) {
    if(p.coach?.family!=='function-values'||!/\bgraphs?\b|\bplotted\b/i.test(String(q.prompt||'')+' '+String(p.method||'')))return null;
    return {id:'graph-reading-schematic',custom:'graph-reading',schematic:true,title:'Read a graph: input → curve → output',parameter:{key:'input',label:'Move the illustrative input',min:.1,max:.9,step:.01,value:.55,unit:'',display:'Illustrative position'},note:'SCHEMATIC ONLY. This curve and its positions are invented to explain graph reading. Use the actual textbook graph above for every numerical value and for its domain, holes, and endpoints.',phases:[
      phase('Locate the input','a = the input on the horizontal axis','Start at the requested input on the actual textbook graph. This schematic has no numerical scale; the gold a only shows where an input belongs.',[105,318,452,61],0),
      phase('Move to the actual curve','(a, f(a)) = a point on the graph','Draw a vertical line from the input until it meets the correct curve. The turquoise point shows that input-output pair. Check the actual graph’s filled or open point if one is shown.',[118,77,436,243],.5),
      phase('Project to the output axis','f(a) = the height of the curve at input a','Trace horizontally from that curve point to the output axis. Read the height using the ticks on the actual textbook graph above. No values can be read from this illustrative drawing.',[73,77,475,250],1)
    ]};
  }
  function descriptor(q,p) {
    if(!p?.verified||!p.steps?.length)return null;
    if(q?.id==='physics-chapter-01-problems-1')return sphereDescriptor(p);
    const id=legacy[q?.id]||q?.id,m=exact[id];
    if(m&&(!m.frame||window.LearningVisuals?.has(m.frame)))return {...m,id};
    const graph=graphDescriptor(q,p);if(graph)return graph;
    const d=formalData(q,p);
    return d?{id:'organic-2-7',custom:'formal',title:'Assign electrons to the selected atom',data:d,phases:formalPhases,note:'Electron bookkeeping for '+d.label+'. Bond pairs are shown separately, so a double or triple bond contributes more than one pair. This is electron bookkeeping, not a full molecular structure or an electron-transfer mechanism.'}:null;
  }
  function defaults(m){return m.parameter?{[m.parameter.key]:m.parameter.value,side:1}:{side:1};}
  function selectedPhase(m,index,p) {
    const i=Math.max(0,Math.floor(Number(index)||0)),step=p?.steps?.[i],last=m.phases.length-1;
    if(step?.final||step&&i===p.steps.length-1)return m.phases[last];
    const value=String(step?.title||'')+' '+String(step?.text||''),key=m.frame||m.custom;
    const patterns={
      'removable-limit':[[1,/nearby|cancel|quotient equals|simplif/i],[0,/factor|numerator|x²|x\^2/i]],
      'secant-slope':[[1,/after dividing|divid|cancel|simplif|quotient/i],[0,/expand|numerator|cube|³|\^3/i]],
      'sliding-ladder':[[1,/height y|height|constraint|differentiat|3\s*\(0\.2\)/i],[0,/dy\/dt|upward|negative|sign/i],[2,/length|hypotenuse|Pythagor/i]],
      'between-curves':[[0,/intersection|bound.*root|x=.*and x/i],[1,/upper minus lower|strip height|integrand|subtract.*curve/i],[3,/antiderivative|upper bound|F\(.*\)/i],[2,/integrat|thin strip|midpoint|area sum/i]],
      'constant-speed':[[0,/km\/h|convert|unit|m\/s/i],[1,/distance|elapsed|duration|displacement/i]],
      'vector-forces':[[0,/Fₓ|F_x|F[xX]|east|west/i],[1,/Fᵧ|F_y|F[yY]|north|vertical/i],[2,/magnitude|acceleration|resultant/i]],
      'acid-log-scale':[[0,/exponent|negative|minus sign/i],[1,/base|logarithm|ten/i],[2,/evaluate|recover|calculate.*K/i]],
      'nmr-field':[[1,/ratio|new.to.old|compare/i],[0,/first|frequency|instrument/i],[2,/ppm|chemical shift|hertz calculation/i]],
      'bow':[[3,/full angle|multiplying by two|2 ×/i],[2,/inverse cosine|arccos|degree mode/i],[0,/Force balance|two.*component/i],[1,/condition|F = T/i]],
      'crate':[[0,/center|centre|horizontally|width|arm/i],[1,/restoring|weight produces|500 N/i],[2,/height|threshold|350h/i]],
      'ladder-torque':[[3,/geometry|x²|5\.0 ×/i],[2,/moments|x\/y|R_wall y|Rwall y/i],[1,/friction|μ|f_max|fmax/i],[0,/vertical|normal|N_ground|Nground/i]],
      'sphere':[[0,/convert|kilometers|kilometres|radius.*in.*km/i],[1,/circumference|surface|volume|radius.*squared|radius.*cubed/i]],
      'graph-reading':[[2,/output|height|horizontal.*line|read.*value/i],[1,/curve|vertical.*line|intersection/i],[0,/input|horizontal.*axis/i]],
      'formal':[[1,/assigned|assign|half/i],[0,/count|group.valence|bonding electrons/i],[2,/Formal charge|neutral.*assigned/i]]
    };
    const matched=(patterns[key]||[]).find(([,rule])=>rule.test(value));
    return m.phases[matched?matched[0]:Math.min(last,i)];
  }
  function cornerFocus(s,p) {
    if(!p?.focus)return s;
    const [x,y,w,h]=p.focus,l=18,points=[`M${x+l} ${y}H${x}V${y+l}`,`M${x+w-l} ${y}H${x+w}V${y+l}`,`M${x} ${y+h-l}V${y+h}H${x+l}`,`M${x+w-l} ${y+h}H${x+w}V${y+h-l}`].join(' ');
    return s.replace('</svg>',`<path data-hv-focus="true" d="${points}" stroke="${C.gold}" stroke-width="3" stroke-linecap="round" fill="none" opacity=".85"/></svg>`);
  }
  function bow(u,p) {
    const angle=p.angle*Math.PI/180,half=angle/2,O={x:424,y:235},r=172,tx=O.x-r*Math.cos(half),dy=r*Math.sin(half),shift=clamp(u*1.8),fx=2*Math.cos(half);
    let b=line(87,O.y,676,O.y,C.grid,2,'stroke-dasharray="5 6"')+line(O.x,O.y,tx,O.y-dy,C.gold,5)+line(O.x,O.y,tx,O.y+dy,C.gold,5);
    b+=arrow(O.x,O.y,tx,O.y-dy,'blue',4)+arrow(O.x,O.y,tx,O.y+dy,'blue',4)+arrow(O.x,O.y,O.x+150,O.y,'coral',5);
    b+=line(tx,O.y-dy,tx,O.y,C.muted,1,'stroke-dasharray="5 6"')+line(tx,O.y+dy,tx,O.y,C.muted,1,'stroke-dasharray="5 6"');
    if(shift>0)b+=arrow(O.x,O.y-18,O.x-r*Math.cos(half)*shift,O.y-18,'gold',3)+arrow(O.x,O.y+18,O.x-r*Math.cos(half)*shift,O.y+18,'gold',3);
    const arcR=58,ax=O.x-arcR*Math.cos(half),ay=arcR*Math.sin(half);
    b+=`<path d="M${n(ax)},${n(O.y-ay)} A58 58 0 0 0 ${n(ax)},${n(O.y+ay)}" stroke="${C.gold}" fill="none" stroke-width="2"/>`;
    b+=dot(O.x,O.y,C.ink,7)+text((O.x+tx)/2-10,O.y-dy/2-12,'T',C.blue,23)+text((O.x+tx)/2-10,O.y+dy/2+22,'T',C.blue,23)+text(O.x+96,O.y-20,'F (pull)',C.coral,20)+text(O.x-93,O.y-8,'φ/2',C.gold,18)+text(O.x-93,O.y+29,'φ/2',C.gold,18);
    b+=text(91,50,'Two tensions, one resultant',C.ink,23)+text(91,89,'Perpendicular components cancel.',C.muted,17)+text(94,425,'Along the bisector: F = T cos(φ/2) + T cos(φ/2)',C.gold,20);
    return {svg:svg(b,'Symmetric two-string tension diagram. Each string makes half the included angle with the force bisector.'),readouts:[['Exploration angle φ',fmt(p.angle,0)+'°'],['Each projection','T cos(φ/2)'],['Source condition','F = T']],values:{angle:p.angle,resultantOverTension:fx}};
  }
  function crate(u,p) {
    const s=270,x=164,y=89,pivot={x:x+s,y:y+s},h=p.height/.75*s,mid={x:x+s/2,y:y+s/2},pushY=pivot.y-h,weight=500,force=350,width=.75,tip=force*p.height,restore=weight*width/2,amount=.25+.75*u;
    let b=`<rect x="${x}" y="${y}" width="${s}" height="${s}" rx="5" fill="${C.blue}" fill-opacity=".07" stroke="${C.blue}" stroke-width="3"/>`;
    b+=line(75,pivot.y,578,pivot.y,C.muted,4)+dot(pivot.x,pivot.y,C.gold,8)+text(pivot.x+15,pivot.y+24,'pivot',C.gold,18);
    b+=arrow(57,pushY,148,pushY,'blue',5)+arrow(mid.x,mid.y,mid.x,mid.y+89,'coral',5)+dot(mid.x,mid.y,C.coral,6);
    b+=text(51,pushY-17,'350 N',C.blue,20)+text(mid.x+15,mid.y+80,'500 N',C.coral,20);
    b+=line(pivot.x+30,pushY,pivot.x+30,pivot.y,C.blue,2)+line(pivot.x+22,pushY,pivot.x+38,pushY,C.blue,2)+line(pivot.x+22,pivot.y,pivot.x+38,pivot.y,C.blue,2)+text(pivot.x+42,pushY+(pivot.y-pushY)/2,'h',C.blue,24);
    b+=line(mid.x,pivot.y+38,pivot.x,pivot.y+38,C.coral,2)+text((mid.x+pivot.x)/2,pivot.y+63,'width / 2',C.coral,17,'middle');
    b+=text(580,82,'Moment comparison',C.ink,19)+text(580,116,'Tipping: Fh',C.blue,18)+text(580,151,'Restoring: Ww/2',C.coral,17);
    b+=`<rect x="580" y="198" width="${n(170*tip/(force*width)*amount)}" height="18" rx="4" fill="${C.blue}"/><rect x="580" y="245" width="${n(170*restore/(force*width)*amount)}" height="18" rx="4" fill="${C.coral}"/>`;
    b+=text(580,295,'Same force,',C.muted,18)+text(580,323,'different lever arm.',C.muted,18)+text(169,60,'Cube width = 0.750 m',C.ink,20);
    return {svg:svg(b,'A 0.750 metre cube with a 350 newton horizontal push at height h, a 500 newton weight through its centre, and a pivot at its lower right edge.'),readouts:[['Exploration height',fmt(p.height,3)+' m'],['Weight arm','width / 2'],['Threshold equation','Fh = Ww/2']],values:{height:p.height,tippingMoment:tip,restoringMoment:restore,width}};
  }
  function ladderTorque(u,p) {
    const theta=p.angle*Math.PI/180,L=5,W=400,mu=.46,x=L*Math.cos(theta),y=L*Math.sin(theta),R=W*x/(2*y),scale=62,foot={x:148+x*scale,y:355},top={x:148,y:355-y*scale},mid={x:(foot.x+top.x)/2,y:(foot.y+top.y)/2};
    let b=line(148,41,148,356,C.muted,6)+line(93,355,548,355,C.muted,6)+line(top.x,top.y,foot.x,foot.y,C.gold,8);
    b+=arrow(top.x,top.y,top.x+74,top.y,'blue',4)+arrow(foot.x,foot.y,foot.x,foot.y-81,'blue',4)+arrow(foot.x,foot.y+25,foot.x-73,foot.y+25,'coral',4)+arrow(mid.x,mid.y,mid.x,mid.y+78,'coral',4);
    b+=dot(foot.x,foot.y,C.ink,6)+text(top.x+83,top.y+7,'Rwall',C.blue,18)+text(foot.x+15,foot.y-59,'Nground',C.blue,17)+text(foot.x-37,foot.y+53,'friction',C.coral,17,'middle')+text(mid.x+14,mid.y-12,'W = 400 N',C.coral,17);
    b+=line(148,395,foot.x,395,C.gold,2)+text((148+foot.x)/2,420,'x',C.gold,22,'middle')+line(110,top.y,110,355,C.gold,2)+text(93,(top.y+355)/2,'y',C.gold,22,'middle');
    b+=text(577,83,'L = 5.0 m',C.ink,21)+text(577,127,'μₛ = 0.46',C.ink,21)+text(577,191,'About the foot:',C.muted,18)+text(577,225,'Rwall y = W x/2',C.gold,19)+text(577,287,'Floor forces have',C.muted,17)+text(577,315,'zero moment arm.',C.muted,17);
    const radius=42,end=-theta*clamp(u),cx=foot.x,cy=foot.y;
    if(u>0)b+=`<path d="M${n(cx-radius)} ${cy} A${radius} ${radius} 0 0 1 ${n(cx-radius*Math.cos(end))} ${n(cy-radius*Math.sin(-end))}" stroke="${C.gold}" fill="none" stroke-width="2"/>`;
    return {svg:svg(b,'Uniform ladder against a frictionless wall, showing the weight, ground normal, floor friction, wall reaction, and perpendicular torque arms x and y.'),readouts:[['Exploration angle',fmt(p.angle,0)+'°'],['Vertical balance','Nground = W'],['Limiting condition','f = μₛNground']],values:{x,y,lengthSquared:x*x+y*y,wallReaction:R,maxFriction:mu*W}};
  }
  function formal(u,p,d) {
    const neutral={x:190,y:207},centre={x:497,y:207},radius=80,pairs=d.bonding/2,lonePairs=d.nonbonding/2;
    let b=text(76,48,'Neutral-atom reference',C.gold,21)+text(411,48,'Selected atom’s neighborhood',C.ink,21);
    b+=`<circle cx="${neutral.x}" cy="${neutral.y}" r="35" fill="${C.gold}" fill-opacity=".1" stroke="${C.gold}" stroke-width="2"/><circle cx="${centre.x}" cy="${centre.y}" r="35" fill="${C.blue}" fill-opacity=".1" stroke="${C.blue}" stroke-width="2"/>`;
    b+=text(neutral.x,neutral.y+8,d.element,C.gold,26,'middle')+text(centre.x,centre.y+8,d.element,C.ink,26,'middle');
    for(let i=0;i<d.valence;i++){const a=-Math.PI/2+i*2*Math.PI/d.valence;b+=dot(neutral.x+radius*Math.cos(a),neutral.y+radius*Math.sin(a),C.gold,6);}
    for(let i=0;i<pairs;i++){
      const a=-Math.PI/2+i*2*Math.PI/Math.max(1,pairs),dx=Math.cos(a),dy=Math.sin(a),edge={x:centre.x+112*dx,y:centre.y+112*dy},near={x:centre.x+54*dx,y:centre.y+54*dy};
      b+=line(centre.x+38*dx,centre.y+38*dy,edge.x,edge.y,C.muted,3)+`<circle cx="${n(edge.x)}" cy="${n(edge.y)}" r="13" fill="${C.bg}" stroke="${C.muted}" stroke-width="2"/>`;
      const offset=5,move=clamp(u)*19;b+=dot(centre.x+(73-move)*dx-offset*dy,centre.y+(73-move)*dy+offset*dx,C.blue,5)+dot(centre.x+73*dx+offset*dy,centre.y+73*dy-offset*dx,C.muted,5);
    }
    for(let i=0;i<lonePairs;i++){const a=Math.PI/4+i*2*Math.PI/Math.max(1,lonePairs),dx=Math.cos(a),dy=Math.sin(a),r=46;b+=dot(centre.x+r*dx-5*dy,centre.y+r*dy+5*dx,C.coral,5)+dot(centre.x+r*dx+5*dy,centre.y+r*dy-5*dx,C.coral,5);}
    b+=text(190,331,'V: valence electrons',C.gold,18,'middle')+text(497,347,'N: lone pairs · B: bonding electrons',C.muted,16,'middle');
    b+=text(109,393,'FC = V − [N + B/2]',C.ink,24)+text(457,396,'Assign one electron per bond pair.',C.blue,17);
    return {svg:svg(b,'Electron bookkeeping for '+d.label+'. Neutral valence electrons are gold, nonbonding electrons are coral, and each bonding pair contains one turquoise electron assigned to the selected atom.'),readouts:[['Gold','Neutral valence reference'],['Coral','Both lone-pair electrons count'],['Turquoise','Half of bonding electrons count']],values:{valence:d.valence,bonding:d.bonding,nonbonding:d.nonbonding,assigned:d.nonbonding+d.bonding/2,formalCharge:d.valence-d.nonbonding-d.bonding/2}};
  }
  function sphere(u,p,mode) {
    const cx=265,cy=228,r=145,ry=43,theta=-Math.PI/2+2*Math.PI*u,px=cx+r*Math.cos(theta),py=cy+ry*Math.sin(theta),radius=6.37e6;
    let b=`<defs><radialGradient id="hv-sphere-shade" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#244c58"/><stop offset="1" stop-color="#111f2d"/></radialGradient><clipPath id="hv-sphere-clip"><circle cx="${cx}" cy="${cy}" r="${r}"/></clipPath></defs>`;
    b+=`<circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#hv-sphere-shade)" stroke="${C.blue}" stroke-width="2.5"/>`;
    if(mode==='area')b+=`<circle cx="${cx}" cy="${cy}" r="${r}" fill="${C.blue}" fill-opacity="${n(.07+.24*u)}"/>`;
    if(mode==='volume')b+=`<circle cx="${cx}" cy="${cy}" r="${r*.7}" fill="${C.gold}" fill-opacity="${n(.04+.23*u)}" stroke="${C.gold}" stroke-opacity=".4" stroke-width="1.5"/>`;
    b+=`<g clip-path="url(#hv-sphere-clip)" stroke="${C.grid}" stroke-width="1.5" fill="none"><ellipse cx="${cx}" cy="${cy}" rx="67" ry="${r}"/><ellipse cx="${cx}" cy="${cy}" rx="117" ry="${r}"/><ellipse cx="${cx}" cy="${cy-68}" rx="133" ry="31"/><ellipse cx="${cx}" cy="${cy+68}" rx="133" ry="31"/></g>`;
    b+=`<ellipse cx="${cx}" cy="${cy}" rx="${r}" ry="${ry}" fill="none" stroke="${mode==='circumference'?C.gold:C.muted}" stroke-width="2" stroke-opacity=".6"/>`;
    if(mode==='circumference'&&u>0){let d='';for(let i=0;i<=100;i++){const a=-Math.PI/2+2*Math.PI*u*i/100;d+=(i?'L':'M')+n(cx+r*Math.cos(a))+','+n(cy+ry*Math.sin(a));}b+=`<path d="${d}" fill="none" stroke="${C.gold}" stroke-width="4"/>`+dot(px,py,C.gold,6);}
    b+=arrow(cx,cy,cx+r,cy,'blue',3)+dot(cx,cy,C.ink,4)+text(cx+r/2,cy-13,'r',C.blue,24,'middle');
    b+=text(120,51,'Source radius: 6.37 × 10⁶ m',C.ink,23)+text(121,411,'Perspective sphere · not to scale',C.muted,16);
    const formulas=[['circumference','C = 2πr','Around the equator'],['area','A = 4πr²','Outside surface'],['volume','V = (4/3)πr³','Interior volume']];
    for(let i=0;i<formulas.length;i++){const [kind,equation,label]=formulas[i],y=111+i*104,color=kind===mode?C.gold:C.muted;b+=text(489,y,label,color,17)+text(489,y+36,equation,color,26);if(kind===mode)b+=line(488,y+49,731,y+49,C.gold,2);}
    return {svg:svg(b,'Perspective sphere with source radius 6.37 times ten to the sixth metres, an equatorial circumference, surface, and interior. The '+mode+' relationship is highlighted.'),readouts:[['Source radius','6.37 × 10⁶ m'],['Active geometry',mode==='area'?'Surface area':mode==='volume'?'Interior volume':'Equatorial circumference'],['Unit conversion','1000 m = 1 km']],values:{radiusMeters:radius,radiusKilometers:radius/1000,circumferenceKm:2*Math.PI*radius/1000,areaKm2:4*Math.PI*(radius/1000)**2,volumeKm3:4*Math.PI*(radius/1000)**3/3}};
  }
  function graphReading(u,p) {
    const x0=110,y0=335,xFor=t=>140+400*t,yFor=t=>275-140*Math.sin(Math.PI*t)+50*t,a=p.input,x=xFor(a),y=yFor(a),up=clamp((u-.1)/.5),across=clamp((u-.6)/.4);
    let d='';for(let i=0;i<=100;i++){const t=i/100;d+=(i?'L':'M')+n(xFor(t))+','+n(yFor(t));}
    let b=line(x0,62,x0,y0,C.muted,2)+line(x0,y0,568,y0,C.muted,2)+`<path d="${d}" fill="none" stroke="${C.blue}" stroke-width="4"/>`;
    b+=dot(x,y0,C.gold,6)+text(x,y0+31,'a',C.gold,24,'middle');
    if(up>0)b+=line(x,y0,x,y0+(y-y0)*up,C.gold,2,'stroke-dasharray="6 5"');
    if(up>=1)b+=dot(x,y,C.blue,7)+text(x+14,y-17,'(a, f(a))',C.blue,19);
    if(across>0)b+=line(x,y,x+(x0-x)*across,y,C.coral,2,'stroke-dasharray="6 5"');
    if(across>=1)b+=dot(x0,y,C.coral,6)+text(x0-15,y+7,'f(a)',C.coral,22,'end');
    b+=text(83,43,'output',C.coral,18)+text(575,343,'input',C.gold,18)+text(600,116,'Input a',C.gold,22)+text(600,181,'Curve point',C.blue,21)+text(600,246,'Output f(a)',C.coral,22);
    b+=text(141,415,'SCHEMATIC · read values from the textbook graph above',C.muted,17);
    return {svg:svg(b,'A schematic curve with no numerical axis scale. An input on the horizontal axis projects vertically to the curve and horizontally to the output axis. Use the actual textbook graph for values.'),readouts:[['Gold','Locate the requested input'],['Turquoise','Meet the actual curve'],['Coral','Read the output height']],values:{inputPosition:a,projectionProgress:u}};
  }
  function finalValue(p){return p?.finalRules?.map(r=>`${r.label&&r.label!=='answer'?r.label+': ':''}${r.answer}${r.unit?' '+r.unit:''}`).join(' · ')||'';}
  function frameFor(m,p,index,u,params,finished) {
    let f=m.frame?window.LearningVisuals.frame(m.frame,u,params,false):m.custom==='bow'?bow(u,params):m.custom==='crate'?crate(u,params):m.custom==='ladder-torque'?ladderTorque(u,params):m.custom==='sphere'?sphere(u,params,m.scopeMode):m.custom==='graph-reading'?graphReading(u,params):formal(u,params,m.data);
    if(!f)return null;
    const readouts=f.readouts.filter(([,value])=>!/Complete.*guided/i.test(String(value)));
    const result=finalValue(p);
    if(result&&!m.schematic)readouts.push([finished?'Checked result':'Your result',finished?result:'Complete the guided blanks to reveal']);
    const clean=f.svg.replace(/lv-/g,'hv-lv-');
    return {...f,svg:cornerFocus(clean,selectedPhase(m,index,p)),readouts};
  }
  let active=null,animation=null,lastTime=null;
  const reduced = () => typeof matchMedia==='function'&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function readoutHTML(f){return f.readouts.map(([label,value])=>`<div><span>${esc(label)}</span><b>${esc(value)}</b></div>`).join('');}
  function html(q,p,index=0,finished=false) {
    const m=descriptor(q,p);if(!m)return '';
    const ph=selectedPhase(m,index,p),f=frameFor(m,p,index,ph.start,defaults(m),finished);if(!f)return '';
    return `<aside class="hint-visual" aria-live="off" data-hv-question="${esc(q.id)}" aria-label="Visual explanation for this guided step"><div class="hv-heading"><span class="hv-eyebrow">SEE THIS STEP</span>${m.schematic?'<span class="hv-schematic-label">SCHEMATIC · METHOD ONLY</span>':''}<h4>${esc(m.title)}</h4><span class="hv-step-label">${finished?'Walkthrough complete':'Step '+(Number(index)+1)} · ${esc(ph.title)}</span></div><div class="hv-connection">${m.schematic?'<p class="hv-schematic-instruction"><b>Use the actual textbook graph above for values.</b> This drawing explains the method and has no numerical scale.</p>':''}<span class="hv-equation-label">The equation and the picture</span><div class="hv-equation">${esc(ph.equation)}</div><p>${esc(ph.explanation)}</p></div><div class="hv-stage" id="hv-stage">${f.svg}</div><div class="hv-controls"><div class="hv-playback"><button type="button" class="btn" id="hv-run" aria-pressed="false">${reduced()?'Advance frame':'Run ▶'}</button><button type="button" class="btn light" id="hv-reset">Reset ↺</button><label for="hv-scrub">Explore the construction</label><input type="range" id="hv-scrub" min="0" max="1000" step="1" value="${Math.round(ph.start*1000)}" aria-valuetext="${Math.round(ph.start*100)} percent"></div>${m.parameter?`<div class="hv-parameter"><label for="hv-parameter">${esc(m.parameter.label)} <output id="hv-parameter-value">${esc(m.parameter.display||m.parameter.value)} ${esc(m.parameter.unit)}</output></label><input type="range" id="hv-parameter" min="${m.parameter.min}" max="${m.parameter.max}" step="${m.parameter.step}" value="${m.parameter.value}"></div>`:''}${m.sides?'<div class="hv-sides"><span>Approach from</span><button type="button" class="btn light" data-hv-side="-1" aria-pressed="false">Left</button><button type="button" class="btn light" data-hv-side="1" aria-pressed="true">Right</button></div>':''}</div><div class="hv-readouts" id="hv-readouts" aria-live="off">${readoutHTML(f)}</div><p class="hv-note">${esc(m.note)}${reduced()?' Reduced motion is enabled. Run advances one frame at a time.':''}</p></aside>`;
  }
  function paint(){
    if(!active)return;
    const f=frameFor(active.model,active.plan,active.stepIndex,active.progress,active.params,active.finished),stage=document.querySelector('#hv-stage');if(!f||!stage)return;
    stage.innerHTML=f.svg;
    const readouts=document.querySelector('#hv-readouts');if(readouts)readouts.innerHTML=readoutHTML(f);
    const scrub=document.querySelector('#hv-scrub');if(scrub){scrub.value=String(Math.round(active.progress*1000));scrub.setAttribute('aria-valuetext',Math.round(active.progress*100)+' percent');}
    const run=document.querySelector('#hv-run');if(run){run.textContent=reduced()?'Advance frame':active.running?'Pause Ⅱ':active.progress>=1?'Run again ▶':'Run ▶';run.setAttribute('aria-pressed',String(active.running));}
    const param=active.model.parameter;
    if(param){const range=document.querySelector('#hv-parameter'),out=document.querySelector('#hv-parameter-value');if(range)range.value=String(active.params[param.key]);if(out)out.textContent=param.display||fmt(active.params[param.key],param.step<1?3:0)+' '+param.unit;}
    for(const side of [-1,1]){const button=document.querySelector(`[data-hv-side="${side}"]`);if(button)button.setAttribute('aria-pressed',String(active.params.side===side));}
  }
  function stop(){if(animation!==null){cancelAnimationFrame(animation);animation=null;}if(active)active.running=false;lastTime=null;}
  function unmount(){stop();active=null;}
  function mount(q,p,index=0,finished=false){
    unmount();const m=descriptor(q,p),node=document.querySelector('.hint-visual');
    if(!m||!node||node.dataset.hvQuestion!==String(q?.id))return false;
    active={question:q.id,model:m,plan:p,stepIndex:Math.max(0,Math.floor(Number(index)||0)),finished:Boolean(finished),progress:selectedPhase(m,index,p).start,params:defaults(m),running:false};paint();return true;
  }
  function tick(time){animation=null;if(!active?.running)return;const delta=lastTime===null?0:Math.min(150,Math.max(0,time-lastTime));lastTime=time;active.progress=clamp(active.progress+delta/6500);if(active.progress>=1){active.running=false;lastTime=null;}paint();if(active?.running)animation=requestAnimationFrame(tick);}
  function run(){
    if(!active)return;
    if(reduced()){stop();active.progress=active.progress>=1?0:clamp(active.progress+.25);paint();return;}
    if(active.running){stop();paint();return;}
    if(active.progress>=1)active.progress=0;active.running=true;lastTime=null;animation=requestAnimationFrame(tick);paint();
  }
  function reset(){if(!active)return;stop();active.params=defaults(active.model);active.progress=selectedPhase(active.model,active.stepIndex,active.plan).start;paint();}
  document.addEventListener('click',e=>{
    const b=e.target.closest('button');if(!active||!b)return;
    if(b.id==='hv-run')run();else if(b.id==='hv-reset')reset();else if(b.dataset.hvSide){stop();active.params.side=Number(b.dataset.hvSide)<0?-1:1;active.progress=0;paint();}
  });
  document.addEventListener('input',e=>{
    if(!active)return;
    if(e.target.id==='hv-scrub'){stop();active.progress=clamp(Number(e.target.value)/1000);paint();}
    else if(e.target.id==='hv-parameter'){const p=active.model.parameter;if(!p)return;stop();active.params[p.key]=clamp(e.target.value,p.min,p.max);active.progress=selectedPhase(active.model,active.stepIndex,active.plan).start;paint();}
  });
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&active?.running){stop();paint();}});
  return {html,mount,unmount,
    has:(q,p)=>Boolean(descriptor(q,p)),
    state:()=>active?{question:active.question,model:active.model.frame||active.model.custom,stepIndex:active.stepIndex,progress:active.progress,params:{...active.params},running:active.running,finished:active.finished}:null,
    describe:(q,p)=>{const m=descriptor(q,p);return m?{id:m.frame||m.custom,title:m.title,phases:m.phases.map(ph=>({title:ph.title,equation:ph.equation,explanation:ph.explanation})),note:m.note}:null;},
    frame:(q,p,index=0,progress=0,params={},finished=false)=>{const m=descriptor(q,p);return m?frameFor(m,p,index,clamp(progress),{...defaults(m),...params},Boolean(finished)):null;}
  };
})();
