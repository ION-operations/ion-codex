


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


CREATE SCHEMA IF NOT EXISTS "ion_ops";


ALTER SCHEMA "ion_ops" OWNER TO "postgres";


COMMENT ON SCHEMA "ion_ops" IS 'ION operational mirror schema. ION files/Git/receipts remain truth; Supabase indexes selected runtime events for cockpit/query/realtime visibility.';



CREATE OR REPLACE FUNCTION "ion_ops"."set_updated_at"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    AS $$
begin
  new.updated_at = now();
  return new;
end;
$$;


ALTER FUNCTION "ion_ops"."set_updated_at"() OWNER TO "postgres";

SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "ion_ops"."automation_events" (
    "event_id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "occurred_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "observed_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "source_system" "text" DEFAULT 'ion'::"text" NOT NULL,
    "event_type" "text" NOT NULL,
    "severity" "text" DEFAULT 'info'::"text" NOT NULL,
    "carrier_id" "text",
    "carrier_type" "text",
    "agent_tag" "text",
    "branch_id" "text",
    "context_instance_id" "text",
    "packet_id" "text",
    "correlation_id" "text",
    "idempotency_key" "text",
    "title" "text",
    "summary" "text",
    "payload" "jsonb" DEFAULT '{}'::"jsonb" NOT NULL,
    "evidence_refs" "jsonb" DEFAULT '[]'::"jsonb" NOT NULL,
    "source_posture" "jsonb" DEFAULT '{}'::"jsonb" NOT NULL,
    "accepted_state_claim" boolean DEFAULT false NOT NULL,
    "settlement_required" boolean DEFAULT true NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    CONSTRAINT "automation_events_severity_check" CHECK (("severity" = ANY (ARRAY['debug'::"text", 'info'::"text", 'notice'::"text", 'warning'::"text", 'error'::"text", 'critical'::"text"])))
);


ALTER TABLE "ion_ops"."automation_events" OWNER TO "postgres";


COMMENT ON TABLE "ion_ops"."automation_events" IS 'Queryable mirror of ION automation/runtime events. Events are evidence, not accepted state.';



CREATE TABLE IF NOT EXISTS "ion_ops"."carrier_mount_receipts" (
    "mount_receipt_id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "mounted_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "carrier_id" "text",
    "carrier_type" "text" NOT NULL,
    "carrier_instance_id" "text",
    "agent_tag" "text" NOT NULL,
    "conversation_tag" "text",
    "context_instance_id" "text" NOT NULL,
    "branch_id" "text",
    "parent_context_id" "text",
    "current_packet" "text",
    "model_lane" "text",
    "loaded_refs" "jsonb" DEFAULT '[]'::"jsonb" NOT NULL,
    "authority" "jsonb" DEFAULT '{}'::"jsonb" NOT NULL,
    "write_scope" "jsonb" DEFAULT '[]'::"jsonb" NOT NULL,
    "source_posture" "jsonb" DEFAULT '{}'::"jsonb" NOT NULL,
    "return_target" "jsonb" DEFAULT '{}'::"jsonb" NOT NULL,
    "persona_presentation" "jsonb" DEFAULT '{}'::"jsonb" NOT NULL,
    "drift_findings" "jsonb" DEFAULT '[]'::"jsonb" NOT NULL,
    "raw_receipt" "jsonb" DEFAULT '{}'::"jsonb" NOT NULL,
    "accepted_state_authority" boolean DEFAULT false NOT NULL,
    "settlement_required" boolean DEFAULT true NOT NULL,
    "valid" boolean DEFAULT true NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "ion_ops"."carrier_mount_receipts" OWNER TO "postgres";


COMMENT ON TABLE "ion_ops"."carrier_mount_receipts" IS 'Mirror of ION carrier mount receipts. A carrier is not its name; it is a mounted context instance with source posture, authority, and return target.';



CREATE TABLE IF NOT EXISTS "ion_ops"."service_health_snapshots" (
    "snapshot_id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "observed_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "service_name" "text" NOT NULL,
    "service_role" "text",
    "carrier_id" "text",
    "endpoint" "text",
    "host" "text",
    "port" integer,
    "pid" integer,
    "status" "text" DEFAULT 'unknown'::"text" NOT NULL,
    "verdict" "text",
    "version_line" "text",
    "production_authority" boolean DEFAULT false NOT NULL,
    "live_execution_authority" boolean DEFAULT false NOT NULL,
    "health" "jsonb" DEFAULT '{}'::"jsonb" NOT NULL,
    "findings" "jsonb" DEFAULT '[]'::"jsonb" NOT NULL,
    "source_posture" "jsonb" DEFAULT '{}'::"jsonb" NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    CONSTRAINT "service_health_snapshots_status_check" CHECK (("status" = ANY (ARRAY['ready'::"text", 'healthy'::"text", 'degraded'::"text", 'blocked'::"text", 'unknown'::"text", 'offline'::"text"])))
);


ALTER TABLE "ion_ops"."service_health_snapshots" OWNER TO "postgres";


COMMENT ON TABLE "ion_ops"."service_health_snapshots" IS 'Point-in-time mirror of service health observations for ION cockpit/runtime visibility.';



CREATE OR REPLACE VIEW "ion_ops"."v_current_carrier_mounts" AS
 SELECT "agent_tag",
    "carrier_type",
    "carrier_id",
    "context_instance_id",
    "branch_id",
    "current_packet",
    "accepted_state_authority",
    "settlement_required",
    "valid",
    "mounted_at",
    "source_posture",
    "authority",
    "persona_presentation"
   FROM "ion_ops"."carrier_mount_receipts"
  WHERE ("valid" = true)
  ORDER BY "mounted_at" DESC;


ALTER VIEW "ion_ops"."v_current_carrier_mounts" OWNER TO "postgres";


CREATE OR REPLACE VIEW "ion_ops"."v_latest_service_health" AS
 SELECT DISTINCT ON ("service_name") "service_name",
    "service_role",
    "carrier_id",
    "endpoint",
    "host",
    "port",
    "status",
    "verdict",
    "production_authority",
    "live_execution_authority",
    "observed_at",
    "health",
    "findings"
   FROM "ion_ops"."service_health_snapshots"
  ORDER BY "service_name", "observed_at" DESC;


ALTER VIEW "ion_ops"."v_latest_service_health" OWNER TO "postgres";


CREATE OR REPLACE VIEW "ion_ops"."v_recent_automation_events" AS
 SELECT "event_id",
    "occurred_at",
    "source_system",
    "event_type",
    "severity",
    "carrier_id",
    "agent_tag",
    "branch_id",
    "packet_id",
    "title",
    "summary",
    "accepted_state_claim",
    "settlement_required"
   FROM "ion_ops"."automation_events"
  ORDER BY "occurred_at" DESC
 LIMIT 100;


ALTER VIEW "ion_ops"."v_recent_automation_events" OWNER TO "postgres";


CREATE OR REPLACE VIEW "ion_ops"."v_cockpit_overview" AS
 SELECT "now"() AS "generated_at",
    ( SELECT "count"(*) AS "count"
           FROM "ion_ops"."carrier_mount_receipts"
          WHERE ("carrier_mount_receipts"."valid" = true)) AS "mounted_carrier_count",
    ( SELECT "jsonb_agg"("jsonb_build_object"('agent_tag', "v_current_carrier_mounts"."agent_tag", 'carrier_type', "v_current_carrier_mounts"."carrier_type", 'context_instance_id', "v_current_carrier_mounts"."context_instance_id", 'current_packet', "v_current_carrier_mounts"."current_packet", 'settlement_required', "v_current_carrier_mounts"."settlement_required", 'mounted_at', "v_current_carrier_mounts"."mounted_at") ORDER BY "v_current_carrier_mounts"."mounted_at" DESC) AS "jsonb_agg"
           FROM "ion_ops"."v_current_carrier_mounts") AS "mounted_carriers",
    ( SELECT "jsonb_agg"("jsonb_build_object"('service_name', "v_latest_service_health"."service_name", 'port', "v_latest_service_health"."port", 'status', "v_latest_service_health"."status", 'verdict', "v_latest_service_health"."verdict", 'observed_at', "v_latest_service_health"."observed_at") ORDER BY "v_latest_service_health"."service_name") AS "jsonb_agg"
           FROM "ion_ops"."v_latest_service_health") AS "service_health",
    ( SELECT "jsonb_agg"("jsonb_build_object"('event_type', "recent"."event_type", 'severity', "recent"."severity", 'agent_tag', "recent"."agent_tag", 'title', "recent"."title", 'occurred_at', "recent"."occurred_at") ORDER BY "recent"."occurred_at" DESC) AS "jsonb_agg"
           FROM ( SELECT "v_recent_automation_events"."event_id",
                    "v_recent_automation_events"."occurred_at",
                    "v_recent_automation_events"."source_system",
                    "v_recent_automation_events"."event_type",
                    "v_recent_automation_events"."severity",
                    "v_recent_automation_events"."carrier_id",
                    "v_recent_automation_events"."agent_tag",
                    "v_recent_automation_events"."branch_id",
                    "v_recent_automation_events"."packet_id",
                    "v_recent_automation_events"."title",
                    "v_recent_automation_events"."summary",
                    "v_recent_automation_events"."accepted_state_claim",
                    "v_recent_automation_events"."settlement_required"
                   FROM "ion_ops"."v_recent_automation_events"
                  ORDER BY "v_recent_automation_events"."occurred_at" DESC
                 LIMIT 10) "recent") AS "recent_events",
    false AS "accepted_state_claim",
    true AS "settlement_required";


ALTER VIEW "ion_ops"."v_cockpit_overview" OWNER TO "postgres";


ALTER TABLE ONLY "ion_ops"."automation_events"
    ADD CONSTRAINT "automation_events_pkey" PRIMARY KEY ("event_id");



ALTER TABLE ONLY "ion_ops"."carrier_mount_receipts"
    ADD CONSTRAINT "carrier_mount_receipts_pkey" PRIMARY KEY ("mount_receipt_id");



ALTER TABLE ONLY "ion_ops"."service_health_snapshots"
    ADD CONSTRAINT "service_health_snapshots_pkey" PRIMARY KEY ("snapshot_id");



CREATE INDEX "automation_events_agent_tag_idx" ON "ion_ops"."automation_events" USING "btree" ("agent_tag");



CREATE INDEX "automation_events_branch_id_idx" ON "ion_ops"."automation_events" USING "btree" ("branch_id");



CREATE INDEX "automation_events_correlation_id_idx" ON "ion_ops"."automation_events" USING "btree" ("correlation_id");



CREATE INDEX "automation_events_event_type_idx" ON "ion_ops"."automation_events" USING "btree" ("event_type");



CREATE INDEX "automation_events_occurred_at_idx" ON "ion_ops"."automation_events" USING "btree" ("occurred_at" DESC);



CREATE INDEX "automation_events_packet_id_idx" ON "ion_ops"."automation_events" USING "btree" ("packet_id");



CREATE INDEX "automation_events_payload_gin_idx" ON "ion_ops"."automation_events" USING "gin" ("payload");



CREATE INDEX "carrier_mount_receipts_agent_tag_idx" ON "ion_ops"."carrier_mount_receipts" USING "btree" ("agent_tag");



CREATE INDEX "carrier_mount_receipts_branch_id_idx" ON "ion_ops"."carrier_mount_receipts" USING "btree" ("branch_id");



CREATE INDEX "carrier_mount_receipts_context_instance_id_idx" ON "ion_ops"."carrier_mount_receipts" USING "btree" ("context_instance_id");



CREATE INDEX "carrier_mount_receipts_loaded_refs_gin_idx" ON "ion_ops"."carrier_mount_receipts" USING "gin" ("loaded_refs");



CREATE INDEX "carrier_mount_receipts_mounted_at_idx" ON "ion_ops"."carrier_mount_receipts" USING "btree" ("mounted_at" DESC);



CREATE INDEX "carrier_mount_receipts_source_posture_gin_idx" ON "ion_ops"."carrier_mount_receipts" USING "gin" ("source_posture");



CREATE INDEX "service_health_snapshots_health_gin_idx" ON "ion_ops"."service_health_snapshots" USING "gin" ("health");



CREATE INDEX "service_health_snapshots_observed_at_idx" ON "ion_ops"."service_health_snapshots" USING "btree" ("observed_at" DESC);



CREATE INDEX "service_health_snapshots_port_idx" ON "ion_ops"."service_health_snapshots" USING "btree" ("port");



CREATE INDEX "service_health_snapshots_service_name_idx" ON "ion_ops"."service_health_snapshots" USING "btree" ("service_name");



CREATE INDEX "service_health_snapshots_status_idx" ON "ion_ops"."service_health_snapshots" USING "btree" ("status");



CREATE OR REPLACE TRIGGER "automation_events_set_updated_at" BEFORE UPDATE ON "ion_ops"."automation_events" FOR EACH ROW EXECUTE FUNCTION "ion_ops"."set_updated_at"();



CREATE OR REPLACE TRIGGER "carrier_mount_receipts_set_updated_at" BEFORE UPDATE ON "ion_ops"."carrier_mount_receipts" FOR EACH ROW EXECUTE FUNCTION "ion_ops"."set_updated_at"();



CREATE OR REPLACE TRIGGER "service_health_snapshots_set_updated_at" BEFORE UPDATE ON "ion_ops"."service_health_snapshots" FOR EACH ROW EXECUTE FUNCTION "ion_ops"."set_updated_at"();



ALTER TABLE "ion_ops"."automation_events" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "ion_ops"."carrier_mount_receipts" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "ion_ops"."service_health_snapshots" ENABLE ROW LEVEL SECURITY;



