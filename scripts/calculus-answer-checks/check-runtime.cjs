/* Run the actual practice enrichment/part/checker pipeline for Chapters 1–17. */
const fs=require('fs'),path=require('path'),vm=require('vm'),zlib=require('zlib'),assert=require('assert'),cp=require('child_process');
const root=path.resolve(__dirname,'../..'),site=path.join(root,'site');
const read=name=>JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(site,'questions',name))));
const source=read('calculus.json.gz'),library=read('answer-library-calculus.json.gz');
const previous=JSON.parse(zlib.gunzipSync(cp.execFileSync('git',['show','HEAD:site/questions/answer-library-calculus.json.gz'],{cwd:root,maxBuffer:10e6})));
for(const q of source.filter(q=>![14,15,16,17].includes(q.chapter)))assert.deepStrictEqual(library.questions[q.id],previous.questions[q.id],q.id+' outside scope');
const c={console,TextDecoder,TextEncoder,Response,Blob,DecompressionStream,URL,Set,Map,Math,Number,JSON,Date,setTimeout,clearTimeout,document:{addEventListener(){},querySelector(){return null},querySelectorAll(){return[]}},localStorage:{getItem(){return null},setItem(){}},fetch:async url=>new Response(fs.readFileSync(path.join(site,url)))};
c.window=c;vm.createContext(c);
for(const file of ['study-data.js','concept-choice-data.js','answer-checker.js','response-parts.js','concept-choices.js','problem-content.js','help-tutor.js','hint-journey.js','answer-library.js','textbook-practice.js'])vm.runInContext(fs.readFileSync(path.join(site,file),'utf8'),c,{filename:file});
(async()=>{
 const totals={};const failures=[];
 for(const original of source.filter(q=>[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17].includes(q.chapter))){
  try{
   const q=(await c.TextbookPractice.context('calculus',original.id)).question;
   const fields=c.ResponseParts.fields(q);
   if(/[^\x00-\x7F]/.test(original.id)){assert.equal((await c.TextbookPractice.context('calculus',encodeURIComponent(original.id))).question.id,original.id,'encoded Unicode exercise ID');}
   assert(fields.length&&fields.every(f=>f.rule&&['numeric','choice'].includes(f.rule.type)),q.id+' missing or unsupported response');
   const audit=q.answerAudit;assert(audit.objectiveChecksVerified,q.id+' not explicitly reviewed');
   assert.equal(fields.length,audit.objectiveFieldCount,q.id+' field count');
   const row=totals[q.chapter]??={questions:0,fields:0,numeric:0,choice:0,wrongCases:0,limited:0};
   row.questions++;if(q.grader.complete===false)row.limited++;
   for(const f of fields){
    const rule=c.ConceptChoices.responseRule(f.rule,q,f.graderIndex)||f.rule;
    assert.equal(c.AnswerChecker.check(rule,String(rule.answer)).status,'correct',q.id+' correct '+f.label);
    assert.equal(c.AnswerChecker.check(rule,'').status,'invalid',q.id+' blank '+f.label);
    row.fields++;row[rule.type]++;
    if(rule.type==='numeric'){
     const expected=Number(rule.answer),delta=Math.max(1,Math.abs(expected)*.1,(rule.tolerance||0)*10,(rule.relativeTolerance||0)*Math.abs(expected)*10);
     assert.equal(c.AnswerChecker.check(rule,String(expected+delta)).status,'incorrect',q.id+' wrong numeric '+f.label);
     assert.equal(c.AnswerChecker.check(rule,'not a number').status,'invalid',q.id+' invalid numeric '+f.label);
     row.wrongCases++;
    }else{
     assert(rule.options.length>=2&&new Set(rule.options).size===rule.options.length,q.id+' options');
     for(const option of rule.options.filter(o=>o!==rule.answer)){
      assert.equal(c.AnswerChecker.check(rule,option).status,'incorrect',q.id+' distractor '+f.label);row.wrongCases++;
     }
    }
   }
  }catch(e){failures.push({id:original.id,error:e.message});}
 }
 fs.writeFileSync(path.join(__dirname,'runtime-audit.json'),JSON.stringify({totals,failures},null,2)+'\n');
 assert.equal(failures.length,0,JSON.stringify(failures.slice(0,8)));
 for(const [ch,total] of [[1,368],[2,570],[3,844],[4,785],[5,486],[6,307],[7,647],[8,239],[9,238],[10,455],[11,751],[12,449],[13,286],[14,646],[15,490],[16,436],[17,123]])assert.equal(totals[ch].questions,total,'chapter '+ch+' coverage');
 console.log('PASS actual practice pipeline: '+JSON.stringify(totals));
})().catch(e=>{console.error(e);process.exitCode=1});
