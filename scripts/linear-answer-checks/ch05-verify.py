import sympy as s,json
from pathlib import Path
M=s.Matrix;R=s.Rational;I=s.I;out={}
def tex(x):return s.latex(x,mat_delim='',mat_str='bmatrix')
def w(x):return r'\('+str(x)+r'\)'
def choice(label,prompt,ans,steps,bad=None):
 if bad is None and ('y(t)=' in ans or ans.startswith(w('y=')[:-2])):
  bad=[ans.replace('=', '=e^{t}',1),ans.replace('=', '=e^{-t}',1)]
 if bad is None:
  import re
  matches=list(re.finditer(r'(?<![A-Za-z])(?<!\\)(-?\d+)',ans))
  match=next((m for m in matches if not re.search(r'(?:C|L|U|x)_\{?$',ans[:m.start()])),None)
  if match:
   old=match.group();n=int(old);a=ans[:match.start()]+str(n+1)+ans[match.end():];b=ans[:match.start()]+str(n-1)+ans[match.end():]
   bad=[a,b]
  elif '=' in ans:
   bad=[ans.replace('=',r'\ne ',1),ans.replace('=',r'=-',1)]
  else:
   bad=['Every nonzero vector satisfies the opposite conclusion.','The conclusion fails because similarity does not preserve eigenvalues.']
 return dict(label=label,selectionPrompt=prompt,type='choice',answer=ans,options=[ans]+bad,explanation=steps[-1],workedSteps=steps)
def num(label,prompt,ans,steps,tol=1e-8):return dict(label=label,selectionPrompt=prompt,type='numeric',answer=float(ans),tolerance=tol,explanation=steps[-1],workedSteps=steps)
def put(key,fields,notice=None):
 id='anton-'+('chapter-05-supplementary-'+key[1:] if key.startswith('s') else 'section-5-'+key)
 out[id]=dict(fields=fields,scope='All requested source parts, including bases, computations, and proof reasoning where requested.',complete=True,sourceImageReviewed=True)
 if notice:out[id]['reviewNotice']=notice

def eigfield(A,label='a',poly=True,real=False):
 ev=A.eigenvects();ans=[]
 for e,m,b in ev:
  for v in b:assert s.simplify(A*v-e*v)==s.zeros(A.rows,1)
  ans.append('E_{'+tex(e)+'}=\\operatorname{span}\\{'+','.join(tex(v) for v in b)+'\\}')
 p=s.factor(A.charpoly(s.Symbol('lambda')).as_expr());body=(tex(p)+'=0;\\quad ' if poly else '')+';\\quad '.join(ans)
 return choice(label,'Select the characteristic equation, eigenvalues, and eigenspace bases.' if poly else 'Select all eigenvalues and eigenspace bases.',w(body),['Form '+w('\\lambda I-A')+' and compute its determinant: '+w(tex(p))+'.','Set each factor to zero. For each eigenvalue, solve '+w('(A-\\lambda I)v=0')+'.','The resulting bases are '+w(';\\quad '.join(ans))+'. Each displayed vector satisfies '+w('Av=\\lambda v')+'.'])
def diagfield(A,label='a'):
 P,D=A.diagonalize();assert s.simplify(P*D*P.inv()-A)==s.zeros(A.rows)
 return choice(label,'Select a diagonalizing matrix and the resulting diagonal matrix.',w('P='+tex(P)+',\\quad P^{-1}AP='+tex(D)),['Use eigenvectors as columns of P, in the same order as eigenvalues in D.','The columns are independent: '+w('\\det P='+tex(P.det()))+'.',w('AP=PD')+' verifies the displayed diagonalization.'])
put('1-1',[num('a','Enter the eigenvalue corresponding to the supplied vector.',-1,[w(r'A\begin{bmatrix}1\\-1\end{bmatrix}=\begin{bmatrix}-1\\1\end{bmatrix}')+'.','The result is −1 times the original nonzero vector.'])])
put('1-5',[eigfield(M(a),chr(97+i)) for i,a in enumerate([[[1,4],[2,3]],[[-2,-7],[1,2]],[[1,0],[0,1]],[[1,-2],[0,1]]])])
for key,A in [('1-7',M([[4,0,1],[-2,1,0],[-2,0,1]])),('1-9',M([[6,3,-8],[0,-2,0],[1,0,-3]])),('1-15',M([[1,4],[2,3]])),('3-15',M([[4,-5],[1,0]]))]:put(key,[eigfield(A)],notice='The complete first matrix row was checked visually; stray neighboring matrix fragments are not part of this exercise.' if key in ['1-7','1-9'] else None)
put('1-13',[choice('a','Select the characteristic equation.',w('(\\lambda-3)(\\lambda-7)(\\lambda-1)=0'),['This matrix is triangular.','The determinant of '+w('\\lambda I-A')+' is the product of diagonal entries '+w('(\\lambda-3),(\\lambda-7),(\\lambda-1)')+'.'])])
geo=[('1-19',[('E_1=\\operatorname{span}\\{(1,1)\\}, E_{-1}=\\operatorname{span}\\{(1,-1)\\}','Reflection fixes its mirror line and reverses the perpendicular line.'),('E_1=\\operatorname{span}\\{(1,0)\\}, E_0=\\operatorname{span}\\{(0,1)\\}','Projection fixes the x-axis and kills the y-axis.'),(r'\text{No real eigenvalues or real eigenvectors}','A quarter-turn sends every nonzero vector to a perpendicular direction.'),('E_k=\\mathbb R^2','Every vector is multiplied by k.'),('E_1=\\operatorname{span}\\{(1,0)\\}','A nonzero horizontal shear fixes precisely the x-axis; any vector with nonzero y-coordinate changes direction.')]),('1-21',[('E_1=\\operatorname{span}\\{(1,0,0),(0,1,0)\\}, E_{-1}=\\operatorname{span}\\{(0,0,1)\\}','The xy-plane is fixed and the normal is reversed.'),('E_1=\\operatorname{span}\\{(1,0,0),(0,0,1)\\}, E_0=\\operatorname{span}\\{(0,1,0)\\}','The xz-plane is fixed and the y direction is killed.'),('E_1=\\operatorname{span}\\{(1,0,0)\\}','Only the rotation axis gives real eigenvectors; perpendicular vectors rotate through a quarter-turn.'),('E_k=\\mathbb R^3','Contraction scales every vector by k.')])]
for key,items in geo:put(key,[choice(chr(97+i),'Select all real eigenvalues and their eigenspaces.',w(ans),[why,'Hence '+w(ans)+'.']) for i,(ans,why) in enumerate(items)])
put('1-25',[num('a','Enter the matrix order n for its n by n size.',6,['The characteristic polynomial has degree '+w('1+2+3=6')+'.','Therefore A is 6 by 6.']),choice('b','Is A invertible?','Yes',['Zero is not a root of the characteristic polynomial.','Therefore zero is not an eigenvalue and A is invertible.'],['No']),num('c','Enter the number of distinct eigenspaces.',3,['The distinct eigenvalues are 1,3,4.','There is one eigenspace for each, giving 3.'])])
put('1-34',[choice('a','Select the calculation proving the shifted eigenpair.',w(r'(A-sI)x=Ax-sx=\lambda x-sx=(\lambda-s)x'),['Begin with the nonzero eigenvector satisfying '+w('Ax=\\lambda x')+'.','Subtract sx from both sides. The same nonzero x is an eigenvector with eigenvalue '+w('\\lambda-s')+'.'])])
put('2-1',[choice('a','Select a similarity invariant proving A and B are not similar.',w(r'\operatorname{tr}(A)=3\ne-1=\operatorname{tr}(B)'),['Compute the sums of diagonal entries: '+w('1+2=3')+' and '+w('1-2=-1')+'.','Similarity preserves trace, so unequal traces rule it out.'],['They are similar because their lower-left entries agree.','They are similar because they have the same size.'])])
put('2-5',[diagfield(M([[1,0],[6,-1]]))])
A=M([[4,0,1],[2,3,2],[1,0,4]]);ev=A.eigenvects()
put('2-9',[eigfield(A,'a',False),choice('b','Select the rank of lambda I minus A for each eigenvalue.',w('; '.join('\\lambda='+tex(e)+':\\operatorname{rank}='+str((e*s.eye(3)-A).rank()) for e,_,_ in ev)),['Compute nullities from the bases in part (a).','Rank equals 3 minus nullity, giving '+w('; '.join(tex(e)+':'+str((e*s.eye(3)-A).rank()) for e,_,_ in ev))+'.']),choice('c','Is A diagonalizable?','Yes',['Its eigenspace dimensions are '+str([len(b) for _,_,b in ev])+'.','They sum to 3, so an eigenvector basis exists.'],['No'])])
A=M([[-1,4,-2],[-3,4,0],[-3,1,3]]);ev=A.eigenvects()
put('2-11',[choice('a','Select algebraic and geometric multiplicities for each eigenvalue.',w('; '.join('\\lambda='+tex(e)+': (m_a,m_g)=('+str(m)+','+str(len(b))+')' for e,m,b in ev)),['Factor '+w('p(\\lambda)='+tex(s.factor(A.charpoly().as_expr())))+'.','Solve the corresponding null spaces; dimensions give geometric multiplicities.']),diagfield(A,'b')])
put('2-15',[choice('a','Select matrix size and possible eigenspace dimensions.',w(r'3\times3;\quad\dim E_1=\dim E_{-3}=\dim E_5=1'),['The polynomial has degree 3.','Each simple eigenvalue has geometric multiplicity 1.']),choice('b','Select matrix size and possible eigenspace dimensions.',w(r'6\times6;\quad\dim E_0\in\{1,2\},\dim E_1=1,\dim E_2\in\{1,2,3\}'),['The degrees sum to '+w('2+1+3=6')+'.','Geometric multiplicity is at least 1 and at most the corresponding algebraic multiplicity.'])])
A=M([[0,3],[2,-1]]);P,D=A.diagonalize();assert P*D**10*P.inv()==A**10
put('2-17',[choice('a','Select A to the tenth power.',w('A^{10}='+tex(A**10)),[w('P='+tex(P)+',D='+tex(D))+' gives '+w('A=PDP^{-1}')+'.',w('A^{10}=PD^{10}P^{-1}')+'.',w('A^{10}='+tex(A**10))])])
put('2-26',[choice('a','Can a matrix be similar to itself?','Yes',[w('I^{-1}AI=A')+' proves this for every square A.'],['No']),choice('b','Select the only matrix similar to the zero matrix.',w('0_{n\\times n}'),[w('P^{-1}0P=0')+' for every invertible P.','Therefore the similar matrix must itself be zero.']),choice('c','Can a nonsingular matrix be similar to a singular one?','No',['Similarity preserves determinant: '+w('\\det(P^{-1}AP)=\\det A')+'.','Zero and nonzero determinants cannot agree.'],['Yes'])])
put('2-27',[choice('a','Select all allowed eigenspace dimensions.',w(r'\dim E_1=1;\quad1\le\dim E_3\le2;\quad1\le\dim E_4\le3'),['Geometric multiplicity lies between 1 and algebraic multiplicity.','Apply this to multiplicities 1,2,3.']),choice('b','Select dimensions if A is diagonalizable.',w(r'\dim E_1=1,\dim E_3=2,\dim E_4=3'),['Diagonalizability requires equality of geometric and algebraic multiplicities.','The eigenspace dimensions must sum to 6.']),num('c','Enter the eigenvalue shared by three independent eigenvectors.',4,['Three independent vectors require geometric multiplicity at least 3.','Only eigenvalue 4 has algebraic multiplicity at least 3.'])])
put('2-30',[choice('a','Select the standard matrix and real diagonalizability conclusion.',w(r'A=\begin{bmatrix}2&-1\\1&1\end{bmatrix};\quad\text{not diagonalizable over }\mathbb R'),['Use the images of the coordinate vectors as columns.','The characteristic polynomial is '+w('\\lambda^2-3\\lambda+3')+' with discriminant −3.','There are no real eigenvalues, hence no real eigenvector basis. Over the complex numbers the two roots are distinct.'])])
put('2-37',[choice('a','Select the proof for positive integer powers.',w('A=PDP^{-1}\\Longrightarrow A^k=PD^kP^{-1}'),['Adjacent factors '+w('P^{-1}P')+' cancel when multiplying k copies of A.','Since '+w('D^k')+' remains diagonal, the same invertible P diagonalizes '+w('A^k')+'.'])])
u=M([2-I,4*I,1+I]);put('3-1',[choice('a','Select the conjugate, real part, imaginary part, and norm.',w(r'\bar u='+tex(s.conjugate(u))+',\\operatorname{Re}u='+tex(s.re(u))+',\\operatorname{Im}u='+tex(s.im(u))+',\\|u\\|='+tex(u.norm())),['Conjugation reverses each imaginary part.','The norm squared is '+w('5+16+2=23')+'.','Thus the norm is '+w(r'\sqrt{23}')+'.'])])
u=M([3-4*I,2+I,-6*I]);v=M([1+I,2-I,4]);k=I
forms=[(r'\overline{\bar u}',u),(r'\overline{ku}=\bar k\bar u',s.conjugate(k*u)),(r'\overline{u+v}=\bar u+\bar v',s.conjugate(u+v)),(r'\overline{u-v}=\bar u-\bar v',s.conjugate(u-v))]
put('3-3',[choice(chr(97+i),'Select the common value verifying the conjugation identity.',w(lhs+'='+tex(s.simplify(val))),['Conjugate each coordinate by replacing i with −i.','Both sides of '+w(lhs)+' evaluate to '+w(tex(s.simplify(val)))+'.']) for i,(lhs,val) in enumerate(forms)])
x=s.simplify((s.conjugate(u)+3*v)/I);assert s.simplify(I*x-3*v-s.conjugate(u))==s.zeros(3,1)
put('3-5',[choice('a','Select x solving i x minus 3v equals conjugate u.',w('x='+tex(x)),['Move 3v to the right: '+w(r'ix=\bar u+3v')+'.','Divide by i, equivalently multiply by −i.',w('x='+tex(x))])])
A=M([[-5*I,4],[2-I,1+5*I]]);B=M([1-I,2*I])
put('3-7',[choice('a','Select all five requested quantities.',w(r'\bar A='+tex(s.conjugate(A))+',\\operatorname{Re}A='+tex(s.re(A))+',\\operatorname{Im}A='+tex(s.im(A))+',\\det A='+tex(s.expand(A.det()))+',\\operatorname{tr}A='+tex(s.trace(A))),['Conjugate and take real/imaginary parts entrywise.','Use '+w('\\det A=a_{11}a_{22}-a_{12}a_{21}')+' and add diagonal entries for trace.','This gives '+w('\\det A=17-i,\\operatorname{tr}A=1')+'.'])])
put('3-9',[choice('a','Select the common value of double conjugation.',w(r'\overline{\bar A}='+tex(A)),['Each imaginary sign is reversed twice.','Therefore double conjugation returns A.']),choice('b','Select the common value of transpose-conjugation.',w(r'\overline{A^T}=\bar A^T='+tex(s.conjugate(A.T))),['Transpose exchanges indices; conjugation changes each scalar.','The two entrywise operations commute.']),choice('c','Select the common value of product-conjugation.',w(r'\overline{AB}=\bar A\bar B='+tex(s.simplify(s.conjugate(A*B)))),['Multiply A and B first, then conjugate.','Distributivity and conjugation of scalar products give the same value as multiplying the conjugated factors.'])])
u=M([I,2*I,3]);v=M([4,-2*I,1+I]);z=M([2-I,2*I,5+3*I]);k=2*I
dot=lambda a,b:s.expand((a.T*s.conjugate(b))[0]);uv=dot(u,v);uz=dot(u,z);vz=dot(v,z)
put('3-11',[choice('a','Select the three pairwise inner products.',w('u\\cdot v='+tex(uv)+',u\\cdot w='+tex(uz)+',v\\cdot w='+tex(vz)),['Conjugate the entries of the second vector before multiplying.',w(r'u\cdot v=u^T\bar v=\bar v^Tu')+'; the same coordinate calculation verifies Formula (5) for the other pairs.']),choice('b','Select the common values verifying antisymmetry, distributivity, and homogeneity.',w(r'u\cdot v=\overline{v\cdot u}='+tex(uv)+r';\quad u\cdot(v+w)='+tex(dot(u,v+z))+r';\quad(ku)\cdot v=k(u\cdot v)='+tex(dot(k*u,v))),['Reversing the inner product conjugates '+w(tex(uv))+'.','Add '+w(tex(uv))+' and '+w(tex(uz))+' to obtain '+w(tex(dot(u,v+z)))+'.','Multiplying the first vector by 2i multiplies the product by 2i, yielding '+w(tex(dot(k*u,v)))+'.'])])
put('3-19',[choice('a','Select the scale factor and rotation angle.',w(r'|\lambda|=\sqrt2,\quad\phi=\pi/4'),['The first column (1,1) has length '+w(r'\sqrt2')+' and angle '+w(r'\pi/4')+'.','Factoring out that length leaves the standard rotation matrix.'])])
A=M([[-1,-5],[4,7]]);P=M([[-1,-2],[0,2]]);C=P.inv()*A*P
# Construct real/imaginary eigenbasis automatically for canonical [[a,-b],[b,a]].
e=3+2*I;vv=(A-e*s.eye(2)).nullspace()[0];P=M.hstack(s.re(vv),-s.im(vv));C=s.simplify(P.inv()*A*P);assert P*C*P.inv()==A
put('3-23',[choice('a','Select an invertible P and real rotation-scaling block C.',w('P='+tex(P)+',\\quad C='+tex(C)),['The eigenvalues are '+w('3\\pm2i')+'.','Use the real and negative imaginary parts of an eigenvector for '+w('3+2i')+' as columns of P.',w('PCP^{-1}=A')+' verifies the result.'])])
put('3-33',[choice('a','Select the expansion that proves the polarization identity.',w(r'\|u+v\|^2-\|u-v\|^2=4\operatorname{Re}(u\cdot v),\quad\|u+iv\|^2-\|u-iv\|^2=4\operatorname{Im}(u\cdot v)'),['Expand each squared norm using the inner product, conjugating scalars in its second slot.','The diagonal terms cancel in each difference. The first difference isolates four times the real part; the second isolates four times the imaginary part.','Divide the first difference by 4 and add i times the second divided by 4 to recover '+w('u\\cdot v')+'.'])])
t=s.symbols('t',real=True);cs=s.symbols('C1:5')
def ode(key,A,initial=None):
 P,D=A.diagonalize();y=s.simplify(P*M([cs[i]*s.exp(D[i,i]*t) for i in range(A.rows)]));assert s.simplify(y.diff(t)-A*y)==s.zeros(A.rows,1)
 steps=['The eigenvector matrix and diagonal matrix are '+w('P='+tex(P)+',D='+tex(D))+'.','Put '+w('y=Pz')+' to obtain '+w('z_i^\\prime=\\lambda_i z_i')+'.','Integrating gives '+w('z_i=C_i e^{\\lambda_i t}')+' and '+w('y='+tex(y))+'.']
 fields=[choice('a','Select the general solution (arbitrary constants C).',w('y(t)='+tex(y)),steps)]
 if initial is not None:
  c=P.inv()*M(initial);yp=s.simplify(y.subs(dict(zip(cs,c))));assert yp.subs(t,0)==M(initial)
  fields.append(choice('b','Select the solution satisfying the initial conditions.',w('y(t)='+tex(yp)),['At t=0 solve '+w('Pc=y(0)')+'.','This gives '+w('c='+tex(c))+'.','Substitute into the general solution: '+w('y(t)='+tex(yp))+'.']))
 put(key,fields)
ode('4-1',M([[1,4],[2,3]]),[0,0]);ode('4-3',M([[4,0,1],[-2,1,0],[-2,0,1]]),[-1,1,0]);ode('4-4',M([[4,2,2],[2,4,2],[2,2,4]]));ode('s18',M([[1,3],[2,4]]),[5,6])
put('4-6',[choice('a','Select the component formula proving the claim.',w(r'y_i(t)=\sum_{j=1}^n p_{ij}C_j e^{\lambda_jt}'),['Write '+w('A=PDP^{-1}')+' and '+w('z=P^{-1}y')+'.','Then '+w('z^\\prime=Dz')+' so '+w('z_j=C_j e^{\\lambda_jt}')+'.','Multiplying by P gives the stated component formula.'])])
for key,roots,A in [('4-7',[-2,3],M([[0,1],[6,1]])),('4-8',[-4,3],M([[0,1],[12,-1]])),('4-9',[1,2,3],M([[0,1,0],[0,0,1],[6,-11,6]]))]:
 y=sum(cs[i]*s.exp(r*t) for i,r in enumerate(roots));vec=M([s.diff(y,t,i) for i in range(len(roots))]);assert s.simplify(vec.diff(t)-A*vec)==s.zeros(len(roots),1)
 put(key,[choice('a','Select the first-order system and full solution, including the original y.',w('Y^\\prime='+tex(A)+'Y,\\quad Y='+tex(vec)),['Set '+w('Y=(y,y^\\prime'+(',y^{\\prime\\prime}' if len(roots)==3 else '')+')^T')+'.','The companion matrix has characteristic roots '+w(','.join(map(str,roots)))+'.','Each root contributes an exponential; the first component gives '+w('y='+tex(y))+'.'])])
put('4-11',[choice('a','Select the necessary and sufficient conditions for every solution to tend to zero.',w(r'a_{11}+a_{22}<0,\quad a_{11}a_{22}-a_{12}a_{21}>0'),['All eigenvalues must have negative real parts.','For real eigenvalues, a positive product and negative sum make both negative. For a conjugate pair the real part is half the trace, and the determinant is positive.','Thus '+w('\\operatorname{tr}A<0,\\det A>0')+' exactly characterize asymptotic decay of every solution.'])])
a,b=s.symbols('C1 C2');cur=s.exp(-t)*(a*s.cos(t)+b*s.sin(t));volt=s.diff(cur,t);yp=M([cur,volt]);A=M([[0,1],[-2,-2]]);assert s.simplify(yp.diff(t)-A*yp)==s.zeros(2,1)
sol=s.simplify(yp.subs({a:2,b:3}));assert sol.subs(t,0)==M([2,1])
put('4-13',[choice('a','Select the general current-voltage solution.',w(r'\begin{bmatrix}i_L(t)\\v_C(t)\end{bmatrix}='+tex(yp)),['Substitute R=1, L=1, C=1/2 to obtain '+w('A='+tex(A))+'.','The characteristic equation '+w('\\lambda^2+2\\lambda+2=0')+' gives '+w('-1\\pm i')+'.','The inductor current is '+w(tex(cur))+' and voltage equals its derivative.']),choice('b','Select the solution for initial current 2 and voltage 1.',w(r'\begin{bmatrix}i_L(t)\\v_C(t)\end{bmatrix}='+tex(sol)),['Initial current gives '+w('C_1=2')+'.','Initial voltage is '+w('-C_1+C_2=1')+', hence '+w('C_2=3')+'.']),choice('c','Select the long-term behavior.','Both current and voltage tend to zero.',['Sine and cosine remain bounded.','The common factor '+w('e^{-t}')+' tends to zero, so both components decay.'],['Both oscillate with constant nonzero amplitude.','Both grow without bound.'])])
put('4-14',[choice('a','Select the linearity identity.',w(r'L(af+bg)=aL(f)+bL(g)'),['Differentiation is linear in each order.','Distribute the constants through '+w(r'(af+bg)^{\prime\prime}+2(af+bg)^\prime-3(af+bg)')+' to obtain the identity.']),choice('b','Select the general solution of L(y)=0.',w('y=C_1e^t+C_2e^{-3t}'),['With '+w('Y=(y,y^\\prime)^T')+', the matrix is '+w(r'\begin{bmatrix}0&1\\3&-2\end{bmatrix}')+'.','Its characteristic polynomial '+w('r^2+2r-3=(r-1)(r+3)')+' gives rates 1 and −3.'],[w('y=C_1e^t+C_2e^{3t}'),w('y=C_1e^{-t}+C_2e^{-3t}')])])
put('5-1',[choice('a','Is matrix (a) stochastic?','Yes',['All entries are nonnegative.','Each column sums to 1.'],['No']),choice('b','Select why matrix (b) is not stochastic.','Its column sums are 0.7 and 1.3.',['Column 1 sums to '+w('0.4+0.3=0.7')+'.','Column 2 sums to '+w('0.6+0.7=1.3')+'.'],['It has a negative entry.','It is stochastic because its rows sum to 1.']),choice('c','Is matrix (c) stochastic?','Yes',['All fractions are nonnegative.','Its column sums are 1, 1/2+1/2=1, and 1/3+1/3+1/3=1.'],['No']),choice('d','Select why matrix (d) is not stochastic.','It contains the negative entry −1/2.',['Each column does sum to 1.','The negative entry violates the nonnegativity requirement.'],['Its first column sums to 2.','It is stochastic because its columns sum to 1.'])])
P=M([[R(1,2),R(3,5)],[R(1,2),R(2,5)]]);x=M([R(1,2),R(1,2)]);seq=[]
for i in range(4):x=P*x;seq.append(x)
assert x==P**4*M([R(1,2),R(1,2)])
put('5-3',[choice('a','Select the fourth state vector obtained by both methods.',w('x_4='+tex(x)),['Successive multiplication '+w('x_{k+1}=Px_k')+' gives '+w(';'.join('x_'+str(i+1)+'='+tex(z) for i,z in enumerate(seq)))+'.','Directly compute '+w('P^4='+tex(P**4))+'.','Multiplying '+w('P^4x_0')+' gives the same '+w('x_4='+tex(x))+'.'])])
put('5-5',[choice('a','Is matrix (a) regular stochastic?','Yes',['Every entry is already positive, and each column sums to 1.','The first power itself proves regularity.'],['No']),choice('b','Is matrix (b) regular stochastic?','No',['The second state is absorbing.','The upper-right entry remains zero in every power, so no power is strictly positive.'],['Yes']),choice('c','Is matrix (c) regular stochastic?','Yes',[w(r'P^2=\begin{bmatrix}21/25&1/5\\4/25&4/5\end{bmatrix}')+'.','Every entry of the second power is positive.'],['No'])])
for key,P in [('5-7',M([[R(1,4),R(2,3)],[R(3,4),R(1,3)]])),('5-10',M([[R(1,3),R(1,4),R(2,5)],[0,R(3,4),R(2,5)],[R(2,3),0,R(1,5)]]))]:
 q=(P-s.eye(P.rows)).nullspace()[0];q=q/sum(q);assert P*q==q and sum(q)==1
 put(key,[choice('a','Select the regularity verification and steady-state vector.',w('P^2='+tex(P**2)+',\\quad q='+tex(q)),['The columns sum to 1, entries are nonnegative, and every entry of the displayed second power is positive.','Solve '+w('(P-I)q=0')+' together with '+w('\\sum q_i=1')+'.','The unique probability vector is '+w('q='+tex(q))+'.'])])
put('5-11',[choice('a','What does entry 0.2 represent?','The probability of state 1 next, given state 1 now.',['Columns are current states; rows are next states.','Entry (1,1) is the probability of remaining in state 1.'],['The probability of state 2 next, given state 1 now.','The probability of state 1 next, given state 2 now.']),choice('b','What does entry 0.1 represent?','The probability of state 1 next, given state 2 now.',['Entry (1,2) uses current state 2 and next state 1.','Thus the probability of a 2-to-1 transition is 0.1.'],['The probability of state 2 next, given state 1 now.','The probability of remaining in state 2.']),num('c','Enter the probability of state 2 next from initial state 1.',.8,['Read entry (2,1).','The probability is 0.8.']),num('d','Enter the probability of state 2 next from a 50–50 initial distribution.',.85,['Use total probability: '+w('0.8(0.5)+0.9(0.5)')+'.','The result is 0.85.'])])
P=M([[R(95,100),R(55,100)],[R(5,100),R(45,100)]])
put('5-13',[choice('a','Select the transition matrix in good,bad order.',w('P='+tex(P)),['A good day stays good with probability .95; a bad day becomes good with probability .55.','Place these probabilities in the good row, with complements below.']),num('b','Enter probability of good air two days after a good day.',(P**2)[0,0],['Use entry (good,good) of '+w('P^2')+'.',w('0.95^2+0.55(0.05)=0.93')]),num('c','Enter probability of bad air three days after a bad day.',(P**3)[1,1],['Use entry (bad,bad) of '+w('P^3')+'.','Matrix multiplication gives '+w(tex((P**3)[1,1]))+'.']),num('d','Enter probability of good air tomorrow.',(P*M([R(1,5),R(4,5)]))[0],['Use '+w('0.95(0.2)+0.55(0.8)')+'.','The result is 0.63.'])])
P=M([[R(95,100),R(3,100)],[R(5,100),R(97,100)]]);x=M([100000,25000]);table=[]
for yr in range(1,6):x=P*x;table.append((yr,round(x[0]),round(x[1])))
put('5-15',[choice('a','Select the five-year table (year, city, suburbs).',w(tex(M(table))),['Use '+w('P='+tex(P))+' and initial column '+w('(100000,25000)^T')+'.','Apply '+w('x_k=P^kx_0')+' without intermediate rounding, then round each annual count to the nearest integer.','The table is '+w(tex(M(table)))+'.']),choice('b','Select the long-term population (city, suburbs).',w('(46875,78125)'),['The equilibrium flow condition is '+w('0.05C=0.03S')+'.','Together with '+w('C+S=125000')+' this yields city fraction 3/8 and suburb fraction 5/8.','Thus populations approach 46875 and 78125.'])])
put('5-19',[choice('a','Select the full sequence and limit.',w('P^kq=q\\quad\\text{for every }k;\\quad\\lim P^kq=q'),['A steady-state vector satisfies '+w('Pq=q')+'.','Repeated multiplication preserves q exactly, so the sequence is constant.'])])
put('5-21',[choice('a','Select the column-sum calculation proving the product is stochastic.',w(r'\sum_i(AB)_{ij}=\sum_k(\sum_i a_{ik})b_{kj}=\sum_k b_{kj}=1'),['Every entry of AB is a sum of nonnegative products and is nonnegative.','Sum a product column, interchange the finite sums, and use each column sum of A, then B, equal to 1.','Thus AB satisfies both requirements for stochasticity.'])])
put('s1',[choice('a','Select the eigenvalues and real-eigenvalue conclusion.',w(r'\lambda=\cos\theta\pm i\sin\theta;\quad\text{no real eigenvalues}'),['The characteristic polynomial is '+w(r'\lambda^2-2\cos\theta\lambda+1')+'.','Its discriminant is '+w(r'-4\sin^2\theta<0')+' for '+w(r'0<\theta<\pi')+'.']),choice('b','Select the geometric explanation.','The rotation sends no nonzero vector to a parallel vector.', ['A real eigenvector would have to remain on its original line.','A rotation through an angle strictly between 0 and π sends every nonzero vector off that line.'],['Every nonzero vector is fixed.','A rotation always has a zero eigenvalue.'])])
k=s.symbols('k');A=M([[0,1,0],[0,0,1],[k**3,-3*k*k,3*k]])
put('s2',[choice('a','Select all eigenvalues with algebraic multiplicity.',w('\\lambda=k\\quad\\text{(multiplicity 3)}'),['Expand '+w('\\det(\\lambda I-A)')+'.','This gives '+w('(\\lambda-k)^3')+', so all three roots equal k.'])])
S=M([[1,1,0],[0,2,1],[0,0,3]]);A=M([[1,3,1],[0,4,5],[0,0,9]]);assert S*S==A
put('s3',[choice('a','Select a square root of nonnegative diagonal D.',w(r'S=\operatorname{diag}(\sqrt{d_1},\ldots,\sqrt{d_n})'),['Squaring a diagonal matrix squares its diagonal entries.','All square roots are real because every '+w('d_i\\ge0')+'.']),choice('b','Select a square root of diagonalizable A with nonnegative eigenvalues.',w(r'S=P\operatorname{diag}(\sqrt{\lambda_1},\ldots,\sqrt{\lambda_n})P^{-1}'),['Write '+w('A=PDP^{-1}')+'.','In '+w('S^2')+' the middle '+w('P^{-1}P')+' cancels, leaving '+w('PDP^{-1}=A')+'.']),choice('c','Select one square root of the supplied matrix.',w('S='+tex(S)),['Choose diagonal entries 1,2,3.','The (1,2) and (2,3) entries of the square require '+w('3s_{12}=3,5s_{23}=5')+'.','The (1,3) entry requires '+w('4s_{13}+s_{12}s_{23}=1')+', hence '+w('s_{13}=0')+'.',w('S^2='+tex(S*S))])])
put('s4',[choice('a','Are the transposes similar? Select the identity when B=P inverse A P.',w(r'B^T=P^TA^T(P^T)^{-1}'),['Transpose reverses the order of factors.','The displayed expression is a similarity transformation.']),choice('b','Are the kth powers similar? Select the identity.',w('B^k=P^{-1}A^kP'),['Cancel neighboring '+w('PP^{-1}')+' pairs in the product of k copies.','The same P gives the similarity of powers.']),choice('c','Are the inverses similar when A is invertible? Select the identity.',w('B^{-1}=P^{-1}A^{-1}P'),['Invert the product '+w('P^{-1}AP')+' in reverse factor order.','The resulting identity proves similarity.'])])
put('s5',[choice('a','Select the coefficient of lambda to n−1 and its determinant argument.',w(r'-\operatorname{tr}(A)=-\sum_i a_{ii}'),['In the determinant expansion, a term with n−1 factors of lambda can only come from the identity permutation.','Choose one diagonal term '+w('-a_{ii}')+' and lambda from the other n−1 diagonal entries.','Summing these contributions gives minus the trace. Other permutations move at least two indices and have degree at most n−2.'])])
put('s6',[choice('a','Select the eigenspace calculation ruling out diagonalization.',w(r'p(\lambda)=(\lambda-a)^2,\quad E_a=\operatorname{span}\{(1,0)^T\}'),['The only eigenvalue is a with algebraic multiplicity 2.','The eigenvector equation gives '+w('by=0')+'. Since b is nonzero, y=0.','The eigenspace has dimension 1, so there are not two independent eigenvectors.'])])
A2=M([[3,6],[1,2]]);A3=M([[0,1,0],[0,0,1],[1,-3,3]])
put('s7',[choice('a','Select the verified Cayley–Hamilton identity.',w('p(\\lambda)=\\lambda^2-5\\lambda;\\quad A^2-5A=0'),[w('A^2='+tex(A2**2))+'.',w('5A='+tex(5*A2))+' is the same matrix, so subtraction gives zero.']),choice('b','Select the verified Cayley–Hamilton identity.',w('p(\\lambda)=(\\lambda-1)^3;\\quad A^3-3A^2+3A-I=0'),[w('A^2='+tex(A3**2))+' and '+w('A^3='+tex(A3**3))+'.','Substituting these powers into '+w('A^3-3A^2+3A-I')+' produces the zero matrix.'])])
assert A2**2-5*A2==s.zeros(2) and A3**3-3*A3**2+3*A3-s.eye(3)==s.zeros(3)
put('s8',[choice('a','Select the 2 by 2 Cayley–Hamilton calculation.',w(r'A^2-(a+d)A+(ad-bc)I=0\quad\text{for }A=\begin{bmatrix}a&b\\c&d\end{bmatrix}'),['The characteristic polynomial is '+w('\\lambda^2-(a+d)\\lambda+ad-bc')+'.','Multiply A by itself. Each diagonal entry cancels after subtracting (a+d)A and adding (ad−bc)I; the off-diagonal entries cancel as well.']),choice('b','Select the diagonalizable-matrix proof.',w(r'p(A)=Pp(D)P^{-1}=P\operatorname{diag}(p(\lambda_1),\ldots,p(\lambda_n))P^{-1}=0'),['For '+w('A=PDP^{-1}')+', every power satisfies '+w('A^k=PD^kP^{-1}')+'.','Apply this to every term of p. Each diagonal entry '+w('p(\\lambda_i)')+' is zero because each eigenvalue is a root.'])])
for key,A,powers in [('s9',A2,range(2,6)),('s10',A3,[3,4])]:put(key,[choice(str(n),'Select '+w('A^{'+str(n)+'}')+'.',w('A^{'+str(n)+'}='+tex(A**n)),['Use '+w('A^2=5A' if A.rows==2 else 'A^3=3A^2-3A+I')+' from Cayley–Hamilton.','Multiply the recurrence by further powers of A and simplify.',w('A^{'+str(n)+'}='+tex(A**n))]) for n in powers])
put('s11',[choice('a','Select the eigenvalues counted with algebraic multiplicity.',w(r'c_1+\cdots+c_n,\quad0\text{ repeated }n-1\text{ times}'),['Write '+w('A=\\mathbf1 c^T')+'.','Then '+w('A\\mathbf1=(\\sum c_i)\\mathbf1')+' and every vector in '+w('\\ker c^T')+' maps to zero.','The characteristic polynomial is '+w(r'\lambda^{n-1}(\lambda-\sum c_i)')+'. If the sum is zero, all eigenvalues are zero.'])])
C=M([[0,0,0,-1],[1,0,0,2],[0,1,0,-1],[0,0,1,-3]])
put('s12',[choice('a','Select the determinant recurrence proving the companion polynomial.',w(r'D_n(\lambda)=\lambda D_{n-1}(\lambda)+c_0,\quad D_{n-1}=\lambda^{n-1}+c_{n-1}\lambda^{n-2}+\cdots+c_1'),['In '+w('\\lambda I-C')+', expand along the first row, whose only nonzero entries are lambda and c₀.','The first minor is the companion determinant with coefficients c₁ through cₙ₋₁. The signed c₀ minor equals c₀.','Induction therefore yields '+w(r'D_n=\lambda^n+c_{n-1}\lambda^{n-1}+\cdots+c_0')+'.']),choice('b','Select a matrix with the requested characteristic polynomial.',w('C='+tex(C)),['Put minus the coefficients 1,−2,1,3 in the last column and ones on the subdiagonal.','Direct computation gives '+w('\\det(\\lambda I-C)='+tex(C.charpoly().as_expr()))+'.'])])
put('s13',[choice('a','Select the possible eigenvalues of a nilpotent matrix.',w('\\lambda=0\\text{ only}'),['For an eigenvector v, '+w('A^nv=\\lambda^nv')+'.','Nilpotence gives zero on the left. Since v is nonzero, '+w('\\lambda^n=0')+', hence '+w('\\lambda=0')+'.'])])
put('s14',[choice('a','Select the argument guaranteeing a real eigenvalue.', 'The real characteristic polynomial has odd degree and therefore a real root.', ['A real matrix has a real monic characteristic polynomial of degree n.','When n is odd its values tend to opposite infinities at opposite ends of the real line.','Continuity gives a real zero, which is a real eigenvalue.'],['Every real matrix has only real eigenvalues.','Every odd-order matrix has determinant zero.'])])
P=M([[0,1,0],[1,-1,1],[-1,1,1]]);D=s.diag(0,1,-1);A=P*D*P.inv();assert A*P==P*D
put('s15',[choice('a','Select the matrix with the given ordered eigenpairs.',w('A='+tex(A)),['Place the given eigenvectors in columns: '+w('P='+tex(P))+'.','Their eigenvalues form '+w('D='+tex(D))+'.','Compute '+w('A=PDP^{-1}='+tex(A))+'. The identity '+w('AP=PD')+' verifies all three pairs.'])])
put('s16',[num('a','Enter the determinant.',18,['Multiply the four eigenvalues: '+w('1(-2)(3)(-3)=18')+'.','This also equals the constant coefficient of the degree-four characteristic polynomial.']),num('b','Enter the trace.',-1,['Add the four eigenvalues: '+w('1-2+3-3=-1')+'.','The trace is −1.'])])
put('s17',[choice('a','Select all possible eigenvalues.',w('\\lambda\\in\\{-1,0,1\\}'),['Apply '+w('A^3=A')+' to a nonzero eigenvector.','This gives '+w('(\\lambda^3-\\lambda)v=0')+', so '+w('\\lambda(\\lambda-1)(\\lambda+1)=0')+'.'])])
put('s19',[choice('a','Select the two remaining eigenvalues.',w('2,3'),['Let the remaining values be x,y. The sum condition gives '+w('x+y=5')+' and the product condition gives '+w('xy=6')+'.','Thus both are roots of '+w('t^2-5t+6=(t-2)(t-3)')+'.'])])
z=-R(1,2)+s.sqrt(3)*I/2;ds=[z,s.conjugate(z),s.Integer(1)];P=M.hstack(*[M([1,d,s.expand(d*d)]) for d in ds]);A=M([[0,1,0],[0,0,1],[1,0,0]]);D=s.diag(*ds);assert s.simplify(A*P-P*D)==s.zeros(3)
put('s20',[choice('a','Select the eigenvector matrix proving similarity.',w(r'P=\begin{bmatrix}1&1&1\\d_1&d_2&d_3\\d_1^2&d_2^2&d_3^2\end{bmatrix},\quad P^{-1}AP=D'),['Each d is a cube root of unity, so '+w('A(1,d,d^2)^T=(d,d^2,1)^T=d(1,d,d^2)^T')+'.','The three roots are distinct, so the Vandermonde matrix P is invertible.','Therefore '+w('AP=PD')+' implies the required similarity.'])])
out['anton-section-5-4-1']['fields'][1]['options']=[out['anton-section-5-4-1']['fields'][1]['answer'],w(r'y(t)=\begin{bmatrix}1\\0\end{bmatrix}'),w(r'y(t)=\begin{bmatrix}0\\1\end{bmatrix}')]
circuit=out['anton-section-5-4-13']['fields'][0]
circuit['options']=[circuit['answer'],circuit['answer'].replace('=','=e^{t}',1),circuit['answer'].replace('=','=e^{-t}',1)]
complex_field=out['anton-section-5-1-5']['fields'][1]
complex_field['selectionPrompt']='Select the characteristic equation and eigenvalue conclusion; complex eigenspaces are supplied as an extension.'
complex_field['answer']='No real eigenvalues or real eigenspaces; over the complex numbers: '+complex_field['answer']
complex_field['options']=['No real eigenvalues or real eigenspaces; over the complex numbers: '+x for x in complex_field['options']]
complex_field['workedSteps'].append('The characteristic polynomial is lambda squared plus 3, so it has no real roots. Thus there are no real eigenvalues or real eigenvectors; the displayed complex eigenpairs extend the answer to the complex field.')
repairs={'1-7': [59, 394, 127.45, 38], '1-9': [59, 432, 127.45, 38], '2-11': [325, 513, 125.96, 39]}
for src in json.load(open('tmp/linear-ch5-input.json')):
 key=src['id'].replace('anton-section-5-','')
 if key in repairs:
  import copy
  parts=copy.deepcopy(src['parts'])
  for part in parts:
   if part['role']=='problem':part['crops']=[repairs[key]]
   if key in ['1-7','1-9'] and part['role']=='instructions':part['crops']=[[62,370.81,255,23]]
  out[src['id']]['sourceFigureParts']=parts
  out[src['id']]['reviewNotice']='The source crop was repaired against the complete chapter page to restore the first matrix row and exclude neighboring exercise fragments.'
# Final crop audit: exact full-page bounds; also repair reused reference crops.
additional_crop_repairs=[('practice/linear-sections/299.svg.gz', [59, 116.24, 127.45, 40.5], [59, 116.24, 127.45, 27]), ('practice/linear-sections/309.svg.gz', [59, 592.48, 127.45, 42.53], [59, 592.48, 127.45, 28]), ('practice/linear-sections/309.svg.gz', [328, 468.55, 255, 58.3], [328, 468.55, 255, 45])]
for src in json.load(open('tmp/linear-ch5-input.json')):
 import copy
 parts=copy.deepcopy(out[src['id']].get('sourceFigureParts',src['parts']))
 changed=False
 for part in parts:
  for i,crop in enumerate(part.get('crops',[])):
   for file,old,new in additional_crop_repairs:
    if part['file']==file and crop==old:
     part['crops'][i]=new;changed=True
 if changed:
  out[src['id']]['sourceFigureParts']=parts
  out[src['id']]['reviewNotice']='Source image crops were checked against the full chapter page and repaired to preserve complete matrices while excluding adjacent exercise fragments.'
expected={q['id'] for q in json.load(open('tmp/linear-ch5-input.json'))};assert set(out)==expected,(expected-set(out),set(out)-expected)
# Normalize simple manual fractions inside explicit math spans.
import re
def format_math(text):
 if not isinstance(text,str):return text
 def fragment(m):
  st=m.group(1)
  st=re.sub(r'(?<![A-Za-z\\])([A-Za-z]+|[0-9]+)/([A-Za-z]+|[0-9]+)',lambda q:r'\frac{'+q.group(1)+'}{'+q.group(2)+'}',st)
  return r'\('+st+r'\)'
 return re.sub(r'\\\((.*?)\\\)',fragment,text)
for question in out.values():
 for field in question['fields']:
  for name in ['answer','selectionPrompt','explanation']:
   field[name]=format_math(field[name])
  for name in ['options','workedSteps']:
   if name in field:field[name]=[format_math(x) for x in field[name]]
Path('scripts/linear-answer-checks/ch05-reviewed.json').write_text(json.dumps(dict(chapter=5,questions=out),ensure_ascii=False,indent=2)+'\n')
print('Verified and generated',len(out),'chapter 5 exercises; eigenvectors, diagonalizations, powers and differential solutions passed exact residual checks.')
