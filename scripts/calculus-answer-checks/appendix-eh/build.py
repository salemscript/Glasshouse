from pathlib import Path
import json,gzip
here=Path(__file__).resolve().parent
root=here.parents[2]
source=json.load(gzip.open(root/'site/questions/calculus.json.gz'))
expected={q['id'] for q in source if q['chapter']=='appendix' and q['section'] in ['E','H']}
out={}
for sec in ['e','h']:
 data=json.loads((here/(sec+'.json')).read_text());assert not (set(data)&set(out));out.update(data)
assert set(out)==expected,(sorted(expected-set(out)),sorted(set(out)-expected))
(here.parent/'appendix-eh.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(len(out),'tasks',sum(q['objectiveFieldCount'] for q in out.values()),'fields')
