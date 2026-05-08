# graph.py Comparison Report — Living Context Graph Adapter v13

**Date:** 2026-04-24  
**Base:** V12 Self-Documenting Approved Context full project  
**Purpose:** Compare restored living-context-graph ontology against existing kernel `model.py`, `store.py`, `index.py`, and `graph.py`.

---

## 1. Finding

The existing kernel graph is an enacted runtime/causal graph projection over persisted kernel records. It is not the whole living context graph.

Correct relation:

```text
store.py persists kernel record nodes.
index.py projects lookup coverage.
graph.py navigates enacted runtime causality.
context_graph_ontology_adapter.py maps broader living-context ontology to existing enacted surfaces and future adapter needs.
```

---

## 2. Existing record evidence

Approximate record classes detected from `model.py`:

```text
AgentIdentity
ArtifactOperation
AuthorityClass
AutomationGate
AutomationStateRecord
BranchClaimReceipt
BranchClaimStatus
BranchControlReceipt
BranchHorizonSyncReceipt
BranchMergeProposal
BranchRescheduleReceipt
BranchSettlementOutcome
BranchSettlementReceipt
CarrierBindingSource
ChildSpec
CommitDelta
CommitDeltaStatus
ContextPackage
ContextPerfectContinuationReceipt
ContextTiers
DependencyInterface
EvidencePressure
ExecutorAvailability
ExecutorCapability
ExecutorTrustClass
ExecutorWorkLifecycleBindingReceipt
FallbackSuitability
HorizonEnactmentReceipt
HorizonLayer
HorizonRecord
HorizonWorkItem
InputRef
InputRefType
InputVisibility
LedgerEntry
ManifestModeBinding
ManifestRouteStateRecord
ManualAutomationEquivalenceReceipt
MissionAdvisoryHorizonBindingReceipt
MissionAdvisoryManifestRouteBindingReceipt
MissionAdvisoryPlannerManifestMaintenanceDispositionAction
MissionAdvisoryPlannerManifestMaintenanceDispositionReceipt
MissionAdvisoryPlannerManifestMaintenanceReceipt
MissionAdvisoryPlannerManifestMaintenanceResolutionReceipt
MissionAdvisoryProfile
MissionAdvisoryRoutingReceipt
OpenQuestion
OpenQuestionPriority
OpenQuestionStatus
PlannerIntentType
PlannerManifest
PlannerManifestStatus
PlannerManifestSweepAggregateRecord
PlannerManifestSweepReceipt
PriorFinding
ProducedArtifact
ProposedSignal
QuestionAnswerRecord
ReviewerAnswerQueueProjectionRecord
ReviewerQueueRefreshReceipt
RootAuthorityBundleExerciseReceipt
RootAuthorityBundleExternalReturnReceipt
RouteBranch
RouteFrame
RouteOwnerScope
RoutingAssessment
ScheduleActivationHandoffCapsuleReceipt
ScheduleCarrier
ScheduleCommitment
ScheduleCompletionReleaseReceipt
ScheduleControlReceipt
ScheduleDispatchReconciliationReceipt
ScheduleExecutorStartPacketMaterializationReceipt
ScheduleHandoffEntryRehearsalReceipt
ScheduleLineageArchiveReceipt
ScheduleLineageReplayReceipt
ScheduleReceipt
ScheduleResumeBundleMaterializationReceipt
ScheduleResumeProjectionReceipt
ScheduleSettlementReceipt
ScheduleSourceKind
ScheduleState
ScheduleTakeoverEntryActivationReceipt
ScopeType
SemanticOverlay
SpawnPolicy
StateMutation
StateMutationOperation
StrEnum
TakeoverAssessmentReceipt
TargetFile
TierFiveDependencies
TierFourSemantic
TierOneDoctrine
TierThreeMission
TierTwoTarget
WorkPriority
WorkUnit
WorkUnitStatus
```

Approximate record types detected from `RecordSpec` patterns:

```text
No record_type patterns detected by simple scanner.
```

---

## 3. Existing graph edge evidence

Approximate edge-like constants detected from `graph.py`:

```text
ANSWERS_QUESTION
ANSWER_FOR_WORK
AUTOMATION_FOR_WORK
BLOCKS_WORK
CONTEXT_FOR
CONTEXT_FOR_DELTA
DELTA_FOR_MANIFEST
EMITS_DELTA
ENABLES_WORK
MANIFEST_BINDS_AUTOMATION
MANIFEST_FOR_WORK
PARENT_QUESTION_FOR
QUESTION_FOR_MANIFEST
RAISES_QUESTION
SPAWNS_CHILD
SWEEPS_MANIFEST
```

---

## 4. Proposed node classes already enacted

```text
node.work_unit -> ENACTED_KERNEL_RECORD
node.context_package -> ENACTED_KERNEL_RECORD
node.receipt -> ENACTED_KERNEL_RECORD / file receipt surface
node.horizon -> ENACTED_KERNEL_RECORD
node.packet -> ENACTED_FILE_SURFACE
node.template -> ENACTED_TEMPLATE_SURFACE
node.registry_entry -> ENACTED_REGISTRY_SURFACE
node.semantic_identity -> ENACTED_REGISTRY_SURFACE
node.template_completion_event -> ENACTED_EVENTED_GRAPH_STATE
node.graph_writeback_proposal -> ENACTED_EVENTED_GRAPH_STATE
node.graph_commit -> ENACTED_EVENTED_GRAPH_STATE
node.approved_context_entry -> ENACTED_REGISTRY_SURFACE
node.ion_file_record -> ENACTED_TEMPLATE_SURFACE
node.system_card -> ENACTED_TEMPLATE_SURFACE
```

---

## 5. Proposed node classes requiring adapter work

```text
node.user_interaction -> ADAPTER_REQUIRED
node.agent.role -> needs jurisdiction lattice hardening
node.archive_capsule -> archive registry/index mapping needed
```

---

## 6. Edge comparison

Existing kernel graph appears to support causal edges around context, work, questions, deltas, manifests, automation, and related runtime records.

Living-context edge classes that require explicit adapter work include:

```text
edge.instantiates
edge.proves
edge.mutates
edge.routes_to
edge.approves_context
edge.classifies_file
```

Some are partially enacted through V10/V12 surfaces but not yet unified into `graph.py`.

---

## 7. Recommendation

Do not rewrite `graph.py` yet.

Next step should be:

```text
1. keep context_graph_ontology_adapter.py read-only;
2. use it to classify node/edge/region classes;
3. add graph-state projection reports;
4. only later decide whether adapter edges should feed kernel graph.py or remain a higher substrate projection.
```

---

## 8. Boundary

This report does not claim full implementation of the Living Context Graph. It provides the adapter map that prevents false equivalence between the restored substrate doctrine and the current kernel graph implementation.
