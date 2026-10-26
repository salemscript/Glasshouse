const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
(async()=>{
const listeners={},timers=[],calls=[],greeting={textContent:''},status={textContent:''};
const dialog={open:true,innerHTML:'',className:'',setAttribute(){},addEventListener(k,f){listeners[k]=f},querySelector(s){return s==='[data-account-status]'?status:null},querySelectorAll(){return[]},showModal(){this.open=true},close(){this.open=false}};
let authHandler;const auth={onAuthStateChange(f){authHandler=f},async signInWithOtp(args){calls.push(args);return{}},async updateUser(args){calls.push(args);return {data:{user:{id:'one',email:'test@example.invalid',user_metadata:args.data}}}}};
const store={scope:()=> 'one',setScope(){},onChange(){}};
const document={activeElement:null,createElement(tag){return tag==='dialog'?dialog:{hidden:true}},body:{appendChild(){}},head:{appendChild(){}},querySelector(){return null},querySelectorAll(){return[greeting]},addEventListener(){}};
const window={GlasshouseAccountConfig:{enabled:true,supabaseUrl:'https://example.supabase.co',publishableKey:'sb_publishable_test'},GlasshouseStorage:store,supabase:{createClient:()=>({auth})},GlasshouseAccountSync:()=>({setUser(){},async sync(){},conflicts:()=>[]}),addEventListener(){}};
vm.runInNewContext(fs.readFileSync('site/accounts.js','utf8'),{window,document,MutationObserver:class{observe(){}},setTimeout:f=>timers.push(f),clearTimeout(){},setInterval(){},location:{reload(){throw Error('unexpected reload')}}});
await new Promise(r=>setImmediate(r));
const form=(elements,profile=false)=>({elements,reportValidity:()=>true,hasAttribute:()=>profile});
const submit=(target,value)=>listeners.submit({preventDefault(){},target,submitter:{value}});
await submit(form({email:{value:'test@example.invalid'}}),'signup');assert.match(dialog.innerHTML,/Your name/);
await submit(form({email:{value:'test@example.invalid'},displayName:{value:'   '}}),'signup');assert.equal(calls.length,0);
await submit(form({email:{value:'test@example.invalid'},displayName:{value:'  Zoë   林  '}}),'signup');assert.equal(calls[0].options.data.display_name,'Zoë 林');assert.equal(calls[0].options.shouldCreateUser,true);
authHandler('SIGNED_IN',{user:{id:'one',email:'test@example.invalid',user_metadata:{display_name:'Zoë 林'}}});await timers.pop()();assert.equal(window.GlasshouseProfile.name(),'Zoë 林');assert.equal(greeting.textContent,'Welcome back, Zoë 林.');
dialog.open=true;await submit(form({displayName:{value:'<b>Ada</b>'}},true));assert.match(dialog.innerHTML,/&lt;b&gt;Ada&lt;\/b&gt;/);assert.equal(greeting.textContent,'Welcome back, <b>Ada</b>.');
console.log('PASS: signup requires name, metadata normalization, account greeting, editable name, escaped rendering');
})().catch(e=>{console.error(e);process.exitCode=1});
