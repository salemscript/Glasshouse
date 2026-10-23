"""Structural/source audit and independent numerical checks of linked physical identities."""
import json, pathlib, math, hashlib, xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[2]
s=(ROOT/'site/physics-formula-data.js').read_text();data=json.loads(s[s.index('window.PHYSICS_FORMULAS=')+len('window.PHYSICS_FORMULAS='):].rstrip(';\n'))
audit=json.loads((ROOT/'scripts/physics-formulas/source-audit.json').read_text());checks=0

def test(condition,message='check failed'):
 global checks
 assert condition,message
 checks+=1

def near(a,b,rel=1e-8):test(abs(a-b)<=rel*max(1,abs(b)),f'{a} != {b}')
def simpson(f,a,b,n=20000):
 h=(b-a)/n
 return h/3*(f(a)+f(b)+4*sum(f(a+(2*i-1)*h) for i in range(1,n//2+1))+2*sum(f(a+2*i*h) for i in range(1,n//2)))

test([c['chapter'] for c in data['chapters']]==list(range(1,45)))
ids=set();groups=lines=0
for c,a in zip(data['chapters'],audit['chapters']):
 test(not a['uncoveredNumberedReferences'])
 test(set(a['numberedSummaryReferences'])<=set(a['coveredReferences']))
 test((ROOT/'site'/c['sourceFile']).is_file())
 test(hashlib.sha256((ROOT/'site'/c['sourceFile']).read_bytes()).hexdigest()==a['sourceSha256'])
 for g in c['groups']:
  groups+=1;test(g['id'] not in ids);ids.add(g['id']);test(bool(g['symbols'] and g['conditions'] and g['title']))
  test(len(g['tex'])==len(g['mathml']))
  for m in g['mathml']:
   lines+=1;el=ET.fromstring(m);test(el.tag=='{http://www.w3.org/1998/Math/MathML}math');test(not list(el.iter('{http://www.w3.org/1998/Math/MathML}merror')))
  for p in g['sourcePages']:test(p>=c['summaryPage'] and p<=c['summaryPage']+2)
near(groups,data['groupCount']);near(lines,data['equationCount'])
# Independent checks: solve related identities in different ways rather than snapshotting output.
for v0,a,t in [(3,2,5),(-4,1,8),(8,-2,3)]:
 x=v0*t+.5*a*t*t;v=v0+a*t;near(v*v,v0*v0+2*a*x);near(x,.5*(v0+v)*t);near(x,v*t-.5*a*t*t)
for angle in [.2,.6,1.0]:
 v=23.;g=9.8;t=2*v*math.sin(angle)/g;near(v*math.cos(angle)*t,v*v*math.sin(2*angle)/g)
# RC charging derivative, resistance heating, and energy balance.
for t in [.1,.8,2.4]:
 R=200.;C=.003;emf=9.;h=1e-5;q=lambda x:C*emf*(1-math.exp(-x/(R*C)))
 i=(q(t+h)-q(t-h))/(2*h);near(i,emf/R*math.exp(-t/(R*C)));near(emf*i,i*i*R+(q(t)/C)*i)
# Energy identities for special relativity at several speeds.
for beta in [.01,.4,.9,.999]:
 gamma=1/math.sqrt(1-beta*beta);m=3.;c=2.;E=gamma*m*c*c;K=(gamma-1)*m*c*c;p=gamma*m*beta*c
 near(E*E,(p*c)**2+(m*c*c)**2);near((p*c)**2,K*K+2*K*m*c*c)
# Maxwell density normalization and second moment (set R=T=M=1).
f=lambda v:4*math.pi*(1/(2*math.pi))**1.5*v*v*math.exp(-v*v/2)
near(simpson(f,0,12),1);near(simpson(lambda v:v*v*f(v),0,12),3)
# Wavefunction normalization and Schrödinger eigenenergy in an infinite well.
for n in [1,2,5]:
 L=3.;h=2.;m=4.;psi=lambda x:math.sqrt(2/L)*math.sin(n*math.pi*x/L)
 near(simpson(lambda x:psi(x)**2,0,L),1)
 x=.27*L;dx=1e-4;second=(psi(x+dx)-2*psi(x)+psi(x-dx))/(dx*dx)
 E=h*h*n*n/(8*m*L*L);near(-h*h/(8*math.pi**2*m)*second,E*psi(x),1e-6)
# Fermi energy follows from integrating the independently stated density of states.
for n in [1.,10.,300.]:
 h=m=1.;Ef=(h/(2*math.pi))**2/(2*m)*(3*math.pi**2*n)**(2/3);coefficient=8*math.sqrt(2)*math.pi*m**1.5/h**3
 near(coefficient*(2/3)*Ef**1.5,n)
# Planck spectral exitance integral recovers the Stefan–Boltzmann coefficient.
near(simpson(lambda x:0 if x==0 else x**3/math.expm1(x),0,45),math.pi**4/15)
h=6.62607015e-34;k=1.380649e-23;c=299792458.
sigma=2*math.pi**5*k**4/(15*h**3*c*c);near(sigma/5.670374419e-8,1,1e-9)
# Reflected-film maxima: optical phase + one reflection reversal adds to a full turn.
for order in range(5):near(math.cos(2*math.pi*(order+.5)+math.pi),1)
# Ideal-gas entropy invariance in a reversible adiabat.
for gamma in [5/3,7/5]:
 R=8.31;Cv=R/(gamma-1);Vi=2.;Vf=5.;Ti=400.;Tf=Ti*(Vi/Vf)**(gamma-1)
 near(R*math.log(Vf/Vi)+Cv*math.log(Tf/Ti),0)
print(f'PASS: {checks} source/MathML/numerical checks; {len(data["chapters"])} chapters, {groups} groups, {lines} equation lines; every numbered summary reference covered.')
