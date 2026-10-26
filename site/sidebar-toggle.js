/* Sidebar preference is local UI state; it never changes account or study data. */
(()=>{'use strict';
 const root=document.documentElement,key='glasshouse-sidebar-closed',mobile=matchMedia('(max-width:760px)');
 const preference=()=>{try{return localStorage.getItem(key)==='true'}catch{return false}};
 root.dataset.sidebarClosed=String(mobile.matches||preference());
 document.addEventListener('DOMContentLoaded',()=>{
  const sidebar=document.getElementById('workspace-sidebar'),toggle=document.getElementById('sidebar-toggle'),close=document.getElementById('sidebar-close'),backdrop=document.getElementById('sidebar-backdrop'),shell=document.querySelector('.shell');
  if(!sidebar||!toggle||!close)return;
  const isClosed=()=>root.dataset.sidebarClosed==='true';
  function sync(){const closed=isClosed();sidebar.inert=closed;sidebar.setAttribute('aria-hidden',String(closed));toggle.setAttribute('aria-expanded',String(!closed));toggle.setAttribute('aria-label',closed?'Open sidebar':'Close sidebar');toggle.title=closed?'Open sidebar':'Close sidebar';backdrop.hidden=closed||!mobile.matches;shell.inert=mobile.matches&&!closed;root.classList.toggle('sidebar-overlay-open',mobile.matches&&!closed);}
  function set(closed,restore=false){root.dataset.sidebarClosed=String(closed);if(!mobile.matches)try{localStorage.setItem(key,String(closed))}catch{}sync();if(restore)toggle.focus();else if(!closed&&mobile.matches)close.focus();}
  toggle.addEventListener('click',()=>set(!isClosed()));close.addEventListener('click',()=>set(true,true));backdrop.addEventListener('click',()=>set(true,true));
  document.addEventListener('keydown',e=>{if(isClosed())return;if(e.key==='Escape'){e.preventDefault();set(true,true)}else if(e.key==='Tab'&&mobile.matches){const items=[...sidebar.querySelectorAll('a[href],button:not([disabled]),summary')].filter(x=>x.getClientRects().length),first=items[0],last=items[items.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}});
  sidebar.addEventListener('click',e=>{const account=e.target.closest('[data-sidebar-account]');if(account){if(mobile.matches)set(true);document.querySelector('header [data-account-open]')?.click();return;}if(mobile.matches&&e.target.closest('[data-page],[data-subject],a[href]'))set(true,true);});
  mobile.addEventListener('change',()=>{root.dataset.sidebarClosed=String(mobile.matches||preference());sync();if(isClosed()&&sidebar.contains(document.activeElement))toggle.focus();});sync();
 });
})();
