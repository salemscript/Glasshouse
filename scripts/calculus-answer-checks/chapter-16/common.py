import gzip,json,hashlib,random,math,re
from pathlib import Path
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[3]
SOURCE=json.loads(gzip.decompress((ROOT/'site/questions/calculus.json.gz').read_bytes()))
correction_path=ROOT/'scripts/calculus-answer-checks/chapter-16/source-correction.json'
if correction_path.exists():
 correction=json.loads(correction_path.read_text());SOURCE=[q for q in SOURCE if q['id'] not in correction['removeQuestionIds']];present={q['id'] for q in SOURCE};SOURCE.extend(q for q in correction['addQuestions'] if q['id'] not in present)
LIB=json.loads(gzip.decompress((ROOT/'site/questions/answer-library-calculus.json.gz').read_bytes()))['questions']
x=s.symbols('x',real=True); R=s.Rational; pi=s.pi
mp.mp.dps=40

def fmt(e):return s.sstr(e).replace('**','^')
def n(label,value,unit='',tol=None):
 v=float(value);assert math.isfinite(v)
 return dict(type='numeric',label=label,answer=v,unit=unit,tolerance=tol if tol is not None else max(1e-8,abs(v)*1e-9))
def c(label,answer,*wrong):
 if not wrong:wrong=('−('+answer+')','2('+answer+')')
 assert answer not in wrong and len(set(wrong))==len(wrong)
 return dict(type='choice',label=label,answer=answer,options=[answer,*wrong])
def f(label,expr,constant=False):
 ans=fmt(expr)+(' + C' if constant else '')
 wrong=[fmt(2*expr)+(' + C' if constant else ''),fmt(-expr)+(' + C' if constant else '')]
 if len(set([ans,*wrong]))<3:wrong=[ans+' + 1',ans+' − 1']
 return c(label,ans,*wrong)
class Author:
 def __init__(self,ch):self.ch=ch;self.qs={q['id']:q for q in SOURCE if q['chapter']==ch};self.out={};self.notes={};self.integrals=[]
 def put(self,sec,num,fields,why,limited=False,suffix=''):
  qid=f'calculus-section-{self.ch}-{sec}-{num}{suffix}' if isinstance(sec,int) else f'calculus-chapter-{self.ch:02}-{sec}-{num}{suffix}'
  assert qid in self.qs,qid;assert qid not in self.out,qid
  if not isinstance(fields,list):fields=[fields]
  for i,field in enumerate(fields):
   field.update(explanation=why,provenance='explicit-source-inspected-original-answer-contract')
   if field['type']=='choice':random.Random(qid+str(i)).shuffle(field['options'])
  grader={**fields[0]} if len(fields)==1 else dict(type='parts',parts=fields)
  if limited:grader['complete']=False
  grader['scope']='Checks each labeled answer or conclusion. A drawing, proof, open-ended model, or written explanation is not automatically assessed.'
  self.out[qid]=dict(grader=grader,responsePartPrompt='Use the complete original textbook question above. Supply each labeled quantity or select the indicated mathematical conclusion. Drawing/proof checks assess results, not the full drawing or proof.',objectiveCheckVersion=3,objectiveChecksVerified=True,objectiveFieldCount=len(fields),answerCheckSource=dict(type='source-reviewed-original-calculation',title='Stewart Calculus: Early Transcendentals, 8e',chapter=self.ch,pages=sorted(set(p['page'] for p in self.qs[qid]['parts']))))
  self.notes[qid]=why
 def row(self,sec,num,*fields,why='',limited=False,suffix=''):self.put(sec,num,list(fields),why,limited,suffix)
 def save(self):
  here=ROOT/f'scripts/calculus-answer-checks/chapter-{self.ch:02}'
  (here.parent/f'chapter-{self.ch:02}.json').write_text(json.dumps(self.out,ensure_ascii=False,indent=2)+'\n')
  (here/'source-audit.json').write_text(json.dumps(dict(chapter=self.ch,sourceSHA256=hashlib.sha256((ROOT/f'site/books/calculus/chapter-{self.ch:02}.pdf').read_bytes()).hexdigest(),questions=self.notes,integrals=self.integrals,missing=sorted(set(self.qs)-set(self.out))),ensure_ascii=False,indent=2)+'\n')
  print(self.ch,len(self.out),'/',len(self.qs),'fields',sum(len(v['grader'].get('parts',[v['grader']])) for v in self.out.values()),'missing',sorted(set(self.qs)-set(self.out)))

A=Author(16)
t=s.symbols("t",real=True)
def norm(v):return s.sqrt(s.simplify(v.dot(v)))
def V(v,label="Vector"):
 return [n(label+" · "+axis,z) if not s.sympify(z).free_symbols else f(label+" · "+axis,s.simplify(z)) for axis,z in zip(["x","y","z"],v)]
def unit(v):return s.simplify(v/norm(v))
def vec(v):return s.Matrix(v)
y,z,u,v=s.symbols('y z u v',real=True)
def savepart(name):
 here=ROOT/'scripts/calculus-answer-checks/chapter-16';(here/(name+'.json')).write_text(json.dumps(A.out,ensure_ascii=False,indent=2)+'\n');(here/(name+'-audit.json')).write_text(json.dumps(A.notes,ensure_ascii=False,indent=2)+'\n');print(name,len(A.out))
def cv(label,ans):
 ans=s.Matrix(ans);display=lambda a:'⟨'+', '.join(map(fmt,a))+'⟩';return c(label,display(ans),display(ans+s.ones(len(ans),1)),display(ans-s.ones(len(ans),1)))
def integral(expr,a,b):
 expr=s.simplify(expr);val=mp.quad(s.lambdify(t,expr,'mpmath'),[mp.mpf(str(s.N(a,25))),mp.mpf(str(s.N(b,25)))]);A.integrals.append(dict(integrand=str(expr),lower=str(a),upper=str(b),value=float(val)));return float(val)
def line(F,r0,a,b,scalar=False):
 r0=vec(r0);sub=dict(zip((x,y,z),r0));expr=s.sympify(F).subs(sub,simultaneous=True)*norm(r0.diff(t)) if scalar else vec(F).subs(sub,simultaneous=True).dot(r0.diff(t));return integral(expr,a,b)
def seg(F,p,q,scalar=False):return line(F,vec(p)+t*(vec(q)-vec(p)),0,1,scalar)
def curl(F):
 P,Q,R0=map(s.sympify,F);return vec([s.diff(R0,y)-s.diff(Q,z),s.diff(P,z)-s.diff(R0,x),s.diff(Q,x)-s.diff(P,y)])
def div(F):return sum(s.diff(s.sympify(a),b) for a,b in zip(F,(x,y,z)))
def surf(expr,r0,ul,uu,vl,vu,flux=False,sign=1):
 from scipy.integrate import dblquad
 r0=vec(r0);N=r0.diff(u).cross(r0.diff(v));sub=dict(zip((x,y,z),r0));e=vec(expr).subs(sub,simultaneous=True).dot(N)*sign if flux else s.sympify(expr).subs(sub,simultaneous=True)*norm(N)
 e=s.trigsimp(s.simplify(e));fn=s.lambdify((v,u),e,'numpy');lo=s.lambdify(u,vl,'numpy');hi=s.lambdify(u,vu,'numpy');ans=dblquad(fn,float(ul),float(uu),lo,hi,epsabs=1e-9,epsrel=1e-9)[0];return ans
