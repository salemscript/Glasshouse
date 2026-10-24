from common import *
row=lambda k,*fs,**kw:A.row(4,k,*fs,**kw)
def dbl(expr,yl,yu,xl,xu):return s.integrate(expr,(y,yl,yu),(x,xl,xu))
vals={1:dbl(2*x*y-2*y,0,4,0,5),2:-32*pi,3:dbl(2*x*y**3-x,0,2*x,0,1),4:dbl(y-2*x*x*y,x*x,1,0,1),5:4*(s.exp(3)-1),6:dbl(2*x-2*y,0,1-x/2,0,2),7:R(1,3),8:0,9:-24*pi,10:R(195,2)*pi,11:-R(16,3),12:pi/2,13:4*pi,14:s.log(2)/2,15:0,16:line([2*x-x**3*y**5,x**3*y**8],[s.cos(t),2*s.sin(t)],0,2*pi),17:dbl(y*y-x,0,1-x,0,1),18:625*pi/8,19:3*pi,20:30*pi,21:R(9,2),27:0,28:12}
# Clockwise arch in12 reverses ∫(2x−2y); Green value is +∫cos²x dx=π/2.
for k,val in vals.items():
 fs=[n('a · Direct integral',val),n('b · Green integral',val)] if k<=4 else [n('Line integral' if k not in(19,20,21) else 'Area',val)]
 if k in(15,16):fs=[n('Line integral',val),n('Double integral',val)]
 if k==20:fs.append(c('Epicycloid geometry','Four outward cusps, at(±4,0),(0,±4); traced once on0≤t≤2π','A circle of radius4','Five outward cusps'))
 if k==21:fs=[c('a · Segment integral','x₁y₂−x₂y₁','x₁y₂+x₂y₁','0 for every segment'),c('b · Polygon area','Half the cyclic sumΣ(xᵢyᵢ₊₁−xᵢ₊₁yᵢ), for CCW vertices','The full cyclic sum without1/2','Half the sum of distances between vertices'),n('c · Pentagon area',val)]
 row(k,*fs,limited=k in(15,16,20,21),why='Green’s theorem gives ∮Pdx+Qdy=∬(Q_x−P_y)dA for positive orientation; reverse the sign for clockwise curves.')
row(22,c('Centroid identities','x̄=(∮x²dy)/(2A), ȳ=−(∮y²dx)/(2A)','x̄=(∮x²dx)/(2A),ȳ=(∮y²dy)/(2A)','Both centroid coordinates are zero for every closed curve'),limited=True)
a,b,rho=s.symbols('a b rho',positive=True)
row(23,f('x̄',4*a/(3*pi)),f('ȳ',4*a/(3*pi)))
row(24,f('x̄',2*a/3),f('ȳ',b/3))
row(25,c('Boundary inertia formulas','Iₓ=−ρ∮y³dx/3; Iᵧ=ρ∮x³dy/3','Both formulas use a plus sign','Iₓ=ρ∮ydx;Iᵧ=ρ∮xdy'),limited=True)
row(26,f('Moment about a diameter',rho*pi*a**4/4))
row(29,c('Why integral vanishes','The field is smooth on the enclosed region and Q_x−P_y=0 there; Green gives0','Every closed curve has zero circulation for any field','The origin contributes2π even when outside'),limited=True)
row(30,c('Type-II region derivation','∬Q_xdA=∫[Q(h₂(y),y)−Q(h₁(y),y)]dy=∮Qdy','∬Q_xdA=∮Qdx','Both boundary integrals have the same traversal sign'),limited=True)
row(31,c('Change-of-variables step','Transform∮xdy; Green in(u,v) gives∬(g_u h_v−g_v h_u)dudv; absolute value handles orientation reversal','Jacobian is g_u+h_v','Jacobian is g_u h_u+g_v h_v'),limited=True)
savepart('section04')
