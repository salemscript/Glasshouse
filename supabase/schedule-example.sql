-- Run only after the Edge Function and secrets are configured.
-- Enable pg_cron and pg_net through the Supabase dashboard first.
-- Create Vault secrets named glasshouse_notification_url (full function URL)
-- and glasshouse_notification_secret (same value as SIGNUP_NOTIFICATION_SECRET).
-- Do not commit their values. Run this once; avoid duplicate jobs.
select cron.schedule('glasshouse-signup-notifications','*/5 * * * *',$job$
 select net.http_post(
   url := (select decrypted_secret from vault.decrypted_secrets where name='glasshouse_notification_url'),
   headers := jsonb_build_object('Content-Type','application/json','x-notification-secret',
     (select decrypted_secret from vault.decrypted_secrets where name='glasshouse_notification_secret')),
   body := '{}'::jsonb,
   timeout_milliseconds := 90000
 );
$job$);
