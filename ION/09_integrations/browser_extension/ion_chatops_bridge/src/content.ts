import {
  requestApproval,
  requestBridgeApproval,
  copyReceiptSummary,
  refreshBridgePosition,
  setBridgeActionDetail,
  setBridgeAgentDetail,
  setBridgeArtifactDetail,
  setBridgeCodexState,
  setBridgeDocsFavorites,
  setBridgeDocsState,
  setBridgeDiagnosticsDetail,
  importBridgeQueuePackFile,
  setBridgeInspectorLayers,
  setBridgeMessageQueueState,
  setBridgeMonitorMetrics,
  setBridgePackageDetail,
  setBridgeProjectsState,
  setBridgeSandboxDetail,
  setBridgeSettingsDetail,
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
const DOM_REGISTRY_POPOVER_ID = "ion-chatops-dom-registry-popover";
const ASSET_CAPTURE_BUTTON_CLASS = "ion-chatops-asset-capture-button";
const ASSET_CAPTURE_STYLE_ID = "ion-chatops-asset-capture-style";
const CHATGPT_LEFT_ICON_DOCK_ID = "ion-chatgpt-left-icon-dock";
const CHATGPT_LEFT_ICON_DOCK_STYLE_ID = "ion-chatgpt-left-icon-dock-style";
const CHATGPT_LEFT_ICON_DOCK_CLASS = "ion-chatgpt-left-icon-dock-bottom-half";
const CHATGPT_LEFT_ICON_DOCK_STORAGE_KEY = "ION_CHATOPS_LEFT_DOCK_PROJECT_PANEL_EXPANDED";
const MESSAGE_QUEUE_BUTTON_ID = "ion-chatops-message-queue-button";
const MESSAGE_QUEUE_SEND_NEXT_BUTTON_ID = "ion-chatops-message-queue-send-next-button";
const MESSAGE_QUEUE_PANEL_ID = "ion-chatops-message-queue-float";
const MESSAGE_QUEUE_CHROME_STYLE_ID = "ion-chatops-message-queue-style";
const MESSAGE_QUEUE_FILE_INPUT_ID = "ion-chatops-message-queue-file-input";
const CONTEXT_WORKFLOW_PANEL_ID = "ion-chatops-context-workflow-float";
const CONTEXT_WORKFLOW_STYLE_ID = "ion-chatops-context-workflow-style";
const CONTEXT_WORKFLOW_IMPORT_INPUT_ID = "ion-chatops-context-workflow-import";
const CAPTURE_FRAME_ID = "ion-chatops-capture-frame";
const ATTACH_PREVIEW_ID = "ion-chatops-attach-target-preview";
const DROP_PREVIEW_ID = "ion-chatops-drop-target-preview";
const TABS_ANCHOR_PREVIEW_ID = "ion-chatops-tabs-anchor-preview";
const INSPECTOR_HUD_ID = "ion-chatops-dom-inspector-hud";
const INSPECTOR_SELECTED_PREVIEW_ID = "ion-chatops-dom-inspector-selected-preview";
const INSPECTOR_ANCHOR_MARKER_CLASS = "ion-chatops-anchor-marker";
const INSPECTOR_OUTLINE_CLASS = "ion-chatops-dom-inspector-outline";
const SETTINGS_CONTROL_PAD_ID = "ion-chatops-settings-control-pad";
const SAFE_MODE_KEY = "ION_CHATOPS_SAFE_MODE";
const ATTACH_TARGET_SELECTOR_KEY = "ION_CHATOPS_ATTACH_TARGET_SELECTOR";
const DROP_TARGET_SELECTOR_KEY = "ION_CHATOPS_DROP_TARGET_SELECTOR";
const CHAT_CONTEXT_REFERENCE_16K = 16000;
const CHAT_CONTEXT_REFERENCE_32K = 32000;
const CHAT_CONTEXT_REFERENCE_128K = 128000;
const CHAT_CONTEXT_REFERENCE_256K = 256000;
const CHAT_CONTEXT_REFERENCE_400K = 400000;
const BROWSER_PRESSURE_INTERVAL_MS = 2500;
const CHAT_CONTEXT_WATCH_PERCENT = 75;
const CHAT_CONTEXT_BLOCKED_PERCENT = 95;
const EVENT_LOOP_WATCH_MS = 120;
const EVENT_LOOP_BLOCKED_MS = 350;
const DOM_WATCH_NODES = 6500;
const DOM_BLOCKED_NODES = 12000;
const MESSAGE_QUEUE_TICK_MS = 900;
const MESSAGE_QUEUE_SEND_SETTLE_MS = 140;
const MESSAGE_QUEUE_NEXT_DELAY_MS = 1600;
const MESSAGE_QUEUE_RIGHT_GUTTER_PX = 28;
const MESSAGE_QUEUE_PANEL_MINI_WIDTH_PX = 76;
const MESSAGE_QUEUE_PANEL_VIS_LIST_LIMIT = 10;
const MESSAGE_QUEUE_PANEL_ROW_HEIGHT_PX = 32;
const LEFT_DOCK_PANEL_WIDTH_MINI_PX = 54;
const LEFT_DOCK_PANEL_WIDTH_EXPANDED_PX = 246;
const CONTEXT_WORKFLOW_AUTO_SYNC_DEBOUNCE_MS = 550;
const TABS_ANCHOR_SELECTOR_KEY = "ION_CHATOPS_TABS_ANCHOR_SELECTOR";
const CAPTURE_FRAME_SELECTOR_KEY = "ION_CHATOPS_CAPTURE_FRAME_SELECTOR";
const CAPTURE_FRAME_TIMEOUT_MS = 30000;
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

type InspectorSaveTarget = "tabs_anchor" | "drop_zone" | "attach_target";
type AnchorPoint = "top" | "left" | "center" | "right" | "bottom";
type TargetMetaInfo = {
  selector: string;
  anchor: AnchorPoint;
};
type AnchorRect = DOMRect | {
  x: number;
  y: number;
  width: number;
  height: number;
};
type InspectorCaptureMode = "single" | "settings";
type DocsEntry = {
  kind: "folder" | "file";
  name: string;
  path: string;
  size_bytes?: number;
  thumbnail?: string;
};

type DocsFavoriteRoot = {
  path: string;
  label: string;
  icon: string;
  accent?: string;
  status?: string;
};

type ProjectPackageEntry = {
  project: string;
  version: string;
  name: string;
  path: string;
  root: string;
  kind: "folder" | "file";
  latest: boolean;
  updated: string;
  score: number;
};

const DOCS_FAVORITE_ROOTS: DocsFavoriteRoot[] = [
  { path: "ION", label: "ION", icon: "🧱" },
  { path: "dAimon_ION", label: "Daimon", icon: "🧠" },
  { path: "ION/09_integrations", label: "Integrations", icon: "🧩" },
  { path: "ION/02_architecture", label: "Architecture", icon: "🧭" },
  { path: "ION/06_artifacts", label: "Artifacts", icon: "🧰" },
];

const DOCS_TREE_LOCATIONS = [
  { value: "", label: "🏠 Home", group: "Start" },
  { value: "ION", label: "ION", group: "Workspace" },
  { value: "dAimon_ION", label: "Daimon", group: "Workspace" },
  { value: "ION/02_architecture", label: "Architecture", group: "Workspace" },
  { value: "ION/03_registry", label: "Registry", group: "Workspace" },
  { value: "ION/05_context", label: "Context", group: "Workspace" },
  { value: "ION/06_artifacts", label: "Artifacts", group: "Workspace" },
  { value: "ION/09_integrations", label: "Integrations", group: "Workspace" },
  { value: "ION/09_integrations/browser_extension", label: "ChatOps Bridge", group: "Workspace" },
  { value: "ION/09_integrations/browser_extension/ion_chatops_bridge", label: "Bridge package", group: "Workspace" },
];
const PROJECT_CONTEXT_PACKAGE_ROOTS = [
  "ION/05_context/history/kernel_store/context_packages",
  "ION/05_context/current/context_packages",
  "ION/06_artifacts/packages",
  "ION/05_context/history/front_door_runtime/persona_response_packages",
  "ION/05_context/history/front_door_runtime/relay_return_packages",
  "ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging",
];
type DocsBrowseState = {
  roots: string[];
  currentRoot: string;
  currentPath: string;
  query: string;
  breadcrumbs: string[];
  entries: DocsEntry[];
  selectedPath: string;
  selectedDocName: string;
  status: string;
};

type InspectorLayer = {
  index: number;
  element: HTMLElement;
  selector: string;
  label: string;
  rect: Record<string, number>;
};

let scanTimer: number | null = null;
let scanRunning = false;
let scanQueued = false;
let inspectorActive = false;
let inspectorCaptureMode: InspectorCaptureMode = "single";
let inspectorCapturedLayers: InspectorLayer[] = [];
let inspectorSelectedIndex = 0;
let settingsInspectorTarget: InspectorSaveTarget = "tabs_anchor";
let settingsAnchorPoint: AnchorPoint = "bottom";
let contextWorkflowAutoSyncTimer: number | null = null;
const defaultDocsState: DocsBrowseState = {
  roots: DOCS_FAVORITE_ROOTS.map((entry) => entry.path),
  currentRoot: "",
  currentPath: "",
  query: "",
  breadcrumbs: [],
  entries: [],
  selectedPath: "",
  selectedDocName: "",
  status: "Open Docs and pick a preselected root folder.",
};
let docsState: DocsBrowseState = { ...defaultDocsState };
let projectPackages: ProjectPackageEntry[] = [];
let selectedProjectPackagePath = "";
let selectedProjectPackagePaths: string[] = [];
let docsDropProgressTimer: number | null = null;
let docsDropFavoritePath = "";
let captureFrameTimer: number | null = null;
let captureFrameLayerIndex = 0;
let captureFrameLayers: Array<{ index: number; element: HTMLElement; label: string; selector: string }> = [];

function safeModeDisabled(): boolean {
  try {
    const value = window.localStorage?.getItem(SAFE_MODE_KEY) ?? window.sessionStorage?.getItem(SAFE_MODE_KEY);
    return ["1", "true", "disabled", "off"].includes(String(value ?? "").trim().toLowerCase());
  } catch (_error) {
    return false;
  }
}

function leftDockPanelExpandedFromStorage(): boolean {
  try {
    return window.localStorage?.getItem(CHATGPT_LEFT_ICON_DOCK_STORAGE_KEY) === "1";
  } catch (_error) {
    return false;
  }
}

function persistLeftDockPanelExpanded(next: boolean): void {
  try {
    window.localStorage?.setItem(CHATGPT_LEFT_ICON_DOCK_STORAGE_KEY, next ? "1" : "0");
  } catch (_error) {
    // Ignore storage failures.
  }
}

function ensureDomRegistryStyle(): void {
  if (document.getElementById(DOM_REGISTRY_STYLE_ID)) return;
  const style = document.createElement("style");
  style.id = DOM_REGISTRY_STYLE_ID;
  style.textContent = `
    .ion-dom-badge {
      position: absolute;
      top: 0;
      left: 0;
      z-index: 2147483644;
      width: 10px;
      height: 10px;
      padding: 0;
      border: 2px solid rgba(12,12,12,0.86);
      border-radius: 999px;
      background: #94a3b8;
      color: transparent;
      font-size: 0;
      line-height: 0;
      pointer-events: auto;
      cursor: pointer;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.18), 0 4px 14px rgba(0,0,0,0.25);
      opacity: 0.18;
      transform: scale(0.74);
      transform-origin: center;
      transition: opacity 120ms ease, transform 120ms ease, box-shadow 120ms ease;
    }
    [data-ion-registry-host="true"] > .ion-dom-badge:hover,
    [data-ion-registry-host="true"] > .ion-dom-badge:focus-visible,
    [data-ion-registry-host="true"]:hover > .ion-dom-badge,
    [data-ion-registry-host="true"]:focus-within > .ion-dom-badge {
      opacity: 1;
      transform: scale(1);
      box-shadow: 0 0 0 2px rgba(255,255,255,0.30), 0 8px 22px rgba(0,0,0,0.34);
    }
    .ion-dom-badge[data-tone="valid"],
    .ion-dom-badge[data-tone="blocked"],
    .ion-dom-badge[data-tone="duplicate"] {
      opacity: 0.92;
      transform: scale(0.9);
      box-shadow: 0 0 0 2px rgba(255,255,255,0.30), 0 8px 22px rgba(0,0,0,0.34);
    }
    .ion-dom-badge[data-tone="valid"] {
      background: #34d399;
    }
    .ion-dom-badge[data-tone="blocked"] {
      background: #fbbf24;
    }
    .ion-dom-badge[data-tone="duplicate"] {
      background: #a78bfa;
    }
    .ion-dom-badge[data-ion-badge-kind="message"] {
      background: #94a3b8;
    }
    .ion-dom-badge[data-ion-badge-role="code"] {
      background: #60a5fa;
    }
    .ion-dom-badge[data-ion-badge-kind="control"] {
      background: #fb923c;
    }
    .ion-dom-badge[data-ion-badge-role="attach_button"],
    .ion-dom-badge[data-ion-badge-role="voice_button"] {
      background: #34d399;
    }
    .ion-dom-badge[data-ion-badge-role="send_button"] {
      background: #fbbf24;
    }
    .ion-dom-badge[data-ion-badge-role="source_plane"] {
      background: #60a5fa;
    }
    .ion-dom-badge[data-ion-badge-role="uploaded_attachment"] {
      background: #a78bfa;
    }
    .ion-dom-badge:focus-visible {
      outline: 2px solid rgba(255,255,255,0.85);
      outline-offset: 2px;
    }
    [data-ion-message-index] {
      outline: 1px solid rgba(148,163,184,0.09);
      outline-offset: 2px;
      border-radius: 12px;
      transition: outline-color 120ms ease, background-color 120ms ease;
    }
    [data-ion-message-index]:hover,
    [data-ion-message-index]:focus-within {
      outline-color: rgba(148,163,184,0.30);
      background-color: rgba(148,163,184,0.025);
    }
    #${DOM_REGISTRY_POPOVER_ID} {
      position: fixed;
      z-index: 2147483647;
      width: min(320px, calc(100vw - 24px));
      max-height: min(420px, calc(100vh - 24px));
      overflow: auto;
      border: 1px solid rgba(255,255,255,0.18);
      border-radius: 10px;
      background: rgba(16, 18, 22, 0.96);
      color: rgba(255,255,255,0.88);
      box-shadow: 0 24px 68px rgba(0,0,0,0.50);
      backdrop-filter: blur(14px);
      padding: 10px;
      font: 11px/1.35 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    #${DOM_REGISTRY_POPOVER_ID} .ion-registry-title {
      font-weight: 700;
      color: #f8fafc;
      margin-bottom: 7px;
    }
    #${DOM_REGISTRY_POPOVER_ID} .ion-registry-grid {
      display: grid;
      grid-template-columns: 68px minmax(0, 1fr);
      gap: 5px 8px;
    }
    #${DOM_REGISTRY_POPOVER_ID} .ion-registry-key {
      color: rgba(255,255,255,0.52);
    }
    #${DOM_REGISTRY_POPOVER_ID} .ion-registry-value {
      color: rgba(255,255,255,0.84);
      overflow-wrap: anywhere;
      white-space: pre-wrap;
    }
    #${DOM_REGISTRY_POPOVER_ID} .ion-registry-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      justify-content: flex-end;
      margin-bottom: 9px;
    }
    #${DOM_REGISTRY_POPOVER_ID} button {
      appearance: none;
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 999px;
      background: rgba(255,255,255,0.08);
      color: rgba(255,255,255,0.88);
      width: 28px;
      height: 28px;
      padding: 0;
      font: 800 12px/1 ui-sans-serif, system-ui, sans-serif;
      cursor: pointer;
    }
    [data-ion-code-index] {
      outline: 1px solid rgba(255,255,255,0.05);
      outline-offset: 3px;
      border-radius: 10px;
      transition: outline-color 120ms ease, box-shadow 120ms ease;
    }
    [data-ion-code-index]:hover,
    [data-ion-code-index]:focus-within {
      outline-color: rgba(96,165,250,0.32);
      box-shadow: 0 0 0 4px rgba(96,165,250,0.045);
    }
    [data-ion-yaml-status="valid"] {
      outline-color: rgba(16,185,129,0.42);
      box-shadow: 0 0 0 4px rgba(16,185,129,0.055);
    }
    [data-ion-yaml-status="blocked"],
    [data-ion-yaml-status="duplicate"] {
      outline-color: rgba(251,191,36,0.42);
      box-shadow: 0 0 0 4px rgba(251,191,36,0.055);
    }
    [data-ion-control-role] {
      position: relative;
      box-shadow: 0 0 0 1px rgba(255,112,28,0.18), 0 0 0 4px rgba(255,112,28,0.035) !important;
      border-radius: 10px !important;
      transition: box-shadow 120ms ease, outline-color 120ms ease;
    }
    [data-ion-control-role]:hover,
    [data-ion-control-role]:focus-within {
      box-shadow: 0 0 0 1px rgba(255,112,28,0.46), 0 0 0 5px rgba(255,112,28,0.09) !important;
    }
    [data-ion-control-role="composer_input"] {
      box-shadow: 0 0 0 1px rgba(255,112,28,0.22), 0 0 0 5px rgba(255,112,28,0.045) !important;
    }
    [data-ion-control-role="attach_button"],
    [data-ion-control-role="voice_button"] {
      box-shadow: 0 0 0 1px rgba(52,211,153,0.22), 0 0 0 4px rgba(52,211,153,0.045) !important;
    }
    [data-ion-control-role="send_button"] {
      box-shadow: 0 0 0 1px rgba(251,191,36,0.50), 0 0 0 4px rgba(251,191,36,0.10) !important;
    }
    [data-ion-control-role="source_plane"],
    [data-ion-control-role="uploaded_attachment"] {
      box-shadow: 0 0 0 1px rgba(129,140,248,0.26), 0 0 0 4px rgba(129,140,248,0.045) !important;
    }
      #${ATTACH_PREVIEW_ID},
      #${DROP_PREVIEW_ID},
      #${TABS_ANCHOR_PREVIEW_ID} {
        position: fixed;
        z-index: 2147483645;
      pointer-events: none;
      border: 2px solid rgba(52,211,153,0.98);
      border-radius: 12px;
      box-shadow: 0 0 0 5px rgba(52,211,153,0.18), 0 0 28px rgba(52,211,153,0.55);
      background: rgba(52,211,153,0.08);
    }
      #${DROP_PREVIEW_ID} {
        border-color: rgba(96,165,250,0.98);
        box-shadow: 0 0 0 5px rgba(96,165,250,0.16), 0 0 34px rgba(96,165,250,0.50);
        background: rgba(96,165,250,0.08);
      }
      #${TABS_ANCHOR_PREVIEW_ID} {
        border-color: rgba(255,112,28,0.98);
        box-shadow: 0 0 0 5px rgba(255,112,28,0.15), 0 0 34px rgba(255,112,28,0.48);
        background: rgba(255,112,28,0.08);
      }
    .${INSPECTOR_OUTLINE_CLASS},
    #${INSPECTOR_SELECTED_PREVIEW_ID} {
      position: fixed;
      z-index: 2147483644;
      pointer-events: none;
      box-sizing: border-box;
      border: 1px solid rgba(96,165,250,0.64);
      border-radius: 8px;
      background: rgba(96,165,250,0.045);
      box-shadow: 0 0 0 2px rgba(96,165,250,0.10);
    }
    .${INSPECTOR_OUTLINE_CLASS}[data-layer="0"] {
      border-color: rgba(255,112,28,0.96);
      background: rgba(255,112,28,0.07);
      box-shadow: 0 0 0 3px rgba(255,112,28,0.14), 0 0 22px rgba(255,112,28,0.28);
    }
    .${INSPECTOR_OUTLINE_CLASS}[data-selected="true"],
    #${INSPECTOR_SELECTED_PREVIEW_ID} {
      z-index: 2147483645;
      border: 2px solid rgba(236,72,153,0.98);
      background: rgba(236,72,153,0.08);
      box-shadow: 0 0 0 5px rgba(236,72,153,0.16), 0 0 34px rgba(236,72,153,0.42);
    }
    .${INSPECTOR_OUTLINE_CLASS} > span,
    #${INSPECTOR_SELECTED_PREVIEW_ID} > span {
      position: absolute;
      top: -20px;
      left: 0;
      max-width: min(320px, 60vw);
      height: 18px;
      padding: 0 6px;
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 999px;
      background: rgba(12,12,12,0.82);
      color: rgba(255,255,255,0.86);
      font: 10px/18px ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      backdrop-filter: blur(8px);
    }
    .${INSPECTOR_ANCHOR_MARKER_CLASS} {
      position: absolute;
      width: 12px;
      height: 12px;
      border-radius: 999px;
      background: rgba(12,12,12,0.92);
      border: 2px solid #ffffff;
      transform: translate(-50%, -50%);
      box-shadow: 0 0 0 3px rgba(0,0,0,0.55);
      pointer-events: none;
      z-index: 2147483647;
    }
    #${INSPECTOR_HUD_ID} {
      position: fixed;
      z-index: 2147483646;
      pointer-events: none;
      max-width: min(430px, calc(100vw - 24px));
      border: 1px solid rgba(255,112,28,0.52);
      border-radius: 10px;
      background: rgba(12,12,12,0.90);
      color: rgba(255,255,255,0.86);
      padding: 8px 9px;
      box-shadow: 0 18px 46px rgba(0,0,0,0.42);
      backdrop-filter: blur(14px);
      font: 11px/1.3 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    #${INSPECTOR_HUD_ID} strong {
      color: #ffd2b0;
      font-weight: 700;
    }
    #${INSPECTOR_HUD_ID} ol {
      margin: 6px 0 0;
      padding-left: 18px;
    }
    #${INSPECTOR_HUD_ID} li {
      margin: 2px 0;
      max-width: 390px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
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

function registryBadgeCanAttach(host: HTMLElement): boolean {
  return !["INPUT", "TEXTAREA", "IMG", "BR", "HR"].includes(host.tagName);
}

function registryBadgeCategory(kind: string, role: string): string {
  if (kind === "message") return "read_chunk";
  if (role.startsWith("yaml_")) return "action_yaml";
  if (kind === "code") return "code_chunk";
  if (role === "send_button" || role === "attach_button" || role === "voice_button" || role === "composer_control") return "click_zone";
  if (role === "composer_input") return "text_entry_zone";
  if (role === "source_plane" || role === "uploaded_attachment") return "source_or_attachment_surface";
  return kind || role || "page_marker";
}

function registryBadgeMeaning(kind: string, role: string, tone: string): string {
  if (kind === "message") return "Readable conversation chunk currently visible in the page DOM.";
  if (role === "code") return "Readable code/text block; scanned but not treated as an action packet.";
  if (role === "yaml_valid") return "Concrete ION action YAML candidate; validation passed locally and still requires operator approval.";
  if (role === "yaml_blocked") return "Concrete ION action-like YAML failed local parsing or validation.";
  if (role === "yaml_duplicate") return "Concrete ION action YAML repeats an action_id already seen in this scan.";
  if (role === "composer_input") return "Composer text-entry zone detected for layout awareness only.";
  if (role === "send_button") return "Send/submit control detected; marked high-signal because silent sending is not allowed.";
  if (role === "attach_button") return "Attach/upload click target candidate detected for operator-visible file flow.";
  if (role === "voice_button") return "Voice control candidate detected near the composer.";
  if (role === "source_plane") return "Source/tool/context chip or connector surface detected near the composer.";
  if (role === "uploaded_attachment") return "Attachment or generated asset surface detected near the composer.";
  if (tone === "valid") return "High-signal marker; local validation sees this as usable evidence.";
  if (tone === "blocked") return "High-signal marker; local validation blocked this surface or packet.";
  return "Low-signal page perception marker; brighten by hovering nearby or focusing it.";
}

function registryBadgeDetail(host: HTMLElement, badge: HTMLElement): Record<string, string> {
  const text = registryText(host, "manual").trim();
  const rect = host.getBoundingClientRect();
  let selector = "";
  try {
    selector = selectorForElement(host);
  } catch (_error) {
    selector = host.tagName.toLowerCase();
  }
  const kind = badge.dataset.ionBadge ?? "";
  const role = badge.dataset.ionBadgeRole ?? "";
  const status = badge.dataset.tone ?? "";
  return {
    type: kind,
    role,
    category: registryBadgeCategory(kind, role),
    meaning: registryBadgeMeaning(kind, role, status),
    label: badge.dataset.ionLabel ?? "",
    status,
    rect: `${Math.round(rect.left)},${Math.round(rect.top)} ${Math.round(rect.width)}x${Math.round(rect.height)}`,
    selector,
    text: text.slice(0, 900),
  };
}

function addRegistryDetailRow(grid: HTMLElement, key: string, value: string): void {
  const keyNode = document.createElement("div");
  keyNode.className = "ion-registry-key";
  keyNode.textContent = key;
  const valueNode = document.createElement("div");
  valueNode.className = "ion-registry-value";
  valueNode.textContent = value || "-";
  grid.append(keyNode, valueNode);
}

function positionRegistryPopover(popover: HTMLElement, badge: HTMLElement): void {
  const rect = badge.getBoundingClientRect();
  const width = 320;
  const left = Math.min(Math.max(12, rect.left), Math.max(12, window.innerWidth - width - 12));
  const below = rect.bottom + 8;
  const top = below + 220 < window.innerHeight ? below : Math.max(12, rect.top - 230);
  popover.style.left = `${Math.round(left)}px`;
  popover.style.top = `${Math.round(top)}px`;
}

async function copyRegistryValue(label: string, value: string): Promise<void> {
  await copyBridgeResult(label, value);
  setBridgeStatus("Registry copied", label, "success");
}

function closeRegistryPopover(popover: HTMLElement | null): void {
  if (!popover?.isConnected) return;
  popover.remove();
  if (registryPopoverCloseHandler) {
    document.removeEventListener("pointerdown", registryPopoverCloseHandler, true);
    registryPopoverCloseHandler = null;
  }
  if (registryPopoverEscapeHandler) {
    document.removeEventListener("keydown", registryPopoverEscapeHandler);
    registryPopoverEscapeHandler = null;
  }
}

function showRegistryBadgeDetail(host: HTMLElement, badge: HTMLElement): void {
  const existingPopover = document.getElementById(DOM_REGISTRY_POPOVER_ID);
  if (existingPopover?.dataset.ionBadgeId && existingPopover.dataset.ionBadgeId === badge.dataset.ionBadgeId) {
    closeRegistryPopover(existingPopover);
    return;
  }
  closeRegistryPopover(existingPopover);
  const detail = registryBadgeDetail(host, badge);
  const popover = document.createElement("section");
  popover.id = DOM_REGISTRY_POPOVER_ID;
  popover.dataset.ionBadgeId = badge.dataset.ionBadgeId ?? "";
  popover.setAttribute("role", "dialog");
  popover.setAttribute("aria-label", "ION registry detail");

  const title = document.createElement("div");
  title.className = "ion-registry-title";
  title.textContent = detail.label || `${detail.type} ${detail.role}`.trim() || "ION registry marker";

  const grid = document.createElement("div");
  grid.className = "ion-registry-grid";
  addRegistryDetailRow(grid, "type", detail.type);
  addRegistryDetailRow(grid, "role", detail.role);
  addRegistryDetailRow(grid, "category", detail.category);
  addRegistryDetailRow(grid, "status", detail.status);
  addRegistryDetailRow(grid, "meaning", detail.meaning);
  addRegistryDetailRow(grid, "rect", detail.rect);
  addRegistryDetailRow(grid, "selector", detail.selector);
  if (detail.text) addRegistryDetailRow(grid, "text", detail.text);

  const actions = document.createElement("div");
  actions.className = "ion-registry-actions";
  const textButton = document.createElement("button");
  textButton.type = "button";
  textButton.textContent = "T";
  textButton.title = "Copy text";
  textButton.disabled = !detail.text;
  textButton.addEventListener("click", () => {
    void copyRegistryValue("ION registry text", registryText(host, "manual"));
  });
  const selectorButton = document.createElement("button");
  selectorButton.type = "button";
  selectorButton.textContent = "#";
  selectorButton.title = "Copy selector";
  selectorButton.addEventListener("click", () => {
    void copyRegistryValue("ION registry selector", detail.selector);
  });
  const detailButton = document.createElement("button");
  detailButton.type = "button";
  detailButton.textContent = "{}";
  detailButton.title = "Copy detail";
  detailButton.addEventListener("click", () => {
    void copyRegistryValue("ION registry detail", JSON.stringify(detail, null, 2));
  });
  const focusButton = document.createElement("button");
  focusButton.type = "button";
  focusButton.textContent = "◎";
  focusButton.title = "Focus element";
  focusButton.addEventListener("click", () => {
    host.scrollIntoView({ block: "center", inline: "nearest", behavior: "smooth" });
    host.animate([{ outlineColor: "rgba(255,255,255,0.95)" }, { outlineColor: "rgba(255,255,255,0.05)" }], { duration: 700 });
  });
  const closeButton = document.createElement("button");
  closeButton.type = "button";
  closeButton.textContent = "×";
  closeButton.title = "Close";
  closeButton.addEventListener("click", () => closeRegistryPopover(popover));
  actions.append(textButton, selectorButton, detailButton, focusButton, closeButton);

  popover.append(actions, title, grid);
  document.documentElement.appendChild(popover);
  positionRegistryPopover(popover, badge);
  popover.tabIndex = -1;
  if (registryPopoverCloseHandler) {
    document.removeEventListener("pointerdown", registryPopoverCloseHandler, true);
  }
  registryPopoverCloseHandler = (event: PointerEvent) => {
    const target = event.target as Element | null;
    if (!target) return;
    if (target.closest(`#${DOM_REGISTRY_POPOVER_ID}`) || target.closest(".ion-dom-badge")) return;
    closeRegistryPopover(popover);
  };
  document.addEventListener("pointerdown", registryPopoverCloseHandler, true);
  const escapeHandler = (event: KeyboardEvent) => {
    if (event.key !== "Escape") return;
    closeRegistryPopover(popover);
  };
  registryPopoverEscapeHandler = escapeHandler;
  document.addEventListener("keydown", registryPopoverEscapeHandler);
}

function ensureRegistryBadge(host: HTMLElement, kind: string, text: string, tone = "idle", role = ""): void {
  if (!registryBadgeCanAttach(host)) return;
  allowRegistryBadge(host);
  host.dataset.ionRegistryHost = "true";
  host.dataset.ionRegistryKind = kind;
  host.dataset.ionRegistryRole = role || kind;
  host.dataset.ionRegistryTone = tone;
  const existing = Array.from(host.children).find((child) => (child as HTMLElement).dataset?.ionBadge === kind) as HTMLElement | undefined;
  const badge = existing ?? document.createElement("span");
  badge.className = "ion-dom-badge";
  badge.dataset.ionBadge = kind;
  badge.dataset.ionBadgeKind = kind;
  badge.dataset.ionBadgeRole = role || kind;
  badge.dataset.ionLabel = text;
  badge.dataset.tone = tone;
  if (!badge.dataset.ionBadgeId) badge.dataset.ionBadgeId = `ion-badge-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  badge.textContent = "";
  badge.title = text;
  badge.setAttribute("aria-label", text);
  badge.setAttribute("role", "button");
  badge.tabIndex = 0;
  if (!badge.dataset.ionBadgeBound) {
    badge.dataset.ionBadgeBound = "true";
    badge.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      showRegistryBadgeDetail(host, badge);
    });
    badge.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      event.preventDefault();
      event.stopPropagation();
      showRegistryBadgeDetail(host, badge);
    });
  }
  if (!existing) host.appendChild(badge);
}

function captureLabel(node: HTMLElement): string {
  return `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.textContent ?? ""}`.replace(/\s+/g, " ").trim();
}

function noteCapture(stats: DomRegistryStats, node: HTMLElement, role: string, status = "healthy", label = ""): void {
  node.dataset.ionControlRole = role;
  node.dataset.ionCaptureStatus = status;
  if (label) node.dataset.ionCaptureLabel = label.slice(0, 80);
  ensureRegistryBadge(node, "control", `${role}${label ? `: ${label}` : ""}`, status === "approval_required" ? "blocked" : "idle", role);
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
    ensureRegistryBadge(node, "message", `ION msg ${index + 1} ${role}`, "idle", role);
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
    const actionLike = isIonActionPacketCandidateText(text);
    if (actionLike) {
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
    if (!actionLike) badge = `ION CODE #${index + 1}`;
    ensureRegistryBadge(host, "code", badge, tone, host.dataset.ionYamlStatus === "none" ? "code" : `yaml_${host.dataset.ionYamlStatus}`);
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
  setBridgeMonitorMetrics({
    actionCandidateCount: stats.validActions + stats.invalidActions + stats.duplicateActions,
    validActionCount: stats.validActions,
    blockedActionCount: stats.invalidActions,
    duplicateActionCount: stats.duplicateActions,
    codeBlockCount: stats.codeBlocks,
    composerControlCount: stats.composerControls,
    selectedSourceCount: stats.selectedSources.length,
    uploadedAttachmentCount: stats.uploadedAttachments,
  });
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
      "Marker legend:",
      "grey = readable message chunk",
      "blue = code/source or drop surface",
      "green = attach/asset or locally valid candidate",
      "amber = send/high-signal approval or locally blocked candidate",
      "violet = duplicate action candidate",
      "low-signal markers stay dim until hover/focus; high-signal markers stay visible.",
      "",
      "Automation markers are visual only. They do not click, submit, upload, or mutate ION state.",
    ].join("\n"),
  );
  return stats;
}

function ensureAssetCaptureStyle(): void {
  if (document.getElementById(ASSET_CAPTURE_STYLE_ID)) return;
  const style = document.createElement("style");
  style.id = ASSET_CAPTURE_STYLE_ID;
  style.textContent = `
    .${ASSET_CAPTURE_BUTTON_CLASS} {
      position: fixed;
      z-index: 2147482500;
      width: 28px;
      height: 28px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.72);
      background: radial-gradient(circle at 35% 22%, #ffffff, #ff701c 42%, #161616 78%);
      color: #ffffff;
      font: 800 8px/1 ui-sans-serif, system-ui, sans-serif;
      letter-spacing: 0.02em;
      box-shadow: 0 8px 22px rgba(0,0,0,0.34), 0 0 0 3px rgba(255,112,28,0.22);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0;
    }
    .${ASSET_CAPTURE_BUTTON_CLASS}:hover {
      transform: translateY(-1px) scale(1.04);
      box-shadow: 0 10px 26px rgba(0,0,0,0.38), 0 0 0 4px rgba(255,112,28,0.30);
    }
  `;
  document.documentElement.appendChild(style);
}

function clearAssetCaptureButtons(): void {
  document.querySelectorAll(`.${ASSET_CAPTURE_BUTTON_CLASS}`).forEach((node) => node.remove());
}

function assetCaptureLabel(node: HTMLElement): string {
  return `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.getAttribute("download") ?? ""} ${node.textContent ?? ""}`.replace(/\s+/g, " ").trim();
}

function assetSourceUrl(node: HTMLElement): string {
  if (node instanceof HTMLImageElement) return node.currentSrc || node.src || "";
  if (node instanceof HTMLAnchorElement) return node.href || "";
  const anchor = node.closest<HTMLAnchorElement>("a[href]");
  return anchor?.href ?? "";
}

function assetFilename(node: HTMLElement, url: string): string {
  const download = node.getAttribute("download") || node.closest<HTMLAnchorElement>("a[download]")?.getAttribute("download") || "";
  if (download.trim()) return download.trim();
  const label = assetCaptureLabel(node).replace(/[^A-Za-z0-9._ -]+/g, "_").trim();
  if (label && label.length <= 80) return label;
  try {
    const parsed = new URL(url);
    const basename = parsed.pathname.split("/").filter(Boolean).pop();
    if (basename) return basename;
  } catch (_error) {
    // Fall through to generated name.
  }
  return node instanceof HTMLImageElement ? "chatgpt-image.png" : "chatgpt-asset.bin";
}

function chatgptAssetCandidates(): HTMLElement[] {
  const selector = [
    "img[src]",
    "a[href]",
    "a[download]",
    "button[aria-label*='download' i]",
    "button[data-testid*='download' i]",
    "[role='button'][aria-label*='download' i]",
    "[data-testid*='download' i]",
    "[data-testid*='attachment' i]",
  ].join(",");
  const candidates: HTMLElement[] = [];
  const seen = new Set<Element>();
  document.querySelectorAll<HTMLElement>(selector).forEach((node) => {
    const host = (node.closest<HTMLElement>("a, button, [role='button']") ?? node);
    if (seen.has(host) || isBridgeElement(host) || shouldIgnoreScanNode(host) || !registryRectVisible(host)) return;
    const assistantHost = host.closest("[data-message-author-role='assistant'], article");
    const label = assetCaptureLabel(host).toLowerCase();
    const url = assetSourceUrl(host).toLowerCase();
    const rect = host.getBoundingClientRect();
    const isImageAsset = host instanceof HTMLImageElement && rect.width >= 96 && rect.height >= 96;
    const isDownloadAsset = /download|attachment|file|image|document|open/.test(label) || /download|attachment|file|image|sandbox|conversation/.test(url);
    if (!assistantHost && !isDownloadAsset) return;
    if (!isImageAsset && !isDownloadAsset) return;
    seen.add(host);
    candidates.push(host);
  });
  return candidates.slice(0, 12);
}

function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const value = String(reader.result ?? "");
      resolve(value.includes(",") ? value.split(",", 2)[1] : value);
    };
    reader.onerror = () => reject(reader.error ?? new Error("blob_read_failed"));
    reader.readAsDataURL(blob);
  });
}

async function captureChatgptAsset(node: HTMLElement): Promise<void> {
  const sourceUrl = assetSourceUrl(node);
  const payload: Record<string, unknown> = {
    asset_kind: node instanceof HTMLImageElement ? "chatgpt_image" : "chatgpt_downloadable",
    filename: assetFilename(node, sourceUrl),
    content_type: node instanceof HTMLImageElement ? "image/png" : "application/octet-stream",
    source_url: sourceUrl,
    page_url: window.location.href,
    chat_context_hint: node.closest("[data-message-author-role='assistant'], article")?.textContent?.slice(0, 700) ?? "",
    dom_summary: {
      tag: node.tagName.toLowerCase(),
      label: assetCaptureLabel(node),
      selector: selectorForElement(node),
    },
  };
  try {
    if (sourceUrl) {
      const response = await fetch(sourceUrl);
      if (!response.ok) throw new Error(`asset_fetch_failed_${response.status}`);
      const blob = await response.blob();
      payload.content_type = response.headers.get("content-type") || blob.type || payload.content_type;
      payload.data_base64 = await blobToBase64(blob);
    } else {
      payload.text = assetCaptureLabel(node) || node.textContent || "ChatGPT asset metadata captured without downloadable URL.";
      payload.content_type = "text/plain; charset=utf-8";
    }
  } catch (error) {
    payload.text = [
      "ChatGPT asset metadata captured; direct byte fetch failed in browser context.",
      `source_url: ${sourceUrl || "none"}`,
      `error: ${error instanceof Error ? error.message : String(error)}`,
      `label: ${assetCaptureLabel(node)}`,
    ].join("\n");
    payload.content_type = "text/plain; charset=utf-8";
  }
  setBridgeStatus("Capturing ChatGPT asset", String(payload.filename ?? "asset"), "working");
  chrome.runtime.sendMessage({ type: "ion_chatops_asset_capture", payload }, async (response) => {
    const result = response?.result ?? {};
    const detail = response?.ok ? compactJson(result, 1600) : blockedDetail(response);
    setBridgeArtifactDetail(detail);
    setBridgeStatus(response?.ok ? "Asset captured for ION" : "Asset capture blocked", detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
    if (response?.ok) await copyBridgeResult("ION asset capture", detail);
  });
}

function renderChatgptAssetCaptureButtons(): void {
  clearAssetCaptureButtons();
}

function ensureCaptureFrameStyle(): void {
  if (document.getElementById(`${CAPTURE_FRAME_ID}-style`)) return;
  const style = document.createElement("style");
  style.id = `${CAPTURE_FRAME_ID}-style`;
  style.textContent = `
    #${CAPTURE_FRAME_ID} {
      position: fixed;
      z-index: 2147482600;
      min-width: 52px;
      min-height: 34px;
      border: 2px solid #38bdf8;
      border-radius: 16px;
      background: rgba(56,189,248,0.06);
      box-shadow: 0 0 0 4px rgba(56,189,248,0.16), 0 18px 50px rgba(0,0,0,0.26);
      cursor: grab;
      pointer-events: auto;
      transition: width 120ms ease, height 120ms ease, left 120ms ease, top 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
    }
    #${CAPTURE_FRAME_ID}[data-dragging="true"] {
      cursor: grabbing;
      transition: none;
      border-color: #ff701c;
      box-shadow: 0 0 0 4px rgba(255,112,28,0.18), 0 18px 50px rgba(0,0,0,0.30);
    }
    #${CAPTURE_FRAME_ID}::before {
      content: attr(data-label);
      position: absolute;
      left: 10px;
      top: -28px;
      max-width: min(460px, calc(100vw - 40px));
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      padding: 5px 8px;
      border-radius: 999px;
      color: #07110d;
      background: #38bdf8;
      font: 800 10px/1 ui-sans-serif, system-ui, sans-serif;
      letter-spacing: 0.04em;
      box-shadow: 0 8px 18px rgba(0,0,0,0.22);
    }
  `;
  document.documentElement.appendChild(style);
}

function captureFrameElement(): HTMLElement {
  ensureCaptureFrameStyle();
  let frame = document.getElementById(CAPTURE_FRAME_ID) as HTMLElement | null;
  if (frame) return frame;
  frame = document.createElement("div");
  frame.id = CAPTURE_FRAME_ID;
  frame.dataset.label = "ION capture frame";
  frame.addEventListener("pointerdown", (event) => {
    event.preventDefault();
    frame?.setPointerCapture?.(event.pointerId);
    if (!frame) return;
    frame.dataset.dragging = "true";
    const rect = frame.getBoundingClientRect();
    const offsetX = event.clientX - rect.left;
    const offsetY = event.clientY - rect.top;
    const move = (moveEvent: PointerEvent) => {
      const width = rect.width;
      const height = rect.height;
      frame!.style.left = `${Math.max(4, Math.min(window.innerWidth - width - 4, moveEvent.clientX - offsetX))}px`;
      frame!.style.top = `${Math.max(34, Math.min(window.innerHeight - height - 4, moveEvent.clientY - offsetY))}px`;
      updateCaptureFrameLayersFromFrame(false);
    };
    const up = () => {
      frame!.dataset.dragging = "false";
      document.removeEventListener("pointermove", move, true);
      document.removeEventListener("pointerup", up, true);
      updateCaptureFrameLayersFromFrame(true);
    };
    document.addEventListener("pointermove", move, true);
    document.addEventListener("pointerup", up, true);
  });
  frame.addEventListener("wheel", (event) => {
    event.preventDefault();
    if (!captureFrameLayers.length) updateCaptureFrameLayersFromFrame(false);
    if (!captureFrameLayers.length) return;
    captureFrameLayerIndex = (captureFrameLayerIndex + (event.deltaY > 0 ? 1 : -1) + captureFrameLayers.length) % captureFrameLayers.length;
    applyCaptureFrameLayer(captureFrameLayerIndex, true);
  }, { passive: false });
  document.documentElement.appendChild(frame);
  return frame;
}

function captureFrameSave(selector: string, label: string): void {
  try {
    window.localStorage?.setItem(CAPTURE_FRAME_SELECTOR_KEY, selector);
  } catch (_error) {
    setBridgeSettingsDetail("Capture frame selector could not be saved to localStorage.");
    return;
  }
  setBridgeSettingsDetail(`capture_frame_saved\nselector: ${selector}\nlabel: ${label}\nScroll on the blue frame to switch stacked DOM layers.`);
}

function captureFrameLayerStack(x: number, y: number): Array<{ index: number; element: HTMLElement; label: string; selector: string }> {
  const seenElements = new Set<Element>();
  return document.elementsFromPoint(x, y)
    .filter((node): node is HTMLElement => node instanceof HTMLElement)
    .filter((node) => {
      if (seenElements.has(node) || isBridgeElement(node) || !registryRectVisible(node)) return false;
      seenElements.add(node);
      return true;
    })
    .slice(0, 16)
    .map((element, index) => {
      const label = captureLabel(element) || element.getAttribute("data-testid") || element.tagName.toLowerCase();
      return {
        index,
        element,
        label: `${element.tagName.toLowerCase()}${label ? ` · ${label.slice(0, 72)}` : ""}`,
        selector: selectorForElement(element),
      };
    });
}

function updateCaptureFrameLayerList(): void {
  setBridgeInspectorLayers(captureFrameLayers.map((layer, index) => ({
    index,
    label: layer.label,
    selector: layer.selector,
  })), captureFrameLayerIndex);
}

function updateCaptureFrameLayersFromFrame(lockActive: boolean): void {
  const frame = document.getElementById(CAPTURE_FRAME_ID) as HTMLElement | null;
  if (!frame) return;
  const rect = frame.getBoundingClientRect();
  captureFrameLayers = captureFrameLayerStack(rect.left + rect.width / 2, rect.top + rect.height / 2);
  captureFrameLayerIndex = Math.min(captureFrameLayerIndex, Math.max(0, captureFrameLayers.length - 1));
  updateCaptureFrameLayerList();
  if (lockActive && captureFrameLayers.length) applyCaptureFrameLayer(captureFrameLayerIndex, true);
}

function applyCaptureFrameLayer(index: number, save: boolean): void {
  const layer = captureFrameLayers[index];
  const frame = captureFrameElement();
  if (!layer) {
    frame.dataset.label = "No page element under frame";
    return;
  }
  const rect = layer.element.getBoundingClientRect();
  frame.style.left = `${Math.max(4, rect.left)}px`;
  frame.style.top = `${Math.max(34, rect.top)}px`;
  frame.style.width = `${Math.max(52, rect.width)}px`;
  frame.style.height = `${Math.max(34, rect.height)}px`;
  frame.dataset.label = `${index + 1}/${captureFrameLayers.length} ${layer.label}`;
  updateCaptureFrameLayerList();
  if (save) captureFrameSave(layer.selector, layer.label);
}

function captureActiveFrameElement(): void {
  const layer = captureFrameLayers[captureFrameLayerIndex];
  if (!layer?.element) {
    setBridgeSettingsDetail("capture_frame_asset_failed\nNo active framed element. Use Frame Capture first, drag the border over an element, then scroll to select a layer.");
    setBridgeStatus("Capture framed blocked", "No active framed element.", "error");
    return;
  }
  captureFrameSave(layer.selector, layer.label);
  setBridgeSettingsDetail([
    "capture_frame_asset_requested",
    `selector: ${layer.selector}`,
    `label: ${layer.label}`,
    "The framed element will be captured through the same ION asset queue path.",
  ].join("\n"));
  void captureChatgptAsset(layer.element);
}

function startCaptureFrame(): void {
  const frame = captureFrameElement();
  const width = Math.min(360, Math.max(220, window.innerWidth * 0.32));
  const height = Math.min(180, Math.max(110, window.innerHeight * 0.18));
  frame.style.left = `${Math.round((window.innerWidth - width) / 2)}px`;
  frame.style.top = `${Math.round((window.innerHeight - height) / 2)}px`;
  frame.style.width = `${Math.round(width)}px`;
  frame.style.height = `${Math.round(height)}px`;
  frame.dataset.label = "Drag frame; scroll on it to cycle layers";
  updateCaptureFrameLayersFromFrame(false);
  if (captureFrameTimer !== null) window.clearTimeout(captureFrameTimer);
  captureFrameTimer = window.setTimeout(() => {
    captureFrameTimer = null;
    document.getElementById(CAPTURE_FRAME_ID)?.remove();
    setBridgeStatus("Capture frame closed", "30 second capture window ended. Saved selector remains in Settings.", "idle");
  }, CAPTURE_FRAME_TIMEOUT_MS);
  setBridgeStatus("Capture frame active", "Drag the blue frame over the target, then scroll on it to cycle stacked DOM layers.", "working");
}

function loadCaptureFrame(): void {
  const selector = window.localStorage?.getItem(CAPTURE_FRAME_SELECTOR_KEY) ?? "";
  if (!selector) {
    setBridgeSettingsDetail("capture_frame_load_failed\nNo saved capture frame selector.");
    setBridgeStatus("Capture frame not loaded", "No saved selector exists yet.", "error");
    return;
  }
  let node: HTMLElement | null = null;
  try {
    node = document.querySelector<HTMLElement>(selector);
  } catch (_error) {
    setBridgeSettingsDetail(`capture_frame_load_failed\nselector_invalid: ${selector}`);
  }
  if (!node || isBridgeElement(node) || !registryRectVisible(node)) {
    setBridgeSettingsDetail(`capture_frame_load_failed\nselector_missing_or_hidden: ${selector}`);
    setBridgeStatus("Capture frame not loaded", "Saved selector is missing or hidden.", "error");
    return;
  }
  captureFrameLayers = [{
    index: 0,
    element: node,
    label: captureLabel(node) || node.tagName.toLowerCase(),
    selector,
  }];
  captureFrameLayerIndex = 0;
  applyCaptureFrameLayer(0, false);
  setBridgeStatus("Capture frame loaded", selector, "success");
}

function deleteCaptureFrame(): void {
  try {
    window.localStorage?.removeItem(CAPTURE_FRAME_SELECTOR_KEY);
  } catch (_error) {
    // Ignore localStorage failures.
  }
  if (captureFrameTimer !== null) window.clearTimeout(captureFrameTimer);
  captureFrameTimer = null;
  captureFrameLayers = [];
  captureFrameLayerIndex = 0;
  document.getElementById(CAPTURE_FRAME_ID)?.remove();
  setBridgeInspectorLayers([], 0);
  setBridgeSettingsDetail("capture_frame_deleted\nSaved capture selector cleared.");
  setBridgeStatus("Capture frame deleted", "Saved capture selector cleared.", "idle");
}

function shouldIgnoreScanNode(node: Element): boolean {
  if (typeof node.closest !== "function") return false;
  return Boolean(
    node.closest(`#${PANEL_ID}`) ??
      node.closest(`#${MODAL_ID}`) ??
      node.closest(`#${SETTINGS_CONTROL_PAD_ID}`) ??
      node.closest(`#${MESSAGE_QUEUE_FILE_INPUT_ID}`) ??
      node.closest(`#${CHATGPT_LEFT_ICON_DOCK_ID}`) ??
      node.closest(`.${CHATGPT_LEFT_ICON_DOCK_CLASS}`) ??
        node.closest(`.${ASSET_CAPTURE_BUTTON_CLASS}`) ??
        node.closest(`#${CAPTURE_FRAME_ID}`) ??
      node.closest("[data-message-author-role='user']") ??
      node.closest("#prompt-textarea") ??
      node.closest("[contenteditable='true']") ??
      node.closest("textarea"),
  );
}

function concreteIonFieldValue(text: string, key: string): string {
  const match = text.match(new RegExp(`^\\s+${key}\\s*:\\s*(.+?)\\s*(?:#.*)?$`, "im"));
  const value = match?.[1]?.trim().replace(/^['"]|['"]$/g, "") ?? "";
  if (!value || value === "..." || /^<[^>]+>$/.test(value) || /^TODO|TBD$/i.test(value)) return "";
  return value;
}

function isIonActionPacketCandidateText(text: string): boolean {
  const yaml = extractIonActionYaml(text);
  if (!yaml) return false;
  if (!concreteIonFieldValue(yaml, "schema").match(/^ion\.chatops\.action\.v1$/)) return false;
  if (!concreteIonFieldValue(yaml, "action_id")) return false;
  if (!concreteIonFieldValue(yaml, "intent")) return false;
  const hasActor = /^\s+actor\s*:\s*(?:#.*)?$/im.test(yaml) || Boolean(concreteIonFieldValue(yaml, "callsign") || concreteIonFieldValue(yaml, "carrier"));
  const hasAuthority =
    /^\s+authority\s*:\s*(?:#.*)?$/im.test(yaml) ||
    Boolean(
      concreteIonFieldValue(yaml, "human_sovereign") ||
        concreteIonFieldValue(yaml, "requires_approval") ||
        concreteIonFieldValue(yaml, "production_authority") ||
        concreteIonFieldValue(yaml, "live_execution_authority"),
    );
  return hasActor && hasAuthority;
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
        if (!isIonActionPacketCandidateText(extracted)) continue;
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

function requestBoundedAgentRead(type: "ion_chatops_bounded_agent_status" | "ion_chatops_agent_relay_pending" | "ion_chatops_agent_receipts_recent", label: string): void {
  setBridgeStatus(label, "Reading bounded agent lane from the Action Gateway.", "working");
  chrome.runtime.sendMessage({ type, payload: {} }, async (response) => {
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

function normalizeDocsStateFromResponse(result: any): DocsBrowseState {
  const incomingEntries = Array.isArray(result?.entries) ? result.entries : [];
  const entries = incomingEntries.map((row: any) => ({
    kind: row?.kind === "file" ? "file" : "folder",
    name: String(row?.name || row?.path || "").trim(),
    path: String(row?.path || "").trim(),
    size_bytes: typeof row?.size_bytes === "number" ? row.size_bytes : undefined,
    thumbnail: typeof row?.thumbnail === "string" ? row.thumbnail : undefined,
  })).filter((entry: DocsEntry) => entry.path);
  return {
    roots: Array.isArray(result?.roots) ? result.roots.filter((row: any) => typeof row === "string" && row.trim()) : defaultDocsState.roots,
    currentRoot: String(result?.current_root ?? result?.currentRoot ?? docsState.currentRoot ?? ""),
    currentPath: String(result?.path ?? result?.current_path ?? docsState.currentPath ?? ""),
    query: String(result?.query ?? docsState.query ?? ""),
    breadcrumbs: Array.isArray(result?.breadcrumbs) ? result.breadcrumbs.filter((row: any) => typeof row === "string") : [],
    entries,
    selectedPath: String(result?.selected_path ?? result?.selectedPath ?? docsState.selectedPath ?? ""),
    selectedDocName: String(result?.selected_doc_name ?? result?.selectedDocName ?? docsState.selectedDocName ?? ""),
    status: String(result?.status ?? docsState.status ?? "Docs browser updated."),
  };
}

function requestDocsBrowse(params: { path?: string; query?: string; root?: string } = {}): void {
  const payload: Record<string, unknown> = {
    path: params.path ?? docsState.currentPath,
    query: params.query ?? docsState.query,
    root: params.root ?? docsState.currentRoot,
  };
  setBridgeStatus("Docs browse", "Loading docs directory and file list.", "working");
  chrome.runtime.sendMessage({ type: "ion_chatops_docs_browse", payload }, async (response) => {
    if (!response?.ok) {
      const detail = blockedDetail(response);
      setBridgeStatus("Docs browse blocked", detail, "error");
      setBridgeDocsState({ ...docsState, status: detail });
      return;
    }
    docsState = normalizeDocsStateFromResponse(response.result);
    setBridgeDocsState(docsState);
    setBridgeStatus("Docs browser ready", docsState.currentPath || "Home", "success");
    await copyBridgeResult("Docs browse", compactJson(response.result));
  });
}

function requestDocsOpenRoot(event?: CustomEvent<{ path?: string }> | Event): void {
  const path = (event as CustomEvent<{ path?: string }>)?.detail?.path;
  docsState.currentPath = path ? path : "";
  docsState.currentRoot = path || "";
  docsState.query = "";
  requestDocsBrowse({ path: docsState.currentPath, root: docsState.currentRoot });
}

function requestDocsOpenFolder(detail: { path: string; query?: string }): void {
  const path = (detail?.path ?? "").trim();
  if (!path) {
    requestDocsOpenRoot();
    return;
  }
  docsState.currentPath = path;
  requestDocsBrowse({ path, query: detail.query ?? docsState.query, root: docsState.currentRoot });
}

function requestDocsOpenParent(): void {
  if (!docsState.currentPath) {
    requestDocsOpenRoot();
    return;
  }
  const parts = docsState.currentPath.split("/").filter(Boolean);
  const parent = parts.slice(0, -1).join("/");
  docsState.currentPath = parent;
  requestDocsBrowse({ path: parent, root: docsState.currentRoot });
}

function requestDocsSearch(query: string): void {
  docsState.query = query;
  requestDocsBrowse({ path: docsState.currentPath, query, root: docsState.currentRoot });
}

function setDocsStatus(status: string): void {
  docsState = { ...docsState, status };
  setBridgeDocsState(docsState);
}

function setDocsFavoriteStatus(path: string, status: string): void {
  docsDropFavoritePath = path;
  const favorites = DOCS_FAVORITE_ROOTS.map((favorite) => favorite.path === path ? { ...favorite, status } : favorite);
  setBridgeDocsFavorites(favorites);
}

function stopDocsDropProgress(): void {
  if (docsDropProgressTimer !== null) {
    window.clearInterval(docsDropProgressTimer);
  docsDropProgressTimer = null;
}
}

function startDocsDropProgress(label: string): void {
  stopDocsDropProgress();
  let progress = 8;
  setDocsStatus(`Zipping ${label}... ${progress}%`);
  if (docsDropFavoritePath) setDocsFavoriteStatus(docsDropFavoritePath, `ZIP ${progress}%`);
  docsDropProgressTimer = window.setInterval(() => {
    progress = Math.min(92, progress + (progress < 55 ? 13 : 5));
    setDocsStatus(`Zipping ${label}... ${progress}%`);
    if (docsDropFavoritePath) setDocsFavoriteStatus(docsDropFavoritePath, `ZIP ${progress}%`);
  }, 360);
}

function requestDocsDrop(path: string): void {
  const resolvedPath = normalizeDocsArtifactPath(path);
  if (!resolvedPath) {
    setBridgeArtifactDetail("docs_drop_failed: no_path_selected");
    setBridgeStatus("Docs drop blocked", "No doc path was provided for zip-drop.", "error");
    return;
  }
  const displayName = resolvedPath.split("/").pop() || "doc";
  docsDropFavoritePath = resolvedPath;
  startDocsDropProgress(displayName);
  setBridgeStatus("Docs drop", "Preparing selected doc for auto-zip drag/drop.", "working");
  chrome.runtime.sendMessage({
    type: "ion_chatops_docs_prepare_drop",
    payload: {
      path: resolvedPath,
      root: docsState.currentRoot,
      user_gesture: "docs_panel_dragstart",
    },
  }, async (response) => {
    const detail = response?.ok ? compactJson(response.result) : blockedDetail(response);
    setBridgeArtifactDetail(detail);
    setBridgeStatus(response?.ok ? "Docs artifact ready" : "Docs drop blocked", detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
    stopDocsDropProgress();
    if (!response?.ok) {
      setDocsFavoriteStatus(resolvedPath, "Blocked");
      setDocsStatus(`Zip-drop blocked: ${detail.split("\n")[0] ?? "prepare failed"}`);
      return;
    }
    setDocsFavoriteStatus(resolvedPath, "ZIP 100%");
    setDocsStatus(`ZIP ready 100%. Dropping ${response.result?.filename ?? displayName}...`);
    await attemptPreparedArtifactDrop(response.result);
    setDocsFavoriteStatus(resolvedPath, "Drop sent");
    setDocsStatus(`Drop attempted: ${response.result?.filename ?? displayName}`);
  });
}

function docsBrowsePromise(path: string): Promise<any> {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({
      type: "ion_chatops_docs_browse",
      payload: {
        path,
        root: path,
        query: "",
      },
    }, (response) => resolve(response));
  });
}

function contextPackageProjectKey(name: string): string {
  const clean = name
    .replace(/\.(zip|tar|gz|json|md)$/i, "")
    .replace(/[_-]?\d{8}(?:[_-]\d{4,6})?$/i, "")
    .replace(/[_-]?v\d+(?:[._-]\d+)*(?:[_-]?[a-z]+)?$/i, "")
    .replace(/[_-]?context[_-]?package$/i, "")
    .replace(/[_-]+/g, " ")
    .trim();
  return clean || name;
}

function contextPackageVersion(name: string): string {
  const version = name.match(/\bv\d+(?:[._-]\d+)*/i)?.[0] ?? "";
  const date = name.match(/\b20\d{6}(?:[_-]\d{4,6})?\b/)?.[0] ?? "";
  return [version, date].filter(Boolean).join(" · ") || "latest";
}

function contextPackageScore(name: string): number {
  const date = name.match(/\b(20\d{6})(?:[_-](\d{4,6}))?\b/);
  const dateScore = date ? Number(`${date[1]}${(date[2] ?? "000000").padEnd(6, "0")}`) : 0;
  const version = name.match(/\bv(\d+(?:[._-]\d+)*)/i)?.[1] ?? "";
  const versionScore = version
    .split(/[._-]/)
    .filter(Boolean)
    .slice(0, 4)
    .reduce((score, part) => score * 1000 + (Number.parseInt(part, 10) || 0), 0);
  return dateScore * 1000000000 + versionScore;
}

function isIonContextPackage(entry: DocsEntry): boolean {
  const text = `${entry.name} ${entry.path}`.toLowerCase();
  return (
    entry.kind === "folder" ||
    text.includes("context") ||
    text.includes("package") ||
    text.includes("capsule") ||
    text.endsWith(".zip")
  );
}

function latestProjectPackages(entries: ProjectPackageEntry[]): ProjectPackageEntry[] {
  const latest = new Map<string, ProjectPackageEntry>();
  for (const entry of entries) {
    const key = entry.project.toLowerCase();
    const existing = latest.get(key);
    if (!existing || entry.score > existing.score || (entry.score === existing.score && entry.name > existing.name)) {
      latest.set(key, entry);
    }
  }
  return Array.from(latest.values())
    .map((entry) => ({ ...entry, latest: true }))
    .sort((a, b) => b.score - a.score || a.project.localeCompare(b.project));
}

async function requestProjectsRefresh(): Promise<void> {
  setBridgeStatus("Projects scan", "Scanning ION context-package folders.", "working");
  setBridgeProjectsState({
    status: "Scanning ION context-package folders...",
    roots: PROJECT_CONTEXT_PACKAGE_ROOTS,
    packages: projectPackages,
    selectedPath: selectedProjectPackagePath,
    selectedPaths: selectedProjectPackagePaths,
  });
  const discovered: ProjectPackageEntry[] = [];
  for (const root of PROJECT_CONTEXT_PACKAGE_ROOTS) {
    const response = await docsBrowsePromise(root);
    if (!response?.ok) continue;
    const state = normalizeDocsStateFromResponse(response.result);
    for (const entry of state.entries.filter(isIonContextPackage)) {
      const name = entry.name || entry.path.split("/").pop() || entry.path;
      discovered.push({
        project: contextPackageProjectKey(name),
        version: contextPackageVersion(name),
        name,
        path: entry.path,
        root,
        kind: entry.kind,
        latest: false,
        updated: contextPackageVersion(name),
        score: contextPackageScore(name),
      });
    }
  }
  projectPackages = latestProjectPackages(discovered);
  if (!selectedProjectPackagePath && projectPackages.length) selectedProjectPackagePath = projectPackages[0].path;
  if (selectedProjectPackagePath && !projectPackages.some((entry) => entry.path === selectedProjectPackagePath)) {
    selectedProjectPackagePath = projectPackages[0]?.path ?? "";
  }
  selectedProjectPackagePaths = selectedProjectPackagePaths.filter((path) => projectPackages.some((entry) => entry.path === path));
  if (!selectedProjectPackagePaths.length && selectedProjectPackagePath) {
    selectedProjectPackagePaths = [selectedProjectPackagePath];
  }
  setBridgeProjectsState({
    status: projectPackages.length
      ? `Found ${projectPackages.length} latest ION project context package(s). Use Context Sync to build one ZIP, or double-click a project to zip/drop it.`
      : "No ION context packages found in known package roots.",
    roots: PROJECT_CONTEXT_PACKAGE_ROOTS,
    packages: projectPackages,
    selectedPath: selectedProjectPackagePath,
    selectedPaths: selectedProjectPackagePaths,
    contextSyncStatus: projectPackages.length
      ? `${selectedProjectPackagePaths.length} project package(s) selected for context sync.`
      : "No ION context packages found in known package roots.",
  });
  setBridgeStatus(projectPackages.length ? "Projects ready" : "Projects empty", `${projectPackages.length} latest package(s)`, projectPackages.length ? "success" : "approval");
}

function requestProjectDrop(path: string): void {
  selectedProjectPackagePath = path || selectedProjectPackagePath;
  setBridgeProjectsState({ selectedPath: selectedProjectPackagePath, status: `Preparing project package drop: ${selectedProjectPackagePath}` });
  requestDocsDrop(selectedProjectPackagePath);
}

function requestProjectContextSync(paths: string[]): void {
  const projectPaths = Array.from(new Set(paths.map((path) => String(path ?? "").trim()).filter(Boolean)));
  if (!projectPaths.length) {
    setBridgeProjectsState({
      contextSyncOpen: true,
      contextSyncStatus: "Select at least one ION project context package before building a context sync ZIP.",
    });
    setBridgeStatus("Context sync blocked", "No project packages selected.", "error");
    return;
  }
  selectedProjectPackagePaths = projectPaths;
  setBridgeProjectsState({
    selectedPaths: projectPaths,
    contextSyncOpen: true,
    contextSyncStatus: `Requesting Braden approval for one context sync ZIP from ${projectPaths.length} project package(s)...`,
  });
  setBridgeStatus("Context sync ZIP", "Requesting Braden approval before local package compilation.", "working");
  chrome.runtime.sendMessage({
    type: "ion_chatops_project_context_sync_zip",
    payload: {
      project_paths: projectPaths,
      context_sync_source: "top_bar_context_sync",
    },
  }, async (response) => {
    const result = response?.result;
    const detail = response?.ok
      ? [
          `zip_path: ${result?.zip_path ?? ""}`,
          `zip_sha256: ${result?.zip_sha256 ?? ""}`,
          `manifest_path: ${result?.manifest_path ?? ""}`,
          `receipt_path: ${result?.receipt_path ?? ""}`,
          `selected_project_count: ${result?.selected_project_count ?? projectPaths.length}`,
        ].join("\n")
      : blockedDetail(response);
    setBridgeProjectsState({
      selectedPaths: projectPaths,
      contextSyncOpen: true,
      contextSyncStatus: response?.ok ? `Context sync ZIP ready for ${projectPaths.length} project package(s).` : detail,
      contextSyncZipPath: response?.ok ? String(result?.zip_path ?? "") : "",
      contextSyncSha256: response?.ok ? String(result?.zip_sha256 ?? "") : "",
    });
    setBridgePackageDetail(response?.ok ? `${detail}\n\n${compactJson(result, 1400)}` : detail);
    setBridgeStatus(response?.ok ? "Context sync ZIP ready" : "Context sync blocked", detail, response?.ok ? "success" : "error");
    if (response?.ok) await copyBridgeResult("Context sync ZIP", detail);
  });
}

function projectPathsOrDefault(paths: string[]): string[] {
  const selected = paths.map((path) => String(path ?? "").trim()).filter(Boolean);
  if (selected.length) return selected;
  if (selectedProjectPackagePath) return [selectedProjectPackagePath];
  if (projectPackages.length) return [projectPackages[0].path];
  return [];
}

function applyContextWorkflowSelectedPaths(nextPaths: string[]): void {
  selectedProjectPackagePaths = Array.from(new Set(nextPaths.map((path) => String(path ?? "").trim()).filter(Boolean)));
  selectedProjectPackagePaths = selectedProjectPackagePaths.filter((path) => projectPackages.some((entry) => entry.path === path));
  if (!selectedProjectPackagePaths.length && selectedProjectPackagePath) selectedProjectPackagePaths = [selectedProjectPackagePath];
  if (!selectedProjectPackagePaths.length && projectPackages.length) selectedProjectPackagePaths = [projectPackages[0].path];
  if (selectedProjectPackagePaths.length) selectedProjectPackagePath = selectedProjectPackagePaths[0];
  setBridgeProjectsState({
    selectedPath: selectedProjectPackagePath,
    selectedPaths: selectedProjectPackagePaths,
    contextSyncOpen: true,
    contextSyncStatus: selectedProjectPackagePaths.length
      ? `${selectedProjectPackagePaths.length} project package(s) selected for context sync.`
      : "No ION context package selected.",
  });
}

function scheduleAutoContextSync(paths: string[]): void {
  applyContextWorkflowSelectedPaths(paths);
  if (contextWorkflowAutoSyncTimer !== null) window.clearTimeout(contextWorkflowAutoSyncTimer);
  const projectPaths = projectPathsOrDefault(selectedProjectPackagePaths);
  if (!projectPaths.length) {
    setBridgeProjectsState({
      contextSyncOpen: true,
      contextSyncStatus: "No project package available for auto-sync.",
    });
    return;
  }
  contextWorkflowAutoSyncTimer = window.setTimeout(() => {
    contextWorkflowAutoSyncTimer = null;
    requestProjectContextSync(projectPaths);
  }, CONTEXT_WORKFLOW_AUTO_SYNC_DEBOUNCE_MS);
}

function renderContextWorkflowProjectSelect(selectedPaths: string[]): HTMLSelectElement {
  const projectSet = new Set(selectedPaths.filter(Boolean));
  const select = document.createElement("select");
  select.className = "ion-context-rail-project-select";
  select.dataset.contextWorkflowAction = "project-select";
  select.multiple = true;
  select.size = Math.min(6, Math.max(3, Math.min(projectPackages.length || 0, 6)));
  select.setAttribute("aria-label", "Select one or more ION project context packages to include in one context sync ZIP.");
  if (!projectPackages.length) {
    const none = document.createElement("option");
    none.value = "";
    none.textContent = "No context packages discovered";
    none.disabled = true;
    none.selected = true;
    select.appendChild(none);
    select.disabled = true;
    return select;
  }
  for (const entry of projectPackages) {
    const option = document.createElement("option");
    option.value = entry.path;
    option.textContent = `${entry.project} · ${entry.version || entry.name}`;
    option.title = `${entry.path}`;
    option.selected = projectSet.has(entry.path);
    select.appendChild(option);
  }
  return select;
}

function codexTurnsFromModel(model: any): Array<Record<string, any>> {
  const turns = model?.lanes?.codex_general?.turns;
  if (!Array.isArray(turns)) return [];
  return turns
    .filter((turn: any) => turn && typeof turn === "object")
    .map((turn: any) => ({
      turn_id: String(turn.turn_id ?? ""),
      author: String(turn.author ?? turn.kind ?? "codex"),
      kind: String(turn.kind ?? ""),
      message: String(turn.message ?? ""),
      created_at: String(turn.created_at ?? ""),
      chat_engine: turn.chat_engine && typeof turn.chat_engine === "object" ? turn.chat_engine : undefined,
      context_refs: Array.isArray(turn.context_refs) ? turn.context_refs.map((ref: any) => String(ref)) : undefined,
      skill_activation: turn.skill_activation && typeof turn.skill_activation === "object" ? turn.skill_activation : undefined,
      codex_model_move: turn.codex_model_move && typeof turn.codex_model_move === "object" ? turn.codex_model_move : undefined,
    }))
    .filter((turn) => turn.message);
}

function requestCodexChatModel(): void {
  setBridgeCodexState({ status: "Loading Codex Capsule chat...", submitting: false, queueing: false });
  chrome.runtime.sendMessage({ type: "ion_chatops_codex_chat_model" }, (response) => {
    const model = response?.result?.model;
    if (!response?.ok || !model) {
      setBridgeCodexState({ status: `Codex chat unavailable: ${blockedDetail(response)}`, submitting: false, queueing: false });
      return;
    }
    const queueCount = model?.codex_queue?.runner?.queued_request_count ?? model?.codex_queue?.runner?.queued_count ?? 0;
    setBridgeCodexState({
      status: `Mounted Codex Capsule chat. Queue: ${queueCount} pending.`,
      model,
      turns: codexTurnsFromModel(model),
      submitting: false,
      queueing: false,
    });
  });
}

function requestCodexChatTurn(message: string): void {
  const text = message.trim();
  if (!text) {
    setBridgeCodexState({ status: "Codex message required." });
    return;
  }
  setBridgeCodexState({ status: "Sending to Codex Capsule chat...", submitting: true });
  chrome.runtime.sendMessage({
    type: "ion_chatops_codex_chat_turn",
    payload: {
      lane_id: "codex_general",
      message: text,
      author: "operator",
      execution_mode: "respond_only",
    },
  }, (response) => {
    const model = response?.result?.model;
    if (!response?.ok || !model) {
      setBridgeCodexState({ status: `Codex turn failed: ${blockedDetail(response)}`, submitting: false });
      return;
    }
    setBridgeCodexState({
      status: "Codex response captured.",
      input: "",
      model,
      turns: codexTurnsFromModel(model),
      submitting: false,
    });
  });
}

function requestCodexChatQueue(message: string): void {
  const text = message.trim();
  if (!text) {
    setBridgeCodexState({ status: "Codex queue objective required." });
    return;
  }
  setBridgeCodexState({ status: "Queueing bounded Codex work request...", queueing: true });
  chrome.runtime.sendMessage({
    type: "ion_chatops_codex_chat_queue",
    payload: {
      lane_id: "codex_general",
      objective: text,
    },
  }, (response) => {
    const result = response?.result ?? {};
    const model = result?.model;
    const link = result?.queue_link ?? {};
    if (!response?.ok) {
      setBridgeCodexState({ status: `Codex queue blocked: ${blockedDetail(response)}`, queueing: false });
      return;
    }
    const nextState: Parameters<typeof setBridgeCodexState>[0] = {
      status: `Queued for Codex: ${link.request_id ?? "request created"}`,
      input: "",
      queueing: false,
    };
    if (model) nextState.turns = codexTurnsFromModel(model);
    if (model) nextState.model = model;
    setBridgeCodexState(nextState);
  });
}

function requestDocsOpenDoc(path: string, name: string): void {
  docsState.selectedPath = path;
  docsState.selectedDocName = name;
  setBridgeDocsState({ ...docsState, selectedPath: path, selectedDocName: name, status: `Selected ${name}` });
}

function normalizeDocsArtifactPath(rawPath: string): string {
  const path = String(rawPath ?? "").trim().replace(/\\/g, "/");
  if (!path) return "";
  if (path.startsWith("/") || /^[A-Za-z]:\//.test(path) || path.startsWith("~")) return path;
  if (docsState.currentRoot && path.startsWith(`${docsState.currentRoot}/`)) return path;
  if (docsState.currentPath) {
    if (path.startsWith(`${docsState.currentPath}/`)) return path;
    const leaf = docsState.currentPath.split("/").filter(Boolean).pop() ?? "";
    if (leaf && path === leaf) return `${docsState.currentPath}/${path}`;
  }
  if (docsState.currentRoot) return `${docsState.currentRoot}/${path}`;
  return path;
}

function visibleDropRect(element: HTMLElement): DOMRect | null {
  if (!visibleElement(element)) return null;
  const rect = element.getBoundingClientRect();
  if (
    element !== document.body &&
    (rect.width < 8 || rect.height < 8 || rect.bottom <= 0 || rect.right <= 0 || rect.top >= window.innerHeight || rect.left >= window.innerWidth)
  ) return null;
  if (element === document.body || rect.height > window.innerHeight * 1.2) {
    return {
      left: 8,
      top: 56,
      right: window.innerWidth - 8,
      bottom: window.innerHeight - 96,
      width: window.innerWidth - 16,
      height: Math.max(160, window.innerHeight - 152),
      x: 8,
      y: 56,
      toJSON: () => ({}),
    } as DOMRect;
  }
  return rect;
}

function dropZoneContainerFromElement(element: HTMLElement): HTMLElement {
  const composer = findComposer();
  const start = composer && elementContains(element, composer) ? composer : element;
  const candidates = [
    start.closest<HTMLElement>("form"),
    start.closest<HTMLElement>("[data-testid*='composer' i]"),
    start.closest<HTMLElement>("[class*='composer' i]"),
    start.closest<HTMLElement>("[class*='prompt' i]"),
    start.parentElement,
    element,
  ].filter(Boolean) as HTMLElement[];
  for (const candidate of candidates) {
    if (isBridgeElement(candidate)) continue;
    const rect = candidate.getBoundingClientRect();
    if (rect.width >= 300 && rect.height >= 54 && rect.bottom > window.innerHeight * 0.45) return candidate;
  }
  return element;
}

function storedDropSelector(): string {
  try {
    return targetMeta("drop_zone").selector;
  } catch (_error) {
    return "";
  }
}

function calibratedDropTargetElement(): HTMLElement | null {
  const selector = storedDropSelector();
  if (!selector) return null;
  let node: HTMLElement | null = null;
  try {
    node = document.querySelector<HTMLElement>(selector);
  } catch (_error) {
    setBridgeArtifactDetail(`calibrated_drop_selector_invalid\nselector: ${selector}`);
    return null;
  }
  if (!node || !visibleDropRect(node)) {
    setBridgeArtifactDetail(`calibrated_drop_target_missing_or_hidden\nselector: ${selector}`);
    return null;
  }
  return dropZoneContainerFromElement(node);
}

function defaultDropTargetElement(): HTMLElement | null {
  const composer = findComposer();
  const main = document.querySelector<HTMLElement>("main");
  const composerDropZone = composer ? dropZoneContainerFromElement(composer) : null;
  const composerShell =
    composer?.closest<HTMLElement>("form") ??
    composer?.closest<HTMLElement>("[data-testid*='composer']") ??
    null;
  const composerForm = composer?.closest("form");
  const composerRoot = composer?.closest<HTMLElement>("[role='region'], [data-testid*='composer']");
  const candidates = [composerDropZone, composerShell, composerForm, composerRoot, composer?.parentElement, main, document.body, composer].filter(Boolean) as HTMLElement[];
  return candidates.find((candidate) => visibleDropRect(candidate)) ?? null;
}

function findDropTarget(): HTMLElement | null {
  const calibrated = calibratedDropTargetElement();
  if (calibrated) return calibrated;
  if (storedDropSelector()) return null;
  return defaultDropTargetElement();
}

function composerRect(): DOMRect | null {
  const composer = findComposer();
  return composer?.getBoundingClientRect() ?? null;
}

function composerShellRect(): DOMRect | null {
  const composer = findComposer();
  if (!composer) return null;
  let best: HTMLElement | null = composer;
  let current: HTMLElement | null = composer;
  let depth = 0;
  while (current?.parentElement && depth < 10) {
    current = current.parentElement;
    depth += 1;
    if (isBridgeElement(current)) break;
    if (!visibleElement(current)) continue;
    const rect = current.getBoundingClientRect();
    const lower = rect.bottom > window.innerHeight * 0.58 && rect.top > window.innerHeight * 0.22;
    const plausibleWidth = rect.width >= Math.min(320, window.innerWidth * 0.40) && rect.width <= window.innerWidth * 0.92;
    const plausibleHeight = rect.height >= 36 && rect.height <= Math.max(430, window.innerHeight * 0.50);
    if (!lower || !plausibleWidth || !plausibleHeight) continue;
    const buttons = current.querySelectorAll("button, [role='button'], input[type='file']").length;
    if (buttons >= 2 || /form/i.test(current.tagName) || String(current.getAttribute("data-testid") ?? "").toLowerCase().includes("composer")) {
      best = current;
    }
  }
  return best?.getBoundingClientRect() ?? null;
}

function rectPayload(rect: DOMRect): Record<string, number> {
  return {
    x: Math.round(rect.left),
    y: Math.round(rect.top),
    width: Math.round(rect.width),
    height: Math.round(rect.height),
  };
}

function controlLabel(node: HTMLElement): string {
  return `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.textContent ?? ""}`.replace(/\s+/g, " ").trim();
}

function visibleElement(node: HTMLElement): boolean {
  const rect = node.getBoundingClientRect();
  return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
}

function isBridgeElement(element: Element): boolean {
  return Boolean(
      element.closest(`#${PANEL_ID}`) ??
      element.closest(`#${MODAL_ID}`) ??
      element.closest(`#${SETTINGS_CONTROL_PAD_ID}`) ??
      element.closest(`.${ASSET_CAPTURE_BUTTON_CLASS}`) ??
      element.closest(`#${CHATGPT_LEFT_ICON_DOCK_ID}`) ??
      element.closest(`.${CHATGPT_LEFT_ICON_DOCK_CLASS}`) ??
      element.closest(`#${CAPTURE_FRAME_ID}`) ??
      element.closest(`#${DOM_REGISTRY_STYLE_ID}`) ??
      element.closest(`#${DOM_REGISTRY_POPOVER_ID}`) ??
      element.closest(`#${ASSET_CAPTURE_STYLE_ID}`) ??
      element.closest(`#${INSPECTOR_HUD_ID}`) ??
      element.closest(`#${INSPECTOR_SELECTED_PREVIEW_ID}`) ??
      element.closest(`#${ATTACH_PREVIEW_ID}`) ??
      element.closest(`#${DROP_PREVIEW_ID}`) ??
      element.closest(`#${TABS_ANCHOR_PREVIEW_ID}`),
  );
}

function cssEscape(value: string): string {
  const css = (window as unknown as { CSS?: { escape?: (input: string) => string } }).CSS;
  if (typeof css?.escape === "function") return css.escape(value);
  return value.replace(/["\\#.;:[\]()>+~*=\s]/g, "\\$&");
}

function cssString(value: string): string {
  return value.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

function storedAttachSelector(): string {
  try {
    return targetMeta("attach_target").selector;
  } catch (_error) {
    return "";
  }
}

function storedTabsAnchorSelector(): string {
  try {
    return targetMeta("tabs_anchor").selector;
  } catch (_error) {
    return "";
  }
}

function elementWithinComposerBand(node: HTMLElement, rect: DOMRect | null): boolean {
  const bounds = node.getBoundingClientRect();
  if (!rect) return bounds.top > window.innerHeight * 0.45;
  const centerX = bounds.left + bounds.width / 2;
  const centerY = bounds.top + bounds.height / 2;
  const xMatch = centerX >= rect.left - 110 && centerX <= rect.right + 110;
  const yMatch = centerY >= rect.top - 260 && centerY <= rect.bottom + 160;
  return xMatch && yMatch;
}

function selectorForElement(node: HTMLElement): string {
  const id = node.id?.trim();
  if (id) return `#${cssEscape(id)}`;
  const tag = node.tagName.toLowerCase();
  const dataTestId = node.getAttribute("data-testid")?.trim();
  if (dataTestId) return `${tag}[data-testid="${cssString(dataTestId)}"]`;
  const aria = node.getAttribute("aria-label")?.trim();
  if (aria) return `${tag}[aria-label="${cssString(aria)}"]`;
  const title = node.getAttribute("title")?.trim();
  if (title) return `${tag}[title="${cssString(title)}"]`;

  const parts: string[] = [];
  let current: HTMLElement | null = node;
  let depth = 0;
  while (current && current.nodeType === Node.ELEMENT_NODE && depth < 5 && !isBridgeElement(current)) {
    const parent = current.parentElement;
    let part = current.tagName.toLowerCase();
    if (parent) {
      const siblings = Array.from(parent.children).filter((sibling) => sibling.tagName === current?.tagName);
      if (siblings.length > 1) part += `:nth-of-type(${siblings.indexOf(current) + 1})`;
    }
    parts.unshift(part);
    current = parent;
    depth += 1;
  }
  return parts.join(" > ");
}

const TARGET_ANCHOR_DEFAULTS: Record<InspectorSaveTarget, AnchorPoint> = {
  tabs_anchor: "bottom",
  drop_zone: "center",
  attach_target: "center",
};

function isAnchorPoint(value: unknown): value is AnchorPoint {
  return value === "top" || value === "left" || value === "center" || value === "right" || value === "bottom";
}

function readStoredTargetMeta(raw: string, fallback: AnchorPoint): TargetMetaInfo {
  if (!raw) return { selector: "", anchor: fallback };
  try {
    const parsed = JSON.parse(raw);
    const selector = typeof parsed?.selector === "string" ? parsed.selector.trim() : "";
    const anchor = isAnchorPoint(parsed?.anchor) ? parsed.anchor : fallback;
    return { selector: selector || "", anchor };
  } catch (_error) {
    return { selector: raw, anchor: fallback };
  }
}

function targetMetaStorageKey(target: InspectorSaveTarget): string {
  return target === "tabs_anchor" ? TABS_ANCHOR_SELECTOR_KEY : target === "drop_zone" ? DROP_TARGET_SELECTOR_KEY : ATTACH_TARGET_SELECTOR_KEY;
}

function targetMeta(target: InspectorSaveTarget): TargetMetaInfo {
  try {
    const storage = window.localStorage ?? window.sessionStorage;
    const raw = String(storage?.getItem(targetMetaStorageKey(target)) ?? "").trim();
    return readStoredTargetMeta(raw, TARGET_ANCHOR_DEFAULTS[target]);
  } catch (_error) {
    return { selector: "", anchor: TARGET_ANCHOR_DEFAULTS[target] };
  }
}

function saveTargetMeta(target: InspectorSaveTarget, selector: string, anchor: AnchorPoint): boolean {
  const key = targetMetaStorageKey(target);
  try {
    const storage = window.localStorage ?? window.sessionStorage;
    if (!storage) return false;
    storage.setItem(key, JSON.stringify({ selector: selector.trim(), anchor }));
    return true;
  } catch (_error) {
    return false;
  }
}

function clearTargetMeta(target: InspectorSaveTarget): boolean {
  try {
    const storage = window.localStorage ?? window.sessionStorage;
    if (storage) storage.removeItem(targetMetaStorageKey(target));
    return true;
  } catch (_error) {
    return false;
  }
}

function anchorForTarget(target: InspectorSaveTarget): AnchorPoint {
  return targetMeta(target).anchor;
}

function setInspectorAnchorTarget(target: InspectorSaveTarget): void {
  settingsInspectorTarget = target;
  settingsAnchorPoint = anchorForTarget(target);
}

function markerPointForRect(rect: AnchorRect, anchor: AnchorPoint): { x: number; y: number } {
  const left = rect.x;
  const top = rect.y;
  const right = rect.x + rect.width;
  const bottom = rect.y + rect.height;
  const centerX = left + rect.width / 2;
  const centerY = top + rect.height / 2;
  if (anchor === "left") return { x: left, y: centerY };
  if (anchor === "right") return { x: right, y: centerY };
  if (anchor === "top") return { x: centerX, y: top };
  if (anchor === "bottom") return { x: centerX, y: bottom };
  return { x: centerX, y: centerY };
}

function addAnchorMarker(overlay: HTMLElement, rect: AnchorRect, anchor: AnchorPoint, borderColor = "#ec4899"): void {
  const point = markerPointForRect(rect, anchor);
  const marker = document.createElement("span");
  marker.className = INSPECTOR_ANCHOR_MARKER_CLASS;
  marker.style.left = `${Math.round(point.x - rect.x)}px`;
  marker.style.top = `${Math.round(point.y - rect.y)}px`;
  marker.style.borderColor = borderColor;
  marker.style.color = borderColor;
  marker.style.boxShadow = `0 0 0 3px ${borderColor}55`;
  overlay.appendChild(marker);
}

function markerForTarget(target: InspectorSaveTarget): string {
  if (target === "tabs_anchor") return "#fb923c";
  if (target === "drop_zone") return "#60a5fa";
  return "#34d399";
}

function storageMetaFromTarget(target: InspectorSaveTarget): TargetMetaInfo {
  return targetMeta(target);
}

function inspectorNodeAllowed(node: Element): node is HTMLElement {
  if (!(node instanceof HTMLElement)) return false;
  if (isBridgeElement(node)) return false;
  if (node.id === INSPECTOR_HUD_ID || node.id === INSPECTOR_SELECTED_PREVIEW_ID) return false;
  if (node.classList.contains(INSPECTOR_OUTLINE_CLASS) || node.classList.contains("ion-dom-badge")) return false;
  if (!visibleElement(node)) return false;
  return true;
}

function inspectorLabel(node: HTMLElement, index: number): string {
  const tag = node.tagName.toLowerCase();
  const id = node.id ? `#${node.id}` : "";
  const role = node.getAttribute("role") ? `[role=${node.getAttribute("role")}]` : "";
  const testId = node.getAttribute("data-testid") ? `[data-testid=${node.getAttribute("data-testid")}]` : "";
  const aria = node.getAttribute("aria-label") || node.getAttribute("title") || "";
  const classes = Array.from(node.classList ?? []).filter(Boolean).slice(0, 3).map((name) => `.${name}`).join("");
  const label = controlLabel(node) || aria || node.textContent?.trim().slice(0, 60) || "";
  const rect = rectPayload(node.getBoundingClientRect());
  return `${index} ${tag}${id}${testId || role || classes} ${rect.x},${rect.y} ${rect.width}x${rect.height}${label ? ` - ${label}` : ""}`.replace(/\s+/g, " ").trim();
}

function inspectorLayersAt(x: number, y: number): InspectorLayer[] {
  const fromPoint = typeof document.elementsFromPoint === "function" ? document.elementsFromPoint(x, y) : [];
  const seenNodes = new Set<Element>();
  const layers: InspectorLayer[] = [];
  fromPoint.forEach((node) => {
    if (seenNodes.has(node) || !inspectorNodeAllowed(node)) return;
    seenNodes.add(node);
    const index = layers.length;
    layers.push({
      index,
      element: node,
      selector: selectorForElement(node),
      label: inspectorLabel(node, index),
      rect: rectPayload(node.getBoundingClientRect()),
    });
  });
  return layers.slice(0, 16);
}

function removeInspectorOutlines(): void {
  document.querySelectorAll(`.${INSPECTOR_OUTLINE_CLASS}`).forEach((node) => node.remove());
}

function removeInspectorHud(): void {
  document.getElementById(INSPECTOR_HUD_ID)?.remove();
}

function removeInspectorSelectedPreview(): void {
  document.getElementById(INSPECTOR_SELECTED_PREVIEW_ID)?.remove();
}

function removeInspectorChrome(): void {
  removeInspectorOutlines();
  removeInspectorHud();
  removeInspectorSelectedPreview();
}

function drawInspectorOutline(
  layer: InspectorLayer,
  selected = false,
  persistentId?: string,
  markerAnchor?: AnchorPoint,
  markerColor = "#ec4899",
): void {
  const overlay = document.createElement("div");
  overlay.className = INSPECTOR_OUTLINE_CLASS;
  if (persistentId) overlay.id = persistentId;
  overlay.dataset.layer = String(layer.index);
  overlay.dataset.selected = String(selected);
  overlay.style.left = `${layer.rect.x}px`;
  overlay.style.top = `${layer.rect.y}px`;
  overlay.style.width = `${layer.rect.width}px`;
  overlay.style.height = `${layer.rect.height}px`;
  const label = document.createElement("span");
  label.textContent = layer.label;
  overlay.appendChild(label);
  if (selected && markerAnchor) {
    const markerRect: AnchorRect = {
      x: layer.rect.x,
      y: layer.rect.y,
      width: layer.rect.width,
      height: layer.rect.height,
    };
    addAnchorMarker(overlay, markerRect, markerAnchor, markerColor);
  }
  document.documentElement.appendChild(overlay);
}

function drawInspectorLayers(layers: InspectorLayer[], selectedIndex = -1): void {
  removeInspectorOutlines();
  layers.slice(0, 10).forEach((layer) => drawInspectorOutline(layer, layer.index === selectedIndex));
}

function updateInspectorHud(x: number, y: number, layers: InspectorLayer[], locked = false): void {
  let hud = document.getElementById(INSPECTOR_HUD_ID);
  if (!hud) {
    hud = document.createElement("div");
    hud.id = INSPECTOR_HUD_ID;
    document.documentElement.appendChild(hud);
  }
  const left = Math.min(window.innerWidth - 24, Math.max(12, x + 14));
  const top = Math.min(window.innerHeight - 28, Math.max(12, y + 14));
  hud.style.left = `${left}px`;
  hud.style.top = `${top}px`;
  const items = layers.slice(0, 8).map((layer) => `<li>${layer.label.replace(/[&<>]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[char] ?? char)}</li>`).join("");
  hud.innerHTML = [
    `<strong>${locked ? "ION DOM Inspector captured" : "ION DOM Inspector"}</strong>`,
    `<div>pixel: ${Math.round(x)},${Math.round(y)} | layers: ${layers.length}</div>`,
    layers.length ? `<ol>${items}</ol>` : "<div>No selectable page element under cursor.</div>",
  ].join("");
}

function publishInspectorLayers(): void {
  setBridgeInspectorLayers(
    inspectorCapturedLayers.map((layer) => ({ index: layer.index, label: layer.label, selector: layer.selector })),
    inspectorSelectedIndex,
  );
}

function inspectorSelectedLayer(): InspectorLayer | null {
  return inspectorCapturedLayers.find((layer) => layer.index === inspectorSelectedIndex) ?? inspectorCapturedLayers[0] ?? null;
}

function previewInspectorSelectedLayer(): void {
  ensureDomRegistryStyle();
  removeInspectorSelectedPreview();
  const layer = inspectorSelectedLayer();
  if (!layer) {
    setBridgeSettingsDetail("dom_inspector_no_layer_selected\nStart Inspector, hover the page, and click the target pixel first.");
    setBridgeStatus("Inspector layer missing", "No captured pixel stack is available.", "error");
    return;
  }
  const current = document.querySelector<HTMLElement>(layer.selector);
  if (current && visibleElement(current)) {
    layer.element = current;
    layer.rect = rectPayload(current.getBoundingClientRect());
    layer.label = inspectorLabel(current, layer.index);
  }
  const markerAnchor = settingsAnchorPoint;
  drawInspectorOutline(layer, true, INSPECTOR_SELECTED_PREVIEW_ID, markerAnchor, markerForTarget(settingsInspectorTarget));
  const detail = [
    "dom_inspector_layer_preview",
    `index: ${layer.index}`,
    `selector: ${layer.selector}`,
    `target: ${settingsInspectorTarget}`,
    `anchor: ${markerAnchor}`,
    `label: ${layer.label}`,
    `rect: ${JSON.stringify(layer.rect)}`,
  ].join("\n");
  setBridgeSettingsDetail(detail);
  setBridgeStatus("Inspector layer previewed", `Pink ring marks the selected captured layer @${markerAnchor}.`, "success");
}

function saveInspectorSelectedLayer(target: InspectorSaveTarget): void {
  const layer = inspectorSelectedLayer();
  if (!layer) {
    setBridgeSettingsDetail("dom_inspector_save_blocked\nNo captured layer is selected.");
    setBridgeStatus("Inspector save blocked", "Capture a pixel stack before saving an anchor.", "error");
    return;
  }
  const anchor = target === settingsInspectorTarget ? settingsAnchorPoint : targetMeta(target).anchor;
  const success = saveTargetMeta(target, layer.selector, anchor);
  if (!success) {
    setBridgeSettingsDetail("dom_inspector_save_failed\nlocalStorage write failed.");
    setBridgeStatus("Inspector save failed", "localStorage write failed.", "error");
    return;
  }
  const detail = [
    "dom_inspector_layer_saved",
    `target: ${target}`,
    `anchor: ${anchor}`,
    `index: ${layer.index}`,
    `selector: ${layer.selector}`,
    `label: ${layer.label}`,
  ].join("\n");
  setBridgeSettingsDetail(detail);
  setBridgeStatus("Inspector anchor saved", `${target} now uses the selected DOM layer.`, "success");
  previewInspectorSelectedLayer();
  if (target === "tabs_anchor") refreshBridgePosition();
}

function selectInspectorLayer(index: number): void {
  inspectorSelectedIndex = Math.max(0, Math.min(index, Math.max(0, inspectorCapturedLayers.length - 1)));
  publishInspectorLayers();
  previewInspectorSelectedLayer();
}

function stopDomInspector(message = "DOM inspector cancelled."): void {
  inspectorActive = false;
  inspectorCaptureMode = "single";
  document.removeEventListener("mousemove", domInspectorMouseMove, true);
  document.removeEventListener("click", domInspectorClick, true);
  document.removeEventListener("keydown", domInspectorKeydown, true);
  removeInspectorHud();
  removeInspectorOutlines();
  setBridgeSettingsDetail(message);
}

function domInspectorMouseMove(event: MouseEvent): void {
  if (!inspectorActive) return;
  const bridgeTarget = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
  if (bridgeTarget && isBridgeElement(bridgeTarget)) return;
  ensureDomRegistryStyle();
  const layers = inspectorLayersAt(event.clientX, event.clientY);
  drawInspectorLayers(layers);
  updateInspectorHud(event.clientX, event.clientY, layers);
}

function domInspectorClick(event: MouseEvent): void {
  if (!inspectorActive) return;
  const bridgeTarget = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
  if (bridgeTarget && isBridgeElement(bridgeTarget)) return;
  event.preventDefault();
  event.stopPropagation();
  event.stopImmediatePropagation();
  const layers = inspectorLayersAt(event.clientX, event.clientY);
  if (!layers.length) {
    setBridgeSettingsDetail("dom_inspector_capture_empty\nNo selectable page element under clicked pixel.");
    setBridgeStatus("Inspector capture empty", "Move over a visible ChatGPT element and click again.", "error");
    return;
  }
  inspectorCapturedLayers = layers;
  inspectorSelectedIndex = 0;
  publishInspectorLayers();
  drawInspectorLayers(layers, 0);
  updateInspectorHud(event.clientX, event.clientY, layers, true);
  const capturedMessage = [
    "dom_inspector_pixel_captured",
    `pixel: ${Math.round(event.clientX)},${Math.round(event.clientY)}`,
    `layers: ${layers.length}`,
    `top_selector: ${layers[0].selector}`,
    "Use the Settings controls to select a lower layer, then preview or save it as Tabs Anchor, Drop Zone, or Attach Target.",
  ].join("\n");
  if (inspectorCaptureMode === "single") {
    const message = `${capturedMessage}\nSettings is not active, so inspector stopped after capture.`;
    stopDomInspector(message);
  } else {
    setBridgeSettingsDetail(capturedMessage);
    setBridgeStatus("Inspector layer captured", "Settings inspector is active. Click again to replace this capture.", "success");
  }
  previewInspectorSelectedLayer();
}

function domInspectorKeydown(event: KeyboardEvent): void {
  if (event.key !== "Escape") return;
  event.preventDefault();
  event.stopPropagation();
  stopDomInspector("dom_inspector_cancelled\nInspector was cancelled with Escape.");
  setBridgeStatus("Inspector cancelled", "No anchor changed.", "idle");
}

function beginDomInspector(settingsMode = false): void {
  ensureDomRegistryStyle();
  removeInspectorChrome();
  inspectorActive = true;
  inspectorCaptureMode = settingsMode ? "settings" : "single";
  if (settingsMode) {
    setBridgeStatus("DOM inspector armed", "Settings mode active: hover the page and click to capture any target anchor point.", "working");
  } else {
    setBridgeStatus("DOM inspector armed", "Hover the page to see every element under the cursor. Click once to capture that pixel stack.", "working");
  }
  setBridgeSettingsDetail([
    "dom_inspector_armed",
    "Hover ChatGPT elements to see the top layer and lower layers under the cursor.",
    "Click one pixel to capture the stack.",
    settingsMode
      ? "Keep clicking new areas to update the captured stack while Settings is open."
      : "After capture, use the Settings controls to choose the exact layer and save it as an anchor.",
    settingsMode ? `Current settings target: ${settingsInspectorTarget} (anchor: ${settingsAnchorPoint}).` : "Press Escape to cancel without saving.",
    "Escape cancels without changing settings.",
  ].join("\n"));
  document.addEventListener("mousemove", domInspectorMouseMove, true);
  document.addEventListener("click", domInspectorClick, true);
  document.addEventListener("keydown", domInspectorKeydown, true);
}

function setSettingsInspectorMode(enabled: boolean): void {
  if (enabled) {
    if (!inspectorActive || inspectorCaptureMode === "single") {
      beginDomInspector(true);
      return;
    }
    inspectorCaptureMode = "settings";
    setBridgeStatus("DOM inspector locked", "Settings mode is active. Hover and click to update the selected layer.", "working");
    setBridgeSettingsDetail("dom_inspector_settings_mode_enabled\nInspector is now locked open for Settings.");
    return;
  }
  if (inspectorActive && inspectorCaptureMode === "settings") {
    stopDomInspector("dom_inspector_cancelled\nSettings inspector closed.");
  }
}

function attachCandidateFromEventTarget(target: EventTarget | null): HTMLElement | null {
  if (!(target instanceof Element)) return null;
  if (isBridgeElement(target)) return null;
  const candidate = target.closest<HTMLElement>("button, [role='button'], input[type='file'], label, [aria-label], [data-testid]");
  if (candidate && !isBridgeElement(candidate)) return candidate;
  return target as HTMLElement;
}

function dropCandidateFromEventTarget(target: EventTarget | null): HTMLElement | null {
  if (!(target instanceof Element)) return null;
  if (isBridgeElement(target)) return null;
  const candidate =
    target.closest<HTMLElement>("main, form, [data-testid*='composer' i], [data-message-author-role], article, section, div") ??
    (target instanceof HTMLElement ? target : null);
  return candidate && !isBridgeElement(candidate) ? dropZoneContainerFromElement(candidate) : null;
}

function tabsAnchorCandidateFromEventTarget(target: EventTarget | null): HTMLElement | null {
  if (!(target instanceof Element)) return null;
  if (isBridgeElement(target)) return null;
  const composer = findComposer();
  const candidate =
    target.closest<HTMLElement>("form, [data-testid*='composer' i], [class*='composer' i], [class*='prompt' i], main, section, div") ??
    (target instanceof HTMLElement ? target : null);
  if (!candidate || isBridgeElement(candidate)) return null;
  if (composer && !elementContains(candidate, composer)) {
    const parent = composer.closest<HTMLElement>("form, [data-testid*='composer' i], [class*='composer' i], [class*='prompt' i]");
    return parent && !isBridgeElement(parent) ? parent : null;
  }
  return candidate;
}

function tabsAnchorElement(): HTMLElement | null {
  const selector = storedTabsAnchorSelector();
  if (!selector) return null;
  let node: HTMLElement | null = null;
  try {
    node = document.querySelector<HTMLElement>(selector);
  } catch (_error) {
    setBridgeSettingsDetail(`tabs_anchor_selector_invalid\nselector: ${selector}`);
    return null;
  }
  const composer = findComposer();
  if (!node || !visibleElement(node)) {
    setBridgeSettingsDetail(`tabs_anchor_missing_or_hidden\nselector: ${selector}`);
    return null;
  }
  if (composer && !elementContains(node, composer)) {
    setBridgeSettingsDetail([
      "tabs_anchor_does_not_contain_composer_input",
      `selector: ${selector}`,
      `anchor_rect: ${JSON.stringify(rectPayload(node.getBoundingClientRect()))}`,
      `composer_rect: ${JSON.stringify(rectPayload(composer.getBoundingClientRect()))}`,
      "Use Pick Tabs Anchor again and click the visible composer background panel.",
    ].join("\n"));
    return null;
  }
  return node;
}

function previewTabsAnchor(): void {
  ensureDomRegistryStyle();
  const meta = storageMetaFromTarget("tabs_anchor");
  const target = tabsAnchorElement();
  document.getElementById(TABS_ANCHOR_PREVIEW_ID)?.remove();
  if (!target) {
    const detail = storedTabsAnchorSelector()
      ? "tabs_anchor_not_detected\nSaved tabs anchor is missing, hidden, or not the composer shell. Use Pick Tabs Anchor again or Clear Tabs Anchor."
      : "tabs_anchor_not_calibrated\nUse Settings -> Pick Tabs Anchor, then click the visible ChatGPT composer background panel.";
    setBridgeSettingsDetail(detail);
    setBridgeStatus("Tabs anchor missing", detail, "error");
    return;
  }
  const rect = target.getBoundingClientRect();
  const overlay = document.createElement("div");
  overlay.id = TABS_ANCHOR_PREVIEW_ID;
  overlay.style.left = `${Math.round(rect.left)}px`;
  overlay.style.top = `${Math.round(rect.top)}px`;
  overlay.style.width = `${Math.round(rect.width)}px`;
  overlay.style.height = `${Math.round(rect.height)}px`;
  addAnchorMarker(overlay, rect, meta.anchor, markerForTarget("tabs_anchor"));
  document.documentElement.appendChild(overlay);
  window.setTimeout(() => overlay.remove(), 4000);
  const detail = [
    "preview_tabs_anchor",
    `selector: ${storedTabsAnchorSelector()}`,
    `anchor: ${meta.anchor}`,
    `target: ${target.tagName.toLowerCase()}`,
    `rect: ${JSON.stringify(rectPayload(rect))}`,
    "The tab rail now anchors to this element before falling back to automatic composer-shell detection.",
  ].join("\n");
  setBridgeSettingsDetail(detail);
  setBridgeStatus("Tabs anchor previewed", "Orange ring marks the selected tab anchor.", "success");
  refreshBridgePosition();
}

function beginTabsAnchorPicker(): void {
  setBridgeStatus("Pick tabs anchor", "Click the visible ChatGPT composer background panel/top shell.", "working");
  setBridgeSettingsDetail("Tabs anchor picker armed. Click the composer background panel that should define the tab rail top edge.");
  const handler = (event: MouseEvent) => {
    const candidate = tabsAnchorCandidateFromEventTarget(event.target);
    if (!candidate) {
      setBridgeSettingsDetail("Tabs anchor pick ignored because the click was inside ION UI or not an element.");
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    document.removeEventListener("click", handler, true);
    const selector = selectorForElement(candidate);
    const anchor = settingsInspectorTarget === "tabs_anchor" ? settingsAnchorPoint : targetMeta("tabs_anchor").anchor;
    const saved = saveTargetMeta("tabs_anchor", selector, anchor);
    if (!saved) {
      setBridgeSettingsDetail("Tabs anchor could not be saved to localStorage.");
      setBridgeStatus("Tabs anchor not saved", "localStorage write failed.", "error");
      return;
    }
    const detail = [
      "tabs_anchor_calibrated",
      `selector: ${selector}`,
      `anchor: ${anchor}`,
      `label: ${controlLabel(candidate) || candidate.tagName.toLowerCase()}`,
      `rect: ${JSON.stringify(rectPayload(candidate.getBoundingClientRect()))}`,
    ].join("\n");
    setBridgeSettingsDetail(detail);
    setBridgeStatus("Tabs anchor calibrated", "Tabs now use the picked composer shell before auto detection.", "success");
    previewTabsAnchor();
    refreshBridgePosition();
  };
  document.addEventListener("click", handler, true);
  window.setTimeout(() => {
    document.removeEventListener("click", handler, true);
  }, 12000);
}

function clearTabsAnchorCalibration(): void {
  clearTargetMeta("tabs_anchor");
  document.getElementById(TABS_ANCHOR_PREVIEW_ID)?.remove();
  const detail = "tabs_anchor_calibration_cleared\nTabs will use automatic composer-shell detection again.";
  setBridgeSettingsDetail(detail);
  setBridgeStatus("Tabs anchor cleared", "Pick Tabs Anchor can be used to bind it again.", "idle");
  refreshBridgePosition();
}

function calibratedAttachControlElement(rect: DOMRect | null): HTMLElement | null {
  const selector = storedAttachSelector();
  if (!selector) return null;
  let node: HTMLElement | null = null;
  try {
    node = document.querySelector<HTMLElement>(selector);
  } catch (_error) {
    setBridgeArtifactDetail(`calibrated_attach_selector_invalid\nselector: ${selector}`);
    return null;
  }
  if (!node || !visibleElement(node)) {
    setBridgeArtifactDetail(`calibrated_attach_target_missing_or_hidden\nselector: ${selector}`);
    return null;
  }
  if (!elementWithinComposerBand(node, rect)) {
    const bounds = node.getBoundingClientRect();
    setBridgeArtifactDetail([
      "calibrated_attach_target_not_near_composer",
      `selector: ${selector}`,
      `target_rect: ${JSON.stringify(rectPayload(bounds))}`,
      `composer_rect: ${rect ? JSON.stringify(rectPayload(rect)) : "missing"}`,
      "Use Settings -> Pick Attach Target to re-calibrate.",
    ].join("\n"));
    return null;
  }
  return node;
}

function findAttachControlElement(): HTMLElement | null {
  const rect = composerShellRect() ?? composerRect();
  const calibrated = calibratedAttachControlElement(rect);
  if (calibrated) return calibrated;
  if (storedAttachSelector()) return null;
  const nodes = Array.from(document.querySelectorAll<HTMLElement>("button, [role='button'], input[type='file']"));
  return nodes.find((node) => {
    if (!visibleElement(node)) return false;
    const label = controlLabel(node).toLowerCase();
    return elementWithinComposerBand(node, rect) && /attach|upload|file|plus|add/.test(label);
  }) ?? null;
}

function findAttachControlRect(): Record<string, unknown> | null {
  const candidate = findAttachControlElement();
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

function localAttachPayload(): Record<string, unknown> | null {
  const targetRect = findAttachControlRect();
  const composer = composerShellRect() ?? composerRect();
  if (!targetRect || !composer) return null;
  return {
    target_kind: "attach_button",
    target_rect: targetRect,
    target_screen_rect: targetRect["screen_rect"],
    composer_rect: rectPayload(composer),
    viewport: {
      width: Math.round(window.innerWidth),
      height: Math.round(window.innerHeight),
    },
    device_pixel_ratio: window.devicePixelRatio || 1,
    page_url: window.location.href,
    captured_at_ms: Date.now(),
  };
}

function beginAttachTargetPicker(): void {
  setBridgeStatus("Pick attach target", "Click ChatGPT's real attach/add-file button. The next page click will be captured.", "working");
  setBridgeSettingsDetail("Attach target picker armed. Click the ChatGPT attach/add-file button, not the ION panel.");
  const handler = (event: MouseEvent) => {
    const candidate = attachCandidateFromEventTarget(event.target);
    if (!candidate) {
      setBridgeSettingsDetail("Attach target pick ignored because the click was inside ION UI or not an element.");
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    document.removeEventListener("click", handler, true);
    const selector = selectorForElement(candidate);
    const anchor = settingsInspectorTarget === "attach_target" ? settingsAnchorPoint : targetMeta("attach_target").anchor;
    const saved = saveTargetMeta("attach_target", selector, anchor);
    if (!saved) {
      setBridgeSettingsDetail("Attach target could not be saved to localStorage.");
      setBridgeStatus("Attach target not saved", "localStorage write failed.", "error");
      return;
    }
    const detail = [
      "attach_target_calibrated",
      `selector: ${selector}`,
      `anchor: ${anchor}`,
      `label: ${controlLabel(candidate) || candidate.tagName.toLowerCase()}`,
      `rect: ${JSON.stringify(rectPayload(candidate.getBoundingClientRect()))}`,
    ].join("\n");
    setBridgeSettingsDetail(detail);
    setBridgeArtifactDetail(detail);
    setBridgeStatus("Attach target calibrated", "Preview Target should now ring the selected button.", "success");
    previewAttachTarget();
  };
  document.addEventListener("click", handler, true);
  window.setTimeout(() => {
    document.removeEventListener("click", handler, true);
  }, 12000);
}

function clearAttachTargetCalibration(): void {
  clearTargetMeta("attach_target");
  document.getElementById(ATTACH_PREVIEW_ID)?.remove();
  const detail = "attach_target_calibration_cleared\nPreview Target will use the guarded automatic heuristic again.";
  setBridgeSettingsDetail(detail);
  setBridgeArtifactDetail(detail);
  setBridgeStatus("Attach target cleared", "Pick Attach Target can be used to bind it again.", "idle");
}

function beginDropTargetPicker(): void {
  setBridgeStatus("Pick drop zone", "Click the ChatGPT area where a normal file drag/drop is accepted.", "working");
  setBridgeSettingsDetail("Drop-zone picker armed. Click the ChatGPT page/composer area you would normally drop a file onto.");
  const handler = (event: MouseEvent) => {
    const candidate = dropCandidateFromEventTarget(event.target);
    if (!candidate) {
      setBridgeSettingsDetail("Drop-zone pick ignored because the click was inside ION UI or not a page element.");
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    document.removeEventListener("click", handler, true);
    const selector = selectorForElement(candidate);
    const anchor = settingsInspectorTarget === "drop_zone" ? settingsAnchorPoint : targetMeta("drop_zone").anchor;
    const saved = saveTargetMeta("drop_zone", selector, anchor);
    if (!saved) {
      setBridgeSettingsDetail("Drop zone could not be saved to localStorage.");
      setBridgeStatus("Drop zone not saved", "localStorage write failed.", "error");
      return;
    }
    const rect = visibleDropRect(candidate) ?? candidate.getBoundingClientRect();
    const detail = [
      "drop_zone_calibrated",
      `selector: ${selector}`,
      `anchor: ${anchor}`,
      `label: ${controlLabel(candidate) || candidate.tagName.toLowerCase()}`,
      `rect: ${JSON.stringify(rectPayload(rect))}`,
    ].join("\n");
    setBridgeSettingsDetail(detail);
    setBridgeArtifactDetail(detail);
    setBridgeStatus("Drop zone calibrated", "Preview Drop Zone should now ring the selected drop area.", "success");
    previewDropTarget();
  };
  document.addEventListener("click", handler, true);
  window.setTimeout(() => {
    document.removeEventListener("click", handler, true);
  }, 12000);
}

function clearDropTargetCalibration(): void {
  clearTargetMeta("drop_zone");
  document.getElementById(DROP_PREVIEW_ID)?.remove();
  const detail = "drop_zone_calibration_cleared\nDrop Latest will use the guarded default page/composer drop zone again.";
  setBridgeSettingsDetail(detail);
  setBridgeArtifactDetail(detail);
  setBridgeStatus("Drop zone cleared", "Pick Drop Zone can be used to bind it again.", "idle");
}

function previewDropTarget(): void {
  ensureDomRegistryStyle();
  const meta = storageMetaFromTarget("drop_zone");
  const target = findDropTarget();
  document.getElementById(DROP_PREVIEW_ID)?.remove();
  if (!target) {
    const detail = storedDropSelector()
      ? "drop_target_not_detected\nSaved drop zone is missing or hidden. Use Settings -> Pick Drop Zone again or Clear Drop Zone."
      : "drop_target_not_detected\nNo page/composer drop zone was found.";
    setBridgeArtifactDetail(detail);
    setBridgeStatus("Drop zone missing", detail, "error");
    return;
  }
  const rect = visibleDropRect(target) ?? target.getBoundingClientRect();
  const overlay = document.createElement("div");
  overlay.id = DROP_PREVIEW_ID;
  overlay.style.left = `${Math.round(rect.left)}px`;
  overlay.style.top = `${Math.round(rect.top)}px`;
  overlay.style.width = `${Math.round(rect.width)}px`;
  overlay.style.height = `${Math.round(rect.height)}px`;
  addAnchorMarker(overlay, rect, meta.anchor, markerForTarget("drop_zone"));
  document.documentElement.appendChild(overlay);
  window.setTimeout(() => overlay.remove(), 4000);
  const detail = [
    "preview_drop_zone",
    `selector: ${storedDropSelector() || "default_page_or_composer_drop_zone"}`,
    `anchor: ${meta.anchor}`,
    `target: ${target.tagName.toLowerCase()}`,
    `rect: ${JSON.stringify(rectPayload(rect))}`,
    "Drop Latest dispatches visible drag/drop events here. Browser/ChatGPT may still reject synthetic drops.",
  ].join("\n");
  setBridgeArtifactDetail(detail);
  setBridgeStatus("Drop zone previewed", "Blue ring marks the current Drop Latest target.", "success");
}

function previewAttachTarget(): void {
  ensureDomRegistryStyle();
  const meta = storageMetaFromTarget("attach_target");
  const target = findAttachControlElement();
  document.getElementById(ATTACH_PREVIEW_ID)?.remove();
  if (!target) {
    const detail = storedAttachSelector()
      ? "attach_control_not_detected\nSaved attach target is missing, hidden, or no longer near the composer. Use Settings -> Pick Attach Target again or Clear Attach Target."
      : "attach_control_not_detected\nNo target ring was drawn. Use Settings -> Pick Attach Target if the heuristic cannot find the attach/add-file button.";
    setBridgeArtifactDetail(detail);
    setBridgeStatus("Attach target missing", detail, "error");
    return;
  }
  const rect = target.getBoundingClientRect();
  const overlay = document.createElement("div");
  overlay.id = ATTACH_PREVIEW_ID;
  overlay.style.left = `${Math.round(rect.left - 5)}px`;
  overlay.style.top = `${Math.round(rect.top - 5)}px`;
  overlay.style.width = `${Math.round(rect.width + 10)}px`;
  overlay.style.height = `${Math.round(rect.height + 10)}px`;
  addAnchorMarker(
    overlay,
    {
      x: rect.left - 5,
      y: rect.top - 5,
      width: rect.width + 10,
      height: rect.height + 10,
    },
    meta.anchor,
    markerForTarget("attach_target"),
  );
  document.documentElement.appendChild(overlay);
  window.setTimeout(() => overlay.remove(), 4000);
  const payload = localAttachPayload();
  const detail = payload ? compactJson(payload, 1200) : "attach_target_payload_unavailable";
  const anchor = storageMetaFromTarget("attach_target").anchor;
  setBridgeArtifactDetail(`preview_attach_target\n${detail}\nanchor: ${anchor}`);
  setBridgeStatus("Attach target previewed", "Green ring marks the exact attach target. Reject Local Attach if the ring is wrong.", "success");
}

function previewCurrentSettingsTargetCalibration(): void {
  if (settingsInspectorTarget === "tabs_anchor") {
    previewTabsAnchor();
    return;
  }
  if (settingsInspectorTarget === "drop_zone") {
    previewDropTarget();
    return;
  }
  previewAttachTarget();
}

function refreshSettingsInspectorPreview(): void {
  if (!inspectorActive) return;
  if (inspectorCapturedLayers.length > 0) {
    previewInspectorSelectedLayer();
    return;
  }
  previewCurrentSettingsTargetCalibration();
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

function dispatchDropCleanupEvents(target: HTMLElement, transfer: DataTransfer): void {
  const cleanupTargets: EventTarget[] = [
    target,
    document.body,
    document.documentElement,
    document,
    window,
  ].filter(Boolean) as EventTarget[];
  const dispatchDrag = (eventName: string) => {
    cleanupTargets.forEach((eventTarget) => {
      try {
        const event = new DragEvent(eventName, {
          bubbles: true,
          cancelable: true,
          composed: true,
          dataTransfer: transfer,
        });
        eventTarget.dispatchEvent(event);
      } catch (_error) {
        // Some event targets may reject synthetic DragEvent dispatch.
      }
    });
  };
  const dispatchEscape = () => {
    [document, window].forEach((eventTarget) => {
      try {
        eventTarget.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", code: "Escape", bubbles: true, cancelable: true }));
        eventTarget.dispatchEvent(new KeyboardEvent("keyup", { key: "Escape", code: "Escape", bubbles: true, cancelable: true }));
      } catch (_error) {
        // Escape cleanup is best-effort only.
      }
    });
  };
  ["dragleave", "dragend"].forEach(dispatchDrag);
  window.setTimeout(() => ["dragleave", "dragend"].forEach(dispatchDrag), 120);
  window.setTimeout(dispatchEscape, 260);
  window.setTimeout(() => document.getElementById(DROP_PREVIEW_ID)?.remove(), 500);
}

function dispatchFilesToDropTarget(target: HTMLElement, files: File[]): DataTransfer {
  const transfer = new DataTransfer();
  files.forEach((file) => transfer.items.add(file));
  for (const eventName of ["dragenter", "dragover", "drop"]) {
    const event = new DragEvent(eventName, {
      bubbles: true,
      cancelable: true,
      composed: true,
      dataTransfer: transfer,
    });
    target.dispatchEvent(event);
  }
  dispatchDropCleanupEvents(target, transfer);
  return transfer;
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
    previewDropTarget();
    const response = await fetch(downloadUrl);
    if (!response.ok) throw new Error(`download_failed_${response.status}`);
    const blob = await response.blob();
    const file = new File([blob], filename, { type: contentType || blob.type || "application/octet-stream" });
    dispatchFilesToDropTarget(target, [file]);
    const detail = [
      "visible_browser_drop_attempted",
      `filename: ${filename}`,
      `size_bytes: ${file.size}`,
      `sha256: ${result?.sha256 ?? ""}`,
      `receipt_path: ${result?.receipt_path ?? ""}`,
      "drop_overlay_cleanup: dragleave_dragend_escape_attempted",
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
  const payload = localAttachPayload();
  const beforeCount = uploadedAttachmentCount();
  if (!payload) {
    const detail = "attach_control_or_composer_not_detected\nUse Preview Attach Target first and confirm Diagnostics sees the attach/add-file control.";
    setBridgeArtifactDetail(detail);
    setBridgeStatus("Local attach blocked", detail, "error");
    return;
  }
  previewAttachTarget();
  setBridgeStatus("Local attach latest", "Requesting approval after local geometry capture. The daemon will dry-run before any mouse movement.", "working");
  chrome.runtime.sendMessage({
    type: "ion_chatops_artifact_local_attach_latest",
    payload,
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

function requestArtifactLocalAttachDryRun(): void {
  const payload = localAttachPayload();
  if (!payload) {
    const detail = "attach_control_or_composer_not_detected\nUse Preview Attach Target and confirm the green ring is on the attach button.";
    setBridgeArtifactDetail(detail);
    setBridgeStatus("Dry run blocked", detail, "error");
    return;
  }
  previewAttachTarget();
  setBridgeStatus("Dry run attach", "Requesting daemon geometry validation. No mouse movement will occur.", "working");
  chrome.runtime.sendMessage({
    type: "ion_chatops_artifact_local_attach_dry_run",
    payload,
  }, async (response) => {
    const detail = response?.ok ? compactJson(response.result, 2200) : blockedDetail(response);
    setBridgeArtifactDetail(detail);
    setBridgeStatus(response?.ok ? "Dry run passed" : "Dry run blocked", detail.split("\n")[0] ?? "", response?.ok ? "success" : "error");
    if (response?.ok) await copyBridgeResult("Local attach dry run", detail);
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
      `queue_target: ${result.queue_target ?? result.queue_path ?? result.verdict ?? ""}`,
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

let browserPressureStarted = false;
let latestEventLoopLagMs = 0;
let latestLongTaskMs = 0;
let nextLagProbeAt = 0;

type QueuedChatMessage = {
  id: string;
  kind?: "text" | "files";
  text: string;
  status: "queued" | "waiting" | "sending" | "sent" | "failed";
  createdAt: string;
  detail?: string;
  source?: "manual" | "gateway" | "pack" | "file";
  autoRun?: boolean;
  editing?: boolean;
  draftText?: string;
  updatedAt?: string;
  attachments?: Array<{ name: string; size: number; type: string }>;
  gateway?: {
    packetId: string;
    leaseId: string;
    carrierId: string;
    objective: string;
    authority: unknown;
    turnIndex: number;
  };
};

let messageQueueStarted = false;
let messageQueuePaused = false;
let messageQueueAllowMidOutput = false;
let messageQueueProcessing = false;
let messageQueueItems: QueuedChatMessage[] = [];
let messageQueueFilePayloads = new Map<string, File[]>();
let lastQueueChromeRect: DOMRect | null = null;
let messageQueueDragItemId = "";
let messageQueuePanelExpanded = false;
let registryPopoverCloseHandler: ((event: PointerEvent) => void) | null = null;
let registryPopoverEscapeHandler: ((event: KeyboardEvent) => void) | null = null;
let messageQueueAutoPlay = false;
let messageQueueSawActiveOutput = false;
let messageQueueLastAutoSentAt = 0;
let browserQueueCarrierStarted = false;
let browserQueueCarrierBusy = false;
let browserQueueGatewayStatus = "Gateway queue warming.";
let browserQueueLastClaimAt = 0;
let browserQueueApprovalPacketId = "";
let browserQueueAutoTurnsThisSession = 0;
let browserQueueAutoAcceptActive = false;
let browserQueueAutoAcceptUntil = "";
let browserQueueAutoAcceptTtlSeconds = 900;
let lastNativeActionAutoAcceptAt = 0;
let nativeActionAutoAcceptCandidate = "";
let nativeActionAutoAcceptCandidateSince = 0;
let leftDockProjectPanelExpanded = leftDockPanelExpandedFromStorage();
let contextWorkflowPanelExpanded = false;
let contextWorkflowRailStatus = "Context rail ready.";
let contextWorkflowLastImportedPack = "No workflow pack imported.";
const BROWSER_QUEUE_CARRIER_ID = `ion-browser-carrier-${Math.random().toString(16).slice(2)}`;
const BROWSER_QUEUE_CLAIM_COOLDOWN_MS = 2500;
const BROWSER_QUEUE_RESULT_TIMEOUT_MS = 10 * 60 * 1000;

function visibleElement(element: Element | null): element is HTMLElement {
  if (!(element instanceof HTMLElement)) return false;
  if (element.closest(`#${PANEL_ID}`) || element.closest(`#${MODAL_ID}`)) return false;
  const rect = element.getBoundingClientRect();
  const style = window.getComputedStyle(element);
  return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
}

function buttonText(button: HTMLElement): string {
  return `${button.textContent ?? ""} ${button.getAttribute("aria-label") ?? ""} ${button.getAttribute("title") ?? ""}`.replace(/\s+/g, " ").trim();
}

function buttonDisabled(button: HTMLButtonElement): boolean {
  return (
    button.disabled ||
    (typeof button.matches === "function" && button.matches(":disabled")) ||
    button.getAttribute("aria-disabled") === "true" ||
    button.dataset.disabled === "true"
  );
}

function nativeActionConfirmCard(button: HTMLButtonElement): HTMLElement | null {
  const label = buttonText(button).toLowerCase();
  if (!/^confirm\b/.test(label) || buttonDisabled(button) || !visibleElement(button)) return null;
  const candidates = [
    button.closest<HTMLElement>("[role='dialog']"),
    button.closest<HTMLElement>("article"),
    button.closest<HTMLElement>("div[class*='rounded']"),
    button.parentElement?.parentElement?.parentElement ?? null,
  ].filter(Boolean) as HTMLElement[];
  for (const card of candidates) {
    const text = (card.textContent ?? "").replace(/\s+/g, " ").toLowerCase();
    if (
      text.includes("wants to talk to ion.helixion.net") ||
      text.includes("ion_helixion") ||
      text.includes("ion helixion") ||
      text.includes("ion wants to talk") ||
      text.includes("tool call: ion")
    ) {
      return card;
    }
  }
  return null;
}

function nativeActionCardKey(card: HTMLElement, button: HTMLButtonElement): string {
  const rect = card.getBoundingClientRect();
  return [
    Math.round(rect.left),
    Math.round(rect.top),
    Math.round(rect.width),
    Math.round(rect.height),
    buttonText(button).slice(0, 40),
    (card.textContent ?? "").replace(/\s+/g, " ").slice(0, 160),
  ].join("|");
}

function tryAutoAcceptNativeAction(): void {
  if (!browserQueueAutoAcceptActive) return;
  const now = Date.now();
  if (now - lastNativeActionAutoAcceptAt < 4500) return;
  const matches: { button: HTMLButtonElement; card: HTMLElement; rect: DOMRect; key: string }[] = [];
  for (const button of Array.from(document.querySelectorAll<HTMLButtonElement>("button"))) {
    const card = nativeActionConfirmCard(button);
    if (!card) continue;
    const rect = card.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > window.innerHeight || rect.width < 180 || rect.height < 48) continue;
    matches.push({ button, card, rect, key: nativeActionCardKey(card, button) });
  }
  if (!matches.length) {
    nativeActionAutoAcceptCandidate = "";
    nativeActionAutoAcceptCandidateSince = 0;
    return;
  }
  matches.sort((a, b) => b.rect.bottom - a.rect.bottom || b.rect.top - a.rect.top);
  const selected = matches[0];
  const next = matches[1];
  if (next && Math.abs(selected.rect.bottom - next.rect.bottom) < 80) {
    browserQueueGatewayStatus = "Auto-accept waiting: multiple ION action confirmations are too close to choose safely.";
    publishMessageQueueState();
    return;
  }
  if (nativeActionAutoAcceptCandidate !== selected.key) {
    nativeActionAutoAcceptCandidate = selected.key;
    nativeActionAutoAcceptCandidateSince = now;
    browserQueueGatewayStatus = "Auto-accept armed: latest ION/Helixion confirmation detected; waiting for card stability.";
    publishMessageQueueState();
    return;
  }
  if (now - nativeActionAutoAcceptCandidateSince < 800) return;
  lastNativeActionAutoAcceptAt = now;
  nativeActionAutoAcceptCandidate = "";
  nativeActionAutoAcceptCandidateSince = 0;
  selected.button.click();
  browserQueueGatewayStatus = "Auto-accepted latest visible ION/Helixion ChatGPT action confirmation.";
  publishMessageQueueState();
}

function findComposerInput(): HTMLElement | null {
  const selectors = [
    "textarea[data-testid='composer-text-input']",
    "textarea[placeholder]",
    "#prompt-textarea",
    "[data-testid='composer'] div[contenteditable='true']",
    "[data-testid='composer'] textarea",
    "form textarea",
    "div[contenteditable='true'][data-testid='composer-text-input']",
    "form div[contenteditable='true']",
    "div[contenteditable='true']",
  ];
  const matches: HTMLElement[] = [];
  for (const selector of selectors) {
    for (const node of Array.from(document.querySelectorAll<HTMLElement>(selector))) {
      if (!visibleElement(node)) continue;
      const rect = node.getBoundingClientRect();
      if (rect.bottom < window.innerHeight - 260) continue;
      matches.push(node);
    }
  }
  matches.sort((a, b) => b.getBoundingClientRect().bottom - a.getBoundingClientRect().bottom);
  return matches[0] ?? null;
}

function findComposerContainer(input: HTMLElement): HTMLElement {
  const candidates = [
    input.closest<HTMLElement>("form"),
    input.closest<HTMLElement>("[data-testid='composer']"),
    input.closest<HTMLElement>("[role='presentation']"),
    input.parentElement,
  ].filter(Boolean) as HTMLElement[];
  for (const candidate of candidates) {
    const rect = candidate.getBoundingClientRect();
    if (rect.width >= 240 && rect.height >= 40 && rect.bottom >= window.innerHeight - 260) return candidate;
  }
  return input;
}

function findChatButton(match: (text: string, button: HTMLButtonElement) => boolean): HTMLButtonElement | null {
  for (const button of Array.from(document.querySelectorAll<HTMLButtonElement>("button"))) {
    if (!visibleElement(button)) continue;
    if (
      button.closest(`#${PANEL_ID}`) ||
      button.closest(`#${MODAL_ID}`) ||
      button.closest(`#${MESSAGE_QUEUE_PANEL_ID}`) ||
      button.closest(`#${CONTEXT_WORKFLOW_PANEL_ID}`) ||
      button.closest(`#${CHATGPT_LEFT_ICON_DOCK_ID}`)
    ) continue;
    if (match(buttonText(button), button)) return button;
  }
  return null;
}

function findSendButton(): HTMLButtonElement | null {
  const matches: HTMLButtonElement[] = [];
  for (const button of Array.from(document.querySelectorAll<HTMLButtonElement>("button"))) {
    if (!visibleElement(button)) continue;
    if (
      button.closest(`#${PANEL_ID}`) ||
      button.closest(`#${MODAL_ID}`) ||
      button.closest(`#${MESSAGE_QUEUE_PANEL_ID}`) ||
      button.closest(`#${CONTEXT_WORKFLOW_PANEL_ID}`) ||
      button.closest(`#${CHATGPT_LEFT_ICON_DOCK_ID}`)
    ) continue;
    const testId = button.getAttribute("data-testid") ?? "";
    const text = buttonText(button);
    if (testId.includes("send") || /send/i.test(button.getAttribute("aria-label") ?? "") || /\bsend\b/i.test(text)) {
      matches.push(button);
    }
  }
  return matches.find((button) => !buttonDisabled(button)) ?? matches[0] ?? null;
}

function findStopButton(): HTMLButtonElement | null {
  return findChatButton((text, button) => {
    const testId = button.getAttribute("data-testid") ?? "";
    return testId.includes("stop") || /\bstop\b/i.test(text) || /stop\s+(generating|streaming)/i.test(text);
  });
}

function chatReadiness(): { activeOutput: boolean; sendAvailable: boolean; reason: string; input: HTMLElement | null; sendButton: HTMLButtonElement | null } {
  const input = findComposerInput();
  const sendButton = findSendButton();
  const stopButton = findStopButton();
  const activeOutput = Boolean(stopButton && !buttonDisabled(stopButton));
  const sendAvailable = Boolean(sendButton && !buttonDisabled(sendButton) && visibleElement(sendButton));
  let reason = "ready";
  if (!input) reason = "composer input not found";
  else if (activeOutput && !messageQueueAllowMidOutput) reason = "assistant output active";
  else if (!sendAvailable) reason = "send button unavailable";
  return { activeOutput, sendAvailable, reason, input, sendButton };
}

function queueStatus(): string {
  const pending = messageQueueItems.filter((item) => item.status === "queued" || item.status === "waiting" || item.status === "failed").length;
  const gatewayPending = messageQueueItems.filter((item) => item.gateway && (item.status === "queued" || item.status === "waiting" || item.status === "failed" || item.status === "sending")).length;
  if (messageQueuePaused) return `Queue paused. ${pending} message(s) waiting.`;
  if (gatewayPending) return `Gateway carrier armed. ${gatewayPending} Action packet(s) waiting. ${browserQueueGatewayStatus}`;
  if (!pending) return `Queue ready. Type in ChatGPT, press Q+ to queue, then ${messageQueueAutoPlay ? "Auto Play will send after output finishes." : "press Q▶ to send next."} ${browserQueueGatewayStatus}`;
  return messageQueueAutoPlay
    ? `Auto Play armed. ${pending} message(s) waiting for the next completed output.`
    : `Queue ready. ${pending} message(s) waiting. Press Q▶ to send the next queued message.`;
}

function publishMessageQueueState(status = queueStatus()): void {
  const readiness = chatReadiness();
  setBridgeMessageQueueState({
    status,
    paused: messageQueuePaused,
    allowMidOutput: messageQueueAllowMidOutput,
    activeOutput: readiness.activeOutput,
    sendAvailable: readiness.sendAvailable,
    autoAcceptActive: browserQueueAutoAcceptActive,
    autoAcceptUntil: browserQueueAutoAcceptUntil,
    autoAcceptTtlSeconds: browserQueueAutoAcceptTtlSeconds,
    items: messageQueueItems,
  });
}

function gatewayRequest(type: string, payload: Record<string, unknown> = {}): Promise<any> {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({ type, payload }, (response) => {
      resolve(response ?? { ok: false, stage: "no_response", finding: "browser_gateway_no_response" });
    });
  });
}

function nextQueuedMessage(autoOnly = false): QueuedChatMessage | undefined {
  return messageQueueItems.find((candidate) => {
    const pending = candidate.status === "queued" || candidate.status === "waiting" || candidate.status === "failed";
    if (!pending) return false;
    return !autoOnly || candidate.autoRun === true || Boolean(candidate.gateway);
  });
}

function gatewayQueueItemPending(): boolean {
  return Boolean(nextQueuedMessage(true));
}

function summarizeGatewayPacket(packet: any): string {
  const objective = String(packet?.objective ?? packet?.prompt_preview ?? packet?.packet_id ?? "ION browser queue packet").trim();
  const authority = typeof packet?.authority === "string" ? packet.authority : JSON.stringify(packet?.authority ?? "analysis_only");
  return `${objective}\n\nION_BROWSER_PACKET:\npacket_id: ${packet?.packet_id ?? ""}\nauthority: ${authority}\nstop_condition: ${packet?.stop_condition ?? "return receipt or blocker"}`;
}

function addGatewayQueueItem(packet: any, claim: any): void {
  const packetId = String(packet?.packet_id ?? "").trim();
  if (!packetId || messageQueueItems.some((item) => item.gateway?.packetId === packetId && item.status !== "sent")) return;
  messageQueueItems.push({
    id: `ion-gateway-${packetId}-${Date.now()}`,
    kind: "text",
    text: String(packet?.prompt ?? summarizeGatewayPacket(packet)).trim(),
    status: "queued",
    createdAt: new Date().toISOString(),
    detail: "Claimed from ION Action Gateway.",
    source: "gateway",
    autoRun: packet?.auto_run !== false,
    gateway: {
      packetId,
      leaseId: String(claim?.lease_id ?? packet?.claim?.lease_id ?? ""),
      carrierId: BROWSER_QUEUE_CARRIER_ID,
      objective: String(packet?.objective ?? packet?.prompt_preview ?? packetId),
      authority: packet?.authority ?? "analysis_only",
      turnIndex: Number(packet?.claim?.turn_index ?? packet?.attempts ?? 1),
    },
  });
  publishMessageQueueState(`Gateway packet claimed: ${packetId}`);
  syncComposerQueueChrome();
}

async function pollBrowserQueueCarrier(): Promise<void> {
  if (browserQueueCarrierBusy || messageQueuePaused) return;
  browserQueueCarrierBusy = true;
  try {
    const statusResponse = await gatewayRequest("ion_chatops_browser_queue_status");
    const status = statusResponse?.result;
    if (!statusResponse?.ok || !status?.ok) {
      browserQueueGatewayStatus = `Gateway blocked: ${blockedDetail(statusResponse?.result ?? statusResponse)}`;
      return;
    }
    const counts = status.counts ?? {};
    const autoAccept = status.auto_accept_actions ?? {};
    browserQueueAutoAcceptActive = Boolean(autoAccept.enabled);
    browserQueueAutoAcceptUntil = String(autoAccept.until ?? "");
    const autoAcceptLabel = browserQueueAutoAcceptActive ? ` Auto-accept on until ${browserQueueAutoAcceptUntil || "TTL expires"}.` : "";
    browserQueueGatewayStatus = `Gateway queued ${counts.queued ?? 0}, needs approval ${counts.needs_operator ?? 0}.${autoAcceptLabel}`;
    tryAutoAcceptNativeAction();
    const packets = Array.isArray(status.packets) ? status.packets : [];
    browserQueueApprovalPacketId = String(packets.find((packet: any) => packet?.state === "needs_operator")?.packet_id ?? "");
    const hasLocalGatewayPacket = messageQueueItems.some((item) => item.gateway && item.status !== "sent");
    if (hasLocalGatewayPacket || status.paused || status.killed || Date.now() - browserQueueLastClaimAt < BROWSER_QUEUE_CLAIM_COOLDOWN_MS) return;
    const autoplayCap = Number(status.max_autoplay_turns ?? 10);
    if (browserQueueAutoTurnsThisSession >= autoplayCap) {
      browserQueueGatewayStatus = `Gateway autoplay cap reached (${autoplayCap}). Use Resume after reviewing receipts.`;
      return;
    }
    if (!Number(counts.queued ?? 0)) return;
    browserQueueLastClaimAt = Date.now();
    const claimResponse = await gatewayRequest("ion_chatops_browser_queue_claim", {
      carrier_id: BROWSER_QUEUE_CARRIER_ID,
      chat_url: window.location.href,
    });
    const claim = claimResponse?.result;
    if (claimResponse?.ok && claim?.claimed && claim.packet) {
      browserQueueAutoTurnsThisSession += 1;
      addGatewayQueueItem(claim.packet, claim);
    } else if (!claimResponse?.ok) {
      browserQueueGatewayStatus = `Gateway claim blocked: ${blockedDetail(claimResponse?.result ?? claimResponse)}`;
    }
  } finally {
    browserQueueCarrierBusy = false;
  }
}

function startBrowserQueueCarrier(): void {
  if (browserQueueCarrierStarted) return;
  browserQueueCarrierStarted = true;
  void pollBrowserQueueCarrier();
  window.setInterval(() => {
    void pollBrowserQueueCarrier();
  }, BROWSER_QUEUE_CLAIM_COOLDOWN_MS);
}

function updateQueueReadinessState(): void {
  const readiness = chatReadiness();
  if (readiness.activeOutput) {
    messageQueueSawActiveOutput = true;
    return;
  }
  const pendingAuto = gatewayQueueItemPending();
  const pending = Boolean(messageQueueAutoPlay ? nextQueuedMessage(false) : nextQueuedMessage(true));
  const readyAfterOutput = (messageQueueSawActiveOutput || pendingAuto) && !readiness.activeOutput && readiness.sendAvailable;
  if (
    (messageQueueAutoPlay || pendingAuto) &&
    pending &&
    readyAfterOutput &&
    !messageQueuePaused &&
    Date.now() - messageQueueLastAutoSentAt > 1200
  ) {
    messageQueueSawActiveOutput = false;
    messageQueueLastAutoSentAt = Date.now();
    void processMessageQueue("auto-after-output", true, !messageQueueAutoPlay);
  }
}

function splitQueuedMessages(text: string): string[] {
  return text.split(/\n{2,}/).map((part) => part.trim()).filter(Boolean);
}

function addQueuedMessageBatch(parts: string[], status?: string, source: "manual" | "pack" = "manual"): void {
  const messages = parts.map((part) => String(part ?? "").trim()).filter(Boolean);
  const now = new Date().toISOString();
  for (const part of messages) {
    messageQueueItems.push({
      id: `ion-queued-${Date.now()}-${Math.random().toString(16).slice(2)}`,
      kind: "text",
      text: part,
      status: "queued",
      createdAt: now,
      source,
      autoRun: false,
    });
  }
  publishMessageQueueState(status || `${messages.length} message(s) queued. Press Q▶ to send next.`);
}

function addQueuedMessages(text: string): void {
  addQueuedMessageBatch(splitQueuedMessages(text));
}

function compactFileSize(bytes: number): string {
  if (!Number.isFinite(bytes) || bytes < 0) return "0 B";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(bytes < 10 * 1024 * 1024 ? 1 : 0)} MB`;
}

function queueFiles(files: File[]): void {
  const selected = files.filter(Boolean);
  if (!selected.length) {
    publishMessageQueueState("File queue blocked: no files selected.");
    return;
  }
  const id = `ion-file-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  const attachments = selected.map((file) => ({ name: file.name || "unnamed-file", size: file.size, type: file.type || "application/octet-stream" }));
  const label = attachments.map((file) => `${file.name} (${compactFileSize(file.size)})`).join(", ");
  messageQueueFilePayloads.set(id, selected);
  messageQueueItems.push({
    id,
    kind: "files",
    text: `Upload ${selected.length} file${selected.length === 1 ? "" : "s"}: ${label}`,
    status: "queued",
    createdAt: new Date().toISOString(),
    detail: "Queued from operator file picker. File objects are held in browser memory only until reload.",
    source: "file",
    autoRun: false,
    attachments,
  });
  messageQueuePanelExpanded = true;
  publishMessageQueueState(`${selected.length} file item${selected.length === 1 ? "" : "s"} queued for visible drop.`);
  syncComposerQueueChrome();
}

function openMessageQueueFilePicker(): void {
  const input = ensureMessageQueueFileInput();
  input.value = "";
  input.click();
}

function visibleQueueItems(): QueuedChatMessage[] {
  return messageQueueItems.filter((item) => item.status !== "sent");
}

function queueItemById(id: string): QueuedChatMessage | undefined {
  return messageQueueItems.find((item) => item.id === id);
}

function queueItemIndexById(id: string): number {
  return messageQueueItems.findIndex((item) => item.id === id);
}

function setQueueItemEditing(id: string, editing: boolean): void {
  const item = queueItemById(id);
  if (!item || item.status === "sending") return;
  item.editing = editing;
  item.draftText = editing ? item.text : "";
  messageQueuePanelExpanded = true;
  publishMessageQueueState(editing ? "Queue item opened for editing." : "Queue item edit cancelled.");
  syncComposerQueueChrome();
}

function queueEditTextFromPanel(panel: HTMLElement, id: string): string {
  const editor = Array.from(panel.querySelectorAll<HTMLTextAreaElement>("[data-queue-edit-id]")).find((node) => node.dataset.queueEditId === id);
  return String(editor?.value ?? "").trim();
}

function saveQueueItemEdit(panel: HTMLElement, id: string): void {
  const item = queueItemById(id);
  if (!item || item.status === "sending") return;
  const text = queueEditTextFromPanel(panel, id);
  if (!text) {
    publishMessageQueueState("Queue edit blocked: message text is empty.");
    return;
  }
  item.text = text;
  item.status = item.status === "failed" ? "queued" : item.status;
  item.detail = "Edited in browser queue panel.";
  item.editing = false;
  item.draftText = "";
  item.updatedAt = new Date().toISOString();
  publishMessageQueueState("Queue item saved.");
  syncComposerQueueChrome();
}

function deleteQueueItem(id: string): void {
  const item = queueItemById(id);
  if (!item || item.status === "sending") {
    publishMessageQueueState("Queue delete blocked: item is currently sending.");
    return;
  }
  messageQueueItems = messageQueueItems.filter((candidate) => candidate.id !== id);
  messageQueueFilePayloads.delete(id);
  publishMessageQueueState("Queue item deleted.");
  syncComposerQueueChrome();
}

function moveQueueItem(id: string, direction: -1 | 1): void {
  const visible = visibleQueueItems();
  const visibleIndex = visible.findIndex((item) => item.id === id);
  const target = visible[visibleIndex + direction];
  if (!target) return;
  const from = queueItemIndexById(id);
  const to = queueItemIndexById(target.id);
  if (from < 0 || to < 0) return;
  [messageQueueItems[from], messageQueueItems[to]] = [messageQueueItems[to], messageQueueItems[from]];
  publishMessageQueueState("Queue sequence updated.");
  syncComposerQueueChrome();
}

function reorderQueueItem(draggedId: string, targetId: string): void {
  if (!draggedId || !targetId || draggedId === targetId) return;
  const from = queueItemIndexById(draggedId);
  const to = queueItemIndexById(targetId);
  if (from < 0 || to < 0) return;
  const [item] = messageQueueItems.splice(from, 1);
  const targetIndex = queueItemIndexById(targetId);
  messageQueueItems.splice(Math.max(0, targetIndex), 0, item);
  publishMessageQueueState("Queue sequence updated.");
  syncComposerQueueChrome();
}

function ensureMessageQueueChromeStyle(): void {
  if (document.getElementById(MESSAGE_QUEUE_CHROME_STYLE_ID)) return;
  const style = document.createElement("style");
  style.id = MESSAGE_QUEUE_CHROME_STYLE_ID;
  style.textContent = `
    #${MESSAGE_QUEUE_BUTTON_ID} {
      position: fixed;
      z-index: 2147483645;
      box-sizing: border-box;
      width: 28px;
      height: 28px;
      border: 1px solid rgba(255,112,28,0.82);
      border-radius: 999px;
      background: rgba(0,0,0,0.88);
      color: #ffd2b0;
      font: 800 11px/26px ui-sans-serif, system-ui, sans-serif;
      text-align: center;
      box-shadow: 0 0 12px rgba(255,112,28,0.34);
      cursor: pointer;
    }
    #${MESSAGE_QUEUE_BUTTON_ID}[data-count="0"] {
      border-color: rgba(255,255,255,0.22);
      color: rgba(255,255,255,0.70);
      box-shadow: none;
    }
    #${MESSAGE_QUEUE_SEND_NEXT_BUTTON_ID} {
      position: fixed;
      z-index: 2147483645;
      box-sizing: border-box;
      width: 30px;
      height: 24px;
      border: 1px solid rgba(56,189,248,0.72);
      border-radius: 9px;
      background: rgba(0,0,0,0.92);
      color: rgba(224,242,254,0.96);
      font: 800 10px/22px ui-sans-serif, system-ui, sans-serif;
      text-align: center;
      box-shadow: 0 0 12px rgba(56,189,248,0.28);
      cursor: pointer;
    }
    #${MESSAGE_QUEUE_SEND_NEXT_BUTTON_ID}[data-disabled="true"] {
      opacity: 0.42;
      cursor: default;
      box-shadow: none;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-float-base {
      display: grid;
      gap: 6px;
      align-self: end;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-float-top {
      display: grid;
      grid-template-columns: auto auto minmax(0, 1fr);
      align-items: center;
      gap: 6px;
      position: relative;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-float-top[data-has-count="true"] {
      grid-template-columns: auto auto minmax(0, 1fr) auto;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-gateway-dot {
      position: relative;
      top: auto;
      left: auto;
      width: 9px;
      height: 9px;
      border-radius: 999px;
      cursor: pointer;
      background: #facc15;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(250,204,21,0.35);
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-gateway-dot[data-gateway-tone="green"] {
      background: #34d399;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(52,211,153,0.40);
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-gateway-dot[data-gateway-tone="yellow"] {
      background: #facc15;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(250,204,21,0.38);
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-gateway-dot[data-gateway-tone="red"] {
      background: #fb7185;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(251,113,133,0.42);
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-count-badge {
      justify-self: end;
      min-width: 24px;
      height: 18px;
      border-radius: 999px;
      padding: 0 5px;
      border: 1px solid rgba(255,112,28,0.45);
      background: rgba(255,112,28,0.16);
      color: rgba(255,229,208,0.96);
      font: 900 9px/16px ui-sans-serif, system-ui, sans-serif;
      text-align: center;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-icon-row {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 5px;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-icon-button {
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 8px;
      background: rgba(255,255,255,0.06);
      color: rgba(255,255,255,0.76);
      height: 28px;
      min-width: 0;
      padding: 0;
      font: 900 13px/26px ui-sans-serif, system-ui, sans-serif;
      cursor: pointer;
      pointer-events: auto;
      text-align: center;
      white-space: nowrap;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-icon-button[data-primary="true"] {
      border-color: rgba(255,112,28,0.50);
      background: rgba(255,112,28,0.13);
      color: rgba(255,229,208,0.96);
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-icon-button[data-disabled="true"] {
      opacity: 0.42;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-icon-button[data-active="true"] {
      border-color: rgba(56,189,248,0.64);
      background: rgba(8,47,73,0.52);
      color: rgba(224,242,254,0.96);
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-add-button {
      height: 30px;
      border-color: rgba(255,112,28,0.58);
      background: rgba(255,112,28,0.15);
      color: rgba(255,229,208,0.98);
      font-size: 16px;
      line-height: 28px;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-add-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 34px;
      gap: 5px;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-float-secondary {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 5px;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-float-secondary .ion-queue-icon-button {
      height: 23px;
      font: 900 10px/21px ui-sans-serif, system-ui, sans-serif;
    }
    #${MESSAGE_QUEUE_PANEL_ID} {
      position: fixed;
      z-index: 2147483645;
      box-sizing: border-box;
      display: grid;
      align-content: end;
      width: 280px;
      max-width: calc(100vw - 24px);
      max-height: min(52vh, 440px);
      overflow: hidden;
      padding: 9px;
      border: 1px solid rgba(56,189,248,0.28);
      border-radius: 13px;
      background: linear-gradient(180deg, rgba(1,12,20,0.96), rgba(0,0,0,0.94));
      color: rgba(255,255,255,0.82);
      box-shadow: 0 16px 42px rgba(0,0,0,0.50), inset 0 1px 0 rgba(255,255,255,0.06);
      font: 11px/1.35 ui-sans-serif, system-ui, sans-serif;
      pointer-events: auto;
      gap: 7px;
    }
    #${MESSAGE_QUEUE_PANEL_ID}[data-visible="false"] {
      display: none;
    }
    #${MESSAGE_QUEUE_PANEL_ID}[data-expanded="false"] {
      width: ${MESSAGE_QUEUE_PANEL_MINI_WIDTH_PX}px;
      min-height: 118px;
      padding: 6px;
      border-radius: 10px;
      gap: 5px;
      cursor: pointer;
    }
    #${MESSAGE_QUEUE_PANEL_ID}[data-expanded="false"] .ion-queue-float-secondary {
      display: none;
    }
    #${MESSAGE_QUEUE_PANEL_ID}[data-expanded="false"] .ion-queue-float-list[data-empty="true"] {
      display: none;
    }
    #${MESSAGE_QUEUE_PANEL_ID}[data-expanded="false"] .ion-queue-float-list {
      gap: 4px;
      max-height: min(42vh, 360px);
      padding-right: 0;
    }
    #${MESSAGE_QUEUE_PANEL_ID}[data-expanded="false"] .ion-queue-float-line {
      grid-template-columns: 1fr;
      gap: 2px;
      padding: 5px;
      border-radius: 7px;
      white-space: normal;
    }
    #${MESSAGE_QUEUE_PANEL_ID}[data-expanded="false"] .ion-queue-float-status {
      font-size: 8px;
      line-height: 1.1;
    }
    #${MESSAGE_QUEUE_PANEL_ID}[data-expanded="false"] .ion-queue-float-text {
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      white-space: normal;
      font-size: 9px;
      line-height: 1.2;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-float-list {
      display: grid;
      gap: 5px;
      max-height: min(42vh, ${MESSAGE_QUEUE_PANEL_VIS_LIST_LIMIT * MESSAGE_QUEUE_PANEL_ROW_HEIGHT_PX}px);
      overflow-y: auto;
      padding-right: 2px;
      align-self: end;
      scrollbar-width: thin;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-float-line {
      display: grid;
      grid-template-columns: 58px 1fr;
      gap: 6px;
      padding: 6px 7px;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 8px;
      background: rgba(255,255,255,0.04);
      min-width: 0;
      white-space: nowrap;
    }
    #${MESSAGE_QUEUE_PANEL_ID}[data-expanded="true"] .ion-queue-float-line {
      grid-template-columns: 16px 54px minmax(0, 1fr) auto;
      align-items: start;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-float-line[data-dragging="true"] {
      opacity: 0.45;
      border-color: rgba(56,189,248,0.74);
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-drag-handle {
      color: rgba(255,255,255,0.38);
      cursor: grab;
      font: 900 13px/1 ui-sans-serif, system-ui, sans-serif;
      padding-top: 1px;
      user-select: none;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-row-main {
      display: grid;
      gap: 4px;
      min-width: 0;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-row-actions {
      display: grid;
      grid-template-columns: repeat(2, 22px);
      gap: 4px;
      justify-content: end;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-row-button {
      width: 22px;
      height: 22px;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 7px;
      background: rgba(255,255,255,0.06);
      color: rgba(255,255,255,0.78);
      padding: 0;
      font: 900 11px/20px ui-sans-serif, system-ui, sans-serif;
      cursor: pointer;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-row-button[data-danger="true"] {
      border-color: rgba(251,113,133,0.42);
      color: rgba(255,210,218,0.92);
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-row-button[data-disabled="true"] {
      opacity: 0.36;
      cursor: default;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-edit-text {
      box-sizing: border-box;
      width: 100%;
      min-height: 88px;
      resize: vertical;
      border: 1px solid rgba(56,189,248,0.30);
      border-radius: 7px;
      background: rgba(0,0,0,0.34);
      color: rgba(255,255,255,0.90);
      padding: 6px;
      font: 10px/1.35 ui-sans-serif, system-ui, sans-serif;
      outline: none;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-edit-text:focus {
      border-color: rgba(56,189,248,0.72);
      box-shadow: 0 0 0 3px rgba(56,189,248,0.10);
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-float-status {
      color: #ffb27a;
      text-transform: uppercase;
      font-size: 9px;
      font-weight: 800;
    }
    #${MESSAGE_QUEUE_PANEL_ID} .ion-queue-float-text {
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  `;
  document.documentElement.appendChild(style);
}

function ensureLeftDockChromeStyle(): void {
  if (document.getElementById(CHATGPT_LEFT_ICON_DOCK_STYLE_ID)) return;
  const style = document.createElement("style");
  style.id = CHATGPT_LEFT_ICON_DOCK_STYLE_ID;
  style.textContent = `
    #${CHATGPT_LEFT_ICON_DOCK_ID} {
      position: fixed;
      z-index: 2147483645;
      box-sizing: border-box;
      display: grid;
      align-content: end;
      align-items: end;
      width: ${LEFT_DOCK_PANEL_WIDTH_MINI_PX}px;
      max-width: min(46vw, 320px);
      max-height: min(54vh, 400px);
      overflow: hidden;
      padding: 7px;
      border: 1px solid rgba(255,112,28,0.28);
      border-radius: 12px;
      background: linear-gradient(180deg, rgba(1,12,20,0.96), rgba(0,0,0,0.94));
      color: rgba(255,255,255,0.84);
      box-shadow: 0 16px 42px rgba(0,0,0,0.50), inset 0 1px 0 rgba(255,255,255,0.06);
      font: 11px/1.35 ui-sans-serif, system-ui, sans-serif;
      pointer-events: auto;
      cursor: default;
      gap: 6px;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-visible="false"] {
      display: none;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-expanded="false"] {
      width: ${LEFT_DOCK_PANEL_WIDTH_MINI_PX}px;
      min-height: 138px;
      padding: 6px;
      border-radius: 12px;
      gap: 5px;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-expanded="false"] .ion-left-dock-title,
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-expanded="false"] .ion-left-dock-section-title,
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-expanded="false"] .ion-left-dock-status,
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-expanded="false"] .ion-left-dock-action-list,
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-expanded="false"] .ion-left-dock-project-list {
      display: none;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-expanded="false"] .ion-left-dock-top {
      grid-template-columns: auto auto;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-expanded="false"] .ion-left-dock-toggle-label {
      display: none;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-expanded="false"] .ion-left-dock-quick {
      grid-template-columns: repeat(1, minmax(0,1fr));
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-top {
      display: grid;
      grid-template-columns: 9px minmax(0, 1fr) auto auto;
      align-items: center;
      gap: 5px;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-toggle-label {
      font: 700 9px/1.1 ui-sans-serif, system-ui, sans-serif;
      text-transform: uppercase;
      letter-spacing: 0.01em;
      color: rgba(255,229,208,0.9);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      text-align: right;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-dot {
      width: 9px;
      height: 9px;
      border-radius: 999px;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(255,255,255,0.2);
      border: 1px solid rgba(255,255,255,0.25);
      opacity: 0.95;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-dot[data-tone="green"] {
      background: #34d399;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(52,211,153,0.45);
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-dot[data-tone="yellow"] {
      background: #facc15;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(250,204,21,0.45);
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-dot[data-tone="red"] {
      background: #fb7185;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(251,113,133,0.45);
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-status {
      color: rgba(255,229,208,0.86);
      font-size: 9px;
      line-height: 1.15;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-icon-button {
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 9px;
      background: rgba(255,255,255,0.06);
      color: rgba(255,255,255,0.78);
      min-height: 24px;
      min-width: 0;
      padding: 0 4px;
      font: 900 11px/22px ui-sans-serif, system-ui, sans-serif;
      cursor: pointer;
      text-align: center;
      white-space: nowrap;
      width: 100%;
      box-sizing: border-box;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-icon-button[data-primary="true"] {
      border-color: rgba(255,112,28,0.52);
      background: rgba(255,112,28,0.12);
      color: rgba(255,229,208,0.98);
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-icon-button[data-disabled="true"] {
      opacity: 0.42;
      cursor: default;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-quick {
      display: grid;
      grid-template-columns: repeat(3, minmax(0,1fr));
      gap: 4px;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-action-list,
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-project-list {
      display: grid;
      gap: 5px;
      max-height: 190px;
      overflow: auto;
      padding-right: 2px;
      scrollbar-width: thin;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-section-title {
      color: rgba(209,250,229,0.96);
      text-transform: uppercase;
      font: 900 9px/1.2 ui-sans-serif, system-ui, sans-serif;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      letter-spacing: 0.01em;
      margin-top: 1px;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-project-row {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 4px;
      align-items: center;
      padding: 4px;
      border: 1px solid rgba(255,255,255,0.10);
      border-radius: 8px;
      background: rgba(255,255,255,0.03);
      min-width: 0;
      cursor: default;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-project-name {
      min-width: 0;
      color: rgba(255,255,255,0.85);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font: 700 10px/1.2 ui-sans-serif, system-ui, sans-serif;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-project-subtitle {
      color: rgba(255,255,255,0.65);
      font-size: 9px;
      line-height: 1.2;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-empty {
      color: rgba(209,250,229,0.86);
      padding: 4px 2px;
      border: 1px dashed rgba(209,250,229,0.28);
      border-radius: 7px;
      text-align: center;
      font-size: 9px;
      line-height: 1.25;
    }
  `;
  document.documentElement.appendChild(style);
}

function leftDockTone(): "green" | "yellow" | "red" {
  if (messageQueueItems.some((item) => item.status === "failed") || browserQueueGatewayStatus.toLowerCase().includes("failed") || messageQueuePaused) {
    return "red";
  }
  if (!messageQueueItems.length || browserQueueGatewayStatus.includes("warming")) return "yellow";
  return "green";
}

function leftDockButton(action: string, icon: string, title: string, primary = false, disabled = false): HTMLButtonElement {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "ion-left-dock-icon-button";
  button.dataset.leftDockAction = action;
  button.textContent = icon;
  button.title = title;
  button.setAttribute("aria-label", title);
  button.disabled = disabled;
  button.dataset.disabled = String(Boolean(disabled));
  button.dataset.primary = String(Boolean(primary));
  button.setAttribute("aria-disabled", String(Boolean(disabled)));
  return button;
}

function ensureLeftDockChrome(): HTMLElement {
  ensureLeftDockChromeStyle();
  let dock = document.getElementById(CHATGPT_LEFT_ICON_DOCK_ID) as HTMLElement | null;
  if (!dock) {
    dock = document.createElement("div");
    dock.id = CHATGPT_LEFT_ICON_DOCK_ID;
    dock.className = CHATGPT_LEFT_ICON_DOCK_CLASS;
    dock.dataset.visible = "true";
    dock.dataset.expanded = String(leftDockProjectPanelExpanded);
    dock.addEventListener("click", (event) => {
      const source = event.target instanceof Element ? event.target.closest<HTMLElement>("[data-left-dock-action]") : null;
      const action = source?.dataset.leftDockAction ?? "";
      const projectPath = source?.dataset.leftDockProjectPath ?? "";
      if (!action && dock?.dataset.expanded === "false") {
        leftDockProjectPanelExpanded = true;
        persistLeftDockPanelExpanded(leftDockProjectPanelExpanded);
        syncLeftDockChrome();
        return;
      }
      if (action === "toggle-panel") {
        leftDockProjectPanelExpanded = !leftDockProjectPanelExpanded;
        persistLeftDockPanelExpanded(leftDockProjectPanelExpanded);
      } else if (action === "open-context-workflow") {
        contextWorkflowPanelExpanded = true;
        syncContextWorkflowRail();
      } else if (action === "open-queue") {
        messageQueuePanelExpanded = true;
        syncComposerQueueChrome();
      } else if (action === "queue-send") {
        if (!messageQueueItems.length) {
          publishMessageQueueState("Queue is empty.");
        } else {
          void processMessageQueue("manual");
        }
      } else if (action === "queue-pause") {
        messageQueuePaused = !messageQueuePaused;
        publishMessageQueueState(messageQueuePaused ? "Queue paused from left dock." : "Queue resumed from left dock.");
        syncComposerQueueChrome();
      } else if (action === "project-refresh") {
        void requestProjectsRefresh();
      } else if (action === "project-sync") {
        const paths = projectPathsOrDefault(contextWorkflowSelectedPaths());
        if (!paths.length) {
          setBridgeProjectsState({ contextSyncStatus: "No project package selected for context sync." });
          return;
        }
        requestProjectContextSync(paths);
      } else if (action === "project-select") {
        if (!projectPath) return;
        const next = new Set(selectedProjectPackagePaths);
        if (next.has(projectPath)) next.delete(projectPath);
        else next.add(projectPath);
        const selected = Array.from(next);
        applyContextWorkflowSelectedPaths(selected.length ? selected : [projectPath]);
      } else if (action === "project-pack-open") {
        leftDockProjectPanelExpanded = true;
        window.dispatchEvent(new CustomEvent("ion-chatops-projects-refresh"));
      } else if (action === "queue-play-next") {
        if (!nextQueuedMessage()) {
          publishMessageQueueState("Queue is empty.");
        } else {
          void processMessageQueue("manual", true);
        }
      } else if (action === "queue-cancel") {
        messageQueueItems = [];
        messageQueueFilePayloads.clear();
        publishMessageQueueState("Queue cleared from left dock.");
      } else if (action === "bounded-status") {
        window.dispatchEvent(new CustomEvent("ion-chatops-bounded-agent-status"));
      } else if (action === "rescan-page") {
        seen.clear();
        scan("manual");
      }
      syncComposerQueueChrome();
      syncContextWorkflowRail();
      syncLeftDockChrome();
    });
    document.documentElement.appendChild(dock);
  }
  return dock;
}

function renderLeftDockChrome(): void {
  const dock = ensureLeftDockChrome();
  const selectedPaths = contextWorkflowSelectedPaths();
  const isExpanded = leftDockProjectPanelExpanded;
  const queueCount = messageQueueItems.filter((item) => item.status === "queued" || item.status === "waiting" || item.status === "sending" || item.status === "failed").length;
  const selectedProjectCount = selectedPaths.length;
  dock.dataset.expanded = String(isExpanded);
  dock.innerHTML = "";

  const top = document.createElement("div");
  top.className = "ion-left-dock-top";
  const dot = document.createElement("span");
  dot.className = "ion-left-dock-dot";
  dot.setAttribute("aria-hidden", "true");
  dot.dataset.tone = leftDockTone();
  const title = document.createElement("div");
  title.className = "ion-left-dock-title";
  title.style.cssText = "min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: rgba(209,250,229,0.96); font: 900 10px/1.2 ui-sans-serif, system-ui, sans-serif; text-transform: uppercase; letter-spacing: 0.01em;";
  title.textContent = "ION Left";
  const toggle = leftDockButton("toggle-panel", isExpanded ? "−" : "⇢", isExpanded ? "Minimize left dock panel" : "Expand left dock panel");
  const label = document.createElement("div");
  label.className = "ion-left-dock-toggle-label";
  label.textContent = isExpanded ? "expanded" : "compact";
  top.append(dot, title, toggle, label);
  dock.appendChild(top);

  const status = document.createElement("div");
  status.className = "ion-left-dock-status";
  status.textContent = `${queueCount} queue · ${projectPackages.length} project${projectPackages.length === 1 ? "" : "s"} · ${selectedProjectCount} selected`;
  dock.appendChild(status);

  const quick = document.createElement("div");
  quick.className = "ion-left-dock-quick";
  quick.append(
    leftDockButton("open-queue", "Q", "Open queue panel"),
    leftDockButton("queue-send", "▶", queueCount ? "Send next queued message" : "Queue is empty", false, !queueCount),
    leftDockButton("queue-play-next", "⏯", "Send now (manual next)", false, !queueCount),
  );
  dock.appendChild(quick);

  if (!isExpanded) {
    return;
  }

  const actions = document.createElement("div");
  actions.className = "ion-left-dock-action-list";
  const actionTitle = document.createElement("div");
  actionTitle.className = "ion-left-dock-section-title";
  actionTitle.textContent = "Actions";
  actions.append(actionTitle);
  actions.append(
    leftDockButton("project-refresh", "↻", "Refresh ION project package list"),
    leftDockButton("project-sync", "⇄", "Build context sync ZIP for selected projects"),
    leftDockButton("open-context-workflow", "C", "Open context workflow rail"),
    leftDockButton("bounded-status", "A", "Read bounded-agent status"),
    leftDockButton("rescan-page", "R", "Rescan page for actions"),
    leftDockButton("queue-cancel", "⌫", "Clear queued items"),
    leftDockButton("queue-pause", messageQueuePaused ? "▶" : "⏸", messageQueuePaused ? "Resume queue" : "Pause queue"),
    leftDockButton("project-pack-open", "P", "Open project package controls"),
  );
  dock.appendChild(actions);

  const projectTitle = document.createElement("div");
  projectTitle.className = "ion-left-dock-section-title";
  projectTitle.textContent = "Projects";
  dock.appendChild(projectTitle);

  const list = document.createElement("div");
  list.className = "ion-left-dock-project-list";
  if (!projectPackages.length) {
    const empty = document.createElement("div");
    empty.className = "ion-left-dock-empty";
    empty.textContent = "No ION project packages discovered. Refresh first.";
    list.appendChild(empty);
  } else {
    for (const pkg of projectPackages.slice(0, 12)) {
      const row = document.createElement("div");
      row.className = "ion-left-dock-project-row";
      const names = document.createElement("div");
      names.append(document.createElement("div"), document.createElement("div"));
      const name = names.children[0] as HTMLDivElement;
      const sub = names.children[1] as HTMLDivElement;
      name.className = "ion-left-dock-project-name";
      name.textContent = pkg.project;
      sub.className = "ion-left-dock-project-subtitle";
      sub.textContent = `${pkg.version || "context package"} · ${pkg.kind}`;
      const selectBtn = leftDockButton("project-select", selectedPaths.includes(pkg.path) ? "☑" : "☐", "Toggle project selection");
      selectBtn.dataset.leftDockProjectPath = pkg.path;
      row.append(names, selectBtn);
      list.appendChild(row);
    }
  }
  dock.appendChild(list);
}

function syncLeftDockChrome(): void {
  const dock = ensureLeftDockChrome();
  if (!dock) return;
  const input = findComposerInput();
  if (!input) {
    dock.dataset.visible = "false";
    return;
  }
  renderLeftDockChrome();
  const topPosition = Math.max(8, Math.round(window.innerHeight * 0.48));
  const width = leftDockProjectPanelExpanded
    ? Math.max(LEFT_DOCK_PANEL_WIDTH_MINI_PX + 1, Math.min(LEFT_DOCK_PANEL_WIDTH_EXPANDED_PX, Math.floor(window.innerWidth * 0.24)))
    : LEFT_DOCK_PANEL_WIDTH_MINI_PX;
  const containerRect = findComposerContainer(input).getBoundingClientRect();
  const anchorRect = lastQueueChromeRect ?? containerRect;
  const panelBottom = composerSidePanelBottom(anchorRect);
  const boundedTopPosition = Math.max(8, Math.min(topPosition, window.innerHeight - panelBottom - 150));
  dock.style.left = "8px";
  dock.style.top = `${boundedTopPosition}px`;
  dock.style.bottom = `${panelBottom}px`;
  dock.style.width = `${width}px`;
  dock.style.maxHeight = `${Math.max(138, window.innerHeight - boundedTopPosition - panelBottom)}px`;
}

function cutComposerTextToQueue(): void {
  const input = findComposerInput();
  if (!input) {
    publishMessageQueueState("Queue button blocked: composer input not found.");
    return;
  }
  const text = composerText(input).trim();
  if (!text) {
    publishMessageQueueState("Queue button: write text in the composer first.");
    return;
  }
  addQueuedMessages(text);
  clearComposerText(input);
  publishMessageQueueState("Composer text cut into queue.");
  syncComposerQueueChrome();
}

function ensureMessageQueueFileInput(): HTMLInputElement {
  let input = document.getElementById(MESSAGE_QUEUE_FILE_INPUT_ID) as HTMLInputElement | null;
  if (!input) {
    input = document.createElement("input");
    input.id = MESSAGE_QUEUE_FILE_INPUT_ID;
    input.type = "file";
    input.multiple = true;
    input.accept = ".zip,.tar,.gz,.bz2,.7z,.pdf,.txt,.md,.json,.yml,.yaml,.csv,.png,.jpg,.jpeg,.webp,.gif,.bmp,.svg,.mp4,image/*";
    input.style.display = "none";
    input.addEventListener("change", () => {
      queueFiles(Array.from(input?.files ?? []));
    });
    document.documentElement.appendChild(input);
  }
  return input;
}

function ensureComposerQueueChrome(): { button: HTMLButtonElement; sendNextButton: HTMLButtonElement; panel: HTMLElement } {
  ensureMessageQueueChromeStyle();
  let button = document.getElementById(MESSAGE_QUEUE_BUTTON_ID) as HTMLButtonElement | null;
  if (!button) {
    button = document.createElement("button");
    button.id = MESSAGE_QUEUE_BUTTON_ID;
    button.type = "button";
    button.textContent = "Q+";
    button.title = "Cut composer text into ION queue";
    button.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      cutComposerTextToQueue();
    });
    button.addEventListener("mouseenter", () => {
      const panel = document.getElementById(MESSAGE_QUEUE_PANEL_ID);
      if (panel) panel.dataset.visible = "true";
    });
    document.documentElement.appendChild(button);
  }
  let sendNextButton = document.getElementById(MESSAGE_QUEUE_SEND_NEXT_BUTTON_ID) as HTMLButtonElement | null;
  if (!sendNextButton) {
    sendNextButton = document.createElement("button");
    sendNextButton.id = MESSAGE_QUEUE_SEND_NEXT_BUTTON_ID;
    sendNextButton.type = "button";
    sendNextButton.textContent = "Q▶";
    sendNextButton.title = "Paste and send next ION queued message";
    sendNextButton.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      if (!nextQueuedMessage()) {
        publishMessageQueueState("Queue is empty.");
        return;
      }
      void processMessageQueue("manual-send-next", true);
    });
    document.documentElement.appendChild(sendNextButton);
  }
  let panel = document.getElementById(MESSAGE_QUEUE_PANEL_ID);
  if (!panel) {
    panel = document.createElement("div");
    panel.id = MESSAGE_QUEUE_PANEL_ID;
    panel.dataset.visible = "false";
    panel.addEventListener("click", (event) => {
      const source = event.target instanceof Element ? event.target.closest<HTMLElement>("[data-queue-float-action]") : null;
      const action = source?.dataset.queueFloatAction ?? "";
      const itemId = source?.dataset.queueItemId ?? "";
      if (!action && panel?.dataset.expanded === "false") {
        messageQueuePanelExpanded = true;
        syncComposerQueueChrome();
      } else if (action === "toggle-panel") {
        messageQueuePanelExpanded = !messageQueuePanelExpanded;
        syncComposerQueueChrome();
      } else if (action === "add-current") {
        cutComposerTextToQueue();
      } else if (action === "add-files") {
        openMessageQueueFilePicker();
      } else if (action === "pause-local") {
        messageQueuePaused = !messageQueuePaused;
        publishMessageQueueState(messageQueuePaused ? "Queue paused." : "Queue resumed.");
        syncComposerQueueChrome();
      } else if (action === "auto") {
        messageQueueAutoPlay = !messageQueueAutoPlay;
        if (messageQueueAutoPlay) messageQueueSawActiveOutput = chatReadiness().activeOutput;
        publishMessageQueueState(messageQueueAutoPlay ? "Auto Play armed. It will send after output finishes." : "Auto Play off. Use Q▶ to send next.");
        syncComposerQueueChrome();
      } else if (action === "next") {
        if (!nextQueuedMessage()) {
          publishMessageQueueState("Queue is empty.");
          return;
        }
        void processMessageQueue("panel-send-next", true);
      } else if (action === "edit-item" && itemId) {
        setQueueItemEditing(itemId, true);
      } else if (action === "save-item" && itemId) {
        saveQueueItemEdit(panel!, itemId);
      } else if (action === "cancel-edit" && itemId) {
        setQueueItemEditing(itemId, false);
      } else if (action === "delete-item" && itemId) {
        deleteQueueItem(itemId);
      } else if (action === "move-up" && itemId) {
        moveQueueItem(itemId, -1);
      } else if (action === "move-down" && itemId) {
        moveQueueItem(itemId, 1);
      } else if (action === "gateway-pause") {
        void gatewayRequest("ion_chatops_browser_queue_control", { operation: "pause" }).then(() => pollBrowserQueueCarrier());
      } else if (action === "gateway-resume") {
        browserQueueAutoTurnsThisSession = 0;
        void gatewayRequest("ion_chatops_browser_queue_control", { operation: "resume" }).then(() => pollBrowserQueueCarrier());
      } else if (action === "gateway-kill") {
        void gatewayRequest("ion_chatops_browser_queue_control", { operation: "kill" }).then(() => pollBrowserQueueCarrier());
      } else if (action === "gateway-auto-accept") {
        const operation = browserQueueAutoAcceptActive ? "auto_accept_off" : "auto_accept_on";
        void gatewayRequest("ion_chatops_browser_queue_control", { operation, ttl_seconds: browserQueueAutoAcceptTtlSeconds }).then(() => pollBrowserQueueCarrier());
      } else if (action === "gateway-approve" && browserQueueApprovalPacketId) {
        void gatewayRequest("ion_chatops_browser_queue_control", { operation: "approve", packet_id: browserQueueApprovalPacketId }).then(() => pollBrowserQueueCarrier());
      }
    });
    panel.addEventListener("dragstart", (event) => {
      const row = event.target instanceof Element ? event.target.closest<HTMLElement>("[data-queue-item-id]") : null;
      const id = row?.dataset.queueItemId ?? "";
      if (!id || row?.dataset.draggable !== "true") return;
      messageQueueDragItemId = id;
      row.dataset.dragging = "true";
      event.dataTransfer?.setData("text/plain", id);
      if (event.dataTransfer) event.dataTransfer.effectAllowed = "move";
    });
    panel.addEventListener("dragover", (event) => {
      const row = event.target instanceof Element ? event.target.closest<HTMLElement>("[data-queue-item-id]") : null;
      if (!messageQueueDragItemId || !row || row.dataset.queueItemId === messageQueueDragItemId) return;
      event.preventDefault();
      if (event.dataTransfer) event.dataTransfer.dropEffect = "move";
    });
    panel.addEventListener("drop", (event) => {
      const row = event.target instanceof Element ? event.target.closest<HTMLElement>("[data-queue-item-id]") : null;
      const targetId = row?.dataset.queueItemId ?? "";
      const draggedId = event.dataTransfer?.getData("text/plain") || messageQueueDragItemId;
      if (!draggedId || !targetId || draggedId === targetId) return;
      event.preventDefault();
      reorderQueueItem(draggedId, targetId);
    });
    panel.addEventListener("dragend", () => {
      messageQueueDragItemId = "";
      panel!.querySelectorAll<HTMLElement>("[data-dragging]").forEach((row) => {
        delete row.dataset.dragging;
      });
    });
    document.documentElement.appendChild(panel);
  }
  return { button, sendNextButton, panel };
}

function queueIconButton(action: string, icon: string, title: string, primary = false, disabled = false): HTMLButtonElement {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "ion-queue-icon-button";
  button.dataset.queueFloatAction = action;
  button.dataset.primary = String(primary);
  button.textContent = icon;
  button.title = title;
  button.setAttribute("aria-label", title);
  button.disabled = disabled;
  button.dataset.disabled = String(Boolean(disabled));
  button.setAttribute("aria-disabled", String(Boolean(disabled)));
  return button;
}

function queueRowButton(action: string, itemId: string, icon: string, title: string, options: { danger?: boolean; disabled?: boolean } = {}): HTMLButtonElement {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "ion-queue-row-button";
  button.dataset.queueFloatAction = action;
  button.dataset.queueItemId = itemId;
  button.dataset.danger = String(Boolean(options.danger));
  button.dataset.disabled = String(Boolean(options.disabled));
  button.textContent = icon;
  button.title = title;
  button.setAttribute("aria-label", title);
  if (options.disabled) button.disabled = true;
  return button;
}

function queueGatewayTone(): "green" | "yellow" | "red" {
  if (/blocked|failed|error|killed/i.test(browserQueueGatewayStatus)) return "red";
  if (/warming|approval|cap reached|paused/i.test(browserQueueGatewayStatus)) return "yellow";
  return "green";
}

function queueCountBadgeLabel(total: number): string {
  return total > 10 ? "10+" : "";
}

function renderComposerQueuePanel(panel: HTMLElement): void {
  const queuedItems = visibleQueueItems();
  const visibleItems = queuedItems.slice(0, MESSAGE_QUEUE_PANEL_VIS_LIST_LIMIT);
  const totalVisibleItems = queuedItems.length;
  const countBadgeLabel = queueCountBadgeLabel(totalVisibleItems);
  const canPlayNext = Boolean(nextQueuedMessage());
  panel.dataset.expanded = String(messageQueuePanelExpanded);
  panel.innerHTML = "";
  if (messageQueuePanelExpanded || totalVisibleItems) {
    const list = document.createElement("div");
    list.className = "ion-queue-float-list";
    list.dataset.empty = String(!visibleItems.length);
    if (!visibleItems.length) {
      const empty = document.createElement("div");
      empty.className = "ion-queue-float-line";
      empty.innerHTML = `<span class="ion-queue-float-status">empty</span><span class="ion-queue-float-text">Composer text can be added from the controls below.</span>`;
      list.appendChild(empty);
    } else {
      visibleItems.forEach((item, index) => {
        const row = document.createElement("div");
        row.className = "ion-queue-float-line";
        row.dataset.queueItemId = item.id;
        row.dataset.draggable = String(messageQueuePanelExpanded && item.status !== "sending");
        if (messageQueuePanelExpanded && item.status !== "sending") row.draggable = true;
        const handle = document.createElement("span");
        handle.className = "ion-queue-drag-handle";
        handle.textContent = "⋮";
        handle.title = "Drag to reorder";
        const status = document.createElement("span");
        status.className = "ion-queue-float-status";
        status.textContent = item.gateway ? `GW ${item.status}` : item.kind === "files" ? `FILE ${item.status}` : item.status;
        const main = document.createElement("div");
        main.className = "ion-queue-row-main";
        if (item.editing && messageQueuePanelExpanded) {
          const editor = document.createElement("textarea");
          editor.className = "ion-queue-edit-text";
          editor.dataset.queueEditId = item.id;
          editor.value = item.draftText ?? item.text;
          editor.spellcheck = true;
          main.appendChild(editor);
        } else {
          const copy = document.createElement("span");
          copy.className = "ion-queue-float-text";
          copy.textContent = item.text.replace(/\s+/g, " ");
          copy.title = item.detail ? `${item.text}\n\n${item.detail}` : item.text;
          main.appendChild(copy);
        }
        if (messageQueuePanelExpanded) {
          const actions = document.createElement("div");
          actions.className = "ion-queue-row-actions";
          if (item.editing) {
            actions.append(
              queueRowButton("save-item", item.id, "✓", "Save queue item"),
              queueRowButton("cancel-edit", item.id, "×", "Cancel edit"),
              queueRowButton("delete-item", item.id, "⌫", "Delete queue item", { danger: true, disabled: item.status === "sending" }),
            );
          } else {
            actions.append(
              queueRowButton("move-up", item.id, "↑", "Move earlier", { disabled: index === 0 }),
              queueRowButton("move-down", item.id, "↓", "Move later", { disabled: index === visibleItems.length - 1 }),
              queueRowButton("edit-item", item.id, "✎", "Edit queue item", { disabled: item.status === "sending" }),
              queueRowButton("delete-item", item.id, "⌫", "Delete queue item", { danger: true, disabled: item.status === "sending" }),
            );
          }
          row.append(handle, status, main, actions);
        } else {
          row.append(status, main);
        }
        list.appendChild(row);
      });
    }
    panel.appendChild(list);
  }
  const base = document.createElement("div");
  base.className = "ion-queue-float-base";
  const top = document.createElement("div");
  top.className = "ion-queue-float-top";
  top.dataset.hasCount = String(Boolean(countBadgeLabel));
  const gatewayDot = document.createElement("span");
  gatewayDot.className = "ion-queue-gateway-dot";
  gatewayDot.dataset.gatewayTone = queueGatewayTone();
  gatewayDot.dataset.queueFloatAction = "toggle-panel";
  gatewayDot.title = `Gateway automation: ${browserQueueGatewayStatus} (click to toggle panel)`;
  const expandButton = queueIconButton("toggle-panel", messageQueuePanelExpanded ? "−" : "↗", messageQueuePanelExpanded ? "Minimize queue panel" : "Expand queue panel");
  top.append(gatewayDot, expandButton);
  if (countBadgeLabel) {
    const countBadge = document.createElement("span");
    countBadge.className = "ion-queue-count-badge";
    countBadge.textContent = countBadgeLabel;
    top.appendChild(countBadge);
  }
  base.appendChild(top);
  const playPause = document.createElement("div");
  playPause.className = "ion-queue-icon-row";
  const nextButton = queueIconButton("next", "▶", "Send next queued message", true, !canPlayNext);
  const pauseButton = queueIconButton("pause-local", messageQueuePaused ? "⏵" : "⏸", messageQueuePaused ? "Resume queue" : "Pause queue");
  pauseButton.dataset.active = String(messageQueuePaused);
  playPause.append(nextButton, pauseButton);
  base.appendChild(playPause);
  const addRow = document.createElement("div");
  addRow.className = "ion-queue-add-row";
  const addButton = queueIconButton("add-current", "+", "Add composer text to queue", true);
  addButton.classList.add("ion-queue-add-button");
  const addFilesButton = queueIconButton("add-files", "⇪", "Add files, ZIPs, or images to queue");
  addFilesButton.classList.add("ion-queue-add-button");
  addRow.append(addButton, addFilesButton);
  base.appendChild(addRow);
  if (messageQueuePanelExpanded) {
    const secondary = document.createElement("div");
    secondary.className = "ion-queue-float-secondary";
    const autoButton = queueIconButton("auto", "A", "Toggle Auto Play after output finishes");
    autoButton.dataset.active = String(messageQueueAutoPlay);
    const gatewayPauseButton = queueIconButton("gateway-pause", "GⅡ", "Pause the Action Gateway browser queue");
    const gatewayResumeButton = queueIconButton("gateway-resume", "G▶", "Resume the Action Gateway browser queue");
    const gatewayKillButton = queueIconButton("gateway-kill", "×", "Stop the current Action Gateway browser queue");
    secondary.append(autoButton, gatewayPauseButton, gatewayResumeButton, gatewayKillButton);
    if (browserQueueApprovalPacketId) {
      const approveButton = queueIconButton("gateway-approve", "✓", "Approve the waiting browser queue packet");
      secondary.appendChild(approveButton);
    }
    base.appendChild(secondary);
  }
  panel.appendChild(base);
  panel.dataset.visible = "true";
}

function ensureContextWorkflowRailStyle(): void {
  if (document.getElementById(CONTEXT_WORKFLOW_STYLE_ID)) return;
  const style = document.createElement("style");
  style.id = CONTEXT_WORKFLOW_STYLE_ID;
  style.textContent = `
    #${CONTEXT_WORKFLOW_PANEL_ID} {
      position: fixed;
      z-index: 2147483645;
      box-sizing: border-box;
      display: grid;
      align-content: end;
      width: 276px;
      max-width: calc(100vw - 24px);
      max-height: min(52vh, 440px);
      overflow: hidden;
      padding: 9px;
      border: 1px solid rgba(45,212,191,0.32);
      border-radius: 13px;
      background: linear-gradient(180deg, rgba(1,18,20,0.96), rgba(0,0,0,0.94));
      color: rgba(255,255,255,0.84);
      box-shadow: 0 16px 42px rgba(0,0,0,0.50), inset 0 1px 0 rgba(255,255,255,0.06);
      font: 11px/1.35 ui-sans-serif, system-ui, sans-serif;
      pointer-events: auto;
      gap: 7px;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID}[data-visible="false"] {
      display: none;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID}[data-expanded="false"] {
      width: 76px;
      min-height: 118px;
      padding: 6px;
      border-radius: 10px;
      gap: 5px;
      cursor: pointer;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID}[data-expanded="false"] .ion-context-rail-list,
    #${CONTEXT_WORKFLOW_PANEL_ID}[data-expanded="false"] .ion-context-rail-actions,
    #${CONTEXT_WORKFLOW_PANEL_ID}[data-expanded="false"] .ion-context-rail-foot,
    #${CONTEXT_WORKFLOW_PANEL_ID}[data-expanded="false"] .ion-context-rail-title {
      display: none;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID}[data-expanded="false"] .ion-context-rail-top {
      grid-template-columns: 1fr;
      justify-items: end;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID}[data-expanded="false"] .ion-context-rail-mini-stack {
      display: grid;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-mini-stack {
      display: none;
      gap: 5px;
      align-self: end;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-mini-row {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 5px;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-mini-button {
      height: 28px;
      min-width: 0;
      padding: 0;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 8px;
      background: rgba(255,255,255,0.06);
      color: rgba(209,250,229,0.90);
      font: 900 12px/26px ui-sans-serif, system-ui, sans-serif;
      cursor: pointer;
      text-align: center;
      white-space: nowrap;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-mini-button[data-primary="true"] {
      border-color: rgba(45,212,191,0.54);
      background: rgba(13,148,136,0.22);
      color: rgba(204,251,241,0.98);
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-top {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 30px;
      align-items: center;
      gap: 6px;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-dot {
      position: relative;
      top: auto;
      left: auto;
      width: 9px;
      height: 9px;
      border-radius: 999px;
      cursor: pointer;
      background: #facc15;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(250,204,21,0.35);
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-dot[data-context-tone="green"] {
      background: #34d399;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(52,211,153,0.40);
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-dot[data-context-tone="yellow"] {
      background: #facc15;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(250,204,21,0.38);
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-dot[data-context-tone="red"] {
      background: #fb7185;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(251,113,133,0.42);
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-title {
      min-width: 0;
      color: rgba(209,250,229,0.96);
      font: 900 10px/1.2 ui-sans-serif, system-ui, sans-serif;
      text-transform: uppercase;
      letter-spacing: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-icon-button,
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-action {
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 8px;
      background: rgba(255,255,255,0.06);
      color: rgba(255,255,255,0.78);
      cursor: pointer;
      pointer-events: auto;
      min-width: 0;
      text-align: center;
      white-space: nowrap;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-icon-button {
      width: 30px;
      height: 28px;
      padding: 0;
      font: 900 13px/26px ui-sans-serif, system-ui, sans-serif;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-list {
      display: grid;
      gap: 5px;
      max-height: min(32vh, 260px);
      overflow-y: auto;
      padding-right: 2px;
      scrollbar-width: thin;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-line {
      display: grid;
      grid-template-columns: 76px minmax(0, 1fr);
      gap: 6px;
      padding: 6px 7px;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 8px;
      background: rgba(255,255,255,0.04);
      min-width: 0;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-project-picker {
      display: grid;
      gap: 4px;
      max-width: 100%;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-project-picker-label {
      color: #5eead4;
      text-transform: uppercase;
      font-size: 9px;
      line-height: 1.2;
      font-weight: 800;
      letter-spacing: 0.01em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-project-select {
      width: 100%;
      box-sizing: border-box;
      min-height: 0;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 8px;
      background: rgba(255,255,255,0.05);
      color: rgba(255,255,255,0.90);
      padding: 3px 5px;
      font: 800 11px/1.25 ui-sans-serif, system-ui, sans-serif;
      outline: none;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-project-select:focus-visible {
      border-color: rgba(255,112,28,0.65);
      box-shadow: 0 0 0 3px rgba(255,112,28,0.14);
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-project-select option {
      background: rgba(1,12,20,0.96);
      color: rgba(255,255,255,0.92);
      padding: 2px 4px;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-label {
      color: #5eead4;
      text-transform: uppercase;
      font-size: 9px;
      font-weight: 900;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-value {
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      color: rgba(255,255,255,0.80);
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-actions {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 5px;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-action {
      height: 28px;
      padding: 0 6px;
      font: 900 10px/26px ui-sans-serif, system-ui, sans-serif;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-action[data-primary="true"] {
      border-color: rgba(45,212,191,0.54);
      background: rgba(13,148,136,0.22);
      color: rgba(204,251,241,0.98);
    }
    #${CONTEXT_WORKFLOW_PANEL_ID} .ion-context-rail-foot {
      color: rgba(209,250,229,0.70);
      font-size: 9px;
      line-height: 1.25;
      overflow-wrap: anywhere;
    }
    #${CONTEXT_WORKFLOW_IMPORT_INPUT_ID} {
      display: none;
    }
  `;
  document.documentElement.appendChild(style);
}

function contextWorkflowTone(): "green" | "yellow" | "red" {
  if (/blocked|failed|error|unavailable/i.test(contextWorkflowRailStatus)) return "red";
  if (!projectPackages.length || /scanning|requesting|importing|ready/i.test(contextWorkflowRailStatus)) return "yellow";
  return "green";
}

function contextWorkflowSelectedPaths(): string[] {
  const selected = selectedProjectPackagePaths.filter((path) => projectPackages.some((entry) => entry.path === path));
  if (selected.length) return selected;
  if (selectedProjectPackagePath) return [selectedProjectPackagePath];
  return projectPackages[0]?.path ? [projectPackages[0].path] : [];
}

function contextWorkflowLine(label: string, value: string): HTMLElement {
  const row = document.createElement("div");
  row.className = "ion-context-rail-line";
  const labelNode = document.createElement("span");
  labelNode.className = "ion-context-rail-label";
  labelNode.textContent = label;
  const valueNode = document.createElement("span");
  valueNode.className = "ion-context-rail-value";
  valueNode.textContent = value;
  row.append(labelNode, valueNode);
  return row;
}

function contextWorkflowAction(action: string, label: string, title: string, primary = false): HTMLButtonElement {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "ion-context-rail-action";
  button.dataset.contextWorkflowAction = action;
  button.dataset.primary = String(primary);
  button.textContent = label;
  button.title = title;
  button.setAttribute("aria-label", title);
  return button;
}

function contextWorkflowMiniButton(action: string, icon: string, title: string, primary = false): HTMLButtonElement {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "ion-context-rail-mini-button";
  button.dataset.contextWorkflowAction = action;
  button.dataset.primary = String(primary);
  button.textContent = icon;
  button.title = title;
  button.setAttribute("aria-label", title);
  return button;
}

function renderContextWorkflowRail(panel: HTMLElement): void {
  const pendingQueueItems = messageQueueItems.filter((item) => item.status !== "sent").length;
  const selectedPaths = contextWorkflowSelectedPaths();
  const selectedProject = selectedPaths.length === 1
    ? projectPackages.find((entry) => entry.path === selectedPaths[0])?.project ?? "1 package"
    : `${selectedPaths.length} packages`;
  panel.dataset.expanded = String(contextWorkflowPanelExpanded);
  panel.innerHTML = "";
  const top = document.createElement("div");
  top.className = "ion-context-rail-top";
  const dot = document.createElement("span");
  dot.className = "ion-context-rail-dot";
  dot.dataset.contextTone = contextWorkflowTone();
  dot.dataset.contextWorkflowAction = "toggle-panel";
  dot.title = `${contextWorkflowRailStatus} (click to toggle this panel)`;
  const title = document.createElement("div");
  title.className = "ion-context-rail-title";
  title.textContent = "ION Context";
  const miniStatus = document.createElement("div");
  miniStatus.className = "ion-context-rail-mini-status";
  miniStatus.textContent = projectPackages.length ? `${projectPackages.length} projects` : "sync";
  title.appendChild(miniStatus);
  const expandButton = document.createElement("button");
  expandButton.type = "button";
  expandButton.className = "ion-context-rail-icon-button";
  expandButton.dataset.contextWorkflowAction = "toggle-panel";
  expandButton.textContent = contextWorkflowPanelExpanded ? "−" : "↗";
  expandButton.title = contextWorkflowPanelExpanded ? "Minimize context workflow rail" : "Expand context workflow rail";
  top.append(dot, title, expandButton);
  panel.appendChild(top);

  if (!contextWorkflowPanelExpanded) {
    const miniStack = document.createElement("div");
    miniStack.className = "ion-context-rail-mini-stack";
    const miniRow = document.createElement("div");
    miniRow.className = "ion-context-rail-mini-row";
    miniRow.append(
      contextWorkflowMiniButton("context-pack", "C", "Insert current ION context pack"),
      contextWorkflowMiniButton("projects-refresh", "P", "Refresh project context package inventory"),
    );
    const miniRowTwo = document.createElement("div");
    miniRowTwo.className = "ion-context-rail-mini-row";
    miniRowTwo.append(
      contextWorkflowMiniButton("context-sync", "S", "Build selected project context sync ZIP", true),
      contextWorkflowMiniButton("import-pack", "Q+", "Import queue workflow pack", true),
    );
    miniStack.append(miniRow, miniRowTwo);
    panel.appendChild(miniStack);
  }

  if (contextWorkflowPanelExpanded) {
    const projectPicker = document.createElement("div");
    const select = renderContextWorkflowProjectSelect(selectedPaths);
    const pickerLabel = document.createElement("div");
    const pickerHint = document.createElement("div");
    projectPicker.className = "ion-context-rail-project-picker";
    pickerLabel.className = "ion-context-rail-project-picker-label";
    pickerLabel.textContent = "Projects for sync";
    pickerHint.className = "ion-context-rail-project-picker-label";
    pickerHint.textContent = "Selecting package(s) auto-builds the context sync ZIP.";
    projectPicker.append(pickerLabel, select, pickerHint);
    panel.appendChild(projectPicker);

    const list = document.createElement("div");
    list.className = "ion-context-rail-list";
    list.append(
      contextWorkflowLine("Gateway", browserQueueGatewayStatus.replace(/\s+/g, " ")),
      contextWorkflowLine("Projects", projectPackages.length ? `${projectPackages.length} found` : "not scanned"),
      contextWorkflowLine("Selected", selectedPaths.length ? selectedProject : "none"),
      contextWorkflowLine("Workflow", pendingQueueItems ? `${pendingQueueItems} queued` : contextWorkflowLastImportedPack),
    );
    panel.appendChild(list);

    const actions = document.createElement("div");
    actions.className = "ion-context-rail-actions";
    actions.append(
      contextWorkflowAction("context-pack", "Context", "Insert current ION context pack into composer", true),
      contextWorkflowAction("projects-refresh", "Projects", "Refresh project context package inventory"),
      contextWorkflowAction("context-sync", "Sync ZIP", "Build one context sync ZIP from selected projects", true),
      contextWorkflowAction("import-pack", "Import Q", "Import an ION queue workflow JSON or ZIP"),
      contextWorkflowAction("receipts", "Receipts", "Read recent bounded agent receipts"),
      contextWorkflowAction("queue-expand", "Queue", "Expand the right-side queue panel"),
    );
    panel.appendChild(actions);

    const foot = document.createElement("div");
    foot.className = "ion-context-rail-foot";
    foot.textContent = contextWorkflowRailStatus;
    panel.appendChild(foot);
  }
  panel.dataset.visible = "true";
}

function ensureContextWorkflowRail(): HTMLElement {
  ensureContextWorkflowRailStyle();
  let panel = document.getElementById(CONTEXT_WORKFLOW_PANEL_ID);
  if (!panel) {
    panel = document.createElement("div");
    panel.id = CONTEXT_WORKFLOW_PANEL_ID;
    panel.dataset.visible = "false";
    panel.addEventListener("click", (event) => {
      const source = event.target instanceof Element ? event.target.closest<HTMLElement>("[data-context-workflow-action]") : null;
      const action = source?.dataset.contextWorkflowAction ?? "";
      if (!action && panel?.dataset.expanded === "false") {
        contextWorkflowPanelExpanded = true;
        syncContextWorkflowRail();
        return;
      }
      if (action === "toggle-panel") {
        contextWorkflowPanelExpanded = !contextWorkflowPanelExpanded;
      } else if (action === "context-pack") {
        contextWorkflowRailStatus = "Requesting current ION context pack.";
        requestContextPack();
      } else if (action === "projects-refresh") {
        contextWorkflowRailStatus = "Scanning project context packages.";
        void requestProjectsRefresh().then(() => {
          contextWorkflowRailStatus = projectPackages.length ? `Projects ready: ${projectPackages.length} package(s).` : "No project context packages found.";
          syncContextWorkflowRail();
        });
      } else if (action === "context-sync") {
        const selectedPaths = contextWorkflowSelectedPaths();
        contextWorkflowRailStatus = selectedPaths.length
          ? `Requesting context sync ZIP for ${selectedPaths.length} project package(s).`
          : "Context sync blocked: select or refresh project packages first.";
        requestProjectContextSync(selectedPaths);
      } else if (action === "import-pack") {
        document.getElementById(CONTEXT_WORKFLOW_IMPORT_INPUT_ID)?.click();
      } else if (action === "receipts") {
        contextWorkflowRailStatus = "Reading recent bounded agent receipts.";
        window.dispatchEvent(new CustomEvent("ion-chatops-agent-receipts"));
      } else if (action === "queue-expand") {
        messageQueuePanelExpanded = true;
        syncComposerQueueChrome();
      }
      syncContextWorkflowRail();
    });
    panel.addEventListener("change", (event) => {
      const target = event.target;
      if (!(target instanceof HTMLSelectElement) || target.dataset.contextWorkflowAction !== "project-select") return;
      const selected = Array.from(target.selectedOptions).map((option) => option.value);
      scheduleAutoContextSync(selected);
      syncContextWorkflowRail();
    });
    document.documentElement.appendChild(panel);
  }
  let input = document.getElementById(CONTEXT_WORKFLOW_IMPORT_INPUT_ID) as HTMLInputElement | null;
  if (!input) {
    input = document.createElement("input");
    input.id = CONTEXT_WORKFLOW_IMPORT_INPUT_ID;
    input.type = "file";
    input.accept = ".zip,.json,application/json,application/zip";
    input.addEventListener("change", () => {
      const file = input?.files?.[0];
      if (!file) return;
      contextWorkflowRailStatus = `Importing queue workflow pack: ${file.name}`;
      syncContextWorkflowRail();
      void importBridgeQueuePackFile(file).then(() => {
        contextWorkflowLastImportedPack = file.name;
        contextWorkflowRailStatus = `Queue workflow import attempted: ${file.name}`;
        if (input) input.value = "";
        syncContextWorkflowRail();
      });
    });
    document.documentElement.appendChild(input);
  }
  return panel;
}

function contextWorkflowPanelWidth(anchorRect: DOMRect): number {
  const available = Math.floor(anchorRect.left - 16);
  if (contextWorkflowPanelExpanded) return Math.max(76, Math.min(276, available));
  return Math.max(54, Math.min(76, available));
}

function composerSidePanelBottom(anchorRect: DOMRect): number {
  return Math.max(8, Math.min(window.innerHeight - 72, window.innerHeight - anchorRect.bottom));
}

function syncContextWorkflowRail(anchorRect?: DOMRect): void {
  const input = findComposerInput();
  const panel = ensureContextWorkflowRail();
  if (!input || !visibleElement(input)) {
    panel.dataset.visible = "false";
    return;
  }
  let resolvedAnchor = anchorRect;
  if (!resolvedAnchor) {
    const containerRect = findComposerContainer(input).getBoundingClientRect();
    if (containerRect.bottom < window.innerHeight - 260) {
      resolvedAnchor = lastQueueChromeRect ?? containerRect;
    } else {
      resolvedAnchor = containerRect;
    }
  }
  const available = Math.floor(resolvedAnchor.left - 16);
  if (available < 54) {
    panel.dataset.visible = "false";
    return;
  }
  renderContextWorkflowRail(panel);
  const panelWidth = contextWorkflowPanelWidth(resolvedAnchor);
  const panelLeft = Math.max(8, resolvedAnchor.left - panelWidth - 8);
  const panelBottom = composerSidePanelBottom(resolvedAnchor);
  panel.style.width = `${panelWidth}px`;
  panel.style.left = `${panelLeft}px`;
  panel.style.top = "auto";
  panel.style.bottom = `${panelBottom}px`;
}

function pendingQueueLabel(visibleCount: number): string {
  if (messageQueuePaused) return "paused";
  if (messageQueueAutoPlay) return "auto";
  if (visibleCount) return `${visibleCount} item${visibleCount === 1 ? "" : "s"}`;
  return browserQueueGatewayStatus === "idle" ? "idle" : browserQueueGatewayStatus;
}

function messageQueueRightGutter(): number {
  const scrollbarWidth = Math.max(0, window.innerWidth - document.documentElement.clientWidth);
  return Math.max(MESSAGE_QUEUE_RIGHT_GUTTER_PX, scrollbarWidth + 10);
}

function messageQueueMiniPanelWidth(anchorRect: DOMRect, rightGutter: number): number {
  const available = Math.floor(window.innerWidth - rightGutter - anchorRect.right - 8);
  return Math.max(MESSAGE_QUEUE_PANEL_MINI_WIDTH_PX, Math.min(MESSAGE_QUEUE_PANEL_MINI_WIDTH_PX + 4, available));
}

function syncComposerQueueChrome(): void {
  startBrowserQueueCarrier();
  const input = findComposerInput();
  const chrome = ensureComposerQueueChrome();
  const pendingCount = messageQueueItems.filter((item) => item.status === "queued" || item.status === "waiting" || item.status === "sending" || item.status === "failed").length;
  chrome.button.dataset.count = String(pendingCount);
  chrome.button.textContent = pendingCount > 10 ? "Q+10+" : "Q+";
  chrome.sendNextButton.dataset.disabled = String(!pendingCount);
  if (!input || !visibleElement(input)) {
    chrome.button.style.display = "none";
    chrome.sendNextButton.style.display = "none";
    chrome.panel.dataset.visible = "false";
    syncContextWorkflowRail();
    syncLeftDockChrome();
    return;
  }
  const containerRect = findComposerContainer(input).getBoundingClientRect();
  if (containerRect.bottom < window.innerHeight - 260) {
    if (!lastQueueChromeRect) {
      chrome.button.style.display = "none";
      chrome.sendNextButton.style.display = "none";
      syncContextWorkflowRail();
      syncLeftDockChrome();
      return;
    }
  } else {
    lastQueueChromeRect = containerRect;
  }
  const anchorRect = lastQueueChromeRect ?? containerRect;
  const rightGutter = messageQueueRightGutter();
  chrome.button.style.display = "none";
  chrome.sendNextButton.style.display = "none";
  renderComposerQueuePanel(chrome.panel);
  const panelWidth = messageQueuePanelExpanded ? Math.min(280, window.innerWidth - rightGutter - 16) : messageQueueMiniPanelWidth(anchorRect, rightGutter);
  const panelLeft = Math.max(8, Math.min(window.innerWidth - panelWidth - rightGutter, anchorRect.right + 8));
  const panelBottom = composerSidePanelBottom(anchorRect);
  chrome.panel.style.width = `${panelWidth}px`;
  chrome.panel.style.left = `${panelLeft}px`;
  chrome.panel.style.top = "auto";
  chrome.panel.style.bottom = `${panelBottom}px`;
  syncContextWorkflowRail(anchorRect);
  syncLeftDockChrome();
}

function setComposerText(input: HTMLElement, text: string): void {
  input.focus();
  if (input instanceof HTMLTextAreaElement || input instanceof HTMLInputElement) {
    const descriptor = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(input), "value");
    descriptor?.set?.call(input, text);
    input.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText", data: text }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
    return;
  }
  const selection = window.getSelection();
  input.textContent = "";
  const range = document.createRange();
  range.selectNodeContents(input);
  range.collapse(false);
  selection?.removeAllRanges();
  selection?.addRange(range);
  document.execCommand("insertText", false, text);
  input.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText", data: text }));
}

function composerText(input: HTMLElement): string {
  if (input instanceof HTMLTextAreaElement || input instanceof HTMLInputElement) return input.value;
  const clone = input.cloneNode(true) as HTMLElement;
  clone.querySelectorAll("[data-placeholder], .placeholder").forEach((node) => node.remove());
  return (clone.innerText || clone.textContent || "").replace(/\u200b/g, "").trim();
}

function clearComposerText(input: HTMLElement): void {
  input.focus();
  if (input instanceof HTMLTextAreaElement || input instanceof HTMLInputElement) {
    const descriptor = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(input), "value");
    descriptor?.set?.call(input, "");
    input.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "deleteContentBackward", data: "" }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
    return;
  }
  const selection = window.getSelection();
  input.textContent = "";
  const range = document.createRange();
  range.selectNodeContents(input);
  range.collapse(false);
  selection?.removeAllRanges();
  selection?.addRange(range);
  input.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "deleteContentBackward", data: "" }));
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

async function waitForSendReadiness(timeoutMs = 2600): Promise<ReturnType<typeof chatReadiness>> {
  const started = Date.now();
  let readiness = chatReadiness();
  while ((!readiness.sendButton || !readiness.sendAvailable || (readiness.activeOutput && !messageQueueAllowMidOutput)) && Date.now() - started < timeoutMs) {
    await sleep(120);
    readiness = chatReadiness();
  }
  return readiness;
}

function latestAssistantText(): string {
  const selectors = [
    '[data-message-author-role="assistant"]',
    '[data-testid^="conversation-turn"] [data-message-author-role="assistant"]',
    "article",
  ];
  const candidates: HTMLElement[] = [];
  for (const selector of selectors) {
    for (const node of Array.from(document.querySelectorAll<HTMLElement>(selector))) {
      if (node.closest(`#${PANEL_ID}`) || node.closest(`#${MODAL_ID}`)) continue;
      const text = (node.innerText || node.textContent || "").replace(/\s+/g, " ").trim();
      if (text.length >= 8) candidates.push(node);
    }
    if (candidates.length) break;
  }
  const last = candidates[candidates.length - 1];
  return last ? (last.innerText || last.textContent || "").replace(/\n{3,}/g, "\n\n").trim() : "";
}

function extractStructuredBlocks(text: string): Array<Record<string, string>> {
  const blocks: Array<Record<string, string>> = [];
  const pattern = /```([A-Za-z0-9_-]+)?\n([\s\S]*?)```/g;
  let match: RegExpExecArray | null;
  while ((match = pattern.exec(text)) && blocks.length < 8) {
    blocks.push({ language: match[1] || "text", text: match[2].trim().slice(0, 20000) });
  }
  return blocks;
}

async function captureGatewayQueueResult(item: QueuedChatMessage): Promise<void> {
  if (!item.gateway) return;
  const started = Date.now();
  let sawOutput = chatReadiness().activeOutput;
  while (Date.now() - started < BROWSER_QUEUE_RESULT_TIMEOUT_MS) {
    await sleep(900);
    const readiness = chatReadiness();
    if (readiness.activeOutput) sawOutput = true;
    if (sawOutput && !readiness.activeOutput && readiness.sendAvailable) break;
  }
  const assistantText = latestAssistantText();
  const completed = Boolean(assistantText.trim());
  const response = await gatewayRequest("ion_chatops_browser_queue_result", {
    packet_id: item.gateway.packetId,
    lease_id: item.gateway.leaseId,
    carrier_id: item.gateway.carrierId,
    chat_url: window.location.href,
    status: completed ? "completed" : "blocked",
    blocked_reason: completed ? "" : "assistant_text_capture_empty_or_timed_out",
    assistant_text: assistantText,
    structured_blocks: extractStructuredBlocks(assistantText),
    captured_at: new Date().toISOString(),
  });
  item.status = "sent";
  item.detail = response?.ok
    ? `Gateway receipt: ${response.result?.gateway_receipt_path ?? "recorded"}`
    : `Gateway result blocked: ${blockedDetail(response?.result ?? response)}`;
  publishMessageQueueState(item.detail);
  syncComposerQueueChrome();
}

async function sendQueuedFileItem(item: QueuedChatMessage): Promise<boolean> {
  const files = messageQueueFilePayloads.get(item.id) ?? [];
  if (!files.length) {
    item.status = "failed";
    item.detail = "File payload missing. Re-add the file after page or extension reload.";
    publishMessageQueueState(item.detail);
    return false;
  }
  const target = findDropTarget();
  if (!target) {
    item.status = "waiting";
    item.detail = "Waiting: ChatGPT drop target not found. Preview or pick the drop zone in Settings.";
    publishMessageQueueState(item.detail);
    return false;
  }
  item.status = "sending";
  item.detail = "Attempting visible browser file drop. No Send click will be performed.";
  publishMessageQueueState("Dropping queued file item.");
  try {
    previewDropTarget();
    dispatchFilesToDropTarget(target, files);
    item.status = "sent";
    item.detail = `Drop attempted for ${files.length} file${files.length === 1 ? "" : "s"}. No Send click was performed.`;
    messageQueueFilePayloads.delete(item.id);
    publishMessageQueueState(item.detail);
    syncComposerQueueChrome();
    return true;
  } catch (error) {
    item.status = "failed";
    item.detail = `File drop failed: ${error instanceof Error ? error.message : String(error)}`;
    publishMessageQueueState(item.detail);
    syncComposerQueueChrome();
    return false;
  }
}

async function sendQueuedMessage(item: QueuedChatMessage): Promise<boolean> {
  if (item.kind === "files") return sendQueuedFileItem(item);
  const readiness = chatReadiness();
  if (!readiness.input) {
    item.status = "waiting";
    item.detail = "Waiting: composer input not found.";
    publishMessageQueueState(item.detail);
    return false;
  }
  const existingText = composerText(readiness.input).trim();
  if (existingText && existingText !== item.text.trim()) {
    item.status = "waiting";
    item.detail = "Waiting: composer contains manual unsent text.";
    publishMessageQueueState(item.detail);
    return false;
  }
  if (readiness.activeOutput && !messageQueueAllowMidOutput) {
    item.status = "waiting";
    item.detail = "Waiting: assistant is still outputting.";
    publishMessageQueueState(item.detail);
    return false;
  }
  if (!readiness.sendAvailable || !readiness.sendButton) {
    item.status = "waiting";
    item.detail = "Waiting: send button is not available.";
    publishMessageQueueState(item.detail);
    return false;
  }
  item.status = "sending";
  item.detail = "Pasting into ChatGPT composer.";
  publishMessageQueueState("Sending queued message.");
  setComposerText(readiness.input, item.text);
  await sleep(MESSAGE_QUEUE_SEND_SETTLE_MS);
  const afterPaste = await waitForSendReadiness();
  if (!afterPaste.sendButton || !afterPaste.sendAvailable) {
    item.status = "waiting";
    item.detail = `Message pasted, waiting for send button to unlock. Last readiness: ${afterPaste.reason}.`;
    publishMessageQueueState(item.detail);
    return false;
  }
  afterPaste.sendButton.click();
  item.status = item.gateway ? "sending" : "sent";
  item.detail = item.gateway ? "Sent; waiting for assistant output receipt." : `Sent at ${new Date().toLocaleTimeString()}.`;
  publishMessageQueueState("Queued message sent.");
  if (item.gateway) void captureGatewayQueueResult(item);
  return true;
}

async function processMessageQueue(reason = "tick", force = false, autoOnly = false): Promise<void> {
  void reason;
  if (messageQueueProcessing) return;
  if (messageQueuePaused && !force) {
    publishMessageQueueState();
    return;
  }
  const item = nextQueuedMessage(autoOnly);
  if (!item) {
    publishMessageQueueState();
    return;
  }
  messageQueueProcessing = true;
  try {
    await sendQueuedMessage(item);
  } catch (error) {
    item.status = "failed";
    item.detail = `Send failed: ${error instanceof Error ? error.message : String(error)}`;
    publishMessageQueueState(item.detail);
  } finally {
    messageQueueProcessing = false;
  }
}

function startMessageQueueEngine(): void {
  if (messageQueueStarted) return;
  messageQueueStarted = true;
  window.setInterval(() => {
    updateQueueReadinessState();
    publishMessageQueueState();
    syncComposerQueueChrome();
  }, MESSAGE_QUEUE_TICK_MS);
  publishMessageQueueState();
  syncComposerQueueChrome();
}

function percentOf(value: number, reference: number): number {
  if (!Number.isFinite(value) || value <= 0) return 0;
  return Math.min(999, Math.round((value / reference) * 100));
}

function estimateVisibleChatPressure(): { chars: number; estimatedTokens: number; messageCount: number; assistantMessageCount: number; userMessageCount: number } {
  const candidates = Array.from(
    document.querySelectorAll<HTMLElement>('[data-message-author-role], [data-testid^="conversation-turn"], article'),
  );
  const seenText = new Set<string>();
  let chars = 0;
  let messageCount = 0;
  let assistantMessageCount = 0;
  let userMessageCount = 0;
  for (const node of candidates) {
    if (node.closest(`#${PANEL_ID}`) || node.closest(`#${MODAL_ID}`)) continue;
    const text = (node.innerText || node.textContent || "").replace(/\s+/g, " ").trim();
    if (text.length < 8) continue;
    const fingerprint = `${text.length}:${text.slice(0, 120)}`;
    if (seenText.has(fingerprint)) continue;
    seenText.add(fingerprint);
    chars += Math.min(text.length, 180000);
    messageCount += 1;
    const role = node.getAttribute("data-message-author-role") || node.closest<HTMLElement>("[data-message-author-role]")?.getAttribute("data-message-author-role") || "";
    if (role === "assistant") assistantMessageCount += 1;
    if (role === "user") userMessageCount += 1;
  }
  return {
    chars,
    estimatedTokens: Math.ceil(chars / 4),
    messageCount,
    assistantMessageCount,
    userMessageCount,
  };
}

function browserPressureGuidance(percent32k: number, lagMs: number, domNodes: number): string[] {
  const guidance: string[] = [];
  if (percent32k >= CHAT_CONTEXT_WATCH_PERCENT) {
    guidance.push("Loaded transcript is large. If responses drift or the browser lags, start a fresh chat or move durable context into Docs/packages.");
  }
  if (lagMs >= EVENT_LOOP_WATCH_MS) {
    guidance.push("Browser main thread is lagging; avoid opening huge drawers, uploading very large folders, or rescanning repeatedly.");
  }
  if (domNodes >= DOM_WATCH_NODES) {
    guidance.push("ChatGPT page DOM is heavy; reload or start a shorter chat if hover/click response gets slow.");
  }
  if (!guidance.length) guidance.push("No pressure warning. Continue normally.");
  return guidance;
}

function refreshBrowserPressureMonitor(): void {
  const chat = estimateVisibleChatPressure();
  const domNodes = document.getElementsByTagName("*").length;
  const lagMs = Math.max(latestEventLoopLagMs, latestLongTaskMs);
  const percent32k = percentOf(chat.estimatedTokens, CHAT_CONTEXT_REFERENCE_32K);
  const percent128k = percentOf(chat.estimatedTokens, CHAT_CONTEXT_REFERENCE_128K);
  const percent256k = percentOf(chat.estimatedTokens, CHAT_CONTEXT_REFERENCE_256K);
  const percent16k = percentOf(chat.estimatedTokens, CHAT_CONTEXT_REFERENCE_16K);
  const percent400k = percentOf(chat.estimatedTokens, CHAT_CONTEXT_REFERENCE_400K);
  const blocked =
    percent32k >= CHAT_CONTEXT_BLOCKED_PERCENT ||
    lagMs >= EVENT_LOOP_BLOCKED_MS ||
    domNodes >= DOM_BLOCKED_NODES;
  const watch =
    blocked ||
    percent32k >= CHAT_CONTEXT_WATCH_PERCENT ||
    lagMs >= EVENT_LOOP_WATCH_MS ||
    domNodes >= DOM_WATCH_NODES;
  const tone = blocked ? "blocked" : watch ? "watch" : "ready";
  const guidance = browserPressureGuidance(percent32k, lagMs, domNodes);
  setBridgeMonitorMetrics({
    estimatedTokens: chat.estimatedTokens,
    plusPercent: percent32k,
    proPercent: percent128k,
    thinkingPercent: percent256k,
    messageCount: chat.messageCount,
    assistantMessageCount: chat.assistantMessageCount,
    userMessageCount: chat.userMessageCount,
    domNodes,
    lagMs: Math.round(latestEventLoopLagMs),
    longTaskMs: Math.round(latestLongTaskMs),
    tone,
    summary: `Loaded transcript ${chat.estimatedTokens.toLocaleString()} est tokens · lag ${Math.round(lagMs)}ms · DOM ${domNodes}`,
    detail: [
      "ChatGPT browser pressure diagnostics",
      "",
      "Important: loaded browser transcript size is not the same thing as active model context.",
      "ChatGPT uses rolling/managed context. Older turns may be summarized, dropped, selectively retrieved, or otherwise transformed server-side. This extension cannot see that private active context window.",
      "This monitor only estimates text currently loaded in the page DOM, using about 4 characters per token. Treat the GPT-5.5 tier percentages as rough browser/transcript pressure markers, not exact remaining context.",
      "",
      "GPT-5.5 ChatGPT context references:",
      `instant_free_16k: ${percent16k}%`,
      `instant_plus_business_32k: ${percent32k}%`,
      `instant_pro_enterprise_128k: ${percent128k}%`,
      `thinking_paid_256k: ${percent256k}%`,
      `thinking_pro_400k: ${percent400k}%`,
      "",
      `visible_messages: ${chat.messageCount}`,
      `visible_assistant_messages: ${chat.assistantMessageCount}`,
      `visible_user_messages: ${chat.userMessageCount}`,
      `visible_characters: ${chat.chars.toLocaleString()}`,
      `estimated_visible_tokens: ${chat.estimatedTokens.toLocaleString()}`,
      `event_loop_lag_ms: ${Math.round(latestEventLoopLagMs)}`,
      `latest_long_task_ms: ${Math.round(latestLongTaskMs)}`,
      `dom_elements: ${domNodes.toLocaleString()}`,
      "",
      "What to do:",
      ...guidance.map((item) => `- ${item}`),
    ].join("\n"),
  });
}

function startBrowserPressureMonitor(): void {
  if (browserPressureStarted) return;
  browserPressureStarted = true;
  nextLagProbeAt = performance.now() + BROWSER_PRESSURE_INTERVAL_MS;
  window.setInterval(() => {
    const now = performance.now();
    latestEventLoopLagMs = Math.max(0, now - nextLagProbeAt);
    latestLongTaskMs = Math.max(0, latestLongTaskMs * 0.72);
    nextLagProbeAt = now + BROWSER_PRESSURE_INTERVAL_MS;
    refreshBrowserPressureMonitor();
  }, BROWSER_PRESSURE_INTERVAL_MS);
  try {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        latestLongTaskMs = Math.max(latestLongTaskMs, entry.duration);
      }
      refreshBrowserPressureMonitor();
    });
    observer.observe({ entryTypes: ["longtask"] });
  } catch {
    // Some browsers do not expose Long Tasks to extension content scripts.
  }
  refreshBrowserPressureMonitor();
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
    refreshBrowserPressureMonitor();
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
          `queue_target: ${result.queue_target ?? result.queue_path ?? result.verdict ?? ""}`,
          `status: ${result.verdict ?? ""}`
        ].join("\n");
        await copyReceiptSummary(summary);
        setBridgeStatus("ION action submitted", summary, "success");
      });
    }
    clearAssetCaptureButtons();
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
        element.closest(`#${DOM_REGISTRY_POPOVER_ID}`) ||
        element.closest(`.${ASSET_CAPTURE_BUTTON_CLASS}`) ||
        element.closest(`#${CAPTURE_FRAME_ID}`) ||
        element.closest(`#${MESSAGE_QUEUE_BUTTON_ID}`) ||
        element.closest(`#${MESSAGE_QUEUE_SEND_NEXT_BUTTON_ID}`) ||
        element.closest(`#${MESSAGE_QUEUE_PANEL_ID}`) ||
        element.closest(`#${MESSAGE_QUEUE_FILE_INPUT_ID}`) ||
        element.closest(`#${CHATGPT_LEFT_ICON_DOCK_ID}`) ||
        element.closest(`#${CONTEXT_WORKFLOW_PANEL_ID}`) ||
        element.closest(`#${CONTEXT_WORKFLOW_IMPORT_INPUT_ID}`) ||
        element.id === PANEL_ID ||
        element.id === MODAL_ID ||
        element.id === DOM_REGISTRY_STYLE_ID ||
        element.id === DOM_REGISTRY_POPOVER_ID ||
        element.id === ASSET_CAPTURE_STYLE_ID ||
        element.id === CAPTURE_FRAME_ID ||
        element.id === MESSAGE_QUEUE_BUTTON_ID ||
        element.id === MESSAGE_QUEUE_SEND_NEXT_BUTTON_ID ||
        element.id === MESSAGE_QUEUE_PANEL_ID ||
        element.id === MESSAGE_QUEUE_CHROME_STYLE_ID ||
        element.id === CHATGPT_LEFT_ICON_DOCK_ID ||
        element.id === CHATGPT_LEFT_ICON_DOCK_STYLE_ID ||
        element.id === MESSAGE_QUEUE_FILE_INPUT_ID ||
        element.id === CONTEXT_WORKFLOW_PANEL_ID ||
        element.id === CONTEXT_WORKFLOW_STYLE_ID ||
        element.id === CONTEXT_WORKFLOW_IMPORT_INPUT_ID ||
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
  settingsInspectorTarget = "tabs_anchor";
  settingsAnchorPoint = anchorForTarget("tabs_anchor");
  startBrowserPressureMonitor();
  startMessageQueueEngine();
  const observerRoot = document.body ?? document.documentElement;
  const observer = new MutationObserver((mutations) => {
    if (mutations.length && mutations.every(mutationTouchesIonUi)) return;
    scheduleScan("auto");
    tryAutoAcceptNativeAction();
  });
  observer.observe(observerRoot, { childList: true, subtree: true });
  window.addEventListener("resize", () => refreshBridgePosition());
  window.addEventListener("scroll", () => scheduleScan("auto"), { capture: true, passive: true });
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
  isIonActionPacketCandidateText,
  candidateBlocks,
  updateDomActionRegistry,
  submitActionText,
  refreshBridgePosition,
  previewAttachTarget,
  previewDropTarget,
  findDropTarget,
  localAttachPayload,
  requestArtifactLocalAttachDryRun,
  beginDomInspector,
  previewInspectorSelectedLayer,
  saveInspectorSelectedLayer,
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
window.addEventListener("ion-chatops-codex-refresh", () => {
  requestCodexChatModel();
});
window.addEventListener("ion-chatops-codex-send", (event) => {
  const detail = (event as CustomEvent<{ message?: string }>).detail ?? {};
  requestCodexChatTurn(detail.message ?? "");
});
window.addEventListener("ion-chatops-codex-queue", (event) => {
  const detail = (event as CustomEvent<{ message?: string }>).detail ?? {};
  requestCodexChatQueue(detail.message ?? "");
});

window.addEventListener("ion-chatops-bounded-agent-status", () => {
  requestBoundedAgentRead("ion_chatops_bounded_agent_status", "Bounded agent lane");
});

window.addEventListener("ion-chatops-agent-relays", () => {
  requestBoundedAgentRead("ion_chatops_agent_relay_pending", "Agent relay inbox");
});

window.addEventListener("ion-chatops-agent-receipts", () => {
  requestBoundedAgentRead("ion_chatops_agent_receipts_recent", "Agent receipts");
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
window.addEventListener("ion-chatops-gateway-auto-accept-toggle", () => {
  const operation = browserQueueAutoAcceptActive ? "auto_accept_off" : "auto_accept_on";
  browserQueueAutoAcceptActive = operation === "auto_accept_on";
  browserQueueGatewayStatus = browserQueueAutoAcceptActive
    ? "Auto-accept on for safe ION actions; watching for ChatGPT confirmation cards."
    : "Auto-accept off.";
  publishMessageQueueState();
  tryAutoAcceptNativeAction();
  void gatewayRequest("ion_chatops_browser_queue_control", { operation, ttl_seconds: browserQueueAutoAcceptTtlSeconds }).then(() => pollBrowserQueueCarrier());
});
window.addEventListener("ion-chatops-gateway-auto-accept-settings", (event) => {
  const detail = (event as CustomEvent<{ ttl_seconds?: number }>).detail;
  if (typeof detail?.ttl_seconds === "number") {
    browserQueueAutoAcceptTtlSeconds = detail.ttl_seconds;
    publishMessageQueueState();
    if (browserQueueAutoAcceptActive) {
      void gatewayRequest("ion_chatops_browser_queue_control", { operation: "auto_accept_on", ttl_seconds: browserQueueAutoAcceptTtlSeconds }).then(() => pollBrowserQueueCarrier());
    }
  }
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
window.addEventListener("ion-chatops-artifact-preview-attach", () => {
  previewAttachTarget();
});
window.addEventListener("ion-chatops-artifact-preview-drop", () => {
  previewDropTarget();
});
window.addEventListener("ion-chatops-artifact-dry-run-attach", () => {
  requestArtifactLocalAttachDryRun();
});
window.addEventListener("ion-chatops-artifact-local-attach", () => {
  requestArtifactLocalAttachLatest();
});
window.addEventListener("ion-chatops-docs-open-root", (event) => {
  requestDocsOpenRoot(event as CustomEvent<{ path?: string }>);
});
window.addEventListener("ion-chatops-docs-open-folder", (event) => {
  const detail = (event as CustomEvent<{ path?: string; query?: string }>).detail ?? {};
  requestDocsOpenFolder({
    path: detail.path ?? "",
    query: detail.query,
  });
});
window.addEventListener("ion-chatops-docs-open-parent", () => {
  requestDocsOpenParent();
});
window.addEventListener("ion-chatops-docs-open-doc", (event) => {
  const detail = (event as CustomEvent<{ path?: string; name?: string }>).detail ?? {};
  requestDocsOpenDoc(detail.path ?? "", detail.name ?? "");
});
window.addEventListener("ion-chatops-docs-search", (event) => {
  const detail = (event as CustomEvent<{ query?: string }>).detail ?? {};
  requestDocsSearch(detail.query ?? "");
});
window.addEventListener("ion-chatops-docs-drag-doc", (event) => {
  const detail = (event as CustomEvent<{ path?: string }>).detail ?? {};
  requestDocsDrop(detail.path ?? "");
});
window.addEventListener("ion-chatops-projects-refresh", () => {
  void requestProjectsRefresh();
});
window.addEventListener("ion-chatops-projects-drop", (event) => {
  const detail = (event as CustomEvent<{ path?: string }>).detail ?? {};
  requestProjectDrop(detail.path ?? "");
});
window.addEventListener("ion-chatops-project-context-sync", (event) => {
  const detail = (event as CustomEvent<{ paths?: string[] }>).detail ?? {};
  requestProjectContextSync(Array.isArray(detail.paths) ? detail.paths : []);
});
window.addEventListener("ion-chatops-settings-pick-attach", () => {
  beginAttachTargetPicker();
});
window.addEventListener("ion-chatops-settings-frame-capture", () => {
  startCaptureFrame();
});
window.addEventListener("ion-chatops-settings-frame-save", () => {
  captureActiveFrameElement();
});
window.addEventListener("ion-chatops-settings-frame-load", () => {
  loadCaptureFrame();
});
window.addEventListener("ion-chatops-settings-frame-delete", () => {
  deleteCaptureFrame();
});
window.addEventListener("ion-chatops-settings-clear-attach", () => {
  clearAttachTargetCalibration();
});
window.addEventListener("ion-chatops-settings-pick-drop", () => {
  beginDropTargetPicker();
});
window.addEventListener("ion-chatops-settings-clear-drop", () => {
  clearDropTargetCalibration();
});
window.addEventListener("ion-chatops-settings-pick-tabs-anchor", () => {
  beginTabsAnchorPicker();
});
window.addEventListener("ion-chatops-settings-clear-tabs-anchor", () => {
  clearTabsAnchorCalibration();
});
window.addEventListener("ion-chatops-settings-inspector-start", () => {
  const panel = document.getElementById(PANEL_ID);
  const settingsMode = panel?.dataset.expanded === "true" && panel?.dataset.tab === "settings";
  beginDomInspector(settingsMode);
});
window.addEventListener("ion-chatops-settings-inspector-cancel", () => {
  stopDomInspector("dom_inspector_cancelled\nInspector was cancelled from Settings.");
  setBridgeStatus("Inspector cancelled", "No anchor changed.", "idle");
});
window.addEventListener("ion-chatops-settings-inspector-mode", (event) => {
  const detail = (event as CustomEvent<{ enabled?: boolean }>).detail;
  setSettingsInspectorMode(Boolean(detail?.enabled));
});
window.addEventListener("ion-chatops-settings-anchor-target", (event) => {
  const detail = (event as CustomEvent<{ target?: InspectorSaveTarget }>).detail;
  if (detail?.target === "tabs_anchor" || detail.target === "drop_zone" || detail.target === "attach_target") {
    setInspectorAnchorTarget(detail.target);
    setBridgeSettingsDetail([
      "dom_inspector_target_selected",
      `target: ${detail.target}`,
      `anchor: ${settingsAnchorPoint}`,
    ].join("\n"));
    refreshSettingsInspectorPreview();
  }
});
window.addEventListener("ion-chatops-settings-anchor-point", (event) => {
  const detail = (event as CustomEvent<{ anchor?: string }>).detail;
  const anchor = detail?.anchor;
  if (anchor === "top" || anchor === "left" || anchor === "center" || anchor === "right" || anchor === "bottom") {
    settingsAnchorPoint = anchor;
    setBridgeSettingsDetail([
      "dom_inspector_anchor_point_selected",
      `target: ${settingsInspectorTarget}`,
      `anchor: ${settingsAnchorPoint}`,
    ].join("\n"));
    refreshSettingsInspectorPreview();
  }
});
window.addEventListener("ion-chatops-settings-inspector-preview", () => {
  previewInspectorSelectedLayer();
});
window.addEventListener("ion-chatops-settings-inspector-layer", (event) => {
  const detail = (event as CustomEvent<{ index?: number }>).detail;
  const index = Number(detail?.index ?? 0);
  if (document.getElementById(CAPTURE_FRAME_ID) && captureFrameLayers.length) {
    captureFrameLayerIndex = Math.max(0, Math.min(index, captureFrameLayers.length - 1));
    applyCaptureFrameLayer(captureFrameLayerIndex, true);
  }
  selectInspectorLayer(index);
});
window.addEventListener("ion-chatops-settings-inspector-save", (event) => {
  const detail = (event as CustomEvent<{ target?: InspectorSaveTarget }>).detail;
  const target = detail?.target;
  if (target === "tabs_anchor" || target === "drop_zone" || target === "attach_target") {
    saveInspectorSelectedLayer(target);
  }
});
window.addEventListener("ion-chatops-message-queue-add", (event) => {
  const detail = (event as CustomEvent<{ text?: string; messages?: string[]; status?: string; source?: string }>).detail;
  if (Array.isArray(detail?.messages) && detail.messages.length) {
    addQueuedMessageBatch(detail.messages, detail.status, detail.source === "pack" ? "pack" : "manual");
    return;
  }
  const text = String(detail?.text ?? "").trim();
  if (text) addQueuedMessages(text);
});
window.addEventListener("ion-chatops-message-queue-pause", (event) => {
  const detail = (event as CustomEvent<{ paused?: boolean }>).detail;
  messageQueuePaused = Boolean(detail?.paused);
  publishMessageQueueState(messageQueuePaused ? "Queue paused." : "Queue resumed.");
});
window.addEventListener("ion-chatops-message-queue-send-next", () => {
  void processMessageQueue("manual");
});
window.addEventListener("ion-chatops-message-queue-clear", (event) => {
  const detail = (event as CustomEvent<{ mode?: string }>).detail;
  if (detail?.mode === "sent") {
    messageQueueItems = messageQueueItems.filter((item) => item.status !== "sent");
    messageQueueFilePayloads = new Map(messageQueueItems.map((item) => [item.id, messageQueueFilePayloads.get(item.id) ?? []]).filter((entry): entry is [string, File[]] => entry[1].length > 0));
    publishMessageQueueState("Sent messages cleared.");
    return;
  }
  messageQueueItems = [];
  messageQueueFilePayloads.clear();
  publishMessageQueueState("Queue cleared.");
});
window.addEventListener("ion-chatops-message-queue-mid-output", (event) => {
  const detail = (event as CustomEvent<{ allow?: boolean }>).detail;
  messageQueueAllowMidOutput = Boolean(detail?.allow);
  publishMessageQueueState(messageQueueAllowMidOutput ? "Mid-output sending allowed when ChatGPT exposes Send." : "Mid-output sending disabled. Queue waits for output to stop.");
});
window.addEventListener("ion-chatops-prompt-insert", (event) => {
  const detail = (event as CustomEvent<{ text?: string; mode?: string }>).detail ?? {};
  const text = String(detail.text ?? "").trim();
  if (!text) return;
  const input = findComposerInput();
  if (!input) {
    setBridgeStatus("Prompt insert blocked", "ChatGPT composer input was not found.", "error");
    return;
  }
  const existing = composerText(input).trim();
  const nextText = detail.mode === "append" && existing ? `${existing}\n\n${text}` : text;
  setComposerText(input, nextText);
  setBridgeStatus("Prompt inserted", detail.mode === "append" ? "Prompt appended to composer." : "Prompt placed in composer.", "success");
});

if (safeModeDisabled()) {
  console.info(`ION ChatOps Bridge disabled by ${SAFE_MODE_KEY}. Remove the flag and reload to re-enable.`);
} else {
  setBridgeDocsState(docsState);
  initializeBridge();
}
