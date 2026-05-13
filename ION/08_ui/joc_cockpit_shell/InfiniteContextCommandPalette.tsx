import type { CognitiveRouteViewModel } from './reactiveTypes';

export function InfiniteContextCommandPalette({ route }: { route: CognitiveRouteViewModel }) {
  return (
    <section className="ion-panel ion-command-palette" aria-label="Infinite context command palette preview">
      <div className="ion-panel-head">
        <span className="ion-section-title">INFINITE CONTEXT COMMAND PALETTE</span>
        <b>PREVIEW ONLY</b>
      </div>
      <div className="ion-command-input" aria-label="Command input preview">
        <span>CMD+K</span>
        <code>&gt; {route.query}</code>
      </div>
      <div className="ion-injection-preview">
        <div className="ion-section-title">INJECTION PREVIEW</div>
        <p>{route.injectionPreview}</p>
      </div>
      <div className="ion-blocked-list">
        {route.blockedCapabilities.map((capability) => <span key={capability}>{capability}</span>)}
      </div>
    </section>
  );
}
