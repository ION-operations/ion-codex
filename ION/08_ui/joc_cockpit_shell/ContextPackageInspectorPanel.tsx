import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export function ContextPackageInspectorPanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const packages = runtime.agents.context_packages ?? [];
  return (
    <section className="ion-panel ion-context-package-panel">
      <div className="ion-section-title">CONTEXT PACKAGE INSPECTOR</div>
      {packages.map((pkg, index) => (
        <article className="ion-runtime-card" key={index}>
          <div className="ion-runtime-card-head"><b>{String(pkg.role ?? 'ROLE')}</b><span>{String(pkg.authority_class ?? 'ACTIVE')}</span></div>
          <code>{String(pkg.path ?? '')}</code>
          {pkg.receipt_path && <code>{String(pkg.receipt_path)}</code>}
        </article>
      ))}
      {packages.length === 0 && <div className="ion-empty-state">NO CONTEXT PACKAGES</div>}
    </section>
  );
}
