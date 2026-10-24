from parent_helper import *
from scipy.integrate import quad
import numpy as np
HERE=Path(__file__).parent;D=json.loads((HERE/'section06.json').read_text());checks=[]
def fs(k):
 g=D[f'calculus-section-10-6-{k}']['grader'];return g.get('parts',[g])
def ck(label,a,b,tol=1e-8):
 assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(label,a,b)
 checks.append(label)
for k,e,axis,d in [(1,.5,'x',4),(2,1,'x',-3),(3,1.5,'y',2),(4,3,'x',3),(6,.6,'y',4),(7,1,'y',6),(8,2,'x',-2)]:
 formula=s.sympify(fs(k)[0]['answer'].replace('^','**'),locals={'t':t});fn=s.lambdify(t,formula,'numpy')
 for theta in [.27,1.03,2.21,4.3]:
  radius=fn(theta);coord=radius*(np.cos(theta)if axis=='x'else np.sin(theta));ck('focus-directrix'+str(k)+str(theta),abs(radius),e*abs(coord-d))
for equation in [2/(3+2*s.cos(t)),10/(3-2*s.cos(t))]:ck('ambiguous given vertex5',equation.subs(t,pi),2)
for k,num,base,trig,coef in [(9,4,5,'sin',-4),(10,1,2,'sin',1),(11,2,3,'sin',3),(12,5,2,'cos',-4),(13,9,6,'cos',2),(14,1,3,'sin',-3),(15,3,4,'cos',-8),(16,4,2,'cos',3)]:
 ck('eccentricity'+str(k),fs(k)[0]['answer'],abs(coef)/base)
 d=num/coef
 for theta in [.3,1.4,2.5]:
  trigvalue=np.sin(theta)if trig=='sin'else np.cos(theta);radius=num/(base+coef*trigvalue);ck('conic focus-directrix'+str(k)+str(theta),abs(radius),abs(coef)/base*abs(radius*trigvalue-d))
for k,aa,e in [(25,2.28e8,.093),(26,7.8e8,.048),(27,18.09,.97),(28,178.25,.9951)]:
 formula=s.sympify(fs(k)[0]['answer'].replace('^','**'),locals={'t':t})
 ck('perihelion'+str(k),formula.subs(t,0),aa*(1-e));ck('aphelion'+str(k),formula.subs(t,pi),aa*(1+e))
aa=4.6e7/(1-.206);bb=aa*np.sqrt(1-.206**2);length=quad(lambda u:np.hypot(aa*np.sin(u),bb*np.cos(u)),0,2*np.pi)[0];ck('Mercury independent ellipse quadrature',fs(31)[0]['answer'],length)
(HERE/'section06-independent-audit.json').write_text(json.dumps({'passed':True,'records':len(D),'checks':checks},indent=2)+'\n');print('PASS10.6',len(checks),'checks')
