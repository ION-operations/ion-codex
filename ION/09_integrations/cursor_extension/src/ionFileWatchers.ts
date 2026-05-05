import * as vscode from 'vscode';
import { runIonCockpitViewModel } from './ionKernel';
import { IonStatusTreeProvider } from './providers/StatusTreeProvider';

export function registerIonFileWatchers(context: vscode.ExtensionContext, root: string, provider: IonStatusTreeProvider) {
  const pattern = new vscode.RelativePattern(root, 'ION/05_context/current/*.json');
  const watcher = vscode.workspace.createFileSystemWatcher(pattern);
  const refresh = async () => {
    await runIonCockpitViewModel(root);
    provider.refresh();
  };
  watcher.onDidCreate(refresh, null, context.subscriptions);
  watcher.onDidChange(refresh, null, context.subscriptions);
  watcher.onDidDelete(refresh, null, context.subscriptions);
  context.subscriptions.push(watcher);
}
