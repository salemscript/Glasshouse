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
 // Independently recomputed physical constants and spectral unit conversions.
 const h=6.62607015e-34,light=299792458,NA=6.02214076e23;
 const expected={
  'organic-12-6':[h*light*NA/5e-11/1000,h*light*NA/3e-9/1000,h*6e15*NA/1000,h*7e14*NA/1000,h*light*NA/2e-5/1000,h*1e11*NA/1000],
  'organic-13-1':[h*187e6*NA/1000,h*200e6*NA/1000],
  'organic-13-2':[h*300e6*NA/1000],
  'organic-13-4':[1454/200,610/200,693/200,1060/200],
  'organic-13-5':[2.1*200,2.1,2.1*500],
  'organic-13-29':[436/200,956/200,1504/200],
  'organic-13-30':[2.1*300,3.45*300,6.3*300,7.7*300],
  'organic-13-31':[7.3,7.3*360,7.3],
  'organic-14-13':[h*light*NA/400e-9/1000,h*light*NA/200e-9/1000],
  'organic-14-14':[.735/50100], 'organic-14-60':[.065/11900]
 };
 for(const [id,values] of Object.entries(expected)){
  const fields=c.AnswerLibrary.lookup('organic',id).grader.parts;
  values.forEach((value,i)=>{
   if(c.AnswerChecker.check(fields[i],String(value)).status!=='correct')throw Error(id+' independent numeric result rejected');
   if(value!==0&&c.AnswerChecker.check(fields[i],'0').status==='correct')throw Error(id+' zero accepted for nonzero result');
  });
 }
 const audit=[];let checks=0;
 for(const source of raw.filter(q=>q.chapter>=12&&q.chapter<=14)){
  const q=c.TextbookPractice.audit.enrich(source),rs=c.TextbookPractice.audit.rules(q);
  if(!q.answerAudit?.objectiveChecksVerified)throw Error(q.id+' missing source review');
  if(!rs.length||rs.some(r=>!r.checkable))throw Error(q.id+' unavailable field');
  for(const r of rs){
   const rule=r.rule||r;
   if(rule.type==='choice'&&(!rule.options || rule.options.length<2 || new Set(rule.options).size!==rule.options.length))throw Error(q.id+' malformed choices');
   if(!rule.explanation)throw Error(q.id+' missing reasoning');
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
 const report={date:'2026-10-26',questions:audit.length,fields:checks,missingQuestions:0,missingFields:0,chapters:[12,13,14].map(ch=>({chapter:ch,questions:audit.filter(x=>x.chapter===ch).length,scopeLimited:audit.filter(x=>x.chapter===ch&&x.freehandOrSourceScopeLimited).length})),records:audit};
 fs.writeFileSync('scripts/organic-answer-checks/runtime-audit-12-14.json',JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({...report,records:undefined},null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
