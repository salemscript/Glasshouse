from common import *
row=lambda k,*fs,**kw:A.row(6,k,*fs,**kw)
cases={1:(x*y*z*z,[(y,-1,2),(z,0,3),(x,0,1)]),2:(x*y+z*z,[(z,0,3),(y,0,1),(x,0,2)]),3:(2*x-y,[(x,0,y-z),(y,0,z*z),(z,0,2)]),4:(6*x*y,[(z,0,x+y),(x,y,2*y),(y,0,1)]),5:(x*s.exp(-y),[(y,0,s.log(x)),(x,0,2*z),(z,1,2)]),6:(z/(y+1),[(x,0,s.sqrt(1-z*z)),(z,0,1),(y,0,1)]),7:(z*s.sin(x),[(y,0,s.sqrt(1-z*z)),(z,0,1),(x,0,pi)]),8:(x*y*s.exp(z),[(z,0,2-x*x-y*y),(y,0,1),(x,0,1)]),9:(y,[(z,x-y,x+y),(y,0,x),(x,0,3)]),10:(s.exp(z/y),[(z,0,x*y),(x,y,1),(y,0,1)]),11:(z/(x*x+z*z),[(x,0,z),(z,y,4),(y,1,4)]),12:(s.sin(y),[(z,0,x),(x,0,pi-y),(y,0,pi)]),13:(6*x*y,[(z,0,1+x+y),(y,0,s.sqrt(x)),(x,0,1)]),14:(x-y,[(z,x*x-1,1-x*x),(y,0,2),(x,-1,1)]),15:(y*y,[(z,0,2-x-y),(y,0,2-x),(x,0,2)]),16:(x*z,[(x,0,z-y),(y,0,z),(z,0,1)]),17:(x*r,[(x,4*r*r,4),(r,0,1),(theta,0,2*pi)]),18:(z,[(x,0,y/3),(z,0,s.sqrt(9-y*y)),(y,0,3)]),19:(s.Integer(1),[(z,0,4-2*x-y),(y,0,4-2*x),(x,0,2)]),20:(r,[(y,r*r,8-r*r),(r,0,2),(theta,0,2*pi)]),21:(s.Integer(1),[(z,0,1-y),(y,x*x,1),(x,-1,1)]),22:(r,[(y,-1,4-r*s.sin(theta)),(r,0,2),(theta,0,2*pi)])}
for num,(expr,bounds) in cases.items():integral(6,num,expr,bounds,label='Volume' if num>=19 else 'Integral')
# The three orders requested in2 all have independent rectangular bounds.
entry=A.out['calculus-section-15-6-2']; old=entry['grader'];fields=[old,c('Three equivalent orders','∫₀²∫₀¹∫₀³ (xy+z²) dz dy dx; ∫₀³∫₀²∫₀¹ (xy+z²) dy dx dz; ∫₀¹∫₀³∫₀² (xy+z²) dx dz dy','All variables range from0 to1','All variables range from0 to3')];entry['grader']={'type':'parts','parts':fields,'scope':old['scope']};entry['objectiveFieldCount']=2
row(23,c('a · Volume integral','∫[0,1]∫[y,1]∫[0,sqrt(1−y²)] dz dx dy','∫[0,1]∫[0,y]∫[0,1] dz dx dy','∫[0,1]∫[0,1]∫[0,1] dz dx dy'),n('b · Volume',pi/4-R(1,3)))
mid=8*sum(s.sqrt(xx*xx+yy*yy+zz*zz) for xx in[1,3] for yy in[1,3] for zz in[1,3])
from scipy.integrate import tplquad
val=tplquad(lambda zz,yy,xx:math.sqrt(xx*xx+yy*yy+zz*zz),0,4,lambda xx:0,lambda xx:4,lambda xx,yy:0,lambda xx,yy:4,epsabs=1e-6)[0]
row(24,n('a · Midpoint estimate',mid),n('b · Integral to nearest integer',round(val),tol=.51),c('Comparison','Midpoint estimate is lower','Midpoint estimate is higher','They agree exactly'),limited=True)
row(25,n('Midpoint estimate',sum(s.cos(xx*yy*zz) for xx in[R(1,4),R(3,4)] for yy in[R(1,4),R(3,4)] for zz in[R(1,4),R(3,4)])/8))
row(26,n('Midpoint estimate',sum(s.sqrt(xx)*s.exp(xx*yy*zz) for xx in[1,3] for yy in[R(1,4),R(3,4)] for zz in[R(1,2),R(3,2)])))
row(27,c('Solid','First-octant wedge: x+z≤1 and y+2z≤2','Unit cube','Unit sphere'),limited=True)
row(28,c('Solid','0≤y≤2, 0≤z≤2−y, 0≤x≤4−y²','A full cylinder','A sphere of radius2'),limited=True)
orders={
29:{'dy dz dx':'x:−2..2; z:−sqrt(4−x²)/2..sqrt(4−x²)/2; y:0..4−x²−4z²','dy dx dz':'z:−1..1; x:−2sqrt(1−z²)..2sqrt(1−z²); y:0..4−x²−4z²','dx dy dz':'z:−1..1; y:0..4−4z²; x:−sqrt(4−y−4z²)..sqrt(4−y−4z²)','dx dz dy':'y:0..4; z:−sqrt(4−y)/2..sqrt(4−y)/2; x:−sqrt(4−y−4z²)..sqrt(4−y−4z²)','dz dy dx':'x:−2..2; y:0..4−x²; z:−sqrt(4−x²−y)/2..sqrt(4−x²−y)/2','dz dx dy':'y:0..4; x:−sqrt(4−y)..sqrt(4−y); z:−sqrt(4−x²−y)/2..sqrt(4−x²−y)/2'},
30:{'dx dy dz':'z:−3..3; y:−sqrt(9−z²)..sqrt(9−z²); x:−2..2','dx dz dy':'y:−3..3; z:−sqrt(9−y²)..sqrt(9−y²); x:−2..2','dy dx dz':'z:−3..3; x:−2..2; y:−sqrt(9−z²)..sqrt(9−z²)','dy dz dx':'x:−2..2; z:−3..3; y:−sqrt(9−z²)..sqrt(9−z²)','dz dx dy':'y:−3..3; x:−2..2; z:−sqrt(9−y²)..sqrt(9−y²)','dz dy dx':'x:−2..2; y:−3..3; z:−sqrt(9−y²)..sqrt(9−y²)'},
31:{'dz dy dx':'x:−2..2; y:x²..4; z:0..(4−y)/2','dy dz dx':'x:−2..2; z:0..(4−x²)/2; y:x²..4−2z','dx dz dy':'y:0..4; z:0..(4−y)/2; x:−sqrt(y)..sqrt(y)','dx dy dz':'z:0..2; y:0..4−2z; x:−sqrt(y)..sqrt(y)','dy dx dz':'z:0..2; x:−sqrt(4−2z)..sqrt(4−2z); y:x²..4−2z','dz dx dy':'y:0..4; x:−sqrt(y)..sqrt(y); z:0..(4−y)/2'},
32:{'dz dy dx':'x:0..2; y:2−x..2; z:0..(x+y−2)/2','dz dx dy':'y:0..2; x:2−y..2; z:0..(x+y−2)/2','dy dz dx':'x:0..2; z:0..x/2; y:2+2z−x..2','dx dz dy':'y:0..2; z:0..y/2; x:2+2z−y..2','dy dx dz':'z:0..1; x:2z..2; y:2+2z−x..2','dx dy dz':'z:0..1; y:2z..2; x:2+2z−y..2'},
33:{'dz dx dy':'y:0..1; x:0..y²; z:0..1−y','dx dz dy':'y:0..1; z:0..1−y; x:0..y²','dx dy dz':'z:0..1; y:0..1−z; x:0..y²','dy dx dz':'z:0..1; x:0..(1−z)²; y:sqrt(x)..1−z','dy dz dx':'x:0..1; z:0..1−sqrt(x); y:sqrt(x)..1−z'},
34:{'dz dy dx':'x:0..1; y:0..1−x; z:0..1−x²','dy dx dz':'z:0..1; x:0..sqrt(1−z); y:0..1−x','dz dx dy':'y:0..1; x:0..1−y; z:0..1−x²','dx dy dz':'Sum: z:0..1,y:0..1−sqrt(1−z),x:0..sqrt(1−z); plus z:0..1,y:1−sqrt(1−z)..1,x:0..1−y','dx dz dy':'Sum: y:0..1,z:0..2y−y²,x:0..1−y; plus y:0..1,z:2y−y²..1,x:0..sqrt(1−z)'},
35:{'dz dy dx':'x:0..1; y:0..x; z:0..y','dx dz dy':'y:0..1; z:0..y; x:y..1','dx dy dz':'z:0..1; y:z..1; x:y..1','dy dx dz':'z:0..1; x:z..1; y:z..x','dy dz dx':'x:0..1; z:0..x; y:z..x'},
36:{'dy dx dz':'z:0..1; x:0..z; y:0..z','dx dy dz':'z:0..1; y:0..z; x:0..z','dy dz dx':'x:0..1; z:x..1; y:0..z','dz dy dx':'Sum: x:0..1,y:0..x,z:x..1; plus x:0..1,y:x..1,z:y..1','dz dx dy':'Sum: y:0..1,x:0..y,z:y..1; plus y:0..1,x:y..1,z:x..1'}}
for num,os in orders.items():
 row(num,*[c(order+' · Bounds listed outermost first',ans,'Use these bounds but replace f by−f','Use these bounds but replace f by2f') for order,ans in os.items()],limited=True,why='Each selected bound set specifies an iterated integral of f in the named order; bounds are listed outermost to innermost. Split sums are necessary when the active bounding surface changes.')
row(37,n('Integral',64*pi),why='The yz² term is odd in y; constant4 times cylinder volume16π remains.')
row(38,n('Integral',4*pi),why='Odd termsz³ and siny cancel on the unit ball.')
def solid(num,density,bounds,X=x,Y=y,Z=z,J=1,inertia=False,tol=None):
 vals=[s.simplify(s.integrate(density*J*mult,*bounds)) for mult in[1,X,Y,Z,X*X+Y*Y]]
 m0=vals[0];results=[m0,*[t/m0 for t in vals[1:4]]]+([vals[4]] if inertia else[])
 labels=['Mass','Center · x','Center · y','Center · z','I_z'];fields=[f(label,s.simplify(vv)) if vv.free_symbols else n(label,vv,tol=tol) for label,vv in zip(labels,results)]
 row(num,*fields,why='Use mass=∫ρdV and coordinate moments divided by mass. I_z=∫(x²+y²)ρdV.')
 A.integrals.append(dict(id=f'6.{num}',density=str(density),coordinates=list(map(str,[X,Y,Z])),jacobian=str(J),bounds=[[str(t) for t in q] for q in bounds],mass=str(m0),moments=list(map(str,vals[1:]))))
solid(39,3,[(z,0,1-r*r),(r,0,1),(theta,0,2*pi)],r*s.cos(theta),r*s.sin(theta),z,r)
solid(40,4,[(x,0,1-z),(z,0,1-y*y),(y,-1,1)])
solid(41,x*x+y*y+z*z,[(x,0,a),(y,0,a),(z,0,a)])
solid(42,y,[(z,0,1-x-y),(y,0,1-x),(x,0,1)])
L,M,c0=s.symbols('L M c',positive=True)
row(43,*[f('I_'+ax,R(2,3)*k*L**5) for ax in['x','y','z']])
row(44,f('I_x',M*(b*b+c0*c0)/12),f('I_y',M*(a*a+c0*c0)/12),f('I_z',M*(a*a+b*b)/12))
row(45,f('I_z',pi*k*h*a**4/2))
row(46,f('I_z',pi*k*h**5/10))
for num,bounds,dens in[(47,'x:−1..1, y:x²..1, z:0..1−y','sqrt(x²+y²)'),(48,'θ:0..2π, φ:0..π/2, ρ:0..1','ρ')]:
 if num==47:
  mass='∫[−1,1]∫[x²,1]∫[0,1−y] sqrt(x²+y²) dz dy dx';cm='(1/m)∫∫∫ (x,y,z)sqrt(x²+y²) dV over those bounds';iz='∫∫∫(x²+y²)^(3/2)dV over those bounds'
 else:
  mass='∫[0,2π]∫[0,π/2]∫[0,1] ρ³sinφ dρ dφ dθ';cm='x̄=ȳ=0; z̄=(1/m)∫[0,2π]∫[0,π/2]∫[0,1] ρ⁴cosφ sinφ dρ dφ dθ';iz='∫[0,2π]∫[0,π/2]∫[0,1] ρ⁵sin³φ dρ dφ dθ'
 row(num,c('a · Mass setup',mass,'The same integral with density omitted','The same integral with doubled density'),c('b · Center setup',cm,'Divide first moments by volume instead of mass','All coordinates are zero'),c('c · I_z setup',iz,'Use z²ρ instead of(x²+y²)ρ','Use xρ instead of(x²+y²)ρ'),limited=True)
solid(49,1+x+y+z,[(z,0,y),(y,0,s.sqrt(1-x*x)),(x,0,1)],inertia=True)
solid(50,x*x+y*y,[(x,0,y/3),(z,0,s.sqrt(9-y*y)),(y,0,3)],inertia=True,tol=.00051)
row(51,n('a · C',R(1,8)),n('b · Probability',R(1,64)),n('c · Probability',R(1,5760)))
row(52,n('a · C',R(1,100)),n('b · Probability',(1-s.exp(-R(1,2)))*(1-s.exp(-R(1,5)))),n('c · Probability',(1-s.exp(-R(1,2)))*(1-s.exp(-R(1,5)))*(1-s.exp(-R(1,10)))))
row(53,f('Average value',L**3/8))
row(54,n('Average height',R(3,8)))
row(55,c('a · Maximizing region','x²+2y²+3z²≤1','Unit ball','All space'),n('b · Maximum integral',8*pi/(15*s.sqrt(6))),why='Include exactly the positive part of the integrand; transform to the unit ball with Jacobian1/√6.')
for num,ans in[(1,'πr²'),(2,'4πr³/3'),(3,'π²r⁴/2'),(4,'V_n=π^(n/2)r^n/Γ(n/2+1); V_2k=π^k r^(2k)/k!; V_(2k+1)=2^(k+1)π^k r^(2k+1)/(2k+1)!!')]:
 row(num,c('Volume or area formula',ans,'Half of '+ans,'Twice '+ans),limited=True,suffix='-project-discovery-project-volumes-of-hyperspheres-1',why='Slice by one coordinate: V_n(r)=∫[−r,r]V_(n−1)(sqrt(r²−t²))dt. Trigonometric substitution gives the even/odd formulas.')
save('section06')
