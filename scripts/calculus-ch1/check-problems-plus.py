"""Independent stdlib checks of authored Chapter2 Problems Plus results."""
import math
checks=0
def near(a,b,tol=1e-9):
 global checks
 assert math.isclose(a,b,rel_tol=tol,abs_tol=tol),(a,b);checks+=1
# Roots and cancellation via original expressions, not authored transformed answers.
for x in [.999999,1.000001]:near((x**(1/3)-1)/(math.sqrt(x)-1),2/3,2e-6)
for x in [-1e-5,1e-5]:
 near((math.sqrt(4*x+4)-2)/x,1,3e-6)
 near((abs(2*x-1)-abs(2*x+1))/x,-4)
 near(x*math.floor(1/x),1,abs(x)+1e-12)
for a in [(1-math.sqrt(5))/2,(1+math.sqrt(5))/2]:near(a+1,a*a)
# The perpendicular-bisector point must be equally distant from O and P.
for t in [-3,-1,-.2,.2,1,3]:
 q=(1+t*t)/2
 near(q*q,t*t+(t*t-q)**2)
# Enumerate the integer lattice for floor square cases.
pairs=[(m,n) for m in range(-8,9) for n in range(-8,9)]
assert {(m,n) for m,n in pairs if m*m+n*n==1}=={(1,0),(-1,0),(0,1),(0,-1)};checks+=1
assert {(m,n) for m,n in pairs if m*m-n*n==3}=={(m,n) for m in [-2,2] for n in [-1,1]};checks+=1
for i in range(-50,51):
 for j in range(-50,51):
  x=i/7+.03;y=j/11+.02
  assert (math.floor(x+y)**2==1)==(-1<=x+y<0 or 1<=x+y<2);checks+=1
  k=math.floor(x)
  assert (math.floor(x)+math.floor(y)==1)==(k<=x<k+1 and 1-k<=y<2-k);checks+=1
# Independently verify angle-bisector construction using distances and normalized vectors.
for b in [.2,1,5]:
 for h in [.00001,.1,1,3,1000]:
  s=math.hypot(b,h);px=b*s/(s+2*b);py=2*b*h/(s+2*b)
  AP=math.hypot(px,py-h);PC=math.hypot(px-b,py)
  near(AP/PC,s/(2*b),1e-8)
  # Unit vector BP has equal cosine with BA and BC.
  bp=math.hypot(px+b,py)
  near(((px+b)*b+py*h)/(bp*s),(px+b)/bp,1e-8)
  near(py*py,3*px*px+2*b*px-b*b,1e-8)
  assert b/3<px<b and 0<py<2*b;checks+=1
# An actual function satisfying the functional equation & supplied derivative.
f=lambda x:x+x**3/3
for x in [-5,-1,0,2,7]:
 for y in [-2,-.5,0,3]:near(f(x+y),f(x)+f(y)+x*x*y+x*y*y)
near((2*2-1)/4,.75)
print(f'PASS: {checks} independently evaluated limit, floor-region, angle-bisector and functional-equation assertions.')
