from common import *
row=lambda k,*fs,**kw:A.row(3,k,*fs,**kw)
row(1,n('Line integral',40),why='Read endpoint contour values in the source, then use f(B)−f(A).')
row(2,n('Line integral',6),why='r(0)=(1,0),r(1)=(2,2); table gives9−3=6.')
pots={4:x*y*y-x*x,5:y*s.exp(x*y),6:y*s.exp(x)+s.exp(y),7:y*s.exp(x)+x*s.sin(y),8:x*x*y+x/y**2,9:y*y*s.sin(x)+x*s.cos(y),10:x*s.log(y)+y*s.log(x),12:3*x+x*x*y*y,13:x**3*y**3/3,14:x*s.exp(x*y),15:x*y*z+z*z,16:x*y*y*z+x*x*z*z,17:y*s.exp(x*z),18:x*s.sin(y)+y*s.cos(z),19:x*x*s.exp(-y)+y*y,20:x*s.sin(y)+s.cos(y),23:(x**4+y**4)/4,24:x*x+x*y}
for k in range(3,11):
 if k==3:row(k,c('Conservative?','No: P_y=x+2y differs from Q_x=2x+2y','Yes, f=x²y+xy²','Yes, f=xy'));continue
 row(k,c('Conservative?','Yes','No','Only at the origin'),f('One potential f',pots[k],constant=True),why='Differentiate the displayed potential with respect to each coordinate to recover F on its domain.')
row(11,c('a · Reason','F=∇(x²y), so only endpoints matter','All three curves have equal length','F is constant'),n('b · Integral',16),limited=True)
ends={12:([1,1],[4,R(1,4)]),13:([0,0],[-1,3]),14:([1,0],[0,2]),15:([1,0,-2],[4,6,3]),16:([0,1,0],[1,2,1]),17:([1,-1,0],[5,3,0]),18:([0,1,0],[1,1,pi]),19:([1,0],[2,1]),20:([2,0],[1,pi]),23:([1,0],[2,2]),24:([1,1],[4,3])}
for k,(p,q) in ends.items():
 val=pots[k].subs(dict(zip((x,y,z),q)))-pots[k].subs(dict(zip((x,y,z),p)));fs=[n('Line integral / work',val)]
 if k<=20:fs.insert(0,f('One potential f',pots[k],constant=True))
 row(k,*fs,limited=k in(19,20),why='Verify ∇f=F and apply f(end)−f(start); the original path orientation determines the sign.')
row(21,c('Least-work path','Every admissible path between the fixed endpoints gives the same work','The shortest path always gives less work','Only a straight line minimizes the work'),limited=True)
row(22,c('Conclusion','F is not conservative because two paths between the same endpoints give unequal work','F is conservative','The result only shows the curves have different lengths'),limited=True)
row(25,c('Conservative?','No: circulation around an origin-centered circle is nonzero','Yes: all closed-loop integrals vanish','Yes: the arrows point radially'),limited=True)
row(26,c('Conservative?','The plot is consistent with a conservative field: opposite sides of symmetric rectangular loops cancel; a plot alone cannot prove it','No: every loop has strictly positive circulation','No: every loop has strictly negative circulation'),limited=True)
row(27,c('Conservative?','Yes','No','Only on the x-axis'),f('Potential',x*s.sin(y)+y,constant=True),limited=True)
row(28,c('a · One valid nonclosed curve','r(t)=(2t,t),0≤t≤1, with constant f=0','r(t)=(t,0),0≤t≤π/2','r(t)=(0,t),0≤t≤π/4'),c('b · One valid nonclosed curve','r(t)=(t,0),0≤t≤π/2','r(t)=(2t,t),0≤t≤1','r(t)=(−t,0),0≤t≤π/2'))
row(29,c('Mixed-partial argument','P=f_x,Q=f_y,R=f_z; equality of continuous mixed partials gives P_y=Q_x,P_z=R_x,Q_z=R_y','All diagonal partials must be equal','All first partials must be zero'),limited=True)
row(30,c('Obstruction','P_z=0 but R_x=yz, so the field cannot be a gradient on an open region','P_y differs from Q_x','R has no derivatives'),limited=True)
for k,ans in {31:('Yes','Yes','Yes'),32:('Yes','No','No'),33:('No','Yes','Yes'),34:('Yes','Yes','No')}.items():row(k,*[c(label,a,'No' if a=='Yes' else 'Yes') for label,a in zip(['a · Open','b · Connected','c · Simply connected'],ans)])
row(35,f('a · Common cross partial',(y*y-x*x)/(x*x+y*y)**2),n('b · Upper semicircle',pi),n('b · Lower semicircle',-pi),c('Theorem6','No contradiction: punctured plane is not simply connected','Contradicts the theorem','The field is undefined everywhere'),limited=True)
cc,d1,d2,eps=s.symbols('c d1 d2 epsilon',positive=True)
row(36,f('a · Work',cc*(1/d1-1/d2)),n('b · Earth work',6.67e-11*5.97e24*1.99e30*(1/1.47e11-1/1.52e11),'J'),f('c · Work',R(16,100000000)*eps),why='Potential−c/r yields c(1/d₁−1/d₂); use meters for gravity and c=εqQ for the electric field.')
savepart('section03')
