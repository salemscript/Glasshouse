"""Create explicit question-to-illustration records. No chapter-only fallback.
Renderers show a named object or process in the prompt, not an inferred solution.
"""
import gzip,json,re,pathlib,collections,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
qs=json.load(gzip.open(ROOT/'site/questions/physics.json.gz'))
old=json.loads((ROOT/'site/physics-loop-map.js').read_text().split('=',1)[1].rstrip(';\n'))
curated={k:v for k,v in old.items() if isinstance(v,str)}
rules=[]
def rule(kind,pattern,chapters=None,score=3):rules.append((kind,re.compile(pattern,re.I),chapters,score))
# Named apparatus first. A stationary object is drawn with a tracing highlight,
# never made to move merely because the chapter concerns mechanics.
rule('shaver',r'shaver|razor',score=8)
rule('stadium',r'human wave|spectators.*stand',score=8)
rule('telescope',r'telescope|astronomical instrument',score=7)
rule('microscope',r'microscope',score=7)
rule('camera',r'camera|photographic film',score=6)
rule('eye',r'near point|far point|nearsighted|farsighted|eyeglass|human eye',score=6)
rule('laser',r'\blaser\b',score=6)
rule('prism',r'\bprism\b',score=6)
rule('grating',r'\bgrating|rulings',score=6)
rule('double-slit',r'two.slit|double.slit|slit separation|slits',score=6)
rule('single-slit',r'single.slit|a slit|the slit|slit width',score=5)
rule('thin-film',r'thin.{0,12}(film|layer)|soap|coating|coat flat glass|wedge.shaped film',list(range(33,37)),6)
rule('lens',r'\blens|lenses',list(range(33,37)),5)
rule('mirror',r'\bmirror',list(range(33,37)),5)
rule('refraction',r'refract|Brewster|critical angle|index of refraction',list(range(33,37)),4)
rule('polarizer',r'polariz',list(range(33,37)),6)
rule('photoelectric',r'work function|photoelectric|electrons.{0,35}eject|electrons.{0,35}emit', [38],6)
rule('tunnel',r'tunnel|potential.{0,8}barrier', [38,39,40],6)
rule('quantum-well',r'potential well|infinite.{0,12}well|corral|box|confined', [38,39],6)
rule('orbital',r'hydrogen atom|hydrogen-atom|electron.{0,25}atom|quantum numbers|quantum number|atomic number|Pauli|electron configuration|orbital', [38,39,40],4)
rule('levels',r'energy.level|transition|excited state|ground state|absorption spectrum|line spectrum', [38,39,40],4)
rule('spin',r'Bohr magneton|magnetic moment|magnetic dipole|spin|angular momentum|semiclassical', [32,40],5)
rule('bands',r'semiconductor|conduction band|valence band|band gap|gap|highest occupied band|silicon|germanium', [41],5)
rule('fermi',r'Fermi|conduction electrons|occupancy|occupation|monovalent|density of states|free.electron', [41],4)
rule('junction',r'junction|diode|\bp[–−-]n\b|doping|donor|acceptor', [41],6)
rule('decay',r'half.life|decay|radioactiv|activity|Bq|curie|\bCi\b', [37,42,43,44],5)
rule('fission',r'fission|reactor|chain reaction|multiplication factor|neutron generation', [37,42,43],6)
rule('fusion',r'fusion|proton.proton|carbon cycle|thermonuclear', [42,43],6)
rule('nucleus',r'nucle|nuclide|isotope|binding energy|mass defect|alpha particle|proton|neutron', [42,43],3)
rule('quarks',r'quark|baryon|hadron|strangeness|meson', [44],5)
rule('particle-event',r'\breaction|\bpion|\bmuon|antiparticle|positron|annihilat|conservation|proton|neutron|neutrino', [44],4)
rule('galaxies',r'Hubble|galax|universe|big.bang|cosmolog|recession|recessional', [44],5)
rule('radiator',r'thermal radiator|Wien|blackbody|radiates|radiating', [33,38,40,43,44],4)
rule('relativity-clock',r'lifetime|mean life|time dilation|clock|time interval|proper time|decay|ages|age of|twin', [37],5)
rule('reference-frame',r'frame|observer|Lorentz|simultane|event|length contraction|proper length|speed parameter', [37],4)
rule('relativistic-particle',r'kinetic energy|rest energy|momentum|total energy|rest mass|electron|proton|particle', [37],3)
rule('spaceship',r'spaceship|spacecraft|rocket|shuttle',score=6)
rule('satellite',r'satellite|orbit|orbital', [13],5)
rule('binary-star',r'two stars|double.star|binary|two neutron stars', [13],6)
rule('planet',r'Earth|Moon|Mars|Jupiter|planet|Sun|star|asteroid|black hole', [1,13,19,32,33,43],3)
rule('gravity-pair',r'gravitational|gravitation|mass M|two.{0,15}particles|particles|sphere', [13],3)
rule('pendulum',r'pendulum',list(range(5,18)),7)
rule('gyroscope',r'gyroscope|precession', [10,11],7)
rule('yoyo',r'yo.yo', [10,11],7)
rule('pulley',r'pulley|Atwood',list(range(5,17)),6)
rule('elevator',r'elevator',list(range(2,13)),6)
rule('rollercoaster',r'roller.coaster|coaster car',list(range(4,12)),6)
rule('ladder',r'ladder', [12],6)
rule('beam',r'scaffold|beam|plank|diving board|horizontal.{0,10}rod|uniform.{0,10}rod', [12],5)
rule('rod',r'rod|stick|blade|barbell', [9,10,11,12,15],4)
rule('disk',r'disk|disc|turntable|merry.go.round|flywheel|grindstone|wheel|rotor|tire|hoop',list(range(4,16)),5)
rule('spring',r'\bspring\b|springs (?:of|with|are|have|in|each)' ,list(range(2,18)),5)
rule('collision',r'collision|collid|strikes a|strikes the|head.on', [9],6)
rule('billiards',r'pool table|billiard|cue ball', [9],7)
rule('center-mass',r'center of mass|center of gravity', [9,12],4)
rule('train',r'train|railroad|flatcar|locomotive',list(range(2,18)),6)
rule('car',r'\bcar\b|\bcars\b|automobile|truck|bus|motorcycle|hot rod',list(range(2,18)),5)
rule('plane',r'airplane|aircraft|jet plane|helicopter|plane flies',list(range(2,18)),5)
rule('boat',r'\bboat|\bship|sailboat|sailor|canoe|raft',list(range(2,18)),5)
rule('ball',r'\bball\b|baseball|basketball|tennis|golf ball|soccer',list(range(2,18)),4)
rule('book',r'\bbook\b',list(range(2,18)),6)
rule('box',r'\bbox\b|crate|trunk|block|bureau',list(range(2,18)),4)
rule('runner',r'runner|running|sprinter|athlete|walk|jog|hiker|cyclist|bicycl',list(range(2,18)),4)
rule('diver',r'\bdiver|\bdiving|swimmer|swimming',list(range(2,18)),5)
rule('projectile',r'projectile|bullet|cannon|fired|launched|thrown|throw',list(range(2,12)),4)
rule('drop',r'dropped|free.fall|falls|falling|stone|rock',list(range(2,12)),3)
rule('coordinate',r'vector|component|coordinates|coordinate|unit.vector|displacement|magnitude|direction|radians|angle', [3,4],3)
rule('particle-motion',r'particle|object|body|position|velocity|acceleration', [2,4,5,6,7,8,10,11],2)
rule('rope',r'rope|cord|cable|wire|tension|stress|strain|Young', [5,7,12],3)
rule('oscillator',r'oscillat|harmonic motion|amplitude|frequency|period', [15],3)
rule('fluid-tank',r'fish tank', [14],8)
rule('fish',r'\bfish\b(?!\s+tank)', [14],7)
rule('manometer',r'manometer|U.tube|mercury|barometer', [14],5)
rule('hydraulic',r'hydraulic(?! jump)|piston|syringe', [14],6)
rule('pipe-flow',r'hydraulic jump|pipe|hose|nozzle|flow|stream|water jet|faucet', [14],4)
rule('buoyancy',r'float|submerged|buoyant|buoyancy|immersed', [14],4)
rule('fluid-tank',r'water|liquid|pressure|fluid|tank|aquarium', [14],2)
rule('string-wave',r'wave|string|wire|tension|pulse|transverse|rubber band', [16],3)
rule('sound-pipe',r'pipe|tube|open end|closed end|organ', [17],5)
rule('speaker',r'sound|loudspeaker|speaker|source|siren|whistle|frequency|Doppler|beat|intensity|decibel', [17],3)
rule('thermometer',r'thermometer|Celsius|Fahrenheit|temperature scale|Kelvin|temperature.*scale|scale.*temperature', [1,18],5)
rule('expansion',r'expansion|expand|coefficient|length|aluminum|copper|steel|metal', [18],3)
rule('ice-water',r'ice|melt|freez|water|steam|boil', [18,20],4)
rule('heat-flow',r'heat|thermal|conductiv|insulat|radiat|temperature', [18],2)
rule('gas',r'gas|mole|molar|atoms|molecules|rms|distribution|kinetic energy|pressure|temperature', [19],3)
rule('piston',r'piston', [18,19,20],4)
rule('engine',r'engine|Carnot|refrigerator|heat pump|efficiency|cycle', [20],5)
rule('entropy',r'entropy|microstate|multiplicity|molecules|configuration', [20],3)
rule('dipole',r'dipole|ammonia|NH3', [21,22,24],5)
rule('charge-ring',r'ring|arc|circle|circumference', [21,22,23,24],5)
rule('charge-disk',r'\bdisk|\bdisc', [21,22,23,24],5)
rule('charge-rod',r'rod|line of charge|line charge|linear charge|nonconducting wire', [21,22,23,24],5)
rule('charge-shell',r'shell|concentric', [21,22,23,24,25],5)
rule('charge-sphere',r'sphere|spherical', [21,22,23,24,25],4)
rule('charge-plane',r'sheet|plate|plane|surface', [22,23,24],3)
rule('flux-box',r'cube|cubical|cubic|square|closed surface|die |faces', [23,32],5)
rule('charge-array',r'charge|charged|electron|proton|particle|electric field|electric potential', [21,22,23,24],2)
rule('capacitor',r'capacitor|capacitance|dielectric', [25,27,31,32],4)
rule('wire-current',r'wire|current density|drift|resistivity|resistance|resistor|current', [26],3)
rule('battery',r'battery|batteries|emf', [24,26,27],3)
rule('rc',r'discharg|charging|time constant|\bRC circuit', [25,27],6)
rule('resistor',r'resistor|resistance|circuit|current|potential difference|voltage', [27],2)
rule('cyclotron',r'cyclotron|spectrometer', [28],6)
rule('magnetic-particle',r'proton|electron|particle|positron|\bion\b|deuteron|alpha', [28],3)
rule('solenoid',r'solenoid|toroid', [28,29,30,32],6)
rule('magnetic-loop',r'coil|loop|dipole|torque|magnetic moment', [28,29,30,32],4)
rule('magnetic-wire',r'wire|current|conductor|cable', [28,29,30],3)
rule('inductor',r'inductance|inductor|henry|coil|induced|induction|emf|flux', [30,31],3)
rule('lc',r'\bLC circuit|\bLC oscillat|oscillating circuit|capacitor.*inductor', [31],6)
rule('ac',r'alternating|reactance|impedance|generator|sinusoid|phase|resonan|transformer|RLC|rms|frequency', [31],4)
rule('compass',r'compass|magnetic field of Earth|Earth.{0,5}magnetic field|Earth’s magnetic|inclination|magnetization|magnetiz|magnetic dipole|magnetic moment|paramagnet|ferromagnet|iron|magnet|susceptibility', [32],3)
rule('light-wave',r'light|electromagnetic|radiation|wave|wavelength|beam|intensity|frequency|photon', [33,35,36,38,40,44],2)
# Measurement objects; traces mark dimensions without inventing motion.
rule('measure-sphere',r'spher|Earth|Sun|\bball\b|radius|diameter', [1],5)
rule('measure-cylinder',r'cylinder|cylindrical|pillar|bottle|tank|barrel', [1],5)
rule('measure-block',r'stack|wood|candy|sand|cube|cubical|container|room', [1],4)
rule('clock',r'time|day|hour|minute|second|year|week|century|calendar|clock', [1],3)
rule('balance-scale',r'mass|density|kilogram|gram|weight|gold|iron|atoms', [1],3)
rule('ruler',r'length|distance|meter|metre|foot|feet|inch|mile|yard|furlong|cubit|point|gry|measure|unit', [1],2)

def desc(q):
 text=re.sub(r'http\S+|www\.\S+','',q['prompt']); text=re.sub(r'(?<=\w)-\s+(?=\w)','',text);text=re.split(r'Module \d|Additional Problems|Review & Summary',text)[0];text=re.sub(r'\s+',' ',text);text=text.split('?')[0][:650]
 matches=[]
 for kind,rx,chapters,score in rules:
  if chapters is not None and q['chapter'] not in chapters:continue
  m=rx.search(text)
  if m and re.search(r'(?:without|not|no)\s+(?:a |the |an )?$',text[:m.start()],re.I):continue
  if m:matches.append((score,-m.start(),kind,m.group(0)))
 if not matches:return None
 score,pos,kind,evidence=max(matches)
 # Motion is optional: absent an explicit motion cue, use a stationary-object reveal.
 motion=bool(re.search(r'mov|travel|slid|slid|speed|velocity|roll|fall|drop|fired|launch|throw|rotat|oscillat|flow|propagat|emits|radiates|decay|expan|compress',text,re.I))
 mode='trace'
 if re.search(r'oscillat|harmonic|vibrat',text,re.I):mode='oscillate'
 elif re.search(r'rotat|revolution|spin|angular speed',text,re.I):mode='rotate'
 elif re.search(r'fall|drop',text,re.I):mode='fall'
 elif re.search(r'mov|travel|slid|speed|velocity|roll|fired|launch|throw|flow',text,re.I):mode='travel'
 # Explicit static constraints take precedence for mechanics props.
 if re.search(r'remains at rest|remain stationary|stationary|equilibrium|rests on|fixed in place|held at rest',text,re.I):mode='trace'
 count=1
 for n,word in [(8,'eight'),(7,'seven'),(6,'six'),(5,'five'),(4,'four'),(3,'three'),(2,'two')]:
  if re.search(r'\b'+word+r'\s+(?:charged\s+|identical\s+|small\s+|thin\s+|long\s+)*(?:particles|charges|spheres|blocks|wires|rods|springs|slits|coils|lenses|mirrors|stars)',text,re.I):count=n;break
 return {'kind':kind,'mode':mode,'count':count,'evidence':evidence,'score':score,'vertical':bool(re.search(r'vertical|upward|downward|hang',text,re.I)),'incline':bool(re.search(r'inclin|slope|hill|ramp',text,re.I)),'hollow':bool(re.search(r'hollow|shell',text,re.I)),'circular':bool(re.search(r'circular|circle|ring|loop',text,re.I)),'channel':bool(re.search(r'stream|river|canal',text,re.I)),'curvedMirror':bool(re.search(r'spherical|concave|convex',text,re.I)),'perpendicular':bool(re.search(r'perpendicular|circular path|circular orbit',text,re.I)),'spectrometer':bool(re.search(r'spectrometer',text,re.I)),'quantumN':int((re.search(r'\bn\s*[=!$]\s*([1-6])\b',text) or [None,'1'])[1]),'ice':bool(re.search(r'\bice\b|melt|freez',text,re.I)),'gas':bool(re.search(r'\bgas|gaseous|molecular speed|rms speed',text,re.I)),'wall':bool(re.search(r'(?:strikes|hits|collid.{0,12})[^.]{0,25}wall',text,re.I)),'block':bool(re.search(r'\bblock|\bcrate',text,re.I)),'arc':bool(re.search(r'\barc|semicirc',text,re.I)),'rectangular':bool(re.search(r'rectang|square',text,re.I)),'toroid':bool(re.search(r'toroid',text,re.I)),'diverging':bool(re.search(r'diverging|concave lens',text,re.I)),'standing':bool(re.search(r'standing wave|resonan|harmonic',text,re.I)),'closed':bool(re.search(r'closed end|one end closed',text,re.I)),'negativeDirection':bool(re.search(r'negative direction|negative x|leftward',text,re.I)),'double':bool(re.search(r'two|double|pair',text,re.I))}

candidates={};report=[];manifest=dict(curated)
for c in range(1,45):
 items=[q for q in qs if q['chapter']==c and q['kind']=='Problems'];target=len(items)//2+1
 chosen=[]
 for q in items:
  d=desc(q)
  if d:candidates[q['id']]=d;chosen.append((q,d))
 # Favor specific named objects, retain existing individually authored scenes.
 needed=max(0,target-sum(q['id'] in curated for q in items))
 chosen=sorted([x for x in chosen if x[0]['id'] not in curated],key=lambda x:(-x[1]['score'],int(x[0]['number']) if x[0]['number'].isdigit() else 9999))[:needed]
 for q,d in chosen:manifest[q['id']]={k:v for k,v in d.items() if k not in ('score','evidence') and (k in ('kind','mode') or v is True or (k in ('count','quantumN') and v!=1))}
 count=sum(q['id'] in manifest for q in items)
 report.append({'chapter':c,'problems':len(items),'target':target,'illustrated':count,'candidateCount':sum(q['id'] in candidates for q in items)})
print('\n'.join(f"{r['chapter']:2} {r['illustrated']:3}/{r['target']:3}  candidates {r['candidateCount']:3}/{r['problems']:3}" for r in report))
(ROOT/'site/physics-loop-map.js').write_text('window.PhysicsLoopMap='+json.dumps(manifest,separators=(',',':'))+';\n')
(ROOT/'scripts/answer-data/physics-loop-coverage.json').write_text(json.dumps({'scope':'More than half of Problems per chapter. Every assignment requires explicit object/process text or an individually authored mapping; no chapter fallback. Illustrative views, not numerical solutions.','chapters':report,'totalIllustrated':len(manifest)},indent=2)+'\n')
audit=[{'questionId':q['id'],'chapter':q['chapter'],'promptSha256':hashlib.sha256(q['prompt'].encode()).hexdigest(),'excerpt':q['prompt'][:100],'sceneKind':manifest[q['id']] if isinstance(manifest[q['id']],str) else manifest[q['id']]['kind'],'matchedEvidence':candidates.get(q['id'],{}).get('evidence','individually authored'),'reviewType':'object-match' if isinstance(manifest[q['id']],dict) else 'individual'} for q in qs if q['id'] in manifest]
(ROOT/'scripts/answer-data/physics-illustration-audit.json').write_text(json.dumps(audit,separators=(',',':'),ensure_ascii=False)+'\n')
# Missing chapter candidates are printed separately for follow-up, not given a fallback.
(ROOT/'scripts/answer-data/physics-illustration-unmatched.json').write_text(json.dumps([{'id':q['id'],'prompt':q['prompt']} for q in qs if q['kind']=='Problems' and q['id'] not in candidates and q['id'] not in curated],indent=2,ensure_ascii=False)+'\n')
