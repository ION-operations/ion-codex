-- Development/private cockpit read policy layer.
--
-- This intentionally contains the broad authenticated read posture that was
-- removed from 001_initial_ion_ops.sql. Apply only for Braden's private ION
-- cockpit/runtime project. For public or multi-user deployments, replace this
-- with narrower tenant/operator scoped policies.

create schema if not exists ion_ops;

grant usage on schema ion_ops to authenticated;
grant select on all tables in schema ion_ops to authenticated;

alter default privileges in schema ion_ops
grant select on tables to authenticated;

drop policy if exists automation_events_authenticated_read on ion_ops.automation_events;
create policy automation_events_authenticated_read
on ion_ops.automation_events
for select
to authenticated
using (true);

drop policy if exists carrier_mount_receipts_authenticated_read on ion_ops.carrier_mount_receipts;
create policy carrier_mount_receipts_authenticated_read
on ion_ops.carrier_mount_receipts
for select
to authenticated
using (true);

drop policy if exists service_health_snapshots_authenticated_read on ion_ops.service_health_snapshots;
create policy service_health_snapshots_authenticated_read
on ion_ops.service_health_snapshots
for select
to authenticated
using (true);
