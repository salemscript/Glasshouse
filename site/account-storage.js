/* Account-scoped learning data. Guest work remains on this device until explicitly imported. */
window.GlasshouseStorage = (() => {
  'use strict';
  const scopeKey='glasshouse-account-scope-v1',prefix='glasshouse-learning-v1:';
  const allowed=k=>/^(foundry-progress-v1|foundry-understanding-v1|foundry-(answer-v1|notes|exercise-notes)-[a-zA-Z0-9_.:-]+|calx-question-v1-[a-zA-Z0-9_.:-]+|calx-fundamentals-[a-zA-Z0-9_-]+|glasshouse-circuit-builder-v1)$/.test(k);
  let user=null;try{const saved=sessionStorage.getItem(scopeKey);if(window.GlasshouseAccountConfig?.enabled&&/^[0-9a-f-]{36}$/.test(saved||''))user=saved;}catch{}
  const listeners=new Set();
  const address=(id,key)=>prefix+id+':'+key;
  const row=(id,key)=>{try{const r=JSON.parse(localStorage.getItem(address(id,key))||'null');return r&&(typeof r.value==='string'||r.value===null)&&Number.isSafeInteger(r.revision)&&r.revision>=0&&typeof r.dirty==='boolean'?r:null}catch{return null}};
  function keys(id=user){const list=[];for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(id?k.startsWith(prefix+id+':'):allowed(k))list.push(id?k.slice((prefix+id+':').length):k);}return list.filter(allowed).sort();}
  function setItem(key,value){key=String(key);value=String(value);if(!allowed(key))throw Error('Unsupported learning data');if(new TextEncoder().encode(value).length>250000)throw Error('This saved item is too large');if(user){const old=row(user,key);localStorage.setItem(address(user,key),JSON.stringify({value,revision:old?.revision||0,dirty:true,edit:crypto.randomUUID()}));}else localStorage.setItem(key,value);for(const fn of listeners)fn(key);}
  function removeItem(key){if(!allowed(key))return;if(!user)localStorage.removeItem(key);else{const old=row(user,key);localStorage.setItem(address(user,key),JSON.stringify({value:null,revision:old?.revision||0,dirty:true,edit:crypto.randomUUID()}));}for(const fn of listeners)fn(key);}
  function setScope(id){if(id!==null&&!/^[0-9a-f-]{36}$/.test(id))throw Error('Invalid account');user=id;if(id)sessionStorage.setItem(scopeKey,id);else sessionStorage.removeItem(scopeKey);}
  // Only acknowledges the exact edit sent. Later keystrokes stay pending.
  function acknowledge(id,key,sent,version){const current=row(id,key);if(!current)return;localStorage.setItem(address(id,key),JSON.stringify({...current,revision:version,dirty:current.edit!==sent.edit}));}
  function receive(id,key,value,version){if(!allowed(key))return false;const current=row(id,key);if(current?.dirty)return false;localStorage.setItem(address(id,key),JSON.stringify({value,revision:version,dirty:false,edit:current?.edit||0}));return current?.value!==value;}
  function importGuest(){if(!user)throw Error('Sign in before importing guest work');let added=0;for(const k of keys(null)){if(!row(user,k)){setItem(k,localStorage.getItem(k));added++;}}return added;}
  return {allowed,keys,row,setItem,removeItem,setScope,acknowledge,receive,importGuest,
    getItem:key=>user?(row(user,key)?.value??null):localStorage.getItem(key),
    scope:()=>user,onChange:fn=>{listeners.add(fn);return()=>listeners.delete(fn)},
    resolve(id,key,remote,keepLocal){const current=row(id,key);if(keepLocal&&current)localStorage.setItem(address(id,key),JSON.stringify({...current,revision:remote.version,dirty:true}));else localStorage.setItem(address(id,key),JSON.stringify({value:remote.value,revision:remote.version,dirty:false,edit:crypto.randomUUID()}));}
  };
})();
