import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

type Props = { runtime: IonCockpitViewModel };

export function RuntimeDebugOverlayPanel({ runtime }: Props) {
  const overlay = runtime.runtime_debug_overlay ?? {};
  const sse = overlay.sse ?? {};
  const render = overlay.render ?? {};
  const hydration = overlay.hydration ?? {};
  const kernel = overlay.kernel ?? {};
  const watcher = overlay.watcher ?? {};
  return (
    <section className="ion-panel ion-runtime-debug-overlay-panel">
      <div className="ion-section-title">DEBUG OVERLAY</div>
      <div className={`ion-runtime-verdict is-${overlay.status ?? 'degraded'}`}>{overlay.status ?? 'degraded'}</div>
      <div className="ion-runtime-grid">
        <Metric label="sse/sec" value={String(sse.events_per_second ?? 0)} />
        <Metric label="dropped" value={String(sse.dropped_events ?? 0)} />
        <Metric label="render p95" value={formatMs(render.p95_render_ms)} />
        <Metric label="db hydrate" value={formatMs(hydration.db_hydration_ms)} />
        <Metric label="receipt gaps" value={String(hydration.unresolved_receipts ?? 0)} />
        <Metric label="conflicts" value={String(hydration.hydration_conflicts ?? 0)} />
        <Metric label="lane proj" value={formatMs(kernel.lane_timeline_projection_ms)} />
        <Metric label="watch refresh" value={formatMs(watcher.refresh_ms)} />
      </div>
      <div className="ion-runtime-source-note">
        SSE {String(sse.measurement_mode ?? 'NOT_CONNECTED')} / render {String(render.measurement_mode ?? 'PROJECTED_ONLY')} / watcher {String(watcher.measurement_mode ?? 'NOT_CONNECTED')}
      </div>
    </section>
  );
}

function formatMs(value: unknown) {
  return typeof value === 'number' ? `${value}ms` : 'n/a';
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="ion-runtime-metric"><span>{label}</span><b>{value}</b></div>;
}
