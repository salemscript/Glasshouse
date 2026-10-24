"""Independent verification from source coordinates, finite differences, polygonal geometry and frustums.
Does not import author scripts, their symbolic expressions or helper functions.
"""
import json, math, gzip, hashlib
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad
P=Path(__file__).parent;checks=[]
D={**json.loads((P/'section01.json').read_text()),**json.loads((P/'section02.json').read_text())}
def fields(sec,k,suffix=''):
 g=D[f'calculus-section-10-{sec}-{k}'+suffix]['grader'];return g.get('parts',[g])
def close(label,a,b,tol=1e-7):
 assert abs(float(a)-float(b))<=tol,(label,a,b,tol)
 checks.append({'label':label,'error':abs(float(a)-float(b)),'tolerance':tol})
def num(sec,k,i,expected,tol=1e-7,suffix=''):
 close(f'{sec}.{k} field{i}',fields(sec,k,suffix)[i]['answer'],expected,tol)
def symbolic(f,tv=0):
 z=f['answer'].replace('^','**').replace('·','*').replace('√(','sqrt(').replace('ln(','log(').replace('arcsin(','asin(').replace('arctan(','atan(')
 return float(sp.sympify(z,locals={'t':sp.Symbol('t')}).subs('t',tv))
def deriv(fn,t,h=1e-5):return (fn(t-2*h)-8*fn(t-h)+8*fn(t+h)-fn(t+2*h))/(12*h)
# All source IDs and field contracts.
root=P.parents[2];qs=json.loads(gzip.decompress((root/'site/questions/calculus.json.gz').read_bytes()))
expected={q['id'] for q in qs if q['chapter']==10 and q['section'] in ['10.1','10.2']}
# Bank uses integer section identifiers in some snapshots; derive stable identifier prefixes.
expected={q['id'] for q in qs if q['chapter']==10 and (q['id'].startswith('calculus-section-10-1-') or q['id'].startswith('calculus-section-10-2-'))}
assert set(D)==expected and len(D)==137
for id,v in D.items():
 fs=v['grader'].get('parts',[v['grader']]);assert len(fs)==v['objectiveFieldCount']
 for f in fs:
  if f['type']=='choice':assert f['answer'] in f['options'] and len(f['options'])==len(set(f['options']))
  else:assert math.isfinite(f['answer'])
# Section1 coordinate samples independently evaluated using scalar arithmetic.
for k,fn,ts in [(1,lambda t:(1-t*t,2*t-t*t),[-1,0,1,2]),(2,lambda t:(t**3+t,t*t+2),[-2,-1,0,1,2]),(3,lambda t:(t+math.sin(t),math.cos(t)),[-math.pi,-math.pi/2,0,math.pi/2,math.pi]),(4,lambda t:(math.exp(-t)+t,math.exp(t)-t),[-2,-1,0,1,2])]:
 for j,tv in enumerate(ts):
  xx,yy=fn(tv);num(1,k,2*j,xx);num(1,k,2*j+1,yy)
for j in range(9):
 xx=fields(1,30)[2*j]['answer'];yy=fields(1,30)[2*j+1]['answer'];close('10.1#30 first cubic '+str(j),yy,xx**3-4*xx);close('10.1#30 second cubic '+str(j),xx,yy**3-4*yy)
# Geometric elimination identities sampled independently.
for tv in [-2,-.4,.2,1.2,2.7]:
 xx=2*tv*tv/(1+tv*tv);yy=2*tv**3/(1+tv*tv);close('cissoid '+str(tv),yy*yy,xx**3/(2-xx))
 xx=2/math.tan(tv);yy=2*math.sin(tv)**2;close('witch '+str(tv),yy,8/(xx*xx+4))
 xx=tv**3;yy=tv*tv;close('semicubical '+str(tv),yy**3,xx*xx)
 for aa in [2,3,4,7/3]:
  xx=(aa-1)*math.cos(tv)+math.cos((aa-1)*tv);yy=(aa-1)*math.sin(tv)-math.sin((aa-1)*tv)
  if aa==4:close('astroid x '+str(tv),xx,4*math.cos(tv)**3);close('astroid y '+str(tv),yy,4*math.sin(tv)**3)
  rr=math.hypot(xx,yy);assert abs(abs(aa-1)-1)-1e-12<=rr<=abs(aa-1)+1+1e-12
num(1,46,0,2*500*math.sin(math.pi/6)/9.8);num(1,46,1,500*math.cos(math.pi/6)*(2*500*math.sin(math.pi/6)/9.8));num(1,46,2,(500*math.sin(math.pi/6))**2/(2*9.8))
# Parameterized tangent slopes: independent high-order finite differences.
for k,fx,fy,tv in [(3,lambda t:t**3+1,lambda t:t**4+t,-1),(4,math.sqrt,lambda t:t*t-2*t,4),(5,lambda t:t*math.cos(t),lambda t:t*math.sin(t),math.pi),(6,lambda t:math.exp(t)*math.sin(math.pi*t),lambda t:math.exp(2*t),0),(7,lambda t:1+math.log(t),lambda t:t*t+2,1),(8,lambda t:1+math.sqrt(t),lambda t:math.exp(t*t),1),(9,lambda t:t*t-t,lambda t:t*t+t+1,1),(10,lambda t:math.sin(math.pi*t),lambda t:t*t+t,1)]:
 m=deriv(fy,tv)/deriv(fx,tv);num(2,k,0,m,2e-7);num(2,k,1,fy(tv)-m*fx(tv),2e-7)
# Derivative formulas checked against source functions without symbolic differentiation.
funcs={1:(lambda t:t/(1+t),lambda t:math.sqrt(1+t)),2:(lambda t:t*math.exp(t),lambda t:t+math.sin(t)),11:(lambda t:t*t+1,lambda t:t*t+t),12:(lambda t:t**3+1,lambda t:t*t-t),13:(math.exp,lambda t:t*math.exp(-t)),14:(lambda t:t*t+1,lambda t:math.exp(t)-1),15:(lambda t:t-math.log(t),lambda t:t+math.log(t)),16:(math.cos,lambda t:math.sin(2*t))}
for k,(fx,fy) in funcs.items():
 for tv in ([.3,.7,1.4,2.4] if k==16 else [.4,.7,1.3,2.]):
  m=deriv(fy,tv)/deriv(fx,tv);close('Slope '+str(k)+' at '+str(tv),symbolic(fields(2,k)[0],tv),m,2e-6)
  if k>=11:
   def slope(q):return deriv(fy,q)/deriv(fx,q)
   dd=deriv(slope,tv,h=.0005)/deriv(fx,tv);close('Second derivative '+str(k)+' at '+str(tv),symbolic(fields(2,k)[1],tv),dd,2e-4)
# Extrema verified with coordinate values and neighboring comparisons.
z=6**(-.2);num(2,21,0,z-z**6);num(2,21,1,math.exp(z))
z=-4**(-1/3);w=2**(-1/3)
for i,val in enumerate([z**4-2*z,z+z**4,w**4-2*w,w+w**4]):num(2,22,i,val)
num(2,29,0,4);num(2,29,1,0)
# Integral areas using Cartesian slices, independently from parameter integrals.
close('Area32',symbolic(fields(2,32)[0]),quad(lambda y:2*y*y-y**4,0,math.sqrt(2))[0])
close('Area33',symbolic(fields(2,33)[0]),quad(lambda xx:2*(xx-1)**(1/3)-(xx-1)**(2/3),1,9)[0])
area=quad(lambda xx:2*math.sqrt(xx)*(3-xx),0,3)[0]
close('Loop area36',symbolic(fields(2,36)[0]),area)
close('Loop volume36',symbolic(fields(2,36)[1]),quad(lambda xx:math.pi*xx*(3-xx)**2,0,3)[0])
num(2,36,2,quad(lambda xx:2*xx*math.sqrt(xx)*(3-xx),0,3)[0]/area);num(2,36,3,0)
# Polygonal arc lengths with 400,000 segments avoid reusing author speed formulas.
curves={37:(lambda t:t+np.exp(-t),lambda t:t-np.exp(-t),0,2),38:(lambda t:t*t-t,lambda t:t**4,1,4),39:(lambda t:t-2*np.sin(t),lambda t:1-2*np.cos(t),0,4*math.pi),40:(lambda t:t+np.sqrt(t),lambda t:t-np.sqrt(t),0,1),41:(lambda t:1+3*t*t,lambda t:4+2*t**3,0,1),42:(lambda t:np.exp(t)-t,lambda t:4*np.exp(t/2),0,2),43:(lambda t:t*np.sin(t),lambda t:t*np.cos(t),0,1),44:(lambda t:3*np.cos(t)-np.cos(3*t),lambda t:3*np.sin(t)-np.sin(3*t),0,math.pi),45:(lambda t:np.exp(t)*np.cos(t),lambda t:np.exp(t)*np.sin(t),0,math.pi),46:(lambda t:np.cos(t)+np.log(np.tan(t/2)),np.sin,math.pi/4,3*math.pi/4),47:(lambda t:np.sin(t)+np.sin(1.5*t),np.cos,0,4*math.pi),48:(lambda t:3*t-t**3,lambda t:3*t*t,-math.sqrt(3),math.sqrt(3)),55:(lambda t:11*np.cos(t)-4*np.cos(5.5*t),lambda t:11*np.sin(t)-4*np.sin(5.5*t),0,4*math.pi)}
for k,(fx,fy,lo,hi) in curves.items():
 ts=np.linspace(lo,hi,400001);xx=fx(ts);yy=fy(ts);L=np.hypot(np.diff(xx),np.diff(yy)).sum();f=fields(2,k)[1];expected=f['answer'] if f['type']=='numeric' else symbolic(f)
 close('Independent polygonal length '+str(k),L,expected,1e-5)
# Simpson-rule explicit sums, distinct from quadrature or exact length.
v=[math.hypot(1-math.exp(t),1+math.exp(t)) for t in range(-6,7,2)]
num(2,49,0,2/3*(v[0]+4*v[1]+2*v[2]+4*v[3]+2*v[4]+4*v[5]+v[6]))
ts=[math.pi/4+i*math.pi/16 for i in range(5)];v=[math.hypot(-2/math.sin(t)**2,4*math.sin(t)*math.cos(t)) for t in ts]
num(2,50,0,math.pi/48*(v[0]+4*v[1]+2*v[2]+4*v[3]+v[4]))
for k,fx,fy,hi,mult in [(51,lambda t:np.sin(t)**2,lambda t:np.cos(t)**2,3*math.pi,6),(52,lambda t:np.cos(t)**2,np.cos,4*math.pi,4)]:
 ts=np.linspace(0,hi,480001);L=np.hypot(np.diff(fx(ts)),np.diff(fy(ts))).sum();close('Retraced distance '+str(k),symbolic(fields(2,k)[0]),L,1e-6);close('Retraced geometric length '+str(k),symbolic(fields(2,k)[1]),L/mult,1e-6)
# Surface area from sums of conical-frustum areas, independent of analytic integrands.
surfaces={57:(lambda t:t*np.sin(t),lambda t:t*np.cos(t),0,math.pi/2,'x'),58:(np.sin,lambda t:np.sin(2*t),0,math.pi/2,'x'),59:(lambda t:t+np.exp(t),lambda t:np.exp(-t),0,1,'x'),60:(lambda t:t*t-t**3,lambda t:t+t**4,0,1,'x'),61:(lambda t:t**3,lambda t:t*t,0,1,'x'),62:(lambda t:2*t*t+1/t,lambda t:8*np.sqrt(t),1,3,'x'),65:(lambda t:3*t*t,lambda t:2*t**3,0,5,'y'),66:(lambda t:np.exp(t)-t,lambda t:4*np.exp(t/2),0,1,'y')}
for k,(fx,fy,lo,hi,axis) in surfaces.items():
 ts=np.linspace(lo,hi,400001);xx=fx(ts);yy=fy(ts);rad=yy if axis=='x' else xx;A=(math.pi*(rad[1:]+rad[:-1])*np.hypot(np.diff(xx),np.diff(yy))).sum();f=fields(2,k)[1];val=f['answer'] if f['type']=='numeric' else symbolic(f)
 close('Independent frustum surface '+str(k),A,val,max(1e-5,abs(val)*2e-10))
for k,fx,fy,expected in [(63,lambda t:np.cos(t)**3,lambda t:np.sin(t)**3,6*math.pi/5),(64,lambda t:2*np.cos(t)-np.cos(2*t),lambda t:2*np.sin(t)-np.sin(2*t),128*math.pi/5)]:
 ts=np.linspace(0,math.pi/2 if k==63 else math.pi,400001);xx=fx(ts);yy=fy(ts);A=(math.pi*(yy[1:]+yy[:-1])*np.hypot(np.diff(xx),np.diff(yy))).sum();close('Geometric symbolic surface '+str(k),A,expected,1e-7)
close('Curvature70',symbolic(fields(2,70)[0]),2/5**1.5);num(2,70,1,0);num(2,70,2,0);num(2,70,3,2);num(2,71,0,.25);num(2,72,0,0)
# Grazing area from the actual boundary polygon with the silo disk removed.
phi=np.linspace(-math.pi/2,math.pi/2,100001);xx=1+math.pi*np.cos(phi);yy=math.pi*np.sin(phi)
theta=np.linspace(0,math.pi,100001);ell=math.pi-theta;ux=np.cos(theta)-ell*np.sin(theta);uy=np.sin(theta)+ell*np.cos(theta)
xx=np.concatenate([xx,ux,ux[::-1]]);yy=np.concatenate([yy,uy,-uy[::-1]])
area=.5*np.sum(xx*np.roll(yy,-1)-yy*np.roll(xx,-1))-math.pi
close('Cow wrapping polygon area',area,5*math.pi**3/6,2e-8)
# Bézier endpoint/tangent and nontrivial loop tests using Bernstein scalar evaluation.
suf='-project-laboratory-project-bézier-curves-1'
def bez(t,ps):return sum(w*np.array(p) for w,p in zip([(1-t)**3,3*t*(1-t)**2,3*t*t*(1-t),t**3],ps))
ps=[(4,1),(28,48),(50,42),(40,5)]
for t in [0,.1,.3,.5,.9,1]:
 pt=bez(t,ps)
 for j in [0,1]:close('Bezier formula '+str(t)+' component'+str(j),symbolic(fields(2,1,suf)[j],t),pt[j])
num(2,2,2,47/24,suffix=suf);num(2,2,3,37/10,suffix=suf)
fs=fields(2,3,suf);u,v=fs[1]['answer'],fs[2]['answer'];assert 0<u<v<1
ps=[(4,1),(80,20),(50,42),(40,5)];p=bez(u,ps);q=bez(v,ps)
for j in [0,1]:close('Bezier distinct-parameter loop component'+str(j),p[j],q[j]);close('Bezier loop point field'+str(j),fs[3+j]['answer'],p[j])
report={'questions':137,'fields':sum(v['objectiveFieldCount'] for v in D.values()),'checks':len(checks),'missing':[],'methods':['Source parameter functions evaluated independently','High-order finite differences for slopes and second derivatives','Cartesian slice integration for areas','400000-segment polygonal arc lengths','400000 conical-frustum sums for surfaces','Explicit Simpson weighted sums','Involute grazing-boundary polygon','Bernstein loop and endpoint evaluation'],'checksDetail':checks,'sourceSHA256':hashlib.sha256((root/'site/books/calculus/chapter-10.pdf').read_bytes()).hexdigest()}
(P/'sections01-02-independent-audit.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k not in ['checksDetail','methods']})
