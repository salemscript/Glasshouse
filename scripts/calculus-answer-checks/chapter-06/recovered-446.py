#!/usr/bin/env python3
"""Source-reviewed answers to22 restored original mathematical questions on printed446."""
import sys,json,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'chapter-05'))
from common import *
from scipy.integrate import quad
A=Author(6);row=A.row;tests=[]
# Integration coordinate x below stands for the explicitly named source x or y.
models={
1:('x',pi*(x+1)**2,0,2,'Outer radius x+1; inner radius0.'),
2:('x',pi/x**2,1,4,'Disk radius1/x.'),
3:('x',pi*(x-1),1,5,'The curve meets y=0 atx=1; radius√(x−1).'),
4:('x',pi*s.exp(2*x),-1,1,'Disk radius e^x.'),
5:('y',4*pi*x,0,9,'Disk radius2√y.'),
6:('y',pi*x**4/4,0,4,'The source equation is2x=y², so radius y²/2.'),
7:('x',pi*(x*x-x**6),0,1,'For0≤x≤1, outer radius x and inner radius x³.'),
8:('x',pi*((6-x*x)**2-4),-2,2,'Intersections with y=2 arex=±2; outer radius6−x², inner radius2.'),
9:('y',pi*(4*x*x-x**4),0,2,'Outer radius2y and inner radius y²; intersections y=0,2.'),
10:('y',pi*((2-x*x)**2-x**8),-1,1,'Outer radius2−y², inner radius y⁴; real intersections y=±1.'),
11:('x',pi*((1-x*x)**2-(1-s.sqrt(x))**2),0,1,'About y=1, distances are1−x² and1−√x, both nonnegative on0–1.'),
12:('x',pi*((x**3+3)**2-16),1,2,'About y=−3, outer radius x³+3 and inner radius4; the curve meets y=1 atx=1.'),
13:('x',pi*(4-s.sec(x)**2),-pi/3,pi/3,'Use the central bounded component: outer radius2, inner radius secx, about y=1. Other periodic components have the same volume.'),
14:('x',pi*((1+s.cos(x))**2-(1+s.sin(x))**2),0,pi/4,'About y=−1, outer radius1+cosx and inner radius1+sinx.'),
15:('y',pi*((2-x**R(1,3))**2-1),0,1,'Horizontal washers about x=2 have outer radius2−y^(1/3), inner radius1.'),
17:('y',pi*((3-x*x)**2-(2+x*x)**2),-1/s.sqrt(2),1/s.sqrt(2),'About x=3, outer radius3−y² and inner radius2+y²; intersections are y=±1/√2.'),
19:('x',pi*x*x,0,1,'R₁ is0≤y≤x≤1; aroundOA(y=0), disk radiusx.'),
20:('y',pi*(1-x*x),0,1,'AroundOC(x=0), horizontal washer radii1 andy.'),
21:('y',pi*(1-x)**2,0,1,'AroundAB(x=1), horizontal disk radius1−y.'),
22:('x',pi*(1-(1-x)**2),0,1,'AroundBC(y=1), vertical washer radii1 and1−x.')}
for no,(coordinate,expr,lo,hi,why) in models.items():
 value=s.integrate(expr,(x,lo,hi));integral='∫['+fmt(lo)+','+fmt(hi)+'] '+fmt(expr).replace('x',coordinate)+' d'+coordinate
 row(2,no,c('Disk/washer volume integral',integral),n('Volume',value),why=why+' The cross-section area isπ(R²−r²); integrate over the stated interval.',limited=no<=18)
 q=A.out[f'calculus-section-6-2-{no}'];q.update(answerCheckSource=dict(type='source-reviewed-original-calculation',title='Stewart Calculus: Early Transcendentals,8e',printedPage=446,fullPDFPage=478,sourceURL='https://s3.amazonaws.com/scschoolfiles/3191/calculus_early_transcendentals_james_stewart_8th_edition.pdf'))
 fn=s.lambdify(x,expr,'numpy');v=quad(fn,float(lo),float(hi),epsabs=1e-10)[0];assert abs(v-float(value))<1e-8*max(1,abs(v));tests.append(dict(number=no,method='Independent SciPy quadrature vs symbolic integral',quadrature=v,exact=fmt(value)))
row(2,16,c('Washer setup','π∫[0,1/2](3²−2²)dy + π∫[1/2,1][(1+1/y)²−2²]dy','π∫[0,1](3²−2²)dy','π∫[1,2](1/x)²dx'),n('Volume',2*pi*(1+s.log(2))),why='Around x=−1, horizontal washers use x from1 to2 while0≤y≤1/2, then1 to1/y for1/2≤y≤1. The outer boundary changes at y=1/2; inner radius remains2.',limited=True)
row(2,18,c('Washer setup','π∫[0,2](3²−1²)dy + π∫[2,4][3²−(y−1)²]dy','π∫[0,4](3²−1²)dy','π∫[2,4]y²dy'),n('Volume',76*pi/3),why='Around x=1, horizontal washers spanx=2 to4 belowy=2, thenx=y to4 above. Outer radius3; inner radius1 ory−1.',limited=True)
for no,fn,lo,hi,value in [(16,lambda z:2*math.pi*(z+1)/z,1,2,2*pi*(1+s.log(2))),(18,lambda z:2*math.pi*(z-1)*z,2,4,76*pi/3)]:
 v=quad(fn,lo,hi)[0];assert abs(v-float(value))<1e-9;tests.append(dict(number=no,method='Independent shell method vs piecewise washers',value=v))
# Cross-check nontrivial washers using shells with entirely different slicing.
for no,fn,lo,hi in [(7,lambda y:2*math.pi*y*(y**(1/3)-y),0,1),(8,lambda y:2*math.pi*y*2*math.sqrt(6-y),2,6),(11,lambda y:2*math.pi*(1-y)*(math.sqrt(y)-y*y),0,1),(15,lambda z:2*math.pi*(2-z)*z**3,0,1),(19,lambda y:2*math.pi*y*(1-y),0,1),(20,lambda z:2*math.pi*z*z,0,1),(21,lambda z:2*math.pi*(1-z)*z,0,1),(22,lambda y:2*math.pi*(1-y)*(1-y),0,1)]:
 val=A.out[f'calculus-section-6-2-{no}']['grader']['parts'][1]['answer'];v=quad(fn,lo,hi,epsabs=1e-9)[0];assert abs(v-val)<1e-7,(no,v,val);tests.append(dict(number=no,method='Shell/washer equivalence',value=v))
for no in range(1,23):
 q=A.out[f'calculus-section-6-2-{no}'];q['answerCheckSource']=dict(type='source-reviewed-original-calculation',title='Stewart Calculus: Early Transcendentals,8e',printedPage=446,fullPDFPage=478,sourceURL='https://s3.amazonaws.com/scschoolfiles/3191/calculus_early_transcendentals_james_stewart_8th_edition.pdf')
 if no>=19:q['nativeFigures']=[dict(url='books/calculus/section-6-2-regions.svg',alt='Original reconstructed unit-square diagram. R₁ lies below y=x; R₂ above y=x^(1/4); R₃ between those curves.')]
folder=Path(__file__).parent
(folder/'recovered-446.json').write_text(json.dumps(A.out,ensure_ascii=False,indent=2)+'\n')
(folder/'recovered-446-audit.json').write_text(json.dumps(dict(scope='All22 original exercise records recovered from omitted printed446',sourceURL='https://s3.amazonaws.com/scschoolfiles/3191/calculus_early_transcendentals_james_stewart_8th_edition.pdf',fullPDFPage=478,printedPage=446,visualReview='Rendered original page inspected: equations, rotation axes, shared sketch instruction1–18 and coordinate diagram19–30.',questions=A.notes,independentChecks=tests,assessmentLimit='Sketching the solid and representative slice is not automatically assessed; records1–18 are complete:false. The volume and integral setup are checked.'),ensure_ascii=False,indent=2)+'\n')
print('Recovered446:',len(A.out),'records;',len(tests),'independent checks')
