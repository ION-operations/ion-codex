import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export function HumanGateQueuePanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const gates = runtime.queues.human_gates ?? [];
  return (
    <section className="ion-panel ion-human-gate-panel">
      <div className="ion-section-title">HUMAN GATES</div>
      {gates.map((gate, index) => (
        <article className={`ion-runtime-card ${String(gate.status ?? 'open').toLowerCase() === 'open' ? 'is-blocked' : 'is-ok'}`} key={index}>
          <div className="ion-runtime-card-head"><b>{String(gate.id ?? `GATE ${index + 1}`)}</b><span>{String(gate.status ?? 'open')}</span></div>
          <p>{String(gate.reason ?? gate.prompt ?? 'operator decision required')}</p>
        </article>
      ))}
      {gates.length === 0 && <div className="ion-empty-state is-ok">NO OPEN HUMAN GATES</div>}
    </section>
  );
}
