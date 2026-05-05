import * as vscode from 'vscode';
import { findIonRoot, uriForIonPath } from './ionWorkspace';
import { runIonAudit, runIonCockpitViewModel, runIonContinue, runIonStatus } from './ionKernel';
import { openCockpitWebview } from './webviews/cockpit/CockpitWebviewProvider';

async function withRoot(action: (root: string) => Promise<void>) {
  const root = findIonRoot();
  if (!root) {
    vscode.window.showErrorMessage('ION root not found. Expected pyproject.toml and ION/REPO_AUTHORITY.md.');
    return;
  }
  await action(root);
}

async function showResult(title: string, result: { stdout: string; stderr: string; exitCode: number | null; command: string }) {
  const doc = await vscode.workspace.openTextDocument({
    language: 'json',
    content: JSON.stringify({ title, command: result.command, exitCode: result.exitCode, stdout: result.stdout, stderr: result.stderr }, null, 2),
  });
  await vscode.window.showTextDocument(doc, { preview: true });
}

export function registerIonCommands(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('ion.continue', () => withRoot(async (root) => showResult('ION Continue', await runIonContinue(root)))),
    vscode.commands.registerCommand('ion.status', () => withRoot(async (root) => showResult('ION Status', await runIonStatus(root)))),
    vscode.commands.registerCommand('ion.auditCarrierWorkflow', () => withRoot(async (root) => showResult('ION Audit', await runIonAudit(root)))),
    vscode.commands.registerCommand('ion.refreshCockpitViewModel', () => withRoot(async (root) => showResult('ION Cockpit View Model', await runIonCockpitViewModel(root)))),
    vscode.commands.registerCommand('ion.openCockpit', () => withRoot(async (root) => {
      await runIonCockpitViewModel(root);
      openCockpitWebview(context, root);
    })),
    vscode.commands.registerCommand('ion.openActiveCarrierTurnPacket', () => withRoot(async (root) => vscode.window.showTextDocument(uriForIonPath(root, 'ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json')))),
    vscode.commands.registerCommand('ion.openTaskReturnLedger', () => withRoot(async (root) => vscode.window.showTextDocument(uriForIonPath(root, 'ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json')))),
    vscode.commands.registerCommand('ion.openStewardIntegrationQueue', () => withRoot(async (root) => vscode.window.showTextDocument(uriForIonPath(root, 'ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json')))),
    vscode.commands.registerCommand('ion.openHumanGateQueue', () => withRoot(async (root) => vscode.window.showTextDocument(uriForIonPath(root, 'ION/05_context/current/ACTIVE_HUMAN_GATE_QUEUE.json')))),
  );
}
