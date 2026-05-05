import type { IonCockpitViewModel, IonReceiptHydrationRecord } from './ionRuntimeCockpitTypes';

type Props = { runtime: IonCockpitViewModel };

export function ReceiptHydrationPanel({ runtime }: Props) {
  const records = runtime.receipt_hydration?.records ?? [];
  return (
    <section className="ion-panel ion-receipt-hydration-panel">
      <div className="ion-section-title">RECEIPT HYDRATION</div>
      <div className="ion-runtime-grid">
        <Metric label="records" value={String(runtime.receipt_hydration?.receipt_count ?? records.length)} />
        <Metric label="unresolved" value={String(runtime.receipt_hydration?.unresolved_count ?? 0)} />
        <Metric label="conflicts" value={String(runtime.receipt_hydration?.hydration_conflict_count ?? 0)} />
      </div>
      <div className="ion-stream-stack">
        {records.slice(0, 8).map((record) => <HydrationRecord record={record} key={record.receipt_id} />)}
        {records.length === 0 && <div className="ion-empty-state">NO RECEIPT HYDRATION RECORDS</div>}
      </div>
    </section>
  );
}

function HydrationRecord({ record }: { record: IonReceiptHydrationRecord }) {
  const status = record.confidence === 'blocked' ? 'blocked' : record.latest_effective ? 'accepted' : 'requested';
  return (
    <article className={`ion-stream-event is-${status}`}>
      <div className="ion-stream-event-head">
        <span>{record.resolution_method}</span>
        <span>{record.resolved_bubble_id ?? 'unresolved'}</span>
        <b>{record.confidence}</b>
      </div>
      <p>{record.warning || record.receipt_id}</p>
    </article>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="ion-runtime-metric"><span>{label}</span><b>{value}</b></div>;
}
