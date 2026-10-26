#!/usr/bin/env python3
"""Original magnetic-force derivations; all source diagrams reviewed PDF24–33."""
import json,math,gzip,pathlib,subprocess
from math import pi,sqrt,sin,cos,tan,acos,asin,atan2,radians as rad,degrees as deg
H=pathlib.Path(__file__).resolve().parent;ROOT=H.parents[1]
e=1.602e-19;me=9.11e-31;mp=1.673e-27;u=1.661e-27;g=9.8
rows=[]
def N(l,a,unit,why,t=None):return dict(label=l,type='numeric',answer=a,unit=unit,tolerance=max(abs(a)*.008,1e-30) if t is None else t,explanation=why)
def C(l,a,b,c,why):return dict(label=l,type='choice',answer=a,options=[a,b,c],explanation=why)
def V(l,v,unit,why):return [N(l+' · '+d,a,unit,why) for d,a in zip(['x component','y component','z component'],v)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def mag(a):return sqrt(sum(x*x for x in a))
def scale(a,s):return [x*s for x in a]
def add(a,b):return [x+y for x,y in zip(a,b)]
def T(m,q,B):return 2*pi*m/(abs(q)*B)
def speed(K,m):return sqrt(2*K/m)
def R(n,p,why,kind='problems',assumptions=None,scope=None,pages=None):
 page=(27 if n<=16 else 28 if n<=29 else 29 if n<=45 else 30 if n<=59 else 31 if n<=71 else 32 if n<=86 else 33) if kind=='problems' else (25 if n<=4 else 26)
 r=dict(id=f'physics-chapter-28-{kind}-{n}',parts=p,reasoning=why+' Verification: '+why,sourcePages=pages or [page],assumptions=assumptions or ['Classical nonrelativistic motion and uniform fields where stated; e=1.602×10⁻¹⁹ C, mₑ=9.11×10⁻³¹ kg, mₚ=1.673×10⁻²⁷ kg.'])
 if scope:r['scope']=scope
 rows.append(r)
v=6.5e-17/(e*.0026*sin(rad(23)))
R(1,[N('a · Proton speed',v,'m/s','F=qvBsinθ.'),N('b · Kinetic energy',.5*mp*v*v/e,'eV','K=mv²/2, then divide by e joules per electron-volt.')],'The speed is inferred from the perpendicular velocity component, not from qvB alone.')
R(2,V('Magnetic field',[0,0,-.010*g/(80e-6*20000)],'T','The magnetic force must be upward: +x velocity crossed with −z field points +y only for negative Bz; solve qv(−Bz)=mg.'),'Balance gravity against magnetic force; positive charge requires B along negative z.')
R(3,V('a · Electron force',scale(cross([2e6,3e6,0],[.03,-.15,0]),-e),'N','Evaluate q(v×B), including the electron sign.')+V('b · Proton force',scale(cross([2e6,3e6,0],[.03,-.15,0]),e),'N','The same velocity and field give the opposite force for +e.'),'The cross product has only a z component; the two charges reverse its sign.')
f=3.2e-19*550*.045*sin(rad(52))
R(4,[N('a · Force magnitude',f,'N','F=qvBsin52°.'),N('b · Acceleration magnitude',f/6.6e-27,'m/s²','a=F/m.'),C('c · Speed change','Remains constant','Increases','Decreases','The magnetic force is perpendicular to instantaneous velocity and does no work.')],'A magnetic field changes velocity direction without changing kinetic energy.')
R(5,[N('Bₓ',-2,'T','Fz=q(2·3Bx−4Bx)=−2eBx=6.4×10⁻¹⁹N.')],'Use the negative electron charge in the cross product.')
R(6,[N('a · vₓ',(2000*.010-2e-17/e)/.030,'m/s','Fy=q(vzBx−vxBz), with B in teslas.'),N('b · vᵧ',(4e-17/e-2000*.020)/.030,'m/s','Fx=q(vyBz−vzBy).')],'Solve the two independent force-component equations; Fz then vanishes.')
E=add([-me/e*2e12,0,0],scale(cross([0,12000,15000],[400e-6,0,0]),-1))
R(7,V('Electric field',E,'V/m','E=ma/q−v×B with B=400μT, not400mT.'),'Original source microtesla unit controls the magnetic term.')
R(8,[N('Electron speed',1500/.4,'m/s','For crossed opposing forces, v=E/B.')],'Charge magnitude cancels in the velocity-selector condition.')
v=speed(e*1000,me);R(9,V('Magnetic field',[0,0,-100/.020/v],'T','The electric field is downward; electron electric force is upward, so its magnetic force must be downward.'),'For a right-moving electron, a field into the page supplies the balancing downward force.')
B=[-.0025,0,0];v=[0,2000,0]
R(10,sum([V(l,scale(add(E,cross(v,B)),e),'N','Add electric and magnetic forces as vectors before multiplying by q.') for l,E in [('a',[0,0,4]),('b',[0,0,-4]),('c',[4,0,0])]],[]),'v×B=+5k V/m, so the electric field may reinforce or oppose it.')
R(11,[N('Smallest electric field',1.2*speed(e*1e4,9.99e-27),'V/m','Use qΔV=mv²/2, then E=vB.')],'The electric field must be perpendicular to velocity and opposite v×B to minimize its magnitude.')
R(12,[N('a · Electric-field magnitude',2e-19/e,'V/m','The zero-speed force intercept is−2×10⁻¹⁹N=qEy.')]+V('b · Magnetic field',[0,0,4e-21/(-e)*(-1)],'T','dFy/dv=−qBz=4×10⁻²¹ N·s/m; Bx=0 and Fx=Fz=0 imply By=0.'),'Read graph endpoints(0,−2) and(100,+2), not just the zero crossing.')
R(13,[N('Hall potential',23*.65/(8.47e28*e*150e-6),'V','VH=iB/(net), with thickness150μm.')],'The current-carrying cross section uses thickness times width; the width cancels from VH.')
R(14,[N('Strip speed',3.90e-6/(.0012*.00850),'m/s','VH=Bvw using the0.850cm width and3.90μV source value.')],'Use the voltage across x and y, not along the strip length.')
R(15,V('a · Internal electric field',[0,0,-.6],'V/m','E=−v×B.')+[N('b · Potential difference magnitude',1.2,'V','ΔV=|Ez|dz=.6×2.')],'The equilibrium electric field balances magnetic deflection of mobile charges.')
R(16,[N('a · dₓ',.25,'m','Motion alongx gives no voltage, so B is alongx; dx is the remaining given25cm edge.'),N('b · dᵧ',.018/(.020*3),'m','Motion alongz produces Ey and V=Bvdy.'),N('c · d_z',.012/(.020*3),'m','Motion alongy produces Ez and V=Bvdz.')],'The zero-voltage direction identifies the magnetic-field axis.')
v=2*e*1.2*.045/(4*u);R(17,[N('a · Speed',v,'m/s','r=mv/(qB).'),N('b · Period',T(4*u,2*e,1.2),'s','T=2πm/(qB).'),N('c · Kinetic energy',.5*4*u*v*v,'J','K=mv²/2.'),N('d · Accelerating potential',.5*4*u*v*v/(2*e),'V','qΔV=K.')],'The alpha charge is2e and its mass is4u.')
v=3.2e-15/(e*.004);R(18,[C('Particle identity','Electron','Proton','Cannot be identified','Outward B and counterclockwise motion require negative charge.'),N('a · Speed',v,'m/s','F=qvB.'),N('b · Radius',me*v/(e*.004),'m','r=mv/(qB).'),N('c · Period',T(me,e,.004),'s','T=2πm/(qB).')],'The arrow at the lower left points downward along the counterclockwise orbit in an outward field.')
R(19,[N('Mass-to-charge ratio',37.5e-9/5/(2*pi),'kg/C','Read T≈37.5ns at 1/B=5T⁻¹; the slope equals2πm/|q|.')],'Graph line extrapolates through the origin; use its full axis scales.')
# Graph at Vs^.5=40 reaches r=2.0mm (not3mm vertical scale).
R(20,[N('Magnetic field',sqrt(2*me/e)*40/.002,'T','r=(√(2m/e)/B)√V; at√V=40, r=2.0mm.')],'Read the graph ordinate at the labeled horizontal tick, not the upper-right endpoint.')
v=speed(1200*e,me);B=me*v/(e*.25)
R(21,[N('a · Speed',v,'m/s','K=mv²/2.'),N('b · Field magnitude',B,'T','B=mv/(er).'),N('c · Circling frequency',e*B/(2*pi*me),'Hz','f=eB/(2πm).'),N('d · Period',T(me,e,B),'s','T=1/f.')],'The frequency and period are reciprocal and the centripetal force equals evB.')
R(22,[N('a · Alpha energy',1,'MeV','At fixedBr, K=q²B²r²/(2m); relative factor4/4=1.'),N('b · Deuteron energy',.5,'MeV','Relative factor1/2=.5.')],'Equal magnetic rigidity fixes momentum per charge, not equal kinetic energy.')
R(23,[N('Field magnitude',me*1.3e6/(e*.35),'T','B=mv/(er).')],'The magnetic field is perpendicular to the beam.')
v=speed(350*e,me);R(24,[N('a · Speed',v,'m/s','K=eΔV=mv²/2.'),N('b · Orbit radius',me*v/(e*.200),'m','r=mv/(eB).')],'The supplied200mT is.200T.')
v=speed(100*e,me);R(25,[N('a · Revolution frequency',e*35e-6/(2*pi*me),'Hz','f=eB/(2πm), B=35.0μT.'),N('b · Path radius',me*v/(e*35e-6),'m','r=mv/(eB).')],'The original PDF says microteslas, a frequent OCR trap.')
R(26,[C('Particle identity','Proton','Electron','Cannot be identified','A downward entrant in outward B bends right, requiring positive q.'),N('a · Field magnitude',pi*mp/(e*130e-9),'T','Half-circle time isπm/(qB).'),N('b · Time at twice the energy',130e-9,'s','The nonrelativistic period is independent of speed.')],'Doubling energy enlarges radius by√2 but leaves half-circle traversal time unchanged.')
M=3.92e-25;q=3.20e-19;v=speed(q*1e5,M);Nions=100e-6/M
R(27,[N('a · Separator field',M*v/q,'T','B=mv/(qr), r=1m.'),N('b · Desired ion current',Nions*q/3600,'A','I=(mass flow/mion)q.'),N('c · Thermal energy in one hour',Nions*q*1e5,'J','Every collected ion deposits qΔV of kinetic energy.')],'The slit dimensions do not alter the requested current for a specified collected mass rate.')
R(28,[N('Kinetic energy',.5*1.60e-17*26.1e-6,'J','Fr=mv²=2K.')],'Eliminate the unknown charge and mass with the centripetal-force identity.')
vp=2e-15/(e*.3);vz=6e-6/T(me,e,.3)
R(29,[N('Electron speed',math.hypot(vp,vz),'m/s','Combine vperp=F/(eB) with vparallel=pitch/T.')],'Magnetic force constrains only the perpendicular component.')
v1=speed(4000*e,me);v2=speed(6000*e,me)
R(30,[N('Exit time',T(me,e,.01)/2+2*.25/(v1+v2)+T(me,e,.02)/2,'s','Add both half-circle times and the gap time2d/(v1+v2).')],'The electron gains2keV in the gap while its speed increases uniformly.')
R(31,[N('Collision time',T(me,e,.00353)/2,'s','Opposite charges with equal momenta traverse opposite semicircles and meet after half a period.')],'Conservation of momentum gives equal and opposite speeds and equal radii.')
R(32,[N('Next field-line crossing distance',1.5e7*cos(rad(10))*T(me,e,.001),'m','A full gyration returns the electron to its original field line, after advancing vparallelT.')],'This distance is the helical pitch, not the orbit diameter.')
v=speed(2000*e,me);tt=T(me,e,.1)
R(33,[N('a · Period',tt,'s','T=2πm/(eB).'),N('b · Pitch',v*cos(rad(89))*tt,'m','p=vparallelT.'),N('c · Radius',me*v*sin(rad(89))/(e*.1),'m','r=mvperp/(eB).')],'Resolve the velocity parallel and perpendicular to B.')
v=[20,-30,50];B=[.02,-.05,-.03];angle=acos(sum(a*b for a,b in zip(v,B))/(mag(v)*mag(B)))
R(34,[N('a · Angle',deg(angle),'degrees','cosφ=(v·B)/(|v||B|).'),C('b · Does speed change?','No','Yes, it increases','Yes, it decreases','Magnetic force does no work.'),C('c · Does the angle change?','No','It continually increases','It continually decreases','Both vparallel and |vperp| stay constant.'),N('d · Helix radius',me*mag(v)*sin(angle)/(e*mag(B)),'m','Use only vperp in mvperp/(eB).')],'The dot product is positive400, so the initial angle is acute.')
R(35,[N('a · Energy gain per passage',200,'eV','A chargee gains eΔV.'),N('b · Energy after100 passages',20000,'eV','Energy gains add.'),N('c · Radius percentage increase',(sqrt(101/100)-1)*100,'%','r∝√K, notK.')],'One gap crossing is one energy increment; distinguish passages from full revolutions.')
B=2*pi*mp*12e6/e
R(36,[N('a · Resonant field',B,'T','f=qB/(2πm).'),N('b · Emerging energy',.5*mp*(2*pi*12e6*.53)**2/e,'eV','v=2πfR.'),N('c · New oscillator frequency',e*1.57/(2*pi*mp),'Hz','Use the new field in the cyclotron frequency.'),N('d · New emerging energy',(e*1.57*.53)**2/(2*mp)/e,'eV','K=(qBR)²/(2m).')],'Resonance means the electric oscillator matches the orbital frequency.')
K=.5*(2*u)*(2*pi*12e6*.53)**2;passes=K/(e*80e3);path=2*pi*.53*passes/3
R(37,[C('General path estimate','Sum semicircle lengths with radius proportional to the square root of passage number','Multiply the final circumference by every passage','Use only the final orbit circumference','Each gap crossing adds equal energy, so successive semicircle radii grow as√n.'),N('Total path length, continuous-turn estimate',path,'m','Integrating πR√(n/N) from 0 to N gives2πRN/3.',t=20)],'The final energy sets the number of half-turns; integrate their growing radii.',scope='This is an estimate using negligible injection energy and a continuous sum of semicircles; a discrete-turn estimate is also valid within the stated precision.')
B=1.2;R(38,[N('a · Oscillator frequency',e*B/(2*pi*mp),'Hz','f=qB/(2πm).'),N('b · Proton kinetic energy',(e*B*.5)**2/(2*mp)/e,'eV','K=(qBr)²/(2m).')],'Use the perpendicular orbit radius0.500m.')
R(39,[N('a · Force magnitude',5000*100*60e-6*sin(rad(70)),'N','Only the downward field component is perpendicular to the northward current.'),C('b · Force direction','West','East','Vertically upward','North crossed with downward points west.')],'Original Earth field is60.0μT, not60mT.')
R(40,[N('Wire force',13*1.8*1.5*sin(rad(35)),'N','F=iLBsinθ.')],'The angle is between the wire/current and field.')
R(41,[N('a · Current magnitude',.013*g/(.62*.44),'A','Set iLB=mg.'),C('b · Current direction','Right','Left','Either direction','Rightward current crossed with inward B gives upward magnetic force.')],'The current must support the wire weight without lead tension.')
R(42,V('a · Force',[0,-16,0],'N','Endpoint displacement is2m along+x; F=iΔr×B.')+V('b · Force',[0,0,0],'N','The endpoint displacement is parallel to Bx.'),'For uniform B, integrate i dl×B over the bent wire to obtain iΔr×B.')
f=4*.075*.5*1.2/1.3
R(43,[N('a · Force on130cm side',0,'N','Current and B are parallel.'),N('b · Force on50cm side',f,'N','The perpendicular component of this side is(.5)(1.2/1.3).'),N('c · Force on120cm side',f,'N','The equal opposite side force closes the force triangle.'),N('d · Net loop force',0,'N','A closed loop in uniform B has zero total force.')],'Forces on the two perpendicular legs have equal magnitudes and opposite directions.')
R(44,[N('Ring force magnitude',.0046*2*pi*.018*.0034*sin(rad(20)),'N','Azimuthal current crossed with the radial field component adds axially around the ring.')],'Axial B produces canceling radial forces; radial B yields the net axial force.')
R(45,V('Wire force',[0,-.0025,.00075],'N','F=iL×B=.25 i×(.003 j+.010 k).'),'Use the right-hand rule for both perpendicular components.')
f=.00913*.0256*.0563
R(46,[N('a · Wire speed',f/(24.1e-6)*.0611,'m/s','a=iLB/m and v=at.'),C('b · Motion direction','Right','Left','No motion','The indicated current across the rod and upward B give a rightward rail force.')],'The generator maintains constant current, hence acceleration is constant.')
R(47,[N('a · Minimum field',.60*g/(50*sqrt(1+.6**2)),'T','Minimize B subject to iLBcosθ=μ(mg−iLBsinθ).'),N('b · Angle from vertical',deg(math.atan(.6)),'degrees','The optimum satisfies tanθ=μ.')],'An upward component of magnetic force reduces the normal force and required friction.')
R(48,V('Force',[0,0,-5*.008*(3**3-1)/3],'N','Integrate −i dx i×(8x²mT j); the parallel Bx term contributes no force.'),'The field varies along the2m segment, so use the integral rather than its midpoint value.')
R(49,V('Torque',[0,-20*.10*.10*.05*.50*cos(rad(30)),0],'N·m','The clockwise-looking loop has μ along−z and Bx=Bcos30°, giving torque−y.'),'The stated angle is between B and the coil plane, so the normal-field angle is60°.')
R(50,[N('Maximum torque',e*2.19e6*5.29e-11/2*.0071,'N·m','I=e/T and μ=Iπr²=evr/2; τmax=μB.')],'Use the magnitude of electron charge for current magnitude.')
R(51,[N('Minimum current',.250*g/(2*10*.100*.500),'A','Balance mgrsinθ against Ni(2rL)Bsinθ; the radius and incline factor cancel.')],'The wrapped area is2rL, notπr²; no cylinder radius is needed.')
R(52,[N('Loop current',4.80e-8/(.04*.020**2),'A','Fixed perimeter8cm gives maximum area(.020m)² at a square.')],'The loop plane contains B, so torque is iAB with sinθ=1.')
R(53,[C('Arbitrary-loop torque relation','τ = NiAB sinθ for a planar closed loop','τ = NiPB sinθ where P is perimeter','τ = NiAB cosθ for every orientation','Partitioning the area into narrow rectangles cancels currents on shared internal boundaries; their vector moments sum to NiA.')],'The internal fictitious currents cancel pairwise, leaving the physical boundary current.')
a=deg(acos(1-.00080/(.020*.052)))
R(54,[N('a · Initial angle',a,'degrees','K=μB(1−cosθinitial).'),N('b · Next-rest angle magnitude',a,'degrees','Energy conservation gives equal turning angles on opposite sides of the field.')],'With no dissipation the dipole oscillates symmetrically through the aligned position.')
R(55,[N('a · Net moment magnitude',7*pi*(.2**2+.3**2),'A·m²','Same current senses make moments add.'),N('b · Reversed inner-loop moment',7*pi*(.3**2-.2**2),'A·m²','Opposite senses make moments subtract.')],'Concentric loops have the same normal axis.')
mu=2.6*pi*.15**2;R(56,[N('a · Magnetic moment',mu,'A·m²','μ=iA.'),N('b · Torque magnitude',mu*12*sin(rad(41)),'N·m','τ=μBsin41°.')],'The stated angle is between the field and loop normal.')
R(57,[N('a · Current',2.30/(160*pi*.019**2),'A','μ=Niπr².'),N('b · Maximum torque',2.30*.035,'N·m','Maximum sinθ=1.')],'Use the160turn factor only once.')
R(58,[N('Core current',8e22/(pi*(3500e3)**2),'A','μ=IπR² with R=3500km.')],'This is an equivalent current-loop model of Earth’s dipole moment.')
R(59,[N('a · Dipole moment',5*.3*.4/2,'A·m²','The right-triangle area isab/2.'),N('b · Torque magnitude',5*.3*.4/2*.080,'N·m','B lies in the loop plane, perpendicular to μ.')],'The triangle shape changes area, not the dipole-torque formula.')
R(60,V('Magnetic moment',[0,.15,-.30],'A·m²','Split along AD: xy rectangle has−z normal andxz rectangle has+y normal.'),'Area-vector sum is(.030j−.060k)m²; multiply by5A.')
mu=[0,-.024,0];B=[.002,-.003,-.004]
R(61,[N('a · Orientation energy',-sum(a*b for a,b in zip(mu,B)),'J','U=−μ·B with μ=−NiA j.')]+V('b · Torque',cross(mu,B),'N·m','τ=μ×B.'),'The indicated current at the near edge fixes the moment along−y.')
R(62,[N('Net moment after reversal',2e-5+(.007)*(.004),'A·m²','Graph interceptμ1=2×10⁻⁵ andslope−.004m²; reversing addsμ2=2.8×10⁻⁵.')],'Use the signed graph before reversing the current, then add the magnitudes.')
mu=scale([.6,-.8,0],.20*pi*.08**2);B=[.25,0,.30]
R(63,V('a · Torque',cross(mu,B),'N·m','Multiply the unit normal by iA, then cross with B.')+[N('b · Orientation energy',-sum(a*b for a,b in zip(mu,B)),'J','U=−μ·B.')],'The unit vector gives direction only; its magnitude must be scaled by iA.')
R(64,[N('Maximum angle',deg(acos(1-6.7e-4/5e-4)),'degrees','Graph minimum is−5×10⁻⁴J; set Uturn=−5×10⁻⁴+6.7×10⁻⁴=1.7×10⁻⁴J.')],'The graph amplitude is2.5Us=5×10⁻⁴J, notUs itself.')
R(65,[N('a · Field-moment angle',90,'degrees','Maximum torque requires sinθ=1.'),N('b · Optimal turn count',1,'turns','For fixed wire lengthL, NiA=iL²/(4πN), largest atN=1.',t=0),N('c · Maximum torque',.00451*.25**2/(4*pi)*.00571,'N·m','Use the one-turn circular areaL²/(4π).')],'Extra turns reduce the area enough to reduce the total magnetic moment.')
R(66,[C('Velocity at time t','v₀ₓ i + v₀ᵧ cos(ωt) j − v₀ᵧ sin(ωt) k, with ω=eB/m','v₀ₓ cos(ωt) i + v₀ᵧ j + v₀ₓ sin(ωt) k','v₀ₓ i + v₀ᵧ cos(ωt) j + v₀ᵧ sin(ωt) k','The Lorentz equations are dvy/dt=ωvz anddvz/dt=−ωvy; vx is constant.')],'Differentiate the proposed solution and check both the Lorentz force and initial velocity.')
R(67,[N('a · Minutes after 1PM',20,'min','Clockwise moment points into the face; crossed with B at 1oclock gives torque toward 4 o’clock.'),N('b · Torque magnitude',6*2*pi*.15**2*70e-3,'N·m','B lies in the clock plane, so τ=NiAB.')],'The given field is70mT; it lies in the clock face plane.')
R(68,V('Wire force',[0,0,.002*.300*.250**2/2],'N','For current along−y, dl×Bx points+z; integrate y from 0 to .250m.'),'The By term is parallel to current and gives no force.')
r1=sqrt(2*35*u*e*7300)/(e*.5);r2=sqrt(2*37*u*e*7300)/(e*.5)
R(69,[N('Detector separation',2*(r2-r1),'m','Each ion turns180°, so the detector displacement is a diameter; use2Δr.')],'Both ions have charge+e and gain the same kinetic energy.')
R(70,V('Minimum magnetic field',[0,0,-1e4/speed(2500*e,me)],'T','E+v×B=0 requires B into the page for rightward velocity and downward E.'),'Any parallel-to-velocity B would increase magnitude without affecting cancellation.')
R(71,[N('Iodine ion mass',e*.045*(1.29e-3/7)/(2*pi)/u,'u','Invert T=2πm/(eB), with T=total time/7.')],'Time is1.29ms, not one orbit; charge is singly ionized+e.')
R(72,[C('a · Minimum-field condition','B ≥ √(2mK)/(ed)','B ≥ √(2mK)/(2ed)','B ≥ 2mK/(ed)','Preventing contact requires orbital radiusr≤d; useK=mv²/2 andr=mv/(eB).'),C('b · Field orientation','Perpendicular to the emerging beam','Parallel to the emerging beam','Any orientation gives the same minimum','Only the perpendicular field bends the beam; a parallel component wastes field strength.')],'At equality the orbit is tangent to the plate, so a strict margin avoids even grazing contact.')
v=speed(12000*e,me);B=55e-6;rr=me*v/(e*B)
R(73,[N('a · Acceleration magnitude',e*v*B/me,'m/s²','Only the vertical component initially acts on the horizontal beam.'),N('b · Distance from x axis at x=.20m',rr-sqrt(rr*rr-.20**2),'m','Circle geometry gives y=r−√(r²−x²).')],'The stated horizontal magnetic component is unspecified. The textbook estimate neglects its later helical influence and uses the vertical-field circular arc.',scope='Part(b) uses the textbook vertical-field approximation. An exact trajectory including an unspecified horizontal field is not uniquely numerical; part(a) is exact at launch.',assumptions=['Use the given vertical Earth field55.0μT. For the textbook part(b) estimate neglect the unspecified horizontal field.'])
R(74,V('Magnetic field',[-3,-3,-4],'T','With Bx=By=b, Fz/q=2b−4b=6 implies b=−3; Fx/q=4Bz−6b=2 gives Bz=−4.'),'Solve all three Lorentz-force component equations with Bx=By and verify F·v=0.')
R(75,[N('a · Deuteron/proton radius ratio',sqrt(2),'dimensionless','At equalK, r∝√m/q.'),N('b · Alpha/proton radius ratio',1,'dimensionless','√4/2=1.')],'Compare equal energies, not equal accelerating voltages.')
R(76,[C('Charge-to-mass relation','q/m = E/(rBB′)','q/m = rBB′/E','q/m = EB/(rB′)','Velocity selector givesv=E/B; the analyzer givesq/m=v/(rB′).')],'Eliminate the common selected speed between the crossed-field and orbit equations.')
R(77,V('Electric field',[0,-500,0],'V/m','Undeflected beam requires E=−v×B; +x crossed with−z is+y.'),'The electron charge cancels in the zero-force condition.')
R(78,[C('a · Hall-to-longitudinal field ratio','E/Ec = B/(neρ)','E/Ec = neρ/B','E/Ec = Bneρ','HallE=vdB, current densityJ=nevd andlongitudinalEc=ρJ.'),N('b · Ratio for copper',.65/(8.47e28*e*1.69e-8),'dimensionless','Substitute copper resistivity1.69×10⁻⁸Ωm fromTable26-1.')],'Both fields scale with current density, so their ratio is independent of current.',pages=[27,32],assumptions=['Copper resistivity1.69×10⁻⁸Ω·m at the table reference temperature.'])
R(79,[N('a · Proton/alpha energy ratio',.5,'dimensionless','Equal voltage givesK=qV.'),N('b · Deuteron/alpha energy ratio',.5,'dimensionless','Both singly charged species gain half the alpha energy.'),N('c · Deuteron radius',.10*sqrt(2),'m','r∝√(m/q) at fixed voltage.'),N('d · Alpha radius',.10*sqrt(2),'m','Alpha m/q=2timesproton m/q.')],'Equal accelerating voltage differs from equal kinetic energy inP75.')
F=e*7.2e6*.083;ang=deg(asin(me*4.9e14/F))
R(80,[N('a · Maximum force',F,'N','Maximumsinθ=1.'),N('b · Minimum force',0,'N','Parallelmotiongiveszero.'),N('c · Acute angle',ang,'degrees','sinθ=ma/(evB).'),N('c · Supplementary angle',180-ang,'degrees','Sinehasthe samevalueatθand180°−θ.')],'Accelerationmagnitudealone permits two velocity-fieldangles.')
R(81,V('Net electromagnetic force',scale(add([0,300,0],cross([17000,-11000,7000],[-.020,0,0])),5e-6),'N','F=q(E+v×B), using5.0μC from the originalsource.'),'Evaluateelectricandmagneticcomponentsbeforeadding.')
vd=10e-6/(1.5*.01);nn=3/(e*vd*.01*10e-6)
R(82,[N('a · Drift speed',vd,'m/s','VH=Bvdw, with 10μV across 1cm.'),N('b · Carrier number density',nn,'m⁻³','I=nevdwt, using thickness t=10μm.'),C('c · Hall polarity for current +x and B +z','The −y edge is at lower potential for electron carriers','The +y edge is at lower potential for electron carriers','Both edges have equal potential','Electrons drift −x; v×B=+y, so their negative charge gives force −y and negative charge accumulates at −y.')],'Coordinate choices are stated explicitly for the polarity check. Charge accumulation creates the balancing Hall field.')
R(83,[N('Particle charge',-.48/(4000*sin(rad(37))*.005),'C','Fz=−qvyBx, so q=−Fz/(vyBx) with vy=v sin37°.')],'Thepositivezforcewithpositive vyandpositiveBxrequires negative charge.')
R(84,V('Wire force',[0,0,-3*.600/3],'N','Integrate i dx i×(−.600x² j), from 0 to 1m.'),'The x-directed field component contributes no transverse force.')
v=[-2,4,-6];B=[.002,-.004,.008];ff=scale(cross(v,B),e)
R(85,V('a · Force',ff,'N','Compute e(v×B).')+[N('b · Velocity-force angle',90,'degrees','A cross productis perpendicularto both inputs.'),N('c · Velocity-field angle',deg(acos(sum(a*b for a,b in zip(v,B))/(mag(v)*mag(B)))),'degrees','Use the full vector dot product.')],'Verify F·v=0 numerically as the zero-work condition.')
R(86,[N('a · Radius',me*40000/(e*60e-6),'m','Use the transverse40km/s and B=60μT.'),N('b · Pitch',32000*T(me,e,60e-6),'m','Pitch=vparallelT.'),C('c · Apparent spiral sense looking alongB','Counterclockwise','Clockwise','No spiral','For negative charge looking along+B, an initially upward transverse velocity curves left.')],'Use the originalmicroteslaunit; +xvelocityadvances alongthe field.')
voltage=.5*.060*(2*pi*4000)*.250**2
R(87,[C('a · Electron magnetic force in the figure','Up along the indicated conducting path','Down along the indicated conducting path','Zero everywhere','The right-hand rule for the indicated rotation and negativeelectroncharge pointsupward.'),C('b · Stronger force location','At the rim','Near the center','Same at both locations','v=ωr increaseswith radius.'),N('c · Work per unit charge along the conducting path, magnitude',voltage,'J/C','Integrate vBdr=ωB∫rdr.'),N('d · Device emf',voltage,'V','Emf isenergytransferredperunitcharge.'),N('e · Electric output power',50*voltage,'W','P=Iε.')],'The motor supplies electrical output energy; the ideal homopolar emf isBωR²/2.',scope='Part(c) is the motional emf/work-per-charge along the conducting path. The magnetic force does no net work on a freely moving charge; the driven rotor transfers mechanical energy through the constrained conducting path.')
R(88,[N('Charge in the current pulse',.010*sqrt(2*g*3)/( .100*.200),'C','ImpulseBL∫idt=mv0, with v0=√(2gh).')],'The pulseisshort, so neglect weight impulse during it and use ballistic rise afterward.')
R(89,[C('Minimum-field condition','B ≥ √(2mV/e)/d','B ≥ √(mV/(2e))/d','B ≥ √(2mV/e)·d','Crossed-fieldmotionfrom resthasmaximumtransversedisplacement2mE/(eB²); requirethis≤d with E=V/d.')],'Solve cycloidal motion under crossed electric and magnetic fields; a strictmargin avoids grazingcontact.')
R(90,[C('Maximum loop torque','τmax = |q|vrB/2','τmax = |q|vrB','τmax = 2|q|vrB','I=|q|v/(2πr), areaπr² andτmax=IAB.')],'Eliminate the period from the equivalent-current-loop model.')
R(91,[C('Carrier density','n = iB/(eVℓ)','n = eVℓ/(iB)','n = iBℓ/(eV)','Hall voltage spans widthw: V=Bvdw andi=nevdwℓ; eliminatevdandw.')],'The current thickness dimension isℓ; the other two rectangular dimensions cancel.')
# F=q v×B with v=(40000,35000,0),Bx0: Fx=q vyBz, Fy=−q vxBz.
R(92,V('Magnetic field',[0,0,-4.2e-9/(-e*35000)],'T','UseFx=qvyBz andFy=−qvxBz; Fz=0 with Bx=0 requiresBy=0.'),'The two measuredforcecomponentsyieldthe samepositiveBz.')
# Conceptual questions; diagrams independently read on PDF25–26.
def Q(n,p,w,pages=None):R(n,p,w,kind='questions',pages=pages)
Q(1,[C('a · Physically reasonable?','No','Yes','Only for a slower particle','The proposed force is not perpendicular to velocity.'),C('b · Physically reasonable?','Yes','No','Only for negative charge','For positive charge, northwest velocity crossed with leftwardB pointsout of the page.'),C('c · Physically reasonable?','No','Yes','Only for a stronger field','Velocity and B areparallel, so the magnetic forcevanishes.')],'Apply both perpendicularity and the right-hand rule.')
Q(2,[C('a · Hall-voltage magnitude ranking','3 = 4 > 1 = 2','1 = 2 > 3 = 4','1 = 2 = 3 = 4','Only perpendicular fields 3 and 4 deflect carriers.'),C('b · Top at higher potential','4','3','1 and2','Electron drift isleftward; anoutward field pushesnegativecarriersdownward.')],'Account for negative mobile charges and their drift opposite conventional current.')
Q(3,[C('a · Voltage-magnitude ranking','±z > ±y > ±x','±y > ±z > ±x','All six are equal','B isalongx; motionalfieldsalongyspan2d, whilealongzspand.'),C('b · Front face at lower potential','Motion along +y','Motion along −y','Motion along +x','Forv=+y and B=+x, E=−v×B=+z; potentialdecreases toward the front(+z).')],'The frontface is the positive z face shownin the perspective diagram.')
forn=['Into the page','Out of the page','Out of the page','Into the page','Into the page','Out of the page']
Q(4,[C(z+' · Field direction',a,'Out of the page' if a=='Into the page' else 'Into the page','Parallel to the page','The electron curves according to negativeq timesv×B in this segment.') for z,a in zip('abcdef',forn)],'Deflection toward thehigher-potential plate identifies a negative particle; use each local curvature.')
Q(5,[C('a · Speed below E/B','Electric force dominates','Magnetic force dominates','The forces remain equal','qE exceeds|q|vB.'),C('b · Speed above E/B','Magnetic force dominates','Electric force dominates','The forces remain equal','|q|vB exceeds|q|E.')],'Compare magnitudes without changing the opposing directions.')
Q(6,[C('Particles accelerating out of the page','2, 5, 6, 9, and 10','1, 2, 7, and 8','3, 4, 5, and 6','B pointsleft and E into thepage. Applyeach charge sign toE+v×B; only 2 overcomes E through speed.')],'Parallel-to-B velocities have no magnetic force; negative charges9and10 respond outward to E.')
Q(7,[C('a · Stronger field','B₁','B₂','Equal fields','Smaller radius requires stronger B at fixed momentum.'),C('b · Field directions','B₁ into the page; B₂ out of the page','B₁ out of the page; B₂ into the page','Both into the page','Follow the electron arrow and local centripetal force.'),C('c · Time in B₁ relative to B₂','Less','Greater','Equal','Half-circle time πm/(eB) decreaseswith B.')],'The particle speed is unchanged by both magnetic regions.')
Q(8,[C('a · Higher-potential top-pair plate','Upper plate','Lower plate','Equal potentials','At the top, electron moves left; magnetic force is down, so electric force must point up and Edown.'),C('b · Higher-potential bottom-pair plate','Lower plate','Upper plate','Equal potentials','At bottom electron moves right, reversing the required E.'),C('c · Magnetic-field direction','Out of the page','Into the page','Parallel to the straight sections','Leftward electroncurvingdown requires outward B.')],'InferBfrom the curved sections, then balanceforcesin the straight sections.')
Q(9,[C('a · Agent work for 2→1','Positive','Negative','Zero','U=−μBcosθ rises when changingfrom acute to obtuse alignment.'),C('b · Agent-work ranking','2→1 = 2→4 > 2→3','2→3 > 2→1 = 2→4','2→1 > 2→4 > 2→3','Orientations 1 and 4have same cosine;2 and 3have equal energy.')],'Use the referenced Checkpoint 5 orientations rather than only the chapter-end figure.',pages=[24,26])
paths=['i','e','c','a','g','j','d','b','h','f','k']
Q(10,[C(f'Particle {j} · Path',a,('b' if a!='b' else 'c'),('a' if a not in ['a','b'] else 'g'),'Match r=mv/(|q|B), charge sign, and incoming velocity; the neutral particle takesk.') for j,a in enumerate(paths,1)],'The tiny-radius negative particle 7 takesd, identifying B into thepage; radius ratios then map all remaining paths.')
Q(11,[C('a · Charge sign','Negative','Positive','Zero','Leftward entry bends downwardinoutward B; apositive chargewouldbendup.'),C('b · Final speed','Equal to v₀','Greater than v₀','Less than v₀','Magnetic force does no work.'),C('c · Time at half the entry speed','Equal to T₀','Greater than T₀','Less than T₀','Half-circle time is independent ofspeed.'),C('d · Fraction of circle at half speed','A half-circle','More than a half-circle','Less than a half-circle','The new smaller circle still intersects the straight boundary after180°.')],'The radius changes with speed while the angular frequency remains fixed.')
Q(12,[C('a · Period ranking','1 = 2 = 3','3 > 2 > 1','1 > 2 > 3','T=2πm/(qB), independent ofpitchangle.'),C('b · Frequency ranking','1 = 2 = 3','3 > 2 > 1','1 > 2 > 3','Frequencyistheinverseof the sameperiod.'),C('c · Pitch ranking','3 > 2 > 1','1 > 2 > 3','1 = 2 = 3','Pitch=vparallelT; parallel velocity is largest in 3 and zero in 1.')],'All particleshavethe same charge,mass,speedand field; only thevelocity orientationdiffers.')
# Conventional angle equivalents, preserving their physical meaning.
for r in rows:
 for p in r['parts']:
  if p['type']=='numeric' and p['unit']=='degrees' and any(z in p['label'].lower() for z in ['direction','angle']) and not any(z in p['label'].lower() for z in ['acute','supplementary','initial','next-rest','maximum','velocity-field','velocity-force','field-moment','from vertical']):p['acceptedValues']=[p['answer']-360,p['answer']+360]
source=json.loads(gzip.decompress((ROOT/'site/questions/physics.json.gz').read_bytes()));ids={q['id'] for q in source if q['chapter']==28}
assert {r['id'] for r in rows}==ids and len(rows)==104
for r in rows:
 for p in r['parts']:
  assert p['type'] in ['numeric','choice']
  if p['type']=='numeric':assert math.isfinite(p['answer']) and (p['answer']==0 or p['tolerance']<abs(p['answer'])),(r['id'],p)
  else:assert len(set(p['options']))==3 and p['answer'] in p['options'],(r['id'],p)
(H/'ch28.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'records',sum(len(r['parts']) for r in rows),'fields')
