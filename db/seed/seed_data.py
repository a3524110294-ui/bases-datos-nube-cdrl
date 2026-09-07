import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="cdrl",
    user="cdrl_dev",
    password="cdrl_dev_only",
)

lecturas_de_prueba = [
    ("SENSOR-01", "temperature", 22.5, "C", "2026-09-01 09:00:00"),
    ("SENSOR-01", "temperature", 23.1, "C", "2026-09-01 13:00:00"),
    ("SENSOR-02", "humidity", 55.0, "pct", "2026-09-01 09:00:00"),
    ("SENSOR-02", "battery_level", 87.0, "pct", "2026-09-01 09:00:00"),
]

insert_sql = """
INSERT INTO telemetry_readings (device_id, metric_name, metric_value, unit, recorded_at)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (device_id, metric_name, recorded_at) DO UPDATE SET
    metric_value = EXCLUDED.metric_value,
    unit = EXCLUDED.unit;
"""

with conn.cursor() as cur:
    for lectura in lecturas_de_prueba:
        cur.execute(insert_sql, lectura)

conn.commit()
conn.close()
print(f"Se insertaron {len(lecturas_de_prueba)} lecturas de prueba.")
