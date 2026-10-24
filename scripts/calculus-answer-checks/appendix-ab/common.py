import gzip,json,math,random,hashlib
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=json.load(gzip.open(ROOT/'site/questions/calculus.json.gz'))
QS={q['id']:q for q in SOURCE if q['chapter']=='appendix' and q['section'] in ('A','B')}
x,y=s.symbols('x y',real=True);R=s.Rational
out={};audit={};checks=[]
def fmt(e):return s.sstr(e).replace('**','^').replace('sqrt','√')
def n(label,value,unit=''):
 value=float(value);assert math.isfinite(value)
 return dict(type='numeric',label=label,answer=value,unit=unit,tolerance=max(1e-9,abs(value)*1e-9))
def c(label,answer,*wrong):
 assert len(wrong)>=2 and len(set([answer,*wrong]))==len(wrong)+1,(label,answer,wrong)
 return dict(type='choice',label=label,answer=answer,options=[answer,*wrong])
def expr(label,e):
 e=s.sympify(e)
 return c(label,fmt(e),fmt(e+1),fmt(e-1))
def put(sec,num,*fields,why,limited=False,prompt=None):
 qid=f'calculus-section-{sec.lower()}-{num}';assert qid in QS and qid not in out
 for i,f in enumerate(fields):
  f.update(explanation=why,provenance='explicit-source-inspected-original-calculation')
  if f['type']=='choice':random.Random(qid+str(i)).shuffle(f['options'])
 g=fields[0].copy() if len(fields)==1 else dict(type='parts',parts=list(fields))
 if limited:g['complete']=False
 g['scope']='Checks the labeled mathematical results. Written proofs and freehand graphs are not automatically assessed.'
 out[qid]=dict(grader=g,responsePartPrompt=prompt or 'Use the original textbook question above. Enter each labeled value or choose the indicated exact mathematical result.',objectiveCheckVersion=4,objectiveChecksVerified=True,objectiveFieldCount=len(fields),answerCheckSource=dict(type='source-reviewed-original-calculation',title='Stewart Calculus: Early Transcendentals, 8e',chapter='appendix',section=sec,pages=sorted({p['page'] for p in QS[qid]['parts']})))
 audit[qid]=dict(reasoning=why,fields=len(fields),limited=limited)
def check(label,condition):
 assert condition,label
 checks.append(label)
def save(name):
 (HERE/(name+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 (HERE/(name+'-audit.json')).write_text(json.dumps({'questions':audit,'independentChecks':checks},ensure_ascii=False,indent=2)+'\n')
 print(name,len(out),'tasks',sum(v['objectiveFieldCount'] for v in out.values()),'fields',len(checks),'checks')
