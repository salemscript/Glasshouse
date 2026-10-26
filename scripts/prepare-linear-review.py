"""Import all nine supplied Anton & Kaul chapter supplementary sets.
Source excerpts preserve typeset mathematics. No inferred answer keys are added.
Coordinates are PDF points; paired matrix exercises require explicit row bounds.
"""
import fitz, gzip, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site'
COUNTS=[29,37,25,18,20,21,15,26,14]
STARTS=[1,118,146,202,291,341,399,446,509]
TITLES=['Systems of Linear Equations and Matrices','Determinants','Euclidean Vector Spaces','General Vector Spaces','Eigenvalues and Eigenvectors','Inner Product Spaces','Diagonalization and Quadratic Forms','General Linear Transformations','Numerical Methods']
# Start overrides include matrix rows above a vertically centred exercise number.
Y={(1,1):686,(1,2):686,(1,3):638,(1,4):638,
 (2,1):435,(2,2):435,(2,3):467,(2,4):467,(2,5):511,(2,6):511,(2,7):559,(2,8):559,(2,13):441,(2,14):441,(2,15):494,
 (9,1):640,(9,3):699,(9,5):675,(9,8):282,(9,9):313,(2,37):633,(3,13):533.5}
# Shared directions are separate source excerpts, repeated for every applicable exercise.
CONTEXT=[(1,range(1,5),115,62,638,255,46),(1,[25,26,27],117,62,134,255,116),
 (2,range(1,9),27,37,399,255,34),(2,range(13,16),27,303,429,255,12),(2,range(17,25),27,303,633,255,25),
 (3,range(13,19),55,303,510,255,23.5),(3,range(19,22),55,303,687,255,23),
 (5,range(8,11),50,37,237,255,24),
 (4,[6],42,70,144,358,73),(5,[8],10,36,238,252,40),(5,[12],10,300,230,252,38),(5,[16],9,325,580,252,77),
 (6,[15],17,70,404,358,75),(7,[15],25,70,634,358,104)]
# End before directions belonging to the following set.
ENDS={(1,24):134,(2,12):429,(2,16):633,(3,12):508,(3,18):687,(5,7):237}
REFS={1:{23:[22],27:[26]},2:{9:[3,4,5,6],11:[1,2,3,4],12:[5,6,7,8],**{n:[n-16] for n in range(17,25)}},3:{2:[1],3:[1],9:[7],10:[8]},4:{15:[14]},5:{8:[7],9:[7],10:[7,9],16:[5]},8:{24:[23]},9:{2:[1],4:[3],10:[9]}}
questions=[];audit=[]
for ch in range(1,10):
 doc=fitz.open(SITE/f'books/linear-algebra/chapter-{ch:02}.pdf'); columns=[]; anchors=[]; started=False
 for pi,p in enumerate(doc):
  lines=[l for b in p.get_text('dict')['blocks'] for l in b.get('lines',[])]
  headings=[l for l in lines if re.match(r'Chapter \d Supplementary Exercises',''.join(s['text'] for s in l['spans']))]
  if headings:started=True; top=headings[0]['bbox'][3]+4
  else:top=49
  if not started:continue
  left=62 if STARTS[ch-1]+pi & 1 else 37
  for col in range(2):
   x=left+266*col; ci=len(columns); columns.append((pi,x,top,752))
   for l in lines:
    t=''.join(s['text'] for s in l['spans']);lx,ly,_,_=l['bbox'];m=re.match(r'^(\d+)\.(?:$|\s)',t)
    if m and ly>top and x-2<=lx<x+255:
     n=int(m[1]);anchors.append(dict(n=n,ci=ci,x=lx,y=Y.get((ch,n),ly-2)))
 # Each source number must appear once and in a complete sequence.
 anchors.sort(key=lambda a:a['n']);assert [a['n'] for a in anchors]==list(range(1,COUNTS[ch-1]+1)),(ch,anchors)
 def part(ci,y,end,x=None,width=255,role='problem'):
  pi,left,top,bottom=columns[ci];x=left if x is None else x
  assert end>y,(ch,ci,y,end)
  return {'file':f'practice/linear-algebra/{STARTS[ch-1]+pi}.svg.gz','pdfPage':STARTS[ch-1]+pi+14,'crops':[[round(x,2),round(y,2),width,round(end-y,2)]],'role':role}
 for ai,a in enumerate(anchors):
  n=a['n'];ci=a['ci'];pi,left,top,bottom=columns[ci];parts=[]
  # Paired short problems share a row but have independent horizontal crops.
  pair=(ch==1 and n<=4) or (ch==2 and (n<=8 or n in [13,14] or 17<=n<=24))
  if pair:
   right=(n%2==0);x=left+(126 if right else 0);width=126
   row_end=next((b['y'] for b in anchors[ai+1:] if b['ci']==ci and b['y']>a['y']+3),bottom)
   if ch==1 and n<=2:row_end=752
   if ch==1 and n in [3,4]:row_end=685
   parts=[part(ci,a['y'],row_end,x,width)]
  else:
   nexta=anchors[ai+1] if ai+1<len(anchors) else None
   lastci=nexta['ci'] if nexta else ci
   for k in range(ci,lastci+1):
    kp,kx,kt,kb=columns[k];s=a['y'] if k==ci else kt
    e=nexta['y'] if nexta and k==lastci else kb
    if k==ci and (ch,n) in ENDS:e=ENDS[ch,n];lastci=ci
    if e>s+1:parts.append(part(k,s,e))
    if (ch,n) in ENDS:break
  for c,ns,page,x,y,w,h in CONTEXT:
   if c==ch and n in ns:parts.insert(0,{'file':f'practice/linear-algebra/{STARTS[ch-1]+page-1}.svg.gz','pdfPage':STARTS[ch-1]+page+13,'crops':[[x,y,w,h]],'role':'instructions'})
  texts=[]
  for p in parts:
   pg=doc[p['pdfPage']-14-STARTS[ch-1]]
   for crop in p['crops']:
    x,y,w,h=crop
    words=[v for v in pg.get_text('words') if v[0]<x+w and v[2]>x and v[1]>=y-.1 and v[3]<=y+h+.1]
    if words:crop[3]=round(min(h,max(v[3] for v in words)-y+3),2)
  for p in parts:
   pg=doc[p['pdfPage']-14-STARTS[ch-1]]
   for x,y,w,h in p['crops']:texts.append(pg.get_text(clip=fitz.Rect(x,y,x+w,y+h)))
  q={'id':f'anton-chapter-{ch:02}-supplementary-{n}','book':'linear-algebra','chapter':ch,'chapterTitle':f'{ch}. {TITLES[ch-1]}','section':'Chapter review','sourceSet':f'anton-chapter-{ch:02}-supplementary','number':str(n),'title':f'Supplementary Exercise {n}','kind':'Supplementary Exercises','prompt':'\n'.join(texts),'promptFormat':'source-text-search-only','parts':parts,'reviewPractice':True,'sourcePdfPage':STARTS[ch-1]+pi+14,'sourceLocalPage':pi+1,'sourceFile':f'books/linear-algebra/chapter-{ch:02}.pdf','grader':None,'hints':[],'steps':[]}
  if n in REFS.get(ch,{}):q['relatedQuestions']=[f'anton-chapter-{ch:02}-supplementary-{v}' for v in REFS[ch][n]]
  questions.append(q)
 for pi in sorted({v[0] for v in columns}|{c[2]-1 for c in CONTEXT if c[0]==ch}):
  path=SITE/f'practice/linear-algebra/{STARTS[ch-1]+pi}.svg.gz';path.parent.mkdir(parents=True,exist_ok=True)
  svg=doc[pi].get_svg_image(text_as_path=True)
  # Intrinsic full-page dimensions would letterbox a cropped viewBox.
  svg=re.sub(r'<svg\b[^>]*>',lambda m:re.sub(r'\s(?:width|height)="[^"]*"','',m[0]),svg,count=1)
  prefix=f'la-{ch}-{pi}-'
  svg=svg.replace('id="','id="'+prefix).replace('xlink:href="#','xlink:href="#'+prefix).replace('url(#','url(#'+prefix)
  path.write_bytes(gzip.compress(svg.encode(),mtime=0))
 audit.append({'chapter':ch,'exerciseCount':COUNTS[ch-1],'numbers':f'1–{COUNTS[ch-1]}','source':'Anton & Kaul, Elementary Linear Algebra, 12th edition; user-supplied PDF','collection':'Chapter Supplementary Exercises','questionCoverage':'complete','automaticChecks':'not yet verified','sourcePages':[STARTS[ch-1]+p for p in sorted({v[0] for v in columns})]})
assert len(questions)==205
(SITE/'linear-review-data.js').write_text('/* Generated by scripts/prepare-linear-review.py. */\nwindow.LinearReviewQuestions='+json.dumps(questions,ensure_ascii=False,separators=(',',':'))+';\n')
(ROOT/'scripts/answer-data/linear-review-coverage.json').write_text(json.dumps({'total':205,'chapters':audit},indent=2)+'\n')
print('Imported',len(questions),'chapter review questions.')
