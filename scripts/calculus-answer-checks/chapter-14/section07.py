from common import *
row=lambda k,*fs,**kw:A.row(7,k,*fs,**kw)
row(1,c('a','Local minimum','Local maximum','Saddle'),c('b','Saddle','Local minimum','Local maximum'),why='D=7>0 with f_xx>0 in(a); D=−1<0 in(b).')
row(2,c('a','Saddle','Local minimum','Local maximum'),c('b','Local maximum','Local minimum','Saddle'),c('c','Test inconclusive','Local minimum guaranteed','Saddle guaranteed'),why='D=−37,4,0 respectively; for(b),g_xx<0.')
polys={3:4+x**3+y**3-3*x*y,4:3*x-x**3-2*y*y+y**4,5:x*x+x*y+y*y+y,6:x*y-2*x-2*y-x*x-y*y,7:(x-y)*(1-x*y),8:y*(s.exp(x)-1),9:x*x+y**4+2*x*y,10:2-x**4+2*x*x-y*y,11:x**3-3*x+3*x*y*y,12:x**3+y**3-3*x*x-3*y*y-9*x,13:x**4-2*x*x+y**3-3*y}
poly_audit={}
for k,ex in polys.items():
 sols=s.solve([s.diff(ex,x),s.diff(ex,y)],[x,y],dict=True);sols=[pt for pt in sols if all(q.is_real is not False for q in pt.values())];sols.sort(key=lambda pt:(float(pt[x]),float(pt[y])))
 fs=[];info=[]
 for i,pt in enumerate(sols):
  H=s.hessian(ex,[x,y]).subs(pt);det=s.simplify(H.det());typ='Saddle' if det<0 else 'Local minimum' if H[0,0]>0 else 'Local maximum'
  fs.extend([c('Critical point '+str(i+1),f'({fmt(pt[x])},{fmt(pt[y])})',f'({fmt(pt[x]+1)},{fmt(pt[y])})',f'({fmt(pt[x])},{fmt(pt[y]+1)})'),c('Classification '+str(i+1),typ,*[v for v in ['Local minimum','Local maximum','Saddle'] if v!=typ]),n('Function value '+str(i+1),ex.subs(pt))]);info.append([str(pt),str(det),typ])
 row(k,*fs,limited=k in [3,4],why='Solve both first partials equal to0, then use D=f_xx f_yy−f_xy² and the sign of f_xx. The values are evaluated in the original function.');poly_audit[k]=info
row(14,c('Critical points and type','(π/2+kπ,0), every one a saddle, k∈Z','(kπ,0), all minima','No critical points'),c('Local extrema','None','Maximum1 and minimum−1','Minimum0'))
row(15,c('Critical points and extrema','No critical points and no local extrema','Critical point(0,0) is a maximum','Minimum−1'),why='f_x=e^x cos y and f_y=−e^x sin y cannot both vanish.')
row(16,c('Maxima','(1,1),(−1,−1), value1/e','(1,−1),(−1,1), value1/e','Origin, value0'),c('Minima','(1,−1),(−1,1), value−1/e','(1,1),(−1,−1), value−1/e','No minima'),c('Saddle','(0,0)','(1,0)','None'))
row(17,c('Minima','Every point with xy=0 has absolute minimum1','Only(0,0), minimum0','Every point with xy=1 has minimum1'),c('Maxima and saddles','None','Origin is a saddle','All points on axes are maxima'),why='u+e^(−u)≥1 with equality only u=0; set u=xy.')
row(18,c('Critical points','(0,0): absolute minimum0; (2,0): saddle4/e²','(0,0): maximum0; (2,0): minimum','Only(0,0)'),c('Local maximum','None','4/e²','1'))
row(19,c('Local minima','(0,1),(π,−1),(2π,1), each value−1','(0,0),(π,0), each value0','No minima'),c('Saddles','(π/2,0),(3π/2,0)','(0,1),(π,−1)','No saddles'),c('Local maxima','None','1','0'))
row(20,c('Local maxima','(π/2,π/2),(−π/2,−π/2), value1','(π/2,−π/2),(−π/2,π/2), value1','Origin, value0'),c('Local minima','(π/2,−π/2),(−π/2,π/2), value−1','Origin, value0','No minima'),c('Saddle','(0,0)','(π/2,π/2)','None'))
row(21,c('Critical set','x=2y, with D=0 everywhere on this line','x=y only','Origin only'),n('Absolute minimum',2),limited=True,why='f=(x−2y)²+2, so every point on the zero-square line is a minimum.')
row(22,c('Nonzero-x extrema','Maxima at(±1,1/√2), value e^(−3/2)/√2; minima at(±1,−1/√2), value−e^(−3/2)/√2','All four points are maxima','Only the origin is critical'),c('Critical line x=0','y>0 gives local minima0; y<0 gives local maxima0; origin is a saddle; D=0 along line','All are saddles','All are minima'),limited=True,why='The nonnegative factor x²e^(−x²−y²) makes the sign equal to sign(y).')
row(23,c('Critical points','(±1,±1), independently chosen signs, all absolute minima3','Origin, minimum0','(±1,±1), all saddles'),c('Other extrema/saddles','None','One maximum at origin','Four saddles'),limited=True,why='For x,y≠0, AM–GM gives x²+y²+1/(x²y²)≥3, with equality when x²=y²=1.')
row(24,c('Maximum','(1/2,−1/2), value e^(−1/2)','(−1/2,1/2), value e^(−1/2)','Origin, value1'),c('Minimum','(−1/2,1/2), value−e^(−1/2)','Origin, value0','None'),c('Saddles','None','Origin','(1/2,−1/2)'),limited=True)
row(25,c('Interior extrema and saddle','Maximum3√3/2 at(π/3,π/3); minimum−3√3/2 at(5π/3,5π/3); saddle(π,π)','Maximum3 at(π/2,π/2); minimum−3','No extrema'),c('Relative-domain boundary extrema','Local minima: (0,0), value0; (3π/2,0),(0,3π/2), value−2. Local maxima: (2π,2π), value0; (π/2,2π),(2π,π/2), value2','Only the origin is a boundary extremum','All boundary points are extrema'),limited=True,why='Solve cos x+cos(x+y)=cos y+cos(x+y)=0 for interior critical points; boundary-only local behavior is distinguished from smooth critical-point classification.')
row(26,c('Interior maximum','(π/6,π/6), value3/2','(π/4,π/4), value2','Origin, value2'),c('Interior saddle/minimum','None','Origin is an interior saddle','(π/6,π/6) is a minimum'),c('Full-square absolute minimum','1 at(0,0)','√2 at(π/4,π/4)','0'),c('Other relative-domain local minimum','√2 at(π/4,π/4), one-sided within the square','No other local minimum','0 at(π/6,π/6)'),limited=True)
# Numerical critical points, independently checked by gradient residual and Hessian.
from scipy.optimize import root
import numpy as np
numeric={27:x**4+y**4-4*x*x*y+2*y,28:y**6-2*y**4+x*x-y*y+y,29:x**4+y**3-3*x*x+y*y+x-2*y+1,30:20*s.exp(-x*x-y*y)*s.sin(3*x)*s.cos(3*y)}
numaudit={}
for k,ex in numeric.items():
 g=s.lambdify((x,y),[s.diff(ex,x),s.diff(ex,y)],'numpy');H=s.lambdify((x,y),s.hessian(ex,[x,y]),'numpy');fun=s.lambdify((x,y),ex,'numpy');pts=[]
 for xx in np.linspace(-2 if k!=30 else -1,2 if k!=30 else 1,11):
  for yy in np.linspace(-2 if k!=30 else -1,2 if k!=30 else 1,11):
   res=root(lambda v:g(*v),[xx,yy])
   if not res.success or np.linalg.norm(g(*res.x))>1e-7 or (k==30 and max(abs(res.x))>1):continue
   if not any(np.linalg.norm(res.x-pt)<1e-5 for pt in pts):pts.append(res.x)
 pts.sort(key=lambda pt:(round(pt[0],5),round(pt[1],5)));fs=[];info=[]
 for i,pt in enumerate(pts):
  eig=np.linalg.eigvalsh(H(*pt));typ='Local minimum' if min(eig)>0 else 'Local maximum' if max(eig)<0 else 'Saddle';val=float(fun(*pt));info.append(dict(point=pt.tolist(),value=val,type=typ,residual=float(np.linalg.norm(g(*pt)))))
  fs.extend([n(f'Critical point{i+1} · x',pt[0],tol=.001),n(f'Critical point{i+1} · y',pt[1],tol=.001),c(f'Classification{i+1}',typ,*[q for q in ['Local minimum','Local maximum','Saddle'] if q!=typ]),n(f'Value{i+1}',val,tol=.002)])
 if k in [27,28]:fs.append(n('Absolute minimum value',min(p['value'] for p in info),tol=.002));fs.append(c('Absolute maximum','None; unbounded above','Finite at origin','Equals0'))
 if k==29:fs.append(c('Absolute extrema','Neither: cubic dependence on y is unbounded both ways','Both exist','An absolute minimum only'))
 if k==30:fs.extend([n('Highest graph value on square',max(p['value'] for p in info),tol=.002),n('Lowest graph value on square',min(p['value'] for p in info),tol=.002)])
 row(k,*fs,limited=True,why='Numerically solve both partial equations, classify with Hessian eigenvalues, and evaluate the function. Report critical points in increasing x, then increasing y order.');numaudit[k]=info
for k,lo,hi in [(31,-1,4),(32,0,4),(33,4,7),(34,-12,19),(35,-2,7),(36,0,2),(37,-2,2),(38,-18,18)]:row(k,n('Absolute minimum',lo),n('Absolute maximum',hi),why='Compare all interior stationary points, edge stationary points and vertices; for curved boundaries substitute the boundary constraint and include endpoints.')
row(39,c('Critical points and type','(1,2) and(−1,0), both absolute maxima0; no local minima','(±1,0), both minima','Origin is the only critical point'),limited=True,why='The function is minus two squares; solve gradient equations. At x=0 the x derivative is−2, so no extra critical point.')
row(40,c('Unique critical point','(1,0), local maximum1','(0,0), local maximum0','(−1,0), minimum−1'),c('Global behavior','Not absolute: f(x,0)=3x−x³−1→∞ as x→−∞','Absolute maximum1','Bounded above by0'),limited=True)
row(41,n('Shortest distance',2/s.sqrt(3)),why='Distance to x+y+z=1 is|2+0−3−1|/√3.')
row(42,*[n('Closest point · '+ax,v) for ax,v in zip('xyz',[R(5,14),R(2,7),R(29,14)])],why='Project(0,1,1) along normal(1,−2,3) by parameter5/14.')
row(43,c('Closest cone points','(2,1,√5) and(2,1,−√5)','(4,2,±√20)','(0,0,0)'),why='Minimize radial distance to the target in its meridian plane; the optimal cone radius is√5.')
row(44,c('Closest surface points','(0,3,0) and(0,−3,0)','(3,0,3) and(−3,0,−3)','(0,0,0)'),why='x²+z²≥2|xz|=2|y²−9| gives total squared distance at least9, attained at these two points.')
row(45,c('Three numbers','100/3,100/3,100/3','25,25,50','1,1,98'),n('Maximum product',(R(100,3))**3))
row(46,c('Three numbers','4,4,4','2,4,6','1,1,10'),n('Minimum sum of squares',48))
row(47,c('Maximum volume','8r³/(3√3)','8r³','4πr³/3'),why='The optimal inscribed box is a cube with each side2r/√3.')
row(48,n('Length',10,'cm'),n('Width',10,'cm'),n('Height',10,'cm'),why='A fixed-volume rectangular box has least surface area when all three dimensions are equal.')
row(49,n('Largest volume',R(4,3)),c('Dimensions','x=2,y=1,z=2/3','x=1,y=1,z=1','x=6,y=0,z=0'))
row(50,c('Dimensions','All three sides=4√6/3 cm','All three sides=8/3 cm','Sides4,4,4 cm'))
row(51,c('Dimensions','All three sides=c/12','All three sides=c/3','c/4,c/8,c/8'))
row(52,c('Least-cost dimensions','Square base side(2V/5)^(1/3), height(25V/4)^(1/3)','Cube side V^(1/3)','Square base side(5V/2)^(1/3), height(4V/25)^(1/3)'),why='Open aquarium cost∝5xy+2h(x+y), xyz=V. Symmetry yields x=y and h=5x/2.')
row(53,n('Base length',40,'cm'),n('Base width',40,'cm'),n('Height',20,'cm'),why='Open-box area xy+2h(x+y), xyz=32000, is minimized with x=y=2h.')
row(54,c('a · Domain','x≥30,y≥30,xy≤1000 (x east-west, y north-south)','x≥30,y≥30,xy≥1000','All positive x,y'),n('b · East-west length',30,'m'),n('b · North-south length',30,'m'),n('b · Height',R(40,9),'m'),c('c · Without wall-length restriction','Yes: x≈25.544m,y≈20.435m,h≈7.664m give smaller heat loss','No:30m square is unconstrained optimum','No finite minimum exists'),limited=True,why='Heat loss=80000/x+64000/y+6xy. On the constrained domain it increases from x=y=30; unconstrained stationary ratio x/y=5/4.')
row(55,c('Maximum volume','L³/(3√3)','L³','L³/27'),why='The largest box for a fixed diagonal is a cube with side L/√3.')
row(56,n('Nitrogen level',1),n('Phosphorus level',1),why='For nonnegative inputs, maximize N e^−N and P e^−P separately.')
row(57,c('a · Entropy function','−p₁ln p₁−p₂ln p₂−(1−p₁−p₂)ln(1−p₁−p₂)','−p₁ln p₁−p₂ln p₂','ln(p₁p₂)'),c('b · Domain','p₁>0,p₂>0,p₁+p₂<1; extends continuously to boundary with0ln0=0','All real pairs','p₁+p₂>1'),n('c · Maximum entropy',s.log(3)),c('Maximizing proportions','p₁=p₂=p₃=1/3','p₁=1,p₂=p₃=0','p₁=p₂=1/2,p₃=0'))
row(58,n('Maximum heterozygote proportion',R(2,3)),c('Equality','p=q=r=1/3','p=1,q=r=0','p=q=1/2,r=0'),limited=True,why='P=1−(p²+q²+r²)≤1−1/3 by Cauchy–Schwarz.')
row(59,c('Normal equations','mΣxᵢ+nb=Σyᵢ; mΣxᵢ²+bΣxᵢ=Σxᵢyᵢ','mΣxᵢ+nb=0; mΣxᵢ²+bΣxᵢ=0','m=Σyᵢ/Σxᵢ, b=0 always'),limited=True,why='Differentiate Σ[yᵢ−(mxᵢ+b)]² with respect to m,b; the quadratic is convex, and unique if x data are not all equal.')
row(60,c('Minimum-volume plane','x/3+y/6+z/9=1','x+y+z=6','x/1+y/2+z/3=1'),n('Minimum first-octant volume',27),why='Intercepts a,b,c satisfy1/a+2/b+3/c=1; AM–GM or multipliers give a3,b6,c9.')
save_section('section07')
(ROOT/'scripts/calculus-answer-checks/chapter-14/section07-calculation-audit.json').write_text(json.dumps({'exactCriticalPoints':poly_audit,'numericalCriticalPoints':numaudit},indent=2)+'\n')
