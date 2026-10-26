import json, sympy as s
from pathlib import Path
M=s.Matrix; R=s.Rational; rt=s.sqrt; x=s.symbols('x', real=True)
OUT={}
def tex(v):
 if isinstance(v,s.MatrixBase): return s.latex(v,mat_delim='',mat_str='bmatrix')
 return s.latex(s.sympify(v))
def math(v): return r'\('+ (v if isinstance(v,str) else tex(v))+r'\)'
def choice(label,prompt,answer,others,steps):
 assert len(set([answer]+others))==len([answer]+others)
 return dict(label=label,selectionPrompt=prompt,type='choice',answer=answer,options=[answer]+others,explanation=steps[-1],workedSteps=steps)
def num(label,prompt,val,steps): return dict(label=label,selectionPrompt=prompt,type='numeric',answer=float(val),tolerance=1e-6,explanation=steps[-1],workedSteps=steps)
def cf(label,prompt,val,steps,others=None):
 if others is None:
  if isinstance(val,s.MatrixBase):
   w=M(val);w[0]+=1;z=M(val);z[0]-=1; others=[w,z]
  else: others=[val+1,val-1]
 return choice(label,prompt,math(val),[math(v) for v in others],steps+[f'The result is {math(val)}.'])
def add(id,*fields,notice=None):
 q=dict(fields=list(fields),scope='All requested subparts, with proof or drawing tasks adapted to specific answer choices.',complete=True,sourceImageReviewed=True)
 if notice:q['reviewNotice']=notice
 OUT[id if id.startswith('anton') else 'anton-section-7-'+id]=q
def proof(id,answer,wrong1,wrong2,steps,label='a',prompt='Select the valid conclusion and reasoning.'):
 add(id,choice(label,prompt,answer,[wrong1,wrong2],steps))
def flush():Path('scripts/linear-answer-checks/ch07-reviewed.json').write_text(json.dumps({'chapter':7,'questions':OUT},indent=2,ensure_ascii=False)+'\n')
# Chapter 7.1
A5=M([[R(4,5),0,-R(3,5)],[-R(9,25),R(4,5),-R(12,25)],[R(12,25),R(3,5),R(16,25)]])
def orthfield(label,A):
 assert s.simplify(A.T*A)==s.eye(A.rows)
 return choice(label,'Select the orthogonality conclusion and inverse.','Orthogonal; '+math('A^{-1}='+tex(A.T)),['Orthogonal; '+math('A^{-1}='+tex(-A.T)),'Not orthogonal.'],['Compute '+math('A^TA=I')+'. Thus the columns are an orthonormal set.','For an orthogonal matrix, '+math('A^{-1}=A^T')+'.'])
add('1-1',orthfield('a',s.diag(1,-1)),orthfield('b',M([[1,-1],[1,1]])/rt(2)))
A=M([[R(1,2)]*4,[R(1,2),-R(5,6),R(1,6),R(1,6)],[R(1,2),R(1,6),R(1,6),-R(5,6)],[R(1,2),R(1,6),-R(5,6),R(1,6)]])
add('1-4',orthfield('a',A),choice('b','Is the matrix orthogonal?','No: the third column has squared length 1/2 and the second and fourth columns are not perpendicular.',['Yes: its columns are orthonormal.','No: its first column has length zero.'],['The third column is '+math(r'(0,-\frac12,0,\frac12)^T')+', whose squared length is 1/2.','Also columns 2 and 4 have dot product '+math(r'\frac1{\sqrt3}')+'. Thus '+math('A^TA\\ne I')+'.']))
assert A5.T*A5==s.eye(3) and A5*A5.T==s.eye(3)
add('1-5',choice('a','Select the three equivalent verifications.','AᵀA=I; all column dot products form I; all row dot products form I.',['AᵀA=−I; all rows have length 1.','AᵀA=I; distinct rows have dot product 1.'],['Direct multiplication gives '+math('A^TA=I_3')+'.','The column squared lengths are 1 and their three distinct dot products are zero.','Likewise '+math('AA^T=I_3')+', verifying unit row lengths and pairwise perpendicular rows.']))
v=M([-2,3,5]);z=A5*v;assert z.dot(z)==v.dot(v)==38
add('1-7',cf('a','Find T_A(x).',z,['Multiply each row of A by '+math('(-2,3,5)^T')+'.']),cf('b','Find the common norm of x and T_A(x).',rt(38),['The original squared norm is '+math('4+9+25=38')+'.','The transformed squared norm also equals 38 by direct summation; equivalently '+math('x^TA^TAx=x^Tx')+'.']))
proof('1-11',math(r'a^2+b^2=\frac12'),math('a^2+b^2=1'),math('a=b'),['The two columns have dot product '+math('(a+b)(b-a)+(a-b)(b+a)=0')+'.','Each squared length is '+math('2(a^2+b^2)')+'.','They are unit vectors exactly when that expression equals 1.'])
proof('1-12','Every diagonal entry must be either +1 or −1.','Every diagonal entry must be +1.','Every diagonal entry must be any nonzero real number.', ['For a real diagonal matrix '+math('D=\\operatorname{diag}(d_i)')+', '+math('D^TD=\\operatorname{diag}(d_i^2)')+'.','It equals I precisely when every '+math('d_i^2=1')+'.'])
for id,angle,old,new in [('1-13',s.pi/3,M([-2,6]),M([5,2])),('1-15',s.pi/4,M([-1,2,5]),M([1,6,-3]))]:
 C=M([[s.cos(angle),-s.sin(angle)],[s.sin(angle),s.cos(angle)]])
 if len(old)==3:C=s.diag(C,1)
 add(id,cf('a','Find the coordinates in the rotated system.',s.simplify(C.T*old),['The columns of C are the rotated basis vectors expressed in the old system.','Convert old coordinates to new by '+math("x'=C^Tx")+'.']),cf('b','Find the coordinates in the original system.',s.simplify(C*new),['The reverse conversion uses '+math("x=Cx'")+'.','Multiply the given new-coordinate vector by the rotation matrix.']))
proof('1-18',math(r'\begin{bmatrix}\cos\theta&0&-\sin\theta\\0&1&0\\\sin\theta&0&\cos\theta\end{bmatrix}'),math(r'\begin{bmatrix}\cos\theta&0&\sin\theta\\0&1&0\\-\sin\theta&0&\cos\theta\end{bmatrix}'),math(r'\begin{bmatrix}\cos\theta&\sin\theta&0\\-\sin\theta&\cos\theta&0\\0&0&1\end{bmatrix}'),['Viewed from positive y toward the origin, the positive rotation about y sends e1 toward −e3.','The new basis vectors are '+math(r'(\cos\theta,0,-\sin\theta),(0,1,0),(\sin\theta,0,\cos\theta)')+'.','Dot the old-coordinate vector with each new basis vector; these basis vectors become the rows of the coordinate conversion matrix.'])
proof('1-26','The first column is (cos θ,sin θ); the second must be either (−sin θ,cos θ) or (sin θ,−cos θ).','The second column can be any unit vector regardless of the first.','Both columns must equal (cos θ,sin θ).',['A unit first column can be parametrized by cos θ,sin θ for a unique angle in [0,2π).','Its perpendicular line is spanned by (−sin θ,cos θ).','A unit vector on that line has precisely the two possible signs, yielding the two matrices in the source.'])
flush()
# 7.2 diagonalization
lam=s.symbols('lambda')
def charfield(label,A):
 es=A.eigenvals();pol=s.factor(A.charpoly(lam).as_expr());desc=math(tex(pol)+'=0')+'; '+', '.join('dim E('+str(k)+') = '+str(v) for k,v in sorted(es.items(),key=lambda a:float(a[0])))
 for k,m in es.items():assert len((A-k*s.eye(A.rows)).nullspace())==m
 return choice(label,'Select the characteristic equation and eigenspace dimensions.',desc,[math(tex(pol+1)+'=0')+'; every eigenspace is one-dimensional.',math(tex(pol-1)+'=0')+'; one eigenspace has dimension '+str(A.rows)+'.'],['Compute '+math(r'\det(\lambda I-A)='+tex(pol))+'.','The matrix is symmetric, so it has an orthonormal eigenbasis and each eigenspace dimension equals its eigenvalue multiplicity.'])
add('2-1',charfield('a',M([[1,2],[2,4]])))
add('2-4',charfield('a',M([[4,2,2],[2,4,2],[2,2,4]])),notice='The original exercise crop clipped the first row. The full PDF matrix is [[4,2,2],[2,4,2],[2,2,4]].')
def diagfield(label,A,P=None,quadratic=False):
 if P is None:
  cols=[]
  for ev,m,vs in A.eigenvects():
   us=s.GramSchmidt(vs,orthonormal=True);cols+=us
  P=M.hstack(*cols)
 D=s.simplify(P.H*A*P);assert s.simplify(P.H*P)==s.eye(P.cols) and s.simplify(A*P-P*D)==s.zeros(A.rows,P.cols)
 assert D.is_diagonal()
 ans=math(('x=Py,\quad ' if quadratic else '')+'P='+tex(P)+',\quad D='+tex(D))
 bad=D.copy() if isinstance(D,s.MutableDenseMatrix) else M(D);bad[0,0]+=1
 steps=['Solve each eigensystem '+math('(A-\\lambda I)v=0')+', then orthonormalize within any repeated eigenspace.','Use the unit eigenvectors as columns of P. The checks are '+math('P^*P=I')+' and '+math('AP=PD')+'.']
 if quadratic:steps+=['Substitute '+math('x=Py')+'; the quadratic form becomes '+math('y^TDy')+', with the diagonal entries of D as the squared-variable coefficients.']
 else:steps+=['Consequently '+math('P^{-1}AP=D')+'.']
 return choice(label,'Select '+('the orthogonal change and diagonal coefficient matrix.' if quadratic else 'an orthonormal diagonalizing matrix and its diagonal result.'),ans,[math('P='+tex(P)+',\quad D='+tex(bad)),math('P='+tex(P)+',\quad D='+tex(-D))],steps)
for id,A in [('2-7',M([[6,2*rt(3)],[2*rt(3),7]])),('2-8',M([[3,1],[1,3]])),('2-11',M([[2,-1,-1],[-1,2,-1],[-1,-1,2]])),('2-14',M([[3,1,0,0],[1,3,0,0],[0,0,0,0],[0,0,0,0]]))]:add(id,diagfield('a',A),notice=('The original crop clipped the first row. The full PDF matrix is [[2,-1,-1],[-1,2,-1],[-1,-1,2]].' if id=='2-11' else None))
proof('2-15',math(r'A=2u_1u_1^T+4u_2u_2^T,\quad u_1=\frac1{\sqrt2}(-1,1)^T,\quad u_2=\frac1{\sqrt2}(1,1)^T'),math(r'A=4u_1u_1^T+2u_2u_2^T,\quad u_1=\frac1{\sqrt2}(-1,1)^T,\quad u_2=\frac1{\sqrt2}(1,1)^T'),math(r'A=2I'),['The eigenvalues are 2 and 4 with the displayed unit eigenvectors.','Their outer products are the orthogonal projections onto the respective eigenspaces.','Multiplying the projections by their eigenvalues and adding gives '+math(r'\begin{bmatrix}3&1\\1&3\end{bmatrix}')+'.'])
P=M([[0,1,0],[1,0,1],[-1,0,1]]);D=s.diag(-1,3,7);A=P*D*P.inv();assert A==A.T
add('2-19',cf('a','Select the symmetric matrix with the stated eigenpairs.',A,['The three given eigenvectors are pairwise perpendicular and nonzero.','Place them in P and set '+math('D=\\operatorname{diag}(-1,3,7)')+'.','The matrix '+math('A=PDP^{-1}')+' is symmetric and satisfies all three eigenvalue equations.']))
proof('2-21','Yes, for a real diagonalizable matrix with real eigenvalues: orthonormalize each eigenspace to obtain an orthogonal diagonalization.','No: the condition can never imply symmetry.','Yes, because every diagonalizable matrix is symmetric.', ['Take an eigenbasis from diagonalizability.','Gram–Schmidt within each eigenspace preserves its eigenvalue; different eigenspaces remain perpendicular by hypothesis.','The resulting orthogonal P gives '+math('A=PDP^T')+' with real diagonal D, so '+math('A^T=A')+'. The section works over real vector spaces.'])
v=M([1,0,1]);A=s.eye(3)-v*v.T
add('2-28',choice('a','Why is I−vvᵀ orthogonally diagonalizable?','It is real symmetric, since (vvᵀ)ᵀ=vvᵀ.',['It is always orthogonal.','It is always invertible.'],['Transpose '+math('I-vv^T')+' to get the same matrix.','The spectral theorem applies to every real symmetric matrix.']),diagfield('b',A))
flush()
# 7.3 quadratic forms
Aform=M([[9,3,-4],[3,-1,R(1,2)],[-4,R(1,2),4]])
add('3-1',*[cf(chr(97+i),'Select the symmetric matrix A in xᵀAx.',A,['Put squared-variable coefficients on the diagonal.','Divide each mixed-term coefficient by 2 and place the result in both symmetric off-diagonal positions.']) for i,A in enumerate([s.diag(3,7),M([[4,-3],[-3,-9]]),Aform])])
proof('3-3',math('2x^2-6xy+5y^2'),math('2x^2-3xy+5y^2'),math('2x^2+6xy+5y^2'),['Multiply A by (x,y)ᵀ to obtain (2x−3y,−3x+5y)ᵀ.','Dot with (x,y); both off-diagonal entries contribute −3xy, so the mixed coefficient is −6.'])
add('3-5',diagfield('a',M([[2,-1],[-1,2]]),quadratic=True))
add('3-9',*[choice(chr(97+i),'Select A, K, f in '+math('x^TAx+Kx+f=0')+'.',math('A='+tex(A)+',\quad K='+tex(K)+',\quad f='+str(f)),[math('A='+tex(2*A)+',\quad K='+tex(K)+',\quad f='+str(f)),math('A='+tex(A)+',\quad K='+tex(-K)+',\quad f='+str(f))],['The symmetric A contains the quadratic coefficients, halving each cross coefficient.','The row K contains the linear coefficients and f is the constant.','Expanding these three terms reproduces the original equation.']) for i,(A,K,f) in enumerate([(M([[2,R(1,2)],[R(1,2),0]]),M([[1,-6]]),2),(s.diag(0,1),M([[7,-8]]),-5)])])
conics=['Ellipse','Hyperbola','Parabola','Circle']
add('3-11',*[choice(chr(97+i),'Identify this conic.',conics[i],[v for v in conics if v!=conics[i]][:2],[st]) for i,st in enumerate([math(r'\frac{x^2}{10}+\frac{y^2}{4}=1')+' has two unequal positive squared terms.',math(r'\frac{x^2}{8}-\frac{y^2}{8}=1')+' has opposite-sign squared terms.',math(r'y^2=\frac27x')+' is a parabola opening right.',math('x^2+y^2=25')+' is a circle centered at the origin with radius 5.'])])
P=M([[2,1],[-1,2]])/rt(5);A=M([[2,-2],[-2,-1]]);D=P.T*A*P;assert D==s.diag(3,-2) and P.det()==1
add('3-13',choice('a','Select a valid rotation, transformed equation, and conic classification.',math(r'\theta=-\arctan\frac12,\quad 3{x\prime}^2-2{y\prime}^2+8=0')+'; hyperbola.',[math(r'\theta=-\arctan\frac12,\quad 3{x\prime}^2+2{y\prime}^2+8=0')+'; ellipse.',math(r'\theta=0,\quad 2{x\prime}^2-{y\prime}^2+8=0')+'; hyperbola.'],['The quadratic matrix has eigenvalues 3 and −2.','Choose the proper rotation '+math('P='+tex(P))+'; its first column gives '+math(r'\cos\theta=\frac2{\sqrt5},\ \sin\theta=-\frac1{\sqrt5}')+'.','The check '+math('P^TAP=\\operatorname{diag}(3,-2)')+' removes the mixed term.','Standard form is '+math(r'\frac{{y\prime}^2}{4}-\frac{{x\prime}^2}{\frac83}=1')+', a hyperbola.']))
classes=['Positive definite','Negative definite','Indefinite','Positive semidefinite (not definite)','Negative semidefinite (not definite)']
add('3-17',*[choice(chr(97+i),'Classify the diagonal matrix.',classes[i],[v for v in classes if v!=classes[i]][:2],[st]) for i,st in enumerate(['Both eigenvalues 1 and 2 are positive.','Both eigenvalues −1 and −2 are negative.','The eigenvalues −1 and 2 have opposite signs.','The eigenvalues 1 and 0 are nonnegative, and the form vanishes on a nonzero vector.','The eigenvalues 0 and −2 are nonpositive, and the form vanishes on a nonzero vector.'])])
proof('3-21',classes[3],classes[0],classes[2],['A square is always nonnegative.','For the nonzero vector (1,1), the value is zero. Thus the form is semidefinite, not definite.'])
add('3-33',choice('a','Select the symmetric matrix of the sample variance (n>1).',math(r'A=\frac1{n-1}(I-\frac1n\mathbf1\mathbf1^T)'),[math(r'A=\frac1nI'),math(r'A=\frac1{n-1}(I+\frac1n\mathbf1\mathbf1^T)')],['Expand '+math(r'\sum_i(x_i-\bar x)^2=\sum_i x_i^2-n\bar x^2')+'.','Substitute '+math(r'\bar x=\frac1n\mathbf1^Tx')+' and divide by n−1.']),choice('b','Is the variance quadratic form positive definite?','No; it is positive semidefinite and vanishes on every constant vector.',['Yes; every nonzero data vector has positive variance.','No; it is indefinite.'],['A sum of squares divided by n−1 is nonnegative.','If all coordinates equal a nonzero constant, every deviation is zero, so definiteness fails.']))
proof('3-36',math(r'2b\cos2\theta+(c-a)\sin2\theta=0\iff\cot2\theta=\frac{a-c}{2b}'),math(r'\cot2\theta=\frac{a+c}{2b}'),math(r'\cot2\theta=\frac{2b}{a-c}'),['Substitute '+math(r'x=x\prime\cos\theta-y\prime\sin\theta,\ y=x\prime\sin\theta+y\prime\cos\theta')+'.','The mixed coefficient becomes '+math(r'2b(\cos^2\theta-\sin^2\theta)+2(c-a)\sin\theta\cos\theta')+'.','Set it to zero and use double-angle identities. Since b≠0, a solution cannot have sin2θ=0, so division gives the displayed cotangent.'])
flush()
# 7.4 extrema
for id,lo,hi,lopt,hipt,reason in [('4-1',-1,5,'(0,\\pm1)','(\\pm1,0)','The diagonal eigenvalues are 5 and −1.'),('4-3',3,7,'(\\pm1,0)','(0,\\pm1)','The diagonal eigenvalues are 3 and 7.'),('4-5',3,9,'(0,0,\\pm1)','(\\pm1,0,0)','The diagonal eigenvalues are 9,4,3.'),('4-6',0,3,r'\pm\frac1{\sqrt3}(1,-1,-1)',r'\pm\frac1{\sqrt6}(2,1,1)','The eigenvalues of '+math(r'\begin{bmatrix}2&1&1\\1&1&0\\1&0&1\end{bmatrix}')+' are 0,1,3.')]:
 add(id,choice('a','Select the minimum and every point attaining it.',math(str(lo))+', at '+math(lopt),[math(str(hi))+', at '+math(hipt),math(str(lo))+', at '+math(hipt)],[reason,'On the unit sphere the least eigenvalue is the minimum; its unit eigenvectors give all minimizing points.']),choice('b','Select the maximum and every point attaining it.',math(str(hi))+', at '+math(hipt),[math(str(lo))+', at '+math(lopt),math(str(hi))+', at '+math(lopt)],[reason,'The greatest eigenvalue is the maximum; its unit eigenvectors give all maximizing points.']))
A=M([[2,1,1],[1,1,0],[1,0,1]]);assert A*M([1,-1,-1])==s.zeros(3,1) and A*M([2,1,1])==3*M([2,1,1])
add('4-8',cf('a','Find the constrained minimum.',8,['Set '+math('u=x/4,\ v=\\sqrt3y/4')+' so '+math('u^2+v^2=1')+'.','The form becomes 16 times the quadratic form with matrix '+math(r'\begin{bmatrix}1&\frac1{2\sqrt3}\\\frac1{2\sqrt3}&\frac23\end{bmatrix}')+'.','Its eigenvalues are 1/2 and 7/6; multiply the smaller by 16.']),cf('b','Find the constrained maximum.',R(56,3),['The transformed unit-circle quadratic matrix has greatest eigenvalue 7/6.','Multiply by 16 to obtain the maximum.']))
add('4-9',choice('a','Select the level curves, tangent intersection points, and extrema.','Level 5: 5x²−y²=5 at (±1,0), maximum 5. Level −1: 5x²−y²=−1 at (0,±1), minimum −1.',['Level 5 touches at (0,±1), and level −1 touches at (±1,0).','Both extreme levels intersect the unit circle in four points.'],['On the circle substitute '+math('y^2=1-x^2')+' to get '+math('q=6x^2-1')+'.','At q=5 we must have x²=1,y=0, giving exactly two points. At q=−1 we must have x=0,y²=1, again two points.','These two hyperbolas are tangent to the circle at those points; all intermediate levels −1<q<5 meet it in four points.']),notice='The wording “each of these curves” is interpreted as the two extremal level curves; generic intermediate levels have four intersections, not two.')
add('4-13',choice('a','Select all critical points and classifications.','(0,0) is a saddle; (−1,1) is a relative maximum; there is no relative minimum.',['(0,0) is a minimum; (1,1) is a maximum.','(0,0) is a maximum; (−1,1) is a saddle.'],['The gradient equations are '+math('3x^2-3y=0,\ -3x-3y^2=0')+'.','Substitution y=x² gives '+math('x+x^4=x(1+x^3)=0')+', hence (0,0) and (−1,1).','The Hessian is '+math(r'\begin{bmatrix}6x&-3\\-3&-6y\end{bmatrix}')+'. Its determinant is −9 at the origin, a saddle; at (−1,1) it is 27 with first diagonal −6, a strict local maximum.']))
add('4-18',num('a','Find xᵀAx.',2,['Since Ax=2x, '+math('x^TAx=2x^Tx')+'.','The unit norm makes xᵀx=1, so the value is 2.']))
add('4-19',choice('a','Select the critical-point and Hessian facts.','Both gradients and both Hessians vanish at (0,0), so the second derivative test is inconclusive.',['Both Hessians are positive definite at (0,0).','Neither function has a critical point at (0,0).'],['The first derivatives are cubic and the second derivatives are quadratic.','They all vanish at the origin; both Hessian determinants are zero.']),choice('b','Select the classifications and valid reason.','f has a strict minimum because x⁴+y⁴>0 away from the origin; g has a saddle because it has opposite signs on the two coordinate axes.',['Both functions have strict minima because fourth powers are nonnegative.','Both functions have maxima because their Hessians vanish.'],['For f, the two fourth powers can sum to zero only at (0,0).','For g, values along y=0 are positive and values along x=0 are negative arbitrarily near the origin.']))
proof('4-21',math('q(x)=\\lambda'),math('q(x)=\\lambda^2'),math('q(x)=0'),['Use the eigenvector identity '+math('Ax=\\lambda x')+'.','Then '+math('x^TAx=\\lambda x^Tx=\\lambda')+' because x is a unit vector.'])
flush()
# 7.5 complex matrices
I=s.I
A=M([[2*I,1-I],[4,3+I],[5+I,0]])
add('5-1',cf('a','Find the conjugate transpose A*.',A.H,['Transpose the 3×2 matrix to a 2×3 matrix.','Conjugate each entry, changing the sign of every imaginary part.']))
A=M([[1,I,2-3*I],[-I,-3,1],[2+3*I,1,2]]);assert A.H==A
add('5-3',cf('a','Select the completed Hermitian matrix.',A,['Hermitian symmetry requires '+math(r'a_{ji}=\overline{a_{ij}}')+'.','The missing lower-triangle entries are −i, 2+3i, and 1.']))
add('5-5',choice('a','Why can no completion be Hermitian?',math(r'a_{31}=2-3i\ne\overline{a_{13}}=2+3i'),['A Hermitian matrix cannot contain any imaginary entries.','The diagonal entry −3 is not allowed in a Hermitian matrix.'],['Hermitian matrices must have conjugate entries across the diagonal.','The fixed (1,3) and (3,1) entries already violate that condition, independently of all blanks.']),choice('b','Why can no completion be Hermitian?','The fixed diagonal entry i is not real.',['The off-diagonal entries −i and i are inconsistent.','Hermitian matrices cannot have a zero entry.'],['A diagonal entry must equal its own conjugate.','Since '+math('i\\ne-i')+', the fixed middle diagonal entry cannot occur in a Hermitian matrix.']))
add('5-6',choice('a','Why can no completion be Hermitian?',math(r'a_{21}=1+i\ne\overline{a_{12}}=-i')+' (and the 1,3 pair also fails).',['The real diagonal entry 7 is forbidden.','The pair i and 1+i are complex conjugates.'],['The fixed (1,2),(2,1) entries are not conjugates.','Also '+math(r'a_{31}=6-2i\ne2+3i=\overline{a_{13}}')+'. Neither defect can be repaired by filling blanks.']),choice('b','Why can no completion be Hermitian?','The fixed diagonal entry 2+i is not real.',['The fixed pair 3+5i and 3−5i violates Hermitian symmetry.','The diagonal entry 3 must instead equal zero.'],['Every diagonal entry in a Hermitian matrix is real.','The imaginary part of the fixed bottom-right entry is 1, so no completion works.']))
A=M([[3,2-3*I],[2+3*I,-1]]);l1=1-rt(17);l2=1+rt(17);v1=M([2-3*I,l1-3]);v2=M([2-3*I,l2-3]);assert s.simplify(A*v1-l1*v1)==s.zeros(2,1) and s.simplify(A*v2-l2*v2)==s.zeros(2,1) and s.simplify((v1.H*v2)[0])==0
add('5-7',choice('a','Select the eigenvalues and orthogonal eigenvectors.',math(r'\lambda_\pm=1\pm\sqrt{17},\quad v_\pm=(2-3i,-2\pm\sqrt{17})^T'),[math(r'\lambda_\pm=1\pm\sqrt{13},\quad v_\pm=(2-3i,-2\pm\sqrt{13})^T'),math(r'\lambda_\pm=\pm4,\quad v_\pm=(1,\pm1)^T')],['The characteristic polynomial is '+math('\\lambda^2-2\\lambda-16')+', yielding real eigenvalues 1±√17.','Substitute each displayed vector into '+math('Av=\\lambda v')+'.','Their Hermitian inner product is '+math('(2+3i)(2-3i)+(-2-\\sqrt{17})(-2+\\sqrt{17})=13-13=0')+'.']))
A=M([[R(3,5),R(4,5)*I],[-R(4,5),R(3,5)*I]]);assert A.H*A==s.eye(2)
add('5-9',cf('a','Select the inverse of the unitary matrix.',A.H,['The two complex columns have squared norms 1 and Hermitian inner product zero.','Thus '+math('A^*A=I')+' and '+math('A^{-1}=A^*')+'.']))
add('5-13',diagfield('a',M([[4,1-I],[1+I,5]])))
A=M([[0,I,2-3*I],[I,0,1],[-2-3*I,-1,4*I]]);assert A.H==-A
add('5-19',cf('a','Select the completed skew-Hermitian matrix.',A,['Use '+math(r'a_{ji}=-\overline{a_{ij}}')+'.','The three missing entries are i, −2−3i, and −1.','All diagonal entries are zero or purely imaginary, and direct conjugate transpose gives '+math('A^*=-A')+'.']))
proof('5-33',math('|b|=|c|')+'; a is unrestricted.',math('b=c')+' and a must be real.',math('a=b=c'),['Compute '+math(r'AA^*=\operatorname{diag}(|a|^2,|c|^2,|b|^2)')+'.','Compute '+math(r'A^*A=\operatorname{diag}(|a|^2,|b|^2,|c|^2)')+'.','Equality holds exactly when the two last diagonal magnitudes agree.'])
proof('5-40',math(r'\lambda=-\overline\lambda')+'; hence Re(λ)=0.',math(r'\lambda=\overline\lambda')+'; hence λ is always real.',math(r'\lambda=1')+' always.', ['If '+math('Av=\\lambda v')+' with v nonzero, then '+math('v^*Av=\\lambda v^*v')+'.','Conjugating this scalar and using '+math('A^*=-A')+' gives '+math(r'\overline\lambda\,v^*v=-\lambda v^*v')+'.','The positive factor v*v cancels, proving that λ is zero or purely imaginary.'])
flush()
# Chapter 7 supplementary
sid=lambda i:f'anton-chapter-07-supplementary-{i}'
add(sid(1),orthfield('a',M([[3,-4],[4,3]])/5),orthfield('b',A5))
proof(sid(2),math(r'q_{ij}=\frac{C_{ij}}{\det Q}')+'; equal cofactors for det=1, negative cofactors for det=−1.',math(r'q_{ij}=C_{ji}')+' regardless of determinant.',math(r'q_{ij}=0')+' for every off-diagonal entry.', ['The inverse formula gives '+math(r'(Q^{-1})_{ji}=C_{ij}/\det Q')+'.','Orthogonality gives '+math('(Q^{-1})_{ji}=(Q^T)_{ji}=q_{ij}')+'.','An orthogonal determinant is ±1; substituting either sign proves the statement.'])
proof(sid(3),'Symmetry of A gives symmetry of uᵀAv; matrix multiplication gives bilinearity; positive definiteness gives positive self-products.','Positive definiteness alone gives bilinearity but never positivity.','The expression is an inner product only when A=I.', ['Transpose the scalar '+math('u^TAv')+' to obtain '+math('v^TA^Tu=v^TAu')+'.','Distributivity and scalar multiplication prove additivity and homogeneity.','For u≠0, '+math('u^TAu>0')+' by positive definiteness, while the value at zero is zero.'])
add(sid(4),charfield('a',M([[3,2,2],[2,3,2],[2,2,3]])))
add(sid(5),diagfield('a',M([[1,0,1],[0,1,0],[1,0,1]])))
add(sid(6),*[cf(chr(97+i),'Select the symmetric matrix A for xᵀAx.',A,['Squared-variable coefficients occupy the diagonal.','Each cross coefficient is twice the matching off-diagonal entry; halve it in each symmetric position.']) for i,A in enumerate([M([[-4,-R(15,2)],[-R(15,2),16]]),Aform])])
proof(sid(7),'Positive definite.','Positive semidefinite but not definite.','Indefinite.', ['The symmetric matrix is '+math(r'\begin{bmatrix}1&-\frac32\\-\frac32&4\end{bmatrix}')+'.','Its leading principal minors are 1 and '+math(r'4-\frac94=\frac74')+', both positive.','Sylvester’s criterion makes the form positive definite; equivalently '+math(r'(x_1-\frac32x_2)^2+\frac74x_2^2>0')+' for every nonzero vector.'])
add(sid(8),diagfield('a',M([[-3,1],[1,5]]),quadratic=True),diagfield('b',M([[-5,2,3],[2,1,0],[3,0,-1]]),quadratic=True))
add(sid(9),*[choice(chr(97+i),'Identify the conic.','Parabola',['Ellipse','Hyperbola'],[st]) for i,st in enumerate([math('y=x^2')+' is a parabola opening upward with vertex (0,0).',math(r'x=\frac{11}{3}y^2')+' is a parabola opening right with vertex (0,0).'])])
w=(-1+I*rt(3))/2;U=M([[1,1,1],[1,w,s.conjugate(w)],[1,w**2,s.conjugate(w)**2]])/rt(3);A=M([[1,1,0],[0,1,1],[1,0,1]]);D=s.diag(2,1+w,1+s.conjugate(w));assert s.simplify(U.H*U)==s.eye(3) and s.simplify(A*U-U*D)==s.zeros(3)
add(sid(10),choice('a','Select a unitary diagonalization (ω = (−1+i√3)/2).',math(r'U=\frac1{\sqrt3}\begin{bmatrix}1&1&1\\1&\omega&\overline\omega\\1&\omega^2&\overline\omega^2\end{bmatrix},\quad D=\operatorname{diag}(2,1+\omega,1+\overline\omega)'),[math(r'U=\frac1{\sqrt3}\begin{bmatrix}1&1&1\\1&\omega&\overline\omega\\1&\omega^2&\overline\omega^2\end{bmatrix},\quad D=\operatorname{diag}(1,\omega,\overline\omega)'),math(r'U=I,\quad D=\operatorname{diag}(2,1+\omega,1+\overline\omega)')],['Write A=I+C, where C cyclically permutes the coordinates.','For a cube root t of 1, '+math('C(1,t,t^2)^T=t(1,t,t^2)^T')+'.','The three vectors for t=1,ω,conjugate(ω) have squared norms 3 and are mutually orthogonal because '+math('1+\\omega+\\omega^2=0')+'.','Normalize by √3. Then '+math('U^*U=I')+' and '+math('AU=UD')+', proving the displayed result.']))
proof(sid(11),math(r'(UZ)^*(UZ)=Z^*U^*UZ=Z^*Z=I'),math(r'(UZ)^*(UZ)=Z^2')+' and is never I.',math(r'UZ=U')+' for all unit-modulus diagonal entries.', ['A diagonal Z with unit-modulus entries satisfies '+math(r'Z^*Z=\operatorname{diag}(|z_i|^2)=I')+'.','Use '+math('U^*U=I')+' and reverse factor order when taking the conjugate transpose.','The product therefore has conjugate transpose equal to its inverse and is unitary.'])
add(sid(12),choice('a','Select the equivalence proof.',math(r'(iA)^*=-iA^*=-iA\iff A^*=A'),[math(r'(iA)^*=iA^*')+' for every A.',math(r'iA')+' is skew-Hermitian for every complex A.'],['Conjugating i changes its sign, so '+math('(iA)^*=-iA^*')+'.','Setting this equal to −iA is equivalent to A*=A.']),choice('b','Why is a skew-Hermitian A unitarily diagonalizable with imaginary eigenvalues?','iA is Hermitian, so a unitary diagonalization of iA with real diagonal H gives A=U(−iH)U*.',['A is Hermitian and therefore has real eigenvalues.','A has to be the zero matrix.'],['From A*=−A, compute '+math('(iA)^*=-i(-A)=iA')+'.','Apply the Hermitian spectral theorem to iA.','Multiplying its real diagonal by −i gives the diagonal of A; every entry is purely imaginary, including zero.']))
u=M([1/rt(2),1/rt(6),1/rt(3)]);v=M([-1/rt(2),1/rt(6),1/rt(3)]);z=s.simplify(u.cross(v));assert z.dot(z)==1 and u.dot(z)==0 and v.dot(z)==0
add(sid(13),choice('a','Select all possible values of (a,b,c) and the uniqueness conclusion.',math(r'(a,b,c)=\pm(0,-\sqrt{\frac23},\frac1{\sqrt3})')+'; two choices, not unique.',[math(r'(a,b,c)=(1,0,0)')+' uniquely.',math(r'(a,b,c)=\pm(0,\frac1{\sqrt3},\sqrt{\frac23})')+'; two choices.'],['The fixed last two columns are orthogonal unit vectors.','Orthogonality of the first column to both gives '+math('a=0')+' and '+math(r'\frac b{\sqrt6}+\frac c{\sqrt3}=0')+', hence b=−√2c.','Unit length then gives '+math('3c^2=1')+'. There are exactly two opposite unit normal vectors.']))
# The printed exercise omits symmetry; explain the intended real symmetric setting explicitly.
answers=['Negative definite under the intended symmetric-matrix hypothesis.','Positive definite under the intended symmetric-matrix hypothesis.','Indefinite under the intended symmetric-matrix hypothesis.','Indefinite under the intended symmetric-matrix hypothesis.','Indefinite under the intended symmetric-matrix hypothesis.','Impossible for a real symmetric matrix: det(M1)=0 forces det(M2)≤0.']
reasons=[['The leading minors alternate −,+,−,+.','Sylvester’s negative-definiteness criterion applies to symmetric A.'],['All leading minors are strictly positive.','Sylvester’s criterion gives positive definiteness for symmetric A.'],['The leading 2×2 block has negative determinant.','A real symmetric 2×2 block with negative determinant has eigenvalues of opposite signs, so restricting the quadratic form already produces both signs.'],['The second leading determinant is negative.','The corresponding symmetric 2×2 restriction is indefinite; the full form is therefore indefinite.'],['Again the leading 2×2 determinant is negative.','That restriction takes both signs, even though the first and third leading determinants are zero.'],['The first condition says a11=0.','For a symmetric top-left block '+math(r'\begin{bmatrix}0&b\\b&d\end{bmatrix}')+', the determinant is '+math('-b^2\\le0')+'.','It cannot be strictly positive, so no symmetric matrix has the listed data.']]
add(sid(14),*[choice(chr(97+i),'Classify this sign pattern in the intended symmetric setting.',ans,[a for a in ['Positive definite under the intended symmetric-matrix hypothesis.','Negative definite under the intended symmetric-matrix hypothesis.','Indefinite under the intended symmetric-matrix hypothesis.'] if a!=ans][:2],reasons[i]) for i,ans in enumerate(answers)],notice='The printed question does not state that A is symmetric, which is required for the principal-minor definiteness criteria. These checks use that intended hypothesis explicitly. Under that hypothesis part (f) is inconsistent; it must not be classified as a realizable symmetric matrix.')
add(sid(15),choice('a','Select the symmetry and nonnegativity proof.',math(r'C^T=(QQ^T)^T=QQ^T,\quad x^TCx=\|Q^Tx\|^2\ge0'),[math(r'C^T=-C,\quad x^TCx\le0'),math(r'x^TCx>0')+' for all nonzero x and every rectangular Q.'],['Transpose the product to establish symmetry.','Regroup '+math('x^TQQ^Tx=(Q^Tx)^T(Q^Tx)')+' as a squared Euclidean norm.','It can vanish for nonzero x if Qᵀ has a kernel, so semidefinite is the general conclusion.']),choice('b','Why are all eigenvalues nonnegative?',math(r'\lambda=\frac{v^TCv}{v^Tv}=\frac{\|Q^Tv\|^2}{\|v\|^2}\ge0'),[math(r'\lambda=-\|Q^Tv\|^2<0'),math(r'\lambda=1')+' always.'],['For an eigenpair Cv=λv with v≠0, multiply by vᵀ.','Divide by the positive denominator vᵀv and apply the squared-norm identity from part (a).']))
for n,y,h in [(4,169,39.4),(11,372,39.84)]:
 qid=f'anton-section-7-2-{n}';original=next(q for q in json.load(open('tmp/linear-ch7-input.json')) if q['id']==qid)
 parts=original['parts'];parts[-1]['crops'][0][1]=y;parts[-1]['crops'][0][3]=h;OUT[qid]['sourceFigureParts']=parts
flush()
expected={q['id'] for q in json.load(open('tmp/linear-ch7-input.json'))};assert set(OUT)==expected,(expected-set(OUT),set(OUT)-expected)
print('Chapter 7:',len(OUT),'questions;',sum(len(q['fields']) for q in OUT.values()),'fields; all symbolic checks passed.')
# Nonunique diagonalization options keep P fixed while changing D. For a
# nonzero unit eigenvector, changing its eigenvalue breaks AP=PD; changing
# every diagonal sign also fails for these nonzero matrices. No sign-flipped
# or permuted valid eigenbasis is offered as an incorrect answer.
for A in [M([[6,2*rt(3)],[2*rt(3),7]]),M([[3,1],[1,3]]),M([[2,-1,-1],[-1,2,-1],[-1,-1,2]]),M([[3,1,0,0],[1,3,0,0],[0,0,0,0],[0,0,0,0]]),s.eye(3)-M([1,0,1])*M([[1,0,1]]),M([[2,-1],[-1,2]]),M([[4,1-I],[1+I,5]]),M([[1,0,1],[0,1,0],[1,0,1]]),M([[-3,1],[1,5]]),M([[-5,2,3],[2,1,0],[3,0,-1]])]:
 P=M.hstack(*[u for ev,m,vs in A.eigenvects() for u in s.GramSchmidt(vs,orthonormal=True)])
 D=s.simplify(P.H*A*P);bad=M(D);bad[0,0]+=1
 assert s.simplify(A*P-P*bad)!=s.zeros(A.rows)
 assert s.simplify(A*P+P*D)!=s.zeros(A.rows)
# Supplement 13 contains both legitimate signs in the correct choice.
u=M([1/rt(2),1/rt(6),1/rt(3)]);v=M([-1/rt(2),1/rt(6),1/rt(3)])
for wrong in [M([1,0,0]),M([0,1/rt(3),rt(R(2,3))])]:
 assert s.simplify(u.dot(wrong))!=0 or s.simplify(v.dot(wrong))!=0
print('Chapter 7 nonunique orthogonal / unitary diagonalization distractor audit passed.')
# Canonical source crop audit, including matrix rows wrongly attached to
# instruction blocks or to neighboring exercises in the original extraction.
import copy
_source7={q['id']:q for q in json.load(open('tmp/linear-ch7-input.json'))}
_repairs7={
 '2-1':[(1,[59,133.5,127.99,28.5])],
 '2-4':[(1,[186.99,169,130.01,39.4])],
 '2-11':[(1,[59,372,127.99,39.84])],
 '2-15':[(1,[59,491.69,127.99,27.31])],
 '2-19':[(0,[62,577.61,255,44.89]),(1,[59,623.8,258,39.2])],
 '5-3':[(0,[37,691.34,255,21.93]),(1,[34,713.5,127.91,37.95])],
 '5-5':[(0,[303,630.67,255,22.93]),(1,[300,660,258,91.45])],
 '5-6':[(0,[303,630.67,255,22.93]),(1,[59,50,258,81.78])],
 '5-19':[(0,[62,575.55,255,22.93]),(1,[59,602,118.28,38.6])],
}
for suffix,rects in _repairs7.items():
 qid='anton-section-7-'+suffix;parts=copy.deepcopy(_source7[qid]['parts'])
 for index,rect in rects:parts[index]['crops']=[rect]
 if suffix=='5-5':
  # Its final page-457 fragment is actually the first row of exercise 6(a).
  # That row is now included in 6(a)'s full problem crop, not duplicated here.
  parts=parts[:2]
 OUT[qid]['sourceFigureParts']=parts
q=OUT['anton-section-7-5-6'];f=q['fields'][0]
f['answer']=math(r'a_{21}=1+i\ne\overline{a_{12}}=1-i')
f['options']=[f['answer'],'The real diagonal entry 7 is forbidden.','The pair 1+i and 1+i are complex conjugates.']
f['workedSteps']=['The full source matrix has first row '+math(r'(1,1+i,\times)')+'.','Hermitian symmetry requires '+math(r'a_{21}=\overline{a_{12}}')+'.','The fixed pair is 1+i in both positions, but its conjugate is 1−i. Filling any blank cannot correct that mismatch.']
f['explanation']=f['workedSteps'][-1]
q['reviewNotice']='The original source assembly incorrectly attached the first row of Exercise 5(a) to the shared instructions and separated the first row of Exercise 6(a). The corrected full matrix for 6(a) is [[1,1+i,×],[1+i,7,×],[6−2i,×,0]].'
flush()
print('Chapter 7 canonical matrix-source crop repairs: 9 questions (including prior 7.2 #4/#11).')
