import type { ReactiveStreamEvent } from './reactiveTypes';

export function AutomationOverlayPanel({ events }: { events: ReactiveStreamEvent[] }) {
  const sessionEvents = events.filter((event) => event.loopId === 'SESSION_HEALTH_LOOP');
  const blocked = Array.from(new Set(sessionEvents.flatMap((event) => event.blockedCapabilities)));
  return (
    <section className="ion-panel ion-automation-overlay-panel" aria-label="Browser automation overlay">
      <div className="ion-section-title">BROWSER SESSION AUTOMATION OVERLAY</div>
      <div className="ion-overlay-grid">
        <OverlayMetric label="injection zones" value="display only" />
        <OverlayMetric label="extraction zones" value="display only" />
        <OverlayMetric label="dom health" value="not mounted" />
        <OverlayMetric label="credential lane" value="blocked" />
      </div>
      <div className="ion-overlay-frame" aria-label="Automation overlay preview">
        <div className="ion-overlay-target is-injection">INJECTION TARGET</div>
        <div className="ion-overlay-target is-extraction">EXTRACTION TARGET</div>
        <div className="ion-overlay-target is-health">DOM HEALTH GATE</div>
      </div>
      <div className="ion-section-title">BLOCKED AUTOMATION CAPABILITIES</div>
      <div className="ion-blocked-list">
        {blocked.map((cap) => <span key={cap}>{cap}</span>)}
      </div>
    </section>
  );
}

function OverlayMetric({ label, value }: { label: string; value: string }) {
  return <div className="ion-metric"><span>{label}</span><b>{value}</b></div>;
}
