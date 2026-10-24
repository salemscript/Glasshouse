from common import *
from scipy.integrate import dblquad
row=lambda k,*fs,**kw:A.row(7,k,*fs,**kw)
plane=[u+v,u-v,1+2*u+v];helix=[u*s.cos(v),u*s.sin(v),v]
vals={1:8*(s.cos(1)+s.cos(2)+s.cos(3)),2:18*pi,3:900*pi,4:-80*pi,5:surf(x+y+z,plane,0,2,0,1),6:surf(x*y*z,[u*s.cos(v),u*s.sin(v),u],0,1,0,pi/2),7:surf(y,helix,0,1,0,pi),8:pi*s.sqrt(2)/2,9:171*s.sqrt(14),10:4,11:s.sqrt(21)/3,12:surf(y,[u,v,R(2,3)*(u**R(3,2)+v**R(3,2))],0,1,0,1),13:surf(z*z,[u*u,u*s.cos(v),u*s.sin(v)],0,1,0,2*pi),14:625*pi*s.sqrt(2),15:(21**R(3,2)-17**R(3,2))/12,16:pi*(R(2,3)-5*s.sqrt(2)/12),17:16*pi,18:2*pi+4,19:0,20:241*pi,21:surf([z*s.exp(x*y),-3*z*s.exp(x*y),x*y],plane,0,2,0,1,True,-1),22:surf([z,y,x],helix,0,1,0,pi,True),23:surf([x*y,y*z,z*x],[u,v,4-u*u-v*v],0,1,0,1,True),24:surf([-x,-y,z**3],[u*s.cos(v),u*s.sin(v),u],1,3,0,2*pi,True,-1),25:72*pi,26:-32*pi/3,27:0,28:surf([y*z,z*x,x*y],[u,v,u*s.sin(v)],0,2,0,pi,True),29:48,30:4*pi,31:2*pi+R(8,3),32:-R(1,6),33:surf(x*x+y*y+z*z,[u,v,u*s.exp(v)],0,1,0,1),34:surf(x*y*z,[u,v,u*u*v*v],0,1,0,2),35:surf(x*x*y*y*z*z,[s.sqrt(R(3,2))*u*s.cos(v),s.sqrt(3)*u*s.sin(v),3-3*u*u],0,1,0,2*pi),36:surf([s.sin(x*y*z),x*x*y,z*z*s.exp(x/5)],[u,s.cos(v),2*s.sin(v)],-2,2,0,pi,True,-1),40:108*pi*s.sqrt(2),43:0,44:0,47:1248*pi}
# Cylinder closed surface20: lateral124π; caps81π+36π=117π.
# scalar18: x odd; y integral gives2π; z contributes4.
for k,val in vals.items():row(k,n('Surface integral' if k<21 or k in(33,34,35) else 'Mass' if k==40 else 'Flow rate' if k>=43 else 'Flux',val,tol=.000051 if k in(33,35) else None),limited=k==36,why='Use the source orientation. Scalar surface integrals use |r_u×r_v|; flux uses the oriented cross product. Closed-surface flux can be checked independently with the divergence theorem.')
row(37,c('Leftward normal formula','∬[P h_x−Q+R h_z]dx dz, with F evaluated at(x,h(x,z),z)','∬[−P h_x+Q−R h_z]dx dz','∬[P+Q+R]dx dz'),limited=True)
row(38,c('Forward normal formula','∬[P−Q k_y−R k_z]dy dz, with F evaluated at(k(y,z),y,z)','∬[−P+Q k_y+R k_z]dy dz','∬[P+Q+R]dy dz'),limited=True)
a,k,K,C,eps,cc=s.symbols('a k K C epsilon_0 c',positive=True)
row(39,n('x̄',0),n('ȳ',0),f('z̄',a/2),why='Uniform thin hemispherical surface: z-average is a/2, unlike solid-hemisphere3a/8.')
row(41,c('a · Moment integral','I_z=∬S(x²+y²)ρdS','I_z=∬Sz²ρdS','I_z=∬SρdS'),n('b · Funnel moment',2*pi*s.sqrt(2)*(R(10,4)*(4**4-1)-R(1,5)*(4**5-1))))
row(42,n('a · x̄',0),n('a · ȳ',0),n('a · z̄',R(9,2)),f('b · I_z',R(140,3)*pi*k),why='Sphere radius5 cap4≤z≤5: dS=5dθdz, x²+y²=25−z².')
row(45,f('Enclosed charge',R(8,3)*pi*a**3*eps),why='divE=4; hemisphere volume2πa³/3; charge=ε₀flux.')
row(46,f('Enclosed charge',16*eps),why='divE=2+2z; cube odd-z term cancels, volume8.')
row(48,f('Outward heat flow for u=C/r',4*pi*K*C),why='−K∇u=KC r-vector/r³; multiply normal componentKC/a² by4πa².')
row(49,f('Flux',4*pi*cc),c('Radius dependence','Independent of radius because inverse-square normal field cancels sphere area','Proportional to radius','Inversely proportional to radius'),limited=True)
qid='calculus-section-16-7-8'
A.out[qid]['grader']['explanation']='The image is the cone z=√(x²+y²),0≤z≤1. The given(u,v)disk parametrization covers it twice. Integrate geometrically once: √2∫₀²π∫₀¹r³drdθ=π/√2. Integrating over the full parameter disk without dividing by2 would count the surface twice.'
A.notes[qid]=A.out[qid]['grader']['explanation']
for k in(43,44):A.out[f'calculus-section-16-7-{k}']['grader']['unit']='kg/s'
savepart('section07')
