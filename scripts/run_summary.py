import json

import psycopg2


conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="cdrl",
    user="cdrl_dev",
    password="cdrl_dev_only",
)

with conn.cursor() as cur:
    cur.execute("""
        SELECT device_id, metric_name, metric_value, unit, recorded_at
        FROM telemetry_readings
        ORDER BY recorded_at, device_id
        LIMIT 10;
    """)
    rows = cur.fetchall()

conn.close()

print("Resumen de lecturas de telemetria")
print(json.dumps([
    {
        "device_id": row[0],
        "metric_name": row[1],
        "metric_value": row[2],
        "unit": row[3],
        "recorded_at": row[4].isoformat(),
    }
    for row in rows
], indent=2))
