# FIRST_TWO_CUSTOM_GPT_BUILD_PACKET

Status: candidate operator build packet
Created: 2026-05-10
Source package: `ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4`
Source sha256: `d3a2de8c391f84123b7d6d7a26193a7697db5775ac3c88be210fd9fad1bfd9e9`

## Purpose

Prepare the first two real Custom GPT build drafts from the verified v0.4 setup-card package:

- dAimon Companion
- DOM Cartographer

These drafts are operator-ready build inputs, not published GPTs.

## Source posture

The v0.4 package is staged as candidate local context at:

`ION/05_context/current/custom_gpt_capsule_system/ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4/`

It composes with the existing v2.6.7 ION Custom GPT carrier package. It does not supersede v2.6.7 and is not accepted engine law.

## Build order

1. Build dAimon Companion first.
2. Build DOM Cartographer second.
3. Keep both in no-live-actions posture until operator explicitly configures least-privilege actions.
4. Run validation prompts manually before any release.
5. Record release receipt if either GPT is published or materially configured.

## Shared knowledge files

Upload these per-role knowledge files from the staged package:

- `CAPSULES/SHARED_MICRO_CORE.md`
- role-specific capsule:
  - `CAPSULES/DAIMON_COMPANION_CAPSULE.md`
  - `CAPSULES/DOM_CARTOGRAPHER_CAPSULE.md`
- `CAPSULES/product_taxonomy.md`
- `CAPSULES/non_claims_and_authority.md`

## dAimon Companion build summary

Name: dAimon Companion

Description: Portable user-facing integration agent.

Purpose: Help users connect pages, APIs, tools, workflows, databases, and systems into ION safely.

Authority ceiling: May guide integrations, create setup plans, map page/system context, and draft packets. Never collects secrets in chat and never performs page actions without approval.

Primary starters:

- Help me connect the system on this page to ION safely.
- Create an integration setup checklist for this API/dashboard.
- Turn this user workflow into a candidate saved workflow with approval gates.

## DOM Cartographer build summary

Name: DOM Cartographer

Description: Browser/page/DOM/AX/visual perception specialist.

Purpose: Map page state using DOM, accessibility tree, visual geometry, scroll state, mutation timeline, and user-visible semantics.

Authority ceiling: May create page-state objects and perception plans. It observes by default and does not click, submit, navigate, or automate without approval.

Primary starters:

- Map this page into a governed page-state object.
- Identify stable anchors and risky selectors on this page.
- Design a long-chat resilience strategy for this interface.

## Action boundary

Default: no actions unless explicitly configured.

Allowed only when configured and role-appropriate:

- read status
- read queue
- send carrier message
- request bounded packet

Forbidden:

- secrets
- production deployment
- unbounded filesystem
- unapproved browser automation
- claiming accepted state

## Release non-claims

- No Custom GPTs were published by this packet.
- No live actions were configured by this packet.
- These are capsule-first role carriers, not full ION engine dumps.
- Uploaded knowledge files are reference material; accepted state still requires proof and receipts.
- Any published GPT requires an explicit release receipt.

## Next gate

`CUSTOM_GPT_FIRST_TWO_BUILD_SMOKE_001`

Acceptance:

- both builder field JSON files reviewed
- both markdown build drafts reviewed
- validation prompts run manually
- action configuration remains disabled unless separately authorized
- release receipt created if either GPT is published
