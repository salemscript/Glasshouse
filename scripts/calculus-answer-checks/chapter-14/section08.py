from common import *
import numpy as np
from scipy.optimize import minimize,brentq
row=lambda k,*fs,**kw:A.row(8,k,*fs,**kw)
row(1,n('Maximum estimate',60,tol=3),n('Minimum estimate',30,tol=3),limited=True,why='The extreme levels are tangent to the pink constraint, at its top and bottom. Read the labeled contours, not the horizontal-axis intersections.')
row(2,n('a,b · Minimum',-1),n('a,b · Maximum',R(5,4)),c('Tangency interpretation','Smallest and largest levels intersecting the circle','Both are minima','Both are maxima'),limited=True,why='On the circle f=1−y²+y=5/4−(y−1/2)².')
values={3:(-1,1),4:(-10,10),5:(-2,2),6:(-s.E,s.E),7:(-9,9),8:(s.exp(-16),s.exp(16)),9:(-2,2),10:(s.log(13),3*s.log(5)),11:(1,s.sqrt(3)),12:(R(1,3),1),13:(-2,2)}
for k,(lo,hi) in values.items():
 fs=[n('Minimum',lo,tol=abs(float(lo))*1e-8 if k==8 else None),n('Maximum',hi)]
 row(k,*fs,why='Solve the multiplier equations and compare every feasible stationary value. Symmetry or weighted AM–GM gives the same bounds.')
row(14,c('Minimum and maximum','−√n and √n','−n and n','0 and n'),c('Equality points','All xᵢ=−1/√n for minimum; all xᵢ=1/√n for maximum','One coordinate1, others0','All coordinates1'),why='Cauchy–Schwarz bounds the sum by√n on the unit sphere.')
row(15,n('Minimum',2),c('Maximum','None; unbounded above','2','1'),c('Minimum points','(1,1),(−1,−1)','(1,−1),(−1,1)','Origin'),limited=True)
row(16,n('Minimum',R(50,3)),c('Minimizing point','(5/3,5/3,5/3)','(1,2,3)','(10,0,0)'),c('Maximum','None; unbounded above','50/3','100'),limited=True,why='Weighted Cauchy–Schwarz gives100≤6f, equality when x=y=z.')
row(17,n('Minimum',1-s.sqrt(2)),n('Maximum',1+s.sqrt(2)),why='x+y=1 implies f=1+z; on x²+z²=2, z lies between±√2.')
row(18,c('Absolute extrema','Neither exists: z is unbounded above and below','Maximum24 and minimum0','Minimum24(√2−1), with no maximum'),n('Positive-branch local minimum z',24*(s.sqrt(2)-1)),n('Negative-branch local maximum z',-24*(1+s.sqrt(2))),why='Feasibility requires(24−z)²≤2z². Hence z≤−24(1+√2) or z≥24(√2−1). The two multiplier values are branch extrema, not global extrema.')
row(19,n('Minimum',R(1,2)),n('Maximum',R(3,2)),why='f=1+yz, y²+z²=1 gives|yz|≤1/2; equality has nonzero y and x=1/y.')
row(20,n('Minimum',1),c('Maximum','None; unbounded above','3','1'),why='x=y+1 and z²=y²−1 give f=3y²+2y for|y|≥1. Minimum is y=−1,x=z=0.')
row(21,n('Minimum',-8),n('Maximum',9+12*s.sqrt(2)),why='f=(x+2)²+(y−2)²−8; center(−2,2) lies inside the disk and the farthest point is on its opposite radius.')
row(22,n('Minimum',-7),n('Maximum',47),why='Interior minimum(1,0). On radius4 boundary, f=43−x²−4x=47−(x+2)².')
row(23,n('Minimum',s.exp(-R(1,4))),n('Maximum',s.exp(R(1,4))),why='Let u=x,v=2y. Then|xy|=|uv|/2≤1/4 on u²+v²≤1.')
row(24,c('a · Multiplier point','(9,4), f=30','(4,9), f=35','(25,0), f=50'),n('b · f(25,0)',50),n('c · Absolute maximum',75),c('Maximizing point','(0,25)','(25,0)','(9,4)'),c('d · Why missed','Constraint gradient is undefined at the endpoint maximum','Objective is not differentiable','Constraint has no points'),c('e · Meaning of f(9,4)','Absolute minimum30','Absolute maximum30','Neither'),limited=True,why='Set u=√x, √y=5−u, 0≤u≤5; f=5(u−3)²+30. Check endpoints as well as interior stationarity.')
row(25,c('a · Regular multiplier solution','(1,0), x=1 (maximum)','(0,0), x=0','No feasible points'),n('b · Minimum',0),c('c · Failure at minimum','∇g(0,0)=0 while ∇f=(1,0), so no multiplier exists','∇f=0','Curve is empty'),limited=True,why='y²=x³(1−x) forces0≤x≤1; the minimum is the singular cusp.')
# Complete circle search using bracketed derivative roots.
a=s.symbols('a',real=True);ex=(3+3*s.cos(a))**3+(3+3*s.sin(a))**3+3*(3+3*s.cos(a))*(3+3*s.sin(a));df=s.lambdify(a,s.diff(ex,a),'numpy');ff=s.lambdify(a,ex,'numpy')
roots=[]
for l,r in zip(np.linspace(0,2*np.pi,10001)[:-1],np.linspace(0,2*np.pi,10001)[1:]):
 if df(l)*df(r)<0:roots.append(brentq(df,l,r))
vs=[float(ff(q)) for q in roots];row(26,n('a,b · Minimum',min(vs),tol=.001),n('a,b · Maximum',max(vs),tol=.001),limited=True,why='Parameterize x=3+3cosθ,y=3+3sinθ, bracket all derivative roots around one full circle, and compare their values.')
row(27,c('Optimal allocation','L=αp/m, K=(1−α)p/n','L=p/m,K=p/n','L=K=p/(m+n)'),limited=True,why='At an interior optimum αP/L=λm and(1−α)P/K=λn. The budget then gives the allocation; boundary production is0.')
row(28,c('Optimal labor','L=(Q/b)[αn/((1−α)m)]^(1−α)','L=αQ/m','L=Q/b'),c('Optimal capital','K=(Q/b)[(1−α)m/(αn)]^α','K=(1−α)Q/n','K=Q/b'),why='Tangency gives K/L=(1−α)m/(αn); substitute into the fixed-production equation.')
row(29,c('Optimal side lengths','p/4,p/4','p/2,p/2','p/3,p/6'),c('Maximum area','p²/16','p²/4','p²/8'),limited=True)
row(30,c('Optimal side lengths','p/3,p/3,p/3','p/2,p/4,p/4','p/4,p/4,p/4'),c('Maximum area','√3 p²/36','√3 p²/4','p²/16'),limited=True,why='With semiperimeter fixed, AM–GM maximizes(s−x)(s−y)(s−z) when x=y=z.')
# Alternate multiplier checks retain all explicit answers from referenced exercises.
prev=json.loads((ROOT/'scripts/calculus-answer-checks/chapter-14/section07.json').read_text())
for k,old in enumerate([41,42,43,44,45,46,47,48,49,50,51,52,55],31):
 fields=prev[f'calculus-section-14-7-{old}']['grader'];fields=fields.get('parts',[fields]);fields=[{kk:vv for kk,vv in q.items() if kk in ['type','label','answer','unit','tolerance','options']} for q in fields]
 row(k,*fields,limited=True,why=f'Apply ∇objective=λ∇constraint and compare feasible boundary candidates for the complete problem14.7#{old}. This checks the resulting dimensions/values, not the written multiplier derivation.')
va=[]
for aa in [(50-5*s.sqrt(10))/3,(50+5*s.sqrt(10))/3]:va.append(s.simplify(aa**2*(50-2*aa)))
row(44,n('Minimum volume',min(va),'cm³'),n('Maximum volume',max(va),'cm³'),why='a+b+c=50 and ab+bc+ca=750. At extrema two dimensions agree; solve3a²−100a+750=0 and compare a²(50−2a).')
row(45,c('Nearest point','(1/2,1/2,1/2)','(0,0,0)','(1,1,2)'),c('Farthest point','(−1,−1,2)','(1,1,2)','(−1/2,−1/2,1/2)'),why='Distance squared=z+z² and feasibility gives1/2≤z≤2, with equal x,y at both endpoints.')
row(46,c('a · Intersection','Closed ellipse entirely in the upper cone','Hyperbola on both cone halves','Circle in z=0'),c('b · Highest point','(−4/3,1,5/3)','(4/3,−1,5/3)','(0,0,5/8)'),c('b · Lowest point','(4/13,−3/13,5/13)','(−4/13,3/13,5/13)','Origin'),limited=True,why='|4x−3y|≤5|z| and4x−3y=5−8z imply5/13≤z≤5/3. Equality fixes the horizontal direction.')
# Multi-start constrained optimizations, with feasible residuals recorded for independent review.
numaudit={}
for k,obj,cons in [(47,lambda v:v[1]*np.exp(v[0]-v[2]),[lambda v:9*v[0]**2+4*v[1]**2+36*v[2]**2-36,lambda v:v[1]*(v[0]+v[2])-1]),(48,lambda v:sum(v),[lambda v:v[0]**2-v[1]**2-v[2],lambda v:v[0]**2+v[2]**2-4])]:
 results=[]
 for sign in [-1,1]:
  best=None
  for seed in np.random.default_rng(k).uniform(-2,2,(120,3)):
   q=minimize(lambda v:sign*obj(v),seed,method='SLSQP',constraints=[{'type':'eq','fun':g} for g in cons],options={'maxiter':500,'ftol':1e-12})
   if q.success and max(abs(g(q.x)) for g in cons)<1e-7 and (best is None or sign*obj(q.x)<sign*obj(best.x)):best=q
  assert best is not None
  results.append({'value':float(obj(best.x)),'point':best.x.tolist(),'residual':max(abs(g(best.x)) for g in cons)})
 hi,lo=results;row(k,n('Minimum',lo['value'],tol=.0001),n('Maximum',hi['value'],tol=.0001),why='Solve the constrained stationary equations on every component; values are evaluated in the original objective and both original constraints are checked.');numaudit[k]=results
row(49,c('a · Maximum geometric mean','c/n','c','c^n/n'),c('b · Inequality and equality','Geometric mean≤arithmetic mean; equality iff all inputs equal','Geometric mean≥arithmetic mean','Equality for every input'),limited=True)
row(50,n('a · Maximum scalar product',1),c('Equality','y=x for unit vectors','y=−x','x and y orthogonal'),c('b · Conclusion','Σaᵢbᵢ≤√(Σaᵢ²)√(Σbᵢ²), including zero vectors by direct inspection','Σaᵢbᵢ≥√(Σaᵢ²)√(Σbᵢ²)','Σaᵢbᵢ=1 for all vectors'),limited=True,why='For unit vectors,0≤||x−y||²=2−2x·y. Normalize nonzero vectors; handle zero vectors separately.')
save_section('section08')
(ROOT/'scripts/calculus-answer-checks/chapter-14/section08-calculation-audit.json').write_text(json.dumps({'circleRoots':roots,'circleValues':vs,'constrainedNumerics':numaudit},indent=2)+'\n')
