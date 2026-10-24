import sys,importlib.util,json,hashlib,math,random
from pathlib import Path
import sympy as s
import mpmath as mp
BASE=Path(__file__).resolve().parents[1]/'chapter-05/common.py'
spec=importlib.util.spec_from_file_location('calculus_contract_base',BASE);base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
ROOT=base.ROOT;A=base.Author(9);row=A.row;n=base.n;c=base.c;f=base.f;fmt=base.fmt;R=s.Rational;pi=s.pi;x=base.x;y,t=s.symbols('y t',real=True);mp.mp.dps=50;TESTS=[]
def check(label,residual):
 value=s.simplify(residual);assert value==0,(label,value);TESTS.append(dict(label=label,residual=str(value)))
def near(label,value,target,tol=1e-8):
 assert abs(float(value)-float(target))<=tol*max(1,abs(float(target))),(label,value,target);TESTS.append(dict(label=label,value=float(value),expected=float(target)))
def finish(name,pages):
 folder=Path(__file__).parent
 (folder/(name+'.json')).write_text(json.dumps(A.out,ensure_ascii=False,indent=2)+'\n')
 audit=dict(chapter=9,sourceSHA256=hashlib.sha256((ROOT/'site/books/calculus/chapter-09.pdf').read_bytes()).hexdigest(),reviewedPrintedPages=pages,questions=A.notes,checks=TESTS,limits='Graph, direction-field, full written proof and modeling discussion checks verify selected mathematical conclusions rather than the full original work. Those records are marked complete:false.')
 (folder/(name+'-audit.json')).write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
 print(name,len(A.out),'records',sum(len(v['grader'].get('parts',[v['grader']])) for v in A.out.values()),'fields',len(TESTS),'checks')
