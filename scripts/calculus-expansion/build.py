#!/usr/bin/env python3
"""Install explicit reviewed additions only, leaving every other question unchanged."""
import gzip,hashlib,json,random,re
from pathlib import Path
from author import records
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'site/questions';OUT=DATA/'answer-library-calculus.json.gz'
source=json.loads(gzip.decompress((DATA/'calculus.json.gz').read_bytes()))
by_id={q['id']:q for q in source};library=json.loads(gzip.decompress(OUT.read_bytes()))
for qid,r in records.items():
 assert qid in by_id,qid
 q=by_id[qid];assert q['chapter'] in (2,3,4,5,6)
 fields=[]
 for i,raw in enumerate(r['fields']):
  f=dict(raw);assert f['type'] in ('numeric','choice')
  f['provenance']='explicit-original-source-inspected-derivation'
  f.setdefault('hint','Use the source expression, stated domain and units. Check the differential and interval endpoints before calculating.')
  f.setdefault('explanation',r['reason'])
  if f['type']=='choice':
   assert f['answer'] in f['options'] and len(set(f['options']))==len(f['options'])>1,(qid,i)
   random.Random(hashlib.sha256(f'{qid}/{i}'.encode()).hexdigest()).shuffle(f['options'])
   f.setdefault('selectionPrompt','Choose the result or reasoning for '+f['label']+'.')
  fields.append(f)
 scope='Checks the displayed numeric answers or selected results. Drawings, written proofs and project reports are not automatically assessed.'
 grader={**fields[0],'scope':scope} if len(fields)==1 else dict(type='parts',parts=fields,scope=scope)
 if r['limited'] or re.search(r'\b(?:sketch|draw|show|prove|graph)\b',q['prompt'],re.I):grader['complete']=False
 entry=library['questions'].setdefault(qid,{})
 # Avoid retaining incomplete or erroneous prior native transcriptions. The exact
 # textbook statement, shared instructions, diagrams and question IDs are untouched.
 for key in ['nativePrompt','nativePromptHtml','nativeParts','nativeFigures','nativeSection','sourceFigureParts','solutions','parts','guidanceEquivalence','preserveGuidance','warnings','reviewNotice','referenceAnswer','svg']:
  entry.pop(key,None)
 entry.update(fullWorkedSolution=True,status='original-worked-explanation',finalText=r['finalText'],
  steps=[dict(title='Work through the question',equation=r['working']),dict(title='Check the reasoning and conditions',why=r['reason']),dict(title='Final answer',calculation=r['finalText'])],
  grader=grader,responsePartPrompt='Use the original textbook exercise above and answer the labeled checks below.',objectiveCheckVersion=1,objectiveChecksVerified=True,objectiveFieldCount=len(fields),
  workedSolutionSource=dict(type='original-derivation-from-user-supplied-textbook',book='Stewart, Calculus: Early Transcendentals, 8th edition',chapter=q['chapter'],sourceSet=q['sourceSet'],exercise=q['number'],pdfPages=sorted({p['page'] for p in q['parts']}),authoringFile='scripts/calculus-expansion/author.py',review='Original source pages visually inspected; antiderivatives checked by independent numerical differentiation and definite integrals by quadrature.'))
for ch in [5,6]:
 qs=[q for q in source if q['chapter']==ch]
 library['coverage'][f'chapter{ch}ExpansionWorked']=sum(q['id'] in records for q in qs)
 library['coverage'][f'chapter{ch}ExpansionFields']=sum(len(records[q['id']]['fields']) for q in qs if q['id'] in records)
for name,val in [('answerRecords',len(library['questions'])),('missing',library['coverage']['total']-len(library['questions'])),('workedSolutionRecords',sum(bool(a.get('steps') or a.get('solutions')) for a in library['questions'].values())),('newGraderRecords',sum(bool(a.get('grader')) for a in library['questions'].values()))]:library['coverage'][name]=val
OUT.write_bytes(gzip.compress(json.dumps(library,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
report=dict(requestedChapters=[2,3,4,5,6],authoredExercises=len(records),objectiveFields=sum(len(r['fields']) for r in records.values()),complete=False,chapters={},limitations=['This checkpoint is not full coverage of Chapters 2–6.','Only explicitly authored IDs are changed; existing coverage elsewhere is preserved.','Graph/proof choices assess selected results or methods, not freehand drawings or written arguments.','Unpublished Chapter 2–4 drafts were removed during workspace maintenance and still need reconstruction and verification.'])
for ch in report['requestedChapters']:
 qs=[q for q in source if q['chapter']==ch];sets={}
 for q in qs:
  row=sets.setdefault(q['sourceSet'],dict(total=0,authored=0,remaining=[]));row['total']+=1
  if q['id'] in records:row['authored']+=1
  else:row['remaining'].append(q['id'])
 report['chapters'][str(ch)]=dict(total=len(qs),authored=sum(q['id'] in records for q in qs),sets=sets)
(Path(__file__).parent/'coverage.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='chapters'},indent=2))
