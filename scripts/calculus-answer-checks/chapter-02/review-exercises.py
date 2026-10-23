#!/usr/bin/env python3
"""Original source-reviewed answer contracts for all 54 Chapter 2 review exercises."""
import gzip,hashlib,json,math,random
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parents[3]
qs=json.loads(gzip.decompress((ROOT/'site/questions/calculus.json.gz').read_bytes()))
QS={q['id']:q for q in qs if q['chapter']==2 and q['sourceSet']=='chapter-02-review' and q['subsection']=='Exercises'}
ROWS={}
def N(v,label='Your answer',unit='',tol=1e-8):return dict(type='numeric',answer=float(v),label=label,unit=unit,tolerance=tol)
def C(ans,*wrong,label='Your answer',why=''):
 assert wrong and ans not in wrong and len(set(wrong))==len(wrong)
 return dict(type='choice',answer=ans,options=[ans,*wrong],label=label,explanation=why)
def I(sign=1,label='Limit'):return C('Positive infinity' if sign>0 else 'Negative infinity','Negative infinity' if sign>0 else 'Positive infinity','0',label=label)
def D(label='Limit'):return C('Does not exist','0','Positive infinity','Negative infinity',label=label)
def add(n,*fields,limited=False,why=''):
 q=QS['calculus-chapter-02-review-'+str(n)];assert q['id'] not in ROWS
 assert len(set(f['label'] for f in fields))==len(fields),(n,fields)
 for i,f in enumerate(fields):
  f['provenance']='explicit-source-inspected-original-derivation'
  if not f.get('explanation'):f['explanation']=why
  f['hint']='Use the original source question, side of approach, shared instructions and graph scale. Keep domain and units in view.'
  if f['type']=='choice':
   random.Random(hashlib.sha256(f"{q['id']}/{i}".encode()).hexdigest()).shuffle(f['options']);f['selectionPrompt']='Choose the mathematical result for '+f['label']+'.'
 scope='Checks the numerical answers and mathematical selections shown. Freehand graphs and written proofs/explanations are not automatically assessed.'
 grader={**fields[0],'scope':scope} if len(fields)==1 else dict(type='parts',parts=list(fields),scope=scope)
 if limited:grader['complete']=False
 ROWS[q['id']]=dict(grader=grader,responsePartPrompt='Use the original textbook exercise above and answer each labeled check below.',objectiveCheckVersion=2,objectiveChecksVerified=True,objectiveFieldCount=len(fields),answerCheckSource=dict(book='Stewart, Calculus: Early Transcendentals, 8th edition',chapter=2,sourceSet=q['sourceSet'],exercise=q['number'],pdfPages=sorted({p['page'] for p in q['parts']}),authoringFile='scripts/calculus-answer-checks/chapter-02/review-exercises.py',review='Printed pages166–168 visually inspected, including graphs; limits and rates independently calculated. Approximate graph readings have explicit tolerances.'))

add(1,N(3,'a(i)'),N(0,'a(ii)'),D('a(iii)'),N(2,'a(iv)'),I(1,'a(v)'),I(-1,'a(vi)'),N(4,'a(vii)'),N(-1,'a(viii)'),C('y=4 and y=−1','y=3 and y=−2','y=0 only',label='b · horizontal asymptotes'),C('x=0 and x=2','x=−3 and x=4','x=0 only',label='c · vertical asymptotes'),C('x=−3,0,2,4','x=0,2 only','x=−3,4 only',label='d · discontinuities'),limited=True)
add(2,C('Left tail tends to y=−2; right tail tends to y=0','Both tails tend to0','Left tail tends to0; right tail tends to−2',label='Tail behavior'),C('Both sides at x=−3 rise without bound','Both sides at x=−3 tend to−2','Only the left side at x=−3 rises without bound',label='Behavior at−3'),C('At3 the left branch falls without bound; the right limit and f(3) both equal2','Both sides at3 fall without bound','f(3) must be undefined',label='Behavior at3'),limited=True)
x,h,t,u,r,v=S.symbols('x h t u r v',real=True)
limits={3:(S.exp(x**3-x),x,1,'+-'),4:((x*x-9)/(x*x+2*x-3),x,3,'+-'),5:((x*x-9)/(x*x+2*x-3),x,-3,'+-'),7:(((h-1)**3+1)/h,h,0,'+-'),8:((t*t-4)/(t**3-8),t,2,'+-'),10:((4-v)/S.Abs(4-v),v,4,'+'),11:((u**4-1)/(u**3+5*u*u-6*u),u,1,'+-'),12:((S.sqrt(x+6)-x)/(x**3-3*x*x),x,3,'+-'),13:(S.sqrt(x*x-9)/(2*x-6),x,S.oo,'-'),14:(S.sqrt(x*x-9)/(2*x-6),x,-S.oo,'+'),15:(S.log(S.sin(x)),x,S.pi,'-'),16:((1-2*x*x-x**4)/(5+x-3*x**4),x,-S.oo,'+'),17:(S.sqrt(x*x+4*x+1)-x,x,S.oo,'-'),18:(S.exp(x-x*x),x,S.oo,'-'),19:(S.atan(1/x),x,0,'+'),20:(1/(x-1)+1/(x*x-3*x+2),x,1,'+-')}
answers={3:1,4:0,5:S.Rational(3,2),7:3,8:S.Rational(1,3),10:-1,11:S.Rational(4,7),12:-S.Rational(5,54),13:S.Rational(1,2),14:-S.Rational(1,2),16:S.Rational(1,3),17:2,18:0,19:S.pi/2,20:-1}
for n,val in answers.items():add(n,N(val,'Limit'))
add(6,I(-1));add(9,I(1));add(15,I(-1))
add(21,C('Horizontal y=0; vertical x=0','Horizontal y=1; no vertical asymptote','Horizontal y=0; vertical x=π/2',label='Asymptotes'),C('0≤cos²x/x²≤1/x² for large |x|; near0, cos²x→1 and x²→0+','cos²x has limit0 as x→∞','The numerator is unbounded',label='Limit reasoning'),limited=True)
add(22,C('Horizontal y=1 as x→∞ and y=−1 as x→−∞; no vertical asymptote','Horizontal y=0 at both ends','Vertical x=0 only',label='Asymptotes'),C('Rationalize: numerator2x+1 divided by the sum of radicals; use |x| in the denominator limit','Replace sqrt(x²) by x at both infinities','Each radical has a finite limit separately',label='Limit reasoning'),limited=True)
add(23,N(1,'Limit'),why='Both bounding expressions tend to1; apply the squeeze theorem.')
add(24,N(0,'Limit'),C('−x²≤x²cos(1/x²)≤x², and both bounds tend to0','cos(1/x²) itself tends to0','x²cos(1/x²)=0 for every x≠0',label='Squeeze argument'),limited=True)
add(25,C('Choose δ=ε/5, so |(14−5x)−4|=5|x−2|<ε','Choose δ=5ε, which always gives error<ε','The definition requires x=2',label='Valid epsilon-delta choice'),limited=True)
add(26,C('Choose δ=ε³, since |cuberoot(x)|=|x|^(1/3)','Choose δ=ε^(1/3) for every ε>0','Choose δ=1 independently of ε',label='Valid epsilon-delta choice'),limited=True)
add(27,C('Choose δ=min(1,ε/2); |x−1|<2 and |x²−3x+2|=|x−2||x−1|','Choose δ=1 independently of ε','Use |x−1|<1 whenever |x−2|<1',label='Valid epsilon-delta proof'),limited=True)
add(28,C('For M>0 choose δ=4/M²; if0<x−4<δ then2/sqrt(x−4)>M','For M>0 choose δ=M²/4; this works for every M','The infinite limit means the function equals infinity at4',label='Valid one-sided infinite-limit proof'),limited=True)
add(29,N(3,'a(i)'),N(0,'a(ii)'),D('a(iii)'),N(0,'a(iv)'),N(0,'a(v)'),N(0,'a(vi)'),C('Discontinuous at0 and3','Discontinuous only at0','Discontinuous only at3',label='b · discontinuities'),C('At0: left branch ends open at(0,0), closed point(0,3); at3 both branches approach an unfilled(3,0)','At0 both branches meet at(0,0)','At3 the function is defined as0',label='c · graph features'),limited=True)
add(30,C('At2: continuous','At2: only left-continuous','At2: only right-continuous',label='a · x=2'),C('At3: continuous','At3: only left-continuous','At3: neither one-sided continuous',label='a · x=3'),C('At4: right-continuous, not left-continuous','At4: continuous','At4: left-continuous, not right-continuous',label='a · x=4'),C('The graph joins at(2,0),(3,−1), then has an open(4,0) and a closed(4,π)','There is a closed point(4,0) and open point(4,π)','The pieces fail to join at2 and3',label='b · graph'),limited=True)
add(31,C('Domain: all real numbers','Domain: x>0','Domain: x≠0',label='Domain'),C('sin, exp, and the identity are continuous; compositions and products preserve continuity','Every product is continuous even if its factors are not','The domain has an infinite discontinuity at0',label='Continuity reasoning'),limited=True)
add(32,C('Domain: (−∞,−3]∪[3,∞)','Domain: all real x except±sqrt(2)','Domain: (−3,3)',label='Domain'),C('The radicand is nonnegative there and the denominator is never0 there; composition and quotient laws apply','The square root is defined only when its radicand is positive, excluding±3','The denominator vanishes at±3',label='Continuity reasoning'),limited=True)
add(33,N(-2,'F(1)'),N(25,'F(2)'),C('A polynomial is continuous and the endpoint values have opposite signs, so IVT gives a zero in(1,2)','Endpoint signs alone guarantee a root without continuity','IVT proves the zero is unique',label='IVT justification'),limited=True)
add(34,N(2,'F(0)'),N(math.cos(1)-math.e+2,'F(1)'),C('cos(sqrt(x))−e^x+2 is continuous on[0,1] and changes sign','cos(sqrt(x)) is undefined throughout(0,1)','Both endpoint values are positive',label='IVT justification'),limited=True)
add(35,N(-8,'a · slope'),C('y−1=−8(x−2)','y−1=8(x−2)','y−1=−4(x−2)',label='b · tangent'))
add(36,C('At x=0: y=2+6x','At x=0: y=2−6x','At x=0: y=6+2x',label='Tangent at0'),C('At x=−1: y−1/2=(3/8)(x+1)','At x=−1: y−1/2=−(3/8)(x+1)','At x=−1: y−1/2=(3/2)(x+1)',label='Tangent at−1'))
add(37,N(3,'a(i) · [1,3]','m/s'),N(2.75,'a(ii) · [1,2]','m/s'),N(2.625,'a(iii) · [1,1.5]','m/s'),N(2.525,'a(iv) · [1,1.1]','m/s'),N(2.5,'b · v(1)','m/s'))
add(38,N(-.016,'a · pressure rate','psi/in³'),C('V(P)=800/P','V(P)=800P','V(P)=P/800',label='b · volume function'),C('dV/dP=−800/P², inversely proportional to P²','dV/dP=800/P²','dV/dP=−800/P',label='b · derivative'),limited=True)
add(39,N(10,'a · f′(2)'),C('y−4=10(x−2)','y−4=6(x−2)','y−4=10(x+2)',label='b · tangent'),C('The tangent passes through(2,4), and its slope matches the curve there','The tangent passes through the origin','The curve is linear everywhere',label='c · graph consistency'),limited=True)
add(40,C('One valid choice is f(x)=x^6, a=2','One valid choice is f(x)=x², a=6','One valid choice is f(x)=x^6, a=0',label='Function and point'),why='The numerator is f(2+h)−f(2), with f(2)=64. Equivalent translated functions are possible; this checks recognition of one valid pair.')
add(41,C('f′(r) is the rate of change of total repayment cost per percentage-point increase in annual interest rate','f′(r) is the total loan principal','f′(r) is the annual interest rate itself',label='a · meaning and units'),C('Near10%, raising the rate by1percentage point increases total repayment by about$1200','Raising the rate by1% of10% costs exactly$1200','The loan principal is$1200',label='b · f′(10)=1200'),C('Positive for the ordinary fixed-principal, fixed-payment-schedule loan model','Always negative for a loan','It must alternate signs as the rate increases',label='c · sign'),limited=True)
add(42,C('Derivative is positive before the single local maximum,0 there, and negative after it','Derivative has the same sign as f everywhere','Derivative is negative everywhere',label='Derivative graph behavior'),limited=True)
add(43,C('Derivative has signs +,−,+,− across the three stationary points from left to right','Derivative has signs−,+,−,+','Derivative has only one zero',label='Derivative graph behavior'),limited=True)
add(44,C('Derivative has signs−,+,−,+ before the corner; it is undefined at the corner and negative on the final straight segment','Derivative is defined and positive at the corner','Derivative has only one stationary zero',label='Derivative graph behavior'),limited=True)
add(45,C('f′(x)=−5/(2sqrt(3−5x))','f′(x)=5/(2sqrt(3−5x))','f′(x)=−5sqrt(3−5x)',label='a · derivative'),C('Domain of f: (−∞,3/5]','Domain of f: (−∞,3/5)','Domain of f: [3/5,∞)',label='b · f domain'),C('Domain of f′: (−∞,3/5)','Domain of f′: (−∞,3/5]','Domain of f′: (3/5,∞)',label='b · derivative domain'),C('f decreases to0 at3/5; its derivative is negative and tends to−∞ as x→(3/5)−','f increases to0 and f′>0','f′ tends to0 at3/5',label='c · graph comparison'),limited=True)
add(46,C('Vertical x=−3; horizontal y=−1','Vertical x=3; horizontal y=1','Vertical x=4; horizontal y=0',label='a · asymptotes'),C('f′(x)=−7/(x+3)²','f′(x)=7/(x+3)²','f′(x)=−1/(x+3)',label='c · derivative'),C('f′ is negative on both domain intervals, tends to−∞ near−3, and approaches0 at both infinities','f′ changes sign at−3','f′ is positive everywhere',label='b/d · derivative graph'),limited=True)
add(47,C('x=−4,−1,2,5','x=−4,−1,2 only','x=−1,0,2,4',label='Not differentiable'),C('−4 is discontinuous;−1 is a sharp point;2 is an infinite discontinuity;5 is a vertical tangent','All four are zeros of f','All four are ordinary horizontal tangents',label='Reasons'),limited=True)
add(48,C('f is a; f′ is c; f″ is b','f is a; f′ is b; f″ is c','f is c; f′ is a; f″ is b',label='Curve identification'),C('a rises then falls, so c changes from positive to negative; extrema of c match zeros of b','The derivative always has the same sign as the original','The second derivative must lie above the original',label='Reasoning'),limited=True)
add(49,C('A valid example is f(x)=e^x for x<0 and f(x)=x for x>0, undefined at0','A valid example is f(x)=1+e^x for x<0 and f(x)=x for x>0','A valid example is f(x)=−e^x for x<0 and f(x)=x for x>0',label='Valid graph/function'),C('Both branches increase; left limit at0 is1, right limit0; tail derivative limits are0 and1','The function must be continuous at0','The derivative is negative on the left branch',label='Condition check'),limited=True)
years=[1950,1960,1970,1980,1990,2000,2010];values=[31.1,35.7,34,28,25.7,25.7,24]
rates=[(values[1]-values[0])/10]+[(values[i+1]-values[i-1])/20 for i in range(1,6)]+[(values[-1]-values[-2])/10]
add(50,C('P′ is the annual change in the share under18, in percentage points per year','P′ is the number of children born per year','P′ is a percentage of the existing under18 share per year',label='a · meaning/units'),*[N(rate,'b · '+str(year)+' centered estimate' if 1950<year<2010 else 'b · '+str(year)+' one-sided estimate','percentage points/year',.00051) for year,rate in zip(years,rates)],C('P peaks around1960; the centered derivative estimates are negative from1970 onward','P increases monotonically from1950 to2010','Every estimated derivative is positive',label='c · graph comparison'),C('Use more frequent, reliable measurements to form shorter-interval differences','Use fewer census years','Replace percentages by cumulative population totals without adjustment',label='d · improving estimates'),limited=True)
add(51,N(.156,'Centered estimate of B′(2000)','billion bills/year',.013),C('Near2000 the count increases by about156million$20bills per year','The dollar value increases by156million dollars per year','The number of bills is156million in2000',label='Interpretation'),limited=True)
add(52,N(.1,'a · F′(1950)','children per woman/year',.035),N(-.18,'a · F′(1965)','children per woman/year',.065),N(.02,'a · F′(1987)','children per woman/year',.05),C('The fertility-rate curve rises near1950, drops near1965, and is nearly flat near1987 at this graph scale','The derivative is the number of women in each year','All three derivatives are negative',label='b · derivative meanings'),C('The baby boom, subsequent bust, and later boomlet provide historical context; the graph alone does not establish causes','The graph proves a single cause for every change','The derivative values are the total US birth counts',label='c · context'),limited=True)
add(53,N(0,'Limit'),why='0≤|f(x)|≤g(x) and g→0 force |f|→0, hence f→0.')
add(54,C('The limit exists at every real a and equals−1','The limit exists only at nonintegers','The limit exists only at integers',label='a · limit existence'),C('Discontinuous at every integer, and continuous at every noninteger','Continuous everywhere','Discontinuous at every noninteger',label='b · discontinuities'),why='floor(x)+floor(−x)=−1 for nonintegers and0 at integers; isolated point values do not change limits.')

def verify():
 tests=0
 for num,args in limits.items():
  expr,var,at,side=args
  value=S.limit(expr,var,at,dir=side)
  expected=answers.get(num,-S.oo if num==15 else None)
  assert S.simplify(value-expected)==0 if value not in [S.oo,-S.oo] else value==expected,(num,value,expected)
  tests+=1
 assert S.limit((x*x-9)/(x*x+2*x-3),x,1,dir='+')==-S.oo;tests+=1
 assert S.limit(S.sqrt(r)/(r-9)**4,r,9)==S.oo;tests+=1
 assert S.simplify(S.diff(2/(1-3*x),x).subs(x,-1)-S.Rational(3,8))==0;tests+=1
 assert S.simplify(S.diff((4-x)/(3+x),x)+7/(3+x)**2)==0;tests+=1
 for y,rate in zip(years,rates):assert math.isfinite(rate);tests+=1
 for k in range(-50,51):
  for z in [k,k+.1,k+.9]:assert math.floor(z)+math.floor(-z)==(0 if z==k else-1);tests+=1
 assert set(ROWS)==set(QS)
 return tests
if __name__=='__main__':
 tests=verify();here=Path(__file__).parent
 (here/'review-exercises.json').write_text(json.dumps({'questions':ROWS},ensure_ascii=False,indent=2)+'\n')
 (here/'review-exercises-audit.json').write_text(json.dumps(dict(questions=len(ROWS),fields=sum(v['objectiveFieldCount'] for v in ROWS.values()),independentMathChecks=tests,source=dict(file='site/books/calculus/chapter-02.pdf',sha256=hashlib.sha256((ROOT/'site/books/calculus/chapter-02.pdf').read_bytes()).hexdigest(),localPages=[90,91,92],printedPages=[166,167,168],globalPages=[198,199,200]),limitations=['Graph52 slopes are approximate and have explicit tolerances.','Freehand graphs and written arguments are not automatically assessed.','Table50 uses centered interior and one-sided endpoint differences; the response labels state this estimation convention.']),indent=2)+'\n')
 print(f'PASS Chapter2 review exercises: {len(ROWS)} questions, {sum(v["objectiveFieldCount"] for v in ROWS.values())} fields; {tests} independent mathematical checks.')
