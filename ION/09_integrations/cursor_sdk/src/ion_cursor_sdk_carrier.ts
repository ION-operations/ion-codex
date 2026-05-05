import { Agent } from "@cursor/sdk";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, join, resolve } from "node:path";

/**
 * Experimental Cursor SDK carrier adapter for ION.
 *
 * This adapter is deliberately packet-bound. It does not invent ION roles.
 * It refreshes carrier state, reads ACTIVE_CARRIER_TURN_PACKET.json, sends a
 * generated context package to a Cursor SDK agent, and captures the response for
 * kernel.ion_carrier_task_return.
 */

type SpawnRow = {
  index: number;
  role: string;
  context_package_path: string;
};

type CarrierTurnPacket = {
  spawn_queue?: SpawnRow[];
};

const repoRoot = resolve(process.env.ION_REPO_ROOT ?? process.cwd());
const modelId = process.env.ION_CURSOR_MODEL ?? "composer-2";
const maxRows = Number.parseInt(process.env.ION_CURSOR_SDK_MAX_ROWS ?? "1", 10);

function runPython(module: string, args: string[]): void {
  const result = spawnSync("python3", ["-m", module, ...args], {
    cwd: repoRoot,
    env: { ...process.env, PYTHONPATH: join(repoRoot, "ION/04_packages") },
    encoding: "utf8",
    stdio: "inherit",
  });
  if (result.status !== 0) {
    throw new Error(`${module} failed with exit code ${result.status}`);
  }
}

function readJson<T>(relativePath: string): T {
  return JSON.parse(readFileSync(join(repoRoot, relativePath), "utf8")) as T;
}

async function main(): Promise<void> {
  if (!process.env.CURSOR_API_KEY) {
    throw new Error("CURSOR_API_KEY is required for Cursor SDK runs.");
  }

  runPython("kernel.ion_carrier_continue", ["--ion-root", ".", "--carrier", "cursor-sdk", "--operator-message", "continue", "--json"]);

  const turn = readJson<CarrierTurnPacket>("ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json");
  const rows = (turn.spawn_queue ?? []).slice(0, Math.max(1, maxRows));
  if (rows.length === 0) {
    console.log("No spawn rows in ACTIVE_CARRIER_TURN_PACKET.json");
    return;
  }

  const agent = await Agent.create({
    apiKey: process.env.CURSOR_API_KEY,
    model: { id: modelId },
    local: { cwd: repoRoot },
  });

  for (const row of rows) {
    const contextPackage = readFileSync(join(repoRoot, row.context_package_path), "utf8");
    const prompt = [
      "You are a Cursor SDK carrier slot executing an ION generated context package.",
      "Your output MUST begin with exactly: ### CONTEXT PROOF",
      "Do not act as the parent Cursor chat. Do not integrate as STEWARD.",
      "",
      contextPackage,
    ].join("\n");

    const run = await agent.send(prompt);
    let output = "";
    for await (const event of run.stream()) {
      output += typeof event === "string" ? event : JSON.stringify(event) + "\n";
    }

    const capturePath = join(repoRoot, "ION/05_context/current/task_returns", `cursor_sdk_${row.index}_${row.role}.md`);
    mkdirSync(dirname(capturePath), { recursive: true });
    writeFileSync(capturePath, output, "utf8");

    runPython("kernel.ion_carrier_task_return", [
      "--ion-root", ".",
      "--role", row.role,
      "--index", String(row.index),
      "--task-output", capturePath,
      "--json",
    ]);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
