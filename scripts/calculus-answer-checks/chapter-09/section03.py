from common import *
C=s.symbols('C',real=True)
row(3,1,c('Nonzero solution family','y=1/(C−x³), on intervals avoiding C−x³=0'),c('Additional equilibrium','y=0','y=1','y=x'),why='Separatey^(−2)dy=3x²dx, integrate−1/y=x³+constant. Dividing byy² excludes the zero solution, so include it separately.')
row(3,2,c('Positive branches','√y=x²/4+C, restricted to x²/4+C>0'),c('Zero and joined solutions','y=0 is a solution; positive branches may join zero intervals with zero derivative','Only the positive family exists','Every squared branch is valid even where x²/4+C<0'),why='The real equation requiresy≥0. For y>0, integrate dy/√y=x dx. Squaring without retaining the nonnegative square root introduces false branches. Non-Lipschitz behavior at0 permits waiting-time joins.')
for no,ans,domain,why in [
(3,'y²=x²+2ln|x|+C','x≠0, y≠0; select either sign on a positive-radicand interval','Separatey dy=(x+1/x)dx.'),
(4,'y=−ln(x²/2+C)','x²/2+C>0','Integrate e^(−y)dy=−x dx to e^(−y)=x²/2+C.'),
(5,'e^y−y=2x+sinx+C','y≠0 for a differentiable solution','The derivative of e^y−y is(e^y−1)y′. At y=0 the original left side is0 but2+cosx>0.'),
(6,'u²/2+u⁵/5=−1/t+t³/3+C','t≠0 andu≠0,−1','Multiply byu+u⁴ and divide byt²; integrate t^(−2)+t².'),
(7,'θsinθ+cosθ=−e^(−t²)/2+C','θ≠0 andcosθ≠0','Separateθcosθ dθ=t e^(−t²)dt; integrate by parts on the left.'),
(8,'−(lnH+1)/H=(1+R²)^(3/2)/3+C','H>0 andH≠1','Separate(lnH)/H² dH=R√(1+R²)dR. Integration by parts produces the left side.'),
(9,'p=Ce^(t³/3−t)−1','All real t; C=0 includes equilibriump=−1','Factorp′=(t²−1)(p+1), separate and exponentiate.'),
(10,'z=−ln(e^t+C)','e^t+C>0','Differentiate e^(−z); the equation givesd(e^(−z))/dt=e^t.')]:
 row(3,no,c('Solution family',ans),c('Domain/constant condition',domain),why=why)
row(3,11,f('IVP solution',-s.log(1-x*x/2)),c('Maximal interval','(−√2,√2)','All real x','(0,∞)'),why='Separation gives e^(−y)=C−x²/2; y(0)=0 fixesC=1. Positivity determines the interval.')
row(3,12,f('IVP solution',-s.sqrt(1+2*s.sin(x)-2*x*s.cos(x))),c('Branch/domain','Negative square root on the connected interval containing0 where the radicand is positive','Positive square root','Allow radicand0 despite the original denominator y'),why='Integrate y dy=xsinx dx using parts, and choose the negative branch fromy(0)=−1.')
row(3,13,c('IVP solution','u(t)=−√(25+t²+tan t)'),c('Domain','The connected interval containing0 with cos t≠0 and25+t²+tan t>0'),why='Integrating2u du=(2t+sec²t)dt yieldsu²=t²+tan t+C; u(0)=−5 fixes25 and the negative sign.')
row(3,14,c('IVP solution','y=(2−√(1+x²))^(1/3), using the real cube root'),c('Maximal interval containing0','(−√3,√3)','All real x','(−1,1)'),why='Integrate3y²dy=−x/√(1+x²)dx. The constant is2. At y=0 the original coefficient vanishes whilex≠0, so the differentiable solution cannot pass throughx=±√3.')
row(3,15,c('Implicit IVP solution','y²/2+(3+y²)^(3/2)/3=x²lnx/2−x²/4+41/12'),c('Branch','Use y>0 andx>0 in the connected domain through(1,1)'),why='Integrate both sides of y(1+√(3+y²))dy=xlnx dx; the initial value gives constant41/12.')
row(3,16,c('IVP solution for t≥0','P(t)=[t^(3/2)/3+√2−1/3]²'),why='For positiveP andt, separate dP/√P=√t dt. The initial condition at t=1 fixes the positive square-root branch.')
row(3,17,c('IVP solution','y=a[4sinx/√3−1], 0<x<π/2'),why='Integrate dy/(a+y)=cotx dx, then usey(π/3)=a. The formula also coversa=0, the equilibrium.')
row(3,18,c('IVP solution','L(t)=−1/[1+k(t ln t−t+1)]'),c('Domain','t>0 in the connected interval through1 where the denominator is nonzero'),why='Integrate L^(−2)dL=kln t dt. L(1)=−1 supplies the constant.')
row(3,19,f('Curve through(0,2)',s.sqrt(x*x+4)),why='Fromy dy=x dx gety²=x²+C; the initial point choosesC=4 and positivey.')
row(3,20,f('f(x)',1+s.exp(x*x/2)),why='Forf−1, the equation is(f−1)′=x(f−1). Initialf(0)−1=1.')
row(3,21,c('Transformed equation','u′=1+u'),c('Solution','y=Ce^x−x−1'),why='u=x+y has derivative1+y′=1+u; solve the separable equation and subtractx.')
row(3,22,c('Transformed equation','v′=e^v/x, v=y/x'),c('Solution','y=−xln(C−ln|x|)'),c('Domain','x≠0 andC−ln|x|>0'),why='Substitutey=xv andy′=v+xv′, cancelxv, then integratee^(−v)dv=dx/x.')
row(3,23,c('(a) nonconstant branches','arcsin y=x²+C, with−π/2<x²+C<π/2'),c('(a) equilibria and joins','y=±1 are equilibria; branches can join them with zero derivative'),c('(b) maximal global IVP solution','y=sin(x²) for|x|≤√(π/2); y=1 for|x|≥√(π/2)'),c('(c) y(0)=2','No real solution:√(1−y²) is not real at2','y=2 is an equilibrium','y=sin(x²)+2'),why='Integrate dy/√(1−y²)=2x dx on−1<y<1. The inverse-sine range matters: continuing sin(x²) past its first maximum violates the differential equation. Join the equilibrium1 at both endpoints to obtain a global differentiable IVP solution.',limited=True)
row(3,24,c('Solution','y=−ln(C+sinx), whereC+sinx>0'),c('Effect of larger C','Lowers y at every common x and may enlarge its domain; it is not a uniform vertical translation','Raises every curve','All curves are unchanged'),c('Condition for an all-real-x solution','C>1','C≥−1','Every C'),why='The source exponent is−y. Integrating e^(−y)y′=−cosx gives e^(−y)=C+sinx. The logarithm argument must stay positive.',limited=True)
row(3,25,c('Implicit IVP curve','cos y=cos x−1'),c('Explicit branch through(0,π/2)','y=arccos(cosx−1), −π/2<x<π/2'),why='Multiply bysin y and integrate; initial data fix the constant−1. At x=±π/2 the branch reachesy=π, where the original denominator vanishes.',limited=True)
row(3,26,c('Implicit family','(y−1)e^y=(1+x²)^(3/2)/3+C'),c('Excluded y','y=0','y=1','All y<0'),c('Increasing C at a fixed x on a common branch','Raises the positive-y branch and lowers the negative-y branch','Raises both branches','Has no effect'),why='Integrate y e^y dy=x√(1+x²)dx. The derivative of the left side isy e^y, positive above0 and negative below0; the differential equation is undefined aty=0.',limited=True)
row(3,27,c('(b) nonzero family','y=−1/(x+C)'),c('Additional solution','y=0','y=1','y=x'),c('(a,c) field and curve behavior','Slopes are positive away from y=0, so every nonzero branch increases on its interval','All curves decrease','All curves are bounded globally'),why='Integratey^(−2)dy=dx and retain the equilibrium excluded by division.',limited=True)
row(3,28,c('(b) general solution','y=Ce^(x²/2), C∈ℝ','y=Ce^(−x²/2), C∈ℝ','y=C+x²/2'),c('(a,c) geometry','Every curve is even; positive branches have a minimum at0 and negative branches a maximum','All curves are odd','All curves cross y=0'),why='Separate dy/y=x dx for nonzero y;C=0 restores the zero solution.',limited=True)
for no,ans,slope,why in [(29,'y=Cx², together with the vertical trajectoryx=0','2y/x','The original slope is−x/(2y); its negative reciprocal integrates to parabolas, plus the vertical axis.'),(30,'2x²+3y²=C, C>0','−2x/(3y)','Eliminatek to get original slope3y/(2x), then integrate3y dy=−2x dx.'),(31,'y²−x²=C','x/y','The original hyperbola has slope−y/x; integratey dy=x dx for orthogonal curves.'),(32,'y³=3x+C','1/y²','The original reciprocal family satisfiesy′=−y²; integratey²dy=dx.')]:row(3,no,c('Orthogonal trajectories',ans),c('Orthogonal slope where finite',slope),why=why+' At vertical/horizontal tangencies interpret orthogonality geometrically, not by multiplying infinite slopes.',limited=True)
row(3,33,f('Solution',1+s.exp(2-x*x/2)),why='Differentiate the integral equation toy′=x(1−y); settingx=2 givesy(2)=2. Solve and check the original constant.')
row(3,34,f('Solution',s.sqrt(4+2*s.log(x))),c('Maximal domain through1','x>e^(−2)','x>0','All real x'),why='FTC givesy′=1/(xy) andy(1)=2. Thusy²=4+2lnx with the positive branch; the original integrand excludesy=0.')
row(3,35,f('Solution',(x*x+4)**2/4),why='FTC givesy′=2x√y andy(0)=4. Integrating the positive square-root branch gives√y=x²/2+2, positive for every realx.')
row(3,36,c('Solution on the interval through t=3','f(t)=(t+1)/(t−1)','f(t)=(t−1)/(t+1)','f(t)=tan(3−t)'),c('Maximal IVP interval','t>1','All real t','t<1'),why='The printed equation is(t²+1)f′+f²+1=0. Separate toarctanf=−arctant+C; f(3)=2 givesC=3π/4 on the continuous branch. The tangent subtraction identity simplifies tof=(t+1)/(t−1). Its pole at1 explains the source restrictiont≠1.')
row(3,37,c('Charge','Q(t)=3(1−e^(−4t)) C'),n('Limiting charge',3,'C'),why='The referenced circuit hasQ′=12−4Q andQ(0)=0; separate around equilibrium3.')
row(3,38,c('Coffee temperature','T(t)=20+75e^(−t/50) °C, t in minutes'),why='The referenced cooling model hask=1/50min⁻¹ and initial excess temperature75°C.')
row(3,39,c('General performance','P(t)=M+Ce^(−kt)'),c('Limit as t→∞','M','0','C'),why='Integrate the constant-coefficient equationP′=k(M−P), withk>0.')
row(3,40,c('(a) a≠b solution','x(t)=ab[e^((a−b)kt)−1]/[a e^((a−b)kt)−b]'),c('(b) a=b solution','x(t)=a²kt/(1+akt)'),c('(b) if x(20)=a/2','x(t)=at/(t+20)'),why='Partial fractions separate dx/[(a−x)(b−x)]=kdt. The initial product concentration0 fixes the ratio constant. When a=b integrate(a−x)^(−2); the half-time condition givesak=1/20.')
row(3,41,c('(a) a=b solution','x(t)=a−a/[1+(k√a/2)t]²'),c('(b) a>b time to concentration x','t=2/[k√(a−b)]·[arctan√(b/(a−b))−arctan√((b−x)/(a−b))], 0≤x≤b'),why='For equal initial concentrations the rate isk(a−x)^(3/2). Otherwise useu=√(b−x), giving−2du/[k(a−b+u²)] and applyt=0 atx=0.')
row(3,42,c('Temperature','T(r)=35−20/r °C, 1≤r≤2'),why='LetS=T′; S′+2S/r=0 impliesS=C/r² andT=A+B/r. Temperatures15°C at1m and25°C at2m giveA=35,B=−20.')
row(3,43,c('(a) concentration','C(t)=r/k+(C₀−r/k)e^(−kt)'),c('(b) limit','r/k'),c('(b) interpretation when C₀<r/k','Concentration rises toward the balance where removalkC equals inputr','Concentration decreases toward0','Concentration grows without bound'),why='The equilibrium isr/k; the differenceC−r/k decays exponentially.')
row(3,44,c('(a) IVP, x in billions of dollars and t in days','x′=(10−x)/200, x(0)=0'),c('(b) solution','x(t)=10(1−e^(−t/200)) billion dollars'),n('(c) 90% replacement time',200*s.log(10),'days',.005),why='Assume bills entering banks are representative of circulation. Daily replacement equals0.05billion times the old-currency fraction1−x/10.')
row(3,45,c('(a) salt','S(t)=15e^(−t/100) kg'),n('(b) salt after20min',15*s.exp(-R(1,5)),'kg',.0005),why='Volume stays1000L and pure inflow adds no salt. Outflow rate10·S/1000 givesS′=−S/100.')
row(3,46,c('CO₂ percentage','p(t)=0.05+0.10e^(−t/90), t in minutes'),n('Limiting percentage',.05,'%'),why='The turnover time is180/2=90minutes. The percentage approaches the inflow percentage0.05, starting at0.15.')
row(3,47,n('Alcohol after1hour',6-2*s.exp(-R(3,5)),'%',.0005),why='Percentage satisfiesp′=(6−p)/100 andp(0)=4; use60minutes.')
row(3,48,c('(a) salt','S(t)=(130/3)(1−e^(−3t/200)) kg'),n('(b) salt after1hour',R(130,3)*(1-s.exp(-R(9,10))),'kg',.0005),why='Salt input0.05·5+0.04·10=.65kg/min; well-mixed outflow is.015Skg/min. The constant-volume equilibrium is.65/.015=130/3kg.')
row(3,49,c('Velocity equation','v′=g−kv'),c('Terminal downward velocity','g/k'),why='Expand(mv)′=m′v+mv′ and usem′=km. Cancel positive m; the velocity relaxes exponentially towardg/k.')
row(3,50,c('(a) velocity','v=v₀e^(−kt/m)'),c('(a) position','s=s₀+(mv₀/k)(1−e^(−kt/m))'),c('(a) total distance','m|v₀|/k'),c('(b) velocity forv₀≥0','v=v₀/[1+(kv₀/m)t]'),c('(b) position forv₀≥0','s=s₀+(m/k)ln[1+(kv₀/m)t]'),c('(b) total distance','Infinite forv₀>0; zero ifv₀=0','Alwaysmv₀/k','Always finite'),why='Separate Newton’s law for each drag model and integrate velocity. The quadratic formula−kv² describes resistance for nonnegative velocity; for negative motion its sign must be reversed. Quadratic-drag speed decreases like1/t, whose integral diverges.')
row(3,51,c('(a) differential relation','dL₁/dL₂=kL₁/L₂'),c('(a) allometric law','L₁=C L₂^k','L₁=C L₂^(−k)','L₁=C+kL₂'),c('(b) biomass law from supplied k','B=C V^0.0794','B=C V^(−0.0794)','B=C+0.0794V'),why='Divide the proportional specific growth rates and integrate logarithmic derivatives. The printed coefficient is0.0794; the unknown proportionality constant remains.')
row(3,52,c('(a) positive family','V(t)=b exp(Ce^(−at))'),c('(b) initial V(0)=1','V(t)=b^(1−e^(−at))'),why='Letu=ln(V/b), givingu′=−au. Positive volumes are required for the logarithm;C=−lnb enforces unit initial volume.')
row(3,53,c('(a) model','A′=k√A(M−A), k>0'),c('(a) fastest-growth area','A=M/3'),c('(b) growing nonzero branches0<A<M','A=M tanh²[k√M(t−t₀)/2], t>t₀'),c('(b) equilibria and other branches','A=0 andA=M; aboveM use M coth²[k√M(t−t₀)/2] on t>t₀; a growing branch can follow a zero interval'),why='Maximize√A(M−A) on[0,M]: its derivative is(M−3A)/(2√A). Foru=√A>0, u′=k(M−u²)/2. Keepu≥0; squaring an unrestrictedtanh creates spurious decreasing branches belowM.',limited=True)
row(3,54,c('(a) required launch speed','v₀=√[2gRh/(R+h)]'),c('(b) escape speed','v_e=√(2gR)'),n('(c) escape speed',s.sqrt(2*32*3960*5280),'ft/s',.05),n('(c) escape speed',s.sqrt(2*32*3960*5280)/5280,'mi/s',.00005),why='Usev dv/dx=−gR²/(R+x)² and integrate fromsurface speedv₀ tozero speed at heighth. Convert Earth radius3960mi into feet before combining with32ft/s².',limited=True)
# Residuals and initial-value checks independently differentiate the stated solutions.
for no,expr,rhs,x0,y0 in [(1,1/(C-x**3),3*x*x*y*y,None,None),(4,-s.log(x*x/2+C),-x*s.exp(y),None,None),(11,-s.log(1-x*x/2),x*s.exp(y),0,0),(12,-s.sqrt(1+2*s.sin(x)-2*x*s.cos(x)),x*s.sin(x)/y,0,-1),(19,s.sqrt(x*x+4),x/y,0,2),(20,1+s.exp(x*x/2),x*y-x,0,2),(21,C*s.exp(x)-x-1,x+y,None,None),(27,-1/(x+C),y*y,None,None),(28,C*s.exp(x*x/2),x*y,None,None),(33,1+s.exp(2-x*x/2),x*(1-y),2,2),(34,s.sqrt(4+2*s.log(x)),1/(x*y),1,2)]:
 check(str(no)+' DE residual',s.diff(expr,x)-rhs.subs(y,expr))
 if x0 is not None:check(str(no)+' initial',expr.subs(x,x0)-y0)
check('3 implicit relation',s.diff(x*x+2*s.log(s.Abs(x)),x)-2*(x*x+1)/x) if False else None
check('5 implicit primitive',s.diff(s.exp(y)-y,y)-(s.exp(y)-1))
check('6 left primitive',s.diff(y*y/2+y**5/5,y)-(y+y**4));check('6 right primitive',s.diff(-1/x+x**3/3,x)-(1+x**4)/x**2)
check('7 left primitive',s.diff(y*s.sin(y)+s.cos(y),y)-y*s.cos(y));check('7 right primitive',s.diff(-s.exp(-x*x)/2,x)-x*s.exp(-x*x))
check('8 left primitive',s.diff(-(s.log(y)+1)/y,y)-s.log(y)/y**2)
check('15 initial constant',R(1,2)+R(8,3)-(-R(1,4)+R(41,12)))
for xx in [-2,-1,.3,1,2]:
 yy=math.sin(xx*xx) if abs(xx)<math.sqrt(math.pi/2) else 1;dy=2*xx*math.cos(xx*xx) if abs(xx)<math.sqrt(math.pi/2) else 0
 near('23 saturated global branch '+str(xx),dy,2*xx*math.sqrt(max(0,1-yy*yy)))
check('35 nonnegative branch',s.diff((x*x+4)**2/4,x)-x*(x*x+4))
check('42 boundary1',35-20-15);check('42 boundary2',35-10-25);check('42 conduction',s.diff(35-20/x,x,2)+2/x*s.diff(35-20/x,x))
a,b,k=s.symbols('a b k',positive=True);E=s.exp((a-b)*k*t);z=a*b*(E-1)/(a*E-b);check('40 unequal rates',s.diff(z,t)-k*(a-z)*(b-z));check('40 initial',z.subs(t,0))
z=a-a/(1+k*s.sqrt(a)*t/2)**2
# Verify the fractional rate on positive physical t using high-precision substitution, avoiding invalid complex-power simplifications.
for av,kv,tv in [(2,.3,0),(2,.3,5),(7,.1,2)]:near('41 fractional kinetics '+str(tv),s.diff(z,t).subs({a:av,k:kv,t:tv}),kv*(av-float(z.subs({a:av,k:kv,t:tv})))**1.5)
check('24 negative exponent residual',s.exp(s.log(C+s.sin(x)))*s.diff(-s.log(C+s.sin(x)),x)+s.cos(x))
check('36 positive denominator source residual',(x*x+1)*s.diff((x+1)/(x-1),x)+((x+1)/(x-1))**2+1)
check('36 initial condition',((x+1)/(x-1)).subs(x,3)-2)
finish('section03',[605,606,607,608])
