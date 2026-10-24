from common import *
R=s.Rational
rad=math.radians
row(2,1,*[c('('+l+') '+name,ans,'Vector' if ans=='Scalar' else 'Scalar') for l,name,ans in [('a','Ticket cost','Scalar'),('b','River current','Vector'),('c','Initial flight path','Vector'),('d','Population','Scalar')]],why='Magnitude alone gives a scalar; current and flight direction require direction as well.',limited=True)
row(2,2,c('Relationship','The vector is the directed displacement from(0,0) to the point(4,7)','The point is a direction with no location','The vector must start at(4,7)'),why='A point is a location; the same coordinate tuple specifies the position vector from the origin. Translated arrows can represent the same vector.',limited=True)
row(2,3,c('Equal displayed vectors','AB=DC; DA=CB; DE=EB; CE=EA','AB=CD; DA=BC; DE=BE','AB=DA; DE=CE'),why='Opposite sides of a parallelogram have equal same-direction displacements; its diagonals bisect each other.',limited=True)
row(2,4,*[c(l,a,*b) for l,a,b in [('(a)','AC',['CA','AB']),('(b)','CB',['BC','CD']),('(c)','DA',['AD','DB']),('(d)','DB',['BD','CA'])]],why='Write each directed segment XY as Y−X and cancel intermediate endpoints.')
for k,labels,coeffs in [(5,['u+v','u+w','v+w','u−v','v+u+w','u−w−v'],[(1,1,0),(1,0,1),(0,1,1),(1,-1,0),(1,1,1),(1,-1,-1)]),(6,['a+b','a−b','a/2','−3b','a+2b','2b−a'],[(1,1),(1,-1),(.5,0),(0,-3),(1,2),(-1,2)])]:
 names=('u','v','w') if k==5 else ('a','b')
 fields=[]
 for l,co in zip(labels,coeffs):
  construction='Then '.join(f'{abs(t):g} times {name}, '+('same direction' if t>0 else 'opposite direction')+'. ' for name,t in zip(names,co) if t)
  fields.append(c(l+' head-to-tail construction',construction,'Reverse every listed arrow without changing its length','All arrows must start at the same tail and their heads are joined'))
 row(2,k,*fields,why='Construct each scaled arrow in the indicated direction, place successive tails at preceding heads, and draw the resultant from the initial tail to the final head. These checks assess the construction recipe rather than the finished drawing.',limited=True)
row(2,7,c('c','(a+b)/2','(a−b)/2','a+b'),c('d','(b−a)/2','(a−b)/2','a+b'),why='Take P as origin: Q=a,R=b and midpoint M=(a+b)/2. Thus PM=c and MR=b−M=d.')
row(2,8,n('|w|',s.sqrt(2)),why='w=−(u+v); perpendicular unit vectors have sum length√2.')
for k,A,B in [(9,(-2,1),(1,2)),(10,(-5,-1),(-3,3)),(11,(3,-1),(2,3)),(12,(3,2),(1,0)),(13,(0,3,1),(2,3,-1)),(14,(0,6,-1),(3,4,4))]:
 row(2,k,*vec('AB',V(*B)-V(*A)),why='Subtract initial coordinates from terminal coordinates. The equivalent arrow from the origin ends at this difference tuple.',limited=True)
for k,a,b in [(15,(-1,4),(6,-2)),(16,(3,-1),(-1,5)),(17,(3,0,1),(0,8,0)),(18,(1,3,-2),(0,0,6))]:row(2,k,*vec('Sum',V(*a)+V(*b)),why='Add corresponding components; place the second arrow at the head of the first.',limited=True)
for k,a,b in [(19,(-3,4),(9,-1)),(20,(5,3),(-1,-2)),(21,(4,-3,2),(2,0,-4)),(22,(8,1,-4),(5,-2,1))]:
 a,b=V(*a),V(*b);row(2,k,*vec('a+b',a+b),*vec('4a+2b',4*a+2*b),n('|a|',a.norm()),n('|a−b|',(a-b).norm()),why='Add and scale componentwise; magnitudes are square roots of sums of component squares.');check(str(k)+' norm',a.dot(a)-a.norm()**2)
for k,a,length in [(23,(6,-2),1),(24,(-5,3,-1),1),(25,(8,-1,4),1),(26,(6,2,-3),4)]:
 a=V(*a);v=length*a/a.norm();row(2,k,*vec('Requested vector',v),why='Divide by the positive norm to preserve direction, then multiply by the requested length.');check(str(k)+' length',v.dot(v)-length**2)
row(2,27,n('Angle',60,'degrees'),why='cosθ=1/√(1+3)=1/2 and the vector lies in the first quadrant.')
row(2,28,n('Angle',math.degrees(math.atan2(6,8)),'degrees',.005),why='The first-quadrant angle is arctan(6/8).')
row(2,29,*vec('v',(2,2*s.sqrt(3))),why='Resolve magnitude4 atπ/3 into4cos(π/3),4sin(π/3).')
for k,m,a,u in [(30,50,38,'N'),(31,60,40,'ft/s')]:row(2,k,n('Horizontal component',m*math.cos(rad(a)),u,.005),n('Vertical component',m*math.sin(rad(a)),u,.005),why='The angle is measured above horizontal, so horizontal=magnitude·cosθ and vertical=magnitude·sinθ.')
for k,v,u in [(32,V(20*s.sqrt(2)/2+8*s.sqrt(3),20*s.sqrt(2)/2-8),'lb'),(33,V(-200,100*s.sqrt(3)),'N')]:row(2,k,n('Resultant magnitude',v.norm(),u,.005),n('Angle counterclockwise from +x',math.degrees(math.atan2(float(v[1]),float(v[0]))),'degrees',.005),why='Add horizontal and vertical components before finding magnitude and the quadrant-correct atan2 angle.')
east=250*math.sin(rad(60))+50*math.sin(rad(45));north=250*math.cos(rad(60))-50*math.cos(rad(45))
row(2,34,n('True course: degrees east of north',math.degrees(math.atan2(east,north)),'degrees',.005),n('Ground speed',math.hypot(east,north),'km/h',.005),why='Wind FROM northwest blows southeast. Add its positive east and negative north components to the airplane air velocity.')
row(2,35,n('Speed',math.sqrt(493),'mi/h',.005),n('Direction: degrees west of north',math.degrees(math.atan2(3,22)),'degrees',.005),why='The velocity relative to water is(−3,22) in east,north coordinates.')
row(2,36,*[n(l,v,'lb',.005) for l,v in [('Left-end cable x',250/s.sqrt(3)),('Left-end cable y',250),('Right-end cable x',-250/s.sqrt(3)),('Right-end cable y',250),('Each magnitude',500/s.sqrt(3))]],why='Forces ON the beam point upward toward the hook. Vertical components share500lb equally; each cable is60° above the beam.')
a,b=rad(50),rad(38);t1=350*math.cos(b)/math.sin(a+b);t2=350*math.cos(a)/math.sin(a+b)
row(2,37,n('2m rope tension magnitude',t1,'N',.005),n('3m rope tension magnitude',t2,'N',.005),n('2m rope x component',-t1*math.cos(a),'N',.005),n('2m rope y component',t1*math.sin(a),'N',.005),n('3m rope x component',t2*math.cos(b),'N',.005),n('3m rope y component',t2*math.sin(b),'N',.005),why='Horizontal forces cancel and vertical components sum to350N; lengths do not enter this static equilibrium once angles are given.')
row(2,38,n('Weight',50*math.sin(rad(37)),'N',.005),why='Two equal upward tension components25sin37° balance the chain weight.')
# Across velocity3/t, upstream velocity2/t, so boat upstream component2/t+3.5.
u=(-14+math.sqrt(14**2+4*156.75*13))/(2*13);t=1/u
row(2,39,n('(a) Steering upstream from straight across',math.degrees(math.atan2(2*u+3.5,3*u)),'degrees',.005),n('(b) Trip time',60*t,'minutes',.005),why='With upstream positive, boat velocity relative to water is(3/t,2/t+3.5). Set its squared norm to13², take positive t, then compute the steering angle.')
row(2,40,n('Counterbalancing force magnitude',math.sqrt(25**2+12**2+2*25*12*math.cos(rad(100))+4**2),'N',.005),why='The in-plane resultant squared uses the cosine dot-product term; add the perpendicular force squared. Negation leaves magnitude unchanged.')
row(2,41,c('Both unit vectors','±(1,4)/√17','±(4,1)/√17','±(1,2)/√5'),why='Tangent slope atx=2 is4; normalize(1,4).')
row(2,42,c('(a) Tangent unit vectors','±(1/2,√3/2)','±(√3/2,1/2)','±(1,√3)'),c('(b) Normal unit vectors','±(−√3/2,1/2)','±(1/2,√3/2)','±(−1,√3)'),c('(c) Common starting point','(π/6,1)','(0,0)','(π/3,1)'),why='The slope2cos(π/6)=√3 determines the tangent. Rotate a unit tangent by90° to get a unit normal.',limited=True)
row(2,43,c('Sum','Zero vector','AB','AC'),why='(B−A)+(C−B)+(A−C)=0.')
row(2,44,c('Position vector','c=(2a+b)/3','c=(a+2b)/3','c=(a+b)/2'),c('Displacement ratio','AC=AB/3 and CB=2AB/3','AC=2AB/3','C is the midpoint'),why='Twice as far from B as from A means AC:CB=1:2. Thus c=a+(b−a)/3.',limited=True)
row(2,45,n('(c,d) s',1),n('(c,d) t',2),c('(a,b) Component identity','(7,1)=(3,2)+2(2,−1)','(7,1)=2(3,2)+(2,−1)','(7,1)=(3,2)+(2,−1)'),why='Solve3s+2t=7 and2s−t=1; s=1,t=2. The head-to-tail construction uses one a and two b arrows.',limited=True)
row(2,46,c('Geometric construction','Resolve c along the two nonparallel side directions of a parallelogram','Only perpendicular vectors can span a plane','Every c must be a scalar multiple of a'),c('Component justification','The 2×2 coordinate matrix with columns a,b has nonzero determinant, so its system for s,t has a unique solution','The determinant is always zero','Set s=t=1 for all c'),why='Nonparallel nonzero vectors form a basis of their plane; invertibility gives existence and uniqueness.',limited=True)
row(2,47,c('Set','Sphere surface of radius1 centered at(x₀,y₀,z₀)','Solid unit ball centered at origin','Plane through r₀'),why='The norm is Euclidean distance to the given center.')
row(2,48,c('Set','Ellipse with foci r₁,r₂ and major-axis length k; a circle if the foci coincide','Hyperbola with transverse-axis length k','Line segment between the foci'),why='The sum of the focal distances is fixed and exceeds the interfocus distance.')
row(2,49,c('Property2 identity','(u+v)+w=u+(v+w)','u+v=u−v','u+v=u·v'),c('Component proof','Both sides have components(u₁+v₁+w₁,u₂+v₂+w₂)','The components multiply','Only lengths need to match'),why='Apply associativity of real addition independently in each coordinate.',limited=True)
row(2,50,c('Property5 identity','c(u+v)=cu+cv','c(u+v)=cu+v','c(u+v)=u+cv'),c('Algebra/geometric reason','Distribute c in every coordinate; similar triangles scale lengths by|c|, with direction reversal if c<0','Only positive c is allowed','Vector direction never changes under a negative scalar'),why='Real distributivity proves the component identity; dilation or reflection of the vector triangle proves the geometry.',limited=True)
row(2,51,c('Midpoint joining vector','(C−B)/2 for midpoints of AB and AC','C−B','(B−C)/3'),c('Conclusion','Parallel to BC and half its length','Perpendicular to BC','Same length as BC'),why='Subtract(A+B)/2 from(A+C)/2; A cancels.',limited=True)
row(2,52,c('After xz reflection','(a₁,−a₂,a₃)','(−a₁,a₂,a₃)','(a₁,a₂,−a₃)'),c('After all three mirrors','−a=(−a₁,−a₂,−a₃), antiparallel to initial ray','a unchanged','Zero vector'),why='Each mirror reverses its normal component and preserves tangential components. Three perpendicular mirrors reverse all three components.',limited=True)
finish('section02')
