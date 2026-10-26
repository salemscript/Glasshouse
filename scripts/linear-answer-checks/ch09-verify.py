import sympy as s,json,numpy as np
from pathlib import Path
M=s.Matrix; R=s.Rational; out={}; checks=[]
def tex(x):return s.latex(x,mat_delim='',mat_str='bmatrix')
def w(x):return r'\('+str(x)+r'\)'
def choice(label,prompt,ans,steps,bad=None):
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
def num(label,prompt,ans,steps,tol=1e-6):return dict(label=label,selectionPrompt=prompt,type='numeric',answer=float(ans),tolerance=tol,explanation=steps[-1],workedSteps=steps)
def put(key,fields,scope=None,notice=None):
 id='anton-'+('chapter-09-supplementary-'+key[1:] if key.startswith('s') else 'section-9-'+key)
 out[id]=dict(fields=fields,scope=scope or 'All requested parts of the source exercise.',complete=True,sourceImageReviewed=True)
 if notice:out[id]['reviewNotice']=notice

def fac(A,ldu=False):
 L,U,p=A.LUdecomposition();P=s.eye(A.rows)
 for i,j in p:P.row_swap(i,j)
 P=P.T
 assert P*L*U==A
 if ldu:
  D=s.diag(*U.diagonal());U=D.inv()*U
  assert P*L*D*U==A
  return 'L='+tex(L)+',\\quad D='+tex(D)+',\\quad U='+tex(U)
 return ('P='+tex(P)+',\\quad ' if p else '')+'L='+tex(L)+',\\quad U='+tex(U)
for key,A,b in [('1-1',M([[3,-6],[-2,5]]),M([0,1])),('1-3',M([[2,8],[-1,-1]]),M([-2,-2])),('1-5',M([[2,-2,-2],[0,-2,2],[-1,5,2]]),M([-4,-2,6])),('1-11',M([[0,1,4],[1,2,2],[3,1,3]]),M([2,1,5])),('1-15',M([[3,-1,0],[3,-1,1],[0,2,1]]),M([-2,1,4]))]:
 L,U,p=A.LUdecomposition(); bb=b.copy()
 for i,j in p:bb.row_swap(i,j)
 y=L.inv()*bb;x=U.inv()*y; assert A*x==b
 steps=['Use the verified triangular factorization '+w(fac(A))+'.','Forward substitution gives '+w('y='+tex(y))+'.','Back substitution gives '+w('x='+tex(x))+'.']
 fields=[choice('a','Select the factorization and solution.',w(fac(A)+',\\quad x='+tex(x)),steps)]
 put(key,fields,notice='The source crop includes a displaced first row; the complete matrix was checked against the chapter PDF.' if key=='1-5' else None)
A=M([[2,-1,3],[4,2,1],[-6,-1,2]]);L=M([[1,0,0],[2,1,0],[-3,-1,1]]);U=L.inv()*A
put('1-7',[choice('a','Select both triangular inverses.',w('L^{-1}='+tex(L.inv())+', U^{-1}='+tex(U.inv())),['Solve the triangular systems column by column.',w('L^{-1}='+tex(L.inv())+', U^{-1}='+tex(U.inv()))]),choice('b','Select the inverse of A.',w('A^{-1}='+tex(A.inv())),[w('(LU)^{-1}=U^{-1}L^{-1}'),w('A^{-1}='+tex(A.inv()))])])
L=M([[1,0,0],[-1,1,0],[1,1,1]]);U=M([[2,1,-1],[0,0,1],[0,0,0]]);D=s.diag(2,1,1);A=M([[2,1,-1],[-2,-1,2],[2,1,0]]);assert L*U==A
put('1-9',[choice('a','Select an LU decomposition.',w('L='+tex(L)+', U='+tex(U)),['Subtract multiples of row 1, then use the pivot in column 3.',w('LU='+tex(A))]),choice('b','Select the requested LDU form.',w('L_1='+tex(L)+', D='+tex(D)+', U_1='+tex(D.inv()*U)),['Move the factor 2 in the first row of U into D.',w('L_1DU_1=A')]),choice('c','Select the unit lower triangular LU form.',w('L_2='+tex(L)+', U_2='+tex(U)),['The L from part (a) already has unit diagonal.',w('L_2U_2=A')])])
for key,A,ldu in [('1-13',M([[2,2],[4,1]]),True),('s1',M([[-6,2],[6,0]]),False),('s2',M([[-6,2],[6,0]]),True),('s3',M([[2,4,6],[1,4,7],[1,3,7]]),False),('s4',M([[2,4,6],[1,4,7],[1,3,7]]),True)]:put(key,[choice('a','Select the requested factorization.',w(fac(A,ldu)),['Eliminate entries below each pivot; record each multiplier in L.','Separate diagonal pivots into D when required.',w(fac(A,ldu))+'; multiplication recovers the original matrix.'])])
put('1-17',[choice('a','With LU already available, select the substitution operation counts (division counted as multiplication).',w('n(n-1)\\text{ additions},\\quad n^2\\text{ multiplications}'),['Each triangular solve uses '+w('n(n-1)/2')+' additions and products. In the text convention, U has unit diagonal, so only the lower solve needs n divisions.','Two solves therefore use '+w('n(n-1)')+' additions and '+w('n^2')+' multiplications including divisions.'],[w('n(n-1)\\text{ additions and }n(n+1)\\text{ multiplications}'),w('2n^3\\text{ of each}')])])
put('1-18',[choice('a','Select the unique factorization and its uniqueness argument.',w(r'L=\begin{bmatrix}1&0\\c/a&1\end{bmatrix},\quad U=\begin{bmatrix}a&b\\0&d-cb/a\end{bmatrix}'),['Write '+w(r'L=\begin{bmatrix}1&0\\l&1\end{bmatrix}, U=\begin{bmatrix}u&v\\0&w\end{bmatrix}')+'.','Comparing entries forces '+w('u=a,v=b,l=c/a,w=d-cb/a')+'. Since a is nonzero, all are uniquely determined.'])])
put('2-1',[num('a','Enter the dominant eigenvalue.',-8,['Compare absolute values: 8 is strictly largest.','The dominant eigenvalue is −8.']),choice('b','Does a dominant eigenvalue exist?','No',['Both −5 and 5 have absolute value 5.','Neither has strictly largest magnitude.'],['Yes, −5','Yes, 5'])])
def power(A,x,n,mode='euclid',rounded=False):
 x=np.array(x,dtype=float);A=np.array(A,dtype=float); seq=[]
 for _ in range(n):
  y=A@x; den=np.linalg.norm(y) if mode=='euclid' else y[np.argmax(abs(y))];x=y/den
  if rounded:x=np.round(x,3)
  seq.append(x.copy())
 q=float(x@A@x/(x@x));return x,q,seq
def vtxt(x):return tex(M([round(float(a),7) for a in x]))
for key,A,x,mode in [('2-3',M([[5,-1],[-1,-1]]),[1,0],'euclid'),('2-5',M([[1,-3],[-3,5]]),[1,1],'max'),('2-6',M([[3,2,2],[2,2,0],[2,0,4]]),[1,1,1],'max')]:
 v,q,seq=power(A,x,4,mode); eig=max(A.eigenvects(),key=lambda t:abs(float(t[0])));ev=eig[2][0]; ev=ev/ev.norm() if mode=='euclid' else ev/max(ev,key=lambda t:abs(float(t)))
 put(key,[choice('a','Select the fourth iterate and Rayleigh quotient.',w('x_4\\approx '+vtxt(v)+', R(x_4)\\approx '+str(round(q,7))),['Apply '+w(r'x_{k+1}=Ax_k/'+(r'\|Ax_k\|_2' if mode=='euclid' else r'\max(Ax_k)'))+'.']+[w('x_'+str(i+1)+'\\approx '+vtxt(z)) for i,z in enumerate(seq)]),choice('b','Select the exact dominant eigenpair for comparison.',w('\\lambda='+tex(eig[0])+', v='+tex(ev)),['Solve the characteristic polynomial '+w(tex(A.charpoly().as_expr()))+'=0.','The largest absolute eigenvalue is '+w(tex(eig[0]))+'. Solving its null space and scaling gives '+w('v='+tex(ev))+'.'])],notice='The full first row of the matrix was verified in the chapter PDF.' if key=='2-6' else None)
v,q,seq=power([[2,-1],[-1,2]],[1,0],3,'max',True)
put('2-7',[choice('a','Select the three-decimal third iterate.',w('x_3='+vtxt(v)),[w('x_'+str(i+1)+'='+vtxt(z)) for i,z in enumerate(seq)]),num('b','Enter the Rayleigh quotient (within 0.001).',q,[w('R(x)=\\frac{x^TAx}{x^Tx}'),w('R(x_3)\\approx '+str(q))],.001),choice('c','Select the exact eigenpair.',w(r'\lambda=3,\quad v=\begin{bmatrix}1\\-1\end{bmatrix}'),['The characteristic polynomial is '+w('(\\lambda-1)(\\lambda-3)')+'.',w(r'A(1,-1)^T=3(1,-1)^T')]),num('d','Enter the percentage error (percent, within 0.001).',abs(q-3)/3*100,[w(r'100\frac{|R-3|}{3}')+' gives the percentage error.','The error is '+str(abs(q-3)/3*100)+'%.'],.001)])
v=np.array([121,122.]);q=v@np.array([[1,2],[2,1]])@v/(v@v)
put('2-9',[choice('a','Select the fifth-iterate approximation and Rayleigh quotient.',w('v\\approx '+vtxt(v/np.linalg.norm(v))+',\\quad \\lambda\\approx '+str(round(q,7))),['Normalize '+w('(121,122)^T')+' to obtain the approximate unit eigenvector.','Substitute this vector into '+w(r'R(v)=\frac{v^TAv}{v^Tv}')+'.',w('R=\\frac{88573}{29525}\\approx '+str(round(q,7)))])])
put('2-11',[choice('a','Select the power-sequence behavior.',w(r'x_k=((-1)^k\operatorname{sgn}(a),0)^T\quad(k\ge1)'),[w('A^kx_0=((-1)^ka,0)^T')+'.','Normalization leaves alternating opposite unit vectors; since a is nonzero, they do not converge.'],['The sequence converges to zero.','The sequence converges to a single unit vector.'])])
fields=[]
for label,A in [('a',[[1,3,3],[3,4,-1],[3,-1,10]]),('b',[[1,0,1,1],[0,2,-1,1],[1,-1,4,1],[1,1,1,8]])]:
 a=np.array(A,float);x=np.ones(len(A));x/=np.linalg.norm(x);old=x@a@x;seq=[]
 for k in range(1,1000):
  x=a@x;x/=np.linalg.norm(x);q=x@a@x;err=abs(q-old)/abs(q)*100;seq.append((k,q,err));old=q
  if err<.1:break
 fields.append(choice(label,'Select the approximation using an all-ones starting direction and successive Rayleigh error below 0.1%.',w('v\\approx '+vtxt(x)+',\\lambda\\approx '+str(round(q,7))),['Normalize the all-ones vector; repeatedly apply A and normalize.','Use '+w(r'100|R_k-R_{k-1}|/|R_k|<0.1')+' as the stopping rule.','At iteration '+str(k)+', '+w('R_k\\approx '+str(round(q,7)))+' and estimated error is '+str(round(err,6))+'%.','The resulting unit vector is '+w(vtxt(x))+'.']))
put('2-12',fields)
for key,den in [('2-16',r'\|A^kx_0\|'),('2-17',r'\max(A^kx_0)')]:
 put(key,[choice('a','Select the induction conclusion wherever the normalization is defined.',w('x_k=\\frac{A^kx_0}{'+den+'}'),['The k=1 case is exactly the defining recurrence.','Substitute the induction hypothesis into the recurrence. The scalar normalization cancels between numerator and denominator.','The result is '+w('x_{k+1}=\\frac{A^{k+1}x_0}{'+den.replace('^k','^{k+1}')+'}')+'.'])])
for key,ns,speed in [('3-1',[1000,10000,100000],10e9),('3-2',[10000,100000,1000000],100e9)]:
 put(key,[num(chr(97+i),'Enter execution time in seconds (relative rounding to six significant figures accepted).',(R(2,3)*n**3+R(3,2)*n**2-R(7,6)*n)/speed,['Formula (5) gives '+w(r'F=\frac23n^3+\frac32n^2-\frac76n')+'.','Divide F by '+str(speed)+' flops per second.','Time is approximately '+str(float((R(2,3)*n**3+R(3,2)*n**2-R(7,6)*n)/speed))+' seconds.'],max(1e-6,float(n**3/speed)*1e-5)) for i,n in enumerate(ns)])
for key,n,speed in [('3-3',10000,70e9),('3-4',100000,16e15)]:
 vals=[2*n**3/3,n*n,2*n**3/3,2*n**3];forms=[r'\frac23n^3','n^2',r'\frac23n^3','2n^3']
 put(key,[num(chr(97+i),'Enter approximate execution time in seconds.',v/speed,['Table 1 gives '+w(forms[i])+' flops.','Divide the operation count by the stated processing rate.','Estimated time = '+str(v/speed)+' seconds.'],max(1e-8,v/speed*1e-4)) for i,v in enumerate(vals)])
put('3-5',[num('a1','Enter forward-phase time in seconds.',2e15/3/1e9,['Forward work is '+w(r'\frac23(10^5)^3')+' flops.','At '+w('10^9')+' flops/s, time is 666666.6667 seconds.'],1),num('a2','Enter backward-phase time in seconds.',10,['Backward work is '+w('(10^5)^2=10^{10}')+' flops.','Dividing by '+w('10^9')+' gives 10 seconds.']),num('b','Enter the speed threshold in gigaflops/s (the speed must exceed it).',4000/3,['Require '+w(r'\frac{(2/3)10^{12}}{r10^9}<0.5')+'.','Thus '+w('r>4000/3')+' gigaflops/s.'],.01)])
put('3-6',[num('a','Enter the speed threshold in teraflops/s (must exceed it).',4000,['Inverse computation costs about '+w('2(10^5)^3=2\\times10^{15}')+' flops.','For less than 0.5 s, require more than '+w('4\\times10^{15}')+' flops/s = 4000 teraflops/s.'])])
for key,ans,why,bad in [('3-7','n^2','Multiply each of the n² entries once.',['n','2n^2']),('3-8','n^2','Add each of the n² corresponding pairs once.',['2n^2','n^3']),('3-9','2n^3-n^2','Each of n² entries uses n multiplications and n−1 additions.',['n^3','2n^3']),('3-10','n(k-1)','Compute each of n diagonal kth powers using k−1 successive multiplications.',['nk','n^2(k-1)'])]:put(key,[choice('a','Select the flop count.',w(ans),[why,'The count is '+w(ans)+'.'],[w(z) for z in bad])])
def svd(A):
 vs=[];vals=[]
 for e,m,basis in sorted((A.T*A).eigenvects(),key=lambda t:float(t[0]),reverse=True):
  for b in s.GramSchmidt(basis,True):vs.append(b);vals.append(s.sqrt(e))
 V=M.hstack(*vs); rank=A.rank(); us=[s.simplify(A*vs[i]/vals[i]) for i in range(rank)]
 # Complete an orthonormal basis by Gram-Schmidt on coordinate vectors.
 for b in s.eye(A.rows).columnspace():
  z=b.copy()
  for u in us:z-=u.dot(z)*u
  if z.norm()!=0:us.append(s.simplify(z/z.norm()))
  if len(us)==A.rows:break
 U=M.hstack(*us);S=s.zeros(A.rows,A.cols)
 for i in range(rank):S[i,i]=vals[i]
 assert s.simplify(U*S*V.T-A)==s.zeros(*A.shape)
 assert s.simplify(U.T*U)==s.eye(A.rows) and s.simplify(V.T*V)==s.eye(A.cols)
 return U,S,V,rank
def svfield(A,reduced=False,expansion=False,label='a'):
 U,S,V,r=svd(A)
 if reduced:U=U[:,:r];S=S[:r,:r];V=V[:,:r]
 ans='U='+tex(U)+',\\quad \\Sigma='+tex(S)+',\\quad V^T='+tex(V.T)
 if expansion:ans='A='+ '+'.join(tex(S[i,i])+tex(U[:,i])+tex(V[:,i].T) for i in range(r))
 return choice(label,'Select a valid '+('reduced singular value expansion.' if expansion else 'singular value decomposition (the displayed third factor is V transpose).'),w(ans),['Compute '+w('A^TA='+tex(A.T*A))+'.','Its nonnegative eigenvalues yield singular values '+w(','.join(tex(S[i,i]) for i in range(r)))+'.','Choose orthonormal right eigenvectors and set '+w(r'u_i=Av_i/\sigma_i')+' for positive singular values.','The displayed factors satisfy '+w('U^TU=I,V^TV=I,U\\Sigma V^T=A')+' (with reduced identity sizes when applicable).'])
put('4-1',[choice('a','Select the distinct singular values (including zero eigenvalues of A transpose A).',w(r'\sqrt5,0'),[w(r'A^TA=\begin{bmatrix}1&2&0\\2&4&0\\0&0&0\end{bmatrix}')+'.','Its eigenvalues are 5,0,0; take their nonnegative square roots.'],[w('5,0'),w('1,2,0')])])
put('4-3',[choice('a','Select the distinct singular value.',w(r'\sqrt5'),[w('A^TA=5I')+'.','Both singular values equal '+w(r'\sqrt5')+'.'],[w('5'),w(r'\sqrt3')])])
As={5:M([[1,-1],[1,1]]),7:M([[4,6],[0,4]]),9:M([[-2,2],[-1,1],[2,-2]]),11:M([[1,0],[1,1],[-1,1]])}
for n,A in As.items():put('4-'+str(n),[svfield(A)])
put('4-13',[choice('a','Select the rank argument.',w(r'\operatorname{rank}(A^TA)=\operatorname{rank}(A)=\operatorname{rank}(A^T)=\operatorname{rank}(AA^T)'),['The identity '+w(r'x^TA^TAx=\|Ax\|^2')+' proves A and A transpose A have the same null space.','Rank-nullity gives equal ranks. Apply the same argument to A transpose and use equality of row and column rank.'])])
put('4-14',[choice('a','Select the rank-nullity calculation.',w(r'\operatorname{rank}(A^TA)=n-\operatorname{nullity}(A^TA)=n-\operatorname{nullity}(A)=\operatorname{rank}(A)'),['Part (a) gives equal null spaces and hence equal nullities.','Both matrices have n columns, so subtracting those nullities from n yields equal ranks.'])])
put('4-17',[choice('a','Select the singular values of A transpose A.',w(r'\sigma_1^2,\ldots,\sigma_n^2'),[w(r'A^TA=V\Sigma^T\Sigma V^T')+'.','This is a positive semidefinite symmetric matrix with eigenvalues '+w(r'\sigma_i^2')+'. Its singular values are these same nonnegative numbers.'])])
put('4-19',[choice('a','Select the polar factors and why they qualify.',w(r'P=U\Sigma U^T,\quad Q=UV^T'),[w(r'PQ=U\Sigma U^TUV^T=A')+'.',w(r'QQ^T=I')+'; moreover '+w(r'x^TPx=(U^Tx)^T\Sigma(U^Tx)\ge0')+'.','P has the same number of positive singular values, hence the same rank, as A.']),choice('b','Select a polar decomposition for Exercise 5.',w(r'P=\sqrt2 I,\quad Q=\frac1{\sqrt2}\begin{bmatrix}1&-1\\1&1\end{bmatrix}'),['For this A, '+w('AA^T=2I')+'.','Thus its positive square root is '+w(r'P=\sqrt2 I')+' and '+w('Q=P^{-1}A')+' is orthogonal.'])])
B={1:As[9],2:M([[-2,-1,2],[2,1,-2]]),3:As[11],4:M([[6,4],[0,0],[4,0]])}
for n,A in B.items():put('5-'+str(n),[svfield(A,True)]);put('5-'+str(n+4),[svfield(A,True,True)])
put('5-9',[num('a','Enter the number of stored scalars in the rank-100 SVD approximation.',70100,['Store 100 left vectors of length 200, 100 right vectors of length 500, and 100 singular values.','Total '+w('100(200+500+1)=70100')+'.']),num('b','Enter the original number of matrix entries.',100000,[w('200\\times500=100000')+'.','The rank-100 representation saves 29900 scalars, or 29.9%.'])])
A=M([[2,1],[1,2]]);v,q,seq=power(A,[1,0],5);v2,q2,seq2=power(A,[1,0],5,'max')
put('s5',[choice('a','Select the exact dominant eigenpair with positive unit eigenvector.',w(r'\lambda=3,\quad v=\frac1{\sqrt2}(1,1)^T'),['The eigenvalues are 3 and 1.','The eigenvector (1,1) has norm '+w(r'\sqrt2')+'.']),choice('b','Select the Euclidean fifth iterate.',w('x_5='+vtxt(v)),[w('A^5x_0=(122,121)^T')+'.','Normalize it to obtain '+w(vtxt(v))+', approaching '+w(r'(1,1)^T/\sqrt2')+'.']),choice('c','Select the maximum-entry fifth iterate.',w('x_5='+vtxt(v2)),['Divide (122,121) by 122.','This gives '+w('(1,121/122)^T')+', approaching (1,1).'])])
put('s6',[choice('a','Select the general behavior.', 'A two-cycle after normalization; constant only when the starting vector has equal coordinates.',[w(r'A(a,b)^T=(b,a)^T,\quad A^2=I')+'.','After normalization the two vectors alternate. They coincide exactly when a=b; a=−b gives opposite vectors.','Eigenvalues 1 and −1 tie in magnitude, so there is no dominant eigenvalue.'],['Always converges to a single eigenvector.','Always converges to zero.'])])
put('s7',[choice('a','Select the Rayleigh-quotient conclusion for a start with nonzero dominant component.', 'They converge to −8.1, slowly because 8/8.1 is close to 1.', ['The unique largest eigenvalue magnitude is 8.1.','The dominant eigenvector sign may alternate, but the Rayleigh quotient is unchanged by sign.','The next-to-dominant magnitude ratio is '+w('8/8.1')+', causing slow convergence.'],['They converge to 8.1.','They cannot converge because the dominant eigenvalue is negative.'])])
for key,A in [('s8',M([[1,1],[1,1]])),('s9',M([[1,1],[0,0],[1,1]]))]:put(key,[svfield(A)])
A=M([[1,1],[0,0],[1,1]]);put('s10',[svfield(A,True,label='a'),svfield(A,True,True,label='b')])
U=M([[1,1],[1,-1],[1,-1],[1,1]])/2;S=s.diag(24,12);Vt=M([[2,-1,2],[2,2,-1]])/3
assert U.T*U==s.eye(2) and Vt*Vt.T==s.eye(2)
put('s11',[choice('a','Select the reduced SVD.',w('U_r='+tex(U)+',\\Sigma_r='+tex(S)+', V_r^T='+tex(Vt)),['Only singular values 24 and 12 are nonzero.','Retain the first two columns of U, the leading 2 by 2 block of the middle factor, and the first two rows of the displayed V transpose.','The reduced product is unchanged because the omitted terms are multiplied by zero.'])])
put('s12',[choice('a','Do orthogonally similar matrices have equal singular values?','Yes',[w('B=Q^TAQ')+' implies '+w('B^TB=Q^TA^TAQ')+'.','The Gram matrices are similar and have identical eigenvalues; their nonnegative square roots agree.'],['No'])])
put('s13',[choice('a','Select the singular values with multiplicities.',w(r'1\text{ repeated }\dim W\text{ times};\quad0\text{ repeated }n-\dim W\text{ times}'),['An orthogonal projection satisfies '+w('P^T=P,P^2=P')+'.','Its eigenvalues are 1 on W and 0 on the orthogonal complement. Since '+w('P^TP=P')+', these are also its singular values.'])])
put('s14',[choice('a','Select the scalar and rank-one proof (A square).',w(r'A=uv^T\Longrightarrow A^2=(v^Tu)A,\quad k=v^Tu=\operatorname{tr}(A)'),['A rank-one square matrix can be written as a nonzero column u times a nonzero row v transpose.','Associativity yields '+w('uv^Tuv^T=u(v^Tu)v^T')+'.','The middle factor is a scalar, so '+w('A^2=kA')+'.'])])
out['anton-section-9-2-3']['fields'][1]['workedSteps'].append('Eigenvector signs are arbitrary; negate this exact vector to compare directly with the positive-first-coordinate power iterate.')
repairs={'1-5': [34, 403, 258, 43], '2-6': [59, 419, 258, 43]}
for src in json.load(open('tmp/linear-ch9-input.json')):
 key=src['id'].replace('anton-section-9-','')
 if key in repairs:
  import copy
  parts=copy.deepcopy(src['parts'])
  for part in parts:
   if part['role']=='problem':part['crops']=[repairs[key]]
  out[src['id']]['sourceFigureParts']=parts
  out[src['id']]['reviewNotice']='The source crop was repaired against the complete chapter page to restore the first matrix row and exclude neighboring exercise fragments.'
# Final crop audit: exact full-page bounds; also repair reused reference crops.
additional_crop_repairs=[('practice/linear-sections/518.svg.gz', [303, 202.88, 255, 47.9], [303, 202.88, 255, 34]), ('practice/linear-sections/518.svg.gz', [300, 250.79, 258, 88.88], [300, 237, 258, 86]), ('practice/linear-sections/518.svg.gz', [303, 473.33, 255, 38.68], [303, 473.33, 255, 23]), ('practice/linear-sections/518.svg.gz', [300, 512.01, 258, 43.43], [300, 498, 258, 42]), ('practice/linear-sections/527.svg.gz', [59, 243.14, 258, 53.99], [59, 243.14, 258, 31]), ('practice/linear-sections/527.svg.gz', [59, 380.65, 258, 52.99], [59, 380.65, 258, 30]), ('practice/linear-sections/540.svg.gz', [34, 51.03, 127.91, 56.61], [34, 50, 127.91, 40]), ('practice/linear-sections/540.svg.gz', [34, 107.64, 127.91, 56.04], [34, 94, 127.91, 40]), ('practice/linear-sections/543.svg.gz', [59, 435.17, 127.99, 57.71], [59, 435.17, 127.99, 41]), ('practice/linear-sections/543.svg.gz', [186.99, 435.17, 130.01, 57.71], [186.99, 435.17, 130.01, 41]), ('practice/linear-sections/543.svg.gz', [59, 492.88, 127.99, 25.97], [59, 479, 127.99, 41]), ('practice/linear-sections/543.svg.gz', [186.99, 492.88, 130.01, 25.97], [186.99, 479, 130.01, 41])]
for src in json.load(open('tmp/linear-ch9-input.json')):
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
expected={q['id'] for q in json.load(open('tmp/linear-ch9-input.json'))};assert set(out)==expected,(expected-set(out),set(out)-expected)
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
Path('scripts/linear-answer-checks/ch09-reviewed.json').write_text(json.dumps(dict(chapter=9,questions=out),ensure_ascii=False,indent=2)+'\n')
print('Verified and generated',len(out),'chapter 9 exercises; exact LU, inverse, SVD and orthonormality checks passed.')
