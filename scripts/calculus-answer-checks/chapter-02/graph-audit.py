import fitz,math
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3]
p=fitz.open(ROOT/'site/books/calculus/chapter-02.pdf')[83]
curves=[d for d in p.get_drawings() if d.get('color') and d['color'][2]>.9 and d['rect'].y0>570 and len(d['items'])>1]
def slope(path,xx):
 for it in path['items']:
  if it[0]!='c':continue
  a,b,c,d=it[1:]
  if a.x-1e-4<=xx<=d.x+1e-4:
   lo,hi=0.,1.
   for _ in range(60):
    t=(lo+hi)/2;x=(1-t)**3*a.x+3*(1-t)**2*t*b.x+3*(1-t)*t*t*c.x+t**3*d.x
    if x<xx:lo=t
    else:hi=t
   t=(lo+hi)/2
   dx=3*((1-t)**2*(b.x-a.x)+2*(1-t)*t*(c.x-b.x)+t*t*(d.x-c.x))
   dy=3*((1-t)**2*(b.y-a.y)+2*(1-t)*t*(c.y-b.y)+t*t*(d.y-c.y))
   return -dy/dx
rows={}
for n,path,origin,xs in [(1,curves[1],154.8452,range(-3,4)),(2,curves[0],376.8453,range(8))]:
 rows[str(n)]={str(x):round(slope(path,origin+12*x),5) for x in xs}
report=dict(sourcePdf='site/books/calculus/chapter-02.pdf',localPage=84,printedPage=160,section='2.8',method='Differentiate original drawn cubic Bezier segments at each labeled x, using the diagram’s equal axis scales. Values guide graph-estimate tolerances; artwork is not an exact underlying analytic model.',tangents=rows)
(Path(__file__).parent/'graph-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
