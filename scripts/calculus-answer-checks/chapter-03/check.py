#!/usr/bin/env python3
"""Independent source-equation checks for new Chapter3 answer contracts.
This is not a proof that every transcribed explanation is correct.
"""
import json,gzip,math,re,hashlib
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
ROOT=Path(__file__).resolve().parents[3]
patch=json.loads((Path(__file__).parents[1]/'chapter-03.json').read_text())['questions']
review=json.loads((Path(__file__).parent/'review.json').read_text())['questions']
qs=json.loads(gzip.decompress((ROOT/'site/questions/calculus.json.gz').read_bytes()))
source={q['id']:q for q in qs if q['chapter']==3}
checks=0
def assert_(condition,detail):
 global checks;checks+=1
 assert condition,detail
def fields(entry):
 g=entry['grader'];return g['parts'] if g['type']=='parts' else[g]
assert_(len(source)==844,'source total')
assert_(set(patch).isdisjoint(review),'exclusive owner files')
assert_(set(patch)|set(review)==set(source),'all844 covered')
for qid,e in patch.items():
 fs=fields(e)
 assert_(e['objectiveFieldCount']==len(fs),(qid,'fieldcount'))
 assert_(e.get('answerCheckSource',{}).get('chapter')==3,(qid,'provenance'))
 assert_(bool(e.get('responsePartPrompt')),(qid,'source contract'))
 for f in fs:
  assert_(f['type'] in ['numeric','choice'],(qid,'supported control'))
  if f['type']=='choice':
   assert_(f['answer'] in f['options'],(qid,'choice membership'))
   assert_(len(set(f['options']))==len(f['options']),(qid,'unique choices'))
  else:
   assert_(math.isfinite(f['answer']),(qid,'finite numeric'))
   assert_(f.get('tolerance',0)>=0,(qid,'nonnegative tolerance'))
x,y,t=s.symbols('x y t',real=True)
def chosen(sec,num,index=0):return fields(patch[f'calculus-section-3-{sec}-{num}'])[index]['answer']
def expression(v):
 v=v.replace('ln2','log(2)').replace('π','pi').replace('ln','log').replace('−','-').replace('²','^2').replace('³','^3').replace('⁴','^4').replace('·','*')
 v=re.sub(r'√(\d+)',r'sqrt(\1)',v)
 return parse_expr(v,local_dict=dict(x=x,pi=s.pi,sqrt=s.sqrt,log=s.log),transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
# Independently derive tangent lines from exact original source functions/equations.
tangents=[(1,33,2*x**3-x*x+2,1),(1,35,x+2/x,2),(1,37,x**4+2*s.exp(x),0),(1,39,3*x*x-x**3,1),(2,31,(x*x-1)/(x*x+x+1),1),(2,32,(1+x)/(1+s.exp(x)),0),(2,33,2*x*s.exp(x),0),(2,35,1/(1+x*x),-1),(2,36,x/(1+x*x),3),(3,21,s.sin(x)+s.cos(x),0),(3,22,s.exp(x)*s.cos(x),0),(3,23,s.cos(x)-s.sin(x),s.pi),(3,24,x+s.tan(x),s.pi),(3,25,2*x*s.sin(x),s.pi/2),(3,26,3*x+6*s.cos(x),s.pi/3),(4,51,2**x,0),(4,52,s.sqrt(1+x**3),2),(4,53,s.sin(s.sin(x)),s.pi),(4,54,x*s.exp(-x*x),0),(4,55,2/(1+s.exp(-x)),0),(4,56,x/s.sqrt(2-x*x),1),(5,33,s.sqrt(5*x**4-x*x),1),(5,34,-s.sqrt(x**3+3*x*x),1),(6,33,s.log(x*x-3*x+1),3),(6,34,x*x*s.log(x),1)]
for sec,num,f,a in tangents:
 line=expression(chosen(sec,num));height=s.simplify(f.subs(x,a));slope=s.simplify(s.diff(f,x).subs(x,a))
 assert_(s.simplify(line.subs(x,a)-height)==0,(sec,num,'passes through source point',line,height))
 assert_(s.simplify(s.diff(line,x)-slope)==0,(sec,num,'source derivative',line,slope))
implicit=[(25,y*s.sin(2*x)-x*s.cos(2*y),s.pi/2,s.pi/4),(26,s.sin(x+y)-2*x+2*y,s.pi,s.pi),(27,x*x-x*y-y*y-1,2,1),(28,x*x+2*x*y+4*y*y-12,2,1),(29,x*x+y*y-(2*x*x+2*y*y-x)**2,0,s.Rational(1,2)),(31,2*(x*x+y*y)**2-25*(x*x-y*y),3,1),(32,y*y*(y*y-4)-x*x*(x*x-5),0,-2)]
for num,F,a,b in implicit:
 line=expression(chosen(5,num));m=(-s.diff(F,x)/s.diff(F,y)).subs({x:a,y:b})
 assert_(s.simplify(F.subs({x:a,y:b}))==0,(num,'source point'))
 assert_(s.simplify(line.subs(x,a)-b)==0,(num,'implicit tangent point'))
 assert_(s.simplify(s.diff(line,x)-m)==0,(num,'implicit tangent slope'))
# Polynomial constraint regressions from source; these caught genuine draft errors.
a,b,c,d=[chosen(1,76,i) for i in range(4)];p=x**4+a*x**3+b*x*x+c*x+d
for expr,val in [(p.subs(x,0),1),(s.diff(p,x).subs(x,0),2),(p.subs(x,1),-1),(s.diff(p,x).subs(x,1),-3)]:assert_(abs(float(expr)-val)<1e-10,('quartic tangency',expr,val))
for a in [-1,5]:
 curve=x*x+x;line=(2*a+1)*x-a*a
 assert_(line.subs(x,2)==-3,('external tangent',a))
 assert_(s.diff(curve,x).subs(x,a)==s.diff(line,x),('tangent slope',a))
# Corrected source derivative and removable-hole regression.
F=(x*x+1)/(x**3-1);correct=-x*(x**3+3*x+2)/(x**3-1)**2
assert_(s.simplify(s.diff(F,x)-correct)==0,'corrected sourcepower3.2#13')
a,p,r,nn=s.symbols('a p r n',positive=True);inner=2*r*a**(r*x)+nn;dF=2*p*r*r*a**(r*x)*s.log(a)*inner**(p-1)
assert_(s.simplify(s.diff(inner**p,x)-dF)==0,'chain rule derivative')
# Motion source derivatives and total distance, independently from turning points.
motion=[t**3-8*t*t+24*t,9*t/(t*t+9),s.sin(s.pi*t/2),t*t*s.exp(-t)]
turns=[[],[3],[1,3,5],[2]]
for num,(f,roots) in enumerate(zip(motion,turns),1):
 knots=[0,*roots,6];dist=sum(abs(float((f.subs(t,b)-f.subs(t,a)).evalf())) for a,b in zip(knots,knots[1:]))
 assert_(abs(chosen(7,num,4)-dist)<1e-8,('total distance',num,dist,chosen(7,num,4)))
# Logarithmic, exponential, and physical-rate finite differences at source inputs.
def near(a,b,label,tol=1e-8):assert_(abs(float(a)-float(b))<=tol*max(1,abs(float(b))),(label,a,b))
near(chosen(7,37),(-.15*8+.1*10)/(10*.0821),'ideal gas temperature rate')
near(chosen(9,39),(100**2*.3+80**2*.2)/180**2,'parallel resistance')
near(chosen(9,41),180*math.sin(math.pi/3)*(math.pi/90)/math.sqrt(12**2+15**2-360*math.cos(math.pi/3)),'triangle degree conversion')
near(chosen(9,42),20/math.sqrt(26**2-12**2),'cart pulley')
near(chosen(9,43,0),3000*600/5000,'rocket slant rate')
near(chosen(9,43,1),4000*600/5000**2,'rocket angular rate')
near(chosen(9,44),3*(1+1/9)*8*math.pi,'lighthouse speed')
near(chosen(9,45),-5/(math.sin(math.pi/3)**2)*(-math.pi/6),'overhead plane')
near(chosen(9,47),(5*math.cos(math.pi/6)*300*math.cos(math.pi/6)+(1+5*math.sin(math.pi/6))*300*math.sin(math.pi/6))/math.sqrt((5*math.cos(math.pi/6))**2+(1+5*math.sin(math.pi/6))**2),'climbing plane radar')
# Root endpoints attain stated tolerances.
for num,fun in [(7,lambda z:math.log1p(z)),(8,lambda z:(1+z)**-3),(9,lambda z:(1+2*z)**.25)]:
 line={7:lambda z:z,8:lambda z:1-3*z,9:lambda z:1+z/2}[num]
 for index in [1,2]:
  root=chosen(10,num,index);near(abs(fun(root)-line(root)),.1,('accuracy boundary',num,index))
for index in [1,2]:
 root=chosen(10,10,index);near(abs(math.exp(root)*math.cos(root)-1-root),.1,('oscillating accuracy boundary',index))
# Hyperbolic identities and branches sampled independently.
for v in [-3,-.2,.2,2]:
 near(math.asin(math.tanh(v)),math.atan(math.sinh(v)),('inverse identity',v))
 near(math.cosh(v)**2-math.sinh(v)**2,1,('hyperbolic norm',v))
 near((1+math.tanh(v))/(1-math.tanh(v)),math.exp(2*v),('double exponential',v))
for v in [.1,.5,.9]:near(math.acosh(1/v),math.log((1+math.sqrt(1-v*v))/v),('inverse sech branch',v))
# Circle tangent/contact geometry and bitangent quartic.
for slope,intercept in [(0,2),(2*math.sqrt(2),6),(-2*math.sqrt(2),6)]:
 near(abs(intercept)/math.sqrt(slope*slope+1),2,'big-circle tangent distance')
 near(abs(intercept-3)/math.sqrt(slope*slope+1),1,'small-circle tangent distance')
assert_(s.expand((x*x-1)**2)==x**4-2*x*x+1,'bitangent double roots')
# Final provenance fingerprint.
audit=json.loads((Path(__file__).parent/'source-review.json').read_text())
assert_(audit['sourceSha256']==hashlib.sha256((ROOT/audit['sourceFile']).read_bytes()).hexdigest(),'source PDF fingerprint')
print(f'{checks} Chapter3 structural and independent mathematical checks passed.')
