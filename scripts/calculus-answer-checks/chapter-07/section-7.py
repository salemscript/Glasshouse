# Composite quadrature from explicitly transcribed functions and data, pages 524–527.
QUAD=[]
def quad(f,a,b,n,kind):
 h=(mp.mpf(b)-a)/n
 if kind=='L':return h*sum(f(a+k*h) for k in range(n))
 if kind=='R':return h*sum(f(a+k*h) for k in range(1,n+1))
 if kind=='M':return h*sum(f(a+(k+mp.mpf('.5'))*h) for k in range(n))
 if kind=='T':return h*(f(a)/2+f(b)/2+sum(f(a+k*h) for k in range(1,n)))
 assert kind=='S' and n%2==0
 return h/3*(f(a)+f(b)+sum((4 if k%2 else 2)*f(a+k*h) for k in range(1,n)))
def qfields(i,f,a,b,n,kinds='TMS',error=False):
 f=P(f);fun=s.lambdify(x,f,'mpmath');truth=mp.quad(fun,[a,b]);fs=[]
 for kind in kinds:
  value=quad(fun,a,b,n,kind);fs.append(num(f'{kind}_{n}',value,tol=6e-7))
  if error:fs.append(num(f'E_{kind} = I−{kind}_{n}',truth-value,tol=6e-7))
  QUAD.append(dict(id=f'calculus-section-7-7-{i}',f=str(f),a=str(a),b=str(b),n=n,kind=kind,value=str(value),error=str(truth-value)))
 return fs
put(7,1,[num('(a) L₂',6,tol=.15),num('(a) R₂',12,tol=.15),num('(a) M₂',9.4,tol=.25),choice('(b) estimates','L₂ under; R₂ and M₂ over','L₂ and M₂ under; R₂ over','All under'),num('(c) T₂',9,tol=.15),choice('(c,d) increasing order','L_n < T_n < I < M_n < R_n','L_n < M_n < I < T_n < R_n','R_n < T_n < I < M_n < L_n')],'Read approximate heights from the source graph. Increasing and concave down gives the indicated ordering; graph-reading tolerances are explicit.',True)
put(7,2,[num('(a) L',.9540,tol=.00001),num('(a) R',.7811,tol=.00001),num('(a) T',.8675,tol=.0001),num('(a) M',.8632,tol=.00001),choice('(b) bounds','0.8632 < I < 0.8675','0.7811 < I < 0.8632','0.8675 < I < 0.9540')],'The source curve is decreasing and concave up; R<M<I<T<L.',True)
put(7,3,qfields(3,'cos(x*x)',0,1,4,'TM')+[choice('Bounds','T₄ < I < M₄','M₄ < I < T₄','Both exceed I')],'The integrand is concave down on [0,1].',True)
put(7,4,[choice('(a,b) order','L_n < M_n < I < T_n < R_n','L_n < T_n < I < M_n < R_n','R_n < M_n < I < T_n < L_n')]+qfields(4,'sin(x*x/2)',0,1,5,'LRMT')+[choice('(c) closest listed estimate','M₅','L₅','R₅','T₅')],'sin(x²/2) is increasing and concave up on [0,1]; midpoint has the smaller leading curvature error.',True)
for i,f,a0,b0,nn in [(5,'x/(1+x*x)',0,2,10),(6,'x*cos(x)',0,mp.pi,4)]:put(7,i,qfields(i,f,a0,b0,nn,'MS',True),'Use equal-width panels. Errors use the signed convention E=exact integral−approximation.')
for i,f,a0,b0,nn in [(7,'sqrt(x**3-1)',1,2,10),(8,'1/(1+x**6)',0,2,8),(9,'exp(x)/(1+x*x)',0,2,10),(10,'(1+cos(x))**(1/3)',0,mp.pi/2,4),(11,'x**3*sin(x)',0,4,8),(12,'exp(1/x)',1,3,8),(13,'sqrt(x)*cos(x)',0,4,8),(14,'1/log(x)',2,3,10),(15,'x*x/(1+x**4)',0,1,10),(16,'sin(x)/x',1,3,4),(17,'log(1+exp(x))',0,4,8),(18,'sqrt(x+x**3)',0,1,10)]:put(7,i,qfields(i,f,a0,b0,nn),'Composite trapezoidal and midpoint use n equal panels; Simpson uses alternating 4,2 weights and even n.')
def bound(K,length,nn,kind):return K*length**(3 if kind!='S' else 5)/((12 if kind=='T' else 24 if kind=='M' else 180)*nn**(2 if kind!='S' else 4))
def needed(K,length,err,kind):
 raw=(K*length**(3 if kind!='S' else 5)/((12 if kind=='T' else 24 if kind=='M' else 180)*err))**(mp.mpf(1)/(2 if kind!='S' else 4));nn=int(mp.floor(raw))+1
 if kind=='S' and nn%2:nn+=1
 return nn
for i,f,a0,b0,nn,K in [(19,'cos(x*x)',0,1,8,mp.mpf(6)),(20,'exp(1/x)',1,2,10,3*mp.e)]:
 fs=qfields(i,f,a0,b0,nn,'TM')
 fs.extend([num(f'(b) {kind} error bound using K₂={float(K):.6f}',bound(K,b0-a0,nn,kind),tol=1e-7) for kind in 'TM'])
 fs.extend([num(f'(c) smallest n from this stated K₂ bound for {kind}',needed(K,b0-a0,mp.mpf('.0001'),kind),tol=0) for kind in 'TM'])
 put(7,i,fs,'Use |f″|≤6 for cos(x²) on [0,1], or |f″|≤3e for e^(1/x) on [1,2]. Other valid upper bounds can yield different sufficient n; these fields explicitly use the stated K₂.')
fs=qfields(21,'sin(x)',0,mp.pi,10,'TMS',True)
fs.extend(num(f'(b) {kind} absolute error bound',bound(1,mp.pi,10,kind),tol=6e-7) for kind in 'TMS')
fs.extend(num(f'(c) smallest sufficient n ({kind}; Simpson even)',needed(1,mp.pi,mp.mpf('.00001'),kind),tol=0) for kind in 'TMS')
put(7,21,fs,'Both |f″| and |f⁽⁴⁾| are at most 1; exact integral is 2. Error estimates bound absolute errors.')
put(7,22,num('Smallest even n guaranteed by K₄=76e',needed(76*mp.e,1,mp.mpf('.00001'),'S'),tol=0),'f⁽⁴⁾=(12+48x²+16x⁴)e^(x²)≤76e on [0,1].')
for i,f,a0,b0,K2,K4 in [(23,'exp(cos(x))',0,2*mp.pi,mp.e,4*mp.e),(24,'sqrt(4-x**3)',-1,1,mp.mpf('2.2'),mp.mpf('19'))]:
 fs=[num('(a) stated safe K₂',K2,tol=.01)]+qfields(i,f,a0,b0,10,'M')
 fun=s.lambdify(x,P(f),'mpmath');truth=mp.quad(fun,[a0,b0]);err=truth-quad(fun,a0,b0,10,'M')
 fs.extend([num('(c) M₁₀ absolute error bound',bound(K2,b0-a0,10,'M'),tol=1e-6),num('(d) accurate integral',truth,tol=1e-6),num('(e) actual signed M error',err,tol=1e-6),num('(f) stated safe K₄',K4,tol=.01)])
 fs.extend(qfields(i,f,a0,b0,10,'S'));fs.extend([num('(h) S₁₀ absolute error bound',bound(K4,b0-a0,10,'S'),tol=1e-6),num('(i) actual signed S error',truth-quad(fun,a0,b0,10,'S'),tol=1e-6),num('(j) smallest sufficient even n from this K₄',needed(K4,b0-a0,mp.mpf('.0001'),'S'),tol=0)])
 put(7,i,fs,'The graph-bound answer is nonunique; these checks use the explicitly stated derivative bounds. Recompute all dependent error bounds from those constants. Signed errors are exact minus approximation.',True)
for i,f,a0,b0,ns,kinds in [(25,'x*exp(x)',0,1,[5,10,20],'LRTM'),(26,'1/x**2',1,2,[5,10,20],'LRTM'),(27,'x**4',0,2,[6,12],'TMS'),(28,'1/sqrt(x)',1,4,[6,12],'TMS')]:
 fs=[]
 for nn in ns:fs+=qfields(i,f,a0,b0,nn,kinds,True)
 fs.append(choice('Error trend when n doubles','Endpoint errors roughly halve; T/M errors roughly quarter; Simpson errors roughly divide by 16','Every error halves','Errors are unchanged'))
 put(7,i,fs,'The trend refers to asymptotic error orders; ratios need not equal their limiting values exactly.',True)
put(7,29,[num('(a) T₆',19,tol=.3),num('(b) M₆',18.8,tol=.4),num('(c) S₆',56/3,tol=.3)],'Graph readings at integer x are approximately 2,1,3,5,4,3,4; midpoint heights are approximate. Graph-reading tolerance is included.',True)
def dataS(ys,h):return mp.mpf(str(h))/3*(ys[0]+ys[-1]+sum((4 if k%2 else 2)*ys[k] for k in range(1,len(ys)-1)))
put(7,30,num('Pool area',dataS([0,6.2,7.2,6.8,5.6,5.0,4.8,4.8,0],2),'m²',.01),'The seven labeled interior widths are 2 m apart; endpoint widths are zero, giving eight subintervals.')
put(7,31,[num('(a) M₄',14.4),num('(b) absolute error bound',.5)],'Four width-1 panels use f(1.5),f(2.5),f(3.5),f(4.5). With |f″|≤3, error≤3·4³/(24·4²)=1/2.')
put(7,32,[num('(a) Simpson estimate',dataS([12.1,11.6,11.3,11.1,11.7,12.2,12.6,13.0,13.2],.2),tol=1e-6),num('(b) absolute error bound',5*1.6**5/(180*8**4),tol=1e-9)],'Use all nine equally spaced samples, n=8, and |g⁽⁴⁾|≤5.')
put(7,33,num('Average temperature',dataS([66.5,65.5,64,62,67,72,75,77,79,75.5,75.5,71.5,67.5],2)/24,'°F',.8),'Approximate graph readings every two hours enter S₁₂; divide the estimated temperature integral by 24 hours.',True)
put(7,34,num('Distance',dataS([0,4.67,7.34,8.86,9.73,10.22,10.51,10.67,10.76,10.81,10.81],.5),'m',.001),'Integrate speed with Simpson panels of width 0.5 seconds.')
put(7,35,num('Velocity increase',dataS([0,.5,4,10,13,9.5,0],1),'ft/s',1),'Source graph heights at one-second spacing give approximately 38 ft/s; visual read-off tolerance is 1 ft/s.',True)
put(7,36,num('Water leaked',dataS([4,3,2.4,1.8,1.4,1.1,1],1),'L',.35),'Source rate is liters per hour and the request says six hours, despite the graph axis being mislabeled seconds. Integrate on the intended hour scale; graph-reading tolerance is included.',True)
put(7,37,num('Energy consumed',dataS([1814,1735,1686,1646,1637,1609,1604,1611,1621,1666,1745,1886,2052],.5),'MWh',.01),'Power in MW integrated over hours gives MWh, using all thirteen half-hour samples.')
put(7,38,num('Data transmitted',3600*dataS([.35,.31,.4,.5,.5,.56,.56,.83,.88],1),'megabits',600),'Graph readings at one-hour spacing are approximate. Multiply the rate integral by 3600 seconds/hour.',True)
y=[0,1.5,1.9,2.2,3,3.8,4,3,0]
put(7,39,[num('(a) Volume about x-axis',mp.pi*dataS([v*v for v in y],1),tol=6),num('(b) Volume about y-axis',2*mp.pi*dataS([(k+2)*v for k,v in enumerate(y)],1),tol=15)],'The graph region spans x=2 to 10, n=8. Use πy² for disks and 2πxy for shells; approximate heights carry graph-reading tolerances.',True)
put(7,40,num('Work',dataS([9.8,9.1,8.5,8,7.7,7.5,7.4],3),'J',.01),'Use Simpson n=6, width3m; force times distance yields joules.')
put(7,41,num('Volume',quad(lambda z:mp.pi/(1+mp.exp(-z))**2,0,10,10,'S'),tol=1e-6),'Square the logistic radius before applying Simpson n=10.')
put(7,42,num('Period using g=9.8 m/s²',4/mp.sqrt(mp.mpf('9.8'))*quad(lambda z:1/mp.sqrt(1-mp.sin(21*mp.pi/180)**2*mp.sin(z)**2),0,mp.pi/2,10,'S'),'s',.00001),'Convert 42° to radians and use k=sin21°; L=1m. The specified g convention removes rounding ambiguity.')
N=mp.mpf(10000);d=mp.mpf('1e-4');lam=mp.mpf('632.8e-9')
fun=lambda z:N*N*(mp.sin(mp.pi*N*d*mp.sin(z)/lam)/(mp.pi*N*d*mp.sin(z)/lam))**2 if z else N*N
put(7,43,num('Total integrated intensity',quad(fun,mp.mpf('-1e-6'),mp.mpf('1e-6'),10,'M'),tol=.001),'Use the symmetric ten-panel midpoint rule. The removable value at zero is N²; angular input is radians.')
put(7,44,[num('T₁₀',20),num('Exact integral',0),choice('Discrepancy','Sampling every 2 units hits cosine maxima and misses all oscillations','Trapezoidal rule is always exact for cosine','The true integral is 20')],'Each grid point x=2k has cosπx=1; this is a sampling/aliasing error.')
put(7,45,choice('A valid continuous example','f(x)=x⁴−(39/5)x² on [0,2]','f(x)=x on [0,2]','f(x)=x² on [0,2]'),'T₂ error for x⁴ is 13/5 and for x² is 1/3, so the stated combination has zero trapezoidal error and nonzero midpoint error.',True)
put(7,46,choice('A valid continuous example','f(x)=x⁴−(53/5)x on [0,2]','f(x)=x on [0,2]','f(x)=x² on [0,2]'),'R₂(x⁴)=17 and exact=32/5; R₂(x)=3 and exact=2, so R₂ is exact for x⁴−(53/5)x. Simpson retains its nonzero quartic error.',True)
put(7,47,choice('Ordering for f″<0','T_n < I < M_n','M_n < I < T_n','I < T_n < M_n'),'For strict concavity, chords lie below the graph and midpoint tangent rectangles overestimate panel areas.',True)
put(7,48,choice('Reason Simpson is exact through degree 3','f⁽⁴⁾=0, so its error bound is zero','Every polynomial has zero fourth derivative','Simpson is exact for every continuous function'),'The fourth-derivative error bound vanishes for polynomials of degree at most three.',True)
put(7,49,choice('Refinement identity','T_(2n)=(T_n+M_n)/2','T_(2n)=T_n+M_n','T_(2n)=(T_n−M_n)/2'),'The fine trapezoid mesh interleaves coarse endpoints and coarse midpoints.',True)
put(7,50,choice('Simpson identity','S_(2n)=T_n/3+2M_n/3','S_(2n)=2T_n/3+M_n/3','S_(2n)=(T_n+M_n)/2'),'Expand weights on the shared refined mesh: endpoint1, old interior2, midpoint4.',True)
(HERE/'quadrature-cases.json').write_text(json.dumps(QUAD,indent=2)+'\n')
