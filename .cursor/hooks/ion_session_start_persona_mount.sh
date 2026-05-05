#!/usr/bin/env bash
# Deprecated thin wrapper — hooks.json should call ion_session_start_persona_mount.py directly.
exec python3 "$(dirname "$0")/ion_session_start_persona_mount.py"
