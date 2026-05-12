# ION Queue Workflow Authoring Protocol

Protocol id: `ION_QUEUE_WORKFLOW_AUTHORING_PROTOCOL_V1`

## Purpose

Turn an operator goal into a reusable queued workflow for the ION ChatOps Bridge.
The workflow is a sequence of browser-chat prompts. It can orchestrate context
review, planning, agent handoff drafts, connector-backed drafts, verification,
and receipts.

## Object Model

`QueuePack`
: Root import object. Contains metadata, queue behavior, workflows, and optional
  package-level gates.

`Workflow`
: A named work surface such as "dAimon release proof" or "Google Cloud setup
  review".

`Chain`
: A phase group such as intake, planning, execution draft, verification, or
  receipt.

`Step`
: One queued ChatGPT message. The extension preserves the step as one message.

`Gate`
: A declared approval requirement. Gates are prompt-level warnings and do not
  replace actual connector or local bridge approval.

`Receipt`
: A requested output section that records what was done, what was not claimed,
  blockers, and next safe action.

## Compile Procedure

1. Parse the operator goal.
2. Declare authority posture and non-claims.
3. Identify required context packages or attachments.
4. Choose workflow phases.
5. Write each step as a self-contained prompt.
6. Add gates before any mutating or external-system action.
7. Add verification and receipt steps.
8. Validate against schema and checklist.
9. Return JSON or ZIP-ready package.

## Save And Load Behavior

The queue pack is saved by the user as a `.json` or `.zip`. The ION extension
loads it with Queue tab `Import Pack`. The extension does not treat the import
as approval to send every step. Manual start is the default.

## Forbidden Content

- secrets, tokens, private keys, cookies, passwords
- instructions to bypass human approval
- claims that the pack can mutate local files or cloud systems
- claims that a workflow is production-proven because a queue ran
- hidden chain-of-thought extraction requests
- destructive action without explicit approval gate

## Required Output Sections Inside Serious Step Prompts

Use these headings unless a step is intentionally tiny:

```text
CONFIRMED FACTS
ASSUMPTIONS
AUTHORITY / GATES
WORK
OUTPUT REQUIRED
STOP CONDITION
```

