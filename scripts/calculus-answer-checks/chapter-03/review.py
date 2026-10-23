#!/usr/bin/env python3
"""Original checks for the 134 Chapter 3 review records, source pp.266–269.

Source equations are explicitly transcribed below after PDF image inspection.
Symbolic derivatives are computed locally, with independent finite-difference
and explicit mathematical regressions. No answer-key/solution-manual parsing.
"""
import gzip, hashlib, json, math, random
from pathlib import Path
import sympy as S
import mpmath as mp

ROOT=Path(__file__).resolve().parents[3]
SOURCE=json.loads(gzip.decompress((ROOT/'site/questions/calculus.json.gz').read_bytes()))
QS={q['id']:q for q in SOURCE if q['chapter']==3 and q['sourceSet']=='chapter-03-review'}
ROWS={}; TESTS=[]
x=S.symbols('x', positive=True)
t,u,theta=S.symbols('t u theta', real=True)
y,m,n,a,b,c,lam,omega,delta=S.symbols('y m n a b c lambda omega delta', real=True)

def fmt(v):
    return S.sstr(v).replace('**','^').replace('sqrt','sqrt').replace('asin','arcsin').replace('acos','arccos').replace('atanh','arctanh').replace('atan','arctan').replace('acosh','arccosh').replace('asinh','arcsinh').replace('log','ln')

def N(v,label='Your answer',unit='',tol=1e-8):
    return dict(type='numeric',answer=float(v),label=label,unit=unit,tolerance=tol)

def C(answer,*wrong,label='Your answer',why=''):
    assert wrong and answer not in wrong and len(set(wrong))==len(wrong),(answer,wrong)
    return dict(type='choice',answer=answer,options=[answer,*wrong],label=label,explanation=why)

def F(value,label='Derivative',why=''):
    value=S.simplify(value)
    if value.is_number and value.is_real:
        return N(value,label,tol=max(1e-9,abs(float(value))*1e-8))
    # Each distractor is provably different: nonconstant functions cannot equal
    # their negative or a constant vertical shift on an interval.
    ans=fmt(value)
    return C(ans,fmt(-value),fmt(value+1),label=label,why=why)

def add(number,*fields,group='Exercises',limited=False,why=''):
    matches=[q for q in QS.values() if q['number']==str(number) and q.get('subsection')==group]
    assert len(matches)==1,(number,group)
    q=matches[0]; assert q['id'] not in ROWS,q['id']
    assert len(set(f['label'] for f in fields))==len(fields),q['id']
    for i,f in enumerate(fields):
        f['provenance']='explicit-source-inspected-original-derivation'
        f.setdefault('explanation',why)
        if not f.get('explanation'):f['explanation']=why
        f['hint']='Use the exact source function and stated variable. Keep chain factors, signs, units, and domain restrictions.'
        if f['type']=='choice':
            random.Random(hashlib.sha256(f"{q['id']}/{i}".encode()).hexdigest()).shuffle(f['options'])
            f['selectionPrompt']='Choose the mathematical result for '+f['label']+'.'
    scope='Checks the numerical answers and mathematical selections shown. Freehand graphs, written proofs, and open-ended examples are not automatically assessed.'
    grader={**fields[0],'scope':scope} if len(fields)==1 else dict(type='parts',parts=list(fields),scope=scope)
    if limited:grader['complete']=False
    ROWS[q['id']]=dict(grader=grader,responsePartPrompt='Use the original textbook question above and answer each labeled check below.',objectiveChecksVerified=True,objectiveCheckVersion=2,objectiveFieldCount=len(fields),answerCheckSource=dict(book='Stewart, Calculus: Early Transcendentals, 8th edition',chapter=3,sourceSet=q['sourceSet'],exercise=q['number'],pdfPages=sorted({p['page'] for p in q['parts']}),authoringFile='scripts/calculus-answer-checks/chapter-03/review.py',review='Printed pages266–269 visually inspected; original symbolic derivations checked by finite differences and independent explicit regressions.'))

# Concept check: every actual requested derivative or rule has its own field.
rules=[('a · Power rule','d(x^r)/dx = r*x^(r−1)','d(x^r)/dx = x^(r−1)','d(x^r)/dx = r*x^r'),
('b · Constant multiple','(k*f)′ = k*f′ for constant k','(k*f)′ = k+f′','(k*f)′ = f′'),
('c · Sum rule','(f+g)′ = f′+g′','(f+g)′ = f′*g′','(f+g)′ = f+g'),
('d · Difference rule','(f−g)′ = f′−g′','(f−g)′ = f′+g′','(f−g)′ = f−g'),
('e · Product rule','(f*g)′ = f′*g+f*g′','(f*g)′ = f′*g′','(f*g)′ = f′+g′'),
('f · Quotient rule','(f/g)′ = (f′*g−f*g′)/g², g≠0','(f/g)′ = f′/g′','(f/g)′ = (f*g′−f′*g)/g²'),
('g · Chain rule','(f(g(x)))′ = f′(g(x))*g′(x)','(f(g(x)))′ = f′(x)*g′(x)','(f(g(x)))′ = f′(g(x))')]
add(1,*[C(ans,w1,w2,label=label) for label,ans,w1,w2 in rules],group='Concept Check',limited=True)
derivatives=[n*x**(n-1),S.exp(x),b**x*S.log(b),1/x,1/(x*S.log(b)),S.cos(x),-S.sin(x),S.sec(x)**2,-S.csc(x)*S.cot(x),S.sec(x)*S.tan(x),-S.csc(x)**2,1/S.sqrt(1-x*x),-1/S.sqrt(1-x*x),1/(1+x*x),S.cosh(x),S.sinh(x),1/S.cosh(x)**2,1/S.sqrt(1+x*x),1/S.sqrt(x*x-1),1/(1-x*x)]
names=['x^n','e^x','b^x','ln(x)','log_b(x)','sin(x)','cos(x)','tan(x)','csc(x)','sec(x)','cot(x)','arcsin(x)','arccos(x)','arctan(x)','sinh(x)','cosh(x)','tanh(x)','arcsinh(x)','arccosh(x)','arctanh(x)']
add(2,*[F(v,chr(97+i)+' · '+names[i]) for i,v in enumerate(derivatives)],group='Concept Check',why='Use real derivative domains: ln/log require x>0, base b>0 and b≠1; inverse circular derivatives require |x|<1, arccosh requires x>1, and arctanh requires |x|<1.')
add(3,C('The base e is the number for which lim[h→0](e^h−1)/h=1','e is the number whose square is 2','e is exactly 2.7',label='a · definition'),C('e=lim[n→∞](1+1/n)^n','e=lim[n→∞](1+1/n)','e=lim[n→∞]n^(1/n)',label='b · limit'),C('(e^x)′=e^x; there is no extra base-dependent factor','Every exponential has derivative e^x','e^x has constant derivative 1',label='c · natural exponential'),C('(ln x)′=1/x; there is no factor 1/ln b','Every logarithm has derivative 1/x','ln x has derivative x',label='d · natural logarithm'),group='Concept Check',limited=True)
add(4,C('Differentiate both sides with respect to x, treating y as y(x), then solve for y′','Treat y as a constant in every term','Differentiate only terms containing x and discard the rest',label='a · implicit differentiation'),C('Take a logarithm (or ln|y| where needed), differentiate, then multiply by y','Replace every power by its exponent without differentiating','Take ln of each summand separately',label='b · logarithmic differentiation'),group='Concept Check',limited=True)
add(5,C('ds/dt is velocity; dN/dt is population growth; dC/dq is marginal cost','ds/dt is always acceleration and dC/dq is total cost','A derivative is the total amount accumulated over all past time',label='Valid rate interpretations'),group='Concept Check',limited=True)
add(6,C('dP/dt=kP','dP/dt=k','dP/dt=P+k',label='a · growth equation'),C('Per-capita growth rate is approximately constant and resources are effectively unlimited','The population increases by a fixed number each year','Resources must be exhausted immediately',label='b · model conditions'),C('P(t)=P(0)*e^(kt)','P(t)=P(0)+kt','P(t)=k*t²',label='c · solution family'),group='Concept Check',limited=True)
add(7,C('L(x)=f(a)+f′(a)(x−a)','L(x)=f′(a)+f(a)(x−a)','L(x)=f(a)*x',label='a · linearization'),C('dy=f′(x)dx','dy=f(x)dx','dy=dx/f′(x)',label='b · differential'),C('Δy is the actual curve rise; dy is the tangent-line rise over the same dx=Δx','dy and Δy are always equal for nonlinear functions','dy is the horizontal change and Δy is the tangent slope',label='c · geometric meanings'),group='Concept Check',limited=True)

truths=[True,False,True,True,False,False,False,False,True,False,True,True,True,False,True]
tfwhy=['Sum rule.','The product rule has two terms.','Chain rule.','Chain rule where f(x)>0 so the displayed denominator and real derivative exist.','The numerator must be f′(sqrt(x)).','e² is constant, so its derivative is0.','The derivative is10^x ln10.','ln10 is constant, so its derivative is0.','sec²x−tan²x=1 on their common domain.','Absolute-value differentiation depends on the sign of x²+x; it is not |2x+1|.','Termwise power differentiation preserves polynomials.','The polynomial has degree30.','Quotient-rule expressions remain rational where defined.','A line must have a constant slope; here slope at−2 is−4.','The limit is g′(2)=5*2⁴=80.']
for i,v in enumerate(truths,1):add(i,C('True' if v else 'False','False' if v else 'True',label='Truth value',why=tfwhy[i-1]),group='True-False Quiz',limited=True)

# Exercises1–50: exact source functions, including radical nesting and variables.
functions={1:((x*x+x**3)**4,x),2:(x**(-S.Rational(1,2))-x**(-S.Rational(3,5)),x),3:((x*x-x+2)/S.sqrt(x),x),4:(S.tan(x)/(1+S.cos(x)),x),5:(x*x*S.sin(S.pi*x),x),6:(x*S.acos(x),x),7:((t**4-1)/(t**4+1),t),9:(S.log(x*S.log(x)),x),10:(S.exp(m*x)*S.cos(n*x),x),11:(S.sqrt(x)*S.cos(S.sqrt(x)),x),12:(S.asin(2*x)**2,x),13:(S.exp(1/x)/x**2,x),14:(S.log(S.sec(x)),x),16:(((u-1)/(u*u+u+1))**4,u),17:(S.sqrt(S.atan(x)),x),18:(S.cot(S.csc(x)),x),19:(S.tan(t/(1+t*t)),t),20:(S.exp(x*S.sec(x)),x),21:(3**(x*S.log(x)),x),22:(S.sec(1+x*x),x),23:((1-1/x)**-1,x),24:((x+S.sqrt(x))**(-S.Rational(1,3)),x),26:(S.sqrt(S.sin(S.sqrt(x))),x),27:(S.log(1+2*x)/S.log(5),x),28:(S.cos(x)**x,x),29:(S.log(S.sin(x))-S.sin(x)**2/2,x),30:((x*x+1)**4/((2*x+1)**3*(3*x-1)**5),x),31:(x*S.atan(4*x),x),32:(S.exp(S.cos(x))+S.cos(S.exp(x)),x),33:(S.log(S.sec(5*x)+S.tan(5*x)),x),34:(10**S.tan(S.pi*theta),theta),35:(S.cot(3*x*x+5),x),36:(S.sqrt(t*S.log(t**4)),t),37:(S.sin(S.tan(S.sqrt(1+x**3))),x),38:(S.atan(S.asin(S.sqrt(x))),x),39:(S.tan(S.sin(theta))**2,theta),41:(S.sqrt(x+1)*(2-x)**5/(x+3)**7,x),42:((x+lam)**4/(x**4+lam**4),x),43:(x*S.sinh(x*x),x),44:(S.sin(m*x)/x,x),45:(S.log(S.cosh(3*x)),x),46:(S.log((x*x-4)/(2*x+5)),x),47:(S.acosh(S.sinh(x)),x),48:(x*S.atanh(S.sqrt(x)),x),49:(S.cos(S.exp(S.sqrt(S.tan(3*x)))),x),50:(S.sin(S.cos(S.sqrt(S.sin(S.pi*x))))**2,x)}
derivative_rules={}
for num,(expr,var) in functions.items():
    derivative=S.diff(expr,var)
    if num==33:derivative=5*S.sec(5*x)
    if num==46:derivative=2*x/(x*x-4)-2/(2*x+5)
    derivative_rules[num]=derivative
    add(num,F(derivative),why='Differentiate with respect to '+str(var)+'. The result is valid where the original function and the real derivative are defined; do not cancel original domain exclusions.')
for num,eq in {8:x*S.exp(y)-y*S.sin(x),15:y+x*S.cos(y)-x*x*y,25:S.sin(x*y)-x*x+y,40:x*S.exp(y)-y+1}.items():
    result=S.simplify(-S.diff(eq,x)/S.diff(eq,y))
    add(num,F(result,'dy/dx'),why='Implicitly differentiate F(x,y)=0: F_x+F_y*y′=0. Solve only where F_y≠0.')

add(51,N(-S.Rational(4,27),'f″(2)'))
add(52,N(S.sqrt(3)-S.pi/12,'g″(π/6)'))
add(53,F(-5*x**4/y**11,'y″'),why='y′=−x⁵/y⁵. Differentiate again and use x⁶+y⁶=1 to simplify; requires y≠0.')
add(54,C('f^(n)(x)=n!/(2−x)^(n+1), x≠2','f^(n)(x)=(−1)^n*n!/(2−x)^(n+1)','f^(n)(x)=n!/(2−x)^n',label='nth derivative'))
add(55,C('Base n=0 holds; differentiating (x+n)e^x gives (x+n+1)e^x','Differentiate only e^x and keep x+n unchanged','The formula is true because every derivative is e^x',label='Induction step'),limited=True)
add(56,N(S.Rational(1,8),'Limit'))
add(57,F(1+2*S.sqrt(3)*(x-S.pi/6),'Tangent line y'))
add(58,C('y=−1','y=x−1','y=1',label='Tangent line'))
add(59,C('y=1+2x','y=1+x','y=2−x',label='Tangent line'))
add(60,C('y−1=−(4/5)(x−2)','y−1=(4/5)(x−2)','y−1=−(5/4)(x−2)',label='Tangent line'),C('y−1=(5/4)(x−2)','y−1=−(5/4)(x−2)','y−1=(4/5)(x−2)',label='Normal line'))
add(61,C('y=2−x','y=2+x','y=−2x',label='Tangent line'),C('y=2+x','y=2−x','y=2+2x',label='Normal line'))
add(62,F(S.exp(S.sin(x))*(1+x*S.cos(x)),'Derivative'),C('f′ has the sign of 1+x*cos(x); its zeros are horizontal tangents of f','f′ equals f at every x','f is increasing wherever f is positive',label='Graph comparison'),limited=True)
add(63,F((10-3*x)/(2*S.sqrt(5-x)),'a · derivative'),C('y−2=(7/4)(x−1)','y−2=(4/7)(x−1)','y−2=2(x−1)',label='b · tangent at (1,2)'),C('y−4=−(x−4)','y−4=x−4','y−4=−2(x−4)',label='b · tangent at (4,4)'),C('Slope is zero at x=10/3; it is positive before and negative after, for x<5','Slope is positive for every x<5','Slope is zero at x=5',label='c/d · graph check'),limited=True)
add(64,F(4-S.sec(x)**2,'a · f′'),F(-2*S.sec(x)**2*S.tan(x),'a · f″'),C('On (−π/2,π/2), f′ is even and f″ is odd; f″ changes from positive to negative at0','f′ is odd and f″ is even','f″ is positive on the entire interval',label='b · graph consistency'),limited=True)
add(65,C('(π/4,√2) and (5π/4,−√2)','(π/2,1) and (3π/2,−1)','(0,1) and (π,−1)',label='Horizontal-tangent points'))
add(66,C('(−√6/3,√6/6) and (√6/3,−√6/6)','(√6/3,√6/6) and (−√6/3,−√6/6)','(0,1/√2) and (0,−1/√2)',label='Slope-1 points'))
add(67,C('Apply the product rule then divide each term by (x−a)(x−b)(x−c), away from roots','Apply a quotient rule at every root','The identity holds at x=a,b,c without any domain condition',label='Derivation'),limited=True)
add(68,C('sin(2x)=2sin(x)cos(x)','sin(2x)=sin²x−cos²x','sin(2x)=sin(x)+cos(x)',label='a · sine double-angle'),C('cos(x+a)=cos(x)cos(a)−sin(x)sin(a)','cos(x+a)=cos(x)cos(a)+sin(x)sin(a)','cos(x+a)=cos(x)+cos(a)',label='b · cosine addition'),limited=True)
add(69,N(4,'a'),N(6,'b'),N(S.Rational(7,9),'c'),N(12,'d'))
# Image: f(2)=1,f′(2)=−1; g(2)=4,g′(2)=2; g(2)=4,f′(4)=3.
add(70,N(-2,'a · P′(2)'),N(-S.Rational(3,8),'b · Q′(2)'),N(6,'c · C′(2)'))
general=[('2*x*g(x)+x²*g′(x)','x²*g′(x)','2*x*g′(x)'),('2*x*g′(x²)','g′(x²)','2*x*g′(x)'),('2*g(x)*g′(x)','2*g′(x)','[g′(x)]²'),('g′(g(x))*g′(x)','[g′(x)]²','g′(g(x))'),('g′(e^x)*e^x','g′(e^x)','g′(x)*e^x'),('e^(g(x))*g′(x)','e^(g′(x))','e^x*g′(x)'),('g′(x)/g(x), g(x)≠0','1/g(x)','g′(x)/|g(x)|'),('g′(ln x)/x, x>0','g′(ln x)','g′(x)/x')]
for num,(ans,w1,w2) in enumerate(general,71):add(num,C(ans,w1,w2,label='f′(x)'))
add(79,C('(f′(x)*g(x)²+f(x)²*g′(x))/(f(x)+g(x))²','(f′(x)*g(x)−f(x)*g′(x))/(f(x)+g(x))²','f′(x)*g′(x)/(f′(x)+g′(x))',label='h′(x)'))
add(80,C('(f′(x)*g(x)−f(x)*g′(x))/(2*g(x)²*sqrt(f(x)/g(x)))','(f′(x)*g(x)+f(x)*g′(x))/(2*g(x)²*sqrt(f(x)/g(x)))','sqrt(f′(x)/g′(x))',label='h′(x)'),why='This derivative expression requires g(x)≠0 and f(x)/g(x)>0.')
add(81,C('4*cos(4x)*g′(sin(4x))*f′(g(sin(4x)))','f′(g(sin(4x)))*g′(sin(4x))','4*sin(4x)*g′(sin(4x))*f′(g(sin(4x)))',label='h′(x)'))
add(82,C('On[0,8], f oscillates about y=x and passes through the origin','f is y=x−2 everywhere','f is bounded between−2 and2',label='a · graph feature'),C('[2,3]','[1,2]','The rates are equal',label='b · larger average rate'),C('x=2','x=5','The rates are equal',label='c · larger instantaneous rate'),F(1-2*S.cos(x),'d · derivative'),N(1-2*math.cos(2),'d · f′(2)'),N(1-2*math.cos(5),'d · f′(5)'),limited=True)
add(83,N(-3,'x-coordinate'),N(0,'y-coordinate'))
add(84,C('y=(1/4)(x+ln4+1)','y=4x+4','y=(1/4)(x−ln4−1)',label='a · parallel tangent'),C('y=e*x','y=x','y=e*(x−1)',label='b · tangent through origin'))
add(85,N(-S.Rational(2,3),'a'),N(S.Rational(14,3),'b'),N(0,'c'))
add(86,N(0,'a · long-time concentration'),C('C′(t)=K*(−a*e^(−at)+b*e^(−bt))','C′(t)=K*(a*e^(−at)−b*e^(−bt))','C′(t)=K*(e^(−at)−e^(−bt))',label='b · concentration rate'),C('t=ln(b/a)/(b−a)','t=ln(a/b)/(b−a)','t=ln(b/a)/(a+b)',label='c · zero-rate time'),limited=True)
add(87,C('v=−A*e^(−ct)*(c*cos(ωt+δ)+ω*sin(ωt+δ))','v=A*e^(−ct)*(c*cos(ωt+δ)+ω*sin(ωt+δ))','v=−A*ω*e^(−ct)*sin(ωt+δ)',label='Velocity'),C('a=A*e^(−ct)*((c²−ω²)*cos(ωt+δ)+2cω*sin(ωt+δ))','a=A*e^(−ct)*((c²+ω²)*cos(ωt+δ)−2cω*sin(ωt+δ))','a=−A*ω²*e^(−ct)*cos(ωt+δ)',label='Acceleration'))
add(88,C('v=c²*t/sqrt(b²+c²*t²)','v=c*t/sqrt(b²+c²*t²)','v=sqrt(b²+c²*t²)',label='a · velocity'),C('a=b²*c²/(b²+c²*t²)^(3/2)','a=−b²*c²/(b²+c²*t²)^(3/2)','a=c²/sqrt(b²+c²*t²)',label='a · acceleration'),C('v(0)=0 and v(t)>0 for t>0 because b,c>0','v is negative for every t≥0','v is positive at t=0 as well',label='b · direction'),limited=True)
add(89,C('v=3t²−12','v=t³−12t+3','v=3t²+12',label='a · velocity'),C('a=6t','a=3t²','a=6',label='a · acceleration'),C('Upward for t>2; downward for0≤t<2; stationary at2','Upward for0<t<2; downward for t>2','Always upward',label='b · direction'),N(23,'c · total distance'),C('Position decreases to y(2)=−13 then increases; velocity crosses0 at2; acceleration=6t','Position increases throughout[0,3]','Acceleration crosses0 at2',label='d · graph features'),C('Speeds up for t>2; slows down for0<t<2','Speeds up for0<t<2; slows down for t>2','Always speeds up',label='e · speed change'),limited=True)
add(90,C('dV/dh=πr²/3','dV/dh=πr²h','dV/dh=2πrh/3',label='a · fixed radius'),C('dV/dr=2πrh/3','dV/dr=πr²/3','dV/dr=πrh/3',label='b · fixed height'))
add(91,N(4,'Linear density','kg/m'))
cost=lambda q:920+2*q-.02*q*q+.00007*q**3
add(92,C('C′(x)=2−0.04x+0.00021x²','C′(x)=2−0.02x+0.00007x²','C′(x)=920+2x−0.02x²',label='a · marginal cost'),N(.1,'b · C′(100)','dollars/item'),C('About$0.10 for one additional item near100items','Total cost of100items is$0.10','The 100th item costs exactly$0.10',label='b · interpretation'),N(cost(101)-cost(100),'c · exact101st-item cost','dollars',1e-7),limited=True)
growth=2*math.log(1.8);pop=200*1.8**8
add(93,C('P(t)=200*e^(2ln(1.8)*t), t in hours','P(t)=200*e^(ln(1.8)*t)','P(t)=200+320t',label='a · population model'),N(pop,'b · after4hours','cells',.51),N(growth*pop,'c · growth at4hours','cells/hour',.51),N(math.log(50)/growth,'d · time to10000','hours',.00051))
add(94,N(100*2**(-20/5.24),'a · remaining mass','mg',.00051),N(5.24*math.log2(100),'b · time to1mg','years',.0051))
add(95,C('C(t)=C₀*e^(−kt)','C(t)=C₀−kt','C(t)=C₀*e^(kt)',label='a · concentration'),N(30*math.log2(10),'b · time to eliminate90%','hours',.0051))
add(96,N(20+60*(2/3)**2,'a · temperature at1hour','°C',.0051),N(.5*math.log(1/3)/math.log(2/3),'b · time from start to40°C','hours',.00051))
add(97,N(S.Rational(4,3),'Surface area rate','cm²/min',.00051))
add(98,N(8/(9*S.pi),'Water depth rate','cm/s',.00051))
add(99,N(13,'Separation rate','ft/s'))
add(100,N(120/S.sqrt(241),'Vertical velocity','ft/s',.00051))
add(101,N(400,'Shadow length rate','ft/hour'))
add(102,C('L(x)=4−(3/4)(x−3)','L(x)=4+(3/4)(x−3)','L(x)=5−(3/4)x',label='a · linear approximation'),C('The tangent lies above the upper semicircle near x=3','The tangent lies below the curve near x=3','The tangent crosses the curve twice near x=3',label='b · graph comparison'),N((369-16*math.sqrt(31))/125,'c · lower x endpoint',tol=.00051),N((369+16*math.sqrt(31))/125,'c · upper x endpoint',tol=.00051),limited=True)
# Solve |(1+x)−cuberoot(1+3x)|=.1 with real cube roots; the small negative
# island around−3 is part of the source's unrestricted real-domain question.
z=S.symbols('z',real=True)
roots_plus=sorted(float(S.re(r)) for r in S.nroots((z-S.Rational(1,10))**3-(3*z-2)) if abs(float(S.im(r)))<1e-10)
roots_minus=sorted(float(S.re(r)) for r in S.nroots((z+S.Rational(1,10))**3-(3*z-2)) if abs(float(S.im(r)))<1e-10)
ends=sorted([r-1 for r in roots_plus+roots_minus])
segments=[]
for lo,hi in zip(ends,ends[1:]):
    mid=(lo+hi)/2
    if abs(1+mid-math.cbrt(1+3*mid))<.1:segments.append((lo,hi))
assert len(segments)==2,segments
interval_text=' or '.join(f'{lo:.6f}<x<{hi:.6f}' for lo,hi in segments)
add(103,C('L(x)=1+x; cuberoot(1+3x)≈1+x','L(x)=1+3x; cuberoot(1+3x)≈1+3x','L(x)=1+x/3',label='a · linearization'),N(1.01,'a · estimate cuberoot(1.03)',tol=.00001),C(interval_text,'−0.1<x<0.1 only','Every real x',label='b · full real accuracy set',why='Use the real cube root. The full real-domain inequality has a small second interval near x=−3 as well as the interval containing0.'),limited=True)
add(104,N(.8,'dy'))
add(105,N(12+1.5*S.pi,'Maximum area error','cm²',.00051))
add(106,C('Derivative of f(x)=x^17 at x=1','Derivative of f(x)=x^16 at x=1','Derivative of f(x)=17x at x=0',label='Derivative identification'),N(17,'Limit'))
add(107,C('Derivative of f(x)=x^(1/4) at x=16','Derivative of f(x)=x^4 at x=16','Derivative of f(x)=sqrt(x) at x=16',label='Derivative identification'),N(S.Rational(1,32),'Limit'))
add(108,C('Derivative of cosθ at θ=π/3','Derivative of sinθ at θ=π/3','Derivative of cosθ at θ=0',label='Derivative identification'),N(-S.sqrt(3)/2,'Limit'))
add(109,N(S.Rational(1,4),'Limit'),why='Rationalize the numerator; tan x−sin x~x³/2 and the sum of radicals tends to2.')
add(110,C('Differentiate f(g(x))=x to get f′(g(x))*g′(x)=1; substitute f(g(x))=x','Differentiate to obtain f′(x)*g′(x)=x','Replace f′(g(x)) by1+g(x)²',label='Proof step'),C('g′(x)=1/(1+x²)','g′(x)=1+x²','g′(x)=1/(1+g(x)²)',label='Result'),limited=True)
add(111,F(x*x/8,'f′(x)'),why='2f′(2x)=x². Substitute u=2x, then f′(u)=u²/8.')
add(112,C('The intercept segment has length a (for a>0, at regular points with two finite intercepts)','Its length is a²','Its length depends on the point of tangency',label='Constant length'),C('Parameterize x=a*cos³t, y=a*sin³t; tangent intercepts are a*cos(t),a*sin(t)','Every tangent has slope1','The x and y intercepts are both a at every point',label='Derivation'),limited=True)

def verify():
    mp.mp.dps=45; tests=0
    # High-precision central finite differences, independently of SymPy.diff.
    substitutions={m:S.Rational(2,5),n:S.Rational(7,10),lam:S.Rational(6,5)}
    for num,(expr,var) in functions.items():
        f=S.lambdify(var,expr.subs(substitutions),'mpmath')
        d=S.lambdify(var,derivative_rules[num].subs(substitutions),'mpmath')
        checked=0
        for val in ['-0.7','-0.2','0.08','0.2','0.4','0.7','1.1','1.4','2.2','3.2']:
            try:
                at=mp.mpf(val);h=mp.mpf('1e-14');fv=f(at);expected=d(at)
                if abs(mp.im(fv))>mp.mpf('1e-20') or abs(mp.im(expected))>mp.mpf('1e-20'):continue
                fd=(f(at+h)-f(at-h))/(2*h)
                assert abs(fd-expected)<mp.mpf('1e-17')*max(1,abs(expected)),(num,val,fd,expected)
                checked+=1;tests+=1
            except (ValueError,ZeroDivisionError,TypeError):continue
        assert checked,(num,'no real finite sample')
    assert S.simplify(S.diff(S.sqrt(4*t+1),t,2).subs(t,2)+S.Rational(4,27))==0;tests+=1
    assert S.simplify(S.diff(theta*S.sin(theta),theta,2).subs(theta,S.pi/6)-(S.sqrt(3)-S.pi/12))==0;tests+=1
    assert S.limit((S.sqrt(1+S.tan(x))-S.sqrt(1+S.sin(x)))/x**3,x,0)==S.Rational(1,4);tests+=1
    assert cost(101)-cost(100)>0 and abs(cost(101)-cost(100)-.10107)<1e-8;tests+=1
    assert abs((45*15+60*5)/75-13)<1e-12;tests+=1
    for lo,hi in segments:
        assert abs(1+(lo+hi)/2-math.cbrt(1+3*(lo+hi)/2))<.1
        assert abs(abs(1+lo-math.cbrt(1+3*lo))-.1)<1e-9
        assert abs(abs(1+hi-math.cbrt(1+3*hi))-.1)<1e-9;tests+=3
    for edge in [(369-16*math.sqrt(31))/125,(369+16*math.sqrt(31))/125]:
        assert abs(4-.75*(edge-3)-math.sqrt(25-edge**2)-.1)<1e-10;tests+=1
    assert set(ROWS)==set(QS),(set(QS)-set(ROWS),set(ROWS)-set(QS))
    return tests

if __name__=='__main__':
    tests=verify()
    here=Path(__file__).parent
    (here/'review.json').write_text(json.dumps({'questions':ROWS},ensure_ascii=False,indent=2)+'\n')
    (here/'review-audit.json').write_text(json.dumps(dict(questions=len(ROWS),fields=sum(v['objectiveFieldCount'] for v in ROWS.values()),independentMathChecks=tests,source=dict(file='site/books/calculus/chapter-03.pdf',sha256=hashlib.sha256((ROOT/'site/books/calculus/chapter-03.pdf').read_bytes()).hexdigest(),localPages=[96,97,98,99],printedPages=[266,267,268,269],globalPages=[298,299,300,301]),notes=['Graph70 visually read with grid; g(2)=4,g′(2)=2,f(2)=1,f′(2)=−1,f′(4)=3.','Exercise103 includes both real-domain accuracy intervals; real cube-root branch retained.','Recognition checks do not assess hand-drawn graphs or complete written proofs.']),indent=2)+'\n')
    print(f'PASS Chapter3 review: {len(ROWS)} questions, {sum(v["objectiveFieldCount"] for v in ROWS.values())} fields; {tests} independent mathematical checks.')
