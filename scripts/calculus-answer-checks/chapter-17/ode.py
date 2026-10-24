from common import *
C1,C2=s.symbols('C1 C2');Y=s.Function('y');cases=[]
def op(y,abc):return s.expand(abc[0]*s.diff(y,x,2)+abc[1]*s.diff(y,x)+abc[2]*y)
def solve(abc,rhs=0,ics=None):
 eq=s.Eq(op(Y(x),abc),rhs)
 kw={} if ics is None else {'ics':{Y(x).subs(x,p):v for p,v in ics.get('y',[]) }|{s.diff(Y(x),x).subs(x,p):v for p,v in ics.get('dy',[])}}
 sol=s.dsolve(eq,**kw).rhs
 assert s.simplify(s.expand_trig(op(sol,abc)-rhs))==0,(abc,rhs,sol)
 if ics:
  for p,v in ics.get('y',[]):assert s.simplify(sol.subs(x,p)-v)==0
  for p,v in ics.get('dy',[]):assert s.simplify(s.diff(sol,x).subs(x,p)-v)==0
 cases.append(dict(coefficients=list(map(str,abc)),forcing=str(rhs),solution=str(sol),ics={k:[[str(p),str(v)] for p,v in vals] for k,vals in (ics or {}).items()}))
 return sol

def answer(sol,abc,label='Solution y(x)',var=x):
 power=next(k for k in range(5) if s.simplify(op(x**k,abc))!=0)
 return c(label,fmt(sol.subs(x,var)),fmt((sol+x**power).subs(x,var)),fmt((sol-x**power).subs(x,var)))
def iv(y,v,p=0):return {'y':[(p,s.sympify(y))],'dy':[(p,s.sympify(v))]}
def save(name):
 here=ROOT/'scripts/calculus-answer-checks/chapter-17'
 (here/(name+'.json')).write_text(json.dumps(A.out,ensure_ascii=False,indent=2)+'\n')
 (here/(name+'-audit.json')).write_text(json.dumps({'notes':A.notes,'differentialChecks':cases},ensure_ascii=False,indent=2)+'\n');print(name,len(A.out),len(cases))
