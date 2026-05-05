import type { IonActionPacket, ValidationResult } from "./schema";

type BridgeTone = "idle" | "working" | "approval" | "success" | "error";

const PANEL_ID = "ion-chatops-bridge-panel";
const MODAL_ID = "ion-chatops-bridge-approval";
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

type AnchorInfo = {
  mode: "composer" | "topbar_fallback";
  rect: DOMRect | null;
  health: "ready" | "degraded";
  detail: string;
};

const bridgeState = {
  title: "Monitoring ChatGPT",
  detail: "Waiting for ion_action YAML blocks.",
  tone: "idle" as BridgeTone,
  action: "No action detected yet.",
  agent: "Codex-backed agent status has not been requested yet.",
  packages: "No context pack or ZIP export has been requested yet.",
  sandbox: "No ChatGPT sandbox returns have been requested yet.",
  automation: "Automation controls are staged only. This packet does not execute macros.",
  artifacts: "Artifact detection is staged only. No upload or local file movement occurs in this shell slice.",
  diagnostics:
    "Normal carrier flow: Sev emits an ion_action YAML block in ChatGPT, the extension detects it, Braden approves it, the local daemon records/executes it, and ION writes a receipt.\n\nThe buttons below are local diagnostics only. They fabricate known-good test actions so the extension/daemon path can be checked without waiting on ChatGPT to emit YAML.",
  tools: "Daemon: http://127.0.0.1:8767\nUse Rescan after ChatGPT finishes rendering a YAML block.",
  logs: [] as string[],
  anchor: {
    mode: "topbar_fallback",
    rect: null,
    health: "degraded",
    detail: "Composer anchor has not been evaluated yet.",
  } as AnchorInfo,
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
      max-height: min(54vh, 520px);
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

function applyTopBarLayout(panel: HTMLElement): void {
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

function candidateComposerContainer(input: HTMLElement): HTMLElement {
  type ScoredCandidate = { element: HTMLElement; score: number };
  let best: ScoredCandidate | null = null;
  let current: HTMLElement | null = input;
  let depth = 0;
  const leftBoundary = detectLeftBoundary();
  while (current?.parentElement && depth < 10) {
    current = current.parentElement;
    depth += 1;
    if (isBridgeElement(current)) break;
    const rect = visibleRect(current);
    if (!rect) continue;
    const bottomHalf = rect.top > viewportHeight() * 0.38;
    const respectsSidebar = rect.left >= Math.max(0, leftBoundary - 12);
    const plausibleWidth =
      rect.width >= Math.min(320, window.innerWidth * 0.42) &&
      rect.width <= Math.min(window.innerWidth * 0.90, window.innerWidth - leftBoundary - 16);
    const plausibleHeight = rect.height >= 36 && rect.height <= Math.max(220, viewportHeight() * 0.30);
    if (!bottomHalf || !respectsSidebar || !plausibleWidth || !plausibleHeight) continue;
    const buttons = Array.from(current.querySelectorAll("button")).filter((button) => visibleRect(button)).length;
    const radius = Number.parseFloat(window.getComputedStyle(current).borderRadius || "0") || 0;
    const score = (buttons >= 2 ? 0 : 60) + (radius >= 10 ? 0 : 16) + rect.width / 100 + rect.height / 40 + depth * 0.4;
    if (!best || score < best.score) best = { element: current, score };
  }
  return best?.element ?? input;
}

function detectComposerAnchor(): AnchorInfo {
  const input = findComposerInput();
  if (!input) {
    return {
      mode: "topbar_fallback",
      rect: null,
      health: "degraded",
      detail: "Composer anchor not found; using top-bar fallback layout.",
    };
  }
  const container = candidateComposerContainer(input);
  const rect = container.getBoundingClientRect();
  if (!rectIsVisible(rect)) {
    return {
      mode: "topbar_fallback",
      rect: null,
      health: "degraded",
      detail: "Composer candidate was not visible; using top-bar fallback layout.",
    };
  }
  return {
    mode: "composer",
    rect,
    health: "ready",
    detail: `Composer anchor ready: ${Math.round(rect.left)},${Math.round(rect.top)} ${Math.round(rect.width)}x${Math.round(rect.height)}.`,
  };
}

function applyComposerLayout(panel: HTMLElement, anchor: AnchorInfo): boolean {
  if (anchor.mode !== "composer" || !anchor.rect) return false;
  const rect = anchor.rect;
  const viewport = viewportHeight();
  const margin = 12;
  const left = Math.max(margin, Math.round(rect.left));
  const available = Math.max(PANEL_TINY_WIDTH, Math.min(Math.round(rect.width), window.innerWidth - left - margin));
  const width = Math.min(COMPOSER_PANEL_MAX_WIDTH, Math.max(PANEL_MIN_WIDTH, available));
  const bottom = Math.max(4, Math.round(viewport - rect.top - 1));
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
    cockpit.style.width = `${Math.min(width, available)}px`;
    cockpit.style.maxWidth = `${available}px`;
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
        <div class="ion-tab-panel" data-panel="artifacts"><div class="ion-detail" data-field="artifacts"></div></div>
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
  panel.querySelectorAll<HTMLElement>(".ion-tab").forEach((tab) => {
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
  const sandboxNode = panel.querySelector<HTMLElement>('[data-field="sandbox"]');
  const automationNode = panel.querySelector<HTMLElement>('[data-field="automation"]');
  const artifactsNode = panel.querySelector<HTMLElement>('[data-field="artifacts"]');
  const diagnosticsNode = panel.querySelector<HTMLElement>('[data-field="diagnostics"]');
  const toolsNode = panel.querySelector<HTMLElement>('[data-field="tools"]');
  if (statusNode) statusNode.textContent = bridgeState.detail;
  if (actionNode) actionNode.textContent = bridgeState.action;
  if (agentNode) agentNode.textContent = bridgeState.agent;
  if (packagesNode) packagesNode.textContent = bridgeState.packages;
  if (sandboxNode) sandboxNode.textContent = bridgeState.sandbox;
  if (automationNode) automationNode.textContent = bridgeState.automation;
  if (artifactsNode) artifactsNode.textContent = bridgeState.artifacts;
  if (diagnosticsNode) diagnosticsNode.textContent = `${bridgeState.anchor.detail}\n\n${bridgeState.diagnostics}`;
  if (toolsNode) toolsNode.textContent = `${bridgeState.tools}\n\nRecent:\n${bridgeState.logs.join("\n") || "No events yet."}`;
}

function positionPanelAboveComposer(panel = ensurePanel()): void {
  const anchor = detectComposerAnchor();
  bridgeState.anchor = anchor;
  applyTopRailLayout(panel);
  if (!applyComposerLayout(panel, anchor)) applyTopBarLayout(panel);
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

export function setBridgeSandboxDetail(detail: string): void {
  bridgeState.sandbox = detail;
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
