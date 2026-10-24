#!/usr/bin/env python3
"""Source-explicit regressions; checks stored answers without importing author.py."""
import json,re,math
from pathlib import Path
import sympy as S
import mpmath as mp
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[3];D=json.loads((ROOT/'scripts/calculus-answer-checks/chapter-05.json').read_text());x=S.symbols('x',real=True);R=S.Rational;pi=S.pi;mp.mp.dps=50
checks=[]
def near(a,b,label,tol=1e-8):
 a=float(a);b=float(b);assert abs(a-b)<=tol*max(1,abs(b)),(label,a,b);checks.append(label)
def read(t):
 t=re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)',lambda m:'^('+m[0].translate(str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻','0123456789-'))+')',t)
 t=t.replace('−','-').replace('·','*').replace('π','pi').replace('√','sqrt').replace('arctan','atan').replace('ln','log').replace('^','**')
 t=re.sub(r'log\|([^|]+)\|',r'log(Abs(\1))',t);t=re.sub(r'\|([^|]+)\|',r'Abs(\1)',t)
 return S.sympify(t,locals={**{v:x for v in ['x','u','t','r','s','y','p','w','z','θ']},'C':0,'e':S.E})
def g(sec,no):return D[f'calculus-section-5-{sec}-{no}']['grader']
def nums(sec,no):
 z=g(sec,no);return [a['answer'] for a in z.get('parts',[z]) if a['type']=='numeric']
# Every retained indefinite integral: numerical differentiation of answer vs source integrand.
for no in range(5,21):
 q=D[f'calculus-section-5-4-{no}'];src=q['nativePrompt'].splitlines()[1];raw=re.match(r'∫ \((.*)\) d.',src)[1];fn=S.lambdify(x,read(raw),'mpmath');F=S.lambdify(x,read(q['grader']['answer']),'mpmath')
 for z in ['.23','.57','.81']:
  z=mp.mpf(z);near(mp.diff(F,z),fn(z),f'5.4#{no} derivative at{z}')
# Every retained definite integral in5.4: source-bounds quadrature, not symbolic primitive reuse.
for no in range(21,47):
 q=D[f'calculus-section-5-4-{no}'];src=q['nativePrompt'].splitlines()[1];m=re.match(r'∫ from (.*?) to (.*?) \((.*)\) d.',src);lo,hi=map(lambda t:float(read(t)),m.group(1,2));expr=read(m[3]);fn=S.lambdify(x,expr,'numpy')
 points=[z for z in [0,.5,math.pi] if lo<z<hi]
 val=quad(fn,lo,hi,points=points,epsabs=1e-9,limit=200)[0];near(val,q['grader']['answer'],f'5.4#{no} quadrature',2e-8)
# FTC derivatives directly from source endpoints, compared to numerical derivative of the integral itself.
ftc={7:(S.sqrt(x+x**3),0,x),8:(S.log(1+x*x),1,x),9:((x-x*x)**8,5,x),10:(S.sqrt(x)/(1+x),0,x),11:(S.sqrt(1+S.sec(x)),x,0),12:(x**3*S.sin(x),x,2),13:(S.log(x),1,S.exp(x)),14:(x*x/(1+x**4),1,S.sqrt(x)),15:(x/(1+x**3),1,3*x+2),16:(S.cos(x)**2,0,x**4),17:(x*S.tan(x),S.sqrt(x),pi/4),18:(S.sqrt(1+x*x),S.sin(x),1),59:((x*x-1)/(x*x+1),2*x,3*x),60:(x*S.sin(x),1-2*x,1+2*x),61:(S.exp(x*x),x,x*x),62:(S.atan(x),S.sqrt(x),2*x),63:(S.log(1+2*x),S.cos(x),S.sin(x))}
for no,(expr,lo,hi) in ftc.items():
 fn=S.lambdify(x,expr,'mpmath');a=S.lambdify(x,S.sympify(lo),'mpmath');b=S.lambdify(x,S.sympify(hi),'mpmath');ans=S.lambdify(x,read(g(3,no)['answer']),'mpmath')
 for z in [mp.mpf('.25'),mp.mpf('.45')]:near(mp.diff(lambda t:mp.quad(fn,[a(t),b(t)]),z),ans(z),f'5.3#{no} numericalFTC at{z}',1e-8)
# Explicit source transcription for5.3 definite integrals19–44.
ints={19:(x*x+2*x-4,1,3),20:(x**100,-1,1),21:(R(4,5)*x**3-R(3,4)*x*x+R(2,5)*x,0,2),22:(1-8*x**3+16*x**7,0,1),23:(S.sqrt(x),1,9),24:(x**(-R(2,3)),1,8),25:(S.sin(x),pi/6,pi),26:(S.E,-5,5),27:((x+2)*(x-3),0,1),28:((4-x)*S.sqrt(x),0,4),29:((2+x*x)/S.sqrt(x),1,4),30:((3*x-2)*(x+1),-1,2),31:(S.csc(x)*S.cot(x),pi/6,pi/2),32:(S.csc(x)**2,pi/4,pi/3),33:((1+x)**3,0,1),34:(2*S.sin(x)-S.exp(x),0,3),35:((x**3+3*x**6)/x**4,1,2),36:(S.sqrt(3/x),1,18),37:(x**S.E+S.exp(x),0,1),38:(S.cosh(x),0,1),39:(8/(1+x*x),1/S.sqrt(3),S.sqrt(3)),40:((x**3-2*x*x-x)/x**2,1,3),41:(2**x,0,4),42:(4/S.sqrt(1-x*x),R(1,2),1/S.sqrt(2))}
for no,(expr,lo,hi) in ints.items():
 near(quad(S.lambdify(x,expr,'numpy'),float(lo),float(hi),epsabs=1e-9)[0],g(3,no)['answer'],f'5.3#{no} source quadrature')
near(g(3,43)['answer'],0,'piecewise trig43');near(g(3,44)['answer'],R(28,3),'piecewise polynomial44')
# Every5.1/5.2 finite rectangle table is independently recomputed at different precision.
for sec,no,expr,lo,hi,Ns,kinds in [(1,3,1/x,1,2,[4],['R','L']),(1,4,S.sin(x),0,pi/2,[4],['R','L']),(1,5,1+x*x,-1,2,[3,6],['R','L','M']),(1,9,x**4,0,1,[10,30,50,100],['R']),(1,10,S.cos(x),0,pi/2,[10,30,50,100],['R']),(1,11,1/(1+x*x),0,1,[10,30,50],['L','R']),(1,12,S.log(x),1,4,[10,30,50],['L','R']),(2,9,S.sin(S.sqrt(x)),0,8,[4],['M']),(2,10,S.sqrt(1+x**3),0,1,[5],['M']),(2,11,x/(x+1),0,2,[5],['M']),(2,12,x*S.sin(x)**2,0,pi,[4],['M'])]:
 vals=[];fn=S.lambdify(x,expr,'mpmath');a=mp.mpf(str(S.N(lo,50)));b=mp.mpf(str(S.N(hi,50)))
 pairs=[(N,k) for k in kinds for N in Ns] if no==5 and sec==1 else [(N,k) for N in Ns for k in kinds]
 for N,kind in pairs:
  h=(b-a)/N;offset={'R':1,'L':0,'M':mp.mpf('.5')}[kind];vals.append(mp.fsum(fn(a+(i+offset)*h)*h for i in range(N)))
 for i,v in enumerate(vals):near(nums(sec,no)[i],v,f'5.{sec}#{no} rectangle{i}')
# Problems Plus: independent optimization, derivatives, planar geometry, limit estimates.
def pp(no):return D[f'calculus-chapter-05-problems-plus-{no}-problems-plus-0']['grader']
def pnums(no):return [z['answer'] for z in pp(no).get('parts',[pp(no)]) if z['type']=='numeric']
near(pnums(1)[0],math.pi/2,'PP1 differentiation')
near(pnums(2)[1],quad(lambda t:t+1/t,.5,2)[0],'PP2 min integral')
for a in [.1,.3,.49,.51,1,5]:assert quad(lambda t:t+1/t,a,a+1.5)[0]>=pnums(2)[1]-1e-9;checks.append('PP2 comparison '+str(a))
for cc in [.1,.5,1,3]:near(quad(lambda t:(2*cc*t-t*t)/cc**3,0,2*cc)[0],pnums(4)[0],'PP4 equal areas')
for t in [.02,.01,.005]:near(quad(lambda z:math.sin(z*z),0,t)[0]/(t*math.sin(t*t)/2),pnums(8)[0],'PP8 limit '+str(t),1e-6)
near(pnums(16)[3],quad(lambda z:4-z*z-z-2,-2,1)[0],'PP16 segment')
pts=[(-2,0),(1,3),(-.5,3.75)];det=abs(sum(pts[i][0]*pts[(i+1)%3][1]-pts[i][1]*pts[(i+1)%3][0] for i in range(3)))/2;near(det,pnums(16)[4],'PP16 determinant')
near(pnums(18)[0],8*quad(lambda y:(1-y*y)/2-y,0,math.sqrt(2)-1)[0],'PP18 octant')
for cc in [-2,-1.5,-1,-.5,0,.5,1,2]:
 val=quad(lambda z:min((z-cc)**2,(z-cc-2)**2),0,1,points=[cc+1] if -1<cc<0 else None)[0];assert pnums(20)[0]-1e-9<=val<=pnums(20)[1]+1e-9;checks.append('PP20 bounds '+str(cc))
report={'passed':True,'checks':len(checks),'tests':checks,'limits':'Graph estimates, drawings, proofs and essays require the source review and explicit limited grading flags; numerical checks do not certify those tasks.'}
(ROOT/'scripts/calculus-answer-checks/chapter-05/math-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(checks),'independent checks')
