/* Original editable DC circuit workspace for Chapter 27. All calculations use CircuitSolver. */
window.CircuitBuilderLab=(()=>{
 'use strict';
 const C=window.CircuitSolver,KEY='glasshouse-circuit-builder-v1';
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const fmt=n=>Number.isFinite(n)?(Math.abs(n)<1e-10?'0':Number(n.toPrecision(5)).toString()):'—';
 const fmtI=n=>n===null||n===undefined?'—':Math.abs(n)<1?fmt(n*1000)+' mA':fmt(n)+' A';
 const valueText=e=>e.type==='wire'?'ideal wire':e.type==='resistor'?(e.value>=1000?fmt(e.value/1000)+' kΩ':fmt(e.value)+' Ω'):e.type==='voltage'?fmt(e.value)+' V':fmtI(e.value);
 const TOOLS=[['select','Select','Inspect or edit a component'],['wire','Wire','Connect any two points; all crossings join'],['resistor','Resistor','Choose two neighboring points'],['voltage','Voltage source','First point is +; second is −'],['current','Current source','Positive current goes from first to second point'],['positive','Probe +','Mark the point to measure'],['negative','Probe −','Mark the measurement reference'],['ground','Ground','Choose the circuit’s 0 V reference'],['erase','Erase','Remove a component or wire']];
 const names={wire:'Wire',resistor:'Resistor',voltage:'Voltage source',current:'Current source'};
 const POS=n=>({x:80+(n%C.COLS)*100,y:75+Math.floor(n/C.COLS)*90});
 const clone=s=>JSON.parse(JSON.stringify(s));let active=null;
 function restore(){try{const s=JSON.parse(localStorage.getItem(KEY));if(s?.version===1&&C.validate(s).valid&&C.validNode(s.positive)&&C.validNode(s.negative))return s;}catch{}return C.preset('divider');}
 function icon(kind){const lines={select:'M7 4L19 12L13 13L10 19Z',wire:'M3 17V7H21',resistor:'M2 12H5L7 6L10 18L13 6L16 18L19 12H22',voltage:'M12 2V6M12 18V22M6 9H18M9 15H15',current:'M12 3V21M7 11L12 5L17 11',positive:'M12 4V20M4 12H20',negative:'M4 12H20',ground:'M12 3V11M3 11H21M6 16H18M9 21H15',erase:'M4 14L12 4L21 12L14 20H10Z'};return`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="${lines[kind]}"/></svg>`;}
 function guided(options){if(window.RCCircuitLab?.applies(options.q,'base'))return{module:window.RCCircuitLab,label:'Guided RC charging & discharging',html:window.RCCircuitLab.html(options)};if(window.PhysicsApparatusLab?.applies(options.q,'base'))return{module:window.PhysicsApparatusLab,label:'Guided experiment for section '+options.section,html:window.PhysicsApparatusLab.html(options)};return null;}
 function html(options={}){
  const g=guided(options);return`<section class="cb-lab" data-circuit-builder data-cb-section="${esc(options.section)}" aria-label="Build your own DC circuit"><div class="cb-heading"><div><span class="cb-eyebrow">CHAPTER 27 / CIRCUIT STUDIO</span><h3>Build it. Probe it. Understand it.</h3><p>Place your components, connect the wires, then measure the voltage between any two connected points.</p></div><span class="cb-live"><i></i> LIVE DC SOLVER</span></div><div class="cb-presets" aria-label="Circuit starting points"><span>Start with</span>${[['divider','Voltage divider'],['series','Series'],['parallel','Parallel'],['bridge','Bridge'],['blank','Blank board']].map(([id,label])=>`<button type="button" data-cb-preset="${id}">${label}</button>`).join('')}<span class="cb-history"><button type="button" data-cb-action="undo" aria-label="Undo circuit edit">↶ Undo</button><button type="button" data-cb-action="redo" aria-label="Redo circuit edit">↷ Redo</button></span></div><nav class="cb-tools" aria-label="Circuit building tools">${TOOLS.map(([id,label,tip])=>`<button type="button" data-cb-tool="${id}" aria-pressed="${id==='select'}" title="${esc(tip)}">${icon(id)}<span>${label}</span></button>`).join('')}</nav><p class="cb-instruction" data-cb-instruction role="status">Select a component to edit it, or choose a tool to build.</p><div class="cb-workspace"><div class="cb-board-column"><div class="cb-board" data-cb-board></div><div class="cb-view-controls"><label><input type="checkbox" data-cb-toggle="voltages"> Node voltages</label><label><input type="checkbox" data-cb-toggle="motion" checked> Current markers</label><span>Grid crossings are connected junctions.</span></div><div class="cb-legend"><span>Potential</span><i></i><span>−24 V</span><b>0 V</b><span>+24 V</span><small>Fixed color scale; values outside this range are shown numerically. Floating nodes stay neutral.</small></div><div class="cb-cards" data-cb-cards></div><div class="cb-warning" data-cb-warning role="status" hidden></div></div><aside class="cb-sidebar"><section class="cb-inspector"><span class="cb-eyebrow">COMPONENT INSPECTOR</span><div data-cb-inspector></div></section><section class="cb-meter"><div class="cb-meter-head"><span class="cb-eyebrow">YOUR VOLTMETER</span><span>V = V₊ − V₋</span></div><label><b class="cb-plus">+</b> Measurement point<select data-cb-probe="positive" aria-label="Positive voltage probe">${nodeOptions()}</select></label><label><b class="cb-minus">−</b> Reference point<select data-cb-probe="negative" aria-label="Negative voltage probe">${nodeOptions()}</select></label><p class="cb-meter-number" data-cb-meter aria-live="polite">—</p><p class="cb-meter-reason" data-cb-meter-reason></p><button type="button" data-cb-action="ground-negative">Set − probe to ground</button><p class="cb-note">A voltage is a difference between two points. Ground defines 0 V; moving it changes node labels, not the circuit currents.</p></section></aside></div><details class="cb-analysis" open><summary>Follow the equations</summary><div data-cb-equations></div><div class="cb-table-wrap"><table><caption>Signed branch values, from endpoint A toward B</caption><thead><tr><th>Component</th><th>A → B</th><th>Value</th><th>Vₐ − Vᵦ</th><th>Current A → B</th><th>Power absorbed</th></tr></thead><tbody data-cb-table></tbody></table></div><p class="cb-note">Positive power means absorbed; a negative source power means energy supplied. Conventional-current markers follow calculated component currents on one fixed speed scale (800 px/s per ampere, capped at 200 px/s). Zero current has no moving markers. Resistor glow uses a fixed 10 W scale and saturates; exact power is in the table. Ideal-wire currents are not assigned: redundant wire paths do not have unique individual currents.</p></details><details class="cb-help"><summary>How to build a circuit</summary><ol><li>Choose <b>Wire</b> and click two points. The wire runs horizontally, then vertically. All crossed grid dots join the same electrical node.</li><li>Choose a resistor or source and click <b>two neighboring points</b>. For a source, the first endpoint is its positive voltage or current reference.</li><li>Click a component to change its resistance, volts or amperes. Use <b>Move</b>, <b>Rotate</b> or <b>Delete</b> in its inspector. Erase an existing wire before inserting a component on that edge.</li><li>Choose <b>Probe +</b> and <b>Probe −</b>, or use the two voltmeter menus. The reading updates immediately.</li><li><b>Undo</b> restores edits, including clearing the board. Your circuit is saved on this device. Grid points and components also work with Tab, Enter and Space; Escape cancels a pending connection.</li></ol><p>Model: ideal wires, ideal independent DC sources and positive ohmic resistors. The builder solves the steady state; it does not simulate capacitors, inductors or AC startup. The guided experiment below covers the section’s other ideas.</p><a href="https://openstax.org/books/university-physics-volume-2/pages/10-3-kirchhoffs-rules" target="_blank" rel="noopener">Read the junction and loop rules at OpenStax ↗</a></details>${g?`<details class="cb-guided"><summary>${esc(g.label)}</summary>${g.html}</details>`:''}<p class="cb-save" data-cb-save>Saved on this device</p></section>`;
 }
 function nodeOptions(){return Array.from({length:C.COLS*C.ROWS},(_,n)=>`<option value="${n}">${C.label(n)}</option>`).join('');}
 function potentialColor(v){
  if(!Number.isFinite(v))return'var(--cb-muted)';const base=[104,132,142],to=v<0?[64,164,177]:[255,103,79],f=Math.min(1,Math.abs(v)/24);return'rgb('+base.map((c,i)=>Math.round(c+(to[i]-c)*f)).join(',')+')';
 }
 function svg(s,result,ui){
  const p=ui.pending;let out=`<title>Your editable DC circuit</title><desc>Columns A to I, rows 1 to 6. Select a component to inspect it. All wire crossings at grid points are connected. The plus and minus probes measure a voltage difference.</desc><defs><pattern id="cb-grid" width="100" height="90" x="80" y="75" patternUnits="userSpaceOnUse"><path d="M100 0H0V90" fill="none" stroke="var(--cb-line)" stroke-width="1" stroke-dasharray="2 6"/></pattern></defs><rect x="80" y="75" width="800" height="450" fill="url(#cb-grid)"/>`;
  for(let col=0;col<C.COLS;col++)out+=`<text x="${80+col*100}" y="30" class="cb-coordinate">${String.fromCharCode(65+col)}</text>`;
  for(let row=0;row<C.ROWS;row++)out+=`<text x="26" y="${80+row*90}" class="cb-coordinate">${row+1}</text>`;
  for(const e of s.elements.filter(e=>e.type==='wire')){
   const points=C.wireNodes(e.a,e.b).map(POS),d=points.map((p,i)=>(i?'L':'M')+p.x+','+p.y).join(''),color=potentialColor(result.nodes[e.a]?.potential);
   out+=`<g class="cb-element cb-wire ${ui.selected===e.id?'is-selected':''}" data-cb-element="${esc(e.id)}" role="button" tabindex="0" aria-label="${esc(e.id+' wire from '+C.label(e.a)+' to '+C.label(e.b))}"><path d="${d}" class="cb-wire-hit"/><path d="${d}" class="cb-wire-shadow"/><path d="${d}" class="cb-wire-line" style="stroke:${color}"/></g>`;
  }
  for(const e of s.elements.filter(e=>e.type!=='wire')){
   const a=POS(e.a),b=POS(e.b),cx=(a.x+b.x)/2,cy=(a.y+b.y)/2,angle=Math.atan2(b.y-a.y,b.x-a.x)*180/Math.PI,half=Math.hypot(b.x-a.x,b.y-a.y)/2,v=result.branches[e.id],selected=ui.selected===e.id;
   const colorA=potentialColor(result.nodes[e.a]?.potential),colorB=potentialColor(result.nodes[e.b]?.potential);
   let symbol='';
   if(e.type==='resistor')symbol=`<rect x="-30" y="-19" width="60" height="38" rx="9" class="cb-resistor-halo" style="opacity:${v?.power!==null?Math.min(.65,(v?.power||0)/10):0}"/><path d="M-27 0L-21 -10L-13 10L-5 -10L3 10L11 -10L19 10L27 0" class="cb-symbol"/>`;
   if(e.type==='voltage')symbol='<circle r="25" class="cb-source-body"/><path d="M-16 0H-6M-11 -5V5M6 0H16" class="cb-symbol"/>';
   if(e.type==='current')symbol='<circle r="25" class="cb-source-body"/><path d="M-15 0H15M7 -7L15 0L7 7" class="cb-symbol"/>';
   const I=v?.current,animate=ui.motion&&I!==null&&I!==undefined&&Math.abs(I)>1e-10;
   out+=`<g class="cb-element ${selected?'is-selected':''}" data-cb-element="${esc(e.id)}" role="button" tabindex="0" aria-label="${esc(e.id+' '+names[e.type]+', '+valueText(e)+', '+C.label(e.a)+' to '+C.label(e.b))}"><rect x="${cx-52}" y="${cy-38}" width="104" height="76" rx="14" class="cb-component-hit"/><g transform="translate(${cx} ${cy}) rotate(${angle})"><path d="M${-half} 0H-27" style="stroke:${colorA}" class="cb-lead"/><path d="M27 0H${half}" style="stroke:${colorB}" class="cb-lead"/>${selected?'<rect x="-36" y="-30" width="72" height="60" rx="14" class="cb-selection-ring"/>':''}${symbol}${animate?`<path d="M${-half+6} 0H${half-6}" class="cb-flow" style="animation-duration:${20/Math.min(200,Math.abs(I)*800)}s;animation-direction:${I<0?'reverse':'normal'}"/>`:''}</g><text x="${cx+(Math.abs(a.x-b.x)<1?(cx>780?-42:42):0)}" y="${cy+(Math.abs(a.x-b.x)<1?-11:-34)}" text-anchor="${Math.abs(a.x-b.x)<1?(cx>780?'end':'start'):'middle'}" class="cb-component-name">${esc(e.id)}</text><text x="${cx+(Math.abs(a.x-b.x)<1?(cx>780?-42:42):0)}" y="${cy+(Math.abs(a.x-b.x)<1?8:-18)}" text-anchor="${Math.abs(a.x-b.x)<1?(cx>780?'end':'start'):'middle'}" class="cb-component-value">${esc(valueText(e))}</text>`;
   if(I!==null&&I!==undefined&&Math.abs(I)>1e-10){const dir=I<0?-1:1;out+=`<g transform="translate(${cx} ${cy}) rotate(${angle})"><path d="M${-15*dir} 34H${15*dir}M${8*dir} 29L${15*dir} 34L${8*dir} 39" class="cb-current-arrow"/></g>`;}
   out+='</g>';
  }
  if(p!==null&&ui.hover!==null&&ui.hover!==p){const points=C.wireNodes(p,ui.hover).map(POS);out+=`<polyline points="${points.map(p=>p.x+','+p.y).join(' ')}" class="cb-preview"/>`;}
  for(let n=0;n<C.COLS*C.ROWS;n++){
   const pos=POS(n),used=Boolean(result.nodes[n]),color=potentialColor(result.nodes[n]?.potential),pending=p===n;
   out+=`<g class="cb-node ${used?'is-connected':''} ${pending?'is-pending':''}" data-cb-node="${n}" role="button" tabindex="0" aria-label="${esc('Grid point '+C.label(n)+(used?', connected':'')+(n===s.positive?', positive probe':'')+(n===s.negative?', negative probe':''))}"><circle cx="${pos.x}" cy="${pos.y}" r="17" class="cb-node-hit"/><circle cx="${pos.x}" cy="${pos.y}" r="${used?5:3}" class="cb-node-dot" style="${used?'fill:'+color:''}"/>${pending?`<circle cx="${pos.x}" cy="${pos.y}" r="12" class="cb-pending-ring"/>`:''}</g>`;
   if(ui.voltages&&used)out+=`<text x="${pos.x+(pos.x>780?-12:12)}" y="${pos.y-12}" text-anchor="${pos.x>780?'end':'start'}" class="cb-node-voltage">${result.nodes[n].potential===null?'— V':fmt(result.nodes[n].potential)+' V'}</text>`;
  }
  const ground=POS(s.ground);out+=`<g class="cb-ground" aria-label="Ground at ${C.label(s.ground)}"><path d="M${ground.x} ${ground.y+7}v14m-15 0h30m-10 6h-10m3 6h4"/><text x="${ground.x}" y="${ground.y+52}">0 V · ${C.label(s.ground)}</text></g>`;
  for(const [key,sign,offset]of[['positive','+',-27],['negative','−',27]]){const p=POS(s[key]);out+=`<g class="cb-probe cb-probe-${key}" aria-label="${sign} probe at ${C.label(s[key])}"><circle cx="${p.x}" cy="${p.y}" r="10"/><path d="M${p.x} ${p.y+(offset<0?-10:10)}v${offset<0?-13:13}"/><rect x="${p.x-24}" y="${p.y+offset-12}" width="48" height="23" rx="8"/><text x="${p.x}" y="${p.y+offset+4}">${sign} ${C.label(s[key])}</text></g>`;}
  out+='<text x="480" y="588" class="cb-board-caption">COMPONENTS: TWO NEIGHBORING DOTS · WIRES: ANY TWO DOTS · CROSSINGS JOIN</text>';
  return`<svg viewBox="0 0 960 610" xmlns="http://www.w3.org/2000/svg" class="cb-svg" role="group" aria-label="Editable circuit board">${out}</svg>`;
 }
 function inspector(a){
  const e=a.circuit.elements.find(e=>e.id===a.selected);
  if(!e)return'<h4>Select a component</h4><p class="cb-note">Click a resistor or source on the board to change its value. To build, choose a tool and connect two points.</p>';
  const limits=C.LIMITS[e.type],title=e.type==='resistor'?'Resistance':e.type==='voltage'?'Source voltage':e.type==='current'?'Source current':'',unit=e.type==='resistor'?'Ω':e.type==='voltage'?'V':'A';
  return`<h4>${esc(e.id)} <span>${esc(names[e.type])}</span></h4><p class="cb-terminals"><b>A · ${C.label(e.a)}</b><span>→</span><b>B · ${C.label(e.b)}</b></p>${limits?`<label class="cb-value-label">${title} <span>${unit}</span><input type="number" data-cb-value="number" min="${limits[0]}" max="${limits[1]}" step="any" value="${e.value}" aria-label="${title} in ${unit}"></label><input class="cb-value-slider" type="range" data-cb-value="range" min="${e.type==='resistor'?0:limits[0]}" max="${e.type==='resistor'?6:limits[1]}" step="${e.type==='resistor'?.01:e.type==='voltage'?.1:.001}" value="${e.type==='resistor'?Math.log10(e.value):e.value}" aria-label="${title}${e.type==='resistor'?', logarithmic scale':''}"><div class="cb-range-labels"><span>${e.type==='resistor'?'1 Ω':limits[0]+' '+unit}</span><span>${e.type==='resistor'?'1 MΩ':limits[1]+' '+unit}</span></div><p class="cb-note">${e.type==='resistor'?'Use the slider or type an exact resistance. The slider spans a logarithmic scale.':e.type==='voltage'?'V(A) − V(B) is fixed at this value. Negative volts reverse the source polarity.':'Positive current is forced from A toward B. A negative value reverses the actual current; the source arrow is its positive reference.'}</p>`:'<p class="cb-note">This is an ideal connection: every grid dot along it is at the same potential. Use a separate branch to place a parallel component.</p>'}<div class="cb-edit-actions"><button type="button" data-cb-action="move">Move</button><button type="button" data-cb-action="rotate" ${e.type==='wire'?'disabled':''}>Rotate</button><button type="button" data-cb-action="reverse" ${e.type==='wire'?'disabled':''}>Reverse A/B</button><button type="button" data-cb-action="delete" class="cb-delete">Delete</button></div>`;
 }
 function calculations(a){
  const s=a.circuit,r=a.result,m=r.measure(s.positive,s.negative),e=s.elements.find(e=>e.id===a.selected),branch=e?r.branches[e.id]:null;
  const voltage=m.value===null?'—':fmt(m.value)+' <small>V</small>';
  const cards=`<article><span>VOLTAGE · ${C.label(s.positive)} − ${C.label(s.negative)}</span><strong>${voltage}</strong></article><article><span>${e?esc(e.id)+' · A → B CURRENT':'SELECT A COMPONENT'}</span><strong>${branch?esc(fmtI(branch.current)):'—'}</strong></article><article><span>RESISTOR HEATING · TOTAL</span><strong>${r.resistorPower===null?'—':fmt(r.resistorPower)+' <small>W</small>'}</strong></article>`;
  let equations=`<p><b>Voltage probe:</b> V(${C.label(s.positive)}) − V(${C.label(s.negative)}) ${m.value===null?'is not determined.':m.grounded?`= ${fmt(m.positive)} − (${fmt(m.negative)}) = <b>${fmt(m.value)} V</b>.`:`= <b>${fmt(m.value)} V</b> within the same floating network.`}</p>`;
  if(e&&branch){
   if(e.type==='resistor')equations+=`<p><b>${esc(e.id)} · Ohm’s law:</b> I<sub>A→B</sub> = (V<sub>A</sub> − V<sub>B</sub>)/R ${branch.current===null?'cannot be determined for this circuit.':`= (${fmt(branch.voltage)} V)/(${fmt(e.value)} Ω) = <b>${esc(fmtI(branch.current))}</b>.`}</p><p>Heating P = I²R ${branch.power===null?'is undetermined.':`= ${fmt(branch.power)} W`}. Negative current means the actual current goes from B toward A.</p>`;
   if(e.type==='voltage')equations+=`<p><b>${esc(e.id)} · voltage source:</b> V<sub>A</sub> − V<sub>B</sub> = <b>${fmt(e.value)} V</b>. Kirchhoff’s junction equations determine its current: ${esc(fmtI(branch.current))}. ${branch.current===null?'Redundant or conflicting ideal sources may leave this current undetermined.':'The current is a result of the connected circuit, not a fixed battery property.'}</p>`;
   if(e.type==='current')equations+=`<p><b>${esc(e.id)} · current source:</b> I<sub>A→B</sub> = <b>${esc(fmtI(e.value))}</b>. The network determines its voltage: ${branch.voltage===null?'undetermined':fmt(branch.voltage)+' V'}. A finite DC return path is required.</p>`;
   if(e.type==='wire')equations+='<p><b>Ideal wire:</b> the voltage drop is zero. Its individual current is not displayed because redundant ideal wire paths can split current in nonunique ways. Inspect an adjacent resistor or source to read a solved branch current.</p>';
  }
  equations+=`<p class="cb-balance"><b>Energy check:</b> sum of signed component powers ${r.powerBalance===null?'is not uniquely determined.':`= ${Math.abs(r.powerBalance)<1e-9?'0':fmt(r.powerBalance)} W (up to numerical roundoff).`} Resistors absorb power; sources may deliver or absorb it.</p>`;
  const rows=s.elements.map(e=>{const b=r.branches[e.id];return`<tr class="${e.id===a.selected?'is-selected':''}"><th><button type="button" data-cb-select="${esc(e.id)}">${esc(e.id)}</button></th><td>${C.label(e.a)} → ${C.label(e.b)}</td><td>${esc(valueText(e))}</td><td>${b.voltage===null?'—':fmt(b.voltage)+' V'}</td><td>${esc(fmtI(b.current))}</td><td>${b.power===null?'—':fmt(b.power)+' W'}</td></tr>`;}).join('')||'<tr><td colspan="6">Your board is empty. Add a voltage source, resistors and wires to make a circuit.</td></tr>';
  const invalid=r.islands.filter(i=>!i.consistent),free=r.islands.filter(i=>i.underdetermined),floating=r.islands.filter(i=>!i.grounded);
  let warning='';
  if(invalid.length)warning='No finite DC solution in '+invalid.length+' network'+(invalid.length===1?'':'s')+'. Check for a shorted voltage source, incompatible source voltages, or a current source without a return path. Unknown readings are shown as —.';
  else if(free.length)warning='Some values are not uniquely determined. Redundant ideal voltage sources can fix node voltages while leaving their individual currents unknown. Add a resistor return path for floating current-source branches.';
  else if(floating.length)warning='A network is floating relative to ground. Its internal voltage differences can still be measured with both probes on that network; absolute node voltages are left blank.';
  return{cards,voltage,equations,rows,warning,reason:m.reason};
 }
 function instruction(a){
  if(a.message)return a.message;
  if(a.pending!==null)return`Start at ${C.label(a.pending)}. ${a.tool==='wire'?'Choose the other endpoint; the preview shows the wire route.':'Choose a neighboring point for the other terminal.'} Escape cancels.`;
  if(a.moving)return`Move ${a.moving}: choose its first new endpoint, then a neighboring second endpoint. Existing wires stay in place.`;
  return ({select:'Click a component to edit volts, resistance or source current. Click a grid dot to move the + voltage probe.',wire:'Click the first grid point, then the second. All crossed grid dots become connected.',resistor:'Place a resistor: choose two neighboring grid dots. Then edit its resistance in the inspector.',voltage:'Place a voltage source: first point is + (A), second is − (B). Choose neighboring dots.',current:'Place a current source: its positive reference points from the first endpoint A to B. Choose neighboring dots.',positive:'Click a connected point for the + voltage probe.',negative:'Click a connected point for the − voltage probe.',ground:'Click a grid point to define the 0 V reference. This does not change any voltage difference or current.',erase:'Click a component or wire to remove it. Undo is available.'})[a.tool];
 }
 function unmount(){if(!active)return;const a=active;for(const [ev,fn]of a.listeners)a.root.removeEventListener(ev,fn);if(a.frame!==null)cancelAnimationFrame(a.frame);a.guided?.unmount();active=null;}
 function mount(container=document){
  const root=container.matches?.('[data-circuit-builder]')?container:container.querySelector('[data-circuit-builder]');if(!root)return false;unmount();
  const circuit=restore(),a={root,circuit,result:C.solve(circuit),selected:circuit.elements.find(e=>e.type==='voltage')?.id||null,tool:'select',pending:null,hover:null,moving:null,message:'',motion:!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches,voltages:false,undo:[],redo:[],editKey:null,listeners:[],frame:null,guided:null};active=a;
  const find=s=>root.querySelector(s);
  function save(){try{localStorage.setItem(KEY,JSON.stringify(a.circuit));find('[data-cb-save]').textContent='Circuit saved on this device';}catch{find('[data-cb-save]').textContent='This browser could not save the circuit. Keep this page open to retain your work.';}}
  function paintInspector(){find('[data-cb-inspector]').innerHTML=inspector(a);}
  function paint(rebuildInspector=false){
   if(active!==a)return;const focused=document.activeElement?.getAttribute?.('data-cb-node');
   find('[data-cb-board]').innerHTML=svg(a.circuit,a.result,a);if(focused!==null&&focused!==undefined)find(`[data-cb-node="${focused}"]`)?.focus?.({preventScroll:true});
   const c=calculations(a);find('[data-cb-cards]').innerHTML=c.cards;find('[data-cb-meter]').innerHTML=c.voltage;find('[data-cb-meter-reason]').textContent=c.reason;
   find('[data-cb-equations]').innerHTML=c.equations;find('[data-cb-table]').innerHTML=c.rows;
   const warning=find('[data-cb-warning]');warning.hidden=!c.warning;warning.textContent=c.warning;
   find('[data-cb-instruction]').textContent=instruction(a);
   for(const button of root.querySelectorAll('[data-cb-tool]'))button.setAttribute('aria-pressed',String(button.dataset.cbTool===a.tool));
   for(const key of ['positive','negative'])find(`[data-cb-probe="${key}"]`).value=String(a.circuit[key]);
   find('[data-cb-action="undo"]').disabled=!a.undo.length;find('[data-cb-action="redo"]').disabled=!a.redo.length;
   find('[data-cb-toggle="motion"]').checked=a.motion;find('[data-cb-toggle="voltages"]').checked=a.voltages;
   if(rebuildInspector)paintInspector();
  }
  function change(mutator,message='',gesture=null){
   const next=clone(a.circuit);mutator(next);const check=C.validate(next);if(!check.valid){a.message=check.message;paint(false);return false;}
   if(JSON.stringify(next)===JSON.stringify(a.circuit)){a.message=message;paint(false);return true;}
   if(!gesture||a.editKey!==gesture){a.undo.push(clone(a.circuit));if(a.undo.length>50)a.undo.shift();a.redo=[];}
   a.editKey=gesture;a.circuit=next;a.result=C.solve(next);a.message=message;save();paint(false);return true;
  }
  function select(id){a.selected=id;a.pending=null;a.hover=null;a.moving=null;a.tool='select';a.message='';a.editKey=null;paint(true);}
  function nextId(type){const prefix={wire:'W',resistor:'R',voltage:'V',current:'I'}[type];let n=1;while(a.circuit.elements.some(e=>e.id===prefix+n))n++;return prefix+n;}
  function remove(id){if(change(s=>s.elements=s.elements.filter(e=>e.id!==id),'Component removed. Undo restores it.')){if(a.selected===id)a.selected=null;a.pending=null;a.moving=null;paint(true);}}
  function point(n){
   a.message='';a.editKey=null;
   if(['positive','negative','ground'].includes(a.tool)){change(s=>s[a.tool]=n,(a.tool==='ground'?'Ground':'Probe')+' moved to '+C.label(n)+'.');return;}
   if(a.tool==='select'){change(s=>s.positive=n,'+ probe moved to '+C.label(n)+'. Select a component to edit its value.');return;}
   if(a.tool==='erase'){a.message='Click the wire line or component body to erase it.';paint(false);return;}
   if(a.pending===null){a.pending=n;paint(false);return;}
   if(a.pending===n){a.pending=null;paint(false);return;}
   const first=a.pending,type=a.tool,id=a.moving||nextId(type),old=a.circuit.elements.find(e=>e.id===a.moving),value=old?.value??({resistor:100,voltage:9,current:.02}[type]);
   const e={id,type,a:first,b:n,...(type==='wire'?{}:{value})};
   const ok=change(s=>{s.elements=s.elements.filter(e=>e.id!==a.moving);s.elements.push(e);},`${id} ${old?'moved':'placed'}. ${type==='wire'?'Every crossed grid dot is connected.':'Use the inspector to change its value.'}`);
   if(ok){a.selected=id;a.pending=null;a.hover=null;a.moving=null;paint(true);}
  }
  const click=e=>{
   const tool=e.target.closest('[data-cb-tool]');if(tool){a.tool=tool.dataset.cbTool;a.pending=null;a.hover=null;a.moving=null;a.message='';a.editKey=null;paint(false);return;}
   const preset=e.target.closest('[data-cb-preset]');if(preset){change(s=>Object.assign(s,C.preset(preset.dataset.cbPreset)),'Starting circuit loaded. Undo restores the previous circuit.');a.selected=a.circuit.elements.find(e=>e.type==='voltage')?.id||null;a.pending=null;a.hover=null;a.tool='select';a.moving=null;paint(true);return;}
   const node=e.target.closest('[data-cb-node]');if(node){point(Number(node.dataset.cbNode));return;}
   const element=e.target.closest('[data-cb-element],[data-cb-select]');if(element){const id=element.dataset.cbElement||element.dataset.cbSelect;if(a.tool==='erase'&&element.dataset.cbElement)remove(id);else select(id);return;}
   const action=e.target.closest('[data-cb-action]')?.dataset.cbAction;if(!action)return;
   if(action==='undo'||action==='redo'){
    const from=action==='undo'?a.undo:a.redo,to=action==='undo'?a.redo:a.undo;if(!from.length)return;to.push(clone(a.circuit));a.circuit=from.pop();a.result=C.solve(a.circuit);a.pending=null;a.hover=null;a.moving=null;a.editKey=null;a.message=action==='undo'?'Edit undone.':'Edit restored.';if(!a.circuit.elements.some(e=>e.id===a.selected))a.selected=a.circuit.elements.find(e=>e.type==='voltage')?.id||null;save();paint(true);return;
   }
   if(action==='ground-negative'){change(s=>s.ground=s.negative,'Ground moved to the − probe. Circuit currents and voltage differences stay the same.');return;}
   const selected=a.circuit.elements.find(e=>e.id===a.selected);if(!selected)return;
   if(action==='delete'){remove(selected.id);return;}
   if(action==='move'){a.moving=selected.id;a.tool=selected.type;a.pending=null;a.hover=null;a.message='';paint(false);return;}
   if(action==='reverse'&&selected.type!=='wire'){change(s=>{const e=s.elements.find(e=>e.id===a.selected);[e.a,e.b]=[e.b,e.a];},'Endpoint references reversed. Source polarity or direction follows its A/B terminals.');paint(true);return;}
   if(action==='rotate'&&selected.type!=='wire'){
    const p=C.xy(selected.a),q=C.xy(selected.b),newCol=p.column-(q.row-p.row),newRow=p.row+(q.column-p.column);
    if(newCol<0||newCol>=C.COLS||newRow<0||newRow>=C.ROWS){a.message='That rotation is outside the board. Move the component inward first.';paint(false);return;}
    change(s=>s.elements.find(e=>e.id===a.selected).b=C.node(newCol,newRow),'Component rotated. Wires remain at their original grid points.');paint(true);
   }
  };
  const input=e=>{
   const kind=e.target.dataset?.cbValue;if(!kind)return;const component=a.circuit.elements.find(e=>e.id===a.selected);if(!component||component.type==='wire')return;
   const value=kind==='range'&&component.type==='resistor'?Math.pow(10,Number(e.target.value)):Number(e.target.value);
   if(e.target.value.trim()===''||!Number.isFinite(value))return;const limits=C.LIMITS[component.type];
   if(value<limits[0]||value>limits[1]){a.message=`Enter a value from ${limits[0]} to ${limits[1]}.`;find('[data-cb-instruction]').textContent=a.message;return;}
   if(change(s=>s.elements.find(c=>c.id===component.id).value=value,'Values updated from the actual connected circuit.',component.id+':value')){
    const other=find(`[data-cb-value="${kind==='range'?'number':'range'}"]`);if(other)other.value=String(kind==='number'&&component.type==='resistor'?Math.log10(value):value);
   }
  };
  const onChange=e=>{
   if(e.target.dataset?.cbValue){input(e);a.editKey=null;return;}
   const probe=e.target.dataset?.cbProbe;if(probe){change(s=>s[probe]=Number(e.target.value),'Probe moved. The reading is V(+) − V(−).');return;}
   const toggle=e.target.dataset?.cbToggle;if(toggle){a[toggle]=Boolean(e.target.checked);a.message='';paint(false);}
  };
  const keydown=e=>{
   if(e.key==='Escape'){a.pending=null;a.hover=null;a.moving=null;a.message='Pending placement canceled.';paint(false);return;}
   if((e.key==='Enter'||e.key===' ')&&e.target.matches?.('[data-cb-node],[data-cb-element]')){e.preventDefault();click(e);}
  };
  const pointermove=e=>{
   if(a.pending===null)return;const n=e.target.closest('[data-cb-node]');if(!n||Number(n.dataset.cbNode)===a.hover)return;a.hover=Number(n.dataset.cbNode);
   if(a.frame===null)a.frame=requestAnimationFrame(()=>{a.frame=null;if(active===a)find('[data-cb-board]').innerHTML=svg(a.circuit,a.result,a);});
  };
  for(const [ev,fn]of [['click',click],['input',input],['change',onChange],['keydown',keydown],['pointermove',pointermove]]){root.addEventListener(ev,fn);a.listeners.push([ev,fn]);}
  paint(true);
  if(root.querySelector('[data-rc-lab]')){a.guided=window.RCCircuitLab;a.guided.mount(root);}else if(root.querySelector('[data-gp-lab]')){a.guided=window.PhysicsApparatusLab;a.guided.mount(root);}
  return true;
 }
 const applies=(q,example='base')=>q?.subject==='physics'&&Number(q.chapter)===27&&example==='base';
 return{html,mount,unmount,applies,svg,restore,state:()=>active?{circuit:clone(active.circuit),selected:active.selected,tool:active.tool,pending:active.pending,running:false,measurement:active.result.measure(active.circuit.positive,active.circuit.negative),branches:clone(active.result.branches),undo:active.undo.length,redo:active.redo.length}:null};
})();
