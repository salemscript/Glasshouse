"""Independent Cartesian geometry checks, separately encoded from contracts."""
import json,math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.optimize import brentq
P=Path(__file__).parent;checks=[]
def ok(name,a,b,tol=1e-8):
 assert abs(float(a)-float(b))<=tol*max(1,abs(float(b))),(name,a,b);checks.append(dict(name=name,value=float(a),expected=float(b)))
x,y,t=s.symbols('x y t',real=True)
# Source polynomials are independently entered directly from printed page680.
poly={1:x*x-6*y,2:2*y*y-5*x,3:2*x+y*y,4:3*x*x+8*y,5:(x+2)**2-8*(y-3),6:(y-2)**2-2*x-1,7:y*y+6*y+2*x+1,8:2*x*x-16*x-3*y+38,9:x+y*y,10:y-(x-2)**2/2+2,11:x*x/2+y*y/4-1,12:x*x/36+y*y/8-1,13:x*x+9*y*y-9,14:100*x*x+36*y*y-225,15:9*x*x-18*x+4*y*y-27,16:x*x+3*y*y+2*x-12*y+10,17:x*x/4+y*y/9-1,18:(x-2)**2/9+(y-1)**2/4-1,19:y*y/25-x*x/9-1,20:x*x/36-y*y/64-1,21:x*x-y*y-100,22:y*y-16*x*x-16,23:x*x-y*y+2*y-2,24:9*y*y-4*x*x-36*y-8*x-4,25:4*x*x-y*y-4,26:4*x*x-y-4,27:x*x-4*y+2*y*y,28:y*y-2-x*x+2*x,29:3*x*x-6*x-2*y-1,30:x*x-2*x+2*y*y-8*y+7}
import runpy,contextlib,io,sys
sys.path.insert(0,str(P))
with contextlib.redirect_stdout(io.StringIO()):auth=runpy.run_path(str(P/'section05.py'))
for no,h,k,p,v in auth['PAR']:
 xx,yy=(h+t,k+t*t/(4*p)) if v else(h+t*t/(4*p),k+t)
 ok(str(no)+' parsed source polynomial',s.simplify(poly[no].subs({x:xx,y:yy})),0)
for no,h,k,a2,b2,v,hyp in auth['CON']:
 for tt in [.2,.8]:
  along=math.sqrt(float(a2))*(math.cosh(tt) if hyp else math.cos(tt));across=math.sqrt(float(b2))*(math.sinh(tt) if hyp else math.sin(tt));xx,yy=(float(h)+across,float(k)+along) if v else(float(h)+along,float(k)+across)
  ok(str(no)+' parsed source polynomial '+str(tt),poly[no].subs({x:xx,y:yy}),0,1e-7)
# Tangencies independently differentiated in Cartesian coordinates.
for no,r,hs,vs in [(61,3*s.cos(t),[s.pi/4,3*s.pi/4],[0,s.pi/2]),(62,1-s.sin(t),[s.pi/6,5*s.pi/6,3*s.pi/2],[7*s.pi/6,11*s.pi/6]),(63,1+s.cos(t),[s.pi/3,5*s.pi/3],[0,2*s.pi/3,4*s.pi/3])]:
 dx=s.diff(r*s.cos(t),t);dy=s.diff(r*s.sin(t),t)
 for th in hs:ok('10.3#'+str(no)+' horizontal '+str(th),dy.subs(t,th),0);assert abs(float(dx.subs(t,th)))>1e-7
 for th in vs:ok('10.3#'+str(no)+' vertical '+str(th),dx.subs(t,th),0);assert abs(float(dy.subs(t,th)))>1e-7
# Discrete Cartesian chord lengths against the independently supplied analytic polar lengths.
for no,fn,end,expected in [(45,lambda q:2*np.cos(q),math.pi,2*math.pi),(48,lambda q:2*(1+np.cos(q)),2*math.pi,16),(49,lambda q:np.cos(q/4)**4,4*math.pi,16/3),(50,lambda q:np.cos(q/2)**2,2*math.pi,4)]:
 ts=np.linspace(0,end,200001);r=fn(ts);pts=np.column_stack([r*np.cos(ts),r*np.sin(ts)]);v=np.sqrt(np.sum(np.diff(pts,axis=0)**2,axis=1)).sum();ok('10.4#'+str(no)+' chord length',v,expected,2e-8)
# Closed numerical polygon areas: independent Cartesian shoelace (not same squared-r integrand).
for no,fn,end in [(9,lambda q:2*np.sin(q),math.pi),(10,lambda q:1-np.sin(q),2*math.pi),(11,lambda q:3+2*np.cos(q),2*math.pi),(12,lambda q:2-np.cos(q),2*math.pi),(13,lambda q:2+np.sin(4*q),2*math.pi),(14,lambda q:3-2*np.cos(4*q),2*math.pi),(15,lambda q:np.sqrt(1+np.cos(5*q)**2),2*math.pi),(16,lambda q:1+5*np.sin(6*q),2*math.pi)]:
 ts=np.linspace(0,end,200001);r=fn(ts);xx=r*np.cos(ts);yy=r*np.sin(ts);v=.5*abs(np.sum(xx[:-1]*yy[1:]-yy[:-1]*xx[1:]));g=json.loads((P/'section04.json').read_text())[f'calculus-section-10-4-{no}']['grader'];expected=g.get('parts',[g])[0]['answer'];ok('10.4#'+str(no)+' Cartesian polygon',v,expected,1e-7)
# Spheroid areas independently approximated by frusta from Cartesian ellipse samples.
for aa,bb in [(2,1),(5,3),(1.01,1)]:
 e=math.sqrt(1-bb*bb/(aa*aa));major=2*math.pi*bb*bb*(1+aa*math.asin(e)/(bb*e));minor=2*math.pi*aa*aa*(1+(1-e*e)*math.atanh(e)/e)
 ts=np.linspace(0,math.pi,100001);xx=aa*np.cos(ts);yy=bb*np.sin(ts);ds=np.sqrt(np.diff(xx)**2+np.diff(yy)**2);ok('10.5#64 prolate frusta'+str(aa),np.sum(math.pi*(yy[:-1]+yy[1:])*ds),major,1e-8)
 ts=np.linspace(-math.pi/2,math.pi/2,100001);xx=aa*np.cos(ts);yy=bb*np.sin(ts);ds=np.sqrt(np.diff(xx)**2+np.diff(yy)**2);ok('10.5#64 oblate frusta'+str(aa),np.sum(math.pi*(xx[:-1]+xx[1:])*ds),minor,1e-8)
# Distinct surface from rotating a single lemniscate loop about y, without double counting its mirror.
ts=np.linspace(-math.pi/4,math.pi/4,100001);rr=np.sqrt(np.maximum(0,np.cos(2*ts)));xx=rr*np.cos(ts);yy=rr*np.sin(ts);ds=np.sqrt(np.diff(xx)**2+np.diff(yy)**2);ok('10.4#56 distinct-surface frusta',np.sum(math.pi*(xx[:-1]+xx[1:])*ds),2*math.sqrt(2)*math.pi,2e-7)
(P/'sections03-05-independent-audit.json').write_text(json.dumps(dict(status='passed',checks=checks),indent=2)+'\n');print(len(checks),'independent Cartesian geometry checks passed')
