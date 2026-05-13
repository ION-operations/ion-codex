---
type: public_orientation
status: DRAFT_NON_AUTHORITY
production_authority: false
live_execution_authority: false
---

# ION Parallel Settlement

Fan-out is easy.

Fan-in is where agent systems usually fail.

ION's parallelism is not a swarm free-for-all. Parallel work is one lawful
parent scope temporarily partitioned into bounded branches. Each branch return
is a proposal, not truth. The parent scope must perform an explicit settlement
act before anything becomes accepted state.

## Branch Return Requirements

A lawful branch return should preserve:

```text
parent scope
branch identity
bounded objective
executor or carrier used
context package used
template followed
files or state touched
proof supplied
conflicts or uncertainties observed
recommended settlement path
```

Parallel return does not imply landing.

## Settlement Outcomes

The Steward does not blindly merge branches. It classifies the settlement
condition.

Minimum outcomes:

```text
ACCEPTED_AS_IS
MERGE_PROPOSAL_REQUIRED
ESCALATE_REVIEW
DEFERRED
ABANDONED
```

## Automated Assistance vs Acceptance Authority

ION may use an LLM carrier to analyze branch returns or draft a merge proposal.

That carrier might be selected because it has the right capability profile:

```text
MASON_CLI for implementation merge work
NEMESIS_CLI for adversarial conflict review
VIZIER_CLI for strategic route analysis
SCRIBE_CLI for receipt and documentation synthesis
STEWARD_REVIEW_CLI for integration analysis
```

But that model-assisted synthesis is still a proposal.

The model may help answer:

```text
Do these branches conflict?
Which files or claims overlap?
Can they be accepted independently?
Is a merge proposal coherent?
What proof is missing?
Should this escalate?
```

It does not become state because it sounds coherent.

## Settlement Gate

A settlement boundary becomes more human-gated as risk increases.

Low-risk settlement may be automated when:

```text
branches touch non-overlapping surfaces
all proofs pass
tests pass
authority ceiling is low
no stale context is detected
no state-bearing conflict exists
```

Human or higher Steward review is required when:

```text
branches overlap in write scope
branch conclusions disagree
authority ceiling is high
business, legal, financial, safety, deployment, or secret-bearing risk exists
tests conflict
proof is incomplete
a branch tries to widen scope
the merge would alter accepted state
```

In short:

```text
LLMs may draft settlement analysis.
ION decides whether that analysis is admissible.
Steward or human authority decides whether it lands.
```

## Settlement Receipt

Every meaningful settlement should leave a receipt showing:

```text
which branches returned
which evidence was considered
which conflicts were found
which outcome was chosen
whether human review was required
what was accepted
what was rejected
what remains deferred
what next packet or context package inherits the result
```

This makes parallel work reversible, auditable, and replayable.

## Strong Formulation

```text
ION does not solve fan-in by asking one model to summarize everything.
ION solves fan-in by making settlement a lawful state-transition act.
```

```text
The intelligence of parallel work is not only in splitting tasks.
It is in settling returns.
```
