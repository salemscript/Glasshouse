const assert=require('assert'),C=require('../../site/circuit-solver.js');let checks=0;
function near(a,b,tol=1e-8){assert(Number.isFinite(a)&&Math.abs(a-b)<=tol*Math.max(1,Math.abs(b)),`${a} versus ${b}`);checks++;}
function solved(s){const r=C.solve(s);assert(r.valid);assert(r.islands.every(i=>i.consistent));checks++;return r;}
function balance(s,r){if(r.powerBalance!==null)near(r.powerBalance,0);const sums={};for(const e of s.elements.filter(e=>e.type!=='wire')){const b=r.branches[e.id];if(b.current===null)return;const a=r.net(e.a),n=r.net(e.b);sums[a]=(sums[a]||0)+b.current;sums[n]=(sums[n]||0)-b.current;}Object.values(sums).forEach(v=>near(v,0));}
let s=C.preset('divider'),r=solved(s);near(r.measure(s.positive,s.negative).value,6);near(r.branches.R1.current,.03);near(r.branches.R2.current,.03);near(r.branches.V1.current,-.03);near(r.resistorPower,.27);balance(s,r);
s.elements.find(e=>e.id==='V1').value=18;r=solved(s);near(r.measure(s.positive,s.negative).value,12);near(r.branches.R1.current,.06);near(r.resistorPower,1.08);
s.elements.find(e=>e.id==='V1').value=-12;r=solved(s);near(r.measure(s.positive,s.negative).value,-8);near(r.branches.R1.current,-.04);near(r.measure(s.negative,s.positive).value,8);balance(s,r);
s=C.preset('parallel');r=solved(s);near(r.branches.R1.current,.09);near(r.branches.R2.current,.045);near(r.branches.V1.current,-.135);balance(s,r);
s=C.preset('bridge');r=solved(s);near(r.measure(s.positive,s.negative).value,0);near(r.branches.R5.current,0);s.elements.find(e=>e.id==='R1').value=200;r=solved(s);near(r.measure(s.positive,s.negative).value,-27/38);balance(s,r);
s=C.preset('divider');s.ground=C.node(0,0);r=solved(s);near(r.measure(s.positive,s.negative).value,6);assert(r.nodes[s.positive].potential===null);assert(r.measure(s.positive,s.ground).value===null);checks+=2;near(r.branches.R1.current,.03);
s.ground=s.positive;r=solved(s);near(r.nodes[s.positive].potential,0);near(r.nodes[s.negative].potential,-6);near(r.measure(s.positive,s.negative).value,6);near(r.branches.R1.current,.03);
s=C.preset('divider');s.elements=s.elements.filter(e=>e.id!=='W2');r=solved(s);near(r.branches.R1.current,0);near(r.branches.R2.current,0);near(r.measure(s.positive,s.negative).value,0);
s=C.preset('divider');s.elements=s.elements.filter(e=>e.type!=='wire');r=solved(s);assert.equal(r.measure(s.positive,s.negative).value,null);checks++;
const N=C.node,el=(type,id,a,b,value)=>({type,id,a:N(...a),b:N(...b),...(value===undefined?{}:{value})});
function twoSources(v2){return{version:1,ground:N(1,2),positive:N(6,1),negative:N(1,2),elements:[el('voltage','V1',[1,1],[1,2],9),el('voltage','V2',[4,1],[4,2],v2),el('resistor','R1',[6,1],[6,2],100),el('wire','W1',[1,1],[6,1]),el('wire','W2',[1,2],[6,2])]};}
s=twoSources(9);r=solved(s);near(r.measure(s.positive,s.negative).value,9);near(r.branches.R1.current,.09);assert.equal(r.branches.V1.current,null);assert.equal(r.branches.V2.current,null);assert(r.islands.some(i=>i.underdetermined));checks+=3;
s=twoSources(12);r=C.solve(s);assert(r.valid);assert(r.islands.some(i=>!i.consistent));assert.equal(r.measure(s.positive,s.negative).value,null);checks+=3;
s={ground:N(1,2),positive:N(1,1),negative:N(1,2),elements:[el('voltage','V1',[1,1],[1,2],9),el('wire','W1',[1,1],[2,1]),el('wire','W2',[2,1],[2,2]),el('wire','W3',[2,2],[1,2])]};
r=C.solve(s);assert(r.valid&&!r.islands[0].consistent);assert.equal(r.measure(s.positive,s.negative).value,null);checks+=2;
s.elements[0].value=0;r=solved(s);near(r.measure(s.positive,s.negative).value,0);assert.equal(r.branches.V1.current,null);checks++;
s={ground:N(2,2),positive:N(2,1),negative:N(2,2),elements:[el('current','I1',[2,1],[2,2],.02),el('resistor','R1',[4,1],[4,2],100),el('wire','W1',[2,1],[4,1]),el('wire','W2',[2,2],[4,2])]};
r=solved(s);near(r.measure(s.positive,s.negative).value,-2);near(r.branches.R1.current,-.02);near(r.branches.I1.current,.02);near(r.branches.I1.power,-.04);balance(s,r);
s.elements=s.elements.filter(e=>e.type==='current');r=C.solve(s);assert(r.valid&&r.islands.some(i=>!i.consistent));assert.equal(r.measure(s.positive,s.negative).value,null);checks+=2;
s.elements[0].value=0;r=solved(s);assert.equal(r.measure(s.positive,s.negative).value,null);near(r.measure(s.positive,s.positive).value,0);checks++;
for(let i=0;i<80;i++){
 s=C.preset('divider');const R1=10**((i*7%61)/10),R2=10**((i*13%61)/10),V=(i%49)-24;
 s.elements.find(e=>e.id==='R1').value=R1;s.elements.find(e=>e.id==='R2').value=R2;s.elements.find(e=>e.id==='V1').value=V;
 r=solved(s);near(r.measure(s.positive,s.negative).value,V*R2/(R1+R2));near(r.branches.R1.current,V/(R1+R2));near(r.branches.R2.current,V/(R1+R2));balance(s,r);
}
// Independent two-node bridge solution by Cramer's rule, not the MNA implementation.
for(let i=0;i<30;i++){
 s=C.preset('bridge');const vals=[31+11*i,41+7*i,71+5*i,89+3*i,53+13*i];vals.forEach((v,j)=>s.elements.find(e=>e.id==='R'+(j+1)).value=v);r=solved(s);
 const [r1,r2,r3,r4,r5]=vals,A=1/r1+1/r2+1/r5,B=-1/r5,D=1/r3+1/r4+1/r5,p=9/r1,q=9/r3,det=A*D-B*B;
 const l=(p*D-B*q)/det,rr=(A*q-B*p)/det;near(r.measure(s.positive,s.negative).value,l-rr);near(r.branches.R5.current,(l-rr)/r5);balance(s,r);
}
assert(!C.validate({ground:0,elements:[el('resistor','R1',[1,1],[3,1],100)]}).valid);checks++;
assert(!C.validate({ground:0,elements:[el('resistor','R1',[1,1],[2,1],0)]}).valid);checks++;
assert(!C.validate({ground:0,elements:[el('wire','W1',[1,1],[2,1]),el('resistor','R1',[1,1],[2,1],100)]}).valid);checks++;
assert(!C.validate({ground:0,elements:[el('voltage','V1',[1,1],[1,2],NaN)]}).valid);checks++;
for(const p of ['blank','divider','series','parallel','bridge'])assert(C.validate(C.preset(p)).valid);checks+=5;
console.log(`PASS: ${checks} solver assertions: analytic series/parallel/bridge results, KCL, energy, scaling, polarity, floating networks, open paths, current sources, ideal-source conflicts and underdetermined currents.`);
