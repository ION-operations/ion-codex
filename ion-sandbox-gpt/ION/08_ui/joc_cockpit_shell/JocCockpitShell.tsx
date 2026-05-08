import './joc-cockpit.css';
import './dispatch-authorization.css';
import './operator-approval.css';
import './ion-runtime-cockpit.css';
import { AutomationOverlayPanel } from './AutomationOverlayPanel';
import { CognitiveExplorerPanel } from './CognitiveExplorerPanel';
import { InfiniteContextCommandPalette } from './InfiniteContextCommandPalette';
import { DispatchAuthorizationPanel } from './DispatchAuthorizationPanel';
import { OperatorApprovalQueuePanel } from './OperatorApprovalQueuePanel';
import { DryRunDispatchHandoffPanel } from './DryRunDispatchHandoffPanel';
import { MissionDispatchRouterPanel } from './MissionDispatchRouterPanel';
import { ModelRouteMatrixPanel } from './ModelRouteMatrixPanel';
import { ReactiveOsStreamPanel } from './ReactiveOsStreamPanel';
import { RuntimeStatusPanel } from './RuntimeStatusPanel';
import { CarrierTurnPanel } from './CarrierTurnPanel';
import { SpawnQueuePanel } from './SpawnQueuePanel';
import { TaskReturnLedgerPanel } from './TaskReturnLedgerPanel';
import { StewardIntegrationQueuePanel } from './StewardIntegrationQueuePanel';
import { HumanGateQueuePanel } from './HumanGateQueuePanel';
import { OperatorMessageQueuePanel } from './OperatorMessageQueuePanel';
import { CursorHookStatePanel } from './CursorHookStatePanel';
import { ContextPackageInspectorPanel } from './ContextPackageInspectorPanel';
import { FrontDoorProofTracePanel } from './FrontDoorProofTracePanel';
import { LaneTimelinePanel } from './LaneTimelinePanel';
import { ReceiptHydrationPanel } from './ReceiptHydrationPanel';
import { RuntimeDebugOverlayPanel } from './RuntimeDebugOverlayPanel';
import { GraphIcon, LensIcon, ReceiptIcon, RouteIcon, StreamIcon, WorkSurfaceIcon } from './icons';
import { v56CockpitProjectionFixture, type CockpitProjectionFixture } from './projectionFixtures';
import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export type JocCockpitShellProps = {
  projection?: CockpitProjectionFixture;
  runtimeProjection?: IonCockpitViewModel;
};

const modes = [
  ['run', WorkSurfaceIcon],
  ['agents', RouteIcon],
  ['context', GraphIcon],
  ['gates', LensIcon],
  ['receipts', ReceiptIcon],
  ['stream', StreamIcon],
] as const;

export function JocCockpitShell({ projection = v56CockpitProjectionFixture, runtimeProjection }: JocCockpitShellProps) {
  if (runtimeProjection) {
    return <LiveRuntimeCockpit projection={projection} runtime={runtimeProjection} />;
  }
  return <FixtureCockpit projection={projection} />;
}

function LiveRuntimeCockpit({ projection, runtime }: { projection: CockpitProjectionFixture; runtime: IonCockpitViewModel }) {
  return (
    <main className="ion-joc-shell" data-version={runtime.runtime.version} data-mode="live-runtime">
      <header className="ion-topbar">
        <div className="ion-brand">ION/JOC LIVE</div>
        <nav className="ion-topnav" aria-label="Primary cockpit groups">
          <button>RUN</button>
          <button>AGENTS</button>
          <button>QUEUES</button>
          <button>GATES</button>
          <button>RECEIPTS</button>
        </nav>
        <div className="ion-state-strip">
          <span>HOST: CARRIER-CONTROL</span>
          <span>STEWARD: QUEUED AUTHORITY</span>
          <span className={runtime.runtime.blocked ? 'ion-runtime-top-warning' : undefined}>STATUS: {runtime.runtime.status}</span>
        </div>
      </header>

      <aside className="ion-left-rail" aria-label="Work surface regions">
        {modes.map(([label, Icon]) => (
          <button key={label} aria-label={label} title={label}>
            <Icon />
          </button>
        ))}
      </aside>

      <section className="ion-main-work-surface" aria-label="Maintained work surface">
        <RuntimeStatusPanel runtime={runtime} />
        <CarrierTurnPanel runtime={runtime} />
        <SpawnQueuePanel runtime={runtime} />
        <TaskReturnLedgerPanel runtime={runtime} />
        <StewardIntegrationQueuePanel runtime={runtime} />
        <HumanGateQueuePanel runtime={runtime} />
        <OperatorMessageQueuePanel runtime={runtime} />
        <CursorHookStatePanel runtime={runtime} />
        <ContextPackageInspectorPanel runtime={runtime} />
        <FrontDoorProofTracePanel runtime={runtime} />
        <LaneTimelinePanel runtime={runtime} />
        <RuntimeDebugOverlayPanel runtime={runtime} />
        <AutomationOverlayPanel events={projection.reactiveEvents} />
      </section>

      <aside className="ion-right-inspector" aria-label="Receipt and evidence inspector">
        <ReceiptHydrationPanel runtime={runtime} />
        <div className="ion-section-title">LIVE RECEIPT RAIL</div>
        {runtime.receipts.map((receipt, index) => (
          <article className="ion-receipt-card" key={`${String(receipt.path ?? index)}`}>
            <div className="ion-receipt-head"><span>{String(receipt.authority_class ?? 'RECEIPT')}</span><b>{String(receipt.name ?? 'receipt')}</b></div>
            <div className="ion-receipt-verdict">{String(receipt.path ?? '')}</div>
          </article>
        ))}
        {runtime.receipts.length === 0 && <div className="ion-empty-state">NO RECEIPTS FOUND</div>}
        <div className="ion-section-title">AUTHORITY CLASSES</div>
        <div className="ion-blocked-list">{runtime.authority_classes.map((cap) => <span key={cap}>{cap}</span>)}</div>
      </aside>

      <footer className="ion-bottom-timeline" aria-label="Reactive OS stream">
        <span className="ion-section-title">LIVE RUNTIME STREAM</span>
        <div className="ion-stream-stack">
          {runtime.timeline.map((event, index) => (
            <article className={`ion-stream-event is-${event.status}`} key={`${event.source}-${index}`}>
              <div className="ion-stream-event-head"><span>{event.source}</span><span>{event.event_type}</span><b>{event.status}</b></div>
              <p>{event.detail || event.path}</p>
            </article>
          ))}
        </div>
      </footer>
    </main>
  );
}

function FixtureCockpit({ projection }: { projection: CockpitProjectionFixture }) {
  return (
    <main className="ion-joc-shell" data-version={projection.version}>
      <header className="ion-topbar">
        <div className="ion-brand">ION/JOC</div>
        <nav className="ion-topnav" aria-label="Primary cockpit groups">
          <button>OPERATIONS</button>
          <button>INTELLIGENCE</button>
          <button>INFRASTRUCTURE</button>
          <button>TOOLS</button>
        </nav>
        <div className="ion-state-strip">
          <span>STEWARD: {projection.stewardState}</span>
          <span>ORACLE: {projection.oracleMode}</span>
          <span>MISSION: {projection.missionRoute.verdict}</span>
        </div>
      </header>

      <aside className="ion-left-rail" aria-label="Work surface regions">
        {modes.map(([label, Icon]) => (
          <button key={label} aria-label={label} title={label}>
            <Icon />
          </button>
        ))}
      </aside>

      <section className="ion-main-work-surface" aria-label="Maintained work surface">
        <div className="ion-panel ion-hero-panel">
          <div className="ion-section-title">ACTIVE SURFACE</div>
          <h1>{projection.activeSurface}</h1>
          <div className="ion-verdict-band">{projection.missionRoute.verdict}</div>
          <div className="ion-grid-3">
            <Metric label="visual lineage" value="V44/V45/V48/V53/V54" />
            <Metric label="ui route" value="V55/V56/V57/V58/V59" />
            <Metric label="authority" value="preview only" />
          </div>
        </div>

        <InfiniteContextCommandPalette route={projection.cognitiveRoute} />
        <CognitiveExplorerPanel route={projection.cognitiveRoute} />
        <MissionDispatchRouterPanel route={projection.missionRoute} />
        <ModelRouteMatrixPanel route={projection.missionRoute} />
        <DispatchAuthorizationPanel />
        <OperatorApprovalQueuePanel />
        <DryRunDispatchHandoffPanel />

        <div className="ion-panel ion-visual-lens">
          <div className="ion-section-title">VISUAL EVIDENCE LENS</div>
          <div className="ion-evidence-chain">
            <span>OBSERVE</span><span>DIAGNOSE</span><span>VERIFY</span><span>RUN</span><span>BIND</span><span>ROUTE</span><span>DISPATCH PREVIEW</span>
          </div>
          <p>Closure, context routes, and mission routes may be displayed only as scoped evidence. Production automation, paid cloud launch, and unrestricted browser control remain blocked.</p>
        </div>

        <AutomationOverlayPanel events={projection.reactiveEvents} />
      </section>

      <aside className="ion-right-inspector" aria-label="Receipt and evidence inspector">
        <div className="ion-section-title">RECEIPT RAIL</div>
        {projection.receiptSummaries.map((receipt) => (
          <article className="ion-receipt-card" key={receipt.id}>
            <div className="ion-receipt-head"><span>{receipt.family}</span><b>{receipt.claimLane}</b></div>
            <div className="ion-receipt-verdict">{receipt.verdict}</div>
            <div className="ion-receipt-scope">{receipt.authorityScope}</div>
            <ul>{receipt.evidenceRefs.map((ref) => <li key={ref}>{ref}</li>)}</ul>
          </article>
        ))}
        <div className="ion-section-title">BLOCKED CAPABILITIES</div>
        <div className="ion-blocked-list">{projection.blockedCapabilities.map((cap) => <span key={cap}>{cap}</span>)}</div>
      </aside>

      <footer className="ion-bottom-timeline" aria-label="Reactive OS stream">
        <span className="ion-section-title">REACTIVE OS STREAM</span>
        <ReactiveOsStreamPanel events={projection.reactiveEvents} />
      </footer>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="ion-metric"><span>{label}</span><b>{value}</b></div>;
}
