from pathlib import Path
import json,gzip,math,random
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
SOURCE=json.load(gzip.open(ROOT/'site/questions/calculus.json.gz'))
QS={q['id']:q for q in SOURCE if q['chapter']=='appendix' and q['section'] in ['E','H']}
OUT={}; AUDIT={}; VERIFY=[]
x=s.symbols('x',real=True); n,m,i,j=s.symbols('n m i j',integer=True,positive=True); a,r=s.symbols('a r',real=True)
def fmt(v):return s.sstr(s.simplify(v)).replace('**','^').replace('I','i')
def num(label,v,tol=None):
 v=float(v);assert math.isfinite(v)
 return dict(type='numeric',label=label,answer=v,tolerance=tol if tol is not None else max(1e-8,abs(v)*1e-9))
def choice(label,ans,*bad):
 assert len(bad)>=2 and len(set([ans,*bad]))==len(bad)+1
 return dict(type='choice',label=label,answer=ans,options=[ans,*bad])
def expr(label,v):
 v=s.simplify(v)
 return choice(label,fmt(v),fmt(v+1),fmt(v-1))
def row(sec,k,*fields,why,limited=False):
 qid=f'calculus-section-{sec.lower()}-{k}';assert qid in QS and qid not in OUT
 for ix,f in enumerate(fields):
  f['explanation']=why;f['provenance']='explicit-source-inspected-original-answer-contract'
  if f['type']=='choice': random.Random(qid+str(ix)).shuffle(f['options'])
 grader=dict(fields[0]) if len(fields)==1 else dict(type='parts',parts=list(fields))
 if limited:grader['complete']=False
 grader['scope']='Checks the labeled mathematical results. Written proofs, explanations and freehand sketches are not automatically assessed.'
 OUT[qid]=dict(grader=grader,responsePartPrompt='Use the original exercise above. Enter each labeled quantity or select the specified mathematical result. For polar answers use radians in [0, 2π).',objectiveChecksVerified=True,objectiveCheckVersion=4,objectiveFieldCount=len(fields),answerCheckSource=dict(type='source-reviewed-original-calculation',title='Stewart Calculus: Early Transcendentals, 8e',chapter='appendix',section=sec,pages=sorted(set(p['page'] for p in QS[qid]['parts']))))
 AUDIT[qid]=dict(reasoning=why,sourcePages=sorted(set(p['page'] for p in QS[qid]['parts'])),limited=limited,fields=len(fields))
def verify(name,value):
 assert value,name
 VERIFY.append(name)
def save(sec):
 (HERE/(sec.lower()+'.json')).write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
 (HERE/(sec.lower()+'-audit.json')).write_text(json.dumps(dict(questions=AUDIT,independentChecks=VERIFY),ensure_ascii=False,indent=2)+'\n')
 print(sec,len(OUT),sum(q['objectiveFieldCount'] for q in OUT.values()),'checks',len(VERIFY))
