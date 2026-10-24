from common import *
import cmath
I=s.I; pi=s.pi; sqrt=s.sqrt
# Store symbolic expression, output and independently inspect real/imaginary pairs.
COMPLEX_CASES={}
def pair(label,z):
 z=s.expand_complex(z);re=s.simplify(s.re(z));im=s.simplify(s.im(z))
 return [num(label+' · real part a',re),num(label+' · imaginary coefficient b',im)]
def cp(k,z,why):
 COMPLEX_CASES[k]=z
 row('H',k,*pair('a+bi',z),why=why)
expressions={1:(5-6*I)+(3+2*I),2:(4-I/2)-(9+5*I/2),3:(2+5*I)*(4-I),4:(1-2*I)*(8-3*I),5:s.conjugate(12+7*I),6:s.conjugate(2*I*(s.Rational(1,2)-I)),7:(1+4*I)/(3+2*I),8:(3+2*I)/(1-4*I),9:1/(1+I),10:3/(4-3*I),11:I**3,12:I**100,13:s.sqrt(-25),14:s.sqrt(-3)*s.sqrt(-12)}
for k,z in expressions.items():
 why='Combine real and imaginary parts using i²=−1. For a quotient, multiply numerator and denominator by the denominator’s conjugate.'
 if k in (5,6):why='The overbar in the original question conjugates the entire expression: calculate the expression, then reverse its imaginary sign.'
 if k in (13,14):why='Use principal square roots of negative real numbers: √(−a)=i√a for a>0. In #14 the two factors each contribute i, so their product is negative real.'
 cp(k,z,why)
for k,z in {15:12-5*I,16:-1+2*sqrt(2)*I,17:-4*I}.items():
 row('H',k,*pair('Conjugate',s.conjugate(z)),num('Modulus',s.Abs(z)),why='The conjugate reverses the imaginary coefficient; the modulus is √(a²+b²), a nonnegative real number.')
 verify(f'H{k}: modulus squared',s.simplify(s.Abs(z)**2-z*s.conjugate(z))==0)
row('H',18,choice('a · Conjugate of a sum','(a+c)−(b+d)i = conjugate(z)+conjugate(w)','(a+c)+(b+d)i = conjugate(z)+conjugate(w)','(a−c)−(b−d)i = conjugate(z)+conjugate(w)'),choice('b · Conjugate of a product','(ac−bd)−(ad+bc)i = conjugate(z)conjugate(w)','(ac+bd)−(ad+bc)i = conjugate(z)conjugate(w)','(ac−bd)+(ad+bc)i = conjugate(z)conjugate(w)'),choice('c · Positive-integer powers','conjugate(z^n) = conjugate(z)^n by repeated use of part (b)','conjugate(z^n) = −conjugate(z)^n','conjugate(z^n) = n conjugate(z)'),why='Write z=a+bi and w=c+di with real components. Direct addition and multiplication give (a) and (b); apply (b) repeatedly, or induct on n, for (c).',limited=True)
solutions={19:(4*x*x+9,[-3*I/2,3*I/2]),20:(x**4-1,[-1,1,-I,I]),21:(x*x+2*x+5,[-1-2*I,-1+2*I]),22:(2*x*x-2*x+1,[(1-I)/2,(1+I)/2]),23:(x*x+x+2,[(-1-I*sqrt(7))/2,(-1+I*sqrt(7))/2]),24:(x*x+x/2+s.Rational(1,4),[(-1-I*sqrt(3))/4,(-1+I*sqrt(3))/4])}
for k,(poly,roots) in solutions.items():
 ans='{'+', '.join(fmt(z) for z in roots)+'}'
 bad1='{'+', '.join(fmt(z+1) for z in roots)+'}'
 bad2='{'+', '.join(fmt(z*2) for z in roots)+'}'
 row('H',k,choice('Complete solution set',ans,bad1,bad2),why='Use the quadratic formula for the quadratics, or factor x⁴−1=(x²−1)(x²+1). Include every complex root; substitution verifies each root.')
 verify(f'H{k}: root count equals degree',len(set(roots))==s.degree(poly,x))
 for q,z in enumerate(roots):verify(f'H{k}: polynomial residual root {q}',s.simplify(poly.subs(x,z))==0)
def polar(z):
 radius=s.simplify(s.Abs(z));arg=s.simplify(s.arg(s.expand_complex(z)))
 if float(arg)<0:arg+=2*pi
 return radius,arg
def polarfields(label,z):
 radius,arg=polar(z)
 zz=complex(s.N(z,18));verify(label+': independent cmath modulus',abs(float(radius)-abs(zz))<1e-10)
 actual=cmath.phase(zz)%(2*math.pi);verify(label+': independent atan2 angle',abs(float(arg)-actual)<1e-10)
 return [num(label+' · radius r',radius),num(label+' · angle θ in [0,2π), radians',arg)]
for k,z in {25:-3+3*I,26:1-sqrt(3)*I,27:3+4*I,28:8*I}.items():
 row('H',k,*polarfields('Polar form',z),why='Write z=r(cos θ+i sin θ). Compute r=√(a²+b²) and choose the argument in the quadrant fixed by the signs of a and b, normalized to [0,2π).')
zw={29:(sqrt(3)+I,1+sqrt(3)*I),30:(4*sqrt(3)-4*I,8*I),31:(2*sqrt(3)-2*I,-1+I),32:(4*(sqrt(3)+I),-3-3*I)}
for k,(z,w) in zw.items():
 fields=[]
 for label,v in [(f'{k} · z',z),(f'{k} · w',w),(f'{k} · zw',z*w),(f'{k} · z/w',z/w),(f'{k} · 1/z',1/z)]:fields+=polarfields(label,v)
 row('H',k,*fields,why='First find polar forms of z and w. Multiplication multiplies radii and adds arguments; division divides radii and subtracts arguments. The reciprocal has radius 1/|z| and argument −arg(z). Normalize every angle to [0,2π).')
for k,(z,power) in {33:(1+I,20),34:(1-sqrt(3)*I,5),35:(2*sqrt(3)+2*I,5),36:(1-I,8)}.items():
 result=s.expand(z**power);cp(k,result,'Use De Moivre: [r(cos θ+i sin θ)]ⁿ=rⁿ(cos nθ+i sin nθ), then express the result as a+bi.')
 radius,arg=polar(z);verify(f'H{k}: De Moivre vs binomial',abs(complex(s.N(result,18))-cmath.rect(float(radius)**power,float(arg)*power))<1e-7)
roots_cases={37:(1,8,1,0),38:(32,5,2,0),39:(I,3,1,pi/6),40:(1+I,3,2**s.Rational(1,6),pi/12)}
for k,(target,degree,radius,offset) in roots_cases.items():
 step=2*pi/degree
 ans=f'{fmt(radius)}[cos({fmt(offset)}+{fmt(step)}k)+i sin({fmt(offset)}+{fmt(step)}k)], k=0,…,{degree-1}'
 bad1=f'{fmt(radius)}[cos({fmt(offset)}+{fmt(step/2)}k)+i sin({fmt(offset)}+{fmt(step/2)}k)], k=0,…,{degree-1}'
 bad2=f'{fmt(2*radius)}[cos({fmt(offset)}+{fmt(step)}k)+i sin({fmt(offset)}+{fmt(step)}k)], k=0,…,{degree-1}'
 row('H',k,choice('All roots',ans,bad1,bad2),num('Circle radius for the sketch',radius),num('Angular spacing, radians',step),why=f'Take the {degree}th root of the modulus. Divide the argument plus 2πk by {degree}. The {degree} distinct roots are equally spaced on the stated circle; the sketch itself is not automatically assessed.',limited=True)
 for kk in range(degree):
  z=cmath.rect(float(radius),float(offset+step*kk));verify(f'H{k}: root {kk} raised to degree',abs(z**degree-complex(target))<1e-9)
for k,z in {41:s.exp(I*pi/2),42:s.exp(2*pi*I),43:s.exp(I*pi/3),44:s.exp(-I*pi),45:s.exp(2+I*pi),46:s.exp(pi+I)}.items():
 cp(k,z,'Euler’s formula gives e^(a+ib)=e^a(cos b+i sin b). Evaluate the trigonometric factors, keeping the real exponential e^a as the modulus.')
row('H',47,choice('cos(3θ)','cos³θ−3 cos θ sin²θ','cos³θ+3 cos θ sin²θ','3 cos θ−cos³θ'),choice('sin(3θ)','3 cos²θ sin θ−sin³θ','3 cos²θ sin θ+sin³θ','sin³θ−3 cos²θ sin θ'),why='Expand (cos θ+i sin θ)³ and compare its real and imaginary parts with cos(3θ)+i sin(3θ).')
row('H',48,choice('Sum identity','e^(ix)+e^(−ix)=2 cos x','e^(ix)+e^(−ix)=2i sin x','e^(ix)+e^(−ix)=0'),choice('Difference identity','e^(ix)−e^(−ix)=2i sin x','e^(ix)−e^(−ix)=2 cos x','e^(ix)−e^(−ix)=2 sin x'),why='Write Euler’s formula at x and −x, using cos(−x)=cos x and sin(−x)=−sin x. Adding yields the cosine formula; subtracting and dividing by 2i yields the sine formula.',limited=True)
row('H',49,choice('Real part of F′(x)','e^(ax)[a cos(bx)−b sin(bx)]','e^(ax)[a cos(bx)+b sin(bx)]','e^(ax) cos(bx)'),choice('Imaginary coefficient of F′(x)','e^(ax)[a sin(bx)+b cos(bx)]','e^(ax)[a sin(bx)−b cos(bx)]','e^(ax) sin(bx)'),choice('Combined derivative','(a+bi)e^((a+bi)x)=r e^(rx)','(a−bi)e^((a+bi)x)','e^(rx)/r'),why='Use F=e^(ax)(cos bx+i sin bx), differentiate the real and imaginary components by the product and chain rules, then factor (a+bi)F.',limited=True)
row('H',50,choice('a · Complex antiderivative','(1−i)e^((1+i)x)/2 + C','(1+i)e^((1+i)x)/2 + C','e^((1+i)x) + C'),choice('b · Integral of e^x cos x','e^x(cos x+sin x)/2 + C','e^x(cos x−sin x)/2 + C','e^x sin x + C'),choice('b · Integral of e^x sin x','e^x(sin x−cos x)/2 + C','e^x(sin x+cos x)/2 + C','e^x cos x + C'),choice('c · Comparison with integration by parts','Both give the same real antiderivatives; the complex method combines the two integrals in one exponential','The two methods give antiderivatives whose derivatives are different','Integration by parts cannot evaluate these integrals'),why='Divide e^((1+i)x) by the constant 1+i; its reciprocal is (1−i)/2. Expand using Euler and separate the real and imaginary parts. Two integrations by parts yield the same pair. Constants in the real integrals are independent real constants.',limited=True)
# Independent standard-library calculations check all elementary a+bi results.
reference={1:complex(5,-6)+complex(3,2),2:complex(4,-.5)-complex(9,2.5),3:complex(2,5)*complex(4,-1),4:complex(1,-2)*complex(8,-3),5:complex(12,7).conjugate(),6:(2j*(.5-1j)).conjugate(),7:complex(1,4)/complex(3,2),8:complex(3,2)/complex(1,-4),9:1/complex(1,1),10:3/complex(4,-3),11:1j**3,12:1j**100,13:cmath.sqrt(-25),14:cmath.sqrt(-3)*cmath.sqrt(-12),33:(1+1j)**20,34:complex(1,-math.sqrt(3))**5,35:complex(2*math.sqrt(3),2)**5,36:(1-1j)**8,41:cmath.exp(1j*math.pi/2),42:cmath.exp(2j*math.pi),43:cmath.exp(1j*math.pi/3),44:cmath.exp(-1j*math.pi),45:cmath.exp(2+1j*math.pi),46:cmath.exp(math.pi+1j)}
for k,z in COMPLEX_CASES.items():
 exact=complex(s.N(z,20));verify(f'H{k}: independent complex arithmetic',abs(exact-reference[k])<1e-8)
for val in [.13,.7,1.9,3.2]:
 verify(f'H47 cosine triple angle {val}',abs(math.cos(3*val)-(math.cos(val)**3-3*math.cos(val)*math.sin(val)**2))<1e-12)
 verify(f'H47 sine triple angle {val}',abs(math.sin(3*val)-(3*math.cos(val)**2*math.sin(val)-math.sin(val)**3))<1e-12)
for antiderivative,integrand,label in [((1-I)*s.exp((1+I)*x)/2,s.exp((1+I)*x),'H50a'),(s.exp(x)*(s.cos(x)+s.sin(x))/2,s.exp(x)*s.cos(x),'H50b cosine'),(s.exp(x)*(s.sin(x)-s.cos(x))/2,s.exp(x)*s.sin(x),'H50b sine')]:verify(label+' derivative',s.simplify(s.diff(antiderivative,x)-integrand)==0)
aa,bb,cc,dd=s.symbols('a b c d',real=True);z=aa+I*bb;w=cc+I*dd
verify('H18a conjugate sum',s.expand(s.conjugate(z+w)-s.conjugate(z)-s.conjugate(w))==0)
verify('H18b conjugate product',s.expand(s.conjugate(z*w)-s.conjugate(z)*s.conjugate(w))==0)
for k in [1,2,3,4,7]:verify(f'H18c conjugate power n={k}',s.expand(s.conjugate(z**k)-s.conjugate(z)**k)==0)
F=s.exp(aa*x)*(s.cos(bb*x)+I*s.sin(bb*x));verify('H49 real-component differentiation',s.simplify(s.diff(F,x)-(aa+I*bb)*F)==0)
assert len(OUT)==50
save('H')
