/* Original mathematical3D vector constructions; fixed orthographic projection. */
(()=>{'use strict';
 const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const finite=v=>typeof v==='number'&&Number.isFinite(v),triple=v=>Array.isArray(v)&&v.length===3&&v.every(finite);
 const project=p=>[(p[0]-p[1])/Math.sqrt(2),(p[0]+p[1]-2*p[2])/Math.sqrt(6)];
 function model(d){
  if(!d||!Number.isInteger(d.fieldIndex)||d.fieldIndex<0||!Array.isArray(d.arrows)||d.arrows.length<1||d.arrows.length>30)return null;
  const ranges=['xRange','yRange','zRange'].map(k=>d[k]);
  if(ranges.some(r=>!Array.isArray(r)||r.length!==2||!r.every(finite)||r[0]>0||r[1]<=0||r[0]>=r[1]))return null;
  const inside=p=>triple(p)&&p.every((v,i)=>v>=ranges[i][0]&&v<=ranges[i][1]);
  if(d.arrows.some(v=>!inside(v?.from)||!inside(v?.to)||!['given','resultant','component'].includes(v.role)))return null;
  const points=d.points||[];if(!Array.isArray(points)||points.length>30||points.some(p=>!inside(p.position)))return null;
  const corners=[];for(const x of ranges[0])for(const y of ranges[1])for(const z of ranges[2])corners.push(project([x,y,z]));
  const minX=Math.min(...corners.map(p=>p[0])),maxX=Math.max(...corners.map(p=>p[0])),minY=Math.min(...corners.map(p=>p[1])),maxY=Math.max(...corners.map(p=>p[1]));
  const scale=Math.min(570/(maxX-minX),350/(maxY-minY));if(!finite(scale)||scale<=0)return null;
  const tx=380-scale*(minX+maxX)/2,ty=240-scale*(minY+maxY)/2;
  const pixel=p=>{const q=project(p);return [tx+scale*q[0],ty+scale*q[1]];};
  const arrows=d.arrows.map(v=>{const delta=v.to.map((x,i)=>x-v.from[i]),norm=Math.hypot(...delta),projection=project(delta),fromPixel=pixel(v.from),toPixel=pixel(v.to);return {...v,delta,norm,zero:norm===0,viewAligned:norm>0&&Math.hypot(...projection)/norm<=16*Number.EPSILON,fromPixel,toPixel};});
  return {type:'vectors3d',title:String(d.title||'Right-handed3D vector construction'),caption:String(d.caption||''),unit:String(d.unit||'m'),fieldIndex:d.fieldIndex,ranges,arrows,points,pixel,scale,project};
 }
 function svg(m){
  if(!m||m.type!=='vectors3d')return '';
  const used=[],segments=m.arrows.map(a=>[...a.fromPixel,...a.toPixel]);
  const color=role=>role==='component'?'#899a93':role==='resultant'?'#4d918b':'#d96556';
  function label(text,x,y){
   if(!text)return '';const value=String(text),w=Math.min(350,value.length*6.4+12),h=19;
   const candidates=[[14,-17],[-14,-17],[14,23],[-14,23],[0,-36],[0,43]];
   const distance=(px,py,s)=>{const dx=s[2]-s[0],dy=s[3]-s[1],n=dx*dx+dy*dy,t=n?Math.max(0,Math.min(1,((px-s[0])*dx+(py-s[1])*dy)/n)):0;return Math.hypot(px-s[0]-t*dx,py-s[1]-t*dy);};
   const choices=candidates.map(([dx,dy])=>{let cx=Math.max(40+w/2,Math.min(720-w/2,x+dx)),cy=Math.max(37,Math.min(437,y+dy));const rect=[cx-w/2,cy-14,w,h];let score=used.reduce((s,r)=>s+(rect[0]<r[0]+r[2]&&rect[0]+w>r[0]&&rect[1]<r[1]+r[3]&&rect[1]+h>r[1]?100:0),0);score+=segments.reduce((s,v)=>s+(distance(cx,cy-5,v)<14?15:0),0);return {cx,cy,rect,score};});choices.sort((a,b)=>a.score-b.score);const p=choices[0];used.push(p.rect);return `<text x="${p.cx}" y="${p.cy}" text-anchor="middle" class="pv3d-label">${esc(value)}</text>`;
  }
  const line=(from,to,role,head=true)=>{const[x1,y1]=from,[x2,y2]=to,dx=x2-x1,dy=y2-y1,len=Math.hypot(dx,dy),ux=len?dx/len:0,uy=len?dy/len:0,h=Math.min(10,len*.3),b=h*.42;return `<g class="pv3d-arrow pv3d-${role}" stroke="${color(role)}" fill="${color(role)}"${role==='component'?' stroke-dasharray="6 4"':''}><path d="M${x1} ${y1}L${x2} ${y2}" fill="none"/>${head&&len?`<path d="M${x2} ${y2}L${x2-h*ux+b*uy} ${y2-h*uy-b*ux}L${x2-h*ux-b*uy} ${y2-h*uy+b*ux}Z" stroke="none"/>`:''}</g>`;};
  const zero=m.pixel([0,0,0]);let axes='',labels='';
  for(let i=0;i<3;i++){
   const lo=[0,0,0],hi=[0,0,0];lo[i]=m.ranges[i][0];hi[i]=m.ranges[i][1];axes+=line(m.pixel(lo),m.pixel(hi),'axis');const end=m.pixel(hi);labels+=label('+'+'xyz'[i],end[0],end[1]);
   const one=[0,0,0];one[i]=1;if(one[i]<=m.ranges[i][1]){const p=m.pixel(one);axes+=`<circle cx="${p[0]}" cy="${p[1]}" r="2" class="pv3d-unit"/>`;}
  }
  const arrows=m.arrows.map(a=>{
   const[x1,y1]=a.fromPixel,[x2,y2]=a.toPixel;labels+=label(a.label+(a.zero?' (zero vector)':a.viewAligned?' (view-aligned)':''),(x1+x2)/2,(y1+y2)/2);
   if(a.zero||a.viewAligned)return `<circle cx="${x1}" cy="${y1}" r="${a.zero?4:6}" class="pv3d-${a.zero?'zero':'view-aligned'} pv3d-${a.role}" stroke="${color(a.role)}" fill="${a.zero?color(a.role):'none'}"><title>${esc(a.zero?'Zero vector; no direction.':'Nonzero vector parallel to viewing direction; projected length vanishes.')}</title></circle>`;
   return `<g data-norm-3d="${a.norm}">${line(a.fromPixel,a.toPixel,a.role)}</g>`;
  }).join('');
  const dots=m.points.map(p=>{const q=m.pixel(p.position);labels+=label(p.label,q[0],q[1]);return `<circle cx="${q[0]}" cy="${q[1]}" r="3" class="pv3d-point"/>`;}).join('');
  const desc='Right-handed coordinates: î cross ĵ equals k̂. Fixed orthographic projection; one 3D unit has the same projected length on all three coordinate axes. Arbitrary 3D lengths and angles are foreshortened; do not measure them from the page. Positive unit-axis dots mark 1 '+m.unit+'.';
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 535" role="img" aria-label="${esc(m.title+'. '+m.caption+'. '+desc)}"><title>${esc(m.title)}</title><desc>${esc(desc)}</desc><g class="pv3d-drawing" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${axes}${arrows}${dots}</g><g class="pv3d-text" fill="#535c59" font-family="system-ui,sans-serif" font-size="13">${labels}<text x="${zero[0]-8}" y="${zero[1]+19}" text-anchor="end">O</text><text x="45" y="477">Right-handed 3D coordinates · same physical unit on each axis</text><text x="45" y="500">Orthographic view: projected lengths/angles are foreshortened.</text><text x="45" y="521">Axis dots mark 1 ${esc(m.unit)}; vector components determine actual length.</text></g></svg>`;
 }
 window.PhysicsVector3D={model,svg};
})();
