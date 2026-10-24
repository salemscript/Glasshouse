"""Independent panel-polynomial integration and high-precision integral checks."""
import json,sys
from pathlib import Path
import sympy as s
import mpmath as mp
H=Path(__file__).resolve().parent;mp.mp.dps=45
rows=[]
for c in json.loads((H/'quadrature-cases.json').read_text()):
 f=s.sympify(c['f']);x=next(iter(f.free_symbols));ff=s.lambdify(x,f,'mpmath')
 a=mp.mpf(c['a']);b=mp.mpf(c['b']);n=c['n'];h=(b-a)/n;k=c['kind']
 if k in 'LRM':
  offset={'L':0,'R':1,'M':mp.mpf('.5')}[k];value=sum(mp.quad(lambda z:ff(a+(j+offset)*h),[a+j*h,a+(j+1)*h]) for j in range(n))
 else:
  value=mp.mpf(0)
  for j in range(0,n,2 if k=='S' else 1):
   nodes=[a+(j+u)*h for u in ([0,1,2] if k=='S' else [0,1])]
   vals=[ff(z) for z in nodes]
   def interpolant(t):
    return sum(v*mp.fprod((t-z)/(q-z) for z in nodes if z!=q) for q,v in zip(nodes,vals))
   value+=mp.quad(interpolant,[nodes[0],nodes[-1]])
 err=abs(value-mp.mpf(c['value']))
 rows.append(dict(id=c['id'],method=k,n=n,status='pass' if err<mp.mpf('1e-10')*(1+abs(value)) else 'FAIL',difference=str(err)))
patch=json.loads((H.parent/'chapter-07.json').read_text())
for c in json.loads((H/'mathematical-cases.json').read_text()):
 if c['lower']=='None':continue
 f=s.sympify(c['integrand']);syms={str(z):z for z in f.free_symbols};x=syms.get('x',s.Symbol('x'))
 if f.free_symbols-{x}:continue
 ff=s.lambdify(x,f,'mpmath');a=mp.mpf(str(s.N(s.sympify(c['lower']),40)));b=mp.mpf(str(s.N(s.sympify(c['upper']),40)))
 value=mp.quad(ff,[a,(a+b)/2,b]);expected=patch[c['id']]['grader']['answer'];err=abs(value-expected)
 rows.append(dict(id=c['id'],method='independent definite quadrature',status='pass' if err<mp.mpf('1e-8')*(1+abs(value)) else 'FAIL',difference=str(err)))
# Verify table62 by symbolic differentiation, including its lower-order term.
x,a,b=s.symbols('x a b',positive=True)
for n in [2,3,4,7]:
 G=-s.sqrt(a+b*x)/(a*(n-1)*x**(n-1))
 residual=s.simplify(s.diff(G,x)-b*(2*n-3)/(2*a*(n-1)*x**(n-1)*s.sqrt(a+b*x))-1/(x**n*s.sqrt(a+b*x)))
 assert residual==0
 rows.append(dict(id='calculus-chapter-07-review-60',method='symbolic recurrence',n=n,status='pass'))
fails=[r for r in rows if r['status']!='pass'];(H/'numerical-audit.json').write_text(json.dumps(dict(cases=rows,failures=fails),indent=2)+'\n');print('Independent numeric cases',len(rows),'failures',fails);sys.exit(bool(fails))
