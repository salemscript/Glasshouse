#!/usr/bin/env python3
"""Compare candidate source subpart labels to reviewed fields; exceptions require review."""
import gzip,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
source=json.loads(gzip.decompress((ROOT/'site/questions/physics.json.gz').read_bytes()))
updates={r['id']:r for f in HERE.glob('ch1[4-8].json') for r in json.loads(f.read_text())}
rows=[]
for q in source:
 if q['id'] not in updates:continue
 requested=set(re.findall(r'\(([a-z])\)',q.get('prompt','')))
 labeled=set()
 for f in updates[q['id']]['parts']:
  m=re.match(r'^(?:Part )?\(?([a-z])\)?(?:\s|$|[·:])',f['label'],re.I)
  if m:labeled.add(m.group(1).lower())
 missing=sorted(requested-labeled)
 if missing:rows.append({'id':q['id'],'candidateMissingLetters':missing,'labels':[f['label'] for f in updates[q['id']]['parts']],'prompt':q.get('prompt','')})
(HERE/'source-part-candidates-14-18.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
