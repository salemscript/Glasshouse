/* Original Glasshouse beam model. Rigid-body equilibrium, not a deflection animation. */
window.StaticsEquilibriumLab = (() => {
  'use strict';
  const DEFAULT=Object.freeze({span:8,load:12,intensity:2,position:2,shape:'point',phase:0,pivot:'A'});
  const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
  const fmt=n=>Number.isFinite(n)?Number(n.toPrecision(4)).toString():'—';
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let active=null;
  function normalise(input={}) {
    const s={...DEFAULT,...input};
    for(const [key,min,max] of [['span',2,10],['load',0,20],['intensity',0,4],['position',0,10],['phase',0,3]]) {
      const n=Number(s[key]);s[key]=Number.isFinite(n)?clamp(n,min,max):DEFAULT[key];
    }
    s.position=clamp(s.position,0,s.span);s.shape=['uniform','triangle'].includes(s.shape)?s.shape:'point';s.pivot=s.pivot==='B'?'B':'A';return s;
  }
  function defaults(section='5.2') {return {...DEFAULT,...(String(section)==='4.9'?{shape:'triangle',span:6,intensity:4}:{} )};}
  function describe(input={}) {
    const s=normalise(input),W=s.shape==='point'?s.load:s.intensity*s.span*(s.shape==='triangle'?.5:1);
    const centroid=s.shape==='point'?s.position:s.span*(s.shape==='triangle'?2/3:.5),By=W*centroid/s.span,Ay=W-By;
    const moment=W*centroid,otherMoment=W*(s.span-centroid);
    return {...s,W,centroid,Ay,By,moment,otherMoment,netForce:Ay+By-W,netMoment:By*s.span-moment,
      geometry:{left:110,right:110+74*s.span,loadX:110+74*centroid,pxPerMeter:74,forceScale:4,intensityScale:20,
        downLength:4*W,leftLength:4*Ay,rightLength:4*By,intensityHeight:20*s.intensity},
      stage:Math.floor(s.phase),zero:W===0};
  }
  function applies(q,example='base') {return q?.subject==='statics'&&['4.9','5.2'].includes(String(q.section))&&example==='base';}
  const line=(x1,y1,x2,y2,klass='steq-line',extra='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${klass}" ${extra}/>`;
  const text=(x,y,s,klass='steq-label',anchor='middle')=>`<text x="${x}" y="${y}" class="${klass}" text-anchor="${anchor}">${esc(s)}</text>`;
  function arrow(x1,y1,x2,y2,klass) {
    const len=Math.hypot(x2-x1,y2-y1);if(len<.001)return `<circle cx="${x2}" cy="${y2}" r="3" class="${klass} steq-zero"/>`;
    const ux=(x2-x1)/len,uy=(y2-y1)/len,h=Math.min(9,len*.5),w=h*.45;
    return line(x1,y1,x2,y2,klass)+`<path d="M${x2-ux*h-uy*w} ${y2-uy*h+ux*w} L${x2} ${y2} L${x2-ux*h+uy*w} ${y2-uy*h-ux*w}" class="${klass}" fill="none"/>`;
  }
  function dimension(x1,x2,y,label,klass='steq-dimension') {return line(x1,y,x2,y,klass)+line(x1,y-5,x1,y+5,klass)+line(x2,y-5,x2,y+5,klass)+text((x1+x2)/2,y-10,label,'steq-small');}
  function svg(input={}) {
    const m=describe(input),g=m.geometry,A=g.left,B=g.right,X=g.loadX,point=m.shape==='point',stage=m.stage;
    let body='<title>A load, its equivalent force, and beam support reactions</title><desc>The upper beam shows the real applied load on a pin and roller. The separate lower beam replaces the loading by its resultant, then adds support reactions. Force arrows use a fixed scale. The beam remains rigid and stationary.</desc>';
    body+=text(480,30,'1 · THE LOADED BEAM','steq-caption')+line(A,170,B,170,'steq-beam');
    // Pin at A, roller at B. These icons belong only to the supported-body panel.
    body+=`<path d="M${A} 177l-15 23h30z" class="steq-support"/><path d="M${B} 177l-15 20h30z" class="steq-support"/><circle cx="${B-8}" cy="203" r="5" class="steq-support"/><circle cx="${B+8}" cy="203" r="5" class="steq-support"/>`;
    body+=line(A-24,204,A+24,204)+line(B-24,211,B+24,211)+text(A,233,'A · pin','steq-small')+text(B,233,'B · roller','steq-small');
    if(point) {
      body+=`<g data-steq-handle role="slider" tabindex="0" aria-label="Point load position in metres; drag or use left and right arrows" aria-valuemin="0" aria-valuemax="${m.span}" aria-valuenow="${m.position}" aria-valuetext="${fmt(m.position)} metres from A"><rect x="${X-22}" y="122" width="44" height="55" rx="8" class="steq-handle"/><path d="M${X-10} 144h20m-20 0l5-5m-5 5l5 5m15-5l-5-5m5 5l-5 5" class="steq-handle-mark"/></g>`;
      body+=arrow(X,160-4*m.load,X,160,'steq-force')+text(clamp(X,200,760),67,`P = ${fmt(m.load)} kN`,'steq-force-label');
    } else {
      const H=20*m.intensity;
      body+=`<path d="M${A} 160 L${A} ${m.shape==='triangle'?160:160-H} L${B} ${160-H} L${B} 160 Z" class="steq-load-area"/>`;
      for(let i=0;i<=12;i++){const x=A+(B-A)*i/12,h=H*(m.shape==='triangle'?i/12:1);body+=arrow(x,160-h,x,160,'steq-intensity');}
      body+=text(480,67,`${m.shape==='triangle'?'Peak':'Uniform'} intensity w = ${fmt(m.intensity)} kN/m`,'steq-force-label');
    }
    body+=dimension(A,B,262,`L = ${fmt(m.span)} m · geometry stays at 74 px/m`);
    body+=text(480,291,point?'Drag the coral handle, or change the position slider.':'Repeated arrows show intensity, not separate forces to add.','steq-small');
    body+=text(480,326,'2 · ISOLATED FREE BODY — AN ALTERNATIVE, NOT AN EXTRA LOAD','steq-caption');
    body+=line(A,495,B,495,'steq-beam');
    if(stage>=1) {
      body+=arrow(X,495-g.downLength,X,495,'steq-force')+text(X+(X>700?-15:15),370,`W = ${fmt(m.W)} kN`,'steq-force-label',X>700?'end':'start');
      body+=dimension(A,X,395,`${point?'x':'x̄'} = ${fmt(m.centroid)} m`);
      body+=`<circle cx="${m.pivot==='A'?A:B}" cy="495" r="12" class="steq-pivot"/>`;
      body+=text(m.pivot==='A'?A-25:B+25,488,`↺ ${m.pivot}`, 'steq-pivot-label',m.pivot==='A'?'end':'start');
    }
    if(stage>=2) {
      body+=arrow(A,495+g.leftLength,A,495,'steq-reaction')+arrow(B,495+g.rightLength,B,495,'steq-reaction');
      body+=text(A-18,535,`Ay = ${fmt(m.Ay)}`,'steq-reaction-label','end')+text(B+18,535,`By = ${fmt(m.By)}`,'steq-reaction-label','start');
      body+=text(480,610,'All forces: 4 px/kN · intensity: 20 px/(kN/m) · no invented deflection','steq-small');
    } else body+=text(480,610,'Next step builds the external free body; the beam is not moving.','steq-small');
    if(stage===3)body+=text(480,578,`ΣFy = ${fmt(m.Ay)} + ${fmt(m.By)} − ${fmt(m.W)} = 0 kN`,'steq-check');
    return `<svg viewBox="0 0 960 635" class="steq-svg" xmlns="http://www.w3.org/2000/svg" role="group" aria-label="${esc(`${m.shape} loading. A reaction ${fmt(m.Ay)} kilonewtons and B reaction ${fmt(m.By)} kilonewtons. Stage ${stage+1} of 4.`)}">${body}</svg>`;
  }
  function steps(input={}) {
    const m=describe(input),point=m.shape==='point',area=m.shape==='triangle'?'½wL':'wL';
    const force=point?`W = P = ${fmt(m.W)} kN`:`W = ${area} = ${m.shape==='triangle'?'½ × ':''}${fmt(m.intensity)} × ${fmt(m.span)} = ${fmt(m.W)} kN`;
    const centroid=point?`x = ${fmt(m.centroid)} m`:`x̄ = ${m.shape==='triangle'?'2L/3':'L/2'} = ${fmt(m.centroid)} m`;
    return [
      {title:'Choose the body and its constraints',why:'The pin prevents translation, so it can supply Ax and Ay. The smooth roller supplies only an upward normal reaction By. Both allow rotation; neither supplies a reaction couple. No horizontal load means Ax = 0. The supported beam is not yet an isolated free-body diagram.',equation:'ΣFx = Ax = 0',look:'The upper panel shows the actual beam and supports. Coral shows the applied loading; supports are hardware, not additional applied forces.'},
      {title:point?'Follow the force line':'Replace the distributed loading',why:point?'The point force acts at its own location. Measure x from A to its vertical line of action, not to the end of the beam.':`Total force is the ${m.shape==='triangle'?'triangle':'rectangle'} area under the intensity distribution. Its line of action passes through the area centroid. ${m.shape==='triangle'?'The triangular centroid is two thirds from the zero-intensity end, not at midspan.':'The uniform rectangle is symmetric, so its centroid is at midspan.'} The lower panel replaces the original loading; never add both.`,equation:`${force}; ${centroid}`,look:m.zero?'All loads are zero. The displayed position is a retained geometric reference; a zero-area distributed load has no unique physical centroid.':'The lower force is the same external loading. Its coral arm is measured from A; the ring marks the chosen moment center.'},
      {title:`Balance rotation about ${m.pivot}`,why:m.pivot==='A'?'A’s reactions have zero moment arm about A. The downward load produces clockwise moment W×x̄. By at distance L must provide the equal counterclockwise moment. Divide that moment by L to find By.':'B’s reaction has zero moment arm about B. The downward force to the left produces counterclockwise moment W(L−x̄). Ay produces the opposing clockwise moment. Divide by L to find Ay.',equation:m.pivot==='A'?`ΣMA = By L − W x̄ = 0; By = (${fmt(m.W)} × ${fmt(m.centroid)}) / ${fmt(m.span)} = ${fmt(m.By)} kN`:`ΣMB = W(L − x̄) − Ay L = 0; Ay = (${fmt(m.W)} × ${fmt(m.span-m.centroid)}) / ${fmt(m.span)} = ${fmt(m.Ay)} kN`,look:'Aqua arrows show both support reactions on the same 4 px/kN scale as the coral resultant. Their lengths respond to load position and magnitude; they are not normalized independently.'},
      {title:'Balance vertical force, then check',why:`${m.pivot==='A'?'Ay = W − By':'By = W − Ay'}. The upward reactions must sum to the downward load. A second moment check about the opposite support must also vanish. Moving a point load right transfers reaction from A to B; a full uniform load stays symmetric. Equilibrium does not mean the individual forces are zero.`,equation:`Ay + By − W = ${fmt(m.Ay)} + ${fmt(m.By)} − ${fmt(m.W)} = 0 kN; ΣM${m.pivot==='A'?'B':'A'} = 0 kN·m`,look:'The green balance statement checks the same forces drawn above. Nothing sways or bends: this model solves rigid-body equilibrium, not elastic deformation.'}
    ];
  }
  function target(input={},part='By') {const m=describe(input);return {answer:part==='Ay'?m.Ay:part==='W'?m.W:part==='centroid'?m.centroid:m.By,unit:part==='centroid'?'m':'kN',label:part==='centroid'?(m.zero&&m.shape!=='point'?'a reference distance from A (with no load, there is no combined force to locate)':'the load line measured from A'):part==='W'?'the total downward force':`${part==='Ay'?'left':'right'} support reaction ${part==='Ay'?'Ay':'By'}`};}
  function grade(input,response,part='By') {
    const q=target(input,part),s=String(response??'').trim();if(!/^[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?$/i.test(s))return {correct:false,message:'Enter a numerical value; scientific notation is allowed.'};
    const correct=Math.abs(Number(s)-q.answer)<=Math.max(1e-7,Math.abs(q.answer)*.001);
    return {correct,message:correct?'Correct. Your value agrees with the drawn free body.':`Try again. ${part==='centroid'?'Use the point location, L/2 for uniform, or 2L/3 from the zero end for the triangle.':part==='W'?'Total force is P for a point, wL for uniform, or ½wL for a triangular load.':'Take moments about the opposite support: reaction × L equals load × its perpendicular arm.'} Use ${q.unit}.`};
  }
  function html({section='5.2'}={}) {
    const s=defaults(section),m=describe(s);
    return `<section class="statics-equilibrium-lab" data-statics-equilibrium-lab data-steq-section="${esc(section)}" aria-label="Beam forces and equilibrium lab"><header><span class="secl-eyebrow">ORIGINAL Glasshouse TEACHING MODEL · STATICS ${esc(section)}</span><h3>Move the load. See what the supports do.</h3><p>Manipulate the actual beam, follow the force’s line of action, and build the equations from its free-body diagram.</p></header><div class="steq-scene" data-steq-scene tabindex="0" role="region" aria-label="Interactive beam. On a small screen scroll horizontally to inspect labels.">${svg(s)}</div><p class="steq-note">The two panels are alternative representations of one loading. Run builds reasoning, not physical motion. This is a rigid, massless beam; no deflection or stress is simulated.</p><div class="steq-controls"><div><label>Applied loading<select data-steq-shape><option value="point" ${s.shape==='point'?'selected':''}>Movable point force</option><option value="uniform">Full-span uniform load</option><option value="triangle" ${s.shape==='triangle'?'selected':''}>Triangle, increasing toward B</option></select></label>${[['span','Beam length L',2,10,.25,s.span,'m'],['load','Point force P',0,20,.5,s.load,'kN'],['intensity','Load intensity w (peak for triangle)',0,4,.1,s.intensity,'kN/m'],['position','Point position x from A',0,s.span,.1,s.position,'m']].map(([key,label,min,max,step,value,unit])=>`<label data-steq-label="${key}">${label}<output data-steq-output="${key}">${value} ${unit}</output><input type="range" data-steq-param="${key}" min="${min}" max="${max}" step="${step}" value="${value}" aria-label="${label} in ${unit}"></label>`).join('')}<label>Moment center<select data-steq-pivot><option value="A">A · eliminate Ay</option><option value="B">B · eliminate By</option></select></label></div><div><div class="steq-transport"><button type="button" data-steq-action="back">← Back</button><button type="button" data-steq-action="play" aria-pressed="false">Run</button><button type="button" data-steq-action="next">Next step →</button><button type="button" data-steq-action="reset">Reset</button></div><p data-steq-status class="steq-note" role="status">Ready. Step through the explanation or move a control.</p><section data-steq-teaching class="steq-teaching" aria-live="polite"></section></div></div><details class="steq-practice"><summary>Check a prediction</summary><label>Find<select data-steq-part><option value="By">Right reaction By</option><option value="Ay">Left reaction Ay</option><option value="W">Total downward force W</option><option value="centroid">Load line x / x̄ from A</option></select></label><p data-steq-prompt>For these controls, find the right support reaction By in kN.</p><div class="steq-answer"><label>Numerical answer<input type="number" step="any" inputmode="decimal" data-steq-answer aria-label="Numerical prediction"></label><button type="button" data-steq-action="check">Check</button><button type="button" data-steq-action="solution">Show calculation</button></div><p data-steq-feedback role="status"></p><div data-steq-solution hidden></div></details><p class="steq-source">Original interactive drawing, aligned to the book’s §4.9 distributed-load reduction and §5.2 free-body diagrams. Teaching references: <a href="https://engineeringstatics.org/distributed-loads.html" target="_blank" rel="noopener">Engineering Statics: Distributed Loads</a> and <a href="https://engineeringstatics.org/Chapter_05-free-body-diagrams.html" target="_blank" rel="noopener">Free-Body Diagrams</a>. This starter is an exploratory model; select a source-linked example above for an exact existing exercise. Loads stay within the supports, downward and nonnegative; no applied couple, beam self-weight, settlement or horizontal load. External load equivalence does not preserve internal shear or bending distribution.</p></section>`;
  }
  function unmount() {if(!active)return;const a=active;stop(a);a.media?.removeEventListener?.('change',a.motion);for(const [event,handler] of Object.entries(a.events))a.root.removeEventListener(event,handler);active=null;}
  function stop(a) {a.running=false;a.last=null;if(a.frame!==null)cancelAnimationFrame(a.frame);a.frame=null;}
  function mount(container=document) {
    unmount();const root=container.matches?.('[data-statics-equilibrium-lab]')?container:container.querySelector?.('[data-statics-equilibrium-lab]');if(!root)return false;
    const a={root,s:defaults(root.getAttribute('data-steq-section')),part:'By',running:false,frame:null,last:null,showSolution:false,drag:null,events:{}};active=a;
    const find=s=>root.querySelector(s),status=s=>{find('[data-steq-status]').textContent=s;};
    function clear(){a.showSolution=false;find('[data-steq-answer]').value='';find('[data-steq-feedback]').textContent='';}
    function paint({focusHandle=false}={}) {
      if(active!==a)return;const m=describe(a.s);a.s=normalise(a.s);find('[data-steq-scene]').innerHTML=svg(a.s);
      if(focusHandle)find('[data-steq-handle]')?.focus();
      for(const key of ['span','load','intensity','position']){find(`[data-steq-param="${key}"]`).value=String(a.s[key]);find(`[data-steq-output="${key}"]`).textContent=`${fmt(a.s[key])} ${key==='span'||key==='position'?'m':key==='load'?'kN':'kN/m'}`;}
      find('[data-steq-param="position"]').max=String(m.span);find('[data-steq-shape]').value=m.shape;find('[data-steq-pivot]').value=m.pivot;
      for(const key of ['load','position','intensity'])find(`[data-steq-label="${key}"]`).hidden=key==='intensity'?m.shape==='point':m.shape!=='point';
      const rows=steps(a.s),row=rows[m.stage];find('[data-steq-teaching]').innerHTML=`<b>Step ${m.stage+1} / 4 · ${esc(row.title)}</b><p>${esc(row.why)}</p><div class="steq-equation">${esc(row.equation)}</div><p class="steq-note">${esc(row.look)}</p>`;
      const run=find('[data-steq-action="play"]');run.textContent=a.running?'Pause':'Run';run.setAttribute('aria-pressed',String(a.running));find('[data-steq-action="back"]').disabled=m.phase<=0;find('[data-steq-action="next"]').disabled=m.phase>=3;
      const q=target(a.s,a.part);find('[data-steq-prompt]').textContent=`For these controls, find ${q.label} in ${q.unit}.`;
      const solution=find('[data-steq-solution]');solution.hidden=!a.showSolution;
      if(a.showSolution)solution.innerHTML=`<ol>${rows.map(row=>`<li><b>${esc(row.title)}</b><p>${esc(row.why)}</p><div class="steq-equation">${esc(row.equation)}</div></li>`).join('')}</ol><p><b>Final answer: ${esc(fmt(q.answer))} ${q.unit}</b></p>`;
    }
    function tick(now) {if(active!==a||!a.running)return;if(root.isConnected===false){unmount();return;}if(a.last!==null)a.s.phase=clamp(a.s.phase+Math.min(.1,Math.max(0,(now-a.last)/1000))*.45,0,3);a.last=now;if(a.s.phase>=3){stop(a);status('Complete. Change the load or check a prediction.');}paint();if(a.running)a.frame=requestAnimationFrame(tick);}
    a.events.input=e=>{const key=e.target.getAttribute?.('data-steq-param');if(!['span','load','intensity','position'].includes(key))return;stop(a);a.s[key]=Number(e.target.value);a.s=normalise(a.s);clear();status('Paused. Geometry, force scale and equation use the changed values.');paint();};
    a.events.change=e=>{if(e.target.hasAttribute?.('data-steq-shape')){stop(a);a.s.shape=e.target.value;clear();paint();}else if(e.target.hasAttribute?.('data-steq-pivot')){a.s.pivot=e.target.value;paint();}else if(e.target.hasAttribute?.('data-steq-part')){a.part=e.target.value;clear();paint();}};
    a.events.click=e=>{const b=e.target.closest?.('[data-steq-action]');if(!b||!root.contains(b))return;const action=b.getAttribute('data-steq-action');if(action==='check'){const r=grade(a.s,find('[data-steq-answer]').value,a.part);find('[data-steq-feedback]').textContent=r.message;return;}if(action==='solution'){a.showSolution=!a.showSolution;paint();return;}if(action==='reset'){stop(a);a.s=defaults(root.getAttribute('data-steq-section'));clear();status('Reset to this section’s original teaching example.');paint();return;}if(action==='back'||action==='next'){stop(a);a.s.phase=clamp(Math.floor(a.s.phase)+(action==='back'?-1:1),0,3);paint();return;}if(action==='play'){if(a.running){stop(a);status('Paused.');paint();return;}if(a.s.phase>=3)a.s.phase=0;if(typeof matchMedia==='function'&&matchMedia('(prefers-reduced-motion: reduce)').matches){a.s.phase=clamp(Math.floor(a.s.phase)+1,0,3);status('Reduced motion: advanced one step.');paint();return;}a.running=true;a.last=null;status('Building the reasoning. This is not physical time.');paint();a.frame=requestAnimationFrame(tick);}};
    function drag(e){if(a.drag===null||a.s.shape!=='point')return;const box=find('.steq-svg').getBoundingClientRect(),viewX=(e.clientX-box.left)*960/box.width;a.s.position=Math.round(clamp((viewX-110)/74,0,a.s.span)*10)/10;clear();paint();}
    a.events.pointerdown=e=>{if(!e.target.closest?.('[data-steq-handle]'))return;e.preventDefault();stop(a);a.drag=e.pointerId;root.setPointerCapture?.(e.pointerId);drag(e);};
    a.events.pointermove=e=>{if(a.drag===e.pointerId)drag(e);};
    const release=e=>{if(a.drag!==e.pointerId)return;root.releasePointerCapture?.(e.pointerId);a.drag=null;};a.events.pointerup=release;a.events.pointercancel=release;
    a.events.keydown=e=>{if(e.target.closest?.('[data-steq-handle]')&&['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();stop(a);a.s.position=e.key==='Home'?0:e.key==='End'?a.s.span:clamp(a.s.position+(e.key==='ArrowLeft'?-.1:.1),0,a.s.span);clear();paint({focusHandle:true});}else if(e.key==='Enter'&&e.target.hasAttribute?.('data-steq-answer')){e.preventDefault();find('[data-steq-action="check"]').click();}};
    a.media=typeof matchMedia==='function'?matchMedia('(prefers-reduced-motion: reduce)'):null;a.motion=()=>{if(a.media?.matches&&a.running){stop(a);status('Reduced motion enabled. Use Next step to inspect the reasoning.');paint();}};a.media?.addEventListener?.('change',a.motion);for(const [event,handler] of Object.entries(a.events))root.addEventListener(event,handler);paint();return true;
  }
  return {applies,html,mount,unmount,state:()=>active?{...active.s,running:active.running,part:active.part,revealed:active.showSolution}:null,defaults,normalise,describe,svg,steps,target,grade};
})();
