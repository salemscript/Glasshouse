'use strict';
window.Sim = (() => {
  let type = '', p = {}, time = 0, running = false, frame = 0, last = null, speed = 1;
  const supported = t => ['physics', 'dynamics', 'statics'].includes(t);
  const C = { ink:'#293a39', muted:'#697775', line:'#bfcac5', coral:'#d85549', aqua:'#27858b', pale:'#e8efea' };
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const finite = (x, fallback) => Number.isFinite(Number(x)) ? Number(x) : fallback;
  const f = (n, d = 2) => Number(n.toFixed(d)).toString();
  function normalize(t, raw = {}) {
    if(t === 'physics') return {angle:clamp(finite(raw.angle,30),0,85), mass:clamp(finite(raw.mass,5),.1,20)};
    if(t === 'dynamics') return {time:clamp(finite(raw.time,4),0,6), acc:clamp(finite(raw.acc,3),-5,5)};
    return {load:clamp(finite(raw.load,12),0,24), pos:clamp(finite(raw.pos,2),0,6)};
  }
  // Fixed units/scales make comparisons meaningful: no normalization by the current answer.
  function model(t, raw, elapsed = 0) {
    const q=normalize(t,raw), theta=(q.angle||0)*Math.PI/180;
    const end=t==='physics'?(theta>0?Math.sqrt(8/(9.81*Math.sin(theta))):5):t==='dynamics'?q.time:5;
    const at=clamp(finite(elapsed,0),0,end);
    if(t==='physics') {
      const a=9.81*Math.sin(theta),weight=q.mass*9.81,normal=weight*Math.cos(theta),parallel=weight*Math.sin(theta);
      return {...q,time:at,duration:end,x:Math.min(4,.5*a*at*at),v:a*at,a,theta,weight,normal,parallel,forceResidual:parallel-q.mass*a};
    }
    if(t==='dynamics') return {...q,time:at,duration:end,x:2*at+.5*q.acc*at*at,v:2+q.acc*at,a:q.acc,initialPart:2*at,accelerationPart:.5*q.acc*at*at};
    const ratio=at/5,load=q.load*ratio,left=load*(6-q.pos)/6,right=load*q.pos/6;
    return {...q,time:at,duration:end,fullLoad:q.load,ratio,load,left,right,forceResidual:left+right-load,momentResidual:6*right-load*q.pos};
  }
  const duration=()=>model(type,p,time).duration;
  const values=(at=time)=>model(type,p,at);
  function controls(t) {
    if(!supported(t))return '';
    return `<div class="sim-controls"><div class="row"><div class="sim-buttons"><button class="btn" id="sim-run">▶ Run</button><button class="btn light" id="sim-reset">↺ Reset</button><button class="btn light" id="sim-step" aria-label="Advance simulation one tenth of a second">Step +0.1</button></div><label class="sim-speed">Speed <select id="sim-speed" aria-label="Playback speed"><option value="0.25">0.25×</option><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label></div><label class="control sim-scrub"><span>${t==='statics'?'Load ramp progress':'Simulation time'}<b id="sim-time">Ready</b></span><input id="sim-scrub" aria-label="Scrub simulation timeline" type="range" min="0" max="1000" value="0" step="1"></label><div id="sim-readouts" class="sim-readouts" aria-live="off"><span>Ready. Run or Step to compare the force and motion model.</span></div><p class="plain-note" id="sim-description">${explanation(model(t,p,0))}</p><p class="plain-note sim-assist">Run, Step, and the timeline reveal results, so this variation counts as guided practice. Changing a given resets time; replay to compare.</p></div>`;
  }
  const text=(x,y,s,color=C.ink,size=13,anchor='start')=>`<text x="${x}" y="${y}" fill="${color}" style="fill:${color};font-size:${size}px" text-anchor="${anchor}">${s}</text>`;
  const line=(x,y,u,v,color=C.line,dash='')=>`<path d="M${x} ${y} L${u} ${v}" fill="none" stroke="${color}" stroke-width="1.5"${dash?' stroke-dasharray="'+dash+'"':''}/>`;
  function arrow(x,y,u,v,color=C.coral,role='') {
    if(Math.hypot(u-x,v-y)<.001)return '';
    return `<path${role?' data-role="'+role+'"':''} d="M${x} ${y} L${u} ${v}" fill="none" stroke="${color}" stroke-width="2.3" marker-end="url(#${color===C.aqua?'sim-aqua':'sim-coral'})"/>`;
  }
  function svg(label,body){return `<svg viewBox="0 0 600 360" role="img" aria-label="${label}"><defs>${[['sim-aqua',C.aqua],['sim-coral',C.coral]].map(([id,color])=>`<marker id="${id}" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="${color}"/></marker>`).join('')}</defs>${body}</svg>`;}
  function draw(t, parameters) {
    if(!supported(t))return '';
    const v=model(t,parameters||p,t===type?time:0);
    if(t==='physics') {
      const c=Math.cos(v.theta),s=Math.sin(v.theta),sx=64,sy=265-225*s,ex=sx+225*c,ey=265;
      const cx=sx+56.25*v.x*c+12*s,cy=sy+56.25*v.x*s-12*c,scale=.55;
      return svg(`Frictionless incline: weight ${f(v.weight)} N, normal force ${f(v.normal)} N, downslope force ${f(v.parallel)} N. Position ${f(v.x)} m at ${f(v.time)} s.`,
        `<path d="M${sx} ${sy} L${ex} ${ey} H${sx} Z" fill="${C.pale}" stroke="${C.line}"/>`+line(sx,sy,ex,ey,C.ink)+
        `<rect data-role="block" x="${cx-14}" y="${cy-11}" width="28" height="22" rx="3" fill="${C.ink}" transform="rotate(${v.angle} ${cx} ${cy})"/>`+
        arrow(cx,cy,cx,cy+v.weight*scale,C.coral,'weight')+
        arrow(cx,cy,cx+v.normal*s*scale,cy-v.normal*c*scale,C.aqua,'normal')+
        arrow(cx+7*s,cy-7*c,cx+7*s+v.parallel*c*scale,cy-7*c+v.parallel*s*scale,C.coral,'parallel')+
        text(326,34,'RESOLVE GRAVITY',C.muted,12)+text(326,64,`W = mg = ${f(v.weight)} N`)+text(326,89,`N = mg cos θ = ${f(v.normal)} N`,C.aqua)+
        text(326,114,`F∥ = mg sin θ = ${f(v.parallel)} N`,C.coral)+text(326,147,'F∥ = ma → a = g sin θ')+text(326,172,`a = ${f(v.a)} m/s²`)+
        text(326,204,`s = ½at² = ${f(v.x)} m`)+text(326,228,`v = at = ${f(v.v)} m/s`)+text(326,252,`t = ${f(v.time)} / ${f(v.duration)} s`)+
        text(64,290,`${v.angle}° · ${v.mass} kg · 4 m ramp`)+text(64,314,'Force scale stays fixed as mass changes.',C.muted,12)+
        text(64,338,'More mass → larger forces; the same acceleration.',C.ink,13));
    }
    if(t==='dynamics') {
      const X=x=>300+2.2*x,Y=y=>268-1.6*y,T=t=>60+80*t,cx=X(v.x),base=268;
      const points=Array.from({length:61},(_,j)=>{const at=v.time*j/60;return `${T(at)},${Y(2+v.a*at)}`;}).join(' ');
      const area=`${T(0)},${base} ${points} ${T(v.time)},${base}`;
      let body=text(40,25,'MOTION: fixed position and velocity scales',C.muted,12)+line(62,110,538,110);
      for(const x of[-100,-50,0,50,100])body+=line(X(x),106,X(x),115)+text(X(x),135,`${x} m`,C.muted,11,'middle');
      body+=`<circle cx="${X(0)}" cy="92" r="9" fill="none" stroke="${C.line}" stroke-dasharray="3 3"/><rect data-role="particle" x="${cx-10}" y="81" width="20" height="20" rx="4" fill="${C.ink}"/>`+
        arrow(cx,72,cx+1.2*v.v,72,C.aqua,'velocity')+arrow(cx,53,cx+8*v.a,53,C.coral,'acceleration')+text(577,57,'a',C.coral,12)+text(577,76,'v',C.aqua,12)+
        text(40,160,`x = v₀t + ½at² = ${f(v.initialPart)} + (${f(v.accelerationPart)}) = ${f(v.x)} m`)+
        text(40,184,`v = v₀ + at = 2 + (${f(v.a)} × ${f(v.time)}) = ${f(v.v)} m/s`)+
        line(60,207,60,318)+line(60,base,545,base)+`<polygon data-role="displacement-area" points="${area}" fill="${C.coral}" opacity=".16"/><polyline data-role="velocity-graph" points="${points}" fill="none" stroke="${C.aqua}" stroke-width="2.7"/><circle cx="${T(v.time)}" cy="${Y(v.v)}" r="4" fill="${C.aqua}"/>`;
      for(const at of[0,2,4,6])body+=text(T(at),332,`${at} s`,C.muted,11,'middle');
      for(const vy of[-20,20])body+=line(56,Y(vy),64,Y(vy))+text(50,Y(vy)+4,String(vy),C.muted,11,'end');
      body+=text(73,220,'v (m/s)',C.muted,11)+text(50,base+4,'0',C.muted,11,'end')+text(360,220,'Signed shaded area = displacement',C.coral,11)+text(300,354,`a = ${f(v.a)} m/s² · chosen end time = ${f(v.duration)} s`,C.ink,12,'middle');
      return svg(`Constant acceleration ${f(v.a)} m/s². Particle position ${f(v.x)} m; velocity ${f(v.v)} m/s at ${f(v.time)} seconds. The velocity graph has a fixed vertical scale; its signed area is displacement.`,body);
    }
    const x=90+70*v.pos,forceScale=2.2,leftFull=v.fullLoad*(6-v.pos)/6,rightFull=v.fullLoad*v.pos/6;
    return svg(`Stationary light beam with a load ${f(v.load)} kN at ${f(v.pos)} m from A. Reactions ${f(v.left)} and ${f(v.right)} kN balance force and moment.`,
      text(40,25,'EQUILIBRIUM: forces change; the rigid beam stays still',C.muted,12)+
      `<path d="M90 164 H510" stroke="${C.ink}" stroke-width="7"/><path d="M90 169 l-13 22 h26 Z M510 169 l-13 22 h26 Z" fill="${C.pale}" stroke="${C.ink}"/><circle cx="503" cy="198" r="3" fill="${C.ink}"/><circle cx="517" cy="198" r="3" fill="${C.ink}"/>`+
      `<g opacity=".2">${arrow(x,150-v.fullLoad*forceScale,x,150,C.coral,'full-load-outline')}${arrow(77,242,77,242-leftFull*forceScale,C.aqua)}${arrow(523,242,523,242-rightFull*forceScale,C.aqua)}</g>`+
      arrow(x,150-v.load*forceScale,x,150,C.coral,'applied-load')+text(x,85,`P = ${f(v.load)} kN`,C.coral,13,'middle')+
      arrow(77,242,77,242-v.left*forceScale,C.aqua,'reaction-a')+arrow(523,242,523,242-v.right*forceScale,C.aqua,'reaction-b')+
      text(77,263,`Aᵧ ${f(v.left)} kN`,C.aqua,12,'middle')+text(523,263,`Bᵧ ${f(v.right)} kN`,C.aqua,12,'middle')+
      line(90,55,x,55,C.coral)+text((90+x)/2,48,`d = ${f(v.pos)} m`,C.coral,12,'middle')+
      line(90,214,510,214)+text(300,234,'6 m span',C.muted,12,'middle')+
      text(300,286,`ΣMₐ = 0: Bᵧ × 6 = P × ${f(v.pos)}`,C.ink,14,'middle')+
      text(300,311,`ΣFᵧ = 0: Aᵧ + Bᵧ = P = ${f(v.load)} kN`,C.ink,14,'middle')+
      text(300,338,'Same force scale in every setting; faint arrows show full load.',C.muted,12,'middle'));
  }
  function explanation(v) {
    if(type==='physics')return `Gravity points down, but the surface blocks motion through the ramp. Its perpendicular part is balanced by N; only mg sin θ accelerates the block. Doubling mass doubles both force and inertia, so a = g sin θ stays the same. No friction or drag; playback ends at 4 m before modeling impact.`;
    if(type==='dynamics')return `Acceleration is the slope of v(t). The shaded signed area under v(t) is displacement: a rectangle v₀t plus a triangle ½at². Increasing acceleration steepens the graph and moves the particle farther at the same time. All comparisons keep the same axes. Current displacement: ${f(v.x)} m.`;
    return `The beam is rigid and its weight is neglected. Run gradually applies the load; this is quasi-static construction, not a bending or vibration model. Taking moments about A removes Aᵧ: Bᵧ = Pd/6. Moving P toward B increases its moment arm and B’s share. Doubling P doubles both reactions; equal total reaction keeps ΣFᵧ = 0.`;
  }
  function paint(){
    const diagram=document.querySelector('#diagram');if(!diagram||!supported(type))return;
    const v=values(),percent=v.duration?time/v.duration:0;diagram.innerHTML=draw(type,p);
    document.querySelector('#sim-time').textContent=type==='statics'?`${f(percent*100,0)}%`:`${f(time)} / ${f(v.duration)} s`;
    document.querySelector('#sim-scrub').value=Math.round(percent*1000);document.querySelector('#sim-speed').value=String(speed);
    document.querySelector('#sim-run').textContent=running?'Ⅱ Pause':time>=v.duration?'↺ Replay':'▶ Run';
    document.querySelector('#sim-description').textContent=explanation(v);
    document.querySelector('#sim-readouts').innerHTML=type==='statics'?`<span>Applied load <b>${f(v.load)} kN</b></span><span>Aᵧ <b>${f(v.left)} kN</b></span><span>Bᵧ <b>${f(v.right)} kN</b></span>`:`<span>Position <b>${f(v.x)} m</b></span><span>Velocity <b>${f(v.v)} m/s</b></span><span>Acceleration <b>${f(v.a)} m/s²</b></span>`;
  }
  function stop(){running=false;if(frame)cancelAnimationFrame(frame);frame=0;last=null;}
  function configure(t,parameters){stop();type=t;p=normalize(t,parameters);time=0;speed=1;}
  function reset(){stop();time=0;paint();}
  function tick(now){if(!running)return;if(last!==null)time=Math.min(duration(),time+Math.min(.1,Math.max(0,(now-last)/1000))*speed);last=now;if(time>=duration())stop();paint();if(running)frame=requestAnimationFrame(tick);}
  function explore(){if(typeof Sim.onExplore==='function')Sim.onExplore();}
  document.addEventListener('click',e=>{const id=e.target.closest('button')?.id;if(id==='sim-run'){if(running){stop();paint();}else{explore();if(time>=duration())time=0;running=true;last=null;paint();frame=requestAnimationFrame(tick);}}else if(id==='sim-reset')reset();else if(id==='sim-step'){explore();stop();time=Math.min(duration(),time+.1);paint();}});
  document.addEventListener('input',e=>{if(e.target.id==='sim-scrub'){explore();stop();time=clamp(finite(e.target.value,0)/1000,0,1)*duration();paint();}});
  document.addEventListener('change',e=>{if(e.target.id==='sim-speed')speed=clamp(finite(e.target.value,1),.25,2);});
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&running){stop();paint();}});
  return {supported,controls,draw,configure,stop,reset,paint,values,duration,model,onExplore:null,state:()=>({type,time,running,speed})};
})();
