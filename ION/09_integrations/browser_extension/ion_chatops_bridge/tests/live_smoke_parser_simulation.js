const fs = require("fs");
const path = require("path");
const vm = require("vm");

function findRepoRoot(start) {
  let current = path.resolve(start);
  while (true) {
    if (fs.existsSync(path.join(current, "ION", "REPO_AUTHORITY.md"))) return current;
    const parent = path.dirname(current);
    if (parent === current) return process.cwd();
    current = parent;
  }
}

const REPO_ROOT = findRepoRoot(__dirname);

const liveSmokeYaml = `YAML
\`\`\`yaml
ion_action:
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

      This file was requested by Sev through a YAML action block in ChatGPT Browser.

      MCP was not required for this action.
  receipts:
    requested:
      - file_write_receipt
      - sha256_receipt
\`\`\``;

const renderedCodeBlockYaml = `ion_action:
  schema: ion.chatops.action.v1
  action_id: sev-20260505-rendered-code-block
  intent: create_codex_work_packet
  callsign: Sev
  carrier: chatgpt_browser
  human_sovereign: Braden
  production_authority: false
  live_execution_authority: false
  requires_approval: true
  objective: "Verify rendered ChatGPT YAML code block detection without literal fences."`;

const flatCodexYaml = `ion_action:
  schema: ion.chatops.action.v1
  action_id: sev-20260505-chatops-codex-work-smoke-001
  intent: create_codex_work_packet
  callsign: Sev
  carrier: chatgpt_browser
  human_sovereign: Braden
  production_authority: false
  live_execution_authority: false
  requires_approval: true
  objective: "Verify and harden the ION ChatOps Browser Carrier Runtime after the first live smoke success."`;

const byId = new Map();

class Element {
  constructor(tag) {
    this.tag = tag;
    this.children = [];
    this.dataset = {};
    this.attributes = {};
    this.style = {};
    this.textContent = "";
    this.innerText = "";
    this._id = "";
    this._innerHTML = "";
    this.classNodes = new Map();
  }

  set id(value) {
    this._id = value;
  }

  get id() {
    return this._id;
  }

  set innerHTML(value) {
    this._innerHTML = value;
  }

  get innerHTML() {
    return this._innerHTML;
  }

  setAttribute(key, value) {
    this.attributes[key] = value;
  }

  appendChild(child) {
    this.children.push(child);
    if (child.id) byId.set(child.id, child);
    return child;
  }

  remove() {
    if (this.id) byId.delete(this.id);
  }

  closest() {
    return null;
  }

  getBoundingClientRect() {
    return { top: 800 };
  }

  addEventListener() {}

  querySelector(selector) {
    if (selector.includes("rescan") || selector.includes("collapse")) return new Element("button");
    if (selector.startsWith(".")) {
      if (!this.classNodes.has(selector)) this.classNodes.set(selector, new Element("span"));
      return this.classNodes.get(selector);
    }
    if (selector.includes("data-field")) return new Element("div");
    return null;
  }

  querySelectorAll(selector) {
    if (selector === ".ion-tab" || selector === ".ion-tab-panel") return [];
    if (selector === "code") return [];
    return [];
  }
}

let sent = null;
const documentElement = new Element("html");
const context = {
  console,
  CustomEvent: class {
    constructor(type) {
      this.type = type;
    }
  },
  window: {
    innerHeight: 1000,
    addEventListener() {},
    dispatchEvent() {},
  },
  document: {
    documentElement,
    getElementById: (id) => byId.get(id) || null,
    createElement: (tag) => new Element(tag),
    querySelector: () => null,
    querySelectorAll: (selector) => (selector === "pre code" ? [{ textContent: liveSmokeYaml }] : []),
  },
  MutationObserver: class {
    observe() {}
  },
  chrome: {
    runtime: {
      sendMessage(message, callback) {
        sent = message;
        callback({ ok: false, stage: "simulation_stop" });
      },
      onMessage: { addListener() {} },
    },
  },
  navigator: { clipboard: { writeText: async () => {} } },
};

vm.createContext(context);
vm.runInContext(
  fs.readFileSync(path.join(REPO_ROOT, "ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js"), "utf8"),
  context,
);

if (!byId.has("ion-chatops-bridge-panel")) {
  throw new Error("status panel did not render");
}
if (!sent || sent.type !== "ion_chatops_candidate") {
  throw new Error("candidate was not sent");
}

const action = sent.packet.ion_action;
if (action.schema !== "ion.chatops.action.v1") throw new Error("schema did not parse");
if (action.action_id !== "sev-20260505-0001-smoke") throw new Error("action_id did not parse");
if (action.intent !== "write_file_draft") throw new Error("intent did not parse");
if (action.actor.callsign !== "Sev") throw new Error("actor.callsign did not parse");
if (action.authority.requires_approval !== true) throw new Error("authority.requires_approval did not parse");
if (action.target.path !== "ION/05_context/current/chatops_bridge/smoke/SEV_CHATOPS_SMOKE.md") {
  throw new Error("target.path did not parse");
}
if (!String(action.content.text || "").includes("MCP was not required for this action.")) {
  throw new Error("content.text block scalar did not parse");
}
if (!Array.isArray(action.receipts.requested) || action.receipts.requested.length !== 2) {
  throw new Error("receipts.requested list did not parse");
}

const flat = context.window.__ION_CHATOPS_BRIDGE_DEBUG__.parseIonActionYamlWithDiagnostics(flatCodexYaml);
if (!flat.packet) throw new Error(`flat codex shape rejected: ${flat.finding}`);
if (flat.packet.ion_action.actor.callsign !== "Sev") throw new Error("flat callsign was not canonicalized");
if (flat.packet.ion_action.authority.human_sovereign !== "Braden") throw new Error("flat authority was not canonicalized");
if (flat.packet.ion_action.receipts.requested[0] !== "codex_work_packet_receipt") {
  throw new Error("flat receipts default was not created");
}

const rendered = context.window.__ION_CHATOPS_BRIDGE_DEBUG__.parseIonActionYamlWithDiagnostics(renderedCodeBlockYaml);
if (!rendered.packet) throw new Error(`rendered code block shape rejected: ${rendered.finding}`);
if (rendered.packet.ion_action.action_id !== "sev-20260505-rendered-code-block") {
  throw new Error("rendered code block action_id did not parse");
}

const assistantNode = new Element("div");
assistantNode.textContent = `Here is the action:\n${liveSmokeYaml}`;
assistantNode.innerText = assistantNode.textContent;
context.document.querySelectorAll = (selector) =>
  selector === "[data-message-author-role='assistant']" ? [assistantNode] : [];
const assistantBlocks = context.window.__ION_CHATOPS_BRIDGE_DEBUG__.candidateBlocks();
if (assistantBlocks.length !== 1) {
  throw new Error("assistant message container fallback did not detect ion_action");
}

const chatgptRenderedCodeNode = new Element("div");
chatgptRenderedCodeNode.textContent = renderedCodeBlockYaml.replace(/\n\s*/g, "");
chatgptRenderedCodeNode.innerText = renderedCodeBlockYaml;
context.document.querySelectorAll = (selector) =>
  selector === "[data-message-author-role='assistant'] [class*='font-mono']" ? [chatgptRenderedCodeNode] : [];
const renderedBlocks = context.window.__ION_CHATOPS_BRIDGE_DEBUG__.candidateBlocks();
if (renderedBlocks.length !== 1 || !renderedBlocks[0].includes("sev-20260505-rendered-code-block")) {
  throw new Error("rendered code block innerText fallback did not detect ion_action");
}

const pageFallbackNode = new Element("main");
pageFallbackNode.textContent = [
  "Older rejected text",
  "ion_action:",
  "  schema: ion.chatops.action.v1",
  "  action_id: sev-YYYYMMDD-HHMMSS-short-slug",
  "  intent: create_codex_work_packet",
  "  callsign: Sev",
  "  carrier: chatgpt_browser",
  "  human_sovereign: Braden",
  "  production_authority: false",
  "  requires_approval: true",
  "  objective: \"State the exact bounded work for local Codex/ION to perform.\"",
  "Current rendered action",
  renderedCodeBlockYaml,
].join("\n");
pageFallbackNode.innerText = pageFallbackNode.textContent;
context.document.querySelectorAll = (selector) => (selector === "main" ? [pageFallbackNode] : []);
const pageFallbackBlocks = context.window.__ION_CHATOPS_BRIDGE_DEBUG__.candidateBlocks();
if (pageFallbackBlocks.length < 2) {
  throw new Error("page fallback did not split multiple ion_action blocks");
}
if (!pageFallbackBlocks.some((block) => block.includes("sev-20260505-rendered-code-block"))) {
  throw new Error("page fallback missed later concrete ion_action block");
}

console.log(JSON.stringify({
  ok: true,
  panel: true,
  candidate: sent.type,
  action_id: action.action_id,
  receipts: action.receipts.requested,
  flat_action_id: flat.packet.ion_action.action_id,
  rendered_action_id: rendered.packet.ion_action.action_id,
  assistant_container_detected: assistantBlocks.length,
  rendered_dom_detected: renderedBlocks.length,
  page_fallback_blocks: pageFallbackBlocks.length,
}));
