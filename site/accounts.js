/* Email-code accounts, with credentials handled by Supabase Auth. */
(()=>{
 'use strict';
 const config=window.GlasshouseAccountConfig||{},store=window.GlasshouseStorage;
 const configured=config.enabled===true&&/^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(config.supabaseUrl)&&/^(sb_publishable_|eyJ)/.test(config.publishableKey||'');
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 let client=null,syncer=null,user=null,busy=false,email='',signup=false,displayName='',sent=false,nextSend=0,changed=false,lastSync='local',returnFocus=null,timer=null;
 const dialog=document.createElement('dialog');dialog.className='account-dialog';dialog.setAttribute('aria-labelledby','account-title');document.body.appendChild(dialog);
 const note=document.createElement('div');note.className='account-sync-notice';note.hidden=true;note.innerHTML='<span>New progress is ready from your account.</span><button type="button" data-account-refresh>Load saved progress</button>';document.body.appendChild(note);
 const cleanName=value=>typeof value==='string'?value.replace(/[\u0000-\u001f\u007f]/g,'').replace(/\s+/g,' ').trim().slice(0,50):'';
 const name=()=>cleanName(user?.user_metadata?.display_name);
 window.GlasshouseProfile={name};
 function greet(){for(const el of document.querySelectorAll('[data-personal-greeting]')){const text=name()?`Welcome back, ${name()}.`:'Make room for your next discovery.';if(el.textContent!==text)el.textContent=text;}}
 new MutationObserver(greet).observe(document.querySelector('main'),{childList:true,subtree:true});
 function status(message){const el=dialog.querySelector('[data-account-status]');if(el)el.textContent=message;}
 function syncLabel(){return ({local:'Saved on this device',saving:'Saving to your account…',saved:'Saved to your account',pending:'Changes waiting to save',offline:'Saved on this device. Cloud sync will retry.',conflict:'Choose which version to keep below.'})[lastSync]||'Checking your account…';}
 function paint(){
   const button=document.querySelector('[data-account-open]');if(button)button.textContent=user?'My account':'Account';
   greet();if(!dialog.open)return;
   const conflictHTML=(syncer?.conflicts()||[]).map(item=>`<div class="account-conflict"><b>Two saved versions</b><code>${esc(item.key)}</code><p>This item changed on another device. Neither version has been overwritten.</p><details><summary>Compare versions</summary><h4>This device</h4><pre>${esc(store.row(user.id,item.key)?.value??'Cleared')}</pre><h4>Your account</h4><pre>${esc(item.value??'Cleared')}</pre></details><button type="button" data-keep-local="${esc(item.key)}">Keep this device’s version</button><button type="button" data-keep-cloud="${esc(item.key)}">Use account version</button></div>`).join('');
   dialog.innerHTML=`<button type="button" class="account-close" aria-label="Close account">×</button><span class="account-eyebrow">YOUR GLASSHOUSE</span><h2 id="account-title">${user?(name()?`Good to see you, ${esc(name())}.`:'What should we call you?'):'Your learning, saved.'}</h2>`+(!configured?'<p>Accounts are being set up. Your work still saves on this device, and you can keep learning without an account.</p><button type="button" data-account-close>Keep learning</button>':!client?'<p>Connecting to sign-in…</p><p role="status" data-account-status></p><button type="button" data-account-retry>Try again</button>':user?`<p class="account-email">${esc(user.email)}</p><form data-profile-form><label>Your name<input name="displayName" autocomplete="nickname" required maxlength="50" value="${esc(name())}" placeholder="First name or nickname"></label><p class="account-small">The name you like to go by. You can change it anytime.</p><button type="submit">Save name</button></form><p class="account-save-state" role="status" data-sync-state>${esc(syncLabel())}</p><p>Your answers, notes, checked questions and saved lab work stay with this account.</p><div class="account-actions"><button type="button" data-account-sync>Save now</button><button type="button" data-account-import>Add guest work from this device</button><button type="button" data-account-signout>Sign out</button></div><p class="account-small">Guest work stays separate until you add it. Existing account items are never replaced during import. Signing out returns to guest mode.</p>${changed?'<button type="button" data-account-refresh>Load saved progress</button>':''}${conflictHTML}<p role="status" data-account-status></p>`:`<p>Use a code sent to your email. No password to remember.</p><form data-account-form>${signup&&!sent?`<label>Your name<input name="displayName" autocomplete="nickname" required maxlength="50" value="${esc(displayName)}" placeholder="First name or nickname"></label><p class="account-small">What would you like us to call you?</p>`:''}<label>Email address<input type="email" autocomplete="email" name="email" required maxlength="254" value="${esc(email)}" ${sent?'readonly':''}></label>${sent?'<label>Email code<input name="code" type="text" inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]{6,10}" minlength="6" maxlength="10" required autofocus></label><button type="submit">Verify code & continue</button><button type="button" data-account-back>Use a different email</button><button type="button" data-account-resend>Send another code</button>':signup?'<button type="submit" name="mode" value="signup">Send my signup code</button><button type="button" data-account-signin>Already have an account? Sign in</button>':'<div class="account-auth-choices"><button type="submit" name="mode" value="signin">Sign in</button><button type="submit" name="mode" value="signup" formnovalidate>Create account</button></div>'}</form><p class="account-small">Your email is used for sign-in and account support. Creating an account notifies the site owner. Your saved learning work is private to your account.</p><p role="status" data-account-status></p>`);
 }
 function open(){returnFocus=document.activeElement;dialog.showModal();paint();dialog.querySelector('input,button')?.focus();}
 function close(){dialog.close();returnFocus?.focus();}
 function notify(result){lastSync=result.state;changed=changed||Boolean(result.changed);note.hidden=!changed;const el=dialog.querySelector('[data-sync-state]');if(el)el.textContent=syncLabel();if(result.state==='conflict')paint();}
 async function start(){
   if(!configured||client)return;
   try{
     await new Promise((resolve,reject)=>{if(window.supabase){resolve();return;}const script=document.createElement('script');script.src='vendor/supabase-2.118.0.js';script.onload=resolve;script.onerror=reject;document.head.appendChild(script);});
     client=window.supabase.createClient(config.supabaseUrl,config.publishableKey,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:false}});
     syncer=window.GlasshouseAccountSync(client,store,notify);
     client.auth.onAuthStateChange((event,session)=>{setTimeout(()=>sessionChanged(session),0);});
     paint();
   }catch{client=null;paint();status('Sign-in could not connect. Your work is still saved on this device. Try again.');}
 }
 let sessionGeneration=0,intentionalReload=false;
 function reload(){intentionalReload=true;location.reload();}
 async function sessionChanged(session){const next=session?.user||null;if(next?.id===user?.id&&store.scope()===(next?.id||null)){user=next;paint();return;}const turn=++sessionGeneration;user=next;syncer.setUser(user?.id||null);const switching=store.scope()!==(user?.id||null);if(switching)document.body.inert=true;store.setScope(user?.id||null);changed=false;note.hidden=true;
   if(user)await syncer.sync();else lastSync='local';if(turn!==sessionGeneration)return;
   if(switching){reload();return;}paint();if(user&&!name()&&!dialog.open)open();
 }
 dialog.addEventListener('submit',async e=>{
   e.preventDefault();if(busy||!client)return;const form=e.target;if(!user&&!sent&&e.submitter?.value==='signup'&&!signup){email=form.elements.email.value.trim();signup=true;paint();dialog.querySelector('[name="displayName"]')?.focus();return;}if(!form.reportValidity())return;busy=true;for(const b of dialog.querySelectorAll('button'))b.disabled=true;
   try{if(form.hasAttribute('data-profile-form')){const value=cleanName(form.elements.displayName.value);if(!value)throw Error('Please enter a first name or nickname.');const {data,error}=await client.auth.updateUser({data:{display_name:value}});if(error)throw Error('Your name could not be saved. Please try again.');user=data.user;paint();status(`Name saved. Welcome, ${name()}!`);}
    else if(sent){const token=form.elements.code.value.trim();const {error}=await client.auth.verifyOtp({email,token,type:'email'});if(error)throw Error('That code is incorrect or expired. Try again or request a new one.');status('Signed in. Loading your progress…');}
    else{email=form.elements.email.value.trim();signup=e.submitter?.value==='signup';if(signup){displayName=cleanName(form.elements.displayName.value);if(!displayName)throw Error('Please enter a first name or nickname.');}await sendCode();}}
   catch(error){status(error.message||'Could not connect. Please try again.');}
   finally{busy=false;for(const b of dialog.querySelectorAll('button'))b.disabled=false;}
 });
 async function sendCode(){if(Date.now()<nextSend)throw Error('Please wait a minute before requesting another code.');const {error}=await client.auth.signInWithOtp({email,options:{shouldCreateUser:signup,...(signup?{data:{display_name:displayName}}:{})}});if(error)throw Error('We could not send a code. Check the email address, or wait a minute and try again.');nextSend=Date.now()+60000;sent=true;paint();status('If this email can sign in, a code is on its way. Check your inbox and spam folder.');dialog.querySelector('[name="code"]')?.focus();}
 dialog.addEventListener('click',async e=>{
   const b=e.target.closest('button');if(!b||busy)return;
   if(b.classList.contains('account-close')||b.hasAttribute('data-account-close')){close();return;}
   if(b.hasAttribute('data-account-retry')){start();return;}
   if(b.hasAttribute('data-account-signin')){signup=false;paint();return;}
   if(b.hasAttribute('data-account-back')){sent=false;paint();return;}
   if(b.hasAttribute('data-account-resend')){busy=true;try{await sendCode();}catch(err){status(err.message);}finally{busy=false;}return;}
   if(b.hasAttribute('data-account-sync')){await syncer.sync();paint();return;}
   if(b.hasAttribute('data-account-import')){const added=store.importGuest();await syncer.sync();changed=added>0||changed;paint();status(`${added} new saved items added. Load saved progress to see them.`);return;}
   if(b.hasAttribute('data-keep-local')||b.hasAttribute('data-keep-cloud')){const local=b.hasAttribute('data-keep-local');await syncer.resolve(b.getAttribute(local?'data-keep-local':'data-keep-cloud'),local);if(!local)changed=true;paint();return;}
   if(b.hasAttribute('data-account-signout')){await syncer.sync();if(syncer.pending()&&!confirm('Some changes are only saved on this device. Sign out anyway? They will remain in this account’s local cache for your next sign-in.'))return;const {error}=await client.auth.signOut({scope:'local'});if(error){status('Could not sign out. Please try again.');return;}store.setScope(null);reload();}
 });
 document.addEventListener('click',e=>{if(e.target.closest('[data-account-open]'))open();if(e.target.closest('[data-account-refresh]'))reload();});
 store.onChange(()=>{if(!user)return;lastSync='pending';clearTimeout(timer);timer=setTimeout(()=>syncer.sync(),1200);});
 window.addEventListener('online',()=>syncer?.sync());window.addEventListener('focus',()=>syncer?.sync());
 window.addEventListener('storage',e=>{if(e.key?.startsWith('glasshouse-learning-v1:'))syncer?.sync();});
 setInterval(()=>{if(user&&!document.hidden)syncer.sync();},60000);
 window.addEventListener('beforeunload',e=>{if(!intentionalReload&&syncer?.pending()){e.preventDefault();e.returnValue='';}});
 start();
})();
