/* Glasshouse · original parameter-response plots. Sample existing teaching laws,
   never a second physics model. Marker values are exact predictions, not a fit. */
window.Physics2ResponseGraph=(()=>{
 'use strict';
 const K=window.GlassPhysicsKit,esc=K.esc,cache=new Map(),N=61;
 const timeDependentSections=['24.4','26.1','28.7','28.8','30.1','30.6','30.7'];
 const discreteSections=['21.2','21.3','36.6'];
 const choices={
  '21.1':'distance','21.2':'electrons','21.3':'transfer',
  '22.1':'probe','22.2':'radius','22.3':'distance','22.4':'distance','22.5':'height','22.6':'mass','22.7':'angle',
  '23.1':'angle','23.2':'charge','23.3':'charge','23.4':'radius','23.5':'sigma','23.6':'probe',
  '24.1':'position','24.2':'lane','24.3':'radius','24.4':'angle','24.5':'distance','24.6':'x','24.7':'side','24.8':'probe',
  '25.1':'gap','25.2':'gap','25.3':'first','25.4':'voltage','25.5':'insert','25.6':'kappa',
  '26.1':'current','26.2':'outlet','26.3':'radius','26.4':'field','26.5':'voltage',
  '27.1':'R1','27.2':'E2','27.3':'RV','27.4':'R',
  '28.1':'angle','28.2':'B','28.3':'thickness','28.4':'B','28.5':'B','28.6':'angle','28.7':'angle','28.8':'angle',
  '29.1':'r','29.2':'d','29.3':'r','29.4':'r','29.5':'z',
  '30.1':'speed','30.2':'speed','30.3':'probe','30.4':'length','30.5':'slope','30.6':'resistance','30.7':'resistance','30.8':'field','30.9':'slope',
  '31.1':'L','31.2':'R','31.3':'f','31.4':'f','31.5':'X','31.6':'load',
  '32.1':'area','32.2':'r','32.3':'rate','32.4':'inclination','32.5':'B','32.6':'gradient','32.7':'temperature','32.8':'alignment',
  '33.1':'wavelength','33.2':'E','33.3':'intensity','33.4':'angle','33.5':'angle','33.6':'n1','33.7':'n2',
  '34.1':'distance','34.2':'p','34.3':'n2','34.4':'p','34.5':'eyepiece','34.6':'R',
  '35.1':'thickness','35.2':'d','35.3':'phase','35.4':'thickness','35.5':'displacement',
  '36.1':'a','36.2':'angle','36.3':'diameter','36.4':'a','36.5':'spacing','36.6':'N','36.7':'spacing'
 };
 const quantities={
  '21.1':'Signed force on right charge','21.2':'Final net charge','21.3':'Final charge of object A',
  '22.1':'Signed force','22.2':'Signed radial field','22.3':'Exact axial field','22.4':'Signed axial field','22.5':'Signed axial field','22.6':'Signed acceleration','22.7':'Signed torque',
  '23.1':'Signed electric flux','23.2':'Net closed-surface flux','23.3':'Outer-surface charge','23.4':'Signed radial field','23.5':'Signed rightward field','23.6':'Signed radial field',
  '24.1':'Destination energy change','24.2':'Endpoint voltage change','24.3':'Potential relative to infinity','24.4':'Exact probe potential','24.5':'Exact rod potential','24.6':'Field magnitude','24.7':'Assembly work for third charge','24.8':'Potential at chosen radius',
  '25.1':'Charge on one plate','25.2':'Coaxial capacitance','25.3':'Equivalent capacitance','25.4':'Stored field energy','25.5':'Final plate voltage','25.6':'Bound-charge density magnitude',
  '26.1':'Charge crossed at displayed time','26.2':'Electron drift-speed magnitude','26.3':'Wire resistance','26.4':'Current density','26.5':'Heater power',
  '27.1':'Steady series current','27.2':'Signed middle-branch current','27.3':'Voltmeter reading','27.4':'Capacitor voltage at one time constant',
  '28.1':'Signed out-of-screen force','28.2':'Undeflected beam speed','28.3':'Top-minus-bottom Hall voltage','28.4':'Ion-orbit radius','28.5':'Cyclotron frequency','28.6':'Signed out-of-screen wire force','28.7':'Signed loop torque','28.8':'Dipole orientation energy',
  '29.1':'Signed tangential magnetic field','29.2':'Signed force per unit length','29.3':'Signed magnetic circulation','29.4':'Signed internal magnetic field','29.5':'Signed axial magnetic field',
  '30.1':'Signed induced emf at displayed time','30.2':'Thermal power','30.3':'Signed tangential electric field','30.4':'Air-core inductance','30.5':'Signed self-induced emf','30.6':'Clockwise current at displayed time','30.7':'Remaining magnetic energy','30.8':'Magnetic energy density','30.9':'Signed secondary emf',
  '31.1':'Maximum LC current','31.2':'Damped angular frequency','31.3':'Steady current amplitude','31.4':'Steady RLC current amplitude','31.5':'Average real power','31.6':'Secondary rms voltage',
  '32.1':'Right-face outward magnetic flux','32.2':'Signed tangential magnetic field','32.3':'Signed displacement current','32.4':'Signed upward field component','32.5':'Spin-level energy separation','32.6':'Signed upward magnetic force','32.7':'Magnetization','32.8':'Signed total core field',
  '33.1':'Vacuum wave frequency','33.2':'Average detector power','33.3':'Light-sail force','33.4':'Transmitted intensity','33.5':'Reflected angle from normal','33.6':'Critical incidence angle','33.7':'Brewster incidence angle',
  '34.1':'Signed image distance','34.2':'Signed mirror-image distance','34.3':'Real refracted image distance','34.4':'Signed lens-image distance','34.5':'Signed angular magnification','34.6':'Paraxial image distance',
  '35.1':'Extra optical path','35.2':'Adjacent bright-fringe separation','35.3':'Center intensity / maximum intensity','35.4':'Round-trip film optical path','35.5':'Fringe-cycle shift',
  '36.1':'Central-maximum width','36.2':'Intensity / center intensity','36.3':'Rayleigh angular limit','36.4':'Slit separation / slit width','36.5':'First-order diffraction angle','36.6':'Minimum resolved wavelength separation','36.7':'First-order Bragg glancing angle'
 };
 const format=n=>Number.isFinite(n)?Number(n.toPrecision(4)).toString():'undefined';
 function normalise(d,input){const s={time:0,stage:0,...input};for(const c of d.controls){if(c.options){const o=c.options.find(o=>String(o.value)===String(s[c.key]));s[c.key]=o?o.value:c.value;}else{s[c.key]=Math.max(c.min,Math.min(c.max,Number.isFinite(Number(s[c.key]))?Number(s[c.key]):c.value));}}return s;}
 function evaluate(d,s){try{const q=d.target(s,d.compute(s));return Number.isFinite(q?.answer)?q:null;}catch{return null;}}
 function describe(section,input={}){
  const key=String(section),d=window.GlassPhysicsRegistry?.[key];if(!d||!choices[key])return null;
  const s=normalise(d,input),control=d.controls.find(c=>c.key===choices[key]&&!c.options);if(!control)return null;
  const fixed=d.controls.filter(c=>c.key!==control.key).map(c=>({key:c.key,label:c.label,value:s[c.key],unit:c.unit||'',display:c.options?.find(o=>String(o.value)===String(s[c.key]))?.label??format(s[c.key])}));
  const discrete=discreteSections.includes(key),signature=JSON.stringify([key,control.key,timeDependentSections.includes(key)?s.time:0,...fixed.map(c=>c.value)]);let sweep=cache.get(signature);
  if(sweep){cache.delete(signature);cache.set(signature,sweep);}else{
   const count=discrete?Math.round((control.max-control.min)/control.step)+1:N;
   const points=[];for(let i=0;i<count;i++){const x=control.min+(control.max-control.min)*i/(count-1),q=evaluate(d,{...s,[control.key]:x});points.push({x,y:q?q.answer:null});}
   const ys=points.filter(p=>p.y!==null).map(p=>p.y);if(!ys.length)return null;
   const low=Math.min(...ys),high=Math.max(...ys),flat=Math.abs(high-low)<=Math.max(Math.abs(high),Math.abs(low),Number.MIN_VALUE)*1e-11;
   let ymin=Math.min(0,low),ymax=Math.max(0,high);
   // |Z|≥R bounds every possible drive-frequency peak, including resonance
   // between samples. Do not let sampling clip the exact current marker.
   if(key==='31.4')ymax=Math.max(ymax,s.V/s.R);
   if(ymin===ymax){ymin=-1;ymax=1;}else{const pad=(ymax-ymin)*.09;if(ymin<0)ymin-=pad;if(ymax>0)ymax+=pad;}
   sweep={points,low,high,flat,ymin,ymax};cache.set(signature,sweep);while(cache.size>32)cache.delete(cache.keys().next().value);
  }
  const q=evaluate(d,s);return{section:key,discrete,control:{key:control.key,label:control.label,unit:control.unit||'',min:control.min,max:control.max},quantity:quantities[key],unit:q?.unit||'',fixed,time:s.time,points:sweep.points,ymin:sweep.ymin,ymax:sweep.ymax,flat:sweep.flat,marker:{x:s[control.key],y:q?q.answer:null},prompt:q?.prompt||'The prediction is undefined at this setting.',note:sweep.flat?'This response is invariant across the chosen control at the other settings and model time shown. A horizontal response is the physical result.':discrete?'Separate points show the permitted integer counts. The highlighted point uses the exact selected count.':'The curve samples the model at 61 settings; the highlighted point uses the exact selected setting.'};
 }
 function draw(f){
  const left=104,right=928,top=52,bottom=219,x=x=>left+(x-f.control.min)/(f.control.max-f.control.min)*(right-left),y=y=>bottom-(y-f.ymin)/(f.ymax-f.ymin)*(bottom-top),txt=(X,Y,t,color='muted',size=13,anchor='middle')=>`<text x="${X}" y="${Y}" fill="var(--gp-${color})" font-size="${size}" text-anchor="${anchor}">${esc(t)}</text>`;
  let grid='',labels='';for(let i=0;i<=4;i++){const X=left+(right-left)*i/4,Y=top+(bottom-top)*i/4;grid+=`<path d="M${X},${top}V${bottom}M${left},${Y}H${right}" fill="none" stroke="var(--gp-line)" stroke-width="1" opacity=".38"/>`;labels+=txt(X,bottom+24,format(f.control.min+(f.control.max-f.control.min)*i/4))+txt(left-14,Y+4,format(f.ymax-(f.ymax-f.ymin)*i/4),'muted',12,'end');}
  let curve='',segment=[];const segments=[];for(const p of f.points){if(p.y===null){if(segment.length)segments.push(segment);segment=[];}else segment.push(p);}if(segment.length)segments.push(segment);
  for(const seg of segments){if(f.discrete){curve+=seg.map(p=>`<circle cx="${x(p.x)}" cy="${y(p.y)}" r="3.5" fill="var(--gp-aqua)"/>`).join('');continue;}const d=seg.map((p,i)=>(i?'L':'M')+x(p.x).toFixed(3)+','+y(p.y).toFixed(3)).join('');curve+=`<path d="${d}L${x(seg[seg.length-1].x)},${y(0)}L${x(seg[0].x)},${y(0)}Z" fill="var(--gp-aqua)" opacity=".075"/><path data-gp-response-curve="true" d="${d}" fill="none" stroke="var(--gp-aqua)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>`;}
  const valid=f.marker.y!==null,X=x(f.marker.x),Y=valid?y(f.marker.y):bottom,id='gp-response-'+f.section.replace('.','-');
  return`<svg class="gp-response-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 300" role="img" aria-label="${esc(f.quantity+' versus '+f.control.label+'. '+f.note)}"><title>${esc(f.quantity)} versus ${esc(f.control.label)}</title><desc>${esc('Prediction response. Other controls and displayed model time held fixed. '+f.note+' Current setting '+format(f.marker.x)+' '+f.control.unit+' gives '+format(f.marker.y)+' '+f.unit+'.')}</desc><defs><clipPath id="${id}"><rect x="${left-8}" y="${top-8}" width="${right-left+16}" height="${bottom-top+16}"/></clipPath></defs>${txt(left,24,f.quantity+(f.unit?' ('+f.unit+')':''),'ink',15,'start')}${grid}${labels}<g clip-path="url(#${id})"><path d="M${left},${y(0)}H${right}" stroke="var(--gp-wire)" stroke-width="1.3" opacity=".6"/>${curve}${valid?`<path d="M${X},${bottom}V${Y}" fill="none" stroke="var(--gp-coral)" stroke-dasharray="4 5" opacity=".6"/><circle data-gp-response-marker="true" cx="${X}" cy="${Y}" r="6" fill="var(--gp-coral)" stroke="var(--gp-paper)" stroke-width="2"><title>${esc(format(f.marker.x)+' '+f.control.unit+' → '+format(f.marker.y)+' '+f.unit)}</title></circle>`:''}</g>${txt(516,282,f.control.label+(f.control.unit?' ('+f.control.unit+')':''),'ink',14)}${txt(right,24,'Selected: '+format(f.marker.y)+(f.unit?' '+f.unit:''),'coral',14,'end')}</svg>`;
 }
 function svg(section,state){const f=describe(section,state);return f?draw(f):'';}
 function html(section,state){const f=describe(section,state);if(!f)return'';const constants=f.fixed.map(c=>`${c.label}: ${c.display}${c.unit?' '+c.unit:''}`).join(' · '),animation=window.GlassPhysicsRegistry[f.section].animation,clock=timeDependentSections.includes(f.section)?'Model time: '+format(f.time)+' '+(animation?.unit||(animation?.kind==='physical'?'s':'visual units')):'This prediction is independent of the illustration clock';return`<section class="gp-response" aria-label="Prediction response graph"><div class="gp-response-heading"><span>CHANGE ONE THING</span><h4>How the prediction responds</h4><p>${esc(f.quantity)} as you change ${esc(f.control.label.toLowerCase())}.</p></div>${draw(f)}<p class="gp-response-note">${esc(f.note)} The prediction can refer to an endpoint or amplitude rather than the moving scene.</p><details class="gp-response-context"><summary>What this graph holds fixed</summary><p>${esc(constants)} · ${esc(clock)}.</p><p>${esc(f.prompt)}</p><p>The horizontal axis always spans this control’s full range. The vertical scale is shared across that sweep; changing another control or model time can change it. The shaded area is only a visual guide, not an integral.</p></details></section>`;}
 const key=(section,state)=>{const d=window.GlassPhysicsRegistry?.[section];if(!d||!choices[section])return null;const s=normalise(d,state);return JSON.stringify([section,...d.controls.map(c=>s[c.key]),timeDependentSections.includes(section)?s.time:0]);};
 return{describe,svg,html,key,timeDependentSections,sections:()=>Object.keys(choices),cacheSize:()=>cache.size};
})();
