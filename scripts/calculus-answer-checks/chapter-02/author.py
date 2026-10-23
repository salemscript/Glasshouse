"""Explicit original answer checks transcribed against the user-supplied chapter PDF.
No graders are inferred from OCR or answer-key prose. Generated patches only.
"""
import gzip,json,math,random,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
SOURCE=json.loads(gzip.decompress((ROOT/'site/questions/calculus.json.gz').read_bytes()))
QS={q['id']:q for q in SOURCE if q['chapter']==2}
ROWS={}
def N(value,label='Your answer',unit='',tol=1e-8):
 return dict(type='numeric',answer=float(value),label=label,unit=unit,tolerance=tol)
def C(answer,*wrong,label='Your answer',why=''):
 assert wrong and answer not in wrong and len(set(wrong))==len(wrong),(answer,wrong)
 return dict(type='choice',answer=answer,options=[answer,*wrong],label=label,explanation=why)
def D(label='Limit'):
 return C('Does not exist','0','Positive infinity','Negative infinity',label=label)
def I(sign=1,label='Limit'):
 return C('Positive infinity' if sign>0 else 'Negative infinity','Negative infinity' if sign>0 else 'Positive infinity','0','Does not exist by oscillation',label=label)
def Y(answer,label='Your answer'):
 return C('Yes' if answer else 'No','No' if answer else 'Yes',label=label)
def TF(answer,label='Truth value'):
 return C('True' if answer else 'False','False' if answer else 'True',label=label)
def add(s,n,*fields,limited=False,reason=''):
 prefix='section-2-'+str(s) if isinstance(s,int) else s
 matches=[q for q in QS.values() if q['sourceSet']==prefix and q['number']==str(n) and 'project-' not in q['id']]
 assert len(matches)==1,(prefix,n,[q['id'] for q in matches]);put(matches[0],fields,limited,reason)
def put(q,fields,limited=False,reason=''):
 assert fields
 for i,f in enumerate(fields):
  f['provenance']='explicit-source-inspected-original-calculation'
  f.setdefault('explanation',reason)
  f.setdefault('hint','Use the original exercise, its side of approach, domain and units. Check the labeled quantity rather than only the form of the expression.')
  if f['type']=='choice':
   random.Random(hashlib.sha256((q['id']+str(i)).encode()).hexdigest()).shuffle(f['options'])
   f['selectionPrompt']='Choose the mathematical result for '+f['label']+'.'
 labels=[x['label'] for x in fields];assert len(labels)==len(set(labels)),(q['id'],labels)
 scope='Checks the displayed numerical values or selected mathematical conclusions. Drawings, written proofs and explanations are not automatically graded.'
 grader={**fields[0],'scope':scope} if len(fields)==1 else dict(type='parts',parts=list(fields),scope=scope)
 if limited or re.search(r'\b(sketch|draw|prove|show|explain|discuss|graph)\b',q['prompt'],re.I):grader['complete']=False
 ROWS[q['id']]=dict(grader=grader,responsePartPrompt='Use the original textbook exercise above and answer each labeled check below.',objectiveCheckVersion=1,objectiveChecksVerified=True,objectiveFieldCount=len(fields),answerCheckSource=dict(book='Stewart, Calculus: Early Transcendentals, 8th edition',chapter=2,sourceSet=q['sourceSet'],exercise=q['number'],pdfPages=sorted({p['page'] for p in q['parts']}),authoringFile='scripts/calculus-answer-checks/chapter-02/author.py',review='Original mathematical results calculated from the source exercise; graph readings have explicit tolerances.'))
def nums(vals,labels=None,unit='',tol=1e-8):
 return [N(v,labels[i] if labels else chr(97+i),unit,tol) for i,v in enumerate(vals)]
# 2.1 Tangent and velocity problems, printed82, global114.
add(1,1,*nums([-44.4,-38.8,-27.8,-22.2,-250/15],['a · t=5','a · t=10','a · t=20','a · t=25','a · t=30'],'gal/min'),N(-33.3,'b · centered estimate','gal/min',.05),N(-33.3,'c · graph estimate','gal/min',3),limited=True)
add(1,2,*nums([418/6,287/4,71,66],['a','b','c','d'],'beats/min'),C('About 69 beats/min near t=42; the estimates vary with the interval','Exactly 418 beats/min','The heart rate is zero','The number of accumulated beats decreases',label='Conclusion'),limited=True)
xs=[1.5,1.9,1.99,1.999,2.5,2.1,2.01,2.001]
add(1,3,*[N(1/(x-1),'a · x='+str(x),tol=5.1e-7) for x in xs],N(1,'b · slope'),C('y=x−3','y=−x+1','y=x−1',label='c · tangent'))
xs=[0,.4,.49,.499,1,.6,.51,.501]
add(1,4,*[N(math.cos(math.pi*x)/(x-.5),'a · x='+str(x),tol=5.1e-7) for x in xs],N(-math.pi,'b · slope',tol=.001),C('y=−π(x−0.5)','y=π(x−0.5)','y=−πx',label='c · tangent'),limited=True)
add(1,5,*[N(-24-16*h,'a · h='+str(h),'ft/s') for h in [.5,.1,.05,.01]],N(-24,'b · instantaneous velocity','ft/s'))
add(1,6,*[N(10-1.86*(1+b),'a · [1,'+str(b)+']','m/s') for b in [2,1.5,1.1,1.01,1.001]],N(6.28,'b · instantaneous velocity','m/s'))
add(1,7,*nums([29.3,32.7,45.6,48.75],['a · [2,4]','a · [3,4]','a · [4,5]','a · [4,6]'],'ft/s'),N(29.3,'b · estimated velocity at t=3','ft/s',4),limited=True)
add(1,8,*[N((2*math.sin(math.pi*b)+3*math.cos(math.pi*b)+3)/(b-1),'a · [1,'+str(b)+']','cm/s',.0001) for b in [2,1.1,1.01,1.001]],N(-2*math.pi,'b · instantaneous velocity','cm/s',.001))
xs=[2,1.5,1.4,1.3,1.2,1.1,.5,.6,.7,.8,.9]
add(1,9,*[N(math.sin(10*math.pi/x)/(x-1),'a · x='+str(x),tol=.000051) for x in xs],C('These sampled slopes do not approach a clear common value','These samples prove that the derivative is zero','These samples prove that the derivative does not exist',label='a · interpretation'),C('The curve oscillates rapidly near these sample points; choose x much closer to 1','The function is discontinuous at x=1','A secant always has the tangent slope',label='b · graph reasoning'),N(-10*math.pi,'c · tangent slope',tol=.01),limited=True)
# 2.3 Limit laws, printed102–104. Section2.3 exercise3 correction retained.
add(3,1,N(-6,'a'),N(-8,'b'),N(2,'c'),N(-6,'d'),D('e'),N(0,'f'))
for n,v in {3:105,4:-4,5:1,6:4,7:0,8:4/9,9:1.5,11:4,12:3/7,15:6/5,16:1/4,17:-10,18:12,19:1/12,20:4/3,21:1/6,22:2/3,23:-1/9,24:-1/9,25:1,26:1,27:1/128,28:0,29:-.5,30:-.8,37:7,38:2,39:0,40:0,41:6,44:1,46:0,51:7,55:-1,56:0,59:8,64:1/2}.items():add(3,n,N(v),limited=n in [39,40,55,56])
# 5: (t^4−2)/(2t²−3t+2) at−2 =14/16; 6 sqrt(u^4+3u+6) at−2=4;
# 7 (1+cuberoot x)(2−6x²+x³) at8=390; 8 ratio squared t→2=(2/7)^2.
add(3,5,N(7/8));add(3,7,N(390));add(3,8,N(4/49));add(3,9,N(1.5))
add(3,10,C('Equality holds only for x≠2; the left side is undefined at 2','Both sides are defined and equal at every real x','The right side is undefined at 2',label='a'),C('Limits depend on nearby values, so removing the common factor is valid for x≠2','The limit requires the value at x=2','The cancellation changes the nearby values',label='b'),limited=True)
for n in [13,14,42]:add(3,n,D())
add(3,43,N(-4));add(3,45,I(-1))
add(3,31,C('3x²','x³','3x',label='Limit as a function of x'))
add(3,32,C('−2/x³, x≠0','2/x³, x≠0','−1/x², x≠0',label='Limit as a function of x'))
add(3,33,N(2/3,'a · graph estimate',tol=.02),N(2/3,'b · table estimate',tol=.001),N(2/3,'c · exact limit'),limited=True)
add(3,34,N(1/(2*math.sqrt(3)),'a · two decimal estimate',tol=.0051),N(1/(2*math.sqrt(3)),'b · four decimal estimate',tol=.000051),N(1/(2*math.sqrt(3)),'c · exact limit'),limited=True)
add(3,35,N(0,'Limit'),C('−x² ≤ x²cos(20πx) ≤ x²; both bounds tend to 0','cos(20πx) tends to infinity','The cosine factor itself tends to 0',label='Squeeze bounds'),limited=True)
add(3,36,N(0,'Limit'),C('−√(x³+x²) ≤ √(x³+x²)sin(π/x) ≤ √(x³+x²) near 0','The sine factor has limit zero','The radicand is negative throughout a neighborhood of 0',label='Squeeze bounds'),limited=True)
add(3,47,N(1,'b(i)'),N(-1,'b(ii)'),D('b(iii)'),N(1,'b(iv)'),C('y=−1 for x<0, y=1 for x>0, and f(0)=0','y=0 for all x','y=x',label='a · graph description'),limited=True)
add(3,48,N(1,'a(i)'),N(-1,'a(ii)'),D('a(iii)'),N(-1,'a(iv)'),N(1,'a(v)'),D('a(vi)'),C('a=nπ for every integer n','Only a=0','Every real a',label='b · failure set'),limited=True)
add(3,49,N(5,'a(i)'),N(-5,'a(ii)'),Y(False,'b · limit exists'),C('g(x)=x+3 for x>2 and g(x)=−x−3 for x<2, with no value at 2','g(x)=x+3 on both sides','g(x)=|x+3|',label='c · graph description'),limited=True)
add(3,50,N(2,'a · left limit'),N(1,'a · right limit'),Y(False,'b · limit exists'),C('Open circle (1,2) on y=x²+1; closed circle (1,1) on y=(x−2)²','Closed circle (1,2) and open circle (1,1)','Both pieces meet at (1,1)',label='c · graph'),limited=True)
add(3,52,N(1,'a(i)'),N(1,'a(ii)'),N(3,'a(iii)'),N(-2,'a(iv)'),N(-1,'a(v)'),D('a(vi)'),limited=True)
add(3,53,N(-2,'a(i)'),D('a(ii)'),N(-3,'a(iii)'),C('n−1','n','n+1',label='b(i)'),C('n','n−1','n+1',label='b(ii)'),C('All nonintegers a','All integers a','All real a',label='c'))
add(3,54,N(0,'b(i)'),N(0,'b(ii)'),N(-1,'b(iii)'),D('b(iv)'),C('Interior a other than ±π/2; one-sided limits exist at the domain endpoints','All a including ±π/2','Only a=0',label='c · existence set'),limited=True)
add(3,57,C('Apply the sum, constant-multiple and power laws to the polynomial terms','Every polynomial has a zero derivative','Only constant polynomials have this limit',label='Proof method'),limited=True)
add(3,58,C('Apply the quotient law where the denominator is nonzero','The quotient law applies even when the denominator tends to zero','Every rational function has limit zero',label='Proof method'),limited=True)
add(3,60,N(0,'a'),N(0,'b'))
add(3,61,N(0,'Limit'),C('0≤f(x)≤x²; squeeze as x→0','f is continuous at every rational point','f(x)=x² at every x',label='Proof bound'),limited=True)
add(3,62,C('f(x)=1/x, g(x)=−1/x at a=0 gives f+g=0','f(x)=x, g(x)=−x at a=0 has neither limit','f(x)=1/x, g(x)=1/x has sum 0',label='Valid example'),limited=True)
add(3,63,C('f(x)=sgn(x), g(x)=sgn(x) at a=0 gives product 1 off 0','f(x)=x and g(x)=x at 0 have neither limit','f(x)=1/x and g(x)=1/x have finite product limit',label='Valid example'),limited=True)
add(3,65,N(15,'a'),N(-1,'Limit'))
# numerator at−2:12−2a+a+3=15−a; factor (x+2)(3x+9) / ((x+2)(x−1)) ->−1.
add(3,66,C('R tends to (4,0)','R tends to (0,0)','R tends to (2,0)',label='Limiting point'),limited=True)
add(3,2,N(1,'a'),D('b'),N(2,'c'),D('d'),N(-4,'e'),N(5,'f'))

# 2.4 Precise definition, printed113–114. Numerical delta checks explicitly
# request the largest symmetric radius; choosing a sufficient symbolic bound is
# an objective adaptation and never claims to grade a full proof.
def bisect(fn,target,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2
for n,v in {1:.1,2:.4,3:1.44,4:math.sqrt(1.5)-1,5:math.atan(1.2)-math.pi/4,6:1/3}.items():
 add(4,n,N(v,'Largest symmetric δ',tol=1e-5),limited=True)
add(4,7,*[N(bisect(lambda x:x**3-3*x+4,6+e,2,3)-2,'Largest δ for ε='+str(e),tol=1e-5) for e in [.2,.1]],limited=True)
add(4,8,*[N(bisect(lambda x:math.expm1(2*x)/x if x else 2,2+e,0,1),'Largest δ for ε='+str(e),tol=1e-5) for e in [.5,.1]],limited=True)
add(4,9,N(math.expm1(.01),'a · largest δ',tol=1e-6),I(1,'b · right-hand limit'),limited=True)
add(4,10,N(math.asin(1/math.sqrt(500)),'a · largest δ',tol=1e-6),N(math.asin(1/math.sqrt(1000)),'b · largest δ',tol=1e-6),limited=True)
r=math.sqrt(1000/math.pi);dr=math.sqrt(1005/math.pi)-r
add(4,11,N(r,'a · radius','cm',.0001),N(dr,'b · largest symmetric radius tolerance','cm',.00001),C('x=radius; f(x)=πx²; a=√(1000/π); L=1000; ε=5','x=area; f(x)=x/π; a=1000; L=0; ε=5','x=radius; f(x)=2πx; a=1000; L=5',label='c · limit quantities'),N(dr,'c · δ','cm',.00001))
power=lambda T:(-2.155+math.sqrt(2.155**2+.4*(T-20)))/.2
w=power(200);dw=min(w-power(199),power(201)-w)
add(4,12,N(w,'a · input power','W',.0001),N(power(199),'b · minimum wattage','W',.0001),N(power(201),'b · maximum wattage','W',.0001),C('x=wattage; f(x)=T(x); a≈33; L=200; ε=1','x=temperature; f(x)=wattage; L=1; ε=200','x=radius; f(x)=πx²; L=200',label='c · quantities'),N(dw,'c · largest δ','W',.00001))
add(4,13,N(.025,'a · largest δ'),N(.0025,'b · largest δ'))
add(4,14,N(.02,'ε=0.1 · largest δ'),N(.01,'ε=0.05 · largest δ'),N(.002,'ε=0.01 · largest δ'))
for n,ans,w1,w2 in [
(15,'δ=3ε','δ=ε/3','δ=3/ε'),(16,'δ=ε/2','δ=2ε','δ=2/ε'),
(17,'δ=ε/4','δ=4ε','δ=4/ε'),(18,'δ=ε/3','δ=3ε','δ=3/ε'),
(19,'δ=3ε/4','δ=4ε/3','δ=3/(4ε)'),(20,'δ=5ε/4','δ=4ε/5','δ=5/(4ε)'),
(21,'δ=ε','δ=2ε','δ=1/ε'),(22,'δ=ε/2','δ=2ε','δ=2/ε'),
(23,'δ=ε','δ=1/ε','δ=−ε'),(24,'Any δ>0','Only δ=0','δ must be negative'),
(25,'δ=√ε','δ=ε²','δ=1/√ε'),(26,'δ=ε^(1/3)','δ=ε³','δ=−ε'),
(27,'δ=ε','δ=−ε','δ=1/ε'),(28,'δ=ε^8','δ=ε^(1/8)','δ=−ε^8'),
(29,'δ=√ε','δ=ε²','δ=−√ε'),
(30,'δ=min(1,ε/9)','δ=min(1,9ε)','δ=−ε'),
(31,'δ=min(1,ε/5)','δ=min(1,5ε)','δ=−ε'),
(32,'δ=min(1,ε/19)','δ=min(1,19ε)','δ=−ε')]:
 add(4,n,C(ans,w1,w2,label='A sufficient δ for every ε>0'),limited=True)
# n30 centered2: |x²+2x−8|=|x−2||x+4|<7δ if δ≤1;9 also safe.
# n31 centered−2: |x²−4|=|x+2||x−2|<5δ if δ≤1.
# n32 centered2: x²+2x+4<19 if |x−2|<1.
add(4,33,C('If |x−3|<2 then |x+3|<8, so |x²−9|<8δ≤ε','If |x−3|<2 then |x+3|<2','δ=ε/8 works without any bound on |x+3|',label='Why δ=min(2,ε/8) works'),limited=True)
add(4,34,C('δ=√(9+ε)−3','δ=√(9+ε)+3','δ=ε²',label='Largest symmetric δ'),limited=True)
# strictly increasing cubic; positive-side displacement is the smaller bound.
e=.4;d=bisect(lambda x:x**3+x+1,3+e,1,2)-1
add(4,35,N(d,'a · graph δ',tol=.0001),C('δ=r−1, where r is the unique real root of r³+r=2+ε','δ=ε³','δ=1/r, where r³+r=2+ε',label='b · largest δ'),N(d,'c · δ for ε=0.4',tol=.0001),limited=True)
add(4,36,C('δ=min(1,2ε), since |x|>1 and |1/x−1/2|<|x−2|/2','δ=2/ε with no restriction on x','δ=−ε',label='Sufficient δ'),limited=True)
add(4,37,C('δ=ε√a for x≥0; divide |x−a| by √x+√a≥√a','δ=−ε√a','δ=ε/√a always suffices for every a>0',label='Sufficient δ'),limited=True)
add(4,38,D('Limit'),C('The one-sided limits are 0 and 1, so they cannot share L','H(t) tends to 1/2 from both sides','Changing H(0) to 1/2 creates the limit',label='Contradiction'),limited=True)
add(4,39,D('Limit'),C('Every neighborhood contains rational values with f=0 and irrational values with f=1','There are no irrational numbers near 0','f(0)=0 forces its limit to be 0',label='Reason'),limited=True)
add(4,40,C('A two-sided limit equals L iff both one-sided limits equal L; use min(δleft,δright)','A two-sided limit exists if just one one-sided limit exists','The two one-sided limits may be unequal',label='Theorem'),limited=True)
add(4,41,C('0<|x+3|<0.1','|x+3|>0.1','x=−3',label='Required distance'))
add(4,42,C('δ=M^(−1/4) for M>0','δ=M^4','δ=−M^(−1/4)',label='Sufficient δ'),limited=True)
add(4,43,C('For any M<0 take δ=e^M; 0<x<δ implies ln x<M','Take δ=−e^M','ln x stays positive near zero',label='Proof condition'),limited=True)
add(4,44,I(1,'a · sum'),I(1,'b · product c>0'),I(-1,'c · product c<0'),limited=True)

# 2.6 Limits at infinity, printed137–140. Graphs visually reviewed.
add(6,1,C('As x grows without bound, f(x) approaches 5','f(5)=infinity','x approaches 5 while f grows',label='a'),C('As x decreases without bound, f(x) approaches 3','f(3)=negative infinity','f approaches negative infinity',label='b'),limited=True)
add(6,2,C('A graph may meet x=a at an isolated defined point even if x=a is a vertical asymptote; it may cross a horizontal asymptote','A graph can never intersect either kind of asymptote','A graph can cross a vertical asymptote only when continuous there',label='a'),C('Zero, one, or two horizontal asymptotes','Exactly one for every function','Arbitrarily many distinct horizontal asymptotes',label='b'),limited=True)
add(6,3,N(-2,'a'),N(2,'b'),I(1,'c'),I(-1,'d'),C('x=1, x=3; y=2, y=−2','x=0; y=1','x=−2, x=2; y=3',label='e · asymptotes'))
add(6,4,N(2,'a'),N(-1,'b'),I(-1,'c'),I(-1,'d'),I(1,'e'),C('x=0, x=2; y=−1, y=2','x=1; y=0','x=−1, x=2; y=1',label='f · asymptotes'))
models={5:('−(10/π)arctan(x)−1/x²','(10/π)arctan(x)−1/x²','−(10/π)arctan(x)+1/x²'),6:('1/(x−2)²+1/(x+2)−3/[4(1+x²)]','−1/(x−2)²+1/(x+2)−3/[4(1+x²)]','1/(x−2)²−1/(x+2)+1/4'),7:('e^x+1/x−1/(x−2)²','e^x−1/x+1/(x−2)²','e^(−x)+1/x−1/(x−2)²'),8:('(6/π)arctan(x)−x/(x²−4)','(6/π)arctan(x)+x/(x²−4)','(6/π)arctan(x)−1/(x−2)'),10:('2−162/(x²−9)²','2+162/(x²−9)²','2−162/(x−3)²')}
for n,options in models.items():add(6,n,C(*options,label='One formula satisfying all given graph conditions'),limited=True)
add(6,9,C('x+4 for x<0; 3 at 0; 2−x/(4−x) for 0<x<4; 3+1/(x−4) for x>4','x+2 for x<0; 3 at 0; 4−x/(4−x) for 0<x<4; 3+1/(x−4) for x>4','x+4 for x<0; 3 at 0; 2+x/(4−x) for 0<x<4; 3−1/(x−4) for x>4',label='One possible piecewise model'),limited=True)
add(6,11,*[N(x*x/(2**x),'Table · x='+str(x),tol=1e-9) for x in list(range(11))+[20,50,100]],N(0,'Limit'),limited=True)
add(6,12,N(math.exp(-2),'a · two decimal estimate',tol=.0051),N(math.exp(-2),'b · four decimal estimate',tol=.000051),limited=True)
values={13:.4,14:3,15:1.5,16:0,17:0,18:2,19:-1,20:-.5,21:4,22:1,23:-2,24:2,25:math.sqrt(3)/4,27:1/6,28:-3/4,35:math.pi/2,36:1,37:-.5,38:0,39:0,40:-math.pi/2,42:0,67:5}
for n,v in values.items():add(6,n,N(v))
for n in [26,30,31,34,41]:add(6,n,I())
add(6,29,C('(a−b)/2','a−b','(a+b)/2',label='Limit'))
add(6,32,D());add(6,33,I(-1))
add(6,43,N(0,'a(i)'),I(-1,'a(ii)'),I(1,'a(iii)'),I(1,'b'),C('Domain x>0, x≠1; x-axis approached as x→0+; vertical asymptote x=1; grows without bound as x→∞','Domain all real x and no vertical asymptote','Horizontal asymptote y=1 at positive infinity',label='c · graph'),limited=True)
add(6,44,N(0,'a'),I(1,'b'),I(1,'c'),I(-1,'d'),C('Vertical asymptotes x=0 and x=1; horizontal asymptote y=0','Only vertical asymptote x=2','No asymptotes',label='e · graph'),limited=True)
add(6,45,N(-.5,'a · graph estimate',tol=.02),N(-.5,'b · table estimate',tol=.001),N(-.5,'c · exact limit'),limited=True)
add(6,46,N(5/(2*math.sqrt(3)),'a · one decimal estimate',tol=.051),N(5/(2*math.sqrt(3)),'b · four decimal estimate',tol=.000051),N(5/(2*math.sqrt(3)),'c · exact limit'),limited=True)
for n,correct,w1,w2 in [
(47,'Vertical x=−3; horizontal y=4','Vertical x=3; horizontal y=4','Vertical x=−3; horizontal y=0'),
(48,'Vertical x=−1 and x=1/3; horizontal y=2/3','Vertical x=1 and x=−1/3; horizontal y=2/3','Vertical x=−1; horizontal y=3/2'),
(49,'Vertical x=−2 and x=1; horizontal y=2','Vertical x=2 and x=−1; horizontal y=2','Vertical x=1; horizontal y=1/2'),
(50,'Vertical x=−1, 0, 1; horizontal y=−1','Vertical x=−1, 1; horizontal y=1','Vertical x=0; horizontal y=0'),
(51,'Vertical x=5; no horizontal asymptote (there is a hole at x=1)','Vertical x=1 and x=5; horizontal y=1','Vertical x=1; horizontal y=0'),
(52,'Vertical x=ln 5; horizontal y=0 and y=2','Vertical x=5; horizontal y=2','Vertical x=ln 5; horizontal y=1')]:add(6,n,C(correct,w1,w2,label='Asymptotes'),limited=True)
add(6,53,C('The small window appears near y=1','The small window appears near y=3','The small window appears near y=500',label='Window estimate'),N(3,'Exact horizontal asymptote y'),C('The 500x² terms dominate the small window, but the cubic leading terms determine the true limit','A function cannot approach an asymptote outside the visible window','The limit depends on the graphing window',label='Reason'),limited=True)
add(6,54,N(math.sqrt(2)/3,'a · positive infinity estimate',tol=.03),N(-math.sqrt(2)/3,'a · negative infinity estimate',tol=.03),N(math.sqrt(2)/3,'b · numerical positive limit',tol=.001),N(-math.sqrt(2)/3,'b · numerical negative limit',tol=.001),N(math.sqrt(2)/3,'c · exact positive limit'),N(-math.sqrt(2)/3,'c · exact negative limit'),C('Two horizontal asymptotes y=±√2/3; one vertical asymptote x=5/3','One horizontal asymptote y=√2/3; no vertical asymptote','Two vertical asymptotes x=±5/3',label='Asymptotes'),limited=True)
add(6,55,N(0,'a'),C('Positive or negative infinity according to the ratio of leading coefficients','Always positive infinity','Always zero',label='b'))
fields=[]
for name,vals in [('i · n=0',[1,1,1,1]),('ii · positive odd n',[0,0,'+','-']),('iii · positive even n',[0,0,'+','+']),('iv · negative odd n',['+','-',0,0]),('v · negative even n',['+','+',0,0])]:
 for part,v in zip(['a','b','c','d'],vals):fields.append(I(1 if v=='+' else -1,name+' · '+part) if isinstance(v,str) else N(v,name+' · '+part))
add(6,56,*fields,limited=True)
add(6,57,C('−(x−2)/[x²(x−3)]','(x−2)/[x²(x−3)]','−(x−2)/(x−3)',label='One formula meeting all five conditions'),limited=True)
add(6,58,C('1+1/[(x−1)(x−3)]','1/[(x−1)(x−3)]','1+1/(x−1)',label='One valid formula'),limited=True)
add(6,59,N(5/4,'a'),N(5,'b'))
for n,sign1,sign2,zeros in [(60,-1,-1,'x=0, 2'),(61,-1,-1,'x=−1, 0, 1'),(62,1,1,'x=−2, 0, 1'),(63,-1,1,'x=−1, 1, 3'),(64,1,-1,'x=−2, −1, 0, 1')]:
 add(6,n,I(sign1,'Limit as x→∞'),I(sign2,'Limit as x→−∞'),C(zeros,'No real intercepts','Only x=0',label='x-intercepts'),limited=True)
add(6,65,N(0,'a · limit'),C('Infinitely many crossings, at nonzero integer multiples of π','No crossings','Exactly one crossing',label='b'),limited=True)
add(6,66,C('Both tend to +∞ on the right and −∞ on the left; P/Q→1','P tends to 0 at both ends','P/Q→0',label='a · end behavior'),N(1,'b · ratio limit'),limited=True)
add(6,68,C('C(t)=750t/(5000+25t)=30t/(200+t)','C(t)=30t/200','C(t)=750t/5000',label='a · concentration model'),N(30,'b · limiting concentration','g/L'),limited=True)
add(6,69,C('v* (the terminal velocity)','0','g',label='a'),N(math.log(100)/9.8,'b · time to 99%','s',.0001),limited=True)
add(6,70,N(10*math.log(10),'a · threshold x',tol=.001),C('x>10 ln 10, by taking logarithms','x>ln 10 /10','x<10 ln 10',label='b'),limited=True)
add(6,71,C('N=20 suffices','N=1 suffices','N=2 suffices',label='One valid N'),limited=True)
add(6,72,C('N=20 suffices','N=1 suffices','N=2 suffices',label='ε=0.1'),C('N=40 suffices','N=1 suffices','N=2 suffices',label='ε=0.05'),limited=True)
add(6,73,C('N=−20 suffices for x<N','N=−1 suffices for x<N','N=−2 suffices for x<N',label='ε=0.1'),C('N=−40 suffices for x<N','N=−1 suffices for x<N','N=−2 suffices for x<N',label='ε=0.05'),limited=True)
add(6,74,N(bisect(lambda x:math.sqrt(x)*math.log(x),100,1,10000),'Threshold N',tol=.001),limited=True)
add(6,75,N(100,'a · positive threshold'),C('For ε>0 choose N=1/√ε; x>N implies 1/x²<ε','Choose N=√ε for every ε>0','Choose N=−1/√ε',label='b · proof'),limited=True)
add(6,76,N(1e8,'a · threshold'),C('For ε>0 choose N=1/ε²','For ε>0 choose N=ε²','For ε>0 choose N=−1/ε²',label='b · proof'),limited=True)
add(6,77,C('Given ε>0 take N=−1/ε; x<N implies |1/x|<ε','Take N=−ε for every ε>0','Take N=1/ε and require x>N',label='Proof bound'),limited=True)
add(6,78,C('For M>0 take N=M^(1/3)','For M>0 take N=−M^(1/3)','For M>0 take N=ln M',label='Proof bound'),limited=True)
add(6,79,C('For M>0 take N=ln M (or max(0,ln M))','For M>0 take N=−ln M','For M>0 take N=1/M',label='Proof bound'),limited=True)
add(6,80,C('For every M<0 there is N<0 such that x<N implies f(x)<M','For some M>0, x>N implies f(x)>M','For every ε>0, |f(x)|<ε for large positive x',label='Definition'),C('For 1+x³ choose N=min(−1,(M−1)^(1/3)) for a negative bound M','Choose N=M² for all negative M','1+x³ tends to positive infinity as x→−∞',label='Proof'),limited=True)
add(6,81,C('Substitute t=1/x; x→∞ gives t→0+ and x→−∞ gives t→0−','Substitute t=x²; both sides become t→0','Substitute t=−x without changing the approach',label='a · substitution'),N(0,'b · limit'),limited=True)

# 2.2 The limit of a function. Printed92–94 source diagrams visually inspected.
add(2,1,C('f(x) approaches 5 as x approaches 2 through values other than 2','f(2) must equal 5','f(x)=5 throughout a neighborhood',label='Meaning'),Y(True,'Can f(2)=3?'),limited=True)
add(2,2,C('Values approach 3 from the left and 7 from the right','Values approach 7 from the left and 3 from the right','Both sides approach 5',label='Meaning'),Y(False,'Can the two-sided limit exist?'),limited=True)
add(2,3,C('f(x) increases without bound as x approaches −3 from either side','f(−3)=infinity','f approaches −3 as x increases',label='a'),C('f(x) decreases without bound as x approaches 4 from the right','f approaches infinity from the left','f(4)=0',label='b'),limited=True)
add(2,4,N(3,'a'),N(1,'b'),D('c'),N(3,'d'),N(4,'e'),C('Undefined','4','0',label='f'))
add(2,5,N(2,'a'),N(1,'b'),N(4,'c'),D('d'),N(3,'e'))
add(2,6,N(4,'a'),N(4,'b'),N(4,'c'),C('Undefined','4','0',label='d'),N(1,'e'),N(-1,'f'),D('g'),N(1,'h'),N(2,'i'),C('Undefined','2','0',label='j'),N(3,'k'),D('l'))
add(2,7,N(-1,'a'),N(-2,'b'),D('c'),N(2,'d'),N(0,'e'),D('f'),N(1,'g'),N(3,'h'))
add(2,8,I(1,'a'),I(-1,'b'),I(1,'c'),I(-1,'d'),C('x=−3, −1, 2','x=−3, 2, 5','x=−1, 0, 2',label='e'))
add(2,9,I(-1,'a'),I(1,'b'),I(1,'c'),I(-1,'d'),I(1,'e'),C('x=−7, −3, 0, 6','x=−7, −3, 6 only','x=−3, 0, 3',label='f'))
add(2,10,N(150,'Left limit at 12','mg'),N(300,'Right limit at 12','mg'),C('The amount jumps upward by 150 mg at the injection','The amount jumps downward by 150 mg','The amount is continuous at the injection',label='Significance'),limited=True)
add(2,11,C('All real a except −1','All real a except 1','All real a',label='Limit-existence set'),limited=True)
add(2,12,C('All real a except π','All real a except 0','All real a',label='Limit-existence set'),limited=True)
add(2,13,N(1,'a'),N(0,'b'),D('c'),limited=True)
add(2,14,N(-1,'a'),N(1,'b'),D('c'),limited=True)
add(2,15,C('f=−1 for x<0, f(0)=1, f=2 for x>0','f=2 for x<0, f(0)=1, f=−1 for x>0','f=1 for all x',label='One valid graph'),limited=True)
add(2,16,C('f=1−x for x<3 except f(0)=−1; f(3)=1; f=2 for x>3','f=1−x for x<3 with f(0)=1; f(3)=1; f=2 for x>3','f=1−x for x<3 except f(0)=−1; f(3)=1; f=−2 for x>3',label='One valid graph'),limited=True)
add(2,17,C('f=2 for x<3 except f(−2)=1; f(3)=3; f=4 for x>3','f=2 for x<3; f(3)=4; f=3 for x>3','f=4 for x<3 except f(−2)=1; f(3)=3; f=2 for x>3',label='One valid graph'),limited=True)
add(2,18,C('f=2 for x≤0; f=3x/4 for 0<x<4; f(4)=1; f=0 for x>4','f=0 for x≤0; f=3x/4 for 0<x<4; f(4)=1; f=2 for x>4','f=2 for x≤0; f=3x/4 for 0<x≤4; f=0 for x>4',label='One valid graph'),limited=True)
for n,xs in [(19,[3.1,3.05,3.01,3.001,3.0001,2.9,2.95,2.99,2.999,2.9999]),(20,[-2.5,-2.9,-2.95,-2.99,-2.999,-2.9999,-3.5,-3.1,-3.05,-3.01,-3.001,-3.0001])]:
 add(2,n,*[N(x/(x+3),'x='+str(x),tol=5.1e-7) for x in xs],N(.5,'Limit') if n==19 else D('Two-sided limit'))
for n,fn,L in [(21,lambda t:math.expm1(5*t)/t,5),(22,lambda h:80+80*h+40*h*h+10*h**3+h**4,80)]:
 vals=[v*sign for v in [.5,.1,.01,.001,.0001] for sign in [1,-1]]
 add(2,n,*[N(fn(x),('t=' if n==21 else 'h=')+str(x),tol=5.1e-7) for x in vals],N(L,'Limit'))
for n,v in {23:.25,24:.6,25:1.5,26:math.log(5),27:1,28:0}.items():add(2,n,N(v,'Estimated limit',tol=.0001),limited=True)
add(2,29,N(-1.5,'a · graph limit',tol=.02),N(-1.5,'b · numerical limit',tol=.001),limited=True)
add(2,30,N(1/math.pi,'a · two decimal estimate',tol=.0051),N(1/math.pi,'b · numerical limit',tol=.001),limited=True)
for n,sign in {31:1,32:-1,33:1,34:-1,35:-1,36:-1,37:-1,38:-1,39:-1,40:-1,41:1,42:1,43:-1}.items():add(2,n,I(sign))
add(2,44,C('x=0 and x=3/2','x=0 and x=−3/2','x=3/2 only',label='a · vertical asymptotes'),C('The graph diverges near both 0 and 3/2','The graph is bounded near both values','The graph has horizontal asymptote y=3/2',label='b · graph check'),limited=True)
add(2,45,I(-1,'Left limit'),I(1,'Right limit'),limited=True)
add(2,46,N(4,'a · graph estimate',tol=.02),N(4,'b · numerical limit',tol=.001),limited=True)
add(2,47,N(math.e,'a · five decimal estimate',tol=.0000051),C('e','π','2',label='a · familiar constant'),C('Values approach about 2.71828 from both sides near 0','Values approach 1 from both sides','Values increase without bound near 0',label='b · graph'),limited=True)
add(2,48,C('A coarse plot can hide the vertical asymptote x=4','The function is continuous at x=4','The function has no domain restriction',label='a · plot accuracy'),C('Exclude x=4 and zoom/sample closely on both sides to reveal the plunge to −∞','Join points across x=4 with a straight line','Replace ln|x−4| by ln(x+4)',label='b · improvement'),limited=True)
add(2,49,*[N(x*x-2**x/1000,'a · x='+str(x),tol=.00000051) for x in [1,.8,.6,.4,.2,.1,.05]],*[N(x*x-2**x/1000,'b · x='+str(x),tol=.00000051) for x in [.04,.02,.01,.005,.003,.001]],N(-.001,'Actual limit'),C('Early values may suggest 0, but closer values approach −0.001','The exact limit is zero because x² tends to zero','The exact limit is 1',label='Interpretation'),limited=True)
add(2,50,*[N((math.tan(x)-x)/x**3,'a · x='+str(x),tol=.000001) for x in [1,.5,.1,.05,.01,.005]],N(1/3,'b · limit'),C('Floating-point subtraction loses significant digits; machine zeros do not imply a zero mathematical limit','A calculator zero proves the limit is zero','The limit changes with calculator precision',label='c · cancellation'),N(1/3,'d · graph estimate',tol=.01),limited=True)
add(2,51,C('Oscillations remain between −1 and 1 and become arbitrarily rapid; no limit at 0','The amplitude shrinks to zero','The function approaches 1',label='Graph behavior'),limited=True)
add(2,52,N(0,'a · values at 1/(nπ)'),N(1,'b · values at 4/((4n+1)π)'),D('c · right-hand limit'),limited=True)
a=math.asin(math.pi/4)
add(2,53,C('x=±arcsin(π/4), ±[π−arcsin(π/4)]','x=±π/4 only','x=0 and ±π/2',label='Exact vertical asymptotes'),N(a,'Positive inner asymptote',tol=.001),N(math.pi-a,'Positive outer asymptote',tol=.001),limited=True)
add(2,54,I(1,'Mass as v→c− (m₀>0)'))
f55=lambda x:sum(x**(k/2) for k in range(6))
d55=bisect(f55,6.5,1,2)-1
add(2,55,N(6,'a · limit',tol=.0001),N(d55,'b · largest symmetric distance δ',tol=.00001),limited=True)

# 2.5 Continuity, printed124–126. Source graph3/4 inspected.
add(5,1,C('lim(x→4) f(x)=f(4)','lim(x→4) f(x)=0','f(4) need not be defined',label='Continuity equation'))
add(5,2,C('The graph has no breaks, holes or jumps anywhere on the real line','The graph must be a straight line','The graph must have a derivative at every point',label='Graph meaning'),limited=True)
add(5,3,C('x=−4, −2, 2, 4','x=−4, −2, 0, 2','x=−2, 0, 4',label='a · discontinuities'),C('−4: neither; −2: left only; 2: right only; 4: right only','−4: both; −2: right only; 2: left only; 4: neither','All are continuous from both sides',label='b · one-sided continuity'),limited=True)
add(5,4,C('[−3,−2), (−2,−1), (−1,0], (0,1), (1,3]','[−3,0], [0,3]','(−3,−1), (−1,1), (1,3)',label='Intervals of continuity'))
for n,ans,w1,w2 in [
(5,'f=0 for x<2 and f=1 for x≥2','f=0 for x≤2 and f=1 for x>2','f=0 for x≠2 and f(2)=1'),
(6,'f=0 for x≤−1; f=1 for −1<x<4; f=2 for x≥4','f=0 for x<−1; f=1 for −1≤x≤4; f=2 for x>4','f=0 for x≤−1; f=1 for −1<x≤4; f=2 for x>4'),
(7,'f=x for x<5 except f(3)=0; f=x+1 for x≥5','f=x for all x','f=x for x≠3 and f(3)=3'),
(8,'f=0 for x<−2; f(−2)=2; f=1 for −2<x≤2; f=3 for x>2','f=0 for x≤−2; f=1 for −2<x≤2; f=3 for x>2','f=0 for x<−2; f(−2)=2; f=1 for −2<x<2; f=3 for x≥2')]:add(5,n,C(ans,w1,w2,label='One graph satisfying the conditions'),limited=True)
add(5,9,C('$7 on 7<t<10 and 16<t<19; $5 at other nonboundary times','$7 on 10<t<16 only','$5 throughout the day',label='a · graph levels'),C('Jumps at t=7,10,16,19; entering just across a boundary changes the toll by $2','Discontinuity only at midnight','The toll is continuous at every time',label='b · discontinuities'),limited=True)
add(5,10,*[C(ans,*wrong,label=label) for label,ans,wrong in [
('a','Continuous in the ordinary idealized temperature model',['Discontinuous at every instant','Always constant']),
('b','Continuous in the ordinary idealized spatial temperature model',['Must jump at every city boundary','Must be linear in distance']),
('c','Can be discontinuous at a vertical cliff',['Must be continuous even across an ideal vertical cliff','Always constant']),
('d','Discontinuous when a meter increments the fare in steps',['Continuous for every taxi fare model','Never changes with distance']),
('e','Discontinuous in an ideal switched circuit when the switch changes state',['Must be constant for all time','A switch cannot change current'])]],limited=True)
for n,v in {11:81,12:14/5,13:4,14:40}.items():add(5,n,N(v,'Function value and limit at a'),C('The limit equals the defined function value','The limit is unrelated to the value','The limit fails to exist',label='Continuity conclusion'),limited=True)
add(5,15,C('x+√(x−4) is continuous for x>4, and its right limit at 4 is f(4)=4','The square root is defined only for x<4','The right limit at 4 is 0',label='Continuity on [4,∞)'),limited=True)
add(5,16,C('The rational function has nonzero denominator throughout (−∞,−2)','The denominator is zero throughout this interval','Only polynomials are continuous',label='Continuity reason'),limited=True)
add(5,17,C('f(−2) is undefined and the one-sided limits are infinite with opposite signs','The finite limit is 1','The function is continuous at −2',label='Discontinuity'),limited=True)
add(5,18,C('f(−2)=1 but the nearby values diverge with opposite signs','The nearby limit is 1','Assigning a value removes this infinite discontinuity',label='Discontinuity'),limited=True)
add(5,19,N(2,'Left limit'),N(.5,'Right limit'),C('Jump discontinuity at −1','Removable hole at −1','Continuous at −1',label='Classification'),limited=True)
add(5,20,N(.5,'Limit at 1'),N(1,'Value at 1'),C('Removable discontinuity: redefine f(1)=1/2','Infinite discontinuity','No discontinuity',label='Classification'),limited=True)
add(5,21,N(1,'Limit at 0'),N(0,'Value at 0'),C('Removable discontinuity at 0','Jump discontinuity at 0','Continuous at 0',label='Classification'),limited=True)
add(5,22,N(7,'Limit at 3'),N(6,'Value at 3'),C('Removable discontinuity at 3','Infinite discontinuity at 3','Continuous at 3',label='Classification'),limited=True)
add(5,23,N(3,'Define f(2) as'));add(5,24,N(3,'Define f(2) as'))
for n,ans,w1,w2 in [
(25,'All real x','x≠−1,1','x>0'),
(26,'All real x except −1/2 and 1','All real x except −1 and 1/2','All real x'),
(27,'All real x except ∛2','x≥2','All real x except 2'),
(28,'All real t','t≠nπ for integer n','t>0'),
(29,'−1≤t≤0','0≤t≤1','All real t'),
(30,'−2<x<2, excluding x=±π/2','−2≤x≤2 with no exclusions','All real x except ±2'),
(31,'x≤−1 or x>0','x≥−1','x≠0'),
(32,'All real r','r≥0 only','r≠0')]:add(5,n,C(ans,w1,w2,label='Domain'),C('Continuous throughout its domain by composition and algebra of continuous functions','Discontinuous at every domain point','Only continuous where its derivative is zero',label='Continuity reason'),limited=True)
add(5,33,C('x=0','x=1','No discontinuities',label='Discontinuity'),limited=True)
add(5,34,C('x=nπ/2 for every integer n','x=nπ only','x=π/4+nπ only',label='Excluded/discontinuous points'),limited=True)
for n,v in {35:8,36:0,37:math.log(2),38:9}.items():add(5,n,N(v))
add(5,39,N(0,'Both one-sided limits and value at x=1'),C('The two continuous pieces agree at x=1','The pieces have different limits at x=1','ln x is defined at every real x',label='Continuity proof'),limited=True)
add(5,40,N(math.sqrt(2)/2,'Both one-sided limits and value at π/4'),C('sin(π/4)=cos(π/4), so the pieces meet continuously','The pieces meet only because their derivatives agree','sin and cos have unequal values at π/4',label='Continuity proof'),limited=True)
add(5,41,C('Only x=−1; continuous from the right there','x=−1 and 1; continuous only from the left at each','Only x=1; continuous from the right there',label='Discontinuities and side'),limited=True)
add(5,42,C('Only x=4; continuous from the left there','x=1 and 4; continuous from the right at each','Only x=1; continuous from the left there',label='Discontinuities and side'),limited=True)
add(5,43,C('x=0: right only; x=1: left only','x=0: left only; x=1: right only','Continuous everywhere',label='Discontinuities and side'),limited=True)
add(5,44,Y(True,'Continuous for physical r≥0?'),C('Both formulas give GM/R² at r=R','Both formulas give zero at R','The inner formula diverges at R',label='Boundary value reason'),limited=True)
add(5,45,N(2/3,'c'))
add(5,46,N(.5,'a'),N(.5,'b'))
add(5,47,N(4,'f(2)'))
add(5,48,C('(f∘g)(x)=x² for x≠0','(f∘g)(x)=1/x³','(f∘g)(x)=x² including its original value at 0',label='a'),C('Continuous on its domain x≠0; not defined at 0, but continuously extendable with value 0','Defined and continuous at 0 as originally composed','Discontinuous at every nonzero x',label='b'),limited=True)
add(5,49,C('Removable; g(x)=x³+x²+x+1 with g(1)=4','Not removable','Removable with g(1)=0',label='a'),C('Removable; g(x)=x²+x with g(2)=6','Not removable','Removable with g(2)=2',label='b'),C('Not removable: one-sided limits at π are 0 and −1','Removable with value 0','Removable with value −1',label='c'))
add(5,50,C('A jump from 1 to 3 at 0.25 can skip 2; another graph may cross 2 later despite a jump there','Any discontinuity makes attaining 2 impossible','The endpoint values alone guarantee attaining 2 without continuity',label='Two possible graph behaviors'),limited=True)
add(5,51,C('f is continuous and f(31)<1000<f(32), so IVT gives c in (31,32)','f(0)>1000 so no crossing is needed','Any function must attain every real value',label='IVT argument'),limited=True)
add(5,52,C('If f(3)≤6, IVT between 2 and 3 gives a forbidden solution of f(x)=6','Continuity implies every function increases','f(3)>6 follows without continuity',label='Reason'),limited=True)
for n,fn,a,b in [(53,lambda x:x**4+x-3,1,2),(54,lambda x:math.log(x)-x+math.sqrt(x),2,3),(55,lambda x:math.exp(x)+2*x-3,0,1),(56,lambda x:math.sin(x)-x*x+x,1,2)]:
 add(5,n,N(fn(a),'Continuous residual at left endpoint'),N(fn(b),'Continuous residual at right endpoint'),C('Opposite signs, so the IVT guarantees a root inside the stated interval','Same sign proves no root','The IVT does not require continuity',label='Conclusion'),limited=True)
add(5,57,C('cos x−x³ is positive at 0 and negative at 1, so IVT applies','cos x−x³ has no real zeros','A sign change proves a root even for discontinuous functions',label='a · existence'),C('(0.86,0.87)','(0.80,0.81)','(0.90,0.91)',label='b · interval of length 0.01'),limited=True)
add(5,58,C('ln x+2x−3 changes sign between 1 and 2','ln x is continuous on all real x','There is no root because logarithms are positive',label='a · existence'),C('(1.34,1.35)','(1.25,1.26)','(1.50,1.51)',label='b · interval of length 0.01'),limited=True)
root59=bisect(lambda x:.01*x*x-100*math.exp(-x/100),0,0,200)
add(5,59,C('100e^(−x/100)−0.01x² changes sign from x=0 to x=100','The residual is always positive','A root must equal zero',label='a · existence'),N(root59,'b · root to three decimals',tol=.00051),limited=True)
root60=bisect(lambda x:math.atan(x)+x-1,0,0,1)
add(5,60,C('arctan x+x−1 changes sign between 0 and 1','The residual is always negative','The equation requires x<0',label='a · existence'),N(root60,'b · root to three decimals',tol=.00051),limited=True)
add(5,61,C('x=∛π and x=∛(2π) both lie in (1,2)','Only x=0 is a root','The roots are x=π and x=2π',label='Two roots'),limited=True)
add(5,62,C('The continuous residual is positive at 1/4, negative at 1, and positive at 2','The residual is positive everywhere in (0,2)','The residual has no singularity at 0',label='Two sign changes give two roots'),limited=True)
add(5,63,C('Set h=x−a; then h→0 exactly when x→a, so the two continuity limits are equivalent','Set h=x+a; then h→0 when x→a','Only one implication holds',label='Change of variable'),limited=True)
add(5,64,C('sin(a+h)=sin a cos h+cos a sin h; use cos h→1 and sin h→0','sin(a+h)=sin a+sin h for every a,h','sin h/h is undefined everywhere',label='Continuity proof'),limited=True)
add(5,65,C('cos(a+h)=cos a cos h−sin a sin h; the limit is cos a','cos(a+h)=cos a+cos h','Cosine is continuous only where it is positive',label='Continuity proof'),limited=True)
add(5,66,C('lim(cf)=c lim f=c f(a), proving continuity of cf','The limit of cf equals f(a) regardless of c','Continuity is not preserved by constants',label='a · constant multiple law'),C('For g(a)≠0, lim(f/g)=f(a)/g(a); continuity of g keeps its denominator nonzero nearby','The quotient law requires no restriction on g(a)','Every quotient is continuous on the entire real line',label='b · quotient law'),limited=True)
add(5,67,C('Nowhere','Only at x=0','At every rational x',label='Continuity set'))
add(5,68,C('Only at x=0','Everywhere','At every rational x',label='Continuity set'))
add(5,69,Y(True,'Does such a number exist?'),C('x³−x+1 changes sign between −2 and −1','x³−x+1 is positive for all x','The required equation is x³=x+1',label='Reason'),limited=True)
add(5,70,C('On ((√5−1)/2,1), the residual is continuous and goes from +∞ to −∞','The denominators are nonzero everywhere on (−1,1)','Both terms are positive throughout (−1,1)',label='IVT interval and signs'),limited=True)
add(5,71,C('At 0, |x⁴sin(1/x)|≤x⁴→0=f(0); away from 0 use compositions','sin(1/x) has limit 0','The function is discontinuous at 0',label='Continuity proof'),limited=True)
add(5,72,C('||x|−|a||≤|x−a| proves continuity','|x| is differentiable at 0','|x| has a jump at 0',label='a'),C('Composition with the continuous absolute-value function preserves continuity','Absolute value always makes a function discontinuous','The claim holds only when f is positive',label='b'),C('No: f(x)=1 for x≥0 and −1 for x<0 has |f|=1 continuous','Yes: |f| continuous always forces f continuous','No continuous function can have constant absolute value',label='c'),limited=True)
add(5,73,C('Subtract the two continuous distance-from-monastery functions at the same clock time; the difference changes sign between 7am and 7pm','The monk must walk at constant speed','Both journeys must have identical pauses',label='IVT argument'),limited=True)

# 2.7 Derivatives and rates, printed148–152; all source graphs inspected.
add(7,1,C('[f(x)−f(3)]/(x−3), x≠3','[f(x)+f(3)]/(x−3)','f(x)/(x−3)',label='a · secant slope'),C('lim(x→3)[f(x)−f(3)]/(x−3)','[f(3)−f(3)]/(3−3)','f(3)/3',label='b · tangent slope'))
add(7,2,C('Near (0,1) the curve looks increasingly like its tangent y=1+x','Near (0,1) the curve looks like y=0','The local slope tends to infinity',label='Zoom observation'),limited=True)
add(7,3,N(2,'a(i) · slope'),N(2,'a(ii) · slope'),C('y=2x+1','y=2x−1','y=−2x+5',label='b · tangent'),C('The curve and tangent become indistinguishable on a sufficiently small scale','The line has a different slope at (1,3)','The curve has a corner at (1,3)',label='c · graph'),limited=True)
add(7,4,N(-2,'a(i) · slope'),N(-2,'a(ii) · slope'),C('y=−2x+2','y=2x−2','y=−2x',label='b · tangent'),C('The curve approaches its tangent in a sufficiently small viewing window','The line stays a fixed vertical distance from the curve at the point','The curve is discontinuous at x=1',label='c · graph'),limited=True)
for n,ans,w1,w2 in [(5,'y=−8x+12','y=8x−20','y=−8x−4'),(6,'y=9x−15','y=9x+3','y=−9x+21'),(7,'y=(x+1)/2','y=x+1','y=2x−1'),(8,'y=(x+2)/3','y=(x+1)/2','y=x')]:add(7,n,C(ans,w1,w2,label='Tangent line'))
add(7,9,C('8a−6a²','4a²−2a³','8a+6a²',label='a · tangent slope'),C('y=2x+3','y=2x−3','y=−2x+7',label='b · tangent at (1,5)'),C('y=−8x+19','y=8x−13','y=−8x+3',label='b · tangent at (2,3)'),limited=True)
add(7,10,C('−1/(2a^(3/2)), a>0','1/(2√a)','−1/(2√a)',label='a · slope'),C('y=−x/2+3/2','y=x/2+1/2','y=−x+2',label='b · tangent at (1,1)'),C('y=−x/16+3/4','y=−x/8+1','y=x/16+1/4',label='b · tangent at (4,1/2)'),limited=True)
add(7,11,C('Right: (0,1),(4,6); left: (2,3); still: (1,2),(3,4)','Right: (0,2); left: (2,4); still: (4,6)','The particle always moves right',label='a · directions'),C('v=3 on (0,1), 0 on (1,2), −2 on (2,3), 0 on (3,4), 1 on (4,6); corner times have no derivative','v equals the position graph','v=1 at every noncorner time',label='b · velocity graph'),limited=True)
add(7,12,C('A runs at constant speed; B starts slower and accelerates to finish with A','B runs at constant speed and A slows down','Both run at the same constant speed',label='a'),N(10,'b · greatest separation time','s',1.2),N(10,'c · equal velocity time','s',1.2),limited=True)
add(7,13,N(-24,'Velocity','ft/s'))
add(7,14,N(6.28,'a · velocity','m/s'),C('v(a)=10−3.72a','v(a)=10−1.86a','v(a)=10+3.72a',label='b'),N(10/1.86,'c · return time','s'),N(-10,'d · impact velocity','m/s'))
add(7,15,C('v(a)=−2/a³, a>0','v(a)=2/a³','v(a)=−1/a²',label='At t=a'),N(-2,'At t=1','m/s'),N(-.25,'At t=2','m/s'),N(-2/27,'At t=3','m/s'))
add(7,16,N(0,'a(i)','ft/s'),N(1,'a(ii)','ft/s'),N(3,'a(iii)','ft/s'),N(4,'a(iv)','ft/s'),N(2,'b','ft/s'),C('Upward-opening parabola with tangent y=2t−9 at t=8','Downward-opening parabola with tangent y=2t−9','Upward-opening parabola with tangent y=−2t+9',label='c · graph'),limited=True)
add(7,17,C('g′(0)<0<g′(4)<g′(2)<g′(−2)','g′(−2)<g′(0)<0<g′(2)<g′(4)','0<g′(0)<g′(4)<g′(2)<g′(−2)',label='Increasing order'),limited=True)
add(7,18,N(10,'a · graph average rate',tol=1),C('[10,50] has equal endpoint values and average rate 0','[20,60] has average rate 0','[40,70] has average rate 0',label='b · one valid interval'),C('[40,60] gives the larger average rate','[40,70] gives the larger average rate','Both average rates are zero',label='c'),N(-20/3,'d · secant slope',tol=.7),C('Slope of the secant from (10,f(10)) to (40,f(40))','Tangent slope at x=40','The function value at x=10',label='d · meaning'),limited=True)
add(7,19,N(25,'a · graph estimate f′(50)',tol=7),Y(False,'b · f′(10)>f′(30)?'),Y(True,'c · tangent slope exceeds displayed secant slope?'),limited=True)
add(7,20,C('y=4x−23','y=4x−3','y=−4x+17',label='Tangent line'))
add(7,21,N(3,'f(2)'),N(4,'f′(2)'))
add(7,22,N(3,'f(4)'),N(.25,'f′(4)'))
add(7,23,C('f(x)=x³/3−2x²+3x','f(x)=x³/3−x²+3x','f(x)=x³/3−2x²−3x',label='One valid function'),limited=True)
add(7,24,C('g=x for x<0; g=(2/π)sin(πx/2) for 0≤x≤4; g=x−4 for x>4','g=(2/π)sin(πx/2) on all real x','g=x(x−2)(x−4)/8 on all real x',label='One graph satisfying every condition'),limited=True)
add(7,25,C('On (−5,5): g=3+(x−5)(2−x/5−141x²/620)/(x+5)','On (−5,5): g=3+(x−5)(2+x/5)/(x+5)','On (−5,5): g=x+1',label='One formula meeting all conditions'),limited=True)
add(7,26,C('On (−2,2): f=x/(4−x²)−9x/4 except f(±1)=0','On (−2,2): f=x/(4−x²)+9x/4 except f(±1)=0','On (−2,2): f=x/(4−x²)−9x/4 with its usual values everywhere',label='One formula meeting all conditions'),limited=True)
add(7,27,N(3,'f′(1)'),C('y=3x−1','y=3x+1','y=−3x+5',label='Tangent line'))
add(7,28,N(4,'g′(1)'),C('y=4x−5','y=4x−1','y=−4x+3',label='Tangent line'))
add(7,29,N(-.6,'a · F′(2)'),C('y=−3x/5+16/5','y=3x/5+4/5','y=−3x/5+2',label='a · tangent'),limited=True)
add(7,30,C('G′(a)=8a−3a²','G′(a)=8a+3a²','G′(a)=4a²−a³',label='a · derivative'),C('y=4x','y=4x+8','y=−4x+16',label='a · tangent at (2,8)'),C('y=−3x+18','y=3x','y=−3x+9',label='a · tangent at (3,9)'),limited=True)
for n,ans,w1,w2 in [(31,'6a−4','3a²−4a','6a+4'),(32,'6a²+1','6a+1','2a³+a'),(33,'5/(a+3)², a≠−3','−5/(a+3)²','2/(a+3)'),(34,'−2/a³, a≠0','2/a³','−1/a²'),(35,'−1/√(1−2a), a<1/2','1/√(1−2a)','−2/√(1−2a)'),(36,'2/(1−a)^(3/2), a<1','−2/(1−a)^(3/2)','4/√(1−a)')]:add(7,n,C(ans,w1,w2,label='f′(a)'))
for n,ans,w1,w2 in [(37,'f(x)=√x, a=9','f(x)=x², a=3','f(x)=√x, a=3'),(38,'f(x)=e^x, a=−2','f(x)=e^x, a=2','f(x)=e^(−x), a=−2'),(39,'f(x)=x⁶, a=2','f(x)=x², a=6','f(x)=x⁶, a=64'),(40,'f(x)=1/x, a=1/4','f(x)=1/x, a=4','f(x)=x, a=1/4'),(41,'f(x)=cos x, a=π','f(x)=sin x, a=π','f(x)=cos x, a=0'),(42,'f(x)=sin x, a=π/6','f(x)=sin x, a=1/2','f(x)=cos x, a=π/6')]:add(7,n,C(ans,w1,w2,label='Function and evaluation point'))
add(7,43,N(32,'Velocity','m/s'),N(32,'Speed','m/s'))
add(7,44,N(-1.8,'Velocity','m/s'),N(1.8,'Speed','m/s'))
add(7,45,C('Temperature decreases toward refrigerator temperature with a negative slope approaching 0; the initial derivative is more negative (smaller)','Temperature increases at a constant positive rate','The initial derivative is positive and increases',label='Cooling graph and rate comparison'),limited=True)
add(7,46,N(-.8,'Graph-estimated cooling rate at 60 min','°F/min',.15),limited=True)
add(7,47,*nums([-.15,-.12,-.12,-.11],['a(i)','a(ii)','a(iii)','a(iv)'],'(mg/mL)/h'),N(-.12,'b · centered derivative estimate','(mg/mL)/h',.015),C('At t=2 the concentration decreases about 0.12 mg/mL each hour','At t=2 the concentration increases 0.12 mg/mL each hour','At t=2 the concentration itself is −0.12 mg/mL',label='b · interpretation'),limited=True)
add(7,48,N(2120,'a(i)','locations/year'),N(89,'a(ii)','locations/year'),C('Growth slowed sharply in 2008–2010 relative to 2006–2008','Growth was unchanged','The number of locations decreased in 2008–2010',label='a · conclusion'),N(346.5,'b · average of adjacent secant slopes','locations/year'),N(346.5,'c · centered graph estimate','locations/year',160),limited=True)
add(7,49,N((84077-66533)/15,'a · average growth','thousand barrels/day/year'),N((84077-70099)/10,'b · centered derivative estimate','thousand barrels/day/year'),limited=True)
vs=[(9.4-53)/7,(9.4-18)/3,(5.2-9.4)/4,(3.6-9.4)/11]
add(7,50,*nums(vs,['a(i)','a(ii)','a(iii)','a(iv)'],'RNA copies/(mL·day)'),N((vs[1]+vs[2])/2,'b · derivative estimate','RNA copies/(mL·day)',.25),C('Viral load is decreasing by roughly 2 RNA copies/mL each day near day11','The viral load is approximately −2 copies/mL','Viral load increases by about 2 copies/mL each day',label='b · interpretation'),limited=True)
add(7,51,N(20.25,'a(i)','dollars/unit'),N(20.05,'a(ii)','dollars/unit'),N(20,'b · marginal cost','dollars/unit'))
fields=[C('dV/dt=−(10000/3)(1−t/60) gal/min; outflow magnitude is its negative','dV/dt=(10000/3)(1−t/60) gal/min','dV/dt=100000(1−t/60)² gal/min',label='Rate formula and sign')]
for t in range(0,61,10):fields += [N(-(10000/3)*(1-t/60),'Signed dV/dt at t='+str(t),'gal/min',.0001),N(100000*(1-t/60)**2,'Water remaining at t='+str(t),'gal',.001)]
fields += [N(0,'Time of greatest outflow magnitude','min'),N(60,'Time of least outflow magnitude','min'),C('Outflow magnitude decreases to 0 while the tank empties','Outflow increases as the tank empties','Signed dV/dt is positive throughout',label='Summary')]
add(7,52,*fields,limited=True)
add(7,53,C('Marginal production cost, measured in dollars per ounce','Total ounces per dollar','Total cost in ounces',label='a'),C('Near 800 ounces, one extra ounce costs approximately $17','The total cost for 800 ounces is $17','Producing one ounce takes 17 hours',label='b'),C('May decrease initially as production becomes efficient, then increase as easy ore is depleted; the model alone gives no universal trend','Must decrease forever','Must be exactly constant at 17 everywhere',label='c'),limited=True)
add(7,54,C('Population growth rate at 5 hours, in bacteria/hour','Population after 5 hours, in bacteria','Average population from hour0 to5',label='a'),C('With unlimited resources, later growth is typically larger; limited resources can slow or reverse that comparison','f′(10) must always exceed f′(5) under any resource conditions','Derivatives do not describe bacterial growth',label='b'),limited=True)
add(7,55,C('Change in daily heating cost per 1°F rise near 58°F, in dollars/day per °F','The heating cost at 58°F','The outside temperature change per dollar',label='a'),C('Negative: warmer outside air usually reduces heating cost','Positive: warmer outside air always increases heating cost','Zero by definition',label='b'),limited=True)
add(7,56,C('Change in pounds sold per $1/lb increase near p=$8/lb; units lb/(dollars/lb)','Total pounds sold at $8/lb','The price itself',label='a'),C('Typically negative: quantity demanded falls as price rises','Always positive by definition','Exactly zero',label='b'),limited=True)
add(7,57,C('Rate of change of oxygen solubility with temperature; units (mg/L)/°F as labeled on the source graph','Oxygen concentration itself in mg/L','Temperature change in °F per minute',label='a'),N(-.23,'b · graph slope at T=16','(mg/L)/°F',.07),C('Solubility decreases by about 0.23 mg/L for a one-degree increase near T=16 on the displayed scale','Solubility increases with temperature','The solubility at T=16 is negative',label='b · interpretation'),limited=True)
add(7,58,C('Rate of change of maximum swimming speed per degree Celsius; units (cm/s)/°C','The swimming speed itself','The water acceleration in m/s²',label='a'),N(.6,'b · graph slope S′(15)','(cm/s)/°C',.45),N(-2,'b · graph slope S′(25)','(cm/s)/°C',.6),C('Near 15°C warming increases speed; near25°C warming decreases speed','Warming increases speed at both temperatures','Both derivatives must be zero',label='b · signs'),limited=True)
add(7,59,Y(False,'Does f′(0) exist?'),C('Difference quotient sin(1/h) oscillates without a limit','Difference quotient h sin(1/h) tends to zero','Continuity forces differentiability',label='Reason'),limited=True)
add(7,60,Y(True,'Does f′(0) exist?'),N(0,'f′(0)'),C('|h sin(1/h)|≤|h|→0','sin(1/h) itself tends to zero','The function is constant near zero',label='Reason'),limited=True)
add(7,61,N(1,'a · apparent coarse-window slope',tol=.15),N(1,'b · apparent intermediate-window slope',tol=.2),C('Fine oscillations become visible; coarse estimates can conceal the true tangent','The derivative is exactly1 because every window proves it','The function is not differentiable at zero',label='c · refined interpretation'),N(0,'Actual derivative at zero'),limited=True)
# Four source records share one writing-project task and differ only in suggested
# bibliography. Each checks the explicit common tangent calculation; the requested
# historical report is not assessed by recognition controls.
for q in QS.values():
 if q['sourceSet']=='section-2-7' and 'project-' in q['id']:
  put(q,[N(5,'Modern tangent slope at (1,3)'),C('y=5x−2','y=3x','y=5x+3',label='Modern tangent line'),C('Compare vanishing-increment/secant reasoning with Fermat or Barrow; the historical report still requires written work','A multiple-choice selection fully replaces the requested historical report','No comparison with historical methods is requested',label='Scope of the writing project')],True)

# 2.8 Derivative as a function, printed160–165. Numeric graph estimates1–2
# cross-checked against tangents to the printed PDF's Bezier artwork; no claim
# that artistic vector coordinates define an exact analytic underlying function.
add(8,1,*nums([-.25,0,1,1.75,1,0,-.25],['a','b','c','d','e','f','g'],tol=.3),C('f′ is negative before the left minimum, positive between the two stationary points, and negative after the right maximum','f′ is positive everywhere','f′ is negative everywhere',label='Derivative graph'),limited=True)
add(8,2,*nums([5.15,0,-1.5,-1.33,-.8,-.35,0,.17],['a','b','c','d','e','f','g','h'],tol=.25),C('f′ changes + to − near x=1 and − to + near x=6','f′ is zero everywhere','f′ changes − to + near x=1 and + to − near x=6',label='Derivative graph'),limited=True)
add(8,3,*[C(ans,*[o for o in ['I','II','III','IV'] if o!=ans],label=part) for part,ans in [('a','II'),('b','IV'),('c','I'),('d','III')]],limited=True)
graphs={
4:('Cubic-like derivative with three zeros at the two minima and central maximum; signs −,+,−,+','Positive derivative everywhere','Derivative has a jump at each smooth extremum'),
5:('Positive to the left of the maximum, zero at the maximum near0, negative on the right and tending toward0','Negative everywhere','A positive constant slope'),
6:('Positive left of0, zero at0, negative right of0; slopes flatten toward the far ends','Negative left of0 and positive right of0','Zero derivative except at0'),
7:('Positive on the left, zero at the top, negative on the right; unbounded slope magnitudes near the semicircle endpoints','Positive constant everywhere','Derivative equals the upper semicircle'),
8:('Negative left of0, positive right of0, with unbounded magnitudes near0 and no finite derivative at0','Derivative is0 at0 and continuous there','Positive on both sides with no singularity'),
9:('Piecewise constant slopes with signs −,+,−,+; undefined at all three corners','A continuous derivative through the corners','The derivative is positive everywhere'),
10:('Negative on the descending portion except a zero at the stationary inflection; zero at the right minimum, then positive','The stationary inflection forces a sign change in f′','There is no zero of f′ at the smooth minimum'),
11:('Positive on both sides of0, very large near the vertical tangent; no finite f′(0), flattening at the far ends','Negative on the left and positive on the right','f′(0)=0')}
for n,options in graphs.items():add(8,n,C(*options,label='Derivative graph description'),limited=True)
add(8,12,C('Positive, hump-shaped P′ with its maximum around6hours, then tending toward0 as population levels off','P′ stays negative','P′ increases without bound as the population levels off',label='Derivative and growth meaning'),limited=True)
add(8,13,C('Charging rate in percentage points of full capacity per hour','The battery percentage itself','The amount of electrical charge in watts',label='a'),C('C′ is positive and decreases toward0; charging slows as full capacity is approached','C′ is negative and decreases forever','C′ is a positive constant',label='b'),limited=True)
add(8,14,C('Change in miles/gal per unit increase in mi/h; units (mi/gal)/(mi/h)','The gasoline consumption in gallons/hour','The speed itself',label='a'),C('F′ positive below about50mph, zero near50mph, negative above50mph','F′ positive at every speed','F′ zero at every speed',label='b'),N(50,'c · fuel-economy maximizing speed','mi/h',4),limited=True)
add(8,15,C('Negative roughly1963–1972, while the average marriage age falls','Negative roughly1980–2000','Negative throughout1950–2000',label='Years with negative derivative'),C('M′ is positive before the early1960s peak, negative to the early1970s minimum, then positive and flattening','M′ always equals M','M′ is a constant negative number',label='Derivative graph'),limited=True)
for n,ans,w1,w2 in [(16,'f′(x)=cos x','f′(x)=sin x','f′(x)=−cos x'),(17,'f′(x)=e^x','f′(x)=xe^x','f′(x)=1/x'),(18,'f′(x)=1/x for x>0','f′(x)=x for all x','f′(x)=−1/x for x>0')]:add(8,n,C(ans,w1,w2,label='Derivative formula/graph'),limited=True)
add(8,19,*[N(2*x,'a · x='+str(x),tol=.05) for x in [0,.5,1,2]],*[N(2*x,'b · x='+str(x),tol=.05) for x in [-.5,-1,-2]],C('f′(x)=2x','f′(x)=x','f′(x)=2x²',label='c · formula'),C('[(x+h)²−x²]/h=2x+h→2x','[(x+h)²−x²]/h=x+h','The quotient is undefined for every nonzero h',label='d · definition proof'),limited=True)
add(8,20,*[N(3*x*x,'a · x='+str(x),tol=.05) for x in [0,.5,1,2,3]],*[N(3*x*x,'b · x='+str(x),tol=.05) for x in [-.5,-1,-2,-3]],C('An upward-opening parabola with vertex(0,0)','A straight line through the origin','A downward-opening parabola',label='c · derivative graph'),C('f′(x)=3x²','f′(x)=3x','f′(x)=x³',label='d · formula'),C('[(x+h)³−x³]/h=3x²+3xh+h²→3x²','The difference quotient equals3x+h','The derivative is3x³',label='e · proof'),limited=True)
for n,ans,w1,w2 in [(21,'3','3x','−8'),(22,'m','b','mx'),(23,'5t+6','2.5t+6','5t−6'),(24,'8−10x','8+10x','4+8x−5x²'),(25,'2x−6x²','2x−2x²','2−6x'),(31,'4x³','4x','x⁴')]:
 add(8,n,C(ans,w1,w2,label='Derivative'),C('Function domain: all real numbers; derivative domain: all real numbers','Function domain: x>0; derivative domain: x>0','Function domain: all real numbers; derivative undefined at0',label='Domains'),limited=True)
add(8,26,C('g′(t)=−1/(2t^(3/2))','g′(t)=1/(2√t)','g′(t)=−1/(2√t)',label='Derivative'),C('Both domains: t>0','Both domains: t≥0','Both domains: all real t',label='Domains'),limited=True)
add(8,27,C('g′(x)=−1/[2√(9−x)]','g′(x)=1/[2√(9−x)]','g′(x)=−√(9−x)',label='Derivative'),C('g domain x≤9; g′ domain x<9','Both domains x≤9','Both domains x>9',label='Domains'),limited=True)
add(8,28,C('f′(x)=(2x²−6x+2)/(2x−3)²','f′(x)=2x/(2x−3)','f′(x)=(2x²+6x−2)/(2x−3)²',label='Derivative'),C('Both domains: x≠3/2','Both domains: all real x','Both domains: x>3/2',label='Domains'),limited=True)
add(8,29,C('G′(t)=−7/(t+3)²','G′(t)=7/(t+3)²','G′(t)=−2/(t+3)',label='Derivative'),C('Both domains: t≠−3','Both domains: all real t','Both domains: t≠3',label='Domains'),limited=True)
add(8,30,C('f′(x)=(3/2)√x for x>0; right derivative at0 is0','f′(x)=3/(2√x)','f′(x)=√x/2',label='Derivative'),C('Function domain x≥0; ordinary two-sided derivative domain x>0','Function domain all real x; derivative domain all real x','Function domain x>0 only',label='Domains and endpoint convention'),limited=True)
add(8,32,C('Reflect √x horizontally and shift right6: endpoint(6,0), extending to the left','Shift √x left6 without reflecting','Reflect √x vertically with endpoint(0,6)',label='a · graph'),C('Derivative is negative for x<6 and diverges downward near6','Derivative is positive for x<6','Derivative is a constant',label='b · derivative graph'),C('f′(x)=−1/[2√(6−x)]','f′(x)=1/[2√(6−x)]','f′(x)=−√(6−x)',label='c · derivative'),C('f domain x≤6; f′ domain x<6','Both domains x≤6','Both domains all real x',label='c · domains'),limited=True)
add(8,33,C('f′(x)=4x³+2','f′(x)=4x+2','f′(x)=x⁴+2',label='a · derivative'),C('Derivative is an increasing cubic; its zero is the minimum of f','Derivative is a parabola','Derivative is always positive',label='b · graph check'),limited=True)
add(8,34,C('f′(x)=1−1/x², x≠0','f′(x)=1+1/x²','f′(x)=−1/x²',label='a · derivative'),C('f′ vanishes at ±1, is negative for0<|x|<1, positive for|x|>1','f′ positive everywhere','f′ is defined at0 and equals1',label='b · graph check'),limited=True)
def centered(xs,ys):
 return [(ys[min(i+1,len(xs)-1)]-ys[max(i-1,0)])/(xs[min(i+1,len(xs)-1)]-xs[max(i-1,0)]) for i in range(len(xs))]
years=list(range(2003,2013));us=[6,5.5,5.1,4.6,4.6,5.8,9.3,9.6,8.9,8.1]
add(8,35,C('Change in unemployment rate per year, in percentage points/year','Number of unemployed people','The unemployment percentage itself',label='a'),*[N(v,'b · U′('+str(y)+')','percentage points/year',.0001) for y,v in zip(years,centered(years,us))],reason='Use centered differences between adjacent years at interior points, and one-sided differences at endpoints; these are estimates, not exact derivatives.',limited=True)
years=list(range(2000,2013,2));counts=[5500,4897,7470,9138,10897,11561,13035]
add(8,36,C('Annual change in number of procedures, measured in thousands/year','Total procedures per patient','The procedure count itself',label='a'),*[N(v,'b · N′('+str(y)+')','thousands/year',.0001) for y,v in zip(years,centered(years,counts))],C('N falls initially then rises; N′ initially negative, later positive with varying growth','N′ is always negative','N is constant',label='c · graphs'),C('Collect data at more closely spaced times','Round every count to the nearest million','Use only the first and last observations',label='d · improve accuracy'),reason='Centered differences between nearest tabulated neighbors; one-sided differences at endpoints.',limited=True)
ages=[14,21,28,35,42,49];heights=[41,54,64,72,78,83]
add(8,37,*[N(v,'H′('+str(y)+')','ft/year',.0001) for y,v in zip(ages,centered(ages,heights))],C('Positive derivative estimates decrease as the tree ages','Derivative estimates are all negative','The derivative increases at every age',label='Graph of growth rate'),reason='Use adjacent centered differences, one-sided at endpoints.',limited=True)
ts=[15.5,17.7,20,22.4,24.4];weights=[37.2,31,19.8,9.7,-9.8]
add(8,38,*[N(v,'W′('+str(t)+')','g/°C',.0001) for t,v in zip(ts,centered(ts,weights))],C('All estimates are negative; higher temperature reduces weight gain over the measured range','All estimates are positive','Units are grams per day',label='Graph and units'),reason='Use secants spanning the nearest neighboring temperatures; endpoint estimates use one-sided adjacent data.',limited=True)
add(8,39,C('Rate of change of the solar share in percentage points/year','Total solar electricity in watts','Percentage divided by total city population',label='a'),C('At January1,2002 the solar share increases about3.5 percentage points per year','At January1,2002 exactly3.5% of power is solar','Solar share decreases3.5points/year',label='b'),limited=True)
add(8,40,C('Negative: higher gasoline prices typically reduce the number taking car vacations','Positive by the definition of a derivative','Exactly zero regardless of prices',label='Expected sign'),limited=True)
for n,ans,w1,w2 in [(41,'x=−4, 0, 5/2','x=−2, 0, 2','Only x=0'),(42,'x=−1 and 2','x=0 and 2','Only x=2'),(43,'x=1 and 5','x=0, 2, 4','Only x=1'),(44,'x=−2, 1, 3','x=−2 and 3 only','Only x=1')]:add(8,n,C(ans,w1,w2,label='Points without finite derivative'),limited=True)
add(8,45,C('Differentiable at−1 with slope1/2; not differentiable at0, which has opposite unbounded one-sided slopes','Not differentiable at−1 but differentiable at0','Differentiable everywhere',label='Local behavior'),limited=True)
add(8,46,C('Cusps and no finite derivative at±1; smooth horizontal tangent at0','Smooth at±1 and a cusp at0','Not differentiable anywhere',label='Zoom and differentiability'),limited=True)
add(8,47,C('f″(1) is bigger','f′(−1) is bigger','They are equal',label='Comparison'),limited=True)
add(8,48,C('f′(−1) is bigger','f″(1) is bigger','They are equal',label='Comparison'),limited=True)
add(8,49,C('f=a, f′=b, f″=c','f=c, f′=b, f″=a','f=b, f′=a, f″=c',label='Curve identities'),limited=True)
add(8,50,C('f=d, f′=c, f″=b, f‴=a','f=a, f′=b, f″=c, f‴=d','f=d, f′=b, f″=c, f‴=a',label='Curve identities'),limited=True)
add(8,51,C('Position=c, velocity=b, acceleration=a','Position=a, velocity=b, acceleration=c','Position=b, velocity=c, acceleration=a',label='Curve identities'),limited=True)
add(8,52,C('Position=d, velocity=c, acceleration=b, jerk=a','Position=a, velocity=b, acceleration=c, jerk=d','Position=d, velocity=b, acceleration=c, jerk=a',label='Curve identities'),limited=True)
add(8,53,C('f′=6x+2','f′=3x²+2','f′=6x',label='First derivative'),N(6,'Second derivative'),limited=True)
add(8,54,C('f′=3x²−3','f′=3x−3','f′=x²−3',label='First derivative'),C('f″=6x','f″=6','f″=3x²',label='Second derivative'),limited=True)
add(8,55,C('f′=4x−3x²','f′=4x+3x²','f′=2x−3x²',label='First derivative'),C('f″=4−6x','f″=4+6x','f″=−6x',label='Second derivative'),N(-6,'Third derivative'),N(0,'Fourth derivative'),C('Yes: zeros/signs of successive derivatives match stationary points and concavity of preceding graphs','No: a cubic must have a nonzero fourth derivative','No: derivatives have unrelated graphs',label='Graph consistency'),limited=True)
# The position illustration is deliberately qualitative; selected conclusions
# check signs and units rather than pretending a unique precise jerk is encoded.
add(8,56,C('Velocity is positive, grows while the position graph steepens, then approaches a positive constant','Velocity is negative throughout','Velocity equals the position function',label='a · velocity graph'),C('Acceleration is positive during the speeding-up transition near10seconds, then falls toward0 as the graph becomes straight','Acceleration is negative throughout','Acceleration must be constant because position increases',label='a · acceleration near10s'),C('Jerk is the slope of the acceleration graph, in ft/s³; it is negative where that acceleration declines','Jerk is the velocity, in ft/s','Jerk has units ft/s² and equals position',label='b · jerk interpretation and units'),limited=True,reason='The printed sketch supports qualitative graph checks. A unique accurate numerical acceleration/jerk at10seconds is not determined by this coarse position illustration; constructing and estimating from the student’s derivative sketches still requires review.')
add(8,57,C('f′(a)=1/(3a^(2/3)), a≠0','f′(a)=3a²','f′(a)=1/(3a^(1/3))',label='a'),C('At0 the difference quotient h^(−2/3)→+∞, so no finite derivative','At0 the difference quotient tends to0','f is discontinuous at0',label='b'),C('Vertical tangent x=0','Horizontal tangent y=0','No tangent direction can be described',label='c'),limited=True)
add(8,58,C('At0 the quotient h^(−1/3) diverges with opposite signs, so no finite derivative','At0 the derivative is0','The function is discontinuous at0',label='a'),C('g′(a)=2/(3∛a), a≠0','g′(a)=2a/3','g′(a)=2/(3a²)',label='b'),C('Vertical tangent x=0; the curve has a cusp at0','Horizontal tangent y=0','The tangent is y=x',label='c/d'),limited=True)
add(8,59,C('f′=−1 for x<6; f′=1 for x>6; undefined at6','f′=1 for every x','f′=0 except at6',label='Derivative and corner'),limited=True)
add(8,60,C('Not differentiable at any integer; f′=0 at every noninteger','Differentiable at every integer with f′=1','Not differentiable at any real number',label='Derivative and failure set'),limited=True)
add(8,61,C('f=−x² for x<0 and f=x² for x≥0','f=x² for every x','f=−x² for every x',label='a · graph'),C('Differentiable at every real x, including0','Differentiable only for x≠0','Differentiable nowhere',label='b'),C('f′(x)=2|x|','f′(x)=2x','f′(x)=−2|x|',label='c'),limited=True)
add(8,62,C('g=0 for x<0 and g=2x for x≥0','g=x² for every x','g=−2x for x<0 and0 for x≥0',label='a · graph'),C('Differentiable for x≠0 only','Differentiable everywhere','Differentiable nowhere',label='b'),C('g′=0 for x<0; g′=2 for x>0; undefined at0','g′=2 for every x','g′=0 for every x',label='c'),limited=True)
add(8,63,C('For differentiable even f, f′(−x)=−f′(x)','For even f, f′(−x)=f′(x)','Every even f is differentiable',label='a'),C('For differentiable odd f, f′(−x)=f′(x)','For odd f, f′(−x)=−f′(x)','Every odd f is differentiable',label='b'),limited=True)
add(8,64,N(-1,'a · left derivative at4'),N(1,'a · right derivative at4'),C('f=0 on x≤0, f=5−x on0<x<4, f=1/(5−x) on x≥4 except5','f=0 on x≤0 and f=5−2x on0<x<4','f is a single straight line everywhere',label='b · graph'),C('Discontinuous at0 and undefined at5; continuous at4','Discontinuous at4 only','Continuous on the whole real line',label='c'),C('No derivative at0,4,5; differentiable at other points of its domain','Only at0','Only at4',label='d'),limited=True)
add(8,65,C('s increases with increasing slope on0–3min; slower line3–8; flat8–10; steeper line10–15; slower line15–19','s decreases while he walks','s is flat during all jogging',label='a · distance graph'),C('Positive increasing velocity0–3, slower positive constant3–8, zero8–10, larger positive constant10–15, smaller positive constant15–19','Velocity is negative during walking','Velocity is zero whenever s is increasing',label='b · derivative'),limited=True)
add(8,66,C('Initially cool and nearly constant, then rises, then levels at the hot-water temperature','Temperature falls forever','Temperature increases linearly forever',label='a'),C('Rate is initially near0, positive during warming, then returns toward0','Rate is always negative','Rate must be a positive constant',label='b'),C('Derivative is a nonnegative hump during the warming transition','Derivative equals T','Derivative is a horizontal negative line',label='c'),limited=True)
add(8,67,N(63,'Inclination to nearest degree','degrees',.51))

def build():
 for name in ['problems-plus.json','review-concepts.json','review-exercises.json']:
  path=Path(__file__).parent/name
  if path.exists():
   extra=json.loads(path.read_text())['questions']
   assert not set(extra)&set(ROWS),(name,'duplicate ownership')
   ROWS.update(extra)
 out=ROOT/'scripts/calculus-answer-checks/chapter-02.json';out.write_text(json.dumps(dict(questions=ROWS),ensure_ascii=False,indent=2)+'\n')
 missing=[q['id'] for q in QS.values() if q['id'] not in ROWS]
 print('Authored',len(ROWS),'of',len(QS),'questions;',sum(r['objectiveFieldCount'] for r in ROWS.values()),'fields. Missing',len(missing))
 (Path(__file__).parent/'coverage.json').write_text(json.dumps(dict(total=len(QS),authored=len(ROWS),missing=missing),indent=2)+'\n')
if __name__=='__main__':build()
