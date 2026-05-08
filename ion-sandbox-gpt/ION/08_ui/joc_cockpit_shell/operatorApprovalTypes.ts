export type OperatorDecision = 'PENDING' | 'APPROVED' | 'DENIED' | 'EXPIRED';
export type ApprovalQueueVerdict =
  | 'QUEUED_FOR_OPERATOR_REVIEW'
  | 'BLOCKED_AUTHORIZATION_NOT_APPROVABLE'
  | 'BLOCKED_MISSING_AUTHORIZATION_EVIDENCE'
  | 'BLOCKED_MISSING_OPERATOR_APPROVAL_EVIDENCE'
  | 'OPERATOR_DENIED'
  | 'DRY_RUN_HANDOFF_READY'
  | 'EXPIRED_REQUIRES_REVIEW_REFRESH';

export interface OperatorApprovalQueueViewModel {
  version: 'V62_OPERATOR_APPROVAL_QUEUE_AND_DRY_RUN_HANDOFF';
  mission_id: string;
  authorization_view_model_ref: string;
  route_preview_id: string;
  selected_target: string;
  approval_verdict: ApprovalQueueVerdict;
  authority_scope: 'OPERATOR_APPROVAL_QUEUE_VIEW_MODEL_RECEIPT_ONLY';
  execution_mode: 'DRY_RUN_HANDOFF_ONLY' | 'VIEW_ONLY_BLOCKED';
  operator_decision: OperatorDecision;
  operator_id: string | null;
  requested_action_summary: string;
  estimated_cost_usd: number;
  estimated_latency_band: string;
  quality_band: string;
  view_surfaces: string[];
  approval_evidence_refs: string[];
  denial_reason: string | null;
  operator_reason: string;
  next_required_action: string;
  dry_run_handoff_preview: Record<string, unknown>;
  production_authority: false;
  live_dispatch_claim: false;
  external_model_call_authorized: false;
}

export const operatorApprovalFixture: OperatorApprovalQueueViewModel = {
  version: 'V62_OPERATOR_APPROVAL_QUEUE_AND_DRY_RUN_HANDOFF',
  mission_id: 'M-062',
  authorization_view_model_ref: 'V61_DISPATCH_AUTHORIZATION_VIEW_MODEL:M-061',
  route_preview_id: 'route-preview-v59-001',
  selected_target: 'gemini-cli',
  approval_verdict: 'QUEUED_FOR_OPERATOR_REVIEW',
  authority_scope: 'OPERATOR_APPROVAL_QUEUE_VIEW_MODEL_RECEIPT_ONLY',
  execution_mode: 'DRY_RUN_HANDOFF_ONLY',
  operator_decision: 'PENDING',
  operator_id: null,
  requested_action_summary: 'Approve dry-run handoff for supervised mission dispatch preview.',
  estimated_cost_usd: 0.02,
  estimated_latency_band: 'interactive_seconds',
  quality_band: 'high',
  view_surfaces: ['OPERATOR_APPROVAL_QUEUE', 'GOVERNOR_EVIDENCE_RAIL', 'APPROVAL_DECISION_CARD', 'DENIAL_REASON_LANE', 'DRY_RUN_HANDOFF_PREVIEW', 'NON_AUTHORITY_BOUNDARY_STRIP'],
  approval_evidence_refs: ['ION/04_packages/kernel/joc_dispatch_authorization_view_model.py', 'ION/03_registry/joc_dispatch_authorization_policy.yaml'],
  denial_reason: null,
  operator_reason: 'Authorization is approvable and queued for supervised operator decision.',
  next_required_action: 'Show operator the target, governors, evidence, blocked capabilities, and dry-run-only boundary.',
  dry_run_handoff_preview: {
    version: 'V62_OPERATOR_APPROVAL_QUEUE_AND_DRY_RUN_HANDOFF',
    mission_id: 'M-062',
    selected_target: 'gemini-cli',
    execution_mode: 'DRY_RUN_HANDOFF_ONLY',
    external_model_call_authorized: false,
    live_dispatch_claim: false,
    production_authority: false,
  },
  production_authority: false,
  live_dispatch_claim: false,
  external_model_call_authorized: false,
};
