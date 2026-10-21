/* Optional integration check: NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node this-file. */
const {parseHTML}=require('linkedom'),fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),zlib=require('zlib');
const site=path.resolve(__dirname,'../../site')+'/',{document,Event}=parseHTML('<html><body></body></html>');
const storage=new Map(),c={console,document,Event,TextDecoder,TextEncoder,Response,Blob,DecompressionStream,URL,setTimeout,clearTimeout,location:{hash:''},history:[],record(){},matchMedia:()=>({matches:true}),title:()=>'',Study:{tabs:()=>''},DiagramInput:{unmount(){}},ProblemVisuals:{stop(){}},Bank:{data:()=>[]},ExerciseFeedback:{answer(){},reset(){}},localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},fetch:async url=>new Response(fs.readFileSync(site+url))};
c.window=c;vm.createContext(c);
for(const f of ['study-data.js','concept-choice-data.js','answer-checker.js','response-parts.js','concept-choices.js','problem-content.js','help-tutor.js','hint-journey.js','answer-library.js','textbook-practice.js'])vm.runInContext(fs.readFileSync(site+f,'utf8'),c,{filename:f});
const data=name=>JSON.parse(zlib.gunzipSync(fs.readFileSync(site+'questions/'+name)));
const audit=data('answer-library-calculus.json.gz'),raw=data('calculus.json.gz').filter(q=>audit.questions[q.id]?.workedSolutionSource?.authoringFile==='scripts/calculus-expansion/author.py');
const click=el=>{assert(el,'missing button');el.dispatchEvent(new Event('click',{bubbles:true}));};
(async()=>{
 const first=raw[0].id,key='calx-question-v1-calculus-'+first;
 storage.set(key,JSON.stringify({checked:true,working:'Keep these notes',drawing:{saved:true},answers:{0:'old written answer'},guidance:{0:{finished:true}}}));
 c.TextbookPractice.configure('calculus',first);document.body.innerHTML=c.TextbookPractice.html('calculus');
 for(let i=0;i<200&&!document.querySelector('#question-check');i++)await new Promise(r=>setTimeout(r,20));
 assert(document.querySelector('#question-check'),'practice failed to load');
 const migrated=JSON.parse(storage.get(key));assert.equal(migrated.checked,false);assert.equal(migrated.working,'Keep these notes');assert(migrated.drawing.saved);assert.equal(migrated.objectiveCheckVersion,1);
 let count=0,parts=0,limited=0;
 for(const original of raw){
  const navigation=document.createElement('button');navigation.dataset.questionId=original.id;document.body.appendChild(navigation);click(navigation);navigation.remove();
  assert.equal(c.TextbookPractice.state().selected,original.id);
  const q=(await c.TextbookPractice.context('calculus',original.id)).question;
  const fields=c.ResponseParts.fields(q),all=document.querySelector('#question-check');assert(!all.disabled,original.id+' disabled');
  click(all);assert(document.querySelector('#question-feedback .error'),original.id+' blank');
  for(const f of fields){
   const input=document.querySelector('#question-answer-'+f.fieldKey);assert(input,original.id+' input');
   if(f.rule.type==='choice'){
    const option=[...document.querySelectorAll('[data-choice-field]')].find(e=>e.dataset.choiceField===f.fieldKey&&e.value===f.rule.answer);assert(option,original.id+' option');option.checked=true;option.dispatchEvent(new Event('change',{bubbles:true}));assert.equal(input.value,f.rule.answer);
   }else{input.value=String(f.rule.answer);input.dispatchEvent(new Event('input',{bubbles:true}));}
   if(fields.length>1){click(document.querySelector('[data-check-part="'+f.fieldKey+'"]'));assert(document.querySelector('#question-result-'+f.fieldKey).classList.contains('correct'));parts++;}
   count++;
  }
  click(all);assert(document.querySelector('#question-feedback .success'),original.id+' correct');
  if(q.grader.complete===false){assert(!JSON.parse(storage.get('calx-question-v1-calculus-'+q.id)).checked);limited++;}
  const f=fields[0];document.querySelector('#question-answer-'+f.fieldKey).value=f.rule.type==='choice'?f.rule.options.find(o=>o!==f.rule.answer):String(f.rule.answer+Math.max(1,Math.abs(f.rule.answer)*.1,(f.rule.tolerance||0)*10));
  click(all);assert(document.querySelector('#question-feedback .error'),original.id+' wrong');
  click(document.querySelector('#question-worked-solution'));assert(!document.querySelector('#question-help').hidden);assert(document.querySelector('#question-help').textContent.includes('Final answer'));assert(JSON.parse(storage.get('calx-question-v1-calculus-'+q.id)).assisted);
 }
 assert.equal(raw.length,128);assert.equal(count,164);
 console.log(`PASS DOM: ${raw.length} exercises, ${count} inputs, ${parts} part buttons, wrong/blank/correct results, solutions, saved notes migration and ${limited} scope-limited exercises.`);
})().catch(e=>{console.error(e);process.exitCode=1});
