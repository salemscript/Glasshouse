/* Exact sine paths and square-root polynomial distance plots for reviewed tasks. */
'use strict';
window.PhysicsTrajectoryPlots=(()=>{
 const finite=Number.isFinite,esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const range=r=>Array.isArray(r)&&r.length===2&&r.every(finite)&&r[1]>r[0]&&finite(r[1]-r[0]);
 const polynomial=(c,x)=>c.reduceRight((v,a)=>v*x+a,0);
 const derivative=c=>c.slice(1).map((a,i)=>a*(i+1));
 function roots(c,lo,hi){
  c=c.slice();while(c.length>1&&c.at(-1)===0)c.pop();if(c.length<=1)return [];
  if(c.length===2){const x=-c[0]/c[1];return x>=lo&&x<=hi?[x]:[];}
  const cuts=[lo,...roots(derivative(c),lo,hi),hi].sort((a,b)=>a-b),out=[];
  for(const x of cuts)if(Math.abs(polynomial(c,x))<=1e-12*Math.max(1,...c.map((v,i)=>Math.abs(v*x**i))))out.push(x);
  for(let i=1;i<cuts.length;i++){
   let l=cuts[i-1],r=cuts[i],fl=polynomial(c,l),fr=polynomial(c,r);if(fl===0||fr===0||Math.sign(fl)===Math.sign(fr))continue;
   for(let j=0;j<80;j++){const m=(l+r)/2,fm=polynomial(c,m);if(Math.sign(fm)===Math.sign(fl)){l=m;fl=fm;}else r=m;}
   out.push((l+r)/2);
  }
  return [...new Set(out)];
 }
 function model(def){
  if(!def||!Number.isInteger(def.fieldIndex)||def.fieldIndex<0||!range(def.xRange)||!range(def.yRange)||!Array.isArray(def.segments)||!def.segments.length||def.segments.length>12)return null;
  const inside=p=>Array.isArray(p)&&p.length===2&&p.every(finite)&&p[0]>=def.xRange[0]&&p[0]<=def.xRange[1]&&p[1]>=def.yRange[0]&&p[1]<=def.yRange[1];
  const segments=[];
  for(const s of def.segments){
   if(!range(s.domain)||s.domain[0]<def.xRange[0]||s.domain[1]>def.xRange[1])return null;
   let value,critical=[];
   if(s.sine){
    const a=s.sine;if(!['amplitude','angularFrequency','phase','offset'].every(k=>finite(a[k]))||s.coefficients||s.transform)return null;
    value=x=>a.offset+a.amplitude*Math.sin(a.angularFrequency*x+a.phase);
    if(a.angularFrequency!==0){const low=Math.min(a.angularFrequency*s.domain[0]+a.phase,a.angularFrequency*s.domain[1]+a.phase),high=Math.max(a.angularFrequency*s.domain[0]+a.phase,a.angularFrequency*s.domain[1]+a.phase);if((high-low)/Math.PI>1000)return null;for(let k=Math.ceil((low-Math.PI/2)/Math.PI);k<=Math.floor((high-Math.PI/2)/Math.PI);k++)critical.push((Math.PI/2+k*Math.PI-a.phase)/a.angularFrequency);}
   }else{
    const c=s.coefficients;if(!Array.isArray(c)||!c.length||c.length>5||!c.every(finite)||s.transform&&!['sqrt'].includes(s.transform))return null;
    critical=roots(derivative(c),...s.domain);
    if(s.transform==='sqrt'){
     const scale=x=>Math.max(1,c.reduce((v,a,i)=>v+Math.abs(a*x**i),0));
     // Only floating-point cancellation at an analytically zero boundary is tolerated.
     for(const x of [s.domain[0],s.domain[1],...critical])if(polynomial(c,x)<-32*Number.EPSILON*scale(x))return null;
     value=x=>{const r=polynomial(c,x);return r<0&&r>=-32*Number.EPSILON*scale(x)?0:Math.sqrt(r);};
    }else value=x=>polynomial(c,x);
   }
   const xs=[...Array.from({length:321},(_,i)=>s.domain[0]+(s.domain[1]-s.domain[0])*i/320),...critical].sort((a,b)=>a-b);xs[0]=s.domain[0];xs[xs.length-1]=s.domain[1];
   const points=xs.map(x=>[x,value(x)]);if(points.some(([x,y])=>!finite(y)||y<def.yRange[0]-1e-8||y>def.yRange[1]+1e-8))return null;
   segments.push({...s,value,points,critical});
  }
  const points=def.points||[],arrows=def.arrows||[];if(!Array.isArray(points)||!Array.isArray(arrows)||arrows.length>24||points.some(p=>!inside([p.x,p.y]))||arrows.some(a=>!inside(a.from)||!inside(a.to)))return null;
  for(const a of arrows)if(a.velocity||a.timeScale!==undefined){if(!Array.isArray(a.velocity)||a.velocity.length!==2||!a.velocity.every(finite)||!finite(a.timeScale)||a.timeScale<=0)return null;for(let i=0;i<2;i++)if(Math.abs(a.to[i]-a.from[i]-a.velocity[i]*a.timeScale)>1e-10*Math.max(1,Math.abs(a.to[i]),Math.abs(a.from[i])))return null;}
  const dx=def.xRange[1]-def.xRange[0],dy=def.yRange[1]-def.yRange[0],scale=Math.min(615/dx,330/dy);
  if(!finite(scale)||scale<=0)return null;
  const width=def.equalScale?scale*dx:615,height=def.equalScale?scale*dy:330,L=90+(615-width)/2,T=60+(330-height)/2,B=T+height,R=L+width;
  if(![width,height,L,T,B,R].every(finite)||width<=0||height<=0)return null;
  const x=v=>L+(v-def.xRange[0])/dx*width,y=v=>B-(v-def.yRange[0])/dy*height;
  return {...def,segments,points,arrows,x,y,box:{L,R,T,B}};
 }
 function svg(m,theme='light'){
  if(!m)return '';const{L,R,T,B}=m.box,fmt=x=>Number(x.toPrecision(4)).toString();
  const palette=theme==='dark'?{ink:'#e5eae4',grid:'#3d4d4b',axis:'#8baba4',curve:'#f0917e',arrow:'#8dc5c9',paper:'#182323'}:{ink:'#3c4645',grid:'#d9ded9',axis:'#83928e',curve:'#d86654',arrow:'#377f85',paper:'#fffdf7'};
  const ticks=Array.from({length:5},(_,i)=>i/4),grid=ticks.map(f=>{const vx=m.xRange[0]+f*(m.xRange[1]-m.xRange[0]),vy=m.yRange[0]+f*(m.yRange[1]-m.yRange[0]);return `<path d="M${m.x(vx)} ${T}V${B}M${L} ${m.y(vy)}H${R}" stroke="var(--ptp-grid)" fill="none"/><text x="${m.x(vx)}" y="${B+25}" text-anchor="middle">${esc(fmt(vx))}</text><text x="${L-12}" y="${m.y(vy)+5}" text-anchor="end">${esc(fmt(vy))}</text>`;}).join('');
  const curves=m.segments.map(s=>`<path d="M${s.points.map(([x,y])=>`${m.x(x).toFixed(3)},${m.y(y).toFixed(3)}`).join('L')}" stroke="var(--ptp-curve)" stroke-width="3" fill="none"/>`).join('');
  const occupied=[];function label(text,px,py){if(!text)return '';const w=String(text).length*7.2;let best=null;for(const dy of[-25,31,-50,56])for(const anchor of['start','end']){const tx=px+(anchor==='start'?9:-9),box={l:anchor==='start'?tx:tx-w,r:anchor==='start'?tx+w:tx,t:py+dy-15,b:py+dy+3};if(box.l<L+3||box.r>R-3||box.t<T+3||box.b>B-3)continue;const hits=occupied.filter(b=>box.l<b.r+5&&box.r>b.l-5&&box.t<b.b+5&&box.b>b.t-5).length;if(!best||hits<best.hits)best={tx,ty:py+dy,anchor,box,hits};}if(!best)best={tx:Math.min(R-15,Math.max(L+15,px)),ty:Math.min(B-18,Math.max(T+18,py)),anchor:'middle'};if(best.box)occupied.push(best.box);return `<text x="${best.tx}" y="${best.ty}" text-anchor="${best.anchor}" paint-order="stroke" stroke="var(--ptp-paper)" stroke-width="4" stroke-linejoin="round">${esc(text)}</text>`;}
  const arrows=m.arrows.map(a=>{const fx=m.x(a.from[0]),fy=m.y(a.from[1]),tx=m.x(a.to[0]),ty=m.y(a.to[1]),d=Math.hypot(tx-fx,ty-fy);if(d===0)return '';const ux=(tx-fx)/d,uy=(ty-fy)/d,h=Math.min(11,d*.35),w=h*.45;return `<path d="M${fx} ${fy}L${tx} ${ty}" stroke="var(--ptp-arrow)" stroke-width="2.5"/><polygon points="${tx},${ty} ${tx-h*ux+w*uy},${ty-h*uy-w*ux} ${tx-h*ux-w*uy},${ty-h*uy+w*ux}" fill="var(--ptp-arrow)"/>${label(a.label,(fx+tx)/2,(fy+ty)/2)}`;}).join('');
  const points=m.points.map(p=>`<circle cx="${m.x(p.x)}" cy="${m.y(p.y)}" r="4" fill="var(--ptp-curve)"/>${label(p.label,m.x(p.x),m.y(p.y))}`).join('');
  const axes=`M${L} ${T}V${B}H${R}${m.yRange[0]<=0&&m.yRange[1]>=0?`M${L} ${m.y(0)}H${R}`:''}${m.xRange[0]<=0&&m.xRange[1]>=0?`M${m.x(0)} ${T}V${B}`:''}`;
  const result=`<svg class="ptp-svg" viewBox="0 0 760 490" role="img" aria-label="${esc(m.title+'. '+m.caption)}" xmlns="http://www.w3.org/2000/svg"><title>${esc(m.title)}</title><desc>${esc(m.caption)}</desc><g fill="var(--ptp-ink)" font-family="sans-serif" font-size="14">${grid}<text x="${L}" y="28">${esc(m.yLabel)}</text><text x="${R}" y="${B+60}" text-anchor="end">${esc(m.xLabel)}</text><path d="${axes}" stroke="var(--ptp-axis)" fill="none"/>${curves}${arrows}${points}</g></svg>`;
  return result.replace(/(fill|stroke)="var\(--ptp-(\w+)\)"/g,(_,attribute,role)=>`class="ptp-${role}" ${attribute}="${palette[role]}"`);
 }
 return{model,svg};
})();
