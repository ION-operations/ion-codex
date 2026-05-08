# ION Full GPT Sandbox Agent Package v1.4 - AI Assistant Work Evolution Diff

Status: evidence report and promotion plan, not accepted canon.

Source package:

```text
ION_FULL_GPT_SANDBOX_AGENT_PACKAGE_v1_4_AI_ASSISTANT_WORK_TEMPLATE_INSTANCE_EXERCISES_CANDIDATE_20260508T154333Z
```

Active comparison root:

```text
/home/sev/ION - Production/ION_CODEX FULL
```

## Executive Finding

The package contains a substantial candidate subsystem that is absent from the
active full build: `ION/05_context/current/ai_assistant_work/`.

This subsystem turns AI-assisted work itself into a governed ION domain system:
chat, IDE, CLI, cloud-agent, PR-agent, background-agent, and hybrid work are
modeled as first-class work embodiments with domains, specialist agents, state
families, protocols, templates, proof requirements, failure modes, route
registries, validation notes, and settlement paths.

The package should not be copied blindly. Its own authority boundary says it is
candidate current state, not accepted canon, and that it does not mutate
`ION/03_registry/` or product front-door law.

## Source Integrity

- Zip SHA-256:
  `0af4e5074c548389e646383a50020168e2d3f08f3df0ff0de94658bed4175e50`
- Identical zip copies found under `/home/sev/ION - Production/` and
  `/home/sev/Downloads/`.
- Extracted package file count: 3756.
- `ai_assistant_work` file count: 139.

Metadata caveat:

- Outer package label says v1.4 assistant-work/template-instance exercise
  candidate.
- `PRODUCT_MANIFEST.json` and `VALIDATION_REPORT.json` still identify
  `ION_FULL_GPT_SANDBOX_AGENT_PACKAGE_v1_1_PERSONA_RELAY_STALE_SURFACE_AUDIT`.
- Treat the package as a v1.4 candidate overlay with stale root metadata, not as
  a cleanly relabeled product release.

## What The Package Adds

### 1. AI Assistant Work As A First-Class Domain System

The central conceptual correction in the package is:

```text
An AI assistant is a model-powered work interface mounted in a host body with
particular context surfaces, tools, memory, authority, workflows, proof
obligations, and handoff/receipt paths.
```

This is highly relevant to our Codex CLI chat and Custom GPT work. It shifts the
system away from "one generic assistant does everything" and toward governed
assistant embodiments:

- browser chat
- IDE agent
- CLI agent
- cloud/background agent
- PR agent
- hybrid assistant workflow

### 2. Candidate Domain Registry

The latest candidate domain registry contains 29 domains.

Seeded domains include:

- AI Assistant Identity and Embodiment
- Chat Work
- IDE Work
- Codebase Understanding
- Planning and Task Breakdown
- Implementation
- UI/UX Specialist Work
- Documentation and Writing
- Testing and Quality
- Review, Safety, and Security
- Debugging and Observability
- DevOps, CI/CD, and Release
- Data and Analysis
- Product and Requirements
- Knowledge, Context, and Memory
- Dependency and Package
- Workflow Automation and Tooling
- Assistant Work Dataset and Taxonomy
- Cross-Domain Settlement

Dataset-mined fission domains include:

- PR Agent Work
- Background Queue Intake
- Terminal Proof
- UI State Modeling
- Documentation Example Validation
- Release Evidence
- Migration Work
- Assistant Work Observation
- Incident Triage
- Untrusted Input Tool Guard

### 3. Candidate Specialist Agent Registry

The package reports 71 candidate specialist agents. These are not a replacement
for ION role law. They are domain-local specialist interfaces that carry context,
proof obligations, drift resistance, and return contracts.

Important examples for our current work:

- `CHAT_STEWARD`
- `IDE_CARTOGRAPHER`
- `WORKSPACE_STEWARD`
- `CODEBASE_CARTOGRAPHER`
- `TASK_PLANNER`
- `PATCH_MASON`
- `UI_ARCHITECT`
- `UX_FLOW_DESIGNER`
- `COMPONENT_BUILDER`
- `DESIGN_SYSTEM_STEWARD`
- `ACCESSIBILITY_AUDITOR`
- `DOCS_ARCHITECT`
- `TECHNICAL_WRITER`
- `TEST_ARCHITECT`
- `REGRESSION_HUNTER`
- `CODE_REVIEWER`
- `SECURITY_NEMESIS`
- `CONTEXT_CARTOGRAPHER`
- `MEMORY_STEWARD`
- `TOOL_STEWARD`
- `SETTLEMENT_STEWARD`

This is directly relevant to the UI failure we diagnosed: UI work should not be
routed through a generic implementation lane when a UI/UX specialist domain is
available.

### 4. Assistant Work Dataset

The package seeds an assistant-work observation corpus:

- 36 entries
- 7 assistant embodiments: chat, IDE, CLI, cloud-agent, PR-agent,
  background-agent, hybrid
- 19 seeded domain coverage with no missing seeded domains
- 47 seeded specialist-agent coverage with no missing seeded agents
- 68 candidate failure modes
- 67 template coverage entries
- 70 state surface coverage entries
- 57 protocol coverage entries
- 13 candidate template gaps
- 13 candidate agent/domain gaps

This is the strongest bridge between our lived development failures and a
governed route system. It gives ION a way to classify the kind of assistant work
being attempted before choosing a template, tool, role, model, or proof gate.

### 5. Template Specs, Instances, And Boot Exercises

The package adds seven machine-checkable candidate template specs:

- `screen_state_matrix_packet`
- `pr_review_packet`
- `background_queue_result_intake_packet`
- `terminal_proof_receipt_packet`
- `api_docs_example_validation_packet`
- `release_readiness_matrix_packet`
- `migration_plan_and_rollback_packet`

For each template spec, the package includes:

- one minimal valid instance
- one expected rejection instance
- validation logic
- simulation report

It also includes seven agent boot exercises:

- `BACKGROUND_QUEUE_STEWARD`
- `EXAMPLE_RUNNER`
- `MIGRATION_MASON`
- `PR_REVIEW_STEWARD`
- `RELEASE_EVIDENCE_CURATOR`
- `TERMINAL_PROOF_CURATOR`
- `UI_STATE_MODELER`

Package-reported validation:

- valid instances accepted: 7/7
- expected rejections accepted as rejections: 7/7
- boot exercises accepted: 7/7
- focused tests: 48 passed
- findings: 0

### 6. Product Custom GPT Adapter

The package contains:

```text
product/custom_gpt_adapter/
product/data_schema/
product/starter_data/
product/package_guides/
```

This is a data-zip continuity product lane. It teaches a browser Custom GPT to
mount an ION data package, operate from accepted state, append receipts, and
export continuity data.

That is different from the active full build, which now has:

```text
ION/09_integrations/custom_gpt_action_gateway/
ION/09_integrations/chatgpt_browser_mcp_action/
```

The active build is a live connector/action surface. The package product adapter
is a portable browser-sandbox continuity surface. They should be reconciled, not
treated as competing systems.

## Diff Against Current Full Build

### Present In Package, Absent In Active Full Build

- `ION/05_context/current/ai_assistant_work/`
- AI assistant work domain registry
- AI assistant work agent registry
- assistant work route, state, protocol, template, failure-mode registries
- assistant work dataset genesis corpus
- domain fission candidates
- seven machine-checkable assistant-work template specs
- seven valid template instances
- seven expected rejection template instances
- seven agent boot exercise packets
- five focused test files for assistant-work candidate validation
- product-level browser Custom GPT data-zip adapter and data schemas

### Present In Active Full Build, Not The Package Focus

- live local MCP HTTP preview and Cloudflare tunnel runtime
- Custom GPT Action Gateway OpenAPI surface
- MCP JSON-RPC Custom GPT Action OpenAPI surface
- Codex capsule chat and response carrier work
- local cockpit app/auth/service status work
- systemd user service templates for local ION services

### Shared Or Related Surfaces

- GPT sandbox carrier profile and session packet
- single-carrier sequential runtime protocol
- Persona/Relay front-door boundary
- sandbox preflight and stale-surface audit logic
- productized runtime framing
- proof/receipt/state boundary

## Diff Against Current Custom GPT/Product Build

Current active Custom GPT/product work is connector-first:

- Action 1: ION Action Gateway at `ion-actions.helixion.net`
- Action 2: ION MCP JSON-RPC action at `ion.helixion.net/mcp`
- auth-gated reads/submits
- local services and Cloudflare tunnels
- live but non-production authority posture

The package Custom GPT product is package-first:

- browser Custom GPT mounts an ION data zip
- GPT operates on package state inside browser sandbox
- receipts are appended to exported continuity package
- persistence is the data zip, not the GPT conversation

Recommended reconciliation:

- Keep the active Action Gateway/MCP surfaces for local live status, bounded
  queueing, and read/status tooling.
- Preserve the package adapter as the portable continuity fallback for Custom
  GPTs without live connector access.
- Add assistant-work route classification so both surfaces can decide whether a
  turn is chat, IDE, CLI, PR, background, release, docs, UI, terminal proof,
  migration, or settlement work.
- Do not expose package candidate registries as accepted law until they are
  reviewed, adapted, and receipted in the active build.

## Active-Root Candidate Import

Phase 1 has now been performed as a bounded candidate import.

Imported surfaces:

- `ION/05_context/current/ai_assistant_work/`
- `ION/tests/test_kernel_ai_assistant_work_domain_candidate.py`
- `ION/tests/test_kernel_ai_assistant_work_dataset_genesis.py`
- `ION/tests/test_kernel_ai_assistant_work_domain_fission_candidate.py`
- `ION/tests/test_kernel_ai_assistant_work_agent_boot_template_specs.py`
- `ION/tests/test_kernel_ai_assistant_work_template_instances.py`

Local active-root adaptation:

- The imported validators were designed to support `python -S`, but the active
  machine's PyYAML install is under the user site-packages path.
- The three validators now add the version-derived user site-packages path before
  importing `yaml`.
- This is a local portability patch only; it does not change candidate
  validation logic.

Import receipt:

```text
ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_ACTIVE_ROOT_CANDIDATE_IMPORT_RECEIPT_20260508T174843Z.json
```

Local validation:

- `validate_ai_assistant_work_template_instances.py`: accepted candidate
  validation.
- `validate_ai_assistant_work_candidate.py`: accepted candidate evidence.
- `validate_ai_assistant_work_dataset_genesis.py`: accepted candidate evidence.
- focused pytest over five assistant-work tests: `36 passed`.
- active `ion_status`: `ION_STATUS_READY`.
- active state integrity audit: `ION_ACTIVE_STATE_INTEGRITY_READY`.
- status/integrity pytest: `8 passed`.

Authority boundary remains unchanged:

- candidate only
- no `ION/03_registry/` mutation
- no product front-door mutation
- no production/live authority
- explicit acceptance still required to land

## Promotion Plan

### Phase 0 - Evidence Freeze

Done:

- Source package located.
- Zip hash recorded.
- Key package state and validation surfaces read.
- Active full build absence confirmed for `ai_assistant_work`.
- No candidate files promoted.

### Phase 1 - Candidate Import, Still Non-Canon

Done:

- `ION/05_context/current/ai_assistant_work/` imported into active root.
- Five focused assistant-work tests imported.
- Active-root candidate import receipt added.

Guard:

- No `ION/03_registry/` mutation.
- No product front-door mutation.
- No route/compiler activation yet.

### Phase 2 - Active-Root Validation

Done for the candidate import:

- validate the copied candidate files parse correctly
- run the five assistant-work tests
- verify the package's `python -S` validation posture works in this active
  environment
- record validation receipt

Still pending before promotion:

- route compiler review
- product/front-door reconciliation
- selected registry landing proposal

### Phase 3 - Route Compiler Review

Review the package next packet:

```text
AI_ASSISTANT_WORK_NEXT_PACKET_ROUTE_COMPILER_AND_PROMOTION_PLAN
```

The route compiler should map assistant-work domains to existing ION carrier
surfaces:

- Codex CLI chat/capsule
- Custom GPT Action Gateway
- MCP JSON-RPC action
- browser Custom GPT data-zip adapter
- future local cockpit UI
- ION full role pipeline

### Phase 4 - Product Reconciliation

Produce one product matrix:

- live connector product lane
- package continuity product lane
- capsule chat lane
- full ION role pipeline lane
- local cockpit lane

Each lane needs:

- authority ceiling
- persistence model
- proof path
- receipt path
- user-facing behavior
- failure mode
- recovery action

Done:

- `ION/06_intelligence/research/sandbox_agent_package_evolution/2026-05-08_phase4_product_reconciliation_matrix.md`
- `ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_PHASE4_PRODUCT_RECONCILIATION_RECEIPT_20260508T182228Z.json`

Core settlement:

```text
active build = live local connector/runtime surface
package product = portable browser-sandbox continuity surface
Codex Capsule Chat = local operator engineering chat with Capsule context
full ION = governed multi-role workflow and proof settlement
```

The lane matrix now reconciles:

- Codex Capsule Chat
- Custom GPT Action Gateway
- MCP JSON-RPC Custom GPT Action
- browser data-zip Custom GPT product
- local cockpit
- full ION role pipeline

The route compiler is assigned to classification only. It does not own
authority, persistence, proof acceptance, or registry promotion.

### Phase 5 - Acceptance Or Rejection

Only after review:

- promote selected registries into accepted ION registry surfaces
- reject or revise weak domains/agents/templates
- bind accepted templates through existing ION template-action gates
- update Custom GPT instructions and Codex chat routing from accepted surfaces

## Immediate Recommendation

Proceed to Phase 3: route compiler review.

The high-value next target is mapping the imported assistant-work taxonomy into
the active Codex chat, Custom GPT Action Gateway, MCP Action, local cockpit, and
full ION role pipeline without promoting the candidate registry to law too early.

Route compiler review now recorded:

- `ION/05_context/current/ai_assistant_work/route_compiler/AI_ASSISTANT_WORK_ROUTE_COMPILER_REVIEW_20260508T175230Z.md`
- `ION/05_context/current/ai_assistant_work/route_compiler/AI_ASSISTANT_WORK_ROUTE_COMPILER_CANDIDATE_MAP_20260508T175230Z.json`
- `ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_ROUTE_COMPILER_REVIEW_RECEIPT_20260508T175340Z.json`

Next implementation target:

```text
ION/04_packages/kernel/ion_assistant_work_route_compiler.py
ION/tests/test_kernel_ion_assistant_work_route_compiler.py
Codex Chat inspector -> Route -> Assistant Work route
```

Route compiler implementation now recorded:

- `ION/04_packages/kernel/ion_assistant_work_route_compiler.py`
- `ION/tests/test_kernel_ion_assistant_work_route_compiler.py`
- `ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_ROUTE_COMPILER_IMPLEMENTATION_RECEIPT_20260508T181926Z.json`

Active integration:

- Codex chat engine turns now carry `assistant_work_route` metadata.
- Codex chat engine surface now exposes `assistant_work_routes`.
- Queued Codex objectives include the selected candidate route, candidate
  domains/agents, include/forbid contract, and explicit non-promotion boundary.
- Turn traces include an `assistant_work_route` event for transparency.
- The right inspector exposes an `Assistant Work Routes` drawer with verdict,
  route count, mapped count, candidate map, registry path, and findings.

Validation:

- focused route/compiler/chat tests: `24 passed`.
- assistant-work candidate tests: `36 passed`.
- active `ion_status`: `ION_STATUS_READY`.
- active state integrity audit: `ION_ACTIVE_STATE_INTEGRITY_READY`.

Authority boundary:

- candidate metadata only
- no `ION/03_registry/` mutation
- no product front-door mutation
- no production/live/secrets authority

Phase 4 is now documented. Next implementation targets:

```text
1. Add candidate route metadata to Action Gateway validation responses. DONE.
2. Add read-only MCP tool for assistant-work route surface and route preview.
   HELD for explicit MCP tool policy / Custom GPT Action schema gate.
3. Add cockpit route-distribution visibility across recent Codex chat turns.
4. Draft Custom GPT instructions distinguishing live Actions from data-zip continuity.
5. Prepare selected template promotion proposal.
```

Action Gateway route metadata receipt:

```text
ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_GATEWAY_ROUTE_METADATA_RECEIPT_20260508T182713Z.json
```

## Non-Claims

- This report does not claim the package is accepted ION canon.
- This report does not claim the active build has accepted the assistant-work
  subsystem as canon.
- This report does not claim the package validation was rerun in the active root.
- This report does not promote any package file into `ION/03_registry/`.
- This report does not grant production, live execution, secret, deployment, or
  external tool authority.
