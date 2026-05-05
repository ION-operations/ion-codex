---
type: signal
from: Atlas
topic: AI-OS evolution wave — protocols, trust, ML serving, observability
created: 2026-04-03
---

# ATLAS AI / OS expansion (planned directions executed as seed wave)

**New packages** (`ATLAS/systems/`):

| Slug | Focus |
|------|--------|
| `ebpf` | Linux eBPF / verifier / kernel hooks |
| `onnx` | Model interchange graph |
| `opentelemetry` | OTel / OTLP observability |
| `grpc` | gRPC / Protobuf RPC |
| `http3` | HTTP/3 + QUIC (RFC 9114 / 9000) |
| `amazon-s3` | S3 REST object API |
| `nvidia-triton-inference-server` | Triton serving |
| `vllm` | vLLM inference engine |
| `nccl` | NVIDIA collectives |
| `openid-connect` | OIDC / identity |
| `tpm2` | TPM 2.0 |
| `uefi` | UEFI firmware interface |
| `linux-security-modules` | LSM / SELinux / AppArmor survey grain |
| `confidential-computing` | TEE survey (strict tiers) |

**Comparative:** `ATLAS/comparative/ai_operating_system_reference_matrices.md`

**Scripts:** `ATLAS/scripts/scaffold_ai_os_wave.py` (generator), `ATLAS/scripts/validate_relations.py` (edge target check)

**MCP package:** `integrates_with` → `grpc`, `http3` (INFERRED distinction / transport layering); sources + ledger **mcp-005** / **mcp-006**

**Indexes:** `systems_index.yaml`, `tag_index.yaml`; `ATLAS/README.md`

**Note:** `kubernetes`, `systemd` were **already** present — not duplicated.

**Evidence:** Survey-grade 00–14 scaffolds — **deepen** **per** **slug** **before** **treating** **as** **audit**-**grade** **A.**
