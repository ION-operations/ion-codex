import type { DispatchAuthorizationViewModel } from './dispatchAuthorizationTypes';

function verdictClass(value: string): string {
  if (value.includes('BLOCK') || value.includes('EXCEEDED') || value.includes('FORBIDDEN')) return 'is-blocked';
  if (value.includes('SUPERVISED') || value.includes('REQUIRED')) return 'is-supervised';
  return 'is-clear';
}

export function GovernorVerdictRail({ model }: { model: DispatchAuthorizationViewModel }) {
  const rows = [
    ['BUDGET', model.budget_governor_verdict],
    ['API RATE', model.api_rate_governor_verdict],
    ['CAPABILITY', model.capability_policy_verdict],
    ['APPROVAL', model.approval_mode],
    ['AUTHORITY', model.authority_scope],
  ];

  return (
    <section className="ion-governor-rail" aria-label="Governor verdict rail">
      <header className="ion-section-header">GOVERNOR VERDICTS</header>
      <div className="ion-governor-grid">
        {rows.map(([label, value]) => (
          <div className="ion-governor-row" key={label}>
            <span className="ion-label">{label}</span>
            <span className={`ion-badge ${verdictClass(value)}`}>{value}</span>
          </div>
        ))}
      </div>
      <div className="ion-evidence-list">
        <span className="ion-label">EVIDENCE</span>
        {model.evidence_refs.map((ref) => (
          <code key={ref}>{ref}</code>
        ))}
      </div>
    </section>
  );
}
