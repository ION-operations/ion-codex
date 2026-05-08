# Terminal Proof Receipt Packet Promotion Proposal Draft

Status: promotion proposal draft, not accepted ION canon.

Created: 2026-05-08T18:50:31Z

Candidate:

```text
terminal_proof_receipt_packet
```

## Proposed Outcome

```text
ACCEPT_AS_TEMPLATE_ONLY
```

The candidate should be considered for template-only promotion because it maps
directly to an existing ION/Codex safety need: command and test claims must be
backed by concrete command/result evidence, not prose.

## Evidence

- `ION/05_context/current/ai_assistant_work/template_specs/terminal_proof_receipt_packet.template_spec.yaml`
- `ION/05_context/current/ai_assistant_work/template_instances/terminal_proof_receipt_packet.minimal_valid.instance.json`
- `ION/05_context/current/ai_assistant_work/template_instances/terminal_proof_receipt_packet.expected_rejection.instance.json`
- `ION/05_context/current/ai_assistant_work/candidate_lifecycle/scorecards/terminal_proof_receipt_packet_scorecard_v0_1.yaml`
- `ION/tests/test_kernel_ai_assistant_work_template_instances.py`

## Why This Is Safe To Promote First

This candidate does not create a new domain identity, route owner, product
front-door, or execution authority. It only tightens proof around something ION
already requires: terminal/test evidence must name the command, result, scope,
and non-claims.

## Required Review Before Landing

1. Steward/human acceptance of the exact target accepted path.
2. Nemesis check that the template rejects missing command/result proof.
3. Scribe receipt naming accepted path and source candidate paths.
4. Focused tests proving accepted template loading still works.

## Open Questions

- Should the accepted target live under an existing template registry, a Codex
  proof protocol, or both?
- Should this remain Codex-specific or generalize to all tool-execution proof?

## Non-Claims

- This proposal does not land the template.
- This proposal does not mutate `ION/03_registry/`.
- This proposal does not grant shell, production, live execution, secrets,
  deployment, or git push authority.
