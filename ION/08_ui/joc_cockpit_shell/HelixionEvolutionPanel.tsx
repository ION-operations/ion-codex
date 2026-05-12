import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export function HelixionEvolutionPanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const rebuild = runtime.helixion_joc_rebuild;
  const roles = Object.entries(rebuild?.product_roles ?? {});
  const surfaces = rebuild?.required_surfaces ?? [];
  const phases = rebuild?.next_build_sequence ?? [];
  const forbidden = rebuild?.forbidden_v1_capabilities ?? [];
  const ready = rebuild?.ready_for_phase_1 ? 'ready' : 'blocked';

  return (
    <section className="ion-panel ion-runtime-status-panel">
      <div className="ion-section-title">HELIXION JOC EVOLUTION</div>
      <div className={`ion-runtime-verdict is-${ready}`}>{rebuild?.status ?? 'not_documented'}</div>
      <div className="ion-runtime-objective">{rebuild?.decision ?? 'NO HELIXION REBUILD PLAN LOADED'}</div>
      <div className="ion-runtime-grid">
        <Metric label="phase 1" value={rebuild?.ready_for_phase_1 ? 'unlocked' : 'blocked'} />
        <Metric label="plan" value={rebuild?.master_plan_present ? 'present' : 'missing'} />
        <Metric label="registry" value={rebuild?.registry_present ? 'present' : 'missing'} />
      </div>
      <div className="ion-runtime-source-note">PRODUCT ROLES</div>
      <div className="ion-path-list">
        {roles.map(([name, role]) => (
          <div className="ion-path-row" key={name}>
            <span>{name}</span>
            <code>{role}</code>
          </div>
        ))}
      </div>
      <div className="ion-runtime-source-note">REQUIRED SURFACES</div>
      <div className="ion-blocked-list">
        {surfaces.map((surface) => <span key={surface}>{surface}</span>)}
      </div>
      <div className="ion-runtime-source-note">BUILD SEQUENCE</div>
      <div className="ion-path-list">
        {phases.slice(0, 5).map((phase, index) => (
          <div className="ion-path-row" key={phase}>
            <span>{String(index + 1).padStart(2, '0')}</span>
            <code>{phase}</code>
          </div>
        ))}
      </div>
      <div className="ion-runtime-source-note">FORBIDDEN V1 CAPABILITIES</div>
      <div className="ion-blocked-list">
        {forbidden.map((capability) => <span key={capability}>{capability}</span>)}
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="ion-runtime-metric"><span>{label}</span><b>{value}</b></div>;
}
