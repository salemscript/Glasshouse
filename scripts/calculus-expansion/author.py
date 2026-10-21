"""Explicit source-reviewed question contracts, not inferred answer-key graders."""
import math
import sympy as S
import mpmath as mp
x=S.symbols('x',real=True)
a,b,alpha,T=S.symbols('a b alpha T',positive=True)
records={}
integrals={}
def fmt(e):return S.sstr(e).replace('**','^').replace('Abs(', 'abs(')
def num(label,value,tolerance=None,unit=''):
 v=float(value);return dict(type='numeric',label=label,answer=v,tolerance=tolerance if tolerance is not None else max(1e-8,abs(v)*1e-9),unit=unit)
def choice(label,correct,*wrong):
 assert correct not in wrong and len(set(wrong))==len(wrong),(label,correct,wrong)
 return dict(type='choice',label=label,answer=correct,options=[correct,*wrong])
def formula(label,expression,constant=False):
 text=fmt(expression)+(' + C' if constant else '')
 return choice(label,text,fmt(2*expression)+(' + C' if constant else ''),fmt(-expression)+(' + C' if constant else ''))
def add(section,number,answer,working,reason,fields,limited=False):
 qid=f'calculus-section-{section.replace(".","-")}-{number}';assert qid not in records
 records[qid]=dict(finalText=answer,working=working,reason=reason,fields=fields,limited=limited)
def primitive(number,integrand,F,sub,converted,domain='On every interval where the original integrand is real and defined.',graph=False):
 integrals[number]=(integrand,F,sub,domain)
 work=f'Set u={sub}. {converted} Integrate in u and substitute back: F(x)={fmt(F)} + C. Differentiating the nonconstant part gives {fmt(integrand)}, recovering the original integrand.'
 if graph:work+=' For the requested plot take C=0. The antiderivative increases where the integrand is positive, decreases where it is negative, and has horizontal tangent where it vanishes; vertical shifts from other C values do not change its derivative.'
 fields=[formula('Antiderivative',F,True)]
 add('5.5',number,fmt(F)+' + C',work,domain+' Each connected interval may have its own integration constant; a logarithm uses absolute value when its inner expression may be negative.',fields,graph)
R=S.Rational
primitives={
1:(S.cos(2*x),S.sin(2*x)/2,'2x','du=2 dx, so the transformed integral is (1/2)∫cos u du.'),
2:(x*S.exp(-x*x),-S.exp(-x*x)/2,'−x²','du=−2x dx, so the integral is −(1/2)∫eᵘ du.'),
3:(x*x*S.sqrt(x**3+1),R(2,9)*(x**3+1)**R(3,2),'x³+1','du=3x² dx, so integrate (1/3)u^(1/2).'),
4:(S.sin(x)**2*S.cos(x),S.sin(x)**3/3,'sin θ','du=cos θ dθ, so the integral is ∫u² du. Here x in the formula represents the source variable θ.'),
5:(x**3/(x**4-5),S.log(S.Abs(x**4-5))/4,'x⁴−5','du=4x³ dx, giving (1/4)∫du/u.'),
6:(S.sqrt(2*x+1),(2*x+1)**R(3,2)/3,'2t+1','du=2 dt, giving (1/2)∫u^(1/2)du. Here x represents the source variable t.'),
7:(x*S.sqrt(1-x*x),-(1-x*x)**R(3,2)/3,'1−x²','du=−2x dx, giving −(1/2)∫u^(1/2)du.'),
8:(x*x*S.exp(x**3),S.exp(x**3)/3,'x³','du=3x² dx, giving (1/3)∫eᵘ du.'),
9:((1-2*x)**9,-(1-2*x)**10/20,'1−2x','du=−2 dx, giving −(1/2)∫u⁹du.'),
10:(S.sin(x)*S.sqrt(1+S.cos(x)),-R(2,3)*(1+S.cos(x))**R(3,2),'1+cos t','du=−sin t dt, giving −∫u^(1/2)du. Here x represents t.'),
11:(S.cos(S.pi*x/2),2*S.sin(S.pi*x/2)/S.pi,'πt/2','du=(π/2)dt, giving (2/π)∫cos u du. Here x represents t.'),
12:(1/S.cos(2*x)**2,S.tan(2*x)/2,'2θ','du=2dθ, giving (1/2)∫sec²u du. Here x represents θ.'),
13:(1/(5-3*x),-S.log(S.Abs(5-3*x))/3,'5−3x','du=−3dx, giving −(1/3)∫du/u.'),
14:(x*x*(4-x**3)**R(2,3),-(4-x**3)**R(5,3)/5,'4−y³','du=−3y²dy, giving −(1/3)∫u^(2/3)du. Interpret cube-root powers as real powers. Here x represents y.'),
15:(S.cos(x)**3*S.sin(x),-S.cos(x)**4/4,'cos θ','du=−sin θ dθ, giving −∫u³du. Here x represents θ.'),
16:(S.exp(-5*x),-S.exp(-5*x)/5,'−5r','du=−5dr, giving −(1/5)∫eᵘdu. Here x represents r.'),
17:(S.exp(x)/(1-S.exp(x))**2,1/(1-S.exp(x)),'1−eᵘ','Use w=1−eᵘ, dw=−eᵘdu to obtain −∫w⁻²dw. Here x represents the source variable u, not the new substitution w.'),
18:(S.sin(S.sqrt(x))/S.sqrt(x),-2*S.cos(S.sqrt(x)),'√x','du=dx/(2√x), giving 2∫sin u du.'),
19:((a+b*x*x)/S.sqrt(3*a*x+b*x**3),R(2,3)*S.sqrt(3*a*x+b*x**3),'3ax+bx³','du=3(a+bx²)dx, giving (1/3)∫u^(−1/2)du.'),
20:(x*x/(x**3+1),S.log(S.Abs(x**3+1))/3,'z³+1','du=3z²dz, giving (1/3)∫du/u. Here x represents z.'),
21:(S.log(x)**2/x,S.log(x)**3/3,'ln x','du=dx/x, giving ∫u²du; x>0.'),
22:(S.sin(x)*S.sin(S.cos(x)),S.cos(S.cos(x)),'cos x','du=−sin x dx, giving −∫sin u du.'),
23:(S.tan(x)**3/S.cos(x)**2,S.tan(x)**4/4,'tan θ','du=sec²θdθ, giving ∫u³du. Here x represents θ.'),
24:(x*S.sqrt(x+2),R(2,5)*(x+2)**R(5,2)-R(4,3)*(x+2)**R(3,2),'x+2','x=u−2 and dx=du, so integrate u^(3/2)−2u^(1/2).'),
25:(S.exp(x)*S.sqrt(1+S.exp(x)),R(2,3)*(1+S.exp(x))**R(3,2),'1+eˣ','du=eˣdx, giving ∫u^(1/2)du.'),
26:(1/(a*x+b),S.log(S.Abs(a*x+b))/a,'ax+b','du=a dx, giving (1/a)∫du/u; a≠0 is required.'),
27:((x*x+1)*(x**3+3*x)**4,(x**3+3*x)**5/15,'x³+3x','du=3(x²+1)dx, giving (1/3)∫u⁴du.'),
28:(S.exp(S.cos(x))*S.sin(x),-S.exp(S.cos(x)),'cos t','du=−sin tdt, giving −∫eᵘdu. Here x represents t.'),
29:(5**x*S.sin(5**x),-S.cos(5**x)/S.log(5),'5ᵗ','du=(ln5)5ᵗdt, giving (1/ln5)∫sin u du. Here x represents t.'),
30:(1/(S.cos(x)**2*S.tan(x)**2),-1/S.tan(x),'tan x','du=sec²x dx, giving ∫u⁻²du. Retain the original sec and tan exclusions even if simplification removes one.'),
31:(S.atan(x)**2/(x*x+1),S.atan(x)**3/3,'arctan x','du=dx/(1+x²), giving ∫u²du.'),
32:(x/(x*x+4),S.log(x*x+4)/2,'x²+4','du=2x dx, giving (1/2)∫du/u; u is always positive.'),
33:(S.cos(1+5*x),S.sin(1+5*x)/5,'1+5t','du=5dt, giving (1/5)∫cos u du. Here x represents t.'),
34:(S.cos(S.pi/x)/x**2,-S.sin(S.pi/x)/S.pi,'π/x','du=−π dx/x², giving −(1/π)∫cos u du; x≠0.'),
35:(S.sqrt(S.cot(x))/S.sin(x)**2,-R(2,3)*S.cot(x)**R(3,2),'cot x','du=−csc²x dx, giving −∫u^(1/2)du; require cot x≥0 and sin x≠0.'),
36:(2**x/(2**x+3),S.log(2**x+3)/S.log(2),'2ᵗ+3','du=(ln2)2ᵗdt, giving (1/ln2)∫du/u. Here x represents t.'),
37:(S.sinh(x)**2*S.cosh(x),S.sinh(x)**3/3,'sinh x','du=cosh x dx, giving ∫u²du.'),
38:(1/(S.cos(x)**2*S.sqrt(1+S.tan(x))),2*S.sqrt(1+S.tan(x)),'1+tan t','du=sec²t dt, giving ∫u^(−1/2)du. The original square-root denominator must be strictly positive. Here x represents t.'),
39:(S.sin(2*x)/(1+S.cos(x)**2),-S.log(1+S.cos(x)**2),'1+cos²x','du=−2cos x sin x dx=−sin2x dx, giving −∫du/u.'),
40:(S.sin(x)/(1+S.cos(x)**2),-S.atan(S.cos(x)),'cos x','du=−sin xdx, giving −∫du/(1+u²).'),
41:(S.cot(x),S.log(S.Abs(S.sin(x))),'sin x','Write cot x=cos x/sin x; du=cos x dx gives ∫du/u.'),
42:(S.cos(S.log(x))/x,S.sin(S.log(x)),'ln t','du=dt/t, giving ∫cos u du; t>0. Here x represents t.'),
43:(1/(S.sqrt(1-x*x)*S.asin(x)),S.log(S.Abs(S.asin(x))),'arcsin x','du=dx/√(1−x²), giving ∫du/u. Require −1<x<1 and x≠0.'),
44:(x/(1+x**4),S.atan(x*x)/2,'x²','du=2x dx, giving (1/2)∫du/(1+u²).'),
45:((1+x)/(1+x*x),S.atan(x)+S.log(1+x*x)/2,'Split the numerator','Integrate 1/(1+x²) directly; for x/(1+x²), use u=1+x² and du=2x dx.'),
46:(x*x*S.sqrt(x+2),R(2,7)*(x+2)**R(7,2)-R(8,5)*(x+2)**R(5,2)+R(8,3)*(x+2)**R(3,2),'x+2','x=u−2, so the integrand becomes (u−2)²u^(1/2)=u^(5/2)−4u^(3/2)+4u^(1/2).'),
47:(x*(2*x+5)**8,(2*x+5)**10/40-R(5,36)*(2*x+5)**9,'2x+5','x=(u−5)/2 and dx=du/2, giving (1/4)∫(u⁹−5u⁸)du.'),
48:(x**3*S.sqrt(x*x+1),(x*x+1)**R(5,2)/5-(x*x+1)**R(3,2)/3,'x²+1','du=2x dx and x²=u−1, giving (1/2)∫(u^(3/2)−u^(1/2))du.'),
49:(x*(x*x-1)**3,(x*x-1)**4/8,'x²−1','du=2x dx, giving (1/2)∫u³du.'),
50:(S.tan(x)**6/S.cos(x)**2,S.tan(x)**7/7,'tan θ','du=sec²θdθ, giving ∫u⁶du. Here x represents θ.'),
51:(S.exp(S.cos(x))*S.sin(x),-S.exp(S.cos(x)),'cos x','du=−sin xdx, giving −∫eᵘdu.'),
52:(S.sin(x)*S.cos(x)**4,-S.cos(x)**5/5,'cos x','du=−sin xdx, giving −∫u⁴du.')}
for index,args in primitives.items():primitive(index,*args,graph=index in [49,50,51,52])
definite_integrals={}
def definite(number,f,F,left,right,method,exact=None):
 value=S.simplify(F.subs(x,right)-F.subs(x,left)) if exact is None else exact
 definite_integrals[number]=(f,F,left,right,value)
 field=formula('Integral',value) if getattr(value,'free_symbols',set()) else num('Integral',S.N(value,30))
 add('5.5',number,fmt(value),method+f' An antiderivative is {fmt(F)}. Evaluate F({fmt(right)})−F({fmt(left)})={fmt(value)}.', 'Transform both endpoints when integrating in a new variable, or substitute back before using the original endpoints. Keep signed orientation and the real domain.',[field])
defs={
53:(S.cos(S.pi*x/2),2*S.sin(S.pi*x/2)/S.pi,S.Integer(0),S.Integer(1),'Use u=πt/2, du=(π/2)dt; the new endpoints are 0 and π/2.'),
54:((3*x-1)**50,(3*x-1)**51/153,S.Integer(0),S.Integer(1),'Use u=3t−1, du=3dt; the new endpoints are −1 and 2.'),
55:((1+7*x)**R(1,3),R(3,28)*(1+7*x)**R(4,3),S.Integer(0),S.Integer(1),'Use u=1+7x; du=7dx; u runs from 1 to 8.'),
56:(1/(5*x+1),S.log(5*x+1)/5,S.Integer(0),S.Integer(3),'Use u=5x+1; du=5dx; u runs from 1 to 16.'),
57:(S.sin(x)/S.cos(x)**2,1/S.cos(x),S.Integer(0),S.pi/6,'Use u=cos t; du=−sin tdt. Integrate −u⁻².'),
58:(1/S.sin(x/2)**2,-2/S.tan(x/2),S.pi/3,2*S.pi/3,'Use u=t/2; dt=2du. Integrate 2csc²u.'),
59:(S.exp(1/x)/x**2,-S.exp(1/x),S.Integer(1),S.Integer(2),'Use u=1/x, du=−dx/x²; u runs from 1 to 1/2, so preserve the reversed orientation.'),
60:(x*S.exp(-x*x),-S.exp(-x*x)/2,S.Integer(0),S.Integer(1),'Use u=−x², du=−2x dx; the endpoints become 0 and −1.'),
61:(x**3+x**4*S.tan(x),S.Integer(0),-S.pi/4,S.pi/4,'Both x³ and x⁴tan x are odd and continuous on this interval. Their signed integrals on symmetric endpoints cancel.',S.Integer(0)),
62:(S.cos(x)*S.sin(S.sin(x)),-S.cos(S.sin(x)),S.Integer(0),S.pi/2,'Use u=sin x, du=cos xdx; u runs from 0 to 1.'),
63:((1+2*x)**R(-2,3),R(3,2)*(1+2*x)**R(1,3),S.Integer(0),S.Integer(13),'Use u=1+2x, du=2dx; u runs from 1 to 27.'),
64:(x*S.sqrt(a*a-x*x),-(a*a-x*x)**R(3,2)/3,S.Integer(0),a,'Use u=a²−x², du=−2x dx. For a≥0, the result is a³/3; for arbitrary real a the same endpoint calculation gives |a|³/3.',a**3/3),
65:(x*S.sqrt(x*x+a*a),(x*x+a*a)**R(3,2)/3,S.Integer(0),a,'The source assumes a>0. Use u=x²+a², du=2x dx; u runs from a² to 2a².'),
66:(x**4*S.sin(x),S.Integer(0),-S.pi/3,S.pi/3,'x⁴sin x is odd and continuous. Its signed areas on the symmetric interval cancel.',S.Integer(0)),
67:(x*S.sqrt(x-1),R(2,5)*(x-1)**R(5,2)+R(2,3)*(x-1)**R(3,2),S.Integer(1),S.Integer(2),'Use u=x−1 and x=u+1; integrate u^(3/2)+u^(1/2) from 0 to 1.'),
68:(x/S.sqrt(1+2*x),(1+2*x)**R(3,2)/6-S.sqrt(1+2*x)/2,S.Integer(0),S.Integer(4),'Use u=1+2x, x=(u−1)/2, dx=du/2. The integrand becomes (1/4)(u^(1/2)−u^(−1/2)), with endpoints 1 and 9.'),
69:(1/(x*S.sqrt(S.log(x))),2*S.sqrt(S.log(x)),S.E,S.exp(4),'Use u=ln x, du=dx/x; endpoints are 1 and 4.'),
70:((x-1)*S.exp((x-1)**2),S.exp((x-1)**2)/2,S.Integer(0),S.Integer(2),'Use u=(x−1)² and an antiderivative; both original endpoints give the same antiderivative value. Equivalently the integrand is odd about x=1.'),
71:((S.exp(x)+1)/(S.exp(x)+x),S.log(S.exp(x)+x),S.Integer(0),S.Integer(1),'Use u=eᶻ+z, du=(eᶻ+1)dz; the endpoints become 1 and e+1.'),
72:(S.sin(2*S.pi*x/T-alpha),-T*S.cos(2*S.pi*x/T-alpha)/(2*S.pi),S.Integer(0),T/2,'Use u=2πt/T−α, dt=Tdu/(2π). The endpoints are −α and π−α; cos(π−α)=−cosα.'),
73:(1/(1+S.sqrt(x))**4,-1/(1+S.sqrt(x))**2+R(2,3)/(1+S.sqrt(x))**3,S.Integer(0),S.Integer(1),'Use u=1+√x. Then x=(u−1)² and dx=2(u−1)du; integrate 2u⁻³−2u⁻⁴ from 1 to 2.')}
for index,args in defs.items():definite(index,*args)
records['calculus-section-5-5-64'].update(finalText='|a|³/3 (a³/3 when a≥0).',fields=[choice('Integral for real a','|a|³/3','−|a|³/3','|a|²/3')])
add('5.5',74,'0≤the integral≤1.','The real cube root is odd and sine is odd, so sin(∛(−x))=−sin(∛x). The integral over [−2,2] is zero. The remaining integral is over [2,3], where 0≤sin(∛x)≤1. Integrating these bounds over an interval of width 1 gives the claimed inequalities.','Odd symmetry cancels only the symmetric portion of the interval, not the entire [−2,3] interval.',[choice('Reason','Cancel [−2,2], then bound the remaining integrand between 0 and 1 on [2,3].','The entire integral is zero by oddness.','The integrand is always negative.')],True)
add('5.5',75,'Exact area (3√3−1)/3≈1.39872.','The curve √(2x+1) is positive and rises from 1 to √3 on [0,1], so its area is roughly 1.4 square units. Put u=2x+1, du=2dx: area=(1/2)∫₁³u^(1/2)du=[u^(3/2)/3]₁³=(3√3−1)/3.','The exact value is consistent with an area between 1 and √3.',[num('Graph estimate',1.4,.15),num('Exact area',(3*S.sqrt(3)-1)/3)],True)
add('5.5',76,'Area 4.','Write y=2sin x−sin2x=2sin x(1−cos x), nonnegative on [0,π]. A graph suggests about 4 square units. Integrating gives [−2cos x+(1/2)cos2x]₀^π=4; no absolute-value splitting is needed.','The definite integral equals geometric area here because the curve stays on or above the axis.',[num('Graph estimate',4,.4),num('Exact area',4)],True)
add('5.5',77,'6π.','Split (x+3)√(4−x²) into x√(4−x²)+3√(4−x²). The first term is odd and integrates to zero on [−2,2]. The second is three times the area of the upper semicircle of radius 2, which is (1/2)π·2²=2π. Thus the integral is 3·2π=6π.','The graph of the radical is the upper semicircle, not the full circle.',[num('Integral',6*S.pi)])
add('5.5',78,'π/8.','Set u=x², du=2x dx. The integral becomes (1/2)∫₀¹√(1−u²)du. The new integrand is a quarter of the unit circle, whose area is π/4. Multiplication by 1/2 gives π/8.','The substitution changes both the differential and the coordinate used for the geometric interpretation.',[num('Integral',S.pi/8)])
add('5.5',79,'All three areas are equal, and each is 2.','The first area is ∫₀¹e^(√x)dx. With u=√x and dx=2u du this becomes ∫₀¹2u eᵘdu, exactly the second area. In the third, e^(sin x)sin2x=2sin x e^(sin x)cos x; set u=sin x to obtain the same integral on [0,1]. Since an antiderivative of 2u eᵘ is 2eᵘ(u−1), the common area is 2.','All three original integrands are nonnegative on their indicated intervals.',[choice('Equal areas','All three areas.','Only the first and second.','Only the first and third.'),num('Common area',2)])
add('5.5',80,'2040 kcal.','Integrate R(t)=85−0.18cos(πt/12) from t=0 to 24 hours. An antiderivative is 85t−(2.16/π)sin(πt/12). Both endpoint sine values are zero, leaving 85·24=2040 kcal.','A complete cosine period contributes zero signed correction to the constant baseline rate; rate×time gives energy.',[num('Total metabolism',2040,1e-6,'kcal')])
add('5.5',81,'10000(1−e⁻⁰·⁶)≈4511.8836 L.','One hour is 60 minutes. Integrate the leak rate: ∫₀⁶⁰100e^(−0.01t)dt=[−10000e^(−0.01t)]₀⁶⁰=10000(1−e^(−0.6)).','The rate is in liters per minute; using an upper endpoint of 1 would calculate only one minute of leakage.',[num('Leaked volume',10000*(1-S.exp(-R(3,5))),.01,'L')])
add('5.5',82,'400e^3.37701≈'+str(float(400*S.exp(S.Rational(337701,100000))))+' bacteria.','The rate is r(t)=450.268e^(1.12567t) bacteria/hour. The population is the initial 400 plus the rate integral from 0 to 3. Since 450.268/1.12567=400, N(3)=400+400(e^3.37701−1)=400e^3.37701.','An integrated growth rate gives the increase, so retain the initial population. Round to a whole bacterium only at the end.',[num('Population after 3 h',400*S.exp(R(337701,100000)),1,'bacteria')])
add('5.5',83,'V(t)=5[1−cos(2πt/5)]/(4π) L above the volume at the beginning of inhalation.','Integrate f(t)=(1/2)sin(2πt/5) from 0 to t: V(t)=[−5cos(2πs/5)/(4π)]₀ᵗ=5[1−cos(2πt/5)]/(4π). During 0≤t≤2.5 s the volume rises to 5/(2π) L; during the next half-cycle it returns to its baseline at t=5 s. If the actual initial lung volume is V₀, add V₀.','The model describes the change from baseline, not total anatomical lung volume; the rate is negative during exhalation.',[choice('Volume above baseline','5[1−cos(2πt/5)]/(4π) L.','−5cos(2πt/5)/(4π) L with no added constant.','(1/2)sin(2πt/5) L.')])
fish=25000+20000/(1+5*S.exp(-12))-S.Rational(20000,6)
add('5.5',84,f'{float(fish):.6f} kg.','Take t=0 in 2000 and t=20 in 2020. Set u=1+5e^(−0.6t), so du=−3e^(−0.6t)dt. The integrated growth is 20000/[1+5e^(−0.6t)]. Hence biomass in 2020 is 25000+20000/(1+5e^(−12))−20000/6≈41666.0523 kg.','Integrating G gives a biomass increase; include the original 25000 kg and subtract the antiderivative at t=0.',[num('Biomass in 2020',fish,.1,'kg')])
add('5.5',85,'C₀(1−e^(−30r/V)) mg.','Treat r,V,C₀ as constants with r,V>0. An antiderivative of (r/V)C₀e^(−rt/V) is −C₀e^(−rt/V). Evaluation from 0 to 30 minutes gives C₀[1−e^(−30r/V)], the total urea removed in that half hour.','The dimensionless exponent uses r/V in min⁻¹; the amount removed is between 0 and the initial amount C₀.',[choice('Removed amount','C₀(1−e^(−30r/V))','C₀e^(−30r/V)','(r/V)C₀e^(−30r/V)')])
add('5.5',86,'85000/21≈4047.619 calculators.','Beginning of the third week is t=2, and end of the fourth is t=4. Integrate 5000[1−100/(t+10)²]: an antiderivative is 5000[t+100/(t+10)]. Thus production is 5000[(4+100/14)−(2+100/12)]=85000/21.','The rate is in calculators per week; using t=3 to t=4 would omit one week. The fitted model produces a continuous estimate of a discrete count.',[num('Calculators produced',S.Rational(85000,21),1,'calculators')])
add('5.5',87,'5.','Set u=2x, dx=du/2. The endpoints x=0,2 become u=0,4. Thus ∫₀²f(2x)dx=(1/2)∫₀⁴f(u)du=10/2=5.','Changing only the integrand and not the differential would miss the factor 1/2.',[num('Integral',5)])
add('5.5',88,'2.','Use u=x², du=2x dx. The endpoints 0 and 3 become 0 and 9, so ∫₀³xf(x²)dx=(1/2)∫₀⁹f(u)du=4/2=2.','The factor x in the original integrand supplies the substitution differential.',[num('Integral',2)])
proofs={89:('∫ from a to b f(−x)dx = ∫ from −b to −a f(u)du.','Put u=−x, du=−dx. The endpoints become −a and −b; the minus sign reverses them. For f≥0 the graph y=f(−x) is the horizontal reflection of f, and reflected regions have equal width/height area.','u=−x, du=−dx, and reverse the transformed endpoints.'),90:('∫ from a to b f(x+c)dx = ∫ from a+c to b+c f(u)du.','Put u=x+c, du=dx. The interval shifts to [a+c,b+c]. For f≥0, horizontal translation preserves the area of the corresponding region.','u=x+c; shift both endpoints by c.'),91:('The two beta-type integrals are equal.','Let u=1−x, du=−dx. The original endpoints 0,1 become 1,0. Reversing them yields ∫₀¹(1−u)^a u^bdu, which is the second integral. For a,b>0 both integrands are continuous at the endpoints.','u=1−x, with endpoints reversed.'),92:('I=(π/2)∫₀^π f(sin x)dx.','Let I=∫₀^π xf(sin x)dx. With u=π−x and sin(π−u)=sin u, I=∫₀^π(π−u)f(sin u)du. Add this to the original form: 2I=π∫₀^πf(sin u)du; divide by 2.','Use u=π−x, then add the transformed and original integrals.')}
for number,(answer,work,right) in proofs.items():add('5.5',number,answer,work,'This checks the substitution/proof idea; the full written proof or drawing is not automatically assessed.',[choice('Proof step',right,'Change the integrand but leave every endpoint unchanged.','Drop the differential factor without adjusting it.')],True)
add('5.5',93,'π²/4.','Apply Exercise 92 with f(sin x)=sin x/(1+cos²x), which is symmetric about π/2. More explicitly, sin x/(1+cos²x)=sin x/(2−sin²x), a continuous function of sin x. Thus I=(π/2)∫₀^π sin x/(1+cos²x)dx. Set u=cos x, du=−sin xdx: the remaining integral is ∫₋₁¹du/(1+u²)=π/2. Hence I=π²/4.','The symmetry applies to the whole non-x factor, including its denominator.',[num('Integral',S.pi**2/4)])
add('5.5',94,'(a) The integrals are equal. (b) Each squared-trig integral is π/4.','For (a), substitute u=π/2−x, so cos x=sin u and the endpoint reversal cancels the differential minus sign. For (b), this makes ∫cos² and ∫sin² equal on [0,π/2]. Their sum is ∫₀^(π/2)1dx=π/2, so each is π/4.','Equality of the two integrals and their sum determine their values without a half-angle antiderivative.',[choice('a','Use u=π/2−x to exchange sine and cosine.','Use u=π−x and claim cos x=sin u.','Treat f as a constant.'),num('b · cosine squared',S.pi/4),num('b · sine squared',S.pi/4)],True)
averages={}
def average(number,f,F,left,right,sub,unit=''):
 value=S.simplify((F.subs(x,right)-F.subs(x,left))/(right-left))
 averages[number]=(f,F,left,right,value)
 add('6.5',number,fmt(value)+((' '+unit) if unit else ''),f'The average is (1/({fmt(right)}−({fmt(left)})))∫ from {fmt(left)} to {fmt(right)} of {fmt(f)}. {sub} An antiderivative is {fmt(F)}; dividing F({fmt(right)})−F({fmt(left)}) by the width gives {fmt(value)}.','A function average is signed integral divided by interval length, not an average of endpoint values. Its units are the original function units.',[num('Average value',S.N(value,30),unit=unit)])
avg_inputs={1:(3*x*x+8*x,x**3+4*x*x,S.Integer(-1),S.Integer(2),'Integrate each polynomial term.'),2:(S.sqrt(x),R(2,3)*x**R(3,2),S.Integer(0),S.Integer(4),'Use the power rule for the antiderivative of x^(1/2).'),3:(3*S.cos(x),3*S.sin(x),-S.pi/2,S.pi/2,'Use the sine antiderivative and the interval width π.'),4:(x/S.sqrt(3+x*x),S.sqrt(3+x*x),S.Integer(1),S.Integer(3),'Use u=3+t², du=2t dt; x denotes the source variable t.'),5:(S.exp(S.sin(x))*S.cos(x),S.exp(S.sin(x)),S.Integer(0),S.pi/2,'Use u=sin t, du=cos tdt; x denotes t.'),6:(x*x/(x**3+3)**2,-1/(3*(x**3+3)),S.Integer(-1),S.Integer(1),'Use u=x³+3, du=3x²dx; the transformed endpoints are 2 and 4.'),7:(S.cos(x)**4*S.sin(x),-S.cos(x)**5/5,S.Integer(0),S.pi,'Use u=cos x, du=−sin xdx; endpoints are 1 and −1.'),8:(S.log(x)/x,S.log(x)**2/2,S.Integer(1),S.Integer(5),'Use u=ln u in the source variable, or more distinctly set w=ln u and dw=du/u. Here x denotes that source u.')}
for index,args in avg_inputs.items():average(index,*args)
mp.mp.dps=50
c11=sorted([float(mp.findroot(lambda z:2*mp.sin(z)-mp.sin(2*z)-4/mp.pi,guess)) for guess in [1.2,2.8]])
a12=(1-mp.exp(-4))/2
c12=sorted([float(mp.findroot(lambda z:2*z*mp.exp(-z*z)-a12,guess)) for guess in [.25,1.3]])
add('6.5',9,'Average 1; c=2 or 4; rectangle base [2,5], height 1.','The integral of (x−3)² from 2 to 5 is [(x−3)³/3]₂⁵=3; divide by width 3 to get 1. Solve (c−3)²=1, giving c=2,4, both in [2,5]. The parabola has vertex (3,0); a rectangle over the whole interval with height 1 has area 3, equal to the integral.','The question asks all c in the interval; an endpoint can be a solution even though the mean-value theorem also guarantees an interior one.',[num('a',1),num('b · smaller c',2),num('b · larger c',4),choice('c · rectangle','Base [2,5], height 1, area 3.','Base [2,5], height 3, area 9.','Base [2,5], height 0, area 0.')],True)
add('6.5',10,'Average ln3/2; c=2/ln3.','∫₁³dx/x=ln3, and the interval width is 2, so f_avg=ln3/2. Solve 1/c=ln3/2, yielding c=2/ln3≈1.820478. The decreasing hyperbola on [1,3] and a rectangle of height ln3/2 both enclose area ln3 above the axis.','c lies in the original interval; the average is not (1+1/3)/2.',[num('a',S.log(3)/2),num('b',2/S.log(3)),choice('c · rectangle','Base [1,3], height ln3/2, area ln3.','Base [1,3], height ln3, area 2ln3.','Base [0,3], height ln3/2.')],True)
add('6.5',11,'Average 4/π; c≈'+', '.join(f'{v:.8f}' for v in c11)+'.','Integrate 2sin x−sin2x on [0,π] to get 4, and divide by π. The curve starts and ends at zero, stays nonnegative, and reaches its maximum at x=2π/3. Solve 2sin c−sin2c=4/π numerically on each side of that maximum, giving '+', '.join(f'{v:.8f}' for v in c11)+'. A width-π rectangle of height 4/π has area 4.','There are two c values; checking only one would leave the requested set incomplete.',[num('a',4/S.pi),num('b · smaller c',c11[0],1e-5),num('b · larger c',c11[1],1e-5),choice('c · rectangle','Base [0,π], height 4/π, area 4.','Base [0,π], height 4, area 4π.','Height 0.')],True)
add('6.5',12,'Average (1−e⁻⁴)/2; c≈'+', '.join(f'{v:.8f}' for v in c12)+'.','An antiderivative of 2xe^(−x²) is −e^(−x²). The integral from 0 to 2 is 1−e⁻⁴, so the average is (1−e⁻⁴)/2≈0.49084218. The curve rises to its maximum at x=1/√2 then falls. Solve 2ce^(−c²)=(1−e⁻⁴)/2 on both sides of that point, yielding '+', '.join(f'{v:.8f}' for v in c12)+'. The equal-area rectangle has base [0,2] and that average height.','The total area is twice the average height, because the interval width is 2.',[num('a',(1-S.exp(-4))/2),num('b · smaller c',c12[0],1e-5),num('b · larger c',c12[1],1e-5),choice('c · rectangle','Base [0,2], height (1−e⁻⁴)/2, area 1−e⁻⁴.','Base [0,2], height 1−e⁻⁴.','A rectangle of height 0.')],True)
add('6.5',13,'There is a c∈[1,3] for which f(c)=4.','The function is continuous, so the Mean Value Theorem for Integrals applies. The average is (1/(3−1))∫₁³f(x)dx=8/2=4. Hence f attains that average at least once in the interval.','Continuity is essential to the existence claim; the value of c need not be unique.',[choice('Reason','Continuity and average value 8/(3−1)=4 imply f(c)=4 for some c.','The integral 8 means f(x)=8 everywhere.','Every function with integral 8 must be linear.')],True)
add('6.5',14,'b=(3−√5)/2 or (3+√5)/2.','For b>0, the average on [0,b] is (1/b)[2x+3x²−x³]₀ᵇ=2+3b−b². Setting it equal to 3 gives b²−3b+1=0 and the two positive roots (3±√5)/2. b=0 is not an averaging interval.','Both solutions must be retained; dividing by b requires b≠0.',[num('Smaller b',(3-S.sqrt(5))/2),num('Larger b',(3+S.sqrt(5))/2)])
add('6.5',15,'9/8=1.125.','Read the graph vertices (0,−1),(2,1),(3,0),(4,2),(6,2),(7,1),(8,3). Sum signed trapezoid areas: 0+1/2+1+4+3/2+2=9. Divide by interval width 8 to get 9/8.','The part below the axis contributes negatively; the first two-unit segment has zero net signed area.',[num('Average value',R(9,8))])
add('6.5',16,'Approximately 45.7 km/h; the instantaneous velocity matches at about 5.4 s.','Choose three equal subintervals of width 4 seconds, with midpoints t=2,6,10. Read approximate velocities 20,50,67 km/h from the graph. The estimated integral is 4(20+50+67) in (km/h)·s; divide by total width 12 s to get (20+50+67)/3≈45.7 km/h. A horizontal line at that velocity meets the rising curve near t=5.4 s.','These are graph estimates, not exact measurements. Other midpoint subdivisions and reasonable graph readings can differ slightly; seconds cancel because both numerator and denominator use the same time unit.',[num('a · midpoint estimate',137/3,2.5,'km/h'),num('b · graph time',5.4,.5,'s')],True)
add('6.5',17,'50+28/π≈58.9127 °F.','From 9 AM to 9 PM, t runs from 0 to 12 hours. Average (1/12)∫₀¹²[50+14sin(πt/12)]dt. An antiderivative is 50t−(168/π)cos(πt/12), so the integral is 600+336/π and the average is 50+28/π.','The sine remains nonnegative over this half-cycle, so its average correction is positive rather than zero.',[num('Average temperature',50+28/S.pi,.0001,'°F')])
add('6.5',18,'PR²/(6ηl), which is 2/3 of the maximum velocity.','Average with respect to r exactly as requested: (1/R)∫₀ᴿ[P/(4ηl)](R²−r²)dr=[P/(4ηl)R][R²r−r³/3]₀ᴿ=PR²/(6ηl). The maximum at r=0 is PR²/(4ηl), giving ratio 2/3.','This is a uniform-radius average. An average over cross-sectional area would use the weight 2πr and gives a different ratio; do not silently change the requested measure.',[choice('Average','PR²/(6ηl)','PR²/(8ηl)','PR²/(4ηl)'),num('Ratio to maximum',R(2,3))])
# Repair a distractor typography slip without altering the correct expression.
records['calculus-section-6-5-18']['fields'][0]['options'][-1]='PR²/(4ηl)'
add('6.5',19,'6 kg/m.','The average linear density is (1/8)∫₀⁸12/√(x+1)dx=(1/8)[24√(x+1)]₀⁸=(24/8)(3−1)=6 kg/m. The total rod mass is 48 kg.','Divide the total mass by length, not by the number of endpoints.',[num('Average density',6,1e-8,'kg/m')])
k=math.log(75/41)/30
coffee=20+34/math.log(75/41)
add('6.5',20,f'k={k:.10f} min⁻¹; average temperature {coffee:.6f} °C.','Newton cooling gives T(t)−20=(95−20)e^(−kt), hence T=20+75e^(−kt). T(30)=61 implies e^(−30k)=41/75 and k=ln(75/41)/30≈0.02013 min⁻¹. Average over 0≤t≤30: 20+75(1−e^(−30k))/(30k)=20+34/ln(75/41)≈'+f'{coffee:.6f}'+' °C. If k is first rounded to 0.02, the average is about 76.3985 °C instead; this small difference is rounding, not a different model.','Use minutes consistently and fit k before rounding.',[num('a · cooling constant',k,1e-6,'min⁻¹'),num('b · average temperature',coffee,.2,'°C')])
popavg=2560*mp.expm1(mp.mpf('.017185')*50)/(mp.mpf('.017185')*50)
add('6.5',21,f'{float(popavg):.6f} million people.','Take t=0 in 1950, so the second half of the twentieth century is 0≤t≤50 years. The average is (1/50)∫₀⁵⁰2560e^(0.017185t)dt=2560[e^(0.017185·50)−1]/(0.017185·50)≈'+f'{float(popavg):.6f}'+' million people.','The model population is measured in millions. Its average is not the arithmetic mean of its endpoint populations.',[num('Average modeled population',float(popavg),.01,'million people')])
add('6.5',22,'Time average v_T/2; displacement average 2v_T/3.','From s=(1/2)gt², v=gt and v_T=gT. Average over time: (1/T)∫₀ᵀgt dt=gT/2=v_T/2. For displacement, v(s)=√(2gs), and s_T=gT²/2. Thus (1/s_T)∫₀^(s_T)√(2gs)ds=(2/3)√(2gs_T)=2v_T/3.','Different averaging measures weight different parts of the motion. g>0,T>0 and motion starts at rest.',[choice('Time average','v_T/2','2v_T/3','v_T'),choice('Displacement average','2v_T/3','v_T/2','v_T')],True)
add('6.5',23,'5/(4π)≈0.397887 L above baseline.','From Exercise 5.5.83, V(t)=5[1−cos(2πt/5)]/(4π) L above the initial baseline. Average over a full five-second cycle: (1/5)∫₀⁵V(t)dt. The cosine integrates to zero over one period, leaving 5/(4π) L. If an initial residual volume V₀ is included, the total-volume average is V₀+5/(4π).','The average flow rate over a full cycle is zero, but the average added lung volume is positive.',[num('Average added volume',5/(4*S.pi),1e-8,'L')])
add('6.5',24,'f_avg≥f((a+b)/2); the inequality is strict for a strictly convex, nonaffine curve as drawn.','Let m=(a+b)/2 and use the tangent-line inequality f(x)≥f(m)+f′(m)(x−m) for a differentiable convex function. Integrate on [a,b]. The linear term integrates to zero by symmetry about m, so ∫f≥(b−a)f(m), and division by b−a proves the claim. If the curve is strictly above the tangent on a nonzero-length portion, the inequality is strict. An affine function gives equality, so strict > requires the corresponding strict-curvature assumption.','The diagram supports the strict case. Weak convexity alone implies ≥, not always >.',[choice('Conclusion','The average is at least the midpoint value, and strictly greater under strict convexity.','The average is always less than the midpoint value.','Every affine function gives a strict > inequality.')],True)
add('6.5',25,'There exists c∈(a,b) with f(c)=f_avg.','For continuous f, define F(x)=∫ₐˣf(t)dt. The Fundamental Theorem gives F′(x)=f(x). The ordinary Mean Value Theorem on [a,b] gives F′(c)=[F(b)−F(a)]/(b−a) for some interior c. Since F(a)=0, the right side is (1/(b−a))∫ₐᵇf(t)dt=f_avg.','Continuity of f makes F differentiable and supplies the theorem hypotheses.',[choice('Proof','Apply the ordinary Mean Value Theorem to F(x)=∫ₐˣf(t)dt, using F′=f.','Apply the theorem without continuity assumptions on f.','Assume every function equals its average everywhere.')],True)
add('6.5',26,'f_avg[a,b]=[(c−a)/(b−a)]f_avg[a,c]+[(b−c)/(b−a)]f_avg[c,b].','Split ∫ₐᵇf=∫ₐᶜf+∫ᶜᵇf. Each subinterval integral is its width times its own average, so substitute (c−a)f_avg[a,c] and (b−c)f_avg[c,b]. Divide by b−a to obtain the displayed weighted average.','The weights are positive and sum to 1; the unweighted mean works only when the subinterval widths are equal.',[choice('Weights','(c−a)/(b−a) and (b−c)/(b−a).','1/2 and 1/2 for every c.','c−a and b−c without division.')],True)
baseball='-project-applied-project-calculus-and-baseball-1'
add('6.5','1'+baseball,'Ball impulse −275/96≈−2.864583 slug·ft/s; average force on the bat +34375/12≈2864.583 lbf (positive from pitcher to batter).','For constant mass, p′=mv′=ma=F, so integrating gives p(t₁)−p(t₀)=∫Fdt. Choose positive from pitcher toward batter. The incoming speed is +90·5280/3600=132 ft/s and outgoing velocity is −110·5280/3600=−484/3 ft/s. The weight is 5/16 lbf, so mass=(5/16)/32=5/512 slug. Hence the ball momentum change is (5/512)(−484/3−132)=−275/96 slug·ft/s. Divide by 0.001 s to obtain average force on the ball −34375/12 lbf. Newton’s third law makes the average force on the bat equal and opposite: +34375/12 lbf.','Weight in ounces must first become pounds-force; divide by g to obtain slugs. The question asks force on the bat, not force on the ball.',[choice('a · impulse identity','p(t₁)−p(t₀)=∫ from t₀ to t₁ F(t)dt.','p(t₁)=F(t₁).','Impulse is always zero.'),num('b(i) · ball momentum change',-S.Rational(275,96),.0001,'slug·ft/s'),num('b(ii) · force on bat',S.Rational(34375,12),.1,'lbf')],True)
add('6.5','2'+baseball,'Work 85.078125 ft·lbf.','With F=ma=mv dv/ds, integrate Fds=∫mvdv=(1/2)mv₁²−(1/2)mv₀², proving the work–energy relation. For a ball starting from rest, mass is (5/16)/32=5/512 slug and 90 mi/h=132 ft/s. Thus W=(1/2)(5/512)(132²)=85.078125 ft·lbf.','Use the ball’s speed change in kinetic energy; the bat-collision contact time is irrelevant to this throwing-work calculation.',[choice('a · work identity','W=(1/2)m(v₁²−v₀²).','W=m(v₁−v₀).','W=(1/2)m(v₁−v₀).'),num('b',S.Rational(10890,128),1e-6,'ft·lbf')],True)
direct=-10*mp.log(mp.mpf('.72'))
def relay(u):
 location=5*u-360
 duration=mp.mpf('.5')-10*mp.log((720+location)/1000)-10*mp.log((10*u-location)/(10*u))
 return float(location),float(duration)
x105,t105=relay(105);x115,t115=relay(115)
threshold=float(mp.findroot(lambda speed:relay(speed)[1]-float(direct),(110,115)))
add('6.5','3'+baseball,f'Direct {float(direct):.8f} s. For 105 ft/s: relay position {x105:g} ft, time {t105:.8f} s; direct is faster. For 115 ft/s: position {x115:g} ft, time {t115:.8f} s; relay is faster. Equal-time speed {threshold:.8f} ft/s.','Solving dv/dt=−v/10 with v(0)=V gives v=Ve^(−t/10) and distance d=10V(1−e^(−t/10)), so flight time is −10ln[1−d/(10V)]. A direct 280-ft throw with V=100 ft/s takes −10ln0.72≈'+f'{float(direct):.8f}'+' s. If the shortstop stands x feet from home and throws at speed U, total time is T(x)=0.5−10ln[(720+x)/1000]−10ln[(10U−x)/(10U)]. Set T′=−10/(720+x)+10/(10U−x)=0 to get x=5U−360; T″ is positive, so this is the minimum when 0≤x≤280. At U=105, x=165 and T≈'+f'{t105:.8f}'+', slower than direct. At U=115, x=215 and T≈'+f'{t115:.8f}'+', faster. For equal times solve (360+5U)²/(10000U)=0.72e^0.05 and retain the root in the physical interval 72≤U≤128, yielding U≈'+f'{threshold:.8f}'+'.','The relay handling delay of 0.5 s is separate from both flight times. The model ignores vertical motion as instructed.',[num('a · direct time',float(direct),1e-5,'s'),num('b · location at 105 ft/s',x105,1e-5,'ft from home'),num('b · time at 105 ft/s',t105,1e-5,'s'),choice('b · preferred at 105 ft/s','Direct throw.','Relayed throw.','They have equal times.'),num('b · location at 115 ft/s',x115,1e-5,'ft from home'),num('b · time at 115 ft/s',t115,1e-5,'s'),choice('b · preferred at 115 ft/s','Relayed throw.','Direct throw.','They have equal times.'),num('c · equal-time speed',threshold,.0001,'ft/s')],True)
movies='-project-applied-project-where-to-sit-at-the-movies-2'
angle=mp.pi/9
sa,ca=mp.sin(angle),mp.cos(angle)
def theta(z):return mp.atan((31-z*sa)/(9+z*ca))-mp.atan((6-z*sa)/(9+z*ca))
def theta_prime(z):
 H=9+z*ca
 return (9*sa+6*ca)/(H*H+(6-z*sa)**2)-(9*sa+31*ca)/(H*H+(31-z*sa)**2)
xopt=float(mp.findroot(theta_prime,(3,15)))
rows=[float(theta(3*i)) for i in range(21)];best=max(range(21),key=rows.__getitem__);avgangle=float(mp.quad(theta,[0,60])/60)
maxangle=float(theta(xopt));minangle=float(min(theta(0),theta(60)))
add('6.5','1'+movies,'The displayed law-of-cosines formula holds, with a and b the top/bottom sightline lengths.','At seating distance x up the 20° incline, horizontal distance to the screen is H=9+xcosα and eye height is 4+xsinα ft. The top screen edge is at 35 ft and the bottom at 10 ft, so vertical differences are 31−xsinα and 6−xsinα. Pythagoras gives a²=H²+(31−xsinα)² and b²=H²+(6−xsinα)². The triangle between the sightlines has opposite side 25 ft. The cosine rule gives cosθ=(a²+b²−25²)/(2ab), and taking arccos proves the formula.','Angles are in radians for calculus; the fixed inclination is α=20°=π/9. Eye height and the first-row screen offset must both be included.',[choice('Sightline geometry','a²=(9+xcosα)²+(31−xsinα)²; b²=(9+xcosα)²+(6−xsinα)².','a²=x²+35²; b²=x²+10².','a=b for every seat.'),choice('Angle formula','θ=arccos[(a²+b²−625)/(2ab)].','θ=arccos[(a²+b²+625)/(2ab)].','θ=arccos[(a+b−25)/(2ab)].')],True)
add('6.5','2'+movies,f'Continuous maximum near x={xopt:.8f} ft; best discrete seat row {best+1}, x={3*best} ft, viewing angle {math.degrees(rows[best]):.8f}°.','A convenient equivalent formula is θ(x)=atan[(31−xsinα)/(9+xcosα)]−atan[(6−xsinα)/(9+xcosα)]. Plot this on 0≤x≤60. The continuous peak is near x='+f'{xopt:.8f}'+'. Seats occur only at x=0,3,…,60. Evaluate the neighboring rows and all endpoints; the maximum discrete value occurs at x='+str(3*best)+', row '+str(best+1)+', with viewing angle '+f'{math.degrees(rows[best]):.8f}'+' degrees.','The continuous optimum is not necessarily a seat row; row 1 corresponds to x=0.',[num('Graph estimate of continuous x',xopt,.5,'ft'),num('Best row',best+1,.01),num('Viewing angle in that row',math.degrees(rows[best]),.01,'degrees')],True)
add('6.5','3'+movies,f'θ′=0 at x≈{xopt:.10f} ft.','Write s=sinα,c=cosα,H=9+cx, Yₜ=31−sx and Yᵦ=6−sx. Differentiating atan(Y/H) gives (Y′H−YH′)/(H²+Y²). Hence θ′=(9s+6c)/(H²+Yᵦ²)−(9s+31c)/(H²+Yₜ²). Numerically solving this expression on [0,60] gives x≈'+f'{xopt:.10f}'+'. The derivative changes from positive to negative there; comparison with endpoints confirms the continuous maximum and supports the row selection in Problem 2.','Use radian derivatives; differentiating a degree-valued angle changes its derivative by a constant factor but not the maximizing x.',[num('Stationary x',xopt,1e-5,'ft')],True)
add('6.5','4'+movies,f'Average angle {avgangle:.10f} rad ({math.degrees(avgangle):.8f}°); minimum {minangle:.10f} rad; maximum {maxangle:.10f} rad.','Numerically integrate the continuous viewing-angle formula from 0 to 60 and divide by 60: θ_avg=(1/60)∫₀⁶⁰θ(x)dx≈'+f'{avgangle:.10f}'+' rad. The minimum occurs at the farther endpoint, while the maximum is at the interior stationary point. Numerically these are '+f'{minangle:.10f}'+' and '+f'{maxangle:.10f}'+' rad. The average lies strictly between them. A graph-area estimate near this value is consistent with the numerical integration.','This is the average over the continuous interval along the incline, as requested, rather than the arithmetic mean of the 21 discrete seat-row angles.',[num('Average angle',avgangle,1e-5,'rad'),num('Minimum angle',minangle,1e-5,'rad'),num('Maximum angle',maxangle,1e-5,'rad')],True)
# Preserve source variable names in the closed-response formulas.
source_variables={4:'θ',6:'t',10:'t',11:'t',12:'θ',14:'y',15:'θ',16:'r',17:'u',20:'z',23:'θ',28:'t',29:'t',33:'t',36:'t',38:'t',42:'t',50:'θ'}
import re
for number,var in source_variables.items():
 r=records[f'calculus-section-5-5-{number}'];v=S.Symbol(var,real=True);F=primitives[number][1]
 r['fields']=[formula('Antiderivative',F.subs(x,v),True)]
 r['finalText']=fmt(F.subs(x,v))+' + C'
 # Use a consistent reading convention in the derivation, while grading the source variable.
 r['working']=r['working'].replace('F(x)=','F('+var+')=')
 r['working']=r['working'].replace(fmt(F),fmt(F.subs(x,v))).replace(fmt(primitives[number][0]),fmt(primitives[number][0].subs(x,v)))
 r['working']=re.sub(r' Here x (?:in the formula )?represents (?:the source variable )?[^.]*\.','',r['working'])
records['calculus-section-5-5-54']['fields'][0]['tolerance']=.01

# Correct a reviewed limit whose previous native transcription used the wrong approach point.
add('2.3',3,'105.','The source asks x→3, not x→2. Since the expression is a polynomial, apply continuity and the finite sum/power laws: 5·3³−3·3²+3−6=135−27+3−6=105.','The approach point comes from the original exercise artwork; substituting 2 would solve a different question.',[num('Limit',105)])

records['calculus-section-5-5-17']['working']=records['calculus-section-5-5-17']['working'].replace('Set u=1−eᵘ.','Set w=1−eᵘ.')
records['calculus-section-5-5-45']['working']='Split (1+x)/(1+x²) into 1/(1+x²)+x/(1+x²). The first integral is arctan x. For the second, use u=1+x² and du=2x dx, giving (1/2)ln(1+x²). Thus F(x)=arctan x+(1/2)ln(1+x²)+C. Differentiating gives 1/(1+x²)+x/(1+x²), recovering the integrand.'
records['calculus-section-6-5-8']['working']='The source variable is u. Its average on [1,5] is (1/4)∫₁⁵(ln u)/u du. Put w=ln u and dw=du/u; the transformed endpoints are 0 and ln5. Thus the integral is [w²/2]₀^(ln5)=(ln5)²/2. Divide by width 4 to obtain (ln5)²/8.'
