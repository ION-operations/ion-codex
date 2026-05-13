import type { MissionDispatchRouteViewModel, MissionRouteTarget } from './reactiveTypes';

export function MissionDispatchRouterPanel({ route }: { route: MissionDispatchRouteViewModel }) {
  const targets = [route.primaryTarget, ...route.fallbackTargets];
  return (
    <section className="ion-panel ion-mission-router" aria-label="Mission dispatch route preview">
      <div className="ion-section-title">MISSION DISPATCH ROUTER</div>
      <div className="ion-route-head">
        <div>
          <h2>{route.missionId}</h2>
          <p>{route.missionTitle}</p>
        </div>
        <span className="ion-verdict-chip">{route.verdict}</span>
      </div>
      <div className="ion-grid-3 ion-route-bands">
        <Metric label="approval" value={route.approvalGate} />
        <Metric label="task" value={route.taskClass} />
        <Metric label="authority" value={route.authorityScope} />
      </div>
      <div className="ion-ring-lanes">
        {targets.map((target) => <TargetCard key={target.targetId} target={target} primary={target.targetId === route.primaryTarget.targetId} />)}
      </div>
      <div className="ion-route-reasoning">
        <div className="ion-section-title">ROUTE REASONING</div>
        <p>{route.routeReasoning}</p>
      </div>
      <div className="ion-receipt-preview">
        <div className="ion-section-title">DISPATCH RECEIPT PREVIEW</div>
        <p>{route.dispatchReceiptPreview}</p>
      </div>
    </section>
  );
}

function TargetCard({ target, primary }: { target: MissionRouteTarget; primary: boolean }) {
  return (
    <article className={primary ? 'ion-target-card ion-target-primary' : 'ion-target-card'}>
      <div className="ion-target-top"><span>{target.computeRing}</span><b>{target.status}</b></div>
      <h3>{target.displayName}</h3>
      <div className="ion-target-meta">
        <span>{target.accessMethod}</span>
        <span>{target.costBand}</span>
        <span>{target.latencyBand}</span>
        <span>{target.qualityBand}</span>
      </div>
      <div className="ion-tag-row">{target.capabilityTags.map((tag) => <span key={tag}>{tag}</span>)}</div>
      {target.riskNotes.length > 0 && <p className="ion-risk-note">{target.riskNotes.join(' - ')}</p>}
    </article>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="ion-metric"><span>{label}</span><b>{value}</b></div>;
}
