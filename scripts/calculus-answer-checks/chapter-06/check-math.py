#!/usr/bin/env python3
"""Independent quadrature and physical regressions. Never imports author.py."""
import json,sys,math
from pathlib import Path
import sympy as S
import mpmath as mp
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[3]
mp.mp.dps=45
x=S.symbols('x',real=True);checks=[]
def parse(v):return S.sympify(str(v).replace('^','**'),locals={'x':x})
def check(a,b,label,tol=2e-7):
 a=float(S.N(a));b=float(S.N(b));assert abs(a-b)<=tol*max(1,abs(b)),(label,a,b)
 checks.append(label)
for ch in [5,6]:
 data=json.loads((ROOT/f'scripts/calculus-answer-checks/chapter-{ch:02}/source-audit.json').read_text())
 for j,it in enumerate(data['integrals']):
  e=parse(it['integrand']);fn=S.lambdify(x,e,'numpy');bs=[float(parse(z)) for z in it.get('bounds',[it.get('lower'),it.get('upper')])]
  pieces=[quad(fn,a,b,epsabs=1e-9,epsrel=1e-10,limit=200)[0] for a,b in zip(bs,bs[1:])]
  v=sum(abs(z) for z in pieces) if it.get('absolute') else sum(pieces)
  check(v,parse(it['value']),f'{ch} integral {j} {it["qid"]}')
d5=json.loads((ROOT/'scripts/calculus-answer-checks/chapter-05.json').read_text());d6=json.loads((ROOT/'scripts/calculus-answer-checks/chapter-06.json').read_text())
def fields(d,q):
 g=d[q]['grader'];return g.get('parts',[g])
def num(ch,sec,no,idx=0):return fields(d5 if ch==5 else d6,f'calculus-section-{ch}-{sec}-{no}')[idx]['answer']
# Independent finite-sum evaluations and signed/absolute area checks.
check(num(5,1,19),sum(2*(-t*(t-21)*(t+1)) for t in [1,3,5,7,9,11]),'infection midpoint source coefficients')
check(num(5,3,86,4),1/15-21.5/900+21.5**2/38700,'depreciation minimum')
for sec,no,fn,lo,hi in [(4,59,lambda t:3*t-5,0,3),(4,60,lambda t:t*t-2*t-3,2,4)]:
 check(num(5,sec,no,0),quad(fn,lo,hi)[0],f'displacement {no}')
 check(num(5,sec,no,1),quad(lambda t:abs(fn(t)),lo,hi)[0],f'distance {no}')
check(num(5,4,61,1),quad(lambda t:t*t/2+4*t+5,0,10)[0],'integrated acceleration61')
check(num(5,4,62,1),quad(lambda t:abs(t*t+3*t-4),0,3,points=[1])[0],'integrated acceleration62')
# Recovered diagram: verify washers independently against shells around every square edge.
for no,fn in [(23,lambda y:2*math.pi*y*y**4),(24,lambda t:2*math.pi*t*(1-t**.25)),(25,lambda t:2*math.pi*(1-t)*(1-t**.25)),(26,lambda y:2*math.pi*(1-y)*y**4),(27,lambda y:2*math.pi*y*(y-y**4)),(28,lambda t:2*math.pi*t*(t**.25-t)),(29,lambda t:2*math.pi*(1-t)*(t**.25-t)),(30,lambda y:2*math.pi*(1-y)*(y-y**4))]:
 check(num(6,2,no),quad(fn,0,1,epsabs=1e-10)[0],f'recovered446 shell-vs-washer {no}')
phi=(math.sqrt(5)-1)/2
check(num(6,2,34,3),math.pi*(quad(lambda y:y,0,phi)[0]+quad(lambda y:1-y*y,phi,1)[0]),'symmetric union counted once')
check(num(6,4,19,1),25*5/2,'folded chain center of mass')
check(num(6,4,30),quad(lambda v:160*(100/v)**1.4,100,800)[0],'pressure work quadrature')
check(num(6,4,34),150*756**2*481/3*(481/4),'pyramid center of mass')
# Spherical water-displacement continuity and limits.
for h in [0,2,5,10,12,15]:
 bowl=math.pi*h*h*(15-h/3)
 ball=math.pi*h*h*(5-h/3) if h<=10 else 500*math.pi/3
 contract=10*math.pi*h*h if h<=10 else bowl-500*math.pi/3
 check(contract,bowl-ball,'sphere displacement at '+str(h))
# Symbolic section6.2 formulas by numerical independent cross sections for several geometries.
for R,r,h in [(4,1,2),(5,3,7),(2,.5,1)]:
 check(math.pi*h*(R*R+R*r+r*r)/3,quad(lambda z:math.pi*(r+(R-r)*z/h)**2,0,h)[0],'conical frustum')
 check(2*math.pi**2*R*r*r,quad(lambda z:math.pi*((R+math.sqrt(r*r-z*z))**2-(R-math.sqrt(r*r-z*z))**2),-r,r)[0],'torus')
 check(16*r**3/3,quad(lambda z:4*(r*r-z*z),-r,r)[0],'orthogonal cylinder intersection')
 check(5*math.pi*r**3/12,2*quad(lambda z:math.pi*(r*r-z*z),r/2,r)[0],'sphere lens')
# Source-estimated values and proof recognition are separately visually reviewed, not certified by these equations.
report={'checks':len(checks),'passed':True,'methods':['SciPy adaptive quadrature independent of symbolic author integration','Shell versus washer recomputation for recovered diagram','Center-of-mass work identities','Explicit signed-distance and source finite-sum regressions'],'tests':checks}
(ROOT/'scripts/calculus-answer-checks/chapter-06/math-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(checks),'independent checks')
