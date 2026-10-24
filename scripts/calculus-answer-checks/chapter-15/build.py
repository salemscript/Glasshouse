from common import *
here=Path(__file__).parent
for name in [f'section{i:02}' for i in range(1,10)]+['review','plus']:
 data=json.loads((here/(name+'.json')).read_text()); audit=json.loads((here/(name+'-audit.json')).read_text())
 assert not set(data)&set(A.out)
 A.out.update(data); A.notes.update(audit['notes']); A.integrals.extend(audit['integrals'])
assert set(A.out)==set(A.qs),(set(A.qs)-set(A.out),set(A.out)-set(A.qs))
for qid,item in A.out.items():
 fields=item['grader'].get('parts',[item['grader']])
 assert len(fields)==item['objectiveFieldCount']
 for i,field in enumerate(fields):
  if not field.get('explanation'):field['explanation']=A.notes[qid] or 'Evaluate the labeled quantity using the full original question and the stated bounds.'
  field.setdefault('provenance','explicit-source-inspected-original-answer-contract')
  if field['type']=='numeric':assert math.isfinite(field['answer']) and field['tolerance']>0
  else:assert field['answer'] in field['options'] and len(set(field['options']))==len(field['options'])
A.save()
