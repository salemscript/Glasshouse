# Printed725–727.
def cv(sec,i,yes,why,limited=False,extra=()):put(sec,i,C('Converges' if yes else 'Diverges','Diverges' if yes else 'Converges',label='Series convergence'),*extra,why=why,limited=limited)
cv(3,1,True,'Right-endpoint rectangles fit below x^(−1.3); the bounding integral equals10/3.',True,extra=(N(S.Rational(10,3),'Integral bound'),))
put(3,2,C('Σ_(i=2)^6 a_i < ∫₁⁶f(x)dx < Σ_(i=1)^5 a_i','Integral is smaller than both sums','Integral is larger than both sums'),limited=True)
for i,yes,why in [(3,1,'p=3>1.'),(4,0,'p=.3≤1.'),(5,0,'Integral grows logarithmically.'),(6,1,'Integral of(3x−1)^−4 is finite.'),(7,0,'Primitive ln(x²+1)/2 grows without bound.'),(8,1,'Substitution u=x³ gives finite exponential integral.'),(9,1,'p=√2>1.'),(10,0,'p=.9999<1.'),(11,1,'p=3.'),(12,0,'Reciprocals of an arithmetic progression have harmonic decay.'),(13,0,'Terms behave like1/(4n).'),(14,1,'p=3/2.'),(15,1,'Sum of p-series n^(−3/2)+4n^(−2).'),(16,0,'Integral substitutes u=1+x^(3/2), giving a divergent logarithm.'),(17,1,'Integral is an arctangent with finite limit.'),(18,1,'Complete square(x+1)²+1.'),(19,0,'Primitive ln(x⁴+4)/4 diverges.'),(20,0,'Terms asymptotic to3/n.'),(21,0,'Primitive ln ln x diverges.'),(22,1,'Integration by parts gives finite integral of ln x/x².'),(23,1,'Exponential decay yields finite integral.'),(24,1,'u=x² gives finite exponential integral.'),(25,1,'Terms below1/n³.'),(26,1,'Terms below1/n³.')]:cv(3,i,bool(yes),why)
put(3,27,C('The terms alternate signs, violating positivity','All positive functions fail the test','The denominator is zero'),why='cosπn=(−1)^n.',limited=True)
put(3,28,C('cos²x/(1+x²) is not eventually decreasing','The terms are negative','Every term is zero'),limited=True)
for i,ans in [(29,'p>1'),(30,'p>1'),(31,'p<−1'),(32,'p>1')]:put(3,i,C(ans,'Every real p','No real p',label='Convergence values'),why='Use an integral substitution for logarithmic factors or the dominant power n^(1+2p); test the equality endpoint separately.')
put(3,33,C('x>1','x≥1','All real x',label='Domain of the defining real series'))
put(3,34,N(pi*pi/6-1,'(a) Sum'),N(pi*pi/6-S.Rational(49,36),'(b) Sum'),N(pi*pi/24,'(c) Sum'))
put(3,35,N(9*pi**4/10,'(a) Sum'),N(pi**4/90-S.Rational(17,16),'(b) Sum'))
for i,p,epsilon in [(36,4,mp.mpf('.00001')),(37,2,mp.mpf('.001'))]:
 ss=sum(S.Rational(1,k**p) for k in range(1,11));low=ss+S.Rational(1,(p-1)*11**(p-1));high=ss+S.Rational(1,(p-1)*10**(p-1));mid=(low+high)/2;exact=pi**4/90 if p==4 else pi*pi/6
 nn=int(mp.floor((1/((p-1)*epsilon))**(mp.mpf(1)/(p-1))))+1
 put(3,i,N(ss,'(a) s₁₀',tol=1e-7),N(S.Rational(1,(p-1)*10**(p-1)),'(a) Integral upper error bound'),N(low,'(b) Improved lower bound'),N(high,'(b) Improved upper bound'),N(mid,'(b) Midpoint estimate'),N(exact,'(c) Exact value'),N(exact-mid,'(c) Exact minus midpoint estimate'),N(nn,'(d) Sufficient n from strict integral bound',tol=0),why='For decreasing positive f, ∫_(n+1)^∞ f<R_n<∫_n^∞ f; the midpoint of the resulting sum interval is one explicit improved estimate.')
put(3,38,N(S.exp(-2)/(1-S.exp(-2))**2,'Sum',tol=.000051),why='The exact geometric derivative sum provides an independent check of the requested four-decimal approximation.')
put(3,39,N((1-S.Rational(1,64))*pi**6/945-1,'Sum',tol=.0000051),why='Sum over all odd positive integers and remove1; independent high-precision finite sums and an integral tail bound verify the approximation.')
put(3,40,C('Choose final index N>exp(100); summing n=2,…,N takes N−1 terms','100 terms','exp(10) terms',label='Integral-bound guarantee'),why='Tail≤∫_N∞dx/[x(ln x)²]=1/ln N, which must be<.01.')
put(3,41,C('n>(2×10^11)^1000, which exceeds10^11301','n>10^11','n>11301'),why='Integral tail bound is1000/n^.001; require it below5×10^−9.',limited=True)
B=lambda k:(mp.log(k)**2+2*mp.log(k)+2)/k
nn=8
while B(nn)>=mp.mpf('.05'):nn+=1
ss=mp.fsum(mp.log(k)**2/k**2 for k in range(1,nn+1))
put(3,42,C('Converges; integral tail is finite','Diverges by harmonic comparison','Terms fail to approach0',label='(a)'),C('[(ln n)²+2ln n+2]/n, for n≥8','(ln n)²/n²','1/ln n',label='(b) Upper error bound'),N(nn,'(c) Smallest n for this bound<.05',tol=0),N(ss,'(d) Partial sum at that n',tol=.000001),why='The function decreases for x>e². Integrate by parts twice to obtain the explicit tail; search the strict bound without rounding.',limited=True)
put(3,43,C('s_n≤1+ln n','s_n≤ln n','s_n≥n',label='(a)'),N(1+mp.log(10**6),'(b) Million-term bound'),N(1+mp.log(10**9),'(b) Billion-term bound'),limited=True)
put(3,44,C('t_n>0','t_n<0','t_n=0',label='(a)'),C('t_n−t_(n+1)>0 because ∫_n^(n+1)dx/x>1/(n+1)','The difference is negative','The difference is zero',label='(b)'),C('Decreasing and bounded below, so converges','Increasing without bound','Alternates signs',label='(c)'),limited=True)
put(3,45,C('0<b<e^(−1)','0<b<1','b>e',label='Convergence values'),why='b^(ln n)=n^(ln b); a p-series converges only when ln b<−1.')
put(3,46,N(1,'Only c permitting convergence'),N(1,'Sum when c=1'),why='Partial sums=(c−1)H_n+1−1/(n+1); harmonic divergence disappears only for c=1.')
