import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export function CursorHookStatePanel({ runtime }: { runtime: IonCockpitViewModel }) {
  return (
    <section className="ion-panel ion-hook-state-panel">
      <div className="ion-section-title">CURSOR HOOK / HOST STATE</div>
      <div className="ion-path-list">
        <div className="ion-path-row"><span>hook</span><code>{runtime.top_bar.hook_status}</code></div>
        <div className="ion-path-row"><span>path</span><code>{runtime.source_paths.hook}</code></div>
        <div className="ion-path-row"><span>mode</span><code>{runtime.runtime.mode}</code></div>
        <div className="ion-path-row"><span>shell</span><code>{runtime.runtime.shell_root}</code></div>
      </div>
    </section>
  );
}
