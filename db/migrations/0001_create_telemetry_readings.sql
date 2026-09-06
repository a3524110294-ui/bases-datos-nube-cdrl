Create table if not exists telemetry_readings (
    reading_id BIGSERIAL PRIMARY KEY,
    device_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    unit TEXT NOT NULL,
    recorded_at TIMESTAMP NOT NULL

);