import { operatorApprovalFixture, type OperatorApprovalQueueViewModel } from './operatorApprovalTypes';

export function DryRunDispatchHandoffPanel({ model = operatorApprovalFixture }: { model?: OperatorApprovalQueueViewModel }) {
  return (
    <section className="ion-dry-run-handoff-panel" aria-label="Dry-run dispatch handoff preview">
      <header className="ion-section-header">DRY-RUN HANDOFF PREVIEW</header>
      <pre>{JSON.stringify(model.dry_run_handoff_preview, null, 2)}</pre>
      <div className="ion-non-authority-footer">external_model_call_authorized=false / live_dispatch_claim=false / production_authority=false</div>
    </section>
  );
}
