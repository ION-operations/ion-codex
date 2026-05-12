(() => {
  const seen = new Set();
  const inFlightActionIds = new Set();
  const submittedActionIds = new Set();
  const reportedBlockedActionIds = new Set();
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
  const INSPECTOR_OUTLINE_CLASS = "ion-chatops-dom-inspector-outline";
  const INSPECTOR_ANCHOR_MARKER_CLASS = "ion-chatops-dom-inspector-anchor-marker";
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
  const TAB_LIFT_KEY = "ION_CHATOPS_TAB_LIFT_PX";
  const DRAWER_MAX_KEY = "ION_CHATOPS_DRAWER_MAX_PX";
  const LAYOUT_TARGET_KEY = "ION_CHATOPS_LAYOUT_TARGET";
  const TOP_RAIL_X_KEY = "ION_CHATOPS_TOP_RAIL_X_PX";
  const TOP_RAIL_Y_KEY = "ION_CHATOPS_TOP_RAIL_Y_PX";
  const TABS_X_KEY = "ION_CHATOPS_TABS_X_PX";
  const TABS_Y_KEY = "ION_CHATOPS_TABS_Y_PX";
  const DRAWER_X_KEY = "ION_CHATOPS_DRAWER_X_PX";
  const DRAWER_Y_KEY = "ION_CHATOPS_DRAWER_Y_PX";
  const TARGET_ANCHOR_DEFAULTS = {
    tabs_anchor: "bottom",
    drop_zone: "center",
    attach_target: "center",
  };
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
  function readOnboardSyncState() {
    const base = {
      project: ONBOARD_PROJECT_NAME,
      bridge: ONBOARD_BRIDGE_NAME,
      protocolId: ONBOARD_PROTOCOL_ID,
      version: ONBOARD_PROTOCOL_VERSION,
      state: "ready",
      detail: `Ready to sync ${ONBOARD_PROJECT_NAME} context protocol ${ONBOARD_PROTOCOL_VERSION}.`,
      lastSyncedAt: ""
    };
    try {
      const stored = JSON.parse(window.localStorage?.getItem(ONBOARD_SYNC_KEY) ?? "{}");
      if (stored.project === ONBOARD_PROJECT_NAME && stored.bridge === ONBOARD_BRIDGE_NAME && stored.protocol_id === ONBOARD_PROTOCOL_ID && stored.version === ONBOARD_PROTOCOL_VERSION) {
        return {
          ...base,
          state: "synced",
          lastSyncedAt: String(stored.synced_at ?? ""),
          detail: `${ONBOARD_PROJECT_NAME} context protocol ${ONBOARD_PROTOCOL_VERSION} is marked synced to this extension build.`
        };
      }
    } catch {
    }
    return base;
  }
  function markOnboardSynced() {
    const next = {
      project: ONBOARD_PROJECT_NAME,
      bridge: ONBOARD_BRIDGE_NAME,
      protocolId: ONBOARD_PROTOCOL_ID,
      version: ONBOARD_PROTOCOL_VERSION,
      state: "synced",
      lastSyncedAt: new Date().toISOString(),
      detail: `${ONBOARD_PROJECT_NAME} context protocol ${ONBOARD_PROTOCOL_VERSION} sync was requested from this page.`
    };
    try {
      window.localStorage?.setItem(
        ONBOARD_SYNC_KEY,
        JSON.stringify({
          project: next.project,
          bridge: next.bridge,
          protocol_id: next.protocolId,
          version: next.version,
          synced_at: next.lastSyncedAt
        })
      );
    } catch {
    }
    return next;
  }
  function defaultPromptLibraryItems() {
    const now = "built-in";
    return [
      { id: "ion-context-router", title: "ION context router", category: "ION Context", tags: ["context", "router", "capsule"], pinned: true, updatedAt: now, usageCount: 0, origin: "built_in", text: "Use ION context routing. First identify the goal, then ask for or use the smallest relevant Capsule/Mini/context package. Do not assume full project context is active unless it has been attached or explicitly loaded." },
      { id: "ion-codex-work-packet", title: "Codex work packet", category: "Codex", tags: ["codex", "implementation", "bounded"], pinned: true, updatedAt: now, usageCount: 0, origin: "built_in", text: "Create a bounded Codex work packet for this objective. Include objective, constraints, files likely involved, validation requested, and exact success criteria. Do not request broad rewrites unless necessary." },
      { id: "ion-diagnostics", title: "Diagnostics report", category: "Diagnostics", tags: ["debug", "status", "browser"], pinned: false, updatedAt: now, usageCount: 0, origin: "built_in", text: "Give me a concise diagnostics report. Separate confirmed facts from assumptions. Include current visible symptoms, likely causes, smallest safe test, and recommended next action." },
      { id: "ion-package-request", title: "Package request", category: "Packages", tags: ["docs", "zip", "context-package"], pinned: false, updatedAt: now, usageCount: 0, origin: "built_in", text: "Use the attached ION package as the source of truth. Summarize what is inside, identify the most relevant files for the current task, and ask before assuming missing context." },
      { id: "ion-review", title: "Engineering review", category: "Review", tags: ["review", "risks", "tests"], pinned: false, updatedAt: now, usageCount: 0, origin: "built_in", text: "Review this like a pragmatic senior engineer. Prioritize bugs, regressions, unsafe assumptions, UX failures, and missing validation. Give findings first, then concise fixes." }
    ];
  }
  function readPromptLibraryItems() {
    try {
      const stored = JSON.parse(window.localStorage?.getItem(PROMPT_LIBRARY_KEY) ?? "[]");
      if (Array.isArray(stored) && stored.length) return stored.filter((item) => item && item.id && item.text);
    } catch {
    }
    return defaultPromptLibraryItems();
  }
  function writePromptLibraryItems(items) {
    try {
      window.localStorage?.setItem(PROMPT_LIBRARY_KEY, JSON.stringify(items));
    } catch {
    }
  }
  function defaultModeMemoryState() {
    return {
      currentMode: "IDLE_MONITORING",
      lastMode: "IDLE_MONITORING",
      lastActionId: "",
      lastIntent: "",
      lastReceiptPath: "",
      lastQueueTarget: "",
      lastStatusTitle: "Monitoring ChatGPT",
      lastDetail: "Waiting for ion_action YAML blocks.",
      lastUpdatedAt: ""
    };
  }
  function readModeMemoryState() {
    try {
      const stored = JSON.parse(window.localStorage?.getItem(MODE_MEMORY_KEY) ?? "{}");
      const defaults = defaultModeMemoryState();
      return {
        ...defaults,
        ...stored,
        currentMode: isBridgeOperationalMode(stored.currentMode) ? stored.currentMode : defaults.currentMode,
        lastMode: isBridgeOperationalMode(stored.lastMode) ? stored.lastMode : defaults.lastMode
      };
    } catch {
      return defaultModeMemoryState();
    }
  }
  function writeModeMemoryState(state) {
    try {
      window.localStorage?.setItem(MODE_MEMORY_KEY, JSON.stringify(state));
    } catch {
    }
  }
  function isBridgeOperationalMode(value) {
    return typeof value === "string" && [
      "IDLE_MONITORING",
      "DETECTED",
      "APPROVAL_REQUIRED",
      "APPROVAL_MODAL",
      "SUBMITTING",
      "RECEIPTED",
      "ERROR_BLOCKED",
      "INSPECTOR_CALIBRATION"
    ].includes(value);
  }
  function classifyOperationalMode(title, detail, tone) {
    const text = `${title}\n${detail}`.toLowerCase();
    if (/approval modal|operator reviews/.test(text)) return "APPROVAL_MODAL";
    if (/inspector|calibrat|capture frame|pick attach|pick drop|tabs anchor|previewed|drop zone|attach target/.test(text)) return "INSPECTOR_CALIBRATION";
    if (tone === "error" || /blocked|rejected|degraded|failed|not parsed|missing|unverified/.test(text)) return "ERROR_BLOCKED";
    if (/approval required/.test(text)) return "APPROVAL_REQUIRED";
    if (/approved, submitting|submitting|requesting daemon validation|requesting braden approval/.test(text)) return "SUBMITTING";
    if (tone === "success" || /submitted|receipt|queued|ready/.test(text)) return "RECEIPTED";
    if (/detected|candidate|validating/.test(text)) return "DETECTED";
    return "IDLE_MONITORING";
  }
  function matchDetailLine(detail, key) {
    const pattern = new RegExp(`^${key}:\\s*(.+)$`, "im");
    return detail.match(pattern)?.[1]?.trim() ?? "";
  }
  function firstDetailLine(detail) {
    return detail.split("\n").map((line) => line.trim()).find(Boolean) ?? "";
  }
  function actionPartsFromDetail(detail) {
    const explicitAction = matchDetailLine(detail, "action_id");
    const explicitIntent = matchDetailLine(detail, "intent");
    if (explicitAction || explicitIntent) return { actionId: explicitAction, intent: explicitIntent };
    const firstLine = firstDetailLine(detail);
    const detected = firstLine.match(/^([a-z0-9_:-]+):\s*(.+)$/i);
    if (!detected) return { actionId: "", intent: "" };
    return { intent: detected[1].trim(), actionId: detected[2].trim() };
  }
  function updateModeMemory(title, detail, tone) {
    const current = bridgeState.modeMemory;
    const nextMode = classifyOperationalMode(title, detail, tone);
    const action = actionPartsFromDetail(detail);
    const receiptPath = matchDetailLine(detail, "receipt_path");
    const status = matchDetailLine(detail, "status");
    const queuePath = matchDetailLine(detail, "queue_path");
    const queueTarget = matchDetailLine(detail, "queue_target");
    const next = {
      ...current,
      currentMode: nextMode,
      lastStatusTitle: title,
      lastDetail: firstDetailLine(detail) || title,
      lastUpdatedAt: new Date().toISOString()
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
  function setExplicitOperationalMode(mode, title, detail = "") {
    const current = bridgeState.modeMemory;
    const next = {
      ...current,
      currentMode: mode,
      lastMode: mode === "IDLE_MONITORING" ? current.lastMode : mode,
      lastStatusTitle: title,
      lastDetail: firstDetailLine(detail) || title,
      lastUpdatedAt: new Date().toISOString()
    };
    bridgeState.modeMemory = next;
    writeModeMemoryState(next);
    renderPanel();
  }
  function modeBadgeLabel(mode) {
    const labels = {
      IDLE_MONITORING: "MON",
      DETECTED: "DET",
      APPROVAL_REQUIRED: "APPR",
      APPROVAL_MODAL: "MODAL",
      SUBMITTING: "SEND",
      RECEIPTED: "RCPT",
      ERROR_BLOCKED: "BLOCK",
      INSPECTOR_CALIBRATION: "CAL"
    };
    return labels[mode];
  }
  function modeMemorySummary(memory) {
    if (memory.lastMode === "RECEIPTED" && memory.lastActionId) return "Last action queued";
    if (memory.lastActionId) return `Last ${memory.lastMode}: ${memory.lastActionId}`;
    return memory.lastStatusTitle || "Monitoring";
  }
  function modeMemoryDetail(memory) {
    return [
      "Mode memory",
      `current_mode: ${memory.currentMode}`,
      `last_mode: ${memory.lastMode}`,
      `last_action: ${memory.lastActionId || "none"}`,
      `last_intent: ${memory.lastIntent || "none"}`,
      `last_receipt: ${memory.lastReceiptPath || "none"}`,
      `last_queue_target: ${memory.lastQueueTarget || "none"}`,
      `last_status: ${memory.lastStatusTitle || "none"}`,
      `last_updated_at: ${memory.lastUpdatedAt || "not recorded"}`
    ].join("\n");
  }
  function promptLibraryInitialState() {
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
      items
    };
  }
  const bridgeState = {
    title: "Monitoring ChatGPT",
    detail: "Waiting for ion_action YAML blocks.",
    tone: "idle",
    modeMemory: readModeMemoryState(),
    action: "No action detected yet.",
    agent: "Codex-backed agent status has not been requested yet.",
    packages: "No context pack or ZIP export has been requested yet.",
    sandbox: "No ChatGPT sandbox returns have been requested yet.",
    automation: "Automation controls are staged only. This packet does not execute macros.",
    artifacts: "Artifact detection is staged only. No upload or local file movement occurs in this shell slice.",
    codex: {
      status: "Open Codex to load the existing Capsule-backed chat.",
      input: "",
      turns: [],
      view: "history",
      model: null,
      submitting: false,
      queueing: false,
    },
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
      items: []
    },
    promptLibrary: promptLibraryInitialState(),
    settings: "No local calibration has been changed in this session.",
    inspectorLayers: [],
    inspectorSelectedIndex: 0,
    diagnostics: "Normal carrier flow: Sev emits an ion_action YAML block in ChatGPT, the extension detects it, Braden approves it, the local daemon records/executes it, and ION writes a receipt.\n\nThe buttons below are local diagnostics only. They fabricate known-good test actions so the extension/daemon path can be checked without waiting on ChatGPT to emit YAML.",
    tools: "Daemon: http://127.0.0.1:8767\nUse Rescan after ChatGPT finishes rendering a YAML block.",
    logs: [],
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
    },
    projects: {
      status: "Open Projects to scan ION context-package folders.",
      roots: [],
      packages: [],
      selectedPath: "",
      selectedPaths: [],
      contextSyncOpen: false,
      contextSyncStatus: "No context sync package has been built yet.",
      contextSyncZipPath: "",
      contextSyncSha256: ""
    },
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
      detail: "ChatGPT browser pressure diagnostics are warming up.\n\nThis measures loaded browser transcript pressure, not exact active model context. ChatGPT uses rolling/managed context and does not expose exact live context composition to browser extensions."
    },
    onboard: readOnboardSyncState(),
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
  let inspectorActive = false;
  let inspectorCaptureMode = "single";
  let inspectorCapturedLayers = [];
  let inspectorSelectedIndex = 0;
  let settingsInspectorTarget = "tabs_anchor";
  let settingsAnchorPoint = "bottom";
  let settingsAnchorTarget = "tabs_anchor";
  let lastSettingsMode = false;
  let syncingSettingsModeEvent = false;
  let renderingPanel = false;
  let renderPanelQueued = false;
  let applyingSettingsInspectorMode = false;
  let settingsPadEventsBound = false;
  let docsClickTimer = null;
  let captureFrameTimer = null;
  let captureFrameLayerIndex = 0;
  let captureFrameLayers = [];
  let docsDropFavoritePath = "";
  let docsFavoriteRoots = [
    { path: "ION", label: "ION", icon: "🧱" },
    { path: "dAimon_ION", label: "Daimon", icon: "🧠" },
    { path: "ION/09_integrations", label: "Integrations", icon: "🧩" },
    { path: "ION/02_architecture", label: "Architecture", icon: "🗂️" },
    { path: "ION/06_artifacts", label: "Artifacts", icon: "📦" },
    { path: "ION/05_context", label: "Context", icon: "🧾" },
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
    "ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging"
  ];
  const defaultDocsState = {
    roots: docsFavoriteRoots.map((entry) => entry.path),
    currentRoot: "",
    currentPath: "",
    query: "",
    breadcrumbs: [],
    entries: [],
    selectedPath: "",
    selectedDocName: "",
    status: "Open Docs and pick a preselected root folder.",
  };
  let docsState = { ...defaultDocsState };
  let projectPackages = [];
  let selectedProjectPackagePath = "";
  let selectedProjectPackagePaths = [];
  let docsDropProgressTimer = null;
  function safeModeDisabled() {
    try {
      const value = window.localStorage?.getItem(SAFE_MODE_KEY) ?? window.sessionStorage?.getItem(SAFE_MODE_KEY);
      return ["1", "true", "disabled", "off"].includes(String(value ?? "").trim().toLowerCase());
    } catch (_error) {
      return false;
    }
  }
  function leftDockPanelExpandedFromStorage() {
    try {
      return window.localStorage?.getItem(CHATGPT_LEFT_ICON_DOCK_STORAGE_KEY) === "1";
    } catch (_error) {
      return false;
    }
  }
  function persistLeftDockPanelExpanded(next) {
    try {
      window.localStorage?.setItem(CHATGPT_LEFT_ICON_DOCK_STORAGE_KEY, next ? "1" : "0");
    } catch (_error) {
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
      top: 0;
      left: 0;
      z-index: 2147483644;
      width: 12px;
      height: 12px;
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
    .ion-dom-badge[data-ion-badge-role="source_plane"],
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

  function registryBadgeCanAttach(host) {
    return !["INPUT", "TEXTAREA", "IMG", "BR", "HR"].includes(host.tagName);
  }

  function registryBadgeCategory(kind, role) {
    if (kind === "message") return "read_chunk";
    if (role.startsWith("yaml_")) return "action_yaml";
    if (kind === "code") return "code_chunk";
    if (role === "send_button" || role === "attach_button" || role === "voice_button" || role === "composer_control") return "click_zone";
    if (role === "composer_input") return "text_entry_zone";
    if (role === "source_plane" || role === "uploaded_attachment") return "source_or_attachment_surface";
    return kind || role || "page_marker";
  }

  function registryBadgeMeaning(kind, role, tone) {
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

  function registryBadgeDetail(host, badge) {
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

  function addRegistryDetailRow(grid, key, value) {
    const keyNode = document.createElement("div");
    keyNode.className = "ion-registry-key";
    keyNode.textContent = key;
    const valueNode = document.createElement("div");
    valueNode.className = "ion-registry-value";
    valueNode.textContent = value || "-";
    grid.append(keyNode, valueNode);
  }

  function positionRegistryPopover(popover, badge) {
    const rect = badge.getBoundingClientRect();
    const width = 320;
    const left = Math.min(Math.max(12, rect.left), Math.max(12, window.innerWidth - width - 12));
    const below = rect.bottom + 8;
    const top = below + 220 < window.innerHeight ? below : Math.max(12, rect.top - 230);
    popover.style.left = `${Math.round(left)}px`;
    popover.style.top = `${Math.round(top)}px`;
  }

  async function copyRegistryValue(label, value) {
    await copyBridgeResult(label, value);
    setBridgeStatus("Registry copied", label, "success");
  }

  function showRegistryBadgeDetail(host, badge) {
    const existingPopover = document.getElementById(DOM_REGISTRY_POPOVER_ID);
    if (existingPopover?.dataset.ionBadgeId && existingPopover.dataset.ionBadgeId === badge.dataset.ionBadgeId) {
      existingPopover.remove();
      return;
    }
    existingPopover?.remove();
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
    closeButton.addEventListener("click", () => popover.remove());
    actions.append(textButton, selectorButton, detailButton, focusButton, closeButton);
  popover.append(actions, title, grid);
    document.documentElement.appendChild(popover);
    positionRegistryPopover(popover, badge);
  }

  function ensureRegistryBadge(host, kind, text, tone = "idle", role = "") {
    if (!registryBadgeCanAttach(host)) return;
    allowRegistryBadge(host);
    host.dataset.ionRegistryHost = "true";
    host.dataset.ionRegistryKind = kind;
    host.dataset.ionRegistryRole = role || kind;
    host.dataset.ionRegistryTone = tone;
    const existing = Array.from(host.children).find((child) => child.dataset?.ionBadge === kind);
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

  function captureLabel(node) {
    return `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.textContent ?? ""}`.replace(/\s+/g, " ").trim();
  }

  function noteCapture(stats, node, role, status = "healthy", label = "") {
    node.dataset.ionControlRole = role;
    node.dataset.ionCaptureStatus = status;
    if (label) node.dataset.ionCaptureLabel = label.slice(0, 80);
    ensureRegistryBadge(node, "control", `${role}${label ? `: ${label}` : ""}`, status === "approval_required" ? "blocked" : "idle", role);
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
      ensureRegistryBadge(node, "message", `ION msg ${index + 1} ${role}`, "idle", role);
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
    setBridgeMonitorMetrics({
      actionCandidateCount: stats.validActions + stats.invalidActions + stats.duplicateActions,
      validActionCount: stats.validActions,
      blockedActionCount: stats.invalidActions,
      duplicateActionCount: stats.duplicateActions,
      codeBlockCount: stats.codeBlocks,
      composerControlCount: stats.composerControls,
      selectedSourceCount: stats.selectedSources.length,
      uploadedAttachmentCount: stats.uploadedAttachments
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

  function ensureAssetCaptureStyle() {
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

  function clearAssetCaptureButtons() {
    document.querySelectorAll(`.${ASSET_CAPTURE_BUTTON_CLASS}`).forEach((node) => node.remove());
  }

  function assetCaptureLabel(node) {
    return `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.getAttribute("download") ?? ""} ${node.textContent ?? ""}`.replace(/\s+/g, " ").trim();
  }

  function assetSourceUrl(node) {
    if (node instanceof HTMLImageElement) return node.currentSrc || node.src || "";
    if (node instanceof HTMLAnchorElement) return node.href || "";
    const anchor = node.closest("a[href]");
    return anchor?.href ?? "";
  }

  function assetFilename(node, url) {
    const download = node.getAttribute("download") || node.closest("a[download]")?.getAttribute("download") || "";
    if (download.trim()) return download.trim();
    const label = assetCaptureLabel(node).replace(/[^A-Za-z0-9._ -]+/g, "_").trim();
    if (label && label.length <= 80) return label;
    try {
      const parsed = new URL(url);
      const basename = parsed.pathname.split("/").filter(Boolean).pop();
      if (basename) return basename;
    } catch (_error) {
    }
    return node instanceof HTMLImageElement ? "chatgpt-image.png" : "chatgpt-asset.bin";
  }

  function chatgptAssetCandidates() {
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
    const candidates = [];
    const seen = new Set();
    document.querySelectorAll(selector).forEach((node) => {
      const host = node.closest("a, button, [role='button']") ?? node;
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

  function blobToBase64(blob) {
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

  async function captureChatgptAsset(node) {
    const sourceUrl = assetSourceUrl(node);
    const payload = {
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

  function renderChatgptAssetCaptureButtons() {
    clearAssetCaptureButtons();
  }

  function ensureCaptureFrameStyle() {
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

  function captureFrameElement() {
    ensureCaptureFrameStyle();
    let frame = document.getElementById(CAPTURE_FRAME_ID);
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
      const move = (moveEvent) => {
        const width = rect.width;
        const height = rect.height;
        frame.style.left = `${Math.max(4, Math.min(window.innerWidth - width - 4, moveEvent.clientX - offsetX))}px`;
        frame.style.top = `${Math.max(34, Math.min(window.innerHeight - height - 4, moveEvent.clientY - offsetY))}px`;
        updateCaptureFrameLayersFromFrame(false);
      };
      const up = () => {
        frame.dataset.dragging = "false";
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

  function captureFrameSave(selector, label) {
    try {
      window.localStorage?.setItem(CAPTURE_FRAME_SELECTOR_KEY, selector);
    } catch (_error) {
      setBridgeSettingsDetail("Capture frame selector could not be saved to localStorage.");
      return;
    }
    setBridgeSettingsDetail(`capture_frame_saved\nselector: ${selector}\nlabel: ${label}\nScroll on the blue frame to switch stacked DOM layers.`);
  }

  function captureFrameLayerStack(x, y) {
    const seenElements = new Set();
    return document.elementsFromPoint(x, y)
      .filter((node) => node instanceof HTMLElement)
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

  function updateCaptureFrameLayerList() {
    setBridgeInspectorLayers(captureFrameLayers.map((layer, index) => ({
      index,
      label: layer.label,
      selector: layer.selector,
    })), captureFrameLayerIndex);
  }

  function updateCaptureFrameLayersFromFrame(lockActive) {
    const frame = document.getElementById(CAPTURE_FRAME_ID);
    if (!frame) return;
    const rect = frame.getBoundingClientRect();
    captureFrameLayers = captureFrameLayerStack(rect.left + rect.width / 2, rect.top + rect.height / 2);
    captureFrameLayerIndex = Math.min(captureFrameLayerIndex, Math.max(0, captureFrameLayers.length - 1));
    updateCaptureFrameLayerList();
    if (lockActive && captureFrameLayers.length) applyCaptureFrameLayer(captureFrameLayerIndex, true);
  }

  function applyCaptureFrameLayer(index, save) {
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

  function captureActiveFrameElement() {
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

  function startCaptureFrame() {
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

  function loadCaptureFrame() {
    const selector = window.localStorage?.getItem(CAPTURE_FRAME_SELECTOR_KEY) ?? "";
    if (!selector) {
      setBridgeSettingsDetail("capture_frame_load_failed\nNo saved capture frame selector.");
      setBridgeStatus("Capture frame not loaded", "No saved selector exists yet.", "error");
      return;
    }
    let node = null;
    try {
      node = document.querySelector(selector);
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

  function deleteCaptureFrame() {
    try {
      window.localStorage?.removeItem(CAPTURE_FRAME_SELECTOR_KEY);
    } catch (_error) {
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
      }      #${PANEL_ID} .ion-context-sync-icon {
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
      #${PANEL_ID} .ion-layout-picker {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 6px;
        width: 100%;
      }
      #${PANEL_ID} .ion-nudge-pad {
        display: grid;
        grid-template-columns: repeat(3, 34px);
        grid-template-rows: repeat(3, 30px);
        gap: 4px;
        align-items: center;
        justify-content: start;
      }
      #${PANEL_ID} .ion-nudge-pad .ion-tool {
        width: 34px;
        padding: 0;
      }
      #${PANEL_ID} .ion-nudge-spacer {
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
        grid-template-columns: repeat(4, minmax(0, 1fr));
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
      #${SETTINGS_CONTROL_PAD_ID} {
        position: fixed;
        z-index: 2147483646;
        top: 12px;
        right: 12px;
        display: grid;
        gap: 6px;
        min-width: 260px;
        width: min(280px, calc(100vw - 24px));
        padding: 10px;
        border: 1px solid rgba(255,112,28,0.38);
        border-radius: 12px;
        background: rgba(24, 24, 24, 0.92);
        color: rgba(255,255,255,0.84);
        font-size: 11px;
        backdrop-filter: blur(12px);
        pointer-events: auto;
      }
      #${SETTINGS_CONTROL_PAD_ID}[data-visible="false"] {
        display: none;
        opacity: 0.55;
        pointer-events: none;
      }
      #${SETTINGS_CONTROL_PAD_ID}[data-visible="true"] {
        display: grid;
        opacity: 1;
        pointer-events: auto;
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-pad-title {
        color: rgba(255,255,255,0.58);
        font-size: 10px;
        line-height: 1.2;
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-pad-state {
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 7px;
        min-height: 28px;
        padding: 4px 7px;
        color: rgba(255,255,255,0.9);
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-tool {
        flex: 0 0 auto;
        border: 1px solid transparent;
        color: rgba(255,255,255,0.82);
        background: transparent;
        padding: 0 8px;
        font-size: 12px;
        font-weight: 500;
        line-height: 1;
        cursor: pointer;
        height: 26px;
        border-radius: 8px;
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-tool:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(255,255,255,0.08);
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-tool[data-active="true"] {
        color: #ffd2b0;
        background: rgba(255,112,28,0.16);
        border-color: rgba(255,112,28,0.70);
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-anchor-pad {
        display: grid;
        grid-template-columns: repeat(7, 28px);
        grid-template-rows: 30px;
        align-items: center;
        justify-content: start;
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-anchor-pad .ion-tool {
        width: 28px;
        padding: 0;
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-anchor-spacer {
        width: 28px;
        height: 30px;
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-nudge-pad {
        display: grid;
        grid-template-columns: repeat(3, 34px);
        grid-template-rows: repeat(3, 30px);
        gap: 4px;
        align-items: center;
        justify-content: start;
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-nudge-pad .ion-tool {
        width: 34px;
        padding: 0;
      }
      #${SETTINGS_CONTROL_PAD_ID} .ion-nudge-spacer {
        width: 34px;
        height: 30px;
      }
      .${INSPECTOR_ANCHOR_MARKER_CLASS} {
        position: absolute;
        width: 0;
        height: 0;
        border-radius: 999px;
        border: 2px solid #ec4899;
        transform: translate(-50%, -50%);
        pointer-events: none;
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

  function ensureSettingsControlPad() {
    let pad = document.getElementById(SETTINGS_CONTROL_PAD_ID);
    if (pad) return pad;
    pad = document.createElement("section");
    pad.id = SETTINGS_CONTROL_PAD_ID;
    pad.dataset.visible = "false";
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
    document.documentElement.appendChild(pad);
    return pad;
  }

  function bindSettingsPadEvents() {
    if (settingsPadEventsBound) return;
    const pad = document.getElementById(SETTINGS_CONTROL_PAD_ID);
    if (!pad) return;
    pad.querySelectorAll('[data-tool^="settings-target-"], [data-tool^="settings-nudge-"]').forEach((button) => {
      const tool = button.dataset.tool ?? "";
      const toolEvent = {
        "settings-target-top": "ion-chatops-settings-target-top",
        "settings-target-tabs": "ion-chatops-settings-target-tabs",
        "settings-target-drawer": "ion-chatops-settings-target-drawer",
        "settings-nudge-up": "ion-chatops-settings-nudge-up",
        "settings-nudge-down": "ion-chatops-settings-nudge-down",
        "settings-nudge-left": "ion-chatops-settings-nudge-left",
        "settings-nudge-right": "ion-chatops-settings-nudge-right",
        "settings-nudge-reset": "ion-chatops-settings-nudge-reset",
      };
      const eventType = toolEvent[tool];
      if (!eventType) return;
      button.addEventListener("click", () => {
        window.dispatchEvent(new CustomEvent(eventType));
      });
    });
    pad.querySelectorAll('[data-tool^="settings-anchor-target-"]').forEach((button) => {
      const tool = button.dataset.tool ?? "";
      button.addEventListener("click", () => {
        const target =
          tool === "settings-anchor-target-tabs" ? "tabs_anchor" :
          tool === "settings-anchor-target-drop" ? "drop_zone" :
          tool === "settings-anchor-target-attach" ? "attach_target" :
          null;
        if (!target) return;
        const anchor = storageMetaForTarget(target).anchor;
        settingsAnchorPoint = anchor;
        settingsAnchorTarget = target;
        window.dispatchEvent(new CustomEvent("ion-chatops-settings-anchor-target", { detail: { target } }));
      });
    });
    pad.querySelectorAll('[data-tool="settings-anchor-point"]').forEach((button) => {
      button.addEventListener("click", () => {
        const anchor = button.dataset.anchor;
        if (!anchor) return;
        window.dispatchEvent(new CustomEvent("ion-chatops-settings-anchor-point", { detail: { anchor } }));
      });
    });
    pad.querySelector('[data-tool="settings-inspector-preview"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-settings-inspector-preview"));
    });
    settingsPadEventsBound = true;
  }

  function syncSettingsControlPadState(panel = ensurePanel()) {
    const pad = document.getElementById(SETTINGS_CONTROL_PAD_ID);
    if (!pad) return;
    const padState = pad.querySelector('[data-tool="settings-pad-state"]');
    if (padState) {
      padState.textContent = `Target: ${settingsAnchorTarget} • Anchor: ${settingsAnchorPoint}`;
    }
    pad.querySelectorAll('[data-tool="settings-target-top"], [data-tool="settings-target-tabs"], [data-tool="settings-target-drawer"]').forEach((button) => {
      const tool = button.dataset.tool ?? "";
      const target = tool === "settings-target-top" ? "top_rail" : tool === "settings-target-drawer" ? "drawer" : "tabs";
      button.dataset.active = String(target === readLayoutTarget());
    });
    pad.querySelectorAll('[data-tool="settings-anchor-target-tabs"], [data-tool="settings-anchor-target-drop"], [data-tool="settings-anchor-target-attach"]').forEach((button) => {
      const tool = button.dataset.tool ?? "";
      const target =
        tool === "settings-anchor-target-tabs" ? "tabs_anchor" :
        tool === "settings-anchor-target-drop" ? "drop_zone" :
        tool === "settings-anchor-target-attach" ? "attach_target" :
        null;
      if (target) button.dataset.active = String(target === settingsAnchorTarget);
    });
    pad.querySelectorAll('[data-tool="settings-anchor-point"]').forEach((button) => {
      button.dataset.active = String(button.dataset.anchor === settingsAnchorPoint);
    });
    syncSettingsMode(panel, false);
  }

  function syncSettingsMode(panel = ensurePanel(), notify = false) {
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

  function storageMetaForTarget(target) {
    if (target === "drop_zone") return dropTargetMeta();
    if (target === "attach_target") return attachTargetMeta();
    return tabsAnchorMeta();
  }

  function rectIsVisible(rect) {
    return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
  }

  function isBridgeElement(element) {
    if (element.classList.contains("ion-dom-badge") || element.classList.contains(INSPECTOR_OUTLINE_CLASS) || element.classList.contains(INSPECTOR_ANCHOR_MARKER_CLASS)) {
      return true;
    }
    return Boolean(
      element.closest(`#${PANEL_ID}`) ??
      element.closest(`#${MODAL_ID}`) ??
      element.closest(`#${SETTINGS_CONTROL_PAD_ID}`) ??
      element.closest(`.${ASSET_CAPTURE_BUTTON_CLASS}`) ??
      element.closest(`#${CHATGPT_LEFT_ICON_DOCK_ID}`) ??
      element.closest(`.${CHATGPT_LEFT_ICON_DOCK_CLASS}`) ??
      element.closest(`#${DOM_REGISTRY_POPOVER_ID}`) ??
      element.closest(`#${INSPECTOR_HUD_ID}`) ??
      element.closest(`#${INSPECTOR_SELECTED_PREVIEW_ID}`) ??
      element.closest(`#${ATTACH_PREVIEW_ID}`) ??
      element.closest(`#${DROP_PREVIEW_ID}`) ??
      element.closest(`#${TABS_ANCHOR_PREVIEW_ID}`) ??
      element.closest(`#${DOM_REGISTRY_STYLE_ID}`) ??
      element.closest(`#${ASSET_CAPTURE_STYLE_ID}`)
    );
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

  function readNumberSetting(key, fallback, min, max) {
    try {
      const raw = window.localStorage?.getItem(key);
      const value = raw === null || raw === undefined ? Number.NaN : Number.parseInt(raw, 10);
      if (!Number.isFinite(value)) return fallback;
      return Math.max(min, Math.min(max, value));
    } catch (_error) {
      return fallback;
    }
  }

  function writeNumberSetting(key, value, min, max) {
    const bounded = Math.max(min, Math.min(max, Math.round(value)));
    try {
      window.localStorage?.setItem(key, String(bounded));
    } catch (_error) {
    }
    return bounded;
  }

  function readLayoutTarget() {
    try {
      const raw = String(window.localStorage?.getItem(LAYOUT_TARGET_KEY) ?? "").trim();
      if (raw === "top_rail" || raw === "tabs" || raw === "drawer") return raw;
    } catch (_error) {
    }
    return "tabs";
  }

  function writeLayoutTarget(target) {
    try {
      window.localStorage?.setItem(LAYOUT_TARGET_KEY, target);
    } catch (_error) {
    }
  }

  function layoutOffset(target) {
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

  function writeLayoutOffset(target, x, y) {
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

  function applyDrawerOffset(panel) {
    const offset = layoutOffset("drawer");
    if (typeof panel.style.setProperty === "function") {
      panel.style.setProperty("--ion-chatops-drawer-x-px", `${offset.x}px`);
      panel.style.setProperty("--ion-chatops-drawer-y-px", `${offset.y}px`);
      panel.style.setProperty("--ion-chatops-tab-height", `${TAB_HEIGHT}px`);
    }
  }

  function attachTargetSelector() {
    try {
      const meta = storageMetaForTarget("attach_target");
      return meta.selector;
    } catch (_error) {
      return "";
    }
  }

  function dropTargetSelector() {
    try {
      const meta = storageMetaForTarget("drop_zone");
      return meta.selector;
    } catch (_error) {
      return "";
    }
  }
  function tabsAnchorSelector() {
    try {
      const meta = storageMetaForTarget("tabs_anchor");
      return meta.selector;
    } catch (_error) {
      return "";
    }
  }

  function settingsSummary() {
    const attachMeta = storageMetaForTarget("attach_target");
    const dropMeta = storageMetaForTarget("drop_zone");
    const tabsAnchorMeta = storageMetaForTarget("tabs_anchor");
    const selector = attachMeta.selector || "not calibrated";
    const dropSelector = dropMeta.selector || "default page/composer zone";
    const tabsAnchor = tabsAnchorMeta.selector || "auto composer shell";
    const selected = readLayoutTarget();
    const top = layoutOffset("top_rail");
    const tabs = layoutOffset("tabs");
    const drawer = layoutOffset("drawer");
    return [
      `inspector: ${inspectorCaptureMode === "settings" ? "settings inspector locked" : "single capture mode"}`,
      `calibration_target: ${settingsAnchorTarget} @${settingsAnchorPoint}`,
      `attach_target: ${selector} [anchor:${attachMeta.anchor}]`,
      `drop_zone: ${dropSelector} [anchor:${dropMeta.anchor}]`,
      `tabs_anchor: ${tabsAnchor} [anchor:${tabsAnchorMeta.anchor}]`,
      `layout_target: ${selected}`,
      `top_rail_offset: x=${top.x}, y=${top.y}`,
      `tabs_offset: x=${tabs.x}, y=${tabs.y}`,
      `drawer_offset: x=${drawer.x}, y=${drawer.y}`,
      `tab_lift_px: ${readNumberSetting(TAB_LIFT_KEY, 2, -24, 48)}`,
      `drawer_max_px: ${readNumberSetting(DRAWER_MAX_KEY, 360, 220, 680)}`,
      `inspector_layers: ${bridgeState.inspectorLayers.length ? `${bridgeState.inspectorLayers.length} captured at last click` : "none captured"}`,
      "",
      "Select Top Rail, Tabs, or Drawer, then use the arrow pad to nudge that surface.",
      "Use DOM Inspector while Settings is open. The selected anchor target and point stay active while picking.",
      "Use Pick Tabs Anchor when the automatic composer shell is not the visible panel top.",
      "Use Preview Drop Zone before Drop Latest. Pick Drop Zone if the blue ring is not where ChatGPT accepts file drops.",
      "Use Pick Attach Target, then click ChatGPT's real attach/add-file button once.",
      "Local Attach is a fallback and should only be used after Preview Target rings the correct button and Dry Run passes.",
    ].join("\n");
  }
  function setBridgeInspectorLayers(layers, selectedIndex = 0) {
    bridgeState.inspectorLayers = layers.slice(0, 24);
    bridgeState.inspectorSelectedIndex = selectedIndex;
    renderPanel();
  }

  function selectLayoutTarget(target) {
    writeLayoutTarget(target);
    bridgeState.settings = `layout_target set to ${target}`;
    appendBridgeLog(`Layout target selected: ${target}`);
    renderPanel();
  }

  function nudgeLayoutTarget(dx, dy) {
    const target = readLayoutTarget();
    const current = layoutOffset(target);
    const next = writeLayoutOffset(target, current.x + dx, current.y + dy);
    bridgeState.settings = `${target} offset set to x=${next.x}, y=${next.y}`;
    appendBridgeLog(`Layout nudged: ${target} x=${next.x} y=${next.y}`);
    renderPanel();
  }

  function resetSelectedLayoutTarget() {
    const target = readLayoutTarget();
    const next = writeLayoutOffset(target, 0, 0);
    bridgeState.settings = `${target} offset reset to x=${next.x}, y=${next.y}`;
    appendBridgeLog(`Layout target reset: ${target}`);
    renderPanel();
  }

  function adjustTabLift(delta) {
    const next = writeNumberSetting(TAB_LIFT_KEY, readNumberSetting(TAB_LIFT_KEY, 2, -24, 48) + delta, -24, 48);
    bridgeState.settings = `tab_lift_px set to ${next}`;
    appendBridgeLog(`Layout adjusted: tab_lift_px=${next}`);
    renderPanel();
  }

  function adjustDrawerMax(delta) {
    const next = writeNumberSetting(DRAWER_MAX_KEY, readNumberSetting(DRAWER_MAX_KEY, 360, 220, 680) + delta, 220, 680);
    bridgeState.settings = `drawer_max_px set to ${next}`;
    appendBridgeLog(`Layout adjusted: drawer_max_px=${next}`);
    renderPanel();
  }

  function resetLayoutSettings() {
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
    } catch (_error) {
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

  function applyTopRailLayout(panel) {
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

  function applyTopBarLayout(panel) {
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
          </div>        </div>
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
              <button type="button" class="ion-tool" data-tool="settings-inspector-start">Start Inspector</button>
              <button type="button" class="ion-tool" data-tool="settings-inspector-cancel">Cancel Inspector</button>
              <button type="button" class="ion-tool" data-tool="settings-inspector-preview">Preview Layer</button>
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
        <span class="ion-monitor-pill" data-monitor="chat">Loaded text warming</span>
        <span class="ion-monitor-pill" data-monitor="actions">Actions warming</span>
        <span class="ion-monitor-pill" data-monitor="queue">Queue warming</span>
        <span class="ion-monitor-pill" data-monitor="connected">Conn warming</span>
        <span class="ion-monitor-pill" data-monitor="lag">Lag warming</span>
        <span class="ion-monitor-pill" data-monitor="dom">DOM warming</span>
      </div>
    `;
    document.documentElement.appendChild(panel);
    panel.querySelector("[data-mode-memory]")?.addEventListener("click", () => {
      panel.dataset.expanded = "true";
      panel.dataset.tab = "status";
      renderPanel(panel);
    });
    panel.querySelectorAll(".ion-tab").forEach((tab) => {
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
          version: ONBOARD_PROTOCOL_VERSION
        }
      }));
    });
    panel.querySelector('[data-tool="context-sync-toggle"]')?.addEventListener("click", () => {
      const projects = bridgeState.projects;
      const nextOpen = !projects.contextSyncOpen;
      setBridgeProjectsState({ contextSyncOpen: nextOpen });
      if (nextOpen && !projects.packages.length) {
        window.dispatchEvent(new CustomEvent("ion-chatops-projects-refresh"));
      }
    });
    panel.querySelector('[data-tool="gateway-auto-accept"]')?.addEventListener("click", (event) => {
      const target = event.target;
      if (target.closest("[data-auto-accept-timer]")) {
        const popover = panel.querySelector(".ion-auto-settings-popover");
        if (popover) {
          popover.dataset.visible = String(popover.dataset.visible === "false");
        }
        return;
      }
      window.dispatchEvent(new CustomEvent("ion-chatops-gateway-auto-accept-toggle"));
    });
    panel.querySelector("[data-auto-accept-ttl-input]")?.addEventListener("input", (event) => {
      const input = event.target;
      const ttl_seconds = Math.max(60, Number(input.value) * 60);
      window.dispatchEvent(new CustomEvent("ion-chatops-gateway-auto-accept-settings", { detail: { ttl_seconds } }));
    });
    const contextSyncMenu = panel.querySelector("[data-context-sync-menu]");
    contextSyncMenu?.addEventListener("click", (event) => {
      const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
      const button = source?.closest("[data-context-sync-action]");
      const action = button?.dataset.contextSyncAction ?? "";
      if (!action) return;
      event.preventDefault();
      const projects = bridgeState.projects;
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
          contextSyncOpen: true
        });
        return;
      }
      if (action === "clear") {
        setBridgeProjectsState({
          selectedPaths: [],
          contextSyncStatus: "Selection cleared. Pick one or more project packages.",
          contextSyncOpen: true
        });
        return;
      }
      if (action === "build") {
        const selectedPaths = (projects.selectedPaths ?? []).filter(Boolean);
        if (!selectedPaths.length) {
          setBridgeProjectsState({
            contextSyncStatus: "Select at least one project package before building a context sync ZIP.",
            contextSyncOpen: true
          });
          return;
        }
        setBridgeProjectsState({
          contextSyncStatus: `Requesting context sync ZIP for ${selectedPaths.length} project package(s)...`,
          contextSyncOpen: true
        });
        window.dispatchEvent(new CustomEvent("ion-chatops-project-context-sync", { detail: { paths: selectedPaths } }));
      }
    });
    contextSyncMenu?.addEventListener("change", (event) => {
      const input = event.target instanceof HTMLInputElement ? event.target : null;
      const path = input?.dataset.contextSyncPath ?? "";
      if (!path) return;
      const projects = bridgeState.projects;
      const selected = new Set((projects.selectedPaths ?? []).filter(Boolean));
      if (input.checked) selected.add(path);
      else selected.delete(path);
      setBridgeProjectsState({
        selectedPaths: Array.from(selected),
        contextSyncStatus: `${selected.size} project package(s) selected for context sync.`,
        contextSyncOpen: true
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
    panel.querySelector('[data-tool="agent-prepare"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-agent-prepare"));
    });
  panel.querySelector('[data-tool="agent-start"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-agent-start"));
  });
  panel.querySelector('[data-tool="codex-refresh"]')?.addEventListener("click", () => {
    window.dispatchEvent(new CustomEvent("ion-chatops-codex-refresh"));
  });
  panel.querySelector('[data-codex="input"]')?.addEventListener("input", (event) => {
    bridgeState.codex.input = event.currentTarget?.value ?? "";
  });
  panel.querySelectorAll("[data-codex-view]").forEach((button) => {
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
    panel.querySelector('[data-queue="input"]')?.addEventListener("input", (event) => {
      bridgeState.messageQueue.input = event.currentTarget?.value ?? "";
    });
    panel.querySelector('[data-tool="queue-add"]')?.addEventListener("click", () => {
      const queue = bridgeState.messageQueue;
      const text = queue.input.trim();
      if (!text) return;
      queue.input = "";
      window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-add", { detail: { text } }));
      renderPanel(panel);
    });
    panel.querySelector('[data-tool="queue-import-pack"]')?.addEventListener("click", () => {
      panel.querySelector('[data-queue-pack="file"]')?.click();
    });
    panel.querySelector('[data-queue-pack="file"]')?.addEventListener("change", (event) => {
      const input = event.currentTarget;
      const file = input?.files?.[0];
      if (!file) return;
      void importQueuePackFile(file).finally(() => {
        if (input) input.value = "";
      });
    });
    panel.querySelector('[data-tool="queue-pause"]')?.addEventListener("click", () => {
      const queue = bridgeState.messageQueue;
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
    panel.querySelector('[data-queue="allow-mid-output"]')?.addEventListener("change", (event) => {
      window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-mid-output", { detail: { allow: Boolean(event.currentTarget?.checked) } }));
    });
    panel.querySelector('[data-prompts="query"]')?.addEventListener("input", (event) => {
      setBridgePromptLibraryState({ query: event.currentTarget?.value ?? "" });
    });
    panel.querySelector('[data-prompts="category"]')?.addEventListener("change", (event) => {
      setBridgePromptLibraryState({ category: event.currentTarget?.value ?? "all" });
    });
    panel.querySelector('[data-prompts="list"]')?.addEventListener("click", (event) => {
      const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
      const target = source?.closest("[data-prompt-id]");
      if (!target?.dataset.promptId) return;
      selectPromptLibraryItem(target.dataset.promptId);
    });
    panel.querySelectorAll('[data-prompts="title"], [data-prompts="draft-category"], [data-prompts="tags"], [data-prompts="text"]').forEach((input) => {
      input.addEventListener("input", () => {
        setBridgePromptLibraryState({
          draftTitle: panel.querySelector('[data-prompts="title"]')?.value ?? "",
          draftCategory: panel.querySelector('[data-prompts="draft-category"]')?.value ?? "",
          draftTags: panel.querySelector('[data-prompts="tags"]')?.value ?? "",
          draftText: panel.querySelector('[data-prompts="text"]')?.value ?? ""
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
      const prompt = bridgeState.promptLibrary;
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
        status: "New prompt draft ready."
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
        status: "Prompt library reset to built-ins."
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
      const path = bridgeState.projects.selectedPath;
      if (path) window.dispatchEvent(new CustomEvent("ion-chatops-projects-drop", { detail: { path } }));
    });
    panel.querySelector('[data-tool="projects-open-root"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root", { detail: { path: "ION/05_context/history/kernel_store/context_packages" } }));
      panel.dataset.expanded = "true";
      panel.dataset.tab = "docs";
      renderPanel(panel);
    });
    panel.querySelector('[data-projects="grid"]')?.addEventListener("click", (event) => {
      const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
      const target = source?.closest("[data-project-path]");
      const path = target?.dataset.projectPath ?? "";
      if (!path) return;
      setBridgeProjectsState({ selectedPath: path });
    });
    panel.querySelector('[data-projects="grid"]')?.addEventListener("dblclick", (event) => {
      const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
      const target = source?.closest("[data-project-path]");
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
    const currentPath = panel.querySelector('[data-docs="entries"]')?.dataset.currentPath ?? "";
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-folder", {
      detail: {
        path: currentPath,
        query: panel.querySelector('[data-docs-control="search"]')?.value ?? "",
      },
    }));
  });
  panel.querySelector('[data-docs-control="search"]')?.addEventListener("input", (event) => {
    const query = event.currentTarget?.value ?? "";
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-search", { detail: { query } }));
  });
  panel.querySelector('[data-docs="favorites"]')?.addEventListener("click", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const action = source?.closest("[data-doc-fav-action]");
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
        setBridgeDocsState({ roots: bridgeState.docs.roots.filter((root) => root !== path), status: `Favorite hidden for this session: ${label}` });
      } else if (kind === "more") {
        setBridgeDocsState({ status: `Favorite actions for ${label}: double-click tile to zip/drop, arrow opens, x hides for this session.` });
      }
      return;
    }
    const target = source?.closest("[data-doc-root]");
    if (!target) return;
    const path = target.dataset.docRoot ?? "";
    if (!path) return;
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root", { detail: { path } }));
  });
  panel.querySelector('[data-docs="favorites"]')?.addEventListener("dblclick", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    if (source?.closest("[data-doc-fav-action]")) return;
    const target = source?.closest("[data-doc-root]");
    if (!target) return;
    const path = target.dataset.docRoot ?? "";
    const label = target.dataset.docLabel ?? path.split("/").pop() ?? "";
    if (!path) return;
    event.preventDefault();
    event.stopPropagation();
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-drag-doc", { detail: { path, name: label, source: "favorite_double_click" } }));
  });
  panel.querySelector('[data-docs="tree"]')?.addEventListener("change", (event) => {
    const select = event.currentTarget;
    const path = select?.value ?? "";
    if (!path) {
      window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root"));
      return;
    }
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root", { detail: { path } }));
  });
  panel.querySelector('[data-docs="roots"]')?.addEventListener("click", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest("[data-doc-root]");
    if (!target) return;
    const path = target.dataset.docRoot ?? "";
    if (!path) return;
    window.dispatchEvent(new CustomEvent("ion-chatops-docs-open-root", { detail: { path } }));
  });
  panel.querySelector('[data-docs="entries"]')?.addEventListener("click", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest("[data-doc-kind]");
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
  panel.querySelector('[data-docs="entries"]')?.addEventListener("dblclick", (event) => {
    if (docsClickTimer !== null) {
      window.clearTimeout(docsClickTimer);
      docsClickTimer = null;
    }
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest("[data-doc-kind]");
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
  panel.querySelector('[data-docs="entries"]')?.addEventListener("dragstart", (event) => {
    const source = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    const target = source?.closest("[data-doc-kind]");
    if (!target) return;
    const path = target.dataset.docPath ?? "";
    const name = target.dataset.docName ?? "";
    if (!path) return;
    event.dataTransfer?.setData("text/plain", path);
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
    panel.querySelector('[data-tool="settings-inspector-start"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-settings-inspector-start"));
    });
    panel.querySelector('[data-tool="settings-inspector-cancel"]')?.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("ion-chatops-settings-inspector-cancel"));
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
    panel.querySelector('[data-control="settings-inspector-layer"]')?.addEventListener("change", (event) => {
      const select = event.currentTarget;
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
    renderPanel(panel);
    return panel;
  }

  function positionPanelAboveComposer(panel = ensurePanel()) {
    const anchor = detectComposerAnchor();
    bridgeState.anchor = anchor;
    applyTopRailLayout(panel);
    if (!applyComposerLayout(panel, anchor)) applyTopBarLayout(panel);
    applyBottomMonitorLayout(panel, anchor);
  }

  function visibleTopRect(element) {
    if (element.closest(`#${PANEL_ID}`) || element.closest(`#${MODAL_ID}`)) return null;
    const rect = element.getBoundingClientRect();
    if (rect.width < 8 || rect.height < 8) return null;
    if (rect.bottom < 0 || rect.top > 72) return null;
    const style = window.getComputedStyle(element);
    if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) return null;
    return rect;
  }
  function findChatGptTopRect(match) {
    const candidates = Array.from(document.querySelectorAll("header button, header [role='button'], header a, header div, nav button, nav [role='button']"));
    const matches = [];
    for (const candidate of candidates) {
      const rect = visibleTopRect(candidate);
      if (!rect) continue;
      const text = `${candidate.textContent ?? ""} ${candidate.getAttribute("aria-label") ?? ""} ${candidate.getAttribute("title") ?? ""}`.replace(/\s+/g, " ").trim();
      if (match(text)) matches.push(rect);
    }
    matches.sort((a, b) => a.left - b.left);
    return matches[0] ?? null;
  }
  function applyChatGptTopRailSafeZone(panel = ensurePanel()) {
    const rail = topRail(panel);
    if (!rail) return;
    const titleRect = findChatGptTopRect((text) => text.length <= 24 && /^ION(?:\s*(?:GPT|ChatGPT|▾|⌄|v))?$/i.test(text.replace(/[⌄▾∨]/g, "").trim()));
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

  function applyBottomMonitorLayout(panel = ensurePanel(), anchor = bridgeState.anchor) {
    const monitor = panel.querySelector(".ion-bottom-monitor");
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

  function renderMessageQueuePanel(panel = ensurePanel()) {
    const queue = bridgeState.messageQueue;
    const statusNode = panel.querySelector('[data-queue="status"]');
    const inputNode = panel.querySelector('[data-queue="input"]');
    const allowNode = panel.querySelector('[data-queue="allow-mid-output"]');
    const readinessNode = panel.querySelector('[data-queue="readiness"]');
    const itemsNode = panel.querySelector('[data-queue="items"]');
    const pauseButton = panel.querySelector('[data-tool="queue-pause"]');
    if (statusNode) statusNode.textContent = queue.status;
    if (inputNode && document.activeElement !== inputNode) inputNode.value = queue.input;
    if (allowNode) allowNode.checked = queue.allowMidOutput;
    if (readinessNode) {
      readinessNode.textContent = [
        queue.activeOutput ? "output: active" : "output: idle",
        queue.sendAvailable ? "send: available" : "send: locked",
        queue.paused ? "queue: paused" : "queue: armed"
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

  function renderProjectsPanel(panel = ensurePanel()) {
    const projects = bridgeState.projects;
    const statusNode = panel.querySelector('[data-projects="status"]');
    const gridNode = panel.querySelector('[data-projects="grid"]');
    if (statusNode) {
      statusNode.textContent = [
        projects.status,
        projects.roots.length ? `roots: ${projects.roots.join(", ")}` : "roots: not scanned yet",
        projects.selectedPath ? `selected: ${projects.selectedPath}` : "selected: none",
        projects.selectedPaths.length ? `context_sync_selected: ${projects.selectedPaths.length}` : "context_sync_selected: none"
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

  function contextSyncActionButton(action, label, disabled = false) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ion-tool";
    button.dataset.contextSyncAction = action;
    button.textContent = label;
    button.disabled = disabled;
    return button;
  }

  function renderContextSyncTopMenu(panel = ensurePanel()) {
    const projects = bridgeState.projects;
    const knownPaths = new Set(projects.packages.map((entry) => entry.path));
    const selectedPaths = (projects.selectedPaths ?? []).filter((path) => !knownPaths.size || knownPaths.has(path));
    const selectedCount = selectedPaths.length;
    const syncReady = Boolean(projects.contextSyncZipPath);
    panel.dataset.contextSyncOpen = String(Boolean(projects.contextSyncOpen));
    const button = panel.querySelector('[data-tool="context-sync-toggle"]');
    const label = panel.querySelector("[data-context-sync-label]");
    const menu = panel.querySelector("[data-context-sync-menu]");
    if (button) {
      button.dataset.contextSyncState = syncReady ? "ready" : selectedCount ? "selected" : "idle";
      button.setAttribute("aria-expanded", String(Boolean(projects.contextSyncOpen)));
      button.title = [
        "Select ION project context packages and build one approved sync ZIP.",
        selectedCount ? `selected_projects: ${selectedCount}` : "selected_projects: none",
        projects.contextSyncZipPath ? `latest_zip: ${projects.contextSyncZipPath}` : "",
        projects.contextSyncSha256 ? `sha256: ${projects.contextSyncSha256}` : "",
        "Authority: context sync only; no production, live execution, mutation, or secrets authority."
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
      projects.contextSyncSha256 ? `sha256: ${projects.contextSyncSha256}` : ""
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
      contextSyncActionButton("open-projects", "Projects")
    );
    menu.append(head, list, actions);
  }

  function promptLibraryCategories(items) {
    return Array.from(new Set(items.map((item) => item.category || "General"))).sort((a, b) => a.localeCompare(b));
  }
  function filteredPromptLibraryItems(state = bridgeState.promptLibrary) {
    const query = state.query.trim().toLowerCase();
    return state.items.filter((item) => state.category === "all" || item.category === state.category).filter((item) => {
      if (!query) return true;
      return `${item.title} ${item.category} ${item.tags.join(" ")} ${item.text}`.toLowerCase().includes(query);
    }).sort((a, b) => Number(b.pinned) - Number(a.pinned) || b.usageCount - a.usageCount || a.title.localeCompare(b.title));
  }
  function selectPromptLibraryItem(id) {
    const state = bridgeState.promptLibrary;
    const item = state.items.find((candidate) => candidate.id === id);
    if (!item) return;
    setBridgePromptLibraryState({
      selectedId: item.id,
      draftTitle: item.title,
      draftCategory: item.category,
      draftTags: item.tags.join(", "),
      draftText: item.text,
      status: `Selected prompt: ${item.title}`
    });
  }
  function promptDraftItem(existing) {
    const state = bridgeState.promptLibrary;
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
      origin: existing?.origin === "built_in" ? "built_in" : "custom"
    };
  }
  function savePromptLibraryDraft() {
    const state = bridgeState.promptLibrary;
    if (!state.draftText.trim()) {
      setBridgePromptLibraryState({ status: "Prompt text is empty. Nothing saved." });
      return;
    }
    const existing = state.items.find((item) => item.id === state.selectedId);
    const nextItem = promptDraftItem(existing);
    const items = existing ? state.items.map((item) => item.id === existing.id ? nextItem : item) : [nextItem, ...state.items];
    writePromptLibraryItems(items);
    setBridgePromptLibraryState({
      items,
      selectedId: nextItem.id,
      draftTitle: nextItem.title,
      draftCategory: nextItem.category,
      draftTags: nextItem.tags.join(", "),
      draftText: nextItem.text,
      status: `Saved prompt: ${nextItem.title}`
    });
  }
  function togglePromptPinned() {
    const state = bridgeState.promptLibrary;
    const items = state.items.map((item) => item.id === state.selectedId ? { ...item, pinned: !item.pinned, updatedAt: new Date().toISOString() } : item);
    writePromptLibraryItems(items);
    setBridgePromptLibraryState({ items, status: "Prompt pin state updated." });
  }
  function deleteSelectedPrompt() {
    const state = bridgeState.promptLibrary;
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
      status: "Prompt deleted."
    });
  }
  function markPromptUsed(id, status) {
    if (!id) {
      setBridgePromptLibraryState({ status });
      return;
    }
    const state = bridgeState.promptLibrary;
    const items = state.items.map((item) => item.id === id ? { ...item, usageCount: item.usageCount + 1, updatedAt: new Date().toISOString() } : item);
    writePromptLibraryItems(items);
    setBridgePromptLibraryState({ items, status });
  }
  function normalizeQueuePackPath(path) {
    return path.replace(/\\/g, "/").replace(/^\/+/, "").split("/").filter((part) => part && part !== "." && part !== "..").join("/");
  }
  function queuePackLine(value) {
    return String(value ?? "").replace(/\s+/g, " ").trim().slice(0, 180);
  }
  function queuePackTitle(pack) {
    return queuePackLine(pack.title || pack.pack_id || "ION queue pack");
  }
  function queuePackStepText(step, textEntries) {
    const direct = String(step.prompt ?? step.text ?? "").trim();
    if (direct) return direct;
    const ref = normalizeQueuePackPath(String(step.prompt_ref ?? ""));
    if (!ref) return "";
    return String(textEntries.get(ref) ?? "").trim();
  }
  function collectQueuePackSteps(pack) {
    const entries = [];
    const addSteps = (steps, workflow, chain) => {
      for (const step of steps ?? []) entries.push({ workflow, chain, step });
    };
    for (const workflow of pack.workflows ?? []) {
      if (workflow.chains?.length) {
        for (const chain of workflow.chains) addSteps(chain.steps, workflow, chain);
      }
      addSteps(workflow.steps, workflow);
    }
    for (const chain of pack.chains ?? []) addSteps(chain.steps, void 0, chain);
    addSteps(pack.steps);
    addSteps(pack.prompts);
    addSteps(pack.queue);
    return entries;
  }
  function queuePackStepHeader(pack, entry, index, total) {
    const lines = [
      "ION_QUEUE_PACK_STEP",
      `pack: ${queuePackTitle(pack)}`,
      pack.objective ? `objective: ${queuePackLine(pack.objective)}` : "",
      entry.workflow?.title || entry.workflow?.id ? `workflow: ${queuePackLine(entry.workflow.title || entry.workflow.id)}` : "",
      entry.chain?.title || entry.chain?.id ? `chain: ${queuePackLine(entry.chain.title || entry.chain.id)}` : "",
      `step: ${index + 1}/${total}`,
      entry.step.title || entry.step.id ? `title: ${queuePackLine(entry.step.title || entry.step.id)}` : "",
      entry.step.tags?.length ? `tags: ${entry.step.tags.map(queuePackLine).filter(Boolean).join(", ")}` : ""
    ].filter(Boolean);
    return `${lines.join("\n")}\n`;
  }
  function queuePackMessages(pack, textEntries = /* @__PURE__ */ new Map()) {
    if (pack.schema_id !== QUEUE_PACK_SCHEMA_ID) {
      throw new Error(`Queue pack schema must be ${QUEUE_PACK_SCHEMA_ID}.`);
    }
    const entries = collectQueuePackSteps(pack);
    const includeHeaders = pack.queue_behavior?.include_step_headers !== false;
    const messages = [];
    for (let index = 0; index < entries.length && messages.length < QUEUE_PACK_MAX_MESSAGES; index += 1) {
      const entry = entries[index];
      const body = queuePackStepText(entry.step, textEntries).slice(0, QUEUE_PACK_MAX_PROMPT_CHARS).trim();
      if (!body) continue;
      messages.push(includeHeaders ? `${queuePackStepHeader(pack, entry, index, entries.length)}\n${body}` : body);
    }
    if (!messages.length) throw new Error("Queue pack did not contain any prompt text.");
    return messages;
  }
  function parseQueuePackJson(text, textEntries = /* @__PURE__ */ new Map()) {
    const pack = JSON.parse(text);
    const messages = queuePackMessages(pack, textEntries);
    const truncated = collectQueuePackSteps(pack).length > messages.length ? ` Loaded first ${messages.length} bounded steps.` : "";
    const autoplayNote = pack.queue_behavior?.auto_play_requested ? " Auto Play was requested by the pack, but manual start remains required." : "";
    return {
      pack,
      messages,
      status: `Imported ${messages.length} prompt(s) from ${queuePackTitle(pack)}.${truncated}${autoplayNote}`
    };
  }
  function findZipEndOfCentralDirectory(view) {
    const min = Math.max(0, view.byteLength - 66e3);
    for (let offset = view.byteLength - 22; offset >= min; offset -= 1) {
      if (view.getUint32(offset, true) === 101010256) return offset;
    }
    return -1;
  }
  async function inflateZipPayload(payload, method) {
    if (method === 0) return payload;
    if (method !== 8) throw new Error(`Unsupported ZIP compression method ${method}.`);
    const streamCtor = globalThis.DecompressionStream;
    if (!streamCtor) throw new Error("This browser cannot decompress ZIP entries.");
    for (const format of ["deflate-raw", "deflate"]) {
      try {
        const stream = new Blob([payload]).stream().pipeThrough(new streamCtor(format));
        return await new Response(stream).arrayBuffer();
      } catch {
      }
    }
    throw new Error("ZIP entry decompression failed.");
  }
  async function readQueuePackZipTextEntries(buffer) {
    const view = new DataView(buffer);
    const eocd = findZipEndOfCentralDirectory(view);
    if (eocd < 0) throw new Error("ZIP manifest not found.");
    const entryCount = view.getUint16(eocd + 10, true);
    let cursor = view.getUint32(eocd + 16, true);
    const decoder = new TextDecoder();
    const entries = [];
    for (let index = 0; index < entryCount && cursor < view.byteLength; index += 1) {
      if (view.getUint32(cursor, true) !== 33639248) break;
      const method = view.getUint16(cursor + 10, true);
      const compressedSize = view.getUint32(cursor + 20, true);
      const uncompressedSize = view.getUint32(cursor + 24, true);
      const nameLength = view.getUint16(cursor + 28, true);
      const extraLength = view.getUint16(cursor + 30, true);
      const commentLength = view.getUint16(cursor + 32, true);
      const localOffset = view.getUint32(cursor + 42, true);
      const name = normalizeQueuePackPath(decoder.decode(buffer.slice(cursor + 46, cursor + 46 + nameLength)));
      if (name && /\.(json|md|txt)$/i.test(name) && uncompressedSize <= QUEUE_PACK_MAX_TEXT_ENTRY_BYTES && !name.includes("__MACOSX/")) {
        entries.push({ name, method, compressedSize, uncompressedSize, localOffset });
      }
      cursor += 46 + nameLength + extraLength + commentLength;
    }
    const texts = /* @__PURE__ */ new Map();
    for (const entry of entries) {
      if (view.getUint32(entry.localOffset, true) !== 67324752) continue;
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
  async function parseQueuePackZip(file) {
    const texts = await readQueuePackZipTextEntries(await file.arrayBuffer());
    const manifestPath = texts.has(QUEUE_PACK_MANIFEST_NAME) ? QUEUE_PACK_MANIFEST_NAME : Array.from(texts.keys()).find((path) => path.endsWith(`/${QUEUE_PACK_MANIFEST_NAME}`));
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
  async function parseQueuePackFile(file) {
    const lowerName = file.name.toLowerCase();
    if (lowerName.endsWith(".zip") || /zip/i.test(file.type)) return parseQueuePackZip(file);
    return parseQueuePackJson(await file.text());
  }
  async function importQueuePackFile(file) {
    setBridgeMessageQueueState({ status: `Importing queue pack: ${file.name}` });
    try {
      const result = await parseQueuePackFile(file);
      window.dispatchEvent(new CustomEvent("ion-chatops-message-queue-add", {
        detail: {
          messages: result.messages,
          status: result.status,
          source: "pack",
          pack_id: result.pack.pack_id,
          title: result.pack.title
        }
      }));
      setBridgeMessageQueueState({ status: result.status });
    } catch (error) {
      setBridgeMessageQueueState({ status: `Queue pack import blocked: ${error instanceof Error ? error.message : String(error)}` });
    }
  }
  function dispatchPromptToComposer(mode) {
    const state = bridgeState.promptLibrary;
    const text = state.draftText.trim();
    if (!text) {
      setBridgePromptLibraryState({ status: "Prompt text is empty." });
      return;
    }
    window.dispatchEvent(new CustomEvent("ion-chatops-prompt-insert", { detail: { text, mode } }));
    markPromptUsed(state.selectedId, mode === "append" ? "Prompt appended to composer." : "Prompt inserted into composer.");
  }
  function renderPromptLibraryPanel(panel = ensurePanel()) {
    const state = bridgeState.promptLibrary;
    const statusNode = panel.querySelector('[data-prompts="status"]');
    const queryNode = panel.querySelector('[data-prompts="query"]');
    const categoryNode = panel.querySelector('[data-prompts="category"]');
    const listNode = panel.querySelector('[data-prompts="list"]');
    const titleNode = panel.querySelector('[data-prompts="title"]');
    const draftCategoryNode = panel.querySelector('[data-prompts="draft-category"]');
    const tagsNode = panel.querySelector('[data-prompts="tags"]');
    const textNode = panel.querySelector('[data-prompts="text"]');
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

  function compactMetric(value) {
    if (!Number.isFinite(value) || value <= 0) return "0";
    if (value >= 1e6) return `${(value / 1e6).toFixed(1)}m`;
    if (value >= 1e4) return `${Math.round(value / 1e3)}k`;
    if (value >= 1e3) return `${(value / 1e3).toFixed(1)}k`;
    return String(Math.round(value));
  }
  function queueCounts(queue) {
    const visible = queue.items.filter((item) => item.status !== "sent");
    return {
      pending: visible.length,
      files: visible.filter((item) => item.kind === "files").length,
      active: visible.filter((item) => item.status === "sending" || item.status === "waiting").length
    };
  }
  function renderPanel(panel = ensurePanel()) {
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
      const modeMemory = bridgeState.modeMemory;
      panel.dataset.operationalMode = modeMemory.currentMode;
      positionPanelAboveComposer(panel);
      const titleNode = panel.querySelector(".ion-title");
      const modeNode = panel.querySelector("[data-mode-memory]");
      const modePill = panel.querySelector("[data-mode-pill]");
      const modeSummary = panel.querySelector("[data-mode-summary]");
      if (titleNode) titleNode.textContent = bridgeState.title;
      if (modeNode) {
        modeNode.title = modeMemoryDetail(modeMemory);
        modeNode.setAttribute("aria-label", `Open ION mode memory: ${modeMemory.currentMode}`);
      }
      if (modePill) modePill.textContent = modeBadgeLabel(modeMemory.currentMode);
      if (modeSummary) modeSummary.textContent = modeMemorySummary(modeMemory);
    const queue = bridgeState.messageQueue;
    const onboard = bridgeState.onboard;
    const onboardButton = panel.querySelector('[data-tool="insert-reentry"]');
    const onboardLabel = panel.querySelector("[data-onboard-label]");
    const autoAcceptButton = panel.querySelector('[data-tool="gateway-auto-accept"]');
    const autoAcceptLabel = panel.querySelector("[data-auto-accept-label]");
    const autoAcceptTimer = panel.querySelector("[data-auto-accept-timer]");
    const autoAcceptTtlInput = panel.querySelector("[data-auto-accept-ttl-input]");
    const autoAcceptActive = queue.autoAcceptActive;
    if (autoAcceptButton) {
      autoAcceptButton.dataset.active = String(autoAcceptActive);
      autoAcceptButton.title = autoAcceptActive ? `ION Action auto-accept is on until ${queue.autoAcceptUntil}. Click the timer to change TTL, or toggle the switch to turn off.` : `ION Action auto-accept is off. Click the toggle to allow safe browser queue packets for ${Math.round(queue.autoAcceptTtlSeconds / 60)} minutes.`;
    }
    if (autoAcceptLabel) autoAcceptLabel.textContent = autoAcceptActive ? "ON" : "OFF";
    if (autoAcceptTimer) {
      autoAcceptTimer.textContent = autoAcceptActive ? queue.autoAcceptUntil || "..." : "SET";
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
          "Click to insert the latest ION onboarding/re-entry context protocol into ChatGPT."
        ].filter(Boolean).join("\n");
      }
      if (onboardLabel) {
        onboardLabel.textContent = onboard.state === "synced" ? `${onboard.project} v${onboard.version} synced` : `${onboard.project} v${onboard.version}`;
      }
      const monitor = bridgeState.monitor;
      const queueSummary = queueCounts(queue);
      const monitorStrip = panel.querySelector('[data-monitor="strip"]');
      const monitorMessagesNode = panel.querySelector('[data-monitor="messages"]');
      const monitorChatNode = panel.querySelector('[data-monitor="chat"]');
      const monitorActionsNode = panel.querySelector('[data-monitor="actions"]');
      const monitorQueueNode = panel.querySelector('[data-monitor="queue"]');
      const monitorConnectedNode = panel.querySelector('[data-monitor="connected"]');
      const monitorLagNode = panel.querySelector('[data-monitor="lag"]');
      const monitorDomNode = panel.querySelector('[data-monitor="dom"]');
      if (monitorStrip) {
        monitorStrip.dataset.tone = monitor.tone;
        monitorStrip.title = monitor.summary;
      }
      if (monitorMessagesNode) {
        monitorMessagesNode.textContent = `Msgs A${compactMetric(monitor.assistantMessageCount)} U${compactMetric(monitor.userMessageCount)}`;
        monitorMessagesNode.title = `${monitor.messageCount.toLocaleString()} visible conversation item(s): ${monitor.assistantMessageCount.toLocaleString()} assistant, ${monitor.userMessageCount.toLocaleString()} user. Counts are loaded DOM only.`;
      }
      if (monitorChatNode) {
        monitorChatNode.textContent = `Loaded ${compactMetric(monitor.estimatedTokens)} tok · ${monitor.plusPercent}%/32k ref`;
        monitorChatNode.title = `Loaded browser transcript estimate, not exact model context: ${monitor.estimatedTokens.toLocaleString()} tokens · 128k reference: ${monitor.proPercent}% · 256k reference: ${monitor.thinkingPercent}%`;
      }
      if (monitorActionsNode) {
        monitorActionsNode.textContent = `Actions ${compactMetric(monitor.actionCandidateCount)}`;
        monitorActionsNode.title = `ION action/code scan: ${monitor.validActionCount} valid · ${monitor.blockedActionCount} blocked · ${monitor.duplicateActionCount} duplicate · ${monitor.codeBlockCount} code block(s).`;
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
      if (monitorLagNode) {
        monitorLagNode.textContent = `Lag ${Math.round(Math.max(monitor.lagMs, monitor.longTaskMs))}ms`;
        monitorLagNode.title = `Event-loop lag: ${Math.round(monitor.lagMs)}ms · Long task: ${Math.round(monitor.longTaskMs)}ms`;
      }
      if (monitorDomNode) {
        monitorDomNode.textContent = `DOM ${compactMetric(monitor.domNodes)}`;
        monitorDomNode.title = `${monitor.domNodes.toLocaleString()} DOM elements loaded in this page`;
      }
      const activeTab = panel.dataset.tab ?? "status";
      panel.querySelectorAll(".ion-tab").forEach((tab) => {
        tab.dataset.active = String(tab.dataset.tab === activeTab);
      });
      ensureSettingsControlPad();
      bindSettingsPadEvents();
      syncSettingsControlPadState(panel);
      panel.querySelectorAll(".ion-tab-panel").forEach((tabPanel) => {
        tabPanel.dataset.active = String(tabPanel.dataset.panel === activeTab);
      });
      const layoutTarget = readLayoutTarget();
      panel.querySelectorAll("[data-tool^='settings-target-']").forEach((button) => {
        const tool = button.dataset.tool ?? "";
        const target = tool.endsWith("top") ? "top_rail" : tool.endsWith("drawer") ? "drawer" : "tabs";
        button.dataset.active = String(target === layoutTarget);
      });
      const statusNode = panel.querySelector('[data-field="status"]');
      const actionNode = panel.querySelector('[data-field="action"]');
      const agentNode = panel.querySelector('[data-field="agent"]');
      const packagesNode = panel.querySelector('[data-field="packages"]');
      const sandboxNode = panel.querySelector('[data-field="sandbox"]');
      const automationNode = panel.querySelector('[data-field="automation"]');
      const artifactsNode = panel.querySelector('[data-field="artifacts"]');
      const settingsNode = panel.querySelector('[data-field="settings"]');
      const inspectorSelect = panel.querySelector('[data-control="settings-inspector-layer"]');
      const diagnosticsNode = panel.querySelector('[data-field="diagnostics"]');
      const toolsNode = panel.querySelector('[data-field="tools"]');
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
          onboard.detail
        ].join("\n");
        diagnosticsNode.textContent = `${monitor.detail}\n\n${onboardDetail}\n\n${bridgeState.anchor.detail}\n\n${bridgeState.diagnostics}`;
      }
      if (toolsNode) {
        toolsNode.textContent = `${bridgeState.tools}\n\nRecent:\n${bridgeState.logs.join("\n") || "No events yet."}`;
      }
    } finally {
      renderingPanel = false;
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
    updateModeMemory(title, detail, tone);
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

  function setBridgeCodexState(nextState) {
    bridgeState.codex = {
      ...bridgeState.codex,
      ...nextState,
      turns: nextState.turns ?? bridgeState.codex.turns,
    };
    renderPanel();
  }

  function setBridgeMessageQueueState(nextState) {
    bridgeState.messageQueue = {
      ...bridgeState.messageQueue,
      ...nextState,
      items: nextState.items ?? bridgeState.messageQueue.items
    };
    renderPanel();
  }

  function setBridgePromptLibraryState(nextState) {
    bridgeState.promptLibrary = {
      ...bridgeState.promptLibrary,
      ...nextState,
      items: nextState.items ?? bridgeState.promptLibrary.items
    };
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

  function setBridgeSettingsDetail(detail) {
    bridgeState.settings = detail;
    renderPanel();
  }

  function setBridgeDocsState(nextState) {
    bridgeState.docs = {
      ...bridgeState.docs,
      ...nextState,
      roots: nextState.roots ?? bridgeState.docs.roots,
      entries: nextState.entries ?? bridgeState.docs.entries,
    };
    renderPanel();
  }

  function setBridgeProjectsState(nextState) {
    const current = bridgeState.projects;
    const packages = nextState.packages ?? current.packages;
    const selectedPaths = nextState.selectedPaths ?? current.selectedPaths ?? [];
    const knownPaths = new Set(packages.map((entry) => entry.path));
    bridgeState.projects = {
      ...current,
      ...nextState,
      roots: nextState.roots ?? current.roots,
      packages,
      selectedPaths: selectedPaths.filter((path) => !knownPaths.size || knownPaths.has(path))
    };
    renderPanel();
  }

  function setBridgeDocsFavorites(nextFavorites) {
    docsFavoriteRoots = nextFavorites;
    renderPanel();
  }

  function setBridgeMonitorMetrics(nextState) {
    bridgeState.monitor = {
      ...bridgeState.monitor,
      ...nextState
    };
    renderPanel();
  }

  function docsStateSummary() {
    const docs = bridgeState.docs;
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

  function asRecord(value) {
    return value && typeof value === "object" && !Array.isArray(value) ? value : {};
  }

  function asArray(value) {
    return Array.isArray(value) ? value : [];
  }

  function shortJson(value, limit = 900) {
    const text = typeof value === "string" ? value : JSON.stringify(value ?? {}, null, 2);
    return text.length > limit ? `${text.slice(0, limit)}\n...` : text;
  }

  function latestCodexTurnWithEngine(turns) {
    for (let index = turns.length - 1; index >= 0; index -= 1) {
      if (turns[index]?.chat_engine || turns[index]?.context_refs?.length) return turns[index];
    }
    return turns.length ? turns[turns.length - 1] : null;
  }

  function appendCodexCard(parent, title, lines) {
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

  function renderCodexContextView(parent, codex) {
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

  function renderCodexPanel(panel = ensurePanel()) {
    const codex = bridgeState.codex;
    const statusNode = panel.querySelector('[data-codex="status"]');
    const turnsNode = panel.querySelector('[data-codex="turns"]');
    const contextNode = panel.querySelector('[data-codex="context"]');
    const inputNode = panel.querySelector('[data-codex="input"]');
    panel.querySelectorAll("[data-codex-view]").forEach((button) => {
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

  function renderDocsPanel(panel = ensurePanel()) {
    const docs = bridgeState.docs;
    const favoritesNode = panel.querySelector('[data-docs="favorites"]');
    const rootList = panel.querySelector('[data-docs="roots"]');
    const breadcrumbNode = panel.querySelector('[data-docs="breadcrumbs"]');
    const entriesNode = panel.querySelector('[data-docs="entries"]');
    const statusNode = panel.querySelector('[data-docs="status"]');
    const searchNode = panel.querySelector('[data-docs-control="search"]');
    const treeNode = panel.querySelector('[data-docs="tree"]');
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
        thumb.style.background = "linear-gradient(160deg, rgba(255,255,255,0.18), rgba(255,255,255,0.05))";
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
      const optionGroups = new Map();
      let homeFound = false;
      for (const option of DOCS_TREE_LOCATIONS) {
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
      if (!homeFound) treeNode.value = docs.currentRoot ?? "";
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
      setExplicitOperationalMode("APPROVAL_MODAL", "Approval modal", `${action.intent}: ${action.action_id}`);
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
      setExplicitOperationalMode("APPROVAL_MODAL", "Approval modal", operation);
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
        node.closest(`#${SETTINGS_CONTROL_PAD_ID}`) ??
        node.closest(`#${MESSAGE_QUEUE_FILE_INPUT_ID}`) ??
        node.closest(`#${CHATGPT_LEFT_ICON_DOCK_ID}`) ??
        node.closest(`.${CHATGPT_LEFT_ICON_DOCK_CLASS}`) ??
        node.closest(`.${ASSET_CAPTURE_BUTTON_CLASS}`) ??
        node.closest("[data-message-author-role='user']") ??
        node.closest("#prompt-textarea") ??
        node.closest("[contenteditable='true']") ??
        node.closest("textarea")
    );
  }

  function concreteIonFieldValue(text, key) {
    const match = text.match(new RegExp(`^\\s+${key}\\s*:\\s*(.+?)\\s*(?:#.*)?$`, "im"));
    const value = match?.[1]?.trim().replace(/^['"]|['"]$/g, "") ?? "";
    if (!value || value === "..." || /^<[^>]+>$/.test(value) || /^TODO|TBD$/i.test(value)) return "";
    return value;
  }
  function isIonActionPacketCandidateText(text) {
    const yaml = extractIonActionYaml(text);
    if (!yaml) return false;
    if (!concreteIonFieldValue(yaml, "schema").match(/^ion\.chatops\.action\.v1$/)) return false;
    if (!concreteIonFieldValue(yaml, "action_id")) return false;
    if (!concreteIonFieldValue(yaml, "intent")) return false;
    const hasActor = /^\s+actor\s*:\s*(?:#.*)?$/im.test(yaml) || Boolean(concreteIonFieldValue(yaml, "callsign") || concreteIonFieldValue(yaml, "carrier"));
    const hasAuthority = /^\s+authority\s*:\s*(?:#.*)?$/im.test(yaml) || Boolean(
      concreteIonFieldValue(yaml, "human_sovereign") ||
        concreteIonFieldValue(yaml, "requires_approval") ||
        concreteIonFieldValue(yaml, "production_authority") ||
        concreteIonFieldValue(yaml, "live_execution_authority")
    );
    return hasActor && hasAuthority;
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

  function normalizeDocsStateFromResponse(result) {
    const incomingEntries = Array.isArray(result?.entries) ? result.entries : [];
    const entries = incomingEntries
      .map((row) => ({
        kind: row?.kind === "file" ? "file" : "folder",
        name: String(row?.name || row?.path || "").trim(),
        path: String(row?.path || "").trim(),
        size_bytes: typeof row?.size_bytes === "number" ? row.size_bytes : undefined,
        thumbnail: typeof row?.thumbnail === "string" ? row.thumbnail : undefined,
      }))
      .filter((entry) => entry.path);
    return {
      roots: Array.isArray(result?.roots) ? result.roots.filter((row) => typeof row === "string" && row.trim()) : defaultDocsState.roots,
      currentRoot: String(result?.current_root ?? result?.currentRoot ?? docsState.currentRoot ?? ""),
      currentPath: String(result?.path ?? result?.current_path ?? docsState.currentPath ?? ""),
      query: String(result?.query ?? docsState.query ?? ""),
      breadcrumbs: Array.isArray(result?.breadcrumbs) ? result.breadcrumbs.filter((row) => typeof row === "string") : [],
      entries,
      selectedPath: String(result?.selected_path ?? result?.selectedPath ?? docsState.selectedPath ?? ""),
      selectedDocName: String(result?.selected_doc_name ?? result?.selectedDocName ?? docsState.selectedDocName ?? ""),
      status: String(result?.status ?? docsState.status ?? "Docs browser updated."),
    };
  }

  function requestDocsBrowse(params = {}) {
    const payload = {
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

  function requestDocsOpenRoot(event) {
    const path = event?.detail?.path;
    docsState.currentPath = path ? path : "";
    docsState.currentRoot = path || "";
    docsState.query = "";
    requestDocsBrowse({ path: docsState.currentPath, root: docsState.currentRoot });
  }

  function requestDocsOpenFolder(detail) {
    const path = (detail?.path ?? "").trim();
    if (!path) {
      requestDocsOpenRoot();
      return;
    }
    docsState.currentPath = path;
    requestDocsBrowse({ path, query: detail.query ?? docsState.query, root: docsState.currentRoot });
  }

  function requestDocsOpenParent() {
    if (!docsState.currentPath) {
      requestDocsOpenRoot();
      return;
    }
    const parts = docsState.currentPath.split("/").filter(Boolean);
    const parent = parts.slice(0, -1).join("/");
    docsState.currentPath = parent;
    requestDocsBrowse({ path: parent, root: docsState.currentRoot });
  }

  function requestDocsSearch(query) {
    docsState.query = query;
    requestDocsBrowse({ path: docsState.currentPath, query, root: docsState.currentRoot });
  }

  function setDocsStatus(status) {
    docsState = { ...docsState, status };
    setBridgeDocsState(docsState);
  }

  function setDocsFavoriteStatus(path, status) {
    docsDropFavoritePath = path;
    const favorites = docsFavoriteRoots.map((favorite) => favorite.path === path ? { ...favorite, status } : favorite);
    setBridgeDocsFavorites(favorites);
  }

  function stopDocsDropProgress() {
    if (docsDropProgressTimer !== null) {
      window.clearInterval(docsDropProgressTimer);
      docsDropProgressTimer = null;
    }
  }

  function startDocsDropProgress(label) {
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

  function requestDocsDrop(path) {
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

  function docsBrowsePromise(path) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({
        type: "ion_chatops_docs_browse",
        payload: {
          path,
          root: path,
          query: ""
        }
      }, (response) => resolve(response));
    });
  }
  function contextPackageProjectKey(name) {
    const clean = name.replace(/\.(zip|tar|gz|json|md)$/i, "").replace(/[_-]?\d{8}(?:[_-]\d{4,6})?$/i, "").replace(/[_-]?v\d+(?:[._-]\d+)*(?:[_-]?[a-z]+)?$/i, "").replace(/[_-]?context[_-]?package$/i, "").replace(/[_-]+/g, " ").trim();
    return clean || name;
  }
  function contextPackageVersion(name) {
    const version = name.match(/\bv\d+(?:[._-]\d+)*/i)?.[0] ?? "";
    const date = name.match(/\b20\d{6}(?:[_-]\d{4,6})?\b/)?.[0] ?? "";
    return [version, date].filter(Boolean).join(" · ") || "latest";
  }
  function contextPackageScore(name) {
    const date = name.match(/\b(20\d{6})(?:[_-](\d{4,6}))?\b/);
    const dateScore = date ? Number(`${date[1]}${(date[2] ?? "000000").padEnd(6, "0")}`) : 0;
    const version = name.match(/\bv(\d+(?:[._-]\d+)*)/i)?.[1] ?? "";
    const versionScore = version.split(/[._-]/).filter(Boolean).slice(0, 4).reduce((score, part) => score * 1e3 + (Number.parseInt(part, 10) || 0), 0);
    return dateScore * 1e9 + versionScore;
  }
  function isIonContextPackage(entry) {
    const text = `${entry.name} ${entry.path}`.toLowerCase();
    return entry.kind === "folder" || text.includes("context") || text.includes("package") || text.includes("capsule") || text.endsWith(".zip");
  }
  function latestProjectPackages(entries) {
    const latest = new Map();
    for (const entry of entries) {
      const key = entry.project.toLowerCase();
      const existing = latest.get(key);
      if (!existing || entry.score > existing.score || entry.score === existing.score && entry.name > existing.name) {
        latest.set(key, entry);
      }
    }
    return Array.from(latest.values()).map((entry) => ({ ...entry, latest: true })).sort((a, b) => b.score - a.score || a.project.localeCompare(b.project));
  }
  async function requestProjectsRefresh() {
    setBridgeStatus("Projects scan", "Scanning ION context-package folders.", "working");
    setBridgeProjectsState({
      status: "Scanning ION context-package folders...",
      roots: PROJECT_CONTEXT_PACKAGE_ROOTS,
      packages: projectPackages,
      selectedPath: selectedProjectPackagePath,
      selectedPaths: selectedProjectPackagePaths
    });
    const discovered = [];
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
          score: contextPackageScore(name)
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
      status: projectPackages.length ? `Found ${projectPackages.length} latest ION project context package(s). Use Context Sync to build one ZIP, or double-click a project to zip/drop it.` : "No ION context packages found in known package roots.",
      roots: PROJECT_CONTEXT_PACKAGE_ROOTS,
      packages: projectPackages,
      selectedPath: selectedProjectPackagePath,
      selectedPaths: selectedProjectPackagePaths,
      contextSyncStatus: projectPackages.length ? `${selectedProjectPackagePaths.length} project package(s) selected for context sync.` : "No ION context packages found in known package roots."
    });
    setBridgeStatus(projectPackages.length ? "Projects ready" : "Projects empty", `${projectPackages.length} latest package(s)`, projectPackages.length ? "success" : "approval");
  }
  function requestProjectDrop(path) {
    selectedProjectPackagePath = path || selectedProjectPackagePath;
    setBridgeProjectsState({ selectedPath: selectedProjectPackagePath, status: `Preparing project package drop: ${selectedProjectPackagePath}` });
    requestDocsDrop(selectedProjectPackagePath);
  }

  function requestProjectContextSync(paths) {
    const projectPaths = Array.from(new Set(paths.map((path) => String(path ?? "").trim()).filter(Boolean)));
    if (!projectPaths.length) {
      setBridgeProjectsState({
        contextSyncOpen: true,
        contextSyncStatus: "Select at least one ION project context package before building a context sync ZIP."
      });
      setBridgeStatus("Context sync blocked", "No project packages selected.", "error");
      return;
    }
    selectedProjectPackagePaths = projectPaths;
    setBridgeProjectsState({
      selectedPaths: projectPaths,
      contextSyncOpen: true,
      contextSyncStatus: `Requesting Braden approval for one context sync ZIP from ${projectPaths.length} project package(s)...`
    });
    setBridgeStatus("Context sync ZIP", "Requesting Braden approval before local package compilation.", "working");
    chrome.runtime.sendMessage({
      type: "ion_chatops_project_context_sync_zip",
      payload: {
        project_paths: projectPaths,
        context_sync_source: "top_bar_context_sync"
      }
    }, async (response) => {
      const result = response?.result;
      const detail = response?.ok ? [
        `zip_path: ${result?.zip_path ?? ""}`,
        `zip_sha256: ${result?.zip_sha256 ?? ""}`,
        `manifest_path: ${result?.manifest_path ?? ""}`,
        `receipt_path: ${result?.receipt_path ?? ""}`,
        `selected_project_count: ${result?.selected_project_count ?? projectPaths.length}`
      ].join("\n") : blockedDetail(response);
      setBridgeProjectsState({
        selectedPaths: projectPaths,
        contextSyncOpen: true,
        contextSyncStatus: response?.ok ? `Context sync ZIP ready for ${projectPaths.length} project package(s).` : detail,
        contextSyncZipPath: response?.ok ? String(result?.zip_path ?? "") : "",
        contextSyncSha256: response?.ok ? String(result?.zip_sha256 ?? "") : ""
      });
      setBridgePackageDetail(response?.ok ? `${detail}\n\n${compactJson(result, 1400)}` : detail);
      setBridgeStatus(response?.ok ? "Context sync ZIP ready" : "Context sync blocked", detail, response?.ok ? "success" : "error");
      if (response?.ok) await copyBridgeResult("Context sync ZIP", detail);
    });
  }

  function codexTurnsFromModel(model) {
    const turns = model?.lanes?.codex_general?.turns;
    if (!Array.isArray(turns)) return [];
    return turns
      .filter((turn) => turn && typeof turn === "object")
      .map((turn) => ({
        turn_id: String(turn.turn_id ?? ""),
        author: String(turn.author ?? turn.kind ?? "codex"),
        kind: String(turn.kind ?? ""),
        message: String(turn.message ?? ""),
        created_at: String(turn.created_at ?? ""),
        chat_engine: turn.chat_engine && typeof turn.chat_engine === "object" ? turn.chat_engine : undefined,
        context_refs: Array.isArray(turn.context_refs) ? turn.context_refs.map((ref) => String(ref)) : undefined,
        skill_activation: turn.skill_activation && typeof turn.skill_activation === "object" ? turn.skill_activation : undefined,
        codex_model_move: turn.codex_model_move && typeof turn.codex_model_move === "object" ? turn.codex_model_move : undefined,
      }))
      .filter((turn) => turn.message);
  }

  function requestCodexChatModel() {
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

  function requestCodexChatTurn(message) {
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

  function requestCodexChatQueue(message) {
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
      const nextState = {
        status: `Queued for Codex: ${link.request_id ?? "request created"}`,
        input: "",
        queueing: false,
      };
      if (model) nextState.turns = codexTurnsFromModel(model);
      if (model) nextState.model = model;
      setBridgeCodexState(nextState);
    });
  }

  function requestDocsOpenDoc(path, name) {
    docsState.selectedPath = path;
    docsState.selectedDocName = name;
    setBridgeDocsState({ ...docsState, selectedPath: path, selectedDocName: name, status: `Selected ${name}` });
  }

  function normalizeDocsArtifactPath(rawPath) {
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

  function visibleDropRect(element) {
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
      };
    }
    return rect;
  }

  function dropZoneContainerFromElement(element) {
    const composer = findComposer();
    const start = composer && elementContains(element, composer) ? composer : element;
    const candidates = [
      start.closest("form"),
      start.closest("[data-testid*='composer' i]"),
      start.closest("[class*='composer' i]"),
      start.closest("[class*='prompt' i]"),
      start.parentElement,
      element
    ].filter(Boolean);
    for (const candidate of candidates) {
      if (isBridgeElement(candidate)) continue;
      const rect = candidate.getBoundingClientRect();
      if (rect.width >= 300 && rect.height >= 54 && rect.bottom > window.innerHeight * 0.45) return candidate;
    }
    return element;
  }

  function readStoredTargetMeta(raw, fallbackAnchor) {
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

  function targetMetaStorageKey(target) {
    if (target === "attach_target") return ATTACH_TARGET_SELECTOR_KEY;
    if (target === "drop_zone") return DROP_TARGET_SELECTOR_KEY;
    return TABS_ANCHOR_SELECTOR_KEY;
  }

  function attachTargetMeta() {
    return readStoredTargetMeta(rawAttachSelector(), TARGET_ANCHOR_DEFAULTS.attach_target);
  }

  function dropTargetMeta() {
    return readStoredTargetMeta(rawDropSelector(), TARGET_ANCHOR_DEFAULTS.drop_zone);
  }

  function tabsAnchorMeta() {
    return readStoredTargetMeta(rawTabsAnchorSelector(), TARGET_ANCHOR_DEFAULTS.tabs_anchor);
  }

  function targetMeta(target) {
    if (target === "attach_target") return attachTargetMeta();
    if (target === "drop_zone") return dropTargetMeta();
    return tabsAnchorMeta();
  }

  function saveTargetMeta(target, selector, anchor) {
    const point = anchor === "top" || anchor === "left" || anchor === "center" || anchor === "right" || anchor === "bottom" ? anchor : "center";
    const key = targetMetaStorageKey(target);
    try {
      window.localStorage?.setItem(
        key,
        JSON.stringify({
          selector: String(selector ?? "").trim(),
          anchor: point,
        }),
      );
      return true;
    } catch (_error) {
      return false;
    }
  }

  function clearTargetMeta(target) {
    const storage = window.localStorage ?? window.sessionStorage;
    const key = targetMetaStorageKey(target);
    try {
      if (storage) storage.removeItem(key);
      return true;
    } catch (_error) {
      return false;
    }
  }

  function anchorForTarget(target) {
    return targetMeta(target).anchor;
  }

  function setInspectorAnchorTarget(target) {
    settingsInspectorTarget = target;
    settingsAnchorPoint = anchorForTarget(target);
  }

  function markerPointForRect(rect, anchor) {
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

  function addAnchorMarker(overlay, rect, anchor, borderColor) {
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

  function markerForTarget(target) {
    if (target === "tabs_anchor") return "#fb923c";
    if (target === "drop_zone") return "#60a5fa";
    return "#34d399";
  }

  function rawDropSelector() {
    try {
      return String(window.localStorage?.getItem(DROP_TARGET_SELECTOR_KEY) ?? "").trim();
    } catch (_error) {
      return "";
    }
  }

  function rawAttachSelector() {
    try {
      return String(window.localStorage?.getItem(ATTACH_TARGET_SELECTOR_KEY) ?? "").trim();
    } catch (_error) {
      return "";
    }
  }

  function rawTabsAnchorSelector() {
    try {
      return String(window.localStorage?.getItem(TABS_ANCHOR_SELECTOR_KEY) ?? "").trim();
    } catch (_error) {
      return "";
    }
  }

  function storedDropSelector() {
    return rawDropSelector();
  }

  function calibratedDropTargetElement() {
    const selector = storedDropSelector();
    if (!selector) return null;
    let node = null;
    try {
      node = document.querySelector(selector);
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

  function defaultDropTargetElement() {
    const composer = findComposer();
    const main = document.querySelector("main");
    const composerDropZone = composer ? dropZoneContainerFromElement(composer) : null;
    const composerShell =
      composer?.closest("form") ??
      composer?.closest("[data-testid*='composer']") ??
      null;
    const composerForm = composer?.closest("form");
    const composerRoot = composer?.closest("[role='region'], [data-testid*='composer']");
    const candidates = [composerDropZone, composerShell, composerForm, composerRoot, composer?.parentElement, main, document.body, composer].filter(Boolean);
    return candidates.find((candidate) => visibleDropRect(candidate)) ?? null;
  }

  function findDropTarget() {
    const calibrated = calibratedDropTargetElement();
    if (calibrated) return calibrated;
    if (storedDropSelector()) return null;
    return defaultDropTargetElement();
  }

  function composerRect() {
    const composer = findComposer();
    return composer?.getBoundingClientRect() ?? null;
  }

  function composerShellRect() {
    const composer = findComposer();
    if (!composer) return null;
    let best = composer;
    let current = composer;
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

  function rectPayload(rect) {
    return {
      x: Math.round(rect.left),
      y: Math.round(rect.top),
      width: Math.round(rect.width),
      height: Math.round(rect.height),
    };
  }

  function controlLabel(node) {
    return `${node.getAttribute("aria-label") ?? ""} ${node.getAttribute("data-testid") ?? ""} ${node.textContent ?? ""}`.replace(/\s+/g, " ").trim();
  }

  function visibleElement(node) {
    const rect = node.getBoundingClientRect();
    return rect.width > 1 && rect.height > 1 && rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
  }

  function cssEscape(value) {
    const css = window.CSS;
    if (typeof css?.escape === "function") return css.escape(value);
    return value.replace(/["\\#.;:[\]()>+~*=\s]/g, "\\$&");
  }

  function cssString(value) {
    return value.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  }

  function storedAttachSelector() {
    try {
      return rawAttachSelector();
    } catch (_error) {
      return "";
    }
  }

  function storedTabsAnchorSelector() {
    try {
      return rawTabsAnchorSelector();
    } catch (_error) {
      return "";
    }
  }

  function elementWithinComposerBand(node, rect) {
    const bounds = node.getBoundingClientRect();
    if (!rect) return bounds.top > window.innerHeight * 0.45;
    const centerX = bounds.left + bounds.width / 2;
    const centerY = bounds.top + bounds.height / 2;
    const xMatch = centerX >= rect.left - 110 && centerX <= rect.right + 110;
    const yMatch = centerY >= rect.top - 260 && centerY <= rect.bottom + 160;
    return xMatch && yMatch;
  }

  function selectorForElement(node) {
    const id = node.id?.trim();
    if (id) return `#${cssEscape(id)}`;
    const tag = node.tagName.toLowerCase();
    const dataTestId = node.getAttribute("data-testid")?.trim();
    if (dataTestId) return `${tag}[data-testid="${cssString(dataTestId)}"]`;
    const aria = node.getAttribute("aria-label")?.trim();
    if (aria) return `${tag}[aria-label="${cssString(aria)}"]`;
    const title = node.getAttribute("title")?.trim();
    if (title) return `${tag}[title="${cssString(title)}"]`;
    const parts = [];
    let current = node;
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

  function inspectorNodeAllowed(node) {
    if (!(node instanceof HTMLElement)) return false;
    if (isBridgeElement(node)) return false;
    if (node.id === INSPECTOR_HUD_ID || node.id === INSPECTOR_SELECTED_PREVIEW_ID) return false;
    if (node.classList.contains(INSPECTOR_OUTLINE_CLASS) || node.classList.contains("ion-dom-badge")) return false;
    if (!visibleElement(node)) return false;
    return true;
  }

  function inspectorLabel(node, index) {
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

  function inspectorLayersAt(x, y) {
    const fromPoint = typeof document.elementsFromPoint === "function" ? document.elementsFromPoint(x, y) : [];
    const seenNodes = new Set();
    const layers = [];
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

  function removeInspectorOutlines() {
    document.querySelectorAll(`.${INSPECTOR_OUTLINE_CLASS}`).forEach((node) => node.remove());
  }

  function removeInspectorHud() {
    document.getElementById(INSPECTOR_HUD_ID)?.remove();
  }

  function removeInspectorSelectedPreview() {
    document.getElementById(INSPECTOR_SELECTED_PREVIEW_ID)?.remove();
  }

  function removeInspectorChrome() {
    removeInspectorOutlines();
    removeInspectorHud();
    removeInspectorSelectedPreview();
  }

  function drawInspectorOutline(layer, selected = false, persistentId, markerAnchor, markerColor = "#ec4899") {
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
      const markerRect = {
        x: layer.rect.x,
        y: layer.rect.y,
        width: layer.rect.width,
        height: layer.rect.height,
      };
      addAnchorMarker(overlay, markerRect, markerAnchor, markerColor);
    }
    document.documentElement.appendChild(overlay);
  }

  function drawInspectorLayers(layers, selectedIndex = -1) {
    removeInspectorOutlines();
    layers.slice(0, 10).forEach((layer) => drawInspectorOutline(layer, layer.index === selectedIndex));
  }

  function updateInspectorHud(x, y, layers, locked = false) {
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

  function publishInspectorLayers() {
    setBridgeInspectorLayers(
      inspectorCapturedLayers.map((layer) => ({ index: layer.index, label: layer.label, selector: layer.selector })),
      inspectorSelectedIndex,
    );
  }

  function inspectorSelectedLayer() {
    return inspectorCapturedLayers.find((layer) => layer.index === inspectorSelectedIndex) ?? inspectorCapturedLayers[0] ?? null;
  }

  function previewInspectorSelectedLayer() {
    ensureDomRegistryStyle();
    removeInspectorSelectedPreview();
    const layer = inspectorSelectedLayer();
    if (!layer) {
      setBridgeSettingsDetail("dom_inspector_no_layer_selected\nStart Inspector, hover the page, and click the target pixel first.");
      setBridgeStatus("Inspector layer missing", "No captured pixel stack is available.", "error");
      return;
    }
    const current = document.querySelector(layer.selector);
    if (current && visibleElement(current)) {
      layer.element = current;
      layer.rect = rectPayload(current.getBoundingClientRect());
      layer.label = inspectorLabel(current, layer.index);
    }
    const anchor = settingsAnchorPoint;
    drawInspectorOutline(layer, true, INSPECTOR_SELECTED_PREVIEW_ID, anchor, markerForTarget(settingsInspectorTarget));
    const detail = [
      "dom_inspector_layer_preview",
      `index: ${layer.index}`,
      `selector: ${layer.selector}`,
      `target: ${settingsInspectorTarget}`,
      `anchor: ${anchor}`,
      `label: ${layer.label}`,
      `rect: ${JSON.stringify(layer.rect)}`,
    ].join("\n");
    setBridgeSettingsDetail(detail);
    setBridgeStatus("Inspector layer previewed", "Pink ring marks the selected captured layer.", "success");
  }

  function saveInspectorSelectedLayer(target) {
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

  function selectInspectorLayer(index) {
    inspectorSelectedIndex = Math.max(0, Math.min(index, Math.max(0, inspectorCapturedLayers.length - 1)));
    publishInspectorLayers();
    previewInspectorSelectedLayer();
  }

  function stopDomInspector(message = "DOM inspector cancelled.") {
    inspectorActive = false;
    inspectorCaptureMode = "single";
    document.removeEventListener("mousemove", domInspectorMouseMove, true);
    document.removeEventListener("click", domInspectorClick, true);
    document.removeEventListener("keydown", domInspectorKeydown, true);
    removeInspectorHud();
    removeInspectorOutlines();
    setBridgeSettingsDetail(message);
  }

  function domInspectorMouseMove(event) {
    if (!inspectorActive) return;
    const bridgeTarget = event.target instanceof Element ? event.target : event.target instanceof Node ? event.target.parentElement : null;
    if (bridgeTarget && isBridgeElement(bridgeTarget)) return;
    ensureDomRegistryStyle();
    const layers = inspectorLayersAt(event.clientX, event.clientY);
    drawInspectorLayers(layers);
    updateInspectorHud(event.clientX, event.clientY, layers);
  }

  function domInspectorClick(event) {
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
      "Use the Settings controls to choose a lower layer, then preview or save it as Tabs Anchor, Drop Zone, or Attach Target.",
    ].join("\n");
    if (inspectorCaptureMode === "single") {
      const message = `${capturedMessage}\nSettings is not active, so inspector stopped after capture.`;
      stopDomInspector(message);
      setBridgeStatus("Inspector layer captured", "Settings is not active. Open Settings to keep inspector open while retargeting.", "success");
    } else {
      setBridgeSettingsDetail(capturedMessage);
      setBridgeStatus("Inspector layer captured", "Settings inspector is active. Click again to replace this capture.", "success");
    }
    previewInspectorSelectedLayer();
  }

  function domInspectorKeydown(event) {
    if (event.key !== "Escape") return;
    event.preventDefault();
    event.stopPropagation();
    stopDomInspector("dom_inspector_cancelled\nInspector was cancelled with Escape.");
    setBridgeStatus("Inspector cancelled", "No anchor changed.", "idle");
  }

  function beginDomInspector(settingsMode = false) {
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

  function setSettingsInspectorMode(enabled) {
    const targetMode = Boolean(enabled);
    if (applyingSettingsInspectorMode) {
      return;
    }
    if (targetMode === (inspectorActive && inspectorCaptureMode === "settings")) {
      return;
    }
    applyingSettingsInspectorMode = true;
    try {
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
    } finally {
      applyingSettingsInspectorMode = false;
    }
  }

  function attachCandidateFromEventTarget(target) {
    if (!(target instanceof Element)) return null;
    if (isBridgeElement(target)) return null;
    const candidate = target.closest("button, [role='button'], input[type='file'], label, [aria-label], [data-testid]");
    if (candidate && !isBridgeElement(candidate)) return candidate;
    return target;
  }

  function dropCandidateFromEventTarget(target) {
    if (!(target instanceof Element)) return null;
    if (isBridgeElement(target)) return null;
    const candidate =
      target.closest("main, form, [data-testid*='composer' i], [data-message-author-role], article, section, div") ??
      (target instanceof HTMLElement ? target : null);
    return candidate && !isBridgeElement(candidate) ? dropZoneContainerFromElement(candidate) : null;
  }

  function tabsAnchorCandidateFromEventTarget(target) {
    if (!(target instanceof Element)) return null;
    if (isBridgeElement(target)) return null;
    const composer = findComposer();
    const candidate =
      target.closest("form, [data-testid*='composer' i], [class*='composer' i], [class*='prompt' i], main, section, div") ??
      (target instanceof HTMLElement ? target : null);
    if (!candidate || isBridgeElement(candidate)) return null;
    if (composer && !elementContains(candidate, composer)) {
      const parent = composer.closest("form, [data-testid*='composer' i], [class*='composer' i], [class*='prompt' i]");
      return parent && !isBridgeElement(parent) ? parent : null;
    }
    return candidate;
  }

  function tabsAnchorElement() {
    const selector = storedTabsAnchorSelector();
    if (!selector) return null;
    let node = null;
    try {
      node = document.querySelector(selector);
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

  function previewTabsAnchor() {
    ensureDomRegistryStyle();
    const meta = storageMetaForTarget("tabs_anchor");
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
    addAnchorMarker(
      overlay,
      { x: rect.left, y: rect.top, width: rect.width, height: rect.height },
      meta.anchor,
      markerForTarget("tabs_anchor"),
    );
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

  function beginTabsAnchorPicker() {
    setBridgeStatus("Pick tabs anchor", "Click the visible ChatGPT composer background panel/top shell.", "working");
    setBridgeSettingsDetail("Tabs anchor picker armed. Click the composer background panel that should define the tab rail top edge.");
    const handler = (event) => {
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

  function clearTabsAnchorCalibration() {
    clearTargetMeta("tabs_anchor");
    document.getElementById(TABS_ANCHOR_PREVIEW_ID)?.remove();
    const detail = "tabs_anchor_calibration_cleared\nTabs will use automatic composer-shell detection again.";
    setBridgeSettingsDetail(detail);
    setBridgeStatus("Tabs anchor cleared", "Pick Tabs Anchor can be used to bind it again.", "idle");
    refreshBridgePosition();
  }

  function calibratedAttachControlElement(rect) {
    const selector = storedAttachSelector();
    if (!selector) return null;
    let node = null;
    try {
      node = document.querySelector(selector);
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

  function findAttachControlElement() {
    const rect = composerShellRect() ?? composerRect();
    const calibrated = calibratedAttachControlElement(rect);
    if (calibrated) return calibrated;
    if (storedAttachSelector()) return null;
    const nodes = Array.from(document.querySelectorAll("button, [role='button'], input[type='file']"));
    return nodes.find((node) => {
      if (!visibleElement(node)) return false;
      const label = controlLabel(node).toLowerCase();
      return elementWithinComposerBand(node, rect) && /attach|upload|file|plus|add/.test(label);
    }) ?? null;
  }

  function findAttachControlRect() {
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

  function localAttachPayload() {
    const targetRect = findAttachControlRect();
    const composer = composerShellRect() ?? composerRect();
    if (!targetRect || !composer) return null;
    return {
      target_kind: "attach_button",
      target_rect: targetRect,
      target_screen_rect: targetRect.screen_rect,
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

  function beginAttachTargetPicker() {
    setBridgeStatus("Pick attach target", "Click ChatGPT's real attach/add-file button. The next page click will be captured.", "working");
    setBridgeSettingsDetail("Attach target picker armed. Click the ChatGPT attach/add-file button, not the ION panel.");
    const handler = (event) => {
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

  function clearAttachTargetCalibration() {
    clearTargetMeta("attach_target");
    document.getElementById(ATTACH_PREVIEW_ID)?.remove();
    const detail = "attach_target_calibration_cleared\nPreview Target will use the guarded automatic heuristic again.";
    setBridgeSettingsDetail(detail);
    setBridgeArtifactDetail(detail);
    setBridgeStatus("Attach target cleared", "Pick Attach Target can be used to bind it again.", "idle");
  }

  function beginDropTargetPicker() {
    setBridgeStatus("Pick drop zone", "Click the ChatGPT area where a normal file drag/drop is accepted.", "working");
    setBridgeSettingsDetail("Drop-zone picker armed. Click the ChatGPT page/composer area you would normally drop a file onto.");
    const handler = (event) => {
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

  function clearDropTargetCalibration() {
    clearTargetMeta("drop_zone");
    document.getElementById(DROP_PREVIEW_ID)?.remove();
    const detail = "drop_zone_calibration_cleared\nDrop Latest will use the guarded default page/composer drop zone again.";
    setBridgeSettingsDetail(detail);
    setBridgeArtifactDetail(detail);
    setBridgeStatus("Drop zone cleared", "Pick Drop Zone can be used to bind it again.", "idle");
  }

  function previewDropTarget() {
    ensureDomRegistryStyle();
    const meta = storageMetaForTarget("drop_zone");
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
    addAnchorMarker(
      overlay,
      { x: rect.left, y: rect.top, width: rect.width, height: rect.height },
      meta.anchor,
      markerForTarget("drop_zone"),
    );
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

  function previewAttachTarget() {
    ensureDomRegistryStyle();
    const meta = storageMetaForTarget("attach_target");
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
    const overlayRect = {
      x: rect.left - 5,
      y: rect.top - 5,
      width: rect.width + 10,
      height: rect.height + 10,
    };
    const overlay = document.createElement("div");
    overlay.id = ATTACH_PREVIEW_ID;
    overlay.style.left = `${Math.round(overlayRect.x)}px`;
    overlay.style.top = `${Math.round(overlayRect.y)}px`;
    overlay.style.width = `${Math.round(overlayRect.width)}px`;
    overlay.style.height = `${Math.round(overlayRect.height)}px`;
    addAnchorMarker(
      overlay,
      overlayRect,
      meta.anchor,
      markerForTarget("attach_target"),
    );
    document.documentElement.appendChild(overlay);
    window.setTimeout(() => overlay.remove(), 4000);
    const payload = localAttachPayload();
    const detail = payload ? compactJson(payload, 1200) : "attach_target_payload_unavailable";
    setBridgeArtifactDetail(`preview_attach_target\n${detail}\nanchor: ${meta.anchor}`);
    setBridgeStatus("Attach target previewed", "Green ring marks the exact attach target. Reject Local Attach if the ring is wrong.", "success");
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

  function dispatchDropCleanupEvents(target, transfer) {
    const cleanupTargets = [
      target,
      document.body,
      document.documentElement,
      document,
      window,
    ].filter(Boolean);
    const dispatchDrag = (eventName) => {
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
        }
      });
    };
    const dispatchEscape = () => {
      [document, window].forEach((eventTarget) => {
        try {
          eventTarget.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", code: "Escape", bubbles: true, cancelable: true }));
          eventTarget.dispatchEvent(new KeyboardEvent("keyup", { key: "Escape", code: "Escape", bubbles: true, cancelable: true }));
        } catch (_error) {
        }
      });
    };
    ["dragleave", "dragend"].forEach(dispatchDrag);
    window.setTimeout(() => ["dragleave", "dragend"].forEach(dispatchDrag), 120);
    window.setTimeout(dispatchEscape, 260);
    window.setTimeout(() => document.getElementById(DROP_PREVIEW_ID)?.remove(), 500);
  }

  function dispatchFilesToDropTarget(target, files) {
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

  function requestArtifactLocalAttachDryRun() {
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
        `queue_target: ${result.queue_target ?? result.queue_path ?? result.verdict ?? ""}`,
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

  let browserPressureStarted = false;
  let latestEventLoopLagMs = 0;
  let latestLongTaskMs = 0;
  let nextLagProbeAt = 0;
  let messageQueueStarted = false;
  let messageQueuePaused = false;
  let messageQueueAllowMidOutput = false;
  let messageQueueProcessing = false;
  let messageQueueItems = [];
  let messageQueueFilePayloads = /* @__PURE__ */ new Map();
  let lastQueueChromeRect = null;
  let messageQueueDragItemId = "";
  let messageQueuePanelExpanded = false;
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
  let lastNativeActionAutoAcceptAt = 0;  let nativeActionAutoAcceptCandidate = "";
  let nativeActionAutoAcceptCandidateSince = 0;
  let leftDockProjectPanelExpanded = leftDockPanelExpandedFromStorage();
  let contextWorkflowPanelExpanded = false;
  let contextWorkflowRailStatus = "Context rail ready.";
  let contextWorkflowLastImportedPack = "No workflow pack imported.";
  const BROWSER_QUEUE_CARRIER_ID = `ion-browser-carrier-${Math.random().toString(16).slice(2)}`;
  const BROWSER_QUEUE_CLAIM_COOLDOWN_MS = 2500;
  const BROWSER_QUEUE_RESULT_TIMEOUT_MS = 10 * 60 * 1000;

  function visibleElement(element) {
    if (!(element instanceof HTMLElement)) return false;
    if (element.closest(`#${PANEL_ID}`) || element.closest(`#${MODAL_ID}`)) return false;
    const rect = element.getBoundingClientRect();
    const style = window.getComputedStyle(element);
    return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
  }
  function buttonText(button) {
    return `${button.textContent ?? ""} ${button.getAttribute("aria-label") ?? ""} ${button.getAttribute("title") ?? ""}`.replace(/\s+/g, " ").trim();
  }
  function buttonDisabled(button) {
    return button.disabled || typeof button.matches === "function" && button.matches(":disabled") || button.getAttribute("aria-disabled") === "true" || button.dataset.disabled === "true";
  }
  function nativeActionConfirmCard(button) {
    const label = buttonText(button).toLowerCase();
    if (!/^confirm\b/.test(label) || buttonDisabled(button) || !visibleElement(button)) return null;
    const candidates = [
      button.closest("[role='dialog']"),
      button.closest("article"),
      button.closest("div[class*='rounded']"),
      button.parentElement?.parentElement?.parentElement ?? null
    ].filter(Boolean);
    for (const card of candidates) {
      const text = (card.textContent ?? "").replace(/\s+/g, " ").toLowerCase();
      if (text.includes("wants to talk to ion.helixion.net") || text.includes("ion_helixion") || text.includes("ion helixion") || text.includes("ion wants to talk") || text.includes("tool call: ion")) {
        return card;
      }
    }
    return null;
  }
  function nativeActionCardKey(card, button) {
    const rect = card.getBoundingClientRect();
    return [
      Math.round(rect.left),
      Math.round(rect.top),
      Math.round(rect.width),
      Math.round(rect.height),
      buttonText(button).slice(0, 40),
      (card.textContent ?? "").replace(/\s+/g, " ").slice(0, 160)
    ].join("|");
  }
  function tryAutoAcceptNativeAction() {
    if (!browserQueueAutoAcceptActive) return;
    const now = Date.now();
    if (now - lastNativeActionAutoAcceptAt < 4500) return;
    const matches = [];
    for (const button of Array.from(document.querySelectorAll("button"))) {
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
  function findComposerInput() {
    const selectors = [
      "textarea[data-testid='composer-text-input']",
      "textarea[placeholder]",
      "#prompt-textarea",
      "[data-testid='composer'] div[contenteditable='true']",
      "[data-testid='composer'] textarea",
      "form textarea",
      "div[contenteditable='true'][data-testid='composer-text-input']",
      "form div[contenteditable='true']",
      "div[contenteditable='true']"
    ];
    const matches = [];
    for (const selector of selectors) {
      for (const node of Array.from(document.querySelectorAll(selector))) {
        if (!visibleElement(node)) continue;
        const rect = node.getBoundingClientRect();
        if (rect.bottom < window.innerHeight - 260) continue;
        matches.push(node);
      }
    }
    matches.sort((a, b) => b.getBoundingClientRect().bottom - a.getBoundingClientRect().bottom);
    return matches[0] ?? null;
  }
  function findComposerContainer(input) {
    const candidates = [
      input.closest("form"),
      input.closest("[data-testid='composer']"),
      input.closest("[role='presentation']"),
      input.parentElement
    ].filter(Boolean);
    for (const candidate of candidates) {
      const rect = candidate.getBoundingClientRect();
      if (rect.width >= 240 && rect.height >= 40 && rect.bottom >= window.innerHeight - 260) return candidate;
    }
    return input;
  }
  function findChatButton(match) {
    for (const button of Array.from(document.querySelectorAll("button"))) {
      if (!visibleElement(button)) continue;
      if (
        button.closest(`#${PANEL_ID}`) ||
        button.closest(`#${MODAL_ID}`) ||
        button.closest(`#${MESSAGE_QUEUE_PANEL_ID}`) ||
        button.closest(`#${CONTEXT_WORKFLOW_PANEL_ID}`)
      ) continue;
      if (match(buttonText(button), button)) return button;
    }
    return null;
  }
  function findSendButton() {
    const matches = [];
    for (const button of Array.from(document.querySelectorAll("button"))) {
      if (!visibleElement(button)) continue;
      if (
        button.closest(`#${PANEL_ID}`) ||
        button.closest(`#${MODAL_ID}`) ||
        button.closest(`#${MESSAGE_QUEUE_PANEL_ID}`) ||
        button.closest(`#${CONTEXT_WORKFLOW_PANEL_ID}`)
      ) continue;
      const testId = button.getAttribute("data-testid") ?? "";
      const text = buttonText(button);
      if (testId.includes("send") || /send/i.test(button.getAttribute("aria-label") ?? "") || /\bsend\b/i.test(text)) {
        matches.push(button);
      }
    }
    return matches.find((button) => !buttonDisabled(button)) ?? matches[0] ?? null;
  }
  function findStopButton() {
    return findChatButton((text, button) => {
      const testId = button.getAttribute("data-testid") ?? "";
      return testId.includes("stop") || /\bstop\b/i.test(text) || /stop\s+(generating|streaming)/i.test(text);
    });
  }
  function chatReadiness() {
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
  function queueStatus() {
    const pending = messageQueueItems.filter((item) => item.status === "queued" || item.status === "waiting" || item.status === "failed").length;
    const gatewayPending = messageQueueItems.filter((item) => item.gateway && (item.status === "queued" || item.status === "waiting" || item.status === "failed" || item.status === "sending")).length;
    if (messageQueuePaused) return `Queue paused. ${pending} message(s) waiting.`;
    if (gatewayPending) return `Gateway carrier armed. ${gatewayPending} Action packet(s) waiting. ${browserQueueGatewayStatus}`;
    if (!pending) return `Queue ready. Type in ChatGPT, press Q+ to queue, then ${messageQueueAutoPlay ? "Auto Play will send after output finishes." : "press Q▶ to send next."} ${browserQueueGatewayStatus}`;
    return messageQueueAutoPlay ? `Auto Play armed. ${pending} message(s) waiting for the next completed output.` : `Queue ready. ${pending} message(s) waiting. Press Q▶ to send the next queued message.`;
  }
  function publishMessageQueueState(status = queueStatus()) {
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
      items: messageQueueItems
    });
  }  function gatewayRequest(type, payload = {}) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ type, payload }, (response) => {
        resolve(response ?? { ok: false, stage: "no_response", finding: "browser_gateway_no_response" });
      });
    });
  }
  function nextQueuedMessage(autoOnly = false) {
    return messageQueueItems.find((candidate) => {
      const pending = candidate.status === "queued" || candidate.status === "waiting" || candidate.status === "failed";
      if (!pending) return false;
      return !autoOnly || candidate.autoRun === true || Boolean(candidate.gateway);
    });
  }
  function gatewayQueueItemPending() {
    return Boolean(nextQueuedMessage(true));
  }
  function summarizeGatewayPacket(packet) {
    const objective = String(packet?.objective ?? packet?.prompt_preview ?? packet?.packet_id ?? "ION browser queue packet").trim();
    const authority = typeof packet?.authority === "string" ? packet.authority : JSON.stringify(packet?.authority ?? "analysis_only");
    return `${objective}\n\nION_BROWSER_PACKET:\npacket_id: ${packet?.packet_id ?? ""}\nauthority: ${authority}\nstop_condition: ${packet?.stop_condition ?? "return receipt or blocker"}`;
  }
  function addGatewayQueueItem(packet, claim) {
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
        turnIndex: Number(packet?.claim?.turn_index ?? packet?.attempts ?? 1)
      }
    });
    publishMessageQueueState(`Gateway packet claimed: ${packetId}`);
    syncComposerQueueChrome();
  }
  async function pollBrowserQueueCarrier() {
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
      browserQueueApprovalPacketId = String(packets.find((packet) => packet?.state === "needs_operator")?.packet_id ?? "");
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
        chat_url: window.location.href
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
  function startBrowserQueueCarrier() {
    if (browserQueueCarrierStarted) return;
    browserQueueCarrierStarted = true;
    void pollBrowserQueueCarrier();
    window.setInterval(() => {
      void pollBrowserQueueCarrier();
    }, BROWSER_QUEUE_CLAIM_COOLDOWN_MS);
  }
  function updateQueueReadinessState() {
    const readiness = chatReadiness();
    if (readiness.activeOutput) {
      messageQueueSawActiveOutput = true;
      return;
    }
    const pendingAuto = gatewayQueueItemPending();
    const pending = Boolean(messageQueueAutoPlay ? nextQueuedMessage(false) : nextQueuedMessage(true));
    const readyAfterOutput = (messageQueueSawActiveOutput || pendingAuto) && !readiness.activeOutput && readiness.sendAvailable;
    if ((messageQueueAutoPlay || pendingAuto) && pending && readyAfterOutput && !messageQueuePaused && Date.now() - messageQueueLastAutoSentAt > 1200) {
      messageQueueSawActiveOutput = false;
      messageQueueLastAutoSentAt = Date.now();
      void processMessageQueue("auto-after-output", true, !messageQueueAutoPlay);
    }
  }
  function splitQueuedMessages(text) {
    return text.split(/\n{2,}/).map((part) => part.trim()).filter(Boolean);
  }
  function addQueuedMessageBatch(parts, status, source = "manual") {
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
        autoRun: false
      });
    }
    publishMessageQueueState(status || `${messages.length} message(s) queued. Press Q▶ to send next.`);
  }
  function addQueuedMessages(text) {
    addQueuedMessageBatch(splitQueuedMessages(text));
  }
  function compactFileSize(bytes) {
    if (!Number.isFinite(bytes) || bytes < 0) return "0 B";
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(bytes < 10 * 1024 * 1024 ? 1 : 0)} MB`;
  }
  function queueFiles(files) {
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
      attachments
    });
    messageQueuePanelExpanded = true;
    publishMessageQueueState(`${selected.length} file item${selected.length === 1 ? "" : "s"} queued for visible drop.`);
    syncComposerQueueChrome();
  }
  function openMessageQueueFilePicker() {
    const input = ensureMessageQueueFileInput();
    input.value = "";
    input.click();
  }
  function visibleQueueItems() {
    return messageQueueItems.filter((item) => item.status !== "sent");
  }
  function queueItemById(id) {
    return messageQueueItems.find((item) => item.id === id);
  }
  function queueItemIndexById(id) {
    return messageQueueItems.findIndex((item) => item.id === id);
  }
  function setQueueItemEditing(id, editing) {
    const item = queueItemById(id);
    if (!item || item.status === "sending") return;
    item.editing = editing;
    item.draftText = editing ? item.text : "";
    messageQueuePanelExpanded = true;
    publishMessageQueueState(editing ? "Queue item opened for editing." : "Queue item edit cancelled.");
    syncComposerQueueChrome();
  }
  function queueEditTextFromPanel(panel, id) {
    const editor = Array.from(panel.querySelectorAll("[data-queue-edit-id]")).find((node) => node.dataset.queueEditId === id);
    return String(editor?.value ?? "").trim();
  }
  function saveQueueItemEdit(panel, id) {
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
  function deleteQueueItem(id) {
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
  function moveQueueItem(id, direction) {
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
  function reorderQueueItem(draggedId, targetId) {
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
  function ensureMessageQueueChromeStyle() {
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
  function ensureLeftDockChromeStyle() {
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
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-visible="false"] { display: none; }
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
    #${CHATGPT_LEFT_ICON_DOCK_ID}[data-expanded="false"] .ion-left-dock-toggle-label { display: none; }
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
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-dot[data-tone="green"] { background: #34d399; box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(52,211,153,0.45); }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-dot[data-tone="yellow"] { background: #facc15; box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(250,204,21,0.45); }
    #${CHATGPT_LEFT_ICON_DOCK_ID} .ion-left-dock-dot[data-tone="red"] { background: #fb7185; box-shadow: 0 0 0 2px rgba(255,255,255,0.10), 0 0 9px rgba(251,113,133,0.45); }
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
  function leftDockTone() {
    if (messageQueueItems.some((item) => item.status === "failed") || browserQueueGatewayStatus.toLowerCase().includes("failed") || messageQueuePaused) return "red";
    if (!messageQueueItems.length || browserQueueGatewayStatus.includes("warming")) return "yellow";
    return "green";
  }
  function leftDockButton(action, icon, title, primary = false, disabled = false) {
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
  function ensureLeftDockChrome() {
    ensureLeftDockChromeStyle();
    let dock = document.getElementById(CHATGPT_LEFT_ICON_DOCK_ID);
    if (!dock) {
      dock = document.createElement("div");
      dock.id = CHATGPT_LEFT_ICON_DOCK_ID;
      dock.className = CHATGPT_LEFT_ICON_DOCK_CLASS;
      dock.dataset.visible = "true";
      dock.dataset.expanded = String(leftDockProjectPanelExpanded);
      dock.addEventListener("click", (event) => {
        const source = event.target instanceof Element ? event.target.closest("[data-left-dock-action]") : null;
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
          if (!messageQueueItems.length) publishMessageQueueState("Queue is empty.");
          else void processMessageQueue("manual");
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
          if (!nextQueuedMessage()) publishMessageQueueState("Queue is empty.");
          else void processMessageQueue("manual", true);
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
  function renderLeftDockChrome() {
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
    const toggle = leftDockButton("toggle-panel", isExpanded ? "-" : ">", isExpanded ? "Minimize left dock panel" : "Expand left dock panel");
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
      leftDockButton("queue-play-next", "⏯", "Send now (manual next)", false, !queueCount)
    );
    dock.appendChild(quick);
    if (!isExpanded) return;
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
      leftDockButton("project-pack-open", "P", "Open project package controls")
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
        const name = document.createElement("div");
        const sub = document.createElement("div");
        name.className = "ion-left-dock-project-name";
        name.textContent = pkg.project;
        sub.className = "ion-left-dock-project-subtitle";
        sub.textContent = `${pkg.version || "context package"} · ${pkg.kind}`;
        names.append(name, sub);
        const selectBtn = leftDockButton("project-select", selectedPaths.includes(pkg.path) ? "☑" : "☐", "Toggle project selection");
        selectBtn.dataset.leftDockProjectPath = pkg.path;
        row.append(names, selectBtn);
        list.appendChild(row);
      }
    }
    dock.appendChild(list);
  }
  function syncLeftDockChrome() {
    const dock = ensureLeftDockChrome();
    if (!dock) return;
    const input = findComposerInput();
    if (!input) {
      dock.dataset.visible = "false";
      return;
    }
    renderLeftDockChrome();
    const topPosition = Math.max(8, Math.round(window.innerHeight * 0.48));
    const width = leftDockProjectPanelExpanded ? Math.max(LEFT_DOCK_PANEL_WIDTH_MINI_PX + 1, Math.min(LEFT_DOCK_PANEL_WIDTH_EXPANDED_PX, Math.floor(window.innerWidth * 0.24))) : LEFT_DOCK_PANEL_WIDTH_MINI_PX;
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
  function cutComposerTextToQueue() {
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
  function ensureMessageQueueFileInput() {
    let input = document.getElementById(MESSAGE_QUEUE_FILE_INPUT_ID);
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
  function ensureComposerQueueChrome() {
    ensureMessageQueueChromeStyle();
    let button = document.getElementById(MESSAGE_QUEUE_BUTTON_ID);
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
    let sendNextButton = document.getElementById(MESSAGE_QUEUE_SEND_NEXT_BUTTON_ID);
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
        const source = event.target instanceof Element ? event.target.closest("[data-queue-float-action]") : null;
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
        saveQueueItemEdit(panel, itemId);
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
        const row = event.target instanceof Element ? event.target.closest("[data-queue-item-id]") : null;
        const id = row?.dataset.queueItemId ?? "";
        if (!id || row?.dataset.draggable !== "true") return;
        messageQueueDragItemId = id;
        row.dataset.dragging = "true";
        event.dataTransfer?.setData("text/plain", id);
        if (event.dataTransfer) event.dataTransfer.effectAllowed = "move";
      });
      panel.addEventListener("dragover", (event) => {
        const row = event.target instanceof Element ? event.target.closest("[data-queue-item-id]") : null;
        if (!messageQueueDragItemId || !row || row.dataset.queueItemId === messageQueueDragItemId) return;
        event.preventDefault();
        if (event.dataTransfer) event.dataTransfer.dropEffect = "move";
      });
      panel.addEventListener("drop", (event) => {
        const row = event.target instanceof Element ? event.target.closest("[data-queue-item-id]") : null;
        const targetId = row?.dataset.queueItemId ?? "";
        const draggedId = event.dataTransfer?.getData("text/plain") || messageQueueDragItemId;
        if (!draggedId || !targetId || draggedId === targetId) return;
        event.preventDefault();
        reorderQueueItem(draggedId, targetId);
      });
      panel.addEventListener("dragend", () => {
        messageQueueDragItemId = "";
        panel.querySelectorAll("[data-dragging]").forEach((row) => {
          delete row.dataset.dragging;
        });
      });
      document.documentElement.appendChild(panel);
    }
    return { button, sendNextButton, panel };
  }
  function queueIconButton(action, icon, title, primary = false, disabled = false) {
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
  function queueRowButton(action, itemId, icon, title, options = {}) {
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
  function queueGatewayTone() {
    if (/blocked|failed|error|killed/i.test(browserQueueGatewayStatus)) return "red";
    if (/warming|approval|cap reached|paused/i.test(browserQueueGatewayStatus)) return "yellow";
    return "green";
  }
  function queueCountBadgeLabel(total) {
    return total > 10 ? "10+" : "";
  }
  function renderComposerQueuePanel(panel) {
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
                queueRowButton("delete-item", item.id, "⌫", "Delete queue item", { danger: true, disabled: item.status === "sending" })
              );
            } else {
              actions.append(
                queueRowButton("move-up", item.id, "↑", "Move earlier", { disabled: index === 0 }),
                queueRowButton("move-down", item.id, "↓", "Move later", { disabled: index === visibleItems.length - 1 }),
                queueRowButton("edit-item", item.id, "✎", "Edit queue item", { disabled: item.status === "sending" }),
                queueRowButton("delete-item", item.id, "⌫", "Delete queue item", { danger: true, disabled: item.status === "sending" })
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
    gatewayDot.title = `Gateway automation: ${browserQueueGatewayStatus}`;
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
    const pauseButton = queueIconButton("pause-local", "Ⅱ", messageQueuePaused ? "Resume queue" : "Pause queue");
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
  function ensureContextWorkflowRailStyle() {
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
        position: absolute;
        top: 0;
        left: 0;
        width: 9px;
        height: 9px;
        border-radius: 999px;
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
  function contextWorkflowTone() {
    if (/blocked|failed|error|unavailable/i.test(contextWorkflowRailStatus)) return "red";
    if (!projectPackages.length || /scanning|requesting|importing|ready/i.test(contextWorkflowRailStatus)) return "yellow";
    return "green";
  }
  function contextWorkflowSelectedPaths() {
    const selected = selectedProjectPackagePaths.filter((path) => projectPackages.some((entry) => entry.path === path));
    if (selected.length) return selected;
    if (selectedProjectPackagePath) return [selectedProjectPackagePath];
    return projectPackages[0]?.path ? [projectPackages[0].path] : [];
  }
  function contextWorkflowLine(label, value) {
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
  function contextWorkflowAction(action, label, title, primary = false) {
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
  function contextWorkflowMiniButton(action, icon, title, primary = false) {
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
  function renderContextWorkflowRail(panel) {
    const pendingQueueItems = messageQueueItems.filter((item) => item.status !== "sent").length;
    const selectedPaths = contextWorkflowSelectedPaths();
    const selectedProject = selectedPaths.length === 1 ? projectPackages.find((entry) => entry.path === selectedPaths[0])?.project ?? "1 package" : `${selectedPaths.length} packages`;
    panel.dataset.expanded = String(contextWorkflowPanelExpanded);
    panel.innerHTML = "";
    const top = document.createElement("div");
    top.className = "ion-context-rail-top";
    const dot = document.createElement("span");
    dot.className = "ion-context-rail-dot";
    dot.dataset.contextTone = contextWorkflowTone();
    dot.title = contextWorkflowRailStatus;
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
        contextWorkflowMiniButton("projects-refresh", "P", "Refresh project context package inventory")
      );
      const miniRowTwo = document.createElement("div");
      miniRowTwo.className = "ion-context-rail-mini-row";
      miniRowTwo.append(
        contextWorkflowMiniButton("context-sync", "S", "Build selected project context sync ZIP", true),
        contextWorkflowMiniButton("import-pack", "Q+", "Import queue workflow pack", true)
      );
      miniStack.append(miniRow, miniRowTwo);
      panel.appendChild(miniStack);
    }
    if (contextWorkflowPanelExpanded) {
      const list = document.createElement("div");
      list.className = "ion-context-rail-list";
      list.append(
        contextWorkflowLine("Gateway", browserQueueGatewayStatus.replace(/\s+/g, " ")),
        contextWorkflowLine("Projects", projectPackages.length ? `${projectPackages.length} found` : "not scanned"),
        contextWorkflowLine("Selected", selectedPaths.length ? selectedProject : "none"),
        contextWorkflowLine("Workflow", pendingQueueItems ? `${pendingQueueItems} queued` : contextWorkflowLastImportedPack)
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
        contextWorkflowAction("queue-expand", "Queue", "Expand the right-side queue panel")
      );
      panel.appendChild(actions);
      const foot = document.createElement("div");
      foot.className = "ion-context-rail-foot";
      foot.textContent = contextWorkflowRailStatus;
      panel.appendChild(foot);
    }
    panel.dataset.visible = "true";
  }
  function ensureContextWorkflowRail() {
    ensureContextWorkflowRailStyle();
    let panel = document.getElementById(CONTEXT_WORKFLOW_PANEL_ID);
    if (!panel) {
      panel = document.createElement("div");
      panel.id = CONTEXT_WORKFLOW_PANEL_ID;
      panel.dataset.visible = "false";
      panel.addEventListener("click", (event) => {
        const source = event.target instanceof Element ? event.target.closest("[data-context-workflow-action]") : null;
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
          contextWorkflowRailStatus = selectedPaths.length ? `Requesting context sync ZIP for ${selectedPaths.length} project package(s).` : "Context sync blocked: select or refresh project packages first.";
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
      document.documentElement.appendChild(panel);
    }
    let input = document.getElementById(CONTEXT_WORKFLOW_IMPORT_INPUT_ID);
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
        void importQueuePackFile(file).then(() => {
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
  function contextWorkflowPanelWidth(anchorRect) {
    const available = Math.floor(anchorRect.left - 16);
    if (contextWorkflowPanelExpanded) return Math.max(76, Math.min(276, available));
    return Math.max(54, Math.min(76, available));
  }
  function composerSidePanelBottom(anchorRect) {
    return Math.max(8, Math.min(window.innerHeight - 72, window.innerHeight - anchorRect.bottom));
  }
  function syncContextWorkflowRail(anchorRect) {
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
  function pendingQueueLabel(visibleCount) {
    if (messageQueuePaused) return "paused";
    if (messageQueueAutoPlay) return "auto";
    if (visibleCount) return `${visibleCount} item${visibleCount === 1 ? "" : "s"}`;
    return browserQueueGatewayStatus === "idle" ? "idle" : browserQueueGatewayStatus;
  }
  function messageQueueRightGutter() {
    const scrollbarWidth = Math.max(0, window.innerWidth - document.documentElement.clientWidth);
    return Math.max(MESSAGE_QUEUE_RIGHT_GUTTER_PX, scrollbarWidth + 10);
  }
  function messageQueueMiniPanelWidth(anchorRect, rightGutter) {
    const available = Math.floor(window.innerWidth - rightGutter - anchorRect.right - 8);
    return Math.max(MESSAGE_QUEUE_PANEL_MINI_WIDTH_PX, Math.min(MESSAGE_QUEUE_PANEL_MINI_WIDTH_PX + 4, available));
  }
  function syncComposerQueueChrome() {
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
  function setComposerText(input, text) {
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
  function composerText(input) {
    if (input instanceof HTMLTextAreaElement || input instanceof HTMLInputElement) return input.value;
    const clone = input.cloneNode(true);
    clone.querySelectorAll("[data-placeholder], .placeholder").forEach((node) => node.remove());
    return (clone.innerText || clone.textContent || "").replace(/\u200b/g, "").trim();
  }
  function clearComposerText(input) {
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
  function sleep(ms) {
    return new Promise((resolve) => window.setTimeout(resolve, ms));
  }
  async function waitForSendReadiness(timeoutMs = 2600) {
    const started = Date.now();
    let readiness = chatReadiness();
    while ((!readiness.sendButton || !readiness.sendAvailable || readiness.activeOutput && !messageQueueAllowMidOutput) && Date.now() - started < timeoutMs) {
      await sleep(120);
      readiness = chatReadiness();
    }
    return readiness;
  }
  function latestAssistantText() {
    const selectors = [
      '[data-message-author-role="assistant"]',
      '[data-testid^="conversation-turn"] [data-message-author-role="assistant"]',
      "article"
    ];
    const candidates = [];
    for (const selector of selectors) {
      for (const node of Array.from(document.querySelectorAll(selector))) {
        if (node.closest(`#${PANEL_ID}`) || node.closest(`#${MODAL_ID}`)) continue;
        const text = (node.innerText || node.textContent || "").replace(/\s+/g, " ").trim();
        if (text.length >= 8) candidates.push(node);
      }
      if (candidates.length) break;
    }
    const last = candidates[candidates.length - 1];
    return last ? (last.innerText || last.textContent || "").replace(/\n{3,}/g, "\n\n").trim() : "";
  }
  function extractStructuredBlocks(text) {
    const blocks = [];
    const pattern = /```([A-Za-z0-9_-]+)?\n([\s\S]*?)```/g;
    let match;
    while ((match = pattern.exec(text)) && blocks.length < 8) {
      blocks.push({ language: match[1] || "text", text: match[2].trim().slice(0, 20000) });
    }
    return blocks;
  }
  async function captureGatewayQueueResult(item) {
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
      captured_at: new Date().toISOString()
    });
    item.status = "sent";
    item.detail = response?.ok ? `Gateway receipt: ${response.result?.gateway_receipt_path ?? "recorded"}` : `Gateway result blocked: ${blockedDetail(response?.result ?? response)}`;
    publishMessageQueueState(item.detail);
    syncComposerQueueChrome();
  }
  async function sendQueuedFileItem(item) {
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
  async function sendQueuedMessage(item) {
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
  async function processMessageQueue(reason = "tick", force = false, autoOnly = false) {
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
  function startMessageQueueEngine() {
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
  function percentOf(value, reference) {
    if (!Number.isFinite(value) || value <= 0) return 0;
    return Math.min(999, Math.round(value / reference * 100));
  }
  function estimateVisibleChatPressure() {
    const candidates = Array.from(document.querySelectorAll('[data-message-author-role], [data-testid^="conversation-turn"], article'));
    const seenText = new Set();
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
      const role = node.getAttribute("data-message-author-role") || node.closest("[data-message-author-role]")?.getAttribute("data-message-author-role") || "";
      if (role === "assistant") assistantMessageCount += 1;
      if (role === "user") userMessageCount += 1;
    }
    return {
      chars,
      estimatedTokens: Math.ceil(chars / 4),
      messageCount,
      assistantMessageCount,
      userMessageCount
    };
  }
  function browserPressureGuidance(percent32k, lagMs, domNodes) {
    const guidance = [];
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
  function refreshBrowserPressureMonitor() {
    const chat = estimateVisibleChatPressure();
    const domNodes = document.getElementsByTagName("*").length;
    const lagMs = Math.max(latestEventLoopLagMs, latestLongTaskMs);
    const percent32k = percentOf(chat.estimatedTokens, CHAT_CONTEXT_REFERENCE_32K);
    const percent128k = percentOf(chat.estimatedTokens, CHAT_CONTEXT_REFERENCE_128K);
    const percent256k = percentOf(chat.estimatedTokens, CHAT_CONTEXT_REFERENCE_256K);
    const percent16k = percentOf(chat.estimatedTokens, CHAT_CONTEXT_REFERENCE_16K);
    const percent400k = percentOf(chat.estimatedTokens, CHAT_CONTEXT_REFERENCE_400K);
    const blocked = percent32k >= CHAT_CONTEXT_BLOCKED_PERCENT || lagMs >= EVENT_LOOP_BLOCKED_MS || domNodes >= DOM_BLOCKED_NODES;
    const watch = blocked || percent32k >= CHAT_CONTEXT_WATCH_PERCENT || lagMs >= EVENT_LOOP_WATCH_MS || domNodes >= DOM_WATCH_NODES;
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
        ...guidance.map((item) => `- ${item}`)
      ].join("\n")
    });
  }
  function startBrowserPressureMonitor() {
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
    }
    refreshBrowserPressureMonitor();
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

  function mutationTouchesIonUi(mutation) {
    const isIonNode = (node) => {
      if (node.nodeType !== Node.ELEMENT_NODE) return false;
      const element = node;
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
    settingsAnchorTarget = "tabs_anchor";
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

  window.__ION_CHATOPS_BRIDGE_DEBUG__ = {
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
    beginAttachTargetPicker,
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
  window.addEventListener("ion-chatops-codex-refresh", () => {
    requestCodexChatModel();
  });
  window.addEventListener("ion-chatops-codex-send", (event) => {
    const detail = event.detail ?? {};
    requestCodexChatTurn(detail.message ?? "");
  });
  window.addEventListener("ion-chatops-codex-queue", (event) => {
    const detail = event.detail ?? {};
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
    browserQueueGatewayStatus = browserQueueAutoAcceptActive ? "Auto-accept on for safe ION actions; watching for ChatGPT confirmation cards." : "Auto-accept off.";
    publishMessageQueueState();
    tryAutoAcceptNativeAction();
    void gatewayRequest("ion_chatops_browser_queue_control", { operation, ttl_seconds: browserQueueAutoAcceptTtlSeconds }).then(() => pollBrowserQueueCarrier());
  });
  window.addEventListener("ion-chatops-gateway-auto-accept-settings", (event) => {
    const detail = event.detail;
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
    requestDocsOpenRoot(event);
  });
  window.addEventListener("ion-chatops-docs-open-folder", (event) => {
    const detail = event.detail ?? {};
    requestDocsOpenFolder({
      path: detail.path ?? "",
      query: detail.query,
    });
  });
  window.addEventListener("ion-chatops-docs-open-parent", () => {
    requestDocsOpenParent();
  });
  window.addEventListener("ion-chatops-docs-open-doc", (event) => {
    const detail = event.detail ?? {};
    requestDocsOpenDoc(detail.path ?? "", detail.name ?? "");
  });
  window.addEventListener("ion-chatops-docs-search", (event) => {
    const detail = event.detail ?? {};
    requestDocsSearch(detail.query ?? "");
  });
  window.addEventListener("ion-chatops-docs-drag-doc", (event) => {
    const detail = event.detail ?? {};
    requestDocsDrop(detail.path ?? "");
  });
  window.addEventListener("ion-chatops-projects-refresh", () => {
    void requestProjectsRefresh();
  });
  window.addEventListener("ion-chatops-projects-drop", (event) => {
    const detail = event.detail ?? {};
    requestProjectDrop(detail.path ?? "");
  });
  window.addEventListener("ion-chatops-project-context-sync", (event) => {
    const detail = event.detail ?? {};
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
    if (syncingSettingsModeEvent) return;
    const detail = event.detail;
    setSettingsInspectorMode(Boolean(detail?.enabled));
  });
  window.addEventListener("ion-chatops-settings-anchor-target", (event) => {
    const detail = event.detail;
    if (detail?.target !== "tabs_anchor" && detail.target !== "drop_zone" && detail.target !== "attach_target") return;
    setInspectorAnchorTarget(detail.target);
    syncSettingsControlPadState();
    setBridgeSettingsDetail([
      "dom_inspector_target_selected",
      `target: ${detail.target}`,
      `anchor: ${settingsAnchorPoint}`,
    ].join("\n"));
    if (inspectorCapturedLayers.length > 0) {
      previewInspectorSelectedLayer();
    } else if (detail.target === "tabs_anchor") {
      previewTabsAnchor();
    } else if (detail.target === "drop_zone") {
      previewDropTarget();
    } else {
      previewAttachTarget();
    }
  });
  window.addEventListener("ion-chatops-settings-anchor-point", (event) => {
    const detail = event.detail;
    const anchor = detail?.anchor;
    if (anchor === "top" || anchor === "left" || anchor === "center" || anchor === "right" || anchor === "bottom") {
      settingsAnchorPoint = anchor;
      syncSettingsControlPadState();
      setBridgeSettingsDetail([
        "dom_inspector_anchor_point_selected",
        `target: ${settingsAnchorTarget}`,
        `anchor: ${settingsAnchorPoint}`,
      ].join("\n"));
      if (inspectorCapturedLayers.length > 0) {
        previewInspectorSelectedLayer();
      } else if (settingsAnchorTarget === "tabs_anchor") {
        previewTabsAnchor();
      } else if (settingsAnchorTarget === "drop_zone") {
        previewDropTarget();
      } else {
        previewAttachTarget();
      }
    }
  });
  window.addEventListener("ion-chatops-settings-inspector-preview", () => {
    previewInspectorSelectedLayer();
  });
  window.addEventListener("ion-chatops-settings-inspector-layer", (event) => {
    const detail = event.detail;
    const index = Number(detail?.index ?? 0);
    if (document.getElementById(CAPTURE_FRAME_ID) && captureFrameLayers.length) {
      captureFrameLayerIndex = Math.max(0, Math.min(index, captureFrameLayers.length - 1));
      applyCaptureFrameLayer(captureFrameLayerIndex, true);
    }
    selectInspectorLayer(index);
  });
  window.addEventListener("ion-chatops-settings-inspector-save", (event) => {
    const detail = event.detail;
    const target = detail?.target;
    if (target === "tabs_anchor" || target === "drop_zone" || target === "attach_target") {
      saveInspectorSelectedLayer(target);
    }
  });
  window.addEventListener("ion-chatops-message-queue-add", (event) => {
    const detail = event.detail;
    if (Array.isArray(detail?.messages) && detail.messages.length) {
      addQueuedMessageBatch(detail.messages, detail.status, detail.source === "pack" ? "pack" : "manual");
      return;
    }
    const text = String(detail?.text ?? "").trim();
    if (text) addQueuedMessages(text);
  });
  window.addEventListener("ion-chatops-message-queue-pause", (event) => {
    const detail = event.detail;
    messageQueuePaused = Boolean(detail?.paused);
    publishMessageQueueState(messageQueuePaused ? "Queue paused." : "Queue resumed.");
  });
  window.addEventListener("ion-chatops-message-queue-send-next", () => {
    void processMessageQueue("manual");
  });
  window.addEventListener("ion-chatops-message-queue-clear", (event) => {
    const detail = event.detail;
    if (detail?.mode === "sent") {
      messageQueueItems = messageQueueItems.filter((item) => item.status !== "sent");
      messageQueueFilePayloads = new Map(messageQueueItems.map((item) => [item.id, messageQueueFilePayloads.get(item.id) ?? []]).filter((entry) => entry[1].length > 0));
      publishMessageQueueState("Sent messages cleared.");
      return;
    }
    messageQueueItems = [];
    messageQueueFilePayloads.clear();
    publishMessageQueueState("Queue cleared.");
  });
  window.addEventListener("ion-chatops-message-queue-mid-output", (event) => {
    const detail = event.detail;
    messageQueueAllowMidOutput = Boolean(detail?.allow);
    publishMessageQueueState(messageQueueAllowMidOutput ? "Mid-output sending allowed when ChatGPT exposes Send." : "Mid-output sending disabled. Queue waits for output to stop.");
  });
  window.addEventListener("ion-chatops-prompt-insert", (event) => {
    const detail = event.detail ?? {};
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
    initializeBridge();
  }
})();
