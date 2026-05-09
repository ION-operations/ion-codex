export type JsonValue = string | number | boolean | null | JsonValue[] | { [key: string]: JsonValue };

export interface IonActionPacket {
  ion_action: {
    schema: string;
    action_id: string;
    intent: string;
    actor: {
      callsign: string;
      carrier: string;
    };
    authority: {
      human_sovereign: string;
      requires_approval: boolean;
      production_authority: boolean;
      live_execution_authority?: boolean;
    };
    target?: Record<string, JsonValue>;
    content?: Record<string, JsonValue>;
    objective?: string;
    github?: Record<string, JsonValue>;
    artifact_refs?: JsonValue[];
    context_refs?: JsonValue[];
    receipts: {
      requested: JsonValue[];
    };
  };
}

export interface ValidationResult {
  accepted: boolean;
  findings: string[];
  action_id?: string;
  intent?: string;
  risk_class?: string;
}

export interface ParseResult {
  packet: IonActionPacket | null;
  finding: string | null;
  extracted_yaml?: string;
}

function scalar(raw: string): JsonValue {
  const value = raw.trim().replace(/\s+#.*$/, "");
  if (value === "true") return true;
  if (value === "false") return false;
  if (value === "null") return null;
  if (value === "[]") return [];
  if (/^-?\d+(\.\d+)?$/.test(value)) return Number(value);
  return value.replace(/^['"]|['"]$/g, "");
}

function setPath(root: Record<string, JsonValue>, path: string[], value: JsonValue): void {
  let cursor: Record<string, JsonValue> = root;
  for (const part of path.slice(0, -1)) {
    const existing = cursor[part];
    if (!existing || Array.isArray(existing) || typeof existing !== "object") {
      cursor[part] = {};
    }
    cursor = cursor[part] as Record<string, JsonValue>;
  }
  cursor[path[path.length - 1]] = value;
}

function appendPath(root: Record<string, JsonValue>, path: string[], value: JsonValue): void {
  let cursor: Record<string, JsonValue> = root;
  for (const part of path.slice(0, -1)) {
    const existing = cursor[part];
    if (!existing || Array.isArray(existing) || typeof existing !== "object") {
      cursor[part] = {};
    }
    cursor = cursor[part] as Record<string, JsonValue>;
  }
  const key = path[path.length - 1];
  const existing = cursor[key];
  if (!Array.isArray(existing)) {
    cursor[key] = [];
  }
  (cursor[key] as JsonValue[]).push(value);
}

function canonicalizeIonAction(root: Record<string, JsonValue>): IonActionPacket | null {
  const raw = root.ion_action;
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;
  const action = raw as Record<string, JsonValue>;
  if (!action.actor || typeof action.actor !== "object" || Array.isArray(action.actor)) {
    const callsign = action.callsign;
    const carrier = action.carrier;
    if (callsign || carrier) {
      action.actor = { callsign, carrier } as Record<string, JsonValue>;
    }
  }
  if (!action.authority || typeof action.authority !== "object" || Array.isArray(action.authority)) {
    const authority: Record<string, JsonValue> = {};
    for (const key of ["human_sovereign", "requires_approval", "production_authority", "live_execution_authority"]) {
      if (key in action) authority[key] = action[key];
    }
    if (Object.keys(authority).length) action.authority = authority;
  }
  if (!action.receipts || typeof action.receipts !== "object" || Array.isArray(action.receipts)) {
    const intent = String(action.intent ?? "");
    const defaults: Record<string, JsonValue[]> = {
      write_file_draft: ["file_write_receipt", "sha256_receipt"],
      create_codex_work_packet: ["codex_work_packet_receipt", "action_receipt"],
      create_github_issue_draft: ["github_issue_draft_receipt", "action_receipt"],
      register_artifact: ["artifact_registration_receipt", "action_receipt"],
    };
    action.receipts = { requested: defaults[intent] ?? ["action_receipt"] } as Record<string, JsonValue>;
  }
  root.ion_action = action;
  return root as unknown as IonActionPacket;
}

export function extractIonActionYaml(text: string): string | null {
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

export function parseStrictIonActionYaml(text: string): IonActionPacket | null {
  return parseIonActionYamlWithDiagnostics(text).packet;
}

export function parseIonActionYamlWithDiagnostics(text: string): ParseResult {
  const yaml = extractIonActionYaml(text);
  if (!yaml) return { packet: null, finding: "missing_top_level_ion_action", extracted_yaml: undefined };
  const lines = yaml.split("\n");
  const root: Record<string, JsonValue> = {};
  const stack: Array<{ indent: number; path: string[] }> = [];
  let literalPath: string[] | null = null;
  let literalIndent = 0;
  const literalLines: string[] = [];

  const flushLiteral = () => {
    if (literalPath) {
      setPath(root, literalPath, literalLines.join("\n").replace(/\n$/, ""));
      literalPath = null;
      literalLines.length = 0;
    }
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

    while (stack.length && indent <= stack[stack.length - 1].indent) stack.pop();
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

export function localValidate(packet: IonActionPacket): ValidationResult {
  const action = packet.ion_action;
  const findings: string[] = [];
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
  if (!action.receipts || !Array.isArray(action.receipts.requested)) findings.push("receipts_requested_list_required");
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
