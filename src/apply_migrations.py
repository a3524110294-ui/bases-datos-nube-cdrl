import psycopg2
from pathlib import Path

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="cdrl",
    user="cdrl_dev",
    password="cdrl_dev_only",
)

migration_folder = Path("db/migrations")

for arhivo_sql in sorted(migration_folder.glob("*.sql")):
    print(f"Aplicado: {arhivo_sql.name}")
    sql = arhivo_sql.read_text()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()

conn.close()
print("Todas las migraciones aplicadas correctamente.")
