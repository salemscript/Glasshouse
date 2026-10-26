/* Recreate source-only chapter inventories for the exact-math verification scripts. */
const fs=require('fs'),vm=require('vm'),path=require('path');
process.chdir(path.resolve(__dirname,'../..'));
const c={console};c.window=c;vm.createContext(c);
for(const name of ['book-data.js','study-data.js','math-course-data.js','math-courses.js','linear-section-data.js','linear-review-data.js','math-workspace.js'])vm.runInContext(fs.readFileSync('site/'+name,'utf8'),c,{filename:name});
const questions=c.MathWorkspace.questions();
if(questions.length!==755)throw Error('Source question inventory changed');
fs.mkdirSync('tmp',{recursive:true});
for(let ch=1;ch<=9;ch++)fs.writeFileSync(`tmp/linear-ch${ch}-input.json`,JSON.stringify(questions.filter(q=>q.chapter===ch),null,2)+'\n');
console.log('Prepared source inventories for all 755 questions.');
