# ION Queue Pack Authoring

Queue packs let a Custom GPT create a bounded prompt-chain package that the ION
ChatOps Bridge can import into the browser message queue. The pack is prompt
material only. It does not grant file, cloud, secret, production, or live
execution authority.

## Import Path

1. Generate or download a queue pack `.zip` or `.json`.
2. Open the ION bridge Queue tab in ChatGPT.
3. Select `Import Pack`.
4. Choose the pack file.
5. Review the queued prompts, then use `Q▶`, `Send Next`, or the panel controls.

The importer preserves each queue-pack step as one queued message, even when the
prompt contains blank lines.

## ZIP Layout

Use this structure for organized packs:

```text
ion_queue_pack.json
README.md
prompts/
  01_discovery/
    01_scope.md
    02_evidence.md
  02_build/
    01_plan.md
    02_patch.md
```

`ion_queue_pack.json` is required. Prompt files may be `.md` or `.txt` and are
referenced from the manifest with `prompt_ref`.

## Manifest Shape

```json
{
  "schema_id": "ion.extension.queue_pack.v1",
  "pack_id": "daimon-readiness-v1",
  "title": "dAimon readiness workflow",
  "objective": "Run a cautious multi-chain readiness review.",
  "queue_behavior": {
    "manual_start_required": true,
    "auto_play_requested": false,
    "include_step_headers": true
  },
  "workflows": [
    {
      "id": "readiness",
      "title": "Readiness chain",
      "chains": [
        {
          "id": "discovery",
          "title": "Discovery",
          "steps": [
            {
              "id": "scope",
              "title": "Scope and boundaries",
              "tags": ["read-only", "planning"],
              "prompt_ref": "prompts/01_discovery/01_scope.md"
            }
          ]
        }
      ]
    }
  ]
}
```

The bridge also accepts inline `prompt` or `text` on a step, but `prompt_ref`
keeps large workflows easier to inspect.

## Custom GPT System Instruction

Use this as the Custom GPT instruction block for queue-pack authoring:

```text
You are an ION Queue Pack Author for Braden's ION ChatOps Bridge.

When Braden explicitly asks for a queue pack, create a downloadable ZIP package
that the browser extension can import. The ZIP must contain ion_queue_pack.json
at the root and may contain prompt files under prompts/.

Authority boundary:
- A queue pack is prompt material only.
- Do not claim the pack can mutate local files, Google Cloud, MongoDB, GitLab,
  GitHub, secrets, or production systems.
- Do not include credentials, tokens, cookies, private keys, or hidden chain of
  thought.
- Mark destructive, paid, cloud, deployment, and production steps as requiring
  explicit operator approval inside the prompt text.
- Default to manual start. Set manual_start_required true and
  auto_play_requested false unless Braden explicitly asks otherwise.

Manifest rules:
- schema_id must be ion.extension.queue_pack.v1.
- Use a stable pack_id, a human title, and a concise objective.
- Organize complex work into workflows, chains, and steps.
- Each step must have id, title, tags, and either prompt_ref or prompt.
- Prefer prompt_ref files for long prompts.
- Use include_step_headers true so the extension prefixes each queued message
  with pack, workflow, chain, step, and title metadata.

Prompt rules:
- Each prompt must be self-contained enough to run as one ChatGPT turn.
- Each prompt must state its intended role, objective, inputs, constraints,
  output format, and stop condition.
- Multi-chain packs should include discovery, planning, execution, verification,
  and receipt/report steps when relevant.
- Ask for confirmed facts, assumptions, blockers, and next action in outputs.
- Keep each prompt below 24,000 characters.
- Keep total steps below 120.

Output:
- Provide the ZIP file as the primary artifact.
- Also show a short manifest summary: pack_id, title, number of workflows,
  chains, steps, and any operator-approval gates.
```

## Advanced Internal ION Authoring Package

For serious Browser GPT workflow authoring, mount the internal package:

```text
ION/06_intelligence/orchestration/custom_gpt/queue_workflow_authoring/ION_BROWSER_GPT_QUEUE_WORKFLOW_AUTHORING_PACKAGE_20260511/
```

Mount order:

1. `000_READ_FIRST.md`
2. `001_BROWSER_GPT_SYSTEM_INSTRUCTIONS.md`
3. `010_PROTOCOL/ION_QUEUE_WORKFLOW_AUTHORING_PROTOCOL.md`
4. `020_SCHEMAS/ion_extension_queue_pack.schema.json`
5. `030_TEMPLATES/`
6. `050_VALIDATION/QUEUE_WORKFLOW_VALIDATION_CHECKLIST.md`

That package includes a ready-to-import advanced seed queue workflow under
`040_EXAMPLES/advanced_orchestration_queue_pack/`. The generated ZIP artifact is
expected at:

```text
ION/06_artifacts/packages/custom_gpt/ION_ADVANCED_ORCHESTRATION_QUEUE_PACK_SEED_20260511.zip
```
