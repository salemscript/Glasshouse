"""Source-transcribed chapter 7 answer contracts; never modifies the shared bank."""
import json,gzip,hashlib,random,re,math
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
QS={q['id']:q for q in json.loads(gzip.decompress((ROOT/'site/questions/calculus.json.gz').read_bytes())) if q['chapter']==7}
LIB=json.loads((HERE/'legacy-source.json').read_text())
OUT={};AUDIT={};MATH=[]
x=s.symbols('x',real=True);a,b,c,m,n=s.symbols('a b c m n',positive=True)
ENV=dict(x=x,a=a,b=b,c=c,m=m,n=n,ln=s.log,log=s.log,abs=s.Abs,exp=s.exp,sqrt=s.sqrt,sin=s.sin,cos=s.cos,tan=s.tan,sec=s.sec,csc=s.csc,cot=s.cot,asin=s.asin,acos=s.acos,atan=s.atan,sinh=s.sinh,cosh=s.cosh,pi=s.pi,E=s.E)
def P(t):return s.sympify(t,locals=ENV)
def fmt(t):return str(t).replace('**','^').replace('log(','ln(').replace('Abs(','abs(')
def num(label,v,unit='',tol=1e-7):return dict(type='numeric',label=label,answer=float(v),unit=unit,tolerance=tol)
def choice(label,ans,*wrong):
 if not wrong:wrong=('−('+ans+')','2 × ('+ans+')')
 assert ans not in wrong and len(set(wrong))==len(wrong)
 return dict(type='choice',label=label,answer=ans,options=[ans,*wrong])
def put(sec,i,fs,why='',limited=False,suffix=''):
 qid=(f'calculus-section-7-{sec}-{i}' if isinstance(sec,int) else f'calculus-chapter-07-{sec}-{i}')+suffix
 assert qid in QS,qid
 if not isinstance(fs,list):fs=[fs]
 for j,f in enumerate(fs):
  f.update(provenance='source-transcribed-independently-calculated',explanation=why,fieldIndex=j)
  if f['type']=='choice':random.Random(qid+str(j)).shuffle(f['options'])
 scope='Checks the labeled mathematical results. Graphs, proofs, explanations and software output comparisons must still be reviewed separately.'
 g={**fs[0],'scope':scope} if len(fs)==1 else dict(type='parts',parts=fs,scope=scope)
 if limited:g['complete']=False
 OUT[qid]=dict(grader=g,objectiveCheckVersion=2,objectiveChecksVerified=True,objectiveFieldCount=len(fs),responsePartPrompt='Use the complete original textbook question above. '+scope,answerCheckSource={'type':'source-reviewed-exact-question','pdf':'books/calculus/chapter-07.pdf'})
 AUDIT[qid]={'why':why,'limited':limited,'sourcePages':sorted(set(p['page'] for p in QS[qid]['parts']))}
def integ(sec,i,f,F=None,lo=None,hi=None,var='x',limited=False):
 f=P(f);F=P(F) if F is not None else s.integrate(f,x)
 assert not F.has(s.Integral),(sec,i,F)
 MATH.append(dict(id=(f'calculus-section-7-{sec}-{i}' if isinstance(sec,int) else f'calculus-chapter-07-{sec}-{i}'),integrand=str(f),primitive=str(F),lower=str(lo),upper=str(hi)))
 why='Here x is a dummy integration variable (rename it to the source variable if different). Differentiate the displayed primitive to recover the original integrand. Apply upper minus lower values for definite integrals; use a separate constant on every connected real domain.'
 if lo is not None:
  val=s.simplify(F.subs(x,P(str(hi)))-F.subs(x,P(str(lo))))
  if val.has(s.nan,s.zoo):val=s.integrate(f,(x,P(str(lo)),P(str(hi))))
  fs=num('Integral value',s.re(val))
 else:
  text=fmt(F).replace('x',var)+' + C';wrong1=fmt(-F).replace('x',var)+' + C';wrong2=fmt(F+x).replace('x',var)+' + C'
  fs=choice('Antiderivative',text,wrong1,wrong2)
 put(sec,i,fs,why,limited)
# Existing exact contracts: retain reviewed source solutions and objective fields.
for qid,q in QS.items():
 if qid in LIB and LIB[qid].get('grader'):
  e=LIB[qid];g=json.loads(json.dumps(e['grader']));fs=g.get('parts',[g]) if g.get('type')=='parts' else [g]
  sec=int(q['section'].split('.')[1]) if q['section'].startswith('7.') else None
  OUT[qid]=dict(grader=g,objectiveCheckVersion=2,objectiveChecksVerified=True,objectiveFieldCount=len(fs),responsePartPrompt='Use the original textbook question. Check each labeled result below.',answerCheckSource={'type':'source-reviewed-existing-exact-question','pdf':'books/calculus/chapter-07.pdf'})
  AUDIT[qid]={'existing':True,'sourcePages':sorted(set(p['page'] for p in q['parts'])),'nativePrompt':e.get('nativePrompt','')}
# Section 7.5, printed pages 507–508; integrands manually transcribed from page images.
T={
1:('cos(x)/(1-sin(x))','-log(abs(1-sin(x)))'),2:('(3*x+1)**sqrt(2)','(3*x+1)**(sqrt(2)+1)/(3*(sqrt(2)+1))',0,1),3:('sqrt(x)*log(x)','x**(3/2)*(2*log(x)/3-4/9)',1,4),4:('sin(x)**3/cos(x)','cos(x)**2/2-log(abs(cos(x)))'),5:('x/(x**4+2)','atan(x**2/sqrt(2))/(2*sqrt(2))'),6:('x/(2*x+1)**3','-1/(4*(2*x+1))+1/(8*(2*x+1)**2)',0,1),7:('exp(atan(x))/(1+x*x)','exp(atan(x))',-1,1),8:('x*sin(x)*cos(x)','-x*cos(2*x)/4+sin(2*x)/8'),9:('(x+2)/(x*x+3*x-4)','3*log(abs(x-1))/5+2*log(abs(x+4))/5',2,4),10:('cos(1/x)/x**3','-sin(1/x)/x-cos(1/x)'),11:('1/(x**3*sqrt(x*x-1))','sqrt(x*x-1)/(2*x*x)+atan(sqrt(x*x-1))/2'),12:('(2*x-3)/(x**3+3*x)','-log(abs(x))+log(x*x+3)/2+2*atan(x/sqrt(3))/sqrt(3)'),13:('sin(x)**5*cos(x)**4','-cos(x)**5/5+2*cos(x)**7/7-cos(x)**9/9'),14:('log(1+x*x)','x*log(1+x*x)-2*x+2*atan(x)'),15:('x*sec(x)*tan(x)','x*sec(x)-log(abs(sec(x)+tan(x)))'),16:('x*x/sqrt(1-x*x)','asin(x)/2-x*sqrt(1-x*x)/2',0,'sqrt(2)/2'),17:('x*cos(x)**2','x*x/4+x*sin(2*x)/4+cos(2*x)/8',0,'pi'),18:('exp(sqrt(x))/sqrt(x)','2*exp(sqrt(x))',1,4),19:('exp(x+exp(x))','exp(exp(x))'),20:('exp(2)','x*exp(2)'),21:('atan(sqrt(x))','(x+1)*atan(sqrt(x))-sqrt(x)'),22:('log(x)/(x*sqrt(1+log(x)**2))','sqrt(1+log(x)**2)'),23:('(1+sqrt(x))**8','2*(1+sqrt(x))**10/10-2*(1+sqrt(x))**9/9',0,1),24:('(1+tan(x))**2*sec(x)','(sec(x)*tan(x)+log(abs(sec(x)+tan(x))))/2+2*sec(x)'),25:('(1+12*x)/(1+3*x)','4*x-log(abs(1+3*x))',0,1),26:('(3*x*x+1)/(x**3+x*x+x+1)','2*log(x+1)+log(x*x+1)/2-atan(x)',0,1),27:('1/(1+exp(x))','x-log(1+exp(x))'),28:('sin(sqrt(a*x))','2*(sin(sqrt(a*x))-sqrt(a*x)*cos(sqrt(a*x)))/a'),29:('log(x+sqrt(x*x-1))','x*log(x+sqrt(x*x-1))-sqrt(x*x-1)'),31:('sqrt((1+x)/(1-x))','asin(x)-sqrt(1-x*x)'),32:('exp(3/x)/x**2','-exp(3/x)/3',1,3),33:('sqrt(3-2*x-x*x)','(x+1)*sqrt(4-(x+1)**2)/2+2*asin((x+1)/2)'),34:('(1+4*cot(x))/(4-cot(x))','log(abs(4*sin(x)-cos(x)))','pi/4','pi/2'),35:('x/(1+cos(x)**2)',None,'-pi/2','pi/2'),36:('(1+sin(x))/(1+cos(x))','tan(x/2)-log(abs(1+cos(x)))'),37:('tan(x)**3*sec(x)**2','tan(x)**4/4',0,'pi/4'),38:('sin(x)*cot(x)/sec(x)','x/2+sin(2*x)/4','pi/6','pi/3'),39:('sec(x)*tan(x)/(sec(x)**2-sec(x))','log(abs(sec(x)-1))-log(abs(sec(x)))'),40:('sin(6*x)*cos(3*x)','-cos(9*x)/18-cos(3*x)/6',0,'pi'),41:('x*tan(x)**2','x*tan(x)+log(abs(cos(x)))-x*x/2'),42:('atan(x)/x**2','-atan(x)/x+log(abs(x))-log(1+x*x)/2'),43:('sqrt(x)/(1+x**3)','2*atan(x**(3/2))/3'),44:('sqrt(1+exp(x))','2*sqrt(1+exp(x))+log((sqrt(1+exp(x))-1)/(sqrt(1+exp(x))+1))'),45:('x**5*exp(-x**3)','-(x**3+1)*exp(-x**3)/3'),46:('(x-1)*exp(x)/x**2','exp(x)/x'),47:('x**3*(x*x-1)**(-4)','-1/(4*(x*x-1)**2)-1/(6*(x*x-1)**3)'),48:('x*sqrt(2-sqrt(1-x*x))','4*(2-sqrt(1-x*x))**(3/2)/3-2*(2-sqrt(1-x*x))**(5/2)/5',0,1),49:('1/(x*sqrt(4*x+1))','log(abs((sqrt(4*x+1)-1)/(sqrt(4*x+1)+1)))'),50:('1/(x*x*sqrt(4*x+1))','-sqrt(4*x+1)/x-2*log(abs((sqrt(4*x+1)-1)/(sqrt(4*x+1)+1)))'),51:('1/(x*sqrt(4*x*x+1))','log(abs(2*x/(sqrt(4*x*x+1)+1)))'),52:('1/(x*(x**4+1))','log(abs(x))-log(x**4+1)/4'),53:('x*x*sin(m*x)','-x*x*cos(m*x)/m+2*x*sin(m*x)/m**2+2*cos(m*x)/m**3'),54:('(x+sin(x))**2','x**3/3-2*x*cos(x)+2*sin(x)+x/2-sin(2*x)/4'),55:('1/(x+x*sqrt(x))','log(x)-2*log(1+sqrt(x))'),56:('1/(sqrt(x)+x*sqrt(x))','2*atan(sqrt(x))'),57:('x*(x+c)**(1/3)','3*(x+c)**(7/3)/7-3*c*(x+c)**(4/3)/4'),58:('x*log(x)/sqrt(x*x-1)','sqrt(x*x-1)*log(x)-sqrt(x*x-1)+atan(sqrt(x*x-1))'),59:('1/(x**4-16)','log(abs((x-2)/(x+2)))/32-atan(x/2)/16'),60:('1/(x*x*sqrt(4*x*x-1))','sqrt(4*x*x-1)/x'),61:('1/(1+cos(x))','tan(x/2)'),62:('1/(1+cos(x)**2)',None),63:('sqrt(x)*exp(sqrt(x))','2*exp(sqrt(x))*(x-2*sqrt(x)+2)'),64:('1/sqrt(sqrt(x)+1)','4*(sqrt(x)+1)**(3/2)/3-4*sqrt(sqrt(x)+1)'),65:('sin(2*x)/(1+cos(x)**4)','-atan(cos(x)**2)'),66:('log(tan(x))/(sin(x)*cos(x))','log(tan(x))**2/2','pi/4','pi/3'),67:('1/(sqrt(x+1)+sqrt(x))','2*((x+1)**(3/2)-x**(3/2))/3'),68:('x*x/(x**6+3*x**3+2)','log(abs((x**3+1)/(x**3+2)))/3'),69:('sqrt(1+x*x)/x**2','log(x+sqrt(1+x*x))-sqrt(1+x*x)/x',1,'sqrt(3)'),70:('1/(1+2*exp(x)-exp(-x))','log(abs((2*exp(x)-1)/(exp(x)+1)))/3'),71:('exp(2*x)/(1+exp(x))','exp(x)-log(1+exp(x))'),72:('log(x+1)/x**2','-log(x+1)/x+log(abs(x))-log(abs(x+1))'),73:('(x+asin(x))/sqrt(1-x*x)','-sqrt(1-x*x)+asin(x)**2/2'),74:('(4**x+10**x)/2**x','2**x/log(2)+5**x/log(5)'),75:('1/(x*log(x)-x)','log(abs(log(x)-1))'),76:('x*x/sqrt(x*x+1)','(x*sqrt(x*x+1)-log(x+sqrt(x*x+1)))/2'),77:('x*exp(x)/sqrt(1+exp(x))','2*x*sqrt(1+exp(x))-4*sqrt(1+exp(x))-2*log((sqrt(1+exp(x))-1)/(sqrt(1+exp(x))+1))'),78:('(1+sin(x))/(1-sin(x))','2*tan(x)+2*sec(x)-x'),79:('x*sin(x)**2*cos(x)','x*sin(x)**3/3+cos(x)/3-cos(x)**3/9'),80:('sec(x)*cos(2*x)/(sin(x)+sec(x))','log(1+sin(x)*cos(x))'),82:('sin(x)*cos(x)/(sin(x)**4+cos(x)**4)','atan(2*sin(x)**2-1)/2'),83:('(2*x*x+1)*exp(x*x)','x*exp(x*x)')}
for i,v in T.items():
 if i in (35,62):continue
 integ(5,i,*v)
put(5,30,num('Integral value',s.E**2+s.exp(-1)-2),'Split the absolute value at x=0 and integrate 1−e^x on [−1,0], e^x−1 on [0,2].')
put(5,35,num('Integral value',0),'The integrand is odd and continuous on the symmetric interval.')
put(5,62,choice('Antiderivative on each tan-continuity interval','atan(tan(x)/sqrt(2))/sqrt(2) + C','sqrt(2)*atan(tan(x)/sqrt(2)) + C','atan(tan(x)) + C'),'Set u=tan(x), giving ∫du/(u²+2). Choose constants separately on the tangent intervals and join continuously if a global primitive is required.')
put(5,81,choice('Local antiderivative (choose sign by interval)','2 sign(cos(x/2)−sin(x/2)) [sin(x/2)+cos(x/2)] + C','2[sin(x/2)+cos(x/2)] + C on every real interval','−cos(x) + C'),'sqrt(1−sin x)=|cos(x/2)−sin(x/2)|. The displayed sign is fixed on each interval between its zeros; integration constants must join pieces continuously.')
put(5,84,[choice('(a) integral from 1 to 2','F(ln 2)−F(0)','F(2)−F(1)','F(1)−F(2)'),choice('(b) integral from 2 to 3','F(ln(ln 3))−F(ln(ln 2))','F(ln 3)−F(ln 2)','F(3)−F(2)')],'For (a) x=e^t; for (b) x=exp(exp(t)); each transformed integrand is exp(exp(t)).')

def save():
 (HERE.parent/'chapter-07.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
 (HERE/'source-audit.json').write_text(json.dumps({'sourceSha256':hashlib.sha256((ROOT/'site/books/calculus/chapter-07.pdf').read_bytes()).hexdigest(),'questions':AUDIT,'missing':[k for k in QS if k not in OUT]},ensure_ascii=False,indent=2)+'\n')
 (HERE/'quadrature-cases.json').write_text(json.dumps(QUAD,indent=2)+'\n')
 (HERE/'mathematical-cases.json').write_text(json.dumps(MATH,indent=2)+'\n')
 print('Chapter 7:',len(OUT),'/',len(QS),flush=True)
exec((HERE/"sections-1-4.py").read_text())
exec((HERE/"section-8.py").read_text())
exec((HERE/"section-6.py").read_text())
exec((HERE/"section-7.py").read_text())
exec((HERE/"review.py").read_text())
exec((HERE/"problems-plus.py").read_text())
exec((HERE/"corrections-tables.py").read_text())
save()
