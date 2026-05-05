import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export function CarrierTurnPanel({ runtime }: { runtime: IonCockpitViewModel }) {
  return (
    <section className="ion-panel ion-carrier-turn-panel">
      <div className="ion-section-title">CARRIER TURN</div>
      <div className="ion-runtime-chain">
        <span>OPERATOR</span>
        <b>QUEUE</b>
        <b>WORK</b>
        <b>SPAWN</b>
        <b>RETURN</b>
        <b>STEWARD</b>
        <span>OUTPUT</span>
      </div>
      <div className="ion-path-list">
        <Path label="work" value={runtime.source_paths.work} />
        <Path label="turn" value={runtime.source_paths.turn} />
        <Path label="spawn" value={runtime.source_paths.spawn} />
        <Path label="ledger" value={runtime.source_paths.ledger} />
      </div>
    </section>
  );
}

function Path({ label, value }: { label: string; value?: string }) {
  return <div className="ion-path-row"><span>{label}</span><code>{value ?? 'missing'}</code></div>;
}
