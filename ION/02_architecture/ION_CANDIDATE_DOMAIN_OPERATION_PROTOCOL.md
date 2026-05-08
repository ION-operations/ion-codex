---
protocol_id: ion.candidate_domain_operation_protocol.v0_1
status: CANDIDATE_OPERATIONAL
rank: A3_PROVISIONAL_CANDIDATE_PROTOCOL
created: 2026-05-08
scope: assistant_work_candidate_domains_agents_templates_routes
production_authority: false
live_execution_authority: false
secrets_authority: false
accepted_canon: false
---

# ION Candidate Domain Operation Protocol

## Purpose

Candidate domains are allowed to be useful before they become accepted ION law.
They may classify work, shape proof, improve route traces, and expose diagnostic
structure while remaining under stricter containment than accepted domains.

This protocol exists because a binary split between inert notes and accepted
canon is too coarse. ION needs a middle layer where candidate domains, agents,
templates, routes, and protocols can operate, gather evidence, and either earn
promotion or be revised, archived, or rejected.

## Core Rule

```text
operational candidate != accepted law
```

Candidate surfaces may help ION think and route. They may not accept state,
mutate accepted registries, alter product front doors, claim production/live
authority, or become sovereign ION roles.

## Lifecycle Ladder

| Level | State | Meaning | Route compiler use |
| --- | --- | --- | --- |
| L0 | `raw_observation` | Preserved signal, complaint, external pattern, or imported witness. | Refused |
| L1 | `candidate_draft` | Named candidate exists but has not earned operational use. | Refused |
| L2 | `operational_candidate` | Candidate may classify work and shape proof under visible caveat. | Allowed |
| L3 | `proof_gated_candidate` | Candidate has examples, validator, boot exercise, receipt, or repeated useful use. | Allowed |
| L4 | `promotion_candidate` | Candidate is ready for Steward/Nemesis/human review. | Allowed |
| A3 | `accepted_operational_domain` | Landed into accepted operational surfaces by explicit receipt. | Allowed by accepted owner |
| A2/A1 | `canonical_domain_or_law` | Stable doctrine, law, or root architecture. | Allowed by accepted owner |
| X | `deferred`, `rejected`, `archived` | Candidate is not currently active. | Refused |

The route compiler must refuse explicit inactive, rejected, archived, deferred,
raw-observation, and draft records. Missing lifecycle records are treated as
unrecorded candidates for compatibility, but promotion work must create records.

## Allowed Candidate Uses

Operational candidates may:

- classify operator messages or action payloads;
- suggest likely domains, specialist interfaces, skills, lenses, and templates;
- shape proof requirements and validation checklists;
- appear in chat traces, cockpit drawers, route graphs, and receipts;
- inform validate-only Action Gateway responses;
- guide package-product continuity and exported data-zip structure;
- collect scorecard evidence for future promotion review.

## Forbidden Candidate Uses

Operational candidates may not:

- mutate `ION/03_registry/`;
- mutate product front-door law or OpenAPI contracts without separate approval;
- accept state or final claims;
- create sovereign ION roles;
- bypass Relay, Steward, proof, validation, or receipt gates;
- grant production authority, live execution authority, secrets authority,
  deployment authority, git push authority, or arbitrary shell authority;
- hide their candidate status from the operator or downstream proof surfaces.

## ION Movement

Candidate domains plug into the existing ION movement:

```text
Relay
  receives operator work or action payload

Route Compiler
  proposes candidate domain/agent/template route

Steward
  decides whether candidate use is lawful for this cycle

Vizier or candidate specialist interface
  expands plan, proof obligations, and risks

Mason/Codex
  performs bounded implementation only when authorized

Nemesis
  tests whether the candidate route reduced drift or created confusion

Scribe
  records receipt, scorecard, and non-claims

Steward / human
  accepts, revises, defers, archives, rejects, or promotes
```

## Candidate Agent Semantics

Candidate specialist agents are domain-local interfaces mounted under accepted
ION roles. They are not independent identity-bearing ION roles.

Example:

```text
UI_ARCHITECT
  may mount under Vizier for planning
  may mount under Mason/Codex for implementation handoff
  may mount under Nemesis for UI proof review
  may mount under Persona only as a user-facing explanation lens
```

Candidate agents may carry domain vocabulary, expected state surfaces, proof
obligations, common failure modes, return contracts, and template
recommendations.

Candidate agents may not carry Steward authority, registry mutation authority,
state acceptance authority, production/live authority, or autonomous execution
authority.

## Lifecycle Registry Contract

Candidate lifecycle records live under:

```text
ION/05_context/current/ai_assistant_work/candidate_lifecycle/
```

The minimum record shape is:

```yaml
candidate_id:
candidate_type: domain | agent | template | route | protocol
lifecycle_state:
source_evidence:
parent_accepted_surface:
host_ion_roles:
allowed_uses:
forbidden_uses:
route_compiler_enabled:
gateway_validation_enabled:
mcp_surface_enabled:
cockpit_display_enabled:
scorecard_path:
promotion_gate:
receipts:
```

## Scorecard Contract

Each operational candidate should accumulate a scorecard with:

```yaml
route_accuracy:
proof_usefulness:
user_burden_reduction:
drift_or_confusion_risk:
test_coverage:
valid_instance_count:
expected_rejection_count:
receipt_count:
conflicts_with_accepted_law:
operator_acceptance_notes:
promotion_recommendation:
```

The scorecard should record both value and failure. A candidate that causes user
chore, authority confusion, or weak proof should be revised or archived rather
than promoted.

## Promotion Gate

Promotion requires:

1. Lifecycle record.
2. Source evidence map.
3. Route/compiler usage evidence when applicable.
4. Validator, machine-checkable examples, or explicit proof corpus where
   applicable.
5. Scorecard with drift/failure notes.
6. Steward review.
7. Human acceptance.
8. Receipt naming exact accepted paths.
9. Tests proving accepted surfaces still pass.

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

## Non-Claims

This protocol does not accept any current assistant-work candidate as canon. It
does not mutate `ION/03_registry/`, does not expand MCP or Custom GPT front-door
contracts, and does not grant production, live execution, secrets, deployment,
git push, or arbitrary shell authority.
