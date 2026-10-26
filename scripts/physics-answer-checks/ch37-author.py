#!/usr/bin/env python3
"""Original source-derived relativity answer checks, PDF29–37 visually reviewed."""
import math,json,pathlib,gzip,subprocess,re
from math import sqrt,pi,log,atanh,tanh,sin,cos
H=pathlib.Path(__file__).resolve().parent;ROOT=H.parents[1]
c=299792458.;e=1.602176634e-19;me=9.10938188e-31;mp=1.672621777e-27;u=1.660538921e-27;year=365.25*86400;MeV=1e6*e;Ee=me*c*c/MeV;Ep=mp*c*c/MeV;uc2=u*c*c/MeV;rows=[]
def gam(b):return 1/sqrt((1-b)*(1+b))
def beta(g):return sqrt((g-1)*(g+1))/g
def add(a,b):return (a+b)/(1+a*b)
def N(l,a,un,w,t=None):return dict(label=l,type='numeric',answer=a,unit=un,tolerance=max(abs(a)*.006,1e-35) if t is None else t,explanation=w)
def B(l,a,w):
 p=N(l,a,'dimensionless',w,min(1e-8,max(1e-35,abs(a)*.001),max(1e-35,(1-abs(a))*.02)));p['noRounding']=True;p['acceptedValues']=[v for v in [float(format(a,'.2g')),float(format(a,'.3g'))] if abs(v)<1] if abs(a)<1 else [];return p

def C(l,a,b,d,w):return dict(label=l,type='choice',answer=a,options=[a,b,d],explanation=w)
def R(n,p,w,kind='problems',assumptions=None,scope=None,pages=None):
 page=30 if n<=8 else 31 if n<=20 else 32 if n<=37 else 33 if n<=56 else 34 if n<=64 else 35 if n<=74 else 36 if n<=91 else 37
 if kind=='questions':page=29 if n<=7 else 30
 r=dict(id=f'physics-chapter-37-{kind}-{n}',parts=p,reasoning=w+' Verification: independently substitute the source values into the Lorentz transformation, invariant interval or energy-momentum identity as applicable; original diagram axes and units checked.',sourcePages=pages or [page],assumptions=assumptions or ['Special relativity in inertial frames; instantaneous turnarounds idealized when required. c=299792458 m/s; explicit source rest energies override rounded constants.'])
 if scope:r['scope']=scope
 rows.append(r)
# Problems 1–15: proper times and proper lengths.
R(1,[B('Speed parameter β',beta(16/2.2),'γ=τlab/τproper=16.000/2.2000; β=√(1−γ⁻²).')],'Both source lifetimes are microseconds; their ratio is unit-independent.')
R(2,[B(f'{l} · Speed parameter β',beta(g),'Invert γ=1/√(1−β²), evaluating β=√[(γ−1)(γ+1)]/γ.') for l,g in zip('abcd',[1.0100000,10,100,1000])],'The near-light values remain below1; β=1 is never an accepted massive-particle answer.')
R(3,[B('a · Speed parameter β',beta(1000),'Earth time1000y divided by ship proper time1y gives γ1000.'),C('b · Must the path be straight?','No; the total proper time depends on speed history, not direction','Yes; dilation exists only along a straight line','No motion is needed','At the same speed, each segment contributes dt/γ; idealized changes of direction do not alter the accumulated ratio.')],'Six months outward and six months back total one ship year.')
R(4,[B('Speed parameter β',beta(11),'The father ages4y; the daughter must age44y, changing a20y lead to a20y lag. γ=44/4=11.')],'Initial age difference plus the two elapsed ages fixes the required dilation.')
R(5,[N('Proper lifetime',.00105/(.992*c*gam(.992)),'s','Lab duration=L/v; divide byγ to obtain time on the particle worldline.')],'The track is1.05mm in the detector frame.')
R(6,[N('Dilated interval at0.98c',8*gam(.98),'s','Graph intercept atβ0 is proper interval8.0s; multiply byγ(.98).',1.0)],'The graph uses Δta14s at the top; the zero-speed intercept is8s, not14s.')
R(7,[N('Elapsed Earth time',120*gam(.999),'y','Earth interval=γ×120y.')],'The120y hibernation interval is the astronauts’ proper time for the full outward-and-return trip.')
R(8,[N('Tube length in electron frame',3/gam(.999987),'m','The tube has proper length3m and contracts by1/γ.')],'The electron is at rest in the primed frame.')
R(9,[N('a · Ship length at station',130/gam(.74),'m','L=L0/γ.'),N('b · Station passage interval',(130/gam(.74))/(.74*c),'s','A single station clock measures contracted length divided by ship speed.')],'Both endpoints pass one stationary timing clock.')
R(10,[N('Stick length',sqrt(cos(pi/6)**2/gam(.9)**2+sin(pi/6)**2),'m','Only the x component contracts: L²=(L0cos30°/γ)²+(L0sin30°)².')],'The transverse half-meter component is unchanged.')
R(11,[N('Measured length',1.70/gam(.63),'m','L=L0√(1−β²).')],'The rod is parallel to motion.')
R(12,[B('a · Speed parameter β',sqrt(3)/2,'L/L0=1/2 gives γ2.'),N('b · Clock slowing factor',2,'dimensionless','Moving-clock duration is smaller by factorγ=2.')],'Distinguish the factor2 from the rate ratio1/2.')
R(13,[N('a · Earth time to arrival',26/.99,'y','Travel time=26ly/(.99c).'),N('b · Earth time until message',26/.99+26,'y','Add26y for the light signal from Vega.'),N('c · Traveler age increase',26/.99/gam(.99),'y','Proper duration is Earth travel time divided byγ.')],'Message travel time is not part of the traveler’s arrival age.')
R(14,[N('Length at0.95c',.8/gam(.95),'m','Graph zero-speed intercept L0=.80m; apply contraction.',.006)],'The graph top scale La1m is not the rest length.')
g=sqrt(1+(23000/30)**2);b=beta(g)
R(15,[B('a · Speed parameter β',b,'D/(cτ)=βγ=23000/30, hence γ=√[1+(D/cτ)²].'),N('b · Contracted galaxy segment',23000/g,'ly','D′=D/γ=βcτ.')],'Use the traveler’s30y as proper time.')
# Lorentz transformations, graph conclusions and velocity composition.
b=.4;g=gam(b);x=3e8;t=2.5
R(16,[N('a · x prime, moving+x',g*(x-b*c*t),'m','x′=γ(x−vt).'),N('b · t prime, moving+x',g*(t-b*x/c),'s','t′=γ(t−vx/c²).'),N('c · x prime, moving−x',g*(x+b*c*t),'m','Change the sign ofv.'),N('d · t prime, moving−x',g*(t+b*x/c),'s','Change the sign ofv.')],'Common origins are synchronized at0.')
R(17,[N('a · Collision x prime',gam(.95)*(1e5-.95*c*200e-6),'m','Transform x100km andt200μs.'),N('b · Collision t prime',gam(.95)*(200e-6-.95*1e5/c),'s','t′=γ(t−βx/c).')],'The original source is200μs, not200ms.')
R(18,[N('a · Event1 t prime',0,'s','The origin event remains the origin.'),N('b · Event2 t prime',gam(.6)*(4e-6-.6*3000/c),'s','Transform3.0km and4.0μs.'),C('c · Event order','Reversed: event2 occurs first in S prime','The same: event1 occurs first','Simultaneous in both frames','The transformed event2 time is negative.')],'These events are spacelike, so their order need not be invariant.')
R(19,[N('a · Temporal separation magnitude',gam(.25)*.25*30000/c,'s','The signed small-minus-big interval is negative; the requested separation magnitude is its absolute value.'),C('b · First flash in moving frame','Small flash','Big flash','They remain simultaneous','The farther+x event has negative transformed time.')],'The requested interval is signed small-minus-big; its magnitude is the positive separation.')
slope=(6-2)*1e-6/400;g=sqrt(1+(slope*c)**2)
R(20,[N('Primed temporal separation',2e-6/g,'s','Δt=γΔt′+(γβ/c)Δx′; graph intercept2μs and slope.01μs/m fixγ.')],'The original vertical scale is6μs; use both slope and intercept.',pages=[31])
b0=c*1e-6/400
R(21,[C('a · Temporal transformation','Δt′=γ(Δt−βΔx/c)','Δt′=γ(Δt+βΔx/c)','Δt′=Δt/γ for all spatial separations','The events occur at different coordinates; the relativity-of-simultaneity term is essential.'),C('b · Low-speed graph','Decreases nearly linearly from1.00μs','Increases from1.00μs','Remains exactly constant','For smallβ, γ≈1 and the first derivative is−Δx/c.'),C('c · High-speed graph','Decreases through zero and tends to negative infinity','Remains positive and tends to positive infinity','Turns positive beforeβ1','The spacelike interval allows order reversal.'),B('d · β at simultaneous events',b0,'Set Δt−βΔx/c=0.'),C('e · Same event order','0≤β<0.74948 approximately','0.74948<β<1','All allowedβ','Below the zero crossing, Δt′ remains positive.'),C('f · Reversed event order','0.74948<β<1','0≤β<0.74948 approximately','No allowedβ','Above the crossing, Δt′ is negative.'),C('g · Can either event cause the other?','No; the separation is spacelike','Yes; order reversal allows backward causation','Yes; any two events can be causal','400m exceeds c×1μs≈300m.')],'Graph features are checked through their slope, crossing and limiting behavior; drawing itself is not graded.',pages=[31,32])
bmin=c*1e-6/400
R(22,[C('a · Spatial transformation','Δx′=γ(Δx−βcΔt)','Δx′=γ(Δx+βcΔt)','Δx′=Δx/γ for arbitrary events','Transform the complete event separation.'),C('b · Low-speed graph','Initially decreases almost linearly','Initially increases','Identically zero','Derivative atβ0 equals−cΔt.'),C('c · High-speed graph','Falls to a positive minimum then rises without bound','Crosses zero and becomes negative','Decreases monotonically to zero','The invariant spacelike distance is a lower bound.'),B('d · β at minimum',bmin,'Differentiate γ(Δx−βcΔt); βmin=cΔt/Δx.'),N('e · Minimum spatial separation',sqrt(400**2-(c*1e-6)**2),'m','At simultaneous primed events, Δx′=√(Δx²−c²Δt²).')],'The minimum is positive because the interval is spacelike.')
R(23,[N('a · Lorentz factor',gam(.6),'dimensionless','γ=1/√(1−.6²).'),N('b · Moving clock reading',180/(.6*c*gam(.6)),'s','Lab duration=180/v; clock proper duration=lab duration/γ.')],'The same moving clock measures the proper interval.')
b=sqrt(3)/2;g=2
R(24,[N('a · Longitudinal meter stick',.5,'m','γ=30/15=2.'),N('b · y meter stick',1,'m','Transverse lengths do not contract.'),N('c · z meter stick',1,'m','Transverse lengths do not contract.'),N('d · Spatial separation',g*(20-b*c*40e-9),'m','Δx′=γ(20m−v×40ns).'),N('e · Temporal separation',g*(40e-9-b*20/c),'s','Δt′=γ(40ns−β20m/c).'),C('f · Event first','Event2','Event1','Simultaneous','The transformed temporal separation is negative.')],'Time dilation fixesγ before the event coordinates are transformed.')
v=-720/5e-6;b=v/c
R(25,[B('a · Speed parameter magnitude β',abs(b),'For coincident primed positions, v=Δx/Δt=−720m/5μs; the speed parameter is the magnitude.'),C('b · S prime motion','Negative x','Positive x','At rest','The small flash is at a smaller x but later time.'),C('c · Flash first','Big flash','Small flash','Simultaneous','These events are timelike; order cannot reverse.'),N('d · Proper time separation',5e-6/gam(b),'s','Coincident primed positions make Δt′ the proper interval.')],'The source interval is5.00μs.')
R(26,[N('Limiting minimum interval',720/c,'s','A coincident-position frame requires |Δx/Δt|<c, so Δt>720/c.'),C('Can the limiting value be attained by an inertial observer?','No; it would require speed c','Yes; atβ1','Yes; atβ0','The quoted threshold is an infimum, not an attained minimum for a massive observer.')],'The lower limit is2.402μs; every allowed same-place observer requires a strictly greater interval.')
R(27,[B('Particle velocity divided by c',add(.4,.6),'u=(u′+v)/(1+u′v/c²).')],'Both velocities are along+x.')
R(28,[B('a · Relativistic u/c',add(.47,.62),'Compose.47and.62.'),N('b · Classical u/c',1.09,'dimensionless','Galilean addition gives.47+.62; its superluminal result signals failure.'),B('c · Relativistic u/c',add(-.47,.62),'Compose−.47and.62.'),N('d · Classical u/c',.15,'dimensionless','Galilean addition gives−.47+.62.')],'Relativistic composition stays belowc.')
R(29,[B('a · Our galaxy recession speed/c',.35,'A sees us receding at its own relative speed.'),B('b · GalaxyB recession speed/c',add(.35,.35),'The galaxies move in opposite directions in our frame.')],'Velocity addition is symmetric for collinear relative speeds.')
R(30,[B('Q2 speed relativeQ1 divided byc',abs((.4-.8)/(1-.4*.8)),'u′=(u−v)/(1−uv/c²).')],'Speed is positive magnitude; Q2 moves toward−x inQ1 frame.')
R(31,[N('Ship-frame passage time',350/(c*add(.82,.82)),'s','Meteorite relative speed is1.64c/(1+.82²); ship proper length350m.')],'The meteorite is antiparallel, so the relative speed uses addition of magnitudes.')
R(32,[B('a · u prime/c at v=.90c',(.8-.9)/(1-.8*.9),'The graph intercept fixesu=.800c; transform to moving frame.'),B('b · Limiting u prime/c',-1,'For fixedu<c, (u−v)/(1−uv/c²) tends to−c asv→c.')],'Partb is a mathematical limiting value, not an observer actually moving atc.')
R(33,[N('a · Messenger proper time',4/gam(.95),'y','Ground length.6ly and closing speed.15c give4y; divide byγmessenger.'),N('b · Armada-frame time',gam(.8)*(4-.8*3.8),'y','Ground event separation isΔt4y, Δx3.8ly.'),N('c · Ground-frame time',4,'y','Time=.6ly/(.95c−.8c).')],'All three frames refer to the same departure and arrival events.')
# Doppler shifts.
R(34,[N('Transverse wavelength shift',(gam(.1)-1)*589,'nm','Transverse detected frequency f=f0/γ, hence λ=γλ0.')],'The fixed center detector sees purely transverse source motion.')
R(35,[N('Received frequency',100*sqrt(.1/1.9),'MHz','Receding Doppler factor√[(1−β)/(1+β)].')],'Frequency decreases for recession.')
r=1.004;b=(r*r-1)/(r*r+1)
R(36,[N('a · Radial speed',b*c,'m/s','Invert λ/λ0=√[(1+β)/(1−β)].'),C('b · Motion','Receding','Approaching','Purely transverse with no radial component','The received wavelength is longer.')],'The exact relativistic result differs negligibly from the small-shift approximation.')
R(37,[N('Required approach speed',80/620*c,'m/s','The explicitly requested small-shift Eq37-36 givesv/c=|Δλ|/λ0=80/620.')],'This exercise explicitly asks for the approximate Doppler relation, not the exact relativistic inversion.',scope='Uses the approximation explicitly requested in the question; exact relativistic inversion would give a different speed.')
r=525/513;b=(r*r-1)/(r*r+1)
R(38,[N('a · Radial speed',b*c,'m/s','Use observed525nm and proper513nm.'),C('b · Motion','Away from Earth','Toward Earth','At rest','Positive wavelength shift is a redshift.')],'The graph labels the line shift+12nm.')
R(39,[N('a · Received wavelength',450*sqrt(1.2/.8),'nm','Receding Doppler wavelength factor.'),C('b · Color','Green','Blue','Red','The wavelength is approximately551nm.')],'Use the light source proper wavelength450nm.')
# Relativistic energy and momentum.
R(40,[N(f'{l} · Work',me*c*c*(gam(b)-1),'J','Work equals the increase in relativistic kinetic energy.') for l,b in zip('abc',[.5,.99,.999])],'Initial kinetic energy is zero.')
g=1+100/Ee
R(41,[N('a · Lorentz factor',g,'dimensionless','γ=1+K/(mc²).',g*2e-7),B('b · Speed parameter β',beta(g),'Invertγ using the specified electron mass.')],'Specified electron mass and energy are retained at full precision.')
R(42,[N('Minimum breakup energy',(3*4.00151-11.99671)*uc2,'MeV','Required energy=(sum final rest masses−initial rest mass)c².')],'Nuclear masses are supplied, so no electron subtraction is introduced.')
R(43,[N('a · Work from.18cto.19c',Ee*(gam(.19)-gam(.18)),'MeV','ΔK=mc²(γf−γi).'),N('b · Work from.98cto.99c',Ee*(gam(.99)-gam(.98)),'MeV','The same speed increment costs much more energy nearc.')],'Use the same electron rest energy for both intervals.')
R(44,[N('Reaction Q',(1.007825+18.998405-4.002603-15.994915)*uc2,'MeV','Q=(Mi−Mf)c².')],'The given atomic masses have equal total electron count on both sides.')
g=1.35e5/139.6;b=beta(g)
R(45,[N('Decay altitude',120000-b*c*g*35e-9,'m','Lab decay duration=γ35ns, downward distance=vΔt.')],'Subtract the traveled distance from the120km creation altitude.')
mE=(121**2-55**2)/(2*55)
R(46,[C('a · Rest mass formula','m=[(pc)²−K²]/(2Kc²)','m=[(pc)²+K²]/(2Kc²)','m=pc²/K','Rearrange (pc)²=K²+2Kmc².'),C('b · Low-speed limit','p²/(2K)=m to leading order','p/K=m','K/c²=m at all low speeds','WithK≈p²/(2m), theK² term is higher order.'),N('c · Mass relative electron mass',mE/Ee,'dimensionless','First compute mc²=[121²−55²]/(2×55)MeV.')],'All energy-like quantities are consistently inMeV.')
R(47,[N('Driving distance',.000320*c*c/3.65e7*12.75,'km','Rest energy divided by gasoline energy per liter timeskm/L.')],'Mass320mg is.000320kg.')
g=6.9/2.2;b=beta(g);E0=207*Ee
R(48,[B('a · β',b,'Lifetime ratio isγ.'),N('b · Kinetic energy',(g-1)*E0,'MeV','K=(γ−1)mc² withmμ=207me.'),N('c · Momentum',E0*sqrt(g*g-1),'MeV/c','pc=mc²√(γ²−1).')],'Both source lifetimes areμs; their ratio fixesγ.')
g=14.24e-9/(mp*c*c);b=beta(g)
R(49,[N('a · Page width in proton frame',.21/g,'m','The page rest width contracts by1/γ.'),N('b · Passage time in reader frame',.21/(b*c),'s','Time=rest page width/proton speed.'),N('c · Passage time in proton frame',.21/(b*c*g),'s','The proton clock measures proper time.')],'The14.24nJ quantity is total energy, not kinetic energy.')
p=[]
for letters,E0 in zip(['ab','cd','ef'],[.510998,938.272,3727.40]):
 g=1+10/E0;p.extend([N(letters[0]+' · Lorentz factor',g,'dimensionless','γ=1+10.00MeV/E0.',g*1e-5),B(letters[1]+' · β',beta(g),'β=√(1−γ⁻²).')])
R(50,p,'Each explicitly supplied rest energy is used directly.')
R(51,[C('Momentum in units mc','√8 mc','3mc','2mc','E3mc² andE²=(pc)²+(mc²)² givepc=√8mc².')],'The requested result is a general relation, not a numerical particle mass.')
p=[C('a · Expansion','K=mv²/2+3mv⁴/(8c²)+higher terms','K=mv²/2+mv⁴/(8c²)+higher terms','K=mc²+mv²/2','Expand (1−β²)^−1/2 throughβ⁴ and subtract rest energy.')]
for letters,b in [('bc',.05),('de',.8)]:p.extend([N(letters[0]+' · Classical kinetic term',.5*Ee*b*b,'MeV','Classical term=mc²β²/2.'),N(letters[1]+' · First correction',.375*Ee*b**4,'MeV','Correction=3mc²β⁴/8.')])
p.append(B('f · β threshold',sqrt(.1*4/3),'Correction/classical=(3/4)β²; set equal.10.'));R(52,p,'At.80c the truncated series is only an approximation; the two requested terms remain well defined.')
E0=Ee;K=10.;vcl=sqrt(2*K*MeV/me);prel=sqrt(K*K+2*K*E0)*MeV/c;gre=1+K/E0
R(53,[C('a · Relativistic period','T=2πγm/(|q|B)','T=2πm/(|q|B) at every speed','T=2π|q|B/(γm)','Insert r=γmv/(|q|B) intoT=2πr/v.'),C('b · Independent of speed?','No; it grows withγ','Yes;γ cancels','No; it decreases withγ','The radius has an extra factorγ.'),N('c · Classical radius',me*vcl/(e*2.2),'m','Use classicalv=√(2K/m), even though this approximation is invalid at10MeV.'),N('d · Correct radius',prel/(e*2.2),'m','r=p/(eB), withpc=√(K²+2KE0).'),N('e · Classical period',2*pi*me/(e*2.2),'s','Classical cyclotron period.'),N('f · Correct period',2*pi*gre*me/(e*2.2),'s','Multiply classical period byγ.')],'The classical answers are requested comparisons, not physically admissible actual electron motion.')
R(54,[B('a · β whenK2E0',beta(3),'Total energy is3E0.'),B('b · β whenE2E0',beta(2),'γ2.')],'K and totalE must not be confused.')
R(55,[B('a · β',1/sqrt(2),'p=mc givesγβ1.'),N('b · γ',sqrt(2),'dimensionless','E²=(mc²)²+(mc²)².'),N('c · K/E0',sqrt(2)-1,'dimensionless','K/E0=γ−1.')],'The invariant relation independently checksγ²−(γβ)²=1.')
mtnt=1.8e14/3.4e6*.227;mfiss=1.8e14/(.0008*c*c)
R(56,[N('a · TNT mass',mtnt,'kg','Energy per mole3.40MJ; mass per mole.227kg.'),C('b · TNT transport','A large train or many trucks are required','A backpack suffices','A few grams suffice','The mass is about1.20×10⁷kg.'),N('c · Fissionable mass',mfiss,'kg','Only.080% of the mass converts to energy.'),C('d · Fissionable material transport','The mass is backpack scale, ignoring shielding and handling','It requires a train by mass alone','It weighs millions of kilograms','The ideal mass is about2.50kg; this comparison concerns mass only.')],'The source word weight is interpreted as requested mass inkg, with transport comparison; no handling claim is implied.',pages=[33,34])
R(57,[N('Mass consumption rate',1e41/c**2*year/2e30,'solar masses/y','dm/dt=P/c²; convert seconds to years andkg to2.0e30kg solar mass.')],'Radiated energy is supplied by a reduction in system mass.')
p=[]
for letters,K in zip(['ab','cd','ef'],[.001,1,1000]):
 g=1+K/Ee;p.extend([N(letters[0]+' · Lorentz factor',g,'dimensionless','γ=1+K/E0.',g*2e-8),B(letters[1]+' · β',beta(g),'Invertγ; retain full precision.')])
R(58,p,'Use the explicitly specified electron mass and energy unitskeV,MeV,GeV.')
KO_momentum=(4.00260*7.70+1.007825*4.44)/16.99914;Q_momentum=KO_momentum+4.44-7.70
Q=(4.00260+14.00307-16.99914-1.007825)*uc2;KO=7.70+Q-4.44
R(59,[N('a · Oxygen kinetic energy',KO,'MeV','Rest masses give Q=(mα+mN−mO−mp)c²; energy conservation then givesKO=7.70+Q−4.44MeV.'),N('b · Reaction Q',Q,'MeV','Q=KO+Kp−Kα.')],'Primary answers use the supplied rest masses and energy conservation. The rounded right-angle nonrelativistic momentum route gives a slightly different valid approximate result; those explicit alternatives are accepted.')
# Additional problems.
bmin=240/(c*1e-6)
R(60,[C('a · Time transformation','Δt′=γ(Δt−βΔx/c)','Δt′=γ(Δt+βΔx/c)','Δt′=Δt/γ for everyβ','Apply the Lorentz transformation to both events.'),C('b · Low-speed graph','Decreases nearly linearly from1μs','Increases from1μs','Constant at1μs','Initial derivative−Δx/c.'),C('c · High-speed graph','Falls to a positive minimum then tends to positive infinity','Crosses zero and tends negative','Remains constant','Timelike events retain positive order.'),B('d · β at minimum',bmin,'Derivative vanishes atβ=Δx/(cΔt).'),N('e · Minimum temporal separation',sqrt((1e-6)**2-(240/c)**2),'s','The proper interval is√(Δt²−Δx²/c²).'),C('f · Causal connection possible?','Yes; the separation is timelike','No; every separated event pair is spacelike','Only ifβ exceeds1','240m is less than light travel distance in1μs.')],'Graph predictions are checked as conclusions, not freehand drawings.')
R(61,[C('a · Spatial transformation','Δx′=γ(Δx−βcΔt)','Δx′=γ(Δx+βcΔt)','Δx′=Δx/γ','Include the time separation.'),C('b · Low-speed graph','Initially decreases nearly linearly','Initially increases','Constant','Initial derivative−cΔt.'),C('c · High-speed graph','Decreases through zero and tends to negative infinity','Always positive and increasing','Toucheszero then rises','At sufficiently largeβ the spatial event ordering reverses.'),B('d · β forcoincident positions',bmin,'SetΔx−βcΔt=0.')],'The same timelike interval permits a frame where both events occur at one place.')
R(62,[B('a · u prime/c at v=.80c',(-.2-.8)/(1+.2*.8),'The graph interceptu=−.200c.'),B('b · Limiting u prime/c',-1,'The transformation tends to−1 asv→c.')],'The primed velocity graph is negative; partb is a mathematical limit.')
R(63,[C('a · Apparent transverse distance','Dapp=vt sinθ','Dapp=vt cosθ','Dapp=ct','Project the knot displacement across the line of sight.'),C('b · Arrival-time difference','Tapp=t(1−v cosθ/c)','Tapp=t(1+v cosθ/c)','Tapp=t/γ','The second flash has a shorter light path byvtcosθ.'),N('c · Apparent speed/c',.98*sin(pi/6)/(1-.98*cos(pi/6)),'dimensionless','Divide projected displacement by arrival-time separation.')],'An apparent transverse speed abovec does not imply local superluminal motion.')
g=sqrt(1+(.7e9/c)**2)
R(64,[N('Primed spatial separation',2/g,'m','Graph intercept2m=γΔx′; slope.7m/ns=γv.',.03)],'The graph runs from(0ns,2m) to(10ns,9m); combine slope andintercept.')
R(65,[C('a · Collinear addition','βAC=(βAB+βBC)/(1+βABβBC)','βAC=βAB+βBC','βAC=(βAB−βBC)/(1+βABβBC)','Transform particleA fromB toC.'),C('b · Doppler-factor product','MAC=MABMBC reproduces the addition law','MAC=MAB+MBC reproduces the addition law','MAC=MAB/MBC for all motions','SubstituteM=(1−β)/(1+β) andsolve forβ.')],'The rational factor linearizes repeated rapidity addition.')
R(66,[N('a · MAC',(1/3)**2,'dimensionless','Eachβ.5 givesM1/3, so product1/9.'),B('b · βAC',.8,'β=(1−M)/(1+M).'),N('c · Particle velocity',.8*c,'m/s','v=βc in the positive direction.')],'Repeated boosts are not ordinary addition.')
b=add(add(.2,-.4),.6)
R(67,[C('a · Three-boost identity','MAD=MABMBCMCD','MAD=MAB+MBC+MCD','MAD=MABMBC/MCD','Associativity of collinear rapidity addition gives a product of all three factors.'),N('b · A velocity relativeD',b*c,'m/s','Compose+.20,−.40,+.60 relativistically.')],'Signed speeds retain their directions.')
t=760/(.98*c)
R(68,[N('a · Ship time front-to-rear',t,'s','Proper shiplength760m divided by protonrelative speed.98c.'),N('b · Earth time front-to-rear',gam(.95)*(t-.95*760/c),'s','Δx′=−760m, so inverse transformationΔt=γ(Δt′+βΔx′/c).'),N('c · Ship time rear-to-front',t,'s','The ship-frame crossing time is the same.'),N('d · Earth time rear-to-front',gam(.95)*(t+.95*760/c),'s','NowΔx′=+760m.')],'Signed displacement is essential for the inverse Lorentz transformation.')
b=.998;g=gam(b);L=30.5/g;tg=(6-L)/(b*c);xc=g*(6-b*c*tg);tc=g*(tg-b*6/c)
R(69,[N('a · Limo length in garageframe',L,'m','Contract30.5m byγ.'),N('b · Event2 xg',6,'m','The backdoor is fixed atxg6m.'),N('c · Event2 tg',tg,'s','The contracted limo nose beginsatL andtravels to6m.'),N('d · Both-door closed interval',tg,'s','Event1closesfront at0; event2opensback attg.'),N('e · Garage length in carframe',6/g,'m','Contract the garage properlength.'),N('f · Event2 xc',xc,'m','xc=γ(xg−vtg).'),N('g · Event2 tc',tc,'s','tc=γ(tg−vxg/c²).'),C('h · Both doors shut around wholelimo in carframe?','No','Yes','Onlyforaninstant','The two door events are not simultaneous in the car frame.'),C('i · First event in carframe','Event2: backdoor opens','Event1: frontdoor closes','Simultaneous','tc2 is negative.'),C('j · Car-frame event sketch conclusion','Back door opens before rear bumper reaches the front door','Rear bumper is shut in before the back opens','Both doors remain shut throughout','The moving garage passes the stationary longcar; relativity of simultaneity reverses door-event order.'),C('k · Events causally related?','No; the interval is spacelike','Yes; the front door sends a light signal to open the back','Yes; all reversed-order events are causal','The door events are separated too far in space for their time difference.'),C('l · Bet outcome','Garageman wins in the garage frame; all observers agree on the physical passage','Carman proves length contraction impossible','They disagree about whether the limo is damaged','A contracted car fits with both doors closed in the garage frame, without requiring simultaneous closure in every frame.')],'Idealized instantaneous dooroperations; no collision or elastic compression is implied.')
b=630/c;g=gam(b)
R(70,[N('a · Fractional contraction',b*b/(1+sqrt(1-b*b)),'dimensionless','Use1−√(1−β²)=β²/[1+√(1−β²)] to avoid cancellation.'),N('b · Ground time for 1μs lag',1e-6/(b*b/(1+sqrt(1-b*b))),'s','Ground elapsedt minusairplane proper t/γ equals1μs.')],'The original requested lag is1.00μs; orbital/gravitational effects are excluded.')
b=27000/3.6/c
R(71,[N('a · Classical relative speed',54000,'km/h','Oppositeorbital speeds addclassically.'),N('b · Classical fractional overestimate',b*b,'dimensionless','vclass/vrel−1=βorbit² exactly.')],'Bothsatellites haveequal andopposite orbitalvelocity.')
R(72,[B('Speed parameter β',.75,'Lightneeds6y, particle8y, soβ6/8.')],'Distance is6ly andextra duration2y.')
R(73,[N('Required work',Ep*(gam(.986)-gam(.985)),'MeV','ΔK=mpc²(γf−γi).')],'Work depends onLorentz-factorchange.')
R(74,[N('Mean Earth-frame distance',.99*c*gam(.99)*26e-9,'m','Lifetimeγ26ns multiplied by.99c.')],'Proper pionlifetime is26ns.')
R(75,[N('Distance in electronframe',26/(1533/Ee),'ly','γ=Etot/E0; contract the26ly Earth-Vegaseparation.')],'1533MeV is totalenergy.')
R(76,[B('Speed parameter β',beta(10.611e-9/(mp*c*c)),'γ=Etot/(mpc²), usingthe specified precise protonmass.')],'Appendix-B best-value protonmass is used, rather than rounded1.67e−27kg.')
n=1
while tanh(n*atanh(.5))<=.999:n+=1
R(77,[N('Number of increments',n,'increments','AfterNboosts β=tanh[Natanh(.5)]; choosefirst integerexceeding.999.',0)],'Eachspeedincrement is measured in the new instantaneous restframe.')
r=462/434;b=(r*r-1)/(r*r+1)
R(78,[N('a · Radial speed',b*c,'m/s','Invert the redshiftfactor.'),C('b · Motion','Receding','Approaching','No radialmotion','Observedwavelength islonger.')],'Proper434nm becomes462nm.')
R(79,[N('Electronmomentum',sqrt(2**2+2*2*Ee),'MeV/c','pc=√(K²+2KE0).')],'K2MeV excludesrestenergy.')
b=30000/c
R(80,[N('Diameter contraction',2*6370000*b*b/(1+sqrt(1-b*b)),'m','ΔD=D0[1−√(1−β²)], evaluated stably.')],'Only the diameterparallelto motioncontracts.')
R(81,[B('Center-of-momentumframe β',gam(.5)*.5/(gam(.5)+1),'βCM=Ptotalc/Etotal=γβ/(γ+1) foroneparticleatrest.')],'The particles haveequal restmass.')
R(82,[N('a · Proper lifetime',.000230/(.96*c*gam(.96)),'s','Labtracklength divided byγv.'),N('b · Particle rest-frame travel distance',0,'m','The particle stays atoneposition in its ownrestframe.')],'The laboratory apparatus moves in the particleframe; the particle itself doesnot.')
p=[]
for letters,E0,unit in [('abc',Ep/1000,'GeV'),('def',Ee,'MeV')]:
 g=gam(.99);p.extend([N(letters[0]+' · Kinetic energy',(g-1)*E0,unit,'K=(γ−1)E0.'),N(letters[1]+' · Total energy',g*E0,unit,'E=γE0.'),N(letters[2]+' · Momentum',g*.99*E0,unit+'/c','pc=γβE0.')])
R(83,p,'The protonanswersareinGeV andelectronanswersinMeV.')
R(84,[C('a · Timer period inS','τ=γτ0','τ=τ0/γ','τ=τ0','Successivetimer ticksoccur atoneplaceinSprime, so theirS coordinateintervalis dilated.'),C('b · Received pulse interval','τR=τ0√[(1+β)/(1−β)]','τR=τ0√[(1−β)/(1+β)]','τR=τ0/γ','DuringeachS tickinterval, the recedingtransmitter adds pathlengthvτ; τR=τ(1+β).'),C('c · Why intervals differ','Pulse arrivals include changing light-travel time; timer ticks do not','Observers inoneframe may assign arbitrarydifferent clockrates','Lighttravelsatdifferent speeds in the two measurements','BothobserversuseS time, buttimedticksandreceivedpulsesaredifferenteventpairs.')],'The transmitter recedes fromthe fixedreceiver shown.')
R(85,[B('Relativeapproachspeed/c',add(.8,.6),'Oppositelydirected cosmicrayvelocitiescompose as(.8+.6)/(1+.8*.6).')],'The station seesoppositedirections, not anallowedrelative speed1.4c.')
E=.003*c*c
R(86,[N('a · Releasedenergy',E,'J','0.10%of3kg is.003kg convertedtoenergy.'),N('b · TNTmass',E/3.4e6*.227,'kg','Energy perkg TNT=3.4MJ/.227kg.'),N('c · Specificenergy ratio',(.001*c*c)/(3.4e6/.227),'dimensionless','Compare energyperkg forfissionablematerialandTNT.')],'Only the stated fractionofnuclearmass isconverted.')
R(87,[N('a · Classical acceleratingvoltage',me*c*c/(2*e),'V','ClassicaleV=mc²/2 atv=c.'),B('b · Actualβ',beta(1.5),'Actualkineticenergy.5mc² impliesγ1.5.')],'The classicalpredictionofc isnotphysicallyvalid.')
R(88,[B('Decoyspeedrelativecruiser/c',(.98-.9)/(1-.98*.9),'Transformdecoyvelocityfromscoutframe tocruiserframe.')],'Bothgivenvelocitieshave the samedirection.')
b=tanh((atanh(.9)+atanh(.8))/2);rel=abs((.9-b)/(1-.9*b))
R(89,[B('a · RequiredβB',b,'Equalrelativeapproachspeeds meanBrapidity is theaverageofAandC rapidities.'),B('b · Relativeapproachspeed/c',rel,'TransformeitheroutershiptoBframe.')],'B liesbetween the twooutershipsinrapidity, notordinaryspeed.')
R(90,[N('Nosealignmentdelay inBframe',gam(.9)*.9*200/c,'s','Eventsare simultaneousinA, separatedby200m; inverseLorentztime givesγvL/c².')],'The laterB-frameeventisnosealignment; timeisrelative totailalignment.')
R(91,[B('RequiredBspeed/c',tanh(atanh(.8)/2),'EqualrapiditygapstoAandstationputBhalfway between0andatanh(.8).')],'Thisgives.500c, makingbothapproachB at.500c.')
b=.9;g=gam(b);Lc=200/g;dt=(200-Lc)/(b*c);dtp=g*(dt-b*200/c)
R(92,[N('a · Tunnel length in trainframe',Lc,'m','The tunnelcontractsfrom200m.'),C('b · Firstevent in trainframe','FF','RN','Simultaneous','The Lorentz-transformedFFminusRNintervalisnegative.'),N('c · Trainframe eventseparationmagnitude',abs(dtp),'s','Transformthe twoevents usingΔx200m andΔt=(200−200/γ)/v.'),C('d · Bombexplodes in trainview?','Yes','No','Observer-dependent','FF occursbeforethe reardevicecan senditsdeactivatingpulse.'),N('e · Trainlength in tunnelframe',Lc,'m','Traincontractsbythesamefactor.'),C('f · Firstevent in tunnelview','RN','FF','Simultaneous','The rear entersbeforethefront reachesfarend.'),N('g · Tunnelframe eventseparation',dt,'s','Fronttravels200−LcafterRN.'),C('h · Bombexplodes in tunnelview?','Yes','No','Onlyif thetraindoesnotcontract','The signalmustchase themovingfrontandcannotarrivebeforeFF.')],'Bothframesagreeonthe physicalexplosion; thedeactivationpulsecannotoutrun light.')
EB=(200**2+100**2-50**2)/(2*200);EC=200-EB;pc=sqrt(EB*EB-100**2)
R(93,[N('a · Btotalenergy',EB,'MeV','Two-bodyrestdecay givesEB=(EA²+EB0²−EC0²)/(2EA).'),N('b · Bmomentummagnitude',pc,'MeV/c','pc=√(EB²−EB0²).'),N('c · Ctotalenergy',EC,'MeV','EC=200−EB.'),N('d · Cmomentummagnitude',pc,'MeV/c','Momentumconservation requires equaloppositemomenta.')],'ChecksverifyEB+EC200MeV andeachmassshellrelation.')
p=[]
for l,D,g in [('a',2,10),('b',4,24),('c',6,30)]:p.append(N(l+' · Earthtime coefficient ofD/c',D/beta(g),'dimensionless','Earthtime=pathlength/(βc).'))
for l,D,g in [('d',2,10),('e',4,24),('f',6,30)]:p.append(N(l+' · Shipproper-time coefficient ofD/c',D/(beta(g)*g),'dimensionless','DivideEarthtimebyγ.'))
R(94,p,'β≈1wouldgive2,4,6 and.2,1/6,.2; exactβfromthegivenγ isused.')
b=.710;mass=2*e*1*6.28/(gam(b)*b*c)
R(95,[N('Particlemass',mass/u,'u','p=2eBr=γmv; solveform.'),C('Particleidentity','Alpha particle: two protons and two neutrons','Proton','Electron','Doublepositivechargeandmassabout4u identifyanαnucleus.')],'The fieldis1T andradius6.28m.')
p=sqrt(2.5**2+2*2.5*Ee)*MeV/c
R(96,[N('Magneticfield',p/(e*.03),'T','Relativisticp=√(K²+2KE0)/c andB=p/(er).')],'Use3.0cmcurvatureradius.')
g=1+500000/Ep;b=beta(g);p=sqrt(500000**2+2*500000*Ep)*MeV/c
R(97,[N('a · Lorentzfactor',g,'dimensionless','γ=1+500GeV/E0.'),B('b · β',b,'β=√(1−γ⁻²).'),N('c · Synchrotronfield',p/(e*750),'T','B=p/(er).')],'500GeViskineticenergy,not totalenergy.')
R(98,[N('a · Pulse rate',150/gam(.9),'beats/min','Groundtimeisdilated, sotheobservedclockrateisreducedbyγ.'),N('b · Summedground-measuredstridedistance',3600/gam(.9),'m','Interpret1m/sasproperwalkingrate; eachlongitudinalstridecontractsby1/γ.')],'The printedphrase stride length1m/s has speedunits; use1m/saswalkingrate, withwalkingparallelto shipmotion.',scope='Partb is the sum of contracted treadmill strides, not the spaceship’s travel distance. Walkingorientation is taken parallel to shipmotion; transverse strides would have no length contraction.')
R(99,[N('a · Observedwavelength',650*sqrt((1-.42)/(1+.42)),'nm','ApproachingDopplerfactorcontractsreceivedwavelength.'),C('b · Color','Blue','Green','Yellow','The wavelengthisapproximately415nm.')],'Sourceproperwavelength650nmisred.')
R(100,[N('a · Classicalrecession speed/c',2,'dimensionless','Classicalλ/λ0=1+v/c yields3=1+v/c.'),B('b · Relativisticrecession β',.8,'InvertDopplerratio3:β=(9−1)/(9+1).')],'Theexerciseassumesthe cosmologicalredshiftcan beinterpretedusingthegivenDopplerrelation.')
R(101,[N('a · Equivalentmass',2.2e12*3.6e6/c**2,'kg','ConvertkWh tojoulesanddividebyc².'),C('b · Dependsonenergysource?','No; equalenergy corresponds toequalmass','Yes; onlynuclearenergyhasmassequivalence','Yes; hydroelectricenergyhaszeromassequivalence','Mass-energyconversionisindependentofgenerationmethod.')],'Themassdifferenceisthatof thecompleteenergy-supplying system.')
t=.2/(.992*c)
R(102,[N('a · Flightduration',t,'s','t=L/v.'),N('b · Gravitationalfall',.5*9.8*t*t,'m','Usey=gt²/2 overthisshortflight.'),C('c · Inertialapproximation','Excellent overthisduration; gravitationalfallisnegligible','Invalidforanytimeinterval','Validonlyifgravityiszeroeverywhere','The calculatedfallisfarbelowatomiclengthscales.')],'Thisis theproblem’s Newtoniangravityestimate, adequateforthe frame-approximationdecision.')
vals=[.0254/year,.0005,55*1609.344/3600,sqrt(3*1.380649e-23*300/(2.016*u)),1200/3.6,11200,30000,3e7]
p=[B(f'{l} · Speedparameter β',v/c,'β=v/c afterconvertingthe stated orassumedrepresentativespeedtoSI.') for l,v in zip('abcdefgh',vals)]
R(103,p,'Representativevalues: year365.25d; roomtemperature300K; H2mass2.016u; explicitplane speed1200km/h; Earthescape11.2km/s; Earthorbit30km/s.',scope='The representative room temperature and Earth speeds are explicit assumptions. For(e), the primary check uses the explicit1200km/h value, givingβ1.112e−6. The accompanying Mach2.5 label is inconsistent if1200km/h denotes the plane speed; treating1200km/h as Mach1 instead givesβ2.780e−6, accepted as an explicitly conditional alternative.')
# Conceptual questions.
R(1,[C('Length-versus-speedcurve','c','d','e','L=L0√(1−β²)decreaseswith increasinglynegative slope.')],'Theoriginalgraphcurvecis thedownward-concave contractioncurve.',kind='questions')
R(2,[C('a · SignofΔxprime','Negative','Positive','Zero','Theprotontravelsfromfronttorrear, opposite+xprime.'),C('b · SignofΔtprime','Positive','Negative','Zero','Impactoccursafterlaunchinshipframe.')],'Theshipmovesright,butthe protontravelsleftinsideit.',kind='questions')
R(3,[C('Time-versus-speedcurve','b','a','c','Δt=γΔτgrowsnonlinearlywithβ.')],'Propertime25sisfixed.',kind='questions')
R(4,[C('a · Smallerreading','C1','C1 prime','C2 prime','C1is theoneclockpresentatbothpassageevents.'),C('b · Propertimeclock','C1','C2 prime','Neitherclock','BothrelevantclockeventslieontheC1worldline.')],'Time dilationcomparesthe oneclockproperintervalwith thetwo synchronizedprimedclocks.',kind='questions')
R(5,[C('a · Smallerreading','C1 prime','C1','C2','C1primeis presentatbothevents.'),C('b · Propertimeclock','C1 prime','C2','Neitherclock','Themovingclockmeasuresproperduration.')],'TheSclockpairmeasurescoordinateelapsedtime.',kind='questions')
R(6,[C('a · Propervoyagetime','Sam','Sally','Neither','Departureandarrivaloccuratthesameplaceontheship.'),C('b · Properlighttraveltime','Neither','Sam','Sally','Neitherinertialobserverisatbothendsof thelightpath; no restframeexistsforlight.')],'Theproperintervalofalightlikepathiszero,notashiporEarthclockduration.',kind='questions')
R(7,[N('a · ClockA initialsetting',4,'s','Ais4light-secondsfromorigin.'),N('b · ClockB initialsetting',3,'s','Bis3light-secondsfromorigin.'),N('c · ClockC initialsetting',5,'s','Cis√(4²+3²)=5light-secondsaway.'),N('d · Eventsignaltraveltime',4,'s','ClockAtotheoriginis4light-seconds.'),N('e · Assignedeventtime',10,'s','Signalarrivesat14s,butobserver subtracts4slighttravel.')],'ReadoriginalgridcoordinatesA(4,0),B(0,3),C(4,3).',kind='questions',pages=[29,30])
R(8,[C('a · Massranking','3>1=2','1=2>3','1>2>3','Restenergyismc²:3AversusA,A.'),C('b · Kineticenergyranking','2>1=3','3>2>1','1>2>3','K=E−E0givesA,2A,A.'),C('c · Lorentzfactorranking','2>1>3','3>2>1','1=2=3','γ=E/E0gives2,3,4/3.'),C('d · Speedranking','2>1>3','3>2>1','1=2=3','Speedincreasesmonotonicallywithγ.')],'Restenergy,totalenergyandkineticenergyaredifferentquantities.',kind='questions')
R(9,[C('a · Massranking','3=4=6>1=2=5','1>2>3>4>5>6','1=2=3=4=5=6','Horizontaltrianglebaseismc².'),C('b · Momentumranking','1>2=3>4>5=6','3=4=6>1=2=5','1=2>3=4>5=6','Verticaltriangleheightispc.'),C('c · Lorentzfactorranking','1>2>3>4>5>6','6>5>4>3>2>1','1=2=3=4=5=6','γ=hypotenuse/baseincreaseswithtriangleangle.'),C('d · Equaltotalenergy','2and4','1and6','3and5','Theirslantedhypotenuselengthsareexplicitlyequal.'),C('e · Kineticenergyamonglowestmasses','1>2>5','5>2>1','1=2=5','Thesamebase mc²meanslargerhypotenuse giveslargerK.')],'Originaltrianglegeometryisused,notline-numberordering.',kind='questions')
R(10,[C('Receivedfrequencyranking','b>a>c>d','d>c>a>b','a>b>c>d','Approachblueshifts; higherapproachspeedgiveshigherfrequency,recessiontheopposite.')],'Allsignalsarecomparedatthesameproperemissionfrequency.',kind='questions')
R(11,[C('a · Shuttlespeedranking','3>1=2>4','3>4>1=2','1>2>3>4','Relativisticadditiongives.9322,.859375,.84615asappropriate.'),C('b · Pilot-measuredracedistanceranking','4>1=2>3','3>1=2>4','1=2=3=4','Thefastestshuttlesees themostcontractedracetrack.'),C('c · Detectedstarshipfrequencyranking','1>4>2>3','3>2>4>1','1=2>3=4','Ship-to-shuttlerelativespeeds are.4,.7,.9,.6; largerrecessionmeanslowerfrequency.')],'Speedaddition, lengthcontractionandDopplershiftusedifferentgivenrelativevelocities.',kind='questions')
# Explicit alternatives from rounded/overdetermined source data and estimates.
for record in rows:
 if record['id']=='physics-chapter-37-problems-59':
  record['parts'][0]['acceptedValues']=[KO_momentum];record['parts'][1]['acceptedValues']=[Q_momentum]
  record['scope']='Primary values use the supplied rest masses. Rounded nonrelativistic momentum estimates from the stated right-angle emission are also accepted explicitly.'
 if record['id']=='physics-chapter-37-problems-103':
  record['parts'][0]['acceptedValues'].append(3e-18);record['parts'][1]['acceptedValues'].append(2e-12)
  record['parts'][4]['acceptedValues'].extend([2.5*1200/3.6/c,2.8e-6])

# Improve prose spacing without altering IDs, units, numeric values or equation symbols.
import wordninja
def readable(value):
 value=re.sub(r"[A-Za-z]{6,}",lambda m:' '.join(wordninja.split(m.group(0))),value)
 for old,new in [('relativistic ally','relativistically'),('non relativistic','nonrelativistic'),('space like','spacelike'),('time like','timelike'),('light like','lightlike'),('blue shift','blueshift')]:value=value.replace(old,new)
 return value
for record in rows:
 for key in ['reasoning','scope','reviewNotice','referenceAnswer']:
  if key in record:record[key]=readable(record[key])
 record['assumptions']=[readable(x) for x in record['assumptions']]
 for field in record['parts']:
  for key in ['label','explanation']:
   field[key]=readable(field[key])
  if field['type']=='choice':
   field['answer']=readable(field['answer']);field['options']=[readable(x) for x in field['options']]

# Structural validation and reproducible output.
source=json.loads(gzip.decompress((ROOT/'site/questions/physics.json.gz').read_bytes()));target={q['id'] for q in source if q['chapter']==37}
assert {r['id'] for r in rows}==target
assert len(rows)==len(target)==114
for r in rows:
 for p in r['parts']:
  if p['type']=='numeric':assert math.isfinite(p['answer']) and (p['answer']==0 or p['tolerance']<abs(p['answer']))
  else:assert p['answer'] in p['options'] and len(set(p['options']))==3
(H/'ch37.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
audit={'chapter':37,'exercises':len(rows),'fields':sum(len(r['parts']) for r in rows),'sourcePagesVisuallyReviewed':list(range(29,38)),'numericChecks':['Lorentz interval invariance and inverse transformation','energy-momentum mass-shell identity','two-body energy and momentum conservation','velocity composition bounded by c','near-light beta fields reject beta=1','source graph intercept/slope independently read'],'sourceResolutions':{'microseconds':'P1/17/18/20/21/25/60/61/70 use original μs, not OCR ms','graphReadings':'P6 proper8s; P14 restlength.80m; P20 intercept2μs,slope.01μs/m; P32 u=.8c; P62 u=-.2c; P64 intercept2m,slope.7m/ns','P19/P25':'Positive separation/speed magnitudes with separate order/direction choices','P59':'Primary rest-mass defect Q=-1.20628MeV; explicitly accepted rounded nonrelativistic right-angle momentum route gives slightly different result','P98':'Printed stride length1m/s interpreted as walkingrate, longitudinal strides; ground answer is summed contracted strides, not shiptravel distance','P103e':'Primary explicit1200km/h; scoped alternative interprets1200km/h as Mach1 for the inconsistent Mach2.5 label'},'sourcePartCoverage':'Every numbered problem and conceptual question ID matched; graph/drawing/proof requests checked through the requested quantities, equations, and conclusions.','typography':'All slash-containing choices checked through actual SolutionMath and Linkedom; no unformatted mathematical slashes.'}
(H/'ch37-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(len(rows),'records',sum(len(r['parts']) for r in rows),'fields')
