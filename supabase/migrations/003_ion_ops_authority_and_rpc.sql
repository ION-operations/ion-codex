-- ION typed operating RPC and authority guard layer.
--
-- Direct table writes remain internal. AI/browser carriers should use these
-- typed operations, which reject accepted-state and live/production authority
-- claims unless a future settlement-approved migration changes policy.

create schema if not exists ion_ops;

create or replace function ion_ops.assert_ion_authority(p_authority jsonb default '{}'::jsonb)
returns jsonb
language plpgsql
stable
set search_path = ion_ops, public
as $$
declare
  normalized jsonb;
begin
  normalized := jsonb_build_object(
    'production_authority', false,
    'live_execution_authority', false,
    'accepted_state_authority', false,
    'settlement_required', true
  ) || coalesce(p_authority, '{}'::jsonb);

  if coalesce((normalized ->> 'production_authority')::boolean, false) then
    raise exception 'ION Supabase RPC rejected production_authority=true';
  end if;
  if coalesce((normalized ->> 'live_execution_authority')::boolean, false) then
    raise exception 'ION Supabase RPC rejected live_execution_authority=true';
  end if;
  if coalesce((normalized ->> 'accepted_state_authority')::boolean, false) then
    raise exception 'ION Supabase RPC rejected accepted_state_authority=true';
  end if;

  return normalized;
end;
$$;

create or replace function ion_ops.reject_accepted_state_claim(p_payload jsonb default '{}'::jsonb)
returns void
language plpgsql
stable
set search_path = ion_ops, public
as $$
begin
  if coalesce((coalesce(p_payload, '{}'::jsonb) ->> 'accepted_state_claim')::boolean, false) then
    raise exception 'ION Supabase RPC rejected accepted_state_claim=true';
  end if;
end;
$$;

create or replace function ion_ops.ion_ops_rpc_authority()
returns jsonb
language sql
stable
set search_path = ion_ops, public
as $$
  select jsonb_build_object(
    'schema', 'ion_ops',
    'posture', 'typed_rpc_guarded_operations',
    'production_authority', false,
    'live_execution_authority', false,
    'accepted_state_authority', false,
    'direct_table_write_for_authenticated', false,
    'accepted_state_claim_default', false,
    'chatgpt_direct_db_mutation', false,
    'allowed_rpc', jsonb_build_array(
      'record_automation_event',
      'record_service_health_snapshot',
      'record_carrier_mount_receipt'
    )
  );
$$;

create or replace function ion_ops.record_automation_event(
  p_event_type text,
  p_title text default null,
  p_summary text default null,
  p_event_id uuid default gen_random_uuid(),
  p_occurred_at timestamptz default now(),
  p_observed_at timestamptz default now(),
  p_source_system text default 'ion',
  p_severity text default 'info',
  p_carrier_id text default null,
  p_carrier_type text default null,
  p_agent_tag text default null,
  p_branch_id text default null,
  p_context_instance_id text default null,
  p_packet_id text default null,
  p_correlation_id text default null,
  p_idempotency_key text default null,
  p_payload jsonb default '{}'::jsonb,
  p_evidence_refs jsonb default '[]'::jsonb,
  p_source_posture jsonb default '{}'::jsonb,
  p_settlement_required boolean default true
)
returns ion_ops.automation_events
language plpgsql
security definer
set search_path = ion_ops, public
as $$
declare
  row_out ion_ops.automation_events;
begin
  perform ion_ops.reject_accepted_state_claim(p_payload);
  perform ion_ops.reject_accepted_state_claim(p_source_posture);

  insert into ion_ops.automation_events (
    event_id,
    occurred_at,
    observed_at,
    source_system,
    event_type,
    severity,
    carrier_id,
    carrier_type,
    agent_tag,
    branch_id,
    context_instance_id,
    packet_id,
    correlation_id,
    idempotency_key,
    title,
    summary,
    payload,
    evidence_refs,
    source_posture,
    accepted_state_claim,
    settlement_required
  ) values (
    p_event_id,
    p_occurred_at,
    p_observed_at,
    p_source_system,
    p_event_type,
    p_severity,
    p_carrier_id,
    p_carrier_type,
    p_agent_tag,
    p_branch_id,
    p_context_instance_id,
    p_packet_id,
    p_correlation_id,
    p_idempotency_key,
    p_title,
    p_summary,
    coalesce(p_payload, '{}'::jsonb),
    coalesce(p_evidence_refs, '[]'::jsonb),
    coalesce(p_source_posture, '{}'::jsonb),
    false,
    coalesce(p_settlement_required, true)
  )
  on conflict (event_id) do update set
    observed_at = excluded.observed_at,
    severity = excluded.severity,
    title = excluded.title,
    summary = excluded.summary,
    payload = excluded.payload,
    evidence_refs = excluded.evidence_refs,
    source_posture = excluded.source_posture,
    settlement_required = excluded.settlement_required,
    updated_at = now()
  returning * into row_out;

  return row_out;
end;
$$;

create or replace function ion_ops.record_service_health_snapshot(
  p_service_name text,
  p_status text,
  p_snapshot_id uuid default gen_random_uuid(),
  p_observed_at timestamptz default now(),
  p_service_role text default null,
  p_carrier_id text default null,
  p_endpoint text default null,
  p_host text default null,
  p_port integer default null,
  p_pid integer default null,
  p_verdict text default null,
  p_version_line text default null,
  p_production_authority boolean default false,
  p_live_execution_authority boolean default false,
  p_health jsonb default '{}'::jsonb,
  p_findings jsonb default '[]'::jsonb,
  p_source_posture jsonb default '{}'::jsonb
)
returns ion_ops.service_health_snapshots
language plpgsql
security definer
set search_path = ion_ops, public
as $$
declare
  row_out ion_ops.service_health_snapshots;
begin
  if coalesce(p_production_authority, false) then
    raise exception 'ION Supabase RPC rejected production_authority=true';
  end if;
  if coalesce(p_live_execution_authority, false) then
    raise exception 'ION Supabase RPC rejected live_execution_authority=true';
  end if;
  perform ion_ops.reject_accepted_state_claim(p_health);
  perform ion_ops.reject_accepted_state_claim(p_source_posture);

  insert into ion_ops.service_health_snapshots (
    snapshot_id,
    observed_at,
    service_name,
    service_role,
    carrier_id,
    endpoint,
    host,
    port,
    pid,
    status,
    verdict,
    version_line,
    production_authority,
    live_execution_authority,
    health,
    findings,
    source_posture
  ) values (
    p_snapshot_id,
    p_observed_at,
    p_service_name,
    p_service_role,
    p_carrier_id,
    p_endpoint,
    p_host,
    p_port,
    p_pid,
    p_status,
    p_verdict,
    p_version_line,
    false,
    false,
    coalesce(p_health, '{}'::jsonb),
    coalesce(p_findings, '[]'::jsonb),
    coalesce(p_source_posture, '{}'::jsonb)
  )
  on conflict (snapshot_id) do update set
    observed_at = excluded.observed_at,
    service_name = excluded.service_name,
    service_role = excluded.service_role,
    carrier_id = excluded.carrier_id,
    endpoint = excluded.endpoint,
    host = excluded.host,
    port = excluded.port,
    pid = excluded.pid,
    status = excluded.status,
    verdict = excluded.verdict,
    version_line = excluded.version_line,
    production_authority = false,
    live_execution_authority = false,
    health = excluded.health,
    findings = excluded.findings,
    source_posture = excluded.source_posture,
    updated_at = now()
  returning * into row_out;

  return row_out;
end;
$$;

create or replace function ion_ops.record_carrier_mount_receipt(
  p_agent_tag text,
  p_carrier_type text,
  p_context_instance_id text,
  p_mount_receipt_id uuid default gen_random_uuid(),
  p_mounted_at timestamptz default now(),
  p_carrier_id text default null,
  p_carrier_instance_id text default null,
  p_conversation_tag text default null,
  p_branch_id text default null,
  p_parent_context_id text default null,
  p_current_packet text default null,
  p_model_lane text default null,
  p_loaded_refs jsonb default '[]'::jsonb,
  p_authority jsonb default '{}'::jsonb,
  p_write_scope jsonb default '[]'::jsonb,
  p_source_posture jsonb default '{}'::jsonb,
  p_return_target jsonb default '{}'::jsonb,
  p_persona_presentation jsonb default '{}'::jsonb,
  p_drift_findings jsonb default '[]'::jsonb,
  p_raw_receipt jsonb default '{}'::jsonb,
  p_settlement_required boolean default true,
  p_valid boolean default true
)
returns ion_ops.carrier_mount_receipts
language plpgsql
security definer
set search_path = ion_ops, public
as $$
declare
  normalized_authority jsonb;
  row_out ion_ops.carrier_mount_receipts;
begin
  normalized_authority := ion_ops.assert_ion_authority(p_authority);
  perform ion_ops.reject_accepted_state_claim(p_source_posture);
  perform ion_ops.reject_accepted_state_claim(p_return_target);
  perform ion_ops.reject_accepted_state_claim(p_persona_presentation);
  perform ion_ops.reject_accepted_state_claim(p_raw_receipt);

  insert into ion_ops.carrier_mount_receipts (
    mount_receipt_id,
    mounted_at,
    carrier_id,
    carrier_type,
    carrier_instance_id,
    agent_tag,
    conversation_tag,
    context_instance_id,
    branch_id,
    parent_context_id,
    current_packet,
    model_lane,
    loaded_refs,
    authority,
    write_scope,
    source_posture,
    return_target,
    persona_presentation,
    drift_findings,
    raw_receipt,
    accepted_state_authority,
    settlement_required,
    valid
  ) values (
    p_mount_receipt_id,
    p_mounted_at,
    p_carrier_id,
    p_carrier_type,
    p_carrier_instance_id,
    p_agent_tag,
    p_conversation_tag,
    p_context_instance_id,
    p_branch_id,
    p_parent_context_id,
    p_current_packet,
    p_model_lane,
    coalesce(p_loaded_refs, '[]'::jsonb),
    normalized_authority,
    coalesce(p_write_scope, '[]'::jsonb),
    coalesce(p_source_posture, '{}'::jsonb),
    coalesce(p_return_target, '{}'::jsonb),
    coalesce(p_persona_presentation, '{}'::jsonb) || jsonb_build_object('hidden_reasoning_exposed', false),
    coalesce(p_drift_findings, '[]'::jsonb),
    coalesce(p_raw_receipt, '{}'::jsonb),
    false,
    coalesce(p_settlement_required, true),
    coalesce(p_valid, true)
  )
  on conflict (mount_receipt_id) do update set
    mounted_at = excluded.mounted_at,
    carrier_id = excluded.carrier_id,
    carrier_instance_id = excluded.carrier_instance_id,
    conversation_tag = excluded.conversation_tag,
    current_packet = excluded.current_packet,
    model_lane = excluded.model_lane,
    loaded_refs = excluded.loaded_refs,
    authority = excluded.authority,
    write_scope = excluded.write_scope,
    source_posture = excluded.source_posture,
    return_target = excluded.return_target,
    persona_presentation = excluded.persona_presentation,
    drift_findings = excluded.drift_findings,
    raw_receipt = excluded.raw_receipt,
    accepted_state_authority = false,
    settlement_required = excluded.settlement_required,
    valid = excluded.valid,
    updated_at = now()
  returning * into row_out;

  return row_out;
end;
$$;

grant usage on schema ion_ops to authenticated, service_role;

grant execute on function ion_ops.assert_ion_authority(jsonb) to authenticated, service_role;
grant execute on function ion_ops.reject_accepted_state_claim(jsonb) to authenticated, service_role;
grant execute on function ion_ops.ion_ops_rpc_authority() to authenticated, service_role;
grant execute on function ion_ops.record_automation_event(text, text, text, uuid, timestamptz, timestamptz, text, text, text, text, text, text, text, text, text, text, jsonb, jsonb, jsonb, boolean) to authenticated, service_role;
grant execute on function ion_ops.record_service_health_snapshot(text, text, uuid, timestamptz, text, text, text, text, integer, integer, text, text, boolean, boolean, jsonb, jsonb, jsonb) to authenticated, service_role;
grant execute on function ion_ops.record_carrier_mount_receipt(text, text, text, uuid, timestamptz, text, text, text, text, text, text, text, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, boolean, boolean) to authenticated, service_role;
