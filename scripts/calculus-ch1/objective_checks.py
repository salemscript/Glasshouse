"""Authored objective adaptations of the source questions; no grading is inferred from answer prose."""
from collections import defaultdict
from pathlib import Path
import hashlib
import math
import random
import re

HERE=Path(__file__).parent

def load_checks():
    data=defaultdict(list)
    for path in sorted((HERE/'checks').glob('*.tsv')):
        for line in path.read_text().splitlines():
            cells=line.split('\t')
            assert len(cells)==4, (path.name,cells)
            key,answer,other1,other2=cells
            number,sep,part=key.partition('/')
            assert not sep or re.fullmatch('[a-z]',part), key
            rule={'label':part or 'Your answer',
                  'provenance':'source-aligned-authored-objective-response',
                  'hint':'Use the source statement and its domain, units and part labels. The worked solution is available separately.'}
            if answer.startswith('#'):
                value=float(answer[1:])
                tol=float(other2)
                assert math.isfinite(value) and 0<tol<max(100,abs(value)),key
                rule.update(type='numeric',answer=value,tolerance=tol,unit=other1)
            else:
                options=[answer,other1]+([other2] if other2 else [])
                assert all(options) and len(set(options))==len(options),key
                seed=hashlib.sha256((path.stem+'/'+key).encode()).hexdigest()
                random.Random(seed).shuffle(options)
                rule.update(type='choice',answer=answer,options=options,
                            selectionPrompt='Choose the result or reasoning'+(' for part '+part.upper() if part else '')+' that matches the source exercise.')
            data[(path.stem,number)].append(rule)
    return data

def install(entry,source_set,number,group,checks,qid,prompt):
    token=(group+number) if source_set=='chapter-01-review' else number
    fields=checks.get((source_set,token))
    if source_set=='chapter-01-review' and group=='T':
        fields=[dict(entry['grader'])]
    elif source_set=='section-1-5' and 3<=int(number)<=14:
        fields=[dict(entry['grader'])]
    assert fields, (qid,'missing objective contract')
    for rule in fields:rule.setdefault('label','Your answer')
    labels=[r['label'] for r in fields]
    assert len(labels)==len(set(labels)),(qid,'duplicate response label')
    # Numeric/algebraic evaluation list in §1.1 Exercise 25 has no source letters.
    # Give its ten newly separated fields descriptive labels in their source order.
    if source_set=='section-1-1' and number=='25':
        names=['f(2)','f(−2)','f(a)','f(−a)','f(a+1)','2f(a)','f(2a)','f(a²)','[f(a)]²','f(a+h)']
        for rule,name in zip(fields,names):
            rule['label']+=' · '+name
            if rule['type']=='choice':rule['selectionPrompt']='Evaluate '+name+'.'
    if source_set=='section-1-4' and number in {'35','36'}:
        names=['Model','1993 prediction','2020 prediction'] if number=='35' else ['Model','1925 prediction','2020 prediction']
        for rule,name in zip(fields,names):rule['label']+=' · '+name
    for rule in fields:
        rule.setdefault('explanation',entry['steps'][1].get('why',''))
    # ResponseParts uses this explicit contract instead of guessing part labels
    # from duplicated or garbled extracted PDF text. Original source art is untouched.
    entry['responsePartPrompt']='Use the original exercise above and answer the labeled checks below.'
    entry['objectiveCheckVersion']=1
    entry['objectiveChecksVerified']=True
    entry['objectiveFieldCount']=len(fields)
    scope='Checks the displayed numeric answers or selected results. Freehand drawings and written proofs are not automatically assessed.'
    entry['grader']={**fields[0],'scope':scope} if len(fields)==1 else {'type':'parts','parts':fields,'scope':scope}
    # A correct recognition choice is useful feedback, but is not evidence that
    # the learner has independently constructed a proof, drawing or open example.
    if re.search(r'\b(?:sketch|draw|prove|show|give .*examples|discuss)\b',prompt,re.I):
        entry['grader']['complete']=False
    return len(fields)
