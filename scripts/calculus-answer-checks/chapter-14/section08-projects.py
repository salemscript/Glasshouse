from common import *
import numpy as np
from scipy.optimize import brentq, minimize
from itertools import combinations

def rocket(i,*fs,**kw):A.row(8,i,*fs,suffix='-project-applied-project-rocket-science-1',**kw)
def hydro(i,*fs,**kw):A.row(8,i,*fs,suffix='-project-applied-project-hydro-turbine-optimization-2',**kw)
rocket(1,c('Final velocity','v_f=c ln[(M₁+M₂+M₃+A)/(SM₁+M₂+M₃+A)]+c ln[(M₂+M₃+A)/(SM₂+M₃+A)]+c ln[(M₃+A)/(SM₃+A)]','v_f is the negative of this sum of three log ratios','v_f=c ln[(M₁+M₂+M₃+A)/A] regardless of S'),limited=True,why='At each burn, the later stages plus payload are carried as that stage’s payload. Add the three velocity increments with the initial-to-final mass ratio in each logarithm, assuming the stated common c and S and negligible external forces.')
rocket(2,c('Each successive total-mass ratio','T_i/T_(i+1)=(1−S)N_i/(1−SN_i), with T₁=M+A,T₂=M₂+M₃+A,T₃=M₃+A,T₄=A','T_i/T_(i+1)=N_i/(1−S)','T_i/T_(i+1)=(1−SN_i)/[(1−S)N_i]'),c('Product identity','(M+A)/A=(1−S)³N₁N₂N₃/[(1−SN₁)(1−SN₂)(1−SN₃)]','(M+A)/A=N₁N₂N₃','(M+A)/A=(1−S)³/[(1−SN₁)(1−SN₂)(1−SN₃)]'),limited=True,why='Rearrange N_i=T_i/[SM_i+T_(i+1)] using M_i=T_i−T_(i+1), then multiply the three telescoping ratios. Physical stages require1≤N_i<1/S for0<S<1.')
rocket(3,c('Monotonic objective','ln((M+A)/A) is strictly increasing in M for fixed A>0','It is strictly decreasing in M','It depends only on A'),c('Optimal N values','N₁=N₂=N₃=exp(v_f/(3c))','N₁=N₂=N₃=exp(v_f/c)','N₁=N₂=N₃=v_f/(3c)'),c('Finite-mass feasibility','0≤v_f<3c ln(1/S), for0<S<1','Any arbitrarily large v_f is feasible with finite mass','v_f must equal3c ln(1/S)'),limited=True,why='For w_i=ln N_i, the objective is3ln(1−S)+Σ[w_i−ln(1−S e^w_i)] with fixed sum v_f/c. Its second derivative isS e^w/(1−S e^w)²>0; equal w_i gives the global minimum.')
rocket(4,c('Minimum engine mass','M_min=A{[(1−S)e^(v_f/(3c))/(1−S e^(v_f/(3c)))]³−1}','M_min=A[e^(v_f/c)−1] for every S','M_min=A e^(v_f/(3c))'),why='Let R=(1−S)N/(1−SN) with N=e^(v_f/(3c)). The optimal total launch mass is AR³ and subtracting the payload gives engine-plus-fuel mass A(R³−1).')
def stages(velocity,payload=1):
 N=np.exp(velocity/18000);rr=.8*N/(1-.2*N);return np.array([payload*rr*rr*(rr-1),payload*rr*(rr-1),payload*(rr-1)])
ss=stages(17500);rocket(5,n('a · Minimum M/A',sum(ss),tol=.0001),*[n('b · M'+str(i+1)+'/A',v,tol=.0001) for i,v in enumerate(ss)],why='With S=.2,c=6000mi/h and v_f=17500mi/h, compute N=e^(17500/18000), R=.8N/(1−.2N). Then M₃=A(R−1),M₂=AR(R−1),M₁=AR²(R−1). Mass ratios do not depend on the unit used for A.')
ss2=stages(24700,500);rocket(6,*[n('Stage'+str(i+1)+' mass',v,'lb (same mass-unit convention as the 500-lb payload)',tol=1) for i,v in enumerate(ss2)],why='Use the same S=.2,c=6000mi/h but v_f=24700mi/h and A=500lb. The geometrically decreasing stage masses again follow R²(R−1),R(R−1),R−1 times A; these are the source’s common pound-based mass ratios.')
b=np.array([.1277,.1358,.1380]);d=np.array([4.08e-5,4.69e-5,3.84e-5]);a=np.array([-18.89,-24.51,-27.02]);caps=np.array([1110,1110,1225]);inv=1/(2*d);slopes=inv/inv.sum();intercepts=inv*(b-(inv*b).sum()/inv.sum())
lo=max((250-intercepts)/slopes);hi=min((caps-intercepts)/slopes)
def opt(total,active=(0,1,2)):
 ids=np.array(active,dtype=int)
 if total<250*len(ids) or total>caps[ids].sum():return None
 lam=brentq(lambda lam:np.clip((b[ids]-lam)/(2*d[ids]),250,caps[ids]).sum()-total,-1,1,xtol=1e-14)
 flows=np.zeros(3);flows[ids]=np.clip((b[ids]-lam)/(2*d[ids]),250,caps[ids]);power=(170-1.6e-6*total**2)*sum(a[ids]+b[ids]*flows[ids]-d[ids]*flows[ids]**2);return flows,power
fs=[]
for i in range(3):fs.extend([n('Interior Q'+str(i+1)+' = slope·Q_T + intercept · slope',slopes[i],tol=.0000005),n('Interior Q'+str(i+1)+' · intercept',intercepts[i],'ft³/s',tol=.0005)])
fs.append(c('Bounds outside the interior interval','Q_i=clip((b_i−λ)/(2d_i),250,cap_i), choose λ so ΣQ_i=Q_T','Keep the affine formulas even if a turbine exceeds its cap','Split flow equally for all Q_T'))
hydro(1,*fs,why='The common positive head factor H=170−1.6×10^−6Q_T² is fixed at a given total flow. Maximize Σ(a_i+b_iQ_i−d_iQ_i²); interior marginal powers b_i−2d_iQ_i are equal. The negative definite Hessian ensures the unique global constrained maximum, with clipping when a flow bound is active.')
hydro(2,n('Lower Q_T for all three affine formulas',lo,'ft³/s',tol=.001),n('Upper Q_T for all three affine formulas',hi,'ft³/s',tol=.001),c('Full feasible all-three interval (with clipping)','750≤Q_T≤3445 ft³/s','250≤Q_T≤1225 ft³/s','All nonnegative Q_T'),why='Intersect each inequality250≤slope_i Q_T+intercept_i≤cap_i. All-three operation at bound-active totals is possible between the sum of lower bounds750 and upper bounds3445.')
flows,power=opt(2500);hydro(3,*[n('Q'+str(i+1),q,'ft³/s',tol=.01) for i,q in enumerate(flows)],n('Maximum power',power,'kW',tol=.1),c('Nearby feasible perturbations','Every nonzero zero-sum perturbation lowers power by HΣd_i(ΔQ_i)²','Some sufficiently small zero-sum perturbation raises power','All distributions give the same power'),limited=True,why='At the interior optimum the first-order change vanishes on zero-sum perturbations; the exact quadratic difference is negative. Numeric comparisons also check nearby splits.')
records={}
for total in [600,1000,1500,2500,3400]:
 records[total]=[]
 for count in [1,2,3]:
  for active in combinations(range(3),count):
   result=opt(total,active)
   if result is not None:records[total].append({'active':[i+1 for i in active],'flows':result[0].tolist(),'power':float(result[1])})
 records[total].sort(key=lambda r:r['power'],reverse=True)
fs=[]
for total in [1000,600]:
 one=max((r for r in records[total] if len(r['active'])==1),key=lambda r:r['power']);fs.extend([c(str(total)+'ft³/s · recommended single turbine','Turbine '+str(one['active'][0]),*[str('Turbine '+str(j)) for j in [1,2,3] if j!=one['active'][0]]),n(str(total)+'ft³/s · best single-turbine power',one['power'],'kW',tol=.1)])
fs.extend([c('1000ft³/s · single versus three','Use the best single turbine; it beats the optimal three-turbine split','Use all three; they always beat one','They give equal power'),c('600ft³/s · three-turbine feasibility','Impossible: three minimum flows require750ft³/s','Feasible with200ft³/s through each','Always feasible if enough turbines are turned on')])
hydro(4,*fs,limited=True,why='For each total, compare the three individual quadratic curves with the constrained all-three maximum. An inactive turbine contributes zero power, not its negative constant intercept. The curves share the same head factor for this total flow; their domain restrictions still apply.')
besttwo=max((r for r in records[1500] if len(r['active'])==2),key=lambda r:r['power']);allthree=opt(1500)
hydro(5,c('Recommended pair','Turbines '+','.join(map(str,besttwo['active'])),*[str('Turbines '+','.join(map(str,pair))) for pair in [(1,2),(1,3),(2,3)] if list(pair)!=besttwo['active']]),*[n('Q'+str(i+1),q,'ft³/s',tol=.01) for i,q in enumerate(besttwo['flows'])],n('Two-turbine power',besttwo['power'],'kW',tol=.1),n('Optimal all-three power',allthree[1],'kW',tol=.1),c('Comparison','The best two turbines generate more power than all three','All three generate more power','Equal power'),why='For each feasible pair solve equality of its two marginal quadratic powers with the sum1500. Compare all three pair maxima and the all-three maximum, including fixed operating intercepts only for active turbines.')
flows,power=opt(3400);hydro(6,c('Operating recommendation','Use all three and enforce turbine3 cap1225ft³/s; optimize the remaining2175ft³/s between1 and2','Use the unconstrained affine split even when Q₃>1225','Use only turbines1 and2 for all3400ft³/s'),*[n('Q'+str(i+1),q,'ft³/s',tol=.01) for i,q in enumerate(flows)],n('Maximum power',power,'kW',tol=.1),why='No pair has enough capacity for3400. The unconstrained optimum exceeds turbine3’s cap. Set Q₃=1225 and equate the remaining marginal powers while Q₁+Q₂=2175; both remain within their limits.')
# Independent SLSQP and nearby-split validation for the analytic clipping solution.
checks=0
for total in [750,900,1000,1500,2500,3400,3445]:
 flows,power=opt(total)
 result=minimize(lambda q: -sum(a+b*q-d*q*q),np.full(3,total/3),method='SLSQP',bounds=[(250,float(v)) for v in caps],constraints=[{'type':'eq','fun':lambda q:q.sum()-total}],options={'ftol':1e-11,'maxiter':1000})
 assert abs(sum(a+b*flows-d*flows*flows)+result.fun)<1e-6,(total,result);checks+=1
for delta in [np.array([1,-1,0]),np.array([0,1,-1]),np.array([10,-5,-5])]:
 q,pow0=opt(2500);pow1=(170-1.6e-6*2500**2)*sum(a+b*(q+delta)-d*(q+delta)**2);assert pow1<pow0;checks+=1
# Direct rocket velocity recovered from generated stage masses.
for target,payload,masses in [(17500,1,ss),(24700,500,ss2)]:
 recovered=0
 for i,mi in enumerate(masses):tail=payload+sum(masses[i+1:]);recovered+=6000*np.log((mi+tail)/(.2*mi+tail))
 assert abs(recovered-target)<1e-8;checks+=1
here=Path(__file__).parent
(here/'section08-projects.json').write_text(json.dumps(A.out,ensure_ascii=False,indent=2)+'\n');(here/'section08-projects-audit.json').write_text(json.dumps({'notes':A.notes,'hydroComparisons':records,'affineSlopes':slopes.tolist(),'affineIntercepts':intercepts.tolist(),'interiorInterval':[lo,hi],'independentChecks':checks,'sourcePages':[979,980,981]},ensure_ascii=False,indent=2)+'\n');print('14.8 projects',len(A.out),'checks',checks)
