import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'chapter-05'))
from common import *
import numpy as np
from scipy.optimize import brentq,curve_fit
A=Author(6);row=A.row
# Source: printed434–437, visually inspected, including source graph labels.
areas={1:[(x**R(1,3)-1/x,1,8)],2:[(s.exp(x)-x*s.exp(x*x),0,1)],3:[(s.exp(x)-x*x+2,-1,1)],4:[(6*x-2*x*x,0,3)],5:[(s.exp(x)-x*x+1,-1,1)],6:[(x-s.sin(x),pi/2,pi)],7:[(x-(x-2)**2,1,4)],8:[(6*x-x*x,0,6)],9:[(1/x-1/x**2,1,2)],10:[(s.sin(x)-2*x/pi,0,pi/2)],11:[(2-2*x*x,-1,1)],12:[(3-x*x/4-x,-6,2)],13:[(18-2*x*x,-3,3)],14:[(4*x-2*x*x,0,2)],15:[(8*s.cos(x)-1/s.cos(x)**2,-pi/3,pi/3)],16:[(2-2*s.cos(x),0,2*pi)],17:[(4-x*x,-2,2)],18:[(s.sqrt(x)-x,0,1)],19:[(s.cos(pi*x)-4*x*x+1,-R(1,2),R(1,2))],20:[(2-x*x-x**4,0,1)],21:[(2*(2*s.sin(x)-s.tan(x)),0,pi/3)],22:[(2*(x-x**3),0,1)],23:[((2*x)**R(1,3)-x*x/8,0,4),(x*x/8-(2*x)**R(1,3),4,6)],24:[(2*s.cos(x)-1,0,pi/3),(1-2*s.cos(x),pi/3,pi)],25:[(2*(2-x-x**4),0,1)],26:[(s.exp(-x)-s.sinh(x),0,s.log(3)/2),(s.sinh(x)-s.exp(-x),s.log(3)/2,2)],27:[(3*x/4,0,1),(1/x-x/4,1,2)],28:[(R(7,4)*x*x,0,1),(3-x-x*x/4,1,2)],30:[(x/s.sqrt(1+x*x)-x/s.sqrt(9-x*x),0,2)],31:[(x/(1+x*x)-x*x/(1+x**3),0,1)],32:[((s.log(x)-s.log(x)**2)/x,1,s.E)],33:[(R(5,2),0,1)],34:[(2,0,1)],35:[(s.cos(2*x)-s.sin(x),0,pi/6),(s.sin(x)-s.cos(2*x),pi/6,pi/2)],36:[(2**x-3**x,-1,0),(3**x-2**x,0,1)],45:[(2*(x**5-6*x**3+3*x),0,s.sqrt(3-s.sqrt(6))),(2*(-x**5+6*x**3-3*x),s.sqrt(3-s.sqrt(6)),s.sqrt(3+s.sqrt(6)))],46:[(2*(1-x-x*x/2),0,s.sqrt(3)-1)],55:[(-2*x*s.sqrt(x+3),-3,0)],56:[(x*x,0,R(1,2)),((x-1)**2,R(1,2),1)]}
# 46 uses horizontal slices: |y|≤sqrt(x/2), |y|≤1−x; integrate y from0 tosqrt3−1, right−left =1−y−2y².
areas[46]=[(2*(1-x-2*x*x),0,R(1,2))]
for num,pieces in areas.items():A.area(num,pieces,limited=num not in [1,2,3,4,33,34,55,56])
row(1,29,n('(a) total area',39),n('(b) signed integral',15),why='The left region contributes −12 to ∫(f−g), the right +27; area adds both magnitudes.')
# Numerically isolated crossings and quadrature; record exact defining functions and brackets.
models={37:(x*s.sin(x*x)-x**4,[(.7,1)],0,None),38:(x/(x*x+1)**2-x**5+x,[(1,1.2)],0,None),39:(3*x*x-2*x-(x**3-3*x+4),[(-2,-1),(1,2),(2,4)],None,None),40:(R(13,10)**x-2*s.sqrt(x),[(.2,.5),(4,10)],None,None),41:(2/(1+x**4)-x*x,[], -1,1),42:(s.exp(1-x*x)-x**4,[],-1,1),43:(s.tan(x)**2-s.sqrt(x),[(.5,1)],0,None),44:(s.cos(x)-x-2*s.sin(x)**4,[(0,1)],0,None)}
for num,(expr,brackets,left,right) in models.items():
 fn=s.lambdify(x,expr,'mpmath'); roots=[mp.findroot(fn,bracket) for bracket in brackets]
 if num==44:
  # Second crossing left of zero bounds the source enclosed region.
  roots=[mp.findroot(fn,(-2,-1.8)),mp.findroot(fn,(-1.3,-1.1)),*roots];left=None
 bounds=([mp.mpf(str(left))] if left is not None else [])+roots+([mp.mpf(str(right))] if right is not None else [])
 val=sum(abs(mp.quad(fn,[a,b])) for a,b in zip(bounds,bounds[1:]))
 fields=[n('Area',val,tol=1e-5 if num>=41 else .0005)]
 if num<=40:fields +=[n(f'Intersection x, ordered {i+1}',r,tol=.0005) for i,r in enumerate(bounds)]
 row(1,num,*fields,why='Find all bounding intersections of '+fmt(expr)+'=0, then integrate the absolute vertical difference over consecutive intervals. Quadrature splits at each listed intersection.',limited=True)
 A.integrals.append(dict(qid=f'calculus-section-6-1-{num}',integrand=fmt(expr),bounds=[str(v) for v in bounds],absolute=True,value=str(val)))
qid='calculus-section-6-1-43'
A.out[qid]['grader']['label']='Area of the first bounded region, 0≤x<π/2'
A.out[qid]['grader']['explanation']+=' This check explicitly uses the first region on the principal tangent branch; additional periodic tangent branches can bound other regions.'
row(1,47,n('Kelly’s extra distance',2*(2+6+9+11+12)/3600,'miles'),why='Midpoints t=1,3,5,7,9 give velocity gaps2,6,9,11,12mph. Multiply sum by2seconds/3600.')
row(1,48,n('Midpoint area estimate',4*(6.2+6.8+5+4.8),'m²'),why='Use four4m-wide strips with midpoint widths6.2,6.8,5.0,4.8m.')
row(1,49,n('Midpoint cross-sectional area',40*(20.3+29+27.3+20.5+8.7),'cm²'),why='Five40cm-wide strips use thicknesses at20,60,100,140,180cm.')
birth=2200*s.exp(R(24,1000)*x);death=1460*s.exp(R(18,1000)*x);value=s.integrate(birth-death,(x,0,10))
row(1,50,n('Area',value,'people',.1),c('Meaning','Net population increase from births minus deaths over10 years','Total births alone','Population at year10'),why='Birth rate exceeds death rate over the interval; integrate b−d. This is increase, not total population.')
g=R(9,10)*(-x*(x-21)*(x+1)); t1=mp.findroot(s.lambdify(x,g-1210,'mpmath'),(10,12)); t2=mp.findroot(s.lambdify(x,g-1210+23*(x-s.Float(str(t1),40)),'mpmath'),(16,19)); val=mp.quad(s.lambdify(x,g-1210+23*(x-s.Float(str(t1),40)),'mpmath'),[t1,t2])
row(1,51,n('(a) infectiousness begins',t1,'days',.001),n('(b) infectiousness ends',t2,'days',.001),n('(c) level',val,'(cells/mL)·days',.1),why='Use g=0.9[−t(t−21)(t+1)]. The first threshold solves g=1210; the end is the later intersection with the line of slope−23 through that threshold.')
e=R(73,100)*x**3-R(217,100)*x*x+R(3,2)*x-R(1,2); rr=sorted(float(s.re(r)) for r in s.nroots(e) if abs(float(s.im(r)))<1e-10 and 0<float(s.re(r))<2); bs=[0,*rr,2];val=sum(abs(float(s.integrate(e,(x,a,b)))) for a,b in zip(bs,bs[1:]))
row(1,52,n('Area between rate curves',val,'inches',.0001),c('Meaning','Accumulated absolute difference in rainfall rates; not necessarily the difference of total rainfall','The signed difference in total rainfall regardless of crossings','Rainfall rate at t=2'),why='Split at crossings and integrate |f−g|. Rate ordering changes, so the absolute area differs from the signed net rainfall difference.',limited=True)
row(1,53,c('(a) ahead at1 minute','Car A','Car B','Tied'),c('(b) shaded area','Distance A is ahead of B at1 minute','Speed difference at1 minute','Total distance traveled by B'),c('(c) ahead at2 minutes','Car B','Car A','Tied'),n('(d) next side-by-side time',1.5,'min',.2),why='Position differences equal signed areas between velocity graphs. The later B-over-A area cancels the earlier A-over-B area near1.5min; this is a sketch estimate.',limited=True)
row(1,54,c('Meaning','Increase in profit from producing50 to100 units','Total revenue at100 units','Total cost from0 to100'),n('Estimated increase in profit',50,'thousand dollars',10),why='The shaded region is ∫50^100(R′−C′)dx. A midpoint at75 gives gap about1 thousand dollars/unit, hence about50 thousand dollars. Allow sketch-reading tolerance.',limited=True)
row(1,57,n('b',4/2**(2/3)),why='The area below y=b and above y=x² is4b^(3/2)/3; equate to half of32/3.')
row(1,58,n('(a) a',1.6),n('(b) b',(1-math.sqrt(6)/4)**2),why='Vertical split:1−1/a=3/8. Horizontal split: integrate min(b,1/x²) over1≤x≤4; b solves2√b−b−1/4=3/8.')
row(1,59,c('c','c=−6 or c=6','c=6 only','c=−3 or c=3'),why='Area=∫−|c|^|c|2(c²−x²)dx=8|c|³/3=576.')
row(1,60,n('c',pi/3),why='First area2sin(c/2)−sin c; second area1−sin c. Equality gives sin(c/2)=1/2.')
row(1,61,c('m range','0<m<1','m>1','m<0'),c('Total area of both symmetric lobes','m−1−ln m','1−m+ln m','(m−1−ln m)/2'),c('Area of one lobe','(m−1−ln m)/2','m−1−ln m','(1−m+ln m)/2'),why='Nonzero crossings require x²=1/m−1>0. Integrate x/(1+x²)−mx from0 to√(1/m−1), then double.')
suf='-project-applied-project-the-gini-index-1'
row(1,1,c('(a) normalization','G=2∫₀¹[x−L(x)]dx','G=∫₀¹L(x)dx','G=2∫₀¹[L(x)−x]dx'),n('(b) equal incomes G',0),n('(b) all income to one person G',1),why='The area below y=x on[0,1] is1/2; dividing the inequality area by1/2 multiplies it by2.',limited=True,suffix=suf)
xx=np.linspace(0,1,6);yy=[0,.034,.120,.266,.498,1];coef=np.polyfit(xx,yy,2);G=1-2*(coef[0]/3+coef[1]/2+coef[2])
row(1,2,n('(a) richest20% income share',50.2,'%'),*[n('(b) '+label,v,tol=.0005) for label,v in zip(['quadratic coefficient','linear coefficient','constant'],coef)],n('(c) G',G,tol=.0005),c('(b) fit assessment','Reasonable overall fit; endpoints are not enforced by unconstrained regression','Exact interpolation at every data point','The model guarantees a valid Lorenz curve everywhere'),why='Use ordinary least-squares quadratic regression of the six source observations, then G=1−2∫L. A regression fit is not automatically a physically constrained Lorenz model.',limited=True,suffix=suf)
fields=[]
for year,y in [(1970,[0,.041,.149,.323,.568,1]),(1980,[0,.042,.144,.312,.559,1]),(1990,[0,.038,.134,.293,.530,1]),(2000,[0,.036,.125,.273,.503,1])]:
 co=np.polyfit(xx,y,2);fields.append(n('G in'+str(year),1-2*(co[0]/3+co[1]/2+co[2]),tol=.0005))
row(1,3,*fields,c('Trend','Inequality generally increases over these years','Inequality decreases throughout','G stays constant'),why='Fit each year by the same unconstrained quadratic least squares method and integrate each model.',limited=True,suffix=suf)
co,_=curve_fit(lambda x,a,k:a*x**k,xx,np.array(yy),p0=[1,3]);Gp=1-2*co[0]/(co[1]+1)
row(1,4,n('Nonlinear least-squares a',co[0],tol=.001),n('Nonlinear least-squares k',co[1],tol=.001),n('Power-model G',Gp,tol=.001),c('Fit comparison','Power model reduces squared residuals compared with the quadratic fit','Both models interpolate all points','Power model must give identical G'),why='Use nonlinear least squares in the original L values, not logarithmic regression (which changes the error criterion and excludes zero). Integrate ax^k as a/(k+1).',limited=True,suffix=suf)

# 6.2 volumes, source printed447–449. The supplied excerpt omits printed446.
def vol(sec,num,expr,lo,hi,why='',limited=False,extra=[]):
 val=s.integrate(expr,(x,lo,hi));
 if val.has(s.Integral):val=s.N(val,25)
 A.integrals.append(dict(qid=f'calculus-section-6-{sec}-{num}',integrand=fmt(expr),lower=fmt(lo),upper=fmt(hi),value=fmt(val)))
 row(sec,num,n('Volume',s.N(val,25)),*extra,why=why+' Integrate '+fmt(expr)+' from '+fmt(lo)+' to '+fmt(hi)+'.',limited=limited)
def volume_pair(num,items):
 fields=[]
 for label,expr,lo,hi in items:
  val=s.integrate(expr,(x,lo,hi));fields +=[c(label+' integral','∫['+fmt(lo)+','+fmt(hi)+'] '+fmt(expr)+' dx'),n(label+' volume',s.N(val,25),tol=1e-5)]
  A.integrals.append(dict(qid=f'calculus-section-6-2-{num}',integrand=fmt(expr),lower=fmt(lo),upper=fmt(hi),value=fmt(val)))
 row(2,num,*fields,why='Use washer cross sections π(outer radius²−inner radius²). Bounds and radii follow the source rotation axis.')
volume_pair(31,[('(a)',pi*s.exp(-2*x*x),-1,1),('(b)',pi*((1+s.exp(-x*x))**2-1),-1,1)])
volume_pair(32,[('(a)',pi*s.cos(x)**4,-pi/2,pi/2),('(b)',pi*(1-(1-s.cos(x)**2)**2),-pi/2,pi/2)])
volume_pair(33,[('(a)',8*pi*s.sqrt(1-x*x/4),-2,2),('(b)',16*pi*s.sqrt(1-x*x),-1,1)])
aa=s.sqrt((s.sqrt(5)-1)/2); yy=(s.sqrt(5)-1)/2
volume_pair(34,[('(a)',pi*(1-x*x-x**4),-aa,aa),('(b) lower part',pi*x,0,yy)])
# Correct (b) rotates the full symmetric region once: integrate min(y,1−y²) from0 to1.
valb=s.integrate(pi*x,(x,0,yy))+s.integrate(pi*(1-x*x),(x,yy,1));qid='calculus-section-6-2-34';A.out[qid]['grader']['parts'][2:]=[c('(b) integral','π∫[0,(√5−1)/2] y dy + π∫[(√5−1)/2,1](1−y²)dy','π∫[0,1]y dy','2π∫[0,1](1−y²)dy'),n('(b) volume',valb,tol=1e-5)]
for field in A.out['calculus-section-6-2-34']['grader']['parts'][2:]:field.update(provenance='explicit-source-inspected-original-answer-contract',explanation='Rotate the symmetric region once; radius squared=min(y,1−y²). Split at y=(√5−1)/2.')
for num,top,bottom,br in [(35,s.sqrt(3-x**3),s.log(x**6+2),[(-2,-1),(1,1.4)]),(36,1+x*s.exp(-x**3),s.atan(x*x),[(-1,0),(1,2)])]:
 diff=s.lambdify(x,top-bottom,'mpmath');roots=[mp.findroot(diff,b) for b in br];expr=pi*(top**2-bottom**2);val=mp.quad(s.lambdify(x,expr,'mpmath'),roots)
 row(2,num,n('Left intersection x',roots[0],tol=.0005),n('Right intersection x',roots[1],tol=.0005),n('Volume',val,tol=.001),why='Find intersections of the two positive source curves; washers have outer radius '+fmt(top)+' and inner radius '+fmt(bottom)+'.',limited=True)
 A.integrals.append(dict(qid=f'calculus-section-6-2-{num}',integrand=fmt(expr),bounds=[str(z) for z in roots],value=str(val)))
vol(2,37,pi*((1+s.sin(x)**2)**2-1),0,pi)
vol(2,38,pi*((3-x)**2-(3-x*s.exp(1-x/2))**2),0,2)
for num,ans,w in [(39,'Rotate 0≤y≤√(sin x),0≤x≤π about the x-axis','The disk radius is √(sin x), not sin x.'),(40,'Rotate 0≤x≤1−y²,−1≤y≤1 about the y-axis','The disk radius is1−y².'),(41,'Rotate y⁴≤x≤y²,0≤y≤1 about the y-axis','Outer radius y², inner radius y⁴.'),(42,'Rotate 0≤y≤√x,1≤x≤4 about y=3','Outer radius3, inner radius3−√x.')]:row(2,num,c('A solid represented by the integral',ans,'Rotate the same region about x=5','Rotate the same region about y=−5'),why=w,limited=True)
row(2,43,n('Midpoint volume',3*(18+79+106+128+39),'cm³'),why='Five slices of width3cm sample the cross sections at1.5,4.5,7.5,10.5,13.5cm.')
row(2,44,n('Midpoint volume',2*(.65+.61+.59+.55+.5),'m³'),why='Five2m slices use x=1,3,5,7,9.')
row(2,45,n('(a) x-axis estimate',2*pi*(1.6**2+2.2**2+3.8**2+3.1**2),tol=20),n('(b) y-axis shell estimate',4*pi*(3*1.6+5*2.2+7*3.8+9*3.1),tol=45),why='On2≤x≤10, four midpoint abscissas are3,5,7,9; source graph heights are approximately1.6,2.2,3.8,3.1. Apply disks for(a) and shells for(b). Tolerances reflect graph reading.',limited=True)
a,b,cc,d,r,h,RR=s.symbols('a b c d r h R',positive=True);egg=pi*(a*x**3+b*x*x+cc*x+d)**2*(1-x*x);V=s.integrate(egg,(x,-1,1))
row(2,46,f('(a) egg volume',s.expand(V)),n('(b) loon egg volume',V.subs({a:-.06,b:.04,cc:.1,d:.54})),why='Square the source radius and integrate from−1 to1; odd terms vanish by symmetry.',limited=True)
for num,expr in [(47,pi*r*r*h/3),(48,pi*h*(RR*RR+RR*r+r*r)/3),(49,pi*h*h*(r-h/3)),(51,2*b*b*h/3),(52,s.sqrt(3)*a*a*h/12),(54,16*r**3/3)]:row(2,num,f('Volume',expr),why='Integrate the source cross-sectional area. Similar lengths scale linearly with height; areas scale quadratically. Use positive geometric dimensions.')
row(2,50,f('Volume',h*(a*a+a*b+b*b)/3),c('When a=b','Square prism, V=b²h','Cone, V=πb²h/3','Volume is zero'),c('When a=0','Square pyramid, V=b²h/3','Square prism, V=b²h','Volume is zero'),why='The side of a horizontal square varies linearly between b and a; integrate its square.')
row(2,53,n('Volume',10,'cm³'),why='Use one triangular face of area(3×4)/2 and perpendicular height5: V=base×height/3.')
for num,expr,lo,hi in [(55,9*(1-x*x/4),-2,2),(56,s.sqrt(3)*(1-x)**2/4,0,1),(57,(1-x)**2,0,1),(58,4*(1-x),0,1),(59,(1-x*x)**2/2,-1,1),(60,pi*(2-x),0,2),(61,pi*(1-x*x)**2/4,-1,1)]:vol(2,num,expr,lo,hi,why='The source specifies cross-section shape and orientation; convert its base width into the corresponding area.')
row(2,62,c('(a) integral','h∫[−r,r]√(r²−x²)dx','2h∫[−r,r]√(r²−x²)dx','π∫[−r,r](r²−x²)dx'),f('(b) volume',pi*r*r*h/2),why='Each triangular section has area½×2√(r²−x²)×h; the remaining integral is a semicircle area.')
row(2,63,c('(a) washer integral','4πR∫[−r,r]√(r²−y²)dy','πR∫[−r,r](r²−y²)dy','2πR∫[−r,r]√(r²−y²)dy'),f('(b) volume',2*pi*pi*RR*r*r),why='Subtract squared radii R±√(r²−y²); use semicircle area. Assume R>r>0.')
row(2,65,c('(a) principle','Equal cross-sectional areas at every height give equal integrals and equal volumes','Equal maximum areas alone give equal volumes','Equal surface areas imply equal volumes'),f('(b) volume',pi*r*r*h),why='V=∫A(z)dz; every horizontal section of the oblique cylinder has areaπr² and vertical height is h.',limited=True)
row(2,66,f('Volume',16*r**3/3),why='Perpendicular cylinders of equal radius produce square sections with side2√(r²−z²); integrate4(r²−z²) from−r to r.')
row(2,67,f('Volume',5*pi*r**3/12),why='The lens is two spherical caps of height r/2. Each cap has volumeπ(r/2)²(r−r/6).')
row(2,68,c('Water volume, in cm³','10πh² for0≤h≤10; πh²(15−h/3)−500π/3 for10≤h≤15','πh²(15−h/3) for all h','10πh² for all h≤15'),why='Subtract submerged ball volume from the radius15 bowl cap. Up to h=10 the ball cap has volumeπh²(5−h/3); beyond10 subtract its full500π/3. Ball rests at bowl bottom.')
row(2,69,c('Removed-volume integral','8∫[0,r]√(R²−x²)√(r²−x²)dx','4∫[0,r](R²−x²)dx','8π∫[0,r](r²−x²)dx'),why='A section perpendicular to the common transverse coordinate is a rectangle with sides2√(R²−x²),2√(r²−x²); use even symmetry.')
row(2,70,f('Remaining volume',4*pi*(RR*RR-r*r)**R(3,2)/3),why='Washers have areaπ(R²−z²−r²) on |z|≤√(R²−r²).')
row(2,71,c('(a) end radius','r=R−ch²/4','r=R−ch/2','r=R+ch²/4'),c('(b) volume','πh(2R²+r²−2d²/5)/3, d=R−r','πh(R²+r²)/3','πh(2R²+r²+2d²/5)/3'),why='Evaluate radius R−cx² at±h/2, then integrateπ(R−cx²)² over the source interval.',limited=True)
row(2,72,c('V₂','V₁+2πkA','V₁+πk²A','V₁−2πkA'),why='At each x the new washer area differs by2πk(top−bottom); integrate the vertical height to obtain A.')
# 6.3, source printed453–455.
shells={1:(x,x*(x-1)**2,0,1),2:(x,s.sin(x*x),0,s.sqrt(pi)),3:(x,x**R(1,3),0,1),4:(x,x**3,1,2),5:(x,s.exp(-x*x),0,1),6:(x,3*x-x*x,0,3),7:(x,6*x-3*x*x,0,2),8:(x,s.sqrt(x)-x*x,0,1),9:(x,1/x,1,3),10:(x,x*x,0,2),11:(x,x**R(2,3),0,8),12:(x,-3*x*x+12*x-9,1,3),13:(x,1-(x-2)**2,1,3),14:(x,3*x-x*x,0,3),15:(3-x,8-x**3,0,2),16:(x+1,4-2*x,0,2),17:(x-1,4*x-x*x-3,1,3),18:(5-x,s.sqrt(x)-x/2,0,4),19:(2-x,s.sqrt(x/2),0,2),20:(x+2,1-x*x,-1,1),21:(x,x*s.exp(-x),0,2),22:(pi/2-x,s.tan(x),0,pi/4),23:(pi-x,2*s.cos(x)**4,-pi/2,pi/2),24:(x+1,2*x/(1+x**3)-x,0,1),25:(4-x,s.sqrt(s.sin(x)),0,pi),26:(5-x,4-s.sqrt(7+x*x),-3,3),35:(pi/2-x,s.sin(x)**2-s.sin(x)**4,0,pi/2),36:(x+1,x**3*s.sin(x),0,pi),37:(x,-x*x+6*x-8,2,4),42:(x-1,4-(x-3)**2,1,5)}
for num,(rad,hei,lo,hi) in shells.items():
 expr=2*pi*rad*hei; val=s.integrate(expr,(x,lo,hi)) if num not in [22,24,25] else s.Float(str(mp.quad(s.lambdify(x,expr,'mpmath'),[float(lo),float(hi)])),30)
 extra=[]
 if num in [1,2]:extra=[c('Shell circumference','2πx'),c('Shell height',fmt(hei)),c('Why shells are convenient','Avoid solving the source curve for two inverse branches','Shells require no integration','Every horizontal section is a disk')]
 if num in range(21,27):extra=[c('(a) shell integral','2π∫['+fmt(lo)+','+fmt(hi)+']('+fmt(rad)+')('+fmt(hei)+')d'+('y' if num in [25,26] else 'x'))]
 if num==8:extra=[c('Washer integral','π∫[0,1](y−y⁴)dy','π∫[0,1](y²−y⁴)dy','π∫[0,1](y−y²)dy')]
 row(3,num,n('Volume',val,tol=1e-5 if 21<=num<=26 else None),*extra,why='Use2π×radius×height. Radius='+fmt(rad)+', height='+fmt(hei)+', bounds '+fmt(lo)+' to '+fmt(hi)+'. The axis is '+('horizontal; x in this calculation stands for the source vertical coordinate y.' if num in [9,10,11,12,13,14,20,25,26,42] else 'vertical.')+(' For#35 use only one side of the symmetry axis to avoid double-counting identical shells.' if num==35 else ''),limited=num in [1,2,8])
 A.integrals.append(dict(qid=f'calculus-section-6-3-{num}',integrand=fmt(expr),lower=fmt(lo),upper=fmt(hi),value=fmt(val)))
row(3,27,n('Midpoint volume',sum(2*math.pi*t*math.sqrt(1+t**3)*.2 for t in [.1,.3,.5,.7,.9])),why='Five shell samples atx=.1,.3,.5,.7,.9, width.2.')
row(3,28,n('Midpoint volume estimate',4*pi*(1*2+3*4+5*3.8+7*2+9*2),tol=30),why='Five2-unit shell strips sample x=1,3,5,7,9. Read vertical heights approximately2,4,3.8,2,2 from the graph, then sum2πx·height·2.',limited=True)
for num,ans in [(29,'Rotate y=x⁴, y=0,0≤x≤3 about the y-axis'),(30,'Rotate x=ln y,x=0,1≤y≤3 about the x-axis'),(31,'Rotate x=1/y²,x=0,1≤y≤4 about y=−2'),(32,'Rotate 2^x≤y≤3^x,0≤x≤1 about x=2')]:row(3,num,c('One represented solid',ans,'Rotate the same region about x=−5','Rotate the same region about y=−5'),why='Read the shell integrand as2π times distance from axis times strip height.',limited=True)
for num,top,bot,br in [(33,x/(1+x*x),x*x-2*x,[(2,3)]),(34,s.exp(s.sin(x)),x*x-4*x+5,[(0,2),(2,4)])]:
 fn=s.lambdify(x,top-bot,'mpmath');roots=[mp.findroot(fn,z) for z in br];bounds=[mp.mpf(0),*roots] if num==33 else roots;expr=2*pi*x*(top-bot);v=mp.quad(s.lambdify(x,expr,'mpmath'),bounds)
 row(3,num,*[n('Intersection x '+str(i+1),z,tol=.0005) for i,z in enumerate(bounds)],n('Volume',v,tol=.001),why='Locate the two bounding intersections and integrate2πx(top−bottom), with positive x radius.',limited=True)
 A.integrals.append(dict(qid=f'calculus-section-6-3-{num}',integrand=fmt(expr),bounds=[str(z) for z in bounds],value=str(v)))
for num,expr,lo,hi in [(38,pi*(-x*x+6*x-8)**2,2,4),(39,pi*(3-x*x),-s.sqrt(3),s.sqrt(3)),(40,pi*(x*x-1),1,2),(41,pi*(1-(x-1)**2),0,2),(43,pi*((x+2)**2-((x-1)**2+1)**2),0,3)]:vol(3,num,expr,lo,hi)
row(3,44,c('a in terms of V','a=V/(2π)+2/3','a=V/(4π)+1/3','a=V/(2π)−2/3'),why='V=∫0^1 2π(a−x)(2x)dx=2πa−4π/3; solve for a>1.')
for num,ans in [(45,4*pi*r**3/3),(46,2*pi*pi*RR*r*r),(47,pi*r*r*h/3)]:row(3,num,f('Volume',ans),why='Integrate cylindrical shells with radius equal to the distance from the symmetry axis and height determined by the source surface.')
row(3,48,c('(a) comparison','Equal volumes for equal h','Larger sphere always leaves more wood','Wider hole always leaves more wood'),f('(b) volume in terms of h',pi*h**3/6),why='V=4π∫r^R x√(R²−x²)dx=4π(R²−r²)^(3/2)/3, and h=2√(R²−r²).',limited=True)
# 6.4, source printed458–460, g=9.8m/s² and source pound-force weights.
row(4,1,n('(a) work',7200,'ft·lb'),n('(b) work',7200,'ft·lb'),why='Work against gravity is weight×height, independent of the ascent duration.')
row(4,2,n('Work',5880,'J'),why='W=mgh=200×9.8×3.')
row(4,3,n('Work',4.5,'ft·lb'),why='Integrate5/x² from1ft to10ft: [−5/x]1^10=4.5ft·lb.')
row(4,4,n('Total work',0,'J'),n('Work from1 to1.5',3/pi*(1-s.sqrt(3)/2),'J'),n('Work from1.5 to2',-3/pi*(1-s.sqrt(3)/2),'J'),c('Interpretation','Equal positive and negative work cancel','The force is zero everywhere','All work is positive'),why='An antiderivative is(3/π)sin(πx/3); force changes sign at1.5.')
row(4,5,n('Work',180,'J'),why='Triangle area½·4·30 plus rectangle4·30.')
row(4,6,n('Midpoint work',4*(5.8+8.8+8.2+5.2),'J'),why='Four width4m intervals use samples6,10,14,18m.')
row(4,7,n('Work',3.75,'ft·lb'),why='k=10/(4/12)=30lb/ft; W=½k(6/12)².')
row(4,8,n('Work to compress10cm',3,'J'),n('Work to reach25cm length',6.75,'J'),why='k=60/.1=600N/m; compressions are.10m and.15m, measured from40cm natural length.')
row(4,9,n('(a) work',25/24,'J'),n('(b) extension',.108,'m'),why='2=½k(.12)² gives k=2500/9N/m; use½k(.10²−.05²), then30/k.')
row(4,10,n('Work',6.75,'ft·lb'),why='Spring work scales with extension squared:12(.75)².')
row(4,11,c('Relation','W₂=3W₁','W₂=W₁','W₂=2W₁'),why='The energy increments are proportional to.1² and.2²−.1².')
row(4,12,n('Natural length',8,'cm'),why='For natural length L, work increments obey10/6=[(14−L)²−(12−L)²]/[(12−L)²−(10−L)²]; solve L=8.')
work={13:[('a',s.Rational(1,2)*x,0,50),('b',s.Rational(1,2)*(50-x),0,25)],14:[('work',3*(60-x),0,25)],15:[('work',800+2*(500-x),0,500)],16:[('work',R(392,5)*x,0,6)],17:[('work',R(49,5)*(10+36-3*x+R(4,5)*(12-x)),0,12)],18:[('work',44-x/10,0,80)],19:[('work',R(5,4)*x,0,10)],20:[('work',R(125,2)*144*pi*(5-x),0,4)],21:[('work',19600*(1-x),R(1,2),1)],23:[('work',9800*8*x*(5-x),0,3)],24:[('work',9800*pi*(9-x*x)*(4-x),-3,3)],25:[('work',R(125,2)*pi*(3+R(3,8)*x)**2*(8-x),0,8)],26:[('work',R(125,2)*20*x*(6-x),0,6)],28:[('work',8820*pi*(9-x*x)*(4-x),-3,0)]}
for num,parts in work.items():
 fields=[]
 for label,expr,lo,hi in parts:
  val=s.integrate(expr,(x,lo,hi));fields +=[c('('+label+') integral','∫['+fmt(lo)+','+fmt(hi)+'] '+fmt(expr)+' dx'),n('('+label+') work',val,'J' if num in [16,17,21,23,24,27,28] else 'ft·lb')];A.integrals.append(dict(qid=f'calculus-section-6-4-{num}',integrand=fmt(expr),lower=fmt(lo),upper=fmt(hi),value=fmt(val)))
 if num==14:fields +=[c('(b) remaining cable weight','3(60−x) lb','3x lb','180 lb'),c('(b) small lift work','3(60−x)Δx ft·lb','3xΔx ft·lb','180x ft·lb')]
 row(4,num,*fields,why='Integrate force times lift distance for horizontal slices, or integrate remaining suspended weight along the lift. Water weight density is9800N/m³ or62.5lb/ft³; pound values are forces, not masses. Riemann terms are the displayed integrand at a sample point timesΔx.',limited=13<=num<=22)
row(4,22,n('Time',float(62.5*(4*pi*12**3/3)*72/(1.5*550)/3600),'hours',.001),why='Water center of mass ends at72ft. Work=62.5×sphere volume×72; divide by825ft·lb/s then3600s/h. Ideal pump; no loss.')
remaining=mp.findroot(lambda h:9800*8*(5*(9-h*h)/2-(27-h**3)/3)-470000,(1,2))
row(4,27,n('Remaining water depth',remaining,'m',.001),why='Pump top slices down from initial depth3 to remaining h. Solve9800·8∫h^3 y(5−y)dy=470000; the spout is5m above bottom.')
row(4,29,c('Work expression','W=∫[V₁,V₂]P(V)dV','W=∫[V₁,V₂]VdP','W=P(V₂)(V₂−V₁) always'),c('Differential relation','dV=πr²dx','dV=2πr dx','dV=dx/(πr²)'),why='Force=Pπr²; piston displacement dx produces dV=πr²dx. Substitute in∫Fdx.',limited=True)
row(4,30,n('Expansion work',160*100**1.4*(100**(-.4)-800**(-.4))/.4,'in·lb',.01),why='k=160·100^1.4; integrate kV^(−1.4) from100 to800in³. Units remain inch-pounds.')
row(4,31,c('(a) transformed work','∫[t₁,t₂]m v′(t)v(t)dt = ½m(v₂²−v₁²)','m(v₂−v₁)','½m(v₂−v₁)²'),n('(b) bowling-ball work',.5*(12/32)*(20*5280/3600)**2,'ft·lb'),why='dx=vdt and F=mv′. Substitute velocity; convert20mph to88/3ft/s and weight12lb to mass12/32slugs.',limited=True)
row(4,32,n('Speed',math.sqrt(2*(5.7*60**3/3+1.5*60**2/2)/800),'m/s'),why='Assuming launch from rest, integrate source force over0–60m and equate to½(800)v².')
row(4,33,c('(a) external lifting work','Gm₁m₂(1/a−1/b)','Gm₁m₂(1/b−1/a)','Gm₁m₂(b−a)'),n('(b) work',6.67e-11*5.98e24*1000*(1/6.37e6-1/7.37e6),'J',1e6),why='External quasistatic work against gravity is∫a^b Gm₁m₂/r²dr; use altitude above Earth, so final center distance7.37×10⁶m.')
Wp=150*756**2*481**2/12
row(4,34,n('(a) work',Wp,'ft·lb',1e5),n('(b) workers estimate',Wp/(10*20*340*200),tol=1),why='Horizontal slice area=756²(1−y/481)² and lifting distance y. Integrate weight density150 times area times y. Divide by each worker’s total200×10×340×20ft·lb.',limited=True)

# Recovered original same-edition source printed446, full source PDF page478.
# R2:0≤x≤1,x^(1/4)≤y≤1; R3:x≤y≤x^(1/4). O(0,0),A(1,0),B(1,1),C(0,1).
for num,expr in [(23,pi*(1-s.sqrt(x))),(24,pi*x**8),(25,pi*(1-(1-x**4)**2)),(26,pi*(1-x**R(1,4))**2),(27,pi*(s.sqrt(x)-x*x)),(28,pi*(x*x-x**8)),(29,pi*((1-x**4)**2-(1-x)**2)),(30,pi*((1-x)**2-(1-x**R(1,4))**2))]:
 vol(2,num,expr,0,1,why='Recovered source figure:O(0,0),A(1,0),B(1,1),C(0,1). R₂ lies above y=x^(1/4) in the unit square; R₃ lies between y=x and y=x^(1/4). Use washers about the indicated square edge.')
for no in range(23,31):
 A.out[f'calculus-section-6-2-{no}']['nativeFigures']=[dict(url='books/calculus/section-6-2-regions.svg',alt='Reconstructed unit square OABC: R2 above y=x^(1/4), R3 between y=x and y=x^(1/4).')]
row(2,64,c('Parallel-section integral','∫[0,4] (2y/√3)√(16−y²)dy','∫[0,4]π(16−y²)dy','∫[0,4]y√(16−y²)dy'),n('Wedge volume',128/(3*s.sqrt(3))),why='Recovered Example9 uses cylinder radius4 and plane angle30°. Sections parallel to the diameter are rectangles of width2√(16−y²), height ytan30°.',limited=True)
# Baseline section6.5 has explicit original derivations in calculus-expansion/author.py.
for qid,q in A.qs.items():
 if q['sourceSet']=='section-6-5':
  e=LIB[qid];assert e.get('grader');A.out[qid]={k:e[k] for k in ['grader','responsePartPrompt'] if k in e};A.out[qid].update(objectiveChecksVerified=True,objectiveCheckVersion=3,objectiveFieldCount=len(e['grader'].get('parts',[e['grader']])),answerCheckSource=dict(type='source-reviewed-original-calculation',title='Stewart8e section6.5; original authored mathematics in scripts/calculus-expansion',chapter=6))
  A.notes[qid]='Retained source-explicit contract; independently verified by scripts/calculus-expansion/check-math.py; complete original derivation remains in library.'
# Chapter6 review, all40 actual source records. Source printed466–467.
cs='-concept-check-1'
row('review',1,c('(a) vertical rectangle sum','Σ[f(xᵢ*)−g(xᵢ*)]Δx → ∫[a,b](f−g)dx','Σ[f(xᵢ*)+g(xᵢ*)]Δx','Σ[f(xᵢ*)−g(xᵢ*)]/Δx'),c('(b) horizontal version','Σ[f(yᵢ*)−g(yᵢ*)]Δy → ∫[c,d](f−g)dy','Always integrate with respect to x','Reverse right-minus-left to left-minus-right'),why='Area is rectangle height times width; choose top−bottom or right−left.',limited=True,suffix=cs)
row('review',2,c('Meaning','Sue’s distance lead after the first minute','Difference in finishing times','Sue’s speed at the end of the race'),why='The integral of velocity difference is displacement difference; both start together.',limited=True,suffix=cs)
row('review',3,c('(a) volume','ΣA(xᵢ*)Δx → ∫[a,b]A(x)dx','∫[a,b]√A(x)dx','A(b)−A(a)'),c('(b) revolution areas','Disk πR² or washer π(R²−r²)','2πR for every slice','π(R−r)² for every washer'),why='Thin slabs contribute cross-sectional area times thickness.',limited=True,suffix=cs)
row('review',4,c('(a) thin shell volume','2πrhΔr','πr²hΔr','2πr²h'),c('(b) volume integral','∫2π(radius)(height)d(radius)','∫2π(radius+height)dx','∫π(radius)²dx always'),c('(c) why shells','Can avoid inverse functions or splitting washer cross sections','Always requires fewer operations','Works only around the y-axis'),why='Use circumference times height times radial thickness.',limited=True,suffix=cs)
row('review',5,c('Meaning and units','Work done on the book; joules (N·m)','Force; newtons','Power; watts'),why='Force integrated over displacement has unitsN·m.',limited=True,suffix=cs)
row('review',6,c('(a) average','(1/(b−a))∫[a,b]f(x)dx','∫[a,b]f(x)dx','(f(a)+f(b))/2 always'),c('(b) theorem','For continuous f, some c∈[a,b] has f(c)=average; equal-area rectangle height f(c)','Every integrable f takes its average','The average always occurs at the midpoint'),why='Continuity and the intermediate value property ensure attainment of the integral average.',limited=True,suffix=cs)
rev_area={1:[(4*x-2*x*x,0,2)],2:[(s.sqrt(x)+x**R(1,3),0,1),(s.sqrt(x)-x+2,1,4)],3:[(2*(1-2*x*x-x),0,R(1,2))],4:[(-x*x-4*x,-4,0)],5:[(s.sin(pi*x/2)-x*x+2*x,0,2)],6:[(x*x-s.sqrt(x),1,2)]}
for num,pieces in rev_area.items():
 value=sum(s.integrate(expr,(x,lo,hi)) for expr,lo,hi in pieces);row('review',num,n('Area',value),why='Find the bounding intersections and integrate positive upper-minus-lower differences, splitting when the boundary changes.')
rev_vol={7:(pi*(4*x*x-x**4),0,2),8:(pi*((x+3)**2-(1+x*x)**2),-1,2),9:(pi*((10-x*x)**2-1),-3,3),10:(pi*((10-x*x)**2-(x*x+2)**2),-2,2),23:(9-x*x,-3,3),24:((2-2*x*x)**2,-1,1),25:(s.sqrt(3)*x*x/64,0,20)}
for num,(expr,lo,hi) in rev_vol.items():row('review',num,n('Volume',s.integrate(expr,(x,lo,hi))),why='Integrate cross-sectional area '+fmt(expr)+' over '+fmt(lo)+' to '+fmt(hi)+'.')
row('review',11,f('Volume',4*pi*(h*(2*a+h))**R(3,2)/3),why='Washer areaπ[(a+h)²−(a²+y²)] on |y|≤√(h(2a+h)).')
for num,ans in [(12,'2π∫[0,π/3]x(tan x−x)dx'),(13,'2π∫[−π/3,π/3](π/2−x)(cos²x−1/4)dx'),(14,'π∫[0,1][(2−x²)²−(2−√x)²]dx')]:row('review',num,c('Volume integral',ans),why='Use source bounding region and axis. Radius is distance to that axis; height is the positive curve difference.')
row('review',15,n('(a) x-axis volume',2*pi/15),n('(b) y-axis volume',pi/6),n('(c) y=2 volume',8*pi/15),why='Integrateπ(x²−x⁴),2πx(x−x²),π[(2−x²)²−(2−x)²] over0–1.')
row('review',16,n('(a) area',R(5,12)),n('(b) x-axis volume',s.integrate(pi*((2*x-x*x)**2-x**6),(x,0,1))),n('(c) y-axis volume',s.integrate(2*pi*x*(2*x-x*x-x**3),(x,0,1))),why='First-quadrant intersections are0 and1. The upper curve is2x−x².')
mids=[.125,.375,.625,.875]
row('review',17,n('(a) midpoint area',sum(math.tan(t*t)*.25 for t in mids)),n('(b) midpoint x-axis volume',sum(math.pi*math.tan(t*t)**2*.25 for t in mids)),why='Use width1/4 and source midpoint values, not an exact integral.')
r0=mp.findroot(lambda t:t**5+t-1,(.7,.8));top=1-x*x;bot=x**6-x+1;lo=0;hi=s.Float(str(r0),40)
row('review',18,n('(a) left x',0),n('(a) right x',r0,tol=.0005),n('(b) area',s.integrate(top-bot,(x,lo,hi)),tol=.0005),n('(c) x-axis volume',s.integrate(pi*(top**2-bot**2),(x,lo,hi)),tol=.0005),n('(d) y-axis volume',s.integrate(2*pi*x*(top-bot),(x,lo,hi)),tol=.0005),why='The nonzero crossing satisfies x⁵+x−1=0. Both curves are positive over the enclosed region.',limited=True)
for num,ans in [(19,'Rotate0≤y≤cos x,0≤x≤π/2 about the y-axis'),(20,'Rotate0≤y≤√2 cos x,0≤x≤π/2 about the x-axis'),(21,'Rotate sin x≤y≤2,0≤x≤π about y=2'),(22,'Rotate0≤x≤4y−y²,0≤y≤4 about y=6')]:row('review',num,c('One represented solid',ans,'Rotate the same region about x=−5','Rotate the same region about y=−5'),why='Identify disk/washer radius or shell radius and height from the stated integrand.',limited=True)
row('review',26,n('(a) volume',pi/3),c('(b) rearrangement','Two half-cones make one cone of radius1,height1','A cylinder of radius1,height1','A sphere of radius1'),why='Semicircle radius1−|x|; integrateπ(1−|x|)²/2 from−1 to1.',limited=True)
row('review',27,n('Work',3.2,'J'),why='k=30/.03=1000N/m, extension.08m; W=½k(.08)².')
row('review',28,n('Work',103500,'ft·lb'),why='Integrate1600+10(200−x) from0 to30ft.')
wv=62.5*4*math.pi*32/3;dep=mp.findroot(lambda h:250*mp.pi*(32/3-2*h*h+h**3/3)-4000,(1,3))
row('review',29,n('(a) work',wv,'ft·lb'),n('(b) remaining depth',dep,'ft',.001),why='At height y above bottom, radius²=4y and lift4−y. Integrate250πy(4−y); for remaining depth h, integrate fromh to4.')
row('review',30,n('Work',920*9.8*4*pi*(18-4.5),'J'),why='Cross-section4πm², lift6−y, oil depth0–3m; integrate920·9.8·4π(6−y).')
row('review',31,n('Average value',4/pi),why='∫sec²t dt=tan t; divide by interval lengthπ/4.')
row('review',32,n('(a) average',R(2,3)),n('(b) c',R(9,4)),n('(c) equal-area rectangle height',R(2,3)),why='Integral2 divided by width3; solve1/√c=2/3. Rectangle spans1≤x≤4.',limited=True)
row('review',33,c('Limit','f(x)','f′(x)','0'),why='Average over[x,x+h] is a difference quotient for an antiderivative; continuity gives f(x).')
row('review',34,c('(a) equal areas','No positive b','b=1','Every positive b'),n('(b) b',2.5),c('(c) equal x-axis volumes','No positive b','b=1','Every positive b'),c('(d) equal y-axis volumes','Every positive b','No positive b','Only b=1'),why='Areas b³/3 and2b³/3. R₁ x-volumeπb⁵/5, y-volumeπb⁴/2. R₂ x-volume4πb⁵/5, y-volumeπb⁴/2.')
# Problems Plus, source printed468–470.
def pp(num,*fields,why='',limited=False):row('problems-plus',num,*fields,why=why,limited=limited,suffix='-problems-plus-0')
pp(1,c('(a) f(x)','3x²'),c('(b) f(x)','√(2x/π)'),why='Differentiate area t³ and volume b². For(b), πf(b)²=2b and positivity selects the positive root.')
pp(2,n('Slope',1-2**(-1/3)),why='Line y=mx intersects parabola atx=1−m. The cap above the line has area(1−m)³/6, half of total1/6.')
pp(3,n('c',R(32,27)),why='Equal shaded regions mean∫0^b[8x−27x³−c]dx=0 with c=8b−27b³. Elimination gives b=4/9 and c=32/27.')
# PP3 elimination: −4b²+(81/4)b⁴=0 gives b=4/9; c=8b−27b³=32/27.
pp(4,c('(a) rectangular slices integral','(L/r)∫[−r,r](r−x)√(r²−x²)dx'),c('(b) trapezoid slices integral','∫[−r,r]L√(r²−y²)dy'),f('(c,d) remaining water',pi*r*r*s.Symbol('L')/2),c('(d) geometric reason','The oblique plane bisects the cylinder by central symmetry','All cross sections are circles','The remaining water fills the whole cylinder'),c('(e) rectangular slices integral','(2L/r)∫[0,r]x√(r²−x²)dx'),c('(e) remaining volume','2Lr²/3'),why='Use coordinates attached to the cylinder. Full-base case water height=L(r−x)/(2r); half-base case height=Lx/r for x≥0. Multiply by chord width2√(r²−x²). Slice parallel to the slope for triangles, perpendicular to the cylinder axis for circular segments.',limited=True)
pp(5,c('(a) cap volume','πh²(3r−h)/3'),c('(b) root equation','3x³−9x+2=0'),n('(b) x',mp.findroot(lambda t:3*t**3-9*t+2,.2),tol=.00005),n('(c) submerged depth',mp.findroot(lambda t:t**3-1.5*t*t+.375,.65),'m',.00005),n('(d-i) rise rate',.2/(21*pi),'in/s'),n('(d-ii) time',370*pi/3,'s'),why='Integrate circular sectionsπ(2rz−z²). For the bowl dV/dh=πh(10−h); evaluate at3. Remaining volume fromdepth4 to5 is74π/3in³, divided by0.2.',limited=True)
pp(6,c('(a) percentage above surface','100(ρf−ρ₀)/ρf'),n('(b) iceberg above water',100*(1030-917)/1030,'%'),c('(c) overflow','No, assuming unchanged temperature/density of the freshwater','Yes, all melted ice adds extra volume','Yes, by the entire iceberg volume'),n('(d) submersion work',9800*(4*pi*.4**4/3),'J'),why='Buoyancy equals object weight in equilibrium. Melting freshwater ice occupies exactly its displaced-water volume. Negligible-weight sphere starts just touching the surface; integrate buoyancy through depth2r.',limited=True)
pp(7,c('Depth rate','dh/dt=−k (constant), when dV/dt=−kA(h)','dh/dt=−kA(h)','dh/dt=−k/A(h)'),why='Chain rule dV/dt=(dV/dh)h′=A(h)h′; cancel positive surface area.',limited=True)
pp(8,n('Maximizing r',2/s.sqrt(5)),why='Let d=√(1−r²). Outside volume is small hemisphere2πr³/3 minus big capπ(1−d)²(1−(1−d)/3). Differentiation gives r=2d; endpoints have smaller volumes.')
pp(9,c('Curve C','y=8x², x≥0','y=4x², x≥0','y=3x², x≥0'),why='At P=(a,2a²), A=a³/3. Differentiate the horizontal-area equality for B: √(y/2)−x_C(y)=√y/(2√2), so x_C=√y/(2√2).')
pp(10,c('Optimal ball radius','h sinθ / [(1−sinθ)(1+2sinθ)]','h sinθ/(1+sinθ)','h tanθ'),why='Ball center is r/sinθ above the tip. Submerged cap height H=h−r(1/sinθ−1), and displaced volumeπH²(r−H/3). Differentiate within the side-contact domain and compare fully submerged/rim-contact endpoints. Assume0<θ<π/2.')
pp(11,c('(a) V(h)','π∫[0,h]f(y)²dy'),c('(b) rate','dV/dt=πf(h)² dh/dt'),c('(c) f(y)','√(kA/(πC)) y^(1/4), with k<0,C<0'),c('(c) advantage','Equal vertical spacing of marks represents equal time intervals','The outflow volume rate is constant','No calibration is needed'),why='FTC and chain rule yieldπf(h)²C=kA√h. Both k,C are negative, making their ratio positive.',limited=True)
pp(12,c('(a) h before dry core or overflow','V/(πr²)−ω²r²/(4g)'),c('(b) bottom-touch threshold with conserved V','ω=√(4gV/(πr⁴)), valid before overflow'),c('(b) first-spill threshold, H=V/(πr²)','√(4g(L−H)/r²) if H≥L/2; L√(πg/V) if H≤L/2'),n('(c-i) angular speed, using g=32ft/s²',8,'rad/s'),n('(c-i) volume',16*pi,'ft³'),n('(c-ii) depth below rim at wall',1,'ft'),why='Integrate h+ω²ρ²/(2g) over horizontal disks. The initial conserved-volume formula needs h≥0. If a dry core forms first, integrate only the wet annulus for overflow; this yieldsω=L√(πg/V). Given profile is y=2+x², givingω=8 and wallheight6. If spill occurs first, later bottom contact is atω=√(2gL/r²).',limited=True)
pp(13,c('Relation','b=2a','b=3a','b=√2 a'),why='Cubic-minus-parabola equalsk x(x−a)(x−b). Equal lobes mean its signed integral0→b vanishes, giving kb³(2a−b)/12=0.')
from scipy.optimize import minimize_scalar
fun=lambda rr:float(mp.quad(lambda t:rr*mp.sqrt(16-t*t)-rr*rr/2*mp.sin(2*mp.sqrt(16-t*t)/rr),[-4,0,4]))
opt=minimize_scalar(lambda rr:-fun(rr),bounds=(4/math.pi,8),method='bounded',options={'xatol':1e-11})
pp(14,c('(a) section area','r√(16−x²)−(r²/2)sin(2√(16−x²)/r)'),c('(a) volume','∫[−4,4][r√(16−x²)−(r²/2)sin(2√(16−x²)/r)]dx'),n('(b) maximizing radius',opt.x,'in',.002),why='Circular segment area equals sector area minus triangle area. Integrate along the tortilla diameter; optimize for r≥4/π to avoid overlapping edges.',limited=True)
pp(15,c('Area relationship','B=16A','B=8A','B=4A'),why='At tangency abscissa a, the other intersection is−2a; enclosed area is proportional to a⁴. Repeating at−2a multiplies area by16 (a≠0).')
A.save()
audit_path=ROOT/'scripts/calculus-answer-checks/chapter-06/source-audit.json'
audit=json.loads(audit_path.read_text());audit.update(scope='The285 original Chapter6 records, including projects, review and Problems Plus. The22 additionally restored6.2#1–22 records are independently authored in recovered-446.json, bringing total Chapter6 coverage to307.',reviewedPrintedPages=[*range(434,438),*range(446,451),*range(453,456),*range(458,462),*range(463,471)],recoveredSource=dict(url='https://s3.amazonaws.com/scschoolfiles/3191/calculus_early_transcendentals_james_stewart_8th_edition.pdf',title='Stewart Calculus: Early Transcendentals,8th edition',printedPage=446,fullPdfPage=478,reason='The supplied chapter excerpt skips printed446. The full original textbook matches the edition, surrounding page headings and exercise continuation numbers; page446 supplies the square diagram referred to by6.2#23–30 and Example9 used by#64.',figure='O(0,0),A(1,0),B(1,1),C(0,1); y=x and y=x^(1/4). R2 above fourth-root; R3 between the two curves.'),mathVerification=['chapter-06/check-math.py independent adaptive quadrature, washer/shell cross-checks and physical identities','scripts/calculus-expansion/check-math.py:307 retained section5.5/6.5 checks'],visualReview='Source exercise graphs, dimensions, labels, shared instructions, referenced figures and model domains were inspected. Graph estimates carry explicit tolerances.',notAssessed='Freehand sketches, complete proofs, open-ended model discussions and original research reports remain explicitly limited recognition checks.')
audit_path.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
