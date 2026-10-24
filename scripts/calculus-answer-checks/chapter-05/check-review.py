#!/usr/bin/env python3
"""Independent source-function quadrature and finite differences for review."""
import json
from pathlib import Path
import sympy as s
import mpmath as m
m.mp.dps=60
H=Path(__file__).parent;rows=json.loads((H/'review.json').read_text());audit=json.loads((H/'review-audit.json').read_text());checks=[];fails=[]
def parse(v):return s.sympify(v,locals={'ln':s.log,'arcsin':s.asin,'arctan':s.atan})
for c in audit['independentCases']:
 var=s.Symbol(c['variable']);expr=parse(c['integrand']);fn=s.lambdify(var,expr,'mpmath')
 if c['kind']=='definite':
  l=m.mpf(str(s.N(parse(c['lower']),60)));r=m.mpf(str(s.N(parse(c['upper']),60)));actual=m.quad(fn,[l,(l+r)/2,r]);expected=m.mpf(str(s.N(parse(c['expected']),60)));ok=abs(actual-expected)<m.mpf('1e-40')
  checks.append(dict(number=c['number'],method='independent numerical quadrature',passed=ok,actual=str(actual),expected=str(expected)))
 else:
  primitive=s.lambdify(var,parse(c['primitive']),'mpmath')
  points=[m.mpf('.2'),m.mpf('.4'),m.mpf('.7')]
  if c['number'] in [25,27,28,29,30,35,36,37,42]:points += [m.mpf('1.2'),m.mpf('2.3')]
  if c['number']==25:points += [-m.mpf('.3'),-m.mpf('2')]
  for z in points:
   h=m.mpf('1e-20');got=(primitive(z+h)-primitive(z-h))/(2*h);expected=fn(z);ok=abs(got-expected)<m.mpf('1e-30')*max(1,abs(expected))
   checks.append(dict(number=c['number'],method='central finite difference',x=str(z),passed=ok,actual=str(got),expected=str(expected)))
for c in checks:
 if not c['passed']:fails.append(c)
report=dict(tests=len(checks),failures=fails,checks=checks)
(H/'review-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(len(checks),'independent checks;',len(fails),'failures');print(fails[:5]);assert not fails
