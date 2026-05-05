# ION Steward Implementation Handoff — API Provider Orchestration and Model Economics

## Scheduler-Aware Multi-Provider Runtime for GPT / Claude / Gemini / Cerebras / Local Models

**Document class:** Steward implementation handoff packet  
**Target system:** ION live project root  
**Target authority:** Steward / implementation planning lane  
**Status:** Implementation handoff draft, not encyclopedia prose  
**Production authority:** false  
**Project-root mutation claim:** false until applied to the live ION project root and verified  
**Primary mission:** Implement the missing model-economic orchestration organ so ION can choose, schedule, throttle, budget, and receipt model calls across multiple providers.

---

# 0. Handoff Receipt

```yaml
handoff_id: ion-steward-api-provider-orchestration-model-economics-implementation-handoff
handoff_class: STEWARD_IMPLEMENTATION_HANDOFF
intended_recipient: Steward
project: ION
production_claim: false
implementation_claim: false
requires_project_root_patch: true
requires_tests: true
requires_receipts: true
requires_manifest_update: true
requires_checksum_update: true

core_instruction:
  - Do not treat this as encyclopedia prose.
  - Treat this as an implementation planning and patch-design packet.
  - Convert the design into live ION project files only through governed write, receipts, tests, manifest updates, and checksum updates.

primary_goal:
  Build ION’s provider-aware model routing, API rate-governance, budget/margin-governance, and model-call receipt subsystem.
```

---

# 1. Steward Mission Statement

Steward must implement a new ION runtime organ that prevents external model calls from being ad hoc, wasteful, provider-biased, unreceipted, or unsafe.

The subsystem must let ION determine:

```text
what work needs a model;
which class of work it is;
which providers/models are eligible;
which model is cheapest-good-enough;
which model is highest quality;
which model gives the best quality per dollar;
which provider has current capacity;
which calls should be interactive, background, batch, local, or human/IDE-carried;
how many calls may run in parallel;
whether the projected cost fits the workflow budget;
whether a premium escalation is justified;
whether a cross-model audit is required;
what happened after the call;
whether the model result needs review, repair, downgrade, escalation, or receipt.
```

The final canon sentence for implementation is:

```text
ION must not merely call models. ION must govern model selection as an economic, epistemic, temporal, and evidentiary act.
```

---

# 2. Non-Negotiable Architecture Separation

Steward must not collapse scheduler, model router, API rate governor, budget governor, provider adapter, and receipt logic into a single mechanism.

The separation of organs is mandatory:

```text
Scheduler
  Decides what work should move and when.

Session Queue and Dispatch
  Holds pending assignments, lanes, retries, and settlement state.

Executor Registry
  Defines eligible carriers and execution surfaces.

Work Classifier
  Types the work before any model is selected.

Model Router
  Selects the model/provider route based on work class, capability, cost, latency, risk, context, privacy, and current performance.

API Rate Governor
  Determines whether the selected provider/model can be called now.

Budget and Margin Governor
  Determines whether the call is economically allowed.

Provider Adapter
  Executes the provider-specific API call.

Model Call Receipt
  Records the decision, route, cost, tokens, latency, retry state, result, and claim boundary.

Evaluation Feedback Layer
  Updates model performance history based on actual ION receipts.
```

Implementation rule:

```text
The scheduler decides what should run. The router decides who should carry it. The governor decides whether it may run now. The budget layer decides whether it should run at all. The receipt proves what happened.
```

---

# 3. Existing ION Surfaces to Inspect Before Patch

Before writing new files, Steward should inspect the live project root for existing scheduler/runtime surfaces and avoid duplicate organs.

Likely related existing surfaces:

```text
ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md
ION/02_architecture/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md
ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md
ION/02_architecture/API_RUNTIME_ENTRY_PROTOCOL.md
ION/02_architecture/SUPERVISED_DAEMON_SERVICE_PROTOCOL.md
ION/04_packages/kernel/scheduler.py
ION/04_packages/kernel/executor_registry.py
ION/04_packages/kernel/schedule_controls.py
ION/04_packages/kernel/api_runtime_entry.py
ION/04_packages/kernel/daemon.py
ION/04_packages/kernel/daemon_service.py
```

If these files already implement partial equivalents, Steward must integrate rather than overwrite.

Required classification if overlap is found:

```yaml
overlap_class:
  - existing_surface_reused
  - existing_surface_extended
  - new_surface_required
  - stale_surface_deprecated
  - duplicate_surface_blocked
```

---

# 4. Required New Project Files

Steward should prepare a patch that adds the following candidate files to the live ION project root.

## 4.1 Architecture protocols

```text
ION/02_architecture/MODEL_ROUTING_AND_PROVIDER_ECONOMICS_PROTOCOL.md
ION/02_architecture/API_RATE_GOVERNOR_AND_PROVIDER_LIMIT_PROTOCOL.md
ION/02_architecture/COST_QUALITY_MARGIN_ROUTING_PROTOCOL.md
ION/02_architecture/CROSS_MODEL_AUDIT_AND_CONSENSUS_PROTOCOL.md
ION/02_architecture/BATCH_AND_BACKGROUND_MODEL_EXECUTION_PROTOCOL.md
ION/02_architecture/LOCAL_MODEL_AND_PRIVATE_EXECUTION_LANE_PROTOCOL.md
ION/02_architecture/MODEL_CALL_RECEIPT_PROTOCOL.md
```

## 4.2 Registries and policies

```text
ION/03_registry/provider_registry.yaml
ION/03_registry/model_capability_registry.yaml
ION/03_registry/model_pricing_registry.yaml
ION/03_registry/model_rate_limit_registry.yaml
ION/03_registry/model_routing_policy.yaml
ION/03_registry/model_eval_score_registry.yaml
ION/03_registry/model_data_handling_registry.yaml
ION/03_registry/budget_policy.yaml
ION/03_registry/work_class_model_policy.yaml
```

## 4.3 Runtime modules

```text
ION/04_packages/kernel/model_router.py
ION/04_packages/kernel/api_rate_governor.py
ION/04_packages/kernel/budget_governor.py
ION/04_packages/kernel/provider_registry.py
ION/04_packages/kernel/cost_quality_router.py
ION/04_packages/kernel/model_call_receipt.py
ION/04_packages/kernel/provider_adapters/__init__.py
ION/04_packages/kernel/provider_adapters/openai_adapter.py
ION/04_packages/kernel/provider_adapters/anthropic_adapter.py
ION/04_packages/kernel/provider_adapters/gemini_adapter.py
ION/04_packages/kernel/provider_adapters/cerebras_adapter.py
ION/04_packages/kernel/provider_adapters/local_model_adapter.py
```

## 4.4 Tests

```text
ION/tests/test_kernel_model_router.py
ION/tests/test_kernel_api_rate_governor.py
ION/tests/test_kernel_budget_governor.py
ION/tests/test_kernel_model_call_receipt.py
ION/tests/test_kernel_scheduler_rate_governor_integration.py
ION/tests/test_kernel_cost_quality_routing.py
ION/tests/test_kernel_cross_model_audit_routing.py
ION/tests/test_kernel_batch_lane_routing.py
```

---

# 5. Work Classes to Implement First

Steward should not attempt a universal routing ontology in the first patch. Implement a minimal but extensible work-class set.

Minimum initial work classes:

```text
cheap_classification
graph_indexing
source_summary_rewrite_draft
source_summary_rewrite_review
code_patch
code_review
architecture_design
visual_diagnosis
claim_audit
adversarial_review
user_facing_answer
front_stage_claim_classification
conversation_repair
long_context_digest
batch_corpus_processing
embedding_generation
local_private_tagging
```

Each work class must define:

```yaml
work_class_contract:
  work_class: <name>
  minimum_quality: low | medium | high | supreme
  default_routing_mode: cheapest_good_enough | balanced | highest_quality | fastest_safe | consensus_required | batch_preferred
  allowed_lanes:
    - interactive
    - checked
    - background
    - batch
    - local
    - human_ide_carrier
  forbidden_lanes: []
  consensus_required_by_default: true | false
  premium_allowed_by_default: true | false
  privacy_floor: normal | sensitive | local_only
  max_default_parallelism: <integer>
```

---

# 6. Runtime Data Contracts

## 6.1 Call intent packet

Every model call must begin with a typed call intent object.

```yaml
call_intent:
  intent_id: call-intent-<timestamp>-<slug>
  workflow_id: <workflow>
  parent_packet: <packet_or_receipt_id>
  work_class: <work_class>
  quality_requirement: low | medium | high | supreme
  latency_requirement: realtime | interactive | checked | background | batch
  cost_posture: cheapest | efficient | balanced | premium | approval_required
  risk_level: low | medium | high | blocking
  context_requirement: small | medium | long | huge
  estimated_input_tokens: <number_or_unknown>
  estimated_output_tokens: <number_or_unknown>
  parallelism_allowed: false | true
  consensus_required: false | true
  privacy_requirement: normal | sensitive | local_only | no_retention_preferred
  max_estimated_cost_usd: <number_or_null>
  max_latency_ms: <number_or_null>
  required_capabilities:
    - reasoning
    - code
    - long_context
    - vision
    - json_schema
  forbidden_providers: []
  preferred_providers: []
  fallback_allowed: true
  escalation_allowed: true
```

A call intent is not an API call. It is a routing request.

## 6.2 Route decision

```yaml
route_decision:
  decision_id: route-decision-<timestamp>-<slug>
  intent_id: <call_intent_id>
  selected_provider: <provider_id>
  selected_model: <model_id>
  selected_lane: interactive | checked | background | batch | local | human_ide_carrier
  routing_mode: cheapest_good_enough | highest_quality | best_margin | fastest_safe | consensus_required | batch_preferred
  selection_reason:
    - sufficient_capability
    - context_fit
    - within_budget
    - provider_capacity_available
  alternatives_considered:
    - provider: <provider_id>
      model: <model_id>
      rejected_reason: too_expensive | insufficient_context | throttled | low_capability | privacy_mismatch | unavailable
  requires_rate_governor_check: true
  requires_budget_governor_check: true
  requires_front_stage_receipt_if_user_facing: true
```

## 6.3 Provider capacity state

```yaml
provider_capacity_state:
  provider: <provider_id>
  project_id: <project_or_account_ref>
  model: <model_id>
  rpm_limit: known_or_unknown
  rpm_remaining: measured_or_estimated
  rpm_reset_at: timestamp_or_unknown
  tpm_limit: known_or_unknown
  tpm_remaining: measured_or_estimated
  tpm_reset_at: timestamp_or_unknown
  rpd_limit: known_or_unknown
  rpd_remaining: measured_or_estimated
  tpd_limit: known_or_unknown
  tpd_remaining: measured_or_estimated
  ipm_limit: known_or_not_applicable
  ipm_remaining: known_or_not_applicable
  in_flight_requests: <number>
  safe_parallelism_current: <number>
  safe_parallelism_max: <number>
  backoff_state: normal | cooling | throttled | blocked
  last_429_at: timestamp_or_null
  retry_after_until: timestamp_or_null
  confidence: high | medium | low
```

## 6.4 Rate governor decision

```yaml
rate_governor_decision:
  decision: allow | queue | reroute | batch | throttle | block
  reason:
    - enough_rpm
    - enough_tpm
    - in_flight_below_safe_parallelism
    - retry_after_active
    - provider_degraded
  earliest_dispatch_at: timestamp_or_now
  suggested_fallbacks:
    - provider/model
```

## 6.5 Budget decision

```yaml
budget_decision:
  decision: allow | downgrade_model | batch_route | require_approval | block
  estimated_cost_usd: <number_or_unknown>
  budget_remaining_usd: <number_or_unknown>
  margin_status: within_margin | above_preferred | exceeds_max | blocked
  reason:
    - within_budget
    - exceeds_preferred_cost_but_within_max
    - premium_escalation_justified
    - projected_cost_exceeds_margin
    - no_remaining_budget
```

## 6.6 Model call receipt

```yaml
model_call_receipt:
  receipt_id: model-call-<timestamp>-<slug>
  provider: openai | anthropic | gemini | cerebras | local | other
  model: <model_id>
  adapter: <adapter_id>
  workflow_id: <workflow>
  parent_intent_id: <call_intent_id>
  route_decision_id: <route_decision_id>
  work_class: <work_class>
  routing_mode: cheapest_good_enough | highest_quality | best_margin | fastest_safe | consensus_required | batch_preferred
  selected_by: model_router
  selection_reason:
    - sufficient_capability
    - context_fit
    - within_budget
    - provider_capacity_available
  estimated_cost_usd: <number_or_unknown>
  actual_cost_usd: <number_or_unknown>
  input_tokens: <number_or_unknown>
  output_tokens: <number_or_unknown>
  latency_ms: <number_or_unknown>
  rate_limit_headers_recorded: true | false
  retry_count: <number>
  backoff_applied: true | false
  result_status: success | partial | failed | throttled | blocked
  confidence: low | medium | high
  escalation_required: true | false
  produced_artifacts: []
  claim_boundary:
    - this receipt proves the call and route, not truth of all returned content
```

---

# 7. Model Routing Modes

Steward must implement routing modes as explicit policy states.

```yaml
routing_modes:
  cheapest_good_enough:
    purpose: low-risk classification, extraction, indexing, draft summaries
    rule: choose cheapest route above minimum capability threshold
    escalation: only if confidence fails or contradiction appears

  highest_quality:
    purpose: high-stakes architecture, canonical claim settlement, difficult reasoning
    rule: choose strongest eligible model within approved budget
    receipt_required: true
    premium_reason_required: true

  best_margin:
    purpose: product economics and sustainable workflow execution
    rule: maximize verified quality per dollar
    prefer_batch_when_latency_allows: true

  fastest_safe:
    purpose: live UI support, quick routing, provisional low-risk help
    rule: choose lowest-latency eligible model above safety and quality threshold

  consensus_required:
    purpose: high-risk or canonical claims
    rule: use primary model plus independent review model or provider
    steward_settlement_required: true

  batch_preferred:
    purpose: large non-urgent work
    rule: route to batch/background lane rather than consuming interactive capacity
```

---

# 8. Cost-Quality-Latency Scoring

The first implementation can use simple deterministic scoring. It does not need ML.

Candidate score formula:

```text
route_score =
  quality_weight      * capability_score
+ latency_weight      * speed_score
+ cost_weight         * inverse_cost_score
+ context_weight      * context_fit_score
+ reliability_weight  * recent_success_score
+ availability_weight * current_capacity_score
+ privacy_weight      * data_policy_score
- risk_penalty
- throttle_penalty
- stale_registry_penalty
```

Implementation may use normalized floats from `0.0` to `1.0`.

Minimum requirements:

```text
Models below required capability threshold must be filtered out before scoring.
Providers failing privacy requirements must be filtered out before scoring.
Routes exceeding hard budget must be blocked before scoring.
Routes under active retry-after should be queued or rerouted before scoring.
```

---

# 9. Provider Adapters

Provider adapters should initially be safe stubs unless credentials and live API use are explicitly configured.

Adapter responsibilities:

```text
normalize request shape;
execute provider call if enabled;
capture response metadata;
capture token usage if available;
capture rate-limit headers if available;
capture retry-after data if present;
map provider errors into ION error classes;
return a provider-neutral execution result;
never bypass model-call receipt generation.
```

Provider-neutral result shape:

```yaml
provider_execution_result:
  provider: <provider_id>
  model: <model_id>
  status: success | partial | failed | throttled | blocked
  output_ref: <artifact_or_text_ref>
  input_tokens: <number_or_unknown>
  output_tokens: <number_or_unknown>
  latency_ms: <number_or_unknown>
  raw_error_class: <string_or_null>
  normalized_error_class: rate_limited | timeout | auth_error | provider_error | invalid_request | safety_block | unknown | null
  retry_after_seconds: <number_or_null>
  rate_limit_headers: {}
```

---

# 10. Integration With Existing Scheduler

The scheduler should not call providers directly.

Correct dispatch path:

```text
assignment
→ work classification
→ call intent packet
→ model router
→ budget governor
→ API rate governor
→ scheduler lane placement
→ provider adapter
→ model call receipt
→ result review / front-stage receipt / repair route
```

The scheduler may dispatch deterministic or local work directly if no model call is needed.

Mandatory no-waste rule:

```text
If deterministic code can perform the task reliably, do not use a model call.
```

Deterministic tasks include:

```text
zip inspection;
manifest generation;
checksum generation;
file tree indexing;
path existence checks;
schema validation;
unit test execution;
diff generation;
line counting;
archive integrity checks.
```

---

# 11. Integration With Front-Stage Council

Model output is not automatically user-facing truth.

Any user-facing result derived from a model call should follow V41 logic:

```text
model output
→ claim extraction
→ claim class assignment
→ Relay grounding/provenance check
→ Steward/VZ risk verdict
→ emission permission
→ Persona rendering
→ user-facing response
```

A premium model does not bypass Front-Stage Council. A cheap model does not automatically disqualify a claim. The determining factors are evidence, grounding, risk, and receipt status.

Implementation requirement:

```text
model_call_receipt.receipt_id must be linkable from any front_stage_council_runtime_receipt derived from that call.
```

---

# 12. Integration With V42 Conversational Repair

The model routing subsystem must support repair.

If the user corrects a response, ION should be able to inspect:

```text
Was the wrong model used?
Was the work class misclassified?
Was the route too cheap?
Was a premium route used wastefully?
Was context missing?
Was provider output ungrounded?
Was front-stage claim classification wrong?
Was the artifact target wrong?
Was the repair applied to chat but not artifact?
```

Conversational repair receipts should link to implicated model-call receipts.

Candidate linkage:

```yaml
repair_receipt:
  repair_class: artifact_target_realignment
  triggering_issue: assistant_updated_canvas_instead_of_markdown_packet
  implicated_model_call_receipts:
    - <receipt_id>
  routing_issue: none_or_misclassified
  workflow_issue: target_surface_misidentified
  corrected_target: encyclopedia_markdown_packet
  artifact_repair_required: true
```

Rule:

```text
Repair is not only apology. Repair is a continuity event.
```

---

# 13. Integration With Visual Perception and Interaction Agent

Visual work must be routed by capability and risk.

Visual call intent should include:

```yaml
visual_call_intent:
  visual_task: observe | diagnose | compare | verify | explain | patch_request
  source_kind: screenshot | DOM_snapshot | browser_state | video_frame | simulation_frame | chart | dashboard
  requires_vision_model: true
  requires_code_context: true | false
  requires_dom_context: true | false
  risk_level: low | medium | high
  mutation_allowed: false
```

Routing examples:

```text
screenshot-only low-risk observation
→ balanced vision-capable model

screenshot + code diagnosis
→ multimodal model with strong code reasoning or vision model followed by code model handoff

visual regression verification
→ cheap vision comparison if low-risk; stronger model if release-impacting

simulation interpretation
→ multimodal reasoning model, possibly followed by research/review model

DOM action proposal
→ visual agent + action authority gate, not direct mutation
```

Rule:

```text
Rendered behavior is part of truth. Source-code correctness is not product correctness.
```

---

# 14. Cross-Model Audit and Consensus

Certain work must require multiple models or a separate reviewer route.

Consensus-required classes:

```text
production-readiness claims;
canonical encyclopedia claims;
high-risk architecture decisions;
security-sensitive interpretations;
semantic-truename disputes;
major project-root mutation proposals;
source-summary rewrite commit decisions;
agent activation decisions;
front-door high-impact user-facing claims.
```

Consensus receipt:

```yaml
cross_model_audit_receipt:
  audit_id: <id>
  primary_model_call: <receipt_id>
  reviewer_model_calls:
    - <receipt_id>
  agreement_status: agreed | partial | contradicted | inconclusive
  disagreements:
    - claim: <claim>
      primary_position: <position>
      reviewer_position: <position>
      severity: low | medium | high | blocking
  steward_settlement_required: true
  final_status: settled | blocked | needs_human_review
```

Consensus does not mean every model agrees. It means disagreement is typed, receipted, and routed to settlement.

---

# 15. Budget and Margin Rules

ION must eventually operate economically. Model routing must therefore include budget envelopes.

Workflow budget object:

```yaml
workflow_budget:
  workflow_id: <workflow_id>
  user_visible_value: low | medium | high | critical
  maximum_cost_usd: <number>
  preferred_cost_usd: <number>
  premium_escalation_allowed: true | false
  batch_allowed: true | false
  consensus_allowed: true | false
  abort_if_projected_cost_exceeds: <number>
```

Rules:

```text
Cheap tasks should not consume premium model budget.
High-risk canonical tasks should not be routed to weak models merely to save cost.
Premium calls require an explicit premium-spend reason.
Budget exhaustion must queue, downgrade, batch, request approval, or block work.
Margin state must be visible in receipts.
```

---

# 16. Provider Fallback

Fallback must be lawful and explicit.

Fallback decision:

```yaml
fallback_decision:
  original_route: provider_a/model_x
  fallback_route: provider_b/model_y
  reason:
    - original_provider_throttled
    - retry_after_active
    - fallback_meets_minimum_capability
    - cost_within_budget
  claim_boundary:
    - fallback model may require stronger review before canonical claim
```

Fallback types:

```text
same provider, cheaper model;
same provider, slower batch lane;
different provider, similar capability;
different provider, lower capability with scope reduction;
local model with reduced claim authority;
human/IDE carrier handoff;
queue until capacity resets.
```

Rule:

```text
ION should prefer explicit degradation over hidden quality loss.
```

---

# 17. Parallelism Rules

Parallelism should be allowed only when capacity, budget, task independence, and settlement rules permit it.

Parallelism types:

```text
independent parallelism:
  unrelated low-risk tasks can run in parallel.

fan-out/fan-in parallelism:
  multiple models or agents explore branches and return packets to Steward.

consensus parallelism:
  several models evaluate the same claim or artifact.

pipeline parallelism:
  one lane indexes while another drafts while another verifies.

forbidden parallelism:
  tasks that mutate the same artifact, depend on unsettled claims, or create external side effects.
```

Safe parallelism requires:

```text
provider capacity available;
workflow budget available;
non-conflicting artifact targets;
clear fan-in settlement point;
receipt generation;
rollback or abort plan;
claim boundary.
```

---

# 18. Failure Modes This Patch Must Prevent

The implementation must explicitly prevent or detect:

```text
premium waste:
  using expensive models for trivial tasks.

cheap overreach:
  using weak models for canonical/high-risk claims.

parallel overload:
  too many calls against one provider or model limit.

silent downgrade:
  falling back to weaker models without changing claim authority.

retry storm:
  repeatedly retrying after rate-limit errors without backoff.

budget blindness:
  completing a workflow with no idea what it cost.

margin collapse:
  delivering product work at unsustainable cost.

provider mythology:
  choosing models by reputation instead of current evidence.

receipt loss:
  losing track of which model produced which claim.

consensus theatre:
  calling multiple models but not reconciling disagreement.

privacy mismatch:
  sending sensitive content to an unsuitable provider.

batch misuse:
  putting urgent interactive work into batch or massive background work into interactive.

scheduler collapse:
  treating model choice, rate limits, and work timing as one undifferentiated mechanism.
```

---

# 19. Initial Implementation Order

Steward should implement this in phases.

## Phase 1 — Policy and registry skeletons

Create architecture protocol files and minimal registries:

```text
provider_registry.yaml
model_capability_registry.yaml
model_routing_policy.yaml
budget_policy.yaml
work_class_model_policy.yaml
```

Acceptance:

```text
registries parse;
required keys exist;
no live provider credentials required;
no production claim emitted.
```

## Phase 2 — Pure routing logic

Implement:

```text
model_router.py
cost_quality_router.py
provider_registry.py
```

Acceptance:

```text
router can choose cheapest_good_enough;
router can choose highest_quality;
router can reject privacy-mismatched route;
router can reject insufficient-capability route;
router can return alternatives_considered.
```

## Phase 3 — Budget and rate governors as deterministic modules

Implement:

```text
budget_governor.py
api_rate_governor.py
```

Acceptance:

```text
budget allows within-budget call;
budget requires approval above max;
rate governor allows when capacity exists;
rate governor queues/reroutes during retry-after;
rate governor blocks excessive in-flight requests.
```

## Phase 4 — Model call receipts

Implement:

```text
model_call_receipt.py
```

Acceptance:

```text
receipt validates required fields;
receipt records selection reason;
receipt records cost/tokens if known;
receipt records claim boundary;
receipt can link to front-stage/conversational repair receipts.
```

## Phase 5 — Provider adapter stubs

Implement safe provider adapter stubs first:

```text
openai_adapter.py
anthropic_adapter.py
gemini_adapter.py
cerebras_adapter.py
local_model_adapter.py
```

Acceptance:

```text
adapters expose common interface;
adapters can run in dry_run mode;
adapters return provider-neutral result objects;
adapters do not require credentials for tests;
adapters never bypass receipt layer.
```

## Phase 6 — Scheduler integration

Integrate with existing scheduler/session queue only after routing, budget, rate, and receipt tests pass.

Acceptance:

```text
scheduler does not call provider adapter directly;
scheduler dispatches through call intent -> router -> governors -> adapter -> receipt;
queued and rerouted states are represented;
parallelism respects capacity.
```

---

# 20. Minimum Test Matrix

Required tests:

```text
test_router_selects_cheapest_good_enough_when_low_risk
test_router_selects_highest_quality_when_required
test_router_rejects_provider_for_privacy_mismatch
test_router_rejects_model_below_capability_threshold
test_router_records_alternatives_considered
test_rate_governor_allows_capacity_available
test_rate_governor_queues_retry_after_active
test_rate_governor_blocks_parallelism_over_limit
test_budget_governor_allows_within_budget
test_budget_governor_requires_approval_above_max
test_model_call_receipt_validates_required_fields
test_model_call_receipt_claim_boundary_present
test_scheduler_uses_router_before_provider_adapter
test_consensus_route_requires_second_model
test_batch_preferred_routes_to_batch_lane
test_visual_diagnosis_requires_vision_capability
```

---

# 21. Completion Criteria

The implementation is complete only when:

```text
all required files exist in the live ION project root;
protocols state boundaries and non-production posture;
registries parse and contain minimal defaults;
runtime modules import without provider credentials;
provider adapters support dry-run mode;
unit tests pass;
manifest is updated;
checksums are updated;
implementation receipt is written;
no production authority is claimed;
no live provider calls occur unless explicitly configured;
model-call receipt path exists;
scheduler integration path is represented or explicitly deferred.
```

---

# 22. Steward Execution Prompt

The following prompt can be handed to Steward or an implementation agent:

```text
You are operating as Steward for the ION live project root.

Mission:
Implement the API Provider Orchestration, Model Economics, and Cost-Quality Routing subsystem as a non-production-authoritative candidate patch.

Hard rules:
1. Do not treat model calls as invisible side effects.
2. Do not collapse scheduler, router, rate governor, budget governor, provider adapter, and receipt logic.
3. Do not make live provider calls during tests unless explicitly configured.
4. Provider adapters must support dry-run mode.
5. Every model call route must be able to produce a model-call receipt.
6. The scheduler must not call providers directly.
7. Preserve production_authority=false.
8. Update manifest, checksums, and receipts.
9. If existing scheduler/runtime files already implement overlapping concepts, integrate rather than duplicate.
10. If any test fails, classify it honestly as missing file, broken path, stale test, environment issue, true logic defect, or deferred integration.

Required outputs:
- architecture protocols
- registries/policies
- runtime modules
- provider adapter stubs
- unit tests
- manifest update
- checksum update
- implementation receipt
- packaged zip

Primary completion standard:
ION can classify a model-call intent, choose an appropriate model/provider route under cost/quality/latency/risk constraints, check capacity and budget, generate a dry-run provider-neutral result, and write a model-call receipt without claiming production authority.
```

---

# 23. Final Steward Directive

```text
Build the organ that lets ION choose models lawfully.
```

Not the most famous model.  
Not the cheapest model blindly.  
Not the highest-quality model wastefully.  
Not the fastest model recklessly.  
Not the easiest provider by habit.

The correct model for the call, under the current work class, risk level, context size, latency requirement, budget envelope, provider capacity, privacy posture, and evidence history.

That is the subsystem Steward must implement.
