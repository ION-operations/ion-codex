# ION/JOC Handoff Package Assembly Plan and Checksum Preview Protocol

V69 exists so the cockpit can show the shape of a future handoff/export package after V68, without materializing that package.

The view model renders:

- package intent
- item plan
- manifest section references
- evidence references
- checksum preview records
- blocked capability ledger
- future materialization authority requirements
- operator review lane

Core law:

```text
A handoff manifest preview may become a package assembly plan preview.
A package assembly plan preview may not become package materialization.
```

V69 is preview-only. It must keep `file_system_write_authorized`, `zip_creation_authorized`, `checksum_file_write_authorized`, `artifact_export_authorized`, `external_transfer_authorized`, `memory_write_authorized`, `canonical_graph_write_authorized`, and `source_summary_rewrite_authorized` false.
