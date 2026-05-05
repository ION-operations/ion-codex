import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export function findIonRoot(): string | undefined {
  const folders = vscode.workspace.workspaceFolders ?? [];
  for (const folder of folders) {
    const root = folder.uri.fsPath;
    if (isIonRoot(root)) return root;
    const found = searchDown(root, 4);
    if (found) return found;
  }
  return undefined;
}

function isIonRoot(candidate: string): boolean {
  return fs.existsSync(path.join(candidate, 'pyproject.toml')) && fs.existsSync(path.join(candidate, 'ION', 'REPO_AUTHORITY.md'));
}

function searchDown(root: string, maxDepth: number): string | undefined {
  if (maxDepth < 0) return undefined;
  if (isIonRoot(root)) return root;
  let children: string[] = [];
  try { children = fs.readdirSync(root); } catch { return undefined; }
  for (const child of children) {
    if (child.startsWith('.') || child === 'node_modules') continue;
    const full = path.join(root, child);
    try {
      if (fs.statSync(full).isDirectory()) {
        const found = searchDown(full, maxDepth - 1);
        if (found) return found;
      }
    } catch { /* ignore unreadable */ }
  }
  return undefined;
}

export function uriForIonPath(root: string, relativePath: string): vscode.Uri {
  return vscode.Uri.file(path.join(root, relativePath));
}
