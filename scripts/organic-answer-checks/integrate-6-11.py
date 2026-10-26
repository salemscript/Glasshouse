"""Merge source-reviewed Organic Chemistry 6–11 checks; preserve source statements."""
import copy, gzip, hashlib, json, random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
path=ROOT/'site/questions/answer-library-organic.json.gz'
data=json.loads(gzip.decompress(path.read_bytes()))
source={q['id']:q for q in json.loads(gzip.decompress((ROOT/'site/questions/organic.json.gz').read_bytes()))}
count=fields=0
for chapter in range(6,12):
    reviews=json.loads((HERE/f'ch{chapter:02}-reviewed.json').read_text())
    reviews=reviews.get('questions',reviews)
    extras=json.loads((HERE/'existing-6-11-reviewed.json').read_text())['questions']
    reviews.update({k:v for k,v in extras.items() if int(k.split('-')[1])==chapter})
    for qid,review in reviews.items():
        a=data['questions'][qid]
        rules=copy.deepcopy(review['fields'])
        for i,r in enumerate(rules):
            for key in ('label','selectionPrompt','explanation'):
                if isinstance(r.get(key),str) and qid=='organic-2-26':
                    r[key]=r[key].replace('terminal carbon','carbon at the other end of the C=C bond (the alpha carbon)')
            r.setdefault('selectionPrompt',r['label'])
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
        if not complete and 'freehand' not in scope.lower(): scope+=' Freehand drawing is not automatically assessed.'
        a['grader']={'type':'parts','parts':rules,'complete':complete,'scope':scope}
        a.pop('sourceFigureParts',None)
        if '<img' in a.get('nativePromptHtml','') or not (a.get('nativePromptHtml') or a.get('nativePrompt')):
            a['sourceFigureParts']=[dict(p,role='figure') for p in source[qid].get('parts',[])]
        related=review.get('sourceRelatedQuestionIds',review.get('relatedSourceQuestions',source[qid].get('relatedQuestions',[])))
        related=list(dict.fromkeys(related+({'organic-6-38':['organic-6-37'],'organic-7-70':['organic-7-69']}.get(qid,[]))))
        if related:
            a['sourceRelatedQuestionIds']=related
            a.setdefault('sourceFigureParts',[])
            for rid in related:
                a['sourceFigureParts'].extend(dict(p,role='figure',contextLabel=source[rid]['number']) for p in source[rid].get('parts',[]))
        if review.get('responsePartPrompt'): a['responsePartPrompt']=review['responsePartPrompt']
        a['chapterStudyVerified']=True
        a['objectiveChecksVerified']=True
        a['answerCheckSource']={'reviewed':'2026-10-26','method':'Source statement and figures reviewed; original answers and explanations; objective choices or numeric checks.', 'references':review.get('references',[])}
        a['sourceTaskCoverage']={'complete':complete,'status':'all-objective-responses-checked' if complete else 'objective-recognition-freehand-unassessed','mappedRecognitionFields':len(rules),'unresolved':[] if complete else ['Freehand construction is not automatically assessed.']}
        a['reviewNotice']=review.get('reviewNotice') or review.get('reviewNotes') or ''
        a['fullWorkedSolution']=False
        a['solutions']=[]
        a['steps']=[]
        for i,r in enumerate(rules):
            explanation=r['explanation']
            answer=str(r['answer'])+((' '+r['unit']) if r.get('unit') else '')
            a['solutions'].append({'fieldIndex':i,'partLabel':r['label'],'title':r['selectionPrompt'],'verified':True,'scope':scope,'briefHint':'Use the exact structure and conditions shown in this question.','method':explanation,'workedSteps':[explanation,'Answer: '+answer],'finalRules':[r],'guidedSteps':[{'title':'Check this response','questionPrompt':r['selectionPrompt'],'text':r['selectionPrompt']+' {{blank:0}}','blanks':[{'label':r['label'],'rule':r}],'why':explanation,'explanation':explanation}],'source':{'book':'organic','chapter':chapter,'exercise':qid,'kind':'source-reviewed-original-answer-check'}})
        count+=1;fields+=len(rules)
data['coverage']['organicChapters6to11Review']={'reviewed':'2026-10-26','updatedQuestions':count,'reviewedFields':fields,'newlyCheckableQuestions':302,'drawingAssessment':'Recognition checks; freehand production remains unassessed.'}
path.write_bytes(gzip.compress(json.dumps(data,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
print(f'Integrated {count} questions / {fields} fields')
