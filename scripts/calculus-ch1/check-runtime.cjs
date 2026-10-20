/* Exercise the real enrichment, part selection, and help rendering for every Chapter 1 ID. */
const fs=require('fs'),path=require('path'),vm=require('vm'),zlib=require('zlib'),assert=require('assert'),cp=require('child_process');
const root=path.resolve(__dirname,'../..'),site=path.join(root,'site');
const read=name=>JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(site,'questions',name))));
const questions=read('calculus.json.gz'),audit=read('answer-library-calculus.json.gz');
const previous=JSON.parse(zlib.gunzipSync(cp.execFileSync('git',['show','HEAD:site/questions/answer-library-calculus.json.gz'],{cwd:root,maxBuffer:5e6})));
for(const q of questions.filter(q=>q.chapter!==1))assert.deepStrictEqual(audit.questions[q.id],previous.questions[q.id],q.id+' outside scope');
const context={console,TextDecoder,TextEncoder,Response,Blob,DecompressionStream,URL,Set,Map,Math,Number,JSON,Date,document:{addEventListener(){},querySelector(){return null},querySelectorAll(){return[]}},localStorage:{getItem(){return null},setItem(){}},fetch:async url=>new Response(fs.readFileSync(path.join(site,url)))};
context.window=context;vm.createContext(context);
for(const file of ['study-data.js','concept-choice-data.js','answer-checker.js','response-parts.js','concept-choices.js','problem-content.js','help-tutor.js','hint-journey.js','answer-library.js'])vm.runInContext(fs.readFileSync(path.join(site,file),'utf8'),context,{filename:file});
(async()=>{
 await context.AnswerLibrary.load('calculus');
 await context.HelpTutor.load();
 let rendered=0,modes=0;
 for(const original of questions.filter(q=>q.chapter===1)){
  const q=context.AnswerLibrary.validateGuidance(context.ConceptChoices.adapt(context.AnswerLibrary.enrich(context.HelpTutor.enrich(original))));
  assert(q.answerAudit.fullWorkedSolution,q.id);
  assert(q.steps.length===3,q.id+' summary');
  assert.equal(q.solutionStatus,'reviewed-specific-solution');
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
 assert.equal(rendered,368);
 const ui=fs.readFileSync(path.join(site,'textbook-practice.js'),'utf8');
 assert(ui.includes('id="question-worked-solution"'));assert(ui.includes("hintCount=2;guidance().view='solution';help();"));
 console.log(`PASS: ${rendered} exact exercises, ${modes} help modes, final-answer availability, all three help tiers, binary graders, unchanged outside chapters and direct solution entry point.`);
})().catch(e=>{console.error(e);process.exit(1)});
