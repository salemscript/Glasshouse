const fs=require('fs'),path=require('path'),assert=require('assert');
const katex=require('../../site/vendor/katex/katex.min.js');
let strings=0,expressions=0;const errors=[];
function visit(value,where){
 if(Array.isArray(value)){value.forEach((v,i)=>visit(v,where+'['+i+']'));return;}
 if(value&&typeof value==='object'){for(const [k,v] of Object.entries(value))visit(v,where+'.'+k);return;}
 if(typeof value!=='string')return;strings++;
 const remainder=value.replace(/\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g,(raw,inline,display)=>{
  try{katex.renderToString(inline??display,{throwOnError:true,trust:false,strict:'ignore',displayMode:display!==undefined});expressions++;}
  catch(e){errors.push(where+': '+e.message);}
  return '';
 });
 if(/\\[()[\]]/.test(remainder))errors.push(where+': unpaired math delimiter '+remainder);
}
for(const file of fs.readdirSync(__dirname).filter(f=>/^ch\d+-reviewed\.json$/.test(f)))visit(JSON.parse(fs.readFileSync(path.join(__dirname,file))),file);
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}else console.log(`Typesetting: ${expressions} mathematical expressions validated in ${strings} strings.`);
assert(katex.renderToString('\\frac{1}{2}').includes('mfrac'));
assert(katex.renderToString('\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}').includes('mtable'));
