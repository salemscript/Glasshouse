begin;
create schema if not exists private;
revoke all on schema private from public;
grant usage on schema private to authenticated,service_role;
create table public.learning_items (
  user_id uuid not null references auth.users(id) on delete cascade,
  key text not null check (length(key)<=240),
  value text check (octet_length(value)<=250000),
  version bigint not null default 1 check(version>0),
  updated_at timestamptz not null default now(),
  primary key(user_id,key)
);
alter table public.learning_items enable row level security;
revoke all on public.learning_items from anon,authenticated;
grant select on public.learning_items to authenticated;
create policy "Read only your learning work" on public.learning_items for select to authenticated using ((select auth.uid())=user_id);

create function private.save_learning_item(p_owner_id uuid,p_key text,p_value text,p_expected_version bigint)
returns jsonb language plpgsql security definer set search_path='' as $$
declare who uuid:=auth.uid(); old public.learning_items; result public.learning_items; item_count bigint; total_bytes bigint;
begin
  if who is null or who is distinct from p_owner_id then raise exception 'Authentication required'; end if;
  if p_key is null or length(p_key)>240 or p_key !~ '^(foundry-progress-v1|foundry-understanding-v1|foundry-(answer-v1|notes|exercise-notes)-[a-zA-Z0-9_.:-]+|calx-question-v1-[a-zA-Z0-9_.:-]+|calx-fundamentals-[a-zA-Z0-9_-]+|glasshouse-circuit-builder-v1)$' then raise exception 'Invalid learning item'; end if;
  if coalesce(octet_length(p_value),0)>250000 or p_expected_version is null or p_expected_version<0 then raise exception 'Invalid saved data'; end if;
  -- Serializes writes for this account, including quota checks and first inserts.
  perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended(who::text,0));
  select * into old from public.learning_items where user_id=who and key=p_key;
  if coalesce(old.version,0)<>p_expected_version then
    return jsonb_build_object('conflict',true,'item',jsonb_build_object('key',p_key,'value',old.value,'version',coalesce(old.version,0)));
  end if;
  select count(*),coalesce(sum(octet_length(value)),0) into item_count,total_bytes from public.learning_items where user_id=who;
  if (old.version is null and item_count>=10000) or total_bytes-coalesce(octet_length(old.value),0)+coalesce(octet_length(p_value),0)>15000000 then raise exception 'Account storage limit reached'; end if;
  insert into public.learning_items(user_id,key,value,version) values(who,p_key,p_value,1)
  on conflict(user_id,key) do update set value=excluded.value,version=learning_items.version+1,updated_at=now()
  returning * into result;
  return jsonb_build_object('conflict',false,'item',jsonb_build_object('key',result.key,'value',result.value,'version',result.version));
end;$$;
revoke all on function private.save_learning_item(uuid,text,text,bigint) from public,anon;
grant execute on function private.save_learning_item(uuid,text,text,bigint) to authenticated;

-- Private notification queue. No visitor can read email events or trigger delivery.
create table public.signup_notifications (
 user_id uuid primary key references auth.users(id) on delete cascade,
 created_at timestamptz not null default now(),sent_at timestamptz,
 attempts integer not null default 0, locked_until timestamptz,
 last_error text
);
alter table public.signup_notifications enable row level security;
revoke all on public.signup_notifications from anon,authenticated;
grant all on public.signup_notifications to service_role;
create function private.queue_signup_notification() returns trigger language plpgsql security definer set search_path='' as $$
begin
 insert into public.signup_notifications(user_id) values(new.id) on conflict do nothing;
 return new;
end;$$;
revoke all on function private.queue_signup_notification() from public,anon,authenticated;
create trigger glasshouse_signup_notification after insert on auth.users for each row execute function private.queue_signup_notification();

create function private.claim_signup_notifications() returns setof public.signup_notifications language sql security definer set search_path='' as $$
 update public.signup_notifications n set attempts=n.attempts+1,locked_until=now()+interval '10 minutes'
 where n.user_id in (select q.user_id from public.signup_notifications q where q.sent_at is null and q.attempts<5 and (q.locked_until is null or q.locked_until<now()) order by q.created_at for update skip locked limit 5)
 returning n.*;
$$;
revoke all on function private.claim_signup_notifications() from public,anon,authenticated;
grant execute on function private.claim_signup_notifications() to service_role;
-- Exposed RPCs are invokers; privileged implementations remain in an unexposed schema.
create function public.save_learning_item(p_owner_id uuid,p_key text,p_value text,p_expected_version bigint)
returns jsonb language sql security invoker set search_path='' as $$
 select private.save_learning_item(p_owner_id,p_key,p_value,p_expected_version);
$$;
revoke all on function public.save_learning_item(uuid,text,text,bigint) from public,anon;
grant execute on function public.save_learning_item(uuid,text,text,bigint) to authenticated;
create function public.claim_signup_notifications() returns setof public.signup_notifications
language sql security invoker set search_path='' as $$ select * from private.claim_signup_notifications(); $$;
revoke all on function public.claim_signup_notifications() from public,anon,authenticated;
grant execute on function public.claim_signup_notifications() to service_role;
commit;
