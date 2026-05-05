export type AuthorizationVerdict =
  | 'AUTHORIZATION_PREVIEW_READY'
  | 'NEEDS_SUPERVISED_APPROVAL'
  | 'BLOCKED_BY_BUDGET'
  | 'BLOCKED_BY_API_RATE_LIMIT'
  | 'BLOCKED_BY_FORBIDDEN_CAPABILITY'
  | 'BLOCKED_BY_MISSING_GOVERNOR_EVIDENCE'
  | 'BLOCKED_BY_CLAIM_REVIEW'
  | 'BLOCKED_BY_PRODUCTION_BOUNDARY';

export type ApprovalMode =
  | 'AUTO_FORBIDDEN'
  | 'SUPERVISED_REQUIRED'
  | 'MANUAL_ONLY'
  | 'VIEW_ONLY_BLOCKED';

export interface DispatchAuthorizationViewModel {
  version: 'V61_DISPATCH_AUTHORIZATION_GOVERNOR_VERDICT_VIEW_MODEL';
  mission_id: string;
  route_preview_id: string;
  selected_target: string;
  compute_ring: string;
  access_method: string;
  task_class: string;
  claim_lane: string;
  authorization_verdict: AuthorizationVerdict;
  authority_scope: 'DISPATCH_AUTHORIZATION_VIEW_MODEL_RECEIPT_ONLY';
  approval_mode: ApprovalMode;
  budget_governor_verdict: string;
  api_rate_governor_verdict: string;
  capability_policy_verdict: string;
  estimated_cost_usd: number;
  estimated_latency_band: string;
  quality_band: string;
  blocked_capabilities: string[];
  route_factors: string[];
  evidence_refs: string[];
  operator_reason: string;
  next_required_action: string;
  production_authority: false;
  live_dispatch_claim: false;
}

export const dispatchAuthorizationFixture: DispatchAuthorizationViewModel = {
  version: 'V61_DISPATCH_AUTHORIZATION_GOVERNOR_VERDICT_VIEW_MODEL',
  mission_id: 'M-061',
  route_preview_id: 'route-preview-v59-001',
  selected_target: 'gemini-cli',
  compute_ring: 'RING_2_API_CLI_LOCAL',
  access_method: 'cli',
  task_class: 'context_route_analysis',
  claim_lane: 'C2',
  authorization_verdict: 'NEEDS_SUPERVISED_APPROVAL',
  authority_scope: 'DISPATCH_AUTHORIZATION_VIEW_MODEL_RECEIPT_ONLY',
  approval_mode: 'SUPERVISED_REQUIRED',
  budget_governor_verdict: 'BUDGET_WITHIN_LIMITS',
  api_rate_governor_verdict: 'API_RATE_WITHIN_LIMITS',
  capability_policy_verdict: 'CAPABILITY_ALLOWED_WITH_SUPERVISION',
  estimated_cost_usd: 0.02,
  estimated_latency_band: 'interactive_seconds',
  quality_band: 'high',
  blocked_capabilities: [],
  route_factors: ['cost', 'latency', 'quality', 'context_window'],
  evidence_refs: [
    'ION/03_registry/model_budget_policy.yaml',
    'ION/03_registry/api_rate_governor_policy.yaml',
    'ION/04_packages/kernel/joc_mission_dispatch_route_view_model.py',
  ],
  operator_reason:
    'Governors allow route preview to request supervised approval; no live dispatch authority is granted.',
  next_required_action:
    'Present to operator with budget/rate/capability evidence and require explicit approval before execution.',
  production_authority: false,
  live_dispatch_claim: false,
};
