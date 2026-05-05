(() => {
  const seen = new Set();
  const inFlightActionIds = new Set();
  const submittedActionIds = new Set();
  const reportedBlockedActionIds = new Set();
  const ION_ACTION_LINE = /(^|\n)\s*ion_action:\s*(\n|$)/;
  const ACTION_SCAN_SELECTORS = [
    "pre code",
    "pre",
    "code",
    "[data-message-author-role='assistant']",
    "[data-message-author-role='assistant'] .markdown",
    "[data-message-author-role='assistant'] pre",
    "[data-message-author-role='assistant'] code",
    "[data-message-author-role='assistant'] [class*='font-mono']",
    "[data-message-author-role='assistant'] [class*='whitespace-pre']",
    "[data-message-author-role='assistant'] [class*='overflow-x-auto']",
    "article .markdown",
    "article pre",
    "article pre code",
    "article [class*='font-mono']",
    "article [class*='whitespace-pre']",
    "article [class*='overflow-x-auto']",
    "main",
  ];
  const PANEL_ID = "ion-chatops-bridge-panel";
  const MODAL_ID = "ion-chatops-bridge-approval";
  const STYLE_ID = "ion-chatops-bridge-style";
  const LOG_LIMIT = 12;
  const bridgeState = {
    title: "Monitoring ChatGPT",
    detail: "Waiting for ion_action YAML blocks.",
    tone: "idle",
    action: "No action detected yet.",
    agent: "Codex-backed agent status has not been requested yet.",
    packages: "No context pack or ZIP export has been requested yet.",
    diagnostics: "Normal carrier flow: Sev emits an ion_action YAML block in ChatGPT, the extension detects it, Braden approves it, the local daemon records/executes it, and ION writes a receipt.\n\nThe buttons below are local diagnostics only. They fabricate known-good test actions so the extension/daemon path can be checked without waiting on ChatGPT to emit YAML.",
    tools: "Daemon: http://127.0.0.1:8767\nUse Rescan after ChatGPT finishes rendering a YAML block.",
    logs: [],
  };
  const SEV_REENTRY_PROMPT = `You are Sev, Braden's ION browser carrier.

You do not have direct local repo context unless ION provides it. Use ION ChatOps action blocks to ask the local bridge/Codex for durable work.

When you need ION to do something, render one YAML/code block whose first YAML key is ion_action:. Literal triple-backtick characters are not required. Do not describe the block instead of emitting it.

Use this carrier boundary:
- callsign: Sev
- carrier: chatgpt_browser
- human_sovereign: Braden
- production_authority: false
- live_execution_authority: false

Supported MVP intents:
- write_file_draft
- create_codex_work_packet
- create_github_issue_draft
- register_artifact

For implementation work, prefer create_codex_work_packet so local Codex can inspect the repo, run tests, and return receipts.`;
  const SMOKE_ACTION = `ion_action:
  schema: ion.chatops.action.v1
  action_id: sev-20260505-0001-smoke
  intent: write_file_draft
  actor:
    callsign: Sev
    carrier: chatgpt_browser
  authority:
    human_sovereign: Braden
    requires_approval: true
    production_authority: false
    live_execution_authority: false
  target:
    provider: local_ion
    root: ION_CODEX
    path: ION/05_context/current/chatops_bridge/smoke/SEV_CHATOPS_SMOKE.md
    overwrite: false
  content:
    encoding: utf-8
    text: |
      # Sev ChatOps Smoke

      Sev emitted this canonical ION ChatOps action from ChatGPT Browser.
      The extension detected it, Braden approved it, and the local daemon wrote it.
  receipts:
    requested:
      - file_write_receipt
      - sha256_receipt`;
  const CODEX_WORK_ACTION = `ion_action:
  schema: ion.chatops.action.v1
  action_id: sev-20260505-0002-codex-work
  intent: create_codex_work_packet
  actor:
    callsign: Sev
    carrier: chatgpt_browser
  authority:
    human_sovereign: Braden
    requires_approval: true
    production_authority: false
    live_execution_authority: false
  objective: |
    Continue the ION ChatOps Browser Carrier Runtime work from the latest browser conversation.
    Inspect the repo, use existing ION gates, run focused validation, and return CONTEXT PROOF,
    TEMPLATE ACTION PROOF, VALIDATION, and RESULT.
  context_refs:
    - ION/02_architecture/ION_BROWSER_CARRIER_RUNTIME_PROTOCOL.md
    - ION/02_architecture/ION_CHATOPS_YAML_ACTION_PROTOCOL.md
    - ION/09_integrations/browser_extension/ion_chatops_bridge/
    - ION/04_packages/kernel/ion_chatops_bridge.py
  receipts:
    requested:
      - codex_work_packet_receipt
      - action_receipt`;

  function scalar(raw) {
    const value = raw.trim().replace(/\s+#.*$/, "");
    if (value === "true") return true;
    if (value === "false") return false;
    if (value === "null") return null;
    if (value === "[]") return [];
    if (/^-?\d+(\.\d+)?$/.test(value)) return Number(value);
    return value.replace(/^['"]|['"]$/g, "");
  }

  function setPath(root, path, value) {
    let cursor = root;
    for (const part of path.slice(0, -1)) {
      const existing = cursor[part];
      if (!existing || Array.isArray(existing) || typeof existing !== "object") {
        cursor[part] = {};
      }
      cursor = cursor[part];
    }
    cursor[path[path.length - 1]] = value;
  }

  function appendPath(root, path, value) {
    let cursor = root;
    for (const part of path.slice(0, -1)) {
      const existing = cursor[part];
      if (!existing || Array.isArray(existing) || typeof existing !== "object") {
        cursor[part] = {};
      }
      cursor = cursor[part];
    }
    const key = path[path.length - 1];
    if (!Array.isArray(cursor[key])) {
      cursor[key] = [];
    }
    cursor[key].push(value);
  }

  function canonicalizeIonAction(root) {
    const raw = root.ion_action;
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;
    const action = raw;
    if (!action.actor || typeof action.actor !== "object" || Array.isArray(action.actor)) {
      const callsign = action.callsign;
      const carrier = action.carrier;
      if (callsign || carrier) {
        action.actor = { callsign, carrier };
      }
    }
    if (!action.authority || typeof action.authority !== "object" || Array.isArray(action.authority)) {
      const authority = {};
      for (const key of ["human_sovereign", "requires_approval", "production_authority", "live_execution_authority"]) {
        if (key in action) authority[key] = action[key];
      }
      if (Object.keys(authority).length) action.authority = authority;
    }
    if (!action.receipts || typeof action.receipts !== "object" || Array.isArray(action.receipts)) {
      const intent = String(action.intent ?? "");
      const defaults = {
        write_file_draft: ["file_write_receipt", "sha256_receipt"],
        create_codex_work_packet: ["codex_work_packet_receipt", "action_receipt"],
        create_github_issue_draft: ["github_issue_draft_receipt", "action_receipt"],
        register_artifact: ["artifact_registration_receipt", "action_receipt"],
      };
      action.receipts = { requested: defaults[intent] ?? ["action_receipt"] };
    }
    root.ion_action = action;
    return root;
  }

  function extractIonActionYaml(text) {
    const normalized = text
      .replace(/\r\n/g, "\n")
      .replace(/\u00a0/g, " ")
      .replace(/[\u200b-\u200d\ufeff]/g, "");
    const lines = normalized
      .split("\n")
      .filter((line) => !line.trim().match(/^```/))
      .filter((line) => line.trim().toLowerCase() !== "yaml");
    const start = lines.findIndex((line) => /^\s*ion_action\s*:\s*(#.*)?$/.test(line));
    if (start < 0) return null;
    return lines.slice(start).join("\n");
  }

  function parseStrictIonActionYaml(text) {
    return parseIonActionYamlWithDiagnostics(text).packet;
  }

  function parseIonActionYamlWithDiagnostics(text) {
    const yaml = extractIonActionYaml(text);
    if (!yaml) return { packet: null, finding: "missing_top_level_ion_action", extracted_yaml: undefined };
    const lines = yaml.split("\n");
    const root = {};
    const stack = [];
    let literalPath = null;
    let literalIndent = 0;
    const literalLines = [];

    const flushLiteral = () => {
      if (!literalPath) return;
      setPath(root, literalPath, literalLines.join("\n").replace(/\n$/, ""));
      literalPath = null;
      literalLines.length = 0;
    };

    for (const raw of lines) {
      if (literalPath) {
        if (!raw.trim()) {
          literalLines.push("");
          continue;
        }
        const literalLineIndent = raw.length - raw.trimStart().length;
        if (literalLineIndent >= literalIndent) {
          literalLines.push(raw.slice(literalIndent));
          continue;
        }
        flushLiteral();
      }

      if (!raw.trim() || raw.trim().startsWith("#")) continue;
      const indent = raw.length - raw.trimStart().length;
      const trimmed = raw.trim();

      while (stack.length && indent <= stack[stack.length - 1].indent) {
        stack.pop();
      }
      const parent = stack.length ? stack[stack.length - 1].path : [];

      if (trimmed.startsWith("- ")) {
        appendPath(root, parent, scalar(trimmed.slice(2)));
        continue;
      }

      const split = trimmed.indexOf(":");
      if (split < 0) continue;
      const key = trimmed.slice(0, split).trim();
      const rest = trimmed.slice(split + 1).trim();
      const path = [...parent, key];

      if (!rest) {
        setPath(root, path, {});
        stack.push({ indent, path });
        continue;
      }
      if (rest === "|") {
        literalPath = path;
        literalIndent = indent + 2;
        continue;
      }
      setPath(root, path, scalar(rest));
    }
    flushLiteral();

    const packet = canonicalizeIonAction(root);
    if (!packet) {
      return { packet: null, finding: "ion_action_not_object", extracted_yaml: yaml.slice(0, 1200) };
    }
    return { packet, finding: null, extracted_yaml: yaml.slice(0, 1200) };
  }

  function localValidate(packet) {
    const action = packet.ion_action;
    const findings = [];
    const actionId = String(action.action_id ?? "");
    const objective = String(action.objective ?? "").trim();
    if (action.schema !== "ion.chatops.action.v1") findings.push("schema_must_be_ion_chatops_action_v1");
    if (!action.action_id) findings.push("action_id_required");
    if (/YYYY|MMDD|HHMMSS|short-slug/i.test(actionId)) findings.push("action_id_must_not_be_template_placeholder");
    if (!action.intent) findings.push("intent_required");
    if (action.actor?.callsign !== "Sev") findings.push("actor_callsign_must_be_Sev");
    if (action.actor?.carrier !== "chatgpt_browser") findings.push("actor_carrier_must_be_chatgpt_browser");
    if (action.authority?.human_sovereign !== "Braden") findings.push("human_sovereign_must_be_Braden");
    if (action.authority?.production_authority !== false) findings.push("production_authority_must_be_false");
    if (action.authority?.live_execution_authority !== false) findings.push("live_execution_authority_must_be_false");
    if (!action.receipts || !Array.isArray(action.receipts.requested)) {
      findings.push("receipts_requested_list_required");
    }
    if (objective === "State the exact bounded work for local Codex/ION to perform.") {
      findings.push("objective_must_be_concrete_not_template_placeholder");
    }
    return {
      accepted: findings.length === 0,
      findings,
      action_id: action.action_id,
      intent: action.intent,
      risk_class: action.authority?.requires_approval ? "approval_required" : "preview_only"
    };
  }

  function ensureStyle() {
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

  function ensurePanel() {
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
    panel.querySelectorAll(".ion-tab").forEach((tab) => {
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

  function positionPanelAboveComposer(panel = ensurePanel()) {
    panel.style.top = "2px";
    panel.style.left = "58px";
    panel.style.right = "auto";
    panel.style.bottom = "auto";
  }

  function renderPanel(panel = ensurePanel()) {
    panel.dataset.tone = bridgeState.tone;
    positionPanelAboveComposer(panel);
    const titleNode = panel.querySelector(".ion-title");
    if (titleNode) titleNode.textContent = bridgeState.title;
    const toggle = panel.querySelector(".ion-toggle");
    if (toggle) toggle.textContent = panel.dataset.expanded === "true" ? "-" : "+";
    const activeTab = panel.dataset.tab ?? "status";
    panel.querySelectorAll(".ion-tab").forEach((tab) => {
      tab.dataset.active = String(tab.dataset.tab === activeTab);
    });
    panel.querySelectorAll(".ion-tab-panel").forEach((tabPanel) => {
      tabPanel.dataset.active = String(tabPanel.dataset.panel === activeTab);
    });
    const statusNode = panel.querySelector('[data-field="status"]');
    const actionNode = panel.querySelector('[data-field="action"]');
    const agentNode = panel.querySelector('[data-field="agent"]');
    const packagesNode = panel.querySelector('[data-field="packages"]');
    const diagnosticsNode = panel.querySelector('[data-field="diagnostics"]');
    const toolsNode = panel.querySelector('[data-field="tools"]');
    if (statusNode) statusNode.textContent = bridgeState.detail;
    if (actionNode) actionNode.textContent = bridgeState.action;
    if (agentNode) agentNode.textContent = bridgeState.agent;
    if (packagesNode) packagesNode.textContent = bridgeState.packages;
    if (diagnosticsNode) diagnosticsNode.textContent = bridgeState.diagnostics;
    if (toolsNode) {
      toolsNode.textContent = `${bridgeState.tools}\n\nRecent:\n${bridgeState.logs.join("\n") || "No events yet."}`;
    }
  }

  function appendBridgeLog(entry) {
    bridgeState.logs.unshift(`${new Date().toLocaleTimeString()} ${entry}`);
    bridgeState.logs.splice(LOG_LIMIT);
  }

  function setBridgeStatus(title, detail = "", tone = "idle") {
    bridgeState.title = title;
    bridgeState.detail = detail;
    bridgeState.tone = tone;
    appendBridgeLog(`${title}${detail ? `: ${detail.split("\n")[0]}` : ""}`);
    renderPanel();
  }

  function setBridgeActionDetail(detail) {
    bridgeState.action = detail;
    renderPanel();
  }

  function setBridgeAgentDetail(detail) {
    bridgeState.agent = detail;
    renderPanel();
  }

  function setBridgePackageDetail(detail) {
    bridgeState.packages = detail;
    renderPanel();
  }

  function refreshBridgePosition() {
    positionPanelAboveComposer();
  }

  async function requestApproval(packet, validation) {
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
      const finish = (approved) => {
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

  async function requestBridgeApproval(operation, summary, riskClass = "approval_required_mutation") {
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
      const finish = (approved) => {
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

  async function copyReceiptSummary(summary) {
    try {
      await navigator.clipboard.writeText(summary);
    } catch (_error) {
      console.info("ION ChatOps receipt summary", summary);
    }
  }

  function shouldIgnoreScanNode(node) {
    if (typeof node.closest !== "function") return false;
    return Boolean(
      node.closest(`#${PANEL_ID}`) ??
        node.closest(`#${MODAL_ID}`) ??
        node.closest("[data-message-author-role='user']") ??
        node.closest("#prompt-textarea") ??
        node.closest("[contenteditable='true']") ??
        node.closest("textarea")
    );
  }

  function candidateBlocks() {
    const nodes = [];
    const seenNodes = new Set();
    for (const selector of ACTION_SCAN_SELECTORS) {
      document.querySelectorAll(selector).forEach((node) => {
        if (seenNodes.has(node) || shouldIgnoreScanNode(node)) return;
        seenNodes.add(node);
        nodes.push(node);
      });
    }
    const blocks = [];
    const seenText = new Set();
    for (const node of nodes) {
      const rawCandidates = [
        node.textContent ?? "",
        typeof node.innerText === "string" ? node.innerText : "",
      ];
      for (const text of rawCandidates) {
        if (!(ION_ACTION_LINE.test(text) || extractIonActionYaml(text) !== null)) continue;
        const starts = Array.from(text.matchAll(/(^|\n)\s*ion_action\s*:\s*(?=\n|$)/g));
        const slices = starts.length ? starts.map((match) => text.slice(match.index + match[1].length)) : [text];
        for (const slice of slices) {
          const extracted = extractIonActionYaml(slice) ?? slice;
          const key = `${extracted.length}:${extracted.slice(0, 240)}`;
          if (seenText.has(key)) continue;
          seenText.add(key);
          blocks.push(extracted);
        }
      }
    }
    return blocks;
  }

  function findComposer() {
    return (
      document.querySelector("#prompt-textarea") ??
      document.querySelector("textarea") ??
      document.querySelector("[contenteditable='true']")
    );
  }

  function insertIntoComposer(text) {
    const target = findComposer();
    if (!target) return false;
    target.focus();
    if (target instanceof HTMLTextAreaElement) {
      const start = target.selectionStart ?? target.value.length;
      const end = target.selectionEnd ?? target.value.length;
      target.value = `${target.value.slice(0, start)}${text}${target.value.slice(end)}`;
      target.selectionStart = start + text.length;
      target.selectionEnd = start + text.length;
      target.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText", data: text }));
      return true;
    }
    const inserted = document.execCommand("insertText", false, text);
    if (!inserted) {
      target.textContent = text;
      target.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText", data: text }));
    }
    return true;
  }

  function insertComposerBlock(label, text) {
    const ok = insertIntoComposer(`\`\`\`yaml\n${text}\n\`\`\``);
    setBridgeStatus(
      ok ? `${label} inserted` : "Composer not found",
      ok ? "Review the inserted block, then send it in ChatGPT." : "Click in the ChatGPT input box and try again.",
      ok ? "success" : "error",
    );
  }

  function insertComposerPrompt(label, text) {
    const ok = insertIntoComposer(text);
    setBridgeStatus(
      ok ? `${label} inserted` : "Composer not found",
      ok ? "Review the inserted prompt, then send it in ChatGPT." : "Click in the ChatGPT input box and try again.",
      ok ? "success" : "error",
    );
  }

  function insertSevContextBrief() {
    setBridgeStatus("Fetching ION context", "Requesting Sev onboarding brief from the local daemon.", "working");
    chrome.runtime.sendMessage({ type: "ion_chatops_fetch_sev_context" }, (response) => {
      const runtimeError = chrome.runtime.lastError?.message;
      const prompt = response?.result?.prompt;
      if (response?.ok && typeof prompt === "string" && prompt.trim()) {
        setBridgeActionDetail(JSON.stringify(response.result.brief ?? {}, null, 2).slice(0, 1600));
        insertComposerPrompt("Sev ION context brief", prompt);
        return;
      }
      setBridgeActionDetail(runtimeError ?? response?.error ?? response?.stage ?? "context_fetch_failed");
      insertComposerPrompt("Fallback Sev re-entry prompt", SEV_REENTRY_PROMPT);
    });
  }

  function actionStamp() {
    const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z").toLowerCase();
    return `sev-${stamp}`;
  }

  function stampActionText(text, kind) {
    const stamp = actionStamp();
    if (kind === "smoke") {
      return text
        .replace("sev-20260505-0001-smoke", `${stamp}-smoke`)
        .replace("SEV_CHATOPS_SMOKE.md", `SEV_CHATOPS_SMOKE_${stamp}.md`);
    }
    return text.replace("sev-20260505-0002-codex-work", `${stamp}-codex-work`);
  }

  function blockedDetail(response) {
    const validation = response?.validation;
    if (validation?.findings?.length) return validation.findings.join("\n");
    const result = response?.result;
    return (
      result?.execution?.finding ??
      result?.finding ??
      response?.error ??
      response?.finding ??
      response?.stage ??
      "No response from extension background worker."
    );
  }

  function compactJson(value, max = 1800) {
    const text = JSON.stringify(value ?? null, null, 2);
    return text.length > max ? `${text.slice(0, max)}\n...` : text;
  }

  async function copyBridgeResult(label, detail) {
    await copyReceiptSummary(`${label}\n${detail}`);
  }

  function requestAgentRead(type, label) {
    setBridgeStatus(label, "Requesting local daemon projection.", "working");
    chrome.runtime.sendMessage({ type }, async (response) => {
      const detail = response?.ok ? compactJson(response.result) : blockedDetail(response);
      setBridgeAgentDetail(detail);
      setBridgeStatus(response?.ok ? `${label} ready` : `${label} blocked`, detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
      if (response?.ok) await copyBridgeResult(label, detail);
    });
  }

  function requestAgentMutation(type, label) {
    setBridgeStatus(label, "Requesting Braden approval through the bridge panel.", "working");
    chrome.runtime.sendMessage({ type, payload: {} }, async (response) => {
      const detail = response?.ok ? compactJson(response.result) : blockedDetail(response);
      setBridgeAgentDetail(detail);
      setBridgeStatus(response?.ok ? `${label} submitted` : `${label} blocked`, detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
      if (response?.ok) await copyBridgeResult(label, detail);
    });
  }

  function requestContextPack() {
    setBridgeStatus("Context pack", "Fetching current ION/agent context from local daemon.", "working");
    chrome.runtime.sendMessage({ type: "ion_chatops_context_pack" }, (response) => {
      const prompt = response?.result?.prompt;
      if (response?.ok && typeof prompt === "string" && prompt.trim()) {
        setBridgePackageDetail(compactJson(response.result.pack));
        insertComposerPrompt("ION context pack", prompt);
        return;
      }
      const detail = blockedDetail(response);
      setBridgePackageDetail(detail);
      setBridgeStatus("Context pack blocked", detail, "error");
    });
  }

  function requestZip(type, label) {
    setBridgeStatus(label, "Requesting Braden approval before creating a local package artifact.", "working");
    chrome.runtime.sendMessage({ type }, async (response) => {
      const result = response?.result;
      const detail = response?.ok
        ? [
            `zip_path: ${result?.zip_path ?? ""}`,
            `zip_sha256: ${result?.zip_sha256 ?? ""}`,
            `receipt_path: ${result?.receipt_path ?? ""}`,
          ].join("\n")
        : blockedDetail(response);
      setBridgePackageDetail(response?.ok ? `${detail}\n\n${compactJson(result, 1400)}` : detail);
      setBridgeStatus(response?.ok ? `${label} ready` : `${label} blocked`, detail, response?.ok ? "success" : "error");
      if (response?.ok) await copyBridgeResult(label, detail);
    });
  }

  function actionSummary(packet) {
    if (!packet) return "packet_parse_failed";
    return JSON.stringify({
      action_id: packet.ion_action.action_id,
      intent: packet.ion_action.intent,
      target: packet.ion_action.target ?? packet.ion_action.github ?? {},
      receipts: packet.ion_action.receipts?.requested ?? [],
    }, null, 2);
  }

  function shouldSkipAction(packet) {
    const actionId = packet?.ion_action?.action_id;
    return Boolean(actionId && (inFlightActionIds.has(actionId) || submittedActionIds.has(actionId)));
  }

  function markBlockedOnce(packet, findings) {
    const actionId = packet?.ion_action?.action_id;
    const key = actionId ? `${actionId}:${findings.join("|")}` : findings.join("|");
    if (reportedBlockedActionIds.has(key)) return false;
    reportedBlockedActionIds.add(key);
    return true;
  }

  function submitPacket(label, packet) {
    if (!packet) {
      setBridgeStatus(`${label} blocked`, "packet_parse_failed", "error");
      return;
    }
    if (shouldSkipAction(packet)) return;
    const local = localValidate(packet);
    setBridgeActionDetail(actionSummary(packet));
    if (!local.accepted) {
      if (!markBlockedOnce(packet, local.findings)) return;
      setBridgeStatus(`${label} blocked locally`, local.findings.join("\n"), "error");
      return;
    }
    const actionId = packet.ion_action.action_id;
    if (actionId) inFlightActionIds.add(actionId);
    setBridgeStatus(`${label} ready`, `${packet.ion_action.intent}: ${packet.ion_action.action_id}\nRequesting daemon validation and approval.`, "working");
    chrome.runtime.sendMessage({ type: "ion_chatops_candidate", packet }, async (response) => {
      if (!response?.ok || !response?.result) {
        if (actionId) inFlightActionIds.delete(actionId);
        setBridgeStatus(`${label} blocked`, blockedDetail(response), "error");
        return;
      }
      if (actionId) {
        inFlightActionIds.delete(actionId);
        submittedActionIds.add(actionId);
      }
      const result = response.result;
      const summary = [
        "ION ChatOps receipt",
        `action_id: ${packet.ion_action.action_id}`,
        `intent: ${packet.ion_action.intent}`,
        `receipt_path: ${result.receipt_path ?? ""}`,
        `status: ${result.verdict ?? ""}`
      ].join("\n");
      await copyReceiptSummary(summary);
      setBridgeStatus(`${label} submitted`, summary, "success");
    });
  }

  function submitActionText(label, text) {
    const parsed = parseIonActionYamlWithDiagnostics(text);
    if (!parsed.packet) {
      setBridgeStatus(`${label} blocked`, parsed.finding ?? "unknown_parse_failure", "error");
      setBridgeActionDetail((parsed.extracted_yaml ?? text).slice(0, 1200));
      return;
    }
    submitPacket(label, parsed.packet);
  }

  function scan() {
    refreshBridgePosition();
    let processed = 0;
    for (const block of candidateBlocks()) {
      const key = `${block.length}:${block.slice(0, 160)}`;
      if (seen.has(key)) continue;
      seen.add(key);
      processed += 1;
      const parsed = parseIonActionYamlWithDiagnostics(block);
      const packet = parsed.packet;
      if (!packet) {
        setBridgeStatus("YAML detected but not parsed", parsed.finding ?? "unknown_parse_failure", "error");
        setBridgeActionDetail((parsed.extracted_yaml ?? block).slice(0, 1200));
        continue;
      }
      if (shouldSkipAction(packet)) continue;
      const local = localValidate(packet);
      if (!local.accepted) {
        if (!markBlockedOnce(packet, local.findings)) continue;
        setBridgeStatus("YAML blocked locally", local.findings.join("\n"), "error");
        setBridgeActionDetail(JSON.stringify(packet.ion_action, null, 2));
        console.warn("ION ChatOps candidate failed local validation", local);
        continue;
      }
      setBridgeActionDetail(actionSummary(packet));
      const actionId = packet.ion_action.action_id;
      if (actionId) inFlightActionIds.add(actionId);
      setBridgeStatus("ION action detected", `${packet.ion_action.intent}: ${packet.ion_action.action_id}\nValidating with local daemon.`, "working");
      chrome.runtime.sendMessage({ type: "ion_chatops_candidate", packet }, async (response) => {
        if (!response?.ok || !response?.result) {
          if (actionId) inFlightActionIds.delete(actionId);
          setBridgeStatus(
            "ION action blocked",
            blockedDetail(response),
            "error",
          );
          return;
        }
        if (actionId) {
          inFlightActionIds.delete(actionId);
          submittedActionIds.add(actionId);
        }
        const result = response.result;
        const summary = [
          "ION ChatOps receipt",
          `action_id: ${packet.ion_action.action_id}`,
          `intent: ${packet.ion_action.intent}`,
          `receipt_path: ${result.receipt_path ?? ""}`,
          `status: ${result.verdict ?? ""}`
        ].join("\n");
        await copyReceiptSummary(summary);
        setBridgeStatus("ION action submitted", summary, "success");
      });
    }
    return processed;
  }

  chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (message?.type === "ion_chatops_request_approval") {
      requestApproval(message.packet, message.validation)
        .then((approved) => sendResponse({ approved }))
        .catch(() => sendResponse({ approved: false }));
      return true;
    }
    if (message?.type === "ion_chatops_request_bridge_approval") {
      requestBridgeApproval(message.operation, message.summary, message.riskClass)
        .then((approved) => sendResponse({ approved }))
        .catch(() => sendResponse({ approved: false }));
      return true;
    }
    return false;
  });

  window.__ION_CHATOPS_BRIDGE_DEBUG__ = {
    extractIonActionYaml,
    parseIonActionYamlWithDiagnostics,
    parseStrictIonActionYaml,
    localValidate,
    candidateBlocks,
    submitActionText,
    rescan: () => {
      seen.clear();
      return scan();
    },
  };

  const observer = new MutationObserver(() => scan());
  observer.observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener("resize", () => refreshBridgePosition());
  window.addEventListener("ion-chatops-rescan", () => {
    seen.clear();
    setBridgeStatus("Manual rescan", "Scanning rendered ChatGPT code blocks.", "working");
    const found = scan();
    if (!found) {
      setBridgeStatus(
        "No action block found",
        "Scanned rendered assistant/code blocks. I did not find a top-level ion_action YAML block.",
        "idle"
      );
    }
  });
  window.addEventListener("ion-chatops-insert-reentry", () => {
    insertSevContextBrief();
  });
  window.addEventListener("ion-chatops-insert-smoke", () => {
    submitActionText("Smoke action", stampActionText(SMOKE_ACTION, "smoke"));
  });
  window.addEventListener("ion-chatops-insert-codex-work", () => {
    submitActionText("Codex work action", stampActionText(CODEX_WORK_ACTION, "codex"));
  });
  window.addEventListener("ion-chatops-agent-status", () => {
    requestAgentRead("ion_chatops_agent_status", "Agent status");
  });
  window.addEventListener("ion-chatops-agent-queue", () => {
    requestAgentRead("ion_chatops_agent_queue", "Agent queue");
  });
  window.addEventListener("ion-chatops-agent-prepare", () => {
    requestAgentMutation("ion_chatops_agent_prepare_next", "Agent prepare next");
  });
  window.addEventListener("ion-chatops-agent-start", () => {
    requestAgentMutation("ion_chatops_agent_start_one", "Agent start one");
  });
  window.addEventListener("ion-chatops-context-pack", () => {
    requestContextPack();
  });
  window.addEventListener("ion-chatops-compact-zip", () => {
    requestZip("ion_chatops_compact_zip", "Compact runtime ZIP");
  });
  window.addEventListener("ion-chatops-safe-full-zip", () => {
    requestZip("ion_chatops_safe_full_zip", "Safe full project ZIP");
  });
  setBridgeStatus("Monitoring ChatGPT", "Waiting for ion_action YAML blocks.", "idle");
  scan();
})();
