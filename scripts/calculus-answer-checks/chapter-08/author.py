#!/usr/bin/env python3
"""Source-inspected original Chapter 8 mathematical answer contracts."""
import gzip,json,hashlib,random,math
from pathlib import Path
import sympy as S
import mpmath as mp
mp.mp.dps=40
ROOT=Path(__file__).resolve().parents[3]
QS=[q for q in json.load(gzip.open(ROOT/'site/questions/calculus.json.gz')) if q['chapter']==8]
ROWS={}; DERIVATIONS=[]
x,y,t,a,b,r,h,k=S.symbols('x y t a b r h k',positive=True)
pi=S.pi

def fmt(e):return S.sstr(e).replace('**','^').replace('log','ln').replace('asinh','arcsinh').replace('asin','arcsin').replace('atan','arctan')
def N(v,label='Answer',unit='',tol=1e-7):return dict(type='numeric',answer=float(v),label=label,unit=unit,tolerance=tol,relativeTolerance=1e-8)
def C(ans,*wrong,label='Answer',why=''):
 assert len(wrong)>0 and ans not in wrong and len(set(wrong))==len(wrong),(ans,wrong)
 return dict(type='choice',answer=ans,options=[ans,*wrong],label=label,explanation=why)
def F(e,label='Exact result',suffix=''):
 e=S.simplify(e);return C(fmt(e)+suffix,fmt(e+1)+suffix,fmt(e*2)+suffix,label=label)
def I(integrand,var,lo,hi,label='Integral'):
 s=f'∫[{fmt(lo)}, {fmt(hi)}] {fmt(integrand)} d{var}'
 return C(s,f'∫[{fmt(lo)}, {fmt(hi)}] {fmt(integrand**2)} d{var}',f'∫[{fmt(lo)}, {fmt(hi)}] {fmt(integrand/2)} d{var}',label=label)
def add(sec,num,*fs,group='Exercises',limited=False,why=''):
 sourceSet=f'section-8-{sec}' if isinstance(sec,int) else f'chapter-08-{sec}'
 matches=[q for q in QS if q['sourceSet']==sourceSet and q['number']==str(num) and q['subsection']==group]
 assert len(matches)==1,(sec,num,group)
 q=matches[0];assert q['id'] not in ROWS
 assert len({f['label'] for f in fs})==len(fs),(sec,num)
 for i,f in enumerate(fs):
  f['provenance']='explicit-source-inspected-original-derivation';f['explanation']=f.get('explanation') or why
  if f['type']=='choice':
   random.Random(q['id']+str(i)).shuffle(f['options']);f['selectionPrompt']='Select the result for '+f['label']+'.'
 scope='Checks the labeled numerical results and mathematical selections. Written proofs, freehand graphs, and open-ended constructions are not automatically assessed.'
 grader={**fs[0],'scope':scope} if len(fs)==1 else dict(type='parts',parts=list(fs),scope=scope)
 if limited:grader['complete']=False
 ROWS[q['id']]=dict(grader=grader,responsePartPrompt='Answer each labeled check for the original textbook question above.',objectiveChecksVerified=True,objectiveCheckVersion=2,objectiveFieldCount=len(fs),answerCheckSource=dict(book='Stewart, Calculus: Early Transcendentals, 8th edition',chapter=8,sourceSet=sourceSet,exercise=q['number'],pdfPages=sorted({p['page'] for p in q['parts']}),authoringFile='scripts/calculus-answer-checks/chapter-08/author.py',review='Original derivation from supplied source, with independently checked numerical calculations.'))
def quad(f,var,lo,hi):
 fn=S.lambdify(var,f,'mpmath');return mp.quad(fn,[mp.mpf(str(S.N(lo,40))),(mp.mpf(str(S.N(lo,40)))+mp.mpf(str(S.N(hi,40))))/2,mp.mpf(str(S.N(hi,40)))])
def simpson(f,var,lo,hi,n=10):
 fn=S.lambdify(var,f,'mpmath');lo=mp.mpf(str(S.N(lo,40)));hi=mp.mpf(str(S.N(hi,40)));d=(hi-lo)/n
 return d/3*sum((1 if j in (0,n) else 4 if j%2 else 2)*fn(lo+j*d) for j in range(n+1))
def arc(expr,var,lo,hi):return S.sqrt(1+S.diff(expr,var)**2)

add(1,1,F(4*S.sqrt(5),'Arc length'),N(4*S.sqrt(5),'Distance between endpoints'),why='Slope 2 gives ds=sqrt(5)dx across an interval of width4.')
add(1,2,F(pi*S.sqrt(2)/4,'Arc length'),F(pi/4,'Central angle (radians)'),why='The circle has radius sqrt(2); the arc subtends pi/4.')
curves={3:(S.sin(x),x,0,pi),4:(x*S.exp(-x),x,0,2),5:(x-S.log(x),x,1,4),6:(y*y-2*y,y,0,2),7:(S.sqrt(y)-y,y,1,4),8:(S.exp(y*y),y,-1,1)}
for n,(e,v,l,u) in curves.items():
 f=arc(e,v,l,u);add(1,n,I(f,v,l,u),N(quad(f,v,l,u),'Length',tol=5.1e-5),why='Use ds=sqrt(1+(derivative)^2) times the independent-variable differential.')
exact={9:2*(82*S.sqrt(82)-1)/243,10:S.Rational(13,6),11:S.Rational(59,24),12:S.Rational(33,16),13:S.Rational(32,3),14:S.log(2+S.sqrt(3)),15:S.log(1+S.sqrt(2)),16:S.sinh(2)/2,17:S.Rational(3,4)+S.log(2)/2,18:2,19:S.log(3)-S.Rational(1,2)}
# Check source endpoints and algebra independently in check.py.
for n,val in exact.items():add(1,n,F(val,'Exact length'),why='Integrate sqrt(1+(derivative)^2); retain the nonnegative square root on the stated domain.')
def exp_primitive(z):return S.sqrt(1+z*z)+S.log(z/(1+S.sqrt(1+z*z)))
add(1,20,F(exp_primitive(1)-exp_primitive(S.exp(-2)),'Exact length'))
add(1,21,F(S.sqrt(2)+S.asinh(1),'Arc length'),limited=True)
add(1,22,F((80*S.sqrt(10)-13*S.sqrt(13))/27,'Arc length'),limited=True)
for n,e,l,u in [(23,x*x+x**3,1,2),(24,x+S.cos(x),0,pi/2)]:add(1,n,N(quad(arc(e,x,l,u),x,l,u),'Computed length',tol=5.1e-5),limited=True)
for n,e,l,u in [(25,x*S.sin(x),0,2*pi),(26,x**S.Rational(1,3),1,6),(27,S.log(1+x**3),0,5),(28,S.exp(-x*x),0,2)]:
 f=arc(e,x,l,u);add(1,n,N(simpson(f,x,l,u),'Simpson estimate, n=10',tol=5.1e-5),N(quad(f,x,l,u),'Accurate integral',tol=5.1e-5))
for n,e,l,u in [(29,x*(4-x)**S.Rational(1,3),0,4),(30,x+S.sin(x),0,2*pi)]:
 fs=[]
 for count in [1,2,4]:
  pts=[(S.Rational(j,count)*(u-l)+l) for j in range(count+1)]
  val=sum(S.sqrt((p2-p1)**2+(e.subs(x,p2)-e.subs(x,p1))**2) for p1,p2 in zip(pts,pts[1:]));fs.append(N(val,f'b · Polygon length n={count}',tol=5.1e-5))
 f=arc(e,x,l,u);fs.extend([I(f,x,l,u,'c · Arc-length integral'),N(quad(f,x,l,u),'d · Arc length',tol=5.1e-5)])
 add(1,n,*fs,limited=True)
add(1,31,F(exp_primitive(S.exp(2))-exp_primitive(1),'Exact length'))
# u=x^(1/3), then integrate 3u²sqrt(1+16u²/9) du.
add(1,32,F(S.Rational(205,128)-S.Rational(81,512)*S.log(3),'Exact length'))
add(1,33,N(6,'Total astroid length'),limited=True)
add(1,34,C('y=|x|^(2/3), an upward cusp at the origin','y=x^(3/2), only in the first quadrant','A circle of radius1',label='a · Curve'),I(S.sqrt(1+S.Rational(4,9)*x**(-S.Rational(2,3))),x,0,1,'b · Integral in x (improper at0)'),I(S.sqrt(1+S.Rational(9,4)*y),y,0,1,'b · Integral in y'),F((13*S.sqrt(13)-8)/27,'b · Length'),F((13*S.sqrt(13)+80*S.sqrt(10)-16)/27,'c · Length across both branches'),limited=True)
add(1,35,F(S.Rational(2,27)*((1+9*x)**S.Rational(3,2)-10**S.Rational(3,2)),'Arc-length function s(x)'))
add(1,36,C('s(x)=ln(tan(x/2)), 0<x<π','s(x)=ln(sin(x))','s(x)=tan(x/2)',label='a · Oriented arc-length function'),limited=True,why='The textbook uses s(x)=integral from starting x to x; for x<π/2 it is negative. Physical distance is |s(x)|.')
f37=S.sqrt(1+((1-x)/S.sqrt(1-x*x))**2)
add(1,37,F(2*S.sqrt(2)*(S.sqrt(1+x)-1),'Oriented arc-length function',suffix=', −1≤x≤1'))
f38=S.Rational(2,9)*(3*x+4)**S.Rational(3,2)+S.Rational(2,9);xx=((S.Rational(27,2)+5*S.sqrt(5))**S.Rational(2,3)-5)/3
add(1,38,F(f38,'a · f(x)'),N(xx,'b · x coordinate',tol=.00051),N(f38.subs(x,xx),'b · y coordinate',tol=.00051))
add(1,39,C('f²−(f′)²=1 and f>0, hence sqrt(1+(f′)²)=f','f′=f for this function','The arc length equals the area for every positive function',label='Proof identity'),limited=True)
add(1,40,N(quad(S.sqrt(1+(x-50)**2/400),x,0,80),'Distance','ft',tol=.0001))
add(1,41,N(quad(S.sqrt(1+4*x*x/2025),x,0,90),'Distance','m',tol=.051))
f42=S.sqrt(1+(S.Float('20.96')*S.Float('0.03291765')*S.sinh(S.Float('0.03291765')*x))**2)
add(1,42,I(f42,x,-S.Rational(912,10),S.Rational(912,10)),N(quad(f42,x,-S.Rational(912,10),S.Rational(912,10)),'Arch length','m',tol=.51))
add(1,43,C('Amplitude1 in and wavelength14 in give y=sin(πx/7)','Amplitude2 in and wavelength28 in give y=2sin(πx/14)','y=sin(7πx)',label='Sine profile'),N(quad(S.sqrt(1+(pi*S.cos(pi*x/7)/7)**2),x,0,28),'Flat-sheet width','in',tol=.0051),limited=True)
aa=mp.findroot(lambda z:2*z*mp.sinh(25/z)-51,(60,80));height=20+aa*(mp.cosh(25/aa)-1)
add(1,44,C('L=2a sinh(b/a)','L=2b cosh(b/a)','L=2a cosh(b/a)',label='a · Wire length'),N(height,'b · Attachment height','ft',tol=.0051))
add(1,45,F(S.Rational(62,5),'Curve length'),why='By FTC y′=sqrt(x³−1), so ds=x^(3/2)dx.')
add(1,46,C('L_(2k)=4∫[0,1] sqrt(1+x^(4k−2)*(1−x^(2k))^(1/k−2)) dx','L_(2k)=4∫[0,1] (1−x^(2k))^(1/(2k)) dx','L_(2k)=2π for every k',label='Arc-length integral'),N(8,'Limit as k→∞'),limited=True)
project='Project: Discovery Project Arc Length Contest'
add(1,1,C('Both endpoints must be zero: f(0)=f(1)=0','Only f(0)=0 is required','Both endpoints must equal1',label='Endpoint condition'),group=project,limited=True)
add(1,2,C('f(x)≥0 throughout [0,1]','f(x) must be negative throughout (0,1)','f(x) must be constant',label='Sign condition'),group=project,limited=True)
add(1,3,C('Example: f(x)=6x(1−x) has area1 and length sqrt(37)/2+asinh(6)/12','Example: f(x)=x(1−x) has area1','Every admissible graph has length1',label='One admissible construction'),C('Second example: f(x)=4x on [0,1/2], 4(1−x) on [1/2,1]; area1, length sqrt(17)','Second example: f(x)=1 satisfies both zero endpoints','Second example: f(x)=−6x(1−x) has area1',label='Second admissible construction'),group=project,limited=True)


# 8.2: surface areas; use geometric radius (nonnegative).
for n,e,v,l,u in [(1,S.tan(x),x,0,pi/3),(2,x**-2,x,1,2),(3,S.exp(-x*x),x,-1,1),(4,S.log(2*y+1),y,0,1),(5,y+y**3,y,0,1),(6,S.atan(x),x,0,2)]:
 ds=arc(e,v,l,u);rx=e if v==x else y;ry=x if v==x else e
 # Exercise3 crosses the y-axis; the two halves generate the SAME surface.
 # Integrate only x>=0 for its y-axis surface, rather than double-counting it.
 ly=0 if n==3 else l
 ix=2*pi*rx*ds;iy=2*pi*ry*ds
 add(2,n,I(ix,v,l,u,'a(i) · About x-axis'),I(iy,v,ly,u,'a(ii) · About y-axis'),N(quad(ix,v,l,u),'b(i) · x-axis area',tol=5.1e-5),N(quad(iy,v,ly,u),'b(ii) · y-axis area',tol=5.1e-5),why='Surface area uses 2π times radius times arc length. For #3 the two symmetric halves generate the same surface about the y-axis, so count it once.')
surface_exact={7:pi*(145**S.Rational(3,2)-1)/27,8:pi*S.Rational(13,3),9:pi*(17**S.Rational(3,2)-5**S.Rational(3,2))/6,10:pi*(S.E+1),11:2*pi*(S.sqrt(5)/2+2*S.asinh(S.Rational(1,2))),12:pi*(1+S.Rational(63,2304)),13:pi*S.Rational(21,2),14:pi*(65**S.Rational(3,2)-17**S.Rational(3,2))/24,15:S.Rational(3712,15)*pi,16:S.Rational(6,5)*pi,17:pi*a*a,18:S.Rational(10,3)*pi}
for n,val in surface_exact.items():add(2,n,F(val,'Exact surface area'))
for n,e,l,u in [(19,x**5/5,0,5),(20,x+x*x,0,1),(21,x*S.exp(x),0,1),(22,x*S.log(x),1,2)]:
 f=2*pi*e*arc(e,x,l,u);add(2,n,N(simpson(f,x,l,u),'Simpson estimate n=10',tol=.0001),N(quad(f,x,l,u),'Accurate integral',tol=.0001))
# Reciprocal curve: u=1/x² gives pi integral sqrt(1+u²)/u du.
add(2,23,F(pi*(exp_primitive(1)-exp_primitive(S.Rational(1,4))),'Exact area'))
add(2,24,F(pi*(3*S.sqrt(19)+S.asinh(3*S.sqrt(2))/S.sqrt(2)),'Exact area'))
add(2,25,F(pi*(S.sqrt(10)/2+S.asinh(3)/6),'Exact area'))
add(2,26,F(2*pi*(S.sqrt(5)-S.sqrt(2)/2+S.asinh(2)/2-S.asinh(1)/2-exp_primitive(2)+exp_primitive(1)),'Exact area'))
add(2,27,C('Infinite: 2π∫[1,∞] sqrt(1+x^(−4))/x dx ≥ 2π∫[1,∞] dx/x','Finite because its enclosed volume is finite','Zero because y tends to0',label='Surface area and comparison'),limited=True)
add(2,28,F(pi*(S.sqrt(2)+S.asinh(1)),'Surface area'))
add(2,29,F(pi*a*a/3,'a · About x-axis'),F(56*pi*a*a/(15*S.sqrt(3)),'b · About y-axis'),why='Parametrize x=at², y=a*t*(1−t²)/sqrt(3), 0≤t≤1. Upper/lower arcs produce the same x-axis surface, but distinct y-axis surfaces.')
add(2,30,N(S.Rational(2,25),'Parabola coefficient a','ft⁻¹'),F(pi*S.Rational(625,96)*((S.Rational(41,25))**S.Rational(3,2)-1),'Dish area (ft²)'))
add(2,31,C('2πb²+2πab*arcsin(e)/e, e=sqrt(1−b²/a²)','4πab','2πa²+2πb²',label='a · Prolate spheroid'),C('2πa²+2πb²*arctanh(e)/e, e=sqrt(1−b²/a²)','2πb²+2πab*arcsin(e)/e','4πb²',label='b · Oblate spheroid'))
add(2,32,C('4π²Rr, with major radius R and tube radius r','2π²Rr²','4πR²',label='Torus surface area'))
add(2,33,C('S=2π∫[a,b](c−f(x))*sqrt(1+f′(x)²)dx','S=2π∫[a,b]f(x)*sqrt(1+f′(x)²)dx','S=π∫[a,b](c−f(x))²dx',label='Area formula'),limited=True)
# Substitute t=sqrt(x): integrate (4−t)*sqrt(1+4t²).
val34=2*pi*(4*S.sqrt(17)+S.asinh(4)-(17**S.Rational(3,2)-1)/12)
add(2,34,I(2*pi*(4-S.sqrt(x))*S.sqrt(1+1/(4*x)),x,0,4),F(val34,'Exact area'))
add(2,35,F(4*pi*pi*r*r,'Surface area'))
add(2,36,C('y=sqrt(R²−x²) gives y*sqrt(1+y′²)=R, hence area2πRh','The spherical-zone area is πh²','The result requires a zone centered at the equator',label='a · Sphere-zone identity'),C('Unwrapping the cylinder gives a rectangle2πR by h, hence2πRh','Cylinder area is πR²h','Cylinder area is2πR²',label='b · Cylinder comparison'),limited=True)
add(2,37,C('1+(y′)²=y²/4; y>0, so2πy*sqrt(1+(y′)²)=πy²','y′=y','Surface area equals volume for every exponential curve',label='Integrand identity'),limited=True)
add(2,38,C('S_g=S_f+2πcL','S_g=S_f+cL','S_g=S_f+πc²L',label='Translated surface area'))
add(2,39,C('The radius is |f(x)|, so S=2π∫[a,b]|f(x)|sqrt(1+f′(x)²)dx','A negative y gives a negative surface area','Replace f′ by |f′| and keep a signed radius',label='Nonnegative-radius justification'),limited=True)
proj='Project: Discovery Project Rotating On A Slant'
add(2,1,C('Perpendicular radius=(f−mx−b)/sqrt(1+m²); du=(1+mf′)dx/sqrt(1+m²)','Perpendicular radius=f−mx−b and du=dx','Perpendicular radius=(f−mx−b)(1+m²)',label='Rotated coordinates'),group=proj,limited=True,why='Assumes projection onto the axis is one-to-one with 1+mf′≥0, as in the drawn region.')
add(2,2,F(4*pi,'Region area'),group=proj)
add(2,3,C('V=π/(1+m²)^(3/2) ∫[p,q](f−mx−b)²(1+mf′)dx','V=π∫[p,q](f−mx−b)²dx','V=π/(1+m²)∫[p,q](f−mx−b)dx',label='Volume formula'),group=proj,limited=True)
add(2,4,F(9*pi*pi/S.sqrt(2),'Volume'),group=proj)
add(2,5,C('S=2π/sqrt(1+m²) ∫[p,q](f−mx−b)sqrt(1+f′²)dx','S=2π∫[p,q](f−mx−b)sqrt(1+f′²)dx','S=π/(1+m²)∫[p,q](f−mx−b)²dx',label='Surface area formula'),group=proj,limited=True)
# t=sqrt(x), radius=(2t−t²)/sqrt5, ds=sqrt(1+4t²)dt.
slant_integrand=2*pi/S.sqrt(5)*(2*t-t*t)*S.sqrt(1+4*t*t)
slant_value=2*pi/S.sqrt(5)*((17**S.Rational(3,2)-1)/6-S.Rational(33,16)*S.sqrt(17)+S.asinh(4)/64)
add(2,6,F(slant_value,'Exact surface area'),N(quad(slant_integrand,t,0,2),'Approximate surface area',tol=.00051),group=proj)


# 8.4 Economics and physiology: textbook units retained.
add(4,1,N(18000+S.Rational(82,100)*4000-S.Rational(3,100000)*4000**2/2+S.Rational(3,10**9)*4000**3/3,'Total production cost','$'))
add(4,2,N(48*5000-S.Rational(12,10000)*(10000**2-5000**2)/2,'Increase in revenue','$'))
add(4,3,N(140000,'First50 tons, including startup','$'),N(60000,'Next50 tons, incremental cost','$'))
add(4,4,N(S.Rational(46,3)*400**S.Rational(3,2),'Consumer surplus','$'),limited=True)
add(4,5,N(450*S.log(S.Rational(45,8))-370,'Consumer surplus','$',tol=.0051))
add(4,6,N(S.Rational(20,3),'Producer surplus','$',tol=.0051),limited=True)
add(4,7,N(S.Rational(500000,3),'Producer surplus','$',tol=.0051))
add(4,8,N(200,'a · Equilibrium quantity'),N(40,'a · Equilibrium price','$'),N(1000,'b · Consumer surplus','$'),N(2000,'b · Producer surplus','$'),limited=True)
add(4,9,N(3.8,'a · Equilibrium quantity','thousand stereos'),N(324900,'b · Maximum total surplus','$'),why='The integral in x has thousand-dollar units because x is measured in thousands.')
eq10=mp.log(12)/mp.mpf('.34');ts10=1000*(312*(1-mp.exp(-mp.mpf('.14')*eq10))/mp.mpf('.14')-26*(mp.exp(mp.mpf('.2')*eq10)-1)/mp.mpf('.2'))
add(4,10,N(ts10,'Maximum total surplus','$',tol=.01))
eq11=mp.findroot(lambda z:800000*mp.exp(-z/5000)/(z+20000)-16,4000)
cs11=mp.quad(lambda z:800000*mp.exp(-z/5000)/(z+20000)-16,[0,eq11])
add(4,11,N(eq11,'Sales level',tol=1),N(cs11,'Consumer surplus','$',tol=1),limited=True)
add(4,12,C('p(x)=15−0.01x','p(x)=10−0.5x','p(x)=15−0.1x',label='Demand function'),N(2450,'Consumer surplus at$8','$'))
add(4,13,N(S.Rational(2,3)*(8**S.Rational(3,2)-8),'Capital formation','million dollars'))
add(4,14,N(78000,'Revenue in first4 years','$'))
pv=8000*(1-mp.exp(-mp.mpf('.022')*6))/mp.mpf('.022')
add(4,15,N(pv*mp.exp(mp.mpf('.062')*6),'Future value after6 years','$',tol=.0051))
add(4,16,N(pv,'Present value','$',tol=.0051))
add(4,17,C('(1−k)/(2−k)*(b^(2−k)−a^(2−k))/(b^(1−k)−a^(1−k)), k≠2','(b−a)/2','A*(b−a)',label='Average income, k≠2'),C('ab*ln(b/a)/(b−a), k=2','(a+b)/2, k=2','ln(b/a), k=2',label='Special case k=2'),why='Assume0<a<b. Normalize the first moment by the population N; A cancels.')
add(4,18,N(8800+mp.mpf('12.5')*(mp.exp(mp.mpf('7.2'))-mp.exp(4)),'Population increase','mosquitoes',tol=.51))
add(4,19,N(pi*S.Rational(4000)*S.Rational(8,1000)**4/(8*S.Rational(27,1000)*2),'Volume flow rate','cm³/s',tol=1e-9))
add(4,20,C('At fixed viscosity and length, PR⁴=P₀R₀⁴, so P/P₀=(R₀/R)⁴','P/P₀=R/R₀','P/P₀=(R₀/R)²',label='Constant-flux relation'),N(S.Rational(256,81),'Pressure multiplier at R=3R₀/4'),limited=True)
add(4,21,N(6/(20*(1-7*mp.exp(-6))/mp.mpf('.36')),'Cardiac output','L/s',tol=.000051))
cc=[0,4.1,8.9,8.5,6.7,4.3,2.5,1.2,.2];integ22=S.Rational(2,3)*sum((1 if j in (0,8) else 4 if j%2 else 2)*S.Rational(str(z)) for j,z in enumerate(cc))
add(4,22,N(S.Rational(55,10)/integ22,'Cardiac output','L/s',tol=.000051))
# Printed graph has not returned to baseline at16s; graph-only quadrature is approximate.
cgraph=[0,6.1,7.4,6.7,5.5,4.1,3.0,2.1,1.5]
ig=2/3*sum((1 if j in (0,8) else 4 if j%2 else 2)*v for j,v in enumerate(cgraph))
add(4,23,N(7/ig,'Graph-based cardiac output over shown0–16s','L/s',tol=.008),limited=True,why='Read approximate concentrations every2s and apply Simpson. The plotted curve is still positive at16s, so the missing tail prevents an exact full-passage output; this checks the textbook graph-window estimate only.')

# 8.5 probability; probability fields use fractions0–1, not percentages unless labeled.
add(5,1,C('Probability the tire lasts between30,000 and40,000 miles','Mean tire lifetime','Probability the tire fails before30,000 miles',label='a · Integral interpretation'),C('Probability the tire lasts at least25,000 miles','Probability the tire lasts less than25,000 miles','Mean tire lifetime conditional on25,000 miles',label='b · Integral interpretation'),limited=True)
add(5,2,C('∫[0,15] f(t)dt','∫[15,∞] f(t)dt','15*f(15)',label='a · Under15 minutes'),C('∫[30,∞] f(t)dt','∫[0,30] f(t)dt','f(30)',label='b · Over30 minutes'))
add(5,3,C('f≥0 and ∫[0,1]30x²(1−x)²dx=1','f is a density merely because it is positive','∫f dx=30',label='a · Density conditions'),N(S.Rational(17,81),'b · P(X≤1/3)'),limited=True)
add(5,4,C('f≥0 and F(x)=1/(1+e^(3−x)) increases from0 to1','f integrates to3','The density is negative for x<3',label='a · Density verification'),N(1/(1+mp.exp(-1))-.5,'b · P(3≤X≤4)'),N(3,'c · Mean'),N(3,'c · Median'),limited=True)
add(5,5,F(1/pi,'a · c'),N(.5,'b · P(−1<X<1)'))
add(5,6,N(S.Rational(2,9),'a · k'),N(S.Rational(20,27),'b · P(X>1)'),N(1.5,'c · Mean'))
add(5,7,C('Nonnegative, with total area10×0.1=1','A density must be strictly positive on the whole real line','The total area is10',label='a · Density justification'),N(5,'b · Mean'),limited=True)
# The graph is triangular, vertices(0,0),(6,.2),(10,0).
add(5,8,C('Nonnegative triangle with base10 and height0.2 has area1','Its area is2','Its maximum value must equal1',label='a · Density verification'),N(.15,'b(i) · P(X<3)'),N(.75,'b(ii) · P(3≤X≤8)'),N(S.Rational(16,3),'c · Mean'),limited=True)
add(5,9,N(5*mp.log(2),'Median waiting time','min',tol=.051),limited=True)
add(5,10,N(1-mp.exp(-mp.mpf('.2')),'a(i) · P(failure within200h)'),N(mp.exp(-mp.mpf('.8')),'a(ii) · P(lifetime>800h)'),N(1000*mp.log(2),'b · Median lifetime','h',tol=.0051))
add(5,11,N(1-mp.exp(-1/mp.mpf('1.6')),'a · P(T<1s)'),N(mp.exp(-3/mp.mpf('1.6')),'b · P(T>3s)'),N(-mp.mpf('1.6')*mp.log(mp.mpf('.05')),'c · Slowest5% threshold','s',tol=.000051))
inc=lambda u:mp.exp(-u/20)*(-20*u*u-800*u-16000)
add(5,12,N((inc(48)-inc(0))/15676,'a · P(T≤48h)',tol=.000051),N((inc(150)-inc(36))/15676,'b · P(T>36h)',tol=.000051),why='Use the printed truncated density on0≤t≤150. Its rounded normalization15676 is used as supplied.')
add(5,13,N(S.Rational(19,32),'a · P(30≤T≤60)'),N(40,'b · Mean REM time','min'))
Phi=lambda z:(1+mp.erf(z/mp.sqrt(2)))/2
add(5,14,N(Phi(4/mp.mpf('2.8'))-Phi(-4/mp.mpf('2.8')),'a · Probability65–73in'),N(100*(1-Phi(3/mp.mpf('2.8'))),'b · Percentage over6ft','%',tol=.0051))
add(5,15,N(100*(1-Phi(mp.mpf('.6')/mp.mpf('4.2'))),'Households discarding at least10lb','%',tol=.0051))
add(5,16,N(Phi(-mp.mpf(20)/12),'a · P(weight<480g)'),N(500+12*mp.sqrt(2)*mp.erfinv(mp.mpf('.9')),'b · Minimum target mean','g',tol=.00051))
add(5,17,N(Phi(-mp.mpf(12)/8),'a · Probability of legal speed'),N(100*(1-Phi(mp.mpf(13)/8)),'b · Percentage targeted','%',tol=.0051))
add(5,18,C('f″(x)=((x−μ)²−σ²)f(x)/σ⁴ changes sign at μ−σ and μ+σ','f″ vanishes only at μ','Inflection points are μ±σ²',label='Inflection-point test'),limited=True)
add(5,19,N(mp.erf(mp.sqrt(2)),'Probability within2 standard deviations'))
add(5,20,C('σ=μ for an exponential distribution with mean μ','σ=μ²','σ=sqrt(μ)',label='Standard deviation'))
add(5,21,C('p≥0 and substitution u=2r/a₀ gives ∫p dr=(1/2)∫[0,∞]u²e^(−u)du=1','The integral of p is a₀','The density must be less than1 everywhere',label='a · Normalization'),N(0,'b · Limit as r→∞'),C('r=a₀','r=2a₀','r=0',label='b · Peak position'),N(1-41*mp.exp(-8),'d · P(r≤4a₀)'),C('Mean distance=3a₀/2','Mean distance=a₀','Mean distance=2a₀',label='e · Mean radius'),limited=True,why='Keep the symbolic Bohr radius; the historical printed numerical value is not needed for these dimensionless checks.')


# 8.3 hydrostatics and centroids. g=9.8m/s²; US water weight density62.4lb/ft³.
water=S.Rational(312,5)
add(3,1,N(water*3,'a · Bottom gauge pressure','lb/ft²'),N(water*30,'b · Bottom force','lb'),N(water*9,'c · End-wall force','lb'))
add(3,2,N(820*9.8*1.5,'a · Bottom gauge pressure','Pa'),N(820*9.8*1.5*32,'b · Bottom force','N'),N(820*9.8*4*1.5**2/2,'c · End-wall force','N'))
def hydro(n,width,lo,hi,gamma,unit,exact=False):
 integrand=gamma*x*width
 value=S.integrate(integrand,(x,lo,hi)) if exact else quad(integrand,x,lo,hi)
 fs=[C('Sum pressure(depth) × strip width × strip height, then take the mesh-size limit','Multiply the maximum pressure by every strip area','Add pressures without strip areas',label='Riemann-sum interpretation'),I(integrand,x,lo,hi,'Force integral')]
 fs.append(F(value,'Exact force') if exact else N(value,'Hydrostatic force',unit,tol=.01))
 add(3,n,*fs,limited=True,why='x is depth below the water surface; use only the submerged portion. Pressure is gauge pressure.')
hydro(3,S.Integer(2),3,11,water,'lb')
hydro(4,2*(x-2),2,7,water,'lb')
hydro(5,2*S.sqrt(64-(x-12)**2),4,20,S.Integer(9800),'N')
hydro(6,2*S.sqrt(36-(4-x)**2),0,4,S.Integer(9800),'N')
hydro(7,2*(1-x/S.sqrt(3)),0,S.sqrt(3),S.Integer(9800),'N')
hydro(8,3*(x-4),4,6,S.Integer(9800),'N')
hydro(9,S.Rational(16,3)+4*x/3,0,2,water,'lb')
add(3,10,C('Split at depth a/√2; strip widths are2x and2(√2a−x)','Width is always a','Use the whole bounding square of width√2a',label='Strip geometry'),C('F=ρg a³/√2','F=ρg a³','F=2ρg a³',label='Hydrostatic force'),limited=True,why='a is the side length of the diamond-oriented square; ρg is the fluid weight density.')
add(3,11,C('F=ρg∫[0,h]x(2a−ax/h)dx=2ρg ah²/3','F=ρg ah²/2','F=ρg ah²',label='Force integral and value'),limited=True)
add(3,12,N(S.Rational(646,10)*27*pi,'a · Full-tank end force','lb',tol=.01),N(S.Rational(646,10)*18,'b · Half-full end force','lb',tol=.01))
add(3,13,N(840*S.Rational(98,10)*64,'End force','N',tol=.01))
add(3,14,N(9800*(20*pi-S.Rational(16,3)),'Gate force','N',tol=.01),why='Water depth is10m, gate radius2m, and its centroid is8/(3π)m above the bottom.')
add(3,15,N(313.6,'a · Force on top','N'),N(352.8,'b · Force on one side','N'))
add(3,16,N(water*S.sqrt(3)/2*(100*70**2/2-S.Rational(5,7)*70**3/3),'Dam force','lb',tol=.1),why='Use slant coordinate s; vertical depth is s cos30°, but area element is width(s)ds.')
add(3,17,N(water*20*9/2,'a · Shallow-end force','lb'),N(water*20*81/2,'b · Deep-end force','lb'),N(water*S.Rational(40,6)*(9**3-3**3)/6,'c · One long-side force','lb'),N(water*6*20*S.sqrt(40**2+6**2),'d · Bottom force','lb',tol=.1))
add(3,18,C('Each strip has pressureρgx and area w(x)Δx, so F=∫[a,b]ρgxw(x)dx','Pressure is constantρgb on every strip','F=∫[a,b]ρg w(x)dx',label='Force derivation'),limited=True)
depths=[7,7.4,7.8,8.2,8.6,9,9.4];widths=[1.2,1.8,2.9,3.8,3.6,4.2,4.4]
weighted=S.Rational(4,30)*sum((1 if j in (0,6) else 4 if j%2 else 2)*S.Rational(str(z))*S.Rational(str(w)) for j,(z,w) in enumerate(zip(depths,widths)))
add(3,19,N(64*weighted/S.Rational(3048,10000)**3,'Hydrostatic force','lb',tol=.1),why='The table uses meters but density useslb/ft³. Convert the cubic-length factor by dividing by0.3048³; do not mix the units.')
add(3,20,C('x̄=(1/A)∫xw(x)dx, soρg x̄ A=ρg∫xw(x)dx','The centroid depth is always half the bottom depth','All plates have the same force at a given deepest point',label='a · Centroid identity'),C('F=ρg a³/√2','F=ρg a³/2','F=2ρg a³',label='b · Exercise10'),limited=True)
add(3,21,N(330,'Moment M'),N(22,'Center x̄'))
add(3,22,N(154,'Moment M'),N(S.Rational(154,47),'Center x̄'))
for n,masses,pts in [(23,[4,2,4],[(2,-3),(-3,1),(3,5)]),(24,[5,4,3,6],[(-4,2),(0,5),(3,2),(1,-2)])]:
 mx=sum(m*p[1] for m,p in zip(masses,pts));my=sum(m*p[0] for m,p in zip(masses,pts));mass=sum(masses)
 add(3,n,N(mx,'Moment Mₓ'),N(my,'Moment Mᵧ'),N(S.Rational(my,mass),'x̄'),N(S.Rational(mx,mass),'ȳ'))
def center(n,top,bot,lo,hi,limited=False):
 area=S.integrate(top-bot,(x,lo,hi));my=S.integrate(x*(top-bot),(x,lo,hi));mx=S.integrate((top**2-bot**2)/2,(x,lo,hi))
 add(3,n,F(my/area,'x̄'),F(mx/area,'ȳ'),limited=limited)
for n,top,bot,lo,hi in [(25,2*x,0,0,1),(26,S.sqrt(x),0,0,4),(27,S.exp(x),0,0,1),(28,S.sin(x),0,0,pi),(29,S.sqrt(x),x*x,0,1),(30,2-x*x,x,-2,1),(31,S.cos(x),S.sin(x),0,pi/4)]:center(n,top,S.sympify(bot),lo,hi,limited=n<=28)
# Piecewise triangle above cubic and x-axis; split at x=1.
area32=S.Rational(3,4);my32=S.Rational(1,5)+S.Rational(2,3);mx32=S.Rational(1,14)+S.Rational(1,6)
add(3,32,F(my32/area32,'x̄'),F(mx32/area32,'ȳ'))
# y horizontal strips, −2≤y≤1, right=2−y,left=y².
area33=S.integrate(2-y-y*y,(y,-2,1));mx33=S.integrate(y*(2-y-y*y),(y,-2,1));my33=S.integrate(((2-y)**2-y**4)/2,(y,-2,1))
add(3,33,F(my33/area33,'x̄'),F(mx33/area33,'ȳ'))
add(3,34,N(12,'Moment Mₓ'),N(8,'Moment Mᵧ'),N(S.Rational(2,3),'x̄'),N(1,'ȳ'))
add(3,35,N(80,'Moment Mₓ'),N(224,'Moment Mᵧ'),F(224/(24*pi+48),'x̄'),F(80/(24*pi+48),'ȳ'))
# Source graph readings at integer abscissae; explicit graphical tolerances.
gy=[0,2,2.6,2.3,2.2,3.3,4,3.2,0]
def simtab(vals):return sum((1 if j in (0,8) else 4 if j%2 else 2)*v for j,v in enumerate(vals))/3
ag=simtab(gy)
add(3,36,N(simtab([j*v for j,v in enumerate(gy)])/ag,'Estimated x̄',tol=.15),N(simtab([v*v/2 for v in gy])/ag,'Estimated ȳ',tol=.15),why='Simpson with h=1 on the plotted graph; readings are approximate, so centroid tolerances reflect graph precision.')
center(37,x**3-x,x*x-1,-1,1,limited=True)
l38=mp.findroot(lambda z:mp.exp(z)+z*z-2,-1.3);u38=mp.findroot(lambda z:mp.exp(z)+z*z-2,.5)
a38=mp.quad(lambda z:2-z*z-mp.exp(z),[l38,u38]);my38=mp.quad(lambda z:z*(2-z*z-mp.exp(z)),[l38,u38]);mx38=mp.quad(lambda z:((2-z*z)**2-mp.exp(2*z))/2,[l38,u38])
add(3,38,N(l38,'Left intersection x',tol=.00051),N(u38,'Right intersection x',tol=.00051),N(my38/a38,'x̄',tol=.00051),N(mx38/a38,'ȳ',tol=.00051),limited=True)
add(3,39,C('Centroid=((a+c)/3,b/3); each median reaches this point two-thirds of the way from its vertex','Centroid=((a+c)/2,b/2)','Centroid=(a+c,b)',label='Centroid and median intersection'),limited=True)
add(3,40,N(S.Rational(1,12),'x̄'),N(S.Rational(5,6),'ȳ'))
add(3,41,N(0,'x̄'),N(S.Rational(1,12),'ȳ'))
add(3,42,C('R₁:(3a/4,3b/10)','R₁:(a/2,b/2)','R₁:(a/4,b/3)',label='Centroid R₁'),C('R₂:(3a/8,3b/5)','R₂:(a/2,b/2)','R₂:(3a/4,3b/10)',label='Centroid R₂'))
add(3,43,C('Expand c∫xf dx+d∫f dx and substitute∫xf dx=x̄∫f dx','Assume f is constant','Replace every x in any integrand by x̄ regardless of its dependence',label='Moment identity'),limited=True)
add(3,44,F(4*pi*r**3/3,'Sphere volume'),why='A semicircle has areaπr²/2 and centroid distance4r/(3π) from its diameter.')
add(3,45,F(pi*r*r*h/3,'Cone volume'))
add(3,46,F(24*pi,'Volume'))
add(3,47,F(8/pi,'x̄'),F(8/pi,'ȳ'))
add(3,48,C('S=∫2πy ds=2πȳL','S=2πȳL²','S=πȳ²L',label='a · Second Pappus theorem'),F(32*pi,'b · Hemisphere area'),limited=True)
add(3,49,C('4π²Rr','2π²Rr²','4πR²',label='Torus surface area'))
add(3,50,C('On0<x<1, x^m<x^n because m>n>0','x^m>x^n throughout(0,1)','The curves never meet at the endpoints',label='a · Region'),C('x̄=(m+1)(n+1)/((m+2)(n+2))','x̄=(m+n)/2','x̄=1/2',label='b · x̄'),C('ȳ=(m+1)(n+1)/((2m+1)(2n+1))','ȳ=1/2','ȳ=(m+n)/(m+n+1)',label='b · ȳ'),C('Example m=20,n=10 puts ȳ above x̄^10, outside the region','Every centroid must lie inside every nonconvex region','m=2,n=1 puts the centroid outside',label='c · Valid outside-centroid example'),limited=True)
add(3,51,C('A=∫(f−g)dx, Mᵧ=ρ∫x(f−g)dx, Mₓ=(ρ/2)∫(f²−g²)dx; divide moments byρA','Mₓ=ρ∫x(f−g)dx','Divide both moments by the interval length',label='Strip moments yielding Formulas9'),limited=True)
proj='Project: Discovery Project Complementary Coffee Cups'
add(3,1,C('k=(2/h)∫[0,h]f(y)dy','k=(1/h)∫[0,h]f(y)dy','k=∫[0,h]f(y)²dy',label='Equal-volume condition'),group=proj)
add(3,2,C('A₁=A₂=kh/2','A₁=2A₂','The areas need not be equal when the cup volumes are equal',label='Cross-section areas'),group=proj)
add(3,3,C('Equal areas give equally distant centroids from their respective axes; Pappus then gives equal volumes','Pappus says equal volumes imply identical cup shapes','Volume is area times height for either cup',label='Pappus explanation'),group=proj,limited=True)
add(3,4,C('Example h=10cm, f(y)=2+y/10cm, k=5cm: both volumes190π/3cm³','The same example gives both volumes100πcm³','The same example gives volume0',label='One valid measured-model example'),group=proj,limited=True,why='This checks a stated illustrative model, not the learner’s independently measured cups or report.')


# Chapter review: concept selections retain original multipart distinctions.
def rc(n,*fs):add('review',n,*fs,group='Concept Check',limited=True)
rc(1,C('Limit of inscribed polygon lengths as maximum subinterval width tends to0','Area under the curve','Distance between endpoints for every curve',label='a · Definition'),C('L=∫[a,b]sqrt(1+f′(x)²)dx','L=∫[a,b]f(x)dx','L=f(b)−f(a)',label='b · y=f(x)'),C('L=∫[c,d]sqrt(1+g′(y)²)dy','L=∫[c,d]g(y)dy','L=g(d)−g(c)',label='c · x=g(y)'))
rc(2,C('S=2π∫|f(x)|sqrt(1+f′(x)²)dx','S=π∫f(x)²dx','S=∫sqrt(1+f′(x)²)dx',label='a · x-axis, y=f(x)'),C('S=2π∫|y|sqrt(1+g′(y)²)dy','S=2π∫|g(y)|sqrt(1+g′(y)²)dy','S=π∫g(y)²dy',label='b · x-axis, x=g(y)'),C('S=∫2π|x|ds, counting each generated surface once','S=∫2π|y|ds','S=π∫x²ds',label='c · y-axis'))
rc(3,C('Integrateρg times vertical depth times horizontal strip width over depth','Multiply the deepest pressure by every strip area','Integrate fluid density alone',label='Hydrostatic force'))
rc(4,C('The balance point of the uniform thin plate','Always a point on the boundary','Always the midpoint of its bounding rectangle',label='a · Physical meaning'),C('x̄=∫xf(x)dx/∫f(x)dx; ȳ=∫f(x)²dx/(2∫f(x)dx)','x̄=(a+b)/2 and ȳ=0 for every shape','Both coordinates equal total area',label='b · Coordinates for f≥0'))
rc(5,C('Volume=area×distance traveled by its centroid; axis does not cut the region interior','Volume=arc length×area','The axis may cut the interior without changing the formula',label='Pappus theorem'))
rc(6,C('Consumer surplus=∫[0,X](p(x)−P)dx, area above priceP and below demand','Consumer surplus=PX','Consumer surplus=∫[0,X]p(x)dx without subtracting spending',label='Consumer surplus'))
rc(7,C('Volume of blood pumped per unit time','Blood pressure','Dye mass per liter',label='a · Cardiac output'),C('Inject known dye massA and measure concentration c(t); output=A/∫c(t)dt','Output=A∫c(t)dt','Output=max c(t)',label='b · Dye dilution'))
rc(8,C('f≥0, integral over all outcomes=1, and interval probabilities are integrals of f','f must be≤1 everywhere','The mean must equal1',label='Density properties'))
rc(9,C('Probability that weight is at most130lb','Mean weight130lb','Probability that weight is exactly130lb',label='a · Integral meaning'),C('μ=∫x f(x)dx over the support','μ=∫f(x)dx','μ=max f(x)',label='b · Mean'),C('Find m with∫[−∞,m]f(x)dx=1/2','Set f(m)=1/2','Use the midpoint of any chosen interval',label='c · Median'))
rc(10,C('Gaussian density exp(−(x−μ)²/(2σ²))/(σ√(2π)); σ sets spread aroundμ','Every symmetric density is normal','σ is the total area under the density',label='Normal distribution and spread'))
add('review',1,F((109*S.sqrt(109)-1)/54,'Length'))
add('review',2,F(2*S.log(2+S.sqrt(3)),'Length'))
add('review',3,F(S.Rational(53,6),'Length'))
add('review',4,F(S.Rational(21,16),'a · Length'),F(41*pi/10,'b · Surface area'))
e=2/(x+1);ds=arc(e,x,0,3)
add('review',5,N(quad(ds,x,0,3),'a · Arc length',tol=5.1e-5),N(quad(2*pi*e*ds,x,0,3),'b · x-axis area',tol=5.1e-5),N(quad(2*pi*x*ds,x,0,3),'c · y-axis area',tol=5.1e-5))
add('review',6,F(pi*(5*S.sqrt(5)-1)/6,'a · y-axis area'),F(pi*(18*S.sqrt(5)-S.asinh(2))/32,'b · x-axis area'))
add('review',7,N(simpson(S.sqrt(1+S.cos(x)**2),x,0,pi),'Simpson length n=10',tol=5.1e-5))
add('review',8,N(simpson(2*pi*S.sin(x)*S.sqrt(1+S.cos(x)**2),x,0,pi),'Simpson surface area n=10',tol=5.1e-5))
add('review',9,F(S.Rational(124,5),'Curve length'))
add('review',10,F(4088*pi/9,'Surface area'))
add('review',11,N(water*S.Rational(22,3),'Gate force','lb'))
add('review',12,N(water*S.Rational(512,15),'End force','lb'))
add('review',13,N(S.Rational(4,3),'x̄'),N(S.Rational(4,3),'ȳ'))
add('review',14,F(16/(pi+2),'x̄'),F(-16/(3*(pi+2)),'ȳ'))
add('review',15,N(S.Rational(8,5),'x̄'),N(1,'ȳ'))
add('review',16,F(pi/2,'x̄'),F((pi+2)/(8*S.sqrt(2)),'ȳ'))
add('review',17,F(2*pi*pi,'Volume'))
add('review',18,N(0,'x̄'),F(4*r/(3*pi),'ȳ'))
add('review',19,N(S.Rational(21500,3),'Consumer surplus','$',tol=.0051))
ct=[0,1.9,3.3,5.1,7.6,7.1,5.8,4.7,3.3,2.1,1.1,.5,0]
int20=S.Rational(2,3)*sum((1 if j in (0,12) else 4 if j%2 else 2)*S.Rational(str(v)) for j,v in enumerate(ct))
add('review',20,N(6/int20,'Cardiac output','L/s',tol=.000051))
add('review',21,C('f≥0 on[0,10] and its integral is1','f has maximum1','The mean equals the integral of f',label='a · Density verification'),N((1-S.cos(2*pi/5))/2,'b · P(X<4)'),N(5,'c · Mean'),limited=True)
add('review',22,N(100*(Phi(mp.mpf(12)/15)-Phi(-mp.mpf(18)/15)),'Percentage lasting250–280 days','%',tol=.0051))
add('review',23,N(1-mp.exp(-mp.mpf(3)/8),'a · Served within3min'),N(mp.exp(-mp.mpf(10)/8),'b · Wait over10min'),N(8*mp.log(2),'c · Median','min',tol=.000051))

# Problems Plus: source-specific geometry and probability derivations.
def pp(n,*fs,**kw):add('problems-plus',n,*fs,group='Problems Plus',**kw)
pp(1,F(2*pi/3-S.sqrt(3)/2,'Area'))
pp(2,N(S.Rational(5,8),'x̄'),N(0,'ȳ'))
pp(3,C('Small zone2πr(r−d); large zone2πr(r+d)','Both zones2πr²','Small zoneπ(r−d)²; large zoneπ(r+d)²',label='a · Zone areas'),N(2*pi*3960**2*(1-S.sin(75*pi/180)),'b · Arctic estimate','mi²',tol=1),C('Both areas2πrh because spherical-zone integrand is constant2πr','Both areasπh²','The equality holds only at the equator',label='c · Cylinder equality'),N(4*pi*3960**2*S.sin(S.Rational(2345,100)*pi/180),'d · Torrid-zone area','mi²',tol=1),limited=True)
pp(4,C('The horizon plane is r²/(r+H) from the center, so cap height=rH/(r+H) and area=2πr²H/(r+H)','Cap height=H for every observer height','Visible area=4πr² for anyH>0',label='a · Visible-area derivation'),C('Between centers: x*=d*r^(3/2)/(r^(3/2)+R^(3/2)) from the r-sphere center, clipped to[r,d−R]','Always midway between centers','x*=dr/(r+R) for all radii',label='b · Best position between the spheres'),limited=True,why='The stationary point maximizes illuminated area when it lies in the external gap. Otherwise the best boundary is the limiting position at the nearer sphere surface; a strictly exterior point may approach but not attain it.')
pp(5,C('dP/dz=ρ(z)g; P(z)=P₀+g∫[0,z]ρ(s)ds','P(z)=ρ(z)gz for every variable density','dP/dz=ρ′(z)g',label='a · Pressure'),C('F=2∫[L−r,L+r][P₀+ρ₀gH(e^(z/H)−1)]sqrt(r²−(z−L)²)dz','F=πr²ρ₀gL for everyH','F=2∫[L−r,L+r]ρ₀e^(z/H)gz sqrt(r²−(z−L)²)dz',label='b · Total external force'),limited=True,why='For net force against an interior pressureP₀, omit the constantP₀ term; the question asks total external force.')
pp(6,F(S.sqrt(3)/2,'Optimal height'))
pp(7,F(S.sqrt(2)*b,'Pyramid height'),F(pi*b**3*(28*S.sqrt(6)/27-2),'Intersection volume'),why='Tangency to the base edges fixes sphere radiusb. Subtract four disjoint spherical caps beyond the inclined pyramid faces from the upper hemisphere; each face is b*sqrt(2/3) from the center.')
pp(8,C('Choose width w(z)=C/z for depthz≥2m, with anyC>0 and finite lower edge','Choose constant width','Choose w(z)=Cz',label='Equal-force strip shape'),limited=True,why='Force densityρgz w(z) is constant, so every horizontal strip of the same height has equal force.')
cut=mp.findroot(lambda c:(mp.mpf(2)/3*(1-c*c)**mp.mpf('1.5'))/(mp.acos(c)-c*mp.sqrt(1-c*c))-.5,.15)
pp(9,N(cut,'Distance of cut from center','m',tol=.0051))
pp(10,N(S.Rational(55,14),'Centroid height above bottom','cm',tol=.000051))
pp(11,F(2/pi,'Probability h=L'),F(1/pi,'Probability h=L/2'))
alpha=S.asin(S.Rational(4,7))
pp(12,F(1+S.Rational(2,1)/pi*(S.Rational(7,4)-S.sqrt(33)/4-alpha),'a · At least one line'),F(S.sqrt(33)/(2*pi)-1+2*alpha/pi,'b · Two lines'),C('P(three)=2/(πL)*[sqrt(h²−4L²)−2L*arccos(2L/h)], 2L<h≤3L','P(three)=2h/(πL)','P(three)=1 for everyh>2L',label='c · General three-line probability'))
pp(13,N(0,'x̄'),N(-1,'ȳ'))

if __name__=='__main__':
 out=ROOT/'scripts/calculus-answer-checks/chapter-08.json';out.write_text(json.dumps(ROWS,ensure_ascii=False,indent=2)+'\n');print(len(ROWS),'of',len(QS))
