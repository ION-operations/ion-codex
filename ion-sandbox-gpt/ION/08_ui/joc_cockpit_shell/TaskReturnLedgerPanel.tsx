import type { IonCockpitViewModel, IonTaskReturn } from './ionRuntimeCockpitTypes';

export function TaskReturnLedgerPanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const returns = runtime.agents.returns ?? [];
  return (
    <section className="ion-panel ion-return-ledger-panel">
      <div className="ion-section-title">TASK RETURN LEDGER</div>
      {returns.map((item) => <ReturnCard key={`${item.role}-${item.index}-${item.path}`} item={item} />)}
      {returns.length === 0 && <div className="ion-empty-state">NO TASK RETURNS CAPTURED</div>}
    </section>
  );
}

function ReturnCard({ item }: { item: IonTaskReturn }) {
  return (
    <article className={`ion-runtime-card authority-${String(item.authority_class ?? '').toLowerCase()}`}>
      <div className="ion-runtime-card-head"><b>{item.role}</b><span>{item.decision}</span></div>
      <div className="ion-authority-scope">{item.authority_class ?? 'PENDING_TASK_RETURN'}</div>
      {item.path && <code>{item.path}</code>}
    </article>
  );
}
