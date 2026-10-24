"""Restore omitted mathematical exercise data with original paraphrases and diagram.
No external textbook page or publisher artwork is redistributed.
"""
from pathlib import Path
import gzip,json,copy,hashlib
ROOT=Path(__file__).resolve().parents[3];path=ROOT/'site/questions/calculus.json.gz'
qs=json.loads(gzip.decompress(path.read_bytes()));base=next(q for q in qs if q['id']=='calculus-section-6-2-23')
regions=[('y=x+1, y=0, x=0, x=2','x-axis'),('y=1/x, y=0, x=1, x=4','x-axis'),('y=√(x−1), y=0, x=5','x-axis'),('y=eˣ, y=0, x=−1, x=1','x-axis'),('x=2√y, x=0, y=9','y-axis'),('2x=y², x=0, y=4','y-axis'),('y=x³, y=x, x≥0','x-axis'),('y=6−x², y=2','x-axis'),('y²=x, x=2y','y-axis'),('x=2−y², x=y⁴','y-axis'),('y=x², x=y²','y=1'),('y=x³, y=1, x=2','y=−3'),('y=1+sec(x), y=3','y=1'),('y=sin(x), y=cos(x), 0≤x≤π/4','y=−1'),('y=x³, y=0, x=1','x=2'),('xy=1, y=0, x=1, x=2','x=−1'),('x=y², x=1−y²','x=3'),('y=x, y=0, x=2, x=4','x=1')]
new=[]
for n in range(1,23):
 q=copy.deepcopy(base);q['id']=f'calculus-section-6-2-{n}';q['number']=str(n);q['title']=f'6.2 · Exercises {n}';q['parts']=[];q.pop('answerKeySource',None);q['flags']=[]
 if n<=18:
  curves,axis=regions[n-1];prompt=f'Find the volume formed when the bounded region described by {curves} revolves around {axis}. Include sketches of the region, resulting solid, and a representative disk or washer.'
  if n==13:prompt+=' Use the central bounded region containing x=0 (−π/3≤x≤π/3).'
 else:prompt='In the unit square OABC, O=(0,0), A=(1,0), B=(1,1), C=(0,1). Region R₁ is the triangle 0≤y≤x≤1. Calculate its volume of revolution around '+{19:'OA (y=0)',20:'OC (x=0)',21:'AB (x=1)',22:'BC (y=1)'}[n]+'.'
 q.update(prompt=prompt,nativePrompt=prompt,promptFormat='native-text',nativePromptSource=dict(book='Stewart Calculus: Early Transcendentals, 8e',printedPage=446,sourceURL='https://s3.amazonaws.com/scschoolfiles/3191/calculus_early_transcendentals_james_stewart_8th_edition.pdf',note='Mathematical givens recovered from omitted page; wording is an original paraphrase.'))
 if n>=19:q['nativeFigures']=[dict(url='books/calculus/section-6-2-regions.svg',alt='Reconstructed coordinate diagram: unit square OABC split by y=x and y=x^(1/4) into R₁ below y=x, R₂ above the fourth-root curve, and R₃ between the curves.')]
 new.append(q)
ids={q['id'] for q in new};qs=[q for q in qs if q['id'] not in ids];at=next(i for i,q in enumerate(qs) if q['id']=='calculus-section-6-2-23');qs[at:at]=new
path.write_bytes(gzip.compress(json.dumps(qs,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
# Original vector reconstruction from the mathematical coordinates, not a copied image.
pts=' '.join(f'{90+300*i/200:.3f},{380-300*(i/200)**.25:.3f}' for i in range(201));poly='M90,380 '+ ' '.join(f'L{90+300*i/200:.3f},{380-300*(i/200)**.25:.3f}' for i in range(1,201))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 460" role="img" aria-labelledby="title desc"><title id="title">Regions in the unit square</title><desc id="desc">O at origin, A at one zero, B at one one, C at zero one. R1 below the diagonal, R2 above fourth root, R3 between.</desc><rect width="500" height="460" fill="#fff9f1"/><path d="M90 380 L390 380 L390 80 Z" fill="#c7e5f4"/><path d="{poly} L90 80 Z" fill="#d9e9c8"/><path d="{poly} Z" fill="#ffe1ba"/><path d="M90 380 H390 V80 H90 Z M90 380 L390 80" fill="none" stroke="#455c6a" stroke-width="2"/><polyline points="{pts}" fill="none" stroke="#dd6b54" stroke-width="3"/><path d="M60 380 H445 M90 410 V40" fill="none" stroke="#36434b" stroke-width="2"/><g font-family="Georgia,serif" font-size="22" fill="#263942"><text x="66" y="406">O</text><text x="365" y="411">A(1,0)</text><text x="394" y="77">B(1,1)</text><text x="13" y="77">C(0,1)</text><text x="451" y="387">x</text><text x="75" y="29">y</text><text x="310" y="325">R₁</text><text x="130" y="125">R₂</text><text x="155" y="253">R₃</text><text x="190" y="181">y = x¹⁄⁴</text><text x="294" y="217">y = x</text></g></svg>'''
(ROOT/'site/books/calculus/section-6-2-regions.svg').write_text(svg)
print('Restored',len(new),'questions; total Chapter6',sum(q['chapter']==6 for q in qs))
