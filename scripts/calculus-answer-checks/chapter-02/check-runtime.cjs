'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const path=require('path'),root=path.resolve(__dirname,'../../..');
const sandbox={window:{}};vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(path.join(root,'site/answer-checker.js'),'utf8'),sandbox);
const checker=sandbox.window.AnswerChecker;
const rows=JSON.parse(fs.readFileSync(path.join(root,'scripts/calculus-answer-checks/chapter-02.json'),'utf8')).questions;
let fields=0,correct=0,wrong=0,invalid=0;
for(const[id,row] of Object.entries(rows)){
 const g=row.grader,ff=g.type==='parts'?g.parts:[g];
 for(const f of ff){
  fields++;
  assert.equal(checker.check(f,String(f.answer)).status,'correct',`${id}: correct ${f.label}`);correct++;
  assert.equal(checker.check(f,'').status,'invalid',`${id}: blank ${f.label}`);invalid++;
  if(f.type==='choice'){
   for(const option of f.options.filter(x=>x!==f.answer)){
    assert.equal(checker.check(f,option).status,'incorrect',`${id}: wrong ${f.label}`);wrong++;
   }
   assert.equal(checker.check(f,'This is not a listed choice').status,'invalid');invalid++;
  }else{
   const delta=Math.max(1,Math.abs(f.answer)*.1,(f.tolerance||0)*3);
   assert.equal(checker.check(f,String(f.answer+delta)).status,'incorrect',`${id}: wrong number ${f.label}`);wrong++;
   assert.equal(checker.check(f,'not a number').status,'invalid');invalid++;
  }
 }
}
console.log(JSON.stringify({questions:Object.keys(rows).length,fields,correct,wrong,invalid}));
