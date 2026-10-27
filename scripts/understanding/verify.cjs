/* Exercise every concept answer through the actual Study event handlers. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const handlers={},storage=new Map(),c={window:null,current:'calculus',page:'calculus',render(){},title(){return ''},ExerciseFeedback:{icon(){return ''}},Exercises:{mode(){return 'understand'}},document:{addEventListener(type,fn){(handlers[type]??=[]).push(fn)},querySelector(){return null},querySelectorAll(){return []}},GlasshouseStorage:{getItem(k){return storage.get(k)||null},setItem(k,v){storage.set(k,v)}},history:{replaceState(){}},TEXTBOOKS:[{id:'calculus',groups:[]}],MathCourseData:{linearAlgebra:[]},console};c.window=c;vm.createContext(c);
for(const f of ['study-data.js','math-workspace.js','organic-study.js','understanding-extra.js','understanding-chapters.js','study.js'])vm.runInContext(fs.readFileSync('site/'+f,'utf8'),c,{filename:f});
function choose(i){for(const fn of handlers.change)fn({target:{name:'concept-answer',value:String(i),closest(){return {classList:{add(){}}}}}})}
function click(button){for(const fn of handlers.click)fn({target:{closest(){return {dataset:{},...button}}}})}
const saved=()=>JSON.parse(storage.get('foundry-understanding-v1')||'{}');let checked=0,chapters=0;const result={};
for(const b of ['calculus','physics','chemistry','organic','linear-algebra','differential-equations']){
 c.current=b;result[b]={};
 for(const base of c.Study.rows(b)){
  const ch=base[0],qs=c.Study.chapterQuestions(b,ch);assert(qs.length>=10,b+' '+ch);chapters++;c.Study.configure(b,ch,'understand');
  assert(new Set(qs.map(q=>q[2])).size===qs.length,'duplicate prompt');
  const keys=[];
  for(let index=0;index<qs.length;index++){
   const q=qs[index];assert(q[3].length>=2&&q[3].length<=4);assert(new Set(q[3]).size===q[3].length);assert(Number.isInteger(q[4])&&q[4]>=0&&q[4]<q[3].length);assert(q[5].length>25);
   assert(c.Study.html().includes('Question '+(index+1)+' of '+qs.length),'visible chapter index');
   const canonical=b==='differential-equations'?'calculus':b,key=canonical+'-'+ch+(q[10]?':concept:'+q[10]:q[9]?':extra-'+q[9]:'');keys.push(key);
   const before=JSON.stringify(saved());choose((q[4]+1)%q[3].length);click({id:'concept-check'});assert.equal(JSON.stringify(saved()),before,'wrong answer changed completion');
   choose(q[4]);click({id:'concept-check'});assert.equal(saved()[key],true,'correct answer not saved');checked++;
   if(index<qs.length-1)click({dataset:{conceptStep:'1'}});
  }
  assert.equal(new Set(keys).size,keys.length,'completion-key collision');result[b][ch]=qs.length;
 }
}
const summary={chapters,answerFlowsChecked:checked,minimumQuestionsPerChapter:Math.min(...Object.values(result).flatMap(Object.values)),subjects:Object.fromEntries(Object.entries(result).map(([b,cs])=>[b,{chapters:Object.keys(cs).length,questions:Object.values(cs).reduce((a,b)=>a+b,0)}]))};
fs.writeFileSync('scripts/understanding/verification.json',JSON.stringify(summary,null,2)+'\n');console.log(JSON.stringify(summary,null,2));
