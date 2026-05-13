-- ION operating runtime bootstrap.
--
-- Base migration only: schema, tables, indexes, triggers, RLS enablement,
-- service writer posture, and views. Broad private-cockpit authenticated read
-- policies live in 002_dev_private_cockpit_read_policies.sql.

create schema if not exists ion_ops;

create extension if not exists pgcrypto;

create or replace function ion_ops.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = timezone('utc', now());
  return new;
end;
$$;

create table if not exists ion_ops.automation_events (
  id uuid primary key default gen_random_uuid(),
  event_id text not null unique,
  event_type text not null,
  event_status text not null default 'recorded',
  severity text not null default 'info'
    check (severity in ('debug', 'info', 'notice', 'warning', 'error', 'critical')),
  source_system text not null default 'ion',
  source_carrier text,
  context_instance_id text,
  branch_id text,
  packet_id text,
  correlation_id text,
  idempotency_key text,
  summary text not null,
  details jsonb not null default '{}'::jsonb,
  evidence_refs jsonb not null default '[]'::jsonb,
  occurred_at timestamptz not null default timezone('utc', now()),
  recorded_at timestamptz not null default timezone('utc', now()),
  updated_at timestamptz not null default timezone('utc', now())
);

create table if not exists ion_ops.carrier_mount_receipts (
  id uuid primary key default gen_random_uuid(),
  receipt_id text not null unique,
  agent_tag text not null,
  carrier text not null,
  carrier_instance_id text,
  conversation_tag text,
  context_instance_id text not null,
  branch_id text,
  parent_context_id text,
  current_packet text,
  model_lane text,
  loaded_refs jsonb not null default '[]'::jsonb,
  authority jsonb not null default '{}'::jsonb,
  source_posture jsonb not null default '{}'::jsonb,
  return_target jsonb not null default '{}'::jsonb,
  persona_presentation jsonb not null default '{}'::jsonb,
  receipt_status text not null default 'candidate'
    check (receipt_status in ('candidate', 'active', 'superseded', 'archived', 'blocked')),
  mounted_at timestamptz not null default timezone('utc', now()),
  recorded_at timestamptz not null default timezone('utc', now()),
  updated_at timestamptz not null default timezone('utc', now())
);

create table if not exists ion_ops.service_health_snapshots (
  id uuid primary key default gen_random_uuid(),
  snapshot_id text not null unique,
  service_name text not null,
  service_owner text not null default 'ION',
  service_kind text,
  port integer check (port is null or (port > 0 and port <= 65535)),
  url text,
  status text not null default 'unknown'
    check (status in ('healthy', 'degraded', 'down', 'unknown', 'blocked')),
  status_detail text,
  health jsonb not null default '{}'::jsonb,
  observed_at timestamptz not null default timezone('utc', now()),
  recorded_at timestamptz not null default timezone('utc', now()),
  updated_at timestamptz not null default timezone('utc', now())
);

create unique index if not exists automation_events_idempotency_key_uidx
  on ion_ops.automation_events (idempotency_key)
  where idempotency_key is not null;

create index if not exists automation_events_occurred_at_idx
  on ion_ops.automation_events (occurred_at desc);

create index if not exists automation_events_packet_idx
  on ion_ops.automation_events (packet_id)
  where packet_id is not null;

create index if not exists carrier_mount_receipts_context_idx
  on ion_ops.carrier_mount_receipts (context_instance_id, mounted_at desc);

create index if not exists carrier_mount_receipts_branch_idx
  on ion_ops.carrier_mount_receipts (branch_id, mounted_at desc)
  where branch_id is not null;

create index if not exists service_health_snapshots_service_idx
  on ion_ops.service_health_snapshots (service_name, observed_at desc);

create index if not exists service_health_snapshots_status_idx
  on ion_ops.service_health_snapshots (status, observed_at desc);

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

drop policy if exists automation_events_service_write on ion_ops.automation_events;
create policy automation_events_service_write
on ion_ops.automation_events
for all
to service_role
using (true)
with check (true);

drop policy if exists carrier_mount_receipts_service_write on ion_ops.carrier_mount_receipts;
create policy carrier_mount_receipts_service_write
on ion_ops.carrier_mount_receipts
for all
to service_role
using (true)
with check (true);

drop policy if exists service_health_snapshots_service_write on ion_ops.service_health_snapshots;
create policy service_health_snapshots_service_write
on ion_ops.service_health_snapshots
for all
to service_role
using (true)
with check (true);

create or replace view ion_ops.v_current_carrier_mounts
with (security_invoker = true)
as
select distinct on (context_instance_id)
  receipt_id,
  agent_tag,
  carrier,
  carrier_instance_id,
  conversation_tag,
  context_instance_id,
  branch_id,
  parent_context_id,
  current_packet,
  model_lane,
  authority,
  source_posture,
  persona_presentation,
  receipt_status,
  mounted_at,
  recorded_at,
  updated_at
from ion_ops.carrier_mount_receipts
order by context_instance_id, mounted_at desc, recorded_at desc;

create or replace view ion_ops.v_latest_service_health
with (security_invoker = true)
as
select distinct on (service_name)
  snapshot_id,
  service_name,
  service_owner,
  service_kind,
  port,
  url,
  status,
  status_detail,
  health,
  observed_at,
  recorded_at,
  updated_at
from ion_ops.service_health_snapshots
order by service_name, observed_at desc, recorded_at desc;

create or replace view ion_ops.v_recent_automation_events
with (security_invoker = true)
as
select
  event_id,
  event_type,
  event_status,
  severity,
  source_system,
  source_carrier,
  context_instance_id,
  branch_id,
  packet_id,
  correlation_id,
  summary,
  details,
  evidence_refs,
  occurred_at,
  recorded_at
from ion_ops.automation_events
order by occurred_at desc, recorded_at desc
limit 200;

create or replace view ion_ops.v_cockpit_overview
with (security_invoker = true)
as
select
  timezone('utc', now()) as generated_at,
  (
    select count(*)
    from ion_ops.v_current_carrier_mounts
    where receipt_status in ('candidate', 'active')
  ) as current_carrier_count,
  (
    select count(*)
    from ion_ops.v_latest_service_health
    where status in ('healthy', 'degraded', 'down', 'blocked', 'unknown')
  ) as tracked_service_count,
  (
    select count(*)
    from ion_ops.v_latest_service_health
    where status in ('degraded', 'down', 'blocked')
  ) as attention_service_count,
  (
    select jsonb_agg(to_jsonb(h) order by h.service_name)
    from ion_ops.v_latest_service_health h
  ) as latest_service_health,
  (
    select jsonb_agg(to_jsonb(e) order by e.occurred_at desc)
    from (
      select *
      from ion_ops.v_recent_automation_events
      limit 20
    ) e
  ) as recent_automation_events;

grant usage on schema ion_ops to service_role;
grant select, insert, update, delete on all tables in schema ion_ops to service_role;

alter default privileges in schema ion_ops
grant select, insert, update, delete on tables to service_role;
