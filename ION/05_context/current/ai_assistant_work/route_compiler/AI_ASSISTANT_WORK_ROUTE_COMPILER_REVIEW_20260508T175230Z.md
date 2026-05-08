# AI Assistant Work Route Compiler Review

Status: candidate review, not accepted canon.

This review executes the package next-packet in a bounded way: it maps the
imported AI Assistant Work route registry against the active Codex chat, Custom
GPT Action Gateway, MCP Action, local cockpit, and full ION workflow surfaces
without landing any registry or product-front-door law.

## Inputs

- `ION/05_context/current/ai_assistant_work/next/AI_ASSISTANT_WORK_NEXT_PACKET_ROUTE_COMPILER_AND_PROMOTION_PLAN_20260508T154333Z.json`
- `ION/05_context/current/ai_assistant_work/registries/AI_ASSISTANT_WORK_ROUTE_REGISTRY_CANDIDATE_V0_1.yaml`
- `ION/03_registry/ion_skill_registry.yaml`
- `ION/03_registry/ion_native_lens_registry.yaml`

Machine map:

```text
ION/05_context/current/ai_assistant_work/route_compiler/AI_ASSISTANT_WORK_ROUTE_COMPILER_CANDIDATE_MAP_20260508T175230Z.json
```

## Main Finding

The imported assistant-work routes map cleanly to existing active surfaces, but
the active build does not yet have a route compiler that uses them.

The right move is not to expose 71 specialist agents to the user. The right move
is to let the chat engine classify intent behind the scenes and choose the right
route, skill, lens, template, proof, and receipt path.

## Active Route Fit

### Assistant Identity

Use for questions like "what is an AI assistant" or "how should Codex/Custom GPT
operate."

Active fit:

- skills: `codex-chat-answer`, `context-mount`, `template-curation`
- lenses: `persona`, `ionologist`, `context_cartographer`, `thoth`
- output: explanation with host body, context surfaces, authority, state/proof,
  and receipt boundary

### IDE Agent Work

Use for coding-agent and workspace tasks.

Active fit:

- skills: `codex-solo-work`, `codex-recovery`, `context-mount`
- lenses: `relay`, `steward`, `context_cartographer`, `mason_codex`,
  `nemesis`
- output: workspace map, bounded write scope, validation loop, proof receipt

This should become the default route for Codex CLI work inside the chat app.

### UI Specialist Work

Use for UI/UX/frontend requests.

Active fit:

- skills: `codex-solo-work`, `template-curation`
- lenses: `vizier`, `mason_codex`, `nemesis`, `persona`
- candidate template: `screen_state_matrix_packet`

This route directly addresses the prior UI failure mode. The first artifact for
serious UI work should be a screen-state matrix and component contract, not a
generic implementation pass.

### Documentation Specialist Work

Use for docs, README, changelog, API docs, and product explanations.

Active fit:

- skills: `codex-chat-answer`, `codex-solo-work`, `template-curation`
- lenses: `thoth`, `scribe`, `context_cartographer`, `nemesis`
- candidate template: `api_docs_example_validation_packet`

Docs should carry reader model, source authority, claim map, and version
boundary.

### Assistant Work Dataset Build

Use for expanding the taxonomy of AI-assisted work itself.

Active fit:

- skills: `template-curation`, `context-mount`, `receipt-post`
- lenses: `template_curator`, `context_cartographer`, `vestige`, `scribe`
- output: observation corpus, failure modes, template gaps, source lineage

### Cross-Domain Feature Delivery

Use for "build this" requests that naturally span product, UI, implementation,
tests, docs, release, and settlement.

Active fit:

- skills: `ion-full-workflow-handoff`, `codex-solo-work`, `receipt-post`
- lenses: `relay`, `steward`, `vizier`, `mason_codex`, `nemesis`, `scribe`,
  `persona`
- output: fan-out/fan-in plan, proof per branch, settlement receipt

## Fission Backlog

The v1.4 package has template specs for route families that are not yet exposed
in the v0.1 route registry. These should become second-pass routes:

- PR agent work -> `pr_review_packet`
- background queue intake -> `background_queue_result_intake_packet`
- terminal proof -> `terminal_proof_receipt_packet`
- release evidence -> `release_readiness_matrix_packet`
- migration work -> `migration_plan_and_rollback_packet`
- documentation example validation -> `api_docs_example_validation_packet`
- UI state modeling -> `screen_state_matrix_packet`

## Implementation Target

Build a small active route compiler with this behavior:

1. Input: user message, selected UI mode, current skill, and current authority.
2. Match candidate assistant-work route by triggers and intent features.
3. Return: route id, selected skill, active lenses, candidate template specs,
   proof obligations, authority warnings, and next action.
4. Surface this in Codex chat as internal route metadata and in the inspector,
   not as user chores.
5. Keep writes behind the existing Codex/ION proof and receipt gates.

Recommended active module after acceptance:

```text
ION/04_packages/kernel/ion_assistant_work_route_compiler.py
```

Recommended active test after acceptance:

```text
ION/tests/test_kernel_ion_assistant_work_route_compiler.py
```

Recommended provisional UI exposure:

```text
Codex Chat inspector -> Route -> Assistant Work route
```

## Promotion Matrix

| Surface | Current Status | Next Action |
| --- | --- | --- |
| `ai_assistant_work` candidate tree | imported and validated | keep candidate |
| route compiler map | drafted | implement compiler behind candidate flag |
| active skill registry | unchanged | no mutation until route compiler proves useful |
| native lens registry | unchanged | no mutation until route compiler proves useful |
| Custom GPT Action Gateway | live separate surface | consume route metadata later |
| MCP JSON-RPC Action | live separate surface | expose read/status route metadata later |
| Codex chat | active app surface | first target for internal route metadata |
| full ION workflow | existing lane | map cross-domain feature requests to handoff |

## Non-Claims

- This review does not accept candidate assistant-work routes as ION law.
- This review does not mutate `ION/03_registry/`.
- This review does not alter Custom GPT product instructions.
- This review does not execute external agents or production actions.

