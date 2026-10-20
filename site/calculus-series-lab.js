/* Original Glasshouse explorations for Stewart 8e, Chapter 11 section topics.
   Finite constructions illustrate theorems; they do not establish convergence. */
window.CalculusSeriesLab = (() => {
  'use strict';
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const clamp=(x,a,b)=>Math.max(a,Math.min(b,x)),fmt=x=>!Number.isFinite(x)?'—':x===0?'0':Number(x.toPrecision(6)).toString();
  const topics=[
    ['11.1','Sequences','Watch a limit become a promise','A sequence is a list of individual values. Convergence means every sufficiently late term stays close to one number.','5-1-sequences'],
    ['11.2','Series','Small pieces. A growing total.','A series asks what happens to the running total, not just what happens to the next term.','5-2-infinite-series'],
    ['11.3','Integral test','Put a fence around the tail','For positive, continuous, decreasing functions, neighboring areas bound the sum still to come.','5-3-the-divergence-and-integral-tests'],
    ['11.4','Comparison','Compare with something you know','Use the same positive benchmark term by term, then connect the inequality to a convergence theorem.','5-4-comparison-tests'],
    ['11.5','Alternating series','Overshoot. Undershoot. Close in.','Decreasing alternating terms trap the answer between consecutive partial sums.','5-5-alternating-series'],
    ['11.6','Ratio & root tests','How fast do the terms shrink?','The limiting ratio or nth root tests absolute convergence. A limit of one needs another test.','5-6-ratio-and-root-tests'],
    ['11.7','Choose a test','Learn to recognize the structure','Choose a useful first test and see the condition that makes it apply.','5-6-ratio-and-root-tests'],
    ['11.8','Power series','Find the safe interval','A power series is a different numerical series at each x. The endpoints need their own tests.','6-1-power-series-and-functions'],
    ['11.9','Function representations','One series. Three functions.','Differentiate or integrate inside the radius of convergence to build new function representations.','6-2-properties-of-power-series'],
    ['11.10','Taylor series','Build a function, one degree at a time','Match derivatives at a center. Compare the polynomial with the function and measure the remaining error.','6-3-taylor-and-maclaurin-series'],
    ['11.11','Taylor applications','Make an approximation you can trust','An error bound turns “looks close” into a mathematical guarantee at the chosen input.','6-4-working-with-taylor-series']
  ];
  const meta=section=>topics.find(t=>t[0]===section)||topics[0];
  const defaults=section=>({section,N:section==='11.1'?12:section==='11.2'?8:section==='11.5'?8:section==='11.10'?4:section==='11.11'?3:12,p:2,r:.65,epsilon:.15,sequence:'decay',family:'factorial',test:'ratio',center:0,radius:1,x:section==='11.11'?.3:.5,fn:section==='11.11'?'sin':'exp',operation:'sum',case:0,digits:3,stage:0});
  function normalise(section,raw={}) {
    const s={...defaults(section),...raw,section};
    for(const[k,lo,hi]of[['N',['11.10','11.11'].includes(section)?0:1,60],['p',.5,3],['r',-1.2,1.2],['epsilon',.02,.5],['center',-1,1],['radius',.5,2],['x',-4,4],['case',0,5],['digits',2,8],['stage',0,3]]){
      const n=Number(s[k]);s[k]=Number.isFinite(n)?clamp(n,lo,hi):defaults(section)[k];
    }
    s.N=Math.round(s.N);s.case=Math.round(s.case);s.digits=Math.round(s.digits);s.stage=Math.round(s.stage);
    if(['11.10','11.11'].includes(section))s.N=clamp(s.N,0,14);
    if(section==='11.9')s.x=clamp(s.x,-.9,.9);
    if(section==='11.11')s.x=clamp(s.x,-1.5,1.5);
    for(const[k,allowed]of Object.entries({sequence:['decay','alternating','oscillating'],family:['factorial','geometric','power'],test:['ratio','root'],fn:['exp','sin','cos'],operation:['sum','derivative','integral']}))if(!allowed.includes(s[k]))s[k]=defaults(section)[k];
    if(section==='11.11'&&s.fn==='cos')s.fn='sin';return s;
  }
  const factorial=n=>{let x=1;for(let k=2;k<=n;k++)x*=k;return x;};
  function taylor(fn,c,x,d){let sum=0;for(let k=0;k<=d;k++){const derivative=fn==='exp'?Math.exp(c):c===0?(fn==='sin'?[0,1,0,-1]:[1,0,-1,0])[k%4]:fn==='sin'?Math.sin(c+k*Math.PI/2):Math.cos(c+k*Math.PI/2);sum+=derivative*(x-c)**k/factorial(k);}return sum;}
  const actual=(fn,x)=>fn==='exp'?Math.exp(x):fn==='sin'?Math.sin(x):Math.cos(x);
  const bound=(fn,c,x,d)=>(fn==='exp'?Math.exp(Math.max(c,x)):1)*Math.abs(x-c)**(d+1)/factorial(d+1);
  const strategies=[
    {formula:'Σ 1/n²',test:'Integral / p-series',why:'For x ≥ 1, x⁻² is positive, continuous and decreasing. The improper integral converges because p = 2 > 1.',result:'Converges',options:['Integral / p-series','Divergence test proves convergence','Ratio test with L = 1 proves convergence']},
    {formula:'Σ n/(n + 1)',test:'Divergence test',why:'The terms approach 1, not 0. A convergent series must have terms approaching zero.',result:'Diverges',options:['Divergence test','Alternating series test','Geometric series formula']},
    {formula:'Σ 2ⁿ/n!',test:'Ratio test',why:'The absolute ratio is 2/(n + 1), which approaches 0 < 1. This proves absolute convergence.',result:'Converges absolutely',options:['Ratio test','Divergence because numerator grows','p-series test directly']},
    {formula:'Σ (−1)ⁿ⁻¹/n',test:'Alternating series test',why:'The magnitudes 1/n decrease to zero, so alternating sums converge. The absolute series is harmonic and diverges.',result:'Converges conditionally',options:['Alternating series test','Absolute convergence by p-series','Divergence because signs change']},
    {formula:'Σ 1/(n² + 1)',test:'Comparison with 1/n²',why:'For n ≥ 1, 0 < 1/(n² + 1) ≤ 1/n². The larger benchmark has a convergent sum.',result:'Converges',options:['Comparison with 1/n²','Comparison with a divergent larger series proves divergence','Ratio test with L = 1 proves divergence']},
    {formula:'Σ (3/4)ⁿ',test:'Geometric series',why:'Each term is multiplied by 3/4. Its absolute value is below one, so the geometric series converges.',result:'Converges absolutely',options:['Geometric series','Alternating series test','Divergence because every term is positive']}
  ];
  function describe(section,raw={}) {
    const s=normalise(section,raw),m={...s,terms:[],sums:[],limit:null,conclusion:'',stats:[],steps:[],formula:''};
    let sum=0;
    function terms(fn,start=1){for(let j=0;j<s.N;j++){const n=start+j,a=fn(n);sum+=a;m.terms.push([n,a]);m.sums.push([n,sum]);}m.sum=sum;m.term=m.terms.at(-1)?.[1]??0;}
    if(section==='11.1'){
      const fn=n=>s.sequence==='oscillating'?(-1)**n:(s.sequence==='alternating'?(-1)**n:1)/n**s.p;terms(fn);
      m.limit=s.sequence==='oscillating'?null:0;m.cutoff=m.limit===null?null:Math.floor(s.epsilon**(-1/s.p))+1;
      // Integer K guarantees n ≥ K implies |a_n| < epsilon, with rounding guard.
      if(m.cutoff!==null)while(1/m.cutoff**s.p>=s.epsilon)m.cutoff++;
      m.formula=s.sequence==='oscillating'?'aₙ = (−1)ⁿ':`aₙ = ${s.sequence==='alternating'?'(−1)ⁿ /':'1 /'} nᵖ`;
      m.conclusion=m.limit===null?'Diverges: two subsequences stay at +1 and −1.':`Converges to 0. Every n ≥ ${m.cutoff} satisfies |aₙ| < ${fmt(s.epsilon)}.`;
      m.stats=[['Selected term aₙ',fmt(m.term)],['Proposed limit',m.limit===null?'Does not exist':'0'],['Tolerance ε',fmt(s.epsilon)],['Tail starts at',m.cutoff===null?'No such K':`K = ${m.cutoff}`]];
      m.steps=[['Read the index','Only integer n values are terms. The points are deliberately not connected.'],['Measure the distance','The shaded band is −ε < aₙ < ε. Distance to the proposed limit 0 is |aₙ|.'],['Control the whole tail',m.limit===null?'Alternating between ±1 never settles in a small band.':`Solve n⁻ᵖ < ε: choose an integer K > ε^(−1/p). Here K = ${m.cutoff}.`],['State what the limit means',m.conclusion+' A finite screen alone is not the proof.']];
    }else if(section==='11.2'){
      terms(n=>s.r**n,0);m.limit=Math.abs(s.r)<1?1/(1-s.r):null;m.remainder=m.limit===null?null:s.r**s.N/(1-s.r);m.formula='Sₙ = 1 + r + ⋯ + rⁿ⁻¹';
      m.conclusion=m.limit===null?'Diverges because the terms do not approach zero.':`Converges to 1/(1 − r) = ${fmt(m.limit)} because |r| < 1.`;
      m.stats=[['Terms included',s.N],['Last term rⁿ⁻¹',fmt(m.term)],['Partial sum Sₙ',fmt(m.sum)],['Signed tail S − Sₙ',m.remainder===null?'No finite sum':fmt(m.remainder)]];
      m.steps=[['Keep terms and totals separate','The upper panel shows each piece rᵏ. The lower panel shows the total after adding it.'],['Subtract a shifted copy','rSₙ shifts the terms by one position. Subtraction cancels the middle: (1 − r)Sₙ = 1 − rⁿ. At r = 1, Sₙ = N.'],['Take a justified limit','When |r| < 1, rⁿ → 0, so Sₙ → 1/(1 − r). For |r| ≥ 1 the term test rules out convergence.'],['Account for what is missing','For |r| < 1, S − Sₙ = rⁿ/(1 − r). With a negative ratio, the signed tail can change sign.']];
    }else if(section==='11.3'){
      terms(n=>1/n**s.p);m.lower=s.p>1?(s.N+1)**(1-s.p)/(s.p-1):null;m.upper=s.p>1?s.N**(1-s.p)/(s.p-1):null;m.formula='aₙ = 1/nᵖ,  f(x) = x⁻ᵖ';
      m.conclusion=s.p>1?'Converges: the positive decreasing tail fits between two finite areas.':'Diverges: the improper integral is infinite for p ≤ 1.';
      m.stats=[['Partial sum Sₙ',fmt(m.sum)],['Tail lower bound',m.lower===null?'Unbounded':fmt(m.lower)],['Tail upper bound',m.upper===null?'Unbounded':fmt(m.upper)],['p-series verdict',s.p>1?'p > 1 · converges':'p ≤ 1 · diverges']];
      m.steps=[['Check the hypotheses','For p > 0, x⁻ᵖ is positive, continuous and decreasing on x ≥ 1.'],['Fit the rectangles','A unit-width rectangle has area f(n). Decreasing heights compare that area with its left and right neighboring integrals.'],['Bound the infinite tail','For p > 1: (N + 1)^(1 − p)/(p − 1) ≤ Rₙ ≤ N^(1 − p)/(p − 1). The finite picture omits the rest of each area.'],['Estimate the whole sum',s.p>1?`Add Sₙ to both tail bounds: the sum lies between ${fmt(m.sum+m.lower)} and ${fmt(m.sum+m.upper)}.`:'For p ≤ 1 there is no finite tail bound or sum; a small last term does not fix this.']];
    }else if(section==='11.4'){
      terms(n=>1/(n**s.p+1));m.benchmark=m.terms.map(([n])=>[n,1/n**s.p]);m.ratio=s.N**s.p/(s.N**s.p+1);m.formula='0 < aₙ = 1/(nᵖ + 1) ≤ bₙ = 1/nᵖ';m.conclusion=s.p>1?'Converges by direct comparison with the convergent p-series.':'Diverges by limit comparison: aₙ/bₙ → 1 and the p-series diverges.';
      m.stats=[['Term aₙ',fmt(m.term)],['Benchmark bₙ',fmt(1/s.N**s.p)],['Current ratio aₙ/bₙ',fmt(m.ratio)],['Limiting ratio','1 · finite and positive']];
      m.steps=[['Choose a positive benchmark','The extra +1 in the denominator suggests bₙ = 1/nᵖ. Both sequences are positive.'],['Use the inequality in the right direction','aₙ ≤ bₙ proves convergence if Σbₙ converges. A divergent larger series alone proves nothing about the smaller one.'],['Use limit comparison when needed','aₙ/bₙ = nᵖ/(nᵖ + 1) → 1. A finite positive ratio means both positive series share convergence behavior.'],['Finish with the p-test',m.conclusion]];
    }else if(section==='11.5'){
      terms(n=>(-1)**(n-1)/n**s.p);m.next=sum+(-1)**s.N/(s.N+1)**s.p;m.lower=Math.min(sum,m.next);m.upper=Math.max(sum,m.next);m.errorBound=1/(s.N+1)**s.p;m.formula='Sₙ = Σₖ₌₁ᴺ (−1)ᵏ⁻¹/kᵖ';m.conclusion=s.p>1?'Absolutely convergent: the absolute p-series also converges.':'Conditionally convergent: alternating test passes, but the absolute p-series diverges.';
      m.stats=[['Partial sum Sₙ',fmt(sum)],['Next partial sum',fmt(m.next)],['Maximum error',fmt(m.errorBound)],['Convergence',s.p>1?'Absolute':'Conditional']];
      m.steps=[['Check before alternating','The magnitudes bₙ = 1/nᵖ are positive, decreasing and approach zero for every p in this lab.'],['Follow the overshoots','Adding a positive term moves up; adding a negative term moves down. The steps shrink as n grows.'],['Trap the true sum',`Consecutive totals enclose S: ${fmt(m.lower)} ≤ S ≤ ${fmt(m.upper)}. The bracket width is the next term’s magnitude.`],['Turn the bracket into an error bound',`|S − Sₙ| ≤ 1/(N + 1)ᵖ = ${fmt(m.errorBound)}. ${m.conclusion}`]];
    }else if(section==='11.6'){
      const value=n=>s.family==='factorial'?Math.abs(s.r)**n/factorial(n):s.family==='geometric'?Math.abs(s.r)**n:1/n**s.p;terms(value);
      m.ratios=Array.from({length:s.N},(_,j)=>{const n=j+1;return[n,s.family==='factorial'?Math.abs(s.r)/(n+1):s.family==='geometric'?Math.abs(s.r):(n/(n+1))**s.p];});
      m.roots=Array.from({length:s.N},(_,j)=>{const n=j+1;return[n,value(n)**(1/n)];});
      m.L=s.family==='power'?1:s.family==='factorial'?0:Math.abs(s.r);m.testValue=(s.test==='ratio'?m.ratios:m.roots).at(-1)[1];
      m.formula=s.family==='factorial'?'aₙ = |r|ⁿ/n!':s.family==='geometric'?'aₙ = |r|ⁿ':'aₙ = 1/nᵖ';
      m.conclusion=m.L<1?'L < 1: the series converges absolutely.':m.L>1?'L > 1: the series diverges.':'L = 1: this test is inconclusive. '+(s.family==='power'?(s.p>1?'The p-test proves convergence.':'The p-test proves divergence.'):'At |r| = 1, terms are 1, so the term test proves divergence.');
      m.zeroRatio=s.r===0&&s.family!=='power'&&s.test==='ratio';
      if(m.zeroRatio)m.conclusion='All terms are zero, so the series converges immediately. The ratio 0/0 is undefined; use this direct argument rather than the ratio test.';
      m.stats=[['Current test value',m.zeroRatio?'Undefined · 0/0':fmt(m.testValue)],['Proved limiting L',m.zeroRatio?'Ratio undefined':fmt(m.L)],['Threshold','1'],['Test verdict',m.zeroRatio?'Use the zero-series argument':m.L===1?'Inconclusive':m.L<1?'Converges absolutely':'Diverges']];
      m.steps=[['Use absolute values','The ratio and root tests examine |aₙ₊₁/aₙ| and |aₙ|^(1/n). They test absolute convergence.'],['Compute the selected limit',s.family==='factorial'?'Factorial growth dominates any fixed exponential. Ratio = |r|/(n + 1) → 0; the nth root also tends to 0.':s.family==='geometric'?'Both test expressions equal |r|. When r = 0 every term vanishes; convergence is immediate even though a ratio 0/0 is undefined.':'Ratio = (n/(n + 1))ᵖ → 1. Root = n^(−p/n) → 1.'],['Compare L with one','L < 1 gives absolute convergence. L > 1 gives divergence. L = 1 supplies no conclusion.'],['Use another test at the boundary',m.conclusion]];
    }else if(section==='11.7'){
      m.strategy=strategies[s.case];m.formula=m.strategy.formula;m.conclusion=m.strategy.result;m.stats=[['Look for','Structure first'],['Useful first test',m.strategy.test],['Conclusion',m.strategy.result]];m.steps=[['Look at the terms','Check whether the terms even approach zero before doing more work.'],['Recognize the structure','Constant ratios suggest geometric series. Factorials suggest ratios. Rational powers suggest a p-series or comparison.'],['Verify the conditions',m.strategy.why],['Explain the conclusion',m.strategy.result+'. A matching formula without its hypotheses is not a proof.']];
    }else if(section==='11.8'){
      m.u=(s.x-s.center)/s.radius;terms(n=>m.u**n/n);m.position=m.u< -1||m.u>=1?'diverges':m.u===-1?'conditional':'absolute';m.limit=m.position==='diverges'?null:-Math.log1p(-m.u);m.formula='Σₙ₌₁∞ [(x − c)/R]ⁿ/n';m.conclusion=m.position==='diverges'?(m.u===1?'Right endpoint: the harmonic series diverges.':'Outside the interval: terms fail to approach zero.'):m.position==='conditional'?'Left endpoint: alternating harmonic series, sum = −ln 2; conditional convergence.':'Inside the radius: absolute convergence to −ln(1 − u).';
      m.stats=[['Normalized input u',fmt(m.u)],['Partial sum Sₙ',fmt(m.sum)],['Convergence interval',`[${fmt(s.center-s.radius)}, ${fmt(s.center+s.radius)})`],['At this x',m.position]];
      m.steps=[['Translate and scale','Set u = (x − c)/R. Each x picks a different numerical series.'],['Find the radius','The ratio limit is |u|. Thus |x − c| < R gives absolute convergence; outside it terms fail the zero-limit requirement.'],['Test both endpoints','At x = c − R: Σ(−1)ⁿ/n converges conditionally. At x = c + R: Σ1/n diverges.'],['Keep boundary and interior distinct',m.conclusion+' The filled left dot and open right dot record these separate tests.']];
    }else if(section==='11.9'){
      m.polynomial=x=>{let v=0;for(let n=0;n<=s.N;n++)v+=s.operation==='sum'?x**n:s.operation==='derivative'?(n===0?0:n*x**(n-1)):x**(n+1)/(n+1);return v;};
      m.function=x=>s.operation==='sum'?1/(1-x):s.operation==='derivative'?1/(1-x)**2:-Math.log1p(-x);m.estimate=m.polynomial(s.x);m.exact=m.function(s.x);m.error=Math.abs(m.exact-m.estimate);
      m.formula=s.operation==='sum'?'Σₙ₌₀∞ xⁿ = 1/(1 − x)':s.operation==='derivative'?'Σₙ₌₁∞ n xⁿ⁻¹ = 1/(1 − x)²':'Σₙ₌₀∞ xⁿ⁺¹/(n + 1) = −ln(1 − x)';m.conclusion='These identities hold for |x| < 1. The selected finite polynomial is an approximation.';
      m.stats=[['Finite polynomial',fmt(m.estimate)],['Function at x',fmt(m.exact)],['Absolute error',fmt(m.error)],['Shared interior','−1 < x < 1']];m.steps=[['Start from a known series','For |x| < 1, the geometric identity is 1 + x + x² + ⋯ = 1/(1 − x).'],['Operate term by term',s.operation==='derivative'?'Differentiate each xⁿ to n xⁿ⁻¹. The constant term disappears.':s.operation==='integral'?'Integrate from 0 to x. Each tⁿ becomes xⁿ⁺¹/(n + 1); the lower endpoint sets the integration constant to zero.':'Keep the geometric series as the starting representation.'],['Respect the domain','Differentiation and integration preserve the radius of convergence. Endpoint behavior must be checked separately for each new series.'],['Measure what truncation changes',`Keeping original indices 0 through ${s.N} gives an absolute error ${fmt(m.error)} at x = ${fmt(s.x)}. The two curves use the same scale.`]];
    }else{
      const c=section==='11.11'?0:s.center;m.center=c;m.polynomial=x=>taylor(s.fn,c,x,s.N);m.function=x=>actual(s.fn,x);m.estimate=m.polynomial(s.x);m.exact=m.function(s.x);m.error=Math.abs(m.exact-m.estimate);m.bound=bound(s.fn,c,s.x,s.N);m.tolerance=10**(-s.digits);m.minimum=Array.from({length:41},(_,n)=>n).find(n=>bound(s.fn,c,s.x,n)<=m.tolerance);
      m.formula=`P${s.N}(x) = Σₖ₌₀^${s.N} f⁽ᵏ⁾(${fmt(c)}) (x − ${fmt(c)})ᵏ/k!`;
      m.conclusion=section==='11.11'?(m.bound<=m.tolerance?'Certified: this remainder bound meets the chosen tolerance.':'Not yet certified by this bound. Add degrees or move closer to the center.'):'The polynomial matches derivatives through degree N at the center. The remainder bound controls the approximation at x.';
      m.stats=section==='11.11'?[['Approximation',fmt(m.estimate)],['Absolute error',fmt(m.error)],['Guaranteed bound',fmt(m.bound)],['Required error',fmt(m.tolerance)]]:[['Pₙ(x)',fmt(m.estimate)],['f(x)',fmt(m.exact)],['Absolute error',fmt(m.error)],['Remainder bound',fmt(m.bound)]];
      m.steps=[['Match at the center',`Choose f = ${s.fn==='exp'?'eˣ':s.fn+' x'} and center c = ${fmt(c)}. The kth coefficient is f⁽ᵏ⁾(c)/k!, so the derivatives agree there.`],['Add one degree at a time','Each new degree adds f⁽ᵏ⁾(c)(x − c)ᵏ/k!. Some trigonometric coefficients are zero; adding that degree genuinely leaves the polynomial unchanged.'],['Bound the omitted terms',`Taylor’s theorem gives |Rₙ(x)| ≤ M|x − c|ⁿ⁺¹/(N + 1)!. ${s.fn==='exp'?'Here M = exp(max(c,x)) bounds the next derivative on the segment.':'Every derivative of sin or cos has magnitude at most 1, so M = 1 works.'}`],['Decide if it is accurate enough',section==='11.11'?`${m.conclusion} The first degree certified here is ${m.minimum}. A bound above tolerance does not prove the actual error exceeds it.`:`At x = c, every polynomial equals the function exactly. Away from c, compare actual error ${fmt(m.error)} with bound ${fmt(m.bound)}.`]];
    }
    return m;
  }
  // SVGs use CSS variables in the app; explicit palette replacement supports native QA.
  const text=(x,y,value,cls='',anchor='start')=>`<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${esc(value)}</text>`;
  const line=(x1,y1,x2,y2,cls='cs-grid')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}"/>`;
  const dot=(x,y,cls='cs-dot',r=4)=>`<circle cx="${x}" cy="${y}" r="${r}" class="${cls}"/>`;
  function plot({x=62,y=54,w=590,h=220,xmin=0,xmax=60,ymin=-1.3,ymax=1.3,label='value',xlabel=xmin<0?'x · input':'n · integer index',id='main'}){
    const X=v=>x+(v-xmin)/(xmax-xmin)*w,Y=v=>y+h-(v-ymin)/(ymax-ymin)*h;
    let svg=`<defs><clipPath id="cs-${id}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8"/></clipPath></defs><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" class="cs-plot-paper"/>`;
    for(let k=0;k<=4;k++){const py=y+k*h/4,v=ymax-k*(ymax-ymin)/4;svg+=line(x,py,x+w,py)+text(x-10,py+4,fmt(v),'cs-tick','end');}
    for(let k=0;k<=4;k++){const px=x+k*w/4,v=xmin+k*(xmax-xmin)/4;svg+=line(px,y,px,y+h,'cs-grid-vertical')+text(px,y+h+21,fmt(v),'cs-tick','middle');}
    svg+=text(x,y-19,label,'cs-label')+text(x+w,y+h+36,xlabel,'cs-xlabel','end')+line(x,y,x,y+h,'cs-axis')+line(x,y+h,x+w,y+h,'cs-axis');if(ymin<0&&ymax>0)svg+=line(x,Y(0),x+w,Y(0),'cs-zero');
    return{X,Y,svg,clip:body=>`<g clip-path="url(#cs-${id})">${body}</g>`};
  }
  const path=(pairs,p,cls)=>`<path d="${pairs.map(([x,y],j)=>(j?'L':'M')+fmt(p.X(x))+','+fmt(p.Y(y))).join('')}" class="${cls}"/>`;
  const points=(pairs,p,cls='cs-dot')=>pairs.map(([x,y],j)=>`<circle data-cs-key="${cls}-${x}" cx="${p.X(x)}" cy="${p.Y(y)}" r="${j===pairs.length-1?5:3.5}" class="${j===pairs.length-1?cls+' cs-last':cls}" ${j===pairs.length-1?'tabindex="0"':''} aria-label="Index ${fmt(x)}, value ${fmt(y)}"><title>Index ${fmt(x)} · value ${fmt(y)}</title></circle>`).join('');
  const curve=(fn,p,lo,hi,cls)=>path(Array.from({length:241},(_,i)=>{const x=lo+(hi-lo)*i/240;return[x,fn(x)];}),p,cls);
  function svg(section,raw={}){
    const m=describe(section,raw);let body='',height=360,caption='';
    if(section==='11.1'){
      const p=plot({ymin:-1.25,ymax:1.25,label:'aₙ · individual terms'});body=p.svg;
      body+=p.clip(`<rect x="${p.X(0)}" y="${p.Y(m.epsilon)}" width="590" height="${p.Y(-m.epsilon)-p.Y(m.epsilon)}" class="cs-band"/>`+line(p.X(0),p.Y(m.epsilon),p.X(60),p.Y(m.epsilon),'cs-dashed')+line(p.X(0),p.Y(-m.epsilon),p.X(60),p.Y(-m.epsilon),'cs-dashed')+points(m.terms,p));
      if(m.cutoff!==null&&m.cutoff<=60)body+=line(p.X(m.cutoff),54,p.X(m.cutoff),274,'cs-marker')+text(clamp(p.X(m.cutoff),90,620),342,'K = '+m.cutoff,'cs-accent','middle');
      caption=m.cutoff>60?'K lies beyond this fixed 60-term window. The algebra still controls the whole tail.':'Coral = terms included so far. Aqua band = acceptable distance from zero.';
    }else if(section==='11.2'){
      height=500;const p=plot({y:48,h:130,ymin:-2,ymax:2,label:'aₖ = rᵏ · each piece',id:'terms'}),q=plot({y:280,h:130,ymin:-3,ymax:12,label:'Sₙ · running total',id:'sums'});body=p.svg+q.svg;
      body+=p.clip(m.terms.map(([n,a])=>line(p.X(n),p.Y(0),p.X(n),p.Y(a),'cs-stem')).join('')+points(m.terms,p));body+=q.clip(points(m.sums.map(([n,a])=>[n+1,a]),q,'cs-aqua-dot')+(m.limit===null?'':line(q.X(0),q.Y(m.limit),q.X(60),q.Y(m.limit),'cs-dashed')));
      caption='Fixed windows: terms −2 to 2; totals −3 to 12. Values outside the windows are clipped, not rescaled.';
    }else if(section==='11.3'){
      const p=plot({xmin:1,xmax:13,ymin:0,ymax:1.05,label:'f(x) = x⁻ᵖ · unit-width rectangles',xlabel:'x · integration coordinate'});body=p.svg;
      const start=m.N,rects=Array.from({length:12},(_,j)=>{const n=j+1;return`<rect x="${p.X(n)}" y="${p.Y(1/(n+1)**m.p)}" width="${p.X(n+1)-p.X(n)}" height="${p.Y(0)-p.Y(1/(n+1)**m.p)}" class="${n>=start?'cs-tail-rect':'cs-rect'}"/>`;}).join('');
      body+=p.clip(rects+curve(x=>x**(-m.p),p,1,13,'cs-function')+(m.N<=13?line(p.X(m.N),54,p.X(m.N),274,'cs-marker'):''));body+=line(62,324,652,324,'cs-axis')+dot(62+(m.N-1)/59*590,324,'cs-dot',5)+text(62,346,'N = 1','cs-tick')+text(652,346,'N = 60 · selected '+m.N,'cs-tick','end');caption='A rectangle over [n, n + 1] has height f(n + 1). Only x = 1…13 is drawn; tail bounds extend to infinity. The lower rail locates N on its full fixed scale.'+(m.N>12?' The selected tail begins beyond the curve window.':' Coral rectangles belong to the omitted tail.');
    }else if(section==='11.4'){
      const p=plot({xmin:1,xmax:60,ymin:0,ymax:1.05,label:'aₙ versus benchmark bₙ · same scale'});body=p.svg;
      body+=p.clip(m.benchmark.map(([n,b])=>line(p.X(n),p.Y(b),p.X(n),p.Y(m.terms[n-1][1]),'cs-gap')).join('')+points(m.benchmark,p,'cs-aqua-dot')+points(m.terms,p));caption='Aqua = 1/nᵖ. Coral = 1/(nᵖ + 1). The smaller terms alone prove convergence only when the benchmark converges.';
    }else if(section==='11.5'){
      height=465;const p=plot({y:50,h:190,ymin:0,ymax:1.5,label:'Sₙ · alternating partial sums'});body=p.svg+p.clip(points(m.sums,p)+`<rect x="${p.X(0)}" y="${p.Y(m.upper)}" width="590" height="${p.Y(m.lower)-p.Y(m.upper)}" class="cs-band"/>`);
      // Separate local interval zoom; labels state its changing scale explicitly.
      const lo=m.lower,hi=m.upper,X=v=>90+(v-lo)/(hi-lo)*520;
      body+=text(62,308,'CURRENT ERROR BRACKET · LOCAL ZOOM','cs-label')+line(90,356,610,356,'cs-bracket')+dot(90,356,'cs-aqua-dot',6)+dot(610,356,'cs-dot',6)+text(90,386,fmt(lo),'','middle')+text(610,386,fmt(hi),'','middle')+text(X(m.sum),337,'Sₙ','cs-accent','middle')+text(X(m.next),415,'Sₙ₊₁','cs-muted','middle');caption='The top plot stays fixed. The lower bracket is enlarged to read its endpoints; its true width is the displayed error bound.';
    }else if(section==='11.6'){
      const p=plot({ymin:0,ymax:1.4,label:m.test==='ratio'?'|aₙ₊₁ / aₙ|':'|aₙ|¹⁄ⁿ'});body=p.svg+p.clip(line(p.X(0),p.Y(1),p.X(60),p.Y(1),'cs-threshold')+(m.zeroRatio?'':points(m.test==='ratio'?m.ratios:m.roots,p)));body+=text(649,p.Y(1)-10,'threshold 1','cs-muted','end');caption=m.zeroRatio?'At r = 0 all terms vanish. Ratio 0/0 is undefined, so no ratio points are plotted. The zero series converges directly.':'The threshold and vertical scale stay fixed. A finite value below one is not a substitute for the limiting test.';
    }else if(section==='11.7'){
      height=280;body=text(55,45,'LOOK FOR THE STRUCTURE','cs-label')+text(55,99,m.strategy.formula,'cs-big')+line(55,126,650,126,'cs-grid');
      const labels=['Terms → 0?','Recognizable form?','Conditions met?'];labels.forEach((label,j)=>{body+=`<circle cx="${85+j*215}" cy="181" r="20" class="cs-step-node"/>`+text(85+j*215,187,j+1,'cs-accent','middle')+text(85+j*215,228,label,'cs-tick','middle');});caption='Choose a series, then use the test-choice exercise below. Every conclusion needs a reason.';
    }else if(section==='11.8'){
      height=490;const X=x=>65+(x+4)/8*590,l=m.center-m.radius,r=m.center+m.radius;body=text(65,35,'CONVERGENCE INTERVAL · FIXED x SCALE','cs-label')+line(65,100,655,100,'cs-axis')+line(X(l),100,X(r),100,'cs-interval')+dot(X(l),100,'cs-aqua-dot',7)+dot(X(r),100,'cs-open-dot',7);
      for(let x=-4;x<=4;x++)body+=line(X(x),107,X(x),114,'cs-axis')+text(X(x),138,x,'cs-tick','middle');body+=line(X(m.x),52,X(m.x),83,'cs-probe')+text(X(m.x),45,'x','cs-accent','middle')+text(X(l),172,'included','cs-tick','middle')+text(X(r),172,'excluded','cs-tick','middle');
      const p=plot({y:230,h:160,ymin:-3,ymax:5,label:'Sₙ at your x · fixed sum scale'});body+=p.svg+p.clip(points(m.sums,p,'cs-dot')+(m.limit===null?'':line(p.X(0),p.Y(m.limit),p.X(60),p.Y(m.limit),'cs-dashed')));caption='Filled left endpoint = conditional convergence. Open right endpoint = divergence. Off-scale totals are clipped.';
    }else if(['11.9','11.10'].includes(section)){
      const rep=section==='11.9',exp=!rep&&m.fn==='exp',p=plot({xmin:rep?-.95:-4,xmax:rep?.95:4,ymin:rep?-3:exp?-3:-2,ymax:rep?(m.operation==='derivative'?30:12):exp?56:2,label:'Function & finite polynomial · common scale'});body=p.svg;
      const lo=rep?-.95:-4,hi=rep?.95:4,xx=Array.from({length:121},(_,j)=>lo+(hi-lo)*j/120),ribbon=[...xx.map(x=>[x,m.function(x)]),...xx.slice().reverse().map(x=>[x,m.polynomial(x)])];
      body+=p.clip(path(ribbon,p,'cs-error-fill')+curve(m.function,p,lo,hi,'cs-function')+curve(m.polynomial,p,lo,hi,'cs-polynomial')+line(p.X(m.x),54,p.X(m.x),274,'cs-probe-guide')+line(p.X(m.x),p.Y(m.exact),p.X(m.x),p.Y(m.estimate),'cs-gap')+dot(p.X(m.x),p.Y(m.exact),'cs-aqua-dot',5)+dot(p.X(m.x),p.Y(m.estimate),'cs-open-dot',7));
      if(!rep)body+=line(p.X(m.center),54,p.X(m.center),274,'cs-marker')+text(p.X(m.center),342,'center c','cs-muted','middle');caption='Aqua = exact function. Coral dashed = polynomial. Shading separates the curves; it is not an integral error bound. The fixed window clips off-scale values.';
    }else{
      height=420;const p=plot({xmin:0,xmax:14,ymin:-12,ymax:2,label:'log₁₀(error bound) · each extra degree',xlabel:'N · polynomial degree'});body=p.svg;
      const pairs=Array.from({length:15},(_,n)=>[n,Math.log10(Math.max(1e-12,bound(m.fn,0,m.x,n)))]);body+=p.clip(path(pairs,p,'cs-polynomial')+points(pairs.slice(0,m.N+1),p)+line(p.X(0),p.Y(-m.digits),p.X(14),p.Y(-m.digits),'cs-dashed'))+text(649,p.Y(-m.digits)-9,'tolerance 10⁻'+m.digits,'cs-muted','end');caption=m.x===0?'At x = 0 the remainder is exactly zero for every degree. Zero is displayed at the lower edge of this logarithmic window.':'This is a logarithmic error scale: one grid unit means a factor of ten. Bounds below 10⁻¹² are drawn at the lower edge.';
    }
    return{markup:`<svg class="cs-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 710 ${height}" role="img" aria-label="${esc(meta(section)[2]+'. '+caption)}"><title>${esc(meta(section)[2])}</title><rect width="710" height="${height}" class="cs-paper"/>${body}</svg>`,caption};
  }
  function controls(section,s){
    const list=[];const range=(key,label,min,max,step)=>list.push({key,label,min,max,step});const select=(key,label,options)=>list.push({key,label,options});
    if(section==='11.1'){select('sequence','Sequence',[['decay','Approach from above · 1/nᵖ'],['alternating','Approach from both sides · (−1)ⁿ/nᵖ'],['oscillating','Never settle · (−1)ⁿ']]);range('N','Terms shown N',1,60,1);if(s.sequence!=='oscillating')range('p','Decay power p',.5,3,.1);range('epsilon','Tolerance ε',.02,.5,.01);}
    if(section==='11.2'){range('r','Common ratio r',-1.2,1.2,.05);range('N','Number of terms N',1,60,1);}
    if(['11.3','11.4','11.5'].includes(section)){range('p','Power p',.5,3,.1);range('N','Terms included N',1,60,1);}
    if(section==='11.6'){select('family','Series family',[['factorial','|r|ⁿ / n!'],['geometric','|r|ⁿ'],['power','1/nᵖ']]);select('test','Test to inspect',[['ratio','Ratio test'],['root','Root test']]);range(s.family==='power'?'p':'r',s.family==='power'?'Power p':'Exponential factor r',s.family==='power'?.5:0,s.family==='power'?3:1.2,.05);range('N','Test values shown',1,60,1);}
    if(section==='11.7')select('case','Series to investigate',strategies.map((q,j)=>[j,q.formula]));
    if(section==='11.8'){range('center','Center c',-1,1,.25);range('radius','Radius R',.5,2,.25);range('x','Probe x',-4,4,.25);range('N','Terms included N',1,60,1);}
    if(section==='11.9'){select('operation','Operation',[['sum','Original geometric series'],['derivative','Differentiate each term'],['integral','Integrate from 0 to x']]);range('N','Last original index N',1,30,1);range('x','Probe x',-.9,.9,.05);}
    if(['11.10','11.11'].includes(section)){select('fn','Function',section==='11.10'?[['exp','Exponential · eˣ'],['sin','Sine · radians'],['cos','Cosine · radians']]:[['sin','Sine · radians'],['exp','Exponential · eˣ']]);range('N','Polynomial degree N',0,14,1);if(section==='11.10')range('center','Expansion center c',-1,1,.25);range('x','Evaluate at x',section==='11.10'?-4:-1.5,section==='11.10'?4:1.5,.05);if(section==='11.11')range('digits','Error tolerance · 10⁻ᵈ',2,8,1);}
    return list;
  }
  const choices=['Converges absolutely','Converges conditionally','Diverges'];
  function target(section,raw={}){
    const m=describe(section,raw);let prompt='',answer=0,options=null,reason='';
    if(section==='11.1'){prompt=`What is the selected term a${m.N}?`;answer=m.term;reason='Substitute the selected integer N into the sequence rule.';}
    else if(section==='11.2'){prompt=`What is S${m.N}, including indices 0 through ${m.N-1}?`;answer=m.sum;reason=m.r===1?'At r = 1, every term is 1, so Sₙ = N.':'Use Sₙ = (1 − rᴺ)/(1 − r). This is a finite sum even if the infinite series diverges.';}
    else if(section==='11.3'){if(m.p>1){prompt='What is the integral-test upper bound on the omitted tail Rₙ?';answer=m.upper;reason='Integrate x⁻ᵖ from N to infinity: N^(1 − p)/(p − 1).';}else{prompt='Does this p-series have a finite infinite sum?';options=['Yes','No'];answer=1;reason='The positive integral diverges for p ≤ 1, so the series diverges.';}}
    else if(section==='11.4'){prompt='What is lim aₙ/bₙ as n → ∞?';answer=1;reason='Divide nᵖ/(nᵖ + 1) by nᵖ: 1/(1 + n⁻ᵖ) → 1.';}
    else if(section==='11.5'){prompt='What upper bound does the alternating-series theorem give for |S − Sₙ|?';answer=m.errorBound;reason='Use the magnitude of the first omitted term: 1/(N + 1)ᵖ.';}
    else if(section==='11.6'){prompt='What does the selected ratio/root test itself prove?';options=['Absolute convergence','Divergence','Inconclusive / not applicable'];answer=m.zeroRatio?2:m.L<1?0:m.L>1?1:2;reason=m.conclusion;}
    else if(section==='11.7'){prompt='Which is a justified first test for this series?';const shift=(m.case+1)%3;options=[...m.strategy.options.slice(shift),...m.strategy.options.slice(0,shift)];answer=(3-shift)%3;reason=m.strategy.why;}
    else if(section==='11.8'){prompt='How does the infinite series behave at this x?';options=choices;answer=m.position==='absolute'?0:m.position==='conditional'?1:2;reason=m.conclusion;}
    else{prompt=section==='11.11'?'What is the guaranteed Taylor remainder bound at this x?':'What value does the finite polynomial give at this x?';answer=section==='11.11'?m.bound:m.estimate;reason=section==='11.11'?'Use M|x − c|^(N + 1)/(N + 1)! with the derivative bound shown in the explanation.':'Evaluate the displayed finite polynomial, rather than substituting the exact function value.';}
    return{prompt,answer,options,reason};
  }
  function grade(section,raw,value){const q=target(section,raw);if(String(value).trim()==='')return{correct:false,message:'Choose an answer or enter a number first.'};const n=Number(value),tolerance=q.answer===0?1e-12:Math.abs(q.answer)*.0001,ok=Number.isFinite(n)&&(q.options?n===q.answer:Math.abs(n-q.answer)<=tolerance);return{correct:ok,message:ok?'Correct. '+q.reason:'Try again. '+q.reason};}
  const controlHTML=(section,s)=>controls(section,s).map(c=>c.options?`<label class="cs-control" data-cs-control-key="${c.key}">${esc(c.label)}<select data-cs-param="${c.key}">${c.options.map(([v,label])=>`<option value="${v}" ${String(s[c.key])===String(v)?'selected':''}>${esc(label)}</option>`).join('')}</select></label>`:`<label class="cs-control" data-cs-control-key="${c.key}">${esc(c.label)}<output data-cs-output="${c.key}">${fmt(s[c.key])}</output><input type="range" min="${c.min}" max="${c.max}" step="${c.step}" value="${s[c.key]}" data-cs-param="${c.key}" aria-label="${esc(c.label)}"></label>`).join('');
  // Explicit semantic MathML: aggregate limits always sit above and below ∑.
  function equation(section,raw={}){
    const m=describe(section,raw),i=x=>`<mi>${esc(x)}</mi>`,n=x=>`<mn>${esc(x)}</mn>`,o=x=>`<mo>${esc(x)}</mo>`,row=(...a)=>`<mrow>${a.join('')}</mrow>`,frac=(a,b)=>`<mfrac>${a}${b}</mfrac>`,pow=(a,b)=>`<msup>${a}${b}</msup>`,sub=(a,b)=>`<msub>${a}${b}</msub>`,sum=(lo,hi,body)=>row(`<munderover><mo largeop="true" movablelimits="false">∑</mo>${lo}${hi}</munderover>`,body),eq=o('='),minus=o('−'),plus=o('+'),inf=o('∞'),np=pow(i('n'),i('p')),ratio=frac(row(i('x'),minus,i('c')),i('R'));
    const sums=[frac(n(1),pow(i('n'),n(2))),frac(i('n'),row(i('n'),plus,n(1))),frac(pow(n(2),i('n')),row(i('n'),o('!'))),frac(pow(row(o('('),minus,n(1),o(')')),row(i('n'),minus,n(1))),i('n')),frac(n(1),row(pow(i('n'),n(2)),plus,n(1))),pow(frac(n(3),n(4)),i('n'))];
    let body;
    if(section==='11.1')body=row(sub(i('a'),i('n')),eq,m.sequence==='oscillating'?pow(row(o('('),minus,n(1),o(')')),i('n')):frac(m.sequence==='alternating'?pow(row(o('('),minus,n(1),o(')')),i('n')):n(1),np));
    else if(section==='11.2')body=row(sub(i('S'),i('N')),eq,sum(row(i('k'),eq,n(0)),row(i('N'),minus,n(1)),pow(i('r'),i('k'))));
    else if(section==='11.3')body=row(sum(row(i('n'),eq,n(1)),inf,frac(n(1),np)));
    else if(section==='11.4')body=row(n(0),o('<'),frac(n(1),row(np,plus,n(1))),o('≤'),frac(n(1),np));
    else if(section==='11.5')body=row(sub(i('S'),i('N')),eq,sum(row(i('n'),eq,n(1)),i('N'),frac(pow(row(o('('),minus,n(1),o(')')),row(i('n'),minus,n(1))),np)));
    else if(section==='11.6')body=sum(row(i('n'),eq,n(1)),inf,m.family==='power'?frac(n(1),np):frac(pow(row(o('|'),i('r'),o('|')),i('n')),m.family==='factorial'?row(i('n'),o('!')):n(1)));
    else if(section==='11.7')body=sum(row(i('n'),eq,n(1)),inf,sums[m.case]);
    else if(section==='11.8')body=sum(row(i('n'),eq,n(1)),inf,frac(pow(row(o('('),ratio,o(')')),i('n')),i('n')));
    else if(section==='11.9')body=m.operation==='sum'?row(sum(row(i('n'),eq,n(0)),inf,pow(i('x'),i('n'))),eq,frac(n(1),row(n(1),minus,i('x')))):m.operation==='derivative'?row(sum(row(i('n'),eq,n(1)),inf,row(i('n'),pow(i('x'),row(i('n'),minus,n(1))))),eq,frac(n(1),pow(row(o('('),n(1),minus,i('x'),o(')')),n(2)))):row(sum(row(i('n'),eq,n(0)),inf,frac(pow(i('x'),row(i('n'),plus,n(1))),row(i('n'),plus,n(1)))),eq,minus,i('ln'),o('('),n(1),minus,i('x'),o(')'));
    else body=row(sub(i('P'),i('N')),o('('),i('x'),o(')'),eq,sum(row(i('k'),eq,n(0)),i('N'),frac(row(pow(i('f'),row(o('('),i('k'),o(')'))),o('('),i('c'),o(')'),pow(row(o('('),i('x'),minus,i('c'),o(')')),i('k'))),row(i('k'),o('!')))));
    return`<math xmlns="http://www.w3.org/1998/Math/MathML" display="block" aria-label="${esc(m.formula)}">${body}</math>`;
  }
  function teaching(section,s){const m=describe(section,s),step=m.steps[m.stage];return`<span class="cs-eyebrow">WHY IT WORKS · ${m.stage+1} / 4</span><h4>${esc(step[0])}</h4><p>${esc(step[1])}</p><div class="cs-formula">${equation(section,s)}</div>`;}
  function questionHTML(section,s){const q=target(section,s);return`<p class="cs-question">${esc(q.prompt)}</p>${q.options?`<fieldset class="cs-options"><legend class="sr-only">Choose one answer</legend>${q.options.map((label,j)=>`<label><input type="radio" name="cs-prediction" data-cs-answer value="${j}"><span>${esc(label)}</span></label>`).join('')}</fieldset>`:'<label class="cs-control">Your prediction<input type="number" step="any" inputmode="decimal" data-cs-answer aria-label="Your numerical prediction"></label>'}`;}
  function html({q,section=q?.section||'11.1'}={}){
    const s=defaults(section),t=meta(section);return`<section class="calculus-series-lab" data-calc-series-lab data-cs-section="${section}"><header class="cs-heading"><div><span class="cs-eyebrow">THE INFINITY LAB · SECTION ${section}</span><h3>${t[2]}</h3><p>${t[3]}</p></div><span class="cs-chapter-mark" aria-hidden="true">∞</span></header><nav class="cs-topic-nav" aria-label="Sequences and series labs">${topics.map(row=>`<a href="#labs/calculus/11/${row[0]}" ${section===row[0]?'aria-current="page"':''}><span>${row[0]}</span>${row[1]}</a>`).join('')}</nav><div class="cs-workspace"><div class="cs-visual"><div class="cs-visual-heading"><span class="cs-eyebrow">EXPLORE THE IDEA</span><span class="cs-live-badge">Live exploration</span></div><div class="cs-legend" data-cs-legend></div><div data-cs-scene tabindex="0" role="region" aria-label="Interactive graph; scroll horizontally to read the full fixed-scale diagram"></div><div class="cs-construction-progress"><span data-cs-count></span><div class="cs-progress-track" aria-hidden="true"><i data-cs-progress></i></div></div><p class="cs-caption" data-cs-caption></p><div class="cs-stats" data-cs-stats></div><div class="cs-verdict" data-cs-verdict></div></div><aside class="cs-dashboard"><div><span class="cs-eyebrow">YOUR EXPERIMENT</span><div data-cs-controls>${controlHTML(section,s)}</div></div><label class="cs-speed-label">Playback pace<select data-cs-speed aria-label="Playback pace"><option value="0.5">Unhurried · ½×</option><option value="1" selected>Steady · 1×</option><option value="2">Quick · 2×</option></select></label><div class="cs-transport"><button type="button" data-cs-action="play" aria-pressed="false">Run construction</button><button type="button" data-cs-action="step">+1 term</button><button type="button" data-cs-action="reset">Reset</button></div><p class="cs-status" data-cs-status role="status">Ready. Change an input or build one term at a time.</p><p class="cs-mini-note">Playback adds terms or degrees. Brief transitions guide your eye between exact settings; the readouts describe the selected settings. Hover or focus the latest point for its value.</p></aside></div><div class="cs-lower"><article class="cs-teaching"><div class="cs-stage-dots" aria-label="Explanation stages">${[0,1,2,3].map(n=>`<button type="button" data-cs-stage="${n}" aria-label="Explanation ${n+1}" aria-pressed="${n===0}">${n+1}</button>`).join('')}</div><div data-cs-teaching></div><div class="cs-reasoning-nav"><button type="button" data-cs-action="back">← Previous</button><button type="button" data-cs-action="next">Next idea →</button></div></article><section class="cs-practice"><span class="cs-eyebrow">TRY THE IDEA</span><h4>Make a prediction.</h4><div data-cs-question>${questionHTML(section,s)}</div><div class="cs-practice-actions"><button type="button" data-cs-action="check">Check prediction</button><button type="button" data-cs-action="solution">Show reasoning</button></div><p data-cs-feedback role="status"></p><div class="cs-solution" data-cs-solution hidden></div></section></div><footer class="cs-sources"><p>Original Glasshouse exploration for the Chapter 11 section topic. These models teach concepts; they are separate from worked textbook exercise solutions.</p><a href="https://openstax.org/books/calculus-volume-2/pages/${t[4]}" target="_blank" rel="noopener noreferrer">Read the related OpenStax explanation ↗</a>${q?.source?.localPage?`<a href="books/calculus/chapter-11.pdf#page=${q.source.localPage}" target="_blank" rel="noopener">Open your section reading ↗</a>`:''}</footer></section>`;
  }
  const legend=section=>({
    '11.1':[['coral','Sequence terms'],['aqua','Tolerance band']],
    '11.2':[['coral','Individual terms'],['aqua','Running totals'],['dash','Infinite sum, when it exists']],
    '11.3':[['aqua','Decreasing function'],['coral','Omitted tail rectangles']],
    '11.4':[['coral','Your series'],['aqua','Benchmark series']],
    '11.5':[['coral','Partial sums'],['aqua','Guaranteed sum bracket']],
    '11.6':[['coral','Finite test values'],['threshold','Threshold = 1']],
    '11.7':[['neutral','Inspect the terms → choose a test → justify the conclusion']],
    '11.8':[['aqua','Convergence interval'],['coral','Your x and partial sums']],
    '11.9':[['aqua','Exact function'],['coral','Finite polynomial'],['fill','Separation between curves']],
    '11.10':[['aqua','Exact function'],['coral','Taylor polynomial'],['fill','Separation between curves']],
    '11.11':[['coral','Guaranteed error bound'],['dash','Required tolerance']]
  })[section].map(([color,label])=>`<span><i class="cs-key-${color}" aria-hidden="true"></i>${label}</span>`).join('');
  let active=null;
  function settle(a,snap=true){if(a.visualFrame!==null)cancelAnimationFrame(a.visualFrame);a.visualFrame=null;for(const item of a.tweens||[]){if(snap)item.node.setAttribute(item.key,item.to);if(item.remove&&snap)item.node.removeAttribute(item.key);item.node.removeAttribute('data-cs-end-'+item.key);}a.tweens=[];}
  function stop(a){a.running=false;a.last=null;if(a.frame!==null)cancelAnimationFrame(a.frame);a.frame=null;}
  function unmount(){if(!active)return;const a=active;stop(a);settle(a);if(a.pendingPaint!==null)cancelAnimationFrame(a.pendingPaint);for(const e of['input','change','click','keydown'])a.root.removeEventListener(e,a[e]);a.media?.removeEventListener?.('change',a.motion);active=null;}
  const attributes=node=>Object.fromEntries(node.attributes?Array.from(node.attributes,a=>[a.name,a.value]):Object.entries(node.a||{}));
  const numbers=s=>(String(s).match(/[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/gi)||[]).map(Number);
  function morphValue(key,from,to){
    if(key==='d'){const skeleton=s=>s.replace(/[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/gi,'#');if(skeleton(from)!==skeleton(to))return null;const aa=numbers(from),bb=numbers(to);if(!aa.length||aa.length!==bb.length||!aa.every(Number.isFinite)||!bb.every(Number.isFinite))return null;return t=>{let j=0;return to.replace(/[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/gi,()=>{const v=aa[j]+(bb[j]-aa[j])*t;j++;return Number(v.toFixed(5)).toString();});};}
    if(!/^(cx|cy|x|y|x1|y1|x2|y2|width|height|r|opacity)$/.test(key)||!Number.isFinite(Number(from))||!Number.isFinite(Number(to)))return null;return t=>String(Number(from)+(Number(to)-Number(from))*t);
  }
  // Keep real SVG objects, axes, focus and scroll position alive between frames.
  function patchChildren(parent,incoming,a,animate=false){
    const keys=nodes=>{const counts={};return nodes.map(node=>{const base=node.getAttribute('data-cs-key')||node.getAttribute('data-cs-control-key')||[node.tagName,node.getAttribute('class')||'',node.getAttribute('clip-path')||'',node.getAttribute('id')||''].join(':');const count=counts[base]||0;counts[base]=count+1;return[base+':'+count,node];});};
    const wanted=keys(Array.from(incoming.children)),old=new Map(keys(Array.from(parent.children))),used=new Set();
    for(let index=0;index<wanted.length;index++){
      const[key,next]=wanted[index];let node=old.get(key),fresh=!node||node.tagName!==next.tagName;if(fresh)node=next;used.add(node);
      if(parent.children[index]!==node){if(parent.insertBefore)parent.insertBefore(node,parent.children[index]||null);else{node.remove();parent.appendChild(node);}}
      if(fresh){if(animate&&node.tagName.toLowerCase()==='circle'&&node.hasAttribute('data-cs-key')){const radius=node.getAttribute('r');a.tweens.push({node,key:'r',from:String(Number(radius)*.65),to:radius,value:morphValue('r',String(Number(radius)*.65),radius)},{node,key:'opacity',from:'0',to:'1',value:t=>String(t),remove:true});}continue;}
      const prior=attributes(node),nextAttrs=attributes(next),moving=animate&&/\bcs-(?:dot|aqua-dot|open-dot|last|gap|function|polynomial|error-fill|marker|probe|interval|band|rect|tail-rect|stem|bracket)/.test(next.getAttribute('class')||'');
      for(const name of Object.keys(prior))if(!Object.hasOwn(nextAttrs,name)&&!name.startsWith('data-cs-end-'))node.removeAttribute(name);
      for(const[name,to]of Object.entries(nextAttrs)){const from=prior[name];if(from===to)continue;node.setAttribute(name,to);const value=moving&&from!==undefined?morphValue(name,from,to):null;if(value)a.tweens.push({node,key:name,from,to,value});}
      if(next.children.length)patchChildren(node,next,a,animate);else if(node.textContent!==next.textContent)node.textContent=next.textContent;
    }
    for(const node of Array.from(parent.children))if(!used.has(node))node.remove();
  }
  function syncHTML(parent,markup,a,animate=false){const scratch=document.createElement('div');scratch.innerHTML=markup;patchChildren(parent,scratch,a,animate);}
  function startTween(a){
    if(!a.tweens.length)return;const duration=a.running?Math.min(320,400/a.speed):200;a.visualStart=null;
    for(const item of a.tweens){item.node.setAttribute('data-cs-end-'+item.key,item.to);item.node.setAttribute(item.key,item.from);}
    function draw(now){if(active!==a)return;if(a.visualStart===null)a.visualStart=now;const t=clamp((now-a.visualStart)/duration,0,1),ease=1-(1-t)**3;for(const item of a.tweens)item.node.setAttribute(item.key,t===1?item.to:item.value(ease));a.motionFrames++;if(t===1){settle(a);return;}a.visualFrame=requestAnimationFrame(draw);}
    a.visualFrame=requestAnimationFrame(draw);
  }
  function mount(container){
    unmount();const root=container.matches?.('[data-calc-series-lab]')?container:container.querySelector('[data-calc-series-lab]');if(!root)return false;const section=root.getAttribute('data-cs-section'),a={root,section,s:defaults(section),running:false,frame:null,visualFrame:null,pendingPaint:null,tweens:[],last:null,revealed:false,speed:1,graphKey:null,paintCount:0,motionFrames:0,media:typeof matchMedia==='function'?matchMedia('(prefers-reduced-motion: reduce)'):null};active=a;
    const find=sel=>root.querySelector(sel),status=msg=>{find('[data-cs-status]').textContent=msg;};
    function invalidate(){a.revealed=false;a.questionDirty=true;find('[data-cs-feedback]').textContent='';find('[data-cs-feedback]').removeAttribute('data-correct');find('[data-cs-solution]').hidden=true;for(const node of root.querySelectorAll('[data-cs-answer]')){node.checked=false;if(node.type!=='radio')node.value='';}}
    function paint(animate=true){if(active!==a)return;a.paintCount++;if(a.questionDirty){find('[data-cs-question]').innerHTML=questionHTML(section,a.s);a.questionDirty=false;}const m=describe(section,a.s),q=target(section,a.s),key=JSON.stringify({...a.s,stage:0}),changed=key!==a.graphKey;
      if(changed){const scene=svg(section,a.s);settle(a,false);const shouldAnimate=animate&&a.graphKey!==null&&!a.media?.matches;syncHTML(find('[data-cs-scene]'),scene.markup,a,shouldAnimate);find('[data-cs-caption]').textContent=scene.caption;syncHTML(find('[data-cs-stats]'),m.stats.map(([label,v])=>`<div data-cs-key="stat-${esc(label)}"><span>${esc(label)}</span><strong>${esc(v)}</strong></div>`).join(''),a);find('[data-cs-verdict]').textContent=m.conclusion;a.graphKey=key;startTween(a);}
      const explanation=teaching(section,a.s);if(a.explanation!==explanation){find('[data-cs-teaching]').innerHTML=explanation;a.explanation=explanation;}
      for(const node of root.querySelectorAll('[data-cs-param]')){const key=node.getAttribute('data-cs-param');node.value=String(a.s[key]);const output=find(`[data-cs-output="${key}"]`);if(output)output.textContent=fmt(a.s[key]);}
      for(const node of root.querySelectorAll('[data-cs-stage]'))node.setAttribute('aria-pressed',String(Number(node.getAttribute('data-cs-stage'))===a.s.stage));find('[data-cs-action="back"]').disabled=a.s.stage===0;find('[data-cs-action="next"]').disabled=a.s.stage===3;
      const play=find('[data-cs-action="play"]'),step=find('[data-cs-action="step"]');play.textContent=a.running?'Pause':'Run construction';play.setAttribute('aria-pressed',String(a.running));play.hidden=section==='11.7';step.hidden=section==='11.7';step.textContent=['11.10','11.11'].includes(section)?'+1 degree':'+1 term';
      if(find('[data-cs-progress]')){const max=['11.10','11.11'].includes(section)?14:section==='11.9'?30:60;find('[data-cs-progress]').style.width=(a.s.N/max*100)+'%';find('[data-cs-count]').textContent=section==='11.7'?'Choose a test':`${['11.10','11.11'].includes(section)?'Degree':'Terms'} ${a.s.N} / ${max}`;find('[data-cs-speed]').value=String(a.speed);}
      const sol=find('[data-cs-solution]');sol.hidden=!a.revealed;if(a.revealed)sol.innerHTML=`<p>${esc(q.reason)}</p><p><b>${q.options?'Answer':'Value'}:</b> ${esc(q.options?q.options[q.answer]:fmt(q.answer))}</p>`;
    }
    function flush(){if(a.pendingPaint!==null)cancelAnimationFrame(a.pendingPaint);a.pendingPaint=null;paint();}
    function schedule(){if(a.pendingPaint===null)a.pendingPaint=requestAnimationFrame(()=>{a.pendingPaint=null;paint();});}
    function pause(){stop(a);if(a.pendingPaint!==null)flush();settle(a);}
    function advance(){const max=['11.10','11.11'].includes(section)?14:section==='11.9'?30:60;a.s.N=a.s.N>=max?(['11.10','11.11'].includes(section)?0:1):a.s.N+1;invalidate();}
    function tick(now){if(active!==a||!a.running)return;if(a.last===null)a.last=now;if(now-a.last>=500/a.speed){advance();a.last=now;const max=['11.10','11.11'].includes(section)?14:section==='11.9'?30:60;if(a.s.N>=max){stop(a);status('Construction complete. Inspect the conclusion and error bounds.');}paint();}if(a.running)a.frame=requestAnimationFrame(tick);}
    a.input=e=>{if(e.target.hasAttribute?.('data-cs-speed')){a.speed=clamp(Number(e.target.value)||1,.5,2);a.last=null;paint(false);return;}const key=e.target.getAttribute?.('data-cs-param');if(!key)return;stop(a);const old=a.s[key];a.s=normalise(section,{...a.s,[key]:e.target.value});if(old===a.s[key])return;if(['sequence','family'].includes(key))syncHTML(find('[data-cs-controls]'),controlHTML(section,a.s),a);invalidate();status('Input changed. Inspect the construction and make a fresh prediction.');if(e.target.type==='range')schedule();else flush();};a.change=a.input;
    a.click=e=>{const stage=e.target.closest?.('[data-cs-stage]');if(stage&&root.contains(stage)){a.s.stage=Number(stage.getAttribute('data-cs-stage'));paint();return;}const button=e.target.closest?.('[data-cs-action]');if(!button||!root.contains(button))return;const action=button.getAttribute('data-cs-action');
      if(a.pendingPaint!==null)flush();
      if(action==='play'){if(a.running){pause();status('Paused for inspection.');}else if(a.media?.matches){advance();status('Reduced motion: advanced one still construction.');}else{const max=['11.10','11.11'].includes(section)?14:section==='11.9'?30:60;if(a.s.N>=max)a.s.N=['11.10','11.11'].includes(section)?0:1;a.running=true;a.last=null;invalidate();status('Building the finite construction. The explanation steps stay separate.');a.frame=requestAnimationFrame(tick);}paint();return;}
      if(action==='reset'){pause();a.s=defaults(section);a.speed=1;syncHTML(find('[data-cs-controls]'),controlHTML(section,a.s),a);invalidate();status('Reset to the starting example.');paint(false);return;}
      if(action==='step'){pause();advance();status('Advanced one finite construction step.');}
      if(action==='back'||action==='next')a.s.stage=clamp(a.s.stage+(action==='next'?1:-1),0,3);
      if(action==='check'){pause();const q=target(section,a.s),input=find(q.options?'[data-cs-answer]:checked':'[data-cs-answer]'),r=grade(section,a.s,input?.value??'');find('[data-cs-feedback]').textContent=r.message;find('[data-cs-feedback]').setAttribute('data-correct',String(r.correct));}
      if(action==='solution'){pause();a.revealed=!a.revealed;}paint();
    };
    a.keydown=e=>{if(e.key==='Enter'&&e.target.hasAttribute?.('data-cs-answer')){e.preventDefault();find('[data-cs-action="check"]').click();}};
    a.motion=()=>{if(a.media?.matches){pause();status('Animation paused for reduced motion. Use +1 to inspect still constructions.');paint(false);}};a.media?.addEventListener?.('change',a.motion);for(const e of['input','change','click','keydown'])root.addEventListener(e,a[e]);if(find('[data-cs-legend]'))find('[data-cs-legend]').innerHTML=legend(section);paint(false);return true;
  }
  return{applies:(q,example='base')=>q.subject==='calculus'&&topics.some(t=>t[0]===q.section)&&example==='base',html,mount,unmount,normalise,describe,svg,target,grade,topics,controls,taylor,bound,equation,state:()=>active?{...active.s,running:active.running,revealed:active.revealed,speed:active.speed,pendingPaint:active.pendingPaint!==null,activeTransitions:active.tweens.length,paintCount:active.paintCount,motionFrames:active.motionFrames}:null};
})();
