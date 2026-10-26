/* Silent concept illustrations. They do not encode givens or reveal answers. */
(()=>{
const circle=(x,y,r,cls='')=>`<circle cx="${x}" cy="${y}" r="${r}" class="${cls}"/>`;
const path=(d,cls='')=>`<path d="${d}" class="${cls}"/>`;
const line=(x,y,X,Y,cls='')=>path(`M${x} ${y}L${X} ${Y}`,cls);
const dot=(x,y,cls='')=>circle(x,y,7,'loop-dot '+cls);
const arrow=(x,y,X,Y)=>line(x,y,X,Y)+path(`M${X-9} ${Y-7}L${X} ${Y}L${X-9} ${Y+7}`);
const waves=(ys=[80,120,160])=>ys.map((y,i)=>`<g class="loop-wave" style="animation-delay:${i*-.4}s">${path(`M-80 ${y}q30 -30 60 0t60 0t60 0t60 0t60 0t60 0t60 0`)}</g>`).join('');
const scenes={
 measure:()=>circle(180,120,69,'loop-soft')+`<g class="loop-spin" style="transform-origin:180px 120px">${line(180,120,249,120)}${dot(249,120)}</g>`+path('M85 207H275M85 199V215M132 202V212M180 199V215M228 202V212M275 199V215','loop-muted'),
 motion:()=>path('M35 170H325','loop-muted')+`<g class="loop-travel">${path('M65 147h50v-19H80l-15 19Z','loop-solid')}${circle(76,153,7,'loop-ink')}${circle(104,153,7,'loop-ink')}</g>`+path('M45 190H70M105 190H130M165 190H190M225 190H250M285 190H310','loop-muted'),
 vector:()=>line(65,180,310,180,'loop-muted')+line(65,180,65,45,'loop-muted')+`<g class="loop-draw">${path('M65 180L265 70L254 88M265 70L245 71')}${path('M265 70V180H65','loop-dashed')}</g>`,
 projectile:()=>path('M35 190H325','loop-muted')+path('M55 185Q180 -70 305 185','loop-dashed')+`<g class="loop-projectile">${dot(0,0)}</g>`,
 force:()=>path('M35 180H325','loop-muted')+`<g class="loop-nudge">${path('M150 105h65v65h-65Z','loop-soft')}${arrow(65,137,135,137)}</g>`,
 energy:()=>path('M50 185Q145 185 180 70T310 45','loop-muted')+`<g class="loop-energy">${dot(0,0)}</g>`+path('M60 210H300','loop-muted'),
 spring:()=>path('M70 65V185','loop-muted')+`<g class="loop-spring">${path('M70 125H90l10 -22 20 44 20 -44 20 44 20 -44 20 44 20 -44 10 22h35')}${path('M265 100h40v50h-40Z','loop-soft')}</g>`,
 collision:()=>path('M35 180H325','loop-muted')+`<g class="loop-collision-a">${circle(100,145,24,'loop-solid')}</g><g class="loop-collision-b">${circle(235,145,24,'loop-soft')}</g>`,
 wheel:()=>path('M40 195H320','loop-muted')+`<g class="loop-spin" style="transform-origin:180px 120px">${circle(180,120,70)}${line(110,120,250,120)}${line(180,50,180,190)}${line(130,70,230,170)}${line(130,170,230,70)}</g>`+circle(180,120,10,'loop-solid'),
 balance:()=>path('M180 125l-32 65h64Z','loop-soft')+`<g class="loop-balance">${line(65,120,295,120)}${path('M85 120v-28h38v28M237 120v-28h38v28','loop-soft')}</g>`,
 orbit:()=>circle(180,120,22,'loop-solid')+`<ellipse cx="180" cy="120" rx="112" ry="72" class="loop-dashed"/><g class="loop-orbit">${dot(0,0)}</g>`,
 fluid:()=>path('M65 55V190H295V55','loop-muted')+path('M65 116Q110 100 155 116T245 116T295 116V190H65Z','loop-soft')+`<g class="loop-bob">${path('M155 97h50v36h-50Z','loop-solid')}</g>`,
 wave:()=>waves(),sound:()=>dot(70,120)+[35,65,95,125].map((r,i)=>`<path d="M${70+r*.7} ${120-r*.7}Q${70+r*1.4} 120 ${70+r*.7} ${120+r*.7}" class="loop-ripple" style="animation-delay:${i*-.6}s"/>`).join(''),
 thermal:()=>path('M75 165H285M90 165V80H270V165','loop-soft')+[125,180,235].map((x,i)=>`<g class="loop-rise" style="animation-delay:${i*-.9}s">${path(`M${x} 150q-14 -18 0 -36t0 -36`)}</g>`).join(''),
 gas:()=>path('M70 50H290V190H70Z','loop-muted')+Array.from({length:10},(_,i)=>`<g class="loop-gas" style="--dx:${i%2?22:-22}px;--dy:${i%3?17:-17}px;animation-delay:${-i*.31}s">${dot(100+(i%5)*39,85+Math.floor(i/5)*65)}</g>`).join(''),
 charge:()=>circle(115,120,26,'loop-soft')+circle(245,120,26,'loop-soft')+path('M103 120h24M115 108v24M233 120h24')+[0,1,2].map(i=>`<ellipse cx="180" cy="120" rx="${70+i*25}" ry="${30+i*20}" class="loop-ripple" style="animation-delay:${-i}s"/>`).join(''),
 field:()=>[70,120,170].map((y,i)=>`<g class="loop-field" style="animation-delay:${-i*.4}s">${arrow(65,y,295,y)}</g>`).join('')+path('M45 45V195M315 45V195','loop-muted'),
 capacitor:()=>path('M140 55V185M220 55V185M55 120H140M220 120H305')+[85,120,155].map((y,i)=>`<g class="loop-pulse" style="animation-delay:${-i*.5}s">${line(155,y,205,y)}</g>`).join(''),
 current:()=>path('M35 92H325M35 148H325','loop-muted')+Array.from({length:7},(_,i)=>`<g class="loop-current" style="animation-delay:${-i*.7}s">${dot(45,120)}</g>`).join(''),
 circuit:()=>path('M95 120V55H290V185H95V145')+path('M78 120h34M85 145h20')+path('M195 55v-10h48v20h-48Z','loop-soft')+`<g class="loop-circuit">${dot(0,0)}</g>`,
 magnet:()=>path('M115 70h45v90h40V70h45v100q0 35 -35 35h-60q-35 0 -35 -35Z','loop-soft')+[0,1,2].map(i=>`<path d="M138 75Q180 ${-10+i*20} 222 75" class="loop-ripple" style="animation-delay:${-i*.7}s"/>`).join(''),
 induction:()=>Array.from({length:6},(_,i)=>`<ellipse cx="${135+i*18}" cy="125" rx="17" ry="65"/>`).join('')+`<g class="loop-nudge">${path('M45 110h65v30H45Z','loop-solid')}</g>`,
 light:()=>path('M180 40V200','loop-dashed')+`<g class="loop-draw">${path('M45 65L180 120L310 170')}</g>`+path('M180 40h145v160H180Z','loop-soft'),
 lens:()=>path('M180 40Q235 120 180 200Q125 120 180 40Z','loop-soft')+`<g class="loop-draw">${path('M40 75H180L305 160M40 165H180L305 80M40 120H315')}</g>`,
 interference:()=>waves([94,146])+path('M290 55V185','loop-muted'),
 diffraction:()=>path('M135 35V102M135 138V205','loop-muted')+[30,65,100,135].map((r,i)=>`<path d="M${145+r*.65} ${120-r*.65}Q${145+r*1.3} 120 ${145+r*.65} ${120+r*.65}" class="loop-ripple" style="animation-delay:${-i*.6}s"/>`).join('')+path('M40 80H115M40 120H115M40 160H115','loop-dashed'),
 photon:()=>waves([120])+path('M290 55V185','loop-muted')+circle(290,120,18,'loop-pulse loop-soft'),
 levels:()=>[65,120,180].map(y=>line(105,y,260,y,'loop-muted')).join('')+`<g class="loop-level">${dot(180,180)}</g>`,
 nucleus:()=>Array.from({length:9},(_,i)=>circle(155+(i%3)*25,95+Math.floor(i/3)*25,15,i%2?'loop-soft':'loop-solid')).join('')+circle(180,120,84,'loop-ripple'),
 particle:()=>path('M45 45L180 120L315 65M45 195L180 120L315 185','loop-dashed')+circle(180,120,17,'loop-pulse loop-solid')+[0,1,2].map(i=>`<g class="loop-particle" style="animation-delay:${-i}s">${dot(180,120)}</g>`).join('')
};
let observer;
window.PhysicsProblemScenes={html(q){const kind=window.PhysicsLoopMap?.[q.id];if(!kind||!scenes[kind])return '';return `<aside class="physics-loop" role="img" aria-label="Decorative ${kind} concept illustration; not a simulation of the problem’s numerical values"><svg viewBox="0 0 360 240" aria-hidden="true">${scenes[kind]()}</svg></aside>`;},layout(el){observer?.disconnect();if(!el.classList.contains('physics-study-work'))return;const v=el.querySelector(':scope > .physics-loop');if(!v)return;const row=document.createElement('div'),copy=document.createElement('div');row.className='physics-problem-pair';copy.className='physics-problem-copy';el.insertBefore(row,el.firstChild);while(row.nextSibling&&row.nextSibling!==v)copy.appendChild(row.nextSibling);row.append(copy,v);observer=new IntersectionObserver(entries=>{for(const e of entries)e.target.classList.toggle('loop-offscreen',!e.isIntersecting)});observer.observe(v);}};
})();
