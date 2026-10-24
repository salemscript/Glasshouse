#!/usr/bin/env python3
"""Merge explicit chapter patches; never infer a checker from answer prose."""
import argparse
import gzip
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = ROOT / 'site/questions'


def read(path):
    return json.loads(gzip.decompress(path.read_bytes()))


def fields(grader):
    return grader.get('parts', []) if grader.get('type') == 'parts' else [grader]


def validate(qid, grader):
    fs = fields(grader)
    assert fs, (qid, 'no fields')
    for f in fs:
        assert f['type'] in ('numeric', 'choice'), (qid, f)
        assert str(f.get('label', '')).strip(), (qid, 'missing response label')
        if f['type'] == 'numeric':
            assert isinstance(f['answer'], (int, float)) and math.isfinite(f['answer']), qid
            assert math.isfinite(f.get('tolerance', 0)) and f.get('tolerance', 0) >= 0, qid
            assert math.isfinite(f.get('relativeTolerance', 0)) and f.get('relativeTolerance', 0) >= 0, qid
        else:
            assert len(f['options']) >= 2 and len(set(f['options'])) == len(f['options']), qid
            assert f['answer'] in f['options'], qid
            assert all(isinstance(s, str) and s.strip() for s in f['options']), qid
    return fs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    source = read(DATA / 'calculus.json.gz')
    removed=set()
    for correction_path in [HERE/'chapter-11/source-correction.json', HERE/'chapter-16/source-correction.json']:
        correction=json.loads(correction_path.read_text())
        ids=set(correction['removeQuestionIds']); removed.update(ids)
        insertion=next((i for i,q in enumerate(source) if q['id'] in ids),len(source))
        source=[q for q in source if q['id'] not in ids]
        present={q['id'] for q in source}
        source[insertion:insertion]=[q for q in correction['addQuestions'] if q['id'] not in present]
    crops=json.loads((HERE/'source-crop-corrections-14-17.json').read_text())['questions']
    for q in source:
        if q['id'] in crops: q.update(crops[q['id']])
    (DATA/'calculus.json.gz').write_bytes(gzip.compress(json.dumps(source,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
    by_id = {q['id']: q for q in source}
    out = DATA / 'answer-library-calculus.json.gz'
    library = read(out)
    for qid in removed: library['questions'].pop(qid,None)
    changed = set()
    for chapter in range(1, 18):
        paths = [HERE / f'chapter-{chapter:02}.json']
        if chapter == 2:
            paths += [HERE/'chapter-02/problems-plus.json', HERE/'chapter-02/review-concepts.json', HERE/'chapter-02/review-exercises.json']
        if chapter in (3,4,5):
            paths += [HERE/f'chapter-{chapter:02}/review.json']
        if chapter == 6:
            paths += [HERE/'chapter-06/recovered-446.json']
        updates = {}
        for patch in paths:
            if patch.exists():
                payload = json.loads(patch.read_text())
                updates.update(payload.get('questions', payload))
        for qid, update in updates.items():
            assert qid in by_id and by_id[qid]['chapter'] == chapter, qid
            fs = validate(qid, update['grader'])
            entry = library['questions'].setdefault(qid, {})
            entry.update(update)
            entry.update(objectiveChecksVerified=True,
                         objectiveCheckVersion=max(2,update.get('objectiveCheckVersion',2)),
                         objectiveFieldCount=len(fs))
            assert entry.get('responsePartPrompt'), (qid, 'explicit source part contract required')
            changed.add(qid)
    report = {'requestedChapters': list(range(1,18)), 'chapters': {},
              'patchedRecords': len(changed), 'complete': True,
              'assessmentScope': 'Numeric fields and explicit mathematical selections are checked. '
              'A selected result does not automatically assess a freehand graph, written proof, or open-ended construction.'}
    for chapter in range(1, 18):
        qs = [q for q in source if q['chapter'] == chapter]
        missing = []
        count = Counter()
        sets = {}
        for q in qs:
            entry = library['questions'].get(q['id'], {})
            grader = entry.get('grader')
            row = sets.setdefault(q['sourceSet'], {'total': 0, 'checkable': 0, 'fields': 0})
            row['total'] += 1
            if not grader:
                missing.append(q['id'])
                continue
            fs = validate(q['id'], grader)
            row['checkable'] += 1
            row['fields'] += len(fs)
            count.update(f['type'] for f in fs)
        report['chapters'][str(chapter)] = dict(total=len(qs), checkable=len(qs)-len(missing),
            fields=sum(count.values()), fieldTypes=dict(count), sets=sets, missing=missing)
        report['complete'] &= not missing
    if args.require_complete:
        assert report['complete'], 'Missing exact question checks; see chapter source patches.'
    library.setdefault('coverage', {})['chapter1To3ObjectiveChecks'] = {
        ch: {k: v for k, v in result.items() if k in ('total', 'checkable', 'fields')}
        for ch, result in report['chapters'].items() if int(ch)<=3}
    library['coverage']['chapter4To8ObjectiveChecks'] = {ch: {k:v for k,v in result.items() if k in ('total','checkable','fields')} for ch,result in report['chapters'].items() if 4<=int(ch)<=8}
    library['coverage']['chapter9To13ObjectiveChecks'] = {ch: {k:v for k,v in result.items() if k in ('total','checkable','fields')} for ch,result in report['chapters'].items() if 9<=int(ch)<=13}
    library['coverage']['chapter14To17ObjectiveChecks'] = {ch: {k:v for k,v in result.items() if k in ('total','checkable','fields')} for ch,result in report['chapters'].items() if 14<=int(ch)<=17}
    library['coverage']['total'] = len(source)
    library['coverage']['answerRecords'] = len(library['questions'])
    library['coverage']['missing'] = library['coverage']['total'] - len(library['questions'])
    library['coverage']['newGraderRecords'] = sum(bool(v.get('grader')) for v in library['questions'].values())
    library['coverage']['workedSolutionRecords'] = sum(bool(v.get('steps') or v.get('solutions')) for v in library['questions'].values())
    out.write_bytes(gzip.compress(json.dumps(library, ensure_ascii=False, separators=(',', ':')).encode(), mtime=0))
    (HERE / 'coverage.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'chapters'}, indent=2))
    for ch, row in report['chapters'].items():
        print(f"Chapter {ch}: {row['checkable']}/{row['total']} questions; {row['fields']} fields")


if __name__ == '__main__':
    main()
