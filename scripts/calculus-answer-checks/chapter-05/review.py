#!/usr/bin/env python3
"""100 Chapter5 review contracts, visually reviewed printed421–424."""
import json,hashlib,random,gzip
from pathlib import Path
import sympy as S
import mpmath as mp
mp.mp.dps=40
ROOT=Path(__file__).resolve().parents[3]
QS=[q for q in json.load(gzip.open(ROOT/'site/questions/calculus.json.gz')) if q['sourceSet']=='chapter-05-review']
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
 ROWS[q['id']]=dict(grader=g,responsePartPrompt='Answer each labeled check using the original textbook question above.',objectiveChecksVerified=True,objectiveCheckVersion=3,objectiveFieldCount=len(fs),answerCheckSource=dict(book='Stewart, Calculus: Early Transcendentals, 8e',chapter=5,pdfPages=sorted({p['page'] for p in q['parts']}),authoringFile='scripts/calculus-answer-checks/chapter-05/review.py'))
def cc(n,*fs):add(n,*fs,group='Concept Check',limited=True)
cc(1,C('Σ f(xᵢ*)Δxᵢ, with xᵢ* in subintervali and Δxᵢ its width','Σ f(xᵢ*) without widths','Σ f′(xᵢ*)Δxᵢ',label='a · Riemann sum'),C('Sum of rectangle areas approximating the area under f','Exact area for every partition','Area between f and its derivative',label='b · f≥0'),C('Signed rectangle sum: positive above and negative below the axis','All rectangles count positively','Negative rectangles are omitted',label='c · Signed f'))
cc(2,C('Integral=lim Σf(xᵢ*)Δxᵢ as maximum width tends to0','Integral=one arbitrary sample value','Integral=f(b)−f(a)',label='a · Definition'),C('Area below f and above the axis on[a,b]','Area between f and its derivative','Length of the graph',label='b · f≥0'),C('Area above the axis minus area below it','Total unsigned area','Area below minus area above',label='c · Signed interpretation'))
cc(3,C('Mₙ=Δx Σ[i=1..n]f(a+(i−1/2)Δx), Δx=(b−a)/n','Mₙ=Σf(a+iΔx)','Mₙ=Δx Σf(a+(i−1)Δx)',label='Midpoint Rule'))
cc(4,C('For continuous f, d/dx∫[a,x]f(t)dt=f(x)','d/dx∫[a,b]f(t)dt=f(x)','d/dx∫[a,x]f(t)dt=f′(x)',label='Part1'),C('∫[a,b]f(x)dx=F(b)−F(a) when F′=f','∫[a,b]f(x)dx=f(b)−f(a)','∫[a,b]f(x)dx=F(a)−F(b)',label='Part2'))
cc(5,C('∫[a,b]F′(x)dx=F(b)−F(a)','∫[a,b]F′(x)dx=F(a)+F(b)','The integral of a rate always gives the final total without an initial value',label='a · Net Change Theorem'),C('Water volume added from t₁ to t₂ (signed net inflow if r is signed)','Water flow rate at t₂','Mean water depth',label='b · Inflow integral'))
cc(6,C('Displacement between60s and120s, in feet','Total distance regardless of direction','Change in velocity',label='a · Integral of velocity'),C('Total distance traveled between60s and120s, in feet','Signed displacement','Final speed',label='b · Integral of speed'),C('Change in velocity v(120)−v(60), in ft/s','Total distance','Final position',label='c · Integral of acceleration'))
cc(7,C('The family F+C of antiderivatives with F′=f on an interval','A single definite number','Only the area above the axis',label='a · Indefinite integral'),C('Choose any antiderivative F; definite integral=F(b)−F(a)','Add arbitraryC to every definite integral','The definite integral is always positive',label='b · Connection'))
cc(8,C('Differentiating an accumulation integral recovers f; integrating f′ recovers f up to an additive constant','Differentiating and integrating always give exactly the original function with no constant','The two operations are unrelated',label='Inverse processes'))
cc(9,C('Set u=g(x), du=g′(x)dx; ∫f(g(x))g′(x)dx=∫f(u)du. Transform definite bounds too.','Change x to u but keep dx and both bounds unchanged','Substitute a convenient symbol without the derivative factor',label='Substitution Rule'))
truth=[True,False,True,False,False,True,True,False,True,True,False,True,True,False,False,False,False,False]
reasons=['Linearity.','Products of integrals do not generally equal the integral of a product.','Constant-multiple rule.','The variable x cannot be factored out as a constant.','For f=1 on[0,4], left=4 and right=2.','FTC2.','Order is preserved by integration on an ordered interval.','Pointwise order of functions does not order their derivatives.','The integrand is odd on[−1,1].','The bx term is odd and the remaining terms are even.','|x| is continuous but not differentiable at0.','FTC1 constructs an antiderivative for every continuous function.','Integral additivity with oriented endpoints.','f(x)=x−1/2 has zero integral without being identicallyzero.','Both integration limits are constants; the derivative is0.','The function is negative for1<x≤2, so the integral is signed area.','The singularity at0 makes the improper integral diverge; a formal primitive evaluation across it is invalid.','A bounded jump discontinuity can still be Riemann integrable.']
for i,(v,why) in enumerate(zip(truth,reasons),1):add(i,C(str(v),'False' if v else 'True',label='Truth value'),group='True-False Quiz',why=why,limited=True)
# Graph readings: source integer/half-integer grid, not exact analytic functions.
add(1,N(8,'a · Left-endpoint sum',tol=.6),N(5.2,'b · Midpoint sum',tol=.7),limited=True,why='Six width1 strips; graph estimates at integer or half-integer x. The sum is signed rectangle area.')
add(2,N(S.Rational(5,4),'a · Right sum n=4'),N(S.Rational(2,3),'b · Integral by definition'),N(S.Rational(2,3),'c · FTC check'),C('Positive area on[1,2] minus negative area magnitude on[0,1]','All area is counted positive','Only area on[1,2] contributes',label='d · Geometry'),limited=True)
add(3,F(S.Rational(1,2)+pi/4),why='Triangle area1/2 plus unit quarter-circle areaπ/4.')
add(4,C('∫[0,π]sin(x)dx','∫[0,π]cos(x)dx','∫[0,1]sin(x)dx',label='Definite integral'),N(2,'Value'))
add(5,N(3))
add(6,C('lim[n→∞](4/n)Σ[i=1..n][1+4i/n+2(1+4i/n)^5]','lim[n→∞](1/n)Σ[i=1..n](i/n+2(i/n)^5)','lim[n→∞]Σ[i=1..n](1+4i/n)',label='a · Right-sum limit'),N(5220,'a · Limit value'),N(5220,'b · FTC value'))
add(7,C('f=c, f′=b, and∫[0,x]f(t)dt=a','f=a, f′=b, and integral=c','f=b, f′=c, and integral=a',label='Graph identification'),limited=True,why='a vanishes at0 and has slopes matching c; the slopes of c match b.')
add(8,F(S.exp(pi/4)-1,'a · Integral of derivative'),N(0,'b · Derivative of fixed-bound integral'),F(S.exp(S.atan(x)),'c · Accumulation derivative'))
add(9,N(3,'g(4)'),N(0,'g′(4)'),why='Signed triangle areas on[0,2]cancel; rectangle[2,3]has area2 and triangle[3,4]area1.')
add(10,N(-2,'g″(4)'),why='FTC gives g″(4)=f′(4), slope−2.')
# Explicit source integrands, not answer-key parsing.
definite={11:(8*x**3+3*x*x,x,1,2),13:(1-x**9,x,0,1),14:((1-x)**9,x,0,1),15:((S.sqrt(u)-2*u*u)/u,u,1,9),16:((u**S.Rational(1,4)+1)**2,u,0,1),17:(x*(x*x+1)**5,x,0,1),18:(x*x*S.sqrt(1+x**3),x,0,2),20:(S.sin(3*pi*t),t,0,1),21:(x*x*S.cos(x**3),x,0,1),22:(S.sin(x)/(1+x*x),x,-1,1),23:(t**4*S.tan(t)/(2+S.cos(t)),t,-pi/4,pi/4),24:(S.exp(x)/(1+S.exp(2*x)),x,0,1),38:((1+S.tan(t))**3/S.cos(t)**2,t,0,pi/4)}
values={11:37,13:S.Rational(9,10),14:S.Rational(1,10),15:-76,16:S.Rational(49,15),17:S.Rational(21,4),18:S.Rational(52,9),20:2/(3*pi),21:S.sin(1)/3,22:0,23:0,24:S.atan(S.E)-pi/4,38:S.Rational(15,4)}
for num,(e,v,l,h) in definite.items():
 add(num,N(values[num],tol=1e-7),why='Evaluate the exact source integral on its stated bounds. Symmetry is used only on a symmetric interval.')
 CHECKS.append(dict(kind='definite',number=num,integrand=fmt(e),variable=str(v),lower=fmt(l),upper=fmt(h),expected=fmt(values[num])))
add(12,F(T**5/5-4*T*T+7*T,'Integral in terms of T'))
for num in (19,26):add(num,C('Does not exist as an ordinary improper integral','0','A finite value from plugging both endpoints into a primitive',label='Integral status'),why='An interior singularity must be split into one-sided improper integrals; those do not both converge.')
indef={25:(((1-x)/x)**2,x,x-2*S.log(S.Abs(x))-1/x),27:((x+2)/S.sqrt(x*x+4*x),x,S.sqrt(x*x+4*x)),28:(S.csc(x)**2/(1+S.cot(x)),x,-S.log(S.Abs(1+S.cot(x)))),29:(S.sin(pi*t)*S.cos(pi*t),t,S.sin(pi*t)**2/(2*pi)),30:(S.sin(x)*S.cos(S.cos(x)),x,-S.sin(S.cos(x))),31:(S.exp(S.sqrt(x))/S.sqrt(x),x,2*S.exp(S.sqrt(x))),32:(S.sin(S.log(x))/x,x,-S.cos(S.log(x))),33:(S.tan(x)*S.log(S.cos(x)),x,-S.log(S.cos(x))**2/2),34:(x/S.sqrt(1-x**4),x,S.asin(x*x)/2),35:(x**3/(1+x**4),x,S.log(1+x**4)/4),36:(S.sinh(1+4*x),x,S.cosh(1+4*x)/4),37:(S.sec(t)*S.tan(t)/(1+S.sec(t)),t,S.log(S.Abs(1+S.sec(t)))),41:(S.cos(x)/S.sqrt(1+S.sin(x)),x,2*S.sqrt(1+S.sin(x))),42:(x**3/S.sqrt(x*x+1),x,(x*x+1)**S.Rational(3,2)/3-S.sqrt(x*x+1))}
for num,(e,v,p) in indef.items():
 add(num,F(p,'Antiderivative',const=True),limited=num in (41,42),why='A general antiderivative on each connected interval of the original real domain; retain all denominator/log/radical restrictions.')
 CHECKS.append(dict(kind='antiderivative',number=num,integrand=fmt(e),variable=str(v),primitive=fmt(p)))
add(39,N(S.Rational(23,3)))
add(40,N(2))
add(43,N(S.Rational(64,5),'Exact area'),limited=True)
add(44,N(0,'Integral'),limited=True)
derivatives={45:x*x/(1+x**3),46:-S.sqrt(x+S.sin(x)),47:4*x**3*S.cos(x**8),48:S.cos(x)*(1-S.sin(x)**2)/(1+S.sin(x)**4),49:S.exp(x)/x-S.exp(S.sqrt(x))/(2*x),50:3*S.sin((3*x+1)**4)-2*S.sin(16*x**4)}
for num,e in derivatives.items():add(num,F(e,'Derivative'),why='Apply FTC and multiply by each variable endpoint derivative; subtract the lower-endpoint contribution.')
add(51,N(4,'Lower bound'),F(4*S.sqrt(3),'Upper bound'),why='On[1,3],2≤sqrt(x²+3)≤sqrt12; multiply by interval width2.')
add(52,N(S.Rational(1,3),'Lower bound'),N(S.Rational(1,2),'Upper bound'))
for num,ans,w1,w2 in [(53,'0≤x²cosx≤x² on[0,1], so integral≤1/3','cosx≥1 on[0,1]','Integral≤0'),(54,'sinx/x decreases on[π/4,π/2], so integral≤(π/4)*(2√2/π)=√2/2','sinx/x increases on that interval','The bound is a consequence of odd symmetry'),(55,'e^x cosx≤e^x on[0,1], so integral≤e−1','cosx≥1','The integrand is odd'),(56,'x*arcsin x≤(π/2)x on[0,1], so integral≤π/4','arcsin x≤x for everyx∈[0,1]','The integral equals0')]:add(num,C(ans,w1,w2,label='Inequality justification'),limited=True)
add(57,N(sum(mp.sin((mp.mpf(j)/2+mp.mpf('.25'))**3)/2 for j in range(6)),'Midpoint estimate n=6',tol=.000051))
add(58,N(S.Rational(175,6),'a · Displacement',unit='m'),N(S.Rational(59,2),'b · Distance',unit='m'))
add(59,C('Total barrels consumed during2000 through2007, ending January1,2008','Consumption rate on January1,2008','Change in consumption rate',label='Integral interpretation'),limited=True)
add(60,N(4.67+8.86+10.22+10.67+10.81,'Midpoint distance estimate',unit='m',tol=.0051))
add(61,N(4*(100+1000+7000+9000+1400+100),'Population increase',unit='bees',tol=5000),why='Six width4 intervals use graph readings at2,6,10,14,18,22weeks. The graph is approximate; tolerance reflects its scale.')
add(62,F(S.Rational(3,2)-pi/4,'Signed integral'))
add(63,N(3))
# Fresnel C is odd, tends to±1/2, and its first positive hump alone exceeds0.7.
root1=mp.findroot(lambda z:mp.fresnelc(z)-mp.mpf('.7'),.8);root2=mp.findroot(lambda z:mp.fresnelc(z)-mp.mpf('.7'),1.2)
add(64,C('cos(πx²/2)>0: (−1,1) and intervals where4k−1<x²<4k+1, k≥1','C increases everywhere','C increases exactly where x>0',label='a · Increasing intervals'),C('−x sin(πx²/2)>0; for x>0:4k+2<x²<4k+4; for x<0:4k<x²<4k+2, k≥0','C is concave upward wheneverx>0','C is concave upward everywhere',label='b · Concavity intervals'),N(root1,'c · Smaller root',tol=.0051),N(root2,'c · Larger root',tol=.0051),C('Both are odd and oscillate toward±1/2; their slopes are cos(πx²/2) and sin(πx²/2), so their oscillations are offset, not a constant horizontal translation','C and S are identical','C=S′ for allx',label='d · Relation of graphs'),limited=True)
add(65,N(mp.findroot(lambda z:(mp.cosh(z)-1)/z-1,1.5),'Positive c',tol=.000051))
add(66,C('C*exp(−x²/(4kt))/sqrt(4πkt), k>0,t>0','C*exp(−x²/(4kt))/(4πkt)','0 for everyx,t',label='Limit as a→0'),why='The numerator integral divided by a tends to its continuous integrand at u=0.')
add(67,F((2*x-1)*S.exp(2*x)/(1-S.exp(-x)),'Forced formula for x≠0'),C('No function continuous on all realx satisfies the identity: atx=0 the differentiated equation requires0=−1','The displayed formula is continuous on all realx','f(0)=0 makes the singularity removable',label='Global existence caveat'),why='On an interval containing1 but excluding0, differentiation and the initial identity yield the displayed formula. The literal condition “for all x” with global continuity is inconsistent.')
add(68,N(3))
add(69,C('d(f²)/dx=2ff′; FTC gives f(b)²−f(a)²','The derivative of f² is f′²','Replace f by its endpoint average',label='Proof step'),limited=True)
add(70,N(3))
add(71,C('Letu=1−x; dx=−du and reverse the bounds1→0','Letu=1−x but keepdx=du','The identity requires f to be symmetric',label='Substitution proof'),limited=True)
add(72,N(S.Rational(1,10)))
add(73,N(S.Rational(2,3)),why='The regions under a strictly increasing bijection and its inverse partition the unit square.')
assert len(ROWS)==100,len(ROWS)
HERE=Path(__file__).parent
(HERE/'review.json').write_text(json.dumps(ROWS,ensure_ascii=False,indent=2)+'\n')
(HERE/'review-audit.json').write_text(json.dumps(dict(total=len(ROWS),fields=sum(len(v['grader'].get('parts',[v['grader']])) for v in ROWS.values()),sourceSHA256=hashlib.sha256((ROOT/'site/books/calculus/chapter-05.pdf').read_bytes()).hexdigest(),reviewedPrintedPages=[421,422,423,424],independentCases=CHECKS,sourceCaveat='Review67 requires a local interval excluding0; its literal global continuity condition is inconsistent.'),ensure_ascii=False,indent=2)+'\n')
print('Chapter5review',len(ROWS))
