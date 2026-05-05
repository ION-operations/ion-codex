# /ion-cockpit

Run the ION cockpit projection command and open the live cockpit view model.

Required action:

```bash
PYTHONPATH=ION/04_packages python3 -m kernel.ion_cockpit_view_model --ion-root . --write --json
```

Then open:

```text
ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json
```

If the Cursor extension scaffold is installed, use command palette action:

```text
ION: Open JOC Cockpit
```

Do not infer cockpit state from chat memory. Use the kernel-generated view model.
