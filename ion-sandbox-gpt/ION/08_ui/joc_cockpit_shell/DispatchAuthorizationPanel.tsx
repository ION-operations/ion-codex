import { dispatchAuthorizationFixture, type DispatchAuthorizationViewModel } from './dispatchAuthorizationTypes';
import { GovernorVerdictRail } from './GovernorVerdictRail';

export function DispatchAuthorizationPanel({
  model = dispatchAuthorizationFixture,
}: {
  model?: DispatchAuthorizationViewModel;
}) {
  const blocked = model.authorization_verdict.startsWith('BLOCKED');

  return (
    <section className="ion-dispatch-auth-panel" aria-label="Dispatch authorization panel">
      <header className="ion-panel-header">
        <div>
          <span className="ion-kicker">MISSION AUTHORIZATION</span>
          <h2>{model.mission_id}</h2>
        </div>
        <span className={`ion-badge ${blocked ? 'is-blocked' : 'is-supervised'}`}>
          {model.authorization_verdict}
        </span>
      </header>

      <div className="ion-route-summary-grid">
        <div><span className="ion-label">TARGET</span><strong>{model.selected_target}</strong></div>
        <div><span className="ion-label">RING</span><strong>{model.compute_ring}</strong></div>
        <div><span className="ion-label">ACCESS</span><strong>{model.access_method}</strong></div>
        <div><span className="ion-label">CLAIM</span><strong>{model.claim_lane}</strong></div>
        <div><span className="ion-label">COST</span><strong>${model.estimated_cost_usd.toFixed(2)}</strong></div>
        <div><span className="ion-label">QUALITY</span><strong>{model.quality_band}</strong></div>
      </div>

      <GovernorVerdictRail model={model} />

      {model.blocked_capabilities.length > 0 && (
        <div className="ion-blocked-capabilities">
          <span className="ion-label">BLOCKED CAPABILITIES</span>
          {model.blocked_capabilities.map((capability) => (
            <span className="ion-badge is-blocked" key={capability}>{capability}</span>
          ))}
        </div>
      )}

      <div className="ion-operator-reason">
        <span className="ion-label">OPERATOR REASON</span>
        <p>{model.operator_reason}</p>
        <span className="ion-label">NEXT REQUIRED ACTION</span>
        <p>{model.next_required_action}</p>
      </div>

      <footer className="ion-non-authority-footer">
        PROJECTION ONLY / NO LIVE DISPATCH / NO PRODUCTION AUTHORITY
      </footer>
    </section>
  );
}
