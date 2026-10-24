from common import *
import scipy.integrate as si
here=Path(__file__).parent
loc={str(q):q for q in[x,y,z,u,v,r,theta,phi,rho,a,b,h,k,t]};sub={a:2,b:3,h:4,k:R(3,2),rho:R(7,5)}
results=[]
for name in ['section04','section06']:
 for rec in json.loads((here/(name+'-audit.json')).read_text())['integrals']:
  if 'density' not in rec:continue
  bs=[tuple(s.sympify(q,locals=loc).subs(sub) for q in bound) for bound in rec['bounds']];vs=[q[0] for q in bs]
  coords=[s.sympify(q,locals=loc).subs(sub) for q in rec['coordinates']];den=s.sympify(rec['density'],locals=loc).subs(sub);J=s.sympify(rec['jacobian'],locals=loc).subs(sub)
  mult=[1,*coords,*([coords[1]**2,coords[0]**2] if len(coords)==2 else[coords[0]**2+coords[1]**2])]
  expected=[rec['mass'],*rec['moments']]
  ranges=[s.lambdify(vs[i+1:],(lo,hi),'math') for i,(_,lo,hi) in enumerate(bs)]
  for index,(m,e) in enumerate(zip(mult,expected)):
   value,error=si.nquad(s.lambdify(vs,den*J*m,'math'),ranges,opts={'epsabs':1e-7,'epsrel':1e-7})
   target=float(s.sympify(e,locals=loc).subs(sub));passed=abs(value-target)<max(2e-6,abs(target)*2e-6,error*3)
   results.append(dict(id=rec['id'],moment=index,expected=target,actual=value,passed=passed));assert passed,results[-1]
(here/'independent-moments.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS',len(results))
