from helper10 import *
import scipy.integrate as si
import numpy as np
R=s.Rational;t=s.symbols('t',real=True);a,r,d=s.symbols('a r d',positive=True)
def ex(label,e):return expr(label,s.simplify(e),t)
def tangent(k,X,Y,T,limited=False):
 m=s.simplify(s.diff(Y,t).subs(t,T)/s.diff(X,t).subs(t,T));b=s.simplify(Y.subs(t,T)-m*X.subs(t,T))
 row(2,k,n('Tangent slope',m),n('Tangent y-intercept',b),why='At the specified source parameter, compute dy/dx=y′(t)/x′(t), then use y−y₀=m(x−x₀).',limited=limited)
for k,X,Y in [(1,t/(1+t),s.sqrt(1+t)),(2,t*s.exp(t),t+s.sin(t))]:row(2,k,ex('dy/dx',s.diff(Y,t)/s.diff(X,t)),why='Divide the derivative of y with respect to t by the derivative of x with respect to t, where x′≠0.')
for args in [(3,t**3+1,t**4+t,-1),(4,s.sqrt(t),t*t-2*t,4),(5,t*s.cos(t),t*s.sin(t),s.pi),(6,s.exp(t)*s.sin(s.pi*t),s.exp(2*t),0)]:tangent(*args)
for k,X,Y,T,cart in [(7,1+s.log(t),t*t+2,1,'y=e^(2(x−1))+2'),(8,1+s.sqrt(t),s.exp(t*t),1,'y=e^((x−1)^4), x≥1')]:
 m=s.diff(Y,t).subs(t,T)/s.diff(X,t).subs(t,T);b=s.simplify(Y.subs(t,T)-m*X.subs(t,T))
 row(2,k,n('Tangent slope (both methods)',m),n('Tangent y-intercept',b),c('Eliminated equation',cart,'y=x²','y=e^x'),why='Solve x(t) for t, preserving its domain, and differentiate the resulting Cartesian equation. This agrees with y′/x′.',limited=True)
tangent(9,t*t-t,t*t+t+1,1,True)
row(2,10,n('Tangent slope',-3/s.pi),n('Tangent y-intercept',2),c('Parameters reaching the given point','t=1 and t=−2; both give the same tangent','Only t=0','Two distinct tangent slopes'),why='Solve t²+t=2, then verify sinπt=0 for both t=1,−2. The slope (2t+1)/(πcosπt) equals−3/π at both.',limited=True)
for k,X,Y,up in [(11,t*t+1,t*t+t,'t<0'),(12,t**3+1,t*t-t,'0<t<1'),(13,s.exp(t),t*s.exp(-t),'t>3/2'),(14,t*t+1,s.exp(t)-1,'t<0 or t>1'),(15,t-s.log(t),t+s.log(t),'0<t<1'),(16,s.cos(t),s.sin(2*t),'π/2<t<π')]:
 m=s.simplify(s.diff(Y,t)/s.diff(X,t));dd=s.simplify(s.diff(m,t)/s.diff(X,t))
 row(2,k,ex('dy/dx',m),ex('d²y/dx²',dd),c('Concave upward',up,'All real t','No t'),why='Use y′/x′ for slope, then divide its t-derivative by x′ again. Solve d²y/dx²>0 on the source domain, excluding x′=0.')
 check('Q'+str(k)+' second derivative identity',dd*s.diff(X,t)-s.diff(m,t))
for k,h,v,why in [(17,'(0,−3)','(−2,−2) and (2,−2)','y′=2t vanishes at0; x′=3(t²−1) vanishes at±1.'),(18,'(0,0) and (2,−4)','(−2,−2) and (2,−4)','At t=0,2, y′=3t(t−2)=0; at t=±1, x′=3(t²−1)=0. The point(2,−4) occurs at t=2 horizontally and t=−1 vertically.'),(19,'(1/2,−1) and (−1/2,1)','None','Eliminate θ to get y=4x³−3x on−1≤x≤1. At θ multiples ofπ both parameter derivatives vanish, but the limiting slope is9, not vertical.'),(20,'(1,e) and (1,1/e)','(e,1) and (1/e,1)','y′=−sinθ e^(cosθ); x′=cosθ e^(sinθ). Their zero sets never overlap.')]:row(2,k,c('Horizontal-tangent points',h,'None','Only (0,0)'),c('Vertical-tangent points',v,'Every point','Only (0,1)'),why=why,limited=True)
T=6**(-R(1,5));row(2,21,n('Rightmost x',T-T**6,tol=.00005),n('Rightmost y',s.exp(T),tol=.00005),ex('Exact maximizing parameter',T),why='x′=1−6t⁵ changes from positive to negative at t=6^(−1/5). Substitute in both coordinates.',limited=True)
T=-4**(-R(1,3));U=2**(-R(1,3));row(2,22,n('Lowest point x',T**4-2*T,tol=.00005),n('Lowest point y',T+T**4,tol=.00005),n('Leftmost point x',U**4-2*U,tol=.00005),n('Leftmost point y',U+U**4,tol=.00005),why='Minimize y using1+4t³=0 and x using4t³−2=0 separately. Both quartics tend to∞ at either end.',limited=True)
for k,X,Y,window in [(23,t**4-2*t**3-2*t*t,t**3-t,'For example −12≤x≤15, −4≤y≤20, with −2≤t≤4'),(24,t**4+4*t**3-8*t*t,2*t*t-t,'For example −130≤x≤30, −1≤y≤50, with −6≤t≤3')]:
 crit=sorted(s.solve(s.diff(X,t),t),key=lambda z:float(z));fields=[c('A window showing the finite turns',window,'0≤x≤1,0≤y≤1 only','−1≤x≤0,−1≤y≤0 only')]
 for j,T in enumerate(crit):fields.extend([n('x-stationary point '+str(j+1)+' (ordered t): x',X.subs(t,T)),n('x-stationary point '+str(j+1)+' (ordered t): y',Y.subs(t,T))])
 row(2,k,*fields,why='Plot the actual polynomial parameterization; locate x-turns from x′=0 and retain both unbounded tails. Numerical feature checks supplement, but cannot assess, the plotted graph.',limited=True)
row(2,25,c('Tangent equations at origin','y=x and y=−x','Only y=0','x=0 and y=0'),c('Cartesian relation and range','y²=x²(1−x²), −1≤x≤1','y=x²','x²+y²=1'),why='At cos t=0 the two possible signs of sin t give slopes±1. Eliminate sin²t using1−cos²t.',limited=True)
row(2,26,n('Self-intersection x',1),n('Self-intersection y',0),c('Two tangent lines','y=(√3/2)(x−1) and y=−(√3/2)(x−1)','y=±x','Only y=0'),why='sin t(1+2cos t)=0; at cos t=−1/2 the two distinct parameters2π/3,4π/3 give(1,0). Slopes are∓√3/2.',limited=True)
row(2,27,c('(a) Slope','d sinθ/(r−d cosθ)','(r−d cosθ)/(d sinθ)','−tanθ'),c('(b) No vertical tangent when 0<d<r','x′=r−d cosθ≥r−d>0','y′ is never zero','x′=0 everywhere'),why='Differentiate both coordinates and divide. A strictly positive denominator excludes a vertical tangent.',limited=True)
row(2,28,c('(a) Slope','−tanθ','tanθ','−cotθ'),c('(b) Horizontal points','(±a,0)','(0,±a)','No points'),c('(b) Vertical points','(0,±a)','(±a,0)','No points'),c('(c) Slope +1','(a/(2√2),−a/(2√2)) and (−a/(2√2),a/(2√2))','The same signs in both coordinates','(±a,0)'),c('(c) Slope −1','(a/(2√2),a/(2√2)) and (−a/(2√2),−a/(2√2))','Opposite coordinate signs','(0,±a)'),why='The slope reduces to−tanθ off the cusps. Limiting secants give horizontal/vertical cusp tangents; solve tanθ=∓1 for the remaining points.')
row(2,29,n('x',4),n('y',0),why='dy/dx=(3t²)/(6t)=t/2 away from0. Slope1/2 requires t=1.')
row(2,30,c('All tangent lines','y=x−1 and y=−2x+11','Only y=x−1','y=x+1 and y=2x−5'),why='A tangent at parameter t has slope t. Requiring it to contain(4,3) gives t³−3t+2=(t−1)²(t+2)=0; t=1,−2 produce the two distinct lines.')
row(2,31,c('Enclosed area','πab','2πab','π(a²+b²)'),why='Integrate y dx around the ellipse, or four times its first quadrant; ∫₀^(π/2)ab sin²θ dθ=πab/4.',limited=True)
row(2,32,ex('Area',8*s.sqrt(2)/15),why='The curve meets the y-axis at t=0,2. Integrate width−x against dy: ∫₀²(2t−t²)/(2√t)dt=8√2/15.')
row(2,33,ex('Area',R(24,5)),why='The x-axis intersections have t=0,2, and x′=3t²≥0. Area=∫₀²(2t−t²)3t²dt=24/5.')
row(2,34,c('Area','3πa²/8','πa²','3πa²/4'),why='Use four quadrants and integrate y|dx|=3a²sin⁴θcos²θ dθ on0..π/2.')
row(2,35,c('Area under one arch','π(2r²+d²)','2πr²','π(r²+d²)'),why='For d<r, x is monotone over0≤θ≤2π. Area=∫y x′dθ=∫(r−dcosθ)²dθ.')
row(2,36,ex('(a) Area',24*s.sqrt(3)/5),ex('(b) Volume',27*s.pi/4),n('(c) Centroid x',R(9,7)),n('(c) Centroid y',0),why='Example1 has x=t²,y=t³−3t. On0≤x≤3 the loop has bounds±√x(3−x). Integrate its height, π times squared upper bound, and x times its height. Symmetry forces centroid y=0.')
def length(k,X,Y,lo,hi,exact=None,limited=False):
 speed=s.simplify(s.sqrt(s.diff(X,t)**2+s.diff(Y,t)**2));fn=s.lambdify(t,speed,'numpy');val=si.quad(fn,float(lo),float(hi),epsabs=2e-9,limit=600)[0]
 fs=[c('Length integral','∫ from '+str(lo)+' to '+str(hi)+' of '+fmt(speed)+' dt','∫ from '+str(lo)+' to '+str(hi)+' of 1 dt','∫ from '+str(lo)+' to '+str(hi)+' of '+fmt(speed**2)+' dt')]
 fs.append(ex('Exact length',exact) if exact is not None else n('Length (four decimals)',val,tol=.000051))
 row(2,k,*fs,why='Arc length integrates speed √((dx/dt)²+(dy/dt)²) over the source parameter interval. Use an improper limit when an endpoint speed is unbounded.',limited=limited)
 if exact is not None:assert abs(float(exact)-val)<1e-7,(k,exact,val)
for z in [(37,t+s.exp(-t),t-s.exp(-t),0,2),(38,t*t-t,t**4,1,4),(39,t-2*s.sin(t),1-2*s.cos(t),0,4*s.pi),(40,t+s.sqrt(t),t-s.sqrt(t),0,1)]:length(*z)
for z in [(41,1+3*t*t,4+2*t**3,0,1,4*s.sqrt(2)-2),(42,s.exp(t)-t,4*s.exp(t/2),0,2,s.exp(2)+1),(43,t*s.sin(t),t*s.cos(t),0,1,(s.sqrt(2)+s.asinh(1))/2),(44,3*s.cos(t)-s.cos(3*t),3*s.sin(t)-s.sin(3*t),0,s.pi,12),(45,s.exp(t)*s.cos(t),s.exp(t)*s.sin(t),0,s.pi,s.sqrt(2)*(s.exp(s.pi)-1),True),(46,s.cos(t)+s.log(s.tan(t/2)),s.sin(t),s.pi/4,3*s.pi/4,s.log(2),True)]:length(*z)
length(47,s.sin(t)+s.sin(3*t/2),s.cos(t),0,4*s.pi,limited=True)
length(48,3*t-t**3,3*t*t,-s.sqrt(3),s.sqrt(3),12*s.sqrt(3))
def simpson(f,lo,hi,N):
 h=(hi-lo)/N
 return h/3*sum((1 if j in(0,N) else 4 if j%2 else 2)*f(lo+j*h) for j in range(N+1))
v49=simpson(lambda u:math.sqrt(2+2*math.exp(2*u)),-6,6,6)
row(2,49,n('Simpson estimate, n=6',v49,tol=.0001),why='Speed=√(2+2e^(2t)); h=2 and Simpson weights1,4,2,4,2,4,1 at t=−6,−4,−2,0,2,4,6. This checks the requested Simpson estimate, not the exact integral.')
v50=simpson(lambda u:math.sqrt(4/math.sin(u)**4+16*math.sin(u)**2*math.cos(u)**2),math.pi/4,math.pi/2,4)
row(2,50,n('Coefficient of a in Simpson length, n=4 (a>0)',v50,tol=.0001),why='Speed=a√(4csc⁴θ+16sin²θcos²θ); apply Simpson with h=π/16 and four subintervals.')
row(2,51,ex('Distance traveled',6*s.sqrt(2)),ex('Geometric curve length',s.sqrt(2)),why='The curve is the segment x+y=1,0≤x≤1. On0..3π it is traversed six times.')
L=s.sqrt(5)+s.asinh(2)/2
row(2,52,ex('Distance traveled',4*L),ex('Geometric curve length',L),why='The source has x=cos²t, y=cos t, hence x=y² for−1≤y≤1. Integrating √(1+4y²) gives√5+asinh(2)/2. Four full endpoint-to-endpoint traversals occur over0..4π.')
row(2,53,c('Quarter-ellipse speed factor','a√(1−e²sin²θ), e=√(a²−b²)/a','a(1−e sinθ)','b√(1−e²sin²θ)'),c('Total length','4a∫₀^(π/2)√(1−e²sin²θ)dθ','2a∫₀^(π/2)√(1−e²sin²θ)dθ','2πab'),why='Differentiate x=a sinθ,y=b cosθ; factor a² from a²cos²θ+b²sin²θ and use fourfold symmetry.',limited=True)
row(2,54,c('Total length','6a','8a','2πa'),why='First-quadrant speed=3a sinθcosθ; its integral is3a/2, and there are four quadrants.')
X=11*s.cos(t)-4*s.cos(11*t/2);Y=11*s.sin(t)-4*s.sin(11*t/2)
speed=s.sqrt(605-484*s.cos(9*t/2));v55=si.quad(s.lambdify(t,speed,'numpy'),0,4*math.pi,epsabs=1e-9,limit=500)[0]
row(2,55,c('(a) Complete-curve interval','0≤t≤4π','0≤t≤π','0≤t≤2π'),n('(b) Complete length',v55,tol=.0001),why='Both frequencies1 and11/2 return together first after4π. The squared speed is605−484cos(9t/2); integrate over the entire period.',limited=True)
row(2,56,c('(a) Limits as t→+∞ and t→−∞','(1/2,1/2) and (−1/2,−1/2), respectively','(0,0) at both ends','The coordinates diverge to infinity'),c('(b) Length from origin to parameter t','|t|','t²','√(C(t)²+S(t)²)'),why='The Fresnel integrals tend to1/2 at+∞ and are odd. By the fundamental theorem, squared speed=cos²(πt²/2)+sin²(πt²/2)=1.',limited=True)
def surf(k,X,Y,lo,hi,axis='x',exact=None,limited=False):
 speed=s.simplify(s.sqrt(s.diff(X,t)**2+s.diff(Y,t)**2));radius=Y if axis=='x' else X;integrand=2*s.pi*radius*speed;fn=s.lambdify(t,integrand,'numpy');val=si.quad(fn,float(lo),float(hi),epsabs=2e-8,limit=500)[0]
 fields=[c('Surface-area integral about '+axis,'∫ from '+str(lo)+' to '+str(hi)+' of '+fmt(integrand)+' dt','∫ from '+str(lo)+' to '+str(hi)+' of '+fmt(speed)+' dt','∫ from '+str(lo)+' to '+str(hi)+' of 2π dt')]
 fields.append(ex('Exact surface area',exact) if exact is not None else n('Surface area (four decimals)',val,tol=.000051))
 row(2,k,*fields,why='Multiply arc-length element √(x′²+y′²)dt by circumference2π times distance from the rotation axis. The chosen interval traces the generating arc once.',limited=limited)
 if exact is not None:assert abs(float(exact)-val)<1e-5,(k,exact,val)
for z in [(57,t*s.sin(t),t*s.cos(t),0,s.pi/2),(58,s.sin(t),s.sin(2*t),0,s.pi/2),(59,t+s.exp(t),s.exp(-t),0,1),(60,t*t-t**3,t+t**4,0,1)]:surf(*z)
# Exact antiderivatives independently checked by quadrature in surf().
area61=s.integrate(2*s.pi*t**3*s.sqrt(9*t*t+4),(t,0,1))
surf(61,t**3,t*t,0,1,exact=area61)
area62=s.integrate(16*s.pi*(4*t**R(3,2)+t**R(-3,2)),(t,1,3))
surf(62,2*t*t+1/t,8*s.sqrt(t),1,3,exact=area62)
row(2,63,c('Exact surface area','6πa²/5','3πa²/5','4πa²'),why='On the first quadrant, ds=3a sinθcosθdθ and radius=a sin³θ. Thus S=6πa²∫₀^(π/2)sin⁴θcosθdθ=6πa²/5.')
row(2,64,c('Generating interval without duplicating the surface','0≤θ≤π (upper half)','0≤θ≤2π counts the surface once','Only0≤θ≤π/2'),c('Surface area','128π/5','256π/5','32π/5'),why='Use the upper half of the symmetric cardioid. Speed=4sin(θ/2) and y=8sin³(θ/2)cos(θ/2); S=2π∫₀^π y ds=128π/5.',limited=True)
area65=36*s.pi*((26**R(5,2)-1)/5-(26**R(3,2)-1)/3)
surf(65,3*t*t,2*t**3,0,5,axis='y',exact=area65)
area66=s.integrate(2*s.pi*(s.exp(t)-t)*(s.exp(t)+1),(t,0,1))
surf(66,s.exp(t)-t,4*s.exp(t/2),0,1,axis='y',exact=area66)
row(2,67,c('Why f is invertible','Continuous nonzero f′ has constant sign on[a,b], so f is strictly monotone','A continuous derivative always makes f constant','g must be invertible'),c('Cartesian function','F(x)=g(f⁻¹(x)) on f([a,b])','F(x)=f(g⁻¹(x))','F(x)=g(x)/f(x)'),why='The intermediate value theorem prevents f′ changing sign without vanishing; the mean value theorem gives strict monotonicity. Substitute t=f⁻¹(x).',limited=True)
row(2,68,c('Changed arc-length factor','√(1+(dy/dx)²)|dx/dt|=√((dx/dt)²+(dy/dt)²)','√(1+dy/dx) dx/dt','dx/dt+dy/dt'),c('Surface formula about x','S=∫2π|y(t)|√(x′²+y′²)dt, with the generating arc traced once','S=∫πy²dt','S=∫2πx(t)dt'),why='Insert dy/dx=y′/x′ into the Cartesian formula. Absolute values account for reversed orientation and the nonnegative radius.',limited=True)
row(2,69,c('(a) Parametric curvature','|x′y″−x″y′|/(x′²+y′²)^(3/2)','|x′y″+x″y′|/(x′²+y′²)','|y′/x′|'),c('(b) Graph curvature','|f″(x)|/(1+f′(x)²)^(3/2)','|f′(x)|/(1+f″(x)²)','f″(x)/(1+f′(x))'),why='Differentiate tanφ=y′/x′ to obtain dφ/dt; divide its absolute value by ds/dt. For a graph use x as parameter.',limited=True)
row(2,70,ex('(a) Curvature at(1,1)',2/(5*s.sqrt(5))),n('(b) Maximum-curvature point x',0),n('(b) Maximum-curvature point y',0),n('Maximum curvature',2),why='For y=x², κ=2/(1+4x²)^(3/2), maximized by minimizing the denominator.')
row(2,71,n('Curvature at arch top',R(1,4)),why='At θ=π, x′=2,y′=0,x″=0,y″=−1, giving |−2|/4^(3/2)=1/4.')
row(2,72,n('(a) Line curvature',0),c('(b) Circle curvature','1/r','r','1/r²'),why='A line has zero second derivatives. For x=r cos t,y=r sin t, the curvature numerator is r² and denominator r³.',limited=True)
row(2,73,c('Tangency point T','(r cosθ,r sinθ)','(rθ,r)','(r sinθ,r cosθ)'),c('Unwound tangent vector TP','rθ(sinθ,−cosθ)','rθ(cosθ,sinθ)','r(sinθ,cosθ)'),c('Parametric involute','x=r(cosθ+θsinθ), y=r(sinθ−θcosθ)','x=r cosθ,y=r sinθ','x=rθ,y=rθ²'),why='The unwound length equals circular arcrθ; add that length times the clockwise unit tangent to the contact-point position.',limited=True)
row(2,74,c('Rope length','πr','2πr','r'),c('Available grazing area','5π³r²/6','π³r²/2','πr²'),why='The free side contributes a half-diskπ(πr)²/2. Winding around either side contributes the two involute regions with total(πr)³/(3r); the contact-boundary terms cancel the excluded silo disk. Sum gives5π³r²/6.')
# Bézier project: explicit valid constructions; the graphical/proof work remains limited.
suffix='-project-laboratory-project-bézier-curves-1'
P=[V(4,1),V(28,48),V(50,42),V(40,5)];B=s.expand((1-t)**3*P[0]+3*t*(1-t)**2*P[1]+3*t*t*(1-t)*P[2]+t**3*P[3])
put(2,1,[ex('x(t)',B[0]),ex('y(t)',B[1]),c('Control polygon','(4,1)→(28,48)→(50,42)→(40,5)','(4,1)→(50,42)→(28,48)→(40,5)','All four control points lie on the curve')],'Substitute the four source control points into the cubic Bernstein basis. Plot the curve0≤t≤1 and straight segments between consecutive control points.',True,suffix)
put(2,2,[c('Initial derivative','B′(0)=3(P₁−P₀)','B′(0)=P₃−P₀','B′(0)=0'),c('Final derivative','B′(1)=3(P₃−P₂)','B′(1)=3(P₁−P₀)','B′(1)=0'),n('Initial tangent slope',R(47,24)),n('Final tangent slope',R(37,10))],'Differentiating the cubic Bernstein formula at its endpoints leaves exactly these differences, placing each tangent on its adjacent control segment.',True,suffix)
# The loop example below is independently checked with two distinct interior parameters.
Q1=V(80,20);Q=(1-t)**3*P[0]+3*t*(1-t)**2*Q1+3*t*t*(1-t)*P[2]+t**3*P[3]
u,v=s.symbols('u v',real=True)
F=[s.div(s.expand(e.subs(t,u)-e.subs(t,v)),u-v,u)[0] for e in Q]
sol=s.solve(F,(u,v));valid=[(uu,vv) for uu,vv in sol if uu.is_real and vv.is_real and 0<float(uu)<float(vv)<1]
assert valid,sol
uu,vv=valid[0];pt=Q.subs(t,uu)
put(2,3,[c('One valid replacement for P₁','(80,20)','(4,1)','(40,5)'),n('First crossing parameter',uu,tol=.000001),n('Second crossing parameter',vv,tol=.000001),n('Loop crossing x',pt[0],tol=.00001),n('Loop crossing y',pt[1],tol=.00001)],'Keeping P₀,P₂,P₃ fixed and moving P₁ to(80,20) makes B(u)=B(v) for two distinct parameters in(0,1). This explicitly certifies a loop rather than relying on appearance.',True,suffix)
put(2,4,[c('One C-shaped control-point list','(1,1),(−2,1),(−2,−1),(1,−1)','(−1,0),(0,0),(1,0),(2,0)','(0,0),(0,1),(0,2),(0,3)'),c('Tracing','Upper-right endpoint→left bulge→lower-right endpoint','A closed circle','A straight diagonal')],'Symmetric control points make an open C shape. This checks one valid construction; many other choices also satisfy the visual task.',True,suffix)
put(2,5,[c('First cubic controls','(1,1),(−1,2),(−1,0),(0,0)','(0,0),(1,0),(2,0),(3,0)','(1,1),(1,2),(1,3),(1,4)'),c('Second cubic controls','(0,0),(1,0),(1,−2),(−1,−1)','(0,0),(0,1),(0,2),(0,3)','(1,0),(2,0),(3,0),(4,0)'),c('Join derivative for both pieces','(3,0)','(0,3)','(0,0)')],'The two cubic pieces produce opposite bulges of an S. At the common endpoint their derivatives both equal(3,0), so the join is C¹ smooth. Other valid letter designs are possible.',True,suffix)
finish('section02')
