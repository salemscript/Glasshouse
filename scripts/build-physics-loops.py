import gzip,json,pathlib
qs=json.load(gzip.open('site/questions/physics.json.gz'))
reviewed={'halliday10-001','halliday10-007','halliday10-008','halliday10-011','halliday10-016','halliday10-018','halliday10-019','halliday10-022'}
manifest={q['id']:q['bankId'] for q in qs if q.get('bankId') in reviewed}
pathlib.Path('site/physics-loop-map.js').write_text('window.PhysicsLoopMap='+json.dumps(manifest,separators=(',',':'))+';\n')
coverage=[{'chapter':c,'problems':len([q for q in qs if q['chapter']==c and q['kind']=='Problems']),'illustrated':sum(q['id'] in manifest for q in qs if q['chapter']==c)} for c in range(1,45)]
pathlib.Path('scripts/answer-data/physics-loop-coverage.json').write_text(json.dumps({'scope':'Only exact reviewed question mappings. No chapter-level fallback. Half-per-chapter target is not met.','chapters':coverage,'totalIllustrated':len(manifest)},indent=2)+'\n')
