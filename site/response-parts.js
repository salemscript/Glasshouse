'use strict';
window.ResponseParts=(()=>{
 // These are response slots, not a reconstruction of the textbook's equations.
 // Numeric keys always refer to the original position in q.grader.parts.
 const generic=/^(?:answer|your answer|listed parts|this exercise|response)$/i;
 const referenceEnd=/\b(?:parts?|panels?|conditions?|theorems?|equations?|examples?)\s*$/i;
 const referenceJoin=/^\s*(?:(?:and|or|to|through|of|in)\s*|[,;–—-]\s*|parts?\s*)*$/i;
 const taskStart=/^(?:find|calculate|what|how|determine|draw|sketch|show|prove|explain|evaluate|write|use|estimate|compute|give|identify|predict|does|do|is|are|can|in|at|if|when|where|for|suppose|would|change|convert|state|test|apply|compare|derive|which|solve|rank|verify|decide|obtain|construct|express|describe|indicate|label|name|assign|complete|fill)\b/i;
 const text=s=>String(s??'').trim();
 function partLabel(value){
  const s=text(value);let m;
  if((m=s.match(/^(?:part\s+)?\(?([a-z])\)?$/i)))return m[1].toLowerCase();
  if((m=s.match(/^(?:part\s+)?\(?([a-z])\)?(?=\s*[·:–—.-]|\s*\((?:[ivx]+|\d+)\))(?:\s|[·:–—.-]|\()/i)))return m[1].toLowerCase();
  if((m=s.match(/\b(?:part|subpart)\b\s*\(?([a-z])\)?(?:\s|$|[·:–—.-]|\()/i)))return m[1].toLowerCase();
  // A source identifier such as "Chapter 1 · Problem 1(a)" is explicit.
  if((m=s.match(/\b(?:problem|exercise|question)\s+[\d.\-]+\s*\(([a-z])\)(?:\s*\([ivx\d]+\))?\s*$/i)))return m[1].toLowerCase();
  return null;
 }
 function captionless(s){return s.split(/\b(?:Figure|FIGURE|Question|Problem)\s+\d+[–-]\d+\b/)[0]}
 function selectionOnly(prompt){return /\bwhich of the following\b[\s\S]*\b(?:least|fewest|greatest|largest|smallest|most|best|represents?|has|contains?)\b/i.test(String(prompt||''))&&!/\b(?:for each|each of the|determine each|calculate each)\b/i.test(String(prompt||''))}
 function promptParts(prompt){
  const p=String(prompt??'').replace(/[\u00a0\u2002\u2003\u2009]/g,' '),matches=[];
  const re=/(?<![\p{L}\p{N}_])\(\s*([a-z])\s*\)/giu;let m;
  while((m=re.exec(p))){
   // R/S and E/Z before a compound name specify chemistry, not a subquestion.
   if(/[RSEZ]/.test(m[1])&&/^\s*[–-]/.test(p.slice(re.lastIndex)))continue;
   const before=p.slice(Math.max(0,m.index-100),m.index),previous=matches.at(-1);
   // Native MathML transcriptions use parentheses around fraction terms. A
   // variable after =, /, * or ^ is part of an equation, not a lettered task.
   if(/[=/*^]\s*$/.test(before))continue;
   // Readable reflows may separate a function symbol and its argument: K (t).
   // The following punctuation/graph noun distinguishes it from a real task.
   if(/\b(?:F|K|P|W|U)\s*$/.test(before)&&/^[txr]$/.test(m[1])&&/^\s*(?:[=+−*/^:;,.)-]|(?:plot|curve|graph|versus)\b)/i.test(p.slice(re.lastIndex)))continue;
   if(/\bdensity\s*$/i.test(before)&&m[1].toLowerCase()==='d'||/\bvolume\s*$/i.test(before)&&m[1].toLowerCase()==='v')continue;
   if(/\b(?:radius|length|distance|position|time|force|energy|mass|height|depth|temperature|frequency|power|current|voltage|reading|x|y|z|t|Q|F|K|P|V|xbg|xbs)\s*$/i.test(before)&&/[msNJKAWV]/.test(m[1]))continue;
   if(/\b(?:f|g|h|x|y|v)\s*$/i.test(before)&&/^\s*[=+−*/^]/.test(p.slice(re.lastIndex)))continue;
   if(m[1]==='i'&&/^\s*[\s\S]{0,120}?\(\s*ii\s*\)/.test(p.slice(re.lastIndex)))continue;
   const range=previous&&/^\s*[–—-]\s*$/.test(p.slice(previous.end,m.index));
   if(range)previous.reference=true;
   const reference=Boolean(range)||referenceEnd.test(before)||(previous?.reference&&referenceJoin.test(p.slice(previous.end,m.index)));
   matches.push({part:m[1].toLowerCase(),start:m.index,end:re.lastIndex,reference});
  }
  const eligible=matches.filter(v=>!v.reference),letters=new Set(eligible.map(v=>v.part));
  const first=eligible[0],head=first?p.slice(0,first.start):'';
  const eachExplicit=/\b(?:each|both\s+sets?|following\s+(?:compounds?|structures?|molecules?|reactions?|expressions?|functions?|formulas?|vectors?|coordinates?|pairs?|elements?|equations?|representations?|names?|transformations?))\b/i.test(head);
  const each=eachExplicit||(letters.has('a')&&letters.has('b')&&/\b(?:calculate|find|draw|write|state|show|sketch|evaluate|simplify|factor|solve|express|convert|change|verify|what|how|determine|give|identify|predict|compare)\b/i.test(head));
  const rankPanels=/\brank\b[\s\S]*\b(?:situations?|plots?|slides?|graphs?)\b/i.test(head)&&!/\bboth\s+sets?\b/i.test(head);
  const choosePanels=selectionOnly(head)||/\b(?:one of|which of|which)\b[\s\S]*\b(?:graphs?|plots?|structures?|molecules?)\b[\s\S]*\b(?:is it|could|possibly|is the|represents?)\b/i.test(head)||/\bone of the following\b[\s\S]*\b(?:which|identify|select|choose)\b/i.test(p);
  const figureTail=first&&p.lastIndexOf('?')>=0&&first.start>p.lastIndexOf('?')&&/\b(?:Figure|FIGURE)\s+\d+[.–-]\d+\b/.test(p)&&!eachExplicit;
  const parts=new Set();
  for(const v of eligible){
   const next=matches.find(w=>w.start>v.start),body=captionless(p.slice(v.end,next?.start??p.length)).trim();
   const firstWord=body.match(/^[A-Za-z]+/)?.[0]||'';
   const words=body.match(/[A-Za-z]{3,}/g)||[];
   const contentWords=words.filter(w=>!/^(?:figure|question|problem|exercises|module|chapter|section|www|http)$/i.test(w));
   // A sentence after a label is a task, even when nearby figure panels repeat it.
   const task=taskStart.test(body);
   // Inline parts may name a quantity: "density of (a) the wood and (b) the oil".
   const phrase=contentWords.length>0&&!/^(?:Figure|Question|Problem|Module)\b/.test(firstWord);
   // A list of mathematical expressions can be short and contain no prose.
   const expression=letters.size>1&&each&&/[\p{L}\p{N}]/u.test(body);
   const illustrated=letters.size>1&&each;
   if(!figureTail&&(task||(!rankPanels&&!choosePanels&&(phrase||expression||illustrated)))&&(letters.size>1||/[abc]/.test(v.part)||task))parts.add(v.part);
  }
  return [...parts].sort();
 }
 function displayLabel(rule,part,multipart,index,count){
  const raw=text(rule?.label);
  if(part){
   const suffix=raw.replace(/^(?:part\s+)?\(?[a-z]\)?\s*/i,'').trim();
   // Keep useful distinctions such as "carbon" or the selected (iii) portion.
   return 'Part '+part.toUpperCase()+(partLabel(raw)===part&&suffix?(/^[·:–—.-]/.test(suffix)?' '+suffix:' · '+suffix):'');
  }
  if(raw&&!generic.test(raw))return (multipart?'Checked answer · ':'')+raw;
  if(multipart)return 'Checked answer'+(count>1?' '+(index+1):'');
  return count>1?'Answer '+(index+1):'Your answer';
 }
 function fields(q={}){
  const rules=q.grader?.type==='parts'?(q.grader.parts||[]):q.grader?[q.grader]:[];
  const parts=new Set(promptParts(q.responsePartPrompt??q.prompt));
  const solutions=(q.learningSolutions||[]).filter(s=>s.verified);
  const solutionParts=new Map();
  for(const solution of solutions){
   const part=partLabel(solution.partLabel)||partLabel(solution.label);
   if(part)parts.add(part);
   for(const final of solution.finalRules||[]){
    const index=Number(final.fieldIndex),label=partLabel(final.label)||part;
    if(Number.isInteger(index)&&index>=0&&index<rules.length&&label){
     const seen=solutionParts.get(index)||new Set();seen.add(label);solutionParts.set(index,seen);
    }
   }
  }
  const assigned=rules.map((rule,index)=>{
   const verified=solutionParts.get(index),part=partLabel(rule.label)||partLabel(rule.answerLabel)||partLabel(rule.selection)||(verified?.size===1?[...verified][0]:null);
   if(part)parts.add(part);
   return {rule,index,part};
  });
  const multipart=parts.size>0,records=[];
  for(const part of [...parts].sort()){
   const graded=assigned.filter(v=>v.part===part);
   if(graded.length)for(const {rule,index} of graded)records.push({fieldKey:String(index),graderIndex:index,rule,partLabel:part,label:displayLabel(rule,part,true,index,rules.length)});
   else records.push({fieldKey:'part-'+part,graderIndex:null,rule:null,partLabel:part,label:'Part '+part.toUpperCase()});
  }
  for(const {rule,index,part} of assigned)if(!part)records.push({fieldKey:String(index),graderIndex:index,rule,partLabel:null,label:displayLabel(rule,null,multipart,index,rules.length)});
  if(!records.length)records.push({fieldKey:'0',graderIndex:null,rule:null,partLabel:null,label:'Your answer'});
  return records;
 }
 return {fields,partLabel,promptParts,selectionOnly};
})();
