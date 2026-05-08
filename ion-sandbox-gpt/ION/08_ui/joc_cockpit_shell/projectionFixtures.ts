import type { CognitiveRouteViewModel, MissionDispatchRouteViewModel, ReactiveStreamEvent } from './reactiveTypes';

export type ClaimLane = 'C0' | 'C1' | 'C2' | 'C3' | 'C4' | 'C5';

export type ReceiptSummary = {
  id: string;
  family: string;
  claimLane: ClaimLane;
  verdict: string;
  authorityScope: string;
  evidenceRefs: string[];
  repairRequired: boolean;
};

export type AutomationEvent = {
  id: string;
  time: string;
  loop: string;
  phase: string;
  status: 'ok' | 'watch' | 'blocked';
  detail: string;
};

export type CockpitProjectionFixture = {
  version: string;
  stewardState: string;
  oracleMode: 'AUTO' | 'SUPERVISED' | 'MANUAL' | 'OFFLINE';
  activeSurface: string;
  closureVerdict: string;
  receiptSummaries: ReceiptSummary[];
  automationEvents: AutomationEvent[];
  reactiveEvents: ReactiveStreamEvent[];
  cognitiveRoute: CognitiveRouteViewModel;
  missionRoute: MissionDispatchRouteViewModel;
  blockedCapabilities: string[];
};

export const v57ReactiveEvents: ReactiveStreamEvent[] = [
  { eventId: 'v57-evt-visual-001', occurredAt: '18:12:01', loopId: 'VISUAL_ISSUE_CLOSURE_LOOP', phase: 'closure_render', status: 'OK', claimLane: 'C0', renderedSurface: 'VISUAL_EVIDENCE_LENS', authorityScope: 'VISUAL_RUN_TO_DIAGNOSIS_CLOSURE_RECEIPT_ONLY', evidenceRefs: ['V45 diagnosis receipt', 'V48 before-after receipt', 'V53 local browser run receipt', 'V54 closure binding receipt'], repairRequired: false, blockedCapabilities: [], detail: 'Visual closure may be rendered as scoped evidence because run and diagnosis lineage agree.' },
  { eventId: 'v57-evt-context-001', occurredAt: '18:12:09', loopId: 'CONTEXT_PROJECTION_LOOP', phase: 'surface_projection', status: 'OK', claimLane: 'C2', renderedSurface: 'CONTEXT_GRAPH_COGNITIVE_EXPLORER', authorityScope: 'UI_WORK_SURFACE_PROJECTION_RECEIPT_ONLY', evidenceRefs: ['V55 projection receipt', 'V56 component contract'], repairRequired: false, blockedCapabilities: [], detail: 'Projection surfaces are mapped into cockpit regions for operator inspection.' },
  { eventId: 'v57-evt-mission-001', occurredAt: '18:12:17', loopId: 'MISSION_DISPATCH_LOOP', phase: 'route_preview', status: 'WATCH', claimLane: 'C2', renderedSurface: 'MISSION_DISPATCH_AND_MODEL_ROUTE_PANEL', authorityScope: 'MISSION_ROUTE_PREVIEW_ONLY', evidenceRefs: ['JOC mission lifecycle doctrine', 'compute ring routing plan'], repairRequired: false, blockedCapabilities: [], detail: 'Route plan may be previewed, but dispatch remains unmounted in this branch.' },
  { eventId: 'v57-evt-session-001', occurredAt: '18:12:24', loopId: 'SESSION_HEALTH_LOOP', phase: 'browser_authority_gate', status: 'BLOCKED', claimLane: 'C1', renderedSurface: 'BROWSER_SESSION_AUTOMATION_OVERLAY', authorityScope: 'BROWSER_AUTOMATION_VISIBILITY_ONLY', evidenceRefs: [], repairRequired: false, blockedCapabilities: ['credential_access', 'form_submission', 'persistent_dom_mutation', 'production_visual_automation'], detail: 'Session overlay can display injection and extraction zones but cannot operate credentials or submit forms.' },
  { eventId: 'v57-evt-repair-001', occurredAt: '18:12:31', loopId: 'CONVERSATIONAL_REPAIR_LOOP', phase: 'artifact_repair_visibility', status: 'REPAIR', claimLane: 'C3', renderedSurface: 'CONVERSATIONAL_REPAIR_QUEUE', authorityScope: 'CONVERSATIONAL_REPAIR_QUEUE_VISIBILITY_ONLY', evidenceRefs: ['V42 conversational repair doctrine', 'current UI branch continuation obligation'], repairRequired: true, blockedCapabilities: [], detail: 'Chat correction and artifact correction remain visibly distinct in the cockpit queue.' },
  { eventId: 'v57-evt-cost-001', occurredAt: '18:12:38', loopId: 'MODEL_COST_QUALITY_LOOP', phase: 'compute_ring_score', status: 'WATCH', claimLane: 'C2', renderedSurface: 'COMPUTE_AND_COST_ROUTER', authorityScope: 'ROUTING_RECOMMENDATION_ONLY', evidenceRefs: ['JOC compute ring design', 'model route policy placeholder'], repairRequired: false, blockedCapabilities: [], detail: 'Cost and quality route scoring is display-only until live dispatch drivers are mounted.' },
  { eventId: 'v59-evt-route-001', occurredAt: '18:13:02', loopId: 'MISSION_DISPATCH_LOOP', phase: 'three_ring_route_preview', status: 'WATCH', claimLane: 'C2', renderedSurface: 'MISSION_DISPATCH_PANEL', authorityScope: 'MISSION_DISPATCH_ROUTE_VIEW_MODEL_RECEIPT_ONLY', evidenceRefs: ['V58 context route receipt', 'V59 route factors', 'V59 approval gate'], repairRequired: false, blockedCapabilities: ['live_external_model_dispatch', 'paid_cloud_launch', 'credential_access'], detail: 'Mission dispatch is rendered as preview-only with primary target, fallbacks, cost/latency bands, and supervised approval gate.' },
];

export const v58CognitiveRoute: CognitiveRouteViewModel = {
  query: 'Explain the reactive OS stream and automation overlay path.',
  verdict: 'VALID_CONTEXT_ROUTE_VIEW_MODEL',
  routeClasses: ['EXACT_SYMBOL', 'FILE_PATH', 'DEPENDENCY_EDGE', 'RECEIPT_FAMILY', 'FALLBACK_BOUNDARY'],
  viewSurfaces: ['COGNITIVE_EXPLORER', 'INFINITE_CONTEXT_COMMAND_PALETTE', 'SELECTED_CONTEXT_LENS', 'STRUCTURAL_BLUEPRINT_VIEW', 'DEPENDENCY_WEB_VIEW', 'SOURCE_LINE_CITATION_RAIL', 'ROUTE_REASONING_PANEL'],
  selectedNodes: [
    { nodeId: 'node.kernel.joc_reactive_os_stream_view_model', label: 'Reactive OS Stream verifier', nodeClass: 'FUNCTION', path: 'ION/04_packages/kernel/joc_reactive_os_stream_view_model.py', symbol: 'validate_reactive_os_stream_view_model', lineRange: 'L1-L220', confidence: 'SOURCE_INDEXED' },
    { nodeId: 'node.ui.ReactiveOsStreamPanel', label: 'Reactive OS Stream panel', nodeClass: 'UI_COMPONENT', path: 'ION/08_ui/joc_cockpit_shell/ReactiveOsStreamPanel.tsx', symbol: 'ReactiveOsStreamPanel', lineRange: 'L1-L80', confidence: 'SOURCE_INDEXED' },
    { nodeId: 'node.ui.AutomationOverlayPanel', label: 'Browser automation overlay panel', nodeClass: 'UI_COMPONENT', path: 'ION/08_ui/joc_cockpit_shell/AutomationOverlayPanel.tsx', symbol: 'AutomationOverlayPanel', lineRange: 'L1-L90', confidence: 'SOURCE_INDEXED' },
    { nodeId: 'node.protocol.reactive_os_stream', label: 'Reactive OS stream protocol', nodeClass: 'PROTOCOL', path: 'ION/02_architecture/ION_JOC_REACTIVE_OS_STREAM_AND_AUTOMATION_VIEW_MODEL_PROTOCOL.md', symbol: 'V57 protocol', lineRange: 'L1-L140', confidence: 'RECEIPT_BACKED' },
  ],
  dependencyEdges: [
    { source: 'node.kernel.joc_reactive_os_stream_view_model', target: 'node.ui.ReactiveOsStreamPanel', edgeClass: 'projects_to', evidenceRef: 'V57 stream fixture' },
    { source: 'node.ui.AutomationOverlayPanel', target: 'node.protocol.reactive_os_stream', edgeClass: 'conforms_to', evidenceRef: 'V57 protocol required surfaces' },
  ],
  sourceCitations: ['ION/04_packages/kernel/joc_reactive_os_stream_view_model.py:L1-L220', 'ION/08_ui/joc_cockpit_shell/ReactiveOsStreamPanel.tsx:L1-L80', 'ION/08_ui/joc_cockpit_shell/AutomationOverlayPanel.tsx:L1-L90', 'ION/02_architecture/ION_JOC_REACTIVE_OS_STREAM_AND_AUTOMATION_VIEW_MODEL_PROTOCOL.md:L1-L140'],
  routeReasoning: 'Exact indexed symbols and files satisfy the route before semantic fallback. Dependency edges explain how kernel receipts project into cockpit components.',
  injectionPreview: 'Preview only: include V57 stream verifier, ReactiveOsStreamPanel, AutomationOverlayPanel, and protocol lines. Dispatch is not executed in V58.',
  blockedCapabilities: ['production_authority', 'external_model_dispatch', 'browser_session_mutation', 'credential_access', 'source_summary_rewrite', 'canonical_graph_write', 'unrestricted_agent_activation', 'live_ui_claim'],
};

export const v59MissionRoute: MissionDispatchRouteViewModel = {
  missionId: 'M-V59-ION-JOC-DISPATCH-ROUTE',
  missionTitle: 'Route V58 cognitive context into supervised mission dispatch lanes',
  taskClass: 'UI_ARCHITECTURE_AND_RUNTIME_VIEW_MODEL',
  verdict: 'ROUTE_PREVIEW_READY',
  authorityScope: 'MISSION_DISPATCH_ROUTE_VIEW_MODEL_RECEIPT_ONLY',
  contextRouteRef: 'V58_COGNITIVE_EXPLORER_ROUTE_VIEW_MODEL_RECEIPT',
  primaryTarget: { targetId: 'target.gpt.reasoning_supervised', displayName: 'GPT reasoning lane', computeRing: 'RING_2_API_CLI_LOCAL', accessMethod: 'api', status: 'PRIMARY_RECOMMENDED', capabilityTags: ['architectural_reasoning', 'code_review', 'receipt_synthesis'], costBand: 'MEDIUM', latencyBand: 'INTERACTIVE_SECONDS', qualityBand: 'HIGH', riskNotes: ['requires supervised approval before live dispatch'] },
  fallbackTargets: [
    { targetId: 'target.browser.chatgpt_manual', displayName: 'ChatGPT browser session', computeRing: 'RING_1_BROWSER_SESSION', accessMethod: 'browser', status: 'SUPERVISED_ONLY', capabilityTags: ['interactive_chat', 'visual_session_context', 'manual_injection'], costBand: 'SUBSCRIPTION_INCLUDED', latencyBand: 'INTERACTIVE_10_60S', qualityBand: 'HIGH_VARIANT', riskNotes: ['browser mutation remains blocked in V59'] },
    { targetId: 'target.local.small_classifier', displayName: 'Local small-model classifier', computeRing: 'RING_2_API_CLI_LOCAL', accessMethod: 'local', status: 'FALLBACK_READY', capabilityTags: ['classification', 'cheap_triage', 'privacy_preserving'], costBand: 'FREE_LOCAL', latencyBand: 'LOW_SECONDS', qualityBand: 'BOUNDED_LOW_RISK', riskNotes: [] },
    { targetId: 'target.vertex.heavy_cloud', displayName: 'Cloud heavy compute lane', computeRing: 'RING_3_CLOUD_COMPUTE', accessMethod: 'cloud_vm', status: 'SUPERVISED_ONLY', capabilityTags: ['heavy_simulation', 'large_batch', 'future_training'], costBand: 'HIGH_PAID_APPROVAL_REQUIRED', latencyBand: 'MINUTES_TO_HOURS', qualityBand: 'SPECIALIZED_HEAVY', riskNotes: ['paid launch remains blocked without explicit operator approval'] },
  ],
  routeFactors: [
    { factorId: 'TASK_CLASS', value: 'UI_ARCHITECTURE_AND_RUNTIME_VIEW_MODEL', rationale: 'The mission asks for ION/JOC UI-runtime synthesis and scaffold work.' },
    { factorId: 'CONTEXT_SIZE', value: 'MEDIUM_PROJECT_ROUTE', rationale: 'V58 selected exact files and citations; no full-repo prompt is needed.' },
    { factorId: 'QUALITY_REQUIREMENT', value: 'HIGH', rationale: 'Architecture and runtime law should be handled by a strong reasoning lane.' },
    { factorId: 'LATENCY_REQUIREMENT', value: 'INTERACTIVE', rationale: 'The branch is being developed in a live conversation loop.' },
    { factorId: 'COST_SENSITIVITY', value: 'CONTROLLED', rationale: 'Use already-mounted local/interactive lanes before paid cloud.' },
    { factorId: 'CAPABILITY_MATCH', value: 'REASONING_PLUS_CODE_PATCH', rationale: 'Primary lane must reason about architecture and produce project files/tests.' },
    { factorId: 'RISK_CLASS', value: 'C2_DESIGN_CANDIDATE', rationale: 'Route preview is a design/runtime candidate, not production dispatch.' },
    { factorId: 'FALLBACK_AVAILABILITY', value: 'THREE_RING_FALLBACK_VISIBLE', rationale: 'Browser, local/API/CLI, and cloud lanes are all represented.' },
  ],
  viewSurfaces: ['MISSION_DISPATCH_PANEL', 'MODEL_ROUTE_MATRIX', 'COMPUTE_RING_SELECTOR', 'COST_LATENCY_QUALITY_BAND', 'CAPABILITY_MATCH_PANEL', 'FALLBACK_CHAIN_PANEL', 'HUMAN_APPROVAL_GATE', 'DISPATCH_RECEIPT_PREVIEW'],
  approvalGate: 'SUPERVISED_APPROVAL_REQUIRED',
  routeReasoning: 'The V58 route has exact context, so V59 previews a supervised mission dispatch plan. A high-quality reasoning/code lane is primary; browser, local, and cloud lanes remain visible as fallbacks without enabling live dispatch.',
  dispatchReceiptPreview: 'If approved by a later live driver branch, the dispatch receipt must record mission id, selected target, context route ref, cost/latency estimate, operator approval, response extraction status, and return routing.',
  blockedCapabilities: ['production_authority', 'live_external_model_dispatch', 'browser_session_mutation', 'credential_access', 'form_submission', 'paid_cloud_launch', 'source_summary_rewrite', 'canonical_graph_write', 'unrestricted_agent_activation'],
};

export const v56CockpitProjectionFixture: CockpitProjectionFixture = {
  version: 'V59_MISSION_DISPATCH_AND_MODEL_ROUTE_VIEW_MODEL',
  stewardState: 'STEWARD_VZ_SCOPED_REVIEW',
  oracleMode: 'SUPERVISED',
  activeSurface: 'Mission Route Preview',
  closureVerdict: 'VISUAL_ISSUE_CLOSED_WITH_RUN_EVIDENCE',
  receiptSummaries: [
    { id: 'v54-visual-run-diagnosis-binding-reference', family: 'visual closure', claimLane: 'C0', verdict: 'VISUAL_ISSUE_CLOSED_WITH_RUN_EVIDENCE', authorityScope: 'VISUAL_RUN_TO_DIAGNOSIS_CLOSURE_RECEIPT_ONLY', evidenceRefs: ['V45 diagnosis', 'V48 before/after', 'V53 local run'], repairRequired: false },
    { id: 'v57-reactive-os-stream-reference', family: 'reactive stream', claimLane: 'C2', verdict: 'VALID_REACTIVE_OS_STREAM_VIEW_MODEL', authorityScope: 'REACTIVE_OS_STREAM_VIEW_MODEL_RECEIPT_ONLY', evidenceRefs: ['loop coverage', 'event evidence', 'blocked capability visibility'], repairRequired: false },
    { id: 'v58-cognitive-explorer-route-reference', family: 'context route', claimLane: 'C2', verdict: 'VALID_CONTEXT_ROUTE_VIEW_MODEL', authorityScope: 'COGNITIVE_EXPLORER_ROUTE_VIEW_MODEL_RECEIPT_ONLY', evidenceRefs: ['selected nodes', 'dependency edges', 'source citations', 'route reasoning'], repairRequired: false },
    { id: 'v59-mission-dispatch-route-reference', family: 'mission route', claimLane: 'C2', verdict: 'ROUTE_PREVIEW_READY', authorityScope: 'MISSION_DISPATCH_ROUTE_VIEW_MODEL_RECEIPT_ONLY', evidenceRefs: ['primary target', 'fallback chain', 'route factors', 'approval gate'], repairRequired: false },
  ],
  automationEvents: v57ReactiveEvents.slice(0, 4).map((event) => ({ id: event.eventId, time: event.occurredAt, loop: event.loopId, phase: event.phase, status: event.status === 'OK' ? 'ok' : event.status === 'BLOCKED' ? 'blocked' : 'watch', detail: event.detail })),
  reactiveEvents: v57ReactiveEvents,
  cognitiveRoute: v58CognitiveRoute,
  missionRoute: v59MissionRoute,
  blockedCapabilities: ['production_authority', 'credential_access', 'external_network_authority', 'form_submission', 'persistent_dom_mutation', 'production_visual_automation', 'external_model_dispatch', 'canonical_graph_write'],
};
