/* Explicit TeX only: existing prose and legacy mathematics keep their renderer. */
(function(root){
 'use strict';
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const cache=new Map();
 function hasMath(value){return /\\\(|\\\[/.test(String(value??''));}
 function render(value){
  const source=String(value??'');if(cache.has(source))return cache.get(source);
  let end=0,out='';
  for(const match of source.matchAll(/\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g)){
   out+=esc(source.slice(end,match.index));
   const display=match[2]!==undefined,raw=display?match[2]:match[1];
   // Tall fractions need explicit row gaps inside matrices, not only a larger font.
   const tex=raw.replace(/\\frac(?![A-Za-z])/g,'\\dfrac').replace(/\\\\(?!\[)/g,'\\\\[0.65em]');
   try{out+='<span class="linear-typeset">'+root.katex.renderToString(tex,{displayMode:display,throwOnError:true,trust:false,strict:'warn',macros:{'\\arraystretch':'1.35'},output:'htmlAndMathml'})+'</span>';}
   catch(error){out+='<span class="linear-math-fallback">'+esc(match[0])+'</span>';console.warn('Unable to typeset mathematics',error.message);}
   end=match.index+match[0].length;
  }
  out+=esc(source.slice(end));if(cache.size>=500)cache.delete(cache.keys().next().value);cache.set(source,out);return out;
 }
 root.LinearMath={hasMath,render};
})(typeof window!=='undefined'?window:globalThis);
