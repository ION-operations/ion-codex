import type { IonCockpitViewModel, IonSpawnRow } from './ionRuntimeCockpitTypes';

export function SpawnQueuePanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const rows = runtime.agents.spawn_rows ?? [];
  return (
    <section className="ion-panel ion-spawn-queue-panel">
      <div className="ion-section-title">SPAWN QUEUE</div>
      <div className="ion-table ion-spawn-table">
        <div className="ion-table-head"><span>#</span><span>role</span><span>spawn</span><span>return</span></div>
        {rows.map((row) => <SpawnRow key={`${row.role}-${row.index}`} row={row} />)}
        {rows.length === 0 && <div className="ion-empty-state">NO SPAWN ROWS</div>}
      </div>
    </section>
  );
}

function SpawnRow({ row }: { row: IonSpawnRow }) {
  return (
    <div className={`ion-table-row is-${row.status}`}>
      <span>{row.index}</span>
      <b>{row.role}</b>
      <span>{row.spawn ? 'true' : 'false'}</span>
      <span>{row.return_recorded ? 'captured' : row.status}</span>
      {row.context_package_path && <code className="ion-row-path">{row.context_package_path}</code>}
    </div>
  );
}
