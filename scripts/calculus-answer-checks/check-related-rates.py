#!/usr/bin/env python3
"""Independent numerical checks of high-risk signed rates from source constraints."""
import json
from pathlib import Path
import mpmath as mp
P=Path(__file__).resolve().parent
data=json.loads((P/'chapter-03.json').read_text())['questions']
mp.mp.dps=70
checks=0
def check(number,fn,label=None,magnitude=False):
 global checks
 qid=f'calculus-section-3-9-{number}'
 g=data[qid]['grader'];fs=g['parts'] if g['type']=='parts' else[g]
 f=next(f for f in fs if f['type']=='numeric' and(label is None or f['label']==label))
 h=mp.mpf('1e-20');value=(fn(h)-fn(-h))/(2*h)
 if magnitude:value=abs(value)
 assert abs(value-mp.mpf(str(f['answer'])))<mp.mpf('1e-11')*max(1,abs(value)),(number,f['label'],value,f['answer'])
 checks+=1

# Reconstruct changing geometry/constitutive laws, then use high-precision
# central differences rather than the stored analytic derivative expression.
check(26,lambda t:mp.sqrt((mp.mpf('3.75')+12*t)/15))
check(27,lambda t:-mp.mpf('.3')+mp.sqrt(mp.mpf('.09')+2*(mp.mpf('1.35')+mp.mpf('.2')*t)/10))
check(37,lambda t:mp.mpf(90000)/(150+20*t),magnitude=True)
check(38,lambda t:400*(mp.mpf(80)/(80-10*t))**(mp.mpf(5)/7))
check(40,lambda t:mp.mpf('.007')*(mp.mpf('.12')*(18+mp.mpf('.5')*t)**mp.mpf('2.53'))**(mp.mpf(2)/3))
check(41,lambda t:mp.sqrt(12**2+15**2-2*12*15*mp.cos(mp.pi/3+mp.pi*t/90)))
check(42,lambda t:mp.sqrt((39-mp.sqrt((5+2*t)**2+144))**2-144),magnitude=True)
check(43,lambda t:mp.sqrt(4000**2+(3000+600*t)**2),'(a) slant-distance rate')
check(43,lambda t:mp.atan((3000+600*t)/4000),'(b) elevation-angle rate')
check(44,lambda t:3*mp.tan(mp.atan(mp.mpf(1)/3)+8*mp.pi*t))
check(45,lambda t:5/mp.tan(mp.pi/3-mp.pi*t/6))
check(47,lambda t:mp.sqrt((5*mp.sqrt(3)/2+150*mp.sqrt(3)*t)**2+(mp.mpf('3.5')+150*t)**2))
check(50,lambda t:mp.sqrt(4**2+8**2-2*4*8*mp.cos(mp.pi/6-11*mp.pi*t/360)))
(P/'related-rates-audit.json').write_text(json.dumps({'independentConstraintDifferenceChecks':checks,'precisionDecimalDigits':70,'differenceStep':'1e-20','method':'Reconstruct source geometry or constitutive functions, then calculate symmetric differences independently of stored analytic rates.','verifiedSections':['3.9'],'limitations':['A bounded independent mathematical check; not independent rederivation of all Chapter3 questions.']},indent=2)+'\n')
print(f'PASS: {checks} independent source-constraint signed-rate checks.')
