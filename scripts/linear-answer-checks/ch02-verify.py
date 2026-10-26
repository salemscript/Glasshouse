import json,sympy as s
from pathlib import Path
Q={}
def tex(v): return '\\('+s.latex(v,mat_delim='',mat_str='bmatrix')+'\\)'
def add(sec,n,fields,scope='All requested parts'):
 Q[f'anton-section-{sec.replace(".","-")}-{n}' if sec!='review' else f'anton-review-2-{n}']={'fields':fields,'scope':scope,'complete':True,'sourceImageReviewed':True}
def num(label,a,steps,prompt=None):
 return dict(label=label,selectionPrompt=prompt or 'Enter the value.',type='numeric',answer=float(a),tolerance=1e-8,explanation=' '.join(steps),workedSteps=steps)
def choice(label,a,wrong,steps,prompt='Select the complete correct result.'):
 return dict(label=label,selectionPrompt=prompt,type='choice',answer=a,options=[a]+wrong,explanation=' '.join(steps),workedSteps=steps)
def matfield(label,A,steps):
 return choice(label,tex(A),[tex(A+s.ones(*A.shape)),tex(-A) if A!=s.zeros(*A.shape) else tex(A+2*s.ones(*A.shape))],steps)
def det(sec,n,A):
 A=s.Matrix(A);d=A.det();steps=[]
 if sec=='2.2' and n in [9,12]:
  U=A.copy()
  for j in range(A.rows):
   for i in range(j+1,A.rows):
    if U[i,j]:
     m=U[i,j]/U[j,j];U.row_op(i,lambda v,k:v-m*U[j,k]);steps.append('Subtract '+tex(m)+' times row '+str(j+1)+' from row '+str(i+1)+'.')
  steps+=['These row additions preserve the determinant and produce '+tex(U)+'.','Multiply the diagonal entries to obtain '+tex(d)+'.'];assert s.prod(U[i,i] for i in range(A.rows))==d
 elif A.is_diagonal():steps=['For a diagonal matrix, multiply the diagonal entries: '+', '.join(tex(A[i,i]) for i in range(A.rows))+'.','The product is '+tex(d)+'.']
 else:steps=['Expand along the first row of '+tex(A)+'.','The signed cofactor contributions are '+', '.join(tex(A[0,j]*A.cofactor(0,j)) for j in range(A.cols))+'.','Their sum is '+tex(d)+'.']
 add(sec,n,[num('a',d,steps)]);assert d==A.det(method='berkowitz')
A=s.Matrix([[1,-2,3],[6,7,-1],[-3,1,4]]);M=s.Matrix(3,3,lambda i,j:A.minor(i,j));C=A.cofactor_matrix()
add('2.1',1,[matfield('a',M,['Delete row i and column j and take the remaining 2 by 2 determinant.','The matrix of minors is '+tex(M)+'.']),matfield('b',C,['Multiply each minor by '+r'\((-1)^{i+j}\)'+'.','The cofactor matrix is '+tex(C)+'.'])])
A=s.Matrix([[3,5],[-2,4]]);add('2.1',5,[num('a',22,['Compute '+r'\(3(4)-5(-2)=22\)'+'.']),matfield('b',A.inv(),['Swap diagonal entries, negate off-diagonal entries, and divide by 22.','The inverse is '+tex(A.inv())+'.'])]);assert A*A.inv()==s.eye(2)
add('2.1',6,[num('a',0,['The determinant is '+r'\(4(2)-1(8)=0\)'+'.']),choice('b','Not invertible',['Invertible'],['A zero determinant means no inverse exists.'])])
a=s.symbols('a');add('2.1',9,[choice('a',tex(a*a-5*a+21),[tex(a*a-5*a-9),tex(a*a+a+21)],[r'\(\det A=(a-3)(a-2)-5(-3)\).','Expand to obtain '+tex(a*a-5*a+21)+'.'])])
add('2.1',15,[choice('a',r'\(\lambda=-3,1\)',[r'\(\lambda=3,-1\)',r'\(\lambda=-2,4\)'],[r'\(\det A=(\lambda-2)(\lambda+4)+5=\lambda^2+2\lambda-3\).',r'Factor as \((\lambda+3)(\lambda-1)\); either factor must be zero.'])])
det('2.1',21,[[-3,0,7],[2,5,1],[-1,0,5]]);det('2.1',27,[[1,0,0],[0,-1,0],[0,0,1]])
add('2.1',36,[choice('a',r'\(\frac{1}{2}[(a+d)^2-(a^2+2bc+d^2)]=ad-bc\)',[r'\(\frac{1}{2}[(a+d)^2+(a^2+2bc+d^2)]=ad+bc\)',r'\(\frac{1}{2}(a+d)=ad-bc\)'],[r'Write \(A=\begin{bmatrix}a&b\\c&d\end{bmatrix}\). Then \(\operatorname{tr}(A)=a+d\) and \(\operatorname{tr}(A^2)=a^2+2bc+d^2\).','Expanding the displayed 2 by 2 determinant gives the selected expression, equal to the determinant of A.'])])
add('2.1',38,[num('a',6,['Every row must contain a nonzero entry, so at least three entries are nonzero.','The identity matrix has six zeros and determinant 1, attaining the bound.'])])
add('2.1',41,[choice('a',r'\((b_1-b_2)x+(a_2-a_1)y+a_1b_2-a_2b_1=0\)',[r'\((b_1+b_2)x+(a_1+a_2)y=0\)',r'\((a_1-a_2)x+(b_1-b_2)y=1\)'],['Expand the determinant along the first row.','Substitution of either given point makes two rows equal, so both points satisfy the equation.','Since the points are distinct, the coefficients of x and y are not both zero; this is their unique line.'])])
add('2.2',1,[num('a',-11,[r'\(\det A=(-2)4-3(1)=-11\).',r'\(\det A^T=(-2)4-1(3)=-11\), verifying equality.'])])
det('2.2',5,s.diag(1,1,-5,1));det('2.2',8,s.diag(1,-s.Rational(1,3),1,1));det('2.2',9,[[3,-6,9],[-2,7,-2],[0,1,5]]);det('2.2',12,[[1,-3,0],[-2,4,1],[5,-2,2]])
add('2.2',15,[num('a',-6,['The cyclic permutation of three rows consists of two row swaps.','Two sign changes cancel, leaving the original determinant -6.'])]);add('2.2',16,[num('a',6,['Interchange the first and third rows of the given matrix.','One row swap negates the determinant: -(-6)=6.'])])
add('2.2',25,[choice('a',r'\(C_3\leftarrow C_3-C_1-C_2\)',[r'\(C_3\leftarrow 2C_3\)',r'\(C_1\leftrightarrow C_3\)'],['Subtracting multiples of other columns leaves the determinant unchanged.','The third column becomes c, proving the equality.'])])
add('2.2',28,[choice('a',r'\(C_3\leftarrow C_3-rC_2+(rt-s)C_1;\ C_2\leftarrow C_2-tC_1\), then transpose',[r'Scale the determinant by \(rst\).',r'Interchange the first two columns only.'],['The first operation removes both the b and a terms from the third column.','The second operation leaves columns a,b,c. Neither operation changes the determinant.','Transposing produces the displayed right-hand matrix, without changing its determinant.'])])
add('2.2',29,[choice('a',r'\(R_3=R_1+R_2\)',[r'\(R_4=R_1+R_2\)',r'\(R_2=2R_1\)'],['The sum of the first two rows is (1,10,6,5), exactly the third row.','Subtracting those rows gives a zero row, so the determinant is zero.'])])
add('2.3',1,[num('a',-40,[r'\(\det A=-4-6=-10\).',r'\(\det(2A)=(-2)(8)-(4)(6)=-40=2^2\det A\).'])])
A=s.Matrix([[2,1,0],[3,4,0],[0,0,2]]);B=s.Matrix([[1,-1,3],[7,1,2],[5,0,1]])
add('2.3',5,[num('a',(A*B).det(),['Multiplication gives '+tex(A*B)+'.','Its determinant, and that of BA, are both '+tex((A*B).det())+'.']),choice('b',f'No: det(A+B)={ (A+B).det() }, whereas det(A)+det(B)={ A.det()+B.det() }',['Yes, both are equal.','No: det(A+B)=0.'],['Compute the two individual determinants: '+tex(A.det())+' and '+tex(B.det())+'.','Their sum differs from '+tex((A+B).det())+', the determinant of the sum.'])]);assert (A*B).det()==(B*A).det()
A=s.Matrix([[2,5,5],[-1,-1,0],[2,4,3]])
for n in [7,19]:
 fs=[num('a',A.det(),['Cofactor expansion gives determinant '+tex(A.det())+'.']),choice('b','Invertible',['Not invertible'],['The determinant is nonzero.'])]
 if n==19:fs.append(matfield('c',A.inv(),['The adjugate is '+tex(A.adjugate())+'.','Divide by the determinant to get '+tex(A.inv())+'.']));assert A*A.inv()==s.eye(3)
 add('2.3',n,fs)
add('2.3',14,[choice('a','Not invertible; determinant 0',['Invertible; determinant 1','Invertible; determinant -1'],['The third column is zero, so cofactor expansion along it gives determinant zero.'])])
add('2.3',15,[choice('a',r'\(k\ne\frac{5+\sqrt{17}}2,\frac{5-\sqrt{17}}2\)',[r'\(k\ne 2,3\)',r'\(k=2,3\)'],[r'\(\det A=(k-3)(k-2)-4=k^2-5k+2\).','The quadratic formula gives the two roots; exclude exactly those values.'])])
A=s.Matrix([[7,-2],[3,1]]);b=s.Matrix([3,5]);x=A.inv()*b;assert A*x==b
add('2.3',24,[matfield('a',x,[r'\(D=13,\ D_1=13,\ D_2=26\).',r'Cramer’s rule gives \(x_1=\frac{D_1}{D}=1,\ x_2=\frac{D_2}{D}=2\).'])])
add('2.3',29,[choice('a',r'Cramer’s rule does not apply; \((x_1,x_2,x_3)=(\frac{29-5t}{20},\frac{7+5t}{20},t)\), \(t\in\mathbb R\)',[r'No solutions.',r'Unique solution \((1,1,2)\).'],['The third coefficient row is the sum of the first two, and 5=4+1, so the determinant is zero and the equations are dependent.',r'Set \(x_3=t\); solving the first two equations gives \(20x_1=29-5t\) and \(20x_2=7+5t\).'])])
add('2.3',33,[num(l,v,[st]) for l,v,st in [('a',-189,r'\(\det(3A)=3^3(-7)=-189\).'),('b',-s.Rational(1,7),r'\(\det(A^{-1})=\frac{1}{-7}=-\frac{1}{7}\).'),('c',-s.Rational(8,7),r'\(\det(2A^{-1})=2^3(-\frac{1}{7})=-\frac{8}{7}\).'),('d',-s.Rational(1,56),r'\(\det((2A)^{-1})=\frac{1}{2^3(-7)}=-\frac{1}{56}\).'),('e',7,'Transpose A and swap its second and third columns; transposition preserves and one swap reverses the determinant.')]])
add('2.3',36,[choice('a',r'\(\det(A^TA)=\det(A^T)\det(A)=(\det A)^2\)',[r'\(\det(A^TA)=2\det A\)',r'\(\det(A^TA)=0\) for every A'],['Apply the product rule and equality of a determinant with that of its transpose.','A square is nonzero exactly when its base is nonzero. Thus A and its Gram matrix are invertible under exactly the same condition.'])])
def save():Path('scripts/linear-answer-checks/ch02-reviewed.json').write_text(json.dumps({'chapter':2,'questions':Q},indent=2))
save()
# Supplementary review, visually transcribed from source crops.
def rev(n,fields,related=None):
 key=f'anton-chapter-02-supplementary-{n}';Q[key]=dict(fields=fields,scope='All requested parts',complete=True,sourceImageReviewed=True)
 if related:Q[key]['relatedSourceQuestionIds']=[f'anton-chapter-02-supplementary-{k}' for k in related]
matrices=[s.Matrix(x) for x in [[[-4,2],[3,3]],[[7,-1],[-2,-6]],[[-1,5,2],[0,2,-1],[-3,1,1]],[[-1,-2,-3],[-4,-5,-6],[-7,-8,-9]],[[3,0,-1],[1,1,1],[0,4,2]],[[-5,1,4],[3,0,2],[1,-2,2]],[[3,6,0,1],[-2,3,1,4],[1,0,-1,1],[-9,2,-2,2]],[[-1,-2,-3,-4],[4,3,2,1],[1,2,3,4],[-4,-3,-2,-1]]]]
for n,A in enumerate(matrices,1):
 d=A.det();terms=[A[0,j]*A.cofactor(0,j) for j in range(A.cols)]
 # Elimination with determinant-preserving row additions (all leading pivots here nonzero until singular).
 U=A.copy();ops=[];sign=1
 for j in range(A.rows):
  if U[j,j]==0:
   idx=next((i for i in range(j+1,A.rows) if U[i,j]!=0),None)
   if idx is None:continue
   U.row_swap(j,idx);sign*=-1;ops.append(f'Swap rows {j+1} and {idx+1}.')
  for i in range(j+1,A.rows):
   if U[i,j]:
    m=U[i,j]/U[j,j];U.row_op(i,lambda v,k:v-m*U[j,k]);ops.append(r'\(R_'+str(i+1)+r'\leftarrow R_'+str(i+1)+'-('+s.latex(m)+')R_'+str(j+1)+r'\).')
 assert sign*s.prod(U[i,i] for i in range(A.rows))==d
 rev(n,[num('a',d,['Expand along the first row. The signed contributions are '+', '.join(tex(t) for t in terms)+'.','Their sum is '+tex(d)+'.']),num('b',d,ops+['The triangular matrix is '+tex(U)+'.','Multiply its diagonal entries and account for row swaps to obtain '+tex(d)+'.'])])
rev(9,[num(chr(97+i),matrices[i+2].det(),['For Exercise '+str(i+3)+', add the three downward diagonal products and subtract the three upward products.','The result is '+tex(matrices[i+2].det())+'.']) for i in range(4)],range(3,7))
rev(10,[choice('a',r'\(\begin{bmatrix}1&0&0&0\\2&3&5&7\\4&6&1&2\\3&8&4&5\end{bmatrix}\)',[r'A dense 4 by 4 matrix with no zeros.',r'A 3 by 3 identity matrix.'],['One valid example is selected; many others are possible.','Expanding the first row immediately reduces to one 3 by 3 determinant, while elimination requires several row operations.']),choice('b',r'\(\begin{bmatrix}1&2&3&4\\1&3&3&4\\1&2&4&4\\1&2&3&5\end{bmatrix}\)',[r'A 4 by 4 diagonal matrix.',r'A 2 by 2 matrix of ones.'],['Subtract the first row from each other row. The result is upper triangular with diagonal 1,1,1,1.','The original matrix has no zero entries, so straightforward cofactor expansion has more terms. Other valid examples are possible.'])])
for n,start in [(11,0),(12,4)]:
 rev(n,[choice(chr(97+i),'Invertible' if matrices[start+i].det()!=0 else 'Not invertible',['Not invertible' if matrices[start+i].det()!=0 else 'Invertible'],['Exercise '+str(start+i+1)+' has determinant '+tex(matrices[start+i].det())+'.','A matrix is invertible exactly when its determinant is nonzero.']) for i in range(4)],range(start+1,start+5))
a,b,x=s.symbols('a b x')
for n,A in [(13,s.Matrix([[5,b-3],[b-2,-3]])),(14,s.Matrix([[3,-4,a],[a*a,1,2],[2,a-1,4]]))]:
 d=s.expand(A.det());rev(n,[choice('a',tex(d),[tex(d+1),tex(-d)],['Expand the determinant using signed products of entries and minors.','Collecting terms gives '+tex(d)+'.'])])
rev(15,[num('a',-120,['Reverse the five columns, requiring 10 swaps and hence no net sign change.','Multiply the resulting diagonal entries: '+r'\((-3)(-4)(-1)(2)(5)=-120\)'+'.'])])
L=x*(1-x)+3;R=s.Matrix([[1,0,-3],[2,x,-6],[1,3,x-5]]).det();assert s.expand(L-R)==-2*x*x+3*x+3
rev(16,[choice('a',r'\(x=\frac{3\pm\sqrt{33}}4\)',[r'\(x=1,-\frac{3}{2}\)',r'\(x=0,2\)'],[r'The left determinant is \(x-x^2+3\). Subtract twice row 1 from row 2 and row 1 from row 3 on the right, obtaining determinant \(x(x-2)\).',r'Equate the determinants and rearrange: \(2x^2-3x-3=0\). Apply the quadratic formula.'])])
for n,A in enumerate(matrices,17):
 if A.det():
  inv=A.inv();assert A*inv==s.eye(A.rows)
  fs=[matfield('a',inv,['The determinant is '+tex(A.det())+'.','Transpose the cofactor matrix to get '+tex(A.adjugate())+'.','Divide by the determinant: '+tex(inv)+'.'])]
 else:fs=[choice('a','No inverse exists',['The inverse is the identity.','The inverse is the zero matrix.'],['The matrix has determinant 0. The adjugate formula cannot be divided by zero, and the matrix is singular.'])]
 rev(n,fs,[n-16])
rev(25,[choice('a',r'\(x\prime=\frac{3x+4y}{5},\quad y\prime=\frac{-4x+3y}{5}\)',[r'\(x\prime=\frac{3x-4y}{5},\ y\prime=\frac{4x+3y}{5}\)',r'\(x\prime=x,\ y\prime=y\)'],[r'The coefficient determinant is \(\frac{9}{25}+\frac{16}{25}=1\).',r'Replacing column 1 gives \(\frac{3x+4y}{5}\); replacing column 2 gives \(\frac{3y-4x}{5}\). Divide each by 1.'])])
rev(26,[choice('a',r'\(x\prime=x\cos\theta+y\sin\theta,\quad y\prime=-x\sin\theta+y\cos\theta\)',[r'\(x\prime=x\cos\theta-y\sin\theta,\ y\prime=x\sin\theta+y\cos\theta\)',r'\(x\prime=x,\ y\prime=y\)'],[r'The coefficient determinant is \(\cos^2\theta+\sin^2\theta=1\).','Cramer’s replaced-column determinants give the two expressions in the selected answer.'])])
a,b=s.symbols('alpha beta');A=s.Matrix([[1,1,a],[1,1,b],[a,b,1]]);assert s.factor(A.det())==-(a-b)**2
rev(27,[choice('a',r'\(\det A=-(\alpha-\beta)^2=0\iff\alpha=\beta\)',[r'\(\det A=\alpha+\beta=0\iff\alpha=-\beta\)',r'\(\det A=1\), so never.'],['Subtract row 1 from row 2, then expand along row 2 to obtain the negative squared difference.','A square homogeneous system has a nonzero solution exactly when its coefficient determinant vanishes.'])])
import itertools
assert max(s.Matrix(3,3,v).det() for v in itertools.product([0,1],repeat=9))==2
rev(28,[num('a',2,['The six-term determinant formula has three positive and three negative terms, each 0 or 1.','A value 3 would require all three positive products to equal 1, forcing all nine entries to be 1; the negative products would then also equal 1. Thus the determinant is at most 2.',r'The matrix \(\begin{bmatrix}1&1&0\\0&1&1\\1&0&1\end{bmatrix}\) has determinant 2, attaining the bound.'])])
rev(29,[choice('a',r'\(b\cos\gamma+c\cos\beta=a,\ c\cos\alpha+a\cos\gamma=b,\ a\cos\beta+b\cos\alpha=c\)',[r'All three left sides are zero.',r'Replace each cosine by sine in the equations.'],['Project the two sides adjacent to each chosen side onto that side. Their signed projections add to its full length, giving the three identities.']),choice('b',r'\(\cos\alpha=\frac{b^2+c^2-a^2}{2bc},\quad\cos\beta=\frac{a^2+c^2-b^2}{2ac},\quad\cos\gamma=\frac{a^2+b^2-c^2}{2ab}\)',[r'\(\cos\alpha=\cos\beta=\cos\gamma=1\)',r'\(\cos\alpha=\frac{a^2-b^2-c^2}{2bc}\), with cyclic analogues.'],[r'For unknowns \((\cos\alpha,\cos\beta,\cos\gamma)\), the coefficient matrix is \(\begin{bmatrix}0&c&b\\c&0&a\\b&a&0\end{bmatrix}\), whose determinant is \(2abc\).',r'The replaced-column determinants are \(a(b^2+c^2-a^2)\), \(b(a^2+c^2-b^2)\), and \(c(a^2+b^2-c^2)\). Divide each by \(2abc\).'])])
rev(30,[choice('a',r'\(\det\begin{bmatrix}1-\lambda&-2\\1&-1-\lambda\end{bmatrix}=\lambda^2+1>0\)',[r'The determinant is \(\lambda^2-1\).',r'The determinant is zero for all real \(\lambda\).'],['Move the right-hand terms to the left to form a homogeneous system.',r'The determinant is \((1-\lambda)(-1-\lambda)+2=\lambda^2+1\), always positive for real lambda. Hence its only solution is x=y=0.'])])
rev(31,[choice('a',r'\([\operatorname{adj}(A)]^{-1}=\frac{A}{\det A}=\operatorname{adj}(A^{-1})\)',[r'\([\operatorname{adj}(A)]^{-1}=A\det A\)',r'\([\operatorname{adj}(A)]^{-1}=A^{-1}\) always'],[r'Use \(\operatorname{adj}(A)=\det(A)A^{-1}\). Since both factors are invertible, its inverse is \(\frac{A}{\det A}\).',r'Also \(\operatorname{adj}(A^{-1})=\det(A^{-1})(A^{-1})^{-1}=\frac{A}{\det A}\).'])])
rev(32,[choice('a',r'\(\det(\operatorname{adj}A)=(\det A)^{n-1}\)',[r'\(\det(\operatorname{adj}A)=(\det A)^n\)',r'\(\det(\operatorname{adj}A)=n\det A\)'],[r'For invertible A, take determinants of \(\operatorname{adj}A=(\det A)A^{-1}\), yielding \(\frac{(\det A)^n}{\det A}\).','For singular A, apply the identity to A+tI for values t with nonzero determinant, then let t tend to zero. Determinants and cofactors are polynomials, so continuity preserves equality. For n=1 both sides equal 1.'])])
rev(33,[choice('a',r'\(A\begin{bmatrix}1\\\vdots\\1\end{bmatrix}=0\), so A is singular and \(\det A=0\).',[r'The row sums imply A is the zero matrix.',r'The row sums imply \(\det A=1\).'],['Each entry of the product is the corresponding row sum, hence zero.','The all-ones vector is nonzero, giving a nontrivial null vector. A square matrix with such a vector is singular.'])])
rev(34,[choice('a',r'\(\frac{1}{2}[(x_3-x_1)(y_1+y_3)+(x_2-x_3)(y_3+y_2)-(x_2-x_1)(y_1+y_2)]\)',[r'Add the areas of all three trapezoids.',r'Subtract all three trapezoid areas from zero.'],['Apply one-half times width times the sum of the vertical sides to each trapezoid.','Expanding cancels the matching terms and leaves one-half of '+r'\(x_1y_2+x_2y_3+x_3y_1-x_1y_3-x_2y_1-x_3y_2\)'+', the displayed determinant.']),num('b',s.Rational(19,2),[r'Insert the vertices into \(\begin{bmatrix}3&3&1\\4&0&1\\-2&-1&1\end{bmatrix}\).','The determinant is -19; take one-half its absolute value, giving 19/2 square units.'])])
rev(35,[choice('a',r'\(C_5\leftarrow10000C_1+1000C_2+100C_3+10C_4+C_5\)',[r'Swap the first and fifth columns.',r'Divide every column by 19.'],['Adding multiples of other columns to column 5 preserves the determinant.','The new last column contains exactly the five given multiples of 19. Factor 19 from that column; the remaining determinant is an integer.'])])
rev(36,[choice('a',r'\(C_3=(\cos\delta)C_1+(\sin\delta)C_2\)',[r'\(C_3=C_1+C_2\) for every delta.',r'\(C_3=C_1-C_2\) for every delta.'],['The sine addition identity gives the stated linear combination in every row.','Subtract this combination from column 3 to create a zero column, proving the determinant is zero.'])])
rev(37,[choice('a','Not linear',['Linear'],[r'Interpreting the input as \(\mathbb R^4\), let v=(1,0,0,1), corresponding to the identity matrix. Then \(T(v)=1\) but \(T(2v)=4\ne2T(v)\).','The required scalar multiplication property fails.'])]);Q['anton-chapter-02-supplementary-37']['reviewNotice']='The source prints a domain of R² but gives four input coordinates; the intended domain is R⁴ (or the space of 2 by 2 matrices).'
save()
assert len(Q)==67
assert set(Q)=={q['id'] for q in json.load(open('tmp/linear-ch2-input.json'))}
print('Verified 67 chapter 2 questions, exact determinants/inverses, and complete ID coverage.')
# Canonical source crops, checked against actual PDF text/vector bounding boxes.
# Keep instructions text-only and every matrix complete inside its problem crop.
import copy
source_repairs={
 '2-1-1': {'instructions': [37,558.54,255,13], 'problem':[34,572,127.91,41]},
 '2-1-21': {'instructions':[62,487.42,255,23], 'problem':[59,516,127.99,40]},
 '2-1-27': {'instructions':[328,50.77,255,23], 'problem':[325,74,126.5,40]},
 '2-2-1': {'problem':[59,354.69,127.99,28]},
 '2-2-9': {'instructions':[62,594.67,255,34], 'problem':[59,636,127.99,40]},
 '2-2-12': {'instructions':[62,594.67,255,34], 'problem':[186.99,693,130.01,39]},
 '2-3-1': {'problem':[34,583.4,127.91,28]},
 '2-3-5': {'instructions':[37,717.38,255,22.92], 'problem':[300,570,258,41], 'singleInstructions':True},
 '2-3-7': {'instructions':[303,671.54,255,23], 'problem':[300,699,126.42,40]},
 '2-3-14': {'instructions':[303,671.54,255,23]},
 '2-3-15': {'problem':[59,221.48,127.99,27]},
 '2-3-19': {'instructions':[62,301.8,255,23], 'problem':[59,327,127.99,39]},
}
for src in json.load(open('tmp/linear-ch2-input.json')):
 key=src['id'].replace('anton-section-','')
 if key not in source_repairs:continue
 repair=source_repairs[key];parts=copy.deepcopy(src['parts']);seen_instruction=False;kept=[]
 for part in parts:
  role=part['role']
  if role=='instructions' and repair.get('singleInstructions'):
   if seen_instruction:continue
   seen_instruction=True
  if role in repair:part['crops']=[repair[role]]
  kept.append(part)
 Q[src['id']]['sourceFigureParts']=kept
 Q[src['id']]['reviewNotice']='Source crop repaired against the chapter PDF: matrix rows stay together, and neighboring exercise fragments are excluded.'
save()
