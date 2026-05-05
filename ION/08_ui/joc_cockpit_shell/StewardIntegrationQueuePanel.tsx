import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export function StewardIntegrationQueuePanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const items = runtime.queues.steward_integration ?? [];
  return (
    <section className="ion-panel ion-steward-queue-panel">
      <div className="ion-section-title">STEWARD INTEGRATION QUEUE</div>
      {items.map((item, index) => (
        <article className="ion-runtime-card" key={index}>
          <div className="ion-runtime-card-head"><b>{String(item.role ?? item.id ?? `ITEM ${index + 1}`)}</b><span>ACCEPTED INPUT</span></div>
          <pre>{JSON.stringify(item, null, 2)}</pre>
        </article>
      ))}
      {items.length === 0 && <div className="ion-empty-state">NO ACCEPTED RETURNS WAITING FOR STEWARD</div>}
    </section>
  );
}
