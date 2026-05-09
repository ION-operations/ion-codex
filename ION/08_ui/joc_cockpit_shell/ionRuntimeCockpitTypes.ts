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
  receipts: Record<string, unknown>[];
  authority_classes: IonAuthorityClass[];
  source_paths: Record<string, string>;
};
