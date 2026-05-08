# Candidate Domain Operation Protocol Plan

Status: planning artifact, not accepted ION canon.

Created: 2026-05-08T18:39:06Z

Active root:

```text
/home/sev/ION - Production/ION_CODEX FULL
```

## Principle

Candidate domains should be operational under containment.

They are not inert notes, but they are also not accepted law. Their value is
that ION can safely try new specialist domains, agents, templates, and proof
requirements while making the candidate boundary visible and receipted.

```text
candidate domain/agent/template
-> operational under stricter candidate protocol
-> evidence collected
-> calibrated against accepted ION law
-> promoted, revised, archived, or rejected
```

## Lifecycle Ladder

| Level | Name | Meaning | Allowed | Forbidden |
| --- | --- | --- | --- | --- |
| L0 | Raw Observation | User complaint, failure, external pattern, package import, or raw idea. | Preserve as evidence. | Route live work from it. |
| L1 | Candidate Draft | Named domain, agent, template, route, or protocol exists as candidate material. | Read, inspect, compare. | Treat as active routing law. |
| L2 | Operational Candidate | Candidate may classify work and shape proof requirements. | Route preview, trace display, work-packet hints. | Mutate accepted registries, claim authority. |
| L3 | Proof-Gated Candidate | Candidate has validator, valid/reject instances, boot exercises, receipts, or repeated successful use. | Use across Codex Chat, Gateway validation, cockpit diagnostics, and package product lane. | Become accepted without review. |
| L4 | Promotion Candidate | Candidate has scorecard evidence and low drift. | Steward/Vizier/Nemesis review for accept/revise/reject. | Bypass explicit acceptance. |
| A3 | Accepted Operational Domain | Landed into accepted registry/protocol surfaces with receipt. | Govern real work routes inside accepted ION law. | Override A2/A1 root law. |
| A2/A1 | Canonical Domain/Law | Stable architecture/doctrine/root law. | Define core movement and authority. | Be changed by candidate evidence alone. |

## Movement Through ION

Candidate domains should plug into the existing ION movement, not create a
parallel workflow.

```text
Relay
  receives operator work or action payload

Route Compiler
  proposes candidate domain/agent/template route

Steward
  decides whether candidate route is lawful for this cycle

Vizier / specialist candidate interface
  expands plan and proof obligations

Mason/Codex
  performs bounded implementation if authorized

Nemesis
  tests whether the candidate route helped or drifted

Scribe
  records receipt and scorecard

Steward
  accepts, revises, defers, rejects, or promotes
```

## Candidate Agent Semantics

Candidate specialist agents are not new sovereign ION roles.

They are domain-local interfaces mounted under accepted ION roles.

Example:

```text
UI_ARCHITECT
  mounted under Vizier when planning UI state/flow
  mounted under Mason/Codex when implementation handoff needs component contract
  mounted under Nemesis when reviewing a11y/state proof
  mounted under Persona only as user-facing explanation lens
```

Candidate agents may carry:

- domain vocabulary
- expected state surfaces
- proof obligations
- common failure modes
- return contract
- template recommendations

Candidate agents may not carry:

- ION identity
- Steward authority
- registry mutation authority
- production/live authority
- autonomous execution authority

## Candidate Operating Contract

Every operational candidate surface should expose:

```yaml
candidate_only: true
lifecycle_state: operational_candidate
source_evidence: required
parent_accepted_domain: required
host_ion_roles: required
allowed_use:
  - classification
  - proof_shaping
  - route_preview
  - trace_display
  - diagnostic_display
forbidden_use:
  - ION/03_registry_mutation
  - product_front_door_mutation
  - production_authority
  - live_execution_authority
  - state_acceptance
  - autonomous_agent_identity_claim
receipts_required: true
promotion_requires:
  - scorecard
  - validation
  - Steward_review
  - human_acceptance
```

## Calibration Scorecard

Each operational candidate should accumulate a scorecard:

```yaml
candidate_id:
candidate_type: domain | agent | template | route | protocol
lifecycle_state:
source_evidence:
route_accuracy:
proof_usefulness:
user_burden_reduction:
drift_or_confusion_rate:
test_coverage:
valid_instance_count:
expected_rejection_count:
receipt_count:
conflicts_with_accepted_law:
operator_acceptance_notes:
promotion_recommendation:
```

The scorecard should distinguish:

- helped route correctly
- routed incorrectly
- reduced user burden
- increased user chore
- improved proof quality
- caused authority confusion
- revealed missing accepted protocol
- should be promoted
- should be revised
- should be archived/rejected

## Registry Placement

Before acceptance, candidate lifecycle data belongs under:

```text
ION/05_context/current/ai_assistant_work/
```

Proposed candidate surfaces:

```text
candidate_lifecycle/
  CANDIDATE_DOMAIN_LIFECYCLE_REGISTRY_V0_1.yaml
  scorecards/
  promotion_proposals/
  rejection_receipts/
```

Do not write these to `ION/03_registry/` until a separate promotion pass is
approved and receipted.

## Promotion Gate

Promotion from candidate to accepted operational domain requires:

1. Candidate lifecycle record.
2. Source evidence map.
3. Route compiler usage evidence.
4. At least one focused validator or machine-checkable instance set.
5. Scorecard with drift/failure notes.
6. Steward review.
7. Human acceptance.
8. Receipt naming exact accepted paths.
9. Tests proving accepted registry/protocol surfaces still pass.

Promotion outcomes:

```text
ACCEPT_AS_OPERATIONAL_DOMAIN
ACCEPT_AS_TEMPLATE_ONLY
ACCEPT_AS_ROUTE_ONLY
REVISE_AND_RETEST
DEFER
ARCHIVE_AS_WITNESS
REJECT
```

## First Candidates To Calibrate

Safest initial candidates:

- `screen_state_matrix_packet`
- `terminal_proof_receipt_packet`
- `api_docs_example_validation_packet`
- `ui_ux_domain`
- `documentation_writing_domain`
- `ide_work_domain`

Reason:

- They have obvious practical value.
- They reduce observed failure modes.
- They can be validated with explicit examples.
- They do not require production/live authority.

## Implementation Sequence

### Packet 1 - Protocol Draft

Create an active candidate protocol:

```text
ION/02_architecture/ION_CANDIDATE_DOMAIN_OPERATION_PROTOCOL.md
```

Status should remain `ACTIVE_PROVISIONAL` or `CANDIDATE_OPERATIONAL`, not A1
canon.

### Packet 2 - Candidate Lifecycle Registry

Create:

```text
ION/05_context/current/ai_assistant_work/candidate_lifecycle/CANDIDATE_DOMAIN_LIFECYCLE_REGISTRY_V0_1.yaml
```

Seed it with current assistant-work domains/routes/templates and lifecycle
states.

### Packet 3 - Scorecard Schema And First Scorecards

Create a scorecard schema and first scorecards for:

- `ui_ux_domain`
- `screen_state_matrix_packet`
- `terminal_proof_receipt_packet`

### Packet 4 - Route Compiler Lifecycle Awareness

Patch the route compiler to read lifecycle state and refuse inactive/rejected
candidates.

### Packet 5 - Promotion Proposal

Draft one promotion proposal for the safest candidate, likely
`terminal_proof_receipt_packet` or `screen_state_matrix_packet`.

## Non-Claims

- This plan does not accept candidate domains into ION canon.
- This plan does not mutate `ION/03_registry/`.
- This plan does not grant production/live authority.
- This plan does not make candidate specialist agents into sovereign ION roles.
- This plan does not approve MCP tool-contract expansion.
