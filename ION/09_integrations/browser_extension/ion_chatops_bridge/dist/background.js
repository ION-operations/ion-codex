const DAEMON_BASE = "http://127.0.0.1:8767";
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

  if (message.type === "ion_chatops_context_pack") {
    (async () => {
      const result = await getJson("/exports/context-pack");
      sendResponse({ ok: Boolean(result?.ok), stage: "context_pack", result });
    })().catch((error) => {
      sendResponse({ ok: false, stage: "context_pack_exception", error: error.message });
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
