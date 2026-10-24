"""Explicit source-reviewed Chapter11 contracts, independent of integrated bank."""
import json,gzip,hashlib,random
from pathlib import Path
import sympy as S
import mpmath as mp
mp.mp.dps=45
H=Path(__file__).resolve().parent;R=H.parents[2]
QS={q['id']:q for q in json.load(gzip.open(R/'site/questions/calculus.json.gz','rt')) if q['chapter']==11}
correction=json.loads((H/'source-correction.json').read_text())
for qid in correction['removeQuestionIds']:QS.pop(qid,None)
for q in correction['addQuestions']:QS[q['id']]=q
OUT={};AUDIT={};CASES=[]
n=S.symbols('n',integer=True,positive=True);x=S.symbols('x',real=True);pi=S.pi
ENV=dict(n=n,x=x,pi=pi,E=S.E,ln=S.log,sqrt=S.sqrt,sin=S.sin,cos=S.cos,exp=S.exp,factorial=S.factorial,atan=S.atan)
def P(t):return S.sympify(t,locals=ENV)
def fmt(v):return str(v).replace('**','^').replace('log(','ln(')
def N(v,label='Answer',tol=1e-8,unit=''):return dict(type='numeric',answer=float(v),label=label,tolerance=tol,unit=unit)
def C(ans,*wrong,label='Answer'):
 assert wrong and ans not in wrong and len(set(wrong))==len(wrong)
 return dict(type='choice',answer=ans,options=[ans,*wrong],label=label)
def F(v,label='Formula'):
 v=S.simplify(v)
 return C(fmt(v),fmt(v+1),fmt(v-1),label=label)
def put(sec,num,*fields,why='',limited=False,group='Exercises'):
 qq=[q for q in QS.values() if q['section']==(f'11.{sec}' if isinstance(sec,int) else sec) and q['number']==str(num) and q['subsection']==group];assert len(qq)==1,(sec,num,group);q=qq[0];qid=q['id'];assert qid not in OUT,qid
 for j,f in enumerate(fields):
  f.update(fieldIndex=j,provenance='source-transcribed-independently-calculated',explanation=why)
  if f['type']=='choice':random.Random(qid+str(j)).shuffle(f['options'])
 g=dict(fields[0]) if len(fields)==1 else dict(type='parts',parts=list(fields))
 g['scope']='Checks the labeled mathematical results. Original proofs, drawings and explanations require separate review.'
 if limited:g['complete']=False
 OUT[qid]=dict(grader=g,objectiveChecksVerified=True,objectiveCheckVersion=3,objectiveFieldCount=len(fields),responsePartPrompt='Use the complete original question above; answer each labeled check.',answerCheckSource=dict(type='source-reviewed-exact-question',pdf='books/calculus/chapter-11.pdf'))
 AUDIT[qid]=dict(sourcePages=sorted({p['page'] for p in q['parts']}),why=why,limited=limited)
def seq(i,expr,limit,count=0,limited=False):
 expr=P(expr);fs=[N(expr.subs(n,k),f'a_{k}',tol=.000051 if count==10 else 1e-8) for k in range(1,count+1)]
 if limit is not None:
  fs.append(C('Diverges: '+limit,'Converges to 0','Converges to 1',label='Convergence') if isinstance(limit,str) else N(limit,'Limit'))
 put(1,i,*fs,why='Use the stated index beginning at n=1. For the limit compare dominant powers/exponentials, or squeeze bounded oscillations; divergence to infinity is not finite convergence.',limited=limited)
 CASES.append(dict(kind='sequence',id=f'calculus-section-11-1-{i}',expr=str(expr),limit=str(limit),count=count))
for file in sorted(H.glob('section-*.py')):exec(file.read_text())
for name in ['review.py','problems-plus.py']:
 if (H/name).exists():exec((H/name).read_text())
(H.parent/'chapter-11.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
(H/'source-audit.json').write_text(json.dumps(dict(sourceSHA256=hashlib.sha256((R/'site/books/calculus/chapter-11.pdf').read_bytes()).hexdigest(),questions=AUDIT,missing=[k for k in QS if k not in OUT]),ensure_ascii=False,indent=2)+'\n')
(H/'math-cases.json').write_text(json.dumps(CASES,indent=2)+'\n')
print('Chapter11',len(OUT),'/',len(QS),'fields',sum(e['objectiveFieldCount'] for e in OUT.values()))
