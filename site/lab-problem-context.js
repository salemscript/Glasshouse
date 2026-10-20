/* Keep the exact linked exercise visible while exploring its chapter model. */
'use strict';
window.LabProblemContext=(()=>{
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const route=/^(calculus|physics|organic|chemistry|statics|dynamics)\/problems\/([a-zA-Z0-9.-]+)$/,sourceFile=/^practice\/(?:calculus|physics|chemistry|organic|organic-body)\/\d+\.svg\.gz$/;
 const urls=new Set();let generation=0;
 const revoke=url=>{URL.revokeObjectURL(url);urls.delete(url)};
 function unmount(){generation++;for(const url of urls)URL.revokeObjectURL(url);urls.clear()}
 function html(back){return route.test(String(back))?'<section id="lab-problem-context" class="lab-problem-context" aria-label="Your linked textbook problem"><p>Loading your problem’s full context…</p></section>':''}
 const substantive=s=>typeof s==='string'?s.trim():['equation','substitution','calculation','why','explanation'].some(k=>String(s?.[k]||'').trim());
 function worked(q){
  const normalize=s=>typeof s==='string'?{explanation:s}:s;
  const a=q.answerAudit,parts=(a?.parts||[]).map(p=>({...p,steps:(p.steps||[]).filter(substantive).map(normalize)})),steps=(a?.steps||[]).filter(substantive).map(normalize);
  const audit=window.AnswerLibrary?.workedHTML({answerAudit:a,auditParts:parts,auditSteps:steps})||'';if(audit)return audit;
  return (q.learningSolutions||[]).filter(s=>s.verified&&s.guidedSteps?.length).map(s=>{const rows=(s.workedSteps?.length?s.workedSteps:s.guidedSteps).filter(substantive).map(step=>typeof step==='string'?{explanation:step}:step);return rows.length?`<section class="answer-worked-part">${s.title?`<h4>${esc(s.title)}</h4>`:''}${s.scope?`<p class="plain-note">${esc(s.scope)}</p>`:''}${AnswerLibrary.stepsHTML(rows)}</section>`:''}).join('');
 }
 async function mount(back){
  unmount();const target=document.querySelector('#lab-problem-context'),token=generation,created=[];
  if(!target)return;const m=String(back).match(route);if(!m){target.innerHTML='<p>This lab has no valid linked textbook problem.</p>';return}
  const current=()=>token===generation&&target.isConnected&&document.querySelector('#lab-problem-context')===target;
  try{
   const data=await TextbookPractice.context(m[1],m[2]);if(!current())return;if(!data)throw Error('Linked problem was not found');
   const q=data.question,written=ProblemContent.html(q),fields=window.ResponseParts?.fields(q)||[],units=[...new Set(fields.map(f=>f.rule?.unit).filter(Boolean))],work=worked(q);
   target.innerHTML=`<details open><summary>Your textbook problem · ${esc(q.number)}</summary><div class="lab-linked-statement">${written||'<p>The original statement, shared directions, and diagrams are shown below.</p>'}</div>${units.length?`<p class="lab-context-units"><b>Requested answer units:</b> ${esc(units.join(' · '))}</p>`:''}${q.reviewNotice?`<p class="plain-note">${esc(q.reviewNotice)}</p>`:''}<details class="lab-context-original" ${written?'':'open'}><summary>Original statement, shared instructions & diagrams</summary><div data-lab-context-art><p>Loading source diagrams…</p></div></details>${work?`<details class="lab-context-work${q.chapterStudyVerified?' chapter-study-work':''}"><summary>Worked reasoning for this exercise</summary>${work}</details>`:''}<p class="lab-context-scope">The model below explores this section’s principles. Its adjustable teaching examples can use different values and assumptions; they do not establish that every condition of this textbook exercise has been simulated.</p></details>`;
   target.setAttribute('data-question-id',q.id);
   target.querySelector('.lab-context-work')?.addEventListener('toggle',event=>{if(!current()||!event.target.open)return;try{const key=`calx-question-v1-${m[1]}-${q.id}`,saved=JSON.parse(localStorage.getItem(key)||'{}');saved.assisted=true;localStorage.setItem(key,JSON.stringify(saved))}catch{}});
   const art=target.querySelector('[data-lab-context-art]');if(!Array.isArray(data.parts)||!data.parts.length){art.innerHTML='<p>The complete written statement is above; this exercise has no additional source artwork.</p>';return}
   const fragments=[];let unavailable=false;
   for(const item of data.parts){
    const part=item&&typeof item==='object'?item:{};
    const crops=(Array.isArray(part.crops)?part.crops:[]).filter(c=>Array.isArray(c)&&c.length===4&&c.every(Number.isFinite)&&c[0]>=0&&c[1]>=0&&c[2]>0&&c[3]>0);
    if(!sourceFile.test(part.file)||!crops.length){unavailable=true;continue}
    let source;try{source=await TextbookPractice.sourceSVG(part.file)}catch{if(!current()){for(const url of created)revoke(url);return}unavailable=true;continue}if(!current()){for(const url of created)revoke(url);return}
    if(!/<svg\b[^>]*>/i.test(source)){unavailable=true;continue}
    for(const crop of crops){
     const svg=source.replace(/<svg\b[^>]*>/i,`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${crop[2]}" height="${crop[3]}" viewBox="${crop.join(' ')}">`);
     const url=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml'}));urls.add(url);created.push(url);
     const label=['instructions','context'].includes(part.role)?'Shared exercise instructions and context':part.role==='reference'?`Context from exercise ${part.contextLabel||''}`:part.role==='figure'?`Source figure for exercise ${q.number}`:`Textbook exercise ${q.number}`;
     fragments.push(`<figure><img src="${esc(url)}" alt="${esc(label)}" loading="lazy"><figcaption>${esc(label)}</figcaption></figure>`);
    }
   }
   if(current())art.innerHTML=fragments.join('')+(unavailable?'<p class="plain-note">Some source artwork could not load. The written statement and any available source portions remain above.</p>':'');else for(const url of created)revoke(url);
  }catch{for(const url of created)revoke(url);if(current())target.innerHTML=`<p>Your linked problem could not load. <a href="#${esc(back)}">Return to the original problem</a> and retry its lab link.</p>`}
 }
 return{html,mount,unmount};
})();
