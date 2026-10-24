"""Merge the six reviewed sections, review, and Problems Plus."""
import json,re,gzip,hashlib,math
from pathlib import Path
folder=Path(__file__).parent;root=folder.parents[2]
def readable(text):
 # Conservative lexical spacing: preserve mathematical identifiers/functions.
 words=['at','for','where','when','with','from','to','and','or','of','on','in','the','is','gives','gives','has','only','before','after','between','minimum','maximum','infimum','supremum','increases','decreases','positive','negative','constant','domain','real','vertical','horizontal','line','function','parabola','quadratic','curve','point','pole','asymptote','height','width','radius','length','area','volume','value','slope','limit','time','speed','distance','cost','every','all','none','no']
 for word in sorted(set(words),key=len,reverse=True):
  text=re.sub(r'\b('+word+r')(?=[0-9−±∞πθσμρ√ℝℤ])',r'\1 ',text,flags=re.I)
  text=re.sub(r'\b('+word+r')(?=[a-zA-Z][=<>⁺⁻′″²³])',r'\1 ',text,flags=re.I)
 pairs={'andthe':'and the','andis':'and is','andhas':'and has','andits':'and its','andtheir':'and their','andthen':'and then','anduse':'and use','isthe':'is the','onthe':'on the','inthe':'in the','atthe':'at the','forthe':'for the','of thezero':'of the zero','thezero':'the zero','theline':'the line','thefunction':'the function','onlywhen':'only when','allreal':'all real','Allreal':'All real','twodistinct':'two distinct','realroots':'real roots','criticalnumbers':'critical numbers','arepeatedroot':'a repeated root','a stationaryinflection':'a stationary inflection','notextrema':'not extrema','alwaysincreasing':'always increasing','Alwaysincreasing':'Always increasing','Alwaysdecreasing':'Always decreasing','alwaysdecreasing':'always decreasing','localmaximum':'local maximum','localminimum':'local minimum','globalmaximum':'global maximum','globalminimum':'global minimum','First derivative':'First derivative','endpointsand':'endpoints and','asymptotic parabolay':'asymptotic parabola y','verticalasymptotes':'vertical asymptotes','verticalasymptote':'vertical asymptote','nonzeroc':'nonzero c','forall':'for all','is tanx':'is tan x','theunderwatercostdoesnotmatter':'the underwater cost does not matter'}
 for a,b in pairs.items():text=text.replace(a,b)
 return text

def walk(obj):
 if isinstance(obj,dict):
  return {k:walk(v) if k in ('grader','parts','label','answer','options','selectionPrompt','explanation','scope','responsePartPrompt') else v for k,v in obj.items()}
 if isinstance(obj,list):return [walk(v) for v in obj]
 return readable(obj) if isinstance(obj,str) else obj
out={}
for path in [*sorted(folder.glob('section[0-9][0-9].json')),*sorted(folder.glob('section[0-9][0-9]-projects.json')),folder/'review.json',folder/'plus.json']:
 data=json.loads(path.read_text());assert not set(data)&set(out);out.update({k:walk(v) for k,v in data.items()})
source=json.loads(gzip.decompress((root/'site/questions/calculus.json.gz').read_bytes()))
expected={q['id'] for q in source if q['chapter']==9}
assert len(out)==238
assert set(out)==expected,(sorted(expected-set(out)),sorted(set(out)-expected))
counts={'questions':len(out),'fields':0,'limitedTasks':0,'numeric':0,'choice':0}
for qid,v in out.items():
 v['nativePrompt']=None;v['objectiveCheckVersion']=max(4,v.get('objectiveCheckVersion',0));g=v['grader'];fields=g.get('parts',[g]);assert len(fields)==v['objectiveFieldCount'];counts['fields']+=len(fields);counts['limitedTasks']+=g.get('complete') is False
 for f in fields:
  counts[f['type']]+=1
  if f['type']=='numeric':assert math.isfinite(f['answer']) and f['tolerance']>=0
  else:assert f['answer'] in f['options'] and len(set(f['options']))==len(f['options']) and all(isinstance(t,str) and t.strip() for t in f['options'])
(folder.parent/'chapter-09.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
counts.update(sourceSHA256=hashlib.sha256((root/'site/books/calculus/chapter-09.pdf').read_bytes()).hexdigest(),missing=[],scope='All 238 source IDs. Limited drawing/proof tasks check conclusions, not full task completion.')
(folder/'coverage-audit.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
