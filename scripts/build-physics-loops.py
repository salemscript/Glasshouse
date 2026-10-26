import gzip,json,collections,pathlib,re
qs=json.load(gzip.open('site/questions/physics.json.gz'))
# Concept illustrations, deliberately not numerical simulations or solution diagrams.
chapter_types=['measure','motion','vector','projectile','force','force','energy','spring','collision','wheel','wheel','balance','orbit','fluid','spring','wave','sound','thermal','gas','thermal','charge','field','field','charge','capacitor','current','circuit','magnet','magnet','induction','wave','field','wave','lens','interference','diffraction','light','photon','wave','levels','current','nucleus','nucleus','particle']
manifest={};coverage=[]
for c in range(1,45):
 items=[q for q in qs if q.get('chapter')==c and q.get('kind')=='Problems']
 for q in items[::2]:
  kind=chapter_types[c-1];p=q.get('prompt','').lower()
  # Only switch within a chapter's physics domain; no inferred numerical givens.
  if c in range(2,14):
   if re.search(r'spring|oscillat',p):kind='spring'
   elif re.search(r'collid|collision',p):kind='collision'
   elif re.search(r'rotat|wheel|angular',p):kind='wheel'
   elif c==4 and re.search(r'projectile|launch|thrown|ball',p):kind='projectile'
  manifest[q['id']]=kind
 coverage.append({'chapter':c,'problems':len(items),'illustrated':len(items[::2]),'percent':round(len(items[::2])/len(items)*100,1)})
pathlib.Path('site/physics-loop-map.js').write_text('window.PhysicsLoopMap='+json.dumps(manifest,separators=(',',':'))+';\n')
pathlib.Path('scripts/answer-data/physics-loop-coverage.json').write_text(json.dumps({'scope':'Decorative concept illustrations; not exact problem simulations. Alternating problems in each chapter, with a final item for odd chapter totals.','chapters':coverage,'totalIllustrated':len(manifest)},indent=2)+'\n')
print(len(manifest),'illustrated problems across',len(coverage),'chapters')
