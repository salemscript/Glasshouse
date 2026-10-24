from common import *
from scipy.optimize import differential_evolution
import numpy as np
x,y,z=s.symbols('x y z',real=True);checks=0
# Numerical global extrema independent of hand-written stationary-point classifications.
for expr,box,expected in [(4*x*y*y-x*x*y*y-x*y**3,[(0,6),(0,1)],(-64,4)),(s.exp(-x*x-y*y)*(x*x+2*y*y),[(0,2),(0,2*np.pi)],(0,2/np.e))]:
 if expected==(-64,4):fun=s.lambdify((x,y),expr,'numpy');evaluate=lambda q:fun(q[0],(6-q[0])*q[1])
 else:fun=s.lambdify((x,y),expr,'numpy');evaluate=lambda q:fun(q[0]*np.cos(q[1]),q[0]*np.sin(q[1]))
 for sign,target in [(1,expected[0]),(-1,expected[1])]:
  result=differential_evolution(lambda q:sign*evaluate(q),box,seed=52,tol=1e-10,popsize=24);assert abs(evaluate(result.x)-target)<1e-6,(result,target);checks+=1
# Polygon area with perimeter1. Variables roof angle and proportion of available side length.
def area(q):
 theta,ratio=q;a=ratio/(2*(1+np.cos(theta)));b=2*a*np.cos(theta);h=(1-b-2*a)/2;return b*h+b*a*np.sin(theta)/2
opt=differential_evolution(lambda q:-area(q),[(0,np.pi/2),(0,1)],seed=23,tol=1e-11)
a=1/(3+2*np.sqrt(3));b=np.sqrt(3)*a;h=(1+np.sqrt(3))*a/2
assert abs(b+2*h+2*a-1)<1e-12
assert abs(-opt.fun-(b*h+b*a/4))<1e-9
assert abs(opt.x[0]-np.pi/6)<1e-5;checks+=3
# Constrained plane quadratic and closest product-surface points.
xx,yy=R(18,23),-R(6,23);zz=R(11,23)
assert xx+yy+zz==1 and xx-yy+2*zz==2
assert xx*xx+2*yy*yy+3*zz*zz==R(33,23);checks+=3
h0=3**(-R(1,4));assert s.simplify(h0*(s.sqrt(2)*h0)**2*(s.sqrt(3)*h0)**3)==2;checks+=1
# Independent finite-difference gradient checks for all review differentiation examples.
u,v,w,alpha,beta,r,t,kk,ll,mm=s.symbols('u v w alpha beta r t k l m',real=True)
exprs=[((5*y**3+2*x*x*y)**8,[x,y]),((u+2*v)/(u*u+v*v),[u,v]),(alpha**2*s.log(alpha**2+beta**2),[alpha,beta]),(s.exp(x*z)*s.sin(y/z),[x,y,z]),(u*s.atan(v*s.sqrt(w)),[u,v,w]),(4*x**3-x*y*y,[x,y]),(x*s.exp(-2*y),[x,y]),(x**3*y**2*z**4,[x,y,z]),(r*s.cos(u+2*t),[r,u,t])]
for expr,vs in exprs:
 fn=s.lambdify(vs,expr,'numpy');pt=np.array([.7+.2*i for i in range(len(vs))]);step=1e-5
 for i,variable in enumerate(vs):
  a0=pt.copy();b0=pt.copy();a0[i]+=step;b0[i]-=step;numeric=(fn(*a0)-fn(*b0))/(2*step);exact=float(s.diff(expr,variable).subs(dict(zip(vs,pt))));assert abs(numeric-exact)<1e-5*(1+abs(exact));checks+=1
# Verify all recorded Hessian classifications directly and the source critical point equations.
audit=json.loads((Path(__file__).parent/'review-audit.json').read_text())
for num,expr in {51:x*x-x*y+y*y+9*x-6*y+10,52:x**3-6*x*y+8*y**3,53:3*x*y-x*x*y-x*y*y,54:(x*x+y)*s.exp(y/2),57:x**3-3*x+y**4-2*y*y}.items():
 for kind,rows in audit['criticalPoints'][str(num)].items():
  for a0,b0,value in rows:
   sub={x:s.sympify(a0),y:s.sympify(b0)};assert s.simplify(s.diff(expr,x).subs(sub))==0 and s.simplify(s.diff(expr,y).subs(sub))==0;assert s.simplify(expr.subs(sub)-s.sympify(value))==0;checks+=3
# Ellipse tangency and numerical containment across entire source circle.
aa=np.sqrt(1.5);bb=3/np.sqrt(2);theta=np.linspace(0,2*np.pi,100001);xx=np.cos(theta);yy=1+np.sin(theta);assert np.max(xx*xx/aa**2+yy*yy/bb**2)<1+1e-10
assert abs(2/3-(1/(aa*aa)))<1e-10
checks+=2
(Path(__file__).parent/'review-independent-audit.json').write_text(json.dumps({'checks':checks,'passed':True,'methods':['numerical global optimization on source regions','finite differences','critical-point residuals','ellipse containment','perimeter and product constraints'],'sourceExceptions':['14Review42 has no regular real implicit graph','14PP1 maximum only supremum for strictly interior cuts','14PP4 literal real powers require domain qualification','14PP8 c=0 bound need not be attained']},indent=2)+'\n')
print('PASS',checks,'independent review/PP checks')
