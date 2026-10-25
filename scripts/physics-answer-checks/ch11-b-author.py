"""Original source-reviewed derivations, Halliday ch11 problems38–86."""
import json,math,gzip
from pathlib import Path
H=Path(__file__).resolve().parent
pi=math.pi;g=9.8
records=[]
def n(label,a,unit,why,tol=None):
 return dict(label=label,type='numeric',answer=a,unit=unit,tolerance=tol if tol is not None else max(abs(a)*.003,1e-9),explanation=why)
def c(label,a,wrong,why):
 return dict(label=label,type='choice',answer=a,options=[a,*wrong],explanation=why)
def add(num,parts,why,assumptions=None,pages=None):
 page=29 if num<=46 else 30 if num<=59 else 31 if num<=69 else 32
 records.append(dict(id=f'physics-chapter-11-problems-{num}',parts=parts,reasoning=why,sourcePages=pages or [page],assumptions=assumptions or []))
add(38,[n('a · Angular momentum',16*.033,'kg·m²/s','Angular impulse is ΔL=τΔt=16(0.033)=0.528 kg·m²/s.'),n('b · Angular speed',16*.033/.0012,'rad/s','ω=L/I=0.528/0.0012=440 rad/s.')],'Integrate the constant torque over 0.033 s, then divide angular momentum by rotational inertia.',['Disk starts from rest; if it initially rotates, 0.528 is the change in angular momentum.'])
W=(.8**2-3**2)/(2*.140)
add(39,[n('a · Average torque magnitude',(3-.8)/1.5,'N·m','|τavg|=|Lf−Li|/Δt.'),n('b · Rotation angle',(3+.8)/(2*.140)*1.5,'rad','For constant angular acceleration, θ=(ωi+ωf)Δt/2.'),n('c · Work done on wheel',W,'J','W=ΔK=(Lf²−Li²)/(2I), negative because the wheel loses energy.'),n('d · Average power delivered by flywheel (positive magnitude)',-W/1.5,'W','Power delivered is (Ki−Kf)/Δt=19.9048 W. The signed average power done on the flywheel is −19.9048 W.')],'Use τ=dL/dt, ω=L/I, and K=L²/(2I).',['Part(d) uses the positive power supplied by the slowing flywheel, consistent with the printed answer convention.'])
add(40,[n('Angular momentum at t=3.00 s',23,'kg·m²/s','L(3)=L(1)+∫₁³(5+2t)dt=5+[5t+t²]₁³=23.')],'Angular impulse, rather than instantaneous torque times the full elapsed time, changes L.')
I=19/6*2*.5**2
add(41,[n('a · Rotational inertia',I,'kg·m²','A hoop about its in-plane tangent has I=(1/2+1)mR². The square has I=(1+1/3+1/3)mR². Total I=(19/6)mR².',.05),n('b · Angular momentum',I*2*pi/2.5,'kg·m²/s','L=Iω with ω=2π/T.',.05)],'The pictured axis runs along one side of the square and tangent to the hoop, not through the hoop center. Sum the four rod inertias and apply the parallel-axis theorem to the hoop.')
add(42,[n('a · Angular momentum at 7.0 s',24,'kg·m²/s','Positive areas from 0–2,2–4,4–7 s are 8,7,9 N·m·s, totaling24.',.1),n('b · Angular momentum at 20 s',1.5,'kg·m²/s','Continue the signed area: L(20)=24+3−4.5−18−3=1.5.',.1)],'Graph vertices (t,τ) are (0,4),(2,4),(4,3),(7,3),(9,0),(12,−3),(18,−3),(20,0), in SI units. Initial L=0; integrate each rectangle/trapezoid.')
add(43,[n('a · Initial circle radius',1.5,'m','Each equal-mass skater is half the3.0 m separation from the center.'),n('b · Initial angular speed',1.4/1.5,'rad/s','ω=v/r.'),n('c · Initial system kinetic energy',98,'J','K=2(1/2)(50)(1.4²).'),n('d · Angular speed at 1.0 m separation',8.4,'rad/s','I decreases by (0.5/1.5)²=1/9; conserving L increases ω ninefold.'),n('e · Final system kinetic energy',882,'J','Kf=1/2[2(50)(0.5²)](8.4²)=882 J.',5),c('f · Source of added kinetic energy','Work done by the skaters, using internal chemical energy',['Work done by the frictionless ice','Angular momentum supplied by the pole'],'Pulling inward converts the skaters’ chemical energy into kinetic energy while net external torque remains negligible.')],'Conserve angular momentum about the two-skater center of mass. Kinetic energy increases because internal forces perform positive work.')
add(44,[n('a · Final angular speed',(.17*.15*2-.005*2.8)/(.005+.17*.15**2),'rad/s','Taking counterclockwise positive, Li=mvR−Iω0=0.037; If=I+mR²=0.008825. Final rotation is counterclockwise.'),c('b · Is mechanical energy conserved?','No; some kinetic energy becomes internal energy',['Yes; angular momentum conservation guarantees it','No; all angular momentum is lost'],'The cockroach stops relative to the disk through internal friction. Angular momentum is conserved, but mechanical energy decreases.')],'Add signed cockroach and disk angular momenta, then use the combined final inertia.',['Stops means the cockroach is at rest relative to the lazy Susan, not relative to the ground.'])
add(45,[n('a · Final angular speed',3.6,'rev/s','ωf=(Ii/If)ωi=(6/2)(1.2).'),n('b · Kinetic energy ratio Kf/Ki',3,'','At constant L, K=L²/(2I), so Kf/Ki=Ii/If.'),c('c · Source of added energy','Muscular work converts chemical energy into rotational kinetic energy',['The frictionless bearing supplies energy','Conservation of angular momentum creates energy'],'Moving the bricks inward requires work; torque-free rotation conserves L, not K.')],'Conserve angular momentum for the man, bricks, and platform.')
add(46,[n('Kinetic energy ratio Kf/Ki',3,'','Kf/Ki=Ii/If=3 when If=Ii/3.')],'With no external torque, L stays constant and rotational kinetic energy is inversely proportional to I.')
add(47,[n('Wheel angular speed',.15/(2.1*.43),'rad/s','Let ωw oppose the train. The train speed relative to ground is0.15−Rωw. Zero total L gives mR(0.15−Rωw)−1.1mR²ωw=0.',.005)],'The specified train speed is relative to the track, so the wheel motion must be included. The wheel turns opposite the train.')
add(48,[n('Cockroach inertia divided by disk inertia',6/5-1,'','Idisk(6)=(Idisk+Icock)(5), so Icock/Idisk=6/5−1=0.20.')],'The graph starts at6rad/s at r=0 and ends at5rad/s at r=R. Use angular momentum conservation.')
add(49,[n('a · Final speed when both initially turn counterclockwise',750,'rev/min','ωf=(3.3·450+6.6·900)/(3.3+6.6)=750.'),n('b · Final speed when second disk initially turns clockwise',450,'rev/min','The signed result is (3.3·450−6.6·900)/9.9=−450 rev/min.'),c('c · Final direction in the opposite-spin case','Clockwise',['Counterclockwise','No rotation'],'With counterclockwise positive, the conserved net angular momentum is negative.')],'Use signed initial angular momenta and the sum of the final inertias.')
add(50,[n('Rotor revolutions about an inertial axis',500,'rev','Integrating Ipωp+Imωm=0 gives |θm|=(Ip/Im)|θp|=6000(30°)=500rev.',1)],'The rotor and probe rotate in opposite directions. Relative to the probe the rotor makes500+1/12rev; the inertial-axis count is500rev.',['Initial total angular momentum is zero; the answer label specifies the inertial-axis convention.'])
add(51,[n('a · Final angular speed',800/3,'rev/min','Iiωi=(Ii+2Ii)ωf.'),n('b · Fraction of initial rotational energy lost',2/3,'','Kf/Ki=Ii/(3Ii)=1/3, so the lost fraction is2/3.')],'Coupling conserves angular momentum but dissipates kinetic energy.')
add(52,[n('a · Final angular speed',.260*3/2.25,'rad/s','Idisk=2mR²; initial total3mR² and final total(2+1/4)mR².'),n('b · Kinetic energy ratio',3/2.25,'','Kf/Ki=Ii/If=3/2.25.'),c('c · Why does kinetic energy increase?','The cockroach does work while walking inward',['The axle exerts a driving torque','Angular momentum increases because the radius decreases'],'Its internal chemical energy is converted to mechanical energy; total L is unchanged.')],'The cockroach ends at r=R/2, so its orbital inertia is one quarter of its initial value.')
I=4*.5**2/12+.003*.25**2
add(53,[n('Bullet speed',I*10/(.003*.25*math.sin(pi/3)),'m/s','mvr sin60°=(ML²/12+mr²)ω. Use r=L/2=.250m and include the lodged bullet inertia.',50)],'Conserve angular momentum about the fixed rod center during the short collision. Only the perpendicular component of bullet momentum contributes.')
Ii=.5*8*(.8**2+.4**2)+2*.8**2;If=.5*8*(.8**2+.4**2)+2*.4**2
add(54,[n('Increase in kinetic energy',.5*(Ii*8)**2/If-.5*Ii*8**2,'J','Iring=M(R1²+R2²)/2=3.20. Ii=4.48, If=3.52kg·m²; ΔK=L²/(2If)−L²/(2Ii).')],'Conserve L=Iiωi while the cat moves from R2 to R1. The cat supplies the increase through work.')
add(55,[n('Final angular speed',.0005*4.7/(.0005+.020*.10**2),'rad/s','The falling putty has zero initial angular momentum about the vertical axis. Iω=(I+mR²)ωf.',.05)],'The vertically falling putty increases the rotational inertia without bringing vertical-axis angular momentum.')
add(56,[n('Total arm angular momentum (uniform-sweep model)',(4*.6**2/3)*(1.5*2*pi/.7),'kg·m²/s','Each arm has I=mℓ²/3=.48. Their angular speeds sum to(0.5+1.0)2π/.700, so Lsum=6.4627.')],'Both arms sweep in the same angular sense to take up body angular momentum.',['Treat each angular sweep as uniform; without that assumption the supplied sweeps determine the time-average L, not a unique instantaneous value.'])
add(57,[n('a · Final angular velocity',20*45.5/49.5,'rad/s','Initially I=(45+0.5)mr². The small disk center finally lies2r from the axis, adding4mr².',.5),n('b · Energy ratio K/K0',45.5/49.5,'','At constant L the energy ratio is I0/I=45.5/49.5.')],'Use the parallel-axis theorem for the off-center small disk: I=m r²/2+m(2r)².')
add(58,[n('Final angular speed',(300+60*2**2)*1.5/(300+60*.5**2),'rad/s','(300+60·2²)1.5=(300+60·0.5²)ωf.')],'Treat the slowly walking student as a point mass at her stated radial position.')
add(59,[n('Ejected particle speed',11,'m/s','With r=.4m, Irod=M(.8²)/12. Conservation gives (Irod+Mr²/3)20=Irodωf+(M/3)r vp, while vp=rωf+6. Solve ωf=12.5 and vp=11.')],'The particle leaves in the forward tangential direction shown. Its speed is6m/s greater than the new rod-end speed, not the old speed.')
I=.060+(.50+.001)*.60**2
add(60,[n('a · Total rotational inertia',I,'kg·m²','Add Irod and the block-plus-bullet point-mass inertia:0.060+0.501(0.60²).'),n('b · Bullet speed',I*4.5/(.001*.60),'m/s','m v ℓ=Itotalω immediately across the collision.')],'The axle supplies no angular impulse about A, so angular momentum about A is conserved during impact.')
add(61,[n('Angular speed after collision',.12*2.4/(.12+.20*.60**2),'rad/s','Irodωi=(Irod+mputtyL²)ωf.')],'The initially stationary putty adds orbital inertia at the rod end.')
add(62,[n('Angular speed in tuck',(pi*19.9/3.93+7*pi)/1.87,'rad/s','The two extended quarter-turns totalπrad; tucked rotation totals7πrad. With ω1=(I2/I1)ω2, t=[π(I1/I2)+7π]/ω2.')],'Use conserved angular momentum and add the time spent in the extended and tucked orientations; the angular speeds are not equal.')
add(63,[n('Angular speed just after catch',1*12*2*math.cos(math.radians(37))/(150+31*2**2),'rad/s','The tangential speed component is v cosφ. Thus m v R cosφ=(Idisk+(mchild+mball)R²)ωf.')],'The given angle is measured from the tangent, so use cosine rather than sine. The caught ball adds to final inertia.')
add(64,[n('Angular speed ratio ωf/ωi',(1.44+.660)/(.660+2*1.44*math.sin(pi/6)**2),'','Each leg contribution scales as sin²θ. Ii=1.44+.660; If=.660+2(1.44)sin²30°=1.38.')],'The initial extended leg contributes1.44kg·m²; the other leg is along the axis. In the final pose both legs contribute. Angular momentum gives ωf/ωi=Ii/If.')
I=(4+.05)*.25**2;omega=.05*3*.25/I;K=.5*I*omega**2
add(65,[n('a · Angular speed just after impact',omega,'rad/s','Angular momentum about the central pivot:mp v r=(2mball+mp)r²ω.'),n('b · Ratio of post-impact energy to incident putty energy',K/(.5*.05*3**2),'','Compute Kafter=Iω²/2 and divide by mp v²/2.'),n('c · Total clockwise angle before first stop',180+math.degrees(math.asin(K/(.05*g*.25))),'°','The equal balls’ gravitational energy changes cancel. With clockwise θ from horizontal, ΔU=−mpgr sinθ. Set Kafter=ΔU, selecting the first stop after passing180°.',.5)],'The putty first moves downward, passes the opposite horizontal position, then stops slightly above it. Do not choose the small arcsine branch near0°.')
I=.1*.4**2/3+.05*.4**2;v=math.sqrt(2*g*.2);L=.05*v*.4;K=L**2/(2*I)
add(66,[n('Maximum angle from vertical',math.degrees(math.acos(1-K/(g*(.1*.2+.05*.4)))),'°','v=√(2gh). After sticking, K=(mvℓ)²/(2I), I=Mℓ²/3+mℓ². The rise costs g(Mℓ/2+mℓ)(1−cosθ).')],'Use energy for the slide, angular momentum for the inelastic impact, then energy for the swing; kinetic energy is not conserved during impact.')
add(67,[n('a · Impact distance d',(.6**2/12*80)/(40/3),'m','For zero final L, (Mℓ²/12)ω=(M/3)vd.'),c('b · Rotation when d exceeds this value','Clockwise',['Counterclockwise','Stationary for every d'],'The downward particle arriving to the right of the axis brings negative angular momentum. At larger d it outweighs the rod’s initial positive L.')],'Set opposite angular momenta equal to find d=.180m.')
add(68,[n('a · Precession angular speed',.5*g*.04/(.0005*30*2*pi),'rad/s','Ω=mgl/(Iωspin); ωspin=30·2πrad/s. The sin30° factor cancels between torque and the precessional change in L.'),c('b · Precession direction viewed from above','Clockwise',['Counterclockwise','No precession'],'The spin angular momentum has a downward component; the gravitational torque gives clockwise steady precession for that spin sense.')],'Use the rapid-spin, steady-precession approximation.',['Spin angular momentum dominates the angular momentum due to precession.'])
add(69,[n('Precession rate',g*.055/(.5*.5**2*(1000*2*pi/60)),'rad/s','The center lies half the11cm axle length from the support. Ω=mg(.055)/[(mR²/2)ωspin]; mass cancels.')],'Use lever arm0.055m, not the full axle length, and convert rev/min to rad/s.')
add(70,[n('Initial center-of-mass speed',math.sqrt(10/7*g*1.5*math.sin(pi/12)),'m/s','For a solid ball, K=(7/10)mv². Set this equal to mg(s sin15°).')],'Rolling without slipping conserves total kinetic plus gravitational potential energy.')
add(71,[n('a · Center-of-mass acceleration',1.6,'m/s²','Translation: F+f=ma. Clockwise torque: (F−f)R=(mR²/2)(a/R). Thus a=4F/(3m).'),n('b · Angular acceleration magnitude',16,'rad/s²','|α|=a/R=1.6/.10.'),c('c · Friction force vector','(4.0 N) î',['−(4.0 N) î','(12 N) î'],'f=ma−F=16−12=+4N. Static friction points right in this top-pull geometry.')],'The line pulls tangentially at the cylinder top. Static friction acts in the same horizontal direction as the applied force to enforce rolling.')
add(72,[n('Translational-to-rotational energy ratio',1,'','For a thin-walled pipe I=mR² and v=Rω; mv²/2=Iω²/2.')],'Use the thin cylindrical-shell inertia about its central lengthwise axis.')
add(73,[c('a · Angular momentum about origin','0',['−30t³ k̂ kg·m²/s','30t³ k̂ kg·m²/s'],'The car moves on the x-axis, so r and p are parallel.'),c('b · Torque about origin','0',['−90t² k̂ N·m','90t² k̂ N·m'],'The force also lies along the x-axis; r×F=0.'),c('c · Angular momentum about (2,5,0) m','−30t³ k̂ kg·m²/s',['30t³ k̂ kg·m²/s','−90t² k̂ kg·m²/s'],'ry=−5m, px=3(−2t³); Lz=−ry px=−30t³.'),c('d · Torque about (2,5,0) m','−90t² k̂ N·m',['90t² k̂ N·m','−30t³ k̂ N·m'],'Differentiate Lz=−30t³, or use Fx=m dvx/dt=−18t² and τz=−ryFx.'),c('e · Angular momentum about (2,−5,0) m','30t³ k̂ kg·m²/s',['−30t³ k̂ kg·m²/s','90t² k̂ kg·m²/s'],'Here ry=+5m, reversing the sign of Lz.'),c('f · Torque about (2,−5,0) m','90t² k̂ N·m',['−90t² k̂ N·m','30t³ k̂ N·m'],'τz=d(30t³)/dt=90t².')],'Use r relative to each specified reference point. The x coordinate of the reference point does not affect r×p when py=0.',['t is in seconds and t>0; +z points out of the xy plane.'])
add(74,[n('Time to zero angular speed',600/50,'s','The opposing angular impulse must equal600kg·m²/s: τt=600.')],'A constant torque opposite the initial angular momentum first brings L to zero in12s.')
I=180*.91**2;L=44*3*1.2
add(75,[n('a · Merry-go-round rotational inertia',I,'kg·m²','I=Mk²=180(.910²)=149.058.'),n('b · Initial child angular momentum',L,'kg·m²/s','For a tangential approach L=mvR=44(3)(1.2)=158.4.'),n('c · Final angular speed',L/(I+44*1.2**2),'rad/s','ωf=mvR/(Mk²+mR²)=158.4/212.418=0.7456995rad/s.',.001)],'Add the child’s final point-mass inertia to the platform inertia and conserve angular momentum.',['The supplied givens imply0.7456995rad/s; the previously imported key value0.744 is not the direct result of those givens.'])
M=2640*.20*.15*.012;I=M*(.20**2+.15**2)/12+M*(.25*math.sqrt(.20**2+.15**2))**2
add(76,[n('Rotational kinetic energy',.104**2/(2*I),'J','M=ρabc=.9504kg. Ic=M(a²+b²)/12; the displaced axis is at d=√(a²+b²)/4=.0625m. I=Ic+Md²=.0086625; K=L²/(2I).')],'Convert dimensions and density to SI, use the parallel-axis theorem, then use K=L²/(2I).')
add(77,[n('a · Angular momentum magnitude about midpoint',2.90e-4*5.46*.042,'kg·m²/s','Each particle contributes m v(d/2) with the same sign; total magnitude mvd.'),c('b · Does a different reference point change the result?','No',['Yes','Only if the point is outside the two paths'],'For opposite momenta total P=0, so shifting the origin leaves total L unchanged.'),n('c · Magnitude at midpoint after reversing one particle',0,'kg·m²/s','Equal parallel momenta now give opposite equal angular momenta about a midpoint between the paths.',1e-9),c('d · Can changing the reference point now change the result?','Yes',['No','Only the kinetic energy changes'],'Now total P is nonzero. Shifting a reference point perpendicular to P changes L by −a×P.')],'Distinguish the opposite-velocity case (zero net momentum) from the same-velocity case (nonzero net momentum).')
a=43**2/(2*225)
add(78,[n('a · Linear acceleration magnitude',a,'m/s²','0=v0²−2aΔx, so a=43²/450.'),n('b · Angular acceleration magnitude',a/.250,'rad/s²','Rolling gives |α|=a/R.'),n('c · Frictional torque magnitude',.155*a/.250,'N·m','|τ|=I|α|.')],'Assume uniform deceleration and no slipping until rest.')
add(79,[n('a · IA/IB for equal angular momenta',1/3,'','Belt speeds match: ωARA=ωBRB, so ωA=3ωB. Equal Iω requires IA/IB=1/3.'),n('b · IA/IB for equal rotational kinetic energies',1/9,'','Equal Iω² requires IA/IB=(ωB/ωA)²=1/9.')],'The belt constrains tangential speeds, not angular speeds.')
add(80,[c('Angular momentum vector after collision','5.55 k̂ kg·m²/s',['−5.55 k̂ kg·m²/s','1.95 k̂ kg·m²/s'],'Total p=(18î−7.5ĵ)kg·m/s. At r=(−.5î−.1ĵ)m, Lz=rxpy−rypx=3.75+1.80=5.55.')],'Linear momentum is conserved in the completely inelastic collision; compute r×ptotal at its location.')
add(81,[n('a · Rotational kinetic energy',58.8,'J','The rolling radius is the axle radius0.200m. I/(mr²)=1.5, so rotation receives1.5/2.5 of the98J gravitational drop.'),n('b · Translational kinetic energy',39.2,'J','Translation receives1/2.5 of mgs sin30°=98J.')],'The wheel does not touch the ramp; v=r_axle ω. Using the0.400m wheel radius would give the wrong energy split.')
I=(10/g)*6**2/3
add(82,[n('a · Rotational inertia about the end',I,'kg·m²','Mass is weight/g. For a uniform rod about an end, I=(W/g)L²/3.'),n('b · Angular momentum magnitude',I*240*2*pi/60,'kg·m²/s','Convert240rev/min to8πrad/s and compute Iω.')],'The given10.0N is weight, not mass.')
K=.7*(36/g)*4.9**2
add(83,[n('a · Total kinetic energy at bottom',K,'J','For a solid sphere, K=(1/2+1/5)mv²=(7/10)(W/g)v².'),n('b · Distance along incline',K/(36*.5),'m','At the turning point K=W s sin30°, giving s=3.43m.'),c('c · Does the distance depend on sphere mass?','No',['Yes, proportional to mass','Yes, inversely proportional to mass'],'Both initial energy and gravitational work are proportional to mass, which cancels.')],'Use total rolling energy, including spin, rather than translational energy alone.')
I=950e-7;m=.120;r=.0032;ell=1.20;v0=1.3;a=g/(1+I/(m*r*r));v=math.sqrt(v0*v0+2*a*ell);omega=v/r;Kt=.5*m*v*v;Kr=.5*I*omega**2
add(84,[n('a · Time to string end',(v-v0)/a,'s','Solve ℓ=v0t+(1/2)at² with a=g/[1+I/(mr²)].'),n('b · Total kinetic energy at end',Kt+Kr,'J','Ktotal=1/2(m+I/r²)v²=Kinitial+mgℓ.'),n('c · Final linear speed',v,'m/s','v²=v0²+2aℓ.'),n('d · Translational kinetic energy',Kt,'J','Kt=mv²/2.'),n('e · Angular speed',omega,'rad/s','No slip between axle and string gives ω=v/r.'),n('f · Rotational kinetic energy',Kr,'J','Kr=Iω²/2.')],'Reuse Problem17: I=950g·cm²=9.50×10⁻⁵kg·m², m=.120kg, r=.0032m, string length1.20m. Unlike P17, include the initial rolling kinetic energy.',['Initial axle/string motion is nonslipping, so ω0=v0/r.'],[28,32])
add(85,[c('a · Merry-go-round angular speed','mvR/(I+MR²)',['mvR/I','mv/(I+MR²)'],'Initial L=0. Afterward rock momentum gives mvR balanced by the opposite platform-plus-girl angular momentum (I+MR²)ω.'),c('b · Girl linear speed','mvR²/(I+MR²)',['mvR/(I+MR²)','mvR²/I'],'The girl stays on the rim; her speed is Rω.')],'The stated rock speed is relative to ground, so no moving-platform velocity correction is needed. The girl and platform move opposite the rock.')
add(86,[c('a · Rotational inertia','(1/2)mR²',['mR²','(2/5)mR²'],'mgh=(1/2)mv²+(1/2)I(v/R)². Insert h=3v²/(4g) and solve I=mR²/2.'),c('b · A body consistent with this inertia','A uniform solid cylinder or disk rolling on its rim',['A thin-walled hollow cylinder','A uniform solid sphere'],'A solid cylinder/disk has I=mR²/2 about its symmetry axis; a hoop and solid sphere have different factors.')],'Use energy conservation and the rolling constraint to identify the inertia coefficient.')
# A distinct verification note accompanies every source-derived exercise.
checks={
38:"τΔt and Iω both give 0.528 kg·m²/s; torque impulse has angular-momentum units.",
39:"The negative work equals τθ with the braking sign; its magnitude divided by 1.5 s is the positive delivered power. All four values match printed-key rounding.",
40:"Differentiating L(t)=5t+t²−1 recovers τ(t), and L(1)=5.",
41:"Independent rod contributions are 0, mR², mR²/3, mR²/3, and the hoop contributes 3mR²/2; both answers match printed-key rounding.",
42:"The signed graph areas are 8+7+9+3−4.5−18−3; summing only through 7 s gives 24 and through 20 s gives 1.5.",
43:"Initial and final Iω each equal 210 kg·m²/s; final energy is nine times initial energy. Numeric values match printed-key rounding.",
44:"Final Iω reproduces the signed initial angular momentum 0.037 kg·m²/s. Final energy is below the initial 0.3596 J, consistent with dissipation.",
45:"Initial and final Iω agree; at fixed L the energy rises threefold. Both numeric answers match the existing key.",
46:"Substitution into K=L²/(2I) gives a factor of three, with no dimensions in the ratio.",
47:"Substitution makes train and wheel angular momenta equal and opposite; the speed matches printed-key rounding.",
48:"With Icock=0.2Idisk, final L=1.2Idisk·5 equals initial Idisk·6.",
49:"Weighted initial angular momenta divided by 9.90 kg·m² reproduce +750 and −450 rev/min; both speed magnitudes match the existing key.",
50:"Ipθp+Imθm=0 after converting both angular displacements into revolutions; the two signs are opposite.",
51:"Final Iω equals initial Iω, while final energy is one third of initial energy; both values match printed-key rounding.",
52:"Final inertia times final speed equals 0.780mR²/s; the energy increase is consistent with positive internal work.",
53:"Substituting the derived v into mvr sin60° yields Ifω=0.835208 kg·m²/s; it agrees with the printed 1.3×10³ m/s after rounding.",
54:"Final speed follows from equal Iω; evaluating both kinetic energies separately gives the same positive ΔK.",
55:"Multiplying final combined inertia by final speed reproduces 0.00235 kg·m²/s; the answer matches printed-key rounding.",
56:"The two arm contributions add to (mℓ²/3)(3π/0.700), with angular-momentum units; without uniform sweeps this is the time-average value.",
57:"45.5·20=49.5·ωf after canceling mr²; the energy ratio is below one and both answers match printed-key rounding.",
58:"540·1.5=315·ωf=810 kg·m²/s; moving inward increases the speed.",
59:"The solved speeds satisfy vp−0.4ωf=6 and both sides of the angular-momentum equation equal (2.13333M) in SI units; the 11 m/s answer matches the key.",
60:"The computed bullet speed gives incoming angular momentum equal to 0.24036·4.5=1.08162 kg·m²/s.",
61:"Initial L=0.288 kg·m²/s equals (0.120+0.072)·1.5; the answer matches the key.",
62:"Using ωextended=ωtucked·3.93/19.9 makes π/ωextended+7π/ωtucked equal the full 1.87 s.",
63:"Final total inertia times ωf equals the incoming tangential angular momentum 24cos37°; the result matches printed-key rounding.",
64:"The initial inertia is 2.10 and the final inertia is 1.38 kg·m²; multiplying the final inertia by the speed ratio recovers the initial inertia.",
65:"Collision Iω equals incoming mvr; the energy ratio is below one. At the first stopping angle, the putty rise stores the post-impact kinetic energy. All three numbers match key rounding.",
66:"The final angle gives (1−cosθ)=0.15, so the potential increase 0.392·0.15 equals post-impact energy 0.0588 J.",
67:"At d=0.180 m the particle and rod angular momenta cancel; increasing d makes the clockwise incoming contribution larger. The distance matches the key.",
68:"The precession magnitude satisfies ΩL sin30°=mgℓ sin30°. The torque direction gives clockwise precession for the stated clockwise spin.",
69:"The lever arm is half the axle length, mass cancels, and Ω has units s⁻¹; the value matches printed-key rounding.",
70:"Substitution gives (7/10)mv²=mg·1.5sin15°; the inferred speed is smaller than the corresponding sliding-particle speed.",
71:"F+f=16 N=ma and (F−f)R=0.8 N·m=Iα; the acceleration results match the existing key.",
72:"Substituting I=mR² and ω=v/R makes the two energies identical for every m,R,v.",
73:"For each reference point, differentiating the angular-momentum result gives its torque result; right-hand-rule signs also follow directly from −ry px.",
74:"The opposing impulse 50·12=600 N·m·s cancels the initial angular momentum exactly.",
75:"Final inertia 212.418 kg·m² times 0.745699517 rad/s equals initial 158.4 kg·m²/s. The old key's 0.744 does not reproduce that equality.",
76:"Directly computing ω=L/I and then Iω²/2 gives the same energy as L²/(2I); density conversion gives mass 0.9504 kg.",
77:"Adding the individual cross products gives mvd for opposite momenta and zero at the midpoint for parallel momenta; origin dependence follows from L′=L−a×P. Numeric values match the key.",
78:"Using t=v0/a gives displacement v0t/2=225 m; αR=a and Iα recovers the torque, with consistent SI units.",
79:"With ωA=3ωB, substitution gives equal Iω for ratio 1/3 and equal Iω² for ratio 1/9. Both agree with printed-key rounding.",
80:"Summing each incoming particle's r×p independently gives +3.75+1.80=+5.55 along k̂, agreeing with the total-momentum cross product.",
81:"The two energies sum to 98 J=mgh and their ratio 1.5 equals I/(mr_axle²); both match the existing key.",
82:"Using the mass 10/g and angular speed 8π yields the required kg·m² and kg·m²/s dimensions; treating newtons as kilograms would fail this check.",
83:"The energy equals the incline gravitational work 36·3.43·sin30°; mass cancels in the distance expression and numeric answers match key rounding.",
84:"Independently check final total energy against initial total energy plus mg·1.20; Ktranslation+Krotation agrees and ωr=v.",
85:"The proposed platform-plus-girl angular momentum is −mvR, canceling the rock's +mvR; multiplying ω by R gives the girl's speed with velocity units.",
86:"Substituting I=mR²/2 gives total initial energy 3mv²/4=mgh, exactly reproducing the specified maximum height."
}
assert set(checks)==set(range(38,87))
for rec in records:
 rec['reasoning']+=' Verification: '+checks[int(rec['id'].split('-')[-1])]
assert {int(r['id'].split('-')[-1]) for r in records}==set(range(38,87))
for rec in records:
 for p in rec['parts']:
  assert p['explanation'] and p['label']
  if p['type']=='numeric':assert math.isfinite(p['answer'])
  else:assert p['answer'] in p['options'] and len(set(p['options']))==len(p['options'])
(H/'ch11-b.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print('Wrote',len(records),'records;',sum(len(r['parts']) for r in records),'fields')
# Independently source-derived answers compared with the old printed-key fields.
root=H.parents[1];source=json.load(gzip.open(root/'site/questions/physics.json.gz'));lib=json.load(gzip.open(root/'site/questions/answer-library-physics.json.gz'))['questions'];qm={q['id']:q for q in source}
audit=[]
for rec in records:
 old=lib.get(rec['id'],{}).get('grader',qm[rec['id']].get('grader'))
 if not old:continue
 olds=old.get('parts',[old]);new=rec['parts']
 for index,p in enumerate(olds):
  if p.get('type')!='numeric':continue
  label=p.get('label','');matches=[x for x in new if x['type']=='numeric' and (x['label'].startswith(label+' ·') if label else len(new)==1)]
  if len(matches)!=1:continue
  now=matches[0];delta=abs(now['answer']-p['answer']);ok=delta<=p.get('tolerance',0)+1e-12
  audit.append(dict(id=rec['id'],part=now['label'],derived=now['answer'],oldKey=p['answer'],oldKeyTolerance=p.get('tolerance'),withinPrintedRounding=ok))
(H/'ch11-b-audit.json').write_text(json.dumps({'sourcePagesVisuallyReviewed':[29,30,31,32],'referencedPriorProblem':17,'comparisons':audit,'discrepancies':[x for x in audit if not x['withinPrintedRounding']]},indent=2)+'\n')
print('Key comparisons',len(audit),'discrepancies',[x for x in audit if not x['withinPrintedRounding']])
