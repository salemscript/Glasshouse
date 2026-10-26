"""Validate coverage, source assets, labels, and glyph boundaries for section selections."""
import fitz,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1];qs=json.loads((root/'site/linear-section-data.js').read_text().split('=',1)[1].strip().rstrip(';'));starts=[1,118,146,202,291,341,399,446,509];docs={i:fitz.open(root/f'site/books/linear-algebra/chapter-{i:02}.pdf') for i in range(1,10)};cache={};issues=[]
for q in qs:
 for p in q['parts']:
  ch=q['chapter'];pg=p['pdfPage']-14-starts[ch-1];key=(ch,pg)
  if key not in cache:
   page=docs[ch][pg];labels=[]
   for b in page.get_text('dict')['blocks']:
    for l in [dict(spans=[s],bbox=s['bbox']) for line in b.get('lines',[]) for s in line['spans']]:
     t=''.join(s['text'] for s in l['spans']);m=re.match(r'^(\d+)\.(?:$|\s)',t.strip())
     if m and 'Bold' in l['spans'][0]['font']:labels.append((int(m[1]),l['spans'][0]['bbox']))
   cache[key]=(page.get_text('words'),labels)
  ws,labs=cache[key]
  for x,y,w,h in p['crops']:
   cut=[v[4] for v in ws if v[0]<x+w-1 and v[2]>x+1 and((v[1]<y-.1 and v[3]>y+.5)or(v[1]<y+h-.5 and v[3]>y+h+.1))]
   others=[n for n,b in labs if x<=b[0]<x+w and y<=b[1]<y+h and str(n)!=q['number']]
   if cut or (others and p['role']=='problem'):issues.append((q['section'],q['number'],p['role'],p['pdfPage'],p['crops'],cut[:10],others))
selection=json.loads((root/'scripts/answer-data/linear-section-selection.json').read_text())
assert len(selection)==55 and len(qs)==548 and len({q['id'] for q in qs})==548
for sec,nums in selection.items():
 assert sorted(int(q['number']) for q in qs if q['section']==sec)==sorted(nums),sec
 assert len(nums)==(9 if sec in ['6.5','9.5'] else 10),sec
for q in qs:
 assert q['grader'] is None and q['selectionGoal'] and q['parts'],q['id']
 assert any(re.search(r'\b'+q['number']+r'\.',q['prompt']) for _ in [0]),q['id']
 for p in q['parts']:
  assert (root/'site'/p['file']).is_file(),p['file']
  for x,y,w,h in p['crops']:assert x>=0 and y>=0 and w>0 and h>0 and x+w<=612 and y+h<=792,(q['id'],p)
by_id={q['id']:q for q in qs}
# Regression checks: later subparts and a matrix below the introductory sentence.
for id in ['anton-section-1-8-50','anton-section-4-9-1','anton-section-6-6-1','anton-section-9-4-19']:
 assert 'b.' in by_id[id]['prompt'],id
assert '𝐴' in by_id['anton-section-8-6-1']['prompt']
assert not issues,issues
print('Verified 548 selections across 55 sections; all assets and crop boundaries pass.')
