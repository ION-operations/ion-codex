# ION Work Packet — Artifact And File Lane

## Status

`PROPOSED_WORK_PACKET`

## Objective

Create an Artifacts/Packages/Sandbox lane in the browser extension for file and package exchange between ChatGPT Browser and local ION.

This packet should treat all external files as witness/candidate material until ION ingests, hashes, classifies, gates, and receipts them.

## Scope

Implement UI and bridge behavior for:

```text
list local ION exportable packages if daemon supports it
show package manifests and hashes
capture ChatGPT code blocks as candidate artifacts
capture generated/downloadable files where browser APIs allow
send candidate text/artifact to daemon inbox
queue sandbox return review
show artifact duplicate warnings
show Drive/local-folder references when present
```

## Artifact Types

Support visible classification:

```text
candidate_patch
review_report
markdown_doc
zip_package
console_log
screenshot_bundle
drive_reference
chat_code_block
yaml_action_block
unknown_witness
```

## File Transfer Law

```text
Drive may carry artifacts.
Downloads may carry artifacts.
ChatGPT may produce artifacts.
The extension may detect and stage artifacts.
ION state changes only after ingest, proof, Steward decision, and receipt.
```

## UI Tabs

Relevant tabs:

```text
Packages
Sandbox
Artifacts
```

### Packages

```text
export package
show active package
copy manifest
open package folder via daemon if supported
prepare package for ChatGPT
```

### Sandbox

```text
capture patch/report from chat
diff preview latest if daemon supports it
submit sandbox return candidate
queue Codex review
show status transition
```

### Artifacts

```text
show detected chat artifacts
show Drive/link references
show local candidate returns
show hashes/manifests where available
show duplicate and stale-base warnings
```

## Required Manifest

When possible, require or generate:

```json
{
  "artifact_id": "string",
  "source": "chatgpt_browser",
  "authority": "proposal_only",
  "artifact_type": "candidate_patch",
  "base_package_sha256": "optional",
  "files": [],
  "allowed_effect": "steward_review_only"
}
```

## Acceptance Criteria

```text
Artifacts tab lists detected code blocks/files/links
Sandbox tab can stage a candidate return from selected content
daemon receives candidate artifact through approved call
artifact status shows pending/reviewed/blocked if daemon provides state
duplicate/stale warnings are visible where detectable
no artifact is applied directly
no local file is uploaded without user approval
```

## Validation

```text
capture code block as candidate patch
capture markdown as review report
send candidate to daemon inbox
verify hash/classification appears if supported
queue Codex review with approval
confirm no direct patch apply occurs
```

## Authority Boundary

Allowed:

```text
artifact detection
manifest generation
approved staging to inbox
approved queue review
```

Forbidden:

```text
silent upload
silent download execution
automatic patch apply
automatic git mutation
Drive treated as authority
```
