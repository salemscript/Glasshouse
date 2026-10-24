"""Independent substitutions, equation solving, geometry, and quadrature.
This does not invoke the website checker and does not copy grader answers as inputs.
"""
from common import *
import mpmath as mp
mp.mp.dps=45
D=json.loads((ROOT/'scripts/calculus-answer-checks/diagnostic.json').read_text())
G=json.loads((ROOT/'scripts/calculus-answer-checks/appendix-g.json').read_text())
checks=[]
def fs(sec,k):return D[f'calculus-diagnostic-tests-{k}-{sec}']['grader'].get('parts',[D[f'calculus-diagnostic-tests-{k}-{sec}']['grader']])
def close(label,actual,expected,tol=1e-10):
 assert abs(float(actual)-float(expected))<tol,(label,actual,expected)
 checks.append(label)
def symbolic(label,lhs,rhs):
 assert s.simplify(lhs-rhs)==0,(label,lhs,rhs);checks.append(label)
def field(sec,k,i,v):close(f'{sec}{k}:{i}',fs(sec,k)[i]['answer'],v,fs(sec,k)[i].get('tolerance',1e-8))
for i,v in enumerate([(-3)**4,-3**4,R(3)**-4,R(5)**23/R(5)**21,R(2,3)**-2,R(16)**R(-3,4)]):field('algebra',1,i,v)
# Recover symbolic selected expressions and compare original algebra over positive variables.
positive={str(z):s.Symbol(str(z),positive=True) for z in [x,y,a,b,h]}
def selected(sec,k,i):return s.sympify(fs(sec,k)[i]['answer'].replace('^','**'),locals=positive)
X,Y,A,B,H=[positive[str(z)] for z in [x,y,a,b,h]]
orig2=[s.sqrt(200)-s.sqrt(32),(3*A**3*B**3)*(4*A*B**2)**2,(3*X**R(3,2)*Y**3/(X**2*Y**R(-1,2)))**-2]
orig3=[3*(X+6)+4*(2*X-5),(X+3)*(4*X-5),(s.sqrt(A)+s.sqrt(B))*(s.sqrt(A)-s.sqrt(B)),(2*X+3)**2,(X+2)**3]
orig5=[(X**2+3*X+2)/(X**2-X-2),(2*X**2-X-1)/(X**2-9)*(X+3)/(2*X+1),X**2/(X**2-4)-(X+1)/(X+2),(Y/X-X/Y)/(1/Y-1/X)]
orig6=[s.sqrt(10)/(s.sqrt(5)-2),(s.sqrt(4+H)-2)/H]
for k,vals in [(2,orig2),(3,orig3),(5,orig5),(6,orig6)]:
 for i,v in enumerate(vals):symbolic(f'algebra{k}:{i}',v,selected('algebra',k,i))
# Factorizations are independently expanded against source polynomials.
for i,(before,after) in enumerate([(4*x*x-25,(2*x-5)*(2*x+5)),(2*x*x+5*x-12,(2*x-3)*(x+4)),(x**3-3*x*x-4*x+12,(x-3)*(x-2)*(x+2)),(x**4+27*x,x*(x+3)*(x*x-3*x+9)),(3*X**R(3,2)-9*s.sqrt(X)+6/s.sqrt(X),3*(X-1)*(X-2)/s.sqrt(X)),(x**3*y-4*x*y,x*y*(x-2)*(x+2))]):symbolic(f'factor{i}',before,after)
symbolic('completed square a',x*x+x+1,(x+R(1,2))**2+R(3,4));symbolic('completed square b',2*x*x-12*x+11,2*(x-3)**2-7)
roots=[([6],x+5-(14-x/2)),([1],2*x/(x+1)-(2*x-1)/x),([-3,4],x*x-x-12),([-1-s.sqrt(2)/2,-1+s.sqrt(2)/2],2*x*x+4*x+1),([-s.sqrt(2),-1,1,s.sqrt(2)],x**4-3*x*x+2),([R(2,3),R(22,3)],3*s.Abs(x-4)-10),([R(12,5)],2*x/s.sqrt(4-x)-3*s.sqrt(4-x))]
for k,(rr,eq) in enumerate(roots):
 for r in rr:symbolic(f'root{k}:{r}',eq.subs(x,r),0)
# Check whole inequality solution sets through independent sign tests, including boundaries.
preds=[lambda z:-4<5-3*z<=17,lambda z:z*z<2*z+8,lambda z:z*(z-1)*(z+2)>0,lambda z:abs(z-4)<3,lambda z:z!=-1 and(2*z-3)/(z+1)<=1]
sets=[s.Interval(-4,3,right_open=True),s.Interval.open(-2,4),s.Union(s.Interval.open(-2,0),s.Interval.open(1,s.oo)),s.Interval.open(1,7),s.Interval(-1,4,left_open=True)]
for k,(pred,domain) in enumerate(zip(preds,sets)):
 for z in [R(i,2) for i in range(-20,21)]:assert bool(domain.contains(z))==bool(pred(z)),(k,z)
 checks.append(f'inequality{k}:41-boundary-and-sign-samples')
P=s.Point(-7,4);Q=s.Point(5,-12);line=s.Line(P,Q);mid=P.midpoint(Q)
field('analytic-geometry',4,0,line.slope);field('analytic-geometry',4,2,line.intersection(s.Line(s.Point(0,0),s.Point(1,0)))[0].x);field('analytic-geometry',4,3,line.intersection(s.Line(s.Point(0,0),s.Point(0,1)))[0].y)
field('analytic-geometry',4,4,mid.x);field('analytic-geometry',4,5,mid.y);field('analytic-geometry',4,6,P.distance(Q))
for pt in [P,Q]:symbolic('line passes endpoint'+str(pt),4*pt.x+3*pt.y+16,0);symbolic('diameter circle endpoint'+str(pt),(pt.x+1)**2+(pt.y+4)**2,100)
symbolic('perpendicular bisector midpoint',3*mid.x-4*mid.y,13);symbolic('perpendicular dot product',s.Matrix([12,-16]).dot(s.Matrix([4,3])),0)
symbolic('circle center input',(-1-3)**2+(4+2)**2,52)
F=lambda z:z*z+2*z-1;g=lambda z:2*z-3
for i,v in enumerate([F(g(X)),g(F(X)),g(g(g(X)))]):symbolic('function composition'+str(i),selected('functions',7,i),v)
symbolic('difference quotient',selected('functions',2,0),((2+H)**3-8)/H)
for k,i,v in [(1,0,R(300,180)*s.pi),(1,1,-R(18,180)*s.pi),(2,0,5*s.pi/6*180/s.pi),(2,1,2*180/s.pi),(3,0,12*s.pi/6),(4,0,s.tan(s.pi/3)),(4,1,s.sin(7*s.pi/6)),(4,2,1/s.cos(5*s.pi/3)),(6,0,s.sin(s.asin(R(1,3))+s.acos(R(4,5))))]:field('trigonometry',k,i,v)
for r in [0,s.pi/3,s.pi,5*s.pi/3,2*s.pi]:symbolic('trig root'+str(r),s.sin(2*r)-s.sin(r),0)
symbolic('identity tangent',s.trigsimp(s.tan(t)*s.sin(t)+s.cos(t)-1/s.cos(t)),0)
symbolic('identity double angle',s.trigsimp(2*s.tan(t)/(1+s.tan(t)**2)-s.sin(2*t)),0)
# Independent high precision integration and convexity checks for G.
gf=lambda k:G[f'calculus-section-g-{k}']['grader']['parts']
mid=sum(mp.mpf('.05')/(mp.mpf('1.025')+mp.mpf('.05')*j) for j in range(10))
close('G1-midpoint',gf(1)[1]['answer'],mid)
area=mp.quad(lambda z:1/z,[1,mp.mpf('1.5')]);assert mp.mpf(1)/3<area<mp.mpf(5)/12;checks.append('G1-area-bounds')
close('G2-tangent-coordinate',gf(2)[1]['answer'],mp.sqrt(2));close('G2-tangent-area',gf(2)[2]['answer'],mp.quad(lambda z:mp.sqrt(2)-z/2,[1,2]));assert mp.quad(lambda z:1/z,[1,2])>gf(2)[2]['answer']>.66;checks.append('G2-strict-bound')
for k in range(2,21):assert sum(mp.mpf(1)/j for j in range(2,k+1))<mp.log(k)<sum(mp.mpf(1)/j for j in range(1,k));checks.append('G3-harmonic-'+str(k))
assert mp.log(2)<1<mp.log(3) and 2<mp.e<3;checks.append('G4-monotone-inverse')
for base in [mp.mpf('.2'),mp.mpf('1.5'),mp.mpf('3')]:
 for exp in [-mp.sqrt(2),mp.mpf('0'),mp.sqrt(3)]:
  close('G-power-log',mp.log(base**exp),exp*mp.log(base))
  close('G-general-log-power',mp.log(base**exp,5),exp*mp.log(base,5))
(Path(__file__).parent/'independent-audit.json').write_text(json.dumps(dict(checks=len(checks),passed=checks,method='Independent symbolic equivalence, source-equation substitution, geometry, sign tests and high-precision quadrature. Source graphs and choice wording manually reviewed.'),indent=2)+'\n')
print('PASS',len(checks),'independent mathematics checks')
