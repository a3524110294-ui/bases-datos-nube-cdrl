import time
import psycopg2
from pathlib import Path


def conectar_con_reintentos(intentos=10, espera=2):
    for intento in range(1, intentos + 1):
        try:
            return psycopg2.connect(
                host="localhost",
                port=5432,
                database="cdrl",
                user="cdrl_dev",
                password="cdrl_dev_only",
            )
        except psycopg2.OperationalError as error:
            print(f"Postgres aun no esta listo (intento {intento}/{intentos}): {error}")
            time.sleep(espera)
    raise SystemExit("No se pudo conectar a Postgres despues de varios intentos.")


conn = conectar_con_reintentos()

migration_folder = Path("db/migrations")

for arhivo_sql in sorted(migration_folder.glob("*.sql")):
    print(f"Aplicado: {arhivo_sql.name}")
    sql = arhivo_sql.read_text()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()

conn.close()
print("Todas las migraciones aplicadas correctamente.")
