"""Build the complete, reviewed linear-algebra answer library deterministically."""
import copy, gzip, hashlib, json, random
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
inventory=json.loads((HERE/'question-inventory.json').read_text())
data={'book':'linear-algebra','questions':{},'coverage':{'reviewed':'2026-10-26','chapters':[]}}
for chapter in range(1,10):
    reviews=json.loads((HERE/f'ch{chapter:02}-reviewed.json').read_text())['questions']
    expected={q['id'] for q in inventory if q['chapter']==chapter}
    assert set(reviews)==expected,(chapter,'Missing',expected-set(reviews),'Unexpected',set(reviews)-expected)
    fields=0
    for qid,review in reviews.items():
        assert review.get('complete') and review.get('sourceImageReviewed'),qid
        rules=copy.deepcopy(review['fields']);assert rules,qid
        scope=review.get('scope','Checks every requested result. Proof and drawing tasks use reasoning choices; freehand work is not automatically graded.')
        solutions=[];parts=[];steps=[]
        for i,r in enumerate(rules):
            assert r.get('explanation') and r.get('workedSteps') and r.get('answer') is not None,(qid,i)
            r['displayFormat']='linear-text'
            r['fieldIndex']=i;r['provenance']='source-reviewed-original-solution'
            r.setdefault('selectionPrompt',r['label'])
            if r['type']=='choice':
                assert r['answer'] in r['options'] and len(set(r['options']))==len(r['options']) and len(r['options'])>=2,(qid,i)
                random.Random(int(hashlib.sha256(f'{qid}:{i}'.encode()).hexdigest(),16)).shuffle(r['options'])
            else:
                assert r['type']=='numeric',(qid,i)
                r.setdefault('tolerance',0)
            worked=r.pop('workedSteps')
            partsteps=[{'title':f'Step {j+1}','equation':text} for j,text in enumerate(worked)]
            parts.append({'fieldIndex':i,'label':r['selectionPrompt'],'answer':r['answer'],'unit':r.get('unit',''),'steps':partsteps})
            steps.extend(dict(s,title=f"{r['label']} · {s['title']}") for s in partsteps)
            solutions.append({'fieldIndex':i,'partLabel':r['label'],'title':r['selectionPrompt'],'verified':True,'scope':scope,'briefHint':review.get('briefHint','Identify the given matrix or vectors and the property requested. The worked explanation shows the calculation for this exact exercise.'),'method':r['explanation'],'workedSteps':worked,'finalRules':[r],'guidedSteps':[{'title':'Check this result','questionPrompt':r['selectionPrompt'],'text':r['selectionPrompt']+' {{blank:0}}','blanks':[{'label':r['label'],'rule':r}],'why':r['explanation'],'explanation':r['explanation']}],'source':{'book':'linear-algebra','chapter':chapter,'exercise':qid,'kind':'source-reviewed-original-worked-solution'}})
        a={'chapterStudyVerified':True,'objectiveChecksVerified':True,'fullWorkedSolution':True,'responsePartPrompt':review.get('responsePartPrompt',''),'grader':{'type':'parts','parts':rules,'complete':True,'scope':scope},'solutions':solutions,'parts':parts,'steps':steps,'reviewNotice':review.get('reviewNotice',''),'answerCheckSource':{'reviewed':'2026-10-26','method':'Original source-specific solutions; matrix and numerical results checked computationally, reasoning reviewed against the source.','references':review.get('references',[])},'sourceTaskCoverage':{'complete':True,'status':'all-adapted-responses-checked','mappedRecognitionFields':len(rules),'unresolved':[]}}
        if review.get('relatedSourceQuestionIds'):a['sourceRelatedQuestionIds']=review['relatedSourceQuestionIds']
        for key in ['sourceFigureParts','nativePrompt','nativePromptHtml','nativeParts','sourceRelatedQuestionIds']:
            if review.get(key):a[key]=review[key]
        data['questions'][qid]=a;fields+=len(rules)
    data['coverage']['chapters'].append({'chapter':chapter,'questions':len(reviews),'fields':fields,'missing':0})
data['coverage'].update(questions=len(data['questions']),fields=sum(c['fields'] for c in data['coverage']['chapters']),missing=0,assessment='Numeric results and multiple-choice reasoning checks. Freehand proofs and drawings are not automatically graded.')
assert len(data['questions'])==755
(ROOT/'site/questions/answer-library-linear-algebra.json.gz').write_bytes(gzip.compress(json.dumps(data,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
(HERE/'coverage.json').write_text(json.dumps(data['coverage'],indent=2)+'\n')
print(json.dumps(data['coverage'],indent=2))
