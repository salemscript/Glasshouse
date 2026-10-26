/* NODE_PATH=/tmp/glasshouse-ui-checks/node_modules node scripts/appearance/check-workspace.cjs */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),{parseHTML}=require('linkedom');
const site=path.resolve(__dirname,'../../site'),{document,Event}=parseHTML('<html><body><main id="main"></main></body></html>');
// Linkedom omits the browser's HTMLSelectElement.value setter.
const selectProto=Object.getPrototypeOf(document.createElement('select'));
Object.defineProperty(selectProto,'value',{configurable:true,get(){return this.querySelector('option[selected]')?.value||this.querySelector('option')?.value||''},set(value){for(const o of this.querySelectorAll('option')){if(o.value===String(value))o.setAttribute('selected','');else o.removeAttribute('selected')}}});
let frame=0,queue=new Map(),reduced=false;
const c={document,Event,console,Math,performance:{now:()=>0},matchMedia:()=>({get matches(){return reduced},addEventListener(){},removeEventListener(){}}),requestAnimationFrame:fn=>{queue.set(++frame,fn);return frame},cancelAnimationFrame:id=>queue.delete(id)};c.window=c;vm.createContext(c);
const index=fs.readFileSync(site+'/index.html','utf8');
const scripts=[...index.matchAll(/<script src="([^"?]+)/g)].map(m=>m[1]).filter(f=>f==='solution-math.js'||f==='physics-apparatus-lab.js'||f.startsWith('physics-lab-')||f==='physics2-visual-guide.js'||f==='physics2-response-graph.js');
for(const f of scripts)vm.runInContext(fs.readFileSync(site+'/'+f,'utf8'),c,{filename:f});
const main=document.querySelector('main'),lab=c.PhysicsApparatusLab,click=el=>{assert(el,'missing UI control');el.dispatchEvent(new Event('click',{bubbles:true}))},change=(el,value)=>{assert(el);el.value=String(value);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}))};
let mounted=0,controls=0;
for(const [section,d] of Object.entries(c.GlassPhysicsRegistry)){
 const initial=lab.describe(section);assert(lab.grade(section,{},initial.target.answer).correct,section+' correct answer');
 main.innerHTML=lab.html({q:{subject:'physics'},section,chapter:Number(section.split('.')[0])});assert(lab.mount(main),section+' mount');mounted++;
 const root=main.querySelector('[data-gp-lab]');assert(root.querySelector('[data-gp-scene] svg'),section+' scene');
 assert(root.querySelector('[data-gp-observation]').textContent.length,section+' observation');
 click(root.querySelector('[data-gp-action="next-story"]'));assert.equal(lab.state().stage,1,section+' next stage');
 click(root.querySelector('[data-gp-action="previous-story"]'));assert.equal(lab.state().stage,0);
 click(root.querySelector('[data-gp-action="compare"]'));assert(!root.querySelector('[data-gp-comparison]').hidden,section+' pinned');
 for(const p of d.controls){const input=root.querySelector(`[data-gp-param="${p.key}"]`),value=p.options?p.options[p.options.length-1].value:p.max;change(input,value);assert.equal(String(lab.state()[p.key]),String(value),section+' control '+p.key);assert(root.querySelector('[data-gp-scene] svg'),section+' retained scene');controls++;}
 assert(root.querySelector('[data-gp-comparison] table'),section+' comparison table');
 click(root.querySelector('[data-gp-action="focus"]'));assert.equal(root.getAttribute('data-gp-expanded'),'true');click(root.querySelector('[data-gp-action="focus"]'));assert.equal(root.getAttribute('data-gp-expanded'),'false');
 click(root.querySelector('[data-gp-action="reset"]'));assert(root.querySelector('[data-gp-comparison]').hidden);assert.equal(lab.state().time,0);
 const before=root.querySelector('[data-gp-scene] svg');click(root.querySelector('[data-gp-action="step"]'));assert(lab.state().time>0);assert.strictEqual(before,root.querySelector('[data-gp-scene] svg'),section+' retains SVG element');
 change(root.querySelector('[data-gp-answer]'),lab.describe(section,lab.state()).target.answer);click(root.querySelector('[data-gp-action="check"]'));assert(root.querySelector('[data-gp-feedback]').classList.contains('gp-correct'),section+' grading');
 reduced=true;const previousTime=lab.state().time;click(root.querySelector('[data-gp-action="play"]'));assert(!lab.state().running);assert(lab.state().time>previousTime);reduced=false;
 click(root.querySelector('[data-gp-action="reset"]'));click(root.querySelector('[data-gp-action="play"]'));assert(lab.state().running);for(const time of [0,100,200]){const pending=[...queue.values()];queue.clear();for(const fn of pending)fn(time)}assert(lab.state().time>0,section+' advances animation');
 lab.unmount();assert.equal(queue.size,0,section+' clean animation teardown');
}
console.log('PASS: '+mounted+' apparatus mounts, '+controls+' controls, story steps, numeric grading, comparison/reset, retained SVG, reduced motion, animation lifecycle.');
