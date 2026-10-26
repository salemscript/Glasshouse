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
 OUT[id if id.startswith('anton') else 'anton-section-6-'+id]=q
def proof(id,answer,wrong1,wrong2,steps,label='a',prompt='Select the valid conclusion and reasoning.'):
 add(id,choice(label,prompt,answer,[wrong1,wrong2],steps))
def flush():Path('scripts/linear-answer-checks/ch06-reviewed.json').write_text(json.dumps({'chapter':6,'questions':OUT},indent=2,ensure_ascii=False)+'\n')
# 6.1: weighted and generated inner products.
u=M([1,1]);v=M([3,2]);w=M([0,-1]);A=M([[2,1],[1,1]])
for id,G in [('1-1',s.diag(2,3)),('1-3',A.T*A)]:
 ip=lambda a,b:(a.T*G*b)[0]
 vals=[ip(u,v),ip(3*v,w),ip(u+v,w),rt(ip(v,v)),rt(ip(u-v,u-v)),rt(ip(u-3*v,u-3*v))]
 prompts=[r'\langle u,v\rangle',r'\langle 3v,w\rangle',r'\langle u+v,w\rangle',r'\|v\|',r'd(u,v)',r'\|u-3v\|']
 add(id,*[cf(chr(97+i),'Find '+math(prompts[i])+'.',a,['Use '+math('\\langle a,b\\rangle=a^TG b')+' with '+math('G='+tex(G))+'.','Lengths are the square root of the self inner product.']) for i,a in enumerate(vals)])
add('1-9',num('a','Find the standard matrix inner product.',3,['Multiply corresponding entries and add: '+math('3(-1)+(-2)3+4(1)+8(1)=3')+'.']))
add('1-11',num('a','Find the standard polynomial inner product.',-29,['Use coefficient vectors '+math('(-2,1,3),(4,0,-7)')+'.',math('(-2)4+1(0)+3(-7)=-29')+'.']))
add('1-15',num('a','Find the evaluation inner product.',-50,['At the four nodes, the values of p are '+math('(-10,-2,0,2)')+' and of q are '+math('(5,2,1,2)')+'.','Their dot product is '+math('-50-4+0+4=-50')+'.']))
add('1-19',cf('a','Find the norm of p.',rt(14),['The coefficient norm squared is '+math('4+1+9=14')+'.']),cf('b','Find the distance between p and q.',rt(137),['Subtract coefficients: '+math('(-6,1,10)')+'.','The squared distance is '+math('36+1+100=137')+'.']))
add('1-27',num('a','Evaluate the inner product.',-101,['Expand bilinearly: '+math('6\\langle v,u\\rangle+4\\langle v,w\\rangle-3\\langle w,u\\rangle-2\\|w\\|^2')+'.',math('12-24+9-98=-101')+'.']),num('b','Find the norm of u+v.',3,['Use '+math('\\|u+v\\|^2=1^2+2(2)+2^2=9')+'.','Take the positive square root: 3.']))
proof('1-29',math(r'\frac{x^2}{4}+\frac{y^2}{16}=1')+'; ellipse with intercepts (±2,0), (0,±4).',math(r'\frac{x^2}{16}+\frac{y^2}{4}=1')+'; intercepts (±4,0), (0,±2).','The ordinary unit circle.', ['The unit circle means '+math('\\langle v,v\\rangle=1')+'.','Substitute the weights to get '+math(r'\frac{x^2}{4}+\frac{y^2}{16}=1')+'.','The horizontal and vertical semiaxes are 2 and 4.'])
proof('1-33','Additivity and scalar homogeneity fail; symmetry and positivity hold.','Only symmetry fails.','All inner product axioms hold.', ['Swapping u and v leaves every term unchanged, and '+math('\\langle u,u\\rangle=\\sum u_i^4')+' is positive for nonzero u.','With '+math('u=v=e_1')+', '+math('\\langle 2u,v\\rangle=4')+' while '+math('2\\langle u,v\\rangle=2')+'.','The same example violates additivity: '+math('\\langle u+u,v\\rangle=4\\ne2')+'.'])
add('1-37',*[cf(chr(97+i),p,a,[st]) for i,(p,a,st) in enumerate([('Find the inner product.',R(2,3),math(r'\int_{-1}^1x^2\,dx=\frac23')),('Find the distance.',rt(R(16,15)),math(r'\int_{-1}^1(1-x^2)^2\,dx=\frac{16}{15}')),('Find the norm of p.',rt(2),math(r'\int_{-1}^1 1\,dx=2')),('Find the norm of q.',rt(R(2,5)),math(r'\int_{-1}^1x^4\,dx=\frac25'))])])
flush()
# 6.2
for id,pairs in [('2-1',[([1,-3],[2,4]),([-1,5,2],[2,4,-9]),([1,0,1,0],[-3]*4)]),('2-3',[([-1,5,2],[2,4,-9])]),('2-5',[([2,6,1,-3],[3,2,1,0])])]:
 fs=[]
 for i,(a,b) in enumerate(pairs):
  a=M(a);b=M(b);c=s.simplify(a.dot(b)/(a.norm()*b.norm()))
  fs.append(cf(chr(97+i),'Find the cosine of the angle.',c,['Use the entry/coefficient dot product.',math(r'\cos\theta=\frac{\langle u,v\rangle}{\|u\|\|v\|}')+'; the numerator is '+math(a.dot(b))+' and squared norms are '+math(a.dot(a))+', '+math(b.dot(b))+'.']))
 add(id,*fs)
add('2-7',*[choice(chr(97+i),'Are these vectors orthogonal?',ans,['No' if ans=='Yes' else 'Yes'],[st,'Orthogonality is equivalent to a zero dot product.']) for i,(ans,st) in enumerate([('Yes',math('-4+6-2=0')),('No',math('-2-2-2=-6')),('Yes',math('-ab+ab=0'))])])
add('2-13',num('a','Find the ordinary dot product.',-1,[math('1(2)+3(-1)=-1')+'; it is nonzero.']),cf('b','Find the positive weight k giving orthogonality.',R(4,3),['The weighted product is '+math('2(1)(2)+k(3)(-1)=4-3k')+'.','Set it to zero and solve.']))
proof('2-17','No such scalars exist.','Yes: k = −10 and l = −19.','Yes: k = 0 and l = 0.', ['Orthogonality to p3 forces '+math('20+2k=0')+' and '+math('l+19=0')+', so k=−10 and l=−19.','Then '+math('\\langle p_1,p_2\\rangle=2l+5k+18=-70\\ne0')+'.'])
proof('2-21',math(r'1\le\sqrt{132}')+' verifies Cauchy–Schwarz.',math(r'13\le\sqrt{12}')+' verifies Cauchy–Schwarz.','The inequality fails.', ['The weighted inner product is '+math('2(1)(2)+3(0)(1)+3(-1)=1')+'.','Squared norms are '+math('11')+' and '+math('12')+'.','Thus '+math(r'|\langle u,v\rangle|=1\le\sqrt{11}\sqrt{12}')+'.'])
B=M([[1,4,5,2],[2,1,3,0],[-1,3,2,2]]);N=M.hstack(*B.nullspace());assert B*N==s.zeros(3,2)
add('2-27',cf('a','Select a matrix whose columns form a basis for the orthogonal complement.',N,['Solve '+math('Bx=0')+' with the given spanning vectors as rows.','Row reduction gives two independent free-variable solutions; multiplication by B gives zero for both.']))
add('2-29',choice('a','Select the equation of the orthogonal complement.',math('x+2y=0'),[math('y=2x'),math('2x+y=0')],['The line W is spanned by (1,2).','A vector (x,y) is perpendicular exactly when '+math('x+2y=0')+'.']),choice('b','Select parametric equations of the orthogonal complement.',math('(x,y,z)=(t,-2t,-3t)'),[math('(x,y,z)=(t,2t,3t)'),math('(x,y,z)=(t,-2t,0)')],['The plane normal is (1,−2,−3).','Its orthogonal complement is precisely the span of that normal.']))
proof('2-38',math(r'\langle w,k_1u_1+k_2u_2\rangle=0')+'; w is perpendicular to their entire span.',math(r'\langle w,k_1u_1+k_2u_2\rangle=k_1+k_2')+' always.','w is parallel to every linear combination.', ['By linearity '+math(r'\langle w,k_1u_1+k_2u_2\rangle=k_1\langle w,u_1\rangle+k_2\langle w,u_2\rangle=0')+'.','In three dimensions, w is normal to the plane spanned by independent u1,u2; if they are dependent the span is a line or zero subspace.'])
flush()
# 6.3
categories=['Orthogonal, but not orthonormal.','Orthonormal (and orthogonal).','Neither orthogonal nor orthonormal.']
add('3-1',*[choice(chr(97+i),'Classify this set.',categories[a],[v for v in categories if v!=categories[a]],[st]) for i,(a,st) in enumerate([(0,'The dot product is zero, but lengths are 1 and 2.'),(1,'The dot product is zero and both squared lengths are 1.'),(2,'The dot product is −1, so orthogonality fails.'),(0,'The zero vector is perpendicular to every vector, but has norm zero.')])])
add('3-7',choice('a','Select the verification and expansion.',math(r'V^TV=I,\quad u=-\frac{11}{5}v_1-\frac25v_2+2v_3'),[math(r'V^TV=I,\quad u=\frac{11}{5}v_1+\frac25v_2+2v_3'),math(r'V^TV=I,\quad u=-\frac{11}{5}v_1-\frac25v_2-2v_3')],['Each vector has norm 1, and all three pairwise dot products vanish.','Compute coordinates by dot products: '+math(r'u\cdot v_1=-\frac{11}{5},\ u\cdot v_2=-\frac25,\ u\cdot v_3=2')+'.','Three orthonormal vectors in R³ are a basis, so these coordinates give the claimed expansion.']))
for id,u,V in [('3-15',M([-1,6]),M([R(3,5),R(4,5)])),('3-19',M([4,2,1]),M([[1,2],[2,1],[-2,2]])/3)]:
 p=V*(V.T*V).inv()*V.T*u;r=u-p;assert V.T*r==s.zeros(V.cols,1)
 add(id,cf('a','Find the orthogonal projection.',p,['Use '+math(r'p=V(V^TV)^{-1}V^Tu')+'.']),cf('b','Find the perpendicular component.',r,['Subtract the projection from u.','The check '+math('V^T(u-p)=0')+' confirms perpendicularity to every spanning vector.']))
V=M([[1,1],[1,1],[1,-1],[1,-1]]);b=M([1,2,0,-2]);p=V*(V.T*V).inv()*V.T*b;assert V.T*(b-p)==s.zeros(2,1)
add('3-23',cf('a','Find the orthogonal projection of b.',p,['The two spanning vectors are orthogonal and each has squared norm 4.','The projection coefficients are '+math(r'\frac{b\cdot v_1}{4}=\frac14,\quad\frac{b\cdot v_2}{4}=\frac54')+'.']))
def gs(U,G):
 vs=[];qs=[]
 for u in U.columnspace():
  v=s.simplify(u-sum((q*(q.T*G*u)[0] for q in qs),s.zeros(U.rows,1)));vs.append(v);qs.append(s.simplify(v/rt((v.T*G*v)[0])))
 Q=M.hstack(*qs);assert s.simplify(Q.T*G*Q)==s.eye(Q.cols)
 return Q,vs
for id,U,G in [('3-27',M([[1,2],[-3,2]]),s.eye(2)),('3-29',M([[1,-1,1],[1,1,2],[1,0,1]]),s.eye(3)),('3-37',M([[1,1,1],[1,1,0],[1,0,0]]),s.diag(1,2,3))]:
 Q,vs=gs(U,G)
 st=['Subtract earlier orthogonal projections from each successive input vector.','Unnormalized orthogonal vectors are the columns of '+math(M.hstack(*vs))+'.','Normalize with '+math('\\|v\\|=\\sqrt{v^TGv}')+'; the check is '+math('Q^TGQ=I')+'.']
 fs=[cf('a','Select an orthonormal basis, given as matrix columns in input order.',Q,st)]
 if id=='3-27':fs.append(choice('b','Which description matches the basis-vector drawing?','Original arrows end at (1,−3),(2,2); new unit arrows point along (1,−3),(3,1), at right angles.',['Both new arrows remain parallel to the original two arrows.','The new unit arrows point along (1,3),(−3,1).'],['The first direction is preserved.','Removing the projection of (2,2) onto (1,−3) leaves a positive multiple of (3,1).']))
 add(id,*fs)
polys=[1,rt(3)*(2*x-1),rt(5)*(6*x*x-6*x+1)]
assert M(3,3,lambda i,j:s.integrate(polys[i]*polys[j],(x,0,1)))==s.eye(3)
add('3-43',choice('a','Select the ordered orthonormal polynomial basis.',math(r'\{1,\sqrt3(2x-1),\sqrt5(6x^2-6x+1)\}'),[math(r'\{1,\sqrt3x,\sqrt5x^2\}'),math(r'\{1,2x-1,6x^2-6x+1\}')],['The first vector is 1. Subtract '+math(r'\int_0^1x\,dx=\frac12')+' from x.','From x² subtract its projections onto 1 and the normalized linear polynomial, obtaining '+math(r'x^2-x+\frac16')+'.','Their squared norms before normalization are '+math(r'1,\frac1{12},\frac1{180}')+', yielding the displayed basis.']))
A=M([[1,0,1],[-1,1,1],[1,0,1],[-1,1,1]]);Q,Rm=A.QRdecomposition();assert Q*Rm==A and Q.T*Q==s.eye(2)
add('3-49',choice('a','Select a valid reduced QR decomposition.',math('Q='+tex(Q)+',\quad R='+tex(Rm)),[math('Q='+tex(-Q)+',\quad R='+tex(Rm)),math('Q='+tex(Q)+',\quad R='+tex(-Rm))],['The third column equals the first plus twice the second, so rank(A)=2.','Normalize the first column and orthogonalize the second to obtain the two columns of Q.','Compute '+math('R=Q^TA')+'. Direct multiplication verifies '+math('QR=A,\ Q^TQ=I_2')+'.']),notice='The source matrix has dependent columns. This check accepts a reduced rank-2 QR decomposition; a 3-column thin QR with all positive diagonal entries is impossible.')
flush()
# 6.4 least squares and projections
A=M([[1,-1],[2,3],[4,5]]);b=M([2,-1,5]);H=A.T*A;c=A.T*b;sol=H.inv()*c;r=b-A*sol;assert A.T*r==s.zeros(2,1)
add('4-1',choice('a','Select the normal equation.',math(tex(H)+r'\begin{bmatrix}x_1\\x_2\end{bmatrix}='+tex(c)),[math(tex(H)+r'\begin{bmatrix}x_1\\x_2\end{bmatrix}='+tex(-c)),math(tex(s.eye(2))+r'\begin{bmatrix}x_1\\x_2\end{bmatrix}='+tex(c))],['Multiply the system by '+math('A^T')+'.','Compute '+math('A^TA='+tex(H))+', '+math('A^Tb='+tex(c))+'.']))
add('4-3',cf('a','Find the least squares solution vector.',sol,['Solve '+math('A^TAx=A^Tb')+'.','The normal matrix is '+math(H)+' and the right-hand side is '+math(c)+'.']))
add('4-7',cf('a','Find the error vector b−Ax.',r,['Use the least squares solution '+math(sol)+'.','Subtract Ax from b. The verification '+math('A^Tr=0')+' proves orthogonality to the column space.']),cf('b','Find the least squares error (norm of the error vector).',r.norm(),['Square and sum the residual components, then take the square root.']),notice='Uses the convention error vector b−Ax; reversing that convention changes only the vector sign.')
A=M([[2,1],[4,2],[-2,-1]]);b=M([3,2,1]);p=A*A.pinv()*b;r=b-p;assert A.T*r==s.zeros(2,1)
add('4-11',choice('a','Select all least squares solutions.',math(r'x_1=t,\quad x_2=1-2t\quad(t\in\mathbb R)'),[math(r'x_1=t,\quad x_2=2-2t'),math(r'x_1=t,\quad x_2=1+2t')],['The first column is twice the second, so '+math('Ax=(2x_1+x_2)(1,2,-1)^T')+'.','Projection onto (1,2,−1) has coefficient '+math(r'\frac{3+4-1}{1+4+1}=1')+'.','Thus '+math('2x_1+x_2=1')+' is the complete condition.']),cf('b','Select the common error vector b−Ax.',r,['Every solution gives '+math('Ax=(1,2,-1)^T')+'.','Consequently b−Ax is independent of the free parameter.']))
A=M([[1,-1],[3,2],[-2,4]]);b=M([4,1,3]);H=A.T*A;P=A*H.inv()*A.T;p=P*b;assert A.T*(b-p)==s.zeros(2,1) and P*P==P
add('4-15',cf('a','Find the orthogonal projection onto the column space.',p,['Solve the normal equation to get '+math(H.inv()*A.T*b)+'.','Multiplying by A gives the projection.','Independently, '+math('P=A(A^TA)^{-1}A^T='+tex(P))+' gives the same '+math('Pb')+'.']))
for id,P in [('4-19',s.diag(1,0)),('4-21',s.diag(1,0,1))]:add(id,cf('a','Select the standard orthogonal projection matrix.',P,['Projection preserves the coordinates along the stated subspace and sets the perpendicular coordinate to zero.','This equals '+math('B(B^TB)^{-1}B^T')+' for the coordinate-axis basis columns B and agrees with the standard coordinate projection.']))
A=M([[3,1],[-4,1]]);b=M([3,2]);Q=M([[3,4],[-4,3]])/5;Rm=Q.T*A;sol=Rm.inv()*Q.T*b;assert A*sol==b
add('4-23',cf('a','Find the least squares solution.',sol,['Multiply by '+math('Q^T')+' to obtain '+math('Rx=Q^Tb='+tex(Q.T*b))+'.','Back-substitute through the upper triangular R. The residual is zero.']))
n=M([5,-3,1]);B=M([[3,1],[5,0],[0,-5]]);P=s.eye(3)-n*n.T/35;assert n.T*B==s.zeros(1,2) and P*B==B and P*P==P
add('4-25',cf('a','Select a basis for W, as matrix columns.',B,['Solve '+math('5x-3y+z=0')+' for two independent directions.','Both columns satisfy the plane equation and are independent.']),cf('b','Select the projection matrix onto W.',P,['Project away the normal component: '+math('P=I-\\frac{nn^T}{n^Tn}')+'.','Here '+math('n=(5,-3,1)^T')+' and '+math('n^Tn=35')+'.']))
proof('4-30','The exact solution satisfies the normal equations and is the unique least squares solution.','An exact solution need not minimize the residual.','The least squares solution is always zero.', ['If '+math('Ax_*=b')+', multiplying by '+math('A^T')+' gives '+math('A^TAx_*=A^Tb')+'.','Independent columns make '+math('A^TA')+' invertible, so the normal equation has only this solution.','Equivalently its residual norm is zero, the smallest possible value.'])
flush()
# 6.5 fitting
sets=[([(0,0),(1,2),(2,7)],1), ([(0,1),(2,0),(3,1),(3,2)],1), ([(2,0),(3,-10),(5,-48),(6,-76)],2), ([(1,-2),(0,-1),(1,0),(2,4)],2)]
for i,(pts,deg) in enumerate(sets,1):
 B=M([[s.Integer(t)**k for k in range(deg+1)] for t,y in pts]);y=M([y for t,y in pts]);c=(B.T*B).inv()*B.T*y;f=sum(c[k]*x**k for k in range(deg+1));r=y-B*c;assert B.T*r==s.zeros(deg+1,1)
 predictions=B*c
 add('5-'+str(i),cf('a','Select the least squares fitted curve y = …',f,['Use design columns '+math('1,x'+(',x^2' if deg==2 else ''))+' and solve '+math('B^TBc=B^Ty')+'.','The coefficient vector in ascending powers is '+math(c)+'.']),cf('b','Select the curve heights at the listed data x-values, in order (the graph check).',predictions,['Evaluate the fitted curve at each given x-value.','Comparing these heights with '+math(y)+' places the plotted data above or below the curve by residuals '+math(r)+'.','The residual is perpendicular to all design columns; this confirms the least squares fit.']))
for i,pts,transform in [(5,[(1,7),(3,3),(6,1)],lambda t:1/t),(6,[(3,R(3,2)),(7,R(5,2)),(10,3)],rt)]:
 B=M([[1,transform(s.Integer(t))] for t,y in pts]);y=M([y for t,y in pts]);c=s.simplify((B.T*B).inv()*B.T*y);assert s.simplify(B.T*(y-B*c))==s.zeros(2,1)
 f=c[0]+c[1]*(1/x if i==5 else rt(x))
 fs=[cf('a','Select the fitted curve y = …',f,['Set '+math('X='+(r'\frac1x' if i==5 else r'\sqrt{x}'))+' and fit '+math('y=a+bX')+'.','Solve the two normal equations. The coefficients are approximately '+math(c.evalf(7))+'.'])]
 if i==6:
  pred=(B*c).evalf(7)
  fs.append(cf('b','Select the fitted heights at x = 3,7,10 (graph comparison).',pred,['Evaluate the curve at the three data abscissae.','The data heights are 1.5, 2.5, 3; the fitted curve is increasing and passes close to all three.']))
 add('5-'+str(i),*fs)
proof('5-7','Independent exactly when at least two x-values differ.','Independent exactly when all x-values are equal.','Always independent for any nonempty sample.', ['A column relation is '+math('a+bx_i=0')+' for every i.','Two distinct x-values force b=0 by subtraction, then a=0.','If all x-values equal c, the second column is c times the first, so the columns are dependent.'])
proof('5-8','A vanishing column combination is a degree-at-most-m polynomial with m+1 distinct roots, so all coefficients vanish.','A polynomial of degree m can have arbitrarily many roots without being zero.','Having n>m alone suffices even when all nodes coincide.', ['A dependence relation gives '+math('p(x_i)=a_0+a_1x_i+\\cdots+a_mx_i^m=0')+' at every node.','A nonzero degree-at-most-m polynomial has at most m distinct roots.','The m+1 distinct nodes force p to be identically zero, which makes every coefficient zero.'])
proof('5-9','The distinct-node condition makes M full column rank, hence MᵀM positive definite and invertible.','MᵀM is invertible whenever M has any nonzero entry.','MᵀM is singular whenever n>m.', ['Exercise 8 gives independent columns.','For nonzero c, '+math('c^TM^TMc=\\|Mc\\|^2>0')+'.','Thus the kernel of '+math('M^TM')+' is zero, proving invertibility.'])
flush()
# 6.6 Fourier and continuous least squares
for id,fa,fn,steps in [('6-1',r'1+\pi-2\sin x-\sin2x',r'1+\pi-2\sum_{k=1}^n\frac{\sin kx}{k}',[r'a_0=2+2\pi',r'a_k=0,\quad b_k=-\frac2k']),('6-2',r'\frac{4\pi^2}{3}+4\cos x+\cos2x+\frac49\cos3x-4\pi\sin x-2\pi\sin2x-\frac{4\pi}{3}\sin3x',r'\frac{4\pi^2}{3}+\sum_{k=1}^n(\frac4{k^2}\cos kx-\frac{4\pi}{k}\sin kx)',[r'a_0=\frac{8\pi^2}{3}',r'a_k=\frac4{k^2},\quad b_k=-\frac{4\pi}{k}'])]:
 add(id,*[choice(chr(97+i),'Select the least squares trigonometric approximation ('+('specified finite order' if i==0 else 'order n')+').',math(ans),[math('-('+ans+')'),math('2('+ans+')')],['Use Fourier coefficients '+math(r'a_0=\frac1\pi\int_0^{2\pi}f,\ a_k=\frac1\pi\int_0^{2\pi}f\cos kx,\ b_k=\frac1\pi\int_0^{2\pi}f\sin kx')+'.','Integration by parts gives '+', '.join(math(st) for st in steps)+'.','Substitute in '+math(r'\frac{a_0}{2}+\sum(a_k\cos kx+b_k\sin kx)')+' and truncate at the requested order.']) for i,ans in enumerate([fa,fn])])
for id,f,bs,lo,hi in [('6-3',x,[1,s.exp(x)],0,1),('6-4',s.exp(x),[1,x],0,1),('6-5',s.sin(s.pi*x),[1,x,x*x],-1,1)]:
 G=M(len(bs),len(bs),lambda i,j:s.integrate(bs[i]*bs[j],(x,lo,hi)));h=M([s.integrate(f*b,(x,lo,hi)) for b in bs]);c=s.simplify(G.inv()*h);p=s.simplify(sum(c[i]*bs[i] for i in range(len(bs))));err=s.simplify(s.integrate(f*f,(x,lo,hi))-(c.T*h)[0]);assert s.simplify(G*c-h)==s.zeros(len(bs),1)
 add(id,cf('a','Select the least squares approximation.',p,['The continuous normal equation is '+math('Gc=h')+' with '+math('G='+tex(G))+' and '+math('h='+tex(h))+'.','Solve for the coefficients in the given basis: '+math(c)+'.']),cf('b','Find the mean square error using the textbook integral convention.',err,['The source defines this error as '+math(r'\int_a^b(f-p)^2\,dx')+' without dividing by interval length.','Orthogonal projection gives '+math(r'\|f-p\|^2=\|f\|^2-c^Th')+'.']))
proof('6-6',math(r'\{\frac1{\sqrt{2\pi}},\frac{\cos x}{\sqrt\pi},\ldots,\frac{\cos nx}{\sqrt\pi},\frac{\sin x}{\sqrt\pi},\ldots,\frac{\sin nx}{\sqrt\pi}\}'),math(r'\{1,\cos x,\ldots,\cos nx,\sin x,\ldots,\sin nx\}'),math(r'\{\frac1{\sqrt\pi},\frac{\cos x}{\sqrt{2\pi}},\ldots,\frac{\sin nx}{\sqrt{2\pi}}\}'), ['The constant, distinct cosine modes, and distinct sine modes are pairwise orthogonal on '+math('[0,2\\pi]')+'.','Their squared norms are '+math('2\\pi')+' for 1 and '+math('\\pi')+' for every sine/cosine mode.','All Gram–Schmidt subtraction terms vanish; divide each vector by its norm.'])
proof('6-7',math(r'a_0=2\pi,\quad a_k=0,\quad b_k=-\frac2k'),math(r'a_0=\pi,\quad a_k=0,\quad b_k=\frac2k'),math(r'a_0=0,\quad a_k=\frac2k,\quad b_k=0'), ['Here formulas (9a–c) concern f(x)=x.','The constant integral is '+math(r'\frac1\pi\int_0^{2\pi}x\,dx=2\pi')+'.','Integration by parts yields '+math(r'\int_0^{2\pi}x\cos kx\,dx=0')+' and '+math(r'\int_0^{2\pi}x\sin kx\,dx=-\frac{2\pi}{k}')+'.'])
for id,ans,steps in [('6-8',r'2\sum_{k=1}^{\infty}\frac{\sin kx}{k}',['The mean and every cosine coefficient vanish.','Integration by parts gives '+math(r'b_k=\frac2k')+'.']),('6-9',r'\frac12+\frac2\pi\sum_{j=0}^{\infty}\frac{\sin((2j+1)x)}{2j+1}',['Integrate only over (0,π), where f is 1.','The coefficients are '+math(r'a_0=1,\ a_k=0,\ b_k=\frac{1-(-1)^k}{\pi k}')+'.','At the jump and periodic endpoints the series converges to the midpoint 1/2.']),('6-10',r'\sin3x',['Orthogonality gives b3=1 and every other coefficient zero.','The function is already one Fourier basis mode.'])]:
 proof(id,math(ans),math('-('+ans+')'),math('2('+ans+')'),steps)
# Independent integral checks of Fourier coefficients.
for k in range(1,5):
 assert s.integrate((1+x)*s.cos(k*x),(x,0,2*s.pi))==0
 assert s.integrate((1+x)*s.sin(k*x),(x,0,2*s.pi))==-2*s.pi/k
 assert s.integrate(x*x*s.cos(k*x),(x,0,2*s.pi))==4*s.pi/k**2
 assert s.integrate(x*x*s.sin(k*x),(x,0,2*s.pi))==-4*s.pi**2/k
flush()
# Chapter supplementary exercises
sid=lambda i:f'anton-chapter-06-supplementary-{i}'
add(sid(1),cf('a','Select one vector satisfying the orthogonality and equal-angle conditions.',M([0,1,1,0]),['Perpendicularity to e1 and e4 forces first and fourth entries to zero.','Equal cosines with e2 and e3 require equal second and third entries; choose both 1.']),cf('b','Select one unit vector satisfying the cosine ratio.',M([0,2,1,0])/rt(5),['The middle coordinates must obey '+math('x_2=2x_3')+'.','Unit length requires '+math('5x_3^2=1')+'; choose the positive sign.']))
proof(sid(2),math(r'\langle u,Av\rangle=u^TAv=(A^Tu)^Tv=\langle A^Tu,v\rangle'),math(r'\langle u,Av\rangle=\langle Au,v\rangle')+' for every A.',math(r'\langle u,Av\rangle=0')+' for every A.', ['Write the Euclidean inner product as a row times a column.','The transpose identity '+math('(A^Tu)^T=u^TA')+' gives the equality.'])
add(sid(3),choice('a','Select the orthogonal complement of diagonal matrices.',math(r'\{\begin{bmatrix}0&a\\b&0\end{bmatrix}:a,b\in\mathbb R\}'),[math(r'\{\begin{bmatrix}a&0\\0&b\end{bmatrix}\}'),math(r'\{\begin{bmatrix}a&b\\b&a\end{bmatrix}\}')],['The entrywise inner product with diag(s,t) is '+math('u_{11}s+u_{22}t')+'.','Vanishing for all s,t forces the two diagonal entries to zero, with off-diagonal entries free.']),choice('b','Select the orthogonal complement of symmetric matrices.',math(r'\{\begin{bmatrix}0&a\\-a&0\end{bmatrix}:a\in\mathbb R\}'),[math(r'\{\begin{bmatrix}0&a\\a&0\end{bmatrix}\}'),math(r'\{\begin{bmatrix}a&0\\0&-a\end{bmatrix}\}')],['Testing the diagonal basis matrices forces zero diagonal entries.','Testing '+math(r'\begin{bmatrix}0&1\\1&0\end{bmatrix}')+' forces '+math('u_{12}+u_{21}=0')+'.']))
proof(sid(4),'Ax=0 exactly when x is perpendicular to every row of A.','Ax=0 exactly when x is perpendicular to every column of A.','Ax=0 implies only the first row is perpendicular to x.', ['The ith component of Ax is '+math(r'\sum_j a_{ij}x_j=r_i\cdot x')+'.','Thus every component is zero if and only if every row dot product is zero.'])
proof(sid(5),math(r'(\sum a_i)(\sum a_i^{-1})\ge n^2'),math(r'(\sum a_i)(\sum a_i^{-1})\le n^2'),'The inequality only holds when all a-values equal 1.', ['Choose '+math(r'u=(\sqrt{a_i})')+' and '+math(r'v=(\frac1{\sqrt{a_i}})')+'.','Their inner product is n, and squared norms are the two sums.','Cauchy–Schwarz squared gives the stated lower bound.'])
proof(sid(6),math(r'\|cx+y\|^2=c^2\|x\|^2+2c\langle x,y\rangle+\|y\|^2'),math(r'\|cx+y\|^2=c\|x\|^2+2\langle x,y\rangle+\|y\|^2'),math(r'\|cx+y\|^2=c^2\|x\|^2-2c\langle x,y\rangle+\|y\|^2'), ['Expand '+math(r'\langle cx+y,cx+y\rangle')+' in both slots.','The cross terms are '+math(r'c\langle x,y\rangle+c\langle y,x\rangle=2c\langle x,y\rangle')+'.','The diagonal terms are the two squared norms with factors c² and 1.'])
add(sid(7),choice('a','Select both unit vectors orthogonal to all three given vectors.',math(r'\pm\frac1{\sqrt2}(1,0,1)'),[math(r'\pm\frac1{\sqrt2}(1,1,0)'),math(r'\pm\frac1{\sqrt3}(1,1,1)')],['The equations '+math('x+y-z=0,-2x-y+2z=0,-x+z=0')+' give y=0,z=x.','Normalize (1,0,1); its norm is √2, and both signs satisfy the equations.']))
proof(sid(8),math(r'\langle u,v\rangle=\sum_{j=1}^n\frac{u_jv_j}{j}'),math(r'\langle u,v\rangle=\sum_{j=1}^n j u_jv_j'),math(r'\langle u,v\rangle=\sum_{j=1}^n u_jv_j'), ['Different listed vectors have disjoint coordinate supports, hence are orthogonal for any positive weights.','The jth squared norm is '+math('w_j(\\sqrt j)^2=jw_j')+'.','Requiring norm 1 forces '+math(r'w_j=\frac1j')+', a positive weight.'])
proof(sid(9),'No: orthogonality and both unit-length equations are inconsistent.','Yes: weights 1 and 1.','Yes: weights 2 and 3.', ['Let weights be a,b>0. Orthogonality requires '+math('3a-2b=0')+'.','The first unit norm then gives '+math('a+4b=7a=1')+', so a=1/7,b=3/14.','The second squared norm becomes '+math(r'9a+b=\frac32')+', not 1.'])
proof(sid(10),math(r'\|u-v\|^2=\|u\|^2+\|v\|^2-2\|u\|\|v\|\cos\theta'),math(r'\|u-v\|^2=\|u\|^2+\|v\|^2+2\|u\|\|v\|\cos\theta'),math(r'\|u-v\|^2=\|u\|^2-\|v\|^2'), ['Expand '+math(r'\langle u-v,u-v\rangle=\|u\|^2+\|v\|^2-2\langle u,v\rangle')+'.','Use '+math(r'\langle u,v\rangle=\|u\|\|v\|\cos\theta')+' for the nonzero sides defining the angle.'])
add(sid(11),choice('a','Select the cosine for each edge and the diagonal.',math(r'\cos\theta=\frac1{\sqrt n}'),[math(r'\cos\theta=\frac1n'),math(r'\cos\theta=\sqrt n')],['Their dot product is k².','Their lengths are |k| and |k|√n for k≠0; dividing gives 1/√n.']),cf('b','Find the limiting angle in radians.',s.pi/2,['As n increases without bound, the cosine tends to zero from above.','Continuity of arccos gives π/2; the angle approaches a right angle.']))
add(sid(12),choice('a','Select the identity proving the equivalence.',math(r'\langle u+v,u-v\rangle=\|u\|^2-\|v\|^2'),[math(r'\langle u+v,u-v\rangle=\|u\|^2+\|v\|^2'),math(r'\langle u+v,u-v\rangle=2\langle u,v\rangle')],['Expand bilinearly and cancel the equal mixed products.','The result vanishes exactly when the two nonnegative norms agree.']),choice('b','Select the plane-geometric interpretation.','A parallelogram has equal adjacent side lengths exactly when its diagonals are perpendicular.',['Every parallelogram has perpendicular diagonals.','Equal adjacent side lengths force parallel diagonals.'],['The vectors u,v form adjacent sides, while u+v and u−v represent the diagonal directions.','Thus the algebra describes perpendicular diagonals of a rhombus, including degenerate limits.']))
proof(sid(13),math(r'\sum_i\cos^2\alpha_i=\frac{\sum_i\langle u,v_i\rangle^2}{\|u\|^2}=1'),math(r'\sum_i\cos^2\alpha_i=n'),math(r'\sum_i\cos^2\alpha_i=\|u\|^2'), ['For nonzero u, '+math(r'\cos\alpha_i=\frac{\langle u,v_i\rangle}{\|u\|}')+'.','Expand u in the orthonormal basis; Pythagoras gives '+math(r'\|u\|^2=\sum_i\langle u,v_i\rangle^2')+'.','Divide by the nonzero squared norm. Angles are undefined when u=0.'])
proof(sid(14),'The sum preserves symmetry and linearity and is strictly positive on every nonzero vector.','The sum fails positivity unless the two products coincide.','The sum is an inner product only in dimension one.', ['Add the symmetry identities of the two products to prove symmetry.','Add their additivity and homogeneity identities to prove linearity.','For nonzero u, both self-products are positive, so their sum is positive; at zero both vanish.'])
proof(sid(15),math(r'(W^\perp)^\perp=W'),'The double orthogonal complement is always the zero subspace.','The double orthogonal complement is always all of V.', ['Every vector of W is perpendicular to every vector in '+math(r'W^\perp')+', giving inclusion in the double complement.','If dim(V)=n and dim(W)=d, then '+math(r'\dim(W^\perp)=n-d')+'.','The double complement has dimension d; inclusion between equal-dimensional subspaces is equality.'])
proof(sid(16),'The unique least squares solution is x=0.','Every x is a least squares solution.','The least squares solution must be nonzero.', ['Orthogonality to every column gives '+math('A^Tb=0')+'.','The normal equation is '+math('A^TAx=0')+'.','Independent columns make '+math('A^TA')+' invertible; hence x=0.'])
proof(sid(17),'No value of s works.','s=17.','s=93/5.', ['At x=(1,2), the residual b−Ax is '+math('(2,-7,s-14)^T')+'.','Orthogonality to the first column requires '+math('2-14+4(s-14)=0')+', hence s=17.','The second column instead requires '+math('-2-21+5(s-14)=0')+', hence s=93/5. They cannot both hold.'])
proof(sid(18),math(r'\int_0^{2\pi}\sin(px)\sin(qx)\,dx=0\quad(p\ne q)'),math(r'\int_0^{2\pi}\sin(px)\sin(qx)\,dx=\pi\quad(p\ne q)'),math(r'\int_0^{2\pi}\sin(px)\sin(qx)\,dx=2\pi\quad(p\ne q)'), ['Use '+math(r'2\sin px\sin qx=\cos((p-q)x)-\cos((p+q)x)')+'.','Both frequencies are nonzero integers, whose cosine integrals over [0,2π] vanish.'])
proof(sid(19),math(r'\int_0^{2\pi}\cos(px)\sin(qx)\,dx=0'),math(r'\int_0^{2\pi}\cos(px)\sin(qx)\,dx=\pi'),math(r'\int_0^{2\pi}\cos(px)\sin(qx)\,dx=2\pi'), ['Use '+math(r'2\cos px\sin qx=\sin((q+p)x)+\sin((q-p)x)')+'.','Each nonzero integer sine frequency integrates to zero over [0,2π]; if p=q the second term is identically zero.'])
proof(sid(20),math('x-z=0'),math('x+z=0'),math('y=0'), ['Subtracting the plane equations yields y=0; then z=−x.','The intersection is the span of (1,0,−1).','A vector is orthogonal to it precisely when its dot product with (1,0,−1) vanishes, giving x−z=0.'])
proof(sid(21),'The displayed Q,R satisfy QᵀQ=I and QR=A, but QR is not unique without a sign convention.','The displayed Q,R are unique among all orthogonal/upper-triangular factorizations.','The displayed Q,R never multiply to A.', ['Put '+math('r=\\sqrt{a^2+c^2}>0')+'. The two columns of Q have squared norm 1 and dot product zero.','Multiplication gives the first column (a,c) and second (b,d), using '+math('a(ab+cd)-c(ad-bc)=b(a^2+c^2)')+' and the analogous second-row identity.','If S=diag(−1,1), then '+math('A=(QS)(SR)')+' is a different orthogonal/upper-triangular factorization.','The displayed choice becomes unique after specifying det(Q)=1 and a positive first diagonal entry of R; the unrestricted uniqueness assertion is false.'])
OUT[sid(21)]['reviewNotice']='The source asserts uniqueness without a sign convention. The answer check identifies and corrects that omission while verifying the displayed factors.'
a,b,c,d=s.symbols('a b c d',real=True);T=M([[a,-c],[c,a]]);U=M([[a*a+c*c,a*b+c*d],[0,a*d-b*c]]);assert s.simplify(T*U-(a*a+c*c)*M([[a,b],[c,d]]))==s.zeros(2)
flush()
expected={q['id'] for q in json.load(open('tmp/linear-ch6-input.json'))};assert set(OUT)==expected,(expected-set(OUT),set(OUT)-expected)
print('Chapter 6:',len(OUT),'questions;',sum(len(q['fields']) for q in OUT.values()),'fields; all symbolic checks passed.')
# Audit nonunique-answer distractors: perturbations must violate the defining
# subspace/orthonormality conditions, rather than merely choose another basis.
def first_entry_perturbations(V):
 for delta in [1,-1]:
  Z=M(V);Z[0]+=delta;yield Z
B=M([[1,4,5,2],[2,1,3,0],[-1,3,2,2]])
N=M.hstack(*B.nullspace())
for Z in first_entry_perturbations(N):assert B*Z!=s.zeros(3,2)
for U,G in [(M([[1,2],[-3,2]]),s.eye(2)),(M([[1,-1,1],[1,1,2],[1,0,1]]),s.eye(3)),(M([[1,1,1],[1,1,0],[1,0,0]]),s.diag(1,2,3))]:
 Q,_=gs(U,G)
 for Z in first_entry_perturbations(Q):assert s.simplify(Z.T*G*Z)!=s.eye(Z.cols)
B=M([[3,1],[5,0],[0,-5]]);n=M([5,-3,1])
for Z in first_entry_perturbations(B):assert n.T*Z!=s.zeros(1,2)
A=M([[1,0,1],[-1,1,1],[1,0,1],[-1,1,1]]);Q,Rm=A.QRdecomposition()
assert (-Q)*Rm!=A and Q*(-Rm)!=A
# Parametric alternatives to 2*x1+x2=1 fail as entire families.
t=s.symbols('t',real=True)
assert s.expand(2*t+(2-2*t)-1)!=0
assert s.expand(2*t+(1+2*t)-1)!=0
# The candidate vector alternatives modify a coordinate required to be zero.
for V in [M([0,1,1,0]),M([0,2,1,0])/rt(5)]:
 for Z in first_entry_perturbations(V):assert Z[0]!=0
print('Chapter 6 nonunique basis / QR / parametric distractor audit passed.')
# Canonical source crops: keep shared prose separate from complete matrix rows,
# and remove the next exercise's detached first row from the bottom margin.
import copy
_source6={q['id']:q for q in json.load(open('tmp/linear-ch6-input.json'))}
for suffix,rects in {
 '4-3':[(0,[37,216.71,255,22.93]),(1,[34,244.5,258,39.5])],
 '4-7':[(2,[37,216.71,255,22.93]),(3,[34,244.5,258,39.5])],
 '4-11':[(0,[37,550.03,255,33.89]),(1,[34,584,258,39])],
 '4-15':[(0,[303,95.2,255,33.89]),(1,[300,129.3,258,39])],
}.items():
 qid='anton-section-6-'+suffix;parts=copy.deepcopy(_source6[qid]['parts'])
 for index,rect in rects:parts[index]['crops']=[rect]
 OUT[qid]['sourceFigureParts']=parts
flush()
print('Chapter 6 canonical matrix-source crop repairs: 4 questions.')
