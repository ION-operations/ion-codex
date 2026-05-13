-- ION operating runtime bootstrap.
--
-- Baseline-aligned to the manually created live ion_ops schema captured in:
-- supabase/live_schema_snapshots/ion_ops_live_schema_20260513.sql
--
-- Base migration only: schema, tables, indexes, triggers, RLS enablement, and
-- views. Broad private-cockpit authenticated read policies live in
-- 002_dev_private_cockpit_read_policies.sql. Typed guarded RPC operations live
-- in 003_ion_ops_authority_and_rpc.sql.

create schema if not exists ion_ops;

comment on schema ion_ops is 'ION operational mirror schema. ION files/Git/receipts remain truth; Supabase indexes selected runtime events for cockpit/query/realtime visibility.';

create extension if not exists pgcrypto;

create or replace function ion_ops.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create table if not exists ion_ops.automation_events (
  event_id uuid primary key default gen_random_uuid(),
  occurred_at timestamptz not null default now(),
  observed_at timestamptz not null default now(),
  source_system text not null default 'ion',
  event_type text not null,
  severity text not null default 'info'
    check (severity in ('debug', 'info', 'notice', 'warning', 'error', 'critical')),
  carrier_id text,
  carrier_type text,
  agent_tag text,
  branch_id text,
  context_instance_id text,
  packet_id text,
  correlation_id text,
  idempotency_key text,
  title text,
  summary text,
  payload jsonb not null default '{}'::jsonb,
  evidence_refs jsonb not null default '[]'::jsonb,
  source_posture jsonb not null default '{}'::jsonb,
  accepted_state_claim boolean not null default false,
  settlement_required boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

comment on table ion_ops.automation_events is 'Queryable mirror of ION automation/runtime events. Events are evidence, not accepted state.';

create table if not exists ion_ops.carrier_mount_receipts (
  mount_receipt_id uuid primary key default gen_random_uuid(),
  mounted_at timestamptz not null default now(),
  carrier_id text,
  carrier_type text not null,
  carrier_instance_id text,
  agent_tag text not null,
  conversation_tag text,
  context_instance_id text not null,
  branch_id text,
  parent_context_id text,
  current_packet text,
  model_lane text,
  loaded_refs jsonb not null default '[]'::jsonb,
  authority jsonb not null default '{}'::jsonb,
  write_scope jsonb not null default '[]'::jsonb,
  source_posture jsonb not null default '{}'::jsonb,
  return_target jsonb not null default '{}'::jsonb,
  persona_presentation jsonb not null default '{}'::jsonb,
  drift_findings jsonb not null default '[]'::jsonb,
  raw_receipt jsonb not null default '{}'::jsonb,
  accepted_state_authority boolean not null default false,
  settlement_required boolean not null default true,
  valid boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

comment on table ion_ops.carrier_mount_receipts is 'Mirror of ION carrier mount receipts. A carrier is not its name; it is a mounted context instance with source posture, authority, and return target.';

create table if not exists ion_ops.service_health_snapshots (
  snapshot_id uuid primary key default gen_random_uuid(),
  observed_at timestamptz not null default now(),
  service_name text not null,
  service_role text,
  carrier_id text,
  endpoint text,
  host text,
  port integer,
  pid integer,
  status text not null default 'unknown'
    check (status in ('ready', 'healthy', 'degraded', 'blocked', 'unknown', 'offline')),
  verdict text,
  version_line text,
  production_authority boolean not null default false,
  live_execution_authority boolean not null default false,
  health jsonb not null default '{}'::jsonb,
  findings jsonb not null default '[]'::jsonb,
  source_posture jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

comment on table ion_ops.service_health_snapshots is 'Point-in-time mirror of service health observations for ION cockpit/runtime visibility.';

create index if not exists automation_events_agent_tag_idx on ion_ops.automation_events (agent_tag);
create index if not exists automation_events_branch_id_idx on ion_ops.automation_events (branch_id);
create index if not exists automation_events_correlation_id_idx on ion_ops.automation_events (correlation_id);
create index if not exists automation_events_event_type_idx on ion_ops.automation_events (event_type);
create index if not exists automation_events_occurred_at_idx on ion_ops.automation_events (occurred_at desc);
create index if not exists automation_events_packet_id_idx on ion_ops.automation_events (packet_id);
create index if not exists automation_events_payload_gin_idx on ion_ops.automation_events using gin (payload);

create index if not exists carrier_mount_receipts_agent_tag_idx on ion_ops.carrier_mount_receipts (agent_tag);
create index if not exists carrier_mount_receipts_branch_id_idx on ion_ops.carrier_mount_receipts (branch_id);
create index if not exists carrier_mount_receipts_context_instance_id_idx on ion_ops.carrier_mount_receipts (context_instance_id);
create index if not exists carrier_mount_receipts_loaded_refs_gin_idx on ion_ops.carrier_mount_receipts using gin (loaded_refs);
create index if not exists carrier_mount_receipts_mounted_at_idx on ion_ops.carrier_mount_receipts (mounted_at desc);
create index if not exists carrier_mount_receipts_source_posture_gin_idx on ion_ops.carrier_mount_receipts using gin (source_posture);

create index if not exists service_health_snapshots_health_gin_idx on ion_ops.service_health_snapshots using gin (health);
create index if not exists service_health_snapshots_observed_at_idx on ion_ops.service_health_snapshots (observed_at desc);
create index if not exists service_health_snapshots_port_idx on ion_ops.service_health_snapshots (port);
create index if not exists service_health_snapshots_service_name_idx on ion_ops.service_health_snapshots (service_name);
create index if not exists service_health_snapshots_status_idx on ion_ops.service_health_snapshots (status);

drop trigger if exists automation_events_set_updated_at on ion_ops.automation_events;
create trigger automation_events_set_updated_at
before update on ion_ops.automation_events
for each row execute function ion_ops.set_updated_at();

drop trigger if exists carrier_mount_receipts_set_updated_at on ion_ops.carrier_mount_receipts;
create trigger carrier_mount_receipts_set_updated_at
before update on ion_ops.carrier_mount_receipts
for each row execute function ion_ops.set_updated_at();

drop trigger if exists service_health_snapshots_set_updated_at on ion_ops.service_health_snapshots;
create trigger service_health_snapshots_set_updated_at
before update on ion_ops.service_health_snapshots
for each row execute function ion_ops.set_updated_at();

alter table ion_ops.automation_events enable row level security;
alter table ion_ops.carrier_mount_receipts enable row level security;
alter table ion_ops.service_health_snapshots enable row level security;

create or replace view ion_ops.v_current_carrier_mounts
with (security_invoker = true)
as
select
  agent_tag,
  carrier_type,
  carrier_id,
  context_instance_id,
  branch_id,
  current_packet,
  accepted_state_authority,
  settlement_required,
  valid,
  mounted_at,
  source_posture,
  authority,
  persona_presentation
from ion_ops.carrier_mount_receipts
where valid = true
order by mounted_at desc;

create or replace view ion_ops.v_latest_service_health
with (security_invoker = true)
as
select distinct on (service_name)
  service_name,
  service_role,
  carrier_id,
  endpoint,
  host,
  port,
  status,
  verdict,
  production_authority,
  live_execution_authority,
  observed_at,
  health,
  findings
from ion_ops.service_health_snapshots
order by service_name, observed_at desc;

create or replace view ion_ops.v_recent_automation_events
with (security_invoker = true)
as
select
  event_id,
  occurred_at,
  source_system,
  event_type,
  severity,
  carrier_id,
  agent_tag,
  branch_id,
  packet_id,
  title,
  summary,
  accepted_state_claim,
  settlement_required
from ion_ops.automation_events
order by occurred_at desc
limit 100;

create or replace view ion_ops.v_cockpit_overview
with (security_invoker = true)
as
select
  now() as generated_at,
  (
    select count(*)
    from ion_ops.carrier_mount_receipts
    where valid = true
  ) as mounted_carrier_count,
  (
    select jsonb_agg(
      jsonb_build_object(
        'agent_tag', agent_tag,
        'carrier_type', carrier_type,
        'context_instance_id', context_instance_id,
        'current_packet', current_packet,
        'settlement_required', settlement_required,
        'mounted_at', mounted_at
      ) order by mounted_at desc
    )
    from ion_ops.v_current_carrier_mounts
  ) as mounted_carriers,
  (
    select jsonb_agg(
      jsonb_build_object(
        'service_name', service_name,
        'port', port,
        'status', status,
        'verdict', verdict,
        'observed_at', observed_at
      ) order by service_name
    )
    from ion_ops.v_latest_service_health
  ) as service_health,
  (
    select jsonb_agg(
      jsonb_build_object(
        'event_type', recent.event_type,
        'severity', recent.severity,
        'agent_tag', recent.agent_tag,
        'title', recent.title,
        'occurred_at', recent.occurred_at
      ) order by recent.occurred_at desc
    )
    from (
      select *
      from ion_ops.v_recent_automation_events
      order by occurred_at desc
      limit 10
    ) recent
  ) as recent_events,
  false as accepted_state_claim,
  true as settlement_required;
