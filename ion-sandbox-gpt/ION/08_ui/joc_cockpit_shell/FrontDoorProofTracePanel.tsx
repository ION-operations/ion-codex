import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

type Props = { runtime: IonCockpitViewModel };

export function FrontDoorProofTracePanel({ runtime }: Props) {
  const trace = runtime.front_door_proof_trace;
  const stages = trace?.stage_sequence ?? [];
  const status = trace?.proof_complete ? 'ready' : 'degraded';
  return (
    <section className="ion-panel ion-front-door-proof-panel">
      <div className="ion-section-title">FRONT-DOOR PROOF</div>
      <div className={`ion-runtime-verdict is-${status}`}>{trace?.verdict ?? 'NO FRONT-DOOR TRACE'}</div>
      <div className="ion-runtime-grid">
        <Metric label="stages" value={String(stages.length)} />
        <Metric label="missing" value={String(trace?.missing_witness_paths?.length ?? 0)} />
        <Metric label="authority" value={trace?.production_authority ? 'production' : 'non-production'} />
      </div>
      <div className="ion-stream-stack">
        {stages.slice(0, 8).map((stage) => (
          <article className={`ion-stream-event is-${stage.status ?? 'requested'}`} key={`${stage.sequence}-${stage.stage}`}>
            <div className="ion-stream-event-head">
              <span>{stage.organ ?? 'organ'}</span>
              <span>{stage.stage ?? 'stage'}</span>
              <b>{stage.status ?? 'unknown'}</b>
            </div>
            <p>{stage.detail || stage.witness_path || stage.receipt_id}</p>
          </article>
        ))}
        {stages.length === 0 && <div className="ion-empty-state">NO FRONT-DOOR PROOF TRACE</div>}
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="ion-runtime-metric"><span>{label}</span><b>{value}</b></div>;
}
