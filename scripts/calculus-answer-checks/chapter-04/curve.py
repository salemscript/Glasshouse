from common import *
def label(v):
 if v==s.oo:return '∞'
 if v==-s.oo:return '−∞'
 if s.sympify(v).has(s.Float):return '≈'+format(float(v),'.6g')
 return fmt(s.simplify(v))
def curve(sec,k,f,critical,inflections,domain=(-s.oo,s.oo),excluded=(),asym=None,limited=True):
 lo,hi=domain
 def val(a):return float(s.N(a))
 pts=sorted(set([lo,hi,*excluded,*critical]),key=val)
 pts2=sorted(set([lo,hi,*excluded,*inflections]),key=val)
 d=s.factor(s.diff(f,x));dd=s.factor(s.diff(f,x,2))
 def signs(expr,ps):
  out=[]
  for a,b in zip(ps[:-1],ps[1:]):
   t=(float(a)+float(b))/2 if a!=-s.oo and b!=s.oo else float(b)-max(1,abs(float(b))) if a==-s.oo and b!=s.oo else float(a)+max(1,abs(float(a))) if b==s.oo and a!=-s.oo else 0
   z=float(expr.subs(x,t).evalf());out.append(1 if z>1e-10 else -1 if z< -1e-10 else 0)
  return out
 ds=signs(d,pts);dds=signs(dd,pts2)
 def intervals(ps,ss,sgn):return ' ∪ '.join('('+label(a)+','+label(b)+')' for a,b,z in zip(ps[:-1],ps[1:],ss) if z==sgn) or 'None'
 inc,dec=intervals(pts,ds,1),intervals(pts,ds,-1);up,down=intervals(pts2,dds,1),intervals(pts2,dds,-1)
 fields=[c('Increasing intervals',inc,dec if dec!=inc else 'All realx','No increasing interval' if inc!='None' else 'All domain intervals'),c('Decreasing intervals',dec,inc if inc!=dec else 'All realx','No decreasing interval' if dec!='None' else 'All domain intervals')]
 extrema=[];ips=[]
 for i,a in enumerate(pts[1:-1],1):
  if a in excluded:continue
  if ds[i-1]!=ds[i] and ds[i-1]*ds[i]<0:extrema.append(('maximum' if ds[i-1]>0 else 'minimum',a,s.simplify(f.subs(x,a))))
 for i,a in enumerate(pts2[1:-1],1):
  if a in excluded:continue
  if dds[i-1]*dds[i]<0:ips.append((a,s.simplify(f.subs(x,a))))
 for typ in ('maximum','minimum'):
  rr=[(a,b) for t,a,b in extrema if t==typ];ans='; '.join('('+label(a)+','+label(b)+')' for a,b in rr) or 'None'
  wrong='; '.join('('+label(a)+','+label(b+1)+')' for a,b in rr) if rr else '(0,0)'
  fields.append(c('Local '+typ+' point(s)',ans,wrong,'All stationary points' if ans!='None' else '(1,1)'))
 fields.extend([c('Concave-up intervals',up,down if down!=up else 'All realx','No concave-up interval' if up!='None' else 'All domain intervals'),c('Concave-down intervals',down,up if up!=down else 'All realx','No concave-down interval' if down!='None' else 'All domain intervals')])
 ans='; '.join('('+label(a)+','+label(b)+')' for a,b in ips) or 'None'
 fields.append(c('Inflection point(s)',ans,'; '.join('('+label(a)+','+label(b+1)+')' for a,b in ips) if ips else '(0,0)','Every point where f′=0'))
 if asym:fields.append(c('Asymptotes / excluded points',asym,'No asymptotes or domain exclusions','Every stationary point is a vertical asymptote'))
 for a in critical:
  if lo<a<hi and a not in excluded:
   try:
    z=s.simplify(d.subs(x,a))
    if z.is_finite:
     if s.sympify(a).has(s.Float):
      assert abs(float(z))<1e-6,(sec,k,a,z)
     else:check(f'{sec}.{k} stationary at'+str(a),z)
   except TypeError:pass
 for a in inflections:
  if lo<a<hi and a not in excluded:
   z=s.simplify(dd.subs(x,a))
   if z.is_finite:
    if s.sympify(a).has(s.Float):
     assert abs(float(z))<1e-7,(sec,k,a,z)
    else:check(f'{sec}.{k} curvature candidate'+str(a),z)
 row(sec,k,*fields,why='Differentiate the source function, split its actual domain at stationary/singular points, and test derivative signs. A local extremum requires a sign change of f′; an inflection requires continuity and a sign change of f″. The coordinate selections check the analytic features, not the freehand drawing.',limited=limited)
 AUDIT[f'calculus-section-4-{sec}-{k}'].update(sourceFunction=str(f),firstDerivative=str(d),secondDerivative=str(dd),derivativeBreaks=[str(z) for z in pts],derivativeSigns=ds,concavityBreaks=[str(z) for z in pts2],concavitySigns=dds)
