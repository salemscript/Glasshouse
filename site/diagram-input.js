/* Native SVG working canvas. Drawings are student work, never automatically graded. */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  let current = null;
  const clone = v => JSON.parse(JSON.stringify(v));
  const escape = v => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const tools = {label:'Atom / text',bond:'Single bond',double:'Double bond',arrow:'Electron pair arrow',fishhook:'Single electron arrow',pair:'Lone pair',charge:'Charge',erase:'Erase'};
  const counts = {label:1,bond:2,double:2,arrow:3,fishhook:3,pair:1,charge:1};
  function html() {
    return `<section class="diagram-input" aria-label="Drawing answer workspace"><div class="diagram-toolbar" role="group" aria-label="Drawing tools">${Object.entries(tools).map(([k,v]) => `<button type="button" data-diagram-tool="${k}" aria-pressed="${k==='label'}">${v}</button>`).join('')}</div><div class="diagram-options"><label>Atom, text, or charge <input class="diagram-label" value="C" maxlength="80" aria-label="Atom, text, or charge label"></label><button type="button" data-diagram-action="undo">Undo</button><button type="button" data-diagram-action="redo">Redo</button><button type="button" data-diagram-action="clear">Clear drawing</button><label>View size <select class="diagram-zoom"><option value="100">Fit width</option><option value="150">150%</option><option value="200">200%</option></select></label></div><p class="diagram-instructions">Choose a tool, then click or tap to place it. Bonds: start, end. Electron arrows: electron source, destination, then curve point. Arrow tails should begin at a bond or lone pair. This is your working drawing; it is not automatically checked.</p><p class="diagram-status" role="status" aria-live="polite"></p><div class="diagram-scroll"><svg class="diagram-canvas" xmlns="${NS}" viewBox="0 0 800 500" role="img" aria-label="Your answer drawing; coordinate controls available below"><title>Answer drawing</title></svg></div><details class="diagram-coordinates"><summary>Draw with coordinates (keyboard alternative)</summary><p>Coordinates begin at the top left. X: 0–800. Y: 0–<span class="diagram-height">500</span>. Enter the points required by your selected tool.</p><div class="diagram-point-fields">${['Start / position','End','Curve point'].map((label,i)=>`<fieldset><legend>${label}</legend><label>X <input type="number" class="diagram-x${i}" min="0" max="800" value="${200+i*150}" step="1"></label><label>Y <input type="number" class="diagram-y${i}" min="0" max="500" value="${i===2?120:250}" step="1"></label></fieldset>`).join('')}</div><button type="button" data-diagram-action="add">Add selected element</button></details><div class="diagram-element-list" aria-label="Drawing elements"></div></section>`;
  }
  function node(name, attrs, text) { const el = document.createElementNS(NS,name); Object.entries(attrs||{}).forEach(([k,v])=>el.setAttribute(k,String(v))); if(text!==undefined)el.textContent=text; return el; }
  function safeState(value) {
    const result={version:1,width:800,height:500,elements:[]};
    if(!value||!Array.isArray(value.elements))return result;
    result.height=Math.max(200,Math.min(8000,Number(value.height)||500));
    result.elements=value.elements.slice(0,500).filter(e=>e&&counts[e.type]&&Array.isArray(e.points)&&e.points.length===counts[e.type]&&e.points.every(p=>p&&Number.isFinite(p.x)&&Number.isFinite(p.y))).map((e,i)=>({id:'e'+i,type:e.type,label:String(e.label||'').slice(0,80),points:e.points.map(p=>({x:Math.max(0,Math.min(800,p.x)),y:Math.max(0,Math.min(result.height,p.y))}))}));
    return result;
  }
  function mount(key,savedState,onChange) {
    unmount();
    const root=document.querySelector('.diagram-input'); if(!root)return null;
    const abort=new AbortController();
    current={root,svg:root.querySelector('.diagram-canvas'),key:String(key),data:safeState(savedState),onChange,abort,tool:'label',pending:[],undo:[],redo:[],background:null};
    const c=current;
    root.addEventListener('click', e=>{
      const tool=e.target.closest('[data-diagram-tool]');
      if(tool){c.tool=tool.dataset.diagramTool;c.pending=[];root.querySelectorAll('[data-diagram-tool]').forEach(b=>b.setAttribute('aria-pressed',String(b===tool))); if(c.tool==='charge')root.querySelector('.diagram-label').value='+'; status();render();return;}
      const remove=e.target.closest('[data-diagram-remove]');
      if(remove){change(()=>{c.data.elements=c.data.elements.filter(x=>x.id!==remove.dataset.diagramRemove);});return;}
      const action=e.target.closest('[data-diagram-action]');if(!action)return;
      const a=action.dataset.diagramAction;
      if(a==='undo'||a==='redo'){const from=c[a],to=c[a==='undo'?'redo':'undo'];if(from.length){to.push(clone(c.data));c.data=from.pop();c.pending=[];notify();render();status('Drawing '+(a==='undo'?'undone.':'restored.'));}}
      if(a==='clear'&&c.data.elements.length&&window.confirm('Clear your drawing? You can undo this.'))change(()=>{c.data.elements=[];});
      if(a==='add'){
        if(c.tool==='erase'){status('Use the Remove buttons in the element list below.');return;}
        const points=[];for(let i=0;i<counts[c.tool];i++){const x=root.querySelector('.diagram-x'+i).value,y=root.querySelector('.diagram-y'+i).value;if(x===''||y===''||!Number.isFinite(Number(x))||!Number.isFinite(Number(y))){status('Enter a number for each required coordinate.');return;}points.push(clamp({x:Number(x),y:Number(y)}));}add(points);
      }
    },{signal:abort.signal});
    root.querySelector('.diagram-zoom').addEventListener('change',e=>{c.svg.style.width=e.target.value+'%';},{signal:abort.signal});
    c.svg.addEventListener('click',e=>{
      if(c.tool==='erase'){const target=e.target.closest('[data-element]');if(target)change(()=>{c.data.elements=c.data.elements.filter(x=>x.id!==target.dataset.element);});else status('Tap a drawn element to erase it.');return;}
      const matrix=c.svg.getScreenCTM();if(!matrix)return;
      const point=c.svg.createSVGPoint();point.x=e.clientX;point.y=e.clientY;
      const mapped=point.matrixTransform(matrix.inverse());c.pending.push(clamp(mapped));
      if(c.pending.length===counts[c.tool])add(c.pending);else{render();status();}
    },{signal:abort.signal});
    root.addEventListener('keydown',e=>{if(e.key==='Escape'){c.pending=[];render();status('Placement canceled.');}},{signal:abort.signal});
    render();status();return api;
  }
  function clamp(p){return {x:Math.max(0,Math.min(800,p.x)),y:Math.max(0,Math.min(current.data.height,p.y))};}
  function status(text){if(!current)return;const c=current;const prompts=c.tool==='erase'?['Select a drawn element to erase.']:counts[c.tool]===1?['Place your '+tools[c.tool].toLowerCase()+'.']:counts[c.tool]===2?['Choose the bond start.','Choose the bond end.']:['Choose the electron source (arrow tail).','Choose the destination (arrow head).','Choose a point to bend the arrow toward.'];c.root.querySelector('.diagram-status').textContent=text||prompts[c.pending.length]||'';}
  function notify(){if(typeof current.onChange==='function')current.onChange(clone(current.data));}
  function change(fn){const c=current;c.undo.push(clone(c.data));if(c.undo.length>80)c.undo.shift();c.redo=[];fn();c.pending=[];notify();render();status();}
  function add(points){const c=current;if(c.data.elements.length>=500){status('This drawing has reached 500 elements. Remove an element to continue.');return;}const label=c.root.querySelector('.diagram-label').value.trim();if((c.tool==='label'||c.tool==='charge')&&!label){status('Enter an atom, text, or charge label first.');return;}const type=c.tool;change(()=>{c.data.elements.push({id:'e'+Date.now().toString(36)+Math.random().toString(36).slice(2,7),type,label,points:clone(points)});});status(tools[type]+' added.');}
  function draw(el){
    const g=node('g',{'data-element':el.id,class:'diagram-element'}),p=el.points,a=p[0],b=p[1],base={stroke:'#152c39','stroke-width':3,'stroke-linecap':'round',fill:'none'};
    if(el.type==='label'||el.type==='charge')g.append(node('text',{x:a.x,y:a.y,'font-size':el.type==='charge'?23:24,'font-family':'sans-serif',fill:'#152c39','text-anchor':'middle','dominant-baseline':'central',stroke:'white','stroke-width':5,'paint-order':'stroke'},el.label));
    else if(el.type==='pair'){for(const dx of [-5,5])g.append(node('circle',{cx:a.x+dx,cy:a.y,r:2.8,fill:'#152c39'}));g.append(node('circle',{cx:a.x,cy:a.y,r:13,fill:'transparent'}));}
    else if(el.type==='bond'||el.type==='double'){
      const len=Math.hypot(b.x-a.x,b.y-a.y)||1,dx=-(b.y-a.y)/len*4,dy=(b.x-a.x)/len*4;
      for(const sign of el.type==='double'?[-1,1]:[0])g.append(node('line',{...base,x1:a.x+sign*dx,y1:a.y+sign*dy,x2:b.x+sign*dx,y2:b.y+sign*dy}));
      g.append(node('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,stroke:'transparent','stroke-width':18}));
    } else {
      const q=p[2],control={x:2*q.x-(a.x+b.x)/2,y:2*q.y-(a.y+b.y)/2},d=`M ${a.x} ${a.y} Q ${control.x} ${control.y} ${b.x} ${b.y}`;
      g.append(node('path',{...base,d,stroke:'#b51f67'}));g.append(node('path',{d,stroke:'transparent','stroke-width':18,fill:'none'}));
      let vx=b.x-control.x,vy=b.y-control.y,len=Math.hypot(vx,vy);if(len<.1){vx=b.x-a.x;vy=b.y-a.y;len=Math.hypot(vx,vy)||1;}vx/=len;vy/=len;
      const left={x:b.x-13*vx+6*vy,y:b.y-13*vy-6*vx},right={x:b.x-13*vx-6*vy,y:b.y-13*vy+6*vx};
      g.append(node('path',{d:el.type==='fishhook'?`M ${left.x} ${left.y} L ${b.x} ${b.y}`:`M ${left.x} ${left.y} L ${b.x} ${b.y} L ${right.x} ${right.y}`,stroke:'#b51f67','stroke-width':3,'stroke-linejoin':'round',fill:'none'}));
    }return g;
  }
  function render(){const c=current;if(!c)return;c.svg.replaceChildren(node('title',{},'Answer drawing'));c.svg.setAttribute('viewBox',`0 0 800 ${c.data.height}`);c.svg.style.aspectRatio='800 / '+c.data.height;
    if(c.background)c.svg.append(node('image',{href:c.background,x:0,y:0,width:800,height:c.data.height,'pointer-events':'none'}));
    c.data.elements.forEach(e=>c.svg.append(draw(e)));c.pending.forEach(p=>c.svg.append(node('circle',{cx:p.x,cy:p.y,r:6,fill:'#fa783b',stroke:'white','stroke-width':2,'pointer-events':'none'})));
    c.root.querySelector('.diagram-height').textContent=c.data.height;c.root.querySelectorAll('[class^="diagram-y"]').forEach(i=>i.max=c.data.height);
    c.root.querySelector('[data-diagram-action="undo"]').disabled=!c.undo.length;c.root.querySelector('[data-diagram-action="redo"]').disabled=!c.redo.length;
    c.root.querySelector('.diagram-element-list').innerHTML=c.data.elements.length?`<details><summary>${c.data.elements.length} drawn elements · review or remove</summary><ol>${c.data.elements.map(e=>`<li>${escape(tools[e.type])}${e.type==='label'||e.type==='charge'?': '+escape(e.label):''} — ${e.points.map((p,i)=>`${i===0?'at':i===1?'to':'curve through'} (${Math.round(p.x)}, ${Math.round(p.y)})`).join(' ')} <button type="button" data-diagram-remove="${escape(e.id)}" aria-label="Remove ${escape(tools[e.type])} at ${Math.round(e.points[0].x)}, ${Math.round(e.points[0].y)}">Remove</button></li>`).join('')}</ol></details>`:'<p>No drawn elements yet.</p>';
  }
  function setBackground(svgString){if(!current)return;const c=current;c.pending=[];if(!svgString){c.background=null;render();return;}const doc=new DOMParser().parseFromString(svgString,'image/svg+xml'),svg=doc.documentElement;if(svg.localName!=='svg'||doc.querySelector('parsererror')){status('Could not load this drawing background.');return;}const box=(svg.getAttribute('viewBox')||'').trim().split(/[\s,]+/).map(Number),w=box.length===4?box[2]:parseFloat(svg.getAttribute('width')),h=box.length===4?box[3]:parseFloat(svg.getAttribute('height'));if(w>0&&h>0)c.data.height=Math.max(200,Math.min(8000,Math.round(800*h/w)));c.background='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svgString);render();status();}
  function unmount(){if(current)current.abort.abort();current=null;}
  const api={html,mount,setBackground,state:()=>current?clone(current.data):null,reset:()=>{if(current)change(()=>{current.data.elements=[];});},unmount};
  window.DiagramInput=api;
})();
