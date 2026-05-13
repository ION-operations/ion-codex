-- ION ion_ops API grants.
--
-- Purpose:
-- - Let the local backend-only ION adapter call typed ion_ops RPCs through
--   Supabase/PostgREST.
-- - Keep browser/public clients out of the write RPC lane.
-- - Preserve RLS and the separate ion_ops schema boundary.
--
-- Do not grant anon execute on write RPCs.
-- Do not move ion_ops functions to public.

create schema if not exists ion_ops;

grant usage on schema ion_ops to authenticated, service_role;
grant select on all tables in schema ion_ops to authenticated, service_role;

revoke execute on all functions in schema ion_ops from public, anon, authenticated;
grant execute on all functions in schema ion_ops to service_role;
grant execute on function ion_ops.ion_ops_rpc_authority() to authenticated, service_role;

alter default privileges in schema ion_ops
revoke execute on functions from public, anon, authenticated;

alter default privileges in schema ion_ops
grant execute on functions to service_role;
