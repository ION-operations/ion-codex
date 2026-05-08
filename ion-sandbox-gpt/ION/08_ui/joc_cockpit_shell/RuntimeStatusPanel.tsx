import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

type Props = { runtime: IonCockpitViewModel };

export function RuntimeStatusPanel({ runtime }: Props) {
  const top = runtime.top_bar;
  const packageVerdict = runtime.safe_full_project_package?.preservation_report?.packaging_verdict
    ?? runtime.safe_full_project_package?.zip_root_audit?.verdict
    ?? 'unknown';
  const donorVerdict = runtime.v72_mcp_donor_reconciliation?.reconciliation_verdict
    ?? 'unknown';
  const bundleState = top.execution_bundle_materialized === false
    ? 'deferred'
    : top.execution_bundle_materialized === true
      ? 'built'
      : 'unknown';
  return (
    <section className="ion-panel ion-runtime-status-panel">
      <div className="ion-section-title">LIVE RUNTIME STATUS</div>
      <div className={`ion-runtime-verdict is-${runtime.runtime.status}`}>{runtime.runtime.status}</div>
      <div className="ion-runtime-objective">{top.objective}</div>
      <div className="ion-runtime-grid">
        <Metric label="mode" value={runtime.runtime.mode} />
        <Metric label="hook" value={top.hook_status} />
        <Metric label="spawn" value={`${top.spawn_count}/${top.spawn_rows_total}`} />
        <Metric label="deferred" value={String(top.deferred_spawn_count ?? 0)} />
        <Metric label="bundle" value={bundleState} />
        <Metric label="gates" value={String(top.gate_count)} />
        <Metric label="returns" value={`A${top.return_counts.accepted ?? 0} R${top.return_counts.rejected ?? 0} P${top.return_counts.pending ?? 0}`} />
        <Metric label="steward q" value={String(top.steward_queue_count)} />
        <Metric label="package" value={packageVerdict} />
        <Metric label="mcp donor" value={donorVerdict} />
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="ion-runtime-metric"><span>{label}</span><b>{value}</b></div>;
}
