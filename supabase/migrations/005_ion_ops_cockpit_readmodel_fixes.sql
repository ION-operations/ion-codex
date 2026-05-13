-- ION cockpit readmodel fixes.
--
-- Purpose:
-- - Expose stable ordering and identity fields from recent automation events.
-- - Keep Supabase as an operational mirror/readmodel, not accepted state.
-- - Preserve existing view column order where possible and append created_at
--   so PostgREST clients can order by it.

create schema if not exists ion_ops;

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
  settlement_required,
  created_at
from ion_ops.automation_events
order by created_at desc, occurred_at desc
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
        'event_id', recent.event_id,
        'event_type', recent.event_type,
        'severity', recent.severity,
        'carrier_id', recent.carrier_id,
        'agent_tag', recent.agent_tag,
        'branch_id', recent.branch_id,
        'packet_id', recent.packet_id,
        'title', recent.title,
        'summary', recent.summary,
        'occurred_at', recent.occurred_at,
        'created_at', recent.created_at,
        'accepted_state_claim', recent.accepted_state_claim,
        'settlement_required', recent.settlement_required
      ) order by recent.created_at desc, recent.occurred_at desc
    )
    from (
      select *
      from ion_ops.v_recent_automation_events
      order by created_at desc, occurred_at desc
      limit 10
    ) recent
  ) as recent_events,
  false as accepted_state_claim,
  true as settlement_required;
