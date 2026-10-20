/* Original, equation-driven plots for source exercises with explicit graph requests. */
'use strict';
window.Chapter23Visuals=(()=>{
 const EPS0=8.8541878128e-12;
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const positive=n=>typeof n==='number'&&Number.isFinite(n)&&n>0;
 const fmt=(n,d=3)=>Number(n).toPrecision(d).replace(/\.0+(?=e|$)/,'').replace(/(\.\d*?[1-9])0+(?=e|$)/,'$1');
 const sample=(a,b,fn,n=100)=>Array.from({length:n+1},(_,i)=>{const r=a+(b-a)*i/n;return [r,fn(r)];});
 function kinematicModel(def){
  const range=r=>Array.isArray(r)&&r.length===2&&r.every(Number.isFinite)&&r[1]>r[0];
  if(!def||!Number.isInteger(def.fieldIndex)||!range(def.xRange)||!range(def.yRange)||!def.segments?.length)return null;
  const segments=[];
  for(const s of def.segments){
   if(!range(s.domain)||s.domain[0]<def.xRange[0]||s.domain[1]>def.xRange[1]||!Array.isArray(s.coefficients)||!s.coefficients.length||s.coefficients.length>5||!s.coefficients.every(Number.isFinite))return null;
   const value=t=>s.coefficients.reduceRight((v,c)=>v*t+c,0),points=sample(s.domain[0],s.domain[1],value,240);
   // Preserve exact authored endpoints; interpolation can round a shared irrational boundary.
   points[0]=[s.domain[0],value(s.domain[0])];points[points.length-1]=[s.domain[1],value(s.domain[1])];
   if(points.some(([,v])=>!Number.isFinite(v)||v<def.yRange[0]-1e-7||v>def.yRange[1]+1e-7))return null;
   const comparison=Boolean(s.dashed||s.style==='secant'||/secant|tangent/i.test(s.label||''));
   const patterns=['9 6','2 5','12 4','8 3 2 3','3 4'];
   segments.push({points,label:s.label||(s.style==='secant'?'Endpoint secant':'Source curve '+(segments.length+1)),comparison,pattern:comparison?patterns[Math.max(0,segments.length-1)%patterns.length]:'',value});
  }
  const points=def.points||[];
  if(!Array.isArray(points)||points.some(p=>!Number.isFinite(p.x)||!Number.isFinite(p.y)||p.x<def.xRange[0]||p.x>def.xRange[1]||p.y<def.yRange[0]||p.y>def.yRange[1]))return null;
  const openEndpoints=[];
  for(let i=0;i<segments.length;i++)for(let j=i+1;j<segments.length;j++){
   if(segments[i].comparison||segments[j].comparison)continue;
   const a=segments[i].points.at(-1),b=segments[j].points[0];
   const sameBoundary=Math.abs(a[0]-b[0])<=32*Number.EPSILON*Math.max(1,Math.abs(a[0]),Math.abs(b[0]));
   if(sameBoundary&&Math.abs(a[1]-b[1])>1e-10)openEndpoints.push(a,[a[0],b[1]]);
  }
  return {...def,segments,points,openEndpoints};
 }
 function kinematicSVG(m){
  const L=90,R=705,T=58,B=325,x=v=>L+(v-m.xRange[0])/(m.xRange[1]-m.xRange[0])*(R-L),y=v=>B-(v-m.yRange[0])/(m.yRange[1]-m.yRange[0])*(B-T);
  const ticks=Array.from({length:5},(_,i)=>i/4);
  const grid=ticks.map(f=>{const vx=m.xRange[0]+f*(m.xRange[1]-m.xRange[0]),vy=m.yRange[0]+f*(m.yRange[1]-m.yRange[0]);return `<path d="M${x(vx)} ${T}V${B}M${L} ${y(vy)}H${R}" class="chapter23-plot-grid"/><text x="${x(vx)}" y="${B+27}" text-anchor="middle">${esc(fmt(vx))}</text><text x="${L-14}" y="${y(vy)+5}" text-anchor="end">${esc(fmt(vy))}</text>`;}).join('');
  const axisX=m.yRange[0]<=0&&m.yRange[1]>=0?y(0):B,axisY=m.xRange[0]<=0&&m.xRange[1]>=0?x(0):L;
  const curves=m.segments.map(s=>`<path d="M${s.points.map(([a,b])=>x(a).toFixed(2)+','+y(b).toFixed(2)).join('L')}"${s.comparison?` class="chapter23-plot-comparison" stroke-dasharray="${s.pattern}"`:''}/>`).join('');
  const occupied=[],curvePixels=m.segments.flatMap(s=>s.points.map(([a,b])=>[x(a),y(b)]));
  const points=m.points.map(p=>{
   const px=x(p.x),py=y(p.y),width=Math.min(260,String(p.label||'').length*7.6),preferred=px>R-125?'end':'start',candidates=[];
   for(const anchor of [preferred,preferred==='start'?'end':'start'])for(const dy of [-32,32,-58,58,-86,86]){
    const tx=px+(anchor==='end'?-10:10),ty=py+dy,box={left:anchor==='end'?tx-width:tx,right:anchor==='end'?tx:tx+width,top:ty-15,bottom:ty+4};
    if(box.left<L+4||box.right>R-4||box.top<T+4||box.bottom>B-4)continue;
    const curveHits=curvePixels.filter(([a,b])=>a>box.left-2&&a<box.right+2&&b>box.top-2&&b<box.bottom+2).length;
    const labelHits=occupied.filter(b=>box.left<b.right+5&&box.right>b.left-5&&box.top<b.bottom+5&&box.bottom>b.top-5).length;
    candidates.push({tx,ty,anchor,box,score:curveHits+1000*labelHits+Math.abs(dy)/1000});
   }
   candidates.sort((a,b)=>a.score-b.score);const best=candidates[0]||{tx:Math.min(R-8,Math.max(L+8,px)),ty:Math.min(B-18,Math.max(T+18,py-24)),anchor:'middle'};
   if(best.box)occupied.push(best.box);
   return `<circle cx="${px}" cy="${py}" r="4.5" class="chapter23-plot-solid"/>${p.label?`<text x="${best.tx}" y="${best.ty}" text-anchor="${best.anchor}">${esc(p.label)}</text>`:''}`;
  }).join('');
  const legend=m.segments.length>1?m.segments.map((s,i)=>{const lx=L+(i%2)*310,ly=421+Math.floor(i/2)*26;return `<path d="M${lx} ${ly}h40" class="chapter23-plot-legend-line${s.comparison?' chapter23-plot-comparison':''}"${s.pattern?` stroke-dasharray="${s.pattern}"`:''}/><text x="${lx+49}" y="${ly+4}" font-size="12">${esc(s.label)}</text>`;}).join(''):'';
  const height=legend?442+Math.ceil(m.segments.length/2)*26:410;
  const endpoints=m.openEndpoints.map(([a,b])=>`<circle cx="${x(a)}" cy="${y(b)}" r="5" class="chapter23-plot-open"/>`).join('');
  return `<svg viewBox="0 0 760 ${height}" role="img" aria-label="${esc(m.title+'. '+m.caption)}" xmlns="http://www.w3.org/2000/svg"><title>${esc(m.title)}</title><desc>${esc(m.caption)}</desc><g class="chapter23-plot-labels">${grid}<text x="${L}" y="27" class="chapter23-plot-axis-label">${esc(m.yLabel)}</text><text x="${R}" y="${B+66}" text-anchor="end" class="chapter23-plot-axis-label">${esc(m.xLabel)}</text></g><path d="M${L} ${T}V${B}H${R}M${L} ${axisX}H${R}M${axisY} ${T}V${B}" class="chapter23-plot-axis"/><g class="chapter23-plot-curves">${curves}</g>${endpoints}<g class="chapter23-plot-labels">${points}${legend}</g></svg>`;
 }
 function vectorModel(def){
  const range=r=>Array.isArray(r)&&r.length===2&&r.every(Number.isFinite)&&Number.isFinite(r[1]-r[0])&&r[1]>r[0];
  if(!def||!Number.isInteger(def.fieldIndex)||def.fieldIndex<0||!range(def.xRange)||!range(def.yRange)||!Array.isArray(def.arrows)||!def.arrows.length||def.arrows.length>32)return null;
  const inside=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isFinite)&&p[0]>=def.xRange[0]&&p[0]<=def.xRange[1]&&p[1]>=def.yRange[0]&&p[1]<=def.yRange[1];
  if(def.arrows.some(a=>!inside(a.from)||!inside(a.to)||!['given','resultant','component'].includes(a.role)))return null;
  const points=def.points||[];
  if(!Array.isArray(points)||points.some(p=>!inside([p.x,p.y])))return null;
  const dx=def.xRange[1]-def.xRange[0],dy=def.yRange[1]-def.yRange[0],scale=Math.min(615/dx,400/dy);
  if(!positive(scale))return null;
  const left=90+(615-scale*dx)/2,top=65+(400-scale*dy)/2;
  const x=v=>left+scale*(v-def.xRange[0]),y=v=>top+scale*(def.yRange[1]-v);
  const arrows=def.arrows.map(a=>({...a,dx:a.to[0]-a.from[0],dy:a.to[1]-a.from[1],fromPixel:[x(a.from[0]),y(a.from[1])],toPixel:[x(a.to[0]),y(a.to[1])]}));
  if(arrows.some(a=>!Number.isFinite(Math.hypot(a.dx,a.dy))))return null;
  const rawStep=Math.max(dx,dy)/4,order=10**Math.floor(Math.log10(rawStep)),step=[1,2,2.5,5,10].find(n=>n*order>=rawStep)*order;
  if(!positive(step))return null;
  const ticks=r=>Array.from({length:Math.max(0,Math.floor(r[1]/step)-Math.ceil(r[0]/step)+1)},(_,i)=>(Math.ceil(r[0]/step)+i)*step).map(v=>Math.abs(v)<step*1e-10?0:v);
  return {...def,points,arrows,scale,x,y,box:{left,top,right:left+scale*dx,bottom:top+scale*dy},xTicks:ticks(def.xRange),yTicks:ticks(def.yRange)};
 }
 function vectorSVG(m){
  const {left:L,top:T,right:R,bottom:B}=m.box;
  const grid=m.xTicks.map(v=>`<path d="M${m.x(v)} ${T}V${B}" class="chapter23-plot-grid"/><text x="${m.x(v)}" y="${B+25}" text-anchor="middle">${esc(fmt(v))}</text>`).join('')+m.yTicks.map(v=>`<path d="M${L} ${m.y(v)}H${R}" class="chapter23-plot-grid"/><text x="${L-12}" y="${m.y(v)+5}" text-anchor="end">${esc(fmt(v))}</text>`).join('');
  const axes=`<path d="M${L} ${T}V${B}H${R}${m.yRange[0]<=0&&m.yRange[1]>=0?`M${L} ${m.y(0)}H${R}`:''}${m.xRange[0]<=0&&m.xRange[1]>=0?`M${m.x(0)} ${T}V${B}`:''}" class="chapter23-plot-axis"/>`;
  const occupied=[],samples=m.arrows.flatMap(a=>Array.from({length:41},(_,i)=>[a.fromPixel[0]+(a.toPixel[0]-a.fromPixel[0])*i/40,a.fromPixel[1]+(a.toPixel[1]-a.fromPixel[1])*i/40]));
  function label(text,px,py,nx=0,ny=-1){
   if(!text)return '';
   const width=Math.min(300,String(text).length*7.3),candidates=[];
   for(const side of[1,-1])for(const gap of[22,42,65])for(const anchor of['middle','start','end']){
    const tx=px+side*gap*nx,ty=py+side*gap*ny,box={left:tx-(anchor==='middle'?width/2:anchor==='end'?width:0),right:tx+(anchor==='middle'?width/2:anchor==='start'?width:0),top:ty-15,bottom:ty+4};
    if(box.left<L+4||box.right>R-4||box.top<T+4||box.bottom>B-4)continue;
    const hits=samples.filter(([a,b])=>a>box.left-3&&a<box.right+3&&b>box.top-3&&b<box.bottom+3).length;
    const overlaps=occupied.filter(b=>box.left<b.right+5&&box.right>b.left-5&&box.top<b.bottom+5&&box.bottom>b.top-5).length;
    candidates.push({tx,ty,anchor,box,score:hits+overlaps*1000+gap/1000});
   }
   candidates.sort((a,b)=>a.score-b.score);
   const p=candidates[0]||{tx:Math.max(L+width/2+4,Math.min(R-width/2-4,px)),ty:Math.max(T+18,Math.min(B-8,py-25)),anchor:'middle'};
   if(p.box)occupied.push(p.box);
   return `<text x="${p.tx}" y="${p.ty}" text-anchor="${p.anchor}">${esc(text)}</text>`;
  }
  let labels='';
  const arrows=m.arrows.map(a=>{
   const [x1,y1]=a.fromPixel,[x2,y2]=a.toPixel,dx=x2-x1,dy=y2-y1,length=Math.hypot(dx,dy),cls='chapter23-vector-'+a.role;
   if(length===0){labels+=label((a.label?a.label+': ':'')+'zero vector',x1,y1);return `<circle cx="${x1}" cy="${y1}" r="4" class="chapter23-vector-zero ${cls}"/>`;}
   const ux=dx/length,uy=dy/length,head=Math.min(11,length*.35),half=head*.42;
   labels+=label(a.label,(x1+x2)/2,(y1+y2)/2,-uy,ux);
   return `<g class="chapter23-vector-arrow ${cls}"><path d="M${x1} ${y1}L${x2} ${y2}"/><path class="chapter23-vector-head" d="M${x2} ${y2}L${x2-head*ux+half*uy} ${y2-head*uy-half*ux}L${x2-head*ux-half*uy} ${y2-head*uy+half*ux}Z"/></g>`;
  }).join('');
  const points=m.points.map(p=>{labels+=label(p.label,m.x(p.x),m.y(p.y));return `<circle cx="${m.x(p.x)}" cy="${m.y(p.y)}" r="3" class="chapter23-plot-solid"/>`;}).join('');
  const roles=['given','resultant','component'].filter(role=>m.arrows.some(a=>a.role===role));
  const legend=roles.map((role,i)=>`<g class="chapter23-vector-arrow chapter23-vector-${role}"><path d="M${90+i*205} 548h34"/></g><text x="${132+i*205}" y="553">${role==='given'?'Given vector':role==='resultant'?'Resultant vector':'Component'}</text>`).join('');
  return `<svg viewBox="0 0 760 580" role="img" aria-label="${esc(m.title+'. '+m.caption)}" xmlns="http://www.w3.org/2000/svg"><title>${esc(m.title)}</title><desc>${esc(m.caption)} Horizontal and vertical coordinates use the same physical scale. A zero vector has no direction.</desc><g class="chapter23-plot-labels">${grid}<text x="${L}" y="30" class="chapter23-plot-axis-label">${esc(m.yLabel)}</text><text x="${R}" y="510" text-anchor="end" class="chapter23-plot-axis-label">${esc(m.xLabel)}</text></g>${axes}${arrows}${points}<g class="chapter23-plot-labels">${labels}${legend}</g></svg>`;
 }
 function model(def){
  if(def?.type==='concentric-shells'){
   const {R1,R2,q1,q2}=def,k=1/(4*Math.PI*EPS0);
   if(!positive(R1)||!positive(R2)||R2<=R1||!positive(q1)||!positive(q2))return null;
   const field=r=>r===R1||r===R2?NaN:r<R1?0:k*(r<R2?q1:q1+q2)/r**2;
   const potential=r=>k*(q1/Math.max(r,R1)+q2/Math.max(r,R2));
   return {type:def.type,R1,R2,q1,q2,k,maxR:4*R2,field,potential,innerField:k*q1/R1**2,outerField:k*(q1+q2)/R2**2};
  }
  if(!def||!positive(def.R))return null;
  const R=def.R;
  if(def.type==='cylinder-shell'&&positive(def.lambda)){
   const peak=def.lambda/(2*Math.PI*EPS0*R),outside=r=>def.lambda/(2*Math.PI*EPS0*r);
   if(!positive(peak))return null;
   return {type:def.type,R,maxR:2*R,peak,scale:1000,unit:'kN/C',surfaceDefined:false,field:r=>r<R?0:r===R?NaN:outside(r),segments:[[[0,0],[R,0]],sample(R,2*R,outside)],endpoint:outside(2*R)};
  }
  if(def.type==='radial-density-sphere'&&positive(def.rho0)){
   const Q=Math.PI*def.rho0*R**3,inside=r=>def.rho0*r*r/(4*EPS0*R),outside=r=>Q/(4*Math.PI*EPS0*r*r),peak=inside(R);
   if(!positive(peak)||!positive(Q))return null;
   return {type:def.type,R,maxR:3*R,Q,peak,scale:.001,unit:'mN/C',surfaceDefined:true,field:r=>r<=R?inside(r):outside(r),segments:[sample(0,R,inside),sample(R,3*R,outside)],endpoint:outside(3*R)};
  }
  return null;
 }
 function plotSVG(m){
  const left=82,right=704,top=65,bottom=321,width=right-left,height=bottom-top;
  const peak=m.peak/m.scale,order=10**Math.floor(Math.log10(peak)),yMax=Math.ceil(peak*1.18/(order/2))*(order/2);
  const x=r=>left+r/m.maxR*width,y=e=>bottom-e/m.scale/yMax*height,rx=x(m.R),peakY=y(m.peak),endY=y(m.endpoint);
  const cylinder=m.type==='cylinder-shell',id='chapter23-'+m.type,domain=cylinder?2:3;
  const path=points=>'M'+points.map(([r,e])=>x(r).toFixed(2)+','+y(e).toFixed(2)).join('L');
  const ticks=Array.from({length:4},(_,i)=>yMax*i/3);
  const grid=ticks.map(v=>`<path d="M${left} ${y(v*m.scale).toFixed(2)}H${right}" class="chapter23-plot-grid"/><text x="${left-15}" y="${y(v*m.scale)+5}" text-anchor="end">${esc(fmt(v))}</text>`).join('');
  const xTicks=Array.from({length:domain+1},(_,i)=>`<path d="M${x(i*m.R)} ${bottom}v7" class="chapter23-plot-tick"/><text x="${x(i*m.R)}" y="${bottom+27}" text-anchor="middle">${esc(fmt(i*m.R*100))}</text>${i?`<text x="${x(i*m.R)}" y="${bottom+47}" text-anchor="middle" class="chapter23-plot-symbol">${i===1?'R':i+'R'}</text>`:''}`).join('');
  const title=cylinder?'Electric field across an ideal cylindrical shell':'Electric field of a sphere with density increasing with radius';
  const description=cylinder?`The field is zero inside radius ${fmt(m.R*100)} centimeters. Its one-sided outer value is ${fmt(peak)} ${m.unit}, then it decreases as one over radius to ${fmt(m.endpoint/m.scale)} ${m.unit} at twice the radius. The ideal surface has no single field value.`:`The field rises quadratically inside radius ${fmt(m.R*100)} centimeters to a continuous maximum of ${fmt(peak)} ${m.unit}, then falls as one over radius squared to ${fmt(m.endpoint/m.scale)} ${m.unit} at three times the radius.`;
  return `<svg viewBox="0 0 760 421" role="img" aria-label="${esc(title+'. '+description)}" xmlns="http://www.w3.org/2000/svg"><title>${esc(title)}</title><desc>${esc(description)}</desc><defs><marker id="${id}-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#535c59"/></marker></defs><rect x="${left}" y="${top}" width="${rx-left}" height="${height}" fill="#ed7466" opacity=".045"/><g class="chapter23-plot-labels">${grid}${xTicks}<text x="${left}" y="26" class="chapter23-plot-axis-label">E (${m.unit})</text><text x="${right+10}" y="${bottom+80}" text-anchor="end" class="chapter23-plot-axis-label">r (cm)</text><text x="${(left+rx)/2}" y="${top-14}" text-anchor="middle" class="chapter23-plot-region">${cylinder?'Inside shell':'Inside sphere'}</text><text x="${(rx+right)/2}" y="${top-14}" text-anchor="middle" class="chapter23-plot-region">${cylinder?'Outside shell':'Outside sphere'}</text></g><path d="M${rx} ${top-3}V${bottom+4}" class="chapter23-plot-boundary"/><path d="M${left} ${top-12}V${bottom}H${right+15}" class="chapter23-plot-axis" marker-end="url(#${id}-arrow)"/><path d="M${left} ${top-20}l-3 8h6Z" fill="#535c59"/><g class="chapter23-plot-curves">${m.segments.map(points=>`<path d="${path(points)}"/>`).join('')}</g>${cylinder?`<circle cx="${rx}" cy="${bottom}" r="5" class="chapter23-plot-open"/><circle cx="${rx}" cy="${peakY}" r="5" class="chapter23-plot-open"/><text x="${(left+rx)/2}" y="${bottom-25}" text-anchor="middle" class="chapter23-plot-formula">E = 0</text><text x="${rx+19}" y="${peakY-19}" class="chapter23-plot-value">E(R<tspan baseline-shift="super" font-size="10">+</tspan>) = ${esc(fmt(peak))} ${m.unit}</text><text x="${rx+18}" y="${bottom-12}" class="chapter23-plot-value">E(R<tspan baseline-shift="super" font-size="10">−</tspan>) = 0</text><text x="${rx+150}" y="${peakY+30}" class="chapter23-plot-formula">E ∝ 1/r</text>`:`<circle cx="${rx}" cy="${peakY}" r="5" class="chapter23-plot-solid"/><text x="${rx+18}" y="${peakY-18}" class="chapter23-plot-value">E(R) = ${esc(fmt(peak))} ${m.unit}</text><text x="${left+34}" y="${top+105}" class="chapter23-plot-formula">E ∝ r²</text><text x="${rx+175}" y="${top+130}" class="chapter23-plot-formula">E ∝ 1/r²</text>`}<circle cx="${right}" cy="${endY}" r="4" class="chapter23-plot-solid"/><text x="${right-6}" y="${endY+(cylinder?28:-17)}" text-anchor="end" class="chapter23-plot-value">E(${domain}R) = ${esc(fmt(m.endpoint/m.scale))} ${m.unit}</text></svg>`;
 }
 function shellSVG(m,quantity){
  const isE=quantity==='E',L=82,T=62,B=320,W=622,H=B-T,scale=1000;
  const max=(isE?Math.max(m.innerField,m.outerField):m.potential(0))*1.18,x=r=>L+W*r/m.maxR,y=v=>B-H*v/max;
  const fn=isE?m.field:m.potential;
  const segments=isE?[[[0,0],[m.R1,0]],sample(m.R1,m.R2,r=>m.k*m.q1/r**2),sample(m.R2,m.maxR,r=>m.k*(m.q1+m.q2)/r**2)]:[sample(0,m.R1,fn),sample(m.R1,m.R2,fn),sample(m.R2,m.maxR,fn)];
  const path=points=>'M'+points.map(([r,v])=>x(r).toFixed(2)+','+y(v).toFixed(2)).join('L');
  const title=isE?'Electric field of two charged conducting shells':'Electric potential of two charged conducting shells';
  const desc=isE?'Zero field inside the inner shell, inverse-square branches outside each shell, and distinct open endpoints at both charged surfaces. The field tends to zero at infinity.':'A constant potential inside the inner shell, decreasing curved branches between and outside shells, continuous at both surfaces and tending to zero at infinity.';
  const grid=Array.from({length:5},(_,i)=>{const v=max*i/4;return `<path d="M${L} ${y(v)}h${W}" class="chapter23-plot-grid"/><text x="${L-12}" y="${y(v)+5}" text-anchor="end">${esc(fmt(v/scale))}</text>`;}).join('');
  const ticks=[0,m.R1,m.R2,2*m.R2,3*m.R2,4*m.R2].map(r=>`<path d="M${x(r)} ${B}v6" class="chapter23-plot-tick"/><text x="${x(r)}" y="${B+25}" text-anchor="middle">${esc(fmt(r))}</text>`).join('');
  const boundaries=[m.R1,m.R2].map((r,i)=>`<path d="M${x(r)} ${T}V${B}" class="chapter23-plot-boundary"/><text x="${x(r)}" y="${T-15}" text-anchor="middle">R${i+1} = ${esc(fmt(r))} m</text>`).join('');
  const endpoints=isE?[[m.R1,0],[m.R1,m.innerField],[m.R2,m.k*m.q1/m.R2**2],[m.R2,m.outerField]].map(([r,v])=>`<circle cx="${x(r)}" cy="${y(v)}" r="5" class="chapter23-plot-open"/>`).join(''):[m.R1,m.R2].map(r=>`<circle cx="${x(r)}" cy="${y(fn(r))}" r="5" class="chapter23-plot-solid"/>`).join('');
  return `<svg viewBox="0 0 760 405" role="img" aria-label="${esc(title+'. '+desc)}" xmlns="http://www.w3.org/2000/svg"><title>${title}</title><desc>${desc}</desc><g class="chapter23-plot-labels">${grid}${ticks}${boundaries}<text x="${L}" y="25" class="chapter23-plot-axis-label">${isE?'E (kN/C)':'V (kV)'}</text><text x="${L+W}" y="${B+60}" text-anchor="end" class="chapter23-plot-axis-label">r (m)</text></g><path d="M${L} ${T}V${B}h${W}" class="chapter23-plot-axis"/><g class="chapter23-plot-curves">${segments.map(p=>`<path d="${path(p)}"/>`).join('')}</g>${endpoints}</svg>`;
 }
 function solution(p){
  const def=p?.answerAudit?.solutionPlot;
  if(def?.type==='work-energy-curves'){
   if(!p?.answerAudit?.chapterStudyVerified||!window.PhysicsWorkPlots)return '';
   return (def.plots||[]).filter(d=>p.finalRules?.some(r=>r.fieldIndex===d.fieldIndex)).map(PhysicsWorkPlots.model).filter(Boolean).map(m=>`<figure class="chapter23-solution-plot"><h4>${esc(m.title)}</h4><div class="chapter23-plot-canvas" tabindex="0" role="region" aria-label="${esc(m.title)}. Scroll horizontally on small screens.">${PhysicsWorkPlots.svg(m)}</div><p class="chapter23-plot-scroll-note">Scroll across the graph to keep its measurements readable.</p><figcaption><p>${esc(m.caption)}</p><p>${m.ledger?'Signed store bars share the declared fixed joule scale; transfer arrows show direction only. Net energy entering the system equals the sum of all store changes. This static energy statement does not automatically grade freehand drawing or certify a simulation.':'Fixed reference axes preserve the stated units and domain. Shading, when present, represents the declared signed integral; a graph of work is already accumulated work. This static construction does not automatically grade freehand drawing or certify a simulated trajectory.'}</p></figcaption></figure>`).join('');
  }
  if(def?.type==='force-motion-curves'){
   if(!p?.answerAudit?.chapterStudyVerified||!window.PhysicsForceCurves)return '';
   return (def.plots||[]).filter(d=>p.finalRules?.some(r=>r.fieldIndex===d.fieldIndex)).map(PhysicsForceCurves.model).filter(Boolean).map(m=>`<figure class="chapter23-solution-plot"><h4>${esc(m.title)}</h4><div class="chapter23-plot-canvas" tabindex="0" role="region" aria-label="${esc(m.title)}. Scroll horizontally on small screens.">${PhysicsForceCurves.svg(m)}</div><p class="chapter23-plot-scroll-note">Scroll across the graph to keep its measurements readable.</p><figcaption><p>${esc(m.caption)}</p><p>The curves follow the worked force equations on fixed reference axes. Only physical branches are drawn; a clipped curve continues above the displayed scale. This static construction does not automatically grade freehand drawing.</p></figcaption></figure>`).join('');
  }
  if(def?.type==='trajectory-curves'){
   if(!p?.answerAudit?.chapterStudyVerified||!window.PhysicsTrajectoryPlots)return '';
   return (def.plots||[]).filter(d=>p.finalRules?.some(r=>r.fieldIndex===d.fieldIndex)).map(PhysicsTrajectoryPlots.model).filter(Boolean).map(m=>`<figure class="chapter23-solution-plot"><h4>${esc(m.title)}</h4><div class="chapter23-plot-canvas" tabindex="0" role="region" aria-label="${esc(m.title)}. Scroll horizontally on small screens.">${PhysicsTrajectoryPlots.svg(m)}</div><p class="chapter23-plot-scroll-note">Scroll across the graph to keep its measurements readable.</p><figcaption><p>${esc(m.caption)}</p><p>Curves follow the stated equations over the physical domain, with fixed reference axes. Arrow lengths use the declared time scale when showing velocity. This worked drawing does not automatically grade freehand work.</p></figcaption></figure>`).join('');
  }
  if(def?.type==='vectors3d'){
   if(!p?.answerAudit?.chapterStudyVerified||!window.PhysicsVector3D)return '';
   return (def.plots||[]).filter(d=>p.finalRules?.some(r=>r.fieldIndex===d.fieldIndex)).map(PhysicsVector3D.model).filter(Boolean).map(m=>`<figure class="chapter23-solution-plot"><h4>${esc(m.title)}</h4><div class="chapter23-plot-canvas" tabindex="0" role="region" aria-label="${esc(m.title)}. Scroll horizontally on small screens.">${PhysicsVector3D.svg(m)}</div><p class="chapter23-plot-scroll-note">Scroll across the construction to keep all three coordinate axes visible.</p><figcaption><p>${esc(m.caption)}</p><p>This fixed orthographic view retains all three signed coordinates. Projected angles and lengths are foreshortened; use the components in the worked equations for actual magnitudes. This construction does not automatically grade freehand drawing.</p></figcaption></figure>`).join('');
  }
  if(def?.type==='vectors2d'){
   if(!p?.answerAudit?.chapterStudyVerified)return '';
   return (def.plots||[]).filter(d=>p.finalRules?.some(r=>r.fieldIndex===d.fieldIndex)).map(vectorModel).filter(Boolean).map(m=>`<figure class="chapter23-solution-plot"><h4>${esc(m.title)}</h4><div class="chapter23-plot-canvas" tabindex="0" role="region" aria-label="${esc(m.title)}. Scroll horizontally on small screens.">${vectorSVG(m)}</div><p class="chapter23-plot-scroll-note">Scroll across the diagram to keep its labels readable.</p><figcaption><p>${esc(m.caption)}</p><p>Both axes use one equal physical scale, preserving vector angles and lengths. Arrowheads show direction; a zero vector has no direction. This worked construction does not automatically grade freehand drawing.</p></figcaption></figure>`).join('');
  }
  if(def?.type==='kinematics'){
   if(!p?.answerAudit?.chapterStudyVerified)return '';
   return (def.plots||[]).filter(d=>p.finalRules?.some(r=>r.fieldIndex===d.fieldIndex)).map(kinematicModel).filter(Boolean).map(m=>`<figure class="chapter23-solution-plot"><h4>${esc(m.title)}</h4><div class="chapter23-plot-canvas" tabindex="0" role="region" aria-label="${esc(m.title)}. Scroll horizontally on small screens.">${kinematicSVG(m)}</div><p class="chapter23-plot-scroll-note">Scroll across the graph to keep its labels readable.</p><figcaption><p>${esc(m.caption)}</p><p>Axes retain the stated physical units and fixed reference ranges. This is an equation-driven solution sketch, not a claim that freehand drawing is automatically graded.</p></figcaption></figure>`).join('');
  }
  if(def?.type==='concentric-shells'){
   if(!p?.answerAudit?.chapterStudyVerified||!def.fieldIndexes?.some(i=>p.finalRules?.some(r=>r.fieldIndex===i)))return '';
   const m=model(def);if(!m)return '';
   const quantity=p.finalRules.some(r=>r.fieldIndex===def.fieldIndexes[0])?'E':'V';
   return `<figure class="chapter23-solution-plot"><h4>Part J · Sketch ${quantity} against radius</h4><div class="chapter23-plot-canvas" tabindex="0" role="region" aria-label="Radial ${quantity==='E'?'electric-field':'potential'} graph. Scroll horizontally on small screens.">${shellSVG(m,quantity)}</div><p class="chapter23-plot-scroll-note">Scroll across the graph to keep its labels readable.</p><figcaption>${quantity==='E'?'<p>The open circles are one-sided field limits, not a continuous vertical field segment. Each shell adds a jump ΔE = kq/R². Between surfaces, fixed enclosed charge gives E ∝ 1/r².</p>':'<p>Both shell potentials add. Inside each shell its contribution is constant kq/R, not zero. The potential remains continuous at both radii; its slope changes because E = −dV/dr.</p>'}<p>The horizontal scale is fixed at 0–4R₂; both curves approach zero beyond the displayed interval as r tends to infinity. See the worked steps for exact boundary values.</p></figcaption></figure>`;
  }
  if(!p?.answerAudit?.chapterStudyVerified||!Number.isInteger(def?.fieldIndex)||!p.finalRules?.some(r=>r.fieldIndex===def.fieldIndex))return '';
  const m=model(def);if(!m)return '';
  const cylinder=m.type==='cylinder-shell';
  return `<figure class="chapter23-solution-plot"><h4>${cylinder?'Part C · Sketch E against distance':'Part E · Sketch E against distance'}</h4><div class="chapter23-plot-canvas" tabindex="0" role="region" aria-label="Electric-field graph. Scroll horizontally on a small screen.">${plotSVG(m)}</div><p class="chapter23-plot-scroll-note">Scroll across the graph to keep its labels readable.</p><figcaption>${cylinder?`<p><b>Inside:</b> a cylindrical Gaussian surface encloses no charge, so E = 0. <b>Outside:</b> E = λ/(2πε₀r), so doubling r halves the field.</p><p>The open circles show different one-sided limits at the ideal charged surface. E(R) itself is undefined in this ideal surface-charge model; do not join those circles with a vertical field curve.</p>`:`<p><b>Inside:</b> Q<sub>enc</sub> = πρ₀r⁴/R, so Gauss’s law gives E = ρ₀r²/(4ε₀R). <b>Outside:</b> the enclosed total charge stays fixed, so E = Q/(4πε₀r²).</p><p>The two curves meet continuously at r = R. This is the maximum; at 3R the field is one ninth of that maximum.</p>`}</figcaption></figure>`;
 }
 return {solution,model,plotSVG,shellSVG,kinematicModel,kinematicSVG,vectorModel,vectorSVG};
})();
