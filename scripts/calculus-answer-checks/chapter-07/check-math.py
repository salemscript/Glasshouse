"""Independent high-precision derivative check of authored primitives, not expected-key replay."""
import json,sys
from pathlib import Path
import sympy as s
import mpmath as mp
H=Path(__file__).resolve().parent;mp.mp.dps=55
cases=json.loads((H/'mathematical-cases.json').read_text());results=[];fail=[]
for row in cases:
 f=s.sympify(row['integrand']);F=s.sympify(row['primitive']);symbols=f.free_symbols|F.free_symbols
 for v in symbols:
  if str(v)!='x':f=f.subs(v,s.Rational(5,2));F=F.subs(v,s.Rational(5,2))
 x=next((v for v in f.free_symbols|F.free_symbols if str(v)=='x'),s.Symbol('x'))
 ff=s.lambdify(x,f,'mpmath');ffp=s.lambdify(x,F,'mpmath');passed=0;bad=[]
 for z in ['-5.3','-3.7','-2.2','-1.4','-.7','-.3','.13','.37','.63','.87','1.3','1.9','2.7','4.1','7.3']:
  z=mp.mpf(z)
  try:
   v=ff(z);w=ffp(z)
   if abs(mp.im(v))>mp.mpf('1e-35') or abs(mp.im(w))>mp.mpf('1e-35') or not mp.isfinite(v):continue
   slope=(ffp(z+mp.mpf('1e-18'))-ffp(z-mp.mpf('1e-18')))/(2*mp.mpf('1e-18'))
   # Float constants authored via SymPy have at worst machine-precision coefficient error.
   if abs(v-slope)>mp.mpf('1e-11')*(1+abs(v)):bad.append(str(z))
   else:passed+=1
  except (ValueError,ZeroDivisionError,TypeError):continue
 status='pass' if passed>=2 and not bad else 'FAIL'
 if status!='pass':fail.append((row['id'],passed,bad))
 results.append(dict(id=row['id'],passedPoints=passed,badPoints=bad,status=status))
(H/'derivative-audit.json').write_text(json.dumps({'method':'55-digit centered differences h=1e-18 across real-domain sample points; parameters fixed at 5/2','cases':results,'failures':fail},indent=2)+'\n')
print('Cases',len(cases),'passed',len(cases)-len(fail),'failures',fail)
sys.exit(bool(fail))
