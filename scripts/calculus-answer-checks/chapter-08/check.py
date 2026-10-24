#!/usr/bin/env python3
"""Independent numerical geometry/probability regressions against serialized checks.
Does not import author.py: uses high-precision derivatives, quadrature and moments.
"""
import json,math,hashlib
from pathlib import Path
import mpmath as m
import sympy as s
m.mp.dps=55
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
rows=json.loads((HERE.parent/'chapter-08.json').read_text());checks=[];failures=[]
def fields(sec,num):
 prefix=f'calculus-section-8-{sec}-{num}' if isinstance(sec,int) else f'calculus-chapter-08-{sec}-{num}'
 qs=[v for k,v in rows.items() if k==prefix or (sec in ['review','problems-plus'] and k.startswith(prefix+'-') and 'concept-check' not in k)]
 assert len(qs)==1,(prefix,len(qs));g=qs[0]['grader'];return g.get('parts',[g])
def value(f):
 if f['type']=='numeric':return m.mpf(str(f['answer']))
 z=s.sympify(f['answer'],locals={'ln':s.log,'arcsinh':s.asinh,'arcsin':s.asin,'arctan':s.atan});return m.mpf(str(s.N(z,55)))
def test(sec,num,label,expected,tol=m.mpf('1e-8')):
 fs=fields(sec,num);f=next((v for v in fs if v['label']==label),None);assert f,(sec,num,label)
 try:
  actual=value(f);delta=abs(actual-expected);ok=delta<=tol*max(1,abs(expected))
 except Exception as e:ok=False;delta=str(e);actual='parse error'
 record=dict(section=sec,number=num,label=label,expected=str(expected),actual=str(actual),absoluteError=str(delta),passed=ok)
 checks.append(record)
 if not ok:failures.append(record)
def length(f,lo,hi):return m.quad(lambda z:m.sqrt(1+m.diff(f,z)**2),[lo,(lo+hi)/2,hi])
def surface(f,lo,hi,axis='x'):return m.quad(lambda z:2*m.pi*(abs(f(z)) if axis=='x' else abs(z))*m.sqrt(1+m.diff(f,z)**2),[lo,(lo+hi)/2,hi])
p=m.pi
arcs={1:(lambda z:2*z-5,-1,3),2:(lambda z:m.sqrt(2-z*z),0,1),3:(m.sin,0,p),4:(lambda z:z*m.exp(-z),0,2),5:(lambda z:z-m.log(z),1,4),6:(lambda z:z*z-2*z,0,2),7:(lambda z:m.sqrt(z)-z,1,4),8:(lambda z:m.exp(z*z),-1,1),9:(lambda z:1+6*z**m.mpf('1.5'),0,1),10:(lambda z:(z*z-4)**m.mpf('1.5')/6,2,3),11:(lambda z:z**3/3+1/(4*z),1,2),12:(lambda z:z**4/8+1/(4*z*z),1,2),13:(lambda z:m.sqrt(z)*(z-3)/3,1,9),14:(lambda z:m.log(m.cos(z)),0,p/3),15:(lambda z:m.log(1/m.cos(z)),0,p/4),16:(lambda z:3+m.cosh(2*z)/2,0,1),17:(lambda z:z*z/4-m.log(z)/2,1,2),18:(lambda z:m.sqrt(z-z*z)+m.asin(m.sqrt(z)),0,1),19:(lambda z:m.log(1-z*z),0,m.mpf('.5')),20:(lambda z:1-m.exp(-z),0,2),21:(lambda z:z*z/2,-1,1),22:(lambda z:(z-4)**m.mpf('1.5'),5,8),23:(lambda z:z*z+z**3,1,2),24:(lambda z:z+m.cos(z),0,p/2),31:(m.exp,0,2),32:(lambda z:z**(m.mpf(4)/3),0,1),40:(lambda z:150-(z-50)**2/40,0,80),41:(lambda z:180-z*z/45,0,90)}
for n,(fn,lo,hi) in arcs.items():
 label='Arc length' if n in [1,2,21,22] else 'Length' if n<=8 else 'Exact length' if n<=20 or n in [31,32] else 'Computed length' if n in [23,24] else 'Distance'
 test(1,n,label,m.re(length(fn,m.mpf(lo),m.mpf(hi))))
# Physical surface area tests use numerical derivative of the ORIGINAL curve.
surfaces={7:(lambda z:z**3,0,2,'x'),8:(lambda z:m.sqrt(5-z),3,5,'x'),9:(lambda z:m.sqrt(z+1),0,3,'x'),10:(lambda z:m.sqrt(1+m.exp(z)),0,1,'x'),11:(lambda z:m.cos(z/2),0,p,'x'),12:(lambda z:z**3/6+1/(2*z),m.mpf('.5'),1,'x'),15:(lambda z:z**m.mpf('1.5')/3,0,12,'y'),18:(lambda z:z*z/4-m.log(z)/2,1,2,'y'),23:(lambda z:1/z,1,2,'x'),24:(lambda z:m.sqrt(1+z*z),0,3,'x'),25:(lambda z:z**3,0,1,'y'),26:(lambda z:m.log(z+1),0,1,'y')}
for n,(fn,lo,hi,axis) in surfaces.items():test(2,n,'Exact surface area' if n<=18 else 'Exact area',m.re(surface(fn,m.mpf(lo),m.mpf(hi),axis)))
for n,fn in [(13,lambda z:(z*z+2)**m.mpf('1.5')/3),(14,lambda z:1+2*z*z)]:test(2,n,'Exact surface area',m.quad(lambda z:2*p*z*m.sqrt(1+m.diff(fn,z)**2),[1,2]))
test(2,16,'Exact surface area',m.quad(lambda z:6*p*m.cos(z)**4*m.sin(z),[0,p/2]))
test(2,28,'Surface area',surface(lambda z:m.exp(-z),m.mpf(0),m.inf)) if False else None
# Infinite endpoint needs direct transformed integration, avoiding inf/2.
test(2,28,'Surface area',2*p*m.quad(lambda z:m.sqrt(1+z*z),[0,1]))
test(2,34,'Exact area',m.quad(lambda z:2*p*(4-z)*m.sqrt(1+4*z*z),[0,2]))
# Two independent cap-subtraction vs sliced-area calculations for PP7.
def slicearea(z):
 R2=1-z*z;a=1-z/m.sqrt(2)
 if z>=2*m.sqrt(2)/3:return p*R2
 return p*R2-4*(R2*m.acos(a/m.sqrt(R2))-a*m.sqrt(max(0,R2-a*a)))
capvolume=m.quad(slicearea,[0,1/m.sqrt(2),2*m.sqrt(2)/3,1])
expr=fields('problems-plus',7)[1]['answer'];calc=s.sympify(expr,locals={'b':s.Integer(1)});expected=m.mpf(str(s.N(calc,55)))
checks.append(dict(section='problems-plus',number=7,label='b=1 slice integral',expected=str(capvolume),actual=str(expected),passed=abs(expected-capvolume)<m.mpf('1e-20')))
if not checks[-1]['passed']:failures.append(checks[-1])
# Moments reconstructed from source geometry, including two-piece shapes.
def centroid(top,bot,lo,hi):
 A=m.quad(lambda z:top(z)-bot(z),[lo,hi]);return (m.quad(lambda z:z*(top(z)-bot(z)),[lo,hi])/A,m.quad(lambda z:(top(z)**2-bot(z)**2)/2,[lo,hi])/A)
centers={25:(lambda z:2*z,lambda z:0,0,1),26:(m.sqrt,lambda z:0,0,4),27:(m.exp,lambda z:0,0,1),28:(m.sin,lambda z:0,0,p),29:(m.sqrt,lambda z:z*z,0,1),30:(lambda z:2-z*z,lambda z:z,-2,1),31:(m.cos,m.sin,0,p/4),37:(lambda z:z**3-z,lambda z:z*z-1,-1,1)}
for n,args in centers.items():
 xc,yc=centroid(*args);test(3,n,'x̄',xc);test(3,n,'ȳ',yc)
for n,args in {15:(m.sqrt,lambda z:z/2,0,4),16:(m.sin,lambda z:0,p/4,3*p/4)}.items():
 xc,yc=centroid(*args);test('review',n,'x̄',xc);test('review',n,'ȳ',yc)
# Plate centroids compute force without integrating pressure strips.
for n,v in {3:m.mpf('62.4')*16*7,4:m.mpf('62.4')*25*(m.mpf(16)/3),5:9800*p*64*12,7:9800*m.sqrt(3)*(m.sqrt(3)/3),8:9800*6*m.mpf(16)/3}.items():test(3,n,'Hydrostatic force',v)
test(3,12,'a · Full-tank end force',m.mpf('64.6')*p*9*3)
test(3,12,'b · Half-full end force',m.mpf('64.6')*p*9/2*4/p)
# Economics separate geometric surplus / exact rate integrals.
test(4,1,'Total production cost',18000+m.quad(lambda z:m.mpf('.82')-m.mpf('.00003')*z+m.mpf('.000000003')*z*z,[0,4000]))
test(4,2,'Increase in revenue',m.quad(lambda z:48-m.mpf('.0012')*z,[5000,10000]))
test(4,4,'Consumer surplus',m.quad(lambda z:46*(20-m.sqrt(z)),[0,400]))
test(4,7,'Producer surplus',m.quad(lambda z:625-125-m.mpf('.002')*z*z,[0,500]))
test(4,9,'b · Maximum total surplus',1000*m.mpf('3.8')*171/2)
# Probability normalization and exact interval areas.
test(5,3,'b · P(X≤1/3)',m.quad(lambda z:30*z*z*(1-z)**2,[0,m.mpf(1)/3]))
test(5,6,'b · P(X>1)',m.quad(lambda z:m.mpf(2)/9*(3*z-z*z),[1,3]))
test(5,8,'b(i) · P(X<3)',m.quad(lambda z:z/30,[0,3]))
test(5,8,'b(ii) · P(3≤X≤8)',m.quad(lambda z:z/30,[3,6])+m.quad(lambda z:(10-z)/20,[6,8]))
test(5,8,'c · Mean',m.quad(lambda z:z*z/30,[0,6])+m.quad(lambda z:z*(10-z)/20,[6,10]))
test(5,13,'a · P(30≤T≤60)',m.quad(lambda z:z/1600,[30,40])+m.quad(lambda z:m.mpf(1)/20-z/1600,[40,60]))
test(5,21,'d · P(r≤4a₀)',m.quad(lambda z:4*z*z*m.exp(-2*z),[0,4]))
# Review expressions checked from independent geometry/calculus.
test('review',1,'Length',length(lambda z:4*(z-1)**m.mpf('1.5'),m.mpf(1),m.mpf(4)))
test('review',2,'Length',length(lambda z:2*m.log(m.sin(z/2)),p/3,p))
test('review',3,'Length',length(lambda z:z**3/3+1/(4*z),m.mpf(1),m.mpf(3)))
test('review',4,'a · Length',length(lambda z:z**4/16+1/(2*z*z),m.mpf(1),m.mpf(2)))
test('review',4,'b · Surface area',surface(lambda z:z**4/16+1/(2*z*z),m.mpf(1),m.mpf(2),'y'))
test('review',6,'a · y-axis area',surface(lambda z:z*z,m.mpf(0),m.mpf(1),'y'))
test('review',6,'b · x-axis area',surface(lambda z:z*z,m.mpf(0),m.mpf(1),'x'))
test('problems-plus',1,'Area',m.quad(lambda z:m.sqrt(4-(z-2)**2),[0,1]))
test('problems-plus',2,'x̄',m.quad(lambda z:2*z*m.sqrt(z**3-z**4),[0,1])/m.quad(lambda z:2*m.sqrt(z**3-z**4),[0,1]))
# Buffon needle integrals compute overlap probabilities directly over angle.
alpha=m.asin(m.mpf(4)/7)
test('problems-plus',12,'a · At least one line',2/p*(m.quad(lambda z:7*m.sin(z)/4,[0,alpha])+p/2-alpha))
test('problems-plus',12,'b · Two lines',2/p*m.quad(lambda z:(7*m.sin(z)-4)/4,[alpha,p/2]))
report=dict(sourceSHA256=hashlib.sha256((ROOT/'site/books/calculus/chapter-08.pdf').read_bytes()).hexdigest(),tests=len(checks),failures=failures,checks=checks)
(HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(len(checks),'independent regressions;',len(failures),'failures')
for f in failures:print(f)
assert not failures
