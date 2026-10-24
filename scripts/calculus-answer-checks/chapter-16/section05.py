from common import *
row=lambda k,*fs,**kw:A.row(5,k,*fs,**kw)
fields={1:[x*y*y*z*z,x*x*y*z*z,x*x*y*y*z],2:[0,x**3*y*z*z,y**4*z**3],3:[x*y*s.exp(z),0,y*z*s.exp(x)],4:[s.sin(y*z),s.sin(z*x),s.sin(x*y)],5:[s.sqrt(x)/(1+z),s.sqrt(y)/(1+x),s.sqrt(z)/(1+y)],6:[s.log(2*y+3*z),s.log(x+3*z),s.log(x+2*y)],7:[s.exp(x)*s.sin(y),s.exp(y)*s.sin(z),s.exp(z)*s.sin(x)],8:[s.atan(x*y),s.atan(y*z),s.atan(z*x)]}
for k,F in fields.items():row(k,cv('a · Curl',curl(F)),f('b · Divergence',div(F)),why='curlF=(R_y−Q_z,P_z−R_x,Q_x−P_y); divF=P_x+Q_y+R_z. Differentiate each component on its actual domain.')
for k,d,cr in [(9,'Negative','Zero'),(10,'Positive','Zero'),(11,'Zero','Negative z-direction')]:row(k,c('a · Divergence',d,*[a for a in ['Positive','Negative','Zero'] if a!=d]),c('b · Curl',cr,*[a for a in ['Zero','Positive z-direction','Negative z-direction'] if a!=cr]),limited=True,why='Divergence measures local spreading; curl follows the sign of local counterclockwise rotation.')
ans=['Not defined: curl requires a vector field','Vector field','Scalar field','Vector field (zero)','Not defined in this vector-calculus convention: grad requires a scalar','Vector field','Scalar field','Not defined: div requires a vector field','Vector field','Not defined: div requires a vector field','Not defined: a vector cross scalar is undefined','Scalar field (zero)']
row(12,*[c(chr(97+i)+' · Expression type',a,'Always a nonzero scalar' if 'Scalar' not in a else 'Vector field','Always a nonzero vector' if 'Vector' not in a else 'Not defined') for i,a in enumerate(ans)])
pots={13:x*y*y*z**3,16:x+y*s.sin(z),17:x*s.exp(y*z),18:s.exp(x)*s.sin(y*z)}
for k in range(13,19):
 if k in pots:row(k,c('Conservative?','Yes','No'),f('Potential',pots[k],constant=True))
 else:row(k,c('Conservative?','No','Yes'),c('Cross-partial obstruction','P_y=xz⁴ but Q_x=2xz⁴' if k==14 else 'P_y=−z sin y but Q_x=z sin y','All cross partials agree','Divergence must be zero'))
row(19,c('Can such G exist?','No: divergence of the proposed curl equals1','Yes because every vector field is a curl','Yes because the proposed divergence is0'),limited=True)
row(20,c('Can such G exist?','No: divergence of⟨x,y,z⟩ is3, whereas div(curlG)=0','Yes, G=⟨x²,y²,z²⟩/2','Yes, G=⟨y,z,x⟩'),limited=True)
row(21,c('Curl','Zero: all cross-coordinate derivatives vanish','⟨f′,g′,h′⟩','f′+g′+h′'),limited=True)
row(22,c('Divergence','Zero: P_x=Q_y=R_z=0','f_y+g_z+h_x','Always3'),limited=True)
ident={23:'div(F+G)=divF+divG by linearity of component derivatives',24:'curl(F+G)=curlF+curlG by linearity of component derivatives',25:'div(fF)=f divF+F·∇f by the product rule',26:'curl(fF)=f curlF+(∇f)×F by the product rule',27:'div(F×G)=G·curlF−F·curlG by expanding the determinant and regrouping',28:'div(∇f×∇g)=∇g·curl∇f−∇f·curl∇g=0',29:'curl(curlF)=∇(divF)−∇²F using equality of continuous mixed partials'}
for k,ans in ident.items():row(k,c('Verified identity and key step',ans,'The identity holds only when every field is constant','Replace the final plus sign by minus and the final minus sign by plus'),limited=True)
row(30,n('a · ∇·r',3),c('b · ∇·(r r-vector)','4r','3r','r'),c('c · ∇²(r³)','12r','6r','9r'),limited=True)
row(31,c('a · ∇r','r-vector/r','r-vector/r²','r-vector'),cv('b · ∇×r',[0,0,0]),c('c · ∇(1/r)','−r-vector/r³','r-vector/r³','−r-vector/r²'),c('d · ∇lnr','r-vector/r²','r-vector/r','−r-vector/r²'),limited=True)
row(32,c('Divergence','(3−p)/r^p, r>0','(3+p)/r^p','p/r³'),n('p for zero divergence',3))
row(33,c('Apply flux Green theorem to','f∇g, whose divergence is∇f·∇g+f∇²g','f+g','∇f×∇g'),limited=True)
row(34,c('Derivation','Subtract first identities for(f,g) and(g,f); ∇f·∇g terms cancel','Add the two first identities','Set f=g=0 in the first identity'),limited=True)
row(35,c('Boundary normal integral','0: set f=1 in the first identity and use∇²g=0','Area(D)','Length(C)'),limited=True)
row(36,c('Energy integral','0: set g=f; boundary term vanishes since f=0 on C, and volume term since∇²f=0','Area(D)','Always positive'),limited=True)
row(37,c('a · Velocity','v=w×r, perpendicular to w and r with magnitudeωd','v=w·r','v=r×w'),c('b · Components','⟨−ωy,ωx,0⟩','⟨ωy,−ωx,0⟩','⟨ωx,ωy,0⟩'),c('c · Curl','2w=⟨0,0,2ω⟩','w','−2w'),limited=True)
row(38,*[c(label,ans,'The right side has the opposite sign','The factor is c² instead of1/c²') for label,ans in [('a','curl(curlE)=−E_tt/c²'),('b','curl(curlH)=−H_tt/c²'),('c','∇²E=E_tt/c²'),('d','∇²H=H_tt/c²')]],limited=True,why='Commute time derivatives with curl and substitute Maxwell equations; divE=divH=0 in the curl-curl identity.')
row(39,c('Construction','Every continuous f works: G=(∫₀ˣ f(t,y,z)dt,0,0) has divG=f','Only harmonic f can be a divergence','Only constant f can be a divergence'),limited=True)
savepart('section05')
