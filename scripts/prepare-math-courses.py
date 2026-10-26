import fitz,json,re,pathlib,gzip,argparse
from pypdf import PdfReader,PdfWriter
parser=argparse.ArgumentParser(description='Prepare Anton & Kaul 12e chapter readings and math course metadata.')
parser.add_argument('textbook',type=pathlib.Path)
args=parser.parse_args()
root=pathlib.Path(__file__).resolve().parents[1]
pdf=fitz.open(args.textbook)
source=PdfReader(args.textbook)
(root/'site/books/linear-algebra').mkdir(parents=True,exist_ok=True)
names=['Systems of Linear Equations and Matrices','Determinants','Euclidean Vector Spaces','General Vector Spaces','Eigenvalues and Eigenvectors','Inner Product Spaces','Diagonalization and Quadratic Forms','General Linear Transformations','Numerical Methods']
starts=[1,118,146,202,291,341,399,446,509,545]
toc=pdf[13].get_text();sections=[]
for m in re.finditer(r'(?m)^(\d+\.\d+)\n(.+?)\n(\d+)\n',toc,re.S):
 number,title,page=m.groups()
 if len(title)>130:raise ValueError(title)
 sections.append({'number':number,'title':' '.join(title.split()),'printedPage':int(page)})
chapters=[]
for n,title in enumerate(names,1):
 doc=PdfWriter()
 for page in range(starts[n-1]+13,starts[n]+13):doc.add_page(source.pages[page])
 file=f'books/linear-algebra/chapter-{n:02}.pdf'
 doc.write(root/'site'/file)
 chapters.append({'number':n,'title':title,'start':starts[n-1],'end':starts[n]-1,'file':file,'sections':[dict(s,localPage=s['printedPage']-starts[n-1]+1) for s in sections if int(s['number'].split('.')[0])==n]})
# The calculus source already supplies complete question checks and reading links.
js=(root/'site/book-data.js').read_text();books=json.JSONDecoder().raw_decode(js.split('=',1)[1].lstrip())[0];calc=next(b for b in books if b['id']=='calculus');questions=json.load(gzip.open(root/'site/questions/calculus.json.gz'))
de=[]
for chapter in [9,17]:
 group=next(g for g in calc['groups'] if g.get('number')==chapter)
 rows=[]
 for s in group['sections']:
  label=s['title'].split(':')[0];qs=[q for q in questions if q['chapter']==chapter and q['section']==label]
  rows.append({'title':s['title'],'section':label,'reading':group['file']+'#page='+str(s['localPage']),'practice':'#calculus/problems/'+qs[0]['id'] if qs else '#calculus/problems/'+str(chapter),'count':len(qs)})
 de.append({'chapter':chapter,'title':group['title'],'count':sum(q['chapter']==chapter for q in questions),'reading':group['file'],'sections':rows})
data={'linearAlgebra':chapters,'differentialEquations':de}
(root/'site/math-course-data.js').write_text('window.MathCourseData='+json.dumps(data,separators=(',',':'))+';\n')
print('Chapters',len(chapters),'Sections',len(sections),'PDF bytes',sum((root/'site'/c['file']).stat().st_size for c in chapters));print([(g['chapter'],g['count'],len(g['sections'])) for g in de])
