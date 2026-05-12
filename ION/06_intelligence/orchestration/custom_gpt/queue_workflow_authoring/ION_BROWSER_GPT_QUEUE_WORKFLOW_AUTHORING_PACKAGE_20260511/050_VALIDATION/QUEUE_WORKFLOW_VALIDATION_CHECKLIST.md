# Queue Workflow Validation Checklist

Before giving the user a queue pack, validate these points.

## Manifest

- `schema_id` is exactly `ion.extension.queue_pack.v1`.
- `pack_id` is stable and filesystem-safe.
- `title` and `objective` are human-readable.
- `manual_start_required` is `true` unless the user explicitly asked otherwise.
- `auto_play_requested` is `false` unless the user explicitly asked otherwise.
- `include_step_headers` is `true`.

## Structure

- Work is grouped into workflows, chains, and steps.
- Every step has `id`, `title`, `tags`, and either `prompt`, `text`, or
  `prompt_ref`.
- Prompt refs resolve to files present in the ZIP layout.
- Total steps are below 120.
- Each prompt is below 24,000 characters.

## ION Safety

- Production authority is false.
- Live execution authority is false.
- Secrets authority is false.
- Mutating, cloud, deployment, billing, account, destructive, or local-file
  operations are explicitly approval-gated.
- No credentials, tokens, cookies, private keys, or connection strings are
  embedded.
- No hidden chain-of-thought request is included.

## Workflow Quality

- The first step scopes intent and boundaries.
- There is a planning/orchestration step.
- Serious workflows include verification and receipt steps.
- Each step states output format and stop condition.
- The workflow separates confirmed facts, assumptions, blockers, and next safe
  action.

## User Handoff

Tell the user:

- where the file is
- whether it is JSON or ZIP
- how to import it through the ION bridge Queue tab
- that importing does not approve live execution or mutation

