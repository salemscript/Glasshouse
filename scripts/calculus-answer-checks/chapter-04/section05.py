from common import *
from curve import curve
R=s.Rational
# Every expression below was transcribed from printed321–323, not OCR inference.
def realzeros(e):
 roots=s.solve(s.together(e).as_numer_denom()[0],x)
 return sorted([z for z in roots if z.is_real],key=lambda z:float(z))
functions={1:x**3+3*x*x,2:2+3*x*x-x**3,3:x**4-4*x,4:x**4-8*x*x+8,5:x*(x-4)**3,6:x**5-5*x,7:x**5/5-R(8,3)*x**3+16*x,8:(4-x*x)**5,9:x/(x-1),10:(x*x+5*x)/(25-x*x),11:(x-x*x)/(2-3*x+x*x),12:1+1/x+1/x**2,13:x/(x*x-4),14:1/(x*x-4),15:x*x/(x*x+3),16:(x-1)**2/(x*x+1),17:(x-1)/x**2,18:x/(x**3-1),19:x**3/(x**3+1),20:x**3/(x-2),65:x*x/(x-1),66:(1+5*x-2*x*x)/(x-2),67:(x**3+4)/x**2,68:x**3/(x+1)**2,74:(x**3+1)/x,75:(x**4+1)/x}
exclusions={9:[1],10:[-5,5],11:[1,2],12:[0],13:[-2,2],14:[-2,2],17:[0],18:[1],19:[-1],20:[2],65:[1],66:[2],67:[0],68:[-1],74:[0],75:[0]}
for k,f in functions.items():
 exc=exclusions.get(k,[]);cr=[v for v in realzeros(s.diff(f,x)) if v not in exc];ip=[v for v in realzeros(s.diff(f,x,2)) if v not in exc]
 desc=[]
 for a in exc:
  ll=s.limit(f,x,a,dir='-');rr=s.limit(f,x,a,dir='+')
  if ll in [s.oo,-s.oo] or rr in [s.oo,-s.oo]:desc.append('vertical x='+str(a))
  else:desc.append('hole at('+str(a)+','+fmt(ll)+')')
 quotient,remainder=s.div(*s.cancel(f).as_numer_denom(),x)
 if s.degree(remainder,x)<s.degree(s.cancel(f).as_numer_denom()[1],x) and s.degree(quotient,x)>=0 and s.degree(s.cancel(f).as_numer_denom()[1],x)>0:desc.append(('horizontal ' if not quotient.has(x) else 'asymptotic curve ')+'y='+fmt(quotient))
 curve(5,k,f,cr,ip,excluded=exc,asym='; '.join(desc) or None)
curve(5,21,(x-3)*s.sqrt(x),[1],[],domain=(0,s.oo))
curve(5,23,s.sqrt(x*x+x-2),[],[],domain=(-s.oo,-2))
# Two disconnected square-root branches, so supply the complete feature contract explicitly.
OUT.pop('calculus-section-4-5-23');AUDIT.pop('calculus-section-4-5-23')
row(5,23,c('Domain','(−∞,−2] ∪ [1,∞)','[−2,1]','All realx'),c('Monotonicity','Decreasing on(−∞,−2), increasing on(1,∞)','Increasing on both branches','Decreasing on both branches'),c('Concavity','Concave down on both branches; no inflection','Concave up everywhere','Inflection at−1/2'),c('Asymptotes','y=−x−1/2 at−∞; y=x+1/2 at+∞','y=0','Verticalx=−2,1'),c('Intercepts','(−2,0) and(1,0); no y-intercept','(0,0)','No intercepts'),why='The radicand(x+2)(x−1) must be nonnegative. f′=(2x+1)/(2√radicand) and f″=−9/(4radicand^(3/2)); the endpoint vertical tangents are not vertical asymptotes.',limited=True)
row(5,24,c('Domain','(−∞,−1] ∪ [0,∞)','[−1,0]','All realx'),c('Monotonicity','Decreasing onx<−1, increasing onx>0','Increasing on both branches','Decreasing on both branches'),c('Concavity','Concave down on both branches','Concave up on both branches','Inflection at−1/2'),c('Asymptotes','y=−2x−1/2 asx→−∞; y=1/2 asx→∞','y=−1/2 at both ends','Verticalx=−1,0'),c('Intercept','(0,0)','(−1,0)','None'),why='Requirex(x+1)≥0. Rationalization supplies the asymptotes; f″=−1/[4(x²+x)^(3/2)]<0 on both open branches.',limited=True)
curve(5,25,x/s.sqrt(x*x+1),[],[0],asym='Horizontaly=−1 at−∞ andy=1 at+∞')
curve(5,26,x*s.sqrt(2-x*x),[-1,1],[0],domain=(-s.sqrt(2),s.sqrt(2)))
row(5,27,c('Domain','[−1,0) ∪ (0,1]','[−1,1]','All nonzerox'),c('Monotonicity','Decreasing on both domain intervals','Increasing on both','Decreasing only forx>0'),c('Concavity','Down on(−1,−√(2/3)) and(0,√(2/3)); up on(−√(2/3),0) and(√(2/3),1)','Up everywhere','Down everywhere'),c('Inflection points','(−√(2/3),−1/√2) and(√(2/3),1/√2)','(0,0)','None'),c('Asymptote','Verticalx=0; no horizontal asymptote','Horizontaly=0','Verticalx=±1'),why='Forf=√(1−x²)/x, f′=−1/[x²√(1−x²)] and f″=(2−3x²)/[x³(1−x²)^(3/2)].',limited=True)
row(5,28,c('Domain','(−∞,−1) ∪ (1,∞)','(−1,1)','All nonzerox'),c('Monotonicity','Decreasing on both branches','Increasing on both','Constant'),c('Concavity','Down forx<−1; up forx>1; no inflection','Up on both','Inflection at0'),c('Asymptotes','Verticalx=±1; horizontaly=−1 at−∞ andy=1 at+∞','Verticalx=0; horizontaly=0','No asymptotes'),why='Differentiatex/√(x²−1): f′=−(x²−1)^(−3/2), f″=3x(x²−1)^(−5/2).',limited=True)
for k,inc,dec,ext,up,dn,ip,extra in [
(22,'(1,∞)','(−∞,0) ∪ (0,1)','Local minimum at(1,−3); no maximum','(−∞,−2) ∪ (0,∞)','(−2,0)','(−2,6∛2) and(0,0)','Domainℝ; zeros0,4; vertical tangent at0'),
(29,'(−∞,−1) ∪ (1,∞)','(−1,0) ∪ (0,1)','Local maximum(−1,2); local minimum(1,−2)','(0,∞)','(−∞,0)','(0,0)','Domainℝ; zeros−3√3,0,3√3; vertical tangent at0'),
(30,'(−∞,0) ∪ (2,∞)','(0,2)','Local maximum(0,0); local minimum(2,−3·2^(2/3))','(0,∞)','(−∞,0)','(0,0)','Domainℝ; zeros0,5'),
(31,'(0,∞)','(−∞,0)','Local minimum(0,−1)','(−1,1)','(−∞,−1) ∪ (1,∞)','(−1,0) and(1,0)','Domainℝ; vertical tangentsx=±1; no asymptotes'),
(32,'(−∞,−1) ∪ (−1,0) ∪ (0,∞)','None','No local extrema','(−∞,−1) ∪ (0,∞)','(−1,0)','(−1,0) and(0,1)','Domainℝ; slant asymptotey=x; vertical tangent at−1')]:
 row(5,k,c('Increasing',inc,dec,'(0,1) only'),c('Decreasing',dec,inc,'Allrealx'),c('Extrema',ext,'No local extrema' if ext!='No local extrema' else 'Maximumat0','Maximumat1'),c('Concave up',up,dn,'None'),c('Concave down',dn,up,'None'),c('Inflection points',ip,'None','(1,1)'),c('Domain / intercept / asymptote feature',extra,'Domainx>0 only','Every derivative singularity is a vertical asymptote'),why='Use real odd roots on negative arguments, then test derivative signs on every interval separated by stationary or vertical-tangent points. The original continuous function determines whether a concavity change is an inflection.',limited=True)
# Correct real-power concavity for #22, #30 below from exact derivatives.
q=OUT['calculus-section-4-5-22']['grader']['parts'];q[3]=c('Concave up','(−∞,−2) ∪ (0,∞)','(−2,0)','None');q[4]=c('Concave down','(−2,0)','(−∞,−2) ∪ (0,∞)','None')
q=OUT['calculus-section-4-5-30']['grader']['parts'];q[3]=c('Concave up','(−1,0) ∪ (0,∞)','(−∞,−1)','None');q[4]=c('Concave down','(−∞,−1)','(−1,0) ∪ (0,∞)','None');q[5]=c('Inflection points','(−1,−6)','(0,0)','None')
row(5,33,c('Monotonicity, repeated every2π','Increasing on(−π/2,π/2); decreasing on(π/2,3π/2)','Always increasing','Always decreasing'),c('Extrema','Maximum1 atπ/2+2kπ; minimum−1 at3π/2+2kπ','Maximum0 at kπ','No extrema'),c('Inflections in[0,2π)','x=0,α,π−α,π,π+α,2π−α; α=arcsin√(2/3)','Onlyx=π/2,3π/2','Onlyx=0,π'),c('Concavity sign rule','Sign of f″ equals sign[sinx·(2−3sin²x)]','Sign off″equals signcosx','f″is always positive'),why='f′=3sin²x cosx and f″=3sinx(2−3sin²x). The zero derivative at kπ does not change monotonicity.',limited=True)
row(5,34,c('Monotonicity','Strictly increasing onℝ','Strictly decreasing','Alternating everyπ'),c('Extrema','None','Maxima atπ/2+2kπ','Minima at3π/2+2kπ'),c('Inflections','(π/2+kπ,π/2+kπ), k∈ℤ','(kπ,kπ)','None'),c('Concavity','Up wherecosx<0; down wherecosx>0','Up wherecosx>0; down wherecosx<0','Always up'),why='f′=1−sinx≥0 with isolated zeros; f″=−cosx changes sign atπ/2+kπ.',limited=True)
curve(5,35,x*s.tan(x),[0],[],domain=(-s.pi/2,s.pi/2),asym='Verticalx=±π/2; even curve with minimum(0,0)')
curve(5,36,2*x-s.tan(x),[-s.pi/4,s.pi/4],[0],domain=(-s.pi/2,s.pi/2),asym='Verticalx=±π/2')
curve(5,37,s.sin(x)+s.sqrt(3)*s.cos(x),[-5*s.pi/6,s.pi/6,7*s.pi/6],[ -4*s.pi/3,-s.pi/3,2*s.pi/3,5*s.pi/3],domain=(-2*s.pi,2*s.pi))
# Include stationary point−11π/6, within source interval.
# Regenerate with complete critical list rather than letting a graph window hide it.
OUT.pop('calculus-section-4-5-37');AUDIT.pop('calculus-section-4-5-37');curve(5,37,s.sin(x)+s.sqrt(3)*s.cos(x),[-11*s.pi/6,-5*s.pi/6,s.pi/6,7*s.pi/6],[-4*s.pi/3,-s.pi/3,2*s.pi/3,5*s.pi/3],domain=(-2*s.pi,2*s.pi))
curve(5,38,1/s.sin(x)-2*s.sin(x),[s.pi/2],[],domain=(0,s.pi),asym='Verticalx=0,π')
row(5,39,c('Equivalent function with original domain','tan(x/2), excludingx=(2k+1)π','tanx for everyx','cot(x/2)'),c('Monotonicity','Increasing on every interval between consecutive poles','Decreasing on every interval','Constant'),c('Inflection points','(2kπ,0), k∈ℤ','((2k+1)π,0)','None'),c('Concavity','Down on((2k−1)π,2kπ); up on(2kπ,(2k+1)π)','Always up','Always down'),why='Use the half-angle identity; f′=(1/2)sec²(x/2)>0 and f″=(1/2)sec²(x/2)tan(x/2).',limited=True)
row(5,40,c('Period and domain','Period2π; all realx','Periodπ; poles atkπ','Not periodic'),c('Extrema in one period','Maximum1/√3 at2π/3; minimum−1/√3 at4π/3','Maximum1 atπ/2; minimum−1 at3π/2','No extrema'),c('Monotonicity','Increasing wherecosx>−1/2; decreasing wherecosx<−1/2','Increasing where sinx>0','Always increasing'),c('Inflections','(kπ,0), k∈ℤ','x=2π/3,4π/3','None'),c('Concavity','Down for2kπ<x<(2k+1)π; up for(2k+1)π<x<(2k+2)π','Up for0<x<π','Always down'),why='f′=(1+2cosx)/(2+cosx)² and f″=2sinx(cosx−1)/(2+cosx)³.',limited=True)
curve(5,41,s.atan(s.exp(x)),[],[0],asym='Horizontaly=0 at−∞,y=π/2 at+∞')
curve(5,42,(1-x)*s.exp(x),[0],[-1],asym='Horizontaly=0 at−∞ only')
curve(5,43,1/(1+s.exp(-x)),[],[0],asym='Horizontaly=0 at−∞,y=1 at+∞')
curve(5,44,s.exp(-x)*s.sin(x),[s.pi/4,5*s.pi/4],[s.pi/2,3*s.pi/2],domain=(0,2*s.pi))
curve(5,45,1/x+s.log(x),[1],[2],domain=(0,s.oo),asym='Verticalx=0')
curve(5,46,s.exp(2*x)-s.exp(x),[-s.log(2)],[-s.log(4)],asym='Horizontaly=0 at−∞')
curve(5,47,(1+s.exp(x))**-2,[],[-s.log(2)],asym='Horizontaly=1 at−∞,y=0 at+∞')
curve(5,48,s.exp(x)/x**2,[2],[],excluded=[0],asym='Verticalx=0; horizontaly=0 at−∞')
row(5,49,c('Domain','(2kπ,(2k+1)π), k∈ℤ','All realx','x>0'),c('Extrema','Maximum0 atπ/2+2kπ; no minima','Maximum1 atπ/2+2kπ','No extrema'),c('Monotonicity','Increasing on(2kπ,π/2+2kπ), decreasing on(π/2+2kπ,(2k+1)π)','Increasing everywhere','Decreasing everywhere'),c('Concavity','Down on every domain interval; no inflections','Up everywhere','Alternates atπ/2'),c('Asymptotes','Verticalx=kπ, approached from the domain side','Horizontaly=0','None'),why='Require sinx>0; f′=cotx and f″=−csc²x<0.',limited=True)
curve(5,50,s.log(1+x**3),[0],[0,2**R(1,3)],domain=(-1,s.oo),asym='Verticalx=−1')
curve(5,51,x*s.exp(-1/x),[-1],[],excluded=[0],asym='Verticalx=0 from the left; right-hand limit0; slanty=x−1 at±∞')
curve(5,52,s.log(x)/x**2,[s.sqrt(s.E)],[s.exp(R(5,6))],domain=(0,s.oo),asym='Verticalx=0; horizontaly=0 at+∞')
curve(5,53,s.exp(s.atan(x)),[],[R(1,2)],asym='Horizontaly=e^(−π/2) at−∞,y=e^(π/2) at+∞')
curve(5,54,s.atan((x-1)/(x+1)),[],[0],excluded=[-1],asym='Jump atx=−1 with one-sided limitsπ/2 and−π/2; horizontaly=π/4 at±∞; no vertical asymptote')
row(5,55,c('Physical speed domain','0≤v<c','All realv','v>c'),c('Behavior','Starts atm₀, increases and is concave up, diverges asv→c⁻','Decreases toward0','Has a maximum atv=c/2'),why='The square root requiresv<c for the physical nonnegative speed. Differentiation gives positive first and second derivatives for0<v<c.',limited=True)
row(5,56,c('Wavelength domain','λ>0','All realλ','λ<0 only'),c('Behavior','Strictly decreasing and concave up;E→∞ asλ→0⁺ andE→m₀c² asλ→∞','Increasing to∞ asλ grows','Energy tends0 asλ→∞'),why='E=√(A+B/λ²), withpositiveA=m₀²c⁴,B=h²c². E′<0 andE″>0 forλ>0.',limited=True)
row(5,57,c('(a) half-population time','t=ln(a)/k','t=ln(k)/a','t=a/k'),c('(b) unconstrained peak spread time','t=ln(a)/k','t=0 for everya','t=2ln(a)/k'),c('(c) graph','Increasing logistic curve, inflection atp=1/2, asymptotes0 and1','Decreasing exponential','A straight line'),c('If physical time is restricted tot≥0 and a<1','Half was reached beforet=0; the rate on t≥0 is greatest att=0','Half is reached at a positive time','The model has no values'),why='Differentiatep: p′=kp(1−p), maximal atp=1/2; solveae^(−kt)=1 and respect the chosen time domain.',limited=True)
row(5,58,c('Peak time','ln(b/a)/(b−a)','ln(a/b)/(b−a)','1/a'),c('Inflection time','2ln(b/a)/(b−a)','ln(b/a)/(b−a)','0'),c('Time evolution fort≥0','Starts0, rises to one peak, then falls toward0; concave down then up','Always increasing','Startsnegative and remainsnegative'),why='b>a>0 impliese^(−at)>e^(−bt) fort>0. SolveC′=0 andC″=0 separately.',limited=True)
row(5,59,c('Maximum downward deflection location','x=L/2','x=L/4','x=L'),c('Maximum downward deflection magnitude','WL⁴/(384EI)','WL³/(384EI)','WL⁴/(24EI)'),c('Inflection locations','x=L(3±√3)/6','x=L/2 only','x=0,L'),c('Boundary behavior','y=y′=0 atx=0,L; symmetric aboutL/2','Both endpoint slopes are nonzero','No symmetry'),why='Factor y=−W x²(x−L)²/(24EI). Derivatives give the midpoint minimum and two curvature changes.',limited=True)
row(5,60,c('Equilibrium','x=1','x=0','x=2'),c('Force direction','Negative(left) forx<1; positive(right) forx>1','Positive forx<1; negative forx>1','Alwaysnegative'),c('Graph','Strictly increasing, concave down on(0,1), up on(1,2), vertical asymptotes0,2','Strictly decreasing','No asymptotes'),c('Equilibrium stability','Unstable: a displacement increases force away from the midpoint','Stable: force restores the midpoint'),why='F′=2k/x³−2k/(x−2)³>0. Atx=1 the attractions cancel; closer to either positive charge, that attraction dominates.',limited=True)
for k,f in [(61,(x*x+1)/(x+1)),(62,(4*x**3-10*x*x-11*x+1)/(x*x-3*x)),(63,(2*x**3-5*x*x+3*x)/(x*x-x-2)),(64,(-6*x**4+2*x**3+3)/(2*x**3-x))]:
 q,r=s.div(*s.together(f).as_numer_denom(),x);row(5,k,expr('Slant asymptote y',q),why='Polynomial division givesf=q+remainder/denominator; the proper rational remainder tends0 at±∞.')
curve(5,69,1+x/2+s.exp(-x),[s.log(2)],[],asym='Slanty=1+x/2 asx→∞ only')
curve(5,70,1-x+s.exp(1+x/3),[3*s.log(3)-3],[],asym='Slanty=1−x asx→−∞ only')
curve(5,71,x-s.atan(x),[0],[0],asym='Slanty=x+π/2 at−∞,y=x−π/2 at+∞')
row(5,72,c('Domain','(−∞,−4] ∪ [0,∞)','[−4,0]','All realx'),c('Asymptotes','y=−x−2 at−∞ andy=x+2 at+∞','y=−x+2 andy=x−2','y=0'),c('Graph behavior','Both branches concave down; left branch decreases to(−4,0), right branch increases from(0,0)','Both branches concave up','A continuous curve through−2'),why='Rationalize the difference from each line. f′=(x+2)/√(x²+4x); f″=−4/(x²+4x)^(3/2)<0.',limited=True)
row(5,73,c('Asymptotic lines','y=±(b/a)x','y=±(a/b)x','y=±bx'),c('Limit argument','√(x²/a²−1)−|x|/a→0 as|x|→∞','The hyperbola meets the lines at everyx','The difference tends1'),why='Solve the hyperbola asy=±b√(x²/a²−1), then rationalize the difference; a,b are positive geometric parameters.',limited=True)
row(5,76,c('Right-end behavior','f(x)−sinx=e^(−x)→0 asx→∞','f(x)→0 asx→∞','f(x)→∞ asx→∞'),c('Left-end behavior','f(x)→∞ asx→−∞ with bounded sinusoidal modulation','f(x)→−∞','f(x)→0'),why='The exact difference fromsinx is the positive decaying exponential; there is no horizontal asymptote on the right because sinx keeps oscillating.',limited=True)
finish('section05')
