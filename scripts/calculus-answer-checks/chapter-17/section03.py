from ode import *
for k,m,damp,stiff,y0,v0 in [(1,5,0,100,R(35,100),0),(2,8,0,80,0,1),(3,2,14,12,1,0),(4,2,8,52,0,R(1,2))]:
 abc=(m,damp,stiff);sol=solve(abc,ics=iv(y0,v0));fs=[n('Spring constant',stiff,'N/m'),answer(sol,abc,'Position relative to equilibrium (meters), x(t)',t)]
 if k==4:fs+=[c('b · Graph features','Decaying oscillation; x(0)=0 and x′(0)=0.5; envelope proportional to e^(−2t)','Growing oscillation','Monotone motion with no zero crossings')]
 A.row(3,k,*fs,limited=k==4,why='Hooke’s law gives k=force/extension. Use m x″+c x′+kx=0 with displacement from equilibrium and the stated initial displacement/velocity; t is in seconds.')
A.row(3,5,n('Critical mass',R(49,12),'kg'),why='Critical damping means c²−4mk=0; using c=14 and k=12 gives m=196/48.')
A.row(3,6,n('Critical damping constant',4*s.sqrt(26),'N·s/m'),why='For m=2 kg and k=52 N/m, c=2√(mk)=4√26.')
for k,vals in [(7,[10,15,20,25,30]),(8,[10,20,25,30,40])]:
 fs=[]
 for val in vals:
  abc=(1,val,100) if k==7 else (1,10,val);sol=solve(abc,ics=iv(-R(1,10),0) if k==7 else iv(0,1));disc=abc[1]**2-4*abc[0]*abc[2];typ='Underdamped' if disc<0 else 'Critically damped' if disc==0 else 'Overdamped'
  label=('c' if k==7 else 'k')+'='+str(val)
  fs.extend([answer(sol,abc,label+' · x(t) in meters',t),c(label+' · damping',typ,*[o for o in ['Underdamped','Critically damped','Overdamped'] if o!=typ])])
 A.row(3,k,*fs,limited=True,why='Positive displacement is downward; released above equilibrium means x(0)=−0.1 m. Use the characteristic discriminant c²−4mk to distinguish oscillatory, repeated-root and two-real-root motion.' if k==7 else 'Use x(0)=0, x′(0)=1. Compare c² with 4mk for each k. Each listed function determines the requested plot; the hand/computer drawing is not automatically assessed.')
A.row(3,9,c('Nonresonant motion','x(t)=C₁cos(ωt)+C₂sin(ωt)+F₀ cos(ω₀t)/[m(ω²−ω₀²)]','x(t)=C₁cos(ωt)+C₂sin(ωt)+F₀ cos(ω₀t)/[m(ω²+ω₀²)]','x(t)=F₀ cos(ω₀t)/m'),limited=True,why='Substitute A cos(ω₀t) into mx″+mω²x=F₀cos(ω₀t): A m(ω²−ω₀²)=F₀. Add the complementary oscillation.')
A.row(3,10,c('Resonant motion','x(t)=C₁cos(ωt)+C₂sin(ωt)+F₀t sin(ωt)/(2mω)','x(t)=C₁cos(ωt)+C₂sin(ωt)+F₀sin(ωt)/(2mω)','x(t)=C₁cos(ωt)+C₂sin(ωt)+F₀t cos(ωt)/(2mω)'),limited=True,why='The forcing overlaps a homogeneous mode, so try At sin(ωt); x″+ω²x contributes 2Aω cos(ωt).')
A.row(3,11,c('One common period when ω/ω₀=p/q, p,q positive integers','T=2πp/ω=2πq/ω₀','T=2πp/ω₀=2πq/ω','T=2π/(ω+ω₀)'),limited=True,why='Both phases change by integer multiples of 2π in this time. The stated period need not be the least period if one amplitude vanishes.')
A.row(3,12,c('a · Critical crossing time','t=−C₁/C₂>0 when C₁,C₂ have opposite signs','t=C₁/C₂>0 for opposite signs','No critical solution can cross equilibrium'),c('b · Positive crossing condition','C₁C₂<0 and |C₂|>|C₁|, assuming r₁>r₂','C₁C₂>0','C₁C₂<0 and |C₂|<|C₁|'),c('b · Crossing time','t=ln(−C₂/C₁)/(r₁−r₂)','t=ln(−C₁/C₂)/(r₁−r₂)','t=−C₁/C₂'),limited=True,why='Exponential factors never vanish. Solve C₁+C₂t=0 in the critical case and exp[(r₁−r₂)t]=−C₂/C₁ in the overdamped case.')
for k,abc,forcing,initial in [(13,(1,20,500),12,iv(0,0)),(14,(2,24,200),12,iv(R(1,1000),0)),(15,(1,20,500),12*s.sin(10*x),iv(0,0)),(16,(2,24,200),12*s.sin(10*x),iv(R(1,1000),0))]:
 sol=solve(abc,forcing,initial);fs=[answer(sol,abc,'a · Charge Q(t), coulombs' if k in (14,16) else 'Charge Q(t), coulombs',t)]
 if k in (13,14):
  cur=s.simplify(s.diff(sol,x));fs.append(c('Current I(t), amperes',fmt(cur.subs(x,t)),fmt((-cur).subs(x,t)),fmt((cur+1).subs(x,t))))
 if k in (14,16):fs.append(c('b · Long-time graph', 'Q→0.06 C and I→0 A, with decaying oscillations' if k==14 else 'Q approaches −cos(10t)/20 C, with a decaying transient','Q grows without bound','Q is identically zero'))
 A.row(3,k,*fs,limited=k in (14,16),why='Use LQ″+RQ′+Q/C=E(t), with I=Q′. Retain the charge/current initial conditions from the referenced exercise; t is seconds. The equation and initial conditions are checked symbolically.')
A.row(3,17,c('Amplitude','A=√(C₁²+C₂²)','A=C₁+C₂','A=C₁²+C₂²'),c('Phase (A>0)','cosδ=C₁/A and sinδ=−C₂/A','cosδ=C₁/A and sinδ=C₂/A','cosδ=−C₁/A and sinδ=C₂/A'),limited=True,why='Expand A cos(ωt+δ). If A=0 the solution is identically zero and the phase is arbitrary.')
g=R(49,5);w=s.sqrt(g);theta=s.cos(w*x)/5+s.sin(w*x)/w;amp=s.sqrt(R(1,25)+1/g);first=(pi-s.atan(w/5))/w;speed=s.sqrt(1+g/25)
A.row(3,18,c('a · θ(t), radians (g=9.8 m/s²)',fmt(theta.subs(x,t)),fmt((theta+s.sin(w*x)).subs(x,t)),fmt((theta*2).subs(x,t))),n('b · Maximum angle',amp,'rad'),n('c · Period',2*pi/w,'s'),n('d · First vertical time',first,'s'),n('e · Angular velocity at first vertical crossing',-speed,'rad/s'),c('e · Velocities at successive vertical crossings','Alternate −√(1+9.8/25) and +√(1+9.8/25) rad/s','Always positive','Always zero'),why='In the stipulated small-angle model θ″+9.8θ=0, use θ(0)=0.2 and θ′(0)=1. The amplitude is √(0.2²+1/9.8), first zero has phase π−atan(0.2√9.8), and crossing speed is amplitude times frequency. This is the linear approximation, not the exact nonlinear pendulum.')
save('section03')
