from common import *
from scipy.integrate import quad,dblquad
here=Path(__file__).parent;checks=[]
def check(label,actual,expected,tol=1e-7):
 actual=float(actual);expected=float(expected);assert abs(actual-expected)<tol*max(1,abs(expected)),(label,actual,expected)
 checks.append(dict(label=label,actual=actual,expected=expected))
# Integrate the original Cartesian/intrinsic geometry, independently of authoring values.
check('15.7.26 shifted-cylinder sphere volume',dblquad(lambda yy,xx:2*math.sqrt(max(0,1-xx*xx-yy*yy)),0,1,lambda xx:-math.sqrt(xx-xx*xx),lambda xx:math.sqrt(xx-xx*xx))[0],2*pi/3-R(8,9))
check('15.8.47 wavy sphere volume',dblquad(lambda ph,th:(1+.2*math.sin(6*th)*math.sin(5*ph))**3*math.sin(ph)/3,0,2*math.pi,lambda th:0,lambda th:math.pi)[0],136*pi/99)
check('15.4.33 edge exposure k=1',dblquad(lambda rr,th:(20-rr)/20*rr,-math.pi/2,math.pi/2,lambda th:0,lambda th:20*math.cos(th))[0],100*pi-R(1600,9))
check('15.4.32 meeting probability',dblquad(lambda xx,yy:math.exp(-xx)*yy/50,0,10,lambda yy:yy,lambda yy:yy+30)[0],(1-s.exp(-30))*(1-11*s.exp(-10))/50)
check('15.9.15 triangle integral',dblquad(lambda vv,uu:3*(-uu-5*vv),0,1,lambda uu:0,lambda uu:1-uu)[0],-3)
check('15.9.16 parallelogram integral',dblquad(lambda vv,uu:(3*vv-5*uu)/4,-4,4,lambda uu:0,lambda uu:8)[0],192)
check('15.9.19 hyperbolic region',dblquad(lambda yy,xx:xx*yy,1/math.sqrt(3),math.sqrt(3),lambda xx:max(xx,1/xx),lambda xx:min(3*xx,3/xx))[0],2*s.log(3),2e-6)
check('15.9.20 nonlinear transformation',dblquad(lambda vv,uu:vv/(uu*uu),1,2,lambda uu:1,lambda uu:2)[0],.75)
check('15.9.23 linear transformation',dblquad(lambda vv,uu:uu/(5*vv),0,4,lambda uu:1,lambda uu:8)[0],R(8,5)*s.log(8))
check('15.9.24 exponential transform',dblquad(lambda vv,uu:vv*math.exp(uu*vv)/2,0,2,lambda uu:0,lambda uu:3)[0],(s.exp(6)-7)/4)
check('15.9.25 trapezoid transform',dblquad(lambda vv,uu:math.cos(vv)*uu/2,1,2,lambda uu:-1,lambda uu:1)[0],R(3,2)*s.sin(1))
check('15.9.26 elliptical sector',dblquad(lambda rr,th:math.sin(rr*rr)*rr/6,0,math.pi/2,lambda th:0,lambda th:1)[0],pi*(1-s.cos(1))/24)
check('15.9.27 diamond Cartesian',dblquad(lambda yy,xx:math.exp(xx+yy),-1,1,lambda xx:-1+abs(xx),lambda xx:1-abs(xx))[0],s.E-1/s.E)
check('Problems Plus12 double integral',dblquad(lambda yy,xx:1/math.sqrt(1+xx+yy),0,1,lambda xx:0,lambda xx:1)[0],R(4,3)*(3*s.sqrt(3)-4*s.sqrt(2)+1))
check('Problems Plus13 spherical cap factor',quad(lambda zz:math.pi*(1-zz*zz),1/math.sqrt(3),1)[0],pi*(R(2,3)-8/(9*s.sqrt(3))))
check('Three-cylinder project volume',8*quad(lambda zz:quad(lambda yy:min(math.sqrt(1-zz*zz),math.sqrt(1-yy*yy)),0,math.sqrt(1-zz*zz))[0],0,1,epsabs=1e-6)[0],16-8*s.sqrt(2),2e-6)
(here/'independent-special-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print('PASS',len(checks))
