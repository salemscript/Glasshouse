from common import *
DRAIN='-project-applied-project-how-fast-does-a-tank-drain-1'
BALL='-project-applied-project-which-is-faster-going-up-or-coming-down-2'
row(3,1,c('(a) height equation in ft and seconds','h′=−√h/72'),c('(b) full-tank solution','h(t)=(√6−t/144)² for0≤t≤144√6; h=0 afterward'),n('(c) emptying time',144*s.sqrt(6),'s',.005),why='The hole radius is1/12ft, areaπ/144; tank cross-section4π. Torricelli flow is−(π/144)√(64h), givingh′=−√h/72. Stop the squared formula when√h reaches0; do not extend it into a refilling branch.',limited=True,suffix=DRAIN)
kval=(s.sqrt(3)-s.sqrt(10))/34
row(3,2,n('(a) fitted k',kval,'√cm/s',.000005),c('(a) fitted height','h(t)=[√10−(√10−√3)t/68]² until empty, then0'),*[n('(a) h('+str(tv)+')',(s.sqrt(10)+(s.sqrt(3)-s.sqrt(10))*tv/68)**2,'cm',.005) for tv in [10,20,30,40,50,60]],c('(b) comparison requirement','Collect actual heights, then compare measured-minus-predicted residuals; no measured values are supplied','The model guarantees exact experimental agreement','Invent measured heights equal to predictions'),why='Integrateh′=k√h to√h=√10+kt/2, and useh(68)=3 to fit negativek. The physical demonstration cannot be graded without the student’s observations.',limited=True,suffix=DRAIN)
H=(s.sqrt(R(2160,1)/R(125,2))+R(600,2304))**2
row(3,3,c('Height equation','h′=−√h/1152, with h in ft andt in seconds'),n('Minimum initial tank height',H,'ft',.005),why='Outlet diameter2.5in gives radius5/48ft. Tank area100πft²; Torricelli gives√h(t)=√H−t/2304. Requireh(600)≥2160/62.5=34.56ft and choose equality for the minimum.',suffix=DRAIN)
Tdrain=10000/s.sqrt(20)*(R(8,3)*2**R(3,2)-R(2,5)*2**R(5,2))
row(3,4,c('(a) differential equation','(4h−h²)h′=−0.0001√(20h)'),n('(b) complete draining time',Tdrain,'s',.05),why='Horizontal sections of the radius2m sphere have areaπ(4h−h²). Half full meansh(0)=2m. Divide volume outflow through areaπ(0.01)² by this section, and integrate dt=(4h−h²)dh/[0.0001√(20h)] from0 to2.',limited=True,suffix=DRAIN)
row(3,1,c('Velocity','v(t)=(v₀+mg/p)e^(−pt/m)−mg/p'),c('Initial check','v(0)=v₀'),why='DivideNewton’s equation bym. The deviationv+mg/p decays at ratep/m, and the initial condition fixes its coefficient.',limited=True,suffix=BALL)
row(3,2,c('Height above launch point','y(t)=(v₀+mg/p)(m/p)(1−e^(−pt/m))−mgt/p'),n('Initial height',0),why='Integrate velocity from0 to t and use ground-level launchy(0)=0. The formula applies until the return to ground.',limited=True,suffix=BALL)
t1=10*s.log(1+R(20,98));height=lambda tt:mp.mpf(118)*10*(1-mp.exp(-tt/10))-98*tt;t2=mp.findroot(height,(3,5))
row(3,3,c('General ascent time','t₁=(m/p)ln(1+pv₀/(mg))'),n('Ascent time, m=1kg,v₀=20m/s,p=0.1kg/s,g=9.8m/s²',t1,'s',.005),why='At maximum heightv=0. Solve the exponential equation; the numerical check explicitly usesg=9.8m/s².',limited=True,suffix=BALL)
row(3,4,n('Return time t₂, same parameters',t2,'s',.02),n('Descent duration t₂−t₁',t2-mp.mpf(str(s.N(t1,50))),'s',.02),c('Faster phase','Ascent','Descent','Equal duration'),why='Find the nonzero positive root of1180(1−e^(−t/10))−98t=0. Compare the return-minus-ascent time with the ascent duration.',limited=True,suffix=BALL)
row(3,5,c('Height at twice the ascent time','y(2t₁)=(m²g/p²)[x−1/x−2lnx], x=e^(pt₁/m)>1'),c('Derivative of f(x)=x−1/x−2lnx','f′(x)=(x−1)²/x²>0 forx>1'),c('Sign ofy(2t₁)','Positive','Zero','Negative'),c('Conclusion','t₂>2t₁, so descent takes longer than ascent','t₂<2t₁, so ascent takes longer','The durations are always equal'),why='f(1)=0 andf′>0 onx>1 implyf(x)>0. Thus the ball is still above ground after twice the ascent time.',limited=True,suffix=BALL)
check('Tank1 Torricelli coefficient',(pi/R(144))/(4*pi)*8-R(1,72))
check('Tank2 observed terminal depth',(s.sqrt(10)+kval*68/2)**2-3)
check('Tank3 outlet coefficient',(pi*(R(5,48))**2)/(100*pi)*8-R(1,1152))
check('Tank3 pressure at600',R(125,2)*(s.sqrt(H)-R(600,2304))**2-2160)
near('Tank4 independent quadrature',mp.quad(lambda hh:(4*hh-hh*hh)/(mp.mpf('.0001')*mp.sqrt(20*hh)),[0,1,2]),Tdrain)
m,p,g,v0=s.symbols('m p g v0',positive=True);v=(v0+m*g/p)*s.exp(-p*t/m)-m*g/p;yy=(v0+m*g/p)*m/p*(1-s.exp(-p*t/m))-m*g*t/p
check('Ball velocity DE',m*s.diff(v,t)+p*v+m*g);check('Ball initial velocity',v.subs(t,0)-v0);check('Ball height derivative',s.diff(yy,t)-v);check('Ball height initial',yy.subs(t,0));check('Ball ascent zero',v.subs(t,m/p*s.log(1+p*v0/(m*g))))
near('Ball nonzero root',height(t2),0,1e-12);check('Ball comparison derivative',s.diff(x-1/x-2*s.log(x),x)-(x-1)**2/x**2)
finish('section03-projects',[608,609,610])
