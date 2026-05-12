import { useState } from 'react';
import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

type TabId = 'favorites' | 'context' | 'packages' | 'custom';

const tabs: Array<{ id: TabId; label: string }> = [
  { id: 'favorites', label: 'favorites' },
  { id: 'context', label: 'context packs' },
  { id: 'packages', label: 'package zips' },
  { id: 'custom', label: 'custom gpt' },
];

export function DocsProjectsPackagesPanel({ runtime }: { runtime: IonCockpitViewModel }) {
  const [activeTab, setActiveTab] = useState<TabId>('favorites');
  const docs = runtime.docs_projects_packages;

  if (!docs) {
    return (
      <section className="ion-panel ion-docs-projects-panel">
        <div className="ion-section-title">DOCS / PROJECTS / PACKAGES</div>
        <div className="ion-empty-state">NO DOCS / PROJECTS PACKAGE PROJECTION FOUND</div>
      </section>
    );
  }

  const context = docs.context_packages ?? {};
  const artifacts = docs.artifact_packages ?? {};
  const safePackage = docs.safe_full_project_package ?? {};
  const custom = docs.custom_gpt_context ?? {};

  return (
    <section className="ion-panel ion-docs-projects-panel">
      <div className="ion-section-title">DOCS / PROJECTS / PACKAGES</div>
      <div className={`ion-runtime-verdict is-${statusClass(docs.status)}`}>{text(docs.status)}</div>
      <p className="ion-runtime-objective">
        Operator-facing index for local project favorites, Codex context packages, candidate package ZIPs, safe project packages, and Custom GPT build material.
      </p>

      <div className="ion-runtime-grid">
        <Metric label="context packs" value={String(context.package_count ?? 0)} />
        <Metric label="default packs" value={String((context.selected_by_default ?? []).length)} />
        <Metric label="favorites" value={String((docs.project_favorites ?? []).length)} />
        <Metric label="visible zips" value={String(artifacts.zip_count_visible ?? 0)} />
        <Metric label="safe package" value={safePackage.present ? text(safePackage.accepted) : 'missing'} />
        <Metric label="drop authority" value={artifacts.drop_zone_execution_authority ? 'true' : 'false'} />
      </div>

      <div className="ion-codex-chat-tabs" role="tablist" aria-label="Docs projects packages tabs">
        {tabs.map((tab) => (
          <button key={tab.id} className={activeTab === tab.id ? 'is-active' : undefined} onClick={() => setActiveTab(tab.id)} type="button">
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'favorites' && (
        <div className="ion-codex-tab-body ion-docs-favorite-grid">
          {(docs.project_favorites ?? []).map((favorite) => (
            <article className={`ion-docs-favorite-card is-${favorite.exists ? 'ready' : 'missing'}`} key={text(favorite.project_id)}>
              <div className="ion-runtime-card-head"><span>{text(favorite.kind)}</span><b>{text(favorite.label)}</b></div>
              <p>{text(favorite.context_authority)}</p>
              <code>{text(favorite.path)}</code>
            </article>
          ))}
        </div>
      )}

      {activeTab === 'context' && (
        <div className="ion-codex-tab-body">
          <div className="ion-docs-context-type-row">
            {Object.entries(context.package_types ?? {}).map(([kind, count]) => <span key={kind}>{kind}: {count}</span>)}
          </div>
          <RecordList title="context packages" records={context.packages} primary="package_id" secondary="context_type" />
          <PathRow label="selector" value={context.path} />
        </div>
      )}

      {activeTab === 'packages' && (
        <div className="ion-codex-tab-body">
          <div className="ion-queue-gateway-strip">
            <span>AUTO ZIP DROP: {artifacts.auto_zip_drop_authority ? 'TRUE' : 'FALSE'}</span>
            <span>DROP EXEC: {artifacts.drop_zone_execution_authority ? 'TRUE' : 'FALSE'}</span>
            <span>PRODUCTION: {docs.production_authority ? 'TRUE' : 'FALSE'}</span>
            <span>LIVE EXEC: {docs.live_execution_authority ? 'TRUE' : 'FALSE'}</span>
            <span>RECEIPTS REQUIRED</span>
          </div>
          <RecordList title="latest package zips" records={artifacts.latest_zips} primary="name" secondary="bytes" />
          <div className="ion-runtime-card">
            <div className="ion-runtime-card-head"><span>safe full project package</span><b>{text(safePackage.packaging_verdict || safePackage.zip_root_verdict)}</b></div>
            <PathRow label="result" value={safePackage.path} />
            <PathRow label="zip" value={safePackage.zip_path} />
            <PathRow label="sha256" value={safePackage.zip_sha256} />
          </div>
        </div>
      )}

      {activeTab === 'custom' && (
        <div className="ion-codex-tab-body ion-queue-file-grid">
          <RecordList title="build drafts" records={asRecords(custom.latest_build_drafts)} primary="name" secondary="suffix" />
          <RecordList title="factory files" records={asRecords(custom.latest_factory_files)} primary="name" secondary="suffix" />
          <PathRow label="capsule system" value={custom.capsule_system_dir} />
          <PathRow label="factory" value={custom.factory_dir} />
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

function RecordList({ title, records = [], primary = 'name', secondary = 'status' }: { title: string; records?: Array<Record<string, unknown>>; primary?: string; secondary?: string }) {
  return (
    <div className="ion-runtime-card">
      <div className="ion-runtime-card-head"><span>{title}</span><b>{records.length}</b></div>
      {records.map((record, index) => (
        <div className="ion-codex-record" key={`${title}-${String(record.path ?? record[primary] ?? index)}`}>
          <b>{text(record[primary], `item-${index + 1}`)}</b>
          <span>{text(record[secondary] ?? record.load_policy ?? record.mtime)}</span>
          <code>{text(record.path ?? record.path_refs, '')}</code>
        </div>
      ))}
      {records.length === 0 && <div className="ion-empty-state">NONE FOUND</div>}
    </div>
  );
}

function asRecords(value: unknown): Array<Record<string, unknown>> {
  return Array.isArray(value) ? value.filter((item): item is Record<string, unknown> => Boolean(item) && typeof item === 'object' && !Array.isArray(item)) : [];
}

function text(value: unknown, fallback = 'unknown') {
  if (Array.isArray(value)) return value.map((item) => text(item)).join(', ');
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
