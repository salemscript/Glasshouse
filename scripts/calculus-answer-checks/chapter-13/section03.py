from common import *
def plane(label,e):return c(label,fmt(e),fmt(e+1),fmt(e-1))
row=lambda k,*fs,**kw:A.row(3,k,*fs,**kw)
CASES=[]
def curvature(r):
 d=r.diff(t);dd=d.diff(t);return s.simplify(norm(d.cross(dd))/norm(d)**3)
def frame(r):
 d=r.diff(t);T=unit(d);N=unit(T.diff(t));return T,N,s.simplify(T.cross(N))
def record(k,r,kind,**kw):CASES.append(dict(n=k,kind=kind,r=list(map(str,r)),**kw))
curves={1:([t,3*s.cos(t),3*s.sin(t)],-5,5),2:([2*t,t*t,t**3/3],0,1),3:([s.sqrt(2)*t,s.exp(t),s.exp(-t)],0,1),4:([s.cos(t),s.sin(t),s.log(s.cos(t))],0,pi/4),5:([1,t*t,t**3],0,1),6:([t*t,9*t,4*t**R(3,2)],1,4),7:([t*t,t**3,t**4],0,2),8:([t,s.exp(-t),t*s.exp(-t)],1,3),9:([s.cos(pi*t),2*t,s.sin(2*pi*t)],0,2),10:([s.sin(t),s.sin(2*t),s.sin(3*t)],0,2*pi),11:([t,t*t/2,t**3/6],0,6),12:([s.cos(t),2*s.sin(t),2-s.cos(t)-2*s.sin(t)],0,2*pi)}
exact={1:10*s.sqrt(10),2:R(7,3),3:s.E-1/s.E,4:s.log(1+s.sqrt(2)),5:(13*s.sqrt(13)-8)/27,6:42,11:42}
for k,(r0,lo,hi) in curves.items():
 r=vec(r0);speed=norm(r.diff(t));fn=s.lambdify(t,speed,'mpmath');points=[mp.mpf(str(s.N(lo,35)))+(mp.mpf(str(s.N(hi,35)))-mp.mpf(str(s.N(lo,35))))*j/32 for j in range(33)];val=exact.get(k)
 if val is None:val=mp.quad(fn,points)
 row(k,n('Arc length',val,tol=.000051 if k in [7,8,9,10,12] else None),limited=k==10,why='Integrate |r′(t)| over the specified interval; a closed curve is traced once over its full period.');record(k,r,'length',lo=str(lo),hi=str(hi),expected=str(val))
ss=s.symbols('s',real=True)
r=vec([5-t,4*t-3,3*t]);re=r.subs(t,1+ss/s.sqrt(26));row(13,f('a · Arc length s(t)',s.sqrt(26)*(t-1)),*V(re,'a · r(s)'),*V(re.subs(ss,4),'b · Point4 units along'),why='Speed is sqrt26; starting point has t=1.')
r=vec([s.exp(t)*s.sin(t),s.exp(t)*s.cos(t),s.sqrt(2)*s.exp(t)]);re=r.subs(t,s.log(1+ss/2));row(14,f('a · Arc length s(t)',2*(s.exp(t)-1)),*V(re,'a · r(s)'),*V(re.subs(ss,4),'b · Point4 units along'),why='Speed=2e^t; the start is t=0. For forward physical arc length use s≥0.')
row(15,*V([3*s.sin(1),4,3*s.cos(1)],'Position after5 units'),why='Constant speed5 gives parameter increment1 from t=0.')
row(16,c('Arc-length parametrization','r(s)=⟨cos s,sin s⟩, s=2arctan t','r(s)=⟨sin s,cos s⟩','r(s)=⟨cos2s,sin2s⟩'),c('Curve and range','Unit circle missing(−1,0) for finite t; signed s∈(−π,π), forward from start0≤s<π','A circle of radius2','All real s correspond to finite original t'),why='Speed2/(1+t²); invert using the tangent-half-angle identities.')
for k,r0 in {17:[t,3*s.cos(t),3*s.sin(t)],18:[t*t,s.sin(t)-t*s.cos(t),s.cos(t)+t*s.sin(t)],19:[s.sqrt(2)*t,s.exp(t),s.exp(-t)],20:[t,t*t/2,t*t]}.items():
 r=vec(r0);T,N,B=frame(r)
 if k==18:T=vec([2,s.sin(t),s.cos(t)])/s.sqrt(5);N=vec([0,s.cos(t),-s.sin(t)]);kap=1/(5*t)
 else:kap=curvature(r)
 row(k,*V(T,'a · Unit tangent T'),*V(N,'a · Principal normal N'),f('b · Curvature',kap),why='Normalize r′, then normalize T′; curvature is |T′|/|r′|. Exercise18 assumes t>0.');record(k,r,'frame',T=list(map(str,T)),N=list(map(str,N)),kappa=str(kap))
for k,r0 in {21:[0,t**3,t*t],22:[t,t*t,s.exp(t)],23:[s.sqrt(6)*t*t,2*t,2*t**3]}.items():
 r=vec(r0);kap=curvature(r);row(k,f('Curvature',kap),why='Use |r′×r″|/|r′|³ at regular parameter values; #21 excludes t=0, where r′=0.');record(k,r,'curvature',kappa=str(kap))
for k,r0,t0 in [(24,[t*t,s.log(t),t*s.log(t)],1),(25,[t,t*t,t**3],1),(26,[s.cos(t),s.sin(t),s.sin(5*t)],0)]:
 r=vec(r0);kap=curvature(r).subs(t,t0);row(k,n('Curvature at the specified point',kap),limited=k==26,why='Find the source parameter for the point before evaluating |r′×r″|/|r′|³.');record(k,r,'curvature-point',at=str(t0),expected=str(kap))
for k,y in {27:x**4,28:s.tan(x),29:x*s.exp(x),34:x**4-2*x*x,35:x**-2}.items():
 kap=s.simplify(s.Abs(s.diff(y,x,2))/(1+s.diff(y,x)**2)**R(3,2));fs=[f('Curvature κ(x)',kap)]
 if k==34:fs.append(c('Graph interpretation','Curvature vanishes at x=±1/√3 and peaks where turning is tight, including stationary-point neighborhoods','Curvature has the same sign as y″','Curvature vanishes at every stationary point'))
 if k==35:fs.append(c('Graph interpretation','Curvature tends to0 both near the excluded x=0 and as|x|→∞; symmetric peaks lie between','Curvature diverges at x=0','Curvature is negative for x<0'))
 row(k,*fs,limited=k>=34,why='For a graph y=f(x), κ=|f″|/(1+f′²)^(3/2). A steep slope alone does not imply high curvature.')
row(30,n('Max-curvature point · x',1/s.sqrt(2)),n('Max-curvature point · y',-s.log(2)/2),n('Limit of curvature as x→∞',0),why='For ln x, κ=x/(1+x²)^(3/2), x>0; derivative changes sign at1/√2.')
row(31,n('Max-curvature point · x',-s.log(2)/2),n('Max-curvature point · y',1/s.sqrt(2)),n('Limit of curvature as x→∞',0),why='For e^x, κ=e^x/(1+e^(2x))^(3/2); maximize in u=e^x>0.')
row(32,c('One valid parabola','y=2x² (also y=−2x² works)','y=x²','y=4x²'),why='At the origin of y=ax², κ=2|a|. This checks a valid construction, not uniqueness.')
row(33,c('a · Greater curvature','P','Q','Equal'),n('b · Approximate curvature at P',1.1,tol=.5),n('b · Approximate curvature at Q',.45,tol=.22),limited=True,why='The source is a qualitative sketch. Use osculating radii roughly1 unit at P and2–3 units at Q; numerical ranges are deliberately approximate, not exact measurements.')
for k,r0 in {36:[t-s.sin(t),1-s.cos(t),4*s.cos(t/2)],37:[t*s.exp(t),s.exp(-t),s.sqrt(2)*t]}.items():
 r=vec(r0);kap=curvature(r);row(k,f('Curvature κ(t)',kap),c('Graph interpretation','Sharper bending corresponds to larger nonnegative κ; only regular points admit this formula','Curvature is a signed height','A constant z-coordinate is required'),limited=True,why='#36 is not regular at t=0,2π,4π,6π,8π; curvature is undefined there. Plot on the regular intervals and do not fill singular values with zero.');record(k,r,'curvature',kappa=str(kap))
row(38,c('Graph identification','a is curvature; b is f','b is curvature; a is f','Both are f'),limited=True,why='The two inflection points of the bell-shaped b correspond to zeros of a; curvature is nonnegative.')
row(39,c('Graph identification','b is curvature; a is f','a is curvature; b is f','Both are curvature'),limited=True,why='The steep flank of a lowers curvature; its rounded top gives the sharp peak of b.')
r=vec([s.sin(3*t),s.sin(2*t),s.sin(3*t)]);kap=curvature(r)
row(40,n('a · Number of distinct curvature-maximum points',6,tol=0),f('b · Curvature function',kap),c('b · Peak types','Four global maxima≈14.1896 and two other local maxima≈3.18198 in one period','Six identical global maxima','Only one maximum'),limited=True,why='Over0≤t<2π, numerical extrema occur near0.543786,π/2,2.597806,3.685379,3π/2,5.739399; these give six distinct spatial points.');record(40,r,'curvature',kappa=str(kap))
r=vec([t-R(3,2)*s.sin(t),1-R(3,2)*s.cos(t),t]);kap=curvature(r)
row(41,f('Curvature function',kap),c('Maximum parameters','t=2πk, k any integer','t=(2k+1)π','t=π/2+2πk'),n('Maximum curvature',R(6,5)),limited=True,why='Writing c=cos t gives κ=(3/2)sqrt(1+(c−3/2)²)/(17/4−3c)^(3/2), maximized at c=1.');record(41,r,'curvature',kappa=str(kap))
row(42,c('Plane-curve curvature','|x′y″−y′x″|/(x′²+y′²)^(3/2)','(x′y″−y′x″)/(x′²+y′²)','|x″y″|'),limited=True,why='Embed the curve in z=0, compute the cross product, and use its nonnegative magnitude.')
a,b,w=s.symbols('a b omega',positive=True)
for k,r0 in {43:[t*t,t**3,0],44:[a*s.cos(w*t),b*s.sin(w*t),0],45:[s.exp(t)*s.cos(t),s.exp(t)*s.sin(t),0]}.items():
 r=vec(r0);kap=curvature(r);row(k,f('Curvature',kap),why='Use the planar cross-product formula. In #44 take a,b>0 and ω≠0; curvature is independent of traversal speed |ω|.');record(k,r,'curvature',kappa=str(kap))
row(46,c('Maximizing members','c=±√2','c=0','c=±1'),n('Largest κ(0)',2/(3*s.sqrt(3))),why='κ(0)=c²/(1+c²)^(3/2); optimize over c²≥0.')
for k,r0,t0 in [(47,[t*t,R(2,3)*t**3,t],1),(48,[s.cos(t),s.sin(t),s.log(s.cos(t))],0)]:
 r=vec(r0);T,N,B=frame(r);row(k,*V(T.subs(t,t0),'T'),*V(N.subs(t,t0),'N'),*V(B.subs(t,t0),'B'),why='T follows increasing t; N points toward bending; B=T×N.');record(k,r,'frame-point',at=str(t0),T=list(map(str,T.subs(t,t0))),N=list(map(str,N.subs(t,t0))),B=list(map(str,B.subs(t,t0))))
X,Y,Z=s.symbols('x y z',real=True)
for k,r0,t0 in [(49,[s.sin(2*t),-s.cos(2*t),4*t],pi/2),(50,[s.log(t),2*t,t*t],1),(55,[t*t,t,t**4],1)]:
 r=vec(r0);p=r.subs(t,t0);v=r.diff(t).subs(t,t0);bn=r.diff(t).cross(r.diff(t,2)).subs(t,t0);dr=vec([X,Y,Z])-p
 row(k,plane('Normal plane: expression=0',s.expand(v.dot(dr))),plane('Osculating plane: expression=0',s.expand(bn.dot(dr))),why='Normal plane normal is r′; osculating plane normal is r′×r″. Nonzero scalar multiples represent the same plane.');record(k,r,'planes',at=str(t0),normal=list(map(str,v)),binormal=list(map(str,bn)))
row(51,c('At(2,0)','(x+5/2)²+y²=81/4','(x−2)²+y²=1','x²+(y−3)²=4'),c('At(0,3)','x²+(y−5/3)²=16/9','x²+(y+5/3)²=16/9','x²+y²=9'),limited=True,why='Ellipse semiaxes2 and3 give curvature radii9/2 and4/3; centers lie inward along the principal normal.')
row(52,c('At(0,0)','x²+(y−1)²=1','x²+(y+1)²=1','x²+y²=1'),c('At(1,1/2)','(x+1)²+(y−5/2)²=8','(x−1)²+(y−1/2)²=8','(x+1)²+(y−5/2)²=4'),limited=True,why='ρ=(1+x²)^(3/2); add ρ times the upward principal normal to each point.')
row(53,*V([-1,-3,1],'Point'),why='Parallelism of(3t²,3,4t³) and(6,6,−8) forces t=−1.')
row(54,c('Existence','No regular osculating plane has that parallelism','Yes, at t=0','Yes, at t=1'),why='r′×r″=(36t²,−12t⁴,−18t). Equal first and second components force t=0, where this cross product vanishes and the osculating plane is undefined.')
row(56,c('Common osculating plane','x+y=3','x−y=3','z=0'),c('Conclusion','The curve is planar','The curve is a straight line','The curve is a circular helix'),limited=True)
row(57,n('T angle with +z-axis',s.acos(1/s.sqrt(3))*180/pi,unit='degrees'),n('N angle with +z-axis',90,unit='degrees'),n('B angle with +z-axis',s.acos(s.sqrt(R(2,3)))*180/pi,unit='degrees'),limited=True,why='The z-components of the three unit vectors are1/√3,0,√(2/3), independently of t.')
r=vec([s.sin(t),s.cos(t),s.tan(t)]);p=r.subs(t,pi/4);v=r.diff(t).subs(t,pi/4);acc=r.diff(t,2).subs(t,pi/4);nn=s.simplify(acc-acc.dot(v)/v.dot(v)*v)
row(58,plane('Rectifying plane: expression=0',s.expand(nn.dot(vec([X,Y,Z])-p))),why='The plane spanned by T and B has normal N; the nonzero normal component of acceleration is parallel to N.')
row(59,c('Identity','dT/ds=κN','dT/ds=κT','dT/ds=−κN'),limited=True,why='T′=|T′|N and ds/dt=|r′|>0.')
row(60,c('Identity','κ=|dφ/ds|','κ=dφ/ds without absolute value','κ=|φ|'),limited=True,why='Differentiate T=(cosφ,sinφ); its derivative magnitude is |dφ/ds|.')
row(61,c('a · Orthogonality to B','Differentiate B·B=1 to obtain B·B_s=0','B_s=B','B_s·B=1'),c('b · Orthogonality to T','Differentiate B·T=0 and use T_s=κN to obtain B_s·T=0','B_s=T','B_s·T=κ'),c('c · Torsion definition','B_s=−τN','B_s=τT','B_s=τB'),n('d · Planar-curve torsion',0),limited=True,why='At regular points with nonzero curvature, T,N,B form an orthonormal basis; a planar curve has constant binormal.')
row(62,c('Frenet–Serret normal derivative','N_s=−κT+τB','N_s=κT+τB','N_s=−κT−τB'),limited=True,why='Differentiate N=B×T and use B_s=−τN, T_s=κN and the orientation of the frame.')
row(63,c('a · r″','s″T+κ(s′)²N','s″T−κ(s′)²N','κN'),c('b · r′×r″','κ(s′)³B','κ(s′)²B','−κ(s′)³B'),c('c · r‴','[s‴−κ²(s′)³]T+[3κs′s″+κ′(s′)²]N+κτ(s′)³B','s‴T only','κτ(s′)²B only'),c('d · Torsion','((r′×r″)·r‴)/|r′×r″|²','|r′×r″|/|r′|³','((r′×r″)·r‴)/|r′|²'),limited=True,why='Differentiate r′=s′T and use the frame derivatives; the triple product isolates the binormal coefficient.')
row(64,f('Curvature',a/(a*a+b*b)),f('Torsion',b/(a*a+b*b)),limited=True,why='For(a cos t,a sin t,bt), speed²=a²+b² and the cross-product/triple-product ratios are constant.')
r=vec([t,t*t/2,t**3/3]);d=r.diff(t);cr=d.cross(d.diff(t));tau=s.simplify(cr.dot(d.diff(t,2))/cr.dot(cr));row(65,f('Torsion',tau));record(65,r,'torsion',expected=str(tau))
r=vec([s.sinh(t),s.cosh(t),t]);d=r.diff(t);cr=d.cross(d.diff(t));tau=s.simplify(cr.dot(d.diff(t,2))/cr.dot(cr));row(66,n('Curvature',curvature(r).subs(t,0)),n('Torsion',tau.subs(t,0)));record(66,r,'torsion-point',at='0',expected=str(tau.subs(t,0)))
row(67,n('Length of each helix',R(29,10)*s.sqrt((20*pi)**2+34**2),unit='cm',tol=.51),why='Length per turn is sqrt((2π·10)²+34²) Å; multiply by2.9×10^8 turns and10^−8 cm/Å.')
row(68,f('a · Transition polynomial P(x)',6*x**5-15*x**4+10*x**3),c('b · Shape','Monotonically rises from0 to1 with zero slope and curvature at both joins; horizontal outside[0,1]','A straight segment with corners at both joins','An oscillation below0 and above1'),limited=True,why='Impose P(0)=P′(0)=P″(0)=0, P(1)=1 andP′(1)=P″(1)=0.')
from pathlib import Path
HERE=Path(__file__).parent
(HERE/'section03.json').write_text(json.dumps(A.out,ensure_ascii=False,indent=2)+'\n');(HERE/'section03-audit.json').write_text(json.dumps(dict(notes=A.notes,cases=CASES),ensure_ascii=False,indent=2)+'\n');print('13.3',len(A.out))
