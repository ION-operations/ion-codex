import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export function openCockpitWebview(context: vscode.ExtensionContext, root: string) {
  const panel = vscode.window.createWebviewPanel(
    'ionJocCockpit',
    'ION/JOC Cockpit',
    vscode.ViewColumn.One,
    { enableScripts: true, retainContextWhenHidden: true }
  );
  const modelPath = path.join(root, 'ION', '05_context', 'current', 'ACTIVE_COCKPIT_VIEW_MODEL.json');
  let model: any = {};
  try { model = JSON.parse(fs.readFileSync(modelPath, 'utf8')); } catch (error) { model = { schema_id: 'missing', error: String(error) }; }
  panel.webview.html = renderCockpitHtml(model, modelPath);
}

function escapeHtml(value: string): string {
  return value.replace(/[&<>'"]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '\'': '&#39;', '"': '&quot;' }[ch] ?? ch));
}

function renderCockpitHtml(model: any, modelPath: string): string {
  const top = model.top_bar ?? {};
  const runtime = model.runtime ?? {};
  const agents = model.agents ?? { spawn_rows: [], returns: [] };
  const queues = model.queues ?? { human_gates: [], operator_messages: [], steward_integration: [] };
  const localServices = model.local_services ?? { services: [] };
  const serviceRows = localServices.services ?? [];
  const timeline = model.timeline ?? [];
  const receipts = model.receipts ?? [];
  const row = (label: string, value: unknown) => `<div class="kv"><span>${escapeHtml(label)}</span><b>${escapeHtml(String(value ?? ''))}</b></div>`;
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
<style>
:root{--bg:#0a0a0a;--surface:#0f0f0f;--panel:#121212;--border:#252525;--text:#d0d0d0;--muted:#777;--ok:#33cc66;--warn:#cc9900;--bad:#cc3333;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}body{margin:0;background:var(--bg);color:var(--text)}main{display:grid;grid-template-columns:1fr 360px;grid-template-rows:42px 1fr 220px;grid-template-areas:'top top' 'main rail' 'timeline rail';height:100vh}.top{grid-area:top;display:flex;gap:18px;align-items:center;padding:0 12px;background:var(--surface);border-bottom:1px solid var(--border);font-size:10px;text-transform:uppercase}.brand{font-weight:800}.state{margin-left:auto;color:var(--muted)}.main{grid-area:main;overflow:auto;padding:12px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.rail{grid-area:rail;overflow:auto;border-left:1px solid var(--border);background:var(--surface);padding:10px}.timeline{grid-area:timeline;overflow:auto;border-top:1px solid var(--border);background:var(--surface);padding:10px}.panel,.card{border:1px solid var(--border);background:var(--panel);padding:10px;border-radius:2px}.title{font-size:9px;color:var(--muted);font-weight:800;text-transform:uppercase;margin-bottom:8px}.verdict{display:inline-block;border:1px solid var(--border);padding:5px 8px;margin-bottom:8px;text-transform:uppercase}.verdict.ready{color:var(--ok)}.verdict.blocked{color:var(--bad)}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}.kv{border:1px solid var(--border);padding:6px;background:#0b0b0b}.kv span{display:block;color:var(--muted);font-size:8px;text-transform:uppercase}.kv b{display:block;margin-top:3px;font-size:10px;text-transform:uppercase}table{width:100%;border-collapse:collapse;font-size:9px}td,th{border:1px solid var(--border);padding:5px;text-align:left;vertical-align:top}th{color:var(--muted);text-transform:uppercase}.path{color:var(--muted);overflow-wrap:anywhere}.bad{color:var(--bad)}.ok{color:var(--ok)}.warn{color:var(--warn)}pre{white-space:pre-wrap;overflow:auto;color:var(--muted);font-size:8px}</style>
</head>
<body>
<main>
<header class="top"><span class="brand">ION/JOC LIVE</span><span>HOST: CARRIER-CONTROL</span><span>STEWARD: INTEGRATION QUEUE</span><span class="state">${escapeHtml(String(runtime.status ?? 'unknown'))}</span></header>
<section class="main">
  <article class="panel"><div class="title">Runtime Status</div><div class="verdict ${escapeHtml(String(runtime.status ?? 'unknown'))}">${escapeHtml(String(runtime.status ?? 'unknown'))}</div><div>${escapeHtml(String(top.objective ?? 'no objective'))}</div><div class="grid">${row('mode', runtime.mode)}${row('hook', top.hook_status)}${row('gates', top.gate_count)}${row('spawn', `${top.spawn_count ?? 0}/${top.spawn_rows_total ?? 0}`)}${row('returns', `A${top.return_counts?.accepted ?? 0} R${top.return_counts?.rejected ?? 0}`)}${row('services', localServices.status ?? top.local_service_status ?? 'unknown')}</div></article>
  <article class="panel"><div class="title">Local Services</div><div class="verdict ${escapeHtml(String(localServices.status ?? 'unknown'))}">${escapeHtml(String(localServices.status ?? 'unknown'))}</div><table><tr><th>Unit</th><th>Status</th><th>Endpoint</th></tr>${serviceRows.map((s:any)=>`<tr><td>${escapeHtml(String(s.unit_name))}</td><td>${escapeHtml(String(s.status))}<div class="path">${escapeHtml((s.findings??[]).join(', '))}</div></td><td class="path">${escapeHtml(String(s.health_url ?? s.public_url ?? s.local_url ?? ''))}</td></tr>`).join('')}</table></article>
  <article class="panel"><div class="title">Carrier Paths</div>${Object.entries(model.source_paths ?? {}).map(([k,v])=>row(k,String(v))).join('')}</article>
  <article class="panel"><div class="title">Spawn Queue</div><table><tr><th>#</th><th>Role</th><th>Spawn</th><th>Status</th></tr>${(agents.spawn_rows??[]).map((r:any)=>`<tr><td>${escapeHtml(String(r.index))}</td><td>${escapeHtml(String(r.role))}</td><td>${escapeHtml(String(r.spawn))}</td><td>${escapeHtml(String(r.status))}<div class="path">${escapeHtml(String(r.context_package_path??''))}</div></td></tr>`).join('')}</table></article>
  <article class="panel"><div class="title">Task Returns</div><table><tr><th>Role</th><th>Decision</th><th>Path</th></tr>${(agents.returns??[]).map((r:any)=>`<tr><td>${escapeHtml(String(r.role))}</td><td>${escapeHtml(String(r.decision))}</td><td class="path">${escapeHtml(String(r.path??''))}</td></tr>`).join('')}</table></article>
  <article class="panel"><div class="title">Human Gates</div><pre>${escapeHtml(JSON.stringify(queues.human_gates ?? [], null, 2))}</pre></article>
  <article class="panel"><div class="title">Operator Queue</div><pre>${escapeHtml(JSON.stringify(queues.operator_messages ?? [], null, 2))}</pre></article>
</section>
<aside class="rail"><div class="title">Receipts</div>${receipts.map((r:any)=>`<div class="card"><b>${escapeHtml(String(r.name??'receipt'))}</b><div class="path">${escapeHtml(String(r.path??''))}</div><div>${escapeHtml(String(r.authority_class??''))}</div></div>`).join('')}<div class="title">Model Path</div><div class="path">${escapeHtml(modelPath)}</div></aside>
<footer class="timeline"><div class="title">Runtime Timeline</div>${timeline.map((e:any)=>`<div class="card"><b>${escapeHtml(String(e.source))}</b> / ${escapeHtml(String(e.event_type))} / <span class="${String(e.status)==='blocked'?'bad':'ok'}">${escapeHtml(String(e.status))}</span><div class="path">${escapeHtml(String(e.detail || e.path || ''))}</div></div>`).join('')}</footer>
</main>
</body>
</html>`;
}
