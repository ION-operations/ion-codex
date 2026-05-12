# DAIMON_EXTENSION_JOC_AUTOMATION_LINEAGE_SYNTHESIS

Status: active architecture synthesis
Created: 2026-05-10
Decision source: operator decision to consolidate older JOC automation protocols into the current portable dAimon extension design
Authority posture: lineage and architecture witness, not live unrestricted browser-control authority

## Purpose

This synthesis binds older ION/JOC cockpit, automation, visual-harness, browser-sandbox, and file-attachment protocols into the current portable dAimon companion architecture.

The dAimon extension companion must not invent a fresh automation model. It inherits the JOC cockpit grammar and the existing ION safety model, then adapts those surfaces to browser-carrier queue work, GPT Actions packets, DOM/page perception, receipts, and approved local mutation.

## Core decision

Older JOC is the primary UI and automation model for the portable dAimon companion.

The dAimon extension companion is a portable JOC micro-shell adapted to browser-carrier needs, not a generic extension popup.

The old JOC visual language is canon. The content model evolves for ION/dAimon browser work.

## Inherited protocol set

| Inherited protocol | Path | Adopted role |
| --- | --- | --- |
| JOC cockpit shell component contract | `ION/02_architecture/ION_JOC_COCKPIT_SHELL_COMPONENT_CONTRACT_PROTOCOL.md` | Primary UI layout grammar for the portable companion. |
| JOC reactive OS stream and automation view model | `ION/02_architecture/ION_JOC_REACTIVE_OS_STREAM_AND_AUTOMATION_VIEW_MODEL_PROTOCOL.md` | Visible automation event rail and blocked-capability stream. |
| JOC dry-run dispatch execution trace | `ION/02_architecture/ION_JOC_DRY_RUN_DISPATCH_EXECUTION_TRACE_VIEW_MODEL_PROTOCOL.md` | Blueprint for GPT Actions to browser queue tracing. |
| Local visual harness prototype | `ION/02_architecture/LOCAL_VISUAL_HARNESS_PROTOTYPE_PROTOCOL.md` | Perception and visual evidence intake model. |
| Visual fixture runner sandbox review | `ION/02_architecture/VISUAL_FIXTURE_RUNNER_LOCAL_SANDBOX_REVIEW_PROTOCOL.md` | Gate that keeps browser execution behind sandbox review. |
| Local browser execution sandbox spec | `ION/02_architecture/LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC_PROTOCOL.md` | Safety floor for any future execution harness. |
| Browser file attachment automation | `ION/02_architecture/ION_BROWSER_FILE_ATTACHMENT_AUTOMATION_PROTOCOL.md` | First concrete screen/DOM calibration lane. |
| Automation state protocol | `ION/02_architecture/AUTOMATION_STATE_PROTOCOL.md` | Runtime maturity ladder and status vocabulary. |
| Portable page companion product context | `ION/02_architecture/PORTABLE_ION_PAGE_COMPANION_001_PRODUCT_CONTEXT.md` | Product shell that carries ION/dAimon across pages. |
| Browser perception domain design | `ION/02_architecture/DOM_PERCEPTION_001_BROWSER_PERCEPTION_DOMAIN_DESIGN.md` | Page perception, branch, evidence, and trust model. |

## Companion UI model

The portable dAimon companion must use JOC micro-shell layout logic:

| Zone | JOC inheritance | dAimon browser-carrier adaptation |
| --- | --- | --- |
| Top status bar | Steward/council state, mode, current work status | Carrier health, gateway health, model/queue mode, claimed packet, blocked capability summary. |
| Left or side rail | Primary mode selection | Status, Queue, Page, Evidence, Actions, Receipts, Settings, Diagnostics. |
| Main work surface | Maintained work surface | Current packet, prompt/result, page branch, workflow plan, approval state. |
| Right inspector/drawers | Receipts, evidence, claims, graph details | DOM/page evidence, target calibration, packet JSON, context refs, approval proof, local mutation proof. |
| Bottom timeline/log rail | Automation/reaction/repair timeline | Output-stopped detector, autoplay turns, claim/result lifecycle, receipts, errors, blocked actions. |

Visual grammar:

| Visual rule | Required posture |
| --- | --- |
| Aesthetic | DXL matte-black instrument panel. |
| Labels | Compact monospace, dense, telemetry-first. |
| Density | Command/mission dashboard feel, not consumer SaaS whitespace. |
| Status | Explicit mode, authority, queue, health, and blocked-capability surfaces. |
| Motion | Functional event changes only, not decorative motion. |
| Controls | Visible pause, kill, approval, retry, details, and receipt controls. |

## Feature inheritance map

Every new queue or companion feature must map to inherited protocol or be marked new.

| Current or planned feature | Inherited model | Status |
| --- | --- | --- |
| Browser queue packets | Dry-run dispatch trace plus automation state protocol | Inherited and adapted. |
| GPT Actions-created packet visibility | Dry-run dispatch trace, reactive OS stream | Inherited and adapted. |
| Autoplay after output stops | Dry-run dispatch trace: simulate prompt injection, wait, extraction receipt | New live carrier slice under inherited trace model. |
| Pause and kill switch | Automation state protocol: suspended/disabled, reactive blocked state | Inherited and adapted. |
| Output-stopped detector | Reactive OS stream event plus dry-run response wait phase | Inherited and adapted. |
| Current claimed packet panel | JOC main work surface and right inspector | Inherited and adapted. |
| Assistant result capture | Dry-run extraction receipt phase | New live carrier slice under inherited receipt model. |
| Visible receipts | Cockpit right inspector, bottom timeline, receipt rail | Inherited. |
| DOM/page evidence panel | Local visual harness plus DOM perception domain | Inherited and adapted. |
| Page branch and workflow memory | Portable companion plus Living Operational Graph model | Inherited from current dAimon product context. |
| Attachment/drop target calibration | Browser file attachment automation protocol | Inherited concrete lane. |
| Inspector frame capture and element targets | Local visual harness, browser perception, attachment automation calibration | Inherited and adapted. |
| Approval gate panel | JOC operator handoff, dry-run handoff, file attachment protocol | Inherited and adapted. |
| Gated local mutation proof | Automation state protocol plus browser file attachment local-operator lane | Inherited and adapted. |
| Carrier health/status | JOC top bar and reactive OS stream | Inherited and adapted. |
| Blocked capability warnings | Reactive OS blocked-capability rail and browser sandbox spec | Inherited. |
| Context carried to ChatGPT/Codex | Portable companion graph plus carrier message receipts | Inherited from current dAimon context model. |
| Browser-queue gateway endpoints | No older direct equivalent | New, must remain governed by dry-run trace, queue receipts, and automation state. |
| Custom GPT Actions enqueue bridge | No older direct equivalent | New, must remain typed API bridge only, not background agency. |

## V1 authority posture

Current v1 authority is explicitly bounded:

| Capability | V1 authority |
| --- | --- |
| Autoplay queue | Allowed for bounded packets with visible state, pause, kill, and receipts. |
| Gated local mutation | Allowed only through approval, policy gates, and proof receipts. |
| DOM/page perception | Allowed as provisional observation with scope and redaction. |
| Attachment/drop-target calibration | Allowed as the first concrete screen/DOM calibration lane. |
| GPT Actions enqueue | Allowed as typed queue bridge. |
| Result capture | Allowed for browser-carrier packet receipts. |
| Silent send for sensitive actions | Forbidden. |
| Credentials | Forbidden. |
| Purchases | Forbidden. |
| Destructive actions | Forbidden. |
| Production mutation | Forbidden. |
| Unrestricted browser control | Forbidden. |

## Automation maturity model

The companion must report automation posture using the existing ladder:

| Stage | Companion meaning |
| --- | --- |
| MANUAL | User carries the action; dAimon only observes or drafts. |
| ASSISTED | dAimon prepares packets, previews targets, or drafts workflows. |
| GATED_AUTOMATION | dAimon can advance bounded queue or approved local helper steps after gates pass. |
| RUNTIME_ACTIVE | Reserved for a future receipted scope where bounded runtime execution is proven. |
| SUSPENDED | Pause or kill switch is active. |
| DISABLED | A capability is unavailable or forbidden in current scope. |

No component may imply `RUNTIME_ACTIVE` unless a matching receipt and scope-specific proof exist.

## Required event model

Every visible automation event in the companion timeline should carry:

```yaml
event_id: stable id
occurred_at: timestamp
loop_id: queue | page_perception | attachment | approval | receipt | diagnostics
phase: local phase name
status: OK | WATCH | BLOCKED | REPAIR
claim_lane: provisional | candidate | approved | receipted | blocked
rendered_surface: top_bar | main | inspector | bottom_timeline
authority_scope: explicit bounded authority
evidence_refs: []
repair_required: false
blocked_capabilities: []
detail: operator-readable detail
```

This is inherited from the Reactive OS stream model and adapted to browser-carrier loops.

## Queue execution trace model

The GPT Actions to browser queue carrier must expose trace phases aligned with dry-run dispatch:

| Trace phase | Browser-carrier meaning |
| --- | --- |
| VALIDATE_OPERATOR_HANDOFF | Validate packet schema, idempotency, authority, and approval state. |
| RECHECK_GOVERNORS | Check pause/kill, queue cap, autoplay cap, page readiness, and blocked capabilities. |
| COMPILE_CONTEXT_PREVIEW | Build visible packet prompt/context preview. |
| BUILD_PROVIDER_ADAPTER_NOOP | Confirm no direct provider/background agent claim is being made. |
| SIMULATE_PROMPT_INJECTION | Show intended injection target and readiness before send. |
| SIMULATE_RESPONSE_WAIT | Track output-started/output-stopped detector state. |
| SIMULATE_EXTRACTION_RECEIPT | Capture assistant answer and structured blocks. |
| EMIT_TRACE_RECEIPT | Post result receipt to gateway and render in timeline. |

In v1, this trace may accompany live bounded browser-carrier send for approved queue packets, but it does not authorize sensitive silent actions.

## Safety floor

The browser sandbox spec is the safety floor:

- no credential capture or secret extraction
- no unapproved navigation or form submission
- no destructive actions
- no purchases or account operations
- no hidden page scraping beyond declared scope
- no production visual automation
- no unrestricted browser control
- no silent promotion of page memory to accepted ION context

If a requested feature violates this floor, it must render as blocked with a reason and next safe path.

## Implementation rule

Future extension work must do one of two things:

1. map the feature to an inherited protocol in this synthesis, or
2. mark it as new and specify the safety gates, event model, receipt path, and forbidden capabilities before implementation.

This prevents the dAimon companion from drifting into a generic automation extension.
