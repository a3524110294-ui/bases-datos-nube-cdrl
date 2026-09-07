CREATE TABLE IF NOT EXISTS telemetry_readings (
    reading_id BIGSERIAL PRIMARY KEY,
    device_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    unit TEXT NOT NULL,
    recorded_at TIMESTAMP NOT NULL,
    CONSTRAINT telemetry_metric_name_valida CHECK (
        metric_name IN ('temperature', 'humidity', 'battery_level')
    ),
    CONSTRAINT telemetry_unit_valida CHECK (
        unit IN ('C', 'pct')
    ),
    CONSTRAINT telemetry_battery_range CHECK (
        metric_name <> 'battery_level' OR metric_value BETWEEN 0 AND 100
    ),
    CONSTRAINT telemetry_humidity_range CHECK (
        metric_name <> 'humidity' OR metric_value BETWEEN 0 AND 100
    )

);

DELETE FROM telemetry_readings a
USING telemetry_readings b
WHERE a.ctid < b.ctid
  AND a.device_id = b.device_id
  AND a.metric_name = b.metric_name
  AND a.recorded_at = b.recorded_at;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'telemetry_metric_name_valida'
    ) THEN
        ALTER TABLE telemetry_readings
        ADD CONSTRAINT telemetry_metric_name_valida
        CHECK (metric_name IN ('temperature', 'humidity', 'battery_level'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'telemetry_unit_valida'
    ) THEN
        ALTER TABLE telemetry_readings
        ADD CONSTRAINT telemetry_unit_valida
        CHECK (unit IN ('C', 'pct'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'telemetry_battery_range'
    ) THEN
        ALTER TABLE telemetry_readings
        ADD CONSTRAINT telemetry_battery_range
        CHECK (metric_name <> 'battery_level' OR metric_value BETWEEN 0 AND 100);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'telemetry_humidity_range'
    ) THEN
        ALTER TABLE telemetry_readings
        ADD CONSTRAINT telemetry_humidity_range
        CHECK (metric_name <> 'humidity' OR metric_value BETWEEN 0 AND 100);
    END IF;
END $$;

CREATE UNIQUE INDEX IF NOT EXISTS telemetry_readings_seed_unico
ON telemetry_readings (device_id, metric_name, recorded_at);
