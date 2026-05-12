import { useCallback, useEffect, useState } from 'react';
import { JocCockpitShell } from './JocCockpitShell';
import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

type LoadState = {
  model?: IonCockpitViewModel;
  error?: string;
  loading: boolean;
};

export function LocalCockpitApp() {
  const [state, setState] = useState<LoadState>({ loading: true });

  const refresh = useCallback(async () => {
    try {
      const response = await fetch('/model.json', { headers: { Accept: 'application/json' }, cache: 'no-store' });
      if (!response.ok) {
        throw new Error(`model_http_${response.status}`);
      }
      const model = await response.json() as IonCockpitViewModel;
      setState({ model, loading: false });
    } catch (error) {
      setState((previous) => ({
        model: previous.model,
        loading: false,
        error: error instanceof Error ? error.message : 'model_fetch_failed',
      }));
    }
  }, []);

  useEffect(() => {
    refresh();
    const timer = window.setInterval(refresh, 20000);
    return () => window.clearInterval(timer);
  }, [refresh]);

  if (state.model) {
    return <JocCockpitShell runtimeProjection={state.model} onRuntimeRefresh={refresh} />;
  }

  return (
    <main className="ion-joc-shell" data-mode="local-model-loading">
      <header className="ion-topbar">
        <div className="ion-brand">ION/JOC LOCAL</div>
        <div className="ion-state-strip"><span>{state.loading ? 'LOADING MODEL' : 'MODEL UNAVAILABLE'}</span></div>
      </header>
      <section className="ion-main-work-surface">
        <section className="ion-panel ion-hero-panel">
          <div className="ion-section-title">LOCAL COCKPIT MODEL</div>
          <h1>{state.error ?? 'Waiting for /model.json'}</h1>
          <div className="ion-runtime-source-note">No production or live execution authority is granted by this UI.</div>
        </section>
      </section>
    </main>
  );
}
