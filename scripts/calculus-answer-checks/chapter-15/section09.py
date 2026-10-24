from common import *
row=lambda k,*fs,**kw:A.row(9,k,*fs,**kw)
w,p,q,t0,ss=s.symbols('w p q t s',real=True)
for num,coords,vs in[(1,[2*u+v,4*u-v],[u,v]),(2,[u*u+u*v,u*v*v],[u,v]),(3,[ss*s.cos(t0),ss*s.sin(t0)],[ss,t0]),(4,[p*s.exp(q),q*s.exp(p)],[p,q]),(5,[u*v,v*w,w*u],[u,v,w]),(6,[u+v*w,v+w*u,w+u*v],[u,v,w])]:
 det=s.simplify(s.Matrix(coords).jacobian(vs).det());row(num,f('Signed Jacobian',det) if det.free_symbols else n('Signed Jacobian',det),why='Take the determinant of partial derivatives in the variable order stated in the problem; integration uses its absolute value.')
for num,ans in[(7,'Parallelogram with vertices(0,0),(6,3),(12,1),(6,−2)'),(8,'0≤x≤1,0≤y≤1+x²'),(9,'0≤y≤1,0≤x≤y²'),(10,'Ellipsex²/a²+y²/b²≤1 (a,b nonzero)')]:row(num,c('Image region',ans,'The same unit square in every case','The whole plane'),limited=True)
for num,ans in[(11,'x=(v−u)/3,y=(2v+u)/3; −1≤u≤1,1≤v≤3'),(12,'x=4u−2v,y=3u+v;0≤u≤1,0≤v≤1'),(13,'x=u cosv,y=u sinv;1≤u≤sqrt2,0≤v≤π/2'),(14,'x=sqrt(u/v),y=sqrt(uv);1≤u≤4,1≤v≤4')]:row(num,c('One valid map and rectangular domain',ans,'x=u,y=v on the unit square','x=u+v,y=u+v on a square'),why='Map each pair of boundary curves to constantu or constantv lines; alternate bijective parametrizations may also be valid.')
vals={15:-3,16:192,17:6*pi,18:4*pi/s.sqrt(3),19:2*s.log(3),20:R(3,4),23:R(8,5)*s.log(8),24:(s.exp(6)-7)/4,25:R(3,2)*s.sin(1),26:pi*(1-s.cos(1))/24,27:s.E-1/s.E}
for num,val in vals.items():row(num,n('Integral',val),limited=num==20,why='Transform the boundary curves as stated, replace the area element by the absolute Jacobian, and integrate on the resulting rectangle, triangle, or disk.')
c0,d=s.symbols('c d',positive=True)
row(21,f('a · Ellipsoid volume',4*pi*a*b*c0/3),n('b · Earth volume',4*pi*6378**2*6356/3,'km³'),f('c · I_z',4*pi*k*a*b*c0*(a*a+b*b)/15),why='Scale the unit ball by(a,b,c), giving Jacobianabc; its coordinate second moments each equal4π/15.')
row(22,f('Work(area in pressure-volume plane)',R(5,2)*(b-a)*s.log(d/c0)),why='Setu=xy,v=xy^(7/5). The absolute inverse Jacobian is5/(2v); integratea≤u≤b,c≤v≤d.')
row(28,c('Change of variables and conclusion','u=x+y,v=x;0≤u≤1,0≤v≤u,|J|=1; integral=∫₀¹u f(u)du','u=x+y gives a full unit square','The integral equals∫₀¹f(u)du'),limited=True)
save('section09')
