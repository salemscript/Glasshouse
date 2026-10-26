/* Keep connected textbook crops in a single coordinate system. Splitting a
   text line into independently scaled SVGs cuts glyphs at the seam. */
(()=>{'use strict';
let serial=0;
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function connected(a,b){
 const overlapX=Math.min(a[0]+a[2],b[0]+b[2])-Math.max(a[0],b[0]);
 const overlapY=Math.min(a[1]+a[3],b[1]+b[3])-Math.max(a[1],b[1]);
 return (overlapX>0&&overlapY>=-.02)||(overlapY>0&&overlapX>=-.02);
}
function groups(crops){
 const result=[];
 for(const crop of crops||[]){
  if(!Array.isArray(crop)||crop.length!==4||!crop.every(Number.isFinite)||crop[2]<=0||crop[3]<=0)continue;
  let group=[crop.slice()];
  for(let i=result.length-1;i>=0;i--)if(result[i].some(a=>group.some(b=>connected(a,b)))){group=[...result[i],...group];result.splice(i,1);}
  // A late crop can bridge multiple existing groups.
  let changed=true;while(changed){changed=false;for(let i=result.length-1;i>=0;i--)if(result[i].some(a=>group.some(b=>connected(a,b)))){group=[...result[i],...group];result.splice(i,1);changed=true;}}
  result.push(group);
 }
 return result;
}
function bounds(crops){const x=Math.min(...crops.map(c=>c[0])),y=Math.min(...crops.map(c=>c[1]));return [x,y,Math.max(...crops.map(c=>c[0]+c[2]))-x,Math.max(...crops.map(c=>c[1]+c[3]))-y];}
function render(source,crops,label){
 const sets=groups(crops);if(!sets.length)return '';
 const boxes=sets.map(bounds),wide=Math.max(...boxes.map(b=>b[2])),width=Math.min(wide*2,800);
 return `<div class="source-excerpt-stack" style="width:${width}px;max-width:100%">`+sets.map((set,i)=>{
  const box=boxes[i],id='source-excerpt-clip-'+(++serial);
  const clip=`<defs><clipPath id="${id}" clipPathUnits="userSpaceOnUse">${set.map(c=>`<rect x="${c[0]}" y="${c[1]}" width="${c[2]}" height="${c[3]}"/>`).join('')}</clipPath></defs>`;
  return source.replace(/<svg\b[^>]*>/,root=>root.replace(/\s(?:viewBox|style|aria-label)="[^"]*"/g,'').replace(/>$/,` viewBox="${box.join(' ')}" style="width:${100*box[2]/wide}%;min-width:0;max-width:100%;height:auto;display:block" aria-label="${escape(label)}">`)+clip+`<g clip-path="url(#${id})">`).replace(/<\/svg>\s*$/,'</g></svg>');
 }).join('')+'</div>';
}
window.SourceExcerpts={groups,bounds,render};
})();
