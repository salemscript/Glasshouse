import json,gzip,random,math
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
SOURCE=json.load(gzip.open(ROOT/'site/questions/calculus.json.gz'))
x,y,a,b,h,t=s.symbols('x y a b h t',real=True)
R=s.Rational

def n(label,v,unit='',tol=None):
 v=float(v);assert math.isfinite(v)
 return dict(type='numeric',label=label,answer=v,unit=unit,tolerance=max(1e-8,abs(v)*1e-9) if tol is None else tol)
def c(label,answer,*wrong):
 assert len(set([answer,*wrong]))==1+len(wrong) and wrong
 return dict(type='choice',label=label,answer=answer,options=[answer,*wrong])
def f(label,expr):
 expr=s.sympify(expr);fmt=lambda v:s.sstr(v).replace('**','^')
 return c(label,fmt(expr),fmt(expr+1),fmt(expr-1))
class Author:
 def __init__(self,chapter,section=None):
  self.chapter=chapter;self.qs={q['id']:q for q in SOURCE if q['chapter']==chapter and (section is None or q['section']==section)};self.out={};self.notes={}
 def row(self,qid,*fields,why,limited=False):
  assert qid in self.qs and qid not in self.out,qid
  for i,field in enumerate(fields):
   field.update(explanation=why,provenance='explicit-source-inspected-original-answer-contract')
   if field['type']=='choice':random.Random(qid+str(i)).shuffle(field['options'])
  grader=dict(fields[0]) if len(fields)==1 else dict(type='parts',parts=list(fields))
  if limited:grader['complete']=False
  grader['scope']='Checks each labeled answer or conclusion. A drawing, proof, or written explanation is not automatically assessed.'
  self.out[qid]=dict(grader=grader,responsePartPrompt='Use the original textbook question above. Answer each labeled part; graph and proof questions check the stated mathematical results, not your drawing or full proof.',objectiveCheckVersion=4,objectiveChecksVerified=True,objectiveFieldCount=len(fields),answerCheckSource=dict(type='source-reviewed-original-calculation',title='Stewart Calculus: Early Transcendentals, 8e',chapter=self.chapter,pages=sorted({p['page'] for p in self.qs[qid]['parts']})))
  self.notes[qid]=dict(reasoning=why,fields=len(fields),limited=limited)
 def save(self,name):
  assert set(self.out)==set(self.qs),sorted(set(self.qs)-set(self.out))
  (ROOT/f'scripts/calculus-answer-checks/{name}.json').write_text(json.dumps(self.out,ensure_ascii=False,indent=2)+'\n')
  (Path(__file__).parent/f'{name}-audit.json').write_text(json.dumps(self.notes,ensure_ascii=False,indent=2)+'\n')
  print(name,len(self.out),sum(v['objectiveFieldCount'] for v in self.out.values()))
