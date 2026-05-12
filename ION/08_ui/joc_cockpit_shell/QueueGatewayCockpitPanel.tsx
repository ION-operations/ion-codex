import type { IonChatgptBrowserMcpSummary, IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export function QueueGatewayCockpitPanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const summary = runtime.chatgpt_browser_mcp;
  if (!summary) {
    return (
      <section className="ion-panel ion-queue-gateway-panel">
        <div className="ion-section-title">GPT ACTIONS / BROWSER QUEUE</div>
        <div className="ion-empty-state">NO ACTION GATEWAY PROJECTION FOUND</div>
      </section>
    );
  }

  const queueRunner = asRecord(summary.codex_queue_runner);
  const agentBroker = asRecord(summary.agent_invocation_broker);
  const brokerCounts = asRecord(agentBroker.counts);
  const uploadCounts = summary.artifact_upload_status_counts ?? {};

  return (
    <section className="ion-panel ion-queue-gateway-panel">
      <div className="ion-section-title">GPT ACTIONS / BROWSER QUEUE</div>
      <div className={`ion-runtime-verdict is-${statusClass(summary)}`}>{label(summary.transport_state || summary.connector_contract_verdict)}</div>
      <p className="ion-runtime-objective">
        Typed API bridge plus browser carrier queue visibility. This panel does not process live packets, silently send prompts, or grant production authority.
      </p>

      <div className="ion-runtime-grid">
        <Metric label="carrier" value={summary.project_facing_callsign || summary.carrier_id || 'unclaimed'} />
        <Metric label="tools" value={String(summary.tool_count ?? 0)} />
        <Metric label="carrier msgs" value={String(summary.carrier_message_count ?? 0)} />
        <Metric label="codex work" value={String(summary.codex_work_request_count ?? 0)} />
        <Metric label="runner" value={label(queueRunner.status || queueRunner.verdict)} />
        <Metric label="agent broker" value={label(agentBroker.status || agentBroker.verdict)} />
      </div>

      <div className="ion-queue-gateway-strip" aria-label="Queue authority boundaries">
        <span>NO SILENT SEND</span>
        <span>OPERATOR GATES REQUIRED</span>
        <span>RECEIPTS REQUIRED</span>
        <span>PRODUCTION: {summary.production_authority ? 'TRUE' : 'FALSE'}</span>
        <span>LIVE EXEC: {summary.live_execution_authority ? 'TRUE' : 'FALSE'}</span>
      </div>

      <div className="ion-queue-tool-grid">
        <ToolGroup label="first parity" tools={summary.first_parity_tools_present} />
        <ToolGroup label="visibility" tools={summary.visibility_tools_present} />
        <ToolGroup label="agents" tools={summary.agent_invocation_tools_present} />
      </div>

      <div className="ion-runtime-grid">
        <Metric label="broker pending" value={String(brokerCounts.pending ?? 0)} />
        <Metric label="broker accepted" value={String(brokerCounts.accepted ?? 0)} />
        <Metric label="broker blocked" value={String(brokerCounts.blocked ?? 0)} />
      </div>

      <div className="ion-queue-upload-counts">
        {Object.entries(uploadCounts).map(([status, count]) => (
          <span key={status}>{status}: {count}</span>
        ))}
        {Object.keys(uploadCounts).length === 0 && <span>artifact uploads: none</span>}
      </div>

      <div className="ion-queue-file-grid">
        <FileSection title="carrier messages" files={summary.latest_carrier_messages} />
        <FileSection title="task returns" files={summary.latest_task_returns} />
        <FileSection title="agent invocations" files={summary.latest_agent_invocations} />
        <FileSection title="artifact receipts" files={summary.latest_artifact_receipts} />
        <FileSection title="decisions" files={summary.latest_decisions} />
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="ion-runtime-metric">
      <span>{label}</span>
      <b>{value}</b>
    </div>
  );
}

function ToolGroup({ label, tools = [] }: { label: string; tools?: string[] }) {
  return (
    <div className="ion-runtime-card">
      <div className="ion-runtime-card-head"><span>{label}</span><b>{tools.length}</b></div>
      <div className="ion-queue-tools">
        {tools.map((tool) => <span key={tool}>{tool}</span>)}
        {tools.length === 0 && <span>none</span>}
      </div>
    </div>
  );
}

function FileSection({ title, files = [] }: { title: string; files?: Array<Record<string, unknown>> }) {
  return (
    <div className="ion-queue-file-section">
      <div className="ion-runtime-card-head"><span>{title}</span><b>{files.length}</b></div>
      {files.slice(0, 3).map((file, index) => (
        <div className="ion-path-row" key={`${title}-${String(file.path ?? index)}`}>
          <span>{String(file.name ?? `item-${index + 1}`)}</span>
          <code>{String(file.path ?? '')}</code>
        </div>
      ))}
      {files.length === 0 && <div className="ion-empty-state">NONE RECENT</div>}
    </div>
  );
}

function asRecord(value: unknown): Record<string, unknown> {
  return value && typeof value === 'object' && !Array.isArray(value) ? value as Record<string, unknown> : {};
}

function label(value: unknown, fallback = 'unknown') {
  if (typeof value === 'string' && value.trim()) return value.trim();
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  return fallback;
}

function statusClass(summary: IonChatgptBrowserMcpSummary) {
  const status = `${summary.transport_state ?? ''} ${summary.connector_contract_verdict ?? ''} ${summary.http_preview_verdict ?? ''}`.toLowerCase();
  if (status.includes('pass') || status.includes('ready') || status.includes('active') || status.includes('connected')) return 'ready';
  if (status.includes('blocked') || status.includes('fail') || status.includes('error')) return 'blocked';
  return 'degraded';
}
