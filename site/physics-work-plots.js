/* Typed, fixed-scale work/energy constructions; not a motion simulation. */
(function(){
 'use strict';
 const finite=Number.isFinite,DEG=Math.PI/180;
 const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
 const range=a=>Array.isArray(a)&&a.length===2&&a.every(finite)&&a[1]>a[0]&&finite(1/(a[1]-a[0]));
 const near=(a,b)=>Math.abs(a-b)<=1e-8*Math.max(1,Math.abs(a),Math.abs(b));
 function model(d){
  if(d?.kind==='energy-ledger'){
   if(!Number.isInteger(d.fieldIndex)||d.fieldIndex<0||!finite(d.workIn)||!finite(d.workOut)||d.workIn<0||d.workOut<0||!Array.isArray(d.stores)||d.stores.length<1||d.stores.length>4||d.stores.some(s=>!s||typeof s.label!=='string'||s.label.length>35||!finite(s.value)||Math.abs(s.value)>180))return null;
   const net=d.workIn-d.workOut,sum=d.stores.reduce((v,s)=>v+s.value,0);
   return finite(net)&&finite(sum)&&near(net,sum)?{...d,ledger:true,net,sum}:null;
  }
  if(!d||!Number.isInteger(d.fieldIndex)||d.fieldIndex<0||!range(d.xRange)||!range(d.yRange)||!['N','J','m/s','ratio'].includes(d.yUnit)||!Array.isArray(d.curves)||!d.curves.length||d.curves.length>3)return null;
  const curves=[];
  for(const c of d.curves){
   if(!c||!range(c.domain)||c.domain[0]<d.xRange[0]||c.domain[1]>d.xRange[1]||['openStart','openEnd'].some(k=>c[k]!==undefined&&typeof c[k]!=='boolean'))return null;
   let limit,primitive,integralCore,critical=[];
   if(c.kind==='polynomial'){
    const a=c.coefficients;if(!Array.isArray(a)||!a.length||a.length>4||!a.every(finite)||d.yUnit==='m/s')return null;
    limit=x=>a.reduceRight((v,k)=>v*x+k,0);primitive=x=>a.reduce((v,k,i)=>v+k*x**(i+1)/(i+1),0);
    const A=3*(a[3]||0),B=2*(a[2]||0),C=a[1]||0;
    if(A){const disc=B*B-4*A*C;if(!finite(disc))return null;if(disc>=0)critical=[(-B-Math.sqrt(disc))/(2*A),(-B+Math.sqrt(disc))/(2*A)];}
    else if(B)critical=[-C/B];
   }else if(c.kind==='exponential'){
    if(!finite(c.amplitude)||!finite(c.rate)||d.yUnit!=='N')return null;
    limit=x=>c.amplitude*Math.exp(c.rate*x);integralCore=(a,b)=>c.rate===0?c.amplitude*(b-a):c.amplitude*Math.exp(c.rate*a)*(Math.expm1(c.rate*(b-a))/c.rate);
   }else if(c.kind==='affine-exponential'){
    if(![c.intercept,c.slope,c.rate].every(finite)||!['N','J'].includes(d.yUnit))return null;
    limit=x=>(c.intercept+c.slope*x)*Math.exp(c.rate*x);
    if(c.rate&&c.slope)critical=[-(c.slope+c.rate*c.intercept)/(c.rate*c.slope)];
    integralCore=(a,b)=>{
     const h=b-a,z=c.rate*h,base=c.intercept+c.slope*a;let i0,i1;
     if(Math.abs(z)<.01){let p=1,s0=1,s1=.5;for(let n=1;n<=20;n++){p*=z/n;s0+=p/(n+1);s1+=p/(n+2);}i0=h*s0;i1=h*h*s1;}
     else{i0=h*Math.expm1(z)/z;i1=h*h*((z-1)*Math.expm1(z)+z)/(z*z);}
     return Math.exp(c.rate*a)*(base*i0+c.slope*i1);
    };
   }else if(c.kind==='piecewise-linear'){
    const ps=c.vertices;
    if(!Array.isArray(ps)||ps.length<2||ps.length>60||ps.some((p,i)=>!Array.isArray(p)||p.length!==2||!p.every(finite)||(i&&p[0]<=ps[i-1][0]))||ps[0][0]!==c.domain[0]||ps.at(-1)[0]!==c.domain[1]||!['N','J','ratio'].includes(d.yUnit))return null;
    limit=x=>{const i=Math.max(0,ps.findIndex((p,i)=>i<ps.length-1&&x>=p[0]&&x<=ps[i+1][0]));const[a,b]=[ps[i],ps[i+1]];return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]);};
    critical=ps.slice(1,-1).map(p=>p[0]);
    integralCore=(a,b)=>{const stops=[a,...critical.filter(x=>x>a&&x<b),b];return stops.slice(1).reduce((v,x,i)=>v+(x-stops[i])*(limit(stops[i])+limit(x))/2,0);};
   }else if(c.kind==='bezier-potential'){
    if(!['potential','kinetic','force'].includes(c.output)||!Array.isArray(c.segments)||!c.segments.length||c.segments.length>8||!Array.isArray(c.origin)||c.origin.length!==2||!c.origin.every(finite)||!Array.isArray(c.scale)||c.scale.length!==2||!c.scale.every(v=>finite(v)&&v>0)||d.yUnit!==(c.output==='force'?'N':'J')||(c.output==='kinetic'&&!finite(c.energy)))return null;
    const pieces=c.segments.map(s=>Array.isArray(s)&&s.length===4?s.map(p=>Array.isArray(p)&&p.length===2&&p.every(finite)?[(p[0]-c.origin[0])/c.scale[0],(p[1]-c.origin[1])/c.scale[1]]:null):null);
    if(pieces.some((s,i)=>!s||s.some(p=>!p||!p.every(finite))||s.some((p,j)=>j&&p[0]<=s[j-1][0])||(i&&(!near(s[0][0],pieces[i-1][3][0])||!near(s[0][1],pieces[i-1][3][1])))))return null;
    if(c.domain[0]<pieces[0][0][0]||c.domain[1]>pieces.at(-1)[3][0])return null;
    const at=(p,t,k)=>{const u=1-t;return u*u*u*p[0][k]+3*u*u*t*p[1][k]+3*u*t*t*p[2][k]+t*t*t*p[3][k];};
    const deriv=(p,t,k)=>3*((1-t)**2*(p[1][k]-p[0][k])+2*(1-t)*t*(p[2][k]-p[1][k])+t*t*(p[3][k]-p[2][k]));
    limit=x=>{const p=pieces.find(s=>x>=s[0][0]-1e-12&&x<=s[3][0]+1e-12);if(!p)return NaN;let lo=0,hi=1;for(let i=0;i<60;i++){const t=(lo+hi)/2;if(at(p,t,0)<x)lo=t;else hi=t;}const t=(lo+hi)/2,U=at(p,t,1);return c.output==='force'?-deriv(p,t,1)/deriv(p,t,0):c.output==='kinetic'?c.energy-U:U;};
    // Artwork is a calibrated graphical trace, not an asserted exact U formula.
    // Analytic parameter extrema protect scales, including extrema of -U'/x'.
    const roots=(A,B,C)=>{if(![A,B,C].every(finite))return null;if(!A)return B?[-C/B]:[];const disc=B*B-4*A*C;if(!finite(disc))return null;if(disc<0)return [];const q=-.5*(B+(B<0?-1:1)*Math.sqrt(disc));return q?[q/A,C/q]:[-B/(2*A)];};
    for(const p of pieces){
     const coeff=k=>[3*(p[1][k]-p[0][k]),6*(p[2][k]-2*p[1][k]+p[0][k]),3*(p[3][k]-3*p[2][k]+3*p[1][k]-p[0][k])];
     const[a,b,h]=coeff(0),[d,e,f]=coeff(1),ts=c.output==='force'?roots(f*b-e*h,2*(f*a-d*h),e*a-d*b):roots(f,e,d);
     if(!ts)return null;
     critical.push(p[0][0],p[3][0],...ts.filter(t=>t>0&&t<1).map(t=>at(p,t,0)));
    }
   }else if(c.kind==='inverse-square'){
    if(!finite(c.coefficient)||c.domain[0]<=0||d.yUnit!=='N')return null;
    limit=x=>c.coefficient/x**2;integralCore=(a,b)=>c.coefficient*((b-a)/a)/b;
   }else if(c.kind==='sqrt-cosine'){
    if(!finite(c.constant)||!finite(c.coefficient)||c.domain[0]<0||c.domain[1]>90||d.yUnit!=='m/s')return null;
    const radicand=x=>c.constant+c.coefficient*Math.cos(x*DEG);
    if([c.domain[0],c.domain[1]].some(x=>radicand(x)<-1e-12))return null;
    limit=x=>{const q=radicand(x);return q>=-1e-12?Math.sqrt(Math.max(0,Math.abs(q)<1e-14?0:q)):NaN;};
   }else return null;
   const candidates=[...c.domain,...critical.filter(x=>x>c.domain[0]&&x<c.domain[1])],extrema=candidates.map(limit);
   if(extrema.some(v=>!finite(v)||v<d.yRange[0]-1e-9||v>d.yRange[1]+1e-9))return null;
   const points=Array.from({length:361},(_,i)=>{const x=c.domain[0]+(c.domain[1]-c.domain[0])*i/360;return [x,limit(x)];});
   for(const x of critical.filter(x=>x>c.domain[0]&&x<c.domain[1]))points.push([x,limit(x)]);
   points.sort((a,b)=>a[0]-b[0]);if(points.some(p=>!p.every(finite)))return null;
   const value=x=>finite(x)&&x>=c.domain[0]&&x<=c.domain[1]&&!(c.openStart&&x===c.domain[0])&&!(c.openEnd&&x===c.domain[1])?limit(x):null;
   const integral=(primitive||integralCore)?(a,b)=>{if(!finite(a)||!finite(b)||a<c.domain[0]||b>c.domain[1]||b<a)return null;const area=integralCore?integralCore(a,b):primitive(b)-primitive(a);return finite(area)?area:null;}:null;
   curves.push({...c,value,limit,integral,critical,points});
  }
  if(d.points!==undefined&&!Array.isArray(d.points)||d.shades!==undefined&&!Array.isArray(d.shades))return null;
  const points=d.points||[],shades=[];
  for(const p of points){if(!p||!Number.isInteger(p.curveIndex)||!curves[p.curveIndex]||!finite(p.x)||!finite(p.y)||p.x<d.xRange[0]||p.x>d.xRange[1]||p.y<d.yRange[0]||p.y>d.yRange[1])return null;const v=curves[p.curveIndex].value(p.x);if(v===null||!near(v,p.y))return null;}
  if((d.shades||[]).length>4)return null;
  for(const s of d.shades||[]){
   const c=curves[s?.curveIndex];if(!s||!Number.isInteger(s.curveIndex)||!c?.integral||!['N','ratio'].includes(d.yUnit)||d.yRange[0]>0||d.yRange[1]<0||!range(s.domain)||s.domain[0]<c.domain[0]||s.domain[1]>c.domain[1])return null;
   const checks=[...s.domain,...c.critical.filter(x=>x>s.domain[0]&&x<s.domain[1])].map(c.limit);
   if(Math.min(...checks)<-1e-10&&Math.max(...checks)>1e-10)return null; // Split signed areas at a zero.
   const area=c.integral(...s.domain);if(!finite(area))return null;
   const polygon=Array.from({length:181},(_,i)=>{const x=s.domain[0]+(s.domain[1]-s.domain[0])*i/180;return [x,c.limit(x)];});
   shades.push({...s,area,negative:area<0,polygon});
  }
  const x=v=>85+(v-d.xRange[0])*625/(d.xRange[1]-d.xRange[0]),y=v=>385-(v-d.yRange[0])*320/(d.yRange[1]-d.yRange[0]);
  if(![x(d.xRange[1]),y(d.yRange[1])].every(finite))return null;
  const openEndpoints=curves.flatMap((c,i)=>[...(c.openStart?[{x:c.domain[0],y:c.limit(c.domain[0]),curveIndex:i}]:[]),...(c.openEnd?[{x:c.domain[1],y:c.limit(c.domain[1]),curveIndex:i}]:[])]);
  return {...d,curves,points,shades,x,y,openEndpoints};
 }
 function svg(m){
  if(!m)return '';
  if(m.ledger){
   const paint=(r,a)=>`class="pwp-${r}" ${a}="${{ink:'#3c4645',first:'#cf5948',second:'#267780',axis:'#83928e',paper:'#fffdf7'}[r]}"`,fmt=v=>(v>0?'+':'')+Number(v.toPrecision(6));
   return `<svg class="pwp-svg" viewBox="0 0 760 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(m.title)}"><title>${esc(m.title)}</title><desc>${esc(m.caption)} Signed store bars use one pixel per joule. Work arrows show direction only.</desc><rect width="760" height="560" ${paint('paper','fill')}/><g font-family="Arial, sans-serif" font-size="16"><rect x="170" y="85" width="420" height="310" rx="10" fill="none" ${paint('axis','stroke')}/><text x="380" y="55" text-anchor="middle" ${paint('ink','fill')}>SYSTEM ENERGY STATEMENT</text><path d="M30 210H155l-14-9m14 9-14 9M600 210H730l-14-9m14 9-14 9" fill="none" stroke-width="3" ${paint('first','stroke')}/><text x="22" y="182" ${paint('ink','fill')}>Work IN ${esc(m.workIn)} J</text><text x="597" y="182" ${paint('ink','fill')}>OUT ${esc(m.workOut)} J</text>${m.stores.map((s,i)=>{const y=128+i*65;return `<text x="192" y="${y}" ${paint('ink','fill')}>${esc(s.label)} = ${esc(fmt(s.value))} J</text><path d="M380 ${y+8}v20" ${paint('axis','stroke')}/><rect x="${380+Math.min(0,s.value)}" y="${y+12}" width="${Math.abs(s.value)}" height="12" ${paint(s.value<0?'second':'first','fill')}/>`;}).join('')}<text x="380" y="432" text-anchor="middle" ${paint('ink','fill')}>Net work = ${esc(m.workIn)} − ${esc(m.workOut)} = ${esc(m.net)} J</text><text x="380" y="463" text-anchor="middle" ${paint('ink','fill')}>Sum of store changes = ${esc(m.stores.map(s=>fmt(s.value)).join(' '))} = ${esc(m.sum)} J</text><text x="380" y="503" font-size="13" text-anchor="middle" ${paint('ink','fill')}>Bars: 1 px/J about their zero marks; arrows indicate transfer direction only.</text><text x="380" y="530" font-size="13" text-anchor="middle" ${paint('ink','fill')}>A negative store change releases energy; thermal increase is not missing energy.</text></g></svg>`;
  }
  const palette={ink:'#3c4645',grid:'#d9ded9',axis:'#83928e',first:'#cf5948',second:'#267780',third:'#8054a1',paper:'#fffdf7'},roles=['first','second','third'];
  const role=(r,a)=>`class="pwp-${r}" ${a}="${palette[r]}"`,x=m.x,y=m.y,fmt=v=>Number(v.toPrecision(4)).toString();
  const path=ps=>'M'+ps.map(p=>`${x(p[0]).toFixed(3)},${y(p[1]).toFixed(3)}`).join('L');
  const grid=Array.from({length:5},(_,i)=>{const xv=m.xRange[0]+(m.xRange[1]-m.xRange[0])*i/4,yv=m.yRange[0]+(m.yRange[1]-m.yRange[0])*i/4;return `<path ${role('grid','stroke')} fill="none" d="M85 ${y(yv)}H710M${x(xv)} 65V385"/><text x="73" y="${y(yv)+5}" text-anchor="end">${esc(fmt(yv))}</text><text x="${x(xv)}" y="413" text-anchor="middle">${esc(fmt(xv))}</text>`;}).join('');
  const shading=m.shades.map(s=>`<path ${role(s.negative?'second':'first','fill')} opacity="0.13" d="M${x(s.domain[0])},${y(0)}L${s.polygon.map(p=>`${x(p[0])},${y(p[1])}`).join('L')}L${x(s.domain[1])},${y(0)}Z"/>`).join('');
  const curves=m.curves.map((c,i)=>`<path ${role(roles[i],'stroke')} fill="none" stroke-width="3" ${i?'stroke-dasharray="'+(i===1?'10 5':'3 5')+'"':''} d="${path(c.points)}"/>`).join('');
  const occupied=[],samples=m.curves.flatMap(c=>c.points.map(p=>[x(p[0]),y(p[1])]));
  function label(text,px,py){
   if(!text)return '';
   // Conservative Arial14 glyph bounds: an average-character estimate missed
   // the wide M/m glyphs and let a descending curve cross a label's last letters.
   const width=Math.min(580,8+[...String(text)].reduce((n,ch)=>n+(/[MW@]/.test(ch)?14:/[mw]/.test(ch)?12:/[ilI1.,:;!|]/.test(ch)?4.5:/\s/.test(ch)?4.5:/[A-Z]/.test(ch)?10.5:8.5),0)),candidates=[];
   for(const dy of [-18,25,-38,45,-58,65])for(const dx of [10,-10,40,-40,70,-70])for(const anchor of ['start','end','middle']){
    const tx=px+dx,ty=py+dy,box={left:tx-(anchor==='end'?width:anchor==='middle'?width/2:0),right:tx+(anchor==='start'?width:anchor==='middle'?width/2:0),top:ty-14,bottom:ty+4};
    if(box.left<89||box.right>706||box.top<69||box.bottom>381)continue;
    const hits=samples.filter(([a,b])=>a>box.left-3&&a<box.right+3&&b>box.top-3&&b<box.bottom+3).length,overlaps=occupied.filter(b=>box.left<b.right+5&&box.right>b.left-5&&box.top<b.bottom+5&&box.bottom>b.top-5).length;
    candidates.push({tx,ty,anchor,box,score:hits+overlaps*1000+(Math.abs(dy)+Math.abs(dx))/1000});
   }
   candidates.sort((a,b)=>a.score-b.score);const p=candidates[0];if(!p)return '';occupied.push(p.box);return `<text x="${p.tx}" y="${p.ty}" text-anchor="${p.anchor}" font-size="14">${esc(text)}</text>`;
  }
  const points=m.points.map(p=>`<circle ${role(roles[p.curveIndex],'fill')} cx="${x(p.x)}" cy="${y(p.y)}" r="4"/>${label(p.label,x(p.x),y(p.y))}`).join('');
  const areaLabels=m.shades.map(s=>{const mid=(s.domain[0]+s.domain[1])/2,cy=y(m.curves[s.curveIndex].limit(mid)/2);return label(s.label,x(mid),cy);}).join('');
  const open=m.openEndpoints.map(p=>`<circle class="pwp-open-${roles[p.curveIndex]}" fill="${palette.paper}" stroke="${palette[roles[p.curveIndex]]}" cx="${x(p.x)}" cy="${y(p.y)}" r="5" stroke-width="2"/>`).join('');
  // Explicit paint attributes are required: global dark SVG text rules otherwise win.
  return (`<svg class="pwp-svg" viewBox="0 0 760 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(m.title)}"><title>${esc(m.title)}</title><desc>${esc(m.caption)} Fixed reference scales; only stated function domains are drawn.</desc><rect width="760" height="560" ${role('paper','fill')}/><g font-family="Arial, sans-serif" font-size="15">${shading}${grid}<path ${role('axis','stroke')} fill="none" d="M85 65V385H710${m.yRange[0]<=0&&m.yRange[1]>=0?'M85 '+y(0)+'H710':''}"/>${curves}${points}${areaLabels}${open}<text x="85" y="28" font-size="17">${esc(m.yLabel)}</text><text x="710" y="445" text-anchor="end" font-size="17">${esc(m.xLabel)}</text>${m.curves.map((c,i)=>`<path ${role(roles[i],'stroke')} fill="none" stroke-width="3" ${i?'stroke-dasharray="'+(i===1?'10 5':'3 5')+'"':''} d="M85 ${465+i*27}h35"/><text x="132" y="${470+i*27}" font-size="14">${esc(c.label)}</text>`).join('')}${m.openEndpoints.length?'<text x="85" y="550" font-size="13">Open circle: limiting value, not an attained traversal endpoint.</text>':''}</g></svg>`).replace(/<text /g,`<text ${role('ink','fill')} `);
 }
 window.PhysicsWorkPlots={model,svg};
})();
