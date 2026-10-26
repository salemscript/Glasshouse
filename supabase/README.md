# Glasshouse accounts — deployment checkpoint

Status: Glasshouse project `fkafhtggxrfxpadkmuwf` created; accounts migration applied and notification function deployed. Browser integration enabled after the owner confirmed custom SMTP and both email-code templates were saved. Live user signup/restore still needs an end-to-end check. Owner notification delivery remains pending Edge Function secrets and scheduling. The notification queue intentionally has no client RLS policies (deny all); its informational advisor notice is expected.

## Activate

1. Select a Supabase project and link it with the Supabase CLI. Apply the migration in `migrations/` with `supabase db push`. Keep the `private` schema outside the exposed Data API schemas. Run Supabase security/performance advisors after deployment.
2. Enable email authentication and email confirmations. Set Site URL to `https://glasshouse.jackchobanian.com`. Configure custom SMTP with a verified sender so real visitors can receive codes. In both signup confirmation and magic-link email templates, display `{{ .Token }}` as the sign-in code. This UI verifies email codes; it does not process magic-link redirects. Enable appropriate Auth email rate limits and monitor abuse. No OAuth providers or password flows are implemented.
3. Set `supabaseUrl` and **publishable** key in `site/account-config.js`. Never put a service-role, secret API, SMTP or Resend key into `site/`. Enable only after a staging signup/signin test succeeds.
4. Deploy `supabase/functions/signup-notifications` with `supabase functions deploy signup-notifications`. It validates its own random `x-notification-secret` header; config intentionally disables JWT verification. Store `SIGNUP_NOTIFICATION_SECRET`, `RESEND_API_KEY`, `SIGNUP_NOTIFICATION_TO` (owner address), and `SIGNUP_NOTIFICATION_FROM` (verified sender) using Supabase secrets. Runtime supplies SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY. Enter credentials through the provider dashboard or secure CLI, never chat or git.
5. Configure a server scheduler to POST to the deployed function every five minutes, using the secret header. Supabase Cron + pg_net can do this; keep URL and header secret in Vault, never literal credentials in migrations. See `schedule-example.sql`. There is no browser-triggered email route.
6. Test with controlled accounts and two browser profiles: account creation, email code, sign-out, restore on another device, offline editing/reconnect, simultaneous edit conflict, guest import, and receipt of the owner notification. Verify the RLS policies remotely before enabling. No real emails were sent during local tests.

## Progress and privacy

Cloud storage covers existing app progress/understanding records, practice answers, notes, reading checks, saved fundamentals labs and circuit-builder layouts. It does not introduce autosave for transient lab controls that were never persisted. Appearance preferences remain on the device. Guest work is imported only on request and never replaces existing account items. Account-local caches remain in that browser after signout and are inaccessible through guest mode; this is not a shared-device secure-erasure feature.

Clients have SELECT only through owner RLS. Writes go through a narrowly granted RPC that validates `auth.uid()`, owner, allowed key, size, quota and expected revision. Concurrent changes require the learner to choose a version. Tombstones propagate deletions. Up to 250 KB per item and 15 MB/10,000 items per account. Deleting an Auth user cascades saved progress and queued notifications; account deletion UI is not implemented.

Creation queues an owner notification, including email and creation time, even before verification. No answers or notes are emailed. The worker claims five records with ten-minute leases and stops retrying after five attempts. Inspect `signup_notifications` failures as an administrator and fix delivery before deliberately resetting attempts. Resend idempotency keys reduce duplicate delivery; an ambiguous send followed by a long outage can still require manual reconciliation. Email delivery is not an exactly-once guarantee.

## Local verification

- `node scripts/accounts/check-storage-sync.cjs`
- `npm install --prefix /tmp/gh-account-check --ignore-scripts @electric-sql/pglite@0.3.14`
- `node scripts/accounts/check-database.cjs`

The database test runs the real migration in local Postgres (PGlite), with mocked Auth schema and roles. It verifies RLS isolation, RPC access, null/wrong owner rejection, anonymous denial, queue privacy, notification leasing and revision conflicts. These checks do not replace end-to-end tests against the selected live project.

Documentation reviewed: https://supabase.com/docs/guides/auth/auth-email-passwordless ; https://supabase.com/docs/guides/database/postgres/row-level-security ; https://resend.com/docs/api-reference/emails/send-email . Supabase changelog reviewed 2026-10-26: current browser TLS unaffected by pending legacy-cipher removal; no relevant schema/API breaking changes identified.
