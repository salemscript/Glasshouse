from pathlib import Path
import json,gzip
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
a={}
for f in ['section-a','section-b']:a.update(json.loads((HERE/(f+'.json')).read_text()))
src=json.load(gzip.open(ROOT/'site/questions/calculus.json.gz'))
ids={q['id'] for q in src if q['chapter']=='appendix' and q['section'] in ['A','B']}
assert ids==set(a)
(HERE.parent/'appendix-ab.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
print(len(a),'tasks',sum(v['objectiveFieldCount'] for v in a.values()),'fields')
