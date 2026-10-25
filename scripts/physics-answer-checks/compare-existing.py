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
updates={r['id']:r for f in HERE.glob('ch[0-9][0-9]-[ab].json') for r in json.loads(f.read_text())}
report={'comparedFields':0,'matchingFields':0,'differences':[]}
for q in source:
 if q['id'] not in updates:continue
 old=fs(baseline.get(q['id'],{}).get('grader',q.get('grader')));new=updates[q['id']]['parts']
 for f in old:
  if f['type']!='numeric':continue
  matches=[x for x in new if x['type']=='numeric' and part(x)==part(f)]
  if len(matches)!=1:continue
  n=matches[0];report['comparedFields']+=1
  o=float(f['answer']);v=n['answer'];sameUnit=unit(f.get('unit',''))==unit(n.get('unit',''))
  threshold=max(abs(o)*.01,abs(v)*.01,1e-9)
  if sameUnit and min([abs(v-o)]+[abs(float(a)-o) for a in n.get('acceptedValues',[])])<=threshold:report['matchingFields']+=1
  else:report['differences'].append({'id':q['id'],'part':part(f),'old':o,'oldUnit':f.get('unit',''),'new':v,'newUnit':n.get('unit',''),'newExplanation':n['explanation']})
(HERE/'existing-key-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
