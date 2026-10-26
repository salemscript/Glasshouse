#!/usr/bin/env python3
"""Original Biot–Savart/Ampere derivations; diagrams reviewed PDF20–28."""
import math,json,gzip,pathlib,subprocess
from math import pi,sqrt,sin,cos,tan,asin,acos,atan,atan2,radians,degrees,log
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[1]
mu=4*pi*1e-7;k=1e-7;e=1.602e-19;me=9.11e-31;c=2.998e8
rows=[]
def N(l,a,u,w,t=None,accepted=None):
 p=dict(label=l,type='numeric',answer=a,unit=u,tolerance=max(abs(a)*.009,1e-30) if t is None else t,explanation=w)
 if accepted:p['acceptedValues']=accepted
 return p
def C(l,a,b,c,w):return dict(label=l,type='choice',answer=a,options=[a,b,c],explanation=w)
def direction(l,a,w):return C(l,a,'Into the page' if a!='Into the page' else 'Out of the page','Zero field',w)
def R(n,parts,w,kind='problems',assumptions=None,scope=None):
 page=(21 if n<=6 else 22 if n<=19 else 23 if n<=28 else 24 if n<=35 else 25 if n<=47 else 26 if n<=62 else 27 if n<=76 else 28) if kind=='problems' else(20 if n<=9 else 21)
 r=dict(id=f'physics-chapter-29-{kind}-{n}',parts=parts,reasoning=w+' Verification: independently sum the signed Biot–Savart contributions or apply Ampere’s law to the stated source geometry; check SI dimensions and symmetry.',sourcePages=[page],assumptions=assumptions or ['Vacuum/air permeability μ₀=4π×10⁻⁷ T·m/A; ideal thin wires and long-wire/solenoid limits where stated.'])
 if scope:r['scope']=scope
 rows.append(r)
def line(i,r):return 2*k*i/r
def arc(i,r,phi):return k*i*phi/r
def loop(i,r,z=0):return mu*i*r*r/(2*(r*r+z*z)**1.5)
def wires(point,items):
 bx=by=0
 for (x,y),i in items:
  dx=point[0]-x;dy=point[1]-y;r2=dx*dx+dy*dy;bx+=-2*k*i*dy/r2;by+=2*k*i*dx/r2
 return bx,by
def vecparts(label,v,unit='T'):
 return [N(label+' · '+axis,a,unit,'Sum signed Cartesian components in the source axes.') for axis,a in zip(['x component','y component','z component'],v)]
def finite(i,A,B,P):
 # Integral of dl × r/r³ along a finite straight segment.
 ax,ay=A;bx,by=B;px,py=P;L=math.hypot(bx-ax,by-ay);ux=(bx-ax)/L;uy=(by-ay)/L
 s=(px-ax)*ux+(py-ay)*uy;hcross=ux*(py-ay)-uy*(px-ax);h2=hcross*hcross
 if h2<1e-30:return 0
 return k*i*hcross/h2*(s/sqrt(s*s+h2)-(s-L)/sqrt((s-L)**2+h2))
R(1,[N('a · Power-line field',line(100,6.1),'T','B=μ₀I/(2πr).'),C('b · Serious compass interference?','Yes; a transverse wire field can deflect the compass by about9°','Yes; it is hundreds of times larger','No; the wire field is exactly zero','Bwire/(20μT)≈0.164, giving a maximum transverse deflection arctan(0.164)≈9.3°, significant for surveying.')],'The source Earth field is20μT, not20mT.')
I=60e-12*.025**2/(k*.001)
R(2,[N('Whole-wire field',line(I,.025),'T','Peak dB=μ₀I ds/(4πr²); eliminate I to obtain B=2r dBmax/ds.')],'The plotted maximum is60pT atπ/2; whole-wire field is3nT.')
R(3,[N('a · Wire current',39e-6*.08/(2*k),'A','Cancel Earth’s39μT field at8cm.'),C('b · Current direction','East','West','North','An eastward current produces a southward field above the wire.')],'The net field is zero only if the wire opposes Earth’s northward field.')
R(4,[N('Field magnitude at C',0,'T','Equal currents split into opposite circulation semicircles, whose fields cancel.',0)],'Straight radial pieces contribute zero; equal branch resistance gives equal branch currents.')
R(5,[N('a · Field at a',mu*10/(4*.005)+2*k*10/.005,'T','Semicircle adds to two semi-infinite tangent legs.'),direction('b · Direction at a','Out of the page','The current rounds the left end counterclockwise.'),N('c · Field at b',2*line(10,.005),'T','Far from the bend both legs act as infinite wires.'),direction('d · Direction at b','Out of the page','Both straight-wire fields point out between the opposite currents.')],'Use different straight-wire limits at the end and far along the hairpin.')
R(6,[N('a · s of maximum contribution',0,'m','dB/ds is maximal at the perpendicular foot.',0),N('b · |s| for10% contribution',.02*sqrt(10**(2/3)-1),'m','dB(s)/dB(0)=[R²/(R²+s²)]^(3/2)=0.1.')],'There are two equal-distance elements, at±s.')
R(7,[N('a · Net field',arc(.411,.107,radians(74))-arc(.411,.135,radians(74)),'T','Opposite arcs subtract; the smaller radius dominates.'),direction('b · Direction','Out of the page','The smaller arc is counterclockwise.')],'Radial pieces give zero Biot–Savart cross product.')
R(8,[N('a · Net field',mu*.281/4*(1/.0315-1/.078),'T','Opposite semicircles subtract.'),direction('b · Direction','Into the page','The smaller arc runs clockwise.')],'The inner semicircle determines the net direction.')
R(9,[C('a · Current directions','Opposite directions','Same direction','Either direction gives the same field','At the midpoint equal same-direction currents cancel.'),N('b · Current in each wire',300e-6*.04/(4*k),'A','B=2[μ₀I/(2πr)] withr=.040m.')],'The source target field is300μT.')
R(10,[N('a · Field at C',mu*.0348/(4*.0926),'T','Only the semicircle contributes.'),direction('b · Direction','Into the page','The semicircle current is clockwise.')],'The radial segments have dl parallel to displacement from C.')
R(11,[N('a · Wire2 current',6.5*.015/(.015+.0075),'A','Equal fields require I₂/d₂=I₁/(d₁+d₂).'),direction('b · Wire2 direction','Out of the page','Opposite current directions cancel below both wires.')],'Use the full wire1-to-P distance2.25cm.')
R(12,[N('a · x of zero field',.16/4,'m','Between like currents I₁/x=3I₁/(d−x).'),C('b · Position when both currents double','Unchanged','Closer to wire1','Closer to wire2','The field equation is homogeneous in both currents.')],'The zero lies closer to the weaker wire.')
R(13,[N('Finite-wire field',2*k*.0582/.131*(.18/2)/sqrt(.131**2+(.18/2)**2),'T','B=μ₀I sinθ/(2πR), tanθ=(L/2)/R.')],'Both finite end contributions are equal.')
R(14,[N('Minimum L/R',2/sqrt(1.01**2-1),'dimensionless','B∞/Bfinite=√[1+(2R/L)²]; set this ratio1.01.')],'The source defines error relative to actual finite-wire field, not the infinite approximation.')
b1=arc(.4,.05,pi);b2=arc(.8,.04,2*pi/3)
R(15,[N('a · Original field magnitude',b2-b1,'T','The upper clockwise field is larger than the lower counterclockwise field.'),direction('b · Original direction','Into the page','Upper clockwise contribution dominates.'),N('c · Field after reversing i₁',b2+b1,'T','Reversal makes both fields point into the page.'),direction('d · Reversed direction','Into the page','The lower arc now reinforces the upper arc.')],'Radial legs contribute zero.')
a=loop(.004,.015);b=loop(.006,.025)
R(16,[N('Rotation angle',degrees(acos((100e-9**2-a*a-b*b)/(2*a*b))),'degrees','B²=B₁²+B₂²+2B₁B₂cosθ.')],'Rotate the field vector of loop2 about the common diameter; magnitudes stay fixed.')
R(17,[N('Finite-wire field',k*.693/.251*.136/sqrt(.136**2+.251**2),'T','At an end, B=μ₀I sinθ/(4πR), tanθ=L/R.')],'Only one endpoint subtends a nonzero angle.')
R(18,[N('Smaller semicircle radius',.02,'m','Initial sum47.25μT and reversed difference15.75μT give Bsmall/Blarge=2; radius ratio is1/2.')],'Flipping the semicircle reverses its normal, not its current magnitude.')
R(19,[N('Resultant field',math.hypot(line(30,2),line(40,2)),'T','Wire along+x gives+z field; wire along+z at y4 gives+x field.')],'The two fields are perpendicular, so add in quadrature.')
bc=loop(.00578,.0189);bw=line(.00578,.0189)
R(20,vecparts('a · Original field',(0,0,bc+bw))+vecparts('b · Rotated field',(bc,0,bw)),'Original loop current is counterclockwise; the straight tangent wire gives+z. A90° counterclockwise rotation about+y sends loopnormal+z to+x.',assumptions=['Counterclockwise rotation is viewed from the positive y end of the indicated rotation axis, as drawn.'])
R(21,[N('Net field magnitude',2*line(4,5)*4/5,'T','Each wire is5m fromP; the y components add and x components cancel.')],'Distances form a3–4–5 triangle.')
R(22,[N('a · x of maximum',.30,'m','Graph zero is0.10m=L/3; derivative zero of4/(x+L)−1/x occurs atx=L.'),N('b · Maximum By',2*k*.003/.30,'T','Atx=L, By=(μ₀I₂/2π)(2/L−1/L).'),direction('c · i₁ direction','Out of the page','Positive far-right By is due to larger out-of-page current.'),direction('d · i₂ direction','Into the page','Near-wire2 field is negative.')],'The graph x axis is measured from wire2, notwire1.')
R(23,vecparts('Magnetic force',(-e*200*line(.350,.0289),0,0),'N'),'At the proton, B points+z and velocity points−y; qv×B is−x.')
x=.15/(1+2*tan(pi/6))
R(24,[N('a · Wire1 x',-x,'m','By/Bx=[d/|x₁|−1]/2=tan30°.'),N('b · Wire3 x',x,'m','Equal same-sign currents at±x cancel the y components.')],'The two vertical wires maintain the same+x field while the horizontal pair changes By.')
R(25,[N('Arc angle θ',2,'rad','Two tangent semi-infinite fields totalμ₀I/(2πR), cancellingμ₀Iθ/(4πR).')],'The arc field opposes the combined straight-leg field.')
R(26,[N('Arc angle',degrees(2*sqrt(1e-10)/(sqrt(5e-10)*.5)),'degrees','The B² intercept is1×10⁻¹⁰T² and slope5×10⁻¹⁰T²/A²; θ=2B_arc/(I₁√slope).')],'The perpendicular wire field is in-plane, so its square adds without a cross term.')
R(27,[N('New current i₁',.040/tan(atan(.040/.030)-radians(20)),'A','Initial field angle isatan(I₂/I₁); clockwise rotation reduces it20°.')],'Wire1 above origin gives+x; wire2 left gives+y.')
R(28,[N('Arc angle',1,'rad','The net field vanishes atI₂=.50A; I₁θ=4I₂.')],'Straight-wire distance isR/2; radial legs give zero.')
bx,by=wires((.1,.1),[((0,.2),20),((.2,.2),-20),((.2,0),-20),((0,0),20)])
R(29,vecparts('Center field',(bx,by,0)),'Opposite x components cancel and all y components reinforce upward.')
R(30,[C('a · Wire2 location/current pair','θ₂=90° with current out of the page, or270° with current into the page','θ₂=0° with current out of the page','θ₂=180° with current into the page','The fixed wire supplies+2μT in+x and zero By; reversing both position and current is indistinguishable.'),N('b · Wire1 current',4,'A','Its sinusoidal component has amplitude4μT atR=.20m.'),direction('c · Wire1 direction','Out of the page','By varies from−4μT to+4μT asθ₁ goes0to180°.'),N('d · Wire2 current magnitude',2,'A','Its fixed+x field is2μT.'),C('e · Wire2 direction','Out of page at90°, or into page at270°','Into page at90°, or out of page at270°','Into page at0°, or out of page at180°','The graphs determine the signed field vector, not a unique position/current pair.')],'Read Bx(0)=2μT, Bx(90°)=6μT, and By endpoints±4μT.',scope='The graphs allow the two explicitly paired wire2 configurations; choosing the upper-half-plane location gives90° and out-of-page current.')
a=.047;verts=[(0,0),(2*a,0),(2*a,a),(a,a),(a,2*a),(0,2*a),(0,0)];bz=sum(finite(13,A,B,(2*a,2*a)) for A,B in zip(verts,verts[1:]))
R(31,[N('a · Field magnitude',abs(bz),'T','Integrate each finite straight segment; the segments collinear withP contribute zero.'),direction('b · Direction','Into the page','The two nearby inward-corner legs dominate the opposite distant-leg contributions.')],'The full closed stepped loop gives B=μ₀I/(4πa√2).')
A=(12-sqrt(56))/2;B=(12+sqrt(56))/2
R(32,[N('Smaller radius',.1*A/B,'m','A+B=12μT andA²+B²=(10μT)², so the smaller radius isR A/B.')],'Atθ0 the semicircle fields add; atπ/2 they are perpendicular.')
R(33,vecparts('Ribbon field',(0,2*k*.00461/.0491*log((.0216+.0491)/.0216),0)),'Integrate dB=(μ₀/2π)(I/w)dx/x over distancesd to d+w. Into-page wires produce+y at a point to their left.')
R(34,[N('Positive angle θ₂',degrees(acos((60e-9**2+40e-9**2-80e-9**2)/(2*60e-9*40e-9))),'degrees','B²=B₁²+B₂²−2B₁B₂cosθ₂ with B₁60nT,B₂40nT.')],'Wire1 at180° gives+y; wire2’s field rotates with its position.')
R(35,[N('x force per length',2*k*.004*.0068*.05/(.05**2+.024**2),'N/m','Opposite currents repel; Fx/L=μ₀I₁I₂Δx/(2πr²).')],'The separation includes the vertical2.40cm offset.')
vals=[]
for j in range(5):vals.append(sum(2*k*3*3*10*(m-j)/abs(m-j)**2/.08 for m in range(5) if m!=j))
R(36,[N(f'{chr(97+j)} · Wire{j+1} y force',v,'N','Parallel same-direction wires attract; sum signed reciprocal separations.') for j,v in enumerate(vals)],'The central wire is force-free by reflection symmetry; end forces are equal/opposite.')
def wireforce(pos,I,others):
 fx=fy=0
 for p,J in others:
  dx=p[0]-pos[0];dy=p[1]-pos[1];r2=dx*dx+dy*dy;fx+=2*k*I*J*dx/r2;fy+=2*k*I*J*dy/r2
 return fx,fy
f=wireforce((0,0),7.5,[((0,.135),7.5),((.135,.135),-7.5),((.135,0),-7.5)])
R(37,vecparts('Force per length',(f[0],f[1],0),'N/m'),'Use signed current products: same directions attract and opposite directions repel.')
R(38,[N('a · Wire2 current',.627e-6*.12/(2*k*.75),'A','Graph zero atx=.040m givesd=3x=.120m; asymptotic force=−μ₀I₁I₂/(2πd).'),direction('b · Wire2 direction','Out of the page','Wire3 attracts wire2 toward+x near it, so they have the same sign.')],'Graph horizontal coordinate is distance from wire2. Asymptote is−.627μN/m, notmillinewtons.')
f=wireforce((1.,0),-.25,[((0,0),-2),((.5,0),4),((1.5,0),-4),((2,0),-2)])
R(39,[N('Force per length magnitude',math.hypot(*f),'N/m','Signed forces on wire3 sum to the right.')],'The two far equal currents cancel; unlike currents on the left repel while like currents on the right attract.')
f=wireforce((0,.085),15,[((.085,.085),15),((.085,0),15),((0,0),15)])
R(40,vecparts('Force per length',(f[0],f[1],0),'N/m'),'All currents attract; side and diagonal forces yield Fx=−Fy.')
R(41,vecparts('Net force',(0,2*k*30*20*.30*(1/.01-1/.09),0),'N'),'The nearer horizontal segment is attracted upward more strongly than the far segment is repelled; vertical-side forces cancel.')
R(42,[N('Signed circulation',mu*15*(.5*4*.20*3*.20),'T·m','The counterclockwise triangular path encloses area6d² and positive-z current.')],'Ampere’s integral depends on enclosed current, not detailed B distribution.')
R(43,[N(f'{chr(97+j)} · B at r={r:g}m',0 if r==0 else line(170,r)*min(1,r*r/.02**2),'T','Inside a uniform wire Ienc=I(r/a)²; outside use the full current.') for j,r in enumerate([0,.01,.02,.04])],'The field rises linearly to its maximum at the surface and then falls as1/r.')
R(44,[N('a · Path1 circulation',mu*(3-5),'T·m','Path1 upward normal links−i₁+i₂.'),N('b · Path2 circulation',mu*(2*5-3),'T·m','Path2 has two positive linkings with the left current loop and one negative linking with the right.')],'Count algebraic linking numbers, including winding direction, rather than geometric proximity.')
R(45,[N('a · Path1 circulation',mu*2,'T·m','Clockwise orientation counts net one inward current positively.'),N('b · Path2 circulation',0,'T·m','Equal inward/outward currents cancel algebraically.',0)],'Only currents inside each path contribute.')
# Problem46 winding audit is finalized below after tracing the complete source contour.
R(46,[N('Signed circulation',mu*.0045*(1+3+7-6),'T·m','Trace the winding contour; enclosed signed currents are1,3,7 outward and6 inward.')],'Currents2,4,5,8 lie in excluded bays of the contour.')
R(47,[N('a · Center field',0,'T','Ienc vanishes faster thanr at the center.',0),N('b · Field at a/2',mu*310*.0031/12,'T','Integrate J₀r/a: B=μ₀J₀r²/(3a).'),N('c · Surface field',mu*310*.0031/3,'T','Evaluate the same expression atr=a.')],'The nonuniform current density must be integrated over concentric annuli.')
R(48,[N('a · Wire current',3*.008/8,'A','AtP, opposing signed contributions satisfy.008/(2R)−I/R=I/(3R).'),direction('b · Wire direction','Into the page','This makes the wire field leftward at both points, opposing the pipe field atP.')],'At the pipe center the pipe itself produces zero field.')
R(49,[N('a · Inner-radius field',mu*500*.8/(2*pi*.15),'T','ToroidalB=μ₀NI/(2πr).'),N('b · Outer-radius field',mu*500*.8/(2*pi*.20),'T','Outer radius=.15+.05=.20m.')],'Field is not uniform across the finite toroid cross-section.')
R(50,[N('Interior field',mu*1200*3.6/.95,'T','B=μ₀NI/length.')],'Use the ideal long-solenoid approximation.')
R(51,[N('Interior field',mu*200*.29/.25,'T','B=μ₀NI/length.')],'Solenoid diameter does not enter the ideal interior field.')
Nturn=.023*1.3/(mu*18)
R(52,[N('Wire length',Nturn*pi*.026,'m','First obtainN=Bℓ/(μ₀I), then multiply byturn circumferenceπd.')],'Neglect small helical pitch correction to each turn length.')
R(53,[N('Solenoid current',me*.046*c/(e*.023)/(mu*10000),'A','Electronorbit requiresB=mv/(er), thenB=μ₀nI with100turns/cm=10000/m.')],'The speed.046c is safely nonrelativistic at this precision.')
R(54,[N('Revolutions',e*mu*8000*4/(2*pi*me*800*cos(pi/6)),'turns','Nrev=(eB/2πm)[ℓ/(vcos30°)]; Bℓ=μ₀NI.')],'The unknown solenoid length cancels; assume uniform field through both ends.')
b=mu*1000*.020
R(55,[N('a · Radius for45°',2*k*6/b,'m','At45° the azimuthal wire field equals the axial solenoid field.'),N('b · Total field',sqrt(2)*b,'T','Perpendicular equal components add in quadrature.')],'The resulting radius lies within the7cm solenoid.')
R(56,[N('Midpoint field',2*200*loop(.0122,.25,.125),'T','Add both200-turn coil fields at axialdistanceR/2.')],'Helmholtz spacing equals coil radius.')
m=300*4*pi*.025**2
R(57,[N('a · Magnetic moment',m,'A·m²','μ=NIπr².'),N('b · Axial distance',((mu*m/(2*pi*5e-6))**(2/3)-.025**2)**.5,'m','Use the coil axial field; dipolelimit givesnearlythe same distance.')],'The target is5μT; at z≫d the dipole formula is accurate.',scope='The coil is short; finite-radius correction is included and the far-axis dipole approximation is also accepted.')
rows[-1]['parts'][1]['acceptedValues']=[(mu*m/(2*pi*5e-6))**(1/3),.46]
R(58,[N('a · B₂/B₁',4,'dimensionless','B∝N/r; two turns at half radius give4timesB.'),N('b · μ₂/μ₁',.5,'dimensionless','μ∝Nr²; two turns at half radius givehalf the moment.')],'Total wire length is fixed.')
R(59,[N('Magnetic moment',200*.29*pi*.05**2,'A·m²','Use Problem51’s200turns,0.29A, radius5cm.')],'The source reference imports the full solenoid dimensions from Problem51.')
rows[-1]['reviewNotice']='The imported0.47A·m² reference conflicts with the supplied Problem51 givens, which give0.456A·m² (0.46 to two significant figures). The0.47 value corresponds to rounding the current to0.30A first.'
rows[-1]['referenceAnswer']='Magnetic moment=0.45553A·m², approximately0.46A·m².'
I1=7.2e-6/loop(1,.04,.03);I2=43.2e-6/loop(1,.04)
R(60,[N('a · Current1 magnitude',I1,'A','At y→∞ only loop1 remains; B₁(0)=7.20μT at axialdistance3cm.'),N('b · Current2 magnitude',I2,'A','At y=0 netBy=−36μT, so loop2 contributes−43.2μT.')],'Loop currents have opposite magnetic moment directions; read the graph’s initial value−36μT.')
b=loop(15,.12)
R(61,[N('a · Loop-center field',b,'T','SingleloopB=μ₀I/(2R).'),N('b · Coil torque',50*1.3*pi*.0082**2*b,'N·m','The planes are perpendicular, hence μ andB are perpendicular andτ=μB.')],'Treat the large-loop field as uniform across the small coil.')
R(62,[N('a · Center field',arc(.0562,.0572,pi)+arc(.0562,.0936,pi),'T','Both semicircle currents circulate clockwise aroundP.'),direction('b · Field direction','Into the page','Apply the right-hand rule to both arcs.'),N('c · Magnetic moment',.0562*pi/2*(.0572**2+.0936**2),'A·m²','The loop encloses the sum of the two half-disk areas.'),direction('d · Moment direction','Into the page','The complete planar loop is clockwise.')],'This is not an annular half-loop: the two semicircles lie on opposite sides of the diameter.')
R(63,vecparts('a · Magnetic moment',(0,6*.10**2,0),'A·m²')+[N('b · Far-field magnitude',mu*6*.1**2/(2*pi*5**3),'T','Three oriented square moments cancel inx,z and sum to+y; point(0,5,0) is axial.')],'The cube path’s area-vector sum is one square in+y; use the dipole approximation at5m≫0.1m.')
R(64,[N('a · Center field',arc(.200,2,2*pi-pi/4)-arc(.200,4,2*pi-pi/4),'T','Opposite major arcs subtend2π−θ, notθ.'),direction('b · Direction','Out of the page','The inner major arc dominates and is counterclockwise.')],'The missing wedge isπ/4, so the conducting arcs cover7π/4.')
R(65,[N('Interior radius',.100e-3*.008**2/(2*k*25),'m','Inside uniform wireB=μ₀Ir/(2πa²).')],'The result is less than the8mm outer radius.')
R(66,vecparts('a · Origin field',(0,0,-line(6,.10)-line(10,.05)))+[N('b · Zero-field y',.08125,'m','6/(y−.10)+10/(y−.05)=0.'),N('c · Zero-field y withI₁ reversed',.175,'m','−6/(y−.10)+10/(y−.05)=0.')],'Fields from+x currents point−z below each wire; the signed field equation determines both roots.')
R(67,[C('Center-field comparison','B_square/B_circle=8√2/π²>1','B_square/B_circle=π²/(8√2)<1','Both are equal for fixed wire length','Square sideL/4 gives8√2μ₀I/(πL), while circle radiusL/(2π) givesπμ₀I/L.')],'Integrate all four finite square sides; do not approximate them as infinite wires.')
f=e*1e7*line(50,.05)
R(68,[N('a · Radially moving electron force',f,'N','Radial velocity is perpendicular to azimuthalB.'),N('b · Axially moving electron force',f,'N','Axial velocity is also perpendicular toB.'),N('c · Azimuthally moving electron force',0,'N','This velocity is parallel or antiparallel toB.',0)],'Use magnitude|q|vBsinθ; charge sign affects direction, not magnitude.')
R(69,[N('a · Wireb current',15,'A','Each base wire pulls topa downward byFcos30°; wireb atheight√3L/2 balances both.'),C('b · Direction','Negative z','Positive z','Zero current','Wireb must repel the upper wire to balance downward attraction.')],'The shorter top-to-midpoint distance changes the required current to3I/2.')
R(70,[N('Center field magnitude',k*2*pi/4,'T','The two equal-radius quarter-circle fields oppose and cancel, leaving the4m half-circle.')],'All radial connecting segments contribute zero.')
R(71,[N('Surface field',line(50,.0026/2),'T','The source diameter is2.6mm; radius is1.3mm.')],'A factor-of-two error results from using diameter asradius.')
R(72,[C('a · Wire-current magnitudes','5.0mA or55mA','25mA only','30mA or50mA','The external field fixes |Iwire+30mA|=25mA; either signed total is possible.'),C('b · Direction','Downward for either permitted magnitude','Upward for either permitted magnitude','Upward for5mA and downward for55mA','Iwire=−5mA or−55mA when upward shell current is+30mA.')],'Only the field magnitude is supplied; its direction is not, so there are two admissible wire currents.',scope='Both downward currents satisfy the supplied field magnitude; an extra field-direction specification would select one.')
R(73,[N('a · Hole-center field',mu*5.25*.02/(2*pi*(.04**2-.015**2)),'T','Superpose a uniformly filled positive cylinder with a negative-current cylinder at the hole.'),C('b · Special-case behavior','d=0 gives zero field in the hole; b→0 retains the solid-cylinder local field at its former center','Both b=0 andd=0 give zero at anylocation','The field diverges whenb→0','Inside the cavity B=μ₀Jd/2, uniform and independent of the cavity coordinates.')],'The actual current density isI/[π(a²−b²)], notI/(πa²).')
R(74,[N('Wire current',7.30e-6*.88/(2*k),'A','Invert the long-wire fieldB=μ₀I/(2πr).')],'The source field is7.30μT, notmT.')
def segment(P):
 x,y,z=P;r=(x*x+y*y+z*z)**.5;return(k*2*.03*z/r**3,0,-k*2*.03*x/r**3)
R(75,sum([vecparts(f'{chr(97+j)} · Field at point',segment(P)) for j,P in enumerate([(0,0,5),(0,6,0),(7,7,0),(-3,-4,0)])],[]),'Use iΔs×r/r³ withΔs along+y. Far from the3cm segment the current-element approximation is valid.')
bx,by=wires((.05,.05),[((0,0),100),((.10,0),100)]);cx,cy=wires((.05,.05),[((0,0),100),((.10,0),-100)])
R(76,vecparts('a · Same-direction currents',(bx,by,0))+vecparts('b · Opposite currents',(cx,cy,0)),'The right angle atP and midpoint symmetry make each wire-P distance d/√2.')
R(77,[C('Equivalent magnetic field','B=μ₀I/(2πR), out of the page','B=μ₀I/(4R), into the page','B=0 because the currents cancel','The twoquarter-arc fields cancel; the remaining two tangent semi-infinite fields add to the infinite-wire field.')],'Use signed contributions from both bent wires, including the finite arc normals.')
R(78,[N('Zero-field distance',line(100,5e-3),'m','Setμ₀I/(2πr)=Buniform.')],'There is one cancelling side of the wire; the opposite side reinforces.')
a=.004;b=.002
R(79,[N(f'{chr(97+j)} · Field at r={r:g}m',line(24 if r<b else 24*(1-(r*r-b*b)/(a*a-b*b)) if r<a else 0,r),'T','Enclosed central current and opposite annular current subtract algebraically.') for j,r in enumerate([.001,.003,.005])],'Outside both conductors, equal/opposite total currents give zero field.')
R(80,[N('Wire radius',sqrt((.004*.010*.20e-3)/(.28e-3)),'m','At4mm field is interior; at10mm it must be exterior. Divide B₄/B₁₀=4mm×10mm/a².')],'If both points were inside, the field would increase withr, contradicting the data.')
R(81,[C('a · Field direction','Left above the sheet; right below the sheet','Right above; left below','Perpendicular to the sheet on both sides','Pairs of equally spaced current filaments cancel normal components and reinforce tangential components.'),C('b · Magnitude','B=μ₀λ/2, independent of distance','B=μ₀λ/r','B=0 outside the sheet','A rectangular Amperian loop has2Bℓ=μ₀λℓ.')],'An infinite ideal sheet has translational symmetry; both Biot–Savart integration and Ampere’s law give the same result.')
bx,by=wires((.342,0),[((0,.186/2),4.23),((0,-.186/2),-4.23)])
R(82,vecparts('Net field',(bx,by,0)),'The y components cancel and the x components reinforce to the right.')
a=.08;verts=[(0,0),(a,0),(a,a),(0,a),(0,0)];P=(a/4,3*a/4);# clockwise source current goes downward onright
bz=-sum(finite(10,A,B,P) for A,B in zip(verts,verts[1:]))
R(83,vecparts('Finite-square field',(0,0,bz)),'Sum the exact four finite-side fields atP, whose distances from the top and left sides area/4.')
R(84,[N('a · Outer-wire force, center current+x',3*2*k*5*(3.2/.1+5/.2),'N','The adjacent center wire and far outer wire both attract.'),N('b · Outer-wire force, center current−x',3*2*k*5*abs(-3.2/.1+5/.2),'N','The nearer opposite current repels while the far outer wire attracts.')],'The requested magnitude is the same for either outer wire by symmetry.')
R(85,[C('a · Annular-conductor interior field','B(r)=μ₀I(r²−b²)/(2πr(a²−b²))','B(r)=μ₀I/(2πr) throughout the hollow region','B(r)=μ₀Ir/(2πa²) for everyb','Ienc=I(r²−b²)/(a²−b²).'),C('b · Boundary limits','B(b)=0; B(a)=μ₀I/(2πa); b=0 gives μ₀Ir/(2πa²)','B(b)=B(a); b=0 gives zero','The field diverges at both boundaries','Apply the same enclosed-current expression before taking limits.'),N('c · Surface peak for plotted example',line(100,.02),'T','Peak occurs ata=.020m; insideholezero, annularrise, outside1/r.'),C('c · Plot shape','Zero to1.8cm, then rises to1mT at2.0cm, then decays as1/r','Constant1mT throughout0–6cm','Diverges at1.8cm andvanishes outside2cm','Use the three radial regions witha2cm,b1.8cm,I100A.')],'The symbolic formula covers onlyb<r<a; attach zero and exterior branches for the requested plot.',scope='The checks assess the piecewise relation, boundary limits and plot features; they do not automatically evaluate a freehand drawing.')
R(86,[C('Rectangular-loop field','B=2μ₀I√(L²+W²)/(πLW)','B=μ₀I/(2π√(LW))','B=μ₀I(L+W)/(πLW)','Integrate each finite side at perpendicular distanceW/2 orL/2, then sum four same-normal fields.')],'The square limit reproduces the four-side result in Problem67.')
R(87,[C('a · r<c','B=μ₀Ir/(2πc²)','B=0','B=μ₀I/(2πr)','Inner conductor encloses thefractionr²/c².'),C('b · c<r<b','B=μ₀I/(2πr)','B=μ₀Ir/(2πb²)','B=0','Full inner current is enclosed; none of the return current is enclosed.'),C('c · b<r<a','B=μ₀I(a²−r²)/(2πr(a²−b²))','B=μ₀I(r²−b²)/(2πr(a²−b²))','B=μ₀I/(2πr)','Subtract the enclosed return-current fraction fromI.'),N('d · Exterior field',0,'T','Total enclosed current iszero.',0),C('e · Continuity tests','B(0)=0; fields agree atc,b; B(a)=0','B diverges atc andb','B jumps atallthreeinterfaces','Finite uniform volume currents have continuousB across each interface.'),N('f · Peak field of example',line(120,.004),'T','Peak atc=.004m is6mT.'),C('f · Plot behavior','Linear rise to6mT at0.40cm, inverse-r fall to1.8cm, return-current fall tozero at2cm','Zero below0.40cm andconstant above','Inverse-square decrease everywhere','Usea2cm,b1.8cm,c.40cm,I120A.')],'The four pieces follow enclosed current and join continuously.',scope='The checks cover all radial pieces, limiting values and graph features, not automatic assessment of a freehand plot.')
F=2*k*(450e3)**2*log((.012+.067)/.067)
R(88,[C('a · Rail-gun force','F=μ₀I² ln((w+R)/R)/(2π), directed right','F=μ₀I²/(2πw), directed left','F=0 because the rails carry opposite currents','Integrate I dℓ×B across the projectile; the two rail contributions reinforce rightward.'),N('b · Exit speed',sqrt(2*F*4/.010),'m/s','Constant-current workFL=(1/2)mv² withw=.012m,R=.067m.')],'Use the printedgap12mm andrailradius6.7cm; both enter only through their ratio.')
# Conceptual questions: independently derived from original source diagrams.
R(1,[C('Field-magnitude ranking','c > a > b','a > b > c','a = b = c','The small andlarge arcs reinforce in(c), and the larger fraction of small-radius circumference makes(c)largest. In(b), inner andouter arc fields subtract.')],'UseB=μ₀Iφ/(4πr) with signed arc circulation; radial legs givezero.',kind='questions')
R(2,[C('Force-magnitude ranking','1 > 3 = 4 > 2','1 = 2 > 3 = 4','2 > 1 > 3 > 4','Electron2 moves parallel to the localB and feelszero; electrons3and4 areequidistant andperpendicular toB.')],'Below the rightward wire current, B points into the page; force magnitude is|q|vBsinθ.',kind='questions')
R(3,[C('Center-field ranking','c > d > a = b','a > b > c > d','a = b = c = d','All-out arrangement(a) and diagonal alternating(b) cancel; two adjacent inward currents(c) reinforce most.')],'Add the equal-radius wire fields as Cartesian vectors at the squarecenter.',kind='questions')
R(4,[direction('a · Current2 direction','Into the page','P lies to the left of bothwires, so cancellation requires opposite current signs.'),C('b · Current2 compared withcurrent1','Greater','Less','Equal','Wire2 is farther fromP; equalB requires largerI.')],'SetI₁/r₁=I₂/r₂ usingr₂>r₁.',kind='questions')
R(5,[C('Center-field ranking','a > c > b','a > b > c','c > b > a','In unitsμ₀I/(4r), fields area4/3,c13/12,b2/3; arc signs andradii must allbe retained.')],'The three radii arer,2r,3r; outerhalf-circle contributes1/3, innerbottomsemicircle contributes1, while(c)addsquarters1/2and1/4.',kind='questions')
R(6,[C('a · Radius ranking','c > a > d > b','a > b > c > d','a = c > b = d','The peak of eachcurve occurs at its wire radius.'),C('b · Surface-field ranking','a > c > b > d','c > a > d > b','a = c > b = d','Read eachpeakheight, not the exterioroverlap.'),C('c · Current ranking','a = c > b = d','a > c > b > d','c > a > d > b','ExteriorB∝I/r, so overlappingexteriorbranches indicate equalcurrents.'),C('d · Density inacomparedwithc','Greater','Less','Equal','InteriorB=μ₀Jr/2; wirea has the greaterinitialslope.')],'Use thelinearinterior andinverse-radius exteriorlaws independently.',kind='questions')
R(7,[C('Circulation-magnitude ranking','c = d > b > a','d > c > b > a','a = b = c = d','c,d enclose allthecurrent; b encloses morecrosssectionthana.')],'Ampere’s integral tracks enclosedcurrent, notlocalfieldmagnitude.',kind='questions')
R(8,[C('Central-force magnitude ranking','b > d > c > a','a > b > c > d','b = d > a = c','In commonunitsμ₀I²/(2πd), netmagnitudes are3,2,1,0 forb,d,c,a.')],'Pairwise wireforces fall as1/separation; signedattraction/repulsion gives thefourvalues.',kind='questions')
R(9,[C('Circulation-magnitude ranking','b > a > d > c','a > b > c > d','d > c > b > a','Enclosed signed currents are4,−5,0,−3A forloops a,b,c,d.')],'Take theabsolutevalue of the algebraic enclosedcurrent.',kind='questions')
R(10,[C('Signed-circulation ranking','d > a = e > b > c','a > b > c > d > e','a = b = c = d = e','In unitsμ₀i the signedlinkings are a2,b0,c−2,d4,e2; twistedlobes reverse theencirclementorientation.')],'Follow the arrows andassign apositive ornegative linking sign ateachwire.',kind='questions')
R(11,[C('a · Force-magnitude ranking','1 > 3 > 2','1 > 2 > 3','3 > 1 = 2','The magnitudes areu+v,√(u²+v²),u−v, withu>v>0.'),C('b · Angle from dashedvertical','Less than45°','Equal to45°','Greater than45°','In(3), the nearerwire produces the largerupward component; tanθ=d/D<1.')],'UseF/L∝1/distance andtheperpendicularforcevectors in(3).',kind='questions')
# Restore readable prose spacing while keeping the mathematical contracts unchanged.
replacements={'theentire':'the entire','thefull':'the full','thefield':'the field','thewire':'the wire','theloop':'the loop','thecurrent':'the current','thetwo':'the two','thefour':'the four','thethree':'the three','thegreater':'the greater','thelarger':'the larger','thesame':'the same','theopposite':'the opposite','thepositive':'the positive','thenegative':'the negative','themaximum':'the maximum','theminimum':'the minimum','thevertical':'the vertical','thehorizontal':'the horizontal','theinner':'the inner','theouter':'the outer','atP':'at P','withcurrent':'with current','loopnormal':'loop normal','samewireloop':'same wire loop','onlythrough':'only through','wirelength':'wire length','sourceprecision':'source precision','sourcecurrent':'source current','crosssection':'cross section','finitewire':'finite wire','same-direction':'same-direction','initialslope':'initial slope','initialvalue':'initial value','plotfeatures':'plot features','fieldregion':'field region','signedlinkings':'signed linkings','theencirclementorientation':'the encirclement orientation','mostpositive':'most positive','fartherfrom':'farther from','fromP':'from P','morecrosssectionthana':'more cross section than a','wireforces':'wire forces','signedattraction':'signed attraction','andtheperpendicularforcevectors':'and the perpendicular force vectors','theperpendicular':'the perpendicular','thecenter':'the center','uniformfield':'uniform field'}
def clean(v):
 if isinstance(v,str):
  for a,b in replacements.items():v=v.replace(a,b)
  import re
  v=re.sub(r'(?i)\b(wire|loop|current|particle|curve|arrangement|Problem)([0-9]+)',r'\1 \2',v)
  return v
 if isinstance(v,list):return [clean(x) for x in v]
 if isinstance(v,dict):return {k:(x if k=='id' else clean(x)) for k,x in v.items()}
 return v
rows=[clean(r) for r in rows]

# Accept valid angular conventions, preserve exact zeros, and audit coverage.
for r in rows:
 for p in r['parts']:
  if p['type']=='numeric' and p['unit']=='degrees':
   p['acceptedValues']=list(dict.fromkeys(p.get('acceptedValues',[])+[p['answer']-360,p['answer']+360]))
source=json.loads(gzip.decompress((ROOT/'site/questions/physics.json.gz').read_bytes()))
expected={q['id'] for q in source if q['chapter']==29}
assert len(rows)==99 and len({r['id'] for r in rows})==99
assert {r['id'] for r in rows}==expected
for r in rows:
 for p in r['parts']:
  assert p['label'] and p['explanation']
  if p['type']=='numeric':assert math.isfinite(p['answer']) and p['tolerance']>=0 and (p['answer']==0 or p['tolerance']<abs(p['answer']))
  else:assert p['answer'] in p['options'] and len(set(p['options']))==3
(HERE/'ch29.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'records',sum(len(r['parts']) for r in rows),'fields')
