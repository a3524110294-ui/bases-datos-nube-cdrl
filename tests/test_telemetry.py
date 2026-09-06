import psycopg2
import pytest


def conectar():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="cdrl",
        user="cdrl_dev",
        password="cdrl_dev_only",
    )


insert_sql = "INSERT INTO telemetry_readings (device_id, metric_name, metric_value, unit, recorded_at) VALUES (%s, %s, %s, %s, %s) RETURNING reading_id;"


def test_caso_normal_lectura_valida():
    conn = conectar()
    with conn.cursor() as cur:
        cur.execute(
            insert_sql, ("TEST-NORMAL", "temperature", 25.0, "C", "2026-09-01 10:00:00")
        )
        reading_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    assert reading_id is not None


def test_caso_limite_valor_en_cero():
    conn = conectar()
    with conn.cursor() as cur:
        cur.execute(
            insert_sql,
            ("TEST-LIMITE-1", "battery_level", 0.0, "pct", "2026-09-01 10:00:00"),
        )
        reading_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    assert reading_id is not None


def test_caso_limite_fecha_muy_antigua():
    conn = conectar()
    with conn.cursor() as cur:
        cur.execute(
            insert_sql,
            ("TEST-LIMITE-2", "humidity", 99.9, "pct", "2000-01-01 00:00:00"),
        )
        reading_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    assert reading_id is not None


def test_fallo_declarado_device_id_vacio_es_rechazado():
    conn = conectar()
    with pytest.raises(Exception):
        with conn.cursor() as cur:
            cur.execute(
                insert_sql, (None, "temperature", 20.0, "C", "2026-09-01 10:00:00")
            )
    conn.rollback()
    conn.close()
