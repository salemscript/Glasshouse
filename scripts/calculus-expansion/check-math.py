#!/usr/bin/env python3
"""High-precision checks independent of symbolic antiderivative construction."""
import math
import mpmath as mp
import sympy as S
from author import *
mp.mp.dps=70
checks=0

def near(actual,expected,tol=mp.mpf('1e-35')):
 global checks
 assert abs(actual-expected)<=tol*max(1,abs(expected)),(actual,expected)
 checks+=1
params={a:S.Integer(2),b:S.Integer(3),T:S.Integer(7),alpha:S.Rational(3,10)}
# Every new indefinite answer is checked with mpmath numerical differentiation.
for number,(f,F,sub,domain) in integrals.items():
 fn=S.lambdify(x,f.subs(params),'mpmath');primitive_fn=S.lambdify(x,F.subs(params),'mpmath')
 for point in [mp.mpf('.2'),mp.mpf('.4'),mp.mpf('.7')]:
  near(mp.diff(primitive_fn,point),fn(point))
 # Also compare a finite definite integral against endpoint primitive values.
 near(mp.quad(fn,[mp.mpf('.2'),mp.mpf('.7')]),primitive_fn(mp.mpf('.7'))-primitive_fn(mp.mpf('.2')))
# Absolute-log intervals and the negative real cube-root branch.
for z in [mp.mpf('2'),mp.mpf('3')]:
 near(mp.diff(lambda y:mp.log(abs(5-3*y))/-3,z),1/(5-3*z))
 near(mp.diff(lambda y:mp.log(abs(mp.asin(y))),mp.mpf('-.3')),1/(mp.sqrt(1-mp.mpf('.3')**2)*mp.asin(mp.mpf('-.3'))))
for z in [mp.mpf('2'),mp.mpf('3')]:
 real_cuberoot=lambda w:mp.sign(w)*abs(w)**(mp.mpf(1)/3)
 near(mp.diff(lambda y:-(real_cuberoot(4-y**3)**5)/5,z),z*z*real_cuberoot(4-z**3)**2)
# Definite integrals checked directly by quadrature, independently of the stored F.
for number,(f,F,left,right,value) in definite_integrals.items():
 fn=S.lambdify(x,f.subs(params),'mpmath');lo=mp.mpf(str(S.N(left.subs(params),70)));hi=mp.mpf(str(S.N(right.subs(params),70)))
 expected=mp.mpf(str(S.N(value.subs(params),70)))
 near(mp.quad(fn,[lo,(lo+hi)/2,hi]),expected,mp.mpf('1e-30'))
for number,(f,F,left,right,value) in averages.items():
 fn=S.lambdify(x,f,'mpmath');lo=mp.mpf(str(S.N(left,70)));hi=mp.mpf(str(S.N(right,70)))
 near(mp.quad(fn,[lo,(lo+hi)/2,hi])/(hi-lo),mp.mpf(str(S.N(value,70))),mp.mpf('1e-30'))
for c0 in c11:near(2*mp.sin(c0)-mp.sin(2*c0),4/mp.pi,mp.mpf('1e-14'))
for c0 in c12:near(2*c0*mp.exp(-c0*c0),a12,mp.mpf('1e-14'))
# Piecewise linear source graph, including its negative initial area.
vertices=[(0,-1),(2,1),(3,0),(4,2),(6,2),(7,1),(8,3)]
area=sum(mp.mpf(v1+v2)/2*(t2-t1) for (t1,v1),(t2,v2) in zip(vertices,vertices[1:]));near(area/8,mp.mpf(9)/8)
# Cooling, biomass, breathing and population averages by direct integration.
near(mp.quad(lambda z:20+75*mp.exp(-k*z),[0,30])/30,coffee,mp.mpf('1e-14'))
near(mp.quad(lambda z:2560*mp.exp(mp.mpf('.017185')*z),[0,50])/50,popavg,mp.mpf('1e-40'))
near(mp.quad(lambda z:5*(1-mp.cos(2*mp.pi*z/5))/(4*mp.pi),[0,5])/5,5/(4*mp.pi))
near(25000+mp.quad(lambda z:60000*mp.exp(-mp.mpf('.6')*z)/(1+5*mp.exp(-mp.mpf('.6')*z))**2,[0,20]),mp.mpf(str(S.N(fish,70))),mp.mpf('1e-35'))
near(mp.quad(lambda z:5000*(1-100/(z+10)**2),[2,4]),mp.mpf(85000)/21)
# Independent unit conversions for the baseball impulse and work.
mass=mp.mpf(5)/16/32;incoming=mp.mpf(90)*5280/3600;outgoing=-mp.mpf(110)*5280/3600
near(mass*(outgoing-incoming),-mp.mpf(275)/96)
near(-mass*(outgoing-incoming)/mp.mpf('.001'),mp.mpf(34375)/12)
near(mass*incoming**2/2,mp.mpf('85.078125'))
# Relay minimum and equal-time threshold, without the author's float-valued helper.
def relay_mp(U):
 pos=5*U-360
 return mp.mpf('.5')-10*mp.log((720+pos)/1000)-10*mp.log((10*U-pos)/(10*U))
near(relay_mp(mp.mpf(threshold)),direct,mp.mpf('1e-14'))
for U in [105,115]:
 pos=mp.mpf(5*U-360)
 fn=lambda z:mp.mpf('.5')-10*mp.log((720+z)/1000)-10*mp.log((10*U-z)/(10*U))
 near(mp.diff(fn,pos),0);assert mp.diff(fn,pos,2)>0;checks+=1
# Movie geometry: cosine-law and arctangent representations coincide at every row.
for i in range(21):
 z=mp.mpf(3*i);H=9+z*ca;top=31-z*sa;bottom=6-z*sa;at=mp.sqrt(H*H+top*top);bt=mp.sqrt(H*H+bottom*bottom)
 near(mp.acos((at*at+bt*bt-625)/(2*at*bt)),theta(z),mp.mpf('1e-40'))
 near(mp.diff(theta,z),theta_prime(z),mp.mpf('1e-40'))
near(theta_prime(mp.mpf(xopt)),0,mp.mpf('1e-16'))
# Composite Simpson comparison, independent of adaptive quadrature.
N=1000;step=mp.mpf(60)/N
simpson=(step/3)*(theta(0)+theta(60)+sum((4 if i%2 else 2)*theta(step*i) for i in range(1,N)))
near(simpson/60,mp.mpf(avgangle),mp.mpf('2e-10'))
assert best==3 and rows[best]>rows[best-1] and rows[best]>rows[best+1];checks+=1
near(5*mp.mpf(3)**3-3*mp.mpf(3)**2+3-6,105)
assert records['calculus-section-2-3-3']['fields'][0]['answer']==105
print(f'PASS: {checks} independent derivative, quadrature, root, graph-area, unit, impulse, optimization and geometry checks.')
