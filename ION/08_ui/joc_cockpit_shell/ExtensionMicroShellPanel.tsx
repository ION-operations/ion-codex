import { useState } from 'react';
import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

type TabId = 'companion' | 'extension' | 'perception' | 'authority';

const tabs: Array<{ id: TabId; label: string }> = [
  { id: 'companion', label: 'companion' },
  { id: 'extension', label: 'extension' },
  { id: 'perception', label: 'perception' },
  { id: 'authority', label: 'authority' },
];

export function ExtensionMicroShellPanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const [activeTab, setActiveTab] = useState<TabId>('companion');
  const shell = runtime.extension_micro_shell;

  if (!shell) {
    return (
      <section className="ion-panel ion-extension-shell-panel">
        <div className="ion-section-title">DAIMON EXTENSION MICRO-SHELL</div>
        <div className="ion-empty-state">NO EXTENSION MICRO-SHELL PROJECTION FOUND</div>
      </section>
    );
  }

  const manifest = shell.manifest ?? {};
  const contract = shell.agent_lane_contract ?? {};
  const companion = shell.portable_companion ?? {};
  const perception = shell.page_perception ?? {};
  const authority = shell.current_v1_authority ?? {};

  return (
    <section className="ion-panel ion-extension-shell-panel">
      <div className="ion-section-title">DAIMON EXTENSION MICRO-SHELL</div>
      <div className={`ion-runtime-verdict is-${statusClass(shell.status)}`}>{text(shell.status)}</div>
      <p className="ion-runtime-objective">
        Portable page companion, browser extension bridge, DOM perception, queue packs, and bounded agent lane projected as one JOC surface.
      </p>

      <div className="ion-runtime-grid">
        <Metric label="extension" value={`${text(manifest.name)} ${text(manifest.version, '')}`} />
        <Metric label="agent panels" value={String((contract.panel_surfaces as unknown[] | undefined)?.length ?? 0)} />
        <Metric label="bg messages" value={String(contract.background_message_count ?? 0)} />
        <Metric label="perception domains" value={String(perception.domain_count ?? 0)} />
        <Metric label="content scripts" value={String(manifest.content_script_count ?? 0)} />
        <Metric label="joc decision" value={text(companion.joc_decision)} />
      </div>

      <div className="ion-codex-chat-tabs" role="tablist" aria-label="Extension micro-shell tabs">
        {tabs.map((tab) => (
          <button key={tab.id} className={activeTab === tab.id ? 'is-active' : undefined} onClick={() => setActiveTab(tab.id)} type="button">
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'companion' && (
        <div className="ion-codex-tab-body">
          <div className="ion-runtime-card">
            <div className="ion-runtime-card-head"><span>portable thesis</span><b>{text(companion.status)}</b></div>
            <p>{text(companion.product_thesis)}</p>
          </div>
          <ChipBlock title="layout zones" items={asList(companion.layout_zones)} />
          <ChipBlock title="inherited protocols" items={asList(companion.inherited_protocols)} />
          <PathRow label="context" value={companion.path} />
          <PathRow label="extension root" value={shell.extension_root} />
        </div>
      )}

      {activeTab === 'extension' && (
        <div className="ion-codex-tab-body">
          <div className="ion-runtime-card">
            <div className="ion-runtime-card-head"><span>agent lane contract</span><b>{text(contract.status)}</b></div>
            <p>{text(contract.purpose)}</p>
          </div>
          <ChipBlock title="panel surfaces" items={asList(contract.panel_surfaces)} />
          <ChipBlock title="background messages" items={asList(contract.background_messages)} />
          <ChipBlock title="host permissions" items={asList(manifest.host_permissions)} />
          <ChipBlock title="content matches" items={asList(manifest.content_script_matches)} />
          <PathRow label="manifest" value={manifest.path} />
          <PathRow label="contract" value={contract.path} />
        </div>
      )}

      {activeTab === 'perception' && (
        <div className="ion-codex-tab-body">
          <div className="ion-extension-domain-grid">
            {asRecords(perception.domains).map((domain, index) => (
              <article className="ion-runtime-card" key={text(domain.domain_id, `domain-${index + 1}`)}>
                <div className="ion-runtime-card-head"><span>{text(domain.domain_id)}</span><b>DOM</b></div>
                <p>{text(domain.purpose)}</p>
                <code>{text(domain.safety_boundary)}</code>
              </article>
            ))}
          </div>
          <ChipBlock title="task return headings" items={asList(perception.task_return_headings)} />
          <PathRow label="domain registry" value={perception.domain_registry_path} />
          <PathRow label="task return" value={perception.task_return_path} />
        </div>
      )}

      {activeTab === 'authority' && (
        <div className="ion-codex-tab-body">
          <div className="ion-queue-gateway-strip">
            <span>PRODUCTION: {shell.production_authority ? 'TRUE' : 'FALSE'}</span>
            <span>LIVE EXEC: {shell.live_execution_authority ? 'TRUE' : 'FALSE'}</span>
            <span>BROWSER CONTROL: {shell.unrestricted_browser_control ? 'TRUE' : 'FALSE'}</span>
            <span>SILENT SEND: {shell.silent_browser_send_authority ? 'TRUE' : 'FALSE'}</span>
            <span>VISIBLE GATES</span>
          </div>
          <AuthorityGrid authority={authority} />
          <ChipBlock title="safety law" items={shell.safety_law ?? []} />
          <ChipBlock title="required boundaries" items={shell.required_boundaries ?? []} />
          <ChipBlock title="non-claim boundaries" items={shell.non_claim_boundaries ?? []} />
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

function ChipBlock({ title, items }: { title: string; items: unknown[] }) {
  return (
    <div className="ion-runtime-card">
      <div className="ion-runtime-card-head"><span>{title}</span><b>{items.length}</b></div>
      <div className="ion-extension-chip-row">
        {items.map((item, index) => <span key={`${title}-${index}`}>{text(item)}</span>)}
        {items.length === 0 && <span>none</span>}
      </div>
    </div>
  );
}

function AuthorityGrid({ authority }: { authority: Record<string, unknown> }) {
  const entries = Object.entries(authority);
  return (
    <div className="ion-extension-authority-grid">
      {entries.map(([key, value]) => (
        <div className={`ion-runtime-metric is-${String(value).toLowerCase()}`} key={key}>
          <span>{key}</span>
          <b>{text(value)}</b>
        </div>
      ))}
      {entries.length === 0 && <div className="ion-empty-state">NO AUTHORITY MAP</div>}
    </div>
  );
}

function asList(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

function asRecords(value: unknown): Array<Record<string, unknown>> {
  return Array.isArray(value) ? value.filter((item): item is Record<string, unknown> => Boolean(item) && typeof item === 'object' && !Array.isArray(item)) : [];
}

function text(value: unknown, fallback = 'unknown') {
  if (typeof value === 'string' && value.trim()) return value.trim();
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  return fallback;
}

function statusClass(value: unknown) {
  const normalized = text(value, '').toLowerCase();
  if (normalized.includes('ready') || normalized.includes('active') || normalized.includes('pass')) return 'ready';
  if (normalized.includes('missing') || normalized.includes('blocked') || normalized.includes('fail')) return 'blocked';
  return 'degraded';
}
