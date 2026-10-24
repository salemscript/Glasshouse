from common import *
R=s.Rational
# Printed pages355–357, visually reviewed, including shared instructions and conditions.
functions={1:4*x+7,2:x*x-3*x+2,3:2*x**3-R(2,3)*x*x+5*x,4:6*x**5-8*x**4-9*x*x,5:x*(12*x+8),6:(x-5)**2,7:7*x**R(2,5)+8*x**R(-4,5),8:x**R(17,5)-2*x**(s.sqrt(2)-1),9:s.sqrt(2),10:s.exp(2),11:3*s.sqrt(x)-2*x**R(1,3),12:x**R(2,3)+x*s.sqrt(x),13:R(1,5)-2/x,14:(3*x**4-x**3+6*x*x)/x**4,15:(1+x+x*x)/s.sqrt(x),16:s.sec(x)*s.tan(x)-2*s.exp(x),17:2*s.sin(x)-s.sec(x)**2,18:2*s.cos(x)-3/s.sqrt(1-x*x),19:2**x+4*s.sinh(x),20:1+2*s.sin(x)+3/s.sqrt(x),21:(2*x**4+4*x**3-x)/x**3,22:(2*x*x+5)/(x*x+1)}
for k,f in functions.items():
 F=s.integrate(s.expand(f),x)
 # Use ln|x| on disconnected real domains; the arbitrary constant is per component.
 check(f'4.9#{k} derivative',s.diff(F,x)-f)
 var={14:'t',15:'t',16:'θ',17:'θ',18:'v'}.get(k,'x');e=F.subs(x,s.Symbol(var,real=True))
 field=expr('Most general antiderivative',e,s.Symbol(var,real=True),' + C')
 if k in (13,14):
  for key in ('answer','options'):
   if key=='answer':field[key]=field[key].replace('ln('+var+')','ln|'+var+'|')
   else:field[key]=[v.replace('ln('+var+')','ln|'+var+'|') for v in field[key]]
 row(9,k,field,why='Integrate each power or standard derivative in the stated real domain, adding an arbitrary constant on each connected domain interval. Differentiation reproduces the original function.')
for k,f,at,value in [(23,5*x**4-2*x**5,0,4),(24,4-3/(1+x*x),1,0)]:
 F=s.integrate(f,x);F+=value-F.subs(x,at);check(str(k),s.diff(F,x)-f)
 row(9,k,expr('F(x)',F),c('Graph relationship','F increases where f>0 and decreases where f<0; F′=f','F and f must have identical graphs','F has the same zeros as f'),why='Integrate f and set the constant using the supplied value of F. The slope of the antiderivative graph is the original function.',limited=True)
for k,order,f in [(25,2,20*x**3-12*x*x+6*x),(26,2,x**6-4*x**4+x+1),(27,2,2*x+3*s.exp(x)),(28,2,1/x**2),(29,3,12+s.sin(x)),(30,3,s.sqrt(x)-2*s.cos(x))]:
 F=f
 for _ in range(order):F=s.integrate(F,x)
 check(str(k),s.diff(F,x,order)-f)
 F=fmt(F).replace('ln(x)','ln|x|');const=' + C₁x + C₂' if order==2 else ' + C₁t² + C₂t + C₃'
 if order==3:F=F.replace('x','t')
 row(9,k,c('General f',F+const,F+' + C',F+' + C₁'+('x²' if order==2 else 't³')+' + C₂'),why=f'Integrate {order} times; each integration introduces an independent constant. The arbitrary polynomial has degree at most {order-1}.')
first={31:(1+3*s.sqrt(x),4,25),32:(5*x**4-3*x*x+4,-1,2),33:(4/(1+x*x),1,0),34:(x+x**-3,1,6),35:(5*x**R(2,3),8,21),36:((x+1)/s.sqrt(x),1,5),37:(s.sec(x)*(s.sec(x)+s.tan(x)),s.pi/4,-1)}
for k,(f,at,val) in first.items():
 F=s.integrate(f,x);F=s.simplify(F+val-F.subs(x,at));check(str(k),s.diff(F,x)-f);check(str(k)+' condition',F.subs(x,at)-val)
 var='t' if k in (33,34,37) else 'x';v=s.Symbol(var,real=True)
 row(9,k,expr('f('+var+')',F.subs(x,v),v),why='Integrate the supplied derivative and solve the given point condition for the constant; differentiation and substitution both verify the result.')
row(9,38,c('f(t), separately on t>0 and t<0','3^t/ln3 − 3ln|t| + 2−3/ln3 for t>0; 3^t/ln3 − 3ln|t| + 1−1/(3ln3) for t<0','3^t/ln3 − 3ln|t| + 2−3/ln3 on both intervals','3^t − 3ln|t| + 2 on both intervals'),why='The derivative is undefined at zero, so the positive and negative domain components have independent constants. Apply f(1)=2 and f(−1)=1 separately.')
second={39:(-2+12*x-12*x*x,[(0,0,4),(1,0,12)]),40:(8*x**3+5,[(0,1,0),(1,1,8)]),41:(s.sin(x)+s.cos(x),[(0,0,3),(1,0,4)]),42:(x*x+1/x**2,[(0,2,3),(1,1,2)]),43:(4+6*x+24*x*x,[(0,0,3),(0,1,10)]),44:(x**3+s.sinh(x),[(0,0,1),(0,2,R(26,10))]),45:(s.exp(x)-2*s.sin(x),[(0,0,3),(0,s.pi/2,0)]),46:(x**R(1,3)-s.cos(x),[(0,0,2),(0,1,2)]),47:(x**-2,[(0,1,0),(0,2,0)])}
for k,(f,conditions) in second.items():
 A,B=s.symbols('A B'); F=s.integrate(s.integrate(f,x),x)+A*x+B
 sol=s.solve([s.diff(F,x,o).subs(x,t)-v for o,t,v in conditions],[A,B]);F=s.simplify(F.subs(sol));check(str(k),s.diff(F,x,2)-f)
 for o,t,v in conditions:check(str(k)+' condition',s.diff(F,x,o).subs(x,t)-v)
 var='t' if k in (42,46) else 'θ' if k==41 else 'x';v=s.Symbol(var,real=True)
 row(9,k,expr('f('+var+')',F.subs(x,v),v),why='Integrate twice and solve both source conditions for the two constants. The second derivative and both conditions independently reproduce the givens.')
F=-s.sin(x)+R(3,2)*x*x+3*x+1;check('48',s.diff(F,x,3)-s.cos(x))
row(9,48,expr('f(x)',F),why='Three integrations introduce a quadratic; f(0)=1,f′(0)=2,f″(0)=3 determine its coefficients.')
row(9,49,n('f(1)',8),why='f=3x−2x²+C; f(2)=5 gives C=7, so f(1)=8.')
row(9,50,c('f(x)','x⁴/4+3/4','x⁴/4−3/4','x⁴/4'),why='Tangency to y=−x requires x³=−1, so x=−1 and f(−1)=1. Thus C=3/4.')
row(9,51,c('Antiderivative graph','b','a','c'),c('Reason','Its slope is negative where f<0, zero where f=0, and positive where f>0','Its height always equals f','It is decreasing everywhere'),why='The blue b curve has precisely the required slope signs.',limited=True)
row(9,52,c('Antiderivative graph','a','b','c'),c('Reason','It rises while f>0, has a maximum where f crosses zero, then falls while f<0','It has a minimum at the zero of f','It is increasing everywhere'),why='The black a curve matches f as its derivative.',limited=True)
row(9,53,n('F(0)',1),c('Monotonicity','Decreases on (0,2), increases on (2,3), decreases after3','Increases on (0,2), decreases on (2,3), increases after3','Always decreases'),c('Local extrema','Minimum at x=2; maximum at x=3','Maximum at x=2; minimum at x=3','No local extrema'),why='Read f’s signs from the graph; F′=f and the required initial height is1.',limited=True)
row(9,54,c('Position behavior','Rises, becomes flat, falls, then becomes flat again','Falls, becomes flat, rises, then becomes flat again','Position equals the velocity graph'),c('Slope during positive velocity plateau','Constant positive slope','Zero slope','Constant negative slope'),why='Position is an antiderivative of velocity; the vertical offset is arbitrary.',limited=True)
row(9,55,c('Continuous f(x)','2x−1 for0≤x≤1; x for1≤x≤2; 4−x for2≤x≤3','2x−1 for0≤x≤1; x−1 for1≤x≤2; −x−1 for2≤x≤3','2x for0≤x≤1; x for1≤x≤2; −x for2≤x≤3'),why='Start at(0,−1), use slopes2,1,−1 and match values at both joins.',limited=True)
row(9,56,c('(c) F(x)','x²−2x^(3/2)+1','x²−3x^(3/2)+1','2x²−2x^(3/2)+1'),c('(a,b,d) shape','F decreases for0<x<9/4 and increases for x>9/4','F always increases','F has a maximum at9/4'),why='Integrate2x−3√x; the initial value supplies+1. Factor F′=√x(2√x−3).',limited=True)
row(9,57,c('Symmetry of F through the origin','Even','Odd','Neither'),c('Extrema in the interior','Minimum at0 and maxima at±π','Maximum at0 and minima at±π','No extrema'),why='f is odd, so its antiderivative through0 is even. Signs of sinx determine monotonicity; the denominator is positive.',limited=True)
row(9,58,c('Symmetry of F through the origin','Odd','Even','Neither'),c('Stationary points','x=±√(1+√3)','x=±1','x=0 only'),c('Classification','Maximum at−√(1+√3), minimum at+√(1+√3)','Minimum at−√(1+√3), maximum at+√(1+√3)','Both maxima'),why='f is even; solve√(x⁴−2x²+2)=2 and inspect the sign on the source interval.',limited=True)
for k,v,at,val in [(59,s.sin(x)-s.cos(x),0,0),(60,x*x-3*s.sqrt(x),4,8)]:
 F=s.integrate(v,x);F=s.simplify(F+val-F.subs(x,at));check(str(k),s.diff(F,x)-v);t=s.Symbol('t',real=True)
 row(9,k,expr('s(t)',F.subs(x,t),t),why='Integrate velocity and apply the stated position condition.')
for k,a,conditions in [(61,2*x+1,[(0,0,3),(1,0,-2)]),(62,3*s.cos(x)-2*s.sin(x),[(0,0,0),(1,0,4)]),(63,10*s.sin(x)+3*s.cos(x),[(0,0,0),(0,2*s.pi,12)]),(64,x*x-4*x+6,[(0,0,0),(0,1,20)])]:
 A,B=s.symbols('A B');F=s.integrate(s.integrate(a,x),x)+A*x+B;sol=s.solve([s.diff(F,x,o).subs(x,t)-v for o,t,v in conditions],[A,B]);F=s.simplify(F.subs(sol));check(str(k),s.diff(F,x,2)-a);t=s.Symbol('t',real=True)
 row(9,k,expr('s(t)',F.subs(x,t),t),why='Integrate acceleration twice and enforce the two position/velocity conditions.')
row(9,65,c('(a) height above ground','450−4.9t² m','450−9.8t² m','4.9t² m'),n('(b) impact time',math.sqrt(900/9.8),'s',.005),n('(c) upward-signed impact velocity',-math.sqrt(2*9.8*450),'m/s',.01),n('(d) time when thrown downward at5m/s',(-5+math.sqrt(25+4*4.9*450))/(2*4.9),'s',.005),why='Assume constant gravity9.8m/s² and no air resistance. Integrate acceleration, then solve height=0 for the positive time.')
row(9,66,c('Velocity after integration','v(t)=at+v₀','v(t)=at²+v₀','v(t)=a+v₀t'),c('Position after integration','s(t)=at²/2+v₀t+s₀','s(t)=at²+v₀t+s₀','s(t)=at+v₀+s₀'),why='Integrating constant acceleration gives velocity; integrating velocity gives position, with the initial conditions fixing both constants.',limited=True)
row(9,67,c('Intermediate expressions','v=v₀−9.8t; s−s₀=v₀t−4.9t²','v=v₀+9.8t; s−s₀=v₀t+4.9t²','v=v₀−4.9t; s−s₀=v₀t−9.8t²'),c('Elimination result','v²=v₀²−19.6(s−s₀)','v²=v₀²+19.6(s−s₀)','v=v₀−19.6(s−s₀)'),why='Square the velocity expression and eliminate time using the displacement expression; upward is positive.',limited=True)
row(9,68,c('Do they pass before impact?','Yes','No'),n('Time since the first launch',5,'s'),n('Height when they meet',272,'ft'),why='Source Example7 has cliff height432ft. Positions are432+48t−16t² and432+24(t−1)−16(t−1)²; equality gives t=5 and height272ft.')
row(9,69,n('Cliff height',225,'ft'),why='With g=32ft/s² and initial speed0, v²=2gh gives h=120²/64.')
row(9,70,c('(a) f(x)','g/[EI] · [m(Lx²/2−x³/6)+ρ(L²x²/4−Lx³/6+x⁴/24)]','g/[EI] · [m(Lx−x²/2)+ρ(L²x/2−Lx²/2+x³/6)]','g/[EI] · [m(Lx²−x³/3)+ρL²x²]'),c('(b) distance below horizontal','−g/[EI] · (mL³/3+ρL⁴/8)','g/[EI] · (mL³/3+ρL⁴/8)','−g/[EI] · (mL²/2+ρL³/6)'),why='Use the clamped-end conditions f(0)=f′(0)=0 shown in the diagram. Integrate twice; since g<0 the downward distance is−f(L).')
row(9,71,n('Cost of100items',742.081,'dollars',.005),why='C(100)−C(1)=1.92(99)−0.001(10000−1); add the given$562 cost of one item.')
row(9,72,n('Mass',20,'g'),why='Use100cm, not1, for the upper limit. The integral of x^(−1/2) from0 to100 is2√100=20; the endpoint singularity is integrable.')
row(9,73,n('Fall time',10+100/55,'s',.005),why='Downward v=10+9t−0.45t² and distance=10t+4.5t²−0.15t³ until10s. Then distance400m and speed55m/s, leaving100m at constant speed.')
row(9,74,n('Stopping distance',(50*5280/3600)**2/44,'ft',.01),why='Convert50mi/h to220/3ft/s and use distance=v₀²/(2·22).')
row(9,75,n('Acceleration',(20*5280/3600)/5,'ft/s²',.005),why='Acceleration is change in velocity divided by5s; convert mi/h toft/s first.')
row(9,76,n('Initial speed',math.sqrt(2*16*200)*3600/5280,'mi/h',.01),why='v₀²=2(16)(200), giving80ft/s, then convert to mi/h.')
row(9,77,n('Minimum deceleration magnitude',(100/3.6)**2/160,'m/s²',.005),why='With no reaction-time delay, stopping distance=v₀²/(2a)≤80m; convert100km/h to250/9m/s.')
row(9,78,c('(a) v(t), in ft/s','30t² for0≤t≤3; 270−32(t−3) for3≤t≤17; −178+32(t−17) for17≤t≤22; −18 for22≤t≤22+424/18','60t for0≤t≤3; 180−32(t−3) thereafter','30t² for0≤t≤3; 270−32t for3≤t≤17; −18 thereafter'),c('(a) s(t), in feet','10t³ for0≤t≤3; 270+270(t−3)−16(t−3)² for3≤t≤17; 914−178(t−17)+16(t−17)² for17≤t≤22; 424−18(t−22) thereafter until landing','10t³ for0≤t≤3; 270t−16t² for3≤t≤17; 424−18t thereafter','30t³ for0≤t≤3; 914−18(t−17) thereafter'),n('(b) time of maximum height',3+270/32,'s'),n('(b) maximum height',270+270**2/64,'ft'),n('(c) landing time',22+424/18,'s',.005),why='Integrate each acceleration segment and match both position and velocity at3,17,22s. At17s s=914ft,v=−178ft/s; at22s s=424ft,v=−18ft/s. Set v=0 for the peak.',limited=True)
row(9,79,n('(a) maximum distance',(132**2/8+132*900)/5280,'mi'),n('(b) maximum distance',132*(900-33)/5280,'mi'),n('(c) minimum trip time',45*5280/132+33,'s'),n('(d) distance',132*(37.5*60-33)/5280,'mi'),why='90mi/h=132ft/s; acceleration and braking each take33s. For a total trip timeT≥66s, distance=132(T−33)ft. Part(a) adds15min cruising after the initial acceleration.')
finish('section09')
