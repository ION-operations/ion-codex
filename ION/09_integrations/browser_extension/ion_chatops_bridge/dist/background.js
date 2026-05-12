const DAEMON_BASE = "http://127.0.0.1:8767";
const ACTION_GATEWAY_DEFAULT_BASE = "http://127.0.0.1:8777";
const ACTION_GATEWAY_BASE_STORAGE_KEY = "ionActionGatewayBase";
const ACTION_GATEWAY_TOKEN_STORAGE_KEY = "ionActionGatewayToken";
const APPROVAL_TOKEN = "ION_CHATOPS_APPROVED";

async function postJson(path, payload) {
  const response = await fetch(`${DAEMON_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return response.json();
}

async function getJson(path) {
  const response = await fetch(`${DAEMON_BASE}${path}`);
  return response.json();
}
async function actionGatewayConfig() {
  if (!chrome.storage?.local) {
    return { base: ACTION_GATEWAY_DEFAULT_BASE, token: "" };
  }
  const stored = await chrome.storage.local.get([ACTION_GATEWAY_BASE_STORAGE_KEY, ACTION_GATEWAY_TOKEN_STORAGE_KEY]);
  return {
    base: String(stored[ACTION_GATEWAY_BASE_STORAGE_KEY] || ACTION_GATEWAY_DEFAULT_BASE).replace(/\/+$/, ""),
    token: String(stored[ACTION_GATEWAY_TOKEN_STORAGE_KEY] || "").trim()
  };
}
async function actionGatewayJson(method, path, payload) {
  const config = await actionGatewayConfig();
  if (!config.token) {
    return {
      ok: false,
      refusal_class: "AUTH_MISSING",
      finding: "ion_action_gateway_token_missing",
      hint: `Set chrome.storage.local ${ACTION_GATEWAY_TOKEN_STORAGE_KEY} so the extension can poll the local Action Gateway.`
    };
  }
  const response = await fetch(`${config.base}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${config.token}`
    },
    body: method === "POST" ? JSON.stringify(payload ?? {}) : undefined
  });
  return response.json();
}

async function validateWithDaemon(packet) {
  return postJson("/actions/validate", packet);
}

async function submitApproved(packet) {
  return postJson("/actions/submit", {
    ...packet,
    approval: {
      approved: true,
      approved_by: "Braden",
      approval_token: APPROVAL_TOKEN
    }
  });
}

function approvedPayload(payload = {}) {
  return {
    ...payload,
    approval: {
      approved: true,
      approved_by: "Braden",
      approval_token: APPROVAL_TOKEN
    }
  };
}

async function requestBridgeApproval(sender, operation, summary, riskClass = "approval_required_mutation") {
  if (typeof sender.tab?.id !== "number") return false;
  const approved = await chrome.tabs.sendMessage(sender.tab.id, {
    type: "ion_chatops_request_bridge_approval",
    operation,
    summary,
    riskClass
  });
  return Boolean(approved?.approved);
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message) return false;

  if (message.type === "ion_chatops_fetch_sev_context") {
    (async () => {
      const result = await getJson("/context/sev/onboarding");
      sendResponse({ ok: Boolean(result?.ok), stage: "context", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "context_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_agent_status") {
    (async () => {
      const result = await getJson("/agent/status");
      sendResponse({ ok: Boolean(result?.ok), stage: "agent_status", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "agent_status_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_agent_queue") {
    (async () => {
      const result = await getJson("/agent/queue");
      sendResponse({ ok: Boolean(result?.ok), stage: "agent_queue", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "agent_queue_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_bounded_agent_status") {
    (async () => {
      const invocationId = String(message.payload?.invocation_id ?? "").trim();
      const suffix = invocationId ? `?invocation_id=${encodeURIComponent(invocationId)}` : "";
      const result = await actionGatewayJson("GET", `/agent/status${suffix}`);
      sendResponse({ ok: Boolean(result?.ok), stage: "bounded_agent_status", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "bounded_agent_status_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_agent_relay_pending") {
    (async () => {
      const invocationId = String(message.payload?.invocation_id ?? "").trim();
      const suffix = invocationId ? `?invocation_id=${encodeURIComponent(invocationId)}` : "";
      const result = await actionGatewayJson("GET", `/agent/relay/pending${suffix}`);
      sendResponse({ ok: Boolean(result?.ok), stage: "agent_relay_pending", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "agent_relay_pending_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_agent_receipts_recent") {
    (async () => {
      const result = await actionGatewayJson("GET", "/agent/receipts/recent?limit=12");
      sendResponse({ ok: Boolean(result?.ok), stage: "agent_receipts_recent", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "agent_receipts_recent_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_agent_invoke_bounded") {
    (async () => {
      const approved = await requestBridgeApproval(sender, "agent_invoke_bounded", "Submit a bounded ION agent invocation packet through the Action Gateway.", "bounded_agent_invocation_approval_required");
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
        return;
      }
      const result = await actionGatewayJson("POST", "/agent/invoke", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "agent_invoke_bounded", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "agent_invoke_bounded_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_agent_relay_respond") {
    (async () => {
      const approved = await requestBridgeApproval(sender, "agent_relay_respond", "Record a bounded relay response without widening authority.", "bounded_agent_relay_response_approval_required");
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
        return;
      }
      const result = await actionGatewayJson("POST", "/agent/relay/respond", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "agent_relay_respond", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "agent_relay_respond_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_agent_control") {
    (async () => {
      const action = String(message.payload?.action ?? "control");
      const approved = await requestBridgeApproval(sender, "agent_control", `Submit bounded agent control action: ${action}.`, "bounded_agent_control_approval_required");
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
        return;
      }
      const result = await actionGatewayJson("POST", "/agent/control", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "agent_control", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "agent_control_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_browser_queue_status") {
    (async () => {
      const result = await actionGatewayJson("GET", "/browser-queue/status?include_packets=1");
      sendResponse({ ok: Boolean(result?.ok), stage: "browser_queue_status", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "browser_queue_status_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_browser_queue_claim") {
    (async () => {
      const result = await actionGatewayJson("POST", "/browser-queue/claim", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "browser_queue_claim", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "browser_queue_claim_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_browser_queue_result") {
    (async () => {
      const result = await actionGatewayJson("POST", "/browser-queue/result", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "browser_queue_result", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "browser_queue_result_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_browser_queue_control") {
    (async () => {
      const payload = { ...(message.payload ?? {}) };
      if (payload.operation === "approve" && !payload.approval) {
        const approved = await requestBridgeApproval(sender, "browser_queue_packet_approval", `Approve queued browser-carrier packet ${payload.packet_id ?? ""}.`, "browser_queue_operator_approval_required");
        if (!approved) {
          sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
          return;
        }
        payload.approval = approvedPayload({}).approval;
      }
      const result = await actionGatewayJson("POST", "/browser-queue/control", payload);
      sendResponse({ ok: Boolean(result?.ok), stage: "browser_queue_control", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "browser_queue_control_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_codex_chat_model") {
    (async () => {
      const result = await getJson("/codex-chat/model");
      sendResponse({ ok: Boolean(result?.ok), stage: "codex_chat_model", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "codex_chat_model_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_codex_chat_turn") {
    (async () => {
      const result = await postJson("/codex-chat/turn", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "codex_chat_turn", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "codex_chat_turn_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_codex_chat_queue") {
    (async () => {
      const result = await postJson("/codex-chat/queue", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "codex_chat_queue", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "codex_chat_queue_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_codex_chat_memory") {
    (async () => {
      const result = await postJson("/codex-chat/memory", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "codex_chat_memory", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "codex_chat_memory_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_asset_capture") {
    (async () => {
      const result = await postJson("/assets/capture", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "asset_capture", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "asset_capture_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_context_pack") {
    (async () => {
      const result = await getJson("/exports/context-pack");
      sendResponse({ ok: Boolean(result?.ok), stage: "context_pack", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "context_pack_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_sandbox_returns") {
    (async () => {
      const result = await getJson("/sandbox/returns");
      sendResponse({ ok: Boolean(result?.ok), stage: "sandbox_returns", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "sandbox_returns_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_docs_browse") {
    (async () => {
      const result = await postJson("/docs/browse", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "docs_browse", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "docs_browse_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_docs_prepare_drop") {
    (async () => {
      const result = await postJson("/docs/prepare-drop", message.payload ?? {});
      sendResponse({ ok: Boolean(result?.ok), stage: "docs_prepare_drop", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "docs_prepare_drop_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_artifact_attachables") {
    (async () => {
      const result = await getJson("/artifacts/attachables");
      sendResponse({ ok: Boolean(result?.ok), stage: "artifact_attachables", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "artifact_attachables_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_artifact_prepare_latest") {
    (async () => {
      const attachables = await getJson("/artifacts/attachables");
      const rows = Array.isArray(attachables?.candidates) ? attachables.candidates : [];
      const candidate = rows.find((row) => row?.attachable && typeof row.path === "string");
      if (!attachables?.ok || !candidate) {
        sendResponse({
          ok: false,
          stage: "artifact_prepare_latest",
          finding: attachables?.ok ? "no_attachable_artifact" : "attachables_unavailable",
          result: attachables
        });
        return;
      }
      const approved = await requestBridgeApproval(
        sender,
        "artifact_prepare_browser_drop",
        `Prepare ${candidate.name ?? candidate.path} (${candidate.size_bytes ?? "unknown"} bytes) for a visible ChatGPT file drop. This will not click Send.`,
        "browser_file_upload_approval_required"
      );
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED", candidate });
        return;
      }
      const result = await postJson("/artifacts/prepare-upload", approvedPayload({ artifact_path: candidate.path }));
      sendResponse({ ok: Boolean(result?.ok), stage: "artifact_prepare_latest", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "artifact_prepare_latest_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_artifact_local_attach_latest") {
    (async () => {
      const attachables = await getJson("/artifacts/attachables");
      const rows = Array.isArray(attachables?.candidates) ? attachables.candidates : [];
      const candidate = rows.find((row) => row?.attachable && typeof row.path === "string");
      if (!attachables?.ok || !candidate) {
        sendResponse({
          ok: false,
          stage: "artifact_local_attach_latest",
          finding: attachables?.ok ? "no_attachable_artifact" : "attachables_unavailable",
          result: attachables
        });
        return;
      }
      const approved = await requestBridgeApproval(
        sender,
        "local_operator_attach_artifact",
        `Let the local ION operator helper attach ${candidate.name ?? candidate.path} (${candidate.size_bytes ?? "unknown"} bytes) to the active ChatGPT composer. This will not click Send.`,
        "local_operator_artifact_attach_approval_required"
      );
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED", candidate });
        return;
      }
      const prepared = await postJson("/artifacts/prepare-upload", approvedPayload({ artifact_path: candidate.path }));
      if (!prepared?.ok) {
        sendResponse({ ok: false, stage: "artifact_prepare_latest", result: prepared });
        return;
      }
      const operatorResult = await postJson("/operator/attach-artifact", approvedPayload({
        download_token: prepared.download_token,
        target_kind: message.payload?.target_kind ?? "attach_button",
        target_rect: message.payload?.target_rect ?? null,
        target_screen_rect: message.payload?.target_screen_rect ?? null,
        composer_rect: message.payload?.composer_rect ?? null,
        viewport: message.payload?.viewport ?? null,
        device_pixel_ratio: message.payload?.device_pixel_ratio ?? null,
        page_url: message.payload?.page_url ?? "",
        captured_at_ms: message.payload?.captured_at_ms ?? null,
        selected_artifact: candidate,
        dry_run: true,
        active_window_required: true,
        file_picker_title_check: true,
        send_after_attach: false
      }));
      if (!operatorResult?.ok) {
        sendResponse({
          ok: false,
          stage: "artifact_local_attach_dry_run",
          result: {
            prepared,
            operator: operatorResult
          }
        });
        return;
      }
      const attachResult = await postJson("/operator/attach-artifact", approvedPayload({
        download_token: prepared.download_token,
        target_kind: message.payload?.target_kind ?? "attach_button",
        target_rect: message.payload?.target_rect ?? null,
        target_screen_rect: message.payload?.target_screen_rect ?? null,
        composer_rect: message.payload?.composer_rect ?? null,
        viewport: message.payload?.viewport ?? null,
        device_pixel_ratio: message.payload?.device_pixel_ratio ?? null,
        page_url: message.payload?.page_url ?? "",
        captured_at_ms: message.payload?.captured_at_ms ?? null,
        selected_artifact: candidate,
        active_window_required: true,
        file_picker_title_check: true,
        send_after_attach: false
      }));
      sendResponse({
        ok: Boolean(attachResult?.ok),
        stage: "artifact_local_attach_latest",
        result: {
          prepared,
          dry_run: operatorResult,
          operator: attachResult
        }
      });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "artifact_local_attach_latest_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_artifact_local_attach_dry_run") {
    (async () => {
      const attachables = await getJson("/artifacts/attachables");
      const rows = Array.isArray(attachables?.candidates) ? attachables.candidates : [];
      const candidate = rows.find((row) => row?.attachable && typeof row.path === "string");
      if (!attachables?.ok || !candidate) {
        sendResponse({
          ok: false,
          stage: "artifact_local_attach_dry_run",
          finding: attachables?.ok ? "no_attachable_artifact" : "attachables_unavailable",
          result: attachables
        });
        return;
      }
      const approved = await requestBridgeApproval(
        sender,
        "local_operator_attach_artifact_dry_run",
        `Dry-run local attach geometry for ${candidate.name ?? candidate.path}. This will not move the mouse or click Send.`,
        "local_operator_geometry_dry_run"
      );
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED", candidate });
        return;
      }
      const prepared = await postJson("/artifacts/prepare-upload", approvedPayload({ artifact_path: candidate.path }));
      if (!prepared?.ok) {
        sendResponse({ ok: false, stage: "artifact_prepare_latest", result: prepared });
        return;
      }
      const operatorResult = await postJson("/operator/attach-artifact", approvedPayload({
        download_token: prepared.download_token,
        target_kind: message.payload?.target_kind ?? "attach_button",
        target_rect: message.payload?.target_rect ?? null,
        target_screen_rect: message.payload?.target_screen_rect ?? null,
        composer_rect: message.payload?.composer_rect ?? null,
        viewport: message.payload?.viewport ?? null,
        device_pixel_ratio: message.payload?.device_pixel_ratio ?? null,
        page_url: message.payload?.page_url ?? "",
        captured_at_ms: message.payload?.captured_at_ms ?? null,
        selected_artifact: candidate,
        dry_run: true,
        active_window_required: true,
        file_picker_title_check: true,
        send_after_attach: false
      }));
      sendResponse({
        ok: Boolean(operatorResult?.ok),
        stage: "artifact_local_attach_dry_run",
        result: {
          prepared,
          operator: operatorResult
        }
      });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "artifact_local_attach_dry_run_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_sandbox_diff_latest") {
    (async () => {
      const returnId = String(message.payload?.return_id ?? "").trim();
      const approved = await requestBridgeApproval(sender, "sandbox_return_diff_preview", `Build a read-only diff preview for sandbox return ${returnId}.`);
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
        return;
      }
      const result = await postJson("/sandbox/returns/diff-preview", approvedPayload({ return_id: returnId }));
      sendResponse({ ok: Boolean(result?.ok), stage: "sandbox_diff_preview", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "sandbox_diff_preview_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_sandbox_queue_latest") {
    (async () => {
      const returnId = String(message.payload?.return_id ?? "").trim();
      const approved = await requestBridgeApproval(sender, "sandbox_return_queue_review", `Queue a bounded Codex review packet for sandbox return ${returnId}.`);
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
        return;
      }
      const result = await postJson("/sandbox/returns/queue-review", approvedPayload({ return_id: returnId }));
      sendResponse({ ok: Boolean(result?.ok), stage: "sandbox_queue_review", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "sandbox_queue_review_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_agent_prepare_next") {
    (async () => {
      const approved = await requestBridgeApproval(sender, "agent_prepare_next", "Create a prepared Codex queue run packet for the next queued ION work request.");
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
        return;
      }
      const result = await postJson("/agent/prepare-next", approvedPayload(message.payload ?? {}));
      sendResponse({ ok: Boolean(result?.ok), stage: "agent_prepare_next", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "agent_prepare_next_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_agent_start_one") {
    (async () => {
      const approved = await requestBridgeApproval(sender, "agent_start_one", "Start one bounded Codex queue runner worker for the next queued ION work request.", "local_execution_approval_required");
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
        return;
      }
      const result = await postJson("/agent/process-one", approvedPayload({ ...(message.payload ?? {}), start: true }));
      sendResponse({ ok: Boolean(result?.ok), stage: "agent_start_one", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "agent_start_one_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_compact_zip") {
    (async () => {
      const approved = await requestBridgeApproval(sender, "compact_runtime_zip", "Create an ION COMPACT_RUNTIME ZIP package using the existing lifecycle packager.");
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
        return;
      }
      const result = await postJson("/exports/lifecycle-zip", approvedPayload({ package_class: "COMPACT_RUNTIME" }));
      sendResponse({ ok: Boolean(result?.ok), stage: "compact_zip", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "compact_zip_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_project_context_sync_zip") {
    (async () => {
      const projectPaths = Array.isArray(message.payload?.project_paths)
        ? message.payload.project_paths.map((path) => String(path ?? "").trim()).filter(Boolean)
        : [];
      const approved = await requestBridgeApproval(
        sender,
        "project_context_sync_zip",
        `Create one ION context sync ZIP from ${projectPaths.length} selected project package(s).`,
        "context_sync_zip_approval_required"
      );
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
        return;
      }
      const result = await postJson("/exports/project-context-sync-zip", approvedPayload({
        ...(message.payload ?? {}),
        project_paths: projectPaths
      }));
      sendResponse({ ok: Boolean(result?.ok), stage: "project_context_sync_zip", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "project_context_sync_zip_exception", error: error.message });
    });
    return true;
  }

  if (message.type === "ion_chatops_safe_full_zip") {
    (async () => {
      const approved = await requestBridgeApproval(sender, "safe_full_project_zip", "Create a safe full-project ZIP package with trunk-preservation checks.");
      if (!approved) {
        sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
        return;
      }
      const result = await postJson("/exports/safe-full-zip", approvedPayload({}));
      sendResponse({ ok: Boolean(result?.ok), stage: "safe_full_zip", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "safe_full_zip_exception", error: error.message });
    });
    return true;
  }

  if (message.type !== "ion_chatops_candidate") return false;

  (async () => {
    const packet = message.packet;
    const validation = await validateWithDaemon(packet);
    if (!validation.accepted) {
      sendResponse({ ok: false, stage: "validate", validation });
      return;
    }

    if (typeof sender.tab?.id !== "number") {
      sendResponse({ ok: false, stage: "approval", finding: "sender_tab_missing" });
      return;
    }

    const approved = await chrome.tabs.sendMessage(sender.tab.id, {
      type: "ion_chatops_request_approval",
      packet,
      validation
    });
    if (!approved?.approved) {
      sendResponse({ ok: false, stage: "approval", finding: "USER_APPROVAL_REJECTED" });
      return;
    }

    const result = await submitApproved(packet);
    sendResponse({ ok: Boolean(result?.ok), stage: "submit", result });
  })().catch((error) => {
    sendResponse({ ok: false, stage: "exception", error: error.message });
  });

  return true;
});
