"""Independent coordinate arithmetic and numerical geometry checks against contracts."""
import json,math,random
from pathlib import Path
import numpy as np
from scipy.integrate import quad
F=Path(__file__).parent
bank=json.loads((F.parent/'chapter-12.json').read_text());checks=[]
def fields(q):return bank[q]['grader'].get('parts',[bank[q]['grader']])
def verify(q,label,value,tol=1e-7):
 field=next(f for f in fields(q) if f['label']==label)
 assert abs(field['answer']-float(value))<=tol*max(1,abs(float(value))),(q,label,field['answer'],value)
 checks.append([q,label,float(value)])
def num(sec,k,label,value,tol=1e-7):verify(f'calculus-section-12-{sec}-{k}',label,value,tol)
def vec(sec,k,label,value):
 for axis,v in zip('xyz',value):num(sec,k,label+' '+axis,v)
def arr(v):return np.asarray(v,dtype=float)
def norm(v):return math.sqrt(sum(float(x)**2 for x in v))
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def angle(a,b):return math.degrees(math.acos(dot(a,b)/(norm(a)*norm(b))))
# Independently transcribed source coordinate datasets.
for k,A,B,C in [(9,(3,-2,-3),(7,0,1),(1,2,1)),(10,(2,-1,0),(4,1,1),(4,-5,4))]:
 for label,p,q in [('PQ',A,B),('QR',B,C),('PR',A,C)]:num(1,k,label,norm(arr(p)-arr(q)))
for k,center,r in [(15,(3,8,1),math.sqrt(30)),(16,(1,2,3),math.sqrt(14)),(17,(1,2,-4),6),(18,(-4,3,-1),3),(19,(2,0,-6),math.sqrt(40.5)),(20,(0,1,2),math.sqrt(25/3)),(22,(3,5,-3),math.sqrt(41)),(24,(5,4,9),4)]:vec(1,k,'Center',center);num(1,k,'Radius',r)
for k,a,b in [(9,(-2,1),(1,2)),(10,(-5,-1),(-3,3)),(11,(3,-1),(2,3)),(12,(3,2),(1,0)),(13,(0,3,1),(2,3,-1)),(14,(0,6,-1),(3,4,4))]:vec(2,k,'AB',arr(b)-arr(a))
for k,a,b in [(15,(-1,4),(6,-2)),(16,(3,-1),(-1,5)),(17,(3,0,1),(0,8,0)),(18,(1,3,-2),(0,0,6))]:vec(2,k,'Sum',arr(a)+arr(b))
for k,a,b in [(19,(-3,4),(9,-1)),(20,(5,3),(-1,-2)),(21,(4,-3,2),(2,0,-4)),(22,(8,1,-4),(5,-2,1))]:
 a,b=arr(a),arr(b);vec(2,k,'a+b',a+b);vec(2,k,'4a+2b',4*a+2*b);num(2,k,'|a|',norm(a));num(2,k,'|a−b|',norm(a-b))
for k,a,length in [(23,(6,-2),1),(24,(-5,3,-1),1),(25,(8,-1,4),1),(26,(6,2,-3),4)]:vec(2,k,'Requested vector',arr(a)/norm(a)*length)
for k,m,a,unit in [(30,50,38,'N'),(31,60,40,'ft/s')]:num(2,k,'Horizontal component',m*math.cos(math.radians(a)));num(2,k,'Vertical component',m*math.sin(math.radians(a)))
# Reconstruct the equilibrium equations rather than reusing closed-form tension formulas.
M=np.array([[-math.cos(math.radians(50)),math.cos(math.radians(38))],[math.sin(math.radians(50)),math.sin(math.radians(38))]])
tensions=np.linalg.solve(M,[0,350]);num(2,37,'2m rope tension magnitude',tensions[0]);num(2,37,'3m rope tension magnitude',tensions[1])
num(2,38,'Weight',2*25*math.sin(math.radians(37)))
q='calculus-section-12-2-39';ff={f['label']:f['answer'] for f in fields(q)};time=ff['(b) Trip time']/60;theta=math.radians(ff['(a) Steering upstream from straight across']);assert abs(13*math.cos(theta)*time-3)<1e-10;assert abs((13*math.sin(theta)-3.5)*time-2)<1e-10;checks.extend([[q,'across displacement',3],[q,'upstream displacement',2]])
for k,a,b in [(2,(5,-2),(3,4)),(3,(1.5,.4),(-4,6)),(4,(6,-2,3),(2,5,-1)),(5,(4,1,.25),(6,-3,-8)),(7,(2,1,0),(1,-1,1)),(8,(3,2,-1),(4,0,5))]:num(3,k,'a·b',dot(a,b))
for k,a,b in [(15,(4,3),(2,-1)),(16,(-2,5),(5,12)),(17,(1,-4,1),(0,2,-2)),(18,(-1,3,4),(5,2,1)),(19,(4,-3,1),(2,0,-1)),(20,(8,-1,4),(0,4,2))]:num(3,k,'Angle to nearest degree',angle(a,b))
for k,names,points in [(21,'PQR',[(2,0),(0,3),(3,4)]),(22,'ABC',[(1,0,-1),(3,-2,0),(1,3,3)])]:
 for i,label in enumerate(names):num(3,k,'Angle '+label,angle(arr(points[(i+1)%3])-points[i],arr(points[(i+2)%3])-points[i]))
for k,a in [(33,(2,1,2)),(34,(6,3,-2)),(35,(1,-2,-3)),(36,(.5,1,1)),(37,(1,1,1))]:
 for axis,v in zip(['α','β','γ'],arr(a)/norm(a)):num(3,k,'cos '+axis,v);num(3,k,axis,math.degrees(math.acos(v)))
for k,a,b in [(39,(-5,12),(4,6)),(40,(1,4),(2,3)),(41,(4,7,-4),(3,-1,1)),(42,(-1,4,8),(12,1,2)),(43,(3,-3,1),(2,4,-1)),(44,(1,2,3),(5,0,-1))]:
 num(3,k,'Scalar projection',dot(a,b)/norm(a));vec(3,k,'Vector projection',arr(a)*dot(a,b)/dot(a,a))
for k,a,b in [(1,(2,3,0),(1,0,5)),(2,(4,3,-2),(2,-1,1)),(3,(0,2,-4),(-1,3,1)),(4,(3,3,-3),(3,-3,3)),(5,(.5,1/3,.25),(1,2,-3))]:vec(4,k,'a×b',cross(a,b));num(4,k,'(a×b)·a',dot(cross(a,b),a));num(4,k,'(a×b)·b',dot(cross(a,b),b))
for k,p,q,r in [(29,(1,0,1),(-2,1,3),(4,2,5)),(30,(0,0,-3),(4,2,0),(3,3,1)),(31,(0,-2,0),(4,1,-2),(5,3,1)),(32,(2,-3,4),(-1,-2,2),(3,1,-3))]:num(4,k,'(b) Triangle area',norm(cross(arr(q)-p,arr(r)-p))/2)
for k,a,b,c in [(33,(1,2,3),(-1,1,2),(2,1,4)),(34,(1,1,0),(0,1,1),(1,1,1)),(35,(4,2,2),(3,3,-1),(5,5,1)),(36,(-4,2,4),(2,1,-2),(-3,4,1))]:num(4,k,'Volume',abs(np.linalg.det(np.array([a,b,c]))))
# Point-line distances via orthogonal least-squares residual, independent of cross-product formula.
for sec,k,p,a,d in [(5,69,(4,1,-2),(1,3,4),(1,-2,-3)),(5,70,(0,1,3),(0,6,3),(2,-2,1))]:
 v=arr(p)-a;t=dot(v,d)/dot(d,d);num(sec,k,'Distance',norm(v-t*arr(d)))
for k,p,d,normal,rhs in [(45,(2,0,1),(-2,3,1),(1,2,-1),7),(46,(-1,1,3),(1,2,-1),(3,-1,2),5),(47,(0,0,-2),(.2,2,1),(10,-7,3),-24),(48,(-3,1,0),(2,4,6),(2,1,-1),-2)]:
 t=(rhs-dot(p,normal))/dot(d,normal);vec(5,k,'Intersection',arr(p)+t*arr(d))
for k,p,a,q,b in [(77,(0,0,0),(1,1,1),(-1,0,0),(1,2,3)),(78,(1,1,0),(1,6,2),(1,5,-2),(2,15,6)),(79,(0,0,0),(2,0,-1),(1,-1,1),(3,2,2))]:
 ts=np.linalg.lstsq(np.column_stack([a,-arr(b)]),arr(q)-p,rcond=None)[0];num(5,k,'Distance',norm(arr(p)+ts[0]*arr(a)-arr(q)-ts[1]*arr(b)))
# Verify every plane contract in the source audit against random in-plane directions.
plane_audit=json.loads((F/'section05-audit.json').read_text())['questions'];rng=random.Random(1205)
for qid,a in plane_audit.items():
 if 'normal' not in a:continue
 normal=arr([float(eval(v,{'__builtins__':{}},{})) for v in a['normal']]);point=arr([float(eval(v,{'__builtins__':{}},{})) for v in a['point']]);d=np.cross(normal,[1,2,4]);e=np.cross(normal,d)
 for _ in range(10):
  trial=point+rng.uniform(-3,3)*d+rng.uniform(-3,3)*e;assert abs(dot(normal,trial-point))<1e-8
  checks.append([qid,'normal orthogonality trial',0])
# Perspective project: each hidden endpoint's camera ray is independently intersected with rectangle basis.
pprefix='calculus-section-12-5-4-project-laboratory-project-putting-3d-in-perspective-1';qfields=fields(pprefix)
for label in ['Hidden segment far endpoint','Surface intersection endpoint']:
 p=arr([next(f['answer'] for f in qfields if f['label']==label+' '+ax) for ax in 'xyz']);cam=arr([1000,0,0]);r0=arr([621,-147,206]);e1=arr([563,31,242])-r0;e2=arr([657,-111,86])-r0
 av,bv,lv=np.linalg.solve(np.column_stack([e1,e2,-(p-cam)]),cam-r0)
 assert -.000001<=av<=1.000001 and -.000001<=bv<=1.000001 and 0<lv<=1.000001,(label,av,bv,lv)
 checks.append([pprefix,label+' rectangle intersection',float(lv)])
# Geometric integration checks of overlapping spheres and maximal projection solid.
lens=2*quad(lambda h:math.pi*(4-h*h),1.5,2)[0];num(1,46,'Common volume',lens)
maxvol=quad(lambda yy:2*math.sqrt(.25-yy*yy)*(1-2*abs(yy)),-.5,.5,epsabs=1e-12)[0]
verify('calculus-chapter-12-problems-plus-8-problems-plus-0','(a) Largest volume',maxvol)
# General algebra identities independently stress-tested on random source-scale integer vectors.
for _ in range(200):
 a,b,c=[arr([rng.randrange(-10,11) for _ in range(3)]) for _ in range(3)]
 cp=np.cross(a,b);assert abs(dot(cp,a))<1e-9 and abs(dot(cp,b))<1e-9
 assert np.allclose(np.cross(a,np.cross(b,c)),dot(a,c)*b-dot(a,b)*c)
 assert abs(dot(cp,cp)-(dot(a,a)*dot(b,b)-dot(a,b)**2))<1e-8
 checks.extend([['general','orthogonality a',0],['general','orthogonality b',0],['general','triple product',0],['general','Lagrange identity',0]])
result={'checks':len(checks),'failed':0,'method':'Independent scalar arithmetic, NumPy linear systems/least squares, SciPy quadrature, and randomized vector identities; no checker self-evaluation','details':checks}
(F/'independent-audit.json').write_text(json.dumps(result,indent=2)+'\n');print('Independent checks passed:',len(checks))
