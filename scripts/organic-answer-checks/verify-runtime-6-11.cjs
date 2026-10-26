const fs=require('fs'),vm=require('vm'),zlib=require('zlib'),path=require('path');const site=path.resolve('site');
const c={console,TextDecoder,TextEncoder,Response,Blob,DecompressionStream,URL,Set,Map,Math,Number,JSON,Date,setTimeout,clearTimeout,document:{addEventListener(){},querySelector(){return null},querySelectorAll(){return[]}},localStorage:{getItem(){return null},setItem(){}},fetch:async url=>{let p=path.join(site,url);return fs.existsSync(p)?new Response(fs.readFileSync(p)):new Response('',{status:404})}};c.window=c;vm.createContext(c);
for(const file of ['book-data.js','solution-math.js','study-data.js','concept-choice-data.js','answer-checker.js','response-parts.js','concept-choices.js','problem-content.js','help-tutor.js','hint-journey.js','answer-library.js','math-course-data.js','math-courses.js','linear-section-data.js','linear-review-data.js','math-workspace.js','textbook-practice.js']){let s=fs.readFileSync(path.join(site,file),'utf8');if(file==='textbook-practice.js')s=s.replace('return {html,configure,check,context,sourceSVG,state:', 'return {audit:{enrich,rules,loadPacks},html,configure,check,context,sourceSVG,state:');vm.runInContext(s,c,{filename:file});}
(async()=>{
 await c.HelpTutor.load(); await c.TextbookPractice.audit.loadPacks(); await c.AnswerLibrary.load('organic');
 const raw=JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(site,'questions/organic.json.gz'))));
 const chemicalHTML=c.ConceptChoices.field({fieldKey:'test',type:'choice',label:'Stereochemistry',selectionPrompt:'Compare R/S',answer:'R/S',options:['R/S','A < B'],displayFormat:'chemical-text'},'');
 if(chemicalHTML.includes('<math')||!chemicalHTML.includes('R/S')||!chemicalHTML.includes('A &lt; B'))throw Error('Chemical notation rendered as mathematics or unescaped HTML');
 const fractionHTML=c.ConceptChoices.field({fieldKey:'test',type:'choice',label:'Fraction',answer:'1/2',options:['1/2','1/3']},'');
 if(!fractionHTML.includes('mfrac'))throw Error('Existing math fraction rendering changed');
 const audit=[];let checks=0;
 for(const source of raw.filter(q=>q.chapter>=6&&q.chapter<=11)){
  const q=c.TextbookPractice.audit.enrich(source),rs=c.TextbookPractice.audit.rules(q);
  if(!rs.length||rs.some(r=>!r.checkable))throw Error(q.id+' unavailable field');
  for(const r of rs){
   const rule=r.rule||r;
   if(c.AnswerChecker.check(rule,String(rule.answer)).status!=='correct')throw Error(q.id+' correct rejected '+JSON.stringify(r));
   if(c.AnswerChecker.check(rule,'').status!=='invalid')throw Error(q.id+' blank accepted');
   const wrong=rule.type==='choice'?rule.options.filter(x=>x!==rule.answer):[Number(rule.answer)+Math.max(1,Math.abs(Number(rule.answer)))*100];
   for(const value of wrong)if(c.AnswerChecker.check(rule,String(value)).status==='correct')throw Error(q.id+' wrong accepted '+value);
   checks++;
  }
  audit.push({id:q.id,chapter:q.chapter,fields:rs.length,freehandOrSourceScopeLimited:q.grader.complete===false,scope:q.grader.scope||'All exposed answer fields checked.'});
 }
 const tiny=c.AnswerLibrary.lookup('organic','organic-2-49').grader.parts[0];
 if(c.AnswerChecker.check(tiny,'0').status==='correct')throw Error('Tiny Ka accepts zero');
 const report={date:'2026-10-26',questions:audit.length,fields:checks,missingQuestions:0,missingFields:0,chapters:[6,7,8,9,10,11].map(ch=>({chapter:ch,questions:audit.filter(x=>x.chapter===ch).length,scopeLimited:audit.filter(x=>x.chapter===ch&&x.freehandOrSourceScopeLimited).length})),records:audit};
 fs.writeFileSync('scripts/organic-answer-checks/runtime-audit-6-11.json',JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({...report,records:undefined},null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
