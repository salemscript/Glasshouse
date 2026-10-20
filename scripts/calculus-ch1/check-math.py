#!/usr/bin/env python3
"""Independent symbolic/numerical checks of the nontrivial computations and edge cases."""
from pathlib import Path
import math
import numpy as np
import sympy as s
import mpmath as mp

HERE=Path(__file__).parent
rows={p.stem:{line.split('\t')[0]:line.split('\t')[1:] for line in p.read_text().splitlines()} for p in HERE.glob('*.tsv')}
checks=0
def equal(a,b):
    global checks
    assert s.simplify(a-b)==0, (a,b)
    checks+=1
def near(a,b,tol=1e-8):
    global checks
    assert math.isclose(float(a),float(b),rel_tol=tol,abs_tol=tol), (a,b)
    checks+=1
def stated(section,n,fragment):
    global checks
    assert fragment in rows[section][str(n)][0], (section,n,fragment)
    checks+=1
x,a,h=s.symbols('x a h',real=True)
f=3*x*x-x+2
equal(f.subs(x,2),12);equal(f.subs(x,-2),16)
equal(s.expand(f.subs(x,a+1)),3*a*a+5*a+4)
equal(s.expand(f.subs(x,a)**2),9*a**4-6*a**3+13*a*a-4*a+4)
equal(((4+3*x-x*x).subs(x,3+h)-(4+3*x-x*x).subs(x,3))/h,-3-h)
equal(((a+h)**3-a**3)/h,3*a*a+3*a*h+h*h)
equal((1/x-1/a)/(x-a),-1/(a*x))
equal(((x+3)/(x+1)-2)/(x-1),-1/(x+1))
stated('section-1-1',30,'−1/(x+1)')

# Derive compositions from their original functions, then compare with the authored forms.
pairs={
33:(3*x+5,x*x+x,[3*x*x+3*x+5,9*x*x+33*x+30,9*x+20,x**4+2*x**3+2*x*x+x]),
34:(x**3-2,1-4*x,[(1-4*x)**3-2,9-4*x**3,(x**3-2)**3-2,16*x-3]),
35:(s.sqrt(x+1),4*x-3,[s.sqrt(4*x-2),4*s.sqrt(x+1)-3,s.sqrt(s.sqrt(x+1)+1),16*x-15]),
36:(s.sin(x),x*x+1,[s.sin(x*x+1),s.sin(x)**2+1,s.sin(s.sin(x)),(x*x+1)**2+1]),
37:(x+1/x,(x+1)/(x+2),[(2*x*x+6*x+5)/((x+2)*(x+1)),(x*x+x+1)/(x+1)**2,(x**4+3*x*x+1)/(x*(x*x+1)),(2*x+3)/(3*x+5)]),
38:(x/(1+x),s.sin(2*x),[s.sin(2*x)/(1+s.sin(2*x)),s.sin(2*x/(1+x)),x/(1+2*x),s.sin(2*s.sin(2*x))])}
for n,(f,g,expected) in pairs.items():
    for actual,want in zip([f.subs(x,g),g.subs(x,f),f.subs(x,f),g.subs(x,g)],expected):equal(actual,want)

# Physical models and regression: fit the supplied raw tables independently.
raw={
23:([4000,6000,8000,12000,16000,20000,30000,45000,60000],[14.1,13,13.4,12.5,12,12.4,10.5,9.4,8.2],-9.978545618789514e-5,13.95076407708521),
24:([50,55,60,65,70,75,80,85,90],[20,46,79,91,113,140,173,198,211],4.85666666666667,-220.966666666667),
25:([50.1,48.3,45.2,44.7,44.5,42.7,39.5,38],[178.5,173.6,164.8,163.7,168.3,165,155.4,155.8],1.88074246942391,82.64973853666984),
26:([50,400,500,900,1100,1600,1800,2000,3000],[2,6,5,10,26,42,37,38,50],.01878914405010438,.30480167014614),
27:([0,5,10,15,20,25],[60083,66533,70099,76784,84077,87302],1116.64,60188.33333333),
28:([0,2,4,6,8,10,12],[8.24,8.44,8.95,10.4,11.26,11.54,11.58],.330892857142857,8.07321428571428)}
for n,(xx,yy,m,b) in raw.items():
    # Centered normal equations differ from the polyfit used during drafting.
    xx=np.array(xx);yy=np.array(yy)
    slope=np.dot(xx-xx.mean(),yy-yy.mean())/np.dot(xx-xx.mean(),xx-xx.mean())
    near(slope,m);near(yy.mean()-slope*xx.mean(),b)
xx=np.arange(0,101,10);yy=np.array([48.3,51.1,55.2,57.4,62.5,65.6,66.6,67.1,70,71.8,73])
sl=np.dot(xx-xx.mean(),yy-yy.mean())/np.dot(xx-xx.mean(),xx-xx.mean())
near(yy.mean()+sl*(110-xx.mean()),77.55636363636)
stated('chapter-01-review','E21','77.56')
near(2**24/(12*5280),264.7919191919)
stated('section-1-4',25,'48 ft')
near(200*2**(-21/5),10.8818820412)
near(2*2**(-96/15),.0236830713517)
near(3*math.log2(500),26.897352853986)
near(math.log(81),4.39444915467244)
near(math.log(.5)/math.log(.818656),3.4641543814987)
near(2**36/63360,1084587.7010101)

# Numerical inverse checks over both domains, including the difficult cubic and sextic cases.
mp.mp.dps=60
def cbrt(v):return mp.sign(v)*abs(v)**(mp.mpf(1)/3)
for value in [-1,-.99,-.5,0,.1,1,2,10,100]:
    y=mp.sqrt(value**3+value**2+value+1)
    A=y*y/2-mp.mpf(10)/27
    inv=cbrt(A+mp.sqrt(A*A+mp.mpf(8)/729))+cbrt(A-mp.sqrt(A*A+mp.mpf(8)/729))-mp.mpf(1)/3
    near(inv,value,1e-10)
for value in [0,1e-4,.1,.3,.5,1,2,10,100]:
    value=mp.mpf(str(value));y=value**6+value**4;w=27*y/2-1
    z=(2*(mp.cos(mp.acos(w)/3) if y<=mp.mpf(4)/27 else mp.cosh(mp.acosh(w)/3))-1)/3
    near(mp.sqrt(max(z,mp.mpf(0))),value,1e-10)

# All piecewise absolute-value cases and repeated-composition domain exclusions.
for xx in np.linspace(-10,10,401):
    r=abs(xx)
    ans=-3 if r<=1 else 2*xx*xx-5 if r<=2 else 3
    near(abs(xx*xx-1)-abs(xx*xx-4),ans)
    for yy in [-2,-1,-.3,0,.3,1,2]:
        actual=abs(xx-yy)+abs(abs(xx)-abs(yy))<=2+1e-12
        expected=abs(xx-yy)<=1+1e-12 if xx*yy>=0 else max(abs(xx),abs(yy))<=1+1e-12
        assert actual==expected;(checks:=checks+1)
for n in range(8):
    for xx in [-5,-1,0,.5,1,1.01,1.3,3,10]:
        v=xx
        for _ in range(n+1):v=1/(2-v)
        near(v,((n+1)-n*xx)/((n+2)-(n+1)*xx))
    excluded={(j+2)/(j+1) for j in range(n+1)}
    assert len(excluded)==n+1
print(f'PASS: {checks} independent symbolic identities, table regressions, conversions, inverse branches, interval samples and recursive-composition checks.')
