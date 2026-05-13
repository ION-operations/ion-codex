import type { MissionDispatchRouteViewModel } from './reactiveTypes';

export function ModelRouteMatrixPanel({ route }: { route: MissionDispatchRouteViewModel }) {
  return (
    <section className="ion-panel ion-route-matrix" aria-label="Model route matrix">
      <div className="ion-section-title">MODEL ROUTE MATRIX</div>
      <div className="ion-route-factor-grid">
        {route.routeFactors.map((factor) => (
          <article key={factor.factorId}>
            <span>{factor.factorId}</span>
            <b>{factor.value}</b>
            <p>{factor.rationale}</p>
          </article>
        ))}
      </div>
      <div className="ion-section-title">BLOCKED DISPATCH CAPABILITIES</div>
      <div className="ion-blocked-list">{route.blockedCapabilities.map((cap) => <span key={cap}>{cap}</span>)}</div>
    </section>
  );
}
