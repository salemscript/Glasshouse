"""Differentiate stored potential/gradient answers against independently transcribed fields."""
import sympy as s,json
from pathlib import Path
H=Path(__file__).parent;D=json.loads((H.parent/'chapter-16.json').read_text());x,y,z=s.symbols('x y z',real=True);loc=dict(x=x,y=y,z=z);checks=[]
def expression(a):return s.sympify(a.replace(' + C','').replace('^','**'),locals=loc)
def parts(qid):g=D[qid]['grader'];return g.get('parts',[g])
F3={4:[y*y-2*x,2*x*y],5:[y*y*s.exp(x*y),(1+x*y)*s.exp(x*y)],6:[y*s.exp(x),s.exp(x)+s.exp(y)],7:[y*s.exp(x)+s.sin(y),s.exp(x)+x*s.cos(y)],8:[2*x*y+y**-2,x*x-2*x*y**-3],9:[y*y*s.cos(x)+s.cos(y),2*y*s.sin(x)-x*s.sin(y)],10:[s.log(y)+y/x,s.log(x)+x/y],12:[3+2*x*y*y,2*x*x*y],13:[x*x*y**3,x**3*y*y],14:[(1+x*y)*s.exp(x*y),x*x*s.exp(x*y)],15:[y*z,x*z,x*y+2*z],16:[y*y*z+2*x*z*z,2*x*y*z,x*y*y+2*x*x*z],17:[y*z*s.exp(x*z),s.exp(x*z),x*y*s.exp(x*z)],18:[s.sin(y),x*s.cos(y)+s.cos(z),-y*s.sin(z)],19:[2*x*s.exp(-y),2*y-x*x*s.exp(-y)],20:[s.sin(y),x*s.cos(y)-s.sin(y)]}
for k,F in F3.items():
 qid=f'calculus-section-16-3-{k}';fs=parts(qid);f=expression(next(a['answer'] for a in fs if 'potential' in a['label'].lower()))
 for coord,component in zip((x,y,z),F):
  assert s.simplify(s.diff(f,coord)-component)==0,(qid,coord);checks.append(dict(id=qid,coordinate=str(coord),test='stored potential differentiates to source component'))
for k,F in {13:[y*y*z**3,2*x*y*z**3,3*x*y*y*z*z],16:[1,s.sin(z),y*s.cos(z)],17:[s.exp(y*z),x*z*s.exp(y*z),x*y*s.exp(y*z)],18:[s.exp(x)*s.sin(y*z),z*s.exp(x)*s.cos(y*z),y*s.exp(x)*s.cos(y*z)]}.items():
 qid=f'calculus-section-16-5-{k}';f=expression(parts(qid)[1]['answer'])
 for coord,component in zip((x,y,z),F):assert s.simplify(s.diff(f,coord)-component)==0;checks.append(dict(id=qid,coordinate=str(coord),test='stored potential differentiates to source component'))
for k,F in {11:[(1+x*y)*s.exp(x*y),s.exp(y)+x*x*s.exp(x*y)],12:[s.sin(y),x*s.cos(y),-s.sin(z)],13:[4*x**3*y*y-2*x*y**3,2*x**4*y-3*x*x*y*y+4*y**3],14:[s.exp(y),x*s.exp(y)+s.exp(z),y*s.exp(z)]}.items():
 qid=f'calculus-chapter-16-review-{k}';f=expression(next(a['answer'] for a in parts(qid) if 'potential' in a['label'].lower()))
 for coord,component in zip((x,y,z),F):assert s.simplify(s.diff(f,coord)-component)==0;checks.append(dict(id=qid,coordinate=str(coord),test='stored potential differentiates to source component'))
# Source tangent planes checked against both tangent directions and specified point.
u,v=s.symbols('u v',real=True)
tans={33:([u+v,3*u*u,u-v],1,1),34:([u*u+1,v**3+1,u+v],2,1),35:([u*s.cos(v),u*s.sin(v),v],1,s.pi/3),36:([s.sin(u),s.cos(u)*s.sin(v),s.sin(v)],s.pi/6,s.pi/6),37:([u*u,2*u*s.sin(v),u*s.cos(v)],1,0),38:([1-u*u-v*v,v,u],-1,-1)}
for k,(r,a,b) in tans.items():
 qid=f'calculus-section-16-6-{k}';e=expression(parts(qid)[0]['answer']);r=s.Matrix(r);point=r.subs({u:a,v:b});normal=s.Matrix([s.diff(e,w) for w in(x,y,z)])
 assert s.simplify(e.subs(dict(zip((x,y,z),point))))==0;checks.append(dict(id=qid,test='tangent plane contains specified point'))
 for w in(u,v):assert s.simplify(normal.dot(r.diff(w).subs({u:a,v:b})))==0;checks.append(dict(id=qid,test='plane normal perpendicular to source tangent '+str(w)))
(H/'symbolic-audit.json').write_text(json.dumps(dict(passed=len(checks),checks=checks),indent=2)+'\n');print('PASS',len(checks),'independent symbolic checks')
# Finite differences of independently transcribed source fields test stored curl/divergence.
import numpy as np
fields={1:[x*y*y*z*z,x*x*y*z*z,x*x*y*y*z],2:[0,x**3*y*z*z,y**4*z**3],3:[x*y*s.exp(z),0,y*z*s.exp(x)],4:[s.sin(y*z),s.sin(z*x),s.sin(x*y)],5:[s.sqrt(x)/(1+z),s.sqrt(y)/(1+x),s.sqrt(z)/(1+y)],6:[s.log(2*y+3*z),s.log(x+3*z),s.log(x+2*y)],7:[s.exp(x)*s.sin(y),s.exp(y)*s.sin(z),s.exp(z)*s.sin(x)],8:[s.atan(x*y),s.atan(y*z),s.atan(z*x)]}
for k,F in fields.items():
 qid=f'calculus-section-16-5-{k}';fs=parts(qid);storedcurl=[expression(a) for a in fs[0]['answer'].strip('⟨⟩').split(',')];storeddiv=expression(fs[1]['answer']);fn=s.lambdify((x,y,z),F,'numpy');cfn=s.lambdify((x,y,z),storedcurl,'numpy');dfn=s.lambdify((x,y,z),storeddiv,'numpy')
 for point in([.7,1.1,1.3],[1.2,.8,1.4],[.9,1.3,.6]):
  p=np.array(point);h=1e-5;J=np.empty((3,3))
  for j in range(3):d=np.zeros(3);d[j]=h;J[:,j]=(np.asarray(fn(*(p+d)),float)-np.asarray(fn(*(p-d)),float))/(2*h)
  want=np.array([J[2,1]-J[1,2],J[0,2]-J[2,0],J[1,0]-J[0,1]])
  assert np.allclose(cfn(*p),want,rtol=2e-7,atol=2e-8),(qid,'curl');assert np.isclose(dfn(*p),np.trace(J),rtol=2e-7,atol=2e-8),(qid,'div')
  checks.extend([dict(id=qid,test='finite-difference source curl',point=point),dict(id=qid,test='finite-difference source divergence',point=point)])
(H/'symbolic-audit.json').write_text(json.dumps(dict(passed=len(checks),checks=checks),indent=2)+'\n');print('PASS total',len(checks),'symbolic and independent finite-difference checks')
