# B04_CHATOPS_QUEUE_CONTROL_AND_FILE_ITEMS_001

packet_id: B04_CHATOPS_QUEUE_CONTROL_AND_FILE_ITEMS_001
status: implemented_candidate
accepted_state: ACCEPTED_AS_B04_QUEUE_CONTROL_CANDIDATE
created: 2026-05-11
phase: extension_micro_shell_queue_control
production_authority: false
live_execution_authority: false
secrets_authority: false

## Goal

Make the floating browser queue panel usable as an operator-controlled sequence editor, and repair queue Play so it has a better chance of sending after ChatGPT unlocks the Send button.

## Implemented Behavior

Queue item controls:

```text
edit item
save edit
cancel edit
delete item
move earlier
move later
drag to reorder
```

Queue Play repair:

```text
prefer an enabled send button over stale disabled send-like buttons
respect aria-disabled and data-disabled
after pasting queued text, wait up to 2.6 seconds for Send to unlock
report the last readiness reason when Send remains unavailable
```

File queue lane:

```text
⇪ opens an operator file picker
selected files/images/ZIPs become queue items
file payloads are held in browser memory only
playing a file item attempts a visible ChatGPT drag/drop
no Send click is performed for file items
payloads are lost on page or extension reload and must be re-selected
```

## Safety Boundary

The queue is still an operator-visible browser carrier surface:

```text
no silent browser send beyond explicit queue Play / Auto Play controls
no production authority
no live execution authority
no credential or local path authority
no persistent file access
no upload guarantee when ChatGPT rejects synthetic drag/drop
```

## UI Notes

The existing bottom-left ChatGPT account/menu area appears to move upward as ChatGPT layout shifts. This creates possible room for later left-rail utility buttons, but this packet does not claim that area or add new left-side tools. The packet stays focused on the right queue panel.

## Validation

```text
node --check ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
node ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js
unzip -t ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_queue_control_file_items_20260511.zip
```

The smoke simulation still confirms:

```text
valid YAML action packet detected
inline ion_action mention ignored
documentation snippet ignored
assistant container action detected
rendered code block action detected
DOM registry emits message/code/control marker stats
safe mode blocks candidate send
```

## Touched Paths

```text
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_QUEUE_CONTROL_AND_FILE_ITEMS_001.md
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_QUEUE_CONTROL_AND_FILE_ITEMS_001_RECEIPT.json
ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
ION/09_integrations/browser_extension/ion_chatops_bridge/README.md
ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_queue_control_file_items_20260511.zip
```

## Package Artifact

```text
zip_path: ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_queue_control_file_items_20260511.zip
zip_sha256: a9aceb1fb51d9b9b88390d7af5289af3e3ffdb09644cff62c5520003d909919d
zip_entries: 23
```

## Acceptance Boundary

Accepted:

```text
B04 queue control candidate
row edit/save/delete candidate
drag and arrow reorder candidate
file/image/ZIP queue item candidate
improved queued text send-button wait candidate
```

Not claimed:

```text
complete browser automation canon
guaranteed ChatGPT synthetic drop acceptance
production authority
live execution authority
silent browser send
```
