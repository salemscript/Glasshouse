"""Independently compare stored Chapter3 derivative contracts with source-aligned rules.
Uses source inspection to flag transcription corrections; never generates site graders.
"""
from pathlib import Path
import gzip,json,re,math,hashlib
from datetime import datetime,timezone
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parents[2]
QS=json.loads(gzip.decompress((ROOT/'site/questions/calculus.json.gz').read_bytes()))
LIB=json.loads(gzip.decompress((ROOT/'site/questions/answer-library-calculus.json.gz').read_bytes()))
SYMS={k:S.Symbol(k,real=True)for k in ['x','y','z','t','u','v','s','r','p','q','a','b','c','d','n','A','B','C','R','θ']}
LOCALS={**SYMS,'e':S.E,'pi':S.pi,'ln':S.log,'sqrt':S.sqrt,'arcsin':S.asin,'arccos':S.acos,'arctan':S.atan,'arcsec':S.asec,'arccot':S.acot,'arsinh':S.asinh,'arcosh':S.acosh,'artanh':S.atanh,'arsech':S.asech,'arcoth':S.acoth,'Abs':S.Abs,'cbrt':lambda value:S.Pow(value,S.Rational(1,3))}
TRANS=standard_transformations+(implicit_multiplication_application,)
SUP='⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺';PLAIN='0123456789-+'
def parse(raw):
 raw=re.sub('['+SUP+']+',lambda m:'^('+''.join(PLAIN[SUP.index(c)]for c in m[0])+')',raw)
 raw=raw.replace('−','-').replace('·','*').replace('π','(pi)').replace('√','sqrt').replace('∛','cbrt').replace('^','**')
 raw=re.sub(r'\|([^|]+)\|',r'Abs(\1)',raw)
 raw=re.sub(r'(sqrt|cbrt)([A-Za-z0-9]+)',r'\1(\2)',raw)
 return parse_expr(raw,local_dict=LOCALS,transformations=TRANS)

def finite(z):
 z=complex(S.N(z,30));return z.real if abs(z.imag)<1e-10 and math.isfinite(z.real)else None
LEGACY_IDS=set(json.loads((Path(__file__).parent/'legacy-chapter3-review.json').read_text())['legacyIds'])
checks=0;verified=[];failures=[];manual=[];details=[]
# Original variable names in the PDF; these four native representations rename them.
VARFIX={'calculus-section-3-1-20':('x','R'),'calculus-section-3-1-46':('x','r'),'calculus-section-3-5-55':('x','t'),'calculus-section-3-5-56':('x','t'),'calculus-section-3-5-58':('x','t')}
# Source-authoritative function checks: mismatched native transcriptions fail explicitly.
SOURCEFIX={'calculus-section-3-2-13':'(x²+1)/(x³−1)'}
MANUAL={
'calculus-section-3-1-34':['3*x+2'],
'calculus-section-3-1-36':['-3*x/4+3/4'],
'calculus-section-3-1-38':['3*x/2-1/2','-2*x/3+5/3'],
'calculus-section-3-1-40':['x/2-1/2'],
'calculus-section-3-6-31':['2'],
'calculus-section-3-6-32':['0'],
'calculus-section-3-6-37':['7'],
'calculus-section-3-6-38':['e**2']}

for q in QS:
 qid=q['id'];a=LIB['questions'].get(qid,{})
 # Explicitly select the source-era contracts even if another agent added metadata.
 if q['chapter']!=3 or not a.get('nativePrompt') or q['sourceSet'] not in ['section-3-1','section-3-2','section-3-3','section-3-4','section-3-5','section-3-6','section-3-11']:continue
 if qid not in LEGACY_IDS:continue
 g=a['grader'];fields=g.get('parts')if g['type']=='parts'else[g]
 if qid in MANUAL:
  assert len(fields)==len(MANUAL[qid])
  for field,expr in zip(fields,MANUAL[qid]):
   ans=parse(re.sub(r'^\s*y\s*=\s*','',str(field['answer'])));want=parse(expr)
   assert abs(complex(S.N((ans-want).subs(SYMS['x'],S.Rational(7,5)),30)))<1e-12,(qid,ans,want)
   checks+=1
  verified.append(qid);continue
 body=a['nativePrompt'].splitlines()[-1].split(';')[0]
 # Questions embedding a whole instruction sentence are independently checked separately.
 if (len(a['nativePrompt'].splitlines())==1 and not re.match(r'^(?:[A-Za-zΑ-ω]\([A-Za-zΑ-ω]\)|y)\s*=',body)) or body.startswith('Illustrate')or'point'in body:
  manual.append(qid);continue
 try:
  assignment=re.match(r'^\s*(?:[A-Za-zΑ-ω]\([A-Za-zΑ-ω]\)|y)\s*=\s*',body)
  implicit=bool(re.search(r'=\s*0\s*$',body)) and not assignment
  if implicit:
   F=parse(body.split('=')[0]);x,y=SYMS['x'],SYMS['y']
   if fields[0]['label']=='dx/dy':expected=-S.diff(F,y)/S.diff(F,x)
   else:
    yp=-S.diff(F,x)/S.diff(F,y);expected=yp
    if 'd²' in fields[0]['label']:
     expected=S.diff(yp,x)+S.diff(yp,y)*yp
   fexpr=None;variable=None
  else:
   if assignment:body=body[assignment.end():]
   fexpr=parse(body)
   if qid in SOURCEFIX:
    assert S.simplify(fexpr-parse(SOURCEFIX[qid]))==0,(qid,'Native function does not match the visually checked source',body)
   candidates=[SYMS[z] for z in ['x','t','u','v','s','r','p','q','y','z','a','R','θ']if SYMS[z]in fexpr.free_symbols]
   # Source-independent variable can be a even with constants elsewhere.
   variable=candidates[0]if candidates else SYMS['x']
   if q['sourceSet']=='section-3-1' and q['number']=='15':variable=SYMS['a']
  ok=True
  for i,f in enumerate(fields):
   if f.get('label')=='Domain':continue
   if not implicit:expected=S.diff(fexpr,variable,2 if'second'in f.get('label','').lower()else 1)
   ans=parse(str(f['answer']))
   # Compare in the native variable; some old labels use the actual source variable.
   if qid in VARFIX:
    old,new=VARFIX[qid]
    if fexpr is not None and SYMS[old] in fexpr.free_symbols and SYMS[new] not in fexpr.free_symbols:
     ans=ans.subs(SYMS[new],SYMS[old])
   diff=S.together(expected-ans)
   numer,denom=S.fraction(diff)
   if implicit and q['number']in['35','36','38']and q['sourceSet']=='section-3-5':
    numer=S.rem(numer,S.Poly(F,SYMS['y']).as_expr(),SYMS['y'])
    diff=numer/denom
   samples=0;bad=[]
   for v in [-2.3,-1.7,-.7,-.3,.2,.45,.7,1.2,1.7,2.3,3.1]:
    subs={sym:S.Rational(str(v))for sym in diff.free_symbols}
    # Separate constants avoid coincident cancellation; positive a>b and parameters.
    subs.update({SYMS['a']:S.Rational(7,2),SYMS['b']:S.Rational(3,2),SYMS['c']:S.Rational(4,3),SYMS['d']:S.Rational(5,3),SYMS['A']:2,SYMS['B']:3,SYMS['C']:5,SYMS['n']:3})
    # a is the independent variable in3.1#15.
    if qid=='calculus-section-3-1-15':subs[SYMS['a']]=S.Rational(str(v))
    try:
     ev=finite(expected.subs(subs));av=finite(ans.subs(subs))
     if ev is None or av is None:continue
     samples+=1;checks+=1
     dv=finite(diff.subs(subs))
     if dv is None or abs(dv)>1e-7*max(1,abs(ev),abs(av)):bad.append((v,ev,av))
    except (TypeError,ValueError,OverflowError,ZeroDivisionError):continue
   if not samples:
    if S.simplify(diff)==0:samples=1;checks+=1
    else:bad.append(('no real sample',str(diff)))
   if bad:ok=False;failures.append(dict(id=qid,label=f.get('label'),body=body,answer=f['answer'],bad=bad[:3]))
  if ok:verified.append(qid)
 except Exception as exc:manual.append(qid);details.append((qid,type(exc).__name__,str(exc)[:200],body))
verified_set=set(verified)
missing=sorted(LEGACY_IDS-verified_set)
unexpected=sorted(verified_set-LEGACY_IDS)
passed=(not failures and not manual and not details and len(verified)==246
        and len(verified_set)==246 and len(LEGACY_IDS)==246
        and not missing and not unexpected)
report=dict(passed=passed,checkedAtUTC=datetime.now(timezone.utc).isoformat(),
            bankSha256=hashlib.sha256((ROOT/'site/questions/answer-library-calculus.json.gz').read_bytes()).hexdigest(),
            sourceSha256=hashlib.sha256((ROOT/'site/books/calculus/chapter-03.pdf').read_bytes()).hexdigest(),
            expected=246,assertions=checks,verified=len(verified),
            verifiedIds=sorted(verified_set),missing=missing,unexpected=unexpected,
            failures=failures,manual=manual,parseDetails=details)
# Keep this current-run evidence separate from the historical source-error audit.
output=Path(__file__).with_name('legacy-chapter3-verification.json')
output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if passed else 1)
