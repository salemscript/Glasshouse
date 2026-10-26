"""Build reviewed section selections from the user's Anton & Kaul textbook.
The original typeset source is preserved; imported problems are not certified answers.
"""
import fitz,gzip,json,re,runpy
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
catalog=runpy.run_path(str(ROOT/'scripts/linear-section-source.py'))['result']
selection=json.loads((ROOT/'scripts/answer-data/linear-section-selection.json').read_text())
meta=json.loads((SITE/'math-course-data.js').read_text().split('=',1)[1].strip().rstrip(';'))['linearAlgebra']
docs={c['number']:fitz.open(SITE/c['file']) for c in meta};used=set();out=[];audits=[]
# Original teaching goals for each selected set, reviewed against its exercise statements.
GOALS={
'1.1':'Recognize linear equations, translate between equations and matrices, check solutions, describe free variables, and model a diet problem.',
'1.2':'Compare Gaussian and Gauss–Jordan elimination, interpret pivots and free variables, test consistency, and fit a curve.',
'1.3':'Check matrix sizes, calculate sums and products, connect multiplication to linear combinations, and model costs.',
'1.4':'Use transpose and inverse rules, solve systems with an inverse, and understand why scalar algebra rules can fail for matrices.',
'1.5':'Connect row operations to elementary matrices, compute inverses, recognize singular cases, and explain row equivalence.',
'1.6':'Use inverse matrices for multiple right-hand sides and connect invertibility to consistency and homogeneous systems.',
'1.7':'Recognize special matrix structures, use efficient calculations, and distinguish symmetry from triangularity and invertibility.',
'1.8':'Connect formulas to matrix transformations, identify domain and codomain, and interpret reflections, rotations, and linearity.',
'1.9':'Understand composition order, compute combined transformations, and connect geometric reversibility to inverses.',
'1.10':'Build linear models for flows, traffic, circuits, chemical reactions, and polynomial interpolation.',
'1.11':'Translate economic exchanges into matrices, distinguish open and closed economies, and interpret feasible production.',
'2.1':'Connect minors and cofactors to determinants, exploit structure, and interpret zero determinants geometrically.',
'2.2':'Track how row operations change determinants and combine reduction with structural reasoning.',
'2.3':'Use determinants to test invertibility, solve systems with Cramer’s rule, and reason about products and scaling.',
'3.1':'Move between geometric and coordinate descriptions, form linear combinations, and reason about parallel vectors.',
'3.2':'Calculate lengths, dot products, and angles; distinguish vectors from scalars; and connect inequalities to geometry.',
'3.3':'Use orthogonality to describe planes, calculate projections and distances, and interpret work done by a force.',
'3.4':'Translate between parametric, vector, and equation descriptions of lines, planes, and solution spaces.',
'3.5':'Use cross products for perpendicular directions, areas, volumes, orientation, and torque.',
'4.1':'Test vector-space axioms across familiar and unfamiliar operations, and explain why examples fail.',
'4.2':'Apply the subspace test to vectors, matrices, polynomials, and functions; connect kernels to geometry.',
'4.3':'Build and test spanning sets in several vector spaces and explain when different sets span the same space.',
'4.4':'Recognize dependence, test independence, investigate parameters, and connect algebraic and functional examples.',
'4.5':'Choose bases, calculate coordinates in different spaces, and distinguish spanning from independence.',
'4.6':'Find bases and dimensions, extend independent sets, remove redundant vectors, and connect dimension to solution spaces.',
'4.7':'Compute and interpret change-of-basis matrices, track direction and order, and relate coordinate changes to geometry.',
'4.8':'Connect consistency to column space, compute bases for fundamental spaces, and interpret homogeneous and nonhomogeneous solutions.',
'4.9':'Calculate rank and nullity, identify the fundamental matrix spaces, and reason about their dimensions and orthogonality.',
'5.1':'Check eigenpairs, find eigenspaces, use geometric transformations, and connect eigenvalues to characteristic polynomials.',
'5.2':'Decide whether diagonalization is possible, build an eigenbasis, and distinguish algebraic from geometric multiplicity.',
'5.3':'Work with complex vectors and conjugation, calculate complex eigenpairs, and connect real matrices with complex eigenvalues.',
'5.4':'Solve systems of differential equations using eigenvalues, impose initial conditions, and connect higher-order equations to systems.',
'5.5':'Interpret stochastic matrices, calculate state evolution and steady states, and model transitions in real situations.',
'6.1':'Compare inner products on vectors, matrices, and functions; calculate lengths; and test which axioms matter.',
'6.2':'Compute angles and orthogonal complements in different inner-product spaces, then explain the underlying structure.',
'6.3':'Build orthonormal bases, calculate projections, apply Gram–Schmidt in different spaces, and compute a QR decomposition.',
'6.4':'Solve least-squares problems, compare exact and approximate solutions, and connect projections to normal equations and QR.',
'6.5':'Fit lines and transformed curves, construct design matrices, and explain when a least-squares fit is unique.',
'6.6':'Approximate functions with polynomials and trigonometric sums, calculate errors, and build Fourier series.',
'7.1':'Recognize orthogonal matrices, use transpose inverses, describe rotations, and explain their geometric properties.',
'7.2':'Build orthonormal eigenbases, compute orthogonal diagonalizations, and interpret spectral decompositions.',
'7.3':'Write quadratic forms as matrices, eliminate cross terms, classify conics, and distinguish types of definiteness.',
'7.4':'Use eigenvalues to optimize quadratic forms under constraints and connect definiteness to critical-point classification.',
'7.5':'Connect conjugate transpose, Hermitian and unitary matrices, complex eigenvalues, and unitary diagonalization.',
'8.1':'Test linearity beyond coordinate vectors, compute kernels and ranges, and use rank–nullity for general transformations.',
'8.2':'Analyze one-to-one transformations, construct inverses, and track the order of compositions across vector spaces.',
'8.3':'Construct and test isomorphisms between different vector spaces and explain which structures they preserve.',
'8.4':'Represent general transformations with matrices, track basis choices, and connect composition and differentiation to matrix products.',
'8.5':'Connect changes of basis to similarity, compare representations of the same operator, and test similarity invariants.',
'8.6':'Visualize images of shapes, decompose transformations, and distinguish the effects of shear, scaling, rotation, and reflection.',
'9.1':'Factor matrices into LU and PLU forms, solve systems efficiently, and understand when pivoting is needed.',
'9.2':'Identify dominant eigenvalues, compare power-method scalings, and investigate convergence and starting-vector effects.',
'9.3':'Count arithmetic operations and compare the computational cost of matrix operations and system-solving methods.',
'9.4':'Calculate singular values and decompositions for different matrix shapes and connect SVD to rank and polar decomposition.',
'9.5':'Build reduced singular-value decompositions and expansions, then compare storage costs of low-rank approximations.'}

@lru_cache(maxsize=None)
def words(ch,pg,x,w):return [a for a in docs[ch][pg].get_text('words') if a[0]<x+w-1 and a[2]>x+1]
def snap(ch,pg,x,w,lo,hi):
 """Choose a whitespace boundary preceding an exercise, above centred matrices."""
 intervals=sorted((max(lo,a[1]),min(hi,a[3])) for a in words(ch,pg,x,w) if a[3]>lo and a[1]<hi)
 # Matrix brackets and diagram lines prevent splitting a vertical object.
 for d in docs[ch][pg].get_drawings():
  r=d['rect']
  if r.width<260 and r.height<250 and r.x0<x+w and r.x1>x and r.y1>lo and r.y0<hi:intervals.append((max(lo,r.y0),min(hi,r.y1)))
 intervals.sort();gaps=[];end=lo
 for a,b in intervals:
  if a>end:gaps.append((a-end,end,a))
  end=max(end,b)
 if hi>end:gaps.append((hi-end,end,hi))
 if not gaps:return hi
 size,a,b=next((g for g in reversed(gaps) if g[0]>1),gaps[-1]);return (a+b)/2 if size>1 else hi

def part(ch,pg,x,y,w,end,role='problem'):
 p=docs[ch][pg];ws=[a for a in words(ch,pg,x,w) if a[3]>y and a[1]<end]
 if not ws:return None
 # Expand across any glyph touching a boundary. A later verifier catches collisions.
 y=min(y,min(a[1] for a in ws));end=max(end,max(a[3] for a in ws))
 end=min(end,max(a[3] for a in ws)+2)
 used.add((ch,pg));printed=meta[ch-1]['start']+pg
 return {'file':f'practice/linear-sections/{printed}.svg.gz','pdfPage':printed+14,'role':role,'crops':[[round(x,2),round(y,2),round(w,2),round(end-y,2)]]}

def build(sec,r):
 ch=r['chapter'];qs=r['questions'];cols=r['cols'];rows=[];by={q['n']:q for q in qs}
 i=0
 while i<len(qs):
  a=qs[i];ci=a['ci'];pg,x,top,end=cols[ci];members=[a]
  while i+len(members)<len(qs):
   b=qs[i+len(members)]
   if b['ci']==ci and b['x']>members[-1]['x']+20 and abs(b['y']-a['y'])<50:members.append(b)
   else:break
  pair=len(members)>1;prev=rows[-1] if rows and rows[-1]['ci']==ci else None
  anchor=min(q['y'] for q in members);lo=max(top,(max(q['y'] for q in prev['members'])+10 if prev else top))
  sy=snap(ch,pg,x,255,lo,anchor-1) if anchor>lo+1 else lo
  rows.append({'ci':ci,'members':members,'start':sy,'pair':pair});i+=len(members)
 # Detect shared instructions, including matrix data extending across columns/pages.
 contexts=[]
 for ci,(pg,x,top,end) in enumerate(cols):
  for block in docs[ch][pg].get_text('dict')['blocks']:
   lines=block.get('lines',[])
   if not lines:continue
   bx,byy,_,_=block['bbox'];text=' '.join(''.join(s['text'] for s in l['spans']) for l in lines)
   m=re.search(r'(?:In\s*(?:each part of\s*)?Exercises?|For Exercises?)\s*(\d+)[–−-](\d+)',text)
   if not m or not(x-3<=bx<x+255 and top<=byy<end):continue
   low,high=map(int,m.groups());first=next((v for v in rows if any(q['n']==low for q in v['members'])),None)
   if not first:continue
   # Start at the actual instruction line, not an earlier problem in the same PDF block.
   lead=next((l for l in lines if re.search(r'In\s*(?:each part|Exercises?)|For Exercises?', ''.join(s['text'] for s in l['spans']))),lines[0]);sy=lead['bbox'][1]-1
   if first['ci']<ci:continue
   # Find the gap after the instruction/data and before the numbered row.
   targetpg,tx,tt,te=cols[first['ci']];numy=min(q['y'] for q in first['members'])
   if first['ci']==ci and first['start']<=sy:first['start']=snap(ch,pg,x,255,sy+8,numy-1)
   cp=[]
   for k in range(ci,first['ci']+1):
    pp,xx,yy,ee=cols[k];yy=sy if k==ci else yy;ee=first['start'] if k==first['ci'] else ee
    if ee>yy:
     p=part(ch,pp,xx,yy,255,ee,'instructions')
     if p:cp.append(p)
   if cp:contexts.append({'lo':low,'hi':high,'parts':cp,'ci':ci,'y':sy})
 allq={}
 for ri,row in enumerate(rows):
  ci=row['ci'];pg,x,top,end=cols[ci];nxt=rows[ri+1] if ri+1<len(rows) else None
  for a in row['members']:
   parts=[];lastci=nxt['ci'] if nxt else len(cols)-1
   for k in range(ci,lastci+1):
    pp,xx,yy,ee=cols[k];yy=row['start'] if k==ci else yy;ee=nxt['start'] if nxt and k==lastci else ee
    # End before unrelated shared instructions or proof headings.
    upcoming=[g['y'] for g in contexts if g['ci']==k and yy<g['y']<ee and not(g['lo']<=a['n']<=g['hi'])]
    if upcoming:ee=min(upcoming)
    xx-=3;width=258
    if row['pair'] and k==ci:
     ix=row['members'].index(a);xx=(x-3 if ix==0 else a['x']-2);right=(row['members'][ix+1]['x']-2 if ix+1<len(row['members']) else x+255);width=right-xx
    if ee>yy+1:
     p=part(ch,pp,xx,yy,width,ee)
     if p:parts.append(p)
    if row['pair']:break
   shared=[p for g in contexts if g['lo']<=a['n']<=g['hi'] for p in g['parts']]
   text=' '.join(docs[ch][p['pdfPage']-14-meta[ch-1]['start']].get_text(clip=fitz.Rect(c[0],c[1],c[0]+c[2],c[1]+c[3])) for p in parts for c in p['crops'])
   allq[a['n']]={'parts':shared+parts,'text':text,'ci':ci}
 return allq

all_sources={s:build(s,r) for s,r in catalog.items()}
for sec,chosen in selection.items():
 r=catalog[sec];ch=r['chapter'];source=all_sources[sec]
 assert len(chosen)==min(10,len(source)) and len(chosen)==len(set(chosen)),sec
 for n in chosen:
  original=source[n];parts=original['parts'].copy();refs=[]
  # Bring explicitly referenced exercises along even when not chosen as standalone practice.
  for m in re.finditer(r'\bExercises?\s+(\d+)(?:[–−-](\d+))?',original['text']):
   low=int(m[1]);high=int(m[2] or low)
   if 0<low<=high<=max(source):refs.extend(range(low,high+1))
  for ref in sorted(set(refs)-{n}):
   for p in source[ref]['parts']:parts.append({**p,'role':'reference','contextLabel':str(ref)})
  ci=original['ci'];pg=catalog[sec]['cols'][ci][0];q={'id':f'anton-section-{sec.replace(".","-")}-{n}','book':'linear-algebra','chapter':ch,'chapterTitle':f'{ch}. '+meta[ch-1]['title'],'section':sec,'sectionTitle':r['title'],'sourceSet':f'anton-section-{sec.replace(".","-")}','number':str(n),'title':f'Exercise {n}','kind':'Selected Section Exercises','prompt':original['text'],'promptFormat':'source-text-search-only','parts':parts,'reviewPractice':True,'sourcePdfPage':meta[ch-1]['start']+pg+14,'grader':None,'hints':[],'steps':[],'selectionGoal':GOALS[sec]}
  out.append(q)
 audits.append({'section':sec,'title':r['title'],'selectedNumbers':chosen,'count':len(chosen),'learningGoals':GOALS[sec],'selectionReviewed':True,'checks':'not added by this import'})
for ch,pg in sorted(used):
 p=SITE/f'practice/linear-sections/{meta[ch-1]["start"]+pg}.svg.gz';p.parent.mkdir(parents=True,exist_ok=True)
 svg=docs[ch][pg].get_svg_image(text_as_path=True)
 svg=re.sub(r'<svg\b[^>]*>',lambda m:re.sub(r'\s(?:width|height)="[^"]*"','',m[0]),svg,count=1)
 prefix=f'las-{ch}-{pg}-';svg=svg.replace('id="','id="'+prefix).replace('xlink:href="#','xlink:href="#'+prefix).replace('url(#','url(#'+prefix)
 p.write_bytes(gzip.compress(svg.encode(),mtime=0))
(SITE/'linear-section-data.js').write_text('/* Generated from reviewed selections in scripts/answer-data/linear-section-selection.json. */\nwindow.LinearSectionQuestions='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n')
(ROOT/'scripts/answer-data/linear-section-coverage.json').write_text(json.dumps({'sections':55,'selectedExercises':len(out),'sets':audits},ensure_ascii=False,indent=2)+'\n')
(ROOT/'tmp/linear-section-crops.json').write_text(json.dumps(out,ensure_ascii=False))
print('Built',len(out),'selected exercises across',len(audits),'sections.')
