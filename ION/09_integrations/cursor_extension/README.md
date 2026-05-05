# ION Cursor Cockpit Extension Scaffold

This extension is a Cursor/VS Code-compatible control and visibility surface for ION. It does not become ION authority. It detects the ION shell root, runs kernel commands, watches active packet files, and renders a sidebar plus JOC webview from `ACTIVE_COCKPIT_VIEW_MODEL.json`.

## Commands

- `ION: Continue` → runs `kernel.ion_carrier_continue`
- `ION: Status` → runs `kernel.ion_status`
- `ION: Audit Carrier Workflow` → runs `kernel.ion_carrier_workflow_audit`
- `ION: Refresh Cockpit View Model` → runs `kernel.ion_cockpit_view_model --write`
- `ION: Open JOC Cockpit` → opens a webview rendering the live cockpit projection

## Authority boundary

The extension reads and invokes kernel commands only. It must not directly mutate active packets, accept Task returns, resolve gates, or integrate state outside ION kernel pathways.
