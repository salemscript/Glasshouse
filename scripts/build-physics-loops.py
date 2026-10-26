import gzip,json,pathlib
qs=json.load(gzip.open('site/questions/physics.json.gz'))
reviewed={'halliday10-001','halliday10-007','halliday10-008','halliday10-011','halliday10-016','halliday10-018','halliday10-019','halliday10-022'}
manifest={q['id']:q['bankId'] for q in qs if q.get('bankId') in reviewed}
pathlib.Path('site/physics-loop-map.js').write_text('window.PhysicsLoopMap='+json.dumps(manifest,separators=(',',':'))+';\n')
extra=[(2,1),(2,3),(2,4),(3,5),(4,4),(6,1),(6,2),(6,3),(7,3),(8,3),(10,1),(10,5),(13,2),(15,1),(15,3),(15,4),(15,5),(16,2),(26,3),(27,3)]
for c,n in extra:
 key=f'physics-chapter-{c:02d}-problems-{n}';manifest[key]=key
pathlib.Path('site/physics-loop-map.js').write_text('window.PhysicsLoopMap='+json.dumps(manifest,separators=(',',':'))+';\n')
coverage=[{'chapter':c,'problems':len([q for q in qs if q['chapter']==c and q['kind']=='Problems']),'target':len([q for q in qs if q['chapter']==c and q['kind']=='Problems'])//2+1,'illustrated':sum(q['id'] in manifest for q in qs if q['chapter']==c)} for c in range(1,45)]
pathlib.Path('scripts/answer-data/physics-loop-coverage.json').write_text(json.dumps({'scope':'Only exact reviewed question mappings. No chapter-level fallback. More-than-half-per-chapter target is not met.','chapters':coverage,'totalIllustrated':len(manifest)},indent=2)+'\n')
