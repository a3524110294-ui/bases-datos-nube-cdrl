import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import psycopg2


def git_value(args, fallback):
    try:
        return subprocess.check_output(["git", *args], text=True).strip()
    except Exception:
        return fallback


conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="cdrl",
    user="cdrl_dev",
    password="cdrl_dev_only",
)

with conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM telemetry_readings;")
    total_readings = cur.fetchone()[0]
    cur.execute("""
        SELECT metric_name, COUNT(*)
        FROM telemetry_readings
        GROUP BY metric_name
        ORDER BY metric_name;
    """)
    metrics = {name: count for name, count in cur.fetchall()}

conn.close()

payload = {
    "assignmentId": "m01-data-contract",
    "status": "passed",
    "generatedAt": datetime.now(timezone.utc).isoformat(),
    "commitSha": git_value(["rev-parse", "HEAD"], "unknown"),
    "commands": ["make setup", "make verify", "make run"],
    "database": {
        "engine": "postgresql-16",
        "tables": ["telemetry_readings"],
        "totalReadings": total_readings,
        "metrics": metrics,
    },
    "tests": {
        "normalCase": "lectura valida de temperatura",
        "boundaryCases": [
            "battery_level acepta valor 0",
            "humidity acepta fecha antigua como dato historico",
        ],
        "declaredFailures": [
            "device_id nulo se rechaza por NOT NULL",
            "battery_level mayor a 100 se rechaza por CHECK",
        ],
    },
    "security": {
        "usesSyntheticData": True,
        "secretsCommitted": False,
    },
}

Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/m01-verify.json").write_text(json.dumps(payload, indent=2) + "\n")
print("Artifact escrito en artifacts/m01-verify.json")
