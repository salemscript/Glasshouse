# Printed780–783; approximation bounds are explicitly named, not claimed unique.
def polydegree(f,a,d):return S.series(P(f).subs(x,h+a),h,0,d+1).removeO().expand()
for i,f,dmax,points in [(1,'sin(x)',5,[pi/4,pi/2,pi]),(2,'tan(x)',3,[pi/6,pi/4,pi/3])]:
 fs=[]
 for d in range(dmax+1):
  poly=polydegree(f,0,d);fs.append(F(poly.subs(h,x),f'(a) T_{d}'))
  for z in points:fs.append(N(poly.subs(h,z),f'(b) T_{d}({fmt(z)})',tol=1e-7))
 fs.extend(N(P(f).subs(x,z),f'(b) f({fmt(z)})',tol=1e-7) for z in points)
 fs.append(C('Converges faster near the center; each fixed point inside the convergence interval is approached as degree increases','Every new degree is closer at every x','The convergence interval is always all real x',label='(c) Behavior'))
 put(11,i,*fs,limited=True)
for i,f,a in [(3,'exp(x)',1),(4,'sin(x)',pi/6),(5,'cos(x)',pi/2),(6,'exp(-x)*sin(x)',0),(7,'ln(x)',1),(8,'x*cos(x)',0),(9,'x*exp(-2*x)',0),(10,'atan(x)',1)]:
 p=polydegree(f,a,3);put(11,i,F(p,f'T₃ with h=x−({fmt(a)})'),limited=True);CASES.append(dict(kind='taylor-polynomial',id=f'calculus-section-11-11-{i}',f=f,a=str(a),poly=str(p),degree=3))
for i,f,a in [(11,'cot(x)',pi/4),(12,'(1+x*x)**(1/3)',0)]:
 put(11,i,*[F(polydegree(f,a,d),f'T_{d}, h=x−({fmt(a)})') for d in range(2,6)],limited=True)
# Bounds use maxima of the next derivative on the full source interval.
configs=[(13,'1/x',1,2,S.Rational(7,10),S.Rational(13,10)),(14,'x**(-1/2)',4,2,S.Rational(7,2),S.Rational(9,2)),(15,'x**(2/3)',1,3,S.Rational(4,5),S.Rational(6,5)),(16,'sin(x)',pi/6,4,0,pi/3),(17,'sec(x)',0,2,-S.Rational(1,5),S.Rational(1,5)),(18,'ln(1+2*x)',1,3,S.Rational(1,2),S.Rational(3,2)),(19,'exp(x*x)',0,3,0,S.Rational(1,10)),(20,'x*ln(x)',1,3,S.Rational(1,2),S.Rational(3,2)),(21,'x*sin(x)',0,4,-1,1),(22,'sinh(2*x)',0,5,-1,1)]
for i,f,a,d,lo,hi in configs:
 expr=P(f);der=S.diff(expr,x,d+1)
 M=S.Integer(1) if i==16 else S.Max(S.Abs(der.subs(x,lo)),S.Abs(der.subs(x,hi)))
 delta=max(abs(a-lo),abs(hi-a));bound=S.simplify(M*delta**(d+1)/S.factorial(d+1));p=polydegree(f,a,d)
 put(11,i,F(p,f'(a) T_{d}, h=x−({fmt(a)})'),N(M,'(b) Stated derivative bound M',tol=1e-6),N(bound,'(b) Uniform Taylor error bound',tol=1e-7),why='Use the maximum next-derivative magnitude on the full source interval and max|x−a| in M|x−a|^(n+1)/(n+1)!. The listed bound is one valid bound, not the exact maximum error.',limited=True)
 CASES.append(dict(kind='taylor-bound',id=f'calculus-section-11-11-{i}',f=f,a=str(a),degree=d,lo=str(lo),hi=str(hi),M=str(M),bound=str(bound),poly=str(p)))
put(11,23,N(S.cos(4*pi/9),'cos80° to5decimals',tol=.0000051),why='Use the expansion aboutπ/2; the local displacement is−π/18.')
put(11,24,N(S.sin(19*pi/90),'sin38° to5decimals',tol=.0000051),why='Use the expansion aboutπ/6; the displacement is2π/45.')
put(11,25,N(5,'Number of terms including constant',tol=0),N(4,'Polynomial degree',tol=0),why='e^.1(.1)^5/5!<10^−6, whereas the degree3Taylor bound fails.')
put(11,26,N(5,'Number of nonzero terms',tol=0),why='The next alternating magnitude is.4^6/6<.001; with4terms the next bound.4^5/5 exceeds.001.')
for i,r in [(27,mp.mpf('1.2')**(mp.mpf(1)/5)),(28,mp.mpf('3.6')**(mp.mpf(1)/6)),(29,mp.mpf('.35')**(mp.mpf(1)/7))]:put(11,i,N(r,'Guaranteed range |x|<this bound',tol=1e-6),why='Use the first neglected magnitude: |x|⁵/120, |x|⁶/720 or |x|⁷/7. A graph may show a slightly wider true-error interval; this field checks the stated theoretical guarantee.',limited=True)
put(11,30,N(sum(S.Rational((-1)**j,3**j*(j+1)) for j in range(6)),'T₅(5)'),N(S.Rational(1,7*3**6),'Next-term error bound'),why='The alternating sixth omitted coefficient is1/(7·3⁶)<.0002.',limited=True)
put(11,31,N(21,'Next-second distance estimate',unit='m'),C('Not justified for a full minute from instantaneous speed and acceleration alone','Always exact for a minute','The acceleration must be zero',label='Longer-time use'),why='Displacement≈20t+(2/2)t². This local model needs control of changing acceleration for longer times.',limited=True)
lo=mp.findroot(lambda u:(1+u)*mp.exp(-u)-mp.mpf('.99'),-.15);hi=mp.findroot(lambda u:(1+u)*mp.exp(-u)-mp.mpf('.99'),.15)
put(11,32,C('ρ₂₀[1+α(t−20)]','ρ₂₀αt','ρ₂₀[1−α(t−20)]',label='(a) Linear'),C('ρ₂₀[1+α(t−20)+α²(t−20)²/2]','ρ₂₀[1+α(t−20)²]','ρ₂₀[1−α²(t−20)²/2]',label='(a) Quadratic'),N(20+lo/mp.mpf('.0039'),'(c) Lower temperature, relative error<1%',tol=.01,unit='°C'),N(20+hi/mp.mpf('.0039'),'(c) Upper temperature, relative error<1%',tol=.01,unit='°C'),why='Measure relative error against the exponential model: |linear−exact|/exact<.01. The supplied copper coefficients determine the interval; the graph and comparison remain separately reviewed.',limited=True)
put(11,33,C('E=(q/D²)[2d/D−3(d/D)²+4(d/D)³−…]≈2qd/D³','E≈q/D²','E≈qd/D',label='Far-field expansion'),why='Expand(1+d/D)^−2 for |d/D|<1 and cancel the leading1.',limited=True)
put(11,34,C('n₁/s₀+n₂/sᵢ=(n₂−n₁)/R','n₁s₀+n₂sᵢ=R','n₁/s₀−n₂/sᵢ=0',label='(a) Gaussian relation'),C('Add h²[n₁(1/s₀+1/R)²/(2s₀)+n₂(1/R−1/sᵢ)²/(2sᵢ)] to the right side','Add a term linear in h','There is no correction',label='(b) Third-order correction'),why='Replace cosφ by1 for(a) and by1−φ²/2 for(b), expand reciprocal path lengths, and retain the stated orders.',limited=True)
put(11,35,C('v≈sqrt(gL/(2π))','v≈sqrt(gd)','v≈gL',label='(a) Deep water'),C('v≈sqrt(gd)','v≈sqrt(gL/(2π))','v≈gd',label='(b) Shallow water'),N(4*pi*pi/3000,'(c) Coefficient bounding error in v² as a multiple of gL'),why='The next tanh term gives error≤4π²gd³/(3L²); ifd/L<.1 this is<.014gL.',limited=True)
put(11,36,C('V≈πkₑR²σ/d','V≈2πkₑRσ','V≈πkₑR²σ/d²'),why='Factor d from√(d²+R²) and use√(1+u)=1+u/2+…; cancel d.',limited=True)
put(11,37,C('C=R sec(L/R)−R','C=R cos(L/R)−R','C=L²/R',label='(a)'),C('C≈L²/(2R)+5L⁴/(24R³)','C≈L²/R+L⁴/R³','C≈L/R',label='(b)'),N(6370*(1/mp.cos(mp.mpf(100)/6370)-1),'(c) Exact correction',unit='km'),N(mp.mpf(100)**2/(2*6370)+5*mp.mpf(100)**4/(24*mp.mpf(6370)**3),'(c) Fourth-degree correction',unit='km'),limited=True)
fs=[C('T=2πsqrt(L/g)[1+k²/4+9k⁴/64+25k⁶/256+…]','T=2πsqrt(L/g)[1−k²/4+…]','T=2πsqrt(L/g) exactly',label='(a)'),C('2πsqrt(L/g)(1+k²/4)≤T≤2πsqrt(L/g)(4−3k²)/(4−4k²)','The inequalities reverse','Both bounds equal the small-angle period',label='(b)')]
base=2*mp.pi/mp.sqrt(mp.mpf('9.8'))
for angle in [10,42]:
 k=mp.sin(mp.pi*angle/360);fs.extend([N(base*(1+k*k/4),f'(c) {angle}° lower bound',unit='s'),N(base*(4-3*k*k)/(4-4*k*k),f'(c) {angle}° upper bound',unit='s')])
fs.append(N(base,'(c) Small-angle estimate, g=9.8',unit='s'));put(11,38,*fs,why='Use the source k=sin(theta₀/2), L=1m and explicitly g=9.8m/s². All correction coefficients are positive.',limited=True)
put(11,39,C('|x_(n+1)−r|≤M|x_n−r|²/(2K)','|x_(n+1)−r|≤M|x_n−r|/K','Newton error is always zero'),why='Taylor-expand f(r)=0 about x_n and divide by |f′(x_n)|≥K; the linear Newton step cancels.',limited=True)
# Radiation project uses the textbook's stated physical constants.
group='Project: Applied Project Radiation From The Stars';hc=mp.mpf('6.6262e-34')*mp.mpf('2.997925e8');kb=mp.mpf('1.3807e-23');peak=mp.findroot(lambda z:5*(1-mp.exp(-z))-z,5)
put(11,1,N(0,'λ→0+ limit'),N(0,'λ→∞ limit'),why='At short wavelength the exponential dominates λ^−5; at long wavelength exp(u)−1~u leaves λ^−4.',limited=True,group=group)
put(11,2,C('f(λ)≈8πkT/λ⁴ when hc/(λkT)≪1','f(λ)≈8πhc/λ⁵','f is constant in λ'),why='Use e^u−1≈u and cancel hc.',limited=True,group=group)
put(11,3,C('Rayleigh–Jeans lies above Planck for λ>0; they agree asymptotically at long wavelengths','They agree at short wavelengths and diverge at long wavelengths','Rayleigh–Jeans is below Planck everywhere'),why='For u>0,e^u−1>u; both laws use T=5700K. Plotting in micrometers requires converting λ to meters in the formula.',limited=True,group=group)
put(11,4,N(hc/(kb*5700*peak)*10**6,'Peak wavelength at5700K',tol=.005,unit='μm'),why='The nonzero maximum solves5(1−e^(−u))=u, u≈4.965114; λ=hc/(kTu).',limited=True,group=group)
put(11,5,*[N(hc/(kb*T*peak)*10**6,f'Peak wavelength at{T}K',tol=.005,unit='μm') for T in [3400,6400,9200,5700]],C('Total area is proportional to T⁴','Total area is proportional to T','Total area is temperature-independent',label='Integrated radiation'),C('Hotter Sirius shifts toward shorter/bluer wavelengths; cooler Betelgeuse toward longer/redder wavelengths','Hotter means redder peak','Both stars have identical spectra',label='Color trend'),why='Substitute u=hc/(λkT) in the total integral; the dimensionless integral is constant. The spectrum is broad, so the peak alone does not determine perceived color.',limited=True,group=group)
