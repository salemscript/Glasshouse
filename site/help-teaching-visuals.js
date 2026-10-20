/* Small, interactive teaching examples. These diagrams explain a concept;
   they do not pretend to be a worked solution to an unreviewed exercise. */
'use strict';
window.HelpTeachingVisuals = (() => {
  const esc = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const C={ink:'#24464b',muted:'#617476',grid:'#dce5df',aqua:'#137b80',coral:'#d85c50',gold:'#986b16',paper:'#fffdf4'};
  const num=x=>Number(Number(x).toFixed(3));
  const fmt=x=>Number.isFinite(x)?String(Number(x.toFixed(3))):'undefined';
  const clamp=(x,a,b)=>Math.min(b,Math.max(a,Number(x)||0));
  const text=(x,y,s,color=C.ink,size=15,anchor='start')=>`<text x="${num(x)}" y="${num(y)}" font-size="${size}" fill="${color}" text-anchor="${anchor}">${esc(s)}</text>`;
  const line=(x1,y1,x2,y2,color=C.grid,width=1,extra='')=>`<line x1="${num(x1)}" y1="${num(y1)}" x2="${num(x2)}" y2="${num(y2)}" stroke="${color}" stroke-width="${width}" ${extra}/>`;
  const dot=(x,y,color=C.aqua,r=6)=>`<circle cx="${num(x)}" cy="${num(y)}" r="${r}" fill="${color}" stroke="${C.paper}" stroke-width="2"/>`;
  // Polygon arrowheads avoid shared marker IDs when several tutors are on screen.
  function arrow(x1,y1,x2,y2,color=C.aqua,width=3){const a=Math.atan2(y2-y1,x2-x1),l=9;return line(x1,y1,x2,y2,color,width)+`<path d="M${num(x2)} ${num(y2)} L${num(x2-l*Math.cos(a-.48))} ${num(y2-l*Math.sin(a-.48))} L${num(x2-l*Math.cos(a+.48))} ${num(y2-l*Math.sin(a+.48))}Z" fill="${color}"/>`;}
  function graph(bounds,id){
    const [xmin,xmax,ymin,ymax]=bounds, X=x=>68+(x-xmin)/(xmax-xmin)*430, Y=y=>264-(y-ymin)/(ymax-ymin)*212;
    let background=`<defs><clipPath id="${id}-clip"><rect x="68" y="52" width="430" height="212"/></clipPath></defs>`;
    for(let x=Math.ceil(xmin);x<=xmax;x++) background+=line(X(x),52,X(x),264)+text(X(x),285,x,C.muted,12,'middle');
    for(let y=Math.ceil(ymin);y<=ymax;y++) if(y%2===0)background+=line(68,Y(y),498,Y(y))+text(56,Y(y)+4,y,C.muted,12,'end');
    background+=line(68,Y(0),506,Y(0),C.muted,1.5)+line(X(0),48,X(0),268,C.muted,1.5)+text(519,Y(0)+5,'x',C.muted,14)+text(X(0)+10,42,'y',C.muted,14);
    const curve=(fn,color=C.aqua,width=3)=>{let points='';for(let i=0;i<=150;i++){const x=xmin+(xmax-xmin)*i/150;points+=`${i?'L':'M'}${num(X(x))} ${num(Y(fn(x)))} `;}return `<path d="${points}" fill="none" stroke="${color}" stroke-width="${width}" clip-path="url(#${id}-clip)"/>`;};
    return{X,Y,background,curve,clip:body=>`<g clip-path="url(#${id}-clip)">${body}</g>`};
  }
  const definitions={
    increasing:{title:'Increasing means rising as you move right',intro:'Compare two inputs in left-to-right order. The signs of the outputs do not tell you whether the function is increasing.',defaults:{mode:'rising',x:-1,shift:0},options:[['mode','Example',[['rising','Rising line'],['falling','Falling line'],['turning','U-shaped curve']]]],ranges:[['x','Left input x₁',-2.5,1.5,.1],['shift','Move the graph up or down',-2,2,.5]]},
    'function-domain-range':{title:'One input must have exactly one output',intro:'Move the vertical line. Every intersection at that input is a possible output. Domain describes allowed inputs; range describes reached outputs.',defaults:{mode:'parabola',x:1},options:[['mode','Relation',[['parabola','y = x²'],['circle','x² + y² = 4']]]],ranges:[['x','Test an input x',-2,2,.1]]},
    'even-odd':{title:'Compare matching inputs x and −x',intro:'Even means f(−x) = f(x). Odd means f(−x) = −f(x). Check the relationship for all allowed inputs, not only one pair.',defaults:{mode:'even',x:1},options:[['mode','Example',[['even','Even: x²'],['odd','Odd: x³'],['neither','Neither: x + 1']]]],ranges:[['x','Distance from zero',.2,1.6,.1]]},
    derivative:{title:'A secant measures an interval; a tangent measures a point',intro:'For the teaching example f(x) = x², compare a point x with x + h. Shrink h to see the average rate approach the instantaneous rate.',defaults:{x:1,h:1},options:[],ranges:[['x','First input x',-1.5,1.5,.1],['h','Horizontal change h',-1.5,1.5,.05]]},
    forces:{title:'Balanced vertical forces do not guarantee balanced horizontal forces',intro:'This block starts at rest on a level surface. Increase the horizontal pull. Static friction matches the pull up to a limit; after the block starts sliding, kinetic friction is smaller.',defaults:{mass:10,pull:20,mu:.4},options:[],ranges:[['mass','Mass m (kg)',5,20,1],['pull','Horizontal pull F (N)',0,100,1],['mu','Static friction coefficient μₛ',0,.8,.05]]},
    'velocity-acceleration':{title:'Velocity gives direction; acceleration changes velocity',intro:'This cart starts at position zero. Change its starting velocity and constant acceleration, then run time. A negative acceleration can slow a right-moving cart or speed a left-moving cart.',defaults:{v:3,a:-1,t:0},options:[],ranges:[['v','Starting velocity v₀ (m/s)',-4,4,.5],['a','Acceleration a (m/s²)',-2,2,.25],['t','Time t (s)',0,4,.05]],animated:true}
  };
  const aliases={'increasing-function':'increasing','increasing-decreasing':'increasing',function:'function-domain-range',domain:'function-domain-range','domain-range':'function-domain-range',symmetry:'even-odd','even-odd-function':'even-odd',tangent:'derivative','secant-tangent':'derivative',velocity:'velocity-acceleration',acceleration:'velocity-acceleration',force:'forces',friction:'forces',equilibrium:'forces'};
  function kindOf(lesson){const raw=typeof lesson==='string'?lesson:typeof lesson?.visual==='string'?lesson.visual:lesson?.visual?.kind||lesson?.kind;return aliases[raw]||raw;}
  function valuesFor(kind,values={}){
    const d=definitions[kind];if(!d)return null;const v={...d.defaults};
    for(const [key,,choices]of d.options)if(choices.some(([choice])=>choice===values[key]))v[key]=values[key];
    for(const [key,,min,max]of d.ranges)if(values[key]!==undefined&&Number.isFinite(Number(values[key])))v[key]=clamp(values[key],min,max);
    return v;
  }
  function describe(lesson,values={},id='htv-example'){
    const kind=kindOf(lesson),v=valuesFor(kind,values);if(!v)return null;
    let body='',takeaway='',metrics={},equation='';
    if(kind==='increasing'){
      const g=graph([-3,3,-5,9],id), f=x=>(v.mode==='rising'?x-2:v.mode==='falling'?-x+2:x*x)+v.shift, x1=v.x,x2=v.x+1,y1=f(x1),y2=f(x2),rises=y2>y1;
      equation=v.mode==='rising'?`f(x) = x − 2 ${v.shift?`${v.shift>0?'+':'−'} ${fmt(Math.abs(v.shift))}`:''}`:v.mode==='falling'?`f(x) = −x + 2 ${v.shift?`${v.shift>0?'+':'−'} ${fmt(Math.abs(v.shift))}`:''}`:`f(x) = x² ${v.shift?`${v.shift>0?'+':'−'} ${fmt(Math.abs(v.shift))}`:''}`;
      body=g.background+g.curve(f)+g.clip(line(g.X(x1),g.Y(0),g.X(x1),g.Y(y1),C.coral,1.5,'stroke-dasharray="5 4"')+line(g.X(x2),g.Y(0),g.X(x2),g.Y(y2),C.aqua,1.5,'stroke-dasharray="5 4"')+dot(g.X(x1),g.Y(y1),C.coral)+dot(g.X(x2),g.Y(y2)))+text(68,312,`x₁ = ${fmt(x1)}  →  f(x₁) = ${fmt(y1)}`,C.coral,14)+text(315,312,`x₂ = ${fmt(x2)}  →  f(x₂) = ${fmt(y2)}`,C.aqua,14);
      takeaway=`The input increases from ${fmt(x1)} to ${fmt(x2)}. The output ${rises?'increases':y2<y1?'decreases':'stays equal'} from ${fmt(y1)} to ${fmt(y2)}. `+(v.mode==='rising'?'This line is increasing everywhere, even when its outputs are negative. Moving it up or down never changes that.':v.mode==='falling'?'This line is decreasing everywhere, even where its outputs are positive. Positive describes height; increasing describes change.':'This curve is concave up, but it decreases for x < 0 and increases for x > 0. One rising pair does not make it increasing on its entire domain.');
      metrics={x1,x2,y1,y2,increasesForPair:rises,increasingEverywhere:v.mode==='rising',concaveUp:v.mode==='turning'};
    }else if(kind==='function-domain-range'){
      const g=graph([-3,3,-3,5],id),circle=v.mode==='circle',ys=circle?[Math.sqrt(Math.max(0,4-v.x*v.x))]:[v.x*v.x];if(circle&&ys[0]>1e-9)ys.push(-ys[0]);
      body=g.background;if(circle){const p=[];for(let i=0;i<=120;i++){const a=i/120*Math.PI*2;p.push(`${i?'L':'M'}${num(g.X(2*Math.cos(a)))} ${num(g.Y(2*Math.sin(a)))}`);}body+=`<path d="${p.join(' ')}" fill="none" stroke="${C.aqua}" stroke-width="3"/>`;}else body+=g.curve(x=>x*x);
      body+=line(g.X(v.x),52,g.X(v.x),264,C.coral,2,'stroke-dasharray="5 4"')+ys.map(y=>dot(g.X(v.x),g.Y(y),C.coral)).join('')+text(68,312,`Input ${fmt(v.x)} → ${ys.length===1?'output':'outputs'} ${ys.map(fmt).join(' and ')}`,C.coral,15);
      equation=circle?'Relation: x² + y² = 4':'Function: f(x) = x²';
      takeaway=circle?`At x = ${fmt(v.x)}, the vertical line finds ${ys.length} ${ys.length===1?'output':'outputs'}: ${ys.map(fmt).join(' and ')}. The circle is not a function of x: other inputs have two outputs. Its domain and range are both [−2, 2].`:`At x = ${fmt(v.x)}, there is exactly one output: ${fmt(ys[0])}. The parabola passes the vertical-line test for every real input. Domain: all real numbers. Range: y ≥ 0.`;
      metrics={x:v.x,outputs:ys,isFunction:!circle,domain:circle?'[-2,2]':'R',range:circle?'[-2,2]':'[0,infinity)'};
    }else if(kind==='even-odd'){
      const g=graph([-2,2,-5,5],id),f=x=>v.mode==='even'?x*x:v.mode==='odd'?x*x*x:x+1,x=v.x,left=f(-x),right=f(x);
      body=g.background+g.curve(f)+g.clip(line(g.X(-x),g.Y(left),g.X(x),g.Y(right),C.gold,1.5,'stroke-dasharray="6 5"')+dot(g.X(-x),g.Y(left),C.coral)+dot(g.X(x),g.Y(right),C.aqua))+text(68,312,`f(−${fmt(x)}) = ${fmt(left)}`,C.coral,15)+text(322,312,`f(${fmt(x)}) = ${fmt(right)}`,C.aqua,15);
      equation=v.mode==='even'?'f(x) = x²;  f(−x) = f(x)':v.mode==='odd'?'f(x) = x³;  f(−x) = −f(x)':'f(x) = x + 1';
      takeaway=v.mode==='even'?`The outputs match: ${fmt(left)} = ${fmt(right)}. Reflection across the y-axis leaves x² unchanged; it is even.`:v.mode==='odd'?`The outputs are opposites: ${fmt(left)} = −(${fmt(right)}). Rotating 180° about the origin leaves x³ unchanged; it is odd.`:`The outputs ${fmt(left)} and ${fmt(right)} are neither equal nor opposites. x + 1 has neither symmetry. A domain must also contain −x whenever it contains x to use these definitions.`;
      metrics={x,left,right,even:v.mode==='even',odd:v.mode==='odd'};
    }else if(kind==='derivative'){
      const g=graph([-3,3,-2,10],id),x=v.x,h=v.h,y=x*x,x2=x+h,y2=x2*x2,tangent=2*x,secant=Math.abs(h)<1e-10?null:2*x+h;
      body=g.background+g.curve(z=>z*z)+g.curve(z=>tangent*(z-x)+y,C.gold,2.5);if(secant!==null)body+=g.curve(z=>secant*(z-x)+y,C.coral,2.5);
      body+=g.clip(line(g.X(x),g.Y(y),g.X(x2),g.Y(y),C.muted,2,'stroke-dasharray="4 3"')+line(g.X(x2),g.Y(y),g.X(x2),g.Y(y2),C.muted,2,'stroke-dasharray="4 3"')+dot(g.X(x),g.Y(y),C.aqua)+dot(g.X(x2),g.Y(y2),C.coral))+text(68,312,`Secant: ${secant===null?'undefined (0 ÷ 0)':fmt(secant)}`,C.coral,14)+text(335,312,`Tangent: ${fmt(tangent)}`,C.gold,14);
      equation='Secant = [f(x + h) − f(x)] / h;  tangent = f′(x)';
      takeaway=secant===null?`At h = 0, the secant quotient is 0 ÷ 0 and is undefined. The limiting slope still exists: f′(${fmt(x)}) = 2(${fmt(x)}) = ${fmt(tangent)}. The gold tangent is that limit.`:`Δx = ${fmt(h)} and Δy = ${fmt(y2-y)}. Dividing gives secant slope ${fmt(secant)} = 2x + h. The tangent slope is ${fmt(tangent)} = 2x. Make |h| smaller from either side: the coral line approaches the gold line.`;
      metrics={x,h,x2,y,y2,secant,tangent};
    }else if(kind==='forces'){
      const weight=v.mass*9.8,normal=weight,maxStatic=v.mu*normal,sliding=v.pull>maxStatic+1e-9,muK=.7*v.mu,friction=sliding?muK*normal:v.pull,net=v.pull-friction,acceleration=net/v.mass;
      const cx=280,cy=171.5,scale=.48;
      body=line(74,202,500,202,C.muted,2)+`<rect x="235" y="144" width="90" height="55" rx="5" fill="${C.aqua}" opacity=".16" stroke="${C.aqua}" stroke-width="2"/>`+text(cx,179,`${fmt(v.mass)} kg`,C.ink,16,'middle');
      body+=arrow(cx,144,cx,144-normal*scale,C.aqua,3)+arrow(cx,199,cx,199+weight*scale,C.gold,3);
      body+=v.pull?arrow(325,cy,325+v.pull*scale,cy,C.aqua,4):dot(325,cy,C.aqua,4);
      body+=friction?arrow(235,cy,235-friction*scale,cy,C.coral,4):dot(235,cy,C.coral,4);
      body+=text(338,67,`N = ${fmt(normal)} N`,C.aqua,14)+text(68,285,`mg = ${fmt(weight)} N`,C.gold,14)+text(395,159,`F = ${fmt(v.pull)} N`,C.aqua,14)+text(68,159,`f = ${fmt(friction)} N`,C.coral,14)+text(68,39,sliding?'Pull exceeds static friction: the block starts sliding.':'The block stays at rest: friction balances the pull.',C.ink,14)+text(68,316,`Horizontal net force: ${fmt(net)} N; acceleration: ${fmt(acceleration)} m/s²`,C.ink,14);
      equation=sliding?'N = mg;  fₖ = μₖN;  a = (F − fₖ) / m':'N = mg;  fₛ = F ≤ μₛN;  net force = 0';
      takeaway=`The upward normal force ${fmt(normal)} N balances the downward weight ${fmt(weight)} N. `+(sliding?`The pull ${fmt(v.pull)} N exceeds the static limit ${fmt(maxStatic)} N. The block starts sliding; using μₖ = 0.7μₛ = ${fmt(muK)}, friction is ${fmt(friction)} N and the horizontal net force is ${fmt(net)} N.`:`The pull ${fmt(v.pull)} N is at or below the static limit ${fmt(maxStatic)} N. Static friction supplies only the needed ${fmt(friction)} N, not automatically its maximum. Both directions balance, so acceleration is zero.`);
      metrics={mass:v.mass,pull:v.pull,weight,normal,maxStatic,muK,sliding,friction,net,acceleration};
    }else{
      const t=v.t,position=v.v*t+.5*v.a*t*t,velocity=v.v+v.a*t,acceleration=v.a,center=280+position*4,base=182;
      body=line(60,base+26,510,base+26,C.muted,2)+text(280,base+58,'Position x (m); right is positive',C.muted,14,'middle');
      for(let p=-48;p<=48;p+=12)body+=line(280+p*4,base+22,280+p*4,base+32,C.muted)+text(280+p*4,base+47,p,C.muted,11,'middle');
      body+=`<rect x="${num(center-20)}" y="${base-18}" width="40" height="24" rx="5" fill="${C.aqua}"/><circle cx="${num(center-12)}" cy="${base+9}" r="6" fill="${C.ink}"/><circle cx="${num(center+12)}" cy="${base+9}" r="6" fill="${C.ink}"/>`;
      body+=velocity?arrow(center,98,center+velocity*10,98,C.aqua,4):dot(center,98,C.aqua,4);
      body+=acceleration?arrow(center,136,center+acceleration*24,136,C.coral,4):dot(center,136,C.coral,4);
      body+=text(68,52,`t = ${fmt(t)} s    x = ${fmt(position)} m`,C.ink,17)+text(68,84,`Velocity: ${fmt(velocity)} m/s`,C.aqua,14)+text(68,126,`Acceleration: ${fmt(acceleration)} m/s²`,C.coral,14)+text(68,292,'Arrow direction shows sign. Arrow length shows magnitude.',C.muted,14);
      equation='x = v₀t + ½at²;  v = v₀ + at';
      const motion=Math.abs(velocity)<1e-10?'The cart is momentarily at rest.':`The cart moves ${velocity>0?'right':'left'} because v is ${velocity>0?'positive':'negative'}.`;
      const change=!acceleration?'Zero acceleration means constant velocity.':!velocity?'Acceleration tells you the direction it will begin moving next.':velocity*acceleration>0?'Velocity and acceleration have the same sign, so speed is increasing.':'Velocity and acceleration have opposite signs, so speed is decreasing until the cart turns.';
      takeaway=`${motion} ${change} After ${fmt(t)} s: v = ${fmt(v.v)} + (${fmt(v.a)})(${fmt(t)}) = ${fmt(velocity)} m/s.`;
      metrics={time:t,position,velocity,acceleration,speedingUp:velocity*acceleration>0};
    }
    const svg=`<svg viewBox="0 0 560 330" role="img" aria-label="${esc(takeaway)}" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Arial,sans-serif"><title>${esc(definitions[kind].title)}</title><desc>${esc(takeaway)}</desc><rect width="560" height="330" fill="${C.paper}"/>${body}</svg>`;
    return{kind,values:v,svg,equation,takeaway,metrics};
  }
  let serial=0,active=null;
  const select=(id,key,label,choices,value)=>`<label class="htv-select" for="${id}-${key}">${esc(label)}<select id="${id}-${key}" data-htv-control="${key}">${choices.map(([k,t])=>`<option value="${esc(k)}" ${k===value?'selected':''}>${esc(t)}</option>`).join('')}</select></label>`;
  const range=(id,key,label,min,max,step,value)=>`<label class="htv-range" for="${id}-${key}"><span>${esc(label)} <output data-htv-output="${key}" for="${id}-${key}">${fmt(value)}</output></span><input id="${id}-${key}" data-htv-control="${key}" type="range" min="${min}" max="${max}" step="${step}" value="${value}"></label>`;
  function html(lesson){const kind=kindOf(lesson),d=definitions[kind];if(!d)return'';const id=`htv-${++serial}`,f=describe(kind,{},id);return `<section class="help-teaching-visual" id="${id}" data-htv-kind="${kind}" aria-labelledby="${id}-title"><div class="htv-heading"><span class="htv-eyebrow">TRY A TEACHING EXAMPLE</span><h5 id="${id}-title">${esc(d.title)}</h5><p>${esc(d.intro)}</p></div><div class="htv-equation" data-htv-equation>${esc(f.equation)}</div><div class="htv-stage" data-htv-stage>${f.svg}</div><div class="htv-controls">${d.options.map(([key,label,choices])=>select(id,key,label,choices,d.defaults[key])).join('')}${d.ranges.map(([key,label,min,max,step])=>range(id,key,label,min,max,step,d.defaults[key])).join('')}${d.animated?`<div class="htv-playback"><button type="button" data-htv-action="play" aria-pressed="false">Run</button><button type="button" data-htv-action="reset">Reset time</button><span data-htv-play-status>Use the time slider to inspect any moment.</span></div>`:`<button type="button" class="htv-reset" data-htv-action="reset">Reset example</button>`}</div><p class="htv-takeaway" data-htv-takeaway>${esc(f.takeaway)}</p><p class="htv-note">This is a teaching example. Use the same idea on your question; these numbers are not its answer.</p></section>`;}
  function unmount(){if(!active)return;if(active.frame!==null)cancelAnimationFrame(active.frame);active.root.removeEventListener('input',active.input);active.root.removeEventListener('change',active.input);active.root.removeEventListener('click',active.click);active=null;}
  function mount(lesson,container){
    unmount();const kind=kindOf(lesson),d=definitions[kind];if(!d)return false;
    const candidates=(container||document).querySelectorAll('.help-teaching-visual');let root=null;for(const node of candidates)if(node.getAttribute('data-htv-kind')===kind)root=node;if(!root)return false;
    const state={root,kind,values:{...d.defaults},running:false,frame:null,last:null,id:root.id};active=state;
    const q=s=>root.querySelector(s),controls=()=>Array.from(root.querySelectorAll('[data-htv-control]'));
    function paint(){if(active!==state)return;const f=describe(kind,state.values,state.id);q('[data-htv-stage]').innerHTML=f.svg;q('[data-htv-equation]').textContent=f.equation;q('[data-htv-takeaway]').textContent=f.takeaway;for(const control of controls()){const key=control.getAttribute('data-htv-control');control.value=String(state.values[key]);const out=q(`[data-htv-output="${key}"]`);if(out)out.textContent=fmt(state.values[key]);}const play=q('[data-htv-action="play"]');if(play){play.textContent=state.running?'Pause':'Run';play.setAttribute('aria-pressed',String(state.running));}}
    function stop(){state.running=false;state.last=null;if(state.frame!==null)cancelAnimationFrame(state.frame);state.frame=null;}
    function tick(now){if(active!==state||!state.running)return;if(state.last!==null)state.values.t=Math.min(4,state.values.t+Math.min(.1,(now-state.last)/1000));state.last=now;if(state.values.t>=4){stop();q('[data-htv-play-status]').textContent='Finished at 4 seconds. Reset time or move the slider to run again.';}paint();if(state.running)state.frame=requestAnimationFrame(tick);}
    state.input=event=>{const key=event.target.getAttribute?.('data-htv-control');if(!key)return;stop();state.values=valuesFor(kind,{...state.values,[key]:event.target.value});if(d.animated)q('[data-htv-play-status]').textContent='Paused. Run to continue, or move the time slider.';paint();};
    state.click=event=>{const button=event.target.closest?.('[data-htv-action]');if(!button||!root.contains(button))return;const action=button.getAttribute('data-htv-action');if(action==='reset'){stop();state.values=d.animated?{...state.values,t:0}:{...d.defaults};if(d.animated)q('[data-htv-play-status]').textContent='Time reset to zero. Your velocity and acceleration settings are kept.';paint();}else if(action==='play'){if(state.running){stop();q('[data-htv-play-status]').textContent='Paused. Inspect the arrows or move the time slider.';}else if(window.matchMedia?.('(prefers-reduced-motion: reduce)').matches){q('[data-htv-play-status]').textContent='Reduced motion is enabled. Move the time slider to inspect each moment.';}else{if(state.values.t>=4)state.values.t=0;state.running=true;state.last=null;q('[data-htv-play-status]').textContent='Running: the arrows and position update as time passes.';state.frame=requestAnimationFrame(tick);}paint();}};
    root.addEventListener('input',state.input);root.addEventListener('change',state.input);root.addEventListener('click',state.click);paint();return true;
  }
  return{html,mount,unmount,describe,supported:()=>Object.keys(definitions),state:()=>active?{kind:active.kind,values:{...active.values},running:active.running}:null};
})();
