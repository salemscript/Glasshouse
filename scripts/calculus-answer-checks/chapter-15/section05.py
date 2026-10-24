from common import *
row=lambda k,*fs,**kw:A.row(5,k,*fs,**kw)
vals={1:12*s.sqrt(35),2:25*pi*s.sqrt(14),3:3*s.sqrt(14),4:(27-5*s.sqrt(5))/3,5:pi*(13*s.sqrt(13)-1)/6,6:pi/3,7:pi*(17*s.sqrt(17)-5*s.sqrt(5))/6,8:s.integrate(s.sqrt(1+x+y),(x,0,1),(y,0,1)),9:2*pi*(2*s.sqrt(2)-1)/3,10:4*pi,11:a*a*(pi-2),12:4*pi,17:3*s.integrate(s.sqrt(5+(3+8*y)**2),(y,0,1)),18:2*s.integrate(s.sqrt(2+(1+2*x)**2),(x,-2,1)),23:pi*(101*s.sqrt(101)-1)/6,24:16}
for num,val in vals.items():row(num,f('Area',val) if s.sympify(val).free_symbols else n('Area',val),limited=num==18,why='Integrate sqrt(1+f_x²+f_y²) over the projected region; for a spherical cap use2πRh. For intersecting cylinders sum all four symmetric patches.')
for num,expr in [(13,2*pi*r*s.sqrt(1+4*r*r/(1+r*r)**4)),(14,2*pi*r*s.sqrt(1+4*r*r*s.sin(r*r)**2))]:
 fun=s.lambdify(r,expr,'mpmath');value=mp.quad(fun,[0,1]);row(num,c('Single integral','∫[0,1] '+fmt(expr)+' dr','∫[0,1] '+fmt(expr/2)+' dr','∫[0,1] '+fmt(expr*2)+' dr'),n('Area',value,tol=.000051))
for num,L,expr in [(15,1,s.sqrt(1+4*x*x+4*y*y)),(16,2,s.sqrt(1+(y+2*x)**2+(x+2*y)**2))]:
 fun=s.lambdify((x,y),expr,'mpmath');val=mp.quad(lambda xx:mp.quad(lambda yy:fun(xx,yy),[0,L]),[0,L]);mid=sum(expr.subs({x:xx,y:yy}) for xx in[R(L,4),R(3*L,4)] for yy in[R(L,4),R(3*L,4)])*R(L*L,4)
 row(num,n('a · Midpoint estimate',mid),n('b · Area',val,tol=.000051),c('Comparison','Midpoint estimate is slightly smaller than the numerical integral','Midpoint estimate is larger','They are exactly equal'),limited=True)
val=mp.quad(lambda rr:mp.quad(lambda tt:mp.sqrt(1+4*rr**6*mp.cos(tt)**2*mp.sin(tt)**2)*rr,[0,mp.pi/2]),[0,1])*4
row(19,n('Area',val,tol=.000051),why='Forz=1+x²y², f_x²+f_y²=4x²y²(x²+y²); use polar coordinates and quadrant symmetry.')
val=4*mp.quad(lambda xx:mp.quad(lambda yy:mp.sqrt(1+(2*xx/(1+yy*yy))**2+(2*yy*(1+xx*xx)/(1+yy*yy)**2)**2),[0,1-xx]),[0,1])
row(20,n('Area',val,tol=.000051),c('Plot domain','Diamond |x|+|y|≤1; z=(1+x²)/(1+y²)','Diskx²+y²≤1','Square[−1,1]²'),limited=True)
row(21,c('Surface area','sqrt(1+a²+b²) A(D)','(1+a+b) A(D)','A(D)/(1+a²+b²)'),limited=True,why='The partial derivatives are the constantsa,b, so the area multiplier is constant.')
row(22,c('Hemisphere integral over radius t','2πa(a−sqrt(a²−t²))','πa(a−sqrt(a²−t²))','2πat²'),f('Full sphere area',4*pi*a*a),limited=True,why='The upper hemisphere area tends to2πa² as t→a from below; double it.')
save('section05')
