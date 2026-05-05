import type { IonCockpitViewModel, IonLaneTimelineEvent } from './ionRuntimeCockpitTypes';

type Props = { runtime: IonCockpitViewModel };

export function LaneTimelinePanel({ runtime }: Props) {
  const events = runtime.lane_timeline?.events ?? [];
  return (
    <section className="ion-panel ion-lane-timeline-panel">
      <div className="ion-section-title">LANE TIMELINE</div>
      <div className="ion-runtime-grid">
        <Metric label="events" value={String(runtime.lane_timeline?.event_count ?? events.length)} />
        <Metric label="messages" value={String(runtime.lane_timeline?.messages?.length ?? 0)} />
      </div>
      <div className="ion-stream-stack">
        {events.slice(0, 8).map((event) => <LaneEvent event={event} key={event.id} />)}
        {events.length === 0 && <div className="ion-empty-state">NO LANE EVENTS PROJECTED</div>}
      </div>
    </section>
  );
}

function LaneEvent({ event }: { event: IonLaneTimelineEvent }) {
  const lane = `${event.requested_lane ?? 'unknown'} -> ${event.effective_lane ?? 'unknown'}`;
  return (
    <article className={`ion-stream-event is-${event.status}`}>
      <div className="ion-stream-event-head">
        <span>{event.organ}</span>
        <span>{lane}</span>
        <b>{event.status}</b>
      </div>
      <p>{event.lane_change_reason || event.receipt_id || event.source_path || event.message_id}</p>
    </article>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="ion-runtime-metric"><span>{label}</span><b>{value}</b></div>;
}
