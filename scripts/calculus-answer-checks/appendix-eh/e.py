from common import *
# Original expansions, with every endpoint explicitly represented.
expansions={
1:('1 + √2 + √3 + 2 + √5','√1 + √2 + √3 + √4','1 + 2 + 3 + 4 + 5'),
2:('1/2 + 1/3 + 1/4 + 1/5 + 1/6 + 1/7','1 + 1/2 + 1/3 + 1/4 + 1/5 + 1/6','1/2 + 1/3 + 1/4 + 1/5 + 1/6'),
3:('3⁴ + 3⁵ + 3⁶','3⁴ + 3⁵','12 + 15 + 18'),
4:('4³ + 5³ + 6³','3⁴ + 3⁵ + 3⁶','4³ + 5³'),
5:('−1 + 1/3 + 3/5 + 5/7 + 7/9','1/3 + 3/5 + 5/7 + 7/9','−1 + 1/3 + 3/5 + 5/7'),
6:('x⁵ + x⁶ + x⁷ + x⁸','x⁵ + x⁶ + x⁷','5x + 6x + 7x + 8x'),
7:('1¹⁰ + 2¹⁰ + ⋯ + n¹⁰','1¹⁰ + 2¹⁰ + ⋯ + (n−1)¹⁰','10 + 20 + ⋯ + 10n'),
8:('n² + (n+1)² + (n+2)² + (n+3)²','n² + (n+1)² + (n+2)²','1² + 2² + ⋯ + (n+3)²'),
9:('1 − 1 + 1 − ⋯ + (−1)^(n−1), n terms','−1 + 1 − 1 + ⋯ + (−1)^n, n terms','1 − 1 + 1 − ⋯ + (−1)^n, n+1 terms'),
10:('f(x₁)Δx₁ + f(x₂)Δx₂ + ⋯ + f(xₙ)Δxₙ','f(x₁)+Δx₁ + f(x₂)+Δx₂ + ⋯ + f(xₙ)+Δxₙ','f(x₀)Δx₀ + ⋯ + f(xₙ)Δxₙ')}
for k,(ans,b1,b2) in expansions.items():row('E',k,choice('Expanded sum',ans,b1,b2),why='Substitute each consecutive integer index from the inclusive lower bound through the inclusive upper bound; retain the summand operation and all endpoint terms.')
# Require one explicitly prescribed indexing convention while recognizing the entire sum.
sigma={11:(1,10,'i'),12:(3,7,'√i'),13:(1,19,'i/(i+1)'),14:(3,23,'i/(i+4)'),15:(1,'n','2i'),16:(1,'n','2i−1'),17:(0,5,'2^i'),18:(1,6,'1/i²'),19:(1,'n','x^i'),20:(0,'n','(−1)^i x^i')}
for k,(lo,hi,summand) in sigma.items():
 label='Sigma notation using index i'
 ans=f'Lower bound {lo}; upper bound {hi}; summand {summand}'
 b1=f'Lower bound {lo+1}; upper bound {hi}; summand {summand}'
 b2=f'Lower bound {lo}; upper bound {hi}; summand 2({summand})'
 row('E',k,choice(label,ans,b1,b2),why='Match the first and last displayed terms and the step between consecutive terms. These bounds include exactly the displayed terms, once each; other equivalent reindexings are mathematically valid.')
finite={21:(3*i-2,4,8),22:(i*(i+2),3,6),23:(3**(i+1),1,6),24:(s.cos(i*s.pi),0,8),25:((-1)**i,1,20),26:(s.Integer(4),1,100),27:(2**i+i**2,0,4),28:(2**(3-i),-2,4)}
for k,(fun,lo,hi) in finite.items():
 ans=s.summation(fun,(i,lo,hi));direct=sum(fun.subs(i,z) for z in range(lo,hi+1));verify(f'E{k}: direct exact term addition',s.simplify(ans-direct)==0)
 row('E',k,num('Sum',ans),why=f'Add the summand at every integer index {lo} through {hi}, inclusive. Exact addition gives {fmt(ans)}.')
polys={29:2*i,30:2-5*i,31:i**2+3*i+4,32:(3+2*i)**2,33:(i+1)*(i+2),34:i*(i+1)*(i+2),35:i**3-i-2}
for k,fun in polys.items():
 ans=s.factor(s.summation(fun,(i,1,n)))
 row('E',k,expr('Sum as a function of n',ans),why=f'Expand the summand and apply the sums of 1, i, i² and i³. Simplifying gives {fmt(ans)} for positive integer n.')
 for N in [1,2,3,7,12]:verify(f'E{k}: direct sum n={N}',s.simplify(ans.subs(n,N)-sum(fun.subs(i,z) for z in range(1,N+1)))==0)
row('E',36,num('Positive integer n',12),why='n(n+1)/2=78 gives (n−12)(n+13)=0. The positive integer solution is 12.')
verify('E36 integer sum',sum(range(1,13))==78)
row('E',37,choice('Induction step for constant summand c','kc+c=(k+1)c','kc+c=k²c','kc+c=(k+1)c²'),expr('Sum of n copies of c',n*s.Symbol('c')),why='There are n identical terms. For induction, the case n=1 is c=c; adding c to kc gives (k+1)c.',limited=True)
row('E',38,expr('Induction step after adding (k+1)³',(s.Symbol('k')+1)**2*(s.Symbol('k')+2)**2/4),expr('Sum of cubes',n**2*(n+1)**2/4),why='The n=1 base case is 1. Assuming [k(k+1)/2]², add (k+1)³ and factor (k+1)²(k+2)²/4, the claimed formula at k+1.',limited=True)
row('E',39,choice('Telescoping identity','(n+1)⁴−1 = 4Σi³ + 6Σi² + 4Σi + n, all sums i=1,…,n','(n+1)⁴−1 = 4Σi³ + 6Σi² + 4Σi','n⁴ = 4Σi³, sum i=1,…,n'),expr('Sum of cubes',n**2*(n+1)**2/4),why='Expand (i+1)⁴−i⁴=4i³+6i²+4i+1, sum and cancel interior fourth powers, then substitute the known linear and square sums.',limited=True)
row('E',40,expr('Area of gnomon Gᵢ',i**3),expr('Total square area',n**2*(n+1)**2/4),why='The ith gnomon is the difference of squares with sides i(i+1)/2 and i(i−1)/2. Their squared difference is i³. The disjoint gnomons fill the square of side n(n+1)/2.',limited=True)
row('E',41,expr('a · Telescoping sum',n**4),choice('b · Exact sum','5^100−1','5^100','5^101−1'),num('c · Telescoping sum',s.Rational(97,300)),choice('d · Telescoping sum','aₙ−a₀','aₙ−a₁','aₙ+a₀'),why='All interior terms cancel pairwise. The surviving terms are n⁴−0⁴, 5¹⁰⁰−5⁰, 1/3−1/100, and aₙ−a₀, respectively.')
row('E',42,choice('Induction step','|Sₖ+aₖ₊₁| ≤ |Sₖ|+|aₖ₊₁| ≤ Σ(i=1…k+1)|aᵢ|','|Sₖ+aₖ₊₁| = |Sₖ|−|aₖ₊₁|','|Sₖ+aₖ₊₁| ≥ Σ(i=1…k+1)|aᵢ|'),why='Let Sₖ be the sum of the first k terms. Use the two-term triangle inequality, then the induction hypothesis; the one-term case is equality.',limited=True)
limits={43:((i/n)**2/n,s.Rational(1,3)),44:(((i/n)**3+1)/n,s.Rational(5,4)),45:(2*((2*i/n)**3+5*(2*i/n))/n,s.Integer(14)),46:(3*((1+3*i/n)**3-2*(1+3*i/n))/n,s.Rational(195,4))}
for k,(fun,target) in limits.items():
 exact=s.summation(fun,(i,1,n));verify(f'E{k}: symbolic sum limit',s.limit(exact,n,s.oo)==target)
 row('E',k,num('Limit',target),why=f'Evaluate the finite polynomial sum using the power-sum formulas and take n→∞; terms containing 1/n vanish, leaving {fmt(target)}.')
row('E',47,choice('Subtraction identity','(r−1)Sₙ=a(rⁿ−1)','(r−1)Sₙ=a(rⁿ+1)','(r+1)Sₙ=a(rⁿ−1)'),expr('Finite geometric sum (r≠1)',a*(r**n-1)/(r-1)),why='Multiply Sₙ=a+ar+⋯+arⁿ⁻¹ by r and subtract Sₙ. Interior powers cancel; divide by r−1, which is nonzero by hypothesis.',limited=True)
for k,fun in {48:3/2**(i-1),49:2*i+2**i}.items():
 ans=s.simplify(s.summation(fun,(i,1,n)));row('E',k,expr('Sum',ans),why='Apply the finite geometric sum; for #49 also add the arithmetic sum 2Σi=n(n+1).')
 for N in [1,2,5,10]:verify(f'E{k}: direct sum n={N}',s.simplify(ans.subs(n,N)-sum(fun.subs(i,z) for z in range(1,N+1)))==0)
ans=m*n*(m+n+2)/2
row('E',50,expr('Double sum',ans),why='For fixed i the inner sum is ni+n(n+1)/2. Summing i=1,…,m gives nm(m+1)/2+mn(n+1)/2=mn(m+n+2)/2.')
for M,N in [(1,1),(2,3),(5,7)]:verify(f'E50 direct rectangle {M}x{N}',ans.subs({m:M,n:N})==sum(I+J for I in range(1,M+1) for J in range(1,N+1)))
k=s.symbols('k',positive=True,integer=True)
verify('E38 induction algebra',s.expand((k*(k+1)/2)**2+(k+1)**3-((k+1)*(k+2)/2)**2)==0)
verify('E39 fourth-power expansion',s.expand((i+1)**4-i**4-(4*i**3+6*i**2+4*i+1))==0)
verify('E40 gnomon area',s.expand((i*(i+1)/2)**2-(i*(i-1)/2)**2-i**3)==0)
OUT['calculus-section-e-37']['reviewNotice']='Referenced Theorem 3(b): for constant c and positive integer n, the sum of c from i=1 through n is nc. Prove this identity.'
for k in [38,39,40]:
 OUT[f'calculus-section-e-{k}']['reviewNotice']='Referenced Theorem 3(e): for positive integer n, 1³+2³+⋯+n³ = [n(n+1)/2]². Prove this sum-of-cubes identity using the method specified in the original question.'
assert len(OUT)==50
save('E')
