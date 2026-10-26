import { createClient } from 'npm:@supabase/supabase-js@2.118.0';
const cors={'Access-Control-Allow-Origin':'https://glasshouse.jackchobanian.com','Access-Control-Allow-Headers':'authorization, apikey, content-type, x-client-info','Access-Control-Allow-Methods':'POST, OPTIONS','Vary':'Origin'};
Deno.serve(async (req: Request)=>{
 const reply=(body:object,status=200)=>Response.json(body,{status,headers:cors});
 if(req.method==='OPTIONS')return new Response(null,{status:204,headers:cors});
 if(req.method!=='POST')return reply({error:'Method not allowed'},405);
 const token=req.headers.get('authorization')?.match(/^Bearer (.+)$/i)?.[1];
 if(!token)return reply({error:'Sign in to delete your account.'},401);
 try{
 const body=await req.json();if(body?.confirmation!=='DELETE')return reply({error:'Confirmation required'},400);
 const admin=createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,{auth:{persistSession:false,autoRefreshToken:false}});
 const {data,error}=await admin.auth.getUser(token);
 if(error||!data.user)return reply({error:'Please sign in again.'},401);
 // The authenticated identity is the only deletion target. Never accept a client user ID.
 const {error:revokeError}=await admin.auth.admin.signOut(token,'global');
 if(revokeError)return reply({error:'Could not secure your sessions. Please try again.'},503);
 const {error:deleteError}=await admin.auth.admin.deleteUser(data.user.id,false);
 if(deleteError)return reply({error:'Account deletion failed. Sign in again and retry.'},503);
 // Foreign keys cascade to learning_items and signup_notifications.
 return reply({deleted:true});
 }catch{return reply({error:'Could not complete deletion. Please try again.'},400);}
});
