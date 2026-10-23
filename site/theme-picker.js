/* Visitor-owned appearance. Apply saved tokens before styles to avoid a palette flash. */
(function () {
  'use strict';
  var root = document.documentElement, key = 'glasshouse-palette-v1';
  var palettes = [
    {id:'coral', name:'Coral', accent:'#ff674f', light:'#fff3ee', dark:'#200e16'},
    {id:'ocean', name:'Ocean', accent:'#287de8', light:'#f1f6ff', dark:'#101d30'},
    {id:'forest', name:'Forest', accent:'#22875c', light:'#f1f8f2', dark:'#12251e'},
    {id:'violet', name:'Violet', accent:'#9860e8', light:'#f7f2ff', dark:'#21172f'},
    {id:'amber', name:'Amber', accent:'#ed9a23', light:'#fff8eb', dark:'#282013'},
    {id:'graphite', name:'Graphite', accent:'#77869d', light:'#f4f5f7', dark:'#191d24'}
  ];
  var choice = {palette:'coral',accent:'#ff674f'}, properties = [], savedOK = true;
  var hex = /^#[0-9a-f]{6}$/i;
  function decode(text) {
    try { var p=JSON.parse(text);if(p && (p.palette==='custom'||palettes.some(function(x){return x.id===p.palette;})) && hex.test(p.accent)) return {palette:p.palette,accent:p.accent}; } catch (_) {}
    return {palette:'coral',accent:'#ff674f'};
  }
  try { choice=decode(localStorage.getItem(key)); } catch (_) {}
  function rgb(h){return [1,3,5].map(function(i){return parseInt(h.slice(i,i+2),16);});}
  function mix(a,b,f){var x=rgb(a),y=rgb(b);return '#'+x.map(function(v,i){return Math.round(v+(y[i]-v)*f).toString(16).padStart(2,'0');}).join('');}
  function luminance(h){var a=rgb(h).map(function(v){v/=255;return v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4);});return .2126*a[0]+.7152*a[1]+.0722*a[2];}
  function contrast(a,b){var x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
  function onColor(c){var preferred=contrast('#ffffff',c)>contrast('#10151e',c)?'#ffffff':'#10151e';return contrast(preferred,c)>=4.5?preferred:'#000000';}
  function readable(c,bg){var target=luminance(bg)<.3?'#ffffff':'#10151e',out=c;for(var i=0;i<=100&&contrast(out,bg)<4.6;i++)out=mix(c,target,i/100);return out;}
  function tokens(p,dark) {
    var accent=p.accent,bg=dark?p.dark:p.light,ink=dark?'#f3f5fa':'#202631';
    var paper=dark?mix(bg,'#ffffff',.045):'#fffefe',soft=mix(bg,accent,dark?.12:.065),tint=mix(bg,accent,dark?.17:.13),muted=readable(dark?'#c2c7d2':'#5d6674',bg);
    var line=mix(bg,ink,dark?.27:.25),link=readable(accent,paper),aqua=dark?'#80d7e4':'#126c82',bright=accent,on=onColor(bright),control=mix(bg,ink,dark?.5:.42);
    return {'--bg':bg,'--ink':ink,'--solution-math-ink':ink,'--muted':muted,'--line':line,'--white':paper,'--green':link,'--pink':accent,'--lime':accent,'--orange':link,'--aqua':aqua,'--ice':soft,
      '--calx-paper':paper,'--calx-soft':soft,'--calx-coral':link,'--calx-coral-paper':tint,'--calx-readable':muted,
      '--mode-control-bg':paper,'--mode-control-ink':ink,'--mode-control-border':control,'--mode-control-hover':tint,'--mode-border':control,'--mode-hover':tint,
      '--gh-bright':bright,'--gh-on-bright':on,'--gh-on-coral':onColor(link),'--gh-hero':dark?tint:mix(bg,accent,.42),'--gh-hero-ink':ink,'--gh-cool-surface':soft,'--gh-cool-ink':ink,'--gh-hover':tint,
      '--appearance-accent':accent};
  }
  function currentPalette(){return palettes.find(function(p){return p.id===choice.palette;})||{id:'custom',name:'Custom',accent:choice.accent,light:'#f5f6f9',dark:'#181e29'};}
  function paint(){
    var panel=document.getElementById('appearance-panel'),p=currentPalette();
    document.querySelectorAll('[data-palette-toggle]').forEach(function(b){b.title='Theme: '+p.name;});
    if(!panel)return;
    panel.querySelectorAll('[data-palette-choice]').forEach(function(input){input.checked=input.value===choice.palette;});
    panel.querySelectorAll('[data-custom-accent]').forEach(function(input){if(document.activeElement!==input)input.value=p.accent;});
    panel.querySelector('[data-palette-status]').textContent=p.name+' selected. '+(savedOK?'Saved on this device.':'Preview applied; this browser could not save your preference.');
    panel.querySelector('[data-custom-row]').setAttribute('data-active',String(choice.palette==='custom'));
  }
  function apply(persist){
    var p=currentPalette(),dark=root.getAttribute('data-theme')==='dark';
    properties.forEach(function(k){root.style.removeProperty(k);});properties=[];
    root.setAttribute('data-palette',p.id);
    if(p.id!=='coral'){var values=tokens(p,dark);properties=Object.keys(values);properties.forEach(function(k){root.style.setProperty(k,values[k]);});}
    var meta=document.querySelector('meta[name="theme-color"]');if(meta)meta.content=dark?p.dark:p.accent;
    if(persist){try{localStorage.setItem(key,JSON.stringify(choice));savedOK=true;}catch(_){savedOK=false;}}
    paint();
  }
  function close(restoreFocus){var p=document.getElementById('appearance-panel'),b=document.querySelector('[data-palette-toggle]');if(!p||p.hidden)return;p.hidden=true;b.setAttribute('aria-expanded','false');if(restoreFocus)b.focus();}
  function mount(){
    var panel=document.getElementById('appearance-panel');if(!panel)return;
    panel.innerHTML='<div class="appearance-heading"><div><span>YOUR WORKSPACE</span><h2 id="appearance-title">Make it yours.</h2></div><button type="button" class="appearance-close" data-palette-close aria-label="Close theme picker">×</button></div><p class="appearance-intro">Pick a palette. Keep your light or dark mode.</p><fieldset class="palette-grid"><legend>Color palette</legend>'+palettes.map(function(p){return '<label class="palette-option" style="--swatch:'+p.accent+';--swatch-paper:'+p.light+';--swatch-dark:'+p.dark+'"><input type="radio" name="glasshouse-palette" value="'+p.id+'" data-palette-choice><span class="palette-preview" aria-hidden="true"><i></i><b></b><em></em></span><span class="palette-name">'+p.name+'</span><span class="palette-check" aria-hidden="true">✓</span></label>';}).join('')+'</fieldset><div class="custom-accent" data-custom-row><label for="custom-theme-color">Custom accent<small>Choose any color</small></label><input id="custom-theme-color" type="color" value="#ff674f" data-custom-accent aria-label="Custom accent color"><input type="text" class="accent-hex" value="#ff674f" data-custom-accent maxlength="7" pattern="#[0-9a-fA-F]{6}" aria-label="Custom accent hex code" spellcheck="false" autocomplete="off"></div><p class="appearance-status" data-palette-status role="status"></p>';
    paint();
  }
  apply(false);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount,{once:true});else mount();
  window.addEventListener('glasshouse:mode-change',function(){apply(false);});
  document.addEventListener('click',function(e){
    var toggle=e.target.closest('[data-palette-toggle]');
    if(toggle){var p=document.getElementById('appearance-panel');if(!p)return;var opening=p.hidden;p.hidden=!opening;toggle.setAttribute('aria-expanded',String(opening));if(opening){var checked=p.querySelector('input:checked')||p.querySelector('input');checked.focus();}return;}
    if(e.target.closest('[data-palette-close]')){close(true);return;}
    if(!e.target.closest('.appearance-picker'))close(false);
  });
  document.addEventListener('change',function(e){
    if(!e.target.matches('[data-palette-choice]'))return;
    var p=palettes.find(function(p){return p.id===e.target.value;});if(p){choice={palette:p.id,accent:p.accent};apply(true);}
  });
  document.addEventListener('input',function(e){if(e.target.matches('[data-custom-accent]')&&hex.test(e.target.value)){choice={palette:'custom',accent:e.target.value.toLowerCase()};apply(true);}});
  document.addEventListener('focusout',function(e){if(e.target.matches('[data-custom-accent]'))paint();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&document.getElementById('appearance-panel')?.hidden===false){e.preventDefault();close(true);}});
  document.addEventListener('focusin',function(e){if(!e.target.closest('.appearance-picker'))close(false);});
  window.addEventListener('storage',function(e){if(e.key===key||e.key===null){choice=decode(e.key===null?null:e.newValue);savedOK=true;apply(false);}});
})();
