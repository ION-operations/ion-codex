# ION

**A continuity substrate for AI work.**

*Local-first. Template-governed. Context-bound. Proof-gated. Stewarded. Carrier-agnostic.*

> *ION is the law by which AI work becomes state.*

---

Most AI sessions produce outputs.

ION produces **state**.

The difference is this: an output exists because a model generated it. State
exists because a bounded act, governed by a template, situated by a compiled
context package, executed through a mounted role, returned a proof-bearing
result, passed a gate, and earned a receipt that the next worker can inherit.

That chain is not ceremony. It is the only thing that separates continuation
from reconstruction.

---

## The Primitive

The primitive in ION is not the agent. It is not the chat. It is not memory.

It is the **lawful act**.

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

Output that cannot show its packet, its context, its template, its proof path,
and its receipt is not yet ION state. It is a candidate.

---

## Six Laws

```text
1. Meaningful AI work is a candidate state transition.
2. Every state-bearing act must be governed by a template.
3. Every template execution must be situated by a bounded context package.
4. Every return is proposal until proof gates and Steward integration accept it.
5. Every accepted delta must leave a receipt.
6. Every receipt must improve the next context, or the system has not continued.
```

These are anti-failure constraints, not slogans. They prevent one specific
collapse:

```text
model said something -> treated as truth
```

and replace it with:

```text
candidate -> proof -> decision -> receipt -> inheritable state
```

In ION, the next context is not merely assembled. It is inherited from prior
accepted template movements.

---

## Templates

A template in ION is not a markdown form. It is the **action type** of the work.

A template defines what kind of act is happening, what context is required,
what output is valid, what authority is exercised, what state may be touched,
what proof is owed, and how the result becomes future context.

This matters because untyped cognition is where drift enters.

```text
AUDIT is not BUILD.
BUILD is not HANDOFF.
HANDOFF is not RATIFICATION.
COMPLETION is not ACCEPTANCE.
```

ION agents do not improvise workflows. They move through proven templates,
evolve templates under governed law, or create new ones through a meta-template
path. The same movement that governs current work builds the context future
workers inherit.

ION can expand into new domains because template creation is itself governed.

---

## Agents

In ION, an agent is not a personality assigned to a model.

An agent is a **domain-bound threshold**: the point where intent, compiled
context, mounted role, governing template, and carrier execution align into a
lawful act.

The domain defines the agent, not the other way around. As the project's
domains mature, templates sharpen, receipts accumulate, and context improves,
the agent's world changes with it. ION does not evolve agents by editing their
prompts. It evolves them by evolving the governed structure they act inside.

---

## Roles And Carriers

A role is a bounded ION function. A carrier is the host executing it. They are
not the same thing.

| Role | Function |
| --- | --- |
| `STEWARD` | Integration, acceptance, rejection, closure. |
| `RELAY` | Intake, packet formation, handoff. |
| `VIZIER` | Strategy and route intelligence. |
| `MASON` | Build coordination and implementation. |
| `NEMESIS` | Adversarial audit and failure-mode attack. |
| `VESTIGE` | Memory, archaeology, residue interpretation. |
| `SCRIBE` | Structured capture and documentation. |
| `VICE` | Discipline, critique, hardening pressure. |

| Carrier | Role in the system |
| --- | --- |
| ChatGPT Browser | Coordination, continuity, bounded connector lane. |
| Cursor IDE | Local IDE carrier with file visibility. |
| Codex CLI | Bounded local filesystem, build, and test worker. |
| MCP | Tool transport and governed capability exposure. |
| Browser Extension + Daemon | Approval-gated ChatGPT-to-local ION bridge. |
| GitHub | Public collaboration and data plane, not ION runtime authority. |

```text
ION governs.
Carriers carry.
Roles execute bounded functions.
No carrier becomes ION identity.
```

---

## What Runs

The executable kernel lives at `ION/04_packages/kernel/`. Its job is to make
state, authority, and transitions **inspectable**.

Core surfaces:

`ion_status` - `ion_carrier_onboard` - `ion_carrier_continue` -
`ion_cycle_runner` - `ion_context_proof_gate` - `ion_template_action_gate` -
`ion_steward_integrate` - `ion_agent_invocation_broker` -
`ion_codex_queue_runner` - `ion_cockpit_view_model`

Active state lives at `ION/05_context/current/`: packets, queues, ledgers,
receipts, handoffs, and projections maintained as explicit runtime objects,
not chat transcripts.

---

## Full Reference

The deeper public orientation layer lives under `ION/docs/`:

- [ION Fundamentals](ION/docs/ION_FUNDAMENTALS.md)
- [Template Law](ION/docs/TEMPLATE_LAW.md)
- [Context System](ION/docs/CONTEXT_SYSTEM.md)
- [Agents, Roles, And Carriers](ION/docs/AGENTS_ROLES_CARRIERS.md)

The long-form system reference is the living encyclopedia:

[ION Production Encyclopedia v4.0](ION/docs/encyclopedia/ION_Production_Encyclopedia_v4_0_LIVE_V96_V100_CONTEXT_SYSTEM_AND_AUTONOMOUS_LOOP_RECOVERY.md)

Use it for wider system history, context architecture, recovery lineage, and
the larger map. It is not the active startup authority. For live work, mount
through `ION/REPO_AUTHORITY.md`, `ION/02_architecture/ION_MOUNT_CONTRACT.md`,
current packets, registries, templates, and receipts.

## Public Collaboration

GitHub is the public collaboration and data plane. It is not ION runtime
authority.

Use these repository entry points:

- [Contributing](CONTRIBUTING.md) - branch, pull request, evidence, and
  validation expectations.
- [Security](SECURITY.md) - secret-handling rules and sensitive report path.
- [ION docs index](ION/docs/README.md) - public docs, setup guides, reports,
  and the encyclopedia.
- [ION content root](ION/README.md) - directory map for the full repository.

Issues, pull requests, comments, and external AI reviews are evidence and
proposals. They become ION state only through the same proof-gated path as any
other work.

---

## Getting Started

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -e .

# Verify state
python3 -m kernel.ion_status --ion-root . --json

# Run tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -m pytest ION/tests -q
```

Before acting in any carrier, read in order:

1. `ION/REPO_AUTHORITY.md`
2. `ION/02_architecture/ION_MOUNT_CONTRACT.md`
3. The current operating packet under `ION/docs/setup/`
4. The carrier profile under `ION/03_registry/`
5. The active context package under `ION/05_context/current/`

Do not treat README prose as runtime truth. Verify with the kernel, current
packets, gates, receipts, manifests, and tests.

The useful question is never *does this look right?*

```text
What receipt, gate, manifest, or test proves the claim?
```

---

## Why This Exists

AI work is becoming serious faster than its continuity machinery.

There are many systems that act alive for a few minutes. Fewer can tell you
what packet opened the work, what context was compiled, what template governed
the act, what proof passed, what Steward accepted, what receipt was emitted,
and what the next worker may inherit.

ION is built to make that chain explicit, inspectable, and durable across
models, tools, sessions, and carriers.

---

*A model can answer.*

*ION is built to continue.*
