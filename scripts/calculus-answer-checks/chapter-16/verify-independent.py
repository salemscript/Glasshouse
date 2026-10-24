"""Independent closed forms, alternate projections, source derivatives and topology checks."""
import json,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad,dblquad
HERE=Path(__file__).parent;data=json.loads((HERE.parent/'chapter-16.json').read_text());checks=[]
pi=math.pi;E=math.e;sq=math.sqrt

def check(sec,num,expected,index=0,label='independent calculation'):
 qid=f'calculus-section-16-{sec}-{num}' if isinstance(sec,int) else f'calculus-chapter-16-{sec}-{num}'
 fs=data[qid]['grader'].get('parts',[data[qid]['grader']]);got=fs[index]['answer'];tol=max(2e-7,abs(float(expected))*3e-8)
 assert isinstance(got,(int,float)) and abs(got-float(expected))<tol,(qid,index,got,expected)
 checks.append(dict(id=qid,field=index,expected=float(expected),method=label))
for k,val in {1:4*(10*sq(10)-1)/3,2:(73**1.5-125)/48,3:8192/5,4:5*quad(lambda t:(2+3*t)*math.exp(4*t),0,1)[0],5:pi**6/3+2*pi,6:E-1/E,7:5/2,8:83/3,9:sq(2)/3,10:107*sq(14)/12,11:(math.exp(6)-1)*sq(14)/12,12:sq(5)*(8*pi**3/3+2*pi),13:2*(E-1)/5,14:722/15,15:35/3,16:2,19:1/20,20:8,21:1.2-math.cos(1)-math.sin(1),22:0,28:0,29:11/8-1/E,30:-2,32:0,39:2*pi*pi,40:7/3+(E*E-E)/2,45:185*90,46:(185-4.5)*90,48:160*pi/100}.items():check(2,k,val)
for k,val in {1:40,2:6,11:16,12:9,13:-9,14:-1,15:77,16:5,17:4,18:math.sin(1)-2,19:4/E,20:-2,23:31/4,24:26}.items():check(3,k,val,1 if k in range(12,21) else 1 if k==11 else 0)
# In12–18 the potential precedes integral;19–20 same structure.
for k,val in {1:120,2:-32*pi,3:2/3,4:22/105,5:4*(E**3-1),6:2/3,7:1/3,8:0,9:-24*pi,10:195*pi/2,11:-16/3,12:pi/2,13:4*pi,14:math.log(2)/2,15:0,16:7*pi,17:-1/12,18:625*pi/8,19:3*pi,20:30*pi,27:0,28:12}.items():
 check(4,k,val)
 if k<=4 or k in(15,16):check(4,k,val,1)
check(4,21,4.5,2)
for k,val in {39:3*sq(14),40:4*sq(22),41:pi*sq(14),42:sq(2)/6,43:4*(3**2.5-2*2**2.5+1)/15,44:(18**1.5-2**1.5)/48,45:2*pi*(2*sq(2)-1)/3,46:2*sq(18)+math.log((4+sq(18))/sq(2)),47:pi*(65**1.5-1)/6,48:pi*(sq(2)+math.asinh(1))/2,49:4,52:pi*quad(lambda w:sq(1+4*w*math.sin(w)**2),0,1)[0],53:pi*quad(lambda w:sq(1+4*w/(w+2)**2),0,1)[0],61:4*pi,62:16}.items():check(6,k,val)
check(6,55,4*sum(sq(1+4*(x*x+y*y)/(1+x*x+y*y)**4) for x in (1,3,5) for y in(1,3)),0)
check(6,55,dblquad(lambda y,x:sq(1+4*(x*x+y*y)/(1+x*x+y*y)**4),0,6,lambda x:0,lambda x:4)[0],1)
assert 'smaller' in data['calculus-section-16-6-55']['grader']['parts'][2]['answer']
for k,val in {1:8*sum(math.cos(t) for t in(1,2,3)),2:18*pi,3:900*pi,4:-80*pi,5:11*sq(14),6:sq(2)/10,7:2*(2*sq(2)-1)/3,8:pi/sq(2),9:171*sq(14),10:4,11:sq(21)/3,14:625*pi*sq(2),15:(21**1.5-17**1.5)/12,16:pi*(2/3-5*sq(2)/12),17:16*pi,18:2*pi+4,19:0,20:241*pi,21:4,22:pi,24:-1712*pi/15,25:72*pi,26:-32*pi/3,27:0,28:pi*pi/2,29:48,30:4*pi,31:2*pi+8/3,32:-1/6,40:108*pi*sq(2),43:0,44:0,47:1248*pi}.items():check(7,k,val)
# Alternate graph projection, avoiding the authoring parametrization.
check(7,23,dblquad(lambda y,x:2*x*x*y+2*y*y*(4-x*x-y*y)+x*(4-x*x-y*y),0,1,lambda x:0,lambda x:1)[0])
check(7,34,dblquad(lambda y,x:x**3*y**3*sq(1+4*x*x*y**4+4*x**4*y*y),0,1,lambda x:0,lambda x:2)[0])
for k,val in {2:0,3:16*pi,4:0,5:0,6:0,7:-1,8:1/24,9:-2/3,10:pi,11:81*pi/2,12:pi,13:-32*pi,14:8*pi,15:-pi,17:3,18:pi}.items():
 check(8,k,val)
 if k in(13,14,15):check(8,k,val,1)
for k,val in {1:4.5,2:2430*pi,3:256*pi/3,4:36*pi,5:4.5,7:9*pi/2,8:384*pi/5,9:0,11:pi,12:-12*pi,13:2*pi,16:19*pi*pi/64,17:13*pi/20,18:3*pi/2,24:4*pi/3}.items():
 check(9,k,val)
 if k<=4:check(9,k,val,1)
for k,val in {2:(5*sq(5)-1)/12,3:6*sq(10),4:0,5:4/15,6:E-9/70,8:pi/4,9:11/12-4/E,13:0,14:2,15:0,16:3,17:-8*pi,25:(27-5*sq(5))/6,28:32*pi*sq(3),29:-64*pi/3,30:pi/2,31:0,32:-4*pi,33:-.5,34:11*pi,35:4*pi,36:4*pi,37:-4,38:4*pi,39:21}.items():check('review',k,val)
check('review',10,1.5*pi-4.5);check('review',10,-.75*pi,1)
# Remaining numeric fields: independent quadrature, moments and dimensional formulas.
check(1,33,2+.01*4);check(1,33,1+.01*3,1);check(1,34,1+.05,0);check(1,34,3-.05,1)
check(2,23,quad(lambda t:2*math.sin(t)*math.cos(t)*sq(math.sin(t)**2+math.sin(t)*math.cos(t))+math.cos(t)/math.sin(t)*math.cos(2*t),pi/6,pi/3)[0])
check(2,24,quad(lambda t:math.sin(t)*math.cos(t)*math.exp(math.sin(t))-math.tan(t)*math.sin(t)**2*math.exp(math.cos(t))+math.tan(t)*math.exp(math.tan(t)),0,pi/4)[0])
check(2,25,quad(lambda t:t**5*math.atan(sq(t))*sq(4*t*t+9*t**4+1/(4*t)),1,2)[0])
check(2,26,quad(lambda t:t**4*math.log(3+3*t+t*t)*sq(9+4*t*t+16*t**6),-1,1)[0])
check(2,27,3*pi+2/3)
check(2,31,21*sq(2)*(1-math.exp(-14*pi))/16*(2/65-1/193-1/449))
check(2,41,7/3);check(2,33,4/pi,1);check(2,33,0,2)
check(2,35,0,1);check(2,35,0,2);check(2,35,3*pi,3)
mass=sq(2)*quad(lambda t:t*t+1,0,2*pi)[0];check(2,36,mass)
for i,fn in enumerate([lambda t:t,math.cos,math.sin],1):check(2,36,sq(2)*quad(lambda t:fn(t)*(t*t+1),0,2*pi)[0]/mass,i)
check(2,47,0);check(2,51,8*2+6*1)
check(3,35,pi,1);check(3,35,-pi,2);check(3,36,6.67e-11*5.97e24*1.99e30*(1/(1.47*10**11)-1/(1.52*10**11)),1)
check(5,30,3);check(5,32,3,1)
check(6,57,3/16*((11*sq(126)+5*math.asinh(11/sq(5)))-(3*sq(14)+5*math.asinh(3/sq(5)))))
check(6,54,dblquad(lambda y,x:sq(1+4*x*x/(1+y*y)**2+4*y*y*(1+x*x)**2/(1+y*y)**4),-1,1,lambda x:-1+abs(x),lambda x:1-abs(x))[0])
check(6,56,18*dblquad(lambda p,q:(1-q)**1.5*sq(q+p*(1-p)*(1-q)),0,1,lambda q:0,lambda q:1,epsabs=1e-10)[0])
check(6,58,dblquad(lambda theta,r:6*r*sq(1+r*r*math.cos(theta)**2+4*r*r*math.sin(theta)**2/9),0,2,lambda r:0,lambda r:2*pi)[0],3)
check(7,12,dblquad(lambda y,x:y*sq(1+x+y),0,1,lambda x:0,lambda x:1)[0])
check(7,13,pi*quad(lambda r:r**3*sq(1+4*r*r),0,1)[0])
check(7,33,dblquad(lambda y,x:(x*x+y*y+x*x*math.exp(2*y))*sq(1+math.exp(2*y)*(1+x*x)),0,1,lambda x:0,lambda x:1)[0])
check(7,35,243/(2*sq(2))*dblquad(lambda theta,r:r**5*math.cos(theta)**2*math.sin(theta)**2*(1-r*r)**2*sq(1+r*r*(24*math.cos(theta)**2+12*math.sin(theta)**2)),0,1,lambda r:0,lambda r:2*pi)[0])
check(7,36,16*pi/3+160*math.sinh(.4)/3)
check(7,39,0);check(7,39,0,1);check(7,41,2*pi*sq(2)*quad(lambda z:z**3*(10-z),1,4)[0],1)
check(7,42,0);check(7,42,0,1);check(7,42,4.5,2)
check(9,15,quad(lambda x:sq(3-x*x)*(3.6-2*x**4),-1,1)[0],1);check(9,23,0)
check('review',7,110/3);check('review',15,0,1)
check('review',27,pi/8*((17**2.5-1)/5-(17**1.5-1)/3))
check('review',31,0,1);check('review',35,4*pi,1);check('review',24,0,2)
check('review',26,4*((3**7/7)*quad(lambda v:1/(1+v**4),0,3)[0]+(3**5/5)*quad(lambda u:u*u/(1+u**4),0,3)[0]),3)
(HERE/'independent-audit.json').write_text(json.dumps(dict(passed=len(checks),checks=checks),indent=2)+'\n');print('PASS',len(checks),'independent numeric checks')
