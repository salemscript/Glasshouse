"""Independent derivative, recurrence, quadrature and contract audits; no author import."""
import json,gzip,math
from pathlib import Path
import sympy as s
import mpmath as m
m.mp.dps=50
H=Path(__file__).resolve().parent;R=H.parents[2]
x=s.Symbol('x',real=True);n=s.Symbol('n',integer=True,positive=True);h=s.Symbol('h',real=True)
E={'x':x,'n':n,'h':h,'ln':s.log,'pi':s.pi,'E':s.E}
def P(v):return s.sympify(v,locals=E)
checks=0
def check(v,msg):
 global checks
 assert v,msg
 checks+=1
def near(a,b,t=1e-30):check(abs(m.mpf(str(a))-m.mpf(str(b)))<t,(a,b))
bank=json.load(open(H.parent/'chapter-11.json'));cases=json.load(open(H/'math-cases.json'))
qs={q['id']:q for q in json.load(gzip.open(R/'site/questions/calculus.json.gz','rt')) if q['chapter']==11}
corr=json.load(open(H/'source-correction.json'))
for q in corr['removeQuestionIds']:qs.pop(q,None)
for q in corr['addQuestions']:qs[q['id']]=q
check(set(bank)==set(qs),'Question coverage mismatch')
for qid,row in bank.items():
 g=row['grader'];fs=g.get('parts',[g]);check(len(fs)==row['objectiveFieldCount'],qid)
 for f in fs:
  if f['type']=='numeric':check(math.isfinite(f['answer']) and math.isfinite(f['tolerance']) and f['tolerance']>=0,qid)
  else:check(f['answer'] in f['options'] and len(set(f['options']))==len(f['options']),qid)
for c in cases:
 kind=c['kind'];qid=c['id'];g=bank[qid]['grader'];fs=g.get('parts',[g])
 if kind=='sequence':
  e=P(c['expr'])
  for j in range(1,c['count']+1):check(abs(float(e.subs(n,j))-fs[j-1]['answer'])<=fs[j-1]['tolerance']+1e-12,qid)
 elif kind=='partial-sums':
  # Independently evaluate each term then accumulate, without symbolic summation.
  fun=s.lambdify(n,P(c['expr']),'mpmath');total=m.mpf(0)
  for j in range(c['count']):
   total+=fun(c['lo']+j)
   if len(fs)>=c['count']:check(abs(total-fs[j]['answer'])<=fs[j]['tolerance']+1e-12,qid)
  if len(fs)<c['count']:check(abs(total-fs[0]['answer'])<=fs[0]['tolerance']+1e-12,qid)
 elif kind=='alternating-remainder':
  f=P(c['magnitude']);N=c['N'];ep=P(c['epsilon'])
  check(f.subs(n,N+1)<ep,qid)
  if N>1:check(f.subs(n,N)>=ep,qid+' minimality')
 elif kind in ['taylor-polynomial','taylor-bound']:
  f=P(c['f']);a=P(c['a']);poly=P(c['poly']);d=s.degree(poly,h)
  for j in range(int(d)+1):
   derivative=s.diff(f,x,j);value=derivative.subs(x,a)
   if value.has(s.nan,s.zoo):value=s.limit(derivative,x,a)
   check(s.simplify(poly.coeff(h,j)-value/s.factorial(j))==0,qid+' coefficient'+str(j))
  if kind=='taylor-bound':
   degree=c['degree'];lo=P(c['lo']);hi=P(c['hi']);M=P(c['M']);bound=P(c['bound'])
   derivative=s.lambdify(x,s.diff(f,x,degree+1),'mpmath');ff=s.lambdify(x,f,'mpmath');pp=s.lambdify(h,poly,'mpmath')
   aa=m.mpf(str(s.N(a,45)));ll=m.mpf(str(s.N(lo,45)));hh=m.mpf(str(s.N(hi,45)));mm=m.mpf(str(s.N(M,45)));bb=m.mpf(str(s.N(bound,45)))
   for j in range(201):
    z=ll+(hh-ll)*j/200
    check(abs(derivative(z))<=mm*(1+m.mpf('1e-35')),qid+' derivative maximum')
    check(abs(ff(z)-pp(z-aa))<=bb*(1+m.mpf('1e-35')),qid+' remainder')
# Exact limits where SymPy can use a direct asymptotic expression. Oscillation
# cases use the source squeeze/subsequence arguments recorded in source-audit.
for c in cases:
 if c['kind']!='sequence' or c['limit']=='None' or 'oscillat' in c['limit']:continue
 f=P(c['expr'])
 if f.has((-1)**n,(-1)**(n+1)) or c['id'] in ['calculus-section-11-1-21','calculus-section-11-1-56']:continue
 v=s.limit(f,n,s.oo);want=s.oo if c['limit']=='+∞' else P(c['limit'])
 check(v==want or s.simplify(v-want)==0,c['id']+' exact limit')
# Strict tail threshold source semantics are n>N, not n≥N.
for eps,N in [(s.Rational(1,10),9),(s.Rational(1,1000),11)]:
 check(N**5/s.factorial(N)>=eps and (N+1)**5/s.factorial(N+1)<eps,'11.1#85 threshold')
check(12**4*s.exp(-12)>s.Rational(1,10)>13**4*s.exp(-13),'review10 threshold')
# Source-transcribed coefficients; compute radius via a ratio limit independently.
coef={3:(-1)**n*n,4:(-1)**n/n**s.Rational(1,3),5:1/(2*n-1),6:(-1)**n/n**2,7:1/s.factorial(n),8:n**n,9:1/(n**4*4**n),10:2**n*n**2,11:(-4)**n/s.sqrt(n),12:(-1)**(n-1)/(n*5**n),13:n/(2**n*(n*n+1)),15:1/(n*n+1),16:(-1)**n/((2*n-1)*2**n),17:1/(2**n*s.log(n)),18:s.sqrt(n)/8**n,19:1/n**n,20:(s.Rational(2,5))**n/s.sqrt(n),23:2**n*s.factorial(n),24:n*n/(2**n*s.factorial(n)),25:5**n/n**3,27:2**n*s.factorial(n)/s.factorial(2*n),28:2**n*s.factorial(n)**2/s.factorial(2*n)}
for i,c in coef.items():
 ratio=s.limit(s.Abs(c/c.subs(n,n+1)),n,s.oo)
 expected=P(next(q['radius'] for q in cases if q['kind']=='power-interval' and q['id']==f'calculus-section-11-8-{i}'))
 check(ratio==expected or s.simplify(ratio-expected)==0,f'11.8#{i} radius')
# Even-power series14 has factorial coefficients and entire radius;26 root coefficient tends1.
check(s.limit((1/(n*s.log(n)**2))**(1/(2*n)),n,s.oo)==1,'11.8#26 root radius')
# Independent source-specific mathematics, using quadrature/recurrences instead of answer formulas.
near(m.quad(lambda z:m.exp(-z/5)*m.sin(z)**2,[0,m.pi]),250/m.mpf(101)*(1-m.exp(-m.pi/5)))
near(m.nsum(lambda k:(-1)**k/((2*k+1)*3**k),[1,m.inf]),m.pi/(2*m.sqrt(3))-1)
a=[m.mpf(1),m.mpf(1)]
for k in range(2,30):
 a.append(((k-1)*(k-2)*a[-1]-(k-3)*a[-2])/(k*(k-1)))
 near(a[-1],1/m.factorial(k))
pts=[(m.mpf(0),m.mpf(1)),(m.mpf(1),m.mpf(1)),(m.mpf(1),m.mpf(0)),(m.mpf(0),m.mpf(0))]
for k in range(600):pts.append(tuple((pts[k][j]+pts[k+1][j])/2 for j in [0,1]))
near(pts[-1][0],m.mpf(4)/7,1e-25);near(pts[-1][1],m.mpf(3)/7,1e-25)
# Termwise-integral values checked against quadrature (different numerical algorithms).
quad_cases=[(9,29,lambda z:z/(1+z**3),'.3',lambda k,b:(-1)**k*b**(3*k+2)/(3*k+2)),(9,30,lambda z:m.atan(z/2),'.5',lambda k,b:(-1)**k*b**(2*k+2)/(2**(2*k+1)*(2*k+1)*(2*k+2))),(9,31,lambda z:z*m.log(1+z*z),'.2',lambda k,b:(-1)**k*b**(2*k+4)/((k+1)*(2*k+4))),(9,32,lambda z:z*z/(1+z**4),'.3',lambda k,b:(-1)**k*b**(4*k+3)/(4*k+3))]
for sec,num,fun,end,term in quad_cases:
 b=m.mpf(end);q=m.quad(fun,[0,b]);v=sum(term(k,b) for k in range(100));near(q,v)
 g=bank[f'calculus-section-11-{sec}-{num}']['grader'];check(abs(q-g['answer'])<=g['tolerance'],'quadrature')
# Three derivatives of the geometric sum independently establish PP11.
f=1/(1-x)
for _ in range(3):f=x*s.diff(f,x)
check(s.simplify(f-x*(1+4*x+x*x)/(1-x)**4)==0,'PP11')
# Rational telescoping identities (exact).
check(s.simplify((1-1/n**2)-((n-1)*(n+1)/n**2))==0,'PP13')
check(s.simplify((n-1)*(n-2)/s.factorial(n-1)-(n-3)/s.factorial(n-2)-n*(n-1)/s.factorial(n))==0,'PP16')
for z in [m.mpf('.1'),m.mpf('1'),m.mpf('3')]:
 u=sum(z**(3*k)/m.factorial(3*k) for k in range(60));v=sum(z**(3*k+1)/m.factorial(3*k+1) for k in range(60));w=sum(z**(3*k+2)/m.factorial(3*k+2) for k in range(60));near(u**3+v**3+w**3-3*u*v*w,1)
# Harmonic parity proof and smallest book count.
for k in range(2,100):check(s.denom(s.harmonic(k))!=1,'harmonic not integer')
check(s.harmonic(3)/2<1<s.harmonic(4)/2,'book count')
print(f'PASS: {checks} independent structural, derivative, numerical, recurrence and identity assertions; {len(bank)} source tasks.')
