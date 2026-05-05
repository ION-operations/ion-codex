import {
  requestApproval,
  requestBridgeApproval,
  copyReceiptSummary,
  refreshBridgePosition,
  setBridgeActionDetail,
  setBridgeAgentDetail,
  setBridgeArtifactDetail,
  setBridgeDiagnosticsDetail,
  setBridgePackageDetail,
  setBridgeSandboxDetail,
  setBridgeStatus,
} from "./approval_ui";
import { extractIonActionYaml, localValidate, parseIonActionYamlWithDiagnostics, parseStrictIonActionYaml } from "./schema";

const seen = new Set<string>();
const inFlightActionIds = new Set<string>();
const submittedActionIds = new Set<string>();
const reportedBlockedActionIds = new Set<string>();
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

type DomRegistryStats = {
  messages: number;
  codeBlocks: number;
  yamlBlocks: number;
  validActions: number;
  invalidActions: number;
  duplicateActions: number;
  composerControls: number;
  composerCapture: Record<string, number>;
  selectedSources: string[];
  uploadedAttachments: number;
  lastUpdated: string;
};

type ScanMode = "auto" | "manual";

let scanTimer: number | null = null;
let scanRunning = false;
let scanQueued = false;

function safeModeDisabled(): boolean {
  try {
    const value = window.localStorage?.getItem(SAFE_MODE_KEY) ?? window.sessionStorage?.getItem(SAFE_MODE_KEY);
    return ["1", "true", "disabled", "off"].includes(String(value ?? "").trim().toLowerCase());
  } catch (_error) {
    return false;
  }
}

function ensureDomRegistryStyle(): void {
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

function registryText(node: Element, mode: ScanMode): string {
  if (mode === "auto") return node.textContent ?? "";
  const inner = typeof (node as HTMLElement).innerText === "string" ? (node as HTMLElement).innerText : "";
  return inner || node.textContent || "";
}

function registryRectVisible(node: Element): boolean {
  if (shouldIgnoreScanNode(node)) return false;
  const rect = node.getBoundingClientRect();
  return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
}

function captureRectVisible(node: Element): boolean {
  if (node.closest(`#${PANEL_ID}`) || node.closest(`#${MODAL_ID}`)) return false;
  const rect = node.getBoundingClientRect();
  return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
}

function allowRegistryBadge(host: HTMLElement): void {
  const currentPosition = window.getComputedStyle(host).position;
  if (!currentPosition || currentPosition === "static") host.style.position = "relative";
}

function ensureRegistryBadge(host: HTMLElement, kind: string, text: string, tone = "idle"): void {
  allowRegistryBadge(host);
  const existing = Array.from(host.children).find((child) => (child as HTMLElement).dataset?.ionBadge === kind) as HTMLElement | undefined;
  const badge = existing ?? document.createElement("span");
  badge.className = "ion-dom-badge";
  badge.dataset.ionBadge = kind;
  badge.dataset.tone = tone;
  if (badge.textContent !== text) badge.textContent = text;
  if (!existing) host.appendChild(badge);
}

function captureLabel(node: HTMLElement): string {
  return `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.textContent ?? ""}`.replace(/\s+/g, " ").trim();
}

function noteCapture(stats: DomRegistryStats, node: HTMLElement, role: string, status = "healthy", label = ""): void {
  node.dataset.ionControlRole = role;
  node.dataset.ionCaptureStatus = status;
  if (label) node.dataset.ionCaptureLabel = label.slice(0, 80);
  stats.composerCapture[role] = (stats.composerCapture[role] ?? 0) + 1;
}

function uniqueElements(selectors: string): HTMLElement[] {
  const elements: HTMLElement[] = [];
  const seenElements = new Set<Element>();
  document.querySelectorAll<HTMLElement>(selectors).forEach((node) => {
    if (seenElements.has(node) || shouldIgnoreScanNode(node) || !registryRectVisible(node)) return;
    seenElements.add(node);
    elements.push(node);
  });
  return elements;
}

function annotateMessages(stats: DomRegistryStats): void {
  const nodes = uniqueElements("[data-message-author-role], article");
  nodes.forEach((node, index) => {
    const role = node.getAttribute("data-message-author-role") || "message";
    node.dataset.ionMessageIndex = String(index + 1);
    ensureRegistryBadge(node, "message", `ION msg ${index + 1} ${role}`, "idle");
  });
  stats.messages = nodes.length;
}

function codeBlockHosts(): HTMLElement[] {
  const hosts: HTMLElement[] = [];
  const seenHosts = new Set<Element>();
  document.querySelectorAll<HTMLElement>("pre, pre code, code, [class*='font-mono'], [class*='whitespace-pre'], [class*='overflow-x-auto']").forEach((node) => {
    if (shouldIgnoreScanNode(node) || !registryRectVisible(node)) return;
    const host = (node.closest("pre") as HTMLElement | null) ?? node;
    if (seenHosts.has(host) || shouldIgnoreScanNode(host) || !registryRectVisible(host)) return;
    seenHosts.add(host);
    hosts.push(host);
  });
  return hosts;
}

function annotateCodeBlocks(stats: DomRegistryStats, mode: ScanMode): void {
  const actionIds = new Set<string>();
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

function annotateComposerControls(stats: DomRegistryStats): void {
  const composer = findComposer();
  const composerRect = composer?.getBoundingClientRect();
  if (composer && captureRectVisible(composer)) {
    noteCapture(stats, composer as HTMLElement, "composer_input", "healthy", "composer input");
  }
  const controls = Array.from(document.querySelectorAll<HTMLElement>("button, [role='button'], input[type='file']")).filter((node) => {
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
    document.querySelectorAll<HTMLElement>(
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
    document.querySelectorAll<HTMLElement>("button, [role='button'], [aria-label], [data-testid], [class*='chip' i], [class*='pill' i]"),
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

function updateDomActionRegistry(mode: ScanMode = "manual"): DomRegistryStats {
  ensureDomRegistryStyle();
  const stats: DomRegistryStats = {
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

function shouldIgnoreScanNode(node: Element): boolean {
  if (typeof node.closest !== "function") return false;
  return Boolean(
    node.closest(`#${PANEL_ID}`) ??
      node.closest(`#${MODAL_ID}`) ??
      node.closest("[data-message-author-role='user']") ??
      node.closest("#prompt-textarea") ??
      node.closest("[contenteditable='true']") ??
      node.closest("textarea"),
  );
}

function candidateBlocks(mode: ScanMode = "manual"): string[] {
  const selectors = mode === "auto" ? AUTO_SCAN_SELECTORS : MANUAL_SCAN_SELECTORS;
  const nodes: Element[] = [];
  const seenNodes = new Set<Element>();
  for (const selector of selectors) {
    document.querySelectorAll<Element>(selector).forEach((node) => {
      if (seenNodes.has(node) || shouldIgnoreScanNode(node)) return;
      seenNodes.add(node);
      nodes.push(node);
    });
  }
  const blocks: string[] = [];
  const seenText = new Set<string>();
  for (const node of nodes) {
    const rawCandidates = [
      node.textContent ?? "",
      mode === "manual" && typeof (node as HTMLElement).innerText === "string" ? (node as HTMLElement).innerText : "",
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

function findComposer(): HTMLElement | HTMLTextAreaElement | null {
  return (
    document.querySelector<HTMLElement>("#prompt-textarea") ??
    document.querySelector<HTMLTextAreaElement>("textarea") ??
    document.querySelector<HTMLElement>("[contenteditable='true']")
  );
}

function insertIntoComposer(text: string): boolean {
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

function insertComposerBlock(label: string, text: string): void {
  const ok = insertIntoComposer(`\`\`\`yaml\n${text}\n\`\`\``);
  setBridgeStatus(
    ok ? `${label} inserted` : "Composer not found",
    ok ? "Review the inserted block, then send it in ChatGPT." : "Click in the ChatGPT input box and try again.",
    ok ? "success" : "error",
  );
}

function insertComposerPrompt(label: string, text: string): void {
  const ok = insertIntoComposer(text);
  setBridgeStatus(
    ok ? `${label} inserted` : "Composer not found",
    ok ? "Review the inserted prompt, then send it in ChatGPT." : "Click in the ChatGPT input box and try again.",
    ok ? "success" : "error",
  );
}

function insertSevContextBrief(): void {
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

function actionStamp(): string {
  const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z").toLowerCase();
  return `sev-${stamp}`;
}

function stampActionText(text: string, kind: "smoke" | "codex"): string {
  const stamp = actionStamp();
  if (kind === "smoke") {
    return text
      .replace("sev-20260505-0001-smoke", `${stamp}-smoke`)
      .replace("SEV_CHATOPS_SMOKE.md", `SEV_CHATOPS_SMOKE_${stamp}.md`);
  }
  return text.replace("sev-20260505-0002-codex-work", `${stamp}-codex-work`);
}

function blockedDetail(response: any): string {
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

function compactJson(value: unknown, max = 1800): string {
  const text = JSON.stringify(value ?? null, null, 2);
  return text.length > max ? `${text.slice(0, max)}\n...` : text;
}

function formatBytes(value: unknown): string {
  const bytes = Number(value);
  if (!Number.isFinite(bytes) || bytes < 0) return "unknown size";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KiB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MiB`;
}

function summarizeAttachables(result: any): string {
  const rows = Array.isArray(result?.candidates) ? result.candidates : [];
  const attachables = rows.filter((row: any) => row?.attachable && typeof row.path === "string");
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
    attachables.slice(1, 4).forEach((row: any, index: number) => {
      lines.push(`  ${index + 2}. ${row.name ?? row.path} (${formatBytes(row.size_bytes)})`);
    });
  }
  lines.push("", "Use Local Attach for OS file-picker assist, or Drop Latest for browser synthetic drop. Neither clicks Send.");
  return lines.join("\n");
}

async function copyBridgeResult(label: string, detail: string): Promise<void> {
  await copyReceiptSummary(`${label}\n${detail}`);
}

function requestAgentRead(type: "ion_chatops_agent_status" | "ion_chatops_agent_queue", label: string): void {
  setBridgeStatus(label, "Requesting local daemon projection.", "working");
  chrome.runtime.sendMessage({ type }, async (response) => {
    const detail = response?.ok ? compactJson(response.result) : blockedDetail(response);
    setBridgeAgentDetail(detail);
    setBridgeStatus(response?.ok ? `${label} ready` : `${label} blocked`, detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
    if (response?.ok) await copyBridgeResult(label, detail);
  });
}

function requestAgentMutation(type: "ion_chatops_agent_prepare_next" | "ion_chatops_agent_start_one", label: string): void {
  setBridgeStatus(label, "Requesting Braden approval through the bridge panel.", "working");
  chrome.runtime.sendMessage({ type, payload: {} }, async (response) => {
    const detail = response?.ok ? compactJson(response.result) : blockedDetail(response);
    setBridgeAgentDetail(detail);
    setBridgeStatus(response?.ok ? `${label} submitted` : `${label} blocked`, detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
    if (response?.ok) await copyBridgeResult(label, detail);
  });
}

function inactiveQueueStatus(status: string): boolean {
  return /SUPERSEDED|FULFILLED|INVALID|ARCHIVE_ONLY|SETTLED|DUPLICATE|BLOCKED|CANCELLED/i.test(status);
}

function firstActionableRequest(queue: any): any | null {
  const rows = Array.isArray(queue?.requests) ? queue.requests : [];
  return rows.find((row: any) => !inactiveQueueStatus(String(row?.status ?? ""))) ?? null;
}

function requestAgentPreview(): void {
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

function requestAgentLatestRuns(): void {
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
          .map((run: any, index: number) => [
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

function requestContextPack(): void {
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

function requestZip(type: "ion_chatops_compact_zip" | "ion_chatops_safe_full_zip", label: string): void {
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

function latestSandboxReturnId(result: any): string | null {
  const rows = Array.isArray(result?.returns) ? result.returns : [];
  const first = rows.find((row: any) => typeof row?.return_id === "string" && row.return_id.trim());
  return first?.return_id ?? null;
}

function requestSandboxReturns(): void {
  setBridgeStatus("Sandbox returns", "Fetching ChatGPT sandbox return queue.", "working");
  chrome.runtime.sendMessage({ type: "ion_chatops_sandbox_returns" }, async (response) => {
    const detail = response?.ok ? compactJson(response.result) : blockedDetail(response);
    setBridgeSandboxDetail(detail);
    setBridgeStatus(response?.ok ? "Sandbox returns ready" : "Sandbox returns blocked", detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
    if (response?.ok) await copyBridgeResult("Sandbox returns", detail);
  });
}

function requestSandboxMutation(type: "ion_chatops_sandbox_diff_latest" | "ion_chatops_sandbox_queue_latest", label: string): void {
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

function requestArtifactAttachables(): void {
  setBridgeStatus("Attachables", "Reading local packages and sandbox return artifacts.", "working");
  chrome.runtime.sendMessage({ type: "ion_chatops_artifact_attachables" }, async (response) => {
    const detail = response?.ok ? summarizeAttachables(response.result) : blockedDetail(response);
    setBridgeArtifactDetail(detail);
    setBridgeStatus(response?.ok ? "Attachables ready" : "Attachables blocked", detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
    if (response?.ok) await copyBridgeResult("Attachable artifacts", detail);
  });
}

function findDropTarget(): HTMLElement | null {
  const composer = findComposer();
  if (!composer) return null;
  return (
    composer.closest("form") ??
    composer.closest("[data-testid*='composer']") ??
    composer.closest("main") ??
    composer
  ) as HTMLElement | null;
}

function composerRect(): DOMRect | null {
  const composer = findComposer();
  return composer?.getBoundingClientRect() ?? null;
}

function controlLabel(node: HTMLElement): string {
  return `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.textContent ?? ""}`.replace(/\s+/g, " ").trim();
}

function visibleElement(node: HTMLElement): boolean {
  const rect = node.getBoundingClientRect();
  return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
}

function findAttachControlRect(): Record<string, unknown> | null {
  const rect = composerRect();
  const nodes = Array.from(document.querySelectorAll<HTMLElement>("button, [role='button'], input[type='file']"));
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

function uploadedAttachmentCount(): number {
  const rect = composerRect();
  return Array.from(
    document.querySelectorAll<HTMLElement>(
      "img, [data-testid*='attachment' i], [data-testid*='upload' i], [data-testid*='file' i], [data-testid*='image' i], [aria-label*='remove' i], [aria-label*='file' i], [aria-label*='image' i], [class*='attachment' i]",
    ),
  ).filter((node) => {
    if (!visibleElement(node)) return false;
    const bounds = node.getBoundingClientRect();
    return rect ? bounds.bottom >= rect.top - 300 && bounds.top <= rect.bottom + 160 : bounds.top > window.innerHeight * 0.45;
  }).length;
}

function waitForUploadChip(previousCount: number, label: string, baseDetail: string): void {
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

async function attemptPreparedArtifactDrop(result: any): Promise<void> {
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

function requestArtifactDropLatest(): void {
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

function requestArtifactLocalAttachLatest(): void {
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
      target_screen_rect: targetRect["screen_rect"],
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

function actionSummary(packet: ReturnType<typeof parseStrictIonActionYaml>): string {
  if (!packet) return "packet_parse_failed";
  return JSON.stringify({
    action_id: packet.ion_action.action_id,
    intent: packet.ion_action.intent,
    target: packet.ion_action.target ?? packet.ion_action.github ?? {},
    receipts: packet.ion_action.receipts?.requested ?? [],
  }, null, 2);
}

function shouldSkipAction(packet: ReturnType<typeof parseStrictIonActionYaml>): boolean {
  const actionId = packet?.ion_action?.action_id;
  return Boolean(actionId && (inFlightActionIds.has(actionId) || submittedActionIds.has(actionId)));
}

function markBlockedOnce(packet: ReturnType<typeof parseStrictIonActionYaml>, findings: string[]): boolean {
  const actionId = packet?.ion_action?.action_id;
  const key = actionId ? `${actionId}:${findings.join("|")}` : findings.join("|");
  if (reportedBlockedActionIds.has(key)) return false;
  reportedBlockedActionIds.add(key);
  return true;
}

function submitPacket(label: string, packet: ReturnType<typeof parseStrictIonActionYaml>): void {
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

function submitActionText(label: string, text: string): void {
  const parsed = parseIonActionYamlWithDiagnostics(text);
  if (!parsed.packet) {
    setBridgeStatus(`${label} blocked`, parsed.finding ?? "unknown_parse_failure", "error");
    setBridgeActionDetail((parsed.extracted_yaml ?? text).slice(0, 1200));
    return;
  }
  submitPacket(label, parsed.packet);
}

function scan(mode: ScanMode = "manual"): number {
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

function mutationTouchesIonUi(mutation: MutationRecord): boolean {
  const isIonNode = (node: Node): boolean => {
    if (node.nodeType !== Node.ELEMENT_NODE) return false;
    const element = node as Element;
    return Boolean(
      element.closest(`#${PANEL_ID}`) ||
        element.closest(`#${MODAL_ID}`) ||
        element.closest(`#${DOM_REGISTRY_STYLE_ID}`) ||
        element.id === PANEL_ID ||
        element.id === MODAL_ID ||
        element.id === DOM_REGISTRY_STYLE_ID ||
        element.closest(".ion-dom-badge"),
    );
  };
  if (isIonNode(mutation.target)) return true;
  return Array.from(mutation.addedNodes).some(isIonNode) || Array.from(mutation.removedNodes).some(isIonNode);
}

function scheduleScan(mode: ScanMode = "auto"): void {
  if (scanTimer !== null) return;
  scanTimer = window.setTimeout(() => {
    scanTimer = null;
    scan(mode);
  }, SCAN_DEBOUNCE_MS);
}

function initializeBridge(): void {
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

(window as unknown as { __ION_CHATOPS_BRIDGE_DEBUG__?: unknown }).__ION_CHATOPS_BRIDGE_DEBUG__ = {
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
      "idle",
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
