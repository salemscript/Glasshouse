#!/usr/bin/env python3
"""Independent requested second-agent checks for Chapter3 ProblemsPlus15/16/21/29.
Owner of Chapter3 files remains calculus_chapter3. This file edits no answer data.
"""
import hashlib,json,math,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent
rng=random.Random(302316);checks=0

def near(a,b,tol=1e-7):
 global checks
 assert abs(a-b)<=tol*max(1,abs(a),abs(b)),(a,b,tol)
 checks+=1

def diff(fn,x,h=1e-5):return (fn(x-2*h)-8*fn(x-h)+8*fn(x+h)-fn(x+2*h))/(12*h)
#15: metre-consistent exact configuration and implicit/explicit derivatives.
for _ in range(500):
 theta=rng.uniform(-math.pi,math.pi);omega=12*math.pi
 xp=lambda q:.4*(math.cos(q)+math.sqrt(9-math.sin(q)**2))
 alpha=lambda q:math.asin(math.sin(q)/3)
 a=(.4*math.cos(theta),.4*math.sin(theta));pin=xp(theta)
 near(math.hypot(pin-a[0],a[1]),1.2)
 near(diff(alpha,theta)*omega,12*math.pi*math.cos(theta)/math.sqrt(9-math.sin(theta)**2))
 near(diff(xp,theta)*omega,-4.8*math.pi*math.sin(theta)*(1+math.cos(theta)/math.sqrt(9-math.sin(theta)**2)))
near(12*math.pi*math.cos(math.pi/3)/math.sqrt(9-math.sin(math.pi/3)**2),12*math.pi/math.sqrt(33))
#16: tangents and Euclidean distances; no reliance on coordinate-distance cancellation.
for _ in range(500):
 a=rng.uniform(-5,4);b=a+rng.uniform(.1,5);c=rng.uniform(a,b)
 p=((a+b)/2,a*b);q1=((a+c)/2,a*c);q2=((b+c)/2,b*c)
 p1=(a,a*a);p2=(b,b*b)
 dist=lambda p,q:math.hypot(p[0]-q[0],p[1]-q[1])
 near(p[1],2*a*p[0]-a*a);near(p[1],2*b*p[0]-b*b)
 near(q1[1],2*c*q1[0]-c*c);near(q2[1],2*c*q2[0]-c*c)
 near(dist(p,q1)/dist(p,p1),(b-c)/(b-a))
 near(dist(p,q2)/dist(p,p2),(c-a)/(b-a))
 near(dist(p,q1)/dist(p,p1)+dist(p,q2)/dist(p,p2),1)
#21: independently verify intersections, unit tangent vectors, dot/cross acute angle.
angle=lambda u,v:math.degrees(math.acos(min(1,abs(sum(a*b for a,b in zip(u,v)))/(math.hypot(*u)*math.hypot(*v)))))
near(1**2,(1-2)**2);near(angle((1,2),(1,-2)),math.degrees(math.atan(4/3)))
for yy in [-1,1]:
 near(2**2-yy*yy,3);near(2**2-4*2+yy*yy+3,0)
 near(angle((1,2/yy),(1,0)),math.degrees(math.atan(2)))
#29: principal arctangent derivative, both real parameter regimes, away from its poles.
for _ in range(1000):
 a=rng.choice([-1,1])*rng.uniform(1.05,8);x=rng.uniform(-10,10)
 b=math.sqrt(a*a-1);k=a+b
 if abs(k+math.cos(x))<.1:continue
 y=lambda z:z/b-2/b*math.atan(math.sin(z)/(k+math.cos(z)))
 near(k*k-1,2*b*k);near(k*k+1,2*a*k)
 near(diff(y,x),1/(a+math.cos(x)),2e-6)
report=dict(chapter=3,subset='ProblemsPlus15,16,21,29',assertions=checks,sourcePdf='site/books/calculus/chapter-03.pdf',sourceSha256=hashlib.sha256((ROOT/'site/books/calculus/chapter-03.pdf').read_bytes()).hexdigest(),sourceLocalPages=[102,103,104],printedPages=[272,273,274],sourceVisuallyInspected=True,findings={
'15':dict(angularSpeed='12πrad/s',rodAngularVelocityAtPiOver3='12π/√33rad/s',pinPosition='.4[cosθ+√(9−sin²θ)]m',pinVelocity='−4.8πsinθ[1+cosθ/√(9−sin²θ)]m/s',conditions='Right-hand slider branch; α is the positive rod inclination at P shown in the figure. Wheel speed360rev/min=6rev/s.'),
'16':dict(ratio1='(b−c)/(b−a)',ratio2='(c−a)/(b−a)',sum=1,conditions='a<c<b are the contact x-coordinates. Rendered formula has denominators |PP1| and |PP2| respectively; OCR has cross-index corruption.'),
'21':dict(intersectionI=[1,1],acuteAngleIDegrees=53,intersectionsII=[[2,-1],[2,1]],acuteAngleIIDegrees=63,conditions='Use acute nonoriented angle (absolute slope-difference quotient). The printed signed formula describes an oriented angle.'),
'29':dict(derivative='1/(a+cosx)',conditions='For a real original expression require |a|>1 and a+√(a²−1)+cosx≠0. If a>1 denominator is nonzero for all realx; if a<−1 the identity applies on each interval excluding principal-arctangent poles.')},limitations='Independent derivations and numerical consistency checks of these four exercises only. No Chapter3 owned files mutated.')
(HERE/'chapter03-independent-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
