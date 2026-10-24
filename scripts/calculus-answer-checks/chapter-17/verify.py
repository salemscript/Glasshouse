"""Independent integration checks, coverage and exact coefficient assertions."""
from ode import *
from scipy.integrate import solve_ivp
here=Path(__file__).parent;checks=0;out={}
for path in sorted(here.glob('section[0-9][0-9].json'))+[here/'review.json']:
 batch=json.loads(path.read_text());assert not out.keys()&batch.keys();out.update(batch)
 for case in json.loads(path.with_name(path.stem+'-audit.json').read_text())['differentialChecks']:
  if 'solution' not in case:continue
  abc=list(map(s.sympify,case['coefficients']));rhs=s.sympify(case['forcing'],locals={'x':x});sol=s.sympify(case['solution'],locals={'x':x,'C1':C1,'C2':C2}).subs({C1:R(2,7),C2:-R(3,11)})
  # Evaluate away from singular endpoints, then integrate the source ODE independently.
  fnum=s.lambdify(x,sol,'numpy');dnum=s.lambdify(x,s.diff(sol,x),'numpy');gnum=s.lambdify(x,rhs,'numpy');a,b,c=map(float,abc)
  start=.3;end=.7
  numeric=solve_ivp(lambda z,v:[v[1],(float(gnum(z))-b*v[1]-c*v[0])/a],[start,end],[float(fnum(start)),float(dnum(start))],rtol=2e-10,atol=2e-11,dense_output=True)
  assert numeric.success
  for z in [.4,.5,.7]:
   actual=numeric.sol(z)[0];expected=float(fnum(z));assert abs(actual-expected)<2e-7*(1+abs(expected)),(path,case,z,actual,expected);checks+=1
qs=[q for q in SOURCE if q['chapter']==17];assert set(out)=={q['id'] for q in qs}
fields=0
for qid,v in out.items():
 g=v['grader'];fs=g.get('parts',[g]);assert len(fs)==v['objectiveFieldCount'];fields+=len(fs)
 for r in fs:
  if r['type']=='choice':assert len(set(r['options']))==len(r['options']) and r['answer'] in r['options']
  else:assert math.isfinite(r['answer']) and r['tolerance']>0
# Independently differentiate closed series forms for the first first-order cases.
for expr,lhs in [(s.exp(x),lambda y:s.diff(y,x)-y),(s.exp(x*x/2),lambda y:s.diff(y,x)-x*y),(s.exp(x**3/3),lambda y:s.diff(y,x)-x*x*y),(1/(1-x/3)**2,lambda y:(x-3)*s.diff(y,x)+2*y)]:assert s.simplify(lhs(expr))==0;checks+=1
(here.parent/'chapter-17.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(here/'verification-results.json').write_text(json.dumps(dict(questions=len(out),fields=fields,independentNumericalChecks=checks,missing=[],sourceSHA256=hashlib.sha256((ROOT/'site/books/calculus/chapter-17.pdf').read_bytes()).hexdigest(),limitedTasks=sum(v['grader'].get('complete') is False for v in out.values()),scope='Every source task has an answer contract. Written proofs and drawings are explicitly limited to checked conclusions.'),indent=2)+'\n')
print('PASS',len(out),'questions',fields,'fields',checks,'independent numerical/closed-form checks')
