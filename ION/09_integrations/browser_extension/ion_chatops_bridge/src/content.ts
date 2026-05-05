import {
  requestApproval,
  requestBridgeApproval,
  copyReceiptSummary,
  refreshBridgePosition,
  setBridgeActionDetail,
  setBridgeAgentDetail,
  setBridgePackageDetail,
  setBridgeStatus,
} from "./approval_ui";
import { extractIonActionYaml, localValidate, parseIonActionYamlWithDiagnostics, parseStrictIonActionYaml } from "./schema";

const seen = new Set<string>();
const inFlightActionIds = new Set<string>();
const submittedActionIds = new Set<string>();
const reportedBlockedActionIds = new Set<string>();
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

function candidateBlocks(): string[] {
  const nodes: Element[] = [];
  const seenNodes = new Set<Element>();
  for (const selector of ACTION_SCAN_SELECTORS) {
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
      typeof (node as HTMLElement).innerText === "string" ? (node as HTMLElement).innerText : "",
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

function scan(): number {
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

(window as unknown as { __ION_CHATOPS_BRIDGE_DEBUG__?: unknown }).__ION_CHATOPS_BRIDGE_DEBUG__ = {
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
