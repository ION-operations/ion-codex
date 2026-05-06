---
type: public_orientation
status: DRAFT_NON_AUTHORITY
production_authority: false
live_execution_authority: false
---

# ION Fundamentals

ION is a continuity substrate for AI work.

Its core claim is simple:

```text
AI output does not become state because it was generated.
It becomes state only through lawful movement.
```

The public README is the compressed front door. This document expands the
foundation without replacing runtime authority. For active work, use
`ION/REPO_AUTHORITY.md`, the mount contract, current packets, registries,
templates, gates, receipts, manifests, and tests.

## The Lawful Act

The primitive in ION is the lawful act:

```text
intent
-> work packet
-> compiled context package
-> governing template
-> mounted role
-> carrier execution
-> proof-bearing return
-> gate
-> Steward decision
-> receipt
-> next state
```

This chain is what separates continuation from reconstruction. A fresh carrier
does not need to trust an older model's private memory. It can inherit the
packet, context, template, proof, decision, and receipt trail.

Prompting tries to make the model behave. ION designs the world the model acts
inside.

## Candidate State

Every meaningful AI result is a candidate state transition.

Candidate state is allowed to be useful, insightful, or even correct. It is not
accepted state until it crosses the proof and integration membrane.

ION therefore rejects the common shortcut:

```text
model said something -> treated as truth
```

and replaces it with:

```text
candidate -> proof -> decision -> receipt -> inheritable state
```

The goal is not to build an AI that never drifts. The goal is to build a system
where drift has nowhere important to land.

## Complexity Reduction

ION is not valuable because it is complex. It is valuable because it reduces
the operational complexity of long-horizon AI work.

A large AI workflow quickly exceeds what a model, a chat transcript, or a human
operator can safely hold in active memory. ION turns that mass into bounded
state transitions:

```text
intent -> packet -> domain -> template -> context package -> proof -> Steward decision -> receipt -> next state
```

The central compression is:

```text
unbounded project complexity -> bounded executable movement
```

ION increases intelligence not by making the model larger, but by reducing the
complexity of the state the model must safely act upon.

## Context Inheritance

ION context is not merely selected for a worker. It is inherited from prior
accepted template movements.

That matters because context quality improves only when accepted work changes
what future workers receive. If a receipt does not improve the next context,
the system has recorded activity without true continuation.

## Context-First Domains

ION does not ask an agent to enter a blank field and reconstruct meaning from
scratch. It mounts the carrier inside a governed contextual domain where
sources, relationships, templates, neighboring routes, authority boundaries,
and proof obligations are already part of the working surface.

The agent no longer has to build the world before acting. The world is shaped
for the act.

```text
governed domain
+ bounded context package
+ governing template
+ known neighboring domains
+ proof obligation
+ receipt path
+ carrier
```

This is the difference between an agent improvising its own map and a carrier
operating inside mapped territory.

## Context Graph And Domain Fission

ION is not a pile of files. It is a living context graph operated through
lawful templates.

A domain is a governed graph region, not a topic folder. Domains should be able
to split when their relationship complexity exceeds one agent's lawful
context-management capacity.

The split point is not size alone. The split point is context manageability.

See `ION/docs/ION_DOMAIN_GRAPH_AND_FISSION.md`.

## Receipts As Learning

An agent workflow without receipts is not auditable, and an unauditable agent
workflow cannot reliably improve.

ION turns failure from anecdote into a traceable state-transition defect:

```text
agent action -> receipt -> failure classification -> template correction -> context correction -> regression test -> next run
```

Prompt patching hides failure. Receipt-based workflows locate failure.

## Git For AI Work

Git made software safer by making code history inspectable, reversible,
branchable, and reviewable. ION applies that principle to AI-mediated state.

| Git | ION |
| --- | --- |
| Commit | Receipt |
| Diff | Proposed state delta |
| Branch | Alternate work trajectory |
| Merge | Steward integration |
| Revert | Rejection / rollback / containment |
| CI check | Proof gate / template action gate |

Git stores file history. ION stores workflow history.

## Parallel Settlement

Fan-out is easy. Fan-in is where agent systems usually fail.

ION treats parallel return as a settlement problem. Branch returns are
proposals, not truth. The parent scope must decide which returns are accepted,
merged, escalated, deferred, or abandoned, and must leave a receipt showing what
future work may inherit.

See `ION/docs/ION_PARALLEL_SETTLEMENT.md`.

## Project Ingestion

ION must not assume it only governs itself.

A new project is not ION-manageable because it has been uploaded. It becomes
ION-manageable when its structure, authority, domains, context nodes,
templates, risks, and first receipts have been established.

The intended path is:

```text
external project -> quarantine -> manifest -> cartography -> context graph
-> domain partition -> template binding -> risk classification
-> first context packages -> receipts -> governed work loop
```

See `ION/docs/ION_PROJECT_INGESTION.md`.

## Runtime Truth

README prose, docs, and historical reports are orientation. Runtime truth is
proven by:

- kernel status
- active packets
- context packages
- template gates
- Steward integration records
- receipts
- manifests
- tests

The practical question is always:

```text
What proves this claim now?
```

## Public Posture

ION is public so others can inspect, critique, and contribute to the protocol.
Public GitHub is the collaboration and data plane. It is not runtime authority,
production authority, secret authority, or proof of acceptance.

Local ION law remains the authority membrane.

To the operator's knowledge, the project artifacts in this repository have been
AI-built under human direction. The human operator supplies intent, correction,
pressure, taste, review, and authority boundaries. ION exists because this
AI-mediated work needed a way to continue without treating raw output as state.

For the longer public explanation, see
`ION/docs/ION_CONTINUITY_SUBSTRATE_EXPLAINER.md`.
