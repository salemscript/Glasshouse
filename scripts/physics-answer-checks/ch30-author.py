#!/usr/bin/env python3
"""Original Faraday/Lenz/RL derivations from visually reviewed chapter PDF30–39."""
import json,math,gzip,pathlib,subprocess
from math import pi,sqrt,log,exp,sin,cos
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[1]
mu=4*pi*1e-7;eps=8.854e-12;e=1.602e-19;me=9.11e-31
rows=[]
def N(l,a,u,w,t=None):return dict(label=l,type='numeric',answer=a,unit=u,tolerance=max(abs(a)*.008,1e-30) if t is None else t,explanation=w)
def C(l,a,b,c,w):return dict(label=l,type='choice',answer=a,options=[a,b,c],explanation=w)
def D(l,a,w):return C(l,a,*[x for x in ['Clockwise','Counterclockwise','None'] if x!=a][:2],w)
def R(n,p,w,kind='problems',assumptions=None,scope=None):
 page=(32 if n<=6 else 33 if n<=16 else 34 if n<=28 else 35 if n<=39 else 36 if n<=56 else 37 if n<=74 else 38 if n<=86 else 39) if kind=='problems' else (30 if n<=2 else 31 if n<=10 else 32)
 r=dict(id=f'physics-chapter-30-{kind}-{n}',parts=p,reasoning=w+' Verification: independently differentiate the source flux or solve Kirchhoff equations; check SI dimensions and the energy balance where applicable.',sourcePages=[page],assumptions=assumptions or ['Ideal wires, inductors and stated field approximations; μ₀=4π×10⁻⁷ H/m.'])
 if scope:r['scope']=scope
 rows.append(r)
R(1,[N('Induced emf',0,'V','Flux BAcosθ is constant even while the normal precesses.')],'Rotation alone is not enough; only changing linked flux creates emf.')
R(2,[N('Induced emf magnitude',.8*2*pi*.12*.75,'V','|d(πr²B)/dt|=2πBr|dr/dt|.')],'Convert75cm/s to.75m/s.')
R(3,[N('Coil current',120*mu*22000*pi*.016**2*1.5/.025/5.3,'A','i=Nμ₀nAsole|ΔI/Δt|/R; use solenoid area, not coil area.')],'Field is confined to the smaller solenoid.')
R(4,[N('a · Emf magnitude',pi*.12**2*.5/2,'V','Field rises.5T in2s.'),N('b · Emf magnitude',0,'V','The field plateau has zero derivative.'),N('c · Emf magnitude',pi*.12**2*.5/2,'V','Field falls.5T in2s.')],'The two nonzero emfs have opposite senses; the prompt requests their scalar magnitudes.')
R(5,[N('Induced loop current',0,'A','Equal and opposite flux above and below the centered wire cancels for every current.')],'Reflection symmetry makes total linked flux identically zero.')
R(6,[N('Field slope a',.008,'T/s','Graph currents1.5mA and.5mA; R=6μV/1.5mA=.004Ω; |emf_ind|=R(1mA)=4μV; a=emf/A.')],'Original PDF battery is6.00μV, not OCRmV; induced emf opposes battery.')
R(7,[N('a · Emf magnitude',.031,'V','dΦ/dt=(12t+7)mWb/s at2s.'),C('b · Current through R','Right to left','Left to right','No current','Outward flux increases, requiring clockwise circulation.')],'A clockwise loop travels through the bottom resistor right to left.')
rwire=1.69e-8*(pi*.1)/(pi*(.0025/2)**2)
R(8,[N('Required field change rate',10*rwire/(pi*.05**2),'T/s','Use wire lengthπDloop and wire areaπdwire²/4 in R=ρl/A.')],'The wire diameter and loop diameter enter different areas.')
R(9,[N('Emf amplitude',6.8e-6*mu*85400*1.28*212,'V','Amplitude Aμ₀nI₀ω.')],'854turns/cm=85400turns/m.')
R(10,[N('a · Emf magnitude',.076*pi*.037**2/sqrt(2)/.0045,'V','The two half-loop area vectors add to πr²/√2 alongB.'),D('b · Viewed along B','Clockwise','Decreasing B induces a field along the original B; viewed in its direction, circulation is clockwise.')],'Use the vector projected area, not the original flat area.')
R(11,[C('a · Generator emf','ε=2πfNabB sin(2πft)','ε=NabB cos(2πft)','ε=2πfNabB cos²(2πft)','Differentiate Φ=NabBcos(2πft).'),N('b · Nab',150/(2*pi*60*.5),'m²','Nab=ε₀/(2πfB).')],'Each turn has areaab, and all turns link the same sinusoidal flux.')
R(12,[N('a · Emf for static Bz(y)',0,'V','The fixed loop sees static flux.'),D('b · Direction','None','No linked-flux change.'),N('c · Emf for Bz=.06t',.06*.4*.25,'V','AreaLW times field time derivative.'),D('d · Direction','Clockwise','Increasing outward field is opposed.'),N('e · Emf for Bz=.08yt',.08*.4*.25**2/2,'V','Integrate y from0 toW.'),D('f · Direction','Clockwise','Positive outward flux increases.'),N('g · Emf for By=.03xt',0,'V','In-plane field has zero normal component.'),D('h · Direction','None','Zero linked flux.'),N('i · Emf for Bx=.05yt',0,'V','In-plane field has zero normal component.'),D('j · Direction','None','Zero linked flux.')],'The loop occupies0<x<L,0<y<W in the original diagram.')
R(13,[N('Transferred charge',100*1.2e-3*3.2/13,'C','q=|NΔΦ|/R; reversal changesB by3.2T.')],'Time profile cancels on integrating Faraday law.')
R(14,[N('Loop resistance',8e-4*.009/.006,'Ω','q=AΔB/R; graph endpointB9mT,q6mC.')],'Source charge unit is mC; both linear plots span the same time.')
R(15,[N('a · Net emf magnitude',20+2*.870,'V','The changing field covers half the4m² square, giving1.74 V aiding the20 V battery.'),D('b · Net direction','Counterclockwise','The battery and induced emf both drive counterclockwise circulation.')],'The long positive battery plate is toward the right vertex; it drives counterclockwise current.')
R(16,[N('a · Induced current magnitude',.02*4e-6/2/.005,'A','Equal regions have slopes(1+.5−2.5)Bs/ts=−Bs/ts.'),D('b · Direction','Counterclockwise','Net outward flux decreases, so induced field is outward.')],'Original axis Bs=4.0μT and resistance5.0mΩ; read B₂ endpoint .5Bs.')
b0=mu*200/2
R(17,[N('a · Field magnitude at0',b0,'T','B=μ₀I/(2R).'),N('b · Field magnitude at.5s',0,'T','Current crosses zero.'),N('c · Field magnitude at1s',b0,'T','Current has equal reversed magnitude.'),C('d · Does B reverse?','Yes','No','Only its magnitude changes','The source current reverses.'),N('e · Emf at.5s',2e-4*mu/2*400,'V','A|dB/dt| remains nonzero whenB=0.')],'Emf depends on derivative, not instantaneous field magnitude.')
R(18,[N('a · Flux at3s',.350*(5.2*3)**2,'Wb','For90° rails, triangle area=(vt)².'),N('b · Emf at3s',2*.350*5.2**2*3,'V','Differentiate Bv²t².'),N('c · Exponent n',1,'dimensionless','Emf is proportional tot.',t=0)],'The bar moves along the angle bisector, so triangle base is2vt.')
R(19,[N('Maximum emf',100*.5*.3*3.5*(1000*2*pi/60),'V','ε₀=NABω.')],'Convert rev/min to radians per second.')
R(20,[N('Charge through meter',2*1000*pi*.1**2*.590e-4*sin(math.radians(70))/(85+140),'C','Flux flips sign; use verticalB=Bsin70° and total225Ω.')],'The charge is independent of the flip speed.')
R(21,[N('a · Frequency',40,'Hz','One sinusoidal cycle per revolution.'),N('b · Emf amplitude',.5*pi*.02**2*.020*2*pi*40,'V','Only a semicircle rotates, areaπa²/2.')],'The stationary resistor closes the loop.')
R(22,[N('Induced emf magnitude',.15*.20*.60,'V','|AB sinθ dθ/dt| atθ=π/2.')],'Angular speed is already in radians per second.')
R(23,[C('a · Flux as function of x','Φ=μ₀iπr²R²/[2(R²+x²)^(3/2)]','Φ=μ₀iπr²/(2x)','Φ=μ₀iπR²/(2r)','Use the axial field of the large loop times the small area.'),C('b · Emf magnitude','ε=3μ₀iπr²R²xv/[2(R²+x²)^(5/2)]','ε=μ₀iπr²v/(2x)','ε=0','Differentiate the axial-field factor withdx/dt=v.'),C('c · Small-loop sense viewed from above','Counterclockwise','Clockwise','None','The outward axial flux decreases as the loops separate.')],'Assume r small enough for uniform field over its area; source x≫R permits the corresponding far-field approximation.')
R(24,[N('a · Emf magnitude',pi*.1**2/4*.003,'V','Only the yz projected quadrant linksBx.'),C('b · Current in bc','From c to b','From b to c','No current','Increasing+x field induces a−x loop normal.')],'Projection onto the plane normal toB determines linked area.')
Dwire=.020;aw=.00125
fl=mu*10/pi*(.5+log(Dwire/aw));inside=mu*10/pi*(.5+log(Dwire/(Dwire-aw)))
R(25,[N('a · Flux per length for opposite currents',fl,'Wb/m','Integrate internal linearB and external1/r fields of both wires.'),N('b · Flux percentage inside wires',100*inside/fl,'%','Include both self-field and other-wire field inside each half-wire region.'),N('c · Net flux per length for parallel currents',0,'Wb/m','Fields oppose and their signed integrals cancel by midpoint symmetry.')],'Uniform current density within each wire; flux means the oriented net flux between central axes.')
R(26,[N('a · Emf magnitude',mu/(2*pi)*.16*17*log(.16/.12),'V','Top and bottom signed flux give bμ₀i ln(b/a)/(2π); di/dt=9t−10=17A/s.'),D('b · Direction','Counterclockwise','Net into-page flux grows.')],'The wire crosses the loop; do not add both area fluxes with the same sign.')
R(27,[N('a · Emf magnitude',8*2.5*.02**2*.03,'V','Integrate y over.02to.04m; |dΦ/dt|=8tAymid.'),D('b · Direction','Clockwise','Outward flux increases.')],'The square is above the x axis, not centered at the origin.')
r=.012;a=.022;b=.008
ph=mu*4.7*a/(2*pi)*log((r+b/2)/(r-b/2));em=mu*4.7*a/(2*pi)*.0032*(1/(r-b/2)-1/(r+b/2))
R(28,[N('a · Flux magnitude',ph,'Wb','Integrate μ₀i/(2πy) fromr−b/2tor+b/2.'),N('b · Induced current magnitude',em/.0004,'A','Differentiate flux as the loop translates; divide by.40mΩ.')],'The loop center, not its near edge, is at1.5b.')
em=.350*.25*.55
R(29,[N('a · Emf',em,'V','ε=BLv.'),N('b · Current',em/18,'A','i=ε/R.'),N('c · Thermal power',em*em/18,'W','P=ε²/R.')],'Mechanical power supplies Joule heating.')
em=mu*8000*pi*.02**2*.4
R(30,[N('Loop resistance',em*em/(80e-9/2),'Ω','Graph gives di/dt=.8A/2s and energy slope80nJ/2s; R=ε²/P.')],'Both graph endpoint values lie one grid interval below the scale-label maxima.')
l=.5;area=(l/(2*pi))**2*pi;res=1.69e-8*l/(pi*.001**2/4)
R(31,[N('Thermal power',(area*.010)**2/res,'W','P=(A dB/dt)²/R; R from copper resistivity and wire dimensions.')],'Use standard copperρ=1.69×10⁻⁸Ωm.',assumptions=['Copper resistivity1.69×10⁻⁸Ωm at approximately20°C.'])
R(32,[N('Thermal energy',(2e-4*17e-6)**2/(5.21e-6*.00296),'J','E=(AΔB)²/(RΔt).')],'Source units are17μT and5.21μΩ, not OCRmT/mΩ.')
em=mu*100*5/(2*pi)*log(.11/.01);I=em/.4
R(33,[N('a · Emf magnitude',em,'V','Integrate vB along rod froma toa+L.'),N('b · Current',I,'A','i=ε/R.'),N('c · Thermal power',I*I*.4,'W','i²R.'),N('d · Applied force magnitude',em*I/5,'N','Use Fv=εi.'),N('e · Mechanical power',em*I,'W','Equals Joule heat.')],'The field is nonuniform, so using one endpointB across the rod is incorrect.')
R(34,[C('Terminal speed','vₜ=mgR/(B²L²)','vₜ=mg/(BL)','vₜ=B²L²/(mgR)','At terminal speed mg=iLB andi=BLv/R.')],'Only the horizontal segment still in the field contributes the net vertical magnetic force.')
R(35,[N('a · Emf magnitude',.6,'V','BLv=.12×5.'),C('b · Emf direction','Up the rod','Down the rod','No emf','Leftward v crossed with outwardB points upward.'),N('c · Current',1.5,'A','ε/R.'),D('d · Loop current','Clockwise','Current climbs the left moving rod.'),N('e · Thermal power',.9,'W','i²R.'),N('f · Applied force magnitude',.18,'N','iLB, directed left to oppose magnetic drag.'),N('g · Work rate',.9,'W','Fv equals Joule heat.')],'Faraday law, Lorentz force, and energy conservation give consistent results.')
R(36,[N('a · Oriented integral path1',-.0085*pi*.2**2,'V','CCW path1 encloses into-page field whose signedB increases.'),N('b · Oriented integral path2',-.0085*pi*.3**2,'V','Clockwise path2 surrounds decreasing outwardB.'),N('c · Oriented integral path3',.0085*pi*(.3**2-.2**2),'V','CCW path3 encloses both signed flux changes.')],'Use the arrows shown on each path; the initial field magnitudes do not set dΦ/dt.')
R(37,[N('a · Electric field inside',.022*.0065/2,'N/C','E=r|dB/dt|/2.'),N('b · Electric field outside',.06**2*.0065/(2*.082),'N/C','E=R²|dB/dt|/(2r).')],'Outside the solenoid the enclosed flux saturates atπR²B.')
R(38,[N('Field slope a',2*300e-6/.02,'T/s','PeakE=300μN/C atR=.020m; E=aR/2.')],'Read the graph radius at the maximum, half ofrs=4cm.')
R(39,[N('Electric field amplitude',.016/2*.2*2*pi*15,'N/C','Field sinusoidal amplitude is(30.0−29.6)/2=.2T.')],'Use the amplitude, not the full peak-to-peak variation.')
R(40,[N('Flux per turn',.008*.005/400,'Wb','Φ=LI/N.')],'Distinguish flux per turn from total flux linkage.')
ph=2.6e-3*pi*.1**2
R(41,[N('a · External flux per turn',ph,'Wb','BA for each turn.'),N('b · Inductance',30*ph/3.8,'H','Self flux must cancel external flux:LI=NΦext.')],'Uniform external field penetrates all 30 turns.')
R(42,[N('a · Interior field',mu*.035/.16,'T','A one-turn solenoid has n=1/W.'),N('b · Inductance',mu*pi*.018**2/.16,'H','L=μ₀A/W.')],'The uniform sheet current approximates an ideal one-turn solenoid.')
R(43,[N('Inductance per length',mu/pi*log((.142-.00153)/.00153),'H/m','Integrate fields between inner wire surfaces, excluding internal flux.')],'The stated approximation neglects flux inside the wire metal.')
R(44,[N('Current-change rate magnitude',5,'A/s','|di/dt|=ε/L=60/12.')],'Either sign can produce the requested emf magnitude; source asks rate magnitude.')
R(45,[C('a · Current behavior','Decreasing','Increasing','Constant','Self-induced emf points with the rightward current, opposing its decrease.'),N('b · Inductance',17/25000,'H','L=ε/|di/dt|.')],'The diagram gives emf and current in the same direction.')
R(46,[N('a · Emf magnitude',4.6*7/.002,'V','Graph rises0to7A in2ms.'),N('b · Emf magnitude',4.6*2/.003,'V','Graph drops7to5A in3ms.'),N('c · Emf magnitude',4.6*5/.001,'V','Graph drops5to0A in1ms.')],'The8A axis label is above the actual7A peak; winding resistance does not alter Ldi/dt for the supplied current.')
R(47,[C('a · Equivalent inductance','L=L₁+L₂','1/L=1/L₁+1/L₂','L=L₁−L₂','Same current derivative passes through both and emfs add.'),C('b · N-inductor generalization','L=ΣLₙ','1/L=Σ(1/Lₙ)','L=ΠLₙ','Add all series self-induced voltage drops.')],'Mutual inductance is negligible by the stated separation.')
R(48,[C('a · Equivalent inductance','1/L=1/L₁+1/L₂','L=L₁+L₂','L=L₁−L₂','Parallel branches have equal emf and their current derivatives add.'),C('b · N-inductor generalization','1/L=Σ(1/Lₙ)','L=ΣLₙ','L=ΠLₙ','Sum branch derivative currents at a shared induced voltage.')],'No mutual coupling, as stated.')
R(49,[N('Equivalent inductance',(.03+.015+.05*.02/(.05+.02)),'H','L₁ andL₄ are in series with parallelL₂,L₃.')],'The two right branches share both junctions.')
R(50,[N('Time constant',-5/log(2/3),'s','1−exp(−5/τ)=1/3.')],'Solve the exponential buildup, not a linear ramp.')
R(51,[N('Resistance',10*log(100),'Ω','I/I₀=e^(−Rt/L)=.01.')],'10mA=.010A.')
R(52,[N('a · Emf magnitude ratio',1,'dimensionless','At closing all battery voltage is acrossL.'),N('b · Ratio at2τ',exp(-2),'dimensionless','εL/ε=e^(−t/τ) in magnitude.'),N('c · Time in τ units',log(2),'dimensionless','e^(−t/τ)=.5.')],'Ratios refer to emf magnitudes, not opposite signed loop-rule voltage.')
R(53,[N('a · Time to 80%',6.3e-6/1200*log(5),'s','t=−(L/R)ln(.2).'),N('b · Current atτ',14/1200*(1-exp(-1)),'A','I=(ε/R)(1−e⁻¹).')],'Original PDF inductance is6.30μH.')
R(54,[N('a · i₁ immediately closed',100/30,'A','Inductor branch initially open; R₁+R₂=30Ω.'),N('b · i₂ immediately closed',100/30,'A','Same series path.'),N('c · i₁ steady closed',100/(10+20*30/50),'A','R₂ andR₃ parallel at steady state.'),N('d · i₂ steady closed',(100/(10+12))*12/20,'A','Junction voltage divided byR₂.'),N('e · i₁ immediately reopened',0,'A','The open switch isolatesR₁.'),N('f · i₂ immediately reopened',-(100/(10+12))*12/30,'A','Inductor current remains continuous and returns upward throughR₂.'),N('g · i₁ long after reopening',0,'A','No source loop.'),N('h · i₂ long after reopening',0,'A','Stored energy has decayed.')],'Track the inductor current through the switching event and retain the indicated signs.')
R(55,[N('Time in τ units',log(1000),'dimensionless','Remaining deficit.001=e^(−t/τ).')],'0.100% less means99.900% of final current.')
L=25*4e-4/2
R(56,[N('Current slope at 1.5τ',16/L*exp(-1.5),'A/s','L=NΔΦ/Δi=.005H; di/dt=(ε/L)e^(−t/τ).')],'The graph is flux per turn, so multiply its slope by25.')
tblow=3*5/10
R(57,[N('a · Fuse time',tblow,'s','The ideal fuse shortsR before blowing, so iL=εt/L.'),C('b · Current graph','Linear rise to3A at1.5s, then exponential fall toward2/3A','Exponential rise from0 toward2/3A at all times','Instantaneous jump from3A tozero at1.5s','After the fuse opens, iL is continuous and relaxes withτ=L/R.')],'The fuse branch initially bypasses the resistor; the standard series buildup equation does not apply before opening.')
R(58,[C('Battery emf as function of t','ε(t)=42+20t V','ε(t)=12+20t V','ε(t)=30 V','ε=Ri+Ldi/dt=4(3+5t)+6(5).')],'Both resistive and inductive voltage drops are required.')
R(59,[C('a · Inductor current','iL=i[1−exp(−Rt/L)]','iL=i exp(−Rt/L)','iL=itR/L for all times','Current-source constraint givesiR=i−iL andLdiL/dt=RiR.'),C('b · Equal branch-current time','t=(L/R)ln2','t=L/R','t=2L/R','Both branches then carryi/2.')],'The external source holds total current fixed rather than voltage.')
Nturn=2*pi*.10/.001;L=mu*Nturn**2*.02/(2*pi)*log(.12/.10);wirelen=Nturn*.08;res=.020*wirelen
R(60,[N('a · Inductance',L,'H','Single-layer turn count is2πrinner/dwire; toroidalL=μ₀N²h ln(b/a)/(2π).'),N('b · Time constant',L/res,'s','Each turn length is approximately4×2cm=.08m; R=.020Ω/m times total wire length.')],'Neglect insulation and wire thickness as instructed; inner circumference sets the closest-packed turn count.')
L=-10000*.005/log(.6)
R(61,[N('a · Inductance',L,'H','2mA/5mA=1−e^(−.005R/L).'),N('b · Stored energy',.5*L*.002**2,'J','U=LI²/2 at the stated current.')],'Assume negligible coil resistance beyond the stated series resistor.')
I=10*(1-exp(-.5));slope=50*exp(-.5)
R(62,[N('a · Magnetic-energy rate',2*I*slope,'W','dU/dt=LI di/dt.'),N('b · Thermal power',I*I*10,'W','I²R.'),N('c · Battery power',100*I,'W','εI equals magnetic plus thermal power.')],'Useτ=.2s; evaluate at.1s.')
R(63,[N('Time',.037*log(2),'s','RI²=LI di/dt requiresI=I∞/2.')],'The power rates, not energies, become equal atτln2.')
R(64,[N('Time in τ units',-log(1-1/sqrt(2)),'dimensionless','Stored energy fraction is(1−e^(−t/τ))².')],'Half the final energy means1/√2 of final current.')
Rr=6.7;L=5.5;V=10;t=2;tau=L/Rr;I=V/Rr*(1-exp(-t/tau));Eb=V*V/Rr*(t-tau*(1-exp(-t/tau)));U=.5*L*I*I
R(65,[N('a · Battery energy',Eb,'J','Integrate εI(t) from0to2s.'),N('b · Magnetic energy',U,'J','LI(2)²/2.'),N('c · Dissipated energy',Eb-U,'J','Battery input minus stored field energy.')],'The first-law balance exactly partitions the delivered energy.')
B=mu*100/(2*.05)
R(66,[N('a · Center field',B,'T','B=μ₀I/(2r).'),N('b · Energy density',B*B/(2*mu),'J/m³','u=B²/(2μ₀).')],'50mm=.050m.')
B=mu*950/.85*6.6;u=B*B/(2*mu)
R(67,[N('a · Energy density',u,'J/m³','Use n=N/l inB=μ₀nI.'),N('b · Total field energy',u*.85*.0017,'J','Multiply by interiorvolumeAl.')],'Neglect solenoid end effects as stated.')
R(68,[N('Current',sqrt(2*70*.02/.09),'A','LI²/2=uV.')],'Magnetic volume and average density determine total energy.')
R(69,[N('Electric field magnitude',.5/sqrt(mu*eps),'N/C','Set ε₀E²/2=B²/(2μ₀).')],'This is E=cB for equal field energy densities.')
B=sqrt(2*mu*1.96e-9);i1=B*(.2/3)/(mu/(2*pi))
R(70,[N('a · Wire1 current',i1,'A','Graph cancellation atx=.20m andi₂=3i₁ puts wire1at−.0667m; asymptote setsB₁.'),N('b · Wire2 current',3*i1,'A','Use stated current ratio1/3.')],'The asymptotic energy density determines the fixed-wire field, and the zero determines its distance.')
B=mu*10/(2*pi*.00125);E=10*.0033
R(71,[N('a · Magnetic energy density',B*B/(2*mu),'J/m³','SurfaceB=μ₀I/(2πr).'),N('b · Electric energy density',eps*E*E/2,'J/m³','AxialE=I(R/length).')],'Convert3.3Ω/km to.0033Ω/m.')
R(72,[N('a · Self flux per turn in1',.025*.006/100,'Wb','Φ₁₁=L₁I₁/N₁.'),N('b · Self-emf magnitude in1',.025*4,'V','L₁|di₁/dt|.'),N('c · Mutual flux per turn in2',.003*.006/200,'Wb','Φ₂₁=MI₁/N₂.'),N('d · Mutual-emf magnitude in2',.003*4,'V','M|di₁/dt|.')],'Flux per turn differs from flux linkage by the receiving turn count.')
R(73,[N('a · Mutual inductance',.025/15,'H','M=|ε₁|/|di₂/dt|.'),N('b · Flux linkage in2',(.025/15)*3.6,'Wb','N₂Φ₂=MI₁; mutual inductance is reciprocal.')],'Partb explicitly requests linkage rather than flux per turn.')
R(74,[N('Mutual inductance',30000/(6/.0025),'H','M=ε/|ΔI/Δt|.')],'The rapid primary-current collapse produces the large secondary voltage.')
R(75,[N('Mutual inductance',100*mu*.3/(2*pi)*log(.09/.01),'H','M=Nμ₀l ln((a+b)/a)/(2π).')],'Integrate the nonuniform straight-wire field over rectangular turns.')
R(76,[C('a · Mutual inductance','M=μ₀πR²nN','M=μ₀πR²n/N','M=μ₀nNR','Each receiving turn links the solenoid fluxμ₀niπR².'),C('b · Independence of receiving-coil geometry','Every turn encloses all the confined solenoid flux','The field outside the solenoid grows to compensate','Mutual inductance never depends on coil geometry','The ideal-solenoid field vanishes outside and the entire interior is enclosed.')],'AllNturns encircle the ideal long solenoid.')
R(77,[C('a · Aiding equivalent inductance','L=L₁+L₂+2M','L=L₁+L₂','L=L₁+L₂−2M','Both self and reciprocal mutual emfs add.'),C('b · How to obtain opposing connection','Reverse the leads of one coil','Reverse both coils together','Increase separation without changing leads','Reversing one current direction changes both mutual cross terms to−M.')],'The source drawing shows series-aiding magnetic fields.')
R(78,[N('Coil resistance',-.023/.00015*log(280/(12/.023)),'Ω','di/dt=(ε/L)e^(−Rt/L).')],'The measured derivative directly determines the exponential decay factor.')
R(79,[N('a · Initial i₁',2,'A','OnlyR₁ conducts initially.'),N('b · Initial i₂',0,'A','Inductor current cannot jump.'),N('c · Initial switch current',2,'A','Sum branch currents.'),N('d · Initial V₂',0,'V','No current inR₂.'),N('e · Initial VL magnitude',10,'V','Full battery voltage initially acrossL.'),N('f · Initial di₂/dt',2,'A/s','ε/L.'),N('g · Steady i₁',2,'A','R₁ remains directly across battery.'),N('h · Steady i₂',1,'A','Inductor shorts; branch resistanceR₂.'),N('i · Steady switch current',3,'A','2+1.'),N('j · Steady V₂',10,'V','R₂ spans battery.'),N('k · Steady VL',0,'V','Constant current.'),N('l · Steady di₂/dt',0,'A/s','No continuing buildup.')],'R₁ is parallel with the seriesL–R₂ branch.')
R(80,[N('Time to 2mA',-8e-6/4000*log(1-.002/(20/4000)),'s','I∞=5mA,τ=L/R.')],'Original inductance8.0μH gives a nanosecond-scale time.')
R(81,[N('a · Field 1 magnitude',3e-6*.020/(.015*.4),'T','Entering-loopi=BHv/R.'),C('b · Field 1 direction','Out of the page','Into the page','Parallel to the page','Clockwise inducedcurrent opposes increasing outward flux.'),N('c · Field 2 magnitude',1e-6*.020/(.015*.4),'T','At the boundary i=(B₂−B₁)Hv/R=−2μA; hence B₂=B₁/3.'),C('d · Field 2 direction','Out of the page','Into the page','Parallel to the page','At the shared boundary the outward field drops from B₁ to B₁/3, giving counterclockwise current.')],'The graph scale is3.0μA. The negative pulse is crossing the boundary between the adjacent regions, not entering an initially field-free second region.')
R(82,[C('Emf magnitude versus time','ε=(πr²B₀/τ)exp(−t/τ)','ε=πr²B₀exp(−t/τ)','ε=(πr²B₀τ)exp(−t/τ)','Differentiate the decaying normal flux.')],'The circulation sense depends on the unspecified field orientation; the magnitude is unique.')
R(83,[N('Equal-voltage time',.015/20*log(2),'s','εe^(−t/τ)=ε(1−e^(−t/τ)).')],'τ=.75ms.')
R(84,[N('a · dB₁/dt',8e-9/(pi*1e-4),'T/s','Inner slope8nV percm² divided byπ.'),N('b · dB₂/dt',4e-9/(pi*1e-4),'T/s','Outer slope(20−8)/(4−1)=4nV percm² divided byπ.'),C('c · Field 2 magnitude','Increasing','Decreasing','Constant','The outer-annulus slope has the same sign as the increasing outward inner field.')],'The horizontal variable is radius squared; divide the emf slope byπ, not by the radius.')
a=e*.05*.010/(2*me)
R(85,[N('a · x acceleration at a',-a,'m/s²','Decreasing inwardB induces clockwiseE; atbottomEpointsleft, electron accelerationright? See signed vector check.'),N('a · y acceleration at a',0,'m/s²','Tangential field is horizontal.'),N('b · x acceleration at center',0,'m/s²','InducedE vanishes ataxis.'),N('b · y acceleration at center',0,'m/s²','Same symmetry.'),N('c · x acceleration at c',a,'m/s²','At top the electron acceleration is opposite the clockwise electric field.'),N('c · y acceleration at c',0,'m/s²','Tangential direction is horizontal.')],'Initially v=0, so magnetic force vanishes; acceleration isqE/m.')
R(86,[N('Equal-flux time',log(1.5)/(30/.003-25/.005),'s','Φ₂/Φ₁=1.5exp[−(R₂/L₂−R₁/L₁)t].')],'Fluxes per turn decay with their respectiveRLtime constants.')
R(87,[N('a · Average emf',2*.2**2/.2,'V','Average|ε|=BΔA/Δt.'),N('b · Average current',2*.2**2/.2/.020,'A','AverageI=averageε/R.')],'No detailed pull trajectory is needed for the integrated flux change.')
L=150*50e-9/.002
R(88,[N('a · Inductance at 2mA',L,'H','L=NΦ/I.'),N('b · Inductance at 4mA',L,'H','Linear coil inductance is independent of current.'),N('c · Flux per turn at 4mA',100e-9,'Wb','Flux doubles with current.'),N('d · Maximum emf',L*.003*377,'V','LωI₀.')],'The coil is assumed linear with no changing magnetic material properties.')
R(89,[N('a · Equilibrium current',10,'A','ε/R.'),N('b · Stored energy',100,'J','LI²/2.')],'At equilibrium the ideal inductance has no voltage drop.')
R(90,[N('Decay time',2/3*log(10),'s','VR(t)/VR(0)=e^(−Rt/L).')],'Voltage and current share the same decay time constant.')
req=20000*20/(20000+20);tau=.05/req;ii=40/req
R(91,[N('a · Initial battery current',0,'A','Inductor initially blocks its series path.'),N('b · Initial slope',800,'A/s','ε/L.'),N('c · Battery current at 3ms',ii*(1-exp(-.003/tau)),'A','Use R₁∥R₂ behind the series inductor.'),N('d · Slope at 3ms',800*exp(-.003/tau),'A/s','Differentiate the exponential.'),N('e · Steady current',ii,'A','ε/(R₁∥R₂).'),N('f · Steady slope',0,'A/s','Current is constant.')],'The top inductor is in series with both parallel resistors.')
L=.026/5.5
R(92,[N('a · Inductance',L,'H','L=fluxlinkage/I.'),N('b · Time to 2.5A',-L/.75*log(1-2.5/(6/.75)),'s','I∞=8A andτ=L/R.')],'Flux linkage already includes turn count.')
x=exp(-1.61)
R(93,[N('Magnetic-energy transfer rate',12**2/20*x*(1-x),'W','LI di/dt=(ε²/R)e^(−t/τ)(1−e^(−t/τ)).')],'The rate is independent ofLwhen time is specified inτunits.')
Lper=mu*10000**2*pi*.016**2
R(94,[N('a · Inductance per length',Lper,'H/m','L/l=μ₀n²A.'),N('b · Induced emf per length',Lper*13,'V/m','(L/l)|di/dt|.')],'100turns/cm=10000turns/m.')
R(95,[N('a · Initial slope inL₁',6/.3,'A/s','InitialL₂branch blocks; zero initialcurrent giveszeroresistordrops, all6VacrossL₁.'),N('b · Steady current inL₁',6/8,'A','L₂shortsR₂ atsteady state; onlyR₁ remains.')],'Apply inductor continuity separately to both inductors.')
R(96,[N('Induced emf magnitude',.24*2*.12*.05,'V','|dΦ/dt|=2Bl|dl/dt|.')],'Both side dimensions shrink, so the factor2isrequired.')
R(97,[N('Current slope at 1.2ms',45/.05*exp(-180*.0012/.05),'A/s','di/dt=(ε/L)e^(−Rt/L).')],'UseL50mH=.050H.')
L=.003/5
R(98,[N('a · Inductance',L,'H','L=ε/|di/dt|.'),N('b · Number of turns',L*8/40e-6,'turns','N=LI/Φperturn.',t=0)],'Original flux unit is40.0μWb.')
R(99,[N('Stored magnetic energy',(1e-10)**2/(2*mu)*(10*9.46e15)**3,'J','u=B²/(2μ₀), volume=(10lightyears)³.')],'Use1lightyear=9.46×10¹⁵m.',assumptions=['Uniform stated field throughout cube; lightyear9.46×10¹⁵m.'])
r=.24;rho=1.7e-8;A=1.2e-6;alpha=12;B=.15;coef=rho*r/A
R(100,[C('a · Resistance as function of θ','R=.0034(2+θ) Ω','R=.0034θ Ω','R=.0034(1+θ²) Ω','Two radial wires add2r and the arc addsrθ.'),C('b · Flux as function of θ','Φ=.00432θ Wb','Φ=.00864θ Wb','Φ=.00432θ² Wb','Sector area r²θ/2.'),N('c · Maximizing angle',2,'rad','I∝√θ/(2+θ); derivativezeroatθ=2.'),N('d · Maximum current',(.5*B*r*r*sqrt(2*alpha*2))/(coef*4),'A','Useω²=2αθ andε=Br²ω/2.')],'Both changing resistance and changing angular speed enter the optimization.')
R(101,[N('Flux through toroid cross section',mu*500*.8*.05/(2*pi)*log(.20/.15),'Wb','Integrate μ₀NIh/(2πr) frominner toouter radius.')],'Field is not uniform across the finite toroidal width.')
# Conceptual questions, independently derived from diagrams.
R(1,[C('Magnetic field direction','Out of the page','Into the page','Parallel to the page','Expansion increases outward flux; clockwise current creates an opposing inward field.')],'Lenz law fixes the external field sign.',kind='questions')
R(2,[C('Clockwise-first emf ranking','1 = 3 > 2 = 5 > 4 = 6','4 = 6 > 2 = 5 > 1 = 3','1 > 2 > 3 > 4 > 5 > 6','Signed emf follows dBz/dt, notBz itself.')],'Positive Bz slopes induce clockwise circulation.',kind='questions')
R(3,[C('a · Constant source current','1 = 2 = 3, all zero','2 > 1 = 3','1 > 2 > 3','Static current means static flux.'),C('b · Increasing source current','2 > 1 = 3','1 = 2 = 3','1 > 3 > 2','Symmetric loops 1 and 3 have canceling flux; off-center loop 2 does not.')],'Net oriented flux determines induction, not local field magnitude.',kind='questions')
R(4,[C('a · Field direction','Into the page','Out of the page','Along the bar','Circuit1bar movesup, reducing area; CCW inducedfieldoutwardopposesdecreasinginwardflux? RecheckLenzgeometry.'),D('b · Circuit 2 current','Clockwise','Circuit2area increases in the same inwardfield, inducingoutwardfield.'),C('c · Circuit 1 emf versus 2','Larger, by a factor2','The same','Smaller, by a factor2','ε=Blv and bar 1 has double length.')],'Account for opposite area changes as the bars move.',kind='questions')
R(5,[C('Integral-magnitude ranking','c = d > b > a','d > c > a > b','a = b = c = d','Only changing enclosed flux matters; outer paths c and d enclose all the field.')],'Leader a ends on the innermost circle; b ends on the next larger circle. Both lie inside the field region, whereas c and d enclose its entire changing flux.',kind='questions')
R(6,[C('a · Work per charge ranking','2 > 1 > 3','1 > 2 > 3','3 > 1 > 2','Projected areas are r²,πr²/4,r²/2 for changing x, z and y components.'),C('b · Current ranking','2 > 1 > 3','1 > 2 > 3','All equal','Same wire resistance for every field choice.'),C('c1 · Choice 1 current','a → b → c → a','a → c → b → a','None','Decreasing +z field requires a +z induced normal.'),C('c2 · Choice 2 current','a → c → b → a','a → b → c → a','None','Increasing +x field requires a −x induced normal.'),C('c3 · Choice 3 current','a → b → c → a','a → c → b → a','None','Decreasing +y field requires a +y induced normal.')],'Use the three projected enclosed areas of the nonplanar loop.',kind='questions')
R(7,[C('a · Central resistor current just closed','Greater','Less','The same','Inductor branch is initially open.'),C('b · Long after closing','The same','Greater','Less','Ideal inductor shorts; identical resistors span the battery.'),C('c · Just reopened','The same','Greater','Less','Remaining resistors are in series with the inductor.'),C('d · Long after reopening','The same, both zero','Central is greater','Central is less','Stored energy fully decays.')],'Inductor current is continuous at switching, and the decay loop has only one series current.',kind='questions')
R(8,[C('Set 1 curve','c','a','d','High initial current and τ=L₀/R₀.'),C('Set 2 curve','a','b','c','Half the initial current and half the time constant.'),C('Set 3 curve','d','a','b','High initial current and doubletime constant.'),C('Set 4 curve','b','c','d','Half the initial current and original time constant.')],'Initial current is set by ε/R; decay time is L/R.',kind='questions')
R(9,[C('a · Steady closed ranking','1 = 2 = 3, all zero','1 = 2 > 3','3 > 1 = 2','Inductors short the parallel resistor branches.'),C('b · Immediately reopened ranking','1 = 2 > 3','1 = 2 = 3','3 > 1 = 2','The same inductor current returns through one resistor in 1 and 2, but splits between parallel resistors in 3.'),C('c · Long after reopening','1 = 2 = 3, all zero','1 > 2 > 3','3 > 2 > 1','All currents decay to zero.')],'The series battery resistor sets identical initial inductor currents.',kind='questions')
R(10,[C('Inductance ranking','c > b > a','a > b > c','All equal','Slower resistor-voltage buildup means larger τ=L/R.')],'Same resistance and battery voltage, different inductance.',kind='questions')
R(11,[C('Induced and battery emfs agree','Only b','Only a and b','All three','Use battery polarity and Lenz direction in each shaded field region.')],'Increasingoutward flux inducesCW; decreasingoutwardCCW; decreasinginwardCW.',kind='questions')
R(12,[C('a · Required-force ranking','1 > 2 > 4 > 3','1 = 2 > 3 = 4','2 > 1 > 3 > 4','F=B²h²v/R; identical wire gauge gives resistance proportional to perimeter.'),C('b · Mechanical-power ranking','1 > 2 > 4 > 3','1 = 2 > 3 = 4','4 > 3 > 2 > 1','P=Fv andthe same speed for all.')],'Loop heights are 2L, 2L, L, L and perimeters are 6L, 8L, 6L, 4L respectively.',kind='questions',assumptions=['All loops are made from the same wire material and cross section, as implied by the comparative diagram.'])
r=next(x for x in rows if x['id']=='physics-chapter-30-problems-91')
r['reviewNotice']='The printed answer key conflicts with the supplied values R₁=20 kΩ, R₂=20 Ω and L=50 mH. These checks use the stated parallel-resistor circuit, giving a final battery current of 2.002 A.'
r['referenceAnswer']='(a)0 A; (b)800 A/s; (c)1.39829 A; (d)241.244 A/s; (e)2.002 A; (f)0 A/s.'
r=next(x for x in rows if x['id']=='physics-chapter-30-problems-99')
r['parts'][0]['acceptedValues']=[3e36]
# Fix clear signed-direction conclusions after vector checks.
r=next(x for x in rows if x['id']=='physics-chapter-30-problems-85')
r['parts'][0]['answer']=a;r['parts'][0]['explanation']='At the bottom a clockwise induced electric field points left, so the negative electron accelerates right.'
r['parts'][4]['answer']=-a;r['parts'][4]['explanation']='At the top clockwise electric field points right, so the negative electron accelerates left.'
r=next(x for x in rows if x['id']=='physics-chapter-30-questions-4')
r['parts'][0]['answer']='Into the page';r['parts'][0]['options']=['Into the page','Out of the page','Along the bar'];r['parts'][0]['explanation']='The fixed U base is below the moving bar: upward motion increases area. Counterclockwise induced field points outward, opposing increasing inward external flux.'
r['parts'][1]['answer']='Counterclockwise';r['parts'][1]['options']=['Counterclockwise','Clockwise','None']
r['parts'][1]['explanation']='The fixed U base is on the left: rightward motion also increases area in the inward field, so induced current is counterclockwise.'
r['reasoning']='Both moving bars increase enclosed area; increasing inward flux is opposed by counterclockwise current. The doubled bar length in circuit1 doubles emf. Verification: inspected the fixed U bases in the high-resolution source, not merely the velocity arrows.'
assert len(rows)==113 and len({r['id'] for r in rows})==113
source=json.loads(gzip.decompress((ROOT/'site/questions/physics.json.gz').read_bytes()));assert {r['id'] for r in rows}=={q['id'] for q in source if q['chapter']==30}
for r in rows:
 for p in r['parts']:
  assert p['type']in['numeric','choice']
  if p['type']=='numeric':assert math.isfinite(p['answer']) and(p['answer']==0 or p['tolerance']<abs(p['answer']))
  else:assert len(set(p['options']))==3 and p['answer']in p['options']
(HERE/'ch30.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'records',sum(len(r['parts'])for r in rows),'fields')
