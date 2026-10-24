#!/usr/bin/env python3
"""Original source-reviewed contracts for all26 Chapter4 Problems Plus."""
from common import *
import mpmath as mp
from scipy.optimize import minimize_scalar
R=s.Rational;pi=s.pi;mp.mp.dps=50

def pp(no,*fields,why,limited=False):put('chapter-04-problems-plus',no,list(fields),why,limited,suffix='-problems-plus-0')
pp(1,c('Maximizing upper vertices','(±1/√2,e^(−1/2))','(±1,1/e)','(±√2,e^(−2))'),n('Maximum area',s.sqrt(2/s.E)),c('Second derivative','(4x²−2)e^(−x²)'),why='Equal upper heights on the Gaussian force symmetric vertices±t. Area2t e^(−t²) has derivative2e^(−t²)(1−2t²), so its unique positive maximum is t=1/√2, exactly the inflection abscissas.',limited=True)
pp(2,c('Equivalent identity','sinx−cosx=√2 sin(x−π/4)','sinx−cosx=2sin(x−π/4)','sinx−cosx=sin(x+π/4)'),c('Equality locations','x=3π/4+kπ, k∈ℤ','x=kπ','x=π/4+kπ'),why='A sine has absolute value at most1. The identity gives the stated bound and equality precisely where the shifted sine equals±1.',limited=True)
pp(3,c('Absolute maximum','e^45','e^5','e^(−4)'),n('Maximum attained at x',-5),c('Absolute minimum','None; infimum0 is approached as x→±∞','0, attained at x=2','e^(−4)'),why='Forx≤2 the exponent is45−(x+5)²; forx≥2 it is5−(x−5)². Compare the two branch maxima. Exponentials are positive but approach0 at both infinite ends.')
pp(4,n('Maximum product',16),c('Equality conditions','|x|=|y|=√2','|x|=|y|=2','x=y=0'),c('One-variable bound','u(4−u)=4−(u−2)²≤4 for0≤u≤4'),why='Setu=x²,v=y². Both factorsu(4−u),v(4−v) are nonnegative and at most4, so their product is at most16.',limited=True)
pp(5,c('Inflection-point equation','(2−x²)sinx−2xcosx=0, x≠0'),c('Resulting locus','y²(x⁴+4)=4'),why='The second derivative is[(2−x²)sinx−2xcosx]/x³. At an inflection point, square2xcosx=(2−x²)sinx and use sin²+cos²=1 to obtain4x²=(x⁴+4)sin²x. Divide byx². The removable extension at0 has second derivative−1/3 and is not an inflection.',limited=True)
pp(6,n('Point x',1/s.sqrt(3)),n('Point y',R(2,3)),n('Minimum triangle area',4*s.sqrt(3)/9),why='Atx=t>0 the tangent is y=1+t²−2tx. Positive intercepts give area(1+t²)²/(4t); its derivative has sign3t²−1 and both endpoint limits are infinite.')
pp(7,n('a+b+c+d',24),c('Necessary cancellation','b+c+d=0','b+c+d=8','a=0'),why='The linear term in the numerator must vanish for a finite two-sided limit. Withb+c+d=0, sine terms areO(x³), so the limit isa/3=8. Thusa=24 and the requested sum is24.')
pp(8,n('Limit',R(2,3)),why='Factorx^(1/x) out of numerator and denominator. The remaining differences are exp(log(1+2/x)/x)−1 and exp(log(1+3/x)/x)−1; their leading terms2/x² and3/x² give2/3.')
pp(9,n('Highest point x',-2),n('Highest point y',4),n('Lowest point x',2),n('Lowest point y',-4),why='Completing the square gives(x+y/2)²+3y²/4=12, so |y|≤4 with equality atx=−y/2.')
pp(10,c('Region including boundary','−x−e^x≤y≤−x+e^x, for every real x','−e^x≤y≤e^x','y≥e^x−x'),c('Left-hand asymptote of both boundary curves','y=−x','y=0','x=0'),why='Resolve the absolute-value inequality into−e^x≤x+y≤e^x. Shade between the two graphs; their gap2e^x is always positive and tends to0 asx→−∞.',limited=True)
pp(11,c('Second intersection Q','(−a−1/(2a),(a+1/(2a))²)'),c('(a) minimizers for all nonzero real a','a=±1/√2; the pictured positive branch gives1/√2','Only a=1/√2 when negative a is allowed','a=±1'),n('(a) minimum y-coordinate of Q',2),c('(b) minimizers for all nonzero real a','a=±1/√2; the pictured positive branch gives1/√2','a=±1','a=±1/2'),n('(b) shortest length',3*s.sqrt(3)/2),why='Normal slope is−1/(2a). Factoring its intersection withy=x² gives second root−a−1/(2a). Its squared ordinate is minimized at a²=1/2; length=(4a²+1)^(3/2)/(4a²) has the same minimizing a². Include the symmetric negative solution because the text allows any nonzero a.',limited=True)
pp(12,c('Parameter range with inflection points','c>0 or c<−e/6','c≠0','c≥−e/6'),c('At c=−e/6','The second derivative vanishes at1 but does not change sign, so there is no inflection','One inflection at1','Two inflections'),c('Number of inflections','One for c>0; two for c<−e/6; zero otherwise'),why='y″=6cx+e^x. Forc>0 it crosses once at negative x. Forc<0 positive zeros solve e^x/x=−6c; this ratio has minimum e atx=1. Equality is a double zero without a concavity change.')
pp(13,n('Minimizing a',(1+s.sqrt(5))/2),c('Equal-side length as a function of a','a√((a+1)/(a−1)), a>1'),why='The base is tangent at y=−1. The unit-radius tangent condition gives equal-side length a(a+1)/√(a²−1). Differentiating its logarithm gives1/a−1/(a²−1)=0, hence the golden ratio; both endpoint limits are infinite.')
pp(14,c('Region in rotated coordinates u=x−y,v=x+y','max(0,2|u|−u²)≤v²≤u²+2|u|','v²≤u² only','v²≥u²+2|u|'),c('Boundary treatment','Include the boundaries, since both source inequalities are non-strict','Exclude every boundary','Include only the origin'),why='Use2xy=(v²−u²)/2 andx²+y²=(u²+v²)/2. Rearranging both inequalities gives the displayed exact description, sufficient to sketch symmetric lobes; it does not grade the drawing.',limited=True)
pp(15,c('Maximizing P','(m/2,m²/4)'),c('Condition for two distinct intersections','m²+4b>0','m²+4b=0','m²+4b<0'),why='BaseAB is fixed, so maximize perpendicular distance from P=(t,t²) to the chord. This distance is(mt+b−t²)/√(1+m²), maximized at t=m/2, the midpoint of the intersection abscissas.')
pp(16,n('Minimum triangle area',R(1,4),'m²'),n('Maximum triangle area',1/(2*s.sqrt(3)),'m²'),c('Minimum crease intercepts','AE=AF=1/√2 m'),c('Maximum crease intercepts','{AE,AF}={1,1/√3} m'),why='Let e=AE,f=AF, each at most1. Reflection movesA a unit distance, so its distance from the crease is1/2:ef/√(e²+f²)=1/2. Thus4e²f²=e²+f². Minimize/maximizeef/2 under0<e,f≤1; equality e=f gives the minimum, an endpoint e=1 orf=1 the maximum.')
pp(17,c('All positive a with an intersection','0<a≤e^(1/e)','a≥1 only','All a>0'),c('Intersection counts','One for0<a≤1; two for1<a<e^(1/e); one tangent intersection at a=e^(1/e)'),why='An intersection hasx>0 and a=x^(1/x). This function increases from0 to its maximume^(1/e) atx=e, then decreases to1 from above.')
pp(18,n('a',R(1,2)),why='The logarithm of the limit islim x[ln(1+a/x)−ln(1−a/x)]=2a; e^(2a)=e givesa=1/2.')
pp(19,c('Key derivative','f′(0)=Σ[k=1..n] k a_k'),c('Bound','|f′(0)|≤1'),why='Since f(0)=0, divide |f(x)|≤|sinx| by|x| and pass to the limitx→0. The differentiable finite sine sum has derivativeΣk a_k at0.',limited=True)
pp(20,c('A(θ) for radius r','r²(θ−sinθ)/2'),c('B(θ) for radius r','r²[tan(θ/2)−θ/2]'),n('Limit A/B',2),why='Subtract the central triangle from the sector forA, and subtract the sector from the two tangent triangles forB. Their leading small-angle terms arer²θ³/12 andr²θ³/24.')
u=(208-6*s.sqrt(110))/289;c1=R(50,13);c2=c1/u;hh=s.sqrt(30)/13
pp(21,c('(a) T₁','D/c₁'),c('(a) T₂','2h/(c₁cosθ)+(D−2h tanθ)/c₂'),c('(a) T₃','√(D²+4h²)/c₁'),c('(b) minimizing angle','sinθ=c₁/c₂, provided D−2h tanθ≥0'),n('(c) c₁',c1,'km/s',.0005),n('(c) c₂',c2,'km/s',.0005),n('(c) h',hh,'km',.00005),c('Admissibility of the second algebraic root','Reject it because it makes the lower-layer segment RS negative','Accept both roots as physical paths','Reject both roots'),why='Angleθ is measured from the vertical. DifferentiateT₂:2h sec²θ(sinθ/c₁−1/c₂). UseT₁=.26 andT₃=.34 to getc₁=50/13,h=√30/13. Settingu=c₁/c₂ inT₂=.32 yields289u²−416u+136=0; choose the smaller root to satisfyRS≥0.',limited=True)
pp(22,c('Parameter range','|c|>4√2','|c|≥4√2','c≠0'),why='Four intersections imply, by repeated Rolle, two distinct zeros off″=12x²+6cx+24, requiringc²>32. Conversely shiftx by−c/4 and subtract a suitable line: the quartic becomesz⁴+(12−3c²/8)z²+constant, a double well when c²>32. A horizontal level between its minima and central maximum gives four distinct roots.')
pp(23,c('Height ED as a function of x','ℓ+√(r²−x²)−√(d²−2dx+r²)'),c('Equilibrium x','r[r+√(r²+8d²)]/(4d)'),c('Parameters absent from maximizing x','W and ℓ','d and r','Only r'),why='The vertical rope remainder isℓ−BF, and EF=√(r²−x²). Differentiate the height; the stationary equation factors as(x−d)(2dx²−r²x−dr²)=0 after squaring. Since d>r, rejectx=d and the negative root. The positive root lies inside(0,r) and is the maximum.',limited=True)
pp(24,c('Square-pyramid minimizing height','h=4r'),c('Regular n-gon minimizing height','h=4r for every integer n≥3'),c('General volume as a function of h','V=nr²tan(π/n)h²/[3(h−2r)], h>2r'),why='A section through the apex and a side midpoint gives base apothem²=r²h/(h−2r). The base area isn·apothem²·tan(π/n). Differentiateh²/(h−2r), which has its unique minimum ath=4r.')
pp(25,n('Additional melting time',3/(2**R(1,3)-1),'hours',.0005),c('Why radius shrinks linearly','4πR²R′=−k·4πR² impliesR′=−k','The volume is linear in time','The area is constant'),why='After3hours radius isR₀2^(−1/3), so the loss3k=R₀(1−2^(−1/3)). Remaining timeR₀2^(−1/3)/k=3/(2^(1/3)−1); this is additional, not total elapsed time.')
pp(26,c('Maximum height for n chambers','1+√n'),c('Inductive step with next radius r','1+max[0≤r≤1]{√(1−r²)+r√(n−1)}'),c('Maximizing next radius','r=√((n−1)/n)'),c('Equality construction radii','1,√((n−1)/n),√((n−2)/n),…,1/√n'),why='Base case n=1 has height2. Above the original center, the first chord plane rises√(1−r²); induction and scaling give top height r√(n−1) above that plane. Cauchy–Schwarz bounds their sum by√n, attained at r=√((n−1)/n). Add the unit distance from sphere bottom to center.',limited=True)
# Independent symbolic/numerical checks; these certify results, not full student proofs.
y=s.symbols('y',real=True);a=s.symbols('a',positive=True);t=s.symbols('t',positive=True)
check('PP1 optimum derivative',s.diff(2*x*s.exp(-x*x),x).subs(x,1/s.sqrt(2)))
check('PP1 inflection derivative',s.diff(s.exp(-x*x),x,2).subs(x,1/s.sqrt(2)))
check('PP4 square-completion identity',x*x*(4-x*x)-(4-(x*x-2)**2))
check('PP5 second derivative',s.diff(s.sin(x)/x,x,2)-((2-x*x)*s.sin(x)-2*x*s.cos(x))/x**3)
check('PP6 optimal tangent triangle',s.diff((1+x*x)**2/(4*x),x).subs(x,1/s.sqrt(3)))
for xx,yy in [(-2,4),(2,-4)]:check('PP9 ellipse '+str(yy),xx*xx+xx*yy+yy*yy-12)
q=-a-1/(2*a);check('PP11 normal intersection',q*q-a*a+(q-a)/(2*a))
check('PP11 ordinate optimum',s.diff(q*q,a).subs(a,1/s.sqrt(2)))
check('PP11 length optimum',s.diff((4*a*a+1)**3/(16*a**4),a).subs(a,1/s.sqrt(2)))
check('PP13 optimum',s.diff(a*a*(a+1)/(a-1),a).subs(a,(1+s.sqrt(5))/2))
check('PP14 transformed upper constraint',2*(x*x+y*y)-(x-y)**2-(x+y)**2)
check('PP16 minimum fold distance',4*R(1,2)*R(1,2)-R(1,2)-R(1,2))
check('PP16 maximum fold distance',4*R(1,3)-1-R(1,3))
check('PP17 maximum loga derivative',s.diff(s.log(x)/x,x).subs(x,s.E))
check('PP20 ratio limit',s.limit((x-s.sin(x))/(2*s.tan(x/2)-x),x,0)-2)
check('PP21 reflection time',(1+4*hh*hh)/c1**2-R(34,100)**2)
check('PP21 root equation',289*u*u-416*u+136)
check('PP24 optimum derivative',s.diff(x*x/(x-2),x).subs(x,4))
check('PP25 radius endpoint',1-(3+3/(2**R(1,3)-1))*(1-2**(-R(1,3)))/3)
def near(actual,wanted,label,tol=1e-9):
 assert abs(float(actual)-float(wanted))<=tol*max(1,abs(float(wanted))),(label,actual,wanted)
 TESTS.append(dict(label=label,actual=float(actual),expected=float(wanted)))
for z in [10,100,1000,10000]:
 v=mp.expm1(mp.log1p(mp.mpf(2)/z)/z)/mp.expm1(mp.log1p(mp.mpf(3)/z)/z)
 near(v,R(2,3),'PP8 convergence at'+str(z),.04 if z==10 else 1/z)
near(2*float(hh)/(float(c1)*math.sqrt(1-float(u)**2))+(1-2*float(hh)*float(u)/math.sqrt(1-float(u)**2))/float(c2),.32,'PP21 refracted time')
assert 1-2*float(hh)*float(u)/math.sqrt(1-float(u)**2)>0
for radius,distance in [(1,2),(2,3),(.5,5),(3,3.1)]:
 xx=radius*(radius+math.sqrt(radius*radius+8*distance*distance))/(4*distance)
 H=lambda z:math.sqrt(radius*radius-z*z)-math.sqrt(distance*distance-2*distance*z+radius*radius)
 opt=minimize_scalar(lambda z:-H(z),bounds=(0,radius),method='bounded',options={'xatol':1e-12})
 near(xx,opt.x,'PP23 numerical global optimum',1e-6)
for nn in range(2,15):
 rr=math.sqrt((nn-1)/nn);near(1+math.sqrt(1-rr*rr)+rr*math.sqrt(nn-1),1+math.sqrt(nn),'PP26 equality construction n='+str(nn))
 for rr in [.1,.3,.7,.9]:assert 1+math.sqrt(1-rr*rr)+rr*math.sqrt(nn-1)<=1+math.sqrt(nn)+1e-12
for v in OUT.values():v['objectiveCheckVersion']=3
finish('problems-plus')
audit_path=Path(__file__).parent/'problems-plus-audit.json';audit=json.loads(audit_path.read_text());audit.update(source='Stewart8e supplied chapter04.pdf, local89–90 / printed363–364, both pages visually inspected including diagrams.',sourceSHA256=hashlib.sha256((ROOT/'site/books/calculus/chapter-04.pdf').read_bytes()).hexdigest(),scope='All26 actual Problems Plus records. Drawings and complete proofs remain limited recognition checks.',importantConventions=['PP11 includes both symmetric signs because the text allows every nonzero a; the pictured positive branch matches the printed statement.','PP21 angle measured from vertical; reject the algebraic root that makes RS negative.','PP25 requests additional time after the initial3hours.','PP26 induction uses a scaled stack of hemispheres above the chord plane.'])
audit_path.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
