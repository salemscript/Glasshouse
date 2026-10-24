# Printed736–737.
put(5,1,C('Successive terms alternate sign','Every term is positive','Terms only need to be bounded',label='(a)'),C('Eventually nonincreasing magnitudes tending to0 guarantee convergence','Alternation alone suffices','Magnitudes may tend to1',label='(b)'),C('|R_n|≤b_(n+1); sign of R_n matches the next term','|R_n|≤b_n for every series','R_n=0',label='(c)'),limited=True)
reasons={2:(1,'Magnitudes2/(2n+1) decrease to0.'),3:(0,'Magnitudes2n/(n+4) tend to2.'),4:(1,'1/ln(n+2) decreases to0.'),5:(1,'1/(3+5n) decreases to0.'),6:(1,'1/√(n+1) decreases to0.'),7:(0,'Magnitude tends to3/2.'),8:(0,'Magnitude tends to1.'),9:(1,'Geometric ratio−e^−1.'),10:(1,'√n/(2n+3) eventually decreases to0 (after n>3/2).'),11:(1,'n²/(n³+4) decreases for n>2 and tends to0.'),12:(1,'ne^−n decreases to0.'),13:(0,'Magnitude tends to1.'),14:(0,'Magnitude tends toπ/2.'),15:(1,'sin((n+1/2)π)=(−1)^n; denominator grows.'),16:(1,'Absolute convergence of n/2^n.'),17:(1,'sin(π/n) decreases to0 after n≥2; ignore initial term.'),18:(0,'cos(π/n)→1, so terms do not tend to0.'),19:(0,'Magnitudes n^n/n! grow.'),20:(1,'Rationalize the difference to1/(√(n+1)+√n), decreasing to0.')}
for i,(yes,why) in reasons.items():cv(5,i,bool(yes),why)
for i,e,value in [(21,'(-4/5)**n/factorial(n)',S.exp(-S.Rational(4,5))-1),(22,'(-1)**(n-1)*n/8**n',S.Rational(8,81))]:
 f=P(e);fs=[];ss=S.Integer(0)
 for k in range(1,11):
  term=f.subs(n,k);ss+=term;fs.extend([N(term,f'a_{k}',tol=.000051),N(ss,f's_{k}',tol=.000051)])
 fs.append(N(value,'Sum to four decimal places',tol=.000051));put(5,i,*fs,limited=True,why='Alternating magnitudes decrease to0; the first omitted magnitude bounds the error. Graphs require separate review.')
for i,b,eps in [(23,'1/n**6','.00005'),(24,'1/(3**n*n)','.0005'),(25,'1/(n*n*2**n)','.0005'),(26,'n**(-n)','.00005')]:
 f=P(b);nn=1
 while mp.mpf(str(S.N(f.subs(n,nn+1),40)))>=mp.mpf(eps):nn+=1
 put(5,i,C('Converges by the Alternating Series Test','Diverges','Term limit is nonzero',label='Convergence'),N(nn,'Smallest N with next-term bound strictly below requested error',tol=0),N(f.subs(n,nn+1),'Next-term error bound',tol=1e-12),why='Check decreasing positive magnitudes and solve b_(N+1)<ε; this is a guaranteed bound, not the unknown exact remainder.')
 CASES.append(dict(kind='alternating-remainder',id=f'calculus-section-11-5-{i}',magnitude=str(f),epsilon=eps,N=nn))
for i,v in [(27,S.cos(1)-1),(28,S.Rational(31,32)*pi**6/945),(29,-S.exp(-2)/(1+S.exp(-2))**2),(30,S.log(S.Rational(5,4)))]:put(5,i,N(v,'Sum to four decimal places',tol=.000051),why='Sum until the first omitted magnitude is below0.00005; the exact closed expression independently verifies the approximation.')
put(5,31,C('Underestimate','Overestimate','Exactly equal'),why='Term51 is positive, so the remainder after50terms is positive.',limited=True)
put(5,32,C('p>0','p≥0','Every real p',label='Convergence values'))
put(5,33,C('Every real p except−1,−2,−3,…','Only p>0','Every real p with no exceptions',label='Convergence values'),why='Negative integerp creates a zero denominator at an actual term. Otherwise discard finitely many terms and apply the alternating test to the positive decreasing tail.')
put(5,34,C('Every real p','Only p>0','Only p<−1',label='Convergence values'),why='(ln n)^p/n→0 for each fixed realp and its derivative is eventually negative.')
put(5,35,C('Diverges to+∞','Converges conditionally','Converges absolutely',label='Conclusion'),C('Magnitudes are not eventually nonincreasing: each odd reciprocal exceeds the preceding even reciprocal square','The terms fail to tend to0','Signs do not alternate',label='Why the test fails'),why='Odd-index harmonic terms diverge while the sum of even reciprocal squares is finite.',limited=True)
put(5,36,C('s_(2n)=h_(2n)−h_n','s_(2n)=h_(2n)+h_n','s_(2n)=h_n/2',label='(a)'),N(S.log(2),'(b) Limit'),why='Subtract the even terms twice from H_(2n); then H_(2n)−ln(2n) and H_n−ln n tend to the same Euler constant.',limited=True)
