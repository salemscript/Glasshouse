'use strict';
window.ConceptChoices=(()=>{
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const norm=s=>String(s??'').normalize('NFKC').trim().toLowerCase().replace(/\s+/g,' ');
 const groups=[
  {values:['Element','Compound','Mixture'],when:/element|compound|mixture/i,teaching:{introduction:'Classify by what particles are present and whether they are chemically bonded or only mixed.',rule:'Element: one type of atom. Compound: different elements chemically bonded in a fixed composition. Mixture: substances combined physically with variable composition.',symbols:[],example:{prompt:'Compare pure copper, pure carbon dioxide, and salt water.',steps:['Copper contains one atomic element, so it is an element.','Carbon dioxide has chemically bonded C and O in a fixed ratio, so it is a compound.','Salt water combines substances physically and can have different salt concentrations, so it is a mixture.'],conclusion:'Fixed chemical composition and physical mixing distinguish these categories.'},approach:['Identify whether the sample contains one atomic element or multiple elements.','If multiple elements are present, ask whether the whole sample is one fixed-composition bonded substance.','If separate substances are physically combined, classify the combination as a mixture.'],pitfalls:['A compound can contain many atoms while still being a pure substance.']},hint:'Check atom types, chemical bonding, and whether composition is fixed.'},
  {values:['Physical','Chemical'],when:/physical|chemical/i,teaching:{introduction:'A physical change rearranges the state or appearance of a substance. A chemical change creates substances with different chemical identities.',rule:'Physical change: chemical identities are retained. Chemical change: reactants are transformed into chemically different products.',symbols:[],example:{prompt:'Compare cutting a copper wire with forming copper oxide on its surface.',steps:['Cutting changes size but retains copper’s chemical identity.','Formation of copper oxide produces a new compound through reaction with oxygen.'],conclusion:'Decide by chemical identity, rather than simply whether the appearance changes.'},approach:['Identify the substances before and after the stated process.','Ask whether their chemical identities change or merely their shape, state, or arrangement.','Match retained identities with a physical change and new substances with a chemical change.'],pitfalls:['A color change alone is evidence to consider, not a universal proof of chemical reaction.']},hint:'Ask whether a different chemical substance is formed.'},
  {values:['Macroscopic','Microscopic','Symbolic'],when:/macroscopic|microscopic|symbolic|domain/i,teaching:{introduction:'Chemistry descriptions can concern directly observed samples, the particles explaining them, or notation representing either.',rule:'Macroscopic: observable bulk properties. Microscopic: atoms, molecules, or ions. Symbolic: formulas, equations, symbols, or numerical representations.',symbols:[],example:{prompt:'Describe a bottle of carbon dioxide at three levels.',steps:['Its measurable pressure is a macroscopic property.','Its moving CO₂ molecules form a microscopic description.','The written formula CO₂ is a symbolic representation.'],conclusion:'The same substance can be described at all three levels.'},approach:['Determine whether the question’s statement describes a bulk observation, particles, or written notation.','Do not classify a formula as an actual particle just because it names that particle.','Choose the level used by this particular description.'],pitfalls:['The domains describe representations, not three different kinds of chemical substance.']},hint:'Distinguish bulk observations, particle explanations, and written notation.'},
  {values:['Exact','Uncertain'],when:/exact|uncertain|measurement|significant/i,teaching:{introduction:'Counting and defined unit relationships can be exact. A measured value has a limit set by the measuring method.',rule:'Exact numbers arise from counts or definitions. Measured numbers carry uncertainty and a finite precision.',symbols:[],example:{prompt:'Compare 8 counted bolts with a measured wire length of 8.3 cm.',steps:['The count of 8 bolts is exact if the count is correct.','The 8.3 cm length has precision limited by the measurement.','The defined conversion 1 m=100 cm is exact.'],conclusion:'The origin of a number determines whether its precision is limited.'},approach:['Identify how the stated number was obtained.','Separate counts and defined conversions from experimental measurements.','Use exact for counts/definitions and uncertain for measurement-limited values.'],pitfalls:['A number with decimals may be exact by definition; appearance alone does not decide.']},hint:'Check whether the value is counted, defined, or measured.'},
  {values:['Intensive','Extensive'],when:/intensive|extensive|property|properties/i,teaching:{introduction:'Imagine dividing the same uniform sample in half. An extensive property decreases with sample size; an intensive property stays the same under unchanged conditions.',rule:'Extensive properties depend on the amount of material. Intensive properties do not depend on the amount for a uniform sample under the same conditions.',symbols:[],example:{prompt:'Split a uniform 200 g liquid sample into two equal portions at the same temperature.',steps:['Each portion has half the mass and volume.','Each retains the same temperature and density as the original sample.'],conclusion:'Mass and volume are extensive; temperature and density are intensive.'},approach:['Imagine increasing or decreasing the amount of the same uniform material.','Hold conditions such as temperature and pressure fixed.','If the property scales with amount, call it extensive; if it remains characteristic of the material, call it intensive.'],pitfalls:['A ratio of two extensive properties, such as mass/volume, can be intensive.']},hint:'Imagine dividing the same uniform sample in half.'},
  {values:['True','False'],when:/true|false/i,hint:'Check every condition in the statement; one counterexample is enough to make it false.'},
  {values:['Yes','No'],when:/\b(?:can|will|is|are|does|do|would|could|conserve|possible|occur|stable|have|make|difference)\b/i,hint:'Compare the stated conditions with the relevant definition or physical relationship.'},
  {values:['Positive','Negative','Zero'],when:/sign|positive|negative|zero|direction/i,hint:'Choose the positive direction or sign convention before classifying the result.'},
  {values:['Positive direction','Negative direction','Neither direction'],when:/direction/i,hint:'Compare the motion with the indicated coordinate axis.'},
  {values:['Less','Same','Greater'],when:/less|equal|greater/i,hint:'Use the relationship between the quantities and compare the stated situations.'},
  {values:['Increases','Decreases','Remains unchanged'],when:/increas|decreas|change|varies/i,hint:'Identify which quantity changes, then hold the other stated quantities fixed.'},
  {values:['Increasing','Decreasing','Constant'],when:/increas|decreas|constant|change/i,hint:'Compare how the requested quantity behaves as the independent variable changes.'},
  {values:['Clockwise','Counterclockwise'],when:/clockwise|rotation|rotat|current|direction/i,hint:'Use the indicated viewing direction and the sign or right-hand rule appropriate to the problem.'},
  {values:['Parallel','Perpendicular','Neither parallel nor perpendicular'],when:/parallel|perpendicular|direction|vector|field/i,hint:'Compare directions; perpendicular vectors have a zero dot product.'},
  {values:['R','S'],when:/configuration|assign.*R|chirality/i,hint:'Rank substituents by priority and view the lowest-priority group toward the rear.'},
  {values:['E','Z'],when:/configuration|alkene|double.bond|assign.*E/i,hint:'Compare the higher-priority substituent on each carbon of the double bond.'},
  {values:['Addition','Elimination','Substitution','Rearrangement'],when:/classify|reaction type|addition|elimination|substitution|rearrangement/i,hint:'Compare the bonds and connectivity of the reactant and product.'},
  {values:['Oxidation','Reduction','Neither'],when:/oxidation|reduction/i,hint:'Compare carbon bonds to electronegative atoms and to hydrogen.'},
  {values:['Ortho','Meta','Para'],when:/ortho|meta|para|disubstituted/i,hint:'Locate the two substituents on the aromatic ring: positions 1,2; 1,3; or 1,4.'},
  {values:['SN1','SN2','E1','E1cB','E2'],when:/SN1|SN2|E1|E2|substitution reaction/i,hint:'Consider the substrate, nucleophile or base, solvent, and whether substitution or elimination occurs.'},
  {values:['Singlet','Doublet','Triplet','Quartet','Multiplet'],when:/NMR|splitting|coupl|multiplicity/i,hint:'Check the number of coupled neighboring protons and whether exchange removes the coupling.'},
  {values:['Dextrorotatory','Levorotatory'],when:/dextrorotatory|levorotatory|rotation/i,hint:'Use the sign of the observed optical rotation; R/S configuration alone does not determine it.'},
  {values:['Constitutional isomers','Enantiomers','Diastereomers','Identical compounds'],when:/isomer|relationship|stereochemical/i,hint:'First compare atom connectivity; then compare the stereochemistry and mirror-image relationship.'}
 ];
 function ordered(values,key){let seed=0;for(const c of key)seed=(seed*31+c.charCodeAt(0))>>>0;const shift=seed%values.length;return values.slice(shift).concat(values.slice(0,shift))}
 function curated(entry,q,index){return {type:'choice',label:entry.label||'answer',selectionPrompt:entry.selectionPrompt,answer:entry.answer,options:ordered([entry.answer,...entry.distractors],q.id+':'+(entry.label||index)),explanation:entry.explanation,hint:entry.hint,provenance:'calx-concept-adaptation'}}
 function categorical(rule,q,index){
  if(rule.type!=='exactText'||rule.normalization==='electron-configuration'||!rule.answer)return rule;
  const group=groups.find(g=>g.values.some(v=>norm(v)===norm(rule.answer))&&g.when.test((q.prompt||'')+' '+q.id));if(!group)return rule;
  const canonical=group.values.find(v=>norm(v)===norm(rule.answer));const values=group.values[0]==='SN1'&&!/\bE(?:1|2|1cB)\b/.test(q.prompt||'')?['SN1','SN2']:group.values;
  return {...rule,type:'choice',answer:canonical,responseSourceRule:{...rule},responseAdaptation:'verified-category-choice',options:ordered(values,q.id+':'+index),hint:group.hint,teaching:group.teaching,explanation:'This selection matches the textbook answer reference. '+group.hint,provenance:rule.provenance||'textbook-answer-key'};
 }
 const counts={zero:0,one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10,twelve:12};
 const termSets=[['Yes','No'],['Positive','Negative','Zero'],['Increasing','Decreasing','Constant'],['Increases','Decreases','Remains unchanged'],['Addition','Elimination','Substitution','Rearrangement'],['Singlet','Doublet','Triplet','Quartet','Multiplet'],['Constitutional isomers','Enantiomers','Diastereomers','Identical compounds'],['opposite','same'],['stronger','weaker'],['bonding','nonbonding','core'],['more substituted carbon','less substituted carbon'],['Markovnikov','anti-Markovnikov'],['Lyase','Hydrolase','Oxidoreductase','Transferase','Isomerase','Ligase'],['squeeze','mean value theorem','intermediate value theorem','extreme value theorem']];
 const scopedText={
  'calculus-section-8-1-14':{'sec x':['cos x','tan x','sec^2 x']},
  'organic-24-4':{'CH3CH2NH2':['The amide shown'],'NaOH':['The neutral alkylamine shown'],'CH3NHCH3':['The pyridine ring shown']},
  'organic-2-46':{'methylamine':['ammonia']}
 };
 const elements='H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra'.split(' ');
 function makeChoice(rule,wrong,q,index,hint){
  const answer=String(rule.answer??''),options=[answer,...wrong.map(String)].filter((v,i,a)=>v&&a.indexOf(v)===i);
  if(!answer||options.length<2)return null;
  return {...rule,type:'choice',answer,options:ordered(options.slice(0,4),(q?.id||'step')+':'+index),responseSourceRule:{...rule},responseAdaptation:'verified-answer-choice',hint:hint||rule.hint||'Compare the alternatives with the equation, definitions, and given conditions.',explanation:rule.explanation||'This option matches the verified reference for the requested quantity.'};
 }
 function responseRule(rule,q={},index=0){
  if(!rule)return null;if(['numeric','choice'].includes(rule.type))return rule;
  if(!String(rule.answer??'').trim())return null;
  if(rule.type==='expression'){
   if(!window.AnswerChecker)return null;try{if(!AnswerChecker.equivalent(rule.answer,rule.answer))return null}catch{return null}
   const a=String(rule.answer),candidates=['-('+a+')','2*('+a+')','('+a+')/2','1/('+a+')'],wrong=candidates.filter(v=>AnswerChecker.check(rule,v).status==='incorrect');
   return makeChoice(rule,wrong,q,index,'Check signs, coefficients, and division in the displayed relationship.');
  }
  if(rule.type!=='exactText')return null;
  const cat=categorical(rule,q,index);if(cat.type==='choice')return cat;
  const a=String(rule.answer),n=norm(a),custom=scopedText[q.id||q.questionId]?.[a];if(custom)return makeChoice(rule,custom,q,index);
  const set=termSets.find(values=>values.some(v=>norm(v)===n));if(set)return makeChoice(rule,set.filter(v=>norm(v)!==n),q,index);
  if(n==='does not exist')return makeChoice(rule,['Exists'],q,index,'Check whether the requested limit or object satisfies its existence conditions.');
  if(Object.hasOwn(counts,n))return {...rule,type:'numeric',answer:counts[n],tolerance:0,responseSourceRule:{...rule},responseAdaptation:'verified-count'};
  if(['northwest','northeast','southwest','southeast'].includes(n))return makeChoice(rule,['northwest','northeast','southwest','southeast'].filter(v=>v!==n),q,index,'Check the signs of the horizontal and vertical components.');
  if(rule.normalization==='electron-configuration'||/^(?:\d[spdf]\d+\s*)+$/.test(a)){
   const matches=[...a.matchAll(/(\d[spdf])(\d+)/g)];if(!matches.length)return null;const last=matches.at(-1),count=Number(last[2]),start=last.index+last[1].length,stop=start+last[2].length;
   const wrong=[count-1,count+1,count+2].filter(v=>v>=0).map(v=>a.slice(0,start)+v+a.slice(stop)).filter(v=>!rule.accepted?.some(x=>norm(x)===norm(v)));
   return makeChoice(rule,wrong,q,index,'Count electrons and check the occupancy of the final subshell against the stated atom or ion.');
  }
  if(rule.normalization==='chemical-formula'){
   const at=elements.indexOf(a),elementContext=/atom|atomic|element|electron|electroneg|periodic|metal|nonmetal|configuration|proton|chemical symbol|polarity/i.test(q.prompt||q.answerPrompt||'')||(q.id||q.questionId)==='organic-2-1';if(at>=0&&elementContext)return makeChoice(rule,[elements[(at+1)%elements.length],elements[(at+2)%elements.length],elements[(at+elements.length-1)%elements.length]],q,index,'Compare the named element, atomic number, periodic trend, or electron count requested in the source question.');
   if(a.length>1&&/^(?:[A-Z][a-z]?\d*)+[+-]?$/.test(a)){
    const match=[...a.matchAll(/[A-Z][a-z]?(\d*)/g)].find(m=>m[1]);
    if(match){const start=match.index+match[0].length-match[1].length,stop=start+match[1].length,count=Number(match[1]);return makeChoice(rule,[count-1,count+1,count+2].filter(v=>v>=1).map(v=>a.slice(0,start)+(v===1?'':v)+a.slice(stop)),q,index,'Count atoms and check the required bonding or charge. The alternatives change an atom count.');}
    const end=a.match(/[+-]$/)?.[0]||'',body=end?a.slice(0,-1):a;return makeChoice(rule,[body+'2'+end,body+'3'+end,body+'4'+end],q,index,'Check the atom counts and the specified formula or bond polarity.');
   }
  }
  return null;
 }
 function adapt(q){
  // A strict study edition already supplies reviewed objective fields and matching
  // guidance. Legacy conceptual wording must not replace those answer contracts.
  const reviewed=q.chapterStudyVerified||q.answerAudit?.chapterStudyVerified||q.answerAudit?.objectiveChecksVerified;
  const reviewedFields=q.grader?.type==='parts'?q.grader.parts:q.grader?[q.grader]:[];
  if(reviewed&&reviewedFields.length&&reviewedFields.every(r=>['numeric','choice'].includes(r.type)))return q;
  const entries=window.CONCEPT_CHOICE_DATA?.[q.id]||[];let all=q.grader?.type==='parts'?(q.grader.parts||[]).map(r=>({...r})):q.grader?[{...q.grader}]:[];
  all=all.map((r,i)=>responseRule(r,q,i)||r);
  for(const [i,entry] of entries.entries()){
   const part=entry.label||null;let at=all.findIndex(r=>(window.ResponseParts?.partLabel(r.label)||null)===part);
   if(at>=0&&all[at].type==='numeric')continue;
   const rule=curated(entry,q,i);if(at<0)all.push(rule);else all[at]={...all[at],...rule};
  }
  if(!all.some(r=>r.type==='choice'||r.responseAdaptation))return q;
  const hints=entries.length?[entries[0].hint,'Compare the definitions and assumptions in the chapter with each option. Eliminate an option if any required condition or part of its explanation fails.']:q.hints;
  const learningSolutions=q.learningSolutions?.map(sol=>({...sol,finalRules:sol.finalRules?.map(r=>['choice','numeric'].includes(all[r.fieldIndex]?.type)&&all[r.fieldIndex]?.responseAdaptation?{...r,...all[r.fieldIndex],fieldIndex:r.fieldIndex}:r)}));
  return {...q,hints,learningSolutions,responsePartPrompt:entries.length&&/concept-check/.test(q.id)?q.prompt.split(/\bCONCEPT CHECK\b/)[0]:q.responsePartPrompt,choiceAdapted:true,grader:all.length===1&&!all[0].label?.match(/^[a-z]$/i)?all[0]:{...(q.grader?.type==='parts'?q.grader:{}),type:'parts',parts:all}};
 }
 function canonical(rule,value){const source=rule.responseSourceRule,compare=v=>source?.caseSensitive?String(v??'').normalize('NFKC').trim():norm(v),option=rule.options?.find(v=>compare(v)===compare(value));if(option)return option;if(String(value??'').trim()&&source&&window.AnswerChecker&&AnswerChecker.check(source,value).status==='correct')return rule.answer;if(!source&&String(value??'').trim()&&(rule.accepted||[]).some(v=>norm(v)===norm(value)))return rule.answer;return ''}
 function field(rule,value){const k=esc(rule.fieldKey),selected=canonical(rule,value);return `<fieldset class="question-choice-group" id="question-choice-group-${k}" aria-describedby="question-result-${k}"><legend>${rule.partLabel?'Part '+esc(rule.partLabel.toUpperCase())+' · ':''}${window.SolutionMath?SolutionMath.inline(rule.selectionPrompt||'Choose the best answer for '+rule.label+'.'):esc(rule.selectionPrompt||'Choose the best answer for '+rule.label+'.')}</legend><input type="hidden" id="question-answer-${k}" data-question-answer="${k}" value="${esc(selected)}">${rule.options.map((option,i)=>`<label class="question-choice-card ${selected===option?'selected':''}"><input type="radio" name="question-choice-${k}" id="question-choice-${k}-${i}" data-choice-field="${k}" value="${esc(option)}" aria-label="${esc(option)}" ${selected===option?'checked':''}><span class="question-choice-letter" aria-hidden="true">${String.fromCharCode(65+i)}</span><span class="question-choice-content">${window.SolutionMath?SolutionMath.render(option):esc(option)}</span></label>`).join('')}</fieldset>`}
 function sync(fieldKey,value){document.querySelectorAll?.('[data-choice-field="'+fieldKey+'"]').forEach(input=>{input.checked=input.value===value;input.closest('label')?.classList.toggle('selected',input.checked)})}
 return {adapt,responseRule,canonical,field,sync};
})();
