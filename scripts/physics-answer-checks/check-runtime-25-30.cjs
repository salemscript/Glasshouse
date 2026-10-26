/* Run the actual practice enrichment/part/checker pipeline for all physics chapter 25–30 records. */
const fs=require('fs'),path=require('path'),vm=require('vm'),zlib=require('zlib'),assert=require('assert'),cp=require('child_process');
const root=path.resolve(__dirname,'../..'),site=path.join(root,'site');
const read=name=>JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(site,'questions',name))));
const all=read('physics.json.gz'),source=all.filter(q=>[25,26,27,28,29,30].includes(q.chapter)),library=read('answer-library-physics.json.gz');
const previous=JSON.parse(zlib.gunzipSync(cp.execFileSync('git',['show','HEAD:site/questions/answer-library-physics.json.gz'],{cwd:root,maxBuffer:10e6})));
for(const q of all.filter(q=>![25,26,27,28,29,30].includes(q.chapter)))assert.deepStrictEqual(library.questions[q.id],previous.questions[q.id],q.id+' outside scope');
const c={console,TextDecoder,TextEncoder,Response,Blob,DecompressionStream,URL,Set,Map,Math,Number,JSON,Date,setTimeout,clearTimeout,document:{addEventListener(){},querySelector(){return null},querySelectorAll(){return[]}},localStorage:{getItem(){return null},setItem(){}},fetch:async url=>new Response(fs.readFileSync(path.join(site,url)))};
c.window=c;vm.createContext(c);
for(const file of ['solution-math.js','study-data.js','concept-choice-data.js','answer-checker.js','response-parts.js','concept-choices.js','problem-content.js','help-tutor.js','hint-journey.js','answer-library.js','textbook-practice.js'])vm.runInContext(fs.readFileSync(path.join(site,file),'utf8'),c,{filename:file});
(async()=>{
 const totals={};const failures=[];
 for(const original of source){
  try{
   const q=(await c.TextbookPractice.context('physics',original.id)).question;
   const fields=c.ResponseParts.fields(q);
   if(/[^\x00-\x7F]/.test(original.id)){assert.equal((await c.TextbookPractice.context('physics',encodeURIComponent(original.id))).question.id,original.id,'encoded Unicode exercise ID');}
   assert(fields.length&&fields.every(f=>f.rule&&['numeric','choice'].includes(f.rule.type)),q.id+' missing or unsupported response');
   const audit=q.answerAudit;assert(audit.objectiveChecksVerified,q.id+' not explicitly reviewed');
   assert.equal(fields.length,audit.objectiveFieldCount,q.id+' field count');
   const row=totals[q.chapter]??={questions:0,fields:0,numeric:0,choice:0,wrongCases:0,limited:0};
   row.questions++;if(q.grader.complete===false)row.limited++;
   for(const f of fields){
    const rule=c.ConceptChoices.responseRule(f.rule,q,f.graderIndex)||f.rule;
    assert.equal(c.AnswerChecker.check(rule,String(rule.answer)).status,'correct',q.id+' correct '+f.label);
    assert.equal(c.AnswerChecker.check(rule,'').status,'invalid',q.id+' blank '+f.label);
    for(const accepted of rule.acceptedValues||[])assert.equal(c.AnswerChecker.check(rule,String(accepted)).status,'correct',q.id+' rounded/alternate answer');
    row.fields++;row[rule.type]++;
    if(rule.type==='numeric'){
     const expected=Number(rule.answer),delta=Math.max(1,Math.abs(expected)*.1,(rule.tolerance||0)*10,(rule.relativeTolerance||0)*Math.abs(expected)*10);
     assert.equal(c.AnswerChecker.check(rule,String(expected+delta)).status,'incorrect',q.id+' wrong numeric '+f.label);
     assert.equal(c.AnswerChecker.check(rule,'not a number').status,'invalid',q.id+' invalid numeric '+f.label);
     const zeroIsAccepted=(rule.acceptedValues||[]).some(v=>Math.abs(Number(v))<=Number(rule.tolerance||0));
     if(expected!==0&&!zeroIsAccepted)assert.equal(c.AnswerChecker.check(rule,'0').status,'incorrect',q.id+' zero instead of nonzero quantity');
     const oppositeIsAccepted=(rule.acceptedValues||[]).some(v=>Math.abs(Number(v)+expected)<=Number(rule.tolerance||0)+Number(rule.relativeTolerance||0)*Math.abs(expected));
     if(expected!==0&&Math.abs(expected)>Math.abs(f.rule.tolerance||0)&&!oppositeIsAccepted)assert.equal(c.AnswerChecker.check(rule,String(-expected)).status,'incorrect',q.id+' wrong sign');
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
 fs.writeFileSync(path.join(__dirname,'runtime-audit-25-30.json'),JSON.stringify({totals,failures},null,2)+'\n');
 assert.equal(failures.length,0,JSON.stringify(failures.slice(0,8)));
 for(const [ch,total] of [[25,91],[26,96],[27,118],[28,104],[29,99],[30,113]])assert.equal(totals[ch].questions,total,'chapter '+ch+' coverage');
 console.log('PASS actual practice pipeline: '+JSON.stringify(totals));
})().catch(e=>{console.error(e);process.exitCode=1});
