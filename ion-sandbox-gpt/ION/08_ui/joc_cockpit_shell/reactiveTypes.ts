export type ClaimLane = 'C0' | 'C1' | 'C2' | 'C3' | 'C4' | 'C5';
export type ReactiveStatus = 'OK' | 'WATCH' | 'BLOCKED' | 'REPAIR';

export type ReactiveStreamEvent = {
  eventId: string;
  occurredAt: string;
  loopId: string;
  phase: string;
  status: ReactiveStatus;
  claimLane: ClaimLane;
  renderedSurface: string;
  authorityScope: string;
  evidenceRefs: string[];
  repairRequired: boolean;
  blockedCapabilities: string[];
  detail: string;
};

export type ExplorerNodeClass = 'FILE' | 'CLASS' | 'FUNCTION' | 'PROTOCOL' | 'REGISTRY' | 'RECEIPT' | 'TEST' | 'UI_COMPONENT';

export type ExplorerNode = {
  nodeId: string;
  label: string;
  nodeClass: ExplorerNodeClass;
  path: string;
  symbol?: string;
  lineRange: string;
  confidence: 'SOURCE_INDEXED' | 'DERIVED_EDGE' | 'RECEIPT_BACKED';
};

export type DependencyEdge = {
  source: string;
  target: string;
  edgeClass: string;
  evidenceRef: string;
};

export type CognitiveRouteViewModel = {
  query: string;
  verdict: 'VALID_CONTEXT_ROUTE_VIEW_MODEL' | 'WATCH' | 'BLOCKED';
  routeClasses: string[];
  viewSurfaces: string[];
  selectedNodes: ExplorerNode[];
  dependencyEdges: DependencyEdge[];
  sourceCitations: string[];
  routeReasoning: string;
  injectionPreview: string;
  blockedCapabilities: string[];
};

export function loopCoverage(events: ReactiveStreamEvent[], requiredLoops: string[]) {
  const present = new Set(events.map((event) => event.loopId));
  return requiredLoops.map((loop) => ({ loop, present: present.has(loop) }));
}

export type ComputeRing = 'RING_1_BROWSER_SESSION' | 'RING_2_API_CLI_LOCAL' | 'RING_3_CLOUD_COMPUTE';
export type RouteTargetStatus = 'PRIMARY_RECOMMENDED' | 'FALLBACK_READY' | 'SUPERVISED_ONLY' | 'BLOCKED';

export type MissionRouteTarget = {
  targetId: string;
  displayName: string;
  computeRing: ComputeRing;
  accessMethod: 'browser' | 'api' | 'cli' | 'local' | 'cloud_vm';
  status: RouteTargetStatus;
  capabilityTags: string[];
  costBand: string;
  latencyBand: string;
  qualityBand: string;
  riskNotes: string[];
};

export type MissionRouteFactor = {
  factorId: string;
  value: string;
  rationale: string;
};

export type MissionDispatchRouteViewModel = {
  missionId: string;
  missionTitle: string;
  taskClass: string;
  verdict: 'ROUTE_PREVIEW_READY' | 'BLOCKED';
  authorityScope: 'MISSION_DISPATCH_ROUTE_VIEW_MODEL_RECEIPT_ONLY';
  contextRouteRef: string;
  primaryTarget: MissionRouteTarget;
  fallbackTargets: MissionRouteTarget[];
  routeFactors: MissionRouteFactor[];
  viewSurfaces: string[];
  approvalGate: 'SUPERVISED_APPROVAL_REQUIRED';
  routeReasoning: string;
  dispatchReceiptPreview: string;
  blockedCapabilities: string[];
};
