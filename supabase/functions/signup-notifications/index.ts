// Supabase Edge Function. Only a scheduled server request may invoke it.
import { createClient } from 'npm:@supabase/supabase-js@2.118.0';
Deno.serve(async (request: Request) => {
  const secret=Deno.env.get('SIGNUP_NOTIFICATION_SECRET');
  if(request.method!=='POST'||!secret||request.headers.get('x-notification-secret')!==secret)return new Response('Unauthorized',{status:401});
  const apiKey=Deno.env.get('RESEND_API_KEY'),to=Deno.env.get('SIGNUP_NOTIFICATION_TO'),from=Deno.env.get('SIGNUP_NOTIFICATION_FROM');
  if(!apiKey||!to||!from)return new Response('Email delivery is not configured',{status:503});
  const admin=createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,{auth:{persistSession:false,autoRefreshToken:false}});
  const {data:events,error}=await admin.rpc('claim_signup_notifications');
  if(error)return new Response('Could not load notifications',{status:503});
  let delivered=0;
  for(const event of events||[]){
    try{
      const {data,error}=await admin.auth.admin.getUserById(event.user_id);if(error||!data.user)throw Error('Account lookup failed');
      const response=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${apiKey}`,'Content-Type':'application/json','Idempotency-Key':`glasshouse-signup-${event.user_id}`},body:JSON.stringify({from,to:[to],subject:'New Glasshouse account',text:`A new Glasshouse account was created.\n\nEmail: ${data.user.email||'(no email)'}\nCreated: ${data.user.created_at}\nEmail verified: ${data.user.email_confirmed_at?'Yes':'Not yet'}\n\nNo learning activity or answers are included in this notification.`}),signal:AbortSignal.timeout(15000)});
      if(!response.ok)throw Error(`Email provider returned ${response.status}`);
      const {error:saveError}=await admin.from('signup_notifications').update({sent_at:new Date().toISOString(),locked_until:null,last_error:null}).eq('user_id',event.user_id);
      if(saveError)throw Error('Delivery receipt could not be stored');delivered++;
    }catch(err){await admin.from('signup_notifications').update({last_error:err instanceof Error?err.message:'Delivery failed'}).eq('user_id',event.user_id);}
  }
  return Response.json({delivered});
});
