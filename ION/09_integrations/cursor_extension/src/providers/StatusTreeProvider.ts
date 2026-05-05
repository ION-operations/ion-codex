import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

class IonTreeItem extends vscode.TreeItem {
  constructor(label: string, description?: string, command?: vscode.Command) {
    super(label, vscode.TreeItemCollapsibleState.None);
    this.description = description;
    this.command = command;
  }
}

export class IonStatusTreeProvider implements vscode.TreeDataProvider<IonTreeItem> {
  private readonly onDidChangeTreeDataEmitter = new vscode.EventEmitter<IonTreeItem | undefined | void>();
  readonly onDidChangeTreeData = this.onDidChangeTreeDataEmitter.event;

  constructor(private root: string) {}

  refresh(): void { this.onDidChangeTreeDataEmitter.fire(); }

  getTreeItem(element: IonTreeItem): vscode.TreeItem { return element; }

  getChildren(): IonTreeItem[] {
    const model = this.readModel();
    if (!model) {
      return [new IonTreeItem('Cockpit view model missing', 'run ION: Refresh Cockpit View Model')];
    }
    const top = model.top_bar ?? {};
    const runtime = model.runtime ?? {};
    return [
      new IonTreeItem('Runtime', String(runtime.status ?? 'unknown')),
      new IonTreeItem('Objective', String(top.objective ?? 'none')),
      new IonTreeItem('Hook', String(top.hook_status ?? 'unknown')),
      new IonTreeItem('Spawn Rows', `${top.spawn_count ?? 0}/${top.spawn_rows_total ?? 0}`),
      new IonTreeItem('Returns', `A${top.return_counts?.accepted ?? 0} R${top.return_counts?.rejected ?? 0} P${top.return_counts?.pending ?? 0}`),
      new IonTreeItem('Human Gates', String(top.gate_count ?? 0), { command: 'ion.openHumanGateQueue', title: 'Open Human Gates' }),
      new IonTreeItem('Steward Queue', String(top.steward_queue_count ?? 0), { command: 'ion.openStewardIntegrationQueue', title: 'Open Steward Queue' }),
      new IonTreeItem('Carrier Turn Packet', 'open', { command: 'ion.openActiveCarrierTurnPacket', title: 'Open Carrier Turn Packet' }),
      new IonTreeItem('Open JOC Cockpit', 'webview', { command: 'ion.openCockpit', title: 'Open JOC Cockpit' }),
    ];
  }

  private readModel(): any | undefined {
    const p = path.join(this.root, 'ION', '05_context', 'current', 'ACTIVE_COCKPIT_VIEW_MODEL.json');
    try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return undefined; }
  }
}
