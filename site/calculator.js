'use strict';
window.CalxCalculator=(()=>{
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function evaluate(raw,mode='deg',ans=0){
  let input=String(raw).replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+/g,m=>'^'+m.replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]/g,c=>'0123456789-+'['⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺'.indexOf(c)])).normalize('NFKC').toLowerCase().replace(/[−–]/g,'-').replace(/[×·]/g,'*').replace(/÷/g,'/').replace(/π/g,'pi').replace(/√/g,'sqrt');
  if(!input.trim())throw Error('Enter a calculation first.');if(input.length>160)throw Error('Keep the calculation under 160 characters.');
  const tokens=input.match(/(?:\d*\.\d+|\d+\.?\d*)(?:e[+-]?\d+)?|log10|[a-z]+|[()+*/^%!\-]/g)||[];
  if(tokens.join('')!==input.replace(/\s/g,''))throw Error('Use numbers, operators, and the scientific functions shown.');
  let balance=0;for(const t of tokens){if(t==='(')balance++;if(t===')')balance--;if(balance<0)throw Error('Check your parentheses.')}while(balance-->0)tokens.push(')');
  const radians=x=>mode==='deg'?x*Math.PI/180:x,angle=x=>mode==='deg'?x*180/Math.PI:x;
  const positive=x=>{if(x<=0)throw Error('Logarithms need a positive value.');return x};
  const fns={sin:x=>Math.sin(radians(x)),cos:x=>Math.cos(radians(x)),tan:x=>{const r=radians(x);if(Math.abs(Math.cos(r))<1e-14)throw Error('Tangent is undefined at this angle.');return Math.tan(r)},asin:x=>angle(Math.asin(x)),acos:x=>angle(Math.acos(x)),atan:x=>angle(Math.atan(x)),sqrt:x=>{if(x<0)throw Error('A real square root needs a nonnegative value.');return Math.sqrt(x)},ln:x=>Math.log(positive(x)),log:x=>Math.log10(positive(x)),log10:x=>Math.log10(positive(x)),abs:Math.abs,exp:Math.exp};
  const constants={pi:Math.PI,e:Math.E,ans:Number.isFinite(ans)?ans:0};let pos=0,depth=0;
  function sum(){let v=product();while(['+','-'].includes(tokens[pos])){const op=tokens[pos++],w=product();v=op==='+'?v+w:v-w}return v}
  function product(){let v=unary();while(['*','/'].includes(tokens[pos])||tokens[pos]==='('||Object.hasOwn(constants,tokens[pos])||Object.hasOwn(fns,tokens[pos])||(/^(?:\d|\.)/.test(tokens[pos]||'')&&[')', '!', '%', 'pi','e','ans'].includes(tokens[pos-1]))){const op=['*','/'].includes(tokens[pos])?tokens[pos++]:'*',w=unary();if(op==='/'&&w===0)throw Error('You cannot divide by zero.');v=op==='*'?v*w:v/w}return v}
  function unary(){if(tokens[pos]==='+'){pos++;return unary()}if(tokens[pos]==='-'){pos++;return -unary()}return power()}
  function power(){let v=atom();if(tokens[pos]==='^'){pos++;v=Math.pow(v,unary())}return v}
  function atom(postfix=true){
   if(++depth>80)throw Error('Simplify this calculation into smaller steps.');const t=tokens[pos++];let v;
   if(t==='('){v=sum();if(tokens[pos++]!==')')throw Error('Check your parentheses.')}
   else if(Object.hasOwn(constants,t))v=constants[t];else if(Object.hasOwn(fns,t))v=fns[t](atom(false));
   else if(/^(?:\d|\.)/.test(t||''))v=Number(t);else throw Error('Check the expression near the cursor.');
   while(postfix&&['%','!'].includes(tokens[pos])){const op=tokens[pos++];if(op==='%')v/=100;else{if(!Number.isInteger(v)||v<0||v>170)throw Error('Factorials require an integer from 0 to 170.');let f=1;for(let i=2;i<=v;i++)f*=i;v=f}}
   depth--;return v;
  }
  const result=sum();if(pos!==tokens.length)throw Error('Add an operator between these values.');if(!Number.isFinite(result))throw Error('This calculation has no finite real result.');return Object.is(result,-0)?0:result;
 }
 const format=n=>Number(n.toPrecision(15)).toString();
 let opened=false,expr='',mode='deg',inverse=false,value=null,lastAns=0,recent=[],message='',justEvaluated=false,target=null,opener=null;
 try{const saved=JSON.parse(localStorage.getItem('calx-calculator-v1')||'{}');expr=typeof saved.expr==='string'?saved.expr.slice(0,160):'';mode=saved.mode==='rad'?'rad':'deg';lastAns=Number.isFinite(saved.lastAns)?saved.lastAns:0;value=typeof saved.value==='number'&&Number.isFinite(saved.value)?saved.value:null;recent=Array.isArray(saved.recent)?saved.recent.filter(x=>x&&typeof x.expr==='string'&&x.expr.length<=160&&Number.isFinite(x.value)&&['deg','rad'].includes(x.mode)).slice(0,6):[]}catch{}
 const get=id=>document.querySelector('#'+id),wide=()=>Boolean(window.matchMedia?.('(min-width:1180px)').matches);
 const keys=[['sin','sin('],['cos','cos('],['tan','tan('],['ln','ln('],['log','log('],['√','sqrt('],['x²','^2'],['xʸ','^'],['(','('],[')',')'],['AC','clear'],['⌫','delete'],['Ans','ans'],['π','pi'],['e','e'],['7','7'],['8','8'],['9','9'],['÷','÷'],['x!','!'],['4','4'],['5','5'],['6','6'],['×','×'],['%','%'],['1','1'],['2','2'],['3','3'],['−','−'],['×10ⁿ','×10^('],['±','sign'],['0','0'],['.','.'],['+','+'],['=','equals']];
 const inverseKeys={'sin(':['sin⁻¹','asin('],'cos(':['cos⁻¹','acos('],'tan(':['tan⁻¹','atan('],'ln(':['eˣ','exp('],'log(':['10ˣ','10^(']};
 function save(){try{localStorage.setItem('calx-calculator-v1',JSON.stringify({expr,mode,lastAns,value,recent}))}catch{}}
 function keyHTML(){return keys.map(([label,token])=>{const pair=inverse&&inverseKeys[token]?inverseKeys[token]:[label,token];const help=token==='%'?'Divide by 100':token==='sign'?'Change the sign of the expression':token==='delete'?'Delete the selected text or previous character':token==='equals'?'Calculate the result':pair[1];return '<button type="button" class="calc-key '+(token==='equals'?'calc-key-equals':/^\d$|\./.test(token)?'calc-key-number':'calc-key-function')+'" data-calc-token="'+esc(pair[1])+'" aria-label="'+esc(help)+'" title="'+esc(help)+'">'+esc(pair[0])+'</button>'}).join('')}
 function targetLabel(){if(!target||target.isConnected===false)return '';return String(target.labels?.[0]?.textContent||target.getAttribute?.('aria-label')||'answer field').trim().slice(0,90)}
 function paintTarget(){const label=targetLabel(),button=get('calculator-insert');if(button){button.disabled=value===null||!label;button.textContent=label?'Use result in answer':'Choose an answer field';button.title=label?'Insert into '+label:'Click the answer box you want to fill.'}const note=get('calculator-target');if(note)note.textContent=label?'Selected: '+label:'Click an answer box to send the result there.'}
 function paint(){
  const panel=get('calculator-panel');if(!panel)return;panel.hidden=!opened;
  document.body?.classList?.toggle('calculator-open',opened);document.body?.classList?.toggle('calculator-docked',false);const dock=get('calculator-mini');if(dock)dock.hidden=opened;
  document.querySelectorAll('[data-calculator-open]').forEach(b=>b.setAttribute('aria-expanded',String(opened)));
  get('calculator-expression').value=expr;const result=get('calculator-result');result.textContent=value===null?'—':format(value);result.title=value===null?'':'Full precision: '+String(value);result.classList.toggle('calc-result-long',value!==null&&format(value).length>14);
  get('calculator-message').textContent=message;get('calculator-deg').setAttribute('aria-pressed',String(mode==='deg'));get('calculator-rad').setAttribute('aria-pressed',String(mode==='rad'));get('calculator-inverse').setAttribute('aria-pressed',String(inverse));
  get('calculator-keys').innerHTML=keyHTML();get('calculator-copy').disabled=value===null;
  get('calculator-history-count').textContent='Recent calculations'+(recent.length?' ('+recent.length+')':'');
  get('calculator-history-list').innerHTML=recent.length?recent.map((x,i)=>'<button type="button" class="calc-history-item" data-calc-history="'+i+'"><span>'+esc(x.expr)+' <small>'+x.mode.toUpperCase()+'</small></span><b>'+esc(format(x.value))+'</b></button>').join(''):'<p class="calc-empty">Your calculations will appear here.</p>';paintTarget();
 }
 function open(trigger){opened=true;opener=trigger||document.activeElement;paint();get('calculator-expression')?.focus?.()}
 function close(restore=true){opened=false;paint();if(restore)get('calculator-mini')?.focus?.()}
 function insert(token){
  const input=get('calculator-expression');let start=input.selectionStart??expr.length,end=input.selectionEnd??start;
  if(justEvaluated&&token!=='delete'&&token!=='clear'){expr=token==='sign'||/^(?:[+−\-×÷*/^%!])/.test(token)?String(value):'';start=end=expr.length}justEvaluated=false;
  if(token==='clear'){expr='';value=null;message='';paint();save();input.focus?.();return}
  if(token==='delete'){if(start===end)start=Math.max(0,start-1);expr=expr.slice(0,start)+expr.slice(end);end=start}
  else if(token==='sign'){expr=expr?'−('+expr+')':'−';end=expr.length}
  else {expr=expr.slice(0,start)+token+expr.slice(end);end=start+token.length}
  expr=expr.slice(0,160);value=null;message='';paint();input.focus?.();input.setSelectionRange?.(Math.min(end,expr.length),Math.min(end,expr.length));save();
 }
 function calculate(){
  try{value=evaluate(expr,mode,lastAns);lastAns=value;justEvaluated=true;message='';recent=[{expr,value,mode},...recent.filter(x=>x.expr!==expr||x.mode!==mode)].slice(0,6)}catch(error){value=null;justEvaluated=false;message=error.message}paint();save();
 }
 function useResult(){
  if(value===null||!targetLabel()){message='Choose an answer box first.';paint();return false}
  const field=target;field.value=String(value);field.dispatchEvent(new Event('input',{bubbles:true}));message='Result inserted at full precision.';
  if(!wide())close(false);else paint();field.focus?.();return true;
 }
 async function copy(){if(value===null)return;try{if(!navigator.clipboard?.writeText)throw Error();await navigator.clipboard.writeText(String(value));message='Result copied at full precision.'}catch{message='Select the result to copy it.'}paint()}
 const root=get('calculator-root');if(root){root.innerHTML='<button type="button" class="calculator-mini" id="calculator-mini" data-calculator-open aria-controls="calculator-panel" aria-expanded="false"><svg viewBox="0 0 20 24" fill="none" aria-hidden="true"><rect x="2" y="1" width="16" height="22" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M5 5h10v4H5zM5 13h2m3 0h2m3 0h1M5 17h2m3 0h2m3 0h1" stroke="currentColor" stroke-width="1.5"/></svg><span>Calculator</span><span aria-hidden="true">↗</span></button><section class="calculator-panel" id="calculator-panel" aria-labelledby="calculator-title" hidden><div class="calc-heading"><button type="button" class="calc-close calc-minimize" id="calculator-close" aria-label="Shrink calculator to bottom-left dock" title="Shrink calculator">↙</button><div><span class="calc-eyebrow">YOUR WORKSPACE TOOL</span><h2 id="calculator-title">Calculator<span>.</span></h2></div></div><div class="calc-toolbar"><div class="calc-angle" role="group" aria-label="Angle units"><button type="button" id="calculator-deg" aria-pressed="true">DEG</button><button type="button" id="calculator-rad" aria-pressed="false">RAD</button></div><button type="button" class="calc-inverse" id="calculator-inverse" aria-pressed="false" title="Show inverse trigonometric and exponential functions">2nd</button><span class="calc-mode-note">Real-number scientific</span></div><div class="calc-display"><label for="calculator-expression">Calculation</label><input id="calculator-expression" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" maxlength="160" placeholder="Try 2 × π × 6370" aria-describedby="calculator-message"><div class="calc-result-row"><span>=</span><output id="calculator-result" aria-live="polite">—</output></div></div><p class="calc-message" id="calculator-message" role="status"></p><div class="calc-keypad" id="calculator-keys"></div><div class="calc-result-actions"><button type="button" class="btn" id="calculator-insert" disabled>Choose an answer field</button><button type="button" class="btn light" id="calculator-copy" disabled>Copy</button></div><p class="calc-target" id="calculator-target">Click an answer box to send the result there.</p><details class="calc-history"><summary id="calculator-history-count">Recent calculations</summary><div id="calculator-history-list"></div></details><p class="calc-footnote">Enter uses =. Functions follow DEG / RAD. Transfers keep full precision.</p></section>';paint()}
 document.addEventListener('focusin',e=>{if(/^(?:answer|bank-answer|question-answer-(?:\d+|part-[a-z])|hint-blank-\d+)$/.test(e.target.id)){target=e.target;paintTarget()}else if(e.target.closest?.('.calculator-panel'))paintTarget()});
 document.addEventListener('input',e=>{if(e.target.id==='calculator-expression'){expr=e.target.value;value=null;message='';justEvaluated=false;get('calculator-result').textContent='—';get('calculator-message').textContent='';get('calculator-copy').disabled=true;paintTarget();save()}});
 document.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b)return;
  if(b.dataset.calculatorOpen!==undefined){opened?close():open(b)}else if(b.id==='calculator-close')close();else if(b.dataset.calcToken!==undefined){b.dataset.calcToken==='equals'?calculate():insert(b.dataset.calcToken)}
  else if(['calculator-deg','calculator-rad'].includes(b.id)){mode=b.id==='calculator-rad'?'rad':'deg';value=null;justEvaluated=false;message='';paint();save()}
  else if(b.id==='calculator-inverse'){inverse=!inverse;paint()}else if(b.id==='calculator-insert')useResult();else if(b.id==='calculator-copy')copy();
  else if(b.dataset.calcHistory!==undefined){const item=recent[Number(b.dataset.calcHistory)];if(item){expr=item.expr;value=item.value;lastAns=value;mode=item.mode;justEvaluated=true;message='Previous result restored.';paint();save()}}
 });
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&opened&&e.target.closest?.('.calculator-panel')){e.preventDefault();close()}else if(e.key==='Enter'&&e.target.id==='calculator-expression'){e.preventDefault();calculate()}});
 window.addEventListener?.('hashchange',()=>{paintTarget();if(opened)paint()});
 return {evaluate,open,close,calculate,useResult,state:()=>({opened,expr,mode,value,lastAns,recent:recent.length,hasTarget:Boolean(targetLabel())})};
})();
