from common import *
for k,v in {1:18,2:-18,6:1}.items():put('A',k,n('Value',v),why='Evaluate the quantities inside each absolute value first; absolute value returns the nonnegative magnitude, then perform the remaining subtraction.')
for k,e in {3:s.pi,4:s.pi-2,5:5-s.sqrt(5),7:2-x,8:x-2,11:x*x+1}.items():put('A',k,expr('Expression without absolute-value symbols',e),why='Determine the sign of the expression inside the absolute value using the stated domain; negate a negative expression and retain a nonnegative one.')
put('A',9,c('Piecewise expression','−x−1 for x<−1; x+1 for x≥−1','x+1 for every real x','−x−1 for every real x'),why='The sign of x+1 changes at x=−1; both branches agree at that point.')
put('A',10,c('Piecewise expression','1−2x for x<1/2; 2x−1 for x≥1/2','2x−1 for every real x','1−2x for every real x'),why='Split the real line at the zero 2x−1=0, namely x=1/2.')
put('A',12,c('Piecewise expression','1−2x² for −1/√2≤x≤1/√2; 2x²−1 otherwise','1−2x² for every real x','2x²−1 for every real x'),why='The inner expression is nonnegative exactly between its roots ±1/√2; reverse its sign outside.')
rels={13:[2*x+7>3],14:[3*x-11<4],15:[1-x<=2],16:[4-3*x>=6],17:[2*x+1<5*x-8],18:[1+5*x>5-3*x],19:[-1<2*x-5,2*x-5<7],20:[1<3*x+4,3*x+4<=16],21:[0<=1-x,1-x<1],22:[-5<=3-2*x,3-2*x<=9],23:[4*x<2*x+1,2*x+1<=3*x+2],24:[2*x-3<x+4,x+4<3*x-2],25:[(x-1)*(x-2)>0],26:[(2*x+3)*(x-1)>=0],27:[2*x*x+x<=1],28:[x*x<2*x+8],29:[x*x+x+1>0],30:[x*x+x>1],31:[x*x<3],32:[x*x>=5],33:[x**3-x*x<=0],34:[(x+1)*(x-2)*(x+3)>=0],35:[x**3>x],36:[x**3+3*x<4*x*x],37:[1/x<4],38:[-3<1/x,1/x<=1],47:[s.Abs(x)<3],48:[s.Abs(x)>=3],49:[s.Abs(x-4)<1],50:[s.Abs(x-6)<R(1,10)],51:[s.Abs(x+5)>=2],52:[s.Abs(x+1)>=3],53:[s.Abs(2*x-3)<=R(2,5)],54:[s.Abs(5*x-2)<6],55:[1<=s.Abs(x),s.Abs(x)<=4],56:[0<s.Abs(x-5),s.Abs(x-5)<R(1,2)]}
def setfmt(z):
 if z==s.S.Reals:return '(−∞, ∞)'
 if z==s.S.EmptySet:return '∅'
 if isinstance(z,s.Union):return ' ∪ '.join(setfmt(t) for t in z.args)
 if isinstance(z,s.FiniteSet):return '{'+', '.join(fmt(v) for v in z)+'}'
 assert isinstance(z,s.Interval),z
 def v(t):return '−∞' if t==-s.oo else '∞' if t==s.oo else fmt(t)
 return ('(' if z.left_open else '[')+v(z.start)+', '+v(z.end)+(')' if z.right_open else ']')
for k,rr in rels.items():
 ans=s.S.Reals
 for rel in rr:ans=ans.intersect(s.solve_univariate_inequality(rel,x,relational=False))
 wrong=ans.complement(s.S.Reals);alt=s.Interval(-100,100)
 if alt==ans or alt==wrong:alt=s.Interval(100,200)
 put('A',k,c('Solution set in interval notation',setfmt(ans),setfmt(wrong),setfmt(alt)),why='Move all terms to one side, split at real roots and excluded denominator zeros, and test each interval. Include equality endpoints only for ≤ or ≥; never include x=0 in a reciprocal expression.',limited=k<=38)
 # Independently substitute a rational grid plus every exact finite boundary into the source inequalities.
 samples={R(j,8) for j in range(-160,161)}
 for bd in list(ans.boundary):samples.add(bd)
 for t in samples:
  if t==0 and k in (37,38):ok=False
  else:ok=all(bool(rel.subs(x,t)) for rel in rr)
  check(f'A{k} substitution x={t}',bool(ans.contains(t))==ok)
put('A',39,n('Lower Celsius endpoint',10,'°C'),n('Upper Celsius endpoint',35,'°C'),c('Endpoints','Both included','Neither included','Only the lower included'),why='C=(5/9)(F−32) is increasing; F=50 and 95 map to C=10 and 35. The original Fahrenheit inequalities include equality.')
put('A',40,n('Lower Fahrenheit endpoint',68,'°F'),n('Upper Fahrenheit endpoint',86,'°F'),c('Endpoints','Both included','Neither included','Only the upper included'),why='Solve for F=(9/5)C+32; the increasing map takes the closed Celsius interval [20,30] onto [68,86].')
put('A',41,c('Part (a) · Temperature at height h in meters','T(h)=20−h/100 °C, 0≤h≤12000','T(h)=20+h/100 °C','T(h)=20−100h °C'),n('Part (b) · Minimum temperature',-30,'°C'),n('Part (b) · Maximum temperature',20,'°C'),why='A 1°C drop per 100m gives slope −0.01°C/m. The flight reaches 5000m, where T=−30°C; the starting temperature is20°C.')
put('A',42,c('Physical time interval','[0,3] seconds','[−2,3] seconds','[0,4] seconds'),why='128+16t−16t²≥32 reduces to (t−3)(t+2)≤0, giving −2≤t≤3 algebraically. Time since launch satisfies t≥0, leaving [0,3].')
for k,sol in [(43,[-R(3,2),R(3,2)]),(44,[-2,-R(4,3)]),(45,[-R(4,3),2]),(46,[-4,-R(2,5)])]:
 put('A',k,*[n(f'Solution {i+1} (ascending order)',v) for i,v in enumerate(sol)],why='Absolute values agree when their inner expressions agree or are negatives. Solve the resulting linear equations and exclude a zero denominator.')
 eq={43:s.Abs(2*x)-3,44:s.Abs(3*x+5)-1,45:s.Abs(x+3)-s.Abs(2*x+1),46:s.Abs((2*x-1)/(x+1))-3}[k]
 for v in sol:check(f'A{k} exact root {v}',s.simplify(eq.subs(x,v))==0)
put('A',57,c('Solution for positive a,b,c','x≥c(a+b)/(ab)','x≤c(a+b)/(ab)','x≥c(a−b)/(ab)'),why='a(bx−c)≥bc gives abx≥ac+bc. Divide by the positive number ab without reversing the inequality.')
put('A',58,c('Solution for positive a,b,c','(a−c)/b≤x<(2a−c)/b','(a−c)/b<x≤(2a−c)/b','(a+c)/b≤x<(2a+c)/b'),why='Subtract c from all three terms, then divide by b>0; preserve the closed left and open right endpoints.')
put('A',59,c('Solution for negative a,b,c','x>(c−b)/a','x<(c−b)/a','x>(c+b)/a'),why='Subtract b, then divide by a<0, reversing the strict inequality.')
put('A',60,c('Solution for negative a,b,c','x≤b(c−1)/a','x≥b(c−1)/a','x≤b(c+1)/a'),why='Multiply by c<0 to obtain ax+b≥bc; then divide ax≥b(c−1) by a<0 to reverse the inequality again.')
put('A',61,c('Triangle-inequality estimate','|(x+y)−5|≤|x−2|+|y−3|<0.05','|(x+y)−5|=0.05','|(x+y)−5|≥|x−2|+|y−3|'),why='Write (x+y)−5=(x−2)+(y−3), apply the triangle inequality, and add the strict error bounds 0.01+0.04.',limited=True)
put('A',62,c('Valid estimate','|4x+13|≤4|x+3|+1<3','|4x+13|=4|x+3|+1=3','|4x+13|≤4|x+3|−1<1'),why='Since 4x+13=4(x+3)+1, the triangle inequality bounds the absolute value by 4|x+3|+1<4(1/2)+1=3.',limited=True)
put('A',63,c('Why the mean lies strictly between a and b','(a+b)/2−a=(b−a)/2>0 and b−(a+b)/2=(b−a)/2>0','Both differences equal (a−b)/2>0','The mean always equals one endpoint'),why='Subtract each endpoint from the mean in the correct order. Both gaps are half the positive difference b−a.',limited=True)
put('A',64,c('Positive multiplier to apply to a<b','1/(ab)','−1/(ab)','a−b'),c('Resulting inequality','1/b<1/a','1/b>1/a','1/b=1/a'),why='For 0<a<b, ab>0. Rule3 preserves order on multiplying a<b by1/(ab), producing1/b<1/a, which is Rule5.',limited=True,prompt='Assume 0<a<b. Rule3 permits multiplication by a positive number without reversing the inequality; Rule5 states 1/a>1/b. Select the multiplier and the resulting comparison.')
put('A',65,c('Absolute value of a product','√((ab)²)=√(a²)√(b²)=|a||b|','|ab|=a|b| for all real a,b','|ab|=|a|+|b|'),why='Use |u|=√(u²) and the product rule for square roots of nonnegative quantities a²,b².',limited=True)
put('A',66,c('Absolute value of a quotient','|a/b|=√(a²/b²)=|a|/|b|, b≠0','|a/b|=|a|/b for all b≠0','|a/b|=|a|−|b|'),why='For b≠0, b²>0; take the nonnegative square root of a²/b². Division by zero remains excluded.',limited=True)
put('A',67,c('Valid positive-factor argument','b²−a²=(b−a)(b+a)>0','b²−a²=(b−a)(b+a)<0','b²−a²=(b−a)²=0'),why='The assumptions0<a<b make both b−a and b+a positive, so their product is positive.',limited=True)
put('A',68,c('Triangle-inequality rearrangement','|x|=|(x−y)+y|≤|x−y|+|y|, so |x−y|≥|x|−|y|','|x|≥|x−y|+|y|, so |x−y|≤|x|−|y|','|x−y|=|x|−|y| for all real x,y'),why='Express x=(x−y)+y, apply the triangle inequality, then subtract |y|.',limited=True)
put('A',69,c('Sum of p/q and r/s','(ps+rq)/(qs)','(p+r)/(q+s)','(pr)/(qs)'),c('Difference of p/q and r/s','(ps−rq)/(qs)','(p−r)/(q−s)','(ps+rq)/(qs)'),c('Product of p/q and r/s','pr/(qs)','(ps+rq)/(qs)','(p+r)/(qs)'),why='For integer p,q,r,s with q,s nonzero, the common denominator qs is a nonzero integer. Integer sums, differences and products supply integer numerators, proving closure.',limited=True)
put('A',70,c('Part (a) · Sum of two irrational numbers','Not always irrational: √2+(−√2)=0','Always irrational','Always rational'),c('Part (b) · Product of two irrational numbers','Not always irrational: √2·√2=2','Always irrational','Always rational'),why='A single counterexample disproves each always claim. Both √2 and −√2 are irrational, but the displayed sum and product are rational.')
# Independent endpoint and physical checks.
for F,C in [(50,10),(95,35),(68,20),(86,30)]:check(f'temperature {F}',R(5,9)*(F-32)==C)
check('A42 height at t=3',128+16*3-16*9==32)
check('A41 top temperature',20-5000/100==-30)
for a in [1,2,5]:
 for b in [1,3,7]:
  for cc in [1,4]:
   t=R(cc*(a+b),a*b);check('A57 boundary',a*(b*t-cc)==b*cc)
   aa,bb,ccc=-a,-b,-cc;t=R(bb*(ccc-1),aa);check('A60 boundary',(aa*t+bb)/ccc==bb)
out['calculus-section-a-64']['reviewNotice']=out['calculus-section-a-64']['responsePartPrompt']
save('section-a')
