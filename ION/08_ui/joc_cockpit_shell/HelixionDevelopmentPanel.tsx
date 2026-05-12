import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export function HelixionDevelopmentPanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const rebuild = runtime.helixion_joc_rebuild;
  const urls = rebuild?.development_urls ?? [];
  const bundle = rebuild?.react_bundle ?? {};
  const packageInfo = rebuild?.orchestration_context_package ?? {};

  return (
    <section className="ion-panel ion-helixion-development-panel">
      <div className="ion-section-title">HELIXION DEVELOPMENT SURFACE</div>
      <div className={`ion-runtime-verdict is-${String(bundle.status ?? 'unknown')}`}>REACT {String(bundle.status ?? 'unknown')}</div>
      <div className="ion-runtime-objective">Local-first JOC shell. Public Helixion routing remains a separate gated phase.</div>
      <div className="ion-runtime-grid">
        <Metric label="capsule" value={rebuild?.latest_capsule_entry_id ?? 'none'} />
        <Metric label="checkpoint" value={rebuild?.latest_codex_solo_checkpoint_id ?? 'none'} />
        <Metric label="dist" value={String(bundle.dist_root ?? 'missing')} />
      </div>
      <div className="ion-runtime-source-note">LOCAL ROUTES</div>
      <div className="ion-path-list">
        {urls.map((url) => (
          <div className="ion-path-row" key={url}>
            <span>URL</span>
            <code>{url}</code>
          </div>
        ))}
        <div className="ion-path-row">
          <span>LEGACY</span>
          <code>/cockpit/legacy</code>
        </div>
        <div className="ion-path-row">
          <span>STATIC</span>
          <code>{String(bundle.static_route ?? '/joc-static/*')}</code>
        </div>
      </div>
      <div className="ion-runtime-source-note">ORCHESTRATION PACKAGE</div>
      <div className="ion-path-list">
        <div className="ion-path-row">
          <span>SKILL</span>
          <code>{String(packageInfo.ion_skill_id ?? 'helixion-joc-orchestration')}</code>
        </div>
        <div className="ion-path-row">
          <span>PACKAGE</span>
          <code>{String(packageInfo.package_json_path ?? 'ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_ORCHESTRATION_CONTEXT_PACKAGE.json')}</code>
        </div>
        <div className="ion-path-row">
          <span>RECEIPT</span>
          <code>{rebuild?.latest_history_receipt ?? 'none'}</code>
        </div>
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="ion-runtime-metric"><span>{label}</span><b>{value}</b></div>;
}
