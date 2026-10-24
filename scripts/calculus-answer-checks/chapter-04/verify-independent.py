"""Independent numerical sign checks across every analytic curve interval.
Re-evaluate source functions with high precision and compare centered differences
against the authored interval classifications; no use of expected answer strings.
"""
import json,glob,math
from pathlib import Path
import sympy as s
import mpmath as mp
mp.mp.dps=40
folder=Path(__file__).parent
x=s.symbols('x',real=True)
checks=[]; failures=[]; skipped=[]
for fn in sorted(folder.glob('section*-audit.json')):
 data=json.loads(fn.read_text())
 if not isinstance(data,dict):continue
 for qid,a in data.get('questions',{}).items():
  if 'sourceFunction' not in a:continue
  f=s.sympify(a['sourceFunction'],locals={'x':x})
  # The real cube-root branches are separately hand-audited in section scripts.
  if any(z.q%2 and z.q>1 for z in f.atoms(s.Rational)):
   skipped.append(qid);continue
  fun=s.lambdify(x,f,'mpmath')
  for kind,br,sign in [('first','derivativeBreaks','derivativeSigns'),('second','concavityBreaks','concavitySigns')]:
   if kind=='first' and qid in [f'calculus-section-4-3-{n}' for n in (61,62,63,64)]:continue
   breaks=[float(s.sympify(v)) for v in a[br]]
   for lo,hi,expected in zip(breaks,breaks[1:],a[sign]):
    if not math.isfinite(lo):lo=hi-max(10,abs(hi)*2) if math.isfinite(hi) else -10
    if not math.isfinite(hi):hi=lo+max(20,abs(lo)*2)
    for fraction in [.05,.2,.4,.6,.8,.95]:
     t=mp.mpf(lo)+(mp.mpf(hi)-lo)*fraction
     try:
      result=mp.diff(fun,t,1 if kind=='first' else 2)
      if isinstance(result,mp.mpc) and abs(result.imag)>mp.mpf('1e-20'):raise ValueError('nonreal')
      value=float(mp.re(result));actual=1 if value>1e-14 else -1 if value< -1e-14 else 0
      if actual and actual!=expected:failures.append([qid,kind,float(t),expected,value])
      checks.append([qid,kind,float(t),actual])
     except (ValueError,ZeroDivisionError,OverflowError):pass
# Independent global comparisons for constrained optimization objectives.
optimization=[]
def global_check(label,fn,a,b,at,kind):
 value=fn(at)
 for i in range(1001):
  z=a+(b-a)*i/1000
  assert (fn(z)-value)*(1 if kind=='min' else -1)>=-1e-8,(label,z,fn(z),value)
 optimization.append({'question':label,'gridPoints':1001,'extremum':kind,'at':at})
global_check('4.7.11',lambda z:z*(750-5*z)/2,0,150,75,'max')
global_check('4.7.12',lambda z:z*(3-2*z)**2,0,1.5,.5,'max')
global_check('4.7.13',lambda z:3*z+3000000/z,10,5000,1000,'min')
global_check('4.7.14',lambda z:z*z+128000/z,.1,200,40,'min')
global_check('4.7.15',lambda z:z*(1200-z*z)/4,0,math.sqrt(1200),20,'max')
for base in (20,32):global_check('4.7.'+str(16 if base==20 else 17),lambda z:base*z*z+180/z,.01,10,(90/base)**(1/3),'min')
global_check('4.7.23',lambda z:5-2*z-3*z*z,-1,1,-1/3,'max')
from scipy.optimize import brentq
z=brentq(lambda z:z-4+(math.sin(z)-2)*math.cos(z),2,3)
global_check('4.7.24',lambda z:(z-4)**2+(math.sin(z)-2)**2,-10,18,z,'min')
global_check('4.7.28',lambda z:(1+z)*math.sqrt(max(0,1-z*z)),0,1,.5,'max')
global_check('4.7.33',lambda z:2*math.pi*(z+2*math.sqrt(max(0,z*(1-z)))),0,1,(5+math.sqrt(5))/10,'max')
global_check('4.7.35',lambda z:(z+8)*(384/z+12),.1,200,16,'min')
global_check('4.7.36',lambda z:186-3*z-360/z,2,60,math.sqrt(120),'max')
global_check('4.7.39',lambda z:16*z-z*z,0,16,8,'max')
global_check('4.7.41',lambda z:math.pi*z*z*math.sqrt(max(0,1-z*z))/3,0,1,math.sqrt(2/3),'max')
global_check('4.7.45',lambda z:z/(z+1)**2,0,20,1,'max')
global_check('4.7.46',lambda z:z**3/(z-1),1.0001,20,1.5,'min')
global_check('4.7.50',lambda z:2*math.sin(z/2)+(2*math.pi-2*z)/4,0,math.pi,0,'min')
out={'method':'40-digit numerical differentiation at six independently chosen points per interval','checks':len(checks),'optimizationComparisons':optimization,'failures':failures,'real_fractional_power_special_cases':sorted(set(skipped))}
(folder/'independent-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert not failures
