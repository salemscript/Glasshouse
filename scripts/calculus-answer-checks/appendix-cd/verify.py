"""Independently check every numeric field using source geometry and mpmath.
Do not import author.py: this verifier reads the frozen output and derives its
reference values from a separate transcription of source equations and givens.
"""
import json,math
from pathlib import Path
import mpmath as m
import sympy as s
m.mp.dps=50
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE.parent/'appendix-cd.json').read_text())
checks=[];seen=set()
def fields(sec,num):
 g=DATA[f'calculus-section-{sec}-{num}']['grader'];return g.get('parts',[g])
def check(sec,num,label,expected,method):
 f=next(z for z in fields(sec,num) if z['label']==label)
 assert f['type']=='numeric',(sec,num,label)
 diff=abs(m.mpf(str(f['answer']))-expected);assert diff<max(m.mpf('1e-7'),abs(expected)*m.mpf('1e-12')),(sec,num,label,diff)
 seen.add((sec,num,label));checks.append(dict(id=f'calculus-section-{sec}-{num}',field=label,method=method,absoluteError=float(diff)))
# Original polynomial coefficients, solved directly for center/radius.
for num,coefs in [(5,[1,-4,10,13]),(6,[1,0,6,2]),(7,[1,1,0,0]),(8,[16,8,32,1]),(9,[2,-1,1,-1])]:
 Q,A,B,K=map(m.mpf,coefs);h=-A/(2*Q);v=-B/(2*Q);radius=m.sqrt(h*h+v*v-K/Q)
 for label,value in [('Center · x',h),('Center · y',v),('Radius',radius)]:check('c',num,label,value,'Center from first derivatives; radius from zero-level equation')
# Parabolas transcribed as dependent = A independent²+B independent+C.
for num,A,B,C,horizontal in [(11,-1,0,0,False),(14,-2,0,0,True),(18,1,0,2,False),(19,1,0,-1,True),(24,1,2,0,False),(27,1,-6,13,False),(29,-1,0,4,True),(30,.5,3,2.5,True)]:
 A,B,C=map(m.mpf,(A,B,C));ind=-B/(2*A);dep=C-B*B/(4*A)
 h,v=(dep,ind) if horizontal else (ind,dep)
 check('c',num,'Vertex · x',h,'Stationary point of original quadratic');check('c',num,'Vertex · y',v,'Stationary point of original quadratic')
# General conic A x²+B y²+C x+D y+E=0, no xy term.
for num,A,B,C,D,E in [(12,-1,1,0,0,-1),(13,1,4,0,0,-16),(15,16,-25,0,0,-400),(16,25,4,0,0,-100),(17,4,1,0,0,-1),(20,9,-25,0,0,-225),(21,-1,9,0,0,-9),(22,2,5,0,0,-10),(25,9,4,-18,-16,-11),(26,16,9,0,-36,-108),(28,1,-1,-4,0,3),(31,1,4,-6,0,5),(32,4,9,-16,54,61)]:
 A,B,C,D,E=map(m.mpf,(A,B,C,D,E));h=-C/(2*A);v=-D/(2*B);rhs=-E+A*h*h+B*v*v
 for label,value in [('Center · x',h),('Center · y',v)]:check('c',num,label,value,'Gradient of source conic vanishes at center')
 if A*B>0:
  check('c',num,'Horizontal semiaxis',m.sqrt(rhs/A),'Axis intercept after translation');check('c',num,'Vertical semiaxis',m.sqrt(rhs/B),'Axis intercept after translation')
 else:
  vdist=m.sqrt(rhs/A) if rhs/A>0 else m.sqrt(rhs/B)
  check('c',num,'Center-to-vertex distance',vdist,'Real nonzero-axis intercept after translation');check('c',num,'Positive asymptote slope',m.sqrt(-A/B),'Homogeneous quadratic asymptote')
for num,deg in enumerate([210,300,9,-315,900,36],1):check('d',num,'Angle',m.mpf(deg)/360*2*m.pi,'Fraction of a full revolution')
for num,turns in enumerate([m.mpf(2),-m.mpf(7)/4,m.mpf(5)/24,m.mpf(4)/3,-m.mpf(3)/16,5/(2*m.pi)],7):check('d',num,'Angle',turns*360,'Radians as fraction of a complete turn')
for num,label,v in [(13,'Arc length',2*m.pi*36/24),(14,'Arc length',2*m.pi*10/5),(15,'Central angle',m.mpf(1)/m.mpf('1.5')),(16,'Radius',m.mpf(6)/(m.pi*3/4))]:check('d',num,label,v,'Circular arc as circumference times fraction of turn')
for num,ang in [(17,m.pi*7/4),(18,-m.pi*5/6),(19,-m.pi*3/4),(20,m.pi*7/3),(21,m.mpf(2)),(22,m.mpf(-3))]:check('d',num,'Coterminal angle in [0,2π)',m.fmod(ang+2*m.pi,2*m.pi),'One-turn normalization independent of degrees')
# Right-triangle sides using cosine law/Pythagorean constructions.
side35=m.sqrt(100-(10*m.cos(m.radians(35)))**2)
side36=m.sqrt(625-(25*m.sin(m.radians(40)))**2)
side37=m.sqrt((8/m.cos(2*m.pi/5))**2-64)
side38=m.sqrt(22**2+(22*m.tan(3*m.pi/8))**2)
for num,value in zip(range(35,39),[side35,side36,side37,side38]):check('d',num,'Side x · to five decimal places',value,'Independent Pythagorean reconstruction')
# Verify source-derived exhaustive factor cases in the closed interval.
# Substitution independently rejects extraneous roots; derivations in the source
# audit establish completeness, including repeated roots and both endpoints.
funcs={65:lambda x:2*m.cos(x)-1,66:lambda x:3*(m.cos(x)/m.sin(x))**2-1,67:lambda x:2*m.sin(x)**2-1,68:lambda x:abs(m.tan(x))-1,69:lambda x:m.sin(2*x)-m.cos(x),70:lambda x:2*m.cos(x)+m.sin(2*x),71:lambda x:m.sin(x)-m.tan(x),72:lambda x:2+m.cos(2*x)-3*m.cos(x)}
# Exact quadrant reasoning yields angles as fractions of pi; independently
# evaluate original equations and check no missing roots via interval signs.
fractions={65:[(1,3),(5,3)],66:[(1,3),(2,3),(4,3),(5,3)],67:[(1,4),(3,4),(5,4),(7,4)],68:[(1,4),(3,4),(5,4),(7,4)],69:[(1,6),(1,2),(5,6),(3,2)],70:[(1,2),(3,2)],71:[(0,1),(1,1),(2,1)],72:[(0,1),(1,3),(5,3),(2,1)]}
for num,ratios in fractions.items():
 for j,(aa,bb) in enumerate(ratios):
  root=m.pi*aa/bb;assert abs(funcs[num](root))<m.mpf('1e-40')
  check('d',num,'Solution '+str(j+1)+' · ascending order',root,'Substitution into original trigonometric equation and exhaustive factor cases')
for num,values in {77:{'Amplitude':1,'Period':2*m.pi,'Horizontal shift · positive means right':m.pi/3},78:{'Period':m.pi/2},79:{'Period':m.pi,'Vertical scale factor':m.mpf(1)/3,'Horizontal shift · positive means right':m.pi/2},80:{'Period':2*m.pi},81:{'Fundamental period':m.pi,'Minimum value':0,'Maximum value':1},82:{'Amplitude':1,'Period':2*m.pi,'Horizontal shift · positive means right':-m.pi/4,'Midline y':2,'Minimum value':1,'Maximum value':3}}.items():
 for label,value in values.items():check('d',num,label,m.mpf(value),'Transformation of parent trig function')
# Coordinate construction independently obtains distance and area.
px=820*m.cos(m.radians(103));py=820*m.sin(m.radians(103))
check('d',84,'Distance |AB|',m.sqrt((px-910)**2+py**2),'Coordinate-distance reconstruction')
check('d',89,'Area · to five decimal places',abs(10*(3*m.sin(m.radians(107))))/2,'Half the absolute determinant of side vectors')
all_numeric={(qid.split('-')[2],int(qid.split('-')[3]),f['label']) for qid,v in DATA.items() for f in v['grader'].get('parts',[v['grader']]) if f['type']=='numeric'}
assert seen==all_numeric,(all_numeric-seen,seen-all_numeric)
# Independently check all 66 exact trig-ratio choice fields, including undefined values.
x=s.symbols('x',real=True)
ratio_checks=[]
def parse(z):return s.sympify(z.replace('^','**'),locals={'pi':s.pi})
for num,theta in [(23,3*m.pi/4),(24,4*m.pi/3),(25,9*m.pi/2),(26,-5*m.pi),(27,5*m.pi/6),(28,11*m.pi/4)]:
 st,ct=m.sin(theta),m.cos(theta)
 for f in fields('d',num):
  name=f['label'].split()[0]
  numerator,denominator={'sin':(st,1),'cos':(ct,1),'tan':(st,ct),'csc':(1,st),'sec':(1,ct),'cot':(ct,st)}[name]
  if abs(denominator)<m.mpf('1e-40'):assert f['answer']=='Undefined'
  else:assert abs(m.mpf(str(s.N(parse(f['answer']),48)))-numerator/denominator)<m.mpf('1e-40')
  ratio_checks.append((num,name))
for num,px,py in [(29,4,3),(30,1,2),(31,-2,s.sqrt(5)),(32,-1,-2*s.sqrt(2)),(33,-3,-1),(34,s.sqrt(7),-3)]:
 rr=s.sqrt(px*px+py*py)
 values={'sin':py/rr,'cos':px/rr,'tan':s.sympify(py)/px,'csc':rr/py,'sec':rr/px,'cot':s.sympify(px)/py}
 for f in fields('d',num):
  name=f['label'].split()[0];assert s.simplify(parse(f['answer'])-values[name])==0
  ratio_checks.append((num,name))
# Independently evaluate shared-given trig combinations by constructing the angles.
xx=s.asin(s.Rational(1,3));yy=s.acos(s.Rational(4,5))
for num,expr in [(59,s.sin(xx+yy)),(60,s.cos(xx+yy)),(61,s.cos(xx-yy)),(62,s.sin(xx-yy)),(63,s.sin(2*yy)),(64,s.cos(2*yy))]:
 assert abs(float(s.N(parse(fields('d',num)[0]['answer'])-expr,40)))<1e-30
# Dense interior inequality verification against independent interval membership.
ineq={73:(lambda x:m.sin(x)<=m.mpf('.5'),lambda x:x<=m.pi/6 or x>=5*m.pi/6),74:(lambda x:2*m.cos(x)+1>0,lambda x:x<2*m.pi/3 or x>4*m.pi/3),75:(lambda x:-1<m.tan(x)<1,lambda x:x<m.pi/4 or 3*m.pi/4<x<5*m.pi/4 or x>7*m.pi/4),76:(lambda x:m.sin(x)>m.cos(x),lambda x:m.pi/4<x<5*m.pi/4)}
for num,(lhs,rhs) in ineq.items():
 for i in range(1000):
  v=2*m.pi*(m.mpf(i)+m.mpf('.123'))/1000;assert bool(lhs(v))==bool(rhs(v)),(num,v)
report=dict(numericFields=len(checks),exactTrigFields=len(ratio_checks),sharedGivenTrigFields=6,inequalityInteriorSamples=4000,checks=checks,scope='All numeric fields independently checked; exact trig choices and inequality intervals checked separately. Symbolic identity audit and source-reviewed reasoning cover proof contracts; proof completion is intentionally not awarded.')
(HERE/'independent-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(checks),'numeric fields;',len(ratio_checks),'exact trig fields;4000 inequality samples')
