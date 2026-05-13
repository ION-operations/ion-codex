-- Development/bootstrap seed for the ION operating runtime.
--
-- Apply only when intentionally recreating the manually bootstrapped demo state.
-- Do not treat these rows as accepted production state.

insert into ion_ops.automation_events (
  event_id,
  event_type,
  event_status,
  severity,
  source_system,
  source_carrier,
  packet_id,
  idempotency_key,
  summary,
  details,
  evidence_refs
) values (
  'seed_ion_ops_bootstrap_001',
  'bootstrap_seed',
  'recorded',
  'notice',
  'ion',
  'local_repo_seed',
  'PCKT-ION-SUPABASE-OPERATING-RUNTIME-BOOTSTRAP-001',
  'seed_ion_ops_bootstrap_001',
  'ION ops runtime bootstrap seed inserted from repo-managed seed file.',
  '{"seed": true, "production_authority": false, "accepted_state_claim": false}'::jsonb,
  '["supabase/seed/001_ion_ops_bootstrap_seed.sql"]'::jsonb
) on conflict (event_id) do nothing;

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
) values
  (
    'seed_service_ion_mcp_preview_8765',
    'ION MCP preview',
    'ION',
    'mcp_http_preview',
    8765,
    'http://127.0.0.1:8765/health',
    'unknown',
    'Seed row only. Replace with live local service snapshot adapter output.',
    '{"seed": true, "canonical_port": 8765, "accepted_state_claim": false}'::jsonb
  ),
  (
    'seed_service_ion_action_gateway_8777',
    'ION Action Gateway',
    'ION',
    'custom_gpt_action_gateway',
    8777,
    'http://127.0.0.1:8777/health',
    'unknown',
    'Seed row only. Replace with live local service snapshot adapter output.',
    '{"seed": true, "canonical_port": 8777, "accepted_state_claim": false}'::jsonb
  ),
  (
    'seed_service_ion_local_cockpit_8788',
    'ION local cockpit',
    'ION',
    'local_cockpit',
    8788,
    'http://127.0.0.1:8788/health',
    'unknown',
    'Seed row only. Replace with live local service snapshot adapter output.',
    '{"seed": true, "canonical_port": 8788, "accepted_state_claim": false}'::jsonb
  )
on conflict (snapshot_id) do nothing;

insert into ion_ops.carrier_mount_receipts (
  receipt_id,
  agent_tag,
  carrier,
  carrier_instance_id,
  conversation_tag,
  context_instance_id,
  branch_id,
  current_packet,
  loaded_refs,
  authority,
  source_posture,
  return_target,
  persona_presentation,
  receipt_status
) values (
  'seed_carrier_mount_codex_local_ion_mason',
  'codex_local_ion_mason',
  'local_codex_cli',
  'local_dev',
  'supabase_operating_runtime_bootstrap',
  'ctx_seed_codex_local_ion_mason_supabase_runtime',
  'branch_seed_supabase_operating_runtime',
  'PCKT-ION-SUPABASE-OPERATING-RUNTIME-BOOTSTRAP-001',
  '[{"path": "supabase/migrations/001_initial_ion_ops.sql", "source_type": "repo", "sha256": null}]'::jsonb,
  '{"production_authority": false, "live_execution_authority": false, "accepted_state_authority": false, "settlement_required": true, "write_scope": ["supabase/", "ION/docs/setup/", "ION/02_architecture/"]}'::jsonb,
  '{"repo_observed": ["supabase/migrations/001_initial_ion_ops.sql"], "user_reported": ["manual ion_ops bootstrap already exists"], "inferred": [], "accepted_state_claim": false}'::jsonb,
  '{"parent_lane": "operator_chat", "settlement_inbox": "ION/05_context/current/context_settlement/inbox/", "accepted_state_claim": false}'::jsonb,
  '{"persona_mounted": false, "presentation_mode": "receipt_only", "hidden_reasoning_exposed": false}'::jsonb,
  'candidate'
) on conflict (receipt_id) do nothing;
