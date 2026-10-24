from parent_helper import *
from scipy.integrate import solve_ivp
D=json.loads((Path(__file__).parent/'review.json').read_text());checks=[]
def ck(label,a,b=0,tol=1e-8):
 assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(label,a,b)
 checks.append(label)
def F(k):
 g=D[f'calculus-chapter-09-review-{k}']['grader'];return g.get('parts',[g])
def ans(k,i=0):return F(k)[i]['answer']
C=s.symbols('C',real=True)
for k,z,rhs in [(5,(x*x/2+C)*s.exp(-s.sin(x)),lambda z:x*s.exp(-s.sin(x))-z*s.cos(x)),(8,(x*x+C)*s.exp(-1/x),lambda z:(z+2*x**3*s.exp(-1/x))/x**2),(11,x*(s.log(x)**2/2+2),lambda z:z/x+s.log(x)),(12,-s.log(s.exp(-1)-x**3),lambda z:3*x*x*s.exp(z))]:
 assert s.simplify(s.diff(z,x)-rhs(z))==0;checks.append('ODE residual'+str(k))
for k,z,rhs,initial in [(6,C*s.exp(t-t*t/2)-1,lambda z:(1-t)*(1+z),None),(9,5*s.exp(t-t*t),lambda z:(1-2*t)*z,5),(15,2000/(1+19*s.exp(-t/10)),lambda z:z/10*(1-z/2000),100),(24,50+10*s.exp(-R(3,2000)*t),lambda z:(750-15*z)/10000,60)]:
 assert s.simplify(s.diff(z,t)-rhs(z))==0;checks.append('ODE residual'+str(k))
 if initial is not None:ck('initial'+str(k),z.subs(t,0),initial)
z=s.log((3-s.cos(x))/(1+s.cos(x)));assert s.simplify((1+s.cos(x))*s.diff(z,x)-(1+s.exp(-z))*s.sin(x))==0;ck('initial10',z.subs(x,0));checks.append('ODE10')
sol=solve_ivp(lambda xx,yy:[xx*xx-yy[0]*yy[0]],(0,.3),[1],rtol=1e-12,atol=1e-14);ck('graph estimate3',ans(3),sol.y[0,-1],tol=.001)
for k,h,N in [(3,.1,3),(4,.2,2),(4,.1,4)]:
 xx=0.;yy=1.
 for j in range(N):yy+=h*(xx*xx-yy*yy if k==3 else 2*xx*yy*yy);xx+=h
 ck('Euler'+str(k)+str(h),yy,ans(k,1 if k==3 or h==.1 else 0))
ck('salt6',ans(18),solve_ivp(lambda tt,yy:[1-yy[0]/10],(0,6),[0],rtol=1e-11,atol=1e-13).y[0,-1])
for name in ['review']:
 for qid,z in D.items():
  for ff in z['grader'].get('parts',[z['grader']]):
   if ff['type']=='choice':assert len(set(ff['options']))==len(ff['options'])
(Path(__file__).parent/'review-independent-audit.json').write_text(json.dumps({'passed':True,'records':len(D),'checks':checks},indent=2)+'\n');print('PASS9review',len(checks))
