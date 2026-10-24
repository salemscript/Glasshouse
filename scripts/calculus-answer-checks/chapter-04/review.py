#!/usr/bin/env python3
"""118 Chapter4 review contracts, visually reviewed printed358–362."""
import json,hashlib,random,gzip
from pathlib import Path
import sympy as S
import mpmath as mp
mp.mp.dps=40
ROOT=Path(__file__).resolve().parents[3]
QS=[q for q in json.load(gzip.open(ROOT/'site/questions/calculus.json.gz')) if q['sourceSet']=='chapter-04-review']
ROWS={};CHECKS=[]
x,t,u,T=S.symbols('x t u T',real=True);pi=S.pi

def fmt(e):return S.sstr(e).replace('**','^').replace('log','ln').replace('asin','arcsin').replace('atan','arctan')
def N(v,label='Answer',tol=1e-8,unit=''):return dict(type='numeric',answer=float(v),label=label,tolerance=tol,unit=unit)
def C(ans,*wrong,label='Answer'):return dict(type='choice',answer=ans,options=[ans,*wrong],label=label)
def F(e,label='Result',const=False):
 suffix=' + C' if const else '';e=S.simplify(e)
 if e==0:return C('0'+suffix,'1'+suffix,'−1'+suffix,label=label)
 return C(fmt(e)+suffix,fmt(-e)+suffix,fmt(2*e)+suffix,label=label)
def add(num,*fs,group='Exercises',why='',limited=False):
 q=[q for q in QS if q['subsection']==group and q['number']==str(num)];assert len(q)==1;(q,)=q
 assert q['id'] not in ROWS
 for i,f in enumerate(fs):
  f.update(explanation=why,provenance='original-source-reviewed-derivation')
  if f['type']=='choice':
   assert len(set(f['options']))==len(f['options']);random.Random(q['id']+str(i)).shuffle(f['options'])
 g=dict(fs[0]) if len(fs)==1 else dict(type='parts',parts=list(fs))
 g['scope']='Checks the labeled results and conclusions; original proofs, drawings, and explanations are not automatically assessed.'
 if limited:g['complete']=False
 ROWS[q['id']]=dict(grader=g,responsePartPrompt='Answer each labeled check using the original textbook question above.',objectiveChecksVerified=True,objectiveCheckVersion=3,objectiveFieldCount=len(fs),answerCheckSource=dict(book='Stewart, Calculus: Early Transcendentals, 8e',chapter=4,pdfPages=sorted({p['page'] for p in q['parts']}),authoringFile='scripts/calculus-answer-checks/chapter-04/review.py'))
def cc(n,*fs):add(n,*fs,group='Concept Check',limited=True)
cc(1,C('Absolute maximum compares every domain value; local maximum compares a neighborhood','Absolute and local maxima always coincide','A local maximum must have derivative zero',label='Definitions'))
cc(2,C('A continuous function on a closed bounded interval attains both absolute extremes','Continuity on an open interval always guarantees extremes','Differentiability is necessary',label='a · Extreme Value Theorem'),C('Compare values at endpoints and all interior critical numbers','Check only stationary points','Check only endpoints',label='b · Closed Interval Method'))
cc(3,C('At an interior local extremum, if f′(c) exists then f′(c)=0','Every stationary point is a local extremum','Endpoints always have zero derivative',label='a · Fermat'),C('A domain number c where f′(c)=0 or f′(c) does not exist','Any number outside the domain','Only a zero of f',label='b · Critical number'))
cc(4,C('Continuous on[a,b], differentiable on(a,b), f(a)=f(b) imply some f′(c)=0','Only equal endpoint values are needed','The conclusion holds at every c',label='a · Rolle'),C('Continuous on[a,b] and differentiable on(a,b) imply f′(c)=(f(b)−f(a))/(b−a): a tangent parallel to the secant','f′(c)=f(b)−f(a) without dividing by width','Continuity alone suffices',label='b · Mean Value Theorem'))
cc(5,C('f′>0 implies increasing; f′<0 implies decreasing on the interval','f>0 implies increasing','f″>0 implies decreasing',label='a · Monotonicity'),C('Graph lies above tangent lines; tangent slopes increase','Function values must be positive','Slopes must be positive',label='b · Concave upward'),C('f″>0 gives concave up; f″<0 gives concave down','f′>0 gives concave up','f″=0 always gives an inflection',label='c · Concavity test'),C('A continuous point where concavity changes; test candidates where f″=0 or is undefined','Every stationary point','Every zero of f″ without a sign test',label='d · Inflection'))
cc(6,C('f′ changes + to −: local maximum; − to +: local minimum','The signs of f determine extrema','No sign change implies maximum',label='a · First derivative test'),C('If f′(c)=0, f″(c)>0 gives minimum and f″(c)<0 maximum; zero is inconclusive','f″(c)=0 proves no extremum','f″<0 gives a minimum',label='b · Second derivative test'),C('Second derivative test is quick when nonzero; first derivative sign changes also handle inconclusive/undefined second derivatives','Second derivative test always decides','First derivative test requires f″ to exist',label='c · Comparison'))
cc(7,C('For 0/0 or ∞/∞ and the differentiability/nonzero denominator derivative hypotheses, a derivative-ratio limit determines the original limit when the theorem applies','Differentiate any quotient regardless of its form','Differentiate the quotient as one function',label='a · l’Hospital'),C('Rewrite fg as f/(1/g) or g/(1/f), then verify quotient hypotheses','Replace the product by f′g′','Every 0·∞ limit is zero',label='b · Product'),C('Combine terms or rationalize to obtain a qualifying quotient','Subtract derivative limits automatically','Every ∞−∞ limit is zero',label='c · Difference'),C('For positive base set y=f^g, find lim g ln f, then exponentiate','Take lim f times lim g','Every 0^0 limit is1',label='d · Power'))
forms=['Indeterminate','Indeterminate','0','No unique two-sided sign; magnitude diverges','+∞','Indeterminate','+∞','Indeterminate','Indeterminate','0','Indeterminate','Indeterminate']
for i,v in enumerate(forms):pass
cc(8,*[C(v,*[w for w in ['Indeterminate','0','+∞','No unique two-sided sign; magnitude diverges'] if w!=v],label=chr(97+i)+' · Limit form') for i,v in enumerate(forms)])
cc(9,C('Calculus identifies exact extrema, concavity, asymptotes, and behavior a finite viewing window can hide','A plotted window proves all global behavior','Calculus only changes plot colors',label='Why calculus remains useful'))
cc(10,C('The tangent at(x₁,f(x₁)) meets the x-axis at x₂','Use the horizontal line through f(x₁)','Double x₁',label='a · Geometry'),C('x₂=x₁−f(x₁)/f′(x₁)','x₂=x₁+f(x₁)/f′(x₁)','x₂=f′(x₁)',label='b · Second iterate'),C('xₙ₊₁=xₙ−f(xₙ)/f′(xₙ)','xₙ₊₁=f(xₙ)','xₙ₊₁=xₙ+1',label='c · Recurrence'),C('Zero/near-zero slopes, poor initial guesses, cycles/divergence, or multiple roots can prevent or slow convergence','It converges from every starting point','Only negative roots cause failure',label='d · Limitations'))
cc(11,C('F′=f on the interval','F=f′','F=f²',label='a · Antiderivative'),C('F₁−F₂ is constant on the interval','F₁=F₂ necessarily','F₁/F₂ is constant necessarily',label='b · Relation'))
truth=[False,False,False,True,True,False,False,False,True,False,True,False,False,True,True,False,True,False,True,False,False]
reasons=['x³ at0.','|x| at0 has no derivative.','f(x)=x on(0,1).','Rolle’s theorem.','Derivative sign test.','(x−2)⁴ at2 has f″(2)=0 but no concavity change.','They may differ by a constant.','MVT would give slope1, contradicting f′>1 everywhere.','e^(−x) is positive, decreasing and concave up.','A negative decreasing convex function on all R is impossible: a negative tangent slope at one point forces the graph above zero sufficiently far left via monotonic slopes/integration.','Sums preserve strict order.','f=g=x gives constant difference.','f=g=x on(−2,−1): product decreases.','Positivity and monotonicity give product order.','Reciprocal reverses positive order.','Derivative of an even function is odd.','Differentiate f(x+T)=f(x).','Domain excludes0; independent constants on the two components are allowed, so a single C is not most general globally.','Otherwise Rolle gives a zero derivative.','(1+1/x)^x tends to e.','Limit is0, not1.']
for i,(v,w) in enumerate(zip(truth,reasons),1):add(i,C(str(v),'False' if v else 'True',label='Truth value'),group='True-False Quiz',why=w,limited=True)
# Interior local extrema; endpoints are checked separately as absolute candidates.
funcs={1:(x**3-9*x*x+24*x-2,0,5,[2,4]),2:(x*S.sqrt(1-x),-1,1,[S.Rational(2,3)]),3:((3*x-4)/(x*x+1),-2,2,[-S.Rational(1,3)]),4:(S.sqrt(x*x+x+1),-2,1,[-S.Rational(1,2)]),5:(x+2*S.cos(x),-pi,pi,[pi/6,5*pi/6]),6:(x*x*S.exp(-x),-1,3,[0,2])}
for num,(f,lo,hi,cr) in funcs.items():
 candidates=[lo,hi,*cr];vs=[f.subs(x,z) for z in candidates];imin=min(range(len(vs)),key=lambda j:float(vs[j]));imax=max(range(len(vs)),key=lambda j:float(vs[j]));fields=[F(vs[imin],'Absolute minimum value'),F(vs[imax],'Absolute maximum value')]
 for z in cr:fields.append(F(f.subs(x,z),('Interior local minimum' if float(S.diff(f,x,2).subs(x,z))>0 else 'Interior local maximum')+' value at x='+fmt(z)))
 add(num,*fields,why='Compare endpoint and interior critical values. Local-extremum labels here mean interior local extrema.');CHECKS.append(dict(kind='extrema',number=num,function=str(f),bounds=[str(lo),str(hi)],critical=list(map(str,cr))))
for n,v in {7:1,8:S.Rational(4,3),9:4,11:0,12:-1,13:S.Rational(1,2),14:1}.items():add(n,N(v),why='Evaluate the stated one-sided/two-sided limit, transforming indeterminate forms before using l’Hospital’s rule.')
add(10,C('+∞','0','4',label='Limit'))
add(15,C('Local minima x=−2; local maxima x=1,9; vertical asymptote x=6; right horizontal asymptote y=0','Local minima x=1,9; maximum x=−2','x=6 is a point of the graph',label='Extrema and asymptotes'),C('Inflection x=0 and12; no inflection at excluded x=6','Inflection x=6 only','Every critical number is an inflection',label='Concavity changes'),limited=True)
add(16,C('Even extension of x² for0≤x≤1, 2−x for1≤x≤3, x−4 forx≥3','Even extension of −x² on[0,1]','f(x)=x² everywhere',label='Compatible function'),limited=True)
add(17,C('Local maximum x=−2, minimum x=2; horizontal asymptotes y=2 left and y=−2 right','Local maximum x=2, minimum x=−2','Both asymptotes are y=−2',label='Extrema and limits'),C('Inflections at x=−3,0,3 under the stated smoothness; use odd symmetry','Only x=2 is an inflection','No concavity changes',label='Concavity'),limited=True)
add(18,C('Increasing on(−2,0) and(4,∞); decreasing on(−∞,−2) and(0,4)','Increasing wherever the derivative graph rises','Increasing on(0,4)',label='a · Monotonicity'),C('Maximum x=0; minima x=−2,4; x=2 is stationary without extremum','Maximum x=2; minima x=0,4','All four zeros are maxima',label='b · Extrema'),C('f″ has the sign of the slopes of the displayed f′ curve; zeros near−1,1,2,3,5','f″ equals the plotted graph','f″ is positive everywhere',label='c · Second derivative sketch'),C('f is determined up to a vertical shift; stationary tangent at2 does not reverse monotonicity','f must pass through the origin','f equals f′',label='d · Original sketch'),limited=True)
# Analytic curve features: symbolic derivatives, independently enumerated breakpoints.
import curve as CV
CV.x=x
def curve_row(sec,k,*fields,why,limited):
 add(k,*fields,why=why,limited=limited);CV.AUDIT[f'calculus-section-4-review-{k}']={}
CV.row=curve_row

def graph(k,f,cr,ips,bounds=(-S.oo,S.oo),ex=(),asym=None):
 CV.curve('review',k,f,cr,ips,domain=bounds,excluded=ex,asym=asym)
 CHECKS.append(dict(kind='curve',number=k,function=str(f),critical=list(map(str,cr)),inflections=list(map(str,ips))))
def realroots(e):
 p=S.Poly(S.fraction(S.cancel(e))[0],x)
 return sorted([S.Float(S.re(z),16) for z in S.nroots(p,maxsteps=500) if abs(float(S.im(z)))<1e-10],key=float)
def scan(e,intervals):
 from scipy.optimize import brentq
 import numpy as np
 fn=S.lambdify(x,e,'numpy');out=[]
 for lo,hi in intervals:
  pts=np.linspace(lo,hi,20001)
  for a,b in zip(pts[:-1],pts[1:]):
   aa=float(fn(a));bb=float(fn(b))
   if aa*bb<0:
    z=brentq(fn,a,b,xtol=1e-14)
    if not out or abs(z-out[-1])>1e-7:out.append(S.Float(z,16))
 return out
for k,f in {19:2-2*x-x**3,20:-2*x**3-3*x*x+12*x+5,21:3*x**4-4*x**3+2,22:x/(1-x*x),23:1/(x*(x-3)**2),24:1/x**2-1/(x-2)**2,25:(x-1)**3/x**2,32:S.exp(2*x-x*x),33:(x-2)*S.exp(-x),34:x+S.log(x*x+1),35:(x*x-1)/x**3,36:(x**3+1)/(x**6+1),37:3*x**6-5*x**5+x**4-5*x**3-2*x*x+2}.items():
 d=S.factor(S.diff(f,x));dd=S.factor(S.diff(f,x,2));ex={22:[-1,1],23:[0,3],24:[0,2],25:[0],35:[0]}.get(k,[])
 if k in (32,33):cr={32:[1],33:[3]}[k];ips={32:[1-1/S.sqrt(2),1+1/S.sqrt(2)],33:[4]}[k]
 else:
  cr=[v for v in realroots(d) if all(abs(float(v)-a)>1e-7 for a in ex)];ips=[v for v in realroots(dd) if all(abs(float(v)-a)>1e-7 for a in ex)]
 asym={22:'Vertical x=−1,1; horizontal y=0',23:'Vertical x=0,3; horizontal y=0',24:'Vertical x=0,2; horizontal y=0',25:'Vertical x=0; slant y=x−3',32:'Horizontal y=0 at both infinities',33:'Horizontal y=0 as x→+∞',35:'Vertical x=0; horizontal y=0',36:'Horizontal y=0 at both infinities'}.get(k)
 graph(k,f,cr,ips,ex=ex,asym=asym)
graph(26,S.sqrt(1-x)+S.sqrt(1+x),[0],[],bounds=(-1,1))
graph(27,x*S.sqrt(2+x),[-S.Rational(4,3)],[],bounds=(-2,S.oo))
add(28,C('Domain R; zeros0,3; local minima(0,0),(3,0); maximum at x=3/4','Only x≥0 is allowed','Maximum at x=0',label='Domain and extrema'),C('Increasing on(0,3/4),(3,∞); decreasing on(−∞,0),(3/4,3)','Increasing everywhere','Decreasing everywhere',label='Monotonicity'),C('Inflections at x=(15−9sqrt(5))/20 and(15+9sqrt(5))/20; concave down between, up outside','Inflection only at0','Concave up everywhere',label='Concavity'),limited=True,why='Use the real cube root: x^(2/3)=|x|^(2/3). x=0 is a cusp, but concavity is down on both sides there.')
graph(29,S.exp(x)*S.sin(x),[-pi/4,3*pi/4],[-pi/2,pi/2],bounds=(-pi,pi))
graph(30,4*x-S.tan(x),[-pi/3,pi/3],[0],bounds=(-pi/2,pi/2),asym='Vertical x=−π/2,π/2')
add(31,C('Domain(−∞,−1]∪[1,∞); odd; decreasing on both branches; horizontal asymptote y=0','Domain all nonzero reals','Increasing on both branches',label='Domain and monotonicity'),C('Concave down on(−∞,−1), up on(1,∞); no inflection because the gap is outside the domain','Inflection at0','Concave up on both branches',label='Concavity'),C('Endpoints(−1,−π/2),(1,π/2), with vertical one-sided tangents','Vertical asymptotes x=±1','Endpoints(±1,0)',label='Endpoints'),limited=True)
f=x*x+S.Rational(13,2)*S.sin(x)
graph(38,f,scan(S.diff(f,x),[(-5,5)]),scan(S.diff(f,x,2),[(-5,5)]),bounds=(-5,5))
f=S.exp(-1/x**2);graph(39,f,[],[-S.sqrt(S.Rational(2,3)),S.sqrt(S.Rational(2,3))],ex=[0],asym='Horizontal y=1 at both infinities; removable hole(0,0)')
f=1/(1+S.exp(1/x));ip=scan(S.diff(f,x,2),[(-3,-.05),(.05,3)])
graph(40,f,[],ip,ex=[0],asym='Limits at +∞,−∞ are1/2; at0+ is0; at0− is1; jump at0')
for k,f,intervals,bounds,ex,asym in [(41,S.cos(x)**2/S.sqrt(x*x+x+1),[(-float(pi),float(pi))],(-pi,pi),[],None),(42,S.exp(-x/10)*S.log(x*x-1),[(-100,-1.0001),(1.0001,100)],(-S.oo,S.oo),[-1,1],'Domain x<−1 orx>1; vertical x=−1,1; y=0 asx→+∞')]:
 cr=scan(S.diff(f,x),intervals);ips=scan(S.diff(f,x,2),intervals)
 if k==41:graph(k,f,cr,ips,bounds=bounds)
 else:
  add(k,*[N(z,('Local maximum x' if float(S.diff(f,x,2).subs(x,z))<0 else 'Local minimum x')+f' #{j+1}',tol=.0001) for j,z in enumerate(cr)],*[N(z,f'Inflection x #{j+1}',tol=.0001) for j,z in enumerate(ips)],C(asym,'Domain all real x','Domain only(−1,1)',label='Domain and asymptotes'),limited=True)
  CHECKS.append(dict(kind='curve',number=k,function=str(f),critical=list(map(str,cr)),inflections=list(map(str,ips))))
add(43,C('Continuous on R exactly when C>1; no real graph when C≤−1','Continuous on R when C≥1','No graph when C<0',label='Domain by parameter'),C('Where defined, periodic with period2π; maxima atπ/2+2kπ; minima at3π/2+2kπ only ifC>1','Period depends onC','All members have the same range',label='Shared and differing features'),C('AsC→∞, values rise like lnC and oscillation amplitude tends to0','Functions tend to0','Amplitude grows without bound',label='Large C'),limited=True)
add(44,C('For c>0: extrema x=±1/sqrt(2c), values±sqrt(c/2)*e^(−1/2); positive x is maximum','Extrema x=±sqrt(c)','Every c has two extrema',label='Positive c extrema'),C('For c>0 inflections x=0,±sqrt(3/(2c)); c<0 only x=0 and no extrema; c=0 gives zero function','For c<0 there are two extrema','No member has an inflection',label='Inflections and other c'),C('As positive c grows, extrema and outer inflections approach the y-axis and their nonzero heights grow in magnitude','Their x-coordinates move outward','All coordinates remain fixed',label='Parameter behavior'),limited=True)
add(45,C('Derivative3−2sinx≥1; opposite signs at−3 and0 give one root by IVT and strict monotonicity','Derivative is sometimes negative','Rolle alone proves existence',label='Uniqueness proof'),limited=True)
add(46,N(9,'Lower bound'),N(21,'Upper bound'),limited=True,why='MVT gives f(4)=1+4f′(c).')
add(47,N(2,'Lower bound'),N(2.0125,'Upper bound'),limited=True,why='MVT derivative1/(5x^(4/5)) lies strictly between0 and1/80 for32<x<33.')
add(48,N(-S.Rational(3,2),'a'),N(S.Rational(9,2),'b'))
add(49,C('Unique minimum atx=0','Maximum atx=0','Extrema atx=±1',label='a · Extreme value'),C('Concave upward on R (g″>0 forx≠0); no inflection at0','Concave down forx<0','Concavity changes at0',label='b · Concavity'),why='g′=2xf′(x²); g″=2f′(x²)+4x²f″(x²). Continuity of f′ gives f′(0)≥0.')
add(50,N(500,'First integer'),N(125,'Second integer'))
add(51,C('|Ax₁+By₁+C|/sqrt(A²+B²), for(A,B)≠(0,0)','|Ax₁+By₁+C|/(A²+B²)','sqrt(A²+B²)',label='Distance'),limited=True)
add(52,N(4,'x'),N(2,'y'),why='Minimize(x−3)²+64/x². The positive-branch stationary equation has root4; all negative-branch distances exceed3 while this candidate has distance sqrt5.')
add(53,C('3sqrt(3)r², attained by an equilateral triangle','πr²','4r²',label='Minimum area'),why='For apex-to-center height, minimize base times height/2 subject to inradiusr; symmetry optimum is equilateral.')
add(54,C('32πr³/81','4πr³/3','16πr³/81',label='Maximum cone volume'),C('Height4r/3 and base radius2sqrt(2)r/3','Height r and radius r','Height2r and radius0',label='Dimensions'))
add(55,N(4/S.sqrt(3),'Distance DP',unit='cm'))
add(56,N(2,'Distance DP',unit='cm'),C('P=C','P=D','P is the midpoint ofCD',label='Location'))
add(57,C('L=C','L=K','L=C²',label='Minimizing wavelength'))
add(58,C('r=(3V/(5π))^(1/3); cylinder height h=r; total height2r','Cylinder height2r','Cylinder height0',label='Least-metal dimensions'),why='Include the flat bottom: A=3πr²+2πrh and V=πr²h+2πr³/3. Eliminating h gives A=5πr²/3+2V/r.')
add(59,N(11.5,'Ticket price',unit='$'))
profit= S.Rational(232,10)*x+S.Rational(17,100)*x*x-S.Rational(1,1000)*x**3-1800
cost=1800+25*x-x*x/5+x**3/1000
avgroot=mp.findroot(lambda z:-1800/z**2-.2+.002*z,145)
add(60,N((S.Rational(34,100)+S.sqrt(S.Rational(394,1000)))/S.Rational(6,1000),'a · Graph estimate maximizing profit',tol=1),N((S.Rational(34,100)+S.sqrt(S.Rational(394,1000)))/S.Rational(6,1000),'b · Calculus maximizing output'),N(avgroot,'c · Minimum-average-cost output',tol=.1),limited=True,why='Profit derivative=23.2+0.34x−0.003x²; average cost derivative=−1800/x²−0.2+0.002x. Continuous output model; nearest feasible integer for integral production.')
root=mp.findroot(lambda z:z**5-z**4+3*z*z-3*z-2,1.5)
add(61,N(root,'Root',tol=.00000051))
roots=[mp.findroot(lambda z:mp.sin(z)-z*z+3*z-1,g) for g in [.2,3]]
add(62,*[N(z,f'Root #{j+1}',tol=.00000051) for j,z in enumerate(roots)],why='h(x)=sinx−x²+3x−1 has h″=−sinx−2<0; strict concavity and tails−∞ prove these two are all roots.')
tmax=mp.findroot(lambda z:-mp.sin(z)+1-2*z,.3)
add(63,N(mp.cos(tmax)+tmax-tmax*tmax,'Absolute maximum value',tol=5.1e-9))
f=x*S.sin(x);graph(64,f,scan(S.diff(f,x),[(.001,2*float(pi))]),scan(S.diff(f,x,2),[(.001,2*float(pi))]),bounds=(0,2*pi))
primitives={65:(4*S.sqrt(x)-6*x*x+3,8*x**S.Rational(3,2)/3-2*x**3+3*x),66:(1/x+1/(x*x+1),S.log(S.Abs(x))+S.atan(x)),67:(2*S.sin(x)-3*S.exp(x),-2*S.cos(x)-3*S.exp(x)),68:(x**-3+S.cosh(x),-1/(2*x*x)+S.sinh(x))}
for num,(e,p) in primitives.items():
 add(num,F(p,'Antiderivative (replace x by t in #67)',const=True),why='Constants may differ on disconnected intervals of the original domain.');CHECKS.append(dict(kind='primitive',number=num,integrand=str(e),primitive=str(p)))
for num,p in {69:x*x+3*S.cos(x)+2,70:x*x/2+2*S.sqrt(x)+S.Rational(1,2),71:x*x/2-x**3+4*x**4+2*x+1,72:x**5/4+x**4/2+x*x-S.Rational(27,4)*x+3,73:x*x-S.atan(x)+1,74:-S.sin(x)-3*S.cos(x)+3*x+3,75:S.exp(x)/10-S.cos(x)+S.Rational(9,10)}.items():
 add(num,F(p,'f / position / antiderivative in the original variable'),limited=num==75,why='Integrate the given derivative and apply each stated initial/boundary condition. The displayed variable x stands for the question’s independent variable.');CHECKS.append(dict(kind='initial-value',number=num,formula=str(p)))
add(76,C('Critical-number transitions at c=9/32 and c=0; c=0 merges a nonzero critical point with0','Only c=9/32 matters for distinct critical numbers','Transition atc=1',label='Critical numbers'),C('Inflection transition c=3/8: two ifc<3/8, none ifc≥3/8','Inflection transition c=0','Always two inflections',label='Inflection points'),limited=True)
add(77,N(S.sqrt(9800),'Impact speed',unit='m/s',tol=.05),C('No: speed≈99m/s<100m/s under free fall from rest with g=9.8m/s²','Yes: speed exceeds100m/s','Cannot estimate using height',label='Conclusion'))
add(78,C('Let d=sA−sB be twice differentiable. Two passages in the same overtaking direction force an intervening reverse crossing; Rolle twice yields d″=0','Two arbitrary meetings alone always guarantee equal accelerations','Equality of positions implies equality of accelerations at that instant',label='Proof and needed interpretation'),limited=True,why='Assume continuous velocities and differentiable velocities, and that “A passed B twice” means two crossings in the same direction; merely two meetings is insufficient (d=t(t−1) is a counterexample).')
z=(5*S.sqrt(2)+5*S.sqrt(34))/4;depth=z-5*S.sqrt(2);width=2*S.sqrt(100-z*z)
add(79,F(10*S.sqrt(2),'a · Square side'),F(width,'b · Plank width'),F(depth,'b · Plank depth'),F(20/S.sqrt(3),'c · Beam width'),F(20*S.sqrt(S.Rational(2,3)),'c · Beam depth'),limited=True,why='For each cap maximize2sqrt(100−z²)(z−5sqrt2). Strength is proportional to width*depth² with width²+depth²=400.')
add(80,C('R=2v²cosθ sin(θ−α)/(g cos²α)','R=v²sinθ/g','R=2v²sinθ/g',label='a · Uphill range'),C('θ=π/4+α/2','θ=π/4−α/2','θ=α',label='b · Uphill optimum'),C('R=2v²cosθ sin(θ+α)/(g cos²α); θ=π/4−α/2','Downhill optimum θ=π/4+α/2','Range is unchanged by slope',label='c · Downhill'),limited=True)
add(81,N(0,'Limit'),limited=True,why='cothE−1/E=E/3+O(E³).')
add(82,C('g/(2t), for fixed t>0','g t²/2','0',label='Limit of the literal printed formula'),C('g t²/2 would result from the physically standard argument t*sqrt(gc/m)','g/(2t) has units of distance','Both printed and corrected arguments are identical',label='Printed-formula caveat'),why='The supplied image places mt beneath the radical: s=(m/c)ln cosh(sqrt(gc/(mt))). Using ln cosh z~z²/2 gives g/(2t). This appears dimensionally inconsistent with distance; the alternative physical formula is explicitly distinguished rather than silently substituted.')
add(83,C('Apply MVT to arctan on[0,x]: arctanx=x/(1+c²), 0<c<x','arctanx=x for every positive x','The derivative of arctan is increasing on positive x',label='Strict bounds proof'),limited=True)
add(84,C('One example f(x)=−x+exp(−x²/2); strictly decreasing, inflections at±1, asymptote y=−x','f(x)=x','f(x)=−x³',label='Compatible graph example'),limited=True,why='f′=−1−x exp(−x²/2)≤−1+exp(−1/2)<0. f″=(x²−1)exp(−x²/2) gives the stated concavity.')
add(85,F(20*S.sqrt(2),'a · Optimal pole height in ft'),C('480k(h−4)/[1600+(h−4)²]^(5/2), for h>4, with I=k cosθ/d²','160k/[1600+(h−4)²]','0',label='b · Positive rate of intensity decrease'),why='At radiusx, I=k(h−4)/[x²+(h−4)²]^(3/2); differentiate with dx/dt=4 and x=40.')
add(86,C('V′ is constant positive inflow; H′ is positive height rise','V′ is negative','H′ is zero',label='a · First derivatives'),N(0,'b · V″'),C('H″(t₁)<0, H″(t₂)=0, H″(t₃)>0','All three are positive','Signs are +,0,−',label='c · Height acceleration'),why='H′=Q/[πH(2r−H)]; the cross-sectional area grows until half full, then shrinks.')
assert len(ROWS)==118,(len(ROWS),[(q['subsection'],q['number']) for q in QS if q['id'] not in ROWS])
HERE=Path(__file__).parent
(HERE/'review.json').write_text(json.dumps(ROWS,ensure_ascii=False,indent=2)+'\n')
(HERE/'review-audit.json').write_text(json.dumps(dict(total=len(ROWS),fields=sum(v['objectiveFieldCount'] for v in ROWS.values()),sourceSHA256=hashlib.sha256((ROOT/'site/books/calculus/chapter-04.pdf').read_bytes()).hexdigest(),reviewedPrintedPages=list(range(358,363)),independentCases=CHECKS),ensure_ascii=False,indent=2)+'\n')
print('Chapter4 review',len(ROWS))
