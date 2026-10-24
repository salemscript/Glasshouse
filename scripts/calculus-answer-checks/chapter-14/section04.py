from common import *
row=lambda k,*fs,**kw:A.row(4,k,*fs,**kw)
def lin(ex,vs,pt):
 sub=dict(zip(vs,pt));return s.simplify(ex.subs(sub)+sum(s.diff(ex,vv).subs(sub)*(vv-aa) for vv,aa in zip(vs,pt)))
data={1:(2*x*x+y*y-5*y,[1,2]),2:((x+2)**2-2*(y-1)**2-5,[2,3]),3:(s.exp(x-y),[2,2]),4:(x/y**2,[-4,2]),5:(x*s.sin(x+y),[-1,1]),6:(s.log(x-2*y),[3,1]),7:(x*x+x*y+3*y*y,[1,1]),8:(s.sqrt(9+x*x*y*y),[2,2]),9:((1+s.cos(x-y)**2)/(1+s.cos(x+y)**2),[pi/3,pi/6]),10:(s.exp(-x*y/10)*(s.sqrt(x)+s.sqrt(y)+s.sqrt(x*y)),[1,1]),11:(1+x*s.log(x*y-5),[2,3]),12:(s.sqrt(x*y),[1,4]),13:(x*x*s.exp(y),[1,0]),14:((1+y)/(1+x),[1,3]),15:(4*s.atan(x*y),[1,1]),16:(y+s.sin(x/y),[0,3])}
for k,(ex,pt) in data.items():
 fs=[f('z = tangent-plane expression' if k<=10 else 'Linearization L(x,y)',lin(ex,[x,y],pt))]
 if k>=11:fs.append(c('Differentiability reason','Both first partials are continuous on a neighborhood of the point','All functions are differentiable everywhere','Continuity of f alone proves differentiability'))
 row(k,*fs,limited=k in [7,8,9,10],why='Use f(a,b)+f_x(a,b)(x−a)+f_y(a,b)(y−b); the stated point lies in the smooth real domain.')
row(17,n('f(0,0)',1),n('f_x(0,0)',1),n('f_y(0,0)',0),f('Linearization',1+x),limited=True)
row(18,n('f(0,0)',-1),n('f_x(0,0)',1),n('f_y(0,0)',1),f('Linearization',x+y-1),limited=True)
row(19,n('Estimate f(2.2,4.9)',6.3),why='6+1(0.2)−1(−0.1)=6.3.')
row(20,f('L(x,y)',x+y),n('Estimate',1.99),limited=True,why='At(1,1), f=2 and both first derivatives equal1.')
L=(3*x+2*y+6*z)/7
row(21,f('L(x,y,z)',L),n('Approximation',L.subs({x:R(302,100),y:R(197,100),z:R(599,100)})),why='The gradient of the norm at(3,2,6) is(3,2,6)/7.')
row(22,c('Linearization','L(v,t)=28+1.15(v−40)+0.45(t−20)','L(v,t)=28−1.15(v−40)+0.45(t−20)','L(v,t)=28+0.45(v−40)+1.15(t−20)'),n('Estimated height',33.25,'ft',.25),why='Use centered speed slope(40−17)/20=1.15 and average adjacent time slopes[(28−25)/5+(31−28)/10]/2=.45.')
row(23,c('Linearization','L(T,H)=127+4(T−94)+(H−80)','L(T,H)=127+(T−94)+4(H−80)','L(T,H)=127−4(T−94)−(H−80)'),n('Estimated heat index',129,'°F',.2),why='Centered slopes: (135−119)/4=4 and(132−122)/10=1.')
row(24,c('Linearization','L(T,v)=−29+1.3(T+15)−0.15(v−50)','L(T,v)=−29−1.3(T+15)+0.15(v−50)','L(T,v)=−29+0.15(T+15)−1.3(v−50)'),n('Estimated wind chill',-32.35,'°C',.15),why='Centered differences from wind-chill table.')
u,v,w,p,q,alpha,beta,gamma=s.symbols('u v w p q alpha beta gamma',real=True)
for k,ex,vs in [(25,s.exp(-2*x)*s.cos(2*pi*t),[x,t]),(26,s.sqrt(x*x+3*y*y),[x,y]),(27,p**5*q**3,[p,q]),(28,v/(1+u*v*w),[u,v,w]),(29,alpha*beta**2*s.cos(gamma),[alpha,beta,gamma]),(30,x*z*s.exp(-y*y-z*z),[x,y,z])]:row(k,*[f('Coefficient of d'+str(vv),s.factor(s.diff(ex,vv))) for vv in vs],why='The total differential is the sum of each displayed coefficient times its corresponding independent-variable differential.')
for k,ex,pt,dv in [(31,5*x*x+y*y,[1,2],[R(5,100),R(1,10)]),(32,x*x-x*y+3*y*y,[3,-1],[-R(4,100),R(5,100)])]:
 sub={x:pt[0],y:pt[1]};de=sum(s.diff(ex,vv).subs(sub)*dd for vv,dd in zip([x,y],dv));actual=ex.subs({x:pt[0]+dv[0],y:pt[1]+dv[1]})-ex.subs(sub)
 row(k,n('Actual change Δz',actual),n('Differential dz',de),why='Evaluate the exact finite change separately from the first-order differential.')
row(33,n('Maximum area error',5.4,'cm²'),why='|dA|≤w|dl|+l|dw|=(24+30)0.1.')
row(34,n('Estimated metal volume',R(14,5)*pi,'cm³'),why='dV=2πrh dr+πr²dh with r=2,h=10,dr=.05,dh=.2.')
row(35,n('Estimated tin volume',R(128,25)*pi,'cm³'),why='r=4,h=12,dr=.04,dh=.08, hence dV=5.12π.')
row(36,n('Maximum wind-chill error',.6215+.3965*26**.16+2*abs(.16*(-11.37+.3965*(-11))*26**(-.84)),'°C'),c('Error rule','|dW|≤|W_T|·1+|W_v|·2','Add signed errors and allow cancellation','Use only temperature error'),why='Maximum measurement error adds absolute derivative contributions.')
r,RR=s.symbols('r R',positive=True);qex=RR/(2*r*r+RR*RR);change=(s.diff(qex,r)+s.diff(qex,RR)).subs({r:R(7,10),RR:3})/10
row(37,n('Estimated ΔT/(mg), lengths in cm',change,'cm⁻¹'),c('Direction','Decrease','Increase','No change'),why='Use the printed T=mgR/(2r²+R²), with dr=dR=.1cm. The printed model has dimensional units mg/length; the checked normalized coefficient explicitly retains cm⁻¹.')
row(38,n('Pressure change',-8.31*310/12**2*.3+8.31/12*(-5),'kPa',.01),why='dP=−8.31T dV/V²+8.31 dT/V.')
req=1/(R(1,25)+R(1,40)+R(1,50))
row(39,n('Maximum resistance error',req*.005,'ohm',.0001),why='dR=R²Σ(dR_i/R_i²); each bound .005R_i gives .005R.')
row(40,n('Maximum percentage error',2.3,'%'),why='|dS|/S≤.425(.02)+.725(.02)=.023.')
L=R(2300,121)+(x-23)/R(121,100)-46/R(1331,1000)*(y-R(11,10))
row(41,c('a · Linearization','B≈23/1.1²+(m−23)/1.1²−46(h−1.1)/1.1³','B≈23/1.1²+(m−23)−(h−1.1)','B≈m/h'),n('b · Linearized new BMI',L.subs({x:24,y:R(113,100)}),tol=.001),n('b · Actual new BMI',24/R(113,100)**2,tol=.001))
row(42,c('Tangent plane','8x−5y+6z=29','3x−4z=−6','8x+5y+6z=39'),why='r₁(0)=P and r₂(1)=P. Cross(3,0,−4),(2,6,2)=(24,−14,18)? See independent cross-product check.')
# Correct cross product: (3,0,-4) × (2,6,2) = (24,-14,18), reduced (12,-7,9).
qid='calculus-section-14-4-42';A.out[qid]['grader']=c('Tangent plane','12x−7y+9z=44','12x+7y+9z=58','3x−4z=−6');A.out[qid]['grader'].update(explanation='Tangents(3,0,−4) and(2,6,2) have normal(12,−7,9); substitute P=(2,1,3).',scope='Checks the tangent-plane equation.',provenance='explicit-source-inspected-original-answer-contract');A.notes[qid]='Independent tangent-vector cross product gives normal(12,−7,9).'
row(43,c('Valid error terms','ε₁=Δx, ε₂=Δy','ε₁=1, ε₂=1','ε₁=2a, ε₂=2b'),limited=True,why='The remainder Δx²+Δy²=ε₁Δx+ε₂Δy and both errors tend to0.')
row(44,c('Valid error terms','ε₁=Δy, ε₂=−5Δy','ε₁=Δx, ε₂=5Δx','ε₁=1, ε₂=−5'),limited=True,why='The remainder is ΔxΔy−5Δy².')
row(45,c('Limit of increment','f(a+Δx,b+Δy)−f(a,b)→0','Always tends to1','Can fail to tend to0 for differentiable f'),limited=True,why='Differentiability expresses the increment as a linear term plus errors tending to0 times increments; every term tends to0.')
row(46,n('a · f_x(0,0)',0),n('a · f_y(0,0)',0),c('a · Differentiability','Not differentiable: y=x gives limiting value1/2 but f(0,0)=0','Differentiable because both partials exist','Differentiable with gradient(1/2,1/2)'),c('b · Partial continuity','Neither partial is continuous: f_x(0,y)=1/y and f_y(x,0)=1/x away from0','Both are continuous','Only f_x is continuous'),limited=True)
suffix='-project-applied-project-the-speedo-lzr-racer-1'
row(1,c('Fractional change','((1+x)/(1+y))^(1/3)−1','(1+x)/(1+y)−1','(x/y)^(1/3)'),c('Physical domain','x≥−1 and y>−1 (positive initial P,C; nonnegative new power)','All R²','x>0,y>0 only'),limited=True,suffix=suffix)
row(2,f('Linearization at(0,0)',(x-y)/3),c('Small-change comparison','Equal fractional power increase and drag decrease have equal first-order benefits','Power increase is three times as effective','Drag decrease has no effect'),suffix=suffix)
ex=((1+x)/(1+y))**R(1,3)-1
row(3,c('f_xx','−2/[9(1+x)^(5/3)(1+y)^(1/3)]','2/[9(1+x)^(5/3)(1+y)^(1/3)]','0'),c('f_yy','4(1+x)^(1/3)/[9(1+y)^(7/3)]','−4(1+x)^(1/3)/[9(1+y)^(7/3)]','0'),c('Approximation comparison','Overestimates gain from increased power; underestimates gain from reduced drag','Underestimates both','Overestimates both'),limited=True,suffix=suffix)
row(4,c('Level curves','x=(1+k)³(1+y)−1, k≥−1, with physical-domain restrictions','x²+y²=k','x+y=k'),c('Interpretation','Lines through(−1,−1) have slope dx/dy=(1+k)³; benefits become more sensitive to drag reduction than equal power increase','All contours are equally spaced circles','Neither input affects speed'),limited=True,suffix=suffix)
save_section('section04')
