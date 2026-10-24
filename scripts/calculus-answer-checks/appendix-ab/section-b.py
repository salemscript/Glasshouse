from common import *
def pt(label,p):return [n(label+' · x',p[0]),n(label+' · y',p[1])]
def dist(p,q):return s.sqrt(sum((s.sympify(a)-b)**2 for a,b in zip(p,q)))
def slope(p,q):return s.Rational(q[1]-p[1],q[0]-p[0])
def line(p,q):
 if p[0]==q[0]:return c('Line equation','x='+fmt(p[0]),'x='+fmt(p[0]+1),'y='+fmt(p[0]))
 return expr('y as a function of x',s.expand(slope(p,q)*(x-p[0])+p[1]))
for k,p,q in [(1,(1,1),(4,5)),(2,(1,-3),(5,7)),(3,(6,-2),(-1,3)),(4,(1,-6),(-1,-3)),(5,(2,5),(4,-7))]:
 d=dist(p,q);put('B',k,n('Distance',d),why='Apply the Euclidean distance formula √((x₂−x₁)²+(y₂−y₁)²); take the nonnegative square root.')
 check(f'B{k} squared distance',s.simplify(d*d-s.Matrix(q).__sub__(s.Matrix(p)).dot(s.Matrix(q)-s.Matrix(p)))==0)
put('B',6,c('Distance between (a,b) and (b,a)','√2 |a−b|','√2(a−b) for all real a,b','2|a+b|'),why='The squared distance is (b−a)²+(a−b)²=2(a−b)². The square root of a square is an absolute value.')
for k,p,q in [(7,(1,5),(4,11)),(8,(-1,6),(4,-3)),(9,(-3,3),(-1,-6)),(10,(-1,-4),(6,0))]:
 m=slope(p,q);put('B',k,n('Slope',m),why='Slope equals vertical change divided by horizontal change, (y₂−y₁)/(x₂−x₁), using the same point order in both differences.')
 check(f'B{k} rise/run',m*(q[0]-p[0])==q[1]-p[1])
put('B',11,n('AB²',18),n('AC²',17),n('BC²',17),c('Equal sides','AC=BC','AB=AC','AB=BC'),why='Distance squared gives18,17,17, so the two sides from C have the same length and the triangle is isosceles.',limited=True)
put('B',12,n('Part (a) · AB²',41),n('Part (a) · AC²',41),n('Part (a) · BC²',82),c('Part (a) · Right-angle vertex','A','B','C'),n('Part (b) · Slope AB',R(4,5)),n('Part (b) · Slope AC',-R(5,4)),n('Part (c) · Area',R(41,2),'square units'),why='AB²+AC²=41+41=82=BC², so A is the right vertex. Slopes4/5 and−5/4 multiply to−1. The perpendicular legs both have length√41, giving area41/2.',limited=True)
put('B',13,n('Common side length',s.sqrt(45)),n('Common diagonal length',s.sqrt(90)),c('Adjacent-side slope product','−1','1','0'),why='In the supplied cyclic order all four squared side lengths are45. The adjacent slopes−1/2 and2 multiply to−1; both diagonals have squared length90. Thus equal sides meet at right angles.',limited=True)
put('B',14,n('Part (a) · AB',4*s.sqrt(5)),n('Part (a) · BC',2*s.sqrt(5)),n('Part (a) · AC',6*s.sqrt(5)),n('Part (b) · Slope AB',2),n('Part (b) · Slope BC',2),why='AB=√80=4√5, BC=√20=2√5 and AC=√180=6√5, so AB+BC=AC. The equal slopes2 give the same straight line.',limited=True)
put('B',15,n('Slope AB = slope CD',R(1,2)),n('Slope BC = slope DA',-3),why='Compute slopes in the cyclic vertex order: opposite sides have equal slopes1/2 and−3, so each opposite pair is parallel.',limited=True)
put('B',16,n('Slope AB = slope CD',R(1,5)),n('Slope BC = slope DA',-5),n('Adjacent-side slope product',-1),why='Both pairs of opposite sides are parallel, and adjacent slopes1/5 and−5 multiply to−1, so the parallelogram has right angles.',limited=True)
graphs={17:('Vertical line x=3','Horizontal line y=3','Vertical line x=−3'),18:('Horizontal line y=−2','Vertical line x=−2','Horizontal line y=2'),19:('Both coordinate axes: x=0 or y=0','Only the origin','The diagonal y=x'),20:('Two horizontal lines y=−1 and y=1','Two vertical lines x=−1 and x=1','A unit circle')}
for k,v in graphs.items():put('B',k,c('Graph description',*v),why='Translate the equation into the exact set of coordinate pairs that satisfy it. Products vanish if either factor vanishes; an absolute value of1 permits either sign.',limited=True)
lines={21:6*x-15,22:-3*x+1,23:R(2,3)*x+R(19,3),24:-R(7,2)*x-R(31,2),25:-5*x+11,26:x-1,27:3*x-2,28:R(2,5)*x+4,29:3*x-3,30:R(3,4)*x+6,31:s.Integer(5),33:-x/2-R(11,2),34:-R(2,3)*x+6,35:R(5,2)*x+R(1,2),36:-2*x+R(1,3)}
for k,e in lines.items():put('B',k,expr('Line equation · y=',e),why='Use y−y₀=m(x−x₀). Obtain m from two points or the stated slope; parallel lines retain m, and perpendicular nonvertical lines use the negative reciprocal. Simplify to slope-intercept form.')
put('B',32,c('Line equation','x=4','y=5','x=5'),why='A line parallel to the y-axis is vertical; every point on it has the x-coordinate4 of the supplied point.')
points={21:[(2,-3)],22:[(-1,4)],23:[(1,7)],24:[(-3,-5)],25:[(2,1),(1,6)],26:[(-1,-2),(4,3)],27:[(0,-2)],28:[(0,4)],29:[(1,0),(0,-3)],30:[(-8,0),(0,6)],31:[(4,5)],33:[(1,-6)],34:[(0,6)],35:[(-1,-2)],36:[(R(1,2),-R(2,3))]}
for k,pp in points.items():
 for a,b in pp:check(f'B{k} passes ({a},{b})',s.simplify(lines[k].subs(x,a)-b)==0)
for k,m in {21:6,22:-3,23:R(2,3),24:-R(7,2),27:3,28:R(2,5),31:0,33:-R(1,2),34:-R(2,3),35:R(5,2),36:-2}.items():check(f'B{k} slope',s.diff(lines[k],x)==m)
for k,m,b in [(37,-R(1,3),0),(38,R(2,5),0),(39,0,-2),(40,R(2,3),2),(41,R(3,4),-3),(42,-R(4,5),2)]:put('B',k,n('Slope',m),n('y-intercept',b),why='Isolate y to obtain y=mx+b; the coefficient of x is the slope and the constant is the y-axis intercept. A horizontal line has slope0.',limited=True)
regions={43:('Left half-plane x<0; exclude the y-axis','Right half-plane x>0','Left half-plane including the y-axis'),44:('Upper half-plane y>0; exclude the x-axis','Lower half-plane y<0','Upper half-plane including the x-axis'),45:('Quadrants II and IV, excluding both axes','Quadrants I and III, excluding both axes','All four quadrants including the axes'),46:('Right of and including x=1, below but excluding y=3','Left of x=1 and above y=3','Right of x=1 and below y=3, excluding both boundaries'),47:('Closed vertical strip −2≤x≤2, all y','Open vertical strip −2<x<2, all y','Horizontal strip −2≤y≤2'),48:('Open rectangle −3<x<3 and −2<y<2; no edges','Closed rectangle −3≤x≤3 and −2≤y≤2','Open rectangle −2<x<2 and −3<y<3'),49:('0≤y≤4 and x≤2, with all finite boundaries included','0<y<4 and x<2, with boundaries excluded','0≤x≤4 and y≤2'),50:('Above y=2x−1, with the boundary line excluded','Below y=2x−1, boundary excluded','Above y=2x−1, boundary included'),51:('For x≤0: between y=1+x and y=1−2x, including both rays and vertex (0,1)','For x≥0: between the same lines','For x≤0: between the lines with both boundaries excluded'),52:('For x>−1: above or on y=−x and strictly below y=(x+3)/2; vertex excluded','For x<−1: between the two lines','For x≥−1: both boundary rays and vertex included')}
for k,v in regions.items():put('B',k,c('Region and boundary description',*v),why='Apply every inequality simultaneously. A strict sign excludes its boundary; a non-strict sign includes it. For a region between two lines, first require the lower bound to be less than (or equal to) the upper bound as allowed.',limited=True)
put('B',53,*pt('Equidistant point on the y-axis',(0,-4)),why='Write the point as(0,t). Equate squared distances25+(t+5)²=1+(t−1)²; cancellation gives12t=−48, hence t=−4.')
put('B',54,c('Midpoint coordinates','((x₁+x₂)/2, (y₁+y₂)/2)','(x₁+x₂, y₁+y₂)','((x₁−x₂)/2, (y₁−y₂)/2)'),c('Vector relationship','M−P₁=(P₂−P₁)/2 and P₂−M=(P₂−P₁)/2','M−P₁=P₂−P₁','M lies beyond P₂ whenever P₁≠P₂'),why='The average-coordinate point equals P₁+(P₂−P₁)/2, so it lies on the segment and splits its displacement into two identical halves.',limited=True)
put('B',55,*pt('Part (a) · Midpoint',(4,9)),*pt('Part (b) · Midpoint',(R(7,2),-3)),why='Average the two x-coordinates and separately average the two y-coordinates.')
put('B',56,n('Median from A',s.sqrt(145)/2),n('Median from B',s.sqrt(109)/2),n('Median from C',s.sqrt(37)),why='The opposite-side midpoints are(11/2,4),(9/2,1),(2,3). Measure from A,B,C respectively using the distance formula.')
put('B',57,n('Slope of 2x−y=4',2),n('Slope of 6x−2y=10',3),*pt('Intersection',(1,-2)),why='Solve each equation for y to get slopes2 and3, which are unequal. Equating2x−4=3x−5 yields x=1,y=−2.',limited=True)
put('B',58,n('Slope of first line',R(3,5)),n('Slope of second line',-R(5,3)),n('Slope product',-1),*pt('Intersection',(2,5)),why='Slopes3/5 and−5/3 have product−1. Solving3x−5y=−19 and10x+6y=50 gives(2,5).',limited=True)
put('B',59,expr('Perpendicular bisector · y=',x-3),why='The midpoint of(1,4),(7,−2) is(4,1); segment slope−1 gives perpendicular slope1. Thus y−1=x−4.')
put('B',60,expr('Part (a) · Side PQ · y=',2*x-2),expr('Part (a) · Side QR · y=',-x/2+R(11,2)),expr('Part (a) · Side RP · y=',-3*x+3),c('Part (b) · Median from P','x=1','y=1','x=0'),expr('Part (b) · Median from Q · y=',x/3+3),expr('Part (b) · Median from R · y=',-4*x/3+R(14,3)),*pt('Part (b) · Intersection',(1,R(10,3))),why='Use pairs of vertices for the sides. For medians, connect each vertex to the midpoint of its opposite side. The three median equations meet at the coordinate average(1,10/3).')
put('B',61,c('Part (a) · Slope through (a,0) and (0,b)','−b/a','b/a','−a/b'),c('Part (a) · Equivalent intercept form','x/a+y/b=1','x/a−y/b=1','ax+by=1'),c('Part (b) · Required line','x/6−y/8=1','x/6+y/8=1','x/8−y/6=1'),why='For nonzero a,b, y=(−b/a)x+b; divide by b and rearrange. Substitute a=6,b=−8 to obtain x/6−y/8=1.',limited=True)
put('B',62,c('Part (a) · Distance d, t hours after 2:00 pm','d(t)=48t miles, t≥0','d(t)=40t miles','d(t)=50t miles'),c('Part (b) · Graph','Ray from (0,0) through (5/6,40), with t≥0','Ray from (0,40) through (5/6,0)','Horizontal line d=40'),n('Part (c) · Slope',48,'mi/h'),c('Part (c) · Meaning','Constant westward speed','Starting distance from Detroit','Acceleration in mi/h²'),why='50minutes=5/6hour, so speed=40/(5/6)=48mi/h. Distance since departure is speed times elapsed time. Its graph is a ray with positive slope48.',limited=True)
# Independent vector/determinant geometry checks.
for k,P in [(11,[(0,2),(-3,-1),(-4,3)]),(12,[(6,-7),(11,-3),(2,-2)]),(13,[(-2,9),(4,6),(1,0),(-5,3)]),(14,[(-1,3),(3,11),(5,15)]),(15,[(1,1),(7,4),(5,10),(-1,7)]),(16,[(1,1),(11,3),(10,8),(0,6)])]:
 V=[s.Matrix(p) for p in P]
 if k==11:check('B11 isosceles',dist(P[0],P[2])==dist(P[1],P[2])==s.sqrt(17))
 if k==12:
  check('B12 dot zero',(V[1]-V[0]).dot(V[2]-V[0])==0);check('B12 determinant area',abs(s.det(s.Matrix.hstack(V[1]-V[0],V[2]-V[0])))/2==R(41,2))
 if k==13:
  check('B13 all sides',all(dist(P[i],P[(i+1)%4])**2==45 for i in range(4)));check('B13 orthogonal',(V[1]-V[0]).dot(V[2]-V[1])==0)
 if k==14:check('B14 determinant',s.det(s.Matrix.hstack(V[1]-V[0],V[2]-V[0]))==0)
 if k in [15,16]:check(f'B{k} diagonal midpoint',V[0]+V[2]==V[1]+V[3])
 if k==16:check('B16 orthogonal',(V[1]-V[0]).dot(V[2]-V[1])==0)
check('B53 squared distances',dist((0,-4),(5,-5))**2==dist((0,-4),(1,1))**2)
for P,Q,e in [((1,4),(7,-2),x-3),((1,0),(3,4),2*x-2),((3,4),(-1,6),-x/2+R(11,2)),((-1,6),(1,0),-3*x+3)]:
 if P==(1,4):check('B59 midpoint',e.subs(x,4)==1);check('B59 perpendicular',s.diff(e,x)*slope(P,Q)==-1)
 else:
  for a,b in [P,Q]:check('B60 side point',s.simplify(e.subs(x,a)-b)==0)
for a,b,e in [(3,4,x/3+3),(0,3,x/3+3),(-1,6,-4*x/3+R(14,3)),(2,2,-4*x/3+R(14,3))]:check('B60 median endpoint',e.subs(x,a)==b)
for e in [x/3+3,-4*x/3+R(14,3)]:check('B60 centroid',e.subs(x,1)==R(10,3))
for P,Q,Rr,ans in [((1,0),(3,6),(8,2),s.sqrt(145)/2),((3,6),(1,0),(8,2),s.sqrt(109)/2),((8,2),(1,0),(3,6),s.sqrt(37))]:
 mid=[s.Rational(a+b,2) for a,b in zip(Q,Rr)];check('B56 median',dist(P,mid)==ans)
check('B62 speed',48*R(5,6)==40)
save('section-b')
