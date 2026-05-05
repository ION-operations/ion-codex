(() => {
  const seen = new Set();
  const inFlightActionIds = new Set();
  const submittedActionIds = new Set();
  const reportedBlockedActionIds = new Set();
  const PANEL_ID = "ion-chatops-bridge-panel";
  const MODAL_ID = "ion-chatops-bridge-approval";
  const DOM_REGISTRY_STYLE_ID = "ion-chatops-dom-registry-style";
  const SAFE_MODE_KEY = "ION_CHATOPS_SAFE_MODE";
  const SCAN_DEBOUNCE_MS = 450;
  const ION_ACTION_LINE = /(^|\n)\s*ion_action:\s*(\n|$)/;
  const AUTO_SCAN_SELECTORS = [
    "pre code",
    "pre",
    "code",
    "[data-message-author-role='assistant'] pre",
    "[data-message-author-role='assistant'] code",
    "[data-message-author-role='assistant'] [class*='font-mono']",
    "[data-message-author-role='assistant'] [class*='whitespace-pre']",
    "[data-message-author-role='assistant'] [class*='overflow-x-auto']",
    "article pre",
    "article pre code",
    "article [class*='font-mono']",
    "article [class*='whitespace-pre']",
    "article [class*='overflow-x-auto']",
  ];
  const MANUAL_SCAN_SELECTORS = [
    ...AUTO_SCAN_SELECTORS,
    "[data-message-author-role='assistant']",
    "[data-message-author-role='assistant'] .markdown",
    "article .markdown",
    "main",
  ];
  const STYLE_ID = "ion-chatops-bridge-style";
  const LOG_LIMIT = 12;
  const TOP_BAR_GAP = 8;
  const PANEL_TOP = 2;
  const DEFAULT_LEFT_BOUNDARY = 50;
  const DEFAULT_RIGHT_RESERVE = 250;
  const PANEL_PREFERRED_WIDTH = 640;
  const PANEL_MIN_WIDTH = 320;
  const PANEL_TINY_WIDTH = 230;
  const COMPOSER_PANEL_MAX_WIDTH = 920;
  const bridgeState = {
    title: "Monitoring ChatGPT",
    detail: "Waiting for ion_action YAML blocks.",
    tone: "idle",
    action: "No action detected yet.",
    agent: "Codex-backed agent status has not been requested yet.",
    packages: "No context pack or ZIP export has been requested yet.",
    sandbox: "No ChatGPT sandbox returns have been requested yet.",
    automation: "Automation controls are staged only. This packet does not execute macros.",
    artifacts: "Artifact detection is staged only. No upload or local file movement occurs in this shell slice.",
    diagnostics: "Normal carrier flow: Sev emits an ion_action YAML block in ChatGPT, the extension detects it, Braden approves it, the local daemon records/executes it, and ION writes a receipt.\n\nThe buttons below are local diagnostics only. They fabricate known-good test actions so the extension/daemon path can be checked without waiting on ChatGPT to emit YAML.",
    tools: "Daemon: http://127.0.0.1:8767\nUse Rescan after ChatGPT finishes rendering a YAML block.",
    logs: [],
    anchor: {
      mode: "topbar_fallback",
      rect: null,
      element: null,
      health: "degraded",
      detail: "Composer anchor has not been evaluated yet.",
      source: "none",
      attachmentsDetected: 0,
    },
  };
  let composerResizeObserver = null;
  let observedComposerElement = null;
  let scanTimer = null;
  let scanRunning = false;
  let scanQueued = false;
  function safeModeDisabled() {
    try {
      const value = window.localStorage?.getItem(SAFE_MODE_KEY) ?? window.sessionStorage?.getItem(SAFE_MODE_KEY);
      return ["1", "true", "disabled", "off"].includes(String(value ?? "").trim().toLowerCase());
    } catch (_error) {
      return false;
    }
  }
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

  function ensureDomRegistryStyle() {
    if (document.getElementById(DOM_REGISTRY_STYLE_ID)) return;
    const style = document.createElement("style");
    style.id = DOM_REGISTRY_STYLE_ID;
    style.textContent = `
    .ion-dom-badge {
      position: absolute;
      top: 6px;
      left: 8px;
      z-index: 7;
      height: 18px;
      max-width: 220px;
      padding: 0 7px;
      border: 1px solid rgba(255,255,255,0.10);
      border-radius: 999px;
      background: rgba(12,12,12,0.68);
      color: rgba(255,255,255,0.62);
      font: 10px/18px ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      pointer-events: none;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      backdrop-filter: blur(8px);
      box-shadow: 0 4px 14px rgba(0,0,0,0.16);
    }
    .ion-dom-badge[data-tone="valid"] {
      border-color: rgba(16,185,129,0.45);
      color: rgba(190,255,230,0.92);
    }
    .ion-dom-badge[data-tone="blocked"],
    .ion-dom-badge[data-tone="duplicate"] {
      border-color: rgba(251,191,36,0.45);
      color: rgba(255,236,180,0.92);
    }
    .ion-dom-badge[data-tone="duplicate"] {
      border-color: rgba(248,113,113,0.50);
      color: rgba(255,210,210,0.92);
    }
    [data-ion-code-index] {
      outline: 1px solid rgba(255,255,255,0.05);
      outline-offset: 3px;
    }
    [data-ion-yaml-status="valid"] {
      outline-color: rgba(16,185,129,0.42);
    }
    [data-ion-yaml-status="blocked"],
    [data-ion-yaml-status="duplicate"] {
      outline-color: rgba(251,191,36,0.42);
    }
    [data-ion-control-role] {
      position: relative;
      box-shadow: 0 0 0 1px rgba(255,112,28,0.34), 0 0 0 4px rgba(255,112,28,0.07) !important;
      border-radius: 10px !important;
    }
    [data-ion-control-role="composer_input"] {
      box-shadow: 0 0 0 1px rgba(255,112,28,0.36), 0 0 0 5px rgba(255,112,28,0.06) !important;
    }
    [data-ion-control-role="attach_button"],
    [data-ion-control-role="voice_button"] {
      box-shadow: 0 0 0 1px rgba(52,211,153,0.28), 0 0 0 4px rgba(52,211,153,0.06) !important;
    }
    [data-ion-control-role="send_button"] {
      box-shadow: 0 0 0 1px rgba(251,191,36,0.42), 0 0 0 4px rgba(251,191,36,0.07) !important;
    }
    [data-ion-control-role="source_plane"],
    [data-ion-control-role="uploaded_attachment"] {
      box-shadow: 0 0 0 1px rgba(129,140,248,0.40), 0 0 0 4px rgba(129,140,248,0.07) !important;
    }
  `;
    document.documentElement.appendChild(style);
  }

  function registryText(node, mode) {
    if (mode === "auto") return node.textContent ?? "";
    const inner = typeof node.innerText === "string" ? node.innerText : "";
    return inner || node.textContent || "";
  }

  function registryRectVisible(node) {
    if (shouldIgnoreScanNode(node)) return false;
    const rect = node.getBoundingClientRect();
    return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
  }

  function captureRectVisible(node) {
    if (node.closest(`#${PANEL_ID}`) || node.closest(`#${MODAL_ID}`)) return false;
    const rect = node.getBoundingClientRect();
    return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
  }

  function allowRegistryBadge(host) {
    const currentPosition = window.getComputedStyle(host).position;
    if (!currentPosition || currentPosition === "static") host.style.position = "relative";
  }

  function ensureRegistryBadge(host, kind, text, tone = "idle") {
    allowRegistryBadge(host);
    const existing = Array.from(host.children).find((child) => child.dataset?.ionBadge === kind);
    const badge = existing ?? document.createElement("span");
    badge.className = "ion-dom-badge";
    badge.dataset.ionBadge = kind;
    badge.dataset.tone = tone;
    if (badge.textContent !== text) badge.textContent = text;
    if (!existing) host.appendChild(badge);
  }

  function captureLabel(node) {
    return `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.textContent ?? ""}`.replace(/\s+/g, " ").trim();
  }

  function noteCapture(stats, node, role, status = "healthy", label = "") {
    node.dataset.ionControlRole = role;
    node.dataset.ionCaptureStatus = status;
    if (label) node.dataset.ionCaptureLabel = label.slice(0, 80);
    stats.composerCapture[role] = (stats.composerCapture[role] ?? 0) + 1;
  }

  function uniqueElements(selectors) {
    const elements = [];
    const seenElements = new Set();
    document.querySelectorAll(selectors).forEach((node) => {
      if (seenElements.has(node) || shouldIgnoreScanNode(node) || !registryRectVisible(node)) return;
      seenElements.add(node);
      elements.push(node);
    });
    return elements;
  }

  function annotateMessages(stats) {
    const nodes = uniqueElements("[data-message-author-role], article");
    nodes.forEach((node, index) => {
      const role = node.getAttribute("data-message-author-role") || "message";
      node.dataset.ionMessageIndex = String(index + 1);
      ensureRegistryBadge(node, "message", `ION msg ${index + 1} ${role}`, "idle");
    });
    stats.messages = nodes.length;
  }

  function codeBlockHosts() {
    const hosts = [];
    const seenHosts = new Set();
    document.querySelectorAll("pre, pre code, code, [class*='font-mono'], [class*='whitespace-pre'], [class*='overflow-x-auto']").forEach((node) => {
      if (shouldIgnoreScanNode(node) || !registryRectVisible(node)) return;
      const host = node.closest("pre") ?? node;
      if (seenHosts.has(host) || shouldIgnoreScanNode(host) || !registryRectVisible(host)) return;
      seenHosts.add(host);
      hosts.push(host);
    });
    return hosts;
  }

  function annotateCodeBlocks(stats, mode) {
    const actionIds = new Set();
    const hosts = codeBlockHosts();
    hosts.forEach((host, index) => {
      const label = `ION CODE #${index + 1}`;
      host.dataset.ionCodeIndex = String(index + 1);
      host.dataset.ionYamlStatus = "none";
      let tone = "idle";
      let badge = label;
      const text = registryText(host, mode);
      if (ION_ACTION_LINE.test(text) || extractIonActionYaml(text) !== null) {
        stats.yamlBlocks += 1;
        const parsed = parseIonActionYamlWithDiagnostics(text);
        const packet = parsed.packet;
        const actionId = packet?.ion_action?.action_id;
        if (!packet) {
          stats.invalidActions += 1;
          tone = "blocked";
          badge = `ION YAML #${index + 1} · blocked`;
          host.dataset.ionYamlStatus = "blocked";
          host.dataset.ionYamlFinding = parsed.finding ?? "parse_failed";
        } else if (actionId && actionIds.has(actionId)) {
          stats.duplicateActions += 1;
          tone = "duplicate";
          badge = `ION YAML #${index + 1} · duplicate`;
          host.dataset.ionYamlStatus = "duplicate";
          host.dataset.ionActionId = actionId;
        } else {
          if (actionId) actionIds.add(actionId);
          const local = localValidate(packet);
          host.dataset.ionActionId = actionId ?? "";
          if (local.accepted) {
            stats.validActions += 1;
            tone = "valid";
            badge = `ION YAML #${index + 1} · valid`;
            host.dataset.ionYamlStatus = "valid";
          } else {
            stats.invalidActions += 1;
            tone = "blocked";
            badge = `ION YAML #${index + 1} · blocked`;
            host.dataset.ionYamlStatus = "blocked";
            host.dataset.ionYamlFinding = local.findings.join("|");
          }
        }
      }
      if (!ION_ACTION_LINE.test(text) && extractIonActionYaml(text) === null) badge = `ION CODE #${index + 1}`;
      ensureRegistryBadge(host, "code", badge, tone);
    });
    stats.codeBlocks = hosts.length;
  }

  function annotateComposerControls(stats) {
    const composer = findComposer();
    const composerRect = composer?.getBoundingClientRect();
    if (composer && captureRectVisible(composer)) {
      noteCapture(stats, composer, "composer_input", "healthy", "composer input");
    }
    const controls = Array.from(document.querySelectorAll("button, [role='button'], input[type='file']")).filter((node) => {
      if (!captureRectVisible(node)) return false;
      const rect = node.getBoundingClientRect();
      const nearComposer = composerRect ? Math.abs(rect.top - composerRect.top) < 180 || Math.abs(rect.bottom - composerRect.bottom) < 180 : false;
      const label = captureLabel(node).toLowerCase();
      return nearComposer || /send|attach|upload|file|voice|mic|stop|plus/.test(label);
    });
    controls.forEach((node) => {
      const label = captureLabel(node).toLowerCase();
      const role =
        label.includes("send") ? "send_button" :
        label.includes("attach") || label.includes("upload") || label.includes("file") || label.includes("plus") ? "attach_button" :
        label.includes("mic") || label.includes("voice") ? "voice_button" :
        label.includes("stop") ? "stop_button" :
        /model|thinking|source|tool|github|drive/.test(label) ? "source_plane" :
        "composer_control";
      noteCapture(stats, node, role, role === "send_button" ? "approval_required" : "healthy", captureLabel(node));
    });
    const chips = Array.from(
      document.querySelectorAll(
        "img, [data-testid*='attachment' i], [data-testid*='upload' i], [data-testid*='file' i], [data-testid*='image' i], [aria-label*='remove' i], [aria-label*='file' i], [aria-label*='image' i], [class*='attachment' i]",
      ),
    ).filter((node) => {
      if (!captureRectVisible(node)) return false;
      const rect = node.getBoundingClientRect();
      return composerRect ? rect.bottom >= composerRect.top - 260 && rect.top <= composerRect.bottom + 120 : rect.top > window.innerHeight * 0.45;
    });
    chips.forEach((node) => {
      noteCapture(stats, node, "uploaded_attachment", "composer_expanded", captureLabel(node) || node.tagName.toLowerCase());
    });
    const sources = Array.from(
      document.querySelectorAll("button, [role='button'], [aria-label], [data-testid], [class*='chip' i], [class*='pill' i]"),
    ).filter((node) => {
      if (!captureRectVisible(node)) return false;
      const label = captureLabel(node);
      return /github|drive|source|tool|connector|memory|search/i.test(label) && (!composerRect || Math.abs(node.getBoundingClientRect().bottom - composerRect.bottom) < 320);
    });
    sources.forEach((node) => {
      const label = captureLabel(node) || "source";
      noteCapture(stats, node, "source_plane", "source_plane_only", label);
      if (!stats.selectedSources.includes(label)) stats.selectedSources.push(label);
    });
    stats.uploadedAttachments = chips.length;
    stats.composerControls = Object.values(stats.composerCapture).reduce((sum, count) => sum + count, 0);
  }

  function updateDomActionRegistry(mode = "manual") {
    ensureDomRegistryStyle();
    const stats = {
      messages: 0,
      codeBlocks: 0,
      yamlBlocks: 0,
      validActions: 0,
      invalidActions: 0,
      duplicateActions: 0,
      composerControls: 0,
      composerCapture: {},
      selectedSources: [],
      uploadedAttachments: 0,
      lastUpdated: new Date().toLocaleTimeString(),
    };
    if (mode === "manual") annotateMessages(stats);
    annotateCodeBlocks(stats, mode);
    if (mode === "manual") annotateComposerControls(stats);
    setBridgeDiagnosticsDetail(
      [
        "DOM action registry",
        `messages: ${stats.messages}`,
        `code_blocks: ${stats.codeBlocks}`,
        `ion_yaml_blocks: ${stats.yamlBlocks}`,
        `valid_actions: ${stats.validActions}`,
      `invalid_actions: ${stats.invalidActions}`,
      `duplicate_actions: ${stats.duplicateActions}`,
      `composer_controls: ${stats.composerControls}`,
      `uploaded_attachments: ${stats.uploadedAttachments}`,
      `capture_roles: ${Object.entries(stats.composerCapture).map(([role, count]) => `${role}=${count}`).join(", ") || "none"}`,
      `selected_sources: ${stats.selectedSources.join(", ") || "none"}`,
      `scan_mode: ${mode}`,
      `last_updated: ${stats.lastUpdated}`,
        "",
        "Automation markers are visual only. They do not click, submit, upload, or mutate ION state.",
      ].join("\n"),
    );
    return stats;
  }

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
        z-index: 2147483646;
        inset: 0;
        box-sizing: border-box;
        pointer-events: none;
      }
      #${PANEL_ID} .ion-top-rail,
      #${PANEL_ID} .ion-composer-cockpit {
        position: fixed;
        box-sizing: border-box;
        pointer-events: auto;
      }
      #${PANEL_ID} .ion-top-rail {
        display: flex;
        align-items: center;
        gap: 6px;
        min-height: 30px;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        background: rgba(33, 33, 33, 0.78);
        box-shadow: 0 6px 18px rgba(0,0,0,0.18);
        padding: 2px 4px;
        backdrop-filter: blur(12px);
      }
      #${PANEL_ID}[data-anchor-health="degraded"] .ion-top-rail {
        border-color: rgba(251,191,36,0.28);
      }
      #${PANEL_ID} .ion-composer-cockpit {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        gap: 0;
        max-width: calc(100vw - 24px);
        pointer-events: none;
      }
      #${PANEL_ID}[data-anchor-mode="topbar_fallback"] .ion-composer-cockpit {
        pointer-events: auto;
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
        max-width: 220px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
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
        border: 1px solid transparent;
        color: rgba(255,255,255,0.82);
        background: transparent;
        padding: 0 8px;
        font-size: 12px;
        font-weight: 500;
        line-height: 1;
        cursor: pointer;
      }
      #${PANEL_ID} .ion-tool {
        height: 26px;
        border-radius: 8px;
      }
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
      #${PANEL_ID}[data-layout="compact"] .ion-title {
        max-width: 150px;
      }
      #${PANEL_ID}[data-layout="compact"] .ion-label {
        display: none;
      }
      #${PANEL_ID}[data-layout="compact"] .ion-tool,
      #${PANEL_ID}[data-layout="compact"] .ion-toggle {
        height: 27px;
        padding: 0 6px;
        font-size: 11px;
      }
      #${PANEL_ID}[data-layout="tiny"] .ion-row > div {
        display: none;
      }
      #${PANEL_ID}[data-layout="tiny"] .ion-tool {
        padding: 0 5px;
        font-size: 0;
      }
      #${PANEL_ID}[data-layout="tiny"] .ion-tool::first-letter,
      #${PANEL_ID}[data-layout="tiny"] .ion-toggle {
        font-size: 11px;
      }
      #${PANEL_ID}[data-layout="tiny"] [data-tool="insert-reentry"] {
        display: none;
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
      #${PANEL_ID} .ion-tabs {
        display: flex;
        gap: 3px;
        align-items: flex-end;
        overflow-x: auto;
        scrollbar-width: none;
        margin: 0;
        padding: 0 0 0 8px;
        pointer-events: auto;
      }
      #${PANEL_ID} .ion-tabs::-webkit-scrollbar {
        display: none;
      }
      #${PANEL_ID}[data-expanded="true"] .ion-expanded {
        display: block;
        border: 1px solid rgba(255,112,28,0.82);
        border-bottom: 0;
        border-radius: 14px 14px 0 0;
        background: rgba(24, 24, 24, 0.96);
        box-shadow: 0 -16px 46px rgba(0,0,0,0.34), 0 -1px 12px rgba(255,112,28,0.15);
        backdrop-filter: blur(14px);
        margin: 0;
        padding: 10px 10px 11px;
        max-height: min(38vh, 360px);
        overflow: auto;
        pointer-events: auto;
      }
      #${PANEL_ID}[data-expanded="true"] .ion-tab-panel[data-active="true"] {
        display: flex;
      }
      #${PANEL_ID}[data-anchor-mode="topbar_fallback"][data-expanded="true"] .ion-expanded {
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 10px 10px 0 0;
        box-shadow: 0 10px 28px rgba(0,0,0,0.26);
      }
      #${PANEL_ID} .ion-tab {
        height: 22px;
        max-width: 118px;
        border: 1px solid rgba(255,112,28,0.70);
        border-bottom: 0;
        border-radius: 8px 8px 0 0;
        background: rgba(32,32,32,0.96);
        color: #ffb27a;
        padding: 0 9px;
        font-size: 11px;
        line-height: 21px;
        box-shadow: 0 -1px 8px rgba(255,112,28,0.16);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        pointer-events: auto;
      }
      #${PANEL_ID} .ion-tab[data-active="true"] {
        color: #ffd2b0;
        background: rgba(255,112,28,0.16);
        border-color: rgba(255,112,28,0.95);
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
      #${PANEL_ID}[data-layout="compact"] .ion-tab {
        padding: 0 6px;
        max-width: 94px;
      }
      #${PANEL_ID}[data-layout="tiny"] .ion-tabs {
        display: none;
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

  function rectIsVisible(rect) {
    return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
  }

  function isBridgeElement(element) {
    return Boolean(element.closest(`#${PANEL_ID}`) ?? element.closest(`#${MODAL_ID}`));
  }

  function visibleRect(element) {
    if (isBridgeElement(element)) return null;
    const style = window.getComputedStyle(element);
    if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) return null;
    const rect = element.getBoundingClientRect();
    return rectIsVisible(rect) ? rect : null;
  }

  function detectLeftBoundary() {
    const selectors = [
      "nav",
      "aside",
      "[role='navigation']",
      "[aria-label*='sidebar' i]",
      "[aria-label*='side bar' i]",
      "[data-testid*='sidebar' i]",
      "[data-testid*='left' i]",
      "[class*='sidebar' i]",
      "[class*='side-bar' i]",
    ];
    let boundary = DEFAULT_LEFT_BOUNDARY;
    document.querySelectorAll(selectors.join(",")).forEach((element) => {
      const rect = visibleRect(element);
      if (!rect) return;
      const plausibleLeftSurface =
        rect.left <= 24 &&
        rect.top <= 92 &&
        rect.bottom >= 34 &&
        rect.width >= 38 &&
        rect.width <= window.innerWidth * 0.72;
      if (plausibleLeftSurface) boundary = Math.max(boundary, rect.right);
    });
    return Math.min(Math.max(boundary, DEFAULT_LEFT_BOUNDARY), window.innerWidth - 120);
  }

  function detectRightBoundary() {
    let boundary = window.innerWidth - TOP_BAR_GAP;
    const selectors = [
      "header button",
      "header a[role='button']",
      "[role='banner'] button",
      "[role='banner'] a[role='button']",
      "button[aria-label*='share' i]",
      "button[aria-label*='more' i]",
      "button[aria-label*='memory' i]",
      "[data-testid*='share' i]",
      "[data-testid*='more' i]",
    ];
    document.querySelectorAll(selectors.join(",")).forEach((element) => {
      const rect = visibleRect(element);
      if (!rect) return;
      const plausibleRightTopControl =
        rect.top <= 82 &&
        rect.bottom >= 16 &&
        rect.left >= window.innerWidth * 0.48 &&
        rect.width <= 180 &&
        rect.height <= 56;
      if (plausibleRightTopControl) boundary = Math.min(boundary, rect.left);
    });
    if (boundary === window.innerWidth - TOP_BAR_GAP) {
      boundary = Math.max(TOP_BAR_GAP, window.innerWidth - DEFAULT_RIGHT_RESERVE);
    }
    return Math.max(boundary, 160);
  }

  function topRail(panel) {
    return panel.querySelector(".ion-top-rail");
  }

  function composerCockpit(panel) {
    return panel.querySelector(".ion-composer-cockpit");
  }

  function topBarGeometry() {
    const left = Math.ceil(detectLeftBoundary() + TOP_BAR_GAP);
    const right = Math.floor(detectRightBoundary() - TOP_BAR_GAP);
    const available = Math.max(PANEL_TINY_WIDTH, right - left);
    const preferred = Math.min(PANEL_PREFERRED_WIDTH, Math.floor(window.innerWidth * 0.58));
    const width = Math.max(Math.min(preferred, available), Math.min(PANEL_MIN_WIDTH, available));
    const layout = width < PANEL_MIN_WIDTH ? "tiny" : width < 430 ? "compact" : "normal";
    return { left, available, width, layout };
  }

  function applyTopRailLayout(panel) {
    const { left, available, width } = topBarGeometry();
    const rail = topRail(panel);
    if (!rail) return;
    rail.style.top = `${PANEL_TOP}px`;
    rail.style.left = `${left}px`;
    rail.style.right = "auto";
    rail.style.bottom = "auto";
    rail.style.width = `${width}px`;
    rail.style.maxWidth = `${Math.max(PANEL_TINY_WIDTH, available)}px`;
    if (typeof panel.style.setProperty === "function") {
      panel.style.setProperty("--ion-chatops-modal-left", `${left}px`);
      panel.style.setProperty("--ion-chatops-modal-width", `${Math.min(420, available)}px`);
    }
  }

  function applyTopBarLayout(panel) {
    const { left, available, width, layout } = topBarGeometry();
    const cockpit = composerCockpit(panel);
    panel.dataset.anchorMode = "topbar_fallback";
    panel.dataset.anchorHealth = "degraded";
    panel.dataset.layout = layout;
    applyTopRailLayout(panel);
    if (cockpit) {
      cockpit.style.top = `${PANEL_TOP + 36}px`;
      cockpit.style.left = `${left}px`;
      cockpit.style.right = "auto";
      cockpit.style.bottom = "auto";
      cockpit.style.width = `${width}px`;
      cockpit.style.maxWidth = `${Math.max(PANEL_TINY_WIDTH, available)}px`;
    }
    if (typeof panel.style.setProperty === "function") {
      panel.style.setProperty("--ion-chatops-modal-left", `${left}px`);
      panel.style.setProperty("--ion-chatops-modal-width", `${Math.min(420, available)}px`);
    }
    positionApprovalModal();
  }

  function viewportHeight() {
    return Math.floor(window.visualViewport?.height ?? window.innerHeight);
  }

  function findComposerInput() {
    const selectors = [
      "#prompt-textarea",
      "textarea",
      "[contenteditable='true'][role='textbox']",
      "[contenteditable='true']",
    ];
    for (const selector of selectors) {
      const node = document.querySelector(selector);
      if (!node || isBridgeElement(node)) continue;
      const rect = visibleRect(node);
      if (rect && rect.top > viewportHeight() * 0.45) return node;
    }
    return null;
  }

  function elementContains(parent, child) {
    let current = child;
    while (current) {
      if (current === parent) return true;
      current = current.parentElement;
    }
    return false;
  }

  function lowerViewportElement(element) {
    const rect = visibleRect(element);
    if (!rect) return false;
    return rect.bottom > viewportHeight() * 0.58 && rect.top > viewportHeight() * 0.25;
  }

  function composerButtonCount(element) {
    return Array.from(element.querySelectorAll("button, [role='button']")).filter((node) => {
      const rect = visibleRect(node);
      if (!rect) return false;
      const label = `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.textContent ?? ""}`.toLowerCase();
      return /send|attach|upload|file|voice|mic|audio|plus|stop|model|tool|source|github|drive/.test(label);
    }).length;
  }

  function composerAttachmentNodes(input) {
    const inputRect = input.getBoundingClientRect();
    const selectors = [
      "img",
      "video",
      "[data-testid*='attachment' i]",
      "[data-testid*='upload' i]",
      "[data-testid*='file' i]",
      "[data-testid*='image' i]",
      "[aria-label*='remove' i]",
      "[aria-label*='attachment' i]",
      "[aria-label*='uploaded' i]",
      "[aria-label*='file' i]",
      "[aria-label*='image' i]",
      "[class*='attachment' i]",
      "[class*='file' i]",
    ].join(",");
    const nodes = [];
    const seen = new Set();
    document.querySelectorAll(selectors).forEach((node) => {
      if (seen.has(node) || isBridgeElement(node)) return;
      seen.add(node);
      const rect = visibleRect(node);
      if (!rect) return;
      const nearInputX = rect.right >= inputRect.left - 80 && rect.left <= inputRect.right + 80;
      const nearInputY = rect.bottom >= inputRect.top - 260 && rect.top <= inputRect.bottom + 80;
      if (lowerViewportElement(node) && nearInputX && nearInputY) nodes.push(node);
    });
    return nodes;
  }

  function candidateComposerContainer(input) {
    let best = null;
    let current = input;
    let depth = 0;
    const leftBoundary = detectLeftBoundary();
    const attachmentNodes = composerAttachmentNodes(input);
    while (current?.parentElement && depth < 14) {
      current = current.parentElement;
      depth += 1;
      if (isBridgeElement(current)) break;
      const rect = visibleRect(current);
      if (!rect) continue;
      const bottomHalf = rect.bottom > viewportHeight() * 0.58 && rect.top > viewportHeight() * 0.22;
      const respectsSidebar = rect.left >= Math.max(0, leftBoundary - 12);
      const plausibleWidth =
        rect.width >= Math.min(320, window.innerWidth * 0.42) &&
        rect.width <= Math.min(window.innerWidth * 0.90, window.innerWidth - leftBoundary - 16);
      const plausibleHeight = rect.height >= 36 && rect.height <= Math.max(420, viewportHeight() * 0.48);
      if (!bottomHalf || !respectsSidebar || !plausibleWidth || !plausibleHeight) continue;
      const containsAttachments = attachmentNodes.every((node) => elementContains(current, node));
      if (attachmentNodes.length && !containsAttachments) continue;
      const buttons = composerButtonCount(current);
      const radius = Number.parseFloat(window.getComputedStyle(current).borderRadius || "0") || 0;
      const score =
        (buttons >= 2 ? 0 : 60) +
        (radius >= 10 ? 0 : 16) +
        (attachmentNodes.length ? 0 : 6) +
        rect.width / 100 +
        rect.height / 44 +
        depth * 0.35;
      if (!best || score < best.score) best = { element: current, score };
    }
    return best?.element ?? input;
  }

  function observeComposerAnchor(element) {
    if (typeof ResizeObserver === "undefined") return;
    if (observedComposerElement === element) return;
    composerResizeObserver?.disconnect();
    observedComposerElement = element;
    if (!element) return;
    composerResizeObserver = new ResizeObserver(() => {
      window.requestAnimationFrame?.(() => refreshBridgePosition()) ?? window.setTimeout(() => refreshBridgePosition(), 0);
    });
    composerResizeObserver.observe(element);
  }

  function detectComposerAnchor() {
    const input = findComposerInput();
    if (!input) {
      observeComposerAnchor(null);
      return {
        mode: "topbar_fallback",
        rect: null,
        element: null,
        health: "degraded",
        detail: "Composer anchor not found; using top-bar fallback layout.",
        source: "not_found",
        attachmentsDetected: 0,
      };
    }
    const attachments = composerAttachmentNodes(input);
    const container = candidateComposerContainer(input);
    const rect = container.getBoundingClientRect();
    if (!rectIsVisible(rect)) {
      observeComposerAnchor(null);
      return {
        mode: "topbar_fallback",
        rect: null,
        element: null,
        health: "degraded",
        detail: "Composer candidate was not visible; using top-bar fallback layout.",
        source: "candidate_not_visible",
        attachmentsDetected: attachments.length,
      };
    }
    observeComposerAnchor(container);
    return {
      mode: "composer",
      rect,
      element: container,
      health: "ready",
      source: attachments.length ? "full_composer_shell_with_attachments" : "full_composer_shell",
      attachmentsDetected: attachments.length,
      detail: [
        `Composer anchor ready: ${Math.round(rect.left)},${Math.round(rect.top)} ${Math.round(rect.width)}x${Math.round(rect.height)}.`,
        `source: ${attachments.length ? "full_composer_shell_with_attachments" : "full_composer_shell"}`,
        `attachments_detected: ${attachments.length}`,
      ].join("\n"),
    };
  }

  function applyComposerLayout(panel, anchor) {
    if (anchor.mode !== "composer" || !anchor.rect) return false;
    const rect = anchor.rect;
    const viewport = viewportHeight();
    const margin = 12;
    const left = Math.max(margin, Math.round(rect.left));
    const available = Math.max(PANEL_TINY_WIDTH, Math.min(Math.round(rect.width), window.innerWidth - left - margin));
    const width = available;
    const bottom = Math.max(4, Math.round(viewport - rect.top + 2));
    const layout = width < PANEL_MIN_WIDTH ? "tiny" : width < 520 ? "compact" : "normal";
    const cockpit = composerCockpit(panel);
    panel.dataset.anchorMode = "composer";
    panel.dataset.anchorHealth = anchor.health;
    panel.dataset.layout = layout;
    if (cockpit) {
      cockpit.style.top = "auto";
      cockpit.style.left = `${left}px`;
      cockpit.style.right = "auto";
      cockpit.style.bottom = `${bottom}px`;
      cockpit.style.width = `${width}px`;
      cockpit.style.maxWidth = `${available}px`;
    }
    positionApprovalModal();
    return true;
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
      <div class="ion-top-rail">
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
        </div>
      </div>
      <div class="ion-composer-cockpit">
        <div class="ion-expanded">
          <div class="ion-tab-panel" data-panel="status"><div class="ion-detail" data-field="status"></div></div>
          <div class="ion-tab-panel" data-panel="action"><div class="ion-detail" data-field="action"></div></div>
          <div class="ion-tab-panel" data-panel="agent">
            <div class="ion-detail" data-field="agent"></div>
            <div class="ion-toolbar-actions">
              <button type="button" class="ion-tool" data-tool="agent-status">Status</button>
              <button type="button" class="ion-tool" data-tool="agent-queue">Queue</button>
              <button type="button" class="ion-tool" data-tool="agent-preview">Preview Next</button>
              <button type="button" class="ion-tool" data-tool="agent-latest">Latest Runs</button>
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
          <div class="ion-tab-panel" data-panel="sandbox">
            <div class="ion-detail" data-field="sandbox"></div>
            <div class="ion-toolbar-actions">
              <button type="button" class="ion-tool" data-tool="sandbox-returns">Returns</button>
              <button type="button" class="ion-tool" data-tool="sandbox-diff">Diff Preview</button>
              <button type="button" class="ion-tool" data-tool="sandbox-review">Queue Review</button>
            </div>
          </div>
          <div class="ion-tab-panel" data-panel="automation"><div class="ion-detail" data-field="automation"></div></div>
          <div class="ion-tab-panel" data-panel="artifacts">
            <div class="ion-detail" data-field="artifacts"></div>
            <div class="ion-toolbar-actions">
              <button type="button" class="ion-tool" data-tool="artifact-attachables">Attachables</button>
              <button type="button" class="ion-tool" data-tool="artifact-drop-latest">Drop Latest</button>
              <button type="button" class="ion-tool" data-tool="artifact-local-attach">Local Attach</button>
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
        <div class="ion-tabs">
          <button type="button" class="ion-tab" data-tab="status">Status</button>
          <button type="button" class="ion-tab" data-tab="action">Action</button>
          <button type="button" class="ion-tab" data-tab="agent">Agent</button>
          <button type="button" class="ion-tab" data-tab="packages">Packages</button>
          <button type="button" class="ion-tab" data-tab="sandbox">Sandbox</button>
          <button type="button" class="ion-tab" data-tab="automation">Automation</button>
          <button type="button" class="ion-tab" data-tab="artifacts">Artifacts</button>
          <button type="button" class="ion-tab" data-tab="diagnostics">Diagnostics</button>
          <button type="button" class="ion-tab" data-tab="tools">Logs</button>
        </div>
      </div>
    `;
    document.documentElement.appendChild(panel);
    panel.querySelectorAll(".ion-tab").forEach((tab) => {
      tab.addEventListener("click", () => {
        const nextTab = tab.dataset.tab ?? "status";
        if (panel.dataset.expanded === "true" && panel.dataset.tab === nextTab) {
          panel.dataset.expanded = "false";
        } else {
          panel.dataset.expanded = "true";
          panel.dataset.tab = nextTab;
        }
        renderPanel(panel);
      });
    });
    if (typeof document.addEventListener === "function") {
      document.addEventListener("keydown", (event) => {
        if (event.key !== "Escape") return;
        panel.dataset.expanded = "false";
        renderPanel(panel);
      });
    }
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
    panel.querySelector('[data-tool="agent-preview"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-agent-preview"));
    });
    panel.querySelector('[data-tool="agent-latest"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-agent-latest"));
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
    panel.querySelector('[data-tool="sandbox-returns"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-sandbox-returns"));
    });
    panel.querySelector('[data-tool="sandbox-diff"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-sandbox-diff"));
    });
    panel.querySelector('[data-tool="sandbox-review"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-sandbox-review"));
    });
    panel.querySelector('[data-tool="artifact-attachables"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-artifact-attachables"));
    });
    panel.querySelector('[data-tool="artifact-drop-latest"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-artifact-drop-latest"));
    });
    panel.querySelector('[data-tool="artifact-local-attach"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-artifact-local-attach"));
    });
    panel.querySelector('[data-tool="collapse"]')?.addEventListener("click", () => {
      panel.dataset.expanded = "false";
      renderPanel(panel);
    });
    renderPanel(panel);
    return panel;
  }

  function positionPanelAboveComposer(panel = ensurePanel()) {
    const anchor = detectComposerAnchor();
    bridgeState.anchor = anchor;
    applyTopRailLayout(panel);
    if (!applyComposerLayout(panel, anchor)) applyTopBarLayout(panel);
  }

  function positionApprovalModal(modal = document.getElementById(MODAL_ID)) {
    const panel = document.getElementById(PANEL_ID);
    if (!modal || !panel) return;
    const anchorElement =
      panel.dataset.expanded === "true"
        ? composerCockpit(panel) ?? topRail(panel)
        : topRail(panel) ?? composerCockpit(panel);
    const rect = (anchorElement ?? panel).getBoundingClientRect();
    const available = Math.max(PANEL_TINY_WIDTH, window.innerWidth - rect.left - TOP_BAR_GAP);
    modal.style.left = `${rect.left}px`;
    modal.style.width = `${Math.min(420, available)}px`;
    modal.style.maxWidth = `${Math.max(PANEL_TINY_WIDTH, available)}px`;
    if (panel.dataset.anchorMode === "composer") {
      modal.style.top = "auto";
      modal.style.bottom = `${Math.max(12, viewportHeight() - rect.top + TOP_BAR_GAP)}px`;
    } else {
      modal.style.bottom = "auto";
      modal.style.top = `${Math.max(48, rect.bottom + TOP_BAR_GAP)}px`;
    }
  }

  function renderPanel(panel = ensurePanel()) {
    panel.dataset.tone = bridgeState.tone;
    positionPanelAboveComposer(panel);
    const titleNode = panel.querySelector(".ion-title");
    if (titleNode) titleNode.textContent = bridgeState.title;
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
    const sandboxNode = panel.querySelector('[data-field="sandbox"]');
    const automationNode = panel.querySelector('[data-field="automation"]');
    const artifactsNode = panel.querySelector('[data-field="artifacts"]');
    const diagnosticsNode = panel.querySelector('[data-field="diagnostics"]');
    const toolsNode = panel.querySelector('[data-field="tools"]');
    if (statusNode) statusNode.textContent = bridgeState.detail;
    if (actionNode) actionNode.textContent = bridgeState.action;
    if (agentNode) agentNode.textContent = bridgeState.agent;
    if (packagesNode) packagesNode.textContent = bridgeState.packages;
    if (sandboxNode) sandboxNode.textContent = bridgeState.sandbox;
    if (automationNode) automationNode.textContent = bridgeState.automation;
    if (artifactsNode) artifactsNode.textContent = bridgeState.artifacts;
    if (diagnosticsNode) diagnosticsNode.textContent = `${bridgeState.anchor.detail}\n\n${bridgeState.diagnostics}`;
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

  function setBridgeSandboxDetail(detail) {
    bridgeState.sandbox = detail;
    renderPanel();
  }

  function setBridgeArtifactDetail(detail) {
    bridgeState.artifacts = detail;
    renderPanel();
  }

  function setBridgeDiagnosticsDetail(detail) {
    bridgeState.diagnostics = detail;
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
      positionApprovalModal(modal);
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
      positionApprovalModal(modal);
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

  function candidateBlocks(mode = "manual") {
    const selectors = mode === "auto" ? AUTO_SCAN_SELECTORS : MANUAL_SCAN_SELECTORS;
    const nodes = [];
    const seenNodes = new Set();
    for (const selector of selectors) {
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
        mode === "manual" && typeof node.innerText === "string" ? node.innerText : "",
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

  function formatBytes(value) {
    const bytes = Number(value);
    if (!Number.isFinite(bytes) || bytes < 0) return "unknown size";
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KiB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MiB`;
  }

  function summarizeAttachables(result) {
    const rows = Array.isArray(result?.candidates) ? result.candidates : [];
    const attachables = rows.filter((row) => row?.attachable && typeof row.path === "string");
    if (!attachables.length) return "No attachable package or sandbox-return artifact is available.";
    const selected = attachables[0];
    const lines = [
      `attachable_count: ${attachables.length}`,
      "selected_latest:",
      `  name: ${selected.name ?? "unknown"}`,
      `  path: ${selected.path}`,
      `  size: ${formatBytes(selected.size_bytes)}`,
      `  sha256: ${selected.sha256 ?? ""}`,
    ];
    if (attachables.length > 1) {
      lines.push("", "other_attachables:");
      attachables.slice(1, 4).forEach((row, index) => {
        lines.push(`  ${index + 2}. ${row.name ?? row.path} (${formatBytes(row.size_bytes)})`);
      });
    }
    lines.push("", "Use Local Attach for OS file-picker assist, or Drop Latest for browser synthetic drop. Neither clicks Send.");
    return lines.join("\n");
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

  function inactiveQueueStatus(status) {
    return /SUPERSEDED|FULFILLED|INVALID|ARCHIVE_ONLY|SETTLED|DUPLICATE|BLOCKED|CANCELLED/i.test(status);
  }

  function firstActionableRequest(queue) {
    const rows = Array.isArray(queue?.requests) ? queue.requests : [];
    return rows.find((row) => !inactiveQueueStatus(String(row?.status ?? ""))) ?? null;
  }

  function requestAgentPreview() {
    setBridgeStatus("Agent preview", "Reading queue/status before any Codex mutation.", "working");
    chrome.runtime.sendMessage({ type: "ion_chatops_agent_status" }, (statusResponse) => {
      chrome.runtime.sendMessage({ type: "ion_chatops_agent_queue" }, async (queueResponse) => {
        if (!statusResponse?.ok || !queueResponse?.ok) {
          const detail = !statusResponse?.ok ? blockedDetail(statusResponse) : blockedDetail(queueResponse);
          setBridgeAgentDetail(detail);
          setBridgeStatus("Agent preview blocked", detail, "error");
          return;
        }
        const status = statusResponse.result;
        const queue = queueResponse.result;
        const request = firstActionableRequest(queue);
        const detail = [
          "Codex agent preview",
          `runner_verdict: ${status?.verdict ?? ""}`,
          `queued_request_count: ${status?.queued_request_count ?? 0}`,
          `active_process_running: ${Boolean(status?.active_process_running)}`,
          `next_request_path: ${status?.next_request_path ?? "none"}`,
          request
            ? `next_actionable_request: ${request.request_id ?? ""}\nstatus: ${request.status ?? ""}\nobjective: ${request.objective ?? ""}`
            : "next_actionable_request: none",
          "",
          "Preview only. No Codex worker was prepared or started.",
        ].join("\n");
        setBridgeAgentDetail(detail);
        setBridgeStatus("Agent preview ready", detail.split("\n")[1] ?? "", "success");
        await copyBridgeResult("Agent preview", detail);
      });
    });
  }

  function requestAgentLatestRuns() {
    setBridgeStatus("Latest Codex runs", "Reading latest Codex queue runner receipts.", "working");
    chrome.runtime.sendMessage({ type: "ion_chatops_agent_status" }, async (response) => {
      if (!response?.ok) {
        const detail = blockedDetail(response);
        setBridgeAgentDetail(detail);
        setBridgeStatus("Latest Codex runs blocked", detail, "error");
        return;
      }
      const runs = Array.isArray(response.result?.latest_runs) ? response.result.latest_runs : [];
      const detail = runs.length
        ? runs
          .slice(0, 6)
          .map((run, index) => [
            `#${index + 1} ${run.status ?? ""}`,
            `run_id: ${run.run_id ?? ""}`,
            `request_id: ${run.request_id ?? ""}`,
            `path: ${run.path ?? ""}`,
          ].join("\n"))
          .join("\n\n")
        : "No Codex queue runs found.";
      setBridgeAgentDetail(detail);
      setBridgeStatus("Latest Codex runs ready", runs[0]?.status ?? "No runs found.", "success");
      await copyBridgeResult("Latest Codex runs", detail);
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

  function latestSandboxReturnId(result) {
    const rows = Array.isArray(result?.returns) ? result.returns : [];
    const first = rows.find((row) => typeof row?.return_id === "string" && row.return_id.trim());
    return first?.return_id ?? null;
  }

  function requestSandboxReturns() {
    setBridgeStatus("Sandbox returns", "Fetching ChatGPT sandbox return queue.", "working");
    chrome.runtime.sendMessage({ type: "ion_chatops_sandbox_returns" }, async (response) => {
      const detail = response?.ok ? compactJson(response.result) : blockedDetail(response);
      setBridgeSandboxDetail(detail);
      setBridgeStatus(response?.ok ? "Sandbox returns ready" : "Sandbox returns blocked", detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
      if (response?.ok) await copyBridgeResult("Sandbox returns", detail);
    });
  }

  function requestSandboxMutation(type, label) {
    setBridgeStatus(label, "Requesting latest sandbox return projection before approval.", "working");
    chrome.runtime.sendMessage({ type: "ion_chatops_sandbox_returns" }, (queueResponse) => {
      const returnId = latestSandboxReturnId(queueResponse?.result);
      if (!queueResponse?.ok || !returnId) {
        const detail = queueResponse?.ok ? "No sandbox returns are available." : blockedDetail(queueResponse);
        setBridgeSandboxDetail(detail);
        setBridgeStatus(`${label} blocked`, detail, "error");
        return;
      }
      chrome.runtime.sendMessage({ type, payload: { return_id: returnId } }, async (response) => {
        const detail = response?.ok ? compactJson(response.result) : blockedDetail(response);
        setBridgeSandboxDetail(detail);
        setBridgeStatus(response?.ok ? `${label} submitted` : `${label} blocked`, detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
        if (response?.ok) await copyBridgeResult(label, detail);
      });
    });
  }

  function requestArtifactAttachables() {
    setBridgeStatus("Attachables", "Reading local packages and sandbox return artifacts.", "working");
    chrome.runtime.sendMessage({ type: "ion_chatops_artifact_attachables" }, async (response) => {
      const detail = response?.ok ? summarizeAttachables(response.result) : blockedDetail(response);
      setBridgeArtifactDetail(detail);
      setBridgeStatus(response?.ok ? "Attachables ready" : "Attachables blocked", detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
      if (response?.ok) await copyBridgeResult("Attachable artifacts", detail);
    });
  }

  function findDropTarget() {
    const composer = findComposer();
    if (!composer) return null;
    return (
      composer.closest("form") ??
      composer.closest("[data-testid*='composer']") ??
      composer.closest("main") ??
      composer
    );
  }

  function composerRect() {
    const composer = findComposer();
    return composer?.getBoundingClientRect() ?? null;
  }

  function controlLabel(node) {
    return `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.textContent ?? ""}`.replace(/\s+/g, " ").trim();
  }

  function visibleElement(node) {
    const rect = node.getBoundingClientRect();
    return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
  }

  function findAttachControlRect() {
    const rect = composerRect();
    const nodes = Array.from(document.querySelectorAll("button, [role='button'], input[type='file']"));
    const candidate = nodes.find((node) => {
      if (!visibleElement(node)) return false;
      const label = controlLabel(node).toLowerCase();
      const bounds = node.getBoundingClientRect();
      const nearComposer = rect ? Math.abs(bounds.top - rect.top) < 220 || Math.abs(bounds.bottom - rect.bottom) < 220 : bounds.top > window.innerHeight * 0.45;
      return nearComposer && /attach|upload|file|plus|add/.test(label);
    });
    if (!candidate) return null;
    const bounds = candidate.getBoundingClientRect();
    const borderX = Math.max(0, (window.outerWidth - window.innerWidth) / 2);
    const chromeY = Math.max(0, window.outerHeight - window.innerHeight - borderX);
    const screenRect = {
      x: Math.round(window.screenX + borderX + bounds.left),
      y: Math.round(window.screenY + chromeY + bounds.top),
      width: Math.round(bounds.width),
      height: Math.round(bounds.height),
    };
    return {
      x: Math.round(bounds.left),
      y: Math.round(bounds.top),
      width: Math.round(bounds.width),
      height: Math.round(bounds.height),
      label: controlLabel(candidate),
      screen_rect: screenRect,
      coordinate_space: "viewport_css_pixels",
    };
  }

  function uploadedAttachmentCount() {
    const rect = composerRect();
    return Array.from(
      document.querySelectorAll(
        "img, [data-testid*='attachment' i], [data-testid*='upload' i], [data-testid*='file' i], [data-testid*='image' i], [aria-label*='remove' i], [aria-label*='file' i], [aria-label*='image' i], [class*='attachment' i]",
      ),
    ).filter((node) => {
      if (!visibleElement(node)) return false;
      const bounds = node.getBoundingClientRect();
      return rect ? bounds.bottom >= rect.top - 300 && bounds.top <= rect.bottom + 160 : bounds.top > window.innerHeight * 0.45;
    }).length;
  }

  function waitForUploadChip(previousCount, label, baseDetail) {
    const started = Date.now();
    const poll = () => {
      const count = uploadedAttachmentCount();
      if (count > previousCount) {
        const detail = `${baseDetail}\n\nupload_chip_verified: true\nuploaded_attachment_count: ${count}`;
        setBridgeArtifactDetail(detail);
        setBridgeStatus(`${label} verified`, "Upload chip/thumbnail detected. No Send click was performed.", "success");
        return;
      }
      if (Date.now() - started > 15000) {
        const detail = `${baseDetail}\n\nupload_chip_verified: false\nuploaded_attachment_count: ${count}\nfinding: upload_chip_not_observed_after_operator_attempt`;
        setBridgeArtifactDetail(detail);
        setBridgeStatus(`${label} unverified`, "Local helper returned, but no upload chip was observed yet. No Send click was performed.", "error");
        return;
      }
      window.setTimeout(poll, 600);
    };
    poll();
  }

  async function attemptPreparedArtifactDrop(result) {
    const downloadUrl = String(result?.download_url ?? "").trim();
    const filename = String(result?.filename ?? result?.artifact?.name ?? "ion-artifact.bin").trim();
    const contentType = String(result?.content_type ?? result?.artifact?.content_type ?? "application/octet-stream").trim();
    const target = findDropTarget();
    if (!downloadUrl || !target) {
      const detail = !downloadUrl ? "download_url_missing" : "chatgpt_drop_target_not_found";
      setBridgeArtifactDetail(detail);
      setBridgeStatus("Artifact drop blocked", detail, "error");
      return;
    }
    try {
      const response = await fetch(downloadUrl);
      if (!response.ok) throw new Error(`download_failed_${response.status}`);
      const blob = await response.blob();
      const file = new File([blob], filename, { type: contentType || blob.type || "application/octet-stream" });
      const transfer = new DataTransfer();
      transfer.items.add(file);
      for (const eventName of ["dragenter", "dragover", "drop"]) {
        const event = new DragEvent(eventName, {
          bubbles: true,
          cancelable: true,
          composed: true,
          dataTransfer: transfer,
        });
        target.dispatchEvent(event);
      }
      const detail = [
        "visible_browser_drop_attempted",
        `filename: ${filename}`,
        `size_bytes: ${file.size}`,
        `sha256: ${result?.sha256 ?? ""}`,
        `receipt_path: ${result?.receipt_path ?? ""}`,
        "",
        "If ChatGPT ignored the synthetic drop, use the manifest/hash above with the manual attach picker or the future native macro lane.",
        "No Send click was performed.",
      ].join("\n");
      setBridgeArtifactDetail(detail);
      setBridgeStatus("Artifact drop attempted", `${filename}\nNo Send click was performed.`, "success");
      await copyBridgeResult("Artifact drop receipt", detail);
    } catch (error) {
      const detail = `artifact_drop_failed: ${error instanceof Error ? error.message : String(error)}`;
      setBridgeArtifactDetail(detail);
      setBridgeStatus("Artifact drop failed", detail, "error");
    }
  }

  function requestArtifactDropLatest() {
    setBridgeStatus("Artifact drop latest", "Requesting Braden approval before preparing a browser drop ticket.", "working");
    chrome.runtime.sendMessage({ type: "ion_chatops_artifact_prepare_latest" }, async (response) => {
      const detail = response?.ok ? compactJson(response.result) : blockedDetail(response);
      setBridgeArtifactDetail(detail);
      if (!response?.ok) {
        setBridgeStatus("Artifact drop blocked", detail.split("\n")[0] ?? "", "error");
        return;
      }
      setBridgeStatus("Artifact ticket ready", "Attempting visible ChatGPT drag/drop. No Send click will occur.", "working");
      await attemptPreparedArtifactDrop(response.result);
    });
  }

  function requestArtifactLocalAttachLatest() {
    const targetRect = findAttachControlRect();
    const beforeCount = uploadedAttachmentCount();
    if (!targetRect) {
      const detail = "attach_control_not_detected\nOpen ChatGPT composer and use Diagnostics to confirm ION sees the attach/add-file control.";
      setBridgeArtifactDetail(detail);
      setBridgeStatus("Local attach blocked", detail, "error");
      return;
    }
    setBridgeStatus("Local attach latest", "Requesting approval for local operator artifact attachment. No Send click will occur.", "working");
    chrome.runtime.sendMessage({
      type: "ion_chatops_artifact_local_attach_latest",
      payload: {
        target_rect: targetRect,
        target_screen_rect: targetRect.screen_rect,
      },
    }, async (response) => {
      const detail = response?.ok ? compactJson(response.result) : blockedDetail(response);
      setBridgeArtifactDetail(detail);
      if (!response?.ok) {
        setBridgeStatus("Local attach blocked", detail.split("\n")[0] ?? "", "error");
        return;
      }
      await copyBridgeResult("Local artifact attach", detail);
      waitForUploadChip(beforeCount, "Local attach", detail);
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

  function scan(mode = "manual") {
    if (scanRunning) {
      scanQueued = true;
      return 0;
    }
    scanRunning = true;
    refreshBridgePosition();
    try {
      updateDomActionRegistry(mode);
      let processed = 0;
      for (const block of candidateBlocks(mode)) {
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
    } catch (error) {
      const detail = error instanceof Error ? error.message : String(error);
      console.warn("ION ChatOps scan failed", error);
      setBridgeStatus("ION scan degraded", detail, "error");
      setBridgeDiagnosticsDetail(`Scan failed in ${mode} mode.\n${detail}`);
      return 0;
    } finally {
      scanRunning = false;
      if (scanQueued) {
        scanQueued = false;
        scheduleScan("auto");
      }
    }
  }

  function mutationTouchesIonUi(mutation) {
    const isIonNode = (node) => {
      if (node.nodeType !== Node.ELEMENT_NODE) return false;
      const element = node;
      return Boolean(
        element.closest(`#${PANEL_ID}`) ||
          element.closest(`#${MODAL_ID}`) ||
          element.closest(`#${DOM_REGISTRY_STYLE_ID}`) ||
          element.id === PANEL_ID ||
          element.id === MODAL_ID ||
          element.id === DOM_REGISTRY_STYLE_ID ||
          element.closest(".ion-dom-badge")
      );
    };
    if (isIonNode(mutation.target)) return true;
    return Array.from(mutation.addedNodes).some(isIonNode) || Array.from(mutation.removedNodes).some(isIonNode);
  }

  function scheduleScan(mode = "auto") {
    if (scanTimer !== null) return;
    scanTimer = window.setTimeout(() => {
      scanTimer = null;
      scan(mode);
    }, SCAN_DEBOUNCE_MS);
  }

  function initializeBridge() {
    const observerRoot = document.body ?? document.documentElement;
    const observer = new MutationObserver((mutations) => {
      if (mutations.length && mutations.every(mutationTouchesIonUi)) return;
      scheduleScan("auto");
    });
    observer.observe(observerRoot, { childList: true, subtree: true });
    window.addEventListener("resize", () => refreshBridgePosition());
    if (typeof document.addEventListener === "function") {
      document.addEventListener("transitionend", (event) => {
        const target = event.target;
        if (target instanceof Element && shouldIgnoreScanNode(target)) return;
        refreshBridgePosition();
      }, true);
      document.addEventListener(
        "click",
        (event) => {
          const target = event.target;
          if (target instanceof Element && shouldIgnoreScanNode(target)) return;
          window.setTimeout(() => refreshBridgePosition(), 60);
          window.setTimeout(() => refreshBridgePosition(), 260);
        },
        true,
      );
    }
    setBridgeStatus("Monitoring ChatGPT", "Waiting for ion_action YAML blocks.", "idle");
    scheduleScan("auto");
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
    updateDomActionRegistry,
    submitActionText,
    refreshBridgePosition,
    rescan: () => {
      seen.clear();
      return scan("manual");
    },
    scheduleScan,
  };
  window.addEventListener("ion-chatops-rescan", () => {
    seen.clear();
    setBridgeStatus("Manual rescan", "Scanning rendered ChatGPT code blocks.", "working");
    const found = scan("manual");
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
  window.addEventListener("ion-chatops-agent-preview", () => {
    requestAgentPreview();
  });
  window.addEventListener("ion-chatops-agent-latest", () => {
    requestAgentLatestRuns();
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
  window.addEventListener("ion-chatops-sandbox-returns", () => {
    requestSandboxReturns();
  });
  window.addEventListener("ion-chatops-sandbox-diff", () => {
    requestSandboxMutation("ion_chatops_sandbox_diff_latest", "Sandbox diff preview");
  });
  window.addEventListener("ion-chatops-sandbox-review", () => {
    requestSandboxMutation("ion_chatops_sandbox_queue_latest", "Sandbox queue review");
  });
  window.addEventListener("ion-chatops-artifact-attachables", () => {
    requestArtifactAttachables();
  });
  window.addEventListener("ion-chatops-artifact-drop-latest", () => {
    requestArtifactDropLatest();
  });
  window.addEventListener("ion-chatops-artifact-local-attach", () => {
    requestArtifactLocalAttachLatest();
  });
  if (safeModeDisabled()) {
    console.info(`ION ChatOps Bridge disabled by ${SAFE_MODE_KEY}. Remove the flag and reload to re-enable.`);
  } else {
    initializeBridge();
  }
})();
