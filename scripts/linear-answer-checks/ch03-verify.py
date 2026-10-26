import json,sympy as s
from pathlib import Path
Q={}
def tex(v):return '\\('+s.latex(v,mat_delim='',mat_str='bmatrix')+'\\)'
def add(sec,n,fs):Q[f'anton-section-{sec.replace(".","-")}-{n}']={'fields':fs,'scope':'All requested parts','complete':True,'sourceImageReviewed':True}
def num(l,a,st,prompt='Enter the value.'):
 return dict(label=l,selectionPrompt=prompt,type='numeric',answer=float(a),tolerance=1e-7,explanation=' '.join(st),workedSteps=st)
def choice(l,a,wr,st,prompt='Select the complete correct result.'):
 return dict(label=l,selectionPrompt=prompt,type='choice',answer=a,options=[a]+wr,explanation=' '.join(st),workedSteps=st)
def vec(l,v,st):
 v=s.Matrix(v);return choice(l,tex(v),[tex(v+s.ones(*v.shape)),tex(v+2*s.ones(*v.shape))],st+['The resulting vector is '+tex(v)+'.'])
def exact(l,v,st):return choice(l,tex(v),[tex(v+1),tex(v+2)],st+['The exact value is '+tex(v)+'.'])
def yes(l,ok,st):return choice(l,'Yes' if ok else 'No',['No' if ok else 'Yes'],st)
def save():Path('scripts/linear-answer-checks/ch03-reviewed.json').write_text(json.dumps({'chapter':3,'questions':Q},indent=2))
V=s.Matrix
add('3.1',1,[vec('a',[3,-4],['Subtract initial point (1,5) from terminal point (4,1).']),vec('b',[-2,-3,4],['The arrow points from (2,3,0) toward (0,0,4); subtract initial from terminal.'])])
add('3.1',3,[vec('a',[-1,3],['Compute (2,8)-(3,5).']),vec('b',[-3,6,1],['Compute (2,4,2)-(5,-2,1).'])])
add('3.1',5,[vec('a',[2,3],['The terminal point is initial point plus displacement: (1,1)+(1,2).']),vec('b',[-2,-2,-1],['The initial point is terminal point minus displacement: (-1,-1,2)-(1,1,3).'])])
u=V([-3,1,2]);v=V([4,0,-8]);w=V([6,-1,-4]);vals=[v-w,6*u+2*v,-3*(v-8*w),(2*u-7*w)-(8*v+u)]
add('3.1',10,[vec(chr(97+i),a,['Distribute scalar multiplication and combine corresponding coordinates.']) for i,a in enumerate(vals)])
add('3.1',15,[yes('a',False,['The first coordinate would require multiplier -2, but the second coordinate would require multiplier 2.']),yes('b',True,['The given vector equals -2u.']),yes('c',True,['The zero vector equals 0u. The text regards zero as parallel to all vectors when convenient.'])])
add('3.1',17,[num('a',3,['The third coordinate gives 3a=9, so a=3.']),num('b',-1,['The first coordinate gives a+2b=1; insert a=3 to get b=-1.','The remaining coordinates check: -3-1=-4 and 15+3=18.'])]);assert 3*V([1,-1,3,5])-V([2,1,0,-3])==V([1,-4,9,18])
A=V([[1,3,0],[-1,2,1],[0,1,4]]);b=V([-1,1,19]);sol=A.inv()*b;assert A*sol==b
add('3.1',19,[vec('a',sol,['Equate coordinates to obtain '+tex(A)+' times '+r'\((c_1,c_2,c_3)^T=(-1,1,19)^T\)'+'.','Eliminate the first variable, then solve the last two equations and back-substitute.'])])
p=V([2,3,-2]);q=V([7,-4,1]);add('3.1',23,[vec('a',(p+q)/2,['Average corresponding endpoint coordinates.']),vec('b',p+s.Rational(3,4)*(q-p),[r'Use \(P+\frac{3}{4}(Q-P)\).'])])
add('3.1',25,[vec('a',[-2,5],['The arrows form a head-to-tail chain from (0,0) to (-2,5).','Equivalently add (5,-5)+(-10,2)+(3,8).']),vec('b',[3,-8],['The arrows form a head-to-tail chain from (-5,4) to (-2,-4).','Subtract the endpoints, or add (10,-7)+(-3,8)+(-4,-9).'])])
add('3.1',28,[yes('a',True,['If u+v+w=0, then w=-u-v lies in the span of u and v.','Their span has dimension at most two, so all three vectors, based at the origin, lie in a common plane.'])])
fs=[]
for l,v in [('a',V([2,2,2])),('b',V([1,0,2,1,3]))]:
 norm=s.sqrt(v.dot(v));unit=-v/norm;assert s.simplify(unit.dot(unit))==1
 fs +=[exact(l+' norm',norm,['Sum the squares of the coordinates and take the square root.']),vec(l+' unit',unit,['Divide the negative vector by its norm to obtain unit length and the opposite direction.'])]
add('3.2',1,fs)
u=V([2,-2,3]);v=V([1,-3,4]);w=V([3,6,-4]);vals=[(u+v).norm(),u.norm()+v.norm(),(-2*u+2*v).norm(),(3*u-5*v+w).norm()]
add('3.2',3,[exact(chr(97+i),a,['First perform the indicated vector operations.','For each norm, take the square root of the sum of the coordinate squares.']) for i,a in enumerate(vals)])
fs=[]
for l,u,v in [('a',V([3,1,4]),V([2,2,-4])),('b',V([1,1,4,6]),V([2,-2,3,-2]))]:
 for name,a in [('u dot v',u.dot(v)),('u dot u',u.dot(u)),('v dot v',v.dot(v))]:fs.append(num(l+' '+name,a,['Multiply matching coordinates and sum the products.','The result is '+tex(a)+'.']))
add('3.2',9,fs)
fs=[]
for l,u,v in [('a',V([3,3,3]),V([1,0,4])),('b',V([0,-2,-1,1]),V([-3,2,4,4]))]:
 dot=u.dot(v);cos=s.simplify(dot/(u.norm()*v.norm()));fs +=[exact(l+' distance',(u-v).norm(),['Subtract the vectors and take the norm.']),exact(l+' cosine',cos,['The dot product is '+tex(dot)+'.',r'Divide by \(\|u\|\|v\|\).']),choice(l+' angle','Acute' if dot>0 else 'Obtuse',['Obtuse' if dot>0 else 'Acute','90 degrees'],['The cosine has the same sign as the dot product. A positive cosine means acute; a negative cosine means obtuse.'])]
add('3.2',11,fs)
add('3.2',15,[yes('a',False,['The inner dot product is a scalar; a dot product requires two vectors.']),yes('b',True,['The sum v+w is a vector, so its dot product with u is defined.']),yes('c',False,['The dot product is a scalar; the displayed vector norm is not defined on scalars in this notation. Its absolute value would be meaningful.']),yes('d',True,['Both the dot product and the norm are scalars, so they can be subtracted.'])])
add('3.2',17,[choice('a',r'\(7\le\sqrt{140}\)',[r'\(14\le7\)',r'\(\sqrt{140}\le7\)'],[r'The dot product is -7, and the squared norms are 10 and 14. Thus \(|u\cdot v|=7\le\sqrt{10}\sqrt{14}\).']),choice('b',r'\(5\le6\)',[r'\(6\le5\)',r'\(9\le4\)'],['The dot product is 5. The norms are 3 and 2, whose product is 6; the required inequality holds.'])])
add('3.2',19,[choice('a','Circle centered at r₀, radius 1',['Disk centered at the origin','Exterior of the unit circle'],['The norm of r-r₀ is the distance to r₀; equality fixes distance 1.']),choice('b','Closed disk centered at r₀, radius 1',['Circle only','Exterior excluding boundary'],['Distance at most 1 includes the interior and the boundary.']),choice('c','Exterior of the circle centered at r₀, radius 1, excluding its boundary',['Closed disk centered at r₀','Circle only'],['Distance strictly greater than 1 excludes the circle and its interior.'])])
add('3.2',24,[num('a',35,[r'For side length 1, \(d=(1,1,1)\) and \(u=(1,1,0)\).',r'Then \(\cos\theta=\frac{2}{\sqrt6}\), giving \(\theta\approx35.264^\circ\), or 35 degrees to the nearest degree.']),num('b',90,[r'The face diagonal v goes from \((1,1,0)\) to \((0,1,1)\), so \(v=(-1,0,1)\).',r'Since \((1,1,1)\cdot(-1,0,1)=0\), d and v are perpendicular, confirming 90 degrees.'])])
add('3.2',27,[choice('a','They point in the same direction (one is a positive scalar multiple of the other).',['They point in opposite directions.','They are perpendicular.'],['Square both sides and cancel the squared norms to get '+r'\(u\cdot v=\|u\|\|v\|\)'+'.','Thus the cosine of the angle is 1, so the angle is zero.'])])
add('3.2',29,[choice('a',r'\(\frac{m}{\|v\|}v\) for nonzero v and positive m',[r'\(m\|v\|v\)',r'\(\frac{\|v\|}{m}v\)'],['Divide v by its norm to make a unit vector in the same direction.','Multiply that unit vector by m to obtain the requested length.'])])
fs=[]
for i,(u,v) in enumerate([([6,1,4],[2,0,-3]),([0,0,-1],[1,1,1]),([3,-2,1,3],[-4,1,-3,7]),([5,-4,0,3],[-4,1,-3,7])]):
 d=V(u).dot(V(v));fs.append(yes(chr(97+i),d==0,['Their dot product is '+tex(d)+'.','Orthogonality holds exactly when the dot product is zero.']))
add('3.3',1,fs)
add('3.3',3,[choice('a',r'\(-2(x+1)+(y-3)-(z+2)=0\)',[r'\(-2(x-1)+(y+3)-(z-2)=0\)',r'\(2x+y+z=0\)'],[r'The point-normal equation is \(n\cdot((x,y,z)-P)=0\).','Insert the stated point and normal. Expanding gives -2x+y-z=7.'])])
add('3.3',7,[yes('a',False,['The normals (4,-1,2) and (7,-3,4) are not scalar multiples: their coordinate ratios disagree.'])])
add('3.3',11,[yes('a',False,['The normals are (3,-1,1) and (1,0,2).','Their dot product is 3+2=5, not zero.'])])
add('3.3',15,[vec('a',[0,0],[r'\(u\cdot a=6(3)+2(-9)=0\), so the projection along a is zero.']),vec('b',[6,2],['Subtract the zero projection from u to obtain the orthogonal component.'])])
add('3.3',21,[num('a',1,[r'Use \(d=\frac{|ax_0+by_0+c|}{\sqrt{a^2+b^2}}\).',r'Here \(d=\frac{|4(-3)+3(1)+4|}{5}=1\).'])])
add('3.3',25,[exact('a',s.Rational(5,3),[r'Write the plane as \(x+2y-2z-4=0\).',r'The distance is \(\frac{|3+2+4-4|}{\sqrt{1+4+4}}=\frac{5}{3}\).'])])
n=V([-1,-1,1])/s.sqrt(3);assert n.dot(V([1,0,1]))==0 and n.dot(V([0,1,1]))==0 and n.dot(n)==1
add('3.3',29,[vec('a',n,['Orthogonality gives x+z=0 and y+z=0, so a common perpendicular is (-1,-1,1).','Its norm is the square root of 3; divide by this norm. The negative of the selected vector is also valid.'])])
add('3.3',34,[yes('a',True,['If u=a is nonzero, both projections equal that common vector.','If u and a are nonzero and orthogonal, both projections are zero. These examples show equality is possible.'])])
add('3.3',41,[exact('a',25000*s.sqrt(2),[r'Work is \(F\cdot d=\|F\|\|d\|\cos\theta\).',r'North and northeast make an angle of 45 degrees, so \(W=500(100)\cos45^\circ=25000\sqrt2\) joules.'])])
save()
add('3.4',1,[choice('a',r'\((x,y)=(-4,1)+t(0,-8);\quad x=-4,\ y=1-8t\)',[r'\((x,y)=(0,-8)+t(-4,1)\)',r'\(x=-4+t,\ y=1\)'],['Use the given point as the constant term and the given parallel vector as the coefficient of t.','Equate the two coordinates to obtain the parametric equations; t is any real number.'])])
add('3.4',4,[choice('a',r'\((x,y,z)=(-9,3,4)+t(-1,6,0);\quad x=-9-t,\ y=3+6t,\ z=4\)',[r'\(x=-9+t,\ y=3+6t,\ z=4t\)',r'\(x=-1-9t,\ y=6+3t,\ z=4t\)'],['Use point plus parameter times direction, then equate coordinates.','At t=0 the line passes through the given point and its direction is exactly the given vector.'])])
add('3.4',5,[vec('a',[3,-6],['Set t=0 to obtain a point on the line. Other points are also valid.']),vec('b',[-5,-1],['Read the coefficients of t to obtain a direction vector. Any nonzero scalar multiple is also valid.'])])
add('3.4',9,[choice('a',r'\((x,y,z)=(-3,1,0)+s(0,-3,6)+t(-5,1,2);\quad x=-3-5t,\ y=1-3s+t,\ z=6s+2t\)',[r'\(x=-3+5t,\ y=1+3s+t,\ z=6s-2t\)',r'\((x,y,z)=s(0,-3,6)+t(-5,1,2)\)'],['Start at the given point and add arbitrary multiples of the two nonparallel direction vectors.','Read off the three component equations. Both parameters are arbitrary real numbers.'])])
add('3.4',13,[choice('a',r'\((x,y)=t(3,2);\quad x=3t,\ y=2t\)',[r'\((x,y)=t(-2,3)\)',r'\((x,y)=(1,1)+t(3,2)\)'],['Choose (3,2), whose dot product with (-2,3) is -6+6=0.','The constant vector is zero because the line passes through the origin. Nonzero rescalings of the direction give equivalent parameterizations.'])])
add('3.4',15,[choice('a',r'\((x,y,z)=s(5,0,4)+t(0,1,0);\quad x=5s,\ y=t,\ z=4s\)',[r'\((x,y,z)=s(4,0,-5)+t(0,1,0)\)',r'\((x,y,z)=(1,0,0)+s(5,0,4)+t(0,1,0)\)'],['The desired plane has equation 4x-5z=0.','Two independent solutions are (5,0,4) and (0,1,0). Their dot products with the normal are zero.','Use their linear combinations with no constant offset, since the plane passes through the origin.'])])
for n,A in [(17,V([[1,1,1],[2,2,2],[3,3,3]])),(19,V([[1,5,1,2,-1],[1,-2,-1,3,2]]))]:
 basis=A.nullspace();letters=['s','t','r'];ans=r'\(x='+ '+'.join(letters[i]+s.latex(b,mat_delim='',mat_str='bmatrix') for i,b in enumerate(basis))+r'\), with arbitrary real parameters'
 for b in basis:assert A*b==s.zeros(A.rows,1)
 add('3.4',n,[choice('a',ans,['Only the zero vector.','No solutions.'],['Row reduction gives '+tex(A.rref()[0])+'.','Choose the nonpivot variables freely and solve for the pivot variables. This gives the displayed general solution.','Multiplying each displayed basis vector by the coefficient matrix gives zero, so every row is orthogonal to each basis vector and hence to every solution.'])])
add('3.4',21,[choice('a',r'\(x+y+z=0,\quad-2x+3y=0\)',[r'\(x+y+z=1,\ -2x+3y=1\)',r'\(x-y+z=0,\ 2x+3y=0\)'],['Set the dot product of (x,y,z) with each given vector equal to zero.']),choice('b','A line through the origin',['A plane through the origin','A single point'],['There are two independent equations in three unknowns, leaving one free parameter.']),choice('c',r'\((x,y,z)=t(3,2,-5),\quad t\in\mathbb R\)',[r'\((x,y,z)=t(1,1,1)\)',r'\((x,y,z)=t(-2,3,0)\)'],['The second equation gives x=3t,y=2t, and the first then gives z=-5t.','Both row dot products vanish: 3+2-5=0 and -6+6=0, confirming the row vectors are orthogonal to every solution.'])])
add('3.4',23,[choice('a',r'\(Ax=Ax_0+tAv\), with \(Av\ne0\)',[r'\(Ax=x_0+tv\) always.',r'The image must be a point.'],['Distribute A over the sum and scalar multiple.','If Av were zero, invertibility would force v=0, contradicting a line direction. Thus the image has a nonzero direction and is a line.']),choice('b',r'\((x,y)=(5,-9)+t(3,10);\quad x=5+3t,\ y=-9+10t\)',[r'\((x,y)=(5,-9)+t(5,-10)\)',r'\((x,y)=(1,3)+t(2,-1)\)'],[r'Compute \(A(1,3)^T=(5,-9)^T\) and \(A(2,-1)^T=(3,10)^T\).','Combine these as constant point plus t times direction, then read off the coordinate equations.'])])
u=V([3,2,-1]);v=V([0,2,-3]);w=V([2,6,7]);vals=[v.cross(w),w.cross(v),(u+v).cross(w),v.dot(v.cross(w)),v.cross(v),(u-3*w).cross(u-3*w)]
add('3.5',1,[num('d',0,['A cross product is perpendicular to its first factor, so this dot product is zero.']) if i==3 else vec(chr(97+i),a,['Use '+r'\(a\times b=(a_2b_3-a_3b_2,\ a_3b_1-a_1b_3,\ a_1b_2-a_2b_1)\)'+'.','A vector crossed with itself is zero.'] if i>=4 else ['Compute the three signed 2 by 2 minors for the cross product.']) for i,a in enumerate(vals)])
a=u.cross(v.cross(w));assert a==v*u.dot(w)-w*u.dot(v)
add('3.5',5,[vec('a',a,['First compute '+tex(v.cross(w))+' for v cross w, then cross u with this vector.',r'Check using \(u\times(v\times w)=v(u\cdot w)-w(u\cdot v)\).','Here u dot w=11 and u dot v=7, producing the same vector.'])])
u=V([-6,4,2]);v=V([3,1,5]);a=u.cross(v);assert a.dot(u)==a.dot(v)==0
add('3.5',7,[vec('a',a,['Take the cross product of u and v.','Both dot products with the result are zero. Any nonzero scalar multiple is also acceptable.'])])
u=V([1,-1,2]);v=V([0,3,1]);a=u.cross(v);add('3.5',9,[exact('a',a.norm(),['The cross product is '+tex(a)+'.','The parallelogram area is its norm.'])])
p=V([2,6,-1]);q=V([1,1,1]);r=V([4,6,2]);a=(q-p).cross(r-p);add('3.5',15,[exact('a',a.norm()/2,['Two edge vectors are '+tex(q-p)+' and '+tex(r-p)+'.','Their cross product is '+tex(a)+'.','The triangle area is half the norm of this cross product.'])])
u=V([2,-6,2]);v=V([0,4,-2]);w=V([2,2,-4]);add('3.5',17,[num('a',abs(u.dot(v.cross(w))),['Compute v cross w='+tex(v.cross(w))+'.','Dot with u and take the absolute value to obtain the volume '+tex(abs(u.dot(v.cross(w))))+'.'])])
u=V([-1,-2,1]);v=V([3,0,-2]);w=V([5,-4,0]);d=u.dot(v.cross(w));add('3.5',19,[yes('a',d==0,['The scalar triple product is '+tex(d)+'.','Here the scalar triple product is 16, which is nonzero, so the vectors are not coplanar.'])])
add('3.5',25,[num('a',-3,['Reversing the two factors of a cross product negates it; therefore the triple product becomes -3.']),num('b',3,['The dot product is commutative, so switching the two dot-product factors preserves the value 3.']),num('c',3,['A cyclic permutation of the three vectors preserves the scalar triple product.'])])
add('3.5',29,[choice('a',r'\(-2(u\times v)\)',[r'\(2(u\times v)\)',r'\(0\)'],['Distribute to obtain u cross u minus u cross v plus v cross u minus v cross v.','The self-cross-products vanish and v cross u=-(u cross v), leaving twice the negative cross product.'])])
r=V([0,2,-1]);F=1000/s.sqrt(2)*V([-1,0,1]);M=r.cross(F);assert M==1000/s.sqrt(2)*V([2,1,2])
add('3.5',31,[exact('a',M.norm(),[r'Take \(P=(1,0,1)\) and \(Q=(1,2,0)\), so \(r=Q-P=(0,2,-1)\).',r'The force points along the right-face diagonal in direction \((-1,0,1)\); hence \(F=\frac{1000}{\sqrt2}(-1,0,1)\).',r'The moment is \(r\times F=\frac{1000}{\sqrt2}(2,1,2)\). Its norm is the scalar moment, in newton-metres.']),choice('b',r'\(\alpha=48^\circ,\quad\beta=71^\circ,\quad\gamma=48^\circ\)',[r'\(\alpha=132^\circ,\ \beta=109^\circ,\ \gamma=132^\circ\)',r'\(\alpha=45^\circ,\ \beta=90^\circ,\ \gamma=45^\circ\)'],[r'Divide the components of (2,1,2) by its norm 3 to obtain direction cosines \((\frac{2}{3},\frac{1}{3},\frac{2}{3})\).','Take inverse cosines and round each angle to the nearest degree.'])])
save()
def rev(n,fs,related=None):
 key=f'anton-chapter-03-supplementary-{n}';Q[key]=dict(fields=fs,scope='All requested parts',complete=True,sourceImageReviewed=True)
 if related:Q[key]['relatedSourceQuestionIds']=[f'anton-chapter-03-supplementary-{k}' for k in related]
for n,(u,v,w) in enumerate([(V([-2,0,4]),V([3,-1,6]),V([2,-5,-5])),(V([3,-5,1]),V([-2,0,2]),V([0,-1,4])),(V([-2,6,2,1]),V([-3,0,8,0]),V([9,1,-6,-6]))],1):
 proj=w*(u.dot(w)/w.dot(w));assert s.simplify((u-proj).dot(w))==0
 fs=[vec('a',3*v-2*u,['Multiply v by 3 and u by 2, then subtract corresponding coordinates.']),exact('b',(u+v+w).norm(),['Add the three vectors coordinatewise, then take the square root of the sum of squares.']),exact('c',(-3*u-(v+5*w)).norm(),['Distance is the norm of the difference of the two vectors.',r'Compute \(-3u-v-5w\), then its norm.']),vec('d',proj,[r'Use \(\operatorname{proj}_w u=\frac{u\cdot w}{w\cdot w}w\).','The numerator is '+tex(u.dot(w))+' and the denominator is '+tex(w.dot(w))+'.'])]
 if n<3:
  triple=u.dot(v.cross(w));cross=(-5*v+w).cross(u.dot(v)*w);assert triple==V.hstack(u,v,w).det()
  fs.extend([num('e',triple,['Compute v cross w='+tex(v.cross(w))+', then dot with u.']),vec('f',cross,['First compute u dot v='+tex(u.dot(v))+'.','Scale w by this scalar, compute -5v+w, and take their cross product.'])])
 rev(n,fs,[1] if n>1 else None)
rev(4,[choice('a','A line through the origin',['A plane','A single nonzero point'],['One nonzero normal in two dimensions imposes one independent homogeneous equation, leaving dimension 1.']),choice('b','A plane through the origin',['A line','Only the origin'],['One nonzero normal in three dimensions imposes one independent homogeneous equation, leaving dimension 2.']),choice('c','Only the origin',['A line','The whole plane'],['Two noncollinear vectors in two dimensions span the plane, so their common orthogonal complement has dimension zero.']),choice('d','A line through the origin',['A plane','Only the origin'],['Two noncollinear vectors give two independent orthogonality equations in three unknowns, leaving dimension 1.'])])
rev(5,[choice('a','The plane through A, B, and C',['The line through A and B','A sphere centered at A'],['Since the points are not collinear, AB cross AC is a nonzero normal to their plane.','The equation requires AP to be orthogonal to that normal, exactly the point-normal description of the plane.'])])
rev(6,[choice('a','The lines are coplanar and nonparallel, so they intersect.',['The lines are parallel.','The lines are skew.'],['The nonzero cross product shows AB and CD are independent directions.','The zero scalar triple product puts AC in their span; write AC=s AB+t CD.','Then A+s AB=C-t CD gives a common point of the two lines.'])])
p7=V([3,-1,4]);q7=V([6,0,2]);r7=V([5,1,1]);p8=V([-3,1,0,6]);q8=V([0,5,1,-2]);r8=V([-4,1,4,0]);
rev(7,[vec('a',r7-2*(q7-p7),['PQ=(3,1,-2). Write S=R+t PQ.','The first coordinate condition gives 5+3t=-1, so t=-2. Substitute into the remaining coordinates.'])])
rev(8,[vec('a',r8+2*(q8-p8),['PQ=(3,4,1,-8). Write S=R+t PQ.','The third coordinate condition is 4+t=6, so t=2. Substitute to get all four coordinates.'])])
for n,p,q,r,related in [(9,p7,q7,r7,7),(10,p8,q8,r8,8)]:
 u=q-p;v=r-p;rev(n,[exact('a',s.simplify(u.dot(v)/(u.norm()*v.norm())),['The two displacement vectors are '+tex(u)+' and '+tex(v)+'.','Their dot product is '+tex(u.dot(v))+'. Divide it by the product of their norms.'])],[related])
rev(11,[exact('a',11/s.sqrt(35),[r'Put the plane in the form \(5x-3y+z+4=0\).',r'The distance is \(\frac{|5(-3)-3(1)+3+4|}{\sqrt{25+9+1}}=\frac{11}{\sqrt{35}}\).'])])
rev(12,[choice('a','Parallel: the second normal is -2 times the first.',['Perpendicular: the normals have zero dot product.','The planes are identical.'],['The normals (3,-1,6) and (-6,2,-12) are proportional.','Dividing the second equation by -2 gives 3x-y+6z=-1/2, so the parallel planes are distinct.']),exact('b',s.Rational(15,2)/s.sqrt(46),[r'Use the same normal for both equations; their constants differ by \(7-(-\frac{1}{2})=\frac{15}{2}\).',r'Divide by the normal length \(\sqrt{3^2+(-1)^2+6^2}=\sqrt{46}\).'])])
rev(13,[choice('a',r'\((x,y,z)=(-2,1,3)+s(1,-2,-2)+t(5,-1,-5);\quad x=-2+s+5t,\ y=1-2s-t,\ z=3-2s-5t\)',[r'\((x,y,z)=s(1,-2,-2)+t(5,-1,-5)\)',r'\((x,y,z)=(-2,1,3)+s(1,2,2)+t(5,1,5)\)'],['Subtract P from Q and R to obtain two independent plane directions.','Add arbitrary multiples of those directions to P; then read off the three coordinate equations.'])])
rev(14,[choice('a',r'\((x,y,z)=(-1,6,0)+t(4,0,-1);\quad x=-1+4t,\ y=6,\ z=-t\)',[r'\((x,y,z)=(-1,6,0)+t(1,0,4)\)',r'\((x,y,z)=t(4,0,-1)\)'],['A line perpendicular to the plane uses its normal (4,0,-1) as direction.','Start at P and add t times that direction.'])])
rev(15,[choice('a',r'\((x,y)=(0,-3)+t(8,-1);\quad x=8t,\ y=-3-t\)',[r'\((x,y)=t(8,-1)\)',r'\((x,y)=(0,-3)+t(1,8)\)'],['Use the given point as base point and the given parallel vector as direction.','Equate coordinates for the parametric equations.'])])
rev(16,[choice('a',r'\((x,y,z)=(-2,1,0)+s(1,0,-8)+t(0,1,6);\quad x=-2+s,\ y=1+t,\ z=-8s+6t\)',[r'\((x,y,z)=s(1,0,-8)+t(0,1,6)\)',r'\((x,y,z)=(-2,1,0)+s(1,0,8)+t(0,1,-6)\)'],['The required plane has normal (-8,6,-1) and passes through P. Its equation is -8x+6y-z=22.','The two displayed directions are independent and have zero dot product with the normal. Add them to the base point with arbitrary parameters.'])])
rev(17,[choice('a',r'\((x,y)=(0,-5)+t(1,3);\quad x=t,\ y=-5+3t\)',[r'\((x,y)=(0,5)+t(1,3)\)',r'\((x,y)=(0,-5)+t(3,1)\)'],['Set x=t in the given equation. Then y=3t-5.','Collect constants and parameter coefficients to obtain the vector form.'])])
rev(18,[choice('a',r'\((x,y,z)=(\frac{5}{2},0,0)+s(3,1,0)+t(-\frac{3}{2},0,1);\quad x=\frac{5}{2}+3s-\frac{3}{2}t,\ y=s,\ z=t\)',[r'\((x,y,z)=s(3,1,0)+t(-\frac{3}{2},0,1)\)',r'\(x=\frac{5}{2}-3s+\frac{3}{2}t,\ y=s,\ z=t\)'],['Take y=s and z=t as free parameters.',r'Solve \(2x=5+6s-3t\) for x and collect the constant and direction vectors.'])])
n=V([0,-1,3]).cross(V([2,-1,0]));assert n==V([3,6,2])
rev(19,[choice('a',r'\(3(x+1)+6(y-5)+2(z-6)=0\)',[r'\(3(x-1)+6(y+5)+2(z+6)=0\)',r'\(3x+6y+2z=0\)'],['Cross the two direction vectors to obtain normal (3,6,2).','Use base point (-1,5,6) in the point-normal equation.'])])
rev(20,[choice('a',r'\(-5(x+5)+2(y-1)=0\)',[r'\(-5(x-5)+2(y+1)=0\)',r'\(2(x+5)+5(y-1)=0\)'],['The line direction (-5,2,0) is a normal to the perpendicular plane.','Use the given point (-5,1,0) in the point-normal formula.'])])
p=V([9,0,4]);q=V([-1,4,3]);r=V([6,6,-2]);n=(q-p).cross(r-p);assert n==V([-18,-57,-48])
rev(21,[choice('a',r'\(6(x-9)+19y+16(z-4)=0\)',[r'\(6(x+9)+19y+16(z+4)=0\)',r'\(6x+19y+16z=0\)'],['Compute the edge vectors (-10,4,-1) and (-3,6,-6).','Their cross product is (-18,-57,-48). Divide by -3 to get normal (6,19,16).','Substitute P=(9,0,4) in the point-normal equation.'])])
rev(22,[choice('a',r'\(v\cdot w=\sum_{i=1}^{3}\sum_{j=1}^{2}a_i b_j(v_i\cdot w_j)=0\)',[r'\(v\cdot w=\sum_i a_i+\sum_j b_j\)',r'\(v\cdot w=1\)'],['Distribute the dot product over both linear combinations and pull out each scalar.','Every one of the six inner dot products is zero by hypothesis, so the entire sum is zero. Thus the combinations are orthogonal.'])])
rev(23,[choice('a',r'\(d=\frac{\|AP\times AB\|}{\|AB\|}\)',[r'\(d=\|AP\times AB\|\|AB\|\)',r'\(d=\frac{|AP\cdot AB|}{\|AB\|}\)'],['The parallelogram spanned by AP and AB has area base times height, '+r'\(\|AB\|d\)'+'.','The same area is the norm of their cross product. Since A and B are distinct, divide by the nonzero base length.'])])
rev(24,[choice('a','False as printed: negative multiples need not give equality.',['True for every real scalar multiple.','Equality is impossible for nonzero vectors.'],['Take u=(1,0,0) and v=(-1,0,0). Their sum has norm 0, whereas their separate norms sum to 2.','Thus an unrestricted scalar multiple is not sufficient.']),choice('b','Correct condition: one vector is a nonnegative scalar multiple of the other.',['Correct condition: one is any real scalar multiple of the other.','Correct condition: the two vectors are orthogonal.'],['If either vector is zero, equality holds. For nonzero vectors, square the norm equality and cancel to obtain '+r'\(u\cdot v=\|u\|\|v\|\)'+'.','This says the cosine of their angle is 1, so they have the same direction and are positive scalar multiples.','Conversely, if v=cu with c nonnegative, both sides equal (1+c) times the norm of u.'])]);Q['anton-chapter-03-supplementary-24']['reviewNotice']='The printed statement omits “nonnegative” before “scalar multiple.” The check identifies the counterexample and establishes the corrected theorem.'
rev(25,[choice('a','A plane through the origin containing the entire z-axis, with normal (A,B,0).',['A line through the origin in three dimensions.','A sphere centered at the origin.'],['Since A and B are not both zero, (A,B,0) is a nonzero normal in three dimensions.','The equation imposes one independent condition, leaving a plane. The z coordinate is free, and every point (0,0,z) satisfies it.'])])
save()
assert len(Q)==75
assert set(Q)=={q['id'] for q in json.load(open('tmp/linear-ch3-input.json'))}
print('Verified 75 chapter 3 questions, vector arithmetic/projections/cross products, and complete ID coverage.')
