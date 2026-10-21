/* Exercise the real enrichment, part selection, and help rendering for every Chapter 1 ID. */
const fs=require('fs'),path=require('path'),vm=require('vm'),zlib=require('zlib'),assert=require('assert'),cp=require('child_process');
const root=path.resolve(__dirname,'../..'),site=path.join(root,'site');
const read=name=>JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(site,'questions',name))));
const questions=read('calculus.json.gz'),audit=read('answer-library-calculus.json.gz');
const previous=JSON.parse(zlib.gunzipSync(cp.execFileSync('git',['show','HEAD:site/questions/answer-library-calculus.json.gz'],{cwd:root,maxBuffer:5e6})));
const authored=q=>audit.questions[q.id]?.workedSolutionSource?.authoringFile==='scripts/calculus-expansion/author.py';
for(const q of questions.filter(q=>!authored(q)))assert.deepStrictEqual(audit.questions[q.id],previous.questions[q.id],q.id+' outside scope');
const context={console,TextDecoder,TextEncoder,Response,Blob,DecompressionStream,URL,Set,Map,Math,Number,JSON,Date,document:{addEventListener(){},querySelector(){return null},querySelectorAll(){return[]}},localStorage:{getItem(){return null},setItem(){}},fetch:async url=>new Response(fs.readFileSync(path.join(site,url)))};
context.window=context;vm.createContext(context);
for(const file of ['study-data.js','concept-choice-data.js','answer-checker.js','response-parts.js','concept-choices.js','problem-content.js','help-tutor.js','hint-journey.js','answer-library.js'])vm.runInContext(fs.readFileSync(path.join(site,file),'utf8'),context,{filename:file});
(async()=>{
 await context.AnswerLibrary.load('calculus');
 await context.HelpTutor.load();
 let rendered=0,modes=0,fieldsChecked=0,wrongChecks=0;
 for(const original of questions.filter(q=>authored(q)||q.chapter===1)){
  const q=context.AnswerLibrary.validateGuidance(context.ConceptChoices.adapt(context.AnswerLibrary.enrich(context.HelpTutor.enrich(original))));
  assert(q.answerAudit.fullWorkedSolution,q.id);
  assert(q.steps.length===3,q.id+' summary');
  assert.equal(q.solutionStatus,'reviewed-specific-solution');
  const fields=context.ResponseParts.fields(q);
  assert.equal(fields.length,q.answerAudit.objectiveFieldCount,q.id+' field contract');
  for(const f of fields){
   assert(f.rule&&['numeric','choice'].includes(f.rule.type),q.id+' unavailable field '+f.label);
   const rule=context.ConceptChoices.responseRule(f.rule,q,f.graderIndex)||f.rule;
   assert.equal(context.AnswerChecker.check(rule,String(rule.answer)).status,'correct',q.id+' correct '+f.label);
   assert.equal(context.AnswerChecker.check(rule,'').status,'invalid',q.id+' empty '+f.label);
   if(rule.type==='numeric'){
    const delta=Math.max(1,Math.abs(rule.answer)*.1,(rule.tolerance||0)*10);
    assert.equal(context.AnswerChecker.check(rule,String(rule.answer+delta)).status,'incorrect',q.id+' wrong numeric');
    assert.equal(context.AnswerChecker.check(rule,'not a number').status,'invalid',q.id+' invalid numeric');
    wrongChecks++;
   }else{
    for(const option of rule.options.filter(o=>o!==rule.answer)){
     assert.equal(context.AnswerChecker.check(rule,option).status,'incorrect',q.id+' wrong option '+option);wrongChecks++;
    }
   }
   fieldsChecked++;
  }
  const count=Math.max(1,context.HelpTutor.modes(q).length);
  for(let i=0;i<count;i++){
   const p=context.HintJourney.plan(q,i);
   assert(context.HintJourney.canReveal(p),q.id+' cannot reveal');
   const html=context.HintJourney.render(p,3,{view:'solution'});
   for(const marker of ['WORKED SOLUTION','Work through the question','Final answer'])assert(html.includes(marker),q.id+' '+marker);
   assert(!html.includes('A reliable final answer is still being checked'),q.id+' missing final');
   assert(!html.includes('exact worked walkthrough is still unavailable'),q.id+' stale gap');
   assert(!html.includes('an exact problem-specific walkthrough is not available yet'),q.id+' stale method');
   assert(!html.includes('[object Object]'),q.id+' serialization');
   for(const tier of [1,2])assert(!context.HintJourney.render(p,tier,{}).includes('exact worked walkthrough is still unavailable'),q.id+' stale help note');
   modes++;
  }
  const rules=q.grader?.type==='parts'?q.grader.parts:q.grader?[q.grader]:[];
  for(const rule of rules){if(rule.type==='choice'){assert.equal(context.AnswerChecker.check(rule,rule.answer).status,'correct');assert.equal(context.AnswerChecker.check(rule,rule.options.find(x=>x!==rule.answer)).status,'incorrect');}}
  rendered++;
 }
 assert.equal(rendered,496);
 assert.equal(fieldsChecked,842);
 const ui=fs.readFileSync(path.join(site,'textbook-practice.js'),'utf8');
 assert(ui.includes('id="question-worked-solution"'));assert(ui.includes("hintCount=2;guidance().view='solution';help();"));
 console.log(`PASS: ${rendered} checkable exercises, ${fieldsChecked} numeric/choice fields, ${wrongChecks} wrong-answer cases, ${modes} help modes, blank/invalid inputs, worked solutions and unchanged outside authored IDs.`);
})().catch(e=>{console.error(e);process.exit(1)});
