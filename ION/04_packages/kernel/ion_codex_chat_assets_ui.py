"""Static CSS and JavaScript assets for the Codex Chat cockpit shell."""
from __future__ import annotations

CODEX_CHAT_APP_CSS = """
:root {
  color-scheme: dark;
  --bg: #080a0b;
  --surface: #0d1113;
  --panel: #12181b;
  --panel-2: #172025;
  --line: #29343b;
  --text: #e7edf0;
  --muted: #96a3aa;
  --muted-2: #687780;
  --green: #5ac585;
  --amber: #d7ad52;
  --red: #e46b68;
  --blue: #69aee9;
  --code: #f2c7a7;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
html, body { min-height: 100%; }
body { margin: 0; background: var(--bg); color: var(--text); }
button, textarea { font: inherit; }
a { color: inherit; text-decoration: none; }
h1, h2, h3, p { margin: 0; letter-spacing: 0; }
.capsule-app {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 54px 280px minmax(0, 1fr) 360px 54px;
  grid-template-rows: 46px minmax(0, 1fr) 120px;
  grid-template-areas:
    "top top top top top"
    "rail leftdrawer chat inspector rrail"
    "rail leftdrawer activity inspector rrail";
  background: var(--bg);
}
.capsule-topbar {
  grid-area: top;
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  padding: 0 12px;
  border-bottom: 1px solid var(--line);
  background: var(--surface);
}
.capsule-brand { display: flex; align-items: baseline; gap: 8px; min-width: 160px; font-weight: 800; }
.capsule-brand small { color: var(--muted-2); font-size: 11px; text-transform: uppercase; }
.capsule-top-spacer { flex: 1 1 auto; }
.top-page-tabs {
  display: inline-flex;
  align-items: center;
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: 6px;
  overflow: hidden;
  background: #090d0f;
}
.top-page-tab {
  min-height: 28px;
  border: 0;
  border-right: 1px solid var(--line);
  background: transparent;
  color: var(--muted);
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
}
.top-page-tab:last-child { border-right: 0; }
.top-page-tab.is-active { color: var(--text); background: var(--panel-2); box-shadow: inset 0 -2px 0 var(--blue); }
.capsule-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  max-width: 220px;
  min-height: 25px;
  padding: 3px 8px;
  border: 1px solid var(--line);
  border-radius: 4px;
  color: var(--muted);
  font-size: 12px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.capsule-chip.ready { color: var(--green); border-color: #2c6241; }
.capsule-chip.blocked { color: var(--red); border-color: #673534; }
.capsule-chip.watch { color: var(--amber); border-color: #665229; }
.capsule-left-rail {
  grid-area: rail;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  border-right: 1px solid var(--line);
  background: #07090a;
}
.capsule-rail-button {
  display: grid;
  place-items: center;
  width: 53px;
  height: 48px;
  border: 0;
  border-bottom: 1px solid var(--line);
  background: transparent;
  color: var(--muted);
  cursor: pointer;
}
.capsule-rail-button svg { width: 18px; height: 18px; }
.capsule-rail-button.is-active,
.capsule-rail-button:hover { color: var(--text); background: var(--panel); box-shadow: inset 2px 0 0 var(--blue); }
.capsule-left-drawer {
  grid-area: leftdrawer;
  min-width: 0;
  overflow: hidden;
  border-right: 1px solid var(--line);
  background: var(--surface);
}
.left-drawer-panel {
  height: 100%;
  overflow: auto;
  padding: 10px;
}
.left-drawer-panel p {
  color: var(--muted);
  font-size: 12px;
  line-height: 1.4;
  margin-bottom: 10px;
}
.left-drawer-list {
  display: grid;
  gap: 6px;
  padding: 0;
  margin: 0;
  list-style: none;
}
.left-drawer-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  min-height: 32px;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 6px;
  background: #0a0f11;
}
.left-drawer-list span { color: var(--muted); font-size: 12px; }
.capsule-main-work-surface {
  grid-area: chat;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
  background: var(--bg);
}
.main-page {
  height: 100%;
  min-height: 0;
}
.main-page[hidden] { display: none; }
.page-surface {
  height: 100%;
  overflow: auto;
  padding: 18px min(5vw, 56px);
}
.page-surface h2 {
  margin-bottom: 6px;
  font-size: 20px;
}
.page-surface > p {
  color: var(--muted);
  margin-bottom: 14px;
  line-height: 1.45;
}
.capsule-main-chat {
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  min-width: 0;
  min-height: 0;
  height: 100%;
  background: var(--bg);
}
.capsule-message-scroll { min-height: 0; overflow: auto; padding: 18px min(5vw, 56px) 22px; }
.capsule-message-stack { display: grid; gap: 16px; max-width: 980px; margin: 0 auto; }
.capsule-empty {
  display: grid;
  place-items: center;
  min-height: 42vh;
  border: 1px dashed var(--line);
  border-radius: 8px;
  color: var(--muted);
  background: #0a0e10;
}
.turn-group { display: grid; gap: 8px; }
.bubble {
  max-width: min(820px, 100%);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 11px 12px;
  background: var(--panel);
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  line-height: 1.45;
  font-size: 14px;
}
.bubble.user { justify-self: end; width: fit-content; max-width: min(760px, 92%); background: #14212a; border-color: #294759; }
.bubble.assistant,
.bubble.execution,
.bubble.proof { justify-self: start; }
.bubble.execution { background: #12190f; border-color: #314b2c; }
.bubble.proof { background: #0e1712; border-color: #2e5a3c; }
.bubble.proof.blocked { background: #1a1111; border-color: #65403d; }
.bubble.proof.returned,
.bubble.proof.pending,
.bubble.proof.running { background: #111722; border-color: #334860; }
.bubble.pending { background: #10161b; border-color: #31546d; }
.bubble.error { background: #1a1010; border-color: #6d3434; }
.bubble.context { justify-self: center; max-width: min(760px, 92%); color: var(--muted); background: #0b1012; font-size: 12px; }
.bubble[role="button"] { cursor: pointer; }
.bubble.is-selected-memory { outline: 2px solid var(--blue); outline-offset: 2px; }
.bubble.is-connected-memory { border-color: #3d657e; }
.bubble-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 7px;
  color: var(--muted-2);
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
}
.bubble-head time { text-align: right; font-weight: 600; text-transform: none; }
.bubble pre,
.mini-text {
  max-height: 280px;
  overflow: auto;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 8px;
  color: var(--muted);
  background: #080c0e;
  white-space: pre-wrap;
  font-size: 11px;
}
.bubble pre { margin: 8px 0 0; }
.mini-text { margin: 0; }
.turn-trace-drawer { justify-self: start; width: min(820px, 100%); border: 1px solid var(--line); border-radius: 8px; background: #0a0f11; }
.turn-trace-drawer summary { min-height: 34px; padding: 8px 10px; color: var(--muted); cursor: pointer; font-size: 12px; font-weight: 800; }
.turn-trace-drawer ol { display: grid; gap: 7px; margin: 0; padding: 0 10px 10px; list-style: none; }
.trace-event { display: grid; grid-template-columns: 128px minmax(0, 1fr); gap: 4px 10px; border-top: 1px solid var(--line); padding-top: 7px; }
.trace-event b { color: var(--text); font-size: 12px; }
.trace-event span,
.trace-event p,
.trace-event code { color: var(--muted); font-size: 11px; overflow-wrap: anywhere; }
.trace-event p { grid-column: 2; margin: 0; }
.capsule-composer { border-top: 1px solid var(--line); background: var(--surface); padding: 12px min(5vw, 56px); }
.composer-inner { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 8px; max-width: 980px; margin: 0 auto; align-items: end; }
.composer-mode { grid-column: 1 / -1; display: inline-flex; width: fit-content; max-width: 100%; border: 1px solid var(--line); border-radius: 7px; overflow: hidden; background: #090d0f; }
.composer-mode label { position: relative; min-width: 82px; min-height: 30px; cursor: pointer; }
.composer-mode input { position: absolute; opacity: 0; pointer-events: none; }
.composer-mode span { display: grid; place-items: center; height: 100%; padding: 5px 10px; color: var(--muted); font-size: 12px; font-weight: 800; }
.composer-mode input:checked + span { color: var(--text); background: var(--panel-2); box-shadow: inset 0 -2px 0 var(--blue); }
.composer-inner textarea {
  width: 100%;
  min-height: 54px;
  max-height: 170px;
  resize: vertical;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #090d0f;
  color: var(--text);
  padding: 10px 11px;
  line-height: 1.4;
}
.composer-inner textarea:focus { outline: 1px solid var(--blue); border-color: var(--blue); }
.composer-inner button {
  min-width: 104px;
  min-height: 42px;
  border: 1px solid var(--line);
  border-radius: 7px;
  background: #17232a;
  color: var(--text);
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
}
.composer-inner button:hover { border-color: var(--blue); }
.composer-inner button:disabled,
.composer-inner textarea:disabled,
.composer-mode input:disabled + span { opacity: .62; cursor: wait; }
.capsule-composer.is-submitting { box-shadow: inset 0 2px 0 #31546d; }
.pending-dots::after {
  content: "";
  display: inline-block;
  width: 1.4em;
  text-align: left;
  animation: pendingDots 1.2s steps(4, end) infinite;
}
@keyframes pendingDots {
  0% { content: ""; }
  25% { content: "."; }
  50% { content: ".."; }
  75%, 100% { content: "..."; }
}
.capsule-inspector { grid-area: inspector; min-width: 0; overflow: hidden; display: grid; grid-template-rows: auto minmax(0, 1fr); border-left: 1px solid var(--line); background: var(--surface); }
.inspector-tabs {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0;
  border-bottom: 1px solid var(--line);
  background: #090d0f;
}
.inspector-tab {
  min-width: 0;
  min-height: 34px;
  border: 0;
  border-right: 1px solid var(--line);
  background: transparent;
  color: var(--muted);
  padding: 4px;
  font-size: 10px;
  font-weight: 800;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
}
.inspector-tab:last-child { border-right: 0; }
.inspector-tab.is-active { color: var(--text); background: var(--panel-2); box-shadow: inset 0 -2px 0 var(--blue); }
.inspector-panel {
  min-height: 0;
  overflow: auto;
  padding: 10px;
}
.inspector-panel[hidden] { display: none; }
.inspector-card { margin-bottom: 10px; border: 1px solid var(--line); border-radius: 7px; background: var(--panel); }
.inspector-card > summary { list-style: none; cursor: pointer; padding: 10px; }
.inspector-card > summary::-webkit-details-marker { display: none; }
.inspector-card > summary::after { content: "+"; color: var(--muted-2); font-size: 13px; }
.inspector-card[open] > summary::after { content: "-"; }
.inspector-card > p,
.inspector-card > ul,
.inspector-card > h3,
.inspector-card > pre { margin-left: 10px; margin-right: 10px; }
.inspector-card > :last-child { margin-bottom: 10px; }
.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
  color: var(--muted-2);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1px;
  text-transform: uppercase;
}
.inspector-card > summary.section-title { margin-bottom: 0; }
.inspector-card p,
.inspector-card li { color: var(--muted); font-size: 12px; line-height: 1.4; }
.inspector-card code { color: var(--code); overflow-wrap: anywhere; }
.inspector-card ul { margin: 6px 0 0; padding-left: 18px; }
.drawer-kpis {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 6px;
  margin: 8px 10px 10px;
}
.drawer-kpi {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 7px;
  background: #0a0f11;
}
.drawer-kpi span {
  display: block;
  color: var(--muted-2);
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
}
.drawer-kpi b {
  display: block;
  margin-top: 4px;
  color: var(--text);
  font-size: 13px;
  overflow-wrap: anywhere;
}
.state-pill {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  max-width: 100%;
  min-height: 20px;
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 2px 6px;
  color: var(--muted);
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  overflow-wrap: anywhere;
}
.state-pill.ready { color: var(--green); border-color: #2c6241; }
.state-pill.blocked { color: var(--red); border-color: #673534; }
.state-pill.watch { color: var(--amber); border-color: #665229; }
.count-list,
.agent-list {
  display: grid;
  gap: 6px;
  padding-left: 0 !important;
  list-style: none;
}
.count-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  border: 1px solid var(--line);
  border-radius: 5px;
  padding: 6px;
  background: #0a0f11;
}
.memory-visualization-surface {
  display: grid;
  gap: 10px;
}
.memory-budget-strip {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 6px;
  margin: 8px 10px 10px;
}
.memory-budget-panel .memory-budget-strip { margin: 0; }
.memory-panel {
  margin: 8px 10px 0;
  border: 1px solid var(--line);
  border-radius: 7px;
  padding: 8px;
  background: #0a0f11;
}
.memory-selection-panel {
  border-color: #31546d;
  background: #0a1117;
}
.memory-panel-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
}
.memory-panel-title h3,
.memory-panel h4 {
  margin: 0;
  color: var(--text);
  font-size: 12px;
}
.memory-panel-title span,
.memory-panel-title code,
.memory-policy-note {
  color: var(--muted);
  font-size: 11px;
}
.memory-window-grid,
.matryoshka-grid,
.memory-lane-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}
.memory-lane-grid.compact {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}
.memory-lane-grid h4 {
  margin-bottom: 6px;
  color: var(--muted);
}
.memory-window,
.matryoshka-layer,
.memory-segment-card {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 7px;
  background: #081012;
}
.memory-window {
  display: grid;
  align-content: start;
  gap: 6px;
}
.memory-window-head,
.memory-segment-head,
.memory-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.memory-window-head b,
.memory-segment-head b {
  color: var(--text);
  font-size: 12px;
  overflow-wrap: anywhere;
}
.memory-window-head span,
.memory-meta-row span,
.memory-ref-line {
  color: var(--muted);
  font-size: 10px;
}
.memory-segment-card {
  display: grid;
  gap: 6px;
}
.memory-segment-card p,
.matryoshka-layer p {
  margin: 0;
  color: var(--muted);
  font-size: 11px;
  line-height: 1.35;
  overflow-wrap: anywhere;
}
.memory-tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.memory-tag {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 2px 5px;
  color: var(--blue);
  font-size: 9px;
  font-weight: 800;
  overflow-wrap: anywhere;
}
.memory-tag.tone { color: var(--muted); }
.memory-tag.muted { color: var(--muted-2); }
.memory-live_input { border-color: #5f95bd; background: #0e1820; }
.memory-active_crucible { border-color: #3d657e; background: #0b1419; }
.memory-active_context { border-color: #3c684d; background: #0b1510; }
.memory-hot_context { border-color: #6b5930; background: #15130b; }
.memory-x_ray_dag { border-color: #3b4850; background: #0a0d0f; }
.memory-mini_lookup { border-color: #385369; background: #0a1117; }
.memory-long_horizon { border-color: #343b43; background: #080b0d; }
.memory-cold_evidence { border-color: #30383d; background: #070a0b; }
.memory-omitted_or_blocked { border-color: #633838; background: #130a0a; opacity: .82; }
.route-edge-list,
.compaction-list,
.source-ref-list,
.omitted-ref-list {
  display: grid;
  gap: 6px;
  margin: 6px 0 0;
  padding-left: 0 !important;
  list-style: none;
}
.source-ref-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.source-ref-lane {
  display: grid;
  gap: 6px;
  border-top: 1px solid var(--line);
  padding-top: 7px;
}
.source-ref-lane + .source-ref-lane { margin-top: 7px; }
.source-ref-button {
  min-width: 0;
  max-width: 100%;
  min-height: 25px;
  border: 1px solid var(--line);
  border-radius: 5px;
  background: #081012;
  color: var(--muted);
  padding: 3px 7px;
  cursor: pointer;
  text-align: left;
}
.source-ref-button code {
  display: block;
  max-width: 220px;
  overflow: hidden;
  color: var(--code);
  font-size: 10px;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.source-ref-button:hover,
.source-ref-button.is-selected-memory {
  border-color: var(--blue);
  color: var(--text);
}
.route-edge-filter-row {
  display: flex;
  gap: 6px;
  min-width: 0;
  overflow-x: auto;
  padding-bottom: 6px;
}
.source-group-filter-row {
  display: flex;
  gap: 6px;
  min-width: 0;
  overflow-x: auto;
  padding-bottom: 7px;
}
.route-edge-filter,
.source-group-filter {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  min-height: 25px;
  border: 1px solid var(--line);
  border-radius: 5px;
  background: #090d0f;
  color: var(--muted);
  padding: 3px 8px;
  font-size: 10px;
  font-weight: 800;
  cursor: pointer;
  white-space: nowrap;
}
.route-edge-filter.is-active,
.source-group-filter.is-active {
  color: var(--text);
  border-color: var(--blue);
}
.route-summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 6px;
  margin-bottom: 8px;
}
.route-summary-card {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: 5px;
  padding: 6px;
  background: #081012;
}
.route-summary-card span {
  display: block;
  color: var(--muted-2);
  font-size: 9px;
  font-weight: 800;
  text-transform: uppercase;
  overflow-wrap: anywhere;
}
.route-summary-card b {
  color: var(--text);
  font-size: 15px;
}
.route-edge-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) auto minmax(0, 1fr);
  gap: 4px 7px;
  align-items: center;
  border-top: 1px solid var(--line);
  padding-top: 6px;
}
.route-edge-row div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  grid-column: 1 / -1;
}
.route-edge-row b,
.compaction-event b,
.trace-link-row b {
  color: var(--text);
  font-size: 12px;
}
.route-edge-row span,
.route-edge-row p,
.compaction-event p,
.compaction-event span,
.trace-link-row p,
.source-ref-list li,
.omitted-ref-list li {
  color: var(--muted);
  font-size: 11px;
  overflow-wrap: anywhere;
}
.route-edge-row p {
  grid-column: 1 / -1;
  margin: 0;
}
.route-arrow {
  color: var(--blue) !important;
  font-weight: 800;
}
.compaction-event {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 4px 8px;
  border-top: 1px solid var(--line);
  padding-top: 6px;
}
.compaction-event p,
.compaction-event code,
.compaction-event span {
  grid-column: 1 / -1;
}
.memory-manifest-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px;
}
.memory-selection-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 6px;
}
.memory-selection-grid p {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: 5px;
  padding: 6px;
  background: #081012;
}
.memory-selection-grid span {
  display: block;
  margin-bottom: 4px;
  color: var(--muted-2);
  font-size: 9px;
  font-weight: 800;
  text-transform: uppercase;
}
.memory-selection-preview {
  margin-top: 8px !important;
  border: 1px solid var(--line);
  border-radius: 5px;
  padding: 8px;
  color: var(--muted);
  background: #070b0d;
}
.memory-manifest-grid p {
  border: 1px solid var(--line);
  border-radius: 5px;
  padding: 6px;
  background: #081012;
}
.memory-segment-card[role="button"],
.route-edge-row[role="button"],
.trace-link-row[role="button"] {
  cursor: pointer;
}
.memory-segment-card.is-selected-memory,
.route-edge-row.is-selected-memory,
.trace-link-row.is-selected-memory {
  outline: 2px solid var(--blue);
  outline-offset: 2px;
  border-color: var(--blue);
}
.memory-segment-card.is-connected-memory,
.route-edge-row.is-connected-memory,
.trace-link-row.is-connected-memory,
.source-ref-button.is-connected-memory {
  border-color: #3d657e;
  background: #0c1519;
}
.memory-segment-card:focus-visible,
.route-edge-row:focus-visible,
.trace-link-row:focus-visible,
.source-ref-button:focus-visible,
.bubble[role="button"]:focus-visible {
  outline: 2px solid var(--blue);
  outline-offset: 2px;
}
.trace-card,
.invocation-card,
.skill-card {
  margin: 8px 10px 0;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 8px;
  background: #0a0f11;
}
.trace-card-head,
.invocation-card div,
.skill-card div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.trace-card-head b,
.invocation-card b,
.skill-card b,
.agent-row b {
  color: var(--text);
  font-size: 12px;
  overflow-wrap: anywhere;
}
.skill-list {
  display: grid;
  gap: 8px;
}
.event-flow {
  display: grid;
  gap: 6px;
  margin: 8px 0 0;
  padding-left: 0;
  list-style: none;
}
.event-flow li {
  display: grid;
  grid-template-columns: minmax(80px, 1fr) auto;
  gap: 4px 8px;
  border-top: 1px solid var(--line);
  padding-top: 6px;
}
.event-flow code,
.event-flow p {
  grid-column: 1 / -1;
  margin: 0;
}
.agent-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 4px 8px;
  border: 1px solid var(--line);
  border-radius: 5px;
  padding: 6px;
  background: #0a0f11;
}
.agent-row code,
.agent-row span {
  overflow-wrap: anywhere;
}
.invocation-list {
  display: grid;
  gap: 8px;
}
.invocation-card code,
.invocation-card p {
  display: block;
  margin-top: 6px;
  overflow-wrap: anywhere;
}
.empty-note {
  margin: 8px 10px 0;
  border: 1px dashed var(--line);
  border-radius: 6px;
  padding: 8px;
  color: var(--muted);
}
.capsule-right-rail {
  grid-area: rrail;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  border-left: 1px solid var(--line);
  background: #07090a;
}
.right-rail-button {
  display: grid;
  place-items: center;
  width: 53px;
  height: 48px;
  border: 0;
  border-bottom: 1px solid var(--line);
  background: transparent;
  color: var(--muted);
  cursor: pointer;
}
.right-rail-button svg { width: 18px; height: 18px; }
.right-rail-button.is-active,
.right-rail-button:hover { color: var(--text); background: var(--panel); box-shadow: inset -2px 0 0 var(--blue); }
.capsule-activity-strip { grid-area: activity; min-width: 0; overflow: hidden; display: grid; grid-template-rows: auto minmax(0, 1fr); padding: 8px 12px; border-top: 1px solid var(--line); background: var(--surface); }
.timeline-filter-row {
  display: flex;
  gap: 6px;
  min-width: 0;
  overflow-x: auto;
  padding-bottom: 7px;
}
.timeline-filter {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  min-height: 25px;
  border: 1px solid var(--line);
  border-radius: 5px;
  background: #090d0f;
  color: var(--muted);
  padding: 3px 8px;
  font-size: 11px;
  font-weight: 800;
  cursor: pointer;
}
.timeline-filter.is-active { color: var(--text); border-color: var(--blue); }
.activity-row { display: flex; gap: 8px; min-width: max-content; }
.activity-item { width: 260px; border: 1px solid var(--line); border-radius: 7px; padding: 8px; background: var(--panel); }
.activity-item b { display: block; color: var(--text); font-size: 12px; overflow-wrap: anywhere; }
.activity-item span,
.activity-item p { color: var(--muted); font-size: 11px; overflow-wrap: anywhere; }
@media (max-width: 1180px) {
  .capsule-app {
    grid-template-columns: 54px minmax(0, 1fr) 54px;
    grid-template-areas:
      "top top top"
      "rail chat rrail"
      "rail leftdrawer rrail"
      "rail inspector rrail"
      "rail activity rrail";
    grid-template-rows: 46px minmax(0, 1fr) auto auto 110px;
  }
  .capsule-left-drawer { border-right: 0; border-top: 1px solid var(--line); max-height: 220px; }
  .capsule-inspector { border-left: 0; border-top: 1px solid var(--line); }
  .inspector-card { margin-bottom: 0; }
  .memory-budget-strip { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .memory-lane-grid.compact { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .memory-selection-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 720px) {
  .capsule-app {
    grid-template-columns: 1fr;
    grid-template-areas:
      "top"
      "rail"
      "leftdrawer"
      "chat"
      "inspector"
      "rrail"
      "activity";
  }
  .capsule-topbar { align-items: stretch; flex-wrap: wrap; height: auto; padding: 8px; }
  .capsule-left-rail { flex-direction: row; overflow-x: auto; border-right: 0; border-bottom: 1px solid var(--line); }
  .capsule-rail-button { min-width: 46px; width: 46px; height: 42px; border-right: 1px solid var(--line); border-bottom: 0; }
  .capsule-left-drawer { max-height: 190px; border-bottom: 1px solid var(--line); }
  .capsule-right-rail { flex-direction: row; overflow-x: auto; border-left: 0; border-top: 1px solid var(--line); }
  .right-rail-button { min-width: 46px; width: 46px; height: 42px; border-right: 1px solid var(--line); border-bottom: 0; }
  .capsule-message-scroll,
  .capsule-composer { padding-left: 10px; padding-right: 10px; }
  .composer-inner { grid-template-columns: 1fr; }
  .composer-inner button { width: 100%; }
  .top-page-tabs { order: 4; width: 100%; overflow-x: auto; }
  .memory-budget-strip,
  .memory-window-grid,
  .matryoshka-grid,
  .memory-lane-grid,
  .memory-lane-grid.compact,
  .memory-selection-grid,
  .route-summary-grid,
  .memory-manifest-grid { grid-template-columns: 1fr; }
  .route-edge-row { grid-template-columns: 1fr; }
  .route-arrow { display: none; }
}
"""


CODEX_CHAT_APP_JS = r"""
(function () {
  const form = document.querySelector(".capsule-composer");
  if (!form || !window.fetch || !window.URLSearchParams) return;

  const textarea = form.querySelector('textarea[name="message"]');
  const submitButton = form.querySelector('button[type="submit"]');
  const stack = document.querySelector(".capsule-message-stack");
  const scroll = document.querySelector(".capsule-message-scroll");
  if (!textarea || !submitButton || !stack) return;
  const SELECTION_STORAGE_KEY = "ion.codexChat.selectedInspection";

  function activateByDataset(buttonSelector, panelSelector, buttonAttrName, panelAttrName, targetValue) {
    document.querySelectorAll(buttonSelector).forEach((button) => {
      button.classList.toggle("is-active", button.dataset[buttonAttrName] === targetValue);
    });
    document.querySelectorAll(panelSelector).forEach((panel) => {
      const active = panel.dataset[panelAttrName] === targetValue;
      panel.classList.toggle("is-active", active);
      panel.hidden = !active;
    });
  }

  document.querySelectorAll("[data-page-target]").forEach((button) => {
    button.addEventListener("click", () => {
      activateByDataset("[data-page-target]", "[data-page-panel]", "pageTarget", "pagePanel", button.dataset.pageTarget);
    });
  });

  document.querySelectorAll("[data-left-drawer-target]").forEach((button) => {
    button.addEventListener("click", () => {
      activateByDataset("[data-left-drawer-target]", "[data-left-panel]", "leftDrawerTarget", "leftPanel", button.dataset.leftDrawerTarget);
    });
  });

  document.querySelectorAll("[data-inspector-target]").forEach((button) => {
    button.addEventListener("click", () => {
      activateByDataset("[data-inspector-target]", "[data-inspector-panel]", "inspectorTarget", "inspectorPanel", button.dataset.inspectorTarget);
    });
  });

  document.querySelectorAll("[data-timeline-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.timelineFilter || "all";
      document.querySelectorAll("[data-timeline-filter]").forEach((candidate) => {
        candidate.classList.toggle("is-active", candidate.dataset.timelineFilter === filter);
      });
      document.querySelectorAll("[data-timeline-kind]").forEach((item) => {
        item.hidden = filter !== "all" && item.dataset.timelineKind !== filter;
      });
    });
  });

  function setSelectionField(name, value) {
    document.querySelectorAll('[data-memory-selection-field="' + name + '"]').forEach((node) => {
      node.textContent = value || "none";
    });
  }

  function memoryCardFor(segmentId) {
    if (!segmentId) return null;
    return document.querySelector('[data-memory-segment-id="' + CSS.escape(segmentId) + '"]');
  }

  function persistMemorySelection(selection) {
    if (!selection || !selection.type || !selection.id) return;
    try {
      window.localStorage.setItem(SELECTION_STORAGE_KEY, JSON.stringify(selection));
    } catch (_) {}
    try {
      if (window.history && window.location) {
        const encoded = encodeURIComponent(selection.type + ":" + selection.id);
        window.history.replaceState(null, "", "#inspect=" + encoded);
      }
    } catch (_) {}
  }

  function storedMemorySelection() {
    try {
      const hash = window.location.hash || "";
      if (hash.indexOf("#inspect=") === 0) {
        const raw = decodeURIComponent(hash.slice("#inspect=".length));
        const split = raw.indexOf(":");
        if (split > 0) {
          return {type: raw.slice(0, split), id: raw.slice(split + 1)};
        }
      }
    } catch (_) {}
    try {
      const raw = window.localStorage.getItem(SELECTION_STORAGE_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (parsed && parsed.type && parsed.id) return parsed;
    } catch (_) {}
    return null;
  }

  function clearMemorySelection() {
    document.querySelectorAll(".is-selected-memory, .is-connected-memory").forEach((node) => {
      node.classList.remove("is-selected-memory", "is-connected-memory");
    });
  }

  function selectMemorySegment(segmentId, options) {
    const opts = options || {};
    const card = memoryCardFor(segmentId);
    clearMemorySelection();
    if (!segmentId) return;

    document.querySelectorAll('[data-memory-segment-id="' + CSS.escape(segmentId) + '"]').forEach((node) => {
      node.classList.add("is-selected-memory");
    });
    document.querySelectorAll("[data-route-edge-id]").forEach((edge) => {
      if (edge.dataset.routeFrom === segmentId || edge.dataset.routeTo === segmentId) {
        edge.classList.add("is-connected-memory");
        const otherId = edge.dataset.routeFrom === segmentId ? edge.dataset.routeTo : edge.dataset.routeFrom;
        document.querySelectorAll('[data-memory-segment-id="' + CSS.escape(otherId || "") + '"]').forEach((node) => {
          node.classList.add("is-connected-memory");
        });
      }
    });

    setSelectionField("id", segmentId);
    setSelectionField("turn", card ? card.dataset.memoryTurnId : (opts.turnId || "none"));
    setSelectionField("window", card ? card.dataset.memoryWindow : "chat_turn");
    setSelectionField("kind", card ? card.dataset.memoryKind : (opts.kind || "chat_turn"));
    setSelectionField("prompt", card ? card.dataset.memoryPromptState : (opts.prompt || "selected_chat_turn"));
    setSelectionField("lifecycle", card ? card.dataset.memoryLifecycle : "visible_turn");
    setSelectionField("compaction", card ? card.dataset.memoryCompaction : "raw_turn");
    setSelectionField("tokens", card ? card.dataset.memoryTokenEstimate : "unknown");
    setSelectionField("confidence", card ? card.dataset.memoryConfidence : "visible");
    setSelectionField("preview", card ? card.dataset.memoryPreview : (opts.preview || "Selected chat turn is visible in the conversation timeline."));
    setSelectionField("refs", card ? card.dataset.memoryRefs : "");
    setSelectionField("edge", opts.edgeId || "none");
    if (!opts.skipPersist) {
      persistMemorySelection({type: "memory", id: segmentId});
    }
  }

  function selectRouteEdge(edge, options) {
    if (!edge) return;
    const opts = options || {};
    const targetId = edge.dataset.routeTo || edge.dataset.routeFrom || "";
    selectMemorySegment(targetId, {
      edgeId: edge.dataset.routeEdgeId || "none",
      kind: edge.dataset.routeType || "route_edge",
      skipPersist: true
    });
    edge.classList.add("is-selected-memory");
    const sourceId = edge.dataset.routeFrom || "";
    document.querySelectorAll('[data-memory-segment-id="' + CSS.escape(sourceId) + '"]').forEach((node) => {
      node.classList.add("is-connected-memory");
    });
    setSelectionField("edge", edge.dataset.routeEdgeId || "none");
    if (!opts.skipPersist) {
      persistMemorySelection({type: "route", id: edge.dataset.routeEdgeId || "none"});
    }
  }

  function highlightSourceRef(sourceRef) {
    if (!sourceRef) return;
    document.querySelectorAll('[data-source-ref="' + CSS.escape(sourceRef) + '"]').forEach((node) => {
      node.classList.add("is-selected-memory");
    });
    document.querySelectorAll("[data-memory-refs]").forEach((node) => {
      if ((node.dataset.memoryRefs || "").includes(sourceRef)) {
        node.classList.add("is-connected-memory");
      }
    });
    document.querySelectorAll("[data-trace-refs]").forEach((node) => {
      if ((node.dataset.traceRefs || "").includes(sourceRef)) {
        node.classList.add("is-connected-memory");
      }
    });
  }

  function selectSourceRef(node, options) {
    if (!node) return;
    const opts = options || {};
    const sourceRef = node.dataset.sourceRef || "";
    clearMemorySelection();
    highlightSourceRef(sourceRef);
    setSelectionField("id", sourceRef || "source_ref");
    setSelectionField("turn", "none");
    setSelectionField("window", "source_ref");
    setSelectionField("kind", node.dataset.sourceKind || "source_ref");
    setSelectionField("prompt", "route_or_evidence_ref");
    setSelectionField("lifecycle", "visible_evidence");
    setSelectionField("compaction", "not_applicable");
    setSelectionField("tokens", "unknown");
    setSelectionField("confidence", "visible");
    setSelectionField("preview", node.dataset.sourcePreview || sourceRef || "Selected source reference.");
    setSelectionField("refs", sourceRef);
    setSelectionField("edge", "none");
    if (!opts.skipPersist) {
      persistMemorySelection({type: "source", id: sourceRef || "source_ref"});
    }
  }

  function selectTraceEvent(node, options) {
    if (!node) return;
    const opts = options || {};
    const refs = node.dataset.traceRefs || "";
    clearMemorySelection();
    node.classList.add("is-selected-memory");
    refs.split(",").map((item) => item.trim()).filter(Boolean).forEach((sourceRef) => {
      highlightSourceRef(sourceRef);
    });
    const turnId = node.dataset.traceTurnId || "none";
    if (turnId && turnId !== "none") {
      document.querySelectorAll('[data-memory-segment-id="' + CSS.escape("turn:" + turnId) + '"]').forEach((card) => {
        card.classList.add("is-connected-memory");
      });
      document.querySelectorAll('[data-chat-turn-id="' + CSS.escape(turnId) + '"]').forEach((turn) => {
        turn.classList.add("is-connected-memory");
      });
    }
    setSelectionField("id", node.dataset.traceEventId || "trace_event");
    setSelectionField("turn", turnId);
    setSelectionField("window", "trace_event");
    setSelectionField("kind", node.dataset.traceType || "trace_event");
    setSelectionField("prompt", "visible_runtime_trace");
    setSelectionField("lifecycle", node.dataset.tracePhase || "trace");
    setSelectionField("compaction", "runtime_event");
    setSelectionField("tokens", "n/a");
    setSelectionField("confidence", node.dataset.traceStatus || "visible");
    setSelectionField("preview", node.dataset.traceLabel || node.textContent || "Selected trace event.");
    setSelectionField("refs", refs);
    setSelectionField("edge", "none");
    if (!opts.skipPersist) {
      persistMemorySelection({type: "trace", id: node.dataset.traceEventId || "trace_event"});
    }
  }

  function restoreMemorySelection() {
    const selection = storedMemorySelection();
    if (!selection || !selection.type || !selection.id) return false;
    if (selection.type === "memory") {
      const card = memoryCardFor(selection.id);
      if (card) {
        selectMemorySegment(selection.id, {skipPersist: true});
        return true;
      }
    }
    if (selection.type === "route") {
      const edge = document.querySelector('[data-route-edge-id="' + CSS.escape(selection.id) + '"]');
      if (edge) {
        selectRouteEdge(edge, {skipPersist: true});
        return true;
      }
    }
    if (selection.type === "source") {
      const source = document.querySelector('[data-source-ref="' + CSS.escape(selection.id) + '"]');
      if (source) {
        selectSourceRef(source, {skipPersist: true});
        return true;
      }
    }
    if (selection.type === "trace") {
      const eventNode = document.querySelector('[data-trace-event-id="' + CSS.escape(selection.id) + '"]');
      if (eventNode) {
        selectTraceEvent(eventNode, {skipPersist: true});
        return true;
      }
    }
    return false;
  }

  function activateSelectable(node, callback) {
    node.addEventListener("click", () => callback(node));
    node.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        callback(node);
      }
    });
  }

  document.querySelectorAll(".memory-segment-card[data-memory-segment-id]").forEach((card) => {
    activateSelectable(card, (node) => selectMemorySegment(node.dataset.memorySegmentId || ""));
  });
  document.querySelectorAll(".route-edge-row[data-route-edge-id]").forEach((edge) => {
    activateSelectable(edge, selectRouteEdge);
  });
  document.querySelectorAll("[data-route-edge-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.routeEdgeFilter || "all";
      document.querySelectorAll("[data-route-edge-filter]").forEach((candidate) => {
        candidate.classList.toggle("is-active", candidate.dataset.routeEdgeFilter === filter);
      });
      document.querySelectorAll("[data-route-edge-type]").forEach((edge) => {
        edge.hidden = filter !== "all" && edge.dataset.routeEdgeType !== filter;
      });
    });
  });
  document.querySelectorAll("[data-source-group-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.sourceGroupFilter || "all";
      const scope = button.closest(".source-ref-drilldown") || document;
      scope.querySelectorAll("[data-source-group-filter]").forEach((candidate) => {
        candidate.classList.toggle("is-active", candidate.dataset.sourceGroupFilter === filter);
      });
      scope.querySelectorAll("[data-source-ref-lane]").forEach((lane) => {
        lane.hidden = filter !== "all" && lane.dataset.sourceRefLane !== filter;
      });
    });
  });
  document.querySelectorAll("[data-source-ref]").forEach((button) => {
    activateSelectable(button, selectSourceRef);
  });
  document.querySelectorAll("[data-trace-event-id]").forEach((eventNode) => {
    activateSelectable(eventNode, selectTraceEvent);
  });
  document.querySelectorAll(".bubble[data-chat-turn-id]").forEach((bubbleNode) => {
    activateSelectable(bubbleNode, (node) => {
      selectMemorySegment(node.dataset.memorySegmentId || "", {
        kind: "chat_turn",
        turnId: node.dataset.chatTurnId || "none",
        preview: node.textContent || "Selected chat turn."
      });
    });
  });
  const initialCard = document.querySelector(".memory-segment-card[data-memory-segment-id]");
  if (initialCard && !document.querySelector(".is-selected-memory")) {
    if (!restoreMemorySelection()) {
      selectMemorySegment(initialCard.dataset.memorySegmentId || "", {skipPersist: true});
    }
  }

  function nowText() {
    return new Date().toISOString().replace(/\.\d{3}Z$/, "+00:00");
  }

  function setSubmitting(isSubmitting) {
    form.dataset.submitting = isSubmitting ? "true" : "false";
    form.classList.toggle("is-submitting", isSubmitting);
    submitButton.disabled = isSubmitting;
    submitButton.textContent = isSubmitting ? (submitButton.dataset.busyLabel || "Sending...") : (submitButton.dataset.readyLabel || "Send");
    textarea.disabled = isSubmitting;
    form.querySelectorAll('input[name="execution_mode"]').forEach((input) => { input.disabled = isSubmitting; });
  }

  function bubble(cssClass, label, message) {
    const article = document.createElement("article");
    article.className = "bubble " + cssClass;
    const head = document.createElement("div");
    head.className = "bubble-head";
    const span = document.createElement("span");
    span.textContent = label;
    const time = document.createElement("time");
    time.textContent = nowText();
    const body = document.createElement("div");
    body.textContent = message;
    head.append(span, time);
    article.append(head, body);
    return article;
  }

  function appendPendingTurn(message) {
    const section = document.createElement("section");
    section.className = "turn-group pending-turn";
    section.appendChild(bubble("user", "You", message));
    const pending = bubble("assistant pending", "Codex", "Codex is working on this response. The carrier can take a few seconds");
    const pendingBody = pending.querySelector("div:last-child");
    if (pendingBody) pendingBody.className = "pending-dots";
    section.appendChild(pending);
    stack.appendChild(section);
    if (scroll) scroll.scrollTop = scroll.scrollHeight;
    return pending;
  }

  function setBubbleMessage(article, cssClass, message) {
    article.className = "bubble " + cssClass;
    const body = article.querySelector("div:last-child");
    if (body) {
      body.className = "";
      body.textContent = message || "No response text returned.";
    }
    if (scroll) scroll.scrollTop = scroll.scrollHeight;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    if (form.dataset.submitting === "true") return;

    const message = textarea.value.trim();
    if (!message) {
      textarea.focus();
      return;
    }

    const pendingBubble = appendPendingTurn(message);
    const params = new URLSearchParams(new FormData(form));
    params.set("message", message);
    params.set("author", "operator");
    textarea.value = "";
    setSubmitting(true);

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: params
      });
      const payload = await response.json();
      if (!response.ok || !payload.ok) {
        const finding = payload.finding || payload.error || "request_failed";
        setBubbleMessage(pendingBubble, "assistant error", "Codex request failed: " + finding);
      } else {
        const assistant = payload.assistant_turn || {};
        setBubbleMessage(pendingBubble, "assistant", assistant.message || "Codex response captured.");
        if (payload.execution_status_turn && payload.execution_status_turn.message) {
          const group = pendingBubble.closest(".turn-group") || stack;
          group.appendChild(bubble("execution", "Execution", payload.execution_status_turn.message));
          if (scroll) scroll.scrollTop = scroll.scrollHeight;
        }
      }
    } catch (error) {
      setBubbleMessage(pendingBubble, "assistant error", "Codex request failed: " + (error && error.name ? error.name : "network_error"));
    } finally {
      setSubmitting(false);
      textarea.focus();
    }
  });
})();
"""
