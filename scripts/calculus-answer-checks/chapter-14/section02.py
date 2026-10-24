from common import *
row=lambda k,*fs,**kw:A.row(2,k,*fs,**kw)
row(1,c('Without continuity','The limit does not determine f(3,1), or even require it to be defined','f(3,1)=6 necessarily','f(3,1)=0'),n('With continuity · f(3,1)',6))
row(2,c('a · Outdoor temperature','Normally modeled as continuous in position and time','Always jumps at each longitude line','Always an integer-valued step function'),c('b · Elevation','Can be discontinuous at vertical cliffs or abrupt terrain changes','Must be continuous everywhere','Always discontinuous everywhere'),c('c · Taxi cost','Discontinuous when the meter increments the fare','Always continuous','Independent of time and distance'),limited=True)
row(3,n('Limit',-R(5,2)),c('Reason','Numerator→−5 and denominator→2≠0','Denominator→0','Different paths give different values'),limited=True)
row(4,c('Limit','Does not exist','0','2/3'),c('Path comparison','y=0 gives0; y=x gives2/3','Both paths give0','Both paths give2/3'),limited=True)
vals={5:56,6:-R(2,3),7:pi/2,8:s.exp(2),13:0,14:0,16:0,17:2,19:s.sqrt(3),22:0}
for k,v in vals.items():row(k,n('Limit',v),why={13:'|xy|/sqrt(x²+y²)≤sqrt(x²+y²)/2→0.',14:'Factor x³−y³=(x−y)(x²+xy+y²), so the quotient is x−y.',16:'|xy⁴/(x⁴+y⁴)|≤|x|→0.',17:'Rationalize; the expression equals sqrt(1+x²+y²)+1.',22:'The absolute quotient is bounded by y²z²→0.'}.get(k,'Substitute into functions continuous at the indicated point.'))
paths={9:'y=0 gives0; x=0 gives−2',10:'y=0 gives0; x=0 gives5',11:'y=0 gives0; y=x gives1/2',12:'y=0 gives0; y=x−1 gives1/2',15:'x=0 gives0; x=y² gives1/2',18:'x=0 gives0; x=y⁴ gives1/2',20:'z=0,y=0 gives0; z=0,y=x gives1/2',21:'z=0,y=0 gives0; z=0,y=x gives1/2',23:'y=0 gives2/3; x=0 gives4/5',24:'x=0 gives0; x=y³ gives1/2'}
for k,a in paths.items():row(k,c('Limit','Does not exist','0','1'),c('Path evidence',a,'All paths give0','All paths give1'),limited=k>=23,why='Two admissible approach paths have different limits, disproving a multivariable limit.')
g=2*x+3*y-6
row(25,f('Composite h',g*g+s.sqrt(g)),c('Continuity set','2x+3y≥6','All R²','2x+3y>6'),why='The square root is continuous on its closed nonnegative domain.')
g=(1-x*y)/(1+x*x*y*y)
row(26,f('Composite h',g+s.log(g)),c('Continuity set','xy<1','xy≤1','xy≠0'),why='The denominator is positive; logarithm requires the numerator to be positive.')
row(27,c('Discontinuity line','x=y','x=0','y=0'),c('Behavior','As x−y→0+, f→∞; as x−y→0−, f→0','Both sides approach1','Both sides approach0'),limited=True)
row(28,c('Discontinuity set','x²+y²=1','x=y','Origin only'),c('Behavior','Diverges to+∞ inside and−∞ outside the unit circle','Approaches0 from both sides','Constant on all R²'),limited=True)
dom={29:'All R²',30:'1+x−y≥0',31:'x²+y²≠1',32:'xy≠0',33:'x≥0 and x²+y²≤1',34:'y<1+x',35:'x²+y²+z²≤1',36:'y≥x² and z>0',37:'R² except(0,0)',38:'R² except(0,0)'}
for k,a in dom.items():row(k,c('Continuity set',a,'No points','Only the origin'),why={37:'Off-origin quotient is continuous; its limit at origin is0 whereas f(0,0)=1.',38:'Along y=0 the limit is0; along y=x it is1/3, so discontinuous at origin.'}.get(k,'Use continuity under sums, products and composition, with root/log/inverse-trig/denominator restrictions.'))
for k,v,why in [(39,0,'In polar coordinates the expression is r(cos³θ+sin³θ), uniformly bounded by2r.'),(40,0,'The expression is r²ln(r²), whose one-variable limit is0.'),(41,-1,'Set u=r²; (e^(−u)−1)/u→−1.'),(42,1,'The radial expression sin(r²)/r² tends to1 independent of θ.')]:row(k,n('Limit',v),limited=k==42,why=why)
row(43,c('Continuity','Continuous on all R², including both axes','Discontinuous on both axes','Discontinuous only at origin'),c('Graph behavior','Height1 on axes, with oscillations depending on xy and decaying as |xy| grows','Unbounded at axes','A plane'),limited=True,why='sin u/u has the continuous extension1 at u=0; compose with u=xy.')
row(44,n('a · Limit along specified powers',0),c('b · Counterexample path','y=x⁴/2 has value1 for x≠0','y=0 has value1','y=x⁴ has value1'),c('c · Discontinuity curves','y=0 and y=x⁴, including the origin','y=x and y=−x','Unit circle'),limited=True,why='For0<a<4, |mx^a| dominates x⁴ near0 where real-defined; positive paths lie above the strip and nonpositive paths below it. The interior quartic path remains in the strip.')
row(45,c('Continuity bound','||x|−|a||≤|x−a|; choose δ=ε','||x|−|a||≥|x−a| always','Norm is discontinuous at origin'),limited=True,why='The reverse triangle inequality makes the norm1-Lipschitz.')
row(46,c('Continuity bound','|c·x−c·a|≤|c||x−a|; δ=ε/|c| for c≠0; constant0 if c=0','δ=ε|c| always works','Dot product is discontinuous at c=0'),limited=True,why='Apply Cauchy–Schwarz to c·(x−a).')
save_section('section02')
