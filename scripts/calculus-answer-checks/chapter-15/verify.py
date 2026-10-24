"""Independent adaptive quadrature of authoring audit integrals (not SymPy integration)."""
from common import *
import scipy.integrate as si
import warnings,time
here=Path(__file__).parent
records=json.loads((here/'source-audit.json').read_text())['integrals']
loc={str(q):q for q in[x,y,z,u,v,r,theta,phi,rho,a,b,h,k,t]}
sub={a:2,b:3,h:4,k:s.Rational(3,2)}
results=[]
for rec in records:
 if 'integrand' not in rec:continue
 expr=s.sympify(rec['integrand'],locals=loc).subs(sub)
 bs=[tuple(s.sympify(q,locals=loc).subs(sub) for q in bound) for bound in rec['bounds']]
 variables=[q[0] for q in bs]
 symbols=set().union(expr.free_symbols,*[set().union(q[1].free_symbols,q[2].free_symbols) for q in bs])-set(variables)
 if symbols:continue
 ranges=[]
 for i,(var,lo,hi) in enumerate(bs):
  fn=s.lambdify(variables[i+1:],(lo,hi),'math')
  ranges.append(fn)
 fn=s.lambdify(variables,expr,'math'); expected=float(s.sympify(rec['result'],locals=loc).subs(sub))
 try:
  with warnings.catch_warnings():
   warnings.simplefilter('ignore'); actual,error=si.nquad(fn,ranges,opts={'epsabs':1e-7,'epsrel':2e-7,'limit':100})
  passed=abs(actual-expected)<=max(2e-6,abs(expected)*2e-6,error*3)
  result=dict(id=rec['id'],expected=expected,numerical=actual,error=error,passed=passed)
 except Exception as e:result=dict(id=rec['id'],error=str(e),passed=False)
 results.append(result);print(result,flush=True)
(here/'independent-quadrature.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(q['passed'] for q in results)
print('PASS',len(results))
