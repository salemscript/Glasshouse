"""Independent numerical differentiation/quadrature and geometric identities."""
from common import *
import numpy as np
from scipy.integrate import quad
HERE=Path(__file__).parent
checks=[]
def close(a,b,label,tol=2e-7):
 aa=np.asarray(a,dtype=float);bb=np.asarray(b,dtype=float)
 assert np.allclose(aa,bb,rtol=tol,atol=tol),(label,aa,bb)
 checks.append(label)
def expr(z):return s.sympify(str(z),locals={'t':t,'a':s.Rational(3,2),'b':s.Rational(4,3),'omega':s.Rational(7,5),'c':s.Rational(6,5)})
def ev(z,tt=0):return float(expr(z).subs(t,tt).evalf())
def evalv(v,tt):return np.array([ev(z,tt) for z in v])
def funcs(v):return [s.lambdify(t,expr(z),'mpmath') for z in v]
def derivative(v,tt,order=1):return np.array([float(mp.diff(fn,mp.mpf(str(tt)),order)) for fn in funcs(v)])
def cross(v,w):return np.cross(v,w)
for sec in [2,3,4]:
 data=json.loads((HERE/f'section{sec:02}-audit.json').read_text())
 for d in data.get('cases',[]):
  k=d.get('kind','motion');label=f'13.{sec}#{d["n"]}:{k}';rr=d['r'];tt=ev(d['at']) if 'at' in d else .73
  if sec==2 and d['n']==9:tt=3.2
  if k=='derivative':close(derivative(rr,tt),evalv(d['derivative'],tt),label)
  elif k=='unit':v=derivative(rr,tt);close(v/np.linalg.norm(v),evalv(d['expected'],tt),label)
  elif k=='tangent':close(evalv(rr,tt),evalv(d['point'],tt),label+'point');close(derivative(rr,tt),evalv(d['direction'],tt),label+'direction')
  elif k=='definite':
   lo,hi=ev(d['lo']),ev(d['hi']);got=[float(mp.quad(fn,[lo,hi])) for fn in funcs(rr)];close(got,evalv(d['expected'],0),label)
  elif k in ['primitive','initial']:
   if sec==2 and d['n']==40:tt=.3
   close(derivative(d['expected'],tt),evalv(rr,tt),label)
   if k=='initial':close(evalv(d['expected'],tt),evalv(d['position'],tt),label+'initial')
  elif k=='length':
   lo,hi=ev(d['lo']),ev(d['hi']);fn=lambda z:np.linalg.norm(derivative(rr,z));ans,err=quad(fn,lo,hi,epsabs=1e-9,limit=1000);close(ans,ev(d['expected']),label,tol=2e-8)
  elif k in ['frame','frame-point','curvature','curvature-point','planes','torsion','torsion-point']:
   v=derivative(rr,tt);aa=derivative(rr,tt,2);j=derivative(rr,tt,3);vn=np.linalg.norm(v);cr=cross(v,aa);cn=np.linalg.norm(cr)
   if k.startswith('frame'):
    T=v/vn;N=aa-np.dot(aa,T)*T;N/=np.linalg.norm(N);close(T,evalv(d['T'],tt),label+'T');close(N,evalv(d['N'],tt),label+'N')
    if 'B'in d:close(cross(T,N),evalv(d['B'],tt),label+'B')
   if 'kappa'in d:close(cn/vn**3,ev(d['kappa'],tt),label+'kappa')
   if k=='curvature-point':close(cn/vn**3,ev(d['expected']),label)
   if k=='planes':close(v,evalv(d['normal'],tt),label+'normal');close(cr,evalv(d['binormal'],tt),label+'binormal')
   if k.startswith('torsion'):close(np.dot(cr,j)/(cn*cn),ev(d['expected'],tt),label)
  elif sec==4:
   v=derivative(rr,tt);aa=derivative(rr,tt,2)
   if 'v'in d:close(v,evalv(d['v'],tt),label+'velocity')
   if 'a'in d:close(aa,evalv(d['a'],tt),label+'acceleration')
   if 'speed'in d:close(np.linalg.norm(v),ev(d['speed'],tt),label+'speed')
   if 'v0'in d:close(derivative(rr,0),d['v0'],label+'v0');close(evalv(rr,0),d['r0'],label+'r0')
   if 'aT'in d:close(np.dot(v,aa)/np.linalg.norm(v),ev(d['aT'],tt),label+'aT');close(np.linalg.norm(cross(v,aa))/np.linalg.norm(v),ev(d['aN'],tt),label+'aN')
# Independently specified endpoint conditions for both transition polynomials.
for P,end in [(6*x**5-15*x**4+10*x**3,[1,0,0]),(3*x**5-8*x**4+6*x**3,[1,1,0])]:
 for order in range(3):close(float(s.diff(P,x,order).subs(x,0)),0,'transition start'+str(order));close(float(s.diff(P,x,order).subs(x,1)),end[order],'transition end'+str(order))
# Direct Cartesian re-insertion for surface intersections.
for tt in [.2,.7,1.3]:
 xx,yy,zz=2*math.cos(tt),2*math.sin(tt),4*math.sin(tt)*math.cos(tt);close(xx*xx+yy*yy,4,'13.1#42 cylinder');close(zz,xx*yy,'13.1#42 surface')
 xx,yy,zz=tt,(tt*tt-1)/2,(tt*tt+1)/2;close(zz*zz-yy*yy,xx*xx,'13.1#43 cone');close(zz-yy,1,'13.1#43 plane')
# Numerical physical conservation checks independent of symbolic authoring.
for h,v,ang in [(0,200,60),(100,200,60)]:
 g=9.8;vx=v*math.cos(math.radians(ang));vy=v*math.sin(math.radians(ang));T=(vy+math.sqrt(vy*vy+2*g*h))/g
 close(h+vy*T-g*T*T/2,0,'projectile ground');close(vx*vx+(vy-g*T)**2,v*v+2*g*h,'projectile energy')
close(float(s.limit(t*t/s.sin(t)**2,t,0)),1,'13.1#3 squared-sine component limit')
# All final patches must be source-backed, finite, uniquely keyed, with no duplicate string choices.
merged={}
for name in ['section01','section02','section03','section04','review','plus']:
 d=json.loads((HERE/(name+'.json')).read_text());assert not set(merged)&set(d);merged.update(d)
assert set(merged)==set(A.qs),(set(A.qs)-set(merged),set(merged)-set(A.qs))
for qid,entry in merged.items():
 for field in entry['grader'].get('parts',[entry['grader']]):
  if field['type']=='numeric':assert math.isfinite(field['answer'])
  else:assert field['answer'] in field['options'] and len(set(field['options']))==len(field['options'])
(HERE.parent/'chapter-13.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n')
(HERE/'independent-audit.json').write_text(json.dumps({'questions':len(merged),'fields':sum(len(e['grader'].get('parts',[e['grader']])) for e in merged.values()),'checks':checks,'passed':True,'limitations':['Drawings and proofs are not automatically assessed.','13.3#33 and13.4#2,#43 use deliberately broad source-sketch estimates.','ProblemsPlus8 explicitly identifies the elementary winding approximation and its physical-model limitation.']},indent=2)+'\n')
print('PASS',len(checks),'independent mathematical checks;',len(merged),'questions')
