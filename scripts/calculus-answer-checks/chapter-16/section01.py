from common import *
row=lambda k,*fs,**kw:A.row(1,k,*fs,**kw)
desc={1:'Constant vector ⟨0.3,−0.4⟩, down and right, magnitude0.5',2:'Outward from origin; horizontal component x/2 and vertical component y',3:'Leftward component−1/2 everywhere; upward when y>x and downward when y<x',4:'Horizontal component y, vertical component x+y; zero only at origin',5:'Unit vectors ⟨y,x⟩/sqrt(x²+y²); undefined at origin; outward on y=x and inward on y=−x',6:'Unit clockwise tangent vectors to circles centered at origin; undefined at origin',7:'Constant unit vector parallel to positive x-axis',8:'Parallel to x-axis; +x for z>0, −x for z<0, zero on z=0; length|z|',9:'Parallel to x-axis; −x for y>0, +x for y<0, zero on y=0; length|y|',10:'Constant vector ⟨1,0,1⟩, magnitude sqrt2, diagonal in positive xz direction'}
for k,ans in desc.items():row(k,c('Vector field geometry',ans,'Vectors all point vertically upward','Vectors are zero at every point'),limited=True,why='Read each vector component at the base point; retain direction and magnitude in the sketch.')
for k,ans in {11:'IV',12:'II',13:'I',14:'III',15:'IV',16:'I',17:'III',18:'II',29:'III',30:'IV',31:'II',32:'I'}.items():row(k,c('Plot',ans,*[a for a in ['I','II','III','IV'] if a!=ans]),limited=True,why='Compare component signs, zero sets and magnitude with the original plotted arrows.')
row(19,c('Zero set','The line y=2x','Only the origin','The line y=−2x'),c('Factorization','F=(y−2x)⟨y,3x⟩','F=(y+2x)⟨y,3x⟩','F=⟨y,3x⟩'),limited=True)
row(20,c('Zero set','Origin and circle x²+y²=4','Circle x²+y²=2 only','Only origin'),c('Radial direction','Inward for0<r<2; outward for r>2','Outward for all r>0','Inward for all r>0'),limited=True)
funcs={21:y*s.sin(x*y),22:s.sqrt(2*u+3*v),23:s.sqrt(x*x+y*y+z*z),24:x*x*y*s.exp(y/z),25:(x-y)**2/2,26:(x*x-y*y)/2,27:s.log(1+x*x+2*y*y),28:s.cos(x)-2*s.sin(y)}
for k,fun in funcs.items():
 var=(u,v) if k==22 else (x,y,z) if k in(23,24) else (x,y);fs=[cv('Gradient', [s.diff(fun,a) for a in var])]
 if k>=27:fs.append(c('Relation to contours','Gradient is perpendicular to regular level curves and points toward increasing f','Gradient is tangent to every contour','Gradient always points toward decreasing f'))
 row(k,*fs,limited=k>=25,why='Differentiate with respect to each coordinate, holding the others fixed; ∇f·tangent=0 along a level curve.')
row(33,n('Estimated x',2.04),n('Estimated y',1.03),why='Euler step: (2,1)+0.01(4,3).')
row(34,n('Estimated x',1.05),n('Estimated y',2.95),why='Euler step: (1,3)+0.05(1,−1).')
row(35,c('a · Flow lines','xy=C, with coordinate axes as special trajectories','x²+y²=C','y=x²+C'),c('b · Differential equations','x′=x, y′=−y','x′=−x,y′=y','x′=y,y′=x'),c('b · Through(1,1)','y=1/x, x>0; x increases with time','y=x','y=−1/x'),limited=True)
row(36,c('a · Shapes','Parabolas y=x²/2+C','Circles','Straight lines'),c('b · Equations','x′=1,y′=x, hence dy/dx=x','x′=x,y′=1','dy/dx=1/x'),c('c · From origin','y=x²/2, x≥0 for future time','y=x²','y=−x²/2'),limited=True)
savepart('section01')
