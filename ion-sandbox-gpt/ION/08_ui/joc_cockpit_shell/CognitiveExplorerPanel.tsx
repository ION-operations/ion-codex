import type { CognitiveRouteViewModel } from './reactiveTypes';

export function CognitiveExplorerPanel({ route }: { route: CognitiveRouteViewModel }) {
  return (
    <section className="ion-panel ion-cognitive-explorer" aria-label="Cognitive Explorer route proof">
      <div className="ion-panel-head">
        <span className="ion-section-title">COGNITIVE EXPLORER</span>
        <b>{route.verdict}</b>
      </div>
      <div className="ion-query-readout">{route.query}</div>
      <div className="ion-route-class-row">
        {route.routeClasses.map((routeClass) => <span key={routeClass}>{routeClass}</span>)}
      </div>
      <div className="ion-explorer-grid">
        <div className="ion-node-list" aria-label="Selected context nodes">
          <div className="ion-section-title">SELECTED CONTEXT</div>
          {route.selectedNodes.map((node) => (
            <article className="ion-node-card" key={node.nodeId}>
              <div className="ion-node-top"><span>{node.nodeClass}</span><b>{node.confidence}</b></div>
              <strong>{node.label}</strong>
              <code>{node.path}</code>
              <small>{node.symbol || 'path'} - {node.lineRange}</small>
            </article>
          ))}
        </div>
        <div className="ion-dependency-web" aria-label="Dependency web">
          <div className="ion-section-title">DEPENDENCY WEB</div>
          {route.dependencyEdges.map((edge) => (
            <article className="ion-edge-card" key={`${edge.source}-${edge.target}-${edge.edgeClass}`}>
              <span>{edge.source}</span>
              <b>{edge.edgeClass}</b>
              <span>{edge.target}</span>
              <small>{edge.evidenceRef}</small>
            </article>
          ))}
        </div>
      </div>
      <div className="ion-route-proof">
        <div>
          <div className="ion-section-title">ROUTE REASONING</div>
          <p>{route.routeReasoning}</p>
        </div>
        <div>
          <div className="ion-section-title">SOURCE LINE RAIL</div>
          <ul>{route.sourceCitations.map((citation) => <li key={citation}>{citation}</li>)}</ul>
        </div>
      </div>
    </section>
  );
}
