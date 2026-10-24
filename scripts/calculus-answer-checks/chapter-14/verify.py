"""Independent finite-difference, reduced-parameter and schema checks for Chapter14."""
from common import *
import ast,numpy as np
from scipy.optimize import minimize_scalar
D=ROOT/'scripts/calculus-answer-checks/chapter-14';checks=[]
def check(label,condition):
 assert condition,label
 checks.append(label)
def records(name):return json.loads((D/(name+'.json')).read_text())
def fields(rec):return rec['grader'].get('parts',[rec['grader']])
# Execute only source declarations and dictionary expressions; do not use symbolic diff results.
namespace=dict(globals());namespace.update(dict(a=s.Symbol('a',real=True),b=s.Symbol('b',real=True),c0=s.Symbol('c',real=True),d=s.Symbol('d',real=True)))
for name in ['section03','section05']:
 ns=dict(globals())
 for node in ast.parse((D/(name+'.py')).read_text()).body:
  if isinstance(node,ast.Assign) and any(isinstance(v,ast.Name) and v.id in ['exprs','data','data2'] for v in node.targets):exec(compile(ast.Module(body=[node],type_ignores=[]),'source-declarations','exec'),ns)
  elif isinstance(node,ast.Assign) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and node.value.func.attr=='symbols':exec(compile(ast.Module(body=[node],type_ignores=[]),'symbols','exec'),ns)
 if name=='section03':cases=[(k,expr,vs) for k,(expr,vs) in ns['exprs'].items()]
 else:cases=[(k,expr,[t]) for k,expr in ns['data'].items()]+[(k,expr,[ns['ss'],t]) for k,expr in ns['data2'].items()]
 for k,expr,variables in cases:
  fs=fields(records(name)[f'calculus-section-14-{3 if name=="section03" else 5}-{k}'])
  vals={vv:1.23+.13*i for i,vv in enumerate(sorted(expr.free_symbols,key=str))}
  # Avoid square-root cancellation in source5.7 and logarithm domain errors by selecting s>t.
  if name=='section05' and ns.get('ss') in vals:vals[ns['ss']]=1.7;vals[t]=.8
  for j,var in enumerate(variables):
   h=1e-5;vp={**vals,var:vals[var]+h};vm={**vals,var:vals[var]-h}
   finite=(float(expr.subs(vp))-float(expr.subs(vm)))/(2*h)
   ans=s.sympify(fs[j]['answer'].replace('^','**'),locals={str(vv):vv for vv in expr.free_symbols})
   exact=float(ans.subs(vals));check(f'{name}#{k} derivative {var}',abs(finite-exact)<2e-4*max(1,abs(exact)))
# Independent reduced-variable optimizations for exercises8.47–48.
num=records('section08-calculation-audit')['constrainedNumerics']
# For47 t=x+z=1/y, w=x-z. Solve the ellipsoid quadratic in w.
# Discriminant =25920−5184t²−2880/t²; allowed t² roots.
roots=np.roots([5184,-25920,2880]);lo,hi=sorted(np.sqrt(roots));vals=[]
for sign in [-1,1]:
 for branch in [-1,1]:
  def ff(q):
   tt=sign*q;disc=max(0,25920-5184*tt*tt-2880/(tt*tt));ww=(54*tt+branch*np.sqrt(disc))/90
   return np.exp(ww)/tt
  grid=np.linspace(lo,hi,2001);gv=np.array([ff(v) for v in grid]);vals.extend([gv[0],gv[-1]])
  for i in range(1,len(grid)-1):
   if (gv[i]-gv[i-1])*(gv[i+1]-gv[i])<=0:
    signopt=1 if gv[i]<gv[i-1] else -1
    res=minimize_scalar(lambda q:signopt*ff(q),bounds=(grid[i-1],grid[i+1]),method='bounded',options={'xatol':1e-14});vals.append(ff(res.x))
check('8.47 global minimum via four 1D branches',abs(min(vals)-num['47'][1]['value'])<1e-6)
check('8.47 global maximum via four 1D branches',abs(max(vals)-num['47'][0]['value'])<1e-6)
# For48 x=2cosθ,z=2sinθ; y is either square-root branch.
vals=[]
for branch in [-1,1]:
 def ff(q):
  xx=2*np.cos(q);zz=2*np.sin(q);rad=xx*xx-zz
  return xx+zz+branch*np.sqrt(max(0,rad)) if rad>=-1e-12 else np.nan
 grid=np.linspace(0,2*np.pi,20001);gv=np.array([ff(v) for v in grid])
 for i in range(1,len(grid)-1):
  if np.isfinite(gv[i-1:i+2]).all() and (gv[i]-gv[i-1])*(gv[i+1]-gv[i])<=0:
   signopt=1 if gv[i]<gv[i-1] else -1
   res=minimize_scalar(lambda q:signopt*ff(q),bounds=(grid[i-1],grid[i+1]),method='bounded',options={'xatol':1e-14});vals.append(ff(res.x))
check('8.48 global minimum via both circle branches',abs(min(vals)-num['48'][1]['value'])<1e-6)
check('8.48 global maximum via both circle branches',abs(max(vals)-num['48'][0]['value'])<1e-6)
# Domain/source anomalies and exact elementary substitutions.
check('3.43 real log undefined',((1-s.sqrt(1+4+4))/(1+s.sqrt(1+4+4)))==-R(1,2))
check('3.76c Laplacian nonzero',s.diff(x**3+3*x*y*y,x,2)+s.diff(x**3+3*x*y*y,y,2)==12*x)
for p0 in [(R(19,3),R(14,3),R(19,3)),(-7,-2,-7)]:check('6.60 sphere '+str(p0),sum(v*v for v in p0)==102)
for i,p0 in enumerate([(R(1,2),)*3,(-1,-1,2)]):check('8.45 constraints '+str(i),p0[2]==p0[0]**2+p0[1]**2 and p0[0]+p0[1]+2*p0[2]==2)
for p0 in [(R(4,13),-R(3,13),R(5,13)),(-R(4,3),1,R(5,3))]:check('8.46 constraints '+str(p0),p0[2]**2==p0[0]**2+p0[1]**2 and 4*p0[0]-3*p0[1]+8*p0[2]==5)
# Exact record inventory and every grader field.
merged={}
for name in [f'section{i:02}' for i in range(1,9)]+['section07-projects','section08-projects','review','plus']:
 for qid,rec in records(name).items():
  check('unique '+qid,qid not in merged);merged[qid]=rec
  for j,field in enumerate(fields(rec)):
   if field['type']=='numeric':check('numeric '+qid+str(j),math.isfinite(field['answer']) and field['tolerance']>0)
   else:check('choice '+qid+str(j),field['answer'] in field['options'] and len(set(field['options']))==len(field['options']))
expected={q['id'] for q in SOURCE if q['chapter']==14};check('all646 source IDs',set(merged)==expected and len(merged)==646)
(D.parent/'chapter-14.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n')
(D/'verification.json').write_text(json.dumps({'passed':len(checks),'records':len(merged),'fields':sum(len(fields(q)) for q in merged.values()),'checks':checks},indent=2)+'\n')
print('PASS',len(checks),'checks;',len(merged),'records')
