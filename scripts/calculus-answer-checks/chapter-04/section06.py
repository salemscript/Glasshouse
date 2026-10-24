from common import *
from curve import curve
import numpy as np
from scipy.optimize import brentq
R=s.Rational
def proots(e):
 p=s.Poly(s.cancel(e).as_numer_denom()[0],x)
 # square-free factorization retains multiplicities without fragile repeated-root iteration.
 rr=[]
 for f,m in s.factor_list(p.as_expr(),x)[1]:
  for z in s.nroots(f,maxsteps=1000):
   if abs(float(s.im(z)))<1e-10:rr.append(s.Float(float(s.re(z)),16))
 return sorted(rr,key=float)
def scans(e,lo,hi,exc=(),step=.002):
 fn=s.lambdify(x,e,'numpy');g=np.linspace(lo,hi,max(10001,int((hi-lo)/step)));rr=[]
 with np.errstate(all='ignore'):
  y=fn(g)
  if np.isscalar(y):return []
  for a,b,fa,fb in zip(g[:-1],g[1:],y[:-1],y[1:]):
   if any(a<=v<=b for v in exc):continue
   if np.isfinite(fa) and np.isfinite(fb) and fa*fb<0:
    r=brentq(fn,a,b,xtol=1e-13)
    if all(abs(r-z)>1e-7 for z in rr):rr.append(r)
 return [s.Float(v,16) for v in rr]
funcs={1:x**5-5*x**4-x**3-28*x*x-2*x,2:-2*x**6+5*x**5+140*x**3-110*x*x,3:x**6-5*x**5+25*x**3-6*x*x-48*x,4:(x**4-x**3-8)/(x*x-x-6),5:x/(x**3+x*x+1),13:(x+4)*(x-3)**2/(x**4*(x-1)),14:(2*x+3)**2*(x-2)**5/(x**3*(x-5)**2),15:x*x*(x+1)**3/((x-2)**2*(x-4)**4),16:(2*x+3)**2*(x-2)**5/(x**3*(x-5)**2),17:(x**3+5*x*x+1)/(x**4+x**3-x*x+2)}
for k,f in funcs.items():
 exc=proots(s.cancel(f).as_numer_denom()[1]); cr=proots(s.diff(f,x)); ip=proots(s.diff(f,x,2));curve(6,k,f,cr,ip,excluded=exc,asym='Vertical exclusions: '+(','.join(format(float(z),'.6g') for z in exc) or 'none')+'; inspect the actual end behavior, not a cropped screen')
 if k in(15,16,17):
  q=OUT[f'calculus-section-4-6-{k}'];q['grader']['parts'] += [expr('f′(x)',s.factor(s.diff(f,x))),expr('f″(x)',s.factor(s.diff(f,x,2)))];q['objectiveFieldCount']+=2
for k,f,lo,hi,exc,crbound in [(6,6*s.sin(x)-x*x,-5,3,[],(-5,3)),(7,6*s.sin(x)+s.cot(x),-s.pi,s.pi,[0],(-math.pi+.0001,math.pi-.0001)),(8,s.exp(x)-R(186,1000)*x**4,-s.oo,s.oo,[],(-50,50)),(19,s.sqrt(x)+5*s.sin(x),0,20,[],(.000001,20)),(20,x-s.atan(x*x),-s.oo,s.oo,[],(-30,30)),(21,(1-s.exp(1/x))/(1+s.exp(1/x)),-s.oo,s.oo,[0],(-20,20))]:
 if k==21:
  cr=[];ip=[s.Float(-.4167782798),s.Float(.4167782798)]
  # Solve the exact f″=0 in a stable variable u=1/(2x): u tanh u=1.
  import mpmath as mp
  u=mp.findroot(lambda u:u*mp.tanh(u)-1,1.2);ip=[s.Float(-1/(2*u),16),s.Float(1/(2*u),16)]
 else:cr=scans(s.diff(f,x),*crbound,exc);ip=scans(s.diff(f,x,2),*crbound,exc)
 curve(6,k,f,cr,ip,domain=(lo,hi),excluded=exc)
 if k==19:
  q=OUT[f'calculus-section-4-6-{k}'];q['grader']['parts'] += [expr('f′(x)',s.diff(f,x)),expr('f″(x)',s.diff(f,x,2))];q['objectiveFieldCount']+=2
curve(6,9,1+1/x+8/x**2+1/x**3,[-8-s.sqrt(61),-8+s.sqrt(61)],[-12-s.sqrt(138),-12+s.sqrt(138)],excluded=[0])
curve(6,10,x**-8-2*10**8*x**-4,[-R(1,100),R(1,100)],[-(R(9,5*10**8))**R(1,4),(R(9,5*10**8))**R(1,4)],excluded=[0])
curve(6,11,x*x*s.log(x),[s.exp(R(-1,2))],[s.exp(R(-3,2))],domain=(0,s.oo))
q=OUT['calculus-section-4-6-11'];q['grader']['parts'].append(n('(b) limit asx→0⁺',0));q['objectiveFieldCount']+=1
curve(6,12,x*s.exp(1/x),[1],[],excluded=[0]);q=OUT['calculus-section-4-6-12'];q['grader']['parts'] += [c('(b) limit asx→0⁻','0','−∞','+∞'),c('(b) limit asx→0⁺','+∞','0','−∞')];q['objectiveFieldCount']+=2
# x^(2/3) is the real cube root squared. Solve exact polynomial factors for derivative signs.
D=1+x+x**4;f=x**R(2,3)/D;pn=s.simplify(s.diff(f,x,2)*x**R(4,3)*D**3);cr=proots(2-x-10*x**4);ips=proots(pn)
realF=lambda t:abs(t)**(2/3)/(1+t+t**4)
vals=[float(z) for z in cr];ivals=[float(z) for z in ips]
row(6,18,c('Domain','All realx; cusp at0','x>0 only','Poles at±1'),c('Increasing intervals',f'(−∞,{vals[0]:.6f}) ∪ (0,{vals[1]:.6f})','(0,∞)','(−∞,0)'),c('Decreasing intervals',f'({vals[0]:.6f},0) ∪ ({vals[1]:.6f},∞)','(−∞,0)','None'),*[n('Local maximum x '+str(i+1),v,tol=1e-5) for i,v in enumerate(vals)],*[n('Local maximum value '+str(i+1),realF(v),tol=1e-5) for i,v in enumerate(vals)],n('Local minimum value at0',0),*[n('Inflection x '+str(i+1),v,tol=1e-5) for i,v in enumerate(ivals)],c('Concavity pattern','Up on (−∞,−0.966025), (−0.456158,−0.123462), (1.114875,∞); down on the intervening intervals, split at the cusp x=0','Up everywhere','Down everywhere'),c('Asymptote','Horizontaly=0 at±∞','Verticalx=0','None'),why='The denominator1+x+x⁴ stays positive. f′ has sign of x^(−1/3)(2−x−10x⁴); use real cube-root signs. f″ factors into the recorded polynomial over3-positive powers. The cusp at0 is continuous and is a local minimum.',limited=True)
row(6,22,c('Period and domain','Period2π; all realx','Periodπ with poles','No period'),c('Extrema','Minimum3/5 atπ/2+2kπ; maximum3 at3π/2+2kπ','Maximum3/5 andminimum3','No extrema'),c('Monotonicity','Decreasing wherecosx>0; increasing wherecosx<0','Increasing wherecosx>0','Always increasing'),c('Inflection condition','sinx=(3−√41)/4','sinx=(3+√41)/4','cosx=0'),c('Concavity','Up where sinx>(3−√41)/4; down where it is smaller','Up everywhere','Down everywhere'),why='f′=−6cosx/(3+2sinx)² andf″=6(4+3sinx−2sin²x)/(3+2sinx)³. Only one sine root lies in[−1,1].',limited=True)
row(6,23,c('Stable equivalent','(1/2)[sin(x⁴/2)/(x⁴/2)]² forx≠0','sin(x⁴)/x⁴','cos(x⁴)/x⁸'),n('Limit at0',.5),c('True graph features','Even, nonnegative, removable hole at(0,1/2), increasingly rapid oscillations decaying to0','A pole at0 with negative values','Constant1/2 everywhere'),c('Nonzero zeros','x=±(2kπ)^(1/4), k=1,2,…','x=kπ','No zeros'),why='Use1−cosu=2sin²(u/2) to avoid cancellation. The envelope is2/x⁸; a coarse display can hide the narrow lobes.',limited=True)
# f=e^x+ln|x−4|: derivative e^x+1/(x−4), curvature e^x−1/(x−4)².
r=brentq(lambda t:math.exp(t)*(4-t)-1,-5,0);r2=brentq(lambda t:math.exp(t)*(4-t)-1,3,3.999999)
ip1=brentq(lambda t:math.exp(t)*(t-4)**2-1,-10,0);ip2=brentq(lambda t:math.exp(t)*(t-4)**2-1,3,3.99999);ip3=brentq(lambda t:math.exp(t)*(t-4)**2-1,4.00001,5)
row(6,24,c('Domain and asymptote','x≠4; verticalx=4 withf→−∞ on both sides','All realx','Verticalx=0'),n('Local minimum x',r,tol=1e-5),n('Local maximum x',r2,tol=1e-5),*[n('Inflection x '+str(i+1),v,tol=1e-5) for i,v in enumerate([ip1,ip2,ip3])],c('End behavior','f→∞ at both−∞ and+∞','f→0 at both ends','f→−∞ at both ends'),why='Differentiate using dln|x−4|/dx=1/(x−4). Solve the bounded derivative/curvature equations on each side of the pole; separate windows are needed near4.',limited=True)
f=x**(1/x);dd=s.diff(f,x,2);rr=scans(dd,.001,100,step=.005)
row(6,25,n('(b) limit asx→0⁺',0),n('(b) limit asx→∞',1),c('(c) maximum','e^(1/e) atx=e','e atx=1','1 atx=1'),c('(c) minimum','None onx>0; infimum0 is not attained','0 atx=0','1 atx=1'),*[n('(d) inflection x '+str(i+1),z,tol=.001) for i,z in enumerate(rr)],why='lnf=lnx/x. Its derivative(1−lnx)/x² gives the unique maximum; the boundary limits follow from logarithms. Solve f″=0 numerically for the two inflections.',limited=True)
f=s.sin(x)**s.sin(x);rr=scans(s.diff(f,x,2),.0001,math.pi-.0001)
row(6,26,c('Real logarithmic-model domain','sinx>0; repeat on(2kπ,(2k+1)π)','All realx','sinx<0'),n('(b) limit asx→0⁺',1),c('(b) limit asx→∞','Does not exist: the real-domain pattern repeats','1','0'),c('(c) maxima/minima in(0,π)','Maximum1 atπ/2; minimae^(−1/e) atarcsin(1/e) andπ−arcsin(1/e)','Minimum1 atπ/2','No extrema'),*[n('(d) inflection x in(0,π), '+str(i+1),z,tol=.001) for i,z in enumerate(rr)],why='Setu=sinx>0 anduse ln f=u ln u. The conventional continuous real-power domain excludes negative sine values; positive-sine intervals repeat every2π.',limited=True)
f=s.sin(x+s.sin(3*x));cr=scans(s.diff(f,x),0,math.pi,step=.0001);ips=scans(s.diff(f,x,2),0,math.pi,step=.0001);curve(6,27,f,cr,ips,domain=(0,s.pi));q=OUT['calculus-section-4-6-27'];q['grader']['parts'].append(c('Symmetry on[−2π,2π]','Odd: f(−x)=−f(x)','Even: f(−x)=f(x)','Neither'));q['objectiveFieldCount']+=1
row(6,28,c('Extrema transition','c<0 gives max at−√(−c/3) andmin at+√(−c/3); c≥0 gives none','c>0 gives two extrema','Everyc gives two extrema'),c('Inflection','Always(0,0)','Only whenc=0','No inflections'),why='f′=3x²+c andf″=6x. Atc=0 the stationary origin is not an extremum.',limited=True)
row(6,29,c('Domain and asymptote','Forc≠0, verticalx=0; asymptotic parabolay=x²+6x; for c=0 the original expression retains a removable hole at x=0','Everyc has horizontaly=0','No asymptotic behavior'),c('Critical-number transition','0<c<8 gives3; c<0 orc>8 gives1; c=8 gives2 distinct; c=0 gives quadraticminimum at−3','Everyc gives2','Transition only atc=1'),c('Inflection','Forc≠0, x=∛(−c); forc=0 none','Alwaysx=0','Never'),why='f′=0 means2x³+6x²−c=0, excludingx=0 when it is a pole; the cubic turning values occur atx=−2,0 with levels8,0. f″=2+2c/x³.',limited=True)
row(6,30,c('Parameter dependence','Only|c| matters; domain[−|c|,|c|]','Changing sign ofc flips the curve','Domainℝ'),c('Extrema forc≠0','Minimum−c²/2 at−|c|/√2; maximumc²/2 at|c|/√2','Maximumc at0','No extrema'),c('Inflection','(0,0) forc≠0; c=0 degenerates to one point','No inflection fornonzeroc','x=±c'),why='Scale x=|c|u to obtainf=c²u√(1−u²); positive|c| stretches horizontally andquadratically vertically.',limited=True)
row(6,31,c('c>0','Unique minimum2√c atx=(lnc)/2; concave up everywhere','Unique maximum','No extrema'),c('c=0','e^x, increasing andconcave up','Constant','A parabola'),c('c<0','Increasing everywhere; one inflection atx=ln(−c)/2','Two extrema','Concave up everywhere'),why='f′=e^x−ce^(−x), f″=e^x+ce^(−x). Their zeros andsigns change atc=0.',limited=True)
row(6,32,c('c>0','Domainℝ; minimumlnc at0; inflectionsx=±√c','Verticalasymptote0','No extrema'),c('c=0','Domainx≠0; verticalasymptote0; concave down onboth branches','Domainℝ','Concave up everywhere'),c('c<0','Domain|x|>√(−c); verticalasymptotes±√(−c); concave down onboth branches','Domain|x|<√(−c)','One maximumat0'),why='f′=2x/(x²+c), f″=2(c−x²)/(x²+c)²; logarithm requiresx²+c>0.',limited=True)
row(6,33,c('c≠0 extrema','Maximum1/2 atx=1/c; minimum−1/2 atx=−1/c','Maximumc at0','No extrema'),c('Inflections','x=0 andx=±√3/|c|','Onlyx=0','None'),c('Scaling/transition','Increasing|c| compresses horizontally; sign reversal reflects vertically; c=0 is thezero function','Increasing|c| changes peak height','No change withc'),why='Writef(x)=u/(1+u²), u=cx. This gives exact horizontal scaling and reflection.',limited=True)
row(6,34,c('Poles when|c|<1','cosx=−c','sinx=−c','No poles'),c('For|c|>1','No poles; extrema wherecosx=−1/c','Alwaysincreasing','Alwaysdecreasing'),c('Critical transition parameters','c=−1 andc=1','c=0 only','c=±2'),c('Curvature equation','sinx(2−c²+c cosx)=0','cosx=0 only','sinx=c'),why='f′=(1+c cosx)/(c+cosx)² andf″=sinx(2−c²+c cosx)/(c+cosx)³. Atc=±1 cancellations retain excluded points andhalf-angle poles; atc=0 thefunction istanx.',limited=True)
row(6,35,c('Monotonicity transitions','c≥1:increasing; c≤−1:decreasing; |c|<1:alternating extrema','Onlyc=0 matters','Alwaysincreasing'),c('Inflection points','(kπ,ckπ), k∈ℤ, independent ofc inx','Onlywhenc=0','No inflections'),c('Extrema equation','cosx=−c, withsign changes onlywhen|c|<1','sinx=−c','x=−c'),why='f′=c+cosx; f″=−sinx. Equalityc=±1 gives isolated stationary points without reversals.',limited=True)
row(6,36,c('Common behavior fort≥0','Starts0, positive thereafter, one peak, returnstoward0','Alwaysrises','Startsnegative'),c('Peak time','ln(b/a)/(b−a)','ln(a/b)/(b−a)','1/b'),c('Asb increases witha,Cfixed','Peak occurs earlier andis higher; C(t) increases ateachfixedt>0','Peak occurslater andislower','Nothingchanges'),why='∂f/∂b=Ct e^(−bt)>0. The peak-time functionln(b/a)/(b−a) decreases forb>a because lnz>1−1/z forz>1.',limited=True)
row(6,37,c('c>0','Local/globalmaximum1/(ce) atx=1/c; limit0 at+∞ and−∞ at−∞','Localminimum at1/c','No extrema'),c('c<0','Local/globalminimum1/(ce) atx=1/c; limit0 at−∞ and+∞ at+∞','Maximum at1/c','No extrema'),c('c=0','Theliney=x','Thezero function','An exponential'),c('Inflection forc≠0','x=2/c, y=2/(ce²)','x=1/c','x=0'),why='f′=e^(−cx)(1−cx), f″=ce^(−cx)(cx−2). Parameter sign swaps the growth end andextremum type.',limited=True)
row(6,38,c('Inflection transition','c<0 givesx=±√(−c/6); c≥0 givesnone','c>0 givestwo','c=0 givesone'),c('Critical-number transition','c=−3/2: belowit3criticalnumbers; aboveit1; atequality2distinctcriticalnumbers','c=0 istheonlytransition','Everyc gives3'),why='f″=12x²+2c. The derivative4x³+2cx+1 hasarepeatedroot when it and12x²+2c vanish: x=1/2,c=−3/2.',limited=True)
row(6,39,c('(a) minima exist','Exactlywhenc>0, atx=±1/√c','Whenc<0','Forallc'),c('(a) origin','Alwaysalocalmaximumwithvalue1','Alwaysaminimum','Neverstationary'),c('(b) extremum locus','y=1−x²','y=1+x²','y=x²'),why='f′=4x(cx²−1); atnonzero stationary points,cx²=1 impliesf=1−x². Theorigin also liesontheparabola.',limited=True)
row(6,40,c('(a) maximum andminimum exist','|c|>√12','|c|<√12','Everyc'),c('(a) stationary x-values','(−c±√(c²−12))/6','(−c±√(c²+12))/6','±√c'),c('(b) extremum locus','y=x−x³','y=x+x³','y=x³'),why='f′=6x²+2cx+2; twodistinctrealroots requirec²>12. Solvec=−3x−1/x andsubstituteintof; equalitygivesastationaryinflection,notextrema.',limited=True)
finish('section06')
