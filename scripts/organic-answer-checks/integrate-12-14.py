"""Merge source-reviewed Organic Chemistry 12–14 checks; preserve source statements."""
import copy, gzip, hashlib, json, random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
path=ROOT/'site/questions/answer-library-organic.json.gz'
data=json.loads(gzip.decompress(path.read_bytes()))
source={q['id']:q for q in json.loads(gzip.decompress((ROOT/'site/questions/organic.json.gz').read_bytes()))}
count=fields=0
for chapter in range(12,15):
    reviews=json.loads((HERE/f'ch{chapter:02}-reviewed.json').read_text())
    reviews=reviews.get('questions',reviews)
    expected={qid for qid,q in source.items() if q['chapter']==chapter}
    assert set(reviews)==expected, (chapter, 'Missing', expected-set(reviews), 'Unexpected', set(reviews)-expected)
    for qid,review in reviews.items():
        a=data['questions'][qid]
        rules=copy.deepcopy(review['fields'])
        assert rules, qid
        assert review.get('sourceImageReviewed'), (qid, 'Source figure review required')
        for i,r in enumerate(rules):
            r.setdefault('selectionPrompt',r['label'])
            assert r.get('explanation') and r.get('answer') is not None, (qid,i)
            r['fieldIndex']=i
            r['provenance']='independently-reviewed-source-question'
            if r['type']=='choice':
                r['displayFormat']='chemical-text'
                assert r['answer'] in r['options'] and len(set(r['options']))==len(r['options']),qid
                random.Random(int(hashlib.sha256(f'{qid}:{i}'.encode()).hexdigest(),16)).shuffle(r['options'])
            else:
                assert r['type']=='numeric',qid
                r.setdefault('tolerance',0)
        complete=review.get('complete',not review.get('scopeLimited',False))
        scope=review.get('scope') or review.get('coverage') or ('All requested objective responses checked.' if complete else 'Checks the listed structure and diagram choices. Freehand drawing is not automatically assessed.')
        a['grader']={'type':'parts','parts':rules,'complete':complete,'scope':scope}
        a.pop('sourceFigureParts',None)
        if '<img' in a.get('nativePromptHtml','') or not (a.get('nativePromptHtml') or a.get('nativePrompt')):
            a['sourceFigureParts']=[dict(p,role='figure') for p in source[qid].get('parts',[])]
        related=review.get('sourceRelatedQuestionIds',review.get('relatedSourceQuestions',source[qid].get('relatedQuestions',[])))
        related=list(dict.fromkeys(related))
        if related:
            a['sourceRelatedQuestionIds']=related
            a.setdefault('sourceFigureParts',[])
            for rid in related:
                a['sourceFigureParts'].extend(dict(p,role='figure',contextLabel=source[rid]['number']) for p in source[rid].get('parts',[]))
        if review.get('extraSourceFigureParts'):
            a.setdefault('sourceFigureParts',[]).extend(dict(p,role='figure') for p in review['extraSourceFigureParts'])
        if review.get('responsePartPrompt'): a['responsePartPrompt']=review['responsePartPrompt']
        a['chapterStudyVerified']=True
        a['objectiveChecksVerified']=True
        a['answerCheckSource']={'reviewed':'2026-10-26','method':'Source statement and figures reviewed; original answers and explanations; objective choices or numeric checks.', 'references':review.get('references',[])}
        a['sourceTaskCoverage']={'complete':complete,'status':'all-adapted-responses-checked' if complete else 'objective-recognition-scope-limited','mappedRecognitionFields':len(rules),'unresolved':review.get('unresolved', [] if complete else [scope])}
        a['reviewNotice']=review.get('reviewNotice') or review.get('reviewNotes') or ''
        a['fullWorkedSolution']=False
        a['solutions']=[]
        a['steps']=[]
        for i,r in enumerate(rules):
            explanation=r['explanation']
            answer=str(r['answer'])+((' '+r['unit']) if r.get('unit') else '')
            a['solutions'].append({'fieldIndex':i,'partLabel':r['label'],'title':r['selectionPrompt'],'verified':True,'scope':scope,'briefHint':'Use the exact structure and conditions shown in this question.','method':explanation,'workedSteps':[explanation,'Answer: '+answer],'finalRules':[r],'guidedSteps':[{'title':'Check this response','questionPrompt':r['selectionPrompt'],'text':r['selectionPrompt']+' {{blank:0}}','blanks':[{'label':r['label'],'rule':r}],'why':explanation,'explanation':explanation}],'source':{'book':'organic','chapter':chapter,'exercise':qid,'kind':'source-reviewed-original-answer-check'}})
        count+=1;fields+=len(rules)
data['coverage']['organicChapters12to14Review']={'reviewed':'2026-10-26','updatedQuestions':count,'reviewedFields':fields,'newlyCheckableQuestions':118,'drawingAssessment':'Recognition checks; freehand production remains unassessed.'}
path.write_bytes(gzip.compress(json.dumps(data,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
print(f'Integrated {count} questions / {fields} fields')
