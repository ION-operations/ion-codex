import { useState } from 'react';
import type { IonCockpitViewModel } from './ionRuntimeCockpitTypes';

export function ServiceConsolePanel({ runtime, onRuntimeRefresh }: { runtime: IonCockpitViewModel; onRuntimeRefresh?: () => void }) {
  const consoleModel = runtime.service_console;
  const services = consoleModel?.services ?? [];
  const [pendingUnit, setPendingUnit] = useState<string | null>(null);
  const [lastResult, setLastResult] = useState<string>('');

  async function restartService(unit: string, confirmation: string) {
    setPendingUnit(unit);
    setLastResult('');
    try {
      const body = new URLSearchParams({ unit, confirmation });
      const response = await fetch('/cockpit/services/restart', {
        method: 'POST',
        headers: { Accept: 'application/json', 'Content-Type': 'application/x-www-form-urlencoded' },
        body,
      });
      const payload = await response.json().catch(() => ({}));
      setLastResult(String(payload.finding ?? (response.ok ? 'service_restart_requested' : 'service_restart_failed')));
      onRuntimeRefresh?.();
    } catch (error) {
      setLastResult(error instanceof Error ? error.name : 'service_restart_request_failed');
    } finally {
      setPendingUnit(null);
    }
  }

  return (
    <section className="ion-panel ion-service-console-panel">
      <div className="ion-section-title">LOCAL SERVICE CONSOLE</div>
      <div className={`ion-runtime-verdict is-${consoleModel?.verdict ?? 'unknown'}`}>{consoleModel?.verdict ?? 'unknown'}</div>
      <div className="ion-runtime-objective">{consoleModel?.headline ?? 'NO SERVICE CONSOLE MODEL'}</div>
      <div className="ion-runtime-source-note">{consoleModel?.operator_message ?? 'Visibility only. Restart buttons require explicit click.'}</div>
      <div className="ion-service-console-grid">
        {services.map((service) => {
          const unit = String(service.unit ?? '');
          const confirmation = String(service.restart_confirmation ?? '');
          const disabled = !unit || !confirmation || pendingUnit === unit;
          return (
            <article className={`ion-runtime-card is-${service.severity ?? 'watch'}`} key={unit || String(service.id)}>
              <div className="ion-runtime-card-head"><b>{String(service.label ?? service.id ?? 'service')}</b><span>{String(service.status ?? 'unknown')}</span></div>
              <p>{String(service.role ?? '')}</p>
              <code>{unit}</code>
              {service.finding && <p>{String(service.finding)}</p>}
              <button className="ion-service-action" type="button" disabled={disabled} onClick={() => restartService(unit, confirmation)}>
                {pendingUnit === unit ? 'REQUESTING' : String(service.fix_label ?? 'RESTART')}
              </button>
            </article>
          );
        })}
      </div>
      {services.length === 0 && <div className="ion-empty-state">NO SERVICE CONSOLE MODEL</div>}
      {lastResult && <div className="ion-runtime-source-note">LAST SERVICE ACTION: {lastResult}</div>}
    </section>
  );
}
