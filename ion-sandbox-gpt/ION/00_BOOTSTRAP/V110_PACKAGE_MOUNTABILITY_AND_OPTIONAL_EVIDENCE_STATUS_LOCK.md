# V110 Package Mountability and Optional Evidence Status Lock

## Lock

V110 makes safe full-project packages mount cleanly after fresh extraction.

Generated package proof sidecars are evidence for the artifact that was emitted, but they cannot be required active state inside the same zip without creating a self-reference problem. The package cannot contain a final hash proof for itself and remain stable.

## Status Rule

The following surfaces are optional evidence in `kernel.ion_status`:

- `ION/05_context/current/TRUNK_PRESERVATION_REPORT_V107.json`
- `ION/05_context/current/SAFE_FULL_PROJECT_PACKAGE_RESULT_V109.json`

The V108 donor reconciliation audit remains active authoritative state:

- `ION/05_context/current/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json`

## Exit Condition

V110 is complete when:

- a freshly extracted safe full-project zip confirms root with `pyproject.toml` and `ION/REPO_AUTHORITY.md`
- `kernel.ion_status` does not degrade solely because generated package sidecars are absent
- package creation still requires the preservation gate before artifact emission
- protected and unexpected removals remain zero

## Authority

```yaml
production_authority: false
live_execution_authority: false
file_deletion_authority: false
```
