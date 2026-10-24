from common import *
R=s.Rational;t,u=s.symbols('t u',real=True);x,y,z=s.symbols('x y z',real=True)
def tup(a):return '('+', '.join(fmt(v) for v in a)+')'
def linefields(p,d,sym=False,segment=False):
 p,d=V(*p),V(*d);param='; '.join(l+'='+fmt(e) for l,e in zip('xyz',p+t*d));fields=[c('Parametric equations',param,'; '.join(l+'='+fmt(e) for l,e in zip('xyz',p+t*d+V(1,1,1))),'x=t; y=t; z=t')]
 if sym:
  ratios=[];fixed=[]
  for l,a,b in zip('xyz',p,d):
   if b:ratios.append(f'({l}−({fmt(a)}))/({fmt(b)})')
   else:fixed.append(l+'='+fmt(a))
  text=' = '.join(ratios)+('; '+', '.join(fixed) if fixed else '')
  fields.append(c('Symmetric equations',text,'x=y=z','x=0; y=0; z=0'))
 else:fields.append(c('Vector equation','r='+tup(p)+'+t'+tup(d),'r='+tup(d)+'+t'+tup(p+V(1,1,1)),'r=t(1,1,1)'))
 if segment:fields.append(c('Parameter interval','0≤t≤1','t∈R','t≥1'))
 return fields

def plane(k,p,normal,why='Use n·(r−p)=0; the normal fixes orientation and p fixes its offset.'):
 p,normal=V(*p),V(*normal);lhs=s.expand(normal.dot(V(x,y,z)));rhs=normal.dot(p)
 row(5,k,c('Plane equation',fmt(lhs)+' = '+fmt(rhs),fmt(lhs)+' = '+fmt(rhs+1),fmt(lhs)+' = '+fmt(rhs-1)),why=why)
 check(str(k)+' source point',lhs.subs(dict(zip((x,y,z),p)))-rhs)
 AUDIT[f'calculus-section-12-5-{k}'].update(normal=list(map(str,normal)),point=list(map(str,p)),equation=str(lhs-rhs))

row(5,1,*[c('('+l+')',a,'False' if a=='True' else 'True') for l,a in zip('abcdefghijk',['True','False','True','False','False','True','False','True','True','False','True'])],why='Use common direction vectors or normals for the true parallelism statements. In three dimensions distinct lines may be skew. Intersect means share at least one point, including containment/coincidence where relevant.')
for k,p,d in [(2,(6,-5,2),(1,3,R(-2,3))),(3,(2,R(12,5),R(7,2)),(3,2,-1)),(4,(0,14,-10),(2,-3,9)),(5,(1,0,6),(1,3,1)),(6,(0,0,0),(4,3,-1)),(7,(0,R(1,2),1),(2,R(1,2),-4)),(8,(1,R(12,5),R(23,5)),(R(8,5),R(-6,5),R(-43,10))),(9,(-8,1,4),(11,-3,0)),(10,(2,1,0),(1,-1,1)),(11,(-6,2,3),(2,3,1)),(12,(1,0,0),(5,2,-3))]:
 row(5,k,*linefields(p,d,k>=6),why='A line through p with nonzero direction d is r=p+td. Subtract endpoints, reuse a parallel direction, use a plane normal for a perpendicular line, or cross normals for a plane intersection as appropriate.')
row(5,13,c('Parallel?','Yes','No'),c('Direction relationship','(−5,−15,10)=−(5/2)(2,6,−4)','The dot product is0','The directions are equal'),why='The endpoint differences are nonzero scalar multiples.')
row(5,14,c('Perpendicular?','No','Yes'),n('Dot product of given endpoint differences',6),why='Directions(3,−3,1) and(1,−4,−12) have dot product3+12−12=3, not zero.')
# Correct arithmetic: the actual dot product is3.
OUT['calculus-section-12-5-14']['grader']['parts'][1]['answer']=3
for k,p,d in [(15,V(1,-5,6),V(-1,2,-3)),(16,V(2,4,6),V(1,-1,3))]:
 fields=linefields(p,d,k==15)
 for i,name in [(2,'xy'),(0,'yz'),(1,'xz')]:fields+=vec('(b) '+name+' intersection',p-p[i]/d[i]*d)
 row(5,k,*fields,why='Set the perpendicular coordinate equal to0 in r=p+td to find each coordinate-plane intersection.')
for k,p,q in [(17,(6,-1,9),(7,6,0)),(18,(-2,18,31),(11,-4,48))]:row(5,k,*linefields(p,V(*q)-V(*p),segment=True),why='Interpolate r=p+t(q−p) over0≤t≤1 to trace exactly the segment.')
for k,p,a,q,b in [(19,(3,4,1),(2,-1,3),(1,3,4),(4,-2,5)),(20,(5,3,1),(-12,9,-3),(3,0,7),(8,-6,2)),(21,(2,3,1),(1,-2,-3),(3,-4,2),(1,3,-7)),(22,(0,1,2),(1,-1,3),(2,3,0),(2,-2,7))]:
 p,a,q,b=map(lambda v:V(*v),(p,a,q,b));sol=s.solve(list(p+t*a-q-u*b),(t,u));parallel=a.cross(b)==s.zeros(3,1);ans='Parallel' if parallel else 'Intersecting' if sol else 'Skew';fields=[c('Relationship',ans,*[v for v in ['Parallel','Intersecting','Skew'] if v!=ans])]
 if sol:fields+=vec('Intersection',p+sol[t]*a)
 row(5,k,*fields,why='Compare direction vectors, then solve all three coordinate equations with independent parameters; two equations alone do not establish an intersection.')
for k,p,normal in [(23,(0,0,0),(1,-2,5)),(24,(5,3,5),(2,1,-1)),(25,(-1,R(1,2),3),(1,4,1)),(26,(2,0,1),(3,-1,4)),(27,(1,-1,-1),(5,-1,-1)),(28,(3,-2,8),(1,1,-1)),(29,(1,R(1,2),R(1,3)),(1,1,1)),(30,(1,2,4),(5,2,1))]:plane(k,p,normal)
for k,P,Q,T in [(31,(0,1,1),(1,0,1),(1,1,0)),(32,(0,0,0),(3,-2,1),(1,1,1)),(33,(2,1,2),(3,-8,6),(-2,-3,1)),(34,(3,0,-1),(-2,-2,3),(7,1,-4))]:
 P,Q,T=V(*P),V(*Q),V(*T);nn=(Q-P).cross(T-P);plane(k,P,nn,'Cross two nonparallel side displacements to get a normal, then substitute one source point.');check(str(k)+' second point',nn.dot(Q-P));check(str(k)+' third point',nn.dot(T-P))
for k,p,l,d in [(35,(3,5,-1),(4,-1,0),(-1,2,-3)),(36,(6,-1,3),(0,-4,0),(3,1,2))]:
 p,l,d=V(*p),V(*l),V(*d);nn=(p-l).cross(d);plane(k,p,nn,'Cross the supplied line direction with the displacement to the extra point; both directions lie in the desired plane.');check(str(k)+' line',nn.dot(d))
plane(37,(3,1,4),(-4,7,3),'Use the plane pencil2(x+2y+3z−1)−3(2x−y+z+3)=0; every intersection point satisfies it, and(3,1,4) fixes the combination.')
plane(38,(0,-2,5),V(-1,5,-4).cross(V(5,4,-2)),'The desired normal is perpendicular both to the point-to-point direction and to the given plane normal.')
plane(39,(1,5,1),V(2,1,-2).cross(V(1,0,3)),'A plane perpendicular to both given planes has a normal perpendicular to both of their normals.')
plane(40,(1,3,0),(1,1,1),'Add(x−z−1)+(y+2z−3)=0. Its normal(1,1,1) is perpendicular to(1,1,−2).')
for k,normal,rhs in [(41,(2,5,1),10),(42,(3,1,2),6),(43,(6,-3,4),6),(44,(6,5,-3),15)]:row(5,k,*[n(axis+' intercept',R(rhs,v)) for axis,v in zip('xyz',normal)],why='Set the other two coordinates to0 for each intercept; join the three intercept points and extend the plane.',limited=True)
for k,p,d,normal,rhs in [(45,(2,0,1),(-2,3,1),(1,2,-1),7),(46,(-1,1,3),(1,2,-1),(3,-1,2),5),(47,(0,0,-2),(R(1,5),2,1),(10,-7,3),-24),(48,(-3,1,0),(2,4,6),(2,1,-1),-2)]:
 p,d,normal=V(*p),V(*d),V(*normal);tv=(rhs-normal.dot(p))/normal.dot(d);v=p+tv*d;row(5,k,*vec('Intersection',v),why='Substitute the line coordinates into the plane, solve its linear parameter equation, and substitute back.');check(str(k)+' plane',normal.dot(v)-rhs)
row(5,49,c('Direction numbers','(1,0,−1)','(1,1,1)','(1,0,1)'),why='Cross the two normals(1,1,1) and(1,0,1); any nonzero scalar multiple is equivalent.')
row(5,50,n('Cosine',s.sqrt(R(6,7))),why='The normal dot product is6 and the product of normal lengths is√42.')
for k,a,b in [(51,(1,4,-3),(-3,6,7)),(52,(9,-3,6),(6,-2,4)),(53,(1,2,-1),(2,-2,1)),(54,(1,-1,3),(3,1,-1)),(55,(2,-3,-1),(4,-6,-2)),(56,(5,2,3),(4,-1,-6))]:
 a,b=V(*a),V(*b);ans='Parallel' if a.cross(b)==s.zeros(3,1) else 'Perpendicular' if a.dot(b)==0 else 'Neither';fields=[c('Relationship',ans,*[v for v in ['Parallel','Perpendicular','Neither'] if v!=ans])]
 if ans=='Neither':fields.append(n('Acute angle',float(s.acos(abs(a.dot(b))/(a.norm()*b.norm())))*180/math.pi,'degrees',.051))
 row(5,k,*fields,why='Compare normals: proportional means parallel; zero dot product means perpendicular; otherwise use arccos of the absolute normalized dot product.')
for k,a,r1,b,r2 in [(57,(1,1,1),1,(1,2,2),1),(58,(3,-2,1),1,(2,1,-3),3),(59,(5,-2,-2),1,(4,1,1),6),(60,(2,-1,-1),5,(4,3,-1),5)]:
 a,b=V(*a),V(*b);d=a.cross(b);sol=s.linsolve([a.dot(V(x,y,z))-r1,b.dot(V(x,y,z))-r2],(x,y,z));p=V(*next(iter(sol)));free=set().union(*(v.free_symbols for v in p));p=p.subs({v:0 for v in free});fields=linefields(p,d,k>=59)
 if k<59:fields.append(n('(b) Acute angle',float(s.acos(abs(a.dot(b))/(a.norm()*b.norm())))*180/math.pi,'degrees',.005))
 row(5,k,*fields,why='Cross plane normals for direction, solve the two plane equations for one point, and use r=p+td. The acute plane angle is the acute normal angle.');check(str(k)+' first plane',a.dot(p)-r1);check(str(k)+' second plane',b.dot(p)-r2);check(str(k)+' tangent1',a.dot(d));check(str(k)+' tangent2',b.dot(d))
for k,a,b in [(61,(1,0,-2),(3,4,0)),(62,(2,5,5),(-6,3,1))]:
 a,b=V(*a),V(*b);plane(k,(a+b)/2,b-a,'The perpendicular-bisector plane has normal B−A and passes through the midpoint(A+B)/2.')
row(5,63,c('Intercept form','x/a+y/b+z/c=1, for nonzero finite a,b,c','ax+by+cz=1','x/a+y/b+z/c=0'),why='Substitution of(a,0,0),(0,b,0),(0,0,c) determines the coefficients up to scale.')
row(5,64,*vec('(a) Intersection',(2,0,2)),c('(b) Plane','x+y=2','x−y=2','x+y+z=2'),why='The first line reaches(2,0,2) att=1 and the second ats=0. Cross directions(1,−1,2) and(−1,1,0) to get a normal parallel to(1,1,0).')
row(5,65,*linefields((0,1,2),(3,-1,-2)),why='The direction must be perpendicular to plane normal(1,1,1) and given line direction(1,−1,2); their cross product is(3,−1,−2).')
p=V(0,1,2);a=V(1,1,0);d=V(1,-1,2);foot=a+d*(p-a).dot(d)/d.dot(d)
row(5,66,*linefields(p,foot-p),*vec('Meeting point',foot),why='Project p−a onto the given line direction to find the foot. The joining line then both intersects and is perpendicular to the given line.');check('66 orthogonality',(foot-p).dot(d))
row(5,67,c('Parallel groups','P₁∥P₄ and P₂∥P₃','All four are parallel','Only P₁∥P₂'),c('Identical planes','P₁=P₄ only','P₂=P₃ only','None'),why='Normalize each equation including its constant. P₁ and P₄ reduce to x+2y−z=2; P₂,P₃ share normals but have different offsets.')
row(5,68,c('Parallel groups','L₁∥L₃ and L₂∥L₄','All four are parallel','L₁∥L₂ only'),c('Identical lines','L₂=L₄ only','L₁=L₃ only','None'),why='L₃ has direction(2,−1,4), parallel to L₁. L₂ reaches(3,1,5) at parameter1, the stated point of L₄; their directions are proportional.')
for k,p,a,d in [(69,(4,1,-2),(1,3,4),(1,-2,-3)),(70,(0,1,3),(0,6,3),(2,-2,1))]:
 p,a,d=V(*p),V(*a),V(*d);row(5,k,n('Distance',d.cross(p-a).norm()/d.norm()),why='Divide the area of the direction/displacement parallelogram by the direction length.')
for k,p,normal,rhs in [(71,(1,-2,4),(3,2,6),5),(72,(-6,3,5),(1,-2,-4),8)]:row(5,k,n('Distance',abs(V(*normal).dot(V(*p))-rhs)/V(*normal).norm()),why='Absolute plane residual divided by normal magnitude is the perpendicular distance.')
row(5,73,n('Distance',R(5,2)/s.sqrt(14)),why='Normalize the second equation to2x−3y+z=3/2; offset difference is5/2.')
row(5,74,n('Distance',1/(3*s.sqrt(14))),why='Normalize to x−2y+3z=0 and x−2y+3z=1/3.')
row(5,75,c('Distance','|d₁−d₂|/√(a²+b²+c²)','|d₁+d₂|/√(a²+b²+c²)','|d₁−d₂|'),why='Evaluate the second plane residual at a point on the first; the shared linear part equals−d₁. Divide by the common normal magnitude.',limited=True)
row(5,76,c('Both planes','x+2y−2z=7 and x+2y−2z=−5','x+2y−2z=3 and x+2y−2z=−1','x+2y−2z=±2'),why='The normal length is3, so a distance2 requires offset change±6 from1.')
for k,p,a,q,b in [(77,(0,0,0),(1,1,1),(-1,0,0),(1,2,3)),(78,(1,1,0),(1,6,2),(1,5,-2),(2,15,6)),(79,(0,0,0),(2,0,-1),(1,-1,1),(3,2,2))]:
 p,a,q,b=map(lambda v:V(*v),(p,a,q,b));normal=a.cross(b);fields=[n('Distance',abs((q-p).dot(normal))/normal.norm())]
 if k==77:fields.append(c('Relationship','Skew: nonparallel and no common point','Parallel','Intersecting'))
 row(5,k,*fields,why='Project the displacement between line origins onto the unit common normal a×b. A positive distance and nonparallel directions establish skew lines.',limited=k==77)
# P₂ through the three source points; then intersect with P₁.
na=V(1,-1,2);A,B,C=V(3,2,-1),V(0,0,1),V(1,2,1);nb=(B-A).cross(C-A);dir2=na.cross(nb);sol=next(iter(s.linsolve([na.dot(V(x,y,z))+1,nb.dot(V(x,y,z)-A)],(x,y,z))));p2=V(*sol).subs(z,0);p1=V(1,2,6);dir1=V(1,2,2);normal=dir1.cross(dir2)
row(5,80,n('Distance',abs((p2-p1).dot(normal))/normal.norm()),why='Find the second plane normal from its three points, cross it with the first plane normal for L₂ direction, then project a connecting displacement onto the common normal.')
row(5,81,*linefields((325,810,561),(440,-135,38),segment=True),*[n('(b) Sight-line elevation at fraction '+str(i)+'/5',561+38*i/5) for i in range(1,5)],c('(b) Can they see each other?','No','Yes'),why='At fraction3/5 the line elevation is583.8, below terrain586; the line of sight is obstructed even though the other sampled points are clear.')
row(5,82,c('(a)','Parallel planes with common normal(1,1,1), moving through space as c changes','Planes all passing through the origin','Spheres of radius c'),c('(b)','Planes through the fixed line x+y=1,z=0; the family omits the plane z=0','Parallel planes','Planes all perpendicular to z-axis'),c('(c)','Planes parallel to x-axis and tangent to the cylinder y²+z²=1','Planes through x-axis','Concentric spheres'),why='Read the fixed normals or common intersection, and note that(c) has unit normal(0,cosθ,sinθ) and offset1.')
row(5,83,c('Normal','(a,b,c), nonzero','(x,y,z)','(d,d,d)'),c('Point-normal representation for a≠0','(a,b,c)·[(x,y,z)−(−d/a,0,0)]=0','(a,b,c)·(x,y,z)=d always','Every point satisfies it'),why='Choose a nonzero coefficient to obtain a specific point on the set; the remaining displacements are perpendicular to the nonzero normal.',limited=True)
# Perspective project: linear clipping and projective occlusion computed exactly.
suffix='-project-laboratory-project-putting-3d-in-perspective-1'
P=V(230,-285,102);D=V(630,390,162);cam=V(1000,0,0);L=P+t*D
bounds=[L[1]+R(2,5)*(1000-L[0]),R(2,5)*(1000-L[0])-L[1],L[2],R(3,5)*(1000-L[0])-L[2]]
lo=max(s.solve(v,t)[0] for v in bounds if s.diff(v,t)>0);hi=min(s.solve(v,t)[0] for v in bounds if s.diff(v,t)<0);A=L.subs(t,lo);B=L.subs(t,hi)
put(5,1,[*vec('First clipped endpoint',A),*vec('Second clipped endpoint',B)],'The viewing cone requires−0.4(1000−x)≤y≤0.4(1000−x) and0≤z≤0.6(1000−x). Substitute the line and intersect the four parameter inequalities.',suffix=suffix)
def project(p):return V(0,1000*p[1]/(1000-p[0]),1000*p[2]/(1000-p[0]))
A2,B2=project(A),project(B)
put(5,2,[*vec('First screen endpoint',A2),*vec('Second screen endpoint',B2)],'Intersect each camera-to-endpoint ray with x=0: screen coordinates are(0,1000y/(1000−x),1000z/(1000−x)).',suffix=suffix)
put(5,3,[c('Window edges','x=0, y=±400,0≤z≤600; x=0,z=0 or600,−400≤y≤400','x=1000 with the same y,z bounds','A unit circle'),c('Clipped segment','r='+tup(A)+'+s'+tup(B-A)+', 0≤s≤1','r=(0,0,0)+s(1,1,1)','All of the infinite line L'),c('Screen segment','r='+tup(A2)+'+s'+tup(B2-A2)+',0≤s≤1','The entire yz-plane','A curved arc'),c('Sight lines','camera+s(endpoint−camera),0≤s≤1','camera+s·endpoint','All lines parallel to x-axis')],'Plot the exact clipped endpoints and their perspective images; each camera ray contains both an endpoint and its screen projection.',limited=True,suffix=suffix)
# A point is occluded when the camera ray meets the rectangle before reaching L(t).
R0=V(621,-147,206);E1=V(563,31,242)-R0;E2=V(657,-111,86)-R0;aa,bb,lam=s.symbols('aa bb lam');sol=s.solve(list(cam+lam*(L-cam)-R0-aa*E1-bb*E2),(aa,bb,lam));occlusion={k:s.factor(v) for k,v in sol.items()}
# Boundaries where ray hits one rectangle edge; intersect with clipped t and lambda<1.
candidates=sorted(set([lo,hi]+[r for e in (sol[aa],sol[aa]-1,sol[bb],sol[bb]-1,sol[lam]-1) for r in s.solve(e,t) if r.is_real and lo<=r<=hi]))
intervals=[]
for a,b in zip(candidates,candidates[1:]):
 mid=(a+b)/2;av,bv,lv=[v.subs(t,mid) for v in (sol[aa],sol[bb],sol[lam])]
 if 0<=av<=1 and 0<=bv<=1 and 0<lv<1:intervals.append((a,b))
assert len(intervals)==1,intervals
ol,oh=intervals[0]
put(5,4,[c('Hidden parameter interval for L=P+tD',f'{fmt(ol)}≤t<{fmt(oh)}',f'{fmt(oh)}<t≤{fmt(hi)}','The entire clipped segment'),*vec('Hidden segment far endpoint',L.subs(t,ol)),*vec('Surface intersection endpoint',L.subs(t,oh))],'Solve camera+λ(L(t)−camera)=R₀+aE₁+bE₂. The point lies behind the opaque rectangle exactly when0≤a,b≤1 and0<λ<1; equalityλ=1 is the line/surface intersection, not a point strictly behind it.',suffix=suffix)
AUDIT[f'calculus-section-12-5-4{suffix}']['rayParameters']={str(k):str(v) for k,v in occlusion.items()}
finish('section05')
