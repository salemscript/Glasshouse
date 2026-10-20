/* Equation-driven Chapter 6 constructions. Fixed scales; no simulated control claim. */
(function () {
 'use strict';
 const DEG=Math.PI/180, finite=Number.isFinite;
 const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
 const range=a=>Array.isArray(a)&&a.length===2&&a.every(finite)&&a[1]>a[0]&&finite(1/(a[1]-a[0]));
 function model(d) {
  if(!d||typeof d!=='object'||!Number.isInteger(d.fieldIndex)||d.fieldIndex<0||!range(d.xRange)||!range(d.yRange)||d.xRange[0]<0||d.xRange[1]>90||d.yRange[0]!==0||d.yRange[1]<=0||!Array.isArray(d.curves)||d.curves.length<1||d.curves.length>3)return null;
  const kinds=d.curves.map(c=>c&&c.kind),kind=kinds[0];
  if(!['banked-turn-speed','friction-push-threshold'].includes(kind)||kinds.some(k=>k!==kind)||kind==='friction-push-threshold'&&d.curves.length!==1||d.yUnit!==(kind==='banked-turn-speed'?'m/s':'ratio'))return null;
  const curves=[];
  for(const c of d.curves){
   if(!c||typeof c!=='object'||!finite(c.coefficient)||c.coefficient<0||!range(c.domain)||c.domain[0]<d.xRange[0]||c.domain[1]>d.xRange[1])return null;
   const mu=c.coefficient,criticalAngle=Math.atan2(1,mu)/DEG,banked=kind==='banked-turn-speed';
   if(banked&&(!finite(c.radius)||!finite(c.gravity)||c.radius<=0||c.gravity<=0||!finite(c.radius*c.gravity)||c.domain[1]>=criticalAngle))return null;
   const physicalEnd=Math.min(c.domain[1],criticalAngle),openEnd=physicalEnd===criticalAngle,pole=mu>0&&openEnd;
   if(c.domain[0]>=physicalEnd)return null;
   const value=theta=>{
    if(!finite(theta)||theta<c.domain[0]||theta>c.domain[1]||theta>=criticalAngle)return null;
    const t=theta*DEG,den=Math.cos(t)-mu*Math.sin(t);
    const v=banked?Math.sqrt(c.radius*c.gravity*(Math.sin(t)+mu*Math.cos(t))/den):mu/den;
    return finite(v)&&v>=0?v:null;
   };
   const initial=value(c.domain[0]);
   if(initial===null||initial>=d.yRange[1])return null;
   let visibleEnd=physicalEnd,clipped=false;
   const end=openEnd?null:value(physicalEnd);
   if(pole||end!==null&&end>d.yRange[1]){
    const ymax=d.yRange[1];
    visibleEnd=(banked?Math.atan((ymax/Math.sqrt(c.radius*c.gravity))**2)-Math.atan(mu):Math.acos(mu/(ymax*Math.hypot(1,mu)))-Math.atan(mu))/DEG;
    if(!finite(visibleEnd)||visibleEnd<=c.domain[0]||visibleEnd>=physicalEnd)return null;
    clipped=true;
   }
   // A zero-friction push has q=0 up to, but not at, a purely vertical push.
   const sampleEnd=openEnd&&!clipped?physicalEnd-1e-9:visibleEnd;
   const points=Array.from({length:361},(_,i)=>{const x=c.domain[0]+(sampleEnd-c.domain[0])*i/360;return [x,i===360&&clipped?d.yRange[1]:value(x)];});
   if(points.some(p=>!p.every(finite)))return null;
   curves.push({...c,value,criticalAngle,pole,openEnd,physicalDomain:[c.domain[0],physicalEnd],visibleEnd,clipped,points});
  }
  if(d.points!==undefined&&!Array.isArray(d.points))return null;
  const points=d.points||[];
  for(const p of points){
   if(!p||!Number.isInteger(p.curveIndex)||!curves[p.curveIndex]||!finite(p.x)||!finite(p.y)||p.x<d.xRange[0]||p.x>d.xRange[1]||p.y<0||p.y>d.yRange[1])return null;
   const v=curves[p.curveIndex].value(p.x);
   if(v===null||Math.abs(v-p.y)>1e-8*Math.max(1,Math.abs(v),Math.abs(p.y)))return null;
  }
  const x=v=>85+(v-d.xRange[0])*625/(d.xRange[1]-d.xRange[0]),y=v=>385-v*320/d.yRange[1];
  if(![x(d.xRange[0]),x(d.xRange[1]),y(d.yRange[1])].every(finite))return null;
  return {...d,curves,points,x,y};
 }
 function svg(m){
  if(!m)return '';
  const palette={ink:'#3c4645',grid:'#d9ded9',axis:'#83928e',first:'#cf5948',second:'#267780',third:'#8054a1',paper:'#fffdf7',region:'#edf0ea'};
  const role=(r,a)=>`class="pfc-${r}" ${a}="${palette[r]}"`;
  const fmt=v=>Number(v.toPrecision(4)).toString(),x=m.x,y=m.y;
  const roles=['first','second','third'];
  const grid=Array.from({length:5},(_,i)=>{const xv=m.xRange[0]+(m.xRange[1]-m.xRange[0])*i/4,yv=m.yRange[1]*i/4;return `<path ${role('grid','stroke')} fill="none" d="M85 ${y(yv)}H710M${x(xv)} 65V385"/><text x="73" y="${y(yv)+5}" text-anchor="end">${esc(fmt(yv))}</text><text x="${x(xv)}" y="413" text-anchor="middle">${esc(fmt(xv))}</text>`;}).join('');
  const threshold=m.curves[0].kind==='friction-push-threshold',c=m.curves[0],critical=c.criticalAngle;
  const forbidden=threshold&&critical<m.xRange[1]?`<rect x="${x(critical)}" y="65" width="${710-x(critical)}" height="320" ${role('region','fill')}/>${710-x(critical)>130?`<text x="${(x(critical)+710)/2}" y="225" text-anchor="middle" font-size="13">No finite force</text><text x="${(x(critical)+710)/2}" y="245" text-anchor="middle" font-size="13">initiates sliding</text>`:''}`:'';
  const asymptote=threshold&&c.pole?`<path ${role('axis','stroke')} fill="none" stroke-dasharray="5 5" d="M${x(critical)} 65V385"/><text x="${x(critical)+(710-x(critical)>160?8:-8)}" y="54" text-anchor="${710-x(critical)>160?'start':'end'}" font-size="13">θcrit = ${esc(fmt(critical))}°</text>`:'';
  const paths=m.curves.map((curve,i)=>`<path ${role(roles[i],'stroke')} fill="none" stroke-width="3" ${i===1?'stroke-dasharray="10 5"':''} d="M${curve.points.map(p=>`${x(p[0]).toFixed(3)},${y(p[1]).toFixed(3)}`).join('L')}"/>${curve.clipped?`<path ${role(roles[i],'stroke')} fill="none" stroke-width="3" d="M${x(curve.visibleEnd)-5} 74L${x(curve.visibleEnd)} 65L${x(curve.visibleEnd)+5} 74"/>`:''}${curve.openEnd&&!curve.pole&&!curve.clipped?`<circle ${role(roles[i],'stroke')} fill="none" cx="${x(curve.physicalDomain[1])}" cy="${y(0)}" r="4" stroke-width="2"/>`:''}`).join('');
  const markers=m.points.map(p=>`<circle ${role(roles[p.curveIndex],'fill')} cx="${x(p.x)}" cy="${y(p.y)}" r="4"/><text x="${x(p.x)+(x(p.x)>530?-8:8)}" y="${y(p.y)-11}" text-anchor="${x(p.x)>530?'end':'start'}" font-size="13">${esc(p.label)}</text>`).join('');
  const legends=m.curves.map((curve,i)=>`<path ${role(roles[i],'stroke')} fill="none" stroke-width="3" ${i===1?'stroke-dasharray="10 5"':''} d="M85 ${465+i*27}h35"/><text x="132" y="${470+i*27}" font-size="14">${esc(curve.label)}</text>`).join('');
  return (`<svg class="pfc-svg" viewBox="0 0 760 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(m.title)}"><title>${esc(m.title)}</title><desc>${esc(m.caption)} Fixed reference axes; only physical branches are shown.</desc><rect width="760" height="560" ${role('paper','fill')}/><g font-family="Arial, sans-serif" font-size="15">${forbidden}${grid}<path ${role('axis','stroke')} fill="none" d="M85 65V385H710"/>${asymptote}${paths}${markers}<text x="85" y="28" font-size="17">${esc(m.yLabel)}</text><text x="710" y="445" text-anchor="end" font-size="17">${esc(m.xLabel)}</text>${legends}${m.curves.some(v=>v.clipped)?'<text x="85" y="550" font-size="13">↑ Curve continues above the fixed vertical scale.</text>':''}</g></svg>`).replace(/<text /g,`<text ${role('ink','fill')} `);
 }
 window.PhysicsForceCurves={model,svg};
})();
