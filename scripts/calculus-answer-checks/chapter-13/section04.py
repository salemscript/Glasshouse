from common import *
row=lambda k,*fs,**kw:A.row(4,k,*fs,**kw)
CASES=[]
pts={0:vec([R(27,10),R(98,10),R(37,10)]),R(1,2):vec([R(35,10),R(72,10),R(33,10)]),1:vec([R(45,10),6,3]),R(3,2):vec([R(59,10),R(64,10),R(28,10)]),2:vec([R(73,10),R(78,10),R(27,10)])}
fs=[]
for lo,hi in [(0,1),(R(1,2),1),(1,2),(1,R(3,2))]:fs+=V((pts[hi]-pts[lo])/(hi-lo),f'a · Average velocity [{lo},{hi}]')
v=pts[R(3,2)]-pts[R(1,2)];row(1,*fs,*V(v,'b · Centered velocity estimate'),n('b · Estimated speed',norm(v),tol=.01),why='Use displacement divided by elapsed time; center the difference at t=1 for the estimate.')
row(2,c('a · Average velocity','[r(2.4)−r(2)]/0.4','r(2.4)−r(2)','r(2.4)/2.4'),c('b · Average velocity','[r(2)−r(1.5)]/0.5','r(2)−r(1.5)','r(2)/2'),c('c · Instantaneous velocity','lim h→0 [r(2+h)−r(2)]/h','r(2)/2','lim h→0 r(2+h)/h'),c('d · Direction','Tangent pointing up and left','Tangent pointing down and right','Radially from the origin'),n('d · Approximate speed',3.2,tol=.7),limited=True,why='From the printed axes the nearby displacement estimates have speeds around3 units/time; the smooth tangent at r(2) points up-left. The sketch cannot supply an exact derivative.')
curves={3:[-t*t/2,t],4:[t*t,t**-2],5:[3*s.cos(t),2*s.sin(t)],6:[s.exp(t),s.exp(2*t)],7:[t,t*t,2],8:[t,2*s.cos(t),s.sin(t)],9:[t*t+t,t*t-t,t**3],10:[2*s.cos(t),3*t,2*s.sin(t)],11:[s.sqrt(2)*t,s.exp(t),s.exp(-t)],12:[t*t,2*t,s.log(t)],13:[s.exp(t)*s.cos(t),s.exp(t)*s.sin(t),t*s.exp(t)],14:[t*t,s.sin(t)-t*s.cos(t),s.cos(t)+t*s.sin(t)]}
at={3:2,4:1,5:pi/3,6:0,7:1,8:0}
for k,r0 in curves.items():
 r=vec(r0);v=r.diff(t);acc=v.diff(t);fs=V(v,'Velocity')+V(acc,'Acceleration')+[f('Speed',norm(v))]
 if k in at:fs+=V(r.subs(t,at[k]),'Position at specified t')+V(v.subs(t,at[k]),'Velocity at specified t')+V(acc.subs(t,at[k]),'Acceleration at specified t')
 row(k,*fs,limited=k in at,why='Differentiate position componentwise; speed is the nonnegative magnitude of velocity. The graph/vector drawing itself requires visual review.');CASES.append(dict(n=k,r=list(map(str,r)),v=list(map(str,v)),a=list(map(str,acc)),speed=str(norm(v))))
for k,acc0,v0,r0 in [(15,[2,0,2*t],[3,-1,0],[0,1,1]),(16,[s.sin(t),2*s.cos(t),6*t],[0,0,1],[0,1,-4]),(17,[2*t,s.sin(t),s.cos(2*t)],[1,0,0],[0,1,0]),(18,[t,s.exp(t),s.exp(-t)],[0,0,1],[0,1,1])]:
 acc=vec(acc0);v=acc.applyfunc(lambda z:s.integrate(z,t));v+=vec(v0)-v.subs(t,0);r=v.applyfunc(lambda z:s.integrate(z,t));r+=vec(r0)-r.subs(t,0)
 row(k,*(V(v,'Velocity') if k<17 else []),*V(r,'Position'),limited=k>=17,why='Integrate acceleration, impose v(0), integrate again, then impose r(0).');CASES.append(dict(n=k,r=list(map(str,r)),a=list(map(str,acc)),v0=v0,r0=r0))
row(19,n('Time of minimum speed',4),why='Speed squared=8(t−4)²+153; its global minimum occurs at t=4.')
m=s.symbols('m',positive=True);row(20,*V(m*vec([6*t,2,6*t]),'Required force'),why='Newton’s law gives F=m r″ for constant mass m.')
row(21,*V([t,-t,R(5,2)*t*t],'Position, meters'),f('Speed, m/s',s.sqrt(2+25*t*t)),why='The stated applied net force is(0,0,20)N and mass4kg, so acceleration is(0,0,5)m/s²; integrate with the initial data.')
row(22,c('Derivative identity','0=d(v·v)/dt=2v·a','0=v+a','v=a'),c('Conclusion','v·a=0; velocity and acceleration are orthogonal','v×a=0; they must be parallel','Acceleration must vanish'),limited=True,why='Constant speed means v·v is constant, not necessarily v itself.')
g=R(49,5);vx=100;vy=100*s.sqrt(3)
row(23,n('a · Range',40000*s.sin(pi/3)/g,'m',tol=.1),n('b · Maximum height',vy*vy/(2*g),'m',tol=.1),n('c · Impact speed',200,'m/s'),why='Use g=9.8m/s², no drag, equal launch/landing heights; horizontal speed is constant.')
T=(vy+s.sqrt(vy*vy+2*g*100))/g
row(24,n('a · Range',vx*T,'m',tol=.1),n('b · Maximum height above ground',100+vy*vy/(2*g),'m',tol=.1),n('c · Impact speed',s.sqrt(40000+2*g*100),'m/s',tol=.01),why='Solve100+v_y t−gt²/2=0 for the positive flight time. Impact kinetic energy includes the initial100m elevation.')
row(25,n('Initial speed',s.sqrt(90*g),'m/s',tol=.01),why='R=v0² sin(2θ)/g and sin90°=1.')
ang=s.asin(3000*g/400**2)*90/pi
row(26,n('Lower angle',ang,'degrees',tol=.01),n('Higher angle',90-ang,'degrees',tol=.01),why='The two elevations are complementary because they have the same sin(2θ).')
row(27,n('Muzzle speed',s.sqrt(2*32*1600)/s.sin(pi/5),'ft/s',tol=.1),why='At the apex vertical speed is zero; use g=32ft/s² and sin36°.')
y=3+400*s.tan(50*pi/180)-16*(400/(115*s.cos(50*pi/180)))**2
row(28,n('Height at fence',y,'ft',tol=.1),c('Home run?','Yes, the ball clears the10-ft fence','No, it strikes below10ft','No, it has landed before400ft'),why='Substitute t=400/(115cos50°) into y=3+115sin50°t−16t².')
u=s.symbols('u');roots=s.solve(100*u-g*10000/(2*6400)*(1+u*u)-15,u);lo=float(s.atan(roots[0])*180/pi);hi=float(s.atan(roots[1])*180/pi);ar=float(s.asin(600*g/6400)*90/pi)
row(29,n('First interval lower elevation',lo,'degrees',tol=.02),n('First interval upper elevation',ar,'degrees',tol=.02),n('Second interval lower elevation',90-ar,'degrees',tol=.02),n('Second interval upper elevation',hi,'degrees',tol=.02),c('Endpoint interpretation','Use strict intervals to clear the near wall and land before the far wall','All four endpoints are guaranteed safe','Only45° works'),why='For ground impact inside the city require y(100)>15 and range<600; y(100)>15 already implies range>100. Wall-grazing/boundary endpoints are excluded.')
row(30,n('Height / maximum height at half-ascent time',R(3,4)),c('Substitution','t=v0 sinα/(2g) into y=v0 sinα t−gt²/2','t=v0 cosα/g into y','t=2v0 sinα/g'),limited=True,why='The apex time is v0 sinα/g and maximum height is(v0 sinα)²/(2g).')
row(31,*V([250,-50,0],'Landing point, ft'),n('Impact speed',s.sqrt(9300),'ft/s',tol=.01),why='Vertical motion80t−16t² gives positive landing time5s; x=50t,y=−2t².')
T=30/g;row(32,n('Eastward landing distance',R(5,2)*T*T,'m',tol=.01),n('Southward landing distance',15*s.sqrt(3)*T,'m',tol=.01),n('Impact speed',s.sqrt(900+25*T*T),'m/s',tol=.01),why='Axes east,north,up give a=(5,0,−9.8); initial velocity(0,−15√3,15). Use positive time30/9.8.')
row(33,n('a · Downstream distance',16,'m'),f('a · Path y(x), meters',3*x*x/100-x**3/2000),n('b · Heading south of east',s.asin(R(2,5))*180/pi,'degrees',tol=.01),f('b · Path y(x), meters',(R(3,20)*x*x-x**3/400-2*x)/s.sqrt(21)),c('b · Shape','Initially upstream, then downstream through the middle, then upstream again to B','Straight across from A to B','Monotonically downstream'),limited=True,why='dy/dx=(f(x)−5sinθ)/(5cosθ). Zero net drift requires5sinθ=mean(f)=2m/s. The S-shaped drift is consistent with slow banks and fast central water.')
row(34,n('Heading south of east',s.asin(6/(5*pi))*180/pi,'degrees',tol=.01),why='Mean current is(1/40)∫0^40 3sin(πx/40)dx=6/π; cancel it with the southward component of boat velocity.')
row(35,c('Path','A circle about the c-axis in the plane c·r=c·r(0); a stationary point in the degenerate case','A spiral with increasing radius','An arbitrary straight line'),c('Invariants','|r| and c·r are constant','Only |r′| grows exponentially','r is parallel to r′'),limited=True,why='r·(c×r)=0 and c·(c×r)=0; their derivatives show constant radius and axial coordinate. If c×r0=0 the point is stationary.')
row(36,c('a · Straight-line acceleration','Parallel to the fixed line, possibly zero','Always normal to the line','Always zero'),c('b · Constant-speed acceleration','Normal to velocity, possibly zero','Parallel to velocity','Nonzero in every case'),limited=True,why='On a fixed line both derivatives follow its direction; constant speed gives v·a=0.')
for k,r0 in {37:[t*t+1,t**3,0],38:[2*t*t,R(2,3)*t**3-2*t,0],39:[s.cos(t),s.sin(t),t],40:[t,2*s.exp(t),s.exp(2*t)],41:[s.log(t),t*t+3*t,4*s.sqrt(t)],42:[1/t,1/t**2,1/t**3]}.items():
 r=vec(r0);v=r.diff(t);acc=v.diff(t);aT=s.simplify(v.dot(acc)/norm(v));aN=s.simplify(norm(v.cross(acc))/norm(v));fs=[n('Tangential acceleration',aT.subs(t,1)),n('Normal acceleration',aN.subs(t,1))] if k>=41 else [f('Tangential acceleration',aT),f('Normal acceleration',aN)]
 if k==37:fs.append(c('At t=0','Velocity vanishes; Frenet components are defined only for t>0, with right-hand limits aT→2,aN→0','Both Frenet directions are uniquely defined at t=0','Normal acceleration diverges'))
 row(k,*fs,why='aT=(v·a)/|v| is signed; aN=|v×a|/|v| is nonnegative, at regular points.');CASES.append(dict(n=k,r=list(map(str,r)),aT=str(aT),aN=str(aN)))
row(43,n('Approximate tangential component',5,'cm/s²',tol=1.2),n('Approximate normal component',s.sqrt(75),'cm/s²',tol=.8),limited=True,why='The diagram suggests an angle of roughly60° between a and the forward tangent: aT≈10cos60°,aN≈10sin60°. The drawing is not an exact angle specification.')
row(44,c('Derivative','L′=m(v×v+r×a)=mr×a=τ','L′=mv×a','L′=mr×v'),c('Zero-torque consequence','Angular momentum L is constant','Velocity must be zero','Position must be constant'),limited=True,why='Use the cross-product product rule and v×v=0.')
row(45,n('Turn engines off at t',1),n('Coasting duration in the same time units',2),why='At t=1, r=(4,2,5),r′=(1,1,2). Adding2r′ gives the station(6,4,9). The tangent must meet all three station coordinates.')
row(46,c('a · Velocity','v(t)=v(0)−ln[m(0)/m(t)] v_e','v(t)=v(0)+ln[m(0)/m(t)] v_e','v(t)=v(0)−m(t)v_e'),n('b · Fraction of initial mass burned',1-s.exp(-2),tol=.00001),limited=True,why='Integrate dv=v_e dm/m for constant relative exhaust vector. A speed gain2|v_e| requires m_final/m_initial=e^−2.')
suf='-project-kepler-s-laws-applied-project-1'
row(1,c('a · Angular momentum per mass','h=r²θ′ k','h=rθ′ k','h=r²θ k'),c('b · Scalar relation','r²θ′=h','rθ′=h','r²θ=h'),c('c · Swept-area rate','A′=r²θ′/2','A′=rθ′','A′=πr²'),c('d · Constant rate','A′=h/2','A′=h','A′=2h'),suffix=suf,limited=True,why='The polar cross product gives h=r×r′; a small sector has area½r²dθ.')
row(2,c('a · Orbital period','T=2πab/h','T=πab/h','T=2πa/h'),c('b · Semilatus rectum','h²/(GM)=ed=b²/a','h²/(GM)=a²/b','h²/(GM)=ab'),c('c · Third law','T²=4π²a³/(GM)','T²=4π²a²/(GM)','T²=GM a³'),suffix=suf,limited=True,why='Areaπab divided by areal rateh/2 gives T; substitute h²=GMb²/a.')
G=6.67e-11;M=1.99e30;T=365.25*86400;major=2*(G*M*T*T/(4*math.pi**2))**(1/3)
row(3,n('Earth orbital major axis',major,'m',tol=major*.0005),suffix=suf,why='Kepler’s law solves for semimajor axis a; the requested major-axis length is2a. Convert days to seconds.')
alt=(G*5.98e24*86400**2/(4*math.pi**2))**(1/3)-6.37e6
row(4,n('Geosynchronous altitude using24h period',alt,'m',tol=150000),suffix=suf,why='Use T=24h as the exercise approximation, compute orbital radius(GMT²/4π²)^(1/3), then subtract Earth radius. Using a sidereal day differs by about77km and is accepted.')
from pathlib import Path
HERE=Path(__file__).parent
(HERE/'section04.json').write_text(json.dumps(A.out,ensure_ascii=False,indent=2)+'\n');(HERE/'section04-audit.json').write_text(json.dumps(dict(notes=A.notes,cases=CASES),ensure_ascii=False,indent=2)+'\n');print('13.4',len(A.out))
