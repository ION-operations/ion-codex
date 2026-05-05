# END-TO-END VALIDATION RUNBOOK

## Purpose

This runbook defines the minimum serious validation loop for the first ION custom GPT build.

The goal is not just to confirm that the GPT answers questions. The goal is to verify that the GPT can:

- ingest a working continuity bundle,
- resume conservatively and honestly,
- preserve live obligations,
- export an updated bundle,
- and support continuity across a fresh chat restart.

This runbook assumes:

- the builder-ready instruction text has been pasted into the custom GPT,
- the curated Knowledge pack has been uploaded,
- Data Analysis is enabled,
- and no Actions are enabled yet.

## Validation stages

### Stage 1 — Builder integrity

Confirm:

- the full `01_BUILDER_READY_INSTRUCTIONS.md` was pasted
- the Knowledge pack files from `knowledge_pack/` were uploaded
- Data Analysis is enabled
- the GPT preview is responsive
- the GPT states its continuity posture correctly when no bundle is present

Expected result:

- the GPT should explain that it expects a working continuity bundle or equivalent project files
- it should not pretend to have active project state when none has been uploaded

### Stage 2 — Clean working-bundle resume

Upload the working example bundle from:

- `ION/07_templates/custom_gpt/examples/generated/working_bundle_example.zip`

Ask:

- Resume from this continuity bundle and tell me the current state.
- What are the live obligations, current priorities, unresolved questions, and next likely actions?

Expected result:

- correct project identity
- correct current phase
- preservation of active temporal obligations
- preservation of unresolved questions
- conservative but useful next-step summary
- no hallucinated missing history

### Stage 3 — Slightly stale continuity handling

Edit or imagine the uploaded bundle is older than the current day and ask:

- Resume conservatively from this bundle and tell me any continuity risks.

Expected result:

- the GPT should warn about stale state if appropriate
- it should distinguish known state from inferred state
- it should not overclaim certainty
- it should still resume coherently

### Stage 4 — Small state mutation and export

After a small working turn, ask:

- Update the continuity bundle to reflect today’s decisions and export a new working bundle.

Expected result:

- continuity generation incremented
- updated timestamps
- refreshed continuity summary
- updated recent decisions
- preserved unresolved questions
- preserved active temporal objects
- deterministic export naming if the GPT is instructed to name files predictably

### Stage 5 — Fresh-chat restart

In a new chat with the same custom GPT:

- upload the exported updated working bundle
- ask the GPT to resume from it

Expected result:

- continuity remains intact
- current mission and decisions survive the reset
- the GPT acts as though the prior chat loss was operationally recoverable

### Stage 6 — Manual local-vault flow

Using the example vault bundle docs and your local process:

- archive the exported working bundle into a vault copy
- later restore the working bundle from the vault
- re-upload into a fresh chat

Expected result:

- continuity can survive outside ChatGPT
- the GPT only needs the decrypted working bundle, not the archive

## Minimum pass criteria

The build should not be treated as viable unless all of the following are true:

- clean resume works
- stale-bundle caution works
- updated export works
- fresh-chat restart works
- continuity generation is preserved
- active obligations and unresolved questions remain intact
- the GPT does not confuse doctrine with mutable state
- the GPT does not rely on ambient chat memory to resume

## Failure signatures to watch for

Major red flags include:

- GPT ignores the bundle and answers generically
- GPT drops unresolved questions
- GPT fails to preserve active temporal objects
- GPT exports malformed structure
- GPT fails to increment continuity generation
- GPT hallucinates history not present in the bundle
- GPT loses state across a fresh chat even with the updated bundle uploaded

## Recommended first manual prompts

Use prompts such as:

- Resume from this continuity bundle and give me the current state.
- Audit this bundle for continuity gaps and stale-state risk.
- Update this bundle after today’s work and export a new working continuity bundle.
- Compact this bundle while preserving live obligations and unresolved questions.
- Tell me exactly what changed in the continuity state before exporting.

## Present conclusion

If this runbook passes, the custom GPT is no longer just doctrinally plausible.

It has demonstrated the first real continuity loop:
resume → work → export → restart → resume again.
