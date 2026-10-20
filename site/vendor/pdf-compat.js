/* Small standard API fallbacks for PDF.js on older browsers and Node QA. */
function installPDFCompatibility(){
 const define=(object,key,value)=>{if(typeof object[key]!=='function')Object.defineProperty(object,key,{value,writable:true,configurable:true});};
 define(Uint8Array.prototype,'toHex',function(){return Array.from(this,n=>n.toString(16).padStart(2,'0')).join('');});
 define(Uint8Array.prototype,'toBase64',function(options={}){let s='';for(let i=0;i<this.length;i+=16384)s+=String.fromCharCode(...this.subarray(i,i+16384));let encoded=btoa(s);if(options.alphabet==='base64url')encoded=encoded.replace(/\+/g,'-').replace(/\//g,'_');return options.omitPadding?encoded.replace(/=+$/,''):encoded;});
 define(Uint8Array,'fromBase64',function(text){const s=atob(String(text).replace(/-/g,'+').replace(/_/g,'/').replace(/\s/g,''));return Uint8Array.from(s,c=>c.charCodeAt(0));});
 define(Promise,'try',function(fn,...args){return new this(resolve=>resolve(fn(...args)));});
 for(const type of [Map,WeakMap]){
  define(type.prototype,'getOrInsert',function(key,value){if(!this.has(key))this.set(key,value);return this.get(key);});
  define(type.prototype,'getOrInsertComputed',function(key,fn){if(!this.has(key))this.set(key,fn(key));return this.get(key);});
 }
}
installPDFCompatibility();
