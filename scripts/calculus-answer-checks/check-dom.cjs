/* Optional development-only UI test: NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node this-file. */
const {parseHTML}=require('linkedom'),fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),zlib=require('zlib');
const site=path.resolve(__dirname,'../../site')+'/',{document,Event}=parseHTML('<html><body></body></html>');
const storage=new Map(),c={console,document,Event,TextDecoder,TextEncoder,Response,Blob,DecompressionStream,URL,setTimeout,clearTimeout,location:{hash:''},history:[],record(){},matchMedia:()=>({matches:true}),title:()=>'',Study:{tabs:()=>''},DiagramInput:{unmount(){}},ProblemVisuals:{stop(){}},Bank:{data:()=>[]},ExerciseFeedback:{answer(){},reset(){}},localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},fetch:async url=>new Response(fs.readFileSync(site+url))};
c.window=c;vm.createContext(c);
for(const f of ['study-data.js','concept-choice-data.js','answer-checker.js','response-parts.js','concept-choices.js','problem-content.js','help-tutor.js','hint-journey.js','answer-library.js','textbook-practice.js'])vm.runInContext(fs.readFileSync(site+f,'utf8'),c,{filename:f});
const data=name=>JSON.parse(zlib.gunzipSync(fs.readFileSync(site+'questions/'+name)));
const selected=process.argv.slice(2);
assert(selected.length<=1&&(!selected.length||/^--chapter=([1-9]|1[0-7]|appendix|diagnostic)$/.test(selected[0])),'Use --chapter=1 through17, appendix or diagnostic; no flag tests all records.');
const chapters=selected.length?[(/^[0-9]+$/.test(selected[0].split('=')[1])?Number(selected[0].split('=')[1]):selected[0].split('=')[1])]:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,'appendix','diagnostic'];
const raw=data('calculus.json.gz').filter(q=>chapters.includes(q.chapter));
const click=el=>{assert(el,'missing button');el.dispatchEvent(new Event('click',{bubbles:true}));};
(async()=>{
 const first=raw[0].id,key='calx-question-v1-calculus-'+first;
 storage.set(key,JSON.stringify({checked:true,working:'Keep these notes',answers:{0:'previous written response'},guidance:{0:{finished:true}}}));
 c.TextbookPractice.configure('calculus',first);document.body.innerHTML=c.TextbookPractice.html('calculus');
 for(let i=0;i<200&&!document.querySelector('#question-check');i++)await new Promise(r=>setTimeout(r,20));
 assert(document.querySelector('#question-check'),'practice failed to load');
 const migrated=JSON.parse(storage.get(key));assert.equal(migrated.checked,false);assert.equal(migrated.working,'Keep these notes');assert.equal(migrated.objectiveCheckVersion,data('answer-library-calculus.json.gz').questions[first].objectiveCheckVersion);
 const totals={};
 for(const original of raw){
  const navigation=document.createElement('button');navigation.dataset.questionId=original.id;document.body.appendChild(navigation);click(navigation);navigation.remove();
  assert.equal(c.TextbookPractice.state().selected,original.id);
  const q=(await c.TextbookPractice.context('calculus',original.id)).question;
  const fields=c.ResponseParts.fields(q),all=document.querySelector('#question-check');assert(!all.disabled,original.id+' check disabled');
  assert(!document.querySelector('.question-format-pending'),original.id+' ungraded field');
  // Remove any migrated or restored values before the blank submission.
  for(const input of document.querySelectorAll('[data-question-answer]'))input.value='';
  click(all);assert(document.querySelector('#question-feedback .error'),original.id+' blank feedback');
  const row=totals[q.chapter]??={questions:0,inputs:0,partButtons:0,limited:0};row.questions++;
  for(const f of fields){
   const input=document.querySelector('#question-answer-'+f.fieldKey);assert(input,original.id+' input');
   if(f.rule.type==='choice'){
    const option=[...document.querySelectorAll('[data-choice-field]')].find(e=>e.dataset.choiceField===f.fieldKey&&e.value===f.rule.answer);assert(option,original.id+' correct radio');option.checked=true;option.dispatchEvent(new Event('change',{bubbles:true}));assert.equal(input.value,f.rule.answer);
   }else{input.value=String(f.rule.answer);input.dispatchEvent(new Event('input',{bubbles:true}));}
   if(fields.length>1){click(document.querySelector('[data-check-part="'+f.fieldKey+'"]'));assert(document.querySelector('#question-result-'+f.fieldKey).classList.contains('correct'),original.id+' part feedback');row.partButtons++;}
   row.inputs++;
  }
  click(all);assert(document.querySelector('#question-feedback .success'),original.id+' correct feedback');
  if(q.grader.complete===false){assert(!JSON.parse(storage.get('calx-question-v1-calculus-'+q.id)).checked,original.id+' limited exercise marked complete');row.limited++;}
  const f=fields[0];document.querySelector('#question-answer-'+f.fieldKey).value=f.rule.type==='choice'?f.rule.options.find(o=>o!==f.rule.answer):String(f.rule.answer+Math.max(1,Math.abs(f.rule.answer)*.1,(f.rule.tolerance||0)*10,(f.rule.relativeTolerance||0)*Math.abs(f.rule.answer)*10));
  click(all);assert(document.querySelector('#question-feedback .error'),original.id+' wrong feedback');
 }
 assert.equal(raw.length,chapters.reduce((sum,ch)=>sum+({1:368,2:570,3:844,4:785,5:486,6:307,7:647,8:239,9:238,10:455,11:751,12:449,13:286,14:646,15:490,16:436,17:123,appendix:371,diagnostic:31}[ch]),0));
 const auditName=chapters.length===19?'dom-audit.json':'dom-audit-chapter-'+chapters[0]+'.json';
 fs.writeFileSync(path.join(__dirname,auditName),JSON.stringify({totals,checks:['actual delegated input/radio events','blank/incorrect/correct feedback','individual part controls','saved note migration','scope-limited completion restrictions']},null,2)+'\n');
 console.log('PASS actual UI events: '+JSON.stringify(totals));
})().catch(e=>{console.error(e);process.exitCode=1});
