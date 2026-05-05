import * as cp from 'child_process';
import * as path from 'path';

export type KernelResult = {
  command: string;
  exitCode: number | null;
  stdout: string;
  stderr: string;
};

export function runKernel(root: string, moduleName: string, args: string[] = []): Promise<KernelResult> {
  const python = process.env.ION_PYTHON ?? 'python3';
  const env = { ...process.env, PYTHONPATH: path.join(root, 'ION', '04_packages') };
  const argv = ['-m', `kernel.${moduleName}`, '--ion-root', root, ...args];
  return new Promise((resolve) => {
    const child = cp.spawn(python, argv, { cwd: root, env });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk) => { stdout += chunk.toString(); });
    child.stderr.on('data', (chunk) => { stderr += chunk.toString(); });
    child.on('close', (code) => resolve({ command: `${python} ${argv.join(' ')}`, exitCode: code, stdout, stderr }));
  });
}

export async function runIonStatus(root: string): Promise<KernelResult> {
  return runKernel(root, 'ion_status', ['--json']);
}

export async function runIonContinue(root: string): Promise<KernelResult> {
  return runKernel(root, 'ion_carrier_continue', ['--carrier', 'cursor', '--operator-message', 'continue', '--json']);
}

export async function runIonAudit(root: string): Promise<KernelResult> {
  return runKernel(root, 'ion_carrier_workflow_audit', ['--json']);
}

export async function runIonCockpitViewModel(root: string): Promise<KernelResult> {
  return runKernel(root, 'ion_cockpit_view_model', ['--write', '--json']);
}
