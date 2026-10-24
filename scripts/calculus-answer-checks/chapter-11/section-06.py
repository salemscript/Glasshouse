# Printed742–744.
def cls(i,kind,why,extra=()):put(6,i,C(kind,*[z for z in ['Absolutely convergent','Conditionally convergent','Divergent'] if z!=kind],label='Classification'),*extra,why=why)
put(6,1,C('Diverges','Converges absolutely','Inconclusive',label='(a) Ratio limit8'),C('Converges absolutely','Diverges','Inconclusive',label='(b) Ratio limit.8'),C('Inconclusive','Converges absolutely','Diverges',label='(c) Ratio limit1'),limited=True)
for i,kind,why in [(2,'Conditionally convergent','Alternating1/√n converges; its positive p-series diverges.'),(3,'Conditionally convergent','Alternating reciprocal linear terms; absolute series harmonic.'),(4,'Absolutely convergent','Compare magnitudes with1/n³.'),(5,'Absolutely convergent','|sin n|/2^n≤1/2^n.'),(6,'Conditionally convergent','Eventually decreasing magnitude tends to0, but n/(n²+4)~1/n.')]:cls(i,kind,why)
ratios={7:S.Rational(1,5),8:2,9:S.Rational(3,2),10:0,11:0,12:1/S.E,13:S.Rational(5,8),14:S.oo,15:pi/3,16:S.Rational(1,10),17:0,18:1/S.E,19:0,20:4,21:S.Rational(1,2),22:S.Rational(3,2),23:2,24:S.Rational(2,3)}
for i,L in ratios.items():
 yes=L!=S.oo and float(L)<1;cv(6,i,yes,'Compute |a_(n+1)/a_n| and its limit; a limit below1 gives absolute convergence, above1 gives divergence.',extra=(C('+∞','0','1',label='Ratio limit') if L==S.oo else N(L,'Ratio limit'),))
roots={25:S.Rational(1,2),26:0,27:0,28:32,29:S.E,30:pi/2}
for i,L in roots.items():cv(6,i,float(L)<1,'Compute lim |a_n|^(1/n); compare it with1.',extra=(N(L,'Root-test limit'),))
for i,kind,why in [(31,'Conditionally convergent','Alternating1/ln n decreases to0; absolute terms eventually exceed1/n.'),(32,'Absolutely convergent','Root limit1/3.'),(33,'Absolutely convergent','Absolute ratio tends to.9.'),(34,'Divergent','Ratio limit25/10=2.5.'),(35,'Divergent','Root n/ln n tends to∞.'),(36,'Absolutely convergent','Bound the sine by1 and compare with1/n^(3/2).'),(37,'Absolutely convergent','Bound arctan n byπ/2 and compare with1/n².'),(38,'Conditionally convergent','Alternating test succeeds, while ∫dx/(x ln x) diverges.')]:cls(i,kind,why)
cv(6,39,False,'The recurrence gives ratio(5n+1)/(4n+3)→5/4.',extra=(N(S.Rational(5,4),'Ratio limit'),))
cv(6,40,True,'0<(2+cos n)/√n≤3/√n→0.',extra=(N(0,'Ratio limit'),))
cls(41,'Absolutely convergent','The root limit is lim b_n/n^(1/n)=1/2.',extra=(N(S.Rational(1,2),'Root limit'),))
cls(42,'Absolutely convergent','The magnitude ratio is[n/(n+1)]^n/b_(n+1)→2/e<1.',extra=(N(2/S.E,'Ratio limit'),))
put(6,43,C('(a) and(d) only','(b) and(c) only','All four',label='Ratio test inconclusive'),why='Limits are1,1/2,3,1 respectively.')
put(6,44,C('Every positive integer k≥2','Every k≥1','Only k≥3',label='Convergent values'),why='k=1 gives terms n!, k=2 ratio1/4, k>2 ratio0.')
put(6,45,C('Absolute ratio |x|/(n+1)→0 for every real x','Only |x|<1 converges','The ratio is |x|',label='(a)'),N(0,'(b) Limit x^n/n! for fixed real x'),limited=True)
put(6,46,C('R_n≤a_(n+1)/(1−r_(n+1))','R_n≤a_n/(1+r_n)','R_n=0',label='(a) Decreasing ratios'),C('R_n≤a_(n+1)/(1−L)','R_n≤a_(n+1)/(1+L)','R_n=L',label='(b) Increasing ratios'),limited=True)
ss5=sum(S.Rational(1,k*2**k) for k in range(1,6));nn=1
while S.Rational(1,(nn+1)*2**nn)>=S.Rational(1,20000):nn+=1
put(6,47,N(ss5,'(a) s₅'),N(S.Rational(1,192),'(a) Ratio-tail upper bound'),N(nn,'(b) Smallest n from this bound<.00005',tol=0),N(sum(S.Rational(1,k*2**k) for k in range(1,nn+1)),'(b) Approximation'),why='Ratios n/[2(n+1)] increase to1/2, so R_n≤2a_(n+1)=1/[(n+1)2^n].')
put(6,48,N(sum(S.Rational(k,2**k) for k in range(1,11)),'s₁₀'),N(S.Rational(121,10240),'Ratio-tail upper bound'),why='Ratios decrease; r₁₁=12/22=6/11, a₁₁=11/2048, so a₁₁/(1−r₁₁)=121/10240.')
put(6,49,C('If L<r<1 then eventually |a_n|<r^n; if L>1 terms fail to tend to0; L=1 is inconclusive','Root limit1 always implies convergence','A root limit>1 gives convergence'),limited=True)
approx=[]
for count in [1,2]:
 val=mp.fsum(mp.factorial(4*k)*(1103+26390*k)/(mp.factorial(k)**4*mp.mpf(396)**(4*k)) for k in range(count));approx.append(9801/(2*mp.sqrt(2)*val))
put(6,50,C('Absolutely convergent: ratio limit1/99^4','Diverges','Ratio limit1',label='(a)'),N(approx[0],'(b) One-term π approximation',tol=1e-14),N(approx[1],'(b) Two-term π approximation',tol=1e-14),N(7,'(b) Matching rounded decimal places, one term',tol=0),N(14,'(b) Matching rounded decimal places, two terms',tol=0),why='Rounded-decimal convention: one-term error≈7.64×10^−8; two-term error≈6.40×10^−16. Matching initial unrounded digits and guaranteed half-unit accuracy are distinct conventions.',limited=True)
put(6,51,C('Both positive and negative subseries converge by comparison withΣ|a_n|','Both diverge','Only the positive subseries converges',label='(a)'),C('Positive subseries→+∞ and negative subseries→−∞','Both have finite limits','Only one diverges',label='(b)'),limited=True)
put(6,52,C('Alternate finite blocks of positives and negatives crossing r; overshoots shrink because a_n→0','Keep positives only','Every rearrangement has the original sum'),limited=True)
put(6,53,C('If Σn²a_n converged its terms would be bounded, giving |a_n|≤M/n² and contradicting conditional convergence','n²a_n always tends to0','Conditional implies absolute',label='(a)'),C('For n≥2, a_n=(−1)^n/[n ln n] makes Σna_n converge; a_n=(−1)^n/n makes it diverge','Both examples a_n=1/n²','Every conditional series gives the same answer',label='(b)'),limited=True)
