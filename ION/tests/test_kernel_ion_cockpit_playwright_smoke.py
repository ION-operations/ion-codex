import json
import os
import re
import shutil
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
SERVICE_DROPIN_PATH = Path.home() / ".config/systemd/user/ion-mcp-preview.service.d/cockpit-token.conf"
SMOKE_RECEIPT_PATH = (
    REPO_ROOT
    / "ION/05_context/current/codex_cli/playwright_cockpit_pending_smoke_latest.json"
)
SHELL_SMOKE_RECEIPT_PATH = (
    REPO_ROOT
    / "ION/05_context/current/codex_cli/playwright_cockpit_shell_smoke_latest.json"
)


pytestmark = pytest.mark.skipif(
    os.environ.get("ION_RUN_PLAYWRIGHT_SMOKE") != "1",
    reason="live cockpit Playwright smoke is opt-in",
)


def _configured_cockpit_token() -> str:
    explicit = os.environ.get("ION_COCKPIT_TOKEN", "").strip()
    if explicit:
        return explicit
    if not SERVICE_DROPIN_PATH.exists():
        pytest.skip("cockpit token drop-in is not present")
    text = SERVICE_DROPIN_PATH.read_text(encoding="utf-8")
    public = re.search(r'ION_COCKPIT_PUBLIC_TOKEN=([^"\s]+)', text)
    if public:
        return public.group(1).strip()
    invites = re.search(r'ION_COCKPIT_INVITE_TOKENS=([^"\s]+)', text)
    if invites:
        first = invites.group(1).split(",", 1)[0].strip()
        return first.split("=", 1)[-1].strip()
    pytest.skip("cockpit permission token is not configured")


def _chrome_executable() -> str:
    configured = os.environ.get("ION_PLAYWRIGHT_CHROME", "").strip()
    candidates = [
        configured,
        shutil.which("google-chrome") or "",
        shutil.which("chromium") or "",
        shutil.which("chromium-browser") or "",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    pytest.skip("no system Chrome/Chromium executable available")


def _assert_service_ready(base_url: str) -> None:
    request = Request(f"{base_url}/health", headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # pragma: no cover - live smoke diagnostic.
        pytest.skip(f"local ION cockpit service is not reachable: {exc.__class__.__name__}")
    if not payload.get("ok") and not payload.get("accepted"):
        pytest.skip("local ION cockpit service is not ready")


def test_cockpit_chat_submit_shows_pending_and_blocks_duplicate() -> None:
    sync_api = pytest.importorskip("playwright.sync_api")
    base_url = os.environ.get("ION_COCKPIT_BASE_URL", "http://127.0.0.1:8765").rstrip("/")
    token = _configured_cockpit_token()
    chrome = _chrome_executable()
    _assert_service_ready(base_url)

    message_id = f"playwright-pending-smoke-{int(time.time())}"
    message = f"{message_id}: reply exactly playwright-ok"

    with sync_api.sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=chrome,
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto(
                f"{base_url}/cockpit/chat?token={quote(token)}",
                wait_until="domcontentloaded",
            )
            textarea = page.locator('form.capsule-composer textarea[name="message"]')
            send = page.locator('form.capsule-composer button[type="submit"]')

            sync_api.expect(textarea).to_be_visible(timeout=10_000)
            textarea.fill(message)
            send.click()

            sync_api.expect(textarea).to_have_value("", timeout=2_000)
            sync_api.expect(send).to_be_disabled(timeout=2_000)
            sync_api.expect(send).to_have_text(re.compile("Sending", re.I), timeout=2_000)
            sync_api.expect(page.locator(".pending-turn .bubble.user")).to_have_count(1)
            sync_api.expect(page.locator(".pending-turn .bubble.user")).to_contain_text(message)
            sync_api.expect(page.locator(".pending-turn .bubble.assistant.pending")).to_contain_text(
                "Codex is working on this response",
                timeout=2_000,
            )

            page.locator("form.capsule-composer").evaluate(
                "form => form.dispatchEvent(new Event('submit', {bubbles: true, cancelable: true}))"
            )
            sync_api.expect(page.locator(".pending-turn .bubble.user")).to_have_count(1)

            assistant = page.locator(".pending-turn .bubble.assistant:not(.pending)")
            sync_api.expect(assistant).to_contain_text("playwright-ok", timeout=360_000)
            sync_api.expect(send).to_be_enabled(timeout=5_000)
            sync_api.expect(send).to_have_text(re.compile(r"^Send$"), timeout=5_000)

            receipt = {
                "schema_id": "ion.playwright_cockpit_pending_smoke.v1",
                "ok": True,
                "base_url": base_url,
                "message_id": message_id,
                "assertions": [
                    "textarea_cleared_immediately",
                    "send_disabled_with_sending_label",
                    "pending_codex_bubble_visible",
                    "duplicate_submit_guard_preserved_single_user_bubble",
                    "codex_response_captured",
                ],
                "token_value_recorded": False,
            }
            SMOKE_RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
            SMOKE_RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        finally:
            browser.close()


def test_cockpit_joc_shell_navigation_and_memory_surface() -> None:
    sync_api = pytest.importorskip("playwright.sync_api")
    base_url = os.environ.get("ION_COCKPIT_BASE_URL", "http://127.0.0.1:8765").rstrip("/")
    token = _configured_cockpit_token()
    chrome = _chrome_executable()
    _assert_service_ready(base_url)

    with sync_api.sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=chrome,
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        try:
            page = browser.new_page(viewport={"width": 1440, "height": 960})
            page.goto(
                f"{base_url}/cockpit/chat?token={quote(token)}",
                wait_until="domcontentloaded",
            )

            sync_api.expect(page.locator(".capsule-main-chat")).to_be_visible(timeout=10_000)
            sync_api.expect(page.locator(".top-page-tabs")).to_be_visible()
            sync_api.expect(page.locator(".capsule-left-drawer")).to_be_visible()
            sync_api.expect(page.locator(".capsule-right-rail")).to_be_visible()
            sync_api.expect(page.locator(".capsule-activity-strip")).to_be_visible()

            page.locator('[data-left-drawer-target="models"]').click()
            sync_api.expect(page.locator('[data-left-panel="models"]')).to_be_visible()
            sync_api.expect(page.locator('[data-left-drawer-target="models"]')).to_have_class(re.compile("is-active"))

            page.locator('[data-inspector-target="context"]').first.click()
            sync_api.expect(page.locator('[data-inspector-panel="context"]')).to_be_visible()
            sync_api.expect(page.locator('[data-inspector-panel="context"]')).to_contain_text("Memory View")

            page.locator('[data-page-target="context"]').click()
            sync_api.expect(page.locator('[data-page-panel="context"]')).to_be_visible()
            sync_api.expect(page.locator('[data-page-panel="chat"]')).to_be_hidden()
            sync_api.expect(page.locator('[data-page-panel="context"]')).to_contain_text("Memory Strata")
            sync_api.expect(page.locator('[data-page-panel="context"]')).to_contain_text("Contextual Matryoshka")
            sync_api.expect(page.locator('[data-page-panel="context"]')).to_contain_text("Context Route Graph")
            sync_api.expect(page.locator('[data-page-panel="context"] [data-memory-window-class="LIVE_INPUT"]')).to_be_visible()
            sync_api.expect(page.locator('[data-page-panel="context"] [data-memory-window-class="ACTIVE_CONTEXT"]')).to_be_visible()
            capsule_card = page.locator('[data-page-panel="context"] [data-memory-segment-id="context:capsule"]').first
            capsule_card.click()
            sync_api.expect(capsule_card).to_have_class(re.compile("is-selected-memory"))
            sync_api.expect(
                page.locator('[data-page-panel="context"] [data-memory-selection-field="id"]').first
            ).to_contain_text("context:capsule")
            route_edge = page.locator('[data-page-panel="context"] [data-route-edge-id]').first
            route_edge_id = route_edge.get_attribute("data-route-edge-id") or ""
            route_edge.click()
            sync_api.expect(route_edge).to_have_class(re.compile("is-selected-memory"))
            sync_api.expect(
                page.locator('[data-page-panel="context"] [data-memory-selection-field="edge"]').first
            ).to_contain_text(route_edge_id)
            compressed_filter = page.locator('[data-page-panel="context"] [data-route-edge-filter="compressed_to"]').first
            compressed_filter.click()
            sync_api.expect(compressed_filter).to_have_class(re.compile("is-active"))
            sync_api.expect(
                page.locator('[data-page-panel="context"] [data-route-edge-type="compressed_to"]').first
            ).to_be_visible()
            source_group_filters = page.locator('[data-page-panel="context"] [data-source-group-filter]')
            if source_group_filters.count() > 1:
                source_group_filter = source_group_filters.nth(1)
                source_group = source_group_filter.get_attribute("data-source-group-filter") or ""
                source_group_filter.click()
                sync_api.expect(source_group_filter).to_have_class(re.compile("is-active"))
                sync_api.expect(
                    page.locator(f'[data-page-panel="context"] [data-source-ref-lane="{source_group}"]').first
                ).to_be_visible()
                source_group_filters.first.click()
            source_ref = page.locator('[data-page-panel="context"] [data-source-ref]').first
            source_ref_value = source_ref.get_attribute("data-source-ref") or ""
            source_ref.click()
            sync_api.expect(source_ref).to_have_class(re.compile("is-selected-memory"))
            sync_api.expect(
                page.locator('[data-page-panel="context"] [data-memory-selection-field="id"]').first
            ).to_contain_text(source_ref_value)
            trace_event = page.locator('[data-page-panel="context"] [data-trace-event-id]').first
            trace_event_id = trace_event.get_attribute("data-trace-event-id") or ""
            trace_event.click()
            sync_api.expect(trace_event).to_have_class(re.compile("is-selected-memory"))
            sync_api.expect(
                page.locator('[data-page-panel="context"] [data-memory-selection-field="id"]').first
            ).to_contain_text(trace_event_id)
            page.reload(wait_until="domcontentloaded")
            sync_api.expect(page.locator(".capsule-main-chat")).to_be_visible(timeout=10_000)
            page.locator('[data-page-target="context"]').click()
            sync_api.expect(
                page.locator('[data-page-panel="context"] [data-memory-selection-field="id"]').first
            ).to_contain_text(trace_event_id)
            sync_api.expect(
                page.locator('[data-page-panel="context"] [data-trace-event-id]').first
            ).to_have_class(re.compile("is-selected-memory"))

            page.locator('[data-inspector-target="evidence"]').first.click()
            sync_api.expect(page.locator('[data-inspector-panel="evidence"]')).to_be_visible()
            sync_api.expect(page.locator('[data-inspector-panel="evidence"]')).to_contain_text("Timeline")

            page.locator('[data-timeline-filter="task_return"]').click()
            sync_api.expect(page.locator('[data-timeline-filter="task_return"]')).to_have_class(re.compile("is-active"))

            page.locator('[data-page-target="chat"]').click()
            sync_api.expect(page.locator('[data-page-panel="chat"]')).to_be_visible()
            sync_api.expect(page.locator('form.capsule-composer textarea[name="message"]')).to_be_visible()
            chat_turn = page.locator('[data-page-panel="chat"] .bubble[data-chat-turn-id]').first
            chat_turn.click()
            sync_api.expect(chat_turn).to_have_class(re.compile("is-selected-memory"))

            receipt = {
                "schema_id": "ion.playwright_cockpit_shell_smoke.v1",
                "ok": True,
                "base_url": base_url,
                "assertions": [
                    "joc_shell_regions_visible",
                    "left_drawer_models_panel_switches",
                    "right_inspector_context_panel_switches",
                    "context_page_memory_visualization_visible",
                    "memory_segment_selection_updates_selected_node_panel",
                    "route_edge_selection_updates_selected_node_panel",
                    "route_edge_type_filter_activates",
                    "source_ref_drilldown_updates_selected_node_panel",
                    "trace_event_selection_updates_selected_node_panel",
                    "right_inspector_evidence_panel_switches",
                    "bottom_timeline_filter_activates",
                    "chat_turn_selection_highlights_message",
                    "chat_page_restores_composer",
                ],
                "token_value_recorded": False,
            }
            SHELL_SMOKE_RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
            SHELL_SMOKE_RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        finally:
            browser.close()
