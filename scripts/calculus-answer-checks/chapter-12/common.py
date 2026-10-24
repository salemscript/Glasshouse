import json,gzip,math,random,hashlib,re
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
QS={q['id']:q for q in json.loads(gzip.decompress((ROOT/'site/questions/calculus.json.gz').read_bytes())) if q['chapter']==12}
OUT={}; AUDIT={}; TESTS=[]
x=s.symbols('x',real=True)
def fmt(v):
 return s.sstr(v).replace('**','^').replace('*','·').replace('log(','ln(').replace('sqrt(','√(').replace('asin(','arcsin(').replace('atan(','arctan(')
def n(label,value,unit='',tol=1e-7):return dict(type='numeric',label=label,answer=float(value),tolerance=tol,unit=unit)
def c(label,ans,*wrong):
 ans=str(ans)
 wrong=tuple(str(v) for v in wrong)
 if not wrong:wrong=('−('+ans+')','('+ans+') + 1')
 assert ans not in wrong and len(set(wrong))==len(wrong),(label,ans,wrong)
 return dict(type='choice',label=label,answer=ans,options=[ans,*wrong],selectionPrompt='Choose the correct '+label+'.')
def expr(label,e,var=x,constant=''):
 a=fmt(e)+constant
 return c(label,a,fmt(e+var)+constant,fmt(e+var+1)+constant)
def put(sec,num,fields,why,limited=False,suffix=''):
 qid=f'calculus-section-12-{sec}-{num}'+suffix if isinstance(sec,int) else f'calculus-{sec}-{num}'+suffix
 assert qid in QS,qid
 assert qid not in OUT,qid
 if not isinstance(fields,list):fields=[fields]
 for i,f in enumerate(fields):
  f.update(provenance='source-inspected-original-answer-contract',explanation=why)
  if f['type']=='choice':random.Random(qid+'/'+str(i)).shuffle(f['options'])
 scope='Checks the requested numerical results and mathematical selections. A selection does not assess a freehand graph or written proof.'
 grader={**fields[0],'scope':scope} if len(fields)==1 else dict(type='parts',parts=fields,scope=scope)
 if limited:grader['complete']=False
 OUT[qid]=dict(nativePrompt=None,grader=grader,responsePartPrompt='Use the original textbook question above. Enter each labeled numerical result or select its mathematical answer. Graph/proof selections check conclusions, not the drawing or full reasoning.',objectiveChecksVerified=True,objectiveCheckVersion=4,objectiveFieldCount=len(fields),answerCheckSource='Stewart Calculus: Early Transcendentals, 8th edition, supplied Chapter 12 source; original independently checked answer contract.')
 AUDIT[qid]=dict(pages=sorted(set(p['page'] for p in QS[qid]['parts'])),reasoning=why,limited=limited)
def row(sec,num,*fields,why,limited=False):put(sec,num,list(fields),why,limited)
def check(label,expression):
 residual=s.simplify(expression)
 assert residual==0,(label,residual)
 TESTS.append(dict(label=label,residual=str(residual)))
def finish(name):
 folder=Path(__file__).parent
 (folder/(name+'.json')).write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
 (folder/(name+'-audit.json')).write_text(json.dumps(dict(questions=AUDIT,checks=TESTS),ensure_ascii=False,indent=2)+'\n')
 print(name,len(OUT),sum(v['objectiveFieldCount'] for v in OUT.values()),'checks',len(TESTS))

def vec(label,values):return [n(label+' '+axis,v) for axis,v in zip(('x','y','z'),values)]
def V(*v):return s.Matrix(v)
def eq(label,e):return c(label,str(e),str(e)+' + 1',str(e)+' − 1')
