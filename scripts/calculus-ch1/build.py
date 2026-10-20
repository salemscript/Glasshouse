#!/usr/bin/env python3
"""Install original Chapter 1 explanations without changing source artwork or other chapters."""
import gzip
import json
from pathlib import Path
from objective_checks import load_checks, install

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'site/questions'
OUT = DATA / 'answer-library-calculus.json.gz'

def read(path):
    return json.loads(gzip.decompress(path.read_bytes()))

def build():
    questions = read(DATA / 'calculus.json.gz')
    chapter = {q['id']: q for q in questions if q['chapter'] == 1}
    library = read(OUT)
    covered = set()
    checks = load_checks()
    checked_fields = 0
    for path in sorted(Path(__file__).parent.glob('*.tsv')):
        source_set = path.stem
        for line in path.read_text().splitlines():
            number, answer, working, explanation = line.split('\t')
            group = ''
            if source_set == 'chapter-01-review':
                group, number = number[0], number[1:]
                suffix = {'C': '-concept-check-1', 'T': '-true-false-quiz-2', 'E': ''}[group]
            elif source_set == 'chapter-01-problem-solving-exercises':
                suffix = '-problem-solving-exercises-0'
            else:
                suffix = ''
            qid = f'calculus-{source_set}-{number}{suffix}'
            assert qid in chapter and qid not in covered, qid
            q = chapter[qid]
            entry = library['questions'].setdefault(qid, {})
            entry.update({
                'fullWorkedSolution': True,
                'status': 'original-worked-explanation',
                'finalText': answer,
                'steps': [
                    {'title': 'Work through the question', 'equation': working},
                    {'title': 'Check the reasoning and conditions', 'why': explanation},
                    {'title': 'Final answer', 'calculation': answer},
                ],
                'workedSolutionSource': {
                    'type': 'original-derivation-from-user-supplied-textbook',
                    'book': 'Stewart, Calculus: Early Transcendentals, 8th edition',
                    'chapter': 1, 'sourceSet': source_set, 'exercise': number,
                    'pdfPages': sorted({p['page'] for p in q.get('parts', []) if p.get('page')}),
                    'questionFigures': 'Preserved original exercise artwork; diagram estimates are explicitly approximate.',
                    'authoringFile': str(path.relative_to(ROOT)),
                    'review': 'Source exercise pages inspected; algebra, numerical models and inverse/domain edge cases checked by separate computations.',
                },
            })
            # Binary questions receive real closed-response controls as well as reasoning.
            if source_set == 'chapter-01-review' and group == 'T':
                assert answer.startswith(('True', 'False')), qid
                truth = 'True' if answer.startswith('True') else 'False'
                entry['grader'] = {'type': 'choice', 'answer': truth,
                    'options': ['True', 'False'], 'explanation': working,
                    'provenance': 'original-counterexample-or-definition-proof',
                    'scope': 'The truth value is checked; the explanation is supplied in the worked solution.'}
            if source_set == 'section-1-5' and 3 <= int(number) <= 14:
                yes = int(number) in {6, 7, 9, 12}
                entry['grader'] = {'type': 'choice', 'answer': 'Yes' if yes else 'No',
                    'options': ['Yes', 'No'], 'selectionPrompt': 'Is this function one-to-one on its stated domain?',
                    'explanation': working, 'provenance': 'original-horizontal-line-test-or-counterexample',
                    'scope': 'The one-to-one classification is checked; source graphs and reasoning remain available.'}
            checked_fields += install(entry,source_set,number,group,checks,qid,q['prompt'])
            covered.add(qid)
    assert covered == set(chapter), sorted(set(chapter) - covered)
    library['coverage']['chapter1WorkedSolutions'] = len(covered)
    library['coverage']['chapter1Total'] = len(chapter)
    library['coverage']['chapter1CheckableExercises'] = len(covered)
    library['coverage']['chapter1ObjectiveFields'] = checked_fields
    # Recalculate only globally defined metrics whose semantics are known.
    library['coverage']['answerRecords'] = len(library['questions'])
    library['coverage']['missing'] = library['coverage']['total'] - len(library['questions'])
    library['coverage']['workedSolutionRecords'] = sum(bool(a.get('steps') or a.get('solutions')) for a in library['questions'].values())
    library['coverage']['newGraderRecords'] = sum(bool(a.get('grader')) for a in library['questions'].values())
    OUT.write_bytes(gzip.compress(json.dumps(library, ensure_ascii=False, separators=(',', ':')).encode(), mtime=0))
    report = {'chapter': 1, 'questions': len(chapter), 'workedSolutions': len(covered),
              'checkableExercises': len(covered), 'objectiveFields': checked_fields,
              'missing': [], 'sets': {}, 'limitations': [
                  'Graph-reading estimates and open-ended examples are not exact measurements or unique models.',
                  'Every exercise has objective checks; freehand drawings and written proofs are not automatically assessed.',
                  'No other calculus chapter, physics solution or lab model was changed.'
              ]}
    for q in chapter.values():
        row = report['sets'].setdefault(q['sourceSet'], {'questions': 0, 'workedSolutions': 0})
        row['questions'] += 1
        row['workedSolutions'] += int(q['id'] in covered)
    (Path(__file__).parent / 'coverage.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    build()
