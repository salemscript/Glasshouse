from common import *
a,b,c0=s.symbols('a b c',real=True)
row=lambda k,*fs,**kw:A.row(2,k,*fs,**kw)
CASES=[]
row(1,c('a · Displacements','Arrows P→R and P→Q','Arrows O→R and O→Q','Arrows R→P and Q→P'),c('b · Difference quotients','2 times P→R and 5 times P→Q, both based at P','Half of P→R and one fifth of P→Q','Position vectors from O'),c('c · Derivative and unit tangent','r′(4)=lim[h→0](r(4+h)−r(4))/h; T(4)=r′(4)/|r′(4)|','T(4)=r(4)/|r(4)|','r′(4)=r(4)'),c('d · Orientation','Unit tangent at P points toward Q along increasing t','Unit tangent points toward O','Unit tangent points opposite Q'),limited=True,why='Difference vectors join the corresponding endpoints; division by positive time increments preserves direction.')
row(2,*V([1,1],'a · r(1)'),*V([R(121,100),R(11,10)],'a · r(1.1)'),*V([R(21,100),R(1,10)],'a · Displacement'),*V([2,1],'b · r′(1)'),*V([R(21,10),1],'b · Secant quotient'),c('b · Comparison','The secant quotient tends to the tangent as the time increment tends to zero','The two vectors are exactly equal','Their lengths must both equal1'),limited=True)
curves={3:([t-2,t*t+1],-1,'Parabola y=(x+2)²+1, traced toward increasing x'),4:([t*t,t**3],1,'Semicubical parabola y²=x³, x≥0; parameter increases from lower to upper branch'),5:([s.exp(2*t),s.exp(t)],0,'x=y² with y>0, traced upward'),6:([s.exp(t),2*t],0,'y=2ln x with x>0, traced toward increasing x'),7:([4*s.sin(t),-2*s.cos(t)],3*pi/4,'Ellipse x²/16+y²/4=1, counterclockwise'),8:([s.cos(t)+1,s.sin(t)-1],-pi/3,'Circle (x−1)²+(y+1)²=1, counterclockwise')}
for k,(r0,t0,shape) in curves.items():
 r0=vec(r0);d=r0.diff(t);row(k,c('a · Curve',shape,'A straight line through the origin','A circle centered at the origin'),*V(d,'b · r′(t)'),*V(r0.subs(t,t0),'c · Position'),*V(d.subs(t,t0),'c · Tangent'),limited=True,why='Eliminate t for the shape, then differentiate each component. The position arrow starts at the origin; the tangent is placed at the curve point.');CASES.append(dict(kind='derivative',n=k,r=list(map(str,r0)),derivative=list(map(str,d))))
curves2={9:[s.sqrt(t-2),3,t**-2],10:[s.exp(-t),t-t**3,s.log(t)],11:[t*t,s.cos(t*t),s.sin(t)**2],12:[1/(1+t),t/(1+t),t*t/(1+t)],13:[t*s.sin(t),s.exp(t)*s.cos(t),s.sin(t)*s.cos(t)],14:[s.sin(a*t)**2,t*s.exp(b*t),s.cos(c0*t)**2]}
for k,r0 in curves2.items():
 r0=vec(r0);d=r0.diff(t);row(k,*V(d,'r′(t)'),why='Differentiate componentwise using product and chain rules on the original real domain.');CASES.append(dict(kind='derivative',n=k,r=list(map(str,r0)),derivative=list(map(str,d))))
row(15,c('r′(t)','b+2tc','a+b+tc','2tb+c'),why='The vectors a,b,c are constant.')
row(16,c('r′(t)','a×b+2t(a×c)','a×b+t(a×c)','b×a+2t(c×a)'),why='Expand r=t(a×b)+t²(a×c); preserve cross-product order.')
for k,r0,t0 in [(17,[t*t-2*t,1+3*t,t**3/3+t*t/2],2),(18,[s.atan(t),2*s.exp(2*t),8*t*s.exp(t)],0),(19,[s.cos(t),3*t,2*s.sin(2*t)],0),(20,[s.sin(t)**2,s.cos(t)**2,s.tan(t)**2],pi/4)]:
 r0=vec(r0);v=r0.diff(t).subs(t,t0);row(k,*V(unit(v),'Unit tangent'),why='Evaluate r′ at the specified parameter, then divide by its positive magnitude.');CASES.append(dict(kind='unit',n=k,r=list(map(str,r0)),at=str(t0),expected=list(map(str,unit(v)))))
r0=vec([t,t*t,t**3]);d=r0.diff(t);row(21,*V(d,'r′'),*V(unit(d.subs(t,1)),'T(1)'),*V(d.diff(t),'r″'),*V(d.cross(d.diff(t)),'r′×r″'))
r0=vec([s.exp(2*t),s.exp(-2*t),t*s.exp(2*t)]);d=r0.diff(t);row(22,*V(unit(d.subs(t,0)),'T(0)'),*V(d.diff(t).subs(t,0),'r″(0)'),f('r′·r″',s.expand(d.dot(d.diff(t)))))
u=s.symbols('u',real=True)
for k,r0,t0 in [(23,[t*t+1,4*s.sqrt(t),s.exp(t*t-t)],1),(24,[s.log(t+1),t*s.cos(2*t),2**t],0),(25,[s.exp(-t)*s.cos(t),s.exp(-t)*s.sin(t),s.exp(-t)],0),(26,[s.sqrt(t*t+3),s.log(t*t+3),t],1),(29,[t,s.exp(-t),2*t-t*t],0),(30,[2*s.cos(t),2*s.sin(t),4*s.cos(2*t)],pi/6),(31,[t*s.cos(t),t,t*s.sin(t)],pi)]:
 r0=vec(r0);p=r0.subs(t,t0);v=r0.diff(t).subs(t,t0);row(k,*V(p+u*v,'Tangent line (parameter u)'),limited=k>=29,why='Use r(t₀)+u r′(t₀), with u a new line parameter. Nonzero scalar multiples of the direction describe the same line.');CASES.append(dict(kind='tangent',n=k,r=list(map(str,r0)),at=str(t0),point=list(map(str,p)),direction=list(map(str,v))))
row(27,*V(vec([3,4,2])+u*vec([4,-3,6]),'Tangent line (parameter u)'),why='The direction is perpendicular to both surface normals(6,8,0) and(0,8,4).')
row(28,*V([s.sqrt(3),1,s.exp(pi/6)],'Point'),why='The plane normal(sqrt3,1,0) dotted with r′ gives−2sqrt3 sin t+2cos t=0; in[0,π] this selects t=π/6.')
row(32,*V([1,2,1],'a · Intersection'),limited=True,why='At t=0 the tangent has z=1 and y=2x; at t=1/2 it is the vertical line x=1,y=2.')
row(33,n('Angle between forward tangent vectors',float(s.acos(1/s.sqrt(6))*180/pi),unit='degrees',tol=.51),why='At0 the tangents are(1,0,0) and(1,2,1).')
# Exact intersection: 3+t²=(3−t)² => t=1, s=2, point(1,0,4).
row(34,*V([1,0,4],'Intersection'),n('Angle between forward tangent vectors',float(s.acos(6/s.sqrt(108))*180/pi),unit='degrees',tol=.51),why='s=3−t and3+t²=s² give t=1,s=2. Tangents(1,−1,2),(−1,1,4) have dot product6 and norm product sqrt108.')
ints={35:([t,-t**3,3*t**5],0,2),36:([2*t**R(3,2),0,(t+1)*s.sqrt(t)],1,4),37:([1/(t+1),1/(t*t+1),t/(t*t+1)],0,1),38:([s.sec(t)*s.tan(t),t*s.cos(2*t),s.sin(2*t)**2*s.cos(2*t)],0,pi/4)}
for k,(r0,lo,hi) in ints.items():
 vals=[s.integrate(z,(t,lo,hi)) for z in r0];row(k,*V(vals,'Integral'),why='Integrate every component over the same interval.');CASES.append(dict(kind='definite',n=k,r=list(map(str,r0)),lo=str(lo),hi=str(hi),expected=list(map(str,vals))))
for k,r0,pr in [(39,[s.sec(t)**2,t*(t*t+1)**3,t*t*s.log(t)],[s.tan(t),(t*t+1)**4/8,t**3*s.log(t)/3-t**3/9]),(40,[t*s.exp(2*t),t/(1-t),1/s.sqrt(1-t*t)],[s.exp(2*t)*(2*t-1)/4,-t-s.log(s.Abs(1-t)),s.asin(t)])]:
 row(k,*[f('Antiderivative · '+axis,z,constant=True) for axis,z in zip('xyz',pr)],why='Each component has its own arbitrary constant; restrict to connected intervals of the original real domain.');CASES.append(dict(kind='primitive',n=k,r=list(map(str,r0)),expected=list(map(str,pr))))
for k,d0,t0,p in [(41,[2*t,3*t*t,s.sqrt(t)],1,[1,1,0]),(42,[t,s.exp(t),t*s.exp(t)],0,[1,1,1])]:
 pr=vec([s.integrate(z,t) for z in d0]);r0=pr-pr.subs(t,t0)+vec(p);row(k,*V(r0,'r(t)'),why='Integrate componentwise, then use all three initial-position components.');CASES.append(dict(kind='initial',n=k,r=list(map(str,d0)),at=str(t0),position=list(map(str,p)),expected=list(map(str,r0))))
proofs={43:('(u+v)′=u′+v′','Apply the scalar sum rule in each coordinate.'),44:('(fu)′=f′u+fu′','Apply the scalar product rule in each coordinate.'),45:('(u×v)′=u′×v+u×v′','Differentiate the determinant components without reversing cross-product order.'),46:('(u(f(t)))′=f′(t)u′(f(t))','Apply the scalar chain rule to each coordinate.'),51:('r×r′=ω(a×b)','Expand and use a×a=b×b=0, b×a=−a×b, cos²+sin²=1.'),52:('r″=−ω²r','Differentiate each trigonometric coefficient twice.'),53:('(r×r′)′=r′×r′+r×r″=r×r″','A vector crossed with itself is zero.'),54:('u′·(v×w)+u·(v′×w)+u·(v×w′)','Use the dot-product rule and the cross-product rule.'),55:('d|r|/dt=(r·r′)/|r|, when |r|>0','Differentiate |r|²=r·r and divide by2|r|.'),56:('|r|² is constant, so the curve lies on a sphere centered at0','The derivative of |r|² is2r·r′=0 on the parameter interval.'),57:('u′=r·(r′×r‴)','Product-rule terms with two equal vectors have zero scalar triple product.'),58:('For h>0 the chord points forward; for h<0 both chord and divisor reverse, so the limit still points toward increasing t','Use the orientation of difference quotients; a unit tangent requires a nonzero derivative.')}
for k,(ans,why) in proofs.items():row(k,c('Identity / proof conclusion',ans,'Reverse the sign of the displayed identity','The conclusion follows without differentiability assumptions'),limited=True,why=why)
u0=vec([s.sin(t),s.cos(t),t]);v0=vec([t,s.cos(t),s.sin(t)])
row(47,f('Derivative of u·v',s.diff(u0.dot(v0),t)))
row(48,*V(s.simplify(u0.diff(t).cross(v0)+u0.cross(v0.diff(t))),'Derivative of u×v'))
uval=vec([1,2,-1]);du=vec([3,0,4]);vval=vec([2,4,8]);dv=vec([1,4,12]);row(49,n('f′(2)',du.dot(vval)+uval.dot(dv)))
row(50,*V(du.cross(vval)+uval.cross(dv),'r′(2)'))
from pathlib import Path
HERE=Path(__file__).parent
(HERE/'section02.json').write_text(json.dumps(A.out,ensure_ascii=False,indent=2)+'\n');(HERE/'section02-audit.json').write_text(json.dumps(dict(notes=A.notes,cases=CASES),ensure_ascii=False,indent=2)+'\n');print('13.2',len(A.out))
