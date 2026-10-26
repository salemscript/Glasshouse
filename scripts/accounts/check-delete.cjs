const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
(async()=>{let handler,deleted,revoked=false,valid=true,revokeFail=false;
const admin={auth:{getUser:async()=>valid?{data:{user:{id:'authenticated-owner'}}}:{error:true,data:{}},admin:{signOut:async()=>{revoked=true;return{error:revokeFail}},deleteUser:async(id,soft)=>{assert(revoked);assert.equal(soft,false);deleted=id;return{}}}}};
const source=fs.readFileSync('supabase/functions/delete-account/index.ts','utf8').replace(/^import .*\n/,'').replace('req: Request','req').replace('body:object','body').replaceAll("')!","')");
vm.runInNewContext(source,{createClient:()=>admin,Request,Response,Deno:{serve:f=>handler=f,env:{get:()=> 'test'}}});
const req=(token,confirmation='DELETE')=>new Request('https://test.invalid',{method:'POST',headers:token?{authorization:'Bearer test'}:{},body:JSON.stringify({confirmation,user_id:'someone-else'})});
assert.equal((await handler(req(false))).status,401);assert.equal((await handler(req(true,'no'))).status,400);valid=false;assert.equal((await handler(req(true))).status,401);assert.equal(deleted,undefined);valid=true;revokeFail=true;assert.equal((await handler(req(true))).status,503);assert.equal(deleted,undefined);revokeFail=false;assert.equal((await handler(req(true))).status,200);assert.equal(deleted,'authenticated-owner');console.log('PASS: auth, confirmation, revocation failure, owner-only hard deletion');
})().catch(e=>{console.error(e);process.exitCode=1});
