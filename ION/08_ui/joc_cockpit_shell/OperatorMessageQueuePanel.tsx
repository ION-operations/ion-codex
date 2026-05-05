import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export function OperatorMessageQueuePanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const items = runtime.queues.operator_messages ?? [];
  return (
    <section className="ion-panel ion-operator-queue-panel">
      <div className="ion-section-title">OPERATOR MESSAGE QUEUE</div>
      {items.map((item, index) => (
        <article className="ion-runtime-card" key={index}>
          <div className="ion-runtime-card-head"><b>{String(item.classification ?? item.status ?? 'queued')}</b><span>{String(item.id ?? index + 1)}</span></div>
          <p>{String(item.text ?? item.message ?? '')}</p>
        </article>
      ))}
      {items.length === 0 && <div className="ion-empty-state">NO QUEUED OPERATOR MESSAGES</div>}
    </section>
  );
}
