'use strict';
window.ExerciseFeedback=(()=>{
 const active=new WeakMap();
 function clear(input){
  const previous=active.get(input);active.delete(input);
  previous?.animation?.cancel();previous?.mark?.remove();
  previous?.bubble?.classList.remove('answer-confirmed','answer-celebrating');
  input.classList.remove('answer-error','answer-correct');
 }
 function answer(selector,success){
  const input=document.querySelector(selector);if(!input)return;clear(input);
  input.setAttribute('aria-invalid',String(!success));
  input.classList.toggle('answer-error',!success);input.classList.toggle('answer-correct',success);
  const bubble=input.closest?.('.input-wrap, .hint-blank')||input;
  const job={bubble,mark:null,animation:null};active.set(input,job);
  if(success){
   bubble.classList.add('answer-confirmed');
   if(bubble!==input&&document.createElement){
    const mark=document.createElement('span');mark.className='answer-success-mark';mark.textContent='✓';mark.setAttribute('aria-hidden','true');bubble.appendChild(mark);job.mark=mark;
   }
  }
  if(window.matchMedia?.('(prefers-reduced-motion: reduce)').matches)return;
  const target=success?bubble:input;if(!target.animate)return;
  if(success)bubble.classList.add('answer-celebrating');
  job.animation=target.animate(success?[
   {transform:'translateY(0) scale(1)',boxShadow:'0 0 0 0 rgba(56,151,96,0)',offset:0},
   {transform:'translateY(-3px) scale(1.035)',boxShadow:'0 0 0 7px rgba(56,151,96,.18)',offset:.3},
   {transform:'translateY(0) scale(.99)',boxShadow:'0 0 0 9px rgba(56,151,96,.08)',offset:.56},
   {transform:'translateY(-1px) scale(1.01)',boxShadow:'0 0 0 4px rgba(56,151,96,.12)',offset:.78},
   {transform:'translateY(0) scale(1)',boxShadow:'0 0 0 3px rgba(56,151,96,.1)',offset:1}
  ]:[0,-9,8,-6,4,-2,0].map(x=>({transform:`translateX(${x}px)`})),{duration:success?620:420,easing:success?'cubic-bezier(.22,1,.36,1)':'ease-out'});
  job.animation.onfinish=()=>{if(active.get(input)===job)bubble.classList.remove('answer-celebrating')};
 }
 function icon(success){return `<span class="feedback-icon" aria-hidden="true">${success?'✓':'↻'}</span>`}
 document.addEventListener('input',e=>{if(/^(?:answer|bank-answer|question-answer-\d+|hint-blank-\d+)$/.test(e.target.id)){clear(e.target);e.target.setAttribute('aria-invalid','false')}});
 return{answer,icon,reset:selector=>{const input=document.querySelector(selector);if(input){clear(input);input.setAttribute('aria-invalid','false')}}};
})();
