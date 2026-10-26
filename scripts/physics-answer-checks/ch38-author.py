#!/usr/bin/env python3
"""Original source-reviewed photon/matter-wave derivations; PDF28–33 and cited diagrams inspected."""
import math,json,pathlib,gzip,subprocess,re
from math import pi,sqrt,sin,cos,acos,exp,expm1,log
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[1]
h=6.62607015e-34;c=299792458.;e=1.602176634e-19;me=9.1093837015e-31;mp=1.67262192369e-27;mn=1.67492749804e-27;u=1.66053906660e-27;kB=1.380649e-23;NA=6.02214076e23;hb=h/(2*pi);lc=h/(me*c);Er=me*c*c/e;rows=[]
def N(label,a,unit,why,t=None,accepted=None):
 p=dict(label=label,type='numeric',answer=a,unit=unit,tolerance=max(abs(a)*.008,1e-300) if t is None else t,explanation=why)
 if accepted is not None:p['acceptedValues']=accepted
 return p
def C(label,a,b,d,why):return dict(label=label,type='choice',answer=a,options=[a,b,d],explanation=why)
def R(n,parts,why,kind='problems',assumptions=None,scope=None,notice=None,reference=None,pages=None):
 if pages is None:
  pages=([28] if n<=9 else [29]) if kind=='questions' else ([29] if n<=9 else [29,30] if n==10 else [30] if n<=32 else [30,31] if n==33 else [31] if n<=53 else [31,32] if n==54 else [32] if n<=69 else [32,33] if n==70 else [33])
 r=dict(id=f'physics-chapter-38-{kind}-{n}',parts=parts,reasoning=why+' Verification: '+parts[0]['explanation'],sourcePages=pages,assumptions=assumptions or ['SI constants h=6.62607015×10⁻³⁴J·s, c=299792458m/s, e=1.602176634×10⁻¹⁹C; stated chapter approximations are identified.'])
 if scope:r['scope']=scope
 if notice:r['reviewNotice']=notice
 if reference:r['referenceAnswer']=reference
 rows.append(r)
def photon(l):return h*c/l
def nrp(K,m=me):return sqrt(2*m*K)
def relK(p,m=me):return (p*c)**2/(sqrt((p*c)**2+(m*c*c)**2)+m*c*c)
def comp(E,theta,m=me):return E/(1+E/(m*c*c)*(1-cos(theta)))
def wkb(E,U,L,m=me):return exp(-2*sqrt(2*m*(U-E))*L/hb)
def exactT(E,U,L,m=me):
 a=sqrt(2*m*(U-E))*L/hb
 return 1/(1+U*U*math.sinh(a)**2/(4*E*(U-E)))
def stepr(E,U):
 a=sqrt(E);b=sqrt(E-U);return ((a-b)/(a+b))**2
# Photon counting and photoelectric effect.
R(1,[N('a · Longest recordable wavelength',h*c/(.6*e),'m','At the threshold hc/λ=0.6eV.'),C('b · Spectrum region','Infrared','Ultraviolet','Visible','The threshold wavelength is about2.07μm, longer than visible light.')],'Absorption requires enough energy to dissociate a molecule; intensity cannot replace photon energy.')
R(2,[N('Electron speed',sqrt(2*photon(590e-9)/me),'m/s','Set mv²/2=hc/λ; the resulting speed is safely nonrelativistic.')],'The photon energy becomes the electron kinetic energy, not its rest energy.')
R(3,[N('Photon emission rate',3.9e26/photon(550e-9),'photons/s','Divide total emitted power by the energy of one550nm photon.')],'Rate times photon energy reconstructs3.9×10²⁶W.')
R(4,[N('Absorbed photon flux',.005/(photon(633e-9)*pi*(.0035/2)**2),'photons/(m²·s)','Flux=P/(EγA), with A=π(d/2)².')],'The diameter must be halved before finding the beam area.')
R(5,[N('Photon energy',photon(1/1650763.73)/e,'eV','The wavelength is1m divided by1650763.73.')],'The historical definition determines the wavelength before using E=hc/λ.')
R(6,[N('Photon energy',photon(589e-9)/e,'eV','Use E=hc/λ and convert joules to electron-volts.')],'One photon carries about2.11eV.')
R(7,[N('Source power',4*photon(500e-9)*4*pi*3**2/(.8*2e-6),'W','Absorbed rate=P Aη/(4πr²Eγ); solve forP.')],'The80% absorption efficiency divides the required emitted power.')
R(8,[N('Central-disk absorption rate',.84*1.5/photon(515e-9),'photons/s','The disk receives84% of beam power; divide that power byhc/λ.')],'Focusing changes the spatial flux, not the total number in the given84% fraction.')
rate=100/photon(589e-9)
R(9,[N('a · Emitted photon rate',rate,'photons/s','P/Eγ gives emitted photons per second.'),N('b · Distance for stated flux',sqrt(rate/(4*pi*1e4)),'m','One photon per cm² per second is10⁴photons/(m²s); useN/(4πr²).'),N('c · Photon flux at2m',rate/(4*pi*2**2),'photons/(m²·s)','Isotropic rate is distributed over a sphere of area4πr².')],'The inverse-square flux integrates to the total emission rate.')
power=2.6*1390;rate=power/photon(550e-9)
R(10,[N('a · Incident power',power,'W','Normal incidence gives P=IA.'),N('b · Absorbed photon rate',rate,'photons/s','All incident photons are absorbed, so rate=P/Eγ.'),N('c · Time for one mole',NA/rate,'s','A mole contains NA photons; time=NA/rate.')],'Energy and photon count are linked through the specified single wavelength.')
R(11,[C('a · Greater photon rate','Infrared700nm lamp','Ultraviolet400nm lamp','Equal rates','At equal power the longer-wavelength photons each cost less energy.'),N('b · Greater rate',400/photon(700e-9),'photons/s','The700nm lamp emitsPλ/(hc).')],'For fixedP, photon rate is proportional to wavelength.')
R(12,[N('Absorbed power',100*photon(550e-9),'W','Multiply photon absorption rate byhc/λ.')],'The minute power is nevertheless a finite positive quantity.')
R(13,[N('Lifetime photon count',.93*60*730*3600/photon(630e-9),'photons','Useful optical energy isηPt; divide byEγ.')],'Convert hours to seconds and apply the93% efficiency once.')
R(14,[N('Absorbed photon rate',(7.2e-9/2)*.5*2e-6/(4*pi*12**2)/photon(600e-9),'photons/s','The original graph slope isEs/ts=3.6nW; use isotropic dilution and50% absorption.')],'The plotted line passes through the dashed Es,ts intersection, so its slope is fixed.',scope='Source graph reading uses Es=7.2nJ and ts=2.0s; both are explicitly supplied.')
R(15,[N('Incident wavelength',h*c/(7.2*e),'m','Einstein balance hc/λ=Φ+eVs=2.2eV+5.0eV.')],'The stopping potential measures maximum kinetic energy, not total photon energy.')
R(16,[N('Maximum kinetic energy',(h*3e15-2.3*e)/e,'eV','Kmax=hf−Φ, positive for the supplied frequency.')],'The work function is subtracted from each absorbed photon energy.')
R(17,[N('Maximum electron speed',sqrt(2*(5.8-4.5)*e/me),'m/s','The largest electron kinetic energy is1.30eV, so v=√(2K/m).')],'The resulting speed is far belowc.')
R(18,[C('Suitable photocell materials','Barium and lithium','Tantalum, tungsten and aluminum','All five materials','Visible photons up to about3.1eV exceed2.5/2.3eV but not4.2/4.5eV.')],'Suitability means some visible wavelengths can exceed the threshold, not that every visible wavelength will eject electrons.')
K=photon(400e-9)-1.8*e
R(19,[N('a · Stopping potential',K/e,'V','eVs=hc/λ−Φ.'),N('b · Maximum speed',sqrt(2*K/me),'m/s','Convert kinetic energy to speed withmv²/2.')],'Both results use the same positive kinetic-energy remainder.')
R(20,[N('Photocurrent',e*1e-16*.002/photon(600e-9),'A','Multiply photon rate by yield10⁻¹⁶ and elementary charge.')],'The photon energy exceeds the1.80eV work function, so the supplied yield applies.')
p=e*1.88e-4;K=relK(p)
R(21,[N('a · Maximum kinetic energy',K/(1e3*e),'keV','Magnetic curvature givesp=eBr; useK=√(p²c²+m²c⁴)−mc².'),N('b · Removal work',(photon(71e-12)-K)/(1e3*e),'keV','Photon energy equals removal energy plus electron kinetic energy.')],'The exact relativistic kinetic energy agrees with the chapter nonrelativistic estimate within about0.3%.')
R(22,[N('Maximum kinetic energy',(photon(254e-9)-photon(325e-9))/e,'eV','The cutoff fixesΦ=hc/325nm, leavinghc/254nm−Φ.')],'The target work function is inferred from its threshold wavelength.')
K=photon(200e-9)/e-4.2
R(23,[N('a · Fastest-electron kinetic energy',K,'eV','A surface electron can retain the fullhc/λ−Φ remainder.'),N('b · Slowest-electron kinetic energy',0,'eV','Electrons can lose energy in the target and emerge arbitrarily slowly.',0),N('c · Stopping potential',K,'V','An opposing potentialK/e stops the fastest electron.'),N('d · Cutoff wavelength',h*c/(4.2*e),'m','Set photon energy equal to the4.20eV work function.')],'Only the maximum kinetic energy is fixed by the simple Einstein balance.')
hfit=e*(1.85-.820)/(c*(1/(300e-9)-1/(400e-9)));phi=hfit*c/(300e-9)-e*1.85
R(24,[N('a · Planck constant from the data',hfit,'J·s','Subtract the two Einstein equations to eliminateΦ.'),N('b · Work function from the data',phi/e,'eV','Use the fittedh inΦ=hc/λ−eVs.'),N('c · Cutoff wavelength from the data',hfit*c/phi,'m','Use the same fittedh andΦ so the two measurements stay self-consistent.')],'The supplied rounded measurements determine their own fitted constants.')
phi=photon(491e-9)/e-.710
R(25,[N('a · New wavelength',h*c/((phi+1.43)*e),'m','The work function stays fixed; new photon energy isΦ+1.43eV.'),N('b · Work function',phi,'eV','Φ=hc/491nm−0.710eV.')],'Subtracting stopping potentials eliminates the material threshold.')
R(26,[N('Longest ejecting wavelength',h*c/(5.32*e),'m','The longest wavelength has photon energy exactlyΦ.')],'Platinum’s large work function puts the cutoff in the ultraviolet.')
# Compton energy/momentum conservation.
R(27,[N('a · Wavelength after30degrees',2.4e-12+lc*(1-cos(pi/6)),'m','λ′=λ+λC(1−cosθ).'),N('b · Wavelength after120degrees',2.4e-12+lc*(1-cos(2*pi/3)),'m','Usecos120°=−1/2 in the same shift law.')],'The wavelength increase is nonnegative and bounded by2λC.')
R(28,[N('a · Photon momentum',Er/1e6,'MeV/c','Photon momentum timesc equals its energy, here the electron rest energy.'),N('b · Wavelength',lc,'m','A photon of energymc² hasλ=h/(mc).'),N('c · Frequency',me*c*c/h,'Hz','f=E/h.')],'Energy, momentum and wavelength give the same electron Compton scale.')
E=photon(35e-12)
R(29,[N('a · Frequency',c/35e-12,'Hz','f=c/λ.'),N('b · Photon energy',E/(1e3*e),'keV','E=hc/λ.'),N('c · Photon momentum',E/(1e3*e),'keV/c','For photons pc=E, so the numericalkeV/c momentum equals thekeV energy.')],'No electron rest energy is assigned to a photon.')
R(30,[N('Maximum proton Compton shift',2*h/(mp*c),'m','The largest1−cosθ is2, reached in backward scattering.')],'The proton shift is smaller than the electron shift by the mass ratio.')
R(31,[N('Wavelength percentage increase',300,'percent','After losing75% of energy,E′=.25E, henceλ′=4λ andΔλ/λ=3.',0)],'Photon energy and wavelength are inversely proportional.')
E=photon(.01e-9);Ep=comp(E,pi)
R(32,[N('a · Compton shift',2*lc,'m','Backward scattering makesΔλ=2λC.'),N('b · Signed photon-energy change',(Ep-E)/(1e3*e),'keV','The photon loses energy:ΔE=E′−E<0.'),N('c · Recoil electron kinetic energy',(E-Ep)/(1e3*e),'keV','The initially stationary electron receives the lost photon energy.'),N('d · Electron direction angle',0,'degrees','Momentum conservation makes the electron move forward when the photon reverses.',0)],'Signed photon change and positive recoil kinetic energy add to zero.')
parts=[]
for lab,l in [('a',.03),('b',500e-9),('c',25e-12)]:
 x=lc/l;parts.append(N(lab+' · Photon-energy percentage change',-100*x/(1+x),'percent','At90°, E′/E=1/(1+λC/λ); evaluate the small change without subtractive cancellation.'))
x=1e6/Er;parts.append(N('d · Photon-energy percentage change',-100*x/(1+x),'percent','For1MeV, use the same ratio withx=E/(mc²).'))
parts.append(C('e · Detectability by fractional energy loss','Most feasible for x rays and gamma rays','Equally feasible in all four ranges','Most feasible for microwaves','The fractional losses are tiny in microwave/visible light but substantial at x-ray/gamma energies.'))
R(33,parts,'The tiny microwave result is computed stably as−100x/(1+x), not as a subtraction of nearly equal energies.')
E=photon(3e-12)
R(34,[N('Recoil electron kinetic energy',(E-comp(E,pi/2))/(1e3*e),'keV','Energy conservation givesK=E−E′ withE′=E/(1+E/mc²).')],'The90° shift and energy formula give identical results.')
R(35,[N('a · Electron Compton wavelength',lc,'m','λC=h/(mc).'),N('b · Proton Compton wavelength',h/(mp*c),'m','Replace electron mass with proton mass.'),N('c · Electron-scale photon energy',Er/1e6,'MeV','AtλC,e, Eγ=mec².'),N('d · Proton-scale photon energy',mp*c*c/(1e6*e),'MeV','AtλC,p, Eγ=mpc².')],'Compton wavelengths and rest energies are reciprocal mass scales.')
l0=photon(1)/(.511e6*e)
R(36,[N('a · Incident wavelength',l0,'m','λ=hc/E atE=.511MeV.'),N('b · Scattered wavelength at90degrees',l0+lc,'m','The90° shift is one electron Compton wavelength.'),N('c · Scattered photon energy',photon(l0+lc)/(1e6*e),'MeV','Use the increased wavelength to find the reduced energy.')],'For an incident photon near the electron rest energy, a90° event approximately halves its energy.')
E=50e3*e;Ep=comp(E,pi)
R(37,[N('a · Backscattered photon energy',Ep/(1e3*e),'keV','E′=E/(1+2E/mc²).'),N('b · Electron kinetic energy',(E-Ep)/(1e3*e),'keV','The recoil takes the photon-energy loss.')],'The two final energies sum to the initial50keV.')
R(38,[C('Maximum recoil relationship','Kmax=E²/(E+mc²/2)','Kmax=E²/(E+mc²)','Kmax=2E','Backscattering maximizes the Compton shift; subtractE/(1+2E/mc²) fromE.')],'Use monotonic decrease ofE′ with scattering angle and conserve total energy.')
theta=acos(1-Er*(1/(.9*200e3)-1/(200e3)))
R(39,[N('Scattering angle',math.degrees(theta),'degrees','Solve1−cosθ=mc²(1/E′−1/E), withE′=.90E.')],'The resulting cosine lies between−1 and1.')
E=17.5e3*e
R(40,[N('Maximum electron kinetic energy',(E-comp(E,pi))/(1e3*e),'keV','Maximum recoil occurs for a backward photon.')],'The work function is explicitly negligible in this question.')
parts=[]
for labs,l in [(('a','b','c'),590e-9),(('d','e','f'),h*c/(50e3*e))]:
 E=photon(l);x=lc/l
 parts.extend([N(labs[0]+' · Compton shift',lc,'m','At90°, Δλ=λC.'),N(labs[1]+' · Fractional wavelength shift',x,'dimensionless','Divide the fixed Compton shift by the incident wavelength.'),N(labs[2]+' · Signed photon-energy change',-E*x/(1+x)/e,'eV','ΔE=−E(λC/λ)/(1+λC/λ).')])
R(41,parts,'The wavelength shift is the same for both incident wavelengths; fractional and energy shifts are not.')
# Blackbody spectrum.
R(42,[N('a · Peak solar wavelength',2.898e-3/5800,'m','Wien law givesλmaxT=2.898×10⁻³mK.'),C('b · Spectrum region','Visible','Infrared','X ray','The peak is near500nm.'),N('c · Radiation temperature',2.898e-3/.00106,'K','Invert Wien law for the supplied microwave peak.')],'Temperature and peak wavelength are inversely proportional.')
R(43,[N('a · Initial peak wavelength',2.898e-3/1e7,'m','Apply Wien law to the supplied10⁷K blackbody.'),C('b · Initial spectrum region','X ray','Infrared','Radio','The initial peak is about0.290nm.'),N('c · Secondary peak wavelength',2.898e-3/1e5,'m','Apply the same law to10⁵K.'),C('d · Secondary spectrum region','Ultraviolet','Visible','Microwave','The second peak is about29.0nm.')],'This calculation uses only the stated ideal-blackbody temperatures.')
def rjratio(l,T):
 x=h*c/(l*kB*T);return expm1(x)/x
R(44,[N('a · Classical-to-Planck radiancy ratio',rjratio(400e-9,2000),'dimensionless','Divide Rayleigh–Jeans by Planck:ratio=(exp(x)−1)/x, x=hc/(λkT).'),N('b · Classical-to-Planck radiancy ratio',rjratio(200e-6,2000),'dimensionless','The original wavelength is200μm, not200mm.'),C('c · Range of agreement','Longer wavelengths','Shorter wavelengths','Neither limit','Forx≪1, exp(x)−1≈x and the ratio approaches1.')],'The ratio tends to1 from above in the long-wavelength limit.')
T=(98.6-32)*5/9+273.15;lm=2.898e-3/T
def spectral(l,T):return 2*pi*h*c*c/(l**5*expm1(h*c/(l*kB*T)))
Pm=spectral(lm,T)*4e-4*1e-9;Pv=spectral(500e-9,T)*4e-4*1e-9
R(45,[N('a · Peak wavelength',lm,'m','Convert98.6°F to310.15K and apply Wien law.'),N('b · Peak-band emitted power',Pm,'W','P=S(λmax)AΔλ withA=4cm² andΔλ=1nm.'),N('c · Peak-band photon rate',Pm/photon(lm),'photons/s','Divide the narrow-band power byhc/λmax.'),N('d · Visible-band emitted power',Pv,'W','Evaluate Planck spectral radiancy at500nm; using rounded310K rather than310.15K gives the accepted source estimate.',accepted=[spectral(500e-9,310)*4e-4*1e-9]),N('e · Visible-band photon rate',Pv/photon(500e-9),'photons/s','Divide visible power by photon energy; the accepted alternate consistently uses310K.',accepted=[spectral(500e-9,310)*4e-4*1e-9/photon(500e-9)])],'Use spectral radiancy per wavelength, not the total Stefan–Boltzmann power.')
# Matter wavelengths and kinetic energy.
R(46,[N('a · Electron wavelength',h/nrp(1000*e),'m','Usep=√(2mK), λ=h/p at1keV.'),N('b · Photon wavelength',h*c/(1000*e),'m','For the photon pc=E.'),N('c · Neutron wavelength',h/nrp(1000*e,mn),'m','Use the neutron mass in the nonrelativistic momentum.')],'Equal kinetic/photon energies do not imply equal momenta.')
R(47,[N('Electron wavelength',h/nrp(25e3*e),'m','The problem explicitly permits the classical25keV relationλ=h/√(2meV).')],'The stated nonrelativistic approximation is used rather than silently changing the model.')
p=100e3*e/c;Knr=p*p/(2*me);Kr=relK(p)
R(48,[N('Required accelerating voltage',Knr/e,'V','Match electron momentum to100keV/c, then useK=p²/(2m); the relativistic correction is small.',accepted=[Kr/e])],'Equal resolving wavelengths require equal momenta, not equal kinetic energies.',scope='The chapter nonrelativistic value and the slightly smaller relativistic value are both accepted; the required electron energy is around9.7keV.')
mNa=22.99*u;p=nrp(300*e,mNa)
R(49,[N('a · Sodium-ion momentum',p,'kg·m/s','A singly charged ion gains300eV; p=√(2mK).'),N('b · Sodium-ion wavelength',h/p,'m','λ=h/p.')],'Use sodium atomic mass22.99u and a singly charged ion.')
l=h*c/(50e9*e)
R(50,[N('a · Electron wavelength',l,'m','The explicitly allowed extreme-relativistic relation ispc≈E.'),N('b · Nuclear radius to wavelength ratio',5e-15/l,'dimensionless','Compare the supplied5fm radius to the computed wavelength.')],'The kinetic energy greatly exceeds the electron rest energy.')
R(51,[N('Electron kinetic energy',(h/(590e-9))**2/(2*me*e),'eV','Electron wavelength fixes momentumh/λ, thenK=p²/(2m).')],'A matter wave and photon of equal wavelength generally have very different energies.')
v=.9900*c;p=mp*v/sqrt(1-.9900**2);l=h/p
R(52,[N('Second-minimum angle',math.degrees(math.asin(1.5*l/4e-9)),'degrees','For two slits the second minimum hasd sinθ=3λ/2; use relativistic proton momentum.')],'The minimum order is half-integer; the first isλ/2, the second3λ/2.')
parts=[]
for lab,K,particle in [('a',e,'photon'),('b',e,'electron'),('c',1e9*e,'photon'),('d',1e9*e,'electron')]:
 l=h*c/K if particle=='photon' else h*c/sqrt(K*K+2*K*me*c*c)
 parts.append(N(lab+' · Wavelength',l,'m','Useλ=hc/E for photons and pc=√(K²+2Kmc²) for electrons.'))
R(53,parts,'For the electron, the stated energy is interpreted as kinetic energy; at1GeV the alternative total-energy convention differs by only0.05%.')
p=h/.2e-9
R(54,[N('a · Electron momentum',p,'kg·m/s','Matter wavelength fixesp=h/λ.'),N('b · Photon momentum',p,'kg·m/s','Photon wavelength has the same momentum relation.'),N('c · Electron kinetic energy',relK(p)/e,'eV','Use the electron mass-energy relation; nonrelativisticK=p²/(2m) is equivalent here.'),N('d · Photon energy',p*c/e,'eV','Photon energy ispc.')],'Equal momenta do not give equal energies for massive and massless particles.')
p=h/10e-12;K=relK(p)
R(55,[N('a · Required electron kinetic energy',K/e,'eV','Resolve10pm withp=h/λ; exact relativisticK differs modestly fromp²/(2m).',accepted=[p*p/(2*me*e)]),N('b · Required photon energy',p*c/e,'eV','For light the same momentum requiresE=pc.'),C('c · More practical probe','Electron microscope: much less kinetic energy is required','Light microscope: its photons require less energy','Both require equal energies','At the same short wavelength, electron kinetic energy is much less than photon energy.')],'The10pm resolving scale is one tenth of the given atomic diameter.',scope='Electron energy accepts the chapter nonrelativistic approximation and the exact relativistic correction.')
l=h/nrp(7.5e6*e,4*u)
R(56,[N('a · Alpha wavelength',l,'m','Use nonrelativisticp=√(2mK) withm=4u.'),C('b · Is the wave nature essential here?','No: wavelength is much smaller than the30fm approach distance','Yes: wavelength is much larger than30fm','Yes: every wavelength forces the same diffraction','The approximately5fm wavelength is smaller than the closest-approach scale; the classical scattering description is appropriate to this estimate.')],'Compare a wave length with the experiment’s spatial scale instead of its beam speed alone.')
m=me/(3*1.813e-4)
R(57,[N('Particle mass',m,'kg','λp/λe=me ve/(mparticle×3ve); solve for mass.'),C('Particle identification','Proton','Electron','Alpha particle','The inferred mass is approximately1839electron masses, about one proton mass.')],'Mass and speed both enter de Broglie momentum.')
parts=[]
for labs,l in [(('a','b'),1e-9),(('c','d'),1e-15)]:
 p=h/l;parts.extend([N(labs[0]+' · Photon energy',p*c/e,'eV','Eγ=pc=hc/λ.'),N(labs[1]+' · Electron kinetic energy',relK(p)/e,'eV','Use exactK=√(p²c²+m²c⁴)−mc²; relativity is essential at1fm.')])
R(58,parts,'The electron’s1fm momentum is far above its rest-momentum scale, so a classical kinetic energy would be invalid.')
p=h/100e-15;gamma=sqrt(1+(p/(mp*c))**2);v=p/(gamma*mp);K=relK(p,mp)
R(59,[N('a · Proton speed',v,'m/s','Usep=h/λ andv=p/(γm).'),N('b · Accelerating potential',K/e,'V','A proton acquires kinetic energyeV.')],'The exact values agree closely with the chapter nonrelativistic estimate at this wavelength.')
# Wavefunction algebra and uncertainty.
R(60,[C('a · Resulting free particle','A particle moving in the negative x direction','A particle moving in the positive x direction','A localized particle at rest','The remaining spatial factor isψ₀ exp(−ikx).'),C('b · Probability-density figure','It stays flat and unchanged','It gains standing-wave nodes','It becomes localized around x=0','A single plane wave has constant|ψ|² regardless of the momentum sign.')],'Removing the positive-momentum component reverses propagation without changing uniform probability density.',pages=[32,19,20])
R(61,[C('Angular-wave-number relation','k=2π√(2m(E−U₀))/h','k=2π√(2m(E+U₀))/h','k=2π(E−U₀)/h','Substitution givesψ″=−k²ψ and k²=2m(E−U₀)/ħ².')],'A constant potential shifts kinetic energy toE−U₀.',pages=[32,19,20])
R(62,[C('Second-derivative identity','ψ″=−k²ψ for both exponential terms','ψ″=+k²ψ for both exponential terms','ψ″=0 for both exponential terms','Each derivative brings±ik; differentiating twice gives−k².')],'Linearity makes both right- and left-moving plane waves solutions of the same free-particle equation.',pages=[32,19,20])
R(63,[C('a · Real and imaginary parts','a=ψ₀cos(kx), b=ψ₀sin(kx)','a=ψ₀sin(kx), b=ψ₀cos(kx)','a=ψ₀cos(kx), b=−ψ₀sin(kx)','Euler’s identity gives exp(ikx)=cos(kx)+i sin(kx).'),C('b · Time-dependent phase','Replace kx by kx−ωt in both trigonometric terms','Replace kx by kx+ωt in both terms','Multiply probability density by cos²(ωt)','Multiplication by exp(−iωt) gives exp(i(kx−ωt)).')],'The time factor changes phase but not the magnitude.',pages=[32,18,20])
R(64,[C('Momentum-energy relationship','k=2π√(2mK)/h','k=2π√(mK)/h','k=2πK/(hc)','p=ħk and K=p²/(2m) imply the stated identity.')],'This proof explicitly assumes a nonrelativistic particle.')
R(65,[C('a · Product with the conjugate','nn*=a²+b², nonnegative and zero only when n=0','nn*=a²−b², sometimes negative','nn*=2iab, always imaginary','The cross terms cancel; the zero complex number is an exception to the wording strictly positive.'),C('b · Product magnitude','|nm|=|n||m|','|nm|=|n|+|m|','|nm|=|n|−|m|','Square both sides and use(nm)(nm)*=(nn*)(mm*).')],'The identity is nonnegative, not strictly positive for every complex number.',scope='Part(a) includes n=0: its magnitude squared is zero, so the source’s word positive means nonnegative.')
R(66,[C('a · Standing-wave probability density','|Ψ|²=4ψ₀²cos²(kx)=2ψ₀²[1+cos(2kx)]','|Ψ|²=4ψ₀²sin²(kx)','|Ψ|²=ψ₀², independent of x','Equal counterpropagating waves add to2ψ₀cos(kx)exp(−iωt).'),N('b · Density period divided by wavelength',.5,'dimensionless','The square of cosine repeats afterΔx=π/k=λ/2.',0),C('c · Node locations','x=(2n+1)λ/4, for integer n','x=nλ/2, for integer n','There are no nodes','cos(kx)=0 at odd quarter wavelengths.'),C('d · Most probable locations','x=nλ/2, for integer n','x=(2n+1)λ/4, for integer n','All locations equally probable','Density maxima occur where|cos(kx)|=1.')],'The spatial pattern is stationary and has nonzero maxima between fixed nodes.',scope='The graph is assessed through its period, nodes and maxima; a freehand plot is not automatically evaluated.',pages=[32,19,20])
R(67,[N('Least momentum uncertainty using the chapter convention',hb/50e-12,'kg·m/s','Eq38-28 usesΔxΔp≈ħ; the rigorous rms lower boundħ/2 is half this value.',accepted=[hb/(2*50e-12)])],'Apply the uncertainty relation using the source’s stated convention.',scope='The chapter uses the approximate bound ħ; the rigorous rms bound ħ/2 is also accepted when Δx and Δp are standard deviations.',pages=[32,21,28])
E=photon(10e-12)
R(68,[N('a · Probe photon energy',E/(1e3*e),'keV','Spatial resolution10pm requires a photon wavelength near10pm.'),N('b · Head-on transferred energy',(E-comp(E,pi))/(1e3*e),'keV','A backward-scattered photon gives the maximum recoil electron energy.'),C('c · Can it trace an unperturbed atomic orbit?','No: the collision transfers far more than ordinary atomic binding energies','Yes: the transferred energy is below a few eV','Yes: the photon changes position without changing momentum','A transfer of tens ofkeV ejects or strongly perturbs an electron bound by only a feweV.')],'The act of measuring the proposed trajectory severely changes that trajectory.')
R(69,[N('Chapter estimate Δp divided by p',1,'dimensionless','Δx=λ/(2π)=ħ/p and the chapterΔxΔp≈ħ giveΔp≈p.',t=.001,accepted=[.5]),C('Assessment of the four momentum outcomes','0, 0.5p and 2p are plausible; 12p is very unlikely, not strictly impossible','All outcomes except p are impossible','12p is as typical as p','An uncertainty is a spread, not a hard allowed interval;12p lies many stated spreads from the mean.')],'The exact rms lower-bound convention would give Δp≥p/2 rather than force equalityp.',scope='The numeric field accepts the chapter estimate1 and rigorous rms-bound value0.5. The uncertainty principle alone does not determine a complete probability distribution.',pages=[32,21,28])
# Electric-potential step and source exponential tunneling approximation.
K=300*e;p=nrp(K)
R(70,[N('a · Kinetic energy',300,'eV','For an electron atV=−200V, potential energy is+200eV; K=500−200eV.',0),N('b · Momentum',p,'kg·m/s','p=√(2mK).'),N('c · Speed',p/me,'m/s','v=p/m at300eV.'),N('d · de Broglie wavelength',h/p,'m','λ=h/p.'),N('e · Angular wave number',p/hb,'rad/m','k=p/ħ.')],'The sign of the electron charge reverses the electric-potential contribution to energy.')
for n,E,U,count in [(71,800*e,600*e,5e5),(72,.5*me*(1.6e7)**2,500*e,3e9)]:
 k1=sqrt(2*me*E)/hb;k2=sqrt(2*me*(E-U))/hb;ref=stepr(E,U)
 R(n,[N('a · Region1 angular wave number',k1,'rad/m','k₁=√(2mE)/ħ.'),N('b · Region2 angular wave number',k2,'rad/m','ForV₂negative, U₂=−eV₂positive; k₂=√(2m(E−U₂))/ħ.'),N('c · Reflection coefficient',ref,'dimensionless','Continuity at one step givesR=[(k₁−k₂)/(k₁+k₂)]².'),N('d · Expected reflected electron count',count*ref,'electrons','Expected count is incident count timesR.')],'The reflected and transmitted flux fractions sum to1.',pages=[33,22,23])
E=.5*me*900**2;U=1.25e-6*e;Rstep=stepr(E,U)
R(73,[N('Transmitted current',.005*(1-Rstep),'A','The source step is−1.25μV, so electron potential energy rises1.25μeV; useT=1−R.')],'The negative electric potential is an upward electron-energy step, but E still exceeds its height.',notice='The original source uses microvolts, not millivolts. The check uses the original −1.25μV step.',reference='Transmitted current ≈4.81mA.')
U=6*e;L=.7e-9;Eapprox=U-(hb*log(.001)/(2*L))**2/(2*me)
lo=1e-12*U;hi=U*(1-1e-12)
for _ in range(150):
 mid=(lo+hi)/2
 if exactT(mid,U,L)<.001:lo=mid
 else:hi=mid
Eexact=(lo+hi)/2
R(74,[N('Incident electron energy',Eapprox/e,'eV','FromT≈exp(−2κL), U−E=[ħln(T)/(2L)]²/(2m).',accepted=[Eexact/e])],'The source exponential approximation and exact rectangular-barrier result use the same positive height and thickness.',scope='The chapter exponential tunneling approximation is the primary result; the exact matched-boundary rectangular-barrier energy is also accepted and differs because of the prefactor.',pages=[33,25,26])
E=3e6*e;U=10e6*e;L=10e-15
parts=[]
for labs,m in [(('a','b','c'),mp),(('d','e','f'),2*mp)]:
 parts.extend([N(labs[0]+' · Transmission coefficient',wkb(E,U,L,m),'dimensionless','The chapter model givesT≈exp[−2L√(2m(U−E))/ħ].',accepted=[exactT(E,U,L,m)]),N(labs[1]+' · Transmitted kinetic energy',3,'MeV','Both outside regions have equal potential energy, so a transmitted particle retains3MeV.',0),N(labs[2]+' · Reflected kinetic energy',3,'MeV','Elastic reflection leaves the kinetic energy3MeV.',0)])
R(75,parts,'The heavier deuteron has the same outside energy but a smaller tunneling probability.',scope='Transmission coefficients accept both the chapter exponential approximation and the exact rectangular-barrier result. Neither transmission nor elastic reflection consumes kinetic energy.',pages=[33,25,26])
E=5*e;U=6*e;L=.7e-9
parts=[]
for lab,m in [('a',mp),('b',me)]:
 Ta=wkb(E,U,L,m);Te=exactT(E,U,L,m)
 parts.append(N(lab+' · Mean wait for one transmitted particle',e/(1000*Ta),'s','Incident rate=I/e; expected wait=1/(rate×T).',accepted=[e/(1000*Te)]))
R(76,parts,'The enormous proton waiting time arises from the square-root mass factor in the tunneling exponent.',scope='Both the source exponential approximation and the exact rectangular-barrier waiting time are accepted.',pages=[33,25,26])
E=5.1*e;U=6.8*e;L=750e-12;T0=wkb(E,U,L);bL=sqrt(2*me*(U-E))*L/hb
finite=[100*(wkb(E,U*1.01,L)/T0-1),100*(wkb(E,U,L*1.01)/T0-1),100*(wkb(E*1.01,U,L)/T0-1)];linear=[-bL*U/(U-E),-2*bL,bL*E/(U-E)]
R(77,[N(lab+' · Percentage change for a1% increase',a,'percent','Re-evaluate the chapter exponentialT after increasing only the stated parameter by1%.',accepted=[b]) for lab,a,b in zip(['a · Barrier height','b · Barrier thickness','c · Incident energy'],finite,linear)],'Increasing height or thickness reduces transmission; increasing incident energy raises it.',scope='A positive1% parameter increase is used. Exact finite changes of the source exponential formula are primary; its first-order differential estimates (about−20%,−10%,+15%) are also accepted.',pages=[33,25,26])
E=.5*me*1200**2;U=4.719e-6*e;L=200e-9;Ta=wkb(E,U,L);Te=exactT(E,U,L)
R(78,[N('Transmitted current',.009*Ta,'A','The original electric potential is−4.719μV, giving a positive4.719μeV electron-energy barrier.',accepted=[.009*Te])],'The source exponential and exact rectangular-barrier solutions both conserve current flux.',scope='The primary result uses the chapter exponential tunneling approximation; the exact rectangular-barrier current is also accepted.',notice='The original source gives −4.719μV, not +4.719mV. The original microscopic barrier and200.0nm thickness are used.',pages=[33,25,26])
# Additional applications and proofs.
R(79,[C('a · Transverse coordinates','Neither y nor z is localized for the exact-momentum plane wave','Both y and z are exactly localized','Only y is localized','Withpy=pz=0 fixed, their uncertainties vanish and transverse positions are delocalized.'),C('b · Three-dimensional matter-wave extent','A plane wave extends throughout space with constant magnitude','The wave is a thin line along x','The wave occupies only the electron radius','An ideal momentum eigenstate has constant density and is not a normalizable localized packet.')],'Zero transverse momentum is not zero transverse position uncertainty.',pages=[33,20,21,28])
R(80,[N('Photon energy',photon(.21)/e,'eV','UseE=hc/λ for the21cm line.')],'The long radio wavelength corresponds to a small positive photon energy.')
coef=h/sqrt(2*me*e)*1e9
R(81,[N('Coefficient in wavelength(nm)=coefficient/√K(eV)',coef,'nm·√eV','λ=h/√(2mK); substituteKjoules=e×KeV and convert meters to nanometers.')],'The nonrelativistic coefficient is about1.226nm√eV.')
R(82,[C('Compton-shift identity','λ′−λ=(h/(mc))(1−cosφ)','λ′−λ=(h/(mc))(1+cosφ)','λ′−λ=(h/(mc))sinφ','Eliminate electron momentum using energy conservation and both Cartesian momentum equations, thenpc=hc/λ.')],'Squaring the vector momentum balance and using the electron energy-momentum relation removes the recoil variables.',pages=[33,9,10])
K=1.5*kB*300
R(83,[N('a · Mean neutron kinetic energy',K/e,'eV','Equipartition gives3kT/2 at300K.'),N('b · Corresponding wavelength',h/nrp(K,mn),'m','Use the momentum corresponding to that mean kinetic energy.')],'This is a representative wavelength at the mean energy, not an independent temperature fit.')
T=300.;p0=101325.;mHe=4.002602*u;lam=h/sqrt(3*mHe*kB*T);meanlam=h*sqrt(2/(pi*mHe*kB*T));spacing=(kB*T/p0)**(1/3)
R(84,[N('a · Representative helium wavelength',lam,'m','The suppliedmeanK=3kT/2 gives representativep=√(3mkT).',accepted=[meanlam]),N('b · Mean atom spacing',spacing,'m','Ideal-gas number density=p/(kT), so representative spacing=(kT/p)^(1/3).'),C('c · Particle approximation','Yes: wavelength is much smaller than the atom spacing','No: wavelength is much greater than the spacing','No: every dilute gas is quantum degenerate','The computed length scales are widely separated, so quantum-wave overlap is weak.')],'The stated room conditions are modeled as300K and1atm.',assumptions=['Room temperature300K, pressure1atm, helium atom mass4.002602u, ideal dilute gas.'],scope='The representative wavelength from the given mean kinetic energy and the exact Maxwell-distribution mean deBroglie wavelength are both accepted; the particle-approximation conclusion is the same.')
ls=[433.9e-9,404.7e-9,365e-9,312.5e-9,253.5e-9];vs=[.55,.73,1.09,1.67,2.57];fs=[c/l for l in ls];fm=sum(fs)/5;vm=sum(vs)/5;slope=sum((f-fm)*(v-vm) for f,v in zip(fs,vs))/sum((f-fm)**2 for f in fs);intercept=vm-slope*fm
R(85,[N('a · Fitted Planck constant',slope,'eV·s','Ordinary least squares ofVs versusf gives slopeh/e, numericallyh in eV·s.'),N('b · Fitted lithium work function',-intercept,'eV','The fittedverticalintercept is−Φ/e.')],'All five original tabulated measurements are used, not just a selected pair.',scope='The plotted line is assessed through its slope and intercept-derived constants; a hand-drawn graph is not automatically graded.')
R(86,[C('Time-factor magnitude','|exp(−iωt)|²=1, hence |Ψ|²=|ψ|²','|exp(−iωt)|²=cos²(ωt)','|Ψ|² grows exponentially with time','A stationary-state time factor has unit complex modulus.')],'Complex conjugation cancels the time phase; probability density is stationary.',pages=[33,18])
R(87,[C('Fractional energy-loss relation','ΔE/E=(hf′/(mc²))(1−cosφ), with ΔE the positive lost energy','ΔE/E=(hf/(mc²))(1+cosφ)','ΔE/E=1−cosφ regardless of frequency','Divide the Compton energy relationE/E′−1=(E/(mc²))(1−cosφ) byE/E′.')],'HereΔE means energy lost, whereas signed photon-energy changes elsewhere are negative.',scope='This proof follows the source convention that ΔE denotes the positive energy loss, not E′−E.')
R(88,[N('Formal bullet wavelength',h/(.040*1000),'m','The formal deBroglie relation givesλ=h/(mv).')],'The result is immeasurably small relative to macroscopic scales.')
R(89,[C('a · Does680nm red light eject electrons?','No','Yes at any intensity','Yes after a sufficiently long exposure','A680nm photon carries less than2.28eV.'),N('b · Cutoff wavelength',h*c/(2.28*e),'m','The cutoff photon energy equals the work function.'),C('c · Cutoff color','Green','Red','Violet','The threshold wavelength is about544nm.')],'Below-threshold single photons cannot cause the ideal single-photon photoelectric effect.')
R(90,[N('Position uncertainty using the chapter convention',.60/(2*pi)/(.5*1.0),'m','The supplied fictitioush givesħ=h/(2π); useΔp=mΔv.',accepted=[.60/(4*pi)/(.5*1.0)])],'The fictitious large Planck constant makes macroscopic uncertainty noticeable.',scope='The source chapter approximateħ bound and rigorous rmsħ/2 lower bound are both accepted.',assumptions=['Fictitioush=.60J·s; nonrelativisticbaseball; Δp=mΔv.'],pages=[33,21,28])
# Conceptual questions, independently derived from original diagrams.
Q=lambda n,p,w,**kw:R(n,p,w,kind='questions',**kw)
Q(1,[C('a · Photon A momentum','Greater; twice photon B momentum','Equal to photon B momentum','Less; half photon B momentum','Photon momentump=E/c.'),C('b · Photon A wavelength','Less; half photon B wavelength','Equal to photon B wavelength','Greater; twice photon B wavelength','Photon wavelengthλ=hc/E.')],'Doubling energy doubles momentum and halves wavelength.')
Q(2,[C('a · Does maximum kinetic energy depend on intensity?','No','Yes, proportional to intensity','Yes, inversely proportional to intensity','Kmax=hf−Φ at fixed frequency and material.'),C('b · Does maximum photocurrent depend on intensity?','Yes','No','Only when the frequency changes','More photons per second can eject more electrons per second.'),C('c · Does stopping potential depend on intensity?','No','Yes, proportional to intensity','Yes, inversely proportional to intensity','Stopping potential measuresKmax/e.'),C('d · Does cutoff frequency depend on intensity?','No','Yes, proportional to intensity','Yes, inversely proportional to intensity','Cutoff frequency isΦ/h, a material property.')],'Single-photon energy depends on frequency; photon number depends on intensity.')
Q(3,[C('Greater maximum electron energy','Potassium','Sodium','Equal for both','Checkpoint2 has the potassiumthreshold at lower frequency, hence a smaller work function.')],'At a fixed above-threshold frequency the smaller work function leaves greaterKmax.',pages=[28,6])
Q(4,[C('Work-function ranking','3 > 2 > 1','1 > 2 > 3','2 > 1 > 3','GreaterΦmeans shorter cutoffλ and lower stopping voltage at the sameλ; curve3 reacheszero first.')],'The cutoff positions in the original graph determine the rank.')
Q(5,[C('Listed property that controls whether emission occurs','Only e: the plate material','a and b: intensity and exposure duration','All five listed properties','At the fixedfrequency, the material work function sets the single-photon emission threshold.')],'The idealphotoelectric threshold does not accumulate subthreshold photon energy over time.')
Q(6,[C('Proton-target recoil-energy curve','It shifts downward to curve3','It shifts upward to curve2','It stays on curve1','At fixed photon energy and angle, a heavier target gains less recoil kinetic energy.')],'The recoil denominator contains targetrestenergymc².')
Q(7,[N('Electron energy-gain fraction in forward scattering',0,'dimensionless','Atφ=0, the Compton wavelength shift and energy transfer vanish.',0)],'No momentum-direction change means no recoil-energy transfer.')
Q(8,[C('Target-mass ranking','3 > 2 > 1','1 > 2 > 3','2 > 1 > 3','Δλ=h(1−cosφ)/(mc); the largest shift corresponds to the smallest target mass.')],'The three curves have the same angle dependence but different inverse-mass scale.')
Q(9,[N('a · Wavelength ratio after doubling kinetic energy',1/sqrt(2),'dimensionless','Nonrelativisticλ∝K^(−1/2).'),N('b · Wavelength ratio after doubling speed',.5,'dimensionless','At fixed mass,λ=h/(mv).',0)],'Kinetic energy is quadratic in speed.')
Q(10,[C('a · Electron opposite the electric field','Decreasing','Increasing','Unchanged','Electron force is oppositeE and parallelv, increasing momentum.'),C('b · Electron along the electric field','Increasing','Decreasing','Unchanged','Electron force opposesv and reduces momentum.'),C('c · Electron along the magnetic field','Unchanged','Increasing','Decreasing','The magnetic force is zero for parallel motion.'),C('d · Electron perpendicular to the magnetic field','Unchanged','Increasing','Decreasing','Magnetic force changes direction but does no work, so momentum magnitude is unchanged.')],'deBroglie wavelength depends on momentum magnitude, not its direction.')
Q(11,[C('Reason minima before a finite barrier are nonzero','Incident and reflected amplitudes are unequal because some flux is transmitted','The electron wavelength is zero','The incident and reflected waves have identical amplitudes','Whenreflection is incomplete, destructive interference cannot cancel two unequal amplitudes fully.')],'The reflected-wave amplitude is smaller than the incident-wave amplitude.',pages=[29,25])
Q(12,[C('Greater wavelength at equal kinetic energy','Electron','Proton','Equal wavelengths','At the intended nonrelativistic energies,λ=h/√(2mK), so the lighter particle has largerλ.')],'Even with the exact energy-momentum formula at equalK, the lower mass has the larger wavelength.')
Q(13,[C('Wavelength ranking','Electron > neutron > alpha particle','Alpha particle > neutron > electron','Neutron > electron > alpha particle','At fixed nonrelativisticK, wavelength is inversely proportional to square-root mass.')],'Use the given equal-energy condition rather than equal-speed ranking.')
Q(14,[C('Region wavelength ranking','2 > 1 > 3','3 > 1 > 2','1 > 2 > 3','For an electron,U=−eV andK=E+eV; more negativeVmeans smallerK and largerλ.')],'The negative charge reverses potential-energy ordering.')
Q(15,[C('Tunneling-probability ranking','a = b = c','a > b > c','c > b > a','The exponent factors areL√(5E−E)=2L√E, (L/2)√(17E−E)=2L√E, and2L√(2E−E)=2L√E.')],'Within the chapter exponential model all three barrier exponents are equal.',scope='The intended ranking uses the chapter exponential approximation. Exact interface prefactors can distinguish barriers with the same exponent.',pages=[29,25])
Q(16,[C('Barrier-height ranking','3 > 2 > 1','1 > 2 > 3','2 > 1 > 3','Equal deBroglie wavelengths mean equal incident energies; faster exponential decay versus thickness means a higher barrier.')],'The lowestTcurve for positiveL has the largest decay constant.')
# Structural and independent numerical checks.
source=json.loads(gzip.decompress((ROOT/'site/questions/physics.json.gz').read_bytes()));expected={q['id'] for q in source if q['chapter']==38}
assert len(rows)==106 and len({r['id'] for r in rows})==106 and {r['id'] for r in rows}==expected
for r in rows:
 assert r['parts'] and r['sourcePages'] and 'Verification:' in r['reasoning']
 for p in r['parts']:
  if p['type']=='numeric':
   assert math.isfinite(p['answer']) and p['tolerance']>=0 and (p['answer']==0 or p['tolerance']<abs(p['answer'])),(r['id'],p)
   assert all(math.isfinite(a) for a in p.get('acceptedValues',[]))
  else:assert p['answer'] in p['options'] and len(set(p['options']))==3,(r['id'],p)
assert abs(stepr(800*e,600*e)-1/9)<1e-14
assert abs(sum([comp(50e3*e,pi),50e3*e-comp(50e3*e,pi)])-50e3*e)<1e-25
assert abs(coef-1.2264)<.001
# Keep prose separated from adjoining numbers without altering symbolic choices.
def readable(s):
 s=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', s)
 s=re.sub(r'(?<=\d)(?=[A-Za-zμ])', ' ', s)
 for a,b in {'Whenreflection':'When reflection','Withpy':'With py','suppliedmeanK':'supplied mean K','negativeVmeans':'negative V means','lowestTcurve':'lowest T curve','positiveL':'positive L','deBroglie':'de Broglie','Fictitioush':'Fictitious h','areL√':'are L√','and2L':'and 2L'}.items():s=s.replace(a,b)
 return s
for r in rows:
 for k in ['reasoning','scope','reviewNotice']:
  if k in r:r[k]=readable(r[k])
 r['assumptions']=[readable(s) for s in r['assumptions']]
 for p in r['parts']:
  p['label']=readable(p['label']);p['explanation']=readable(p['explanation'])
(HERE/'ch38.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'records',sum(len(r['parts']) for r in rows),'fields')
