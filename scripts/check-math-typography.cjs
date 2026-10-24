/* Presentation regression checks. Run with Linkedom in NODE_PATH. */
const assert=require('node:assert/strict'),fs=require('node:fs'),z=require('node:zlib');
const {parseHTML}=require('linkedom');require('../site/solution-math.js');
const doc=s=>parseHTML('<html><body>'+SolutionMath.render(s)+'</body></html>').document;
const frac=s=>{const d=doc(s),f=d.querySelector('mfrac');assert(f,s+' lacks stacked fraction');for(const n of d.querySelectorAll('mfrac'))assert.equal(n.children.length,2,s+' fraction must have exactly two operands');return d;};
for(const s of ['1/2','(a+b)/(c-d)','1/(1+1/x)','x^(-1/2)','sqrt(1/2)','dy/dx','⟨8,9⟩/√145','xₙ₊₁=(xₙ+a/xₙ)/2','Σ_(n=0)^∞ x^n/n!','∫ 1/x dx','m/s²','m/s^2','The slope is 1/2, with x>0.','−π/4≤θ≤π/4 (one loop)','(Big circle(−4√2/3,2/3), small circle(−2√2/3,10/3)) + 1','sin(x)^2/3','E=|kqz|/(z²+R²)^(3/2)'])frac(s);
assert(doc('sqrt(x)^2').querySelector('msup > msqrt'),'square applies outside radical');
assert(!doc('sqrt(x)^2').querySelector('msqrt msup'),'square must not move inside radical');
assert.equal(doc('sqrt(x)^2').querySelector('msqrt').textContent,'x');
assert(doc('x^-2').querySelector('msup').lastElementChild.textContent==='−2');
assert.equal(frac('m/s^2').querySelector('mfrac').lastElementChild.localName,'msup');
const integral=frac('∫ 1/x dx');assert.equal(integral.querySelector('mfrac').textContent,'1x');assert(!integral.querySelector('mfrac').textContent.includes('∫'));
const sum=frac('Σ_(n=0)^∞ x^n/n!');assert.equal(sum.querySelector('munderover').firstElementChild.textContent,'∑');assert(!sum.querySelector('mfrac').querySelector('munderover'));
for(const s of ['https://example.com/a/b','left/right','wet/icy','<img src=x onerror=alert(1)>']){const d=doc(s);assert(!d.querySelector('img,script'));for(const n of d.querySelectorAll('annotation'))n.remove();assert.equal(d.body.textContent,s);}
assert.equal(doc('The slope is 1/2.').querySelector('annotation').textContent,'1/2');
let count=0,fractions=0,unformatted=[];
for(const book of ['calculus','physics']){const data=JSON.parse(z.gunzipSync(fs.readFileSync(__dirname+'/../site/questions/answer-library-'+book+'.json.gz')));for(const [id,q] of Object.entries(data.questions))for(const f of q.grader?.parts||[q.grader])for(const s of f?.options||[]){if(!s.includes('/'))continue;const d=doc(s);count++;for(const n of d.querySelectorAll('mfrac')){assert.equal(n.children.length,2,id);fractions++;}for(const n of d.querySelectorAll('annotation'))n.remove();if(d.body.textContent.includes('/'))unformatted.push({id,source:s,visibleText:d.body.textContent});}}
const proseSlashes=new Set('overnight/daytime domains/ranges left/up right/up right/down horizontal/vertical zeros/signs derivative/real-domain demographic/health zeros/undefined reciprocal/cyclic local/global birth/death power/division input/output zoom/sample vanishing-increment/secant corner/cusp vertical/horizontal before/after inconclusive/undefined differentiability/nonzero zero/near-zero cycles/divergence left/right temperature/density infinite/divergent speeds/forward cusp/vertical-tangent ratio/root scalar/vector shorter/bluer longer/redder size/shape radial/azimuth axial/circular hills/negative manufacturing/handling slopes/rates seat/contact wet/icy α/torque'.split(' '));
for(const row of unformatted){const remaining=row.visibleText.replace(/[A-Za-zα-ω-]+\s*\/\s*[A-Za-zα-ω-]+/g,pair=>proseSlashes.has(pair.toLowerCase().replace(/\s/g,''))?'':pair);assert(!remaining.includes('/'),row.id+' still has a mathematical slash: '+row.source);}
const summary={slashContainingChoices:count,stackedFractions:fractions,proseSlashChoices:unformatted.length,unformattedMathematicalChoices:0,reviewedProseSlashPairs:[...proseSlashes],checks:['two operands per fraction','root and exponent scope','integral differential scope','summation bounds','compound units','safe escaped text','all calculus and physics slash-containing choices']};
fs.writeFileSync(__dirname+'/math-typography-audit.json',JSON.stringify(summary,null,2)+'\n');
console.log('PASS typography: '+count+' choices, '+fractions+' fractions, no unformatted mathematical slashes; '+unformatted.length+' prose-only slash choices preserved.');
