/* Presentation only. Never evaluates an expression or changes answer data. */
(function(root){
 'use strict';
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const row=a=>'<mrow>'+a.join('')+'</mrow>',mo=s=>'<mo>'+esc(s)+'</mo>';
 const supMap={'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁻':'−','⁺':'+','ʳ':'r','ᴿ':'R'};
 const subMap={'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9','ₓ':'x','ᵧ':'y','ᵣ':'r','ₑ':'e','ᵢ':'i'};
 const unit=/^(?:N·m[²³]\/C|N\*m\^[23]\/C|N\/C|C\/m[²³]|[μnp]C\/m[²³]?|kg\/m³|kg\/s|m\/s[²³]?|m\/mm|mm|cm|km|μC|nC|pC|kg)(?![A-Za-z])/;
 const words=new Set(['cos','sin','tan','min','max','ln','log','lim','enc','enclosed','net','total','initial','final','inner','outer','inside','outside','sheet','wire','water','base','cap','point','center','shell','face','one','cube','square','crit','break']);
 function tokens(source){
  const out=[];let at=0;
  while(at<source.length){
   const tail=source.slice(at),space=/^\s+/.exec(tail);if(space){at+=space[0].length;continue;}
   const u=unit.exec(tail);if(u){if(u[0].includes('/')&&(tail[u[0].length]==='^'||supMap[tail[u[0].length]]))throw Error('Unsupported unit exponent');out.push({kind:'unit',value:u[0]});at+=u[0].length;continue;}
   const n=/^(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+−-]?\d+)?/.exec(tail);if(n){out.push({kind:'number',value:n[0]});at+=n[0].length;continue;}
   const fn=/^(atan2|asinh|acosh|atanh|sinh|cosh|tanh|acos|asin|atan|cos|sin|tan|min|max|ln|log|lim)(?![A-Za-z])/.exec(tail);if(fn){out.push({kind:'function',value:fn[0]});at+=fn[0].length;continue;}
   const c=tail[0];
   if(c==='_'){
    const sub=/^_([A-Za-z]+|[0-9]+|[α-ωΑ-Ω])/.exec(tail);if(!sub)throw Error('Incomplete subscript');
    out.push({kind:'sub',value:sub[1]});at+=sub[0].length;continue;
   }
   if(supMap[c]||subMap[c]){let v='',map=supMap[c]?supMap:subMap;while(map[source[at]])v+=map[source[at++]];out.push({kind:map===supMap?'sup':'sub',value:v});continue;}
   if(/[A-Za-zα-ωΑ-Ωℓṁĵ]/.test(c)){
    // Unknown prose is deliberately not interpreted as a run of variables.
    const word=/^[a-z]{3,}/.exec(tail);if(word&&!words.has(word[0]))throw Error('Prose is not algebra');
    if(word&&words.has(word[0])){out.push({kind:'label',value:word[0]});at+=word[0].length;continue;}
    out.push({kind:'symbol',value:c});at++;continue;
   }
   if('=≈≠≤≥<>+−-×·*/^()[]{}|√°;,⇒→∞∫Σ∮⃗̂′'.includes(c)){out.push({kind:'operator',value:c});at++;continue;}
   throw Error('Unsupported notation');
  }
  return out;
 }
 function parse(source){
  // An integral is an operator on its integrand, not a factor that belongs in
  // a fraction numerator. This compact algebra parser has no integral grammar.
  // Preserve the original notation until scope/bounds can be represented safely.
  if(/[∫∮∑Σ]/.test(String(source)))throw Error('Aggregate operator scope requires the original notation');
  const normalized=String(source).replace(/\*\*/g,'^').replace(/\bpi\b/g,'π').replace(/\bsqrt\b/g,'√');
  const ts=tokens(normalized);let i=0,depth=0;
  const peek=v=>ts[i]?.value===v,next=()=>ts[i++],node=(tag,s)=>'<'+tag+'>'+esc(s)+'</'+tag+'>';
  const text=s=>'<mtext>'+esc(s)+'</mtext>';
  const starts=()=>{const t=ts[i];return t&&(['number','symbol','unit','label','function'].includes(t.kind)||['(','[','{','√','|','∞','∫','Σ','∮'].includes(t.value));};
  function atom(){
   if(++depth>50)throw Error('Expression too deep');
   const t=next();if(!t)throw Error('Missing expression');let result;
   if(['(','[','{'].includes(t.value)){const close={'(':')','[':']','{':'}'}[t.value],inside=sequence(close);if(!peek(close))throw Error('Unbalanced group');next();result=row([mo(t.value),inside,mo(close)]);}
   else if(t.value==='|'){const inside=sequence('|');if(!peek('|'))throw Error('Unbalanced absolute value');next();result=row([mo('|'),inside,mo('|')]);}
   else if(t.value==='√'){result='<msqrt>'+atom()+'</msqrt>';}
   else if(t.kind==='number'){
    const sci=/^(.+)[eE]([+−-]?\d+)$/.exec(t.value);
    result=sci?row([node('mn',sci[1]),mo('×'),'<msup>'+node('mn','10')+node('mn',sci[2].replace('-','−'))+'</msup>']):node('mn',t.value);
   }
   else if(t.kind==='unit'||t.kind==='label')result=text(t.value);
   else if(t.kind==='function')result='<mrow><mi mathvariant="normal">'+esc(t.value)+'</mi><mo>⁡</mo></mrow>';
   else if(t.kind==='symbol')result=node('mi',t.value);
   else if(['∞','∫','Σ','∮'].includes(t.value))result=mo(t.value);
   else throw Error('Unsupported atom');
   let sub=null,sup=null;
   while(ts[i]&&(ts[i].kind==='sub'||ts[i].kind==='sup'||['^','°','⃗','̂','′'].includes(ts[i].value))){
    const a=next();if(a.kind==='sub'){if(sub)throw Error('Repeated subscript');sub=text(a.value);}
    else if(a.kind==='sup'){if(sup)throw Error('Repeated superscript');sup=/^[+−]?\d+$/.test(a.value)?node('mn',a.value):node('mi',a.value);}
    else if(a.value==='^'){if(sup)throw Error('Repeated superscript');sup=atom();}
    else if(a.value==='°')result=row([result,mo('°')]);
    else if(a.value==='′')result=row([result,mo('′')]);
    else result='<mover accent="true">'+result+mo(a.value==='⃗'?'→':'^')+'</mover>';
   }
   if(sub&&sup)result='<msubsup>'+result+sub+sup+'</msubsup>';
   else if(sub)result='<msub>'+result+sub+'</msub>';
   else if(sup)result='<msup>'+result+sup+'</msup>';
   depth--;return result;
  }
  function product(stop,denominator=false){const a=[];while(starts()&&!peek(stop)&&!(denominator&&ts[i].kind==='unit'))a.push(atom());if(!a.length)throw Error('Missing fraction operand');return a.length===1?a[0]:row(a);}
  function ratio(stop){let a=product(stop);while(peek('/')){next();const grouped=['(','[','{','|','√'].includes(ts[i]?.value),b=grouped?atom():product(stop,true);a='<mfrac>'+a+b+'</mfrac>';}return a;}
  function sequence(stop){const a=[];while(i<ts.length&&!peek(stop)){
   if(starts())a.push(ratio(stop));else{const t=next();if(t.kind!=='operator'||['/',')',']','}','^'].includes(t.value))throw Error('Invalid equation');a.push(mo(t.value==='-'?'−':t.value==='*'?'×':t.value));}
  }if(!a.length)throw Error('Empty expression');return row(a);}
  const result=sequence(null);if(i!==ts.length)throw Error('Unconsumed notation');return result;
 }
 function render(value){
  const source=String(value??'');if(!source.trim()||source.length>2000)return esc(source);
  try{const markup=parse(source);return '<span class="solution-math-scroll" role="region" tabindex="0" aria-label="Equation: '+esc(source)+'"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block" aria-label="'+esc(source)+'"><semantics>'+markup+'<annotation encoding="text/plain">'+esc(source)+'</annotation></semantics></math></span>';}
  catch(_){return esc(source);}
 }
 function inline(value){return String(value??'').split(/(\.(?=\s|$))/).map(part=>{
  if(part==='.')return '.';
  const prefix=/^(\s*(?:Use\s+|Substitute:\s*|[^=:.]{3,}:\s*))/.exec(part);
  return prefix?esc(prefix[0])+render(part.slice(prefix[0].length)):render(part);
 }).join('');}
 root.SolutionMath={render,html:render,inline,parse};
})(typeof window!=='undefined'?window:globalThis);
