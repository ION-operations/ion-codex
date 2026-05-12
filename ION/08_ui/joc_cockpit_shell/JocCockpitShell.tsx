import './joc-cockpit.css';
import './dispatch-authorization.css';
import './operator-approval.css';
import './ion-runtime-cockpit.css';
import { useEffect, useState, type ReactNode } from 'react';
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
import { ServiceConsolePanel } from './ServiceConsolePanel';
import { HelixionEvolutionPanel } from './HelixionEvolutionPanel';
import { HelixionDevelopmentPanel } from './HelixionDevelopmentPanel';
import { QueueGatewayCockpitPanel } from './QueueGatewayCockpitPanel';
import { CodexCapsuleChatWorkbenchPanel } from './CodexCapsuleChatWorkbenchPanel';
import { ExtensionMicroShellPanel } from './ExtensionMicroShellPanel';
import { DocsProjectsPackagesPanel } from './DocsProjectsPackagesPanel';
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
  onRuntimeRefresh?: () => void;
};

const modes = [
  ['run', WorkSurfaceIcon],
  ['agents', RouteIcon],
  ['context', GraphIcon],
  ['gates', LensIcon],
  ['receipts', ReceiptIcon],
  ['stream', StreamIcon],
] as const;

type LivePageId = 'mission' | 'queue' | 'codex' | 'extension' | 'docs' | 'gates' | 'receipts';
type LiveDrawerId = 'receipts' | 'context' | 'debug' | 'timeline';

const liveTopNav: Array<{ id: LivePageId; label: string; title: string; summary: string }> = [
  { id: 'mission', label: 'RUN', title: 'Mission Control', summary: 'Runtime health, service console, rebuild state, and local development route status.' },
  { id: 'queue', label: 'QUEUE', title: 'Queue Gateway', summary: 'GPT Actions bridge, browser carrier queue, packet files, and queue authority boundaries.' },
  { id: 'codex', label: 'CODEX', title: 'Codex Workbench', summary: 'Capsule Chat, response runs, worker handoffs, spawn queue, and task-return ledger.' },
  { id: 'extension', label: 'EXT', title: 'Extension Micro-Shell', summary: 'Portable dAimon companion, browser extension contract, DOM perception, and page safety law.' },
  { id: 'docs', label: 'DOCS/PKG', title: 'Docs / Projects / Packages', summary: 'Project favorites, context packages, candidate zips, safe package state, and Custom GPT materials.' },
  { id: 'gates', label: 'GATES', title: 'Gates and Approvals', summary: 'Human gates, operator queue, steward queue, and blocked runtime state.' },
  { id: 'receipts', label: 'RECEIPTS', title: 'Receipts and Proof', summary: 'Hydrated receipts, proof trace, lane timeline, and accepted-state evidence.' },
] as const;

const liveRail: Array<[LivePageId, (typeof WorkSurfaceIcon)]> = [
  ['mission', WorkSurfaceIcon],
  ['queue', StreamIcon],
  ['codex', RouteIcon],
  ['extension', LensIcon],
  ['docs', GraphIcon],
  ['gates', LensIcon],
  ['receipts', ReceiptIcon],
] as const;

const drawerTabs: Array<{ id: LiveDrawerId; label: string }> = [
  { id: 'receipts', label: 'receipts' },
  { id: 'context', label: 'context' },
  { id: 'debug', label: 'debug' },
  { id: 'timeline', label: 'timeline' },
];

export function JocCockpitShell({ projection = v56CockpitProjectionFixture, runtimeProjection, onRuntimeRefresh }: JocCockpitShellProps) {
  if (runtimeProjection) {
    return <LiveRuntimeCockpit projection={projection} runtime={runtimeProjection} onRuntimeRefresh={onRuntimeRefresh} />;
  }
  return <FixtureCockpit projection={projection} />;
}

function LiveRuntimeCockpit({ projection, runtime, onRuntimeRefresh }: { projection: CockpitProjectionFixture; runtime: IonCockpitViewModel; onRuntimeRefresh?: () => void }) {
  const [activePage, setActivePage] = useState<LivePageId>('mission');
  const [activeDrawer, setActiveDrawer] = useState<LiveDrawerId>('receipts');
  const page = liveTopNav.find((item) => item.id === activePage) ?? liveTopNav[0];

  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (window.location.hash === '#docs-packages') {
      setActivePage('docs');
    }
  }, []);

  return (
    <main className="ion-joc-shell" data-version={runtime.runtime.version} data-mode="live-runtime">
      <header className="ion-topbar">
        <div className="ion-brand">ION/JOC LIVE</div>
        <nav className="ion-topnav" aria-label="Primary cockpit groups">
          {liveTopNav.map((item) => (
            <button className={activePage === item.id ? 'is-active' : undefined} key={item.id} onClick={() => setActivePage(item.id)} type="button">{item.label}</button>
          ))}
        </nav>
        <div className="ion-state-strip">
          <span>HOST: CARRIER-CONTROL</span>
          <span>STEWARD: QUEUED AUTHORITY</span>
          <span>ACTION QUEUE: {runtime.top_bar.browser_carrier_message_count ?? 0}/{runtime.top_bar.codex_work_request_count ?? 0}</span>
          <span>CODEX CHAT: {runtime.top_bar.codex_capsule_chat_turn_count ?? 0}/{runtime.top_bar.codex_capsule_chat_response_run_count ?? 0}</span>
          <span>EXT: {runtime.top_bar.extension_version ?? 'NA'} / DOM {runtime.top_bar.page_perception_domain_count ?? 0}</span>
          <span>PKG: {runtime.top_bar.context_package_count ?? 0}/{runtime.top_bar.artifact_package_count ?? 0}</span>
          <span className={runtime.runtime.blocked ? 'ion-runtime-top-warning' : undefined}>STATUS: {runtime.runtime.status}</span>
        </div>
      </header>

      <aside className="ion-left-rail" aria-label="Work surface regions">
        {liveRail.map(([id, Icon]) => (
          <button className={activePage === id ? 'is-active' : undefined} key={id} aria-label={id} title={id} onClick={() => setActivePage(id)} type="button">
            <Icon />
          </button>
        ))}
      </aside>

      <section className={`ion-main-work-surface ion-live-page is-${activePage}`} aria-label="Maintained work surface">
        <div className="ion-live-page-header">
          <div>
            <div className="ion-section-title">ACTIVE PAGE</div>
            <h1>{page.title}</h1>
            <p>{page.summary}</p>
          </div>
          <div className="ion-live-page-mode">PAGE / {page.label}</div>
        </div>
        <div className="ion-live-page-body">
          {renderLivePage(activePage, runtime, projection, onRuntimeRefresh)}
        </div>
      </section>

      <aside className="ion-right-inspector ion-live-drawer" aria-label="Receipt and evidence inspector">
        <div className="ion-live-drawer-tabs">
          {drawerTabs.map((tab) => (
            <button className={activeDrawer === tab.id ? 'is-active' : undefined} key={tab.id} onClick={() => setActiveDrawer(tab.id)} type="button">{tab.label}</button>
          ))}
        </div>
        {renderLiveDrawer(activeDrawer, runtime)}
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

function renderLivePage(activePage: LivePageId, runtime: IonCockpitViewModel, projection: CockpitProjectionFixture, onRuntimeRefresh?: () => void): ReactNode {
  switch (activePage) {
    case 'mission':
      return (
        <>
          <RuntimeStatusPanel runtime={runtime} />
          <ServiceConsolePanel runtime={runtime} onRuntimeRefresh={onRuntimeRefresh} />
          <HelixionEvolutionPanel runtime={runtime} />
          <HelixionDevelopmentPanel runtime={runtime} />
        </>
      );
    case 'queue':
      return (
        <>
          <QueueGatewayCockpitPanel runtime={runtime} />
          <CarrierTurnPanel runtime={runtime} />
          <OperatorMessageQueuePanel runtime={runtime} />
        </>
      );
    case 'codex':
      return (
        <>
          <CodexCapsuleChatWorkbenchPanel runtime={runtime} />
          <SpawnQueuePanel runtime={runtime} />
          <TaskReturnLedgerPanel runtime={runtime} />
        </>
      );
    case 'extension':
      return (
        <>
          <ExtensionMicroShellPanel runtime={runtime} />
          <FrontDoorProofTracePanel runtime={runtime} />
          <AutomationOverlayPanel events={projection.reactiveEvents} />
        </>
      );
    case 'docs':
      return (
        <>
          <DocsProjectsPackagesPanel runtime={runtime} />
          <ContextPackageInspectorPanel runtime={runtime} />
        </>
      );
    case 'gates':
      return (
        <>
          <HumanGateQueuePanel runtime={runtime} />
          <OperatorMessageQueuePanel runtime={runtime} />
          <StewardIntegrationQueuePanel runtime={runtime} />
        </>
      );
    case 'receipts':
      return (
        <>
          <ReceiptHydrationPanel runtime={runtime} />
          <TaskReturnLedgerPanel runtime={runtime} />
          <FrontDoorProofTracePanel runtime={runtime} />
        </>
      );
    default:
      return <RuntimeStatusPanel runtime={runtime} />;
  }
}

function renderLiveDrawer(activeDrawer: LiveDrawerId, runtime: IonCockpitViewModel): ReactNode {
  if (activeDrawer === 'context') {
    return (
      <>
        <ContextPackageInspectorPanel runtime={runtime} />
        <div className="ion-section-title">AUTHORITY CLASSES</div>
        <div className="ion-blocked-list">{runtime.authority_classes.map((cap) => <span key={cap}>{cap}</span>)}</div>
      </>
    );
  }
  if (activeDrawer === 'debug') {
    return <RuntimeDebugOverlayPanel runtime={runtime} />;
  }
  if (activeDrawer === 'timeline') {
    return <LaneTimelinePanel runtime={runtime} />;
  }
  return (
    <>
      <ReceiptHydrationPanel runtime={runtime} />
      <div className="ion-section-title">LIVE RECEIPT RAIL</div>
      {runtime.receipts.map((receipt, index) => (
        <article className="ion-receipt-card" key={`${String(receipt.path ?? index)}`}>
          <div className="ion-receipt-head"><span>{String(receipt.authority_class ?? 'RECEIPT')}</span><b>{String(receipt.name ?? 'receipt')}</b></div>
          <div className="ion-receipt-verdict">{String(receipt.path ?? '')}</div>
        </article>
      ))}
      {runtime.receipts.length === 0 && <div className="ion-empty-state">NO RECEIPTS FOUND</div>}
    </>
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
