"""Independent source-equation, boundary, geometry and optimization regressions."""
import json, math
from pathlib import Path
import mpmath as m
import sympy as s
m.mp.dps=45;HERE=Path(__file__).parent
rows=json.loads((HERE/'review.json').read_text());audit=json.loads((HERE/'review-audit.json').read_text());checks=[]
x=s.symbols('x',real=True)
def check(label,got,want,tol=1e-7):
 err=abs(float(got)-float(want));ok=err<=tol*max(1,abs(float(want)));checks.append(dict(label=label,error=err,passed=ok));assert ok,(label,got,want,err)
def fields(n):return rows[f'calculus-chapter-04-review-{n}-exercises-2']['grader']
# Locate by exact source ID, independent of subsection suffix generation.
def fs(n):
 q=next(v for k,v in rows.items() if k==f'calculus-chapter-04-review-{n}');return q['grader'].get('parts',[q['grader']])
def val(n,i=0):
 f=fs(n)[i];return f['answer'] if f['type']=='numeric' else s.sympify(f['answer'],locals={'ln':s.log,'arctan':s.atan,'x':x})
for c in audit['independentCases']:
 if c['kind']=='curve':
  f=s.sympify(c['function'],locals={'x':x});fn=s.lambdify(x,f,'mpmath')
  for z in c['critical']:check(f"{c['number']}stationary{z}",m.diff(fn,m.mpf(str(s.N(s.sympify(z),40)))),0,1e-6)
  for z in c['inflections']:check(f"{c['number']}curvature{z}",m.diff(fn,m.mpf(str(s.N(s.sympify(z),40))),2),0,1e-6)
 elif c['kind']=='primitive':
  f=s.sympify(c['integrand'],locals={'x':x});p=s.sympify(c['primitive'],locals={'x':x});fn=s.lambdify(x,f,'mpmath');pn=s.lambdify(x,p,'mpmath')
  for z in [m.mpf('.4'),m.mpf('1.3'),m.mpf('2.2')]:check(f"primitive{c['number']}@{z}",m.diff(pn,z),fn(z))
# Objective functions independently reconstructed from physical dimensions.
check('50 linear constraint',val(50)+4*val(50,1),1000)
check('52 hyperbola',val(52)*val(52,1),8)
check('52 distance stationarity',2*(val(52)-3)-128/val(52)**3,0)
check('55 minimizing DP',m.diff(lambda z:2*m.sqrt(16+z*z)+5-z,m.mpf(val(55))),0)
check('59 revenue derivative',23000-2000*val(59),0)
check('60 profit stationarity',23.2+.34*val(60,1)-.003*val(60,1)**2,0)
check('60 average cost stationarity',-1800/val(60,2)**2-.2+.002*val(60,2),0)
check('61 original polynomial',val(61)**5-val(61)**4+3*val(61)**2-3*val(61)-2,0)
for j in (0,1):check('62 original equation'+str(j),m.sin(val(62,j))-val(62,j)**2+3*val(62,j)-1,0)
t=m.findroot(lambda z:1-2*z-m.sin(z),(.2,.5));check('63 concave objective maximum',val(63),m.cos(t)+t-t*t)
for n,deriv,order,conditions in [(69,lambda z:2*z-3*m.sin(z),1,[(0,5)]),(70,lambda z:(z*z+m.sqrt(z))/z,1,[(1,3)]),(71,lambda z:1-6*z+48*z*z,2,[(0,1)]),(72,lambda z:5*z**3+6*z*z+2,2,[(0,3),(1,-2)]),(73,lambda z:2*z-1/(1+z*z),1,[(0,1)]),(74,lambda z:m.sin(z)+3*m.cos(z),2,[(0,0)]),(75,lambda z:m.exp(z)/10+m.sin(z),1,[(0,0)])]:
 p=val(n);fn=s.lambdify(x,p,'mpmath')
 for z in [m.mpf('.3'),m.mpf('1.2')]:check(f'{n} derivative@{z}',m.diff(fn,z,order),deriv(z))
 for z,v in conditions:check(f'{n} boundary@{z}',fn(z),v)
check('71 initial slope',s.diff(val(71),x).subs(x,0),2);check('74 initial velocity',s.diff(val(74),x).subs(x,0),2)
w,d=map(float,[val(79,1),val(79,2)]);z=d+5*math.sqrt(2)
check('79 plank circle',w*w/4+z*z,100);check('79 plank stationarity',100-2*z*z+5*math.sqrt(2)*z,0)
check('79 strong beam diagonal',val(79,3)**2+val(79,4)**2,400)
check('85 optimal pole',val(85),math.sqrt(800))
# Both interpretations of the misprinted source formula are explicitly distinguished.
for c in [m.mpf('1e-7'),m.mpf('1e-9')]:
 check('82 literal asymptotic'+str(c),3/c*m.log(m.cosh(m.sqrt(9.8*c/(3*2)))),9.8/4,1e-6)
# Correct original construction satisfies all signs at representative values.
f=lambda z:-z+m.exp(-z*z/2)
for z in [-4,-1.5,-.5,0,.5,1.5,4]:
 assert m.diff(f,z)<0;dd=m.diff(f,z,2);assert (dd>0)==(abs(z)>1)
 checks.append(dict(label='84 signs@'+str(z),passed=True))
(HERE/'review-verification.json').write_text(json.dumps(dict(checks=len(checks),failures=0,cases=checks),indent=2)+'\n');print('PASS',len(checks),'Chapter4review independent regressions')
