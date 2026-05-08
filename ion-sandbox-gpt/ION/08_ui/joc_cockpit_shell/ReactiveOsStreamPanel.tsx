import type { ReactiveStreamEvent } from './reactiveTypes';
import { loopCoverage } from './reactiveTypes';

const requiredLoops = [
  'VISUAL_ISSUE_CLOSURE_LOOP',
  'MISSION_DISPATCH_LOOP',
  'SESSION_HEALTH_LOOP',
  'CONTEXT_PROJECTION_LOOP',
  'CONVERSATIONAL_REPAIR_LOOP',
  'MODEL_COST_QUALITY_LOOP',
];

export function ReactiveOsStreamPanel({ events }: { events: ReactiveStreamEvent[] }) {
  const coverage = loopCoverage(events, requiredLoops);
  return (
    <section className="ion-panel ion-reactive-stream-panel" aria-label="Reactive OS Stream">
      <div className="ion-section-title">REACTIVE OS STREAM</div>
      <div className="ion-loop-coverage" aria-label="Loop coverage">
        <span>LOOP COVERAGE</span>
        {coverage.map((item) => (
          <b key={item.loop} className={item.present ? 'is-covered' : 'is-missing'}>{item.loop}</b>
        ))}
      </div>
      <div className="ion-stream-stack">
        {events.map((event) => (
          <article className={`ion-stream-event is-${event.status.toLowerCase()}`} key={event.eventId}>
            <div className="ion-stream-event-head">
              <time>{event.occurredAt}</time>
              <span>{event.loopId}</span>
              <b>{event.claimLane}</b>
            </div>
            <div className="ion-stream-phase">{event.phase} / {event.status}</div>
            <p>{event.detail}</p>
            <div className="ion-evidence-tags">
              {event.evidenceRefs.map((ref) => <span key={ref}>{ref}</span>)}
              {event.blockedCapabilities.map((cap) => <span className="is-blocked" key={cap}>{cap}</span>)}
            </div>
            <div className="ion-authority-scope">{event.authorityScope}</div>
          </article>
        ))}
      </div>
    </section>
  );
}
