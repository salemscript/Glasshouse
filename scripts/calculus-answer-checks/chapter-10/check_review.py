from parent_helper import *
import numpy as np
from scipy.integrate import quad
HERE=Path(__file__).parent
D=json.loads((HERE/'review.json').read_text());P=json.loads((HERE/'plus.json').read_text());checks=[]
def ck(label,a,b,tol=1e-7):
 assert np.allclose(np.array(a,dtype=float),np.array(b,dtype=float),atol=tol,rtol=tol),(label,a,b)
 checks.append(label)
def ans(k,i=0,pp=False):
 z=(P if pp else D)[f'calculus-chapter-10-{("problems-plus" if pp else "review")}-{k}'+('-problems-plus-0' if pp else '')]['grader'];return z.get('parts',[z])[i]['answer']
# Quadrature independently recomputes the source line/area integrals.
ck('loop28',ans(28),abs(quad(lambda t:(t*t+t+1)*(3*t*t-3),-2,1)[0]))
ck('cardioid parametric area30',float(6*pi),quad(lambda t:((2*np.cos(t)-np.cos(2*t))*(2*np.cos(t)-2*np.cos(2*t))-(2*np.sin(t)-np.sin(2*t))*(-2*np.sin(t)+2*np.sin(2*t)))/2,0,2*np.pi)[0])
ck('signed-radius ten-petal31',ans(31,2),10*quad(lambda q:4.5*np.cos(5*q),-np.pi/10,np.pi/10)[0])
beta=np.arcsin(1/3);ck('inner-loop32',ans(32),quad(lambda q:(1-3*np.sin(q))**2/2,beta,np.pi-beta)[0])
ck('circle overlap35',ans(35),quad(lambda q:min(2*np.sin(q),np.sin(q)+np.cos(q))**2/2,0,3*np.pi/4,points=[np.pi/4])[0])
ck('polar difference36',ans(36),quad(lambda q:max(0,((2+np.cos(2*q))**2-(2+np.sin(q))**2)/2),0,2*np.pi,points=[np.pi/6,5*np.pi/6,3*np.pi/2])[0])
ck('length37',ans(37),quad(lambda t:np.hypot(6*t,6*t*t),0,2)[0]);ck('length38',ans(38),quad(lambda t:np.hypot(3,3*np.sinh(3*t)),0,1)[0]);ck('length39',ans(39),quad(lambda t:np.hypot(1/t,-1/t**2),np.pi,2*np.pi)[0]);ck('length40',ans(40),quad(lambda t:np.hypot(np.sin(t/3)**3,np.sin(t/3)**2*np.cos(t/3)),0,np.pi)[0]);ck('surface41',ans(41),quad(lambda t:2*np.pi*(t**3/3+1/(2*t*t))*np.hypot(2/np.sqrt(t),t*t-t**-3),1,4)[0]);ck('surface42',ans(42),quad(lambda t:2*np.pi*np.cosh(3*t)*np.hypot(3,3*np.sinh(3*t)),0,1)[0])
# Source tangent slopes, using independent numerical differences.
for k,xx,yy,t0 in [(21,lambda t:mp.log(t),lambda t:1+t*t,1),(22,lambda t:t**3+6*t+1,lambda t:2*t-t*t,-1),(23,lambda t:mp.exp(-t)*mp.cos(t),lambda t:mp.exp(-t)*mp.sin(t),mp.pi),(24,lambda t:(3+mp.cos(3*t))*mp.cos(t),lambda t:(3+mp.cos(3*t))*mp.sin(t),mp.pi/2)]:ck('slope'+str(k),ans(k),mp.diff(yy,t0)/mp.diff(xx,t0))
for k,xx,yy in [(25,t+s.sin(t),t-s.cos(t)),(26,1+t*t,t-t**3)]:
 for tt in [.27,.83,1.4]:
  xf=s.lambdify(t,xx,'mpmath');yf=s.lambdify(t,yy,'mpmath');slope=lambda z:mp.diff(yf,z)/mp.diff(xf,z);d2=mp.diff(slope,tt)/mp.diff(xf,tt)
  for j,expected in enumerate([slope(tt),d2]):ck(f'derivative{k}.{j}@{tt}',s.sympify(ans(k,j).replace('^','**'),locals={'t':t}).subs(t,tt),expected)
# Every reported tangent point on the nephroid-like epicycloid satisfies the source parametrization.
for tt in [0,2*np.pi/3,4*np.pi/3,np.pi,np.pi/3,5*np.pi/3]:
 xp=-2*np.sin(tt)+2*np.sin(2*tt);yp=2*np.cos(tt)-2*np.cos(2*tt)
 ck('horizontal/vertical29@'+str(tt),min(abs(xp),abs(yp)),0)
# Conic focal identities independently checked from semiaxes.
for aa,bb,cc in [(3,np.sqrt(8),1),(5,3,4),(4,np.sqrt(12),2),(401/8,5,399/8),(5,2,np.sqrt(21))]:ck('ellipse focal identity'+str(aa)+str(bb),aa*aa-bb*bb,cc*cc)
ck('hyperbola51',72/5+8/5,16)
# Longbow midpoint: ray point Q lies on circle and R on horizontal line.
for tt in [.4,1.1,2.3]:
 Q=np.array([2*np.sin(tt)*np.cos(tt),2*np.sin(tt)**2]);RR=np.array([2/np.tan(tt),2]);M=(Q+RR)/2
 ck('longbow circle',Q[0]**2+(Q[1]-1)**2,1);ck('longbow midpoint',M,[np.sin(tt)*np.cos(tt)+1/np.tan(tt),1+np.sin(tt)**2])
# Folium and its improper loop area.
for tt in [-3,-.7,.2,1,5]:
 xx=3*tt/(1+tt**3);yy=3*tt*tt/(1+tt**3);ck('folium cubic'+str(tt),xx**3+yy**3,3*xx*yy)
ck('folium area',1.5,-quad(lambda t:9*t*t*(1-2*t**3)/(1+t**3)**3,0,np.inf)[0])
# ProblemsPlus1 direct disk intersection cross section, with independent clipping.
edge=np.sqrt(2)-1
ck('PP1disk intersection',ans(1,pp=True),4*quad(lambda xx:min(np.sqrt(2-xx*xx)-1,np.sqrt(max(0,2-(xx+1)**2))),0,edge,points=[(np.sqrt(3)-1)/2])[0])
ck('PP2polar area',ans(2,5,True),quad(lambda q:.5/(np.cos(q)**4+np.sin(q)**4),0,2*np.pi)[0])
# Tight rectangle: sample all c and angles, then check known equality points.
qs=np.linspace(0,2*np.pi,4001)
for cc in np.linspace(0,1,51):
 rr=1+cc*np.sin(qs);xx=rr*np.cos(qs);yy=rr*np.sin(qs);assert xx.min()>=-3*np.sqrt(3)/4-1e-9 and xx.max()<=3*np.sqrt(3)/4+1e-9 and yy.min()>=-1-1e-9 and yy.max()<=2+1e-9
checks.append('PP3entire-family-bounds-grid')
# PP5 midpoint invariant at both branches, including negative y.
for uu in [-2,-.4,.5,1.7]:
 a,b=2.,3.;x0=a*np.cosh(uu);y0=b*np.sinh(uu);xp=a*a*b/(b*x0-a*y0);xm=a*a*b/(b*x0+a*y0);ck('PP5midpoint'+str(uu),[(xp+xm)/2,b/a*(xp-xm)/2],[x0,y0])
# PP6 equilateral/centroid identities for several b and phase values.
for bb in [.1,.4,.9]:
 for tt in [.2,1.1,2.6]:
  qq=tt+np.arange(3)*2*np.pi/3;pts=np.c_[bb*np.cos(3*qq)+3*np.cos(qq),bb*np.sin(3*qq)+3*np.sin(qq)];ck('PP6centroid',pts.mean(axis=0),[bb*np.cos(3*tt),bb*np.sin(3*tt)]);ck('PP6sides',[np.linalg.norm(pts[j]-pts[(j+1)%3]) for j in range(3)],[3*np.sqrt(3)]*3)
(HERE/'review-independent-audit.json').write_text(json.dumps({'passed':True,'reviewRecords':len(D),'plusRecords':len(P),'checks':checks},indent=2)+'\n');print('PASS10review+PP',len(checks),'checks')
