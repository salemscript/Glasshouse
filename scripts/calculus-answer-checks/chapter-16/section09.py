from common import *
row=lambda k,*fs,**kw:A.row(9,k,*fs,**kw)
vals={1:R(9,2),2:2430*pi,3:256*pi/3,4:36*pi,5:R(9,2),7:9*pi/2,8:384*pi/5,9:0,11:pi,12:-12*pi,13:2*pi,16:19*pi*pi/64,17:13*pi/20,18:3*pi/2,24:4*pi/3}
for k,val in vals.items():row(k,*([n('Outward flux',val),n('Volume integral of divergence',val)] if k<=4 else [n('Flux / integral',val)]),limited=k<=4 or k==16,why='Use outward orientation and integrate divF over the enclosed solid. For an open surface, close it with a disk and subtract the added disk flux.')
a,b,cc,rr=s.symbols('a b c R',positive=True)
row(6,f('Flux',3*a*a*b*b*cc*cc/4))
row(10,f('Flux',a*b*cc*(a+4)/24))
row(14,f('Flux',4*pi*rr**5))
formal=s.integrate(s.sqrt(3-x*x)*(R(18,5)-2*x**4),(x,-1,1))
row(15,c('Domain and ordinary flux','As printed, F is singular at z=π/2 inside this solid; the ordinary surface integral and standard Divergence Theorem are not applicable','F is smooth throughout the solid','The singularity is outside the solid'),n('Formal volume integral of divF (not an ordinary flux justification)',formal),limited=True,why='The printed tan z term has poles intersecting the surface and interior. Integrating the formal divergence√(3−x²) gives a finite candidate, but that does not repair the missing regularity. An explicit principal-value convention or corrected field would be needed.')
row(19,c('P₁ divergence','Negative','Positive','Zero'),c('P₂ divergence','Positive','Negative','Zero'),limited=True)
row(20,c('a · P₁','Source','Sink'),c('a · P₂','Sink','Source'),f('b · Divergence',1+2*y),limited=True)
row(21,f('Divergence',3*y),c('Sign regions','Positive for y>0, negative for y<0, zero on y=0','Positive for x>0, negative for x<0','Always positive'),limited=True)
row(22,f('Divergence',2*x+2*y),c('Sign regions','Positive above y=−x, negative below, zero on line','Positive above y=x, negative below','Always zero'),limited=True)
row(23,n('Divergence away from origin',0),c('Domain qualification','Formula holds for r>0; the point charge at origin is excluded','Formula holds classically at origin too','Formula holds only on unit sphere'),limited=True)
proofs={25:'Apply divergence theorem to constant vectora: diva=0',26:'div⟨x,y,z⟩=3, so flux=3Volume',27:'div(curlF)=0, so every closed-surface curl flux is0',28:'Dₙf=∇f·n and div∇f=∇²f',29:'div(f∇g)=∇f·∇g+f∇²g',30:'Subtract the product-rule identities; ∇f·∇g cancels',31:'Apply the theorem componentwise to f i,f j,f k, obtaining∬f n=∭∇f',32:'With z measured down,∇p=ρg k; force=−∭∇p=−ρgVolume k=−Wk'}
for k,ans in proofs.items():row(k,c('Identity and decisive reasoning',ans,'The result follows by setting every derivative to zero regardless of the function','The boundary and volume terms have opposite signs for outward normal'),limited=True)
savepart('section09')
