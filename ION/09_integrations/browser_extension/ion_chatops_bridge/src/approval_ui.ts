import type { IonActionPacket, ValidationResult } from "./schema";

type BridgeTone = "idle" | "working" | "approval" | "success" | "error";

const PANEL_ID = "ion-chatops-bridge-panel";
const MODAL_ID = "ion-chatops-bridge-approval";
const STYLE_ID = "ion-chatops-bridge-style";
const LOG_LIMIT = 12;

const bridgeState = {
  title: "Monitoring ChatGPT",
  detail: "Waiting for ion_action YAML blocks.",
  tone: "idle" as BridgeTone,
  action: "No action detected yet.",
  agent: "Codex-backed agent status has not been requested yet.",
  packages: "No context pack or ZIP export has been requested yet.",
  diagnostics:
    "Normal carrier flow: Sev emits an ion_action YAML block in ChatGPT, the extension detects it, Braden approves it, the local daemon records/executes it, and ION writes a receipt.\n\nThe buttons below are local diagnostics only. They fabricate known-good test actions so the extension/daemon path can be checked without waiting on ChatGPT to emit YAML.",
  tools: "Daemon: http://127.0.0.1:8767\nUse Rescan after ChatGPT finishes rendering a YAML block.",
  logs: [] as string[],
};

function ensureStyle(): void {
  if (document.getElementById(STYLE_ID)) return;
  const style = document.createElement("style");
  style.id = STYLE_ID;
  style.textContent = `
    #${PANEL_ID}, #${MODAL_ID} {
      color-scheme: dark;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }
    #${PANEL_ID} {
      position: fixed;
      top: 2px;
      left: 58px;
      right: auto;
      bottom: auto;
      z-index: 2147483646;
      width: clamp(430px, 56vw, 640px);
      max-width: calc(100vw - 380px);
      border: 1px solid rgba(255,255,255,0.10);
      border-radius: 10px;
      background: rgba(33, 33, 33, 0.94);
      box-shadow: 0 8px 28px rgba(0,0,0,0.22);
      padding: 4px;
      backdrop-filter: blur(12px);
    }
    #${PANEL_ID}[data-expanded="true"] {
      width: clamp(430px, 56vw, 640px);
      max-width: calc(100vw - 380px);
    }
    #${PANEL_ID} .ion-toolbar {
      display: flex;
      align-items: center;
      gap: 6px;
      min-height: 34px;
    }
    #${PANEL_ID} .ion-row {
      display: flex;
      align-items: center;
      gap: 7px;
      min-width: 0;
      flex: 1 1 auto;
      padding: 0 7px;
    }
    #${PANEL_ID} .ion-dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      flex: 0 0 auto;
      background: #9ca3af;
      box-shadow: 0 0 18px currentColor;
    }
    #${PANEL_ID}[data-tone="working"] .ion-dot,
    #${PANEL_ID}[data-tone="approval"] .ion-dot { background: #fbbf24; color: #fbbf24; }
    #${PANEL_ID}[data-tone="success"] .ion-dot { background: #34d399; color: #34d399; }
    #${PANEL_ID}[data-tone="error"] .ion-dot { background: #fb7185; color: #fb7185; }
    #${PANEL_ID} .ion-title {
      font-size: 12px;
      font-weight: 600;
      line-height: 1.25;
      overflow-wrap: anywhere;
      color: rgba(255,255,255,0.88);
    }
    #${PANEL_ID} .ion-label {
      font-size: 10px;
      color: rgba(255,255,255,0.56);
      margin-bottom: 0;
    }
    #${PANEL_ID} .ion-toggle,
    #${PANEL_ID} .ion-tool,
    #${PANEL_ID} .ion-tab {
      flex: 0 0 auto;
      height: 28px;
      border: 1px solid transparent;
      border-radius: 8px;
      color: rgba(255,255,255,0.82);
      background: transparent;
      padding: 0 8px;
      font-size: 12px;
      font-weight: 500;
      line-height: 1;
      cursor: pointer;
    }
    #${PANEL_ID} .ion-toggle {
      min-width: 32px;
      margin-left: 2px;
    }
    #${PANEL_ID} .ion-toggle:hover,
    #${PANEL_ID} .ion-tool:hover,
    #${PANEL_ID} .ion-tab:hover {
      background: rgba(255,255,255,0.08);
      border-color: rgba(255,255,255,0.08);
    }
    #${PANEL_ID} .ion-toolbar-actions {
      display: flex;
      align-items: center;
      gap: 2px;
      flex: 0 0 auto;
    }
    #${PANEL_ID} .ion-tab-panel .ion-toolbar-actions {
      flex-wrap: wrap;
      gap: 6px;
    }
    #${PANEL_ID} .ion-tabs,
    #${PANEL_ID} .ion-tab-panel,
    #${PANEL_ID} .ion-expanded {
      display: none;
    }
    #${PANEL_ID}[data-expanded="true"] .ion-expanded {
      display: block;
      border-top: 1px solid rgba(255,255,255,0.08);
      margin: 4px 2px 0;
      padding: 8px 8px 9px;
    }
    #${PANEL_ID}[data-expanded="true"] .ion-tabs {
      display: flex;
    }
    #${PANEL_ID}[data-expanded="true"] .ion-tab-panel[data-active="true"] {
      display: flex;
    }
    #${PANEL_ID} .ion-tabs {
      gap: 6px;
      margin-top: 0;
    }
    #${PANEL_ID} .ion-tab[data-active="true"] {
      color: rgba(255,255,255,0.96);
      background: rgba(255,255,255,0.11);
      border-color: rgba(255,255,255,0.10);
    }
    #${PANEL_ID} .ion-detail {
      margin-top: 0;
      color: rgba(255,255,255,0.74);
      font-size: 12px;
      line-height: 1.35;
      overflow-wrap: anywhere;
      white-space: pre-wrap;
    }
    #${PANEL_ID} .ion-tab-panel {
      flex-direction: column;
      gap: 8px;
      margin-top: 9px;
    }
    #${MODAL_ID} {
      position: fixed;
      top: 62px;
      left: 58px;
      right: auto;
      bottom: auto;
      z-index: 2147483647;
      width: min(420px, calc(100vw - 36px));
      border: 1px solid rgba(255,255,255,0.20);
      border-radius: 8px;
      background: rgba(12, 13, 16, 0.97);
      box-shadow: 0 22px 70px rgba(0,0,0,0.55);
      padding: 14px;
      backdrop-filter: blur(16px);
    }
    #${MODAL_ID} .ion-modal-title {
      font-size: 15px;
      font-weight: 700;
      margin-bottom: 10px;
    }
    #${MODAL_ID} .ion-preview {
      display: grid;
      gap: 7px;
      font-size: 12px;
      line-height: 1.35;
      color: rgba(255,255,255,0.78);
    }
    #${MODAL_ID} .ion-preview code {
      color: #f8fafc;
      background: rgba(255,255,255,0.08);
      border-radius: 5px;
      padding: 2px 5px;
      overflow-wrap: anywhere;
    }
    #${MODAL_ID} .ion-actions {
      display: flex;
      justify-content: flex-end;
      gap: 8px;
      margin-top: 14px;
    }
    #${MODAL_ID} button {
      appearance: none;
      border: 1px solid rgba(255,255,255,0.18);
      border-radius: 7px;
      color: #f8fafc;
      background: rgba(255,255,255,0.08);
      padding: 8px 11px;
      font-size: 12px;
      font-weight: 650;
      cursor: pointer;
    }
    #${MODAL_ID} button[data-primary="true"] {
      color: #07110d;
      background: #34d399;
      border-color: #34d399;
    }
  `;
  document.documentElement.appendChild(style);
}

function ensurePanel(): HTMLElement {
  ensureStyle();
  let panel = document.getElementById(PANEL_ID);
  if (panel) return panel;
  panel = document.createElement("section");
  panel.id = PANEL_ID;
  panel.setAttribute("aria-live", "polite");
  panel.dataset.expanded = "false";
  panel.dataset.tab = "status";
  panel.innerHTML = `
    <div class="ion-toolbar">
      <div class="ion-row">
        <span class="ion-dot"></span>
        <div>
          <div class="ion-label">ION ChatOps</div>
          <div class="ion-title"></div>
        </div>
      </div>
      <div class="ion-toolbar-actions">
        <button type="button" class="ion-tool" data-tool="rescan">Rescan</button>
        <button type="button" class="ion-tool" data-tool="insert-reentry">Onboard</button>
        <button type="button" class="ion-toggle" title="Expand ION ChatOps details">+</button>
      </div>
    </div>
    <div class="ion-expanded">
      <div class="ion-tabs">
        <button type="button" class="ion-tab" data-tab="status">Status</button>
        <button type="button" class="ion-tab" data-tab="action">Action</button>
        <button type="button" class="ion-tab" data-tab="agent">Agent</button>
        <button type="button" class="ion-tab" data-tab="packages">Packages</button>
        <button type="button" class="ion-tab" data-tab="diagnostics">Diagnostics</button>
        <button type="button" class="ion-tab" data-tab="tools">Log</button>
      </div>
      <div class="ion-tab-panel" data-panel="status"><div class="ion-detail" data-field="status"></div></div>
      <div class="ion-tab-panel" data-panel="action"><div class="ion-detail" data-field="action"></div></div>
      <div class="ion-tab-panel" data-panel="agent">
        <div class="ion-detail" data-field="agent"></div>
        <div class="ion-toolbar-actions">
          <button type="button" class="ion-tool" data-tool="agent-status">Status</button>
          <button type="button" class="ion-tool" data-tool="agent-queue">Queue</button>
          <button type="button" class="ion-tool" data-tool="agent-prepare">Prepare Next</button>
          <button type="button" class="ion-tool" data-tool="agent-start">Start One</button>
        </div>
      </div>
      <div class="ion-tab-panel" data-panel="packages">
        <div class="ion-detail" data-field="packages"></div>
        <div class="ion-toolbar-actions">
          <button type="button" class="ion-tool" data-tool="context-pack">Context Pack</button>
          <button type="button" class="ion-tool" data-tool="compact-zip">Compact ZIP</button>
          <button type="button" class="ion-tool" data-tool="safe-full-zip">Safe Full ZIP</button>
        </div>
      </div>
      <div class="ion-tab-panel" data-panel="diagnostics">
        <div class="ion-detail" data-field="diagnostics"></div>
        <div class="ion-toolbar-actions">
          <button type="button" class="ion-tool" data-tool="insert-smoke">Submit Smoke Test</button>
          <button type="button" class="ion-tool" data-tool="insert-codex">Queue Codex Test Work</button>
        </div>
      </div>
      <div class="ion-tab-panel" data-panel="tools"><div class="ion-detail" data-field="tools"></div></div>
    </div>
  `;
  document.documentElement.appendChild(panel);
  panel.querySelector(".ion-toggle")?.addEventListener("click", () => {
    panel.dataset.expanded = panel.dataset.expanded === "true" ? "false" : "true";
    renderPanel(panel);
  });
  panel.querySelectorAll<HTMLElement>(".ion-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      panel.dataset.tab = tab.dataset.tab ?? "status";
      renderPanel(panel);
    });
  });
  panel.querySelector('[data-tool="rescan"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-rescan"));
  });
  panel.querySelector('[data-tool="insert-reentry"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-insert-reentry"));
  });
  panel.querySelector('[data-tool="insert-smoke"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-insert-smoke"));
  });
  panel.querySelector('[data-tool="insert-codex"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-insert-codex-work"));
  });
  panel.querySelector('[data-tool="agent-status"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-agent-status"));
  });
  panel.querySelector('[data-tool="agent-queue"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-agent-queue"));
  });
  panel.querySelector('[data-tool="agent-prepare"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-agent-prepare"));
  });
  panel.querySelector('[data-tool="agent-start"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-agent-start"));
  });
  panel.querySelector('[data-tool="context-pack"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-context-pack"));
  });
  panel.querySelector('[data-tool="compact-zip"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-compact-zip"));
  });
  panel.querySelector('[data-tool="safe-full-zip"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-safe-full-zip"));
  });
  panel.querySelector('[data-tool="collapse"]')?.addEventListener("click", () => {
    panel.dataset.expanded = "false";
    renderPanel(panel);
  });
  renderPanel(panel);
  return panel;
}

function renderPanel(panel = ensurePanel()): void {
  panel.dataset.tone = bridgeState.tone;
  positionPanelAboveComposer(panel);
  const titleNode = panel.querySelector<HTMLElement>(".ion-title");
  if (titleNode) titleNode.textContent = bridgeState.title;
  const toggle = panel.querySelector<HTMLElement>(".ion-toggle");
  if (toggle) toggle.textContent = panel.dataset.expanded === "true" ? "-" : "+";
  const activeTab = panel.dataset.tab ?? "status";
  panel.querySelectorAll<HTMLElement>(".ion-tab").forEach((tab) => {
    tab.dataset.active = String(tab.dataset.tab === activeTab);
  });
  panel.querySelectorAll<HTMLElement>(".ion-tab-panel").forEach((tabPanel) => {
    tabPanel.dataset.active = String(tabPanel.dataset.panel === activeTab);
  });
  const statusNode = panel.querySelector<HTMLElement>('[data-field="status"]');
  const actionNode = panel.querySelector<HTMLElement>('[data-field="action"]');
  const agentNode = panel.querySelector<HTMLElement>('[data-field="agent"]');
  const packagesNode = panel.querySelector<HTMLElement>('[data-field="packages"]');
  const diagnosticsNode = panel.querySelector<HTMLElement>('[data-field="diagnostics"]');
  const toolsNode = panel.querySelector<HTMLElement>('[data-field="tools"]');
  if (statusNode) statusNode.textContent = bridgeState.detail;
  if (actionNode) actionNode.textContent = bridgeState.action;
  if (agentNode) agentNode.textContent = bridgeState.agent;
  if (packagesNode) packagesNode.textContent = bridgeState.packages;
  if (diagnosticsNode) diagnosticsNode.textContent = bridgeState.diagnostics;
  if (toolsNode) toolsNode.textContent = `${bridgeState.tools}\n\nRecent:\n${bridgeState.logs.join("\n") || "No events yet."}`;
}

function positionPanelAboveComposer(panel = ensurePanel()): void {
  panel.style.top = "2px";
  panel.style.left = "58px";
  panel.style.right = "auto";
  panel.style.bottom = "auto";
}

export function setBridgeStatus(title: string, detail = "", tone: BridgeTone = "idle"): void {
  bridgeState.title = title;
  bridgeState.detail = detail;
  bridgeState.tone = tone;
  appendBridgeLog(`${title}${detail ? `: ${detail.split("\n")[0]}` : ""}`);
  renderPanel();
}

export function setBridgeActionDetail(detail: string): void {
  bridgeState.action = detail;
  renderPanel();
}

export function setBridgeAgentDetail(detail: string): void {
  bridgeState.agent = detail;
  renderPanel();
}

export function setBridgePackageDetail(detail: string): void {
  bridgeState.packages = detail;
  renderPanel();
}

export function appendBridgeLog(entry: string): void {
  bridgeState.logs.unshift(`${new Date().toLocaleTimeString()} ${entry}`);
  bridgeState.logs.splice(LOG_LIMIT);
}

export function refreshBridgePosition(): void {
  positionPanelAboveComposer();
}

export async function requestApproval(packet: IonActionPacket, validation: ValidationResult): Promise<boolean> {
  const action = packet.ion_action;
  setBridgeStatus("Approval required", `${action.intent}: ${action.action_id}`, "approval");
  document.getElementById(MODAL_ID)?.remove();

  return new Promise((resolve) => {
    ensureStyle();
    const modal = document.createElement("section");
    modal.id = MODAL_ID;
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "false");
    modal.innerHTML = `
      <div class="ion-modal-title">Approve ION ChatOps Action</div>
      <div class="ion-preview">
        <div>action_id: <code></code></div>
        <div>intent: <code></code></div>
        <div>risk: <code></code></div>
        <div>target: <code></code></div>
        <div>receipts: <code></code></div>
      </div>
      <div class="ion-actions">
        <button type="button" data-choice="reject">Reject</button>
        <button type="button" data-choice="approve" data-primary="true">Approve</button>
      </div>
    `;
    const values = [
      action.action_id,
      action.intent,
      validation.risk_class ?? "unknown",
      JSON.stringify(action.target ?? action.github ?? {}),
      JSON.stringify(action.receipts?.requested ?? []),
    ];
    modal.querySelectorAll("code").forEach((node, index) => {
      node.textContent = values[index] ?? "";
    });
    const finish = (approved: boolean) => {
      modal.remove();
      setBridgeStatus(
        approved ? "Approved, submitting" : "Action rejected",
        approved ? `${action.action_id}` : `${action.action_id} was not sent to ION.`,
        approved ? "working" : "error",
      );
      resolve(approved);
    };
    modal.querySelector('[data-choice="reject"]')?.addEventListener("click", () => finish(false));
    modal.querySelector('[data-choice="approve"]')?.addEventListener("click", () => finish(true));
    document.documentElement.appendChild(modal);
  });
}

export async function requestBridgeApproval(operation: string, summary: string, riskClass = "approval_required_mutation"): Promise<boolean> {
  setBridgeStatus("Approval required", operation, "approval");
  document.getElementById(MODAL_ID)?.remove();

  return new Promise((resolve) => {
    ensureStyle();
    const modal = document.createElement("section");
    modal.id = MODAL_ID;
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "false");
    modal.innerHTML = `
      <div class="ion-modal-title">Approve ION ChatOps Operation</div>
      <div class="ion-preview">
        <div>operation: <code></code></div>
        <div>risk: <code></code></div>
        <div>summary: <code></code></div>
      </div>
      <div class="ion-actions">
        <button type="button" data-choice="reject">Reject</button>
        <button type="button" data-choice="approve" data-primary="true">Approve</button>
      </div>
    `;
    const values = [operation, riskClass, summary];
    modal.querySelectorAll("code").forEach((node, index) => {
      node.textContent = values[index] ?? "";
    });
    const finish = (approved: boolean) => {
      modal.remove();
      setBridgeStatus(
        approved ? "Approved, submitting" : "Operation rejected",
        approved ? operation : `${operation} was not sent to ION.`,
        approved ? "working" : "error",
      );
      resolve(approved);
    };
    modal.querySelector('[data-choice="reject"]')?.addEventListener("click", () => finish(false));
    modal.querySelector('[data-choice="approve"]')?.addEventListener("click", () => finish(true));
    document.documentElement.appendChild(modal);
  });
}

export async function copyReceiptSummary(summary: string): Promise<void> {
  try {
    await navigator.clipboard.writeText(summary);
  } catch (_error) {
    console.info("ION ChatOps receipt summary", summary);
  }
}
