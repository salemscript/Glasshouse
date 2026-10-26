#!/usr/bin/env python3
"""Merge explicit, reviewed physics answer contracts; never infer from answer prose."""
import gzip,json,math,copy,hashlib
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=ROOT/'site/questions'
FILES=[f'ch{ch}.json' for ch in [38,39,40,41,42,43,44]]
def read(p):return json.loads(gzip.decompress(p.read_bytes()))
def fields(g):return g.get('parts',[]) if g.get('type')=='parts' else [g] if g else []
def main():
 source=read(DATA/'physics.json.gz');byid={q['id']:q for q in source};target={q['id'] for q in source if q['chapter'] in [38,39,40,41,42,43,44]}
 library=read(DATA/'answer-library-physics.json.gz');seen=set();report={'chapters':{},'scope':'Every listed chapter 38–44 problem and conceptual question has checks for the requested numeric results or conclusions. Selection checks do not automatically assess a freehand drawing or a written derivation.'}
 for filename in FILES:
  for record in json.loads((HERE/filename).read_text()):
   qid=record['id'];assert qid in target and qid not in seen,qid;seen.add(qid);q=byid[qid]
   parts=copy.deepcopy(record['parts']);assert parts and record['reasoning'] and record['sourcePages'],qid
   for p in parts:
    assert p['type'] in ['numeric','choice'] and p['label'] and p['explanation'],(qid,p)
    p['provenance']='source-reviewed-independent-derivation'
    if p['type']=='numeric':
     assert isinstance(p['answer'],(int,float)) and math.isfinite(p['answer']),qid
     assert p.get('unit') is not None,(qid,'unit')
     p.setdefault('tolerance',max(abs(p['answer'])*.005,1e-8))
     # Accept conventional two/three-significant-figure submissions without widening the continuous tolerance.
     if p['tolerance']>0 and not p.get('noRounding'):
      p['acceptedValues']=list(dict.fromkeys(p.get('acceptedValues',[])+[float(format(p['answer'],'.2g')),float(format(p['answer'],'.3g'))]))
     assert math.isfinite(p['tolerance']) and p['tolerance']>=0,(qid,p)
     assert p['answer']==0 or p['tolerance']<abs(p['answer']),(qid,'nonzero answer tolerance admits zero',p)
    else:
     assert p['answer'] in p['options'] and len(set(p['options']))==len(p['options'])>=2,(qid,p)
     # Stable option order prevents the correct answer always occupying the first position.
     p['options'].sort(key=lambda option:hashlib.sha256((qid+'|'+p['label']+'|'+option).encode()).digest())
   entry=library['questions'].setdefault(qid,{})
   entry.update(grader={'type':'parts','parts':parts},objectiveChecksVerified=True,objectiveCheckVersion=1,objectiveFieldCount=len(parts),
    responsePartPrompt='Use the complete original textbook question and its diagrams above. Supply each labeled quantity or select the stated conclusion.',
    answerCheckSource={'type':'source-reviewed-original-calculation','title':'Fundamentals of Physics, Halliday, Resnick and Walker, 10th edition','chapter':q['chapter'],'exercise':q['number'],'kind':q['kind'],'chapterPdfPages':record['sourcePages'],'sourceFile':f"books/physics/chapter-{q['chapter']:02}.pdf"},
    objectiveCheckReasoning=record['reasoning'],objectiveCheckAssumptions=record.get('assumptions',[]))
   if record.get('scope'):entry['grader']['scope']=record['scope']
   if record.get('nativePrompt'):entry['nativePrompt']=record['nativePrompt']
   for key in ['reviewNotice','referenceAnswer']:
    if record.get(key):entry[key]=record[key]
 assert seen==target,sorted(target-seen)
 for ch in [38,39,40,41,42,43,44]:
  qs=[q for q in source if q['chapter']==ch];f=[p for q in qs for p in fields(library['questions'][q['id']]['grader'])]
  report['chapters'][str(ch)]={'total':len(qs),'checkable':len(qs),'problems':sum(q['kind']=='Problems' for q in qs),'conceptualQuestions':sum(q['kind']=='Questions' for q in qs),'fields':len(f),'fieldTypes':dict(Counter(p['type'] for p in f)),'missing':[]}
 cov=library['coverage'];cov.update(total=len(source),answerRecords=len(library['questions']),missing=len(source)-len(library['questions']),newGraderRecords=sum(bool(v.get('grader')) for v in library['questions'].values()),workedSolutionRecords=sum(bool(v.get('solutions') or v.get('steps')) for v in library['questions'].values()),chapter38To44ObjectiveChecks=report['chapters'])
 (DATA/'answer-library-physics.json.gz').write_bytes(gzip.compress(json.dumps(library,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
 (HERE/'coverage-38-44.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
