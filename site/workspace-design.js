/* Original Glasshouse UI. The preview is f(x)=x² on fixed axes, not a decorative curve. */
(()=>{'use strict';
 const main=document.getElementById('main');
 const number=n=>String(Number(n.toFixed(3)));
 function paintDemo(){
  const root=main.querySelector('.studio-demo');if(!root)return;
  const input=root.querySelector('[data-studio-h]'),h=Number(input.value),x=1,x2=x+h,X=x=>46+x*(400/3),Y=y=>255-y*32;
  let grid='';for(let k=0;k<=3;k++)grid+=`<path d="M${X(k)},34V255"/><text x="${X(k)}" y="276">${k}</text>`;for(let k=0;k<=6;k+=2)grid+=`<path d="M46,${Y(k)}H446"/><text x="26" y="${Y(k)+4}">${k}</text>`;
  const curve=Array.from({length:81},(_,i)=>{const t=2.6*i/80;return(i?'L':'M')+X(t)+','+Y(t*t);}).join('');
  const secant=t=>1+(2+h)*(t-1),tangent=t=>2*t-1;
  root.querySelector('[data-studio-plot]').innerHTML=`<svg viewBox="0 0 480 300" role="img" aria-label="For f(x)=x squared, a secant between x=1 and x=${number(x2)} has slope ${number(2+h)}. The tangent at x=1 has slope 2."><defs><clipPath id="studio-plot-clip"><rect x="46" y="30" width="400" height="225"/></clipPath></defs><g class="studio-plot-grid">${grid}</g><g clip-path="url(#studio-plot-clip)"><path d="${curve}" class="studio-function"/><path d="M${X(.5)},${Y(tangent(.5))}L${X(2.6)},${Y(tangent(2.6))}" class="studio-tangent"/><path d="M${X(.5)},${Y(secant(.5))}L${X(2.6)},${Y(secant(2.6))}" class="studio-secant"/><path d="M${X(1)},${Y(1)}H${X(x2)}V${Y(x2*x2)}" class="studio-difference"/><circle cx="${X(1)}" cy="${Y(1)}" r="5" class="studio-point"/><circle cx="${X(x2)}" cy="${Y(x2*x2)}" r="5" class="studio-point"/></g><text x="430" y="283" class="studio-axis-label">x</text><text x="50" y="20" class="studio-axis-label">f(x) = x²</text></svg><div class="studio-plot-legend"><span><i class="function-key"></i>Function</span><span><i class="secant-key"></i>Secant</span><span><i class="tangent-key"></i>Tangent</span></div>`;
  root.querySelector('[data-studio-h-output]').textContent=number(h);root.querySelector('[data-studio-secant]').textContent=number(2+h);
 }
 main.addEventListener('input',e=>{if(e.target.matches('[data-studio-h]'))paintDemo();});
 new MutationObserver(records=>{if(records.some(r=>Array.from(r.addedNodes).some(n=>n.nodeType===1&&(n.matches?.('.studio-hero')||n.querySelector?.('.studio-demo')))))paintDemo();}).observe(main,{childList:true});
 paintDemo();
})();
