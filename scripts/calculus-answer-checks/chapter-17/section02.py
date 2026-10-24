from ode import *
rows={1:((1,2,-8),1-2*x*x,None),2:((1,-3,0),s.sin(2*x),None),3:((9,0,1),s.exp(2*x),None),4:((1,-2,2),x+s.exp(x),None),5:((1,-4,5),s.exp(-x),None),6:((1,-4,4),x-s.sin(x),None),7:((1,-2,5),s.sin(x),iv(1,1)),8:((1,0,-1),x*s.exp(2*x),iv(0,1)),9:((1,-1,0),x*s.exp(x),iv(2,1)),10:((1,1,-2),x+s.sin(2*x),iv(1,0)),11:((1,3,2),s.cos(x),None),12:((1,0,4),s.exp(-x),None)}
for k,(abc,rhs,ics) in rows.items():
 sol=solve(abc,rhs,ics);fs=[answer(sol,abc)]
 if k==11:fs+=[c('Graph behavior','All solutions approach (cos x+3sin x)/10 as x→∞','All solutions approach zero','All solutions grow exponentially')]
 if k==12:fs+=[c('Graph behavior','y−e^(−x)/5 is a sinusoid of angular frequency 2; the exponential transient vanishes as x→∞','Every solution approaches zero','Every solution is monotone')]
 A.row(2,k,*fs,limited=k in (11,12),why='Choose a particular trial matching the forcing, multiply by x if it overlaps the complementary solution, then match coefficients. Add the complementary solution and impose any stated initial conditions. Direct substitution checks the result.')
trials={13:('e^x[(Ax+B)cos x+(Cx+D)sin x]','(Ax+B)cos x+(Cx+D)sin x','Ae^x cos x'),14:('A cos4x+B sin4x+x(C cos2x+D sin2x)','A cos4x+B sin4x+C cos2x+D sin2x','Ax+B'),15:('Ax e^x+B cos x+C sin x','Ae^x+B cos x+C sin x','Ax e^x'),16:('x e^x(Ax³+Bx²+Cx+D)','e^x(Ax³+Bx²+Cx+D)','Ax e^x'),17:('x e^(−x)[(Ax²+Bx+C)cos3x+(Dx²+Ex+F)sin3x]','e^(−x)[(Ax²+Bx+C)cos3x+(Dx²+Ex+F)sin3x]','Ax²e^(−x)cos3x'),18:('Ae^(3x)+x[(Bx+C)cos2x+(Dx+E)sin2x]','Ae^(3x)+(Bx+C)cos2x+(Dx+E)sin2x','Ae^(3x)+Bx sin2x')}
for k,opts in trials.items():A.row(2,k,c('Trial particular solution',*opts),why='Include the complete polynomial times sine/cosine pair. Multiply each resonant component by x once for a simple characteristic root; do not solve for the arbitrary trial coefficients.')
for k,abc,rhs in [(19,(4,0,1),s.cos(x)),(20,(1,-2,-3),x+2),(21,(1,-2,1),s.exp(-x)),(22,(1,-1,0),s.exp(x))]:
 sol=solve(abc,rhs)
 y1,y2=({19:(s.cos(x/2),s.sin(x/2)),20:(s.exp(3*x),s.exp(-x)),21:(s.exp(x),x*s.exp(x)),22:(1,s.exp(x))}[k]);y1=s.sympify(y1);y2=s.sympify(y2)
 W=s.simplify(y1*s.diff(y2,x)-s.diff(y1,x)*y2);u=s.simplify(-y2*rhs/(abc[0]*W));v=s.simplify(y1*rhs/(abc[0]*W))
 A.row(2,k,answer(sol,abc,'a · Solution by undetermined coefficients'),f('b · u₁′ for basis ('+fmt(y1)+', '+fmt(y2)+')',u),f('b · u₂′ for the same basis',v),answer(sol,abc,'b · Solution by variation of parameters'),why='For normalized forcing g=G/a and W=y₁y₂′−y₁′y₂, variation of parameters gives u₁′=−y₂g/W and u₂′=y₁g/W. Its solution agrees with undetermined coefficients up to homogeneous terms.')
# Explicit variation-of-parameters solutions, with domain restrictions retained.
part={23:-1+s.sin(x)*s.log(s.sec(x)+s.tan(x)),24:s.sec(x)/2,25:s.exp(x)*(-x+s.log(1+s.exp(x)))+s.exp(2*x)*(s.log(1+s.exp(-x))-s.exp(-x)),26:-s.exp(-2*x)*s.sin(s.exp(x)),27:s.exp(x)*(x*s.atan(x)-s.log(1+x*x)/2),28:s.exp(-2*x)/(2*x)}
for k,abc,rhs,basis,domain in [(23,(1,0,1),s.sec(x)**2,s.cos(x)*C1+s.sin(x)*C2,'0<x<π/2'),(24,(1,0,1),s.sec(x)**3,s.cos(x)*C1+s.sin(x)*C2,'0<x<π/2'),(25,(1,-3,2),1/(1+s.exp(-x)),C1*s.exp(x)+C2*s.exp(2*x),'All real x'),(26,(1,3,2),s.sin(s.exp(x)),C1*s.exp(-x)+C2*s.exp(-2*x),'All real x'),(27,(1,-2,1),s.exp(x)/(1+x*x),(C1+C2*x)*s.exp(x),'All real x'),(28,(1,4,4),s.exp(-2*x)/x**3,(C1+C2*x)*s.exp(-2*x),'Any interval wholly in x>0 or x<0')]:
 sol=basis+part[k];res=s.trigsimp(s.simplify(op(sol,abc)-rhs));assert res==0,(k,res)
 cases.append(dict(coefficients=list(map(str,abc)),forcing=str(rhs),solution=str(sol),ics={}))
 A.row(2,k,answer(sol,abc),c('Validity interval',domain,'No real interval','Only x=0'),why='Variation of parameters integrates −y₂G/(aW) and y₁G/(aW); substitute the particular solution into the original equation. Restrict to an interval where the forcing is defined.')
save('section02')
