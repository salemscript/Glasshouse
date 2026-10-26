/* Presentation only. Never evaluates an expression or changes answer data. */
(function(root){
 'use strict';
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const row=a=>'<mrow>'+a.join('')+'</mrow>',mo=s=>'<mo>'+esc(s)+'</mo>';
 const supMap={'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁻':'−','⁺':'+','ʳ':'r','ᴿ':'R','ⁿ':'n','ˣ':'x','ᵏ':'k','⁽':'(','⁾':')'};
 const subMap={'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9','ₓ':'x','ᵧ':'y','ᵣ':'r','ₑ':'e','ᵢ':'i','ₙ':'n','ₖ':'k','ₘ':'m','ₜ':'t','ᵦ':'b','₊':'+','₋':'−','ₐ':'a'};
 const unit=/^(?:(?:mg|lb|ft[³²]?|mi|rad|shakes|seconds)\/(?:in[²³]?|mL|L|h|s[²³]?|hour|second|year)|N·m[²³]\/C|N\*m\^[23]\/C|N\/C|C\/m[²³]|[μnp]C\/m[²³]?|kg\/m³|kg\/s|m\/s[²³]?|m\/mm|mm|cm|km|μC|nC|pC|kg)(?![A-Za-z])/;
 const words=new Set(['cos','sin','tan','min','max','ln','log','lim','enc','enclosed','net','total','initial','final','inner','outer','inside','outside','sheet','wire','water','base','cap','point','center','shell','face','one','cube','square','crit','break']);
 function tokens(source){
  const out=[];let at=0;
  while(at<source.length){
   const tail=source.slice(at),space=/^\s+/.exec(tail);if(space){at+=space[0].length;continue;}
   const u=unit.exec(tail);if(u){if(u[0].includes('/')&&tail[u[0].length]==='^'){const power=/^\^[+-]?\d+/.exec(tail.slice(u[0].length));if(!power)throw Error('Unsupported unit exponent');u[0]+=power[0];}out.push({kind:'unit',value:u[0]});at+=u[0].length;continue;}
   const n=/^(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+−-]?\d+)?/.exec(tail);if(n){out.push({kind:'number',value:n[0]});at+=n[0].length;continue;}
   const fn=/^(erf|comp|proj|cuberoot|arcosh|arsinh|factorial|binom|arcsinh|arccosh|arctanh|arcsec|arccsc|arccot|arcsin|arccos|arctan|floor|ceil|atan2|asinh|acosh|atanh|sinh|cosh|tanh|coth|sech|csch|acos|asin|atan|cos|sin|tan|sec|csc|cot|exp|abs|min|max|ln|log|lim)(?![A-Za-z])/.exec(tail);if(fn){out.push({kind:'function',value:fn[0]});at+=fn[0].length;continue;}
   const c=tail[0];if(c==='Σ'){out.push({kind:'operator',value:'∑'});at++;continue;}
   if(c==='_'){
    const sub=/^_([a-z]+(?=[A-Z])|[A-Za-z]+(?:_[A-Za-z]+)*|[0-9]+|[α-ωΑ-Ω])/ .exec(tail);if(!sub){if(tail[1]==='('||tail[1]==='{'){out.push({kind:'operator',value:'_'});at++;continue;}throw Error('Incomplete subscript');}
    out.push({kind:'sub',value:sub[1]});at+=sub[0].length;continue;
   }
   if(supMap[c]||subMap[c]){let v='',map=supMap[c]?supMap:subMap;while(map[source[at]])v+=map[source[at++]];out.push({kind:map===supMap?'sup':'sub',value:v});continue;}
   if(/^d[xyztrθφ]\b/.test(tail)){out.push({kind:'differential',value:tail.slice(0,2)});at+=2;continue;}
   if(/[A-Za-zα-ωΑ-Ωℓṁĵîķℤℝℕ∂ȳ∇]/.test(c)){
    // Unknown prose is deliberately not interpreted as a run of variables.
    const word=/^[a-z]{3,}/.exec(tail);if(word&&!words.has(word[0])&&!['ckt','kqz','xyz','akt','mgt','kqr','mgL'].includes(word[0]))throw Error('Prose is not algebra');
    if(word&&words.has(word[0])){out.push({kind:'label',value:word[0]});at+=word[0].length;continue;}
    out.push({kind:'symbol',value:c});at++;continue;
   }
   if('=≈≠≤≥<>+−-×·*/^()[]{}|√°;,⇒→∞∫∬∭Σ∑∮⃗̂′″‴̄∘…⋯∪∈±≡!≪≫:⟨⟩∛'.includes(c)){out.push({kind:'operator',value:c});at++;continue;}
   throw Error('Unsupported notation');
  }
  return out;
 }
 function parse(source){
  // Aggregate operators remain separate from the fractions they act on.

  const normalized=String(source).replace(/!=/g,'≠').replace(/([A-Za-z])-vector/g,'$1⃗').replace(/½/g,'(1/2)').replace(/\.\./g,'…').replace(/\*\*/g,'^').replace(/\bpi\b/g,'π').replace(/sqrt(?=\s*[\d(])/g,'√').replace(/\bAbs\b/g,'abs').replace(/\b(theta|alpha|beta|gamma|lambda|phi|omega|rho|epsilon|delta|sigma|tau)(?=\b|_)/g,v=>({theta:'θ',alpha:'α',beta:'β',gamma:'γ',lambda:'λ',phi:'φ',omega:'ω',rho:'ρ',epsilon:'ε',delta:'δ',sigma:'σ',tau:'τ'}[v])).replace(/(?<![A-Za-z])(sin|cos|tan|sec|csc|cot|sinh|cosh|tanh|ln|log)([xyzcvθφ])\b/g,'$1 $2');
  const ts=tokens(normalized);let i=0,depth=0;
  const peek=v=>ts[i]?.value===v,next=()=>ts[i++],node=(tag,s)=>'<'+tag+'>'+esc(s)+'</'+tag+'>';
  const ungroup=s=>s.startsWith('<mrow><mo>(</mo>')&&s.endsWith('<mo>)</mo></mrow>')?s.slice('<mrow><mo>(</mo>'.length,-'<mo>)</mo></mrow>'.length):s;
  const text=s=>'<mtext>'+esc(s)+'</mtext>';
  const starts=()=>{const t=ts[i];return t&&(['number','symbol','unit','label','function','differential'].includes(t.kind)||['(','[','{','⟨','√','∛','|','∞','∫','∬','∭','Σ','∑','∮'].includes(t.value));};
  function atom(scripts=true){
   if(++depth>50)throw Error('Expression too deep');
   const t=next();if(!t)throw Error('Missing expression');let result;
   if(['(','[','{','⟨'].includes(t.value)){const close={'(':')','[':']','{':'}','⟨':'⟩'}[t.value],inside=sequence(close);const actual=ts[i]?.value;if(!peek(close)&&!(['(', '['].includes(t.value)&&[')',']'].includes(actual)&&inside.includes('<mo>,</mo>')))throw Error('Unbalanced group');next();result=row([mo(t.value),inside,mo(actual)]);}
   else if(t.value==='|'){const inside=sequence('|');if(!peek('|'))throw Error('Unbalanced absolute value');next();result=row([mo('|'),inside,mo('|')]);}
   else if(t.value==='√'){result='<msqrt>'+ungroup(atom(false))+'</msqrt>';}
   else if(t.value==='∛'){result='<mroot>'+ungroup(atom(false))+'<mn>3</mn></mroot>';}
   else if(t.value==='-'||t.value==='−'||t.value==='+'){result=row([mo(t.value==='-'?'−':t.value),atom()]);}
   else if(t.kind==='number'){
    const sci=/^(.+)[eE]([+−-]?\d+)$/.exec(t.value);
    result=sci?row([node('mn',sci[1]),mo('×'),'<msup>'+node('mn','10')+node('mn',sci[2].replace('-','−'))+'</msup>']):node('mn',t.value);
   }
   else if(t.kind==='unit'){
    const part=v=>{const m=/^(.*?)([²³]|\^[+-]?\d+)$/.exec(v);return m?'<msup>'+text(m[1])+node('mn',supMap[m[2]]||m[2].slice(1))+'</msup>':text(v);};
    const pieces=t.value.split('/');result=pieces.length===2?'<mfrac>'+part(pieces[0])+part(pieces[1])+'</mfrac>':part(t.value);
   }
   else if(t.kind==='label')result=text(t.value);
   else if(t.kind==='differential')result=row([node('mi','d'),node('mi',t.value.slice(1))]);
   else if(t.kind==='function'){result='<mrow><mi mathvariant="normal">'+esc(t.value)+'</mi><mo>⁡</mo></mrow>';if(peek('('))result=row([result,atom(false)]);}
   else if(t.kind==='symbol')result=node('mi',t.value);
   else if(['∞','∫','∬','∭','Σ','∑','∮'].includes(t.value))result=mo(t.value==='Σ'?'∑':t.value);
   else throw Error('Unsupported atom');
   let sub=null,sup=null;
   while(scripts&&ts[i]&&(ts[i].kind==='sub'||ts[i].kind==='sup'||['^','_','°','⃗','̂','′','″','‴','̄','!'].includes(ts[i].value))){
    const a=next();if(a.kind==='sub'){if(sub)throw Error('Repeated subscript');sub=text(a.value.replace(/_/g,','));}
    else if(a.kind==='sup'){if(sup)throw Error('Repeated superscript');sup=/^[+−]?\d+$/.test(a.value)?node('mn',a.value):node('mi',a.value);}
    else if(a.value==='_'){if(sub)throw Error('Repeated subscript');sub=atom(false);}
    else if(a.value==='^'){if(sup)throw Error('Repeated superscript');sup=atom();}
    else if(a.value==='!')result=row([result,mo('!')]);
    else if(a.value==='°')result=row([result,mo('°')]);
    else if(a.value==='′'||a.value==='″'||a.value==='‴')result=row([result,mo(a.value)]);
    else result='<mover accent="true">'+result+mo(a.value==='⃗'?'→':a.value==='̄'?'¯':'^')+'</mover>';
   }
   if(['Σ','∑'].includes(t.value)&&sub)sub=ungroup(sub);
   if(sub&&sup)result=['Σ','∑'].includes(t.value)?'<munderover>'+result+sub+sup+'</munderover>':'<msubsup>'+result+sub+sup+'</msubsup>';
   else if(sub)result=['Σ','∑'].includes(t.value)?'<munder>'+result+sub+'</munder>':'<msub>'+result+sub+'</msub>';
   else if(sup)result=['Σ','∑'].includes(t.value)?'<mover>'+result+sup+'</mover>':'<msup>'+result+sup+'</msup>';
   depth--;return result;
  }
  function product(stop,denominator=false){const a=[];while(starts()&&!peek(stop)&&!(denominator&&a.length&&['unit','differential'].includes(ts[i].kind)))a.push(atom());if(!a.length)throw Error('Missing fraction operand');return a.length===1?a[0]:row(a);}
  function ratio(stop){let a=product(stop);while(peek('/')){next();const grouped=['(','[','{','|','√','−','-','+'].includes(ts[i]?.value),b=grouped?atom():product(stop,true);a='<mfrac>'+ungroup(a)+ungroup(b)+'</mfrac>';}return a;}
  function sequence(stop){const a=[];while(i<ts.length&&!peek(stop)&&!(stop===')'&&peek(']'))&&!(stop===']'&&peek(')'))){
   if(['∫','∬','∭','∮'].includes(ts[i]?.value)||(['Σ','∑'].includes(ts[i]?.value)&&['sub','sup'].includes(ts[i+1]?.kind))||(['Σ','∑'].includes(ts[i]?.value)&&['_','^','(' ,'['].includes(ts[i+1]?.value)))a.push(atom());
   else if(starts())a.push(ratio(stop));else{const t=next();if(t.kind!=='operator'||['/',')',']','}','^'].includes(t.value))throw Error('Invalid equation');a.push(mo(t.value==='-'?'−':t.value==='*'?'×':t.value));}
  }if(!a.length)throw Error('Empty expression');return row(a);}
  const result=sequence(null);if(i!==ts.length)throw Error('Unconsumed notation');return result;
 }
 // Plain text is never injected as markup. Source strings remain unchanged for grading.
 function mathHTML(source,markup,inline=false){return '<span class="solution-math-scroll'+(inline?' solution-math-inline':'')+'"'+(inline?'':' role="region" tabindex="0"')+' aria-label="'+(inline?'':'Equation: ')+esc(source)+'"><math xmlns="http://www.w3.org/1998/Math/MathML" display="'+(inline?'inline':'block')+'" aria-label="'+esc(source)+'"><semantics>'+markup+'<annotation encoding="text/plain">'+esc(source)+'</annotation></semantics></math></span>';}
 const mathWords=new Set('pi sqrt theta alpha beta gamma lambda phi omega rho epsilon delta sigma tau erf comp proj cuberoot arcosh arsinh factorial binom arcsinh arccosh arctanh arcsec arccsc arccot coth sech csch arcsin arccos arctan floor ceil sin cos tan sec csc cot asin acos atan atan2 sinh cosh tanh asinh acosh atanh ln log exp abs Abs min max lim kg mm cm km'.split(' '));
 const proseWords=new Set('is in as at of to or by on an if be it no so we do up'.split(' '));
 const trigger=/[\/√^²³⁴⁵⁶⁷⁸⁹₀-₉=<>≤≥≈≠∫∮Σ∑]|\b(?:sqrt|sin|cos|tan|exp|ln|log)\b/;
 function inline(value){
  if(root.LinearMath?.hasMath(value))return root.LinearMath.render(value);
  const source=String(value??'').replace(/(Always|Sphere|Ellipse|ellipses|and|as)(?=(?:mv|x²|b\/|W\/))/g,'$1 ').replace(/minimae(?=\^)/g,'minima e').replace(/atarcsin/g,'at arcsin');if(!source.trim()||source.length>6000)return esc(source);
  // Leave URLs and filenames intact. Partition prose at word boundaries, never
  // infer the extent of a numerator from surrounding natural-language words.
  if(/https?:\/\/|www\.|\.(?:pdf|js|html|json)\b/.test(source))return esc(source);
  if(/\.\s/.test(source))return source.split(/(?<=\.)\s+/).map(inline).join(' ');
  // Compound units and monetary rates need the entire ratio kept together.
  const compound=/(?:\((?:mg\/L|cm\/s|mi\/gal)\)\/(?:°[CF]|\(mi\/h\))|lb\/\(dollars\/lb\)|\$\d+(?:\.\d+)?\/(?:lb|yard|item))/g;
  const compoundMatches=[...source.matchAll(compound)];
  const unitNode=v=>{if(v[0]==='('&&v.endsWith(')')){let d=0,outer=true;for(let i=0;i<v.length-1;i++){if(v[i]==='(')d++;if(v[i]===')')d--;if(d===0){outer=false;break;}}if(outer)v=v.slice(1,-1);}let depth=0;for(let j=0;j<v.length;j++){if(v[j]==='(')depth++;if(v[j]===')')depth--;if(v[j]==='/'&&!depth)return '<mfrac>'+unitNode(v.slice(0,j))+unitNode(v.slice(j+1))+'</mfrac>';}return '<mtext>'+esc(v)+'</mtext>';};
  if(compoundMatches.length){let end=0,out='';for(const m of compoundMatches){out+=inline(source.slice(end,m.index))+mathHTML(m[0],unitNode(m[0]),true);end=m.index+m[0].length;}return out+inline(source.slice(end));}
  const unitRatio=/(?<![A-Za-z])(?:°[CF]|ft[³²]?|shakes|seconds|mg|points|beats|copies|bacteria|gallons|thousands|miles|mi|rad|gal|lb|CFU|chirp|barrels|million|fibers|cents|dollars|spaces|mL|mol|kg|g|cm|mm|km|m|J|N|C|V|W|A)\/(?:°[CF]|in[²³]?|second|lb|L|gal|h|hour|kWh|mL|year|day|min|space|mol|kg|mm|cm|km|m|s|C|A|\$)(?:[²³])?(?![A-Za-z])/g;
  const unitMatches=[...source.matchAll(unitRatio)];
  if(unitMatches.length){let end=0,out='';for(const m of unitMatches){out+=inline(source.slice(end,m.index));const [n,d]=m[0].split('/'),power=/[²³]$/.exec(d);const denominator=power?'<msup><mtext>'+esc(d.slice(0,-1))+'</mtext><mn>'+supMap[power[0]]+'</mn></msup>':'<mtext>'+esc(d)+'</mtext>';out+=mathHTML(m[0],'<mfrac><mtext>'+esc(n)+'</mtext>'+denominator+'</mfrac>',true);end=m.index+m[0].length;}return out+inline(source.slice(end));}
  const pieces=[];let start=0;
  function chunk(end){const raw=source.slice(start,end),lead=/^[\s:]+/.exec(raw)?.[0]||'',trail=/\s*$/.exec(raw)[0],body=raw.slice(lead.length,raw.length-trail.length).trim();
   if(!body){pieces.push(esc(raw));return;}
   if(trigger.test(body)&&body.endsWith('.')){try{pieces.push(esc(lead)+mathHTML(body.slice(0,-1),parse(body.slice(0,-1)),true)+'.'+esc(trail));return;}catch(_){}}
   if(trigger.test(body)){try{pieces.push(esc(lead)+mathHTML(body,parse(body),true)+esc(trail));return;}catch(_){}}
   if(body.includes('/')){
    // Keep unmatched prose parentheses outside the equation. Only remove a
    // boundary delimiter after parsing has failed, and preserve it visibly.
    let core=body,left='',right='';
    for(let tries=0;tries<12;tries++){
     if(/^[(:;,]/.test(core)){left+=core[0];core=core.slice(1);}
     else if(/[).;,:!?]$/.test(core)){right=core.slice(-1)+right;core=core.slice(0,-1);}
     else break;
     try{pieces.push(esc(lead+left)+mathHTML(core,parse(core),true)+esc(right+trail));return;}catch(_){}
    }
   }
   // A prose aside can leave unmatched delimiters in a mathematical chunk.
   // Split only at those delimiters; preserve every source character in place.
   if(body.includes('/')){
    const stack=[],cuts=[],pairs={')':'(',']':'[','}':'{','⟩':'⟨'};
    for(let j=0;j<body.length;j++){const c=body[j];if('([{⟨'.includes(c))stack.push(j);else if(pairs[c]){if(stack.length&&body[stack[stack.length-1]]===pairs[c])stack.pop();else cuts.push(j);}}
    cuts.push(...stack);cuts.sort((a,b)=>a-b);
    if(cuts.length){let pos=0,out=esc(lead);for(const end of [...cuts,body.length]){const fragment=body.slice(pos,end);try{out+=trigger.test(fragment)?mathHTML(fragment,parse(fragment),true):esc(fragment);}catch(_){out+=esc(fragment);}if(end<body.length)out+=esc(body[end]);pos=end+1;}pieces.push(out+esc(trail));return;}
   }
   pieces.push(esc(raw));
  }
  for(const m of source.matchAll(/[A-Za-z]{2,}/g)){
   if(source[m.index-1]==='_')continue;
   if(m[0].length>=3&&/^[A-Za-z]{2}[A-Z_a-z]$/.test(m[0])&&/[A-Z]/.test(m[0])&&!['For','The','All','Not','Use','Let','Yes','Its'].includes(m[0]))continue;
   if(m[0].length>3&&/[a-z][A-Z]$/.test(m[0])){const word=m[0].slice(0,-1);chunk(m.index);pieces.push(esc(word));start=m.index+word.length;continue;}
   if(['ckt','kqz','xyz','akt','mgt','kqr','mgL'].includes(m[0])||mathWords.has(m[0])||(/^(sin|cos|tan|sec|csc|cot|sinh|cosh|tanh|ln|log)[xyzcv]$/.test(m[0]))||(m[0].length===2&&!proseWords.has(m[0])))continue;
   chunk(m.index);pieces.push(esc(m[0]));start=m.index+m[0].length;
  }
  chunk(source.length);return pieces.join('');
 }
 function render(value){
  if(root.LinearMath?.hasMath(value))return root.LinearMath.render(value);
  const source=String(value??'');if(!source.trim()||source.length>6000)return esc(source);
  if(source.endsWith('.')){try{return mathHTML(source.slice(0,-1),parse(source.slice(0,-1)))+'.';}catch(_){}}
  if(/(?:^|\s)(?:is|in|as|at|of|to|or|by|on|an|if|be|it|no|so|we|do|up)(?=\s|$)/i.test(source))return inline(source);
  try{return mathHTML(source,parse(source));}catch(_){return inline(source);}
 }
 root.SolutionMath={render,html:render,inline,parse};
})(typeof window!=='undefined'?window:globalThis);
