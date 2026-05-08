# ION Product Reconciliation Matrix - Phase 4

Status: candidate product architecture reconciliation, not accepted canon.

Created: 2026-05-08T18:22:28Z

Active root:

```text
/home/sev/ION - Production/ION_CODEX FULL
```

Source package:

```text
ION_FULL_GPT_SANDBOX_AGENT_PACKAGE_v1_4_AI_ASSISTANT_WORK_TEMPLATE_INSTANCE_EXERCISES_CANDIDATE_20260508T154333Z
```

## Purpose

This matrix reconciles the active full build with the v1.4 package product
lane. The goal is to keep each product surface honest about what it owns:

- Codex Capsule Chat
- Custom GPT Action Gateway
- MCP JSON-RPC Custom GPT Action
- browser data-zip Custom GPT product
- local cockpit
- full ION role pipeline

The new Assistant Work route compiler may classify work for these surfaces, but
candidate routes are metadata only. They do not promote package registries into
`ION/03_registry/` and do not change product front-door law.

## Core Finding

The active full build and the package product are complementary, not competing.

```text
active build = live local connector/runtime surface
package product = portable browser-sandbox continuity surface
Codex Capsule Chat = local operator engineering chat with Capsule context
full ION = governed multi-role workflow and proof settlement
```

The route compiler should become a shared classifier across them, while each
surface keeps its own authority ceiling, persistence model, proof path, and
recovery mode.

## Reconciliation Matrix

| Lane | User-facing role | Persistence model | Proof path | Receipt path | Authority ceiling | Route metadata use | Primary failure | Recovery action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Codex Capsule Chat | Normal operator chat with Codex-quality responses and optional bounded work queueing. | `ION/05_context/current/codex_solo/` plus chat state/model files. Capsule is minimum context; Mini is lookup/receipt index. | Chat engine turn, selected skill, native lenses, model move, response carrier proof, queue proof when used. | Capsule post, Codex task return, response carrier run packet. | No production/live/secrets authority; bounded queue only through existing connector owner. | Selects candidate assistant-work route for chat objective shaping, trace visibility, and queued-work context. | Slow or missing response carrier; drift into UI chores or raw ION internals; missing route refs. | Fall back to visible local response, show execution status, hydrate proof returns, use Capsule/Hot Context recovery. |
| Custom GPT Action Gateway | Browser Custom GPT Action for bounded validation, context reads, receipts, and approved submits. | Active local repo state through public HTTPS tunnel to local gateway. | Bearer auth, schema validation, idempotency, hard-gate refusals, approval evidence before submit. | Gateway receipts and ChatOps/owner receipts. | Non-production, non-live; protected routes require bearer token; mutations require approval evidence. | May use route metadata to classify submitted action intent before validation/submit. | Auth missing, token mismatch, 502 tunnel/backend failure, schema invalid, missing approval, idempotency replay. | Test `/health`, then `/policy`/reads, validate before submit, inspect gateway refusal class and service/tunnel status. |
| MCP JSON-RPC Custom GPT Action | Browser Custom GPT Action wrapper around existing ION MCP preview for broad read/status/tool calls. | Active local repo/runtime through `https://ion.helixion.net/mcp` tunnel. | MCP method response, tool manifest, bounded write confirmation where applicable. | MCP tool results; downstream owner receipts for bounded tools. | Non-production, non-live; no shell/secrets/production/deploy authority; bounded write tools require confirmation. | May expose route/compiler status and assistant-work metadata as read/status tools, but should not become submit owner. | 502 tunnel/backend failure, ResponseTooLarge, unsupported method, tool-level refusal, missing confirmation. | Start/check MCP preview and tunnel, call `ping`, `tools/list`, then bounded read/status tools before any write-gated tool. |
| Browser Data-Zip Custom GPT Product | Portable Custom GPT continuity mode when live connectors are absent or not desired. | User-mounted data zip; exported data zip is the durable state carrier. GPT chat itself is not persistent state. | Manifest/state/schema checks, package-local receipt append, export protocol. | `RECEIPTS/receipt_ledger.jsonl` inside exported data package; export receipt. | Browser sandbox only; cannot mutate live repo, daemon, GitHub, or local services. | May use assistant-work route registry inside the data package as candidate product-local classifier. | User forgets to export, stale zip remounted, GPT treats conversation memory as state, package schema drift. | Mount manifest first, verify current state, append receipt for meaningful updates, export a new zip and carry it forward. |
| Local Cockpit | Operator visibility and control surface for local status, chat, queues, services, traces, and receipts. | Dynamic local model from active repo state; optional saved active model surfaces. | Read-only health/status plus explicit chat/queue endpoints with existing gates. | Existing Capsule, task-return, gateway, and service receipts. | Local visibility; public access requires signed cockpit session/token/Google auth when configured; no production/live authority. | Displays route counts, selected route traces, and route findings to help diagnose classification without making the operator route manually. | Service stopped, stale model, auth not configured, public tunnel down, UI monolith/drift. | Use systemd service status, `/health`, `/chat/model.json`, route drawer, timeline, and service runbook checks. |
| Full ION Role Pipeline | Governing multi-role workflow: Relay, Steward, Vizier, Mason/Codex, Vice, Nemesis, return/Persona. | Accepted ION state surfaces, queues, packets, receipts, and active registries. | Template action proof, Steward/human acceptance, task return, receipt-backed settlement. | Formal ION receipts and accepted state updates. | Highest governance in this project, but still no production/live/deploy authority unless explicitly granted through accepted law. | Candidate route metadata can suggest domain fan-out and specialist proof needs, but accepted ION roles/templates decide. | Candidate classifier mistaken for law, role bypass, missing acceptance, unreceipted state mutation. | Route through accepted front door, require proof gates, settle via receipts, promote/reject candidate routes only after review. |

## Route Compiler Placement

The route compiler belongs at the classification layer:

```text
operator message or action payload
-> assistant-work candidate route metadata
-> surface-specific behavior
-> accepted proof/receipt owner
```

It must not become an authority owner:

```text
route metadata != registry promotion
route metadata != state acceptance
route metadata != production/live authority
route metadata != autonomous execution
```

## Surface Boundaries

### Codex Capsule Chat

Codex Capsule Chat is the primary local operator chat. It should behave like a
high-quality Codex/ChatGPT conversation while quietly carrying ION context:
Capsule, Mini lookup, Hot Context, native lenses, skills, model moves, response
carrier, and proof hydration.

The route compiler improves this lane by preventing generic routing. A UI task
can now carry `route.ui_specialist_work`, a docs task can carry
`route.documentation_specialist_work`, and implementation work can carry
`route.ide_agent_work_map`. The user should see this in inspector/traces, not
as a chore.

### Action Gateway

The Action Gateway is the approval-gated submit membrane for Custom GPT
Actions. It is the right lane for validate-before-submit, work-packet drafts,
receipt reads, and bounded approved submissions.

It should not become the broad MCP tool surface, and it should not bypass
approval just because a Custom GPT can call it.

### MCP JSON-RPC Action

The MCP Action is the broad read/status/tool wrapper for Custom GPTs. It is
useful because Custom GPT Actions can call OpenAPI schemas even when Custom GPT
Builder does not expose normal MCP connectors.

It should remain the discovery and read/status surface. Bounded write tools must
keep their own confirmation and owner gates.

### Browser Data-Zip Custom GPT Product

The package product is the offline/portable continuity lane. It is especially
valuable when the user's PC, tunnels, or local services are unavailable.

It should not pretend to be the live full build. Its correct product promise is:

```text
I can mount your project memory package, continue from accepted state, append
receipts, and export a new continuity package.
```

### Local Cockpit

The cockpit is the visibility surface. It should show the operator:

- which services are up
- which tunnels are up
- which chat turn selected which route
- what context the chat carried
- which queue/run/receipt is connected
- which proof is accepted or blocked

The cockpit should not ask the user to manually become the ION router.

### Full ION Pipeline

Full ION remains the governed workflow. Candidate assistant-work routes can
feed it, but only accepted templates, proof gates, Steward/human acceptance, and
receipts can land state.

## Promotion Path

The correct order is:

1. Keep assistant-work route compiler candidate-only.
2. Observe route metadata through Codex chat, gateway validations, MCP reads,
   cockpit traces, and package-product continuity.
3. Record failures and missing domains/templates.
4. Promote only selected route/domain/template pieces into accepted ION
   registries after review.
5. Keep package product and live connector product as separate lanes with a
   bridge/export story, not as one blurred runtime.

## Candidate Next Work

Recommended next implementation packets:

1. Add route metadata to Action Gateway validation responses, still candidate
   only. Done:
   `ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_GATEWAY_ROUTE_METADATA_RECEIPT_20260508T182713Z.json`.
2. Add a read-only MCP tool for `ion_assistant_work_route_surface` and optional
   route classification preview. Held for explicit tool-contract/front-door gate
   because this requires MCP tool policy and Custom GPT Action schema updates.
3. Add cockpit display coverage for current route distribution across recent
   Codex chat turns.
4. Draft Custom GPT product instructions that distinguish the live Actions lane
   from the data-zip continuity lane.
5. Create a promotion proposal for only the safest accepted assistant-work
   templates: terminal proof receipt, screen state matrix, and API docs example
   validation.

## Non-Claims

- This matrix does not accept the v1.4 package as ION canon.
- This matrix does not mutate `ION/03_registry/`.
- This matrix does not mutate the product front door.
- This matrix does not grant production, live execution, secrets, deploy, Git
  push, or arbitrary shell authority.
- This matrix does not claim the live tunnels are currently running; service
  status must be checked separately.
