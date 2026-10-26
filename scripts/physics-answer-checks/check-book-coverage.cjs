/* Audit availability through the real physics practice pipeline, without changing records. */
const fs=require('fs'),path=require('path'),vm=require('vm'),zlib=require('zlib'),assert=require('assert');
const site=path.resolve(__dirname,'../../site');
const all=JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(site,'questions/physics.json.gz'))));
const c={console,TextDecoder,TextEncoder,Response,Blob,DecompressionStream,URL,Set,Map,Math,Number,JSON,Date,setTimeout,clearTimeout,document:{addEventListener(){},querySelector(){return null},querySelectorAll(){return[]}},localStorage:{getItem(){return null},setItem(){}},fetch:async url=>new Response(fs.readFileSync(path.join(site,url)))};
c.window=c;vm.createContext(c);
for(const file of ['solution-math.js','study-data.js','concept-choice-data.js','answer-checker.js','response-parts.js','concept-choices.js','problem-content.js','help-tutor.js','hint-journey.js','answer-library.js','textbook-practice.js'])vm.runInContext(fs.readFileSync(path.join(site,file),'utf8'),c,{filename:file});
(async()=>{
 const baseline=process.argv.includes('--through-37'),questions=all.filter(q=>!baseline||q.chapter<=37),chapters={},issues=[];
 for(const original of questions){
  const q=(await c.TextbookPractice.context('physics',original.id)).question,fields=c.ResponseParts.fields(q);
  const row=chapters[q.chapter]??={questions:0,checkable:0,fields:0,types:{}};row.questions++;
  const errors=[];if(!fields.length)errors.push('no answer fields');
  for(const f of fields){
   const rule=c.ConceptChoices.responseRule(f.rule,q,f.graderIndex)||f.rule;
   if(!rule||!['numeric','choice'].includes(rule.type))errors.push('unsupported response '+f.label);
   else if(c.AnswerChecker.check(rule,String(rule.answer)).status!=='correct')errors.push('reference response fails '+f.label);
   if(rule){row.types[rule.type]=(row.types[rule.type]||0)+1;row.fields++;}
  }
  if(q.grader?.complete===false)errors.push('explicitly incomplete grader');
  if(errors.length)issues.push({id:q.id,errors});else row.checkable++;
 }
 const report={scope:baseline?'Chapters1–37 baseline':'All44physicschapters',questions:questions.length,checkable:questions.length-issues.length,chapters,issues};
 if(!baseline)fs.writeFileSync(path.join(__dirname,'whole-book-coverage.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({scope:report.scope,questions:report.questions,checkable:report.checkable,issues:issues.slice(0,15)}));
 assert.equal(issues.length,0,'physics availability audit has unresolved fields');
 if(!baseline)assert.equal(questions.length,4695,'complete physics inventory');
})().catch(e=>{console.error(e);process.exitCode=1});
