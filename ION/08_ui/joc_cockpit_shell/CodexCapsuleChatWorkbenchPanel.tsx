import { useState } from 'react';
import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

type TabId = 'overview' | 'context' | 'runs' | 'queue' | 'skills';

const tabs: Array<{ id: TabId; label: string }> = [
  { id: 'overview', label: 'overview' },
  { id: 'context', label: 'capsule / mini' },
  { id: 'runs', label: 'runs' },
  { id: 'queue', label: 'queue' },
  { id: 'skills', label: 'skills' },
];

export function CodexCapsuleChatWorkbenchPanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const [activeTab, setActiveTab] = useState<TabId>('overview');
  const chat = runtime.codex_capsule_chat;

  if (!chat) {
    return (
      <section className="ion-panel ion-codex-chat-workbench-panel">
        <div className="ion-section-title">CODEX CAPSULE CHAT WORKBENCH</div>
        <div className="ion-empty-state">NO CODEX CAPSULE CHAT MODEL FOUND</div>
      </section>
    );
  }

  const summary = chat.conversation_summary ?? {};
  const memory = chat.memory_visualization ?? {};
  const carrier = chat.response_carrier ?? {};
  const bridge = chat.execution_bridge ?? {};

  return (
    <section className="ion-panel ion-codex-chat-workbench-panel">
      <div className="ion-section-title">CODEX CAPSULE CHAT WORKBENCH</div>
      <div className={`ion-runtime-verdict is-${verdictClass(chat.verdict)}`}>{text(chat.verdict)}</div>
      <p className="ion-runtime-objective">
        Local chat workbench view over Capsule/Mini, traces, response runs, queue handoffs, and skill activation. Hidden reasoning remains hidden; accepted state still requires receipts.
      </p>

      <div className="ion-runtime-grid">
        <Metric label="turns" value={String(summary.turn_count ?? 0)} />
        <Metric label="assistant" value={String(summary.assistant_turn_count ?? 0)} />
        <Metric label="capsule rows" value={String(chat.capsule?.entry_count ?? 0)} />
        <Metric label="response runs" value={String(chat.response_run_count ?? 0)} />
        <Metric label="queued req" value={String(chat.queued_request_count ?? 0)} />
        <Metric label="runner" value={chat.runner_active ? 'active' : 'idle'} />
      </div>

      <div className="ion-codex-chat-tabs" role="tablist" aria-label="Codex Capsule Chat workbench tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={activeTab === tab.id ? 'is-active' : undefined}
            onClick={() => setActiveTab(tab.id)}
            type="button"
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'overview' && (
        <div className="ion-codex-tab-body">
          <div className="ion-runtime-grid">
            <Metric label="model" value={text(carrier.verdict || chat.chat_engine?.verdict)} />
            <Metric label="codex cli" value={carrier.uses_codex_cli ? 'yes' : 'no'} />
            <Metric label="dispatch auth" value={carrier.provider_api_dispatch_authorized ? 'true' : 'false'} />
            <Metric label="state accept" value={carrier.state_acceptance_granted ? 'true' : 'false'} />
            <Metric label="bridge mode" value={text(bridge.default_mode)} />
            <Metric label="chat quality" value={text(chat.chat_engine?.quality_target)} />
          </div>
          <div className="ion-queue-gateway-strip">
            <span>PRODUCTION: {chat.production_authority ? 'TRUE' : 'FALSE'}</span>
            <span>LIVE EXEC: {chat.live_execution_authority ? 'TRUE' : 'FALSE'}</span>
            <span>SECRETS: {chat.secrets_authority ? 'TRUE' : 'FALSE'}</span>
            <span>RAW REASONING: {memory.raw_hidden_reasoning_exposed ? 'EXPOSED' : 'HIDDEN'}</span>
            <span>RECEIPTS REQUIRED</span>
          </div>
          <PathRow label="model" value={chat.model_path} />
          <PathRow label="queue" value={chat.codex_queue_path} />
        </div>
      )}

      {activeTab === 'context' && (
        <div className="ion-codex-tab-body">
          <div className="ion-runtime-grid">
            <Metric label="mini lines" value={`${chat.mini?.line_count ?? 0}/${chat.mini?.max_lines ?? 0}`} />
            <Metric label="hot bytes" value={String(chat.hot_context?.bytes ?? 0)} />
            <Metric label="memory segs" value={String(memory.memory_segment_count ?? 0)} />
            <Metric label="context layers" value={String(memory.context_layer_count ?? 0)} />
            <Metric label="visible windows" value={String(memory.visible_window_count ?? 0)} />
            <Metric label="selected turn" value={text(memory.selected_turn_id)} />
          </div>
          <PathRow label="capsule" value={chat.capsule?.path} />
          <PathRow label="hot" value={chat.hot_context?.path} />
          <pre className="ion-codex-mini-excerpt">{chat.mini?.text_excerpt || 'Mini excerpt unavailable.'}</pre>
          <RecordList title="recent capsule receipts" records={chat.capsule?.recent_rows} />
        </div>
      )}

      {activeTab === 'runs' && (
        <div className="ion-codex-tab-body">
          <RecordList title="latest response runs" records={chat.latest_response_runs} />
        </div>
      )}

      {activeTab === 'queue' && (
        <div className="ion-codex-tab-body ion-queue-file-grid">
          <RecordList title="work requests" records={chat.latest_work_requests} />
          <RecordList title="task returns" records={chat.latest_task_returns} />
        </div>
      )}

      {activeTab === 'skills' && (
        <div className="ion-codex-tab-body">
          <div className="ion-runtime-grid">
            <Metric label="skills" value={String(chat.skills?.skill_count ?? 0)} />
            <Metric label="verdict" value={text(chat.skills?.verdict)} />
            <Metric label="activation" value={text(chat.skills?.current_activation_verdict)} />
          </div>
          <div className="ion-runtime-card">
            <div className="ion-runtime-card-head"><span>selection</span><b>{text(chat.skills?.selection_reason)}</b></div>
            <p>{formatList(chat.skills?.findings, 'no findings')}</p>
          </div>
        </div>
      )}
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

function PathRow({ label, value }: { label: string; value: unknown }) {
  return (
    <div className="ion-path-row">
      <span>{label}</span>
      <code>{text(value, '')}</code>
    </div>
  );
}

function RecordList({ title, records = [] }: { title: string; records?: Array<Record<string, unknown>> }) {
  return (
    <div className="ion-runtime-card">
      <div className="ion-runtime-card-head"><span>{title}</span><b>{records.length}</b></div>
      {records.map((record, index) => (
        <div className="ion-codex-record" key={`${title}-${String(record.path ?? record.id ?? record.run_id ?? index)}`}>
          <b>{text(record.id || record.run_id || record.name || record.status, `item-${index + 1}`)}</b>
          <span>{text(record.status || record.decision || record.selected_model || record.created_at || record.mtime)}</span>
          <code>{text(record.path || record.latest_return_path || record.evidence, '')}</code>
          {record.summary ? <p>{text(record.summary)}</p> : null}
        </div>
      ))}
      {records.length === 0 && <div className="ion-empty-state">NONE RECENT</div>}
    </div>
  );
}

function text(value: unknown, fallback = 'unknown') {
  if (typeof value === 'string' && value.trim()) return value.trim();
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  return fallback;
}

function formatList(value: unknown, fallback: string) {
  return Array.isArray(value) && value.length ? value.map((item) => text(item)).join(' | ') : fallback;
}

function verdictClass(value: unknown) {
  const normalized = text(value, '').toLowerCase();
  if (normalized.includes('ready') || normalized.includes('pass') || normalized.includes('ok')) return 'ready';
  if (normalized.includes('blocked') || normalized.includes('fail') || normalized.includes('error')) return 'blocked';
  return 'degraded';
}
