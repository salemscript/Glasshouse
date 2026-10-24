from common import *
here=ROOT/'scripts/calculus-answer-checks/chapter-16';out={}
for path in [*sorted(here.glob('section[0-9][0-9].json')),here/'review.json',here/'plus.json']:
 data=json.loads(path.read_text());assert not(set(data)&set(out));out.update(data)
assert set(out)==set(A.qs),(set(A.qs)-set(out),set(out)-set(A.qs))
counts=dict(questions=len(out),fields=0,limitedTasks=0,numeric=0,choice=0)
for qid,entry in out.items():
 fields=entry['grader'].get('parts',[entry['grader']]);assert len(fields)==entry['objectiveFieldCount'];counts['fields']+=len(fields);counts['limitedTasks']+=entry['grader'].get('complete') is False
 entry['objectiveCheckVersion']=4
 for f0 in fields:
  counts[f0['type']]+=1
  if f0['type']=='numeric':assert math.isfinite(f0['answer'])
  else:assert f0['answer'] in f0['options'] and len(set(f0['options']))==len(f0['options']), (qid,f0)
(here.parent/'chapter-16.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
counts.update(missing=[],sourceSHA256=hashlib.sha256((ROOT/'site/books/calculus/chapter-16.pdf').read_bytes()).hexdigest(),sourceCorrection='Eight bibliography references replaced by one actual historical writing project.',scope='All actual tasks have explicit answer checks; proofs, plots and reports retain limited-assessment labels.')
(here/'coverage-audit.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
