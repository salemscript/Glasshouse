const fs=require('fs'),vm=require('vm'),zlib=require('zlib'),path=require('path');const site=path.resolve('site');
const c={console,TextDecoder,TextEncoder,Response,Blob,DecompressionStream,URL,Set,Map,Math,Number,JSON,Date,setTimeout,clearTimeout,document:{compatMode:"CSS1Compat",addEventListener(){},querySelector(){return null},querySelectorAll(){return[]}},localStorage:{getItem(){return null},setItem(){}},fetch:async url=>{let p=path.join(site,url);return fs.existsSync(p)?new Response(fs.readFileSync(p)):new Response('',{status:404})}};c.window=c;vm.createContext(c);
for(const file of ['book-data.js','vendor/katex/katex.min.js','linear-math.js','solution-math.js','study-data.js','concept-choice-data.js','answer-checker.js','response-parts.js','concept-choices.js','problem-content.js','help-tutor.js','hint-journey.js','answer-library.js','math-course-data.js','math-courses.js','linear-section-data.js','linear-review-data.js','math-workspace.js','textbook-practice.js']){let s=fs.readFileSync(path.join(site,file),'utf8');if(file==='textbook-practice.js')s=s.replace('return {html,configure,check,context,sourceSVG,state:', 'return {audit:{enrich,rules,loadPacks},html,configure,check,context,sourceSVG,state:');vm.runInContext(s,c,{filename:file});}

(async()=>{
 await c.HelpTutor.load();await c.TextbookPractice.audit.loadPacks();await c.AnswerLibrary.load('linear-algebra');
 const raw=c.MathWorkspace.questions(),audit=[];let checks=0;
 const assert=(test,message)=>{if(!test)throw Error(message)};
 assert(raw.length===755,'Question count changed');
 for(const source of raw){
  const q=c.TextbookPractice.audit.enrich(source),rs=c.TextbookPractice.audit.rules(q);
  assert(q.answerAudit?.fullWorkedSolution&&q.answerAudit?.objectiveChecksVerified,q.id+' missing verified work');
  assert(!q.reviewPractice,q.id+' still uses uncheckable review textarea');
  assert(rs.length&&rs.every(r=>r.checkable),q.id+' unavailable response');
  assert(q.grader.complete!==false,q.id+' limited scope');
  assert(q.learningSolutions.length===rs.length,q.id+' mismatched solution fields');
  for(const r of rs){
   const rule=r.rule||r;
   assert(c.AnswerChecker.check(rule,String(rule.answer)).status==='correct',q.id+' correct rejected');
   assert(c.AnswerChecker.check(rule,'').status==='invalid',q.id+' blank accepted');
   const wrong=rule.type==='choice'?rule.options.filter(x=>x!==rule.answer):[Number(rule.answer)+100*Math.max(1,Math.abs(Number(rule.answer)))];
   for(const value of wrong)assert(c.AnswerChecker.check(rule,String(value)).status!=='correct',q.id+' wrong accepted');
   if(rule.type==='choice'){
    const html=c.ConceptChoices.field({...rule,fieldKey:'test'},'');
    assert(!html.includes('linear-math-fallback'),q.id+' broken choice mathematics');
   }
   checks++;
  }
  for(const [solutionIndex,solution] of q.learningSolutions.entries()){
   const plan=c.HintJourney.plan(q,solutionIndex),html=c.HintJourney.render(plan,3,{revealed:true});
   assert(plan.auditParts.every(part=>part.answer!==undefined)&&!html.includes('linear-math-fallback')&&!html.includes('answer-missing'),q.id+' broken final-answer/solution view');
   assert(solution.workedSteps?.length,q.id+' missing worked steps');
   for(const step of solution.workedSteps)assert(!c.SolutionMath.render(step).includes('linear-math-fallback'),q.id+' broken solution math');
  }
  const parts=q.answerAudit.sourceFigureParts||q.parts||[];
  for(const p of parts)assert(fs.existsSync(path.join(site,p.file)),q.id+' missing source art '+p.file);
  audit.push({id:q.id,chapter:q.chapter,fields:rs.length,reviewNotice:q.reviewNotice||''});
 }
 assert(c.SolutionMath.render('The result is \\(\\frac{1}{2}\\).').includes('mfrac'),'TeX fraction not stacked');
 assert(c.SolutionMath.render('\\(\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}\\)').includes('mtable'),'Matrix not typeset');
 assert(c.SolutionMath.render('1/2').includes('mfrac'),'Legacy fraction regression');
 const report={date:'2026-10-26',questions:audit.length,fields:checks,missingQuestions:0,missingFields:0,chapters:Array.from({length:9},(_,i)=>({chapter:i+1,questions:audit.filter(q=>q.chapter===i+1).length,fields:audit.filter(q=>q.chapter===i+1).reduce((n,q)=>n+q.fields,0)})),records:audit};
 fs.writeFileSync('scripts/linear-answer-checks/runtime-audit.json',JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({...report,records:undefined},null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
