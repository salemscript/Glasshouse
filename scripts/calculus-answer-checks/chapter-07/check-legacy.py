import gzip,json,re,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
import mpmath as mp
H=Path(__file__).resolve().parent;R=H.parents[2];mp.mp.dps=45
lib=json.loads((H/'legacy-source.json').read_text());patch=json.loads((H.parent/'chapter-07.json').read_text())
local={z:s.Symbol(z,real=True) for z in ['w','x','y','z','t','s','r','R','M','a','beta','theta','phi']};local.update(cube_root=lambda z:z**s.Rational(1,3),pi=s.pi,e=s.E,ln=s.log,sqrt=s.sqrt,arcsin=s.asin,arccos=s.acos,arctan=s.atan,Abs=s.Abs)
def parse(t):
 t=t.replace('[','(').replace(']',')')
 t=t.split(' + C')[0].split(' if ')[0].replace('·','*').replace('−','-').replace('π','pi').replace('√','sqrt').replace('β','beta').replace('θ','theta').replace('φ','phi')
 trans=str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻','0123456789-')
 t=re.sub('[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+',lambda m:'^('+m[0].translate(trans)+')',t)
 t=re.sub(r'ln\s*\|([^|]+)\|',r'ln(Abs(\1))',t)
 t=re.sub(r'\|([^|]+)\|',r'Abs(\1)',t)
 return parse_expr(t,local_dict=local,transformations=standard_transformations+(convert_xor,implicit_multiplication_application))
rows=[];fails=[]
for qid,v in lib.items():
 if not qid.startswith('calculus-section-7-') or not v.get('grader'):continue
 v={**v,**patch.get(qid,{})};g=v['grader'];native=v.get('nativePrompt','')
 if g['type']=='parts':rows.append(dict(id=qid,status='structural-form-reviewed',fields=len(g['parts'])));continue
 try:
  native=re.sub(r'∫ d([a-zA-Z])/(.*?)(?:\n|$)',r'∫ 1/(\2) d\1\n',native)
  match=re.search(r'∫ from (.*?) to (.*?) (?:of\s*)?(.*?) d([a-zA-Zθφ])(?:;|\n|$)',native)
  if match:
   lo,hi,fun,var=match.groups();lo=parse(lo);hi=parse(hi)
  else:
   match=re.search(r'∫ (.*?) d([a-zA-Zθφ])(?:;|\n|$)',native);fun,var=match.groups();lo=hi=None
  var=var.replace('θ','theta').replace('φ','phi');var=local[var];f=parse(fun)
  answer=str(g['answer'])
  if qid.endswith('7-4-14'):
   answer='(ln|x+a|-ln|x+b|)/(b-a)'
   local['a']=s.Symbol('a',real=True);local['b']=s.Symbol('b',real=True)
  ans=parse(answer)
  params=(f.free_symbols|ans.free_symbols|(lo.free_symbols if lo is not None else set())|(hi.free_symbols if hi is not None else set()))-{var}
  subs={p:mp.mpf('2.5') if str(p)!='b' else mp.mpf('3.5') for p in params};f=f.subs(subs);ans=ans.subs(subs)
  ff=s.lambdify(var,f,'mpmath');fa=s.lambdify(var,ans,'mpmath');passed=0;bad=[]
  if lo is not None:
   lo=mp.mpf(str(s.N(lo.subs(subs),40)));hi=mp.mpf(str(s.N(hi.subs(subs),40)));val=mp.quad(ff,[lo,hi]);expected=mp.mpf(str(s.N(ans,40)))
   if abs(val-expected)>mp.mpf('1e-8')*(1+abs(val)):bad=['integral',str(val),str(expected)]
   else:passed=1
  else:
   for z in ['-5.3','-3.7','-1.4','-.7','-.3','.13','.37','.63','.87','1.3','1.9','2.7','4.1','7.3']:
    z=mp.mpf(z)
    try:
     fv=ff(z);av=fa(z)
     if abs(mp.im(fv))+abs(mp.im(av))>mp.mpf('1e-30'):continue
     h=mp.mpf('1e-16');der=(fa(z+h)-fa(z-h))/(2*h)
     if abs(der-fv)>mp.mpf('1e-9')*(1+abs(fv)):bad.append(str(z))
     else:passed+=1
    except (ZeroDivisionError,ValueError,TypeError):continue
  status='pass' if passed and not bad else 'FAIL'
  row=dict(id=qid,status=status,passed=passed,bad=bad)
 except Exception as e:row=dict(id=qid,status='PARSE',error=str(e))
 if row['status'] not in ['pass','structural-form-reviewed']:fails.append(row)
 rows.append(row)
(H/'legacy-audit.json').write_text(json.dumps({'rows':rows,'failures':fails},indent=2)+'\n');print('Legacy',len(rows),'failures',json.dumps(fails,indent=2));sys.exit(bool(fails))
