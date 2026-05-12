export type IonAuthorityClass =
  | 'ACTIVE_RUNTIME_AUTHORITY'
  | 'ACCEPTED_TASK_RETURN'
  | 'PENDING_TASK_RETURN'
  | 'REJECTED_TASK_RETURN'
  | 'HUMAN_GATE_REQUIRED'
  | 'LEGACY_CONTEXT_WITNESS'
  | 'DONOR_REFERENCE'
  | 'FORBIDDEN_CAPABILITY'
  | string;

export type IonTimelineEvent = {
  time: string;
  source: string;
  event_type: string;
  status: string;
  path?: string;
  detail?: string;
};

export type IonLaneTimelineEvent = {
  id: string;
  message_id?: string;
  utterance_id?: string;
  atom_id?: string;
  timestamp: string;
  organ: string;
  requested_lane?: string;
  effective_lane?: string;
  lane_change_reason?: string;
  claim_class?: string;
  authority_verdict?: string;
  receipt_id?: string;
  repair_id?: string;
  source_path?: string;
  status: string;
  latency_ms?: number;
};

export type IonReceiptHydrationRecord = {
  receipt_id: string;
  repair_id?: string;
  utterance_id?: string;
  atom_id?: string;
  resolved_bubble_id?: string;
  resolution_method: string;
  confidence: string;
  claim_class?: string;
  authority_verdict?: string;
  latest_effective: boolean;
  supersedes?: string[];
  superseded_by?: string;
  source_receipt_path?: string;
  db_row_id?: string;
  warning?: string;
};

export type IonRuntimeDebugOverlay = {
  schema_id?: string;
  generated_at?: string;
  window_seconds?: number;
  sse?: Record<string, unknown>;
  render?: Record<string, unknown>;
  hydration?: Record<string, unknown>;
  kernel?: Record<string, unknown>;
  watcher?: Record<string, unknown>;
  status?: string;
};

export type IonSafeFullProjectPackage = {
  schema_id?: string;
  accepted?: boolean;
  zip_path?: string;
  zip_sha256?: string;
  production_authority?: boolean;
  zip_root_audit?: {
    verdict?: string;
    archive_root_mode?: string;
    wrapped_root_prefix?: string | null;
    missing_at_archive_root?: string[];
  };
  preservation_report?: {
    files_before?: number;
    files_after?: number;
    added_files?: number;
    modified_files?: number;
    removed_files?: number;
    protected_removed_files?: number;
    unexpected_removed_files?: number;
    packaging_verdict?: string;
  };
};

export type IonV72McpDonorReconciliation = {
  schema_id?: string;
  version_line?: string;
  reconciliation_verdict?: string;
  donor_scope?: string;
  restored_donor_surface_count?: number;
  missing_donor_surface_count?: number;
  forbidden_runtime_file_count?: number;
  cursor_bridge_preserved?: boolean;
  donor_runtime_receipts_restored?: boolean;
  live_execution_authority?: boolean;
  production_authority?: boolean;
};

export type IonFrontDoorProofTrace = {
  schema_id?: string;
  trace_id?: string;
  generated_at?: string;
  projection_mode?: string;
  session_id?: string;
  proof_complete?: boolean;
  verdict?: string;
  operator_message?: string;
  controlled_system_output?: string;
  boundary_proof?: Record<string, unknown>;
  steward_verdict?: Record<string, unknown>;
  receipts?: Record<string, unknown>;
  stage_sequence?: Array<{
    sequence?: number;
    stage?: string;
    organ?: string;
    status?: string;
    artifact_id?: string;
    witness_path?: string;
    receipt_id?: string;
    detail?: string;
  }>;
  witness_paths?: string[];
  missing_witness_paths?: string[];
  production_authority?: boolean;
  live_execution_authority?: boolean;
};

export type IonSpawnRow = {
  index: string | number;
  role: string;
  spawn: boolean;
  status: string;
  context_package_path?: string;
  context_load_receipt_path?: string;
  authority_class?: IonAuthorityClass;
  return_recorded?: boolean;
};

export type IonTaskReturn = {
  role: string;
  index: string | number;
  decision: string;
  path?: string;
  authority_class?: IonAuthorityClass;
};

export type IonQueueState = {
  operator_messages: Record<string, unknown>[];
  human_gates: Record<string, unknown>[];
  steward_integration: Record<string, unknown>[];
};

export type IonLocalServiceStatus = {
  schema_id: 'ion.local_service_status.v1';
  generated_at: string;
  verdict: string;
  status: string;
  probe_http: boolean;
  service_count: number;
  ready_count: number;
  not_running_count: number;
  degraded_count: number;
  missing_template_count: number;
  services: Array<{
    service_id: string;
    unit_name: string;
    role: string;
    local_url?: string | null;
    health_url?: string | null;
    public_url?: string | null;
    tunnel_name?: string | null;
    status: string;
    findings: string[];
    production_authority: boolean;
    live_execution_authority: boolean;
  }>;
  install_authority: boolean;
  production_authority: boolean;
  live_execution_authority: boolean;
};

export type IonHelixionJocRebuildProjection = {
  schema_id?: string;
  status?: string;
  decision?: string;
  master_plan_path?: string;
  registry_path?: string;
  current_plan_path?: string;
  master_plan_present?: boolean;
  registry_present?: boolean;
  current_plan_present?: boolean;
  ready_for_phase_1?: boolean;
  phase_0_gate?: Record<string, unknown>;
  product_roles?: Record<string, string>;
  required_surfaces?: string[];
  canonical_zones?: string[];
  canonical_object_types?: string[];
  allowed_v1_capabilities?: string[];
  forbidden_v1_capabilities?: string[];
  next_build_sequence?: string[];
  source_authorities?: string[];
  orchestration_context_package?: Record<string, unknown>;
  local_shell?: Record<string, unknown>;
  react_bundle?: Record<string, unknown>;
  development_urls?: string[];
  latest_capsule_entry_id?: string;
  latest_history_receipt?: string;
  latest_codex_solo_checkpoint_id?: string;
  authority_posture?: Record<string, unknown>;
  production_authority?: boolean;
  live_execution_authority?: boolean;
  unrestricted_browser_control?: boolean;
};

export type IonServiceConsoleModel = {
  schema_id?: 'ion.cockpit_service_console.v1' | string;
  ok?: boolean;
  verdict?: string;
  headline?: string;
  required_issue_count?: number;
  warning_count?: number;
  generated_at?: string;
  shell_root?: string;
  operator_message?: string;
  production_authority?: boolean;
  live_execution_authority?: boolean;
  services?: Array<{
    id?: string;
    unit?: string;
    label?: string;
    role?: string;
    critical?: boolean;
    fix_label?: string;
    active?: boolean;
    status?: string;
    finding?: string;
    severity?: string;
    restart_confirmation?: string;
  }>;
};

export type IonChatgptBrowserMcpSummary = {
  schema_id?: 'ion.chatgpt_browser_mcp_cockpit_summary.v1' | string;
  connector_contract_verdict?: string;
  http_preview_verdict?: string;
  transport_state?: string;
  active_connector_url?: string;
  carrier_id?: string;
  project_facing_callsign?: string;
  callsign_authority?: string;
  callsign_decision_receipt?: string;
  tool_count?: number;
  first_parity_tools_present?: string[];
  visibility_tools_present?: string[];
  agent_invocation_tools_present?: string[];
  carrier_message_count?: number;
  codex_work_request_count?: number;
  latest_carrier_messages?: Array<Record<string, unknown>>;
  latest_task_returns?: Array<Record<string, unknown>>;
  latest_agent_invocations?: Array<Record<string, unknown>>;
  latest_artifact_receipts?: Array<Record<string, unknown>>;
  latest_decisions?: Array<Record<string, unknown>>;
  codex_queue_runner?: Record<string, unknown>;
  agent_invocation_broker?: Record<string, unknown>;
  artifact_upload_status_counts?: Record<string, number>;
  adapter_gap_not_core_failure?: boolean;
  production_authority?: boolean;
  live_execution_authority?: boolean;
};

export type IonCodexCapsuleChatSummary = {
  schema_id?: 'ion.codex_capsule_chat_cockpit_summary.v1' | string;
  model_path?: string;
  model_present?: boolean;
  verdict?: string;
  generated_at?: string;
  product?: Record<string, unknown>;
  product_mode?: Record<string, unknown>;
  authority?: Record<string, unknown>;
  conversation_summary?: Record<string, unknown>;
  turn_trace_count?: number;
  queued_request_count?: number;
  runner_active?: boolean;
  response_run_count?: number;
  latest_response_status?: string;
  latest_response_runs?: Array<Record<string, unknown>>;
  latest_work_requests?: Array<Record<string, unknown>>;
  latest_task_returns?: Array<Record<string, unknown>>;
  codex_queue_path?: string;
  capsule?: {
    ok?: boolean;
    path?: string;
    entry_count?: number;
    context_line_limit?: number;
    recent_rows?: Array<Record<string, unknown>>;
  };
  mini?: {
    ok?: boolean;
    role?: string;
    line_count?: number;
    max_lines?: number;
    text_excerpt?: string;
  };
  hot_context?: Record<string, unknown>;
  memory_visualization?: Record<string, unknown>;
  chat_engine?: Record<string, unknown>;
  skills?: Record<string, unknown>;
  response_carrier?: Record<string, unknown>;
  execution_bridge?: Record<string, unknown>;
  production_authority?: boolean;
  live_execution_authority?: boolean;
  secrets_authority?: boolean;
};

export type IonExtensionMicroShellSummary = {
  schema_id?: 'ion.extension_micro_shell_cockpit_summary.v1' | string;
  status?: string;
  extension_root?: string;
  manifest?: Record<string, unknown>;
  agent_lane_contract?: Record<string, unknown>;
  portable_companion?: Record<string, unknown>;
  page_perception?: {
    domain_registry_path?: string;
    task_return_path?: string;
    domain_registry_present?: boolean;
    task_return_present?: boolean;
    domain_count?: number;
    domains?: Array<Record<string, unknown>>;
    task_return_headings?: string[];
  };
  queue_pack_authoring?: Record<string, unknown>;
  current_v1_authority?: Record<string, unknown>;
  safety_law?: string[];
  required_boundaries?: string[];
  implementation_gates?: string[];
  non_claim_boundaries?: string[];
  production_authority?: boolean;
  live_execution_authority?: boolean;
  unrestricted_browser_control?: boolean;
  silent_browser_send_authority?: boolean;
};

export type IonDocsProjectsPackagesSummary = {
  schema_id?: 'ion.docs_projects_packages_cockpit_summary.v1' | string;
  status?: string;
  context_packages?: {
    path?: string;
    generated_at?: string;
    package_count?: number;
    selected_by_default?: string[];
    package_types?: Record<string, number>;
    packages?: Array<Record<string, unknown>>;
    production_authority?: boolean;
    live_execution_authority?: boolean;
  };
  project_favorites?: Array<Record<string, unknown>>;
  artifact_packages?: {
    root?: string;
    zip_count_visible?: number;
    latest_zips?: Array<Record<string, unknown>>;
    auto_zip_drop_authority?: boolean;
    drop_zone_execution_authority?: boolean;
  };
  safe_full_project_package?: Record<string, unknown>;
  custom_gpt_context?: Record<string, unknown>;
  operator_model?: Record<string, unknown>;
  production_authority?: boolean;
  live_execution_authority?: boolean;
  unrestricted_filesystem_mutation?: boolean;
};

export type IonCockpitViewModel = {
  schema_id: 'ion.cockpit_view_model.v1';
  generated_at: string;
  runtime: {
    status: string;
    shell_root: string;
    mode: string;
    version: string;
    blocked: boolean;
    audit_findings: unknown[];
  };
  top_bar: {
    objective: string;
    carrier_status: string;
    hook_status: string;
    gate_count: number;
    spawn_count: number;
    plan_spawn_count?: number;
    deferred_spawn_count?: number;
    spawn_rows_total: number;
    execution_bundle_materialized?: boolean | null;
    return_counts: Record<string, number>;
    steward_queue_count: number;
    operator_queue_pending: number;
    local_service_status?: string;
    local_service_count?: number;
    local_service_missing_template_count?: number;
    helixion_rebuild_status?: string;
    helixion_rebuild_ready_for_phase_1?: boolean;
    browser_carrier_message_count?: number;
    codex_work_request_count?: number;
    action_gateway_tool_count?: number;
    action_gateway_transport_state?: string;
    codex_capsule_chat_verdict?: string;
    codex_capsule_chat_turn_count?: number;
    codex_capsule_chat_response_run_count?: number;
    extension_version?: string;
    extension_panel_count?: number;
    page_perception_domain_count?: number;
    context_package_count?: number;
    artifact_package_count?: number;
  };
  queues: IonQueueState;
  agents: {
    spawn_rows: IonSpawnRow[];
    context_packages: Record<string, unknown>[];
    returns: IonTaskReturn[];
  };
  timeline: IonTimelineEvent[];
  front_door_proof_trace?: IonFrontDoorProofTrace;
  lane_timeline?: {
    schema_id?: string;
    event_count?: number;
    events?: IonLaneTimelineEvent[];
    messages?: Record<string, unknown>[];
  };
  receipt_hydration?: {
    schema_id?: string;
    receipt_count?: number;
    unresolved_count?: number;
    hydration_conflict_count?: number;
    records?: IonReceiptHydrationRecord[];
  };
  runtime_debug_overlay?: IonRuntimeDebugOverlay;
  safe_full_project_package?: IonSafeFullProjectPackage;
  v72_mcp_donor_reconciliation?: IonV72McpDonorReconciliation;
  local_services?: IonLocalServiceStatus;
  service_console?: IonServiceConsoleModel;
  helixion_joc_rebuild?: IonHelixionJocRebuildProjection;
  chatgpt_browser_mcp?: IonChatgptBrowserMcpSummary;
  codex_capsule_chat?: IonCodexCapsuleChatSummary;
  extension_micro_shell?: IonExtensionMicroShellSummary;
  docs_projects_packages?: IonDocsProjectsPackagesSummary;
  receipts: Record<string, unknown>[];
  authority_classes: IonAuthorityClass[];
  source_paths: Record<string, string>;
};
