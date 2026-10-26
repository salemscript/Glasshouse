const fs=require('fs'),vm=require('vm'),zlib=require('zlib'),assert=require('assert/strict');
const window={};vm.runInNewContext(fs.readFileSync('site/source-excerpts.js','utf8'),{window});const S=window.SourceExcerpts;
const touching=[[57,358.742,274,30.665989501953106],[57,389.4079895019531,154.40199279785156,6.281010498046896]];
assert.equal(S.groups(touching).length,1,'Chapter 16 exercise 3 must retain a complete last line');
assert.equal(S.groups([[0,0,10,10],[0,30,10,10]]).length,2,'Do not expose the gap between excerpts');
assert.equal(S.groups([[0,0,10,10],[0,20,10,10],[0,10,10,10]]).length,1,'Merge a bridging crop');
assert.equal(S.groups([[0,0,NaN,10]]).length,0);
let parts=0,joined=0,questions=0;const perBook={};
for(const book of ['physics','calculus','chemistry','organic']){
 const file='site/questions/'+book+'.json.gz';if(!fs.existsSync(file))continue;
 let affected=0;
 for(const q of JSON.parse(zlib.gunzipSync(fs.readFileSync(file)))){
  let changed=false;
  for(const p of q.parts||[]){if(!p.crops?.length)continue;parts++;const g=S.groups(p.crops);assert.equal(g.flat().length,p.crops.length,q.id);assert.equal(JSON.stringify(g.flat().slice().sort()),JSON.stringify(p.crops.slice().sort()),q.id+' crop coordinates changed');if(g.length<p.crops.length){joined++;changed=true;}}
  if(changed){questions++;affected++;}
 }perBook[book]=affected;
}
const source='<svg viewBox="0 0 600 800" role="group" aria-label="Page"><defs><style>font-face</style></defs><text>unchanged x² + y</text></svg>';
const out=S.render(source,touching,'Exercise "3"');assert.equal((out.match(/<svg /g)||[]).length,1);assert(out.includes('unchanged x² + y'));assert(out.includes('Exercise &quot;3&quot;'));assert.equal((out.match(/<rect /g)||[]).length,2);assert(out.includes('clipPathUnits="userSpaceOnUse"'));assert(!/NaN|undefined/.test(out));
const again=S.render(source,touching,'Exercise 3');assert.notEqual(out.match(/source-excerpt-clip-\d+/)[0],again.match(/source-excerpt-clip-\d+/)[0],'Unique clip IDs');
console.log(JSON.stringify({passed:true,partsChecked:parts,connectedPartsRepaired:joined,questionsWithConnectedCrops:questions,perBook},null,2));
