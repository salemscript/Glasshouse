#!/usr/bin/env python3
"""Report differences from existing keys for human review, not automatic acceptance."""
import json,gzip,re,subprocess,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
source=json.loads(gzip.decompress((ROOT/'site/questions/physics.json.gz').read_bytes()))
baseline=json.loads(gzip.decompress(subprocess.check_output(['git','show','HEAD:site/questions/answer-library-physics.json.gz'],cwd=ROOT)))['questions']
def fs(g):return g.get('parts',[]) if g and g.get('type')=='parts' else [g] if g else []
def part(x):
 s=x.get('label','');m=re.match(r'^(?:Part )?\(?([a-z])\)?(?:\s|$|[·:])',s,re.I);return m.group(1).lower() if m else ''
def unit(s):return s.replace(' ','').replace('·','*').replace('²','^2').replace('³','^3').replace('−','-').replace('N*m','Nm').replace('kg*m^2','kgm^2').replace('degrees','deg').replace('degree','deg').replace('°','deg')
def si(s):
 u=unit(s)
 table={'N':('force',1),'kN':('force',1e3),'Pa':('pressure',1),'kPa':('pressure',1e3),'MPa':('pressure',1e6),'m':('length',1),'cm':('length',.01),'mm':('length',.001),'km':('length',1000),'s':('time',1),'ms':('time',.001),'μs':('time',1e-6),'kg':('mass',1),'g':('mass',.001),'J':('energy',1),'kJ':('energy',1000),'mJ':('energy',.001),'W':('power',1),'kW':('power',1000),'m/s':('speed',1),'cm/s':('speed',.01),'m/s^2':('acceleration',1),'cm/s^2':('acceleration',.01)}
 return table.get(u,(u,1))
updates={r['id']:r for f in HERE.glob('ch1[4-8].json') for r in json.loads(f.read_text())}
report={'comparedFields':0,'matchingFields':0,'differences':[]}
for q in source:
 if q['id'] not in updates:continue
 old=fs(baseline.get(q['id'],{}).get('grader',q.get('grader')));new=updates[q['id']]['parts']
 for f in old:
  if f['type']!='numeric':continue
  matches=[x for x in new if x['type']=='numeric' and part(x)==part(f)]
  if len(matches)!=1:continue
  n=matches[0];report['comparedFields']+=1
  ou,oscale=si(f.get('unit',''));nu,nscale=si(n.get('unit',''));o=float(f['answer'])*oscale;v=n['answer']*nscale;sameUnit=ou==nu
  threshold=max(abs(o)*.01,abs(v)*.01,1e-15)
  if sameUnit and min([abs(v-o)]+[abs(float(a)*nscale-o) for a in n.get('acceptedValues',[])])<=threshold:report['matchingFields']+=1
  else:report['differences'].append({'id':q['id'],'part':part(f),'old':float(f['answer']),'oldUnit':f.get('unit',''),'new':n['answer'],'newUnit':n.get('unit',''),'newExplanation':n['explanation']})
(HERE/'existing-key-comparison-14-18.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
