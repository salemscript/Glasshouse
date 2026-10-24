# Printed771–773; direct Taylor coefficients and independently recognizable expansions.
h=S.symbols('h',real=True)
def taylor(f,a,count=None,degree=16):
 f=P(f);z=S.series(f.subs(x,h+a),h,0,degree).removeO().expand();terms=[z.coeff(h,k)*h**k for k in range(degree) if z.coeff(h,k)!=0];return S.Add(*(terms[:count] if count else terms))
def radfield(r):return C('∞','0','1',label='Radius') if r==S.oo else N(r,'Radius')
def ts(i,text,r=S.oo,limited=False):put(10,i,sf(text),radfield(r),limited=limited,why='Taylor coefficient is f^(n)(a)/n!. The stated series is centered at the source center; convergence radius follows from ratio/root tests or the nearest singularity.')
put(10,1,C('f^(8)(5)/8!','f^(8)(0)/8!','8!f^(8)(5)',label='b₈'))
put(10,2,C('The proposed linear coefficient−.8 contradicts the positive slope at1','The graph is decreasing at1','A Taylor series cannot have negative coefficients',label='(a)'),C('The proposed quadratic coefficient1.5 implies f″(2)>0, but the graph is concave down there','The graph is concave up at2','The constant coefficient alone proves the error',label='(b)'),limited=True)
ts(3,'Σ_(n=0)^∞(n+1)x^n',1)
ts(4,'Σ_(n=0)^∞(−1)^n(x−4)^n/[3^n(n+1)]',3)
for i,f,a in [(5,'x*exp(x)',0),(6,'1/(1+x)',2),(7,'x**(1/3)',8),(8,'ln(x)',1),(9,'sin(x)',pi/6),(10,'cos(x)**2',0)]:
 poly=taylor(f,a,4);put(10,i,F(poly,f'First4nonzero terms; h=x−({fmt(a)})'),why='Differentiate at the stated center and divide by the factorial; include the constant term when nonzero.');CASES.append(dict(kind='taylor-polynomial',id=f'calculus-section-11-10-{i}',f=f,a=str(a),poly=str(poly),count=4))
for i,text,r in [(11,'Σ_(n=0)^∞(n+1)x^n',1),(12,'Σ_(n=1)^∞(−1)^(n−1)x^n/n',1),(13,'Σ_(n=0)^∞(−1)^n x^(2n)/(2n)!',S.oo),(14,'Σ_(n=0)^∞(−2)^n x^n/n!',S.oo),(15,'Σ_(n=0)^∞(ln2)^n x^n/n!',S.oo),(16,'Σ_(n=0)^∞(−1)^n x^(2n+1)/(2n)!',S.oo),(17,'Σ_(n=0)^∞x^(2n+1)/(2n+1)!',S.oo),(18,'Σ_(n=0)^∞x^(2n)/(2n)!',S.oo)]:ts(i,text,r)
for i,f,a,degree in [(19,'x**5+2*x**3+x',2,6),(20,'x**6-x**4+2',-2,7)]:
 poly=taylor(f,a,degree=degree);put(10,i,F(poly,f'Exact Taylor polynomial; h=x−({a})'),radfield(S.oo));CASES.append(dict(kind='taylor-polynomial',id=f'calculus-section-11-10-{i}',f=f,a=str(a),poly=str(poly),count=degree))
for i,text,r in [(21,'ln2+Σ_(n=1)^∞(−1)^(n−1)(x−2)^n/(n2^n)',2),(22,'−Σ_(n=0)^∞(x+3)^n/3^(n+1)',3),(23,'e^6 Σ_(n=0)^∞2^n(x−3)^n/n!',S.oo),(24,'−Σ_(n=0)^∞(−1)^n(x−π/2)^(2n+1)/(2n+1)!',S.oo),(25,'−Σ_(n=0)^∞(−1)^n(x−π)^(2n+1)/(2n+1)!',S.oo),(26,'4Σ_(n=0)^∞binom(1/2,n)((x−16)/16)^n',16)]:ts(i,text,r)
for i,center,bound in [(27,'0','|x|^(N+1)/(N+1)!'),(28,'π','|x−π|^(N+1)/(N+1)!'),(29,'0','e^|x| |x|^(N+1)/(N+1)!'),(30,'0','e^|x| |x|^(N+1)/(N+1)!')]:put(10,i,C(bound+'→0 for fixed x','Remainder is always0','Radius alone proves equality to the function',label='Taylor remainder bound'),limited=True)
for i,text,r in [(31,'Σ_(n=0)^∞binom(1/4,n)(−x)^n',1),(32,'2Σ_(n=0)^∞binom(1/3,n)(x/8)^n',8),(33,'(1/8)Σ_(n=0)^∞binom(−3,n)(x/2)^n',2),(34,'Σ_(n=0)^∞binom(3/4,n)(−x)^n',1)]:ts(i,text,r)
for i,text,r in [(35,'Σ_(n=0)^∞(−1)^n x^(4n+2)/(2n+1)',1),(36,'Σ_(n=0)^∞(−1)^n(πx/4)^(2n+1)/(2n+1)!',S.oo),(37,'Σ_(n=0)^∞(−1)^n2^(2n)x^(2n+1)/(2n)!',S.oo),(38,'Σ_(n=1)^∞(3^n−2^n)x^n/n!',S.oo),(39,'Σ_(n=0)^∞(−1)^n x^(4n+1)/[2^(2n)(2n)!]',S.oo),(40,'Σ_(n=1)^∞(−1)^(n−1)x^(3n+2)/n',1),(41,'(x/2)Σ_(n=0)^∞binom(−1/2,n)(x²/4)^n',2),(42,'(x²/sqrt(2))Σ_(n=0)^∞binom(−1/2,n)(x/2)^n',2),(43,'Σ_(n=1)^∞(−1)^(n+1)2^(2n−1)x^(2n)/(2n)!',S.oo),(44,'Σ_(n=0)^∞(−1)^n x^(2n)/(2n+3)!',S.oo)]:ts(i,text,r)
for i,text,r in [(45,'Σ_(n=0)^∞(−1)^n x^(4n)/(2n)!',S.oo),(46,'Σ_(n=1)^∞(−1)^(n−1)x^(2n)/n',1),(47,'Σ_(n=0)^∞(−1)^n x^(n+1)/n!',S.oo),(48,'Σ_(n=0)^∞(−1)^n x^(6n+3)/(2n+1)',1)]:ts(i,text,r,True)
put(10,49,N(S.cos(pi/36),'cos5° to5decimal places',tol=.0000051),why='Convert degrees to radians before substituting into the cosine Maclaurin series.')
put(10,50,N(S.exp(-S.Rational(1,10)),'1/tenth-root(e) to5decimal places',tol=.0000051))
put(10,51,sf('Σ_(n=0)^∞(2n)!x^(2n)/[4^n(n!)²]','(a)'),sf('Σ_(n=0)^∞(2n)!x^(2n+1)/[4^n(n!)²(2n+1)]','(b) arcsin x'),why='Integrate the binomial series from0to x; arcsin0=0 fixes the constant.')
put(10,52,sf('Σ_(n=0)^∞binom(−1/4,n)x^n','(a)'),N(mp.mpf('1.1')**(-mp.mpf('.25')),'(b) Approximation to3decimals',tol=.00051))
for i,text,r in [(53,'C+Σ_(n=0)^∞binom(1/2,n)x^(3n+1)/(3n+1)',1),(54,'C+Σ_(n=0)^∞(−1)^n x^(4n+5)/[(4n+5)(2n+1)!]',S.oo),(55,'C+Σ_(n=1)^∞(−1)^n x^(2n)/[2n(2n)!]',S.oo),(56,'C+Σ_(n=0)^∞(−1)^n x^(4n+3)/[(4n+3)(2n+1)]',1)]:ts(i,text,r)
for i,fun,b,tol in [(57,lambda z:z**3*mp.atan(z),mp.mpf('.5'),.000051),(58,lambda z:mp.sin(z**4),1,.000051),(59,lambda z:mp.sqrt(1+z**4),mp.mpf('.4'),.000005),(60,lambda z:z*z*mp.exp(-z*z),mp.mpf('.5'),.001)]:put(10,i,N(mp.quad(fun,[0,b]),'Integral',tol=tol),why='Integrate the source Maclaurin/binomial series and bound the omitted tail; high-precision quadrature independently checks the result.')
for i,v in {61:S.Rational(1,2),62:-1,63:S.Rational(1,120),64:-S.Rational(1,8),65:S.Rational(3,5),66:S.Rational(1,3)}.items():put(10,i,N(v,'Limit'),limited=i==66,why='Cancel the lower-order Taylor terms and divide by the stated power; the surviving coefficient gives the limit.')
for i,f in [(67,'exp(-x*x)*cos(x)'),(68,'1/cos(x)'),(69,'x/sin(x)'),(70,'exp(x)*ln(1+x)'),(71,'atan(x)**2'),(72,'exp(x)*sin(x)**2')]:
 poly=taylor(f,0,3);put(10,i,F(poly.subs(h,x),'First3nonzero terms'));CASES.append(dict(kind='taylor-polynomial',id=f'calculus-section-11-10-{i}',f=f,a='0',poly=str(poly),count=3))
for i,v in [(74,S.sqrt(3)/2),(75,S.log(S.Rational(8,5))),(76,S.exp(S.Rational(3,5))),(77,S.sqrt(2)/2),(78,S.Rational(1,2)),(79,S.exp(3)-1),(80,S.atan(S.Rational(1,2)))]:put(10,i,N(v,'Sum'),why='Recognize the appropriate exponential, logarithmic, sine/cosine or arctangent Maclaurin series, including the starting index.')
put(10,73,F(S.exp(-x**4),'Sum'))
put(10,81,C('Taylor expansion about x evaluated at x+1; derivatives above degree n vanish','The remainder is nonzero for every polynomial','All derivatives equal1'),limited=True)
put(10,82,N(0,'f^(58)(0)',tol=0),why='Only powers divisible by3 occur in(1+x³)^30; the x^58 coefficient is0.')
put(10,83,C('|R₂(x)|≤M|x−a|³/6','|R₂(x)|≤M|x−a|²/2','|R₂(x)|=0'),why='Integrate the third-derivative bound three times, or use the Lagrange remainder with3!=6.',limited=True)
put(10,84,C('All derivatives at0 are0, so the Maclaurin series is0 while f(x)>0 for x≠0','The Maclaurin series is e^x','f has no derivative at0',label='(a)'),C('The graph is positive off0 and flatter than every power near0','The graph has a cusp at0','The graph crosses below0',label='(b)'),limited=True)
put(10,85,C('g′=kg/(1+x)','g′=kg','g′=0',label='(a)'),N(0,'(b) h′'),C('h is constant and h(0)=1, so g=(1+x)^k for |x|<1','h=0','g=(1−x)^k',label='(c)'),limited=True)
put(10,86,C('L=2πa[1−e²/4−3e⁴/64−5e⁶/256+…]','L=2πa[1+e²/4+3e⁴/64+…]','L=2πb for every ellipse',label='Expansion through e⁶'),why='Use sqrt(1−u)=1−u/2−u²/8−u³/16+… and ∫₀^(π/2)sin^(2n)θdθ=(π/2)(2n)!/[4^n(n!)²].')
# Elusive-limit project: cancellations begin at order7.
group='Project: Laboratory Project An Elusive Limit'
fn=lambda z:(mp.sin(mp.tan(z))-mp.tan(mp.sin(z)))/(mp.asin(mp.atan(z))-mp.atan(mp.asin(z)))
put(10,1,*[N(fn(mp.mpf(z)),f'f({z}), high precision',tol=1e-7) for z in ['1','.1','.01','.001','.0001']],C('Appears to approach1 when evaluated with sufficient precision','The true limit fails to exist','Approaches0',label='Conclusion'),group=group,limited=True)
put(10,2,C('A stable high-precision plot approaches1; ordinary precision may show artifacts','The graph proves divergence','The limit is0'),group=group,limited=True)
put(10,3,N(7,'Required l’Hôpital differentiations before nonzero constants',tol=0),N(1,'Limit'),group=group,limited=True)
put(10,4,C('Numerator=−x⁷/30+O(x⁹); denominator=−x⁷/30+O(x⁹)','Leading terms are x and−x','Numerator has lower order',label='Leading terms'),N(1,'Limit'),group=group,limited=True)
put(10,5,N(1,'CAS limit'),group=group,limited=True)
put(10,6,C('Subtraction of nearly equal quantities loses significant digits; use higher precision or Taylor expansions','The mathematical limit depends on machine precision','A graph always decides a limit'),group=group,limited=True)
# One real writing assignment, not four bibliography exercises.
group='Project: Writing Project How Newton Discovered The Binomial Series'
put(10,'Report',C('Coefficient of z^j is α(α−1)…(α−j+1)/j!','Coefficient is α^j','Coefficient is j!',label='Generalized binomial coefficient'),C('∫₀ˣ(1−t²)^αdt=Σ_(j=0)^∞(−1)^j binom(α,j)x^(2j+1)/(2j+1), |x|<1','The integral is always x','The denominator is2j instead of2j+1',label='Area-series pattern'),C('For nonnegative integer α the expansion terminates; fractional α generally gives an infinite series','Every fractional-power expansion terminates','Only integer exponents have expansions',label='Interpolation distinction'),why='Checks only mathematical conclusions in the shared report. Historical reading, Newton’s original notation, evidence from his letters and the written explanation must be reviewed separately. The four printed numbered items are retained references, not exercises.',limited=True,group=group)
