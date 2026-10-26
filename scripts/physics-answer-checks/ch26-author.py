#!/usr/bin/env python3
"""Original current/resistance derivations; diagrams reviewed chapter PDF20–26."""
import json,math,pathlib,gzip,subprocess
from math import pi,sqrt
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[1]
e=1.602e-19;eps=8.854e-12;rho=1.69e-8;rhoAl=2.75e-8;alpha=.0043;ncu=8.49e28;g=9.8;rows=[]
def N(l,a,u,w,t=None):return dict(label=l,type='numeric',answer=a,unit=u,tolerance=max(abs(a)*.008,1e-30) if t is None else t,explanation=w)
def C(l,a,b,c,w):return dict(label=l,type='choice',answer=a,options=[a,b,c],explanation=w)
def R(n,ps,why,kind='problems',assumptions=None,scope=None):
 page=(21 if n<=6 else 22 if n<=26 else 23 if n<=37 else 24 if n<=53 else 25 if n<=71 else 26) if kind=='problems' else (20 if n<=4 else 21)
 r=dict(id=f'physics-chapter-26-{kind}-{n}',parts=ps,reasoning=why+' Verification: independently substitute the source givens into charge conservation, current-density integrals, Ohm law and energy balance; check SI dimensions.',sourcePages=[page],assumptions=assumptions or ['Use copper resistivity1.69×10⁻⁸Ω·m and temperature coefficient0.0043K⁻¹ from Table26-1 when needed. Uniform current density unless otherwise stated.'])
 if scope:r['scope']=scope
 rows.append(r)
def area(d):return pi*d*d/4
R(1,[N('a · Charge',5*4*60,'C','Q=It; convert4min to240s.'),N('b · Electrons',5*4*60/e,'electrons','N=Q/e.')],'Current measures charge per second.')
R(2,[N('Charging time',4*pi*eps*.10*1000/2e-6,'s','ΔQ=4πε₀RΔV; net current is2.0μA.')],'Subtract the two currents before using the isolated-sphere capacitance.')
R(3,[N('Surface charge density',100e-6/(.50*30),'C/m²','Current equals surface density times swept belt area per second, σwv.')],'The source says100μA, not100mA.')
ds=[204,162,129,102,81,64,51,40];safe=[70,50,35,25,20,15,6,3];gauges=[4,6,8,10,12,14,16,18]
ps=[N(f'Gauge {a} · Safe current density',i/area(d*.0000254),'A/m²','J=I/(πd²/4), with1mil=25.4μm.') for a,d,i in zip(gauges,ds,safe)]
ps+=[C('Gauge with maximum safe current density','Gauge 14','Gauge 4','Gauge 18','Evaluate all eight areas; gauge14 has the largest current per area.')]
R(4,ps,'The requested graph is represented by its eight numerical data points and maximum.',scope='Checks cover all plotted safe-current-density values and the maximizing gauge; a freehand graph is not automatically assessed.')
R(5,[N('a · Current density',2e14*2*e*1e5,'A/m²','Convert ions/cm³ to ions/m³ and use J=nqv.'),C('b · Current direction','North','South','No net current','Positive ions carry conventional current in their direction of motion.'),C('c · Additional quantity required','Beam cross-sectional area perpendicular to motion','Ion mass','Potential at the beam center','I=JA for a uniform beam.')],'The charge per ion is2e.')
R(6,[C('a · Uniform density?','Yes','No, it rises with radius','No, it falls with radius','I proportional to r² means I=Jπr².'),N('b · Current density',.004/(pi*4e-6),'A/m²','J=(di/d(r²))/π; graph endpoint4mA at4mm².')],'The graph is linear in radius squared, not radius.')
R(7,[N('Fuse diameter',sqrt(4*.5/(pi*440e4)),'m','A=I/J and d=√(4A/π);440A/cm²=4.40×10⁶A/m².')],'A smaller area reaches the melting density at a smaller current.')
J=1.2e-10/area(.0025)
R(8,[N('a · Current density',J,'A/m²','J=I/A.'),N('b · Electron drift speed',J/(ncu*e),'m/s','v_d=J/(ne).')],'The extremely small current gives a correspondingly tiny drift speed.')
R(9,[N('Ring current',2*pi*2e5*(.0012)**2*10e-6,'A','dI=J(r)2πrdr=2πBr²dr for the thin ring.')],'Source ring width is10.0μm; treating10mm would exceed the wire diameter.',assumptions=['Thin-ring approximation with r=1.20mm and width10.0μm; exact centered-ring integration differs by less than0.001%.'])
R(10,[N('Outer-annulus current',pi*3e8/2*(.002**4-(.9*.002)**4),'A','Integrate JdA=2πar³dr from.9R toR.')],'Only the specified outer annulus contributes.')
R(11,[N('a · Current for J₀r/R',2*pi*5.5e4*.0034**2/3,'A','Integrate2πJ₀r²/R.'),N('b · Current for J₀(1−r/R)',pi*5.5e4*.0034**2/3,'A','Integrate2πJ₀(r−r²/R).'),C('c · Larger surface current density','J_a=J₀r/R','J_b=J₀(1−r/R)','Both equal','At r=R, J_a=J₀ while J_b=0.')],'Area weighting makes the outward-increasing profile carry twice the total current.')
J=8.7e6*e*470e3
R(12,[N('a · Proton current density',J,'A/m²','J=nev.'),N('b · Current intercepted by Earth',J*pi*(6.37e6)**2,'A','A parallel solar-wind beam intercepts Earth projected disk πR².')],'Use projected area rather than the entire sphere surface.',assumptions=['No magnetic deflection; parallel uniform proton beam; Earth radius6.37×10⁶m.'])
R(13,[N('Travel time',.85*ncu*e*.21e-4/300,'s','t=L/v_d=LneA/I.')],'This is electron drift time, not electromagnetic signal propagation time.')
R(14,[N('Potential difference',.050*2000,'V','V=IR using the stated current and resistance.')],'This is the idealized threshold estimate from the stated resistance, not a universal human safety threshold.')
R(15,[N('Coil resistance',rho*250*2*pi*.12/area(.0013),'Ω','Wire length is250circumferences; R=ρL/A.')],'Neglect insulation thickness as requested.')
Ac=rho/.00015;Aa=rhoAl/.00015
R(16,[N('a · Copper current density',60/Ac,'A/m²','A=ρ/(R/L) with.150Ω/km=.000150Ω/m.'),N('b · Copper mass per length',8960*Ac,'kg/m','λ=mass density times area.'),N('c · Aluminum current density',60/Aa,'A/m²','Use aluminum resistivity2.75×10⁻⁸Ωm.'),N('d · Aluminum mass per length',2600*Aa,'kg/m','Use supplied aluminum density2600kg/m³.')],'Equal resistance per length requires different material cross sections.')
R(17,[N('Conductivity',4*1/(1e-6*2),'S/m','σ=IL/(AV).')],'Conductivity is the reciprocal of resistivity.')
A=area(.006);I=23/.015;res=.015*A/4
R(18,[N('a · Current',I,'A','15mΩ=.015Ω; I=V/R.'),N('b · Current density',I/A,'A/m²','Divide by the6mm-diameter area.'),N('c · Resistivity',res,'Ω·m','ρ=RA/L.'),C('d · Material','Platinum','Copper','Tungsten','Calculatedρ≈1.06×10⁻⁷Ωm matches Table26-1 platinum.')],'All geometrical dimensions are converted to meters.')
R(19,[N('Resistivity',.05*area(.001)/2,'Ω·m','ρ=RA/L with50mΩ=.050Ω.')],'A diameter is not a radius.')
R(20,[C('Resistance in terms of R','2R','R/2','R/4','Half length and quarter area give R′/R=(1/2)/(1/4)=2.')],'The material resistivity is unchanged.')
R(21,[N('Filament temperature',20+((2.9/.30)/1.1-1)/.0045,'°C','Use R=R₂₀[1+α(T−20°C)], α_W=.0045K⁻¹.')],'The operating resistance comes from rated voltage/current; use the chapter linear-temperature approximation.',assumptions=['Tungsten temperature coefficient0.0045K⁻¹; linear resistivity approximation over the stated range.'])
R(22,[N('Water-layer current',160e6*pi*((.0025)**2-.002**2)/(150*800),'A','Water forms an annulus; I=VA/(ρL).')],'Source radii are2.00mm and2.50mm; only water conducts in this model.')
R(23,[N('Resistivity',115/(10*1.4e8),'Ω·m','ρ=E/J=V/(LJ).')],'Wire radius cancels because J is already given.')
R(24,[N('a · Section1 radius',.002*sqrt(1.5/2.5),'m','Same current implies E₁r₁²=E₃r₃²; graph E₁:E₂:E₃=2.5:4:1.5.'),N('b · Section2 radius',.002*sqrt(1.5/4),'m','r₂=r₃√(E₃/E₂).')],'Read the piecewise field levels from the original grid, not the sketch of rod width.')
R(25,[N('New resistance',54,'Ω','Constant volume gives A′=A/3 and R′=9R.')],'Drawing the wire triples its length while conserving material volume.')
R(26,[N('a · Section1 conductivity',3e7*(1)/(0.5),'S/m','Read slopes E₁=.5,E₂=4,E₃=1 V/mm; σE is common.'),N('b · Section2 conductivity',3e7*1/4,'S/m','σ₂=σ₃E₃/E₂.')],'Graph vertices are(0,9),(4,7),(5,3),(8,0) in mm,V.')
R(27,[N('Resistance ratio R_A/R_B',3,'dimensionless','Tube area isπ(2²−1²)/4=3times solid-wire area.')],'Same length/material makes resistance inversely proportional to conducting area.')
R(28,[N('Current',12e-6/3*(pi*.002**2)/rho,'A','E=12μV/3m; I=EA/ρ.')],'Original voltage scale is microvolts.')
R(29,[N('Transported charge',3e-9*(pi*.002**2)/(rho*.02)*.003,'C','Q=It=VAt/(ρL).')],'Use nanovolts and milliseconds.')
R(30,[N('Estimated resistance',.025*16,'Ω','Twelve gauge steps reduce diameter by4, so resistance per length increases16fold.')],'Scale the stated1Ω per1000ft by25ft and the area factor16.')
R(31,[N('a · Current per strand',.75/125,'A','Equal strand resistances share the current equally.'),N('b · Potential difference',.75/125*2.65e-6,'V','Each strand resistance is2.65μΩ in the source.'),N('c · Cable resistance',2.65e-6/125,'Ω','125identical parallel strands give R/N.')],'Original micro-ohm unit is crucial.')
J=2.7e-14*120
R(32,[N('a · Current density',J,'A/m²','J=σE.'),N('b · Common ion drift speed',J/((620+550)*1e6*e),'m/s','Oppositely signed ions moving oppositely contribute currents in the same direction.')],'Both ion populations must be included in ne.')
I=35.8/935;J=I/3.5e-4;vd=J/(5.33e22*e)
R(33,[N('a · Current',I,'A','I=V/R.'),N('b · Current density',J,'A/m²','J=I/A.'),N('c · Electron drift speed',vd,'m/s','v_d=J/(ne); electron velocity is opposite conventional current.'),C('c · Electron drift direction','Toward the higher-potential face','Toward the lower-potential face','No drift','Negative carriers drift opposite E.'),N('d · Electric field magnitude',35.8/.158,'V/m','E=V/L.')],'The source gives area3.50cm²=3.50×10⁻⁴m².')
R(34,[N('Section1 drift speed',(10e-6/2)/rho/(ncu*e)/4,'m/s','Section2 E=10μV/2m; area1 is4times area2, so drift1=drift2/4.')],'Original source potential change is10.0μV, not10mV.')
R(35,[N('Cone resistance',731*.0194/(pi*.002*.0023),'Ω','Integratingρdx/[π(a+(b−a)x/L)²] givesρL/(πab).')],'Verify the formula reduces toρL/(πa²) when a=b.')
Is=30*78e3*.7/(2*pi*35**2*4000)
p=N('Current through swimmer',Is,'A','Use hemispherical J=I/(2πD²), E=ρJ, ΔV≈EΔr, and i=ΔV/R.',t=.0015);p['acceptedValues']=[30*78e3/(2*pi*4000)*(1/(35-.7)-1/35),30*78e3/(2*pi*4000)*(1/35-1/(35+.7))]
R(36,[p],'The thin-width approximation uses Δr/D=.02; exact integration changes the result by about2%.',assumptions=['Uniform hemispherical current spreading and a swimmer width much smaller than D; neglect current redistribution by the swimmer.'],scope='The primary check uses the textbook local-field approximation across the0.70m width; exact inverse-radius integrations for either endpoint convention are accepted.')
R(37,[C('Classical temperature dependence','ρ is proportional to √T','ρ is proportional to T²','ρ is independent of T','With mean free path fixed, τ=ℓ/v and v proportional to√T, soρ=m/(ne²τ) is proportional to√T.')],'This is the classical free-electron-model prediction, not the observed approximately linear metal resistivity.')
R(38,[N('Battery voltage',sqrt(20*(2.5e-3/5)),'V','The graph reaches2.50mJ at5s; ts=4s is the penultimate vertical line. P=.500mW and V=√(PR).')],'Read the full graph endpoint rather than treating ts as its right edge.')
R(39,[N('Cooking time',3*60e3/(120*10),'s','Total required energy triples while total power remains1200W.')],'The problem explicitly holds the power supply rate unchanged.')
R(40,[N('Resistance',100/3**2,'Ω','R=P/I².')],'Power and current specify the resistance directly.')
P=120**2/14
R(41,[N('a · Thermal power',P,'W','P=V²/R.'),N('b · Cost for 5 h',P/1000*5*.05,'USD','Convert power to kW then multiply by hours and stated rate.')],'The quoted rate is the hypothetical problem rate, not a current utility tariff.')
R(42,[C('a · Electron motion through strip','Upward through the resistor','Downward through the resistor','No net drift','The battery positive terminal is upper; conventional current descends, so electrons rise.'),N('b · Electric-field work on electron',12*e,'J','The electron gains positive work eV while moving toward higher potential.'),N('c · Thermal energy delivered',12*e,'J','Steady drift transfers the same field work to thermal energy through collisions.')],'Electron charge is negative, but field work in its drift direction is positive.')
R(43,[N('New dissipation rate',.540*(1.5/3)**2,'W','At fixed R, power scales as voltage squared.')],'Halving voltage quarters resistor power.')
R(44,[N('Transported charge',7/9*5*3600,'C','Q=It=(P/V)t, with5h elapsed.')],'The interval crosses midnight but lasts5hours.')
R(45,[N('a · Current',1250/115,'A','I=P/V.'),N('b · Heating-coil resistance',115**2/1250,'Ω','R=V²/P.'),N('c · Thermal energy in 1 h',1250*3600,'J','Energy=Pt.')],'All input electrical energy is assumed to become thermal energy.')
R(46,[N('a · Electric field',rho*2/2e-6,'V/m','E=ρJ=ρI/A.'),N('b · Thermal energy',2**2*(rho*4/2e-6)*1800,'J','E_th=I²Rt with t=30min.')],'Use Table26-1 copper resistivity.')
R(47,[N('a · Length at75V',75**2/5000*2.6e-6/5e-7,'m','R=V²/P and L=RA/ρ.'),N('b · Length at100V',100**2/5000*2.6e-6/5e-7,'m','Same resistivity and area; length scales withV².')],'The wire cross-sectional area stays fixed.')
R(48,[N('Average current',sqrt((1000*.12*15e-5*2256e3)/(150*.12/(15e-5)*.002)),'A','Set I²Rt=mass times latent heat; mass=ρ_waterLA and R=ρ_eL/A.')],'Heating to boiling is neglected as the source only supplies vaporization energy.')
R(49,[N('a · Monthly cost',.1*31*24*.06,'USD','Energy=.100kW×744h.'),N('b · Bulb resistance',120**2/100,'Ω','R=V²/P.'),N('c · Bulb current',100/120,'A','I=P/V.')],'Use the supplied fictional electricity price.')
R(50,[N('Battery power',(.040+.020)/5,'W','At ts=5s, resistor energies are40mJ and20mJ; add their slopes.')],'Series resistors dissipate the total battery power together.')
Rc=2e-6*1/area(.001);Rd=1e-6*1/area(.0005)
R(51,[N('a · Potential drop1to2',2*Rc,'V','V_C=IR_C.'),N('b · Potential drop2to3',2*Rd,'V','V_D=IR_D.'),N('c · Power1to2',4*Rc,'W','P_C=I²R_C.'),N('d · Power2to3',4*Rd,'W','P_D=I²R_D.')],'The two joined wires carry the same current, despite different current densities.')
R(52,[N('Thermal energy in 1 h',60*(pi*2.75e10*.003**4/2)*3600,'J','I=∫2πar³dr=πaR⁴/2; energy=VIt.')],'Do not replace varying current density with its edge value over the whole area.')
R(53,[N('a · Resistance',120**2/500,'Ω','R=V²/P.'),N('b · Electron crossing rate',500/(120*e),'electrons/s','Rate=I/e=P/(Ve).')],'The rate is a particle count per second, not drift speed.')
R(54,[N('Cut position L',sqrt((5**2/200)/2.5),'m','R=∫₀ᴸ5xdx=2.5L² and requiredR=V²/P=.125Ω.')],'Integrating resistance per length is essential.')
R(55,[N('Power at 200°C',500/(1+4e-4*(200-800)),'W','Reference temperature is800°C, so R₂₀₀=.76R₈₀₀ and P rises by1/.76.')],'Use the coefficient explicitly specified at800°C, not one referenced to20°C.')
A=area(.04*.0254);I=1.2*A/(rho*33)
R(56,[N('a · Current',I,'A','Convert.0400inch diameter to.001016m; I=VA/(ρL).'),N('b · Current density',I/A,'A/m²','J=I/A.'),N('c · Electric field',1.2/33,'V/m','E=V/L.'),N('d · Thermal power',1.2*I,'W','P=VI.')],'All four checks use the same geometry and copper resistivity.')
R(57,[N('Transported charge',18/9*4*3600,'C','Q=(P/V)t.')],'Four hours equals14400seconds.')
Aa=.0052**2;RAl=rhoAl*1.3/Aa
R(58,[N('a · Aluminum resistance',RAl,'Ω','R=ρ_AlL/A.'),N('b · Copper diameter',sqrt(4*rho*1.3/(pi*RAl)),'m','Set copperR equal to aluminumR and solve A_Cu=ρ_CuL/R.')],'Both rods have the same length, but different resistivities.')
res=1.09e-3*area(.0055)/1.6
R(59,[C('a · Material','Silver','Copper','Aluminum','Calculatedρ≈1.62×10⁻⁸Ωm matches silver.'),N('b · Disk resistance',1.62e-8*.001/area(.02),'Ω','Use silverρ from the table and disk thickness as current path length.')],'Current flows between round disk faces, not across its diameter.')
I=1.1e-3*2*pi*.05**2;Vrad=1.1e-3*.05**2/(4*eps);P=I*Vrad
R(60,[C('a · General current','I = ρvπR²','I = ρv2πR','I = ρπR²/v','Charge in a swept cylinder per second givesρvA.'),N('b · Current',I,'A','Use radius.050m, speed2m/s and density.0011C/m³.'),C('c · Radial-field spark transfer during axial flow','No, axial charge motion is perpendicular to the radial field','Yes, every radial field accelerates axial flow','Yes, because a larger pipe always produces a spark','The electrical power is force dot velocity; radial E does no work on axial charge motion.'),N('d · Minimum exit spark power',P,'W','Use ΔV=ρR²/(4ε₀) from the referenced uniform cylindrical charge distribution and P=IΔV.'),N('e · Spark energy in 0.20 s',P*.2,'J','Energy=Pt.'),C('e · Enough energy for the 150 mJ threshold?','Yes','No','Exactly equal','Compare computed spark energy with.150J.'),C('f · Most likely explosion location','At the pipe exit into the silo','Within the straight pipe','Only in the unloading-bin powder cloud','Exit potential change allows energy transfer that radial motion inside does not.')],'The referenced electrostatic potential difference is reconstructed from Gauss law, not an unavailable answer key.',assumptions=['Long uniformly charged cylinder; minimum exit potential change equals center-to-wall differenceρR²/(4ε₀); neglect fringing details.'])
v=sqrt(2*20e6*e/6.645e-27)
R(61,[N('a · Alpha particles striking surface',.25e-6*3/(2*e),'particles','N=It/(2e); source current is.25μA.'),N('b · Particles in 20 cm',.25e-6*.20/(2*e*v),'particles','Number per length is rate/speed; nonrelativistic v=√(2K/mα).'),N('c · Accelerating potential',10e6,'V','qΔV=20MeV with q=2e gives10MV.')],'Use alpha-particle mass6.645×10⁻²⁷kg; kinetic energy is20MeV.')
R(62,[N('Resistance',200**2/3000,'Ω','R=V²/P.')],'The quantity is an operating resistance.')
R(63,[C('General power ratio','P′/P = (V′/V)² × (L/L′)','P′/P = L′/L','Power never changes when wire is shortened','At fixed material and cross section, R is proportional to length and P=V²/R.'),N('Power if original rating is at 120V',2000*80/70,'W','With the same voltage before and after, power rises by80/70.')],'The source does not explicitly specify the original rating voltage; a numerical answer requires it.',assumptions=['The conditional numeric field assumes the original2.0kW rating is at120V; fixed resistivity/cross section.'],scope='The general relationship applies for any original rating voltage. The numeric field assumes the original rating was at120V; other original voltages give different valid results.')
A=area(.010);Rr=3.5e-5*.02/A;I=sqrt(1/Rr)
R(64,[N('a · Current density',I/A,'A/m²','R=ρL/A, I=√(P/R), J=I/A.'),N('b · Potential difference',sqrt(Rr),'V','V=√(PR), P=1W.')],'Radius5mm means diameter10mm.')
R(65,[N('a · New-length ratio',sqrt(30/16),'dimensionless','R′/R=(P′/P)/(I′/I)²=30/16; fixed volume givesR∝L².'),N('b · New-area ratio',1/sqrt(30/16),'dimensionless','A′/A=L/L′ by volume conservation.')],'Voltage changes are compatible withV′/V=30/4=7.5.')
R(66,[N('Engine mechanical power',12*10/.8/746,'hp','Mechanical power=electrical output/efficiency;1hp=746W.')],'The20% loss increases engine power demand, not decreases it.')
R(67,[N('a · Heat-output decrease',100*(1-(110/115)**2),'%','At fixedR, power scales withV².'),C('b · Actual decrease with temperature dependence','Smaller','Larger','Unchanged','Lower voltage cools the element, decreasing its resistance and partly offsetting the power drop.')],'Positive metal temperature coefficient supplies negative thermal feedback.')
R(68,[N('Winding temperature',20+(58/50-1)/alpha,'°C','R/R₂₀=1+α(T−20).')],'Use copperα=.0043K⁻¹.')
R(69,[N('Thermal energy',90**2/400*2*3600,'J','Energy=(V²/R)t.')],'Two hours equals7200seconds.')
A=area(.0052);J=12/A;vd=J/(ncu*e)
R(70,[N('a · Caterpillar end-to-end potential difference',rho*J*.04,'V','ΔV=EL=ρJL.'),C('b · Tail relative to head','Negative','Positive','Same potential','Electron drift is toward higher potential; the head points that way, so the tail is lower.'),N('c · Time to crawl 1 cm',.01/vd,'s','t=distance/v_d with v_d=I/(neA).')],'The caterpillar crawls along electron drift, opposite conventional current.')
R(71,[N('a · Doubling temperature',20+1/alpha,'°C','Set R/R₂₀=2 in the linear law.'),C('b · Same temperature for all copper shapes?','Yes, under the same linear resistivity model','No, longer wires always double first','No, thicker wires always double first','The fractional resistance change is set by materialα, not initial geometry.')],'The model neglects dimensional changes and variation ofα with temperature.')
R(72,[N('Rail resistance',3e-7*1e4/(56e-4),'Ω','R=ρL/A;56cm²=.0056m².')],'Ten kilometers is10000m.')
R(73,[N('Latent heat of vaporization',12*5.2/(21e-6),'J/kg','Electrical power equals mass evaporation rate times latent heat.')],'Assume all coil power vaporizes the liquid at steady boiling.')
R(74,[N('Electron drift time',5*ncu*e/2e6,'s','v_d=J/(ne) and t=L/v_d.')],'Thermal random speeds do not determine net drift travel time.')
R(75,[N('X-ray tube power',7e-3*80e3,'W','P=IV.')],'Convert7mA and80kV to SI.')
R(76,[N('a · Current',(3.1e18+1.1e18)*e,'A','Electron and proton currents add because opposite charges move oppositely.'),C('b · Conventional-current direction','Toward the negative terminal','Away from the negative terminal','No net current','Positive ions move toward the negative terminal; electron motion gives the same conventional current.')],'Count both particle fluxes.')
R(77,[N('Piston speed',(.240**2*550)/(12*g),'m/s','For isothermal ideal gas ΔU=0; coil power equals work rate mgv.')],'As in the textbook model, neglect external atmospheric pressure or assume it is balanced.',assumptions=['Quasistatic ideal-gas expansion; piston external load is its weight mg, with atmosphere absent or balanced. If an uncompensated atmosphere is included, divide power bymg+p_atmA instead.'])
R(78,[N('Belt surface charge density',100e-6/(30*.50),'C/m²','I=σwv, with100μA from the source.')],'This repeats the belt calculation with the same source microampere unit.')
R(79,[N('a · Net current density',2*2.8e21*e*(25+88),'A/m²','Alpha densityn contributes2envα; electron density2n contributes2env_e.'),C('b · Current direction','East','West','Zero','Both positive-ion eastward motion and electron westward motion carry conventional current east.')],'Full ionization gives twice as many electrons as alpha particles.')
aL=1.7e-5;dR=(1+alpha)*(1+aL)/(1+aL)**2-1
R(80,[N('a · Percentage length increase',aL*100,'%','ΔL/L=α_linearΔT.'),N('b · Percentage area increase',2*aL*100,'%','For small expansion ΔA/A≈2α_linearΔT.'),N('c · Percentage resistance increase',dR*100,'%','R′/R=(ρ′/ρ)(L′/L)/(A′/A)≈1+(α_resistivity−α_linear)ΔT.'),C('d · Importance of dimensional changes','Much smaller than the resistivity change; usually negligible here','Larger than the resistivity change','Exactly cancel the resistivity change','Geometrical correction is.0017%, versus roughly.43% resistivity change.')],'Exact isotropic scaling and the first-order formula differ negligibly for a1K change.')
R(81,[N('a · Deuteron arrival rate',15e-6/e,'particles/s','Each deuteron has charge+e; source current is15μA.'),N('b · Thermal power',15e-6*16e6,'W','Every deuteron deposits16MeV; current times equivalent16MV gives power.')],'Source microampere unit must not be read as mA.')
R(82,[N('a · Electrons per pulse',.5*.10e-6/e,'electrons','Q=I_peakΔt, with source pulse duration.10μs.'),N('b · Average current',.5*.10e-6*500,'A','I_avg=I_peak times duty fraction.'),N('c · Average power',.5*.10e-6*500*50e6,'W','Average power=I_avg×50MV.'),N('d · Peak power',.5*50e6,'W','Peak power=I_peak×50MV.')],'Duty fraction is5×10⁻⁵, not.05.')
R(83,[N('Heating time',100/.94**2,'min','Fixed energy and resistance imply t∝1/V².')],'A6% voltage reduction meansV′=.94V, not.06V.')
R(84,[N('a · Time to boiling',2*4190*80/(.8*400),'s','Energy=mcΔT; useful power=.8×400W.'),N('b · Additional time to evaporate half',1*2256e3/(.8*400),'s','One kilogram is vaporized; energy=mL_v.')],'Assume water density1kg/L, specific heat4190J/(kgK), latent heat2256kJ/kg and80% transfer efficiency for both stages.')
R(85,[N('a · Capacitor charge',30e-6*(6+4*.5-2*.5**2),'C','Q=CV; source capacitance is30μF.'),N('b · Current into capacitor',30e-6*(4-4*.5),'A','I=C dV/dt.'),N('c · Supply output power',30e-6*(4-4*.5)*(6+4*.5-2*.5**2),'W','P=VI; both voltage and charging current are positive at.5s.')],'Differentiate the programmed voltage before evaluating current.')
# Conceptual questions: source diagrams on PDF20–21.
R(1,[C('Resistance ranking','A = B = C > A+B = B+C > A+B+C','A > B > C > A+B > B+C > A+B+C','A+B+C > A+B = B+C > A = B = C','Each individual conductor has areaℓ²; combined conducting areas are2ℓ² and3ℓ².')],'Subtract the nested square holes before comparing areas.',kind='questions')
R(2,[C('Resistance ranking','b > a > c','c > a > b','a = b = c','Areas are10,16,18mm² for b,a,c; resistance is inversely proportional to area.')],'The wires have equal length and material.',kind='questions')
rank='Top–bottom > front–back > left–right'
R(3,[C('a · Electric-field ranking',rank,'Left–right > front–back > top–bottom','All equal','Field magnitude is V divided by path length L,2L,3L.'),C('b · Current-density ranking',rank,'Left–right > front–back > top–bottom','All equal','J=σE for the same material.'),C('c · Current ranking',rank,'Left–right > front–back > top–bottom','All equal','For fixed volume, A=volume/path length, so I∝1/path length².'),C('d · Drift-speed ranking',rank,'Left–right > front–back > top–bottom','All equal','Drift speed is J/(ne).')],'Read the3D edge labels: left–right3L, top–bottomL, front–back2L.',kind='questions')
R(4,[C('Net-charge ranking','a = b = c > d','a > b > c > d','d > a = b = c','The signed areas under the four current plots are equal positive areas for a,b,c and zero for d.')],'Net charge is the signed integral of current, not its peak.',kind='questions')
R(5,[C('Effective-current magnitude ranking','a = b = c > d','d > c > b > a','a > b > c > d','Conventional currents are7,7,7,5C/s to the left; negative rightward motion contributes leftward current.')],'Add signed charge fluxes before comparing magnitudes.',kind='questions')
R(6,[C('a · Current ranking','A = B = C','B > C > A','A > C > B','Steady current is conserved.'),C('b · Current-density ranking','B > C > A','A > C > B','A = B = C','J=I/(πr²).'),C('c · Field-magnitude ranking','B > C > A','A > C > B','A = B = C','The same material has E=ρJ.')],'Narrower section requires larger current density and field.',kind='questions')
R(7,[C('a · Field-magnitude ranking','B > A > C','A > B > C','C > A > B','Electric field magnitude is absolute slope of V(x).'),C('b · Current-density ranking','B > A > C','A > B > C','C > A > B','J=σE for copper.')],'The steepest potential slope is in sectionB.',kind='questions')
R(8,[C('a · Field-magnitude ranking','1 = 2 > 3','3 > 2 > 1','1 > 2 > 3','Ratios V/L are1,1,2/3.'),C('b · Current-density ranking','1 = 2 > 3','3 > 2 > 1','1 > 2 > 3','Same material conductivity makes J proportional toE.'),C('c · Drift-speed ranking','1 = 2 > 3','3 > 2 > 1','1 > 2 > 3','Same carrier density makes drift speed proportional toJ.')],'Diameter does not change field or current density when the voltage and length are specified.',kind='questions')
R(9,[C('a · Radius ranking','C > B > A','A > B > C','A = B = C','At fixed current and carrier density, drift speed is inversely proportional to area.'),C('b · Carrier-density ranking','A = B = C','A > B > C','C > B > A','All sections are the same copper material.'),C('c · Field-magnitude ranking','A > B > C','C > B > A','A = B = C','E=ρnev_d.'),C('d · Conductivity ranking','A = B = C','A > B > C','C > B > A','Conductivity is a material property under the stated conditions.')],'The plotted drift speed decreases AtoBtoC.',kind='questions')
R(10,[C('Thermal-power ranking','C > A > B','B > A > C','A = B = C','At fixed voltage P=V²A/(ρL); resistance ratios are.9,1,1.44 for C,A,B.')],'Current and power depend on the productρL.',kind='questions')
R(11,[C('a · Field at center','a = c > b','a > b > c','a = b > c','At r=0, curves a and c start at the same current density, while b starts at zero.'),C('b · Field halfway to surface','a > b > c','a > c > b','a = b > c','Read the curves atR/2; rising b lies above falling c.'),C('c · Field at surface','a = b > c','a > b > c','c > a = b','Curves a,b reach the same edge value while c tends tozero.')],'For the same material, local field magnitude follows localJ(r).',kind='questions')
next(r for r in rows if r['id']=='physics-chapter-26-problems-63')['referenceAnswer']='At the same120V before and after shortening: P′=2.0kW×80/70=2.285714kW, approximately2.3kW. In general P′/P=(V′/V)²(L/L′).'
next(r for r in rows if r['id']=='physics-chapter-26-problems-63')['reviewNotice']='The source omits the original rating voltage, and the printed answer key conflicts with the same-voltage calculation. The numeric check explicitly assumes the original2.0kW rating was at120V; the general relationship covers other ratings.'
next(r for r in rows if r['id']=='physics-chapter-26-problems-13')['parts'][0]['acceptedValues']=[780]
for r in rows:
 n=int(r['id'].split('-')[-1])
 if '-problems-' in r['id'] and n in [15,16,18,21,23,28,29,34,46,56,58,59,68,70,71,80]:r['sourcePages']=sorted(set(r['sourcePages']+[10]))
 if r['id']=='physics-chapter-26-problems-6':r['sourcePages']=[21,22]
 if r['id']=='physics-chapter-26-problems-26':r['sourcePages']=[22,23]
assert len(rows)==96
source=json.loads(gzip.decompress((ROOT/'site/questions/physics.json.gz').read_bytes()));ids={q['id'] for q in source if q['chapter']==26}
assert {r['id'] for r in rows}==ids
for r in rows:
 for p in r['parts']:
  if p['type']=='numeric':assert math.isfinite(p['answer']) and (p['answer']==0 or p['tolerance']<abs(p['answer']))
  else:assert p['answer'] in p['options'] and len(set(p['options']))==3
(HERE/'ch26.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'records',sum(len(r['parts']) for r in rows),'fields')
