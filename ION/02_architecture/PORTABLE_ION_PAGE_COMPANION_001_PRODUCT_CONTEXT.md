# PORTABLE_ION_PAGE_COMPANION_001_PRODUCT_CONTEXT

Status: active product context
Created: 2026-05-10
Source carrier message: `carmsg_2026-05-10T181352Z0000_chatgpt_browser_carrier_to_codex_cli_carrier`

## Purpose

Define the portable ION page companion product shape before DOM perception and extension work harden around a narrower model.

The companion is one portable ION/Helixion presence that follows the user across pages, opens a page-aware cockpit, and binds page context into one governed ION chat/context graph.

## Product thesis

One ION logo/icon follows the user across arbitrary pages. Clicking it opens an ION/Helixion companion panel scoped to the current page and connected to the same governed ION chat/context graph used by ChatGPT, Codex, local ION apps, and future Helixion surfaces.

Every page, session, workflow, and chat becomes a branch of one graph rather than a disconnected conversation. Learned page context can be settled, saved, replayed, and carried back to ChatGPT/Codex.

## Architecture distinction

DOM Perception is how ION sees a page.

Portable Page Companion is how the user carries ION onto any page.

Mini-Helixion is the embedded cockpit surface opened from the companion.

Living Operational Graph is the global city map of context, branches, workflows, receipts, and settlements.

## JOC inheritance decision

The portable dAimon companion inherits older JOC as its primary UI and automation model.

It is a JOC micro-shell adapted to browser-carrier work, not a generic extension popup. The inherited cockpit grammar is:

- top status bar
- left or side mode rail
- main work surface
- right inspector or drawers
- bottom timeline and receipt rail

The visual language should preserve DXL matte-black instrument-panel posture, compact monospace labels, dense telemetry, explicit mode/status surfaces, visible automation streams, split inspector drawers, and command/mission dashboard feel.

The content model evolves for current ION/dAimon needs: browser queue packets, GPT Actions-created packet visibility, autoplay/pause/kill controls, output-stopped detector status, claimed packet state, DOM/page evidence, attachment/drop target calibration, approval gates, receipts, local mutation proof, carrier health, and blocked-capability warnings.

The governing synthesis is `ION/02_architecture/DAIMON_EXTENSION_JOC_AUTOMATION_LINEAGE_SYNTHESIS.md`.

## Core model

The browser extension provides a portable ION companion surface with these responsibilities:

- maintain one visible ION affordance across eligible pages
- open a page-aware companion panel without claiming hidden authority over the page
- create or resume a page branch in the shared ION chat/context graph
- capture governed page perception packets with explicit scope and redaction
- learn stable page structure, task state, and user-described workflows
- propose workflows as visible plans before any state-bearing action
- route settled page context back to ChatGPT/Codex as context packages
- preserve receipts for every state-bearing workflow and context promotion

## Shared graph model

The companion must bind each page interaction into one graph:

- `global_chat_graph`: the shared ION/Codex/ChatGPT context graph
- `page_branch`: URL or page-class scoped branch for a specific page family
- `session_branch`: time-bounded page visit or task session
- `workflow_branch`: replayable, user-approved routine derived from one or more page sessions
- `settlement_edge`: explicit promotion from observed page memory into accepted ION context
- `receipt_edge`: durable proof that a context or workflow state transition occurred

Page memory is provisional until settled. It may be useful for local continuity, but it is not accepted ION context until a settlement packet, receipt, or operator confirmation promotes it.

## Page context package shape

Future page context packages should preserve:

- page identity: origin, URL pattern, title pattern, page class, and optional stable app identifiers
- capture scope: what the user allowed the companion to observe
- redaction policy: what was ignored, summarized, masked, or forbidden
- perception summary: stable DOM landmarks, visible task state, forms, controls, and semantic regions
- workflow candidates: user-described or inferred routines, stored as drafts until approved
- action boundary: permitted observation and explicitly approved action classes
- provenance: source page session, capture time, tool version, and carrier surface
- receipts: capture receipts, settlement receipts, action receipts, and replay receipts

## Safety law

Observe by default.

Plan before acting.

Preview before clicking.

Ask before navigation/forms.

Receipt every state-bearing workflow.

Never treat page memory as accepted context without settlement.

## Automation boundary

The portable companion must not become unsafe autonomous browser control. It may help users understand, plan, and execute workflows, but state-changing operations require visible user consent.

Required boundaries:

- per-page capability scopes
- visible action plans before state changes
- dry-run or preview for clicks, navigation, forms, purchases, submissions, account changes, and destructive actions
- explicit approval for each state-bearing action batch
- no hidden navigation or background form submission
- no credential capture, secret extraction, or bypass of page/user intent
- no claims that provisional page memory is verified truth
- receipts for captures, promotions, action approvals, executions, and replays

## Current v1 authority

- autoplay queue is allowed for bounded packets with visible state, pause, kill, and receipts
- gated local mutation is allowed only through approval, policy gates, and proof receipts
- DOM/page perception is allowed as provisional observation with scope and redaction
- attachment/drop-target calibration is allowed as the first concrete screen/DOM calibration lane
- GPT Actions enqueue is allowed as a typed queue bridge
- result capture is allowed for browser-carrier packet receipts
- silent send for sensitive actions is forbidden
- credentials are forbidden
- purchases are forbidden
- destructive actions are forbidden
- production mutation is forbidden
- unrestricted browser control is forbidden

## Implementation gates

Gate 1: Product packet exists and is linked to DOM Perception, Mini-Helixion, and Living Graph work.

Gate 2: JOC lineage synthesis is registered and future companion features map to inherited protocol or declare themselves new with explicit gates.

Gate 3: Extension shell shows one portable ION affordance and opens a page-aware JOC micro-shell.

Gate 4: Page branch model stores provisional page perception with redaction and scope metadata.

Gate 5: Context package ingest can settle selected page memory into the shared graph.

Gate 6: Workflow memory stores replayable plans without granting autonomous action authority.

Gate 7: Approved-action executor requires preview, explicit consent, and receipts for state-bearing actions.

## Connected work

- `DOM_PERCEPTION_001_DOMAIN_DESIGN`: defines how ION sees a page
- `DOM_PERCEPTION_002_CONTEXT_PACKAGE_INGEST_AND_OPERATION_MODEL`: defines how page observations become context packages
- `ION_EXTENSION_MINI_HELIXION_CONTEXT_PACKAGE`: defines the embedded cockpit surface
- `LIVING_OPERATIONAL_GRAPH`: defines the global context/workflow map

## Acceptance criteria

- A future extension design can distinguish page perception from the portable companion surface.
- A future Mini-Helixion panel can show the current page branch and global graph branch relationship.
- A future workflow routine can be saved as a replayable plan without silently acting.
- A future ChatGPT/Codex interaction can receive settled page context with source receipts.
- Any state-bearing page action requires user-visible plan, preview where applicable, approval, and receipt.
