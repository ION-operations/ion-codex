import type { IonActionPacket, ValidationResult } from "./schema";

type BridgeTone = "idle" | "working" | "approval" | "success" | "error";

const PANEL_ID = "ion-chatops-bridge-panel";
const MODAL_ID = "ion-chatops-bridge-approval";
const STYLE_ID = "ion-chatops-bridge-style";
const SETTINGS_CONTROL_PAD_ID = "ion-chatops-settings-control-pad";
const LOG_LIMIT = 12;
const TOP_BAR_GAP = 8;
const PANEL_TOP = 2;
const DEFAULT_LEFT_BOUNDARY = 50;
const DEFAULT_RIGHT_RESERVE = 250;
const PANEL_PREFERRED_WIDTH = 640;
const PANEL_MIN_WIDTH = 320;
const PANEL_TINY_WIDTH = 230;
const COMPOSER_PANEL_MAX_WIDTH = 920;
const ATTACH_TARGET_SELECTOR_KEY = "ION_CHATOPS_ATTACH_TARGET_SELECTOR";
const DROP_TARGET_SELECTOR_KEY = "ION_CHATOPS_DROP_TARGET_SELECTOR";
const TABS_ANCHOR_SELECTOR_KEY = "ION_CHATOPS_TABS_ANCHOR_SELECTOR";
const TAB_LIFT_KEY = "ION_CHATOPS_TAB_LIFT_PX";
const DRAWER_MAX_KEY = "ION_CHATOPS_DRAWER_MAX_PX";
const LAYOUT_TARGET_KEY = "ION_CHATOPS_LAYOUT_TARGET";
const TOP_RAIL_X_KEY = "ION_CHATOPS_TOP_RAIL_X_PX";
const TOP_RAIL_Y_KEY = "ION_CHATOPS_TOP_RAIL_Y_PX";
const TABS_X_KEY = "ION_CHATOPS_TABS_X_PX";
const TABS_Y_KEY = "ION_CHATOPS_TABS_Y_PX";
const DRAWER_X_KEY = "ION_CHATOPS_DRAWER_X_PX";
const DRAWER_Y_KEY = "ION_CHATOPS_DRAWER_Y_PX";
const TAB_LABEL_MIN_WIDTH = 780;
const TAB_HEIGHT = 22;
const ONBOARD_PROJECT_NAME = "ION";
const ONBOARD_BRIDGE_NAME = "ION ChatOps Bridge";
const ONBOARD_PROTOCOL_ID = "ION_CONTEXT_ONBOARD_PROTOCOL_V1";
const ONBOARD_PROTOCOL_VERSION = "0.1.0";
const ONBOARD_SYNC_KEY = "ION_CHATOPS_ONBOARD_PROTOCOL_SYNC";
const MODE_MEMORY_KEY = "ION_CHATOPS_MODE_MEMORY_V1";
const PROMPT_LIBRARY_KEY = "ION_CHATOPS_PROMPT_LIBRARY_V1";
const QUEUE_PACK_SCHEMA_ID = "ion.extension.queue_pack.v1";
const QUEUE_PACK_MANIFEST_NAME = "ion_queue_pack.json";
const QUEUE_PACK_MAX_MESSAGES = 120;
const QUEUE_PACK_MAX_PROMPT_CHARS = 24000;
const QUEUE_PACK_MAX_TEXT_ENTRY_BYTES = 1024 * 1024;

type LayoutTarget = "top_rail" | "tabs" | "drawer";
type AnchorPoint = "top" | "left" | "center" | "right" | "bottom";
type SettingsAnchorTarget = "tabs_anchor" | "drop_zone" | "attach_target";
type BridgeOperationalMode =
  | "IDLE_MONITORING"
  | "DETECTED"
  | "APPROVAL_REQUIRED"
  | "APPROVAL_MODAL"
  | "SUBMITTING"
  | "RECEIPTED"
  | "ERROR_BLOCKED"
  | "INSPECTOR_CALIBRATION";
type OnboardSyncInfo = {
  project: string;
  bridge: string;
  protocolId: string;
  version: string;
  state: "ready" | "synced";
  detail: string;
  lastSyncedAt: string;
};
type TargetMetaInfo = {
  selector: string;
  anchor: AnchorPoint;
};

type ModeMemoryState = {
  currentMode: BridgeOperationalMode;
  lastMode: BridgeOperationalMode;
  lastActionId: string;
  lastIntent: string;
  lastReceiptPath: string;
  lastQueueTarget: string;
  lastStatusTitle: string;
  lastDetail: string;
  lastUpdatedAt: string;
};

type InspectorLayerOption = {
  index: number;
  label: string;
  selector: string;
};

type DocsBrowserEntry = {
  kind: "folder" | "file";
  name: string;
  path: string;
  size_bytes?: number;
  thumbnail?: string;
};

type DocsBrowserState = {
  roots: string[];
  currentRoot: string;
  currentPath: string;
  query: string;
  breadcrumbs: string[];
  entries: DocsBrowserEntry[];
  selectedPath: string;
  status: string;
  selectedDocName: string;
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

type ProjectsState = {
  status: string;
  roots: string[];
  packages: ProjectPackageEntry[];
  selectedPath: string;
  selectedPaths: string[];
  contextSyncOpen: boolean;
  contextSyncStatus: string;
  contextSyncZipPath: string;
  contextSyncSha256: string;
};

type CodexChatTurn = {
  turn_id?: string;
  author?: string;
  kind?: string;
  message?: string;
  created_at?: string;
  chat_engine?: Record<string, unknown>;
  context_refs?: string[];
  skill_activation?: Record<string, unknown>;
  codex_model_move?: Record<string, unknown>;
};

type CodexChatView = "history" | "capsule" | "mini" | "context" | "queue";

type CodexChatState = {
  status: string;
  input: string;
  turns: CodexChatTurn[];
  view: CodexChatView;
  model?: Record<string, unknown> | null;
  submitting: boolean;
  queueing: boolean;
};

type MessageQueueItem = {
  id: string;
  kind?: "text" | "files";
  text: string;
  status: "queued" | "waiting" | "sending" | "sent" | "failed";
  createdAt: string;
  detail?: string;
};

type MessageQueueState = {
  input: string;
  status: string;
  paused: boolean;
  allowMidOutput: boolean;
  activeOutput: boolean;
  sendAvailable: boolean;
  autoAcceptActive: boolean;
  autoAcceptUntil: string;
  autoAcceptTtlSeconds: number;
  items: MessageQueueItem[];
};

type PromptLibraryItem = {
  id: string;
  title: string;
  category: string;
  tags: string[];
  text: string;
  pinned: boolean;
  updatedAt: string;
  usageCount: number;
  origin: "built_in" | "custom";
};

type PromptLibraryState = {
  status: string;
  query: string;
  category: string;
  selectedId: string;
  draftTitle: string;
  draftCategory: string;
  draftTags: string;
  draftText: string;
  items: PromptLibraryItem[];
};

type QueuePackStep = {
  id?: string;
  title?: string;
  prompt?: string;
  text?: string;
  prompt_ref?: string;
  tags?: string[];
};

type QueuePackChain = {
  id?: string;
  title?: string;
  objective?: string;
  steps?: QueuePackStep[];
};

type QueuePackWorkflow = {
  id?: string;
  title?: string;
  objective?: string;
  chains?: QueuePackChain[];
  steps?: QueuePackStep[];
};

type QueuePackManifest = {
  schema_id?: string;
  pack_id?: string;
  title?: string;
  objective?: string;
  queue_behavior?: {
    manual_start_required?: boolean;
    auto_play_requested?: boolean;
    include_step_headers?: boolean;
  };
  workflows?: QueuePackWorkflow[];
  chains?: QueuePackChain[];
  steps?: QueuePackStep[];
  prompts?: QueuePackStep[];
  queue?: QueuePackStep[];
};

type QueuePackImportResult = {
  pack: QueuePackManifest;
  messages: string[];
  status: string;
};

type MonitorMetrics = {
  estimatedTokens: number;
  plusPercent: number;
  proPercent: number;
  thinkingPercent: number;
  messageCount: number;
  assistantMessageCount: number;
  userMessageCount: number;
  actionCandidateCount: number;
  validActionCount: number;
  blockedActionCount: number;
  duplicateActionCount: number;
  codeBlockCount: number;
  composerControlCount: number;
  selectedSourceCount: number;
  uploadedAttachmentCount: number;
  domNodes: number;
  lagMs: number;
  longTaskMs: number;
  tone: "ready" | "watch" | "blocked";
  summary: string;
  detail: string;
};

type AnchorInfo = {
  mode: "composer" | "topbar_fallback";
  rect: DOMRect | null;
  element?: HTMLElement | null;
  health: "ready" | "degraded";
  detail: string;
  source?: string;
  attachmentsDetected?: number;
};

type DocsFavoriteRoot = {
  path: string;
  label: string;
  icon: string;
  accent: string;
  status?: string;
};

let docsFavoriteRoots: DocsFavoriteRoot[] = [
  { path: "ION", label: "ION", icon: "🧱", accent: "#38bdf8" },
  { path: "dAimon_ION", label: "Daimon", icon: "🧠", accent: "#a78bfa" },
  { path: "ION/02_architecture", label: "Architecture", icon: "🧩", accent: "#60a5fa" },
  { path: "ION/03_registry", label: "Registry", icon: "🗂️", accent: "#f472b6" },
  { path: "ION/05_context", label: "Context", icon: "🧾", accent: "#34d399" },
  { path: "ION/06_artifacts", label: "Artifacts", icon: "📦", accent: "#fb923c" },
  { path: "ION/09_integrations", label: "Integrations", icon: "🔌", accent: "#f97316" },
];

const DOCS_TREE_OPTIONS = [
  { value: "", label: "🏠 File system home", group: "Quick Root" },
  { value: "ION", label: "ION", group: "Workspace" },
  { value: "dAimon_ION", label: "Daimon", group: "Workspace" },
  { value: "ION/02_architecture", label: "Architecture", group: "Workspace" },
  { value: "ION/03_registry", label: "Registry", group: "Workspace" },
  { value: "ION/05_context", label: "Context", group: "Workspace" },
  { value: "ION/06_artifacts", label: "Artifacts", group: "Workspace" },
  { value: "ION/06_artifacts/packages", label: "Artifacts/packages", group: "Workspace" },
  { value: "ION/09_integrations", label: "Integrations", group: "Workspace" },
  { value: "ION/09_integrations/browser_extension", label: "Browser extensions", group: "Workspace" },
  { value: "ION/09_integrations/browser_extension/ion_chatops_bridge", label: "ChatOps bridge", group: "Workspace" },
];

function readOnboardSyncState(): OnboardSyncInfo {
  const base: OnboardSyncInfo = {
    project: ONBOARD_PROJECT_NAME,
    bridge: ONBOARD_BRIDGE_NAME,
    protocolId: ONBOARD_PROTOCOL_ID,
    version: ONBOARD_PROTOCOL_VERSION,
    state: "ready",
    detail: `Ready to sync ${ONBOARD_PROJECT_NAME} context protocol ${ONBOARD_PROTOCOL_VERSION}.`,
    lastSyncedAt: "",
  };
  try {
    const stored = JSON.parse(window.localStorage?.getItem(ONBOARD_SYNC_KEY) ?? "{}") as Record<string, unknown>;
    if (
      stored.project === ONBOARD_PROJECT_NAME &&
      stored.bridge === ONBOARD_BRIDGE_NAME &&
      stored.protocol_id === ONBOARD_PROTOCOL_ID &&
      stored.version === ONBOARD_PROTOCOL_VERSION
    ) {
      return {
        ...base,
        state: "synced",
        lastSyncedAt: String(stored.synced_at ?? ""),
        detail: `${ONBOARD_PROJECT_NAME} context protocol ${ONBOARD_PROTOCOL_VERSION} is marked synced to this extension build.`,
      };
    }
  } catch {
    // Local storage can be unavailable on restricted pages.
  }
  return base;
}

function markOnboardSynced(): OnboardSyncInfo {
  const next: OnboardSyncInfo = {
    project: ONBOARD_PROJECT_NAME,
    bridge: ONBOARD_BRIDGE_NAME,
    protocolId: ONBOARD_PROTOCOL_ID,
    version: ONBOARD_PROTOCOL_VERSION,
    state: "synced",
    lastSyncedAt: new Date().toISOString(),
    detail: `${ONBOARD_PROJECT_NAME} context protocol ${ONBOARD_PROTOCOL_VERSION} sync was requested from this page.`,
  };
  try {
    window.localStorage?.setItem(
      ONBOARD_SYNC_KEY,
      JSON.stringify({
        project: next.project,
        bridge: next.bridge,
        protocol_id: next.protocolId,
        version: next.version,
        synced_at: next.lastSyncedAt,
      }),
    );
  } catch {
    // Non-fatal; the button can still show synced in this page session.
  }
  return next;
}

function defaultPromptLibraryItems(): PromptLibraryItem[] {
  const now = "built-in";
  return [
    {
      id: "ion-context-router",
      title: "ION context router",
      category: "ION Context",
      tags: ["context", "router", "capsule"],
      pinned: true,
      updatedAt: now,
      usageCount: 0,
      origin: "built_in",
      text: "Use ION context routing. First identify the goal, then ask for or use the smallest relevant Capsule/Mini/context package. Do not assume full project context is active unless it has been attached or explicitly loaded.",
    },
    {
      id: "ion-codex-work-packet",
      title: "Codex work packet",
      category: "Codex",
      tags: ["codex", "implementation", "bounded"],
      pinned: true,
      updatedAt: now,
      usageCount: 0,
      origin: "built_in",
      text: "Create a bounded Codex work packet for this objective. Include objective, constraints, files likely involved, validation requested, and exact success criteria. Do not request broad rewrites unless necessary.",
    },
    {
      id: "ion-diagnostics",
      title: "Diagnostics report",
      category: "Diagnostics",
      tags: ["debug", "status", "browser"],
      pinned: false,
      updatedAt: now,
      usageCount: 0,
      origin: "built_in",
      text: "Give me a concise diagnostics report. Separate confirmed facts from assumptions. Include current visible symptoms, likely causes, smallest safe test, and recommended next action.",
    },
    {
      id: "ion-package-request",
      title: "Package request",
      category: "Packages",
      tags: ["docs", "zip", "context-package"],
      pinned: false,
      updatedAt: now,
      usageCount: 0,
      origin: "built_in",
      text: "Use the attached ION package as the source of truth. Summarize what is inside, identify the most relevant files for the current task, and ask before assuming missing context.",
    },
    {
      id: "ion-review",
      title: "Engineering review",
      category: "Review",
      tags: ["review", "risks", "tests"],
      pinned: false,
      updatedAt: now,
      usageCount: 0,
      origin: "built_in",
      text: "Review this like a pragmatic senior engineer. Prioritize bugs, regressions, unsafe assumptions, UX failures, and missing validation. Give findings first, then concise fixes.",
    },
  ];
}

function readPromptLibraryItems(): PromptLibraryItem[] {
  try {
    const stored = JSON.parse(window.localStorage?.getItem(PROMPT_LIBRARY_KEY) ?? "[]") as PromptLibraryItem[];
    if (Array.isArray(stored) && stored.length) return stored.filter((item) => item && item.id && item.text);
  } catch {
    // Use built-ins if local storage is unavailable.
  }
  return defaultPromptLibraryItems();
}

function writePromptLibraryItems(items: PromptLibraryItem[]): void {
  try {
    window.localStorage?.setItem(PROMPT_LIBRARY_KEY, JSON.stringify(items));
  } catch {
    // Non-fatal. The in-page library still works for this session.
  }
}

function defaultModeMemoryState(): ModeMemoryState {
  return {
    currentMode: "IDLE_MONITORING",
    lastMode: "IDLE_MONITORING",
    lastActionId: "",
    lastIntent: "",
    lastReceiptPath: "",
    lastQueueTarget: "",
    lastStatusTitle: "Monitoring ChatGPT",
    lastDetail: "Waiting for ion_action YAML blocks.",
    lastUpdatedAt: "",
  };
}

function readModeMemoryState(): ModeMemoryState {
  try {
    const stored = JSON.parse(window.localStorage?.getItem(MODE_MEMORY_KEY) ?? "{}") as Partial<ModeMemoryState>;
    const defaults = defaultModeMemoryState();
    return {
      ...defaults,
      ...stored,
      currentMode: isBridgeOperationalMode(stored.currentMode) ? stored.currentMode : defaults.currentMode,
      lastMode: isBridgeOperationalMode(stored.lastMode) ? stored.lastMode : defaults.lastMode,
    };
  } catch {
    return defaultModeMemoryState();
  }
}

function writeModeMemoryState(state: ModeMemoryState): void {
  try {
    window.localStorage?.setItem(MODE_MEMORY_KEY, JSON.stringify(state));
  } catch {
    // Mode memory is helpful but not required for action safety.
  }
}

function isBridgeOperationalMode(value: unknown): value is BridgeOperationalMode {
  return typeof value === "string" && [
    "IDLE_MONITORING",
    "DETECTED",
    "APPROVAL_REQUIRED",
    "APPROVAL_MODAL",
    "SUBMITTING",
    "RECEIPTED",
    "ERROR_BLOCKED",
    "INSPECTOR_CALIBRATION",
  ].includes(value);
}

function classifyOperationalMode(title: string, detail: string, tone: BridgeTone): BridgeOperationalMode {
  const text = `${title}\n${detail}`.toLowerCase();
  if (/approval modal|operator reviews/.test(text)) return "APPROVAL_MODAL";
  if (/inspector|calibrat|capture frame|pick attach|pick drop|tabs anchor|previewed|drop zone|attach target/.test(text)) {
    return "INSPECTOR_CALIBRATION";
  }
  if (tone === "error" || /blocked|rejected|degraded|failed|not parsed|missing|unverified/.test(text)) return "ERROR_BLOCKED";
  if (/approval required/.test(text)) return "APPROVAL_REQUIRED";
  if (/approved, submitting|submitting|requesting daemon validation|requesting braden approval/.test(text)) return "SUBMITTING";
  if (tone === "success" || /submitted|receipt|queued|ready/.test(text)) return "RECEIPTED";
  if (/detected|candidate|validating/.test(text)) return "DETECTED";
  return "IDLE_MONITORING";
}

function matchDetailLine(detail: string, key: string): string {
  const pattern = new RegExp(`^${key}:\\s*(.+)$`, "im");
  return detail.match(pattern)?.[1]?.trim() ?? "";
}

function firstDetailLine(detail: string): string {
  return detail.split("\n").map((line) => line.trim()).find(Boolean) ?? "";
}

function actionPartsFromDetail(detail: string): { actionId: string; intent: string } {
  const explicitAction = matchDetailLine(detail, "action_id");
  const explicitIntent = matchDetailLine(detail, "intent");
  if (explicitAction || explicitIntent) return { actionId: explicitAction, intent: explicitIntent };
  const firstLine = firstDetailLine(detail);
  const detected = firstLine.match(/^([a-z0-9_:-]+):\s*(.+)$/i);
  if (!detected) return { actionId: "", intent: "" };
  return { intent: detected[1].trim(), actionId: detected[2].trim() };
}

function updateModeMemory(title: string, detail: string, tone: BridgeTone): ModeMemoryState {
  const current = bridgeState.modeMemory as ModeMemoryState;
  const nextMode = classifyOperationalMode(title, detail, tone);
  const action = actionPartsFromDetail(detail);
  const receiptPath = matchDetailLine(detail, "receipt_path");
  const status = matchDetailLine(detail, "status");
  const queuePath = matchDetailLine(detail, "queue_path");
  const queueTarget = matchDetailLine(detail, "queue_target");
  const next: ModeMemoryState = {
    ...current,
    currentMode: nextMode,
    lastStatusTitle: title,
    lastDetail: firstDetailLine(detail) || title,
    lastUpdatedAt: new Date().toISOString(),
  };
  if (nextMode !== "IDLE_MONITORING") next.lastMode = nextMode;
  if (action.actionId) next.lastActionId = action.actionId;
  if (action.intent) next.lastIntent = action.intent;
  if (receiptPath) next.lastReceiptPath = receiptPath;
  if (queueTarget || queuePath) next.lastQueueTarget = queueTarget || queuePath;
  if (status && /queue|codex|carrier|accepted|submitted/i.test(status)) next.lastQueueTarget = status;
  bridgeState.modeMemory = next;
  writeModeMemoryState(next);
  return next;
}

function setExplicitOperationalMode(mode: BridgeOperationalMode, title: string, detail = ""): void {
  const current = bridgeState.modeMemory as ModeMemoryState;
  const next: ModeMemoryState = {
    ...current,
    currentMode: mode,
    lastMode: mode === "IDLE_MONITORING" ? current.lastMode : mode,
    lastStatusTitle: title,
    lastDetail: firstDetailLine(detail) || title,
    lastUpdatedAt: new Date().toISOString(),
  };
  bridgeState.modeMemory = next;
  writeModeMemoryState(next);
  renderPanel();
}

function modeBadgeLabel(mode: BridgeOperationalMode): string {
  const labels: Record<BridgeOperationalMode, string> = {
    IDLE_MONITORING: "MON",
    DETECTED: "DET",
    APPROVAL_REQUIRED: "APPR",
    APPROVAL_MODAL: "MODAL",
    SUBMITTING: "SEND",
    RECEIPTED: "RCPT",
    ERROR_BLOCKED: "BLOCK",
    INSPECTOR_CALIBRATION: "CAL",
  };
  return labels[mode];
}

function modeMemorySummary(memory: ModeMemoryState): string {
  if (memory.lastMode === "RECEIPTED" && memory.lastActionId) return "Last action queued";
  if (memory.lastActionId) return `Last ${memory.lastMode}: ${memory.lastActionId}`;
  return memory.lastStatusTitle || "Monitoring";
}

function modeMemoryDetail(memory: ModeMemoryState): string {
  return [
    "Mode memory",
    `current_mode: ${memory.currentMode}`,
    `last_mode: ${memory.lastMode}`,
    `last_action: ${memory.lastActionId || "none"}`,
    `last_intent: ${memory.lastIntent || "none"}`,
    `last_receipt: ${memory.lastReceiptPath || "none"}`,
    `last_queue_target: ${memory.lastQueueTarget || "none"}`,
    `last_status: ${memory.lastStatusTitle || "none"}`,
    `last_updated_at: ${memory.lastUpdatedAt || "not recorded"}`,
  ].join("\n");
}

function promptLibraryInitialState(): PromptLibraryState {
  const items = readPromptLibraryItems();
  const selected = items.find((item) => item.pinned) ?? items[0];
  return {
    status: "Prompt Library ready. Pick a prompt, insert it, queue it, or edit and save your own.",
    query: "",
    category: "all",
    selectedId: selected?.id ?? "",
    draftTitle: selected?.title ?? "",
    draftCategory: selected?.category ?? "General",
    draftTags: selected?.tags.join(", ") ?? "",
    draftText: selected?.text ?? "",
    items,
  };
}

const bridgeState = {
  title: "Monitoring ChatGPT",
  detail: "Waiting for ion_action YAML blocks.",
  tone: "idle" as BridgeTone,
  modeMemory: readModeMemoryState() as ModeMemoryState,
  action: "No action detected yet.",
  agent: "Codex-backed agent status has not been requested yet.",
  codex: {
    status: "Open Codex to load the existing Capsule-backed chat.",
    input: "",
    turns: [],
    view: "history",
    model: null,
    submitting: false,
    queueing: false,
  } as CodexChatState,
  messageQueue: {
    input: "",
    status: "Queue is idle. Add messages here and ION will send when ChatGPT is ready.",
    paused: false,
    allowMidOutput: false,
    activeOutput: false,
    sendAvailable: false,
    autoAcceptActive: false,
    autoAcceptUntil: "",
    autoAcceptTtlSeconds: 900,
    items: [],
  } as MessageQueueState,
  promptLibrary: promptLibraryInitialState() as PromptLibraryState,
  monitor: {
    estimatedTokens: 0,
    plusPercent: 0,
    proPercent: 0,
    thinkingPercent: 0,
    messageCount: 0,
    assistantMessageCount: 0,
    userMessageCount: 0,
    actionCandidateCount: 0,
    validActionCount: 0,
    blockedActionCount: 0,
    duplicateActionCount: 0,
    codeBlockCount: 0,
    composerControlCount: 0,
    selectedSourceCount: 0,
    uploadedAttachmentCount: 0,
    domNodes: 0,
    lagMs: 0,
    longTaskMs: 0,
    tone: "ready",
    summary: "Loaded transcript and browser lag monitor warming up.",
    detail:
      "ChatGPT browser pressure diagnostics are warming up.\n\nThis measures loaded browser transcript pressure, not exact active model context. ChatGPT uses rolling/managed context and does not expose exact live context composition to browser extensions.",
  } as MonitorMetrics,
  onboard: readOnboardSyncState() as OnboardSyncInfo,
  packages: "No context pack or ZIP export has been requested yet.",
  sandbox: "No ChatGPT sandbox returns have been requested yet.",
  automation: "Automation controls are staged only. This packet does not execute macros.",
  artifacts: "Artifact detection is staged only. No upload or local file movement occurs in this shell slice.",
  docs: {
    roots: [],
    currentRoot: "",
    currentPath: "",
    query: "",
    breadcrumbs: [],
    entries: [],
    selectedPath: "",
    selectedDocName: "",
    status: "Open Docs and pick a preselected root folder to browse files.",
  } as DocsBrowserState,
  projects: {
    status: "Open Projects to scan ION context-package folders.",
    roots: [],
    packages: [],
    selectedPath: "",
    selectedPaths: [],
    contextSyncOpen: false,
    contextSyncStatus: "No context sync package has been built yet.",
    contextSyncZipPath: "",
    contextSyncSha256: "",
  } as ProjectsState,
  settings: "No local calibration has been changed in this session.",
  inspectorLayers: [] as InspectorLayerOption[],
  inspectorSelectedIndex: 0,
  diagnostics:
    "Normal carrier flow: Sev emits an ion_action YAML block in ChatGPT, the extension detects it, Braden approves it, the local daemon records/executes it, and ION writes a receipt.\n\nThe buttons below are local diagnostics only. They fabricate known-good test actions so the extension/daemon path can be checked without waiting on ChatGPT to emit YAML.",
  tools: "Daemon: http://127.0.0.1:8767\nUse Rescan after ChatGPT finishes rendering a YAML block.",
  logs: [] as string[],
  anchor: {
    mode: "topbar_fallback",
    rect: null,
    element: null,
    health: "degraded",
    detail: "Composer anchor has not been evaluated yet.",
    source: "none",
    attachmentsDetected: 0,
  } as AnchorInfo,
};

let composerResizeObserver: ResizeObserver | null = null;
let observedComposerElement: HTMLElement | null = null;
let lastSettingsMode = false;
let renderingPanel = false;
let renderPanelQueued = false;
let syncingSettingsModeEvent = false;
let settingsPadEventsBound = false;
let docsClickTimer: number | null = null;
let settingsAnchorTarget: SettingsAnchorTarget = "tabs_anchor";
let settingsAnchorPoint: AnchorPoint = tabsAnchorMeta().anchor;

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
      inset: 0;
      z-index: 2147483646;
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
      flex-wrap: nowrap;
      justify-content: space-between;
      gap: 6px;
      min-height: 30px;
      border: 1px solid rgba(56,189,248,0.22);
      border-radius: 10px;
      background: rgba(0, 0, 0, 0.96);
      box-shadow: 0 0 18px rgba(56,189,248,0.12), 0 8px 22px rgba(0,0,0,0.34);
      padding: 2px 6px;
      backdrop-filter: blur(10px);
      pointer-events: auto;
    }
    #${PANEL_ID} .ion-top-rail .ion-toolbar-actions,
    #${PANEL_ID} .ion-top-rail .ion-tool {
      pointer-events: auto;
    }
    #${PANEL_ID}[data-anchor-health="degraded"] .ion-top-rail {
      border-color: rgba(56,189,248,0.22);
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
      max-width: max(74px, min(210px, calc(100% - 360px)));
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
    #${PANEL_ID} .ion-mode-memory {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      min-width: 0;
      max-width: 190px;
      height: 24px;
      padding: 0 7px;
      border: 1px solid rgba(255,255,255,0.13);
      border-radius: 8px;
      background: rgba(255,255,255,0.055);
      color: rgba(255,255,255,0.76);
      cursor: pointer;
      pointer-events: auto;
    }
    #${PANEL_ID} .ion-mode-pill {
      flex: 0 0 auto;
      min-width: 34px;
      height: 16px;
      border-radius: 999px;
      background: rgba(255,255,255,0.08);
      color: rgba(255,255,255,0.84);
      font: 900 8px/16px ui-sans-serif, system-ui, sans-serif;
      text-align: center;
    }
    #${PANEL_ID} .ion-mode-summary {
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 10px;
      font-weight: 750;
      line-height: 1;
    }
    #${PANEL_ID}[data-operational-mode="DETECTED"] .ion-mode-memory,
    #${PANEL_ID}[data-operational-mode="SUBMITTING"] .ion-mode-memory {
      border-color: rgba(56,189,248,0.35);
      background: rgba(8,47,73,0.26);
      color: rgba(224,242,254,0.96);
    }
    #${PANEL_ID}[data-operational-mode="APPROVAL_REQUIRED"] .ion-mode-memory,
    #${PANEL_ID}[data-operational-mode="APPROVAL_MODAL"] .ion-mode-memory {
      border-color: rgba(251,191,36,0.48);
      background: rgba(120,53,15,0.28);
      color: rgba(254,243,199,0.96);
    }
    #${PANEL_ID}[data-operational-mode="RECEIPTED"] .ion-mode-memory {
      border-color: rgba(52,211,153,0.44);
      background: rgba(6,78,59,0.30);
      color: rgba(220,252,231,0.96);
    }
    #${PANEL_ID}[data-operational-mode="ERROR_BLOCKED"] .ion-mode-memory {
      border-color: rgba(251,113,133,0.52);
      background: rgba(127,29,29,0.32);
      color: rgba(255,228,230,0.96);
    }
    #${PANEL_ID}[data-operational-mode="INSPECTOR_CALIBRATION"] .ion-mode-memory {
      border-color: rgba(168,85,247,0.42);
      background: rgba(46,16,101,0.28);
      color: rgba(237,233,254,0.96);
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
    #${PANEL_ID} .ion-icon-tool {
      width: 28px;
      padding: 0;
      font-size: 15px;
      font-weight: 700;
      text-align: center;
    }
    #${PANEL_ID} .ion-onboard-sync {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      max-width: 178px;
      border-color: rgba(56,189,248,0.24);
      background: rgba(8,47,73,0.24);
      color: rgba(224,242,254,0.95);
    }
    #${PANEL_ID} .ion-onboard-sync[data-onboard-state="synced"] {
      border-color: rgba(52,211,153,0.42);
      background: rgba(20,83,45,0.28);
      color: rgba(220,252,231,0.96);
    }
    #${PANEL_ID} .ion-context-sync {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      max-width: 150px;
      border-color: rgba(168,85,247,0.26);
      background: rgba(46,16,101,0.24);
      color: rgba(237,233,254,0.96);
    }
    #${PANEL_ID} .ion-context-sync[data-context-sync-state="ready"] {
      border-color: rgba(52,211,153,0.38);
      background: rgba(6,78,59,0.28);
      color: rgba(220,252,231,0.96);
    }
    #${PANEL_ID} .ion-auto-accept {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 0 8px;
      height: 24px;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 999px;
      background: rgba(255,255,255,0.06);
      color: rgba(255,255,255,0.76);
      font: 900 11px/22px ui-sans-serif, system-ui, sans-serif;
      cursor: pointer;
      pointer-events: auto;
      transition: all 0.2s ease;
    }
    #${PANEL_ID} .ion-auto-accept[data-active="true"] {
      border-color: rgba(56,189,248,0.64);
      background: rgba(8,47,73,0.52);
      color: rgba(224,242,254,0.96);
      box-shadow: 0 0 12px rgba(56,189,248,0.22);
    }
    #${PANEL_ID} .ion-auto-accept-toggle {
      width: 20px;
      height: 12px;
      border-radius: 999px;
      background: rgba(255,255,255,0.14);
      position: relative;
      transition: background 0.2s ease;
    }
    #${PANEL_ID} .ion-auto-accept[data-active="true"] .ion-auto-accept-toggle {
      background: #38bdf8;
    }
    #${PANEL_ID} .ion-auto-accept-toggle::after {
      content: "";
      position: absolute;
      top: 2px;
      left: 2px;
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: #fff;
      transition: transform 0.2s ease;
    }
    #${PANEL_ID} .ion-auto-accept[data-active="true"] .ion-auto-accept-toggle::after {
      transform: translateX(8px);
    }
    #${PANEL_ID} .ion-auto-accept-timer {
      font-variant-numeric: tabular-nums;
      opacity: 0.82;
      font-size: 10px;
    }
    #${PANEL_ID} .ion-auto-settings-popover {
      position: absolute;
      top: 32px;
      right: 12px;
      z-index: 2147483647;
      width: 140px;
      padding: 10px;
      border: 1px solid rgba(56,189,248,0.32);
      border-radius: 12px;
      background: rgba(1,12,20,0.98);
      box-shadow: 0 8px 32px rgba(0,0,0,0.48);
      display: grid;
      gap: 8px;
    }
    #${PANEL_ID} .ion-auto-settings-popover[data-visible="false"] {
      display: none;
    }
    #${PANEL_ID} .ion-auto-settings-title {
      font: 800 10px ui-sans-serif, system-ui, sans-serif;
      color: rgba(56,189,248,0.92);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    #${PANEL_ID} .ion-auto-settings-row {
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: center;
      gap: 8px;
      font: 900 11px ui-sans-serif, system-ui, sans-serif;
    }
    #${PANEL_ID} .ion-auto-settings-input {
      width: 48px;
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 6px;
      color: #fff;
      font: 900 11px ui-sans-serif, system-ui, sans-serif;
      padding: 2px 4px;
      text-align: center;
      outline: none;
    }
    #${PANEL_ID} .ion-auto-settings-input:focus {
      border-color: #38bdf8;
    }
    #${PANEL_ID} .ion-context-sync-icon {
      font-size: 13px;
      line-height: 1;
    }
    #${PANEL_ID} .ion-context-sync-label {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    #${PANEL_ID} .ion-context-sync-menu {
      position: absolute;
      top: calc(100% + 6px);
      right: 6px;
      display: none;
      width: min(380px, calc(100vw - 24px));
      max-height: min(58vh, 460px);
      box-sizing: border-box;
      gap: 8px;
      padding: 10px;
      border: 1px solid rgba(168,85,247,0.34);
      border-radius: 10px;
      background: rgba(12, 12, 16, 0.98);
      box-shadow: 0 16px 40px rgba(0,0,0,0.42), 0 0 18px rgba(168,85,247,0.14);
      backdrop-filter: blur(14px);
      z-index: 4;
    }
    #${PANEL_ID}[data-context-sync-open="true"] .ion-context-sync-menu {
      display: grid;
    }
    #${PANEL_ID} .ion-context-sync-head {
      display: grid;
      gap: 3px;
      min-width: 0;
    }
    #${PANEL_ID} .ion-context-sync-title {
      color: rgba(237,233,254,0.98);
      font-size: 12px;
      font-weight: 800;
      line-height: 1.25;
    }
    #${PANEL_ID} .ion-context-sync-status {
      color: rgba(255,255,255,0.66);
      font-size: 11px;
      line-height: 1.3;
      overflow-wrap: anywhere;
      white-space: pre-wrap;
    }
    #${PANEL_ID} .ion-context-sync-list {
      display: grid;
      gap: 5px;
      max-height: 220px;
      overflow: auto;
      padding-right: 2px;
    }
    #${PANEL_ID} .ion-context-sync-row {
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 8px;
      align-items: start;
      min-width: 0;
      padding: 7px;
      border: 1px solid rgba(255,255,255,0.10);
      border-radius: 8px;
      background: rgba(255,255,255,0.045);
      color: rgba(255,255,255,0.80);
      cursor: pointer;
    }
    #${PANEL_ID} .ion-context-sync-row[data-selected="true"] {
      border-color: rgba(168,85,247,0.56);
      background: rgba(88,28,135,0.22);
    }
    #${PANEL_ID} .ion-context-sync-row input {
      width: 14px;
      height: 14px;
      margin: 1px 0 0;
      accent-color: #a855f7;
    }
    #${PANEL_ID} .ion-context-sync-copy {
      display: grid;
      gap: 3px;
      min-width: 0;
    }
    #${PANEL_ID} .ion-context-sync-name {
      color: rgba(255,255,255,0.92);
      font-size: 12px;
      font-weight: 750;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    #${PANEL_ID} .ion-context-sync-meta {
      color: rgba(255,255,255,0.58);
      font-size: 10px;
      line-height: 1.25;
      overflow-wrap: anywhere;
    }
    #${PANEL_ID} .ion-context-sync-actions {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
    }
    #${PANEL_ID} .ion-context-sync-actions .ion-tool {
      height: 25px;
      border-color: rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.04);
    }
    #${PANEL_ID} .ion-onboard-icon {
      font-size: 13px;
      line-height: 1;
    }
    #${PANEL_ID} .ion-onboard-label {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    #${PANEL_ID} .ion-tool:hover,
    #${PANEL_ID} .ion-tab:hover {
      background: rgba(255,255,255,0.08);
      border-color: rgba(255,255,255,0.08);
    }
    #${PANEL_ID} .ion-tool[data-active="true"] {
      color: #ffd2b0;
      background: rgba(255,112,28,0.16);
      border-color: rgba(255,112,28,0.70);
    }
    #${PANEL_ID} .ion-toolbar-actions {
      display: flex;
      align-items: center;
      gap: 2px;
      flex: 0 0 auto;
      margin-left: auto;
    }
    #${PANEL_ID} .ion-monitor-strip {
      display: flex;
      align-items: center;
      gap: 6px;
      flex: 1 1 360px;
      min-width: 240px;
      overflow: hidden;
    }
    #${PANEL_ID} .ion-bottom-monitor {
      position: fixed;
      left: 12px;
      bottom: 1px;
      width: min(960px, calc(100vw - 24px));
      min-height: 22px;
      box-sizing: border-box;
      padding: 0 8px;
      border: 0;
      border-radius: 0;
      background: rgba(0,0,0,0.96);
      box-shadow: none;
      backdrop-filter: none;
      pointer-events: auto;
    }
    #${PANEL_ID} .ion-monitor-button,
    #${PANEL_ID} .ion-monitor-pill {
      height: 18px;
      border: 0;
      border-radius: 0;
      background: transparent;
      color: rgba(255,255,255,0.74);
      font-size: 10px;
      font-weight: 650;
      line-height: 18px;
      white-space: nowrap;
      text-shadow: 0 1px 4px rgba(0,0,0,0.85);
    }
    #${PANEL_ID} .ion-monitor-button {
      padding: 0;
      cursor: pointer;
    }
    #${PANEL_ID} .ion-monitor-pill {
      min-width: 0;
      max-width: 132px;
      padding: 0;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #${PANEL_ID} .ion-monitor-strip[data-tone="ready"] .ion-monitor-pill {
      color: rgba(190,242,100,0.92);
      background: transparent;
    }
    #${PANEL_ID} .ion-monitor-strip[data-tone="watch"] .ion-monitor-pill,
    #${PANEL_ID} .ion-monitor-strip[data-tone="watch"] .ion-monitor-button {
      color: rgba(254,240,138,0.96);
      background: transparent;
    }
    #${PANEL_ID} .ion-monitor-strip[data-tone="blocked"] .ion-monitor-pill,
    #${PANEL_ID} .ion-monitor-strip[data-tone="blocked"] .ion-monitor-button {
      color: rgba(254,202,202,0.98);
      background: transparent;
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
    #${PANEL_ID}[data-layout="tiny"] .ion-mode-summary {
      display: none;
    }
    #${PANEL_ID}[data-layout="tiny"] .ion-mode-memory {
      max-width: 52px;
      padding: 0 5px;
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
    #${PANEL_ID}[data-layout="tiny"] .ion-context-sync-label {
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
      justify-content: center;
      overflow-x: auto;
      scrollbar-width: none;
      margin: 0;
      padding: 0 8px;
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
      margin: 0 0 calc(-1 * var(--ion-chatops-tab-height, 22px));
      padding: 10px 10px calc(var(--ion-chatops-tab-height, 22px) + 12px);
      max-height: min(38vh, var(--ion-chatops-drawer-max-px, 360px));
      overflow: auto;
      pointer-events: auto;
      transform: translate(var(--ion-chatops-drawer-x-px, 0px), var(--ion-chatops-drawer-y-px, 0px));
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
      position: relative;
      z-index: 2;
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
    #${PANEL_ID} .ion-message-queue {
      display: grid;
      gap: 8px;
    }
    #${PANEL_ID} .ion-queue-input {
      width: 100%;
      min-height: 68px;
      resize: vertical;
      box-sizing: border-box;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 10px;
      background: rgba(0,0,0,0.28);
      color: rgba(255,255,255,0.86);
      padding: 8px;
      font: inherit;
      font-size: 12px;
      line-height: 1.35;
    }
    #${PANEL_ID} .ion-queue-flags {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      color: rgba(255,255,255,0.70);
      font-size: 11px;
    }
    #${PANEL_ID} .ion-queue-list {
      display: grid;
      gap: 6px;
      max-height: 150px;
      overflow: auto;
    }
    #${PANEL_ID} .ion-queue-item {
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 7px;
      padding: 7px;
      border: 1px solid rgba(255,255,255,0.10);
      border-radius: 9px;
      background: rgba(255,255,255,0.045);
      color: rgba(255,255,255,0.76);
      font-size: 11px;
      line-height: 1.3;
    }
    #${PANEL_ID} .ion-queue-item[data-status="waiting"] {
      border-color: rgba(251,191,36,0.32);
    }
    #${PANEL_ID} .ion-queue-item[data-status="sending"] {
      border-color: rgba(56,189,248,0.42);
    }
    #${PANEL_ID} .ion-queue-item[data-status="sent"] {
      opacity: 0.68;
      border-color: rgba(52,211,153,0.28);
    }
    #${PANEL_ID} .ion-queue-item[data-status="failed"] {
      border-color: rgba(251,113,133,0.38);
    }
    #${PANEL_ID} .ion-queue-status-chip {
      color: #ffd2b0;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 9px;
      letter-spacing: 0.03em;
    }
    #${PANEL_ID} .ion-queue-copy {
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }
    #${PANEL_ID} .ion-projects-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 8px;
      max-height: 210px;
      overflow: auto;
    }
    #${PANEL_ID} .ion-project-card {
      display: grid;
      gap: 6px;
      min-width: 0;
      padding: 9px;
      border: 1px solid rgba(56,189,248,0.22);
      border-radius: 12px;
      background: linear-gradient(160deg, rgba(8,47,73,0.34), rgba(0,0,0,0.22));
      color: rgba(255,255,255,0.82);
      text-align: left;
      cursor: pointer;
    }
    #${PANEL_ID} .ion-project-card[data-selected="true"] {
      border-color: rgba(255,112,28,0.82);
      box-shadow: 0 0 16px rgba(255,112,28,0.20);
    }
    #${PANEL_ID} .ion-project-title {
      color: rgba(224,242,254,0.96);
      font-weight: 800;
      font-size: 12px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    #${PANEL_ID} .ion-project-meta {
      color: rgba(255,255,255,0.58);
      font-size: 10px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    #${PANEL_ID} .ion-prompts-layout {
      display: grid;
      grid-template-columns: minmax(180px, 0.7fr) minmax(260px, 1.3fr);
      gap: 9px;
    }
    #${PANEL_ID} .ion-prompts-filters,
    #${PANEL_ID} .ion-prompts-editor {
      display: grid;
      gap: 7px;
    }
    #${PANEL_ID} .ion-prompt-list {
      display: grid;
      gap: 6px;
      max-height: 210px;
      overflow: auto;
    }
    #${PANEL_ID} .ion-prompt-card {
      display: grid;
      gap: 3px;
      padding: 7px;
      border: 1px solid rgba(255,255,255,0.10);
      border-radius: 9px;
      background: rgba(255,255,255,0.04);
      color: rgba(255,255,255,0.78);
      text-align: left;
      cursor: pointer;
    }
    #${PANEL_ID} .ion-prompt-card[data-selected="true"] {
      border-color: rgba(56,189,248,0.58);
      background: rgba(8,47,73,0.38);
    }
    #${PANEL_ID} .ion-prompt-title {
      color: rgba(224,242,254,0.96);
      font-weight: 800;
      font-size: 11px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    #${PANEL_ID} .ion-prompt-meta {
      color: rgba(255,255,255,0.54);
      font-size: 10px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    #${PANEL_ID} .ion-prompt-input,
    #${PANEL_ID} .ion-prompt-select,
    #${PANEL_ID} .ion-prompt-textarea {
      width: 100%;
      box-sizing: border-box;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 9px;
      background: rgba(0,0,0,0.28);
      color: rgba(255,255,255,0.86);
      padding: 7px;
      font: inherit;
      font-size: 11px;
    }
    #${PANEL_ID} .ion-prompt-textarea {
      min-height: 126px;
      resize: vertical;
      line-height: 1.35;
    }
    #${PANEL_ID}[data-layout="compact"] .ion-tab {
      padding: 0 6px;
      max-width: 94px;
    }
    #${PANEL_ID} .ion-tab-icon {
      display: none;
      font-size: 13px;
      line-height: 21px;
    }
    #${PANEL_ID}[data-tab-mode="icons"] .ion-tab {
      width: 31px;
      min-width: 31px;
      max-width: 31px;
      padding: 0;
      text-align: center;
    }
    #${PANEL_ID}[data-tab-mode="icons"] .ion-tab-label {
      display: none;
    }
    #${PANEL_ID}[data-tab-mode="icons"] .ion-tab-icon {
      display: inline;
    }
    #${SETTINGS_CONTROL_PAD_ID} {
      position: fixed;
      right: 16px;
      bottom: 16px;
      z-index: 2147483646;
      display: none;
      width: min(252px, calc(100vw - 24px));
      max-height: min(54vh, 340px);
      overflow: auto;
      padding: 8px;
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 10px;
      background: rgba(12,12,12,0.92);
      backdrop-filter: blur(12px);
      box-shadow: 0 14px 36px rgba(0,0,0,0.45);
      gap: 6px;
      grid-template-columns: 1fr;
      pointer-events: auto;
    }
    #${SETTINGS_CONTROL_PAD_ID}[data-visible="true"] {
      display: grid;
    }
    #${SETTINGS_CONTROL_PAD_ID}[data-visible="false"] {
      display: none;
    }
    #${SETTINGS_CONTROL_PAD_ID} .ion-pad-title {
      color: rgba(255,255,255,0.86);
      font-size: 10px;
      letter-spacing: 0.01em;
      line-height: 1.2;
    }
    #${SETTINGS_CONTROL_PAD_ID} .ion-pad-state {
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 7px;
      padding: 5px 7px;
      color: rgba(255,255,255,0.72);
      font-size: 10px;
      line-height: 1.25;
      background: rgba(12,12,12,0.74);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #${SETTINGS_CONTROL_PAD_ID} .ion-tool {
      min-height: 28px;
    }
    #${PANEL_ID} .ion-layout-picker {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 6px;
      width: 100%;
    }
    #${PANEL_ID} .ion-nudge-pad,
    #${SETTINGS_CONTROL_PAD_ID} .ion-nudge-pad {
      display: grid;
      grid-template-columns: repeat(3, 34px);
      grid-template-rows: repeat(3, 30px);
      gap: 4px;
      align-items: center;
      justify-content: start;
    }
    #${PANEL_ID} .ion-nudge-pad .ion-tool,
    #${SETTINGS_CONTROL_PAD_ID} .ion-nudge-pad .ion-tool {
      width: 34px;
      padding: 0;
    }
    #${PANEL_ID} .ion-nudge-spacer {
      width: 34px;
      height: 30px;
    }
    #${SETTINGS_CONTROL_PAD_ID} .ion-anchor-pad {
      display: grid;
      grid-template-columns: repeat(3, 34px);
      grid-template-rows: repeat(3, 30px);
      gap: 4px;
      align-items: center;
      justify-content: start;
    }
    #${SETTINGS_CONTROL_PAD_ID} .ion-anchor-pad .ion-tool {
      width: 34px;
      padding: 0;
    }
    #${SETTINGS_CONTROL_PAD_ID} .ion-anchor-spacer {
      width: 34px;
      height: 30px;
    }
    #${PANEL_ID} .ion-setting-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr);
      gap: 6px;
      width: 100%;
    }
    #${PANEL_ID} .ion-codex-chat {
      display: grid;
      gap: 7px;
    }
    #${PANEL_ID} .ion-codex-status {
      color: rgba(255,255,255,0.68);
      font-size: 10px;
      line-height: 1.25;
      white-space: pre-wrap;
    }
    #${PANEL_ID} .ion-codex-turns {
      display: grid;
      gap: 6px;
      max-height: 220px;
      overflow: auto;
      padding: 4px;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 9px;
      background:
        radial-gradient(circle at 18% 0%, rgba(56,189,248,0.16), transparent 34%),
        rgba(9,13,16,0.78);
    }
    #${PANEL_ID} .ion-codex-turn {
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 8px;
      padding: 7px;
      background: rgba(255,255,255,0.05);
      color: rgba(255,255,255,0.84);
      font-size: 11px;
      line-height: 1.35;
      white-space: pre-wrap;
    }
    #${PANEL_ID} .ion-codex-turn[data-author="operator"],
    #${PANEL_ID} .ion-codex-turn[data-author="user"] {
      border-color: rgba(255,112,28,0.42);
      background: rgba(255,112,28,0.10);
    }
    #${PANEL_ID} .ion-codex-turn b {
      display: block;
      margin-bottom: 4px;
      color: rgba(255,255,255,0.62);
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
    #${PANEL_ID} .ion-codex-input {
      min-height: 64px;
      resize: vertical;
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 9px;
      background: rgba(12,12,12,0.78);
      color: rgba(255,255,255,0.90);
      font-size: 12px;
      line-height: 1.35;
      padding: 8px;
      outline: none;
      font: inherit;
    }
    #${PANEL_ID} .ion-codex-input:focus {
      border-color: rgba(56,189,248,0.72);
      box-shadow: 0 0 0 3px rgba(56,189,248,0.13);
    }
    #${PANEL_ID} .ion-codex-subtabs {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 4px;
    }
    #${PANEL_ID} .ion-codex-subtab {
      appearance: none;
      min-height: 26px;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 999px;
      background: rgba(255,255,255,0.05);
      color: rgba(255,255,255,0.68);
      font: 800 10px/1 ui-sans-serif, system-ui, sans-serif;
      cursor: pointer;
    }
    #${PANEL_ID} .ion-codex-subtab[data-active="true"] {
      color: #07110d;
      background: #38bdf8;
      border-color: #38bdf8;
    }
    #${PANEL_ID} .ion-codex-context {
      display: grid;
      gap: 7px;
      max-height: 260px;
      overflow: auto;
      padding: 4px;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 9px;
      background: rgba(5,10,12,0.82);
    }
    #${PANEL_ID} .ion-codex-card {
      display: grid;
      gap: 5px;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 8px;
      padding: 8px;
      background: rgba(255,255,255,0.045);
      color: rgba(255,255,255,0.78);
      font-size: 10px;
      line-height: 1.32;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }
    #${PANEL_ID} .ion-codex-card b {
      color: rgba(255,255,255,0.92);
      font-size: 11px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }
    #${PANEL_ID} .ion-codex-card code {
      color: #bae6fd;
      font: 10px/1.3 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }
      #${PANEL_ID} .ion-docs-favorites,
      #${PANEL_ID} .ion-docs-root-list,
      #${PANEL_ID} .ion-docs-breadcrumbs,
      #${PANEL_ID} .ion-docs-entries,
      #${PANEL_ID} .ion-docs-actions {
        display: grid;
        gap: 5px;
        margin-top: 5px;
        align-items: start;
      }
      #${PANEL_ID} .ion-docs-actions {
        grid-template-columns: auto auto auto minmax(130px, 1fr);
        margin-top: 6px;
      }
      #${PANEL_ID} .ion-docs-root-list {
        grid-template-columns: 1fr;
        margin-bottom: 4px;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 7px;
        padding: 5px;
        max-height: 120px;
        overflow: auto;
        background: rgba(12,12,12,0.74);
      }
      #${PANEL_ID} .ion-docs-root-list .ion-tool[data-doc-root] {
        justify-content: flex-start;
        text-align: left;
        padding-inline: 7px;
      }
      #${PANEL_ID} .ion-docs-favorites {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
      #${PANEL_ID} .ion-docs-favorite {
        display: grid;
        grid-template-columns: 34px minmax(0, 1fr) auto;
        align-items: center;
        gap: 8px;
        min-height: 42px;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 8px;
        padding: 6px;
        background: rgba(14,14,20,0.72);
      }
      #${PANEL_ID} .ion-docs-favorite[data-selected="true"] {
        border-color: currentColor;
        color: rgba(255,112,28,0.95);
        box-shadow: 0 0 0 1px rgba(255,112,28,0.28) inset;
      }
      #${PANEL_ID} .ion-docs-favorite-thumb {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        border: 1px solid rgba(255,255,255,0.25);
        background: linear-gradient(160deg, rgba(255,255,255,0.18), rgba(255,255,255,0.05));
      }
      #${PANEL_ID} .ion-docs-favorite-copy {
        font-size: 10px;
        color: rgba(255,255,255,0.52);
      }
      #${PANEL_ID} .ion-docs-favorite-actions {
        display: inline-flex;
        gap: 4px;
        align-items: center;
      }
      #${PANEL_ID} .ion-docs-favorite-action {
        appearance: none;
        width: 24px;
        height: 24px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.14);
        background: rgba(255,255,255,0.07);
        color: rgba(255,255,255,0.82);
        font: 800 10px/1 ui-sans-serif, system-ui, sans-serif;
        cursor: pointer;
        padding: 0;
      }
      #${PANEL_ID} .ion-docs-favorite-action:hover {
        border-color: rgba(255,112,28,0.55);
        background: rgba(255,112,28,0.16);
      }
      #${PANEL_ID} .ion-docs-breadcrumbs {
        min-height: 18px;
        color: rgba(255,255,255,0.72);
        font-size: 10px;
        line-height: 1.2;
      border-radius: 7px;
      border: 1px dashed rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.03);
      padding: 4px 7px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #${PANEL_ID} .ion-docs-entry {
      display: flex;
      align-items: center;
      gap: 7px;
      min-height: 28px;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 7px;
      background: rgba(12,12,12,0.70);
      color: rgba(255,255,255,0.82);
      font-size: 11px;
      line-height: 1.2;
      padding: 5px 7px;
      justify-content: flex-start;
    }
    #${PANEL_ID} .ion-docs-entry[data-selected="true"] {
      border-color: rgba(255,112,28,0.72);
      background: rgba(255,112,28,0.13);
    }
    #${PANEL_ID} .ion-docs-entry[data-kind="folder"]::before {
      content: "📁";
      width: 20px;
      text-align: center;
      flex: 0 0 auto;
    }
    #${PANEL_ID} .ion-docs-entry[data-kind="file"]::before {
      content: "📄";
      width: 20px;
      text-align: center;
      flex: 0 0 auto;
    }
      #${PANEL_ID} .ion-docs-entry .ion-docs-thumbnail {
        width: 46px;
        height: 46px;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 6px;
        display: inline-flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      background: rgba(255,255,255,0.08);
      font-size: 9px;
      text-align: center;
      color: rgba(255,255,255,0.66);
      padding: 4px;
    }
    #${PANEL_ID} .ion-docs-entry .ion-docs-name {
      flex: 1 1 auto;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: rgba(255,255,255,0.86);
    }
    #${PANEL_ID} .ion-docs-entry .ion-docs-meta {
      font-size: 10px;
      color: rgba(255,255,255,0.53);
      margin-left: auto;
      white-space: nowrap;
    }
    #${PANEL_ID} .ion-docs-status {
      color: rgba(255,255,255,0.62);
      font-size: 10px;
      line-height: 1.25;
      margin-top: 4px;
      white-space: pre-wrap;
    }
      #${PANEL_ID} .ion-docs-toolbar {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto auto auto;
        gap: 6px;
        align-items: center;
        margin-top: 4px;
      }
      #${PANEL_ID} .ion-docs-tree-select {
        appearance: none;
        min-height: 28px;
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 7px;
        color: rgba(255,255,255,0.88);
        background: rgba(12,12,12,0.86);
        font-size: 11px;
        line-height: 1.2;
        padding: 4px 7px;
        outline: none;
      }
      #${PANEL_ID} .ion-docs-tree-select:focus {
        border-color: rgba(255,112,28,0.78);
        box-shadow: 0 0 0 3px rgba(255,112,28,0.13);
      }
    #${PANEL_ID} .ion-docs-search {
      min-height: 28px;
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 7px;
      background: rgba(12,12,12,0.72);
      color: rgba(255,255,255,0.86);
      font-size: 11px;
      padding: 4px 7px;
      outline: none;
    }
    #${PANEL_ID} .ion-docs-search:focus {
      border-color: rgba(255,112,28,0.78);
      box-shadow: 0 0 0 3px rgba(255,112,28,0.13);
    }
    #${PANEL_ID} .ion-setting-label {
      color: rgba(255,255,255,0.58);
      font-size: 10px;
      line-height: 1.2;
    }
    #${PANEL_ID} .ion-select {
      width: 100%;
      min-height: 28px;
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 7px;
      background: rgba(12,12,12,0.72);
      color: rgba(255,255,255,0.86);
      font-size: 11px;
      line-height: 1.2;
      padding: 4px 7px;
      outline: none;
    }
    #${PANEL_ID} .ion-select:focus {
      border-color: rgba(255,112,28,0.78);
      box-shadow: 0 0 0 3px rgba(255,112,28,0.13);
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

function ensureSettingsControlPad(): HTMLElement {
  let pad = document.getElementById(SETTINGS_CONTROL_PAD_ID);
  if (pad) return pad;
  pad = document.createElement("section");
  pad.id = SETTINGS_CONTROL_PAD_ID;
  pad.innerHTML = `
    <div class="ion-pad-title">Calibration controls</div>
    <div class="ion-pad-state" data-tool="settings-pad-state"></div>
    <div class="ion-pad-title">Move selected surface</div>
    <div class="ion-layout-picker">
      <button type="button" class="ion-tool" data-tool="settings-target-top">Top Rail</button>
      <button type="button" class="ion-tool" data-tool="settings-target-tabs">Tabs</button>
      <button type="button" class="ion-tool" data-tool="settings-target-drawer">Drawer</button>
    </div>
    <div class="ion-nudge-pad" aria-label="Move selected panel position">
      <span class="ion-nudge-spacer"></span>
      <button type="button" class="ion-tool" data-tool="settings-nudge-up" title="Move selected surface up">↑</button>
      <span class="ion-nudge-spacer"></span>
      <button type="button" class="ion-tool" data-tool="settings-nudge-left" title="Move selected surface left">←</button>
      <button type="button" class="ion-tool" data-tool="settings-nudge-reset" title="Reset selected surface">0</button>
      <button type="button" class="ion-tool" data-tool="settings-nudge-right" title="Move selected surface right">→</button>
      <span class="ion-nudge-spacer"></span>
      <button type="button" class="ion-tool" data-tool="settings-nudge-down" title="Move selected surface down">↓</button>
      <span class="ion-nudge-spacer"></span>
    </div>
    <div class="ion-pad-title">Anchor target</div>
    <div class="ion-layout-picker">
      <button type="button" class="ion-tool" data-tool="settings-anchor-target-tabs">Tabs Anchor</button>
      <button type="button" class="ion-tool" data-tool="settings-anchor-target-drop">Drop Zone</button>
      <button type="button" class="ion-tool" data-tool="settings-anchor-target-attach">Attach Target</button>
    </div>
    <div class="ion-pad-title">Anchor point on selected target</div>
    <div class="ion-anchor-pad" aria-label="Inspector anchor point">
      <span class="ion-anchor-spacer"></span>
      <button type="button" class="ion-tool" data-tool="settings-anchor-point" data-anchor="top" title="Anchor point: top edge">↑</button>
      <span class="ion-anchor-spacer"></span>
      <button type="button" class="ion-tool" data-tool="settings-anchor-point" data-anchor="left" title="Anchor point: left edge">←</button>
      <button type="button" class="ion-tool" data-tool="settings-anchor-point" data-anchor="center" title="Anchor point: center">•</button>
      <button type="button" class="ion-tool" data-tool="settings-anchor-point" data-anchor="right" title="Anchor point: right edge">→</button>
      <span class="ion-anchor-spacer"></span>
      <button type="button" class="ion-tool" data-tool="settings-anchor-point" data-anchor="bottom" title="Anchor point: bottom edge">↓</button>
      <span class="ion-anchor-spacer"></span>
    </div>
    <div class="ion-toolbar-actions">
      <button type="button" class="ion-tool" data-tool="settings-inspector-preview">Preview Layer</button>
    </div>
  `;
  pad.querySelectorAll<HTMLElement>('[data-tool^="settings-target-"], [data-tool^="settings-nudge-"]').forEach((button) => {
    const tool = button.dataset.tool ?? "";
    button.addEventListener("click", () => {
      const toolEvent = {
        "settings-target-top": "ion-chatops-settings-target-top",
        "settings-target-tabs": "ion-chatops-settings-target-tabs",
        "settings-target-drawer": "ion-chatops-settings-target-drawer",
        "settings-nudge-up": "ion-chatops-settings-nudge-up",
        "settings-nudge-down": "ion-chatops-settings-nudge-down",
        "settings-nudge-left": "ion-chatops-settings-nudge-left",
        "settings-nudge-right": "ion-chatops-settings-nudge-right",
        "settings-nudge-reset": "ion-chatops-settings-nudge-reset",
      } as Record<string, string>;
      const eventType = toolEvent[tool];
      if (!eventType) return;
      window.dispatchEvent(new CustomEvent(eventType));
    });
  });
  pad.querySelectorAll<HTMLElement>('[data-tool^="settings-anchor-target-"]').forEach((button) => {
    const tool = button.dataset.tool ?? "";
    button.addEventListener("click", () => {
    const target =
      tool === "settings-anchor-target-tabs" ? "tabs_anchor" :
      tool === "settings-anchor-target-drop" ? "drop_zone" :
      tool === "settings-anchor-target-attach" ? "attach_target" :
      null;
    if (!target) return;
    settingsAnchorTarget = target;
    settingsAnchorPoint = settingsAnchorPointForTarget(target);
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-anchor-target", { detail: { target } }));
    syncSettingsControlPadState();
  });
  });
  pad.querySelectorAll<HTMLElement>('[data-tool="settings-anchor-point"]').forEach((button) => {
    button.addEventListener("click", () => {
      const anchor = button.dataset.anchor;
      if (!anchor) return;
      settingsAnchorPoint = anchor as AnchorPoint;
      syncSettingsControlPadState();
      window.dispatchEvent(new CustomEvent("ion-chatops-settings-anchor-point", { detail: { anchor } }));
    });
  });
  pad.querySelector<HTMLElement>('[data-tool="settings-inspector-preview"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-inspector-preview"));
  });
  document.documentElement.appendChild(pad);
  return pad;
}

function syncSettingsControlPadState(panel = ensurePanel()): void {
  const pad = document.getElementById(SETTINGS_CONTROL_PAD_ID);
  if (!pad) return;
  const layoutTarget = readLayoutTarget();
  const padState = pad.querySelector<HTMLElement>('[data-tool="settings-pad-state"]');
  if (padState) {
    padState.textContent = `Target: ${settingsAnchorTarget} • Anchor: ${settingsAnchorPoint}`;
  }
  pad.querySelectorAll<HTMLElement>('[data-tool="settings-target-top"], [data-tool="settings-target-tabs"], [data-tool="settings-target-drawer"]').forEach((button) => {
    const tool = button.dataset.tool ?? "";
    const target = tool === "settings-target-top" ? "top_rail" : tool === "settings-target-drawer" ? "drawer" : "tabs";
    button.dataset.active = String(target === layoutTarget);
  });
  pad.querySelectorAll<HTMLElement>('[data-tool="settings-anchor-target-tabs"], [data-tool="settings-anchor-target-drop"], [data-tool="settings-anchor-target-attach"]').forEach((button) => {
    const tool = button.dataset.tool ?? "";
    const target =
      tool === "settings-anchor-target-tabs" ? "tabs_anchor" :
      tool === "settings-anchor-target-drop" ? "drop_zone" :
      tool === "settings-anchor-target-attach" ? "attach_target" :
      null;
    if (target) button.dataset.active = String(target === settingsAnchorTarget);
  });
  pad.querySelectorAll<HTMLElement>('[data-tool="settings-anchor-point"]').forEach((button) => {
    button.dataset.active = String(button.dataset.anchor === settingsAnchorPoint);
  });
  syncSettingsMode(panel, false);
}

function syncSettingsMode(panel = ensurePanel(), notify = false): void {
  const pad = document.getElementById(SETTINGS_CONTROL_PAD_ID);
  if (!pad) return;
  const settingsMode = panel.dataset.expanded === "true" && panel.dataset.tab === "settings";
  pad.dataset.visible = String(settingsMode);
  if (!notify) {
    lastSettingsMode = settingsMode;
    return;
  }
  if (settingsMode !== lastSettingsMode) {
    if (syncingSettingsModeEvent) return;
    lastSettingsMode = settingsMode;
    syncingSettingsModeEvent = true;
    try {
      window.dispatchEvent(new CustomEvent("ion-chatops-settings-inspector-mode", { detail: { enabled: settingsMode } }));
    } finally {
      syncingSettingsModeEvent = false;
    }
  }
}

function rectIsVisible(rect: DOMRect): boolean {
  return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
}

function isBridgeElement(element: Element): boolean {
  return Boolean(element.closest(`#${PANEL_ID}`) ?? element.closest(`#${MODAL_ID}`));
}

function visibleRect(element: Element): DOMRect | null {
  if (isBridgeElement(element)) return null;
  const style = window.getComputedStyle(element);
  if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) return null;
  const rect = element.getBoundingClientRect();
  return rectIsVisible(rect) ? rect : null;
}

function detectLeftBoundary(): number {
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
  document.querySelectorAll<Element>(selectors.join(",")).forEach((element) => {
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

function detectRightBoundary(): number {
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
  document.querySelectorAll<Element>(selectors.join(",")).forEach((element) => {
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

function topRail(panel: HTMLElement): HTMLElement | null {
  return panel.querySelector<HTMLElement>(".ion-top-rail");
}

function composerCockpit(panel: HTMLElement): HTMLElement | null {
  return panel.querySelector<HTMLElement>(".ion-composer-cockpit");
}

function readNumberSetting(key: string, fallback: number, min: number, max: number): number {
  try {
    const raw = window.localStorage?.getItem(key);
    const value = raw === null || raw === undefined ? Number.NaN : Number.parseInt(raw, 10);
    if (!Number.isFinite(value)) return fallback;
    return Math.max(min, Math.min(max, value));
  } catch (_error) {
    return fallback;
  }
}

function writeNumberSetting(key: string, value: number, min: number, max: number): number {
  const bounded = Math.max(min, Math.min(max, Math.round(value)));
  try {
    window.localStorage?.setItem(key, String(bounded));
  } catch (_error) {
    // Ignore storage failures; the panel will continue with defaults.
  }
  return bounded;
}

function readLayoutTarget(): LayoutTarget {
  try {
    const raw = String(window.localStorage?.getItem(LAYOUT_TARGET_KEY) ?? "").trim();
    if (raw === "top_rail" || raw === "tabs" || raw === "drawer") return raw;
  } catch (_error) {
    // Ignore storage failures; the panel will continue with defaults.
  }
  return "tabs";
}

function writeLayoutTarget(target: LayoutTarget): void {
  try {
    window.localStorage?.setItem(LAYOUT_TARGET_KEY, target);
  } catch (_error) {
    // Ignore storage failures; the panel will continue with defaults.
  }
}

function layoutOffset(target: LayoutTarget): { x: number; y: number } {
  if (target === "top_rail") {
    return {
      x: readNumberSetting(TOP_RAIL_X_KEY, 0, -260, 260),
      y: readNumberSetting(TOP_RAIL_Y_KEY, 0, -40, 160),
    };
  }
  if (target === "drawer") {
    return {
      x: readNumberSetting(DRAWER_X_KEY, 0, -260, 260),
      y: readNumberSetting(DRAWER_Y_KEY, 0, -180, 180),
    };
  }
  return {
    x: readNumberSetting(TABS_X_KEY, 0, -260, 260),
    y: readNumberSetting(TABS_Y_KEY, 0, -120, 160),
  };
}

function writeLayoutOffset(target: LayoutTarget, x: number, y: number): { x: number; y: number } {
  if (target === "top_rail") {
    return {
      x: writeNumberSetting(TOP_RAIL_X_KEY, x, -260, 260),
      y: writeNumberSetting(TOP_RAIL_Y_KEY, y, -40, 160),
    };
  }
  if (target === "drawer") {
    return {
      x: writeNumberSetting(DRAWER_X_KEY, x, -260, 260),
      y: writeNumberSetting(DRAWER_Y_KEY, y, -180, 180),
    };
  }
  return {
    x: writeNumberSetting(TABS_X_KEY, x, -260, 260),
    y: writeNumberSetting(TABS_Y_KEY, y, -120, 160),
  };
}

function applyDrawerOffset(panel: HTMLElement): void {
  const offset = layoutOffset("drawer");
  if (typeof panel.style.setProperty === "function") {
    panel.style.setProperty("--ion-chatops-drawer-x-px", `${offset.x}px`);
    panel.style.setProperty("--ion-chatops-drawer-y-px", `${offset.y}px`);
    panel.style.setProperty("--ion-chatops-tab-height", `${TAB_HEIGHT}px`);
  }
}

function attachTargetSelector(): string {
  try {
    return String(window.localStorage?.getItem(ATTACH_TARGET_SELECTOR_KEY) ?? "").trim();
  } catch (_error) {
    return "";
  }
}

function dropTargetSelector(): string {
  try {
    return String(window.localStorage?.getItem(DROP_TARGET_SELECTOR_KEY) ?? "").trim();
  } catch (_error) {
    return "";
  }
}

function tabsAnchorSelector(): string {
  try {
    return String(window.localStorage?.getItem(TABS_ANCHOR_SELECTOR_KEY) ?? "").trim();
  } catch (_error) {
    return "";
  }
}

function readStoredTargetMeta(raw: string, fallbackAnchor: AnchorPoint): TargetMetaInfo {
  if (!raw) return { selector: "", anchor: fallbackAnchor };
  try {
    const parsed = JSON.parse(raw);
    const selector = typeof parsed?.selector === "string" ? parsed.selector.trim() : "";
    const anchor =
      parsed?.anchor === "top" || parsed?.anchor === "left" || parsed?.anchor === "center" || parsed?.anchor === "right" || parsed?.anchor === "bottom"
        ? parsed.anchor
        : fallbackAnchor;
    return { selector: selector || "", anchor };
  } catch (_error) {
    return { selector: raw, anchor: fallbackAnchor };
  }
}

function attachTargetMeta(): TargetMetaInfo {
  return readStoredTargetMeta(attachTargetSelector(), "center");
}

function dropTargetMeta(): TargetMetaInfo {
  return readStoredTargetMeta(dropTargetSelector(), "center");
}

function tabsAnchorMeta(): TargetMetaInfo {
  return readStoredTargetMeta(tabsAnchorSelector(), "bottom");
}

function settingsAnchorPointForTarget(target: SettingsAnchorTarget): AnchorPoint {
  if (target === "tabs_anchor") return tabsAnchorMeta().anchor;
  if (target === "drop_zone") return dropTargetMeta().anchor;
  return attachTargetMeta().anchor;
}

function settingsSummary(): string {
  const attachMeta = attachTargetMeta();
  const dropMeta = dropTargetMeta();
  const tabsMeta = tabsAnchorMeta();
  const selected = readLayoutTarget();
  const top = layoutOffset("top_rail");
  const tabs = layoutOffset("tabs");
  const drawer = layoutOffset("drawer");
  return [
    `attach_target: ${attachMeta.selector || "not calibrated"} @${attachMeta.anchor}`,
    `drop_zone: ${dropMeta.selector || "default page/composer zone"} @${dropMeta.anchor}`,
    `tabs_anchor: ${tabsMeta.selector || "auto composer shell"} @${tabsMeta.anchor}`,
    `layout_target: ${selected}`,
    `top_rail_offset: x=${top.x}, y=${top.y}`,
    `tabs_offset: x=${tabs.x}, y=${tabs.y}`,
    `drawer_offset: x=${drawer.x}, y=${drawer.y}`,
    `tab_lift_px: ${readNumberSetting(TAB_LIFT_KEY, 2, -24, 48)}`,
    `drawer_max_px: ${readNumberSetting(DRAWER_MAX_KEY, 360, 220, 680)}`,
    `inspector_layers: ${bridgeState.inspectorLayers.length ? `${bridgeState.inspectorLayers.length} captured at last click` : "none captured"}`,
    "",
    "Inspector mode is always on while Settings is open. Use the fixed pad to select target + anchor point.",
    "Select Top Rail, Tabs, or Drawer, then use the arrow pad to nudge that surface.",
    "Capture and save anchor targets with the Inspector dropdown, then pick target + anchor point in the fixed pad.",
    "Use Pick Tabs Anchor when the automatic composer shell is not the visible panel top.",
    "Use Preview Drop Zone before Drop Latest. Pick Drop Zone if the blue ring is not where ChatGPT accepts file drops.",
    "Use Pick Attach Target, then click ChatGPT's real attach/add-file button once.",
    "Local Attach is a fallback and should only be used after Preview Target rings the correct button and Dry Run passes.",
  ].join("\n");
}

export function setBridgeInspectorLayers(layers: InspectorLayerOption[], selectedIndex = 0): void {
  bridgeState.inspectorLayers = layers.slice(0, 24);
  bridgeState.inspectorSelectedIndex = selectedIndex;
  renderPanel();
}

function selectLayoutTarget(target: LayoutTarget): void {
  writeLayoutTarget(target);
  bridgeState.settings = `layout_target set to ${target}`;
  appendBridgeLog(`Layout target selected: ${target}`);
  renderPanel();
}

function nudgeLayoutTarget(dx: number, dy: number): void {
  const target = readLayoutTarget();
  const current = layoutOffset(target);
  const next = writeLayoutOffset(target, current.x + dx, current.y + dy);
  bridgeState.settings = `${target} offset set to x=${next.x}, y=${next.y}`;
  appendBridgeLog(`Layout nudged: ${target} x=${next.x} y=${next.y}`);
  renderPanel();
}

function resetSelectedLayoutTarget(): void {
  const target = readLayoutTarget();
  const next = writeLayoutOffset(target, 0, 0);
  bridgeState.settings = `${target} offset reset to x=${next.x}, y=${next.y}`;
  appendBridgeLog(`Layout target reset: ${target}`);
  renderPanel();
}

function adjustTabLift(delta: number): void {
  const next = writeNumberSetting(TAB_LIFT_KEY, readNumberSetting(TAB_LIFT_KEY, 2, -24, 48) + delta, -24, 48);
  bridgeState.settings = `tab_lift_px set to ${next}`;
  appendBridgeLog(`Layout adjusted: tab_lift_px=${next}`);
  renderPanel();
}

function adjustDrawerMax(delta: number): void {
  const next = writeNumberSetting(DRAWER_MAX_KEY, readNumberSetting(DRAWER_MAX_KEY, 360, 220, 680) + delta, 220, 680);
  bridgeState.settings = `drawer_max_px set to ${next}`;
  appendBridgeLog(`Layout adjusted: drawer_max_px=${next}`);
  renderPanel();
}

function resetLayoutSettings(): void {
  try {
    window.localStorage?.removeItem(TAB_LIFT_KEY);
    window.localStorage?.removeItem(DRAWER_MAX_KEY);
    window.localStorage?.removeItem(LAYOUT_TARGET_KEY);
    window.localStorage?.removeItem(TOP_RAIL_X_KEY);
    window.localStorage?.removeItem(TOP_RAIL_Y_KEY);
    window.localStorage?.removeItem(TABS_X_KEY);
    window.localStorage?.removeItem(TABS_Y_KEY);
    window.localStorage?.removeItem(DRAWER_X_KEY);
    window.localStorage?.removeItem(DRAWER_Y_KEY);
    window.localStorage?.removeItem(TABS_ANCHOR_SELECTOR_KEY);
  } catch (_error) {
    // Ignore storage failures; the panel will continue with defaults.
  }
  bridgeState.settings = "Layout tuning reset to defaults.";
  appendBridgeLog("Layout tuning reset");
  renderPanel();
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

function applyTopRailLayout(panel: HTMLElement): void {
  const { left, available, width } = topBarGeometry();
  const offset = layoutOffset("top_rail");
  const rail = topRail(panel);
  if (!rail) return;
  rail.style.top = `${Math.max(0, PANEL_TOP + offset.y)}px`;
  rail.style.left = `${Math.max(TOP_BAR_GAP, left + offset.x)}px`;
  rail.style.right = "auto";
  rail.style.bottom = "auto";
  rail.style.width = `${width}px`;
  rail.style.maxWidth = `${Math.max(PANEL_TINY_WIDTH, available)}px`;
  if (typeof panel.style.setProperty === "function") {
    panel.style.setProperty("--ion-chatops-modal-left", `${left}px`);
    panel.style.setProperty("--ion-chatops-modal-width", `${Math.min(420, available)}px`);
  }
}

function applyTopBarLayout(panel: HTMLElement): void {
  const { left, available, width, layout } = topBarGeometry();
  const offset = layoutOffset("tabs");
  const cockpit = composerCockpit(panel);
  panel.dataset.anchorMode = "topbar_fallback";
  panel.dataset.anchorHealth = "degraded";
  panel.dataset.layout = layout;
  panel.dataset.tabMode = width < TAB_LABEL_MIN_WIDTH ? "icons" : "labels";
  applyTopRailLayout(panel);
  applyDrawerOffset(panel);
  if (cockpit) {
    cockpit.style.top = `${Math.max(0, PANEL_TOP + 36 + offset.y)}px`;
    cockpit.style.left = `${Math.max(TOP_BAR_GAP, left + offset.x)}px`;
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

function viewportHeight(): number {
  return Math.floor(window.visualViewport?.height ?? window.innerHeight);
}

function findComposerInput(): HTMLElement | null {
  const selectors = [
    "#prompt-textarea",
    "textarea",
    "[contenteditable='true'][role='textbox']",
    "[contenteditable='true']",
  ];
  for (const selector of selectors) {
    const node = document.querySelector<HTMLElement>(selector);
    if (!node || isBridgeElement(node)) continue;
    const rect = visibleRect(node);
    if (rect && rect.top > viewportHeight() * 0.45) return node;
  }
  return null;
}

function elementContains(parent: Element, child: Element): boolean {
  let current: Element | null = child;
  while (current) {
    if (current === parent) return true;
    current = current.parentElement;
  }
  return false;
}

function lowerViewportElement(element: Element): boolean {
  const rect = visibleRect(element);
  if (!rect) return false;
  return rect.bottom > viewportHeight() * 0.58 && rect.top > viewportHeight() * 0.25;
}

function composerButtonCount(element: Element): number {
  return Array.from(element.querySelectorAll("button, [role='button']")).filter((node) => {
    const rect = visibleRect(node);
    if (!rect) return false;
    const label = `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.textContent ?? ""}`.toLowerCase();
    return /send|attach|upload|file|voice|mic|audio|plus|stop|model|tool|source|github|drive/.test(label);
  }).length;
}

function composerAttachmentNodes(input: HTMLElement): HTMLElement[] {
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
  const nodes: HTMLElement[] = [];
  const seen = new Set<Element>();
  document.querySelectorAll<HTMLElement>(selectors).forEach((node) => {
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

function candidateComposerContainer(input: HTMLElement): HTMLElement {
  type ScoredCandidate = { element: HTMLElement; score: number };
  let best: ScoredCandidate | null = null;
  let current: HTMLElement | null = input;
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
    const containsAttachments = attachmentNodes.every((node) => elementContains(current as HTMLElement, node));
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

function observeComposerAnchor(element: HTMLElement | null): void {
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

function detectComposerAnchor(): AnchorInfo {
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
  const calibratedSelector = tabsAnchorSelector();
  if (calibratedSelector) {
    let calibrated: HTMLElement | null = null;
    try {
      calibrated = document.querySelector<HTMLElement>(calibratedSelector);
    } catch (_error) {
      return {
        mode: "topbar_fallback",
        rect: null,
        element: null,
        health: "degraded",
        detail: `Saved tabs anchor selector is invalid; clear or re-pick it.\nselector: ${calibratedSelector}`,
        source: "calibrated_tabs_anchor_invalid",
        attachmentsDetected: attachments.length,
      };
    }
    const calibratedRect = calibrated ? visibleRect(calibrated) : null;
    if (calibrated && calibratedRect && elementContains(calibrated, input)) {
      observeComposerAnchor(calibrated);
      return {
        mode: "composer",
        rect: calibratedRect,
        element: calibrated,
        health: "ready",
        source: "calibrated_tabs_anchor",
        attachmentsDetected: attachments.length,
        detail: [
          `Composer anchor ready: ${Math.round(calibratedRect.left)},${Math.round(calibratedRect.top)} ${Math.round(calibratedRect.width)}x${Math.round(calibratedRect.height)}.`,
          "source: calibrated_tabs_anchor",
          `selector: ${calibratedSelector}`,
          `attachments_detected: ${attachments.length}`,
        ].join("\n"),
      };
    }
    return {
      mode: "topbar_fallback",
      rect: null,
      element: null,
      health: "degraded",
      detail: [
        "Saved tabs anchor is missing, hidden, or does not contain the composer input.",
        `selector: ${calibratedSelector}`,
        "Use Settings -> Pick Tabs Anchor again, or Clear Tabs Anchor.",
      ].join("\n"),
      source: "calibrated_tabs_anchor_missing",
      attachmentsDetected: attachments.length,
    };
  }
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

function applyComposerLayout(panel: HTMLElement, anchor: AnchorInfo): boolean {
  if (anchor.mode !== "composer" || !anchor.rect) return false;
  const rect = anchor.rect;
  const viewport = viewportHeight();
  const margin = 12;
  const left = Math.max(margin, Math.round(rect.left));
  const available = Math.max(PANEL_TINY_WIDTH, Math.min(Math.round(rect.width), window.innerWidth - left - margin));
  const width = available;
  const tabLift = readNumberSetting(TAB_LIFT_KEY, 2, -24, 48);
  const drawerMax = readNumberSetting(DRAWER_MAX_KEY, 360, 220, 680);
  const offset = layoutOffset("tabs");
  const bottom = Math.max(4, Math.round(viewport - rect.top + tabLift - offset.y));
  const layout = width < PANEL_MIN_WIDTH ? "tiny" : width < 520 ? "compact" : "normal";
  const cockpit = composerCockpit(panel);
  panel.dataset.anchorMode = "composer";
  panel.dataset.anchorHealth = anchor.health;
  panel.dataset.layout = layout;
  panel.dataset.tabMode = width < TAB_LABEL_MIN_WIDTH ? "icons" : "labels";
  applyDrawerOffset(panel);
  if (cockpit) {
    cockpit.style.top = "auto";
    cockpit.style.left = `${Math.max(margin, left + offset.x)}px`;
    cockpit.style.right = "auto";
    cockpit.style.bottom = `${bottom}px`;
    cockpit.style.width = `${width}px`;
    cockpit.style.maxWidth = `${available}px`;
  }
  if (typeof panel.style.setProperty === "function") {
    panel.style.setProperty("--ion-chatops-drawer-max-px", `${drawerMax}px`);
  }
  positionApprovalModal();
  return true;
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
    <div class="ion-top-rail">
      <div class="ion-row">
        <span class="ion-dot"></span>
        <div>
          <div class="ion-label">ION ChatOps</div>
          <div class="ion-title"></div>
        </div>
      </div>
      <button type="button" class="ion-mode-memory" data-mode-memory aria-label="Open ION mode memory">
        <span class="ion-mode-pill" data-mode-pill>MON</span>
        <span class="ion-mode-summary" data-mode-summary>Monitoring</span>
      </button>
      <div class="ion-toolbar-actions">
        <button type="button" class="ion-tool ion-icon-tool" data-tool="rescan" aria-label="Rescan page for ION actions" title="Rescan page for ION actions">↻</button>
        <button type="button" class="ion-tool ion-onboard-sync" data-tool="insert-reentry" aria-label="Sync latest ION context protocol">
          <span class="ion-onboard-icon" aria-hidden="true">◎</span>
          <span class="ion-onboard-label" data-onboard-label>ION v0.1.0</span>
        </button>
          <button type="button" class="ion-tool ion-context-sync" data-tool="context-sync-toggle" aria-label="Open ION context sync projects" aria-expanded="false">
            <span class="ion-context-sync-icon" aria-hidden="true">⇄</span>
            <span class="ion-context-sync-label" data-context-sync-label>Context Sync</span>
          </button>
          <div class="ion-tool ion-auto-accept" data-tool="gateway-auto-accept" aria-label="Toggle ION Action auto accept" title="Toggle Action Gateway auto-accept for safe browser queue packets">
            <div class="ion-auto-accept-toggle"></div>
            <span data-auto-accept-label>Auto</span>
            <span class="ion-auto-accept-timer" data-auto-accept-timer></span>
          </div>
          <div class="ion-auto-settings-popover" data-visible="false">
            <div class="ion-auto-settings-title">Auto Settings</div>
            <div class="ion-auto-settings-row">
              <span>TTL (min)</span>
              <input type="number" class="ion-auto-settings-input" data-auto-accept-ttl-input min="1" max="1440" step="1">
            </div>
          </div>
        </div>
      <div class="ion-context-sync-menu" data-context-sync-menu></div>
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
            <button type="button" class="ion-tool" data-tool="bounded-agent-status">Bounded Lane</button>
            <button type="button" class="ion-tool" data-tool="agent-relays">Relays</button>
            <button type="button" class="ion-tool" data-tool="agent-receipts">Receipts</button>
            <button type="button" class="ion-tool" data-tool="agent-prepare">Prepare Next</button>
            <button type="button" class="ion-tool" data-tool="agent-start">Start One</button>
          </div>
        </div>
        <div class="ion-tab-panel" data-panel="codex">
          <div class="ion-codex-chat">
            <div class="ion-codex-status" data-codex="status"></div>
            <div class="ion-codex-subtabs">
              <button type="button" class="ion-codex-subtab" data-codex-view="history">History</button>
              <button type="button" class="ion-codex-subtab" data-codex-view="capsule">Capsule</button>
              <button type="button" class="ion-codex-subtab" data-codex-view="mini">Mini</button>
              <button type="button" class="ion-codex-subtab" data-codex-view="context">Context</button>
              <button type="button" class="ion-codex-subtab" data-codex-view="queue">Queue</button>
            </div>
            <div class="ion-codex-turns" data-codex="turns"></div>
            <div class="ion-codex-context" data-codex="context"></div>
            <textarea class="ion-codex-input" data-codex="input" placeholder="Ask the mounted ION Codex Capsule chat..."></textarea>
            <div class="ion-toolbar-actions">
              <button type="button" class="ion-tool" data-tool="codex-refresh">Refresh</button>
              <button type="button" class="ion-tool" data-tool="codex-send">Send</button>
              <button type="button" class="ion-tool" data-tool="codex-queue">Queue for Codex</button>
              <button type="button" class="ion-tool" data-tool="codex-open-helixion">Open Helixion</button>
            </div>
          </div>
        </div>
        <div class="ion-tab-panel" data-panel="queue">
          <div class="ion-message-queue">
            <div class="ion-detail" data-queue="status"></div>
            <textarea class="ion-queue-input" data-queue="input" placeholder="Type one or more queued messages. Use blank lines to split multiple messages. ION sends them only when ChatGPT is idle unless mid-output sending is enabled."></textarea>
            <div class="ion-queue-flags">
              <label><input type="checkbox" data-queue="allow-mid-output"> Allow mid-output send if ChatGPT enables Send</label>
              <span data-queue="readiness"></span>
            </div>
            <div class="ion-toolbar-actions">
              <button type="button" class="ion-tool" data-tool="queue-add">Add to Queue</button>
              <button type="button" class="ion-tool" data-tool="queue-import-pack">Import Pack</button>
              <button type="button" class="ion-tool" data-tool="queue-pause">Pause</button>
              <button type="button" class="ion-tool" data-tool="queue-send-next">Send Next</button>
              <button type="button" class="ion-tool" data-tool="queue-clear-sent">Clear Sent</button>
              <button type="button" class="ion-tool" data-tool="queue-clear-all">Clear All</button>
            </div>
            <input type="file" data-queue-pack="file" accept=".json,.zip,application/json,application/zip" hidden>
            <div class="ion-queue-list" data-queue="items"></div>
          </div>
        </div>
        <div class="ion-tab-panel" data-panel="prompts">
          <div class="ion-detail" data-prompts="status"></div>
          <div class="ion-prompts-layout">
            <div class="ion-prompts-filters">
              <input type="search" class="ion-prompt-input" data-prompts="query" placeholder="Search prompts, tags, categories">
              <select class="ion-prompt-select" data-prompts="category"></select>
              <div class="ion-prompt-list" data-prompts="list"></div>
            </div>
            <div class="ion-prompts-editor">
              <input class="ion-prompt-input" data-prompts="title" placeholder="Prompt title">
              <input class="ion-prompt-input" data-prompts="draft-category" placeholder="Category">
              <input class="ion-prompt-input" data-prompts="tags" placeholder="tags, comma, separated">
              <textarea class="ion-prompt-textarea" data-prompts="text" placeholder="Prompt text"></textarea>
              <div class="ion-toolbar-actions">
                <button type="button" class="ion-tool" data-tool="prompt-insert">Insert</button>
                <button type="button" class="ion-tool" data-tool="prompt-append">Append</button>
                <button type="button" class="ion-tool" data-tool="prompt-queue">Queue</button>
                <button type="button" class="ion-tool" data-tool="prompt-save">Save</button>
                <button type="button" class="ion-tool" data-tool="prompt-new">New</button>
                <button type="button" class="ion-tool" data-tool="prompt-pin">Pin</button>
                <button type="button" class="ion-tool" data-tool="prompt-delete">Delete</button>
                <button type="button" class="ion-tool" data-tool="prompt-reset">Reset Built-ins</button>
              </div>
            </div>
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
        <div class="ion-tab-panel" data-panel="projects">
          <div class="ion-detail" data-projects="status"></div>
          <div class="ion-toolbar-actions">
            <button type="button" class="ion-tool" data-tool="projects-refresh">Refresh Projects</button>
            <button type="button" class="ion-tool" data-tool="projects-drop-selected">Drop Selected</button>
            <button type="button" class="ion-tool" data-tool="projects-open-root">Open Context Packages</button>
          </div>
          <div class="ion-projects-grid" data-projects="grid"></div>
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
            <button type="button" class="ion-tool" data-tool="artifact-preview-drop">Preview Drop Zone</button>
            <button type="button" class="ion-tool" data-tool="artifact-preview-attach">Preview Target</button>
            <button type="button" class="ion-tool" data-tool="artifact-dry-run-attach">Dry Run Attach</button>
            <button type="button" class="ion-tool" data-tool="artifact-drop-latest">Drop Latest</button>
            <button type="button" class="ion-tool" data-tool="artifact-local-attach">Local Attach</button>
          </div>
          </div>
          <div class="ion-tab-panel" data-panel="docs">
            <div class="ion-setting-row">
              <input type="search" class="ion-docs-search" data-docs-control="search" placeholder="Search docs (name contains)">
            </div>
            <div class="ion-pad-title">Favorites</div>
            <div class="ion-docs-favorites" data-docs="favorites"></div>
            <div class="ion-pad-title">Quick roots</div>
            <div class="ion-docs-root-list" data-docs="roots"></div>
            <div class="ion-docs-actions">
              <button type="button" class="ion-tool" data-tool="docs-open-home">Home</button>
              <button type="button" class="ion-tool" data-tool="docs-open-parent">Parent</button>
              <button type="button" class="ion-tool" data-tool="docs-refresh">Refresh</button>
              <select class="ion-docs-tree-select" data-docs="tree">
                <option value="">Browse file-tree…</option>
              </select>
            </div>
            <div class="ion-pad-title">Current path</div>
            <div class="ion-docs-breadcrumbs" data-docs="breadcrumbs"></div>
            <div class="ion-pad-title">Directory</div>
            <div class="ion-docs-entries" data-docs="entries"></div>
            <div class="ion-docs-status" data-docs="status"></div>
        </div>
        <div class="ion-tab-panel" data-panel="settings">
          <div class="ion-detail" data-field="settings"></div>
          <div class="ion-setting-row">
            <div class="ion-setting-label">DOM inspector captured element stack</div>
            <select class="ion-select" data-control="settings-inspector-layer"></select>
          </div>
          <div class="ion-toolbar-actions">
            <button type="button" class="ion-tool" data-tool="settings-inspector-save-tabs">Save As Tabs Anchor</button>
            <button type="button" class="ion-tool" data-tool="settings-inspector-save-drop">Save As Drop Zone</button>
            <button type="button" class="ion-tool" data-tool="settings-inspector-save-attach">Save As Attach Target</button>
          </div>
          <div class="ion-toolbar-actions">
            <button type="button" class="ion-tool" data-tool="settings-frame-capture">Frame Capture</button>
            <button type="button" class="ion-tool" data-tool="settings-frame-save">Capture Framed</button>
            <button type="button" class="ion-tool" data-tool="settings-frame-load">Load Frame</button>
            <button type="button" class="ion-tool" data-tool="settings-frame-delete">Delete Frame</button>
            <button type="button" class="ion-tool" data-tool="settings-pick-attach">Pick Attach Target</button>
            <button type="button" class="ion-tool" data-tool="settings-clear-attach">Clear Attach Target</button>
            <button type="button" class="ion-tool" data-tool="settings-pick-drop">Pick Drop Zone</button>
            <button type="button" class="ion-tool" data-tool="settings-clear-drop">Clear Drop Zone</button>
            <button type="button" class="ion-tool" data-tool="settings-pick-tabs-anchor">Pick Tabs Anchor</button>
            <button type="button" class="ion-tool" data-tool="settings-clear-tabs-anchor">Clear Tabs Anchor</button>
            <button type="button" class="ion-tool" data-tool="settings-tabs-up">Tabs Up</button>
            <button type="button" class="ion-tool" data-tool="settings-tabs-down">Tabs Down</button>
            <button type="button" class="ion-tool" data-tool="settings-drawer-taller">Drawer Taller</button>
            <button type="button" class="ion-tool" data-tool="settings-drawer-shorter">Drawer Shorter</button>
            <button type="button" class="ion-tool" data-tool="settings-layout-reset">Reset Layout</button>
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
        <button type="button" class="ion-tab" data-tab="status" title="Status"><span class="ion-tab-label">Status</span><span class="ion-tab-icon" aria-hidden="true">●</span></button>
        <button type="button" class="ion-tab" data-tab="action" title="Action"><span class="ion-tab-label">Action</span><span class="ion-tab-icon" aria-hidden="true">✓</span></button>
        <button type="button" class="ion-tab" data-tab="agent" title="Agent"><span class="ion-tab-label">Agent</span><span class="ion-tab-icon" aria-hidden="true">A</span></button>
        <button type="button" class="ion-tab" data-tab="codex" title="Codex Chat"><span class="ion-tab-label">Codex</span><span class="ion-tab-icon" aria-hidden="true">C</span></button>
        <button type="button" class="ion-tab" data-tab="queue" title="Message Queue"><span class="ion-tab-label">Queue</span><span class="ion-tab-icon" aria-hidden="true">Q</span></button>
        <button type="button" class="ion-tab" data-tab="prompts" title="Prompt Library"><span class="ion-tab-label">Prompts</span><span class="ion-tab-icon" aria-hidden="true">Pr</span></button>
        <button type="button" class="ion-tab" data-tab="packages" title="Packages"><span class="ion-tab-label">Packages</span><span class="ion-tab-icon" aria-hidden="true">□</span></button>
        <button type="button" class="ion-tab" data-tab="projects" title="Projects"><span class="ion-tab-label">Projects</span><span class="ion-tab-icon" aria-hidden="true">P</span></button>
        <button type="button" class="ion-tab" data-tab="sandbox" title="Sandbox"><span class="ion-tab-label">Sandbox</span><span class="ion-tab-icon" aria-hidden="true">◇</span></button>
        <button type="button" class="ion-tab" data-tab="automation" title="Automation"><span class="ion-tab-label">Automation</span><span class="ion-tab-icon" aria-hidden="true">▶</span></button>
        <button type="button" class="ion-tab" data-tab="artifacts" title="Artifacts"><span class="ion-tab-label">Artifacts</span><span class="ion-tab-icon" aria-hidden="true">⇪</span></button>
        <button type="button" class="ion-tab" data-tab="docs" title="Docs"><span class="ion-tab-label">Docs</span><span class="ion-tab-icon" aria-hidden="true">📚</span></button>
        <button type="button" class="ion-tab" data-tab="settings" title="Settings"><span class="ion-tab-label">Settings</span><span class="ion-tab-icon" aria-hidden="true">⚙</span></button>
        <button type="button" class="ion-tab" data-tab="diagnostics" title="Diagnostics"><span class="ion-tab-label">Diagnostics</span><span class="ion-tab-icon" aria-hidden="true">!</span></button>
        <button type="button" class="ion-tab" data-tab="tools" title="Logs"><span class="ion-tab-label">Logs</span><span class="ion-tab-icon" aria-hidden="true">≡</span></button>
      </div>
    </div>
    <div class="ion-monitor-strip ion-bottom-monitor" data-monitor="strip" data-tone="ready">
      <button type="button" class="ion-monitor-button" data-tool="monitor-diagnostics">Diagnostics</button>
      <span class="ion-monitor-pill" data-monitor="messages">Msgs warming</span>
      <span class="ion-monitor-pill" data-monitor="assistant">AI warming</span>
      <span class="ion-monitor-pill" data-monitor="chat">Loaded text warming</span>
      <span class="ion-monitor-pill" data-monitor="actions">Actions warming</span>
      <span class="ion-monitor-pill" data-monitor="queue">Queue warming</span>
      <span class="ion-monitor-pill" data-monitor="connected-actions">Conn Acts warming</span>
      <span class="ion-monitor-pill" data-monitor="connected">Conn warming</span>
      <span class="ion-monitor-pill" data-monitor="sources">Sources warming</span>
      <span class="ion-monitor-pill" data-monitor="attachments">Attaches warming</span>
      <span class="ion-monitor-pill" data-monitor="lag">Lag warming</span>
      <span class="ion-monitor-pill" data-monitor="dom">DOM warming</span>
    </div>
  `;
  document.documentElement.appendChild(panel);
  panel.querySelector<HTMLElement>("[data-mode-memory]")?.addEventListener("click", () => {
    panel.dataset.expanded = "true";
    panel.dataset.tab = "status";
    renderPanel(panel);
  });
  panel.querySelectorAll<HTMLElement>(".ion-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      const nextTab = tab.dataset.tab ?? "status";
      if (panel.dataset.expanded === "true" && panel.dataset.tab === nextTab) {
        panel.dataset.expanded = "false";
      } else {
        panel.dataset.expanded = "true";
        panel.dataset.tab = nextTab;
      }
      if (nextTab === "docs" && panel.dataset.expanded === "true") {
        window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root"));
      }
      if (nextTab === "codex" && panel.dataset.expanded === "true") {
        window.dispatchEvent(new CustomEvent("ion-chatops-codex-refresh"));
      }
      if (nextTab === "projects" && panel.dataset.expanded === "true") {
        window.dispatchEvent(new CustomEvent("ion-chatops-projects-refresh"));
      }
      syncSettingsMode(panel, true);
      renderPanel(panel);
    });
  });
  if (typeof document.addEventListener === "function") {
    document.addEventListener("keydown", (event) => {
      if (event.key !== "Escape") return;
      panel.dataset.expanded = "false";
      setBridgeProjectsState({ contextSyncOpen: false });
      syncSettingsMode(panel, true);
      renderPanel(panel);
    });
  }
  panel.querySelector('[data-tool="rescan"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-rescan"));
  });
  panel.querySelector('[data-tool="insert-reentry"]')?.addEventListener("click", () => {
    bridgeState.onboard = markOnboardSynced();
    renderPanel(panel);
    window.dispatchEvent(new CustomEvent("ion-chatops-insert-reentry", {
      detail: {
        project: ONBOARD_PROJECT_NAME,
        bridge: ONBOARD_BRIDGE_NAME,
        protocol_id: ONBOARD_PROTOCOL_ID,
        version: ONBOARD_PROTOCOL_VERSION,
      },
    }));
  });
  panel.querySelector('[data-tool="context-sync-toggle"]')?.addEventListener("click", () => {
    const projects = bridgeState.projects as ProjectsState;
    const nextOpen = !projects.contextSyncOpen;
    setBridgeProjectsState({ contextSyncOpen: nextOpen });
    if (nextOpen && !projects.packages.length) {
      window.dispatchEvent(new CustomEvent("ion-chatops-projects-refresh"));
    }
  });
  panel.querySelector('[data-tool="gateway-auto-accept"]')?.addEventListener("click", (event) => {
    const target = event.target as HTMLElement;
    if (target.closest("[data-auto-accept-timer]")) {
      const popover = panel.querySelector<HTMLElement>(".ion-auto-settings-popover");
      if (popover) {
        popover.dataset.visible = String(popover.dataset.visible === "false");
      }
      return;
    }
    window.dispatchEvent(new CustomEvent("ion-chatops-gateway-auto-accept-toggle"));
  });
  panel.querySelector('[data-auto-accept-ttl-input]')?.addEventListener("input", (event) => {
    const input = event.target as HTMLInputElement;
    const ttl_seconds = Math.max(60, Number(input.value) * 60);
    window.dispatchEvent(new CustomEvent("ion-chatops-gateway-auto-accept-settings", { detail: { ttl_seconds } }));
  });
  const contextSyncMenu = panel.querySelector<HTMLElement>("[data-context-sync-menu]");
  contextSyncMenu?.addEventListener("click", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const button = source?.closest<HTMLElement>("[data-context-sync-action]");
    const action = button?.dataset.contextSyncAction ?? "";
    if (!action) return;
    event.preventDefault();
    const projects = bridgeState.projects as ProjectsState;
    if (action === "refresh") {
      window.dispatchEvent(new CustomEvent("ion-chatops-projects-refresh"));
      return;
    }
    if (action === "open-projects") {
      panel.dataset.expanded = "true";
      panel.dataset.tab = "projects";
      setBridgeProjectsState({ contextSyncOpen: false });
      return;
    }
    if (action === "select-all") {
      setBridgeProjectsState({
        selectedPaths: projects.packages.slice(0, 12).map((entry) => entry.path),
        contextSyncStatus: `Selected ${Math.min(projects.packages.length, 12)} project package(s) for context sync.`,
        contextSyncOpen: true,
      });
      return;
    }
    if (action === "clear") {
      setBridgeProjectsState({
        selectedPaths: [],
        contextSyncStatus: "Selection cleared. Pick one or more project packages.",
        contextSyncOpen: true,
      });
      return;
    }
    if (action === "build") {
      const selectedPaths = (projects.selectedPaths ?? []).filter(Boolean);
      if (!selectedPaths.length) {
        setBridgeProjectsState({
          contextSyncStatus: "Select at least one project package before building a context sync ZIP.",
          contextSyncOpen: true,
        });
        return;
      }
      setBridgeProjectsState({
        contextSyncStatus: `Requesting context sync ZIP for ${selectedPaths.length} project package(s)...`,
        contextSyncOpen: true,
      });
      window.dispatchEvent(new CustomEvent("ion-chatops-project-context-sync", { detail: { paths: selectedPaths } }));
    }
  });
  contextSyncMenu?.addEventListener("change", (event) => {
    const input = event.target instanceof HTMLInputElement ? event.target : null;
    const path = input?.dataset.contextSyncPath ?? "";
    if (!path) return;
    const projects = bridgeState.projects as ProjectsState;
    const selected = new Set((projects.selectedPaths ?? []).filter(Boolean));
    if (input.checked) selected.add(path);
    else selected.delete(path);
    setBridgeProjectsState({
      selectedPaths: Array.from(selected),
      contextSyncStatus: `${selected.size} project package(s) selected for context sync.`,
      contextSyncOpen: true,
    });
  });
  panel.querySelector('[data-tool="monitor-diagnostics"]')?.addEventListener("click", () => {
    panel.dataset.expanded = "true";
    panel.dataset.tab = "diagnostics";
    syncSettingsMode(panel, true);
    renderPanel(panel);
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
  panel.querySelector('[data-tool="bounded-agent-status"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-bounded-agent-status"));
  });
  panel.querySelector('[data-tool="agent-relays"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-agent-relays"));
  });
  panel.querySelector('[data-tool="agent-receipts"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-agent-receipts"));
  });
  panel.querySelector('[data-tool="agent-prepare"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-agent-prepare"));
  });
  panel.querySelector('[data-tool="agent-start"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-agent-start"));
  });
  panel.querySelector('[data-tool="codex-refresh"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-codex-refresh"));
  });
  panel.querySelector<HTMLTextAreaElement>('[data-codex="input"]')?.addEventListener("input", (event) => {
    bridgeState.codex.input = event.currentTarget?.value ?? "";
  });
  panel.querySelectorAll<HTMLElement>("[data-codex-view]").forEach((button) => {
    button.addEventListener("click", () => {
      const view = button.dataset.codexView;
      if (view === "history" || view === "capsule" || view === "mini" || view === "context" || view === "queue") {
        setBridgeCodexState({ view });
      }
    });
  });
  panel.querySelector('[data-tool="codex-send"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-codex-send", { detail: { message: bridgeState.codex.input } }));
  });
  panel.querySelector('[data-tool="codex-queue"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-codex-queue", { detail: { message: bridgeState.codex.input } }));
  });
  panel.querySelector('[data-tool="codex-open-helixion"]')?.addEventListener("click", () => {
    window.open("https://ion.helixion.net/cockpit/chat", "_blank", "noopener,noreferrer");
  });
  panel.querySelector<HTMLTextAreaElement>('[data-queue="input"]')?.addEventListener("input", (event) => {
    (bridgeState.messageQueue as MessageQueueState).input = event.currentTarget?.value ?? "";
  });
  panel.querySelector('[data-tool="queue-add"]')?.addEventListener("click", () => {
    const queue = bridgeState.messageQueue as MessageQueueState;
    const text = queue.input.trim();
    if (!text) return;
    queue.input = "";
    window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-add", { detail: { text } }));
    renderPanel(panel);
  });
  panel.querySelector('[data-tool="queue-import-pack"]')?.addEventListener("click", () => {
    panel.querySelector<HTMLInputElement>('[data-queue-pack="file"]')?.click();
  });
  panel.querySelector<HTMLInputElement>('[data-queue-pack="file"]')?.addEventListener("change", (event) => {
    const input = event.currentTarget;
    const file = input?.files?.[0];
    if (!file) return;
    void importQueuePackFile(file).finally(() => {
      if (input) input.value = "";
    });
  });
  panel.querySelector('[data-tool="queue-pause"]')?.addEventListener("click", () => {
    const queue = bridgeState.messageQueue as MessageQueueState;
    window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-pause", { detail: { paused: !queue.paused } }));
  });
  panel.querySelector('[data-tool="queue-send-next"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-send-next"));
  });
  panel.querySelector('[data-tool="queue-clear-sent"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-clear", { detail: { mode: "sent" } }));
  });
  panel.querySelector('[data-tool="queue-clear-all"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-clear", { detail: { mode: "all" } }));
  });
  panel.querySelector<HTMLInputElement>('[data-queue="allow-mid-output"]')?.addEventListener("change", (event) => {
    window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-mid-output", { detail: { allow: Boolean(event.currentTarget?.checked) } }));
  });
  panel.querySelector<HTMLInputElement>('[data-prompts="query"]')?.addEventListener("input", (event) => {
    setBridgePromptLibraryState({ query: event.currentTarget?.value ?? "" });
  });
  panel.querySelector<HTMLSelectElement>('[data-prompts="category"]')?.addEventListener("change", (event) => {
    setBridgePromptLibraryState({ category: event.currentTarget?.value ?? "all" });
  });
  panel.querySelector<HTMLElement>('[data-prompts="list"]')?.addEventListener("click", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest<HTMLElement>("[data-prompt-id]");
    if (!target?.dataset.promptId) return;
    selectPromptLibraryItem(target.dataset.promptId);
  });
  panel.querySelectorAll<HTMLInputElement | HTMLTextAreaElement>('[data-prompts="title"], [data-prompts="draft-category"], [data-prompts="tags"], [data-prompts="text"]').forEach((input) => {
    input.addEventListener("input", () => {
      setBridgePromptLibraryState({
        draftTitle: (panel.querySelector<HTMLInputElement>('[data-prompts="title"]')?.value ?? ""),
        draftCategory: (panel.querySelector<HTMLInputElement>('[data-prompts="draft-category"]')?.value ?? ""),
        draftTags: (panel.querySelector<HTMLInputElement>('[data-prompts="tags"]')?.value ?? ""),
        draftText: (panel.querySelector<HTMLTextAreaElement>('[data-prompts="text"]')?.value ?? ""),
      });
    });
  });
  panel.querySelector('[data-tool="prompt-insert"]')?.addEventListener("click", () => {
    dispatchPromptToComposer("replace");
  });
  panel.querySelector('[data-tool="prompt-append"]')?.addEventListener("click", () => {
    dispatchPromptToComposer("append");
  });
  panel.querySelector('[data-tool="prompt-queue"]')?.addEventListener("click", () => {
    const prompt = bridgeState.promptLibrary as PromptLibraryState;
    if (prompt.draftText.trim()) window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-add", { detail: { text: prompt.draftText.trim() } }));
    markPromptUsed(prompt.selectedId, "Prompt queued.");
  });
  panel.querySelector('[data-tool="prompt-save"]')?.addEventListener("click", () => {
    savePromptLibraryDraft();
  });
  panel.querySelector('[data-tool="prompt-new"]')?.addEventListener("click", () => {
    setBridgePromptLibraryState({
      selectedId: "",
      draftTitle: "",
      draftCategory: "General",
      draftTags: "",
      draftText: "",
      status: "New prompt draft ready.",
    });
  });
  panel.querySelector('[data-tool="prompt-pin"]')?.addEventListener("click", () => {
    togglePromptPinned();
  });
  panel.querySelector('[data-tool="prompt-delete"]')?.addEventListener("click", () => {
    deleteSelectedPrompt();
  });
  panel.querySelector('[data-tool="prompt-reset"]')?.addEventListener("click", () => {
    const items = defaultPromptLibraryItems();
    writePromptLibraryItems(items);
    const selected = items[0];
    setBridgePromptLibraryState({
      items,
      selectedId: selected.id,
      draftTitle: selected.title,
      draftCategory: selected.category,
      draftTags: selected.tags.join(", "),
      draftText: selected.text,
      status: "Prompt library reset to built-ins.",
    });
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
  panel.querySelector('[data-tool="projects-refresh"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-projects-refresh"));
  });
  panel.querySelector('[data-tool="projects-drop-selected"]')?.addEventListener("click", () => {
    const path = (bridgeState.projects as ProjectsState).selectedPath;
    if (path) window.dispatchEvent(new CustomEvent("ion-chatops-projects-drop", { detail: { path } }));
  });
  panel.querySelector('[data-tool="projects-open-root"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root", { detail: { path: "ION/05_context/history/kernel_store/context_packages" } }));
    panel.dataset.expanded = "true";
    panel.dataset.tab = "docs";
    renderPanel(panel);
  });
  panel.querySelector<HTMLElement>('[data-projects="grid"]')?.addEventListener("click", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest<HTMLElement>("[data-project-path]");
    const path = target?.dataset.projectPath ?? "";
    if (!path) return;
    setBridgeProjectsState({ selectedPath: path });
  });
  panel.querySelector<HTMLElement>('[data-projects="grid"]')?.addEventListener("dblclick", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest<HTMLElement>("[data-project-path]");
    const path = target?.dataset.projectPath ?? "";
    if (!path) return;
    event.preventDefault();
    window.dispatchEvent(new CustomEvent("ion-chatops-projects-drop", { detail: { path } }));
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
  panel.querySelector('[data-tool="artifact-preview-attach"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-artifact-preview-attach"));
  });
  panel.querySelector('[data-tool="artifact-preview-drop"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-artifact-preview-drop"));
  });
  panel.querySelector('[data-tool="artifact-dry-run-attach"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-artifact-dry-run-attach"));
  });
  panel.querySelector('[data-tool="artifact-local-attach"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-artifact-local-attach"));
  });
  panel.querySelector('[data-tool="docs-open-home"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root"));
  });
  panel.querySelector('[data-tool="docs-open-parent"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-parent"));
  });
  panel.querySelector('[data-tool="docs-refresh"]')?.addEventListener("click", () => {
    const currentPath = panel.querySelector<HTMLElement>('[data-docs="entries"]')?.dataset.currentPath ?? "";
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-folder", {
      detail: {
        path: currentPath,
        query: panel.querySelector<HTMLInputElement>('[data-docs-control="search"]')?.value ?? "",
      },
    }));
  });
  panel.querySelector<HTMLInputElement>('[data-docs-control="search"]')?.addEventListener("input", (event) => {
    const query = event.currentTarget?.value ?? "";
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-search", { detail: { query } }));
  });
  panel.querySelector('[data-docs="favorites"]')?.addEventListener("click", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const action = source?.closest<HTMLElement>("[data-doc-fav-action]");
    if (action) {
      event.preventDefault();
      event.stopPropagation();
      const path = action.dataset.docRoot ?? "";
      const label = action.dataset.docLabel ?? path.split("/").pop() ?? "";
      if (!path) return;
      const kind = action.dataset.docFavAction ?? "";
      if (kind === "drop") {
        window.dispatchEvent(new CustomEvent("ion-chatops-docs-drag-doc", { detail: { path, name: label, source: "favorite_button" } }));
      } else if (kind === "open") {
        window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root", { detail: { path } }));
      } else if (kind === "remove") {
        setBridgeDocsState({ roots: (bridgeState.docs as DocsBrowserState).roots.filter((root) => root !== path), status: `Favorite hidden for this session: ${label}` });
      } else if (kind === "more") {
        setBridgeDocsState({ status: `Favorite actions for ${label}: double-click tile to zip/drop, arrow opens, x hides for this session.` });
      }
      return;
    }
    const target = source?.closest<HTMLElement>("[data-doc-root]");
    if (!target) return;
    const path = target.dataset.docRoot ?? "";
    if (!path) return;
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root", { detail: { path } }));
  });
  panel.querySelector('[data-docs="favorites"]')?.addEventListener("dblclick", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    if (source?.closest("[data-doc-fav-action]")) return;
    const target = source?.closest<HTMLElement>("[data-doc-root]");
    if (!target) return;
    const path = target.dataset.docRoot ?? "";
    const label = target.dataset.docLabel ?? path.split("/").pop() ?? "";
    if (!path) return;
    event.preventDefault();
    event.stopPropagation();
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-drag-doc", { detail: { path, name: label, source: "favorite_double_click" } }));
  });
  panel.querySelector<HTMLSelectElement>('[data-docs="tree"]')?.addEventListener("change", (event) => {
    const select = event.currentTarget;
    const path = select?.value ?? "";
    if (!path) {
      window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root"));
      return;
    }
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root", { detail: { path } }));
  });
  panel.querySelector<HTMLElement>('[data-docs="roots"]')?.addEventListener("click", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest<HTMLElement>("[data-doc-root]");
    if (!target) return;
    const path = target.dataset.docRoot ?? "";
    if (!path) return;
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root", { detail: { path } }));
  });
  panel.querySelector<HTMLElement>('[data-docs="entries"]')?.addEventListener("click", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest<HTMLElement>("[data-doc-kind]");
    if (!target) return;
    const kind = target.dataset.docKind ?? "";
    const path = target.dataset.docPath ?? "";
    if (!path) return;
    if (kind === "folder") {
      if (docsClickTimer !== null) window.clearTimeout(docsClickTimer);
      docsClickTimer = window.setTimeout(() => {
        docsClickTimer = null;
        window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-folder", { detail: { path } }));
      }, 220);
      return;
    }
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-doc", { detail: { path, name: target.dataset.docName ?? path.split("/").pop() ?? "" } }));
  });
  panel.querySelector<HTMLElement>('[data-docs="entries"]')?.addEventListener("dblclick", (event) => {
    if (docsClickTimer !== null) {
      window.clearTimeout(docsClickTimer);
      docsClickTimer = null;
    }
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest<HTMLElement>("[data-doc-kind]");
    if (!target) return;
    const path = target.dataset.docPath ?? "";
    const name = target.dataset.docName ?? path.split("/").pop() ?? "";
    if (!path) return;
    event.preventDefault();
    event.stopPropagation();
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-drag-doc", {
      detail: {
        path,
        name,
      },
    }));
  });
  panel.querySelector<HTMLElement>('[data-docs="entries"]')?.addEventListener("dragstart", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest<HTMLElement>("[data-doc-kind]");
    if (!target) return;
    const path = target.dataset.docPath ?? "";
    const name = target.dataset.docName ?? "";
    if (!path) return;
    (event as DragEvent).dataTransfer?.setData("text/plain", path);
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-drag-doc", {
      detail: {
        path,
        name,
      },
    }));
  });
  panel.querySelector('[data-tool="settings-pick-attach"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-pick-attach"));
  });
  panel.querySelector('[data-tool="settings-frame-capture"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-frame-capture"));
  });
  panel.querySelector('[data-tool="settings-frame-save"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-frame-save"));
  });
  panel.querySelector('[data-tool="settings-frame-load"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-frame-load"));
  });
  panel.querySelector('[data-tool="settings-frame-delete"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-frame-delete"));
  });
  panel.querySelector('[data-tool="settings-clear-attach"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-clear-attach"));
  });
  panel.querySelector('[data-tool="settings-pick-drop"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-pick-drop"));
  });
  panel.querySelector('[data-tool="settings-clear-drop"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-clear-drop"));
  });
  panel.querySelector('[data-tool="settings-pick-tabs-anchor"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-pick-tabs-anchor"));
  });
  panel.querySelector('[data-tool="settings-clear-tabs-anchor"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-clear-tabs-anchor"));
  });
  panel.querySelector('[data-tool="settings-inspector-preview"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-inspector-preview"));
  });
  panel.querySelector('[data-tool="settings-inspector-save-tabs"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-inspector-save", { detail: { target: "tabs_anchor" } }));
  });
  panel.querySelector('[data-tool="settings-inspector-save-drop"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-inspector-save", { detail: { target: "drop_zone" } }));
  });
  panel.querySelector('[data-tool="settings-inspector-save-attach"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-inspector-save", { detail: { target: "attach_target" } }));
  });
  panel.querySelector<HTMLSelectElement>('[data-control="settings-inspector-layer"]')?.addEventListener("change", (event) => {
    const select = event.currentTarget as HTMLSelectElement;
    window.dispatchEvent(new CustomEvent("ion-chatops-settings-inspector-layer", { detail: { index: Number.parseInt(select.value, 10) || 0 } }));
  });
  panel.querySelector('[data-tool="settings-tabs-up"]')?.addEventListener("click", () => {
    adjustTabLift(4);
  });
  panel.querySelector('[data-tool="settings-tabs-down"]')?.addEventListener("click", () => {
    adjustTabLift(-4);
  });
  panel.querySelector('[data-tool="settings-drawer-taller"]')?.addEventListener("click", () => {
    adjustDrawerMax(40);
  });
  panel.querySelector('[data-tool="settings-drawer-shorter"]')?.addEventListener("click", () => {
    adjustDrawerMax(-40);
  });
  panel.querySelector('[data-tool="settings-layout-reset"]')?.addEventListener("click", () => {
    resetLayoutSettings();
  });
  panel.querySelector('[data-tool="collapse"]')?.addEventListener("click", () => {
    panel.dataset.expanded = "false";
    syncSettingsMode(panel, true);
    renderPanel(panel);
  });
  ensureSettingsControlPad();
  bindSettingsPadEvents();
  syncSettingsMode(panel);
  syncSettingsControlPadState(panel);
  renderPanel(panel);
  return panel;
}

function bindSettingsPadEvents(): void {
  if (settingsPadEventsBound) return;
  settingsPadEventsBound = true;
  window.addEventListener("ion-chatops-settings-target-top", () => {
    selectLayoutTarget("top_rail");
  });
  window.addEventListener("ion-chatops-settings-target-tabs", () => {
    selectLayoutTarget("tabs");
  });
  window.addEventListener("ion-chatops-settings-target-drawer", () => {
    selectLayoutTarget("drawer");
  });
  window.addEventListener("ion-chatops-settings-nudge-up", () => {
    nudgeLayoutTarget(0, -2);
  });
  window.addEventListener("ion-chatops-settings-nudge-down", () => {
    nudgeLayoutTarget(0, 2);
  });
  window.addEventListener("ion-chatops-settings-nudge-left", () => {
    nudgeLayoutTarget(-2, 0);
  });
  window.addEventListener("ion-chatops-settings-nudge-right", () => {
    nudgeLayoutTarget(2, 0);
  });
  window.addEventListener("ion-chatops-settings-nudge-reset", () => {
    resetSelectedLayoutTarget();
  });
  window.addEventListener("ion-chatops-settings-anchor-target", (event) => {
    const detail = (event as CustomEvent<{ target?: SettingsAnchorTarget }>).detail;
    if (detail?.target && (detail.target === "tabs_anchor" || detail.target === "drop_zone" || detail.target === "attach_target")) {
      settingsAnchorTarget = detail.target;
      syncSettingsControlPadState(ensurePanel());
    }
  });
  window.addEventListener("ion-chatops-settings-anchor-point", (event) => {
    const detail = (event as CustomEvent<{ anchor?: string }>).detail;
    const anchor = detail?.anchor;
    if (anchor === "top" || anchor === "left" || anchor === "center" || anchor === "right" || anchor === "bottom") {
      settingsAnchorPoint = anchor;
      syncSettingsControlPadState(ensurePanel());
    }
  });
  window.addEventListener("ion-chatops-settings-inspector-mode", (event) => {
    const detail = (event as CustomEvent<{ enabled?: boolean }>).detail;
    const enabled = Boolean(detail?.enabled);
    if (enabled) {
      syncSettingsControlPadState(ensurePanel());
    } else if (!enabled) {
      syncSettingsControlPadState(ensurePanel());
    }
  });
}

function docsStateSummary(): string {
  const docs = bridgeState.docs as DocsBrowserState;
  const root = docs.currentRoot ? `root: ${docs.currentRoot}` : "root: not selected";
  const path = docs.currentPath || "/";
  const count = docs.entries.length;
  return [
    root,
    `path: ${path}`,
    `items: ${count}`,
    docs.selectedPath ? `selected: ${docs.selectedDocName || docs.selectedPath}` : "selected: none",
  ].join("\n");
}

function asRecord(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {};
}

function asArray(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

function shortJson(value: unknown, limit = 900): string {
  const text = typeof value === "string" ? value : JSON.stringify(value ?? {}, null, 2);
  return text.length > limit ? `${text.slice(0, limit)}\n...` : text;
}

function latestCodexTurnWithEngine(turns: CodexChatTurn[]): CodexChatTurn | null {
  for (let index = turns.length - 1; index >= 0; index -= 1) {
    if (turns[index]?.chat_engine || turns[index]?.context_refs?.length) return turns[index];
  }
  return turns.length ? turns[turns.length - 1] : null;
}

function appendCodexCard(parent: HTMLElement, title: string, lines: unknown[]): void {
  const card = document.createElement("section");
  card.className = "ion-codex-card";
  const heading = document.createElement("b");
  heading.textContent = title;
  card.appendChild(heading);
  const body = document.createElement("code");
  body.textContent = lines.map((line) => typeof line === "string" ? line : shortJson(line)).filter(Boolean).join("\n") || "No data exposed by the current Codex model.";
  card.appendChild(body);
  parent.appendChild(card);
}

function renderCodexContextView(parent: HTMLElement, codex: CodexChatState): void {
  const model = asRecord(codex.model);
  const solo = asRecord(model.codex_solo_context);
  const capsule = asRecord(solo.capsule);
  const docs = asRecord(model.context_documents);
  const latest = latestCodexTurnWithEngine(codex.turns);
  const latestEngine = asRecord(latest?.chat_engine);
  const contextMount = asRecord(latestEngine.context_mount);
  parent.innerHTML = "";
  if (codex.view === "capsule") {
    appendCodexCard(parent, "Capsule basis", [
      `verdict: ${String(solo.verdict ?? model.verdict ?? "unknown")}`,
      `minimum_context: ${String(capsule.minimum_context ?? "")}`,
      `path: ${String(capsule.path ?? asRecord(solo.paths).capsule ?? "ION/05_context/current/codex_solo/CAPSULE.md")}`,
      `entry_count: ${String(capsule.entry_count ?? "")}`,
      `witness_policy: ${String(solo.witness_policy ?? "")}`,
    ]);
    appendCodexCard(parent, "Recent capsule rows", asArray(capsule.recent_rows).slice(-6).map((row) => {
      const record = asRecord(row);
      return `${record.id ?? ""} ${record.date ?? ""} ${record.status ?? ""}\n${record.summary ?? ""}\n${record.evidence ?? ""}`;
    }));
    appendCodexCard(parent, "CAPSULE.md snapshot", [asRecord(docs.capsule).text ?? "Capsule text is not exposed by the current model response."]);
    appendCodexCard(parent, "Capsule tail", asArray(capsule.tail).slice(-6));
    return;
  }
  if (codex.view === "mini") {
    appendCodexCard(parent, "Mini role", [
      `mini_role: ${String(asRecord(solo.active_context).mini_role ?? "lookup_receipt_index_not_prompt_source")}`,
      `mini_path: ${String(asRecord(solo.paths).mini ?? asRecord(solo.active_context).mini_path ?? "ION/05_context/current/codex_solo/MINI.md")}`,
      `hot_context: ${String(asRecord(solo.paths).hot_context ?? asRecord(solo.active_context).hot_context_path ?? "ION/05_context/current/codex_solo/HOT_CONTEXT.md")}`,
      `context_packages: ${String(asRecord(solo.active_context).context_packages_path ?? "")}`,
    ]);
    appendCodexCard(parent, "MINI.md snapshot", [asRecord(docs.mini).text ?? "Mini text is not exposed by the current model response."]);
    appendCodexCard(parent, "Mini auto-post", [asRecord(model.mini_auto_post)]);
    appendCodexCard(parent, "Active context package selector", [asRecord(solo.context_packages)]);
    return;
  }
  if (codex.view === "queue") {
    const queue = asRecord(model.codex_queue);
    const runner = asRecord(queue.runner);
    const serviceConsole = asRecord(model.service_console);
    appendCodexCard(parent, "Codex queue runner", [
      `verdict: ${String(runner.verdict ?? "unknown")}`,
      `queued_request_count: ${String(runner.queued_request_count ?? "")}`,
      `active_process_running: ${String(runner.active_process_running ?? "")}`,
      `next_request_path: ${String(runner.next_request_path ?? "")}`,
      `work_queue_path: ${String(queue.work_queue_path ?? "")}`,
    ]);
    appendCodexCard(parent, "Operator service alerts visible to AI", [
      `verdict: ${String(serviceConsole.verdict ?? "unknown")}`,
      `headline: ${String(serviceConsole.headline ?? "")}`,
      `required_issue_count: ${String(serviceConsole.required_issue_count ?? "")}`,
      `warning_count: ${String(serviceConsole.warning_count ?? "")}`,
      shortJson(asArray(serviceConsole.services), 1400),
    ]);
    appendCodexCard(parent, "Latest work requests", asArray(queue.latest_work_requests).slice(0, 5));
    appendCodexCard(parent, "Latest task returns", asArray(queue.latest_task_returns).slice(0, 5));
    appendCodexCard(parent, "Response runs", [asRecord(model.response_runs)]);
    return;
  }
  appendCodexCard(parent, "Current turn context mount", [
    `turn_id: ${String(latest?.turn_id ?? "")}`,
    `response_mode: ${String(latestEngine.response_mode ?? latest?.kind ?? "")}`,
    `context_mount: ${shortJson(contextMount, 1200)}`,
  ]);
  appendCodexCard(parent, "Context refs visible to this chat", asArray(contextMount.context_refs).length ? asArray(contextMount.context_refs) : latest?.context_refs ?? []);
  appendCodexCard(parent, "Skill, lenses, and model move", [
    `skill_activation:\n${shortJson(latest?.skill_activation ?? latestEngine.skill_activation, 900)}`,
    `native_lenses:\n${shortJson(latestEngine.native_lenses, 900)}`,
    `model_move:\n${shortJson(latest?.codex_model_move ?? latestEngine.model_move, 900)}`,
  ]);
  appendCodexCard(parent, "ION comms adapter", [asRecord(model.ion_comms)]);
  appendCodexCard(parent, "HOT_CONTEXT.md snapshot", [asRecord(docs.hot_context).text ?? "Hot context text is not exposed by the current model response."]);
}

function renderCodexPanel(panel = ensurePanel()): void {
  const codex = bridgeState.codex as CodexChatState;
  const statusNode = panel.querySelector<HTMLElement>('[data-codex="status"]');
  const turnsNode = panel.querySelector<HTMLElement>('[data-codex="turns"]');
  const contextNode = panel.querySelector<HTMLElement>('[data-codex="context"]');
  const inputNode = panel.querySelector<HTMLTextAreaElement>('[data-codex="input"]');
  panel.querySelectorAll<HTMLElement>("[data-codex-view]").forEach((button) => {
    button.dataset.active = String(button.dataset.codexView === codex.view);
  });
  if (statusNode) {
    statusNode.textContent = [
      codex.status,
      codex.submitting ? "Codex response pending..." : "",
      codex.queueing ? "Queue request pending..." : "",
    ].filter(Boolean).join("\n");
  }
  if (inputNode && document.activeElement !== inputNode) inputNode.value = codex.input;
  if (contextNode) {
    contextNode.style.display = codex.view === "history" ? "none" : "grid";
    if (codex.view !== "history") renderCodexContextView(contextNode, codex);
  }
  if (!turnsNode) return;
  turnsNode.style.display = codex.view === "history" ? "grid" : "none";
  if (codex.view !== "history") return;
  turnsNode.innerHTML = "";
  const turns = codex.turns.slice(-10);
  if (!turns.length) {
    const empty = document.createElement("div");
    empty.className = "ion-codex-turn";
    empty.textContent = "No Codex chat turns loaded yet. Use Refresh.";
    turnsNode.appendChild(empty);
    return;
  }
  turns.forEach((turn) => {
    const row = document.createElement("article");
    const author = String(turn.author || turn.kind || "codex");
    row.className = "ion-codex-turn";
    row.dataset.author = author;
    const label = document.createElement("b");
    label.textContent = `${author}${turn.created_at ? ` · ${turn.created_at}` : ""}`;
    const body = document.createElement("div");
    body.textContent = String(turn.message || "");
    row.append(label, body);
    turnsNode.appendChild(row);
  });
}

function renderDocsPanel(panel = ensurePanel()): void {
  const docs = bridgeState.docs as DocsBrowserState;
  const favoritesNode = panel.querySelector<HTMLElement>('[data-docs="favorites"]');
  const rootList = panel.querySelector<HTMLElement>('[data-docs="roots"]');
  const breadcrumbNode = panel.querySelector<HTMLElement>('[data-docs="breadcrumbs"]');
  const entriesNode = panel.querySelector<HTMLElement>('[data-docs="entries"]');
  const statusNode = panel.querySelector<HTMLElement>('[data-docs="status"]');
  const searchNode = panel.querySelector<HTMLInputElement>('[data-docs-control="search"]');
  const treeNode = panel.querySelector<HTMLSelectElement>('[data-docs="tree"]');

  if (favoritesNode) {
    favoritesNode.innerHTML = "";
    for (const favorite of docsFavoriteRoots) {
      const tile = document.createElement("button");
      tile.type = "button";
      tile.className = "ion-docs-favorite";
      tile.dataset.docRoot = favorite.path;
      tile.dataset.docLabel = favorite.label;
      if (docs.currentRoot === favorite.path) tile.dataset.selected = "true";
      const thumb = document.createElement("span");
      thumb.className = "ion-docs-favorite-thumb";
      thumb.style.background = `linear-gradient(160deg, ${favorite.accent}33, ${favorite.accent}11)`;
      thumb.textContent = favorite.icon;
      const copy = document.createElement("span");
      copy.className = "ion-docs-favorite-copy";
      const title = document.createElement("span");
      title.className = "ion-docs-name";
      title.textContent = favorite.label;
      const path = document.createElement("span");
      path.className = "ion-docs-meta";
      path.textContent = favorite.status || favorite.path;
      copy.append(title, path);
      const actions = document.createElement("span");
      actions.className = "ion-docs-favorite-actions";
      [
        ["drop", "⇪", "Zip and drop"],
        ["open", "↗", "Open"],
        ["remove", "×", "Hide favorite"],
        ["more", "…", "More"],
      ].forEach(([kind, glyph, label]) => {
        const action = document.createElement("button");
        action.type = "button";
        action.className = "ion-docs-favorite-action";
        action.dataset.docFavAction = kind;
        action.dataset.docRoot = favorite.path;
        action.dataset.docLabel = favorite.label;
        action.textContent = glyph;
        action.title = label;
        actions.appendChild(action);
      });
      tile.append(thumb, copy, actions);
      favoritesNode.appendChild(tile);
    }
  }
  if (rootList) {
    const roots = docs.roots.length ? docs.roots : docsFavoriteRoots.map((entry) => entry.path);
    rootList.innerHTML = "";
    for (const root of roots) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "ion-tool";
      button.dataset.docRoot = root;
      button.textContent = root;
      rootList.appendChild(button);
    }
  }
  if (breadcrumbNode) {
    const crumbPath = docs.breadcrumbs.length ? docs.breadcrumbs.join(" / ") : "Home";
    breadcrumbNode.textContent = crumbPath;
  }
  if (searchNode) searchNode.value = docs.query;
  if (treeNode) {
    const currentTreeValue = treeNode.value;
    treeNode.innerHTML = "";
    const optionGroups = new Map<string, HTMLOptGroupElement>();
    let homeFound = false;
    for (const option of DOCS_TREE_OPTIONS) {
      const opt = document.createElement("option");
      opt.value = option.value;
      opt.textContent = option.label;
      if (option.value === currentTreeValue) homeFound = true;
      if (option.group) {
        opt.textContent = option.value ? `— ${option.label}` : option.label;
      }
      if (!option.group) {
        treeNode.appendChild(opt);
        continue;
      }
      let optGroup = optionGroups.get(option.group);
      if (!optGroup) {
        optGroup = document.createElement("optgroup");
        optGroup.label = option.group;
        optGroup.dataset.docTreeGroup = option.group;
        treeNode.appendChild(optGroup);
        optionGroups.set(option.group, optGroup);
      }
      optGroup.appendChild(opt);
    }
    if (currentTreeValue && homeFound) treeNode.value = currentTreeValue;
    if (!homeFound) {
      treeNode.value = docs.currentRoot ?? "";
    }
  }
  if (entriesNode) {
    entriesNode.dataset.currentPath = docs.currentPath;
    entriesNode.innerHTML = "";
    for (const entry of docs.entries) {
      const row = document.createElement("div");
      row.className = "ion-docs-entry";
      row.dataset.docKind = entry.kind;
      row.dataset.docPath = entry.path;
      if (entry.name === docs.selectedDocName || entry.path === docs.selectedPath) row.dataset.selected = "true";
      row.dataset.docName = entry.name;
      row.textContent = "";
      row.draggable = true;
      const thumbnail = document.createElement("span");
      thumbnail.className = "ion-docs-thumbnail";
      thumbnail.textContent = entry.thumbnail ?? entry.name.slice(0, 2).toUpperCase();
      const title = document.createElement("span");
      title.className = "ion-docs-name";
      title.textContent = entry.name;
      const meta = document.createElement("span");
      meta.className = "ion-docs-meta";
      meta.textContent = entry.size_bytes ? `${Math.round(entry.size_bytes / 1024)} KB` : "";
      row.append(thumbnail, title, meta);
      entriesNode.appendChild(row);
    }
    if (!docs.entries.length) {
      const empty = document.createElement("div");
      empty.className = "ion-docs-entry";
      empty.textContent = "No docs found. Use Search or Home.";
      entriesNode.appendChild(empty);
    }
  }
  if (statusNode) statusNode.textContent = [docs.status || docsStateSummary(), "Drag a doc tile into ChatGPT to auto-zip and drop."].join("\n");
}

function renderMessageQueuePanel(panel = ensurePanel()): void {
  const queue = bridgeState.messageQueue as MessageQueueState;
  const statusNode = panel.querySelector<HTMLElement>('[data-queue="status"]');
  const inputNode = panel.querySelector<HTMLTextAreaElement>('[data-queue="input"]');
  const allowNode = panel.querySelector<HTMLInputElement>('[data-queue="allow-mid-output"]');
  const readinessNode = panel.querySelector<HTMLElement>('[data-queue="readiness"]');
  const itemsNode = panel.querySelector<HTMLElement>('[data-queue="items"]');
  const pauseButton = panel.querySelector<HTMLElement>('[data-tool="queue-pause"]');
  if (statusNode) statusNode.textContent = queue.status;
  if (inputNode && document.activeElement !== inputNode) inputNode.value = queue.input;
  if (allowNode) allowNode.checked = queue.allowMidOutput;
  if (readinessNode) {
    readinessNode.textContent = [
      queue.activeOutput ? "output: active" : "output: idle",
      queue.sendAvailable ? "send: available" : "send: locked",
      queue.paused ? "queue: paused" : "queue: armed",
    ].join(" · ");
  }
  if (pauseButton) pauseButton.textContent = queue.paused ? "Resume" : "Pause";
  if (!itemsNode) return;
  itemsNode.innerHTML = "";
  const items = queue.items.slice(-18);
  if (!items.length) {
    const empty = document.createElement("div");
    empty.className = "ion-detail";
    empty.textContent = "No queued messages.";
    itemsNode.appendChild(empty);
    return;
  }
  for (const item of items) {
    const row = document.createElement("article");
    row.className = "ion-queue-item";
    row.dataset.status = item.status;
    const chip = document.createElement("span");
    chip.className = "ion-queue-status-chip";
    chip.textContent = item.status;
    const copy = document.createElement("div");
    copy.className = "ion-queue-copy";
    copy.textContent = [item.text, item.detail ? `\n${item.detail}` : ""].join("");
    row.append(chip, copy);
    itemsNode.appendChild(row);
  }
}

function renderProjectsPanel(panel = ensurePanel()): void {
  const projects = bridgeState.projects as ProjectsState;
  const statusNode = panel.querySelector<HTMLElement>('[data-projects="status"]');
  const gridNode = panel.querySelector<HTMLElement>('[data-projects="grid"]');
  if (statusNode) {
    statusNode.textContent = [
      projects.status,
      projects.roots.length ? `roots: ${projects.roots.join(", ")}` : "roots: not scanned yet",
      projects.selectedPath ? `selected: ${projects.selectedPath}` : "selected: none",
      projects.selectedPaths.length ? `context_sync_selected: ${projects.selectedPaths.length}` : "context_sync_selected: none",
    ].join("\n");
  }
  if (!gridNode) return;
  gridNode.innerHTML = "";
  if (!projects.packages.length) {
    const empty = document.createElement("div");
    empty.className = "ion-detail";
    empty.textContent = "No ION context packages discovered yet. Use Refresh Projects.";
    gridNode.appendChild(empty);
    return;
  }
  for (const entry of projects.packages) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "ion-project-card";
    card.dataset.projectPath = entry.path;
    card.dataset.selected = String(entry.path === projects.selectedPath || projects.selectedPaths.includes(entry.path));
    const title = document.createElement("div");
    title.className = "ion-project-title";
    title.textContent = entry.project;
    const version = document.createElement("div");
    version.className = "ion-project-meta";
    version.textContent = `latest: ${entry.version || "unversioned"} · ${entry.kind}`;
    const name = document.createElement("div");
    name.className = "ion-project-meta";
    name.textContent = entry.name;
    const root = document.createElement("div");
    root.className = "ion-project-meta";
    root.textContent = entry.root;
    card.append(title, version, name, root);
    gridNode.appendChild(card);
  }
}

function contextSyncActionButton(action: string, label: string, disabled = false): HTMLButtonElement {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "ion-tool";
  button.dataset.contextSyncAction = action;
  button.textContent = label;
  button.disabled = disabled;
  return button;
}

function renderContextSyncTopMenu(panel = ensurePanel()): void {
  const projects = bridgeState.projects as ProjectsState;
  const knownPaths = new Set(projects.packages.map((entry) => entry.path));
  const selectedPaths = (projects.selectedPaths ?? []).filter((path) => !knownPaths.size || knownPaths.has(path));
  const selectedCount = selectedPaths.length;
  const syncReady = Boolean(projects.contextSyncZipPath);
  panel.dataset.contextSyncOpen = String(Boolean(projects.contextSyncOpen));
  const button = panel.querySelector<HTMLElement>('[data-tool="context-sync-toggle"]');
  const label = panel.querySelector<HTMLElement>("[data-context-sync-label]");
  const menu = panel.querySelector<HTMLElement>("[data-context-sync-menu]");
  if (button) {
    button.dataset.contextSyncState = syncReady ? "ready" : selectedCount ? "selected" : "idle";
    button.setAttribute("aria-expanded", String(Boolean(projects.contextSyncOpen)));
    button.title = [
      "Select ION project context packages and build one approved sync ZIP.",
      selectedCount ? `selected_projects: ${selectedCount}` : "selected_projects: none",
      projects.contextSyncZipPath ? `latest_zip: ${projects.contextSyncZipPath}` : "",
      projects.contextSyncSha256 ? `sha256: ${projects.contextSyncSha256}` : "",
      "Authority: context sync only; no production, live execution, mutation, or secrets authority.",
    ].filter(Boolean).join("\n");
  }
  if (label) {
    label.textContent = selectedCount ? `Sync ${selectedCount}` : syncReady ? "Context Synced" : "Context Sync";
  }
  if (!menu) return;
  menu.innerHTML = "";

  const head = document.createElement("div");
  head.className = "ion-context-sync-head";
  const title = document.createElement("div");
  title.className = "ion-context-sync-title";
  title.textContent = "Project Context Sync";
  const status = document.createElement("div");
  status.className = "ion-context-sync-status";
  status.textContent = [
    projects.contextSyncStatus || projects.status || "Select current project packages to compile into one browser sync ZIP.",
    projects.contextSyncZipPath ? `zip: ${projects.contextSyncZipPath}` : "",
    projects.contextSyncSha256 ? `sha256: ${projects.contextSyncSha256}` : "",
  ].filter(Boolean).join("\n");
  head.append(title, status);

  const list = document.createElement("div");
  list.className = "ion-context-sync-list";
  if (!projects.packages.length) {
    const empty = document.createElement("div");
    empty.className = "ion-detail";
    empty.textContent = "No current project packages loaded yet. Refresh scans the governed ION context package roots.";
    list.appendChild(empty);
  } else {
    for (const entry of projects.packages) {
      const row = document.createElement("label");
      row.className = "ion-context-sync-row";
      row.dataset.selected = String(selectedPaths.includes(entry.path));
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = selectedPaths.includes(entry.path);
      checkbox.dataset.contextSyncPath = entry.path;
      const copy = document.createElement("span");
      copy.className = "ion-context-sync-copy";
      const name = document.createElement("span");
      name.className = "ion-context-sync-name";
      name.textContent = entry.project;
      const meta = document.createElement("span");
      meta.className = "ion-context-sync-meta";
      meta.textContent = `${entry.version || "unversioned"} · ${entry.kind} · ${entry.path}`;
      copy.append(name, meta);
      row.append(checkbox, copy);
      list.appendChild(row);
    }
  }

  const actions = document.createElement("div");
  actions.className = "ion-context-sync-actions";
  actions.append(
    contextSyncActionButton("build", "Build ZIP", selectedCount === 0),
    contextSyncActionButton("refresh", "Refresh"),
    contextSyncActionButton("select-all", "Select All", projects.packages.length === 0),
    contextSyncActionButton("clear", "Clear", selectedCount === 0),
    contextSyncActionButton("open-projects", "Projects"),
  );
  menu.append(head, list, actions);
}

function promptLibraryCategories(items: PromptLibraryItem[]): string[] {
  return Array.from(new Set(items.map((item) => item.category || "General"))).sort((a, b) => a.localeCompare(b));
}

function filteredPromptLibraryItems(state = bridgeState.promptLibrary as PromptLibraryState): PromptLibraryItem[] {
  const query = state.query.trim().toLowerCase();
  return state.items
    .filter((item) => state.category === "all" || item.category === state.category)
    .filter((item) => {
      if (!query) return true;
      return `${item.title} ${item.category} ${item.tags.join(" ")} ${item.text}`.toLowerCase().includes(query);
    })
    .sort((a, b) => Number(b.pinned) - Number(a.pinned) || b.usageCount - a.usageCount || a.title.localeCompare(b.title));
}

function selectPromptLibraryItem(id: string): void {
  const state = bridgeState.promptLibrary as PromptLibraryState;
  const item = state.items.find((candidate) => candidate.id === id);
  if (!item) return;
  setBridgePromptLibraryState({
    selectedId: item.id,
    draftTitle: item.title,
    draftCategory: item.category,
    draftTags: item.tags.join(", "),
    draftText: item.text,
    status: `Selected prompt: ${item.title}`,
  });
}

function promptDraftItem(existing?: PromptLibraryItem): PromptLibraryItem {
  const state = bridgeState.promptLibrary as PromptLibraryState;
  const title = state.draftTitle.trim() || "Untitled prompt";
  return {
    id: existing?.id || `prompt-${Date.now()}-${Math.random().toString(16).slice(2)}`,
    title,
    category: state.draftCategory.trim() || "General",
    tags: state.draftTags.split(",").map((tag) => tag.trim()).filter(Boolean),
    text: state.draftText.trim(),
    pinned: existing?.pinned ?? false,
    updatedAt: new Date().toISOString(),
    usageCount: existing?.usageCount ?? 0,
    origin: existing?.origin === "built_in" ? "built_in" : "custom",
  };
}

function savePromptLibraryDraft(): void {
  const state = bridgeState.promptLibrary as PromptLibraryState;
  if (!state.draftText.trim()) {
    setBridgePromptLibraryState({ status: "Prompt text is empty. Nothing saved." });
    return;
  }
  const existing = state.items.find((item) => item.id === state.selectedId);
  const nextItem = promptDraftItem(existing);
  const items = existing
    ? state.items.map((item) => item.id === existing.id ? nextItem : item)
    : [nextItem, ...state.items];
  writePromptLibraryItems(items);
  setBridgePromptLibraryState({
    items,
    selectedId: nextItem.id,
    draftTitle: nextItem.title,
    draftCategory: nextItem.category,
    draftTags: nextItem.tags.join(", "),
    draftText: nextItem.text,
    status: `Saved prompt: ${nextItem.title}`,
  });
}

function togglePromptPinned(): void {
  const state = bridgeState.promptLibrary as PromptLibraryState;
  const items = state.items.map((item) => item.id === state.selectedId ? { ...item, pinned: !item.pinned, updatedAt: new Date().toISOString() } : item);
  writePromptLibraryItems(items);
  setBridgePromptLibraryState({ items, status: "Prompt pin state updated." });
}

function deleteSelectedPrompt(): void {
  const state = bridgeState.promptLibrary as PromptLibraryState;
  const items = state.items.filter((item) => item.id !== state.selectedId);
  writePromptLibraryItems(items);
  const selected = items[0];
  setBridgePromptLibraryState({
    items,
    selectedId: selected?.id ?? "",
    draftTitle: selected?.title ?? "",
    draftCategory: selected?.category ?? "General",
    draftTags: selected?.tags.join(", ") ?? "",
    draftText: selected?.text ?? "",
    status: "Prompt deleted.",
  });
}

function markPromptUsed(id: string, status: string): void {
  if (!id) {
    setBridgePromptLibraryState({ status });
    return;
  }
  const state = bridgeState.promptLibrary as PromptLibraryState;
  const items = state.items.map((item) => item.id === id ? { ...item, usageCount: item.usageCount + 1, updatedAt: new Date().toISOString() } : item);
  writePromptLibraryItems(items);
  setBridgePromptLibraryState({ items, status });
}

function normalizeQueuePackPath(path: string): string {
  return path.replace(/\\/g, "/").replace(/^\/+/, "").split("/").filter((part) => part && part !== "." && part !== "..").join("/");
}

function queuePackLine(value: unknown): string {
  return String(value ?? "").replace(/\s+/g, " ").trim().slice(0, 180);
}

function queuePackTitle(pack: QueuePackManifest): string {
  return queuePackLine(pack.title || pack.pack_id || "ION queue pack");
}

function queuePackStepText(step: QueuePackStep, textEntries: Map<string, string>): string {
  const direct = String(step.prompt ?? step.text ?? "").trim();
  if (direct) return direct;
  const ref = normalizeQueuePackPath(String(step.prompt_ref ?? ""));
  if (!ref) return "";
  return String(textEntries.get(ref) ?? "").trim();
}

function collectQueuePackSteps(pack: QueuePackManifest): Array<{ workflow?: QueuePackWorkflow; chain?: QueuePackChain; step: QueuePackStep }> {
  const entries: Array<{ workflow?: QueuePackWorkflow; chain?: QueuePackChain; step: QueuePackStep }> = [];
  const addSteps = (steps: QueuePackStep[] | undefined, workflow?: QueuePackWorkflow, chain?: QueuePackChain) => {
    for (const step of steps ?? []) entries.push({ workflow, chain, step });
  };
  for (const workflow of pack.workflows ?? []) {
    if (workflow.chains?.length) {
      for (const chain of workflow.chains) addSteps(chain.steps, workflow, chain);
    }
    addSteps(workflow.steps, workflow);
  }
  for (const chain of pack.chains ?? []) addSteps(chain.steps, undefined, chain);
  addSteps(pack.steps);
  addSteps(pack.prompts);
  addSteps(pack.queue);
  return entries;
}

function queuePackStepHeader(pack: QueuePackManifest, entry: { workflow?: QueuePackWorkflow; chain?: QueuePackChain; step: QueuePackStep }, index: number, total: number): string {
  const lines = [
    "ION_QUEUE_PACK_STEP",
    `pack: ${queuePackTitle(pack)}`,
    pack.objective ? `objective: ${queuePackLine(pack.objective)}` : "",
    entry.workflow?.title || entry.workflow?.id ? `workflow: ${queuePackLine(entry.workflow.title || entry.workflow.id)}` : "",
    entry.chain?.title || entry.chain?.id ? `chain: ${queuePackLine(entry.chain.title || entry.chain.id)}` : "",
    `step: ${index + 1}/${total}`,
    entry.step.title || entry.step.id ? `title: ${queuePackLine(entry.step.title || entry.step.id)}` : "",
    entry.step.tags?.length ? `tags: ${entry.step.tags.map(queuePackLine).filter(Boolean).join(", ")}` : "",
  ].filter(Boolean);
  return `${lines.join("\n")}\n`;
}

function queuePackMessages(pack: QueuePackManifest, textEntries = new Map<string, string>()): string[] {
  if (pack.schema_id !== QUEUE_PACK_SCHEMA_ID) {
    throw new Error(`Queue pack schema must be ${QUEUE_PACK_SCHEMA_ID}.`);
  }
  const entries = collectQueuePackSteps(pack);
  const includeHeaders = pack.queue_behavior?.include_step_headers !== false;
  const messages: string[] = [];
  for (let index = 0; index < entries.length && messages.length < QUEUE_PACK_MAX_MESSAGES; index += 1) {
    const entry = entries[index];
    const body = queuePackStepText(entry.step, textEntries).slice(0, QUEUE_PACK_MAX_PROMPT_CHARS).trim();
    if (!body) continue;
    messages.push(includeHeaders ? `${queuePackStepHeader(pack, entry, index, entries.length)}\n${body}` : body);
  }
  if (!messages.length) throw new Error("Queue pack did not contain any prompt text.");
  return messages;
}

function parseQueuePackJson(text: string, textEntries = new Map<string, string>()): QueuePackImportResult {
  const pack = JSON.parse(text) as QueuePackManifest;
  const messages = queuePackMessages(pack, textEntries);
  const truncated = collectQueuePackSteps(pack).length > messages.length ? ` Loaded first ${messages.length} bounded steps.` : "";
  const autoplayNote = pack.queue_behavior?.auto_play_requested ? " Auto Play was requested by the pack, but manual start remains required." : "";
  return {
    pack,
    messages,
    status: `Imported ${messages.length} prompt(s) from ${queuePackTitle(pack)}.${truncated}${autoplayNote}`,
  };
}

function findZipEndOfCentralDirectory(view: DataView): number {
  const min = Math.max(0, view.byteLength - 66000);
  for (let offset = view.byteLength - 22; offset >= min; offset -= 1) {
    if (view.getUint32(offset, true) === 0x06054b50) return offset;
  }
  return -1;
}

async function inflateZipPayload(payload: ArrayBuffer, method: number): Promise<ArrayBuffer> {
  if (method === 0) return payload;
  if (method !== 8) throw new Error(`Unsupported ZIP compression method ${method}.`);
  const streamCtor = (globalThis as unknown as { DecompressionStream?: new (format: string) => DecompressionStream }).DecompressionStream;
  if (!streamCtor) throw new Error("This browser cannot decompress ZIP entries.");
  for (const format of ["deflate-raw", "deflate"]) {
    try {
      const stream = new Blob([payload]).stream().pipeThrough(new streamCtor(format));
      return await new Response(stream).arrayBuffer();
    } catch {
      // Try the next supported stream format.
    }
  }
  throw new Error("ZIP entry decompression failed.");
}

async function readQueuePackZipTextEntries(buffer: ArrayBuffer): Promise<Map<string, string>> {
  const view = new DataView(buffer);
  const eocd = findZipEndOfCentralDirectory(view);
  if (eocd < 0) throw new Error("ZIP manifest not found.");
  const entryCount = view.getUint16(eocd + 10, true);
  let cursor = view.getUint32(eocd + 16, true);
  const decoder = new TextDecoder();
  const entries: Array<{ name: string; method: number; compressedSize: number; uncompressedSize: number; localOffset: number }> = [];
  for (let index = 0; index < entryCount && cursor < view.byteLength; index += 1) {
    if (view.getUint32(cursor, true) !== 0x02014b50) break;
    const method = view.getUint16(cursor + 10, true);
    const compressedSize = view.getUint32(cursor + 20, true);
    const uncompressedSize = view.getUint32(cursor + 24, true);
    const nameLength = view.getUint16(cursor + 28, true);
    const extraLength = view.getUint16(cursor + 30, true);
    const commentLength = view.getUint16(cursor + 32, true);
    const localOffset = view.getUint32(cursor + 42, true);
    const name = normalizeQueuePackPath(decoder.decode(buffer.slice(cursor + 46, cursor + 46 + nameLength)));
    if (
      name &&
      /\.(json|md|txt)$/i.test(name) &&
      uncompressedSize <= QUEUE_PACK_MAX_TEXT_ENTRY_BYTES &&
      !name.includes("__MACOSX/")
    ) {
      entries.push({ name, method, compressedSize, uncompressedSize, localOffset });
    }
    cursor += 46 + nameLength + extraLength + commentLength;
  }
  const texts = new Map<string, string>();
  for (const entry of entries) {
    if (view.getUint32(entry.localOffset, true) !== 0x04034b50) continue;
    const nameLength = view.getUint16(entry.localOffset + 26, true);
    const extraLength = view.getUint16(entry.localOffset + 28, true);
    const dataStart = entry.localOffset + 30 + nameLength + extraLength;
    const compressed = buffer.slice(dataStart, dataStart + entry.compressedSize);
    const inflated = await inflateZipPayload(compressed, entry.method);
    if (inflated.byteLength <= QUEUE_PACK_MAX_TEXT_ENTRY_BYTES) {
      texts.set(entry.name, decoder.decode(inflated));
    }
  }
  return texts;
}

async function parseQueuePackZip(file: File): Promise<QueuePackImportResult> {
  const texts = await readQueuePackZipTextEntries(await file.arrayBuffer());
  const manifestPath = texts.has(QUEUE_PACK_MANIFEST_NAME)
    ? QUEUE_PACK_MANIFEST_NAME
    : Array.from(texts.keys()).find((path) => path.endsWith(`/${QUEUE_PACK_MANIFEST_NAME}`));
  if (!manifestPath) throw new Error(`ZIP must contain ${QUEUE_PACK_MANIFEST_NAME}.`);
  const manifestBase = manifestPath.slice(0, -QUEUE_PACK_MANIFEST_NAME.length).replace(/\/$/, "");
  const scopedTexts = new Map(texts);
  if (manifestBase) {
    for (const [path, value] of texts.entries()) {
      if (path.startsWith(`${manifestBase}/`)) scopedTexts.set(path.slice(manifestBase.length + 1), value);
    }
  }
  return parseQueuePackJson(String(texts.get(manifestPath) ?? ""), scopedTexts);
}

async function parseQueuePackFile(file: File): Promise<QueuePackImportResult> {
  const lowerName = file.name.toLowerCase();
  if (lowerName.endsWith(".zip") || /zip/i.test(file.type)) return parseQueuePackZip(file);
  return parseQueuePackJson(await file.text());
}

async function importQueuePackFile(file: File): Promise<void> {
  setBridgeMessageQueueState({ status: `Importing queue pack: ${file.name}` });
  try {
    const result = await parseQueuePackFile(file);
    window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-add", {
      detail: {
        messages: result.messages,
        status: result.status,
        source: "pack",
        pack_id: result.pack.pack_id,
        title: result.pack.title,
      },
    }));
    setBridgeMessageQueueState({ status: result.status });
  } catch (error) {
    setBridgeMessageQueueState({ status: `Queue pack import blocked: ${error instanceof Error ? error.message : String(error)}` });
  }
}

export async function importBridgeQueuePackFile(file: File): Promise<void> {
  await importQueuePackFile(file);
}

function dispatchPromptToComposer(mode: "replace" | "append"): void {
  const state = bridgeState.promptLibrary as PromptLibraryState;
  const text = state.draftText.trim();
  if (!text) {
    setBridgePromptLibraryState({ status: "Prompt text is empty." });
    return;
  }
  window.dispatchEvent(new CustomEvent("ion-chatops-prompt-insert", { detail: { text, mode } }));
  markPromptUsed(state.selectedId, mode === "append" ? "Prompt appended to composer." : "Prompt inserted into composer.");
}

function renderPromptLibraryPanel(panel = ensurePanel()): void {
  const state = bridgeState.promptLibrary as PromptLibraryState;
  const statusNode = panel.querySelector<HTMLElement>('[data-prompts="status"]');
  const queryNode = panel.querySelector<HTMLInputElement>('[data-prompts="query"]');
  const categoryNode = panel.querySelector<HTMLSelectElement>('[data-prompts="category"]');
  const listNode = panel.querySelector<HTMLElement>('[data-prompts="list"]');
  const titleNode = panel.querySelector<HTMLInputElement>('[data-prompts="title"]');
  const draftCategoryNode = panel.querySelector<HTMLInputElement>('[data-prompts="draft-category"]');
  const tagsNode = panel.querySelector<HTMLInputElement>('[data-prompts="tags"]');
  const textNode = panel.querySelector<HTMLTextAreaElement>('[data-prompts="text"]');
  if (statusNode) statusNode.textContent = state.status;
  if (queryNode && document.activeElement !== queryNode) queryNode.value = state.query;
  if (categoryNode) {
    const value = categoryNode.value;
    categoryNode.innerHTML = "";
    const all = document.createElement("option");
    all.value = "all";
    all.textContent = "All categories";
    categoryNode.appendChild(all);
    for (const category of promptLibraryCategories(state.items)) {
      const option = document.createElement("option");
      option.value = category;
      option.textContent = category;
      categoryNode.appendChild(option);
    }
    categoryNode.value = state.category || value || "all";
  }
  if (titleNode && document.activeElement !== titleNode) titleNode.value = state.draftTitle;
  if (draftCategoryNode && document.activeElement !== draftCategoryNode) draftCategoryNode.value = state.draftCategory;
  if (tagsNode && document.activeElement !== tagsNode) tagsNode.value = state.draftTags;
  if (textNode && document.activeElement !== textNode) textNode.value = state.draftText;
  if (!listNode) return;
  listNode.innerHTML = "";
  const items = filteredPromptLibraryItems(state);
  if (!items.length) {
    const empty = document.createElement("div");
    empty.className = "ion-detail";
    empty.textContent = "No prompts match the current filters.";
    listNode.appendChild(empty);
    return;
  }
  for (const item of items) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "ion-prompt-card";
    card.dataset.promptId = item.id;
    card.dataset.selected = String(item.id === state.selectedId);
    const title = document.createElement("div");
    title.className = "ion-prompt-title";
    title.textContent = `${item.pinned ? "PIN " : ""}${item.title}`;
    const meta = document.createElement("div");
    meta.className = "ion-prompt-meta";
    meta.textContent = `${item.category} · used ${item.usageCount}`;
    const tags = document.createElement("div");
    tags.className = "ion-prompt-meta";
    tags.textContent = item.tags.join(", ") || item.origin;
    card.append(title, meta, tags);
    listNode.appendChild(card);
  }
}

function compactMetric(value: number): string {
  if (!Number.isFinite(value) || value <= 0) return "0";
  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}m`;
  if (value >= 10000) return `${Math.round(value / 1000)}k`;
  if (value >= 1000) return `${(value / 1000).toFixed(1)}k`;
  return String(Math.round(value));
}

function queueCounts(queue: MessageQueueState): { pending: number; files: number; active: number } {
  const visible = queue.items.filter((item) => item.status !== "sent");
  return {
    pending: visible.length,
    files: visible.filter((item) => item.kind === "files").length,
    active: visible.filter((item) => item.status === "sending" || item.status === "waiting").length,
  };
}

function renderPanel(panel = ensurePanel()): void {
  if (renderingPanel) {
    if (!renderPanelQueued) {
      renderPanelQueued = true;
      window.requestAnimationFrame(() => {
        renderPanelQueued = false;
        renderPanel();
      });
    }
    return;
  }
  renderingPanel = true;
  try {
  panel.dataset.tone = bridgeState.tone;
  const modeMemory = bridgeState.modeMemory as ModeMemoryState;
  panel.dataset.operationalMode = modeMemory.currentMode;
  positionPanelAboveComposer(panel);
  const titleNode = panel.querySelector<HTMLElement>(".ion-title");
  const modeNode = panel.querySelector<HTMLElement>("[data-mode-memory]");
  const modePill = panel.querySelector<HTMLElement>("[data-mode-pill]");
  const modeSummary = panel.querySelector<HTMLElement>("[data-mode-summary]");
  if (titleNode) titleNode.textContent = bridgeState.title;
  if (modeNode) {
    modeNode.title = modeMemoryDetail(modeMemory);
    modeNode.setAttribute("aria-label", `Open ION mode memory: ${modeMemory.currentMode}`);
  }
  if (modePill) modePill.textContent = modeBadgeLabel(modeMemory.currentMode);
  if (modeSummary) modeSummary.textContent = modeMemorySummary(modeMemory);
  const queue = bridgeState.messageQueue as MessageQueueState;
  const onboard = bridgeState.onboard as OnboardSyncInfo;
  const onboardButton = panel.querySelector<HTMLElement>('[data-tool="insert-reentry"]');
  const onboardLabel = panel.querySelector<HTMLElement>("[data-onboard-label]");
  const autoAcceptButton = panel.querySelector<HTMLElement>('[data-tool="gateway-auto-accept"]');
  const autoAcceptLabel = panel.querySelector<HTMLElement>("[data-auto-accept-label]");
  const autoAcceptTimer = panel.querySelector<HTMLElement>("[data-auto-accept-timer]");
  const autoAcceptTtlInput = panel.querySelector<HTMLInputElement>("[data-auto-accept-ttl-input]");
  const autoAcceptActive = queue.autoAcceptActive;
  if (autoAcceptButton) {
    autoAcceptButton.dataset.active = String(autoAcceptActive);
    autoAcceptButton.title = autoAcceptActive
      ? `ION Action auto-accept is on until ${queue.autoAcceptUntil}. Click the timer to change TTL, or toggle the switch to turn off.`
      : `ION Action auto-accept is off. Click the toggle to allow safe browser queue packets for ${Math.round(queue.autoAcceptTtlSeconds / 60)} minutes.`;
  }
  if (autoAcceptLabel) autoAcceptLabel.textContent = autoAcceptActive ? "ON" : "OFF";
  if (autoAcceptTimer) {
    autoAcceptTimer.textContent = autoAcceptActive ? (queue.autoAcceptUntil || "...") : "SET";
  }
  if (autoAcceptTtlInput && !autoAcceptTtlInput.matches(":focus")) {
    autoAcceptTtlInput.value = String(Math.round(queue.autoAcceptTtlSeconds / 60));
  }
  if (onboardButton) {
    onboardButton.dataset.onboardState = onboard.state;
    onboardButton.title = [
      onboard.detail,
      `project: ${onboard.project}`,
      `bridge: ${onboard.bridge}`,
      `protocol: ${onboard.protocolId}`,
      `version: ${onboard.version}`,
      onboard.lastSyncedAt ? `last_synced_at: ${onboard.lastSyncedAt}` : "",
      "Click to insert the latest ION onboarding/re-entry context protocol into ChatGPT.",
    ].filter(Boolean).join("\n");
  }
  if (onboardLabel) {
    onboardLabel.textContent = onboard.state === "synced"
      ? `${onboard.project} v${onboard.version} synced`
      : `${onboard.project} v${onboard.version}`;
  }
  const monitor = bridgeState.monitor as MonitorMetrics;
  const queueSummary = queueCounts(queue);
  const monitorStrip = panel.querySelector<HTMLElement>('[data-monitor="strip"]');
  const monitorMessagesNode = panel.querySelector<HTMLElement>('[data-monitor="messages"]');
  const monitorAssistantNode = panel.querySelector<HTMLElement>('[data-monitor="assistant"]');
  const monitorChatNode = panel.querySelector<HTMLElement>('[data-monitor="chat"]');
  const monitorActionsNode = panel.querySelector<HTMLElement>('[data-monitor="actions"]');
  const monitorQueueNode = panel.querySelector<HTMLElement>('[data-monitor="queue"]');
  const monitorConnectedActionsNode = panel.querySelector<HTMLElement>('[data-monitor="connected-actions"]');
  const monitorConnectedNode = panel.querySelector<HTMLElement>('[data-monitor="connected"]');
  const monitorSourcesNode = panel.querySelector<HTMLElement>('[data-monitor="sources"]');
  const monitorAttachmentNode = panel.querySelector<HTMLElement>('[data-monitor="attachments"]');
  const monitorLagNode = panel.querySelector<HTMLElement>('[data-monitor="lag"]');
  const monitorDomNode = panel.querySelector<HTMLElement>('[data-monitor="dom"]');
  if (monitorStrip) {
    monitorStrip.dataset.tone = monitor.tone;
    monitorStrip.title = monitor.summary;
  }
  if (monitorMessagesNode) {
    monitorMessagesNode.textContent = `Msgs A${compactMetric(monitor.assistantMessageCount)} U${compactMetric(monitor.userMessageCount)}`;
    monitorMessagesNode.title = `${monitor.messageCount.toLocaleString()} visible conversation item(s): ${monitor.assistantMessageCount.toLocaleString()} assistant, ${monitor.userMessageCount.toLocaleString()} user. Counts are loaded DOM only.`;
  }
  if (monitorAssistantNode) {
    monitorAssistantNode.textContent = `AI ${compactMetric(monitor.assistantMessageCount)} msgs`;
    monitorAssistantNode.title = `Assistant-visible messages in DOM: ${monitor.assistantMessageCount.toLocaleString()}`;
  }
  if (monitorChatNode) {
    monitorChatNode.textContent = `Loaded ${compactMetric(monitor.estimatedTokens)} tok · ${monitor.plusPercent}%/32k ref`;
    monitorChatNode.title = `Loaded browser transcript estimate, not exact model context: ${monitor.estimatedTokens.toLocaleString()} tokens · 128k reference: ${monitor.proPercent}% · 256k reference: ${monitor.thinkingPercent}%`;
  }
  if (monitorActionsNode) {
    monitorActionsNode.textContent = `Actions ${compactMetric(monitor.actionCandidateCount)}`;
    monitorActionsNode.title = `ION action/code scan: ${monitor.validActionCount} valid · ${monitor.blockedActionCount} blocked · ${monitor.duplicateActionCount} duplicate · ${monitor.codeBlockCount} code block(s).`;
  }
  if (monitorConnectedActionsNode) {
    const connectedCandidates = monitor.validActionCount + monitor.blockedActionCount + monitor.duplicateActionCount;
    monitorConnectedActionsNode.textContent = `ConnActs ${compactMetric(connectedCandidates)}`;
    monitorConnectedActionsNode.title = `Action candidates detected from connected sources: ${connectedCandidates} total (valid ${monitor.validActionCount}, blocked ${monitor.blockedActionCount}, duplicate ${monitor.duplicateActionCount}).`;
  }
  if (monitorQueueNode) {
    monitorQueueNode.textContent = `Queue ${compactMetric(queueSummary.pending)}${queueSummary.files ? ` · F${queueSummary.files}` : ""}`;
    monitorQueueNode.title = `${queueSummary.pending} unsent queue item(s), ${queueSummary.files} file item(s), ${queueSummary.active} waiting/sending. Paused: ${queue.paused}. Send available: ${queue.sendAvailable}.`;
  }
  if (monitorConnectedNode) {
    const send = queue.sendAvailable ? "send" : queue.activeOutput ? "output" : "nosend";
    monitorConnectedNode.textContent = `Conn ${send} · src ${compactMetric(monitor.selectedSourceCount)}`;
    monitorConnectedNode.title = `Connected surfaces: send_available=${queue.sendAvailable}, active_output=${queue.activeOutput}, composer_controls=${monitor.composerControlCount}, source_chips=${monitor.selectedSourceCount}, uploaded_attachments=${monitor.uploadedAttachmentCount}.`;
  }
  if (monitorSourcesNode) {
    monitorSourcesNode.textContent = `Sources ${compactMetric(monitor.selectedSourceCount)}`;
    monitorSourcesNode.title = `Connector/source chips detected: ${monitor.selectedSourceCount.toLocaleString()}.`;
  }
  if (monitorAttachmentNode) {
    monitorAttachmentNode.textContent = `Attach ${compactMetric(monitor.uploadedAttachmentCount)}`;
    monitorAttachmentNode.title = `Uploaded attachment nodes detected near composer: ${monitor.uploadedAttachmentCount.toLocaleString()}.`;
  }
  if (monitorLagNode) {
    monitorLagNode.textContent = `Lag ${Math.round(Math.max(monitor.lagMs, monitor.longTaskMs))}ms`;
    monitorLagNode.title = `Event-loop lag: ${Math.round(monitor.lagMs)}ms · Long task: ${Math.round(monitor.longTaskMs)}ms`;
  }
  if (monitorDomNode) {
    monitorDomNode.textContent = `DOM ${compactMetric(monitor.domNodes)}`;
    monitorDomNode.title = `${monitor.domNodes.toLocaleString()} DOM elements loaded in this page`;
  }
  const activeTab = panel.dataset.tab ?? "status";
  panel.querySelectorAll<HTMLElement>(".ion-tab").forEach((tab) => {
    tab.dataset.active = String(tab.dataset.tab === activeTab);
  });
  panel.querySelectorAll<HTMLElement>(".ion-tab-panel").forEach((tabPanel) => {
    tabPanel.dataset.active = String(tabPanel.dataset.panel === activeTab);
  });
  syncSettingsMode(panel);
  syncSettingsControlPadState(panel);
  const layoutTarget = readLayoutTarget();
  panel.querySelectorAll<HTMLElement>("#" + PANEL_ID + " [data-tool^='settings-target-'], #" + SETTINGS_CONTROL_PAD_ID + " [data-tool^='settings-target-']").forEach(
    (button) => {
    const tool = button.dataset.tool ?? "";
    const target = tool.endsWith("top") ? "top_rail" : tool.endsWith("drawer") ? "drawer" : "tabs";
    button.dataset.active = String(target === layoutTarget);
  });
  const statusNode = panel.querySelector<HTMLElement>('[data-field="status"]');
  const actionNode = panel.querySelector<HTMLElement>('[data-field="action"]');
  const agentNode = panel.querySelector<HTMLElement>('[data-field="agent"]');
  const packagesNode = panel.querySelector<HTMLElement>('[data-field="packages"]');
  const sandboxNode = panel.querySelector<HTMLElement>('[data-field="sandbox"]');
  const automationNode = panel.querySelector<HTMLElement>('[data-field="automation"]');
  const artifactsNode = panel.querySelector<HTMLElement>('[data-field="artifacts"]');
  const settingsNode = panel.querySelector<HTMLElement>('[data-field="settings"]');
  const inspectorSelect = panel.querySelector<HTMLSelectElement>('[data-control="settings-inspector-layer"]');
  const diagnosticsNode = panel.querySelector<HTMLElement>('[data-field="diagnostics"]');
  const toolsNode = panel.querySelector<HTMLElement>('[data-field="tools"]');
  renderContextSyncTopMenu(panel);
  renderCodexPanel(panel);
  renderDocsPanel(panel);
  renderMessageQueuePanel(panel);
  renderProjectsPanel(panel);
  renderPromptLibraryPanel(panel);
  if (statusNode) statusNode.textContent = `${bridgeState.detail || "No status detail."}\n\n${modeMemoryDetail(modeMemory)}`;
  if (actionNode) actionNode.textContent = bridgeState.action;
  if (agentNode) agentNode.textContent = bridgeState.agent;
  if (packagesNode) packagesNode.textContent = bridgeState.packages;
  if (sandboxNode) sandboxNode.textContent = bridgeState.sandbox;
  if (automationNode) automationNode.textContent = bridgeState.automation;
  if (artifactsNode) artifactsNode.textContent = bridgeState.artifacts;
  if (settingsNode) settingsNode.textContent = `${bridgeState.settings}\n\n${settingsSummary()}`;
  if (inspectorSelect) {
    const layers = bridgeState.inspectorLayers;
    inspectorSelect.innerHTML = "";
    if (!layers.length) {
      const option = document.createElement("option");
      option.value = "0";
      option.textContent = "No pixel stack captured yet";
      inspectorSelect.appendChild(option);
      inspectorSelect.disabled = true;
    } else {
      inspectorSelect.disabled = false;
      layers.forEach((layer) => {
        const option = document.createElement("option");
        option.value = String(layer.index);
        option.textContent = `${layer.index}: ${layer.label}`;
        option.title = layer.selector;
        option.selected = layer.index === bridgeState.inspectorSelectedIndex;
        inspectorSelect.appendChild(option);
      });
    }
  }
  if (diagnosticsNode) {
    const onboardDetail = [
      "ION onboard context protocol",
      `project: ${onboard.project}`,
      `bridge: ${onboard.bridge}`,
      `protocol_id: ${onboard.protocolId}`,
      `version: ${onboard.version}`,
      `state: ${onboard.state}`,
      onboard.lastSyncedAt ? `last_synced_at: ${onboard.lastSyncedAt}` : "last_synced_at: not clicked in this browser profile",
      onboard.detail,
    ].join("\n");
    diagnosticsNode.textContent = `${monitor.detail}\n\n${onboardDetail}\n\n${bridgeState.anchor.detail}\n\n${bridgeState.diagnostics}`;
  }
  if (toolsNode) toolsNode.textContent = `${bridgeState.tools}\n\nRecent:\n${bridgeState.logs.join("\n") || "No events yet."}`;
  } finally {
    renderingPanel = false;
  }
}

function positionPanelAboveComposer(panel = ensurePanel()): void {
  const anchor = detectComposerAnchor();
  bridgeState.anchor = anchor;
  applyTopRailLayout(panel);
  if (!applyComposerLayout(panel, anchor)) applyTopBarLayout(panel);
  applyBottomMonitorLayout(panel, anchor);
}

function visibleTopRect(element: HTMLElement): DOMRect | null {
  if (element.closest(`#${PANEL_ID}`) || element.closest(`#${MODAL_ID}`)) return null;
  const rect = element.getBoundingClientRect();
  if (rect.width < 8 || rect.height < 8) return null;
  if (rect.bottom < 0 || rect.top > 72) return null;
  const style = window.getComputedStyle(element);
  if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) return null;
  return rect;
}

function findChatGptTopRect(match: (text: string) => boolean): DOMRect | null {
  const candidates = Array.from(document.querySelectorAll<HTMLElement>("header button, header [role='button'], header a, header div, nav button, nav [role='button']"));
  const matches: DOMRect[] = [];
  for (const candidate of candidates) {
    const rect = visibleTopRect(candidate);
    if (!rect) continue;
    const text = `${candidate.textContent ?? ""} ${candidate.getAttribute("aria-label") ?? ""} ${candidate.getAttribute("title") ?? ""}`.replace(/\s+/g, " ").trim();
    if (match(text)) matches.push(rect);
  }
  matches.sort((a, b) => a.left - b.left);
  return matches[0] ?? null;
}

function applyChatGptTopRailSafeZone(panel = ensurePanel()): void {
  const rail = topRail(panel);
  if (!rail) return;
  const titleRect = findChatGptTopRect((text) => (
    text.length <= 24 &&
    /^ION(?:\s*(?:GPT|ChatGPT|▾|⌄|v))?$/i.test(text.replace(/[⌄▾∨]/g, "").trim())
  ));
  const memoryRect = findChatGptTopRect((text) => text.length <= 80 && /memory\s*off/i.test(text));
  const left = Math.max(12, Math.min((titleRect?.right ?? 86) + 10, window.innerWidth - 260));
  const rightLimit = memoryRect ? Math.max(left + 220, memoryRect.left - 12) : window.innerWidth - 132;
  const width = Math.max(220, Math.min(560, rightLimit - left));
  rail.style.left = `${left}px`;
  rail.style.right = "auto";
  rail.style.top = `${PANEL_TOP}px`;
  rail.style.width = `${Math.min(width, window.innerWidth - left - 12)}px`;
  rail.style.maxWidth = `${Math.min(width, window.innerWidth - left - 12)}px`;
}

function applyBottomMonitorLayout(panel = ensurePanel(), anchor = bridgeState.anchor as AnchorInfo): void {
  const monitor = panel.querySelector<HTMLElement>(".ion-bottom-monitor");
  if (!monitor) return;
  const maxWidth = Math.max(PANEL_MIN_WIDTH, window.innerWidth - 24);
  let width = Math.min(720, maxWidth);
  let left = 12;
  if (anchor.mode === "composer" && anchor.rect) {
    width = Math.min(720, Math.max(PANEL_MIN_WIDTH, anchor.rect.width));
    left = Math.max(12, Math.min(anchor.rect.left, window.innerWidth - width - 12));
  }
  monitor.style.left = `${left}px`;
  monitor.style.right = "auto";
  monitor.style.top = "auto";
  monitor.style.bottom = "1px";
  monitor.style.width = `${Math.min(width, maxWidth)}px`;
}

function positionApprovalModal(modal = document.getElementById(MODAL_ID)): void {
  const panel = document.getElementById(PANEL_ID) as HTMLElement | null;
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

export function setBridgeStatus(title: string, detail = "", tone: BridgeTone = "idle"): void {
  bridgeState.title = title;
  bridgeState.detail = detail;
  bridgeState.tone = tone;
  updateModeMemory(title, detail, tone);
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

export function setBridgeCodexState(nextState: Partial<CodexChatState>): void {
  bridgeState.codex = {
    ...(bridgeState.codex as CodexChatState),
    ...nextState,
    turns: nextState.turns ?? (bridgeState.codex as CodexChatState).turns,
  };
  renderPanel();
}

export function setBridgeMessageQueueState(nextState: Partial<MessageQueueState>): void {
  bridgeState.messageQueue = {
    ...(bridgeState.messageQueue as MessageQueueState),
    ...nextState,
    items: nextState.items ?? (bridgeState.messageQueue as MessageQueueState).items,
  };
  renderPanel();
}

export function setBridgePromptLibraryState(nextState: Partial<PromptLibraryState>): void {
  bridgeState.promptLibrary = {
    ...(bridgeState.promptLibrary as PromptLibraryState),
    ...nextState,
    items: nextState.items ?? (bridgeState.promptLibrary as PromptLibraryState).items,
  };
  renderPanel();
}

export function setBridgePackageDetail(detail: string): void {
  bridgeState.packages = detail;
  renderPanel();
}

export function setBridgeSandboxDetail(detail: string): void {
  bridgeState.sandbox = detail;
  renderPanel();
}

export function setBridgeArtifactDetail(detail: string): void {
  bridgeState.artifacts = detail;
  renderPanel();
}

export function setBridgeSettingsDetail(detail: string): void {
  bridgeState.settings = detail;
  renderPanel();
}

export function setBridgeDocsState(nextState: Partial<DocsBrowserState>): void {
  bridgeState.docs = {
    ...(bridgeState.docs as DocsBrowserState),
    ...nextState,
    roots: nextState.roots ?? (bridgeState.docs as DocsBrowserState).roots,
    entries: nextState.entries ?? (bridgeState.docs as DocsBrowserState).entries,
  };
  renderPanel();
}

export function setBridgeProjectsState(nextState: Partial<ProjectsState>): void {
  const current = bridgeState.projects as ProjectsState;
  const packages = nextState.packages ?? current.packages;
  const selectedPaths = nextState.selectedPaths ?? current.selectedPaths ?? [];
  const knownPaths = new Set(packages.map((entry) => entry.path));
  bridgeState.projects = {
    ...current,
    ...nextState,
    roots: nextState.roots ?? current.roots,
    packages,
    selectedPaths: selectedPaths.filter((path) => !knownPaths.size || knownPaths.has(path)),
  };
  renderPanel();
}

export function setBridgeDocsFavorites(nextFavorites: DocsFavoriteRoot[]): void {
  docsFavoriteRoots = nextFavorites;
  renderPanel();
}

export function setBridgeMonitorMetrics(nextState: Partial<MonitorMetrics>): void {
  bridgeState.monitor = {
    ...(bridgeState.monitor as MonitorMetrics),
    ...nextState,
  };
  renderPanel();
}

export function setBridgeDiagnosticsDetail(detail: string): void {
  bridgeState.diagnostics = detail;
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
    setExplicitOperationalMode("APPROVAL_MODAL", "Approval modal", `${action.intent}: ${action.action_id}`);
    positionApprovalModal(modal);
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
    setExplicitOperationalMode("APPROVAL_MODAL", "Approval modal", operation);
    positionApprovalModal(modal);
  });
}

export async function copyReceiptSummary(summary: string): Promise<void> {
  try {
    await navigator.clipboard.writeText(summary);
  } catch (_error) {
    console.info("ION ChatOps receipt summary", summary);
  }
}
