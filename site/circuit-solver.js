/* Original DC modified nodal analysis. Ideal wires merge nodes; no artificial leakage/grounding. */
(function(root){
 'use strict';
 const COLS=9,ROWS=6,MAX_ELEMENTS=80,EPS=1e-10;
 const LIMITS={resistor:[1,1e6],voltage:[-24,24],current:[-1,1]};
 const validNode=n=>Number.isInteger(n)&&n>=0&&n<COLS*ROWS;
 const node=(column,row)=>row*COLS+column;
 const xy=n=>({column:n%COLS,row:Math.floor(n/COLS)});
 const label=n=>validNode(n)?String.fromCharCode(65+n%COLS)+(Math.floor(n/COLS)+1):'—';
 const adjacent=(a,b)=>validNode(a)&&validNode(b)&&Math.abs(a%COLS-b%COLS)+Math.abs(Math.floor(a/COLS)-Math.floor(b/COLS))===1;
 function wireNodes(a,b){
  if(!validNode(a)||!validNode(b))return[];
  const start=xy(a),end=xy(b),out=[a];let c=start.column,r=start.row;
  while(c!==end.column){c+=Math.sign(end.column-c);out.push(node(c,r));}
  while(r!==end.row){r+=Math.sign(end.row-r);out.push(node(c,r));}
  return out;
 }
 const edge=(a,b)=>Math.min(a,b)+':'+Math.max(a,b);
 const wireEdges=e=>wireNodes(e.a,e.b).slice(1).map((n,i)=>edge(wireNodes(e.a,e.b)[i],n));
 function validate(input){
  if(!input||!Array.isArray(input.elements)||input.elements.length>MAX_ELEMENTS)return{valid:false,message:'Use at most 80 circuit elements.'};
  const ids=new Set(),occupied=new Set(),wires=new Set();let sources=0;
  for(const e of input.elements){
   if(!e||!['wire','resistor','voltage','current'].includes(e.type)||typeof e.id!=='string'||!/^[A-Za-z][A-Za-z0-9_-]{0,23}$/.test(e.id)||ids.has(e.id)||!validNode(e.a)||!validNode(e.b)||e.a===e.b)return{valid:false,message:'Every element needs two distinct valid endpoints and a unique name.'};
   ids.add(e.id);
   if(e.type==='wire'){wireEdges(e).forEach(k=>wires.add(k));continue;}
   if(!adjacent(e.a,e.b))return{valid:false,message:'Place a component between two neighboring grid points. Wires can span several points.'};
   const k=edge(e.a,e.b);if(occupied.has(k))return{valid:false,message:'This edge already has a component. Build a separate branch for parallel components.'};occupied.add(k);
   const range=LIMITS[e.type];if(!Number.isFinite(e.value)||e.value<range[0]||e.value>range[1])return{valid:false,message:`${e.type} value is outside the supported range.`};
   if(e.type!=='resistor')sources++;
  }
  if(sources>8)return{valid:false,message:'Use at most eight independent sources.'};
  if([...occupied].some(k=>wires.has(k)))return{valid:false,message:'Erase the wire on this edge before inserting a component, or route a bypass on another row.'};
  if(!validNode(input.ground))return{valid:false,message:'Choose a valid ground point.'};
  return{valid:true};
 }
 // Rank-revealing elimination retains free-variable coefficients. Redundant ideal
 // sources can determine voltage while their individual currents stay unknown.
 function linear(A,b){
  const m=A.length,n=m?A[0].length:0;
  if(!n)return{consistent:b.every(v=>Math.abs(v)<EPS),forms:[],rank:0,free:[]};
  const M=A.map((row,i)=>{const scale=Math.max(...row.map(Math.abs));return[...row.map(v=>scale?v/scale:v),scale?b[i]/scale:b[i]];});
  const pivots=[];let r=0;
  for(let c=0;c<n&&r<m;c++){
   let p=r;for(let i=r+1;i<m;i++)if(Math.abs(M[i][c])>Math.abs(M[p][c]))p=i;
   if(Math.abs(M[p][c])<EPS)continue;
   [M[p],M[r]]=[M[r],M[p]];const d=M[r][c];for(let j=0;j<=n;j++)M[r][j]/=d;
   for(let i=0;i<m;i++)if(i!==r){const f=M[i][c];if(Math.abs(f)<EPS){M[i][c]=0;continue;}for(let j=0;j<=n;j++)M[i][j]-=f*M[r][j];}
   pivots.push(c);r++;
  }
  for(const row of M)if(row.slice(0,n).every(v=>Math.abs(v)<EPS)&&Math.abs(row[n])>1e-7)return{consistent:false,forms:[],rank:r,free:[]};
  const free=Array.from({length:n},(_,i)=>i).filter(i=>!pivots.includes(i));
  const forms=Array.from({length:n},()=>({value:0,coeff:Array(free.length).fill(0)}));
  free.forEach((c,j)=>forms[c].coeff[j]=1);
  pivots.forEach((c,i)=>{forms[c].value=M[i][n];free.forEach((f,j)=>forms[c].coeff[j]=-M[i][f]);});
  // Reject unreliable numeric results rather than display a fabricated answer.
  for(let i=0;i<m;i++){
   const residual=A[i].reduce((v,k,j)=>v+k*forms[j].value,0)-b[i];
   if(!Number.isFinite(residual)||Math.abs(residual)>1e-6*Math.max(1,Math.abs(b[i]),A[i].reduce((v,k,j)=>v+Math.abs(k*forms[j].value),0)))return{consistent:false,numerical:true,forms:[],rank:r,free};
  }
  return{consistent:true,forms,rank:r,free};
 }
 const known=f=>f&&f.coeff.every(v=>Math.abs(v)<1e-8);
 const difference=(a,b)=>({value:a.value-b.value,coeff:a.coeff.map((v,i)=>v-(b.coeff[i]||0))});
 function solve(input){
  const check=validate(input);if(!check.valid)return{valid:false,message:check.message,nodes:{},branches:{},islands:[]};
  const elements=input.elements,parent=Array.from({length:COLS*ROWS},(_,i)=>i),used=new Set([input.ground]);
  const find=n=>parent[n]===n?n:(parent[n]=find(parent[n]));const join=(a,b)=>{a=find(a);b=find(b);if(a!==b)parent[b]=a;};
  for(const e of elements){used.add(e.a);used.add(e.b);if(e.type==='wire'){const points=wireNodes(e.a,e.b);points.forEach(n=>used.add(n));points.slice(1).forEach((n,i)=>join(points[i],n));}}
  const roots=[...new Set([...used].map(find))],links=new Map(roots.map(n=>[n,new Set()]));
  for(const e of elements)if(e.type!=='wire'){const a=find(e.a),b=find(e.b);links.get(a).add(b);links.get(b).add(a);}
  const islands=[],islandByRoot=new Map(),branches={},nodes={};const groundRoot=find(input.ground);
  for(const first of roots){
   if(islandByRoot.has(first))continue;
   const group=[],queue=[first],seen=new Set(queue);while(queue.length){const a=queue.pop();group.push(a);for(const b of links.get(a))if(!seen.has(b)){seen.add(b);queue.push(b);}}
   const island={id:islands.length,roots:group,grounded:seen.has(groundRoot),consistent:true};islands.push(island);group.forEach(n=>islandByRoot.set(n,island));
   const reference=island.grounded?groundRoot:group[0],variables=group.filter(n=>n!==reference),index=new Map(variables.map((n,i)=>[n,i]));
   const parts=elements.filter(e=>e.type!=='wire'&&seen.has(find(e.a))),sources=parts.filter(e=>e.type==='voltage'),size=variables.length+sources.length;
   const A=Array.from({length:size},()=>Array(size).fill(0)),b=Array(size).fill(0);
   const stamp=(row,col,v)=>{if(row!==undefined&&col!==undefined)A[row][col]+=v;};
   for(const e of parts){
    const ai=index.get(find(e.a)),bi=index.get(find(e.b));
    if(e.type==='resistor'){const g=1/e.value;stamp(ai,ai,g);stamp(bi,bi,g);stamp(ai,bi,-g);stamp(bi,ai,-g);}
    if(e.type==='current'){if(ai!==undefined)b[ai]-=e.value;if(bi!==undefined)b[bi]+=e.value;}
   }
   sources.forEach((e,j)=>{const c=variables.length+j,ai=index.get(find(e.a)),bi=index.get(find(e.b));stamp(ai,c,1);stamp(bi,c,-1);stamp(c,ai,1);stamp(c,bi,-1);b[c]=e.value;});
   const solution=linear(A,b);island.consistent=solution.consistent;island.underdetermined=solution.consistent&&solution.free.length>0;island.numerical=Boolean(solution.numerical);
   island.forms=new Map();
   if(solution.consistent){const zero={value:0,coeff:Array(solution.free.length).fill(0)};island.forms.set(reference,zero);variables.forEach((n,i)=>island.forms.set(n,solution.forms[i]));}
   for(const e of parts){
    let voltage=null,current=null;
    if(solution.consistent){const dv=difference(island.forms.get(find(e.a)),island.forms.get(find(e.b)));if(known(dv))voltage=Math.abs(dv.value)<1e-12?0:dv.value;
     if(e.type==='resistor'&&voltage!==null)current=voltage/e.value;
     if(e.type==='current')current=e.value;
     if(e.type==='voltage'){const form=solution.forms[variables.length+sources.indexOf(e)];if(known(form))current=form.value;}
    }
    branches[e.id]={id:e.id,voltage,current,power:voltage!==null&&current!==null?voltage*current:null,island:island.id};
   }
  }
  for(const n of used){const root=find(n),island=islandByRoot.get(root),form=island.forms.get(root);nodes[n]={island:island.id,grounded:island.grounded,consistent:island.consistent,relative:known(form)?form.value:null,potential:island.grounded&&known(form)?form.value:null};}
  for(const e of elements)if(e.type==='wire'){const island=islandByRoot.get(find(e.a));branches[e.id]={id:e.id,voltage:island.consistent?0:null,current:null,power:island.consistent?0:null,island:island.id};}
  function measure(p,n){
   if(!nodes[p]||!nodes[n])return{value:null,reason:'Place both probes on connected grid points.'};
   const ip=islandByRoot.get(find(p)),im=islandByRoot.get(find(n));
   if(ip!==im)return{value:null,reason:'These points are on separate networks. Their voltage difference is not defined.'};
   if(!ip.consistent)return{value:null,reason:ip.numerical?'This circuit exceeds reliable numerical precision. Simplify the circuit or use less extreme values.':'No finite DC solution: check for a shorted/conflicting voltage source or a current source without a return path.'};
   const dv=difference(ip.forms.get(find(p)),ip.forms.get(find(n)));
   if(!known(dv))return{value:null,reason:'This voltage is not uniquely determined. Add a resistor return path or check the ideal sources.'};
   return{value:Math.abs(dv.value)<1e-12?0:dv.value,grounded:ip.grounded,positive:nodes[p].potential,negative:nodes[n].potential,reason:ip.grounded?'Voltage is measured from the − probe to the + probe.':'Same floating network: the difference is defined, but neither point has a voltage relative to ground.'};
  }
  const resistorPower=elements.filter(e=>e.type==='resistor').reduce((sum,e)=>branches[e.id].power===null?null:sum===null?null:sum+branches[e.id].power,0);
  const powerKnown=Object.values(branches).every(b=>b.power!==null),balance=powerKnown?Object.values(branches).reduce((s,b)=>s+b.power,0):null;
  return{valid:true,nodes,branches,islands:islands.map(({forms,...i})=>i),measure,resistorPower,powerBalance:balance,used:[...used],net:n=>validNode(n)?find(n):null};
 }
 function preset(name='divider'){
  const elements=[];let w=0;const add=(type,id,a,b,value)=>elements.push({type,id,a:node(...a),b:node(...b),...(value===undefined?{}:{value})});
  const wire=(a,b)=>add('wire','W'+(++w),a,b);
  let ground=node(1,4),positive=node(6,1),negative=ground;
  if(name==='blank')return{version:1,elements,ground:node(1,4),positive:node(6,1),negative:node(1,4)};
  if(name==='bridge'){
   add('voltage','V1',[1,2],[1,3],9);wire([1,2],[1,1]);wire([1,1],[6,1]);
   add('resistor','R1',[3,1],[3,2],100);add('resistor','R2',[3,3],[3,4],200);wire([3,2],[3,3]);
   add('resistor','R3',[6,1],[6,2],100);add('resistor','R4',[6,3],[6,4],200);wire([6,2],[6,3]);
   add('resistor','R5',[4,2],[5,2],150);wire([3,2],[4,2]);wire([5,2],[6,2]);
   wire([1,3],[1,5]);wire([1,5],[6,5]);wire([3,4],[3,5]);wire([6,4],[6,5]);
   ground=node(1,5);positive=node(3,2);negative=node(6,2);
  }else{
   add('voltage','V1',[1,1],[1,2],9);
   if(name==='parallel'){
    wire([1,1],[6,1]);add('resistor','R1',[4,1],[4,2],100);add('resistor','R2',[6,1],[6,2],200);wire([4,2],[4,4]);
   }else{wire([1,1],[3,1]);add('resistor','R1',[3,1],[4,1],100);wire([4,1],[6,1]);add('resistor','R2',[6,1],[6,2],name==='series'?100:200);}
   wire([6,2],[6,4]);wire([6,4],[1,4]);wire([1,4],[1,2]);
  }
  return{version:1,elements,ground,positive,negative};
 }
 const api={COLS,ROWS,MAX_ELEMENTS,LIMITS,validNode,node,xy,label,adjacent,wireNodes,wireEdges,edge,validate,linear,solve,preset};
 root.CircuitSolver=api;if(typeof module==='object'&&module.exports)module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
