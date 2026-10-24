"""Source-reviewed original answer contracts for appendices C and D."""
import gzip,json,random,math
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
SOURCE=json.load(gzip.open(ROOT/'site/questions/calculus.json.gz'))
QS={q['id']:q for q in SOURCE if q['chapter']=='appendix' and q['section'] in ('C','D')}
x,y,a,b,c,t=s.symbols('x y a b c t',real=True)
R=s.Rational;pi=s.pi
OUT={};AUDIT={};CHECKS=[]
def fmt(e):return s.sstr(e).replace('**','^')
def n(label,value,unit='',tol=None):
 v=float(value);assert math.isfinite(v)
 return dict(type='numeric',label=label,answer=v,unit=unit,tolerance=tol if tol is not None else max(1e-8,abs(v)*1e-9))
def choice(label,answer,*wrong):
 assert len(wrong)>=2 and len(set((answer,*wrong)))==len(wrong)+1
 return dict(type='choice',label=label,answer=answer,options=[answer,*wrong])
def exact(label,value):
 value=s.simplify(value)
 if value.has(s.zoo,s.nan,s.oo):return choice(label,'Undefined','0','1')
 return choice(label,fmt(value),fmt(value+1),fmt(value-1))
def put(sec,num,*fields,why,limited=False):
 qid=f'calculus-section-{sec.lower()}-{num}';assert qid in QS and qid not in OUT
 for i,f in enumerate(fields):
  f.update(explanation=why,provenance='explicit-source-inspected-original-answer-contract')
  if f['type']=='choice':random.Random(qid+str(i)).shuffle(f['options'])
 grader=dict(fields[0]) if len(fields)==1 else dict(type='parts',parts=list(fields))
 grader['scope']='Checks the labeled mathematical results. A freehand graph or complete written proof is not automatically assessed.'
 if limited:grader['complete']=False
 OUT[qid]=dict(grader=grader,responsePartPrompt='Use the original textbook question above. Answer each labeled item. Graph and proof questions check their mathematical features or reasoning steps, not the complete drawing or written proof.',objectiveCheckVersion=4,objectiveChecksVerified=True,objectiveFieldCount=len(fields),answerCheckSource=dict(type='source-reviewed-original-calculation',title='Stewart Calculus: Early Transcendentals, 8e',chapter='Appendix '+sec.upper(),sourcePageIndices=sorted(set(p['page'] for p in QS[qid]['parts']))))
 AUDIT[qid]=dict(reasoning=why,sourcePages=sorted(set(p['page']+1 for p in QS[qid]['parts'])),limited=limited,fields=len(fields))
def eqcheck(name,lhs,rhs):
 d=s.trigsimp(s.expand_trig(lhs-rhs));assert s.simplify(d)==0,(name,d);CHECKS.append(dict(name=name,method='independent symbolic identity',pass_=True))
def save():
 assert len(OUT)==129 and set(OUT)==set(QS),set(QS)-set(OUT)
 (HERE.parent/'appendix-cd.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
 (HERE/'source-audit.json').write_text(json.dumps(AUDIT,ensure_ascii=False,indent=2)+'\n')
 (HERE/'symbolic-audit.json').write_text(json.dumps(CHECKS,indent=2)+'\n')
 print('Complete:',len(OUT),'tasks',sum(v['objectiveFieldCount'] for v in OUT.values()),'fields;',len(CHECKS),'symbolic checks')
