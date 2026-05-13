-- ION typed operating RPC and authority guard layer.
--
-- Direct table writes remain service/internal posture. AI/browser carriers should
-- use these typed operations, which reject accepted-state and live/production
-- authority claims unless a future settlement-approved migration changes policy.

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
      'ion_ops_record_automation_event',
      'ion_ops_record_service_health_snapshot',
      'ion_ops_record_carrier_mount_receipt'
    )
  );
$$;

create or replace function ion_ops.ion_ops_record_automation_event(
  p_event_id text,
  p_event_type text,
  p_summary text,
  p_event_status text default 'recorded',
  p_severity text default 'info',
  p_source_system text default 'ion',
  p_source_carrier text default null,
  p_context_instance_id text default null,
  p_branch_id text default null,
  p_packet_id text default null,
  p_correlation_id text default null,
  p_idempotency_key text default null,
  p_details jsonb default '{}'::jsonb,
  p_evidence_refs jsonb default '[]'::jsonb
)
returns ion_ops.automation_events
language plpgsql
security definer
set search_path = ion_ops, public
as $$
declare
  row_out ion_ops.automation_events;
begin
  perform ion_ops.reject_accepted_state_claim(p_details);

  insert into ion_ops.automation_events (
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
    idempotency_key,
    summary,
    details,
    evidence_refs
  ) values (
    p_event_id,
    p_event_type,
    p_event_status,
    p_severity,
    p_source_system,
    p_source_carrier,
    p_context_instance_id,
    p_branch_id,
    p_packet_id,
    p_correlation_id,
    p_idempotency_key,
    p_summary,
    coalesce(p_details, '{}'::jsonb) || jsonb_build_object('accepted_state_claim', false),
    coalesce(p_evidence_refs, '[]'::jsonb)
  )
  on conflict (event_id) do update set
    event_status = excluded.event_status,
    severity = excluded.severity,
    summary = excluded.summary,
    details = excluded.details,
    evidence_refs = excluded.evidence_refs,
    updated_at = timezone('utc', now())
  returning * into row_out;

  return row_out;
end;
$$;

create or replace function ion_ops.ion_ops_record_service_health_snapshot(
  p_snapshot_id text,
  p_service_name text,
  p_status text,
  p_service_owner text default 'ION',
  p_service_kind text default null,
  p_port integer default null,
  p_url text default null,
  p_status_detail text default null,
  p_health jsonb default '{}'::jsonb
)
returns ion_ops.service_health_snapshots
language plpgsql
security definer
set search_path = ion_ops, public
as $$
declare
  row_out ion_ops.service_health_snapshots;
begin
  perform ion_ops.reject_accepted_state_claim(p_health);

  insert into ion_ops.service_health_snapshots (
    snapshot_id,
    service_name,
    service_owner,
    service_kind,
    port,
    url,
    status,
    status_detail,
    health
  ) values (
    p_snapshot_id,
    p_service_name,
    p_service_owner,
    p_service_kind,
    p_port,
    p_url,
    p_status,
    p_status_detail,
    coalesce(p_health, '{}'::jsonb) || jsonb_build_object('accepted_state_claim', false)
  )
  on conflict (snapshot_id) do update set
    service_name = excluded.service_name,
    service_owner = excluded.service_owner,
    service_kind = excluded.service_kind,
    port = excluded.port,
    url = excluded.url,
    status = excluded.status,
    status_detail = excluded.status_detail,
    health = excluded.health,
    updated_at = timezone('utc', now())
  returning * into row_out;

  return row_out;
end;
$$;

create or replace function ion_ops.ion_ops_record_carrier_mount_receipt(
  p_receipt_id text,
  p_agent_tag text,
  p_carrier text,
  p_context_instance_id text,
  p_carrier_instance_id text default null,
  p_conversation_tag text default null,
  p_branch_id text default null,
  p_parent_context_id text default null,
  p_current_packet text default null,
  p_model_lane text default null,
  p_loaded_refs jsonb default '[]'::jsonb,
  p_authority jsonb default '{}'::jsonb,
  p_source_posture jsonb default '{}'::jsonb,
  p_return_target jsonb default '{}'::jsonb,
  p_persona_presentation jsonb default '{}'::jsonb,
  p_receipt_status text default 'candidate'
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

  insert into ion_ops.carrier_mount_receipts (
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
    loaded_refs,
    authority,
    source_posture,
    return_target,
    persona_presentation,
    receipt_status
  ) values (
    p_receipt_id,
    p_agent_tag,
    p_carrier,
    p_carrier_instance_id,
    p_conversation_tag,
    p_context_instance_id,
    p_branch_id,
    p_parent_context_id,
    p_current_packet,
    p_model_lane,
    coalesce(p_loaded_refs, '[]'::jsonb),
    normalized_authority,
    coalesce(p_source_posture, '{}'::jsonb),
    coalesce(p_return_target, '{}'::jsonb),
    coalesce(p_persona_presentation, '{}'::jsonb) || jsonb_build_object('hidden_reasoning_exposed', false),
    p_receipt_status
  )
  on conflict (receipt_id) do update set
    carrier_instance_id = excluded.carrier_instance_id,
    current_packet = excluded.current_packet,
    model_lane = excluded.model_lane,
    loaded_refs = excluded.loaded_refs,
    authority = excluded.authority,
    source_posture = excluded.source_posture,
    return_target = excluded.return_target,
    persona_presentation = excluded.persona_presentation,
    receipt_status = excluded.receipt_status,
    updated_at = timezone('utc', now())
  returning * into row_out;

  return row_out;
end;
$$;

grant usage on schema ion_ops to authenticated, service_role;

grant execute on function ion_ops.assert_ion_authority(jsonb) to authenticated, service_role;
grant execute on function ion_ops.reject_accepted_state_claim(jsonb) to authenticated, service_role;
grant execute on function ion_ops.ion_ops_rpc_authority() to authenticated, service_role;
grant execute on function ion_ops.ion_ops_record_automation_event(text, text, text, text, text, text, text, text, text, text, text, text, jsonb, jsonb) to authenticated, service_role;
grant execute on function ion_ops.ion_ops_record_service_health_snapshot(text, text, text, text, text, integer, text, text, jsonb) to authenticated, service_role;
grant execute on function ion_ops.ion_ops_record_carrier_mount_receipt(text, text, text, text, text, text, text, text, text, text, jsonb, jsonb, jsonb, jsonb, jsonb, text) to authenticated, service_role;
