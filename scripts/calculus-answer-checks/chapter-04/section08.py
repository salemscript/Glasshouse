from common import *
import mpmath as mp
mp.mp.dps=55
# Source printed348–350 visually reviewed. Decimal roots independently checked by residual.
def root(f,a,b=None):
 fn=s.lambdify(x,f,'mpmath');r=mp.findroot(fn,(a,b) if b is not None else a)
 assert abs(fn(r))<mp.mpf('1e-40'),(f,r)
 TESTS.append(dict(label='root of '+str(f),root=str(r),residual=str(fn(r))))
 return r
def rootsrow(k,f,seeds,digits=6,limited=False):
 rr=sorted(set(root(f,*v) if isinstance(v,tuple) else root(f,v) for v in seeds))
 row(8,k,*[n('Root '+str(i+1)+' (ascending order)',r,tol=.51*10**-digits) for i,r in enumerate(rr)],why='Apply xₙ₊₁=xₙ−f(xₙ)/f′(xₙ), retaining guard digits. Substitute the resulting real roots into the original equation; exclude values outside its domain.',limited=limited)
row(8,1,n('(a) graph estimate x₂',7.1,tol=.5),n('(a) graph estimate x₃',6.8,tol=.3),c('(b) better initial choice','Yes: x₁=8 approaches from the increasing, concave-up side','No: every initial value gives identical iterations','No: Newton’s method cannot find this root'),why='Extend each tangent to its x-intercept; the source diagram supports approximate readings, not exact decimal iterates.',limited=True)
row(8,2,n('Graph estimate x₂',3.5,tol=.5),n('Graph estimate x₃',2.8,tol=.35),why='Starting at1, extend the tangent to the x-axis and repeat at its intercept. These are approximate source-graph readings.',limited=True)
row(8,3,n('x₂',4.5),why='The next iterate is the tangent’s x-intercept:0=9−2x gives4.5.')
row(8,4,c('(a) x₁=0','Iterates move left and do not reach a root','Converges to the right root','Derivative is zero at the start'),c('(b) x₁=1','Fails because the initial tangent is horizontal','Converges to the left root','Converges to the right root'),c('(c) x₁=3','Converges to the left root near2','Converges to the right root near6','Initial derivative is zero'),c('(d) x₁=4','Fails because the initial tangent is horizontal','Converges to the left root','Converges to the right root'),c('(e) x₁=5','Converges to the right root near6','Converges to the left root','Initial derivative is zero'),why='Use the drawn tangent slopes. Horizontal tangents make division by f′ undefined, and the nearly flat positive left tail drives iterates farther left.',limited=True)
row(8,5,c('Starting values expected to converge','a and b','c and d','All four'),why='Near the root the tangents from a and b repeatedly reduce distance to0. Farther out, the shallow tangents at c,d overshoot and drive large oscillations.',limited=True)
for k,f,a in [(6,2*x**3-3*x*x+2,-1),(7,2/x-x*x+1,2),(8,x**7+4,-1)]:
 z=s.Rational(a)
 for _ in range(2):z=s.cancel(z-f.subs(x,z)/s.diff(f,x).subs(x,z))
 row(8,k,n('x₃',z,tol=.000051),why='Perform exactly two Newton updates from the supplied x₁, keeping unrounded intermediate values.')
for k,f,a in [(9,x**3+x+3,-1),(10,x**4-x-1,1)]:
 v=a-f.subs(x,a)/s.diff(f,x).subs(x,a)
 row(8,k,n('x₂',v),expr('Tangent line y',f.subs(x,a)+s.diff(f,x).subs(x,a)*(x-a)),why='The tangent at x₁ has equation y=f(x₁)+f′(x₁)(x−x₁); its zero is x₂.',limited=True)
row(8,11,n('Fourth root of75',mp.root(75,4),tol=.0000000051),why='Use f(x)=x⁴−75 and the positive initial estimate3; retain guard digits through convergence.')
row(8,12,n('Eighth root of500',mp.root(500,8),tol=.0000000051),why='Use f(x)=x⁸−500 and a positive initial estimate near2.2.')
for k,f,a,b in [(13,3*x**4-8*x**3+2,2,3),(14,-2*x**5+9*x**4-7*x**3-11*x,3,4)]:
 r=root(f,a,b)
 row(8,k,c('(a) existence reason','Polynomial continuity and opposite endpoint signs imply a root by the IVT','Equal endpoint signs imply a root','A horizontal tangent guarantees a root'),n('(b) root',r,tol=.00000051),why='Evaluate the continuous polynomial at both endpoints, then use Newton’s iteration and verify the resulting residual.',limited=True)
for k,f,seeds,digits in [(15,s.exp(x)+x*x-4,[-2],6),(16,3*s.sin(x)-x,[2],6),(17,3*s.cos(x)-x,[(-3,-2),(-2,-1),(1,2)],6),(18,s.sqrt(x+1)-x*x+x,[(-1,0),(1,2)],6),(19,2**x+x*x-2,[(-2,-1),(0,1)],6),(20,s.log(x)-1/(x-3),[(.1,.9),(3.5,4)],6),(21,x**3-s.atan(x),[-1,0,1],6),(22,s.sin(x)-x*x+2,[-1,2],6),(23,-2*x**7-5*x**4+9*x**3+5,[-2,-1,1],8),(24,x**5-3*x**4+x**3-x*x-x+6,[-1,1,3],8),(25,x/(x*x+1)-s.sqrt(1-x),[(.5,1)],8),(26,s.cos(x*x-x)-x**4,[(-1,0),(0,1)],8),(27,4*s.exp(-x*x)*s.sin(x)-x*x+x-1,[(0,.5),(.5,1.5)],8),(28,s.log(x*x+2)-3*x/s.sqrt(x*x+1),[(0,1),(2,5)],8)]:rootsrow(k,f,seeds,digits,k>=23)
row(8,29,c('(a) square-root iteration','xₙ₊₁=(xₙ+a/xₙ)/2','xₙ₊₁=(xₙ−a/xₙ)/2','xₙ₊₁=xₙ+a/xₙ'),n('(b) √1000',mp.sqrt(1000),tol=.00000051),why='Apply Newton to x²−a, whose derivative is2x, then simplify the update. A positive initial value gives the positive root.',limited=True)
row(8,30,c('(a) reciprocal iteration','xₙ₊₁=2xₙ−axₙ²','xₙ₊₁=xₙ−axₙ²','xₙ₊₁=2xₙ+axₙ²'),n('(b) 1/1.6984',1/mp.mpf('1.6984'),tol=.00000051),why='For f=1/x−a and f′=−1/x², Newton simplifies to2x−ax². Use a nonzero starting value in the convergence interval.',limited=True)
row(8,31,c('Failure at x₁=1','f′(1)=0 but f(1)=4; the tangent has no x-intercept','f(1)=0 so the root is already found','f′(1)=4 so division is impossible'),why='f′=3x²−3 vanishes at1; the next Newton quotient is undefined.')
r=root(x**3-x-1,1)
row(8,32,*[n('('+a+') root from x₁='+b,r,tol=.00000051) for a,b in [('a','1'),('b','0.6'),('c','0.57')]],c('(d) sensitivity reason','Near x=1/√3 the derivative is nearly zero, producing very large Newton steps','All three first steps are equal','The equation has three real roots'),why='The equation has one real root. Small starting-value changes near a horizontal tangent cause large changes in subsequent steps and iteration count.',limited=True)
row(8,33,c('Iteration for nonzero xₙ','xₙ₊₁=−2xₙ','xₙ₊₁=xₙ/2','xₙ₊₁=0'),c('Behavior','Alternating signs with doubling magnitude; no convergence','Converges monotonically to0','Converges in one step'),why='For the real cube root, f′=(1/3)x^(−2/3), so f/f′=3x.',limited=True)
row(8,34,c('Iteration for nonzero xₙ','xₙ₊₁=−xₙ','xₙ₊₁=xₙ/2','xₙ₊₁=−2xₙ'),c('Behavior','A two-cycle between x₁ and−x₁','Converges to0','Magnitude doubles'),why='For either sign of x, f/f′=2x. Hence Newton flips sign without reducing magnitude.',limited=True)
f=x**6-x**4+3*x**3-2*x;rr=[root(s.diff(f,x),z) for z in [-1.4,-.5,.5]]
row(8,35,*[n('(a) critical number '+str(i+1),r,tol=.00000051) for i,r in enumerate(rr)],n('(b) absolute minimum',min(s.lambdify(x,f,'mpmath')(r) for r in rr),tol=.000051),why='Apply Newton to f′=6x⁵−4x³+9x²−2; compare f at all three real stationary points. Since f→∞ at both ends, the least value is the absolute minimum.')
f=x*s.cos(x);r=root(s.diff(f,x),.8)
row(8,36,n('Absolute maximum value',s.lambdify(x,f,'mpmath')(r),tol=.00000051),n('Location',r,tol=.00000051),why='Solve cosx−xsinx=0 in(0,π/2), then compare with f(0)=0 and f(π)=−π.')
f=x*x*s.sin(x);r=root(s.diff(f,x,2),2)
row(8,37,n('Inflection x',r,tol=.00000051),n('Inflection y',s.lambdify(x,f,'mpmath')(r),tol=.00000051),why='Solve(2−x²)sinx+4xcosx=0 in(0,π) and verify the concavity changes there; endpoints are not inflection points.')
r=root(x*s.cos(x)-s.sin(x),4.5)
row(8,38,n('Largest tangent slope',-mp.cos(r),tol=.00000051),why='A tangent through the origin obeys xcosx=sinx. The first nonzero positive solution near4.493409 gives the greatest positive slope; at later roots the magnitude1/√(1+x²) is smaller.')
r=root(x+2*(x-1)**3,.4)
row(8,39,n('Closest point x',r,tol=.00000051),n('Closest point y',(r-1)**2,tol=.00000051),why='Minimize squared distance x²+(x−1)⁴; its derivative vanishes when x+2(x−1)³=0. The second derivative is positive everywhere.')
r=root(s.sin(x/2)-s.Rational(2,5)*x,2)
row(8,40,n('θ in radians',r,'rad',.000051),n('θ to nearest degree',round(float(r*180/mp.pi)),'degrees',0),why='Arc length gives rθ=5 and chord length gives2r sin(θ/2)=4; eliminate radius. Reject the extraneous zero-angle root of the multiplied equation.')
r=root(48*x*(1+x)**60-(1+x)**60+1,.008)
row(8,41,c('Equation after eliminating denominators','48i(1+i)^60−(1+i)^60+1=0','60i(1+i)^48−(1+i)^48+1=0','48i−(1+i)^60+1=0'),n('Monthly interest rate',r*100,'percent/month',.00001),why='Set18000=375[1−(1+i)^(−60)]/i. Solve for the positive rate; i=0 is an extraneous root of the denominator-cleared equation because zero-rate payments total22500.')
r=s.Rational(304042,10**11);p=x**5-(2+r)*x**4+(1+2*r)*x**3-(1-r)*x*x+2*(1-r)*x+r-1
row(8,42,n('(a) L₁ x-coordinate',root(p,.99),'AU',.0000001),n('(b) L₂ x-coordinate',root(p-2*r*x*x,1.01),'AU',.0000001),why='Use the source mass ratio r=3.04042×10⁻⁶ and solve each stated fifth-degree equation, choosing the location near Earth as shown.')
finish('section08')
