from common import *
from scipy.integrate import dblquad,quad
row=lambda k,*fs,**kw:A.row(6,k,*fs,**kw)
row(1,c('P','On surface at(u,v)=(1,3)','Not on surface'),c('Q','Not on surface: first two coordinates force(u,v)=(4/3,−4/3), giving z=17/3','On surface at(u,v)=(2,−2)'))
row(2,c('P','Not on surface: x=1 forcesu=v and hencez=0','On surface'),c('Q','On surface at(u,v)=(2,1)','Not on surface'))
for k,ans in {3:'Plane z=4x−y+4',4:'Circular paraboloid x=y²+z², opening toward+x',5:'Double cone z²=x²+y²',6:'Elliptic cylinder x²/9+z²=1 with−1≤y≤1'}.items():row(k,c('Surface',ans,'Unit sphere','Plane z=0'))
param={7:[u*u,v*v,u+v],8:[u,v**3,-v],9:[u**3,u*s.sin(v),u*s.cos(v)],10:[u,s.sin(u+v),s.sin(v)],11:[s.sin(v),s.cos(u)*s.sin(4*v),s.sin(2*u)*s.sin(4*v)],12:[s.cos(u),s.sin(u)*s.sin(v),s.cos(v)],13:[u*s.cos(v),u*s.sin(v),v],14:[u*v*v,u*u*v,u*u-v*v],15:[u**3-u,v*v,u*u],16:[(1-u)*(3+s.cos(v))*s.cos(4*pi*u),(1-u)*(3+s.cos(v))*s.sin(4*pi*u),3*u+(1-u)*s.sin(v)],17:[s.cos(u)**3*s.cos(v)**3,s.sin(u)**3*s.cos(v)**3,s.sin(v)**3],18:[s.sin(u),s.cos(u)*s.sin(v),s.sin(v)]}
for k in range(7,19):
 r0=param[k];fs=[]
 if k>=13:
  ans={13:'IV',14:'VI',15:'I',16:'V',17:'III',18:'II'}[k];fs.append(c('Graph',ans,*[a for a in ['I','II','III','IV','V','VI'] if a!=ans]))
 # Check the precise constant-parameter family rather than a generic plot assertion.
 fs += [cv('u=0 grid curve (v varies)',[s.simplify(e.subs(u,0)) for e in r0]),cv('v=0 grid curve (u varies)',[s.simplify(e.subs(v,0)) for e in r0])]
 row(k,*fs,limited=True,why='Hold one parameter constant and vary the other within the source bounds. These checks identify grid curves; the entire plotted surface is not automatically assessed.')
reps={19:([u,-u+v,-v],'u,v∈R'),20:([2*u-3*v,-1+u+2*v,5+4*u+5*v],'u,v∈R'),21:([s.sqrt(1+u*u+v*v/4),u,v],'u,v∈R; positive x-sheet'),22:([u,-s.sqrt((1-u*u-3*v*v)/2),v],'u²+3v²≤1; y≤0'),23:([2*s.sin(u)*s.cos(v),2*s.sin(u)*s.sin(v),2*s.cos(u)],'0≤u≤π/4,0≤v≤2π'),24:([3*s.cos(u),v,3*s.sin(u)],'0≤u≤π,−4≤v≤4'),25:([6*s.sin(u)*s.cos(v),6*s.sin(u)*s.sin(v),6*s.cos(u)],'π/6≤u≤π/2,0≤v≤2π'),26:([u*s.cos(v),u*s.sin(v),3+u*s.cos(v)],'0≤u≤1,0≤v≤2π'),29:([u,s.cos(v)/(1+u*u),s.sin(v)/(1+u*u)],'−2≤u≤2,0≤v≤2π'),30:([s.cos(v)/u,u,s.sin(v)/u],'u≥1,0≤v≤2π')}
for k,(r0,dom) in reps.items():row(k,cv('One parametrization',r0),c('Parameter region',dom,'u=v=0 only','All real parameters with no restriction'),limited=k>=29,why='Substitute the parametrization into the defining equation and impose the source inequalities.')
row(27,c('Surface and grid','A parabolic cylinder: use a parabola in the xz-plane and straight generators parallel to the y-axis','A closed sphere','A cone with circular cross sections'),cv('One parametrization reproducing the illustrated shape',[5*(1-v*v/9),u,v]),c('One matching plotting window','−3≤u≤0,−3≤v≤3; adjust view to the source','0≤u,v≤1 only','No parameter restrictions needed'),limited=True,why='This is one reproducible graph resembling the source illustration, not a unique equation inferred from an unlabeled surface. The actual plotted output still needs visual review.')
row(28,c('Surface and grid','A sphere patch: latitude circles and meridian arcs with polar angle restricted to omit the cap shown','A planar disk','A cylinder with straight meridians'),cv('One sphere-patch parametrization',[s.sin(u)*s.cos(v),s.sin(u)*s.sin(v),s.cos(u)]),c('One plotting window resembling the cut shown','π/4≤u≤π,0≤v≤2π','0≤u≤π/4 only','u=0 only'),limited=True,why='The cutoff π/4 is a chosen plotting setting that resembles the pictured open top, not a uniquely specified source value. Adjust the viewpoint and mesh to reproduce the image.')
row(31,c('a · Exchange sin and cos','Reflect across plane x=y, reversing the spiral handedness','No geometric change','Double the number of turns'),c('b · Double the angular argument','Twice as many turns over the same u-range, with reduced pitch','Half as many turns','Only the tube radius doubles'),limited=True)
row(32,c('Unusual property','One-sided nonorientable band with a half twist and one boundary component','Two disjoint sides and two boundary components','Closed sphere without a boundary'),limited=True)
tans={33:([u+v,3*u*u,u-v],1,1),34:([u*u+1,v**3+1,u+v],2,1),35:([u*s.cos(v),u*s.sin(v),v],1,pi/3),36:([s.sin(u),s.cos(u)*s.sin(v),s.sin(v)],pi/6,pi/6),37:([u*u,2*u*s.sin(v),u*s.cos(v)],1,0),38:([1-u*u-v*v,v,u],-1,-1)}
for k,(r0,ua,va) in tans.items():
 r0=vec(r0);p=r0.subs({u:ua,v:va});N=r0.diff(u).cross(r0.diff(v)).subs({u:ua,v:va});e=s.expand(N.dot(vec([x,y,z])-p));row(k,f('Tangent plane: expression equal to zero',e),limited=k>=37,why='Normal r_u×r_v at the specified point; plane N·((x,y,z)−r₀)=0. Scalar multiples represent the same plane.')
# Plane choices require additive offsets, not scalar multiples.
for k in tans:
 field=A.out[f'calculus-section-16-6-{k}']['grader'];ans=field['answer'];field['options']=[ans,ans+' + 1',ans+' − 1']
area={39:3*s.sqrt(14),40:4*s.sqrt(22),41:pi*s.sqrt(14),42:s.sqrt(2)/6,43:s.integrate(s.sqrt(1+x+y),(y,0,1),(x,0,1)),44:s.integrate(x*s.sqrt(2+16*x*x),(x,0,1)),45:2*pi*(2*s.sqrt(2)-1)/3,46:2*s.integrate(s.sqrt(2+4*z*z),(z,0,2)),47:pi*(65*s.sqrt(65)-1)/6,48:pi*(s.sqrt(2)+s.log(1+s.sqrt(2)))/2,49:R(11,3),52:integral(2*pi*t*s.sqrt(1+4*t*t*s.sin(t*t)**2),0,1),53:integral(2*pi*t*s.sqrt(1+4*t*t/(t*t+2)**2),0,1),57:3*s.integrate(s.sqrt(5+(3+8*y)**2),(y,0,1)),61:4*pi,62:16}
# x=u²,y=uv,z=v²/2 has crossproduct magnitude 2u²+v²; integral 0..1,0..2 =4.
area[49]=4
for k,val in area.items():row(k,n('Surface area',val,tol=.000051 if k in(52,53) else None),why='Integrate |r_u×r_v| over the parameter domain, or sqrt(1+f_x²+f_y²) over the projected graph domain.')
a,b,rho=s.symbols('a b rho',positive=True)
row(50,f('Area of both spherical caps',4*pi*b*(b-s.sqrt(b*b-a*a))))
row(51,c('Area bound','πR²≤A(S)≤√3πR²','A(S)=πR² always','A(S)≤πR²'),limited=True)
def area_graph(fun,xl,xu,yl,yu):
 e=s.sqrt(1+s.diff(fun,x)**2+s.diff(fun,y)**2);fn=s.lambdify((y,x),e,'numpy');return dblquad(fn,xl,xu,yl,yu,epsabs=1e-9)[0]
val54=4*area_graph((1+x*x)/(1+y*y),0,1,lambda x:0,lambda x:1-x)
row(54,n('Surface area',val54,tol=.000051),c('Graph domain','Diamond with vertices(±1,0),(0,±1)','Unit disk','Square[0,1]²'),limited=True)
fun=1/(1+x*x+y*y);e=s.sqrt(1+s.diff(fun,x)**2+s.diff(fun,y)**2)
mid=sum(4*e.subs({x:xx,y:yy}) for xx in(1,3,5) for yy in(1,3))
row(55,n('a · Six-square midpoint estimate',mid),n('b · Numerical area',area_graph(fun,0,6,lambda x:0,lambda x:4),tol=.000051),c('Comparison','Midpoint estimate is smaller than the numerical area','Midpoint estimate is larger','Exactly equal'),limited=True)
r0=vec(param[17]);J=s.simplify(norm(r0.diff(u).cross(r0.diff(v))));fn=s.lambdify((v,u),J,'numpy');val56=8*dblquad(fn,0,float(pi/2),lambda u:0,lambda u:float(pi/2),epsabs=1e-9)[0]
row(56,n('Surface area',val56,tol=.000051),why='Integrate on one smooth octant and multiply by8; the stated parameter rectangle covers the surface once apart from seam degeneracies.')
row(58,c('a · Parameter-area integral','∫₀²π∫₀² u√(a²b²+4u²(b²cos²v+a²sin²v)) du dv','∫₀²π∫₀² ab du dv','∫₀²π∫₀² u² du dv'),c('b · Graph and area','z=x²/a²+y²/b²; ∬D√(1+4x²/a⁴+4y²/b⁴)dA, D:x²/a²+y²/b²≤4','z=x²+y²;D is always unit disk','z=x/a+y/b'),c('c · a=2,b=3 geometry','Elliptic paraboloid truncated at z=4; x-semiaxis4 and y-semiaxis6','Sphere radius4','Cone with height4'),n('d · Numerical area',dblquad(lambda u,v:u*math.sqrt(36+4*u*u*(9*math.cos(v)**2+4*math.sin(v)**2)),0,2*math.pi,lambda v:0,lambda v:2)[0],tol=.000051),limited=True)
row(59,c('a · Surface identity','x²/a²+y²/b²+z²/c²=1','x²/a²+y²/b²−z²/c²=1','x²+y²+z²=1 for all a,b,c'),c('b · Semiaxes','1,2,3 along x,y,z','3,2,1 along x,y,z','All semiaxes equal1'),c('c · Area integral','∫₀²π∫₀π sin u√(36sin²u cos²v+9sin²u sin²v+4cos²u)du dv','∫₀²π∫₀π 6sin u du dv','∫₀²π∫₀π 36du dv'),limited=True)
row(60,c('a · Surface identity','x²/a²+y²/b²−z²/c²=1','x²/a²+y²/b²+z²/c²=1','z=x²+y²'),c('b · Shape','One-sheet hyperboloid, waist ellipse semiaxes1 and2 at z=0','Two-sheet hyperboloid','Ellipsoid'),c('c · Area integral','∫₀²π∫₋asinh1^asinh1 cosh u√(36cosh²u cos²v+9cosh²u sin²v+4sinh²u)du dv','Same integral with−π≤u≤π','∫₀²π∫₋₁¹ 6du dv'),limited=True)
row(63,f('Area',2*a*a*(pi-2)),why='Both hemispheres: polar projection 0≤r≤a cosθ, −π/2≤θ≤π/2; dS=2a r/√(a²−r²)drdθ.')
row(64,c('a · Parametrization','⟨(b+a cosα)cosθ,(b+a cosα)sinθ,a sinα⟩;0≤θ,α≤2π','⟨b cosθ,a sinθ,α⟩','⟨a cosθ,a sinθ,b⟩'),c('b · Shape','Ring torus for0<a<b; tube radiusa and major radiusb','Sphere radiusa+b','Cone'),f('c · Surface area',4*pi*pi*a*b),limited=True)
savepart('section06')
