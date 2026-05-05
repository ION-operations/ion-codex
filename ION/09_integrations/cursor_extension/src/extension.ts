import * as vscode from 'vscode';
import { findIonRoot } from './ionWorkspace';
import { registerIonCommands } from './ionCommands';
import { registerIonFileWatchers } from './ionFileWatchers';
import { runIonCockpitViewModel } from './ionKernel';
import { IonStatusTreeProvider } from './providers/StatusTreeProvider';

export async function activate(context: vscode.ExtensionContext) {
  registerIonCommands(context);
  const root = findIonRoot();
  if (!root) {
    vscode.window.registerTreeDataProvider('ionStatus', new IonStatusTreeProvider(''));
    return;
  }
  await runIonCockpitViewModel(root);
  const statusProvider = new IonStatusTreeProvider(root);
  vscode.window.registerTreeDataProvider('ionStatus', statusProvider);
  registerIonFileWatchers(context, root, statusProvider);
}

export function deactivate() {}
