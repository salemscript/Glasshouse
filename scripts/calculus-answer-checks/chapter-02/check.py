#!/usr/bin/env python3
"""Independent structure, symbolic and numerical checks (development only).
Does not claim to certify every graph reading or every transcription.
"""
import gzip,hashlib,json,math,random
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parents[3]
P=Path(__file__).parent
q=json.loads(gzip.decompress((ROOT/'site/questions/calculus.json.gz').read_bytes()))
qs={x['id']:x for x in q if x['chapter']==2}
data=json.loads((P.parent/'chapter-02.json').read_text())['questions'];checks=0

def ok(v,msg):
 global checks
 assert v,msg
 checks+=1

def field(sec,n,label=None):
 k=f'calculus-section-2-{sec}-{n}';g=data[k]['grader'];ff=g['parts'] if g['type']=='parts' else [g]
 return ff[0] if label is None else next(f for f in ff if f['label']==label)
def numeric(sec,n,val,label=None,tol=1e-8):
 f=field(sec,n,label);ok(f['type']=='numeric',(sec,n,label));ok(abs(f['answer']-float(val))<=tol,(sec,n,label,f['answer'],val))
ok(set(data)==set(qs),'Exact all570IDs')
count=0
for k,row in data.items():
 g=row['grader'];ff=g['parts'] if g['type']=='parts' else [g]
 ok(row.get('objectiveChecksVerified') is True,(k,'verified metadata'))
 ok(row['objectiveFieldCount']==len(ff),(k,'fieldcount'))
 ok(len({f.get('label') for f in ff})==len(ff),(k,'distinct labels'))
 for f in ff:
  count+=1;ok(f['type'] in ['numeric','choice'],(k,'supported type'))
  if f['type']=='numeric':
   ok(math.isfinite(f['answer']) and f.get('tolerance',0)>=0,(k,'finite result/tolerance'))
  else:
   ok(len(set(f['options']))==len(f['options'])>=2,(k,'distinct options'))
   ok(f['options'].count(f['answer'])==1,(k,'unique canonical answer'))
# Independently encode original source expressions; compare symbolic limits.
x,t,h,u=S.symbols('x t h u',real=True)
limits=[(3,3,5*x**3-3*x*x+x-6,x,3),(3,4,(x**4-3*x)*(x*x+5*x+3),x,-1),
(3,5,(t**4-2)/(2*t*t-3*t+2),t,-2),(3,6,S.sqrt(u**4+3*u+6),u,-2),
(3,7,(1+S.real_root(x,3))*(2-6*x*x+x**3),x,8),(3,8,((t*t-2)/(t**3-3*t+5))**2,t,2),
(3,9,S.sqrt((2*x*x+1)/(3*x-2)),x,2),
(3,11,(x*x-6*x+5)/(x-5),x,5),(3,12,(x*x+3*x)/(x*x-x-12),x,-3),
(3,15,(t*t-9)/(2*t*t+7*t+3),t,-3),(3,16,(2*x*x+3*x+1)/(x*x-2*x-3),x,-1),
(3,17,((-5+h)**2-25)/h,h,0),(3,18,((2+h)**3-8)/h,h,0),
(3,19,(x+2)/(x**3+8),x,-2),(3,20,(t**4-1)/(t**3-1),t,1),
(3,21,(S.sqrt(9+h)-3)/h,h,0),(3,22,(S.sqrt(4*u+1)-3)/(u-2),u,2),
(3,23,(1/x-S.Rational(1,3))/(x-3),x,3),(3,24,(1/(3+h)-S.Rational(1,3))/h,h,0),
(3,25,(S.sqrt(1+t)-S.sqrt(1-t))/t,t,0),(3,26,1/t-1/(t*t+t),t,0),
(3,27,(4-S.sqrt(x))/(16*x-x*x),x,16),(3,28,(x*x-4*x+4)/(x**4-3*x*x-4),x,2),
(3,29,1/(t*S.sqrt(1+t))-1/t,t,0),(3,30,(S.sqrt(x*x+9)-5)/(x+4),x,-4),
(3,64,(S.sqrt(6-x)-2)/(S.sqrt(3-x)-1),x,2),
(6,13,(2*x*x-7)/(5*x*x+x-3),x,S.oo),(6,14,S.sqrt((9*x**3+8*x-4)/(3-5*x+x**3)),x,S.oo),
(6,15,(3*x-2)/(2*x+1),x,S.oo),(6,16,(1-x*x)/(x**3-x+1),x,S.oo),
(6,17,(x-2)/(x*x+1),x,-S.oo),(6,18,(4*x**3+6*x*x-2)/(2*x**3-4*x+5),x,-S.oo),
(6,19,(S.sqrt(t)+t*t)/(2*t-t*t),t,S.oo),(6,20,(t-t*S.sqrt(t))/(2*t**S.Rational(3,2)+3*t-5),t,S.oo),
(6,21,(2*x*x+1)**2/((x-1)**2*(x*x+x)),x,S.oo),(6,22,x*x/S.sqrt(x**4+1),x,S.oo),
(6,23,S.sqrt(1+4*x**6)/(2-x**3),x,S.oo),(6,24,S.sqrt(1+4*x**6)/(2-x**3),x,-S.oo),
(6,25,S.sqrt(x+3*x*x)/(4*x-1),x,S.oo),(6,27,S.sqrt(9*x*x+x)-3*x,x,S.oo),
(6,28,S.sqrt(4*x*x+3*x)+2*x,x,-S.oo),(6,35,S.atan(S.exp(x)),x,S.oo),
(6,36,(S.exp(3*x)-S.exp(-3*x))/(S.exp(3*x)+S.exp(-3*x)),x,S.oo),
(6,37,(1-S.exp(x))/(1+2*S.exp(x)),x,S.oo),(6,40,S.atan(S.log(x)),x,0),
(6,42,S.log(2+x)-S.log(1+x),x,S.oo)]
for sec,n,f,v,a in limits:numeric(sec,n,S.limit(f,v,a))
# One-sided absolute-value cancellation: finite -4, not negative infinity.
numeric(3,43,S.limit((2*x-1)/S.Abs(2*x**3-x*x),x,S.Rational(1,2),dir='-'))
# True tangent line data and physically signed velocities.
for n,f,a,lab in [(3,4*x-x*x,1,'a(i) · slope'),(4,x-x**3,1,'a(i) · slope'),(27,3*x*x-x**3,1,'f′(1)'),(28,x**4-2,1,'g′(1)'),(29,5*x/(1+x*x),2,'a · F′(2)')]:numeric(7,n,S.diff(f,x).subs(x,a),lab)
numeric(7,43,S.diff(80*t-6*t*t,t).subs(t,4),'Velocity')
numeric(7,44,S.diff(10+45/(t+1),t).subs(t,4),'Velocity')
# Constructed graph models satisfy every listed numerical condition.
f=x**3/3-2*x*x+3*x
for a,v in [(0,3),(1,0),(2,-1)]:ok(S.diff(f,x).subs(x,a)==v,('2.7#23',a))
g=3+(x-5)*(2-x/5-S.Rational(141,620)*x*x)/(x+5)
for val,target in [(g.subs(x,0),1),(S.diff(g,x).subs(x,0),1),(S.diff(g,x).subs(x,-2),0),(S.limit(g,x,5,dir='-'),3),(S.limit(g,x,-5,dir='+'),S.oo)]:ok(val==target,('2.7#25',val,target))
f=x/(4-x*x)-S.Rational(9,4)*x
ok(S.diff(f,x).subs(x,0)==-2,'2.7#26 derivative');ok(S.simplify(f.subs(x,-x)+f)==0,'2.7#26 odd');ok(S.limit(f,x,2,dir='-')==S.oo,'2.7#26 pole')
# Independent roots for continuity models, compare reported numerical answers.
numeric(5,59,float(S.nsolve(100*S.exp(-x/100)-S.Rational(1,100)*x*x,70)),'b · root to three decimals')
numeric(5,60,float(S.nsolve(S.atan(x)+x-1,.5)),'b · root to three decimals')
# Epsilon-delta bounds: independently sample required inequalities over many eps.
rng=random.Random(27023)
proofs=[(15,lambda x:1+x/3,3,2,lambda e:3*e),
(16,lambda x:2*x-5,4,3,lambda e:e/2),(17,lambda x:1-4*x,-3,13,lambda e:e/4),
(18,lambda x:3*x+5,-2,-1,lambda e:e/3),(19,lambda x:(2+4*x)/3,1,2,lambda e:3*e/4),
(20,lambda x:3-.8*x,10,-5,lambda e:1.25*e),
(21,lambda x:x+2,4,6,lambda e:e),(22,lambda x:3-2*x,-1.5,6,lambda e:e/2),
(25,lambda x:x*x,0,0,lambda e:math.sqrt(e)),(26,lambda x:x**3,0,0,lambda e:e**(1/3)),
(27,abs,0,0,lambda e:e),(29,lambda x:x*x-4*x+5,2,1,lambda e:math.sqrt(e)),
(30,lambda x:x*x+2*x-7,2,1,lambda e:min(1,e/9)),
(31,lambda x:x*x-1,-2,3,lambda e:min(1,e/5)),
(32,lambda x:x**3,2,8,lambda e:min(1,e/19))]
for n,fn,a,L,delta in proofs:
 for _ in range(250):
  eps=10**rng.uniform(-4,2);xx=a+delta(eps)*rng.uniform(-.999,.999)
  ok(abs(fn(xx)-L)<eps+1e-11,('epsilon delta',n,eps,xx))
# Numerical graph estimates are explicitly tolerance-limited. Exact C2/C3 values
# cannot be recovered from qualitative illustration2.8#56; do not invent them.
f56=data['calculus-section-2-8-56']
ok(f56['grader'].get('complete') is False,'2.8#56 no full-drawing completion')
ok(all(f['type']=='choice' for f in f56['grader']['parts']),'2.8#56 qualitative contract')
report=dict(chapter=2,sourceQuestions=len(qs),checkedQuestions=len(data),objectiveFields=count,assertions=checks,sourcePdfSha256=hashlib.sha256((ROOT/'site/books/calculus/chapter-02.pdf').read_bytes()).hexdigest(),coverageComplete=True,limitations=['Recognition checks on proofs, freehand graphs and historical reports do not automatically grade the original written/drawn task.','The coarse position sketch in section2.8 exercise56 supports sign/units recognition; exact numerical acceleration and jerk at10seconds are not uniquely determined by its artwork.','Numerical derivative estimates from tables use the stated centered/one-sided stencil.','Symbolic and numerical checks independently cover selected authored expressions, not every transcription or distractor.'])
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
