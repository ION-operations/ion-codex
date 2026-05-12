# Codex Queue, Reconcile, and Live Telemetry Runbook v2.6.7

## Queue Loop

1. Inspect queue with `ion_codex_work_queue`.
2. Inspect runtime with `ion_daemon_status`.
3. Process one cycle with `ion_codex_queue_process_once`.
4. Inspect live telemetry with `ion_codex_worker_live_status`.
5. Optionally inspect worker UI projections:
   - `/cockpit/worker`
   - `/cockpit/worker/model.json`

## Stale Runner Recovery

If telemetry indicates stale/blocked runner posture, execute
`ion_codex_runner_reconcile` before retrying `ion_codex_queue_process_once`.

## Proof-Gated Return Boundary

Do not classify raw worker output as accepted state. Require proof-gated task
return path with context proof + template action proof before accepted-state
claims.
