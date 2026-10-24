from common import *
PAR=[];CON=[]
def pair(a,b):return '('+fmt(a)+','+fmt(b)+')'
def para(no,h,k,p,vertical=True,eq=None,limited=True):
 focus=(h,k+p) if vertical else(h+p,k);direct=('y='+fmt(k-p)) if vertical else('x='+fmt(h-p));fields=[c('Vertex',pair(h,k)),c('Focus',pair(*focus)),c('Directrix',direct)]
 if eq:fields.insert(0,c('Equation',eq))
 fields.append(c('Opening',('Upward' if p>0 else'Downward') if vertical else('Rightward' if p>0 else'Leftward')))
 row(5,no,*fields,why='Translate to vertex(h,k), then use(x−h)²=4p(y−k) or(y−k)²=4p(x−h). The signed distancep locates focus and directrix on opposite sides.',limited=limited);PAR.append((no,s.sympify(h),s.sympify(k),s.sympify(p),vertical))
for args in [(1,0,0,R(3,2),True),(2,0,0,R(5,8),False),(3,0,0,-R(1,2),False),(4,0,0,-R(2,3),True),(5,-2,3,2,True),(6,-R(1,2),2,R(1,2),False),(7,4,-3,-R(1,2),False),(8,4,2,R(3,8),True)]:para(*args)
para(9,0,0,-R(1,4),False,'x=−y²',False)
para(10,2,-2,R(1,2),True,'y=(x−2)²/2−2',False)
def con(no,h,k,a2,b2,vertical=False,hyper=False,eq=None,limited=True):
 a2,b2=s.sympify(a2),s.sympify(b2)
 a=s.sqrt(a2);cc=s.sqrt(a2+b2 if hyper else a2-b2)
 verts=[(h,k-a),(h,k+a)] if vertical else[(h-a,k),(h+a,k)]
 foc=[(h,k-cc),(h,k+cc)] if vertical else[(h-cc,k),(h+cc,k)]
 fields=[c('Type','Hyperbola' if hyper else'Ellipse'),c('Vertices',' and '.join(pair(*z) for z in verts)),c('Foci',' and '.join(pair(*z) for z in foc))]
 if eq:fields.insert(0,c('Standard equation',eq))
 if hyper:fields.append(c('Asymptotes','y−('+fmt(k)+')=±'+fmt(s.sqrt(a2/b2) if vertical else s.sqrt(b2/a2))+'(x−('+fmt(h)+'))'))
 row(5,no,*fields,why='Complete squares and divide to get standard form. For an ellipsec²=a²−b²; for a hyperbolac²=a²+b². The positive squared term determines the hyperbola transverse axis; the larger denominator determines the ellipse major axis.',limited=limited);CON.append((no,s.sympify(h),s.sympify(k),s.sympify(a2),s.sympify(b2),vertical,hyper))
for args in [(11,0,0,4,2,True),(12,0,0,36,8,False),(13,0,0,9,1,False),(14,0,0,R(25,4),R(9,4),True),(15,1,0,9,4,True),(16,-1,2,3,1,False)]:con(*args)
con(17,0,0,9,4,True,eq='x²/4+y²/9=1',limited=False)
con(18,2,1,9,4,eq='(x−2)²/9+(y−1)²/4=1',limited=False)
for args in [(19,0,0,25,9,True),(20,0,0,36,64,False),(21,0,0,100,100,False),(22,0,0,16,1,True),(23,0,1,1,1,False),(24,-1,2,4,9,True)]:con(*args,hyper=True)
con(25,0,0,1,4,hyper=True,eq='x²−y²/4=1',limited=False)
para(26,0,-4,R(1,16),True,'x²=(y+4)/4',False)
con(27,0,1,2,1,eq='x²/2+(y−1)²=1',limited=False)
con(28,1,0,1,1,True,True,'y²−(x−1)²=1',False)
para(29,1,-2,R(1,6),True,'(x−1)²=(2/3)(y+2)',False)
con(30,1,2,2,1,eq='(x−1)²/2+(y−2)²=1',limited=False)
for no,eq,why in [(31,'y²=4x','Vertex0, focusdistancep=1.'),(32,'x²=−12(y−3)','Vertex halfway between focusy=0 anddirectrixy=6 is(0,3);p=−3.'),(33,'y²=−12(x+1)','Vertexx=−1,p=−3.'),(34,'(x−2)²=−16(y−3)','Vertical axis andp=−4.'),(35,'(y+1)²=−(x−3)/2','At(−15,2),9=4p(−18),sop=−1/8.'),(36,'y=−2x²+x+4','Fitquadraticy=Ax²+Bx+C to the three given points.'),(37,'x²/25+y²/21=1','a=5,c=2,b²=21.'),(38,'x²/2+y²/4=1','Verticala=2,c=√2,b²=2.'),(39,'x²/12+(y−4)²/16=1','Center(0,4),a=4,c=2,b²=12.'),(40,'(x−4)²/25+(y+1)²/9=1','Center(4,−1),a=5,c=4,b²=9.'),(41,'(x+1)²/12+(y−4)²/16=1','Verticala=4,c=2,b²=12.'),(42,'x²/25+y²/9=1','At(−4,1.8), distances to the foci are1.8and8.2, giving2a=10;c=4.'),(43,'x²/9−y²/16=1','a=3,c=5,b²=16.'),(44,'y²/4−x²/21=1','Verticala=2,c=5,b²=21.'),(45,'(y−1)²/25−(x+3)²/39=1','Center(−3,1),a=5,c=8,b²=39.'),(46,'(x−3)²/16−(y−2)²/9=1','Center(3,2),a=4,c=5,b²=9.'),(47,'x²/9−y²/36=1','a=3,b/a=2 givesb=6.'),(48,'(y−4)²/(16/5)−(x−2)²/(64/5)=1','Asymptotes meet at(2,4);c=4 andslopea/b=1/2 implya²=16/5,b²=64/5.')]:row(5,no,c('One equation in the stated coordinates',eq),why=why)
row(5,49,c('Ellipse with center at origin and major axis horizontal','x²/3763600+y²/3753196=1 (coordinates inkm)'),n('Semimajor axis',1940,'km'),n('Focus offset',102,'km'),why='Add the Moon radius to each altitude: nearest/farthest focus distances1838and2042km. Thena=(1838+2042)/2=1940,c=(2042−1838)/2=102,b²=a²−c². A translation/rotation gives equivalent equations; the stated convention fixes one.')
row(5,50,c('(a) equation with vertexorigin and axis+x','y²=10x (cm units)'),n('(b) opening diameter atx=11',2*s.sqrt(110),'cm',.00005),why='The focus liesp from the vertex and the latus-rectum opening is4p=10cm, sop=2.5. Atx=11, y=±√110, so diameter is2√110, not a radius.')
a=R(1225,11);b2=40000-a*a
row(5,51,c('(a) coordinates','Origin midpoint of stations;A=(−200,0),B=(200,0), distances in miles'),c('(a) hyperbola','x²/(1225/11)²−y²/[40000−(1225/11)²]=1, right branchx>0'),n('(b) distance north ofB',b2/a,'mi',.00005),why='The earlier B signal meansPA−PB>0, selecting the right branch. Convert980ft/μs·1200μs to miles, then set this difference2a. Focaldistancec=200mi; atx=c, y=b²/a.')
row(5,52,c('Standard equation','x²/a²−y²/(c²−a²)=1'),c('Parameter condition','c>a>0 andb²=c²−a²'),c('Distance condition','|distance to(−c,0)−distance to(c,0)|=2a'),why='Square the defining distance-difference relation twice, keeping both branches via the absolute value. The resulting positiveb² requiresc>a.',limited=True)
row(5,53,c('Upper branch','y=(a/b)√(b²+x²), a,b>0'),c('Second derivative','y″=ab/(b²+x²)^(3/2)>0'),why='Differentiate the positive square-root branch twice. Positivity ofa,b makes the numerator and denominator positive at everyx.',limited=True)
row(5,54,c('Rotated ellipse equation','3x²−2xy+3y²=8'),c('Principal coordinates','u=(x+y)/√2,v=(x−y)/√2;u²/4+v²/2=1'),why='The foci lie on the liney=x withc=√2. Majoraxislength4 givesa=2,b²=2. Rotate byπ/4 and expand.')
row(5,55,c('(a) k>16','Ellipse with major axis horizontal'),c('(b)0<k<16','Hyperbola with transverse axis horizontal'),c('(c)k<0','No real points'),c('(d) common foci','(−4,0) and(4,0)'),why='For the ellipse,c²=k−(k−16)=16. For the hyperbola,c²=k+(16−k)=16. Ifk<0 both squared-term denominators are negative, so their sum cannot equal1. k=0,16 are excluded undefined denominators.',limited=True)
row(5,56,c('(a) tangent equation','y₀y=2p(x+x₀)'),c('(b) x-intercept','(−x₀,0)'),why='Implicit differentiation gives2yy′=4p. The tangent through(x₀,y₀), together withy₀²=4px₀, simplifies to the symmetric equation. At the vertex the tangent isx=0, consistent with the intercept.',limited=True)
row(5,57,c('Tangent slopes from(q,−p)','m₁m₂=−1'),c('Contact-abscissa equation','x₀²−2qx₀−4p²=0'),why='The tangent at(x₀,x₀²/(4p)) isx₀x=2py+x₀²/2. Substituting the directrix point produces the quadratic; its root product−4p² divided by(2p)² gives−1. Assume a nondegenerate parabolap≠0.',limited=True)
row(5,58,c('Intersection tangent angle','π/2 radians'),c('Key parameter relation','a_ellipse²−b_ellipse²=a_hyperbola²+b_hyperbola²=c²'),why='The shared foci make the gradient of the sum of focal distances perpendicular to the gradient of their difference: (u₁+u₂)·(u₁−u₂)=|u₁|²−|u₂|²=0. Normals, hence tangents, are perpendicular at regular intersections.',limited=True)
def simpson(fn,a,b,N):
 h=(b-a)/N;return h/3*(fn(a)+fn(b)+4*sum(fn(a+i*h) for i in range(1,N,2))+2*sum(fn(a+i*h) for i in range(2,N,2)))
for no,aa,bb,N,unit in [(59,2,3,8,'units'),(60,mp.mpf('5.9e9'),mp.mpf('5.7e9'),10,'km')]:
 fn=lambda z:mp.sqrt(aa*aa*mp.sin(z)**2+bb*bb*mp.cos(z)**2);v=4*simpson(fn,mp.mpf(0),mp.pi/2,N)
 row(5,no,n('Simpson estimate usingn='+str(N)+' panels on one quadrant, then×4',v,unit, .000005 if no==59 else 500),c('Parametrization','x='+str(aa)+'cos t,y='+str(bb)+'sin t'),why='Exploit fourfold symmetry and apply the specified Simpson panel count to0≤t≤π/2. This convention is explicit because usingn panels on the entire0..2π interval gives a different finite-panel approximation. Arc speed is√(a²sin²t+b²cos²t).')
 near(str(no)+' Simpson vs high-precision arc integral',v,4*mp.quad(fn,[0,mp.pi/2]),1e-6)
row(5,61,c('Area, c=√(a²+b²)','b²c/a−ab ln[(b+c)/a]'),why='For the right focus, integrate2(b/a)√(x²−a²) fromx=a tox=c. The left focus gives the same area by symmetry. Use the standard radical primitive andc²−a²=b².')
row(5,62,c('(a) major-axis rotation volume','4πab²/3'),c('(b) minor-axis rotation volume','4πa²b/3'),why='Assumea≥b>0 are the major/minor semiaxes. Disk integration gives the ellipsoid volume4π times the product of its three semiaxes divided by3.')
row(5,63,n('Centroid x',0),n('Centroid y',4/pi),why='The upper half ellipse has semiaxes2and3. Symmetry givesx̄=0; a half-ellipse centroid hasȳ=4b/(3π)=4/π, from the area and first moment integrals.')
row(5,64,c('(a) major-axis surface, e=√(1−b²/a²)','2πb²[1+a·arcsin(e)/(b e)]'),c('(b) minor-axis surface','2πa²[1+(1−e²)atanh(e)/e]'),c('Circular limit a=b','Both formulas limit to4πa²'),why='Rotate the ellipse witha≥b>0. Use circumference times arc length; the prolate integral producesarcsin and the oblate integralatanh. At e=0 use the continuous limit instead of dividing byzero.')
row(5,65,c('Reflection-angle conclusion','α=β'),c('Normal direction','The sum of the two unit vectors from the foci towardP'),why='The ellipse is a level set of the sum of distances to its foci. Its gradient is the sum of the corresponding unit vectors, which bisects their angle. Therefore their angles to the tangent are equal, giving reflection from one focus to the other.',limited=True)
row(5,66,c('Reflection-angle conclusion','α=β'),c('Normal direction','The difference of the two unit vectors from the foci towardP, with branch-dependent sign'),why='A hyperbola is a level set of the difference of focal distances. Its normal is the difference of unit focal vectors, while their sum is perpendicular to that normal. This angle-bisector geometry yields the stated equal tangent angles.',limited=True)
# Independently verify geometric definitions at sample points for each authored standard conic.
for no,h,k,p,v in PAR:
 for z in [R(-3,2),R(1,3),2]:
  xx,yy=(h+z,k+z*z/(4*p)) if v else(h+z*z/(4*p),k+z)
  fx,fy=(h,k+p) if v else(h+p,k)
  distline=yy-(k-p) if v else xx-(h-p)
  check(str(no)+' focus directrix at'+str(z),(xx-fx)**2+(yy-fy)**2-distline**2)
for no,h,k,a2,b2,v,hyp in CON:
 aa=mp.sqrt(float(a2));bb=mp.sqrt(float(b2));cc=mp.sqrt(float(a2+b2 if hyp else a2-b2))
 for z in [.3,1.1]:
  along=aa*mp.cosh(z) if hyp else aa*mp.cos(z);across=bb*mp.sinh(z) if hyp else bb*mp.sin(z)
  d1=mp.sqrt((along-cc)**2+across**2);d2=mp.sqrt((along+cc)**2+across**2)
  near(str(no)+' focal definition at'+str(z),abs(d2-d1) if hyp else d1+d2,2*aa)
check('36 three point fit',sum((-2*xx**2+xx+4-yy)**2 for xx,yy in [(0,4),(1,3),(-2,-6)]))
check('42 supplied point',R(16,25)+R(9,5)**2/9-1)
check('49 semiminor',1940**2-102**2-3753196)
near('51 time-distance conversion',2*a,1200*980/5280)
finish('section05',[680,681,682])
