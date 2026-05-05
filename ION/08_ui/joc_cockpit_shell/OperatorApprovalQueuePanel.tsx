import { operatorApprovalFixture, type OperatorApprovalQueueViewModel } from './operatorApprovalTypes';

export function OperatorApprovalQueuePanel({ model = operatorApprovalFixture }: { model?: OperatorApprovalQueueViewModel }) {
  const blocked = model.approval_verdict.startsWith('BLOCKED') || model.approval_verdict === 'OPERATOR_DENIED';
  return (
    <section className="ion-operator-approval-panel" aria-label="Operator approval queue">
      <header className="ion-panel-header">
        <div>
          <span className="ion-kicker">OPERATOR APPROVAL QUEUE</span>
          <h2>{model.mission_id}</h2>
        </div>
        <span className={`ion-badge ${blocked ? 'is-blocked' : 'is-supervised'}`}>{model.approval_verdict}</span>
      </header>
      <div className="ion-route-summary-grid">
        <div><span className="ion-label">TARGET</span><strong>{model.selected_target}</strong></div>
        <div><span className="ion-label">DECISION</span><strong>{model.operator_decision}</strong></div>
        <div><span className="ion-label">MODE</span><strong>{model.execution_mode}</strong></div>
        <div><span className="ion-label">COST</span><strong>${model.estimated_cost_usd.toFixed(2)}</strong></div>
        <div><span className="ion-label">LATENCY</span><strong>{model.estimated_latency_band}</strong></div>
        <div><span className="ion-label">QUALITY</span><strong>{model.quality_band}</strong></div>
      </div>
      <div className="ion-operator-reason">
        <span className="ion-label">REQUEST</span>
        <p>{model.requested_action_summary}</p>
        <span className="ion-label">OPERATOR REASON</span>
        <p>{model.operator_reason}</p>
        <span className="ion-label">NEXT REQUIRED ACTION</span>
        <p>{model.next_required_action}</p>
      </div>
      <div className="ion-evidence-list">
        <span className="ion-label">APPROVAL EVIDENCE</span>
        {model.approval_evidence_refs.map((ref) => <code key={ref}>{ref}</code>)}
      </div>
      <footer className="ion-non-authority-footer">APPROVAL QUEUE ONLY / DRY-RUN HANDOFF ONLY / NO LIVE DISPATCH</footer>
    </section>
  );
}
