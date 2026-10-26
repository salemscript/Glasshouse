#!/usr/bin/env python3
"""Source-derived paraxial optics; original diagram/table pages28–37 visually reviewed."""
import math,json,pathlib,gzip,subprocess
from math import sqrt,pi,sin,cos,tan,atan
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[1];rows=[]
def N(l,a,u,w,t=None):return dict(label=l,type='numeric',answer=a,unit=u,tolerance=max(abs(a)*.008,1e-18) if t is None else t,explanation=w)
def C(l,a,b,c,w):return dict(label=l,type='choice',answer=a,options=[a,b,c],explanation=w)
def boolc(l,a,w):return C(l,'Yes' if a else 'No','No' if a else 'Yes','Cannot be determined',w)
def R(n,ps,why,kind='problems',scope=None,assumptions=None,pages=None):
 page=(29 if n<=29 else 30 if n<=40 else 31 if n<=57 else 32 if n<=87 else 33 if n<=93 else 34 if n<=105 else 35 if n<=114 else 36 if n<=131 else 37)
 r=dict(id=f'physics-chapter-34-{kind}-{n}',parts=ps,reasoning=why+' Verification: substitute signed distances in the imaging equations and check orientation, reality, and limiting behavior independently.',sourcePages=pages or ([28] if kind=='questions' else [page]),assumptions=assumptions or ['Paraxial rays and ideal thin lenses/spherical mirrors; real object distance positive, real image distance positive, and m=−i/p. Distances use the field units.'])
 if scope:r['scope']=scope
 rows.append(r)
def orient(m,label='Image orientation'):return C(label,'Inverted' if m<0 else 'Noninverted','Noninverted' if m<0 else 'Inverted','No image','The sign of lateral magnification determines orientation.')
def reality(i,label='Image type'):return C(label,'Real' if i>0 else 'Virtual','Virtual' if i>0 else 'Real','No image','The sign of image distance determines whether rays actually converge.')
def side(i,mirror=False,label='Image side'):
 same=(i>0) if mirror else (i<0)
 return C(label,'Same side as object' if same else 'Opposite side from object','Opposite side from object' if same else 'Same side as object','At the optical element','A real mirror image is in front; a real lens image is beyond the lens.')
def image(p,f):return 1/(1/f-1/p)
def pack(p,f,mirror=False,labels=('a','b','c','d','e')):
 i=image(p,f);m=-i/p
 return [N(labels[0]+' · Image distance',i,'cm','1/i=1/f−1/p.'),N(labels[1]+' · Lateral magnification',m,'dimensionless','m=−i/p.'),reality(i,labels[2]+' · Image type'),orient(m,labels[3]+' · Orientation'),side(i,mirror,labels[4]+' · Side')]
R(1,[N('Camera-to-image distance',sqrt(5**2+(4.3+3.3)**2),'m','Mirror image has equal depth behind the mirror; apply Pythagoras.')],'Use the image position, not the bird position.')
R(2,[N('Eye-to-image distance',40,'cm','The eye is30cm in front and the moth image10cm behind.')],'Plane reflection preserves perpendicular distance.')
R(3,[N('Intensity multiplier',1+1/9,'dimensionless','Direct path d and reflected virtual-source path3d give I/I₀=1+1/9.')],'Add incoherent isotropic intensities.',assumptions=['The textbook intensity model neglects coherent interference and assumes an ideal plane mirror.'])
R(4,[N('Burglar distance from mirror at first visibility',1.5,'m','Unfold the corridor reflection; limiting ray through the corner gives mirror-distance d/2.')],'Trace the first unobstructed reflected ray through the corridor corner.')
R(5,[N('Image depth below mirror',250+200*(2/1.33-1),'cm','Refract down, reflect, then refract back to air: apparent depth below surface=d₁+2d₂/n; subtract physical mirror depth d₂.')],'The final image is viewed from air after both passages through the water surface.',assumptions=['Use n_water=1.33 and paraxial rays.'])
R(6,[N('Magnification at p=14cm',-2.5,'dimensionless','Graph crossesm=2 atp5cm, givingf=10cm; m=f/(f−14).')],'Infer focal length from the graph before extrapolating.')
R(7,[N('Mirror-to-face distance',17.5*(1-1/2.5),'cm','For upright virtual magnification m, p=f(1−1/m); f=r/2.')],'Positive magnification identifies the virtual image inside focus.')
R(8,[N('Image distance at70cm',28,'cm','Graph asymptote p=f=20cm; i=pf/(p−f).')],'The focal point is read from the vertical asymptote.')
for n,p,f in [(9,18,12),(10,15,10),(11,8,-10),(12,24,36),(13,12,18),(14,22,-35),(15,10,-8),(16,17,-14)]:
 ps=pack(p,f,True,('b','c','d','e','f'));ps.insert(0,N('a · Radius of curvature',2*f,'cm','For a spherical mirror r=2f.'))
 R(n,ps,'Table34-3 supplies unsigned focal magnitudes; concave f>0, convex f<0.',pages=[29])
# Fully derive missing entries of Table34-4; given values need not be re-entered.
T={17:(20,10),18:(8,24),19:(-20,20),20:(40*28/68,40),21:(20,30),22:(-20,180),23:(-30,120),24:(20,60),25:(30*12/42,30),26:(20,60),27:(-30,30),28:(math.inf,10),29:(-20,5)}
given={17:{'type','f','p'},18:{'p','m','ori'},19:{'r','i'},20:{'p','m'},21:{'f','p'},22:{'f','m'},23:{'f','m'},24:{'p','m'},25:{'p','m','ori'},26:{'f','p','side'},27:{'f','i'},28:{'p','m'},29:{'type','r','i'}}
for n,(f,p) in T.items():
 i=-p if math.isinf(f) else image(p,f);m=-i/p;typ='Plane' if math.isinf(f) else 'Concave' if f>0 else 'Convex';ps=[];gs=given[n]
 vals=[('type',C('a · Mirror type',typ,*[x for x in ['Concave','Convex','Plane'] if x!=typ],'Mirror type follows the sign of f.')),('f',N('b · Focal length',f if math.isfinite(f) else 0,'cm','Use f=pi/(p+i).') if math.isfinite(f) else C('b · Focal length','Infinite','Zero','Equal to p','A plane mirror has zero optical power.')),('r',N('c · Radius of curvature',2*f,'cm','r=2f.') if math.isfinite(f) else C('c · Radius of curvature','Infinite','Zero','Equal to p','A plane is the infinite-radius limit.')),('p',N('d · Object distance',p,'cm','Use p=−i/m with the mirror equation.')),('i',N('e · Image distance',i,'cm','i=pf/(p−f).')),('m',N('f · Magnification',m,'dimensionless','m=−i/p.')),('rv',reality(i,'g · Image type')),('ori',orient(m,'h · Orientation')),('side',side(i,True,'i · Side'))]
 ps=[v for k,v in vals if k not in gs];R(n,ps,'Solve the simultaneous signed imaging and magnification relations; interpret given unsigned magnitudes using the orientation/type information.',pages=[30])
R(30,[N('Magnification at21cm',10/(10+21),'dimensionless','Graph m=.5 atp10cm gives f=−10cm; m=f/(f−p).')],'A convex mirror has positive magnification below one.')
R(31,[C('a · Signed image velocity','v_I=−(r/(2p−r))² v_O','v_I=(r/(2p−r)) v_O','v_I=−v_O','Differentiate i=rp/(2p−r) with respect to p.'),N('b · Image speed',(15/(60-15))**2*5,'cm/s','Substitute r15cm,p30cm,vO5cm/s.'),N('c · Image speed',(15/(16-15))**2*5,'cm/s','Near focus the denominator is small.'),N('d · Image speed',(15/(2-15))**2*5,'cm/s','10mm=1cm.')],'The signed velocity relation is negative with respect to the signed object velocity; the requested speeds are magnitudes.')
# Refraction: n1/p+n2/i=(n2−n1)/r.
ref={32:(1,1.5,10,30),33:(1,1.5,10,None),34:(1.5,None,100,-30),35:(1.5,1,70,30),36:(1.5,1,None,-30),37:(1.5,1,10,None),38:(1,1.5,None,30)}
for n,(n1,n2,p,r) in ref.items():
 if n==33:i=-13;r=(n2-n1)/(n1/p+n2/i)
 elif n==34:i=600;n2=(n1/p+n1/r)/(1/r-1/i)
 elif n==36:i=-7.5;p=n1/((n2-n1)/r-n2/i)
 elif n==37:i=-6;r=(n2-n1)/(n1/p+n2/i)
 elif n==38:i=600;p=n1/((n2-n1)/r-n2/i)
 else:i=n2/((n2-n1)/r-n1/p)
 allp={'n2':N('a · Refracted-medium index',n2,'dimensionless','Solve n₁/p+n₂/i=(n₂−n₁)/r.'),'p':N('b · Object distance',p,'cm','Use the signed spherical-refraction equation.'),'r':N('c · Surface radius',r,'cm','r=(n₂−n₁)/(n₁/p+n₂/i).'),'i':N('d · Image distance',i,'cm','i=n₂/[(n₂−n₁)/r−n₁/p].'),'rv':reality(i,'e · Image type'),'side':side(i,False,'f · Side')}
 need={32:['i','rv','side'],33:['r','rv','side'],34:['n2','rv','side'],35:['i','rv','side'],36:['p','rv','side'],37:['r','rv','side'],38:['p','rv','side']}[n]
 R(n,[allp[k] for k in need],'Use indices on the incident and transmitted sides and the radius sign in Table34-5.',pages=[30])
R(39,[N('a · Index for back-surface focus',2,'dimensionless','First-surface image i=nR/(n−1)=2R requires n=2.'),C('b · Finite index for center focus','No finite index','n=1','n=2','i/R=n/(n−1) approaches1 only as n tends to infinity.')],'Parallel incident rays set object distance to infinity.')
i=1/((1-1.6)/(-5)-1.6/3)
R(40,[N('Apparent tabletop distance',5-i,'cm','Top surface is3cm above table; image distance is negative, and observer is5cm above top.')],'Apply refraction from glass to air with surface radius−5cm, then add observer separation.')
R(41,[N('a · Focal length',40,'cm','1/f=(n−1)/R for a plano-convex lens.'),C('b · Image location','At infinity','40cm behind the lens','40cm in front of the lens','The real object is exactly at the focal point.')],'A collimated emerging beam has no finite image distance.')
R(42,[N('Magnification at35cm',15/50,'dimensionless','Graph m=.5 atp15cm gives f=−15cm; m=15/(15+p).')],'Infer the negative focal length from the graph.')
R(43,[N('Image height magnitude',180*.075/(27-.075),'cm','|hI|=hO*f/(p−f), keeping meters in the ratio.')],'The film image is inverted; requested height is a magnitude.')
R(44,[N('Image distance at100cm',100*30/(100-30),'cm','Graph vertical asymptote p30cm identifies f30cm.')],'The graph is the converging-lens imaging hyperbola.')
R(45,[N('Sun image diameter',.20*1.39e9/1.50e11,'m','Parallel-ray image diameter f*Dsun/dsun.')],'Use the Sun angular diameter from AppendixC.',assumptions=['Dsun=1.39×10⁹m and Earth–Sun distance1.50×10¹¹m; small angular diameter.'])
R(46,[N('Image distance at70cm',-20*70/(70+20),'cm','Graph has f=−20cm, giving i=fp/(p−f).')],'A diverging lens gives a negative image distance.')
R(47,[N('a · Smaller radius',45,'mm','With radii R and−2R, 1/f=.5(1/R+1/(2R)); R=.75f.'),N('b · Larger radius',90,'mm','Larger radius is twice the smaller.')],'Lensmaker equation uses opposite signs for the two convex faces.')
R(48,[N('Magnification at14cm',10/(10-14),'dimensionless','Graph m=5 atp8cm gives f=10cm; m=f/(f−p).')],'At14cm the object has passed beyond focus and its real image is inverted.')
R(49,[N('Slide-to-lens distance',22,'cm','Object-screen distance equals4f, the unique lens placement has p=i=2f.')],'The quadratic discriminant vanishes.')
for n,p,f in [(50,16,4),(51,12,16),(52,25,35),(53,8,-12),(54,10,-6),(55,22,-14),(56,12,-31),(57,45,20)]:R(n,pack(p,f),'Table34-6: positive focal length for converging, negative for diverging.',pages=[31])
for n,p,index,r1,r2 in [(58,29,1.65,35,math.inf),(59,75,1.55,30,-42),(60,6,1.7,10,-12),(61,24,1.5,-15,-25),(62,10,1.5,30,-30),(63,35,1.7,42,33),(64,10,1.5,-30,-60),(65,10,1.5,-30,30),(66,18,1.6,-27,24),(67,60,1.5,35,-35)]:
 f=1/((index-1)*(1/r1-1/r2));R(n,pack(p,f),'Lensmaker equation 1/f=(n−1)(1/r₁−1/r₂), followed by the signed lens equation.',pages=[32])
R(68,[C('a · Lens type','Converging','Diverging','Plane glass plate','A real image of a real object needs a positive-power lens.'),N('b · Object-to-lens distance',40/1.5,'cm','i=.5p and p+i=40cm.'),N('c · Focal length',40/4.5,'cm','f=pi/(p+i).')],'Inversion fixes m=−.5.')
more={69:(10,5),70:(-20,8),71:(-16/3,16),72:(16/5,16),73:(10/3,10),74:(10,20),75:(-10,5),76:(10,5),77:(80,16),78:(-10,10),79:(20,8)}
given={69:{'f','p'},70:{'p','ori'},71:{'p','m'},72:{'p','m'},73:{'p','m'},74:{'type','p'},75:{'p','side'},76:{'p'},77:{'p','m'},78:{'p','ori'},79:{'p'}}
for n,(f,p) in more.items():
 i=image(p,f);m=-i/p;typ='Converging' if f>0 else 'Diverging';allp={'type':C('a · Lens type',typ,'Diverging' if f>0 else 'Converging','Zero-power lens','Sign of focal length determines lens type.'),'f':N('b · Focal length',f,'cm','Solve the signed imaging equation, using orientation/side to choose any missing sign.'),'p':N('c · Object distance',p,'cm','Use given positive real-object distance.'),'i':N('d · Image distance',i,'cm','i=pf/(p−f).'),'m':N('e · Magnification',m,'dimensionless','m=−i/p.'),'rv':reality(i,'f · Image type'),'ori':orient(m,'g · Orientation'),'side':side(i,False,'h · Side')}
 R(n,[v for k,v in allp.items() if k not in given[n]],'Table34-8 missing signs are determined by virtual/real orientation and the given magnification inequality.',pages=[32])
def system(p,fs,ds):
 M=1
 for k,f in enumerate(fs):
  i=image(p,f);M*=-i/p
  if k<len(ds):p=ds[k]-i
 return i,M
for n,p,f1,d,f2 in [(80,10,15,10,8),(81,12,8,32,6),(82,8,-6,12,6),(83,20,9,8,5),(84,15,12,67,10),(85,4,6,8,-6),(86,12,8,30,-8),(87,20,-12,10,-8)]:
 i,m=system(p,[f1,f2],[d]);R(n,[N('a · Final image distance',i,'cm','Use i₁=p₁f₁/(p₁−f₁), p₂=d−i₁, i₂=p₂f₂/(p₂−f₂).'),N('b · Overall magnification',m,'dimensionless','Multiply the two signed lateral magnifications.'),reality(i,'c · Final image type'),orient(m,'d · Final orientation'),side(i,False,'e · Final side')],'The intermediate image can be a virtual object for lens2; retain the sign of p₂.',pages=[32,33])
R(88,[N('Minimum eyepiece diameter',75/36,'mm','The exit-pupil diameter equals objective diameter divided by angular magnification.')],'Similar triangles preserve angular ray bundles.')
R(89,[N('a · Tube length',25-4-8,'cm','s=L−fob−fey.'),N('b · Object distance',4*17/(17-4),'cm','Intermediate image lies17cm from objective, so solve its lens equation.'),N('c · Objective magnification',-13/4,'dimensionless','m=−s/fob.'),N('d · Eyepiece angular magnification',25/8,'dimensionless','Relaxed-eye magnifier gives25cm/fey.'),N('e · Overall magnification',-(13/4)*(25/8),'dimensionless','Multiply objective and eyepiece magnifications.')],'The intermediate image is just inside the eyepiece focal plane, approximated at its focal plane.')
R(90,[N('a · New lens-film distance',100*5/95,'cm','i=pf/(p−f).'),N('b · Required increase',100*5/95-5,'cm','Subtract infinity-focus image distance f.')],'The lens moves away from the film to focus a closer object.')
R(91,[N('a · Effective focal length',1/(1/40+1/2.5),'cm','Retina stays2.50cm behind effective lens.'),C('b · Lens radii change','Decrease','Increase','No change','Stronger curvature gives shorter positive focal length.')],'The retinal image plane stays fixed.')
R(92,[N('Overall microscope magnification',-(250/10)*(25/5),'dimensionless','Objective image250mm from objective; eyepiece f≈50mm. Multiply−25by5.')],'The intermediate image is at the eyepiece focal plane for relaxed viewing.')
R(93,[N('a · Near-point angular magnification',3.5,'dimensionless','1+Pn/f.'),N('b · Infinity-image angular magnification',2.5,'dimensionless','Pn/f.')],'Use near point25cm.')
R(94,[N('Image distance at70cm',-30*70/100,'cm','Graph crossesi=−10cm atp15cm andi≈−17.1at40cm; f=−30cm.')],'The negative-image graph is a convex mirror with f=−30cm.')
for n,p,f1,d12,f2,d23,f3 in [(95,12,8,28,6,8,6),(96,4,-6,9.6,6,14,4),(97,18,6,15,3,11,3),(98,2,6,15,6,19,5),(99,8,-8,8,-16,5.1,8),(100,4,6,8,-4,5.7,-12)]:
 i,m=system(p,[f1,f2,f3],[d12,d23]);R(n,[N('a · Final image distance',i,'cm','Apply each lens equation successively with p_next=d−i_previous.'),N('b · Overall magnification',m,'dimensionless','M=m₁m₂m₃.'),reality(i,'c · Final image type'),orient(m,'d · Final orientation'),side(i,False,'e · Final side')],'All three intermediate object distances retain their algebraic signs.',pages=[34])
R(101,[C('Newtonian imaging relation','x x′=f²','x+x′=f','x x′=−f²','Substitute p=x+f and i=x′+f into1/p+1/i=1/f, then cancel linear terms.')],'The two distances are measured from their respective focal points.')
R(102,[N('a · Images for90degrees',3,'images','N=360/θ−1.'),N('b · Images for45degrees',7,'images','Eight angular sectors include the actual object.'),N('c · Images for60degrees',5,'images','Six sectors include the actual object.'),N('d · Minimum images at120degrees',2,'images','Symmetric placement gives two distinct images.'),N('e · Maximum images at120degrees',3,'images','An off-bisector object can give three images.'),C('f · Construction rule','Reflect each sector and its image orientation successively across each mirror','Place every image in front of its mirror','Rotate every image without reflecting its orientation','Unfold the angular sectors and exclude the actual object.')],'Overlapping sector images must only be counted once.',scope='Checks assess counts and the construction rule; freehand image-location drawings are not automatically assessed.')
R(103,[C('Equivalent focal length','f=f₁f₂/(f₁+f₂)','f=f₁+f₂','f=f₁−f₂','At zero separation p₂=−i₁; summing the two lens equations gives additive optical powers.')],'Contact thin lenses have1/f=1/f₁+1/f₂.')
R(104,[N('a · Smallest separation',20,'cm','First image in near mirror lies20cm from object.'),N('b · Second separation',60,'cm','First image in far mirror lies60cm away.'),N('c · Third separation',80,'cm','Two second-order images are each80cm from object.'),N('d · Fourth separation',100,'cm','Next reflected near-side image is100cm away.')],'Generate image coordinates−10,70,−70,90,−90 relative to near mirror0/object10.')
R(105,[N('a · Object distance',3,'cm','First lens image must be6cm to right,4cm in front of mirror; p=fi/(i−f).'),N('b · Return-pass image distance',1/(1/2-1/14),'cm','Mirror image lies14cm to the right of lens and is the return-pass object.')],'The plane mirror reflects an object4cm in front to4cm behind its surface.')
R(106,[C('a · Final distance from lens','2f₁','f₁','2f₂','First lens images at2f₁; mirror object at2f₂ images back at the same point; return lens images at2f₁.'),N('b · Overall magnification',-1,'dimensionless','Three inverted stages each m=−1 multiply to−1.'),C('c · Final image type','Real','Virtual','At infinity','Return rays converge in front of the returning lens.'),C('d · Final image location','Left of lens','Right of lens','At the lens','The final pass travels left.'),C('e · Final orientation','Inverted','Noninverted','No finite image','Overall M=−1.')],'Trace the three optical stages, reversing the propagation direction after reflection.')
R(107,[N('a · f₁',40,'cm','m=2 gives i=−2p; separation|i|−p=p=20cm; f=2p.'),N('b · p₁',20,'cm','Object/image on same side are20cm apart.'),N('c · f₂',-40,'cm','m=.5 gives i=−.5p; separation.5p=20 =>p40,f−40.'),N('d · p₂',40,'cm','Use physical object–virtual-image separation.')],'Both images are upright and virtual.')
ps=[]
for k,f in enumerate([40,80,240,-40,-80,-240]):
 ps.extend([N(chr(97+2*k)+' · Focal length',f,'cm','Use radii40cm for equal faces; meniscus requires40cm and60cm, so1/f=.5(1/40−1/60).'),reality(f,chr(98+2*k)+' · Sun image type')])
R(108,ps,'Assign curvature signs from the six original lens profiles; parallel sunlight images at f.',pages=[35])
R(109,[N('a · Watcher apparent distance to fish',6.8+(4/3)*(8+3/(8/5)),'cm','Water-view optical distance equals waterdepth+nwater*(airdistance+glassdistance/nglass).'),N('b · Fish apparent distance to watcher',8+3/(8/5)+6.8/(4/3),'cm','Apparent plane-interface path in air sums physical layer thickness divided by its index.')],'Apply plane refraction twice, then add the observer-to-interface distance.')
R(110,[N('Fish lateral magnification',2*1.33/(1.33+1),'dimensionless','For spherical refraction m=−n₁i/(n₂p), withp=R/2,r=−R,n₁1.33,n₂1.')],'Refraction image distancei=−R/(n+1); apparent height must use the refractive magnification, not−i/p.')
R(111,[N('a · Output beam width',2.5*30/12.5,'mm','Beam width scales asf₂/f₁.'),N('b · Output intensity',9000*(12.5/30)**2,'W/m²','Power is conserved while circular beam area scales aswidth squared.'),N('c · New lens separation',30-26,'cm','Afocal pair needsd=f₁+f₂ withnegative f₁.')],'The beam remains parallel after the two lens powers cancel.')
R(112,[C('Apparent liquid depth','d_a=d/n','d_a=nd','d_a=d/n²','Small-angle Snell givesθair=nθliquid; the same lateral offset givesd_aθair=dθliquid.')],'Use paraxial viewing near the normal.')
R(113,[N('Object-to-pinhole distance',100,'cm','The square image must fit6cm film width; hI/hO=12/p=6/50.')],'The smaller film dimension limits a complete square image.')
R(114,[C('Shortest reflected path condition','Angle of incidence equals angle of reflection','The two angles sum to90degrees','Incident ray must be normal','Reflect A across the mirror; straight A′OB is the shortest unfolded path.')],'A straight segment is shorter than a bent path between fixed endpoints.')
R(115,[N('Used mirror area',pi*(5/2*10/(10+20))**2,'mm²','Similar triangles give used diameter=5mm*10/(10+20).')],'The pupil bounds the reflected ray cone.')
R(116,[C('Minimum object-image separation','D≥4f, with equality at p=i=2f','D≥2f, with equality at p=i=f','D≥f','D=p+i=pi/f and (p−i)²≥0 imply(p+i)²≥4pi=4fD.')],'Both p and i are positive for a real image.')
R(117,[C('a · Lens-position separation','d=√(D(D−4f))','d=D−2f','d=√(D²+4Df)','The roots ofp(D−p)=fD differ bysqrt(D²−4fD).'),C('b · Smaller-to-larger image-size ratio','((D−d)/(D+d))²','(D−d)/(D+d)','((D+d)/(D−d))²','At the two conjugate placements the magnifications are reciprocal.')],'The conditionD≥4f is required for real screen images.')
for n,p,fs,ds,h in [(118,10,[-15,12],[12],1),(119,40,[20,-15],[10],None),(120,20,[10,12.5],[30],None)]:
 i,m=system(p,fs,ds)
 if n==118:ps=[N('a · Final image distance',i,'cm','Sequential thin-lens imaging.'),N('b · Image height magnitude',abs(m)*h,'cm','|hI|=|M|hO.'),reality(i,'c · Image type'),orient(m,'d · Orientation')]
 elif n==119:ps=[N('a · Final image distance',i,'cm','Sequential thin-lens imaging.'),orient(m,'b · Orientation'),reality(i,'c · Image type'),N('d · Overall magnification',m,'dimensionless','Product of both signed magnifications.')]
 else:ps=[N('a · Final image distance',i,'cm','Sequential thin-lens imaging.'),N('b · Overall magnification',m,'dimensionless','Product of signed magnifications.'),reality(i,'c · Image type'),orient(m,'d · Orientation')]
 R(n,ps,'Use p₂=d−i₁, including a negative p₂ if the first image lies beyond lens2.',pages=[36])
R(121,[N('a · Image distance',-12,'cm','1/i=−1/30−1/20.'),C('b · Ray-diagram image','Upright virtual image12cm left of lens, between lens and object','Inverted real image12cm right of lens','Upright real image30cm right of lens','A diverging lens sends rays apart; their backward extensions cross on the object side.')],'The ray through optical center is undeviated; a parallel incident ray diverges from the near focus.',scope='Checks include signed image distance and ray-diagram conclusions; the freehand drawing is not evaluated.')
i1=1.;pmirror=2-i1;imirror=-pmirror;preturn=2-imirror;i=image(preturn,.5);m=(-i1/1)*1*(-i/preturn)
R(122,[N('a · Final image distance',i,'m','First lens image1m right; plane-mirror image3m right; returnp3m,f.5m.'),N('b · Overall magnification',m,'dimensionless','Multiply firstlens−1, plane mirror+1 and returnlens−.2.'),reality(i,'c · Image type'),C('d · Final side','Left of lens','Right of lens','At infinity','Return propagation is leftward.'),orient(m,'e · Orientation')],'The plane mirror has m=+1, unlike a concave mirror at its center of curvature.')
R(123,[N('a · Object-image separation',80,'cm','Refraction givesi=1.5/[(.5/6)−.1]=−90cm; object−10cm/image−90cm gives80cm separation.')],'Use spherical refraction into glass; the virtual image lies on the incident side.')
rows[-1]['parts'].append(C('b · Virtual-image object range','0<p<12cm','p>12cm','All positive p','The denominator(.5/6−1/p) is negative only forp<12cm.'))
R(124,[C('a · Longitudinal image length','L′=L(f/(p−f))²','L′=L f/(p−f)','L′=L(p/f)²','Differentiate i=pf/(p−f):|di/dp|=f²/(p−f)² for short object.'),C('b · Longitudinal magnification','m′=m²','m′=m','m′=−m²','Lateralm=−f/(p−f); square it.')],'The stated result is the differential short-object approximation; finite objects use the two endpoint images.')
R(125,[C('Reflected-ray angular change','2α','α','α/2','Rotating the normal changes both incident-angle and reflected-angle contributions.'),N('Check at α=45degrees',90,'degrees','2α=90degrees.')],'Hold the incident ray fixed while rotating the mirror.')
R(126,[N('Focal length',10,'cm','m=−.5 impliesi15cm; f=pi/(p+i).')],'The real inverted image identifies a concave mirror.')
R(127,[N('a · Object distance for upright3times',8,'cm','f12cm,m3 givesp=f(1−1/m).'),N('b · Object distance for inverted3times',16,'cm','m−3 givesp=f(1−1/m).'),N('c · Object distance for invertedone-third',48,'cm','m−1/3 givesp48cm.')],'Use a positive focal length f=r/2=12cm.')
R(128,[N('Image distance',-28,'cm','Upright reduced image meansf−40cm; i=f(1−m)=−28cm.')],'A real-object reduced upright lens image is virtual.')
def exactmirror(p,r,a):
 # Ray from x=r-p on the axis to the near-right spherical surface.
 A=1+tan(a)**2;B=2*(p-r)*tan(a)**2;C0=(p-r)**2*tan(a)**2-r*r
 x=(-B+sqrt(B*B-4*A*C0))/(2*A);y=(x+p-r)*tan(a);beta=atan(y/x);gamma=2*beta-a
 return r-x+y/tan(gamma)
ps=[]
for part,p in [('a',20),('b',4)]:
 for a in [.5,.1,.01]:ps.append(N(f'{part} · Exact image distance, α={a}rad',exactmirror(p,12,a),'cm','Intersect ray with x²+y²=r², apply specular reflection, then find its axis intercept.'))
 ps.append(N(part+' · Paraxial image distance',image(p,6),'cm','Use1/p+1/i=2/r for comparison.'))
R(129,ps,'The exact reflected direction differs from the paraxial approximation at larger α; verify convergence as α→0.')
R(130,[N('a · Image distance',-1.5,'cm','Upright reducedmirrorimageisconvex:f−2cm,i=f(1−m)=−1.5cm.'),C('b · Focal-length sign','Negative','Positive','Zero','A real-object upright reduced image comes from a convex mirror.'),C('c · Image type','Virtual','Real','At infinity','i<0.')],'The mirror focal magnitude2cm must be assigned the negative sign.')
R(131,[N('Apparent depth',20/1.33+40/1.46,'mm','For layers near-normal apparent depths add d_j/n_j.')],'Both plane interfaces have zero optical power apart from depth scaling.')
R(132,[N('a · Image distance',image(1,-.175),'m','Convex sphere radius−.35m, f−.175m.'),N('b · Image height',-image(1,-.175)*2,'mm','hI=−i hO/p.'),C('c · Inverted?','No','Yes','Only at large angles','Convex mirror magnification is positive.')],'Use the near-surface object distance, not distance from sphere center.')
R(133,[C('a · Motion toward eye','Virtual image approaches lens from infinity and angular size increases','Virtual image recedes beyond infinity','Image stays fixed','Forp<f, i=fp/(p−f); reducingp brings negativei towardzero.'),C('b · Maximum useful image position','At the near point25cm from eye','At the lens surface','At infinity','A nearer virtual image cannot be sharply accommodated.'),C('c · Maximum useful angular magnification','1+(25cm)/f','(25cm)/f','1+f/(25cm)','Seti=−25cm and use the lens equation.'),C('d · Relation to lateral magnification','Equal','Opposite sign','Square of lateral magnification','At near-point placement, lateralm=1+Pn/f equals angularmagnification.')],'Assume lens placed close to eye and nearpoint25cm.')
R(134,[C('a · Telescope angular magnification','m_θ=−f_ob/f_ey','m_θ=f_ey/f_ob','m_θ=−f_ob f_ey','Objectiveimageheight=f_obθ; eyepiece angle=−h/f_ey.'),N('b · Meterstick image height',16.8/2000,'m','Small-angle estimate hI=f_ob*hO/p.'),N('c · Eyepiece focal length',.025,'m','Objective f=R/2=5m; |M|=5/fey=200.')],'The folding plane mirror changes the ray direction but adds no optical power.')
R(135,[C('a · Distance beyond sphere surface','r(2−n)/(2(n−1))','nr/(n−1)','r/(n−1)','Firstrefraction i₁=nr/(n−1), secondobjectp₂=2r−i₁; apply second sphericalrefraction.'),C('b · Image side for1<n<2','Right of sphere','Left of sphere','At sphere center','The derived back-focal distance is positive for1<n<2.')],'The sphere is a thick optical element; do not substitute a thin-lens approximation.')
R(136,[C('Outgoing ray direction','Exactly opposite to the incident direction','Perpendicular to the incident direction','Unchanged','Each orthogonal mirror reverses one Cartesian component: (vx,vy,vz)→(−vx,−vy,−vz).')],'Three mutually perpendicular reflections reverse all three direction components.')
R(137,[N('Focal length',8/3,'cm','m−2 givesi8cm; f=4*8/(4+8).')],'The image is inverted and real.')
R(138,[C('a · Mirror type','Convex','Concave','Plane','Positive reduced magnification requires convex mirror for a real object.'),N('b · Object distance',160,'cm','f−40cm,m.2 yields p=f(1−1/m)=160cm.')],'Do not assign a positive sign to the focal magnitude.')
i,m=system(3,[4,-4],[8]);R(139,[N('a · Final image distance',abs(i),'cm','Lens1converging f4cm givesi₁−12cm; p₂20cm, divergingf₂−4cm.'),C('b · Final side','Left of lens2','Right of lens2','At infinity','i₂<0.'),reality(i,'c · Image type'),orient(m,'d · Orientation')],'Original lensprofiles identify lens1converging andlens2diverging.')
R(140,[N('a · Corrective focal length',-.50,'m','Infinityobject must formvirtualimage atfarpoint−.50m.'),C('b · Lens type','Diverging','Converging','Plane','Negativepower correctsmyopia.'),N('c · Lens power',-2,'diopters','P=1/f withf inmeters.')],'Assume corrective lens close to eye.')
R(141,[C('a · Near-point angular magnification','1+(25cm)/f','(25cm)/f','1+f/(25cm)','Place virtualimage atnearpoint anduseparaxiallensformula.'),C('b · Relaxed-eye angular magnification','(25cm)/f','1+(25cm)/f','f/(25cm)','Image at infinity occurs withobject atfocus.'),N('c · Near-point value for f10cm',3.5,'dimensionless','1+25/10.'),N('d · Infinity value for f10cm',2.5,'dimensionless','25/10.')],'Near-pointimage requires accommodation; infinityimage is relaxed viewing.')
# Concept questions appended below.
R(1,[C('a · Apparent fish region','a','b','At its actual position','Refraction away from the normal in air moves the backward ray extension toward regiona.'),C('b · Apparent eyes region','c','d','At their actual position','An underwater observer sees an above-water object farther from the surface.')],'Apply Snell law at the water–air interface to backward extensions of rays.',kind='questions')
R(2,[C('a · Impossible images','I₁ and I₄','I₂ and I₃','Only I₄','For a real object, mirror images are real/inverted in front or virtual/upright behind.'),C('b · Concave-mirror possibilities','I₂ and I₃','Only I₂','I₁ and I₄','Concave mirrors make either real inverted or virtual upright images.'),C('c · Convex-mirror possibility','I₃','I₁','I₂','Convex mirrors give virtual upright images behind the mirror.'),C('d · Virtual image','I₃','I₂','I₁ and I₄','Virtual mirror images lie behind the reflecting surface.'),C('e · Negative magnification','I₂','I₃','I₁','The inverted real image hasm<0.')],'Classify sides and orientation from the original figure; sizes and distances are not to scale.',kind='questions')
R(3,[C('a · Monsters visible along the virtual hallways','a and c','All three','Only b','Unfold the equilateral mirror walls along each corridor axis; b remains behind a blocking wall.'),N('b · Images of each visible monster per hallway',2,'images','Unfolding gives two appearances of each visible monster before the corridor returns to the entrance.'),C('c · Far end of each hallway','An image of you at the entrance','Monster b','An unmirrored wall','Repeated reflections return the corridor to an image of the entrance.')],'Trace the three straight virtual-hallway centerline directions through the original triangular mirror layout; each returns to an unfolded image of the entrance.',kind='questions',scope='Counts use the textbook straight virtual-hallway (corridor-centerline) unfolding, not every possible off-axis multireflection path. The freehand construction is not automatically evaluated.')
R(4,[C('a · Image motion','From infinity toward the focal point, in front of the mirror','From the focal point toward infinity','Behind the mirror toward the object','i=fp/(p−f) decreases from positive infinity to f as p grows fromf.'),C('b · Image height','Decreases continuously','Increases continuously','First increases then decreases','|m|=f/(p−f) falls continuously.')],'A concave mirror with p>f always gives an inverted real image.',kind='questions')
R(5,[C('Mirror type','Convex','Plane','Concave','An upright reduced virtual image makes objects appear farther away.')],'A convex mirror provides a wider field of view with reduced magnification.',kind='questions')
R(6,[C('Concave mirror curve','1','2','3','The positive focal point gives a vertical asymptote.'),C('Convex mirror curve','2','1','3','|i| grows toward|f| from below.'),C('Plane mirror curve','3','1','2','|i|=p is a straight line.')],'Match the limiting imaging laws to the plotted curves.',kind='questions')
ps=[C('a · Easy variations','1, 3, 4, 5 and 6','Only 2','All six','Only variation2 can make an intermediate real image on either side of lens2.')]
for n in [1,3,4,5,6]:
 ps.append(C(f'b · Variation {n} final image','Right; inverted' if n in [1,3,4] else 'Left; same orientation','Left; inverted','Right; same orientation','A virtual image from lens1 lies left of lens1; the illustrated lens spacing places it beyond lens2 focal distance. Two diverging lenses retain upright virtual imaging.'))
R(7,ps,'Use the diagram spacing and signs of the intermediate object distance; no unique conclusion is possible for variation2 without actual distances.',kind='questions')
R(8,[C('Converging lens curve','1','2','3','A positive focal length gives a pole in image distance.'),C('Diverging lens curve','2','1','3','The virtual-image distance approaches|f| smoothly.')],'The same mathematical imaging curves describe mirrors and thin lenses, with different image-side interpretation.',kind='questions')
R(9,[C('Focal-magnitude ranking','d > a = b > c','c > a = b > d','a = b = c = d','Equal signed curvatures in meniscusd cancel thin-lens power; single convexfacesa,b have equal power; double convexc has twice it.')],'Use 1/f=(n−1)(1/r₁−1/r₂); plane faces have infinite radius.',kind='questions')
R(10,[C('a · Impossible images','I₂ and I₃','I₁ and I₄','Only I₃','A real-object lens image is virtual upright on the incident side or real inverted on the transmitted side.'),C('b · Converging-lens possibilities','I₁ and I₄','Only I₄','I₂ and I₃','A converging lens makes a virtual upright image inside focus or real inverted image beyond focus.'),C('c · Diverging-lens possibility','I₁','I₃','I₄','A diverging lens makes an upright virtual image on the object side.'),C('d · Virtual image','I₁','I₄','I₂','Backward ray extensions intersect left of lens.'),C('e · Negative magnification','I₄','I₁','I₃','An inverted image has negative lateral magnification.')],'The original figure is reused with a lens rather than a mirror.',kind='questions')
R(11,[C('a · Reversed coordinate axis','x','y','z','The coordinate normal to the mirror changes sign.'),C('b · Top-bottom inversion?','No','Yes','Only for a concave mirror','A plane mirror leaves vertical coordinate unchanged.'),C('c · Physical left-right interchange?','No','Yes','Only with one eye','The parallel horizontal coordinate is unchanged; the common perception involves a mental rotation.'),C('d · Actual reversal','Front and back','Top and bottom','Left and right','Reflection reverses the normal coordinate and handedness.')],'Apply (x,y,z)→(−x,y,z) in the specified coordinate system.',kind='questions')
for row in rows:
 if row['id'] in ['physics-chapter-34-problems-33','physics-chapter-34-problems-35','physics-chapter-34-problems-51']:
  row['reviewNotice']='The imported numerical reference has a sign transcription error: it omitted a required negative sign. These checks use signed distances from the original imaging equations; the source image is virtual or the surface radius is negative as labeled.'
  row['referenceAnswer']='; '.join(p['label']+': '+str(round(p['answer'],6))+' '+p.get('unit','') for p in row['parts'] if p['type']=='numeric')

# Readability and explicit per-problem verification details.
cleanups={'reducedmirrorimageisconvex':'reduced mirror image is convex','angularmagnification':'angular magnification','Objectiveimageheight':'Objective image height','sphericalrefraction':'spherical refraction','formvirtualimage':'form a virtual image','anduseparaxiallensformula':'and use the paraxial lens formula','Returnp3m':'Return object distance3m','upperhalf':'upper half','firstlens':'first lens','returnlens':'return lens','waterdepth':'water depth','airdistance':'air distance','glassdistance':'glass distance','nearpoint':'near point','finalimage':'final image','virtualimage':'virtual image','Sunimage':'Sun image','objectimage':'object–image','thinlens':'thin lens','imageheight':'image height','lensprofiles':'lens profiles','rayconstruction':'ray construction','focalpoint':'focal point'}
for row in rows:
 for part in row['parts']:
  for key in ['label','explanation']:
   for old,new in cleanups.items():part[key]=part[key].replace(old,new)
 for key in ['reasoning','scope']:
  if key in row:
   for old,new in cleanups.items():row[key]=row[key].replace(old,new)
 n=int(row['id'].split('-')[-1])
 if '-problems-' in row['id']:
  if 9<=n<=29:detail='Reconstruct the specified focal length from the signed conjugates and verify m=−i/p; the implied concave/convex type and image side agree with the table.'
  elif 32<=n<=38:detail='Check n₁/p+n₂/i=(n₂−n₁)/r using the given table values and the solved entry; the sign of i agrees with the real/virtual classification.'
  elif 50<=n<=79:detail='Substitute the lensmaker focal length where needed, then independently check the reciprocal imaging equation and the magnification sign against the specified orientation.'
  elif 80<=n<=87 or 95<=n<=100 or n in [118,119,120]:detail='Propagate the intermediate image coordinates along the common axis; verify that each next object distance equals separation minus the preceding image distance and multiply all signed magnifications.'
  elif n in [6,8,30,42,44,46,48,94]:detail='The original graph grid yields the focal length used here; the reconstructed imaging curve passes through the plotted grid crossings before extrapolation.'
  else:detail='Check the stated limiting case and signs in the specific derivation above; numerical answers use the full source givens before final rounding.'
  row['reasoning']=row['reasoning'].split(' Verification:')[0]+' Verification: '+detail

# Final structural and numerical audit against the source exercise inventory.
source=json.loads(gzip.decompress((ROOT/'site/questions/physics.json.gz').read_bytes()))
expected={q['id'] for q in source if q['chapter']==34};actual={r['id'] for r in rows}
assert expected==actual,(expected-actual,actual-expected)
assert len(rows)==len(actual)==152
for r in rows:
 assert r['parts'] and r['sourcePages']
 for p in r['parts']:
  if p['type']=='numeric':assert math.isfinite(p['answer']) and (p['answer']==0 or p['tolerance']<abs(p['answer'])),(r['id'],p)
  else:assert p['answer'] in p['options'] and len(set(p['options']))==3,(r['id'],p)
(HERE/'ch34.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'records',sum(len(r['parts']) for r in rows),'fields')
